# IDE Agent Handoff — Electricity Price Forecasting Capstone

**Last updated:** August 21, 2026  
**Current phase:** January 2025 leakage-safe feature engineering  
**Current notebook:** `notebooks/04_feature_engineering.ipynb`

## Project decision

Research question:

> How accurately can statistical and machine-learning models forecast hourly day-ahead electricity prices, and how does predictive performance differ between PJM PSEG and NYISO Hudson Valley Zone G?

Current scope:

- PJM target location: PSEG zone, pricing node `51301`.
- PJM target field: `total_lmp_da`, interpreted as the complete day-ahead LMP in `$/MWh`.
- NYISO target location: Hudson Valley Zone G, `HUD VL`, PTID `61758`.
- NYISO target field: zonal day-ahead LBMP in `$/MWh`.
- Unit of analysis: one target delivery hour per market.
- Planned primary study period: January 1, 2020 through December 31, 2024.
- January 2025 remains a feasibility and pipeline-development sample.
- `timestamp_utc` is the canonical field for joins, ordering, validation, splitting, and modeling.
- Timezone-aware local timestamps are retained for market interpretation, calendar features, and reporting.
- Raw files under `data/raw/` must remain unchanged.

The project is no longer waiting for PJM, NYISO, or NOAA responses. Their responses have been received and summarized. Remaining work concerns implementation, full-period validation, and several explicitly documented limitations.

## Active development environment

- The earlier Python 3.11 environment was superseded.
- The active project environment uses Python 3.12.
- The active notebook kernel is `Python 3.12 (electricity-forecasting)`.
- The project is installed in editable mode.
- Required development packages include pandas, NumPy, pytest, ipykernel, Ruff, and `tzdata`.

## Completed work

- Reorganized `notebooks/02_data_cleaning.ipynb`.
- Added reusable cleaning functions in `src/electricity_forecasting/data_processing.py`.
- Standardized PJM and NYISO market timestamps using timezone-aware local timestamps and UTC.
- Added NOAA weather cleaning and UTC conversion.
- Added PJM, NYISO, load, price, and weather merge logic.
- Corrected indentation and nested-function errors in `data_processing.py`.
- Confirmed that `data_processing.py` compiles successfully with `py_compile`.
- Created the January 2025 PJM and NYISO processed electricity tables with 744 unique target hours each.
- Preserved raw source files and source-provenance fields.
- Added the most current NOAA, NYISO, and PJM correspondence and technical documentation to the project sources.
- Completed Steps 1–6 of the January 2025 NYISO load-forecast workflow in `notebooks/04_feature_engineering.ipynb`.
- Built `data/interim/nyiso_hudson_valley_load_forecast_vintages.csv` with 4,464 forecast-vintage/target-hour rows covering 744 unique target hours.
- Applied a 5:00 a.m. `America/New_York` information cutoff on the calendar day before NYISO delivery.
- Selected exactly one latest eligible NYISO load-forecast vintage for each of the 744 target hours.
- Excluded post-cutoff forecast vintages.
- Merged the selected forecasts one-to-one with the 744-row NYISO electricity table.
- Preserved forecast-cutoff, availability, lead-time, archive, and source-file audit fields.
- Verified the current project test suite: 3 tests passed.
- Verified Ruff checks for `src` and `tests`.

## Confirmed external findings

### PJM

- PJM confirmed that pricing node `51301` is the appropriate PSEG zone-level pricing node to pair with the `PS` metered-load area.
- The public historical load-forecast source is `load_frcstd_hist`.
- `MIDATL` is the most geographically specific historical forecast area available for modeling PSEG; PSEG-only historical forecast detail is not available.
- `evaluated_at_ept` represents when a PJM forecast was generated and made available.
- The historical feed preserves six-hour snapshots starting one day before the effective date; it does not preserve every twice-hourly live forecast revision.
- PJM uses system conditions, including forecasts, as of 11:00 a.m. EPT when calculating Day-Ahead Market results.
- The project will conservatively require PJM predictors to have availability timestamps strictly before 11:00 a.m. EPT on the day before delivery.
- PJM reported no 2020–2024 changes that would affect the forecasts. A year-by-year continuity audit is still required before bulk modeling.

### NYISO

- NYISO confirmed that `HUD VL`, PTID `61758`, is the appropriate identifier for both Hudson Valley zonal day-ahead LBMP and actual zonal load.
- NYISO directed the project to Markets → Load Data → NY Load Forecast → Custom Reports for historical load forecasts.
- The NYISO Energy Marketplace timeline shows that the Day-Ahead Market closes at 5:00 a.m. EPT on the day before dispatch.
- The project therefore uses a strict pre-5:00 a.m. eligibility rule for the NYISO operational experiment.
- The same timeline places the NYISO Load Forecast posting after the 5:00 a.m. market close. Therefore, an operational model must use an earlier forecast version that was already available before 5:00 a.m.; it cannot use the later same-day posting.
- NYISO directed daylight-saving-time questions to Technical Bulletin TB-064. The full-period implementation must be validated against that bulletin.

