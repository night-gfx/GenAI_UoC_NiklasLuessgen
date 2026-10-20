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
