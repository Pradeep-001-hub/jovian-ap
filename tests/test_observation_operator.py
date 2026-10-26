import numpy as np
import pytest

from src.observations.observation_operator import observation_operator


@pytest.fixture
def sample_grid():
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 1.0, 2.0])

    X, Y = np.meshgrid(x, y)

    fields = {
        "u": 10.0 * X + Y,
        "v": X - 2.0 * Y,
        "h": 1000.0 + X + Y,
    }

    return x, y, fields


def test_exact_grid_point_sampling(sample_grid):
    x, y, fields = sample_grid

    locations = np.array([
        [0.0, 0.0],
        [1.0, 1.0],
        [2.0, 2.0],
    ])

    result = observation_operator(x, y, fields, locations)

    np.testing.assert_allclose(
        result["values"]["u"],
        [0.0, 11.0, 22.0],
    )

    np.testing.assert_allclose(
        result["values"]["v"],
        [0.0, -1.0, -2.0],
    )

    np.testing.assert_allclose(
        result["values"]["h"],
        [1000.0, 1002.0, 1004.0],
    )


def test_off_grid_sampling_uses_nearest_grid_point(sample_grid):
    x, y, fields = sample_grid

    locations = np.array([
        [0.8, 0.9],
        [1.8, 1.2],
    ])

    result = observation_operator(x, y, fields, locations)

    # (0.8, 0.9) is nearest to (1, 1).
    # (1.8, 1.2) is nearest to (2, 1).
    np.testing.assert_allclose(
        result["values"]["u"],
        [11.0, 21.0],
    )

    np.testing.assert_array_equal(
        result["grid_indices"],
        [[1, 1], [2, 1]],
    )


def test_midpoint_ties_select_lower_grid_coordinate(sample_grid):
    x, y, fields = sample_grid

    locations = np.array([
        [0.5, 0.5],
        [1.5, 1.5],
    ])

    result = observation_operator(x, y, fields, locations)

    np.testing.assert_array_equal(
        result["grid_indices"],
        [[0, 0], [1, 1]],
    )


def test_multiple_fields_are_returned(sample_grid):
    x, y, fields = sample_grid

    locations = np.array([
        [1.0, 0.0],
        [0.0, 2.0],
    ])

    result = observation_operator(x, y, fields, locations)

    assert set(result["values"]) == {"u", "v", "h"}

    for name in ("u", "v", "h"):
        assert result["values"][name].shape == (2,)

    assert result["sampling_method"] == "nearest_grid_point"


def test_observation_coordinates_are_preserved(sample_grid):
    x, y, fields = sample_grid

    locations = np.array([
        [0.8, 0.9],
        [1.8, 1.2],
    ])

    result = observation_operator(x, y, fields, locations)

    np.testing.assert_array_equal(result["x"], locations[:, 0])
    np.testing.assert_array_equal(result["y"], locations[:, 1])


@pytest.mark.parametrize(
    "locations",
    [
        np.array([0.5, 0.5]),
        np.array([[0.5, 0.5, 1.0]]),
        np.array([[np.nan, 0.5]]),
        np.array([[0.5, np.inf]]),
        np.array([[-0.1, 0.5]]),
        np.array([[0.5, 2.1]]),
        np.empty((0, 2)),
    ],
)
def test_invalid_observation_locations_are_rejected(
    sample_grid,
    locations,
):
    x, y, fields = sample_grid

    with pytest.raises(ValueError):
        observation_operator(x, y, fields, locations)


def test_non_monotonic_grid_is_rejected(sample_grid):
    x, y, fields = sample_grid

    invalid_x = np.array([0.0, 2.0, 1.0])

    with pytest.raises(ValueError):
        observation_operator(invalid_x, y, fields, np.array([[1.0, 1.0]]))


def test_incorrect_field_shape_is_rejected(sample_grid):
    x, y, fields = sample_grid

    invalid_fields = {
        "u": np.zeros((2, 2)),
    }

    with pytest.raises(ValueError):
        observation_operator(
            x,
            y,
            invalid_fields,
            np.array([[1.0, 1.0]]),
        )


def test_non_finite_field_values_are_rejected(sample_grid):
    x, y, fields = sample_grid

    invalid_fields = {
        "u": np.array([
            [0.0, 1.0, 2.0],
            [1.0, np.nan, 3.0],
            [2.0, 3.0, 4.0],
        ]),
    }

    with pytest.raises(ValueError):
        observation_operator(
            x,
            y,
            invalid_fields,
            np.array([[0.0, 0.0]]),
        )


def test_operator_does_not_modify_input_fields(sample_grid):
    x, y, fields = sample_grid

    original_fields = {
        name: field.copy()
        for name, field in fields.items()
    }

    observation_operator(
        x,
        y,
        fields,
        np.array([[1.0, 1.0]]),
    )

    for name in fields:
        np.testing.assert_array_equal(
            fields[name],
            original_fields[name],
        )