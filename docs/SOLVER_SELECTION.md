Numerical Solver Selection and Verification

1. Objective

This document establishes the process for selecting the numerical solver for JOVIAN-AP.

The initial model uses rotating shallow-water equations on a beta-plane to investigate idealised planetary jets, vortices, and data assimilation.

The solver must implement the selected mathematical formulation correctly. Solver availability, successful execution, and visual plausibility are not sufficient evidence of numerical correctness.

2. Candidate: shallowWaterFoam

OpenFOAM distributions have included a solver named "shallowWaterFoam", described as a transient solver for inviscid shallow-water equations with rotation.

This makes it a candidate for investigation.

Official documentation and source-code references:

- OpenFOAM Foundation v14 source-code guide:
  https://cpp.openfoam.org/v14/index.html

- OpenFOAM solver documentation:
  https://www.openfoam.com/documentation/user-guide/a-reference/a.1-standard-solvers

- OpenFOAM API documentation for shallowWaterFoam:
  https://www.openfoam.com/documentation/guides/v2206/api/dir_7d94bfc9a83a5dc0f40ac0aeda28eb12.html

The references above establish a starting point for the investigation. They do not establish that the solver in every OpenFOAM distribution or version implements all requirements of JOVIAN-AP.

3. Exact Version Verification

The intended environment is OpenFOAM Foundation version 14 on Ubuntu.

Before selecting a solver, the actual installation must be inspected.

The investigation will record:

- OpenFOAM distribution.
- Exact version.
- Solver executable name.
- Solver source-code location.
- Governing equations implemented.
- Required fields and physical parameters.
- Available boundary conditions.
- Numerical schemes and time-integration approach.

Documentation for OpenFOAM.com and OpenFOAM Foundation releases must not be treated as interchangeable without checking the relevant implementation.

4. Required Physical Formulation

The solver must represent the rotating shallow-water system documented in "MATHEMATICAL_MODEL.md".

The required physical features include:

- Conservation of layer thickness.
- Horizontal momentum evolution.
- Coupling between layer thickness and velocity.
- Coriolis acceleration.
- Spatial variation of the Coriolis parameter on a beta-plane.
- Appropriate initial and boundary conditions.
- Positive layer thickness.
- Numerically controlled time integration.

The implementation must be mathematically consistent with the selected equations.

5. The Beta-Plane Requirement

The intended local planetary model uses

f(y) = f0 + beta*y

where f0 is the Coriolis parameter at the reference latitude and beta represents its north-south gradient.

A solver that supports rotation does not necessarily support this spatially varying Coriolis parameter.

The source code and model configuration must therefore be examined to determine:

1. How rotational effects are represented.
2. Whether the Coriolis parameter is constant or spatially varying.
3. Whether a spatially varying parameter can be represented correctly.
4. Whether the implementation preserves the intended momentum equations.
5. Whether any required modification changes the numerical formulation.

If the required beta-plane behaviour cannot be represented correctly, the solver must be adapted or replaced.

6. Solver Selection Decision

Three implementation routes will be evaluated.

Route A: Use an Existing Solver

This route is acceptable if the installed solver implements the required equations and supports the intended beta-plane formulation.

The source code and verification tests must support that conclusion.

Route B: Extend an Existing Solver

This route may be appropriate if the solver provides a suitable shallow-water numerical framework but requires a carefully designed extension.

Any changes to the governing equations, rotational terms, or numerical treatment must be documented and tested.

The modified solver must be verified independently of the unmodified version.

Route C: Develop a Custom Solver

A custom solver will be considered if the available implementation cannot represent the required equations correctly.

The custom solver must implement the selected mathematical model explicitly and include suitable verification cases.

The choice will be based on mathematical suitability, numerical correctness, development effort, and reproducibility rather than convenience alone.

7. Verification Requirements

Before production experiments, the selected solver must undergo appropriate verification.

The planned checks include:

- Comparison of implemented terms with the documented equations.
- Dimensional consistency.
- Testing of the continuity equation.
- Testing of the Coriolis terms.
- Conservation of layer volume under suitable conditions.
- Comparison with analytical solutions where available.
- Time-step sensitivity.
- Spatial grid-refinement studies.
- Checks for unphysical layer thickness.
- Reproducibility of controlled test cases.

Additional tests will be selected according to the numerical formulation.

8. Connection to Data Assimilation

The solver will provide the forecast model for the data assimilation system.

A reference solution or controlled reference simulation will generate synthetic observations.

The free-run simulation will establish the baseline. Assimilated forecasts will then be evaluated against the same reference state.

The model interface must define how simulation fields are exported, how observation locations correspond to the computational mesh, and how updated states are transferred back into the model when required.

Any state-update method must preserve numerical consistency and avoid introducing unphysical states.

9. Current Decision Status

The candidate solver has been identified, but the final selection remains pending verification of the exact OpenFOAM Foundation v14 installation and its source code.

No claim is made that the installed solver already implements the complete JOVIAN-AP model.

The next implementation step is to inspect the actual solver source and a suitable example case, then record the findings before writing or modifying solver code.

10. Final Selection Criteria

The solver will be accepted for the project only when:

- Its governing equations are identified.
- Its rotational formulation is understood.
- Its compatibility with the beta-plane requirement is established.
- Its numerical settings and boundary conditions are documented.
- Appropriate verification tests pass.
- The simulation can be reproduced from documented files and commands.

The final choice and its rationale will be recorded after these requirements have been evaluated.