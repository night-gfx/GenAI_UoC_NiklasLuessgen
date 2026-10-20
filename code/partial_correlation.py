"""Describe utilities–technology co-movement after controlling for the market.

Task 02 residuals remain separate by period; weekly volatilities retain percent
units (0.02 denotes 0.02 percent). No significance tests are performed here.
"""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "output"
RESIDUALS_PATH = OUTPUT_DIR / "market_residuals.csv"
STATISTICS_PATH = OUTPUT_DIR / "regression_statistics.csv"
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
RESIDUAL_COLUMNS = [
    "period", "week_end", "utilities_residual", "technology_residual", "market_excess",
]
STATISTICS_REQUIRED = [
    "period", "n_obs", "corr_UT", "corr_UM", "corr_TM", "vol_U", "vol_T", "vol_M",
]


def _validate_periods(table, name):
    """Require exactly one row per prescribed period, irrespective of input order."""
    if (not table.columns.is_unique or "period" not in table.columns
            or table["period"].isna().any() or table["period"].duplicated().any()
            or set(table["period"]) != set(PERIOD_NAMES)):
        raise ValueError(f"{name}: expected exactly the nine unique proposal periods")


def _validate_residuals(residuals):
    """Validate residual keys/values without dropping, filling or pooling rows."""
    if list(residuals.columns) != RESIDUAL_COLUMNS:
        raise ValueError("Invalid residual columns")
    if (residuals[["period", "week_end"]].isna().any().any()
            or residuals.duplicated(["period", "week_end"]).any()
            or set(residuals["period"]) != set(PERIOD_NAMES)):
        raise ValueError("Missing, duplicate or unknown residual keys")
    if not np.isfinite(residuals[RESIDUAL_COLUMNS[2:]].to_numpy(dtype=float)).all():
        raise ValueError("Nonfinite residual values")


def _validate_statistics(statistics):
    _validate_periods(statistics, "Regression statistics")
    if not set(STATISTICS_REQUIRED).issubset(statistics.columns):
        raise ValueError("Missing regression statistics columns")
    numeric = statistics[STATISTICS_REQUIRED[1:]].to_numpy(dtype=float)
    if not np.isfinite(numeric).all():
        raise ValueError("Nonfinite regression statistics")
    n = statistics["n_obs"].to_numpy(dtype=float)
    if (n < 2).any() or (n != np.floor(n)).any():
        raise ValueError("Invalid regression observation counts")
    if (statistics[["corr_UT", "corr_UM", "corr_TM"]].abs() > 1).any().any():
        raise ValueError("Invalid input correlations")
    if (statistics[["vol_U", "vol_T", "vol_M"]] <= 0).any().any():
        raise ValueError("Nonpositive weekly volatility")


def load_inputs(residuals_path, statistics_path):
    """Read Task 02 inputs; reject missing weeks, invalid keys and count mismatches."""
    residuals = pd.read_csv(residuals_path, float_precision="round_trip")
    statistics = pd.read_csv(statistics_path, float_precision="round_trip")
    _validate_residuals(residuals)
    _validate_statistics(statistics)
    dates = residuals["week_end"].astype("string")
    if not dates.str.fullmatch(r"\d{4}-\d{2}-\d{2}").fillna(False).all():
        raise ValueError("Expected ISO YYYY-MM-DD residual dates")
    residuals["week_end"] = pd.to_datetime(dates, format="%Y-%m-%d", errors="raise")
    keyed_statistics = statistics.set_index("period")
    for period, start, end in PERIODS:
        group = residuals.loc[residuals["period"].eq(period)]
        expected = pd.date_range(start, end, freq="W-FRI")
        if not pd.DatetimeIndex(group["week_end"]).equals(expected):
            raise ValueError(f"{period}: expected every prescribed Friday exactly once in order")
        if len(group) != keyed_statistics.loc[period, "n_obs"]:
            raise ValueError(f"{period}: residual count differs from Task 02 n_obs")
        for column, actual in [("first_week", expected[0]), ("last_week", expected[-1])]:
            if column in statistics and pd.Timestamp(keyed_statistics.loc[period, column]) != actual:
                raise ValueError(f"{period}: {column} differs from residual dates")
    return residuals, statistics
