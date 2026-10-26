import numpy as np
import pytest

from src.verification.metrics import (
    calculate_bias,
    calculate_mae,
    calculate_metrics,
    calculate_rmse,
)


def test_rmse_for_known_values():
    predictions = np.array([2.0, 4.0, 6.0])
    reference = np.array([1.0, 5.0, 6.0])

    expected = np.sqrt(2.0 / 3.0)

    assert calculate_rmse(predictions, reference) == pytest.approx(
        expected
    )


def test_mae_for_known_values():
    predictions = np.array([2.0, 4.0, 6.0])
    reference = np.array([1.0, 5.0, 6.0])

    assert calculate_mae(predictions, reference) == pytest.approx(2.0 / 3.0)


def test_bias_for_known_values():
    predictions = np.array([2.0, 4.0, 6.0])
    reference = np.array([1.0, 5.0, 6.0])

    assert calculate_bias(predictions, reference) == pytest.approx(0.0)


def test_combined_metrics():
    predictions = np.array([3.0, 5.0, 8.0])
    reference = np.array([1.0, 5.0, 6.0])

    result = calculate_metrics(predictions, reference)

    assert result["rmse"] == pytest.approx(np.sqrt(8.0 / 3.0))
    assert result["mae"] == pytest.approx(4.0 / 3.0)
    assert result["bias"] == pytest.approx(4.0 / 3.0)


def test_perfect_predictions_have_zero_error():
    reference = np.array([1.0, 2.0, 3.0])

    result = calculate_metrics(reference, reference)

    assert result["rmse"] == 0.0
    assert result["mae"] == 0.0
    assert result["bias"] == 0.0


@pytest.mark.parametrize(
    "predictions, reference",
    [
        ([], []),
        ([1.0, 2.0], [1.0]),
        ([np.nan], [1.0]),
        ([1.0], [np.inf]),
    ],
)
def test_invalid_inputs_are_rejected(predictions, reference):
    with pytest.raises(ValueError):
        calculate_metrics(predictions, reference)