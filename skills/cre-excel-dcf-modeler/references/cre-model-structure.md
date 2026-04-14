# CRE Excel Model — Detailed Sheet Structure

Cell-by-cell layout for each of the 7 tabs. Rows labeled by content; columns labeled by time period.

## Table of Contents
1. [Tab 1: Cover](#tab-1-cover)
2. [Tab 2: Assumptions](#tab-2-assumptions)
3. [Tab 3: Rent Roll / Unit Mix](#tab-3-rent-roll--unit-mix)
4. [Tab 4: Operating Statement](#tab-4-operating-statement)
5. [Tab 5: Debt Schedule](#tab-5-debt-schedule)
6. [Tab 6: Cash Flows & Returns](#tab-6-cash-flows--returns)
7. [Tab 7: Sensitivity](#tab-7-sensitivity)

---

## Tab 1: Cover

**Purpose**: Executive summary — key metrics dashboard for IC / LP presentation.

```
Row  | Column A             | Column B            | Column C
─────|──────────────────────|─────────────────────|────────────
1    | [Property Name]      | [merged title]      |
2    | [Address]            |                     |
3    | [Property Type]      |                     |
4    | Valuation Date       | [=TODAY()]          |
─────|──────────────────────|─────────────────────|────────────
     DEAL METRICS
─────|──────────────────────|─────────────────────|────────────
6    | Purchase Price       | $X,XXX,XXX          |
7    | GLA / Units          | X,XXX SF / XX units |
8    | Going-in Cap Rate    | X.XX%               | =NOI_Y1/PP
9    | Year 1 NOI           | $XXX,XXX            |
10   | Hold Period          | X years             |
─────|──────────────────────|─────────────────────|────────────
     FINANCING
─────|──────────────────────|─────────────────────|────────────
12   | Loan Amount          | $X,XXX,XXX          | =PP*LTV
13   | LTV                  | XX.X%               |
14   | Interest Rate        | X.XX%               |
15   | Equity Required      | $X,XXX,XXX          |
16   | Year 1 DSCR          | X.XXx               |
17   | Debt Yield           | X.X%                |
─────|──────────────────────|─────────────────────|────────────
     RETURNS
─────|──────────────────────|─────────────────────|────────────
19   | Levered IRR          | X.X%                | ← from Tab 6
20   | Unlevered IRR        | X.X%                | ← from Tab 6
21   | Equity Multiple      | X.Xx                | ← from Tab 6
22   | Year 1 Cash-on-Cash  | X.X%                | ← from Tab 6
23   | Exit Cap Rate        | X.XX%               |
24   | Gross Exit Value     | $X,XXX,XXX          |
─────|──────────────────────|─────────────────────|────────────
     SOURCES & USES
─────|──────────────────────|─────────────────────|────────────
26   | SOURCES              |                     |
27   | Loan Proceeds        | $X,XXX,XXX          |
28   | Equity               | $X,XXX,XXX          |
29   | Total Sources        | $X,XXX,XXX          | (bold)
30   | USES                 |                     |
31   | Purchase Price       | $X,XXX,XXX          |
32   | Closing Costs        | $XXX,XXX            |
33   | CapEx/TI Reserve     | $XXX,XXX            |
34   | Total Uses           | $X,XXX,XXX          | (bold)
35   | Check                | PASS/FAIL           | =IF(Sources=Uses...)
```

---

## Tab 2: Assumptions

**Purpose**: All user inputs. Blue-filled cells are hard-coded values; a few calculated display cells (e.g., `=PURCHASE_PRICE * LTV` for Loan Amount, validation checks) are acceptable but should be clearly distinguished.

```
SECTION                  | Input Cell         | Unit
─────────────────────────|────────────────────|──────
PROPERTY INFORMATION
Property Name            | [text]             |
Property Address         | [text]             |
Property Type            | [dropdown]         | Office/Retail/Industrial/MF/Mixed-Use
GLA (SF)                 | [number]           | SF
Unit Count (MF only)     | [number]           | Units
Year Built               | [number]           |
Current Occupancy        | [%]                | %

ACQUISITION
Purchase Price           | [number]           | $
Acq Closing Cost %       | 1.50%              | %
Upfront CapEx Reserve    | [number]           | $
Upfront TI/LC Reserve    | [number]           | $

REVENUE
Market Rent ($/SF/yr)    | [number]           | $/SF/yr   (or $/unit/mo for MF)
Annual Rent Growth       | 3.00%              | %
Vacancy & Credit Loss    | 6.00%              | % of PGI
Other Income             | [number]           | $/yr total (or $/unit/yr for MF)
Expense Recovery Rate    | 0%                 | % (for NNN leases: up to 100%)

OPERATING EXPENSES                              [all in $/yr unless noted]
Real Estate Taxes        | [number]           | $/yr
Insurance                | [number]           | $/yr
Utilities (CAM)          | [number]           | $/yr
Repairs & Maintenance    | [number]           | $/yr
Management Fee           | 4.00%              | % of EGI
Administrative           | [number]           | $/yr
Expense Inflation Rate   | 2.50%              | %
CapEx Reserve            | [number]           | $/SF/yr (or $/unit/yr)

CAPITAL EVENTS (rollover — if not using Rent Roll tab)
TI — New Lease           | [number]           | $/SF
TI — Renewal             | [number]           | $/SF
LC — New Lease           | 5.00%              | % of total lease value
LC — Renewal             | 2.50%              | % of total lease value
Rolling Vacancy (months) | 6                  | months at lease expiry

FINANCING
Loan-to-Value (LTV)      | 70.00%             | %
Interest Rate            | 5.50%              | %/yr
Interest-Only Period     | 2                  | years
Amortization Period      | 30                 | years
DSCR Minimum             | 1.25               | x
Debt Yield Minimum       | 8.00%              | %
[display] LTV Loan       | =PP*LTV            | $ (blue: inputs above; black: this row is display)
[display] DY Loan        | =NOI_Y1/DY_Min     | $ (lender DY constraint)
[display] Actual Loan    | =MIN(LTV Loan, DY Loan) | $ (binding constraint — use in debt schedule)

HOLD & EXIT
Hold Period              | 5                  | years
Exit Cap Rate            | 5.75%              | %
Selling Costs            | 1.25%              | % of gross exit value
Unlevered Discount Rate  | 7.50%              | % (for NPV check only)
Target Levered IRR       | 13.00%             | % (for sensitivity color-coding)
```

---

## Tab 3: Rent Roll / Unit Mix

### Multi-Tenant (Office / Retail / Industrial)

**Columns:**
```
A: Tenant Name
B: Suite Number
C: Leased SF
D: Lease Start Date
E: Lease Expiration Date
F: Lease Term Remaining (years)  =MAX(0,(E2-TODAY())/365.25)
G: Rent/SF/Year (current)
H: Annual Rent (current)         =C2*G2
I: Lease Type (Gross/NNN/MG)
J: Annual Escalation %
K: TI/SF at Expiry               =from Assumptions (new or renewal)
L: LC Rate at Expiry             =from Assumptions
M: Market Rent/SF/Yr             =MARKET_RENT_PSF * (1+RENT_GROWTH)^ExpYr
N: Notes
```

**Summary rows below tenant list:**
```
Total Leased SF:     =SUM(C2:C[last])          [explicit range — never whole column]
Total Vacant SF:     =GLA_SF - Total_Leased_SF
Occupancy %:         =Total_Leased_SF / GLA_SF
Total Annual GPR:    =SUM(H2:H[last]) + Vacant_SF * MARKET_RENT_PSF
WALT (years):        =SUMPRODUCT(C2:C[last], F2:F[last]) / Total_Leased_SF
                     [CRITICAL: use explicit data ranges, NOT C:C / F:F — full-column SUMPRODUCT
                      includes header and summary rows, producing inflated or #VALUE! results]
```

**Rollover schedule (year-by-year expirations):**
```
                   | Y1 | Y2 | Y3 | Y4 | Y5 | ...
Expiring SF        |    |    |    |    |    |
Rolling Vacancy ($)|    |    |    |    |    | [expiring SF × market rent × vacancy months/12]
TI ($)             |    |    |    |    |    | [expiring SF × TI_PSF]
LC ($)             |    |    |    |    |    | [new rent × new term × expiring SF × LC_rate]
```
Rolling vacancy represents the lost rent during the period between lease expiry and new tenant commencement (typically 3–12 months). Include it as a revenue deduction or a negative CFBDS item in the Operating Statement in the year of rollover.

### Multifamily (Unit Mix)

**Columns:**
```
A: Unit Type (Studio / 1BR / 2BR / 3BR / Townhome)
B: # Units
C: Unit Size (SF)
D: Current Rent/Mo
E: Market Rent/Mo
F: Annual Revenue (Current)   =B*D*12
G: Annual Revenue (Market)    =B*E*12
H: Notes
```

**Summary:**
```
Total Units:           =SUM(B:B)
Total SF:              =SUMPRODUCT(B:B, C:C)
Avg Current Rent/Mo:   =SUM(F:F)/SUM(B:B)/12
Avg Market Rent/Mo:    =SUM(G:G)/SUM(B:B)/12
Avg $/SF:              =SUM(F:F)/(SUM(B:B)*12) / (SUMPRODUCT(B:B,C:C)/SUM(B:B))
Gross Potential (100%):=SUM(G:G)
```

---

## Tab 4: Operating Statement

**Rows (A) | Year 0 (B) | Year 1 (C) | Year 2 (D) | ... | Year n**

Year 0 column shows acquisition year (pre-operations); Years 1–n show operating projections.

```
Row  | Line Item                              | Formula (Year 1) | Growth
─────|────────────────────────────────────────|──────────────────|──────────────────
     REVENUE
1    | Gross Potential Rent (GPR)              | =RentRoll!GPR_Y1 | × (1+RentGrowth)
2    | (+) Expense Recoveries                  | =GPR×RecovRate  | × (1+RentGrowth)
3    | (+) Other Income                        | =Asmp!OtherInc  | × (1+RentGrowth)
4    | = Potential Gross Income (PGI)          | =SUM(1:3)       |
5    | (−) Vacancy & Credit Loss               | =PGI×VacPct     |
6    | = Effective Gross Income (EGI)          | =PGI-Vacancy    |
     ──────────────────────────────────────────
     OPERATING EXPENSES
7    | (−) Real Estate Taxes                   | =Asmp!RETaxes   | × (1+ExpInfl)
8    | (−) Insurance                           | =Asmp!Insurance | × (1+ExpInfl)
9    | (−) Utilities                           | =Asmp!Utilities | × (1+ExpInfl)
10   | (−) Repairs & Maintenance               | =Asmp!Repairs   | × (1+ExpInfl)
11   | (−) Management Fee                      | =EGI×MgmtFee%  | (% of EGI, auto)
12   | (−) Administrative                      | =Asmp!Admin     | × (1+ExpInfl)
13   | = Total OpEx                            | =SUM(7:12)      |
     ──────────────────────────────────────────
14   | = NET OPERATING INCOME (NOI)            | =EGI-TotalOpEx  | (bold, highlighted)
     ──────────────────────────────────────────
     CAPITAL ITEMS (deducted for CFBDS)
15   | (−) CapEx Reserve                       | =GLA×CapExPSF   | fixed $/SF
16   | (−) Tenant Improvements                 | =RentRoll!TI_Yn | from rollover sched
17   | (−) Leasing Commissions                 | =RentRoll!LC_Yn | from rollover sched
     ──────────────────────────────────────────
18   | = CASH FLOW BEFORE DEBT SERVICE (CFBDS) | =NOI-15-16-17   | (bold)
```

**Note on Y0 column**: Show purchase price, closing costs, upfront reserves as uses only (no NOI). This sets up the Sources & Uses table.

---

## Tab 5: Debt Schedule

**Columns:** Year | Beginning Balance | Annual Debt Service | Interest | Principal | Ending Balance | DSCR | Debt Yield

```
Row | Year | Beg Bal   | Ann DS     | Interest  | Principal | End Bal   | DSCR  | DY
────|──────|───────────|────────────|───────────|───────────|───────────|───────|────
1   | 0    | =Loan Amt | —          | —         | —         | =Loan Amt | —     | —
2   | 1    | =D1       | IO/Amort   | =B2×Rate  | =C2-D2    | =B2-E2    | =NOI/C2 | =NOI/B2
3   | 2    | =F2       | IO/Amort   | ...       | ...       | =B3-E3    | ...   | ...
... | ...  | ...       | ...        | ...       | ...       | ...       | ...   | ...
n   | n    | =F(n-1)   | Amort      | ...       | ...       | =Bn-En    | ...   | ...
```

IO years: `Ann DS = Beginning_Balance × INTEREST_RATE`; `Principal = 0`; `End Bal = Beg Bal`
Amort years: `Ann DS = -PMT(Rate/12, AmortYrs×12, OrigLoanAmt) × 12`

**Conditional formatting on DSCR column:**
- `≥ DSCR_MIN`: green
- `1.10 to DSCR_MIN`: orange
- `< 1.10`: red fill

---

## Tab 6: Cash Flows & Returns

### Section 1: Cash Flow Table

```
Row | Item                          | Y0          | Y1     | Y2     | ... | Yn
────|───────────────────────────────|─────────────|────────|────────|──---|──────
1   | NOI                           | —           | ←OpStmt| ...    | ... | ...
2   | CapEx Reserve                 | —           | ←OpStmt| ...    | ... | ...
3   | Tenant Improvements           | —           | ←OpStmt| ...    | ... | ...
4   | Leasing Commissions           | —           | ←OpStmt| ...    | ... | ...
5   | CFBDS (Unlevered CF)          | −Total Cost | =1−2−3−4 | ... | ... | ...+Exit
6   | Debt Service                  | +Loan Amt   | ←DebtSch| ...  | ... | ...−RemBal
7   | CFADS (Levered CF)            | −Equity     | =5−6   | ...    | ... | ...
```

**Year 0 special values:**
- CFBDS: `= −(Purchase Price + Closing Costs + Upfront Reserves)`
- Debt row: `= +Loan Amount` (positive — proceeds received)
- CFADS: `= −Equity Invested` (net cash out)

**Year n (final) additions:**
- CFBDS: `+ Net Exit Value`
- CFADS: `+ Net Equity Proceeds`

### Section 2: Exit Calculation

```
Row | Item                          | Formula
────|───────────────────────────────|──────────────────────────────────
10  | Year n NOI                    | =OpStmt!NOI_Yn
11  | Rent Growth Rate              | =RENT_GROWTH
12  | Exit NOI (Forward, Year n+1)  | =C10*(1+C11)
13  | Exit Cap Rate                 | =EXIT_CAP
14  | Gross Exit Value              | =C12/C13
15  | Selling Costs %               | =SELL_COST_PCT
16  | Net Exit Value                | =C14*(1-C15)
17  | Remaining Loan Balance        | =DebtSched!EndBal_Yn
18  | Net Equity Proceeds           | =C16-C17
```

### Section 3: Return Summary

```
Row | Metric               | Formula
────|──────────────────────|─────────────────────────────────────────────────────
20  | Total Equity Invested| =−CFADS_Y0
21  | Levered IRR          | =IRR(CFADS_Full_Range, 0.12)
    |                      | [CFADS_Full_Range = {-Equity, CFADS_Y1, ..., CFADS_Yn + NetEquityProceeds}]
22  | Unlevered IRR        | =IRR(CFBDS_Full_Range, 0.10)
    |                      | [CFBDS_Full_Range = {-TotalCost, CFBDS_Y1, ..., CFBDS_Yn + NetExitValue}]
23  | Equity Multiple (EM) | =SUM(CFADS_Full_Range) / Equity
    |                      | [Use the SAME full range as IRR (exit embedded in Year n) — no separate add]
    |                      | [OR: =(SUM(CFADS_Operating_Y1:Yn) + NetEquityProceeds) / Equity
    |                      |  where CFADS_Operating_Y1:Yn excludes exit — pick ONE convention, not both]
24  | Year 1 Cash-on-Cash  | =CFADS_Y1/Equity
25  | Avg Cash-on-Cash     | =(SUM(CFADS_Operating_Y1:Yn)/HOLD_YEARS)/Equity
    |                      | [Operating CFADS only — excludes exit proceeds from Year n]
26  | Unlevered NPV        | =NPV(DISCOUNT_RATE,CFBDS_Y1:CFBDS_Yn+NetExitValue)−TotalCost
    |                      | [positive NPV = premium over required return; discount rate from Assumptions]
27  | Going-in Cap Rate    | =OpStmt!NOI_Y1/PURCHASE_PRICE
28  | Exit Cap Rate        | =EXIT_CAP
29  | Hold Period          | =HOLD_YEARS
30  | Min DSCR             | =MIN(DebtSched!DSCR_Range)
31  | Debt Yield (Y1)      | =OpStmt!NOI_Y1/Loan_Amount
    |                      | [CRITICAL: use original Loan_Amount — NOT current outstanding balance]
```

---

## Tab 7: Sensitivity

### Table 1: Levered IRR (Exit Cap × Rent Growth)

```
     |         | 0.0% | 1.0% | 2.0% | 3.0% | 4.0% | 5.0%  ← Rent Growth (row input cell)
─────|─────────|──────|──────|──────|──────|──────|──────
     |  4.50%  |      |      |      |      |      |
     |  4.75%  |      |      |      |      |      |
↑    |  5.00%  |      |      |    [base]   |      |
Exit |  5.25%  |      |      |      |      |      |
Cap  |  5.50%  |      |      |      |      |      |
     |  5.75%  |      |      |      |      |      |
     |  6.00%  |      |      |      |      |      |
              ↑
       Corner cell = =Returns!LeveredIRR
       (Data Table: Row input = RENT_GROWTH cell, Col input = EXIT_CAP cell)
```

### Table 2: Year 1 DSCR (Interest Rate × LTV)

```
     |         | 55%  | 60%  | 65%  | 70%  | 75%   ← LTV (row input cell)
─────|─────────|──────|──────|──────|──────|──────
     |  4.00%  |      |      |      |      |
     |  4.50%  |      |      |      |      |
↑    |  5.00%  |      |      |      |      |
Int  |  5.50%  |      |      |   [base]    |
Rate |  6.00%  |      |      |      |      |
     |  6.50%  |      |      |      |      |
     |  7.00%  |      |      |      |      |
              ↑
       Corner cell = =DebtSchedule!DSCR_Y1
       (Data Table: Row input = LTV cell, Col input = INTEREST_RATE cell)
```

### Table 3 (Optional): Equity Multiple (Purchase Price × Hold Period)

```
     |         | 3yr  | 4yr  | 5yr  | 7yr  | 10yr  ← Hold Period
─────|─────────|──────|──────|──────|──────|──────
     | −15%    |      |      |      |      |
     | −10%    |      |      |      |      |
↑    |  −5%    |      |      |      |      |
PP   |  base   |      |      | [base]      |
adj  |  +5%    |      |      |      |      |
     | +10%    |      |      |      |      |
     | +15%    |      |      |      |      |
              ↑
       Corner cell = =Returns!EquityMultiple
       (Data Table: Row input = HOLD_YEARS cell, Col input = PURCHASE_PRICE ×scalar)
```

### Conditional Formatting (IRR Table)
- Apply to entire body range of each table (excluding headers/labels)
- IRR table thresholds based on `TARGET_LEVERED_IRR` from Assumptions:
  ```
  Green:  Value ≥ TARGET_IRR
  Yellow: Value ≥ TARGET_IRR − 0.02 AND Value < TARGET_IRR
  Red:    Value < TARGET_IRR − 0.02
  ```
- DSCR table thresholds:
  ```
  Green:  Value ≥ 1.25
  Yellow: Value ≥ 1.10 AND Value < 1.25
  Red:    Value < 1.10
  ```
