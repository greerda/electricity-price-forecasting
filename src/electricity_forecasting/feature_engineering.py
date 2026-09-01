"""Leakage-safe feature creation for hourly electricity-price forecasting."""

from __future__ import annotations

import numpy as np
import pandas as pd


def is_available_by_cutoff(
    source_available_at: pd.Series,
    prediction_cutoff: pd.Series,
) -> pd.Series:
    """Return whether each source was available by its target cutoff."""
    return (
        source_available_at.notna()
        & source_available_at.lt(prediction_cutoff).fillna(False)
    )

def add_rolling_mean_from_safe_feature(
    df: pd.DataFrame,
    *,
    safe_feature_column: str,
    window: int,
    feature_column: str,
) -> pd.DataFrame:
    """Add a full-window mean from a cutoff-safe, target-excluded feature."""
    if window < 1:
        raise ValueError("window must be at least 1")

    result = df.copy()

    result[feature_column] = result[
        safe_feature_column
    ].rolling(
        window=window,
        min_periods=window,
    ).mean()

    return result


def add_cutoff_safe_feature(
    df: pd.DataFrame,
    *,
    source_value_column: str,
    source_available_at_column: str,
    prediction_cutoff_column: str,
    feature_column: str,
) -> pd.DataFrame:
    """Add a feature only when its source was available by the cutoff."""
    result = df.copy()

    source_is_available = is_available_by_cutoff(
        result[source_available_at_column],
        result[prediction_cutoff_column],
    )

    result[feature_column] = result[source_value_column].where(
        source_is_available
    )

    return result

def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create calendar features from the local market timestamp."""
    result = df.copy()

    # Calendar values use market-local time because demand and price patterns
    # follow the local business day, not the UTC clock.
    local_time = result["timestamp_local"]

    result["hour_of_day"] = local_time.dt.hour
    result["day_of_week"] = local_time.dt.dayofweek
    result["day_of_month"] = local_time.dt.day
    result["month"] = local_time.dt.month
    result["is_weekend"] = (
    result["day_of_week"].isin([5, 6]).astype(int)
    )

    # Sine and cosine preserve the circular relationship: hour 23 is close to
    # hour 0, even though their integer values are far apart.
    result["hour_sin"] = np.sin(
        2.0 * np.pi * result["hour_of_day"] / 24.0
    )

    result["hour_cos"] = np.cos(
        2.0 * np.pi * result["hour_of_day"] / 24.0
    )

    result["day_of_week_sin"] = np.sin(
        2.0 * np.pi * result["day_of_week"] / 7.0
    )

    result["day_of_week_cos"] = np.cos(
        2.0 * np.pi * result["day_of_week"] / 7.0
    )

    return result


def add_lag_features(
    df: pd.DataFrame,
    column: str,
    lags: tuple[int, ...],
) -> pd.DataFrame:
    """Create lagged values using past observations only."""
    # Sorting makes each positional shift refer to an earlier market-hour.
    result = df.sort_values("timestamp_utc").copy()

    for lag in lags:
        result[f"{column}_lag_{lag}"] = result[column].shift(lag)

    return result


def add_rolling_features(
    df: pd.DataFrame,
    column: str,
    windows: tuple[int, ...],
) -> pd.DataFrame:
    """
    Create rolling statistics that exclude the current observation.
    """
    result = df.sort_values("timestamp_utc").copy()
    # Shift first so the current target is excluded from its own rolling
    # statistic; otherwise the feature would leak target information.
    past_values = result[column].shift(1)

    for window in windows:
        result[f"{column}_rolling_mean_{window}"] = (
            past_values.rolling(
                window=window,
                min_periods=window,
            )
            .mean()
        )

        result[f"{column}_rolling_std_{window}"] = (
            past_values.rolling(
                window=window,
                min_periods=window,
            )
            .std()
        )

    return result


def add_load_ramp_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate changes using historical metered load only.
    """
    result = df.sort_values("timestamp_utc").copy()

    # Both terms end before the target hour, so actual metered load is used
    # only as historical information rather than a contemporaneous predictor.
    result["load_change_lagged_1h"] = (
        result["load_mw"].shift(1)
        - result["load_mw"].shift(2)
    )

    result["load_change_lagged_24h"] = (
        result["load_mw"].shift(1)
        - result["load_mw"].shift(25)
    )

    return result


def build_initial_features(df: pd.DataFrame) -> pd.DataFrame:
    """Build the initial leakage-safe feature dataset."""
    # This initial set uses features known from the calendar or prior hours.
    # Forecast-vintage load or weather variables require separate availability
    # validation before they can be included in a day-ahead model.
    result = add_calendar_features(df)

    result = add_lag_features(
        result,
        column="day_ahead_lmp",
        lags=(1, 24, 48, 168),
    )

    result = add_rolling_features(
        result,
        column="day_ahead_lmp",
        windows=(24, 168),
    )

    result = add_lag_features(
        result,
        column="load_mw",
        lags=(1, 24, 168),
    )

    result = add_load_ramp_features(result)

    return result

def select_latest_eligible_forecasts(
    forecast_vintages: pd.DataFrame,
    *,
    target_timestamp_column: str,
    available_at_column: str,
    prediction_cutoff_column: str,
) -> pd.DataFrame:
    """Select one latest cutoff-eligible forecast per target hour."""
    eligible_vintages = forecast_vintages.loc[
        is_available_by_cutoff(
            forecast_vintages[available_at_column],
            forecast_vintages[prediction_cutoff_column],
        )
    ].copy()

    latest_available_at = eligible_vintages.groupby(
        target_timestamp_column
    )[available_at_column].transform("max")

    latest_rows = eligible_vintages.loc[
        eligible_vintages[available_at_column].eq(latest_available_at)
    ].copy()

    latest_row_counts = latest_rows.groupby(
        target_timestamp_column
    ).size()

    if not latest_row_counts.eq(1).all():
        tied_targets = latest_row_counts[
            latest_row_counts.ne(1)
        ].index.tolist()
        raise ValueError(
            "Expected exactly one latest eligible forecast per target "
            f"hour; found ties for {tied_targets}."
        )

    return latest_rows.sort_values(
        target_timestamp_column
    ).reset_index(drop=True)
