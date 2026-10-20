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
