# Electricity Price Forecasting Capstone — Project Plan

**Last updated:** August 31, 2026
**Current phase:** January 2025 pre-modeling completion gate  
**Current task:** Task 7 of 7 — create the pre-modeling checkpoint

## How to Use This Document

This file is the authoritative academic and technical roadmap for the capstone. It records the project scope, methodological decisions, milestones, risks, schedule, and completion criteria.

- Use `docs/current_status.md` for the short, frequently updated handoff.
- Use `AGENTS.md` for instructions that govern coding-agent behavior in the repository.
- Use this file when a milestone, project decision, dependency, or scope item changes.

### Document Organization

| Part | Sections | Purpose |
|---|---|---|
| Project definition | 1–5 | Research question, significance, and scope |
| Data and methods | 6–13 | Sources, feasibility results, predictors, models, features, and evaluation |
| Execution | 14–18 | Completed work, current milestone, dependencies, risks, and schedule |
| Delivery and governance | 19–25 | Literature, reproducibility, next tasks, completion criteria, status, and dashboard |

## Authoritative pre-modeling completion gate — Tasks 1–7

Complete these tasks in order. Do not begin model fitting until all seven gates pass.

1. **Complete — validate calendar features in Notebook 04.** Fresh-kernel validation confirmed the derived fields' ranges, types, nonmissingness, weekend logic, and candidate-list membership.
2. **Complete — reconcile the notebook and reusable preprocessing paths.** The reusable January path now uses the committed schema and matches Notebook 02's SI-unit, report-priority, complete-hourly-index, and weather-audit policies.
3. **Complete — implement forecast-origin-aware historical features.** Explicit availability checks, cutoff-safe prior-day lags, and full-window rolling statistics are implemented and validated for NYISO. Availability assumptions remain provisional.
4. **Complete — comparable PJM feature path.** The provisional D−1 11:00 America/New_York cutoff, cutoff-safe historical-price features, excluded same-hour operational fields, and common-versus-NYISO-augmented feature sets are implemented and validated.
5. **Complete — expand automated validation.** Tests cover schemas, timestamp order and uniqueness, calendar ranges, weather policy, cutoff eligibility, latest-vintage selection and tie failure, prohibited-column exclusion, row counts, and absence of future information. The full 21-test suite and Ruff pass.
6. **Complete — validate Notebook 03 EDA.** Notebook 03 provides descriptive January price/load analysis, retains and identifies high/negative prices, labels same-hour actual load and observed weather as non-operational, and runs from a fresh kernel without errors.
7. **Create the pre-modeling checkpoint.** Export one validated January modeling-ready table per market with explicit target, candidate, identifier, audit, and excluded-field roles. Require 744 unique target hours, nonmissing targets, no prohibited predictors, successful fresh-process notebook runs, passing tests/Ruff, updated documentation, and a deliberate Git commit.

**Exit condition:** after Task 7, the January feasibility pipeline is ready for baseline-model development. January 2025 remains a feasibility sample; it is not the final 2020–2024 evidence base.

---

## 1. Project Overview

This graduate data-science capstone will develop, evaluate, and compare models for forecasting hourly day-ahead electricity prices in two wholesale electricity markets:

- PJM PSEG pricing zone
- NYISO Hudson Valley Zone G

The project will compare statistical baselines, regularized regression, and tree-based machine-learning models using predictors that can be verified as available before the applicable day-ahead forecasting cutoff.

January 2025 is being used as a feasibility sample for developing and validating the data pipeline. The planned primary study period is January 1, 2020, through December 31, 2024, subject to confirmation of historical data availability, definitions, timestamp conventions, and forecast issuance information.

---

## 2. Working Research Question

**How accurately can statistical and machine-learning models forecast hourly day-ahead electricity prices, and how does predictive performance differ between PJM PSEG and NYISO Hudson Valley Zone G?**

---

## 3. Supporting Research Questions

