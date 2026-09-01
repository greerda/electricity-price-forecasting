# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
# ---

# %% [markdown]
# # January 2025 Data Cleaning
#
# This notebook loads raw PJM, NYISO, and NOAA data, cleans and validates the
# hourly observations, merges electricity and weather data using UTC timestamps,
# and exports standardized processed files.
#
# `timestamp_utc` is the canonical key for joins, ordering, and later modeling.
# `timestamp_local` is retained for local calendar features and reporting.
#

# %%
'''imports MARKETS and PROCESSED_DATA_DIR from the project configuration module.
MARKETS centralizes the location and raw-file paths for PJM and NYISO. 
That avoids scattering hard-coded paths throughout the notebook.'''

import re
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile
from zoneinfo import ZoneInfo

import pandas as pd

from electricity_forecasting.config import (
    MARKETS,
    PROCESSED_DATA_DIR,
)

# %% [markdown]
#

# %% [markdown]
# ## 1. Verify configuration and input files
#

# %%
print("PJM location:", MARKETS["pjm"]["location"])
print("NYISO location:", MARKETS["nyiso"]["location"])

#It loops through both market configurations and checks that each price, load, and weather file exists:

for market_name, market_config in MARKETS.items():
    print(f"\n{market_name.upper()}")

    for key in ["price_file", "load_file", "weather_file"]:
        file_path = market_config[key]
        print(f"{key}: {file_path.exists()} — {file_path}")
        assert file_path.exists(), f"Missing input file: {file_path}"


# %% [markdown]
# ## 2. Load raw data
#

# %%

#loading PJM and NYISO Data location
pjm_config = MARKETS["pjm"]
nyiso_config = MARKETS["nyiso"]

#PJM price, load, and Newark weather
pjm_price_raw = pd.read_csv(pjm_config["price_file"])
pjm_load_raw = pd.read_csv(pjm_config["load_file"])
pjm_weather_raw = pd.read_csv(
    pjm_config["weather_file"],
    low_memory=False,
)

#NYISO price, load, and Stewart weather
nyiso_price_raw = pd.read_csv(nyiso_config["price_file"])
nyiso_load_raw = pd.read_csv(nyiso_config["load_file"])
nyiso_weather_raw = pd.read_csv(
    nyiso_config["weather_file"],
    low_memory=False,
)

raw_datasets = {
    "PJM price": pjm_price_raw,
    "PJM load": pjm_load_raw,
    "PJM weather": pjm_weather_raw,
    "NYISO price": nyiso_price_raw,
    "NYISO load": nyiso_load_raw,
    "NYISO weather": nyiso_weather_raw,
}


'''It prints their shapes and asserts expected sizes for the four electricity files. 
    Each January electricity source should contain 744 rows: 31 days × 24 hours.'''
for name, data in raw_datasets.items():
    print(
        f"{name:15} "
        f"rows={data.shape[0]:6} "
        f"columns={data.shape[1]:3}"
    )

assert pjm_price_raw.shape == (744, 14)
assert pjm_load_raw.shape == (744, 8)
assert nyiso_price_raw.shape == (744, 7)
assert nyiso_load_raw.shape == (744, 6)


# %% [markdown]
# ## 3. Clean PJM electricity data
#

# %%
#Making a local copy of PJM data

pjm_price = pjm_price_raw.copy()

#Parses the local Eastern Prevailing Time timestamp.
pjm_price["timestamp_local"] = (
    pd.to_datetime(
        pjm_price["datetime_beginning_ept"],
        format="%m/%d/%Y %I:%M:%S %p",
    )
    .dt.tz_localize("America/New_York")
)

#Parses the supplied UTC timestamp.
pjm_price["timestamp_utc"] = pd.to_datetime(
    pjm_price["datetime_beginning_utc"],
    format="%m/%d/%Y %I:%M:%S %p",
    utc=True,
)

#Keeps only relevant PJM data set columns.
pjm_price = pjm_price[
    [
        "timestamp_local",
        "timestamp_utc",
        "pnode_id",
        "pnode_name",
        "total_lmp_da",
        "system_energy_price_da",
        "congestion_price_da",
        "marginal_loss_price_da",
    ]
    #Renames fields into common project names
].rename(
    columns={
        "pnode_id": "location_id",
        "pnode_name": "location",
        "total_lmp_da": "day_ahead_price_usd_mwh",
        "system_energy_price_da": "energy_component_usd_mwh",
        "congestion_price_da": "congestion_component_usd_mwh",
        "marginal_loss_price_da": "loss_component_usd_mwh",
    }
)

