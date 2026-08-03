---
name: cre-excel-underwriting
description: >-
  Use when underwriting, valuing, or stress-testing a commercial real estate deal in Excel —
  NOI pro formas, DCF cash flows, rent rolls, unit mixes, debt schedules, waterfalls, IRR /
  equity multiple / DSCR / debt yield / cap rate math, and sensitivity tables. Also use when
  reviewing a model somebody else built, working from an OM, broker package, rent roll, or
  T-12, or explaining how a CRE metric or Excel formula works. Covers office, industrial,
  retail, multifamily, hospitality, self-storage, and mixed-use. Triggers even when the request
  never says "DCF" or "Excel" — "run the numbers on this deal", "can you check this
  spreadsheet". Prefer over generic spreadsheet or corporate-DCF help for anything
  property-related.
triggers:
  - CRE underwriting
  - underwrite a property
  - pro forma
  - acquisition model
  - rent roll
  - unit mix
  - T-12
  - offering memorandum
  - NOI
  - cap rate
  - IRR
  - equity multiple
  - DSCR
  - debt yield
  - debt schedule
  - waterfall
  - sensitivity table
  - audit this model
  - check this spreadsheet
role: expert
scope: implementation
output-format: report
---

# CRE Underwriting in Excel

Commercial real estate underwriting is not corporate finance with different labels. It is
NOI-based, the terminal value comes from a cap rate rather than a growth perpetuity, returns
are measured as IRR and equity multiple rather than per-share value, and debt is modeled
explicitly because the covenants bind the deal. Applying a corporate DCF template to a
building produces answers that look reasonable and are wrong.

This skill does three jobs. Read the section that matches the ask.

| The ask | Go to |
|---|---|
| "Underwrite this deal" / "build me a model" | **Building a model** |
| "Check this model" / "does this pro forma hold up" | **Auditing a model** |
| "How does X work" / "why is my IRR wrong" | **Explaining the mechanics** |

---

## The one rule that matters most

**Never invent an assumption and never let one pass undocumented.**

A CRE model is a chain of assumptions with arithmetic between them. The arithmetic is easy and
this skill guarantees it. The assumptions are the entire analysis, and a plausible-looking
number you supplied from nowhere is worse than a blank, because a blank gets questioned and a
number gets trusted.

When you do not have a figure, do exactly one of these:

1. **Ask.** Most of the time the person has the OM, the T-12, or the term sheet.
2. **Use a labelled placeholder** from `references/property-types.md`, and say plainly in your
   response that it is a placeholder that must be replaced before the number is used for
   anything real.

Every assumption in the generated workbook has a **Source** column. Any assumption without a
source is highlighted amber and reads `⚠ UNSOURCED`. Leave those visible rather than filling
them with something invented — the highlight is the feature.

Do not state current market cap rates, rents, or lending terms from memory. They move
constantly and being confidently stale is the failure mode that destroys trust in the whole
model.

---

## Building a model

### 1. Gather inputs

Work from the source documents, not from a summary of them. The minimum set:

- **Property** — type, rentable SF (or unit count), year built, current occupancy
- **Price** — purchase price, acquisition costs (typically 1–2% of price), any upfront capital
- **Revenue** — rent roll or unit mix if available, otherwise market rent and occupancy;
  other income; expense recovery structure (gross / modified gross / NN / NNN)
- **Expenses** — T-12 or budget line items if available, otherwise an OpEx ratio; management
  fee; replacement reserve; TI/LC at rollover
- **Debt** — loan sizing basis (LTV, fixed amount, or DSCR-sized), rate, IO period,
  amortization term, DSCR and debt-yield covenants
- **Exit** — hold period, exit cap rate, disposition costs
- **Returns** — unlevered discount rate

`assets/assumptions-template.json` is a fully annotated skeleton. Four worked examples sit
beside it — office NNN, multifamily unit-mix, industrial all-cash, retail rent-roll — and each
one is a working starting point for a real deal.

### 2. Write the assumptions file

Copy the template, fill it in, and keep two conventions straight because they cause the most
expensive errors in the entire discipline:

- **Every rate is a decimal fraction.** 6.5% is `0.065`. Never `6.5`. The builder refuses to
  run on a rate above 1.0 rather than producing a model that is silently wrong by 100x.
- **Recoveries require line-item expenses.** An OpEx *ratio* is a percentage of EGI, and
  recoveries feed EGI, so combining them is circular. Use `"mode": "line_items"` with
  `recoverable: true` flags for NNN, NN, and modified-gross deals. Use `"mode": "ratio"` for
  gross-lease and multifamily deals, where recoveries are zero anyway.

### 3. Build, verify, audit

```bash
cd scripts
python3 build_model.py  assumptions.json  model.xlsx    # writes the workbook
python3 verify_model.py assumptions.json  model.xlsx    # proves the formulas are right
python3 audit_model.py  model.xlsx                      # structural defect scan
```

`verify_model.py` is the step that separates this from a template. It recalculates the
workbook with LibreOffice and compares every material cell — EGI, NOI, CFBDS, debt service,
loan balance, CFADS, forward NOI, exit value, equity proceeds, both IRRs, equity multiple,
cash-on-cash, DCF value, minimum DSCR — against `cre_engine.py`, an independent Python
implementation of the same documented math. Agreement across two implementations is real
evidence. "The spreadsheet looks right" is not.

Run it every time, and always after hand-editing a formula. If it reports mismatches, the
workbook is wrong — fix it before showing anyone.

> Verification needs LibreOffice **with Calc**: `apt-get install libreoffice-calc`, or
> `brew install --cask libreoffice`. `libreoffice-core` alone cannot open .xlsx and the
> script will tell you so rather than silently passing.

