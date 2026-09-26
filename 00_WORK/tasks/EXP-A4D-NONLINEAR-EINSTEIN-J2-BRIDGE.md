# EXP-A4D-NONLINEAR-EINSTEIN-J2-BRIDGE

Class: `EXPENSIVE`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `exp/a4d-nonlinear-einstein-j2-bridge`
Primary artifact: `02_REGISTRY/research/MEMO_A4D_NONLINEAR_EINSTEIN_J2_BRIDGE.md`
Execution: `GitHub-first`

## Why delegated

This is the upper-wall OTO problem after the exact finite seed is known. PR #201 certified `K_star,metric=(1/4)K_E_eta` with zero `E_sp` contamination. The next question is whether this finite response extends to one metric-only smooth local second-jet response satisfying the hypotheses that place it in the Einstein/Lovelock class, or where that bridge fails. This requires geometry and natural-operator research, not more coefficient fitting.

## Runtime / collision gate

Search for an open PR carrying this exact task id before starting. Do not edit #202 F4 artifacts or the Palatini target-span primary memo. Treat any unmerged #203 result as provisional until independently reproduced or landed.

## Current repository-owned inputs

- #201: `S_STAR-CARRIES-EINSTEIN-SEED`, with exact `c_eta=1/4 != 0`, `c_sp=0`.
- #201: `R=O(X^4 t)`, quadratic `Q=O(X^8 t^2)`, hence `j^2_flat Q=0`.
- E-NJET: the owned finite `E_eta,N` normal-jet estimator reconstructs `-2G[g]+O(epsilon_N^2)` under its explicitly imported normal-coordinate/geometric hypotheses.
- E-RAYSEL: the extra spatial ray fails metric-only frame erasure.
- E-T4NAT: one fixed T4 carrying all Lorentz metric 2-jets is sufficient for the cited local natural-tensor theorem; arbitrary-manifold reconstruction is not the immediate blocker.
- E-LORSEL: no separate finite selector forces beta=0; #201 bypasses that blocker by deriving the star Hessian directly.

## Objective

Construct, or sharply obstruct, the shortest bridge

`finite EL(S_star) -> metric-only smooth local J^2 response E[g] -> a G[g] + b g`

without importing the Einstein field equation as D0 dynamics.

## Required gates

1. Define the nonlinear metric readout from the selected finite action, not from an arbitrary metric stencil.
2. State every reconstruction/interpolation assumption separately from finite consequences.
3. Test arbitrary Lorentz 2-jets, not one normal-frame sample.
4. Prove/falsify local frame/grid erasure.
5. Separate recognition of `G` plus external contracted Bianchi from an internally derived finite-Noether-to-covariant-divergence route.
6. Classify any zeroth-order `b g` channel separately; do not tune Lambda from phi.
7. Audit the exact Navarro/Lovelock hypotheses and cite which are proved, imported, or still missing.
8. If the bridge fails, name the first minimal obstruction and give an explicit counterexample.

## Two-sided attack

Bottom-up: nonlinearize the exact #201 star response and follow the quotient/metric map.

Top-down: write the minimal local second-order, metric-only, local-Diff-natural, divergence-free target class and determine exactly which antecedent the finite action does or does not supply.

## Falsification controls

Reject a frame-dependent `G + alpha R q_grid`; detect any reappearance of `E_sp`; reject a theorem valid only in one selected normal frame; keep continuum definitions/classification external where appropriate.

## Desired terminal

Either `STAR-ACTION-NONLINEAR-J2-RESPONSE-ENTERS-EINSTEIN-LOVELOCK-CLASS` with explicit hypotheses/coefficient map, or a smallest named obstruction.

## GitHub execution contract

Start only from current `main`; run `python tools/task_dispatch.py EXP-A4D-NONLINEAR-EINSTEIN-J2-BRIDGE`; open a Draft PR before substantive work; checkpoint exact and structural results; no Lean/claims/release/BOOK promotion; refresh before Ready; never self-merge.

## Chat handoff

Return PR, SHA, exact/structural bridge statement, all external hypotheses, coefficient map if reached, and the first remaining obstruction.
