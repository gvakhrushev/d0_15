# A4D joint response decoupling — corrected Y normal-jet result

> **Finite normal-jet compatibility is certified; the nonlinear continuum gate remains open.**
>
> The physical TT-defect interpretation at `ea6e9d0` is superseded. Its mixed metric/connection Bloch placement was swapped. The corrected convention is connection-side `lambda^(-s)` and metric-readout `lambda^(+s)`, derived from the actual face-base and shifted-link placement. The flat `z=0` control could not detect the sign error.
>
> The corrected four-direction, 20-curvature normal-jet certificate now passes exactly. Full joint compatibility leaves one curved spatial direction, and imposing only fast-phase erasure makes its common metric response equal the independently constructed flat Einstein response. This is a finite normal-jet theorem, not a nonlinear or refinement-uniform theorem.

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`
Execution: PR #310
Lifecycle: `IN_PROGRESS`; PR remains Draft
Action: unchanged naked star action; no selector, torsion equation, spectral filter, or added term.

## Inputs and response convention

The calculation consumes merged #216, #223, #226, #227, #232, #237, and #275. The exact merge commits are pinned in the execution history and task brief.

The target is the normalized response difference

`D_h(K_h) = h^-2 [E_Q(Q_h,K_h) - E_Q(Q_h,K_h^sm)]`

for exact joint-critical sequences, with the #216 smooth branch evaluated on the same sampled smooth metric. The owner sum norm from #226 is the default for refinement claims. Comparing two exact solutions to the identical prescribed metric source is tautological and is not the source condition used below.

The exact #232 period-four Y family is a curved nongauge joint vacuum at the flat metric. It rules out a universal claim that every zero-residual connection lies in one smooth/LC-like fiber. The response question is whether its stationary center can remain compatible with a genuinely curved metric background.

## Corrected finite response across the four Bloch axes

`a4d_y_curved_response_phase_corrected_check.py` independently reconstructs the 96-by-96 connection Hessian and the 10-component low-color response with the corrected mixed phase convention. It verifies the submitted aggregate ledger in `a4d_y_curved_response_corrected_report.json` and writes `a4d_y_curved_response_phase_corrected_results.json`.

At `z=0`, the Hessian matches the owned #275 `L2/2` entry by entry, has rank 80 and kernel dimension 16, and reproduces the half-Einstein symbol on all four axes. At `z=1`, it has rank 94 and a two-dimensional center. The exact range and center equations pass for all four Bloch axes; the reduced center determinant for `e0` is `625/16287`.

For the 10-component metric perturbation shared across the four phases, the exact aggregate `q12` coefficients are:

| Bloch axis | Curved `q12` coefficient | Difference from flat | Rank of 10-by-10 defect |
|---|---:|---:|---:|
| `e0` | `-186451/236250` | `-34163/118125` | 6 |
| `e1` | `-2665927/85127280` | `-2665927/85127280` | 8 |
| `e2` | `-2665927/85127280` | `-2665927/85127280` | 8 |
| `e3` | `177811967/340509120` | `7557407/340509120` | 8 |

The averaged first-order response is zero in this ten-component reduction. The per-site `q12` arrays from the submitted JSON are retained for provenance, but this four-axis checker cross-checks only the aggregate fields. The separate normal-jet checker below supplies the phase-resolved compatibility calculation used for the finite theorem.

## Exact phase-resolved normal-jet compatibility at `z=1`

`a4d_y_curved_normaljet_compatibility_check.py` builds the 40-row phase-resolved metric equations and all four slow directions, then checks the exact ledger in `a4d_y_curved_normaljet_compatibility_results.json`.

The algebraic Riemann normal-jet space has dimension 20. The pure quadratic phase-resolved system has rank 10 on 40 variables; its kernel still projects onto all 20 curvature directions. After adding the four slow directions, connection Fredholm equations, phase-resolved first-slow metric equations, and spatial center gradients, the combined system has rank 43, nullity 5 on 48 variables, and curvature projection rank 1. The constant-order connection Fredholm condition is automatic on that kernel.

Impose only fast-phase erasure of the metric Euler output: the ten components must agree across all four fast phases, without prescribing their common value. This smooth-source system has rank 5, nullity 2, and still projects onto one curved direction. Only after solving these compatibility equations is the response compared with Einstein. The exact response difference has rank zero on the full smooth-source kernel.

With spatial bivector basis `(12,13,23)`, the surviving curvature operator, after the declared normalization, is

`-Y tensor Y`, where `Y=(1,-1,1)`.

The common metric response in coordinate order `(q00,q01,q02,q03,q11,q12,q13,q22,q23,q33)` is

`(3/2, 0, 0, 0, -1/2, -1, -1, -1/2, -1, -1/2)`.

The independently assembled flat Einstein control is exactly the same vector. The finite terminal is `A4D-Y-CURVED-NORMAL-JET-RESPONSE-COMPATIBLE`.

## Nonlinear status of the second connection-center mode

The exact checker `a4d_y_dual_center_joint_visibility_check.py` integrates the boost-dual connection-kernel tangent to a finite Cayley path at the `z=1` flat Y vacuum. All 96 connection Euler rows vanish identically on this path. Its ten Gram-response components are

`(0,0,0,0,-f,f,f,-f,f,-f)`

on fast phases 0 and 1, and the negative vector on phases 2 and 3, where `f=4d/(3d^2-4)`. The four-phase average is zero, but a smooth source requires fast-phase erasure and forces `d=0` near the origin. Thus the second connection-Hessian center is not an independent smooth-source joint modulus: it is connection-stationary and staggered-metric-visible.

## Quadratic symbol of the surviving center envelopes

The follow-up certificate `a4d_y_center_envelope_symbol_check.py` computes the exact quadratic symbol of the two-dimensional stationary center at `z=1`. The two components decouple at principal order. With `s=t1+t2+t3` and `r_perp^2=t1^2+t2^2+t3^2-s^2/3`, their symbols are

`S_Y(t) = -2/188307 * [26250*(t0-16*s/75)^2 - (2283779/2)*r_perp^2]`

and

`S_dual(t) = -1/6408 * [882*(t0-16*s/21)^2 - (603687/2)*r_perp^2]`.

These are two transported `2+1` hyperbolic envelope modes, not an elliptic range with a spectral gap. The exact symbol fixes the linear principal part only; nonlinear envelope existence, energy estimates, and uniform coupling to the transverse range remain open.

## Small-amplitude splitting at zero slow momentum

The exact checker `a4d_y_small_amplitude_kernel_splitting_check.py` reduces the flat 16-dimensional connection kernel twice. The effective ranks through order six are `(0,0,12,12,14,14,14)`. After the order-two block, four directions remain; the reduced order-four and order-five blocks vanish, while the order-six block is `diag(0,0,9/8,3/8)`. The final kernel consists of the exact Y and boost-dual center tangents. Twelve transverse modes lift at order two, two soft modes at order six, and the worst inverse loss is `O(z^-6)`. This exact zero-momentum splitting identifies the small-amplitude conditioning that a nonlinear uniform estimate must control; it is not itself an `h`-uniform continuation theorem.

## Site-resolved source response on a 37-dimensional compatibility class

The follow-up certificate `a4d_y_phase_resolved_compatible_response_check.py` builds the 40-dimensional, four-phase metric-source problem for the `e0` axis at `z=1`. The exact zero-order and first-order Fredholm maps have ranks 1 and 2, so their common kernel has dimension 37. Solving the range and two center equations through second order gives a defect of rank 8 on this class. Its averaged first-order response has rank 4 on the full class but vanishes on the phase-independent ten-dimensional source subspace. The phase-independent second-order defect has rank 6 and reproduces the previously pinned `q12` value `-34163/118125`.

The 10-by-40 defect matrix extends the map from the compatible class by Euclidean orthogonal projection; the checker states this convention explicitly. It is a finite source-response calculation, separate from the curvature normal-jet system, and does not alter the latter's Einstein match after spatial center-gradient and fast-phase-erasure constraints. The submitted value `2626083/44800` lacks a specified source vector/projection in the provided package and is not treated as verified.

## Reproduction

From the repository root, run:

```bash
python3 02_REGISTRY/research/certificates/a4d_y_curved_response_phase_corrected_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_normaljet_compatibility_check.py
python3 02_REGISTRY/research/certificates/a4d_y_dual_center_joint_visibility_check.py
python3 02_REGISTRY/research/certificates/a4d_y_center_envelope_symbol_check.py
python3 02_REGISTRY/research/certificates/a4d_y_small_amplitude_kernel_splitting_check.py
python3 02_REGISTRY/research/certificates/a4d_y_phase_resolved_compatible_response_check.py
```

The first command verifies the four-axis aggregate, exact center/range solves, three direct rational Schur controls, and a hostile swapped-phase control. The second verifies curvature normal-jet compatibility and Einstein response. The next three verify dual-center source visibility, the hyperbolic center symbol, and the zero-momentum small-amplitude splitting. The final command verifies the 37-dimensional site-resolved source-response class and its projected defect map. Each checker compares its result with a pinned JSON. The old `a4d_y_curved_response_quotient_check.py` and its output remain historical regression material; its `ea6e9d0` TT-defect interpretation must not be used.

The submitted aggregate JSON has SHA-256 `79e6db7d96a0863a6af56e94752d080d5505a7fc47a307b752269dd092c4e230`. Its per-site `q12` arrays are not separately asserted by the aggregate checker.

## What is and is not settled

The finite claim that a nonzero Y microstructure necessarily induces a different smooth metric response is false on the corrected compatible normal-jet subspace: its sole curved linear direction has the Einstein response after phase erasure. This is stronger than comparing two solutions with an already prescribed common source.

The following boundaries remain:

- #232 is still a curved nongauge joint vacuum at the flat metric.
- #227 is connection-stationary but is not a joint-critical metric counterexample.
- The corrected normal-jet certificate is finite and linear in the sampled curvature jet.
- No exact nonlinear stationary branch over a genuinely curved sampled metric is constructed here.
- No refinement-uniform `o(h^2)` response remainder is proved here.
- No global selector or task-level no-go is established.

## Single remaining gate

Derive the nonlinear reduced equations for the two compatible center envelopes and continue the `-Y tensor Y` curved normal jet to an exact stationary branch with the declared #216 comparator, or prove an exact obstruction in those reduced equations. The continuation must control the hyperbolic principal symbols without assuming an elliptic spectral gap. Then prove the refinement-uniform estimate

`|E_Q(Q_h,K_h) - E_Q(Q_h,K_h^sm)| = o(h^2)`

in the owner topology, including almost-resonant complements and the allowed stationary-center amplitudes. A finite jet theorem alone does not close the task.

Keep PR #310 Draft and the task `IN_PROGRESS` until the nonlinear continuation and uniform remainder are proved or refuted. Do not claim either global terminal:

- Positive: `A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED`.
- Negative: `A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO`.
