# Property Types — What Changes, and Sanity Ranges

## How to use the numbers in this file

**These are order-of-magnitude sanity ranges, not comps and not market data.** Their job is to
catch an input error — a rent that is 10x off, an expense ratio that is structurally
impossible — before it reaches a model. They are not a substitute for a submarket comp set, a
T-12, or a lender quote, and they are not current as of any particular date.

Cap rates, rents, and lending terms move continuously and vary enormously by submarket,
vintage, tenancy, and quality tier. **Never populate a model from this file and present the
result as an underwriting.** If a real number is unavailable, use a range value, mark it
unsourced, and say so explicitly.

---

## What actually differs by asset class

The cash-flow engine is identical across types. Four things change:

1. **Revenue unit** — $/SF/year for commercial, $/unit/month for residential, RevPAR for hotels
2. **Lease structure** — determines whether recoveries exist at all
3. **Rollover cost** — TI and LC for commercial; unit turn cost for multifamily; none for hotels
4. **Operating leverage** — how much of EGI the landlord actually bears

---

## Multifamily

**Structure:** gross leases, no recoveries, no TI/LC. Turnover cost replaces rollover cost.
Leases are annual, so the whole rent roll marks to market every year — the shortest duration
and the fastest inflation pass-through of any asset class.

| Parameter | Typical range |
|---|---|
| Vacancy + credit loss | 5–12% |
| OpEx ratio (% of EGI) | 35–48% |
| Management fee | 3–5% of EGI |
| Replacement reserve | $200–500 / unit / yr |
| Turnover rate | 35–55% / yr |
| Unit turn cost | $1,500–6,000 |

Model it with `"mode": "unit_mix"` and per-type unit counts and rents. Other income is material
— 8–15% of EGI from parking, pets, laundry, and fees — and is frequently understated in a
seller's pro forma.

**Watch:** real estate taxes reassessing at the purchase price post-close. In many
jurisdictions this is the single largest expense change after acquisition, and the seller's
T-12 will never show it.

---

## Office

**Structure:** the most complex. Lease type drives everything. Full-service gross means the
landlord bears all operating cost; NNN means the tenant reimburses. TI and LC are large and
lumpy, and they are the reason office models live or die on the rent roll rather than on the
income statement.

| Parameter | Typical range |
|---|---|
| Vacancy (market) | 12–30%+ |
| OpEx ratio | 30–50% of EGI |
| Replacement reserve | $0.40–1.50 / SF / yr |
| TI — new lease | $30–100 / SF |
| TI — renewal | $10–40 / SF |
| LC — new / renewal | 4–6% / 2–3% of total lease value |

Always model office with a real rent roll. Rollover concentration is the risk that matters:
more than ~30% of GLA expiring in one year is a serious exposure, and the TI/LC to re-tenant it
can exceed a full year of NOI.

**Watch:** office has bifurcated sharply by quality tier. A single sector cap rate applied
across Class A and Class B/C is meaningless. Free rent and concession packages are also
frequently excluded from headline quoted rents — underwrite net effective rent, not face rent.

---

## Industrial / logistics

**Structure:** usually NNN, so the landlord's net expense load is small. Simple to model,
small rollover cost, long leases.

| Parameter | Typical range |
|---|---|
| Vacancy | 3–10% |
| OpEx ratio (landlord net) | 5–15% of EGI |
| Replacement reserve | $0.10–0.30 / SF / yr |
| TI — new / renewal | $5–20 / $2–8 per SF |
| Lease term | 5–10+ years |

**Watch:** clear height, truck court depth, and power capacity determine whether the building
competes for modern logistics tenants at all. A functionally obsolete box carries a much wider
cap rate than the sector average regardless of current occupancy. Mark-to-market on legacy
leases can be large in either direction.

---

## Retail

**Structure:** NNN with CAM reconciliation. Anchor versus inline is the key distinction —
anchors carry long leases at low rents, inline carries short leases at high rents and most of
the rollover risk. Percentage rent may apply above a sales breakpoint.

| Parameter | Typical range |
|---|---|
| Vacancy | 5–12% |
| OpEx ratio (landlord net) | 10–25% of EGI |
| Replacement reserve | $0.15–0.40 / SF / yr |
| TI — new / renewal | $20–60 / $5–15 per SF |

**Watch:** co-tenancy clauses. If an anchor goes dark, inline tenants may have contractual
rights to reduced rent or termination — a single anchor departure can cascade through the rent
roll in a way no expense assumption captures. Read the leases; grocery-anchored and
discretionary retail behave very differently.

---

## Hospitality

**Structure:** genuinely different. Not a lease-based asset — it is an operating business.
Revenue is RevPAR (ADR × occupancy) × rooms × 365. Expense ratios are far higher, and NOI is
after a franchise fee, a management fee, and an FF&E reserve.

| Parameter | Typical range |
|---|---|
| Operating expense ratio | 60–75% of revenue |
| FF&E reserve | 4–5% of total revenue |
| Franchise fee | 4–8% of room revenue |
| Management fee | 2–4% of total revenue |

**This skill's generator does not model hotels properly.** Its revenue build has no
ADR/occupancy/RevPAR structure and no departmental expense split. Use the DCF, debt, and return
mechanics — they are unchanged — but build the revenue and expense layer separately, or use a
purpose-built hotel model. Say so rather than forcing a hotel into the SF-based template.

---

## Self-storage

**Structure:** month-to-month leases, so effectively continuous mark-to-market. Very low
operating cost, minimal rollover cost, high management intensity.

| Parameter | Typical range |
|---|---|
| Physical vacancy | 8–15% |
| OpEx ratio | 25–38% of EGI |
| Management fee | 5–6% of EGI |
| Replacement reserve | $0.15–0.30 / SF / yr |

Model with `"mode": "unit_mix"` treating unit sizes as types. **Watch:** street rate versus
in-place rate can diverge sharply, and new supply within a 3-mile radius is the dominant risk.

---

## Mixed-use

Model each component **separately** with its own revenue structure, expense load, and cap rate,
then aggregate. Applying one blended cap rate to a combined NOI is a well-known way to
mis-value the whole asset — retail podium income and residential income are not worth the same
multiple, and the market prices them independently.

---

## Choosing the expense mode

| Asset / lease structure | Mode | Recoveries |
|---|---|---|
| Multifamily, self-storage | `ratio` | None |
| Full-service gross office | `ratio` | None |
| Modified gross office | `line_items` | Partial |
| NNN office, industrial, retail | `line_items` | Yes |

The builder enforces this: recoveries with an OpEx ratio is a circular definition and is
rejected rather than silently computed. See `excel-construction.md` for why.
