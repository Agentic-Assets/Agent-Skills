---
name: stata-background-runner
description: Use when running or troubleshooting Stata do-files in the background on macOS or Windows.
triggers:
  - Stata
  - do-file
  - background Stata
  - Stata batch
  - macOS Stata
  - Windows Stata
  - StataMP
  - StataSE
role: specialist
scope: implementation
output-format: code
---

# Stata Background Runner

Run a Stata do-file in batch mode, monitor the actual process, and verify the result on the current computer. Use the installed Stata version and licensed edition; do not assume a fixed version, username, installation path, shell, or operating system.

## Workflow

1. Identify the operating system and shell. Read the corresponding reference below and discover the executable locally. Honor an explicit executable path; if several installations are plausible, select the intended licensed edition rather than guessing.
2. Inspect the do-file's inputs, working-directory assumptions, dependencies, and output paths. Choose the working directory the analysis requires and plan a writable, non-colliding log location. Do not overwrite existing research outputs without authorization.
3. Launch batch Stata with a properly quoted absolute do-file path; check for Stata macro characters and other unsafe path characters before launch. Retain the process handle or PID and log location; do not infer completion from an output file appearing.
4. Wait or poll with a bounded timeout. On timeout report that the job is still running, and retain its identifier; do not kill it without authorization. Inspect the complete log and expected outputs after the process exits. A zero process exit code alone does not prove the do-file succeeded.
5. Report the executable, working directory, log, process outcome, and verified results. Investigate errors in the log, including errors intentionally caught by `capture`; a generic text search alone cannot establish success.

For long jobs, use a fresh completion marker written only after the intended final operation succeeds, in addition to process and log inspection. A marker from a previous run, an intermediate output, or an `end of do-file` line is not proof of success. Do not alter the analysis merely to create a marker without preserving its semantics.

## References

| Platform | Read when |
| --- | --- |
| [macOS launch and troubleshooting](references/macos-launch-and-troubleshooting.md) | Running from a Mac terminal or agent shell |
| [Windows launch and troubleshooting](references/windows-launch-and-troubleshooting.md) | Running from PowerShell, Windows Terminal, or a Windows bash shell |

Stata's own [Mac batch guidance](https://www.stata.com/support/faqs/mac/advanced-topics/) and [Windows batch guidance](https://www.stata.com/support/faqs/windows/batch-mode/) describe the platform modes.
