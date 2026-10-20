# Task 02: Estimate Market Betas

## 2026-10-21 — Selection and branch verification

- User invoked `research-task-workflow`. Read its SKILL.md, proposal.md,
  AGENTS.md, tasks/README.md and tasks/02_estimate_beta.md.
- Initial branch was `agent/01_prepare_weekly_returns`; stopped without edits
  as required. Reported the existing deletion of code/.gitkeep without changing it.
- User asked to retry after switching branches. Rechecked
  `git branch --show-current`, `git status --short`, `git diff --cached`:
  correct branch `agent/02_estimate_beta`, clean working tree, nothing staged.
- Task 01 is Completed. The local weekly input exists. Changes are limited to
  code/estimate_beta.py, this log and Task 02's status in tasks/README.md;
  only the task script may create the three specified output files.
- `git check-ignore` confirms all three generated outputs are ignored.
- Git emits a nonfatal warning about the inaccessible global ignore file;
  repository commands still complete successfully.

## Step 1 — Load and assign periods

- Marked Task 02 In Progress. Added load_weekly_returns with the exact input
  schema, unchanged percent units, finite numeric values and every fixed-sample
  Friday exactly once in order. Invalid data cause errors without filling or dropping.
- Assigned the nine periods in proposal order by Friday calendar month.
  Verified that before/AI partition the sample and the six crisis subperiods
  plus March–November 2022 partition Before AI boom.
- Dependency/input probe using `.venv/bin/python -B -c ...` imported pandas,
  openpyxl and statsmodels successfully; input has 1,913 rows and four columns,
  1990-01-05 through 2026-08-28. No dependency changes needed.
- Initial inline check failed on manually entered expected counts (Financial
  Crisis 91 and COVID 105). Calendar enumeration shows 92 and 104 respectively;
  implementation boundaries were correct. Replaced manual counts with an
  independent enumeration of Fridays; no CHECK requirement changed.
- Run the reproducible blocks below from the project root with:
  `.venv/bin/python -B - <<'PY'` followed by the block and closing `PY`.

### Step 1 check

```python
import sys
from unittest.mock import patch
import numpy as np
import pandas as pd
sys.path.insert(0, "code")
import estimate_beta as m
p = m.load_weekly_returns(m.WEEKLY_PATH)
w = pd.read_csv(m.WEEKLY_PATH, float_precision="round_trip")
assert p.index.is_unique
assert list(p.index.get_level_values("period").unique()) == m.PERIOD_NAMES
np.testing.assert_array_equal(p.loc["Full Sample"].to_numpy(), w[m.RETURN_COLUMNS].to_numpy())
bounds = [
    ("1990-01-01", "2026-08-28"), ("1990-01-01", "2022-11-30"),
    ("2022-12-01", "2026-08-28"), ("1990-01-01", "2000-02-29"),
    ("2000-03-01", "2002-10-31"), ("2002-11-01", "2007-05-31"),
    ("2007-06-01", "2009-02-28"), ("2009-03-01", "2020-02-29"),
    ("2020-03-01", "2022-02-28"),
]
for name, (start, end) in zip(m.PERIOD_NAMES, bounds):
    assert p.loc[name].index.equals(pd.date_range(start, end, freq="W-FRI", name="week_end"))
invalid = [w.iloc[:-1], pd.concat([w.iloc[:1], w]), w.iloc[::-1]]
for column, value in [("week_end", "1990-01-04"), ("utilities_excess", np.nan),
                      ("technology_excess", np.inf), ("week_end", "1989-12-29")]:
    bad = w.copy(); bad.loc[0, column] = value; invalid.append(bad)
invalid.append(w.rename(columns={"utilities_excess": "wrong"}))
for bad in invalid:
    with patch.object(m.pd, "read_csv", return_value=bad):
        try:
            m.load_weekly_returns(m.WEEKLY_PATH)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid input accepted")
print("PASS: exact preservation, 9 calendar-verified periods, 8 invalid-input cases")
print(p.groupby(level="period", sort=False).size().to_string())
```

- Result: PASS. Counts in proposal order: 1913, 1717, 196, 530, 139, 239,
  92, 574, 104. All eight invalid inputs rejected. `git diff --check` passed.

## Step 2 — OLS, Newey–West and residuals

- Step 1 commit: `765bd30c1df710f8e69b9f438922070b560e2653`; verified author
  `Codex <codex@openai.com>` with `git log -1 --format='%H %an <%ae>'`.
