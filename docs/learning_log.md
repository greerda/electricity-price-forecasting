## Learning Log

This file records what the student can now explain and reproduce, not merely what an agent changed.

## 2026-08-24 — Pre-modeling checkpoint

### What I can explain

- Why one market-location-hour must be unique.
- Why `timestamp_utc` is the canonical join/order key and `timestamp_local` is still needed.
- How Notebook 02 converts six raw electricity/weather sources into two 744-row January tables.
- Why reindexing to a complete hourly calendar reveals missing weather observations.
- Why an outer price/load reconciliation followed by a left weather join is safer than hiding unmatched hours.
- What a forecast vintage, target hour, availability time, prediction cutoff, and provenance field mean.
- How 4,464 NYISO forecast rows represent six vintages for each of 744 target hours.
- Why the latest eligible forecast is selected before, not after, the cutoff.
- Why same-hour actual load, observed weather, and target components can leak target-time information.
- Why audit and identifier fields travel with a modeling table but must not be supplied to a model.

## 2026-08-31 — Automated validation and January EDA

### Work completed

- Added automated tests for canonical schemas, timestamp order and uniqueness, missing hours, missing targets, prohibited predictors, calendar ranges, cutoff eligibility, and forecast-vintage tie handling.
- Completed descriptive EDA for the January 2025 PJM PSEG and NYISO Hudson Valley feasibility tables.
- Verified that same-hour actual load and observed weather are descriptive only and not operational day-ahead predictors.

### What I learned

- A test should verify both rejection of invalid data and acceptance of valid data.
- A latest-eligible forecast must be selected by availability time before the prediction cutoff, and tied latest rows should fail rather than be chosen arbitrarily.
- Mean and median can tell different stories when electricity-price spikes create right-skewed distributions.
- Correlation describes association, not causation or operational feature availability.

### Next single action

Create the Task 7 modeling-ready checkpoint tables with explicit target, predictor, identifier, audit, and excluded-field roles.

### Evidence already reproduced

- 744 PJM processed hours.
- 744 NYISO processed hours.
- 4,464 NYISO forecast-vintage rows.
- 744 unique NYISO target hours with six vintages each.
- 744 latest-eligible NYISO selections.
- One-to-one NYISO forecast/electricity merge.
- Passing feature-role overlap/prohibited-field assertions.
- Twenty-one passing tests and passing Ruff checks.

### Limitation I must remember

Every current selected NYISO forecast uses a ZIP-entry last-modified availability proxy. A proxy is evidence for a feasibility pipeline, not proof of the original publication timestamp.

## Remaining learning tasks

| Task | I can mark this complete when I can… | Status |
|---:|---|---|
| 1 | derive and validate hour/day/weekend fields from a timezone-aware Series without copying the project code | Complete |
| 2 | reconcile two competing schemas and explain the NOAA unit/hourly-selection decision | Complete |
| 3 | design a lag/rolling feature whose source values are provably available at the forecast origin | Completed |
| 4 | explain the common versus market-augmented PJM/NYISO feature sets and why PJM metered load is not a load forecast | Completed |
| 5 | write tests that fail for leakage, duplicate keys, wrong units, bad cutoffs, and ambiguous latest-vintage ties | Completed |
| 6 | complete January EDA and distinguish descriptive relationships from operational predictors and final conclusions | Completed |
| 7 | rebuild the January pre-modeling pipeline in a fresh environment and defend every exported field role | Not started |

## Entry template

### YYYY-MM-DD — Task or concept

**Purpose:**  
What problem was this work intended to solve?

**My plain-English explanation:**  
Explain the transformation or method without looking at the code.

**C#/LINQ/SQL analogy:**  
What familiar programming or database idea is most similar?

**Code I typed or changed:**  
List the notebook cells, functions, tests, or configuration values.

**Verification evidence:**  
Record row counts, ranges, assertions, test output, and relevant file paths.

**Mistake or confusion:**  
What failed or was initially misunderstood?

**What I learned:**  
What can now be reproduced without assistance?

**Remaining limitation:**  
What is still assumed, provisional, or unresolved?

