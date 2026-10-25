"""
JOVIAN-AP: Rotating Shallow-Water Model Utilities

This module defines physical parameter calculations and state validation
for the rotating shallow-water model on a local beta-plane.

It does not yet implement a spatial discretisation or time integrator.
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ShallowWaterParameters:
    """Physical parameters for a local beta-plane model."""

    rotation_rate: float
    planetary_radius: float
    reference_latitude_deg: float
    gravity: float

    def __post_init__(self):
        values = (
            self.rotation_rate,
            self.planetary_radius,
            self.reference_latitude_deg,
            self.gravity,
        )

        if not all(np.isfinite(value) for value in values):
            raise ValueError("All physical parameters must be finite.")

        if self.rotation_rate <= 0:
            raise ValueError("rotation_rate must be positive.")

        if self.planetary_radius <= 0:
            raise ValueError("planetary_radius must be positive.")

        if not -90.0 <= self.reference_latitude_deg <= 90.0:
            raise ValueError(
                "reference_latitude_deg must lie between -90 and 90."
            )

        if self.gravity <= 0:
            raise ValueError("gravity must be positive.")

    @property
    def f0(self):
        """Coriolis parameter at the reference latitude, in s^-1."""

        latitude = np.deg2rad(self.reference_latitude_deg)

        return float(
            2.0 * self.rotation_rate * np.sin(latitude)
        )

    @property
    def beta(self):
        """Meridional gradient of the Coriolis parameter, in m^-1 s^-1."""

        latitude = np.deg2rad(self.reference_latitude_deg)

        return float(
            2.0
            * self.rotation_rate
            * np.cos(latitude)
            / self.planetary_radius
        )

    def coriolis_parameter(self, y):
        """
        Evaluate f(y) = f0 + beta*y.

        Parameters
        ----------
        y : array-like
            Meridional coordinates relative to the reference latitude,
            in metres.

        Returns
        -------
        float or numpy.ndarray
            Coriolis parameter in s^-1.
        """

        y = np.asarray(y, dtype=float)

        if not np.all(np.isfinite(y)):
            raise ValueError("y coordinates must be finite.")

        result = self.f0 + self.beta * y

        if result.ndim == 0:
            return float(result)

        return result


def validate_state(h, u, v):
    """
    Validate shallow-water state arrays.

    All three fields must have identical shapes and finite values.
    Layer thickness must be strictly positive.

    Returns
    -------
    tuple of numpy.ndarray
        Validated arrays (h, u, v).
    """

    try:
        h = np.asarray(h, dtype=float)
        u = np.asarray(u, dtype=float)
        v = np.asarray(v, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("State fields must contain numeric values.") from exc

    if h.shape != u.shape or h.shape != v.shape:
        raise ValueError("h, u, and v must have identical shapes.")

    if h.size == 0:
        raise ValueError("State fields must not be empty.")

    if not (
        np.all(np.isfinite(h))
        and np.all(np.isfinite(u))
        and np.all(np.isfinite(v))
    ):
        raise ValueError("State fields must contain only finite values.")

    if np.any(h <= 0):
        raise ValueError("Layer thickness h must be strictly positive.")

    return h, u, v