# Research Tasks

| Order | Task specification | Purpose | Expected branch | Status |
| --- | --- | --- | --- | --- |
| 01 | [01_collect_data.md](01_collect_data.md) | Verify sources and freeze input inventory | `agent/01_collect_data` | Planned |
| 02 | [02_prepare_returns.md](02_prepare_returns.md) | Construct aligned weekly excess returns | `agent/02_prepare_returns` | Planned |
| 03 | [03_estimate_beta.md](03_estimate_beta.md) | Estimate utilities and technology market betas | `agent/03_estimate_beta` | Planned |
| 04 | [04_partial_correlation.md](04_partial_correlation.md) | Calculate market-adjusted correlations | `agent/04_partial_correlation` | Planned |
| 05 | [05_results.md](05_results.md) | Generate comparison table and final checks | `agent/05_results` | Planned |

## Statuses

- **Planned:** Execution has not started.
- **In Progress:** Execution or corrections are underway; checks may still fail.
- **Ready for Review:** All required checks passed; awaiting researcher review.
- **Completed:** Reviewed and explicitly approved by the researcher; Codex then sets this status.

## Task specification structure

Each task specification is stored in `tasks/NN_task_name.md`, where `NN` is
the execution order (e.g. `tasks/02_prepare_returns.md`).

| Section | Meaning |
| --- | --- |
| `GOAL` | Required result when the task is finished. |
| `FILES` | Files allowed to be created or modified, read-only inputs and expected branch. |
| `CONSTRAINTS` | Required conventions, inputs and methodological restrictions. |
| `STEPS` | Ordered implementation and validation steps. |
| `CHECK` | Check commands and success criteria. |
| `OUTPUT` | Required artifacts, commits and final handoff. |
| `STOP` | Conditions for stopping or asking the researcher. |
