# Data Source Register

**Last updated:** August 31, 2026

Record the exact download date, query, archive name, and source URL when the full 2020–2024 data are acquired. Unknown metadata must remain marked unknown rather than guessed.

| Dataset | Provider/source | Market/location | Current January artifact | Time basis | Purpose | Status and limitation |
|---|---|---|---|---|---|---|
| Day-ahead hourly LMP | PJM Data Miner 2 | PSEG pnode 51301 | `da_hrl_lmps_PJM_PS.csv` | Source UTC and EPT fields | PJM target and component audit | 744 January rows; total, energy, congestion, and loss retained |
| Metered hourly load | PJM Data Miner 2 | PS load area | `hrl_load_metered_PJM_PS.csv` | Eastern/UTC normalized | EDA and possible historical lag source | Actual metered load; prohibited as same-hour day-ahead predictor |
| Day-ahead zonal LBMP | NYISO MIS public data | HUD VL, PTID 61758 | `nyiso_hudson_valley_jan2025_LMP_DATA.csv` | Source Eastern normalized to UTC | NYISO target and component audit | 744 January rows |
| Integrated hourly load | NYISO MIS public data | HUD VL, PTID 61758 | `nyiso_hudson_valley_jan2025palIntegrated_HV_loaddata.csv` | Source EST/local normalized to UTC | EDA and possible historical lag source | Actual integrated load; prohibited as same-hour day-ahead predictor |
| Local climatological observations | NOAA LCD | Newark/EWR, station USW00014734 | `WeatherData Jan25 Newark.csv` | January path uses market-local and UTC keys; DST policy remains unresolved beyond January | PJM-area weather EDA and lag research | 744 hours; SI units; `FM-15` → `FM-12` → `FM-16` hourly priority; 3 missing hours |
| Local climatological observations | NOAA LCD | Stewart/SWF, station USW00014714 | `WeatherData Jan25 Stewart.csv` | January path uses market-local and UTC keys; DST policy remains unresolved beyond January | NYISO-area weather EDA and lag research | 744 hours; SI units; same priority; 7 missing, 7 quality-flagged, and 4 rejected hours |
| Archived load forecasts | NYISO MIS ISO Load Forecast archives | Hudson Valley | daily `*isolf.csv` entries from December 2024 and January 2025 ZIP archives | Target Eastern time; ZIP entry modification time used as availability proxy | NYISO day-ahead load predictor | 4,464 January rows, six vintages per target; proxy limitation applies to all 744 selected rows |
| Historical load forecasts | PJM Data Miner 2 or other authoritative PJM feed | PSEG/appropriate PJM forecast geography | Not yet acquired | Must include target hour and issue/availability time | Comparable PJM load-forecast predictor | Unresolved; do not substitute metered load |
| Calendar attributes | Derived in Notebook 04 | Both markets | Derived from `timestamp_local` | Known before cutoff | Common predictor set | `hour_of_day`, `day_of_week`, and `is_weekend` validated in Task 1 |
| NYISO market guidance | NYISO correspondence and Energy Marketplace slides | NYISO | `NYISO Energy Marketplace Email.pdf` and `NYISO Energy Marketplace.pdf` | Documentation evidence | Interpret market timing and data limitations | Retain with project sources; cite only claims actually supported |
| PJM market guidance | PJM public knowledge and Data Miner documentation | PJM | Correspondence/public documentation | Documentation evidence | Interpret target, timing, forecast availability, and DST | Continue with documented provisional assumptions while a definitive reply is absent |

## Processed January outputs

- `data/processed/pjm_pseg_january_2025_electricity.csv` — 744 rows.
- `data/processed/nyiso_hudson_valley_january_2025_electricity.csv` — 744 rows.
- `data/interim/nyiso_hudson_valley_load_forecast_vintages.csv` — 4,464 rows; regenerable and not a final modeling artifact.

## Provenance requirements for future acquisitions

For every full-period source, record:

- authoritative source URL or API endpoint;
- retrieval date and query parameters;
- archive/file name and checksum where practical;
- market location and identifier;
- field definitions and units;
- local/UTC and hour-beginning/hour-ending meaning;
- revision or vintage behavior;
- publication/availability timestamp evidence;
- licensing or permitted-use note; and
- known definition changes during 2020–2024.

**Last updated:** August 21, 2026

This register records modeling datasets, technical documentation, correspondence, intended uses, limitations, and required future validation. Raw data files remain immutable under `data/raw/`. Private correspondence is referenced but must not be published in the public repository.

## Modeling datasets