- Added run_ols: refit both sectors with intercepts per period; fixed four-lag
  Bartlett HAC without a finite-sample multiplier, standard normal two-sided
  tests against beta=1. This is the asymptotic Newey–West convention and is
  explicit in code. No alternative estimators or factors used.
- residual_std denotes sample residual standard deviation (ddof=1), consistent
  with the reported weekly volatilities; it is not residual RMSE (n−2 denominator).
- Output statistics preserve full precision and percent units. Residual output
  preserves every (period, week_end) observation. Singular designs, constant
  returns, nonfinite results and malformed keys are rejected.

### Step 2 check

```python
import sys
from math import erfc, sqrt
import numpy as np
import pandas as pd
sys.path.insert(0, "code")
import estimate_beta as m
p = m.load_weekly_returns(m.WEEKLY_PATH)
stats, residuals = m.run_ols(p)
assert list(stats.columns) == m.STATISTICS_COLUMNS
assert list(residuals.columns) == m.RESIDUAL_COLUMNS
assert stats.period.tolist() == m.PERIOD_NAMES
assert stats.hac_lags.eq(4).all()
counts = stats.set_index("period").n_obs
assert counts["Before AI boom"] + counts["AI boom"] == counts["Full Sample"]
gap = pd.date_range("2022-03-01", "2022-11-30", freq="W-FRI")
assert counts.iloc[3:].sum() + len(gap) == counts["Before AI boom"]
assert not residuals.duplicated(["period", "week_end"]).any()
assert len(residuals) == len(p)
max_hac_error = 0.0
for row in stats.itertuples(index=False):
    data = p.loc[row.period]
    rr = residuals.loc[residuals.period.eq(row.period)].set_index("week_end")
    assert rr.index.equals(data.index)
    assert row.n_obs == len(data)
    assert row.first_week == data.index[0] and row.last_week == data.index[-1]
    x = data.market_excess.to_numpy()
    design = np.column_stack([np.ones(len(x)), x])
    inverse = np.linalg.inv(design.T @ design)
    np.testing.assert_array_equal(rr.market_excess, x)
    for code, col, resid_col in [("U", "utilities_excess", "utilities_residual"),
                                 ("T", "technology_excess", "technology_residual")]:
        y = data[col].to_numpy()
        alpha, beta = getattr(row, f"alpha_{code}"), getattr(row, f"beta_{code}")
        r = rr[resid_col].to_numpy()
        np.testing.assert_allclose(beta, np.cov(y, x, ddof=1)[0, 1] / np.var(x, ddof=1), atol=1e-12, rtol=1e-12)
        np.testing.assert_allclose(beta, getattr(row, f"corr_{code}M") * getattr(row, f"vol_{code}") / row.vol_M, atol=1e-12, rtol=1e-12)
        np.testing.assert_allclose(getattr(row, f"r_squared_{code}"), getattr(row, f"corr_{code}M") ** 2, atol=1e-12, rtol=1e-12)
        np.testing.assert_allclose(getattr(row, f"vol_{code}"), y.std(ddof=1), atol=1e-12, rtol=1e-12)
        np.testing.assert_allclose(r, y - alpha - beta*x, atol=1e-12, rtol=1e-12)
        assert abs(r.mean()) < 1e-12 and abs(np.mean(r*x)) < 1e-12
        np.testing.assert_allclose(getattr(row, f"residual_std_{code}"), r.std(ddof=1), atol=1e-12, rtol=1e-12)
        # Independent HAC: direct scalar loops, not statsmodels' covariance code.
        scores = design * r[:, None]
        meat = np.zeros((2, 2))
        for j in range(2):
            for k in range(2):
                meat[j, k] = sum(scores[t, j]*scores[t, k] for t in range(len(x)))
                for lag in range(1, 5):
                    weight = 1 - lag/5
                    meat[j, k] += weight * sum(
                        scores[t, j]*scores[t-lag, k] + scores[t-lag, j]*scores[t, k]
                        for t in range(lag, len(x)))
        se = np.sqrt(np.diag(inverse @ meat @ inverse))
        actual = [getattr(row, f"se_alpha_{code}"), getattr(row, f"se_beta_{code}")]
        np.testing.assert_allclose(actual, se, atol=1e-12, rtol=1e-10)
        max_hac_error = max(max_hac_error, float(np.max(np.abs(actual-se))))
        t = (beta-1)/se[1]
        np.testing.assert_allclose(getattr(row, f"t_beta_1_{code}"), t, atol=1e-10, rtol=1e-10)
        np.testing.assert_allclose(getattr(row, f"p_beta_1_{code}"), erfc(abs(t)/sqrt(2)), atol=1e-12, rtol=1e-10)
    np.testing.assert_allclose(row.vol_M, x.std(ddof=1), atol=1e-12, rtol=1e-12)
    np.testing.assert_allclose(row.corr_UT, np.corrcoef(data.utilities_excess, data.technology_excess)[0, 1], atol=1e-12, rtol=1e-12)

# Nonzero noise orthogonalized to intercept and market gives known OLS coefficients.
rng = np.random.default_rng(20261021)
x = rng.normal(size=160)
design = np.column_stack([np.ones(len(x)), x])
noise = rng.normal(size=(len(x), 2))
noise -= design @ np.linalg.lstsq(design, noise, rcond=None)[0]
synthetic = pd.DataFrame({"utilities_excess": 0.3 + 0.6*x + noise[:, 0],
                          "technology_excess": -0.2 + 1.4*x + noise[:, 1],
                          "market_excess": x}, index=pd.date_range("2000-01-07", periods=len(x), freq="W-FRI", name="week_end"))
keyed = pd.concat([synthetic]*9, keys=m.PERIOD_NAMES, names=["period", "week_end"])
s, _ = m.run_ols(keyed)
np.testing.assert_allclose(s[["alpha_U", "beta_U", "alpha_T", "beta_T"]], np.tile([0.3, 0.6, -0.2, 1.4], (9, 1)), atol=1e-12, rtol=1e-12)
for bad in [keyed.assign(market_excess=1.0), keyed.assign(utilities_excess=0.0),
            keyed.assign(technology_excess=np.inf), keyed.iloc[::-1],
            pd.concat([keyed, keyed.iloc[:1]])]:
    try:
        m.run_ols(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid OLS input accepted")
print(f"PASS: all 18 regressions, synthetic coefficients, 5 invalid inputs; maximum HAC SE error={max_hac_error:.3g}")
print(stats[["period", "n_obs", "beta_U", "se_beta_U", "beta_T", "se_beta_T"]].to_string(index=False))
```

