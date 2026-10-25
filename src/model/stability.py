"""
JOVIAN-AP: Numerical stability utilities.

Provides gravity-wave speed, characteristic-speed estimates,
and a CFL-based time-step estimate for the shallow-water model.

These estimates help choose a time step for an explicit method.
They do not guarantee stability for every numerical configuration.
"""

import numpy as np


def gravity_wave_speed(thickness, gravity):
    """
    Calculate the local shallow-water gravity-wave speed.

    c = sqrt(g * h)

    Parameters
    ----------
    thickness : array-like
        Positive layer thickness.
    gravity : float
        Positive gravitational acceleration.

    Returns
    -------
    float or numpy.ndarray
        Gravity-wave speed in m/s.
    """

    if isinstance(gravity, (bool, np.bool_)):
        raise ValueError("Gravity must be finite and positive.")

    try:
        gravity = float(gravity)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            "Gravity must be finite and positive."
        ) from exc

    if not np.isfinite(gravity) or gravity <= 0.0:
        raise ValueError("Gravity must be finite and positive.")

    try:
        thickness = np.asarray(thickness, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("Thickness must contain numeric values.") from exc

    if thickness.size == 0:
        raise ValueError("Thickness must not be empty.")

    if not np.all(np.isfinite(thickness)) or np.any(thickness <= 0.0):
        raise ValueError("Thickness must be finite and positive.")

    return np.sqrt(gravity * thickness)


def maximum_characteristic_speeds(state, gravity):
    """
    Estimate maximum characteristic speeds in x and y.

    The conservative state is U = [h, hu, hv].

    Local speeds:
        a_x = abs(u) + sqrt(g*h)
        a_y = abs(v) + sqrt(g*h)

    Parameters
    ----------
    state : array-like, shape (..., 3)
        Conservative state [h, hu, hv].
    gravity : float
        Positive gravitational acceleration.

    Returns
    -------
    tuple of float
        Maximum characteristic speeds (a_x, a_y).
    """

    if isinstance(gravity, (bool, np.bool_)):
        raise ValueError("Gravity must be finite and positive.")

    try:
        gravity = float(gravity)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            "Gravity must be finite and positive."
        ) from exc

    if not np.isfinite(gravity) or gravity <= 0.0:
        raise ValueError("Gravity must be finite and positive.")

    try:
        state = np.asarray(state, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("State must contain numeric values.") from exc

    if state.ndim < 1 or state.shape[-1] != 3 or state.size == 0:
        raise ValueError(
            "State must be non-empty and have final dimension 3."
        )

    if not np.all(np.isfinite(state)):
        raise ValueError("State must contain only finite values.")

    thickness = state[..., 0]

    if np.any(thickness <= 0.0):
        raise ValueError("Layer thickness must be positive.")

    u = state[..., 1] / thickness
    v = state[..., 2] / thickness
    wave_speed = np.sqrt(gravity * thickness)

    speed_x = float(np.max(np.abs(u) + wave_speed))
    speed_y = float(np.max(np.abs(v) + wave_speed))

    return speed_x, speed_y


def cfl_time_step(state, dx, dy, gravity, cfl=0.5):
    """
    Estimate an explicit time step from the multidimensional CFL limit.

    dt = CFL / (max(a_x)/dx + max(a_y)/dy)

    where a_x and a_y are maximum shallow-water characteristic speeds.

    Parameters
    ----------
    state : array-like, shape (..., 3)
        Conservative state [h, hu, hv].
    dx, dy : float
        Positive grid spacings.
    gravity : float
        Positive gravitational acceleration.
    cfl : float
        Positive CFL factor, no greater than 1.

    Returns
    -------
    float
        Estimated maximum time step in seconds.
    """

    def positive_finite(name, value):
        if isinstance(value, (bool, np.bool_)):
            raise ValueError(f"{name} must be finite and positive.")

        try:
            value = float(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(
                f"{name} must be finite and positive."
            ) from exc

        if not np.isfinite(value) or value <= 0.0:
            raise ValueError(f"{name} must be finite and positive.")

        return value

    dx = positive_finite("dx", dx)
    dy = positive_finite("dy", dy)
    cfl = positive_finite("CFL", cfl)

    if cfl > 1.0:
        raise ValueError("CFL must not exceed 1.0.")

    speed_x, speed_y = maximum_characteristic_speeds(
        state, gravity
    )

    denominator = speed_x / dx + speed_y / dy

    if not np.isfinite(denominator) or denominator <= 0.0:
        raise ValueError(
            "Could not calculate a finite positive CFL denominator."
        )

    dt = cfl / denominator

    if not np.isfinite(dt) or dt <= 0.0:
        raise ValueError("Calculated time step is not finite and positive.")

    return float(dt)