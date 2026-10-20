# Task 02: Estimate Market Betas

## GOAL

Implement Python code (`code/estimate_beta.py`) with separate functions to load the weekly excess returns from Task 01 (`output/weekly_returns.csv`) and estimate utilities and technology market betas by OLS for the full sample and all eight predefined comparison periods. After the OLS, the script must save:

- **Regression table** (`output/regression_table.xlsx`), formatted as the proposal's Regression Table: betas as `estimate (SE)` with stars, R² and N, rounded to 3 decimals, with the proposal's table note.
- **Regression statistics** (`output/regression_statistics.csv`), unrounded, one row per period: `period`, `n_obs`, `first_week`, `last_week`, `hac_lags`, `alpha_U`, `se_alpha_U`, `beta_U`, `se_beta_U`, `t_beta_1_U`, `p_beta_1_U`, `r_squared_U`, `residual_std_U`, the same for `_T`, `vol_U`, `vol_T`, `vol_M`, `corr_UM`, `corr_TM`, `corr_UT`.
- **Residuals** (`output/market_residuals.csv`), one row per `(period, week_end)`: `utilities_residual`, `technology_residual`, `market_excess`.

## FILES

- **`code/`:** May add/edit only the task's own file, `code/estimate_beta.py`. All other contents are read-only.
- **`logs/`:** May add/edit `logs/02_estimate_beta.md` to record all other results, execution and check logs.
- **All others:** Read-only for direct edits. Only running the Python script may create or update the three output files; the LLM must not write them directly.

## CONSTRAINTS

**Inputs:** `output/weekly_returns.csv` from Task 01 (`week_end`, `utilities_excess`, `technology_excess`, `market_excess`; source percent units: `0.02 = 0.02%`); periods exactly as in the [proposal](../proposal.md). Task 01 must be `Completed`. Excel output requires `openpyxl` in `requirements.txt` (researcher-approved).

**Conventions:** Keep percent units and full precision. Confirm the period assignment rule (e.g. by `week_end`) before estimation. Fit `sector_excess = alpha + beta * market_excess + epsilon` separately for utilities and technology, refitted in every period on the same weeks. Standard errors: Newey–West (HAC) with `hac_lags = floor(4 * (n_obs / 100) ** (2 / 9))`, with a simple two-sided t-test of `beta = 1` (`t = (beta - 1) / se_beta`, normal distribution) and stars `*` p < 0.10, `**` p < 0.05, `***` p < 0.01 (stars only in the Excel table). Volatilities: weekly standard deviations (`ddof = 1`), not annualized; correlations: Pearson. No other factors, estimators, rolling windows or causal claims. Do not drop or fill data without approval; log unresolved errors, stop and ask.

| Function | Description | Failure |
| --- | --- | --- |
| `main ()` | Run load → OLS → format → save. | A function fails. |
| `load_weekly_returns (weekly_path)` | Read the weekly returns and return them keyed by `(period, week_end)`: each week in its subperiod, plus all weeks as Full Sample. | File cannot be read; unassigned, overlapping or empty periods. |
| `run_ols (weekly_periods)` | Fit both regressions per period, calculate all statistics and return `(regression_statistics, residuals)`. | Zero variance, singular design or nonfinite results. |
| `format_regression_table (regression_statistics)` | Return the proposal's Regression Table (nine rows in proposal order). | Missing or invalid columns. |
| `save_results (regression_table, regression_statistics, residuals, output_dir)` | Write the regression table as Excel and the statistics and residuals as CSV, without a row index. | Invalid output path or write error. |

## CHECK

**Input**

- **Data file exists:** `output/weekly_returns.csv` exists and is read correctly.

**Output**

- **Periods:** Nine rows in proposal order; each week in exactly one subperiod; subperiod `n_obs` sum to the Full Sample.
- **Calculation:** `beta` matches `Cov / Var` and `corr_SM * vol_S / vol_M`; `r_squared = corr_SM ** 2`; HAC standard errors match an independent Newey–West calculation; `t_beta_1 = (beta - 1) / se_beta` and p-values are consistent; synthetic data recover known coefficients (declared tolerances).
- **Residuals:** Residuals reconstruct `sector_excess - alpha - beta * market_excess`, have mean near zero, are orthogonal to `market_excess` and match `residual_std`.
- **Regression table:** Values in the Excel table match the unrounded CSV after rounding; stars match `p_beta_1`.
- **File output:** Running `.venv/bin/python -B code/estimate_beta.py` creates the three files.

## OUTPUT

- **Branch:** Work only on `agent/02_estimate_beta`; do not push or merge.
- **Commits:** One descriptive commit per completed step (e.g. loading, OLS, regression table, saving).
- **Final message:** Summarize code changes, CHECK results, open issues and items for researcher verification; list the commit hashes and report `Ready for Review`.

## STOP

- **Done:** Stop when all CHECK criteria pass.
- **Step limit:** Stop and report after 5 commits without passing CHECK.
- **Ask first:** Stop and ask if a read-only file would have to change, Task 01 is not `Completed`, `openpyxl` is missing, or on unclear methodology or period assignment.
