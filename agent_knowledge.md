# Agent Knowledge & Guidelines

## Windows & CLI Environment: OpenSpec CLI execution
- **Constraint / Issue**: Running `bash -c "openspec ..."` on Windows resolves to the WSL launcher (`C:\Windows\System32\bash.exe`). If Node.js is installed on Windows but not inside the WSL environment, this command will fail with `node: not found` errors.
- **Actionable Guideline**: Always invoke Git Bash explicitly when executing OpenSpec or node-based commands that need to access the Windows environment:
  ```powershell
  & 'C:\Program Files\Git\bin\bash.exe' -c "openspec <command>"
  ```
- **Constraint / Issue**: Double quotes nested inside double quotes in PowerShell commands passed to `run_command` (e.g. `... -c "openspec new change \"name\""`) will fail with parser errors such as `unexpected EOF while looking for matching '"'`.
- **Actionable Guideline**: Use single quotes around the outer command string when executing nested command lines in PowerShell, e.g.:
  ```powershell
  & 'C:\Program Files\Git\bin\bash.exe' -c 'openspec status --change "integrate-mpu6050"'
  ```
- **Temporary Files**: Remember to redirect JSON output files to the `.scratch/` directory (never the project root) and use `view_file` to read them to prevent encoding/truncation errors.

## Git Version Control Routine
- **Constraint / Issue**: Modifying code without committing existing functional changes can lead to cluttered diffs, lost progress, or difficulties in tracking changes.
- **Actionable Guideline**: Before implementing a new feature, proposing a plan, or making any changes to files:
  1. The agent MUST check the status of the repository (`git status` or inspect the files).
  2. If there are uncommitted changes, the agent MUST explicitly remind the user of these pending changes and suggest making a git commit before starting the new task.
  3. The agent can recommend using the Conventional Commits conventional style or the `git-commit` skill.

## ESP32 Serial REPL & Uploading (USB CDC)
- **Constraint / Issue**: ESP32-S3 Native USB CDC ports do not respond to `mpremote` or standard raw REPL attempts if DTR/RTS are disabled or if the board is running a tight `uasyncio` loop.
- **Actionable Guideline**: Always open the serial port with `dtr=True` and `rts=True`, spam `\x03` (Ctrl-C) to break execution, then send `\x01` (Ctrl-A) for Raw REPL. Write files in base64 chunks (`ubinascii.a2b_base64`) to prevent memory allocation errors on target.

## MicroPython Async OTA Updates
- **Constraint / Issue**: Running `urequests.get()` for HTTPS raw GitHub files inside an active Microdot HTTP handler causes memory allocation failures (RAM exhaustion) due to SSL socket buffers.
- **Actionable Guideline**: Always trigger OTA updates asynchronously via `asyncio.create_task()` with a delay (`await asyncio.sleep(1)`), allowing Microdot to complete HTTP response sending and perform `gc.collect()` before initiating HTTPS requests.


