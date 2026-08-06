from __future__ import annotations

import numpy as np
import pandas as pd


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create calendar features from the local market timestamp."""
    result = df.copy()

    local_time = result["timestamp_local"]

    result["hour"] = local_time.dt.hour
    result["day_of_week"] = local_time.dt.dayofweek
    result["day_of_month"] = local_time.dt.day
    result["month"] = local_time.dt.month
    result["is_weekend"] = (
        result["day_of_week"].isin([5, 6]).astype(int)
    )

    result["hour_sin"] = np.sin(
        2.0 * np.pi * result["hour"] / 24.0
    )

    result["hour_cos"] = np.cos(
        2.0 * np.pi * result["hour"] / 24.0
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