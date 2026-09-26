# WRK-A4D-227-TORSION-DIAGNOSTIC

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
Research lane: `EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `wrk/a4d-227-torsion-diagnostic`  
Primary artifact: `02_REGISTRY/research/A4D_227_TORSION_DIAGNOSTIC.md`  
Execution: `GitHub-first`

## Why delegated

Merged #227 gives an exact curved (E_K=0) family that is rejected by the metric Euler equation. A Cartan torsion computation can characterize why it is not LC-like, but torsion is diagnostic only: the repository already owns that raw/open torsion squared is not a legal generic full-affine scalar.

## Objective

Using the repository's existing discrete Cartan/open-torsion convention, compute the exact torsion 2-form of the #227 family

[
L_0(x)=W_{p(x)},qquad L_s(x)=I,quad s=1,2,3.
]

At standard solder, verify or correct the schematic relation

[
T_{rs}
=
(L_r-I)e_s-(L_s-I)e_r
]

according to the canonical owner.

## Required outputs

1. Exact torsion on every phase (p=0,1,2,3) and every face.
2. Leading small-(t) order.
3. Prove whether
   [
   T=0
   ]
   along the #227 family iff (t=0) in the near-identity chart.
4. Check spatial faces separately from ((0,s)) faces.
5. Record the relation, if any, between:
   - curvature amplitude (c(t));
   - metric partial (E_Q);
   - torsion amplitude.
6. If the joint-linear invisible-kernel worker is already available, optionally evaluate the linear torsion map on its diagonal invisible basis, but do not block the primary #227 result on this extension.

## Claim fence

This worker must explicitly state:

- torsion-free is **not** added as a new field equation;
- no (T_{\rm open}^2) action term is introduced;
- the result is a branch diagnostic compatible with the existing Palatini equations;
- full-affine legality of raw open torsion is not claimed.

## Terminal

`J2-227-CURVED-STATIONARY-FAMILY-TORSION-DIAGNOSTIC-CERTIFIED`

or a corrected terminal if the expected torsion pattern is false.

## GitHub execution contract

Start from fresh current `main`. Open Draft before substantive edits, self-retire at the exact diagnostic terminal, refresh against main before Ready, and never self-merge.

## Chat handoff

Return PR, SHA, canonical torsion formula used, exact phase/face table, small-(t) order, and whether torsion-free cuts the #227 family only at identity.
