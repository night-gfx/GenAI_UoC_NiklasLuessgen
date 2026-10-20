# Research tasks

Execute the tasks below in order, following [proposal.md](../proposal.md),
[AGENTS.md](../AGENTS.md), and the
[research-task-workflow skill](../.agents/skills/research-task-workflow/SKILL.md).
This index plans execution; no research task has been executed by creating it.

| Order | Specification | Purpose | Expected branch | Status | Last verified step |
| --- | --- | --- | --- | --- | --- |
| 01 | [01_collect_data.md](01_collect_data.md) | Verify the existing source data and freeze the input inventory | `agent/01_collect_data` | Planned | — |
| 02 | [02_prepare_returns.md](02_prepare_returns.md) | Construct and align weekly excess returns | `agent/02_prepare_returns` | Planned | — |
| 03 | [03_estimate_beta.md](03_estimate_beta.md) | Estimate utilities and technology market betas | `agent/03_estimate_beta` | Planned | — |
| 04 | [04_partial_correlation.md](04_partial_correlation.md) | Calculate market-adjusted correlations | `agent/04_partial_correlation` | Planned | — |
| 05 | [05_results.md](05_results.md) | Generate the comparison table and final checks | `agent/05_results` | Planned | — |

## Status and review

- **Planned:** Execution has not started.
- **In Progress:** The agent is executing the task on its expected branch.
- **In Review:** All task checks passed; equivalent to **Ready for Review**.
  The agent stops here for independent researcher review.
- **Completed:** The researcher reviewed and accepted the task. Only the
  researcher may set this status.

Transitions: `Planned → In Progress → In Review → Completed`.
After rejection, the researcher may return a task to `In Progress` and record
the requested corrections. Failed checks leave a task `In Progress`, with the
failure recorded; they never justify `In Review`.

Select the single `In Progress` task, otherwise the first `Planned` task.
All earlier tasks must be `Completed` before execution begins. A task awaiting
review blocks subsequent tasks. Stop if more than one task is `In Progress`.
The researcher prepares each expected branch from the accepted predecessor
state; the agent verifies it and does not create, switch, or merge branches.

## Progress log

Append an entry after every verified step and for any blocker. Include task and
step IDs, date, artifacts changed, exact check commands, actual outcomes and
test-log paths. Record passed, failed and skipped checks separately; explain
skips. Each completed step has one descriptive commit containing its progress
update. Obtain commit hashes from Git for the handoff; do not attempt to embed
a commit's own hash inside that commit.

| Date | Task / step | Work and checks | Outcome / evidence |
| --- | --- | --- | --- |
| — | — | No research execution yet | — |

## Execution conventions

- Run commands from the repository root using `.venv/bin/python`.
- Every task contains `GOAL`, `FILES`, `CONSTRAINTS`, `STEPS`, `CHECK`, `OUTPUT`,
  and `STOP`. Step checks and final checks must pass before advancing.
- Test files and analysis scripts named in the specifications are deliverables
  to implement during execution; they are not supplied by this task setup.
- Save all agent check outputs under `tests/agent/`. Run relevant tests under
  `tests/researcher/` without modifying them or writing caches there. Report
  explicitly when no researcher tests exist; this is not a passed test suite.
- Use the currently approved dependencies. Request authorization before changing
  `requirements.txt` or installing packages into the protected `.venv/`.
- Final research tables belong in `data/adjusted/results/` under the current
  permissions. Writing to `output/` requires separate researcher authorization.
- No automatic push, pull request, merge, or transition to `Completed`.
