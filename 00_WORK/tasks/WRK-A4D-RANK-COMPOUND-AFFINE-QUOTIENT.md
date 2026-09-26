# WRK-A4D-RANK-COMPOUND-AFFINE-QUOTIENT

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
Research lanes: lower-wall #202 / cross-wall parabolic seam

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `wrk/a4d-rank-compound-affine-quotient`  
Primary artifact: `02_REGISTRY/research/A4D_RANK_COMPOUND_AFFINE_QUOTIENT.md`  
Execution: `GitHub-first`

## Why delegated

The homogeneous parabolic #202 controls expose a precise blind spot of the old det/adj affine residual on rank-two Lorentz holonomy. The rank-adapted exterior-compound coordinate is an algebraic quotient statement independent of the open finite-vacuum search and can be certified separately without changing the physical action.

## Objective

Let

[
H=(P,t),qquad M=I-P,qquad operatorname{rank}M=r.
]

Define

[
Psi_r(M,t):Lambda^rV	oLambda^{r+1}V,
qquad
omegamapsto twedge(Lambda^rM)omega.
]

Prove exactly on the fixed-rank-r stratum:

[
Psi_r(M,t+Mc)=Psi_r(M,t),
]

Lorentz covariance

[
Psi_r(gMg^{-1},gt+gMg^{-1}c)
=
(Lambda^{r+1}g)Psi_r(M,t)(Lambda^rg^{-1}),
]

and completeness

[
Psi_r(M,t)=0
iff
tinoperatorname{im}M,
]

[
Psi_r(M,t)=Psi_r(M,t')
iff
t-t'inoperatorname{im}M.
]

Thus obtain a canonical coordinate embedding of (V/operatorname{im}M) without choosing a quotient basis.

## Rank-two parabolic specialization

For a nontrivial null rotation (P=e^N), certify:

[
Pi=operatorname{im}(I-P),
qquad
ell=operatorname{im}(I-P)^2,
]

[
ell=operatorname{rad}Pi=PicapPi^perp,
]

and that the projective top nonzero compound

[
[Lambda^2(I-P)]
]

determines the degenerate plane and hence its null flag.

Relate this to the repository's existing graph-closure/top-nonzero-compound machinery.

## Scope / claim fence

This is a **rank-stratified quotient coordinate/resolution diagnostic**.

It is not:

- a new action term;
- a new I-channel;
- a globally translation-invariant tensor when the rank changes;
- a replacement for the selected physical residual without a separate theorem.

Explicitly show why using (Psi_2) off the rank-two stratum can lose translation invariance.

## Terminal

`FIXED-RANK-AFFINE-COKERNEL-COMPOUND-COORDINATE-CERTIFIED`

## GitHub execution contract

Start from fresh current `main` after this registration is merged. Run lifecycle start, open a Draft PR before substantive scientific edits, keep Git-visible task state synchronized with the PR lifecycle, self-retire only at a declared terminal, refresh against current `main` before Ready, and never self-merge.

## Chat handoff

Return PR, SHA, theorem statement, rank-two null-flag corollary, relation to the old adjugate r=3 case, and the exact boundary at rank changes.
