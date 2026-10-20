# Task 03: Calculate Partial Correlations

## 2026-10-21 — Selection and preconditions

- Researcher approved Task 02 and requested the next task. Initially stopped
  on branch mismatch; after the user asked to retry, checked
  `git branch --show-current`, `git status --short`, `git diff --cached`:
  correct prepared branch `agent/03_partial_correlation`, clean tree, no
  staged changes. Reused the previously read research-task-workflow skill.
- Read proposal.md, tasks/README.md and tasks/03_partial_correlation.md.
  Tasks 01 and 02 are Completed. No overlapping edits or nested AGENTS.md
  files found. Marked Task 03 In Progress.
- `.venv/bin/python -B` input/dependency probe: both Task 02 files exist and
  read successfully; residuals 5,504×5, statistics 9×27; openpyxl 3.1.5 present.
  `git check-ignore` confirms both requested generated outputs are ignored.
- Scope: only code/partial_correlation.py, Task 03 status in tasks/README.md,
  this log, and the two outputs generated exclusively by the task script.
  No changes to Task 02 outputs, methods, sources or dependencies authorized
  or needed. No significance tests or causal claims in Task 03.
- Git emits the already known nonfatal global ignore-file warning; commands
  complete successfully.

## Step 1 — Load and validate inputs

- Added load_inputs with finite values, exact residual schema, required
  regression statistics, unique period/date keys and all nine proposal periods.
  Validates each period's full calendar of Friday labels and the Task 02
  observation counts and first/last-week metadata. No rows are filled or dropped.
- General helpers permit arbitrary period input order; later output will
  explicitly follow proposal order. Repeated weeks in different periods are
  intentional; duplicate keys within the same period are rejected.

### Step 1 check

```python
import sys
from unittest.mock import patch
import numpy as np
import pandas as pd
sys.path.insert(0, "code")
import partial_correlation as m
r, s = m.load_inputs(m.RESIDUALS_PATH, m.STATISTICS_PATH)
raw_r = pd.read_csv(m.RESIDUALS_PATH, float_precision="round_trip")
raw_s = pd.read_csv(m.STATISTICS_PATH, float_precision="round_trip")
pd.testing.assert_frame_equal(r.drop(columns="week_end"), raw_r.drop(columns="week_end"), check_exact=True)
pd.testing.assert_frame_equal(s, raw_s, check_exact=True)
assert r.shape == (5504, 5) and s.shape == (9, 27)
assert not r.duplicated(["period", "week_end"]).any()
assert r.groupby("period").size().to_dict() == s.set_index("period").n_obs.to_dict()
invalid_pairs = [
    (pd.concat([raw_r, raw_r.iloc[:1]]), raw_s),
    (raw_r.iloc[:-1], raw_s),
    (raw_r, pd.concat([raw_s, raw_s.iloc[:1]])),
    (raw_r, raw_s.iloc[:-1]),
    (raw_r, raw_s.assign(n_obs=1)),
    (raw_r.assign(utilities_residual=np.nan), raw_s),
    (raw_r, raw_s.assign(corr_UM=np.inf)),
    (raw_r, raw_s.assign(vol_U=-1)),
    (raw_r.drop(columns="market_excess"), raw_s),
    (raw_r, raw_s.drop(columns="corr_UT")),
]
bad = raw_r.copy(); bad.loc[0, "week_end"] = "1990-01-04"
invalid_pairs.append((bad, raw_s))
bad = raw_r.copy(); bad.loc[0, "period"] = "Unknown"
invalid_pairs.append((bad, raw_s))
bad = raw_s.copy(); bad.loc[0, "n_obs"] += 1
invalid_pairs.append((raw_r, bad))
for rr, ss in invalid_pairs:
    with patch.object(m.pd, "read_csv", side_effect=[rr.copy(deep=True), ss.copy(deep=True)]):
        try:
            m.load_inputs(m.RESIDUALS_PATH, m.STATISTICS_PATH)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid Task 02 input accepted")
try:
    m.load_inputs(m.RESIDUALS_PATH.with_name("does_not_exist.csv"), m.STATISTICS_PATH)
except FileNotFoundError:
    pass
else:
    raise AssertionError("Missing input accepted")
print("PASS: exact input preservation, counts and calendars; 13 invalid pairs and missing file rejected")
```

Run each fenced Python check using `.venv/bin/python -B` from the project root.

