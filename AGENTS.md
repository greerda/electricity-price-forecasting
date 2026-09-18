# Project overview

This repository contains a graduate data-science capstone comparing the incremental predictive value of day-ahead load forecasts for hourly day-ahead electricity-price forecasting in:

- PJM PSEG pricing zone; and
- NYISO Hudson Valley Zone G.

The project must remain achievable within the DATA 698 capstone schedule, academically defensible, reproducible, and suitable for presentation to professors and prospective employers.

# Current execution checkpoint

The project is currently **Conditional GO** for the revised load-forecast-centered research question.

The authoritative current state lives in:

- `docs/current_status.md`
- `docs/full_go_checkpoint.md`

Do not treat the revised research design as fully committed until every Full-GO criterion passes.

Current execution order:

1. implement PJM January 2025 `load_frcstd_hist` / `MIDATL` latest-eligible forecast selection;
2. regenerate NYISO January 2025 forecast timing using P-7 `Last Updated`;
3. test representative 2020, 2024, and DST historical periods for both markets;
4. calculate valid pre-cutoff forecast coverage and document gaps;
5. record Full GO, Conditional GO, or No-GO; and
6. only after Full GO, begin bulk 2020–2024 acquisition and freeze the feature-ablation design.

Do not skip directly to model tuning before this checkpoint is complete.

# Research question

> How much does adding day-ahead load forecasts improve hourly day-ahead electricity-price prediction accuracy in PJM PSEG and NYISO Hudson Valley, and is the improvement larger in one market than the other?

# Supplementary question

> Does the day-ahead load forecast contain more unique predictive information about electricity prices in the market where the larger improvement occurs?

The supplementary question is a predictive/statistical explanation, not a broad causal market-design claim.

# Full-GO experimental design

After the data gate passes, compare the same model under two feature sets.

Base feature set:

```text
calendar features
+ cutoff-safe historical price features
```

Augmented feature set:

```text
calendar features
+ cutoff-safe historical price features
+ eligible day-ahead load forecast
```

Keep the model family, chronological split, preprocessing, random seed, and metrics fixed when comparing the base and augmented feature sets.

Primary models:

- persistence baseline;
- Ridge or Elastic Net regression;
- Random Forest; and
- XGBoost or `HistGradientBoostingRegressor`.

PyTorch and pretrained time-series models are optional extensions only after the core analysis is complete.

# Unit of analysis and target

Unit: one market-location-hour.

Targets:

- PJM PSEG: complete hourly day-ahead LMP, canonical project name `day_ahead_price_usd_mwh`;
- NYISO Hudson Valley: complete hourly day-ahead LBMP, canonical project name `day_ahead_price_usd_mwh`.

Locations:

- PJM PSEG pnode `51301`, paired metered-load area `PS`;
- NYISO `HUD VL`, PTID `61758`.

PJM MIDATL forecast load is a regional proxy for PSEG and must never be described as a PSEG-specific forecast.

# Study period

January 2025 is a feasibility and pipeline-development sample only.

Planned primary study period: January 1, 2020 through December 31, 2024, subject to passing the Full-GO coverage and continuity checks.

# Forecast cutoffs

Every operational predictor must be available strictly before the applicable cutoff:

- PJM: D−1 11:00 `America/New_York`;
- NYISO: D−1 05:00 `America/New_York`.

A predictor at exactly the cutoff is excluded under the conservative project rule unless stronger authoritative evidence justifies otherwise.

# PJM historical load forecast rule

Use:

- feed: `load_frcstd_hist`;
- forecast area: `MIDATL`;
- availability: `evaluated_at_ept` / `evaluated_at_utc`;
- target hour: `forecast_hour_beginning_ept` / `forecast_hour_beginning_utc`;
- value: `forecast_load_mw`.

For each target hour, select the latest MIDATL snapshot satisfying:

```text
evaluated_at_ept < prediction_cutoff
```

PJM confirmed `evaluated_at_ept` as the generated-and-available timestamp. Require no duplicate selected target hours and preserve all audit fields.

# NYISO historical load forecast rule

Use P-7 ISO Load Forecast / `isolf` data for Hudson Valley.

Use:

```text
availability_basis = "p7_last_updated"
availability_is_proxy = True
```

P-7 public-report `Last Updated` is the best available public-source evidence of forecast availability, but its formal publication semantics remain inferred rather than operator-confirmed. ZIP-entry timestamps remain secondary provenance.

For each target hour:

1. preserve every P-7 vintage whose multi-day horizon contains the target hour;
2. construct the D−1 05:00 EPT cutoff;
3. reject vintages with `forecast_available_at >= prediction_cutoff`; and
4. select the latest eligible earlier vintage.

# Full-GO coverage gate

For representative 2020, 2024, and DST sample periods in both markets, measure the percentage of target hours with a defensible pre-cutoff load forecast.

The gate passes only if coverage is sufficiently high for the comparison and all material gaps are understood and documented.

Never:

