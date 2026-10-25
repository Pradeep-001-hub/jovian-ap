import numpy as np
import pytest

from src.model.initial_conditions import (
    uniform_rest_state,
    gaussian_vortex_state,
)


def test_uniform_rest_state_shape():
    state = uniform_rest_state(
        nx=8,
        ny=6,
        mean_thickness=100.0,
    )

    assert state.shape == (6, 8, 3)


def test_uniform_rest_state_has_constant_thickness():
    state = uniform_rest_state(
        nx=8,
        ny=6,
        mean_thickness=100.0,
    )

    np.testing.assert_allclose(state[..., 0], 100.0)


def test_uniform_rest_state_has_zero_momentum():
    state = uniform_rest_state(
        nx=8,
        ny=6,
        mean_thickness=100.0,
    )

    np.testing.assert_array_equal(state[..., 1], 0.0)
    np.testing.assert_array_equal(state[..., 2], 0.0)


def test_uniform_rest_state_rejects_invalid_grid_sizes():
    for nx, ny in [(1, 5), (5, 1), (2.5, 5), (True, 5)]:
        with pytest.raises(ValueError):
            uniform_rest_state(
                nx=nx,
                ny=ny,
                mean_thickness=100.0,
            )


@pytest.mark.parametrize(
    "thickness",
    [0.0, -1.0, np.inf, np.nan, True, None],
)
def test_uniform_rest_state_rejects_invalid_thickness(thickness):
    with pytest.raises(ValueError):
        uniform_rest_state(
            nx=4,
            ny=4,
            mean_thickness=thickness,
        )


def test_gaussian_vortex_state_shape_and_finite_values():
    state = gaussian_vortex_state(
        nx=10,
        ny=8,
        mean_thickness=100.0,
        amplitude=2.0,
        width=3.0,
        dx=1.0,
        dy=1.0,
    )

    assert state.shape == (8, 10, 3)
    assert np.all(np.isfinite(state))


def test_gaussian_vortex_has_positive_uniform_thickness():
    state = gaussian_vortex_state(
        nx=10,
        ny=8,
        mean_thickness=100.0,
        amplitude=2.0,
        width=3.0,
    )

    assert np.all(state[..., 0] > 0.0)
    np.testing.assert_allclose(state[..., 0], 100.0)


def test_zero_amplitude_produces_zero_momentum():
    state = gaussian_vortex_state(
        nx=8,
        ny=8,
        mean_thickness=100.0,
        amplitude=0.0,
        width=2.0,
    )

    np.testing.assert_array_equal(state[..., 1], 0.0)
    np.testing.assert_array_equal(state[..., 2], 0.0)


def test_vortex_momentum_is_nonzero_for_nonzero_amplitude():
    state = gaussian_vortex_state(
        nx=9,
        ny=9,
        mean_thickness=100.0,
        amplitude=2.0,
        width=2.0,
    )

    assert np.any(np.abs(state[..., 1]) > 0.0)
    assert np.any(np.abs(state[..., 2]) > 0.0)


@pytest.mark.parametrize(
    "width, dx, dy",
    [
        (0.0, 1.0, 1.0),
        (-1.0, 1.0, 1.0),
        (2.0, 0.0, 1.0),
        (2.0, 1.0, -1.0),
        (np.inf, 1.0, 1.0),
    ],
)
def test_vortex_rejects_invalid_width_or_spacing(width, dx, dy):
    with pytest.raises(ValueError):
        gaussian_vortex_state(
            nx=6,
            ny=6,
            mean_thickness=100.0,
            amplitude=2.0,
            width=width,
            dx=dx,
            dy=dy,
        )


def test_vortex_rejects_invalid_grid_size():
    with pytest.raises(ValueError):
        gaussian_vortex_state(
            nx=1,
            ny=6,
            mean_thickness=100.0,
            amplitude=2.0,
            width=2.0,
        )


def test_vortex_rejects_invalid_mean_thickness():
    with pytest.raises(ValueError):
        gaussian_vortex_state(
            nx=6,
            ny=6,
            mean_thickness=0.0,
            amplitude=2.0,
            width=2.0,
        )