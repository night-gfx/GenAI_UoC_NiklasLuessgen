---
name: research-task-workflow
description: Execute this repository's numbered research tasks sequentially on researcher-prepared task branches, track progress in tasks/README.md, run validation, and commit each verified step. Use when asked to execute or resume a research task; stop for independent researcher review after each task.
---

# Research Task Workflow

## 1. Select task

- Read `AGENTS.md`, `proposal.md` and `tasks/README.md` from the repository root.
- Select the single task marked `In Progress`, otherwise the first `Planned`
  task. Stop if selection is ambiguous, a preceding task is not `Completed`, or
  a task is awaiting review. If all are `Completed`, report that no task remains.
- Read the selected specification, including its `GOAL`, `FILES`, `CONSTRAINTS`,
  `STEPS`, `CHECK`, `OUTPUT` and `STOP` sections. Do not execute tasks merely
  because this skill or the task specifications are being edited.
- Derive the expected branch from the filename:
  `tasks/02_prepare_returns.md` means `agent/02_prepare_returns`.

## 2. Verify branch and scope

- Inspect `git branch --show-current`, `git status --short` and staged changes.
- Require the exact expected branch; `main`, detached HEAD and any other branch
  are invalid. Stop and ask the researcher to prepare or switch the branch.
  Do not create, switch or merge branches yourself.
- Confirm accepted predecessor artifacts are present and match their recorded
  metadata. Respect the task's authorized paths and all protected files.
- Preserve unrelated existing changes. Never stage them or commit them. Stop
  if existing edits overlap task work or unrelated changes are already staged
  and cannot safely be separated without modifying the researcher's work.
- Resolve methodological ambiguities with the researcher before dependent work.
  Use installed dependencies; ask before editing `requirements.txt` or `.venv/`.

## 3. Execute steps

- Mark the task `In Progress` in `tasks/README.md` after branch verification.
- Follow `STEPS` in order. When resuming, inspect progress, commits and artifacts
  and rerun relevant checks before continuing; never trust status alone.
- For each step:
  1. Implement only the authorized changes for that step.
  2. Run its relevant checks and applicable researcher-maintained tests without
     modifying those tests. Disable bytecode/cache writes outside allowed paths.
  3. Fix in-scope implementation errors and rerun checks. Never weaken tests,
     loosen tolerances to hide failure or alter methodology without approval.
  4. Save actual check commands and pass/fail/skip results under `tests/agent/`;
     explain absent tests and skips. Record the verified step, artifacts and
     evidence in `tasks/README.md`.
  5. Review `git diff`, stage only explicit authorized paths or isolated hunks,
     inspect `git diff --cached`, and create one descriptive commit for the
     verified step. Report the resulting hash from Git.
- Continue only after the step's checks pass and its commit succeeds. On an
  unresolved failure, leave status `In Progress`, record the blocker and stop.
  Never claim unrun tests passed. Do not automatically reset, stash or discard
  changes to make a commit possible.

## 4. Finish task

- Run all final `CHECK` requirements and relevant researcher-maintained and
  agent-written tests. Missing researcher tests must be disclosed explicitly.
- Verify required outputs, unchanged raw data and no out-of-scope modifications.
- In the final step's commit, include final check evidence and change status
  to `In Review` in `tasks/README.md`. This is the canonical status for
  **Ready for Review**; do not introduce a second spelling in the status table.
- Report changes, commit hashes, exact checks and outcomes, artifact locations,
  remaining issues and items requiring human verification. Retrieve the final
  commit hash after committing; do not write a self-referential hash into it.

## 5. Human review

- Stop after one task. Do not begin the next task while review is pending.
- The researcher independently reviews the diff and reruns checks, then accepts
  and merges or rejects the task and specifies corrections.
- Only the researcher may mark a task `Completed` and perform merges.
- Do not push or open pull requests without explicit authorization. Never merge
  automatically. A request to execute this workflow does not authorize either.
