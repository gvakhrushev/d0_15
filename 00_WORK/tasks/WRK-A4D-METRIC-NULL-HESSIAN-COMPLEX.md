# WRK-A4D-METRIC-NULL-HESSIAN-COMPLEX

Class: `WORKER`
State on registration: `PLANNED`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Research lane: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-metric-null-hessian-complex`
Primary artifact: `02_REGISTRY/research/A4D_METRIC_NULL_HESSIAN_COMPLEX.md`
Execution: `GitHub-first`

## Why delegated

FUGU forward scouts found a universal two-real-dimensional metric-only block and a nonzero raw character-detune residual. The current interpretation is unsafe because a character change moves the carrier itself. This bounded worker must decide the exact symbol geometry before #240 or #237 consume the scout as a physical response.

## Objective

Using the accepted polarized star metric-response symbol `C(z)=H_AQ(z)`, set
`d_r=z_r^{-1}-1` and determine the exact metric-only kernel for arbitrary nontrivial character.

The worker must distinguish:
- a fixed-vector derivative `(D_j C)q`;
- transport of the kernel section itself;
- the forward-coframe metric shadow built from `a_r=z_r-1`;
- physical conjugate-paired realification.

## Required gates

1. Rebuild the exact `24 x 10` metric-response symbol from the accepted star conventions.
2. Prove the identity `C(z) vec_sym(d d^T)=0` symbolically.
3. On a projective cover of `d != 0`, prove `rank C=9` and
   `ker C = span{vec_sym(d d^T)}`; record the trivial-character exception.
4. Differentiate the exact identity with `D_j=z_j d/dz_j` and certify
   `(D_j C)q = -C(D_j q)` for all four character directions.
5. Reproduce the nine L4 orbit representatives as a hostile control and show
   every one of the 36 raw FUGU detune vectors lies in `im C`.
6. Compare the null line with the flat forward-coframe metric image:
   `a=z-1`, `d=z^{-1}-1`. Classify exact alignment on the nine owned L4
   singular orbit types without calling the affine image gauge.
7. Record the smooth-character expansion `z=e^{ihk}`: the backward-null
   metric tensor and the forward-coframe scalar metric shadow agree at order
   `h^2` and differ first at `O(h^3)`; after `h^{-2}` normalization the
   mismatch is `O(h)`.
8. State consequences for #240/#237/#264 and the FUGU v2-v4 interpretation.
   Keep the #232 connection family separate from this metric null line.

## Preferred terminal

`J2-METRIC-NULL-HESSIAN-COMPLEX-EXACT`

A narrower terminal is acceptable if global rank-9 exactness fails on a named nonzero stratum.

## Forbidden

No new action term, no `varphi`, no BOOK/claim promotion, no declaration of full diffeomorphism gauge, no identification with `E_eta/E_sp`, and no use of the FUGU numerical SVD as theorem evidence.

## GitHub execution contract

Open the Draft PR before substantive science commits. Produce an exact certificate under
`02_REGISTRY/research/certificates/`, self-retire only after the exact terminal is reached, and do not self-merge.

## Chat handoff

Return the PR link, head SHA, exact terminal, the closed-form null generator `q=d d^T`, the projective rank-9 proof summary, the 36/36 detune-transport verdict, the L4 affine-alignment orbit list, and the exact certificate command. State explicitly that the result is a metric-symbol complex, not a full diffeomorphism-gauge theorem.
