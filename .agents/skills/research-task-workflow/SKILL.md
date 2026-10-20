---
name: research-task-workflow
description: Execute or resume one research task on its researcher-prepared branch, validate and commit each step, and stop for researcher review.
---

# Research Task Workflow

All datasets are stored directly in `data/`, without subfolders. The researcher
authorizes task-specified processed files there as an explicit exception to
the path restrictions in `AGENTS.md`. The originals
`data/12_Industry_Portfolios_Daily.csv`, `data/F-F_Research_Data_Factors_daily.csv`
and `data/README.md` remain read-only.

## 1. Select Task

- Read `proposal.md` for an overview of the research project.
- Read `tasks/README.md` for the separate execution tasks, their order,
  statuses and task specification structure.
- Select the task marked `In Progress`, or the first `Planned` task.
- Read the corresponding task specification in `tasks/` (e.g. `tasks/02_prepare_returns.md`).

## 2. Verify Branch

- Check the branch: `git branch --show-current`.
- Require `agent/<task-name>`; for example, `tasks/02_prepare_returns.md`
  requires `agent/02_prepare_returns`. Reject `main` and detached HEAD.
- Otherwise, stop and ask the researcher to switch branches. Do not create
  or switch branches yourself.
- Inspect changes: `git status --short` and `git diff --cached`.
  Preserve unrelated changes; stop on overlapping edits or existing staged changes.

## 3. Execute Steps of Task

- Mark the task `In Progress` in `tasks/README.md` after branch verification.
- Execute the `STEPS` in the task specification (`tasks/`) sequentially.

After each step of the task:

1. **Self-check:** The executing agent reviews its own work and runs the
   required checks using `.venv/bin/python`. Run relevant agent and researcher
   tests with `-B -m pytest -p no:cacheprovider`. Fix in-scope errors and rerun
   checks. If unresolved, log the blocker, leave `In Progress` and stop.

2. **Log:** Record actions and actual check results in `logs/<task-name>.md`
   using the table below, with one row per check. Include failures and explain skips.

   | UTC time | Step | Actions / changed paths | Exact check command | Result / evidence |
   | --- | --- | --- | --- | --- |
   | YYYY-MM-DD HH:MM | Step number | Action and file paths | `command` | PASS / FAIL / SKIP; exit code; output path or skip reason |

3. **Commit:** After successful checks, commit only the verified step's files
   using the commands below. **Codex must explicitly set itself as the author:
   `Codex <codex@openai.com>`.** Verify the recorded author after committing.

   Replace the example file list and commit message with the current step's values:

   ```bash
   git diff --check
   git diff
   git add -- 'path/to/changed-file' 'logs/<task-name>.md' tasks/README.md
   git diff --cached
   git commit --author='Codex <codex@openai.com>' -m '<task-name>: step <n> - <description>'
   git log -1 --format='%H %an <%ae>'
   ```

   **Create local commits only. Do not push, open pull requests or merge.**
   Never stage unrelated files or use `git add .`. For the final step, complete
   section 4 before committing so its results and final status share that commit.

## 4. Final Agent Review

- Run all final `CHECK` requirements in the task specification (`tasks/`).
- Update the task status in `tasks/README.md` to `Ready for Review`.
- Record final results in `logs/<task-name>.md` and commit using section 3.

## 5. Researcher Review

- The researcher independently reviews the diff and reruns checks, then accepts and merges or rejects the task and specifies corrections.
- After explicit researcher approval, Codex sets the task status in
  `tasks/README.md` to `Completed`. Never set it before approval.
- Only the researcher performs merges.
- Stop after one task. Do not push, open pull requests or merge automatically.