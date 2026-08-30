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
- Raw NOAA LCDv2 `DATE` values use fixed Local Standard Time (UTC−05:00), not daylight-saving-adjusted market time; do not initially localize them as `America/New_York`.
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

**Last updated:** August 25, 2026

This document records methodological decisions for the electricity-price forecasting capstone. It distinguishes adopted decisions, conditional decisions, unresolved questions, and future actions.

## Decision-status definitions

| Status | Meaning |
|---|---|
| Adopted | Supported by available evidence and currently governs implementation. |
| Conditional | Approved for pilot use but requires additional evidence before final 2020–2024 modeling. |
| Under investigation | No final decision has been made. |
| Future action | A required validation, implementation, or documentation task. |

## M-01: Research design

**Status:** Adopted

The project will forecast hourly day-ahead electricity prices separately for:

- PJM PSEG pricing zone; and
- NYISO Hudson Valley Zone G.

Model performance will be compared using consistent metrics and evaluation periods. Market-specific predictors will not be forced into false equivalence.

January 2025 is a feasibility and pipeline-development period. The planned primary study period is January 1, 2020 through December 31, 2024.

## M-02: Price targets and location identifiers

**Status:** Adopted

### PJM

- Location: PSEG zone.
- Pricing node: `51301`.
- Paired metered-load area: `PS`.
- Source target field: `total_lmp_da`.
- Unit: `$/MWh`.

PJM directly confirmed that node `51301` is the appropriate PSEG zone-level pricing node to pair with the `PS` metered-load area. Public PJM LMP documentation establishes that total LMP contains the energy, congestion, and marginal-loss components. The component fields must not be added to `total_lmp_da` a second time.

### NYISO

- Location: Hudson Valley Zone G.
- Location name: `HUD VL`.
- PTID: `61758`.
- Source target field: `LBMP ($/MWHr)`.
- Unit: `$/MWh`.

NYISO directly confirmed that PTID `61758` is the appropriate identifier for both Hudson Valley zonal day-ahead LBMP and actual zonal load.

## M-03: Canonical timestamps

**Status:** Adopted

All processed datasets use `timestamp_utc` as the canonical field for:

- joins;
- chronological ordering;
- duplicate detection;
- validation;
- train/validation/test splitting; and
- modeling.

Timezone-aware local timestamps are retained for market interpretation, calendar features, cutoff construction, and reporting.

### Market timestamps

PJM and NYISO market-local timestamps are interpreted using `America/New_York`, which follows Eastern Prevailing Time and daylight-saving transitions.

### NOAA observation timestamps

Raw NOAA LCDv2 `DATE` values are different. LCDv2 observations are reported in Local Standard Time without daylight-saving adjustment. For Newark and Stewart, raw LCDv2 time is fixed UTC−05:00.

The raw NOAA timestamp must initially be localized as fixed standard time, for example:

```python
weather["timestamp_utc"] = (
    pd.to_datetime(weather["DATE"])
      .dt.tz_localize("Etc/GMT+5")
      .dt.tz_convert("UTC")
)
```

Do not initially localize raw LCDv2 `DATE` values as `America/New_York`; doing so would shift summer observations incorrectly.

For January 2025, both approaches happen to align because January is in Eastern Standard Time. This does not make the approaches equivalent for the full 2020–2024 period.

## M-04: Forecast origins and information cutoffs

**Status:** Adopted for cutoff construction; source availability remains conditional where noted

### PJM cutoff

PJM uses system conditions, including forecasts, as of 11:00 a.m. EPT when calculating Day-Ahead Market results.

The project will use a conservative leakage-control rule:

```text
forecast_available_at < 11:00 a.m. EPT on the day before delivery
```

A forecast timestamped exactly at 11:00 a.m. is excluded because the project cannot prove that it was available before the cutoff.

### NYISO cutoff

The NYISO Energy Marketplace timeline shows that the Day-Ahead Market closes at 5:00 a.m. EPT on the day before dispatch.

The project will use:

```text
forecast_available_at < 5:00 a.m. EPT on the day before delivery
```

A forecast timestamped exactly at 5:00 a.m. is excluded.

### Controlling leakage rule

Every predictor must have been available at the applicable market's forecast origin. Target-hour or later information is excluded from the operational model even when it improves retrospective accuracy.

