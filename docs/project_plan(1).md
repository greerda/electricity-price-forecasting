# Electricity Price Forecasting Capstone — Project Plan

**Last updated:** August 21, 2026  
**Current phase:** January 2025 leakage-safe feature engineering  
**Current task:** Complete feature-role classification after the NYISO forecast merge in `notebooks/04_feature_engineering.ipynb`

## How to use this document

This file is the authoritative academic and technical roadmap for the capstone. It records scope, methodology, milestones, risks, dependencies, future actions, schedule, and completion criteria.

- Use `current_status.md` for the short, frequently updated IDE-agent handoff.
- Use `docs/methodology_decisions.md` for the detailed rationale and status of methodological decisions.
- Use `docs/data_source_register.md` for dataset, documentation, correspondence, and source limitations.
- Use `docs/data_dictionary.md` for field definitions, units, time conventions, and modeling roles.
- Use `docs/notebook_pipeline_map.md` for the high-level notebook and source-code flow.
- Use `AGENTS.md` for stable instructions governing coding-agent behavior.
- Update this plan whenever a milestone, dependency, source decision, study-period decision, or scope item changes.

## 1. Project overview

This graduate data-science capstone will develop, evaluate, and compare models for forecasting hourly day-ahead electricity prices in two organized wholesale electricity markets:

- PJM PSEG pricing zone; and
- NYISO Hudson Valley Zone G.

The project compares statistical baselines, regularized regression, Random Forest, and gradient-boosted tree models using predictors that can be demonstrated to have been available before the applicable market cutoff.

January 2025 is the feasibility and pipeline-development sample. The planned primary study period is January 1, 2020 through December 31, 2024, subject to the future validation actions in this plan.

## 2. Working research question

> How accurately can statistical and machine-learning models forecast hourly day-ahead electricity prices, and how does predictive performance differ between PJM PSEG and NYISO Hudson Valley Zone G?

The research question does not need to change because of the PJM, NYISO, or NOAA responses.

## 3. Supporting research questions

1. Which forecasting model produces the lowest chronological out-of-sample error in each market?
2. Does the best-performing model differ between PJM and NYISO?
3. How does forecasting accuracy vary by hour, weekday, season, price level, and market condition?
4. How well do relatively simple baselines and regularized linear models perform compared with tree-based models?
5. How do models perform during negative-price and unusually high-price periods?
6. How do differences in forecast areas, data availability, and market design affect comparison of the two markets?
7. How much performance changes when only operationally available predictors are used rather than same-hour observed variables?

## 4. Academic and practical significance

Day-ahead electricity prices affect generators, utilities, energy traders, large consumers, and market operators. Prices are difficult to predict because they depend on time-sensitive demand, weather, generation availability, congestion, fuel costs, transmission constraints, and market-specific rules.

Comparing PJM and NYISO demonstrates practical data-science skills in:

- data acquisition and source validation;
- time-series cleaning and quality control;
- timestamp and timezone management;
- forecast-vintage reconstruction;
- exploratory data analysis;
- leakage-safe feature engineering;
- chronological validation;
- regression and tree-based modeling;
- cross-market comparison;
- reproducible research;
- technical documentation; and
- communication through a final paper, presentation, and optional dashboard.

## 5. Project scope

### 5.1 Markets, locations, and targets

| Market | Selected location | Confirmed identifier | Price target | Unit |
|---|---|---|---|---|
| PJM | PSEG zone | Pnode `51301`; load area `PS` | `total_lmp_da` | `$/MWh` |
| NYISO | Hudson Valley Zone G | `HUD VL`, PTID `61758` | `LBMP ($/MWHr)` | `$/MWh` |

PJM confirmed the PSEG/PS pairing. NYISO confirmed PTID `61758` for both Hudson Valley zonal day-ahead LBMP and actual zonal load.

`total_lmp_da` and NYISO LBMP are treated as complete price targets. Component fields are retained for audit and explanation but are not added to the already complete target.

### 5.2 Unit of analysis

One target delivery hour per market.

PJM and NYISO will be modeled separately. Performance will then be compared using consistent metrics and aligned evaluation periods where possible.

### 5.3 Feasibility period

January 1–31, 2025.

Each market contains 744 unique hourly target observations during the pilot period.

### 5.4 Planned primary study period

January 1, 2020 through December 31, 2024.

This period is the working final scope. Before bulk modeling, the pipeline must validate:

