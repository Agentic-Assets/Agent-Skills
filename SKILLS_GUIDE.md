# Skills Quick Reference Guide

## Skill Categories

This personal skill collection supports work across five domains:

### 📚 PhD Academic Business Research (4 skills)
- **academic-writing**: LaTeX manuscript drafting and revision for finance, economics, and real estate research
- **pyfixest-latex**: PyFixest econometric models to publication-quality LaTeX (DiD, event studies, panel regression)
- **stata-accounting-research**: STATA code patterns from published accounting research (entropy balancing, PSM, DiD, RDD, IV)
- **pandas-pro**: DataFrame manipulation, data cleaning, aggregation, time series analysis

### 💰 Financial Analysis & Services (2 skills)
- **pandas-pro**: Financial data analysis, portfolio analytics, time series
- **wrds-data-pull**: WRDS data extraction (Compustat, CRSP, IBES, Thomson Reuters)

### 🏢 Real Estate (Residential/Commercial) (1 skill)
- **cre-investment-analysis**: Commercial real estate investment analysis, DCF/IRR modeling, business plans, institutional underwriting

### 🤖 AI/ML/AI Agents (3 skills)
- **ml-pipeline**: ML pipelines with MLflow/Kubeflow, experiment tracking, feature stores
- **prompt-engineer**: LLM prompt design, chain-of-thought, few-shot learning, evaluation frameworks
- **mcp-developer**: Model Context Protocol servers/clients, AI tool integration

### 💻 Development & Technical Writing (5 skills)
- **fastapi-expert**: Async Python APIs with FastAPI, Pydantic V2, async SQLAlchemy
- **code-documenter**: Docstrings, API docs (OpenAPI/Swagger), documentation sites
- **code-reviewer**: PR reviews, code quality audits, security checks
- **debugging-wizard**: Systematic debugging, error investigation, root cause analysis
- **n8n-skills**: n8n workflow automation, node configuration, workflow patterns

### 📊 Data Visualization (2 skills)
- **matplotlib**: Low-level plotting with full customization, novel plot types, fine-grained control
- **scientific-visualization**: Publication-ready multi-panel figures with journal-specific formatting (Nature, Science, Cell)

### 🧠 Context Engineering (1 skill)
- **context-engineering**: Audit, optimize, and architect the AI agent context layer (CLAUDE.md, hooks, commands, skills)

---

## When to Use Each Skill

### PhD Academic Business Research

**academic-writing**
- Use when: Creating or revising academic paper sections, formatting for journal submission, writing referee responses
- Triggers: academic writing, research paper, LaTeX manuscript, journal submission, referee response, JF, JFE, RFS
- Output: LaTeX manuscript sections, referee response letters

**pyfixest-latex**
- Use when: Generating regression tables, event study plots, or summary statistics for academic papers
- Triggers: PyFixest, LaTeX tables, econometric, DiD, event study, fixed effects
- Output: LaTeX .tex files, PNG figures

**stata-accounting-research**
- Use when: Requesting STATA code patterns for empirical accounting research methods
- Triggers: STATA, accounting research, entropy balancing, PSM, DiD, RDD, IV, Fama-MacBeth
- Output: STATA .do files with tested syntax

**pandas-pro**
- Use when: Data cleaning, transformation, aggregation for research datasets
- Triggers: pandas, DataFrame, data cleaning, aggregation, time series
- Output: Python code with efficient pandas operations

### Financial Analysis & Services

**pandas-pro**
- Use when: Financial data analysis, portfolio analytics, return calculations
- Triggers: pandas, financial data, portfolio, returns, risk metrics
- Output: Python code for financial analysis

**wrds-data-pull**
- Use when: Extracting data from WRDS databases or merging financial datasets
- Triggers: WRDS, Compustat, CRSP, IBES, CUSIP, GVKEY, PERMNO
- Output: SQL queries, Python extraction scripts, linking tables

### Real Estate

**cre-investment-analysis**
- Use when: Analyzing commercial properties, creating investment memos, DCF/IRR analysis
- Triggers: commercial real estate, CRE, multifamily, DCF, IRR, NOI, cap rate
- Output: Investment analysis reports, financial models

### AI/ML/AI Agents

**ml-pipeline**
- Use when: Building ML training pipelines, experiment tracking, model lifecycle management
- Triggers: ML pipeline, MLflow, Kubeflow, model training, experiment tracking
- Output: Python code for ML pipelines

**prompt-engineer**
- Use when: Designing LLM prompts, optimizing model performance, building evaluation frameworks
- Triggers: prompt engineering, LLM, chain-of-thought, few-shot, prompt evaluation
- Output: Prompt designs, evaluation frameworks

