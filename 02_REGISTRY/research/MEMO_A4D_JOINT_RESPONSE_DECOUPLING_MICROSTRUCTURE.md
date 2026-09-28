> **STATUS CORRECTION — supersedes the finite-defect interpretation at ea6e9d0.**
>
> A follow-up literal-pairing audit found that the mixed metric/connection Bloch phase in the ea6e9d0 response assembly did not follow the same test-variable placement convention as the connection block. The flat z=0 control did not detect this because the sign enters quadratically there. Therefore the exported z=1 TT defect at ea6e9d0 must **not** be used as an on-shell or physical response obstruction.
>
> After correcting that phase convention in the follow-up calculation, a phase-resolved metric Euler term appears already at first slow order and vanishes only after four-phase averaging. Solving the full normal-jet compatibility problem, rather than the one-direction ansatz, removes most of these apparent defects. In the reported 20-component geodesic-normal curvature test, the linear compatibility system leaves one physical compatible curvature component; on that surviving component the corrected response agrees exactly with the flat Einstein control.
>
> The corrected replay/certificate for this follow-up result is **not yet present in this branch**. Until it is committed and independently replayed, treat the preceding paragraph as a reviewed execution result awaiting repository certification, not as a registered theorem.
>
> Consequently the task terminal remains OPEN. The smallest live blocker is now: construct the exact nonlinear stationary branch from the compatible genuinely-curved normal jet and prove a refinement-uniform remainder estimate strong enough that the h^-2-normalized response converges to the Einstein value; or produce a corrected on-shell compatible curvature direction with a persistent exact response defect.

# A4D joint response decoupling — stationary-center quotient

Task: EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE
Execution: PR #310
Lifecycle: IN_PROGRESS; PR remains Draft
Action and scope: unchanged naked star action; no selector, torsion equation, spectral filter, or added action term.

## 0. Pinned inputs

These inputs were rechecked against the current main line on 2026-09-29. The listed merge commit is the exact integrated version consumed by this execution.

| Input | State | Merge commit |
|---|---|---|
| #216 smooth J2 resonance and comparator | MERGED | 5523d8f679c1ea02f9b73d757c81649740010d0a |
| #223 normal-coordinate locality | MERGED | 25de48600cbc7c06e233d7b8f886f89566bdd6a4 |
| #226 metric-response sensitivity | MERGED | 4b145afe33b2fb7381615199167608b71457d01d |
| #227 curved connection-stationary control | MERGED | 245095f941a047dec95877ef03996742f37cb429 |
| #232 exact curved nongauge Y joint vacuum | MERGED | caa1e65087ddf15cda35325189ebfcbf51a56592 |
| #237 post-no-go gravity synthesis | MERGED | 7d7ad1ba561dc1fb1d726ea54307679f09e0dd88 |
| #275 exact Y slow stationary lift | MERGED | ad61743e5be3de25ac987a912e497d26fd531271 |

## 1. Typed target and comparison convention

At fixed connection, the finite metric Euler response is the vector E_Q(Q,K) in the direct sum over sites of Sym²((R⁴)*), with ten symmetric Gram coordinates per site. The physical normalization is applied after evaluation: R_h(Q,K) = h^-2 E_Q(Q,K).

For refinement statements, the owner sum norm from #226 is the default: sum over sites and symmetric Gram components of the absolute value. Any continuum claim must name its testing topology and justify the reconstruction map into it.

The designated comparator is the #216 smooth branch evaluated on the same sampled smooth metric Q_h. The source convention must be stated with every result. Comparing two exact solutions of the identical prescribed metric-source equation makes their response difference zero by substitution; that is only a tautological control.

The task target remains the normalized response difference
D_h(K_h) = h^-2 [ E_Q(Q_h,K_h) - E_Q(Q_h,K_h^sm) ]
for the declared exact joint-critical class, including the curved nongauge microstructure in #232.

## 2. Why the stationary center is the right object

The exact #232 period-four Y family satisfies E_K(eta,K_Y(z)) = 0 and E_Q(eta,K_Y(z)) = 0. For nonzero z it has nonzero plaquette curvature and is nongauge. Thus a universal estimate forcing every zero-residual connection into one smooth/LC-like fiber cannot cover this family.

Separate the stationary center from transverse range directions. Normal rescue may still control the range. Along the center, the relevant question is whether the metric response is constant on the physical stationary fiber.

The decisive finite test is the slow Bloch metric symbol around a genuinely curved point of the Y branch, with a Lyapunov–Schmidt reduction at the singular zero-momentum connection Hessian. No inverse of that singular Hessian is used.

## 3. Exact finite-cell response at z = 1

The certificate a4d_y_curved_response_quotient_check.py reconstructs the full 96 by 96 connection Hessian from the four oriented face factors using exact rational arithmetic.

