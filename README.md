# Electricity Price Forecasting Capstone

Graduate data-science capstone comparing the incremental predictive value of day-ahead load forecasts for hourly day-ahead electricity-price forecasting in:

- PJM PSEG pricing zone, pnode `51301`
- NYISO Hudson Valley Zone G, `HUD VL`, PTID `61758`

The target is hourly day-ahead total LMP/LBMP in `$/MWh`. The unit of analysis is one market-location-hour.

## Research question

> How much does adding day-ahead load forecasts improve hourly day-ahead electricity-price prediction accuracy in PJM PSEG and NYISO Hudson Valley, and is the improvement larger in one market than the other?

## Supplementary question

> Does the day-ahead load forecast contain more unique predictive information about electricity prices in the market where the larger improvement occurs?

The supplementary question is intentionally predictive/statistical rather than a broad causal claim about market design.

## Current decision status

**Conditional GO.** The January 2025 feasibility pipeline is proven, but the revised load-forecast-centered research design becomes a **Full GO** only after the validation gate in `docs/full_go_checkpoint.md` passes.

The five Full-GO criteria are:

1. complete the PJM January 2025 `load_frcstd_hist` / `MIDATL` load-forecast path;
2. regenerate NYISO January 2025 forecast timing using P-7 `Last Updated`;
3. prove the same rules on representative 2020, 2024, and DST historical samples;
4. measure and accept forecast coverage without using post-cutoff data or silent imputation; and
5. freeze the base-versus-augmented feature-ablation design.

## Study design

January 2025 is a 744-hour feasibility and pipeline-development sample. It is used to validate source acquisition, schemas, timestamp handling, data quality, forecast-vintage reconstruction, information cutoffs, feature definitions, leakage controls, reproducibility, and automated validation.

January 2025 is **not** the final evidence base. The planned primary study period is **January 1, 2020 through December 31, 2024**.

## Markets and targets

| Market | Location | Identifier | Target |
|---|---|---|---|
| PJM | PSEG pricing zone | pnode `51301` | Hourly day-ahead total LMP |
| NYISO | Hudson Valley Zone G | `HUD VL`, PTID `61758` | Hourly day-ahead LBMP |

PJM metered load uses load area `PS`. PJM historical load forecasts use `MIDATL`, which is explicitly treated as a regional proxy rather than a PSEG-specific load forecast.

## Forecast origin and leakage policy

A predictor is eligible only if it can be demonstrated to have been available before the applicable market cutoff.

| Market | Project cutoff |
|---|---|
| PJM | Strictly before 11:00 a.m. EPT on D−1 |
| NYISO | Strictly before 5:00 a.m. EPT on D−1 |

Same-hour actual load, same-hour observed weather, target components, future prices, identifiers, and audit fields are excluded from the strict operational predictor set.

## Required final-study data

Required for the revised question:

- PJM PSEG day-ahead price history for 2020–2024;
- NYISO Hudson Valley day-ahead LBMP history for 2020–2024;
- PJM `load_frcstd_hist` MIDATL forecasts with `evaluated_at_*` timing;
- NYISO P-7 Hudson Valley forecasts with historical `Last Updated` metadata;
- sufficient prior data for cutoff-safe historical-price features; and
- calendar variables derived from market-local timestamps.

Useful but not required for the main question: actual load, NOAA observed weather, archived weather forecasts, natural-gas prices, PyTorch models, and pretrained time-series models.

## Full-GO execution order

1. Finish PJM January 2025 historical load-forecast ingestion, eligibility filtering, and one-to-one merge.
2. Regenerate NYISO January forecast-vintage timing with P-7 `Last Updated` and rerun leakage tests.
3. Run historical continuity spot checks in 2020, 2024, and a DST-transition period for both markets.
4. Produce a coverage and leakage-validation summary.
5. Record Full GO, Conditional GO, or No-GO for the load-forecast-centered question.
6. If Full GO, acquire the complete 2020–2024 study data and freeze the experimental design.

See `docs/full_go_checkpoint.md` for the detailed acceptance criteria.

## Experimental design after Full GO

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

Primary model families:

1. persistence baseline;
2. Ridge or Elastic Net regression;
3. Random Forest regression; and
4. gradient-boosted tree regression such as XGBoost or `HistGradientBoostingRegressor`.

Use chronological evaluation only. Candidate split, subject to final coverage review:

- training: 2020–2022;
- validation/tuning: 2023;
- final untouched test: 2024.

Primary metrics are MAE and RMSE, including the percentage improvement from the base feature set to the augmented feature set. MAPE is not primary because electricity prices may be zero or negative.

## Supplementary-analysis plan

If one market benefits more from load forecasts, measure whether `load_forecast_mw` contributes more unique predictive information there using controlled feature ablation, baseline residual association, permutation importance, and out-of-sample error reduction. Do not substitute vague explanations such as “market design” unless a specific measurable mechanism is demonstrated.

## Current verified January status

Verified work includes 744-row PJM and NYISO processed electricity tables, NYISO forecast-vintage reconstruction, calendar features, cutoff-safe historical price features, January EDA, modeling-ready checkpoint tables, pytest validation, and Ruff checks.

The remaining January work for the revised question is specifically:

- implement PJM MIDATL historical load forecasts; and
- regenerate NYISO P-7 timing using `Last Updated` rather than ZIP-only timing.

## Source timing rules

### PJM

Use `load_frcstd_hist` with `forecast_area = MIDATL`. PJM confirmed that `evaluated_at_ept` represents when the historical forecast was generated and made available. Select the latest eligible snapshot strictly before 11:00 a.m. EPT on D−1.

### NYISO

Use the public P-7 ISO Load Forecast / `isolf` route. Use:

```text
availability_basis = p7_last_updated
availability_is_proxy = True
```

P-7 `Last Updated` is the best available public-source evidence of forecast availability. Its formal semantics remain inferred rather than directly operator-confirmed. ZIP-entry timestamps remain secondary provenance.

## Timekeeping and DST

`timestamp_utc` is the canonical key for joins, chronological ordering, duplicate detection, splitting, and modeling. Timezone-aware `timestamp_local` is retained for market interpretation, calendar features, and cutoff construction.

NYISO TB-064 documents the 25-hour fall-back day and `HB25`; TB-088 documents the 23-hour spring-forward day and omitted `HB02`. Actual 2020–2024 files still require implementation testing. PJM DST behavior must also be validated empirically.

## Repository guide

| Path | Purpose |
|---|---|
| `AGENTS.md` | Stable instructions and guardrails for IDE/Codex agents |
| `docs/current_status.md` | Authoritative current state and exact next task |
| `docs/full_go_checkpoint.md` | Acceptance criteria for committing to the revised research question |
| `docs/project_plan.md` | Project roadmap and final-study design |
| `docs/methodology_decisions.md` | Methodological decisions and evidence status |
| `docs/data_dictionary.md` | Field definitions, units, timing, and feature roles |
| `docs/data_source_register.md` | Source provenance, limitations, and acquisition requirements |
| `docs/notebook_pipeline_map.md` | High-level notebook/code workflow |
| `docs/decisions.md` | Dated decision index |
| `docs/learning_log.md` | Learning and reproducibility record |

## Current next action

Complete the PJM January 2025 MIDATL historical load-forecast proof, then regenerate NYISO January timing with P-7 `Last Updated`. Do not begin final model selection until the Full-GO checkpoint has been evaluated.
