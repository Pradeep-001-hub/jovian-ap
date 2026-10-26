import numpy as np
import pytest

from src.verification.forecast_comparison import compare_forecasts

def test_assimilated_forecast_improves_accuracy():
reference = np.array([1.0, 2.0, 3.0])
free_forecast = np.array([2.0, 4.0, 4.0])
assimilated_forecast = np.array([1.5, 2.5, 3.0])

result = compare_forecasts(
    free_forecast,
    assimilated_forecast,
    reference,
)

assert (
    result["assimilated_forecast"]["rmse"]
    < result["free_forecast"]["rmse"]
)
assert result["improvement_percent"]["rmse"] > 0.0

def test_worse_assimilated_forecast_shows_negative_improvement():
reference = np.array([1.0, 2.0, 3.0])
free_forecast = np.array([1.1, 2.1, 3.1])
assimilated_forecast = np.array([3.0, 4.0, 5.0])

result = compare_forecasts(
    free_forecast,
    assimilated_forecast,
    reference,
)

assert result["improvement_percent"]["rmse"] < 0.0
assert result["improvement_percent"]["mae"] < 0.0

def test_identical_forecasts_have_zero_improvement():
reference = np.array([1.0, 2.0, 3.0])
forecast = np.array([2.0, 3.0, 4.0])

result = compare_forecasts(forecast, forecast, reference)

assert result["improvement_percent"]["rmse"] == pytest.approx(0.0)
assert result["improvement_percent"]["mae"] == pytest.approx(0.0)

def test_perfect_free_forecast_has_undefined_percentage_improvement():
reference = np.array([1.0, 2.0, 3.0])
free_forecast = reference.copy()
assimilated_forecast = np.array([1.1, 2.1, 3.1])

result = compare_forecasts(
    free_forecast,
    assimilated_forecast,
    reference,
)

assert result["improvement_percent"]["rmse"] is None
assert result["improvement_percent"]["mae"] is None

def test_mismatched_shapes_are_rejected():
with pytest.raises(ValueError):
compare_forecasts(
np.array([1.0, 2.0]),
np.array([1.0, 2.0, 3.0]),
np.array([1.0, 2.0]),
)

def test_nonfinite_values_are_rejected():
with pytest.raises(ValueError):
compare_forecasts(
np.array([1.0, np.nan]),
np.array([1.0, 2.0]),
np.array([1.0, 2.0]),
)