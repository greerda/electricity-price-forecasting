# Full-GO Checkpoint — Load-Forecast Value Study

**Created:** September 14, 2026  
**Current status:** Conditional GO — the January feasibility pipeline is proven, but the load-forecast feature must pass the validation steps below before the final research design is considered fully committed.

## Research question

> How much does adding day-ahead load forecasts improve hourly day-ahead electricity-price prediction accuracy in PJM PSEG and NYISO Hudson Valley, and is the improvement larger in one market than the other?

## Supplementary question

> Does the day-ahead load forecast contain more unique predictive information about electricity prices in the market where the larger improvement occurs?

The supplementary question is a predictive/statistical explanation, not a causal market-design claim. It will be answered using measurable incremental information after historical-price and calendar effects are accounted for.

## Full-GO criteria

The project becomes a **full GO** for this research question when all five criteria below are satisfied.

### 1. PJM January 2025 load-forecast proof

Acquire PJM Data Miner 2 `load_frcstd_hist` data for `forecast_area = MIDATL` covering enough late-December 2024 and January 2025 dates to support every January target hour.

For every January 2025 target hour:

- construct the D−1 11:00 a.m. EPT prediction cutoff;
- require `evaluated_at_ept < prediction_cutoff`;
- select the latest eligible MIDATL forecast snapshot;
- preserve `evaluated_at_ept`, `evaluated_at_utc`, target-hour timestamps, forecast value, source metadata, and cutoff audit fields;
- require at most one selected forecast per target hour; and
- merge the selected forecast one-to-one into the PJM modeling-ready path.

Completion evidence:

- expected January target-hour coverage is measured and documented;
- no selected forecast is at or after the cutoff;
- no duplicate target hours are introduced;
- all selected rows use MIDATL; and
- tests pass for cutoff eligibility, latest-vintage selection, uniqueness, and merge cardinality.

MIDATL must remain labeled a regional proxy for PSEG, not a PSEG-specific load forecast.

### 2. NYISO January 2025 timing correction

Regenerate the NYISO forecast-vintage timing path using P-7 public-report `Last Updated` as the primary availability evidence:

```text
availability_basis = "p7_last_updated"
availability_is_proxy = True
```

Retain ZIP-entry modification timestamps as secondary provenance where available.

For every target hour:

- construct the D−1 5:00 a.m. EPT cutoff;
- require `forecast_available_at < prediction_cutoff`;
- select the latest eligible P-7 vintage whose multi-day horizon still contains the target hour; and
- rerun cutoff, tie, uniqueness, leakage, and one-to-one merge checks.

Completion evidence:

- January forecast-vintage data are rebuilt with P-7 timing;
- selected-vintage coverage is measured;
- the modeling-ready NYISO checkpoint is regenerated/revalidated; and
- all relevant tests pass.

### 3. Historical continuity spot checks

Before downloading the entire 2020–2024 study period, prove that the same acquisition and timing rules work on representative historical samples from both markets.

Minimum spot-check set:

- one representative month in 2020;
- one representative month in 2024; and
- at least one DST-transition period that exercises spring-forward or fall-back behavior.

For PJM, verify:

- PSEG pnode `51301` continuity;
- `PS` load-area continuity where relevant;
- MIDATL forecast-area availability;
- `evaluated_at_*` behavior;
- schema/field consistency; and
- correct UTC uniqueness through DST.

For NYISO, verify:

- `HUD VL` / PTID `61758` continuity;
- P-7 forecast availability and multi-day horizon behavior;
- `Last Updated` metadata availability;
- annual schema/archive conventions; and
- transition-day behavior consistent with TB-064/TB-088 and unique UTC timestamps.

### 4. Forecast coverage gate

Calculate the percentage of target hours for which a valid pre-cutoff load forecast can be constructed in every spot-check period.