1. Which forecasting model produces the lowest out-of-sample error in each market?
2. Does the best-performing model differ between PJM and NYISO?
3. How does forecasting accuracy vary by hour of day, day of week, season, and price level?
4. How well do relatively simple statistical models perform compared with tree-based machine-learning models?
5. How do models perform during negative-price and unusually high-price periods?
6. What market or data characteristics may help explain differences in predictive performance between PJM and NYISO?

---

## 4. Academic and Practical Significance

Day-ahead electricity prices affect generators, utilities, energy traders, large consumers, and market operators. These prices are difficult to predict because they are influenced by time-dependent demand, weather, generation availability, congestion, fuel costs, and market-specific operating conditions.

Comparing PJM and NYISO provides an opportunity to determine whether the same forecasting methods perform consistently across two organized wholesale electricity markets. The project will also demonstrate practical data-science skills in:

- Data acquisition and validation
- Time-series data cleaning
- Timestamp and timezone management
- Exploratory data analysis
- Feature engineering
- Leakage prevention
- Regression modeling
- Machine-learning model comparison
- Chronological validation
- Reproducible research
- Technical documentation and presentation

---

## 5. Project Scope

### 5.1 Markets and Selected Locations

| Market | Selected location             | Target variable            |
| ------ | ----------------------------- | -------------------------- |
| PJM    | PSEG zone, pricing node 51301 | Hourly day-ahead total LMP |
| NYISO  | Hudson Valley Zone G          | Hourly day-ahead LMP       |

### 5.2 Dependent Variable

The dependent variable is the hourly day-ahead locational marginal price in dollars per megawatt-hour (`$/MWh`).

PJM currently uses the `total_lmp_da` field. Confirmation has been requested that this represents the complete day-ahead LMP, including applicable energy, congestion, and marginal-loss components.

### 5.3 Unit of Analysis

One hourly observation per market.

PJM and NYISO will be modeled separately. Their model performance will then be compared using consistent evaluation metrics and evaluation periods.

### 5.4 Feasibility Period

January 1–31, 2025.

Each market contains 744 hourly observations during this period.

### 5.5 Planned Primary Study Period

January 1, 2020, through December 31, 2024.

The five-year period will not be finalized until the project confirms:

- Historical data availability
- Consistency of market-location definitions
- Historical forecast availability
- Forecast issuance timestamps
- Prediction cutoffs
- Daylight-saving-time treatment
- Whether important dataset definitions changed during the period

### 5.6 Primary Forecast Horizon

The intended task is day-ahead hourly price forecasting.

The exact cutoff must specify what information would have been available when the forecast was produced. This cutoff remains provisional pending clarification from PJM and NYISO.

### 5.7 Out-of-Scope Items

The primary capstone will not include:

- Real-time streaming infrastructure
- Causal inference
- Retrieval-augmented generation
- Hugging Face or large language models
- Multiple pricing locations within each market
- Logistic price-spike classification
- Extensive AWS production architecture
- LSTM or GRU neural networks unless substantial time remains

These may be discussed as future extensions.

---

## 6. Data Sources

| Dataset                             | Source                | Intended purpose                                   | Current status                                     |
| ----------------------------------- | --------------------- | -------------------------------------------------- | -------------------------------------------------- |
| PJM Day-Ahead Hourly LMP            | PJM Data Miner 2      | PJM target variable                                | January sample validated                           |
| PJM PS Hourly Load: Metered         | PJM Data Miner 2      | Feasibility EDA and possible predictor             | Validated but provisional                          |
| NYISO Hudson Valley Day-Ahead LMP   | NYISO                 | NYISO target variable                              | January sample validated                           |
| NYISO Hudson Valley integrated load | NYISO                 | Feasibility EDA and possible predictor             | Validated but provisional                          |
| Newark weather observations         | NOAA                  | PJM-area weather feasibility testing               | January reusable path reconciled; 744 hours        |
| Stewart weather observations        | NOAA                  | NYISO-area weather feasibility testing             | January reusable path reconciled; 744 hours        |
| Calendar variables                  | Derived               | Hour, weekday, month, season, and holiday features | Hour/day/weekend validated in Task 1               |
| Historical day-ahead load forecasts | PJM and NYISO         | Potential final predictor                          | Availability under investigation                   |
| Historical weather forecasts        | To be determined      | Potential final predictor                          | Availability under investigation                   |
| Historical price lags               | Derived from LMP data | Final predictor                                    | Planned                                            |
| Natural-gas prices                  | To be determined      | Optional predictor                                 | Include only if readily available and time permits |

