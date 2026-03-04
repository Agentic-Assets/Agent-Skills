# CRE Investment Analysis

Professional-grade commercial real estate investment analysis combining academic rigor with institutional underwriting standards.

## What This Skill Does

- **Property Analysis**: Multifamily, office, retail, industrial, mixed-use, land development
- **Financial Modeling**: DCF, IRR, NPV, cash-on-cash returns, equity multiples
- **Underwriting**: Institutional-grade assumptions, sensitivity analysis, scenario modeling
- **Business Plans**: Executive summaries, market analysis, financial projections, exit strategies
- **REIT Analysis**: FFO/AFFO metrics, same-store NOI growth, leverage ratios
- **Document Integration**: Works with PDF offering memos, Excel rent rolls, and more

## Installation

### Option 1: Download the `.skill` file (Easiest)

Download `cre-investment-analysis.skill` from this directory and place it in your skills folder:

```bash
# Claude Code
cp cre-investment-analysis.skill ~/.claude/skills/

# Or unzip for manual inspection
unzip cre-investment-analysis.skill -d ~/.claude/skills/cre-investment-analysis/
```

### Option 2: Copy the skill folder

```bash
cp -r skills/cre-investment-analysis ~/.claude/skills/
```

### Option 3: Clone the full repository

```bash
git clone https://github.com/Agentic-Assets/Agent-Skills.git
cp -r Agent-Skills/skills/cre-investment-analysis ~/.claude/skills/
```

## What's Included

```
cre-investment-analysis/
├── SKILL.md                          # Core skill (608 lines)
├── references/
│   ├── underwriting-standards.md     # Industry benchmarks and standards
│   ├── market-data-sources.md        # Data provider guidance (CoStar, REIS, etc.)
│   ├── reit-analysis-framework.md    # REIT-specific metrics and analysis
│   └── document-integration-workflows.md  # PDF/Excel/Word integration workflows
├── scripts/
│   ├── dcf_analysis.py               # Discounted cash flow calculations
│   └── sensitivity_analysis.py       # Scenario modeling utilities
└── assets/
    └── templates/                    # Excel pro forma templates
```

## Example Prompts

```
Analyze this multifamily acquisition: 200 units in Austin, TX at $35M.
Current NOI is $2.1M. Market cap rate is 5.5%. Assume 70% LTV at 6.25%.
Create a 10-year DCF with base, downside, and upside scenarios.
```

```
Create an investment committee memo for a Class B office building.
Purchase price $18M, 95,000 SF, 88% occupied, in-place NOI $1.2M.
Include market analysis, risk assessment, and return projections.
```

```
Perform a REIT analysis comparing Prologis (PLD), Realty Income (O),
and AvalonBay (AVB). Include FFO/AFFO, dividend safety, and NAV analysis.
```

## Platform Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | Full support | Copy to `~/.claude/skills/` |
| Claude.ai | Full support | Upload SKILL.md as project knowledge |
| Other LLM platforms | Partial | Use SKILL.md content as system prompt |

## Dependencies

For document processing (PDF, Excel, Word, PowerPoint), this skill works best with Claude's official document skills (`pdf`, `xlsx`, `docx`, `pptx`). See SKILL.md for details.