- PSEG node `51301` continuity;
- `PS` load-area continuity;
- PJM MIDATL historical forecast coverage;
- NYISO PTID `61758` continuity;
- NYISO forecast-vintage availability timestamps;
- daylight-saving transition behavior;
- NOAA station histories;
- annual feed schemas, units, revisions, and missingness; and
- possible structural breaks, including PJM fast-start pricing effective September 1, 2021.

### 5.5 Forecast origins

The project predicts all 24 hours of the next operating day using only information available before the applicable market cutoff.

| Market | Market cutoff | Project eligibility rule | Status |
|---|---|---|---|
| PJM | 11:00 a.m. EPT on the day before delivery | Availability strictly before 11:00 a.m. | Adopted; PJM implementation pending |
| NYISO | 5:00 a.m. EPT on the day before delivery | Availability strictly before 5:00 a.m. | Adopted for the January pipeline |

The strict “before” rule is deliberately conservative. A source timestamped exactly at the cutoff is excluded unless future authoritative evidence proves it was available beforehand.

### 5.6 Out-of-scope primary items

The primary capstone will not require:

- real-time streaming infrastructure;
- causal inference;
- retrieval-augmented generation;
- large language models;
- multiple pricing locations per market;
- extensive cloud production architecture;
- neural networks such as LSTM or GRU; or
- price-spike classification.

These may be discussed as future extensions after the academic requirements are complete.

## 6. Data sources and current determinations

Detailed source metadata belong in `docs/data_source_register.md`.

| Data family | Current source | Current determination | Remaining action |
|---|---|---|---|
| PJM price | `da_hrl_lmps` January pilot | PSEG node `51301`; `total_lmp_da` is the target | Decide whether final history uses or is reconciled against `rt_da_monthly_lmps` |
| PJM actual load | `hrl_load_metered` | `PS` pairs with PSEG; target-hour actual load is EDA-only | Validate all study years and use only safe lags if modeled |
| PJM load forecast | `load_frcstd_hist` | Use `MIDATL`; six-hour snapshots; evaluated time is generated-and-available time | Implement strict pre-11:00 a.m. latest-vintage selection |
| NYISO price | MIS day-ahead LBMP | Use `HUD VL`, PTID `61758` | Acquire and validate 2020–2024 files |
| NYISO actual load | Integrated zonal load | Use `HUD VL`, PTID `61758`; target-hour actual load is EDA-only | Validate all study years and safe-lag rules |
| NYISO load forecast | ISO Load Forecast archive and Custom Reports | January selection implemented; availability uses ZIP metadata proxy | Validate authoritative publication time before final use |
| Newark weather | NOAA LCDv2 station `USW00014734` | Appropriate point observation with geographic limitation | Acquire 2020–2024; audit HOMR and apply fixed-standard-time rule |
| Stewart weather | NOAA LCDv2 station `USW00014714` | Appropriate point observation with geographic limitation | Acquire 2020–2024; audit HOMR and physical outliers |
| Archived weather forecast | NOAA/NWS SRRS, NOAAPort, FPUS5, FXUS6 candidates | No structured hourly modeling source approved | Investigate reproducible issuance/valid-time extraction or exclude from core model |
| Calendar variables | Derived | Approved | Document holiday calendar and cyclical encodings |
| Historical price features | Derived from target feeds | Approved in principle | Implement forecast-origin-aware lags and rolling windows |
| Natural-gas price | Undetermined | Optional | Include only if timing, coverage, and effort are acceptable |

## 7. Current repository structure

Expected major files include:

```text
AGENTS.md
PROJECT_PLAN.md
current_status.md
pyproject.toml

notebooks/
├── 01_data_inventory.ipynb
├── 02_data_cleaning.ipynb
├── 03_exploratory_data_analysis.ipynb
├── 04_feature_engineering.ipynb
├── 05_baseline_models.ipynb
└── 06_model_comparison.ipynb

src/electricity_forecasting/
├── __init__.py
├── data_processing.py
└── feature_engineering.py

docs/
├── data_dictionary.md
├── data_source_register.md
├── methodology_decisions.md
├── notebook_pipeline_map.md
├── learning_log.md
└── textbook_notes/

data/
├── raw/
├── interim/
└── processed/

outputs/
├── metrics/
├── models/
└── predictions/

reports/
├── capstone.qmd
├── figures/
├── tables/
└── references.bib
```

