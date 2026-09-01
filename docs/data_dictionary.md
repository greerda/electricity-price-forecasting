# Data Dictionary

**Last updated:** September 1, 2026

This dictionary documents processed fields, source mappings, units, time conventions, feature roles, and audit fields used by the PJM PSEG and NYISO Hudson Valley pipelines.

## Core fields

| Column | Type/unit | Meaning | Model role |
|---|---|---|---|
| `timestamp_utc` | timezone-aware datetime, UTC | Canonical target-hour key | Join/order/split key |
| `timestamp_local` | timezone-aware datetime, `America/New_York` | Market-local target hour | Calendar and interpretation |
| `market` | string | `PJM` or `NYISO` | Identifier |
| `location_id` | integer/string | PJM pnode or NYISO PTID | Identifier |
| `location` | string | Standardized pricing location | Identifier |
| `day_ahead_price_usd_mwh` | numeric, `$/MWh` | Complete hourly day-ahead LMP/LBMP | Prediction target |
| `actual_load_mw` | numeric, MW | Target-hour metered/integrated load | EDA/audit; excluded operationally unless safely lagged |

## PJM source mapping

| Processed concept | Source field | Notes |
|---|---|---|
| Target UTC hour | `datetime_beginning_utc` | Preferred canonical key |
| Target local hour | `datetime_beginning_ept` | Retain for local interpretation and DST audit |
| Pricing node | `pnode_id` | Expected `51301` |
| Pricing name | `pnode_name` | Expected `PSEG` |
| Day-ahead price | `total_lmp_da` | Complete target; do not add components again |
| Actual load | `mw` | Paired `PS` metered load; same-hour value excluded operationally |
| Historical forecast availability | `evaluated_at_ept` / `evaluated_at_utc` | PJM confirmed generated-and-available timestamp |
| Historical forecast target hour | `forecast_hour_beginning_ept` / `forecast_hour_beginning_utc` | Future delivery hour |
| Historical forecast area | `forecast_area` | Use `MIDATL`; regional proxy for PSEG |
| Historical forecast value | `forecast_load_mw` | Candidate predictor after cutoff filtering |

## NYISO source mapping

| Processed concept | Source field | Notes |
|---|---|---|
| Target local hour | `Time Stamp` | Convert to timezone-aware local and UTC fields |
| Source timezone label | `Time Zone` | Preserve for DST and provenance audit |
| Location name | `Name` | Expected `HUD VL` |
| Location identifier | `PTID` | Expected `61758` |
| Day-ahead price | `LBMP ($/MWHr)` | Complete zonal target |
| Actual integrated load | `Integrated Load` | Same-hour value excluded operationally |
| Forecast target hour | `Time Stamp` or archive target field | Future operating hour represented by forecast |
| Forecast value | Hudson Valley zonal forecast field | Candidate predictor subject to availability proof |
| Forecast availability | currently ZIP entry last-modified | Proxy only unless validated against authoritative NYISO timing |

## NOAA source mapping

| Processed column | NOAA source | Unit/time rule | Model role |
|---|---|---|---|
| `weather_station` | `STATION` | Newark `USW00014734`, Stewart `USW00014714` | Identifier/audit |
| `weather_observed_at_local_standard` | `DATE` | Fixed Local Standard Time; no DST adjustment | Audit |
| `weather_timestamp_utc` | derived | Convert from fixed UTC−05:00 | Canonical weather timestamp |
| `temperature_c` | `HourlyDryBulbTemperature` | °C | Descriptive/safe-lag only |
| `dew_point_c` | `HourlyDewPointTemperature` | °C | Descriptive/safe-lag only |
| `relative_humidity_pct` | `HourlyRelativeHumidity` | % | Descriptive/safe-lag only |
| `wind_speed_mps` | `HourlyWindSpeed` | m/s | Descriptive/safe-lag only |
| `weather_quality_flagged` | derived | Boolean | Audit |
| `weather_value_rejected` | derived | Boolean | Audit |
| `weather_missing` | derived | Boolean | Audit |

## Forecast-vintage and cutoff fields

