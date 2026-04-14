---
name: cre-dcf-valuation
description: "Build Discounted Cash Flow (DCF) valuation models for commercial real estate (CRE). Calculate NOI-based cash flows, levered and unlevered IRR, equity multiple, DSCR, debt yield, exit cap rate reversion, and sensitivity analysis. Use for office, retail, industrial, multifamily, mixed-use, and hotel properties. Trigger on: CRE valuation, property DCF, NOI projection, cap rate analysis, IRR analysis, real estate investment return, acquisition underwriting, hold-period analysis, CRE sensitivity table."
---

# CRE DCF Valuation Skill

Build institutional-grade Discounted Cash Flow models for commercial real estate acquisitions. CRE DCF differs fundamentally from corporate DCF: it is NOI-based (not EBIT/FCF), uses cap rate exit (not Gordon Growth), measures IRR and equity multiple (not EV/share), and debt is modeled explicitly via loan amortization.

## Inputs Required

**Property**
- Property type (Office / Retail / Industrial / Multifamily / Mixed-Use / Hotel)
- Gross Leasable Area (GLA) in SF, or unit count for multifamily
- Purchase price
- Closing costs (default: 1.5–2.0% of purchase price for buyer)

**Revenue**
- Rent roll: tenant, SF, rent/SF (or $/unit/month for MF), lease start/end, escalations
- Market vacancy rate and credit loss assumption
- Other income (parking, signage, laundry, etc.)
- For NNN leases: expense reimbursements

**Expenses**
- Operating expense line items (taxes, insurance, utilities, maintenance, management fee)
- OR total OpEx ratio (% of EGI) if line items unavailable
- Capital expenditure reserve ($/SF/yr or % of EGI)
- Tenant improvement costs ($/SF) at rollover
- Leasing commissions (% of total lease value at rollover)

**Financing**
- Loan-to-Value (LTV) percentage
- Interest rate (fixed or floating)
- Interest-only period (years)
- Amortization period (years, typically 25–30)
- DSCR covenant minimum (default: 1.25x)
- Debt yield minimum (default: 8%)

**Hold Period & Exit**
- Hold period (years; typically 5–10)
- Annual rent growth rate (market NOI growth)
- Exit cap rate (going-in cap rate + 25–50 bps expansion is the convention)
- Selling costs (default: 1.0–1.5% of gross exit value)

## Workflow

### 1. Build Annual NOI

See `references/cre-cash-flow.md` for the exact waterfall. In brief:

```
Gross Potential Rent (GPR)
+ Expense Recoveries (NNN or partial NNN)
+ Other Income
= Potential Gross Income (PGI)
− Vacancy & Credit Loss  (market vacancy % × PGI)
= Effective Gross Income (EGI)
− Operating Expenses
= Net Operating Income (NOI)
```

Grow NOI each year by `rentGrowthRate`. Apply lease-specific escalations when rent roll is available.

### 2. Compute Leasing Costs (deducted from NOI for cash flow)

At each lease expiration: deduct TI ($/SF × rolling SF) and LC (% of total new lease value).

```
CFBDS (Cash Flow Before Debt Service) = NOI − CapEx − TI − LC
```

### 3. Model Debt

```
Loan Amount  = LTV × Purchase Price
IO Years     = interest-only period (Debt Service = Loan × Rate)
Amort Years  = amortizing period
Annual DS    = PMT(rate/12, amortYrs×12, loanAmt) × 12  (amortizing years)
Loan Balance = track via amortization schedule each year

CFADS (Cash Flow After Debt Service) = CFBDS − Annual Debt Service
DSCR = NOI / Annual Debt Service          (covenant: ≥ 1.25x)
Debt Yield = NOI / Original Loan Amount   (covenant: ≥ 8%; always use origination balance, not current)
```

### 4. Model Exit Reversion

```
Exit NOI (forward) = Year n NOI × (1 + rentGrowthRate)
Gross Exit Value   = Exit NOI / Exit Cap Rate
Net Exit Value     = Gross Exit Value × (1 − Selling Costs %)
Remaining Balance  = Loan balance at end of Year n (from amort schedule)
Net Equity Proceeds = Net Exit Value − Remaining Balance
```

### 5. Calculate Returns

```
Unlevered IRR: IRR([ −(Purchase Price + Closing Costs + upfront CapEx/TI Reserves),
                      CFBDS_Y1, …, CFBDS_Yn + Net Exit Value ])

Levered IRR:   IRR([ −Equity Invested,
                      CFADS_Y1, …, CFADS_Yn + Net Equity Proceeds ])

Equity Multiple (EM) = (Σ Operating CFADS Y1–Yn  +  Net Equity Proceeds) / Equity Invested
  [Σ Operating CFADS = years 1 through n, EXCLUDING exit; add Net Equity Proceeds once separately]
  [If your CFADS array already embeds exit in Year n, use SUM(full array)/Equity — do NOT add proceeds again]

Cash-on-Cash (Year 1) = CFADS_Y1 / Equity Invested
Avg Cash-on-Cash      = (Σ CFADS_Y1…Yn / Hold Period) / Equity Invested
  [CFADS Yn = operating only here — exclude exit reversion from annual average]

Going-in Cap Rate = Year 1 NOI / Purchase Price
```