Raw source files must remain unchanged under `data/raw/`.

---

## 7. Current Repository Files

### 7.1 Main Notebooks

```text
notebooks/
├── 01_data_inventory.ipynb
├── 02_data_cleaning.ipynb
├── 03_exploratory_analysis.ipynb
├── 04_feature_engineering.ipynb
├── 05_baseline_models.ipynb
└── 06_model_comparison.ipynb
```

### 7.2 Processed January Files

```text
data/processed/
├── pjm_pseg_january_2025_electricity.csv
└── nyiso_hudson_valley_january_2025_electricity.csv
```

The two processed CSV files are committed to and tracked by Git.

These files are suitable for:

- Pipeline testing
- Exploratory data analysis
- Feature-engineering tests
- Preliminary modeling-code tests
- Reproducibility verification

They are not the final modeling datasets.

### 7.3 Other Project Files

```text
AGENTS.md
PROJECT_PLAN.md
docs/textbook_notes/
```

`AGENTS.md` contains repository guidance for IDE coding agents. It should not be used as a replacement for the academic project plan.

---

## 8. January 2025 Feasibility Results

### 8.1 Electricity Data Validation

| Validation check           | PJM | NYISO |
| -------------------------- | --: | ----: |
| Hourly records             | 744 |   744 |
| Unique hourly timestamps   | Yes |   Yes |
| Missing price values       |   0 |     0 |
| Missing load values        |   0 |     0 |
| Matched price/load records | 744 |   744 |

The price and load datasets were successfully aligned within each market.

### 8.2 Weather Data Validation

| Validation check                  | Newark | Stewart |
| --------------------------------- | -----: | ------: |
| Output hourly records             |    744 |     744 |
| Incomplete hours                  |      3 |       7 |
| Corrupted observations rejected   |      0 |       4 |
| Future-looking interpolation used |     No |      No |

The clearly implausible Stewart observations were rejected. Examples included extreme temperature, dew-point, humidity, and wind values that were physically unrealistic.

NOAA quality flags are retained. A quality-flagged observation is not automatically treated as corrupted.

Missing weather measurements remain visible. They have not been filled using future observations or substituted with measurements from the other weather station.

### 8.3 Timestamp Status

The January feasibility data include local and UTC timestamp handling.

January occurs entirely under Eastern Standard Time, but the final 2020–2024 dataset will cross daylight-saving-time transitions. Timezone-aware conversion and explicit handling of repeated or missing local hours will therefore be required.

---

## 9. Methodological Decisions

The following decisions currently govern the project:

- The target is hourly day-ahead LMP in `$/MWh`.
- PJM and NYISO will be modeled separately.
- Results will be compared using the same evaluation metrics.
- Local market timestamps and UTC timestamps will both be retained.
- Daylight-saving-time transitions will be explicitly validated.
- Only information available before the prediction cutoff may be used as a final predictor.
- Same-hour actual load is provisional because it may not have been available when a day-ahead prediction would have been made.
- Same-hour observed weather is provisional for the same reason.
- Historical weather forecasts are preferred if they can be obtained with valid issuance timestamps.
- Lagged observed weather may be considered only when the lag guarantees availability before the prediction cutoff.
- Historical price lags and calendar variables form the minimum defensible predictor set.
- Time-series observations will not be randomly shuffled.
- Training, validation, and testing will follow chronological order.
- Missing values will not be filled using future observations.
- Negative electricity prices will be retained.
- Price spikes will be retained as legitimate market outcomes.
- Extreme prices will not be deleted or winsorized without documented justification.
- Correlation will not be interpreted as causation.
- Raw datasets will never be overwritten.
- Processed outputs will be reproducibly generated from the raw data.