- use a post-cutoff forecast to fill a gap;
- silently impute a missing forecast vintage;
- infer an availability timestamp without documenting the evidence basis; or
- declare Full GO before historical continuity and coverage are measured.

# Leakage prevention

Never use:

- future target values;
- same-hour actual load in the strict operational model;
- target-hour observed weather in the strict operational model;
- target components as predictors of the total target;
- post-cutoff forecast vintages;
- preprocessing fitted on validation/test data; or
- random train/test splitting for the primary evaluation.

Historical price lags and rolling features must pass forecast-origin availability checks, not merely chronological row-order checks.

# Evaluation

Use chronological train/validation/test periods. Candidate full-period design:

- train: 2020–2022;
- validation/tuning: 2023;
- final untouched test: 2024.

Primary metrics:

- MAE;
- RMSE;
- percentage improvement in MAE/RMSE from base to augmented features.

R² may support interpretation. MAPE is not primary because prices may be zero or negative.

For the supplementary question, approved diagnostics include:

- base-versus-augmented error reduction;
- baseline residual association with `load_forecast_mw`;
- permutation importance; and
- out-of-sample R² change where useful.

Do not attribute differences to “market design” unless a specific measurable mechanism is separately demonstrated.

# Timekeeping and DST

Use `timestamp_utc` as the canonical unique key for joins, ordering, duplicate detection, splitting, and modeling. Retain timezone-aware `timestamp_local` for interpretation, calendar features, and cutoff construction.

NYISO documentation:

- TB-064: fall-back 25-hour day, repeated second 01:00, `HB25` in MIS Upload/Download;
- TB-088: spring-forward 23-hour day, no `HB02`.

Actual 2020–2024 source files must still be regression-tested. PJM Data Miner timestamp behavior must also be tested empirically across DST.

# Required final-study data

Required:

- PJM PSEG day-ahead price history 2020–2024;
- NYISO Hudson Valley day-ahead LBMP history 2020–2024;
- PJM MIDATL `load_frcstd_hist` history with `evaluated_at_*`;
- NYISO P-7 Hudson Valley forecast history with usable `Last Updated` metadata;
- prior history needed to construct safe price features; and
- calendar variables.

Useful but not required for the revised primary question:

- actual load;
- NOAA observed weather;
- archived weather forecasts;
- natural-gas prices;
- neural networks or pretrained forecasting models.

# Student background and teaching approach

The student is an experienced C#/.NET and SQL developer developing proficiency in Python, pandas, NumPy, scikit-learn, statistical learning, time-series forecasting, testing, Jupyter notebooks, and reproducible data-science workflows.

Use C#, LINQ, SQL, relational-database, or strongly typed programming comparisons when they make unfamiliar Python or data-science concepts easier to understand.

Break work into small, testable tasks. Explain the data-science purpose before substantial implementation. Diagnose before fixing. Provide explicit verification. Never invent results, citations, source definitions, or conclusions.

# Textbook-guided methodology

Use these books as methodological guides when they are appropriate to the research question and valid time-series design:

1. *An Introduction to Statistical Learning with Applications in Python* (`ISLP`);
2. *Hands-On Machine Learning with Scikit-Learn and PyTorch* (`HOML`); and
3. *Forecasting: Principles and Practice, the Pythonic Way* (`FPPPy`).

Consult `docs/textbook_notes/` for project-specific notes, `docs/literature_source_register.md` for the master source inventory and FPPPy chapter-to-capstone checklist, and `reports/references.bib` for citation keys and bibliographic metadata.

Give priority to DATA 698 requirements, leakage-free time-series methodology, and the documented project design over generic textbook examples. Paraphrase sources, verify chapter claims, and never fabricate quotations, page numbers, or citations.

# Data and code rules

- Raw files under `data/raw/` are immutable.
- Intermediate data go under `data/interim/`.
- Validated analysis-ready data go under `data/processed/`.
- Figures go under `reports/figures/`.
- Tables go under `reports/tables/`.
- Models, metrics, and predictions go under `outputs/`.
- Stable reusable logic belongs in `src/electricity_forecasting/`.
- Use Python 3.12 and repository-relative paths.
- Use pytest and Ruff before major checkpoints.

# Documentation governance

After meaningful work:

- update `docs/current_status.md` with the verified state and exact next action;
- update `docs/full_go_checkpoint.md` when a Full-GO criterion is completed or fails;
- update `docs/decisions.md` for new methodological decisions;
- update `docs/methodology_decisions.md` for governing rules;
- update `docs/data_dictionary.md` for schema/field-role changes;
- update `docs/data_source_register.md` for source/provenance changes;
- update `docs/notebook_pipeline_map.md` when the high-level workflow changes;
- update `docs/project_plan.md` when scope, milestones, or final design changes; and
- update `docs/learning_log.md` for meaningful lessons and reproduced verification.

Do not modify documentation merely to restate unchanged information.

# Git workflow

Work in small, meaningful units. Run tests when code changes. Review changed files. Do not commit credentials, private correspondence, notebook checkpoints, caches, or prohibited raw data. Do not push, merge, delete branches, or rewrite history without explicit student approval.
