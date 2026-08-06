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

## Current issue

- Complete the final validation of all imports and run Notebook 2 from top to bottom.
- Confirm the processed PJM and NYISO exports each contain 744 hourly rows.
- Confirm weather columns merge correctly and document remaining missing values.

## Next task

Run:

```powershell
python -m ruff check src\electricity_forecasting\data_processing.py
python -m pytest -v
## Important files

Repository files:

* `AGENTS.md`
* `notebooks/01_data_inventory.ipynb`
* `notebooks/02_data_cleaning.ipynb`
* `data/processed/pjm_pseg_january_2025_electricity.csv`
* `data/processed/nyiso_hudson_valley_january_2025_electricity.csv`
* `docs/textbook_notes/`

Source datasets include:

* PJM day-ahead hourly LMP
* PJM PS metered load
* NYISO Hudson Valley day-ahead LMP
* NYISO Hudson Valley integrated load
* January 2025 Newark weather
* January 2025 Stewart weather
* DATA 698 syllabus

The two processed CSVs are already committed and pushed. The last known working tree also contained modified notebooks and possibly `AGENTS.md`, plus untracked `docs/textbook_notes/`. Do not assume these remaining changes have been committed; inspect `git status` first. Do not discard or overwrite any existing work.

## Exact Next Task

Complete and validate:

`notebooks/03_exploratory_data_analysis.ipynb`

Use only the two committed January 2025 electricity files under `data/processed/`.

The notebook must:

1. Load both processed CSVs using repository-relative paths.
2. Confirm 744 rows and 744 unique hourly timestamps per market.
3. Confirm there are no missing price or load values.
4. Display column names, data types, and timestamp ranges.
5. Produce descriptive statistics for price and load.
6. Plot hourly price and load time series for both markets.
7. Compare price distributions.
8. Analyze prices by hour of day and day of week.
9. Calculate price-load correlations separately for each market, clearly labeling actual load as provisional.
10. Identify negative-price and unusually high-price hours without deleting, replacing, or winsorizing them.
11. Write a concise summary of the findings and the limitations of using only January 2025.
12. Restart the kernel and run the notebook from top to bottom, resolving all errors before completion.

Do not:

- Merge weather data.
- Begin final model training.
- Download or process the full historical period as part of this task.
- Treat actual load as an approved final predictor.
- Finalize the predictor set before resolving forecast-availability questions.
- Modify `01_data_inventory.ipynb` or `02_data_cleaning.ipynb` unless correcting a reproducibility defect.

After validation, commit and push the completed Notebook 03 deliberately.