# CRE Excel Formula Templates

All formulas use standard Excel/Google Sheets syntax. Named ranges shown in `UPPER_SNAKE` are defined in the Assumptions sheet.

## Table of Contents
1. [Assumptions Cross-References](#assumptions-cross-references)
2. [Revenue Formulas](#revenue-formulas)
3. [Operating Expense Formulas](#operating-expense-formulas)
4. [NOI & Cash Flow Waterfall](#noi--cash-flow-waterfall)
5. [Debt Schedule Formulas](#debt-schedule-formulas)
6. [Exit / Reversion Formulas](#exit--reversion-formulas)
7. [Return Metric Formulas](#return-metric-formulas)
8. [Sensitivity Table Setup](#sensitivity-table-setup)
9. [Validation Checks](#validation-checks)
10. [Conditional Formatting Rules](#conditional-formatting-rules)

---

## Assumptions Cross-References

Define named ranges on the Assumptions sheet for all inputs. Then reference them from projection sheets using the named range instead of cell addresses — this survives row/column insertions.

| Named Range | Description | Example Value |
|-------------|-------------|--------------|
| `PURCHASE_PRICE` | Acquisition purchase price | $15,000,000 |
| `ACQ_COST_PCT` | Acquisition closing cost % | 1.5% |
| `LTV` | Loan-to-value ratio | 70% |
| `INTEREST_RATE` | Annual interest rate | 5.50% |
| `IO_YEARS` | Interest-only period (years) | 2 |
| `AMORT_YEARS` | Amortization period (years) | 30 |
| `HOLD_YEARS` | Hold period (years) | 5 |
| `RENT_GROWTH` | Annual rent growth rate | 3.0% |
| `VACANCY_PCT` | Vacancy & credit loss % | 6.0% |
| `MGMT_FEE_PCT` | Management fee % of EGI | 4.0% |
| `CAPEX_PSF` | CapEx reserve per SF per year | $0.35 |
| `EXIT_CAP` | Exit cap rate | 5.75% |
| `SELL_COST_PCT` | Selling costs % of gross exit | 1.25% |
| `DSCR_MIN` | Minimum DSCR covenant | 1.25 |
| `GLA_SF` | Gross Leasable Area (SF) | 100,000 |
| `MARKET_RENT_PSF` | Market rent per SF per year | $18.00 |

---

## Revenue Formulas

### Gross Potential Rent (multi-tenant, with rent roll)
```excel
Year 1 In-place GPR:
  =SUMPRODUCT(RentRoll[Leased_SF], RentRoll[Rent_PSF_Yr])

Year 1 Vacant at market:
  =(GLA_SF - SUMPRODUCT(RentRoll[Leased_SF])) * MARKET_RENT_PSF

Year 1 Total GPR:
  =InPlaceGPR + VacantAtMarket
```

### GPR Growth (years 2–n)
```excel
Year N GPR from prior year (aggregate growth approach):
  =GPR_PriorYear * (1 + RENT_GROWTH)

Or apply per-tenant with lease steps:
  Contracted bump years: =Rent_PSF_CurrentYear * (1 + LeaseEscalation_Pct)
  Market renewal: =MARKET_RENT_PSF * (1 + RENT_GROWTH)^(Year - BaseYear)
```

### Vacancy & Credit Loss
```excel
  =PGI * VACANCY_PCT
```

### Effective Gross Income (EGI)
```excel
  =PGI - Vacancy_Loss
```

### Expense Recoveries (NNN leases)
```excel
  =SUMPRODUCT(NNNTenants[Leased_SF] / GLA_SF, TotalRecoverableOpEx)
```
Where `TotalRecoverableOpEx` = RE Taxes + Insurance + CAM (utilities, maintenance, admin).

---

## Operating Expense Formulas

### Fixed expenses grown by expense inflation rate (default 2.5%)

```excel
RE Taxes Year 1:      =RE_TAXES_BASE               (from Assumptions)
RE Taxes Year N:      =RE_Taxes_PriorYear * (1 + EXPENSE_GROWTH)

Insurance Year N:     =Insurance_PriorYear * (1 + EXPENSE_GROWTH)
Utilities Year N:     =Utilities_PriorYear * (1 + EXPENSE_GROWTH)
Repairs Year N:       =Repairs_PriorYear * (1 + EXPENSE_GROWTH)
Admin Year N:         =Admin_PriorYear * (1 + EXPENSE_GROWTH)
```

### Management Fee (variable — % of EGI)
```excel
  =EGI_Year * MGMT_FEE_PCT
```

### Total Operating Expenses
```excel
  =SUM(RETaxes, Insurance, Utilities, Repairs, MgmtFee, Admin)
```

### Net Operating Income (NOI)
```excel
  =EGI - TotalOpEx
```

### CapEx Reserve
```excel
  =GLA_SF * CAPEX_PSF
  [Or for MF: =UNIT_COUNT * CAPEX_PER_UNIT]
```

### Tenant Improvements (at rollover year)
```excel
  =Expiring_SF * TI_PSF_New       (new/vacant space)
  =Renewing_SF * TI_PSF_Renewal   (renewal)
  =IF(IsRolloverYear, Expiring_SF*TI_PSF, 0)
```

### Leasing Commissions (at rollover year)
```excel
  =Expiring_SF * New_Rent_PSF * New_Lease_Term_Yrs * LC_RATE_NEW
  Or:
  =IF(IsRolloverYear, TotalNewLeaseValue * LC_RATE, 0)
```

### Cash Flow Before Debt Service (CFBDS)
```excel
  =NOI - CapEx_Reserve - TI_This_Year - LC_This_Year
```

---

## Debt Schedule Formulas

### Loan Amount
```excel
  =PURCHASE_PRICE * LTV
```

### Loan Sizing — Dual Constraint (LTV + Debt Yield)
In practice, lenders size loans to the MORE RESTRICTIVE of LTV and Debt Yield:
```excel
  LTV_Constrained_Loan = PURCHASE_PRICE * LTV
  DY_Constrained_Loan  = NOI_Y1 / DY_MIN         [e.g., NOI / 8.0%]
  Actual_Loan_Amount   = MIN(LTV_Constrained_Loan, DY_Constrained_Loan)
  Equity               = Total_Cost - Actual_Loan_Amount
```
If `DY_Constrained_Loan < LTV_Constrained_Loan`, the lender will cut proceeds even though LTV looks acceptable. Flag this gap prominently so equity requirements are understood upfront.

### Monthly Payment (amortizing years)
```excel
  =PMT(INTEREST_RATE/12, AMORT_YEARS*12, -Loan_Amount)
  [Note: PMT returns negative; use -PMT() or ABS(PMT()) for positive DS display]
```

### Annual Debt Service
```excel
IO year:
  =Loan_Amount * INTEREST_RATE

Amortizing year:
  =ABS(PMT(INTEREST_RATE/12, AMORT_YEARS*12, -Loan_Amount)) * 12
  [Shortcut: =-PMT(INTEREST_RATE/12, AMORT_YEARS*12, Loan_Amount)*12]
```

**Zero-rate guard**:
```excel
  =IF(INTEREST_RATE=0, Loan_Amount/AMORT_YEARS, -PMT(INTEREST_RATE/12, AMORT_YEARS*12, Loan_Amount)*12)
```

### Loan Balance (track year-by-year)

Year 0: `=Loan_Amount`

IO year (balance unchanged):
```excel
  =Beginning_Balance
```

Amortizing year — Ending Balance (canonical form):
```excel
  =FV(INTEREST_RATE/12, AmortizingMonths, MonthlyPI, -Loan_Amount)
```
Where:
- `MonthlyPI` = `ABS(PMT(INTEREST_RATE/12, AMORT_YEARS*12, Loan_Amount))` — POSITIVE monthly payment
- `AmortizingMonths` = months elapsed SINCE THE FIRST AMORTIZING MONTH (i.e., subtract IO months, start counting at 1)
- `-Loan_Amount` = negative present value (the loan as a liability)
- Result is **POSITIVE** (remaining balance owed) — **NO outer minus sign**

Sign memo: `FV(r, n, +pmt, -loanAmt) = loanAmt*(1+r)^n - pmt*((1+r)^n-1)/r` → POSITIVE. An outer `-` would flip the sign and give a wrong NEGATIVE balance.

Alternative (cumulative principal paid):
```excel
  Ending_Balance = Beginning_Balance + CUMPRINC(rate/12, totalAmortPeriods, loanAmt, startPeriod, endPeriod, 0)
```
**CRITICAL**: `CUMPRINC` returns NEGATIVE values (principal paid = cash outflow). Use `+` (not `-`) to subtract it from balance; using `-` reverses the sign and INCREASES the balance instead of decreasing it.

Concrete example (Year 3 of a 30-year, 5% loan, 2-yr IO):
```excel
  Ending_Balance_Y3 = Beginning_Balance_Y3 + CUMPRINC(5%/12, 30*12, LoanAmount, 1, 12, 0)
  [startPeriod=1, endPeriod=12 = months 1–12 of the amortizing schedule]
```

### Interest Paid (for each year, informational)
```excel
IO year:    =Loan_Amount * INTEREST_RATE
Amort year (exact, preferred):
            =-CUMIPMT(INTEREST_RATE/12, AMORT_YEARS*12, Loan_Amount, startPeriod, endPeriod, 0)
            [CUMIPMT returns negative; negate it for a positive display]
Amort year (rough annual approximation — avoid for precision work):
            =Beginning_Balance * INTEREST_RATE
            [CAUTION: overstates interest — uses simple annual rate on beginning balance
             instead of the monthly compounding schedule; acceptable for ballpark only]
```

### Principal Paid (amortizing years only)
```excel
  =Annual_Debt_Service - Interest_Paid
  Or: =-CUMPRINC(INTEREST_RATE/12, AMORT_YEARS*12, Loan_Amount, startPeriod, endPeriod, 0)
```

### DSCR
```excel
  =IF(Annual_Debt_Service=0, "N/A", NOI/Annual_Debt_Service)
```

### Debt Yield
```excel
  =IF(Loan_Amount=0, "N/A", NOI/Loan_Amount)
```
**CRITICAL**: Always divide by the **original loan amount at origination** (`Loan_Amount = PURCHASE_PRICE * LTV`), NOT the current outstanding balance. Lenders set this covenant at origination; using the declining balance makes DY look progressively better as the loan amortizes — which is precisely the gaming vector the metric was designed to prevent.

---

## Exit / Reversion Formulas

### Exit NOI (Forward NOI — Year n+1)
```excel
  =NOI_LastYear * (1 + RENT_GROWTH)
```

### Gross Exit Value
```excel
  =ExitNOI / EXIT_CAP
```

### Net Exit Value
```excel
  =GrossExitValue * (1 - SELL_COST_PCT)
```

### Remaining Loan Balance at Exit
```excel
For loan with IO_YEARS interest-only then amortizing:
  =IF(HOLD_YEARS <= IO_YEARS,
      Loan_Amount,                                                    [still IO at exit]
      FV(INTEREST_RATE/12, (HOLD_YEARS-IO_YEARS)*12,
         ABS(PMT(INTEREST_RATE/12, AMORT_YEARS*12, Loan_Amount)),
         -Loan_Amount))
```
Result is **POSITIVE** (remaining balance owed) — no outer minus sign.

**Simpler with named ranges**:
```excel
  =FV(INTEREST_RATE/12, AmortizingMonths, MonthlyPI, -Loan_Amount)
  where AmortizingMonths = MAX(0, HOLD_YEARS - IO_YEARS) * 12
  and MonthlyPI = ABS(PMT(INTEREST_RATE/12, AMORT_YEARS*12, Loan_Amount))  [positive]
```
**No outer minus sign needed.** `FV(rate, n, +pmt, -loanAmt)` already returns a POSITIVE remaining balance. Adding `-` would incorrectly negate it.

### Net Equity Proceeds
```excel
  =NetExitValue - RemainingLoanBalance
```

---

## Return Metric Formulas

### Equity Invested (Year 0 outflow)
```excel
  Total_Cost = PURCHASE_PRICE + (PURCHASE_PRICE * ACQ_COST_PCT) + Upfront_Reserves
  Loan_Amount = PURCHASE_PRICE * LTV
  Equity = Total_Cost - Loan_Amount
```

### Sources = Uses Validation
```excel
  =IF(ABS((Loan_Amount + Equity) - Total_Cost) < 1, "OK", "CHECK SOURCES/USES")
```

### Levered IRR (array of cash flows in one row or column)
```excel
  =IRR(Levered_CF_Array, 0.12)
  where Levered_CF_Array = {-Equity, CFADS_Y1, CFADS_Y2, ..., CFADS_Yn + NetEquityProceeds}
```

### Unlevered IRR
```excel
  =IRR(Unlevered_CF_Array, 0.10)
  where Unlevered_CF_Array = {-TotalCost, CFBDS_Y1, ..., CFBDS_Yn + NetExitValue}
```

### Equity Multiple (EM)
```excel
  Option A — if CFADS_Range contains OPERATING years only (Y1–Yn, no exit embedded):
    =(SUM(CFADS_Range) + NetEquityProceeds) / Equity

  Option B — if Year n CFADS already includes NetEquityProceeds (embedded exit):
    =SUM(CFADS_Range) / Equity   ← do NOT add NetEquityProceeds again
```
**Double-count trap**: The IRR array formula `{-Equity, CFADS_Y1, ..., CFADS_Yn + NetEquityProceeds}` embeds exit in the last year. If `CFADS_Range` points to that same array, use Option B. If `CFADS_Range` is a separate operating-only range (Y1–Yn without exit), use Option A. Mixing them produces EM ~1.5× too high.

### Year 1 Cash-on-Cash
```excel
  =CFADS_Y1 / Equity
```

### Average Cash-on-Cash
```excel
  =(SUM(CFADS_Y1_to_Yn_operating) / HOLD_YEARS) / Equity
```
Where `CFADS_Y1_to_Yn_operating` = annual CFADS for Y1–Yn with **no exit proceeds** in Year n. Average CoC measures the annual income return only; exit reversion is a capital return captured by IRR and EM, not CoC.

### Going-in Cap Rate
```excel
  =NOI_Y1 / PURCHASE_PRICE
```

---

## Sensitivity Table Setup

### 2-Variable Data Table in Excel

**Table 1: Levered IRR by Exit Cap Rate × Rent Growth**

Step 1: Create the table grid
```
         | 0%Growth | 1%Growth | 2%Growth | 3%Growth | 4%Growth | 5%Growth
4.50%Cap |          |          |          |          |          |
4.75%Cap |          |          |          |          |          |
5.00%Cap |          |          |          |          |          |  [base]
5.25%Cap |          |          |          |          |          |
5.50%Cap |          |          |          |          |          |
```

Step 2: Top-left "corner" cell = reference to Levered IRR output:
```excel
  =Returns!LeveredIRR     [or wherever IRR is calculated]
```

Step 3: Left column = exit cap rate values (linked to EXIT_CAP cell)
Step 4: Top row = rent growth values (linked to RENT_GROWTH cell)

Step 5: Select entire table including corner cell → Data → What-If Analysis → Data Table
- Row input cell: `RENT_GROWTH` (the assumption cell)
- Column input cell: `EXIT_CAP` (the assumption cell)

**Critical**: The table temporarily substitutes each row/column value into the input cell and recalculates. Both input cells must be the actual Assumptions cells (not named ranges directly — point to the cell containing the named range value).

### Sensitivity in Google Sheets / ExcelJS
When native DATA TABLE is not available (e.g., ExcelJS), calculate sensitivity programmatically:

```javascript
// ExcelJS: calculate each IRR manually by iterating assumptions
for (const exitCap of exitCapRange) {
  for (const rentGrowth of rentGrowthRange) {
    const irr = calculateLeveredIRR({ ...assumptions, exitCap, rentGrowth })
    matrix[exitCapIdx][rentGrowthIdx] = irr
  }
}
```

---

## Validation Checks

Add a hidden `_Checks` sheet (or visible `Validation` section) with these formulas:

```excel
Sources = Uses:
  =IF(ABS(Loan_Amount + Equity - Total_Cost) < 1, "PASS", "FAIL: " & TEXT(ABS(Loan_Amount + Equity - Total_Cost), "$#,##0"))

Going-in cap matches stated:
  =IF(ABS(NOI_Y1/PURCHASE_PRICE - Stated_Going_In_Cap) < 0.0001, "PASS", "WARN: cap rate mismatch")

Exit cap >= going-in cap:
  =IF(EXIT_CAP >= (NOI_Y1/PURCHASE_PRICE), "PASS", "WARN: exit cap compresses vs going-in")

DSCR min:
  =IF(MIN(DSCR_Range) >= DSCR_MIN, "PASS", "FAIL: DSCR breach " & TEXT(MIN(DSCR_Range), "0.00x"))

Debt yield at origination:
  =IF(NOI_Y1/Loan_Amount >= 0.08, "PASS", "WARN: DY=" & TEXT(NOI_Y1/Loan_Amount, "0.0%"))

Positive equity:
  =IF(Equity > 0, "PASS", "FAIL: negative equity")

Positive EM:
  =IF(Equity_Multiple >= 1.0, "PASS", "WARN: EM < 1.0x — losing money")
```

---

## Conditional Formatting Rules

### IRR Sensitivity Table
- ≥ Target IRR: green fill (#C6EFCE), dark green text (#375623)
- Target IRR − 2% to Target IRR: yellow fill (#FFEB9C), dark yellow text (#9C6500)
- < Target IRR − 2%: red fill (#FFC7CE), dark red text (#9C0006)
- Highlight base case cell: bold border

### DSCR Column
- ≥ 1.25x: green text
- 1.10x – 1.24x: orange text
- < 1.10x: red fill + bold

### Debt Yield Column
- ≥ 8%: green text
- 6% – 7.9%: orange text
- < 6%: red fill

### Cash Flow Column
- Positive CFADS: black
- Negative CFADS: red (parentheses format: `($1,234)`)
