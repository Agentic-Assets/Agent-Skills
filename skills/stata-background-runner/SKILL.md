---
name: stata-background-runner
description: Use when running a Stata .do file on Windows - launching it silently in the background, polling for completion, or diagnosing failures like GUI windows appearing, relative-path errors, or wrong-executable errors.
triggers:
  - Stata
  - do-file
  - .do file
  - run Stata
  - Windows batch
  - PowerShell Start-Process
  - StataMP
  - StataSE
  - StataIC
role: specialist
scope: implementation
output-format: code
---

# Stata Background Runner

Run Stata 18 do-files on Windows silently from a bash-based agent shell, monitor them for completion, and recover from the common failure modes.

## Why this is not obvious

Claude Code runs in a bash shell. PowerShell cmdlets like `Start-Process` cannot be called directly from bash — they fail with `command not found`. The correct pattern wraps everything in `powershell.exe -Command "..."`.

Stata's `/e` batch flag suppresses interactive prompts but still opens a visible window; `-WindowStyle Hidden` is required to run truly silently.

## Core workflow

1. Find the installed Stata executable (`StataMP-64.exe`, `StataSE-64.exe`, or `StataIC-64.exe`).
2. Launch it with `Start-Process` via `powershell.exe -Command`, using an absolute path to the do-file and `-WindowStyle Hidden`.
3. Poll for the **last** file the script writes to detect completion — Stata gives no shell-level completion signal.
4. On failure, match the symptom against the common failure modes table.
5. For pipeline work, prefer a standalone wrapper do-file that sets its own globals and loads its own data.

## Constraints

- MUST use an absolute path to the do-file; relative paths cause `command E is unrecognized r(199)`.
- MUST pass `-WindowStyle Hidden`; `/e` alone still opens a visible window.
- MUST escape inner quotes around the do-file path inside the PowerShell string (`\"`).
- MUST poll for the last output file the script writes, not an early one — an early file gives a false "done" signal.
- MUST NOT call PowerShell cmdlets directly from bash; always wrap in `powershell.exe -Command "..."`.

## Reference

- [Windows launch, monitoring, and failure modes](references/windows-launch-and-troubleshooting.md) — full launch command, monitoring pattern, failure-mode table, machine-portability handling, and a complete worked example.