- Ran Step 1's block by extracting the first fenced Python block from this
  log and executing it with `.venv/bin/python -B`: PASS for exact numeric
  preservation, full calendars, matching counts, 13 invalid pairs and a
  missing-file case. `git diff --check` passed before committing.
- Baseline SHA-256 hashes recorded before implementation, using
  `.venv/bin/python -B` with `hashlib.sha256(Path(...).read_bytes())`:

```text
weekly_returns.csv 40c2d638d4426384766d3b22b69c84043e3d29aa74b532421cc646a3078d9365
regression_table.xlsx bd78cc5cafb1c0b1a9679f56bf6106421d2009e027b310f47af9987b0064245b
regression_statistics.csv 45516df4983ae2d6ca562b3d9c368b4e35ebe2f59f3f1ad100db090b6e8d7d57
market_residuals.csv 8083c7d59a1375e1744440749fd36f714f0521aa063e561d061f6982ccaf3c30
```

## Step 2 — Period-specific Pearson correlations

- Step 1 commit: `7464916f6b2d18bd029884eff5478db8245e5288`; verified
  `Codex <codex@openai.com>` with `git log -1 --format='%H %an <%ae>'`.
- Added calculate_partial_correlations: center each residual series within
  its own period, compute the Pearson dot-product ratio, return exactly nine
  rows in proposal order with integer n_obs and unrounded correlations.
- Zero residual variance (including constant decimal values), insufficient
  observations, nonfinite results and out-of-range correlations cause errors.
  No clipping, pooling across periods or statistical hypothesis tests.
- Analytic agreement tolerance declared as 1e-12 absolute / 1e-10 relative;
  synthetic known-correlation checks use 1e-12 absolute / relative tolerance.

### Step 2 check

```python
import sys
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
sys.path.insert(0, "code")
import partial_correlation as m
r, s = m.load_inputs(m.RESIDUALS_PATH, m.STATISTICS_PATH)
original_r, original_s = r.copy(deep=True), s.copy(deep=True)
p = m.calculate_partial_correlations(r)
assert list(p.columns) == ["period", "n_obs", "partial_correlation"]
assert p.period.tolist() == m.PERIOD_NAMES
assert p.partial_correlation.between(-1, 1).all()
joined = p.merge(s, on=["period", "n_obs"], validate="one_to_one")
assert len(joined) == 9
analytic = (joined.corr_UT - joined.corr_UM*joined.corr_TM) / np.sqrt((1-joined.corr_UM**2)*(1-joined.corr_TM**2))
np.testing.assert_allclose(p.partial_correlation, analytic, atol=1e-12, rtol=1e-10)
for row in p.itertuples(index=False):
    group = r.loc[r.period.eq(row.period)]
    assert row.n_obs == len(group)
    np.testing.assert_allclose(row.partial_correlation, pearsonr(group.utilities_residual, group.technology_residual).statistic, atol=1e-12, rtol=1e-12)
    assert abs(group.utilities_residual.mean()) < 1e-12
    assert abs(group.technology_residual.mean()) < 1e-12
    assert abs(np.mean(group.utilities_residual*group.market_excess)) < 1e-12
    assert abs(np.mean(group.technology_residual*group.market_excess)) < 1e-12
pd.testing.assert_frame_equal(r, original_r, check_exact=True)
pd.testing.assert_frame_equal(s, original_s, check_exact=True)

# Equal-norm orthogonal vectors yield exactly known correlations. Distinct
# period offsets expose accidental pooling instead of within-period centering.
u = np.array([-1., -1, -1, -1, 1, 1, 1, 1])
v = np.array([-1., -1, 1, 1, -1, -1, 1, 1])
targets = [-0.8, 0.6, 0., 0.2, -0.4, 0.9, -0.2, 0.4, -0.6]
frames = []
for i, (period, rho) in enumerate(zip(m.PERIOD_NAMES, targets)):
    frames.append(pd.DataFrame({"period": period,
        "week_end": pd.date_range("2000-01-07", periods=8, freq="W-FRI"),
        "utilities_residual": (i+1)*u + 10*i,
        "technology_residual": (i+2)*(rho*u + np.sqrt(1-rho*rho)*v) - 20*i,
        "market_excess": np.arange(8, dtype=float)}))
synthetic = pd.concat(frames, ignore_index=True)[m.RESIDUAL_COLUMNS]
known = m.calculate_partial_correlations(synthetic)
np.testing.assert_allclose(known.partial_correlation, targets, atol=1e-12, rtol=1e-12)
assert known.n_obs.eq(8).all()
# Exact positive/negative co-movement is also supported, without clipping.
for sign in (-1, 1):
    endpoint = synthetic.copy()
    endpoint["utilities_residual"] = np.tile(u, 9)
    endpoint["technology_residual"] = 2*sign*endpoint.utilities_residual
    np.testing.assert_array_equal(m.calculate_partial_correlations(endpoint).partial_correlation, np.full(9, sign))
invalid = [synthetic.assign(utilities_residual=0.1),
           synthetic.assign(technology_residual=0.0),
           synthetic.assign(utilities_residual=np.inf),
           synthetic.loc[synthetic.period.ne("AI boom")],
           pd.concat([synthetic, synthetic.iloc[:1]]),
           synthetic.groupby("period", sort=False).head(1)]
for bad in invalid:
    try:
        m.calculate_partial_correlations(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid residuals accepted")
print(f"PASS: 9 analytic and independent Pearson checks; max analytic error={np.max(np.abs(p.partial_correlation-analytic)):.3g}")
print("PASS: synthetic positive/negative/zero co-movement, both endpoints, 6 invalid inputs")
print(p.to_string(index=False))
```

