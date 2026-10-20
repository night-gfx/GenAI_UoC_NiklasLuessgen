"""Prepare Monday–Friday excess returns from the original French daily CSVs.

Input and output returns use percent units: 0.02 denotes 0.02 percent.
"""

import csv
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDUSTRY_PATH = PROJECT_ROOT / "data/12_Industry_Portfolios_Daily.csv"
FACTORS_PATH = PROJECT_ROOT / "data/F-F_Research_Data_Factors_daily.csv"
OUTPUT_PATH = PROJECT_ROOT / "output/weekly_returns.csv"
SAMPLE_START = pd.Timestamp("1990-01-01")
SAMPLE_END = pd.Timestamp("2026-08-28")


def _read_daily_block(path, *, section=None):
    """Read one CSV block as strings, preserving invalid cells for validation."""
    with Path(path).open(encoding="utf-8-sig", newline="") as source:
        lines = source.readlines()
    if section is not None:
        matches = [i for i, line in enumerate(lines) if line.strip() == section]
        if len(matches) != 1:
            raise ValueError(f"{path}: expected exactly one {section!r} section")
        header_position = matches[0] + 1
    else:
        matches = [
            i for i, line in enumerate(lines)
            if line.lstrip().startswith(",Mkt-RF,")
        ]
        if len(matches) != 1:
            raise ValueError(f"{path}: expected exactly one daily factor header")
        header_position = matches[0]
    rows = csv.reader(lines[header_position:], strict=True)
    header = [cell.strip() for cell in next(rows)]
    if not header or header[0] or len(set(header)) != len(header):
        raise ValueError(f"{path}: malformed daily CSV header")
    header[0] = "date"
    records = []
    for row in rows:
        if not row or all(not cell.strip() for cell in row):
            break
        if len(row) != len(header):
            raise ValueError(f"{path}: malformed daily CSV row {row!r}")
        records.append([cell.strip() for cell in row])
    if not records:
        raise ValueError(f"{path}: empty daily return block")
    table = pd.DataFrame(records, columns=header, dtype=str)
    table.attrs.update(source=str(path), units="percent", section=section or "daily factors")
    return table


def load_daily_returns(industry_path, factors_path):
    """Return raw value-weighted industry and factor tables without scaling."""
    industry = _read_daily_block(
        industry_path, section="Average Value Weighted Returns -- Daily"
    )
    factors = _read_daily_block(factors_path)
    return industry, factors


def _sample_table(table, columns, name):
    """Validate raw dates/units and return a numeric copy of the fixed sample."""
    required = {"date", *columns}
    if not table.columns.is_unique or not required.issubset(table.columns):
        raise ValueError(f"{name}: missing or duplicate required columns")
    if table.attrs.get("units") != "percent":
        raise ValueError(f"{name}: expected source percent units")
    date_text = table["date"].astype("string")
    if not date_text.str.fullmatch(r"\d{8}").fillna(False).all():
        raise ValueError(f"{name}: invalid YYYYMMDD dates")
    dates = pd.DatetimeIndex(pd.to_datetime(date_text, format="%Y%m%d", errors="raise"))
    if dates.has_duplicates or not dates.is_monotonic_increasing:
        raise ValueError(f"{name}: duplicate or unordered dates")
    if dates.empty or dates.min() > SAMPLE_START or dates.max() < SAMPLE_END:
        raise ValueError(f"{name}: source does not span the fixed sample")
    in_sample = (dates >= SAMPLE_START) & (dates <= SAMPLE_END)
    sample = table.loc[in_sample, list(columns)].apply(pd.to_numeric, errors="raise")
    sample.index = dates[in_sample]
    if sample.empty or (sample.index.dayofweek > 4).any():
        raise ValueError(f"{name}: empty sample or weekend observations")
    values = sample.to_numpy(dtype=float)
    if not np.isfinite(values).all() or np.isin(values, [-99.99, -999]).any():
        raise ValueError(f"{name}: missing markers or nonfinite daily values")
    if (values < -100).any():
        raise ValueError(f"{name}: daily return below -100 percent")
    return sample.astype(float)


def _aligned_sample(industry, factors):
    """Check daily coverage before joining, so no observation is silently lost."""
    sectors = _sample_table(industry, ("Utils", "BusEq"), "industry")
    market = _sample_table(factors, ("Mkt-RF", "RF"), "factors")
    if not sectors.index.equals(market.index):
        only_industry = sectors.index.difference(market.index).strftime("%Y-%m-%d").tolist()
        only_factors = market.index.difference(sectors.index).strftime("%Y-%m-%d").tolist()
        raise ValueError(
            f"Daily sample coverage differs: industry only={only_industry}; "
            f"factors only={only_factors}"
        )
    daily = sectors.join(market)
    daily["market_total"] = daily["Mkt-RF"] + daily["RF"]
    if (daily["market_total"] < -100).any():
        raise ValueError("Reconstructed daily market return below -100 percent")
    labels = daily.index.to_period("W-FRI").end_time.normalize()
    expected = pd.date_range(SAMPLE_START, SAMPLE_END, freq="W-FRI")
    if not pd.DatetimeIndex(labels.unique()).equals(expected):
        raise ValueError("Missing shared sample weeks or incomplete sample boundaries")
    return daily


def validate_daily_returns(industry, factors):
    """Reject invalid selected daily series; never mutate, fill or drop input rows.

    Values are checked within the predefined sample; full-block dates must be
    valid, unique, ordered and span it. Percent units follow the raw sources'
    documented convention, not an inference from the size of observed returns.
    """
    _aligned_sample(industry, factors)


def calculate_weekly_returns(
    industry, factors, week_rule="W-FRI", boundary_rule="full_sample_weeks"
):
    """Compound each total return and RF separately, then subtract weekly RF.

    Only W-FRI and full_sample_weeks are supported: sample boundaries enclose
    whole Monday–Friday weeks; all observed trading days, including short holiday
    weeks, are kept. Labels remain Friday even when Friday itself is a holiday.
    """
    if week_rule != "W-FRI" or boundary_rule != "full_sample_weeks":
        raise ValueError("Use W-FRI with full_sample_weeks; other rules are not approved")
    if SAMPLE_START.dayofweek != 0 or SAMPLE_END.dayofweek != 4:
        raise ValueError("Fixed sample boundaries must enclose full Monday–Friday weeks")
    daily = _aligned_sample(industry, factors)
    labels = daily.index.to_period(week_rule).end_time.normalize()
    gross = 1 + daily[["Utils", "BusEq", "market_total", "RF"]] / 100
    totals = 100 * (gross.groupby(labels).prod() - 1)
    excess = totals[["Utils", "BusEq", "market_total"]].subtract(totals["RF"], axis=0)
    if not np.isfinite(excess.to_numpy()).all():
        raise ValueError("Nonfinite compounded weekly returns")
    weekly = excess.rename(columns={
        "Utils": "utilities_excess",
        "BusEq": "technology_excess",
        "market_total": "market_excess",
    }).rename_axis("week_end").reset_index()
    weekly.attrs["units"] = "percent"
    return weekly
