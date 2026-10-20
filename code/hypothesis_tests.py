"""Test the four prespecified H1a/H1b/H2/H3 alternatives using weekly data.

Returns remain in source percent units. Regression inference uses four-lag
asymptotic Newey–West covariance; all p-values use the standard normal law.
"""

from pathlib import Path

import numpy as np
import pandas as pd


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
