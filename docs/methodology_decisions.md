# Methodology Decisions

**Last updated:** September 14, 2026

This document records methodological decisions governing the electricity-price forecasting capstone.

## M-01 — Research design

**Status:** Adopted conditionally pending Full-GO gate

Primary question:

> How much does adding day-ahead load forecasts improve hourly day-ahead electricity-price prediction accuracy in PJM PSEG and NYISO Hudson Valley, and is the improvement larger in one market than the other?

Supplementary question:

> Does the day-ahead load forecast contain more unique predictive information about electricity prices in the market where the larger improvement occurs?

The supplementary analysis is predictive/statistical, not a broad causal market-design analysis.

## M-02 — Full-GO gate

**Status:** Adopted

The revised question becomes fully committed only after all criteria in `docs/full_go_checkpoint.md` pass:

1. PJM January 2025 load-forecast integration;
2. NYISO January 2025 P-7 timing regeneration;
3. 2020/2024/DST historical continuity spot checks;
4. acceptable documented pre-cutoff forecast coverage; and
5. frozen base-versus-augmented experimental design.

Until then, status is **Conditional GO**.

## M-03 — Markets, targets, and unit

**Status:** Adopted

- PJM PSEG: pnode `51301`, target = complete hourly day-ahead LMP.
- NYISO Hudson Valley: `HUD VL`, PTID `61758`, target = complete hourly day-ahead LBMP.
- Unit of analysis: one market-location-hour.
- Canonical project target name: `day_ahead_price_usd_mwh`.

## M-04 — Study period

**Status:** Adopted subject to Full-GO coverage review

January 2025 is a feasibility/pipeline-development sample only. Planned primary period is January 1, 2020 through December 31, 2024.

Candidate final split:

- train 2020–2022;
- validation/tuning 2023;
- final untouched test 2024.

## M-05 — Canonical timestamps

**Status:** Adopted

Use `timestamp_utc` for joins, ordering, duplicate detection, splitting, and modeling. Retain timezone-aware local timestamps for interpretation, calendar features, and cutoff construction.

## M-06 — Forecast origins and leakage rule

**Status:** Adopted

- PJM cutoff: strictly before 11:00 a.m. EPT on D−1.
- NYISO cutoff: strictly before 5:00 a.m. EPT on D−1.

Same-hour actual load, same-hour observed weather, future prices, target components, and post-cutoff forecasts are excluded from the strict operational predictor set.

## M-07 — PJM historical load forecasts

**Status:** Adopted candidate predictor; January implementation pending

- Feed: `load_frcstd_hist`.
- Forecast area: `MIDATL`.
- Availability: `evaluated_at_ept` / `evaluated_at_utc`.
- Target hour: `forecast_hour_beginning_ept` / `forecast_hour_beginning_utc`.
- Value: `forecast_load_mw`.

PJM confirmed `evaluated_at_ept` is the generated-and-available timestamp. MIDATL is a regional proxy for PSEG, not a PSEG-specific forecast.

Selection rule:

```text
evaluated_at_ept < prediction_cutoff
```

Choose the latest eligible MIDATL forecast per target hour. Preserve audit fields and reject duplicate selected target hours.

Immediate validation requirement: implement and validate this rule for January 2025 before bulk historical acquisition.

## M-08 — NYISO historical load forecasts

**Status:** Adopted with evidence caveat

Use P-7 ISO Load Forecast / `isolf` for Hudson Valley.

```text
availability_basis = "p7_last_updated"
availability_is_proxy = True
```

P-7 public-report `Last Updated` is treated as the best available public-source evidence of forecast availability. Its formal semantics remain inferred rather than directly operator-confirmed. ZIP-entry timestamps remain secondary provenance.

Selection rule:

1. preserve every P-7 vintage whose rolling multi-day horizon contains the target hour;
2. construct D−1 05:00 EPT cutoff;
3. require `forecast_available_at < prediction_cutoff`; and
4. choose the latest eligible earlier vintage.

January 2025 must be regenerated using this rule before the revised study becomes Full GO.

## M-09 — Base-versus-augmented feature ablation

