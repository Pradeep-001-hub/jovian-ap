"""
JOVIAN-AP: Basic simulation runner.

Connects the spatial operator and forward Euler integrator
to advance the rotating shallow-water state over time.

The state uses conservative variables:
    U = [h, hu, hv]

This is an initial numerical framework, not yet a validated
Jupiter-atmosphere simulation.
"""

import numpy as np

from src.model.time_integration import forward_euler_step
from src.model.spatial_operator import spatial_operator


def run_simulation(
    initial_state,
    *,
    dt,
    num_steps,
    dx,
    dy,
    gravity,
    coriolis,
):
    """
    Advance the shallow-water model for a specified number of steps.

    Parameters
    ----------
    initial_state : array-like, shape (ny, nx, 3)
        Initial conservative state [h, hu, hv].
    dt : float
        Positive time-step size.
    num_steps : int
        Number of time steps to execute.
    dx, dy : float
        Positive grid spacings.
    gravity : float
        Positive gravitational acceleration.
    coriolis : float or array-like
        Coriolis parameter supplied to the spatial operator.

    Returns
    -------
    dict
        Final state, final simulation time, number of steps,
        and layer-thickness diagnostics.
    """

    try:
        state = np.asarray(initial_state, dtype=float).copy()
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Initial state must contain numeric values."
        ) from exc

    if state.ndim != 3 or state.shape[-1] != 3:
        raise ValueError(
            "Initial state must have shape (ny, nx, 3)."
        )

    if state.shape[0] < 2 or state.shape[1] < 2:
        raise ValueError(
            "Grid must contain at least two cells per direction."
        )

    if not np.all(np.isfinite(state)):
        raise ValueError(
            "Initial state must contain only finite values."
        )

    if np.any(state[..., 0] <= 0.0):
        raise ValueError(
            "Initial layer thickness must be strictly positive."
        )

    if isinstance(num_steps, (bool, np.bool_)):
        raise ValueError("Number of steps must be a nonnegative integer.")

    if not isinstance(num_steps, (int, np.integer)) or num_steps < 0:
        raise ValueError("Number of steps must be a nonnegative integer.")

    if isinstance(dt, (bool, np.bool_)):
        raise ValueError("Time step must be finite and positive.")

    try:
        dt = float(dt)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            "Time step must be finite and positive."
        ) from exc

    if not np.isfinite(dt) or dt <= 0.0:
        raise ValueError("Time step must be finite and positive.")

    if num_steps > 0:
        if not callable(spatial_operator):
            raise ValueError("Spatial operator must be callable.")

        if not callable(forward_euler_step):
            raise ValueError("Time integrator must be callable.")

    initial_mass = float(np.sum(state[..., 0]))

    for _ in range(num_steps):
        state = forward_euler_step(
            state,
            dt,
            spatial_operator,
            dx=dx,
            dy=dy,
            gravity=gravity,
            coriolis=coriolis,
        )

    final_mass = float(np.sum(state[..., 0]))

    return {
        "state": state,
        "time": num_steps * dt,
        "steps": num_steps,
        "initial_total_thickness": initial_mass,
        "final_total_thickness": final_mass,
        "thickness_change": final_mass - initial_mass,
        "minimum_thickness": float(np.min(state[..., 0])),
        "maximum_thickness": float(np.max(state[..., 0])),
    }