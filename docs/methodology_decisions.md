# Methodology Decisions

**Last updated:** September 1, 2026

This document records the methodological decisions that govern the electricity-price forecasting capstone. It distinguishes adopted rules, conditional features, unresolved source questions, and future validation work.

## Status definitions

| Status | Meaning |
|---|---|
| Adopted | Supported by available evidence and currently governs implementation. |
| Conditional | Usable for feasibility or sensitivity analysis but not yet approved for the final strict operational model. |
| Under investigation | Additional evidence is still required. |
| Future action | Implementation or validation work still required. |

## M-01 — Research design

**Status:** Adopted

The project will forecast hourly day-ahead electricity prices separately for:

- PJM PSEG pricing zone; and
- NYISO Hudson Valley Zone G.

The unit of analysis is one market-location-hour. January 2025 is a feasibility and pipeline-development sample. The planned primary study period is January 1, 2020 through December 31, 2024.

## M-02 — Price targets and locations

**Status:** Adopted

### PJM

- Location: PSEG zone.
- Pricing node: `51301`.
- Paired metered-load area: `PS`.
- Target: `total_lmp_da`.
- Unit: `$/MWh`.

PJM confirmed that node `51301` is the appropriate PSEG zone-level pricing node to pair with the `PS` metered-load area. `total_lmp_da` is treated as the complete day-ahead LMP target; its components must not be added to it again.

### NYISO

- Location: Hudson Valley Zone G.
- Name: `HUD VL`.
- PTID: `61758`.
- Target: published day-ahead `LBMP ($/MWHr)`.
- Unit: `$/MWh`.

NYISO confirmed PTID `61758` for both Hudson Valley zonal day-ahead LBMP and actual zonal load.

## M-03 — Canonical timestamps

**Status:** Adopted

`timestamp_utc` is the canonical field for joins, ordering, duplicate detection, validation, train/validation/test splitting, and modeling.

Timezone-aware market-local timestamps are retained for interpretation, calendar features, cutoff construction, and reporting.

Raw NOAA LCDv2 `DATE` values are different: they use fixed Local Standard Time and do not apply daylight saving time. For Newark and Stewart they must initially be interpreted as fixed UTC−05:00 before conversion to UTC.

## M-04 — Forecast origins and leakage rule

**Status:** Adopted

### PJM cutoff

Use the latest eligible predictor value strictly before **11:00 a.m. EPT on D−1**.

### NYISO cutoff

Use the latest eligible predictor value strictly before **5:00 a.m. EPT on D−1**.

A timestamp exactly at the cutoff is excluded under the project’s conservative rule unless authoritative evidence proves prior availability.

### Controlling rule

Every operational predictor must have been available at the applicable market forecast origin. Same-hour actual load, same-hour observed weather, future prices, and post-cutoff forecast vintages are excluded from the strict operational model.

## M-05 — PJM historical load forecasts

**Status:** Adopted candidate predictor; implementation pending

- Feed: `load_frcstd_hist`.
- Forecast area: `MIDATL`.
- Availability timestamp: `evaluated_at_ept` / `evaluated_at_utc`.
- Target hour: `forecast_hour_beginning_ept` / `forecast_hour_beginning_utc`.
- Value: `forecast_load_mw`.

PJM confirmed that:

- MIDATL is the narrowest preserved historical forecast area covering PSEG;
- PSEG-specific historical forecast detail is not available;
- `evaluated_at_ept` is when the historical forecast was generated and made available; and
- the historical feed preserves six-hour snapshots rather than every live twice-hourly revision.

MIDATL must always be described as a regional proxy, not as PSEG-specific forecast load.

**Future action:** acquire 2020–2024 MIDATL history and implement latest-eligible-vintage selection strictly before the 11:00 a.m. cutoff.

## M-06 — NYISO historical load forecasts

**Status:** Conditional

NYISO directed the project to the ISO Load Forecast archive / NY Load Forecast Custom Reports. The January pilot preserves all available vintages, applies a 5:00 a.m. D−1 cutoff, and selects the latest eligible vintage for each target hour.

The implemented January workflow uses the ZIP-entry last-modified timestamp as a proxy for original public availability:

```text
availability_basis = zip_entry_last_modified
availability_is_proxy = True
```

This proxy is sufficient for pipeline development but is not yet authoritative evidence for final strict operational use.

The remaining source-validation question is narrow: whether NYISO preserves a field, report timestamp, archive convention, or other authoritative indicator that proves when a specific historical short-term ISO Load Forecast vintage became publicly available.

If NYISO identifies an authoritative timestamp, validate and replace the proxy where appropriate. If NYISO confirms that no authoritative historical publication/availability timestamp is retained, exclude `load_forecast_mw` from the strict operational model and retain it only in a clearly labeled conditional or sensitivity analysis.

