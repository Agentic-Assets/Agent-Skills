# Lease-Level Rent Roll Modeling

The generated workbook grows each lease at its own contractual escalation. That is correct for
in-place income, but it does **not** model what happens when a lease expires. When rollover
drives the deal — which is almost always true for office and multi-tenant retail — extend the
model by hand using this document.

## Contents
1. [When lease-level detail is required](#when-lease-level-detail-is-required)
2. [The four events at expiry](#the-four-events-at-expiry)
3. [Building the schedule](#building-the-schedule)
4. [WALT and rollover exposure](#walt-and-rollover-exposure)
5. [Mark-to-market](#mark-to-market)
6. [Common errors](#common-errors)

---

## When lease-level detail is required

| Situation | Approach |
|---|---|
| Multifamily, self-storage | Never — annual/monthly leases, use unit mix |
| Single-tenant NNN, term beyond hold | Not needed — no rollover in the hold period |
| Industrial, 1–3 tenants, long leases | Aggregate is usually fine |
| Multi-tenant office or retail | **Required** |
| Any deal where >20% of GLA expires during the hold | **Required** |
| Value-add thesis based on marking rents to market | **Required** |

The test: if the answer changes materially depending on *when* space rolls, model the timing.

---

## The four events at expiry

When a lease reaches its expiration, four things happen — and blended-probability modeling
handles all four at once.

**1. Renewal or vacancy.** Renewal probability is typically 60–75%, higher for industrial and
anchored retail, lower for small office suites.

**2. Downtime on non-renewal.** If the tenant leaves, the space generates no rent for a
re-letting period — typically 3–12 months depending on asset type and market. Downtime is the
single most commonly omitted item in amateur models, and it hits both rent and recoveries.

**3. Rent resets to market.** The new rent is market rent grown to that year, not the old
contract rent. This is where mark-to-market gain or loss is realised.

**4. TI and LC are incurred.** Both land in the year the new lease commences, and renewal costs
are far lower than new-lease costs because the buildout is reused.

Blended expected cost at a rollover:

```
Expected TI  = P(renew) × TI_renewal + (1 − P(renew)) × TI_new
Expected LC  = P(renew) × LC_renewal + (1 − P(renew)) × LC_new
Expected downtime = (1 − P(renew)) × downtime_months
```

Excel:

```excel
=-rolling_SF*(Asmp_Renewal*Asmp_TIrenew+(1-Asmp_Renewal)*Asmp_TInew)
=-rolling_SF*market_rent*lease_term*(Asmp_Renewal*Asmp_LCrenew+(1-Asmp_Renewal)*Asmp_LCnew)
=-rolling_SF*market_rent*(1-Asmp_Renewal)*downtime_months/12
```

---

## Building the schedule

One row per lease, one column per year. For each lease and year:

```excel
' Is the lease still in place this year?
=IF(year <= lease_end_year - start_year + 1, in_place_rent, rollover_rent)

' In-place rent — the lease's OWN escalation
=base_rent*(1+$F6)^(year-1)

' Post-rollover rent — market rent grown to that year,
' net of expected downtime in the rollover year only
=SF*Asmp_RentPSF*(1+Asmp_RentGrowth)^(year-1)
   *IF(year=rollover_year, 1-(1-Asmp_Renewal)*downtime_months/12, 1)
```

Sum the lease rows into a single Gross Potential Rent row and the rest of the model is
unchanged. Keep the roll-up as the only interface to the Cash Flow tab, so the downstream model
never has to know how revenue was built.

Add a **vacant space** row for currently empty suites: market rent from the assumed lease-up
date, with its own TI and LC in the lease-up year.

---

## WALT and rollover exposure

```
WALT = Σ(tenant SF × remaining term) / total leased SF
```

Excel:

```excel
=SUMPRODUCT(SF_range, remaining_term_range)/SUM(SF_range)
```

WALT is the headline duration statistic. Longer means more income certainty and, usually, a
tighter cap rate.

Build a rollover exposure schedule alongside it — the percentage of GLA expiring each year:

| Year | SF expiring | % of GLA | Cumulative % |
|---|---|---|---|

**Read it for concentration, not just level.** More than ~30% of GLA in a single year is a
serious exposure: it concentrates TI/LC into one period, it can exceed a full year of NOI, and
if it lands in the exit year the next buyer will price that risk into their cap rate. Rollover
in the year *before* exit is materially worse than rollover in year one, because you fund the
cost and the buyer captures the stabilized income.

A single tenant above ~25% of income is credit concentration regardless of WALT — model that
tenant's departure as an explicit downside case.

---

## Mark-to-market

```
Mark-to-market = (market rent − in-place rent) / in-place rent
```

Positive means in-place rents are below market and rolling leases will lift income. Negative
means rents are above market and rollover will hurt.

Quantify it before relying on it:

- Compute the weighted average in-place rent across the rent roll
- Compare to a genuine market rent comp set, not the seller's stated market rent
- Apply it only as leases actually expire — that is the whole point of the schedule

**A value-add thesis built on mark-to-market lives or dies on lease expiration timing.** A 20%
gap that does not roll until year eight of a five-year hold is worth nothing to you; the next
buyer captures it. Show the mark-to-market gain year by year, not as one headline number.

---

## Common errors

| Error | What happens |
|---|---|
| Growing in-place fixed-bump leases at market rent growth | Double-counts escalation; overstates revenue every year, compounding |
| Omitting downtime | Overstates revenue and recoveries in every rollover year |
| Applying new-lease TI to renewals | Overstates capital cost — renewals reuse the buildout |
| Booking TI/LC in the expiry year instead of commencement | Shifts cash by a year; distorts IRR |
| Applying blanket market vacancy on top of a lease-level model | Double-counts vacancy — the schedule already models exposure |
| Ignoring free rent / concessions | Face rent overstates net effective rent, often by 5–15% |
| Renewal probability of 100% | Not an assumption, an omission |

The first and last are the ones that most often survive review, because both make the model
look *simpler* rather than more aggressive.
