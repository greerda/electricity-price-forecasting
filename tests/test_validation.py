from pathlib import Path

import pandas as pd
import pytest

from electricity_forecasting.validation import (
    DataValidationError,
    validate_no_prohibited_predictors,
    validate_processed_dataset,
    validate_required_columns,
)


def test_validate_required_columns_rejects_missing_column():
    df = pd.DataFrame(
        {
            "timestamp_utc": pd.date_range(
                "2025-01-01",
                periods=2,
                freq="h",
                tz="UTC",
            ),
        }
    )

    with pytest.raises(
        DataValidationError,
        match="Missing required columns",
    ):
        validate_required_columns(
            df,
            [
                "timestamp_utc",
                "day_ahead_price_usd_mwh",
            ],
        )

def test_validate_processed_dataset_accepts_canonical_target():
    df = pd.DataFrame(
        {
            "timestamp_utc": pd.date_range(
                "2025-01-01",
                periods=3,
                freq="h",
                tz="UTC",
            ),
            "day_ahead_price_usd_mwh": [20.0, 21.0, 22.0],
        }
    )

    validate_processed_dataset(
        df,
        required_columns=[
            "timestamp_utc",
            "day_ahead_price_usd_mwh",
        ],
    )

def test_validate_processed_dataset_rejects_duplicate_timestamps():
    df = pd.DataFrame(
        {
            "timestamp_utc": pd.to_datetime(
                [
                    "2025-01-01 00:00:00+00:00",
                    "2025-01-01 00:00:00+00:00",
                ],
                utc=True,
            ),
            "day_ahead_price_usd_mwh": [20.0, 21.0],
        }
    )

    with pytest.raises(
        DataValidationError,
        match="Found 1 duplicate timestamps",
    ):
        validate_processed_dataset(
            df,
            required_columns=[
                "timestamp_utc",
                "day_ahead_price_usd_mwh",
            ],
        )

def test_validate_processed_dataset_rejects_unordered_timestamps():
    df = pd.DataFrame(
        {
            "timestamp_utc": pd.to_datetime(
                [
                    "2025-01-01 01:00:00+00:00",
                    "2025-01-01 00:00:00+00:00",
                ],
                utc=True,
            ),
            "day_ahead_price_usd_mwh": [21.0, 20.0],
        }
    )

    with pytest.raises(
        DataValidationError,
        match="not chronologically ordered",
    ):
        validate_processed_dataset(
            df,
            required_columns=[
                "timestamp_utc",
                "day_ahead_price_usd_mwh",
            ],
        )

def test_validate_processed_dataset_rejects_missing_hour():
    df = pd.DataFrame(
        {
            "timestamp_utc": pd.to_datetime(
                [
                    "2025-01-01 00:00:00+00:00",
                    "2025-01-01 02:00:00+00:00",
                ],
                utc=True,
            ),
            "day_ahead_price_usd_mwh": [20.0, 22.0],
        }
    )

    with pytest.raises(
        DataValidationError,
        match="Found 1 missing hourly timestamps",
    ):
        validate_processed_dataset(
            df,
            required_columns=[
                "timestamp_utc",
                "day_ahead_price_usd_mwh",
            ],
        )

def test_validate_processed_dataset_rejects_missing_target():
    df = pd.DataFrame(
        {
            "timestamp_utc": pd.date_range(
                "2025-01-01",
                periods=2,
                freq="h",
                tz="UTC",
            ),
            "day_ahead_price_usd_mwh": [20.0, None],
        }
    )

    with pytest.raises(
        DataValidationError,
        match="day_ahead_price_usd_mwh contains 1 missing values",
    ):
        validate_processed_dataset(
            df,
            required_columns=[
                "timestamp_utc",
                "day_ahead_price_usd_mwh",
            ],
        )

@pytest.mark.parametrize(
    ("filename", "market"),
    [
        (
            "nyiso_hudson_valley_january_2025_electricity.csv",
            "NYISO",
        ),
        (
            "pjm_pseg_january_2025_electricity.csv",
            "PJM",
        ),
    ],
)

def test_processed_january_datasets_have_744_valid_target_hours(
    filename: str,
    market: str,
):
    project_root = Path(__file__).resolve().parents[1]

    df = pd.read_csv(
        project_root / "data" / "processed" / filename,
        parse_dates=["timestamp_utc"],
    )

    assert len(df) == 744, f"{market} should have 744 January rows."
    assert df["timestamp_utc"].nunique() == 744

    validate_processed_dataset(
        df,
        required_columns=[
            "timestamp_utc",
            "day_ahead_price_usd_mwh",
        ],
    )

def test_validate_no_prohibited_predictors_rejects_load_and_weather():
    candidate_feature_columns = [
        "hour_of_day",
        "actual_load_mw",
        "temperature_c",
    ]

    prohibited_columns = {
        "actual_load_mw",
        "temperature_c",
        "day_ahead_price_usd_mwh",
    }

    with pytest.raises(
        DataValidationError,
        match="actual_load_mw",
    ):
        validate_no_prohibited_predictors(
            candidate_feature_columns,
            prohibited_columns,
        )

def test_validate_no_prohibited_predictors_accepts_safe_features():
    candidate_feature_columns = [
        "hour_of_day",
        "day_of_week",
        "is_weekend",
        "day_ahead_price_lag_1d",
        "load_forecast_mw",
    ]

    prohibited_columns = {
        "actual_load_mw",
        "temperature_c",
        "day_ahead_price_usd_mwh",
    }

    validate_no_prohibited_predictors(
        candidate_feature_columns,
        prohibited_columns,
    )