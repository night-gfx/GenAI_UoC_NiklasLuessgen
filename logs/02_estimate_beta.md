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
