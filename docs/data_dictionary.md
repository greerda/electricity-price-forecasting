| Processed column        | Source column               | Unit |
| ----------------------- | --------------------------- | ---- |
| `temperature_c`         | `HourlyDryBulbTemperature`  | °C   |
| `dew_point_c`           | `HourlyDewPointTemperature` | °C   |
| `relative_humidity_pct` | `HourlyRelativeHumidity`    | %    |
| `wind_speed_mps`        | `HourlyWindSpeed`           | m/s  |
| Column | Type | Unit | Description |
|---|---|---|---|
| `timestamp_utc` | datetime | UTC | Canonical timestamp used for joins and modeling |
| `timestamp_local` | datetime | America/New_York | Local market timestamp |
| `day_ahead_lmp` | numeric | $/MWh | Day-ahead locational marginal price |
| `load_mw` | numeric | MW | Actual or integrated hourly load |
| `temperature_c` | numeric | °C | Hourly dry-bulb temperature |
| `dew_point_c` | numeric | °C | Hourly dew-point temperature |
| `relative_humidity_pct` | numeric | % | Hourly relative humidity |
| `wind_speed_mps` | numeric | m/s | Hourly wind speed |
| `weather_station` | string | — | NOAA station identifier |