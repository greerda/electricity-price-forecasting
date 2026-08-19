"""Functions for evaluating day-ahead electricity-price predictions."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


def calculate_regression_metrics(
    actual: pd.Series,
    predicted: pd.Series,
) -> dict[str, float]:
    """Calculate MAE and RMSE from aligned, complete prediction pairs."""
    # Build one comparison table before dropping nulls so an actual value is
    # always evaluated against the prediction for the same market-hour.
    comparison = pd.DataFrame(
        {
            "actual": actual,
            "predicted": predicted,
        }
    ).dropna()

    if comparison.empty:
        raise ValueError(
            "No complete actual-prediction pairs were available."
        )

    # MAE is the primary project metric: its units are dollars per MWh, making
    # the typical size of an absolute forecasting error easy to interpret.
    mae = mean_absolute_error(
        comparison["actual"],
        comparison["predicted"],
    )

    # RMSE gives larger errors, such as price spikes, more influence than MAE.
    rmse = np.sqrt(
        mean_squared_error(
            comparison["actual"],
            comparison["predicted"],
        )
    )

    return {
        "n_observations": len(comparison),
        "mae": float(mae),
        "rmse": float(rmse),
    }


def evaluate_prediction_columns(
    df: pd.DataFrame,
    market: str,
    prediction_columns: list[str],
) -> pd.DataFrame:
    """Evaluate several model-prediction columns using the same metrics."""
    records: list[dict[str, object]] = []

    for prediction_column in prediction_columns:
        # All models use day_ahead_lmp as the observed target.  The prediction
        # columns should already be generated from a chronological evaluation
        # split; this function only summarizes their errors.
        metrics = calculate_regression_metrics(
            actual=df["day_ahead_lmp"],
            predicted=df[prediction_column],
        )

        records.append(
            {
                "market": market,
                # Remove the shared storage prefix to create a readable model
                # name in the metrics table (for example, previous_day).
                "model": prediction_column.replace(
                    "prediction_",
                    "",
                ),
                **metrics,
            }
        )

    return pd.DataFrame(records)
