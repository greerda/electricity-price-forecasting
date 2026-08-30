import pandas as pd

from electricity_forecasting.feature_engineering import (
    add_cutoff_safe_feature,
    add_lag_features,
    add_rolling_features,
    add_rolling_mean_from_safe_feature,
    is_available_by_cutoff,
)


def test_lag_one_uses_previous_row():
    df = pd.DataFrame(
        {
            "timestamp_utc": pd.date_range(
                "2025-01-01",
                periods=4,
                freq="h",
                tz="UTC",
            ),
            "day_ahead_lmp": [10.0, 20.0, 30.0, 40.0],
        }
    )

    result = add_lag_features(
        df,
        column="day_ahead_lmp",
        lags=(1,),
    )

    assert pd.isna(result.loc[0, "day_ahead_lmp_lag_1"])
    assert result.loc[1, "day_ahead_lmp_lag_1"] == 10.0
    assert result.loc[3, "day_ahead_lmp_lag_1"] == 30.0


def test_rolling_mean_excludes_current_target():
    df = pd.DataFrame(
        {
            "timestamp_utc": pd.date_range(
                "2025-01-01",
                periods=4,
                freq="h",
                tz="UTC",
            ),
            "day_ahead_lmp": [10.0, 20.0, 30.0, 1000.0],
        }
    )

    result = add_rolling_features(
        df,
        column="day_ahead_lmp",
        windows=(3,),
    )

    assert result.loc[3, "day_ahead_lmp_rolling_mean_3"] == 20.0

def test_is_available_by_cutoff_rejects_missing_and_post_cutoff_sources():
    source_available_at = pd.Series(
        [
            pd.Timestamp(
                "2025-01-09 05:00",
                tz="America/New_York",
            ),
            pd.Timestamp(
                "2025-01-09 06:00",
                tz="America/New_York",
            ),
            pd.NaT,
        ]
    )

    prediction_cutoff = pd.Series(
        [
            pd.Timestamp(
                "2025-01-09 05:00",
                tz="America/New_York",
            ),
        ]
        * 3
    )

    result = is_available_by_cutoff(
        source_available_at,
        prediction_cutoff,
    )

    assert result.tolist() == [True, False, False]

def test_add_cutoff_safe_feature_masks_unsafe_values():
    df = pd.DataFrame(
        {
            "source_price": [20.0, 30.0, 40.0],
            "source_available_at": [
                pd.Timestamp(
                    "2025-01-09 04:00",
                    tz="America/New_York",
                ),
                pd.Timestamp(
                    "2025-01-09 06:00",
                    tz="America/New_York",
                ),
                pd.NaT,
            ],
            "prediction_cutoff": [
                pd.Timestamp(
                    "2025-01-09 05:00",
                    tz="America/New_York",
                ),
            ]
            * 3,
        }
    )

    result = add_cutoff_safe_feature(
        df,
        source_value_column="source_price",
        source_available_at_column="source_available_at",
        prediction_cutoff_column="prediction_cutoff",
        feature_column="cutoff_safe_price",
    )

    assert result["cutoff_safe_price"].iloc[0] == 20.0
    assert pd.isna(result["cutoff_safe_price"].iloc[1])
    assert pd.isna(result["cutoff_safe_price"].iloc[2])
    assert "cutoff_safe_price" not in df.columns


def test_add_rolling_mean_from_safe_feature_requires_full_window():
    df = pd.DataFrame(
        {
            "cutoff_safe_price": [10.0, 20.0, 30.0, 40.0],
        }
    )

    result = add_rolling_mean_from_safe_feature(
        df,
        safe_feature_column="cutoff_safe_price",
        window=3,
        feature_column="cutoff_safe_price_rolling_mean_3h",
    )

    rolling_feature = "cutoff_safe_price_rolling_mean_3h"

    assert pd.isna(result[rolling_feature].iloc[0])
    assert pd.isna(result[rolling_feature].iloc[1])
    assert result[rolling_feature].iloc[2] == 20.0
    assert result[rolling_feature].iloc[3] == 30.0
    assert rolling_feature not in df.columns