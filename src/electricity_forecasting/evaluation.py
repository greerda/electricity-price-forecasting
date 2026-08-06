from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


def calculate_regression_metrics(
    actual: pd.Series,
    predicted: pd.Series,
) -> dict[str, float]:
    """Calculate metrics after removing incomplete pairs."""
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

    mae = mean_absolute_error(
        comparison["actual"],
        comparison["predicted"],
    )

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
    """Evaluate several prediction columns consistently."""
    records: list[dict[str, object]] = []

    for prediction_column in prediction_columns:
        metrics = calculate_regression_metrics(
            actual=df["day_ahead_lmp"],
            predicted=df[prediction_column],
        )

        records.append(
            {
                "market": market,
                "model": prediction_column.replace(
                    "prediction_",
                    "",
                ),
                **metrics,
            }
        )

    return pd.DataFrame(records)