## M-05: PJM historical load forecasts

**Status:** Adopted candidate predictor; implementation pending

- Historical feed: `load_frcstd_hist`.
- Forecast area: `MIDATL`.
- Vintage timestamp: prefer `evaluated_at_utc` for filtering and audit.
- Target timestamp: use `forecast_hour_beginning_utc`.
- Value: `forecast_load_mw`.

PJM confirmed that:

- MIDATL is the most geographically specific preserved historical forecast area covering PSEG;
- PSEG-only historical forecast detail is not available;
- the zones in the MIDATL region are rolled up in the historical feed;
- `evaluated_at_ept` is when the forecast was generated and made available; and
- the historical feed preserves forecasts every six hours starting one day before the effective date rather than every twice-hourly live revision.

MIDATL must be described as a regional proxy for PSEG demand, not as forecasted PSEG load.

**Future action:** Implement the PJM vintage-selection workflow and verify that each target hour has exactly one latest eligible MIDATL snapshot strictly before the 11:00 a.m. cutoff.

## M-06: NYISO historical load forecasts

**Status:** Conditional

NYISO directed the project to Markets → Load Data → NY Load Forecast → Custom Reports. The January pilot uses the public ISO Load Forecast (`isolf`) archive and selects the Hudson Valley field.

The January workflow:

1. retains every available forecast-vintage/target-hour row;
2. constructs the 5:00 a.m. cutoff for each delivery day;
3. excludes post-cutoff vintages;
4. selects the latest eligible vintage per target hour; and
5. merges the selected value one-to-one with the target electricity table.

The NYISO Energy Marketplace timeline places the NYISO Load Forecast posting after the 5:00 a.m. Day-Ahead Market close. Consequently, the operational experiment may use only an earlier forecast version that was already available before 5:00 a.m. The later same-day posting is not eligible for the 5:00 a.m. forecast origin.

The current archive does not provide a separately verified original publication timestamp in the implemented workflow. The ZIP entry's last-modified timestamp is therefore retained as a proxy:

```text
availability_basis = zip_entry_last_modified
availability_is_proxy = True
```

`load_forecast_mw` is conditionally approved for January pipeline development. It is not yet approved as a final 2020–2024 operational predictor.

**Future action:** Locate an authoritative NYISO issuance or publication timestamp, verify that every selected vintage was published before 5:00 a.m., validate the proxy against the authoritative timestamp, or exclude the affected forecast feature from the final operational model.

## M-07: Actual load

**Status:** Adopted exclusion for the operational model

The current PJM `PS` and NYISO Hudson Valley load files contain actual, metered, or integrated load.

Same-hour target-period actual load is unavailable when a day-ahead prediction is made. It will not be used directly as an operational day-ahead predictor.

Actual load may be used for:

- feasibility EDA;
- descriptive correlation analysis;
- an explicitly non-operational explanatory model; or
- lagged features whose values were available before the applicable cutoff.

Actual-load correlations must not be interpreted as evidence that target-hour actual load is a deployable predictor.

## M-08: NOAA stations and geographic interpretation

**Status:** Adopted with limitation

- Newark Liberty International Airport: `USW00014734`.
- New York Stewart International Airport: `USW00014714`.
- Applicable Weather Forecast Office: OKX.

NOAA explained that whether a single station represents a broad region is subjective. Newark and Stewart are retained as defensible point observations near the selected market areas, but neither is assumed to represent every location or weather condition within its entire electricity-pricing zone.

**Future action:** Review both stations' HOMR histories for location, equipment, reporting, or instrumentation changes during 2020–2024. Record any change that could create a structural break.

## M-09: NOAA dataset, units, and study-period filtering

**Status:** Adopted

LCDv2 is the primary observed-weather source. NOAA described LCDv2 as a higher-quality-controlled presentation of GHCN-Hourly observations with additional parameters.

Bulk LCDv2 station-year files use SI units:

- dry-bulb temperature: degrees Celsius;
- dew point: degrees Celsius;
- relative humidity: percent;
- wind speed and gust speed: meters per second; and
- precipitation: millimeters where reported.

No Fahrenheit-to-Celsius or mph-to-m/s conversion is applied.

