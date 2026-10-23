Data Assimilation Methods

1. Purpose

This document defines the mathematical foundation and proposed implementation strategy for the data assimilation methods investigated in JOVIAN-AP.

The project will examine whether incorporating sparse, noisy synthetic observations into an idealised rotating-flow model improves state reconstruction and short-term forecasting compared with an otherwise comparable simulation without assimilation.

The initial methods under consideration are:

1. Free-run baseline.
2. Nudging.
3. Optimal Interpolation (OI).
4. Ensemble Kalman Filter (EnKF).

The free run is the control experiment rather than a data assimilation method.

Implementation status: Mathematical design documented. Numerical implementations, integration with the fluid solver, and comparative experiments remain to be completed and verified.

2. Model State and Observations

Represent the discrete model state as:

"x = [u, v, h]^T"

where the notation represents the collection of discretised fields:

- "u": horizontal velocity in the x-direction.
- "v": horizontal velocity in the y-direction.
- "h": fluid-layer thickness.

The actual state vector will depend on the numerical representation adopted by the solver.

Let:

- "x_b" be the background state or model forecast before assimilation.
- "y" be the observation vector.
- "H" be the observation operator.
- "R" be the observation-error covariance matrix.
- "x_a" be the analysis state after assimilation.

The observation model is:

"y = H(x_truth) + epsilon"

where "x_truth" denotes the designated reference state and "epsilon" represents synthetic observation errors.

For a linear observation operator, the observation innovation is:

"d = y - H x_b"

The innovation measures the difference between the observations and the corresponding model predictions.

An assimilation method uses this difference and its assumptions about uncertainty to calculate an updated state.

3. Free-Run Baseline

The free-run simulation advances the model without observational corrections.

Its numerical evolution can be represented as:

"x_(k+1)^b = M(x_k^b)"

where "M" represents the implemented numerical time-advancement procedure.

The free run establishes the baseline against which assimilated simulations will be evaluated.

It must use documented initial conditions, physical parameters, numerical settings, and boundary conditions.

Where practical, comparisons should begin from equivalent initial conditions and use consistent model configurations.

The free run is essential because a reduction in error cannot be attributed to assimilation unless it is compared with an appropriate baseline.

4. Nudging

4.1 Principle

Nudging introduces a correction that gradually draws the model toward available observations.

A general continuous-time representation is:

"dx/dt = F(x) + G(y - H(x))"

where:

- "F(x)" represents the model's physical evolution.
- "G" represents the nudging correction operator.
- "y - H(x)" is the current observation mismatch.

The precise definition of "G" depends on the observed variables, observation locations, units, and numerical implementation.

4.2 Relaxation toward observations

For a directly observed scalar variable, a simple local relaxation term can be written as:

"du/dt = physical_terms + alpha * (u_obs - u_model)"

where "alpha" has units of inverse time.

A positive relaxation coefficient encourages the model value to move toward the observation.

The coefficient must be selected and tested carefully. Excessively strong corrections may destabilise the numerical solution or cause the model to follow observation noise too closely.

For sparse observations, the correction must be mapped appropriately to the model grid. Its spatial influence must be explicitly defined rather than assumed.

4.3 Proposed implementation

The nudging implementation should:

1. Read observations and their timestamps.
2. Identify the corresponding model variables and locations.
3. Calculate the observation mismatch.
4. Apply a documented correction.
5. advance the numerical model.
6. Record the corrected state and relevant diagnostics.

The correction must respect the model's variable definitions, units, time integration, and numerical constraints.

The initial implementation should begin with a simple, clearly documented nudging scheme before considering more elaborate variants.

5. Optimal Interpolation

5.1 Principle

Optimal Interpolation uses estimates of background-error and observation-error covariance to calculate a statistically weighted correction.

For a linear observation operator, the analysis equation is:

"x_a = x_b + K(y - H x_b)"

where "K" is the gain matrix.

The standard gain expression is:

"K = B H^T (H B H^T + R)^(-1)"

where:

- "B" is the background-error covariance matrix.
- "H" maps the model state to observation space.
- "R" is the observation-error covariance matrix.
- "H^T" is the transpose of "H".

This formulation assumes that the required covariance information is available and that the relevant matrices and inverses are well-defined.

