import pandas as pd

from electricity_forecasting.splitting import (
    chronological_split_by_fraction,
)


def test_chronological_split_has_no_overlap():
    df = pd.DataFrame(
        {
            "timestamp_utc": pd.date_range(
                "2025-01-01",
                periods=100,
                freq="h",
                tz="UTC",
            ),
        }
    )

    train, validation, test = (
        chronological_split_by_fraction(df)
    )

    assert train["timestamp_utc"].max() < (
        validation["timestamp_utc"].min()
    )

    assert validation["timestamp_utc"].max() < (
        test["timestamp_utc"].min()
    )