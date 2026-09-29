> **STATUS CORRECTION — corrected normal-jet compatibility is now exact and pinned.**
>
> The historical finite TT-defect interpretation at `ea6e9d0` is superseded. The mixed metric/connection Bloch placement is
> [
> D_QE_K:lambda^{-s},qquad D_KE_Q:lambda^{+s},
> ]
> because the metric variable is attached to the face base while the connection test/input is attached to the shifted factor. The flat `z=0` control cannot detect this sign because it enters quadratically.
>
> The replacement exact checker
> `certificates/a4d_y_curved_normaljet_compatibility_check.py`
> and pinned JSON
> `certificates/a4d_y_curved_normaljet_compatibility_results.json`
> certify the full four-direction, 20-curvature geodesic-normal calculation at `z=1`.
>
> The one-direction averaged `q12` coefficient is corrected to
> [
> -186451/236250,
> ]
> with difference (-34163/118125) from the flat (-1/2) control. This residual is not physical by itself: after phase-resolved joint compatibility and allowed spatial center variations, the 20-dimensional algebraic-curvature space is cut to one physical curvature direction.
>
> Imposing only **fast-phase erasure** of the metric Euler output (smooth-source compatibility), not its value, leaves that same one-dimensional curvature direction. On it the emergent common response equals the flat Einstein control exactly. The surviving curvature operator is proportional to
> [
> -Yotimes Y,qquad Y=(1,-1,1)_{(12,13,23)}.
> ]
>
> Current smallest blocker: exact nonlinear stationary continuation of this compatible genuinely-curved normal jet, followed by a refinement-uniform (o(h^2)) response remainder. No global positive or negative task terminal is claimed yet.

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

## 3. Corrected exact finite normal-jet theorem at z = 1

The historical checker `a4d_y_curved_response_quotient_check.py` remains a regression fixture for the exact 96-by-96 Y connection Hessian, its rank data, and the bordered Lyapunov--Schmidt machinery. Its old physical TT-defect conclusion is superseded.

The corrected checker reconstructs the same finite action but rebuilds the mixed blocks with literal placement signs. It proves:

- flat connection rank (80), kernel dimension (16), and the owned half-Einstein control;
- curved (z=1) connection rank (94), center dimension (2);
- reduced center matrix
  [
  operatorname{diag}(-2500/8967,-49/356);
  ]
- corrected one-axis averaged `q12` coefficient
  [
  -186451/236250;
  ]
- 20-dimensional algebraic Riemann normal-jet input.

At the pure quadratic phase-resolved metric layer the condition matrix has rank (10) on (40) variables and does **not** restrict curvature: the kernel still projects with rank (20) to curvature space.

After adding all four slow directions, the connection Fredholm equations, phase-resolved first-slow metric equations, and spatial center gradients, the combined matrix has

[
oxed{operatorname{rank}=43,qquad dimker=5}
]

on (48) variables, while its projection to the 20-dimensional Riemann space has

[
oxed{operatorname{rank}=1}.
]

Thus full joint compatibility cuts

[
20 	ext{curvature directions}longrightarrow1.
]

The constant connection Fredholm condition is automatic on this five-dimensional kernel.

## 4. Smooth-source test without imposing Einstein

At constant slow order, do **not** set the metric Euler vector equal to the desired Einstein source. Require only that its ten components be identical on all four fast phases. This is the non-tautological smooth-source condition.

The resulting system has

[
oxed{operatorname{rank}=5,qquad dimker=2},
]

and its curvature projection still has rank one.

Only after this phase-erasure solve is complete is the common response compared with the flat control. The exact difference matrix has rank zero:

[
oxed{
E_Q^{Y,mathrm{common}}
=
E_Q^{mathrm{flat Einstein}}
}
]

on the entire smooth-source kernel.

One kernel direction carries the physical curvature; the other is a pure stationary-center freedom.

With the curvature normalized in the spatial bivector basis ((12,13,23)), the surviving curvature operator is

[
oxed{
R_{mathrm{sp}}
=
-egin{pmatrix}
1&-1&1\
-1&1&-1\
1&-1&1
end{pmatrix}
=
-Yotimes Y,
qquad Y=(1,-1,1).
}
]

The corresponding common metric-response vector in the repository ten-coordinate order
[
(q_{00},q_{01},q_{02},q_{03},q_{11},q_{12},q_{13},q_{22},q_{23},q_{33})
]
is

[
oxed{
(3/2,0,0,0,-1/2,-1,-1,-1/2,-1,-1/2),
}
]

and the independently constructed flat Einstein control is exactly the same vector.

This is a finite **normal-jet compatibility theorem**, not merely an averaged Schur coincidence.

Current finite terminal:

`A4D-Y-CURVED-NORMAL-JET-RESPONSE-COMPATIBLE`.

## 5. Reproduction

Run:

```bash
python3 02_REGISTRY/research/certificates/a4d_y_curved_normaljet_compatibility_check.py
```

The checker compares its complete invariant ledger with the pinned JSON. The historical `ea6e9d0` artifact is retained only as a regression control demonstrating why the mixed placement must be derived literally.

## 6. What this settles

The dangerous statement

> a nonzero finite Y microstructure automatically produces a different smooth macroscopic metric response

is false at the corrected compatible normal-jet level.

For a generic normal curvature direction, the (z=1) Y microstructure is already cut by phase-resolved joint compatibility. The sole linear curvature direction that survives is aligned with the same Y bivector and is Einstein-response compatible.

This is stronger than comparing two exact solutions with an already prescribed identical metric source: only phase erasure was imposed before the Einstein comparison.

The following distinctions remain binding:

- #232 remains an exact curved nongauge joint vacuum at flat metric.
- #227 remains connection-stationary but is not a joint-critical metric counterexample.
- Orth3 remains an off-shell obstruction control.
- #315/#317 remain local/algebraic resonance controls.
- the corrected finite theorem does not itself construct a nonlinear curved smooth-background exact branch.

## 7. Single remaining gate

The smallest missing result is now:

[
oxed{
	ext{exact nonlinear stationary continuation of the }-Yotimes Y
	ext{ compatible curved normal jet}
}
]

together with a refinement-uniform estimate

[
left|
E_Q(Q_h,K_h)-E_Q(Q_h,K_h^{sm})
ight|
=o(h^2).
]

A positive continuation with this remainder closes the Y microstructure threat and supplies the central response-decoupling mechanism. A negative continuation obstruction that kills the finite-amplitude Y branch on curved metrics also supports the positive Einstein route, provided shrinking-amplitude branches are controlled.

PR #310 remains Draft / IN_PROGRESS. Do not promote either global task terminal until this nonlinear gate is resolved:

- Positive: `A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED`.
- Negative: `A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO`.
