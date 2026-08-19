from __future__ import annotations

import pandas as pd


def add_baseline_predictions(df: pd.DataFrame) -> pd.DataFrame:
    """Create simple historical benchmark predictions."""
    # Put observations in chronological order and preserve the caller's dataframe.
    result = df.sort_values("timestamp_utc").copy()

    # Naive baseline: predict this hour's price with the immediately preceding
    # hour's published day-ahead price.
    result["prediction_previous_hour"] = (
        result["day_ahead_lmp"].shift(1)
    )

    # Daily seasonal baseline: predict with the price from the same hour
    # on the previous day (24 hours earlier).
    result["prediction_previous_day"] = (
        result["day_ahead_lmp"].shift(24)
    )

    # Weekly seasonal baseline: predict with the price from the same hour
    # one week earlier (7 days × 24 hours = 168 hours).
    result["prediction_previous_week"] = (
        result["day_ahead_lmp"].shift(168)
    )

    # Historical same-hour baseline: for each hour of day, predict using the
    # average of all earlier observed prices for that hour. The shift excludes
    # the current target hour, preventing target leakage.
    result["prediction_expanding_hour_average"] = (
        result.groupby("hour")["day_ahead_lmp"]
        .transform(
            lambda values: values.shift(1).expanding().mean()
        )
    )

    return result