Private correspondence and restricted reference materials must remain outside the public repository or in a gitignored private reference location.

## 8. January 2025 feasibility results

### 8.1 Electricity validation

| Validation check | PJM | NYISO |
|---|---:|---:|
| Hourly target rows | 744 | 744 |
| Unique hourly timestamps | Yes | Yes |
| Missing price values | 0 | 0 |
| Missing actual-load values | 0 | 0 |
| Matched price/load rows | 744 | 744 |

The January electricity tables are suitable for pipeline development, EDA, feature-engineering tests, and baseline-code tests. They are not the final modeling datasets.

### 8.2 Weather validation

Earlier January processing produced:

| Validation check | Newark | Stewart |
|---|---:|---:|
| Output hourly rows | 744 | 744 |
| Incomplete hours | 3 | 7 |
| Clearly corrupted observations rejected | 0 | 4 |
| Future-looking interpolation | No | No |

The full NOAA review added several requirements:

- filter the station-year file by timestamp rather than filename;
- use fixed Local Standard Time for raw `DATE` conversion;
- use `FM-15` as the primary routine source;
- exclude daily/monthly summaries and `FM-12` from the primary series;
- use `FM-16` only as a documented fallback;
- preserve quality indicators and raw `REM` text;
- distinguish blank, zero, trace, suspect, and erroneous values; and
- apply project-level physical plausibility checks.

**Future action:** Re-run the January weather cleaning after confirming that every requirement above is implemented consistently in `data_processing.py` and the notebook.

### 8.3 NYISO load-forecast feasibility

- 4,464 forecast-vintage/target-hour rows were retained.
- The vintages cover 744 unique January target hours.
- A 5:00 a.m. day-before-delivery cutoff was constructed.
- Post-cutoff vintages were excluded.
- Exactly one latest eligible forecast was selected per target hour.
- The selected forecasts merged one-to-one with the 744-row NYISO electricity table.
- Forecast timing and provenance fields were retained.
- The availability timestamp is currently a ZIP-entry last-modified proxy.

The workflow proves that the vintage-selection pipeline works. It does not yet prove that the proxy represents the original public availability time for the full study period.

The NYISO training timeline places the NYISO Load Forecast posting after the 5:00 a.m. Day-Ahead Market close. The operational experiment must therefore use an earlier version demonstrably published before 5:00 a.m.; a later same-day posting is ineligible even if it forecasts the correct delivery hours.

## 9. Methodological decisions

The full rationale belongs in `docs/methodology_decisions.md`. The controlling decisions are:

- Use UTC as the canonical join and modeling key.
- Retain timezone-aware market-local timestamps for interpretation and calendar features.
- Treat raw NOAA LCDv2 timestamps as fixed Local Standard Time before UTC conversion.
- Use market-specific day-ahead forecast origins.
- Exclude any predictor not demonstrably available before its market cutoff.
- Use MIDATL as a PJM regional load-forecast proxy, not as PSEG-specific load.
- Treat the NYISO archive last-modified timestamp as a proxy pending validation.
- Exclude same-hour actual load from operational models.
- Exclude same-hour observed weather from operational models.
- Retain actual load and observed weather for EDA or explicitly non-operational analyses.
- Shift before calculating rolling features.
- Do not randomly shuffle time-series observations.
- Fit preprocessing on training data only.
- Preserve an untouched final test period.
- Retain negative prices and genuine price spikes.
- Keep raw datasets immutable.
- Regenerate processed data reproducibly.
- Keep private correspondence out of the public repository.

## 10. Predictor status

| Predictor | Status | Market-specific rule | Future action |
|---|---|---|---|
| Hour, weekday, weekend, month, season | Approved | Known in advance | Implement and test cyclical encodings |
| Holiday indicator | Approved in principle | Known in advance | Select and cite a holiday calendar |
| Historical day-ahead price lags | Approved in principle | Must be available for all 24 forecasted hours | Implement forecast-origin-aware lags |
| Backward-looking price windows | Approved in principle | Shift before rolling | Add automated leakage tests |
| NYISO `load_forecast_mw` | Conditional pilot predictor | Latest eligible vintage strictly before 5:00 a.m. | Validate authoritative availability timestamp |
| PJM MIDATL forecast | Approved candidate; pending implementation | Latest six-hour snapshot strictly before 11:00 a.m. | Build and validate the PJM pipeline |
| Same-hour actual load | Excluded operationally | EDA or safe lag only | Document any lag before use |
| Same-hour observed weather | Excluded operationally | EDA or upper-bound model only | Keep out of the core predictor list |
| Lagged observed weather | Conditional | Lag must guarantee pre-cutoff availability | Define and test exact lag |
| Archived weather forecast | Under investigation | Must preserve issue time, valid time, and vintage | Decide feasibility before final feature approval |
| Natural-gas price | Optional | Publication timing must be documented | Include only if scope permits |