### NOAA

- Newark Liberty International Airport is station `USW00014734`.
- New York Stewart International Airport is station `USW00014714`.
- NOAA explained that station representativeness is subjective. The selected stations remain defensible point observations, but they are not certified as perfect representations of the full pricing zones.
- LCDv2 is an appropriate NOAA source and uses the same underlying observations as GHCN-Hourly with additional quality-controlled parameters.
- Bulk LCDv2 station-year files use SI units. No Fahrenheit-to-Celsius or mph-to-m/s conversion is applied.
- Raw LCDv2 `DATE` values use fixed Local Standard Time without daylight-saving adjustment. They must not initially be localized as `America/New_York`.
- Blank precipitation values mean missing or unreported, not zero.
- NOAA quality indicators and raw `REM` observations must be preserved for audit and validation.
- NOAA identified SRRS and NOAAPort as archived text-product interfaces and identified FPUS5 and FXUS6 as relevant products. Their suitability for structured hourly forecast features remains to be investigated.

## Predictor status

| Predictor | Current status | Rule |
|---|---|---|
| Calendar variables | Approved | Known before both market cutoffs. |
| Historical price lags | Approved in principle | Each lag and rolling window must be available at the forecast origin. |
| NYISO `load_forecast_mw` | Conditionally approved for the January pilot | The selected vintage must be strictly before 5:00 a.m.; full-period use requires validation of the availability timestamp. |
| PJM MIDATL historical load forecast | Approved candidate; not yet implemented | Use `load_frcstd_hist`; select the latest snapshot strictly before 11:00 a.m. EPT. |
| Same-hour actual load | Excluded from the operational model | May be used for EDA or only with a demonstrated safe lag. |
| Same-hour observed NOAA weather | Excluded from the operational model | May be used for EDA, an explicitly labeled upper-bound model, or with a demonstrated safe lag. |
| Archived weather forecast | Under investigation | Must preserve issuance time, valid time, and the exact forecast vintage. |
| Natural-gas price | Optional future feature | Publication timing must be documented before use. |

## Current issue

The January 2025 NYISO load-forecast workflow uses each archived ZIP entry's last-modified timestamp as a proxy for the forecast's original availability time.

The workflow correctly records:

- `availability_basis="zip_entry_last_modified"`
- `availability_is_proxy=True`

This proxy is acceptable for developing and testing the January pipeline, but it is not yet sufficient evidence for final 2020–2024 operational-model use. It must also be verified that every selected NYISO vintage represents a forecast actually published before 5:00 a.m., rather than a later post-close forecast.

## Current task

Continue `notebooks/04_feature_engineering.ipynb` immediately after the completed Step 6 merge validation.

1. Add a Markdown cell classifying NYISO columns as:
   - prediction target;
   - conditionally approved candidate predictor;
   - audit-only forecast fields; and
   - excluded or provisional fields.
2. Add a code cell defining:
   - `target_column = "day_ahead_price_usd_mwh"`
   - `candidate_feature_columns = ["load_forecast_mw"]`
   - `forecast_audit_columns` containing the cutoff, lead-time, availability-basis, proxy, archive, and source-file fields.
3. Run the new cells with the `Python 3.12 (electricity-forecasting)` kernel.
4. Verify that the target, candidate-feature, audit, and excluded groups print without error.
5. Preserve the NYISO availability limitation in notebook Markdown.

Do not yet create the final modeling CSV, add same-hour actual load or observed weather as operational predictors, or begin final model training.

## Future actions

### Required before full-period modeling

- Validate NYISO forecast-vintage availability timestamps using an authoritative publication or archive field rather than relying only on ZIP metadata.
- Download and validate the 2020–2024 NYISO ISO Load Forecast archive.
- Implement the PJM `load_frcstd_hist` MIDATL workflow with the strict pre-11:00 a.m. cutoff.
- Decide whether final PJM historical prices will use or be reconciled against the settlements-verified `rt_da_monthly_lmps` feed.
- Validate PSEG node `51301`, `PS`, MIDATL, `HUD VL`, and PTID `61758` for every study year.
- Obtain and implement NYISO Technical Bulletin TB-064 rules for daylight-saving transition hours.
- Decide whether archived structured weather forecasts are feasible. If not, limit the operational weather features to leakage-safe lags or exclude weather from the core model.
- Complete a NOAA station-history audit using HOMR for both stations.
- Re-run the complete cleaning, feature-engineering, and test workflow after full-period data are acquired.

### Documentation follow-up

- Keep private correspondence outside the public repository.
- Refer to the PJM reply as `PJM Case 00334055, received 2026-08-21` without publishing mail headers, personal contact information, or the raw confidentially labeled message.
- Cite public PJM, NYISO, and NOAA technical pages wherever a public source supports the same decision.
- Record every future change in `docs/methodology_decisions.md`, `docs/data_source_register.md`, and this status file.