**mcp-developer**
- Use when: Building MCP servers/clients for AI tool integration
- Triggers: MCP, Model Context Protocol, AI tools, Claude integration
- Output: Python/TypeScript MCP server code

### Development & Technical Writing

**fastapi-expert**
- Use when: Building async Python APIs with FastAPI
- Triggers: FastAPI, Pydantic, async Python, REST API, SQLAlchemy async
- Output: Python API code

**code-documenter**
- Use when: Adding docstrings, API docs, or building documentation sites
- Triggers: documentation, docstrings, OpenAPI, Swagger, API docs
- Output: Documented code, API specs

**code-reviewer**
- Use when: Reviewing code for quality, security, or best practices
- Triggers: code review, PR review, code quality, security
- Output: Review report with recommendations

**debugging-wizard**
- Use when: Investigating errors, analyzing stack traces, troubleshooting
- Triggers: debug, error, bug, exception, stack trace, troubleshoot
- Output: Root cause analysis, fix recommendations

**n8n-skills**
- Use when: Building workflow automation with n8n
- Triggers: n8n, workflow automation, webhook, workflow trigger
- Output: n8n workflow configurations

### Data Visualization

**matplotlib**
- Use when: Creating custom plots, fine-grained control over figure elements, novel visualization types
- Triggers: matplotlib, plot, visualization, figure, chart, pyplot, custom plot
- Output: Python code for matplotlib figures

**scientific-visualization**
- Use when: Creating publication-ready multi-panel figures with journal-specific formatting
- Triggers: publication figure, journal figure, multi-panel plot, Nature figure, Science figure, significance annotation
- Output: Python code for journal-quality figures

### Context Engineering

**context-engineering**
- Use when: Auditing or optimizing CLAUDE.md files, hooks, commands, or skills for AI agent effectiveness
- Triggers: CLAUDE.md, context engineering, agent instructions, agent memory, context audit, context architecture
- Output: Audit reports, optimized context files, gap analyses

---

## Common Workflows

### Academic Research Paper

**Data → Analysis → Output**
1. **wrds-data-pull** or **pandas-pro** - Extract and clean data
2. **pyfixest-latex** or **stata-accounting-research** - Run econometric analysis
3. **code-documenter** - Document methodology
4. **code-reviewer** - Review analysis code

### Financial Analysis Project

**Data → Analysis → Report**
1. **wrds-data-pull** - Extract financial data from WRDS
2. **pandas-pro** - Clean, merge, and analyze data
3. **code-documenter** - Document analysis
4. **code-reviewer** - Quality check

### Real Estate Investment Analysis

**Property → Analysis → Decision**
1. **pandas-pro** - Analyze property/market data
2. **cre-investment-analysis** - Create investment analysis and DCF model
3. **code-documenter** - Document assumptions and methodology

### ML/AI Project

**Data → Pipeline → Production**
1. **pandas-pro** - Data preparation and feature engineering
2. **ml-pipeline** - Build training pipeline with experiment tracking
3. **prompt-engineer** - Design LLM components (if applicable)
4. **mcp-developer** - Build AI integrations
5. **code-documenter** - Document pipeline
6. **code-reviewer** - Review implementation

### API Development

**Design → Implement → Test → Document**
1. **fastapi-expert** - Implement API endpoints
2. **debugging-wizard** - Debug issues
3. **code-documenter** - Create OpenAPI documentation
4. **code-reviewer** - Review code quality and security

### Automation Workflow

**Design → Build → Integrate → Test**
1. **n8n-skills** - Design workflow
2. **mcp-developer** - Add AI capabilities (if needed)
3. **debugging-wizard** - Troubleshoot workflow
4. **code-documenter** - Document automation

---

## Decision Trees

### Research & Analysis Tasks

**What type of analysis?**
- **Academic paper writing** → academic-writing
- **Econometric (Python)** → pyfixest-latex
- **Econometric (STATA)** → stata-accounting-research
- **Data manipulation** → pandas-pro
- **Financial data extraction** → wrds-data-pull
- **Real estate investment** → cre-investment-analysis

### Development Tasks

**What are you building?**
- **REST API** → fastapi-expert
- **ML pipeline** → ml-pipeline
- **AI integration** → mcp-developer
- **Workflow automation** → n8n-skills
- **LLM application** → prompt-engineer

### Visualization Tasks

**What type of figure?**
- **Custom/exploratory plots** → matplotlib
- **Publication-ready journal figures** → scientific-visualization

### Code Quality Tasks

