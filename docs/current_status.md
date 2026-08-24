# IDE Agent Handoff — Electricity Price Forecasting Capstone

## Project decision

Research question: How accurately can statistical and machine-learning models forecast hourly day-ahead electricity prices, and how does performance differ between PJM PSEG and NYISO Hudson Valley Zone G?

Current scope:

* PJM target: PSEG zone, pricing node 51301, `total_lmp_da`
* NYISO target: Hudson Valley Zone G day-ahead LMP
* Unit of analysis: one hourly observation per market
* Planned study period: 2020–2024, pending responses from PJM and NYISO
* January 2025 is a feasibility/pipeline sample only
* Store local timestamps and UTC timestamps
* Do not overwrite files under `data/raw/`

Actual load and same-hour observed weather are provisional predictors because they may not have been available at the day-ahead prediction cutoff. Final predictor selection must wait for PJM/NYISO guidance about historical forecasts, issuance times, market cutoffs, and revisions.

## Current status

- Created a project-specific Python 3.11 virtual environment.
- Installed the project in editable mode.
- Registered the `Python 3.11 (electricity-forecasting)` notebook kernel.
- Added `tzdata`, pandas, NumPy, pytest, ipykernel, and Ruff to the environment.
- Reorganized `02_data_cleaning.ipynb`.
- Standardized PJM and NYISO timestamps using timezone-aware local timestamps and UTC.
- Added reusable cleaning functions in `src/electricity_forecasting/data_processing.py`.
- Added NOAA weather cleaning and UTC conversion.
- Added PJM, NYISO, load, price, and weather merge logic.
- Corrected indentation and nested-function errors in `data_processing.py`.
- Confirmed that `data_processing.py` compiles successfully with `py_compile`.

### NYISO leakage-control update

- Recreated the project `.venv` with Python 3.12 and registered the
  `Python 3.12 (electricity-forecasting)` Jupyter kernel.
- Completed Steps 1–5 in `notebooks/04_feature_engineering.ipynb` for the
  January 2025 NYISO Hudson Valley load forecasts.
- Built `nyiso_hudson_valley_load_forecast_vintages.csv` with 4,464 forecast
  vintage rows covering 744 unique target hours.
- Applied a prediction cutoff of 5:00 a.m. America/New_York on the calendar
  day before delivery.
- Selected exactly one latest eligible load-forecast vintage for each of the
  744 target hours; post-cutoff vintages are excluded.
- Completed Step 6: merged the selected forecasts one-to-one with the 744-row
  NYISO electricity table, preserving cutoff and source-provenance fields.
- Verified the project test suite: 3 tests passed. Ruff checks passed for
  `src` and `tests`.
- Classified NYISO model columns in `notebooks/04_feature_engineering.ipynb`:
  `day_ahead_price_usd_mwh` is the target, `load_forecast_mw` is the sole
  approved load-based candidate predictor, forecast-vintage timing and
  provenance fields are audit-only, and same-hour actual load, observed weather,
  and target components are excluded from operational predictors.
- Completed Step 7: defined the target, candidate-predictor, forecast-audit,
  identifier, and excluded-operational column groups.
- Added and passed assertions that every grouped column exists, groups contain
  no duplicate names, groups do not overlap, and no target, audit, or excluded
  field is selected as an operational predictor.
- Preserved the NYISO availability-proxy warning: all 744 January rows use
  `availability_basis="zip_entry_last_modified"` and
  `availability_is_proxy=True`.
- Verified 744 unique January 2025 target hours with nonmissing target prices.
- Executed the saved notebook from a fresh Python 3.12 process through Step 7,
  stopping before the calendar-feature cells; all Steps 4–7 assertions passed.

## Current issue

The January 2025 NYISO load forecast uses the archived ZIP entry's
last-modified time as a proxy for the original forecast-availability time.
This is documented with `availability_is_proxy=True` and must be revisited
before using the approach for the planned 2020–2024 study period.

## Next task

Continue `notebooks/04_feature_engineering.ipynb` by deriving and validating
leakage-safe calendar features from `timestamp_local`.

## Exact Next Task

In `notebooks/04_feature_engineering.ipynb`, review the existing calendar
feature cells after the completed model-column classification:

1. Confirm their explanation states why calendar values are known at the
   day-ahead forecast cutoff.
2. Run the cells from a fresh Python 3.12 kernel to derive `hour_of_day`,
   `day_of_week`, and `is_weekend` from timezone-aware `timestamp_local`.
3. Confirm that only these calendar fields are appended to
   `candidate_feature_columns`.
4. Verify their valid ranges and nonmissingness.

Do not create a final modeling CSV, add same-hour actual load or observed
weather as predictors, or begin model training.
