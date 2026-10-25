import numpy as np
import pytest

from src.model.finite_volume import (
    physical_flux_x,
    physical_flux_y,
    coriolis_source,
)


def test_x_flux_matches_analytical_equations():
    gravity = 2.0
    state = np.array([4.0, 8.0, 12.0])

    actual = physical_flux_x(state, gravity)

    expected = np.array([
        8.0,
        8.0**2 / 4.0 + 0.5 * gravity * 4.0**2,
        8.0 * 12.0 / 4.0,
    ])

    np.testing.assert_allclose(actual, expected)


def test_y_flux_matches_analytical_equations():
    gravity = 2.0
    state = np.array([4.0, 8.0, 12.0])

    actual = physical_flux_y(state, gravity)

    expected = np.array([
        12.0,
        8.0 * 12.0 / 4.0,
        12.0**2 / 4.0 + 0.5 * gravity * 4.0**2,
    ])

    np.testing.assert_allclose(actual, expected)


def test_x_flux_for_resting_uniform_layer():
    gravity = 9.81
    thickness = 10.0
    state = np.array([thickness, 0.0, 0.0])

    actual = physical_flux_x(state, gravity)

    expected = np.array([
        0.0,
        0.5 * gravity * thickness**2,
        0.0,
    ])

    np.testing.assert_allclose(actual, expected)


def test_y_flux_for_resting_uniform_layer():
    gravity = 9.81
    thickness = 10.0
    state = np.array([thickness, 0.0, 0.0])

    actual = physical_flux_y(state, gravity)

    expected = np.array([
        0.0,
        0.0,
        0.5 * gravity * thickness**2,
    ])

    np.testing.assert_allclose(actual, expected)


def test_coriolis_source_has_correct_signs():
    state = np.array([5.0, 10.0, 15.0])
    coriolis = 2.0

    actual = coriolis_source(state, coriolis)

    expected = np.array([
        0.0,
        2.0 * 15.0,
        -2.0 * 10.0,
    ])

    np.testing.assert_allclose(actual, expected)


def test_coriolis_source_is_zero_at_zero_rotation():
    state = np.array([5.0, 10.0, 15.0])

    actual = coriolis_source(state, 0.0)

    np.testing.assert_array_equal(actual, np.zeros(3))


def test_coriolis_source_supports_grid_arrays():
    state = np.array([
        [[10.0, 2.0, 3.0], [11.0, 4.0, 5.0]],
        [[12.0, 6.0, 7.0], [13.0, 8.0, 9.0]],
    ])
    coriolis = np.array([
        [0.1, 0.2],
        [0.3, 0.4],
    ])

    actual = coriolis_source(state, coriolis)

    assert actual.shape == state.shape
    np.testing.assert_allclose(actual[..., 0], 0.0)
    np.testing.assert_allclose(
        actual[..., 1], coriolis * state[..., 2]
    )
    np.testing.assert_allclose(
        actual[..., 2], -coriolis * state[..., 1]
    )


@pytest.mark.parametrize(
    "bad_state",
    [
        np.array([0.0, 1.0, 1.0]),
        np.array([-1.0, 1.0, 1.0]),
        np.array([np.nan, 1.0, 1.0]),
        np.array([1.0, np.inf, 1.0]),
        np.array([1.0, 1.0]),
        np.array([1.0, 1.0, 1.0, 1.0]),
    ],
)
def test_x_flux_rejects_invalid_states(bad_state):
    with pytest.raises(ValueError):
        physical_flux_x(bad_state, 9.81)


@pytest.mark.parametrize(
    "bad_state",
    [
        np.array([0.0, 1.0, 1.0]),
        np.array([-1.0, 1.0, 1.0]),
        np.array([np.nan, 1.0, 1.0]),
        np.array([1.0, np.inf, 1.0]),
        np.array([1.0, 1.0]),
        np.array([1.0, 1.0, 1.0, 1.0]),
    ],
)
def test_y_flux_rejects_invalid_states(bad_state):
    with pytest.raises(ValueError):
        physical_flux_y(bad_state, 9.81)


@pytest.mark.parametrize("gravity", [0.0, -1.0, np.nan, np.inf, True])
def test_fluxes_reject_invalid_gravity(gravity):
    state = np.array([10.0, 2.0, 3.0])

    with pytest.raises(ValueError):
        physical_flux_x(state, gravity)

    with pytest.raises(ValueError):
        physical_flux_y(state, gravity)


@pytest.mark.parametrize(
    "bad_coriolis",
    [
        np.nan,
        np.inf,
        np.array([0.1, np.nan]),
        np.ones((2, 3)),
    ],
)
def test_coriolis_source_rejects_invalid_rotation_values(bad_coriolis):
    state = np.array([
        [10.0, 2.0, 3.0],
        [11.0, 4.0, 5.0],
    ])

    with pytest.raises(ValueError):
        coriolis_source(state, bad_coriolis)


def test_fluxes_support_grid_arrays():
    state = np.array([
        [[10.0, 2.0, 3.0], [11.0, 4.0, 5.0]],
        [[12.0, 6.0, 7.0], [13.0, 8.0, 9.0]],
    ])

    flux_x = physical_flux_x(state, 9.81)
    flux_y = physical_flux_y(state, 9.81)

    assert flux_x.shape == state.shape
    assert flux_y.shape == state.shape
    assert np.all(np.isfinite(flux_x))
    assert np.all(np.isfinite(flux_y))


def test_fluxes_reject_non_numeric_states():
    state = np.array(["bad", "value", "here"])

    with pytest.raises(ValueError):
        physical_flux_x(state, 9.81)

    with pytest.raises(ValueError):
        physical_flux_y(state, 9.81)


def test_coriolis_source_rejects_non_numeric_state():
    state = np.array(["bad", "value", "here"])

    with pytest.raises(ValueError):
        coriolis_source(state, 0.1)