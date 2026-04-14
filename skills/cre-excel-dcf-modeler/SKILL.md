---
name: cre-excel-dcf-modeler
description: |
  Build discounted cash flow (DCF) valuation models in Excel specifically for commercial real estate (CRE). Use when creating
  CRE acquisition underwriting models, property-level DCF workbooks, NOI projections, rent roll buildouts, debt schedules,
  or IRR/equity-multiple return analyses in Excel or ExcelJS. Covers all CRE property types: office, retail, industrial,
  multifamily, mixed-use, hotel. Trigger on: 'CRE excel model', 'build underwriting model', 'property DCF excel', 'NOI
  projection spreadsheet', 'rent roll model', 'IRR excel', 'acquisition model', 'CRE waterfall', 'cap rate model'.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(cmd:*)
---

# CRE Excel DCF Modeler

Builds institutional-grade CRE acquisition underwriting workbooks following investment manager / ARGUS conventions. CRE Excel models are structurally different from corporate DCF: they use NOI-based cash flows, direct capitalization exit, loan amortization schedules, and CRE-specific return metrics (IRR, equity multiple, cash-on-cash, DSCR, debt yield).

## Prerequisites

- Excel, Google Sheets, or ExcelJS (for programmatic creation via this project's `exceljs` library)
- Property information: type, size, purchase price
- Rent roll or revenue assumptions
- Operating expense data or ratios
- Financing terms (LTV, rate, IO, amortization)

## Sheet Structure (7 tabs, in order)

| Tab | Name | Purpose |
|-----|------|---------|
| 1 | Cover | Deal summary, key metrics dashboard |
| 2 | Assumptions | All user inputs (blue cells) |
| 3 | Rent Roll | Tenant-level revenue model (or Unit Mix for MF) |
| 4 | Operating Statement | EGI → NOI waterfall by year |
| 5 | Debt Schedule | Amortization table, balance, DSCR, debt yield |
| 6 | Cash Flows & Returns | CFBDS, CFADS, IRR, EM, CoC |
| 7 | Sensitivity | IRR/EM sensitivity tables (2-variable) |

See `references/cre-model-structure.md` for full sheet layouts.

## Instructions

### 1. Assumptions Sheet (Tab 2) — User Inputs Only

Color-code convention: **blue** = user input, **black** = formula, **green** = cross-sheet reference.

```
Property Information
├── Property Name / Address
├── Property Type  (Office / Retail / Industrial / MF / Mixed-Use / Hotel)
├── GLA (SF) or Unit Count
└── Year Built

Acquisition
├── Purchase Price
├── Acquisition Closing Costs %      (default: 1.5%)
├── Upfront CapEx / TI Reserve       ($)

Revenue Assumptions
├── Market Rent ($/SF/yr or $/unit/month)
├── Annual Rent Growth Rate          (% — applied to market rent each year)
├── Vacancy & Credit Loss %          (% of PGI)
├── Other Income                     ($ or $/unit/yr)

Operating Expenses
├── Real Estate Taxes                ($ or $/SF/yr)
├── Insurance                        ($ or $/SF/yr)
├── Utilities (CAM)                  ($ or $/SF/yr)
├── Repairs & Maintenance            ($ or $/SF/yr)
├── Management Fee %                 (% of EGI)
├── Administrative                   ($ or $/SF/yr)
├── CapEx Reserve                    ($/SF/yr or $/unit/yr)

Financing
├── Loan-to-Value (LTV) %
├── Interest Rate %
├── Interest-Only Period (years)
├── Amortization Period (years)
├── DSCR Minimum                     (default: 1.25x)
├── Debt Yield Minimum               (default: 8%)

Hold Period & Exit
├── Hold Period (years)
├── Exit Cap Rate %                  (convention: going-in + 25–50 bps)
├── Selling Costs %                  (default: 1.25%)
```

**Critical**: Every projection cell must link back to Assumptions. Never hardcode a value in the projection sheets.

### 2. Rent Roll Sheet (Tab 3)

For office/retail/industrial (multi-tenant):
```
Columns: Tenant | Suite | Leased SF | Lease Start | Lease End | Rent/SF/Yr | Annual Rent | Lease Type | Escalation | Market Rent/SF
```
- Row per tenant
- Totals row: Total Leased SF, Total Annual Rent
- Vacant row: Vacant SF at market rent
- GPR summary: in-place rent + vacant at market rent

For multifamily (unit mix):
```
Columns: Unit Type | # Units | Unit Size SF | Current Rent/Mo | Market Rent/Mo | Annual Revenue
```
- Row per unit type (Studio, 1BR, 2BR, etc.)
- Physical vacancy applied via assumption

For NNN leases: add Expense Recovery column.

### 3. Operating Statement Sheet (Tab 4)

Build the NOI waterfall by year (Y0 through Yn):

```
               | Y1      | Y2      | ... | Yn
Gross Potential Rent     ← from Rent Roll × (1+growth)^yr
+ Expense Recoveries     ← NNN tenants (if applicable)
+ Other Income           ← from Assumptions
= PGI
- Vacancy & Credit Loss  ← PGI × vacancy %
= EGI
- Real Estate Taxes      ← grown by expense inflation rate
- Insurance
- Utilities
- Repairs & Maintenance
- Management Fee         ← % × EGI
- Administrative
= NOI
- CapEx Reserve          ← $/SF × SF or $/unit × units
- Tenant Improvements    ← from rollover schedule
- Leasing Commissions    ← from rollover schedule
= CFBDS (Cash Flow Before Debt Service)
```

Apply rent growth to GPR each year: `=GPR_Y1 × (1 + RentGrowth)^(year-1)`
Apply expense growth (typically 2–3%) to all fixed-cost line items.

### 4. Debt Schedule Sheet (Tab 5)

One row per year:

```
| Year | Beginning Balance | Annual Debt Service | Interest Paid | Principal Paid | Ending Balance | DSCR | Debt Yield |
```

Key formulas (see `references/cre-excel-formulas.md` for Excel syntax):
- IO years: `Debt Service = Loan × Rate`; balance unchanged
- Amortizing years: `Debt Service = PMT(Rate/12, AmortYrs×12, Loan) × 12`
- `DSCR = NOI / Debt Service`  (flag if < DSCR_Min with conditional formatting)
- `Debt Yield = NOI / Beginning Balance`

### 5. Cash Flows & Returns Sheet (Tab 6)

```
Year 0 — Equity Investment:
  Total Cost = Purchase Price + Closing Costs + Upfront Reserves
  Equity     = Total Cost − Loan Amount

Years 1–n:
  CFBDS  (from Operating Statement)
  − Debt Service (from Debt Schedule)
  = CFADS

Year n — Exit Reversion:
  Exit NOI (forward) = Year n NOI × (1 + RentGrowth)
  Gross Exit Value   = Exit NOI / Exit Cap Rate
  Net Exit Value     = Gross Exit Value × (1 − Selling Costs)
  Remaining Balance  = Ending Balance from Debt Schedule Year n
  Net Equity Proceeds = Net Exit Value − Remaining Balance

Return Calculations:
  Unlevered IRR  = IRR({−TotalCost, CFBDS_Y1, ..., CFBDS_Yn + NetExitValue})
  Levered IRR    = IRR({−Equity, CFADS_Y1, ..., CFADS_Yn + NetEquityProceeds})
  Equity Multiple = (Σ CFADS + Net Equity Proceeds) / Equity
  Year 1 CoC    = CFADS_Y1 / Equity
  Going-in Cap  = NOI_Y1 / Purchase Price
```

### 6. Sensitivity Sheet (Tab 7)

Build two standard 2-variable tables:

**Table 1 — Levered IRR by Exit Cap Rate × Rent Growth**
- Rows: Exit Cap Rate (going-in ± 100 bps in 25 bps increments)
- Columns: Rent Growth (0% to 5% in 1% increments)
- Corner cell: `=Returns!LeveredIRR`
- Use Excel Data Table (Data → What-If → Data Table)

**Table 2 — DSCR by Interest Rate × LTV**
- Rows: Interest Rate (base ± 150 bps in 50 bps increments)
- Columns: LTV (55% to 75% in 5% increments)
- Corner cell: `=DebtSchedule!DSCR_Y1` (first amortizing year DSCR — the binding lender test; use a named range defined on the debt schedule sheet)

Apply conditional formatting:
- IRR table: green ≥ target IRR, yellow = within 200 bps, red < target
- DSCR table: green ≥ 1.25x, yellow 1.10–1.25x, red < 1.10x

---

## Error Handling

| Error | Cause | Correct Approach |
|-------|-------|-----------------|
| `#DIV/0!` in DSCR | Zero debt service (no loan) | Wrap: `=IF(DS=0, "N/A", NOI/DS)` |
| `#DIV/0!` in cap rate | Zero purchase price | Wrap: `=IF(PP=0, "N/A", NOI/PP)` |
| Negative equity | LTV > 100% or typo | Validate LTV < 100%; add check cell |
| IRR not converging | All same-sign CFs | Verify Year 0 is negative (equity outflow) |
| Exit cap < going-in cap | Model assumption error | Flag with conditional format; warn user |
| DSCR < 1.00 | Debt service exceeds NOI | Flag red; model may not be financeable |
| Loan > Debt Yield min | DY = NOI/Loan < floor | Flag; lender will cut loan proceed |
| Terminal growth ≥ discount rate | Gordon Growth break | Not applicable to CRE (uses cap rate exit) |

---

## Formatting Standards

- **Blue fill + white text**: All user input cells (Assumptions tab)
- **No fill**: Formula cells
- **Green text**: Cross-sheet references
- **Bold + gray background**: Section headers and totals
- **Red text / red fill**: Negative cash flows, DSCR breaches
- **Borders**: Around each major section (NOI summary, returns summary)
- **Number formats**: `$1,234,567` for dollar amounts; `0.0%` for percentages; `0.00x` for multiples

---

## Validation Checklist

Before delivering the model:
- [ ] Sources = Uses: `Loan + Equity = Purchase Price + Closing Costs + Reserves`
- [ ] Going-in cap rate matches seller's stated cap (cross-check NOI ÷ PP)
- [ ] DSCR ≥ 1.25x in every year — check **first amortizing year** (not just IO period)
- [ ] Debt Yield ≥ 8% at origination using **original loan amount** (not current balance)
- [ ] Loan amount = MIN(LTV × PP, NOI_Y1 / DY_min) — DY constraint may cut proceeds below LTV
- [ ] Exit cap ≥ going-in cap (warning if compressed; document value-add rationale)
- [ ] Exit NOI is forward NOI (Year n+1), NOT Year n NOI
- [ ] IO period debt service = Loan × Rate only (no principal)
- [ ] Amortizing period PMT uses original loan amount, not remaining balance
- [ ] All projection cells link to Assumptions (no hardcoded values)
- [ ] Unlevered IRR > going-in cap rate (sanity: unlevered return must beat cap rate)
- [ ] Avg CoC range uses operating CFADS only (exclude exit year reversion)
- [ ] Sensitivity tables use DATA TABLE (Excel) or programmatic loop (ExcelJS) — not hardcoded values

---

## Examples

**Example 1 — Multifamily Acquisition**
Request: "Build a 5-year DCF model for a 120-unit apartment building at $15M, 5.5% cap rate, 70% LTV, 5% interest, 2-year IO, DSCR 1.25x"
Result: 7-tab workbook with unit mix, stabilized NOI waterfall, debt schedule, levered IRR ~14%, EM 1.85x, sensitivity tables

**Example 2 — Industrial NNN Acquisition**
Request: "Model a 250,000 SF industrial building at $20M, in-place NNN lease at $6.50/SF, 7-year term, 3% annual bumps, exit at 5.25% cap"
Result: Rent roll with single tenant, NNN expense recoveries, minimal landlord OpEx, 7-tab model with IRR bridge analysis

**Example 3 — Value-Add Office**
Request: "Underwrite a 60,000 SF office at $8M, 55% occupied, lease-up over 3 years to 90%, $50/SF TI, 5% LC, 6.5% exit cap"
Result: Multi-tenant rent roll with vacancy burn-off, TI/LC schedule, stabilized and as-is NOI projection, levered IRR 16%

---

## Resources

- `references/cre-excel-formulas.md` — All CRE-specific Excel formula templates
- `references/cre-model-structure.md` — Detailed cell-by-cell layout for each sheet
- `cre-dcf-valuation` skill — CRE DCF methodology and property-type benchmarks
