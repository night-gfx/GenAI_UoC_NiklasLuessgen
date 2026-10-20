# The Changing Defensive Role of U.S. Utilities During the AI Boom

Has the defensive role of U.S. utility stocks changed during the AI boom? The project compares utilities' market beta and their market-adjusted correlation with technology stocks during the AI boom with the period since 1990 before it. Research design: [proposal.md](proposal.md).

## Data

Kenneth French Data Library, daily: 12 industry portfolios (`Utils`, `BusEq`) and Fama–French factors (`Mkt-RF`, `RF`). Details: [data/README.md](data/README.md).

## Method

Weekly excess returns from January 1990 to 31 August 2026, nine predefined comparison periods. Per period: OLS market betas with Newey–West standard errors (test of β = 1) and partial correlations from regression residuals.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Execution

Run in order; results are written to `output/`.

| Step | Script | Output |
| --- | --- | --- |
| 1 | `code/prepare_returns.py` | `weekly_returns.csv` |
| 2 | `code/estimate_beta.py` | `regression_table.xlsx`, `regression_statistics.csv`, `market_residuals.csv` |
| 3 | `code/partial_correlation.py` | `descriptive_statistics.xlsx`, `partial_correlations.csv` |

```bash
.venv/bin/python -B code/prepare_returns.py
```

## Structure

| Path | Content |
| --- | --- |
| `code/` | Analysis scripts |
| `data/` | Raw data (read-only) |
| `output/` | Generated tables (not tracked by Git) |
| `tasks/` | Agent task specifications and status ([tasks/README.md](tasks/README.md)) |
| `logs/` | Task execution logs |
| `literature/` | Literature matrix and PDFs |

## Workflow

Scripts are implemented by an AI agent, one task per branch (`agent/<task>`), following [AGENTS.md](AGENTS.md) and the [research-task-workflow skill](.agents/skills/research-task-workflow/SKILL.md). The researcher reviews and merges.
