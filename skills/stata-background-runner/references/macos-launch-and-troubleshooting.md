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

Use an absolute path to the console executable and a writable working directory. Use a fresh run directory only if the do-file does not depend on relative paths from a project directory. Otherwise run from its required project directory, check that the batch log name will not overwrite an existing file, and preserve any existing log before launch. An isolated project copy or a wrapper may be appropriate only when it preserves the analysis's input and output semantics. Run the example in bash. Supply literal double quotes *inside* the do-file argument: on Stata/MP tested on macOS, ordinary shell quoting alone passes the path as one OS argument but Stata still splits a path containing spaces.

```sh
stata_exe='/path/discovered/on/this/mac/stata-mp'
do_file='/absolute/path with spaces/analysis.do'
run_dir='/absolute/path/to/required-working-directory'
launcher_log='/absolute/path/to/new/launcher-output.txt'
# Stata parses macros after shell parsing. Reject paths requiring separate handling.
case "$do_file" in
  *'"'*|*'$'*|*'`'*|*"'"*|*$'\n'*|*$'\r'*)
    printf 'Unsupported do-file path characters; resolve safely before launch.\n' >&2
    exit 1 ;;
esac
# Atomically create a new launcher log; never truncate an existing file.
( set -C; : > "$launcher_log" ) 2>/dev/null || { printf 'Launcher log exists or cannot be created.\n' >&2; exit 1; }
cd "$run_dir" || exit 1
"$stata_exe" -b do "\"$do_file\"" > "$launcher_log" 2>&1 &
stata_pid=$!
printf 'Stata PID: %s\n' "$stata_pid"
# Poll for at most 60 seconds; adjust the deadline for the task.
deadline=$((SECONDS + 60))
while kill -0 "$stata_pid" 2>/dev/null && [ "$SECONDS" -lt "$deadline" ]; do
  sleep 1
done
if kill -0 "$stata_pid" 2>/dev/null; then
  printf 'Still running; PID: %s\n' "$stata_pid"
else
  wait "$stata_pid"
  printf 'Process exit status: %s\n' "$?"
fi
```

The batch log normally uses the do-file's basename with `.log` in the working directory. Verify its actual location and inspect it after the process exits. Keep the shell alive to use `wait`; if the controlling shell may end, use a managed persistent job or `nohup` and preserve the PID and logs. A PID alone can be reused after a process exits, so use the original process handle when available.

`-b` invokes the console batch mode and writes a text log. Do not assume that GUI application flags, foreground behavior, or exit statuses are identical to the console executable. The process status is supplemental evidence: this Mac's Stata returned zero for a failed do-file. Inspect the log and validate the intended results. Do not rely on `end of do-file` alone, since it may appear after an error.

## Troubleshooting

- **Executable missing:** search the actual installation location and use the console binary, not a hard-coded Stata version or edition.
- **`file ... not found` with a space in the path:** confirm that literal quotes reach Stata, not only the shell. Stata also interprets macro delimiters such as `$` and backticks in paths. The example rejects those characters, quotes, and line breaks rather than risk executing a different file. Resolve such paths with a tested Stata-safe encoding or a safely named wrapper, and preserve path-dependent behavior; do not silently copy or rename research files.
- **No log or permission error:** check the working directory, executable, license availability, and the launcher log; avoid exposing license information.
- **Log reports an error:** fix the underlying input, package, working directory, or do-file problem, then rerun with a fresh log while preserving the required working directory. Caught errors may be intentional and require contextual inspection.
- **Job still running:** report its PID and log; do not treat an existing output as completion or terminate a user's job without authorization.