**Status:** Adopted after Full GO

Base feature set:

```text
calendar features
+ cutoff-safe historical price features
```

Augmented feature set:

```text
calendar features
+ cutoff-safe historical price features
+ eligible load_forecast_mw
```

To isolate the incremental predictive value of load forecasts, hold model family, chronological split, preprocessing, seed, and evaluation metrics fixed when comparing feature sets.

## M-10 — Primary models

**Status:** Adopted

Primary scope:

1. persistence baseline;
2. Ridge or Elastic Net regression;
3. Random Forest regression;
4. XGBoost or `HistGradientBoostingRegressor`.

PyTorch, Hugging Face, LSTM/GRU, and pretrained time-series models are optional extensions only after the core capstone is complete.

## M-11 — Evaluation metrics

**Status:** Adopted

Primary metrics:

- MAE;
- RMSE;
- percentage improvement in MAE/RMSE from base to augmented feature set.

R² may support interpretation. MAPE is not primary because prices may be zero or negative.

## M-12 — Supplementary predictive-information analysis

**Status:** Adopted

If load forecasts improve one market more than the other, measure whether they provide more unique predictive information there using:

- controlled feature-ablation error reduction;
- association between `load_forecast_mw` and baseline-model residuals;
- permutation importance; and
- out-of-sample R² change where useful.

Do not claim that undefined “market design” explains a difference unless a specific measurable mechanism is separately established.

## M-13 — Forecast coverage gate

**Status:** Adopted

Before Full GO, calculate valid pre-cutoff load-forecast coverage for representative 2020, 2024, and DST sample periods in both markets.

Coverage is acceptable only when sufficiently high for a defensible comparison and all material gaps are understood and documented.

Never use post-cutoff forecasts or silent imputation to increase coverage.

## M-14 — Historical continuity tests

**Status:** Future action required before Full GO

Verify on representative historical samples:

- PSEG pnode `51301` continuity;
- `PS` load-area continuity where relevant;
- MIDATL forecast-area availability and schema;
- `HUD VL` / PTID `61758` continuity;
- P-7 `Last Updated` metadata availability;
- annual schema/archive conventions; and
- unique UTC timestamps through DST transitions.

## M-15 — Actual load

**Status:** Adopted exclusion for strict operational model

Same-hour actual/metered/integrated load may be retained for EDA or safe lag experiments but is not a primary operational predictor.

## M-16 — Weather

**Status:** Optional for revised primary question

NOAA observed weather remains useful for EDA and potential safe-lag experiments, but it is not required to answer the revised load-forecast question. Archived weather forecasts are optional and should not delay the Full-GO checkpoint.

## M-17 — DST handling

**Status:** Documentation resolved; implementation testing pending

NYISO TB-064: 25-hour fall-back day, repeated second 01:00, `HB25` in MIS Upload/Download.

NYISO TB-088: 23-hour spring-forward day, `HB02` absent.

PJM and NYISO historical source files must still be tested empirically. UTC must remain unique.

## M-18 — Full-GO fallback

**Status:** Adopted contingency

If one market lacks defensible historical pre-cutoff load-forecast coverage, do not force the revised primary question.

Fallback:

> How does hourly day-ahead electricity-price predictability differ between PJM PSEG and NYISO Hudson Valley using historical prices and calendar information?

## M-19 — External-contact requirement

**Status:** Adopted

No additional PJM or NYISO response is required to begin or complete the Full-GO checkpoint.

- PJM timing semantics are sufficiently resolved for implementation.
- NYISO clarification of the formal meaning of `Last Updated` is useful but not blocking.

If later evidence changes the timing interpretation, rebuild affected features and rerun leakage checks.

## Change protocol

When evidence changes a governing rule:

1. record the new evidence and date;
2. mark the prior rule superseded rather than silently deleting it;
3. identify affected code, datasets, and results;
4. rebuild derived data;
5. rerun tests/notebooks; and
6. update `docs/current_status.md`, `docs/full_go_checkpoint.md`, `docs/data_source_register.md`, `docs/data_dictionary.md`, `docs/project_plan.md`, `docs/decisions.md`, and this file.