## 11. Planned models

Primary comparison:

1. historical-average and/or persistence baseline;
2. regularized linear regression, such as Ridge or Elastic Net;
3. Random Forest regression; and
4. gradient-boosted tree regression, such as XGBoost.

A simple unregularized linear regression may be included as an interpretable reference.

Neural networks are not required to answer the research question and remain outside the primary scope.

## 12. Feature-engineering plan

### 12.1 Price-history features

- same-hour previous-day price;
- same-hour previous-week price;
- earlier prices demonstrably available at the forecast origin;
- shifted rolling mean, standard deviation, minimum, and maximum; and
- recent price-change indicators.

Every feature must document its source, lag, rolling window, forecast origin, and availability rule.

### 12.2 Calendar features

- target hour;
- weekday;
- weekend indicator;
- holiday indicator;
- month;
- season; and
- sine/cosine cyclical encodings.

### 12.3 Load features

- selected NYISO Hudson Valley historical forecast, conditional on timestamp validation;
- selected PJM MIDATL forecast;
- safe lagged actual-load features if justified; and
- forecast ramp or change indicators derived only from eligible forecasts.

### 12.4 Weather features

- archived temperature forecast if reproducibly available before cutoff;
- archived humidity or dew-point forecast if reproducibly available;
- archived wind forecast if reproducibly available;
- heating/cooling transformations derived only from safe inputs; and
- sufficiently lagged observations if archived forecasts are not feasible.

Same-hour observed weather will not be part of the operational core feature set.

### 12.5 Audit-only fields

Cutoff timestamps, forecast availability timestamps, lead times, source archives, source files, revision numbers, proxy indicators, and quality flags are retained for validation but excluded from the default predictor matrix.

## 13. Validation and evaluation strategy

### 13.1 Chronological splitting

Candidate final split:

- training: 2020–2022;
- validation and tuning: 2023; and
- final untouched test: 2024.

The exact split will be finalized after source coverage and structural changes are validated.

Random train/test splitting is prohibited.

### 13.2 Cross-validation

Use rolling-origin or expanding-window validation. Every training window must occur before its corresponding validation window.

### 13.3 Preprocessing controls

- Fit imputation on training data only.
- Fit scaling on training data only.
- Fit encoding and feature selection on training data only.
- Use reproducible pipelines where practical.
- Never backward-fill missing time-series values.
- Use forward fill only within a documented maximum gap and only when the prior value was operationally available.

### 13.4 Metrics

Primary metrics:

- Mean Absolute Error; and
- Root Mean Squared Error.

MAPE is not primary because electricity prices may be zero or negative.

### 13.5 Secondary analyses

Evaluate errors by:

- market;
- hour;
- weekday versus weekend;
- month or season;
- normal versus high-price periods;
- negative-price periods;
- before and after material structural changes; and
- operational versus explanatory feature sets if both are implemented.

## 14. Completed work

- [x] Selected PJM and NYISO.
- [x] Selected PSEG and Hudson Valley Zone G.
- [x] Defined the research question and unit of analysis.
- [x] Selected January 2025 as the feasibility period.
- [x] Identified 2020–2024 as the planned primary period.
- [x] Downloaded the January electricity, load, and weather files.
- [x] Created notebooks 01–04.
- [x] Validated 744 unique January target hours per market.
- [x] Cleaned and merged January price and actual load.
- [x] Implemented reusable data-processing functions.
- [x] Added market local/UTC timestamp handling.
- [x] Added NOAA cleaning and validation logic.
- [x] Preserved missing, rejected, and flagged weather observations.
- [x] Exported the two January processed electricity datasets.
- [x] Received and reviewed the NOAA response and LCDv2 documentation.
- [x] Received and reviewed the NYISO response and Energy Marketplace training.
- [x] Received and reviewed PJM Case `00334055`.
- [x] Confirmed the PSEG/PS and HUD VL/PTID `61758` identifiers.
- [x] Defined the 5:00 a.m. NYISO cutoff.
- [x] Defined the 11:00 a.m. PJM cutoff.
- [x] Identified PJM `load_frcstd_hist` and MIDATL as the public historical forecast route.
- [x] Built the January NYISO forecast-vintage table.
- [x] Selected and merged one eligible NYISO forecast per target hour.
- [x] Preserved forecast timing and provenance audit fields.
- [x] Verified 3 tests and Ruff checks for `src` and `tests`.
- [ ] Verify whether all planned EDA requirements in Notebook 03 are complete and reproducible.
- [ ] Complete the feature-role classification in Notebook 04.
- [ ] Validate NYISO availability timestamps.
- [ ] Implement PJM historical load-forecast selection.
- [ ] Acquire and validate the full 2020–2024 datasets.
- [ ] Build final analysis-ready datasets.
- [ ] Train and compare models.
- [ ] Complete the paper and presentation.

