# Data Dictionary

**Last updated:** August 31, 2026

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
| `hour_of_day` | integer 0–23 | Local target-hour clock value | Validated leakage-safe candidate feature |
| `day_of_week` | integer 0–6 | Monday=0 through Sunday=6 | Validated leakage-safe candidate feature |
| `is_weekend` | Boolean | True for day 5 or 6 | Validated leakage-safe candidate feature |

## Derived cutoff-safe price features

The following January 2025 NYISO and PJM fields use a configurable, provisional rule that a day-ahead price schedule becomes available at 00:00 America/New_York on its delivery date. Each market then compares that availability time with its own provisional D−1 prediction cutoff: 05:00 for NYISO and 11:00 for PJM. This is distinct from, and does not remove, the NYISO load-forecast ZIP-entry availability-proxy warning.

| Column | Type/unit | Meaning | Model role |
|---|---|---|---|
| `day_ahead_price_available_at` | timezone-aware datetime, America/New_York | Provisional availability time assigned to each day-ahead price schedule | Audit; not a predictor |
| `target_day_price_available_by_cutoff` | Boolean | Whether the target day’s own price schedule was available by its prediction cutoff | Audit; expected false for all January 2025 target hours |
| `previous_day_same_hour_source_timestamp` | timezone-aware datetime, America/New_York | Target timestamp minus one calendar day, at the same local clock hour | Audit join key |
| `previous_day_same_hour_price_value` | numeric, $/MWh | Raw prior-day same-hour source price before the cutoff-safety mask | Audit; not a predictor |
| `previous_day_same_hour_price_available_at` | timezone-aware datetime, America/New_York | Provisional availability time of the prior-day source price | Audit |
| `previous_day_same_hour_price_is_available` | Boolean | Whether the prior-day source was available no later than the target cutoff | Audit |
| `day_ahead_price_lag_1d` | numeric, $/MWh | Prior-day same-hour price retained only when cutoff-safe | Approved candidate predictor |
| `day_ahead_price_lag_1d_rolling_mean_24h` | numeric, $/MWh | Full 24-value mean of cutoff-safe prior-day price lags | Approved candidate predictor |


## Required role groups for modeling-ready tables

Every column must belong to exactly one documented group:

- **target:** `day_ahead_price_usd_mwh`;
- **candidate predictors:** only cutoff-valid features;
- **forecast audit:** cutoffs, availability, horizons, source, and proxy flags;
- **identifiers:** timestamps, market, locations, stations, and data-type labels; or
- **excluded operational fields:** actual target-hour values, observed weather, target components, and quality/audit columns not intended for fitting.

Task 7 must assert that groups exist, contain no duplicate names, do not overlap, and place no target, identifier, audit, or excluded field in the candidate list.

### January 2025 checkpoint exports

| Market | Checkpoint file | Target | Candidate predictors | Identifiers | Audit fields | Excluded operational fields |
|---|---|---:|---|---:|---:|---:|
| PJM PSEG | `pjm_pseg_january_2025_modeling_ready.csv` | 1 | `hour_of_day`, `day_of_week`, `is_weekend`, `day_ahead_price_lag_1d`, `day_ahead_price_lag_1d_rolling_mean_24h` | 10 | 8 | 14 |
| NYISO Hudson Valley | `nyiso_hudson_valley_january_2025_modeling_ready.csv` | 1 | PJM candidate set plus `load_forecast_mw` | 12 | 14 | 14 |

Both checkpoint tables contain 744 ordered, unique January 2025 target hours and a nonmissing `day_ahead_price_usd_mwh` target. The field roles are validated in Notebook 04 before export. Same-hour `actual_load_mw` and observed weather fields are retained only as excluded operational fields; they are not candidate predictors.

The NYISO `load_forecast_mw` candidate remains conditional: all 744 January rows use `availability_basis="zip_entry_last_modified"` and `availability_is_proxy=True`. It is suitable for feasibility-pipeline development only until authoritative historical publication or issuance timing is verified.

