# EXP-A4D-GRASSMANN-GRAPH-CLOSURE-RESOLUTION

Class: `EXPENSIVE`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `exp/a4d-grassmann-graph-closure-resolution`
Primary artifact: `02_REGISTRY/research/MEMO_A4D_GRASSMANN_GRAPH_CLOSURE_RESOLUTION.md`
Execution: `GitHub-first`

## Why delegated

This is an expensive rank-changing quotient classification requiring exact finite-dimensional incidence geometry, first-jet analysis, exceptional-fiber reconstruction and hostile seam controls. It is isolated so the resolved carrier can be selected without colliding with the active stationary-sector and holonomy lanes.

## GitHub execution contract

Start only from current `main`; run `python tools/task_dispatch.py EXP-A4D-GRASSMANN-GRAPH-CLOSURE-RESOLUTION` before implementation, open a Draft PR before substantive edits, keep changes on the declared branch and primary artifact, obey dependency gates and collision fences, validate narrow targets first, refresh the branch against current main before Ready, self-retire the executable task when required by repository lifecycle, and never self-merge.

## Chat handoff

Return the PR number, final commit SHA, strongest exact theorem or formalization blocker, validation commands/results, and one smallest remaining dependency. A fresh agent must be able to continue from GitHub/task artifacts alone without relying on hidden chat context.


## Objective

Classify the canonical resolution of the rank-changing map

[
Lmapsto operatorname{im}D_L.
]

Test whether the correct resolved carrier is the closure of the generic
rank-64 graph in an incidence/Grassmannian space and classify the exceptional
fiber above the flat rank-60 point.

## Dependencies

Do not start while the current EXPENSIVE WIP limit is saturated.
Before execution, incorporate or independently reproduce the durable results
from #188 and #189.

## Required gates

1. Define the generic graph and its closure without importing arbitrary memory.
2. At `L=I`, set `U=im D_0`, `K=ker D_0`, `Q=C1_+/U`.
3. Derive the first-jet map
   [
   Phi(delta L):K	o Q,qquad kmapsto[delta D,k].
   ]
4. Prove or falsify the transverse limit formula
   [
   G_*=operatorname{im}Phi(delta L),
   qquad
   mathcal I_*=Uoplus G_*.
   ]
5. Classify the realizable exceptional fiber in Plucker/Grassmann coordinates.
6. Determine whether higher jets are required exactly when the first jet loses
   rank.
7. Separate endpoint resolved data from true history dependence.

## Desired terminal

`AFFINE-GAUGE-RANK-SEAM-RESOLVED-BY-GRASSMANN-GRAPH-CLOSURE`

or the first exact obstruction to this construction.

Research only. No Lean, claim/release/BOOK promotion. Checkpoint after every
load-bearing exact result.
