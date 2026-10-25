JOVIAN-AP Numerical Model

1. Purpose

This directory contains the planned numerical implementation of an idealised rotating shallow-water model for studying atmospheric flows inspired by Jupiter's jets and vortices.

The model will provide the physical state used to generate synthetic observations, test data-assimilation methods, and evaluate short-term forecasts.

The implementation must be verified before its output is treated as a scientifically reliable reference solution.

2. Governing Equations

The initial model is the single-layer rotating shallow-water system on a local beta-plane.

Let:

- "h(x,y,t)" be the fluid-layer thickness.
- "u(x,y,t)" be the zonal velocity.
- "v(x,y,t)" be the meridional velocity.
- "g" be the reduced gravity used by the model.
- "f(y) = f0 + beta*y" be the Coriolis parameter.

The horizontal velocity vector is:

"U = (u, v)"

2.1 Conservation of Layer Thickness

For constant reference density and no mass sources:

"∂h/∂t + ∂(hu)/∂x + ∂(hv)/∂y = 0"

This equation expresses conservation of fluid-layer volume per unit horizontal area.

2.2 Zonal Momentum

"∂u/∂t + u*∂u/∂x + v*∂u/∂y - f*v = -g*∂h/∂x"

2.3 Meridional Momentum

"∂v/∂t + u*∂v/∂x + v*∂v/∂y + f*u = -g*∂h/∂y"

The momentum equations describe nonlinear advection, Coriolis acceleration, and the pressure-gradient acceleration of the shallow-water model.

These equations assume a flat local Cartesian domain, constant reduced gravity, and no explicit friction or external forcing in the initial formulation.

3. Planetary Rotation

For a local beta-plane approximation:

"f(y) = f0 + beta*y"

The coefficients are:

"f0 = 2*Omega*sin(phi0)"

"beta = 2*Omega*cos(phi0)/a"

where:

- "Omega" is the planetary rotation rate.
- "phi0" is the reference latitude.
- "a" is the planetary radius.

The coordinate "y" is measured relative to the reference latitude. The beta-plane approximation is local and should not be assumed accurate over an arbitrarily large domain.

4. State Representation

The model state is:

"X = [h, u, v]"

The computational representation must define:

- Spatial grid and grid spacing.
- Time integration method.
- Boundary conditions.
- Initial conditions.
- Numerical fluxes and spatial discretisation.
- Treatment of the Coriolis term.
- Treatment of the layer-thickness field.
- Output format and output frequency.

The initial implementation must use consistent units and explicitly document whether stored velocities are cell-centred or face-centred.

5. Required Numerical Properties

The implementation must be tested for:

1. Conservation of total layer volume under compatible closed or periodic boundary conditions.
2. Positivity of layer thickness.
3. Stability under the selected time-step restrictions.
4. Correct representation of rotating-flow behaviour.
5. Grid and time-step convergence.
6. Reproducibility of numerical experiments.

Potential vorticity and energy behaviour should also be assessed where appropriate to the selected discretisation.

Conservation and stability requirements must be matched to the actual numerical scheme and boundary conditions.

6. Reference Solution and Observations

The numerical model will eventually generate a reference state:

"X_truth(t)"

Synthetic observations will be sampled from this reference state:

"y = H(X_truth) + epsilon"

where "H" is the observation operator and "epsilon" is observation noise.

The reference simulation and evaluation data must be kept separate from the information supplied to the assimilation algorithm to prevent accidental data leakage.

7. Implementation Status

This directory currently specifies the intended model requirements.

The governing equations have not yet been implemented or numerically verified by this documentation alone.

A numerical solver must not be described as validated until appropriate verification tests have been completed and their results recorded.