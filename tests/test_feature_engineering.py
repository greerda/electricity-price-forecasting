# focused tests tell us the new sections work; this checks that the new functions
# and imports did not break cleaning or splitting tests elsewhere in the project.

import pandas as pd
import pytest

from electricity_forecasting.feature_engineering import (
    add_calendar_features,
    add_cutoff_safe_feature,
    add_lag_features,
    add_rolling_features,
    add_rolling_mean_from_safe_feature,
    is_available_by_cutoff,
    select_latest_eligible_forecasts,
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

    assert result.tolist() == [False, False, False]


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


def test_add_calendar_features_uses_local_time_and_valid_ranges():
    df = pd.DataFrame(
        {
            "timestamp_local": pd.to_datetime(
                [
                    "2025-01-03 23:00:00-05:00",
                    "2025-01-04 00:00:00-05:00",
                ],
            ),
        }
    )

    result = add_calendar_features(df)

    assert result["hour_of_day"].tolist() == [23, 0]
    assert result["day_of_week"].tolist() == [4, 5]
    assert result["is_weekend"].tolist() == [0, 1]
    assert result["hour_of_day"].between(0, 23).all()
    assert result["day_of_week"].between(0, 6).all()
    assert result["hour_sin"].between(-1.0, 1.0).all()
    assert result["hour_cos"].between(-1.0, 1.0).all()


def test_select_latest_eligible_forecasts_uses_newest_safe_vintage():
    cutoff = pd.Timestamp(
        "2025-01-09 05:00",
        tz="America/New_York",
    )

    forecast_vintages = pd.DataFrame(
        {
            "target_timestamp": [
                pd.Timestamp(
                    "2025-01-10 12:00",
                    tz="America/New_York",
                ),
                pd.Timestamp(
                    "2025-01-10 12:00",
                    tz="America/New_York",
                ),
                pd.Timestamp(
                    "2025-01-10 12:00",
                    tz="America/New_York",
                ),
                pd.Timestamp(
                    "2025-01-10 13:00",
                    tz="America/New_York",
                ),
            ],
            "forecast_available_at": [
                pd.Timestamp(
                    "2025-01-09 03:00",
                    tz="America/New_York",
                ),
                cutoff,
                pd.Timestamp(
                    "2025-01-09 06:00",
                    tz="America/New_York",
                ),
                pd.Timestamp(
                    "2025-01-09 04:00",
                    tz="America/New_York",
                ),
            ],
            "prediction_cutoff": [cutoff] * 4,
            "load_forecast_mw": [100.0, 110.0, 120.0, 130.0],
        }
    )

    selected = select_latest_eligible_forecasts(
        forecast_vintages,
        target_timestamp_column="target_timestamp",
        available_at_column="forecast_available_at",
        prediction_cutoff_column="prediction_cutoff",
    )

    assert selected["load_forecast_mw"].tolist() == [100.0, 130.0]
    assert selected["forecast_available_at"].tolist() == [
        pd.Timestamp(
            "2025-01-09 03:00",
            tz="America/New_York",
        ),
        pd.Timestamp(
            "2025-01-09 04:00",
            tz="America/New_York",
        ),
    ]


def test_select_latest_eligible_forecasts_rejects_tied_vintages():
    target_timestamp = pd.Timestamp(
        "2025-01-10 12:00",
        tz="America/New_York",
    )
    cutoff = pd.Timestamp(
        "2025-01-09 05:00",
        tz="America/New_York",
    )

    tied_available_at = pd.Timestamp(
        "2025-01-09 04:00",
        tz="America/New_York",
    )

    forecast_vintages = pd.DataFrame(
        {
            "target_timestamp": [target_timestamp, target_timestamp],
            "forecast_available_at": [tied_available_at, tied_available_at],
            "prediction_cutoff": [cutoff, cutoff],
            "load_forecast_mw": [100.0, 110.0],
        }
    )

    with pytest.raises(
        ValueError,
        match="found ties",
    ):
        select_latest_eligible_forecasts(
            forecast_vintages,
            target_timestamp_column="target_timestamp",
            available_at_column="forecast_available_at",
            prediction_cutoff_column="prediction_cutoff",
        )
