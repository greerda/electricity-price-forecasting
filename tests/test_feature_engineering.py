import pandas as pd

from electricity_forecasting.feature_engineering import (
    add_lag_features,
    add_rolling_features,
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