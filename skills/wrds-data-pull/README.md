# WRDS Data Pull

Automated WRDS data extraction with pre-built query templates, merge logic, validation, and variable documentation for finance and real estate research.

## What This Skill Does

- Provides parameterized SQL query templates for major WRDS databases (Compustat, CRSP, IBES, Thomson Reuters, CoreLogic, NCREIF, and more)
- Merges financial datasets using CCM linking tables or CUSIP-based matching with date-range validation
- Validates panel structure by checking balance, duplicates, coverage, and known data issues
- Constructs standard financial variables (Tobin's Q, leverage, ROA, etc.) with academic citations
- Generates coverage reports with LaTeX output suitable for research papers
- Handles known data quirks including restated data, delisting returns, negative book equity, and CUSIP mismatches

## Installation

### Option 1: Install via .skill file

Add the following to your project's `.skill` file:

```yaml
skills:
  - name: wrds-data-pull
    source: github:jeffallan/claude-skills/skills/wrds-data-pull
```

### Option 2: Copy the folder directly

Copy the `wrds-data-pull/` folder into your project's skills directory:

```bash
cp -r wrds-data-pull/ your-project/.skills/wrds-data-pull/
```

Then install the Python dependencies for the bundled package:

```bash
pip install wrds pandas numpy scipy
```

## What's Included

```
wrds-data-pull/
├── SKILL.md
├── README.md
├── assets/
│   ├── requirements.txt
│   ├── setup.py
│   ├── examples/
│   │   └── quickstart.py
│   └── wrds_data_pull/
│       ├── __init__.py
│       ├── config.py
│       ├── crsp_utils.py
│       ├── merge_utils.py
│       ├── orchestrator.py
│       ├── panel_diagnostics.py
│       ├── query_templates.py
│       └── variable_builders.py
├── references/
│   ├── INDEX.md
│   ├── alternative-data.md
│   ├── compustat-crsp.md
│   ├── known-data-issues.md
│   ├── merge-keys.md
│   ├── real-estate-databases.md
│   ├── variable-construction.md
│   └── wrds-databases.md
└── scripts/
    ├── coverage_report.py
    ├── setup_wrds.py
    └── validate_panel.py
```

## Example Prompts

1. **"Pull quarterly Compustat and CRSP data from 2015-2023, merge them using CUSIP-based linking, and validate the panel for duplicates and missing coverage."**

2. **"Build a real estate research panel using NCREIF property-level returns for office and retail properties, then construct standard return metrics and generate a LaTeX coverage table."**

## Platform Compatibility

| Platform       | Supported |
|----------------|-----------|
| Claude Code    | Yes       |
| Cursor         | Yes       |
| Windsurf       | Yes       |
| Cline          | Yes       |
| Custom Agents  | Yes       |

## Related Skills

- **python-expert** - General Python development patterns and best practices
- **data-pipeline** - Broader data pipeline design and orchestration patterns
- **research-methodology** - Academic research workflow and reproducibility standards