- Ran the Step 2 block with `.venv/bin/python -B` by extracting the second
  fenced Python block from this log and executing it. PASS for all 18 regressions,
  both beta identities, R², volatility, residual reconstruction/centering/
  orthogonality/dispersion, independently calculated HAC intercept and slope
  SEs, normal p-values, known synthetic coefficients and five rejection cases.
- Tolerances: 1e-12 absolute and relative for identities and synthetic
  coefficients; HAC SEs 1e-12 absolute / 1e-10 relative; t-statistics 1e-10;
  p-values 1e-12 absolute / 1e-10 relative. Maximum HAC SE absolute difference
  was 3.61e-16. `git diff --check` passed.
- Full-sample betas (unrounded outputs retained in memory): utilities 0.565569,
  technology 1.210095. These are estimates, without causal interpretation.

## Step 3 — Proposal regression table

- Step 2 commit: `d646660bd5e636d87d912e72eb3411354cb504e8`, author verified
  as Codex. Added format_regression_table with nine rows in proposal order,
  displayed beta stars against one, three-decimal betas/SEs/R² and integer N.
- Added validation for complete statistics, finite values, counts, dates,
  SEs, p-values, volatilities and correlation/R² ranges. Kept the proposal's
  table note in table metadata for the Excel export. Source statistics are
  not rounded or modified.

### Step 3 check

```python
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, "code")
import estimate_beta as m
s, _ = m.run_ols(m.load_weekly_returns(m.WEEKLY_PATH))
original = s.copy(deep=True)
t = m.format_regression_table(s)
pd.testing.assert_frame_equal(s, original)
assert list(t.columns) == ["Comparison period", "Utilities Beta (SE)", "Technology Beta (SE)", "R² Utilities", "R² Technology", "N"]
assert t.iloc[:, 0].tolist() == m.PERIOD_NAMES
assert t.attrs["note"] == "Newey–West standard errors in parentheses; stars test H0: β = 1 (two-sided): * p < 0.10, ** p < 0.05, *** p < 0.01."
for i, row in s.iterrows():
    for code, column in [("U", "Utilities Beta (SE)"), ("T", "Technology Beta (SE)")]:
        p = row[f"p_beta_1_{code}"]
        stars = "*" * sum(p < threshold for threshold in [0.10, 0.05, 0.01])
        assert t.loc[i, column] == f"{row[f'beta_{code}']:.3f}{stars} ({row[f'se_beta_{code}']:.3f})"
        assert t.loc[i, f"R² {'Utilities' if code == 'U' else 'Technology'}"] == round(row[f"r_squared_{code}"], 3)
    assert t.loc[i, "N"] == row.n_obs
for p, stars in [(0, "***"), (0.009999, "***"), (0.01, "**"), (0.049999, "**"),
                  (0.05, "*"), (0.099999, "*"), (0.10, ""), (1, "")]:
    modified = s.copy()
    modified.loc[0, "p_beta_1_U"] = p
    assert m.format_regression_table(modified).loc[0, "Utilities Beta (SE)"].split(" (")[0] == f"{s.loc[0, 'beta_U']:.3f}{stars}"
invalid = [s.drop(columns="beta_U"), s.iloc[::-1], s.assign(beta_U=np.nan),
           s.assign(p_beta_1_T=1.01), s.assign(se_beta_U=-1), s.assign(n_obs=1.5)]
for bad in invalid:
    try:
        m.format_regression_table(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid statistics accepted")
print("PASS: table values, note, precision preservation, 8 star boundaries, 6 invalid cases")
print(t.to_string(index=False))
```

