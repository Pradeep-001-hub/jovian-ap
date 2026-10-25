"""
JOVIAN-AP: Initial conditions for shallow-water simulations.

Provides simple, reproducible initial states for testing the
rotating shallow-water numerical model.

The conservative state is U = [h, hu, hv].

The vortex generated here is an idealised initial condition.
It is not claimed to be an exact steady-state solution.
"""

import numpy as np


def uniform_rest_state(nx, ny, mean_thickness):
    """
    Generate a uniform layer at rest.

    Parameters
    ----------
    nx, ny : int
        Number of grid cells in the x and y directions.
    mean_thickness : float
        Uniform layer thickness; must be finite and positive.

    Returns
    -------
    numpy.ndarray
        State array with shape (ny, nx, 3).
        Components are [h, hu, hv].
    """

    for name, value in (("nx", nx), ("ny", ny)):
        if isinstance(value, (bool, np.bool_)):
            raise ValueError(f"{name} must be a positive integer.")
        if not isinstance(value, (int, np.integer)) or value < 2:
            raise ValueError(f"{name} must be an integer of at least 2.")

    if isinstance(mean_thickness, (bool, np.bool_)):
        raise ValueError("Mean thickness must be finite and positive.")

    try:
        mean_thickness = float(mean_thickness)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            "Mean thickness must be finite and positive."
        ) from exc

    if not np.isfinite(mean_thickness) or mean_thickness <= 0.0:
        raise ValueError("Mean thickness must be finite and positive.")

    state = np.zeros((ny, nx, 3), dtype=float)
    state[..., 0] = mean_thickness

    return state


def gaussian_vortex_state(
    nx,
    ny,
    mean_thickness,
    amplitude,
    width,
    *,
    dx=1.0,
    dy=1.0,
):
    """
    Generate an idealised Gaussian vortex-like velocity field.

    A smooth tangential velocity is constructed around the domain
    centre. Layer thickness is initially uniform.

    This is a numerical test condition, not a geostrophically
    balanced shallow-water vortex.

    Parameters
    ----------
    nx, ny : int
        Grid-cell counts, each at least 2.
    mean_thickness : float
        Uniform positive layer thickness.
    amplitude : float
        Velocity scale in m/s. May be positive or negative.
    width : float
        Positive vortex length scale, in the same units as dx and dy.
    dx, dy : float
        Positive grid spacings.

    Returns
    -------
    numpy.ndarray
        Conservative state array of shape (ny, nx, 3).
    """

    for name, value in (("nx", nx), ("ny", ny)):
        if isinstance(value, (bool, np.bool_)):
            raise ValueError(f"{name} must be a positive integer.")
        if not isinstance(value, (int, np.integer)) or value < 2:
            raise ValueError(f"{name} must be an integer of at least 2.")

    def finite_float(name, value):
        if isinstance(value, (bool, np.bool_)):
            raise ValueError(f"{name} must be finite.")
        try:
            value = float(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"{name} must be finite.") from exc
        if not np.isfinite(value):
            raise ValueError(f"{name} must be finite.")
        return value

    mean_thickness = finite_float("Mean thickness", mean_thickness)
    amplitude = finite_float("Amplitude", amplitude)
    width = finite_float("Width", width)
    dx = finite_float("dx", dx)
    dy = finite_float("dy", dy)

    if mean_thickness <= 0.0:
        raise ValueError("Mean thickness must be positive.")
    if width <= 0.0:
        raise ValueError("Width must be positive.")
    if dx <= 0.0 or dy <= 0.0:
        raise ValueError("Grid spacings must be positive.")

    x = (np.arange(nx) - (nx - 1) / 2.0) * dx
    y = (np.arange(ny) - (ny - 1) / 2.0) * dy
    X, Y = np.meshgrid(x, y)

    radius_squared = X**2 + Y**2
    envelope = np.exp(-radius_squared / (2.0 * width**2))

    u = -amplitude * (Y / width) * envelope
    v = amplitude * (X / width) * envelope

    state = np.zeros((ny, nx, 3), dtype=float)
    state[..., 0] = mean_thickness
    state[..., 1] = mean_thickness * u
    state[..., 2] = mean_thickness * v

    return state