5.2 Interpretation

The analysis balances the model background against the observations.

If the observation errors are large relative to the assumed background errors, the analysis generally gives less weight to those observations.

If the background is considered uncertain and the observations are comparatively reliable, the analysis can give the observations greater influence.

The background covariance also determines how corrections at observed locations can influence other state variables and spatial locations.

5.3 Computational considerations

A complete covariance matrix for a large computational state can be expensive to store and manipulate.

JOVIAN-AP must therefore choose a computationally appropriate representation.

Possible approaches include:

- A small-domain dense covariance matrix for an initial demonstration.
- A structured covariance model.
- A local or spatially limited approximation.
- Matrix-free operations where justified by the implementation.

The chosen method must be documented and its limitations evaluated.

The initial OI implementation should prioritise mathematical transparency and verification over unnecessary complexity.

6. Ensemble Kalman Filter

6.1 Principle

The Ensemble Kalman Filter estimates model uncertainty using an ensemble of model states.

Instead of maintaining only one forecast state, the system advances multiple realisations under an ensemble of initial conditions, perturbations, or other justified sources of uncertainty.

Let the forecast ensemble be:

"x_b^(1), x_b^(2), ..., x_b^(N_e)"

where "N_e" is the ensemble size.

The ensemble mean is:

"x_bar_b = (1/N_e) * sum[x_b^(i)]"

The ensemble spread provides information about the estimated forecast uncertainty.

6.2 Estimate forecast covariance

For each ensemble member, define its deviation from the ensemble mean:

"A_b^(i) = x_b^(i) - x_bar_b"

An ensemble estimate of the background-error covariance is:

"B ≈ (1/(N_e - 1)) * sum[A_b^(i) A_b^(i)^T]"

This estimate describes the covariance represented by the ensemble.

Its accuracy depends on ensemble size, the ensemble-generation procedure, and how well the ensemble represents relevant uncertainties.

A small ensemble may produce noisy covariance estimates and spurious long-distance correlations.

6.3 Analysis update

A common EnKF formulation uses the gain:

"K = B H^T (H B H^T + R)^(-1)"

The ensemble members are then updated using an appropriate ensemble Kalman analysis scheme.

For a deterministic square-root implementation, the analysis ensemble is adjusted so that its mean and spread approximate the desired analysis statistics without perturbing the observations.

Other formulations use perturbed observations. These variants have different implementation details and statistical properties.

JOVIAN-AP must select and document one formulation rather than combining equations from different variants without justification.

6.4 Computational requirements

An EnKF requires multiple model states and repeated analysis calculations.

The main costs include:

- Advancing the ensemble members.
- Storing or accessing the ensemble fields.
- Calculating ensemble statistics.
- Applying the analysis update.
- Transferring corrected states into the model.

The initial ensemble size should be chosen to permit testing on available hardware. Sensitivity to ensemble size should be investigated before making strong claims about performance.

6.5 Physical consistency

The analysis update can introduce states that violate constraints of the underlying physical model.

For JOVIAN-AP, important checks include:

- Positive fluid-layer thickness.
- Acceptable numerical stability.
- Mass conservation or a documented explanation of mass changes.
- Consistent units and state-vector ordering.

Any constraint-handling procedure must be documented and evaluated for its effect on the analysis.

7. Relationship to OpenFOAM

OpenFOAM is intended to provide the numerical fluid model, subject to the successful implementation and verification of the rotating shallow-water formulation.

The assimilation algorithms will need access to model states and a way to return corrected states to the numerical solver.

A possible coupling cycle is:

1. Advance the fluid model.
2. Export or otherwise access the forecast state.
3. Read the observations available at the current assimilation time.
4. Calculate the assimilation update.
5. Map the analysis state back into the model representation.
6. Continue the simulation from the corrected state.
7. Save fields and diagnostics.

The first implementation may use file-based exchange between the solver and external analysis scripts.

The precise coupling design remains open until the solver representation, mesh, time integration, and field layout have been established.

A correction calculated in Python is not sufficient by itself: the updated state must actually be applied to the OpenFOAM-based model before the subsequent forecast is advanced.

The project must distinguish between an offline analysis of saved fields and a genuinely coupled forecast-and-assimilation cycle.