- Ran the second fenced block with `.venv/bin/python -B`: PASS for all nine
  analytic comparisons and independent scipy Pearson checks. Maximum analytic
  absolute difference 1.22e-15. Residual centering and market orthogonality
  from Task 02 also passed at absolute 1e-12; both loaded inputs unchanged.
- Synthetic data recovered all nine known correlations within 1e-12;
  exact +1/−1 endpoints and six rejection cases passed. `git diff --check`
  passed. Full-sample correlation is approximately −0.387235; no inference
  about differences or causality is made.

## Step 3 — Descriptive statistics panels

- Step 2 commit: `6ab9e5421eed3ccf9311bfc22f4fc59804b5cb52`; author
  verified as Codex. Added format_descriptive_statistics, joining inputs
  one-to-one by period and requiring equal n_obs before output.
- The task script now verifies the analytic identity itself, before rounding.
  A zero denominator or analytic mismatch raises an error without changing
  Task 02 results. Fixed tolerances remain 1e-12 absolute / 1e-10 relative.
- Panel A contains partial/raw correlations and N; Panel B contains the
  three weekly percent volatilities from Task 02, without annualizing or
  dividing by 100. Only display panels are rounded to three decimals.

### Step 3 check

```python
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, "code")
import partial_correlation as m
r, s = m.load_inputs(m.RESIDUALS_PATH, m.STATISTICS_PATH)
p = m.calculate_partial_correlations(r)
original_p, original_s = p.copy(deep=True), s.copy(deep=True)
panels = m.format_descriptive_statistics(p, s)
assert list(panels) == ["Panel A", "Panel B"]
assert list(panels["Panel A"].columns) == ["Comparison period", "Partial Correlation", "Corr(U, T)", "Corr(U, M)", "Corr(T, M)", "N"]
assert list(panels["Panel B"].columns) == ["Comparison period", "σ Utilities", "σ Technology", "σ Market"]
ss, pp = s.set_index("period"), p.set_index("period")
for i, period in enumerate(m.PERIOD_NAMES):
    a, b = panels["Panel A"].iloc[i], panels["Panel B"].iloc[i]
    assert a.iloc[0] == b.iloc[0] == period
    assert a["Partial Correlation"] == round(pp.loc[period, "partial_correlation"], 3)
    for display, source in [("Corr(U, T)", "corr_UT"), ("Corr(U, M)", "corr_UM"), ("Corr(T, M)", "corr_TM")]:
        assert a[display] == round(ss.loc[period, source], 3)
    assert a["N"] == pp.loc[period, "n_obs"] == ss.loc[period, "n_obs"]
    for display, source in [("σ Utilities", "vol_U"), ("σ Technology", "vol_T"), ("σ Market", "vol_M")]:
        assert b[display] == round(ss.loc[period, source], 3)
pd.testing.assert_frame_equal(p, original_p, check_exact=True)
pd.testing.assert_frame_equal(s, original_s, check_exact=True)
shuffled = m.format_descriptive_statistics(p.iloc[::-1], s.sample(frac=1, random_state=7))
for panel in panels:
    pd.testing.assert_frame_equal(panels[panel], shuffled[panel], check_exact=True)
invalid = [
    (p.iloc[:-1], s), (pd.concat([p, p.iloc[:1]]), s),
    (p, s.iloc[:-1]), (p, pd.concat([s, s.iloc[:1]])),
    (p.assign(n_obs=p.n_obs+1), s),
    (p.assign(partial_correlation=p.partial_correlation+0.01), s),
    (p.assign(partial_correlation=1.01), s),
    (p, s.assign(corr_UM=1.0)), (p, s.assign(vol_M=np.nan)),
]
for bad_p, bad_s in invalid:
    try:
        m.format_descriptive_statistics(bad_p, bad_s)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid panel inputs accepted")
print("PASS: both 9-row panels, all rounded values/counts, precision preservation, shuffled join and 9 invalid cases")
for name, panel in panels.items():
    print(name)
    print(panel.to_string(index=False))
```

