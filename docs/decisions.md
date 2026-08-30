# Decision Log

Detailed reasoning lives in `docs/methodology_decisions.md`. This table is the dated index of decisions that affect implementation.

| ID | Date | Decision | Status |
|---|---|---|---|
| D-001 | 2026-08-24 | Use PJM PSEG pnode 51301 and NYISO HUD VL/PTID 61758; model markets separately. | Active |
| D-002 | 2026-08-24 | Use `day_ahead_price_usd_mwh` as the canonical target name and `actual_load_mw` for observed target-hour load. | Active; reusable January path reconciled and tested in Task 2 |
| D-003 | 2026-08-24 | Use `timestamp_utc` for joins/order/splits and timezone-aware `timestamp_local` for interpretation/calendar features. | Active |
| D-004 | 2026-08-24 | Use NYISO D−1 05:00 America/New_York as the provisional cutoff and select the latest eligible vintage. | Active, provisional |
| D-005 | 2026-08-24 | Preserve `availability_is_proxy=True` for all current NYISO selections because ZIP-entry modification time is not an authoritative publication timestamp. | Active limitation |
| D-006 | 2026-08-24 | Use PJM D−1 11:00 America/New_York as a configurable provisional cutoff while authoritative confirmation is absent. | Active, provisional |
| D-007 | 2026-08-24 | Exclude same-hour actual load, observed weather, target components, identifiers, and forecast audit fields from operational predictors. | Active |
| D-008 | 2026-08-24 | Require forecast-origin-aware availability tests before approving historical lags or rolling features. | Active |
| D-009 | 2026-08-24 | Treat the downloaded NOAA LCD values as SI and reconcile reusable code to Notebook 02's selection and audit policy. | Active; January implementation verified in Task 2 |
| D-012 | 2026-08-25 | Select one eligible NOAA report per January hour by `FM-15`, then `FM-12`, then `FM-16` priority; retain missingness, quality, rejection, and imputation audit flags. | Active for January 2025; validate NOAA timestamp behavior across DST before the 2020–2024 expansion |
| D-013 | 2026-08-25 | Require a common-versus-NYISO-augmented feature ablation and error-by-regime reporting in final model comparison; treat importance stability and tuning diagnostics as time-permitting. | Active; no new model families or final-test-driven selection |
| D-010 | 2026-08-24 | Proceed without blocking on unanswered ISO correspondence; keep assumptions conservative, testable, configurable, and explicitly provisional. | Active |
| D-011 | 2026-08-24 | Complete the seven pre-modeling tasks before baseline model development. | Active |
| D-014 | 2026-08-29 | For January 2025 NYISO historical-price features, retain a prior-day same-hour price only when its provisional availability time is no later than the target cutoff; compute the 24-hour mean only from those safe lag values. | Active; price-schedule availability is provisional and does not replace the load-forecast proxy warning |

When a decision changes, add a new row that identifies the replaced decision rather than silently rewriting the historical rationale.

# Methodological decisions

## NYISO January 2025 load-forecast cutoff and vintage selection

For the January 2025 NYISO Hudson Valley feasibility sample, the day-ahead
prediction cutoff is defined as 5:00 a.m. America/New_York on the calendar day
before the target delivery date.

For each target hour, retain forecast vintages only when:

`forecast_available_at <= prediction_cutoff`

Select the eligible vintage with the latest `forecast_available_at`. Require
exactly one selected vintage per target hour; a tie at the latest eligible
availability timestamp is treated as a data-quality error.

`forecast_available_at` is derived from the archived ZIP entry's recorded
last-modified timestamp. It is therefore a proxy for original NYISO forecast
availability and is retained with `availability_is_proxy=True` and
`availability_basis="zip_entry_last_modified"`.

Use `load_forecast_mw` as the currently approved NYISO load-based candidate
predictor. Exclude same-hour actual load and forecasts available after the
cutoff from model inputs. Retain forecast timing and source-provenance fields
for auditability rather than as model features.

This decision applies to the January 2025 feasibility sample and must be
reassessed before extending the analysis to the planned 2020–2024 study period.
