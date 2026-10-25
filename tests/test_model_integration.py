import numpy as np

from src.model.initial_conditions import (
    uniform_rest_state,
    gaussian_vortex_state,
)
from src.model.simulation import run_simulation


def test_complete_model_preserves_uniform_rest_state():
    """A uniform resting layer should remain at rest."""

    initial_state = uniform_rest_state(
        nx=8,
        ny=8,
        mean_thickness=100.0,
    )

    result = run_simulation(
        initial_state,
        dt=0.001,
        num_steps=10,
        dx=1.0,
        dy=1.0,
        gravity=9.81,
        coriolis=0.0,
    )

    np.testing.assert_allclose(
        result["state"],
        initial_state,
        rtol=0.0,
        atol=1.0e-12,
    )

    assert result["steps"] == 10
    assert result["time"] == 0.01
    assert result["minimum_thickness"] > 0.0


def test_complete_model_accepts_vortex_initial_condition():
    """The complete model should evolve a valid vortex-like state."""

    initial_state = gaussian_vortex_state(
        nx=8,
        ny=8,
        mean_thickness=100.0,
        amplitude=0.01,
        width=2.0,
        dx=1.0,
        dy=1.0,
    )

    result = run_simulation(
        initial_state,
        dt=1.0e-5,
        num_steps=3,
        dx=1.0,
        dy=1.0,
        gravity=9.81,
        coriolis=0.0,
    )

    final_state = result["state"]

    assert final_state.shape == initial_state.shape
    assert np.all(np.isfinite(final_state))
    assert np.all(final_state[..., 0] > 0.0)
    assert result["steps"] == 3
    assert np.isclose(result["time"], 3.0e-5, rtol=1.0e-12)


def test_complete_model_conserves_total_thickness():
    """Periodic conservative fluxes should preserve total thickness."""

    initial_state = gaussian_vortex_state(
        nx=8,
        ny=8,
        mean_thickness=100.0,
        amplitude=0.01,
        width=2.0,
        dx=1.0,
        dy=1.0,
    )

    result = run_simulation(
        initial_state,
        dt=1.0e-5,
        num_steps=3,
        dx=1.0,
        dy=1.0,
        gravity=9.81,
        coriolis=0.0,
    )

    assert result["final_total_thickness"] == (
        result["initial_total_thickness"]
    ) or np.isclose(
        result["final_total_thickness"],
        result["initial_total_thickness"],
        rtol=1.0e-12,
        atol=1.0e-10,
    )


def test_simulation_does_not_modify_original_initial_state():
    """Running the simulation must not mutate the caller's array."""

    initial_state = uniform_rest_state(
        nx=6,
        ny=6,
        mean_thickness=50.0,
    )
    original_state = initial_state.copy()

    run_simulation(
        initial_state,
        dt=0.001,
        num_steps=2,
        dx=1.0,
        dy=1.0,
        gravity=9.81,
        coriolis=0.0,
    )

    np.testing.assert_array_equal(initial_state, original_state)