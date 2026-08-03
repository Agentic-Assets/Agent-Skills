# CRE Metric Definitions — Formula, Excel Syntax, and the Trap

Every metric below has three parts: what it actually measures, how to write it in Excel, and
the specific mistake that makes it wrong. The traps are the point — the arithmetic is easy and
almost nobody gets it wrong. What people get wrong is *which* number goes into it.

## Contents
1. [The income statement](#the-income-statement)
2. [Yield metrics](#yield-metrics)
3. [Return metrics](#return-metrics)
4. [Credit metrics](#credit-metrics)
5. [Exit and reversion](#exit-and-reversion)
6. [Quick reference: which metric answers which question](#quick-reference)

---

## The income statement

```
  Gross Potential Rent (GPR)      all space at full rent, as if 100% occupied
+ Expense Recoveries              what tenants reimburse (NNN / NN / modified gross)
+ Other Income                    parking, signage, laundry, pet fees, late fees
= Potential Gross Income (PGI)
− Vacancy & Credit Loss           structural vacancy + expected non-payment
= Effective Gross Income (EGI)    what you actually collect
− Operating Expenses              including management fee
= NET OPERATING INCOME (NOI)      before capital, before debt, before tax
− Replacement Reserve             recurring capital (roof, HVAC, parking)
− Tenant Improvements             at rollover only
− Leasing Commissions             at rollover only
= Cash Flow Before Debt Service   (CFBDS) — unlevered free cash flow
− Debt Service                    interest + principal
= Cash Flow After Debt Service    (CFADS) — what equity actually receives
```

**NOI is the hinge of the entire discipline.** Cap rates, debt yield, DSCR, and exit value all
divide into or out of it, so a definitional error in NOI multiplies through everything.

### The three NOI traps

**1. Putting capital costs inside NOI.** Replacement reserve, TI, and LC belong *below* NOI.
Deduct them above the line and NOI falls, which drops the going-in cap rate and — because the
exit cap divides into NOI — drops the exit value too. The error compounds in the direction
that makes the deal look worse, which is why it survives review: nobody challenges a
conservative-looking number.

**2. Double-counting NNN recoveries.** In a triple-net deal the tenant reimburses recoverable
operating expenses. Show the recovery as income *and* the expense as a cost — that nets
correctly. What is wrong is showing the recovery as income while omitting the expense, which
inflates NOI by the full recovery amount. Pick one presentation and be consistent.

**3. Applying market vacancy to contractually obligated rent.** A tenant with eight years left
on a lease is not vacant. Structural vacancy belongs on space that is actually exposed —
vacant suites and near-term expiries. Blanket-applying a market vacancy rate to a fully leased
credit-tenant building understates NOI.

---

## Yield metrics

### Going-in cap rate

```
Going-in Cap Rate = Year 1 NOI / Purchase Price

Excel:  =IF(Asmp_Price>0, Ret_NOI1/Asmp_Price, 0)
```

The unlevered first-year yield on the price. It is a *quoting* convention, not a valuation
method — it compresses an entire cash-flow profile into one number and says nothing about
growth, rollover, or capital needs.

> **Trap:** a seller's quoted cap rate is almost always computed on *their* NOI, which may
> include recoveries you will not collect, exclude reserves you will fund, and use a management
> fee below market. Recompute it on your NOI before comparing anything.

### Yield on cost / development yield

```
Yield on Cost = Stabilized NOI / Total Basis   (price + closing + capital)
```

The right metric for value-add. Going-in cap uses price and Year-1 NOI; yield on cost uses
everything you will put in and the NOI you expect once stabilized. The spread between yield on
cost and the market cap rate is the value you are creating — under ~100 bps, the business plan
is not paying for its own risk.

### Cash-on-cash

```
Year 1 CoC = Year 1 CFADS / Equity Invested
Average CoC = AVERAGE(operating CFADS Y1..Yn) / Equity Invested

Excel:  =IF(Ret_Equity>0, 'Cash Flow'!C39/Ret_Equity, 0)
```

Current distributable yield on equity. It ignores the exit entirely, which is exactly why it
is useful — it is the only return metric that cannot be rescued by an optimistic terminal
assumption.

> **Trap:** including exit proceeds in the average. Average cash-on-cash must use operating
> cash flow only. The workbook keeps operating and reversion on separate rows so this cannot
> happen by accident.

---

## Return metrics

### IRR

The discount rate at which the cash flows net to zero.

```
Unlevered:  Year 0 = −(Price + Closing + Upfront Capital)
            Years 1..n = CFBDS,  plus Net Sale Proceeds in year n

Levered:    Year 0 = −Equity Invested
            Years 1..n = CFADS,  plus Net Equity Proceeds in year n

Excel:  =IRR('Cash Flow'!B38:H38, 0.1)
```

The second argument is a seed guess, not an assumption — it only helps Excel converge. Use
`0.1` for unlevered and `0.12` for levered.

> **Trap 1 — double-counting the exit.** If the year-*n* cash flow already includes sale
> proceeds, do not add them again. Keep an operating row and a total row and point IRR at the
> total row only.
>
> **Trap 2 — timing.** `IRR` assumes evenly spaced periods with the outflow at t=0. If your
> flows are dated, use `XIRR(values, dates, guess)` instead. Mixing them silently shifts the
> answer.
>
> **Trap 3 — sign changes.** IRR is only well defined with at least one sign change. Deals
> with mid-hold capital calls can produce multiple IRRs or none. When IRR misbehaves, that is
> information about the cash-flow shape, not an Excel problem — use NPV at a stated discount
> rate instead.

**Why levered IRR can fall below unlevered IRR:** leverage is accretive only when the cost of
debt is below the unlevered return. Compare the *annual debt constant* — not the interest rate
— against the cap rate. A 6.45% rate on a 30-year amortizing loan has a constant near 7.5%;
against a 7.2% cap that is negative leverage, and adding debt lowers the return while raising
the risk. This is the single most useful thing to be able to explain to a room.

### Equity multiple

```
EM = (operating CFADS Y1..Yn + Net Equity Proceeds) / Equity Invested

Excel:  =IF(Ret_Equity>0,
            (SUM('Cash Flow'!C39:H39) + 'Cash Flow'!H35) / Ret_Equity, 0)
```

Total cash returned per dollar invested. 2.0x means the investment doubled. EM is blind to
time — 2.0x over three years and 2.0x over ten are the same multiple and wildly different
deals. Always quote EM and IRR together.

### NPV and DCF indicated value

```
DCF Value = NPV(discount rate, unlevered operating CF Y1..Yn)
          + Net Sale Proceeds / (1 + discount rate)^n

NPV       = DCF Value − Total Basis

Excel:  =NPV(Asmp_DiscRate, 'Cash Flow'!C37:H37)
        + 'Cash Flow'!H33/(1+Asmp_DiscRate)^Asmp_Hold
```

> **Trap:** Excel's `NPV` discounts the *first* value by one period. It is a present value of a
> t=1..n stream, not a true NPV. Never put the year-0 outflow inside `NPV()` — add it outside,
> or you discount it by a year it never spent.

---

## Credit metrics

### DSCR

```
DSCR = NOI / Annual Debt Service

Excel:  =IF(-C22>0, C14/-C22, "—")
```

How many times operating income covers the payment. Typical minimums: ~1.20x agency/life
company, ~1.25x CMBS, ~1.10x bridge. Confirm against the actual term sheet — these move.

> **Trap:** measuring DSCR during the interest-only period and calling it the answer. IO
> payments are lower, so coverage looks strong and then steps down the day amortization
> begins. The binding test is the **first amortizing year**. The workbook reports it as its own
> line for this reason.

### Debt yield

```
Debt Yield = Year 1 NOI / Original Loan Amount

Excel:  =IF(Asmp_Loan>0, C14/Asmp_Loan, "—")
```

The lender's return if it foreclosed and owned the asset outright. It is deliberately immune to
interest rate, amortization term, and value — which is precisely why lenders rely on it, since
those are the inputs a borrower can most easily argue about. Typical minimums 7.5–10%, tighter
in weaker markets.

> **Trap:** computing it on the *current* balance. As the loan amortizes the balance falls, so
> current-balance debt yield improves every year even if NOI is flat. That is a surveillance
> statistic, not the origination covenant. The workbook shows both rows and labels which is
> which.

### LTV and LTC

```
LTV = Loan / Value      LTC = Loan / Total Cost
```

On an acquisition at market these are close. On a value-add with significant capital they
diverge sharply, and lenders size to the tighter of the two.

---

## Exit and reversion

```
Forward NOI          = NOI in year n+1
Gross Exit Value     = Forward NOI / Exit Cap Rate
Disposition Costs    = Gross Exit Value × cost %
Net Sale Proceeds    = Gross Exit Value − Disposition Costs
Net Equity Proceeds  = Net Sale Proceeds − Loan Payoff

Excel:  =IF(Asmp_ExitCap>0, H30/Asmp_ExitCap, "—")
```

> **The most consequential trap in CRE modeling: capping the wrong NOI.** A buyer in year 5 is
> purchasing year 6's income. The exit cap must divide into **forward** NOI, not the final
> operating year. Using year-5 NOI understates the exit by roughly one year of NOI growth,
> which on a five-year hold is often 60–100 bps of IRR.
>
> This is why the pro forma projects `hold + 1` years. That final column exists solely to
> supply forward NOI and is excluded from every return calculation.

**Exit cap convention:** going-in + 25 to 50 bps. The asset is older at sale and the next buyer
prices that. An exit cap tighter than the going-in cap is a bet on market compression — it can
be right, but it must be stated as a thesis and stress-tested, never left implicit.

**Loan payoff during IO:** if the hold period is entirely within the interest-only period, no
principal has amortized and the payoff equals the original loan.

---

## Quick reference

| Question | Metric |
|---|---|
| What does it yield on day one? | Going-in cap rate |
| Am I creating value? | Yield on cost vs. market cap |
| What does it distribute each year? | Cash-on-cash |
| What is the time-weighted return? | IRR |
| How much total cash comes back? | Equity multiple |
| Is it worth the price? | NPV / DCF indicated value |
| Will the lender lend? | DSCR, debt yield, LTV |
| What breaks it? | Sensitivity on exit cap and rent growth |

**Never quote one alone.** IRR without equity multiple hides duration. Equity multiple without
IRR hides time. Both without DSCR hide whether the deal is financeable at all.
