import numpy as np

from src.model.stability import cfl_time_step
from src.model.time_integration import forward_euler_step

def run_simulation(
initial_state,
*,
dt,
num_steps,
dx,
dy,
gravity,
coriolis,
cfl=None,
):
"""
Advance a shallow-water state through a fixed number of time steps.

Parameters
----------
initial_state : array_like
    Conservative state with shape (ny, nx, 3), storing
    [h, h*u, h*v].
dt : float
    Requested time step in seconds.
num_steps : int
    Number of time steps to perform.
dx, dy : float
    Grid spacings in the x and y directions.
gravity : float
    Positive gravity parameter.
coriolis : float or array_like
    Coriolis parameter used by the spatial operator.
cfl : float or None, optional
    If provided, check the requested time step against the
    estimated CFL time-step limit before every step.
    Must be positive and no greater than 1.
    If None, no CFL check is performed.

Returns
-------
dict
    Final state, elapsed time, step count, and thickness diagnostics.

Notes
-----
The CFL estimate is a stability guideline, not a proof that the
complete numerical scheme is stable or physically accurate.
"""

state = np.array(initial_state, dtype=float, copy=True)

if state.ndim != 3 or state.shape[-1] != 3:
    raise ValueError(
        "initial_state must have shape (ny, nx, 3)."
    )

if state.shape[0] < 2 or state.shape[1] < 2:
    raise ValueError(
        "The state must contain at least two cells in each direction."
    )

if not np.all(np.isfinite(state)):
    raise ValueError("initial_state must contain only finite values.")

if np.any(state[..., 0] <= 0.0):
    raise ValueError("Initial layer thickness must be positive.")

if isinstance(num_steps, (bool, np.bool_)):
    raise ValueError("num_steps must be a non-negative integer.")

if not isinstance(num_steps, (int, np.integer)) or num_steps < 0:
    raise ValueError("num_steps must be a non-negative integer.")

if isinstance(dt, (bool, np.bool_)):
    raise ValueError("dt must be finite and positive.")

if not np.isscalar(dt) or not np.isfinite(dt) or dt <= 0.0:
    raise ValueError("dt must be finite and positive.")

if cfl is not None:
    if isinstance(cfl, (bool, np.bool_)):
        raise ValueError("cfl must be positive and no greater than 1.")

    if not np.isscalar(cfl) or not np.isfinite(cfl):
        raise ValueError("cfl must be positive and no greater than 1.")

    if cfl <= 0.0 or cfl > 1.0:
        raise ValueError("cfl must be positive and no greater than 1.")

initial_thickness = float(np.sum(state[..., 0]))

for _ in range(num_steps):
    if cfl is not None:
        dt_limit = cfl_time_step(
            state,
            dx,
            dy,
            gravity,
            cfl=cfl,
        )

        tolerance = 1.0e-12 * max(1.0, abs(dt_limit))

        if dt > dt_limit + tolerance:
            raise ValueError(
                f"Requested dt ({dt}) exceeds the estimated "
                f"CFL time-step limit ({dt_limit}). "
                "Reduce dt or refine the time integration."
            )

    state = forward_euler_step(
        state,
        dt,
        _spatial_operator,
        dx=dx,
        dy=dy,
        gravity=gravity,
        coriolis=coriolis,
    )

final_thickness = float(np.sum(state[..., 0]))

return {
    "state": state,
    "time": float(num_steps * dt),
    "steps": int(num_steps),
    "initial_total_thickness": initial_thickness,
    "final_total_thickness": final_thickness,
    "total_thickness_change": final_thickness - initial_thickness,
    "minimum_thickness": float(np.min(state[..., 0])),
    "maximum_thickness": float(np.max(state[..., 0])),
}

def _spatial_operator(state, *, dx, dy, gravity, coriolis):
"""Adapter connecting the simulation to the spatial discretisation."""
from src.model.spatial_operator import spatial_operator

return spatial_operator(
    state,
    dx=dx,
    dy=dy,
    gravity=gravity,
    coriolis=coriolis,
)