#Sorts records by UTC time
pjm_price = (
    pjm_price
    .sort_values("timestamp_utc")
    .reset_index(drop=True)
)


# %%
pjm_load = pjm_load_raw.copy()

#Parses the local Eastern Prevailing Time timestamp.
pjm_load["timestamp_local"] = (
    pd.to_datetime(
        pjm_load["datetime_beginning_ept"],
        format="%m/%d/%Y %I:%M:%S %p",
    )
    .dt.tz_localize("America/New_York")
)

#Parses the UTC timestamp for reliable matching.
pjm_load["timestamp_utc"] = pd.to_datetime(
    pjm_load["datetime_beginning_utc"],
    format="%m/%d/%Y %I:%M:%S %p",
    utc=True,
)

#Keeps the zone, load area, megawatt value, and verification flag.
pjm_load = pjm_load[
    [
        "timestamp_local",
        "timestamp_utc",
        "zone",
        "load_area",
        "mw",
        "is_verified",
    ]
  #Renames mw to actual_load_mw so the column name is clear and consistent with NYISO  
].rename(
    columns={
        "mw": "actual_load_mw",
    }
)

#Sorts rows by timestamp_utc and resets the row index.
pjm_load = (
    pjm_load
    .sort_values("timestamp_utc")
    .reset_index(drop=True)
)


# %% [markdown]
# ## 4. Clean NYISO electricity data
#

# %%
#making local vopy of nyiso dataset
nyiso_price = nyiso_price_raw.copy()

#Parses the local Eastern Prevailing Time timestamp.
nyiso_price["timestamp_local"] = (
    pd.to_datetime(
        nyiso_price["Time Stamp"],
        format="%Y-%m-%d %H:%M:%S",
    )
    .dt.tz_localize("America/New_York")
)

#Parses the supplied UTC timestamp.
nyiso_price["timestamp_utc"] = (
    nyiso_price["timestamp_local"]
    .dt.tz_convert("UTC")
)

#Keeps only relevant PJM data set columns.
nyiso_price = nyiso_price[
    [
        "timestamp_local",
        "timestamp_utc",
        "PTID",
        "Name",
        "LBMP ($/MWHr)",
        "Marginal Cost Losses ($/MWHr)",
        "Marginal Cost Congestion ($/MWHr)",
    ]
    #Renames fields into common project names  
].rename(
    columns={
        "PTID": "location_id",
        "Name": "location",
        "LBMP ($/MWHr)": "day_ahead_price_usd_mwh",
        "Marginal Cost Losses ($/MWHr)": "loss_component_usd_mwh",
        "Marginal Cost Congestion ($/MWHr)": "congestion_component_usd_mwh",
    }
)
'''The NYISO price file provides total LBMP, congestion, and loss. 
    The notebook calculates the energy component'''

nyiso_price["energy_component_usd_mwh"] = (
    nyiso_price["day_ahead_price_usd_mwh"]
    - nyiso_price["loss_component_usd_mwh"]
    - nyiso_price["congestion_component_usd_mwh"]
)

#sorting nyiso price  by data
nyiso_price = (
    nyiso_price
    .sort_values("timestamp_utc")
    .reset_index(drop=True)
)


# %% [markdown]
# ## Clean Up of NYISO data

# %%
'''This needs to happen because raw vendor files use their own column names and time formats.
 PJM and NYISO label similar concepts differently, and weather data needs to align to 
 the same hourly moment. Standardizing timestamps and names lets the project safely join price,
 load, and weather records without matching the wrong hours.'''

#Makes a copy of the raw data, leaving the original untouched.
nyiso_load = nyiso_load_raw.copy()

#Parses the Eastern local timestamp and marks it as New York time.
nyiso_load["timestamp_local"] = (
    pd.to_datetime(
        nyiso_load["Time Stamp"],
        format="%Y-%m-%d %H:%M:%S",
    )
    .dt.tz_localize("America/New_York")
)

#Parses the UTC timestamp, which becomes the consistent matching key.
nyiso_load["timestamp_utc"] = (
    nyiso_load["timestamp_local"]
    .dt.tz_convert("UTC")
)

'''Keeps only useful fields: location, total day-ahead price, and its energy,
 congestion, and loss components'''

nyiso_load = nyiso_load[
    [
        "timestamp_local",
        "timestamp_utc",
        "Time Zone",
        "Name",
        "PTID",
        "Integrated Load",
    ]
    #Renames those fields to standard project names and sorts by UTC time.
].rename(
    columns={
        "Time Zone": "source_time_zone",
        "Name": "load_location",
        "PTID": "load_location_id",
        "Integrated Load": "actual_load_mw",
    }
)

