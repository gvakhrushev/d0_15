# WRK-A4D-J2-SLOW-BACKGROUND-DIAGONAL-GERM

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
Research lane: `EXP-A4D-J2-UNIFORM-COUPLED-NORMAL-RESCUE`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `wrk/a4d-j2-slow-background-diagonal-germ`  
Primary artifact: `02_REGISTRY/research/A4D_J2_SLOW_BACKGROUND_DIAGONAL_GERM.md`  
Execution: `GitHub-first`

## Why delegated

The expensive rescue theorem must control slow-background perturbations of resonant normal germs. The frozen diagonal quarter-wave is already owned well enough to make a bounded hostile-control calculation possible. This worker tests one concrete mechanism only: whether the first slow-background corrections to the corrected polarized diagonal reduced equation create new zero-source flat-approaching sheets of the u^3-hu type.

This is a control/certificate, not the global rescue theorem.

## Mandatory inputs

- the corrected polarized #208 connection block;
- #216 diagonal Lyapunov-Schmidt / Puiseux certificate and exact reduced quartic;
- #216 fixed-realization IR memo for the meaning of a slow background;
- no #202 variables or lower-wall action channels.

## Objective

Introduce one declared low-frequency smooth background mode or equivalent local slow parameter into the diagonal quarter-wave reduction and derive the first nonzero background-dependent correction to the **full range-reduced normal Euler germ** at zero external UV source.

Use exact symbolic/rational algebra wherever possible.

The canonical question is whether the reduced zero-source equation acquires terms schematically like

[
h,L_1u,qquad
h,Q_2(u),qquad
h^2L_2u,
]

that can split the frozen flat sheet and generate nonzero roots u(h)->0.

## Required gates

1. Reproduce the frozen diagonal reduced germ from the existing certificate.
2. Specify the slow background unambiguously: momentum, polarization/metric component, scaling variable, and sidebands retained.
3. Include every sideband/range mode required at the perturbative order used; do not project them away by hand.
4. Derive the background-dependent reduced normal map through the first order capable of changing the zero set.
5. Solve/classify the zero-source small-root scaling at that order.
6. Distinguish:
   - coefficient vanishing by symmetry;
   - a genuine no-new-sheet result to the computed order;
   - an explicit bifurcation term producing u(h)->0.
7. Check the result against the hostile abstract model u^3-hu.

## Terminal outcomes

- `J2-DIAGONAL-SLOW-BACKGROUND-NO-NEW-SHEET-TO-CERTIFIED-ORDER`
- `J2-DIAGONAL-SLOW-BACKGROUND-FLAT-SPLITTING-TERM-FOUND`
- `J2-DIAGONAL-SLOW-BACKGROUND-GERM-BLOCKED-BY-MISSING-RANGE-DATA`

A positive no-splitting result is only a model control and must not be promoted to the global theorem.

## Forbidden

No orbit enumeration. No new Newton scout without the exact reduced coefficients. No new action channel. No modification of the finite action. No claim that one diagonal control proves uniform rescue.

## Handoff

Return the PR, SHA, declared slow background, exact reduced correction, small-root classification, and the perturbative order certified.
