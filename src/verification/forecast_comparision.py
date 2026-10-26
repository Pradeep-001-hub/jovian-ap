"""Utilities for comparing forecast fields against a reference."""

from __future__ import annotations

import numpy as np

from src.verification.metrics import calculate_metrics


def compare_forecasts(
    free_forecast,
    assimilated_forecast,
    reference,
):
    """Compare free and assimilated forecasts against one reference."""

    free_forecast = np.asarray(free_forecast, dtype=float)
    assimilated_forecast = np.asarray(
        assimilated_forecast, dtype=float
    )
    reference = np.asarray(reference, dtype=float)

    if (
        free_forecast.shape != assimilated_forecast.shape
        or free_forecast.shape != reference.shape
    ):
        raise ValueError(
            "Both forecasts and the reference must have identical shapes."
        )

    free_metrics = calculate_metrics(free_forecast, reference)
    assimilated_metrics = calculate_metrics(
        assimilated_forecast, reference
    )

    improvement = {}

    for metric in ("rmse", "mae"):
        baseline = free_metrics[metric]

        if baseline == 0.0:
            improvement[metric] = None
        else:
            improvement[metric] = (
                (baseline - assimilated_metrics[metric])
                / baseline
                * 100.0
            )

    return {
        "free_forecast": free_metrics,
        "assimilated_forecast": assimilated_metrics,
        "improvement_percent": improvement,
    }