- Ran Step 3's fenced block with `.venv/bin/python -B`: PASS for all nine
  rows, rounding, stars, unchanged source precision, exact table note, eight
  p-value boundary cases and six invalid-statistics cases. `git diff --check`
  passed. The displayed table is ready for the Excel saving step.

## Step 4 — Save outputs and final agent review

- Step 3 commit: `796d073bf9ec03d360e19dcac5934035d85dc74e`, author verified
  as Codex. Added save_results and main. Export paths are restricted to the
  three named outputs and symlink redirection is rejected. Validation and
  write errors propagate to the caller.
- Excel uses the proposal's headers, two separator rows, nine data rows,
  three-decimal display, integer N and the exact proposal note. Added column
  widths, header rules, frozen labels and landscape A4 fit-to-page printing.
- CSVs retain full floating-point precision, exact column order, ISO dates
  and no row index. No output files are written directly by the LLM.
- Final command: `.venv/bin/python -B code/estimate_beta.py`.

### Step 4 check

```python
import sys
from pathlib import Path
from unittest.mock import patch
import numpy as np
import pandas as pd
from openpyxl import load_workbook
sys.path.insert(0, "code")
import estimate_beta as m
p = m.load_weekly_returns(m.WEEKLY_PATH)
s, r = m.run_ols(p)
t = m.format_regression_table(s)
disk_s = pd.read_csv(m.OUTPUT_DIR / "regression_statistics.csv", float_precision="round_trip", parse_dates=["first_week", "last_week"])
disk_r = pd.read_csv(m.OUTPUT_DIR / "market_residuals.csv", float_precision="round_trip", parse_dates=["week_end"])
pd.testing.assert_frame_equal(disk_s, s, check_exact=True, check_dtype=False)
pd.testing.assert_frame_equal(disk_r, r, check_exact=True, check_dtype=False)
assert disk_s.shape == (9, 27) and disk_r.shape == (5504, 5)
assert all("*" not in Path(m.OUTPUT_DIR / name).read_text() for name in ["regression_statistics.csv", "market_residuals.csv"])
book = load_workbook(m.OUTPUT_DIR / "regression_table.xlsx", data_only=False)
assert book.sheetnames == ["Market Betas"]
sheet = book.active
assert [sheet.cell(1, col).value for col in range(1, 7)] == list(t.columns)
data_rows = [2, 4, 5, 7, 8, 9, 10, 11, 12]
assert sheet.max_column == 6 and sheet.max_row == 14
for source_i, excel_i in enumerate(data_rows):
    for col in range(1, 7):
        assert sheet.cell(excel_i, col).value == t.iloc[source_i, col-1]
    for col in (4, 5):
        assert sheet.cell(excel_i, col).number_format == "0.000"
    assert sheet.cell(excel_i, 6).number_format == "0"
for blank in (3, 6, 13):
    assert all(sheet.cell(blank, col).value is None for col in range(1, 7))
assert sheet["A14"].value == t.attrs["note"]
assert "A14:F14" in sheet.merged_cells
assert sheet["A14"].alignment.wrap_text and sheet["A1"].font.bold
assert sheet.freeze_panes == "B2"
assert sheet.page_setup.fitToWidth == sheet.page_setup.fitToHeight == 1
book.close()

# Rejection checks operate before writes; injected write errors also propagate.
for table, stats, residuals, directory in [
    (t, s, r, m.PROJECT_ROOT),
    (t.iloc[::-1], s, r, m.OUTPUT_DIR),
    (t, s, pd.concat([r, r.iloc[:1]]), m.OUTPUT_DIR),
    (t, s, r.iloc[:-1], m.OUTPUT_DIR),
    (t, s, r.assign(market_excess=np.inf), m.OUTPUT_DIR),
]:
    try:
        m.save_results(table, stats, residuals, directory)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid output accepted")
with patch.object(m.Workbook, "save", side_effect=OSError("Injected write error")):
    try:
        m.save_results(t, s, r, m.OUTPUT_DIR)
    except OSError:
        pass
    else:
        raise AssertionError("Write error swallowed")
print("PASS: exact CSV round trips, 9-row Excel/table/note/format match, 5 invalid outputs, write-error propagation")
print(f"Statistics: {disk_s.shape}; residuals: {disk_r.shape}")
```

