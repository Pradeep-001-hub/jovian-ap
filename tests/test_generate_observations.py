"""Tests for the JOVIAN-AP observation generator."""

import numpy as np
import pytest

from src.observations.generate_observations import (
    generate_observations,
)


@pytest.fixture
def sample_data():
    """Create a small grid with analytically known fields."""

    x = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 1.0, 2.0])

    X, Y = np.meshgrid(x, y)

    # Known fields make expected results easy to calculate.
    u = 10.0 + 2.0 * X
    v = 5.0 + 3.0 * Y

    locations = np.array([
        [0.0, 0.0],
        [1.0, 1.0],
        [2.0, 2.0],
    ])

    return x, y, {"u": u, "v": v}, locations


def test_zero_noise_returns_exact_sampled_values(sample_data):
    """Zero noise should preserve the sampled field values."""

    x, y, fields, locations = sample_data

    result = generate_observations(
        x,
        y,
        fields,
        locations,
        noise_std=0.0,
    )

    np.testing.assert_allclose(
        result["values"]["u"],
        [10.0, 12.0, 14.0],
    )

    np.testing.assert_allclose(
        result["values"]["v"],
        [5.0, 8.0, 11.0],
    )


def test_observations_are_reproducible(sample_data):
    """Identical inputs and seeds should reproduce the same output."""

    x, y, fields, locations = sample_data

    result_1 = generate_observations(
        x, y, fields, locations,
        noise_std=0.5,
        seed=123,
    )

    result_2 = generate_observations(
        x, y, fields, locations,
        noise_std=0.5,
        seed=123,
    )

    for name in fields:
        np.testing.assert_array_equal(
            result_1["values"][name],
            result_2["values"][name],
        )


def test_different_seeds_change_noisy_observations(sample_data):
    """Different seeds should generally produce different noise."""

    x, y, fields, locations = sample_data

    result_1 = generate_observations(
        x, y, fields, locations,
        noise_std=1.0,
        seed=1,
    )

    result_2 = generate_observations(
        x, y, fields, locations,
        noise_std=1.0,
        seed=2,
    )

    assert not np.array_equal(
        result_1["values"]["u"],
        result_2["values"]["u"],
    )


def test_observation_coordinates_are_preserved(sample_data):
    """The returned coordinates should match the requested locations."""

    x, y, fields, locations = sample_data

    result = generate_observations(
        x, y, fields, locations,
        noise_std=0.0,
    )

    np.testing.assert_array_equal(result["x"], locations[:, 0])
    np.testing.assert_array_equal(result["y"], locations[:, 1])


def test_nearest_grid_point_sampling():
    """An off-grid location should use the nearest grid point."""

    x = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 1.0, 2.0])

    X, Y = np.meshgrid(x, y)
    field = 10.0 + 2.0 * X + 3.0 * Y

    locations = np.array([[0.9, 1.1]])

    result = generate_observations(
        x,
        y,
        {"field": field},
        locations,
        noise_std=0.0,
    )

    # Nearest grid point is (1, 1).
    np.testing.assert_allclose(
        result["values"]["field"],
        [15.0],
    )


def test_out_of_domain_observation_is_rejected(sample_data):
    """Observations outside the grid must not be silently accepted."""

    x, y, fields, _ = sample_data
    locations = np.array([[3.0, 1.0]])

    with pytest.raises(ValueError):
        generate_observations(
            x, y, fields, locations,
            noise_std=0.0,
        )


def test_negative_noise_is_rejected(sample_data):
    """Noise standard deviation cannot be negative."""

    x, y, fields, locations = sample_data

    with pytest.raises(ValueError):
        generate_observations(
            x, y, fields, locations,
            noise_std=-0.1,
        )


def test_incorrect_field_shape_is_rejected(sample_data):
    """Fields must match the grid dimensions."""

    x, y, fields, locations = sample_data

    invalid_fields = {
        "u": np.zeros((2, 2)),
    }

    with pytest.raises(ValueError):
        generate_observations(
            x, y, invalid_fields, locations,
            noise_std=0.0,
        )


def test_duplicate_observation_locations_are_allowed(sample_data):
    """Repeated locations should be handled consistently."""

    x, y, fields, _ = sample_data

    locations = np.array([
        [1.0, 1.0],
        [1.0, 1.0],
    ])

    result = generate_observations(
        x, y, fields, locations,
        noise_std=0.0,
    )

    np.testing.assert_allclose(
        result["values"]["u"],
        [12.0, 12.0],
    )