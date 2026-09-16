# Running Stata 18 on Windows: Silent Background Execution

## Finding the executable

Stata MP and SE use different executables. Check what is installed:

```bash
powershell.exe -Command "Get-ChildItem 'C:\Program Files\Stata18\' -Filter 'Stata*.exe'"
```

Common names: `StataMP-64.exe`, `StataSE-64.exe`, `StataIC-64.exe`. Use whichever is present.

## The launch command

```bash
powershell.exe -Command "Start-Process \
  -FilePath 'C:\Program Files\Stata18\StataMP-64.exe' \
  -ArgumentList '/e do \"C:\full\absolute\path\to\script.do\"' \
  -WindowStyle Hidden"
```

Key rules:
- **Always use an absolute path** to the do-file: relative paths cause `command E is unrecognized r(199)`
- **`-WindowStyle Hidden`** suppresses the GUI; `/e` alone does not
- **Inner quotes** around the do-file path need backslash-escaping inside the PowerShell string: `\"`

## Monitoring for completion

Stata gives no completion signal to the shell. Poll for an expected output file:

```bash
powershell.exe -Command "
  \$target = 'C:\full\path\to\expected_output_file.tex'
  while (-not (Test-Path \$target)) { Start-Sleep -Seconds 30 }
  Write-Host 'Done'
"
```

Choose the **last file the script writes** as the target, not an early one: a file appearing mid-run will give a false "done" signal.

## Common failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Start-Process: command not found` | Called from bash without `powershell.exe -Command` | Wrap in `powershell.exe -Command "..."` |
| `command E is unrecognized r(199)` | Relative path; Stata read the drive letter as a command | Use full absolute path |
| GUI window appears | `/e` without `-WindowStyle Hidden` | Add `-WindowStyle Hidden` |
| `executable not found` | Wrong Stata edition name | Check actual `.exe` name with the `Get-ChildItem` command above |
| Script runs but no output | Globals not set, or wrong working directory inside the do-file | Verify all `global` path definitions at the top of the do-file |

## Laptop / machine portability

If a do-file contains multiple laptop blocks (e.g., `global base "C:\Users\alice\..."` and `global base "C:\Users\bob\..."`), ensure exactly **one block is uncommented** before running. A common pattern is to wrap each block in comments and only activate the one matching the current machine.

## Standalone wrapper scripts

For analyses that are part of a larger pipeline, prefer creating a small standalone do-file that:
1. Sets all globals
2. Loads its own data (does not depend on prior `use` commands in memory)
3. Runs only the analyses needed

This avoids re-running expensive upstream steps. Example structure:

```stata
* my_analysis_wrapper.do
global base   "C:\Users\you\Dropbox\MyProject"
global tables "${base}\Output\Tables"
global figures "${base}\Output\Figures"
cap mkdir "${tables}"
cap mkdir "${figures}"

cd "${base}\Data"
use my_dataset, clear

* ... analysis code ...
```

## Full example

```bash
# Launch silently
powershell.exe -Command "Start-Process \
  -FilePath 'C:\Program Files\Stata18\StataMP-64.exe' \
  -ArgumentList '/e do \"C:\Users\you\Projects\MyStudy\DoFiles\run_analysis.do\"' \
  -WindowStyle Hidden"

# Monitor for the last output file
powershell.exe -Command "
  \$target = 'C:\Users\you\Projects\MyStudy\Output\Tables\main_results.tex'
  while (-not (Test-Path \$target)) { Start-Sleep -Seconds 30 }
  Write-Host 'Analysis complete'
"
```
