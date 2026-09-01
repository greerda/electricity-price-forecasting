# Current Status — Electricity Price Forecasting Capstone

**Last verified:** September 1, 2026  
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
- NYISO latest-eligible vintage selection and one-to-one merge are implemented, but the January forecast timing must now be regenerated using P-7 `Last Updated` metadata rather than ZIP-only timing.
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

### Resolved / adopted

- Hudson Valley target location: `HUD VL`, PTID `61758`.
- Historical price/load route: NYISO MIS public archive.
- Historical load-forecast product: P-7 ISO Load Forecast / `isolf`.
- Historical P-7 files contain rolling multi-day zonal forecasts, including `HUD VL`.
- The public P-7 interface pairs each dated forecast artifact with a timezone-specific `Last Updated` timestamp.
- The project will treat P-7 `Last Updated` as the best available public-source evidence of forecast availability.
- This interpretation is explicitly documented as an inference from NYISO's public interface rather than a direct NYISO confirmation of the field's formal publication semantics.
- Day-Ahead Market cutoff: 5:00 a.m. EPT on D−1.
- Conservative project rule: predictor availability must be strictly before 5:00 a.m.
- NYISO Technical Bulletin TB-064 documents the 25-hour fall-back transition and repeated second 01:00 hour (`HB25` in MIS Upload/Download).
- NYISO Technical Bulletin TB-088 documents the 23-hour spring-forward transition and omission of `HB02` in MIS Upload/Download.
- DST is resolved at the documentation level. Remaining DST work is implementation and testing against actual 2020–2024 files.

### P-7 availability rule

The project will use:

```text
availability_basis = p7_last_updated
availability_is_proxy = True
```

Here `availability_is_proxy=True` means **public-source inferred rather than operator-confirmed**. ZIP-entry last-modified timestamps should remain available as secondary audit/provenance values where possible.

For each target hour, select the latest P-7 vintage whose `Last Updated` timestamp is strictly before the 5:00 a.m. D−1 cutoff and whose multi-day horizon still includes the target hour.

Current P-7 examples show updates commonly around 7–8 a.m. on D−1. Therefore, the P-7 artifact whose first forecast date equals the target day will often be too late for the strict cutoff; an older multi-day P-7 vintage may still be eligible.

A narrow NYISO clarification remains useful but is no longer a blocker: whether `Last Updated` formally means the time the specific P-7 file became publicly available.

### Remaining NYISO implementation/continuity work

- Capture or reconstruct P-7 `Last Updated` metadata across 2020–2024.
- Regenerate January 2025 NYISO forecast-vintage timing using P-7 metadata and rerun leakage checks.
- Acquire and validate 2020–2024 LBMP, integrated load, and P-7 forecast data.
- Verify `HUD VL` / PTID `61758` continuity and annual schema/field conventions.
- Compare P-7/`isolf` output with Custom Reports where useful.
- Test every spring-forward and fall-back transition in actual historical files against TB-064/TB-088.

## NOAA status

- Newark station: `USW00014734`.
- Stewart station: `USW00014714`.
- LCDv2 is the primary observed-weather source.
- Raw LCDv2 `DATE` uses fixed Local Standard Time, not DST-adjusted market time.
- Bulk station-year CSV files use SI/metric units.
- Blank hourly precipitation means missing/unreported, not zero.
- Same-hour observed weather is excluded from the strict operational model unless an operationally available forecast or safe lag is demonstrated.
- Full-period HOMR station-history audits remain required.

## Readiness assessment

Both PJM and NYISO are ready for full 2020–2024 implementation work.

- PJM has stronger operator-confirmed historical forecast timing semantics.
- NYISO now has a defensible public-source timing rule based on P-7 `Last Updated`, with an explicit evidence caveat.
- The NYISO load-forecast feature no longer needs to be treated as likely excluded by default. It remains usable subject to implementation, full-period metadata coverage, and revision if NYISO later defines `Last Updated` differently.

## Exact next action

Update the NYISO forecast-ingestion/vintage-selection code to ingest P-7 `Last Updated` metadata, retain ZIP-entry timestamps as secondary provenance, regenerate the January forecast-vintage table, and rerun cutoff/leakage validation before full-period acquisition.
