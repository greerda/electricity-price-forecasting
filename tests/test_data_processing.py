"""Regression tests for the January 2025 preprocessing contract."""

import pandas as pd

from electricity_forecasting.data_processing import (
    clean_noaa_weather,
    clean_pjm_load,
    clean_pjm_prices,
)


def test_pjm_cleaners_use_committed_schema_names() -> None:
    """PJM price and load cleaners must emit the canonical field names."""
    price_raw = pd.DataFrame(
        {
            "datetime_beginning_utc": ["01/01/2025 05:00:00 AM"],
            "datetime_beginning_ept": ["01/01/2025 12:00:00 AM"],
            "pnode_name": ["PSEG"],
            "total_lmp_da": [50.0],
            "system_energy_price_da": [45.0],
            "congestion_price_da": [3.0],
            "marginal_loss_price_da": [2.0],
        }
    )
    load_raw = pd.DataFrame(
        {
            "datetime_beginning_utc": ["01/01/2025 05:00:00 AM"],
            "datetime_beginning_ept": ["01/01/2025 12:00:00 AM"],
            "load_area": ["PS"],
            "mw": [5_000.0],
            "is_verified": [True],
        }
    )

    cleaned_price = clean_pjm_prices(price_raw)
    cleaned_load = clean_pjm_load(load_raw)

    assert "day_ahead_price_usd_mwh" in cleaned_price.columns
    assert "day_ahead_lmp" not in cleaned_price.columns
    assert "actual_load_mw" in cleaned_load.columns
    assert "load_mw" not in cleaned_load.columns


def test_noaa_weather_uses_report_priority_and_preserves_audit_flags() -> None:
    """FM-15 wins an hourly tie and weather audit fields remain available."""
    raw_weather = pd.DataFrame(
        {
            "DATE": [
                "2025-01-01 00:05:00",
                "2025-01-01 00:55:00",
                "2025-01-01 01:55:00",
            ],
            "REPORT_TYPE": ["FM-12", "FM-15", "FM-15"],
            "HourlyDryBulbTemperature": ["10", "12Q", "999"],
            "HourlyDewPointTemperature": ["5", "6", "6"],
            "HourlyRelativeHumidity": ["70", "71", "71"],
            "HourlyWindSpeed": ["3", "4", "4"],
        }
    )

    cleaned = clean_noaa_weather(raw_weather, station_code="TEST")
    by_hour = cleaned.set_index("timestamp_local")
    first_hour = by_hour.loc[pd.Timestamp("2025-01-01 00:00", tz="America/New_York")]
    rejected_hour = by_hour.loc[pd.Timestamp("2025-01-01 01:00", tz="America/New_York")]

    assert len(cleaned) == 744
    assert cleaned["timestamp_utc"].is_unique
    assert cleaned["timestamp_utc"].is_monotonic_increasing
    assert first_hour["REPORT_TYPE"] == "FM-15"
    assert first_hour["temperature_c"] == 12.0
    assert bool(first_hour["weather_quality_flagged"])
    assert bool(rejected_hour["weather_value_rejected"])
    assert bool(rejected_hour["weather_missing"])
    assert not bool(first_hour["weather_imputed"])