- Ran the third fenced block with `.venv/bin/python -B`: PASS. All Panel A/B
  values, period order and counts match unrounded inputs after rounding;
  shuffled input orders produce identical panels and do not join by position.
  Both original input frames retain full precision. Nine invalid input pairs
  rejected, including analytic mismatch, denominator zero and n_obs mismatch.
  `git diff --check` passed.

## Step 4 — Export and final review

- Step 3 commit: `cbdd25ac00397a3b14f73e7486d9bb35aa95f099`; author
  verified as Codex. Added save_results and main. Save only to the two named
  output paths; reject alternate directories, redirected paths, inconsistent
  panels and invalid values. Read/validation/write errors propagate.
- Workbook has Panel A and Panel B worksheets, each with the proposal's
  title, columns, nine period rows and two group separators. Three-decimal
  numeric formats, integer N, wrapped titles, explicit widths and landscape
  A4 printing; percent values use numeric 0.000, without Excel percent scaling.
- CSV retains unrounded correlations, integer counts, proposal order and
  no index. Results are generated only by the task script.

### Step 4 check

```python
import sys
from pathlib import Path
from hashlib import sha256
from unittest.mock import patch
import numpy as np
import pandas as pd
from openpyxl import load_workbook
sys.path.insert(0, "code")
import partial_correlation as m
r, s = m.load_inputs(m.RESIDUALS_PATH, m.STATISTICS_PATH)
p = m.calculate_partial_correlations(r)
panels = m.format_descriptive_statistics(p, s)
disk = pd.read_csv(m.OUTPUT_DIR / "partial_correlations.csv", float_precision="round_trip")
pd.testing.assert_frame_equal(disk, p, check_exact=True)
assert disk.shape == (9, 3) and disk.partial_correlation.between(-1, 1).all()
assert disk.period.tolist() == m.PERIOD_NAMES
book = load_workbook(m.OUTPUT_DIR / "descriptive_statistics.xlsx", data_only=False)
assert book.sheetnames == ["Panel A", "Panel B"]
data_rows = [4, 6, 7, 9, 10, 11, 12, 13, 14]
for name, panel in panels.items():
    sheet = book[name]
    assert sheet.max_row == 14 and sheet.max_column == len(panel.columns)
    assert sheet["A1"].value == m.PANEL_TITLES[name]
    assert [sheet.cell(3, col).value for col in range(1, len(panel.columns)+1)] == list(panel.columns)
    for i, row in enumerate(data_rows):
        for col in range(1, len(panel.columns)+1):
            cell = sheet.cell(row, col)
            assert cell.value == panel.iloc[i, col-1]
            if col > 1:
                expected_format = "0" if name == "Panel A" and col == 6 else "0.000"
                assert cell.number_format == expected_format
                assert cell.data_type == "n"
    for blank in (2, 5, 8):
        assert all(sheet.cell(blank, col).value is None for col in range(1, len(panel.columns)+1))
    assert sheet["A1"].alignment.wrap_text and sheet["A3"].font.bold
    assert sheet.freeze_panes == "B4"
    assert sheet.page_setup.fitToWidth == sheet.page_setup.fitToHeight == 1
book.close()

bad_panel = {name: panel.copy() for name, panel in panels.items()}
bad_panel["Panel A"].loc[0, "Partial Correlation"] += 0.01
bad_vol = {name: panel.copy() for name, panel in panels.items()}
bad_vol["Panel B"].loc[0, "σ Market"] = np.inf
bad_count = {name: panel.copy() for name, panel in panels.items()}
bad_count["Panel A"].loc[0, "N"] += 1
for pp, directory in [(panels, m.PROJECT_ROOT), (bad_panel, m.OUTPUT_DIR),
                       (bad_vol, m.OUTPUT_DIR), (bad_count, m.OUTPUT_DIR),
                       ({"Panel A": panels["Panel A"]}, m.OUTPUT_DIR)]:
    try:
        m.save_results(pp, p, directory)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid output accepted")
with patch.object(m.Workbook, "save", side_effect=OSError("Injected write error")):
    try:
        m.save_results(panels, p, m.OUTPUT_DIR)
    except OSError:
        pass
    else:
        raise AssertionError("Write error swallowed")
baseline = {
    "weekly_returns.csv": "40c2d638d4426384766d3b22b69c84043e3d29aa74b532421cc646a3078d9365",
    "regression_table.xlsx": "bd78cc5cafb1c0b1a9679f56bf6106421d2009e027b310f47af9987b0064245b",
    "regression_statistics.csv": "45516df4983ae2d6ca562b3d9c368b4e35ebe2f59f3f1ad100db090b6e8d7d57",
    "market_residuals.csv": "8083c7d59a1375e1744440749fd36f714f0521aa063e561d061f6982ccaf3c30",
}
for name, digest in baseline.items():
    assert sha256((m.OUTPUT_DIR / name).read_bytes()).hexdigest() == digest
print("PASS: exact CSV round trip, both Excel panels/cells/format, 5 invalid outputs, write-error propagation")
print("PASS: all four Task 01/02 output hashes unchanged")
```

