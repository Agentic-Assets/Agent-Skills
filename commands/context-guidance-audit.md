---
description: "Two-phase context guidance audit — read skill, audit with subagents, remediate, delete review folder"
---

# Context Guidance Audit

Run a full **context guidance audit** on this repository.

## Step 0 — Invoke the skill

**First:** Read and follow `skills/context-guidance-audit/SKILL.md` (or `~/.claude/skills/context-guidance-audit/SKILL.md` when installed from this collection). Treat it as the source of truth for phases, subagent rules, report format, and cleanup.

Discover guidance artifacts before scoping (`Glob **/CLAUDE.md`, root agent instruction files, `.cursor/`, `.agents/`, docs index). Map **recent codebase changes** to guidance and ensure **≥1–2 Phase 1 scopes** cover those areas. Do not assume this repo matches any example layout in the skill references.

## Step 1 — Phase 1 (read-only audit)

1. Create `docs/reviews/context-guidance-audit-YYYY-MM-DD/`.
2. Split into **4–8 disjoint scopes** (see skill `references/example-scope-splits.md`).
3. Launch **one subagent per scope in parallel** — **no guidance edits**; verify findings; write `NN-<scope-slug>.md` using the skill’s report template.
4. **Wait for all Phase 1 subagents to finish.**
5. Optionally write `SYNTHESIS.md`. Do not remediate yet unless the user asked for audit-and-fix in one run.

## Step 2 — Gate

If fixes were not pre-approved, stop after Phase 1, summarize, and ask to proceed. Otherwise continue.

## Step 3 — Phase 2 (verify + remediate)

1. **One subagent per Phase 1 report**, parallel when scopes are disjoint.
2. Re-verify findings; fix verified issues in **guidance files only**; append `## Remediation log` to each report.
3. **Wait for all Phase 2 subagents to finish.**
4. Run repo doc/link verification if applicable.

## Step 4 — Close out

Summarize fixes and deferrals. **Delete** the audit folder after acceptance (or immediately if unattended cleanup is configured). Do not commit unless asked.

**Orchestration:** Many narrow subagents; Phase 1 = reports only; Phase 2 = fixes only; write-capable subagents for file output.