| Dataset | Provider | Source or feed | Current coverage | Key source fields | Intended use | Status and limitations | Future action |
|---|---|---|---|---|---|---|---|
| PJM Day-Ahead Hourly LMP | PJM Data Miner 2 | [Day-Ahead Hourly LMPs](https://dataminer2.pjm.com/feed/da_hrl_lmps/definition) | January 2025 pilot | `datetime_beginning_utc`, `datetime_beginning_ept`, `pnode_id`, `pnode_name`, `type`, `total_lmp_da`, component fields, `version_nbr` | PJM price target and component audit | Pilot file uses PSEG node `51301`; `total_lmp_da` is the complete target and must not be recomputed by adding its components | Decide whether the final 2020–2024 series will use or be reconciled against settlements-verified prices |
| PJM Settlements Verified Hourly LMPs | PJM Data Miner 2 | [Settlements Verified Hourly LMPs](https://dataminer2.pjm.com/feed/rt_da_monthly_lmps/definition) | Not yet acquired | Verified real-time LMPs and final day-ahead LMPs | Candidate final PJM historical target source | Not used in the January pilot | Compare against `da_hrl_lmps` and document the final source decision before bulk acquisition |
| PJM Hourly Load: Metered | PJM Data Miner 2 | [Hourly Load: Metered](https://dataminer2.pjm.com/feed/hrl_load_metered/definition) | January 2025 pilot | `datetime_beginning_utc`, `datetime_beginning_ept`, `zone`, `load_area`, `mw`, `is_verified` | EDA and possible safely lagged load features | PJM confirmed that `PS` is the appropriate load area to pair with PSEG node `51301`; target-hour actual load is unavailable at forecast time | Validate `PS` coverage for every study year; exclude same-hour actual load from operational predictors |
| PJM Historical Load Forecasts | PJM Data Miner 2 | [Historical Load Forecasts](https://dataminer2.pjm.com/feed/load_frcstd_hist/definition) | 2020–2024 available but not yet acquired | `evaluated_at_utc`, `evaluated_at_ept`, `forecast_hour_beginning_utc`, `forecast_hour_beginning_ept`, `forecast_area`, `forecast_load_mw` | Leakage-safe PJM load-forecast feature | Use `forecast_area == "MIDATL"`; PJM confirmed no PSEG-only historical detail; six-hour snapshots do not preserve every twice-hourly revision | Implement latest-eligible-vintage selection strictly before 11:00 a.m. EPT and validate coverage. If the feed definition/sample does not establish it, ask PJM whether `evaluated_at_ept` is the participant-available snapshot time and whether `MIDATL` is the appropriate historical PSEG proxy. |
| PJM Seven-Day Load Forecast | PJM Data Miner 2 | [Seven-Day Load Forecast](https://dataminer2.pjm.com/feed/load_frcstd_7_day/definition) | Current/live feed | Forecast area, issue/evaluation time, target hours | Documentation and comparison only | Live forecasts replace earlier revisions; not a suitable source for reconstructing all 2020–2024 vintages | Do not use as the historical training source |
| PJM Pricing Nodes | PJM Data Miner 2 | [Pricing Nodes](https://dataminer2.pjm.com/feed/pnode/definition) | Historical metadata; not yet audited | Pnode identifier, name, type, effective and termination information | Historical identifier continuity audit | Node identifiers may change across model updates | Verify PSEG node `51301` for every study year |
| NYISO Hudson Valley Day-Ahead LBMP | NYISO MIS public archive | [NYISO MIS public data](https://mis.nyiso.com/public/) | January 2025 pilot | `Time Stamp`, `Name`, `PTID`, `LBMP ($/MWHr)`, marginal loss and congestion fields, `source_file` | NYISO price target and component audit | NYISO confirmed `HUD VL`, PTID `61758`; download date was not retained in the current register | Record the exact archive page, download date, and monthly file pattern during full-period acquisition |
| NYISO Hudson Valley Integrated Load | NYISO MIS public archive | [NYISO MIS public data](https://mis.nyiso.com/public/) | January 2025 pilot | `Time Stamp`, `Time Zone`, `Name`, `PTID`, `Integrated Load`, `source_file` | EDA and possible safely lagged load features | NYISO confirmed PTID `61758`; target-hour integrated load is not available at prediction time | Exclude same-hour actual load from operational predictors and validate full-period identifier continuity |
| NYISO ISO Load Forecast archive | NYISO MIS | [ISO Load Forecast archive](https://mis.nyiso.com/public/P-7list.htm) | December 2024 archive entries supporting January 2025 target hours | `Time Stamp`, `Hud Vl`, archive name, entry name, entry last-modified time | NYISO load-forecast candidate feature | January archive downloaded 2026-08-12; ZIP entry last-modified time is an availability proxy, not a verified original publication timestamp; the NYISO timeline places its load-forecast posting after the 5:00 a.m. market close | Validate that each selected forecast was actually available before 5:00 a.m.; otherwise use an earlier eligible vintage or omit the feature |
| NYISO Historical Load Forecast Custom Reports | NYISO | NYISO website: Markets → Load Data → NY Load Forecast → Custom Reports | Availability indicated by NYISO; full period not yet acquired | Forecast vintage or report time, target hour, forecast zone, forecast MW | Candidate authoritative route for historical forecast reconstruction | NYISO directed the project here but did not explicitly document every field or revision rule in the response | Compare Custom Reports with the MIS `isolf` archive and determine the authoritative availability timestamp |
| NOAA Newark LCDv2 | NOAA/NCEI | [Local Climatological Data Version 2](https://www.ncei.noaa.gov/oa/local-climatological-data/index.html#v2/doc/) | Station-year 2025 file; January pilot filtered by timestamp | `STATION`, `DATE`, `REPORT_TYPE`, `SOURCE`, hourly weather fields, `REM`, backup-equipment metadata | PJM-area observed-weather EDA, validation, and possible safe lags | Station `USW00014734`; raw file is full-year, not January-only; raw `DATE` uses fixed Local Standard Time; observed target-hour weather is not operationally available | Acquire 2020–2024 station-year files, audit HOMR, and apply the documented report-type/QC rules |
| NOAA Stewart LCDv2 | NOAA/NCEI | [Local Climatological Data Version 2](https://www.ncei.noaa.gov/oa/local-climatological-data/index.html#v2/doc/) | Station-year 2025 file; January pilot filtered by timestamp | `STATION`, `DATE`, `REPORT_TYPE`, `SOURCE`, hourly weather fields, `REM`, backup-equipment metadata | NYISO-area observed-weather EDA, validation, and possible safe lags | Station `USW00014714`; raw file is full-year; includes implausible parsed values requiring physical validation | Acquire 2020–2024 station-year files, audit HOMR, and preserve raw/flagged values for traceability |
| Archived NWS text products | NOAA/NWS | SRRS and NOAAPort; academic search through [Iowa State IEM AFOS](https://mesonet.agron.iastate.edu/wx/afos) | Not yet acquired | Issuance time, bulletin/product type, issuing office, forecast text | Possible historical weather-forecast source | NOAA identified FPUS5 Zone Forecast Products and FXUS6 Area Forecast Discussions; structured hourly station-level variables are not yet established | Determine whether a reproducible parser can produce comparable hourly forecast features with issuance and valid times |

## Technical documentation and external confirmations

| Source | Provider | Location | Date | Supports | Limitations and handling | Future action |
|---|---|---|---|---|---|---|
| LCDv2 Dataset Documentation | NOAA/NCEI | [LCDv2 documentation](https://www.ncei.noaa.gov/oa/local-climatological-data/index.html#v2/doc/) | Current project copy reviewed August 2026 | Units, timestamp convention, missing values, precipitation meanings, QC indicators, station-year contents, `REM`, and equipment metadata | Technical documentation; not a scholarly literature-review source | Cite in data and methodology sections; monitor for version updates |
| NOAA questions answered | NOAA/NCEI correspondence | Private project source; do not publish personal contact details | Date not recorded in current notes | Station identifiers, subjective representativeness, LCDv2/GHCN-H relationship, archived text-product routes, blank precipitation, HOMR, QC contact | Correspondence does not guarantee station representativeness or define a structured forecast dataset | Record the original message date; follow up only if archived forecast or QC questions remain material |
| NOAA Historical Observing Metadata Repository | NOAA/NCEI | [HOMR](https://www.ncei.noaa.gov/access/homr/) | Not yet reviewed for the study period | Station location, equipment, reporting, and history | Required for full-period station-continuity validation | Audit both stations for 2020–2024 and record material changes |
| NYISO Energy Marketplace response | NYISO correspondence, Case `00143873` | Private project source | Received 2026-08-07 | PTID `61758`, price-validation references, historical load-forecast route, NYISO market timeline, daylight-saving bulletin | Response often points to other documentation rather than fully defining archive fields | Cite public documents for technical claims and keep the raw email private |
| NYISO Energy Marketplace training | NYISO | Project source: `NYISO Energy Marketplace.pdf` | 2026 training material | Day-ahead/real-time market concepts, load forecasting, Day-Ahead Market timeline | Training document; verify any operational rule against the current manual if the study scope changes | Cite slide 62 for the 5:00 a.m. cutoff and recheck if NYISO changes its market timeline |
| NYISO Technical Bulletin TB-064 | NYISO | NYISO Regulatory → Manuals, Technical Bulletins & Guides → Technical Bulletins | Not yet added to project sources | Daylight-saving transition representation in MIS files | Required for multiyear timestamp handling | Retrieve, cite, and implement before processing DST-transition dates |
| PJM Data Miner response | PJM correspondence, Case `00334055` | Private project source; do not commit the raw `.msg` | Received 2026-08-21 | PSEG/PS pairing, `load_frcstd_hist`, MIDATL proxy, `evaluated_at` meaning, six-hour retention, 11:00 a.m. conditions, no forecast-impacting 2020–2024 changes | Message includes full mail headers, personal information, and a confidentiality label | Retain privately; cite the case number and public feed definitions in public documentation |
| PJM LMP Components | PJM Knowledge Base | [Locational Marginal Price Components](https://pjm.my.site.com/publicknowledge/s/article/Locational-Marginal-Price-LMP-Components) | Accessed August 2026 | Total LMP equals energy plus congestion plus marginal-loss components | Public technical source | Cite when defining `total_lmp_da` |
| PJM Day-Ahead timeline | PJM Knowledge Base | [Day-ahead market and rebidding timelines](https://pjm.my.site.com/publicknowledge/s/article/Changes-to-Day-ahead-market-and-rebid-period-timelines-effective-date-March-31-2016) | Accessed August 2026 | 11:00 a.m. EPT Day-Ahead Market timing | Does not prescribe an academic leakage rule | Document strict `< 11:00` as the project's conservative decision |
| PJM daylight-saving guidance | PJM Knowledge Base | [Daylight Savings Time and Standard Savings Time](https://pjm.my.site.com/publicknowledge/s/article/Daylight-Savings-Time-and-Standard-Savings-Time) | Accessed August 2026 | 23-hour and 25-hour market-day behavior | Article focuses on Markets Gateway; Data Miner fields still require validation | Use UTC as the unique modeling key and test transition dates |
| PJM model-update guidance | PJM Knowledge Base | [LMP Model Update FAQ](https://pjm.my.site.com/publicknowledge/s/article/LMP-Model-Update-Frequently-Asked-Questions-FAQ) | Accessed August 2026 | Pnode and model-change risks | Does not replace feed-level effective-date validation | Audit node continuity before full-period joins |
| PJM fast-start pricing | PJM Knowledge Base | [Fast-Start Pricing](https://pjm.my.site.com/publicknowledge/s/article/Fast-Start-Pricing) | Effective 2021-09-01 | Possible structural break in PJM price formation | PJM's “no changes affecting forecasts” reply does not eliminate price-methodology changes | Consider a structural-break indicator or sensitivity analysis |
| DATA 698 syllabus | CUNY SPS | Private course source | Spring 2026 syllabus | Proposal, midterm, final-paper, presentation, and course-timeline requirements | Course document; not a modeling data source | Recheck deadlines and formatting requirements against the instructor's current guidance |

## Derived and interim datasets

| Dataset | Provider | Grain | Purpose | Status and limitation | Future action |
|---|---|---|---|---|---|
| `data/processed/pjm_pseg_january_2025_electricity.csv` | Derived | One row per PJM target hour | January cleaning, validation, EDA, and feature-engineering tests | Feasibility data only | Rebuild from full-period raw data after final source decisions |
| `data/processed/nyiso_hudson_valley_january_2025_electricity.csv` | Derived | One row per NYISO target hour | January cleaning, validation, EDA, and feature-engineering tests | Feasibility data only | Rebuild from full-period raw data after final source decisions |
| `data/interim/nyiso_hudson_valley_load_forecast_vintages.csv` | Derived | One row per forecast-vintage/target-hour pair; multiple vintages may exist per target hour | Audit and select the latest forecast eligible at the NYISO cutoff | Contains 4,464 rows for 744 unique target hours; availability is based on a proxy | Preserve all vintages; replace or validate proxy timestamps before final modeling |

## Register maintenance rules

- Record an actual download date; do not use placeholder angle brackets.
- Record the exact archive page, feed name, filename pattern, coverage, units, timezone, and revision behavior.
- Add a new row whenever a new dataset, feed, bulletin, or external confirmation affects methodology.
- Do not silently replace a historical source. Mark the old source as superseded and document the effect on derived data.
- Keep private correspondence and restricted material outside the public repository.
- Prefer canonical public URLs over email security-redirect links.
- Recheck source definitions before every bulk multiyear download.

