# Where Every Number Comes From

A model is a chain of assumptions with arithmetic between them. The arithmetic is guaranteed by
the generator and verified by `verify_model.py`. The assumptions are the analysis — and an
unsourced assumption is the only kind that reliably causes losses, because a blank gets
questioned and a number gets trusted.

This is why every assumption in the workbook carries a **Source** column, and why anything
unsourced is highlighted amber rather than quietly filled in.

---

## The source hierarchy

When two sources disagree, the higher one wins unless there is a documented reason otherwise.

| Rank | Source | Examples |
|---|---|---|
| 1 | **Executed documents** | Leases, PSA, loan agreement, tax bills |
| 2 | **Audited / verified operating data** | Audited financials, trailing-12 with bank support |
| 3 | **Unaudited owner data** | Seller T-12, rent roll, budget |
| 4 | **Third-party market data** | CoStar, appraisal, broker comp set |
| 5 | **Broker / seller pro forma** | The OM's own projections |
| 6 | **Your own estimate** | A reasoned assumption you can defend |

**Rank 5 deserves specific scepticism.** An OM pro forma is a marketing document produced by
someone paid on the sale price. Treat every number in it as a claim to verify, not an input to
accept. The most common OM adjustments in the seller's favour: rents at face rather than net
effective, no replacement reserve, a below-market management fee, no vacancy on "credit"
tenants, taxes at the current rather than reassessed basis, and a stabilized occupancy the
asset has never achieved.

---

## Per-assumption sourcing

### Purchase price and costs

| Input | Source |
|---|---|
| Purchase price | LOI or PSA. Before that, seller guidance — label it as such |
| Acquisition costs | Title quote, transfer tax schedule, legal estimate. Typically 1–2% |
| Upfront capital | Property condition report, your business plan |

Acquisition costs are jurisdiction-specific — transfer taxes vary from near zero to several
percent. Look it up; do not assume.

### Revenue

| Input | Source |
|---|---|
| In-place rent | **Rent roll, tied to the leases.** Spot-check at least the top 5 tenants against actual lease documents |
| Market rent | Submarket comp set of recent *signed* leases, adjusted for concessions |
| Rent growth | Submarket forecast, or a defensible long-run assumption |
| Vacancy | Submarket vacancy plus a credit loss allowance, sanity-checked against the property's own history |
| Other income | T-12, broken out by category |

**Underwrite net effective rent, not face rent.** A lease at $30/SF with six months free on a
five-year term is $27/SF net effective. Comp sets quote face rent almost universally.

The rent roll must foot to the T-12 revenue line. If it does not, find out why before going
further — the gap is usually concessions, a tenant in default, or space that is leased but not
occupied.

### Expenses

| Input | Source |
|---|---|
| Line items | **T-12, normalized.** Then adjust for known changes |
| Real estate taxes | The assessor. Model the **post-sale reassessment**, not the current bill |
| Insurance | A current quote from your broker for your ownership structure |
| Management fee | Your actual management agreement or market rate — not the seller's affiliate rate |
| Replacement reserve | Property condition assessment |

Normalizing a T-12 means removing what will not recur: one-time legal costs, capital
misclassified as repair, an owner's above- or below-market affiliate contract.

**Real estate taxes are the most common large error in CRE underwriting.** In jurisdictions
that reassess on sale, taxes can jump 30–100% at close. The seller's T-12 shows the old basis
by definition. Check the local reassessment rule every time.

### Debt

Every debt input should come from an actual term sheet. Before you have one, use a lender
indication and label it. Do not carry a rate from memory or from another deal — pricing moves
weekly, and rate is the input the whole capital stack turns on.

### Exit

| Input | Source |
|---|---|
| Exit cap rate | Going-in cap + 25–50 bps, adjusted for the asset's condition at sale |
| Hold period | Your business plan and fund life |
| Disposition costs | Brokerage + transfer tax + legal, typically 1–2.5% |

**The exit cap is the most consequential assumption in the model and the least verifiable.**
Nobody knows cap rates five years out. That is exactly why it must be explicit and sensitised,
never buried. An exit cap tighter than the going-in cap is a bet on market compression: state
the thesis or change the number.

### Discount rate

The unlevered return you require for this risk. Anchor it to your own cost of capital and the
deal's risk profile — core assets carry lower required returns than opportunistic ones. Do not
reverse-engineer it from the answer you want.

---

## Documenting a source

Write it so a reviewer can find the same number without asking you.

**Good:**
- `CoStar submarket comps, 7/2026 — 6 leases signed 2025–26, $23.10–$26.40/SF NNN`
- `Lender term sheet, Regions Bank, 7/22/2026`
- `T-12 ending 6/30/2026, normalized to remove $84k non-recurring legal`
- `Tulsa County assessor, reassessment at sale price × 0.011 millage`

**Not good:** `market`, `standard`, `broker`, `assumption`, `per OM`.

The test: could someone else reproduce the number from your note alone?

---

## What to do when you have nothing

Never invent a figure that reads like a fact. Do exactly one of:

1. **Ask.** Usually the fastest path — the person has the document.
2. **Use a labelled placeholder** from `property-types.md`, mark it unsourced, and say so in
   your written response, not only in the spreadsheet.
3. **Model a range** and show the outcome across it, so the decision does not hinge on a number
   nobody has.

Then say plainly which assumptions are unsourced and which of them the answer is actually
sensitive to. Those are not the same list, and the second one is what matters.

---

## The pre-circulation check

Before a model leaves your hands:

- [ ] Every amber cell is either sourced or explicitly flagged in the accompanying note
- [ ] Rent roll foots to the T-12 revenue line
- [ ] Taxes reflect the post-sale basis
- [ ] Debt terms come from a real quote
- [ ] The exit cap has a stated rationale
- [ ] The three assumptions the answer is most sensitive to are named in the summary
- [ ] `verify_model.py` passes and `audit_model.py` shows no HIGH findings