---

## 10. Predictor Status

| Predictor                     | Current status | Final-use requirement                            |
| ----------------------------- | -------------- | ------------------------------------------------ |
| Historical day-ahead LMP lags | Planned        | Lag must precede prediction cutoff               |
| Hour of day                   | Approved       | Derived from target operating hour               |
| Day of week                   | Approved       | Derived from target operating date               |
| Weekend indicator             | Approved       | Derived from calendar                            |
| Month and season              | Approved       | Derived from calendar                            |
| Holiday indicator             | Planned        | Holiday calendar must be documented              |
| Actual metered load           | Provisional    | Must be available before cutoff or excluded      |
| Day-ahead load forecast       | Preferred      | Issuance timestamp and revision history required |
| Observed weather              | Provisional    | Must be appropriately lagged                     |
| Historical weather forecast   | Preferred      | Forecast must have been issued before cutoff     |
| Natural-gas price             | Optional       | Must be historically available before cutoff     |

---

## 11. Planned Models

The primary model comparison will include:

1. Historical-average or persistence baseline
2. Regularized linear regression, such as Ridge or Elastic Net
3. Random Forest regression
4. Gradient-boosted tree regression, such as XGBoost

A simple unregularized linear regression may also be included as an interpretable reference model.

Additional models will only be added if they materially improve the study and can be completed within the course schedule.

LSTM or GRU models are not part of the primary scope because they would increase implementation, tuning, and interpretability demands without being necessary to answer the research question.

---

## 12. Feature Engineering Plan

Potential features include:

### 12.1 Price-History Features

- Previous available hourly prices
- Price at the same hour on the previous day
- Price at the same hour during the previous week
- Backward-looking rolling averages
- Backward-looking rolling standard deviations
- Recent minimum and maximum prices

Every rolling or lagged feature must use only information available before the prediction cutoff.

### 12.2 Calendar Features

- Hour of day
- Day of week
- Weekend indicator
- Holiday indicator
- Month
- Season
- Cyclical sine and cosine encodings for hour and calendar variables

### 12.3 Load Features

- Day-ahead load forecast, if historically available
- Properly lagged actual load, if used
- Recent backward-looking load changes
- Load forecast differences or ramp indicators, if available

### 12.4 Weather Features

- Forecast temperature
- Forecast humidity
- Forecast wind
- Heating- and cooling-related variables
- Properly lagged observations when forecast archives are unavailable

Same-hour observed weather will not be used as a final predictor unless its availability at prediction time can be demonstrated.

---

## 13. Validation and Evaluation Strategy

### 13.1 Data Splitting

The data will be divided chronologically.

A possible structure is:

- Training: earlier years
- Validation: a later period used for model selection
- Testing: the final untouched period

The exact years will be determined after the full dataset is acquired and validated.

Random train-test splitting will not be used.

### 13.2 Cross-Validation

Model tuning should use time-series cross-validation or rolling-origin evaluation.

Each training window must occur before its corresponding validation window.

### 13.3 Primary Metrics

- Mean Absolute Error
- Root Mean Squared Error

MAE will provide an interpretable measure of typical forecast error. RMSE will place greater emphasis on large errors and price-spike periods.

### 13.4 Secondary Analyses

Forecast errors may also be evaluated by:

- Market
- Hour of day
- Weekday versus weekend
- Month or season
- Negative-price periods
- High-price periods
- Normal-price versus extreme-price conditions

