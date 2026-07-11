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

