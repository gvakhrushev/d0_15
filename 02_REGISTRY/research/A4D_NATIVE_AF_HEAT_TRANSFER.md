# SOURCE #310: native AF heat-factor transfer and complete archive source

14 October 2026. RESEARCH; original parent remains Draft / IN_PROGRESS.
Scientific input: `25bf1db4876c20223f2dbaeb1cbe1105039cf7a1`.

[Full proof, Russian](sources/d0_native_af_heat_transfer_v7_2026-10-14/NATIVE_AF_HEAT_TRANSFER_RU.md)
[Exact replay](sources/d0_native_af_heat_transfer_v7_2026-10-14/af_heat_check.py)
[Immutable receipt](sources/d0_native_af_heat_transfer_v7_2026-10-14/af_heat_receipt.json)

The existing PF adjoint `C_n(Z,W)=(pX+p^2W,Y)` is not the full ordinary
GNS-operator trace reduction. Trace duality forces the central correction
`R_n=w_n^-1 C_n(w_(n+1) .)` and the literal formula
`R_n(Z,W)=(((a+b)X+aW)/a, ((a+b)/b)Y)`. No tensor cut or free coefficient
is introduced. This does not replace the correct PF adjoint in kinematics.

On the full fine GNS space, old-block multiplicities are
`M_phi^(2(N-n))(a_n,b_n)=(a_(2N-n),b_(2N-n))`. The reductions compose
exactly. The positive heat factor, not its logarithm, transfers linearly;
full heat-plus-matter price and its archive remainder telescope with their
actual noncommuting, moving-state first derivatives.

The literal native residual `I-JJ*` gives a full five-state control:
`M_0=(2,3/2)`, partition `7/2`, full source `-3/7` at beta=log2 and unit
gap. The cyclic preparation has the necessary archive derivative
`-(p+2)/6`. All new modes remain. At this commutant reference the full
first-response map is unital CP with operator norm one, including
noncommuting perturbations. No such positivity is inferred for general
interacting operators; the v6 counterexample remains valid.

The exact fixed-old-algebra counting-to-PF error is
`a_n b_n p^(2n+2r+3)/d_(n+r)`, hence order `phi^(-4r)` at fixed n.
The bounded-width inherited Gibbs source satisfies the explicit corresponding
operator-norm bound. This is not a continuum theorem for arbitrary fine heat.

Verification: 304 exact conditions including seven negative controls;
five executed mathematical mutations and a false-GR receipt are rejected.
Independent complex Frechet and moving-state tests are labelled floating-point,
not interval proofs. Normal and optimized exact replays pass. No Lean compilation.

The actual physical full generator, field-to-operator map, changing-algebra
terms, pi0 placement, common H+J+R, physical Ward, curved roots and GR remain
open. The result replaces the arbitrary tensor-cut input of v6 on the
specified real native AF representation; it does not identify that representation
with all physical cochains or declare a total physical action selected.
Existing owners, claims, tasks and CONTROL snapshots are unchanged.

Run `python 02_REGISTRY/research/certificates/a4d_native_af_heat_transfer_check.py`.
