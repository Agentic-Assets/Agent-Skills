# Context Engineering

Architect, audit, and optimize the context layer that governs AI agent effectiveness in any codebase.

## What This Skill Does

- **Audits** existing context engineering maturity using a 70-point scoring rubric and produces a structured report with recommendations
- **Optimizes** CLAUDE.md files, hooks, slash commands, and skills through a five-pass refinement process (prune, sharpen, structure, fortify, budget)
- **Performs gap analysis** by matching your project to an archetype (web app, API, library, monorepo, etc.) and identifying missing context layers
- **Bootstraps** context engineering from scratch, generating a root CLAUDE.md, module-level files, and hooks for projects with no existing setup
- **Diagnoses** agent underperformance by checking for anti-patterns, contradictions, misplaced rules, and missing verification loops
- **Guides feature selection** so each rule or knowledge piece uses the right mechanism (CLAUDE.md, hooks, skills, MCP, or subagents)

## Installation

### Option 1: Install via `.skill` file

Create a file called `context-engineering.skill` in your project's `.claude/skills/` directory:

```
https://github.com/jeffallan/claude-skills/tree/main/skills/context-engineering
```

Claude Code will automatically fetch and use the skill when relevant triggers are matched.

### Option 2: Copy the folder

Copy the entire `skills/context-engineering/` folder into your project's `.claude/skills/` directory:

```bash
cp -r skills/context-engineering .claude/skills/context-engineering
```

## What's Included

```
context-engineering/
├── SKILL.md                            # Core skill definition and workflows
├── README.md                           # This file
├── references/
│   ├── anti-patterns.md                # 12 common context anti-patterns and diagnostics
│   ├── audit-checklist.md              # 70-point scoring rubric for context maturity
│   ├── context-patterns.md             # Project archetype templates and must-have context
│   └── feature-selection.md            # Decision framework for choosing the right mechanism
└── scripts/
    └── scan-context.sh                 # Inventories all context artifacts in a project
```

## Example Prompts

**Audit an existing project's context layer:**

> "Audit the context engineering in this repo. Score the CLAUDE.md files, hooks, and slash commands, then tell me what's missing and what to fix first."

**Bootstrap context for a new project:**

> "This project has no CLAUDE.md or agent configuration. Set up context engineering from scratch based on the codebase structure and tech stack."

## Platform Compatibility

| Platform     | Supported |
|--------------|-----------|
| Claude Code  | Yes       |
| Cursor       | Yes       |
| Windsurf     | Yes       |

## Related Skills

- **code-review** — Reviews code quality; context engineering ensures the agent knows project conventions before reviewing
- **debug** — Investigates bugs; effective context prevents recurring agent mistakes that lead to bugs
