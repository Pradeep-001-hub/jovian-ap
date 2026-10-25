JOVIAN-AP OpenFOAM Implementation

1. Purpose

JOVIAN-AP is a research-oriented computational framework for investigating idealised rotating atmospheric flows inspired by Jupiter's jets and vortices.

The primary computational engine will be a custom or appropriately verified OpenFOAM Foundation v14 solver.

OpenFOAM will perform the fluid simulation using its finite-volume infrastructure. Supporting software will handle observation generation, data assimilation, experiment management, and scientific evaluation.

The project is being developed incrementally. A planned feature must not be described as implemented until its source code, configuration, and verification results are available.

2. Software architecture

The intended architecture consists of five principal components.

2.1 OpenFOAM solver

The solver will implement the selected governing equations and advance the fluid state in time.

Its responsibilities include:

- Layer-thickness evolution.
- Horizontal momentum evolution.
- Planetary rotation and Coriolis acceleration.
- The selected dissipative and forcing terms.
- Numerical time integration.
- Physical and numerical diagnostics.

The solver will be written in C++ using the OpenFOAM finite-volume framework.

The final solver name and implementation strategy will be established after inspecting the target OpenFOAM Foundation v14 source and available numerical infrastructure.

2.2 OpenFOAM simulation cases

Each case will provide the configuration required to run a particular experiment.

Depending on the selected formulation, a case may contain:

- Initial and boundary conditions.
- Mesh definitions.
- Physical properties.
- Numerical schemes.
- Linear and nonlinear solver settings.
- Time-control settings.
- Experiment-specific parameters.

Separate cases will be maintained for verification, rotating-flow experiments, and idealised atmospheric-flow experiments.

2.3 Observation generation

Supporting observation utilities will generate reproducible synthetic observations from selected model fields.

The observation system will specify:

- Observation locations.
- Observed variables.
- Sampling methods.
- Observation errors.
- Random seeds.
- Observation metadata.

Observation generation will remain separate from the OpenFOAM fluid solver.

2.4 Data assimilation

The data-assimilation component will use observations and model forecasts to construct updated estimates of the simulated state.

Candidate methods include:

- Nudging.
- Optimal interpolation.
- Ensemble Kalman filtering.

Each method will be evaluated against a forecast without assimilation using identical reference conditions wherever appropriate.

The interface between OpenFOAM and the assimilation tools must be documented and tested before the complete workflow is considered operational.

2.5 Verification and evaluation

Verification will assess whether the implementation correctly solves the selected mathematical model.

The initial programme will examine:

- Conservation of total layer mass.
- Positive layer thickness.
- Gravity-wave propagation.
- Rotating-flow behaviour.
- Time-step sensitivity.
- Mesh convergence.
- Sensitivity to numerical dissipation.
- Reproducibility.

Evaluation will measure reconstruction and forecast errors, including root-mean-square error and mean absolute error.

Improved forecast performance must be demonstrated by reproducible experiments rather than assumed from the use of data assimilation.

3. Initial mathematical model

The initial target is a single-layer rotating shallow-water model.

Its layer-thickness equation is

[
\frac{\partial h}{\partial t}
+\nabla_h\cdot(h\mathbf{u})=0.
]

Its horizontal momentum equation is

[
\frac{\partial \mathbf{u}}{\partial t}
+(\mathbf{u}\cdot\nabla_h)\mathbf{u}
+f(y)\mathbf{k}\times\mathbf{u}
=-g'\nabla_h h
+\mathcal{D}(\mathbf{u})
+\mathbf{F}.
]

Here:

- h is the fluid-layer thickness.
- \mathbf{u} is the horizontal velocity.
- f(y) is the Coriolis parameter.
- \mathbf{k} is the vertical unit vector.
- g' is the effective restoring acceleration.
- \mathcal{D} represents explicitly selected dissipative terms.
- \mathbf{F} represents explicitly defined forcing.

For a local beta-plane approximation,

[
f(y)=f_0+\beta y.
]

The model is an idealised two-dimensional horizontal-flow model. It does not resolve Jupiter's complete three-dimensional atmosphere.

The equations, coordinate conventions, assumptions, and parameter definitions must be reviewed before solver implementation.

4. Implementation strategy

Development will proceed through the following stages.

Stage 1: Inspect the target framework

- Confirm the OpenFOAM Foundation v14 environment.
- Inspect available solvers and relevant finite-volume classes.
- Review time integration, field handling, and source-term implementation.
- Determine whether an existing implementation can be adapted safely.

Stage 2: Implement the fluid solver

- Define the required fields.
- Implement layer-thickness conservation.
- Implement horizontal momentum evolution.
- Add Coriolis acceleration.
- Introduce selected physical dissipation and forcing.
- Establish suitable numerical and boundary-condition treatments.

Stage 3: Verify the solver

- Compile the solver against the target OpenFOAM version.
- Run a minimal verification case.
- Check conservation and physical admissibility.
- Compare selected results against analytical or independently verified references.
- Record numerical settings and verification results.

Stage 4: Develop atmospheric-flow experiments

- Construct idealised vortex cases.
- Develop suitable zonal-jet initial conditions.
- Investigate rotational effects and flow evolution.
- Study mesh and time-step sensitivity.

Stage 5: Integrate observations and assimilation

- Generate observations from reference simulations.
- Establish a forecast without assimilation.
- Implement the observation-to-model data interface.
- Add and verify assimilation methods.
- Compare reconstruction and forecast errors.

Stage 6: Scientific evaluation

- Automate reproducible experiments.
- Record parameters, software versions, and random seeds.
- Visualise relevant flow fields.
- Document limitations and distinguish verified results from exploratory results.

5. Role of Python

Python is a supporting technology, not the primary CFD engine.

It may be used for:

- Synthetic observation generation.
- Data-assimilation algorithms.
- Experiment orchestration.
- Numerical verification.
- Error analysis.
- Plotting and post-processing.
- Automated tests.

The physical simulation itself must be performed by the OpenFOAM solver.

Existing Python numerical components may be retained temporarily as reference implementations. They must not be confused with the OpenFOAM solver or treated as authoritative until independently verified.

6. Development and verification policy

The project will distinguish between planned, implemented, and verified functionality.

A solver is not considered operational merely because its source code exists.

Before a capability is described as implemented, the project must have the necessary source code and configuration.

Before a numerical result is described as verified, the relevant test must have been executed and its outcome recorded.

Scientific claims about improved forecasts, physical accuracy, or agreement with Jovian observations require appropriate evidence.

7. Current implementation status

This document defines the intended architecture and development strategy.

The complete OpenFOAM solver, its verification suite, and the integrated data-assimilation workflow are not established by this document alone.

Their status will be updated as implementation and verification progress.

8. Target environment

- CFD framework: OpenFOAM Foundation v14.
- Solver language: C++.
- Primary operating environment: Ubuntu/WSL.
- Supporting scientific tools: Python, NumPy, SciPy, and Matplotlib.
- Visualisation: ParaView.
- Source control and collaboration: GitHub.

The exact compiler, OpenFOAM build configuration, and runtime dependencies will be documented after the target environment is inspected.