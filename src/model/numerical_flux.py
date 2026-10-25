"""
JOVIAN-AP: Rusanov numerical fluxes.

This module calculates numerical interface fluxes for the conservative
rotating shallow-water model.

State:
    U = [h, hu, hv]

The numerical flux uses the local Lax-Friedrichs (Rusanov) method.
It estimates wave speeds from the shallow-water gravity-wave speed.

This module does not implement a grid, boundary conditions, or
time integration.
"""

import numpy as np

from src.model.finite_volume import (
    physical_flux_x,
    physical_flux_y,
)


def _validate_pair(left, right, gravity):
    """Validate two conservative states and gravitational acceleration."""

    try:
        left = np.asarray(left, dtype=float)
        right = np.asarray(right, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("States must contain numeric values.") from exc

    if left.ndim < 1 or right.ndim < 1:
        raise ValueError("States must have at least one dimension.")

    if left.shape != right.shape:
        raise ValueError("Left and right states must have identical shapes.")

    if left.shape[-1] != 3:
        raise ValueError(
            "States must have a final dimension of length 3: [h, hu, hv]."
        )

    if left.size == 0:
        raise ValueError("States must not be empty.")

    if not np.all(np.isfinite(left)) or not np.all(np.isfinite(right)):
        raise ValueError("States must contain only finite values.")

    if np.any(left[..., 0] <= 0.0) or np.any(right[..., 0] <= 0.0):
        raise ValueError("Layer thickness must be strictly positive.")

    if isinstance(gravity, (bool, np.bool_)):
        raise ValueError("Gravity must be a finite positive number.")

    try:
        gravity = float(gravity)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("Gravity must be numeric.") from exc

    if not np.isfinite(gravity) or gravity <= 0.0:
        raise ValueError("Gravity must be a finite positive number.")

    return left, right, gravity


def rusanov_flux_x(left, right, gravity):
    """
    Calculate the Rusanov numerical flux across an x-normal interface.

    Parameters
    ----------
    left, right : array-like, shape (..., 3)
        Conservative states [h, hu, hv] on either side of the interface.
    gravity : float
        Positive gravitational acceleration.

    Returns
    -------
    numpy.ndarray
        Numerical flux with the same shape as the input states.
    """

    left, right, gravity = _validate_pair(left, right, gravity)

    flux_left = physical_flux_x(left, gravity)
    flux_right = physical_flux_x(right, gravity)

    h_left = left[..., 0]
    h_right = right[..., 0]

    u_left = left[..., 1] / h_left
    u_right = right[..., 1] / h_right

    speed_left = np.abs(u_left) + np.sqrt(gravity * h_left)
    speed_right = np.abs(u_right) + np.sqrt(gravity * h_right)

    alpha = np.maximum(speed_left, speed_right)[..., np.newaxis]

    return (
        0.5 * (flux_left + flux_right)
        - 0.5 * alpha * (right - left)
    )


def rusanov_flux_y(lower, upper, gravity):
    """
    Calculate the Rusanov numerical flux across a y-normal interface.

    Parameters
    ----------
    lower, upper : array-like, shape (..., 3)
        Conservative states on either side of the interface.
        The names refer to their positions in the y-direction.
    gravity : float
        Positive gravitational acceleration.

    Returns
    -------
    numpy.ndarray
        Numerical flux with the same shape as the input states.
    """

    lower, upper, gravity = _validate_pair(lower, upper, gravity)

    flux_lower = physical_flux_y(lower, gravity)
    flux_upper = physical_flux_y(upper, gravity)

    h_lower = lower[..., 0]
    h_upper = upper[..., 0]

    v_lower = lower[..., 2] / h_lower
    v_upper = upper[..., 2] / h_upper

    speed_lower = np.abs(v_lower) + np.sqrt(gravity * h_lower)
    speed_upper = np.abs(v_upper) + np.sqrt(gravity * h_upper)

    alpha = np.maximum(speed_lower, speed_upper)[..., np.newaxis]

    return (
        0.5 * (flux_lower + flux_upper)
        - 0.5 * alpha * (upper - lower)
    )