## 15. Current milestone — feature-role classification

Current notebook:

```text
notebooks/04_feature_engineering.ipynb
```

The NYISO forecast-vintage construction, cutoff filtering, selection, and merge are complete through Step 6.

### 15.1 Immediate work

1. Add a Markdown cell classifying columns as target, conditional predictor, audit-only, or excluded.
2. Define:

   ```python
   target_column = "day_ahead_price_usd_mwh"
   candidate_feature_columns = ["load_forecast_mw"]
   ```

3. Define the full `forecast_audit_columns` list.
4. Print and validate each role group.
5. State that NYISO availability uses a proxy and is not yet approved for final operational modeling.
6. Run the notebook using `Python 3.12 (electricity-forecasting)`.
7. Preserve all unrelated existing work.

### 15.2 Milestone constraints

- Do not create a final modeling CSV yet.
- Do not add same-hour actual load as an operational predictor.
- Do not add same-hour observed weather as an operational predictor.
- Do not put audit fields into the default predictor list.
- Do not begin final model training.
- Do not remove forecast vintages or provenance fields needed for audit.

### 15.3 Milestone completion criteria

- Every available column has a documented role.
- The target is not present in the candidate predictor list.
- Audit-only fields are preserved but excluded from modeling.
- Excluded fields are explicit.
- The NYISO availability limitation is stated in Markdown.
- Cells run without error from the active kernel.

## 16. Resolved findings and remaining uncertainties

### 16.1 Resolved

| Topic | Resolution | Evidence type |
|---|---|---|
| PJM price/load pairing | PSEG node `51301` with `PS` | Direct PJM response |
| PJM historical forecast source | `load_frcstd_hist` | Direct PJM response and feed definition |
| PJM forecast area | MIDATL; no PSEG-only historical detail | Direct PJM response |
| PJM evaluated time | Forecast generated and made available | Direct PJM response |
| PJM snapshot retention | Every six hours; not every live revision | Direct PJM response |
| PJM forecast cutoff | Conditions as of 11:00 a.m. EPT; project uses strict pre-cutoff rule | PJM response and market documentation |
| NYISO identifier | `HUD VL`, PTID `61758` for price and actual load | Direct NYISO response |
| NYISO cutoff | 5:00 a.m. EPT day before dispatch | NYISO training timeline |
| NOAA station identifiers | Newark `USW00014734`; Stewart `USW00014714` | Direct NOAA response |
| NOAA units | SI units | LCDv2 documentation |
| NOAA raw timestamp | Fixed Local Standard Time | LCDv2 documentation |
| Blank precipitation | Missing/unreported, not zero | Direct NOAA response and documentation |

### 16.2 Remaining uncertainties and future actions

| Uncertainty | Why it matters | Required future action | Decision trigger |
|---|---|---|---|
| NYISO archive timestamp is a proxy | Could misclassify post-cutoff information as eligible | Validate against an authoritative publication timestamp or exclude the feature | Before final NYISO modeling table |
| NYISO load forecast may be posted after market close | The correct target hours can still come from an operationally unavailable forecast | Verify that each selected vintage was actually public before 5:00 a.m.; otherwise use an earlier vintage or omit the feature | Before final NYISO predictor approval |
| Structured archived weather forecast not selected | Same-hour observations would leak future information | Test SRRS/NOAAPort/IEM feasibility or restrict weather to safe lags | Before approving weather predictors |
| NYISO DST implementation not coded from TB-064 | Could create missing or duplicated local hours | Retrieve bulletin, implement, and test both transitions | Before multiyear NYISO processing |
| Final PJM price feed not selected | Different feed versions could change the target | Compare `da_hrl_lmps` with `rt_da_monthly_lmps` | Before PJM bulk download |
| Full-period identifiers not audited | Identifier changes could invalidate joins | Check effective dates and annual coverage | Before each annual merge |
| NOAA station histories not audited | Equipment or location changes could create breaks | Review HOMR for both stations | Before full weather modeling |
| PJM fast-start pricing changed in 2021 | Possible price-series structural break | Add indicator, sensitivity test, or limitation discussion | During EDA/model diagnostics |
| Notebook 03 completion not independently verified in current status | Project-plan milestone may be overstated | Restart and run Notebook 03; check deliverables | Before declaring EDA complete |

