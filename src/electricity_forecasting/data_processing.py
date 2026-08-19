"""Cleaning and UTC-based integration of the January 2025 source data."""

from __future__ import annotations

import pandas as pd

from electricity_forecasting.config import MARKET_TIMEZONE

# These NOAA report types represent routine hourly observations.  Excluding
# other report types avoids mixing in observations with different reporting
# purposes or timing.
VALID_REPORT_TYPES = {
    "FM-12",
    "FM-15",
    "FM-16",
}

def ensure_chronological_order(
    df: pd.DataFrame,
    timestamp_column: str = "timestamp_utc",
) -> pd.DataFrame:
    """Sort data chronologically and reset the index."""
    # Chronological ordering is required before time-series merges, lag features,
    # rolling calculations, and train/validation/test splits.
    result = df.copy()
    result = result.sort_values(timestamp_column)
    return result.reset_index(drop=True)


def add_standard_identifiers(
    df: pd.DataFrame,
    market: str,
    location: str,
) -> pd.DataFrame:
    """Add common market and location identifiers."""
    # Standard identifiers make the PJM and NYISO tables easier to combine,
    # filter, validate, and compare without relying on source-specific names.
    result = df.copy()
    result["market"] = market
    result["location"] = location
    return result


def create_utc_and_local_timestamps(
    timestamp_series: pd.Series,
) -> tuple[pd.Series, pd.Series]:
    """
    Convert naive Eastern local timestamps into timezone-aware
    local and UTC timestamps.
    """
    # NYISO source timestamps are naive local Eastern clock times.  Localizing
    # before converting preserves the market-hour meaning across DST changes.
    timestamp_local = (
        pd.to_datetime(timestamp_series)
        .dt.tz_localize(
            MARKET_TIMEZONE,
            ambiguous="infer",
            nonexistent="shift_forward",
        )
    )

    timestamp_utc = timestamp_local.dt.tz_convert("UTC")

    return timestamp_utc, timestamp_local


def clean_pjm_prices(
    raw_df: pd.DataFrame,
) -> pd.DataFrame:
    """Clean PJM PSEG day-ahead LMP data."""

    required_columns = {
        "datetime_beginning_utc",
        "datetime_beginning_ept",
        "pnode_name",
        "total_lmp_da",
    }

    #required_columns is a set of column names the function needs.
    #raw_df.columns is the DataFrame’s actual column names.
    #.difference(...) returns items in required_columns that are not in raw_df.columns
    missing = required_columns.difference(raw_df.columns)

    if missing:
        raise ValueError(
            f"PJM price data is missing columns: {sorted(missing)}"
        )

    df = raw_df.copy()

    # Keep the project-scope PSEG pricing node only; other PJM nodes are not
    # comparable observations for this market-location-hour study.
    df = df.loc[
        df["pnode_name"].eq("PSEG"),
        [
            "datetime_beginning_utc",
            "datetime_beginning_ept",
            "pnode_name",
            "total_lmp_da",
            "system_energy_price_da",
            "congestion_price_da",
            "marginal_loss_price_da",
        ],
    ]

    df["timestamp_utc"] = pd.to_datetime(
        df["datetime_beginning_utc"],
        format="%m/%d/%Y %I:%M:%S %p",
        utc=True,
    )

    # Retain both source time representations so joins use an unambiguous UTC
    # key while local hour remains available for later calendar features.
    df["timestamp_local"] = (
        pd.to_datetime(
            df["datetime_beginning_ept"],
            format="%m/%d/%Y %I:%M:%S %p",
        )
        .dt.tz_localize(
            MARKET_TIMEZONE,
            ambiguous="infer",
            nonexistent="shift_forward",
        )
    )

    # Component prices are retained for reconciliation and auditing, but they
    # must not become contemporaneous predictors of total day-ahead LMP.
    df = df.rename(
        columns={
            "pnode_name": "location",
            "total_lmp_da": "day_ahead_lmp",
        }
    )

    df["market"] = "PJM"
    df["day_ahead_lmp"] = pd.to_numeric(
        df["day_ahead_lmp"],
        errors="coerce",
    )

    return ensure_chronological_order(df)