# Sorts rows by timestamp_utc and resets the row index.
nyiso_load = (
    nyiso_load
    .sort_values("timestamp_utc")
    .reset_index(drop=True)
)


# %% [markdown]
# ## 5. Validate cleaned electricity tables
# ### 
#

# %%
# Reusable validation helper for cleaned hourly tables.
# Confirms that each January 2025 dataset has all 744 hourly records,
# complete and unique local/UTC timestamps, chronological UTC ordering,
# and no missing values in its primary measure (price or actual load).
# These checks catch missing, duplicate, or misaligned hours before
# price, load, and weather data are merged.

def validate_hourly_table(
    df: pd.DataFrame, # the dataframe to check;
    table_name: str, # a readable name for error messages
    value_column: str, # the key numeric field that must not be missing, such as price or actual load.
) -> None:
    expected_rows = 744

    '''It then asserts that each table:
    Has exactly 744 rows—every hour in January 2025.
    Has no missing local timestamps.
    Has no missing UTC timestamps.
    Has no duplicate local or UTC hours.
    Is sorted chronologically by UTC.
    Has no missing values in its main measure.'''

    assert len(df) == expected_rows, (
        f"{table_name}: expected {expected_rows} rows, "
        f"but found {len(df)}"
    )

    assert df["timestamp_local"].notna().all(), (
        f"{table_name}: missing local timestamps"
    )

    assert df["timestamp_utc"].notna().all(), (
        f"{table_name}: missing UTC timestamps"
    )

    assert df["timestamp_local"].is_unique, (
        f"{table_name}: duplicate local timestamps"
    )

    assert df["timestamp_utc"].is_unique, (
        f"{table_name}: duplicate UTC timestamps"
    )

    assert df["timestamp_utc"].is_monotonic_increasing, (
        f"{table_name}: UTC timestamps are not sorted"
    )

    assert df[value_column].notna().all(), (
        f"{table_name}: missing values in {value_column}"
    )

    print(f"{table_name} passed validation.")

'''After defining the function, the cell runs it four times: PJM price
                                                             PJM load
                                                             NYISO price
                                                             NYISO load
'''


validate_hourly_table(
    pjm_price,
    "PJM price",
    "day_ahead_price_usd_mwh",
)

validate_hourly_table(
    pjm_load,
    "PJM load",
    "actual_load_mw",
)

validate_hourly_table(
    nyiso_price,
    "NYISO price",
    "day_ahead_price_usd_mwh",
)

validate_hourly_table(
    nyiso_load,
    "NYISO load",
    "actual_load_mw",
)

#Finally, it checks that every PJM load observation is marked as verified.
assert pjm_load["is_verified"].all(), (
    "PJM load contains unverified observations"
)


# %% [markdown]
# ## 6. Clean NOAA weather data
#

# %%
'''The purpose is to make NOAA weather consistent,
 auditable, and safe to merge with the hourly price and load tables.
 It is called twice: once for Newark, for the PJM dataset, and once 
 for Stewart Airport, for the NYISO dataset.'''


#Creates the full January hourly timeline: 744 expected hours.
JANUARY_HOURS = pd.date_range(
    start="2025-01-01 00:00:00",
    end="2025-01-31 23:00:00",
    freq="h",
)

#clean_weather, a reusable function used for both Newark and Stewart weather files.
def clean_weather(
    raw_weather: pd.DataFrame,
    station_code: str,
) -> pd.DataFrame:
    weather = raw_weather.copy()

#It converts NOAA’s DATE column into real Python datetime values and stores them in observed_at.
# errors="coerce" means an invalid date does not crash the notebook—it becomes a missing value 
# (NaT), which will be excluded later.

    weather["observed_at"] = pd.to_datetime(
        weather["DATE"],
        errors="coerce",
    )

    #The observation occurred during January 2025.
    weather = weather[
        weather["observed_at"].between(
            "2025-01-01 00:00:00",
            "2025-01-31 23:59:59",
        )
        #The row is one of the selected NOAA hourly report 
        # types: FM-12, FM-15, or FM-16.
        & weather["REPORT_TYPE"].isin(
            ["FM-12", "FM-15", "FM-16"]
        )
    ].copy()

    #Creating dictionary of columns
    source_columns = {
        "HourlyDryBulbTemperature": "temperature_c",
        "HourlyDewPointTemperature": "dew_point_c",
        "HourlyRelativeHumidity": "relative_humidity_pct",
        "HourlyWindSpeed": "wind_speed_mps",
    }

    quality_flag_columns = []

    # For each selected NOAA weather field, extract a clean numeric value
    # and record whether the original value contained letter-based flags.
    for source_column, clean_column in source_columns.items():

        # Convert the raw source column to pandas string type so text methods work safely.   
        raw_values = weather[source_column].astype("string")

        # Create a matching audit-flag column, e.g., temperature_c_quality_flagged.   
        flag_column = f"{clean_column}_quality_flagged"

        # Flag values that contain letters, which may indicate NOAA quality codes
        # or other nonnumeric annotations in the raw source.

        weather[flag_column] = (
            raw_values.notna()
            & raw_values.str.contains(
                r"[A-Za-z]",
                regex=True,
                na=False,
            )
        )
        # Extract the numeric portion of each value and convert it to a number.
        # Invalid or unparseable values become missing rather than raising an error.
            
        weather[clean_column] = pd.to_numeric(
            raw_values.str.extract(
                r"([-+]?\d*\.?\d+)",
                expand=False,
            ),
            errors="coerce",
        )

         # Retain the flag-column names for the later combined quality check.
        quality_flag_columns.append(flag_column)

    # Weather measures that must be checked for plausible physical ranges.
    value_columns = [
        "temperature_c",
        "dew_point_c",
        "relative_humidity_pct",
        "wind_speed_mps",
    ]

