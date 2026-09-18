# Literature and Reference Source Register

**Project:** DATA 698 Electricity Price Forecasting

**Last updated:** September 18, 2026

**Citation file:** `reports/references.bib`

## Purpose

This is the readable master list of books, scholarly literature, manuals,
technical bulletins, course documents, and other references used by the
project. Formal citation records are stored in `reports/references.bib`.

This register does **not** replace `docs/data_source_register.md`, which tracks
datasets, feeds, downloads, correspondence, coverage, and data limitations.

## Books and textbooks

| Citation key | Source | Project use | Status |
|---|---|---|---|
| `hyndman2026fpppy` | Hyndman, Athanasopoulos, Garza, Challu, Mergenthaler, and Olivares (2026), *Forecasting: Principles and Practice, the Pythonic Way* | Primary methodological reference and implementation checklist for time-series exploration, decomposition, features, forecasting, validation, diagnostics, and accuracy measurement | Active core textbook; citation complete; online edition is continuously updated |

### How this textbook will be used

Use the book as both a citation source and a practical checklist. Its examples
guide the workflow, but the project must apply the ideas to PJM PSEG and NYISO
Hudson Valley data rather than copying the book's example datasets.

| Book chapter | Capstone application | Required or optional | Planned evidence |
|---|---|---|---|
| 1. Getting started | State the forecast target, forecast horizon, decision context, and limits on predictability | Required | Research question and methodology sections |
| 2. Time series graphics | Plot hourly prices; inspect trend, seasonality, volatility, outliers, negative prices, and market differences | Required | Notebook 03 figures and EDA findings |
| 3. Time series decomposition | Separate trend, seasonal, and remainder behavior where suitable; explain whether multiple seasonal periods require methods beyond simple decomposition | Required diagnostic | Notebook 03 decomposition plots and interpretation |
| 4. Time series features | Create calendar, lag, rolling, seasonal, and distributional features without future leakage | Required | Notebook 04 feature table and feature dictionary |
| 5. The forecaster's toolbox | Define training, validation, and test periods; implement benchmark forecasts; measure out-of-sample accuracy | Required | Notebook 05 baselines and metric tables |
| 6. Judgmental forecasts | Explain expert or operational adjustments only if they are used | Optional | Limitations or future-work discussion |
| 7. Time series regression models | Fit interpretable regression models using calendar, load-forecast, weather, and lagged-price predictors | Required | Ridge or regression model results |
| 8. Exponential smoothing | Evaluate as a classical statistical benchmark when appropriate | Recommended | Statistical benchmark comparison |
| 9. ARIMA models | Evaluate seasonal ARIMA or an appropriate ARIMA-family model when feasible | Recommended | Statistical benchmark comparison |
| 10. Dynamic regression models | Consider regression errors with time-series structure for exogenous predictors | Optional, scope permitting | Sensitivity or extended-model analysis |
| 11. Hierarchical and grouped time series | Use concepts to frame the relationship among markets, zones, and aggregate load forecasts; reconciliation is not required for the two-location study | Contextual | Methodology limitations |
| 12. Advanced forecasting methods | Consult when choosing models beyond the required statistical baselines | Optional | Model rationale |
| 13. Practical forecasting issues | Address missing data, outliers, structural breaks, forecast production, and operational constraints | Required | Data-quality, methodology, and limitations sections |
| 14. Neural networks | Guide LSTM/GRU design and evaluation only after simpler baselines are working | Optional stretch goal | Neural-network experiment |
| 15. Foundation forecasting models | Consider only as a clearly separated exploratory extension | Optional future work | Future-work section or portfolio enhancement |

### Minimum textbook-derived project checklist

- [ ] Define the target as hourly day-ahead price for each selected market location.
- [ ] State the operational forecast horizon and information cutoff.
- [ ] Preserve chronological order and use time-based validation rather than random splitting.
- [ ] Establish simple benchmark forecasts before fitting complex models.
- [ ] Visualize each time series before modeling.
- [ ] Examine trend, multiple seasonal patterns, volatility, outliers, negative prices, and structural breaks.
- [ ] Create lagged and calendar features using information available before the forecast cutoff.
- [ ] Keep training, validation, and final test data temporally separated.
- [ ] Compare models on the same forecast origins and test hours.
- [ ] Report MAE and RMSE; use percentage errors only with an explicit warning about zero and near-zero electricity prices.
- [ ] Inspect residuals for remaining structure and unusually large errors.
- [ ] Compare results separately for PJM PSEG and NYISO Hudson Valley.
- [ ] Document uncertainty, limitations, and conditions under which forecasts may fail.
- [ ] Record the online book's access date because the text is continuously updated.