def clean_pjm_load(
    raw_df: pd.DataFrame,
) -> pd.DataFrame:
    """Clean PJM PSEG metered load data."""

    required_columns = {
        "datetime_beginning_utc",
        "datetime_beginning_ept",
        "load_area",
        "mw",
    }

    missing = required_columns.difference(raw_df.columns)

    if missing:
        raise ValueError(
            f"PJM load data is missing columns: {sorted(missing)}"
        )

    df = raw_df.copy()

    # PS is PJM's load area corresponding to the selected PSEG study area.
    df = df.loc[
        df["load_area"].eq("PS"),
        [
            "datetime_beginning_utc",
            "datetime_beginning_ept",
            "load_area",
            "mw",
            "is_verified",
        ],
    ]

    df["timestamp_utc"] = pd.to_datetime(
        df["datetime_beginning_utc"],
        format="%m/%d/%Y %I:%M:%S %p",
        utc=True,
    )

    df["timestamp_local"] = (
        pd.to_datetime(
            df["datetime_beginning_ept"],
            format="%m/%d/%Y %I:%M:%S %p",
        )
        .dt.tz_localize(
            MARKET_TIMEZONE,
            ambiguous="infer",
            nonexistent="shift_forward",
        )
    )

    df = df.rename(
        columns={
            "load_area": "location",
            "mw": "load_mw",
        }
    )

    df["market"] = "PJM"
    df["load_mw"] = pd.to_numeric(
        df["load_mw"],
        errors="coerce",
    )

    return ensure_chronological_order(df)


def clean_nyiso_prices(
    raw_df: pd.DataFrame,
) -> pd.DataFrame:
    """Clean NYISO Hudson Valley day-ahead LBMP data."""

    required_columns = {
        "Time Stamp",
        "Name",
        "LBMP ($/MWHr)",
    }

    missing = required_columns.difference(raw_df.columns)

    if missing:
        raise ValueError(
            f"NYISO price data is missing columns: {sorted(missing)}"
        )

    df = raw_df.copy()

    # HUD VL is NYISO's Hudson Valley Zone G identifier in these extracts.
    df = df.loc[
        df["Name"].eq("HUD VL"),
        [
            "Time Stamp",
            "Name",
            "LBMP ($/MWHr)",
            "Marginal Cost Losses ($/MWHr)",
            "Marginal Cost Congestion ($/MWHr)",
        ],
    ]

    timestamp_utc, timestamp_local = (
        create_utc_and_local_timestamps(
            df["Time Stamp"]
        )
    )

    df["timestamp_utc"] = timestamp_utc
    df["timestamp_local"] = timestamp_local

    # Keep LBMP components for auditability, not as same-hour predictors.
    df = df.rename(
        columns={
            "Name": "location",
            "LBMP ($/MWHr)": "day_ahead_lmp",
            "Marginal Cost Losses ($/MWHr)": "loss_price",
            "Marginal Cost Congestion ($/MWHr)": "congestion_price",
        }
    )

    df["market"] = "NYISO"
    df["day_ahead_lmp"] = pd.to_numeric(
        df["day_ahead_lmp"],
        errors="coerce",
    )

    return ensure_chronological_order(df)


def clean_nyiso_load(
    raw_df: pd.DataFrame,
) -> pd.DataFrame:
    """Clean NYISO Hudson Valley integrated load data."""

    required_columns = {
        "Time Stamp",
        "Name",
        "Integrated Load",
    }

    missing = required_columns.difference(raw_df.columns)

    if missing:
        raise ValueError(
            f"NYISO load data is missing columns: {sorted(missing)}"
        )

    df = raw_df.copy()

    # Restrict the load extract to the same Hudson Valley zone as the price.
    df = df.loc[
        df["Name"].eq("HUD VL"),
        [
            "Time Stamp",
            "Name",
            "Integrated Load",
        ],
    ]

    timestamp_utc, timestamp_local = (
        create_utc_and_local_timestamps(
            df["Time Stamp"]
        )
    )

    df["timestamp_utc"] = timestamp_utc
    df["timestamp_local"] = timestamp_local

    df = df.rename(
        columns={
            "Name": "location",
            "Integrated Load": "load_mw",
        }
    )

    df["market"] = "NYISO"
    df["load_mw"] = pd.to_numeric(
        df["load_mw"],
        errors="coerce",
    )

    return ensure_chronological_order(df)

