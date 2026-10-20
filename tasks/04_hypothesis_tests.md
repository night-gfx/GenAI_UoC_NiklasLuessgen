# Task 04: Test Hypotheses

## GOAL

Implement Python code (`code/hypothesis_tests.py`) with separate functions to load the results of Tasks 01–03 and test H1–H3 as specified in the proposal. The script must save:

- **Hypothesis tests table** (`output/hypothesis_tests.xlsx`), formatted as the proposal's Hypothesis Tests table: estimate, test statistic, one-sided p-value and N (Full Sample weeks for H1 and H2, `n_obs_bai + n_obs_ai` for H3) for H1a, H1b, H2 and H3, rounded to 3 decimals, with the proposal's table note.
- **Hypothesis test statistics** (`output/hypothesis_tests.csv`), unrounded, one row per hypothesis: `hypothesis`, `estimate`, `std_error`, `test_statistic`, `p_value_one_sided`, `n_obs`, `n_obs_bai`, `n_obs_ai`, `hac_lags`.

## FILES

- **`code/`:** May add/edit only the task's own file, `code/hypothesis_tests.py`. All other contents are read-only.
- **`tasks/README.md`:** May update only this task's status.
- **`logs/`:** May add/edit `logs/04_hypothesis_tests.md` to record all other results, execution and check logs.
- **All others:** Read-only for direct edits. Only running the Python script may create or update the two output files; the LLM must not write them directly.

## CONSTRAINTS

**Inputs:** `output/weekly_returns.csv` (Task 01), `output/regression_statistics.csv` (Task 02) and `output/partial_correlations.csv` (Task 03); periods exactly as in the [proposal](../proposal.md). Tasks 01–03 must be `Completed` and their outputs must exist locally (`output/` is not tracked by Git). Excel output requires `openpyxl`.

**Conventions:** Keep percent units and full precision. Use the same period assignment rule as Task 02 (AI boom from December 2022, Before AI boom through November 2022). All tests are one-sided and use the normal distribution; Newey–West standard errors with a fixed `hac_lags = 4`, as in Task 02.

- **H1:** Take `beta_U`, `se_beta_U`, `beta_T`, `se_beta_T` of the Full Sample from Task 02; `t = (beta - 1) / se_beta`; H1a p-value `Φ(t_U)` (left tail), H1b p-value `1 - Φ(t_T)` (right tail).
- **H2:** On all Full Sample weeks, fit `utilities_excess = alpha + delta * D + beta * market_excess + gamma * (D * market_excess) + epsilon` by OLS, with `D = 1` in AI boom weeks and `0` otherwise; `t = gamma / se_gamma`; p-value `1 - Φ(t)`.
- **H3:** Take the partial correlations of Before AI boom and AI boom from Task 03; `z = atanh(rho)`; `Z = (z_AI - z_BAI) / sqrt(1 / (n_AI - 4) + 1 / (n_BAI - 4))`; estimate `rho_AI - rho_BAI`; p-value `1 - Φ(Z)`.

No other hypotheses, tests, periods or causal claims. Do not change Task 01–03 results; log unresolved errors, stop and ask.

| Function | Description | Failure |
| --- | --- | --- |
| `main ()` | Run load → H1 → H2 → H3 → format → save. | A function fails. |
| `load_inputs (weekly_path, statistics_path, partial_path)` | Read and return `(weekly, regression_statistics, partial_correlations)`. | Files cannot be read; missing periods or columns. |
| `test_h1 (regression_statistics)` | Return the H1a and H1b rows. | Missing Full Sample row, zero or nonfinite standard error. |
| `test_h2 (weekly)` | Fit the dummy regression and return the H2 row. | No weeks in either period, singular design or nonfinite results. |
| `test_h3 (partial_correlations)` | Return the H3 row. | Missing period, `n_obs <= 4` or correlation outside `(-1, 1)`. |
| `format_hypothesis_table (hypothesis_tests)` | Return the proposal's Hypothesis Tests table (four rows in proposal order). | Missing or invalid columns. |
| `save_results (hypothesis_table, hypothesis_tests, output_dir)` | Write the table as Excel and the statistics as CSV, without a row index. | Invalid output path or write error. |

## CHECK

**Input**

- **Data files exist:** All three input files exist and are read correctly; `n_obs` for Full Sample, Before AI boom and AI boom agree across the inputs.

**Output**

- **H1:** `t` matches the Task 02 `t_beta_1` of the Full Sample; each one-sided p-value equals half the Task 02 two-sided `p_beta_1` when `t` lies in the hypothesized direction, and one minus that half otherwise.
- **H2:** `gamma` equals `beta_U(AI boom) - beta_U(Before AI boom)` from Task 02 and `beta` equals `beta_U(Before AI boom)` (declared tolerance); `n_obs` equals the Full Sample; HAC standard errors match an independent Newey–West calculation; synthetic data with a known beta difference are recovered.
- **H3:** `Z` matches an independent hand calculation; identical correlations give `Z = 0`; synthetic data with a known correlation difference give the expected sign.
- **Table:** Four rows in proposal order; values in the Excel table match the unrounded CSV after rounding; all p-values lie in `[0, 1]`.
- **File output:** Running `.venv/bin/python -B code/hypothesis_tests.py` creates both files.

## OUTPUT

- **Branch:** Work only on `agent/04_hypothesis_tests`; do not push or merge.
- **Commits:** One descriptive commit per completed step (e.g. loading, H1, H2, H3, table and saving).
- **Final message:** Summarize code changes, CHECK results, open issues and items for researcher verification; list the commit hashes and report `Ready for Review`.

## STOP

- **Done:** Stop when all CHECK criteria pass.
- **Step limit:** Stop and report after 5 commits without passing CHECK.
- **Ask first:** Stop and ask if a read-only file would have to change, Tasks 01–03 are not `Completed`, their outputs are missing, `openpyxl` is missing, or on unclear methodology or period assignment.