8. Controlled Comparison Strategy

The free run, nudging, OI, and EnKF should be compared under controlled conditions.

Whenever possible, the experiments should share:

- The same designated reference solution.
- Comparable initial conditions.
- The same observation datasets.
- The same observation times and locations.
- Consistent physical parameters.
- Comparable forecast evaluation times.
- Clearly documented numerical settings.

Method-specific parameters, such as nudging strength, covariance assumptions, or ensemble size, must be recorded.

Parameter tuning should be separated from final evaluation when practical, so that reported results do not simply reflect tuning to the evaluation cases.

9. Evaluation Metrics

The primary evaluation metric will be the Root Mean Square Error (RMSE).

For a scalar field:

"RMSE = sqrt[(1/N) * sum((x_i - x_ref_i)^2)]"

where:

- "x_i" is the evaluated model value.
- "x_ref_i" is the reference value.
- "N" is the number of evaluated locations.

Velocity-component errors should be reported separately for "u" and "v".

The project may also evaluate:

- Mean Absolute Error.
- Relative error where mathematically appropriate.
- Spatial error distributions.
- Forecast error growth.
- Mass and potential-vorticity diagnostics where appropriate to the model.
- Computational cost.

Metrics should be calculated over a clearly defined evaluation domain and at documented times.

The reference solution and evaluation grid may differ. If so, the interpolation procedure used to compare them must be documented.

10. Forecast Evaluation

An immediate reduction in analysis error does not necessarily imply a lasting improvement in prediction.

To test forecast skill, an experiment should assimilate observations up to a defined cutoff time and then continue without further observational corrections.

The forecast from that point should be compared with the designated reference solution at several future times.

This allows the project to investigate how long the benefit of assimilation persists.

Results should distinguish:

- Analysis error immediately after assimilation.
- Forecast error after observations stop.
- Error growth over the forecast period.

11. Verification of the Assimilation Algorithms

Before conducting the full experiment programme, each implementation should pass appropriate tests.

11.1 Zero-innovation test

When the model prediction agrees with the observations, the innovation should be zero within the applicable numerical tolerance. The update should not introduce an unintended correction.

11.2 Observation-mapping test

Verify that each observation is associated with the correct variable, coordinate, and time.

11.3 Nudging test

For a controlled scalar case with a fixed observation and no competing physical evolution, verify that the relaxation behaves according to its prescribed coefficient and time integration.

11.4 Optimal Interpolation test

Use a small test problem with known covariance matrices and compare the computed analysis with a direct calculation of the stated OI equations.

11.5 EnKF test

Use a small ensemble with known statistical properties to check the ensemble mean, covariance calculation, observation mapping, and analysis update.

11.6 Coupling test

Verify that the analysis state actually becomes the initial state for the subsequent numerical forecast.

11.7 Reproducibility test

Record configurations, random seeds, software versions, and code revisions so that the experiments can be repeated.

12. Scientific Interpretation

The project does not assume in advance that EnKF, OI, or nudging will perform best.

The results may depend on observation density, noise, forecast lead time, covariance assumptions, numerical errors, and model limitations.

An assimilation method may improve reconstruction under one experimental condition and provide little benefit or even degrade the forecast under another.

The scientific objective is to identify and explain these conditions using verified numerical experiments.

13. Scope and Limitations

The initial study concerns an idealised rotating shallow-water model inspired by Jovian atmospheric dynamics.

Its findings will apply directly to the implemented numerical model and experimental design, not automatically to the complete atmosphere of Jupiter.

The validity of the results depends on the physical formulation, numerical verification, reference solution, observation-generation procedure, and correct implementation of the assimilation algorithms.

14. Completion Criteria

The data assimilation component will be considered implemented when:

1. The selected numerical model has been verified sufficiently for the intended experiments.
2. Synthetic observations can be generated reproducibly.
3. Each implemented assimilation method passes appropriate mathematical tests.
4. The corrected state is correctly applied to the subsequent numerical forecast.
5. The free-run and assimilated experiments can be reproduced from documented configurations.
6. Reconstruction and forecast errors are calculated against a designated reference solution.
7. Numerical limitations and experimental uncertainties are reported honestly.