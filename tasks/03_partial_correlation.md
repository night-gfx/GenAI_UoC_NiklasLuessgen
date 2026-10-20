# Task 03: Calculate Partial Correlations

## GOAL

Implement Python code (`code/partial_correlation.py`) with separate functions to load the residuals and regression statistics from Task 02 and calculate the utilities–technology partial correlation controlling for market excess returns for the full sample and all eight predefined comparison periods. The script must save:

- **Descriptive statistics** (`output/descriptive_statistics.xlsx`), formatted as the proposal's Descriptive Statistics: Panel A (partial correlation, `Corr(U, T)`, `Corr(U, M)`, `Corr(T, M)`, N) and Panel B (weekly volatilities in %), rounded to 3 decimals.
- **Partial correlations** (`output/partial_correlations.csv`), unrounded, one row per period: `period`, `n_obs`, `partial_correlation`.

## FILES

- **`code/`:** May add/edit only the task's own file, `code/partial_correlation.py`. All other contents are read-only.
- **`tasks/README.md`:** May update only this task's status.
- **`logs/`:** May add/edit `logs/03_partial_correlation.md` to record all other results, execution and check logs.
- **All others:** Read-only for direct edits. Only running the Python script may create or update the two output files; the LLM must not write them directly.

## CONSTRAINTS

**Inputs:** `output/market_residuals.csv` and `output/regression_statistics.csv` from Task 02 (`n_obs`, `corr_UT`, `corr_UM`, `corr_TM`, `vol_U`, `vol_T`, `vol_M`); periods exactly as in the [proposal](../proposal.md). Tasks 01–02 must be `Completed` and their outputs must exist locally (`output/` is not tracked by Git). Excel output requires `openpyxl`.

**Conventions:** Keep full precision. Calculate the Pearson correlation of `utilities_residual` and `technology_residual` within each period; never combine residuals from different periods. Verify with `(corr_UT - corr_UM * corr_TM) / sqrt((1 - corr_UM ** 2) * (1 - corr_TM ** 2))`. Report descriptively: no significance tests (H3 is tested in Task 04), no clipping into `[-1, 1]`, no causal claims. Use the proposal's columns and row order; round only for display. Do not change Task 02 results; log unresolved errors, stop and ask.

| Function | Description | Failure |
| --- | --- | --- |
| `main ()` | Run load → partial correlation → format → save. | A function fails. |
| `load_inputs (residuals_path, statistics_path)` | Read and return `(residuals, regression_statistics)`. | Files cannot be read; duplicate or missing keys. |
| `calculate_partial_correlations (residuals)` | Return one row per period with `period`, `n_obs`, `partial_correlation`. | Zero residual variance or nonfinite results. |
| `format_descriptive_statistics (partial_correlations, regression_statistics)` | Return Panel A and Panel B as in the proposal, joined one-to-one by period. | Missing, duplicate or mismatched periods or `n_obs`. |
| `save_results (panels, partial_correlations, output_dir)` | Write the panels as Excel and the partial correlations as CSV, without a row index. | Invalid output path or write error. |

## CHECK

**Input**

- **Data files exist:** Both Task 02 files exist and are read correctly; `n_obs` per period agree.

**Output**

- **Periods:** Nine rows in proposal order, including Before AI boom; `n_obs` per period match Task 02.
- **Calculation:** Residual correlation matches the analytic formula in every period and synthetic data with known co-movement are recovered (declared tolerances); values lie in `[-1, 1]`.
- **Descriptive statistics:** Values in both panels match the unrounded inputs after rounding.
- **File output:** Running `.venv/bin/python -B code/partial_correlation.py` creates both files.

## OUTPUT

- **Branch:** Work only on `agent/03_partial_correlation`; do not push or merge.
- **Commits:** One descriptive commit per completed step (e.g. loading, partial correlation, descriptive statistics, saving).
- **Final message:** Summarize code changes, CHECK results, open issues and items for researcher verification; list the commit hashes and report `Ready for Review`.

## STOP

- **Done:** Stop when all CHECK criteria pass.
- **Step limit:** Stop and report after 5 commits without passing CHECK.
- **Ask first:** Stop and ask if a read-only file would have to change, Tasks 01–02 are not `Completed`, their outputs are missing, `openpyxl` is missing, or the analytic check fails after in-scope fixes.
