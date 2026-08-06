
### `docs/methodology_decisions.md`

Add:

```markdown
## Canonical timestamp

All datasets use `timestamp_utc` as the canonical field for joins,
chronological ordering, validation, splitting, and modeling.

A timezone-aware `timestamp_local` field is retained for local calendar
features and reporting.

Both PJM and NYISO local timestamps are interpreted using
`America/New_York`.

## NOAA weather units

The NOAA Local Climatological Data files are interpreted as using
metric/SI units:

- temperature: degrees Celsius
- dew point: degrees Celsius
- relative humidity: percent
- wind speed: meters per second

No unit conversion is applied. Implausible values are rejected and
recorded with a weather-quality indicator.

## Load-data limitation

The current PJM and NYISO load files contain actual or metered load.
Target-hour actual load will not be used directly as a day-ahead
forecasting predictor.

Only appropriately lagged load values may be used unless verified
day-ahead load forecast data are obtained.