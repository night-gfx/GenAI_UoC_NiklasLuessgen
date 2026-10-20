---
name: research-task-workflow
description: Execute or resume one research task on its researcher-prepared branch, validate and one commit per step, and stop for researcher review.
---

# Research Task Workflow

## 1. Select Task

- **Project:** Read `proposal.md` for an overview of the research project.
- **Task overview:** Read `tasks/README.md` for the separate execution tasks, their order,
  statuses and task specification structure.
- **Selection:** Select the task marked `In Progress`, or the first `Planned` task.
- **Specification:** Read the corresponding task specification in `tasks/` (e.g. `tasks/02_prepare_returns.md`).

## 2. Verify Branch

- **Branch check:** Check the branch: `git branch --show-current`.
- **Required branch:** Require `agent/<task-name>`; for example, `tasks/02_prepare_returns.md`
  requires `agent/02_prepare_returns`. Reject `main` and detached HEAD.
- **Branch mismatch:** Otherwise, stop and ask the researcher to switch branches. Do not create
  or switch branches yourself.
- **Working tree:** Inspect changes: `git status --short` and `git diff --cached`.
  Preserve unrelated changes; stop on overlapping edits or existing staged changes.

## 3. Task Execution

- **Execution:** After branch verification, mark the task `In Progress` in
  `tasks/README.md`. Follow its GOAL, FILES, CONSTRAINTS, CHECK, OUTPUT and STOP.

- **Files:** Save scripts in `code/`, and generated results in
  `output/`. Name the main script after the task file, replacing `.md` with `.py`.

- **Log:** Maintain one chronological record in `logs/<task-name>.md`, covering
  the task conversation, actions, decisions with brief reasons, changed files,
  execution/check commands, results, failures and fixes.

- **Self-check:** Review your work and run required checks using `.venv/bin/python`.
  Fix in-scope errors and rerun checks. If unresolved, log the blocker, leave
  `In Progress` and stop.

- **Commits:** Create one local commit per successfully checked step. Set the
  author to `Codex <codex@openai.com>` and verify it after committing. Stage only
  task-related files; never use `git add .`. Do not push, open pull requests or
  merge. Complete section 4 before the final commit so its results and final
  status share that commit. Adapt the file list and description below:

  ```bash
  git diff --check
  git diff
  git add -- 'path/to/changed-file' 'logs/<task-name>.md' tasks/README.md
  git diff --cached
  git commit --author='Codex <codex@openai.com>' -m '<task-name>: <description>'
  git log -1 --format='%H %an <%ae>'
  ```

## 4. Final Agent Review

- **Final checks:** Run all final `CHECK` requirements in the task specification (`tasks/`).
- **Results:** Save final results in `output/<task-name>.<extension>`, using the file type
  required by the task; for example, `output/01_collect_data.json`. If there
  are several result files, add a short name after the task name, such as
  `output/01_collect_data_source_inventory.json`.
- **Final log:** Complete `logs/<task-name>.md` with the final check results, output paths,
  remaining issues and items for researcher review.
- **Review status:** Only if all required checks pass, update the task status in
  `tasks/README.md` to `Ready for Review`.
- **Final commit:** Commit the verified files and final log using section 3. Do not stage
  generated files in `output/`, which is ignored by Git.

## 5. Researcher Review

- **Independent review:** The researcher independently reviews the diff and compares to its checks ("first check, then delegate"), then accepts and merges or rejects the task and specifies corrections.
- **Approval:** After explicit researcher approval, Codex sets the task status in
  `tasks/README.md` to `Completed`. Never set it before approval.
- **Merge authority:** Only the researcher performs merges.
- **Stop:** Stop after one task. Do not push, open pull requests or merge automatically.
