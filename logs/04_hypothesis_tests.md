# Task 04: Test Hypotheses

## 2026-10-21 — Researcher approval, branch and preconditions

- Researcher explicitly approved Task 03: "ok gut bitte schliese das ab ist
  reviewed un mache letzten schritt". Initially stopped on main without edits.
  After retry, branch is the researcher-prepared `agent/04_hypothesis_tests`;
  `git status --short` and `git diff --cached` confirm a clean, unstaged tree.
- This prepared branch starts before Task 03's code commits: its overview
  still says Planned, and code/partial_correlation.py is absent. The reviewed
  implementation and successful checks remain on agent/03_partial_correlation
  at ea2fc4899e474280c9d34c8bbe21e89b143b9759. Read that branch's log read-only
  with `git show`; the local Task 03 outputs are present and unchanged.
- Applied the researcher's explicit prior authorization to set Task 03 to
  Completed despite the stale overview on this branch. This one status edit
  is explicitly authorized beyond Task 04's normal status-only boundary.
  No Task 03 code was copied, changed or merged. Integration of that reviewed
  branch remains the researcher's responsibility; Task 04 uses its local CSV.
- Reused research-task-workflow, read proposal.md, AGENTS.md, tasks/README.md
  and tasks/04_hypothesis_tests.md. Tasks 01–03 now Completed; Task 04 In Progress.
- Inputs exist/read correctly: weekly 1913×4, regression statistics 9×27,
  partial correlations 9×3. openpyxl 3.1.5 installed. No dependency changes.
- `git check-ignore` confirms both requested outputs are ignored. Scope is
  code/hypothesis_tests.py, this log, Task 04 status, the explicitly approved
  Task 03 status, and the two outputs generated only by the task script.
- Known nonfatal global Git ignore-file warning continues; commands succeed.
- Baseline SHA-256 hashes, obtained with `.venv/bin/python -B` and hashlib:

```text
weekly_returns.csv 40c2d638d4426384766d3b22b69c84043e3d29aa74b532421cc646a3078d9365
regression_table.xlsx bd78cc5cafb1c0b1a9679f56bf6106421d2009e027b310f47af9987b0064245b
regression_statistics.csv 45516df4983ae2d6ca562b3d9c368b4e35ebe2f59f3f1ad100db090b6e8d7d57
market_residuals.csv 8083c7d59a1375e1744440749fd36f714f0521aa063e561d061f6982ccaf3c30
descriptive_statistics.xlsx 209bcdec1af1f09fc5c7142bc7d52830807fc88168d8eb7ef156c73e400c9048
partial_correlations.csv a80a0666f24f0b5236bf38e7c4a498b0acc49d18740d1501fcb255d5e4ddebc6
```

## Step 1 — Load and cross-check inputs

- Added load_inputs with source percent units unchanged, all fixed-sample
  Fridays, finite values, unique period keys, nine expected periods, valid
  SEs/p-values/correlations, four HAC lags and matching counts across all inputs.
- No filling, dropping or replacement of observations. Weeks are assigned
  by their Friday date with AI starting in December 2022.

### Step 1 check

