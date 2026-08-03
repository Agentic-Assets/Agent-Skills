# Reviewing Somebody Else's Model

Most CRE models in circulation were built by someone with an incentive. This is the sequence
for taking one apart efficiently. Roughly 20 minutes gets you to a defensible view.

## Step 0 — Run the scanner

```bash
python3 audit_model.py their_model.xlsx
```

Mechanical defects first, because they are free to find and they change how much weight the
rest of the review deserves. HIGH findings — error cells, external links, percent-unit errors,
plugs — mean the model is broken as a calculator, before anyone argues about assumptions.

A clean scan means the **wiring** is sound. It says nothing about whether the assumptions are
honest. Everything below is the part software cannot do.

---

## Step 1 — Find the answer, then find what drives it

Locate the headline metrics (IRR, equity multiple, cap rate) and then trace *backwards* to the
three or four inputs that actually move them. On a typical five-year hold that is the exit cap
rate, rent growth, the expense load, and the debt terms.

Do not read the model front to back. Read it from the answer.

---

## Step 2 — The six questions that find most problems

**1. Is exit value computed on FORWARD NOI?**

Find the exit calculation. The cap rate should divide into the year *after* the final operating
year. Capping the final year understates the exit by about one year of growth — but the far
more common error is the reverse: a model that projects only `hold` years and caps the last one
while calling it forward. Check which year the formula actually points at.

**2. Is the exit cap ≥ the going-in cap?**

Compute the going-in cap yourself (Year 1 NOI ÷ price) and compare. Compression is the easiest
way to manufacture an IRR and the hardest to defend. It needs a stated thesis. Silence is the
answer to look for.

**3. Does DSCR hold in the first amortizing year?**

Find where IO ends and check coverage in the very next year. A model showing 1.8x DSCR
throughout an IO period may be at 1.15x the day amortization starts. This is what the lender
sizes to.

**4. Do the expenses tie to the T-12?**

Compare the Year-1 expense line to the trailing twelve months. Then ask specifically about:
real estate taxes (reassessment at sale), management fee (is it market or an affiliate rate),
and replacement reserve (is there one at all). Under-reserving is the second easiest way to
manufacture a return.

**5. Are in-place leases being grown at market rent growth?**

If the rent roll has contractual escalations and the model also applies a market growth rate to
those same leases, revenue is double-escalated and the error compounds every year.

**6. Does the rent roll foot to the revenue line?**

Sum the rent roll and compare to Year-1 GPR. A gap means concessions, a defaulting tenant,
leased-but-unoccupied space — or that the two were built independently and never reconciled.

---

## Step 3 — Check the return math itself

Three specific things, all of which are common:

- **Double-counted exit.** Does the year-*n* cash flow used for IRR include sale proceeds that
  are *also* added separately? Trace the IRR range and see exactly what is in the final cell.
- **Equity multiple built on the wrong base.** Operating cash flow plus net equity proceeds,
  over equity invested. If exit proceeds sit in both the operating row and the reversion, the
  multiple is inflated.
- **Equity that excludes closing costs.** Equity = total basis − loan, where basis includes
  acquisition costs and upfront capital. Omitting them understates equity and overstates every
  equity-based return.

---

## Step 4 — Stress it yourself

Do not trust the model's own sensitivity tables — rebuild the two that matter:

| Change | Watch |
|---|---|
| Exit cap +50 bps | IRR. Usually the largest single driver |
| Rent growth −100 bps | IRR and DSCR |
| Interest rate +100 bps | DSCR, and whether the loan still sizes |
| Vacancy +300 bps | NOI, DSCR, debt yield |

If a plausible downside breaks the covenant, that is the finding — not the base-case IRR.

---

## Step 5 — Reconstruct it

For any deal that matters, rebuild it independently from source documents:

```bash
python3 build_model.py your_assumptions.json check.xlsx
python3 verify_model.py your_assumptions.json check.xlsx
```

Then compare, and investigate every material difference. This is the only review that finds
errors nobody thought to look for, and it takes less time than reading a complex model
carefully.

---

## Red flags, ranked

**Serious:**
- Exit cap tighter than going-in with no stated thesis
- No replacement reserve, TI, or LC anywhere in the model
- Taxes at the seller's current basis in a reassessment jurisdiction
- DSCR measured only during IO
- Hardcoded numbers inside otherwise calculated rows
- Links to files you do not have

**Worth a question:**
- Rent growth above ~3% without submarket evidence
- Stabilized occupancy the asset has never achieved
- Management fee below market or paid to an affiliate
- Single tenant above 25% of income with no downside case
- Rollover concentrated in the exit year
- Face rents with no concession adjustment

**Presentation tells:**
- No assumptions tab — inputs scattered through the calculations
- No sources cited for anything
- IRR quoted without equity multiple, or either without DSCR
- Sensitivity tables whose ranges are too narrow to break the deal

---

## Writing it up

Lead with the decision, not the tour:

> The deal underwrites to a 6.5% unlevered IRR on my numbers versus the 9.2% in the OM. The gap
> is three items: taxes are modelled at the current basis and will reassess at roughly $180k
> higher, there is no replacement reserve, and the exit cap is 40 bps tighter than going-in
> without a stated rationale. Correcting those three takes it to 6.5%. Coverage is the binding
> constraint — DSCR falls to 1.18x in the first amortizing year against a 1.25x covenant, so
> the quoted proceeds do not size.

Name the specific corrections and their individual impact. "The model is aggressive" is not a
finding; "taxes reassess at +$180k and that alone is 70 bps of IRR" is.
