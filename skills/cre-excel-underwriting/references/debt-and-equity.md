# Debt Sizing, Amortization, Covenants, and the Equity Waterfall

## Contents
1. [Sizing the loan](#sizing-the-loan)
2. [Amortization mechanics](#amortization-mechanics)
3. [Covenants](#covenants)
4. [Positive vs negative leverage](#positive-vs-negative-leverage)
5. [Refinance](#refinance)
6. [LP/GP waterfalls and promote](#lpgp-waterfalls-and-promote)

---

## Sizing the loan

Lenders size to the **tightest** of three constraints, not to whichever the borrower prefers.

```
LTV constraint:        Loan = LTV × Value
Debt yield constraint: Loan = Year 1 NOI / minimum debt yield
DSCR constraint:       Loan = (Year 1 NOI / minimum DSCR) / annual debt constant

Annual debt constant = -PMT(rate/12, amort_years*12, 1) * 12
```

Excel:

```excel
=MIN( Asmp_Price*Asmp_LTV,
      Ret_NOI1/Asmp_DYMin,
      (Ret_NOI1/Asmp_DSCRMin) / (-PMT(Asmp_Rate/12,Asmp_Amort*12,1)*12) )
```

The builder supports all three via `debt.sizing_method` = `"ltv"`, `"amount"`, or `"dscr"`.
When a deal is marketed at a headline LTV, compute all three anyway — if debt yield or DSCR
binds tighter, the quoted proceeds are not real and the equity requirement is larger than the
seller's materials suggest.

**Rate environment matters more than LTV.** When rates rise, the DSCR constraint binds long
before the LTV constraint. A deal that sized to 70% LTV at a 4.5% rate may only size to 55% at
7%, on identical NOI. This is the mechanism behind most repricing.

---

## Amortization mechanics

### The payment

```excel
=-PMT(rate/12, amort_years*12, loan_amount)        ' monthly, positive
=-PMT(rate/12, amort_years*12, loan_amount)*12     ' annual constant
```

`PMT` returns a negative number by Excel's sign convention. Negate it, or pass a negative
present value — do not do both.

### Interest-only

During IO, debt service is interest alone and the balance does not move:

```
Debt Service = Loan × Rate
Ending Balance = Beginning Balance
```

**If the hold period sits entirely inside the IO period, the payoff at exit equals the original
loan.** No principal has been repaid. Models that assume amortization regardless of IO
understate the payoff and overstate equity proceeds.

### The amortizing years

```excel
' Interest in a given amortizing year
=-CUMIPMT(rate/12, amort*12, ORIGINAL_LOAN,
          (year-IO-1)*12+1, (year-IO)*12, 0)

' Principal in that year
=-CUMPRINC(rate/12, amort*12, ORIGINAL_LOAN,
           (year-IO-1)*12+1, (year-IO)*12, 0)
```

Three rules:

1. **Original principal, never the current balance.** These functions compute from the loan's
   own schedule. Passing the current balance understates interest in every year after the first.
2. **Negate the result.**
3. **Offset periods by the IO years.** The first amortizing year is periods 1–12 of the
   amortization schedule.

### Balance at any point

```excel
=FV(rate/12, months_amortized, monthly_payment, -loan_amount)
```

Positive result, no outer negation. With `months_amortized = 0` it returns the original loan —
which is exactly right for an IO-only hold.

Or track it directly, which is easier to audit: `Ending = Beginning − Principal`.

---

## Covenants

### DSCR

```
DSCR = NOI / Annual Debt Service
```

Test it in the **first amortizing year**, not during IO. IO coverage is flattering and is not
what the lender sizes to. Common minimums: ~1.20x agency/life co, ~1.25x CMBS, ~1.10x bridge —
confirm against the actual term sheet.

A breach triggers a cash trap (excess cash flow swept to a lender-controlled account) before it
triggers default. Model the trap if coverage is tight, because it interrupts distributions and
therefore the levered IRR even when the loan never defaults.

### Debt yield

```
Debt Yield = Year 1 NOI / ORIGINAL Loan Amount
```

The lender's unlevered return if it took the keys. Immune to rate, amortization, and value —
which is why it exists, since those are the inputs most open to argument. Typical minimums
7.5–10%.

Use the original loan amount. Current-balance debt yield improves automatically as the loan
amortizes and is a surveillance statistic only.

### Ranking

At origination, debt yield and DSCR bind more often than LTV. In appraisal-driven
recapitalizations LTV binds. Model all three — the covenant test block on the Returns tab
reports each against its threshold.

---

## Positive vs negative leverage

The most useful concept to be able to explain, and the most commonly misunderstood.

```
Positive leverage:  Going-in cap rate  >  annual debt constant
Negative leverage:  Going-in cap rate  <  annual debt constant
```

**Compare against the debt constant, not the interest rate.** A 6.45% rate on a 30-year
amortizing loan carries a constant of roughly 7.5%, because principal repayment consumes cash
flow too. Against a 7.2% cap, that deal is in negative leverage even though the rate looks
comfortably below the cap.

Under negative leverage, adding debt *lowers* the levered return while *raising* the risk. When
a model shows levered IRR below unlevered IRR, this is almost always why, and it is a real
result rather than an error.

Interest-only periods mask this: during IO the constant equals the rate, so leverage looks
accretive until amortization begins. Check the constant in the first amortizing year.

---

## Refinance

Model a refinance as three events in the same year:

1. Pay off the existing balance
2. Draw new proceeds, sized on the then-current NOI and the new rate
3. Distribute the net (or fund a shortfall)

```
Net Refi Proceeds = New Loan − Old Balance − Refi Costs
```

The proceeds are a **return of capital**, not income. They belong in the levered cash-flow row
in the refinance year, and they do not touch NOI. A cash-out refinance can lift the equity
multiple substantially while leaving unlevered returns untouched — which is the point, and also
why a deal that only works with a refinance is a bet on the rate environment at that date, not
on the asset.

---

## LP/GP waterfalls and promote

Not built into the generator. Add it as a sheet below Returns when the deal has a promote
structure — which most institutional deals do.

### Structure

Distributions flow through tiers in order. Each tier fills before the next receives anything.

```
Tier 1 — Return OF capital:   100% to LP until contributed capital is returned
Tier 2 — Preferred return:    100% to LP until an 8% IRR is achieved
Tier 3 — Catch-up (optional): 100% (or 50/50) to GP until GP has its target share of profit
Tier 4 — Residual split:      80/20 LP/GP, often stepping to 70/30 above a 14% IRR hurdle
```

### European vs American

- **European (fund-level):** hurdles are tested on aggregate cash flows across the whole fund.
  LP capital and preferred return come back before *any* promote is paid. LP-favourable.
- **American (deal-by-deal):** hurdles are tested per deal, so the GP earns promote on winners
  before losers resolve. Almost always paired with a clawback.

State which one applies. The same headline split produces materially different GP economics.

### Building it in Excel

The clean approach is an IRR-hurdle waterfall computed on cumulative cash flows:

```excel
' Cash required to hit the hurdle IRR through year n
=Equity*(1+Hurdle)^n - SUM(prior distributions compounded to year n)

' Tier distribution
=MIN(remaining_cash, cash_required_for_this_tier)

' Residual after all hurdles
=remaining_cash * LP_share    /    =remaining_cash * GP_share
```

Two rules that prevent the common errors:

- **Compound the hurdle on unreturned capital**, not on original capital. A partially returned
  investment accrues preferred return on the remaining balance only.
- **Test each tier against cumulative distributions**, not the current year alone.

Verify the waterfall with one check: **the sum of LP and GP distributions across every tier and
every year must equal total levered cash flow.** If it does not, cash is being created or
destroyed somewhere in the tiers. Build that check as a visible formula.
