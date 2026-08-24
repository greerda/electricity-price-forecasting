# Methodology Decisions

**Last updated:** August 24, 2026

This file records decisions that govern the current implementation. A statement marked **provisional** is a conservative, testable project assumption rather than a verified market rule.

## Scope and targets

- Model PJM PSEG and NYISO Hudson Valley separately, then compare performance using consistent metrics and evaluation periods.
- Use one market-location-hour as the unit of analysis.
- Use hourly day-ahead total price in `$/MWh` as the target.
- Use PSEG pnode 51301 for PJM and HUD VL/PTID 61758 for NYISO.
- Treat January 2025 as a feasibility sample, not the final evidence base.

## Canonical schema

The committed processed-table names are authoritative:

- `day_ahead_price_usd_mwh` — supervised target;
- `actual_load_mw` — target-hour actual/metered or integrated load;
- `load_forecast_mw` — forecast-vintage load predictor when cutoff eligibility is proven;
- `timestamp_utc` — canonical join, ordering, validation, splitting, and modeling key; and
- `timestamp_local` — timezone-aware local time used for calendar derivation and interpretation.

Reusable modules and configuration must be reconciled to these names during Task 2. Do not maintain two competing schemas.

## Time handling

- Interpret PJM and NYISO local timestamps with `America/New_York`.
- Retain both timezone-aware local and UTC timestamps.
- Never convert Eastern time by manually subtracting five hours.
- Validate daylight-saving transitions explicitly when expanding beyond January.
- Confirm whether each source is hour-beginning or hour-ending before joining it.

## Forecast origins

### NYISO

- **Provisional operational cutoff:** D−1 05:00 `America/New_York` for every target hour on delivery day D.
- Select the latest load-forecast vintage whose availability timestamp is less than or equal to the cutoff.
- Current January availability is reconstructed from ZIP-entry last-modified time.
- Preserve `availability_is_proxy=True` and `availability_basis="zip_entry_last_modified"`.
- Do not present the proxy as an authoritative NYISO publication timestamp.

### PJM

- **Provisional operational cutoff:** D−1 11:00 `America/New_York` for every target hour on delivery day D.
- Continue without waiting for a PJM reply, but keep the cutoff configurable and visibly provisional.
- Current PS load is metered actual load and is not a day-ahead predictor.
- If a historical PJM load-forecast series is acquired, retain all vintages and apply the same latest-eligible selection pattern used for NYISO.

## Predictor roles

### Approved before modeling

- calendar values derived from the target operating hour;
- a forecast vintage whose availability is proven to precede the cutoff; and
- historical price/load/weather features only when an explicit availability rule and automated test prove they were knowable at the forecast origin.

### Excluded from operational predictors

- `day_ahead_price_usd_mwh` and same-hour target components;
- same-hour `actual_load_mw`;
- same-hour observed weather;
- forecast audit/provenance fields;
- identifiers and source labels;
- post-cutoff forecast vintages; and
- any lag or rolling value validated only by row position rather than information availability.

Actual load and observed weather may remain in the analysis table for EDA and diagnostics, provided they are labeled descriptive or excluded.

## Comparable feature sets

Use two clearly labeled experiments if market inputs differ:

1. **Common feature set:** only features available and defensible in both markets.
2. **Market-augmented feature set:** additional valid market-specific predictors, such as NYISO `load_forecast_mw`.

Do not silently substitute PJM metered load for a missing PJM day-ahead load forecast.

## NOAA weather policy

The currently downloaded NOAA LCD exports used by Notebook 02 already contain SI values:

- temperature and dew point in degrees Celsius;
- relative humidity in percent; and
- wind speed in meters per second.

Do not apply Fahrenheit-to-Celsius or miles-per-hour-to-meters-per-second conversion to these files. During Task 2, make the reusable module match the notebook's report-type priority, hourly selection, plausible-range rejection, and audit-flag behavior.

## Missingness and extremes

- Reindex to the complete expected hourly calendar so missing source observations remain visible.
- Do not use future-looking interpolation.
- Retain legitimate negative and high electricity prices.
- Do not delete or winsorize target values without a separately documented methodological reason.
- Preserve NOAA quality and rejection flags.

## Validation and evaluation

- Require one row per market-location-hour after the pre-modeling merge.
- Use one-to-one validation where one row is expected on both sides.
- Use chronological, never random, train/validation/test splits.
- Fit all learned preprocessing on training data only.
- Keep the final test period untouched until model design is complete.
- Use MAE as the primary metric and RMSE as the secondary metric; treat MAPE cautiously because prices can be zero or negative.

## Change rule

An authoritative PJM, NYISO, NOAA, syllabus, or professor source may replace a provisional assumption. Record the source, date, affected code/configuration, and rerun requirements in this file and `docs/decisions.md`.
