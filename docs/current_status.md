# Current Status — Electricity Price Forecasting Capstone

**Last verified:** September 14, 2026  
**Current phase:** Conditional GO for revised load-forecast value study

## Research question

> How much does adding day-ahead load forecasts improve hourly day-ahead electricity-price prediction accuracy in PJM PSEG and NYISO Hudson Valley, and is the improvement larger in one market than the other?

## Supplementary question

> Does the day-ahead load forecast contain more unique predictive information about electricity prices in the market where the larger improvement occurs?

The supplementary question will be answered with predictive/statistical evidence, not a broad causal explanation such as unspecified “market design.”

## Current readiness decision

**Status: Conditional GO.**

The January 2025 feasibility pipeline is sufficiently mature to continue, but the revised research question becomes a **Full GO** only after the checkpoint in `docs/full_go_checkpoint.md` passes.

### Full-GO criteria

1. PJM January 2025 MIDATL historical load-forecast integration passes cutoff, uniqueness, merge, and coverage tests.
2. NYISO January 2025 forecast timing is regenerated using P-7 `Last Updated` and passes the same leakage controls.
3. Representative 2020, 2024, and DST historical spot checks work for both markets.
4. Valid pre-cutoff load-forecast coverage is measured and judged sufficient, with gaps documented rather than silently repaired.
5. The base-versus-augmented feature-ablation design is frozen before final modeling.

## Project scope

- PJM target: PSEG zone, pnode `51301`, hourly day-ahead total LMP.
- NYISO target: Hudson Valley Zone G, `HUD VL`, PTID `61758`, hourly day-ahead LBMP.
- Unit of analysis: one market-location-hour.
- Canonical key: timezone-aware `timestamp_utc`.
- Market-local interpretation key: timezone-aware `timestamp_local`.
- January 2025 is a 744-hour feasibility/pipeline-development sample only.
- Planned primary study period: January 1, 2020 through December 31, 2024, subject to passing the Full-GO gate.
- Raw files remain immutable.

## Verified January 2025 pipeline status

- `notebooks/02_data_cleaning.ipynb` produces 744-row PJM and NYISO processed electricity tables.
- NOAA weather is reduced to a complete hourly index while preserving quality and missingness audit flags.
- `data/interim/nyiso_hudson_valley_load_forecast_vintages.csv` contains 4,464 vintage/target-hour rows covering 744 target hours, but its timing basis must be regenerated using P-7 `Last Updated`.
- Calendar and cutoff-safe historical-price features are implemented for both markets.
- Same-hour actual load, observed weather, target components, identifiers, and audit fields are excluded from the strict operational predictor set.
- January modeling-ready checkpoint files contain 744 unique ordered target hours per market.
- January feasibility work has passed notebook execution, pytest, Ruff, role-overlap checks, and prohibited-predictor checks.

## PJM status

Resolved:

- PSEG pnode `51301` is the price location.
- `PS` is the paired metered-load area.
- Historical load forecasts use `load_frcstd_hist`.
- `MIDATL` is the historical forecast geography and must be described as a regional proxy, not a PSEG-specific forecast.
- PJM confirmed `evaluated_at_ept` is when a historical forecast was generated and made available.
- The historical feed preserves six-hour snapshots.
- Project cutoff: latest eligible forecast strictly before 11:00 a.m. EPT on D−1.

Immediate PJM work:

- acquire enough late-December 2024/January 2025 `load_frcstd_hist` MIDATL data to cover every January target hour;
- select the latest eligible pre-cutoff forecast per target hour;
- merge it one-to-one into the PJM January modeling path;
- measure coverage; and
- add/execute tests for cutoff, latest-vintage selection, uniqueness, and join cardinality.

Historical validation still required:

- representative 2020 and 2024 samples;
- a DST-transition sample;
- continuity of pnode `51301`, `PS`, and MIDATL; and
- eventual full 2020–2024 acquisition.

PJM has no major unresolved external-source question that requires waiting for another response.

## NYISO status

Resolved/adopted:

- Hudson Valley target location: `HUD VL`, PTID `61758`.
- Historical price/load route: NYISO MIS public archive.
- Historical load-forecast product: P-7 ISO Load Forecast / `isolf`.
- P-7 contains rolling multi-day zonal forecasts including `HUD VL`.
- Project cutoff: strictly before 5:00 a.m. EPT on D−1.
- P-7 public-report `Last Updated` is the best available public-source evidence of forecast availability.

Use:

```text
availability_basis = p7_last_updated
availability_is_proxy = True
```

The proxy flag means the formal semantics are inferred from the public interface rather than directly operator-confirmed. ZIP-entry last-modified timestamps remain secondary provenance.

Immediate NYISO work:

- ingest/capture P-7 `Last Updated` for the January 2025 artifacts;
- regenerate the forecast-vintage table;
- select the latest eligible multi-day vintage strictly before 5:00 a.m.;
- rerun cutoff, tie, uniqueness, leakage, and merge validation; and
- measure coverage.

Historical validation still required:

- representative 2020 and 2024 samples;
- one or more DST-transition periods;
- `HUD VL` / PTID `61758` continuity;
- annual P-7 archive/schema conventions; and
- historical `Last Updated` metadata coverage.

A narrow NYISO clarification about the formal meaning of `Last Updated` remains useful but is not a blocker.

## Required data for the revised final study

Required:

- PJM PSEG day-ahead price history, 2020–2024;
- NYISO Hudson Valley day-ahead LBMP history, 2020–2024;
- PJM MIDATL `load_frcstd_hist` history with `evaluated_at_*`;
- NYISO P-7 Hudson Valley forecast history with usable `Last Updated` metadata;
- sufficient prior price history for lag/rolling features; and
- derived calendar fields.

Useful but not required for the main question:

- same-hour actual load;
- NOAA observed weather;
- archived weather forecasts;
- natural-gas prices;
- PyTorch or pretrained time-series models.

## Planned experiment after Full GO

Base feature set:

```text
calendar + cutoff-safe historical price features
```

Augmented feature set:

```text
calendar + cutoff-safe historical price features + eligible load_forecast_mw
```

Primary models:

1. persistence baseline;
2. Ridge or Elastic Net;
3. Random Forest;
4. XGBoost or `HistGradientBoostingRegressor`.

Primary metrics: MAE, RMSE, and percentage error improvement from base to augmented features.

Candidate chronological split, subject to final coverage review:

- 2020–2022 train;
- 2023 validation/tuning;
- 2024 untouched test.

## Full-GO fallback

If one market cannot provide defensible historical pre-cutoff load-forecast coverage, do not force the load-forecast-centered question.

Fallback:

> How does hourly day-ahead electricity-price predictability differ between PJM PSEG and NYISO Hudson Valley using historical prices and calendar information?

## Exact next action

**Complete the PJM January 2025 MIDATL historical load-forecast proof.** After that, regenerate NYISO January timing with P-7 `Last Updated`, then run the historical spot checks and coverage gate described in `docs/full_go_checkpoint.md`.
