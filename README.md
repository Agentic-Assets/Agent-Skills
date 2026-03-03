<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,25,27&height=200&section=header&text=Agent%20Skills&fontSize=80&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=17%20Skills%20%E2%80%A2%209%20Workflows%20%E2%80%A2%20Personal%20Skill%20Collection&descSize=20&descAlignY=55" width="100%"/>
</p>

<p align="center">
  <a href="https://github.com/cas3526/Agent-Skills"><img src="https://img.shields.io/badge/version-0.4.2-blue.svg?style=for-the-badge" alt="Version"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge" alt="License"/></a>
  <a href="https://github.com/cas3526/Agent-Skills"><img src="https://img.shields.io/badge/Claude_Code-Skills-purple.svg?style=for-the-badge" alt="Claude Code"/></a>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=A855F7&center=true&vCenter=true&multiline=true&repeat=false&width=800&height=80&lines=Specialized+skills+for+PhD+research,+finance,+real+estate,;data+visualization,+automation,+and+AI+integration" alt="Typing SVG" />
</p>

<p align="center">
  <strong>🎯 <!-- SKILL_COUNT -->17<!-- /SKILL_COUNT --> Skills</strong> • <strong>🚀 <!-- WORKFLOW_COUNT -->9<!-- /WORKFLOW_COUNT --> Workflows</strong> • <strong>🧠 Context Engineering</strong> • <strong>📖 Progressive Disclosure</strong>
</p>

---

## Overview

This is a personal collection of specialized Claude Code skills organized around PhD research, finance, real estate, and AI/ML development:

- **📚 PhD Academic Business Research**: Econometric analysis (PyFixest, STATA), data manipulation, publication-ready output
- **💰 Financial Analysis & Services**: WRDS data extraction, financial data analysis, portfolio analytics
- **🏢 Real Estate (Residential/Commercial)**: Investment analysis, DCF/IRR modeling, institutional underwriting
- **🤖 AI/ML/AI Agents**: ML pipelines, prompt engineering, AI tool integration via MCP
- **💻 Development & Technical Writing**: FastAPI APIs, code quality, documentation, automation

---

## Quick Start

### Installation

```bash
# Copy skills to Claude Code directory
cp -r ./skills/* ~/.claude/skills/
```

### Usage

Skills activate automatically based on your requests:

```bash
# Python API Development
"Build a FastAPI endpoint with async SQLAlchemy"
→ Activates: fastapi-expert

# Data Analysis
"Clean this DataFrame and create summary statistics"
→ Activates: pandas-pro

# Research
"Generate LaTeX tables from PyFixest models"
→ Activates: pyfixest-latex

# Debugging
"Help me debug this stack trace"
→ Activates: debugging-wizard

# Context Engineering
"Audit my CLAUDE.md and agent context setup"
→ Activates: context-engineering
```

---

## Skills Overview

**<!-- SKILL_COUNT -->17<!-- /SKILL_COUNT --> specialized skills** organized by domain:

### 📚 PhD Academic Business Research (4 skills)
- **academic-writing**: LaTeX manuscript drafting and revision for finance, economics, and real estate research
- **pyfixest-latex**: PyFixest econometric models to publication-quality LaTeX (DiD, event studies, panel regression)
- **stata-accounting-research**: STATA code patterns from published accounting research (entropy balancing, PSM, DiD, RDD, IV)
- **pandas-pro**: DataFrame manipulation, data cleaning, aggregation, time series analysis for research

### 💰 Financial Analysis & Services (3 skills)
- **wrds-data-pull**: WRDS data extraction (Compustat, CRSP, IBES, Thomson Reuters, BoardEx, ISS, CoreLogic, ZTRAX, CoStar)
- **pandas-pro**: Financial data analysis, portfolio analytics, return calculations, risk metrics
- **pyfixest-latex**: Financial econometric analysis and publication-ready output

### 🏢 Real Estate (Residential/Commercial) (1 skill)
- **cre-investment-analysis**: Commercial real estate investment analysis, DCF/IRR modeling, business plans, institutional underwriting

### 🤖 AI/ML/AI Agents (3 skills)
- **ml-pipeline**: ML pipelines with MLflow/Kubeflow, experiment tracking, feature stores, model lifecycle
- **prompt-engineer**: LLM prompt design, chain-of-thought, few-shot learning, evaluation frameworks
- **mcp-developer**: Model Context Protocol servers/clients for AI tool integration

### 💻 Development & Technical Writing (5 skills)
- **fastapi-expert**: Async Python APIs with FastAPI, Pydantic V2, async SQLAlchemy, JWT auth
- **code-documenter**: Docstrings, API docs (OpenAPI/Swagger), documentation sites, user guides
- **code-reviewer**: PR reviews, code quality audits, security checks, refactoring suggestions
- **debugging-wizard**: Systematic debugging, error investigation, root cause analysis
- **n8n-skills**: n8n workflow automation, node configuration, workflow patterns

