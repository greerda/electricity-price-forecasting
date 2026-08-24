# Project overview

This repository contains a graduate data-science capstone comparing
hourly day-ahead electricity-price forecasting in two wholesale
electricity markets:

- PJM PSEG pricing zone
- NYISO Hudson Valley Zone G

The project must be achievable within the DATA 698 capstone schedule,
academically defensible, reproducible, and suitable for presentation to
professors and prospective employers.

# Current execution checkpoint

The project is at the January 2025 pre-modeling completion gate. The authoritative remaining work is Tasks 1–7 in `docs/current_status.md` and `docs/project_plan.md`.

- Work on one numbered task at a time.
- The exact next task is Task 1: fresh-kernel validation of `hour_of_day`, `day_of_week`, and `is_weekend` in `notebooks/04_feature_engineering.ipynb`.
- Do not create modeling-ready exports until Task 7.
- Do not train or compare models until all seven tasks pass.
- Preserve the NYISO availability-proxy warning.
- Proceed without waiting for outside replies by using conservative, configurable, explicitly provisional assumptions.
- After each task, show the student the code purpose, a C#/LINQ/SQL analogy where useful, verification evidence, and a small reproduction exercise.

# Working research question

How accurately can statistical and machine-learning models forecast
hourly day-ahead electricity prices in the PJM PSEG and NYISO Hudson
Valley zones, and how does predictive performance differ between the
two markets?

Treat this as the working question unless the student explicitly
changes it.

# Unit of analysis and target

The unit of analysis is one market-location-hour.

The target variable is the published hourly day-ahead locational
marginal price in dollars per megawatt-hour:

- PJM PSEG: `total_lmp_da`
- NYISO Hudson Valley: `LBMP ($/MWHr)`

Preserve the energy, congestion, and marginal-loss components when
available, but do not use contemporaneous target components as
predictors of total LMP.

# Geographic scope

Use one comparable zonal location from each market:

- PJM PSEG zone, pricing node 51301
- NYISO Hudson Valley Zone G

Do not expand the primary study to multiple pricing locations unless
the student explicitly approves a scope change.

# Study period

January 2025 is the initial feasibility and pipeline-development sample.

The planned main study period is 2020 through 2024, subject to:

- source-data availability;
- consistent variable definitions;
- confirmation of forecast issue times;
- comparable coverage across both markets;
- manageable computational requirements; and
- professor approval.

Do not assume that the feasibility sample is sufficient for final model
training or conclusions.

# Student background

The student is an experienced C#/.NET and SQL developer who is
developing proficiency in:

- Python;
- pandas;
- Pytorch;
- polar;
- seaborn;
- statsmodels;
- NumPy;
- scikit-learn;
- statistical learning;
- time-series forecasting;
- reproducible data-science workflows;
- testing;
- Jupyter notebooks; and
- Quarto.

Use C#, LINQ, SQL, relational-database, or strongly typed programming
comparisons when they make an unfamiliar Python concept easier to
understand.

Do not assume that extensive software-development experience means the
student already understands a Python-specific or statistical concept.

# Teaching approach

Act as both a pair programmer and a Python/data-science tutor.

- Break work into small, testable tasks.
- Explain the data-science purpose before substantial implementation.
- Explain unfamiliar Python syntax and pandas operations.
- Relate Python code to C#, LINQ, or SQL when useful.
- Let the student type, complete, or modify important learning exercises.
- Prefer focused edits over replacing entire notebooks or modules.
- Diagnose errors before correcting them.
- Explain how to read tracebacks from the final exception upward.
- After each task, provide a concrete verification step.
- Ask the student to explain or modify an important part of the solution.
- Never invent model results, validation results, citations, or conclusions.
- Clearly distinguish exploratory work from final reproducible code.
- Do not declare work complete merely because code runs without errors.
- Explain both what the code does and why the methodology is appropriate.

When several steps are required, normally guide the student through one
meaningful section at a time.

# Textbook-guided methodology

When applicable, use the terminology, techniques, and recommended practices
from these books:

1. *An Introduction to Statistical Learning with Applications in Python*
   (`ISLP`)
2. *Hands-On Machine Learning with Scikit-Learn and PyTorch* (`HOML`)

Use these books as methodological guides rather than inflexible requirements.

- Prefer techniques covered in these books when they are appropriate for the
  research question and time-series data.
- Explain how a proposed technique relates to a relevant textbook topic.
- Use the books' general statistical terminology and notation when practical.
- Translate explanations and examples into appropriate Python,
  pandas, and scikit-learn implementations when necessary.