## 17. Risk and future-change register

| Risk | Effect | Current mitigation | Future action or change trigger |
|---|---|---|---|
| NYISO forecast availability is misdated | Leakage and inflated performance | Proxy flag and strict cutoff | Replace proxy when authoritative timestamps are found; rebuild features and models |
| MIDATL is broader than PSEG | Market-feature mismatch | Label as a regional proxy and model markets separately | Test RTO forecast or no-load-forecast sensitivity model |
| Same-hour actual load leaks target information | Unrealistic accuracy | Exclude operationally | Reconsider only if a safe lag is explicitly defined |
| Observed target-hour weather leaks future information | Unrealistic accuracy | EDA/upper-bound only | Replace with archived forecast or safe lag |
| NOAA parsed values are physically invalid | Distorted coefficients and tree splits | QC preservation and physical rejection | Expand validation if new anomalies appear |
| NOAA fixed-standard-time timestamps are localized incorrectly | One-hour summer misalignment | Localize raw `DATE` as UTC−05:00 | Add transition-date regression tests |
| DST creates 23/25-hour local days | Duplicate or missing joins | Use UTC canonical key | Implement market-specific transition tests |
| Source definitions change during 2020–2024 | Invalid cross-year joins | Annual source audit | Version transformation rules by effective date |
| Price methodology changes | Structural break | Retain all observations and document changes | Add regime indicator or sensitivity analysis |
| Forecast snapshots are incomplete | Missing features or biased sample | Preserve all vintages and missingness | Compare included versus excluded hours |
| Model tuning becomes excessive | Delayed writing and completion | Bounded searches and fixed validation design | Stop tuning when predeclared budget is reached |
| Scope expands beyond the course | Threatens completion | Two markets, two locations, four model families | Defer dashboard/cloud/streaming enhancements |
| Private correspondence is committed publicly | Privacy or confidentiality problem | Keep private sources outside Git | Audit staged files before every commit |
| Documentation falls out of sync | Reproducibility failure | Update related Markdown files together | Treat schema/source/method changes as documentation-change triggers |

## 18. Thirteen-week schedule

| Week | Primary objective | Deliverable |
|---|---|---|
| 1 | Finalize question and scope | Documented question, locations, target, exclusions |
| 2 | Validate availability | Data inventory and source documentation |
| 3 | Build January pipeline | Reproducible cleaning and validation |
| 4 | Complete preliminary EDA | Executed EDA notebook, figures, tables, findings |
| 5 | Review literature and prepare proposal | Proposal and preliminary bibliography |
| 6 | Acquire full historical data | Documented 2020–2024 raw sources |
| 7 | Clean, align, and engineer features | Validated analysis-ready datasets |
| 8 | Draft major paper sections | Midterm draft |
| 9 | Build baselines and regularized models | Baseline and linear-model results |
| 10 | Build tree-based models | Random Forest and gradient-boosting results |
| 11 | Tune, evaluate, and compare | Final metrics and diagnostic figures |
| 12 | Write results and conclusions | Complete final-paper draft |
| 13 | Revise and present | Final paper, repository, and presentation |

Course deliverables remain aligned with the DATA 698 syllabus, including the research proposal, midterm draft, final paper, and final presentation. Exact dates and formatting must be checked against the instructor's current guidance.

## 19. Literature-review plan

The literature review will address:

- day-ahead electricity-price forecasting;
- PJM and NYISO market characteristics;
- statistical and machine-learning electricity-price models;
- regularized regression;
- Random Forest and gradient boosting;
- negative prices and price spikes;
- load and weather predictors;
- forecast-vintage data and data leakage;
- chronological validation;
- structural breaks in electricity markets; and
- cross-market model comparisons.

