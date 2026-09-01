# Electricity Price Forecasting Capstone — Project Plan

**Last updated:** September 1, 2026  
**Current phase:** Full-period source-continuity and acquisition preparation

## 1. Project overview

This capstone will develop, evaluate, and compare statistical and machine-learning models for forecasting hourly day-ahead electricity prices in:

- PJM PSEG pricing zone; and
- NYISO Hudson Valley Zone G.

January 2025 is the feasibility and pipeline-development sample. The planned primary study period is January 1, 2020 through December 31, 2024.

## 2. Research question

> How accurately can statistical and machine-learning models forecast hourly day-ahead electricity prices, and how does predictive performance differ between PJM PSEG and NYISO Hudson Valley Zone G?

## 3. Markets, targets, and identifiers

| Market | Location | Identifier | Target | Unit |
|---|---|---|---|---|
| PJM | PSEG zone | pnode `51301`; paired load area `PS` | `total_lmp_da` | `$/MWh` |
| NYISO | Hudson Valley Zone G | `HUD VL`, PTID `61758` | published day-ahead LBMP | `$/MWh` |

The unit of analysis is one market-location-hour. PJM and NYISO are modeled separately and compared with consistent out-of-sample metrics.

## 4. Canonical time and forecast origins

`timestamp_utc` is the canonical join, ordering, validation, split, and modeling key. Timezone-aware market-local timestamps are retained for interpretation and calendar features.

| Market | Operational cutoff | Project eligibility rule |
|---|---|---|
| PJM | 11:00 a.m. EPT on D−1 | Predictor must be available strictly before 11:00 a.m. |
| NYISO | 5:00 a.m. EPT on D−1 | Predictor must be available strictly before 5:00 a.m. |

Every operational predictor must have been available at the applicable cutoff. Same-hour actual load and same-hour observed weather are excluded from the strict operational predictor set unless a safe lag or archived forecast is demonstrated.

## 5. January 2025 feasibility checkpoint

Completed:

- 744 unique hourly target rows for PJM and NYISO;
- cleaned and merged price/load tables;
- NOAA hourly weather reconciliation;
- NYISO forecast-vintage reconstruction with 4,464 vintage/target-hour rows;
- latest-eligible NYISO vintage selection and merge;
- calendar features;
- cutoff-safe historical price lags and rolling features;
- explicit predictor/audit/identifier/excluded field roles;
- January modeling-ready checkpoint exports;
- notebook execution and automated validation.

January remains a pipeline-development sample and is not final capstone evidence.

## 6. PJM source status

### Resolved

- PSEG pnode `51301` selected as the price location.
- `PS` selected as the paired metered-load area.
- Historical load forecasts use `load_frcstd_hist`.
- `MIDATL` is the narrowest preserved historical forecast area covering PSEG and is a regional proxy, not PSEG-specific forecast load.
- PJM confirmed `evaluated_at_ept` is when a historical forecast was generated and made available.
- Historical feed preserves six-hour snapshots.
- Project cutoff is latest eligible forecast strictly before 11:00 a.m. EPT D−1.

### Remaining PJM work

- acquire 2020–2024 `load_frcstd_hist` MIDATL data;
- verify pnode `51301`, `PS`, and MIDATL continuity by year;
- decide whether the final historical price series uses or is reconciled against `rt_da_monthly_lmps`;
- test Data Miner timestamp behavior across DST transitions; and
- evaluate September 1, 2021 fast-start pricing as a possible structural break.

PJM no longer has a major unresolved external-source question.

## 7. NYISO source status

### Resolved

- Hudson Valley location: `HUD VL`, PTID `61758`.
- Historical price/load source: NYISO MIS public archive.
- Historical load-forecast route: ISO Load Forecast archive / NY Load Forecast Custom Reports.
- Day-Ahead Market cutoff: 5:00 a.m. EPT D−1.
- NYISO TB-064 documents the 25-hour fall-back transition and `HB25` representation.
- NYISO TB-088 documents the 23-hour spring-forward transition and missing `HB02`.
- DST is resolved at the documentation level; only implementation/testing remains.

### Remaining NYISO external-source question

The January forecast workflow currently uses ZIP-entry last-modified time as a proxy for public availability:

```text
availability_basis = zip_entry_last_modified
availability_is_proxy = True
```

The remaining question is whether NYISO preserves an authoritative historical issuance/publication/public-availability timestamp for each short-term ISO Load Forecast vintage.

If an authoritative timestamp exists, validate and replace the proxy where appropriate. If no authoritative timestamp is retained, exclude `load_forecast_mw` from the strict operational model and retain it only in a clearly labeled conditional/sensitivity analysis.

This issue does **not** block the full 2020–2024 capstone.

### Remaining NYISO work

