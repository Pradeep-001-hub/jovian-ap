Mathematical Formulation of the Rotating Shallow-Water Model

1. Purpose

This document defines the proposed mathematical foundation for the initial JOVIAN-AP numerical model.

The objective is to investigate rotating atmospheric flows containing jets and vortices, and to determine whether data assimilation can improve the reconstruction and prediction of these flows when observations are sparse or noisy.

The initial formulation uses the rotating shallow-water equations on a beta-plane. This is an idealised model of large-scale atmospheric dynamics, not a complete representation of Jupiter's atmosphere.

The equations and numerical implementation must be verified before simulation results are used for scientific conclusions.

2. Physical Interpretation

The shallow-water approximation represents a fluid layer whose horizontal length scales are much greater than its vertical depth.

The model describes horizontal velocity and variations in the fluid-layer thickness or free-surface elevation. Vertical structure is not resolved explicitly.

The approximation can represent important rotating-flow behaviour, including the interaction of advection, pressure gradients, planetary rotation, and planetary-vorticity variation.

It does not resolve the full vertical structure, atmospheric stratification, radiative transfer, or detailed thermodynamics of Jupiter.

3. State Variables

Consider a two-dimensional horizontal domain with coordinates x and y.

The model variables are:

- x: horizontal coordinate in the east-west direction, measured in metres.
- y: horizontal coordinate in the north-south direction, measured in metres.
- t: time, measured in seconds.
- u(x,y,t): east-west velocity component, measured in metres per second.
- v(x,y,t): north-south velocity component, measured in metres per second.
- eta(x,y,t): free-surface displacement relative to a reference level, measured in metres.
- H: constant reference layer depth, measured in metres.
- g: effective gravitational acceleration, measured in metres per second squared.

For a flat bottom, the total layer thickness is

h = H + eta

The model requires h > 0 everywhere.

The horizontal velocity vector is

U = (u, v)

The reference depth H and the perturbation eta must be defined consistently throughout the implementation.

4. Beta-Plane Approximation

Planetary rotation influences horizontal motion through the Coriolis parameter.

In a local beta-plane approximation, the Coriolis parameter varies linearly with the north-south coordinate:

f(y) = f0 + beta*y

where:

- f0 is the Coriolis parameter at the centre of the domain, measured in inverse seconds.
- beta is the meridional gradient of the Coriolis parameter, measured in inverse metres per second.

For a planet rotating with angular velocity Omega, the local approximation is commonly written as

f0 = 2Omegasin(phi0)

beta = 2Omegacos(phi0)/a

where:

- Omega is the planetary rotation rate, measured in inverse seconds.
- phi0 is the reference latitude.
- a is the planetary radius, measured in metres.

These expressions apply to a local beta-plane expansion around the reference latitude.

For a Jupiter-inspired study, planetary parameters must be obtained from documented sources. The reference latitude and domain dimensions must be selected so that the local approximation is appropriate for the intended experiment.

A beta-plane model is not equivalent to a global spherical planetary model.

5. Governing Equations

For a flat bottom, constant gravitational acceleration, and no explicitly modelled friction or external forcing, the rotating shallow-water equations can be written as follows.

5.1 Conservation of Mass

The layer-thickness equation is

d(h)/dt + div(h*U) = 0

In component form,

d(h)/dt + d(hu)/dx + d(hv)/dy = 0

Since h = H + eta and H is constant, the equation can also be expressed as

d(eta)/dt + d(hu)/dx + d(hv)/dy = 0

This equation represents conservation of fluid-layer volume in the absence of sources and sinks.

5.2 Conservation of Momentum

The horizontal momentum equations in velocity form are

du/dt + udu/dx + vdu/dy - fv = -gd(eta)/dx

dv/dt + udv/dx + vdv/dy + fu = -gd(eta)/dy

where f = f(y).

The terms involving f represent the Coriolis acceleration. Their signs follow the convention in which x points eastward, y points northward, and the vertical direction is upward.

The pressure-gradient terms are represented by gradients of the free-surface displacement.

These equations assume a flat bottom and omit explicit friction, viscosity, and external forcing.

5.3 Vector Form

The momentum equations can be expressed compactly as

d(U)/dt + (U dot grad)U + fk_cross_U = -ggrad(eta)

where:

- U is the horizontal velocity vector.
- k is the upward unit vector.
- grad is the horizontal gradient operator.
- dot represents the vector dot product.
- cross represents the vector cross product.

The continuity and momentum equations form a coupled system: the velocity field transports layer thickness, while free-surface gradients influence the velocity field.

6. Potential Vorticity

For the inviscid rotating shallow-water system, a useful diagnostic is the shallow-water potential vorticity:

q = (zeta + f)/h

where zeta is the vertical component of relative vorticity:

zeta = dv/dx - du/dy

Potential vorticity combines relative vorticity, planetary rotation, and layer thickness.

For smooth solutions of the unforced, inviscid equations, potential vorticity is materially conserved:

D(q)/Dt = 0

where D/Dt is the material derivative following the horizontal flow.

This conservation law provides an important theoretical and numerical diagnostic. Numerical errors, boundary effects, or added physical processes may affect the observed behaviour, so the diagnostic must be interpreted in the context of the chosen discretisation and boundary conditions.