### 4. Report the result

Lead with what the deal returns and what would break it, not with a description of the
workbook. Something like:

> 7.05% going-in cap, 6.5% unlevered IRR, 1.41x equity multiple over a 6-year hold, minimum
> DSCR 1.42x against a 1.35x covenant. The return is carried by the exit — at a flat exit cap
> the IRR is 8.2%, and every 25 bps of cap expansion costs about 90 bps of IRR. Three
> assumptions are unsourced and marked amber: market rent, TI/SF, and the disposition cost.

Then state the unsourced assumptions explicitly. Do not bury them.

---

## Auditing a model

This is the higher-leverage use, because most CRE models in circulation were built by someone
with an incentive. `audit_model.py` works on **any** workbook, not just generated ones.

```bash
python3 audit_model.py their_model.xlsx          # readable report
python3 audit_model.py their_model.xlsx --json   # machine-readable
```

It finds, ranked HIGH / MEDIUM / LOW:

| Finding | Why it matters |
|---|---|
| **Formula errors** | `#REF!` and friends propagate into every dependent total |
| **External links** | Values come from a file you do not have — what you see is stale cache |
| **Percent-unit errors** | A cap rate stored as `7.25` instead of `0.0725` computes cleanly and is wrong by 100x |
| **Plugs** | A typed number sitting inside an otherwise calculated row — someone overwrote a formula to force a tie |
| **Hardcoded rates** | `=C4*1.03` hides a growth assumption inside a formula where review will never find it |
| **Static sheets** | A tab with no formulas is a paste of someone else's output |

A clean audit means the **wiring** is sound. It says nothing about whether the assumptions are
honest. After the mechanical scan, always check the judgment layer by hand:

1. **Is the exit cap ≥ the going-in cap?** Compression is the easiest way to manufacture an
   IRR. It needs a stated thesis, not silence.
2. **Is exit value computed on forward NOI?** Capping the final operating year instead of the
   year after overstates value by roughly one year of growth.
3. **Does the T-12 support the expense line?** Under-reserving OpEx and CapEx is the second
   easiest way to manufacture a return.
4. **Does DSCR hold in the first amortizing year**, not just during IO?
5. **Are in-place fixed-bump leases also being grown at market rent growth?** That double-counts.
6. **Does the rent roll actually foot to the revenue line?**

`references/audit-playbook.md` has the full review sequence.

---

## Explaining the mechanics

When the ask is conceptual — "why is my levered IRR below my unlevered IRR", "what is debt
yield actually for", "how do I build this in Excel myself" — teach it, don't just answer.
These references are written to be read aloud in a room:

| File | Use it for |
|---|---|
| `references/metric-definitions.md` | Every metric: plain-language definition, exact Excel formula, and the specific trap |
| `references/excel-construction.md` | Building the workbook by hand — layout, named ranges, formula patterns, data tables, formatting discipline |
| `references/property-types.md` | What changes by asset class, plus sanity-check ranges |
| `references/debt-and-equity.md` | Loan sizing, amortization, IO, covenants, refinance, LP/GP waterfalls and promote |
| `references/rent-roll-modeling.md` | Lease-level projection, WALT, rollover, downtime, mark-to-market |
| `references/assumption-sourcing.md` | Where each number legitimately comes from and how to document it |
| `references/audit-playbook.md` | The review sequence for someone else's model |

A useful teaching move: build the model, then deliberately break one assumption and show what
moves. The Sensitivity tab exists for exactly this.

---

## Conventions this skill holds to

These are the choices where practitioners differ and silence causes errors. The generated
workbook states each one on its README tab so the reader never has to guess.

- **NOI is before** capital reserve, TI, LC, and debt service. Capital costs sit below NOI.
- **Exit value uses forward NOI** — the year *after* the sale year. The pro forma therefore
  projects one extra year, and that year is excluded from every return calculation.
- **Debt yield is reported on the original loan amount.** That is the lender's covenant. A
  current-balance row is shown separately and labelled surveillance-only, because a balance
  that amortizes down makes debt yield improve on its own.
- **Vacancy and credit loss apply to Potential Gross Income.**
- **The OpEx ratio anchors to Year-1 EGI and then inflates at expense growth.** Re-applying the
  ratio to each year's EGI would force expenses to grow at the revenue rate and erase exactly
  the margin change the model exists to show.
- **In-place leases grow at their own contractual bump**, not at market rent growth. Market
  growth applies to vacant space and at renewal.
- **Equity multiple** = operating cash flow (excluding the exit) + net equity proceeds, over
  equity invested. The workbook separates operating and reversion rows specifically so the
  double-count is impossible to make and easy to see.
- **DSCR must be tested in the first amortizing year.** IO-period coverage flatters the deal
  and is not what the lender sizes to.

If a deal genuinely calls for a different convention, change it deliberately, say so, and note
it on the README tab. What is not acceptable is an undeclared convention.

---

## What this skill will not do

Be direct about these rather than producing something that looks authoritative and is not:

- It is not an appraisal. It does not replace an MAI valuation or a lender's own credit work.
- It does not model income tax, depreciation, cost recovery, or after-tax IRR. Everything is
  pre-tax.
- It does not model construction draws or development-period interest. It underwrites
  stabilized and value-add acquisitions, not ground-up development.
- The generated rent roll grows leases at their contractual escalation but does **not**
  automatically model lease expiry, downtime, and mark-to-market. When rollover drives the
  deal, extend it by hand using `references/rent-roll-modeling.md`.
- It has no live market data. Every cap rate, rent, and lending term must come from the user
  or from a source you can cite.