def fahrenheit_to_celsius(values: pd.Series) -> pd.Series:
    """Convert temperatures from degrees Fahrenheit to degrees Celsius."""
    return (values - 32.0) * (5.0 / 9.0)


def miles_per_hour_to_meters_per_second(
    values: pd.Series,
) -> pd.Series:
    """Convert wind speed from miles per hour to meters per second."""
    return values * 0.44704


def clean_noaa_weather(
    raw_df: pd.DataFrame,
    station_code: str,
) -> pd.DataFrame:
    """Convert NOAA observations into one record per local hour."""
    required_columns = {
        "DATE",
        "REPORT_TYPE",
        "HourlyDryBulbTemperature",
        "HourlyDewPointTemperature",
        "HourlyRelativeHumidity",
        "HourlyWindSpeed",
    }

    missing = required_columns.difference(raw_df.columns)

    if missing:
        raise ValueError(
            f"NOAA weather data is missing columns: {sorted(missing)}"
        )

    df = raw_df.copy()

    # Filter before aggregation so each hourly value is based on comparable
    # routine observations only.
    df = df.loc[df["REPORT_TYPE"].isin(VALID_REPORT_TYPES)].copy()

    df["observation_local"] = pd.to_datetime(
        df["DATE"],
        errors="coerce",
    )

    numeric_columns = [
        "HourlyDryBulbTemperature",
        "HourlyDewPointTemperature",
        "HourlyRelativeHumidity",
        "HourlyWindSpeed",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # NOAA observations may occur within the hour; floor them before taking
    # one mean per local hour.
    df["timestamp_local"] = df["observation_local"].dt.floor("h")

    hourly = (
        df.groupby("timestamp_local", as_index=False)
        .agg(
            temperature_f=(
                "HourlyDryBulbTemperature",
                "mean",
            ),
            dew_point_f=(
                "HourlyDewPointTemperature",
                "mean",
            ),
            relative_humidity_pct=(
                "HourlyRelativeHumidity",
                "mean",
            ),
            wind_speed_mph=(
                "HourlyWindSpeed",
                "mean",
            ),
        )
    )

    # Convert the aggregated local hour to an aware timestamp before creating
    # the UTC join key, including daylight-saving-time transitions.
    hourly["timestamp_local"] = (
        hourly["timestamp_local"]
        .dt.tz_localize(
            MARKET_TIMEZONE,
            ambiguous="infer",
            nonexistent="shift_forward",
        )
    )

    hourly["timestamp_utc"] = (
        hourly["timestamp_local"].dt.tz_convert("UTC")
    )

    hourly["temperature_c"] = fahrenheit_to_celsius(
        hourly["temperature_f"]
    )

    hourly["dew_point_c"] = fahrenheit_to_celsius(
        hourly["dew_point_f"]
    )

    hourly["wind_speed_mps"] = (
        miles_per_hour_to_meters_per_second(
            hourly["wind_speed_mph"]
        )
    )

    hourly["weather_station"] = station_code

    keep_columns = [
        "timestamp_utc",
        "timestamp_local",
        "weather_station",
        "temperature_c",
        "dew_point_c",
        "relative_humidity_pct",
        "wind_speed_mps",
    ]

    return ensure_chronological_order(hourly[keep_columns])

def merge_market_data(
    prices: pd.DataFrame,
    load: pd.DataFrame,
    weather: pd.DataFrame,
) -> pd.DataFrame:
    """Merge price, load, and hourly weather using UTC timestamps."""

    load_columns = load[
        [
            "timestamp_utc",
            "load_mw",
        ]
    ]

    weather_columns = weather[
        [
            "timestamp_utc",
            "weather_station",
            "temperature_c",
            "dew_point_c",
            "relative_humidity_pct",
            "wind_speed_mps",
        ]
    ]

    # UTC prevents accidental joins between matching clock times that refer to
    # different instants.  one_to_one makes duplicate source hours fail fast.
    result = prices.merge(
        load_columns,
        on="timestamp_utc",
        how="left",
        validate="one_to_one",
    )

    result = result.merge(
        weather_columns,
        on="timestamp_utc",
        how="left",
        validate="one_to_one",
    )

    return ensure_chronological_order(result)