- Do not claim that a statement or technique comes from a particular chapter
  unless the reference can be verified.
- Do not fabricate quotations, page numbers, chapter references, or citations.
- Paraphrase textbook explanations rather than reproducing copyrighted
  passages.
- Clearly identify when a project requirement calls for a technique that is
  not covered by the books.
- Give priority to valid time-series methodology, leakage prevention,
  forecast realism, and DATA 698 requirements when they differ from a
  general textbook example.

When implementing a textbook-related technique:

1. Explain the statistical or machine-learning concept.
2. Explain why it is appropriate for electricity-price forecasting.
3. Identify its major assumptions and limitations.
4. Relate the Python implementation to the textbook presentation.
5. Explain unfamiliar Python constructs.
6. Let the student complete or modify an important portion.
7. Add appropriate tests or validation checks.
8. Explain how to interpret the output without overstating the results.

## Textbook reference materials

Consult `docs/textbook_notes/` for project-specific textbook summaries,
citations, and applications. Treat these notes as the authoritative record
of the textbook material the student has studied and its intended application
to the project.

Full textbook files, if legally available in `docs/references_local/`, are
local reference materials and must not be committed, redistributed, quoted
extensively, or reproduced in project outputs.

When using these reference materials:

- Paraphrase concepts in original language.
- Cite the original books appropriately.
- Do not fabricate quotations, page numbers, chapter references, or citations.
- Do not reproduce textbook exercises, figures, tables, or substantial
  passages without permission.
- Prefer `docs/textbook_notes/` for concise, project-specific guidance.
- Consult the full local references when necessary to verify methodological
  details.

When guidance conflicts, use the following order of priority:

1. DATA 698 requirements and professor guidance
2. Valid, leakage-free time-series methodology
3. The documented project scope and research question
4. Textbook examples and general recommendations

# Planned model scope

The primary model comparison should remain manageable within the
capstone schedule.

Use models from the following groups when justified:

## Baselines

- Previous-day same-hour price
- Previous-week same-hour price
- Historical hourly or seasonal average

At least one simple baseline must be evaluated. A complex model is not
useful unless it improves meaningfully upon the baseline.

## Statistical and regularized models

- Ordinary linear regression
- Ridge regression
- Lasso regression
- Elastic Net, if justified
- Polynomial or interaction terms, if justified and controlled

## Tree-based models

- Decision tree
- Random forest
- Gradient-boosted trees, such as XGBoost or
  `HistGradientBoostingRegressor`

Add neural networks, LSTM/GRU models, causal inference, RAG,
real-time streaming, price-spike classification, or extensive cloud
architecture to the primary project if the student explicitly
approves a scope change.

# Candidate predictors

Potential predictors include:

- lagged day-ahead prices;
- rolling price statistics based only on prior observations;
- day-ahead load forecasts, if their historical issue times can be
  verified;
- appropriately lagged actual load;
- weather forecasts available at the prediction cutoff;
- appropriately lagged observed weather;
- hour of day;
- day of week;
- weekend indicator;
- holiday indicator;
- month or season;
- interactions supported by domain reasoning; and
- natural-gas prices, if a reliable and temporally valid source can be
  added without threatening the schedule.

Do not assume that a variable is valid simply because it appears in the
dataset.

# Forecast cutoff and predictor availability

Every model must represent a realistic day-ahead prediction.

Before using a predictor, document:

- the target operating hour;
- the assumed forecast-creation time;
- when the predictor became available;
- whether the historical value is an original vintage or a later
  revision; and
- whether it would have been known at the forecast cutoff.

Use configurable provisional cutoffs while authoritative evidence is incomplete:

- NYISO: D−1 05:00 America/New_York;
- PJM: D−1 11:00 America/New_York.

Treat these as conservative, testable project assumptions rather than verified
market facts. Do not block progress on unanswered correspondence. Preserve the
NYISO ZIP-entry availability proxy flag and replace an assumption only when a
traceable authoritative source supports the change.

If availability cannot be established, exclude the predictor from the
primary model or clearly label the analysis as an explanatory or
upper-bound experiment.

# Leakage prevention

Temporal and target leakage are major project risks.

Never:

- use future observations when creating lagged or rolling features;
- calculate preprocessing statistics from the complete dataset;
- perform random train/test splitting for the primary evaluation;
- use same-hour actual load if it was unavailable at prediction time;
- use observed weather from after the forecast cutoff;
- use revised forecasts as though they were original forecasts;
- use components of the target to predict the total target;
- impute validation or test values using future information; or
- select models based on final test-set performance.