**Next single action:**  
Name one concrete task and its completion check.

## 2026-08-25 — Task 1: Leakage-safe calendar features

**Purpose:**
Create calendar predictors that capture recurring market patterns while using only information known at the day-ahead forecast cutoff.

**My plain-English explanation:**
I can derive `hour_of_day`, `day_of_week`, and `is_weekend` from the timezone-aware `timestamp_local` field. Hour of day can capture daily demand and pricing patterns; day of week and the weekend flag can capture differences between workdays and weekends. These fields are leakage-safe because the calendar time of a target hour is known before that hour occurs. Using `America/New_York` makes the features follow the electricity market's local clock, including daylight-saving-time transitions.

**C#/LINQ/SQL analogy:**
This is like adding computed columns to a SQL query from a typed `DateTimeOffset` value: extract the local hour and weekday first, then derive a Boolean weekend field from the weekday. The important rule is to use the market-local timestamp, not a UTC clock value that could assign a market hour to the wrong calendar day.

**Remaining limitation:**
The reusable calendar helper now uses the canonical `hour_of_day` field name. It retains an integer weekend indicator, which is appropriate for the current feature-engineering implementation and separately tested from the Notebook 04 validation.

**Next single action:**
Compare the Notebook 02 preprocessing workflow with the reusable preprocessing modules and identify the first schema mismatch.

## 2026-08-25 — Task 2: Reusable preprocessing reconciliation

**Purpose:**
Make the reusable preprocessing code reproduce the approved January Notebook 02 schema and weather policies, so a notebook run and a script run do not silently produce different data.

**My plain-English explanation:**
I can explain why an external source name, such as `total_lmp_da` or `Integrated Load`, must be translated once into a canonical project name. I can also explain why the January NOAA fields remain in SI units, why one report is selected per hour by a documented priority, and why missing, flagged, and rejected weather values must remain visible as audit fields.

**C#/LINQ/SQL analogy:**
The canonical schema is an internal DTO contract. The hourly report rule is like `ROW_NUMBER() OVER (PARTITION BY hour ORDER BY report_priority, observed_at)` followed by `WHERE row_number = 1`; it is not an average across incompatible source reports.

**Verification evidence:**
Fresh-process PJM and NYISO runs each produced 744 ordered, unique hourly rows with no missing price or actual-load values. Weather flags matched Notebook 02: PJM had 3 missing weather hours and NYISO had 7 missing, 7 quality-flagged, and 4 rejected hours. Five pytest tests and Ruff passed.

**Remaining limitation:**
January has no daylight-saving transition. Resolve the raw NOAA fixed-standard-time versus market-local-time interpretation before applying this weather timestamp policy to 2020–2024.

**Next single action:**
For one target market-hour, identify the forecast cutoff and prove whether a proposed historical price value was available by that cutoff.

## Planned model-comparison learning

Before final model selection, I will be able to explain why a feature-ablation comparison must keep the model, chronological split, and metrics fixed while changing only the feature set. I will also be able to explain why error should be reported by price regime as well as overall MAE and RMSE, without deleting or redefining legitimate negative and high prices.

## 2026-08-21 — External responses and forecast timing

### Work completed

- Reviewed the PJM, NYISO, and NOAA responses.
- Updated the project documentation.
- Identified the remaining NYISO forecast-availability questions.

### What I learned

- PJM preserves six-hour historical MIDATL load-forecast snapshots.
- NYISO’s Day-Ahead Market closes at 5:00 a.m. EPT.
- A forecast covering the correct target hour is not safe unless it was also available before the market cutoff.
- ZIP-entry modification time is not automatically proof of public availability.

### Decision or consequence

- Treat NYISO `load_forecast_mw` as conditionally approved for the January pilot.
- Do not use it in the final operational model until its publication time is verified.
- Send a focused follow-up inquiry to NYISO.

### Files or work affected

- `notebooks/04_feature_engineering.ipynb`
- `docs/methodology_decisions.md`
- `docs/data_source_register.md`
- `PROJECT_PLAN.md`

### Next step

- Complete the feature-role classification in Notebook 04 while waiting for NYISO’s response.

