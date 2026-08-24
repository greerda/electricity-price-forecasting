# Decision Log

Detailed reasoning lives in `docs/methodology_decisions.md`. This table is the dated index of decisions that affect implementation.

| ID | Date | Decision | Status |
|---|---|---|---|
| D-001 | 2026-08-24 | Use PJM PSEG pnode 51301 and NYISO HUD VL/PTID 61758; model markets separately. | Active |
| D-002 | 2026-08-24 | Use `day_ahead_price_usd_mwh` as the canonical target name and `actual_load_mw` for observed target-hour load. | Active; modules must be reconciled in Task 2 |
| D-003 | 2026-08-24 | Use `timestamp_utc` for joins/order/splits and timezone-aware `timestamp_local` for interpretation/calendar features. | Active |
| D-004 | 2026-08-24 | Use NYISO D−1 05:00 America/New_York as the provisional cutoff and select the latest eligible vintage. | Active, provisional |
| D-005 | 2026-08-24 | Preserve `availability_is_proxy=True` for all current NYISO selections because ZIP-entry modification time is not an authoritative publication timestamp. | Active limitation |
| D-006 | 2026-08-24 | Use PJM D−1 11:00 America/New_York as a configurable provisional cutoff while authoritative confirmation is absent. | Active, provisional |
| D-007 | 2026-08-24 | Exclude same-hour actual load, observed weather, target components, identifiers, and forecast audit fields from operational predictors. | Active |
| D-008 | 2026-08-24 | Require forecast-origin-aware availability tests before approving historical lags or rolling features. | Active |
| D-009 | 2026-08-24 | Treat the downloaded NOAA LCD values as SI and reconcile reusable code to Notebook 02's selection and audit policy. | Active; implementation pending Task 2 |
| D-010 | 2026-08-24 | Proceed without blocking on unanswered ISO correspondence; keep assumptions conservative, testable, configurable, and explicitly provisional. | Active |
| D-011 | 2026-08-24 | Complete the seven pre-modeling tasks before baseline model development. | Active |

When a decision changes, add a new row that identifies the replaced decision rather than silently rewriting the historical rationale.
