# Data Source Register

**Last updated:** August 24, 2026

Record the exact download date, query, archive name, and source URL when the full 2020–2024 data are acquired. Unknown metadata must remain marked unknown rather than guessed.

| Dataset | Provider/source | Market/location | Current January artifact | Time basis | Purpose | Status and limitation |
|---|---|---|---|---|---|---|
| Day-ahead hourly LMP | PJM Data Miner 2 | PSEG pnode 51301 | `da_hrl_lmps_PJM_PS.csv` | Source UTC and EPT fields | PJM target and component audit | 744 January rows; total, energy, congestion, and loss retained |
| Metered hourly load | PJM Data Miner 2 | PS load area | `hrl_load_metered_PJM_PS.csv` | Eastern/UTC normalized | EDA and possible historical lag source | Actual metered load; prohibited as same-hour day-ahead predictor |
| Day-ahead zonal LBMP | NYISO MIS public data | HUD VL, PTID 61758 | `nyiso_hudson_valley_jan2025_LMP_DATA.csv` | Source Eastern normalized to UTC | NYISO target and component audit | 744 January rows |
| Integrated hourly load | NYISO MIS public data | HUD VL, PTID 61758 | `nyiso_hudson_valley_jan2025palIntegrated_HV_loaddata.csv` | Source EST/local normalized to UTC | EDA and possible historical lag source | Actual integrated load; prohibited as same-hour day-ahead predictor |
| Local climatological observations | NOAA LCD | Newark/EWR, station USW00014734 | `WeatherData Jan25 Newark.csv` | Observation time normalized to America/New_York and UTC | PJM-area weather EDA and lag research | Full-year source file; January reduced to 744-hour calendar; SI units |
| Local climatological observations | NOAA LCD | Stewart/SWF, station USW00014714 | `WeatherData Jan25 Stewart.csv` | Observation time normalized to America/New_York and UTC | NYISO-area weather EDA and lag research | Full-year source file; corrupt extremes rejected; SI units |
| Archived load forecasts | NYISO MIS ISO Load Forecast archives | Hudson Valley | daily `*isolf.csv` entries from December 2024 and January 2025 ZIP archives | Target Eastern time; ZIP entry modification time used as availability proxy | NYISO day-ahead load predictor | 4,464 January rows, six vintages per target; proxy limitation applies to all 744 selected rows |
| Historical load forecasts | PJM Data Miner 2 or other authoritative PJM feed | PSEG/appropriate PJM forecast geography | Not yet acquired | Must include target hour and issue/availability time | Comparable PJM load-forecast predictor | Unresolved; do not substitute metered load |
| Calendar attributes | Derived in Notebook 04 | Both markets | Derived from `timestamp_local` | Known before cutoff | Common predictor set | Hour/day/weekend pending fresh-kernel Task 1 validation |
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