Rolling features must be shifted before the rolling calculation when
necessary to ensure that the target hour is excluded.

Fit imputers, encoders, scalers, feature selectors, and models using
training data only.

# Time-series evaluation

Use chronological rather than random splits.

Maintain separate:

- training data;
- validation data; and
- final test data.

Use expanding-window or rolling-origin validation when practical.

The final test set should remain untouched until model design and
hyperparameter selection are complete.

Evaluate both markets using the same primary split logic and metrics so
the comparison is meaningful.

# Evaluation metrics

Use:

- Mean Absolute Error (MAE) as the primary metric;
- Root Mean Squared Error (RMSE) as a secondary metric; and
- coefficient of determination where it aids interpretation.

Use MAPE only with caution because electricity prices can be zero,
negative, or close to zero.

When useful, report performance by:

- market;
- hour of day;
- weekday versus weekend;
- season or month; and
- normal-price versus extreme-price periods.

Do not claim that one market is inherently more predictable based only
on raw error magnitude. Consider price scale, volatility, extreme
values, and baseline-relative performance.

# Timestamp requirements

Pay special attention to:

- timezone-aware timestamps;
- UTC;
- Eastern Standard Time;
- Eastern Daylight Time;
- Eastern Prevailing Time;
- daylight-saving transitions;
- duplicated fall-back hours;
- missing spring-forward hours; and
- inconsistent hour-ending versus hour-beginning conventions.

Maintain both a market-local timestamp and a UTC timestamp where
appropriate.

Use `America/New_York` for timezone localization rather than manually
subtracting five hours.

Do not assume that all source timestamps use the same convention.

Document whether each source uses:

- hour beginning or hour ending;
- local time or UTC;
- EST, EDT, or EPT;
- numbered hours 1–24 or timestamps 00:00–23:00; and
- special daylight-saving markers.

Before merging tables, verify timestamp meaning rather than merely
matching formatted clock values.

# January 2025 feasibility tables

Create two separate hourly tables:

## PJM table

Merge:

- PJM PSEG day-ahead LMP;
- PJM PS load; and
- Newark weather.

## NYISO table

Merge:

- NYISO Hudson Valley day-ahead LBMP;
- Hudson Valley integrated load; and
- Stewart Airport weather.

Each completed January 2025 table should contain exactly 744 hourly
rows unless a documented source issue justifies otherwise.

Use one-to-one merge validation when both sides should contain one row
per timestamp.

Preserve flags identifying:

- imputed weather;
- missing source observations;
- duplicate-source resolution;
- invalid or rejected measurements; and
- any manual correction.

Actual load and observed weather may be retained for exploration, data
validation, and later lag construction. Do not automatically use their
contemporaneous values as day-ahead predictors.

# Data integrity and auditability

Treat files under `data/raw/` as immutable source data.

Never overwrite, manually edit, or silently repair a raw source file.

Store:

- intermediate data under `data/interim/`;
- final analysis-ready data under `data/processed/`;
- figures under `reports/figures/`;
- tables under `reports/tables/`;
- trained models under `outputs/models/`;
- model metrics under `outputs/metrics/`; and
- predictions under `outputs/predictions/`.

Document source URLs, download dates, query parameters, market
locations, units, and relevant definitions in
`docs/data_source_register.md`.

Document important methodological choices in
`docs/methodology_decisions.md`.

Maintain a data dictionary in `docs/data_dictionary.md`.

# Data-quality validation

Add assertions or automated tests for:

- expected row counts;
- column presence;
- timestamp parsing;
- timestamp uniqueness;
- chronological ordering;
- expected time ranges;
- missingness;
- numeric conversion;
- units;
- price-component reconciliation where applicable;
- valid measurement ranges;
- join cardinality;
- duplicate records;
- timezone conversion;
- daylight-saving transitions; and
- absence of future information in model features.

A merge that runs without an exception is not sufficient proof that the
data was merged correctly.

Inspect unmatched timestamps and unexpected row-count changes.

# Code organization

Use Python 3.12.

Prefer:

- `pathlib.Path` instead of hard-coded path strings;
- descriptive variable and function names;
- small functions with one clear responsibility;
- type hints;
- concise docstrings;
- pandas method chains only when they remain readable;
- scikit-learn `Pipeline` and `ColumnTransformer` where appropriate;
- fixed random seeds;
- explicit configuration values; and
- deterministic output where practical.

Keep notebooks readable and focused on explanation, exploration, and
results.

Move stable reusable logic into `src/electricity_forecasting/`.

Avoid copying substantial cleaning or feature-engineering logic across
multiple notebooks.