Final reproducible check commands:

```sh
.venv/bin/python -B code/partial_correlation.py
.venv/bin/python -B - <<'PY'
from pathlib import Path
blocks = Path('logs/03_partial_correlation.md').read_text().split('```python\n')[1:]
for i, block in enumerate(blocks, 1):
    print(f'CHECK block {i}', flush=True)
    exec(compile(block.split('```')[0], f'CHECK block {i}', 'exec'), {'__name__': '__main__'})
print('ALL TASK 03 CHECKS PASSED')
PY
git diff --check
```

### Final CHECK results and handoff

- Ran `.venv/bin/python -B code/partial_correlation.py`: exit 0, saved all
  nine periods. Ran all four fenced Python check blocks with the command
  above: exit 0 and `ALL TASK 03 CHECKS PASSED`. `git diff --check` passed.
- Input CHECK: both files read correctly at full precision; each residual
  period's n_obs agrees with Task 02 and every prescribed Friday is present.
  No rows dropped, filled or pooled. Invalid-key/value/count cases rejected.
- Period CHECK: nine rows in proposal order, including Before AI boom;
  n_obs = 1913, 1717, 196, 530, 139, 239, 92, 574, 104.
- Calculation CHECK: every residual correlation matches the analytic formula
  within 1e-12 absolute / 1e-10 relative tolerance; maximum error 1.22e-15.
  Independently checked against scipy.stats.pearsonr within 1e-12 absolute /
  relative. All values are in [-1, 1], without clipping. Synthetic known
  positive/negative/zero correlations meet 1e-12 tolerances; exact +1/−1
  cases, constant residuals and other invalid inputs tested successfully.
- Descriptive-statistics CHECK: every Panel A/B value agrees with unrounded
  Task 02 statistics and partial correlations after three-decimal rounding;
  N is integer. Input order changes do not affect the one-to-one join or
  output order. Unrounded source frames remain unchanged.
- File-output CHECK: generated only by the task script:
  - `output/descriptive_statistics.xlsx`: Panel A (9×6) and Panel B (9×4),
    separate worksheets with proposal labels, group separators, numeric
    three-decimal formats and percent units without rescaling.
  - `output/partial_correlations.csv`: 9×3, exact floating-point round trip,
    `period,n_obs,partial_correlation`, no index.
- Checked every Excel cell/header/title, blank separators, number formats,
  freezes and page settings. Alternate paths and invalid panels rejected;
  an injected write error propagates. No actual validation failures remain.
- SHA-256 comparisons confirm all four Task 01/02 generated files are
  unchanged from the baseline above. Only code/partial_correlation.py,
  tasks/README.md (Task 03 status) and this log are committed. Generated
  outputs are ignored and not staged. No dependency or protected-source edits.
- Status set to Ready for Review after all CHECK criteria passed. No open
  implementation issues or methodological deviations. The known nonfatal
  Git global ignore-file warning remains unrelated to the checks.
- Researcher verification: independently inspect the four-step diff, rerun
  the script and checks above, and view the Excel layout in a spreadsheet
  application. Human acceptance and merge remain pending; do not mark
  Completed before explicit approval. H3 testing belongs to Task 04.
- Final commit includes saving, final checks and Ready for Review status.
  Stop after Task 03; no push, pull request, merge or Task 04 execution.
