# Current Status — Electricity Price Forecasting Capstone

**Last verified:** August 29, 2026
**Current phase:** January 2025 pre-modeling completion gate  
**Current task:** Task 4 of 7 — complete the comparable PJM feature path

## Project scope

- Research question: How accurately can statistical and machine-learning models forecast hourly day-ahead electricity prices, and how does performance differ between PJM PSEG and NYISO Hudson Valley Zone G?
- PJM target: PSEG zone, pnode 51301, hourly day-ahead total LMP.
- NYISO target: Hudson Valley Zone G, HUD VL, PTID 61758, hourly day-ahead LBMP.
- Unit of analysis: one market-location-hour.
- Canonical time key: timezone-aware `timestamp_utc`.
- Interpretation and calendar key: timezone-aware `timestamp_local` in `America/New_York`.
- January 2025: 744-hour feasibility sample only.
- Planned primary study period: 2020–2024, subject to final feasibility and professor approval.
- Raw files are immutable.

## Verified completed work

- Python 3.12 project environment and notebook kernel are established.
- `notebooks/01_data_inventory.ipynb` contains seven code cells for file, shape, schema, and representative-row inspection.
- `notebooks/02_data_cleaning.ipynb` produces:
  - `data/processed/pjm_pseg_january_2025_electricity.csv` — 744 rows;
  - `data/processed/nyiso_hudson_valley_january_2025_electricity.csv` — 744 rows; and
  - `data/interim/nyiso_hudson_valley_load_forecast_vintages.csv` — 4,464 rows.
- The two electricity tables have 744 unique hourly timestamps, nonmissing prices and loads, and aligned price/load records.
- NOAA data are reduced to a complete January hourly index while preserving missing, quality, rejection, and imputation indicators.
- NYISO forecast construction preserves six vintages for each of 744 target hours.
- Notebook 04 Steps 1–7 are complete:
  - D−1 05:00 America/New_York cutoffs are calculated;
  - post-cutoff forecast vintages are excluded;
  - exactly one latest eligible forecast is selected per target;
  - selected forecasts are merged one-to-one with the NYISO electricity table;
  - target, candidate, audit, identifier, and excluded-operational groups are defined; and
  - overlap and prohibited-predictor checks pass.
- Three automated tests pass and Ruff passes for `src` and `tests`.
- Task 1 calendar-feature validation passed from a fresh Notebook 04 kernel:
  - 744 rows;
  - `hour_of_day` is nonmissing integer data spanning 0–23;
  - `day_of_week` is nonmissing integer data spanning 0–6, with Monday as 0;
  - `is_weekend` is nonmissing Boolean data and agrees with days 5 and 6;
  - `candidate_feature_columns` contains only `load_forecast_mw` plus the three calendar fields; and
  - `pytest` passed (3 tests) and `ruff check src tests` passed.
- Task 2 reusable-preprocessing reconciliation passed:
  - canonical price/load names are `day_ahead_price_usd_mwh` and `actual_load_mw`;
  - NOAA values retain the Notebook 02 SI interpretation;
  - one report per hour is selected by `FM-15`, then `FM-12`, then `FM-16` priority;
  - weather missingness, quality, rejection, and imputation flags survive the merge; and
  - fresh-process PJM and NYISO runs each produced 744 unique ordered hours with Notebook-matching weather-flag counts.
- Five automated tests pass and `ruff check src tests` passes.
- Task 3 forecast-origin-aware NYISO historical-price features passed:
  - prior-day same-hour source timestamps are explicitly joined and checked against each target hour’s cutoff;
  - 720 of 744 January target hours have a prior-day source, and all 720 are cutoff-safe under the provisional day-ahead-price availability rule;
  - `day_ahead_price_lag_1d` has 720 nonmissing cutoff-safe values;
  - `day_ahead_price_lag_1d_rolling_mean_24h` has 697 full-window values, built only from cutoff-safe lag values;
  - source availability, safe-feature masking, and full-window rolling behavior are implemented in `feature_engineering.py`;
  - a fresh Notebook 04 kernel completed with zero errors; five focused tests passed; and Ruff passed.


## Known limitations and unresolved inconsistencies

