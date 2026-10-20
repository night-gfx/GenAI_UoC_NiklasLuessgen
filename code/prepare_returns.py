"""Prepare Monday–Friday excess returns from the original French daily CSVs.

Input and output returns use percent units: 0.02 denotes 0.02 percent.
"""

import csv
from pathlib import Path

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
