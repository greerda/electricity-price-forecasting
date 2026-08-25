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

### Evidence already reproduced

- 744 PJM processed hours.
- 744 NYISO processed hours.
- 4,464 NYISO forecast-vintage rows.
- 744 unique NYISO target hours with six vintages each.
- 744 latest-eligible NYISO selections.
- One-to-one NYISO forecast/electricity merge.
- Passing feature-role overlap/prohibited-field assertions.
- Three passing tests and passing Ruff checks.

### Limitation I must remember

Every current selected NYISO forecast uses a ZIP-entry last-modified availability proxy. A proxy is evidence for a feasibility pipeline, not proof of the original publication timestamp.

## Remaining learning tasks

| Task | I can mark this complete when I can… | Status |
|---:|---|---|
| 1 | derive and validate hour/day/weekend fields from a timezone-aware Series without copying the project code | Next |
| 2 | reconcile two competing schemas and explain the NOAA unit/hourly-selection decision | Not started |
| 3 | design a lag/rolling feature whose source values are provably available at the forecast origin | Not started |
| 4 | explain the common versus market-augmented PJM/NYISO feature sets and why PJM metered load is not a load forecast | Not started |
| 5 | write tests that fail for leakage, duplicate keys, wrong units, bad cutoffs, and ambiguous latest-vintage ties | Not started |
| 6 | complete January EDA and distinguish descriptive relationships from operational predictors and final conclusions | Not started |
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