```python
import sys
from unittest.mock import patch
import pandas as pd
import numpy as np
sys.path.insert(0, "code")
import hypothesis_tests as m
w, s, p = m.load_inputs(m.WEEKLY_PATH, m.STATISTICS_PATH, m.PARTIAL_PATH)
raw = [pd.read_csv(path, float_precision="round_trip") for path in (m.WEEKLY_PATH, m.STATISTICS_PATH, m.PARTIAL_PATH)]
pd.testing.assert_frame_equal(w.drop(columns="week_end"), raw[0].drop(columns="week_end"), check_exact=True)
pd.testing.assert_frame_equal(s, raw[1], check_exact=True)
pd.testing.assert_frame_equal(p, raw[2], check_exact=True)
assert len(w) == 1913
for period, n in [("Full Sample", 1913), ("Before AI boom", 1717), ("AI boom", 196)]:
    assert s.set_index("period").loc[period, "n_obs"] == p.set_index("period").loc[period, "n_obs"] == n
invalid = [
    (raw[0].iloc[:-1], raw[1], raw[2]),
    (pd.concat([raw[0], raw[0].iloc[:1]]), raw[1], raw[2]),
    (raw[0], raw[1].iloc[:-1], raw[2]),
    (raw[0], raw[1], raw[2].iloc[:-1]),
    (raw[0], pd.concat([raw[1], raw[1].iloc[:1]]), raw[2]),
    (raw[0], raw[1], pd.concat([raw[2], raw[2].iloc[:1]])),
    (raw[0], raw[1].assign(n_obs=1), raw[2]),
    (raw[0], raw[1], raw[2].assign(n_obs=1)),
    (raw[0].assign(utilities_excess=np.nan), raw[1], raw[2]),
    (raw[0], raw[1].assign(hac_lags=3), raw[2]),
    (raw[0], raw[1].assign(se_beta_U=0), raw[2]),
    (raw[0], raw[1], raw[2].assign(partial_correlation=1.01)),
    (raw[0].drop(columns="market_excess"), raw[1], raw[2]),
]
for values in invalid:
    with patch.object(m.pd, "read_csv", side_effect=[value.copy() for value in values]):
        try:
            m.load_inputs(m.WEEKLY_PATH, m.STATISTICS_PATH, m.PARTIAL_PATH)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid input accepted")
print("PASS: exact numeric preservation, all-period count agreement, 13 invalid input combinations")
```

Checks are reproducible by executing each fenced Python block with
`.venv/bin/python -B` from the project root.

- Step 1 check executed with `.venv/bin/python -B`: PASS for numeric input
  preservation, counts in all nine periods and 13 rejection cases.
  `git diff --check` passed before staging this checked step.

## Step 2 — H1 one-sided beta tests

- Step 1 commit: `e083347aefd0a92985cf9db9de2ee0a7dcc5b074`; author verified
  as Codex. Added H1a/H1b using the Full Sample betas and SEs from Task 02.
- H1a uses the normal left tail; H1b uses the normal survival function,
  equivalent to 1−Φ(t) but stable for small p-values. No coefficients are refit.
- CSV fields n_obs_bai/n_obs_ai are not applicable to H1 and are blank;
  hac_lags is 4. Nullable integer fields preserve integer formatting.

### Step 2 check

```python
import sys
from math import erfc, sqrt
import numpy as np
import pandas as pd
sys.path.insert(0, "code")
import hypothesis_tests as m
w, s, p = m.load_inputs(m.WEEKLY_PATH, m.STATISTICS_PATH, m.PARTIAL_PATH)
original = s.copy(deep=True)
h = m.test_h1(s).set_index("hypothesis")
full = s.set_index("period").loc["Full Sample"]
for hypothesis, sector, left in [("H1a", "U", True), ("H1b", "T", False)]:
    row = h.loc[hypothesis]
    t, p_two = full[f"t_beta_1_{sector}"], full[f"p_beta_1_{sector}"]
    np.testing.assert_allclose(row.test_statistic, t, atol=1e-12, rtol=1e-12)
    correct_direction = t < 0 if left else t > 0
    expected = p_two/2 if correct_direction else 1-p_two/2
    np.testing.assert_allclose(row.p_value_one_sided, expected, atol=1e-15, rtol=1e-12)
    assert row.estimate == full[f"beta_{sector}"] and row.std_error == full[f"se_beta_{sector}"]
    assert row.n_obs == 1913 and row.hac_lags == 4
    assert pd.isna(row.n_obs_bai) and pd.isna(row.n_obs_ai)
for t in (-40., -2., 0., 2., 40.):
    modified = s.copy()
    select = modified.period.eq("Full Sample")
    for sector in ("U", "T"):
        modified.loc[select, f"beta_{sector}"] = 1 + t*0.1
        modified.loc[select, f"se_beta_{sector}"] = 0.1
    synthetic = m.test_h1(modified).set_index("hypothesis")
    np.testing.assert_allclose(synthetic.loc["H1a", "p_value_one_sided"], erfc(-t/sqrt(2))/2, atol=1e-15, rtol=1e-12)
    np.testing.assert_allclose(synthetic.loc["H1b", "p_value_one_sided"], erfc(t/sqrt(2))/2, atol=1e-15, rtol=1e-12)
for bad in [s.loc[s.period.ne("Full Sample")], pd.concat([s, s.iloc[:1]]),
            s.assign(se_beta_U=0), s.assign(se_beta_T=np.inf), s.assign(beta_U=np.nan)]:
    try:
        m.test_h1(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid H1 input accepted")
pd.testing.assert_frame_equal(s, original, check_exact=True)
print("PASS: H1 matches Task 02, both one-sided tails including reversed/null/extreme cases, 5 invalid cases")
print(h.to_string())
```