Do not introduce unnecessary frameworks, abstractions, or cloud
services.

# Notebook requirements

A notebook must:

- run from beginning to end after a kernel restart;
- contain its own imports or import project modules;
- not depend on variables created in a different notebook;
- show important validation results;
- explain the purpose of each major section;
- avoid hidden manual steps; and
- use relative project paths.

Variables disappear when the kernel restarts. If a notebook uses a raw
DataFrame, it must load that DataFrame or call a reusable loading
function.

Use notebooks for learning and exploration, but move finalized
production logic into `src/`.

# Testing requirements

Use `pytest`.

Before declaring a task complete:

1. Run the relevant notebook or script.
2. Run applicable tests.
3. Inspect row counts and missingness.
4. Check timestamp uniqueness and ordering.
5. Review joins and feature timing.
6. Confirm that raw data was not modified.
7. Explain how the student can reproduce the result.

When correcting a bug, add a regression test when practical.

# Academic integrity

The student must be able to explain and defend every methodological and
programming decision.

Never provide:

- fabricated citations;
- fabricated quotations;
- invented data definitions;
- invented model results;
- invented statistical significance;
- generated conclusions unsupported by reproduced output; or
- claims that cannot be traced to code, data, or a reliable source.

Clearly distinguish among:

- observed facts;
- source documentation;
- assumptions;
- methodological decisions;
- exploratory findings; and
- final results.

Use primary and authoritative sources for PJM, NYISO, NOAA, EIA, market
rules, and data definitions whenever possible.

Record AI assistance if required by the DATA 698 syllabus or professor.

# Research-paper requirements

The final paper should allow a reader to trace every reported table,
figure, metric, and conclusion to reproducible code and stored output.

Support development of:

- problem statement;
- research question;
- literature review;
- data-source description;
- methodology;
- exploratory analysis;
- model design;
- evaluation;
- results;
- limitations;
- conclusions;
- references; and
- appendices where appropriate.

Do not write conclusions before validated results exist.

Use Quarto for the final reproducible report unless the student chooses
a different approved format.

# Git workflow

Work in small, meaningful units.

Before recommending a commit:

- run relevant tests;
- review changed files;
- verify that generated or private files are excluded;
- update documentation when necessary; and
- summarize what the commit represents.

Do not commit:

- `.venv/`;
- notebook checkpoints;
- caches;
- credentials;
- secrets;
- unnecessarily large generated files; or
- raw data when licensing, size, or repository policy prohibits it.

Do not push, merge, delete branches, or rewrite Git history without the
student's explicit request.

# Working sequence

For each project unit:

1. Explain the concept and its role in the project.
2. Inspect the relevant data or existing code.
3. Define a small testable objective.
4. Let the student implement or complete an important part.
5. Run and inspect the result.
6. Diagnose errors before changing the code.
7. Refactor stable logic into `src/`.
8. Add validation or a test.
9. Ask the student to explain or modify the result.
10. Update project documentation.
11. Review changes before committing to Git.

# Scope control

This is a 13-week graduate capstone, not a production electricity-market
forecasting platform.

When proposing additional work, classify it as one of:

- required for a valid capstone;
- useful if time permits; or
- future enhancement.

Prioritize:

1. valid and comparable data;
2. realistic predictor timing;
3. reproducible preprocessing;
4. strong baselines;
5. leakage-free evaluation;
6. interpretable model comparison;
7. a defensible paper and presentation; and
8. professional repository quality.

Avoid unnecessary scope expansion.

## Project documentation maintenance

When completing a substantial project task:

- Update `docs/current_status.md` with completed work, validation results,
  unresolved issues, and the exact next task.
- Update `docs/decisions.md` when a methodological or architectural decision
  is made.
- Update `docs/data_dictionary.md` when datasets, fields, units, time zones,
  transformations, or derived features change.
- Update `docs/project_plan.md` only when the project scope, schedule,
  milestones, or deliverables change.
- Do not modify documentation merely to restate unchanged information.
- Include relevant documentation updates in the same Git commit as the
  corresponding code change.

  ## Code comments and documentation

- Add concise docstrings to public modules, classes, and functions.
- Add comments only where they explain business rules, methodological
  decisions, non-obvious transformations, or important assumptions.
- Document units, time zones, forecast horizons, and data-availability
  constraints where they affect the code.
- Explain safeguards against target leakage and look-ahead bias.
- Do not add comments that merely repeat what the code already says.
- Preserve useful existing comments and update comments when the related
  implementation changes.
- Use `TODO` comments only for specific, actionable unfinished work.
