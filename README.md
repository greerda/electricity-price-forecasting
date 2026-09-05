# Electricity Price Forecasting Capstone

Graduate data-science capstone for forecasting and comparing hourly day-ahead electricity prices in:

- PJM PSEG pricing zone, pnode `51301`
- NYISO Hudson Valley Zone G, `HUD VL`, PTID `61758`

The target is hourly day-ahead total LMP/LBMP in `$/MWh`. The unit of analysis is one market-location-hour.

## Research question

> How accurately can statistical and machine-learning models forecast hourly day-ahead electricity prices, and how does predictive performance differ between PJM PSEG and NYISO Hudson Valley Zone G?

PJM and NYISO are modeled separately and compared using a consistent chronological out-of-sample evaluation framework.

## Study design

January 2025 is a 744-hour feasibility and pipeline-development sample. It is used to validate source acquisition, schemas, timestamp handling, data quality, forecast-vintage reconstruction, information cutoffs, feature definitions, leakage controls, reproducibility, and automated validation.

January 2025 is **not** the final evidence base and must not be used for final capstone conclusions.

The planned primary study period is **January 1, 2020 through December 31, 2024**.

## Markets and targets

| Market | Location | Identifier | Target |
|---|---|---|---|
| PJM | PSEG pricing zone | pnode `51301` | Hourly day-ahead total LMP |
| NYISO | Hudson Valley Zone G | `HUD VL`, PTID `61758` | Hourly day-ahead LBMP |

PJM metered load uses load area `PS`. PJM historical load forecasts use `MIDATL`, which is explicitly treated as a regional proxy rather than a PSEG-specific load forecast.

## Forecast origin and leakage policy

The project is designed as an operational day-ahead forecasting experiment. A predictor is eligible only if it can be demonstrated to have been available before the applicable market cutoff.

| Market | Project cutoff |
|---|---|
| PJM | Strictly before 11:00 a.m. EPT on D−1 |
| NYISO | Strictly before 5:00 a.m. EPT on D−1 |

The strict operational predictor set excludes same-hour actual load, same-hour observed weather, target-hour LMP/LBMP components, future prices, identifiers, provenance fields, and forecast audit fields.

Historical price features must also pass explicit availability checks. A chronological lag is not automatically leakage-safe merely because it occurs earlier in the dataset.

## Timekeeping

`timestamp_utc` is the canonical key for joins, chronological ordering, duplicate detection, validation, splitting, and modeling.

Timezone-aware `timestamp_local` is retained for market interpretation, calendar features, cutoff construction, and reporting.

NOAA LCDv2 observations require separate treatment: raw `DATE` values use fixed Local Standard Time rather than daylight-saving-adjusted Eastern Prevailing Time. The full-period weather pipeline must preserve that distinction when converting observations to UTC.

## Current verified status

The January 2025 pre-modeling completion gate is complete.

Verified work includes:

- source inventory and schema validation;
- January electricity and weather cleaning;
- 744-row PJM and NYISO processed electricity tables;
- 4,464 NYISO forecast-vintage/target-hour rows covering 744 target hours;
- latest-eligible NYISO forecast selection;
- calendar feature engineering;
- forecast-origin-aware historical price features;
- comparable PJM and NYISO operational feature paths;
- explicit target, predictor, identifier, audit, and excluded-field roles;
- January exploratory data analysis;
- January modeling-ready checkpoint tables for both markets;
- fresh-kernel notebook execution;
- 21 passing pytest tests; and
- passing Ruff checks.

The January feasibility pipeline is ready to support the transition to full-period implementation, subject to the NYISO P-7 timing update described below.

## January modeling-ready checkpoints

The pre-modeling checkpoint produces:

```text
data/processed/
├── pjm_pseg_january_2025_modeling_ready.csv
└── nyiso_hudson_valley_january_2025_modeling_ready.csv
```

Each table contains 744 unique ordered target hours, a nonmissing day-ahead price target, explicitly classified candidate predictors, identifiers, audit/provenance fields, and excluded operational fields.

Audit and excluded fields remain available for traceability but are not supplied to the default forecasting models.

## Data sources

### PJM

Primary PJM Data Miner 2 sources include:

- day-ahead hourly LMP;
- hourly metered load;
- historical load forecasts; and
- pricing-node metadata.

PJM historical load forecasts use `forecast_area = MIDATL` with the latest eligible historical snapshot strictly before the project cutoff.

### NYISO

Primary NYISO MIS sources include:

- Hudson Valley day-ahead LBMP;
- Hudson Valley integrated load; and
- P-7 ISO Load Forecast / `isolf` data.

For historical P-7 forecast timing, the project uses the public P-7 interface's `Last Updated` timestamp as the best available public-source evidence of forecast availability:

```text
availability_basis = p7_last_updated
availability_is_proxy = True
```

Here `availability_is_proxy=True` means the timing interpretation is based on public-source evidence rather than direct NYISO confirmation of the formal semantic meaning of the field. ZIP-entry modification timestamps may be retained as secondary provenance.