The supplied weather files are station-year files even though their filenames contain `Jan25`. The modeling pipeline must filter by timestamp rather than filename:

```python
weather = weather.loc[
    (weather["DATE"] >= "2025-01-01") &
    (weather["DATE"] < "2025-02-01")
]
```

## M-10: NOAA report-type selection

**Status:** Adopted for the primary observed-weather series; sensitivity analysis optional

The raw station-year files contain sub-hourly, hourly, daily, and monthly records. They must not be treated as one already-hourly modeling table.

Primary rule:

- use `FM-15` routine METAR observations as the first-choice hourly source;
- use `FM-12` fixed-station SYNOP observations as the second-choice fallback;
- use `FM-16` special aviation observations as the third-choice fallback;
- exclude `SOD` and `SOM` summary rows; and
- select the lowest-priority-numbered eligible report within each local hour before reindexing to the complete January calendar;
- preserve the original observation timestamp until the hourly alignment rule is applied.

**Future action:** If time permits, perform a sensitivity analysis comparing the primary FM-15 rule with a documented FM-15/FM-16 combination.

## M-11: NOAA missing values, flags, and physical validation

**Status:** Adopted

- Blank values remain missing; they are not automatically replaced with zero.
- Blank hourly precipitation means missing or unreported.
- Precipitation `0` means measured with no precipitation.
- Trace precipitation is retained separately from zero.
- Suspect (`s`) and erroneous (`*`) indicators are preserved before numeric conversion.
- Raw values and `REM` text are retained for audit when practical.
- Blanket `fillna(0)` is prohibited.
- Backward filling is prohibited because it imports future information.
- Forward filling is permitted only within a documented maximum gap and only when the previous observation was genuinely available.

Project-level physical checks include:

- plausible temperature range;
- plausible dew-point range;
- relative humidity between 0% and 100%;
- dew point not materially above temperature;
- plausible wind-speed range; and
- cross-checking questionable records against `REM`.

Invalid observations are converted to missing rather than guessed or silently corrected.

## M-12: Weather predictors and leakage

**Status:** Observed-weather rule adopted; archived forecast source under investigation

LCDv2 contains observations, not archived day-ahead forecasts.

Same-hour target-day observed weather may be used for:

- EDA;
- explaining price behavior; or
- an explicitly labeled observed-weather or upper-bound model.

It must not be presented as an operational day-ahead predictor.

The operational model may use:

- archived weather forecasts issued before the market cutoff; or
- sufficiently lagged observed weather demonstrably available before the cutoff.

NOAA identified SRRS and NOAAPort as archived text-product interfaces and FPUS5 and FXUS6 as relevant text products. These sources have not yet been shown to provide a consistent structured hourly temperature forecast for both stations throughout 2020–2024.

**Future action:** Determine whether a reproducible archived forecast product can supply issuance time, valid time, location, and forecast value. If not, exclude contemporaneous weather from the core operational model and use lagged observations only where defensible.

## M-13: Lagged and rolling features

**Status:** Adopted

Every price, load, or weather lag must be available at the forecast origin for all 24 next-day target hours.

Rolling features must shift before rolling so that the target and future values are excluded. A one-hour lag is not automatically safe when all next-day hours are predicted before the operating day.

Each engineered feature must have a documented:

- source field;
- lag or window;
- availability rule;
- forecast origin; and
- role as predictor, target, audit-only field, or exclusion.

## M-14: Data splitting and preprocessing

**Status:** Adopted

- Random train/test splitting is prohibited.
- Training, validation, and test periods follow chronological order.
- Time-series cross-validation or rolling-origin evaluation is used for tuning.
- Scaling, imputation, encoding, and feature selection are fit on training data only.
- The final test period remains untouched until model and feature choices are complete.

A candidate full-period split is:

- training: 2020–2022;
- validation and tuning: 2023; and
- final test: 2024.

The exact split will be finalized after full-period coverage and structural changes are validated.

## M-15: Price outliers and metrics

**Status:** Adopted

- Negative prices and price spikes are legitimate market outcomes and are retained.
- Prices are not deleted or winsorized without documented evidence of a data error.
- Primary metrics are MAE and RMSE.
- MAPE is not a primary metric because prices may be zero or negative.
- Performance is also examined by market, hour, weekday, season, negative-price periods, and high-price periods.

