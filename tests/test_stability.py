import numpy as np
import pytest

from src.model.stability import (
    gravity_wave_speed,
    maximum_characteristic_speeds,
    cfl_time_step,
)


def test_gravity_wave_speed_matches_formula():
    speed = gravity_wave_speed(100.0, 9.81)

    assert speed == pytest.approx(np.sqrt(9.81 * 100.0))


def test_gravity_wave_speed_supports_arrays():
    thickness = np.array([25.0, 100.0])

    speed = gravity_wave_speed(thickness, 9.81)

    np.testing.assert_allclose(
        speed,
        np.sqrt(9.81 * thickness),
    )


@pytest.mark.parametrize(
    "thickness",
    [0.0, -1.0, np.nan, np.inf, [], "invalid"],
)
def test_gravity_wave_speed_rejects_invalid_thickness(thickness):
    with pytest.raises(ValueError):
        gravity_wave_speed(thickness, 9.81)


@pytest.mark.parametrize(
    "gravity",
    [0.0, -9.81, np.nan, np.inf, True, "invalid"],
)
def test_gravity_wave_speed_rejects_invalid_gravity(gravity):
    with pytest.raises(ValueError):
        gravity_wave_speed(100.0, gravity)


def test_characteristic_speeds_for_resting_state():
    state = np.zeros((2, 3, 3), dtype=float)
    state[..., 0] = 100.0

    speed_x, speed_y = maximum_characteristic_speeds(
        state,
        gravity=9.81,
    )

    expected = np.sqrt(9.81 * 100.0)

    assert speed_x == pytest.approx(expected)
    assert speed_y == pytest.approx(expected)


def
est_characteristic_speeds_include_fluid_velocity():
    state = np.zeros((2, 2, 3), dtype=float)
    state[..., 0] = 100.0
    state[..., 1] = 200.0
    state[..., 2] = -100.0

    speed_x, speed_y = maximum_characteristic_speeds(
        state,
        gravity=9.81,
    )

    wave_speed = np.sqrt(9.81 * 100.0)

    assert speed_x == pytest.approx(2.0 + wave_speed)
    assert speed_y == pytest.approx(1.0 + wave_speed)

@pytest.mark.parametrize(
    "state",
    [
        np.zeros((2, 2, 2)),
        np.zeros((2, 2, 3)) * np.nan,
        np.zeros((2, 2, 3)),
        np.array([["invalid"]]),
    ],
)
def test_characteristic_speeds_reject_invalid_state(state):
    with pytest.raises(ValueError):
        maximum_characteristic_speeds(state, 1.0)


def test_cfl_time_step_matches_formula():
    state = np.zeros((2, 2, 3), dtype=float)
    state[..., 0] = 100.0

    cfl = 0.5
    dx = 1000.0
    dy = 2000.0
    wave_speed = np.sqrt(9.81 * 100.0)

    expected = cfl / (
        wave_speed / dx + wave_speed / dy
    )

    dt = cfl_time_step(
        state,
        dx=dx,
        dy=dy,
        gravity=9.81,
        cfl=cfl,
    )

    assert dt == pytest.approx(expected)


def test_cfl_time_step_decreases_when_grid_is_refined():
    state = np.zeros((2, 2, 3), dtype=float)
    state[..., 0] = 100.0

    coarse_dt = cfl_time_step(
        state,
        dx=1000.0,
        dy=1000.0,
        gravity=9.81,
        cfl=0.5,
    )

    fine_dt = cfl_time_step(
        state,
        dx=500.0,
        dy=500.0,
        gravity=9.81,
        cfl=0.5,
    )

    assert fine_dt < coarse_dt


@pytest.mark.parametrize(
    "dx, dy, cfl",
    [
        (0.0, 100.0, 0.5),
        (100.0, -1.0, 0.5),
        (100.0, 100.0, 0.0),
        (100.0, 100.0, -0.1),
        (100.0, 100.0, 1.1),
        (np.inf, 100.0, 0.5),
        (100.0, np.nan, 0.5),
        (True, 100.0, 0.5),
    ],
)
def test_cfl_time_step_rejects_invalid_parameters(dx, dy, cfl):
    state = np.zeros((2, 2, 3), dtype=float)
    state[..., 0] = 100.0

    with pytest.raises(ValueError):
        cfl_time_step(
            state,
            dx=dx,
            dy=dy,
            gravity=9.81,
            cfl=cfl,
        )


def test_cfl_time_step_rejects_invalid_gravity():
    state = np.zeros((2, 2, 3), dtype=float)
    state[..., 0] = 100.0

    with pytest.raises(ValueError):
        cfl_time_step(
            state,
            dx=100.0,
            dy=100.0,
            gravity=-9.81,
        )