7. Initial Conditions

The model requires initial fields for u, v, and eta.

Possible test cases include:

1. A resting layer with a small surface perturbation.
2. A balanced rotating vortex.
3. A prescribed zonal jet.
4. A jet interacting with a vortex.
5. A perturbed flow used to investigate reconstruction and forecast errors.

Each initial condition must be defined mathematically and implemented reproducibly.

The first verification cases should be simpler than the final jet-vortex experiments. This allows numerical errors to be isolated before more complex flows are introduced.

Initial conditions must satisfy h > 0. Where a balanced initial state is required, the balance assumptions and construction method must be documented.

8. Boundary Conditions

Boundary conditions must be chosen to match the geometry and intended physical experiment.

Potential choices include:

- Periodic boundaries for idealised domains.
- Wall boundaries for confined test problems.
- Other open-boundary formulations when a suitable numerical treatment has been established.

Periodic boundaries can simplify controlled numerical experiments, but they also make the domain repeat periodically. They must not be interpreted as realistic global planetary boundaries.

The selected boundary conditions must be stated explicitly in each simulation configuration.

9. Model Assumptions

The initial model adopts the following assumptions:

- The flow is represented in two horizontal dimensions.
- The fluid layer is shallow relative to horizontal length scales.
- The reference depth is constant.
- The bottom is flat.
- The gravitational acceleration is constant.
- Planetary rotation is represented using a beta-plane approximation.
- Explicit friction and external forcing are initially omitted.
- Vertical atmospheric structure is not resolved.
- Synthetic observations are used before attempting more complex observational datasets.

Additional physical processes may be introduced in later experiments, but each addition must be accompanied by a clear mathematical definition and appropriate verification.

10. Dimensional Consistency

Every term in each governing equation must have consistent physical dimensions.

For example:

- Velocity u and v: metres per second.
- Layer thickness h: metres.
- Free-surface displacement eta: metres.
- Coriolis parameter f: inverse seconds.
- Beta parameter: inverse metres per second.
- Gravitational acceleration g: metres per second squared.
- Relative vorticity zeta: inverse seconds.
- Potential vorticity q: inverse metres per second.

Dimensional checks must be performed on the final implemented equations, including any additional forcing, diffusion, or numerical regularisation terms.

11. Numerical Implementation Requirements

The selected equations must be translated into a consistent numerical formulation.

Before implementing the full model, the project must establish:

1. The spatial discretisation.
2. The temporal integration scheme.
3. The treatment of Coriolis terms.
4. The coupling between velocity and layer thickness.
5. The numerical representation of gradients and fluxes.
6. The boundary-condition implementation.
7. The time-step stability criteria.
8. The treatment of positive layer thickness.
9. The relevant conservation and accuracy diagnostics.

OpenFOAM is a possible implementation framework, but its standard solvers must not be assumed to solve this particular system without verification.

A suitable existing solver must be demonstrated to implement the required equations correctly. Otherwise, an appropriately formulated custom solver will be required.

The final solver choice will be documented with reference to its actual mathematical formulation and implementation.

12. Verification Strategy

Verification will begin with controlled cases before progressing to jet-vortex simulations.

The planned checks include:

- Dimensional consistency of the governing equations.
- Tests of the continuity equation.
- Tests of the momentum and Coriolis terms.
- Comparison with analytical solutions where available.
- Conservation of total layer volume under suitable boundary conditions.
- Potential-vorticity behaviour in appropriate inviscid test cases.
- Spatial grid-refinement studies.
- Time-step sensitivity studies.
- Checks for unphysical negative layer thickness.
- Reproducibility of initial conditions and simulation outputs.

The exact verification cases will be selected after the numerical formulation and solver architecture have been established.

A simulation that executes without errors is not, by itself, evidence that the equations have been implemented correctly.

13. Connection to Data Assimilation

Once the numerical model has been verified, it will provide the forecast model for data assimilation experiments.

A reference simulation or controlled reference state will be used to generate synthetic observations.

The free-run simulation will establish a baseline. Assimilated simulations will then be compared with that baseline using consistent observation schedules, initial conditions, and evaluation times.

The purpose is to determine under which conditions data assimilation improves state reconstruction and subsequent forecasts.

Any improvement must be demonstrated quantitatively using reproducible experiments.

14. Scope and Future Extensions

The initial objective is a verified rotating shallow-water framework suitable for controlled data assimilation experiments.

Possible extensions include additional physical forcing, more realistic dissipation, improved observational operators, alternative assimilation methods, and more complex planetary-atmosphere models.

Three-dimensional atmospheric modelling is a separate and substantially more demanding extension. It will require additional governing equations, physical assumptions, numerical methods, and verification.

The project will not treat a two-dimensional shallow-water result as a complete prediction of Jupiter's atmosphere.

15. References and Parameter Sources

The final implementation must include appropriate scientific references for:

- Rotating shallow-water theory.
- The beta-plane approximation.
- Planetary parameters.
- Numerical discretisation and solver methods.
- Data assimilation algorithms.
- Verification and validation procedures.

Parameter values, reference states, and numerical settings must be traceable to documented sources or explicitly identified as idealised experimental choices.

References will be added and checked before the corresponding physical assumptions are used to support scientific conclusions.