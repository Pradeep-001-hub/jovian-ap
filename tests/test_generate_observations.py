"""Scientific verification tests for the JOVIAN-AP observation generator."""

import numpy as np
import pytest

from src.observations.generate_observations import (
    generate_observations,
)


@pytest.fixture
def sample_data():
    """Create analytically known fields on a small regular grid."""
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 1.0, 2.0])
    X, Y = np.meshgrid(x, y)

    fields = {
        "u": 10.0 + 2.0 * X,
        "v": 5.0 + 3.0 * Y,
    }
    locations = np.array([
        [0.0, 0.0],
        [1.0, 1.0],
        [2.0, 2.0],
    ])

    return x, y, fields, locations


def test_zero_noise_returns_exact_sampled_values(sample_data):
    x, y, fields, locations = sample_data

    result = generate_observations(
        x, y, fields, locations, noise_std=0.0
    )

    np.testing.assert_allclose(result["values"]["u"], [10, 12, 14])
    np.testing.assert_allclose(result["values"]["v"], [5, 8, 11])


def test_seeded_noise_is_reproducible(sample_data):
    x, y, fields, locations = sample_data

    first = generate_observations(
        x, y, fields, locations, noise_std=0.5, seed=123
    )
    second = generate_observations(
        x, y, fields, locations, noise_std=0.5, seed=123
    )

    for name in fields:
        np.testing.assert_array_equal(
            first["values"][name], second["values"][name]
        )


def test_different_seeds_change_noisy_values(sample_data):
    x, y, fields, locations = sample_data

    first = generate_observations(
        x, y, fields, locations, noise_std=1.0, seed=1
    )
    second = generate_observations(
        x, y, fields, locations, noise_std=1.0, seed=2
    )

    assert not np.array_equal(
        first["values"]["u"], second["values"]["u"]
    )


def test_observation_coordinates_are_preserved(sample_data):
    x, y, fields, locations = sample_data

    result = generate_observations(
        x, y, fields, locations, noise_std=0.0
    )

    np.testing.assert_array_equal(result["x"], locations[:, 0])
    np.testing.assert_array_equal(result["y"], locations[:, 1])


def test_nearest_grid_point_sampling():
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 1.0, 2.0])
    X, Y = np.meshgrid(x, y)
    field = 10.0 + 2.0 * X + 3.0 * Y

    result = generate_observations(
        x, y, {"field": field},
        np.array([[0.9, 1.1]]), noise_std=0.0
    )

    np.testing.assert_allclose(result["values"]["field"], [15.0])
    assert result["grid_indices"]["ix"][0] == 1
    assert result["grid_indices"]["iy"][0] == 1


def test_exact_midpoint_tie_selects_lower_grid_index():
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 1.0])
    field = np.tile(x, (len(y), 1))

    result = generate_observations(
        x, y, {"field": field},
        np.array([[0.5, 0.5]]), noise_std=0.0
    )

    assert result["grid_indices"]["ix"][0] == 0
    assert result["grid_indices"]["iy"][0] == 0
    np.testing.assert_allclose(result["values"]["field"], [0.0])


@pytest.mark.parametrize(
    "locations",
    [
        np.array([[-0.1, 1.0]]),
        np.array([[2.1, 1.0]]),
        np.array([[1.0, -0.1]]),
        np.array([[1.0, 2.1]]),
    ],
)
def test_out_of_domain_locations_are_rejected(sample_data, locations):
    x, y, fields, _ = sample_data

    with pytest.raises(ValueError):
        generate_observations(
            x, y, fields, locations, noise_std=0.0
        )


def test_boundary_locations_are_allowed(sample_data):
    x, y, fields, _ = sample_data
    locations = np.array([
        [x[0], y[0]],
        [x[-1], y[-1]],
    ])

    result = generate_observations(
        x, y, fields, locations, noise_std=0.0
    )

    np.testing.assert_array_equal(
        result["grid_indices"]["ix"], [0, len(x) - 1]
    )
    np.testing.assert_array_equal(
        result["grid_indices"]["iy"], [0, len(y) - 1]
    )


def test_duplicate_observation_locations_are_allowed(sample_data):
    x, y, fields, _ = sample_data
    locations = np.array([[1.0, 1.0], [1.0, 1.0]])

    result = generate_observations(
        x, y, fields, locations, noise_std=0.0
    )

    np.testing.assert_allclose(result["values"]["u"], [12.0, 12.0])


def test_field_specific_noise_levels_are_recorded(sample_data):
    x, y, fields, locations = sample_data
    levels = {"u": 0.1, "v": 0.5}

    result = generate_observations(
        x, y, fields, locations,
        noise_std=levels, seed=42
    )

    assert result["noise_std"] == levels


@pytest.mark.parametrize(
    "noise_std",
    [
        -0.1,
        np.nan,
        np.inf,
        {"u": 0.1},
        {"u": 0.1, "v": -0.1},
        {"u": 0.1, "v": np.nan},
    ],
)
def test_invalid_noise_settings_are_rejected(sample_data, noise_std):
    x, y, fields, locations = sample_data

    with pytest.raises(ValueError):
        generate_observations(
            x, y, fields, locations, noise_std=noise_std
        )


def test_incorrect_field_shape_is_rejected(sample_data):
    x, y, _, locations = sample_data

    with pytest.raises(ValueError):
        generate_observations(
            x, y, {"u": np.zeros((2, 2))},
            locations, noise_std=0.0
        )


@pytest.mark.parametrize(
    "invalid_grid",
    [
        np.array([[0.0, 1.0], [2.0, 3.0]]),
        np.array([0.0, 0.0, 1.0]),
        np.array([0.0, np.nan, 2.0]),
        np.array([0.0, 2.0, 1.0]),
        np.array([0.0]),
    ],
)
def test_invalid_x_grids_are_rejected(sample_data, invalid_grid):
    _, y, fields, locations = sample_data

    with pytest.raises(ValueError):
        generate_observations(
            invalid_grid, y, fields, locations, noise_std=0.0
        )


@pytest.mark.parametrize(
    "locations",
    [
        np.array([[np.nan, 1.0]]),
        np.array([[1.0, np.inf]]),
        np.array([[1.0, 1.0, 1.0]]),
        np.array([]),
    ],
)
def test_invalid_observation_locations_are_rejected(
    sample_data, locations
):
    x, y, fields, _ = sample_data

    with pytest.raises(ValueError):
        generate_observations(
            x, y, fields, locations, noise_std=0.0
        )


def test_non_finite_field_values_are_rejected(sample_data):
    x, y, _, locations = sample_data
    field = np.zeros((len(y), len(x)))
    field[1, 1] = np.nan

    with pytest.raises(ValueError):
        generate_observations(
            x, y, {"field": field}, locations, noise_std=0.0
        )


def test_invalid_seeds_are_rejected(sample_data):
    x, y, fields, locations = sample_data

    for seed in (-1, 1.5, "42"):
        with pytest.raises(ValueError):
            generate_observations(
                x, y, fields, locations,
                noise_std=0.0, seed=seed
            )


def test_metadata_and_grid_indices_are_returned(sample_data):
    x, y, fields, locations = sample_data

    result = generate_observations(
        x, y, fields, locations,
        noise_std=0.0, seed=17
    )

    assert result["seed"] == 17
    assert result["sampling_method"] == "nearest_grid_point"
    assert result["noise_std"] == {"u": 0.0, "v": 0.0}

    np.testing.assert_array_equal(
        result["grid_indices"]["ix"], [0, 1, 2]
    )
    np.testing.assert_array_equal(
        result["grid_indices"]["iy"], [0, 1, 2]
    )