MAPE will not be a primary metric because electricity prices can be zero or negative.

### 13.5 Model Comparison

The same evaluation definitions and test periods will be used wherever possible for both markets. Market-specific differences will be documented rather than concealed through forced variable equivalence.

### 13.6 Planned Ablation and Error-Regime Analyses

The final model-comparison deliverables will include two additions that improve interpretation without expanding the primary model families:

- **Feature ablation:** compare the common calendar-and-availability-safe-price-history feature set with the NYISO augmented set that additionally includes `load_forecast_mw`. Use the same model, chronological split, and metric definitions for both runs. Label the NYISO result as conditional because its forecast availability is currently supported by a ZIP-entry proxy.
- **Error by regime:** report MAE and RMSE by hour of day, weekday versus weekend, and normal-price versus extreme-price regimes. Define any regime threshold using training data only and preserve negative and high prices.

If time permits after the primary comparison is complete, add feature-importance stability across rolling validation folds and a concise bounded-tuning diagnostic. Do not add new model families or use the final test set for these decisions.

---

## 14. Completed Work

- [x] Selected PJM and NYISO as the comparison markets.
- [x] Selected PSEG and Hudson Valley Zone G as the representative locations.
- [x] Defined the working research question.
- [x] Defined one hourly observation per market as the unit of analysis.
- [x] Selected January 2025 as the feasibility period.
- [x] Identified 2020–2024 as the proposed primary study period.
- [x] Downloaded the January 2025 feasibility datasets.
- [x] Created `notebooks/01_data_inventory.ipynb`.
- [x] Created `notebooks/02_data_cleaning.ipynb`.
- [x] Validated all four electricity tables.
- [x] Confirmed 744 unique January hours per market.
- [x] Merged price and load within each market.
- [x] Cleaned and validated Newark weather.
- [x] Cleaned and validated Stewart weather.
- [x] Rejected four clearly corrupted Stewart observations.
- [x] Preserved missing and quality-flagged weather observations.
- [x] Avoided future-looking weather interpolation.
- [x] Added local and UTC timestamp handling for the January sample.
- [x] Exported the two processed electricity datasets.
- [x] Updated `.gitignore` to permit the intended processed CSV files.
- [x] Committed and pushed the processed January datasets.
- [x] Created `notebooks/03_exploratory_analysis.ipynb`.
- [x] Prepared detailed historical-data questions for PJM.
- [ ] Receive and document responses from PJM and NYISO.
- [ ] Finalize the prediction cutoff.
- [ ] Finalize the approved predictor set.
- [ ] Complete and validate all January EDA requirements.
- [ ] Acquire the full historical datasets.
- [ ] Build final analysis-ready datasets.
- [ ] Train and evaluate the forecasting models.
- [ ] Complete the paper and presentation.

---

## 15. Task 6 Milestone: January 2025 EDA

Notebook:

```text
notebooks/03_exploratory_analysis.ipynb
```

The notebook has been created. The next step is to complete and validate its contents.

### 15.1 Required EDA Work

- [ ] Load both processed January CSV files using repository-relative paths.
- [ ] Confirm that each market has 744 rows.
- [ ] Confirm that each market has 744 unique hourly timestamps.
- [ ] Confirm that price and load contain no missing values.
- [ ] Display column names, data types, and timestamp ranges.
- [ ] Produce descriptive statistics for price and load.
- [ ] Plot hourly PJM and NYISO price time series.
- [ ] Plot hourly PJM and NYISO load time series.
- [ ] Compare the two price distributions.
- [ ] Analyze prices by hour of day.
- [ ] Analyze prices by day of week.
- [ ] Calculate price-load correlations separately for each market.
- [ ] Clearly label actual load as a provisional predictor.
- [ ] Identify all negative-price hours.
- [ ] Define and identify unusually high-price hours.
- [ ] Retain all negative and high-price observations.
- [ ] Write a short interpretation of the principal findings.
- [ ] Document the limitations of using only January 2025.
- [ ] Restart the kernel and run the notebook from top to bottom.
- [ ] Resolve all notebook errors before considering the milestone complete.

