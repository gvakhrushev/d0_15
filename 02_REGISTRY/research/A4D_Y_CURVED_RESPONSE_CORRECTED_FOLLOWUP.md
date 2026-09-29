# A4D Y curved response — next closure gate

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`
Execution PR: #310
Status: `IN_PROGRESS` / nonlinear continuation open
Action: unchanged naked star action; no added selector or torsion equation.

## Corrected finite result

The result at `ea6e9d0` used the wrong mixed Bloch placement and its finite TT-defect interpretation is withdrawn. The corrected convention is connection equation `lambda^(-s)` and metric readout `lambda^(+s)`.

Two exact certificates are now pinned in this PR:

- `a4d_y_curved_response_phase_corrected_check.py` verifies the 10-component aggregate response for all four Bloch axes, the exact flat and curved connection ranks, the center/range equations, and a hostile swapped-phase control. Its four `q12` averages and defect ranks match the submitted corrected ledger.
- `a4d_y_curved_normaljet_compatibility_check.py` builds all 40 phase-resolved metric rows and the 20-dimensional Riemann normal-jet system. Exact ranks, kernels, curvature projection, smooth-source compatibility, and response comparison match the pinned JSON.

The normal-jet result is:

- connection ranks: flat 80, curved `z=1` 94; curved center dimension 2;
- quadratic phase system: rank 10, nullity 30, curvature projection rank 20;
- all-direction first-slow system: rank 43, nullity 5, curvature projection rank 1;
- smooth-source fast-phase-erasure system: rank 5, nullity 2, curvature projection rank 1;
- response difference from the independently built Einstein control: rank 0 on the compatible smooth-source kernel.

After normalization, the only compatible curved direction is `-Y tensor Y`, with `Y=(1,-1,1)` in spatial bivector order `(12,13,23)`. Its common response is `(3/2,0,0,0,-1/2,-1,-1,-1/2,-1,-1/2)` in metric-coordinate order `(q00,q01,q02,q03,q11,q12,q13,q22,q23,q33)`, exactly equal to the flat Einstein control.

These are finite exact normal-jet statements. They do not construct an exact branch on a curved background or prove a refinement-uniform limit.

## Exact stationary-center envelope symbol

The certificate `a4d_y_center_envelope_symbol_check.py` computes the principal quadratic symbol of the two center amplitudes at `z=1`. They decouple and give

`S_Y(t) = -2/188307 * [26250*(t0-16*s/75)^2 - (2283779/2)*r_perp^2]`

and

`S_dual(t) = -1/6408 * [882*(t0-16*s/21)^2 - (603687/2)*r_perp^2]`,

where `s=t1+t2+t3` and `r_perp^2=t1^2+t2^2+t3^2-s^2/3`. These are two transported `2+1` hyperbolic envelope modes; there is no elliptic spectral gap. This is only the quadratic principal symbol. It does not prove nonlinear envelope existence or an energy estimate.

The exact dual-center visibility check gives a second boundary at zero slow momentum: its finite Cayley path has zero connection Euler on all 96 rows, while its metric response alternates sign between the first and second phase pairs. The four-phase average vanishes, but requiring the metric Euler output to be equal on all four phases forces the dual amplitude to zero near the origin.

The small-amplitude Schur certificate starts from the 16-dimensional flat connection kernel and gives effective ranks `(0,0,12,12,14,14,14)` through order six. After the order-two reduction, four directions remain; the order-four and order-five reduced blocks vanish, and the order-six block is `diag(0,0,9/8,3/8)`. Thus twelve transverse directions first lift at order two, two soft transverse directions at order six, and two exact center directions remain. The worst inverse loss is `O(z^-6)`, so this finite splitting does not supply the uniform estimate needed for the continuum limit.

## Site-resolved source response on the `t0/t1` compatible class

The certificate `a4d_y_phase_resolved_compatible_response_check.py` independently builds the four-phase, 40-component metric source space at `z=1` for the `e0` axis. Its first two exact Fredholm conditions have ranks 1 and 2, leaving a 37-dimensional source class. The second-order averaged response defect has rank 8 on that class. The averaged first-order response has rank 4 there, although it vanishes on the ten-dimensional phase-independent source subspace. On that phase-independent subspace, the single-source defect has rank 6 and its `q12` coefficient is `-34163/118125`, matching the corrected four-axis certificate.

For a 10-by-40 matrix on all source coordinates, the checker explicitly extends the restricted defect by the Euclidean orthogonal projection onto the compatible class. This convention gives rank 8 and kernel dimension 32; the stationary response itself is only defined on the compatible class. This source-response calculation is distinct from the curvature normal-jet system above, which also imposes spatial center-gradient and fast-phase-erasure equations. It does not change that system's exact Einstein response on its surviving curvature direction.

The submitted scalar `2626083/44800` is not adopted: the supplied JSON does not identify the source vector or projection defining that `q12` value, and it is not the phase-independent `q12` coefficient under the pinned convention.

## Leading-order phase-independent source and curvature witness

The certificate `a4d_y_singleq_curvature_witness_check.py` independently verifies the latest consolidated single-source result. For one metric `q` shared across the four phases, both the curved order-zero and order-one connection cokernel maps have rank zero; the flat controls also have rank zero. The `q12` source excites the two center amplitudes by `(-3311/3750, 0)`, and its corrected second-order defect has rank 6 with `q12` coefficient `-34163/118125`.

The same checker verifies the supplied 10-by-10 normal-jet matrix as an element of the 20-dimensional algebraic Riemann-jet image. Its Frobenius pairing with the single-source defect is exactly `-27247/17500`. Six generators in the checker’s deterministic Riemann basis have nonzero pairings; that count depends on basis choice, while the explicit matrix and its nonzero pairing do not. This is a finite witness for the single-axis response map. It has not been shown to satisfy the full coupled slow-center and fast-phase-erasure system; the separate full normal-jet certificate still leaves only `-Y tensor Y` and matches Einstein on that surviving direction.

The latest submitted report also states that a defect map over all 20 Riemann jets has rank 4. The supplied JSON contains the explicit witness and its scalar pairing, but not the full response-by-curvature matrix or a replayable rank certificate. The six nonzero entries recorded above are pairings against one pinned basis and are not a matrix-rank result. Keep the rank-4 statement unverified until that map is supplied and independently replayed; it is distinct from the certified rank-6 single-q metric defect and the rank-1 curvature projection in the fully compatible normal-jet system.

## Reproduction

From the repository root:

```bash
python3 02_REGISTRY/research/certificates/a4d_y_curved_response_phase_corrected_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_normaljet_compatibility_check.py
python3 02_REGISTRY/research/certificates/a4d_y_dual_center_joint_visibility_check.py
python3 02_REGISTRY/research/certificates/a4d_y_center_envelope_symbol_check.py
python3 02_REGISTRY/research/certificates/a4d_y_small_amplitude_kernel_splitting_check.py
python3 02_REGISTRY/research/certificates/a4d_y_phase_resolved_compatible_response_check.py
python3 02_REGISTRY/research/certificates/a4d_y_singleq_curvature_witness_check.py
```

The first checker also records the submitted report JSON as provenance; it cross-checks its aggregate four-axis fields, not the report's per-site `q12` arrays. The normal-jet checker owns the full curvature compatibility theorem. The dual-center and center-symbol checks distinguish the staggered flat mode from the two hyperbolic principal forms. The small-amplitude checker certifies the zero-momentum splitting through order six. The phase-resolved source-response checker verifies the 37-dimensional `t0/t1` compatible class. The single-source witness checker verifies the corrected phase-independent defect and its explicit algebraic curvature pairing; neither is a nonlinear continuation result.

## Remaining target: nonlinear continuation

Derive and control the nonlinear equations for the two center envelopes, then continue the surviving curved normal jet `J` to an exact stationary branch

`K_h(J) = K_Y + a_h(J)`

over sampled smooth metrics `Q_h(J)` with `q(0)=0`, `partial q(0)=0`, and `partial^2 q(0)=J`. Solve the literal finite connection Euler equation `E_K(Q_h,K_h)=0`, retaining the center variables and imposing the full cokernel equations at every order.

Acceptable proof routes include analytic Lyapunov–Schmidt/Kuranishi continuation with a convergent majorant, Newton–Kantorovich on a certified range complement plus exact reduced hyperbolic center estimates, or another finite-dimensional analytic continuation with constants tracked in `h`. The continuation radius must support the background scaling, and omitted orders must be controlled. An elliptic inverse or elliptic spectral-gap estimate cannot be assumed for the center symbol.

The branch must then satisfy the owner-topology estimate

`|E_Q(Q_h,K_h) - E_Q(Q_h,K_h^sm)| = o(h^2)`

uniformly under refinement. Control near-resonant complements, the allowed stationary-center amplitudes, conjugate Bloch-sector interactions, and the declared compact set of smooth background parameters.

If continuation fails, return the first exact reduced center or cokernel equation that fails, its rational/polynomial obstruction, the surviving nonlinear curvature variety, and whether the obstruction forces the Y amplitude to shrink with `h`. A finite normal-jet compatibility result is not itself a nonlinear failure.

## Selector and terminal rules

Do not claim a selector is required unless two exact source-compatible stationary branches over the same admissible smooth background have different normalized metric responses. The corrected finite normal-jet response agrees with Einstein on its compatible direction.

Keep PR #310 Draft and the lifecycle `IN_PROGRESS` until the nonlinear continuation and uniform remainder are proved or refuted. Neither global task terminal has been reached:

- Positive: `A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED`.
- Negative: `A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO`.
