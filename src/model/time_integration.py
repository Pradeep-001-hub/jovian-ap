"""
JOVIAN-AP: Time integration.

Implements a forward Euler update for the rotating shallow-water
model using an existing spatial operator.

The method advances the conservative state by one time step.

Important:
Forward Euler is a first-order method. The caller must choose
a sufficiently small time step to maintain numerical stability.
"""

import numpy as np


def forward_euler_step(
    state,
    dt,
    spatial_operator,
    *,
    dx,
    dy,
    gravity,
    coriolis,
):
    """
    Advance a conservative state by one forward Euler time step.

    Parameters
    ----------
    state : array-like, shape (ny, nx, 3)
        Current conservative state [h, hu, hv].
    dt : float
        Positive time-step size.
    spatial_operator : callable
        Function that calculates dU/dt.
    dx, dy : float
        Positive grid spacings.
    gravity : float
        Positive gravitational acceleration.
    coriolis : float or array-like
        Coriolis parameter supplied to the spatial operator.

    Returns
    -------
    numpy.ndarray
        Updated conservative state with the same shape as the input.
    """

    try:
        state = np.asarray(state, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("State must contain numeric values.") from exc

    if state.ndim != 3 or state.shape[-1] != 3:
        raise ValueError(
            "State must have shape (ny, nx, 3), "
            "with final dimension [h, hu, hv]."
        )

    if state.shape[0] < 2 or state.shape[1] < 2:
        raise ValueError(
            "Grid must contain at least two cells per direction."
        )

    if not np.all(np.isfinite(state)):
        raise ValueError("State must contain only finite values.")

    if np.any(state[..., 0] <= 0.0):
        raise ValueError("Layer thickness must be strictly positive.")

    if isinstance(dt, (bool, np.bool_)):
        raise ValueError("Time step must be a finite positive number.")

    try:
        dt = float(dt)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            "Time step must be a finite positive number."
        ) from exc

    if not np.isfinite(dt) or dt <= 0.0:
        raise ValueError("Time step must be a finite positive number.")

    if not callable(spatial_operator):
        raise ValueError("Spatial operator must be callable.")

    tendency = np.asarray(
        spatial_operator(
            state,
            dx=dx,
            dy=dy,
            gravity=gravity,
            coriolis=coriolis,
        ),
        dtype=float,
    )

    if tendency.shape != state.shape:
        raise ValueError(
            "Spatial operator must return an array with the same "
            "shape as the state."
        )

    if not np.all(np.isfinite(tendency)):
        raise ValueError(
            "Spatial operator returned non-finite values."
        )

    updated_state = state + dt * tendency

    if not np.all(np.isfinite(updated_state)):
        raise ValueError(
            "Time integration produced non-finite state values."
        )

    if np.any(updated_state[..., 0] <= 0.0):
        raise ValueError(
            "Time step produced nonpositive layer thickness. "
            "Reduce the time step or use a suitable positivity-preserving method."
        )

    return updated_state