import numpy as np
import pytest

from src.verification.analytical_flows import (
    gaussian_vortex,
    zonal_jet,
)


def test_zonal_jet_field_shapes():
    x = np.linspace(-2.0, 2.0, 21)
    y = np.linspace(-3.0, 3.0, 31)

    flow = zonal_jet(x, y)

    expected_shape = (len(y), len(x))

    for field in ("u", "v", "h", "eta"):
        assert flow[field].shape == expected_shape


def test_zonal_jet_is_symmetric_about_jet_axis():
    x = np.linspace(-2.0, 2.0, 21)
    y = np.linspace(-2.0, 2.0, 21)

    flow = zonal_jet(
        x,
        y,
        jet_speed=100.0,
        jet_width=1.0,
    )

    center_row = len(y) // 2

    np.testing.assert_allclose(
        flow["u"][center_row, :],
        100.0,
    )

    np.testing.assert_allclose(
        flow["u"],
        flow["u"][::-1, :],
    )


def test_zonal_jet_northward_velocity_is_zero():
    x = np.linspace(-2.0, 2.0, 21)
    y = np.linspace(-2.0, 2.0, 21)

    flow = zonal_jet(x, y)

    np.testing.assert_allclose(
        flow["v"],
        0.0,
    )


def test_layer_thickness_matches_reference_plus_perturbation():
    x = np.linspace(-2.0, 2.0, 21)
    y = np.linspace(-2.0, 2.0, 21)

    reference_thickness = 10000.0

    flow = zonal_jet(
        x,
        y,
        reference_thickness=reference_thickness,
    )

    np.testing.assert_allclose(
        flow["h"],
        reference_thickness + flow["eta"],
    )

    assert np.all(flow["h"] > 0.0)


def test_gaussian_vortex_has_zero_velocity_at_center():
    x = np.linspace(-2.0, 2.0, 21)
    y = np.linspace(-2.0, 2.0, 21)

    flow = gaussian_vortex(
        x,
        y,
        center_x=0.0,
        center_y=0.0,
    )

    center_j = np.argmin(np.abs(y))
    center_i = np.argmin(np.abs(x))

    assert flow["u"][center_j, center_i] == pytest.approx(0.0)
    assert flow["v"][center_j, center_i] == pytest.approx(0.0)


def test_gaussian_vortex_has_expected_rotational_symmetry():
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

    center_j = len(y) // 2
    center_i = len(x) // 2

    # At equal distances to the east and north of the center:
    # eastward velocity is negative to the north,
    # northward velocity is positive to the east.
    assert flow["u"][center_j + 5, center_i] < 0.0
    assert flow["v"][center_j, center_i + 5] > 0.0

    # The corresponding opposite positions reverse the signs.
    assert flow["u"][center_j - 5, center_i] > 0.0
    assert flow["v"][center_j, center_i - 5] < 0.0


def test_gaussian_vortex_layer_thickness_is_positive():
    x = np.linspace(-2.0, 2.0, 21)
    y = np.linspace(-2.0, 2.0, 21)

    flow = gaussian_vortex(
        x,
        y,
        reference_thickness=10000.0,
        thickness_amplitude=10.0,
    )

    assert np.all(np.isfinite(flow["h"]))
    assert np.all(flow["h"] > 0.0)

    np.testing.assert_allclose(
        flow["h"],
        10000.0 + flow["eta"],
    )


@pytest.mark.parametrize(
    "bad_width",
    [0.0, -1.0],
)
def test_zonal_jet_rejects_nonpositive_width(bad_width):
    x = np.linspace(-1.0, 1.0, 5)
    y = np.linspace(-1.0, 1.0, 5)

    with pytest.raises(ValueError):
        zonal_jet(
            x,
            y,
            jet_width=bad_width,
        )


@pytest.mark.parametrize(
    "bad_radius",
    [0.0, -1.0],
)
def test_gaussian_vortex_rejects_nonpositive_radius(bad_radius):
    x = np.linspace(-1.0, 1.0, 5)
    y = np.linspace(-1.0, 1.0, 5)

    with pytest.raises(ValueError):
        gaussian_vortex(
            x,
            y,
            radius=bad_radius,
        )


def test_analytical_flows_reject_nonmonotonic_grid():
    x = np.array([-1.0, 0.0, -0.5, 1.0])
    y = np.linspace(-1.0, 1.0, 5)

    with pytest.raises(ValueError):
        zonal_jet(x, y)

    with pytest.raises(ValueError):
        gaussian_vortex(x, y)


def test_analytical_flows_reject_nonfinite_grid():
    x = np.array([-1.0, 0.0, np.nan, 1.0])
    y = np.linspace(-1.0, 1.0, 5)

    with pytest.raises(ValueError):
        zonal_jet(x, y)

    with pytest.raises(ValueError):
        gaussian_vortex(x, y)