# Identify measurements outside the project’s allowed ranges.
    invalid_temperature = ~weather["temperature_c"].between(-50,50,)
    invalid_dew_point = ~weather["dew_point_c"].between(-60,40,)
    invalid_humidity = ~weather["relative_humidity_pct"].between(0,100,)
    invalid_wind_speed = ~weather["wind_speed_mps"].between(0,75,)

   # Reject an entire observation when any required weather measurement is implausible.
    weather["weather_value_rejected"] = (
        invalid_temperature
        | invalid_dew_point
        | invalid_humidity
        | invalid_wind_speed
    )


# Replace rejected weather values with missing values while retaining the rejection flag.
    weather.loc[
        weather["weather_value_rejected"],
        value_columns,
    ] = pd.NA
# Create one overall flag showing whether any source weather value had a quality marker.
    weather["weather_quality_flagged"] = weather[
        quality_flag_columns
    ].any(axis=1)
# Round each observation down to its hourly period for hourly analysis and merging.
    weather["timestamp_local"] = (
        weather["observed_at"].dt.floor("h")
    )
# Prefer one NOAA report type when more than one report exists for the same hour.
# Lower number means higher priority.
    report_priority = {
        "FM-15": 1,
        "FM-12": 2,
        "FM-16": 3,
    }

    weather["report_priority"] = weather[
        "REPORT_TYPE"
    ].map(report_priority)

# Sort observations so the preferred report is first, keep one observation per hour,
# then reindex against every January hour so missing hours remain visible.
    hourly = (
        weather.sort_values(
            [
                "timestamp_local",
                "report_priority",
                "observed_at",
            ]
        )
        .drop_duplicates(
            subset="timestamp_local",
            keep="first",
        )
        .set_index("timestamp_local")
        .reindex(JANUARY_HOURS)
    )
# Mark an hour as missing when any required weather measure is unavailable
    hourly["weather_missing"] = hourly[
        value_columns
    ].isna().any(axis=1)
# No imputation occurs here; this flag supports later tracking if values are filled.
    hourly["weather_imputed"] = False
# Preserve the source station identifier for traceability.  
    hourly["weather_station"] = station_code
    hourly.index.name = "timestamp_local"
# Restore timestamp_local as a normal column after reindexing.
    hourly = hourly.reset_index()

# Make local timestamps timezone-aware and derive UTC timestamps
# for reliable joins with electricity data.
    hourly["timestamp_local"] = (
        hourly["timestamp_local"]
        .dt.tz_localize("America/New_York")
    )

    hourly["timestamp_utc"] = (
        hourly["timestamp_local"]
        .dt.tz_convert("UTC")
    )

# Return only the standardized fields needed downstream.
    output_columns = [
        "timestamp_local",
        "timestamp_utc",
        "observed_at",
        "REPORT_TYPE",
        "temperature_c",
        "dew_point_c",
        "relative_humidity_pct",
        "wind_speed_mps",
        "weather_quality_flagged",
        "weather_value_rejected",
        "weather_missing",
        "weather_imputed",
        "weather_station",
    ]

    return hourly[output_columns]


# %%
#The next cell runs clean_weather for both markets and validates the results.
#newark_weather for PJM, using Newark Airport weather.
newark_weather = clean_weather(
    pjm_weather_raw,
    station_code="USW00014734",
)

#stewart_weather for NYISO Hudson Valley, using Stewart Airport weather.
stewart_weather = clean_weather(
    nyiso_weather_raw,
    station_code="USW00014714",
)