### 15.2 EDA Constraints

- Use only the two committed January 2025 processed electricity datasets.
- Treat January 2025 as a feasibility sample rather than the final study dataset.
- Analyze PJM and NYISO separately before comparing them.
- Do not interpret correlation as causation.
- Do not treat actual load as an approved final predictor.
- Do not delete, replace, or winsorize negative or unusually high prices.
- Do not merge weather during this milestone.
- Do not begin final model training in the EDA notebook.
- Do not finalize the full-period predictor set before resolving the forecast-availability questions.

### 15.3 EDA Deliverables

- Validated January input tables
- Descriptive-statistics tables
- Price time-series charts
- Load time-series charts
- Price-distribution comparisons
- Hour-of-day summaries
- Day-of-week summaries
- Price-load correlation results
- Negative-price observation tables
- High-price observation tables
- Written findings and limitations
- A notebook that runs successfully from a restarted kernel

---

## 16. Open Questions and External Dependencies

The following questions must be resolved before finalizing the full modeling dataset:

### 16.1 PJM Questions

1. Is PSEG pricing node 51301 the appropriate zonal day-ahead LMP aggregate to pair with the PS metered-load area?
2. Does `total_lmp_da` represent the complete hourly day-ahead LMP in `$/MWh`, including energy, congestion, and marginal-loss components?
3. Should finalized historical research use the Day-Ahead Hourly LMP feed or another settlements-verified feed?
4. Does PJM maintain historical day-ahead load forecasts with target operating hours and issuance timestamps?
5. Can the forecasts be retrieved as they existed before the relevant day-ahead market cutoff?
6. What prediction cutoff would PJM recommend for an academic day-ahead forecasting experiment?
7. Did definitions, identifiers, timestamp conventions, or processing methods change during 2020–2024?
8. How are daylight-saving-time transition hours represented?

### 16.2 NYISO Questions

Equivalent NYISO questions must confirm:

- The correct Hudson Valley Zone G day-ahead LMP dataset
- The appropriate load area or forecast series
- Historical day-ahead load-forecast availability
- Forecast issuance and revision timestamps
- Recommended prediction cutoff
- Historical identifier or definition changes
- Daylight-saving-time conventions
- Comparability with the selected PJM data

### 16.3 Weather Questions

- Are historical archived weather forecasts available for both selected regions?
- Do the archives include forecast issuance timestamps?
- Are the forecast horizons compatible with the market prediction cutoff?
- If forecast archives are unavailable, which lagged observed-weather variables can be used without leakage?

---

## 17. Risk Management

| Risk                                                                | Effect on project                            | Mitigation                                                                     |
| ------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------ |
| Historical load forecasts are unavailable                           | Removes a desirable day-ahead predictor      | Use price history and calendar variables as the minimum defensible model       |
| Forecast issuance times are unavailable                             | Creates leakage uncertainty                  | Exclude variables whose historical availability cannot be proven               |
| Actual load creates target-time leakage                             | Inflated model performance                   | Keep actual load provisional or use valid lags                                 |
| Observed weather creates leakage                                    | Inflated model performance                   | Use historical forecasts or carefully lagged observations                      |
| PJM and NYISO variables are not directly equivalent                 | Weakens direct feature comparison            | Model markets separately and document differences                              |
| Daylight-saving transitions create missing or duplicate local hours | Misaligned records                           | Store timezone-aware local and UTC timestamps and validate each year           |
| Extreme prices dominate squared-error measures                      | Can obscure typical performance              | Retain extremes and report both MAE and RMSE                                   |
| Missing weather observations reduce usable data                     | Can create inconsistent samples              | Document missingness and use backward-looking methods only if justified        |
| Data definitions changed during 2020–2024                           | Produces invalid historical joins            | Verify identifiers and definitions before bulk processing                      |
| Scope becomes too large                                             | Threatens completion within 13 weeks         | Limit the primary study to two markets, two locations, and four model families |
| Model tuning becomes excessive                                      | Delays writing and evaluation                | Use bounded, documented hyperparameter searches                                |
| Git commits include unrelated files                                 | Makes project history difficult to interpret | Review `git status` and stage related files deliberately                       |

