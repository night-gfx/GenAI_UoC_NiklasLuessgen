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
