# Electricity Price Forecasting Capstone

Graduate data-science capstone for forecasting and comparing hourly day-ahead electricity prices in:

- PJM PSEG pricing zone, pnode 51301
- NYISO Hudson Valley Zone G, HUD VL, PTID 61758

The target is hourly day-ahead total LMP/LBMP in `$/MWh`. The unit of analysis is one market-location-hour.

## Current state

January 2025 is the 744-hour feasibility sample. It is used to prove the data pipeline, timestamp handling, leakage controls, feature definitions, and reproducibility. It is not the final study period and must not be used for final capstone conclusions.

Verified work includes:

- source inventory and schema inspection in `notebooks/01_data_inventory.ipynb`;
- January electricity and weather cleaning in `notebooks/02_data_cleaning.ipynb`;
- two committed 744-row processed electricity tables;
- 4,464 NYISO load-forecast vintage rows covering 744 target hours;
- one latest eligible NYISO forecast selected per target using a D−1 05:00 Eastern cutoff;
- feature-role classification and leakage checks in `notebooks/04_feature_engineering.ipynb`; and
- three passing tests plus passing Ruff checks for `src` and `tests`.

All selected NYISO forecasts currently use a ZIP-entry last-modified timestamp as a documented availability proxy. That limitation must remain visible.

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

## Exact next action

Complete Task 1 only: run the calendar-feature cells in `notebooks/04_feature_engineering.ipynb` from a fresh Python 3.12 kernel and validate `hour_of_day`, `day_of_week`, and `is_weekend`. Do not create modeling-ready CSV files or train models yet.

## Repository guide

| Path | Purpose |
|---|---|
| `AGENTS.md` | Instructions and guardrails for Codex/IDE agents |
| `docs/current_status.md` | Short handoff, evidence, limitations, and exact next action |
| `docs/project_plan.md` | Authoritative project roadmap and completion gates |
| `docs/methodology_decisions.md` | Current methodological decisions and provisional assumptions |
| `docs/data_dictionary.md` | Field meanings, units, timing roles, and model eligibility |
| `docs/data_source_register.md` | Source provenance and unresolved source limitations |
| `docs/decisions.md` | Dated decision index |
| `docs/learning_log.md` | Student learning record and reproduction checks |
| `notebooks/` | Inventory, cleaning, EDA, feature engineering, and later modeling work |
| `src/electricity_forecasting/` | Reusable Python logic |
| `tests/` | Automated leakage, transformation, split, and validation checks |

## Reproducibility rules

- Use Python 3.12 and the project virtual environment.
- Run commands from the repository root.
- Install the package in editable mode with development dependencies.
- Use `timestamp_utc` for joins, order, validation, splitting, and modeling.
- Retain timezone-aware `timestamp_local` for calendar features and interpretation.
- Never modify files under `data/raw/`.
- Never use a predictor unless its availability before the forecast cutoff is documented and tested.
- Restart the kernel and run a completed notebook from top to bottom before calling it complete.
- Run `pytest` and `ruff check src tests` before each pre-modeling checkpoint.

See `docs/current_status.md` for the single next task.
