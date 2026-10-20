"""Estimate period-specific market betas from weekly excess returns.

Returns remain in source percent units: 0.02 denotes 0.02 percent.
"""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WEEKLY_PATH = PROJECT_ROOT / "output/weekly_returns.csv"
OUTPUT_DIR = PROJECT_ROOT / "output"
SAMPLE_START = pd.Timestamp("1990-01-01")
SAMPLE_END = pd.Timestamp("2026-08-28")
HAC_LAGS = 4
RETURN_COLUMNS = ["utilities_excess", "technology_excess", "market_excess"]
PERIODS = (
    ("Full Sample", "1990-01", "2026-08"),
    ("Before AI boom", "1990-01", "2022-11"),
    ("AI boom", "2022-12", "2026-08"),
    ("Pre-Dot-Com", "1990-01", "2000-02"),
    ("Dot-com Crash", "2000-03", "2002-10"),
    ("Pre Financial Crisis", "2002-11", "2007-05"),
    ("Financial Crisis", "2007-06", "2009-02"),
    ("Pre-COVID", "2009-03", "2020-02"),
    ("COVID", "2020-03", "2022-02"),
)
PERIOD_NAMES = [name for name, _, _ in PERIODS]


def load_weekly_returns(weekly_path):
    """Validate all fixed-sample Fridays and key unchanged returns by period/date.

    The six crisis subperiods partition Before AI boom except March–November
    2022. Full Sample and the before/AI split intentionally repeat observations.
    """
    weekly = pd.read_csv(weekly_path, float_precision="round_trip")
    if list(weekly.columns) != ["week_end", *RETURN_COLUMNS]:
        raise ValueError("Expected week_end and the three weekly excess-return columns")
    dates = weekly["week_end"].astype("string")
    if not dates.str.fullmatch(r"\d{4}-\d{2}-\d{2}").fillna(False).all():
        raise ValueError("Expected ISO YYYY-MM-DD week_end dates")
    weekly["week_end"] = pd.to_datetime(dates, format="%Y-%m-%d", errors="raise")
    expected = pd.date_range(SAMPLE_START, SAMPLE_END, freq="W-FRI")
    if not pd.DatetimeIndex(weekly["week_end"]).equals(expected):
        raise ValueError("Expected every fixed-sample Friday once, in chronological order")
    weekly[RETURN_COLUMNS] = weekly[RETURN_COLUMNS].apply(pd.to_numeric, errors="raise")
    if not np.isfinite(weekly[RETURN_COLUMNS].to_numpy(dtype=float)).all():
        raise ValueError("Nonfinite weekly excess returns; no rows may be filled or dropped")
    weekly = weekly.set_index("week_end")
    months = weekly.index.to_period("M")
    masks = {
        name: (months >= pd.Period(start, "M")) & (months <= pd.Period(end, "M"))
        for name, start, end in PERIODS
    }
    if any(not mask.any() for mask in masks.values()):
        raise ValueError("Empty comparison period")
    split = masks["Before AI boom"].astype(int) + masks["AI boom"].astype(int)
    crisis_count = np.sum([masks[name] for name in PERIOD_NAMES[3:]], axis=0)
    gap = (months >= pd.Period("2022-03", "M")) & (months <= pd.Period("2022-11", "M"))
    if not masks["Full Sample"].all() or not (split == 1).all():
        raise ValueError("Invalid Full Sample or before/AI partition")
    if not np.array_equal(crisis_count + gap, masks["Before AI boom"].astype(int)):
        raise ValueError("Overlapping or incomplete crisis subperiods")
    periods = pd.concat(
        [weekly.loc[masks[name]] for name in PERIOD_NAMES],
        keys=PERIOD_NAMES, names=["period", "week_end"],
    )
    periods.attrs["units"] = "percent"
    return periods
