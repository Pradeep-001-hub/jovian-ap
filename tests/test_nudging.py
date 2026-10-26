import numpy as np
import pytest

from src.assimilation.nudging import apply_nudging


def test_nudging_moves_forecast_toward_observation():
    result = apply_nudging(
        forecast_values={"u": np.array([95.0])},
        observations={"u": np.array([100.0])},
        predicted_values={"u": np.array([95.0])},
        alpha=0.2,
    )

    np.testing.assert_allclose(result["u"], [96.0])


def test_negative_innovation_decreases_adjusted_value():
    result = apply_nudging(
        forecast_values={"u": np.array([100.0])},
        observations={"u": np.array([90.0])},
        predicted_values={"u": np.array([100.0])},
        alpha=0.5,
    )

    np.testing.assert_allclose(result["u"], [95.0])


def test_zero_innovation_leaves_forecast_unchanged():
    result = apply_nudging(
        forecast_values={"u": np.array([95.0])},
        observations={"u": np.array([95.0])},
        predicted_values={"u": np.array([95.0])},
        alpha=0.5,
    )

    np.testing.assert_allclose(result["u"], [95.0])


def test_alpha_zero_leaves_forecast_unchanged():
    result = apply_nudging(
        forecast_values={"u": np.array([95.0])},
        observations={"u": np.array([100.0])},
        predicted_values={"u": np.array([95.0])},
        alpha=0.0,
    )

    np.testing.assert_allclose(result["u"], [95.0])


def test_alpha_one_applies_full_innovation():
    result = apply_nudging(
        forecast_values={"u": np.array([95.0])},
        observations={"u": np.array([100.0])},
        predicted_values={"u": np.array([95.0])},
        alpha=1.0,
    )

    np.testing.assert_allclose(result["u"], [100.0])


def test_multiple_variables_are_supported():
    result = apply_nudging(
        forecast_values={
            "u": np.array([95.0, 110.0]),
            "v": np.array([5.0, 8.0]),
        },
        observations={
            "u": np.array([100.0, 100.0]),
            "v": np.array([7.0, 10.0]),
        },
        predicted_values={
            "u": np.array([95.0, 110.0]),
            "v": np.array([5.0, 8.0]),
        },
        alpha=0.5,
    )

    np.testing.assert_allclose(result["u"], [97.5, 105.0])
    np.testing.assert_allclose(result["v"], [6.0, 9.0])


def test_input_arrays_are_not_modified():
    forecast = np.array([95.0, 110.0])
    observations = np.array([100.0, 100.0])
    predictions = np.array([95.0, 110.0])

    originals = [
        forecast.copy(),
        observations.copy(),
        predictions.copy(),
    ]

    apply_nudging(
        {"u": forecast},
        {"u": observations},
        {"u": predictions},
        alpha=0.2,
    )

    np.testing.assert_array_equal(forecast, originals[0])
    np.testing.assert_array_equal(observations, originals[1])
    np.testing.assert_array_equal(predictions, originals[2])


@pytest.mark.parametrize("alpha", [-0.1, 1.1, np.nan, np.inf, -np.inf])
def test_invalid_alpha_is_rejected(alpha):
    with pytest.raises(ValueError):
        apply_nudging(
            {"u": np.array([1.0])},
            {"u": np.array([2.0])},
            {"u": np.array([1.0])},
            alpha=alpha,
        )


@pytest.mark.parametrize(
    "forecast, observations, predictions",
    [
        ({}, {}, {}),
        ({"u": np.array([1.0])}, {"v": np.array([1.0])},
         {"v": np.array([1.0])}),
        ({"u": np.array([1.0, 2.0])}, {"u": np.array([1.0])},
         {"u": np.array([1.0])}),
        ({"u": np.array([[1.0]])}, {"u": np.array([[2.0]])},
         {"u": np.array([[1.0]])}),
        ({"u": np.array([])}, {"u": np.array([])},
         {"u": np.array([])}),
        ({"u": np.array([np.nan])}, {"u": np.array([2.0])},
         {"u": np.array([1.0])}),
        ({"u": np.array([1.0])}, {"u": np.array([np.inf])},
         {"u": np.array([1.0])}),
        ({"u": np.array([1.0])}, {"u": np.array([2.0])},
         {"u": np.array([np.nan])}),
    ],
)
def test_invalid_inputs_are_rejected(forecast, observations, predictions):
    with pytest.raises(ValueError):
        apply_nudging(
            forecast,
            observations,
            predictions,
        )