weather_value_columns = [
    "temperature_c",
    "dew_point_c",
    "relative_humidity_pct",
    "wind_speed_mps",
]

'''Summarizes_weather, which prints and validates:
total rows;
duplicate UTC hours;
missing hours or values;
quality-flagged observations;
rejected observations; and
missing values by weather column.'''

def summarize_weather(
    weather: pd.DataFrame,
    station_name: str,
) -> None:
    print(f"\n{station_name}")
    print("Rows:", len(weather))
    print(
        "Duplicate UTC hours:",
        weather["timestamp_utc"].duplicated().sum(),
    )
    print(
        "Missing hours or values:",
        weather["weather_missing"].sum(),
    )
    print(
        "Quality-flagged observations:",
        weather["weather_quality_flagged"]
        .fillna(False)
        .sum(),
    )
    print(
        "Rejected observations:",
        weather["weather_value_rejected"]
        .fillna(False)
        .sum(),
    )
    print("\nMissing values by column:")
    print(weather[weather_value_columns].isna().sum())

    assert len(weather) == 744
    assert weather["timestamp_utc"].notna().all()
    assert weather["timestamp_utc"].is_unique
    assert weather["timestamp_utc"].is_monotonic_increasing


summarize_weather(newark_weather, "Newark")
summarize_weather(stewart_weather, "Stewart")


# %% [markdown]
# ### NOAA weather units
#
# The NOAA Local Climatological Data CSV files use metric/SI units.
#
# The selected variables are interpreted as:
#
# - `HourlyDryBulbTemperature`: degrees Celsius
# - `HourlyDewPointTemperature`: degrees Celsius
# - `HourlyRelativeHumidity`: percent
# - `HourlyWindSpeed`: meters per second
#
# No unit conversion is applied. Values outside documented plausible ranges
# are rejected and recorded through the `weather_value_rejected` indicator.

# %% [markdown]
# ## 7. Merge price, load, and weather data
#

# %%
pjm_electricity = pjm_price.merge(
    pjm_load.drop(
        columns=["timestamp_local"],
        errors="ignore",
    ),
    on="timestamp_utc", # on="timestamp_utc" matches records by the exact same UTC hour.
    how="outer", # keeps unmatched rows temporarily, so the code can detect a missing price or load hour rather than silently discarding it.
    validate="one_to_one", # requires exactly one price row and one load row per hour.
    indicator=True, # adds _merge, showing whether each row came from price only, load only, or both.
)

print(pjm_electricity["_merge"].value_counts())
assert len(pjm_electricity) == 744
assert pjm_electricity["_merge"].eq("both").all()

#After removing the temporary _merge column and sorting by UTC, 
# it adds cleaned Newark weather with a left join:
pjm_electricity = (
    pjm_electricity
    .drop(columns="_merge")
    .sort_values("timestamp_utc")
    .reset_index(drop=True)
)

#A left join preserves every confirmed PJM electricity hour, even if a
# weather value is missing. The weather-cleaning flags retain evidence
# of that missingness.

pjm_processed = pjm_electricity.merge(
    newark_weather.drop(
        columns=["timestamp_local"],
        errors="ignore",
    ),
    on="timestamp_utc",
    how="left",
    validate="one_to_one",
)

pjm_processed["market"] = "PJM"
pjm_processed["pricing_location"] = "PSEG"
pjm_processed["load_data_type"] = "actual_metered"

print("PJM processed shape:", pjm_processed.shape)


# %%
#It merges cleaned NYISO day-ahead price data with cleaned NYISO 
# actual-load data using timestamp_utc, checks that every one of the 744 
# January hours appears in both tables, removes the temporary merge 
# indicator, and sorts chronologically.
#The result is the NYISO equivalent of pjm_processed: one standardized 
# hourly table containing Hudson Valley price, actual load, 
# Stewart weather, timestamps, and metadata.

nyiso_electricity = nyiso_price.merge(
    nyiso_load.drop(
        columns=["timestamp_local"],
        errors="ignore",
    ),
    on="timestamp_utc",
    how="outer",
    validate="one_to_one",
    indicator=True,
)

print(nyiso_electricity["_merge"].value_counts())
assert len(nyiso_electricity) == 744
assert nyiso_electricity["_merge"].eq("both").all()

nyiso_electricity = (
    nyiso_electricity
    .drop(columns="_merge")
    .sort_values("timestamp_utc")
    .reset_index(drop=True)
)

#left-joins Stewart Airport weather onto those same hours:
nyiso_processed = nyiso_electricity.merge(
    stewart_weather.drop(
        columns=["timestamp_local"],
        errors="ignore",
    ),
    on="timestamp_utc",
    how="left",
    validate="one_to_one",
)

