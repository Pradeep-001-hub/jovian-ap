import numpy as np
import pytest

from src.model.time_integration import forward_euler_step


def test_forward_euler_matches_hand_calculated_update():
    state = np.zeros((2, 2, 3), dtype=float)
    state[..., 0] = 10.0
    state[..., 1] = 2.0
    state[..., 2] = -1.0

    def constant_tendency(
        state, *, dx, dy, gravity, coriolis
    ):
        tendency = np.zeros_like(state)
        tendency[..., 0] = 0.5
        tendency[..., 1] = 2.0
        tendency[..., 2] = -4.0
        return tendency

    dt = 0.1

    updated = forward_euler_step(
        state,
        dt,
        constant_tendency,
        dx=1.0,
        dy=1.0,
        gravity=9.81,
        coriolis=0.0,
    )

    expected = state + dt * np.array([0.5, 2.0, -4.0])

    np.testing.assert_allclose(updated, expected)
    assert updated.shape == state.shape


def test_forward_euler_does_not_modify_input_state():
    state = np.zeros((2, 3, 3), dtype=float)
    state[..., 0] = 10.0
    original = state.copy()

    def zero_tendency(
        state, *, dx, dy, gravity, coriolis
    ):
        return np.zeros_like(state)

    forward_euler_step(
        state,
        0.1,
        zero_tendency,
        dx=1.0,
        dy=1.0,
        gravity=9.81,
        coriolis=0.0,
    )

    np.testing.assert_array_equal(state, original)


def test_zero_tendency_leaves_state_unchanged():
    state = np.zeros((2, 2, 3), dtype=float)
    state[..., 0] = 25.0
    state[..., 1] = 3.0
    state[..., 2] = -2.0

    def zero_tendency(
        state, *, dx, dy, gravity, coriolis
    ):
        return np.zeros_like(state)

    updated = forward_euler_step(
        state,
        0.01,
        zero_tendency,
        dx=100.0,
        dy=100.0,
        gravity=9.81,
        coriolis=1.0e-4,
    )

    np.testing.assert_allclose(updated, state)


@pytest.mark.parametrize("dt", [0.0, -0.1, np.inf, np.nan, True])
def test_invalid_time_step_is_rejected(dt):
    state = np.zeros((2, 2, 3), dtype=float)
    state[..., 0] = 10.0

    def zero_tendency(
        state, *, dx, dy, gravity, coriolis
    ):
        return np.zeros_like(state)

    with pytest.raises(ValueError, match="Time step"):
        forward_euler_step(
            state,
            dt,
            zero_tendency,
            dx=1.0,
            dy=1.0,
            gravity=9.81,
            coriolis=0.0,
        )


def test_incorrect_tendency_shape_is_rejected():
    state = np.zeros((2, 2, 3), dtype=float)
    state[..., 0] = 10.0

    def incorrect_tendency(
        state, *, dx, dy, gravity, coriolis
    ):
        return np.zeros((2, 2))

    with pytest.raises(ValueError, match="same shape"):
        forward_euler_step(
            state,
            0.01,
            incorrect_tendency,
            dx=1.0,
            dy=1.0,
            gravity=9.81,
            coriolis=0.0,
        )


def test_nonfinite_tendency_is_rejected():
    state = np.zeros((2, 2, 3), dtype=float)
    state[..., 0] = 10.0

    def invalid_tendency(
        state, *, dx, dy, gravity, coriolis
    ):
        tendency = np.zeros_like(state)
        tendency[0, 0, 1] = np.nan
        return tendency

    with pytest.raises(ValueError, match="non-finite"):
        forward_euler_step(
            state,
            0.01,
            invalid_tendency,
            dx=1.0,
            dy=1.0,
            gravity=9.81,
            coriolis=0.0,
        )


def test_negative_updated_thickness_is_rejected():
    state = np.zeros((2, 2, 3), dtype=float)
    state[..., 0] = 1.0

    def decreasing_thickness(
        state, *, dx, dy, gravity, coriolis
    ):
        tendency = np.zeros_like(state)
        tendency[..., 0] = -20.0
        return tendency

    with pytest.raises(ValueError, match="nonpositive"):
        forward_euler_step(
            state,
            0.1,
            decreasing_thickness,
            dx=1.0,
            dy=1.0,
            gravity=9.81,
            coriolis=0.0,
        )