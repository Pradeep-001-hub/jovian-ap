import numpy as np

from src.observations.generate_observations import generate_observations
from src.verification.analytical_flows import (
    gaussian_vortex,
    zonal_jet,
)


def test_zonal_jet_connects_to_observation_generator():
    x = np.linspace(-2.0, 2.0, 21)
    y = np.linspace(-2.0, 2.0, 21)

    flow = zonal_jet(
        x,
        y,
        jet_speed=100.0,
        jet_width=1.0,
    )

    locations = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [-1.0, 1.0],
    ])

    result = generate_observations(
        x_coords=x,
        y_coords=y,
        fields={
            "u": flow["u"],
            "v": flow["v"],
            "h": flow["h"],
        },
        observation_locations=locations,
        noise_std=0.0,
        seed=42,
    )

    assert set(result["values"]) == {"u", "v", "h"}
    assert result["values"]["u"].shape == (3,)
    assert result["values"]["v"].shape == (3,)
    assert result["values"]["h"].shape == (3,)

    # The jet depends on y, not x.
    # At y = 0, u = 100.
    # At y = 1, u = 100 * exp(-1).
    np.testing.assert_allclose(
        result["values"]["u"],
        [100.0, 100.0, 100.0 * np.exp(-1.0)],
    )

    np.testing.assert_allclose(
        result["values"]["v"],
        [0.0, 0.0, 0.0],
        atol=1e-12,
    )

    assert result["seed"] == 42
    assert result["sampling_method"] == "nearest_grid_point"


def test_gaussian_vortex_connects_to_observation_generator():
    x = np.linspace(-2.0, 2.0, 21)
    y = np.linspace(-2.0, 2.0, 21)

    flow = gaussian_vortex(
        x,
        y,
        center_x=0.0,
        center_y=0.0,
        circulation_speed=50.0,
        radius=1.0,
    )

    locations = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
    ])

    result = generate_observations(
        x_coords=x,
        y_coords=y,
        fields={
            "u": flow["u"],
            "v": flow["v"],
            "h": flow["h"],
        },
        observation_locations=locations,
        noise_std=0.0,
        seed=7,
    )

    assert set(result["values"]) == {"u", "v", "h"}
    assert result["values"]["u"].shape == (3,)
    assert result["values"]["v"].shape == (3,)
    assert result["values"]["h"].shape == (3,)

    # u = -V0 * (y - yc) / radius * exp(-r^2 / (2 radius^2))
    np.testing.assert_allclose(
        result["values"]["u"],
        [0.0, 0.0, -50.0 * np.exp(-0.5)],
        atol=1e-12,
    )

    # v = V0 * (x - xc) / radius * exp(-r^2 / (2 radius^2))
    np.testing.assert_allclose(
        result["values"]["v"],
        [0.0, 50.0 * np.exp(-0.5), 0.0],
        atol=1e-12,
    )


def test_observations_are_reproducible_for_same_seed():
    x = np.linspace(-2.0, 2.0, 21)
    y = np.linspace(-2.0, 2.0, 21)

    flow = zonal_jet(x, y)

    locations = np.array([
        [-1.0, 0.0],
        [0.0, 0.5],
        [1.0, -0.5],
    ])

    arguments = {
        "x_coords": x,
        "y_coords": y,
        "fields": {
            "u": flow["u"],
            "v": flow["v"],
            "h": flow["h"],
        },
        "observation_locations": locations,
        "noise_std": {
            "u": 1.0,
            "v": 1.0,
            "h": 0.1,
        },
        "seed": 123,
    }

    first = generate_observations(**arguments)
    second = generate_observations(**arguments)

    for field in ("u", "v", "h"):
        np.testing.assert_array_equal(
            first["values"][field],
            second["values"][field],
        )