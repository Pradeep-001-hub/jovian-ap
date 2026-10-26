"""Map model fields to predicted observations.

This module predicts observations from a supplied model state.
It does not generate synthetic noise or modify the model fields.

Sampling currently uses nearest-grid-point sampling.
"""

from __future__ import annotations

import numpy as np


def observation_operator(
    x_coords,
    y_coords,
    fields,
    observation_locations,
):
    """Sample model fields at specified observation locations.

    Parameters
    ----------
    x_coords : array-like, shape (nx,)
        Strictly increasing east-west grid coordinates.
    y_coords : array-like, shape (ny,)
        Strictly increasing north-south grid coordinates.
    fields : dict[str, array-like], each shape (ny, nx)
        Model fields to sample, such as ``u``, ``v``, and ``h``.
    observation_locations : array-like, shape (n_observations, 2)
        Observation coordinates in ``(x, y)`` order.

    Returns
    -------
    dict
        Contains observation coordinates, predicted field values,
        grid indices, and the sampling method.

    Notes
    -----
    Nearest-grid-point sampling is used, not interpolation.
    Midpoint ties select the lower coordinate.
    Locations outside the grid domain are rejected.
    """

    x = np.asarray(x_coords, dtype=float)
    y = np.asarray(y_coords, dtype=float)
    locations = np.asarray(observation_locations, dtype=float)

    if x.ndim != 1 or y.ndim != 1:
        raise ValueError("Grid coordinates must be one-dimensional.")

    if x.size < 2 or y.size < 2:
        raise ValueError("Each grid coordinate array must contain at least two points.")

    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("Grid coordinates must contain only finite values.")

    if np.any(np.diff(x) <= 0) or np.any(np.diff(y) <= 0):
        raise ValueError("Grid coordinates must be strictly increasing.")

    if locations.ndim != 2 or locations.shape[1] != 2:
        raise ValueError(
            "Observation locations must have shape (n_observations, 2)."
        )

    if locations.shape[0] == 0:
        raise ValueError("At least one observation location is required.")

    if not np.all(np.isfinite(locations)):
        raise ValueError("Observation locations must contain only finite values.")

    if np.any(locations[:, 0] < x[0]) or np.any(locations[:, 0] > x[-1]):
        raise ValueError("Observation x-coordinates must lie inside the grid domain.")

    if np.any(locations[:, 1] < y[0]) or np.any(locations[:, 1] > y[-1]):
        raise ValueError("Observation y-coordinates must lie inside the grid domain.")

    if not isinstance(fields, dict) or not fields:
        raise ValueError("fields must be a non-empty dictionary.")

    validated_fields = {}

    for name, field in fields.items():
        if not isinstance(name, str) or not name:
            raise ValueError("Every field must have a non-empty string name.")

        array = np.asarray(field, dtype=float)

        if array.shape != (y.size, x.size):
            raise ValueError(
                f"Field '{name}' must have shape "
                f"({y.size}, {x.size}); got {array.shape}."
            )

        if not np.all(np.isfinite(array)):
            raise ValueError(f"Field '{name}' must contain only finite values.")

        validated_fields[name] = array

    # Search each coordinate array independently.
    # On an exact midpoint, select the lower coordinate.
    def nearest_indices(grid, points):
        upper = np.searchsorted(grid, points, side="left")
        upper = np.clip(upper, 0, grid.size - 1)
        lower = np.clip(upper - 1, 0, grid.size - 1)

        lower_distance = np.abs(points - grid[lower])
        upper_distance = np.abs(grid[upper] - points)

        choose_lower = lower_distance <= upper_distance
        return np.where(choose_lower, lower, upper)

    x_indices = nearest_indices(x, locations[:, 0])
    y_indices = nearest_indices(y, locations[:, 1])

    predicted_values = {
        name: array[y_indices, x_indices].copy()
        for name, array in validated_fields.items()
    }

    return {
        "x": locations[:, 0].copy(),
        "y": locations[:, 1].copy(),
        "values": predicted_values,
        "grid_indices": np.column_stack((x_indices, y_indices)),
        "sampling_method": "nearest_grid_point",
    }