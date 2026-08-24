# Data Dictionary

**Last updated:** August 24, 2026

The committed January processed tables define the canonical preprocessing schema. Field eligibility is a separate question from field presence.

## Core electricity and identity fields

| Column | Type/unit | Meaning | Model role |
|---|---|---|---|
| `timestamp_local` | timezone-aware datetime, America/New_York | Market-local target hour | Identifier; source for calendar features |
| `timestamp_utc` | timezone-aware datetime, UTC | Canonical target-hour key | Identifier/order/split key |
| `market` | string | `PJM` or `NYISO` | Identifier |
| `location_id` | integer/string | Pnode or PTID | Identifier |
| `location` | string | Source pricing-location label | Identifier |
| `pricing_location` | string | Standardized pricing label | Identifier |
| `day_ahead_price_usd_mwh` | numeric, $/MWh | Hourly day-ahead total LMP/LBMP | Target |
| `energy_component_usd_mwh` | numeric, $/MWh | Energy component of target | Audit; prohibited predictor |
| `congestion_component_usd_mwh` | numeric, $/MWh | Congestion component of target | Audit; prohibited predictor |
| `loss_component_usd_mwh` | numeric, $/MWh | Marginal-loss component of target | Audit; prohibited predictor |
| `actual_load_mw` | numeric, MW | Target-hour metered/integrated load | Descriptive/excluded unless safely lagged |
| `load_data_type` | string | `actual_metered` or `actual_integrated` | Audit |
| `is_verified` | Boolean, PJM | PJM source verification flag | Audit |
| `zone` / `load_area` | string, PJM | PJM load geography | Identifier/audit |
| `source_time_zone` | string, NYISO | Source-reported time-zone label | Audit |
| `load_location` | string, NYISO | NYISO load-area label | Identifier |
| `load_location_id` | integer, NYISO | NYISO load PTID | Identifier |

## Weather and weather-audit fields

| Column | Type/unit | Meaning | Model role |
|---|---|---|---|
| `observed_at` | datetime | Selected source-observation time | Audit; not a same-hour predictor |
| `REPORT_TYPE` | string | Selected NOAA report type | Audit |
| `temperature_c` | numeric, °C | Hourly dry-bulb temperature | Descriptive/excluded unless safely lagged |
| `dew_point_c` | numeric, °C | Hourly dew point | Descriptive/excluded unless safely lagged |
| `relative_humidity_pct` | numeric, % | Hourly relative humidity | Descriptive/excluded unless safely lagged |
| `wind_speed_mps` | numeric, m/s | Hourly wind speed | Descriptive/excluded unless safely lagged |
| `weather_quality_flagged` | Boolean | At least one selected source value has a NOAA quality flag | Audit |
| `weather_value_rejected` | Boolean | Selected observation failed a plausible-value rule | Audit |
| `weather_missing` | Boolean | Expected hour has no usable weather value | Audit |
| `weather_imputed` | Boolean | A documented imputation was applied; currently false | Audit |
| `weather_station` | string | NOAA station identifier | Identifier/audit |

## Forecast-vintage and cutoff fields

| Column | Type/unit | Meaning | Model role |
|---|---|---|---|
| `target_timestamp` | timezone-aware datetime | Delivery hour represented by a load forecast | Join/audit identifier |
| `load_forecast_mw` | numeric, MW | Forecast load for the target hour | Candidate when cutoff eligible |
| `forecast_available_at` | timezone-aware datetime | Time the vintage is treated as available | Audit |
| `prediction_cutoff` | timezone-aware datetime | Latest permitted information time | Audit |
| `hours_before_cutoff` | numeric, hours | Lead from availability time to cutoff | Audit |
| `forecast_horizon_hours` | numeric, hours | Lead from forecast issue/proxy time to target hour | Audit |
| `source_archive` | string | Archive containing the forecast file | Provenance |
| `source_file` | string | Daily forecast file inside the archive | Provenance |
| `availability_basis` | string | Evidence used for availability time | Provenance |
| `availability_is_proxy` | Boolean | True when availability is reconstructed rather than authoritative | Limitation/audit |

## Derived calendar fields

| Column | Type/range | Meaning | Model role |
|---|---|---|---|
| `hour_of_day` | integer 0–23 | Local target-hour clock value | Candidate after Task 1 validation |
| `day_of_week` | integer 0–6 | Monday=0 through Sunday=6 | Candidate after Task 1 validation |
| `is_weekend` | Boolean | True for day 5 or 6 | Candidate after Task 1 validation |

## Required role groups for modeling-ready tables

Every column must belong to exactly one documented group:

- **target:** `day_ahead_price_usd_mwh`;
- **candidate predictors:** only cutoff-valid features;
- **forecast audit:** cutoffs, availability, horizons, source, and proxy flags;
- **identifiers:** timestamps, market, locations, stations, and data-type labels; or
- **excluded operational fields:** actual target-hour values, observed weather, target components, and quality/audit columns not intended for fitting.

Task 7 must assert that groups exist, contain no duplicate names, do not overlap, and place no target, identifier, audit, or excluded field in the candidate list.