**Last updated:** August 31, 2026

This dictionary documents raw source fields, processed fields, feature roles, units, time conventions, and audit fields used by the PJM PSEG and NYISO Hudson Valley electricity-price forecasting pipelines.

## Naming and role conventions

| Concept | Preferred processed name | Role |
|---|---|---|
| Hourly day-ahead price | `day_ahead_price_usd_mwh` | Prediction target |
| Actual or integrated load | `actual_load_mw` | EDA or safely lagged feature only; excluded at the target hour |
| Selected historical load forecast | `load_forecast_mw` | Candidate predictor subject to market-specific availability rules |
| Canonical target timestamp | `timestamp_utc` | Join, ordering, validation, split, and modeling key |
| Market-local target timestamp | `timestamp_local` | Calendar features, market cutoffs, interpretation, and reporting |

The reusable January preprocessing path uses the canonical names consistently: `day_ahead_price_usd_mwh` and `actual_load_mw`.

## Common processed electricity fields

| Column | Type | Unit/timezone | Description | Role and rule |
|---|---|---|---|---|
| `timestamp_utc` | timezone-aware datetime | UTC | Canonical target delivery-hour timestamp | Required unique key for joins and modeling |
| `timestamp_local` | timezone-aware datetime | `America/New_York` | PJM or NYISO local target delivery hour | Calendar and cutoff construction; retain UTC as the unique key |
| `day_ahead_price_usd_mwh` | numeric | `$/MWh` | Complete hourly day-ahead zonal price | Prediction target |
| `actual_load_mw` | numeric | MW | Actual, metered, or integrated hourly load | EDA/audit; same-hour value excluded from the operational model |
| `market` | string | — | Market identifier, such as `PJM` or `NYISO` | Provenance and grouped reporting |
| `location_name` | string | — | PSEG or HUD VL | Provenance and validation |
| `location_id` | string/integer | — | PJM pnode `51301` or NYISO PTID `61758` | Historical identity validation |

## PJM source-to-processed mapping

| Processed concept | PJM source field | Source type | Unit | Notes |
|---|---|---|---|---|
| Target UTC hour | `datetime_beginning_utc` | datetime | UTC | Preferred source for the canonical key |
| Target local hour | `datetime_beginning_ept` | datetime | Eastern Prevailing Time | Local interpretation; test DST transitions |
| Location identifier | `pnode_id` | integer | — | Expected value `51301` |
| Location name | `pnode_name` | string | — | Expected value `PSEG` |
| Location type | `type` | string | — | Expected value `ZONE` |
| Day-ahead price target | `total_lmp_da` | numeric | `$/MWh` | Complete LMP; do not add component columns to it again |
| Energy component | `system_energy_price_da` | numeric | `$/MWh` | Audit/explanation only unless explicitly modeled |
| Congestion component | `congestion_price_da` | numeric | `$/MWh` | Audit/explanation only unless explicitly modeled |
| Marginal-loss component | `marginal_loss_price_da` | numeric | `$/MWh` | Audit/explanation only unless explicitly modeled |
| Current-row indicator | `row_is_current` | boolean/string | — | Retain for revision validation |
| Version | `version_nbr` | integer | — | Retain for revision validation |
| Actual-load zone | `zone` | string | — | Expected `PS` |
| Actual-load area | `load_area` | string | — | Expected `PS` |
| Actual load | `mw` | numeric | MW | Same-hour value is not an operational predictor |
| Load verification | `is_verified` | boolean/string | — | Retain for historical-quality audit |

## NYISO source-to-processed mapping

