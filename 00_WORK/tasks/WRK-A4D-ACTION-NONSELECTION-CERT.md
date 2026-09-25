# WRK-A4D-ACTION-NONSELECTION-CERT

Class: `WORKER`
Parent: `CTRL-A4D-VARIATIONAL-FRONTIER`

## Objective

Extract the finite countermodel and Green witness from
`MEMO_A4D_CURVATURE_ACTION_GRAVITY_GATE.md`
into a deterministic exact-arithmetic research certificate.

This worker certifies the **nonselection witness**, not gravity.

## Required artifact

Create:

`02_REGISTRY/research/certificates/a4d_action_nonselection_l3_check.py`

The first printed line must begin with:

`STRUCTURE_FIXED_BEFORE_NUMBER:`

Use Python standard library exact rational arithmetic.

## Required positive checks

On `(Z/3)^2`:

1. construct the forward-difference matrices `D1,D2`;
2. construct curl matrix `C=(-D2 D1)`;
3. verify `rank(C)=8`;
4. verify
   [
   spec(K_A)={0^{10},3^4,6^4};
   ]
5. verify
   [
   spec(K_B)={0^{10},12^4,42^4};
   ]
6. verify the two physical spectra are not related by one overall rescaling;
7. split the 10 zero modes as 8 gauge + 2 harmonic;
8. verify
   [
   G=(7Delta-Delta^2)/36,quad
   Delta G=I-mathbf1mathbf1^T/9,quad Gmathbf1=0;
   ]
9. verify the stated nearest/diagonal source-potential differences.

## Mandatory negative controls

Reachable `FAIL_*` mutations must include:

- replacing `I+Delta` by a scalar multiple of identity, destroying the inequivalent spectral shape witness;
- perturbing one Green coefficient so the pseudoinverse identity fails.

A third control should demonstrate that a site-local constant constitutive Hessian has momentum-independent symbol and therefore cannot be silently identified with the curl-derived operator.

## Scope guard

Do not identify the SO(2) witness with the physical D0 gravity carrier.
Do not call the conditional scalar reduction Newtonian gravity.
Do not add fitted coefficients.
Do not alter existing claim status.

## Exit condition

One exact finite checker reproduces the inequivalent L=3 Hessian spectra, gauge/harmonic count and Green identity with reachable negative controls, establishing a durable regression witness for action nonselection without physical overclaim.