1. Every selected NYISO forecast currently has `availability_is_proxy=True` and `availability_basis="zip_entry_last_modified"`. This is a material limitation, not a cosmetic warning.
2. The January NOAA reconciliation is unaffected by daylight saving time; before the 2020–2024 expansion, reconcile the documented fixed-local-standard-time interpretation of raw NOAA `DATE` values with the market-local timestamp policy across DST transitions.
3. Generic row-based lags prove chronological order but do not by themselves prove predictor availability at the chosen forecast origin.
4. PJM has metered actual load in the current sample, not a verified historical day-ahead load-forecast vintage series.
5. `notebooks/03_exploratory_analysis.ipynb`, `05_baseline_models.ipynb`, and `06_model_comparison.ipynb` are still placeholders.
6. January 2025 cannot support final multi-year conclusions.

## External-response policy

Do not block progress on unanswered PJM or NYISO correspondence. Continue with documented, conservative, testable assumptions. Label those assumptions provisional and design the code so a later authoritative answer can replace a configuration value or availability rule without rewriting the pipeline.

## Authoritative pre-modeling completion gate — Tasks 1–7

Complete these tasks in order. Do not begin model fitting until all seven gates pass.

1. **Complete — validate calendar features in Notebook 04.** Fresh-kernel evidence confirms valid ranges, types, nonmissingness, weekend logic, and candidate-list membership for the three calendar fields.
2. **Complete — reconcile the notebook and reusable preprocessing paths.** The reusable January path uses the committed schema and matches Notebook 02’s SI-unit, report-priority, hourly-index, and weather-audit policies; focused regression tests pass.
3. **Complete — implement forecast-origin-aware NYISO historical-price features.** Explicit source-availability checks, cutoff-safe prior-day lags, and full-window rolling means are implemented and validated. The NYISO availability-proxy warning and provisional availability assumptions remain active.
4. **Complete the comparable PJM feature path.** Use the provisional PJM cutoff of D−1 11:00 America/New_York until authoritative evidence changes it. Exclude same-hour metered load and observed weather. Produce a minimum common feature set for both markets; retain the NYISO load-forecast feature as an explicitly augmented feature until a comparable PJM forecast series is available.
5. **Expand automated validation.** Populate the empty preprocessing and validation test files. Test schemas, timestamp order and uniqueness, calendar ranges, weather policy, cutoff eligibility, latest-vintage selection, tie failure, prohibited-column exclusion, row counts, and absence of future information. Require `pytest` and Ruff to pass.
6. **Complete and validate Notebook 03 EDA.** Use `notebooks/03_exploratory_analysis.ipynb` and the two committed January processed tables. Keep actual load and observed weather descriptive only, preserve negative and high prices, distinguish feasibility findings from final conclusions, and run from a fresh kernel.
7. **Create the pre-modeling checkpoint.** Export one validated January modeling-ready table per market with explicit target, candidate, identifier, audit, and excluded-field roles. Require 744 unique target hours, nonmissing targets, no prohibited predictors, successful fresh-process notebook runs, passing tests/Ruff, updated documentation, and a deliberate Git commit.

**Exit condition:** after Task 7, the January feasibility pipeline is ready for baseline-model development. January 2025 remains a feasibility sample; it is not the final 2020–2024 evidence base.


## Exact next task — Task 4

Complete the comparable PJM feature path.

1. Use the provisional PJM D−1 11:00 America/New_York cutoff, retained as a configurable assumption.
2. Build calendar and historical-price features using explicit source-availability checks relative to that cutoff.
3. Exclude same-hour metered load and observed target-hour weather from operational predictors.
4. Define the common NYISO/PJM feature set, and keep NYISO `load_forecast_mw` explicitly labeled as an augmented feature until comparable PJM forecast vintages exist.
5. Run fresh-kernel/process validation, focused tests, and Ruff; record the evidence before Task 5.
6. Do not export modeling-ready tables or begin EDA/modeling.

## Stop conditions

Do not yet:

- create the Task 7 modeling-ready CSV files;
- train, tune, or compare models;
- use same-hour actual load or observed weather as operational predictors;
- hide or remove the NYISO availability-proxy warning;
- treat positional lags as leakage-safe without an availability test; or
- describe January feasibility findings as final capstone results.
