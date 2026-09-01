# Data Source Register

**Last updated:** September 1, 2026

This register records modeling datasets, technical documentation, external confirmations, limitations, and required future validation. Raw datasets remain immutable. Private correspondence must not be published in the public repository.

## Modeling datasets

| Dataset | Provider/source | Market/location | Intended use | Current status | Remaining action |
|---|---|---|---|---|---|
| PJM Day-Ahead Hourly LMP | PJM Data Miner 2 `da_hrl_lmps` | PSEG pnode `51301` | PJM price target | January 2025 pilot validated | Decide whether final 2020–2024 history uses or is reconciled against settlements-verified prices |
| PJM Settlements Verified Hourly LMPs | PJM Data Miner 2 `rt_da_monthly_lmps` | PSEG | Candidate final PJM target source | Not yet acquired | Compare with `da_hrl_lmps` before bulk acquisition |
| PJM Hourly Load: Metered | PJM Data Miner 2 `hrl_load_metered` | `PS` load area | EDA and possible safe historical lags | January pilot validated; target-hour value excluded operationally | Validate `PS` coverage for every study year |
| PJM Historical Load Forecasts | PJM Data Miner 2 `load_frcstd_hist` | `MIDATL` regional forecast area | Leakage-safe PJM load-forecast feature | Source and timing definition validated by PJM; implementation pending | Acquire 2020–2024; select latest eligible snapshot strictly before 11:00 a.m. EPT D−1 |
| PJM Pricing Nodes | PJM Data Miner 2 | PSEG | Historical identity validation | Not yet audited across full period | Verify pnode `51301` effective/termination history across 2020–2024 |
| NYISO Hudson Valley Day-Ahead LBMP | NYISO MIS public archive | `HUD VL`, PTID `61758` | NYISO price target | January 2025 pilot validated | Acquire and validate 2020–2024 archive files and annual schema continuity |
| NYISO Hudson Valley Integrated Load | NYISO MIS public archive | `HUD VL`, PTID `61758` | EDA and possible safe lags | January pilot validated; target-hour value excluded operationally | Validate identifier continuity and annual schema |
| NYISO ISO Load Forecast archive | NYISO MIS `isolf` archive | Hudson Valley | Candidate NYISO load-forecast feature | January workflow implemented; ZIP entry last-modified time is only an availability proxy | Determine authoritative historical publication/availability timestamp if one exists; otherwise omit from strict operational model |
| NYISO NY Load Forecast Custom Reports | NYISO | Hudson Valley / zonal forecasts | Candidate authoritative route for historical forecast reconstruction | NYISO directed project here; exact field/revision semantics not fully established | Compare with `isolf` archive and determine whether an authoritative vintage availability timestamp is preserved |
| NOAA Newark LCDv2 | NOAA/NCEI | Station `USW00014734` | PJM-area observed-weather EDA and safe lags | January pilot validated | Acquire 2020–2024 station-year files and audit HOMR |
| NOAA Stewart LCDv2 | NOAA/NCEI | Station `USW00014714` | NYISO-area observed-weather EDA and safe lags | January pilot validated with quality filtering | Acquire 2020–2024 station-year files and audit HOMR |
| Archived NWS text products | NOAA/NWS | OKX / relevant forecast zones | Possible archived weather-forecast source | Under investigation | Determine whether reproducible issue-time/valid-time hourly features are feasible |
| Calendar variables | Derived | Both markets | Common leakage-safe predictors | Approved | Add remaining calendar features and document holiday calendar |
| Historical price features | Derived | Both markets | Common leakage-safe predictors | January cutoff-safe prior-day and rolling features implemented | Extend to full period and add automated leakage tests |

## Technical documentation and external confirmations

