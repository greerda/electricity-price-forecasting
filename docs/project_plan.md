# Electricity Price Forecasting Capstone — Project Plan

**Last updated:** September 14, 2026  
**Current phase:** Conditional GO — validating the load-forecast-centered research design

## 1. Project overview

This capstone will measure the incremental predictive value of day-ahead load forecasts for hourly day-ahead electricity-price forecasting in:

- PJM PSEG pricing zone; and
- NYISO Hudson Valley Zone G.

January 2025 is the feasibility and pipeline-development sample. The planned primary study period is January 1, 2020 through December 31, 2024, subject to passing the Full-GO checkpoint.

## 2. Research question

> How much does adding day-ahead load forecasts improve hourly day-ahead electricity-price prediction accuracy in PJM PSEG and NYISO Hudson Valley, and is the improvement larger in one market than the other?

## 3. Supplementary question

> Does the day-ahead load forecast contain more unique predictive information about electricity prices in the market where the larger improvement occurs?

The supplementary analysis is predictive/statistical. It does not presume that an undefined concept such as “market design” explains any difference.

## 4. Markets, targets, and identifiers

| Market | Location | Identifier | Target | Unit |
|---|---|---|---|---|
| PJM | PSEG zone | pnode `51301`; paired load area `PS` | `day_ahead_price_usd_mwh` from total DA LMP | `$/MWh` |
| NYISO | Hudson Valley Zone G | `HUD VL`, PTID `61758` | `day_ahead_price_usd_mwh` from published DA LBMP | `$/MWh` |

Unit of analysis: one market-location-hour.

PJM MIDATL load forecast is a regional proxy for PSEG and must be labeled accordingly.

## 5. Forecast origins

| Market | Operational cutoff | Eligibility rule |
|---|---|---|
| PJM | 11:00 a.m. EPT on D−1 | Predictor must be available strictly before 11:00 a.m. |
| NYISO | 5:00 a.m. EPT on D−1 | Predictor must be available strictly before 5:00 a.m. |

`timestamp_utc` is the canonical join/order/split key. Market-local timestamps are retained for interpretation, calendar features, and cutoff construction.

## 6. Full-GO checkpoint

The project is currently **Conditional GO** for the revised research question. It becomes a **Full GO** only when all of the following pass:

1. PJM January 2025 historical load-forecast integration;
2. NYISO January 2025 P-7 timing regeneration;
3. representative historical continuity tests in 2020, 2024, and a DST period;
4. forecast-coverage measurement and acceptance; and
5. final experimental-design freeze.

Detailed acceptance criteria live in `docs/full_go_checkpoint.md`.

## 7. Immediate implementation sequence

### Step A — PJM January 2025

Acquire `load_frcstd_hist` / `MIDATL` data covering enough late December 2024 and January 2025 to support all January target hours.

For each target hour:

- build the D−1 11:00 a.m. EPT cutoff;
- require `evaluated_at_ept < prediction_cutoff`;
- choose the latest eligible MIDATL forecast;
- preserve availability, target-hour, source, and cutoff audit fields;
- merge one-to-one into the PJM modeling-ready path; and
- measure coverage.

Add tests for eligibility, latest-vintage selection, uniqueness, and merge cardinality.

### Step B — NYISO January 2025

Regenerate the forecast-vintage path using P-7 `Last Updated`:

```text
availability_basis = "p7_last_updated"
availability_is_proxy = True
```

Retain ZIP timestamps as secondary provenance. Select the latest P-7 vintage strictly before 5:00 a.m. EPT D−1 whose multi-day horizon still contains the target hour. Rerun tie, uniqueness, leakage, coverage, and one-to-one merge checks.

### Step C — Historical spot checks

Before bulk acquisition, test both market pipelines on:

- one representative month in 2020;
- one representative month in 2024; and
- at least one DST-transition period.

Validate identifiers, schemas, forecast-vintage timing, UTC uniqueness, and source continuity.

### Step D — Coverage gate

Calculate the share of target hours with a defensible pre-cutoff load forecast for every test period. Do not use post-cutoff data or silent imputation to increase coverage. Material gaps must be understood and documented.

### Step E — Go/No-Go decision