### 📊 Data Visualization (2 skills)
- **matplotlib**: Low-level plotting library for full customization, novel plot types, fine-grained control
- **scientific-visualization**: Publication-ready multi-panel figures with journal-specific formatting (Nature, Science, Cell)

### 🧠 Context Engineering (1 skill)
- **context-engineering**: Audit, optimize, and architect the AI agent context layer (CLAUDE.md, hooks, commands, skills)

See **[SKILLS_GUIDE.md](SKILLS_GUIDE.md)** for when to use each skill, workflows, and examples.

### Recommended Complementary Skills

These skills work seamlessly with the collection above. **Highly recommended** for document processing in research and real estate workflows:

#### Official Anthropic Document Skills

- **[pdf](https://github.com/anthropics/skills/tree/main/skills/pdf)** - Extract text/tables from PDFs, OCR scanned documents
  - Essential for: Offering memos, appraisals, research papers, reports

- **[xlsx](https://github.com/anthropics/skills/tree/main/skills/xlsx)** - Read/write Excel spreadsheets, create financial models
  - Essential for: Rent rolls, operating statements, financial models, data analysis
  - **Critical for CRE**: Creates professional models with proper formulas and formatting

- **[docx](https://github.com/anthropics/skills/tree/main/skills/docx)** - Process Word documents, create reports
  - Essential for: Investment memos, business plans, market reports

- **[pptx](https://github.com/anthropics/skills/tree/main/skills/pptx)** - Create/analyze PowerPoint presentations
  - Essential for: Investment committee presentations, board decks

**Installation**: These skills are built-in to Claude.ai and available at `/mnt/skills/public/` in Claude Code.

**Integration Example**:
```
pdf (extract offering memo) → pandas-pro (analyze data) →
cre-investment-analysis (perform analysis) → xlsx (create model) →
pptx (create presentation)
```

#### Discover More Skills

For a comprehensive, up-to-date catalog of available skills:

🔗 **[skills.sh](https://skills.sh/)** - Browse hundreds of community and official skills

---

## Architecture

### Progressive Disclosure Pattern

Each skill follows this structure:

```
skills/fastapi-expert/
├── SKILL.md                    # Lean core (~80 lines)
│   ├── Role definition
│   ├── When to use
│   ├── Core workflow
│   └── Routing table          # Points to references
└── references/                 # Loaded on-demand
    ├── async-patterns.md
    ├── pydantic-v2.md
    ├── authentication.md
    └── ...
```

**How It Works:**
1. Skill loads with minimal context (~80 lines)
2. Claude reads the routing table
3. Loads specific references only when context requires
4. 50% faster initial responses, surgical precision when needed

**Stats:**
- <!-- SKILL_COUNT -->17<!-- /SKILL_COUNT --> skills
- <!-- REFERENCE_COUNT -->89<!-- /REFERENCE_COUNT --> reference files
- ~50% token reduction through progressive disclosure

---

## Usage Patterns

### Multi-Skill Workflows

Complex tasks combine multiple skills:

**Academic Research Paper:**
```
wrds-data-pull → pandas-pro → pyfixest-latex → code-documenter → code-reviewer
```

**Financial Analysis Project:**
```
wrds-data-pull → pandas-pro → code-documenter → code-reviewer
```

**Real Estate Investment Analysis:**
```
pandas-pro → cre-investment-analysis → code-documenter
```

**ML/AI Pipeline:**
```
pandas-pro → ml-pipeline → prompt-engineer → mcp-developer → code-documenter
```

**API Development:**
```
fastapi-expert → debugging-wizard → code-documenter → code-reviewer
```

**Accounting Research (STATA):**
```
wrds-data-pull → stata-accounting-research → code-documenter
```

---

## Tech Stack Coverage

### Research & Academia
- **Econometrics**: PyFixest (DiD, event studies, panel regression), STATA (PSM, entropy balancing, RDD, IV)
- **Data Sources**: WRDS (Compustat, CRSP, IBES, Thomson Reuters, BoardEx, ISS, CoreLogic, ZTRAX)
- **Output**: LaTeX tables/figures, publication-quality plots
- **Languages**: Python 3.11+, STATA 18

### Financial Analysis
- **Data**: pandas, NumPy, SciPy
- **Sources**: WRDS financial databases
- **Methods**: Portfolio analytics, return calculations, risk metrics, event studies
- **Integration**: SQL queries, CUSIP/GVKEY/PERMNO linking

### Real Estate
- **Analysis**: DCF modeling, IRR analysis, NOI calculations, cap rate analysis
- **Property Types**: Multifamily, office, retail, industrial, mixed-use
- **Output**: Investment memos, underwriting models, feasibility studies

### AI/ML
- **Pipelines**: MLflow, Kubeflow, experiment tracking, feature stores
- **LLMs**: Prompt engineering, chain-of-thought, few-shot learning
- **Integration**: Model Context Protocol (MCP), AI tool development
- **ML Stack**: scikit-learn, PyTorch, TensorFlow

### Development
- **Backend**: FastAPI, Pydantic V2, async SQLAlchemy, OpenAPI/Swagger
- **Automation**: n8n workflow automation, webhook processing
- **Documentation**: Docstrings, API docs, technical writing
- **Quality**: Code review, debugging, security audits

---

## Project Structure

```
Agent-Skills/
├── .claude-plugin/
│   ├── plugin.json           # Plugin metadata
│   └── marketplace.json      # Marketplace configuration
├── skills/                   # 17 specialized skills
│   ├── academic-writing/
│   ├── code-documenter/
│   ├── code-reviewer/
│   ├── context-engineering/
│   ├── cre-investment-analysis/
│   ├── debugging-wizard/
│   ├── fastapi-expert/
│   ├── matplotlib/
│   ├── mcp-developer/
│   ├── ml-pipeline/
│   ├── n8n-skills/
│   ├── pandas-pro/
│   ├── prompt-engineer/
│   ├── pyfixest-latex/
│   ├── scientific-visualization/
│   ├── stata-accounting-research/
│   └── wrds-data-pull/
├── commands/                 # 9 workflow commands
│   ├── common-ground/
│   └── project/
├── scripts/
│   ├── update-docs.py        # Update version and counts
│   └── validate-skills.py    # Validate skill integrity
├── docs/
│   ├── ATLASSIAN_MCP_SETUP.md
│   ├── COMMON_GROUND.md
│   └── WORKFLOW_COMMANDS.md
├── README.md
├── SKILLS_GUIDE.md          # Quick reference guide
├── CLAUDE.md                # Project configuration
└── CONTRIBUTING.md          # Contribution guidelines
```

---

## Documentation

- **[SKILLS_GUIDE.md](SKILLS_GUIDE.md)** - Quick reference for when to use each skill
- **[CLAUDE.md](CLAUDE.md)** - Project configuration and skill authorship standards
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guidelines for contributing
- **skills/*/SKILL.md** - Individual skill documentation
- **skills/*/references/** - Deep-dive reference materials

---

## Maintenance

### Update Documentation

When adding/removing skills or changing versions:

```bash
# Update version in version.json, then:
python scripts/update-docs.py

# Validate all skills
python scripts/validate-skills.py
```

### Validate Skills

Before committing changes:

```bash
# Run full validation
python scripts/validate-skills.py

# Validate specific skill
python scripts/validate-skills.py --skill fastapi-expert

# Check YAML only
python scripts/validate-skills.py --check yaml
```

---

## Contributing

This is a personal skill collection, but contributions are welcome!

### Adding a New Skill

1. Create skill directory:
   ```bash
   mkdir -p skills/my-skill/references
   ```

2. Create lean SKILL.md with YAML frontmatter:
   ```yaml
   ---
   name: my-skill
   description: Use when [triggering conditions]
   triggers:
     - keyword1
     - keyword2
   role: specialist|expert|architect
   scope: implementation|review|design
   output-format: code|document|report
   ---
   ```

3. Create reference files (100-600 lines each)

4. Update version.json and run:
   ```bash
   python scripts/update-docs.py
   python scripts/validate-skills.py
   ```

5. Test locally and commit

See **[CLAUDE.md](CLAUDE.md)** for detailed authorship standards.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

Original template: [jeffallan/claude-skills](https://github.com/jeffallan/claude-skills)

---

## Skill Sources & Attribution

Some skills in this collection were created by other contributors in the community:

### Community-Contributed Skills

- **[stata-accounting-research](skills/stata-accounting-research/)**
  - Original: [jusi-aalto/stata-accounting-research](https://github.com/jusi-aalto/stata-accounting-research)
  - Author: @jusi-aalto
  - Description: STATA code patterns from 126+ published JAR papers

- **[n8n-skills](skills/n8n-skills/)**
  - Original: [haunchen/n8n-skills](https://github.com/haunchen/n8n-skills)
  - Author: Frank Chen (@haunchen)
  - Description: n8n workflow automation knowledge base
  - License: MIT

- **[matplotlib](skills/matplotlib/)** + **[scientific-visualization](skills/scientific-visualization/)**
  - Original: [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills)
  - Author: K-Dense Inc.
  - Description: Scientific plotting and publication-ready figures
  - License: MIT

### Related Resources

- **[K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills)** - Additional scientific research skills (matplotlib, scientific-visualization source)
- **[quant-sentiment-ai/claude-equity-research](https://github.com/quant-sentiment-ai/claude-equity-research)** - Equity research analysis skills

**Check for Updates**: Visit the original repositories above to get the latest versions and contribute back improvements.

---

## About

**Personal skill collection** for Python development, data analysis, econometric research, and AI integration.

Built on the [Agent Skills](https://agentskills.io/specification) specification.

Originally forked from [jeffallan/claude-skills](https://github.com/jeffallan/claude-skills).

---

**Built for Claude Code** | **<!-- WORKFLOW_COUNT -->9<!-- /WORKFLOW_COUNT --> Workflows** | **<!-- REFERENCE_COUNT -->89<!-- /REFERENCE_COUNT --> Reference Files** | **<!-- SKILL_COUNT -->17<!-- /SKILL_COUNT --> Skills**
