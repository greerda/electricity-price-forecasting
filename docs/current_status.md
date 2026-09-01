# Current Status — Electricity Price Forecasting Capstone

**Last verified:** August 31, 2026  
**Current phase:** January 2025 pre-modeling completion gate complete; preparing full 2020–2024 implementation

## Project scope

- Research question: How accurately can statistical and machine-learning models forecast hourly day-ahead electricity prices, and how does performance differ between PJM PSEG and NYISO Hudson Valley Zone G?
- PJM target: PSEG zone, pnode `51301`, hourly day-ahead total LMP.
- NYISO target: Hudson Valley Zone G, `HUD VL`, PTID `61758`, hourly day-ahead LBMP.
- Unit of analysis: one market-location-hour.
- Canonical modeling key: timezone-aware `timestamp_utc`.
- Market interpretation/calendar key: timezone-aware `timestamp_local`.
- January 2025 is a 744-hour feasibility and pipeline-development sample only.
- Planned primary study period: January 1, 2020 through December 31, 2024.
- Raw files remain immutable.

## Verified January 2025 pipeline status

- `notebooks/02_data_cleaning.ipynb` produces 744-row PJM and NYISO processed electricity tables.
- NOAA weather is reduced to a complete hourly index while preserving missingness, quality, rejection, and imputation indicators.
- `data/interim/nyiso_hudson_valley_load_forecast_vintages.csv` contains 4,464 forecast-vintage/target-hour rows covering 744 target hours.
- NYISO latest-eligible vintage selection and one-to-one merge are implemented.
- Calendar features and cutoff-safe historical-price features are implemented for both markets.
- Same-hour actual load, observed weather, target components, identifiers, and audit fields are excluded from the strict operational predictor set.
- January modeling-ready checkpoint files have 744 unique ordered target hours per market.
- The January feasibility pipeline has passed notebook execution, pytest, Ruff, role-overlap checks, and prohibited-predictor checks.

## PJM source-validation status

### Resolved

- PSEG pricing location: pnode `51301`.
- Paired metered-load area: `PS`.
- Historical load-forecast feed: `load_frcstd_hist`.
- Historical forecast geography: `MIDATL`, explicitly treated as a regional proxy rather than a PSEG-specific forecast.
- PJM confirmed that `evaluated_at_ept` represents when the historical forecast was generated and made available.
- Historical feed preserves six-hour snapshots rather than every live twice-hourly revision.
- Conservative project cutoff: latest eligible forecast strictly before 11:00 a.m. EPT on D−1.

### Remaining PJM implementation/continuity work

- Acquire and validate the 2020–2024 `load_frcstd_hist` MIDATL series.
- Verify PSEG pnode `51301`, `PS`, and MIDATL continuity across all study years.
- Decide whether the final historical price target will use or be reconciled against settlements-verified `rt_da_monthly_lmps`.
- Validate actual Data Miner timestamp behavior across spring and fall DST transitions.
- Treat the September 1, 2021 fast-start-pricing change as a possible structural break and test it explicitly.

PJM no longer has a major unresolved external-source question. Remaining work is primarily data acquisition, implementation, and continuity validation.

## NYISO source-validation status

### Resolved

- Hudson Valley target location: `HUD VL`, PTID `61758`.
- Historical price/load route: NYISO MIS public archive.
- Historical load-forecast route: ISO Load Forecast archive / NY Load Forecast Custom Reports.
- Day-Ahead Market cutoff: 5:00 a.m. EPT on D−1.
- Conservative project rule: predictor availability must be strictly before 5:00 a.m.
- NYISO Technical Bulletin TB-064 documents the 25-hour fall-back transition and repeated second 01:00 hour (`HB25` in MIS Upload/Download).
- NYISO Technical Bulletin TB-088 documents the 23-hour spring-forward transition and omission of `HB02` in MIS Upload/Download.
- DST is resolved at the documentation level. Remaining DST work is implementation and testing against actual 2020–2024 files.

### Remaining NYISO external-source question

The January 2025 workflow uses the archive ZIP-entry last-modified timestamp as the forecast-availability proxy:

```text
availability_basis = zip_entry_last_modified
availability_is_proxy = True
```

The remaining question is whether NYISO preserves an authoritative historical issuance/publication/public-availability timestamp for each short-term ISO Load Forecast vintage.

If NYISO identifies an authoritative field or archive convention, validate the proxy and replace it where appropriate. If NYISO confirms that no authoritative historical availability timestamp is retained, exclude `load_forecast_mw` from the strict operational model and retain it only in a clearly labeled conditional or sensitivity analysis.

### Remaining NYISO implementation/continuity work

- Acquire and validate 2020–2024 LBMP, integrated load, and historical load-forecast data.
- Verify `HUD VL` / PTID `61758` continuity and annual schema/field conventions.
- Compare ISO Load Forecast archive output with Custom Reports where useful.
- Test every spring-forward and fall-back transition in the actual historical files against TB-064/TB-088.

## NOAA status

- Newark station: `USW00014734`.
- Stewart station: `USW00014714`.
- LCDv2 is the primary observed-weather source.
- Raw LCDv2 `DATE` uses fixed Local Standard Time, not DST-adjusted market time.
- Bulk station-year CSV files use SI/metric units.
- Blank hourly precipitation means missing/unreported, not zero.
- Same-hour observed weather is excluded from the strict operational model unless an operationally available forecast or safe lag is demonstrated.
- Full-period HOMR station-history audits remain required.

## Key modeling limitation

The unresolved NYISO load-forecast publication timestamp is a **feature limitation, not a project blocker**. The full 2020–2024 capstone can proceed using common leakage-safe predictors. If necessary, the strict NYISO operational model will omit `load_forecast_mw` while a separately labeled conditional model may test it.

## Exact next action

Begin the full-period source-continuity and acquisition audit for 2020–2024, starting with market identifiers, schemas, timestamp conventions, and historical forecast coverage before final model fitting.