### 6. Sensitivity Analysis

Run two standard tables:

**Table 1 — IRR by Exit Cap Rate × Rent Growth**
Rows: Exit Cap Rate (going-in ± 100 bps in 25 bps steps)
Cols: Annual Rent Growth (0% to 5% in 1% steps)

**Table 2 — DSCR by Interest Rate × LTV**
Rows: Interest Rate (base ± 150 bps in 50 bps steps)
Cols: LTV (55% to 75% in 5% steps)

## Output Format

```markdown
# CRE DCF Valuation: [Property Name]

**Valuation Date**: [Date]  **Property Type**: [Type]  **Hold Period**: [N] years

---

## Deal Summary
| Metric | Value |
|--------|-------|
| GLA / Units | X,XXX SF or XX units |
| Purchase Price | $X,XXX,XXX |
| Going-in Cap Rate | X.XX% |
| Year 1 NOI | $XXX,XXX |
| LTV | XX% |
| Loan Amount | $X,XXX,XXX |
| Equity Required | $X,XXX,XXX |

## Sources & Uses
| | Amount |
|--|--------|
| Loan Proceeds | $X,XXX,XXX |
| Equity | $X,XXX,XXX |
| **Total Sources** | **$X,XXX,XXX** |
| Purchase Price | $X,XXX,XXX |
| Closing Costs (X.X%) | $XX,XXX |
| CapEx / TI Reserve | $XX,XXX |
| **Total Uses** | **$X,XXX,XXX** |

## Annual Cash Flow Projection
| | Y1 | Y2 | Y3 | Y4 | Y5 |
|--|--|--|--|--|--|
| GPR | | | | | |
| Vacancy Loss | | | | | |
| EGI | | | | | |
| OpEx | | | | | |
| NOI | | | | | |
| TI / LC | | | | | |
| CFBDS | | | | | |
| Debt Service | | | | | |
| CFADS | | | | | |
| DSCR | | | | | |
| Debt Yield | | | | | |

## Exit & Returns
| Metric | Value |
|--------|-------|
| Exit NOI (forward) | $XXX,XXX |
| Exit Cap Rate | X.XX% |
| Gross Exit Value | $X,XXX,XXX |
| Net Exit Value (after costs) | $X,XXX,XXX |
| Remaining Loan Balance | $X,XXX,XXX |
| Net Equity Proceeds | $X,XXX,XXX |
| **Unlevered IRR** | **X.X%** |
| **Levered IRR** | **X.X%** |
| **Equity Multiple** | **X.Xx** |
| **Year 1 Cash-on-Cash** | **X.X%** |
| **Unlevered NPV (@ X% DR)** | **$X,XXX,XXX** |

## Sensitivity — Levered IRR (Exit Cap Rate × Rent Growth)
| Cap Rate ↓ / Growth → | 0% | 1% | 2% | 3% | 4% |
|-----------------------|----|----|----|----|-----|
| [going-in −1.0%] | | | | | |
| [going-in −0.5%] | | | | | |
| **[base]** | | | **X.X%** | | |
| [going-in +0.5%] | | | | | |
| [going-in +1.0%] | | | | | |
```

## Validation Checks (run before finalizing)

- [ ] Going-in cap rate = Year 1 NOI ÷ Purchase Price (cross-check)
- [ ] DSCR ≥ 1.25x every year (flag breaches)
- [ ] Debt Yield ≥ 8% at origination
- [ ] LTV ≤ 75% (80% absolute max for most lenders)
- [ ] Terminal growth < Discount rate (model break if violated)
- [ ] Exit cap ≥ going-in cap (**warning**, not a hard fail; value-add / renovation thesis can justify compression — document rationale)
- [ ] Sources = Uses (equity + debt = purchase price + all costs)
- [ ] Total Equity Proceeds > Equity Invested for positive EM (obvious but easy to miss)

## Property Type Defaults

See `references/cre-benchmarks.md` for full benchmark tables by property type (cap rates, vacancy, OpEx ratios, rent growth, WACC/discount rate targets, DSCR/LTV norms).

## What This Skill Cannot Do

- Guarantee accuracy of market assumptions (use actual comps)
- Replace licensed MAI appraisal or lender underwriting
- Model LP/GP waterfall distributions, preferred equity splits, or promoted interest
- Account for lease-specific rent steps automatically without a full rent roll
- Model income tax, depreciation, or after-tax IRR (pre-tax, pre-depreciation only)
- Provide investment recommendations
