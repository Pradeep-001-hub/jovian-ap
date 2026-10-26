"""
JOVIAN-AP: Analytical atmospheric flow fields.

Purpose
-------
Generate reproducible, mathematically prescribed flow fields for
testing observation sampling, data assimilation, and numerical
verification workflows.

Important
---------
These are prescribed analytical fields, not claimed exact solutions
of the rotating shallow-water equations.
"""

import numpy as np


def _validate_grid(x_coords, y_coords):
    """Validate one-dimensional, strictly increasing grid coordinates."""

    x = np.asarray(x_coords, dtype=float)
    y = np.asarray(y_coords, dtype=float)

    if x.ndim != 1 or y.ndim != 1:
        raise ValueError("Grid coordinates must be one-dimensional.")

    if len(x) < 2 or len(y) < 2:
        raise ValueError("Each grid direction needs at least two points.")

    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("Grid coordinates must be finite.")

    if not np.all(np.diff(x) > 0):
        raise ValueError("x_coords must be strictly increasing.")

    if not np.all(np.diff(y) > 0):
        raise ValueError("y_coords must be strictly increasing.")

    return x, y


def zonal_jet(
    x_coords,
    y_coords,
    jet_speed=100.0,
    jet_width=1.0,
    reference_thickness=10000.0,
    thickness_amplitude=10.0,
):
    """
    Generate a smooth east-west atmospheric jet.

    The eastward velocity is a Gaussian function of latitude:

        u(y) = U0 * exp[-(y / L)^2]

    The northward velocity is zero:

        v(x, y) = 0

    The prescribed layer thickness is:

        h(y) = H + A * exp[-(y / L)^2]

    Parameters
    ----------
    x_coords, y_coords : array-like
        One-dimensional grid coordinates.
    jet_speed : float
        Maximum eastward velocity.
    jet_width : float
        Characteristic jet width, in the same length units as y.
    reference_thickness : float
        Reference fluid-layer thickness.
    thickness_amplitude : float
        Amplitude of the thickness perturbation.

    Returns
    -------
    dict
        Grid coordinates and two-dimensional fields u, v, h, eta.

    Notes
    -----
    This is a prescribed initial-condition benchmark. It is not
    automatically a steady solution of the governing equations.
    """

    x, y = _validate_grid(x_coords, y_coords)

    parameters = {
        "jet_speed": jet_speed,
        "jet_width": jet_width,
        "reference_thickness": reference_thickness,
        "thickness_amplitude": thickness_amplitude,
    }

    for name, value in parameters.items():
        if not np.isscalar(value) or not np.isfinite(value):
            raise ValueError(f"{name} must be a finite scalar.")

    if jet_width <= 0:
        raise ValueError("jet_width must be positive.")

    if reference_thickness <= 0:
        raise ValueError("reference_thickness must be positive.")

    X, Y = np.meshgrid(x, y)

    profile = np.exp(-((Y / jet_width) ** 2))

    u = jet_speed * profile
    v = np.zeros_like(u)

    eta = thickness_amplitude * profile
    h = reference_thickness + eta

    if np.any(h <= 0):
        raise ValueError("Layer thickness must remain positive.")

    return {
        "x": x.copy(),
        "y": y.copy(),
        "u": u,
        "v": v,
        "h": h,
        "eta": eta,
        "metadata": {
            "flow_type": "prescribed_zonal_jet",
            "jet_speed": float(jet_speed),
            "jet_width": float(jet_width),
            "reference_thickness": float(reference_thickness),
            "thickness_amplitude": float(thickness_amplitude),
            "is_exact_shallow_water_solution": False,
        },
    }


def gaussian_vortex(
    x_coords,
    y_coords,
    center_x=0.0,
    center_y=0.0,
    circulation_speed=50.0,
    radius=1.0,
    reference_thickness=10000.0,
    thickness_amplitude=10.0,
):
    """
    Generate a smooth, localized, rotating vortex-like velocity field.

    Define:

        r^2 = (x - xc)^2 + (y - yc)^2

        q = exp[-r^2 / (2 Rv^2)]

        u = -V0 * (y - yc) / Rv * q

        v =  V0 * (x - xc) / Rv * q

        h = H + A * exp[-r^2 / (2 Rv^2)]

    Parameters
    ----------
    x_coords, y_coords : array-like
        One-dimensional grid coordinates.
    center_x, center_y : float
        Vortex center.
    circulation_speed : float
        Velocity scale of the vortex.
    radius : float
        Characteristic vortex radius.
    reference_thickness : float
        Reference fluid-layer thickness.
    thickness_amplitude : float
        Amplitude of the thickness perturbation.

    Returns
    -------
    dict
        Grid coordinates and fields u, v, h, eta.

    Notes
    -----
    The velocity field is a prescribed vortex benchmark. The chosen
    thickness field is not guaranteed to satisfy gradient-wind
    balance or the full rotating shallow-water equations.
    """

    x, y = _validate_grid(x_coords, y_coords)

    parameters = {
        "center_x": center_x,
        "center_y": center_y,
        "circulation_speed": circulation_speed,
        "radius": radius,
        "reference_thickness": reference_thickness,
        "thickness_amplitude": thickness_amplitude,
    }

    for name, value in parameters.items():
        if not np.isscalar(value) or not np.isfinite(value):
            raise ValueError(f"{name} must be a finite scalar.")

    if radius <= 0:
        raise ValueError("radius must be positive.")

    if reference_thickness <= 0:
        raise ValueError("reference_thickness must be positive.")

    X, Y = np.meshgrid(x, y)

    dx = X - center_x
    dy = Y - center_y

    r_squared = dx**2 + dy**2
    profile = np.exp(-r_squared / (2.0 * radius**2))

    u = -circulation_speed * (dy / radius) * profile
    v = circulation_speed * (dx / radius) * profile

    eta = thickness_amplitude * profile
    h = reference_thickness + eta

    if np.any(h <= 0):
        raise ValueError("Layer thickness must remain positive.")

    return {
        "x": x.copy(),
        "y": y.copy(),
        "u": u,
        "v": v,
        "h": h,
        "eta": eta,
        "metadata": {
            "flow_type": "prescribed_gaussian_vortex",
            "center_x": float(center_x),
            "center_y": float(center_y),
            "circulation_speed": float(circulation_speed),
            "radius": float(radius),
            "reference_thickness": float(reference_thickness),
            "thickness_amplitude": float(thickness_amplitude),
            "is_exact_shallow_water_solution": False,
        },
    }