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