**What do you need?**
- **Documentation** → code-documenter
- **Code review** → code-reviewer
- **Debugging** → debugging-wizard
- **Agent context optimization** → context-engineering

---

## Skill Combinations

### Research-Focused Combinations

**Accounting Research (STATA)**
```
wrds-data-pull → stata-accounting-research → code-documenter
```

**Finance Research (Python)**
```
wrds-data-pull → pandas-pro → pyfixest-latex → code-documenter
```

**Real Estate Research**
```
pandas-pro → cre-investment-analysis → code-documenter
```

### Development-Focused Combinations

**API Development**
```
fastapi-expert → debugging-wizard → code-documenter → code-reviewer
```

**ML Pipeline Development**
```
pandas-pro → ml-pipeline → prompt-engineer → code-documenter → code-reviewer
```

**AI Agent Development**
```
mcp-developer → prompt-engineer → fastapi-expert → code-documenter
```

### Full-Stack Workflows

**Research Data Pipeline**
```
wrds-data-pull → pandas-pro → pyfixest-latex → code-documenter → code-reviewer
```

**Financial Analysis Platform**
```
wrds-data-pull → pandas-pro → fastapi-expert → code-documenter → code-reviewer
```

**AI-Powered Research Tool**
```
wrds-data-pull → pandas-pro → ml-pipeline → mcp-developer → prompt-engineer → code-documenter
```

---

## Example Prompts by Domain

### PhD Academic Business Research

- "Extract Compustat data for my accounting study" → wrds-data-pull
- "Run DiD analysis and generate LaTeX tables" → pyfixest-latex
- "Show me STATA code for entropy balancing" → stata-accounting-research
- "Clean this panel dataset for regression analysis" → pandas-pro
- "Merge CRSP and Compustat using CCM linking table" → wrds-data-pull

### Financial Analysis & Services

- "Pull IBES analyst estimates for tech companies" → wrds-data-pull
- "Calculate portfolio returns and risk metrics" → pandas-pro
- "Analyze stock price reactions around earnings announcements" → pandas-pro
- "Build financial ratios from Compustat fundamentals" → wrds-data-pull
- "Create event study with CRSP daily returns" → pandas-pro + pyfixest-latex

### Real Estate

- "Analyze this multifamily acquisition opportunity" → cre-investment-analysis
- "Build DCF model for office building investment" → cre-investment-analysis
- "Create investment memo for REIT portfolio" → cre-investment-analysis
- "Evaluate mixed-use development feasibility" → cre-investment-analysis
- "Perform sensitivity analysis on cap rate assumptions" → cre-investment-analysis

### AI/ML/AI Agents

- "Build MLflow experiment tracking pipeline" → ml-pipeline
- "Design prompts for financial text classification" → prompt-engineer
- "Create MCP server for database access" → mcp-developer
- "Optimize this LLM prompt for accuracy" → prompt-engineer
- "Build feature store for ML pipeline" → ml-pipeline

### Development & Technical Writing

- "Implement async FastAPI endpoint with Pydantic V2" → fastapi-expert
- "Add OpenAPI documentation to my API" → code-documenter + fastapi-expert
- "Review this code for security vulnerabilities" → code-reviewer
- "Debug this async Python error" → debugging-wizard
- "Create n8n workflow to process webhooks" → n8n-skills

---

## Tips for Effective Use

1. **Be Specific About Domain**: Mention whether it's research, finance, real estate, or development work
2. **Specify Data Source**: For research, mention WRDS, Compustat, CRSP, etc.
3. **State Your Output Goal**: LaTeX tables, investment memo, API endpoint, etc.
4. **Combine Skills**: Complex projects benefit from multiple skill perspectives
5. **Document Everything**: Use code-documenter for reproducibility and academic rigor

---

## Quick Reference by Use Case

**"I need to..."**

| Task | Skills to Use |
|------|---------------|
| Write academic paper sections | academic-writing |
| Pull financial data from WRDS | wrds-data-pull |
| Run econometric analysis (Python) | pyfixest-latex |
| Run econometric analysis (STATA) | stata-accounting-research |
| Clean and analyze data | pandas-pro |
| Analyze CRE investment | cre-investment-analysis |
| Build ML pipeline | ml-pipeline |
| Design LLM prompts | prompt-engineer |
| Create AI integration | mcp-developer |
| Build Python API | fastapi-expert |
| Document code | code-documenter |
| Review code quality | code-reviewer |
| Fix bugs | debugging-wizard |
| Automate workflows | n8n-skills |
| Create custom plots | matplotlib |
| Create publication figures | scientific-visualization |
| Audit/optimize agent context | context-engineering |
