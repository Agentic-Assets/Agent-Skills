"""
Pure-Python CRE underwriting engine.

This module is the reference implementation of the cash-flow and return math.
`build_model.py` writes an Excel workbook whose live formulas mirror this logic,
and `verify_model.py` recalculates that workbook and compares Excel's answers
against this engine's answers. If they agree, the workbook's formulas are
provably consistent with the documented math.

Conventions (all of these are documented in references/metric-definitions.md):
  - All rates are decimal fractions: 6.5% is 0.065, never 6.5.
  - Vacancy & credit loss applies to Potential Gross Income (PGI).
  - NOI is before capital costs (reserve, TI, LC) and before debt service.
  - Exit value divides the exit cap into FORWARD NOI (year N+1), not year N.
  - Debt yield at origination uses the ORIGINAL loan amount, not the balance.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

# --------------------------------------------------------------------------
# Financial primitives
# --------------------------------------------------------------------------


def pmt(rate: float, nper: int, pv: float) -> float:
    """Level payment per period. Returns a POSITIVE number for a positive loan."""
    if nper <= 0:
        return 0.0
    if rate == 0:
        return pv / nper
    return pv * rate / (1 - (1 + rate) ** -nper)


def remaining_balance(rate: float, nper: int, pv: float, periods_paid: int) -> float:
    """Balance after `periods_paid` level payments on an amortizing loan."""
    if pv <= 0:
        return 0.0
    if periods_paid <= 0:
        return pv
    if rate == 0:
        return max(0.0, pv - pmt(rate, nper, pv) * periods_paid)
    p = pmt(rate, nper, pv)
    bal = pv * (1 + rate) ** periods_paid - p * (((1 + rate) ** periods_paid - 1) / rate)
    return max(0.0, bal)


def npv(rate: float, cashflows: list[float]) -> float:
    """NPV of cashflows occurring at t=1..n (Excel NPV convention)."""
    return sum(cf / (1 + rate) ** (i + 1) for i, cf in enumerate(cashflows))


def irr(cashflows: list[float], lo: float = -0.9999, hi: float = 10.0) -> float | None:
    """
    IRR by bisection. Returns None when undefined (no sign change, or no root
    in the bracket) rather than a misleading number.
    """
    if not cashflows or all(cf >= 0 for cf in cashflows) or all(cf <= 0 for cf in cashflows):
        return None

    def f(r: float) -> float:
        return sum(cf / (1 + r) ** t for t, cf in enumerate(cashflows))

    try:
        f_lo, f_hi = f(lo), f(hi)
    except (ZeroDivisionError, OverflowError):
        return None
    if f_lo * f_hi > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        f_mid = f(mid)
        if abs(f_mid) < 1e-9:
            return mid
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


# --------------------------------------------------------------------------
# Assumption loading & validation
# --------------------------------------------------------------------------

RATE_FIELDS = [
    ("revenue", "rent_growth"),
    ("revenue", "stabilized_occupancy"),
    ("revenue", "vacancy_credit_loss"),
    ("expenses", "opex_ratio"),
    ("expenses", "management_fee_pct"),
    ("expenses", "expense_growth"),
    ("debt", "ltv"),
    ("debt", "interest_rate"),
    ("exit", "exit_cap_rate"),
    ("exit", "disposition_cost_pct"),
    ("acquisition", "acquisition_cost_pct"),
    ("returns", "discount_rate"),
]


class AssumptionError(ValueError):
    """Raised when assumptions are structurally invalid or unit-suspicious."""


def _get(d: dict, *path, default=None):
    cur = d
    for p in path:
        if not isinstance(cur, dict) or p not in cur or cur[p] is None:
            return default
        cur = cur[p]
    return cur


def validate(a: dict) -> list[str]:
    """
    Returns a list of warnings. Raises AssumptionError on unrecoverable problems.

    The unit checks matter more than they look: entering 6.5 instead of 0.065 for
    a cap rate produces a workbook that computes cleanly and is off by 100x, which
    is exactly the kind of error that survives review.
    """
    warnings: list[str] = []

    ptype = _get(a, "deal", "property_type", default="other")
    sf = _get(a, "property", "rentable_sf")
    units = _get(a, "property", "units")
    if ptype == "multifamily":
        if not units:
            raise AssumptionError("multifamily requires property.units")
    elif not sf:
        raise AssumptionError(f"{ptype} requires property.rentable_sf")

    price = _get(a, "acquisition", "purchase_price")
    if not price or price <= 0:
        raise AssumptionError("acquisition.purchase_price must be > 0")

    hold = _get(a, "exit", "hold_years")
    if not hold or hold < 1:
        raise AssumptionError("exit.hold_years must be >= 1")
    if hold > 30:
        raise AssumptionError("exit.hold_years > 30 is out of supported range")

    # Unit sanity: any "rate" field above 1.0 is almost certainly percent-points.
    for section, keyname in RATE_FIELDS:
        v = _get(a, section, keyname)
        if v is None:
            continue
        if v > 1.0:
            raise AssumptionError(
                f"{section}.{keyname} = {v}. Rates must be decimal fractions "
                f"(6.5% is 0.065, not 6.5). Divide by 100."
            )
        if v < 0:
            raise AssumptionError(f"{section}.{keyname} = {v} cannot be negative")

    exp_mode = _get(a, "expenses", "mode", default="ratio")
    if exp_mode not in ("ratio", "line_items"):
        raise AssumptionError("expenses.mode must be 'ratio' or 'line_items'")

    recovery = _get(a, "revenue", "recovery_structure", default="gross")
    if exp_mode == "ratio" and recovery not in ("gross", None):
        raise AssumptionError(
            "Expense recoveries require expenses.mode='line_items'. An OpEx ratio is a "
            "percentage of EGI, and recoveries feed EGI, so combining them is circular. "
            "Use line_items with recoverable flags for NNN/NN/modified-gross deals."
        )

    # Underwriting-convention warnings (not errors — a thesis can justify these).
    exit_cap = _get(a, "exit", "exit_cap_rate")
    if exit_cap:
        try:
            going_in_cap = compute(a)["returns"]["going_in_cap_rate"]
        except Exception:  # structural problems surface elsewhere; skip the soft check
            going_in_cap = None
    if exit_cap and going_in_cap:
        if exit_cap < going_in_cap:
            warnings.append(
                f"Exit cap {exit_cap:.2%} is TIGHTER than going-in cap {going_in_cap:.2%}. "
                "This assumes cap-rate compression and needs an explicit, documented thesis."
            )
        elif exit_cap < going_in_cap + 0.0025:
            warnings.append(
                f"Exit cap {exit_cap:.2%} is within 25 bps of going-in {going_in_cap:.2%}. "
                "Convention is +25 to +50 bps for asset aging."
            )

    disc = _get(a, "returns", "discount_rate")
    growth = _get(a, "revenue", "rent_growth", default=0)
    if disc is not None and disc <= growth:
        warnings.append(
            f"Discount rate {disc:.2%} <= rent growth {growth:.2%}. "
            "The DCF value will be unstable/meaningless."
        )

    ltv = _get(a, "debt", "ltv")
    if ltv and ltv > 0.80:
        warnings.append(f"LTV {ltv:.0%} exceeds the 80% ceiling most lenders will quote.")

    return warnings


# --------------------------------------------------------------------------
# Projection
# --------------------------------------------------------------------------


@dataclass
class YearRow:
    year: int
    gpr: float = 0.0
    recoveries: float = 0.0
    other_income: float = 0.0
    pgi: float = 0.0
    vacancy_loss: float = 0.0
    egi: float = 0.0
    opex_base: float = 0.0
    mgmt_fee: float = 0.0
    opex_total: float = 0.0
    noi: float = 0.0
    capex_reserve: float = 0.0
    ti: float = 0.0
    lc: float = 0.0
    capital_total: float = 0.0
    cfbds: float = 0.0
    debt_begin: float = 0.0
    interest: float = 0.0
    principal: float = 0.0
    debt_service: float = 0.0
    debt_end: float = 0.0
    cfads: float = 0.0
    dscr: float | None = None
    debt_yield_orig: float | None = None
    debt_yield_current: float | None = None
    ltv_current: float | None = None


@dataclass
class Model:
    rows: list[YearRow] = field(default_factory=list)
    exit: dict[str, float] = field(default_factory=dict)
    returns: dict[str, Any] = field(default_factory=dict)
    debt: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


def gpr_for_year(a: dict, y: int) -> float:
    """
    Gross potential rent in year `y` (1-indexed) at 100% occupancy.

    Each revenue mode escalates differently, and the workbook mirrors this
    exactly. In rent_roll mode every lease grows at ITS OWN contractual bump,
    not at the market rate — compounding a fixed-bump lease at market growth is
    one of the most common ways a model quietly overstates revenue.
    """
    ptype = _get(a, "deal", "property_type", default="other")
    mode = _get(a, "revenue", "mode", default="simple")
    g = _get(a, "revenue", "rent_growth", default=0.0)

    if mode == "rent_roll":
        tenants = _get(a, "revenue", "tenants", default=[])
        if tenants:
            return sum(
                t["sf"] * t["rent_psf"] * (1 + t.get("escalation", g)) ** (y - 1)
                for t in tenants
            )

    if mode == "unit_mix" or ptype == "multifamily":
        mix = _get(a, "revenue", "unit_types")
        if mix:
            base = sum(u["count"] * u["rent_month"] * 12 for u in mix)
        else:
            base = (
                _get(a, "property", "units", default=0)
                * _get(a, "revenue", "market_rent_month", default=0) * 12
            )
        return base * (1 + g) ** (y - 1)

    sf = _get(a, "property", "rentable_sf", default=0)
    return sf * _get(a, "revenue", "market_rent_psf", default=0) * (1 + g) ** (y - 1)


def _size_loan(a: dict, noi_1: float) -> float:
    if not _get(a, "debt", "enabled", default=False):
        return 0.0
    method = _get(a, "debt", "sizing_method", default="ltv")
    price = _get(a, "acquisition", "purchase_price")
    rate = _get(a, "debt", "interest_rate", default=0)
    amort = _get(a, "debt", "amort_years", default=30)

    if method == "amount":
        return float(_get(a, "debt", "loan_amount", default=0))
    if method == "dscr":
        dscr_min = _get(a, "debt", "dscr_min", default=1.25)
        if rate == 0 or amort <= 0:
            return 0.0
        annual_constant = pmt(rate / 12, int(amort * 12), 1.0) * 12
        if annual_constant <= 0:
            return 0.0
        return (noi_1 / dscr_min) / annual_constant
    return price * _get(a, "debt", "ltv", default=0)


def compute(a: dict) -> dict:
    """Run the full projection. Returns a plain dict (JSON-serialisable)."""
    ptype = _get(a, "deal", "property_type", default="other")
    sf = _get(a, "property", "rentable_sf", default=0) or 0
    units = _get(a, "property", "units", default=0) or 0
    price = _get(a, "acquisition", "purchase_price")
    hold = int(_get(a, "exit", "hold_years"))

    rent_growth = _get(a, "revenue", "rent_growth", default=0.0)
    vac = _get(a, "revenue", "vacancy_credit_loss", default=0.0)
    other_inc = _get(a, "revenue", "other_income_annual", default=0.0)
    other_growth = _get(a, "revenue", "other_income_growth", default=rent_growth)

    exp_mode = _get(a, "expenses", "mode", default="ratio")
    exp_growth = _get(a, "expenses", "expense_growth", default=0.0)
    mgmt_pct = _get(a, "expenses", "management_fee_pct", default=0.0)
    recovery_ratio = _get(a, "revenue", "recovery_ratio", default=0.0)

    # Project hold + 1 years: the extra year supplies FORWARD NOI for the exit.
    n_years = hold + 1
    rows: list[YearRow] = []

    # ---- Revenue, expenses, NOI -------------------------------------------
    egi_year1 = None
    for y in range(1, n_years + 1):
        r = YearRow(year=y)
        esc = (1 + rent_growth) ** (y - 1)
        r.gpr = gpr_for_year(a, y)
        r.other_income = other_inc * (1 + other_growth) ** (y - 1)

        # Recoveries need absolute recoverable dollars, so they exist only in
        # line_items mode (validate() enforces this).
        recoverable = 0.0
        if exp_mode == "line_items":
            for li in _get(a, "expenses", "line_items", default=[]):
                amt = li["amount_annual"] * (1 + li.get("growth", exp_growth)) ** (y - 1)
                if li.get("recoverable"):
                    recoverable += amt
            r.recoveries = recoverable * recovery_ratio

        r.pgi = r.gpr + r.recoveries + r.other_income
        r.vacancy_loss = r.pgi * vac
        r.egi = r.pgi - r.vacancy_loss
        if y == 1:
            egi_year1 = r.egi

        if exp_mode == "line_items":
            r.opex_base = sum(
                li["amount_annual"] * (1 + li.get("growth", exp_growth)) ** (y - 1)
                for li in _get(a, "expenses", "line_items", default=[])
            )
        else:
            # Ratio applies to YEAR-1 EGI, then inflates at expense growth.
            # Applying the ratio to each year's EGI would force expenses to grow
            # at the revenue rate and erase any margin expansion or compression.
            r.opex_base = egi_year1 * _get(a, "expenses", "opex_ratio", default=0.0) * (
                1 + exp_growth
            ) ** (y - 1)

        r.mgmt_fee = r.egi * mgmt_pct
        r.opex_total = r.opex_base + r.mgmt_fee
        r.noi = r.egi - r.opex_total

        # ---- Capital costs -------------------------------------------------
        if ptype == "multifamily":
            reserve_per_unit = _get(a, "expenses", "capex_reserve_per_unit", default=0.0)
            r.capex_reserve = units * reserve_per_unit * (1 + exp_growth) ** (y - 1)
            turn_rate = _get(a, "expenses", "turnover_rate", default=0.0)
            turn_cost = _get(a, "expenses", "turn_cost_per_unit", default=0.0)
            r.ti = units * turn_rate * turn_cost * (1 + exp_growth) ** (y - 1)
            r.lc = 0.0
        else:
            r.capex_reserve = (
                sf * _get(a, "expenses", "capex_reserve_psf", default=0.0)
                * (1 + exp_growth) ** (y - 1)
            )
            roll_pct = _get(a, "expenses", "rollover_pct_annual", default=0.0)
            renew = _get(a, "expenses", "renewal_probability", default=0.6)
            roll_sf = sf * roll_pct
            ti_blend = renew * _get(a, "expenses", "ti_renewal_psf", default=0.0) + (
                1 - renew
            ) * _get(a, "expenses", "ti_new_psf", default=0.0)
            lc_blend = renew * _get(a, "expenses", "lc_renewal_pct", default=0.0) + (
                1 - renew
            ) * _get(a, "expenses", "lc_new_pct", default=0.0)
            term = _get(a, "expenses", "new_lease_term_years", default=5)
            rent_psf_y = _get(a, "revenue", "market_rent_psf", default=0.0) * esc
            r.ti = roll_sf * ti_blend
            r.lc = roll_sf * rent_psf_y * term * lc_blend

        r.capital_total = r.capex_reserve + r.ti + r.lc
        r.cfbds = r.noi - r.capital_total
        rows.append(r)

    # ---- Debt --------------------------------------------------------------
    loan = _size_loan(a, rows[0].noi)
    rate = _get(a, "debt", "interest_rate", default=0.0)
    io_years = int(_get(a, "debt", "io_years", default=0))
    amort_years = int(_get(a, "debt", "amort_years", default=30))
    monthly_pmt = pmt(rate / 12, amort_years * 12, loan) if loan > 0 else 0.0

    balance = loan
    for r in rows:
        r.debt_begin = balance
        if loan <= 0:
            r.interest = r.principal = r.debt_service = r.debt_end = 0.0
        elif r.year <= io_years:
            r.interest = balance * rate
            r.principal = 0.0
            r.debt_service = r.interest
            r.debt_end = balance
        else:
            months_paid_before = (r.year - io_years - 1) * 12
            bal_start = remaining_balance(rate / 12, amort_years * 12, loan, months_paid_before)
            bal_end = remaining_balance(rate / 12, amort_years * 12, loan, months_paid_before + 12)
            r.principal = bal_start - bal_end
            r.debt_service = monthly_pmt * 12
            r.interest = r.debt_service - r.principal
            r.debt_end = bal_end
        balance = r.debt_end

        r.cfads = r.cfbds - r.debt_service
        if r.debt_service > 0:
            r.dscr = r.noi / r.debt_service
        if loan > 0:
            r.debt_yield_orig = r.noi / loan
            if r.debt_begin > 0:
                r.debt_yield_current = r.noi / r.debt_begin
            r.ltv_current = r.debt_end / price if price else None

    # ---- Exit --------------------------------------------------------------
    exit_row = rows[hold - 1]
    forward = rows[hold]  # year N+1
    exit_cap = _get(a, "exit", "exit_cap_rate")
    disp_pct = _get(a, "exit", "disposition_cost_pct", default=0.0)

    gross_exit = forward.noi / exit_cap if exit_cap else 0.0
    disp_costs = gross_exit * disp_pct
    net_sale = gross_exit - disp_costs
    payoff = exit_row.debt_end
    net_equity_proceeds = net_sale - payoff

    # ---- Returns -----------------------------------------------------------
    acq_cost = price * _get(a, "acquisition", "acquisition_cost_pct", default=0.0)
    upfront = _get(a, "acquisition", "upfront_capex", default=0.0)
    total_basis = price + acq_cost + upfront
    equity = total_basis - loan

    op_rows = rows[:hold]
    unlev = [-total_basis] + [r.cfbds for r in op_rows]
    unlev[-1] += net_sale
    lev = [-equity] + [r.cfads for r in op_rows]
    lev[-1] += net_equity_proceeds

    disc = _get(a, "returns", "discount_rate", default=0.0)
    dcf_value = npv(disc, [r.cfbds for r in op_rows]) + net_sale / (1 + disc) ** hold

    sum_op_cfads = sum(r.cfads for r in op_rows)
    dscrs = [r.dscr for r in op_rows if r.dscr is not None]
    dys = [r.debt_yield_orig for r in op_rows if r.debt_yield_orig is not None]

    returns = {
        "purchase_price": price,
        "acquisition_costs": acq_cost,
        "upfront_capex": upfront,
        "total_basis": total_basis,
        "loan_amount": loan,
        "equity_required": equity,
        "going_in_cap_rate": rows[0].noi / price if price else 0.0,
        "unlevered_irr": irr(unlev),
        "levered_irr": irr(lev) if loan > 0 else irr(unlev),
        "equity_multiple": (sum_op_cfads + net_equity_proceeds) / equity if equity else None,
        "year1_cash_on_cash": (op_rows[0].cfads / equity) if equity else None,
        "avg_cash_on_cash": (sum_op_cfads / hold / equity) if equity else None,
        "dcf_indicated_value": dcf_value,
        "npv_vs_basis": dcf_value - total_basis,
        "min_dscr": min(dscrs) if dscrs else None,
        "min_debt_yield_orig": min(dys) if dys else None,
        "first_amortizing_year_dscr": next(
            (r.dscr for r in op_rows if r.year == io_years + 1 and r.dscr is not None), None
        ),
        "unlevered_cashflows": unlev,
        "levered_cashflows": lev,
    }

    return {
        "rows": [vars(r) for r in rows],
        "exit": {
            "forward_noi": forward.noi,
            "exit_cap_rate": exit_cap,
            "gross_exit_value": gross_exit,
            "disposition_costs": disp_costs,
            "net_sale_proceeds": net_sale,
            "loan_payoff": payoff,
            "net_equity_proceeds": net_equity_proceeds,
        },
        "debt": {
            "loan_amount": loan,
            "monthly_payment": monthly_pmt,
            "annual_debt_service_amortizing": monthly_pmt * 12,
            "io_years": io_years,
            "amort_years": amort_years,
            "rate": rate,
        },
        "returns": returns,
        "hold_years": hold,
    }


def load(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


if __name__ == "__main__":
    import sys

    assumptions = load(sys.argv[1])
    warns = validate(assumptions)
    result = compute(assumptions)
    for w in warns:
        print(f"WARNING: {w}")
    print(json.dumps(result["returns"], indent=2, default=str))
