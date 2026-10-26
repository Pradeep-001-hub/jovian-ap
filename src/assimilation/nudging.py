"""Observation-space nudging utility for JOVIAN-AP.

Applies a simple relaxation update:

    x_adjusted = x_forecast + alpha * (observation - prediction)

This initial utility adjusts predicted observation values. It does
not yet update the complete spatial shallow-water model state.
"""

from __future__ import annotations

import numpy as np


def apply_nudging(
    forecast_values,
    observations,
    predicted_values,
    alpha=0.2,
):
    """Apply a nudging update to forecast values.

    Parameters
    ----------
    forecast_values : dict[str, array-like]
        Forecast values to adjust, keyed by variable name.
    observations : dict[str, array-like]
        Observed values for each variable.
    predicted_values : dict[str, array-like]
        Model-predicted observations corresponding to observations.
    alpha : float, default=0.2
        Nudging coefficient in the interval [0, 1].

    Returns
    -------
    dict[str, numpy.ndarray]
        Adjusted forecast values.

    Notes
    -----
    The innovation is observation minus predicted observation.
    The innovation and forecast arrays must have matching shapes.
    Input arrays are not modified.
    """

    if not isinstance(alpha, (int, float, np.integer, np.floating)):
        raise ValueError("alpha must be a finite number between 0 and 1.")

    if not np.isfinite(alpha) or not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must be a finite number between 0 and 1.")

    if not isinstance(forecast_values, dict) or not forecast_values:
        raise ValueError("forecast_values must be a non-empty dictionary.")

    if not isinstance(observations, dict) or not observations:
        raise ValueError("observations must be a non-empty dictionary.")

    if not isinstance(predicted_values, dict) or not predicted_values:
        raise ValueError("predicted_values must be a non-empty dictionary.")

    expected_names = set(forecast_values)

    if expected_names != set(observations):
        raise ValueError(
            "Forecasts and observations must contain the same variables."
        )

    if expected_names != set(predicted_values):
        raise ValueError(
            "Forecasts and predictions must contain the same variables."
        )

    adjusted = {}

    for name in forecast_values:
        if not isinstance(name, str) or not name:
            raise ValueError("Variable names must be non-empty strings.")

        forecast = np.asarray(forecast_values[name], dtype=float)
        observed = np.asarray(observations[name], dtype=float)
        predicted = np.asarray(predicted_values[name], dtype=float)

        if forecast.ndim != 1 or observed.ndim != 1 or predicted.ndim != 1:
            raise ValueError(
                f"Forecasts, observations, and predictions for '{name}' "
                "must be one-dimensional arrays."
            )

        if forecast.size == 0:
            raise ValueError(
                f"Arrays for '{name}' must contain at least one value."
            )

        if forecast.shape != observed.shape or observed.shape != predicted.shape:
            raise ValueError(
                f"Forecast, observation, and prediction shapes must match "
                f"for '{name}'."
            )

        if not (
            np.all(np.isfinite(forecast))
            and np.all(np.isfinite(observed))
            and np.all(np.isfinite(predicted))
        ):
            raise ValueError(
                f"Forecasts, observations, and predictions for '{name}' "
                "must contain only finite values."
            )

        innovation = observed - predicted
        adjusted[name] = forecast + float(alpha) * innovation

    return adjusted