## M-07 — Actual load

**Status:** Adopted exclusion for the strict operational model

Same-hour actual/metered/integrated load is unavailable at the day-ahead forecast origin and will not be used directly as an operational predictor.

Actual load may be used for EDA, descriptive analysis, explanatory models, or carefully justified lagged features whose values were available before cutoff.

## M-08 — NOAA stations

**Status:** Adopted with geographic limitation

- Newark Liberty International Airport: `USW00014734`.
- New York Stewart International Airport: `USW00014714`.

These are defensible point observations, not perfect representations of the full electricity-pricing zones.

**Future action:** audit both stations in HOMR for 2020–2024 location, equipment, instrumentation, and reporting changes.

## M-09 — NOAA units and observations

**Status:** Adopted

LCDv2 is the primary observed-weather source. Bulk station-year CSV files use SI/metric units. Blank precipitation means missing/unreported, not zero. Raw values, quality indicators, and audit information should be preserved where practical.

Observed target-hour weather is descriptive unless an operationally available forecast or leakage-safe lag is demonstrated.

## M-10 — NYISO daylight-saving-time handling

**Status:** Adopted at the documentation level; implementation/testing pending

NYISO Technical Bulletin TB-064 documents the fall transition to Eastern Standard Time and the resulting 25-hour operating day.

For the fall transition:

- the first 01:00 hour occurs in EDT;
- the second 01:00 hour occurs in EST;
- MIS Upload/Download identifies the repeated second hour as `HB25`;
- MIS Web distinguishes `HB01 EDT` and `HB01 EST`; and
- the repeated local hour maps to a distinct UTC hour.

NYISO Technical Bulletin TB-088 documents the spring transition to Eastern Daylight Time and the resulting 23-hour operating day.

For the spring transition:

- `HB02` does not occur in MIS Upload/Download;
- the sequence advances from 01:00 EST to 03:00 EDT; and
- UTC remains continuous and unique.

The DST source-documentation issue is considered resolved. The remaining work is to implement and test these conventions against actual 2020–2024 NYISO files. Because the available bulletins are 2026 versions, the historical files themselves must be audited rather than assuming every earlier year is identical.

## M-11 — Lagged and rolling features

**Status:** Adopted

Every lag and rolling feature must be evaluated against the market forecast origin, not merely against row order. Rolling features must shift before rolling so that target and future information cannot enter the feature window.

## M-12 — Data splitting and preprocessing

**Status:** Adopted

- No random train/test split.
- Use chronological train/validation/test periods.
- Use rolling-origin or expanding-window validation for tuning.
- Fit scaling, imputation, encoding, and feature selection on training data only.
- Preserve an untouched final test period.

A candidate full-period split is training 2020–2022, validation 2023, and final test 2024, subject to final source coverage and structural-break review.

## M-13 — Price extremes and metrics

**Status:** Adopted

Negative prices and legitimate price spikes remain in the target series. Primary metrics are MAE and RMSE. MAPE is not a primary metric because electricity prices can be zero or negative.

## M-14 — Final PJM historical price feed

**Status:** Under investigation

The January pilot uses `da_hrl_lmps`. Before final 2020–2024 acquisition, decide whether the historical target will use settlements-verified `rt_da_monthly_lmps` or whether `da_hrl_lmps` will be reconciled against it.

## M-15 — Historical continuity and structural changes

**Status:** Future action

Before final modeling, audit:

- PSEG pnode `51301` effective/termination history;
- `PS` load-area continuity;
- MIDATL historical forecast coverage and schema;
- the September 1, 2021 PJM fast-start-pricing change as a possible structural break;
- NYISO `HUD VL` / PTID `61758` continuity;
- NYISO annual schemas and DST behavior;
- NOAA station histories; and
- annual field names, units, revisions, and missingness.

## M-16 — NYISO Load Forecasting Manual

**Status:** Supporting documentation only

NYISO M-06 Load Forecasting Manual Version 5.1 documents ICAP/capacity-planning load forecasting, weather normalization, and related submission procedures. It does **not** establish the publication timestamp of the short-term historical ISO Load Forecast archive used by this project.

## M-17 — Source privacy and citation

**Status:** Adopted

Private PJM/NYISO correspondence containing personal contact information, full mail headers, or confidentiality notices must remain outside the public repository. Public technical documentation should be cited whenever it supports the same methodological conclusion.

## Change protocol

When later evidence changes a decision:

1. record the new evidence and date;
2. mark the prior rule as superseded rather than silently deleting its rationale;
3. identify affected notebooks, functions, datasets, and model results;
4. rebuild derived data where necessary;
5. rerun tests and notebooks from a clean kernel; and
6. update `docs/current_status.md`, `docs/data_source_register.md`, `docs/data_dictionary.md`, `docs/project_plan.md`, and this file together.
