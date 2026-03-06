# Academic Writing

Use when creating or revising academic paper sections, formatting tables/figures for journal submission, writing referee responses, or adapting papers to journal-specific requirements in finance, economics, and real estate research.

## What This Skill Does

- **Section-by-Section Manuscript Drafting**: Write publication-ready LaTeX sections (Introduction, Methodology, Results, Discussion) using structured templates and academic writing conventions
- **Referee Response Preparation**: Draft point-by-point responses to reviewer comments with professional tone, covering common objections like endogeneity, sample selection, and alternative explanations
- **Journal-Specific Formatting**: Adapt manuscripts to requirements for JF, JFE, RFS, JFQA, Real Estate Economics, and other journals
- **Econometric Reporting**: Interpret and present regression results with proper coefficient discussion, significance reporting, and economic magnitude translation
- **Consistency Checking**: Validate cross-references, citation keys, hypothesis-result mapping, and notation consistency across the manuscript
- **Citation Validation**: Verify BibTeX entries against OpenAlex and check that all cited works appear in the bibliography

## Installation

### Option 1: Download the `.skill` file (Easiest)

Download `academic-writing.skill` from this directory and place it in your skills folder:

```bash
cp academic-writing.skill ~/.claude/skills/
```

### Option 2: Copy the skill folder

```bash
cp -r skills/academic-writing ~/.claude/skills/
```

## What's Included

```
academic-writing/
├── SKILL.md                                    # Core skill definition
├── references/
│   ├── paper-structure.md                      # Section-by-section templates with annotated examples
│   ├── introduction-patterns.md                # Framing patterns (motivation, gap, contribution)
│   ├── hypothesis-development.md               # Theory to testable prediction scaffolding
│   ├── results-discussion.md                   # Table walkthrough patterns, magnitude interpretation
│   ├── writing-conventions.md                  # Academic tone, voice, hedging guidance
│   ├── referee-responses.md                    # Common objections, response frameworks, tone
│   ├── common-mistakes.md                      # Frequent writing issues and fixes
│   ├── journal-formats.md                      # JF, JFE, RFS, Real Estate Economics formatting
│   ├── econometric-reporting.md                # Coefficient interpretation, significance, fixed effects
│   └── econometric-analysis-integration.md     # Workflow linking data pull, analysis, and writing
├── assets/
│   ├── templates/
│   │   ├── Main.tex                            # Full LaTeX preamble and document structure
│   │   ├── Results.tex                         # Results section with table formatting templates
│   │   ├── Figures.tex                         # Figure formatting and layout examples
│   │   ├── Appendix.tex                        # Online appendix structure
│   │   ├── Internet_Results.tex                # Internet appendix tables
│   │   ├── Data_Documentation.tex              # Data sources and methodology documentation
│   │   └── referee_response.tex                # Point-by-point referee response letter
│   └── bibtex/
│       └── jfe.bst                             # Journal of Financial Economics bibliography style
├── scripts/
│   ├── 01-check_citations.py                   # Citation key validator
│   ├── 02-bibtex_validator.py                  # BibTeX validation via OpenAlex API
│   ├── check_consistency.py                    # Cross-reference and notation consistency checker
│   └── latex_section_word_counter.py           # Section-by-section word counter
└── requirements.txt                            # Python dependencies
```

## Example Prompts

```
Write the Results section describing Table 2 (main regression results with firm fixed effects).
```

```
Reviewer 2 says our treatment variable is endogenous. Draft a response addressing this concern.
```

```
Format my manuscript for submission to the Journal of Financial Economics.
```

```
Check my paper for consistency issues before submission — cross-references, citations, and hypothesis numbering.
```

```
Write the Introduction section. Our paper studies how climate risk affects commercial real estate prices.
```

## Platform Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | Full support | Copy to `~/.claude/skills/` |
| Claude.ai | Full support | Upload SKILL.md as project knowledge |
| Other LLM platforms | Full | Use SKILL.md content as system prompt |

## Related Skills

- **wrds-data-pull** - Pull and merge financial datasets from WRDS (Compustat, CRSP) used as inputs for empirical analysis
- **pyfixest-latex** - Run regressions with PyFixest and generate publication-ready LaTeX tables that integrate directly into manuscripts
- **stata-accounting-research** - Stata-based econometric analysis as an alternative analysis pipeline before writing up results