---

## 18. Thirteen-Week Schedule

| Week | Primary objective                           | Deliverable                                                  |
| ---- | ------------------------------------------- | ------------------------------------------------------------ |
| 1    | Finalize research question and scope        | Documented question, locations, target, and exclusions       |
| 2    | Validate data availability                  | Data inventory and source documentation                      |
| 3    | Build January feasibility pipeline          | Reproducible cleaning and validation notebook                |
| 4    | Complete preliminary EDA                    | Executed January EDA notebook, figures, tables, and findings |
| 5    | Review literature and prepare proposal      | Research proposal and preliminary bibliography               |
| 6    | Acquire full historical data                | Documented raw 2020–2024 datasets                            |
| 7    | Clean, align, and engineer features         | Validated analysis-ready datasets                            |
| 8    | Complete first major paper sections         | Midterm draft                                                |
| 9    | Build baseline and regularized models       | Baseline and linear-model results                            |
| 10   | Build tree-based models                     | Random Forest and gradient-boosting results                  |
| 11   | Tune, evaluate, and compare models          | Final metric tables and diagnostic figures                   |
| 12   | Write results, limitations, and conclusions | Complete final-paper draft                                   |
| 13   | Revise and prepare presentation             | Final paper, repository, and presentation                    |

The schedule will remain aligned with the DATA 698 syllabus requirements, including:

- Research proposal of at least 3 pages
- Midterm draft of approximately 10–12 pages or more
- Final paper of approximately 15–20 single-spaced pages or more
- Final presentation of approximately 5–10 minutes

---

## 19. Literature Review Plan

The literature review will address:

- Day-ahead electricity-price forecasting
- Characteristics of PJM and NYISO day-ahead markets
- Statistical electricity-price models
- Regularized regression for time-series forecasting
- Random Forest and gradient-boosting methods
- Price spikes and negative electricity prices
- Load and weather as electricity-price predictors
- Chronological validation and data-leakage prevention
- Cross-market forecasting comparisons

Sources should primarily include:

- Peer-reviewed journal articles
- Conference papers where appropriate
- PJM and NYISO technical documentation
- Government sources such as EIA and NOAA
- Authoritative software documentation for implemented methods

Every source used in the final paper must be recorded with sufficient information for complete citation.

---

## 20. Reproducibility and Repository Standards

- Run project commands from the repository root.
- Use repository-relative paths in notebooks and reusable code.
- Do not depend on a specific Windows user directory.
- Keep raw data immutable.
- Store temporary transformations under `data/interim/`.
- Store analysis-ready datasets under `data/processed/`.
- Store model outputs, predictions, and metrics under `outputs/`.
- Store report figures and tables under the appropriate report directories.
- Use clear notebook execution order.
- Restart the kernel and run every completed notebook from top to bottom.
- Record dataset sources, fields, units, and decisions under `docs/`.
- Use Git commits that group logically related changes.
- Review `git status` before staging files.
- Do not use `git add .` without reviewing every included change.
- Do not commit credentials, tokens, personal information, or restricted data.
- Keep public processed feasibility samples only when repository size and data-use rules permit them.

---

## 21. Immediate Next Task

Complete Task 3 only: implement forecast-origin-aware historical price features.

