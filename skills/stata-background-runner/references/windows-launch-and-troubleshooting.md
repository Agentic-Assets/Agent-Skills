# Windows batch execution

## Discover the executable

In PowerShell, check an explicit user-provided executable first, then `Get-Command StataMP-64.exe, StataSE-64.exe, StataBE-64.exe, StataIC-64.exe -ErrorAction SilentlyContinue`. If needed, inspect Stata installation folders under both `$env:ProgramFiles` and `${env:ProgramFiles(x86)}`, as well as the user's custom install location. Names and versions vary. Select the intended licensed edition when several exist; do not assume `C:\Program Files\Stata18` or print license information.

## Launch and monitor

Use native PowerShell syntax from PowerShell. From bash, invoke a `.ps1` file with `powershell.exe -NoProfile -File ...` (or `pwsh` if installed); do not paste PowerShell cmdlets directly into bash. The following is a PowerShell example; substitute discovered absolute paths and a writable working directory. Use a fresh directory only if the analysis does not depend on a project working directory; otherwise use the required directory and check for a batch-log collision before launching:

```powershell
$stataExe = 'C:\path\discovered\StataMP-64.exe'
$doFile = 'C:\absolute path\analysis.do'
$runDir = 'C:\absolute path\new-run-directory'
# Reject Stata macro delimiters and quotes until the path is safely handled.
if ($doFile -match '[`$"'']|[\r\n]') { throw 'Unsupported do-file path characters; resolve safely before launch.' }
# Start-Process joins ArgumentList, so the literal quotes protect spaces for Stata.
$arguments = '/e do "{0}"' -f $doFile
$process = Start-Process -FilePath $stataExe -ArgumentList $arguments `
    -WorkingDirectory $runDir -WindowStyle Hidden -PassThru
"Stata PID: $($process.Id)"
# Wait at most one hour; the process is left running on timeout.
if ($process.WaitForExit(3600000)) {
    $process.Refresh()
    "Process exit status: $($process.ExitCode)"
} else {
    "Still running; PID: $($process.Id)"
}
```

Stata's `/e` batch mode exits without the `/b` completion dialog. `-WindowStyle Hidden` requests a hidden window; GUI behavior can differ by environment and should be verified locally. The batch log normally has the do-file basename and `.log` in the working directory. Check the actual log and expected results after process exit; process status alone is not reliable proof of analysis success. Keep logs private because their headers may contain license information.

## Troubleshooting and portability

- **Executable not found:** discover the actual installed edition and version, including custom locations.
- **Path errors:** ensure literal quotes reach Stata around paths containing spaces; `Start-Process` joins argument arrays into a command line. Stata macro delimiters such as `$` and backticks, quotes, and line breaks require separate handling: use a tested Stata-safe encoding or a safely named wrapper that preserves path-dependent behavior.
- **No log or `r(608)`:** use a writable working directory; do not launch with the protected installation directory as the working directory.
- **Unexpected output location or missing inputs:** inspect the do-file's `cd`, globals, dependencies, and machine-specific paths. Resolve paths for the current machine instead of blindly enabling a different user's block.
- **Errors in log:** inspect context, including intentionally captured errors, and rerun with a fresh log after fixing the cause, preserving the required working directory. An early output or `end of do-file` is not a success signal.
- **Job still running:** retain its process ID and log; do not terminate it without authorization. If a process handle is lost, PID reuse limits what a later PID check can prove.