### NOAA

Observed weather uses NOAA Local Climatological Data Version 2 for:

- Newark Liberty International Airport — `USW00014734`
- New York Stewart International Airport — `USW00014714`

Bulk LCDv2 station-year CSV files use SI/metric units. Observed target-hour weather is excluded from the strict operational model unless a leakage-safe lag or archived forecast is established.

## Daylight-saving-time handling

DST behavior is treated as a first-class data-quality issue.

- NYISO Technical Bulletin TB-064 documents the 25-hour fall-back day and the repeated second 01:00 hour as `HB25` in MIS Upload/Download.
- NYISO Technical Bulletin TB-088 documents the 23-hour spring-forward day and omission of `HB02` in MIS Upload/Download.

The documentation rules are understood, but actual 2020–2024 historical files must still be tested before final processing.

## Feature strategy

The strict common operational feature set emphasizes features demonstrably available before forecast origin.

Candidate groups include calendar features, cutoff-safe historical price features, eligible load forecasts, and any later weather or fuel features whose publication timing can be proven.

Market-specific feature sets are allowed where equivalent source data do not exist. The project does not force false feature equivalence between the two ISOs.

## Planned models

The primary comparison is expected to include:

1. persistence and/or historical-average baseline;
2. regularized linear regression;
3. Random Forest regression; and
4. gradient-boosted tree regression.

A simple linear regression may also be retained as an interpretable reference. Neural networks are not required for the primary capstone question.

## Evaluation strategy

Random train/test splitting is prohibited. The project uses chronological evaluation.

A candidate full-period design, subject to final coverage review, is:

- training: 2020–2022;
- validation/tuning: 2023;
- final untouched test: 2024.

Primary metrics are Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE). MAPE is not primary because electricity prices may be zero or negative.

## Repository guide

| Path | Purpose |
|---|---|
| `AGENTS.md` | Stable instructions and guardrails for IDE/Codex agents |
| `docs/current_status.md` | Current verified state, limitations, and exact next action |
| `docs/project_plan.md` | Authoritative project roadmap |
| `docs/methodology_decisions.md` | Methodological decisions and evidence status |
| `docs/data_dictionary.md` | Field definitions, units, timing, and model roles |
| `docs/data_source_register.md` | Source provenance, limitations, and future validation |
| `docs/notebook_pipeline_map.md` | High-level notebook/code workflow |
| `docs/decisions.md` | Dated decision index |
| `docs/learning_log.md` | Student learning and reproduction record |
| `notebooks/` | Inventory, cleaning, EDA, feature engineering, and modeling notebooks |
| `src/electricity_forecasting/` | Reusable Python implementation |
| `tests/` | Automated transformation, leakage, schema, and validation tests |
| `data/raw/` | Immutable source files |
| `data/interim/` | Intermediate and multi-vintage datasets |
| `data/processed/` | Validated derived datasets |
| `outputs/` | Predictions, models, and metrics |
| `reports/` | Capstone paper, figures, tables, and references |

## Reproducibility rules

- Use Python 3.12 and the project virtual environment.
- Run commands from the repository root.
- Install the package in editable mode with development dependencies.
- Keep files under `data/raw/` immutable.
- Use repository-relative paths.
- Use UTC as the canonical modeling key.
- Preserve source filenames and provenance.
- Do not use a predictor unless its pre-cutoff availability is documented and tested.
- Fit imputation, scaling, encoding, and feature selection using training data only.
- Do not randomly shuffle time-series data.
- Restart the notebook kernel and run completed notebooks top-to-bottom before declaring them reproducible.
- Run pytest and Ruff before completing major pipeline milestones.
- Keep private correspondence and restricted reference material out of the public repository.

## Known limitations and remaining work

Before final modeling:

- acquire the full 2020–2024 PJM and NYISO target data;
- acquire and validate the 2020–2024 PJM MIDATL historical load forecasts;
- capture or reconstruct NYISO P-7 `Last Updated` metadata for the full period;
- regenerate January NYISO forecast timing using P-7 metadata;
- verify PSEG `51301`, `PS`, MIDATL, `HUD VL`, and PTID `61758` continuity;
- test PJM and NYISO DST transitions against actual historical files;
- complete NOAA station-history audits;
- decide the final PJM historical price source;
- investigate the September 1, 2021 PJM fast-start-pricing change as a possible structural break; and
- rerun the complete pipeline after full-period acquisition.

## Current next action

Update the NYISO historical forecast-ingestion workflow to use P-7 `Last Updated` metadata as the primary availability field. Retain ZIP-entry timestamps as secondary provenance, rebuild the January NYISO forecast-vintage table, rerun cutoff/leakage validation, and confirm that the January modeling-ready checkpoint remains valid.

After that validation passes, proceed to full 2020–2024 historical acquisition and implementation.

## Project status

**Current phase:** January 2025 pre-modeling feasibility pipeline complete; preparing full 2020–2024 implementation.

See `docs/current_status.md` for the authoritative current task and latest verification evidence.
