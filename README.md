# jovian-ap
A research prototype for estimating and forecasting Jupiter's global atmospheric state from sparse observations, with uncertainty.
# JOVIAN-AP: Data Assimilation with an OpenFOAM-Based Rotating-Flow Model of Jovian Jets and Vortices

> A research prototype for estimating and forecasting the state of Jupiter-like atmospheric jets and vortices from sparse, noisy observations, with uncertainty made explicit.

**Status:** Early-stage research prototype (discussion draft, October 2026)
**Author:** Pradeep
**Repository visibility:** Private until the supervisor and university IP policy are confirmed

---

## Table of contents

1. [Project name and meaning](#1-project-name-and-meaning)
2. [Background and motivation](#2-background-and-motivation)
3. [The long-term vision](#3-the-long-term-vision)
4. [Scope of this repository (first stage)](#4-scope-of-this-repository-first-stage)
5. [What this project does NOT claim](#5-what-this-project-does-not-claim)
6. [Research questions and hypotheses](#6-research-questions-and-hypotheses)
7. [Physical model](#7-physical-model)
8. [Numerical setup in OpenFOAM](#8-numerical-setup-in-openfoam)
9. [Observing system simulation experiment (OSSE)](#9-observing-system-simulation-experiment-osse)
10. [Data assimilation methods](#10-data-assimilation-methods)
11. [The coupled assimilation cycle](#11-the-coupled-assimilation-cycle)
12. [Evaluation and metrics](#12-evaluation-and-metrics)
13. [Experiments planned](#13-experiments-planned)
14. [Repository structure](#14-repository-structure)
15. [Getting started](#15-getting-started)
16. [Reproducibility rules](#16-reproducibility-rules)
17. [Data sources and provenance](#17-data-sources-and-provenance)
18. [Roadmap](#18-roadmap)
19. [Risks and limitations](#19-risks-and-limitations)
20. [Future work](#20-future-work)
21. [References and literature leads](#21-references-and-literature-leads)
22. [License and citation](#22-license-and-citation)

---

## 1. Project name and meaning

**JOVIAN-AP** stands for **Jovian Atmospheric Observation, Reconstruction and Prediction System**.

"Jovian" means "relating to Jupiter" (from *Jove*, a poetic name for the Roman god Jupiter). The name describes the long-term idea: observe, reconstruct, simulate and predict the atmosphere of Jupiter.

This repository implements the **first, narrow research stage** of that idea.

## 2. Background and motivation

Jupiter's atmosphere contains alternating east-west jets, long-lived vortices (including the Great Red Spot) and turbulent structures. Our knowledge of its state comes from:

- Spacecraft such as Juno (visible, infrared and microwave instruments)
- Space and ground telescopes (for example Hubble imaging)
- Cloud-tracking methods that estimate winds from image sequences

These observations are **sparse in space and time, uneven in quality, and sometimes delayed**. They do not directly give every atmospheric variable everywhere.

In Earth weather prediction, this problem is addressed with **data assimilation**: combining a physics-based model forecast with observations to produce the best-supported estimate of the current state, along with its uncertainty. This project studies a small, testable version of that approach for Jupiter-like rotating flow, built on OpenFOAM.

## 3. The long-term vision

The full vision (not implemented here) is an evolving, observation-updated, three-dimensional estimate of Jupiter's global atmosphere:

1. A spacecraft-side module that processes, prioritises and transmits observations
2. An Earth-side modelling system that assimilates observations into a physics model
3. Forecasts with uncertainty maps
4. Advisory guidance on which future observations would reduce uncertainty most

This is a long-term research and mission-development goal. It requires a large team, mission access and validated global 3D models.

## 4. Scope of this repository (first stage)

| Long-term vision | First stage (this repo) |
|---|---|
| Global, multilayer 3D atmosphere | Regional or beta-plane rotating-flow model |
| Real mission data stream | Synthetic observations (OSSE), real data optional later |
| Spacecraft onboard processing | Not implemented (future work) |
| Operational real-time updates | Offline, cycled experiments |
| Observation-targeting guidance | Observation-impact study |

**Core question of this stage:** Can an OpenFOAM-based rotating-flow model give better short-term state estimates and forecasts of Jupiter-like jets and vortices when it is updated with sparse observations than when it runs without them?

## 5. What this project does NOT claim

- It does not claim continuous, full-planet observation of Jupiter.
- It does not claim a validated global 3D digital twin.
- It does not claim flight-ready onboard software or any mission integration.
- It does not claim novelty until a literature review confirms it.
- A ParaView animation is not validation. Success is judged by equations, numerical verification and quantitative metrics.

## 6. Research questions and hypotheses

**RQ1: Model.** Can OpenFOAM reproduce Jupiter-like zonal jets and vortices in a rotating-flow model with verified stability and conservation properties?
*H1:* A verified configuration reproduces expected jet structure and vortex behaviour against a reference solution.

**RQ2: Assimilation benefit.** Does assimilating sparse observations improve state estimates and short-term forecasts?
*H2:* Nudging, optimal interpolation (OI) and an ensemble Kalman filter (EnKF) each reduce error compared with a free run, and the benefit shrinks as observation coverage falls.

**RQ3: Observation impact.** Which observation types and placements matter most?
*H3:* Observations near jet cores and vortex edges give more improvement per observation than uniform sampling.

**RQ4: Practical limits.** What are the cost and accuracy limits of OpenFOAM-based ensembles?
*H4:* A small ensemble (roughly 10 to 30 members) on a coarse mesh gives useful, reasonably calibrated spread at feasible runtime.

## 7. Physical model

### 7.1 Starting formulation: rotating shallow water

The first model is a rotating shallow-water system on a beta-plane (a local Cartesian approximation where the Coriolis parameter varies linearly with latitude):

```
du/dt + (u . grad) u + f k x u = -g grad(h) + nu * laplacian(u) - r * u + F
dh/dt + div( (H + h) u )       = 0

f = f0 + beta * y
```

Where:

- `u` is the horizontal velocity vector, `h` the layer-height perturbation, `H` the mean layer depth
- `f` is the Coriolis parameter, `beta` its northward gradient
- `g` is an effective (reduced) gravity for the layer
- `nu` is viscosity or hyperviscosity, `r` is a linear drag, `F` is forcing used to maintain jets

Parameters (planet radius, rotation rate of about 9.9 hours, jet speeds and spacing, effective gravity, layer depth) must be taken from **verified literature**, and the source recorded in `docs/parameters.md`.

### 7.2 Why shallow water first

- It captures rotation, jets, vortices and wave dynamics at low cost.
- It is simple enough to verify properly.
- It does **not** capture thermodynamics, deep structure or full 3D dynamics. These are later extensions.

### 7.3 Staged model complexity

| Stage | Capability | Evidence of success |
|---|---|---|
| M1 | Single-layer rotating shallow water, beta-plane | Stability, conservation, reference comparison |
| M2 | Jet forcing and vortex initialisation | Jupiter-like jet spacing, vortex persistence |
| M3 (optional) | Two layers or added thermodynamics | Sensitivity tests, documented expectations |
| M4 (future) | Spherical or global geometry | Handled outside this stage |

### 7.4 Solver choice

Before writing a custom solver, check whether your OpenFOAM distribution and version already includes a shallow-water or geophysical-flow solver. Record the distribution (Foundation or ESI), version and solver in `docs/solver_decision.md`. If a custom solver is needed, verify it against analytical or reference cases before any assimilation work.

## 8. Numerical setup in OpenFOAM

Document and version-control all of the following:

- OpenFOAM distribution and version
- Domain size, boundary conditions (for example periodic in x, walls or sponge in y)
- Mesh type and resolution for the truth and ensemble meshes
- Discretisation schemes (time, convection, diffusion)
- Time step and the stability criterion used (Courant number)
- Viscosity or hyperviscosity values and why they were chosen
- Initial conditions and spin-up procedure

### Verification checklist

- [ ] Geostrophic balance test (steady balanced state stays balanced)
- [ ] Gravity wave or Rossby wave propagation against analytical speed
- [ ] Mass conservation check
- [ ] Energy behaviour check (dissipation only where intended)
- [ ] Mesh convergence study (at least three resolutions)
- [ ] Time-step sensitivity test
- [ ] Reproducibility test (same inputs give same outputs)

## 9. Observing system simulation experiment (OSSE)

An OSSE tests an assimilation system in a controlled setting where the truth is known.

1. **Truth run:** A high-resolution OpenFOAM simulation after spin-up. This is treated as "reality".
2. **Synthetic observations:** Sampled from the truth at chosen locations and times, with added noise. Typical observed quantities: velocity components, layer height, or a derived quantity.
3. **Sparse and irregular sampling:** Observations are thinned in space and time, with gaps, to mimic real coverage.
4. **Model under test:** A coarser mesh and/or perturbed parameters, so the model is deliberately imperfect (avoiding the "identical twin" problem as far as possible).
5. **Assimilation and forecast:** Assimilate the synthetic observations, then forecast and compare with the truth.

**Important:** Keep a set of observations **held out** from assimilation and use them only for verification.

## 10. Data assimilation methods

Implement these in order. Do not move to the next until the previous one is working and tested.

### 10.1 Free run (baseline A)
The model runs from a perturbed or imperfect initial state with no observations.

### 10.2 Nudging (Newtonian relaxation)
```
dx/dt = M(x) + G * (y - H(x))
```
Simple and cheap. `G` is a relaxation gain. Good as a first assimilation experiment.

### 10.3 Optimal interpolation (OI)
```
x_a = x_f + K (y - H x_f)
K   = B H^T (H B H^T + R)^(-1)
```
`B` is a fixed background-error covariance (often a distance-based function), `R` the observation-error covariance.

### 10.4 Ensemble Kalman filter (EnKF)
```
x_a(i) = x_f(i) + K (y(i) - H x_f(i))
K      = P_f H^T (H P_f H^T + R)^(-1)
```
`P_f` is estimated from the ensemble. Use perturbed observations `y(i)` for the stochastic EnKF. Add:

- **Covariance localisation** to remove spurious long-range correlations from small ensembles
- **Covariance inflation** to avoid ensemble collapse

Consider the LETKF later if time allows.

### 10.5 Observation operator
`H` maps the model state to the observed quantity. At first, `H` simply interpolates model fields to observation locations. More complex operators (for example for brightness temperature) are outside the first stage.

## 11. The coupled assimilation cycle

OpenFOAM has no built-in ensemble Kalman filter, so the analysis step is a small external program coupled by files.

```
          +--------------------+
          |  Truth run (OF)    |--> sample + add noise --> observations
          +--------------------+
                                              |
 +-------------------+   forecast    +--------v---------+
 | Ensemble members  |-------------->| Analysis utility |
 | (OpenFOAM runs)   |<--------------| (Python or C++)  |
 +-------------------+  updated      +------------------+
          ^             fields
          |                                  |
          +---- restart next cycle ----------+
```

### Cycle steps

1. Run N members from current initial conditions to the analysis time.
2. Extract each member's fields at observation locations (sampling/probes, or read the fields directly).
3. The analysis utility computes the update using nudging, OI or EnKF.
4. Write updated fields as new initial conditions in each member's time directory.
5. Restart OpenFOAM and continue to the next analysis time.
6. Log everything: analysis time, ensemble spread, innovation statistics, runtime.

### Skills note
The analysis step is a few hundred lines. It can be written in Python with NumPy, or as a C++ OpenFOAM utility. Bash scripts handle running members and restart cycles.

## 12. Evaluation and metrics

| Metric | What it tells you |
|---|---|
| RMSE vs truth (analysis, forecast at several lead times) | Accuracy |
| Error against held-out observations | Honest forecast skill |
| Ensemble spread | Estimated uncertainty |
| Spread-skill ratio (mean spread / RMSE) | Whether uncertainty is calibrated (near 1 is good) |
| Rank histogram | Ensemble reliability (flat is good) |
| Innovation statistics (observation minus forecast) | Filter consistency |
| Runtime and core-hours | Practical cost |
| Sensitivity to observation density, noise and gaps | Robustness |
| Failure cases (divergence, collapse) | Honest limits |

**Baselines:** (A) free run, (B) each assimilation method. Always compare against A.

## 13. Experiments planned

| ID | Experiment | Purpose |
|---|---|---|
| E1 | Model verification suite | Prove the model is trustworthy |
| E2 | Spin-up and jets/vortex case | Produce a Jupiter-like truth |
| E3 | Free run vs truth | Establish error growth and predictability horizon |
| E4 | Nudging | First assimilation benchmark |
| E5 | OI | Static-covariance baseline |
| E6 | EnKF with localisation and inflation | Main method |
| E7 | Observation density sweep | How much data is enough |
| E8 | Observation type and placement study | Observation-impact result (RQ3) |
| E9 | Ensemble-size and runtime study | Practical limits (RQ4) |
| E10 (optional) | Real wind data case | Realism check |

## 14. Repository structure

```
jovian-ap/
├── README.md
├── LICENSE
├── CITATION.cff
├── .gitignore
├── environment.yml            # Python environment (pinned versions)
├── docs/
│   ├── proposal/              # proposal PDFs and abstract
│   ├── parameters.md          # physical parameters with sources
│   ├── solver_decision.md     # OpenFOAM version and solver choice
│   └── literature_notes.md    # review table: paper, method, model, data, relevance
├── openfoam/
│   ├── cases/
│   │   ├── verification/      # geostrophic, wave, convergence cases
│   │   ├── truth/             # high-resolution truth case
│   │   └── ensemble/          # template for ensemble members
│   ├── solvers/               # custom solver source, if any
│   └── scripts/               # run, clean, restart (bash)
├── assimilation/
│   ├── nudging.py
│   ├── optimal_interpolation.py
│   ├── enkf.py
│   ├── observation_operator.py
│   └── localisation.py
├── observations/
│   ├── generate_synthetic.py
│   └── README.md              # how observations are made, noise model
├── experiments/
│   ├── configs/               # one config per experiment (E1..E10)
│   └── run_experiment.sh
├── analysis/
│   ├── metrics.py             # RMSE, spread-skill, rank histogram
│   └── plots.py
├── notebooks/
├── tests/                     # tests for assimilation and metrics code
├── data/
│   └── README.md              # sources, versions, usage terms (no large files)
└── results/                   # ignored by git; small summaries only
```

## 15. Getting started

> Commands are placeholders. Update them after your environment is set up.

```bash
# 1. Clone
git clone <repo-url> jovian-ap
cd jovian-ap

# 2. Python environment (for analysis and assimilation)
conda env create -f environment.yml
conda activate jovian-ap

# 3. OpenFOAM environment
#    Source your OpenFOAM installation (distribution and version in docs/solver_decision.md)
source /path/to/openfoam/etc/bashrc

# 4. Run a verification case
cd openfoam/cases/verification/<case-name>
./Allrun

# 5. Run an experiment
cd ../../../../
bash experiments/run_experiment.sh experiments/configs/E4_nudging.yaml
```

## 16. Reproducibility rules

- Commit **configurations and scripts**, not large outputs. Use `.gitignore`, or Git LFS or DVC if needed.
- Tag the code state behind every reported result (for example `paper1-v1`).
- Record random seeds for noise and ensemble perturbations.
- Record OpenFOAM version, compiler, and Python package versions.
- Label every dataset and figure clearly as **synthetic** or **real**.
- Never commit credentials, unpublished third-party data or copyrighted papers.

## 17. Data sources and provenance

For each dataset used, record in `data/README.md`:

| Field | Example |
|---|---|
| Name and version | (to be filled) |
| Source and URL | (to be filled) |
| Access and usage terms | (to be filled) |
| Calibration and known limits | (to be filled) |
| How it is used | Synthetic / real, assimilated / held out |

Candidate real-data sources to investigate: NASA Planetary Data System (Juno archive), Hubble OPAL Jupiter observations, published cloud-tracked wind products. Verify availability, format and terms before use.

## 18. Roadmap

| Phase | Period | Deliverable |
|---|---|---|
| 1. Literature and data audit | Months 1-6 | Literature review draft, novelty check, solver decision |
| 2. Model build and verification | Months 7-15 | Verified OpenFOAM model (E1, E2) |
| 3. OSSE and assimilation | Months 16-27 | Nudging, OI, EnKF results (E3-E6) |
| 4. Observation impact | Months 28-36 | E7-E9 results |
| 5. Optional extension | Months 37-42 | Real-data case or added physics |
| 6. Thesis writing | Months 43-48 | Thesis and defence |

## 19. Risks and limitations

| Risk | Mitigation |
|---|---|
| OpenFOAM lacks a suitable rotating-flow solver | Start regional or beta-plane; check existing solvers; verify any custom solver |
| Ensemble runs too expensive | Coarse mesh, small ensemble, fall back to nudging and OI |
| Limited Python skills | Keep scripting small; learn NumPy early; consider a C++ utility or co-supervisor |
| Regional domain seen as too limited | State scope clearly; position global work as future |
| Identical-twin optimism | Use different mesh or perturbed parameters for the model under test |
| Novelty already covered | Early literature review; keep observation-impact as a fallback contribution |
| Sparse real verification data | OSSE-first design; use denser imaging-based winds later |
| Visuals mistaken for proof | Use quantitative metrics and held-out data |

## 20. Future work

- Global or spherical-geometry model
- Added thermodynamics and multilayer or 3D structure
- Assimilation of real Juno or imaging-derived observations, including the microwave radiometer (a research problem in itself)
- Machine-learning surrogates for cheaper ensembles
- Uncertainty-guided observation prioritisation
- A spacecraft-side data prioritisation concept, tested in simulation only

## 21. References and literature leads

> These are **search leads, not verified citations**. Confirm title, authors, year, DOI and relevance before citing.

- **Jovian dynamics:** Showman (2007) on forced shallow-water turbulence; Kaspi et al. (2018) on the depth of Jupiter's jets; Marcus and co-authors on the Great Red Spot
- **Data assimilation:** Evensen on the EnKF; Hunt, Kostelich and Szunyogh (2007) on the LETKF; Kalnay's textbook on atmospheric modelling, data assimilation and predictability
- **Planetary precedents:** Mars atmosphere data assimilation (important for the novelty check)
- **Observations:** Hubble OPAL Jupiter winds; Juno MWR retrieval papers; cloud-tracking and image-velocimetry methods
- **OpenFOAM:** existing shallow-water or geophysical-flow solvers and rotating-frame studies

## 22. License and citation

- **License:** not yet chosen. All rights reserved until a license is added (consider MIT or BSD for code and CC-BY for documents when the repository becomes public, after checking university policy).
- **Citation:** see `CITATION.cff` (to be added).

---

*This README describes a planning-stage research prototype. It is not a validated scientific model, a mission proposal, or a claim of novelty.*