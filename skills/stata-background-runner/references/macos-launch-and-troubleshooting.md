# macOS batch execution

## Discover the executable

First check `command -v stata-mp`, `stata-se`, `stata-be`, and `stata`. If none is on PATH, inspect installed applications, including versioned directories and `/Applications/StataNow`. For example:

```sh
find /Applications "$HOME/Applications" -type f \
  \( -name stata-mp -o -name stata-se -o -name stata-be -o -name stata \) \
  -path '*/Contents/MacOS/*' -print 2>/dev/null
```

These are console executables inside app bundles. Installations can also be elsewhere: check the user's chosen location if discovery finds nothing. If multiple candidates exist, identify the intended version and edition. Do not print license files or license details from logs.

## Launch and monitor

Use an absolute path to the console executable and a writable, run-specific working directory. Supply literal double quotes *inside* the do-file argument: on Stata/MP tested on macOS, ordinary shell quoting alone passes the path as one OS argument but Stata still splits a path containing spaces.

```sh
stata_exe='/path/discovered/on/this/mac/stata-mp'
do_file='/absolute/path with spaces/analysis.do'
run_dir='/absolute/path/to/new/run-directory'
cd "$run_dir" || exit 1
"$stata_exe" -b do "\"$do_file\"" > launcher.out 2>&1 &
stata_pid=$!
printf 'Stata PID: %s\n' "$stata_pid"
# In the same shell, wait when ready; for long jobs poll the PID with a timeout.
wait "$stata_pid"
printf 'Process exit status: %s\n' "$?"
```

The batch log normally uses the do-file's basename with `.log` in the working directory. Verify its actual location and inspect it after the process exits. Keep the shell alive to use `wait`; if the controlling shell may end, use a managed persistent job or `nohup` and preserve the PID and logs. A PID alone can be reused after a process exits, so use the original process handle when available.

`-b` invokes the console batch mode and writes a text log. Do not assume that GUI application flags, foreground behavior, or exit statuses are identical to the console executable. The process status is supplemental evidence: this Mac's Stata returned zero for a failed do-file. Inspect the log and validate the intended results. Do not rely on `end of do-file` alone, since it may appear after an error.

## Troubleshooting

- **Executable missing:** search the actual installation location and use the console binary, not a hard-coded Stata version or edition.
- **`file ... not found` with a space in the path:** confirm that literal quotes reach Stata, not only the shell. Paths containing a literal double quote need separate handling; use a safely named temporary wrapper or relocate a copy with permission.
- **No log or permission error:** check the working directory, executable, license availability, and `launcher.out`; avoid exposing license information.
- **Log reports an error:** fix the underlying input, package, working directory, or do-file problem, then rerun in a fresh directory. Caught errors may be intentional and require contextual inspection.
- **Job still running:** report its PID and log; do not treat an existing output as completion or terminate a user's job without authorization.
