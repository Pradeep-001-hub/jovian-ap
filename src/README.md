Source Code Architecture

1. Purpose

The "src/" directory will contain the implementation of the JOVIAN-AP computational framework.

The architecture separates physical modelling, numerical simulation, observation generation, data assimilation, and scientific evaluation. This separation is intended to make individual components easier to test, verify, and improve.

The structure described here is the intended architecture. Components will be identified as implemented only after their code has been developed and tested.

2. Planned Structure

src/
├── model/
│   ├── governing_equations
│   ├── physical_parameters
│   └── initial_conditions
├── observations/
│   ├── sampling
│   └── observation_noise
├── assimilation/
│   ├── nudging
│   ├── optimal_interpolation
│   └── ensemble_kalman_filter
├── evaluation/
│   ├── error_metrics
│   └── diagnostics
└── utilities/
    ├── configuration
    └── data_io

These names describe planned component responsibilities, not existing executable modules.

3. Physical Model

The "model/" component will define the rotating shallow-water formulation selected for the initial study.

It will document the governing equations, physical parameters, initial conditions, and assumptions.

The numerical implementation must be consistent with the mathematical formulation. OpenFOAM will be used where suitable, with a custom solver or an appropriately modified existing solver developed if required.

The final implementation strategy will be determined after examining the equations, numerical methods, and available solver capabilities.

4. Observation Generation

The "observations/" component will generate synthetic observations from a documented reference state or reference simulation.

It will support configurable observation locations, sampling intervals, and measurement noise.

The observation-generation process must be reproducible and must not introduce unintended information from the reference state into the assimilation algorithm.

5. Data Assimilation

The "assimilation/" component will contain the data assimilation methods selected for the study.

Development will begin with a clearly defined baseline and a simple assimilation method. Additional algorithms will be introduced after the initial implementation has passed suitable tests.

Each algorithm will document its assumptions, required inputs, numerical settings, and limitations.

6. Evaluation and Diagnostics

The "evaluation/" component will compare model estimates and forecasts against the selected reference state.

It will provide quantitative metrics, error diagnostics, and reproducible comparisons between assimilated and unassimilated simulations.

Metrics will be defined consistently so that comparisons remain meaningful across experiments.

7. Utilities

The "utilities/" component will provide shared functionality for configuration handling, data input and output, and other supporting operations.

Shared utilities should remain independent of specific assimilation algorithms wherever practical.

8. Testing and Verification

Every numerical component will require appropriate tests before being relied upon in scientific experiments.

Tests will cover relevant mathematical behaviour, input validation, reproducibility, and numerical correctness.

The project will distinguish software tests from physical-model verification and validation. Passing a software test alone does not establish that the model accurately represents atmospheric physics.

9. Implementation Principles

- Keep physical assumptions explicit.
- Prefer small, testable components.
- Separate simulation code from analysis code.
- Record configuration and experiment settings.
- Make numerical results reproducible.
- Avoid duplicating shared calculations.
- Document units and array conventions.
- Do not report unexecuted simulations as completed.
- Keep the Python and OpenFOAM interfaces explicit.

10. Development Order

The planned development sequence is:

1. Finalise the mathematical model and governing equations.
2. Select and verify a suitable numerical implementation.
3. Establish a reproducible free-run baseline.
4. Generate controlled synthetic observations.
5. Implement and test nudging.
6. Evaluate errors against the reference state.
7. Investigate additional assimilation algorithms.
8. Conduct controlled experiments and sensitivity studies.
9. Document results, limitations, and reproducibility procedures.

The architecture may be refined as technical requirements become clearer.