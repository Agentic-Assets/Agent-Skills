---
name: goal-writer
description: Use when the user asks to create, draft, save, revise, or improve a Codex Goal, GOAL.md, goal file, persistent objective, completion contract, or long-running Codex work objective. This skill must be used before inventing or saving any goal for Codex.
---

# Goal Writer

Write concise Codex Goal files using the OpenAI Goals pattern: a goal is a scoped completion contract, not a vague task prompt.

## Output

Save one Markdown file under `goals/` named:

```text
YYYY-MM-DD-<short-slug>-goal.md
```

The saved goal body should be between 3000 and 4000 characters, excluding frontmatter if any. Treat 4000 characters as a hard cap, but do not over-optimize exact length once the goal lands anywhere in that range. Do not use `GOAL.md`, `goal.md`, or undated names.

## Required Shape

Use these headings:

```markdown
# Codex Goal - <short title>

## Goal

## Boundaries

## Iteration Policy

## Verification

## Deliverables

## Blocked Stop Condition
```

## Workflow

1. Identify the real objective and the evidence Codex can inspect.
2. Convert weak wording into an auditable end state: outcome, verification surface, and constraints.
3. Keep the goal narrow enough to audit but broad enough for Codex to choose next actions.
4. Define what counts as done, partial, blocked, and out of scope.
5. Include verification commands, artifacts, reports, or review surfaces.
6. Save the file to `goals/YYYY-MM-DD-<short-slug>-goal.md`.
7. If the user asked to start the Goal in Codex, use the saved file as the source for `/goal`.

## Standards

- Goal: one paragraph naming the durable end state.
- Boundaries: files, systems, branches, data sources, user constraints, and non-goals.
- Iteration Policy: how Codex should proceed between evidence checks, when to pause, and how to handle discoveries.
- Verification: concrete checks such as tests, builds, benchmarks, browser proof, report review, or artifact inspection.
- Deliverables: exact files, reports, commits, or decisions expected.
- Blocked Stop Condition: when Codex must stop and report rather than claim completion.

Do not mark a goal complete just because a budget is reached. Budget exhaustion means summarize progress, blockers, and the next useful step.

## Filename Slug

Use a short lowercase slug from the objective:

- `2026-05-20-citation-refresh-hardening-goal.md`
- `2026-05-20-prospecting-browser-qa-goal.md`
- `2026-05-20-replication-evidence-audit-goal.md`

## Source Pattern

This follows OpenAI's "Using Goals in Codex" guidance: strong goals name the outcome, verification method, and constraints, and research goals must separate confirmed evidence, support-only evidence, blockers, and remaining uncertainty.
