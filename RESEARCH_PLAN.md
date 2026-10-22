# JOVIAN-AP Research Plan

## 1. Research Objective

JOVIAN-AP aims to develop a reproducible computational framework
for investigating the reconstruction and prediction of rotating
atmospheric flows inspired by Jupiter's jets and vortices.

The central research question is whether assimilating sparse,
noisy observations into a numerical flow model can improve the
estimation of the underlying flow state and the accuracy of
subsequent predictions compared with an unassimilated simulation.

The project will combine mathematical modelling, computational
fluid dynamics, observation modelling, data assimilation,
quantitative evaluation, and scientific visualisation.

## 2. Scientific Scope

The initial physical model will use a rotating shallow-water
formulation on a suitable beta-plane domain.

This model provides a tractable framework for investigating
rotating flows, planetary vorticity variation, jet structures,
and coherent vortices.

The shallow-water approximation is a deliberate modelling choice.
It does not represent the full three-dimensional structure,
thermodynamics, or atmospheric chemistry of Jupiter.

A future extension may investigate more complete atmospheric
models after the initial framework has been implemented and
verified.

## 3. Mathematical Foundations

The mathematical development will cover:

- Conservation of mass.
- Momentum conservation in a rotating reference frame.
- Coriolis acceleration and planetary vorticity variation.
- Potential vorticity and its interpretation.
- Initial and boundary conditions.
- Dimensional analysis and nondimensional parameters.
- Spatial and temporal discretisation.
- Numerical stability and conservation properties.

The governing equations and assumptions will be documented
before implementation. Their numerical form must be consistent
with the selected model and solver.

## 4. Numerical Implementation

OpenFOAM will be evaluated and used where its numerical
framework is appropriate for the selected equations.

The implementation may require a custom solver or modification
of an existing solver. The choice will depend on whether the
required rotating shallow-water equations can be represented
correctly using the available formulations.

The numerical implementation will document:

- Governing equations and discretisation.
- Mesh generation and domain configuration.
- Initial and boundary conditions.
- Solver settings and convergence criteria.
- Time-step selection and stability constraints.
- Conservation and verification checks.
- Reproducible execution instructions.

Python will support observation generation, data assimilation,
statistical evaluation, plotting, and experiment automation.

ParaView will support inspection and visualisation of simulation
fields and derived quantities.

## 5. Observation Modelling

Synthetic observations will be generated from a controlled
reference solution or another clearly documented reference state.

The observation framework will investigate:

- Sparse spatial sampling.
- Observation intervals.
- Measurement noise.
- Observation coverage.
- Missing observations.
- Differences between the reference state and model state.

Observation generation must be reproducible. Random noise,
when used, will have documented statistical assumptions and
configurable random seeds.

## 6. Data Assimilation Methods

The study will establish an unassimilated free-run baseline
before evaluating data assimilation methods.

The planned comparisons include:

1. Free-run simulation.
2. Newtonian relaxation or nudging.
3. Optimal interpolation.
4. Ensemble Kalman Filter.
5. Localisation and inflation strategies where appropriate.

Methods will be implemented and evaluated progressively.
Each method will be compared using consistent reference data,
initial conditions, observation schedules, and evaluation metrics.

The project will document the assumptions, computational costs,
limitations, and performance of each implemented method.

## 7. Experimental Programme

The experimental programme will investigate the following areas:

- Baseline numerical behaviour.
- Sensitivity to observation density.
- Sensitivity to observation noise.
- Sensitivity to observation frequency.
- Sensitivity to initial-state errors.
- Sensitivity to model parameters.
- Comparison of assimilation methods.
- Forecast performance after assimilation.
- Robustness across multiple controlled cases.
- Computational cost and reproducibility.

The final experiment matrix will be refined after the physical
model and numerical implementation have been verified.

## 8. Quantitative Evaluation

Evaluation will use clearly defined metrics appropriate to
the simulated fields and research question.

Candidate metrics include:

- Root mean square error.
- Mean absolute error.
- Relative error where mathematically appropriate.
- Spatial error distributions.
- Error growth during forecast periods.
- Conservation diagnostics.
- Computational runtime.

Results will compare the free-run baseline against assimilated
simulations using consistent reference states and evaluation
times.

Any reported improvement must be calculated from actual
simulation outputs. Limitations and cases where assimilation
does not improve performance will also be documented.

## 9. Verification and Reproducibility

The project will include verification tests suitable for the
chosen equations and numerical methods.

These may include simplified analytical cases, limiting cases,
grid-refinement studies, time-step sensitivity studies,
conservation checks, and comparison against trusted reference
solutions where available.

The repository will document software versions, configuration
files, execution commands, experiment settings, and procedures
for reproducing reported results.

Illustrative examples will be clearly distinguished from
completed simulations and verified results.

## 10. Repository Deliverables

The completed research repository is intended to contain:

- Mathematical and physical documentation.
- Numerical solver implementation or required solver extensions.
- Mesh and case configuration files.
- Synthetic observation generation tools.
- Data assimilation implementations.
- Verification and testing procedures.
- Reproducible experiment configurations.
- Quantitative analysis scripts.
- Generated plots and selected visualisations.
- Results and interpretation.
- Scientific references and citation metadata.
- Installation and execution instructions.

Generated data and large simulation outputs will be managed
carefully so the repository remains practical to clone and use.

## 11. Research Integrity

JOVIAN-AP will distinguish clearly between planned work,
implemented methods, completed simulations, verified results,
and future extensions.

No numerical result, validation claim, or performance improvement
will be presented as established without supporting evidence.

Model assumptions, numerical limitations, software dependencies,
and sources of uncertainty will be documented.

The project aims to produce a scientifically defensible and
reproducible computational study rather than relying on
visualisations alone.

## 12. Long-Term Direction

After the initial rotating shallow-water framework has been
implemented, verified, and evaluated, the project may be extended
toward more complex planetary-atmosphere models.

Potential extensions include more realistic physical forcing,
additional observations, improved assimilation algorithms,
three-dimensional modelling, and comparisons with published
planetary-atmosphere datasets.

These extensions will be pursued only when their mathematical,
computational, and validation requirements can be addressed.

## 13. Completion Criteria

The research will be considered computationally complete when:

- The selected governing equations are documented.
- The numerical implementation has passed appropriate checks.
- Synthetic observations can be generated reproducibly.
- The free-run baseline is established.
- At least one data assimilation method is implemented and tested.
- Controlled experiments compare assimilated and unassimilated
  simulations.
- Quantitative results are reproducible.
- Findings and limitations are documented.
- Installation and execution instructions are complete.

Additional assimilation methods and model extensions will be
included according to their scientific value and verification.

The final conclusions will be based on the completed experiments
rather than assumed outcomes.