#labeled output
nyiso_processed["market"] = "NYISO"
nyiso_processed["pricing_location"] = "HUD VL"
nyiso_processed["load_data_type"] = "actual_integrated"

print("NYISO processed shape:", nyiso_processed.shape)


# %% [markdown]
# ## 8. Final validation
#

# %%
'''The next code cell performs final validation on both completed datasets: pjm_processed and nyiso_processed.
For each dataset, it reports: total row count;
                              duplicate UTC timestamps;
                              missing day-ahead prices;
                              missing actual-load values; 
                              and hours with missing weather.

Both final January datasets must have one complete, unique, 
time-ordered row per hour, with a valid price and actual-load value.
Weather is treated differently: missing weather is counted and retained
through a flag rather than causing the whole notebook to fail. 
That preserves the electricity dataset while making weather gaps 
visible for later decisions.
'''

for name, data in {
    "PJM processed": pjm_processed,
    "NYISO processed": nyiso_processed,
}.items():
    print(f"\n{name}")
    print("Rows:", len(data))
    print(
        "Duplicate UTC timestamps:",
        data["timestamp_utc"].duplicated().sum(),
    )
    print(
        "Missing prices:",
        data["day_ahead_price_usd_mwh"].isna().sum(),
    )
    print(
        "Missing load:",
        data["actual_load_mw"].isna().sum(),
    )
    print(
        "Rows with missing weather:",
        data["weather_missing"].fillna(True).sum(),
    )

    assert len(data) == 744
    assert data["timestamp_utc"].is_unique
    assert data["timestamp_utc"].is_monotonic_increasing
    assert data["day_ahead_price_usd_mwh"].notna().all()
    assert data["actual_load_mw"].notna().all()


# %% [markdown]
# ## 9. Export processed datasets
#

# %%
PROCESSED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

pjm_output_path = (
    PROCESSED_DATA_DIR
    / "pjm_pseg_january_2025_electricity.csv"
)

nyiso_output_path = (
    PROCESSED_DATA_DIR
    / "nyiso_hudson_valley_january_2025_electricity.csv"
)

pjm_processed.to_csv(
    pjm_output_path,
    index=False,
)

nyiso_processed.to_csv(
    nyiso_output_path,
    index=False,
)

print("Saved:", pjm_output_path.resolve())
print("Saved:", nyiso_output_path.resolve())


# %%
assert pjm_output_path.exists()
assert nyiso_output_path.exists()

pjm_exported = pd.read_csv(pjm_output_path)
nyiso_exported = pd.read_csv(nyiso_output_path)

print("PJM exported rows:", len(pjm_exported))
print("NYISO exported rows:", len(nyiso_exported))

assert len(pjm_exported) == 744
assert len(nyiso_exported) == 744


# %% [markdown]
# ## NYISO Hudson Valley load-forecast vintages
#
# This section normalizes the archived NYISO ISO Load Forecast reports for
# Hudson Valley. Each source file contains six operating days. The ZIP entry's
# last-modified timestamp is retained as the forecast-availability proxy.
#
# Multiple rows per target hour are expected because NYISO publishes successive
# forecast vintages. The leakage-safe vintage is selected later during feature
# engineering.

# %% [markdown]
# ### Configure the forecast source files
#
# This step locates the project root and defines the raw and interim data paths. Both the December 2024 and January 2025 NYISO forecast archives are required because forecasts for the beginning of January were issued during December.
#
# The cell also confirms that both monthly ZIP archives exist before processing begins.

# %%
def find_project_root(start: Path | None = None) -> Path:
    """Find the repository directory containing pyproject.toml."""
    if start is None:
        start = Path.cwd()

    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").exists():
            return candidate

    raise FileNotFoundError(
        "Could not find the project root containing pyproject.toml."
    )

PROJECT_ROOT = find_project_root()
NYISO_FORECAST_DIR = (
    PROJECT_ROOT / "data" / "raw" / "nyiso" / "load_forecast"
)
NYISO_FORECAST_INTERIM_FILE = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "nyiso_hudson_valley_load_forecast_vintages.csv"
)

FORECAST_ARCHIVES = [
    NYISO_FORECAST_DIR / "20241201isolf_csv.zip",
    NYISO_FORECAST_DIR / "20250101isolf_csv.zip",
]

missing_archives = [
    archive for archive in FORECAST_ARCHIVES if not archive.exists()
]

if missing_archives:
    raise FileNotFoundError(
        "Missing forecast archives:\n"
        + "\n".join(str(path) for path in missing_archives)
    )