The gate passes when coverage is sufficiently high for a defensible comparison and all material gaps are understood and documented. Do not silently impute missing forecast vintages or use post-cutoff data to increase coverage.

If coverage is materially incomplete or systematically biased in one market, stop and reassess the research question before bulk acquisition.

### 5. Freeze the experimental design

After the first four criteria pass, freeze the primary design before full-period modeling.

Base feature set:

```text
calendar features
+ cutoff-safe historical price features
```

Augmented feature set:

```text
calendar features
+ cutoff-safe historical price features
+ eligible day-ahead load forecast
```

Primary models:

1. persistence baseline;
2. Ridge or Elastic Net regression;
3. Random Forest regression; and
4. gradient-boosted tree regression such as XGBoost or `HistGradientBoostingRegressor`.

Primary metrics:

- MAE;
- RMSE; and
- percentage improvement in MAE/RMSE from the base feature set to the augmented feature set.

Use the same model family, chronological split, preprocessing policy, and metric definitions when comparing base versus augmented feature sets. This isolates the incremental predictive value of the load forecast.

Candidate full-period split, subject to final coverage review:

- training: 2020–2022;
- validation/tuning: 2023;
- final untouched test: 2024.

## Supplementary-analysis plan

If the augmented feature set improves prediction more in one market, test whether load forecast contains more unique predictive information there using measurable diagnostics such as:

- reduction in out-of-sample MAE and RMSE;
- change in out-of-sample R² where useful;
- association between load forecast and baseline-model residuals;
- permutation importance of `load_forecast_mw`; and
- controlled feature-ablation results with the model/split held fixed.

Do not claim that a broad concept such as “market design” explains the difference unless a specific measurable mechanism is separately demonstrated.

## Required data for the final study

Required:

- PJM PSEG day-ahead price history for 2020–2024;
- NYISO Hudson Valley day-ahead LBMP history for 2020–2024;
- PJM MIDATL `load_frcstd_hist` forecasts with `evaluated_at_*` timing;
- NYISO P-7 Hudson Valley forecasts with usable `Last Updated` metadata;
- sufficient preceding data to construct historical-price features at study boundaries; and
- calendar variables derived from market-local timestamps.

Useful but not required for the main research question:

- actual/metered load for EDA and safe-lag experiments;
- NOAA observed weather for EDA or later leakage-safe lag experiments;
- archived weather forecasts;
- natural-gas prices; and
- neural-network or pretrained time-series models.

## External-contact requirement

No additional PJM or NYISO response is required to begin this checkpoint.

- PJM historical forecast timing semantics are sufficiently resolved for implementation.
- NYISO clarification of the formal meaning of P-7 `Last Updated` remains useful, but the project has a documented public-source rule and does not need to wait for a response.

If new operator evidence contradicts the current timing interpretation, update the methodology, rebuild affected features, and rerun leakage validation.

## Decision outcomes

### Full GO

Declare **Full GO** when all five criteria pass and the experiment is frozen.

### Continue as Conditional GO

Remain **Conditional GO** when the pipeline is working but historical forecast coverage or timing evidence still needs proof.

### No-GO for the load-forecast-centered question

Do not use the load-forecast-centered question as the primary capstone if one market lacks defensible pre-cutoff forecast coverage across the study period.

Fallback question:

> How does hourly day-ahead electricity-price predictability differ between PJM PSEG and NYISO Hudson Valley using historical prices and calendar information?

The fallback preserves the two-market comparison while removing dependence on historical load-forecast availability.

## Immediate execution order

1. Complete PJM January 2025 MIDATL historical load-forecast ingestion and selection.
2. Regenerate NYISO January 2025 forecast timing with P-7 `Last Updated`.
3. Run the 2020/2024/DST historical spot checks for both markets.
4. Produce a coverage and leakage-validation summary.
5. Record the Full GO / Conditional GO / No-GO decision.
6. If Full GO, begin bulk 2020–2024 acquisition and freeze the model/feature-ablation design.