| Column | Type/unit | Meaning | Model role / limitation |
|---|---|---|---|
| `load_forecast_mw` | numeric, MW | Latest eligible load forecast for target hour | Candidate predictor |
| `forecast_target_at_utc` | timezone-aware datetime | Future operating hour represented by forecast | Join/audit key |
| `forecast_available_at_utc` | timezone-aware datetime | Availability/evaluation time used for cutoff | Audit; may be proxy for NYISO |
| `forecast_available_at` | timezone-aware datetime | Local representation of forecast availability | Audit |
| `prediction_cutoff_utc` | timezone-aware datetime | Market cutoff in UTC | Audit and eligibility validation |
| `prediction_cutoff` | timezone-aware datetime | NYISO 05:00 or PJM 11:00 on D−1 | Audit |
| `hours_before_cutoff` | numeric, hours | `prediction_cutoff - forecast_available_at` | Must be positive under strict rule |
| `forecast_horizon_hours` | numeric, hours | Target hour minus forecast availability | Audit |
| `forecast_area` | string | `MIDATL`, `HUD VL`, or other documented area | Provenance |
| `source_archive` | string | Archive containing forecast | Provenance |
| `source_file` | string | Forecast file/entry | Provenance |
| `availability_basis` | string | Evidence used to establish availability time | For NYISO pilot currently `zip_entry_last_modified` |
| `availability_is_proxy` | Boolean | Whether availability is inferred rather than authoritative | For NYISO currently `True`; replace/validate or exclude feature before strict operational use |

## Derived calendar fields

| Column | Type/range | Meaning | Model role |
|---|---|---|---|
| `hour_of_day` | integer 0–23 | Local target-hour clock value | Approved predictor |
| `day_of_week` | integer 0–6 | Monday=0 through Sunday=6 | Approved predictor |
| `is_weekend` | Boolean | Saturday/Sunday indicator | Approved predictor |

## Cutoff-safe historical price fields

| Column | Type/unit | Meaning | Model role |
|---|---|---|---|
| `previous_day_same_hour_source_timestamp` | timezone-aware datetime | Source target timestamp one local calendar day earlier | Audit join key |
| `previous_day_same_hour_price_value` | numeric, `$/MWh` | Raw source price before eligibility mask | Audit |
| `previous_day_same_hour_price_is_available` | Boolean | Whether source was available by target cutoff | Audit |
| `day_ahead_price_lag_1d` | numeric, `$/MWh` | Prior-day same-hour price retained only when cutoff-safe | Approved candidate predictor |
| `day_ahead_price_lag_1d_rolling_mean_24h` | numeric, `$/MWh` | 24-value rolling mean built only from cutoff-safe lag values | Approved candidate predictor |

## NYISO daylight-saving audit fields

NYISO TB-064 and TB-088 establish that NYISO local market time can contain a repeated 01:00 hour in fall and omit 02:00 in spring. UTC remains the canonical unique key.

Candidate audit fields for the full 2020–2024 implementation are:

| Column | Type | Meaning | Model role |
|---|---|---|---|
| `market_hour_label` | string | Original NYISO hour representation such as `HB01`, `HB25`, or source timestamp label | Audit-only |
| `dst_transition_type` | category/string | `normal`, `spring_forward`, or `fall_back` | Audit-only |
| `is_repeated_local_hour` | Boolean | True for the repeated fall-back local hour where supported by source | Audit-only |
| `utc_offset` | string/timedelta | Effective UTC offset for the local hour | Audit-only |
| `timestamp_utc` | timezone-aware datetime | Canonical unique target timestamp | Join/order/model key |

Do not fabricate these fields if the actual source schema does not support them. The implementation must preserve enough source information to distinguish transition-hour records and prove UTC uniqueness.

## Feature-role classification

Every modeling-ready column must belong to exactly one role:

- **target** — `day_ahead_price_usd_mwh`;
- **candidate predictors** — only features proven available before the applicable cutoff;
- **forecast audit** — cutoffs, availability, horizons, source, proxy flags;
- **identifiers** — timestamps, market, location, station, data-type labels;
- **excluded operational fields** — same-hour actual load, observed weather, target components, future values; or
- **EDA-only fields** — descriptive variables not allowed in the strict operational predictor matrix.

## January 2025 checkpoint status

| Market | Checkpoint | Candidate predictor note |
|---|---|---|
| PJM PSEG | `data/processed/pjm_pseg_january_2025_modeling_ready.csv` | Calendar plus cutoff-safe price-history features; historical MIDATL forecast not yet implemented |
| NYISO Hudson Valley | `data/processed/nyiso_hudson_valley_january_2025_modeling_ready.csv` | Common features plus conditional `load_forecast_mw` using proxy availability timing |

Both checkpoint tables contain 744 unique ordered January target hours. They are feasibility artifacts, not the final 2020–2024 evidence base.

## Missing-value and quality rules

- Do not use blanket `fillna(0)`.
- Do not backward-fill time-series predictors.
- Preserve the distinction among missing, zero, trace, suspect, erroneous, and rejected observations.
- Fit imputation on training data only.
- Preserve raw/source values needed to reproduce rejection decisions where practical.

## Future dictionary actions

- Add exact PJM `load_frcstd_hist` processed columns after first full-period acquisition.
- Replace or validate NYISO proxy availability fields if NYISO identifies an authoritative historical publication timestamp.
- Add finalized DST audit fields after testing actual 2020–2024 transition-day files.
- Version this dictionary whenever processed schemas or feature-role definitions change.
