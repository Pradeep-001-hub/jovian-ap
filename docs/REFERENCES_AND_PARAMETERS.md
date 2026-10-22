Scientific References and Physical Parameters

1. Purpose

This document establishes the scientific references and parameter-selection principles for JOVIAN-AP.

The project will use a rotating shallow-water model to investigate data assimilation in idealised flows inspired by Jupiter's atmospheric jets and vortices.

Physical constants, idealised experimental parameters, and numerical settings must be distinguished explicitly. Values will not be selected merely because they produce visually appealing simulations.

2. Primary Scientific References

2.1 Rotating Shallow-Water Theory

Zeitlin, V. (2018).

Geophysical Fluid Dynamics: Understanding (almost) everything with rotating shallow water models.

Oxford University Press.

DOI: https://doi.org/10.1093/oso/9780198804338.001.0001

Purpose:

- Rotating shallow-water equations.
- Planetary rotation and tangent-plane approximations.
- Potential vorticity.
- Wave and vortex dynamics.
- Mathematical foundations for idealised planetary-flow experiments.

2.2 Jupiter's Physical Parameters

NASA National Space Science Data Center.

Jupiter Fact Sheet.

https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html

Purpose:

- Planetary radius.
- Rotation period.
- Gravity and other documented planetary properties.
- Reference values for Jupiter-inspired model parameters.

The specific value and definition used for each parameter must be recorded. Different radius definitions and rotation conventions must not be mixed without explanation.

2.3 Additional Jupiter Information

NASA Science.

Jupiter Facts.

https://science.nasa.gov/jupiter/jupiter-facts/

Purpose:

- Independent reference for Jupiter's rotation and general planetary characteristics.
- Background for interpreting the idealised model.

This source provides general planetary information; it does not, by itself, determine every parameter required by the numerical model.

2.4 OpenFOAM Solver Documentation

OpenFOAM Foundation documentation and the documentation for the specific OpenFOAM distribution used in the project.

https://openfoam.org/

https://www.openfoam.com/documentation/

Purpose:

- Identify available solvers.
- Examine the equations and assumptions implemented by candidate solvers.
- Verify the relationship between the selected mathematical model and its numerical implementation.

The exact OpenFOAM distribution, version, solver source code, and documentation must be recorded when the implementation is selected.

2.5 Data Assimilation

Evensen, G. (2009).

Data Assimilation: The Ensemble Kalman Filter, second edition.

Springer.

DOI: https://doi.org/10.1007/978-3-642-03711-5

Purpose:

- State estimation using observations and model forecasts.
- Ensemble Kalman Filter theory.
- Ensemble methods.
- Model error, localisation, and inflation.
- Principles for reproducible assimilation experiments.

Additional references will be added as individual assimilation methods are implemented.

3. Parameter Categories

JOVIAN-AP will maintain three distinct parameter categories.

Category A: Planetary Parameters

These are derived from documented planetary sources.

Examples include:

- Planetary rotation rate.
- Planetary radius.
- Reference latitude.
- Local Coriolis parameter.
- Beta-plane Coriolis gradient.

The source, definition, units, and conversion method must be recorded for each parameter.

Category B: Idealised Physical Parameters

These define the simplified mathematical experiment rather than a complete physical description of Jupiter.

Examples include:

- Reference fluid-layer depth.
- Effective gravity when an idealised model requires it.
- Initial jet amplitude and width.
- Initial vortex amplitude and radius.
- Domain dimensions.
- Idealised background flow.

These values must be justified by the experiment's objectives and checked for mathematical consistency.

An idealised parameter must not be presented as a measured property of Jupiter unless an appropriate physical interpretation and source support that claim.

Category C: Numerical and Assimilation Parameters

These control the computational experiment.

Examples include:

- Mesh resolution.
- Time step.
- Simulation duration.
- Numerical discretisation settings.
- Observation spacing.
- Observation noise.
- Nudging strength.
- Ensemble size.
- Localisation length.
- Inflation factor.

These parameters must be recorded in reproducible configuration files. Sensitivity studies will be used where appropriate to evaluate their influence on the results.

4. Planetary Rotation and Beta-Plane Parameters

For a local beta-plane centred at latitude phi0, the conventional first-order approximation is

f(y) = f0 + beta*y

where

f0 = 2Omegasin(phi0)

and

beta = 2Omegacos(phi0)/a

Here:

- Omega is the adopted planetary rotation rate in inverse seconds.
- phi0 is the reference latitude.
- a is the adopted planetary radius in metres.
- y is the northward distance from the reference latitude.
- f0 is the local Coriolis parameter in inverse seconds.
- beta is the meridional Coriolis gradient in inverse metres per second.

The latitude convention and rotation-rate definition must be documented.

The beta-plane approximation is local. Its suitability depends on the reference latitude and the size of the model domain.

A global spherical domain must not be represented as a single local beta-plane without a specific mathematical justification.

5. Parameter Selection Procedure

Before the first production simulation, the project will:

1. Select and document the reference latitude.
2. Identify the authoritative planetary rotation-rate source.
3. Select the planetary radius definition.
4. Calculate f0 and beta consistently.
5. Select the idealised layer depth and effective gravity.
6. Define the domain dimensions and initial flow scales.
7. Check dimensional consistency.
8. Evaluate whether the beta-plane approximation is suitable for the selected domain.
9. Record all parameter values and their sources.
10. Establish numerical stability and resolution requirements.

The selected values will be recorded only after these choices have been justified.

6. OpenFOAM Implementation Verification

OpenFOAM provides solvers for specific classes of physical problems. A solver's name alone is insufficient evidence that it implements the required JOVIAN-AP formulation.

The implementation investigation must establish:

- Whether an available shallow-water solver is suitable.
- Which governing equations it actually solves.
- How rotation is represented.
- Whether the required spatial variation of the Coriolis parameter is supported.
- Which numerical schemes and boundary conditions are available.
- Whether any custom solver development is necessary.
- How the implementation can be verified against the mathematical model.

The project's chosen OpenFOAM distribution and version must be verified before relying on distribution-specific solver capabilities.

7. Parameter Record

A machine-readable parameter record will be created when the model configuration is implemented.

Each entry should include:

Field| Description
Parameter| Symbol or configuration name
Value| Selected numerical value
Unit| SI unit where applicable
Category| Planetary, idealised physical, or numerical
Source| Reference or documented selection method
Rationale| Why the value was chosen
Uncertainty| Known uncertainty or sensitivity considerations

Parameters that have not yet been selected must remain explicitly marked as undecided rather than being assigned arbitrary values.

8. Scientific Integrity

All planetary parameters must be traceable to appropriate sources.

Idealised parameters must be identified as such.

Numerical settings must be documented separately from physical constants.

The use of Jupiter's rotation rate or radius does not, by itself, make a simulation a realistic model of Jupiter's atmosphere.

The final interpretation must reflect the shallow-water approximation, selected forcing and dissipation, numerical limitations, and observation assumptions.

9. Reference Maintenance

References will be reviewed as the project develops.

Additional scientific literature will be included for:

- Jupiter's zonal jets and vortices.
- Rotating shallow-water numerical methods.
- Verification and validation.
- Synthetic observation design.
- Nudging and optimal interpolation.
- Ensemble Kalman filtering.
- Error metrics and forecast evaluation.

A reference will support a scientific claim only when it is relevant to that claim.