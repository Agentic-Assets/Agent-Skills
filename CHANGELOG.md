# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.3] - 2026-08-03

### Added
- **cre-excel-underwriting** — CRE underwriting in Excel: build, verify, and audit. Ships `build_model.py` (9-tab workbook generator), `verify_model.py` (recalculates the workbook in LibreOffice and compares every material cell against an independent Python engine), `audit_model.py` (structural defect scan that runs against **any** workbook, not just generated ones), 7 reference files, and 4 worked examples (office NNN, multifamily unit-mix, industrial all-cash, retail rent-roll). Covers office, industrial, retail, multifamily, hospitality, self-storage, and mixed-use.
- **context-guidance-audit** — Two-phase, multi-subagent audit and remediation playbook for codebase guidance (CLAUDE.md, AGENTS.md, docs, skills/agents references). Phase 1 is read-only reports; Phase 2 verifies and fixes guidance. Includes `automation-prompt.md`, scope-split reference, and `commands/context-guidance-audit.md`.
- **Skill Packaging** section in CLAUDE.md and AGENTS.md documenting the two-format requirement (`skills/<name>/` plus `skills/<name>.skill`) and the re-zip command.

### Changed
- Documented every skill actually present in the repo. README.md, SKILLS_GUIDE.md, and QUICKSTART.md previously listed 18 of them; **cre-dcf-valuation**, **cre-excel-dcf-modeler**, **goal-writer**, **skill-creator**, and **social-media-content** were installed but undocumented.
- Added a Real Estate disambiguation table to SKILLS_GUIDE.md — the four CRE skills overlap by design, so routing is now by output produced rather than by topic.
- Added an **Authoring & Productivity** category (skill-creator, goal-writer, social-media-content).

### Fixed
- `cre-excel-underwriting/scripts/verify_model.py` wrote its recalculation macro to the Linux LibreOffice profile path on every platform. On macOS and Windows the macro was never found, so the recalculation silently did not run and verification reported "no calculated values" instead of proving the formulas. The profile path is now resolved per platform.

### Stats
- **24 skills** across 8 domains
- **106 reference files**
- **9 workflow commands**

## [0.4.2] - 2026-03-02

### Changed
- **Customized from jeffallan/claude-skills template** for personal use focused on PhD research, finance, real estate, and AI/ML
- 17 specialized skills across 6 domains:
  - **📚 PhD Academic Business Research**: academic-writing, pyfixest-latex, stata-accounting-research, pandas-pro
  - **💰 Financial Analysis & Services**: wrds-data-pull, pandas-pro
  - **🏢 Real Estate**: cre-investment-analysis
  - **🤖 AI/ML/AI Agents**: ml-pipeline, prompt-engineer, mcp-developer
  - **💻 Development & Technical Writing**: fastapi-expert, code-documenter, code-reviewer, debugging-wizard, n8n-skills
  - **📊 Data Visualization**: matplotlib, scientific-visualization
  - **🧠 Context Engineering**: context-engineering
- Reorganized all documentation around domain-specific categories
- Updated all docs to accurately reflect current skill set (was missing academic-writing, context-engineering, matplotlib, scientific-visualization)
- Fixed plugin.json and marketplace.json (were still referencing template "fullstack-dev-skills" content)
- Fixed CONTRIBUTING.md (was referencing wrong project name and repo URL)
- Removed stale n8n-skills.zip file

### Fixed
- Added missing `triggers` field to skill frontmatter
- Fixed skill frontmatter descriptions to follow "Use when" trigger-only format
- Added missing `role`, `scope`, and `output-format` fields
- Updated version.json and all documentation with correct counts (17 skills, 89 references)

### Stats
- **17 skills** across 6 domains
- **89 reference files**
- **9 workflow commands**

### Attribution & Community Skills
- **stata-accounting-research** from [@jusi-aalto](https://github.com/jusi-aalto/stata-accounting-research)
- **n8n-skills** from [@haunchen](https://github.com/haunchen/n8n-skills)
- **matplotlib** + **scientific-visualization** from [K-Dense Inc.](https://github.com/K-Dense-AI/claude-scientific-skills)

---

## Original Template History

This repository was forked from [jeffallan/claude-skills](https://github.com/jeffallan/claude-skills) v0.4.2.

See the original repository for full version history prior to customization.

---

*Customized for personal use by Dr. Cayman Seagraves*
