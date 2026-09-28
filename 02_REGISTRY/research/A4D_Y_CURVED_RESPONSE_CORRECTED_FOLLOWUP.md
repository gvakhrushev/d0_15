# A4D Y CURVED RESPONSE — CORRECTED FOLLOW-UP CLOSURE BRIEF

Task: EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE
Execution PR: #310
Status: IN_PROGRESS / correction lane
Scientific scope: naked star action unchanged; no added selector or torsion equation.

## 0. Why this addendum exists

The exact finite response certificate committed at ea6e9d0 established a nonzero z=1 TT defect in a one-direction Bloch reduction. A subsequent literal pairing audit found a mixed-block Bloch phase inconsistency: the metric/connection mixed term did not follow the same test-variable placement convention as the connection Hessian. The flat z=0 control did not expose this because the sign enters quadratically there.

Therefore:

- the ea6e9d0 TT numbers remain a useful regression fixture;
- they are not a valid physical no-go witness;
- the response problem must be redone with phase-resolved metric Euler output and the full geodesic-normal curvature compatibility system.

The follow-up execution reported three important facts that now define the research frontier:

1. after the phase correction, the full 40-component phase-resolved metric Euler has a first-slow-order contribution that disappears under four-phase averaging;
2. one-coordinate slow ansätze are too restrictive because spatial center variations cancel part of the apparent obstruction;
3. in the full 20-component geodesic-normal curvature test, the linear compatibility system leaves one compatible physical curvature component, and on that surviving component the corrected response equals the flat Einstein control exactly.

These follow-up claims still require repository-level exact replay and must not be promoted before that replay exists.

## 1. Immediate certificate target

Create a corrected exact certificate, separate from the historical ea6e9d0 artifact.

Required outputs:

- literal mixed-block phase convention derived from the same oriented-edge/test-variable placement used for A;
- phase-resolved 40-component metric Euler, not only the four-phase average;
- exact z=0 owner/Schur/Einstein control;
- exact z=1 connection rank/kernel/cokernel;
- all four slow modulation directions;
- the full 20-dimensional geodesic-normal curvature basis;
- center/range corrections allowed in every spatial direction;
- exact compatibility matrix from normal curvature components to connection cokernel conditions;
- rank, kernel and basis of the compatible curvature subspace;
- exact metric response restricted to that compatible subspace;
- comparison with the flat Einstein symbol on the same physical quotient;
- hostile regression showing that the old mixed-phase convention reproduces the superseded defect and therefore fails the corrected assembly guard.

The certificate must explicitly distinguish:

- phase-resolved local output;
- supercell average;
- genuine continuum tensor readout.

## 2. Decisive finite verdict

There are only two acceptable outcomes.

### Positive compatibility terminal

If every physical curvature direction surviving the full joint compatibility equations satisfies

[
S_{Y,mathrm{compat}}^{[2]}=S_{mathrm{Einstein}}^{[2]},
]

record:

A4D-Y-CURVED-NORMAL-JET-RESPONSE-COMPATIBLE

This is a finite normal-jet theorem, not yet the nonlinear continuum theorem.

### Negative compatibility terminal

If there exists a curvature direction J in the exact compatible subspace with

[
Delta S^{[2]}J
e0
]

on the physical quotient, record the exact rational witness and continue immediately to the nonlinear realization gate. Do not call it a global no-go until an exact smooth-background stationary sequence is built.

## 3. Nonlinear continuation from the compatible jet

Assume the corrected finite compatibility theorem is positive on a nonzero curved normal jet J.

Construct an exact stationary branch

[
K_h(J)=K_Y+ a_h(J)
]

over a sampled smooth metric

[
Q_h(J)
]

with

[
q(0)=0,qquad partial q(0)=0,qquad partial^2q(0)=J.
]

The construction must solve the literal finite connection Euler equation, not only its first two formal orders.

Acceptable routes:

- analytic Lyapunov--Schmidt/Kuranishi continuation with a convergent majorant;
- Newton--Kantorovich on the certified range complement plus exact reduced center equation;
- another rigorous finite-dimensional analytic continuation with constants tracked in h.

Required:

1. gauge-fixed/right-complement coordinates;
2. exact stationary center variables retained;
3. full cokernel compatibility at every solved order;
4. a radius of continuation that does not collapse faster than the background scaling needed for the continuum sequence;
5. explicit control of all omitted orders.

## 4. Uniform refinement estimate

The nonlinear branch is useful only if the remainder survives the h^-2 response normalization.

Prove, for the declared compatible branch,

[
E_K(Q_h,K_h)=0
]

exactly and

[
h^{-2}
left[
E_Q(Q_h,K_h)-E_Q(Q_h,K_h^{sm})
ight]	o0
]

in the owner topology.

A sufficient quantitative form is

[
left|
E_Q(Q_h,K_h)-E_Q(Q_h,K_h^{sm})
ight|
le C h^{2+gamma},
qquad gamma>0.
]

All constants must be controlled against:

- lattice refinement;
- almost-resonant complements;
- stationary-center amplitudes allowed by the theorem;
- interaction of conjugate Bloch sectors;
- smooth background parameters in the declared compact set.

## 5. If exact continuation fails

A failure is scientifically useful only if it is located in the actual reduced nonlinear equations.

Return:

- the first order at which the reduced center/cokernel equation fails;
- the exact polynomial/rational obstruction;
- whether the compatible linear curvature subspace is cut to zero or to a smaller nonlinear variety;
- whether the failure forces the Y amplitude to scale to zero with h.

If curvature kills the Y center nonlinearly, this supports the positive Einstein route; it is not itself a no-go.

## 6. Selector rule

Do not claim that a selector is required unless there are two exact source-compatible stationary branches over the same admissible smooth background with different normalized metric responses.

The mere existence of flat-metric nongauge Y vacua does not imply a selector is needed for the metric continuum theorem.

## 7. Smallest current blocker

After the phase correction, the smallest unresolved object is:

[
oxed{
	ext{exact nonlinear continuation of the corrected compatible curved normal jet}
+
	ext{uniform }o(h^2)	ext{ metric-response remainder}
}
]

Do not reopen global determinant geometry or connection uniqueness before this object is resolved.

## 8. Required final report

Return:

1. corrected phase convention;
2. exact compatible-curvature matrix/rank/basis;
3. response restricted to the compatible subspace;
4. nonlinear continuation theorem or exact obstruction;
5. h-uniform remainder estimate or exact failure;
6. selector verdict;
7. Einstein verdict;
8. one smallest blocker if still open;
9. exact replay commands and result artifacts;
10. nonclaims.