| Source | Provider | Date/status | Supports | Limitation / handling | Future action |
|---|---|---|---|---|---|
| PJM Data Miner response, Case `00334055` | PJM correspondence | Received 2026-08-21 | PSEG/PS pairing; `load_frcstd_hist`; MIDATL proxy; `evaluated_at_ept` meaning; six-hour snapshot retention; 11:00 a.m. system conditions | Private correspondence; do not publish raw message or personal data | Retain privately and cite public feed definitions where possible |
| PJM Day-Ahead timeline | PJM public knowledge | Current public reference | 11:00 a.m. EPT day-ahead timing | Does not itself prescribe academic leakage rules | Keep strict `< 11:00` as conservative project rule |
| PJM daylight-saving guidance | PJM public knowledge | Current public reference | 23-hour / 25-hour market-day behavior | Actual Data Miner field behavior still must be tested | Test 2020–2024 DST transition dates |
| PJM fast-start pricing | PJM public knowledge | Effective 2021-09-01 | Possible structural break in price formation | Not a forecast-source change | Include structural-break analysis/sensitivity |
| NYISO Energy Marketplace response, Case `00143873` | NYISO correspondence | Received 2026-08-07 | `HUD VL` / PTID `61758`; historical load-forecast route; market timing; DST references | Private correspondence; often points to public sources | Retain privately and cite public documentation |
| NYISO follow-up response, Case `00145063` | NYISO correspondence | Received 2026 | NYISO directed project to MT-201 NYMOC course materials and stated it cannot provide research-project consultation | Useful for documenting support boundary; contains private contact information | Ask only narrow technical source-definition/timestamp questions if needed |
| NYISO Energy Marketplace training | NYISO | 2026 training material | Day-ahead/real-time market concepts; load forecasting; 5:00 a.m. Day-Ahead Market close; load forecast posting context | Training material; not an authoritative historical archive data dictionary | Use for market timing/context |
| NYISO Technical Bulletin TB-064 | NYISO | 02/25/2026 | Fall DST transition; 25-hour day; repeated 01:00; `HB25` in MIS Upload/Download; GMT mapping | Current 2026 bulletin does not by itself prove identical handling in every 2020–2024 file | Validate actual historical transition-day files |
| NYISO Technical Bulletin TB-088 | NYISO | 02/25/2026 | Spring DST transition; 23-hour day; no `HB02` in MIS Upload/Download; GMT mapping | Current 2026 bulletin; historical files still require empirical validation | Validate actual historical transition-day files |
| NYISO Load Forecasting Manual M-06, Version 5.1 | NYISO | Effective 10/27/2025 | ICAP/capacity load-forecasting methodology, weather normalization, data submission, revision history | Does not establish short-term ISO Load Forecast archive publication timestamps | Retain as supporting methodology documentation only |
| LCDv2 Dataset Documentation | NOAA/NCEI | Current project copy | Units, Local Standard Time convention, QC, precipitation meanings, station-year structure | Technical source, not an operational forecast archive | Cite in methodology/data sections |
| NOAA questions answered | NOAA/NCEI correspondence | Project source | Station IDs, subjective representativeness, LCDv2/GHCN-H relation, archive routes, blank precipitation, HOMR | Does not define structured day-ahead weather forecast series | Follow up only if archived forecast feasibility remains material |
| NOAA HOMR | NOAA/NCEI | Not yet audited | Station location/equipment/reporting history | Required for full-period continuity | Audit both stations for 2020–2024 |

## Key source determinations

### PJM

- PSEG pnode `51301` is the selected price location.
- `PS` is the paired metered-load area.
- `MIDATL` is the narrowest preserved historical load-forecast area covering PSEG and must be labeled a regional proxy.
- `evaluated_at_ept` is the authoritative historical forecast generated/available timestamp supplied by PJM.
- Historical forecasts are preserved as six-hour snapshots.
- The project uses latest eligible forecast strictly before 11:00 a.m. EPT D−1.

### NYISO

- `HUD VL`, PTID `61758`, is the selected Hudson Valley location.
- The project uses a strict pre-5:00 a.m. D−1 operational cutoff.
- January historical load-forecast availability currently uses `zip_entry_last_modified` and is explicitly marked as a proxy.
- The remaining external-source issue is whether an authoritative short-term historical forecast publication/availability timestamp is preserved.
- TB-064 and TB-088 resolve DST conventions at the documentation level; implementation/testing remains.

## Derived and interim datasets

| Dataset | Grain | Purpose | Status |
|---|---|---|---|
| `data/processed/pjm_pseg_january_2025_electricity.csv` | One row per PJM target hour | January cleaning, EDA, feature tests | 744 rows; feasibility only |
| `data/processed/nyiso_hudson_valley_january_2025_electricity.csv` | One row per NYISO target hour | January cleaning, EDA, feature tests | 744 rows; feasibility only |
| `data/interim/nyiso_hudson_valley_load_forecast_vintages.csv` | One row per vintage/target-hour pair | Audit and latest-eligible selection | 4,464 rows; availability proxy limitation applies |
| `data/processed/pjm_pseg_january_2025_modeling_ready.csv` | One row per target hour | January pre-modeling checkpoint | 744 rows; not final evidence |
| `data/processed/nyiso_hudson_valley_january_2025_modeling_ready.csv` | One row per target hour | January pre-modeling checkpoint | 744 rows; NYISO load forecast remains conditional |

## Provenance requirements for full-period acquisition

For every 2020–2024 source, record:

- authoritative source URL/API/archive page;
- retrieval date and query parameters;
- archive/file naming pattern and checksum where practical;
- market location and identifier;
- field definitions and units;
- local/UTC and hour-beginning/hour-ending meaning;
- revision/vintage behavior;
- publication/availability timestamp evidence;
- licensing/reuse note; and
- known definition or structural changes during the study period.

## Register maintenance rule

Add a row whenever a new dataset, bulletin, manual, correspondence item, or source-definition change affects methodology. Do not silently replace old evidence; mark it superseded and document the impact on derived data and model results.