- acquire 2020–2024 LBMP, integrated load, and load-forecast files;
- verify `HUD VL` / PTID `61758` continuity;
- validate annual schemas and archive conventions;
- compare Custom Reports and `isolf` where helpful; and
- test every historical spring/fall transition against TB-064/TB-088 behavior.

## 8. NOAA status

- Newark station: `USW00014734`.
- Stewart station: `USW00014714`.
- LCDv2 is the primary observed-weather source.
- Bulk station-year CSVs use SI units.
- Raw `DATE` values use fixed Local Standard Time without DST.
- Blank precipitation means missing/unreported, not zero.
- Same-hour observed weather is descriptive only unless operational timing is established.

Remaining NOAA work:

- acquire 2020–2024 station-year files;
- audit both station histories in HOMR; and
- decide whether a reproducible archived weather-forecast feature is feasible.

## 9. Predictor status

| Predictor | Status | Rule |
|---|---|---|
| Calendar features | Approved | Known before cutoff |
| Cutoff-safe historical price lags | Approved | Explicit availability test required |
| PJM MIDATL historical load forecast | Approved candidate | Latest eligible snapshot strictly before 11:00 a.m. |
| NYISO `load_forecast_mw` | Conditional | Latest eligible vintage strictly before 5:00 a.m.; availability currently proxy-based |
| Same-hour actual load | Excluded operationally | EDA or safe lag only |
| Same-hour observed weather | Excluded operationally | EDA/upper-bound only |
| Archived weather forecast | Under investigation | Must preserve issue time, valid time, and vintage |
| Natural-gas price | Optional | Publication timing must be documented |

## 10. Planned models

Primary model comparison:

1. persistence/historical-average baseline;
2. regularized linear regression such as Ridge or Elastic Net;
3. Random Forest regression; and
4. gradient-boosted tree regression such as XGBoost.

A simple unregularized linear regression may be included as an interpretable reference. Neural networks are not required for the primary capstone.

## 11. Validation strategy

- Chronological splitting only.
- Rolling-origin or expanding-window validation for tuning.
- Fit preprocessing on training data only.
- Preserve an untouched final test period.
- Primary metrics: MAE and RMSE.
- MAPE is not a primary metric because prices may be zero or negative.

Candidate split, subject to final coverage review:

- training: 2020–2022;
- validation/tuning: 2023;
- final test: 2024.

## 12. Full-period implementation checklist

Before final modeling:

1. validate PSEG pnode `51301`, `PS`, MIDATL, `HUD VL`, and PTID `61758` across every study year;
2. acquire all final 2020–2024 market datasets with provenance records;
3. resolve the NYISO authoritative forecast-availability timestamp if possible;
4. if unresolved, remove NYISO `load_forecast_mw` from the strict operational feature set;
5. implement PJM MIDATL latest-eligible selection using `evaluated_at` and the strict pre-11:00 rule;
6. implement/test NYISO TB-064 and TB-088 handling against actual transition-day files;
7. test PJM DST behavior in Data Miner fields;
8. audit NOAA station histories and fixed-standard-time conversion;
9. decide the final PJM historical price feed;
10. audit annual schemas, units, revisions, and missingness;
11. evaluate the PJM fast-start pricing change as a structural break; and
12. rerun all cleaning, feature engineering, validation, and leakage checks before final model training.

## 13. Risk handling

| Risk | Treatment |
|---|---|
| NYISO forecast availability cannot be authoritatively reconstructed | Exclude `load_forecast_mw` from strict model; optionally retain conditional sensitivity model |
| Historical identifier/schema change | Detect during annual continuity audit; document and adapt reproducibly |
| DST ambiguity | Use UTC canonical key and test actual transition-day files |
| Weather forecast archive impractical | Use only leakage-safe historical/weather features or omit operational weather |
| PJM price-method structural change | Analyze pre/post fast-start pricing and report limitation |
| Missing or revised source data | Preserve provenance, missingness, versions, and source-specific limitations |

## 14. Documentation governance

Authoritative project documentation:

- `docs/current_status.md` — short current-state handoff;
- `docs/methodology_decisions.md` — methodological decisions and rationale;
- `docs/data_source_register.md` — source evidence and limitations;
- `docs/data_dictionary.md` — fields, units, roles, and timestamp rules;
- `docs/notebook_pipeline_map.md` — high-level data/notebook flow; and
- `docs/learning_log.md` — learning and reproducibility notes.

Private correspondence must remain outside the public repository when it includes personal information, mail headers, or confidentiality language.

## 15. Immediate next action

Begin the 2020–2024 source-continuity and acquisition audit. Validate identifiers, annual schemas, timestamp conventions, and forecast coverage before final multiyear feature generation or model fitting.
