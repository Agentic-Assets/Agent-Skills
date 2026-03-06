# PyFixest LaTeX Generator

Generate publication-quality LaTeX tables and figures from PyFixest econometric models for academic research papers.

## What This Skill Does

- Converts PyFixest regression models into formatted LaTeX tables ready for journal submission
- Creates event study (dynamic effects) plots with configurable styles (errorbar, filled, step)
- Generates summary statistics tables from pandas DataFrames with customizable variable labels
- Produces robustness check tables with grouped model specifications
- Creates treatment assignment heatmaps and coefficient comparison forest plots
- Handles proper small-sample inference (t-distribution for n<30, normal for n>=30)

## Installation

### Option 1: .skill file

Add the following to your project's `.skill` file:

```
pyfixest-latex
```

### Option 2: Copy folder

Copy the `skills/pyfixest-latex/` folder into your project's skills directory, then copy `assets/pyfixest_latex/` into your project root and install dependencies:

```bash
pip install pyfixest pandas numpy scipy matplotlib
```

## What's Included

```
skills/pyfixest-latex/
├── SKILL.md
├── README.md
├── assets/
│   ├── pyfixest_latex/
│   │   ├── __init__.py
│   │   ├── academic_figure_generator.py
│   │   └── academic_table_generator.py
│   ├── example_did_analysis_template.py
│   ├── 1---example_summary_statistics.py
│   ├── 2---example_figure_usage.py
│   ├── 3---example_enhanced_table_generator.py
│   └── 4---run_all_examples.py
├── references/
│   ├── common-patterns.md
│   ├── data-requirements.md
│   ├── did-template-guide.md
│   ├── did-template-quick-reference.md
│   ├── figures-api.md
│   ├── stargazer-alternative.md
│   ├── tables-api.md
│   ├── troubleshooting.md
│   └── workflow-patterns.md
└── scripts/
    └── setup_module.py
```

## Example Prompts

- "I have a difference-in-differences model fitted with PyFixest. Generate a LaTeX regression table comparing specifications with and without controls, and create an event study plot showing dynamic treatment effects."
- "Create a summary statistics table in LaTeX for my panel dataset, then produce a robustness table grouping my baseline, extended, and placebo specifications."

## Platform Compatibility

| Platform | Supported |
|----------|-----------|
| Claude Code CLI | Yes |
| Claude Desktop | Yes |
| Cursor | Yes |
| Windsurf | Yes |

## Related Skills

This skill is specialized for PyFixest-based econometric workflows. For general statsmodels regression tables, see the stargazer alternative documentation in `references/stargazer-alternative.md`.
