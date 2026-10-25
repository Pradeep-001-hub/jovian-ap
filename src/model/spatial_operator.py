"""
JOVIAN-AP: Finite-volume spatial operator.

Calculates the spatial flux divergence and Coriolis source term
for a two-dimensional rotating shallow-water state.

State shape:
(ny, nx, 3)

Final state dimension:
[h, hu, hv]

Boundary conditions:
Periodic in x and y.

Important:
Periodic boundaries are a numerical starting point. A periodic
y-domain is not generally compatible with a non-periodic beta-plane
Coriolis parameter. Use constant Coriolis parameter for periodic-y
tests until suitable physical boundary conditions are implemented.

This module calculates dU/dt; it does not perform time integration.
"""

import numpy as np

from src.model.finite_volume import coriolis_source
from src.model.numerical_flux import rusanov_flux_x, rusanov_flux_y

def spatial_operator(state, dx, dy, gravity, coriolis):
try:
state = np.asarray(state, dtype=float)
except (TypeError, ValueError) as exc:
raise ValueError("State must contain numeric values.") from exc

if state.ndim != 3 or state.shape[-1] != 3:
    raise ValueError(
        "State must have shape (ny, nx, 3), "
        "with final dimension [h, hu, hv]."
    )

ny, nx, _ = state.shape

if nx < 2 or ny < 2:
    raise ValueError(
        "Grid must contain at least two cells per direction."
    )

if not np.all(np.isfinite(state)):
    raise ValueError("State must contain only finite values.")

if np.any(state[..., 0] <= 0.0):
    raise ValueError("Layer thickness must be strictly positive.")

for name, spacing in (("dx", dx), ("dy", dy)):
    if isinstance(spacing, (bool, np.bool_)):
        raise ValueError(
            f"{name} must be a finite positive number."
        )

    try:
        spacing = float(spacing)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            f"{name} must be a finite positive number."
        ) from exc

    if not np.isfinite(spacing) or spacing <= 0.0:
        raise ValueError(
            f"{name} must be a finite positive number."
        )

    if name == "dx":
        dx = spacing
    else:
        dy = spacing

try:
    gravity = float(gravity)
except (TypeError, ValueError, OverflowError) as exc:
    raise ValueError(
        "Gravity must be a finite positive number."
    ) from exc

if not np.isfinite(gravity) or gravity <= 0.0:
    raise ValueError(
        "Gravity must be a finite positive number."
    )

# Calculate numerical fluxes across x-direction interfaces.
state_right = np.roll(state, -1, axis=1)
flux_x = rusanov_flux_x(state, state_right, gravity)

# Calculate numerical fluxes across y-direction interfaces.
state_upper = np.roll(state, -1, axis=0)
flux_y = rusanov_flux_y(state, state_upper, gravity)

# Calculate conservative flux divergence.
divergence_x = (
    flux_x - np.roll(flux_x, 1, axis=1)
) / dx

divergence_y = (
    flux_y - np.roll(flux_y, 1, axis=0)
) / dy

# Calculate the Coriolis source term.
source = coriolis_source(state, coriolis)

# Return the instantaneous time derivative of the state.
return -divergence_x - divergence_y + source