At z = 0, the reconstructed Hessian equals the owned #275 matrix L2/2 entry by entry. Its exact rank is 80 and its kernel has dimension 16. This is the flat assembly control.

At z = 1, the Hessian has two independent exact null vectors: the right-log Y tangent and the phase-0/2 boost-dual direction. Clearing denominators by 14 and reducing modulo 1,000,003 gives rank at least 94; the two exact null vectors give rank at most 94. Hence the rational rank is exactly 94 and the center dimension is exactly two.

For Bloch modulation in role direction e0, set lambda = exp(t) and use one low-color metric perturbation q shared across the four phases. The exact reduced center matrix at order t² is diagonal with entries -2500/8967 and -49/356, so it is nondegenerate. The left-center compatibility conditions at orders zero and one vanish exactly. The connection range and center corrections are solved with a bordered exact system, and the certificate checks the full range equations and the reduced center equation with zero residual. The JSON exports the exact right-kernel columns, left-cokernel rows, and the 96-entry q12 range-correction witnesses at orders t⁰ and t¹.

The flat control reproduces the owned Einstein symbol: the coefficient of t² per site agrees entry by entry with one half of the linearized Einstein symbol in the repository Gram convention. Since t = i k0, this is the required negative one-half Einstein coefficient in physical k0².

At z = 1 the transverse-traceless q12 component for momentum e0 has these exact coefficients per site:

| Quantity | Coefficient of t² |
|---|---:|
| Flat Einstein control | -1/2 |
| Curved Y branch, z = 1 | 38218/13125 |
| Difference, curved minus flat | 89561/26250 |

The full TT subspace for momentum e0 is spanned by q12 and q13. Its exact per-site defect matrix is [[89561/26250, -92753/52500], [-92753/52500, 89561/26250]], with determinant 2504701/294000, so the response mismatch survives the linearized diffeomorphism quotient. The q12 diagonal witness is already nonzero by itself. In physical k0² the matrix sign is reversed. The discrepancy is an exact rational Hessian/Schur response defect, not a floating-point or rank-threshold artifact.

Two independent exact Schur evaluations at lambda = 1 + 1/20 and 1 + 1/100 converge toward the computed quadratic coefficient, with the latter error smaller. They are corroborating finite controls; the Lyapunov–Schmidt coefficient calculation is the exact derivation.

## 4. Reproduction

Run:

    python3 02_REGISTRY/research/certificates/a4d_y_curved_response_quotient_check.py

The script checks the flat owner match, exact flat and curved ranks, center vectors, Fredholm compatibility, nondegenerate reduced center matrix, exact range solves, Einstein control, TT non-gauge defect, direct-lambda convergence, and a hostile wrong-phase-transpose control that fails. It also compares its result with the pinned JSON. The certified finite-cell terminal is:

    A4D-Y-CURVED-RESPONSE-QUOTIENT-OBSTRUCTED-AT-Z1-TT

The JSON records the full 10 by 10 flat and curved t² matrices, center matrix, rank evidence, exact TT defect, and the finite scope.

## 5. What this settles and what it does not

The coefficient identity S_z^[2] = S_0^[2] fails at the curved #232 vacuum z = 1 in a physical TT component. Therefore the proposed finite stationary-center response-equivalence identity is false in this tested direction. This is a concrete response-quotient obstruction at the Hessian level.

It does not yet close #310 negatively. The task requires an actual smooth-background, source-compatible exact joint-critical sequence in the genuine Lorentz quotient whose normalized response gap has a nonzero limit or liminf. A Hessian defect at one curved vacuum is not that nonlinear sequence. It also does not prove global homogenization failure for every source convention or every physical branch.

The following distinctions remain binding:

- #232 is an exact curved nongauge joint vacuum at the flat metric and has zero metric response there.
- #227 is curved and connection-stationary with nonzero metric response, but is not a joint-critical metric counterexample.
- #275 supplies an exact slow off-shell coefficient, not an on-shell response residue.
- #317 and #315 are algebraic character and local Smith controls, not nonlinear stationary-response theorems.
- An identical-source comparison between two exact solutions is tautological.

## 6. Single remaining gate

The smallest missing result is a uniform nonlinear Lyapunov–Schmidt continuation of the z = 1 Y stationary center over a genuinely curved sampled smooth metric, with the declared #216 comparator and source convention, and with a remainder that is o(1) after the h^-2 normalization. The exact TT Hessian defect supplies the candidate nonzero response gap; the continuation must show that it persists on an exact source-compatible joint-critical sequence.

Until that continuation is proved or refuted, keep PR #310 Draft and Lifecycle IN_PROGRESS. Do not promote the finite certificate to either task terminal:

- Positive: A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED.
- Negative: A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO.
