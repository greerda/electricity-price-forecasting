"""Validation checks for cleaned, hourly market datasets."""

from __future__ import annotations

import pandas as pd


class DataValidationError(ValueError):
    """Raised when a dataset fails a required validation rule."""


def validate_required_columns(
    df: pd.DataFrame,
    required_columns: list[str],
) -> None:
    # Validate the schema early so later transformations fail with a clear
    # source-data message instead of a less informative pandas KeyError.
    missing = set(required_columns).difference(df.columns)

    if missing:
        raise DataValidationError(
            f"Missing required columns: {sorted(missing)}"
        )


def validate_unique_timestamps(
    df: pd.DataFrame,
    timestamp_column: str = "timestamp_utc",
) -> None:
    # One row must represent one market-location-hour.  Duplicate timestamps
    # can inflate observations and make later one-to-one joins invalid.
    duplicate_count = df[timestamp_column].duplicated().sum()

    if duplicate_count:
        raise DataValidationError(
            f"Found {duplicate_count} duplicate timestamps."
        )


def validate_chronological_order(
    df: pd.DataFrame,
    timestamp_column: str = "timestamp_utc",
) -> None:
    # Ordered timestamps are required for positional lags, rolling windows,
    # and chronological train/validation/test splits.
    if not df[timestamp_column].is_monotonic_increasing:
        raise DataValidationError(
            f"{timestamp_column} is not chronologically ordered."
        )


def validate_target(
    df: pd.DataFrame,
    target_column: str = "day_ahead_lmp",
) -> None:
    # The published day-ahead price is the supervised-learning target, so a
    # missing value cannot be silently used for model fitting or scoring.
    missing_count = df[target_column].isna().sum()

    if missing_count:
        raise DataValidationError(
            f"{target_column} contains {missing_count} missing values."
        )


def find_missing_hours(
    df: pd.DataFrame,
    timestamp_column: str = "timestamp_utc",
) -> pd.DatetimeIndex:
    # Build the expected inclusive UTC hourly sequence, then return the hours
    # absent from the observed data. UTC avoids daylight-saving clock changes.
    expected = pd.date_range(
        start=df[timestamp_column].min(),
        end=df[timestamp_column].max(),
        freq="h",
        tz="UTC",
    )

    actual = pd.DatetimeIndex(df[timestamp_column])

    return expected.difference(actual)


def validate_processed_dataset(
    df: pd.DataFrame,
    required_columns: list[str],
) -> None:
    # Run the common integrity checks together before the data feeds feature
    # engineering or model evaluation.
    validate_required_columns(df, required_columns)
    validate_unique_timestamps(df)
    validate_chronological_order(df)
    validate_target(df)

    missing_hours = find_missing_hours(df)

    # Missing hours must be reviewed rather than silently filled because they
    # can indicate an incomplete source extract or an incorrect time conversion.
    if len(missing_hours) > 0:
        raise DataValidationError(
            f"Found {len(missing_hours)} missing hourly timestamps. "
            f"First missing timestamps: {list(missing_hours[:5])}"
        )
