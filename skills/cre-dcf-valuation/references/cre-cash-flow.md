# CRE Cash Flow Model — Reference

## Table of Contents
1. [Cash Flow Waterfall](#cash-flow-waterfall)
2. [Revenue Components](#revenue-components)
3. [Operating Expense Components](#operating-expense-components)
4. [Debt Service & Amortization](#debt-service--amortization)
5. [Exit / Reversion Math](#exit--reversion-math)
6. [Return Metric Formulas](#return-metric-formulas)
7. [IRR Calculation](#irr-calculation)
8. [Lease-Level Projection](#lease-level-projection)
9. [Common Pitfalls](#common-pitfalls)

---

## Cash Flow Waterfall

```
Gross Potential Rent (GPR)
  = Σ (leased SF × contracted rent/SF/yr)
  + (vacant SF × market rent/SF/yr)           ← market rent for vacancy
+ Expense Recoveries (NNN / partial NNN)       ← reimbursed OpEx from tenants
+ Other Income                                 ← parking, signage, laundry, antenna, etc.
──────────────────────────────────────────────
= Potential Gross Income (PGI)
− Vacancy & Credit Loss                        ← market vacancy % × PGI
──────────────────────────────────────────────
= Effective Gross Income (EGI)
− Operating Expenses                           ← see detail below
──────────────────────────────────────────────
= Net Operating Income (NOI)
  [NOI is the standard CRE income metric — before debt, depreciation, income tax, CapEx]
− Capital Expenditure / Replacement Reserve    ← $/SF/yr or % of EGI
− Tenant Improvements (TI)                     ← $/SF × rolling/expiring SF at year of rollover
− Leasing Commissions (LC)                     ← % of total new lease value at rollover
──────────────────────────────────────────────
= Cash Flow Before Debt Service (CFBDS)        ← Unlevered free cash flow
− Annual Debt Service                          ← Principal + Interest
──────────────────────────────────────────────
= Cash Flow After Debt Service (CFADS)         ← Levered free cash flow / distributable cash
```

**Note**: Some models present NOI excluding CapEx/TI/LC (the pure income approach used for cap rate valuation), then deduct these costs separately for the levered cash flow waterfall. Both conventions are valid; be consistent within a model.

---

## Revenue Components

### Gross Potential Rent (GPR)
- **In-place tenants**: Use contracted rent per lease (including fixed bumps)
- **Rolling / expiring tenants**: Apply market rent at renewal (typically current market rent grown at rent growth rate to year of expiry)
- **Vacant units/space**: Apply market rent × (1 − vacancy loss) OR show GPR at 100% market rent and deduct vacancy separately

### Expense Recoveries
- **Gross lease**: Tenant pays rent only; landlord absorbs all OpEx → Recoveries = $0
- **Modified Gross**: Tenant pays base + some expenses → Recover specific items
- **NNN (Triple Net)**: Tenant reimburses RE taxes + insurance + CAM → Recoveries ≈ OpEx (landlord nets full NOI)
- **Double Net (NN)**: Tenant pays taxes + insurance; landlord pays maintenance
- Recovery rate convention: `Recoveries = (tenant_SF / total_SF) × recoverable_OpEx × recovery_ratio`

### Vacancy & Credit Loss
- **Structural vacancy**: Reflects expected stabilized vacancy in the market
- **Credit loss**: Additional haircut for tenant default/slow payment (typically 1–2%)
- **Combined**: Apply as % of PGI (e.g., 7% = 5% vacancy + 2% credit loss)
- **Lease-level model**: Only apply to vacant/expiring space; in-place leases are 100% collected until expiry

### Other Income
- Parking: $/space/month × spaces
- Signage/rooftop antenna: contractual
- Laundry, vending (MF): $/unit/month
- Late fees, pet fees (MF): $/unit/month

---

## Operating Expense Components

### Standard Line Items

| Expense | Typical Range | Notes |
|---------|--------------|-------|
| Real Estate Taxes | Varies widely | Reassess at acquisition cost in some jurisdictions |
| Insurance | $0.20–$0.60/SF/yr | Higher for older/coastal properties |
| Utilities (CAM) | $0.50–$2.00/SF/yr | Common area only; tenant pays own in NNN |
| Repairs & Maintenance | $0.50–$1.50/SF/yr | Higher for older buildings |
| Property Management Fee | 3–5% of EGI | 4–6% for MF; 3–4% for industrial |
| Administrative | $0.20–$0.50/SF/yr | Accounting, legal, admin |
| Landscaping / Snow | $0.10–$0.40/SF/yr | Climate-dependent |
| Security | $0.30–$1.00/SF/yr | If applicable |
| **Total OpEx** | **25–50% of EGI** | Varies by property type and lease structure |

### OpEx Ratio Shortcuts (when detail unavailable)

| Property Type | OpEx as % of EGI |
|--------------|-----------------|
| Multifamily | 35–45% |
| Office (gross leases) | 35–50% |
| Retail (gross) | 25–40% |
| Industrial (NNN) | 5–15% (landlord net; tenant pays most) |
| Hotel | 60–70% (EBITDA approach) |

### Capital Expenditure Reserve
- Replacement reserve: covers roof, HVAC, parking lot, elevator, etc.
- **MF**: $150–$400/unit/yr (older buildings = higher)
- **Office/Retail**: $0.25–$0.75/SF/yr
- **Industrial**: $0.10–$0.30/SF/yr
- Distinguish from TI/LC which are rollover-driven, not recurring

### Tenant Improvements (TI) — at Rollover Only
- New leases (vacant space): $20–$80/SF (office); $10–$40/SF (retail); $5–$20/SF (industrial)
- Renewal leases: $5–$30/SF (lower, existing buildout reused)
- MF: Typically unit-turn costs ($1,500–$5,000/unit)

### Leasing Commissions (LC) — at Rollover Only
- Typically 4–6% of total lease value for new leases
- 2–4% for renewals
- `LC = LC_rate × (new_rent × new_term_years × leased_SF)`
- Paid in year of lease commencement

---

## Debt Service & Amortization

### Loan Amount
```
Loan Amount = LTV × Purchase Price
```

### Interest-Only Period
```
Annual Debt Service (IO years) = Loan Amount × Interest Rate
```

### Amortizing Period
```
Monthly Payment = ABS(PMT(rate/12, amortYrs×12, loanAmt))    ← positive dollar amount
  [Excel: =-PMT(rate/12, amortYrs*12, loanAmt)
       or  =PMT(rate/12, amortYrs*12, -loanAmt)   (negative pv → positive payment)]
  Note: PMT(rate, nper, +pv) returns negative; always negate to get a positive payment figure.

Annual Debt Service = Monthly Payment × 12
```

**Zero-rate guard**: If interest rate = 0%, use straight-line amortization:
`Annual Principal = Loan Amount / Amort Years`

### Loan Balance Tracking (amortization schedule)
```
Year 0 balance   = Loan Amount
Year n balance   = FV(rate/12, amortizingMonths, monthlyPayment, -loanAmount)
  where:
    monthlyPayment    = positive dollar amount (ABS of PMT result)
    amortizingMonths  = count of months elapsed SINCE FIRST AMORTIZING MONTH
                        (i.e., subtract the IO period months, start at 1)
  [Excel: =FV(rate/12, MAX(0,holdYr-IO_Years)*12, MonthlyPayment, -LoanAmount)]
  [Result is POSITIVE — no outer minus sign needed]
  [Or track: Balance(n) = Balance(n-1) - Principal_Paid(n)]
```
**IO-period balance**: Stays flat — no principal is paid during interest-only years.
**IO-only hold** (hold period ≤ IO years): Remaining Balance = Original Loan Amount.

### DSCR (Debt Service Coverage Ratio)
```
DSCR = NOI / Annual Debt Service
Minimum acceptable: 1.20x (agency/life co); 1.25x (CMBS); 1.10x (bridge)
```
**Post-IO stress test**: Always check DSCR in the first amortizing year (Year IO_Years + 1), not just the IO period. IO-period debt service is interest-only (lower payment = artificially high DSCR). After IO expires, amortizing payments are materially higher. Lenders require DSCR ≥ 1.25x on the amortizing schedule. Report both: DSCR_IO (favorable) and DSCR_Amortizing (binding constraint).

### Debt Yield
```
Debt Yield (origination) = Year 1 NOI / Original Loan Amount
```
**Critical convention**: Always use the **original loan amount** at underwriting — NOT the outstanding balance. Outstanding balance falls as the loan amortizes, which makes DY look progressively better even if NOI hasn't improved. Lenders explicitly use original loan to eliminate this gaming vector. DY is an origination covenant; post-close lenders may track current-balance DY for surveillance only.

Lender minimums: 7.5–9% (CMBS / bridge); 9–10%+ (life company / agency in tighter markets)

---

## Exit / Reversion Math

### Exit NOI (Forward NOI)
```
Exit NOI = Year n NOI × (1 + Rent Growth Rate)
```
Use the NEXT year's NOI as the cap rate divisor — this is the institutional convention (buyer is buying forward income).

### Exit Cap Rate Convention
- Exit cap rate typically equals going-in cap rate PLUS 25–50 bps expansion
- Rationale: property is older at exit; buyer demands higher return for age/obsolescence
- Do NOT use going-in cap = exit cap unless explicitly justified (e.g., significant renovation)

### Gross Exit Value
```
Gross Exit Value = Exit NOI / Exit Cap Rate
```

### Net Exit Value (after selling costs)
```
Net Exit Value = Gross Exit Value × (1 − Selling Costs %)
Selling Costs: 1.0–1.5% for large deals (>$20M); up to 2.0% for smaller deals
Includes: brokerage, title, transfer taxes, legal, closing costs
```

### Remaining Loan Balance at Exit
```
Remaining Balance = FV(rate/12, amortizingMonths, monthlyPayment, −loanAmount)
  where amortizingMonths = MAX(0, holdYears − IO_Years) × 12
  and monthlyPayment = positive monthly payment (ABS of PMT result)
  [Excel: =FV(INTEREST_RATE/12, MAX(0,HOLD_YEARS-IO_YEARS)*12, MonthlyPayment, -LoanAmount)]
  [Result is POSITIVE — no outer minus sign needed]
  [For IO-only holds: amortizingMonths = 0, so FV returns original loan — correct]
```

### Net Equity Proceeds
```
Net Equity Proceeds = Net Exit Value − Remaining Loan Balance
```

---

## Return Metric Formulas

### Unlevered IRR
```
Cash Flows:
  Year 0: −(Purchase Price + Closing Costs + upfront CapEx/TI)
  Years 1–n: CFBDS each year
  Year n: add Net Exit Value to Year n CFBDS

IRR: solve for r in  Σ[ CF_t / (1+r)^t ] = 0
```

### Levered IRR
```
Cash Flows:
  Year 0: −Equity Invested
           = −(Total Cost − Loan Amount)
           = −(Purchase Price + Closing Costs + Reserves − Loan Proceeds)
  Years 1–n: CFADS each year
  Year n: add Net Equity Proceeds to Year n CFADS

IRR: solve for r in  Σ[ CF_t / (1+r)^t ] = 0
```

### Equity Multiple (EM)
```
EM = (Σ Operating CFADS Y1–Yn  +  Net Equity Proceeds) / Equity Invested
```
- **Operating CFADS**: annual CFADS for Years 1–n, EXCLUDING exit proceeds (operating income only)
- **Net Equity Proceeds**: the single reversion check at end of hold (from exit section)
- **Do NOT double-count**: if your IRR cash flow array already embeds exit proceeds in Year n CFADS, then `EM = SUM(full CFADS array) / Equity` — adding Net Equity Proceeds again double-counts the exit.

Convention: total cash in / total cash out. 2.0x EM = doubled invested capital.

### Cash-on-Cash Return
```
Year 1 CoC = CFADS_Y1 / Equity Invested
Avg CoC    = (Σ CFADS / Hold Period) / Equity Invested
```
Note: CoC ignores terminal value; EM and IRR capture both income and appreciation.

### Going-in Cap Rate
```
Going-in Cap Rate = Year 1 NOI / Purchase Price
```
This is the headline yield at acquisition. Always verify it matches the seller's pro forma.

---

## IRR Calculation

Use Newton-Raphson iteration (same as Excel's `=IRR()` function):

```
Initial guess: r₀ = 0.12 (12%)

NPV(r) = Σ[ CF_t / (1+r)^t ]

Iterate: r_{n+1} = r_n − NPV(r_n) / NPV'(r_n)

NPV'(r) = Σ[ −t × CF_t / (1+r)^(t+1) ]   (first derivative)

Converge when |NPV(r)| < 1e-7
```

**Edge cases**:
- All negative CFs → IRR undefined (return NaN)
- IRR > 500% or < −99.99% → unreliable, return NaN
- No sign change in CFs → IRR undefined

---

## Lease-Level Projection

When a full rent roll is available:

1. **In-place leases**: Project rent at contracted escalation (e.g., 3%/yr fixed bump)
   - At lease expiry: reset to market rent (market rent grown to that year)
   - Apply rollover vacancy: assume X months of vacancy at lease expiry (typically 3–12 months)
   - Deduct TI and LC in the year of new lease commencement

2. **Market rent growth**: Apply rent growth rate to market rent each year
   - In-place rents with fixed bumps may diverge from market — model both

3. **WALT (Weighted Average Lease Term)**
   - `WALT = Σ(tenant_SF × remaining_term) / total_leased_SF`
   - Higher WALT = lower rollover risk

4. **Rollover exposure**: % of GLA expiring each year
   - >30% expiring in a single year is high rollover risk
   - Model each year's expirations explicitly for TI/LC sizing

---

## Common Pitfalls

| Pitfall | Correct Approach |
|---------|-----------------|
| Using going-in cap = exit cap | Add 25–50 bps to exit cap; older property, less favorable |
| Forgetting closing costs in equity calculation | Total Cost = Purchase Price + Closing Costs + Reserves; Equity = Total Cost − Loan |
| Applying vacancy to NNN rent | In NNN deals, tenants are contractually obligated; vacancy applies to vacant/expiring space |
| Terminal growth rate ≥ discount rate | Model breaks; always ensure discount rate > terminal growth |
| Applying DSCR check to unlevered model | DSCR only applies where there is debt; unlevered model has no debt service |
| IO period debt service = amortizing payment | IO period: Debt Service = Loan × Rate only (no principal) |
| Exit value on in-place NOI (not forward) | Exit cap divides into FORWARD (Year n+1) NOI, not Year n |
| Forgetting selling costs at exit | Net exit value must deduct transaction/brokerage costs of 1–2% |
| Hardcoding values instead of linking to assumptions | Link all cells to assumption inputs for scenario/sensitivity flexibility |
| Double-counting NNN expense recoveries | NNN tenants reimburse OpEx — do NOT also subtract that OpEx from NOI as a landlord cost. Either net NOI already excludes those OpEx items, or show recoveries as income that exactly offsets them |
| Double-applying rent growth to in-place fixed-bump leases | In-place leases with contractual annual bumps (e.g., 3%/yr fixed) already have their own escalation — do NOT also compound them at the market rent growth rate. Market growth rate applies only to vacant space and at lease renewal |
