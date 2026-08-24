# Current Status — Electricity Price Forecasting Capstone

**Last verified:** August 24, 2026  
**Current phase:** January 2025 pre-modeling completion gate  
**Current task:** Task 1 of 7 — validate calendar features in Notebook 04

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

## Known limitations and unresolved inconsistencies

1. Every selected NYISO forecast currently has `availability_is_proxy=True` and `availability_basis="zip_entry_last_modified"`. This is a material limitation, not a cosmetic warning.
2. Notebook 02 and `src/electricity_forecasting/data_processing.py` do not yet implement identical NOAA unit and hourly-selection policies.
3. Configuration/modules still use older names such as `day_ahead_lmp` and `load_mw`, while the committed tables use `day_ahead_price_usd_mwh` and `actual_load_mw`.
4. Generic row-based lags prove chronological order but do not by themselves prove predictor availability at the chosen forecast origin.
5. PJM has metered actual load in the current sample, not a verified historical day-ahead load-forecast vintage series.
6. `notebooks/03_exploratory_analysis.ipynb`, `05_baseline_models.ipynb`, and `06_model_comparison.ipynb` are still placeholders.
7. January 2025 cannot support final multi-year conclusions.

## External-response policy

Do not block progress on unanswered PJM or NYISO correspondence. Continue with documented, conservative, testable assumptions. Label those assumptions provisional and design the code so a later authoritative answer can replace a configuration value or availability rule without rewriting the pipeline.

## Authoritative pre-modeling completion gate — Tasks 1–7

Complete these tasks in order. Do not begin model fitting until all seven gates pass.

1. **Validate calendar features in Notebook 04.** From a fresh Python 3.12 kernel, run through the existing feature-role classification and derive `hour_of_day`, `day_of_week`, and `is_weekend` from timezone-aware `timestamp_local`. Prove valid ranges, types, nonmissingness, and candidate-list membership.
2. **Reconcile the notebook and reusable preprocessing paths.** Make `src/electricity_forecasting/data_processing.py` and configuration use the committed schema (`day_ahead_price_usd_mwh` and `actual_load_mw`), the same NOAA SI-unit interpretation, the same hourly-report selection rule, and the same quality/rejection flags as Notebook 02.
3. **Implement forecast-origin-aware historical features.** Replace assumptions based only on row position with explicit availability checks relative to each market cutoff. Add price lags and shifted rolling statistics only after tests prove that every source value was knowable at prediction time.
4. **Complete the comparable PJM feature path.** Use the provisional PJM cutoff of D−1 11:00 America/New_York until authoritative evidence changes it. Exclude same-hour metered load and observed weather. Produce a minimum common feature set for both markets; retain the NYISO load-forecast feature as an explicitly augmented feature until a comparable PJM forecast series is available.
5. **Expand automated validation.** Populate the empty preprocessing and validation test files. Test schemas, timestamp order and uniqueness, calendar ranges, weather policy, cutoff eligibility, latest-vintage selection, tie failure, prohibited-column exclusion, row counts, and absence of future information. Require `pytest` and Ruff to pass.
6. **Complete and validate Notebook 03 EDA.** Use `notebooks/03_exploratory_analysis.ipynb` and the two committed January processed tables. Keep actual load and observed weather descriptive only, preserve negative and high prices, distinguish feasibility findings from final conclusions, and run from a fresh kernel.
7. **Create the pre-modeling checkpoint.** Export one validated January modeling-ready table per market with explicit target, candidate, identifier, audit, and excluded-field roles. Require 744 unique target hours, nonmissing targets, no prohibited predictors, successful fresh-process notebook runs, passing tests/Ruff, updated documentation, and a deliberate Git commit.

**Exit condition:** after Task 7, the January feasibility pipeline is ready for baseline-model development. January 2025 remains a feasibility sample; it is not the final 2020–2024 evidence base.

## Exact next task — Task 1

In `notebooks/04_feature_engineering.ipynb`:

1. Restart into the `Python 3.12 (electricity-forecasting)` kernel.
2. Run the notebook from the top through the completed Step 7 cells.
3. Run the existing calendar-feature cells.
4. Confirm:
   - `hour_of_day` contains integers 0–23;
   - `day_of_week` contains integers 0–6, where Monday is 0;
   - `is_weekend` is Boolean and agrees with days 5 and 6;
   - none of the three fields is missing;
   - only those three fields are appended to `candidate_feature_columns`; and
   - all prior target/audit/excluded overlap assertions still pass.
5. Record the row count, ranges, and candidate list in the notebook output.
6. Add or update a focused automated test if the reusable calendar-feature function is exercised.
7. Run `pytest` and `ruff check src tests`.

### Task 1 completion evidence

- Fresh-kernel notebook output showing 744 rows.
- Valid ranges and nonmissingness for all three fields.
- Candidate list contains `load_forecast_mw` plus the three calendar fields and no prohibited field.
- Tests and Ruff pass.
- `docs/current_status.md` advances to Task 2 only after this evidence exists.

## Stop conditions

Do not yet:

- create the Task 7 modeling-ready CSV files;
- train, tune, or compare models;
- use same-hour actual load or observed weather as operational predictors;
- hide or remove the NYISO availability-proxy warning;
- treat positional lags as leakage-safe without an availability test; or
- describe January feasibility findings as final capstone results.
