"""
JOVIAN-AP: Synthetic Observation Generator

Sample supplied physical fields at observation locations and add
controlled Gaussian observation noise.

Grid convention
---------------
x_coords and y_coords are one-dimensional, strictly increasing arrays.
Each field is a two-dimensional NumPy array with shape (ny, nx).
Observation locations are rows of (x, y).

Sampling
--------
This implementation uses nearest-grid-point sampling, not interpolation.
It generates observations from supplied fields; it does not solve the
fluid equations or run OpenFOAM.
"""

from collections.abc import Mapping

import numpy as np


def _validate_grid(x_coords, y_coords):
    """Validate one-dimensional, finite, strictly increasing grids."""

    try:
        x_coords = np.asarray(x_coords, dtype=float)
        y_coords = np.asarray(y_coords, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("Grid coordinates must be numeric.") from exc

    if x_coords.ndim != 1 or y_coords.ndim != 1:
        raise ValueError("Grid coordinates must be one-dimensional.")

    if len(x_coords) < 2 or len(y_coords) < 2:
        raise ValueError("Each grid direction needs at least two points.")

    if not np.all(np.isfinite(x_coords)):
        raise ValueError("x_coords contains non-finite values.")

    if not np.all(np.isfinite(y_coords)):
        raise ValueError("y_coords contains non-finite values.")

    if not np.all(np.diff(x_coords) > 0):
        raise ValueError("x_coords must be strictly increasing.")

    if not np.all(np.diff(y_coords) > 0):
        raise ValueError("y_coords must be strictly increasing.")

    return x_coords, y_coords


def _nearest_indices(grid, locations):
    """Return indices of the nearest grid coordinates."""

    right = np.searchsorted(grid, locations)
    right = np.clip(right, 0, len(grid) - 1)
    left = np.clip(right - 1, 0, len(grid) - 1)

    choose_left = (
        np.abs(locations - grid[left])
        <= np.abs(locations - grid[right])
    )

    return np.where(choose_left, left, right)


def _validate_noise_level(name, level):
    """Return a valid noise standard deviation as a float."""

    if isinstance(level, (bool, np.bool_)):
        raise ValueError(
            f"Noise level for '{name}' must be a numeric standard deviation."
        )

    try:
        value = float(level)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            f"Noise level for '{name}' must be numeric."
        ) from exc

    if not np.isfinite(value) or value < 0:
        raise ValueError(
            f"Noise level for '{name}' must be finite and non-negative."
        )

    return value


def generate_observations(
    x_coords,
    y_coords,
    fields,
    observation_locations,
    noise_std,
    seed=42,
):
    """
    Sample supplied fields and add Gaussian observation noise.

    Parameters
    ----------
    x_coords : array-like, shape (nx,)
        Strictly increasing x-coordinates.
    y_coords : array-like, shape (ny,)
        Strictly increasing y-coordinates.
    fields : mapping of str to array, each shape (ny, nx)
        Fields to observe, such as u and v.
    observation_locations : array-like, shape (n_obs, 2)
        Observation coordinates, with columns (x, y).
    noise_std : non-negative float or mapping of field names to floats
        Gaussian noise standard deviation. A scalar applies to all fields.
    seed : non-negative integer, default=42
        Random seed for reproducible observation noise.

    Returns
    -------
    dict
        Observation coordinates, noisy values, noise settings, grid
        indices, random seed, and sampling-method metadata.

    Notes
    -----
    Coordinates between grid points are assigned to the nearest grid point.
    Ties are resolved toward the lower coordinate. Observations outside the
    grid domain are rejected rather than clipped to the boundary.
    """

    x_coords, y_coords = _validate_grid(x_coords, y_coords)

    if not isinstance(fields, Mapping) or not fields:
        raise ValueError("fields must be a non-empty mapping.")

    if not isinstance(seed, (int, np.integer)) or isinstance(
        seed, (bool, np.bool_)
    ):
        raise ValueError("seed must be an integer.")

    if seed < 0:
        raise ValueError("seed must be non-negative.")

    try:
        locations = np.asarray(observation_locations, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("Observation locations must be numeric.") from exc

    if locations.ndim != 2 or locations.shape[1] != 2:
        raise ValueError(
            "observation_locations must have shape (n_obs, 2)."
        )

    if locations.shape[0] == 0:
        raise ValueError("At least one observation is required.")

    if not np.all(np.isfinite(locations)):
        raise ValueError("Observation locations must be finite.")

    if np.any(locations[:, 0] < x_coords[0]) or np.any(
        locations[:, 0] > x_coords[-1]
    ):
        raise ValueError("An observation lies outside the x-domain.")

    if np.any(locations[:, 1] < y_coords[0]) or np.any(
        locations[:, 1] > y_coords[-1]
    ):
        raise ValueError("An observation lies outside the y-domain.")

    if isinstance(noise_std, Mapping):
        noise_levels = dict(noise_std)
        if set(noise_levels) != set(fields):
            raise ValueError(
                "noise_std must specify exactly one level per field."
            )
    else:
        noise_levels = {name: noise_std for name in fields}

    validated_fields = {}

    for name, values in fields.items():
        if not isinstance(name, str) or not name:
            raise ValueError("Each field must have a non-empty string name.")

        try:
            array = np.asarray(values, dtype=float)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Field '{name}' must contain numeric values."
            ) from exc

        if array.shape != (len(y_coords), len(x_coords)):
            raise ValueError(
                f"Field '{name}' must have shape "
                f"({len(y_coords)}, {len(x_coords)})."
            )

        if not np.all(np.isfinite(array)):
            raise ValueError(
                f"Field '{name}' contains non-finite values."
            )

        validated_fields[name] = array

    validated_noise = {
        name: _validate_noise_level(name, level)
        for name, level in noise_levels.items()
    }

    ix = _nearest_indices(x_coords, locations[:, 0])
    iy = _nearest_indices(y_coords, locations[:, 1])

    rng = np.random.default_rng(int(seed))
    observations = {}

    for name, array in validated_fields.items():
        sampled_values = array[iy, ix]
        noise = rng.normal(
            loc=0.0,
            scale=validated_noise[name],
            size=len(locations),
        )
        observations[name] = sampled_values + noise

    return {
        "x": locations[:, 0].copy(),
        "y": locations[:, 1].copy(),
        "values": observations,
        "noise_std": validated_noise,
        "grid_indices": {
            "ix": ix.copy(),
            "iy": iy.copy(),
        },
        "seed": int(seed),
        "sampling_method": "nearest_grid_point",
    }