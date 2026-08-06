from __future__ import annotations

from pathlib import Path

import pandas as pd

PREDICTION_OUTPUT_COLUMNS = [
    "timestamp_utc",
    "timestamp_local",
    "market",
    "location",
    "model",
    "dataset_split",
    "actual",
    "prediction",
    "residual",
]


def create_prediction_output(
    df: pd.DataFrame,
    prediction_column: str,
    model_name: str,
    dataset_split: str,
) -> pd.DataFrame:
    output = pd.DataFrame(
        {
            "timestamp_utc": df["timestamp_utc"],
            "timestamp_local": df["timestamp_local"],
            "market": df["market"],
            "location": df["location"],
            "model": model_name,
            "dataset_split": dataset_split,
            "actual": df["day_ahead_lmp"],
            "prediction": df[prediction_column],
        }
    )

    output["residual"] = (
        output["actual"] - output["prediction"]
    )

    return output[PREDICTION_OUTPUT_COLUMNS]


def save_csv(
    df: pd.DataFrame,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)