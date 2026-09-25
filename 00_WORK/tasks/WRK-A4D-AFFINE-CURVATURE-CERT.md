# WRK-A4D-AFFINE-CURVATURE-CERT

Class: `WORKER`
Parent: `CTRL-A4D-VARIATIONAL-FRONTIER`

## Objective

Turn the exact finite curvature results of
`MEMO_A4D_MIXED_LETTER_PLAQUETTE_CURVATURE.md`
into a deterministic executable research regression certificate.

This is a Python/exact-arithmetic worker. Lean is not required.

## Required artifact

Create:

`02_REGISTRY/research/certificates/a4d_affine_curvature_packet_check.py`

The first printed line must begin with:

`STRUCTURE_FIXED_BEFORE_NUMBER:`

## Required positive checks

1. exact semidirect multiplication and inverse;
2. exact affine square formula
   [
   P_{rs}=T_{Theta_{rs}}ho(Lambda_{rs});
   ]
3. pure-translation reduction `L=I => Lambda=I, Theta=d1 b`;
4. noncommuting rational linear-link witness with `Lambda != I`;
5. shared-F mixed plaquette reduction to `F T_Omega F^-1`;
6. pure shared-F even flatness at `kappa=0`;
7. frame-image bridge `F=rho(E)` gives `Lambda=I`;
8. ordered cube/Bianchi word identity on a finite hostile model;
9. trace blindness of the degree-raising translation block.

## Mandatory negative controls

At least two reachable `FAIL_*` mutations, including:

- wrong corner/shift in the affine `Theta` formula;
- illegal ordinary `dTheta=0` replacement for the nonlinear semidirect cube law.

The checker must fail under those mutations and pass only with the exact ordered formula.

## Scope guard

Do not claim continuum Riemann curvature or Cartan torsion.
Do not add a new 2-cocycle.
Do not change claim release status.
Do not formalize the full memo in Lean.

## Exit condition

The exact affine/mixed plaquette formulas, ordered cube identity and trace-blindness boundary are reproducibly checked by exact finite arithmetic with reachable negative mutations, and the memo links the checker without any claim-status promotion.
