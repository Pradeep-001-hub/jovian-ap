import numpy as np

from src.assimilation.innovation import calculate_innovations
from src.assimilation.nudging import apply_nudging
from src.observations.observation_operator import observation_operator
from src.verification.analytical_flows import zonal_jet


def test_zonal_jet_observation_innovation_nudging_pipeline():
    # 1. Create a prescribed analytical jet.
    x = np.linspace(-2.0, 2.0, 21)
    y = np.linspace(-2.0, 2.0, 21)

    flow = zonal_jet(
        x,
        y,
        jet_speed=100.0,
        jet_width=1.0,
    )

    fields = {
        "u": flow["u"],
        "v": flow["v"],
        "h": flow["h"],
    }

    # 2. Predict model values at observation locations.
    locations = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
    ])

    predicted = observation_operator(
        x_coords=x,
        y_coords=y,
        fields=fields,
        observation_locations=locations,
    )

    predicted_values = predicted["values"]

    # 3. Construct a controlled synthetic observation dataset.
    # These values intentionally differ from model predictions.
    observations = {
        "u": predicted_values["u"] + np.array([5.0, -4.0, 2.0]),
        "v": predicted_values["v"] + np.array([1.0, -2.0, 3.0]),
        "h": predicted_values["h"] + np.array([0.5, -0.5, 1.0]),
    }

    # 4. Calculate innovations.
    innovations = calculate_innovations(
        observations=observations,
        predicted_values=predicted_values,
    )

    np.testing.assert_allclose(
        innovations["u"],
        [5.0, -4.0, 2.0],
    )

    np.testing.assert_allclose(
        innovations["v"],
        [1.0, -2.0, 3.0],
    )

    np.testing.assert_allclose(
        innovations["h"],
        [0.5, -0.5, 1.0],
    )

    # 5. Apply observation-space nudging.
    alpha = 0.2

    adjusted = apply_nudging(
        forecast_values=predicted_values,
        observations=observations,
        predicted_values=predicted_values,
        alpha=alpha,
    )

    # 6. Verify the mathematical update independently.
    for name in ("u", "v", "h"):
        expected = predicted_values[name] + alpha * innovations[name]

        np.testing.assert_allclose(
            adjusted[name],
            expected,
        )

    # 7. Verify that the adjustment moves toward the observations.
    for name in ("u", "v", "h"):
        initial_error = np.abs(
            observations[name] - predicted_values[name]
        )

        adjusted_error = np.abs(
            observations[name] - adjusted[name]
        )

        np.testing.assert_allclose(
            adjusted_error,
            (1.0 - alpha) * initial_error,
        )