# %% [markdown]
# ### Normalize the archived load forecasts
#
# The cleaning function reads each daily ISO Load Forecast CSV directly from its monthly ZIP archive. It retains the Hudson Valley (`Hud Vl`) forecast and converts each forecasted operating hour to an Eastern Time timestamp.
#
# The ZIP entry's last-modified timestamp is retained as a proxy for when that forecast vintage became available. Source filenames, archive names, forecast horizons, and other provenance fields are preserved so the appropriate leakage-safe forecast can be selected later.
#
# Each daily source file is expected to contain 144 rows, representing hourly forecasts for six operating days.

# %%
# Normalize archived NYISO ISO Load Forecast files into a long, auditable
# forecast-vintage table. Each output row represents one forecast version
# for one future Hudson Valley operating hour. The ZIP entry modification
# time is retained only as a proxy for forecast availability.

NYISO_TIMEZONE = "America/New_York"

# Match daily forecast filenames such as 20250110isolf.csv and capture
# the report's first operating date.
FORECAST_FILENAME_PATTERN = re.compile(
    r"(?P<report_date>\d{8})isolf\.csv$",
    re.IGNORECASE,
)


def clean_nyiso_forecast_archive(zip_path: Path) -> pd.DataFrame:
    """
    Normalize all NYISO ISO Load Forecast CSV files in one monthly ZIP.

    Returns one row for each:
        forecast vintage × target operating hour
    """

    cleaned_files = []

    # Examine each daily forecast CSV stored inside the monthly ZIP archive.
    with ZipFile(zip_path) as archive:
        for zip_info in archive.infolist():
            source_file = Path(zip_info.filename).name
            filename_match = FORECAST_FILENAME_PATTERN.fullmatch(source_file)

            # Ignore folders and files that are not daily ISO load forecasts.
            if zip_info.is_dir() or filename_match is None:
                continue

            with archive.open(zip_info) as raw_file:
                raw = pd.read_csv(raw_file)

            # Confirm the source contains the timestamp and Hudson Valley forecast.
            required_columns = {"Time Stamp", "Hud Vl"}
            missing_columns = required_columns.difference(raw.columns)

            if missing_columns:
                raise ValueError(
                    f"{source_file} is missing columns: "
                    f"{sorted(missing_columns)}"
                )

             # Convert each forecasted delivery hour to timezone-aware Eastern time.
            target_naive = pd.to_datetime(
                raw["Time Stamp"],
                format="%m/%d/%Y %H:%M",
                errors="raise",
            )

            target_timestamp = target_naive.dt.tz_localize(
                NYISO_TIMEZONE,
                ambiguous="infer",
                nonexistent="raise",
            )
            
            # Preserve the ZIP entry timestamp as an availability proxy.
            # This is not treated as verified NYISO publication time.
            source_last_modified_at = pd.Timestamp(
            datetime(
                *zip_info.date_time,
                tzinfo=ZoneInfo(NYISO_TIMEZONE),
            )
        )

            # The filename date is the first operating day in the report.
            report_start_date = pd.to_datetime(
                filename_match.group("report_date"),
                format="%Y%m%d",
            )

             # Create a standardized, traceable table for this forecast file.
            cleaned = pd.DataFrame(
                {
                    "target_timestamp": target_timestamp,
                    "load_forecast_mw": pd.to_numeric(
                        raw["Hud Vl"],
                        errors="raise",
                    ),
                    "report_start_date": report_start_date,
                    "forecast_vintage_date": (
                        source_last_modified_at.date().isoformat()
                    ),
                    "zip_entry_last_modified": source_last_modified_at,
                    "forecast_available_at": source_last_modified_at,
                    "availability_basis": "p7_last_updated_inferred_from_zip_entry",
                    "availability_is_proxy": True,
                    "source_archive": zip_path.name,
                }
            )

            # Measure how far in advance each target hour was forecast.
            cleaned["forecast_horizon_hours"] = (
                cleaned["target_timestamp"]
                - cleaned["forecast_available_at"]
            ).dt.total_seconds() / 3600

            # Each report should forecast six days of hourly values: 6 × 24 = 144.
            if len(cleaned) != 144:
                raise ValueError(
                    f"{source_file}: expected 144 rows, "
                    f"found {len(cleaned)}."
                )

             # Stop if any Hudson Valley forecast value is missing.
            if cleaned["load_forecast_mw"].isna().any():
                raise ValueError(
                    f"{source_file}: missing Hudson Valley forecasts."
                )

            cleaned_files.append(cleaned)
    # Stop if no valid daily forecast files were found in the archive.
    if not cleaned_files:
        raise ValueError(
            f"No NYISO ISO Load Forecast CSV files found in {zip_path}."
        )

    # Combine all daily forecast files from the monthly archive.
    return pd.concat(cleaned_files, ignore_index=True)


