"""Test the four prespecified H1a/H1b/H2/H3 alternatives using weekly data.

Returns remain in source percent units. Regression inference uses four-lag
asymptotic Newey–West covariance; all p-values use the standard normal law.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.regression.linear_model import OLS


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "output"
WEEKLY_PATH = OUTPUT_DIR / "weekly_returns.csv"
STATISTICS_PATH = OUTPUT_DIR / "regression_statistics.csv"
PARTIAL_PATH = OUTPUT_DIR / "partial_correlations.csv"
HAC_LAGS = 4
AI_START = pd.Timestamp("2022-12-01")
PERIODS = (
    ("Full Sample", "1990-01-01", "2026-08-28"),
    ("Before AI boom", "1990-01-01", "2022-11-30"),
    ("AI boom", "2022-12-01", "2026-08-28"),
    ("Pre-Dot-Com", "1990-01-01", "2000-02-29"),
    ("Dot-com Crash", "2000-03-01", "2002-10-31"),
    ("Pre Financial Crisis", "2002-11-01", "2007-05-31"),
    ("Financial Crisis", "2007-06-01", "2009-02-28"),
    ("Pre-COVID", "2009-03-01", "2020-02-29"),
    ("COVID", "2020-03-01", "2022-02-28"),
)
PERIOD_NAMES = [name for name, _, _ in PERIODS]
WEEKLY_COLUMNS = ["week_end", "utilities_excess", "technology_excess", "market_excess"]
STATISTICS_REQUIRED = [
    "period", "n_obs", "hac_lags", "beta_U", "se_beta_U", "t_beta_1_U", "p_beta_1_U",
    "beta_T", "se_beta_T", "t_beta_1_T", "p_beta_1_T",
]
PARTIAL_COLUMNS = ["period", "n_obs", "partial_correlation"]
RESULT_COLUMNS = [
    "hypothesis", "estimate", "std_error", "test_statistic", "p_value_one_sided",
    "n_obs", "n_obs_bai", "n_obs_ai", "hac_lags",
]
HYPOTHESES = ["H1a", "H1b", "H2", "H3"]


def _period_row(table, period, columns):
    if not table.columns.is_unique or not {"period", *columns}.issubset(table.columns):
        raise ValueError(f"{period}: missing or duplicate input columns")
    matched = table.loc[table["period"].eq(period)]
    if len(matched) != 1:
        raise ValueError(f"Expected exactly one {period} row")
    row = matched.iloc[0]
    if not np.isfinite(row[columns].to_numpy(dtype=float)).all():
        raise ValueError(f"{period}: nonfinite values")
    return row


def _result_frame(rows):
    """Keep optional count/lag metadata nullable; never round test statistics."""
    result = pd.DataFrame(rows, columns=RESULT_COLUMNS)
    for column in ("n_obs", "n_obs_bai", "n_obs_ai", "hac_lags"):
        result[column] = pd.array(result[column], dtype="Int64")
    numeric = result[["estimate", "std_error", "test_statistic", "p_value_one_sided", "n_obs"]]
    if (not np.isfinite(numeric.to_numpy(dtype=float)).all()
            or (result["std_error"] <= 0).any()
            or not result["p_value_one_sided"].between(0, 1).all()
            or (result["n_obs"] < 1).any()):
        raise ValueError("Nonfinite or invalid hypothesis test results")
    return result


def _validate_period_table(table, required, name):
    if (not table.columns.is_unique or not set(required).issubset(table.columns)
            or table["period"].isna().any() or table["period"].duplicated().any()
            or set(table["period"]) != set(PERIOD_NAMES)):
        raise ValueError(f"{name}: missing columns or missing/duplicate proposal periods")
    if not np.isfinite(table[required[1:]].to_numpy(dtype=float)).all():
        raise ValueError(f"{name}: nonfinite values")
    n = table["n_obs"].to_numpy(dtype=float)
    if (n < 1).any() or (n != np.floor(n)).any():
        raise ValueError(f"{name}: invalid observation counts")


def _validate_weekly(weekly):
    if list(weekly.columns) != WEEKLY_COLUMNS:
        raise ValueError("Invalid weekly return columns")
    dates = weekly["week_end"]
    if (not pd.api.types.is_datetime64_any_dtype(dates) or dates.isna().any()
            or dates.duplicated().any() or not dates.is_monotonic_increasing
            or (dates.dt.dayofweek != 4).any() or len(weekly) == 0):
        raise ValueError("Expected unique chronological Friday labels")
    if not np.isfinite(weekly[WEEKLY_COLUMNS[1:]].to_numpy(dtype=float)).all():
        raise ValueError("Nonfinite weekly returns")


def load_inputs(weekly_path, statistics_path, partial_path):
    """Read inputs unchanged in units and validate coverage and matching counts."""
    weekly = pd.read_csv(weekly_path, float_precision="round_trip")
    statistics = pd.read_csv(statistics_path, float_precision="round_trip")
    partial = pd.read_csv(partial_path, float_precision="round_trip")
    if list(weekly.columns) != WEEKLY_COLUMNS:
        raise ValueError("Invalid weekly return columns")
    dates = weekly["week_end"].astype("string")
    if not dates.str.fullmatch(r"\d{4}-\d{2}-\d{2}").fillna(False).all():
        raise ValueError("Expected ISO YYYY-MM-DD dates")
    weekly["week_end"] = pd.to_datetime(dates, format="%Y-%m-%d", errors="raise")
    _validate_weekly(weekly)
    expected = pd.date_range("1990-01-01", "2026-08-28", freq="W-FRI")
    if not pd.DatetimeIndex(weekly["week_end"]).equals(expected):
        raise ValueError("Weekly input does not contain every fixed-sample Friday")
    _validate_period_table(statistics, STATISTICS_REQUIRED, "Regression statistics")
    _validate_period_table(partial, PARTIAL_COLUMNS, "Partial correlations")
    if not statistics["hac_lags"].eq(HAC_LAGS).all():
        raise ValueError("Task 02 must use four HAC lags")
    for sector in ("U", "T"):
        if ((statistics[f"se_beta_{sector}"] <= 0).any()
                or not statistics[f"p_beta_1_{sector}"].between(0, 1).all()):
            raise ValueError("Invalid Task 02 standard errors or p-values")
    if (partial["partial_correlation"].abs() > 1).any():
        raise ValueError("Task 03 correlation outside [-1, 1]")
    ss, pp = statistics.set_index("period"), partial.set_index("period")
    for period, start, end in PERIODS:
        n = weekly["week_end"].between(start, end).sum()
        if n != ss.loc[period, "n_obs"] or n != pp.loc[period, "n_obs"]:
            raise ValueError(f"{period}: n_obs differs across inputs")
    return weekly, statistics, partial


def test_h1(regression_statistics):
    """Test full-sample utilities beta < 1 and technology beta > 1."""
    row = _period_row(regression_statistics, "Full Sample", [
        "n_obs", "beta_U", "se_beta_U", "beta_T", "se_beta_T",
    ])
    if row.n_obs < 1 or row.n_obs != np.floor(row.n_obs):
        raise ValueError("Invalid Full Sample observation count")
    results = []
    for hypothesis, sector in [("H1a", "U"), ("H1b", "T")]:
        beta, se = row[f"beta_{sector}"], row[f"se_beta_{sector}"]
        if se <= 0:
            raise ValueError(f"{hypothesis}: nonpositive beta standard error")
        statistic = (beta - 1) / se
        # sf avoids cancellation in 1 - cdf for very large positive t values.
        p = norm.cdf(statistic) if hypothesis == "H1a" else norm.sf(statistic)
        results.append([hypothesis, beta, se, statistic, p, row.n_obs, None, None, HAC_LAGS])
    return _result_frame(results)


def _fit_h2(weekly):
    """Fit the prespecified pooled model, retaining chronological HAC ordering."""
    _validate_weekly(weekly)
    market = weekly["market_excess"].to_numpy(dtype=float)
    dummy = (weekly["week_end"] >= AI_START).to_numpy(dtype=float)
    n_ai, n_bai = int(dummy.sum()), int(len(dummy) - dummy.sum())
    if n_ai == 0 or n_bai == 0 or len(weekly) <= 4:
        raise ValueError("H2 requires observations in both periods and residual degrees of freedom")
    design = np.column_stack([np.ones(len(weekly)), dummy, market, dummy * market])
    if np.linalg.matrix_rank(design) != 4:
        raise ValueError("Singular H2 dummy/interacted-market design")
    fit = OLS(weekly["utilities_excess"].to_numpy(dtype=float), design, missing="raise").fit(
        cov_type="HAC", use_t=False,
        cov_kwds={"maxlags": HAC_LAGS, "kernel": "bartlett", "use_correction": False},
    )
    if (not np.isfinite(fit.params).all() or not np.isfinite(fit.bse).all()
            or not np.isfinite(fit.resid).all() or fit.bse[3] <= 0):
        raise ValueError("Nonfinite H2 results or nonpositive gamma standard error")
    return fit, n_bai, n_ai


def test_h2(weekly):
    """Test gamma = beta_AI - beta_BAI > 0 using four-lag Newey–West SEs."""
    fit, n_bai, n_ai = _fit_h2(weekly)
    gamma, se = fit.params[3], fit.bse[3]
    statistic = gamma / se
    result = _result_frame([[
        "H2", gamma, se, statistic, norm.sf(statistic), len(weekly), n_bai, n_ai, HAC_LAGS,
    ]])
    # In-memory coefficients support verification of the separate period slopes.
    result.attrs["coefficients"] = dict(zip(["alpha", "delta", "beta", "gamma"], fit.params))
    return result
