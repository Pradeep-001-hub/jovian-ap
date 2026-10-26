import numpy as np

from src.verification.analytical_flows import (
    gaussian_vortex,
    zonal_jet,
)


def test_zonal_jet_matches_independent_reference_values():
    """
    Compare the generated zonal jet against independently evaluated
    values from u(y) = U0 * exp(-(y/L)^2).
    """
    x = np.array([-2.0, 0.0, 2.0])
    y = np.array([-1.0, 0.0, 1.0])

    speed = 100.0
    width = 1.0
    reference_thickness = 10000.0
    thickness_amplitude = 10.0

    flow = zonal_jet(
        x,
        y,
        jet_speed=speed,
        jet_width=width,
        reference_thickness=reference_thickness,
        thickness_amplitude=thickness_amplitude,
    )

    expected_profile = np.array([
        speed * np.exp(-1.0),
        speed,
        speed * np.exp(-1.0),
    ])

    expected_u = np.tile(expected_profile[:, None], (1, len(x)))
    expected_v = np.zeros((len(y), len(x)))

    expected_eta_profile = np.array([
        thickness_amplitude * np.exp(-1.0),
        thickness_amplitude,
        thickness_amplitude * np.exp(-1.0),
    ])

    expected_eta = np.tile(
        expected_eta_profile[:, None],
        (1, len(x)),
    )

    expected_h = reference_thickness + expected_eta

    np.testing.assert_allclose(flow["u"], expected_u)
    np.testing.assert_allclose(flow["v"], expected_v)
    np.testing.assert_allclose(flow["eta"], expected_eta)
    np.testing.assert_allclose(flow["h"], expected_h)


def test_gaussian_vortex_matches_independent_reference_values():
    """
    Compare selected vortex values against direct evaluation of
    the prescribed Gaussian vortex equations.
    """
    x = np.array([-1.0, 0.0, 1.0])
    y = np.array([-1.0, 0.0, 1.0])

    center_x = 0.0
    center_y = 0.0
    speed = 50.0
    radius = 1.0
    reference_thickness = 10000.0
    thickness_amplitude = 10.0

    flow = gaussian_vortex(
        x,
        y,
        center_x=center_x,
        center_y=center_y,
        circulation_speed=speed,
        radius=radius,
        reference_thickness=reference_thickness,
        thickness_amplitude=thickness_amplitude,
    )

    # Check the centre.
    assert flow["u"][1, 1] == 0.0
    assert flow["v"][1, 1] == 0.0
    assert flow["h"][1, 1] == reference_thickness + thickness_amplitude

    # Check the point directly east of the vortex centre.
    east_profile = np.exp(-0.5)

    np.testing.assert_allclose(
        flow["u"][1, 2],
        0.0,
        atol=1e-12,
    )

    np.testing.assert_allclose(
        flow["v"][1, 2],
        speed * east_profile,
    )

    # Check the point directly north of the vortex centre.
    np.testing.assert_allclose(
        flow["u"][2, 1],
        -speed * east_profile,
    )

    np.testing.assert_allclose(
        flow["v"][2, 1],
        0.0,
        atol=1e-12,
    )

    # Check thickness at one radius from the centre.
    expected_thickness = (
        reference_thickness
        + thickness_amplitude * east_profile
    )

    np.testing.assert_allclose(
        flow["h"][1, 2],
        expected_thickness,
    )


def test_reference_flow_fields_are_finite_and_physically_admissible():
    """
    Confirm that representative prescribed fields contain finite
    velocities and strictly positive layer thickness.
    """
    x = np.linspace(-3.0, 3.0, 31)
    y = np.linspace(-3.0, 3.0, 31)

    flows = [
        zonal_jet(x, y),
        gaussian_vortex(x, y),
    ]

    for flow in flows:
        for field in ("u", "v", "h", "eta"):
            assert np.all(np.isfinite(flow[field]))

        assert np.all(flow["h"] > 0.0)

        np.testing.assert_allclose(
            flow["h"],
            10000.0 + flow["eta"],
        )