| Processed concept | NYISO source field | Source type | Unit | Notes |
|---|---|---|---|---|
| Target local hour | `Time Stamp` | datetime | NYISO local market time | Convert to timezone-aware local and UTC fields |
| Source timezone label | `Time Zone` | string | Eastern market label | Present in the load file; validate across DST transitions |
| Location name | `Name` | string | — | Expected `HUD VL` |
| Location identifier | `PTID` | integer | — | Expected `61758` |
| Day-ahead price target | `LBMP ($/MWHr)` | numeric | `$/MWh` | Complete NYISO zonal day-ahead LBMP |
| Marginal-loss component | `Marginal Cost Losses ($/MWHr)` | numeric | `$/MWh` | Audit/explanation |
| Congestion component | `Marginal Cost Congestion ($/MWHr)` | numeric | `$/MWh` | Audit/explanation |
| Actual integrated load | `Integrated Load` | numeric | MW | Same-hour value is not an operational predictor |
| Raw-source provenance | `source_file` | string | — | Preserve input filename |

## NOAA raw and processed weather mapping

| Processed column | NOAA source column | Type | Unit/timezone | Description and rule |
|---|---|---|---|---|
| `weather_station` | `STATION` | string | — | GHCN station identifier; Newark `USW00014734`, Stewart `USW00014714` |
| `weather_observed_at_local_standard` | `DATE` | naive source datetime | Fixed Local Standard Time, UTC−05:00 | Raw LCDv2 observation time; do not initially localize as `America/New_York` |
| `weather_timestamp_utc` | derived from `DATE` | timezone-aware datetime | UTC | Canonical weather timestamp after fixed-standard-time localization |
| `report_type` | `REPORT_TYPE` | string | — | Hourly priority: `FM-15`, then `FM-12`, then `FM-16`; exclude `SOD` and `SOM` |
| `weather_source_code` | `SOURCE` | string | — | NOAA observation-source code |
| `temperature_c` | `HourlyDryBulbTemperature` | numeric after flag parsing | °C | Already metric; preserve raw text and QC indicators before conversion |
| `dew_point_c` | `HourlyDewPointTemperature` | numeric after flag parsing | °C | Already metric; apply plausibility and dew-point/temperature checks |
| `relative_humidity_pct` | `HourlyRelativeHumidity` | numeric after flag parsing | % | Valid physical range is 0–100% |
| `wind_speed_mps` | `HourlyWindSpeed` | numeric after flag parsing | m/s | Already metric; reject physically implausible parsed values |
| `wind_gust_mps` | `HourlyWindGustSpeed` | numeric after flag parsing | m/s | Optional; preserve missing and flagged states |
| `precipitation_mm` | `HourlyPrecipitation` | numeric/indicator | mm | Blank is missing, `0` is measured no precipitation, and trace must remain distinct |
| `present_weather_type` | `HourlyPresentWeatherType` | string | — | Optional descriptive/audit field |
| `weather_rem_raw` | `REM` | string | — | Original METAR and remarks used to audit questionable parsed observations |
| `weather_qc_flag` | derived | string/category | — | Consolidated quality, suspect, erroneous, and physical-validation status |
| `weather_value_rejected` | derived | boolean | — | True when a source value is converted to missing because it fails validation |

## Selected load-forecast fields