- **Full GO:** both markets have defensible, sufficiently complete pre-cutoff forecast coverage and the experiment can be frozen.
- **Conditional GO:** more historical timing/coverage work is needed.
- **No-GO for load-forecast question:** one market cannot support a defensible comparison.

Fallback question if required:

> How does hourly day-ahead electricity-price predictability differ between PJM PSEG and NYISO Hudson Valley using historical prices and calendar information?

## 8. Required data after Full GO

Required:

- PJM PSEG DA price history, 2020–2024;
- NYISO Hudson Valley DA LBMP history, 2020–2024;
- PJM MIDATL `load_frcstd_hist` history with `evaluated_at_*`;
- NYISO P-7 Hudson Valley history with usable `Last Updated` metadata;
- enough prior price history for safe lag/rolling features; and
- derived calendar variables.

Useful but not required for the primary question:

- actual load;
- NOAA observed weather;
- archived weather forecasts;
- natural-gas prices;
- neural networks or pretrained time-series models.

## 9. Experimental design after Full GO

### Base feature set

```text
calendar features
+ cutoff-safe historical price features
```

### Augmented feature set

```text
calendar features
+ cutoff-safe historical price features
+ eligible load_forecast_mw
```

The model, split, preprocessing, seed, and metrics must remain fixed when comparing base versus augmented features.

## 10. Planned models

1. persistence baseline;
2. Ridge or Elastic Net regression;
3. Random Forest regression; and
4. XGBoost or `HistGradientBoostingRegressor`.

PyTorch/Hugging Face experiments are optional only after the core capstone is complete.

## 11. Evaluation

Chronological evaluation only. Candidate split, subject to final coverage review:

- train: 2020–2022;
- validation/tuning: 2023;
- final untouched test: 2024.

Primary metrics:

- MAE;
- RMSE;
- percentage MAE/RMSE improvement from base to augmented feature set.

R² may be used for interpretation. MAPE is not primary because prices can be zero or negative.

## 12. Supplementary-analysis plan

If one market benefits more from the load forecast, evaluate whether `load_forecast_mw` supplies more unique predictive information there using:

- controlled feature-ablation results;
- baseline residual association;
- permutation importance; and
- out-of-sample R² change where useful.

Do not claim a causal mechanism unless it is directly measured and supported.

## 13. Source status

### PJM

- `load_frcstd_hist` is the historical forecast feed.
- `MIDATL` is the relevant preserved regional forecast area.
- `evaluated_at_ept` is confirmed as the generated/available time.
- strict project rule: latest eligible forecast before 11:00 a.m. EPT D−1.
- no additional PJM response is required to proceed.

### NYISO

- P-7 / `isolf` is the historical load-forecast route.
- `Last Updated` is the best public-source evidence of forecast availability.
- formal semantics remain inferred; `availability_is_proxy=True`.
- strict project rule: latest eligible vintage before 5:00 a.m. EPT D−1 whose horizon contains the target hour.
- additional NYISO clarification remains useful but is not a blocker.

## 14. DST and continuity

Before final modeling:

- validate PJM Data Miner timestamp behavior across actual historical DST transitions;
- validate NYISO actual historical files against TB-064/TB-088 behavior;
- prove unique UTC target keys through transition dates;
- verify PSEG `51301`, `PS`, MIDATL, `HUD VL`, and PTID `61758` continuity; and
- audit schema/field changes by year.

## 15. Documentation governance

Authoritative documents:

- `docs/current_status.md` — current state and exact next action;
- `docs/full_go_checkpoint.md` — Full-GO acceptance criteria;
- `docs/methodology_decisions.md` — governing methodology;
- `docs/data_source_register.md` — source evidence and acquisition status;
- `docs/data_dictionary.md` — schema, timing, and feature roles;
- `docs/notebook_pipeline_map.md` — data/notebook flow;
- `docs/decisions.md` — dated decision index;
- `docs/learning_log.md` — learning/reproducibility record.

## 16. Immediate next action

Complete the PJM January 2025 MIDATL historical load-forecast proof, then regenerate NYISO January timing and run the historical spot-check/coverage gate before bulk 2020–2024 acquisition.
