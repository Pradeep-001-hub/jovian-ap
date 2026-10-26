"""Calculate observation innovations for JOVIAN-AP.

The innovation is the difference between an observation and
the corresponding model-predicted observation:

    d = y - H(x_f)

This module calculates innovations only. It does not update
the model state or perform data assimilation.
"""

from __future__ import annotations

import numpy as np


def calculate_innovations(observations, predicted_values):
    """Calculate innovations for one or more observed variables.

    Parameters
    ----------
    observations : dict[str, array-like]
        Observed values for each variable, such as ``u``, ``v``,
        or ``h``. Each array has shape (n_observations,).

    predicted_values : dict[str, array-like]
        Model-predicted observations for the same variables,
        with matching array shapes.

    Returns
    -------
    dict[str, numpy.ndarray]
        Innovation arrays calculated as observations minus
        predicted values.

    Raises
    ------
    ValueError
        If the inputs are invalid, variable names do not match,
        array shapes differ, or values are non-finite.

    Notes
    -----
    Positive innovation means the observation exceeds the
    model prediction. Negative innovation means the observation
    is below the model prediction.
    """

    if not isinstance(observations, dict) or not observations:
        raise ValueError("observations must be a non-empty dictionary.")

    if not isinstance(predicted_values, dict) or not predicted_values:
        raise ValueError("predicted_values must be a non-empty dictionary.")

    if set(observations) != set(predicted_values):
        raise ValueError(
            "Observations and predictions must contain the same variables."
        )

    innovations = {}

    for name in observations:
        if not isinstance(name, str) or not name:
            raise ValueError(
                "Every observed variable must have a non-empty string name."
            )

        observed = np.asarray(observations[name], dtype=float)
        predicted = np.asarray(predicted_values[name], dtype=float)

        if observed.ndim != 1 or predicted.ndim != 1:
            raise ValueError(
                f"Values for '{name}' must be one-dimensional arrays."
            )

        if observed.size == 0:
            raise ValueError(
                f"Values for '{name}' must contain at least one observation."
            )

        if observed.shape != predicted.shape:
            raise ValueError(
                f"Observation and prediction shapes differ for '{name}': "
                f"{observed.shape} versus {predicted.shape}."
            )

        if not np.all(np.isfinite(observed)):
            raise ValueError(
                f"Observations for '{name}' must contain only finite values."
            )

        if not np.all(np.isfinite(predicted)):
            raise ValueError(
                f"Predictions for '{name}' must contain only finite values."
            )

        innovations[name] = observed - predicted

    return innovations