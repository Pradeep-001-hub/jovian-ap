"""
JOVIAN-AP: Conservative shallow-water fluxes.

This module defines the physical fluxes and Coriolis source term for
the rotating shallow-water equations in conservative variables.

State vector:
    U = [h, hu, hv]

where:
    h  : layer thickness
    hu : zonal momentum per unit area
    hv : meridional momentum per unit area

The functions in this module evaluate physical fluxes only. They do not
yet implement numerical interface fluxes, spatial discretisation,
boundary conditions, or time integration.
"""

import numpy as np


def _validate_state_vector(state, gravity):
    """Validate a conservative state array with final dimension of 3."""

    try:
        state = np.asarray(state, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("State must contain numeric values.") from exc

    if state.ndim < 1 or state.shape[-1] != 3:
        raise ValueError(
            "State must have a final dimension of length 3: [h, hu, hv]."
        )

    if state.size == 0:
        raise ValueError("State must not be empty.")

    if not np.all(np.isfinite(state)):
        raise ValueError("State must contain only finite values.")

    if np.any(state[..., 0] <= 0.0):
        raise ValueError("Layer thickness must be strictly positive.")

    if isinstance(gravity, (bool, np.bool_)):
        raise ValueError("Gravity must be a finite positive number.")

    try:
        gravity = float(gravity)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("Gravity must be numeric.") from exc

    if not np.isfinite(gravity) or gravity <= 0.0:
        raise ValueError("Gravity must be a finite positive number.")

    return state, gravity


def physical_flux_x(state, gravity):
    """
    Evaluate the physical flux in the x-direction.

    Parameters
    ----------
    state : array-like, shape (..., 3)
        Conservative state [h, hu, hv].
    gravity : float
        Positive gravitational acceleration.

    Returns
    -------
    numpy.ndarray
        Flux with the same shape as state.

    Notes
    -----
    F = [hu, (hu)^2/h + g*h^2/2, (hu)(hv)/h].
    """

    state, gravity = _validate_state_vector(state, gravity)

    h = state[..., 0]
    hu = state[..., 1]
    hv = state[..., 2]

    flux = np.empty_like(state, dtype=float)
    flux[..., 0] = hu
    flux[..., 1] = hu * hu / h + 0.5 * gravity * h * h
    flux[..., 2] = hu * hv / h

    return flux


def physical_flux_y(state, gravity):
    """
    Evaluate the physical flux in the y-direction.

    Parameters
    ----------
    state : array-like, shape (..., 3)
        Conservative state [h, hu, hv].
    gravity : float
        Positive gravitational acceleration.

    Returns
    -------
    numpy.ndarray
        Flux with the same shape as state.

    Notes
    -----
    G = [hv, (hu)(hv)/h, (hv)^2/h + g*h^2/2].
    """

    state, gravity = _validate_state_vector(state, gravity)

    h = state[..., 0]
    hu = state[..., 1]
    hv = state[..., 2]

    flux = np.empty_like(state, dtype=float)
    flux[..., 0] = hv
    flux[..., 1] = hu * hv / h
    flux[..., 2] = hv * hv / h + 0.5 * gravity * h * h

    return flux


def coriolis_source(state, coriolis_parameter):
    """
    Evaluate the Coriolis source term in conservative variables.

    Parameters
    ----------
    state : array-like, shape (..., 3)
        Conservative state [h, hu, hv].
    coriolis_parameter : scalar or array-like
        Coriolis parameter f. It must be broadcastable to the
        spatial shape of state, state.shape[:-1].

    Returns
    -------
    numpy.ndarray
        Source with the same shape as state.

    Notes
    -----
    S = [0, f*hv, -f*hu].

    The source corresponds to the momentum equations with the
    Coriolis terms written on the right-hand side.
    """

    try:
        state = np.asarray(state, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("State must contain numeric values.") from exc

    if state.ndim < 1 or state.shape[-1] != 3:
        raise ValueError(
            "State must have a final dimension of length 3: [h, hu, hv]."
        )

    if state.size == 0:
        raise ValueError("State must not be empty.")

    if not np.all(np.isfinite(state)):
        raise ValueError("State must contain only finite values.")

    if np.any(state[..., 0] <= 0.0):
        raise ValueError("Layer thickness must be strictly positive.")

    try:
        f = np.asarray(coriolis_parameter, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("Coriolis parameter must be numeric.") from exc

    if not np.all(np.isfinite(f)):
        raise ValueError("Coriolis parameter must contain finite values.")

    try:
        f = np.broadcast_to(f, state.shape[:-1])
    except ValueError as exc:
        raise ValueError(
            "Coriolis parameter must be broadcastable to the state grid."
        ) from exc

    source = np.zeros_like(state, dtype=float)
    source[..., 1] = f * state[..., 2]
    source[..., 2] = -f * state[..., 1]

    return source