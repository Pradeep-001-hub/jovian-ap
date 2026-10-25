import numpy as np
import pytest

from src.model.finite_volume import physical_flux_x, physical_flux_y
from src.model.numerical_flux import rusanov_flux_x, rusanov_flux_y


def test_x_flux_matches_physical_flux_for_equal_states():
    state = np.array([4.0, 8.0, 12.0])

    actual = rusanov_flux_x(state, state, gravity=2.0)
    expected = physical_flux_x(state, gravity=2.0)

    np.testing.assert_allclose(actual, expected)


def test_y_flux_matches_physical_flux_for_equal_states():
    state = np.array([4.0, 8.0, 12.0])

    actual = rusanov_flux_y(state, state, gravity=2.0)
    expected = physical_flux_y(state, gravity=2.0)

    np.testing.assert_allclose(actual, expected)


def test_x_flux_for_different_states_is_finite():
    left = np.array([4.0, 8.0, 12.0])
    right = np.array([5.0, 10.0, 15.0])

    actual = rusanov_flux_x(left, right, gravity=9.81)

    assert actual.shape == (3,)
    assert np.all(np.isfinite(actual))


def test_y_flux_for_different_states_is_finite():
    lower = np.array([4.0, 8.0, 12.0])
    upper = np.array([5.0, 10.0, 15.0])

    actual = rusanov_flux_y(lower, upper, gravity=9.81)

    assert actual.shape == (3,)
    assert np.all(np.isfinite(actual))


def test_x_flux_uses_zonal_velocity_for_wave_speed():
    left = np.array([4.0, 8.0, 0.0])
    right = np.array([4.0, 0.0, 0.0])
    gravity = 2.0

    actual = rusanov_flux_x(left, right, gravity)

    alpha = max(
        abs(left[1] / left[0]) + np.sqrt(gravity * left[0]),
        abs(right[1] / right[0]) + np.sqrt(gravity * right[0]),
    )

    expected = (
        0.5
        * (
            physical_flux_x(left, gravity)
            + physical_flux_x(right, gravity)
        )
        - 0.5 * alpha * (right - left)
    )

    np.testing.assert_allclose(actual, expected)


def test_y_flux_uses_meridional_velocity_for_wave_speed():
    lower = np.array([4.0, 0.0, 8.0])
    upper = np.array([4.0, 0.0, 0.0])
    gravity = 2.0

    actual = rusanov_flux_y(lower, upper, gravity)

    alpha = max(
        abs(lower[2] / lower[0]) + np.sqrt(gravity * lower[0]),
        abs(upper[2] / upper[0]) + np.sqrt(gravity * upper[0]),
    )

    expected = (
        0.5
        * (
            physical_flux_y(lower, gravity)
            + physical_flux_y(upper, gravity)
        )
        - 0.5 * alpha * (upper - lower)
    )

    np.testing.assert_allclose(actual, expected)


def test_x_flux_supports_arrays_of_states():
    left = np.array([
        [4.0, 8.0, 12.0],
        [5.0, 10.0, 15.0],
    ])
    right = np.array([
        [4.5, 9.0, 13.0],
        [5.5, 11.0, 16.0],
    ])

    actual = rusanov_flux_x(left, right, gravity=9.81)

    assert actual.shape == left.shape
    assert np.all(np.isfinite(actual))


def test_y_flux_supports_arrays_of_states():
    lower = np.array([
        [4.0, 8.0, 12.0],
        [5.0, 10.0, 15.0],
    ])
    upper = np.array([
        [4.5, 9.0, 13.0],
        [5.5, 11.0, 16.0],
    ])

    actual = rusanov_flux_y(lower, upper, gravity=9.81)

    assert actual.shape == lower.shape
    assert np.all(np.isfinite(actual))


@pytest.mark.parametrize(
    "bad_state",
    [
        np.array([0.0, 1.0, 1.0]),
        np.array([-1.0, 1.0, 1.0]),
        np.array([np.nan, 1.0, 1.0]),
        np.array([1.0, np.inf, 1.0]),
        np.array([1.0, 1.0]),
    ],
)
def test_x_flux_rejects_invalid_states(bad_state):
    valid_state = np.array([2.0, 1.0, 1.0])

    with pytest.raises(ValueError):
        rusanov_flux_x(bad_state, valid_state, gravity=9.81)


@pytest.mark.parametrize(
    "bad_state",
    [
        np.array([0.0, 1.0, 1.0]),
        np.array([-1.0, 1.0, 1.0]),
        np.array([np.nan, 1.0, 1.0]),
        np.array([1.0, np.inf, 1.0]),
        np.array([1.0, 1.0]),
    ],
)
def test_y_flux_rejects_invalid_states(bad_state):
    valid_state = np.array([2.0, 1.0, 1.0])

    with pytest.raises(ValueError):
        rusanov_flux_y(bad_state, valid_state, gravity=9.81)


@pytest.mark.parametrize("gravity", [0.0, -1.0, np.nan, np.inf, True])
def test_numerical_fluxes_reject_invalid_gravity(gravity):
    left = np.array([4.0, 2.0, 1.0])
    right = np.array([5.0, 3.0, 2.0])

    with pytest.raises(ValueError):
        rusanov_flux_x(left, right, gravity)

    with pytest.raises(ValueError):
        rusanov_flux_y(left, right, gravity)


def test_numerical_fluxes_reject_mismatched_shapes():
    left = np.array([[4.0, 2.0, 1.0]])
    right = np.array([4.0, 2.0, 1.0])

    with pytest.raises(ValueError):
        rusanov_flux_x(left, right, gravity=9.81)

    with pytest.raises(ValueError):
        rusanov_flux_y(left, right, gravity=9.81)