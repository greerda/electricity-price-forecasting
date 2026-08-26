# This file prevents file paths, locations, time zones, 
# and market names from being repeated throughout multiple notebooks.

from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

OUTPUT_DIR = PROJECT_ROOT / "outputs"
METRICS_DIR = OUTPUT_DIR / "metrics"
PREDICTIONS_DIR = OUTPUT_DIR / "predictions"
MODELS_DIR = OUTPUT_DIR / "models"

MARKET_TIMEZONE = ZoneInfo("America/New_York")
UTC_TIMEZONE = ZoneInfo("UTC")

MARKETS = {
    "pjm": {
        "market_name": "PJM",
        "location": "PSEG",
        "weather_station": "EWR",
        "weather_file": RAW_DATA_DIR / "noaa" / "WeatherData Jan25 Newark.csv",
        "price_file": RAW_DATA_DIR / "pjm" / "da_hrl_lmps_PJM_PS.csv",
        "load_file": RAW_DATA_DIR / "pjm" / "hrl_load_metered_PJM_PS.csv",
    },
    "nyiso": {
        "market_name": "NYISO",
        "location": "HUD VL",
        "weather_station": "SWF",
        "weather_file": RAW_DATA_DIR / "noaa" / "WeatherData Jan25 Stewart.csv",
        "price_file": (
            RAW_DATA_DIR
            / "nyiso"
            / "nyiso_hudson_valley_jan2025_LMP_DATA.csv"
        ),
        "load_file": (
            RAW_DATA_DIR
            / "nyiso"
            / "nyiso_hudson_valley_jan2025palIntegrated_HV_loaddata.csv"
        ),
    },
}

REQUIRED_PROCESSED_COLUMNS = [
    "timestamp_utc",
    "timestamp_local",
    "market",
    "location",
    "day_ahead_price_usd_mwh",
    "actual_load_mw",
    "temperature_c",
    "dew_point_c",
    "relative_humidity_pct",
    "wind_speed_mps",
]