- Step 2 block executed with `.venv/bin/python -B`: PASS. H1 test statistics
  match Task 02 within 1e-12 absolute/relative; p-values meet 1e-15 absolute /
  1e-12 relative tolerance, including wrong-direction, zero and extreme t.
  Five invalid H1 cases rejected; source statistics unchanged.
  Actual p-values: H1a 5.666856e-17, H1b 2.405260e-09.
  `git diff --check` passed.

## Step 3 — H2 pooled dummy/interaction regression

- Step 2 commit: `9f732ed6053f91ef13e4b51cc911364741fe4188`; Codex author
  verified. Added test_h2 using intercept, AI dummy, market and dummy×market.
  AI starts on December 2022 Friday labels; before/AI weeks remain chronological.
- HAC exactly follows Task 02: four lags, Bartlett weights, no finite-sample
  multiplier, normal inference. Point estimates remain OLS. Invalid inputs,
  absent comparison periods, singular designs and nonfinite results fail.
- H2's split counts are recorded; coefficients are retained only in DataFrame
  metadata for checks, without extra output files or columns.

### Step 3 check

```python
import sys
from math import erfc, sqrt
import numpy as np
import pandas as pd
sys.path.insert(0, "code")
import hypothesis_tests as m
w, s, p = m.load_inputs(m.WEEKLY_PATH, m.STATISTICS_PATH, m.PARTIAL_PATH)
original = w.copy(deep=True)
result = m.test_h2(w)
row = result.iloc[0]
ss = s.set_index("period")
np.testing.assert_allclose(row.estimate, ss.loc["AI boom", "beta_U"]-ss.loc["Before AI boom", "beta_U"], atol=1e-12, rtol=1e-10)
np.testing.assert_allclose(result.attrs["coefficients"]["beta"], ss.loc["Before AI boom", "beta_U"], atol=1e-12, rtol=1e-10)
assert row.n_obs == 1913 and row.n_obs_bai == 1717 and row.n_obs_ai == 196 and row.hac_lags == 4
x = w.market_excess.to_numpy()
d = (w.week_end >= pd.Timestamp("2022-12-01")).to_numpy(dtype=float)
design = np.column_stack([np.ones(len(w)), d, x, d*x])
coefficients = np.linalg.lstsq(design, w.utilities_excess.to_numpy(), rcond=None)[0]
residuals = w.utilities_excess.to_numpy() - design@coefficients
inverse = np.linalg.inv(design.T@design)
# Independent Newey–West: explicit scalar lag sums for all 16 matrix entries.
scores = design*residuals[:, None]
meat = np.zeros((4, 4))
for j in range(4):
    for k in range(4):
        meat[j, k] = sum(scores[t, j]*scores[t, k] for t in range(len(w)))
        for lag in range(1, 5):
            meat[j, k] += (1-lag/5)*sum(
                scores[t, j]*scores[t-lag, k] + scores[t-lag, j]*scores[t, k]
                for t in range(lag, len(w)))
independent_se = np.sqrt(np.diag(inverse@meat@inverse))
fit, _, _ = m._fit_h2(w)
np.testing.assert_allclose(fit.params, coefficients, atol=1e-12, rtol=1e-12)
np.testing.assert_allclose(fit.bse, independent_se, atol=1e-12, rtol=1e-10)
np.testing.assert_allclose(row.std_error, independent_se[3], atol=1e-12, rtol=1e-10)
np.testing.assert_allclose(row.test_statistic, coefficients[3]/independent_se[3], atol=1e-10, rtol=1e-10)
np.testing.assert_allclose(row.p_value_one_sided, erfc(row.test_statistic/sqrt(2))/2, atol=1e-15, rtol=1e-12)
# Independent within-period slopes also imply the pooled slope and difference.
slopes = [np.cov(w.utilities_excess.to_numpy()[d == group], x[d == group], ddof=1)[0, 1]/np.var(x[d == group], ddof=1) for group in (0, 1)]
np.testing.assert_allclose([coefficients[2], coefficients[3]], [slopes[0], slopes[1]-slopes[0]], atol=1e-12, rtol=1e-12)

rng = np.random.default_rng(20261021)
dates = pd.date_range("2021-01-01", periods=180, freq="W-FRI")
x = rng.normal(size=len(dates)); d = (dates >= pd.Timestamp("2022-12-01")).astype(float)
design = np.column_stack([np.ones(len(dates)), d, x, d*x])
noise = rng.normal(size=len(dates))
noise -= design@np.linalg.lstsq(design, noise, rcond=None)[0]
for gamma in (-0.3, 0., 0.35):
    expected = np.array([0.2, -0.4, 0.55, gamma])
    synthetic = pd.DataFrame({"week_end": dates, "utilities_excess": design@expected+noise,
                              "technology_excess": rng.normal(size=len(dates)), "market_excess": x})
    recovered = m.test_h2(synthetic)
    np.testing.assert_allclose(list(recovered.attrs["coefficients"].values()), expected, atol=1e-12, rtol=1e-12)
    if gamma:
        assert np.sign(recovered.iloc[0].test_statistic) == np.sign(gamma)
for bad in [w.loc[w.week_end < m.AI_START], w.loc[w.week_end >= m.AI_START],
            w.assign(market_excess=1.), w.assign(utilities_excess=np.nan), w.iloc[::-1]]:
    try:
        m.test_h2(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid H2 input accepted")
pd.testing.assert_frame_equal(w, original, check_exact=True)
print(f"PASS: H2 period identities and independent HAC; max SE error={np.max(np.abs(fit.bse-independent_se)):.3g}")
print("PASS: synthetic negative/zero/positive beta differences; 5 invalid cases")
print(result.to_string(index=False))
```