| Column | Type | Unit/timezone | Description | Role and limitation |
|---|---|---|---|---|
| `load_forecast_mw` | numeric | MW | Latest forecast value eligible at the market cutoff | Candidate predictor |
| `forecast_target_at_utc` | timezone-aware datetime | UTC | Future operating hour being forecast | Join and audit key |
| `forecast_available_at_utc` | timezone-aware datetime | UTC | Availability or evaluated time used for cutoff filtering | Audit-only; may be a proxy for NYISO |
| `forecast_available_at` | timezone-aware datetime | `America/New_York` | Local representation of forecast availability | Audit-only |
| `prediction_cutoff_utc` | timezone-aware datetime | UTC | Market-specific cutoff converted to UTC | Audit-only and eligibility validation |
| `prediction_cutoff` | timezone-aware datetime | `America/New_York` | NYISO 5:00 a.m. or PJM 11:00 a.m. on the day before delivery | Audit-only |
| `hours_before_cutoff` | numeric | hours | `prediction_cutoff - forecast_available_at` | Must be strictly positive under the conservative rule |
| `forecast_horizon_hours` | numeric | hours | Target delivery time minus forecast availability time | Audit-only |
| `forecast_area` | string | — | `HUD VL`, `MIDATL`, or other documented forecast area | Provenance; MIDATL is not PSEG-specific |
| `source_archive` | string | — | Archive name containing the selected forecast | Audit-only provenance |
| `source_file` | string | — | Forecast file or entry used for the target hour | Audit-only provenance |
| `availability_basis` | string | — | How availability was determined | Currently `zip_entry_last_modified` for the NYISO pilot |
| `availability_is_proxy` | boolean | — | Whether availability is estimated rather than authoritative | Must be `False` or explicitly accepted before final operational use |
| `forecast_snapshot_frequency` | string/numeric | — | Retained snapshot interval | PJM historical feed preserves six-hour snapshots, not every live revision |

## Interim and processed dataset grains

| Dataset | Grain | Expected uniqueness | Description |
|---|---|---|---|
| `data/processed/pjm_pseg_january_2025_electricity.csv` | One row per PJM target delivery hour | `timestamp_utc` unique | January feasibility electricity table |
| `data/processed/nyiso_hudson_valley_january_2025_electricity.csv` | One row per NYISO target delivery hour | `timestamp_utc` unique | January feasibility electricity table |
| `data/interim/nyiso_hudson_valley_load_forecast_vintages.csv` | One row per forecast-vintage/target-hour pair | Forecast availability plus target hour unique | Contains multiple vintages for each target hour; currently 4,464 rows and 744 target hours |
| Selected NYISO forecast table | One selected row per target hour | Target hour unique | Latest eligible vintage strictly before the 5:00 a.m. cutoff |
| Future selected PJM forecast table | One selected row per target hour | Target hour unique | Latest MIDATL snapshot strictly before the 11:00 a.m. cutoff |

## Feature-role classification

| Role | Included fields or examples | Modeling rule |
|---|---|---|
| Target | `day_ahead_price_usd_mwh` | Never included in predictors for the same target hour |
| Approved predictors | Calendar variables; leakage-safe price lags | Must be available at the forecast origin |
| Conditional predictors | NYISO `load_forecast_mw`; future PJM MIDATL forecast; archived weather forecast | Require verified vintage/availability timing |
| Audit-only fields | Cutoffs, availability timestamps, lead time, proxy indicator, archives, source files, revision/version fields | Preserve for validation; exclude from the model unless explicitly justified |
| Excluded target-period fields | Same-hour actual load; same-hour observed weather; future prices | Do not use in the operational model |
| EDA-only fields | Same-hour actual load and observed weather when clearly labeled | May explain relationships but cannot support deployment claims |

## Missing-value and quality rules

- Do not use blanket `fillna(0)`.
- Do not backward-fill time-series values.
- Preserve the distinction among missing, zero, trace, suspect, erroneous, and physically rejected observations.
- Fit imputation only on training data.
- Retain source values or raw text needed to reproduce rejection decisions.
- Record every imputation method, maximum gap, and feature affected.

## Future dictionary actions

- Verify the exact processed column names by comparing this dictionary with the outputs of `02_data_cleaning.ipynb` and `04_feature_engineering.ipynb`.
- Recheck schema consistency if a future source or export introduces a new field name.
- Add the exact PJM historical forecast columns after the first `load_frcstd_hist` download.
- Add any authoritative NYISO forecast issuance/publication field when identified.
- Add DST-fold or repeated-hour audit fields if Technical Bulletin TB-064 requires them.
- Add feature definitions, lags, and windows when `feature_engineering.py` is finalized.
- Version this dictionary whenever a processed schema changes.
