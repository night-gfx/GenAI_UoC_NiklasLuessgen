# Research Tasks

Agent task specifications, executed in order, one branch per task.

## Tasks

| Order | Task specification | Purpose | Expected branch | Status |
| --- | --- | --- | --- | --- |
| Step 1 | [01_prepare_weekly_returns.md](01_prepare_weekly_returns.md) | Inspect CSV structure, load and validate daily data, construct and validate weekly excess returns | `agent/01_prepare_weekly_returns` | Planned |
| Step 2 | [02_estimate_beta.md](02_estimate_beta.md) | Estimate market betas with significance tests and build regression table | `agent/02_estimate_beta` | Planned |
| Step 3 | [03_partial_correlation.md](03_partial_correlation.md) | Calculate partial correlations and build descriptive statistics | `agent/03_partial_correlation` | Planned |

## Statuses

- **Planned:** Execution has not started.
- **In Progress:** Execution or corrections are underway; checks may still fail.
- **Ready for Review:** All required checks passed; awaiting researcher review.
- **Completed:** Reviewed and explicitly approved by the researcher; Codex then sets this status.

## Task specification structure

Each task specification is stored in `tasks/NN_task_name.md`, where `NN` is
the execution order from `01` to `03` (e.g. `tasks/01_prepare_weekly_returns.md`).
The expected implementation branch uses the same identifier and task name.

| Section | Meaning |
| --- | --- |
| `GOAL` | Required result when the task is finished. |
| `FILES` | Files allowed to be created or modified; all others are read-only. |
| `CONSTRAINTS` | Inputs, conventions and required functions. |
| `CHECK` | Check commands and success criteria. |
| `OUTPUT` | Branch, commits and final handoff. |
| `STOP` | Conditions for stopping or asking the researcher. |
