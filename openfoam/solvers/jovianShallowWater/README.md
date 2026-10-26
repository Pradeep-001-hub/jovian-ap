# jovianShallowWater

## 1. Purpose

`jovianShallowWater` is the planned native OpenFOAM C++ solver for
JOVIAN-AP.

Its purpose is to solve a single-layer rotating shallow-water model
that can be used to investigate idealised planetary jets, vortices,
and atmospheric-flow reconstruction.

The initial target is OpenFOAM Foundation v14.

This directory currently defines the solver's implementation plan.
A working solver must be implemented, compiled, and verified before
simulation results can be reported.

## 2. Governing equations

The initial model uses the rotating shallow-water equations.

Layer-thickness conservation:

    d(h)/dt + div(h U) = 0

Horizontal momentum:

    d(U)/dt + (U . grad)U + f k x U
        = -g grad(h) + D(U) + F

The beta-plane approximation is:

    f(y) = f0 + beta*y

Here:

- `h` is the total layer thickness.
- `U` is the horizontal velocity.
- `f` is the Coriolis parameter.
- `g` is the selected effective gravity.
- `D(U)` represents explicitly defined dissipation.
- `F` represents explicitly defined forcing.

The physical interpretation and numerical treatment of every term
must be documented.

## 3. Implementation strategy

The solver will be developed as a native OpenFOAM C++ application.

OpenFOAM will provide the mesh, field representation, finite-volume
infrastructure, time control, boundary conditions, and output.

The shallow-water equations require a suitable formulation for
layer-thickness and horizontal-momentum evolution. They must not be
implemented by simply treating the model as an ordinary
three-dimensional incompressible-flow problem.

The solver architecture must be checked against OpenFOAM Foundation
v14 source code and APIs before implementation.

## 4. Development sequence

### Stage 1: Solver foundation

- Establish the native C++ application structure.
- Read the mesh and simulation controls.
- Define the physical fields and parameters.
- Establish a reproducible build procedure.

### Stage 2: Governing equations

- Implement layer-thickness conservation.
- Implement horizontal momentum.
- Add the Coriolis source term.
- Add configurable dissipation only after the basic equations work.

### Stage 3: Verification

- Test a uniform resting layer.
- Check layer-mass conservation.
- Check positivity of layer thickness.
- Test suitable wave and balanced-flow cases.
- Assess mesh and time-step sensitivity.

### Stage 4: Idealised flows

- Introduce a vortex initial condition.
- Develop a controlled jet configuration.
- Document all initial and boundary conditions.

### Stage 5: Data assimilation

Only after the underlying solver has passed its initial verification:

- Generate synthetic observations.
- Establish a free-running forecast baseline.
- Implement and compare assimilation methods.
- Evaluate forecasts against withheld synthetic observations.

## 5. Scientific limitations

The initial solver is a simplified rotating shallow-water model.

It is not a complete three-dimensional model of Jupiter's atmosphere.

Its results must not be described as validated predictions of
Jupiter's real weather without independent scientific evidence.

## 6. Completion criteria

The solver will be considered operational only when:

1. It compiles against the intended OpenFOAM Foundation version.
2. A documented test case runs successfully.
3. Numerical and physical checks produce recorded results.
4. The test can be reproduced using documented settings.