"""Forecast verification metrics for JOVIAN-AP."""

from __future__ import annotations

import numpy as np


def _validate_arrays(predictions, reference):
    """Validate and convert prediction and reference arrays."""
    predictions = np.asarray(predictions, dtype=float)
    reference = np.asarray(reference, dtype=float)

    if predictions.shape != reference.shape:
        raise ValueError(
            "Predictions and reference values must have identical shapes."
        )

    if predictions.size == 0:
        raise ValueError("Input arrays must not be empty.")

    if not np.all(np.isfinite(predictions)):
        raise ValueError("Predictions must contain only finite values.")

    if not np.all(np.isfinite(reference)):
        raise ValueError("Reference values must contain only finite values.")

    return predictions, reference


def calculate_rmse(predictions, reference):
    """Calculate root mean square error."""
    predictions, reference = _validate_arrays(predictions, reference)

    return float(np.sqrt(np.mean((predictions - reference) ** 2)))


def calculate_mae(predictions, reference):
    """Calculate mean absolute error."""
    predictions, reference = _validate_arrays(predictions, reference)

    return float(np.mean(np.abs(predictions - reference)))


def calculate_bias(predictions, reference):
    """Calculate mean signed error: predictions minus reference."""
    predictions, reference = _validate_arrays(predictions, reference)

    return float(np.mean(predictions - reference))


def calculate_metrics(predictions, reference):
    """Calculate RMSE, MAE, and bias for the same data."""
    predictions, reference = _validate_arrays(predictions, reference)

    error = predictions - reference

    return {
        "rmse": float(np.sqrt(np.mean(error**2))),
        "mae": float(np.mean(np.abs(error))),
        "bias": float(np.mean(error)),
    }