- Ran Step 3 with `.venv/bin/python -B`: PASS for the pooled BAI slope and
  gamma difference versus Task 02 (1e-12 absolute / 1e-10 relative tolerance),
  independent covariance/variance slopes, all four OLS coefficients and all
  four independent HAC SEs (1e-12 absolute / 1e-10 relative). Maximum SE error
  6.25e-17. t/p-value checks passed at declared tolerances in the block.
- Synthetic negative/zero/positive gamma coefficients recovered within
  1e-12 absolute/relative; five invalid H2 cases rejected. Source weekly
  observations unchanged. Actual gamma −0.286757, t −3.061409, one-sided
  p 0.998899: the prespecified alternative is an increase, not any change.
  `git diff --check` passed.

## Step 4 — H3 Fisher partial-correlation comparison

- Step 3 commit: `78fa2c98334155ff42ad3b89f41fb8545a2dd82a`; author
  verified as Codex. Added H3 using atanh(rho), the specified n−4 weights,
  the AI-minus-BAI difference and the normal right tail.
- H3 estimate is the raw correlation difference. Its CSV std_error is the
  denominator on the Fisher-z difference scale, not an SE for the raw
  correlation difference. H3's hac_lags field is blank (not applicable);
  no HAC adjustment is introduced into the fixed Fisher test.
