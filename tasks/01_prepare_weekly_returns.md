# Task 01: Prepare Weekly Returns

## GOAL

Implement Python code (`code/prepare_returns.py`) with separate functions to load and check the existing daily returns, then convert them into weekly excess returns for utilities, technology and the market from January 1990 onward. The script must save the weekly return results as a CSV file (`output/weekly_returns.csv`).

## FILES

- **`code/`:** May add/edit only the task's own file, `code/prepare_returns.py`. All other contents are read-only.
- **`tasks/README.md`:** May update only this task's status.
- **`logs/`:** May add/edit `logs/01_prepare_weekly_returns.md` to record all other results, execution and check logs.
- **All others:** Read-only for direct edits. Only running the Python script may create or update `output/weekly_returns.csv`; the LLM must not write the CSV directly.

## CONSTRAINTS

**Inputs:** `Utils`/`BusEq` (value-weighted) from [industry CSV](../data/12_Industry_Portfolios_Daily.csv); `Mkt-RF`/`RF` from [factor CSV](../data/F-F_Research_Data_Factors_daily.csv). Daily returns are given in percent: `0.02 = 0.02%`. Use January 1990 to the last full week ending on or before 31 August 2026; record the final sample week in the log.

**Conventions:** Keep the source percent units in the output. Confirm week and boundary rules before calculation; keep valid holiday weeks. Loading reads, validation checks and calculation computes returns. Do not drop or fill data without approval; log unresolved errors, stop and ask.

| Function | Description | Failure |
| --- | --- | --- |
| `main ()` | Run load → validate daily → calculate weekly → save. | A function fails. |
| `load_daily_returns (industry_path, factors_path)` | Read and return the two source tables as raw DataFrames `(industry, factors)`. | Files cannot be read. |
| `validate_daily_returns (industry, factors)` | Check columns, dates, values, units and shared coverage. | Invalid or inconsistent daily data. |
| `calculate_weekly_returns (industry, factors, week_rule, boundary_rule)` | Calculate weekly excess returns in source units by setting market = `Mkt-RF + RF`, compounding sectors, market and RF separately with `100 * (product(1 + r / 100) - 1)`, then subtracting weekly RF. | Invalid week rules or no complete shared week. |
| `save_weekly_returns (weekly, output_path)` | Write the calculated weekly returns to the CSV without a row index. | Invalid output path or CSV write error. |

## CHECK

**Input**

- **Data files exist:** Both input CSVs exist and are read correctly (value-weighted block, selected columns).
- **No missing or invalid values:** No missing markers, duplicate dates, bad values or wrong units; mismatched coverage is detected.

**Output**

- **Weekly observations:** One row per shared week; valid holiday weeks are kept.
- **Calculation:** Weekly returns match independent hand calculations for sample weeks, including holiday and boundary weeks.
- **Sample period:** Data starts in January 1990 and ends with the last full week ending on or before 31 August 2026, covered by both files.
- **CSV output:** Running `.venv/bin/python -B code/prepare_returns.py` creates `output/weekly_returns.csv` with `week_end`, `utilities_excess`, `technology_excess`, `market_excess` in source percent units (`0.02 = 0.02%`).

## OUTPUT

- **Branch:** Work only on `agent/01_prepare_weekly_returns`; do not push or merge.
- **Commits:** One descriptive commit per completed step (e.g. loading, validation, weekly calculation, CSV output).
- **Final message:** Summarize code changes, CHECK results, open issues and items for researcher verification; list the commit hashes and report `Ready for Review`.

## STOP

- **Done:** Stop when all CHECK criteria pass.
- **Step limit:** Stop and report after 5 commits without passing CHECK.
- **Ask first:** Stop and ask if a read-only file would have to change, or on unclear methodology or unresolved data problems.
