# Decision Log

Detailed reasoning lives in `docs/methodology_decisions.md`. This table is the dated index of decisions that affect implementation.

| ID | Date | Decision | Status |
|---|---|---|---|
| D-001 | 2026-08-24 | Use PJM PSEG pnode 51301 and NYISO HUD VL/PTID 61758; model markets separately. | Active |
| D-002 | 2026-08-24 | Use `day_ahead_price_usd_mwh` as the canonical target name and `actual_load_mw` for observed target-hour load. | Active; reusable January path reconciled and tested in Task 2 |
| D-003 | 2026-08-24 | Use `timestamp_utc` for joins/order/splits and timezone-aware `timestamp_local` for interpretation/calendar features. | Active |
| D-004 | 2026-08-24 | Use NYISO D−1 05:00 America/New_York as the provisional cutoff and select the latest eligible vintage. | Superseded in wording by D-016; 05:00 cutoff remains active |
| D-005 | 2026-08-24 | Preserve `availability_is_proxy=True` for all current NYISO selections because ZIP-entry modification time is not an authoritative publication timestamp. | Superseded by D-016; ZIP timing is now secondary provenance |
| D-006 | 2026-08-24 | Use PJM D−1 11:00 America/New_York as a configurable provisional cutoff while authoritative confirmation is absent. | Superseded in wording by D-018; 11:00 cutoff remains active |
| D-007 | 2026-08-24 | Exclude same-hour actual load, observed weather, target components, identifiers, and forecast audit fields from operational predictors. | Active |
| D-008 | 2026-08-24 | Require forecast-origin-aware availability tests before approving historical lags or rolling features. | Active |
| D-009 | 2026-08-24 | Treat the downloaded NOAA LCD values as SI and reconcile reusable code to Notebook 02's selection and audit policy. | Active; January implementation verified in Task 2 |
| D-010 | 2026-08-24 | Proceed without blocking on unanswered ISO correspondence; keep assumptions conservative, testable, configurable, and explicitly provisional. | Active |
| D-011 | 2026-08-24 | Complete the seven pre-modeling tasks before baseline model development. | Completed; all seven tasks passed by 2026-08-31 |
| D-012 | 2026-08-25 | Select one eligible NOAA report per January hour by `FM-15`, then `FM-12`, then `FM-16` priority; retain missingness, quality, rejection, and imputation audit flags. | Active for January 2025; validate NOAA timestamp behavior across DST before the 2020–2024 expansion |
| D-013 | 2026-08-25 | Require a common-versus-NYISO-augmented feature ablation and error-by-regime reporting in final model comparison; treat importance stability and tuning diagnostics as time-permitting. | Active; no new model families or final-test-driven selection |
| D-014 | 2026-08-29 | For January 2025 NYISO historical-price features, retain a prior-day same-hour price only when its provisional availability time is no later than the target cutoff; compute the 24-hour mean only from those safe lag values. | Active; price-schedule availability remains provisional |
| D-015 | 2026-08-30 | Apply the same cutoff-safe prior-day price-lag and full-window rolling-feature pattern to PJM PSEG, using the PJM D−1 11:00 America/New_York cutoff. | Active; price-schedule availability remains provisional |
| D-016 | 2026-09-01 | Use NYISO P-7 `Last Updated` as the best available public-source evidence of forecast availability; set `availability_basis="p7_last_updated"` and keep `availability_is_proxy=True` until NYISO confirms the field's formal publication semantics. Retain ZIP-entry timestamps as secondary provenance. | Active; replaces the ZIP-only timing rule in D-005 |
| D-017 | 2026-09-01 | Treat NYISO TB-064 and TB-088 as resolving DST conventions at the documentation level: fall-back uses a repeated 01:00 with `HB25` in MIS Upload/Download; spring-forward omits `HB02`. Historical 2020–2024 files still require implementation and regression testing. | Active |
| D-018 | 2026-09-01 | Treat PJM's D−1 11:00 EPT forecast cutoff as supported by PJM correspondence/public timing evidence; apply a strict `< 11:00` project eligibility rule. | Active |

When a decision changes, add a new row that identifies the replaced decision rather than silently rewriting the historical rationale.

# Current methodological decisions

## NYISO load-forecast availability and vintage selection

For each NYISO target hour, define the day-ahead prediction cutoff as 5:00 a.m. America/New_York on the calendar day before delivery.

The current primary availability evidence is the P-7 public report's `Last Updated` timestamp:

```text
availability_basis = "p7_last_updated"
availability_is_proxy = True
```

`availability_is_proxy=True` means the timing semantics are inferred from NYISO's public interface rather than directly confirmed by NYISO as a formal publication timestamp. ZIP-entry last-modified timestamps remain secondary provenance/audit values when available.

For each target hour:

1. preserve all P-7 vintages whose rolling multi-day horizon contains the target hour;
2. require `forecast_available_at < prediction_cutoff`;
3. reject any vintage at or after the 5:00 a.m. cutoff; and
4. select the latest eligible earlier vintage.

A tie at the latest eligible availability timestamp is a data-quality error and must not be resolved arbitrarily.

The January forecast-vintage and modeling-ready outputs must be regenerated after P-7 `Last Updated` is integrated into the implementation.

## PJM historical load-forecast cutoff

Use PJM `load_frcstd_hist` with `forecast_area = "MIDATL"` as the historical load-forecast source. MIDATL is a regional proxy for PSEG, not a PSEG-specific load forecast.

For each PJM target hour, use the strict project rule:

```text
forecast_available_at < 11:00 a.m. EPT on D−1
```

PJM confirmed that `evaluated_at_ept` represents when a historical forecast was generated and made available. Select the latest eligible MIDATL snapshot before the cutoff.

## Historical day-ahead price features

For each PJM or NYISO target delivery hour, derive historical price lags only from source values that are provably available by the applicable forecast cutoff.

The approved January common candidate features include:

- `hour_of_day`;
- `day_of_week`;
- `is_weekend`;
- `day_ahead_price_lag_1d`; and
- `day_ahead_price_lag_1d_rolling_mean_24h`.

NYISO may additionally use `load_forecast_mw` after the P-7 timing path is regenerated and revalidated. Same-hour actual load, observed weather, target components, identifiers, and audit fields remain excluded from the strict operational predictor set.

## NYISO daylight-saving-time conventions

NYISO TB-064 documents the 25-hour fall-back day. The first 01:00 occurs in EDT and the second 01:00 occurs in EST; MIS Upload/Download identifies the repeated second hour as `HB25`.

NYISO TB-088 documents the 23-hour spring-forward day. `HB02` does not occur in MIS Upload/Download and the sequence advances from 01:00 EST to 03:00 EDT.

These rules are adopted at the documentation level. The project must still test actual 2020–2024 historical files and prove UTC uniqueness across transition dates before final modeling.