- First complete final run: all four blocks passed, including exact CSV
  round trips and all Excel cells, note and formats; 9×27 statistics and
  5,504×5 residuals. During final code review, strengthened the zero-variance
  guard: a constant decimal can yield tiny positive computed variance through
  rounding, so an exact range check also rejects constant inputs.

### Constant-decimal regression guard

```python
import sys
sys.path.insert(0, "code")
import estimate_beta as m
p = m.load_weekly_returns(m.WEEKLY_PATH)
for column in m.RETURN_COLUMNS:
    try:
        m.run_ols(p.assign(**{column: 0.1}))
    except ValueError as error:
        assert "zero return variance" in str(error)
    else:
        raise AssertionError("Constant decimal accepted")
print("PASS: constant 0.1 rejected in each of the three return series")
```

Final reproducible check command (runs every block above):

```sh
.venv/bin/python -B code/estimate_beta.py
.venv/bin/python -B - <<'PY'
from pathlib import Path
blocks = Path('logs/02_estimate_beta.md').read_text().split('```python\n')[1:]
for i, block in enumerate(blocks, 1):
    print(f'CHECK block {i}', flush=True)
    exec(compile(block.split('```')[0], f'CHECK block {i}', 'exec'), {'__name__': '__main__'})
print('ALL TASK 02 CHECKS PASSED')
PY
git diff --check
```

### Final results and handoff

- Re-ran the exact task command after the constant-decimal guard change:
  exit 0, saved nine periods and 5,504 residual rows. All five verification
  blocks then passed, followed by `git diff --check` (exit 0).
- Input: 1,913 complete ordered Fridays, 1990-01-05–2026-08-28, percent
  units unchanged, no missing rows, filling, exclusions or source changes.
- Periods: Before AI boom 1,717 + AI boom 196 = Full Sample 1,913.
  Six crisis subperiods 1,678 + gap March–November 2022 39 = 1,717;
  exact calendar ranges verified independently, with no crisis overlap.
- All 18 regressions passed covariance/variance and correlation/volatility
  beta identities, R² identities, independent four-lag Bartlett HAC SEs,
  normal t-statistic/p-value checks and residual reconstruction, centering,
  market orthogonality and ddof=1 dispersion checks. Maximum HAC SE error
  3.61e-16; declared numerical tolerances above were met. Known synthetic
  intercepts/slopes recovered within 1e-12 absolute/relative tolerance.
- Exported CSV values exactly match the computed floating-point results on
  round-trip reading. Excel values, three-decimal formats, significance stars,
  nine ordered data rows, separator rows and exact note all passed checks.
- Generated only by `.venv/bin/python -B code/estimate_beta.py`:
  - `output/regression_table.xlsx`: nine rows, six columns, proposal table note.
  - `output/regression_statistics.csv`: nine rows, 27 columns, unrounded.
  - `output/market_residuals.csv`: 5,504 rows, five columns, unrounded.
- Source changes: only code/estimate_beta.py; metadata changes: Task 02 status
  in tasks/README.md and this chronological log. Generated outputs remain
  ignored and are not staged. No protected source files or dependencies changed.
- Status set to Ready for Review only after all CHECK criteria passed.
  No unresolved implementation failures or methodological deviations.
  The earlier global Git ignore warning remains nonfatal.
- Researcher review: inspect the four-step diff, rerun the task command and
  checks above independently, and verify the Excel layout in the researcher's
  spreadsheet application. Review the explicitly documented asymptotic HAC
  convention (no finite-sample multiplier) and residual sample std (ddof=1).
  Researcher acceptance and merge remain pending; do not mark Completed yet.
- Final commit includes saving, final validation results and Ready for Review
  status. Stop after Task 02; no push, pull request, merge or Task 03 execution.
