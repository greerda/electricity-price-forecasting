from __future__ import annotations

import pandas as pd


def add_baseline_predictions(df: pd.DataFrame) -> pd.DataFrame:
    """Create simple historical benchmark predictions."""
    result = df.sort_values("timestamp_utc").copy()

    result["prediction_previous_hour"] = (
        result["day_ahead_lmp"].shift(1)
    )

    result["prediction_previous_day"] = (
        result["day_ahead_lmp"].shift(24)
    )

    result["prediction_previous_week"] = (
        result["day_ahead_lmp"].shift(168)
    )

    result["prediction_expanding_hour_average"] = (
        result.groupby("hour")["day_ahead_lmp"]
        .transform(
            lambda values: values.shift(1).expanding().mean()
        )
    )

    return result