## M-16: Final PJM price-feed selection

**Status:** Under investigation

The January pilot uses `da_hrl_lmps`. Public PJM documentation indicates that settlements-verified `rt_da_monthly_lmps` contains final day-ahead LMPs.

**Future action:** Before downloading the final 2020–2024 price series, decide whether to:

1. use `rt_da_monthly_lmps` as the final historical price source; or
2. use `da_hrl_lmps` and reconcile it against the settlements-verified feed.

The selected rule must be applied consistently across all study years.

## M-17: Historical consistency and structural changes

**Status:** Future action

PJM reported no 2020–2024 changes that would affect its historical forecasts. This does not eliminate the need to validate other market and data changes.

Before bulk modeling, audit:

- PSEG node `51301` effective and termination dates;
- presence and meaning of the `PS` load area;
- MIDATL historical forecast coverage and schema;
- the September 1, 2021 PJM fast-start-pricing change as a possible price-series structural break;
- NYISO PTID `61758` continuity;
- NYISO daylight-saving representation under Technical Bulletin TB-064;
- NOAA station-history changes; and
- feed field names, units, versions, and revision behavior by year.

## M-18: Source privacy and citation

**Status:** Adopted

- Raw PJM and NYISO correspondence must not be committed to the public repository when it contains personal contact information, full mail headers, or confidentiality labels.
- The PJM response is referenced as `PJM Case 00334055, received 2026-08-21`.
- Public technical pages are cited whenever they support the same conclusion.
- Private correspondence is summarized without publishing personal contact details.
- Local reference files belong in a private or gitignored reference location.

## M-19: Model-comparison depth and interpretability

**Status:** Adopted

The final model comparison will include:

- a feature-ablation comparison between the common calendar-and-availability-safe-price-history feature set and the NYISO augmented set that adds `load_forecast_mw`; and
- error reporting by hour of day, weekday/weekend, and normal-price versus extreme-price regimes in addition to overall MAE and RMSE.

For an ablation, hold the model class, chronological split, preprocessing, and metrics fixed; change only the feature set. The NYISO augmented result remains conditional because its current forecast-availability evidence is a ZIP-entry proxy.

Define any price-regime threshold using training data only. Preserve negative and high prices; do not delete, winsorize, or classify observations with information from the final test set.

**Time-permitting additions:** assess feature-importance stability across chronological validation folds and include a concise bounded-tuning diagnostic. These additions do not authorize new primary model families or final-test-driven choices.

## Future-change protocol

When later evidence changes a decision:

1. do not silently overwrite the earlier rationale;
2. add the new evidence and date;
3. mark the prior decision as superseded;
4. identify affected notebooks, functions, datasets, and model results;
5. rebuild derived data where necessary;
6. rerun tests and notebooks from a clean kernel; and
7. update `PROJECT_PLAN.md`, `current_status.md`, `data_source_register.md`, and `data_dictionary.md` in the same change set.
## NYISO January 2025 historical day-ahead price features

For each NYISO target delivery hour, use the existing provisional prediction cutoff of D−1 05:00 America/New_York.

For the January 2025 feasibility implementation, assign each day-ahead price schedule a configurable provisional availability time of 00:00 America/New_York on its delivery date. This is an explicit project assumption, not verified NYISO publication evidence.

Create a prior-day same-hour source timestamp by subtracting one calendar day from the target’s local timestamp. Retain the source price only when:

`previous_day_same_hour_price_available_at <= prediction_cutoff`

Store the source timestamp, raw source value, source availability time, and Boolean eligibility result as audit fields. The approved `day_ahead_price_lag_1d` feature is the raw source value masked to missing when that condition is false.

Create `day_ahead_price_lag_1d_rolling_mean_24h` only from the already cutoff-safe lag feature, require a full 24-value window, and do not use the current target price as an input.

Fresh-kernel January verification produced 744 target hours, 720 cutoff-safe prior-day lags, and 697 full-window rolling means. The 24 missing prior-day lag values are the January 1 boundary, which lacks December 31 source data in this feasibility sample.

This price-schedule availability assumption is independent of the NYISO load-forecast ZIP-entry last-modified-time proxy. The proxy warning remains active and must not be removed or treated as authoritative availability evidence.
