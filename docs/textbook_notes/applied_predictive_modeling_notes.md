# Applied Predictive Modeling — Project Notes

## Reference

Kuhn, Max, and Kjell Johnson. *Applied Predictive Modeling*. Springer, 2013. DOI: 10.1007/978-1-4614-6849-3.

The full local reference is stored under `docs/references_local/` and must not be committed or reproduced. These notes paraphrase only the material selected for this project.

## Relevant concepts

- Data preprocessing, missing values, predictor construction, and removal of unhelpful predictors support the project’s reproducible cleaning and feature-engineering workflow.
- Overfitting, tuning, data splitting, and resampling support the chronological validation design. The book’s general resampling guidance must be adapted to time order; random resampling is not valid for the primary electricity-forecasting evaluation.
- Regression-performance measures support MAE and RMSE as the primary evaluation metrics.
- Predictor-importance and feature-selection material supports post-selection interpretation, provided the calculation is confined to training/validation folds and does not use the final test set.
- The discussion of factors affecting performance supports reporting error across meaningful price regimes rather than only one overall metric.

## Adopted project applications

1. Compare a common core feature set against an NYISO augmented set that adds `load_forecast_mw`; retain the proxy-availability limitation in the results.
2. Report error by hour of day, weekday/weekend, and normal-price versus extreme-price regimes.
3. Keep the final test period untouched while selecting features, models, and hyperparameters.

## Time-permitting applications

- Assess whether feature importance is stable across chronological validation folds.
- Add a concise bounded-tuning diagnostic after the primary model comparison is complete.

## Scope boundary

The book contains broad predictive-modeling guidance but does not replace the project’s leakage-prevention and chronological-evaluation requirements. It does not justify adding neural networks or other new primary model families.
