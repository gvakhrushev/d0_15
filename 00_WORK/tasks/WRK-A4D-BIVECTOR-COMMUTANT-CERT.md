# WRK-A4D-BIVECTOR-COMMUTANT-CERT

Class: `WORKER`
Parent: `CTRL-A4D-VARIATIONAL-FRONTIER`

## Objective

Create a deterministic exact-rational certificate for the local Role-bivector intertwiner count used by the active insertion research.

This worker certifies only finite linear algebra. It does not select a physical action.

## Required artifact

Create:

`02_REGISTRY/research/certificates/a4d_role_bivector_commutant_check.py`

First printed line:

`STRUCTURE_FIXED_BEFORE_NUMBER:`

Use exact rational arithmetic. A small self-contained Gaussian elimination implementation is preferred; SymPy is acceptable only if already part of the repository certificate environment.

## Fixed basis

Use Role order (A,B,C,D) corresponding to a Lorentz metric

[
eta=operatorname{diag}(1,-1,-1,-1).
]

Use ordered bivector basis

[
(AB,AC,AD,BC,BD,CD).
]

## Required positive checks

1. Build three boost and three spatial-rotation generators satisfying
   [
   X^Teta+eta X=0.
   ]

2. Build their induced (6	imes6) action on (Lambda^2V).

3. Let (T) be an unknown (6	imes6) intertwiner with 36 rational unknowns and impose
   [
   Tho_2(X_i)=ho_2(X_i)T
   ]
   for all six generators.

4. Verify exact system rank
   [
   34
   ]
   and nullity
   [
   2.
   ]

5. Exhibit a nullspace basis (I,J) with
   [
   J^2=-I.
   ]

6. Build the spacelike odd Role swap (Bleftrightarrow C). Verify it preserves (eta) and has determinant (-1).

7. Add its commutation constraint and verify exact rank
   [
   35
   ]
   and nullity
   [
   1.
   ]

8. Verify
   [
   ho_2(Bleftrightarrow C)Jho_2(Bleftrightarrow C)^{-1}=-J.
   ]

9. Print the two basis matrices and the one-dimensional survivor after the odd swap.

## Mandatory negative controls

At least three reachable FAIL modes:

- omit one boost generator and demonstrate that the centralizer can enlarge;
- replace the Lorentz boost by a non-Lorentz shear and fail the metric-preservation precheck;
- mutate one entry of (J) and fail either commutation or (J^2=-I).

A fourth control should show that testing only one or two generators is insufficient to certify the full commutant.

## Scope guard

Do not claim that the odd Role swap is a mandatory physical symmetry.
Do not call the one-dimensional result a selected gravitational action.
Do not use this certificate to promote any claim release status.
Do not introduce continuum epsilon tensors.

## Exit condition

The exact rational certificate independently reproduces:

[
36-34=2,
qquad
36-35=1,
]

identifies the Hodge-like complex structure (J), and records that the reduction to one dimension is conditional on imposing the odd Role swap.
