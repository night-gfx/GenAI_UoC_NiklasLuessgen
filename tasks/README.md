# Research Tasks

| Order | Task specification | Purpose | Expected branch | Status |
| --- | --- | --- | --- | --- |
| 01 | [01_prepare_weekly_returns.md](01_prepare_weekly_returns.md) | Inspect CSV structure, load and validate daily data, construct and validate weekly excess returns | `agent/01_prepare_weekly_returns` | Planned |
| 02 | [02_estimate_beta.md](02_estimate_beta.md) | Estimate utilities and technology market betas | `agent/02_estimate_beta` | Planned |
| 03 | [03_partial_correlation.md](03_partial_correlation.md) | Calculate market-adjusted correlations | `agent/03_partial_correlation` | Planned |
| 04 | [04_results.md](04_results.md) | Generate comparison table and final checks | `agent/04_results` | Planned |

## Workflow

Execute Tasks 01–04 in order. Each task requires researcher-approved completion
of all preceding tasks before implementation begins.

Task 01, [Prepare weekly returns](01_prepare_weekly_returns.md), specifies a
Python script that loads and validates daily data, calculates weekly excess
returns and generates `output/weekly_returns.csv` after validation. Its CHECK
criteria define completion; no prescribed STEPS sequence is required.

Task 02 uses the validated weekly sample to estimate betas and save residuals.
Task 03 uses those residuals to calculate market-adjusted correlations.
Task 04 assembles the comparison table and checks reproducibility of the complete
pipeline, including data preparation through `code/prepare_returns.py`.

Before implementation, resolve the protected generated-data destinations and
the path conventions shared with the workflow skill, as specified in the combined
task. Editing these specifications on `main` does not start or complete analysis.

## Statuses

- **Planned:** Execution has not started.
- **In Progress:** Execution or corrections are underway; checks may still fail.
- **Ready for Review:** All required checks passed; awaiting researcher review.
- **Completed:** Reviewed and explicitly approved by the researcher; Codex then sets this status.

## Task specification structure

Each task specification is stored in `tasks/NN_task_name.md`, where `NN` is
the execution order from `01` to `04` (e.g. `tasks/01_prepare_weekly_returns.md`).
The expected implementation branch uses the same identifier and task name.

| Section | Meaning |
| --- | --- |
| `GOAL` | Required result when the task is finished. |
| `FILES` | Files allowed to be created or modified, read-only inputs and expected branch. |
| `CONSTRAINTS` | Required conventions, inputs and methodological restrictions. |
| `STEPS` | Optional implementation sequence; Task 01 uses CHECK criteria instead. |
| `CHECK` | Check commands and success criteria. |
| `OUTPUT` | Required artifacts, commits and final handoff. |
| `STOP` | Conditions for stopping or asking the researcher. |
