Observation Model and Synthetic Data Generation

1. Purpose

This document defines the planned observation model for JOVIAN-AP.

The observation model specifies how simulated atmospheric states are converted into observations suitable for data assimilation. It also establishes how observation locations, sampling times, and measurement errors will be controlled during numerical experiments.

The initial study will use synthetic observations generated from a designated reference solution. This provides a known target against which reconstructed states and forecasts can be evaluated quantitatively.

Implementation status: Design documented; observation-generation code and its verification remain to be completed.

2. Experimental Concept

The initial experimental framework follows an Observing System Simulation Experiment (OSSE).

The procedure is:

1. Produce a designated reference solution for the idealised rotating-flow problem.
2. Select observation locations and sampling times.
3. Extract specified physical variables from the reference solution.
4. Add controlled synthetic observation errors.
5. Provide the resulting observations to the data assimilation methods.
6. Evaluate the reconstructed states against the reference solution.

The reference solution represents the known target for the experiment. It must be distinguished from the forecast produced by the model being evaluated.

Synthetic observations are not actual measurements of Jupiter's atmosphere. They are experimental data designed to test the proposed computational methods.

3. Observation Variables

The initial candidate observation variables are the horizontal velocity components:

- "u": velocity in the x-direction.
- "v": velocity in the y-direction.

The fluid-layer thickness, "h", may be included in later experiments if its observation model and physical interpretation are justified.

The initial experiments should begin with a clearly defined observation set and add complexity only when the baseline workflow has been verified.

All observation variables must use consistent units and coordinate conventions.

4. Mathematical Observation Model

Let the reference model state at time t be represented by:

"x_truth(t)".

The synthetic observation vector is defined as:

"y(t) = H[x_truth(t)] + epsilon(t)"

where:

- "y(t)" is the synthetic observation vector.
- "H" is the observation operator.
- "x_truth(t)" is the reference state.
- "epsilon(t)" is the prescribed observation-error vector.

The observation operator maps the complete model state to the quantities available at the observation locations.

For example, if observations contain only horizontal velocity, the operator extracts or interpolates the two velocity components at the selected locations.

If an observation falls between computational locations, an appropriate interpolation method must be used.

The observation operator used by the assimilation system must be consistent with the locations, variables, and units represented by the observation data.

5. Observation Errors

The initial experimental design may use zero-mean Gaussian observation errors:

"epsilon ~ N(0, R)"

where "R" is the observation-error covariance matrix.

For independent errors with a common standard deviation, the covariance matrix can be represented as:

"R = sigma_obs^2 I"

where:

- "sigma_obs" is the prescribed observation-error standard deviation.
- "I" is the identity matrix.

This independent-error model is a simplifying assumption, not a universal description of atmospheric measurement errors.

Observation noise must be controlled through documented parameters. A random seed should be recorded to make stochastic experiments reproducible.

Noise levels should be selected relative to the characteristic magnitudes of the reference variables and varied systematically during sensitivity experiments.

The initial configuration does not prescribe a final noise level. That choice will be made after the reference solution and characteristic flow scales have been established.

6. Observation Locations

Observations will be available at selected locations rather than throughout the entire computational domain.

Candidate sampling strategies include:

- Regular spatial sampling.
- Randomly selected observation locations.
- Sparse and dense observation networks.

The initial experiment should use a simple, reproducible sampling strategy. More complex sampling patterns can be introduced later.

Observation coordinates must be consistent with the computational domain and its coordinate system.

The observation generator must record the locations associated with every observation so that the assimilation system can map the data to the correct model state.

7. Observation Timing

Observations will be generated at prescribed times during the reference simulation.

The observation interval must be distinguished from the numerical time step used by the fluid solver. They need not be equal.

Experiments may investigate the effect of:

- Frequent observations.
- Less frequent observations.
- Different observation start times.
- A forecast period during which observations are no longer assimilated.

The final sampling interval must be selected in relation to the characteristic evolution times of the simulated flow and the numerical stability requirements.

8. Reference Solution and Experimental Independence

The reference solution is central to the validity of the experiments.

It must be generated using a documented, numerically verified configuration. Its resolution, time step, initial conditions, boundary conditions, and solver settings must be recorded.

Where practical, the reference solution should be more accurate than the solution being evaluated. For example, it may use a finer spatial resolution or a smaller time step after appropriate convergence testing.

The reference and evaluation configurations should be designed carefully to reduce the risk that the experiment merely reproduces identical numerical errors in both solutions.

Any differences between the reference and evaluation configurations must be documented.

A reference solution is not automatically the exact physical truth. It is the designated numerical target for the experiment, subject to its own numerical errors and modelling assumptions.

9. Data Integrity and Reproducibility

Each observation dataset should preserve:

- Observation times.
- Observation coordinates.
- Observed variable names.
- Variable units.
- Observation values.
- Noise settings.
- Random seed.
- Reference-solution identifier.
- Observation-generation configuration.

The generated dataset must be distinguishable from the original reference fields.

Observation-generation scripts should use recorded settings so that the same experiment can be reproduced.

Missing, invalid, or out-of-domain observations must be handled explicitly rather than silently accepted.

10. Planned Verification Tests

Before using observations in a scientific comparison, the observation-generation workflow should pass the following checks.

10.1 Zero-noise test

Set the observation noise to zero and verify that the generated observations agree with the reference values sampled through the observation operator, within the expected interpolation and numerical tolerances.

10.2 Noise statistics test

Generate enough samples to check whether the imposed noise has approximately the prescribed mean and variance. Small finite-sample deviations are expected.

10.3 Coordinate test

Verify that every observation location maps to the intended position in the computational domain.

10.4 Timing test

Verify that observations are extracted from the correct reference time levels or interpolated consistently when observation times fall between stored outputs.

10.5 Reproducibility test

Confirm that repeating the observation-generation procedure with the same inputs and random seed produces the same dataset.

10.6 Data completeness test

Check variable names, units, array dimensions, missing values, and the correspondence between observation records and their coordinates and times.

11. Relationship to Data Assimilation

The observation model supplies the data used by the planned assimilation methods:

- Nudging.
- Optimal interpolation.
- Ensemble Kalman filtering.

Each method will require an appropriate observation operator and a documented treatment of observation errors.

The methods must be evaluated using the same reference target and comparable observation datasets when conducting controlled comparisons.

Differences in performance should be attributed to the assimilation methods only when other experimental conditions have been held sufficiently consistent.

12. Scope and Limitations

The initial observation system is synthetic. It is intended to test the numerical and statistical behaviour of data assimilation in an idealised rotating-flow model.

It does not establish that the same performance would be achieved using real spacecraft observations or in a comprehensive model of Jupiter's atmosphere.

The validity of any conclusions depends on the quality of the reference solution, the physical assumptions of the shallow-water model, the numerical implementation, and the reproducibility of the experiments.

13. Completion Criteria

The observation-model component will be considered implemented when:

1. Synthetic observations can be generated reproducibly from a verified reference solution.
2. Observation locations, times, variables, and units are recorded correctly.
3. Observation noise can be controlled and tested.
4. The observation operator has passed appropriate verification tests.
5. The resulting datasets can be read by the assimilation workflow.
6. The procedure is documented sufficiently for another researcher to reproduce it.