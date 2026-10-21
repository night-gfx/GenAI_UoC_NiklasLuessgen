# The Changing Defensive Role of U.S. Utilities During the AI Boom

Has the defensive role of U.S. utility stocks changed during the AI boom? The project compares utilities' market beta and their market-adjusted correlation with technology stocks during the AI boom with the period since 1990 before it. Research design: [proposal.md](proposal.md).

## Data

Kenneth French Data Library, daily: 12 industry portfolios (`Utils`, `BusEq`) and Fama–French factors (`Mkt-RF`, `RF`). Details: [data/README.md](data/README.md).

## Reproduce Workflow

- **Start:** Invoke `$research-task-workflow` in Codex.
- **Tasks:** The skill reads `tasks/README.md` and executes one pending task per invocation (`agent/<task>`), in order 01–04, on its prepared branch.
- **Checks:** Codex validates results, logs checks, commits changes, and marks the task `Ready for Review`.
- **Approval:** The researcher reviews the code and independently tests inputs and outputs before merging. After approval, Codex marks the task `Completed`; invoke the skill again for the next task.

## Execution of Scripts

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Run in order; results are written to `output/`.

| Step | Script | Output |
| --- | --- | --- |
| 1 | `code/prepare_returns.py` | `weekly_returns.csv` |
| 2 | `code/estimate_beta.py` | `regression_table.xlsx`, `regression_statistics.csv`, `market_residuals.csv` |
| 3 | `code/partial_correlation.py` | `descriptive_statistics.xlsx`, `partial_correlations.csv` |
| 4 | `code/hypothesis_tests.py` | `hypothesis_tests.xlsx`, `hypothesis_tests.csv` |

```bash
.venv/bin/python -B code/prepare_returns.py
```

## AI Use Statement

- **Model:** GPT-6.1 with medium reasoning effort.
- **Tool:** Codex, used for code implementation, automated checks, and documentation under researcher review.
