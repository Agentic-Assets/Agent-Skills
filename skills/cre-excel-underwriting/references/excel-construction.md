# Building a CRE Model in Excel by Hand

The generator produces a correct workbook in seconds. This document is for the other half of
the job: understanding the construction well enough to build one yourself, extend one, or take
apart somebody else's. Workshop material lives here.

## Contents
1. [Structural principles](#structural-principles)
2. [Sheet architecture](#sheet-architecture)
3. [Named ranges](#named-ranges)
4. [The formula patterns](#the-formula-patterns)
5. [Sensitivity and data tables](#sensitivity-and-data-tables)
6. [Formatting discipline](#formatting-discipline)
7. [Integrity checks](#integrity-checks)
8. [Google Sheets and LibreOffice](#google-sheets-and-libreoffice)

---

## Structural principles

Four rules separate a model that survives diligence from one that does not.

**1. Inputs live in exactly one place.** Every assumption appears once, on the Assumptions tab,
in blue. Everything else references it. The moment the same number is typed in two cells, they
will diverge — not maybe, eventually.

**2. Nothing is typed into a calculated row.** If a row is a formula, every cell in it is a
formula. A hardcoded value inside a calculated row is a plug: it will not respond to a scenario
change, and it is invisible to anyone reading the numbers rather than the formula bar.

**3. Rates never appear inside formulas.** `=C4*1.03` is wrong even though it computes
correctly. The 3% cannot be flexed, cannot be sensitised, and will not appear when someone
reviews the assumptions. Write `=C4*(1+Asmp_ExpGrowth)`.

**4. One direction of flow.** Assumptions → Revenue → Expenses → Cash Flow → Debt → Returns.
When a later sheet feeds an earlier one you get either a circular reference or, worse, a model
that quietly resolves to something nobody intended.

> **Where circularity really comes from in CRE models:** an OpEx *ratio* applied to EGI while
> recoveries feed EGI. Expenses depend on income, income depends on recoveries, recoveries
> depend on expenses. The clean fix is structural — use an OpEx ratio *or* recoveries, never
> both. Ratio mode suits gross-lease and multifamily deals; line-item mode with recoverable
> flags suits NNN and modified-gross. This is enforced rather than warned about.

---

## Sheet architecture

| # | Sheet | Contains |
|---|---|---|
| 1 | README | Colour legend, conventions used, warnings raised at build |
| 2 | Assumptions | Every input, with unit and **source** columns |
| 3 | Revenue | Unit mix or rent roll, rolling up to one GPR row |
| 4 | Operating Expenses | Line items with per-item growth, and the recoverable pool |
| 5 | Cash Flow | The pro forma, coverage tests, exit block, return cash-flow rows |
| 6 | Debt Schedule | Beginning balance, interest, principal, service, ending balance |
| 7 | Returns | Sources & uses, going-in metrics, returns, value, covenant tests |
| 8 | Sensitivity | Two-way tables on the assumptions that actually move the answer |
| 9 | Checks | Visible integrity tests |

**Columns follow one convention throughout:** column A is labels, column B is Year 0, and years
1..n run from column C. Year 0 carries only the acquisition outflow. Keeping this identical on
every sheet is what makes cross-sheet formulas safe to copy.

**Keep the Checks tab visible.** Institutional models often hide it. For a model that will be
read by people who did not build it — which is every model that matters — a visible checks tab
tells the reader the model is internally consistent and teaches them what to verify.

---

## Named ranges

Named ranges are the difference between a model you can read and one you can only trace.

```excel
=IF(Asmp_Price>0, Ret_NOI1/Asmp_Price, 0)     ' obvious
=IF($B$8>0, $B$12/$B$8, 0)                    ' correct, unreadable
```

Naming convention used throughout:

| Prefix | Meaning | Examples |
|---|---|---|
| `Asmp_` | An input on the Assumptions tab | `Asmp_Price`, `Asmp_ExitCap`, `Asmp_RentGrowth` |
| `Ret_` | A headline output on the Returns tab | `Ret_Equity`, `Ret_NOI1`, `Ret_DCFValue` |

**To create one:** select the cell → Formulas ▸ Define Name, or type the name into the Name Box
left of the formula bar. **To audit them:** Formulas ▸ Name Manager. Any name showing `#REF!`
points at a deleted cell and is a live defect.

Name the assumptions and the handful of outputs other sheets need. Naming all 300 projection
cells produces a Name Manager nobody will ever read.

---

## The formula patterns

### Revenue

```excel
' Simple: SF × market rent, escalated
=Asmp_SF * Asmp_RentPSF * (1+Asmp_RentGrowth)^(year-1)

' Unit mix: each type's annual rent, escalated, then summed
=$E$6 * (1+Asmp_RentGrowth)^(year-1)

' Rent roll: each lease at ITS OWN contractual bump
=$E$6 * (1+$F$6)^(year-1)
```

The rent-roll form matters. A lease with fixed 2% bumps escalates at 2%, not at whatever
market rent is doing. Compounding in-place leases at market growth is one of the most common
ways a model quietly overstates revenue.

### Expenses

```excel
' Line item, growing at its own rate (rate in column B, not in the formula)
=C4*(1+$B4)

' Ratio mode: anchor to YEAR-1 EGI, then inflate
='Cash Flow'!C10 * Asmp_OpExRatio * (1+Asmp_ExpGrowth)^(year-1)

' Management fee scales with actual collections
=-C10*Asmp_MgmtFee
```

> Anchoring the ratio to Year-1 EGI is deliberate. Applying the ratio to *each* year's EGI
> forces expenses to grow at exactly the revenue rate, which holds the margin constant forever
> and erases the NOI margin change the model exists to show. Expenses and revenue grow at
> different rates in reality; the model has to be able to express that.

### Capital costs

```excel
' Replacement reserve
=-Asmp_SF*Asmp_ReservePSF*(1+Asmp_ExpGrowth)^(year-1)

' TI, probability-weighted across renewal and new leases
=-Asmp_SF*Asmp_RollPct*(Asmp_Renewal*Asmp_TIrenew+(1-Asmp_Renewal)*Asmp_TInew)

' LC as a % of total lease value
=-Asmp_SF*Asmp_RollPct*Asmp_RentPSF*(1+Asmp_RentGrowth)^(year-1)
  *Asmp_Term*(Asmp_Renewal*Asmp_LCrenew+(1-Asmp_Renewal)*Asmp_LCnew)
```

Blending renewal and new-lease costs by renewal probability is the standard simplification when
you do not have a lease-by-lease schedule. With a real rent roll, model expiries explicitly —
see `rent-roll-modeling.md`.

### Debt schedule

This is where hand-built models break most often, so the structure is worth internalising.

```excel
' Beginning balance
=Asmp_Loan                       ' year 1
=B5                              ' later years: prior ending balance

' Interest — IO years vs amortizing years, decided live
=IF(Asmp_Loan<=0, 0,
   IF(year<=Asmp_IO,
      C5*Asmp_Rate,
      -CUMIPMT(Asmp_Rate/12, Asmp_Amort*12, Asmp_Loan,
               MAX(1,(year-Asmp_IO-1)*12+1), MAX(1,(year-Asmp_IO)*12), 0)))

' Principal
=IF(Asmp_Loan<=0, 0,
   IF(year<=Asmp_IO, 0,
      -CUMPRINC(Asmp_Rate/12, Asmp_Amort*12, Asmp_Loan,
                MAX(1,(year-Asmp_IO-1)*12+1), MAX(1,(year-Asmp_IO)*12), 0)))

' Ending balance
=MAX(0, C5-C7)
```

Four things to get right:

1. **`CUMIPMT` and `CUMPRINC` always take the ORIGINAL principal**, never the current balance.
   They compute from the loan's own amortization schedule. Feeding them the current balance
   understates interest in every year after the first.
2. **Negate them.** Both return negative values, following Excel's cash-flow sign convention.
3. **Offset the periods by the IO years.** The first amortizing year is periods 1–12 of the
   amortization schedule, not periods 13–24 of the loan's life.
4. **Structure the IO/amortizing split with a live `IF`**, not by writing different formulas
   into different columns. Excel only evaluates the taken branch, so the `CUMIPMT` in the false
   branch never errors during IO years — and changing `Asmp_IO` restructures the whole schedule
   automatically, which is what makes the model worth having.

Sanity check the whole schedule with one formula:

```excel
=IF(Asmp_Loan>0, -PMT(Asmp_Rate/12, Asmp_Amort*12, Asmp_Loan)*12, 0)
```

Total debt service in any amortizing year must equal this constant.

### Returns

```excel
=IRR('Cash Flow'!B38:H38, 0.1)                            ' unlevered
=IRR('Cash Flow'!B40:H40, 0.12)                           ' levered
=(SUM('Cash Flow'!C39:H39)+'Cash Flow'!H35)/Ret_Equity    ' equity multiple
=NPV(Asmp_DiscRate,'Cash Flow'!C37:H37)
   +'Cash Flow'!H33/(1+Asmp_DiscRate)^Asmp_Hold           ' DCF value
```

Note the row discipline: row 37 is unlevered operating, 38 is unlevered total, 39 is levered
operating, 40 is levered total. IRR points at the *total* rows; equity multiple and average
cash-on-cash use the *operating* rows plus the reversion added once. Separating them is what
makes double-counting the exit structurally impossible.

---

## Sensitivity and data tables

A two-variable Data Table is the native Excel tool for this, and it is worth teaching because
almost nobody knows it exists.

**Setup:**
1. Put the output formula in the **top-left corner** of the grid — e.g. `=Returns!B16`.
2. Row headers run across the top; column headers run down the left.
3. Select the whole block **including** both header lines.
4. Data ▸ What-If Analysis ▸ Data Table.
5. *Row input cell* = the assumption varying across the columns. *Column input cell* = the
   assumption varying down the rows.

Excel substitutes each pair into the live model and records the result — a genuine re-run of
the entire workbook per cell, not an approximation.

**Two constraints worth knowing:**

- Data tables recalculate with the workbook. On a large model set Formulas ▸ Calculation
  Options ▸ *Automatic Except for Data Tables* while working.
- **LibreOffice and Google Sheets do not round-trip two-variable data tables.** LibreOffice
  rewrites them into legacy `TABLE()` calls and corrupts the body. This is why the generated
  Sensitivity tab ships Table 1 (IRR) as computed values with instructions to convert it in
  desktop Excel, and Table 2 (DSCR) as live formulas — DSCR is a single-formula metric that can
  be computed directly per cell, while IRR requires re-running the entire projection.

**What to sensitise.** Only the assumptions that actually move the answer:

| Table | Axes | Output |
|---|---|---|
| 1 | Exit cap rate × rent growth | Unlevered IRR |
| 2 | Interest rate × LTV | Year-1 DSCR |

Exit cap is almost always the largest single driver of IRR on a 5–10 year hold. If a sensitivity
table shows the answer barely moving, the axes are wrong or the ranges are too narrow.

---

## Formatting discipline

The colour convention is universal in institutional finance. Follow it and any analyst can read
your model cold.

| Colour | Meaning |
|---|---|
| **Blue** text | Hardcoded input — the only cells anyone should type into |
| **Black** text | Formula on this sheet |
| **Green** text | Link to another sheet in this workbook |
| **Red** text | Link to an external file |
| Amber fill | Needs attention — here, an undocumented assumption |

Number formats that prevent misreading:

```
Currency    $#,##0;($#,##0);"—"        negatives in parentheses, zeros as em-dash
Percent     0.00%;(0.00%);"—"          two decimals — 6.5% vs 6.45% is 5 bps of value
Multiple    0.00"x";;"—"               DSCR and equity multiple
Count       #,##0;(#,##0);"—"
```

Always state units in the header: "Revenue ($)", "Rent ($/SF/yr)", "Loan ($mm)". A column of
numbers with no unit is where the 100x error lives.

---

## Integrity checks

Build these as visible formulas. Each should evaluate to zero.

```excel
=(Asmp_Loan+Ret_Equity)-Ret_Basis                        ' sources = uses
='Cash Flow'!C14-('Cash Flow'!C10+'Cash Flow'!C13)       ' NOI = EGI − OpEx
='Cash Flow'!C20-('Cash Flow'!C14+'Cash Flow'!C19)       ' CFBDS = NOI − capital
='Cash Flow'!C23-('Cash Flow'!C20+'Cash Flow'!C22)       ' CFADS = CFBDS − debt service
='Debt Schedule'!C9-('Debt Schedule'!C5-'Debt Schedule'!C7)   ' end = begin − principal
='Cash Flow'!H31-'Cash Flow'!H30/Asmp_ExitCap            ' exit = forward NOI ÷ cap
='Cash Flow'!H40-('Cash Flow'!H39+'Cash Flow'!H35)       ' no double-counted exit
```

Wrap each in a status flag so the tab is readable at a glance:

```excel
=IF(ABS(B4)<0.01,"OK","CHECK")
```

The last two are the ones that catch the expensive errors. Everything else catches typos.

---

## Google Sheets and LibreOffice

The core model is portable. `PMT`, `IRR`, `NPV`, `FV`, `CUMIPMT`, and `CUMPRINC` all behave
identically. What does not port:

| Feature | Excel | Google Sheets | LibreOffice |
|---|---|---|---|
| Two-variable data tables | Yes | No | Corrupts on save |
| Named ranges | Yes | Yes | Yes |
| `CUMIPMT` / `CUMPRINC` | Yes | Yes | Yes |
| Number format sections | Yes | Partial | Yes |

For Google Sheets, replace data tables with an explicit grid of formulas, or compute the grid
externally and paste values with a note saying when they were generated.

**LibreOffice is fine for recalculating and checking a model** — that is exactly what
`verify_model.py` uses it for — but do not save a workbook containing data tables from it.