- Missing/duplicate required periods, nonfinite values, integer counts <=4
  and correlations at or outside ±1 fail without clipping or changing inputs.

### Step 4 check

```python
import sys
from math import log, sqrt, erfc
import numpy as np
import pandas as pd
sys.path.insert(0, "code")
import hypothesis_tests as m
w, s, p = m.load_inputs(m.WEEKLY_PATH, m.STATISTICS_PATH, m.PARTIAL_PATH)
original = p.copy(deep=True)
row = m.test_h3(p).iloc[0]
keyed = p.set_index("period")
rho_bai, rho_ai = keyed.loc["Before AI boom", "partial_correlation"], keyed.loc["AI boom", "partial_correlation"]
n_bai, n_ai = int(keyed.loc["Before AI boom", "n_obs"]), int(keyed.loc["AI boom", "n_obs"])
z_bai = 0.5*log((1+rho_bai)/(1-rho_bai))
z_ai = 0.5*log((1+rho_ai)/(1-rho_ai))
denominator = sqrt(1/(n_ai-4)+1/(n_bai-4))
expected = (z_ai-z_bai)/denominator
np.testing.assert_allclose(row.test_statistic, expected, atol=1e-12, rtol=1e-12)
np.testing.assert_allclose(row.std_error, denominator, atol=1e-12, rtol=1e-12)
assert row.estimate == rho_ai-rho_bai and row.n_obs == n_bai+n_ai == 1913
assert row.n_obs_bai == n_bai and row.n_obs_ai == n_ai and pd.isna(row.hac_lags)
np.testing.assert_allclose(row.p_value_one_sided, erfc(expected/sqrt(2))/2, atol=1e-15, rtol=1e-12)
for rho in (-0.8, 0., 0.8):
    identical = p.assign(partial_correlation=rho)
    equal = m.test_h3(identical).iloc[0]
    assert equal.estimate == equal.test_statistic == 0 and equal.p_value_one_sided == 0.5
for left, right, sign in [(0.15, 0.5, 1), (0.5, 0.15, -1), (-0.4, 0.2, 1)]:
    synthetic = pd.DataFrame({"period": ["Before AI boom", "AI boom"],
        "n_obs": [160, 190], "partial_correlation": [left, right]})
    actual = m.test_h3(synthetic).iloc[0]
    hand = (0.5*log((1+right)/(1-right))-0.5*log((1+left)/(1-left)))/sqrt(1/186+1/156)
    np.testing.assert_allclose(actual.test_statistic, hand, atol=1e-12, rtol=1e-12)
    assert np.sign(actual.test_statistic) == sign
    np.testing.assert_allclose(actual.estimate, right-left, atol=1e-15, rtol=1e-12)
for bad in [p.loc[p.period.ne("AI boom")], pd.concat([p, p.loc[p.period.eq("AI boom")]]),
            p.assign(n_obs=4), p.assign(n_obs=4.5), p.assign(partial_correlation=1.),
            p.assign(partial_correlation=-1.), p.assign(partial_correlation=1.01),
            p.assign(partial_correlation=np.nan)]:
    try:
        m.test_h3(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid H3 input accepted")
pd.testing.assert_frame_equal(p, original, check_exact=True)
print("PASS: independent Fisher hand calculation, identical-correlation null, expected difference signs, 8 invalid cases")
print(m.test_h3(p).to_string(index=False))
```

- Ran Step 4's block with `.venv/bin/python -B`: PASS against the independent
  logarithm-based hand calculation (1e-12 absolute/relative); p-value check
  1e-15 absolute / 1e-12 relative. Identical correlations give exactly Z=0,
  p=0.5; positive/negative synthetic differences have the expected signs.
- All eight invalid H3 cases rejected and input partial correlations unchanged.
  Actual raw difference −0.104679, Z −1.691393, right-tail p 0.954619.
  Ordered this log's sections chronologically before committing.
  `git diff --check` passed.
