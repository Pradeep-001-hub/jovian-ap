import numpy as np
import pytest

from src.model.spatial_operator import spatial_operator

def test_uniform_resting_state_has_zero_tendency():
"""A uniform fluid at rest should have no spatial tendency."""
ny, nx = 4, 5
gravity = 9.81
h0 = 100.0

state = np.zeros((ny, nx, 3), dtype=float)
state[..., 0] = h0

tendency = spatial_operator(
    state=state,
    dx=1000.0,
    dy=1000.0,
    gravity=gravity,
    coriolis=1.0e-4,
)

assert tendency.shape == state.shape
np.testing.assert_allclose(tendency, 0.0, atol=1.0e-12)

def test_spatial_operator_preserves_state_shape():
"""The tendency must have the same shape as the input state."""
state = np.zeros((3, 4, 3), dtype=float)
state[..., 0] = 50.0

tendency = spatial_operator(
    state, dx=1000.0, dy=2000.0,
    gravity=9.81, coriolis=0.0
)

assert tendency.shape == state.shape

def test_periodic_fluxes_conserve_total_thickness():
"""
Periodic flux differences should sum to zero globally,
apart from floating-point round-off.
"""
rng = np.random.default_rng(42)
ny, nx = 5, 6

state = np.zeros((ny, nx, 3), dtype=float)
state[..., 0] = rng.uniform(10.0, 100.0, size=(ny, nx))
state[..., 1] = rng.normal(0.0, 2.0, size=(ny, nx))
state[..., 2] = rng.normal(0.0, 2.0, size=(ny, nx))

tendency = spatial_operator(
    state,
    dx=1000.0,
    dy=1000.0,
    gravity=9.81,
    coriolis=0.0,
)

# The first conservative variable is layer thickness h.
# The Coriolis source has zero thickness component.
total_thickness_tendency = np.sum(tendency[..., 0])

assert abs(total_thickness_tendency) < 1.0e-10

@pytest.mark.parametrize("dx", [0.0, -1.0, np.inf, np.nan, True])
def test_invalid_dx_is_rejected(dx):
state = np.zeros((2, 2, 3), dtype=float)
state[..., 0] = 10.0

with pytest.raises(ValueError):
    spatial_operator(
        state, dx=dx, dy=1.0,
        gravity=9.81, coriolis=0.0
    )

@pytest.mark.parametrize("dy", [0.0, -1.0, np.inf, np.nan, True])
def test_invalid_dy_is_rejected(dy):
state = np.zeros((2, 2, 3), dtype=float)
state[..., 0] = 10.0

with pytest.raises(ValueError):
    spatial_operator(
        state, dx=1.0, dy=dy,
        gravity=9.81, coriolis=0.0
    )

def test_nonpositive_thickness_is_rejected():
state = np.zeros((2, 2, 3), dtype=float)
state[..., 0] = 10.0
state[0, 0, 0] = 0.0

with pytest.raises(ValueError, match="positive"):
    spatial_operator(
        state, dx=1.0, dy=1.0,
        gravity=9.81, coriolis=0.0
    )

def test_invalid_coriolis_shape_is_rejected():
state = np.zeros((3, 4, 3), dtype=float)
state[..., 0] = 10.0

with pytest.raises(ValueError):
    spatial_operator(
        state, dx=1.0, dy=1.0,
        gravity=9.81, coriolis=np.zeros((2, 2))
    )