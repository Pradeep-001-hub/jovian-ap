import numpy as np
import pytest

from src.model.shallow_water import (
    ShallowWaterParameters,
    validate_state,
)


@pytest.fixture
def parameters():
    return ShallowWaterParameters(
        rotation_rate=1.7585e-4,
        planetary_radius=6.9911e7,
        reference_latitude_deg=45.0,
        gravity=1.0,
    )


def test_reference_coriolis_parameter(parameters):
    expected = (
        2.0
        * parameters.rotation_rate
        * np.sin(np.deg2rad(45.0))
    )

    assert parameters.f0 == pytest.approx(expected)


def test_beta_plane_coefficient(parameters):
    expected = (
        2.0
        * parameters.rotation_rate
        * np.cos(np.deg2rad(45.0))
        / parameters.planetary_radius
    )

    assert parameters.beta == pytest.approx(expected)


def test_coriolis_parameter_at_reference_latitude(parameters):
    assert parameters.coriolis_parameter(0.0) == pytest.approx(
        parameters.f0
    )


def test_coriolis_parameter_varies_linearly_with_y(parameters):
    y = np.array([-1000.0, 0.0, 1000.0])

    actual = parameters.coriolis_parameter(y)
    expected = parameters.f0 + parameters.beta * y

    np.testing.assert_allclose(actual, expected)


def test_coriolis_parameter_rejects_non_finite_coordinates(parameters):
    with pytest.raises(ValueError):
        parameters.coriolis_parameter(np.array([0.0, np.nan]))


@pytest.mark.parametrize(
    "kwargs",
    [
        {"rotation_rate": 0.0},
        {"rotation_rate": -1.0},
        {"planetary_radius": 0.0},
        {"planetary_radius": -1.0},
        {"reference_latitude_deg": 91.0},
        {"reference_latitude_deg": -91.0},
        {"gravity": 0.0},
        {"gravity": -1.0},
        {"gravity": np.nan},
    ],
)
def test_invalid_physical_parameters_are_rejected(kwargs):
    values = {
        "rotation_rate": 1.7585e-4,
        "planetary_radius": 6.9911e7,
        "reference_latitude_deg": 45.0,
        "gravity": 1.0,
    }
    values.update(kwargs)

    with pytest.raises(ValueError):
        ShallowWaterParameters(**values)


def test_valid_state_is_returned_as_arrays():
    h = np.array([[1000.0, 1001.0]])
    u = np.array([[10.0, 11.0]])
    v = np.array([[1.0, 2.0]])

    actual_h, actual_u, actual_v = validate_state(h, u, v)

    np.testing.assert_array_equal(actual_h, h)
    np.testing.assert_array_equal(actual_u, u)
    np.testing.assert_array_equal(actual_v, v)


def test_state_fields_must_have_identical_shapes():
    h = np.ones((2, 2))
    u = np.ones((2, 2))
    v = np.ones((3, 2))

    with pytest.raises(ValueError):
        validate_state(h, u, v)


@pytest.mark.parametrize(
    "thickness",
    [
        np.array([[0.0, 1.0]]),
        np.array([[-1.0, 1.0]]),
        np.array([[np.nan, 1.0]]),
        np.array([[np.inf, 1.0]]),
    ],
)
def test_invalid_layer_thickness_is_rejected(thickness):
    u = np.ones_like(thickness)
    v = np.ones_like(thickness)

    with pytest.raises(ValueError):
        validate_state(thickness, u, v)


@pytest.mark.parametrize(
    "velocity",
    [
        np.array([[np.nan, 1.0]]),
        np.array([[np.inf, 1.0]]),
    ],
)
def test_non_finite_velocity_is_rejected(velocity):
    h = np.ones_like(velocity)
    v = np.ones_like(velocity)

    with pytest.raises(ValueError):
        validate_state(h, velocity, v)


def test_empty_state_is_rejected():
    empty = np.array([])

    with pytest.raises(ValueError):
        validate_state(empty, empty, empty)


def test_non_numeric_state_is_rejected():
    h = np.array([["bad"]])
    u = np.array([[1.0]])
    v = np.array([[1.0]])

    with pytest.raises(ValueError):
        validate_state(h, u, v)