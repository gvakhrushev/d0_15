# EXP-A4D-GRASSMANN-GRAPH-CLOSURE-RESOLUTION

Class: `EXPENSIVE`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

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
