import numpy as np
import pytest

from src.model.simulation import run_simulation


def make_resting_state():
    state = np.zeros((3, 4, 3), dtype=float)
    state[..., 0] = 10.0
    return state


def test_zero_steps_preserves_initial_state():
    initial_state = make_resting_state()

    result = run_simulation(
        initial_state,
        dt=0.01,
        num_steps=0,
        dx=1.0,
        dy=1.0,
        gravity=9.81,
        coriolis=0.0,
    )

    np.testing.assert_array_equal(result["state"], initial_state)
    assert result["time"] == 0.0
    assert result["steps"] == 0


def test_uniform_resting_state_remains_unchanged():
    initial_state = make_resting_state()

    result = run_simulation(
        initial_state,
        dt=0.001,
        num_steps=5,
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


def test_simulation_time_and_step_count():
    result = run_simulation(
        make_resting_state(),
        dt=0.02,
        num_steps=10,
        dx=1.0,
        dy=1.0,
        gravity=9.81,
        coriolis=0.0,
    )

    assert result["steps"] == 10
    assert result["time"] == pytest.approx(0.2)


def test_thickness_diagnostics_are_consistent():
    result = run_simulation(
        make_resting_state(),
        dt=0.001,
        num_steps=3,
        dx=1.0,
        dy=1.0,
        gravity=9.81,
        coriolis=0.0,
    )

    assert result["initial_total_thickness"] == pytest.approx(120.0)
    assert result["final_total_thickness"] == pytest.approx(120.0)
    assert result["thickness_change"] == pytest.approx(0.0)
    assert result["minimum_thickness"] == pytest.approx(10.0)
    assert result["maximum_thickness"] == pytest.approx(10.0)


@pytest.mark.parametrize("num_steps", [-1, 1.5, True, "3"])
def test_invalid_step_count_is_rejected(num_steps):
    with pytest.raises(ValueError, match="Number of steps"):
        run_simulation(
            make_resting_state(),
            dt=0.01,
            num_steps=num_steps,
            dx=1.0,
            dy=1.0,
            gravity=9.81,
            coriolis=0.0,
        )


@pytest.mark.parametrize("dt", [0.0, -0.1, np.inf, np.nan, True])
def test_invalid_time_step_is_rejected(dt):
    with pytest.raises(ValueError, match="Time step"):
        run_simulation(
            make_resting_state(),
            dt=dt,
            num_steps=1,
            dx=1.0,
            dy=1.0,
            gravity=9.81,
            coriolis=0.0,
        )


def test_invalid_initial_thickness_is_rejected():
    state = make_resting_state()
    state[0, 0, 0] = 0.0

    with pytest.raises(ValueError, match="strictly positive"):
        run_simulation(
            state,
            dt=0.01,
            num_steps=1,
            dx=1.0,
            dy=1.0,
            gravity=9.81,
            coriolis=0.0,
        )