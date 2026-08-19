"""Chronological train, validation, and test splitting utilities."""

from __future__ import annotations

import pandas as pd


def chronological_split_by_fraction(
    df: pd.DataFrame,
    train_fraction: float = 0.70,
    validation_fraction: float = 0.15,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split an ordered dataset without shuffling.

    Intended for pipeline testing. Date-based splits are preferable
    for the final multi-month or multi-year study.
    """
    if train_fraction <= 0 or validation_fraction <= 0:
        raise ValueError("Split fractions must be positive.")

    if train_fraction + validation_fraction >= 1:
        raise ValueError(
            "Train and validation fractions must sum to less than 1."
        )

    # Random splitting would let a model train on future market hours, so each
    # subset is a consecutive block after sorting by the UTC timestamp.
    ordered = df.sort_values("timestamp_utc").reset_index(drop=True)

    train_end = int(len(ordered) * train_fraction)
    validation_end = int(
        len(ordered) * (train_fraction + validation_fraction)
    )

    # The final test block remains untouched during feature and model choices.
    train = ordered.iloc[:train_end].copy()
    validation = ordered.iloc[train_end:validation_end].copy()
    test = ordered.iloc[validation_end:].copy()

    return train, validation, test


def chronological_split_by_date(
    df: pd.DataFrame,
    train_end: str,
    validation_end: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Create explicit date-based train, validation, and test sets."""
    ordered = df.sort_values("timestamp_utc").copy()

    # Interpret explicit cutoffs in UTC to match the standardized join and
    # ordering key used throughout the pipeline.
    train_end_timestamp = pd.Timestamp(train_end, tz="UTC")
    validation_end_timestamp = pd.Timestamp(
        validation_end,
        tz="UTC",
    )

    # Each boundary belongs to the earlier partition, preventing duplicate
    # timestamps while keeping the three time periods contiguous.
    train = ordered.loc[
        ordered["timestamp_utc"] <= train_end_timestamp
    ].copy()

    validation = ordered.loc[
        ordered["timestamp_utc"].gt(train_end_timestamp)
        & ordered["timestamp_utc"].le(validation_end_timestamp)
    ].copy()

    test = ordered.loc[
        ordered["timestamp_utc"].gt(validation_end_timestamp)
    ].copy()

    validate_split_order(train, validation, test)

    return train, validation, test


def validate_split_order(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    test: pd.DataFrame,
) -> None:
    """Confirm strict chronological separation."""
    if train.empty or validation.empty or test.empty:
        raise ValueError("One or more chronological splits are empty.")

    # A strict comparison catches both overlapping timestamps and an invalid
    # partition order before model fitting begins.
    if train["timestamp_utc"].max() >= validation["timestamp_utc"].min():
        raise ValueError("Train and validation periods overlap.")

    if validation["timestamp_utc"].max() >= test["timestamp_utc"].min():
        raise ValueError("Validation and test periods overlap.")