Primary scholarly sources should be peer-reviewed articles and appropriate conference papers. PJM, NYISO, NOAA, and software documentation support the data and methodology sections rather than replacing the scholarly literature review.

## 20. Reproducibility and repository standards

- Run commands from the repository root.
- Use repository-relative paths.
- Use the active Python 3.12 project environment and registered kernel.
- Keep raw data immutable.
- Store temporary or multi-vintage tables under `data/interim/`.
- Store analysis-ready tables under `data/processed/`.
- Store models, predictions, and metrics under `outputs/`.
- Restart and run completed notebooks from top to bottom.
- Preserve source filenames, identifiers, versions, and provenance.
- Use UTC as the canonical key.
- Keep market-local time for interpretation.
- Keep raw NOAA fixed-standard-time semantics distinct from market-local time.
- Add automated tests for uniqueness, chronology, cutoff eligibility, rolling-window safety, and DST transitions.
- Review `git status` before staging.
- Stage only files belonging to the current change.
- Do not commit credentials, tokens, private correspondence, personal contact information, or restricted material.
- Update source, methodology, dictionary, pipeline, plan, and status documentation when a material decision changes.

## 21. Immediate next task

Continue `notebooks/04_feature_engineering.ipynb` after Step 6.

The next change must:

1. document the column-role classification;
2. define the price target;
3. retain `load_forecast_mw` as a conditional January candidate;
4. define all forecast audit columns;
5. explicitly exclude same-hour actual load and observed weather;
6. print and validate the role groups; and
7. preserve the NYISO availability-proxy limitation.

Do not create the final modeling dataset or begin final training as part of this task.

## 22. Near-term backlog

After the immediate task:

1. derive leakage-safe calendar features;
2. implement and test forecast-origin-aware price lags;
3. add automated feature-leakage tests;
4. implement PJM MIDATL historical forecast selection;
5. validate NYISO availability timestamps;
6. retrieve and implement TB-064 DST rules;
7. verify Notebook 03 completion;
8. decide the final PJM price feed;
9. audit identifiers and NOAA station histories;
10. acquire the full 2020–2024 data only after the above source rules are documented; and
11. freeze the approved predictor set before final modeling.

## 23. Definition of project completion

The project is complete when:

- the research question is precise and defensible;
- targets, locations, identifiers, and units are documented;
- market-specific forecast origins are explicit;
- every operational predictor is proven available before its cutoff;
- proxy availability timestamps are resolved or disclosed and excluded where necessary;
- the full historical data are reproducibly cleaned and validated;
- DST transitions are handled correctly;
- leakage-safe features are generated reproducibly;
- baselines, regularized regression, Random Forest, and boosted trees are trained;
- tuning and evaluation are chronological;
- the final test period remains untouched until final evaluation;
- MAE and RMSE are reported consistently;
- negative and high-price performance is documented;
- market-specific differences and limitations are explained;
- notebooks run successfully from restarted kernels;
- source, methodology, dictionary, and pipeline documentation match the implementation;
- the final paper satisfies the syllabus; and
- the presentation clearly explains methods, findings, limitations, and significance.

## 24. Project status summary

**Current phase:** January 2025 leakage-safe feature engineering.

**Completed milestone:** NYISO forecast-vintage construction, strict pre-5:00 a.m. filtering, latest-eligible selection, and one-to-one merge for all 744 January target hours.

**Current working notebook:** `notebooks/04_feature_engineering.ipynb`.

**Primary technical dependency:** Validation of an authoritative NYISO forecast-availability timestamp for final 2020–2024 use.

**Other required validations:** PJM MIDATL implementation, final PJM price-feed selection, NYISO TB-064 DST handling, NOAA station-history review, and full-period identifier continuity.

**Next deliverable:** A completed and tested column-role classification followed by leakage-safe calendar and historical features.

## 25. Optional interactive dashboard

If the forecasting analysis, final paper, and presentation remain on schedule, an optional Streamlit dashboard may provide:

- PJM PSEG and NYISO Hudson Valley selection;
- historical price exploration;
- actual-versus-predicted plots;
- MAE and RMSE comparisons;
- error analysis by time and price regime;
- negative and high-price analysis;
- feature-importance displays; and
- downloadable prediction and metric tables.

The dashboard will read saved outputs and will not retrain models when opened. It remains secondary to the validated analysis, paper, and presentation.