## Technical manuals and documentation

| Citation key | Source | Project use | Status |
|---|---|---|---|
| `noaa_lcdv2` | NOAA/NCEI, *Local Climatological Data Version 2 (LCDv2) Dataset Documentation* | Weather fields, units, timestamps, report types, missing values, and quality-control interpretation | Active; confirm revision date before final paper |
| `nyiso2025loadforecast` | NYISO, *Load Forecasting Manual*, Version 5.1 | NYISO load-forecast process and terminology | Active project copy |
| `nyiso2026marketplace` | Kelly Stegmann/NYISO, *NYISO Energy Marketplace* | Day-ahead and real-time market concepts, bidding, scheduling, and market timeline | Active training reference; verify operational rules against current manuals |
| `nyiso2026tb064` | NYISO Technical Bulletin 064 | Fall daylight-saving transition and 25-hour market day | Required for multiyear timestamp handling |
| `nyiso2026tb088` | NYISO Technical Bulletin 088 | Spring daylight-saving transition and 23-hour market day | Required for multiyear timestamp handling |

## PJM public technical references

| Citation key | Source | Project use | Status |
|---|---|---|---|
| `pjm_lmp_components` | PJM, *Locational Marginal Price Components* | Definition of total LMP and its energy, congestion, and marginal-loss components | Active |
| `pjm_dayahead_timeline` | PJM, *Changes to Day-Ahead Market and Rebid Period Timelines* | Support for the 11:00 a.m. EPT day-ahead cutoff | Active |
| `pjm_daylight_saving` | PJM, *Daylight Savings Time and Standard Savings Time* | PJM 23-hour and 25-hour market-day handling | Active; validate Data Miner behavior separately |
| `pjm_model_update` | PJM, *LMP Model Update Frequently Asked Questions* | Pnode and model-change risk | Active |
| `pjm_fast_start` | PJM, *Fast-Start Pricing* | Potential September 2021 structural break in PJM price formation | Candidate for sensitivity analysis |

## Course and governance references

| Citation key | Source | Project use | Status |
|---|---|---|---|
| `cuny2026data698` | CUNY SPS, *DATA 698: Data Science Capstone Syllabus* | Proposal, midterm, final-paper, presentation, and course requirements | Private course document; do not publish without permission |

## Sources tracked elsewhere

The following are important project evidence but are not books or conventional
literature-review sources. They remain in `docs/data_source_register.md`:

- PJM and NYISO market datasets and archive feeds;
- NOAA station-year data files;
- PJM and NYISO correspondence;
- NOAA correspondence;
- derived and interim datasets; and
- download dates, coverage, identifiers, limitations, and validation tasks.

## Maintenance rules

1. Add a source here when it contributes a substantive concept, method,
   definition, or documented operating rule.
2. Add the matching BibTeX record to `reports/references.bib` before citing it.
3. Use one stable citation key everywhere in Quarto files and notebooks.
4. Record page, section, table, figure, or slide numbers in working notes when a
   source supports a specific claim.
5. Confirm URLs, editions, publication dates, and document versions before the
   final submission.
6. Keep private correspondence and restricted course documents out of the
   public repository.
7. Add any additional textbook immediately rather than leaving it only in a
   notebook, chat, or course assignment.

## Known follow-up work

- Add peer-reviewed electricity-price forecasting studies during the formal
  literature review.
- Add sources supporting spike definitions, probabilistic forecasting, and
  time-series cross-validation if those methods enter the final scope.
- Confirm the public URLs for NYISO Technical Bulletins 064 and 088 and the
  Load Forecasting Manual.
- Confirm the revision date of the local LCDv2 documentation copy.
- Add page or section locators as claims are drafted in `reports/capstone.qmd`.