# %% [markdown]
# ### Clean and combine the monthly archives
#
# The cleaning function is applied to the December 2024 and January 2025 archives. The resulting daily forecast reports are combined into one long table containing every available forecast vintage and target operating hour.
#
# Multiple records for the same target hour are expected because NYISO updates its six-day forecast each day.

# %%
# Apply the forecast-cleaning function to both monthly NYISO ZIP archives
# and combine the resulting forecast-vintage tables into one dataframe.
# This preserves every available forecast version for each future target hour;
# the leakage-safe version is selected later during feature engineering.

all_forecast_vintages = pd.concat(
    [
        clean_nyiso_forecast_archive(archive)
        for archive in FORECAST_ARCHIVES
    ],
    ignore_index=True,
)

# Display the combined table's row and column count for a quick sanity check.
print(all_forecast_vintages.shape)

# %% [markdown]
# ### Retain January 2025 target hours
#
# The combined forecast table is restricted to operating hours from January 1 through January 31, 2025. All available vintages for those target hours are retained and ordered by target timestamp and forecast availability time.
#
# Duplicate target timestamps are intentional at this stage because each target hour has six forecast vintages.

# %%
study_start = pd.Timestamp(
    "2025-01-01 00:00",
    tz=NYISO_TIMEZONE,
)

study_end = pd.Timestamp(
    "2025-02-01 00:00",
    tz=NYISO_TIMEZONE,
)

january_forecast_vintages = (
    all_forecast_vintages.loc[
        (all_forecast_vintages["target_timestamp"] >= study_start)
        & (all_forecast_vintages["target_timestamp"] < study_end)
    ]
    .sort_values(
        ["target_timestamp", "forecast_available_at"]
    )
    .reset_index(drop=True)
)

january_forecast_vintages.head()

# %% [markdown]
# ### Validate the January forecast vintages
#
# The following checks confirm that the normalized data contain all 744 hourly target periods in January 2025, with six forecast vintages per target hour.
#
# The validation also checks for missing Hudson Valley forecasts and duplicate combinations of target timestamp and source file. The expected result is 4,464 rows: 744 target hours multiplied by six forecast vintages.

# %%
assert january_forecast_vintages["target_timestamp"].nunique() == 744

assert len(january_forecast_vintages) == 744 * 6

assert (
    january_forecast_vintages
    .groupby("target_timestamp")
    .size()
    .eq(6)
    .all()
)

assert january_forecast_vintages["load_forecast_mw"].notna().all()

assert not january_forecast_vintages.duplicated(
    ["target_timestamp", "source_file"]
).any()

print("Rows:", len(january_forecast_vintages))
print(
    "Unique target hours:",
    january_forecast_vintages["target_timestamp"].nunique(),
)
print(
    "Forecast vintages per hour:",
    january_forecast_vintages
    .groupby("target_timestamp")
    .size()
    .value_counts()
    .to_dict(),
)

# %% [markdown]
# ### Inspect forecast revisions for one target hour
#
# The January 10, 2025 noon operating hour is examined as a representative example. Its six records show how the Hudson Valley load forecast changed as the delivery date approached.
#
# No forecast is selected in this step. The example verifies that the successive forecast vintages and their availability timestamps were preserved correctly.

# %%
# Inspect all forecast versions for one representative target hour:
# January 10, 2025 at noon Eastern Time.
#
# This confirms that the pipeline preserved successive forecast revisions,
# their availability timestamps, source files, and forecast horizons.
# No forecast is selected here; leakage-safe selection happens later.

january_forecast_vintages.loc[
    january_forecast_vintages["target_timestamp"]
    == pd.Timestamp("2025-01-10 12:00", tz=NYISO_TIMEZONE),
    [
        "target_timestamp",
        "load_forecast_mw",
        "forecast_available_at",
        "source_file",
        "forecast_horizon_hours",
    ],
]

# %% [markdown]
# ### Export the interim forecast-vintage dataset
#
# The complete January forecast-vintage table is saved as an interim dataset. It intentionally contains multiple forecasts for every target hour.
#
# A later feature-engineering step will calculate the day-ahead prediction cutoff and select the most recent forecast that was available before that cutoff. The interim file is not yet suitable for direct use as a modeling dataset.

# %%
NYISO_FORECAST_INTERIM_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

january_forecast_vintages.to_csv(
    NYISO_FORECAST_INTERIM_FILE,
    index=False,
)

print(f"Saved: {NYISO_FORECAST_INTERIM_FILE}")