1. Define each market's provisional prediction cutoff and an availability timestamp for every proposed lag or rolling source value.
2. Prove each source value was available at or before the target hour's cutoff; chronological row position alone is insufficient.
3. Add only availability-safe price lags and shifted rolling statistics.
4. Add tests for post-cutoff values, missing elapsed hours, and target leakage in rolling windows.
5. Preserve the NYISO ZIP-entry availability-proxy warning and provisional PJM D−1 11:00 / NYISO D−1 05:00 cutoffs.
6. Run fresh-process validation, `pytest`, and `ruff check src tests`.

Do not create Task 7 modeling-ready CSV files or train models during Task 3.

---

## 22. Tasks That Can Proceed While Awaiting ISO Responses

The following work can proceed safely:

- Complete January exploratory data analysis.
- Continue the literature review.
- Build the project bibliography.
- Document data dictionaries.
- Design feature-engineering functions using January data.
- Test chronological splitting code.
- Implement baseline-model scaffolding using leakage-safe features.
- Draft the introduction, background, and methodology sections.
- Document all provisional variables and unresolved decisions.

The following work should wait:

- Final predictor approval
- Final prediction-cutoff definition
- Bulk 2020–2024 processing
- Use of same-hour actual load in final models
- Use of same-hour observed weather in final models
- Final comparison of market predictor sets

---

## 23. Definition of Project Completion

The project will be considered complete when:

- The final research question is precise and academically defensible.
- The PJM and NYISO targets and locations are fully documented.
- The prediction cutoff is explicitly defined.
- Every final predictor is verified as available before that cutoff.
- The full historical data are reproducibly cleaned and validated.
- Timezone and daylight-saving transitions are handled correctly.
- Leakage-safe features are generated reproducibly.
- Baseline, regularized, Random Forest, and boosted-tree models are trained.
- Models are evaluated using chronological out-of-sample data.
- PJM and NYISO results are compared using consistent metrics.
- Negative and high-price performance is documented.
- Limitations and market differences are clearly explained.
- The final paper satisfies the DATA 698 requirements.
- The repository contains reproducible code and documentation.
- Completed notebooks run successfully from restarted kernels.
- The final presentation clearly explains the research question, methods, findings, limitations, and significance.

---

## 24. Project Status Summary

**Current phase:** January 2025 pre-modeling completion gate.

**Verified checkpoint:** Notebook 02 has two 744-row processed electricity tables and a 4,464-row NYISO forecast-vintage table. Notebook 04 Steps 1–7 and calendar validation are complete. The reusable January preprocessing path has been reconciled and tested against Notebook 02's canonical schema and weather policies.

**Current working implementation:** `notebooks/04_feature_engineering.ipynb` and `src/electricity_forecasting/feature_engineering.py`.

**Exact next task:** Task 3 — forecast-origin-aware historical features.

**Primary limitations:** NYISO availability uses a ZIP timestamp proxy; PJM lacks a verified comparable load-forecast vintage series; forecast-origin-aware lags are not yet complete; and NOAA raw timestamp handling needs DST validation before the multi-year expansion.

**Pre-modeling exit:** all seven authoritative tasks pass, January modeling-ready tables are validated, notebooks run fresh, tests/Ruff pass, and documentation matches the implementation.

---

## 25. Optional Interactive Results Dashboard

If the forecasting analysis, final paper, and presentation remain on schedule, the project will include a Streamlit dashboard for communicating the results.

Potential dashboard features include:

- PJM PSEG and NYISO Hudson Valley market selection
- Historical day-ahead price exploration
- Actual-versus-predicted hourly price charts
- Model comparisons using MAE and RMSE
- Forecast-error analysis by hour, weekday, and season
- Negative-price and unusually high-price analysis
- Feature-importance visualizations
- Downloadable prediction and evaluation tables

The dashboard will read saved predictions, metrics, and model outputs. It will not retrain models whenever a user opens the application.

The dashboard is a secondary project deliverable. Completion of the validated forecasting analysis, academic paper, and presentation takes priority.
