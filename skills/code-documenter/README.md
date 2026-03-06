# Code Documenter

Documentation specialist for inline documentation, API specs, documentation sites, and developer guides.

## What This Skill Does

- Adds docstrings to functions and classes using Google, NumPy, Sphinx, or JSDoc formats
- Creates OpenAPI/Swagger specifications and interactive API portals (Swagger UI, Redoc, Stoplight)
- Builds documentation sites with Docusaurus, MkDocs, or VitePress
- Documents multi-protocol APIs including REST, GraphQL, WebSocket, and gRPC
- Writes getting started guides, tutorials, and user-facing documentation
- Generates documentation coverage reports and metrics

## Installation

### Option 1: Download the `.skill` file (Easiest)

1. Download `code-documenter.skill` from the releases page
2. Place it in your project's `.claude/skills/` directory (or `~/.claude/skills/` for global access)

### Option 2: Copy the skill folder

1. Copy the entire `skills/code-documenter/` directory into your project's `.claude/skills/` directory:

```bash
cp -r skills/code-documenter .claude/skills/
```

## What's Included

```
code-documenter/
├── SKILL.md                                  # Main skill definition and workflow
├── README.md                                 # This file
└── references/
    ├── api-docs-fastapi-django.md            # FastAPI and Django API documentation patterns
    ├── api-docs-nestjs-express.md            # NestJS and Express API documentation patterns
    ├── coverage-reports.md                   # Documentation coverage reporting and metrics
    ├── documentation-systems.md              # Doc sites, static generators, search, testing
    ├── interactive-api-docs.md               # OpenAPI 3.1, portals, GraphQL, WebSocket, gRPC, SDKs
    ├── python-docstrings.md                  # Google, NumPy, and Sphinx docstring styles
    ├── typescript-jsdoc.md                   # JSDoc patterns for TypeScript projects
    └── user-guides-tutorials.md              # Getting started guides, tutorials, FAQs
```

## Example Prompts

- "Add Google-style docstrings to all public functions and classes in `src/services/`, then generate a coverage report."
- "Create an OpenAPI 3.1 spec for our REST API and set up a Redoc portal so the team can browse endpoints interactively."

## Platform Compatibility

| Platform | Compatibility | Notes |
|----------|:---:|-------|
| Claude Code | Yes | Full support including reference file loading |
| Claude.ai Projects | Yes | Add SKILL.md and references to project knowledge |
| Other LLM platforms | Partial | SKILL.md works as a system prompt; reference routing may need manual handling |

## Related Skills

- **Spec Miner** - Provides code analysis insights that inform documentation
- **Fullstack Guardian** - Documents code during implementation
- **Code Reviewer** - Checks documentation quality during reviews
