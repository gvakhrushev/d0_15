# Strict prospective-minimum gate for the actual whole-HJR collar branch

## Input and exact consumer

This is a bounded consumer of
`A4D_EXACT_CURVED_WHOLE_HJR_FIXED_COLLAR_ROOT_2026_10_20.md` at
`07f2f2b15b7050a612d0075aa73db8dc46087a95`, its exact ten-variable chart,
and its saved rigorous Arb enclosure `COLLAR_HESSIAN_ARB.json`.
Their byte-exact original inputs are retained under `inputs/` with source
commit/blob/SHA256 pins. Later appended source theorems do not rewrite
what this certificate checked.
It does not recompute the unchanged spectral Hessian or alter the finite
stationarity theorem. The exact consumer is the possible substitution
“these conditional whole-HJR curved roots are selected by prospective
strict minimization of the complete native price.”

The source owner proves only joint stationarity and deliberately retains
physical admission, price, clock/current and refinement hypotheses.
The earlier v8 root expressly did not claim a stable minimum. The present
calculation decides the stronger question on the NEW fixed-collar domain:
the global-scale objection cannot automatically be used there, but the
following allowed interior direction can.

## One admissible interior path

Use the owner's variables in their exact order:

- five interior coframe generators S0,...,S4;
- four outgoing proper-link families T0,...,T3;
- incoming time-link coefficient.

Take the constant chart tangent

    v = (-1,-2,-1,0,-2,-1,0,0,0,1),  v^T v = 12.

At the owned base, the literal field path corresponding to x=s v is

    V(0;s) = (I+s Q) V0,
    Q = -I - 4 sum_(i=1)^3 E_(0i),
    U0(0;s) = exp(-s B),
    U0(-1;s) = exp(+s B),
    B = sum_(i=1)^3 (E_(0i)+E_(i0)).

All spatial links and every other exterior field keep their base values.
Both time links are among the owner's incident variable links. For small
s the coframe is invertible, the links remain proper Lorentz exactly, the
strict Julia/gap/positivity conditions persist, and the observers remain
in the rest gauge. Preparation is the same analytic rank128 Riesz section
M(q(s)); its complete RIGHT Gram is I128/128 for every s. No preparation
row or complementary mode is frozen.

This is not a gauge direction: since V0 is invertible,

    d(V^T eta V) = V0^T (Q^T eta + eta Q) V0 != 0,

and the central factor is exactly

    [[-2,-4,-4,-4],
     [-4, 2, 0, 0],
     [-4, 0, 2, 0],
     [-4, 0, 0, 2]].

The path is admissible for the DECLARED conditional fixed-collar problem.
Admission in the complete physical D0 execution is a separate hypothesis;
one may neither assert it for free nor forbid it retrospectively because
of the result below.

## Exact rational enclosure

The owned source normalization is D_x^2 S_red(0,0)=A/8. Parsing each
published Arb decimal enclosure as a rational interval, with no float or
eigenvalue computation, gives

    v^T A v in
    [-2372501681/4000000000, -2372493199/4000000000].

Thus the actual conditional action's second derivative along this path is

    d^2/ds^2 S_red(sv,0)|s=0 in
    [-2372501681/32000000000, -2372493199/32000000000]
    = [-0.07414067753125, -0.07414041246875].

Its first derivative is zero by the existing exact root theorem. Taylor's
formula consequently supplies strictly cheaper nearby allowed fields on
both sides for sufficiently small nonzero s. The base is not a local
minimum. This conclusion does not depend on the exploratory floating
minimum eigenvalue of A.

The curved IFT branch x(epsilon) and its full Riesz-reduced Hessian are
analytic. Since the displayed second variation is bounded strictly below
zero, it remains negative at x(epsilon) for all sufficiently small
|epsilon|. The theorem therefore extends to the actual nonflat branch,
with the same fixed epsilon/collar during the varied x-path. Shrinking
the owner's analytic neighborhood, one can retain the conservative bound

    D_x^2 S_red(x(epsilon),epsilon)[v,v] <= -c/2,
    c = 2372493199/32000000000.

No explicit epsilon radius is asserted.

## What a complete-price identification must now establish

Let the physically selected complete price on this SAME admitted path be

    S_full = S_HJR + E.

If the same base is to remain a critical point and be a local minimum,
then necessarily

    dE = 0,
    D^2 E[v,v] >= c,
    c = 2372493199/32000000000.

In the owner's ten-coordinate Euclidean operator norm, this implies

    ||D^2 E||_op >= c/12
                  = 2372493199/384000000000
                  > 0.00617836.

This is a necessary bound in this chart, not a new physical constant or
source term to insert. If the full-price minimizer moves, the exact base
bound does not apply to that new location; continuity gives the stated
local half-bound only while it remains in the corresponding neighborhood.
The actual original preparation/work/clock/history action must provide the
correction or its native constraints must actually exclude the direction.
An arbitrary stabilizer or a fitted exclusion does not close the premise.

An exact local invertible field dressing of the SAME action cannot turn
this stationary saddle into a minimum. At a critical point the Hessian
transforms by congruence. Its negative direction survives under the
inverse tangent map. Thus the already-owned exact coframe/source
reparameterization can transfer equations, but cannot by itself discharge
this strict prospective-minimum gate.

The result does not refute a weighted path law, stationary action, the
correct fixed-collar existence theorem, or GR. It distinguishes their
mathematical conclusions from strict minimization on the specified
admissible family. It introduces no change to raw216, any price, any
physical hypothesis or any goal status.

## Exact embedding into the later seven-slice bulk chart

The source continuation at `5b5c60047f1cfe518d4a8b42d9f71c6db033779c`
appends a stronger finite bulk theorem in section10. Its original sections1-9
and `COLLAR_HESSIAN_ARB.json` are unchanged. Separate byte-exact snapshots
of that extended proof, `WIDE_COLLAR_ARB.json` and its source checker are
pinned under `inputs/`; the latter is retained as text and is not executed
by this consumer. This section uses only the stated common action, Riesz
section and the bulk chart. It does not re-review or replay the new uniform
preparation theorem in section11.

The bulk interior contains t=0,...,6, with a sole fixed coframe/spatial-link
collar at t=7. The free chart has the original nine coframe/outgoing-link
coordinates on each interior slice, followed by the incoming time-link
coordinate at7. Let E: R^10 -> R^64 be the coordinate embedding

    (0,1,2,3,4,5,6,7,8,9) -> (0,1,2,3,4,5,6,7,8,63).

At the common homogeneous boundary value epsilon=0 the literal field maps
agree: the old incoming slice -1 equals7 modulo8, all other added interior
coordinates are zero, and the full rank128 Riesz section is the same.
Consequently the actual reduced actions obey

    S_10(x,0) = S_64(E x,0)

on their common local chart. Both values include all original conditional
H+J+R terms and the full spectral complement. No exterior Schur elimination,
new price, omitted preparation response or fitted identification is used.
The Hessian identity at their common root follows:

    E^T (A_64/8) E = A_10/8.

The bounded checker also verifies this identity at the exact Fourier-index
level. For every i,j among the ten coordinates, the triples

    ((r_i-r_j) mod8, c_i, c_j)

agree in the old chart and the pinned bulk chart after embedding. Thus all
100 entries use the SAME exact H kernel and the same original enclosing
calculation. No fresh wide Hessian evaluation or inversion is needed.

The extended vector has the only nonzero entries

    vwide[0]=-1, vwide[1]=-2, vwide[2]=-1,
    vwide[4]=-2, vwide[5]=-1, vwide[63]=1.

Its squared norm remains12 and its second variation at the common base is
in the SAME original rational interval displayed above. It is an allowed
bulk variation; keeping additional free coordinates fixed along this path
does not restrict the bulk equations. Analyticity gives a negative second
variation on the sufficiently small curved BULK branch as well. The exact
base correction bound and the local half-bound therefore have the same
conditional use in the larger chart. The finite bulk stationary theorem
does not itself establish a strict local minimum.

This is a fixed L8 result, not a uniform-refinement instability theorem.
Under a hypothetical change h->0, this delta-slice coframe tangent has a
discrete C1_h seminorm of order1/h. The corresponding physical link-log
coordinate K=log(U)/h also has a tangent of order1/h. The source's new
uniform preparation estimates require bounded jets in those norms. This
direction cannot be inserted as a uniformly bounded family without a
separate scaling and field analysis; the finite negative direction neither
contradicts that preparation result nor supplies a uniform joint estimate.
Native physical admission and complete-price identification remain open.

## Reproduction

    python3 check_collar_minimum.py --root REPOSITORY

The checker requires only Python's standard library. It verifies exact
input SHA256, reproduces the rational interval, checks the non-gauge
coframe generator and the proper Lorentz time-link generator, and rejects
a diagonal-only false positive: dropping the actual cross terms makes
the quadratic form positive. It additionally verifies the separate bulk
input pins and all100 principal-compression index equalities, with a wrong
incoming-coordinate control. `COLLAR_MINIMUM.json` is its receipt.

This packet consumes the existing pinned interval evidence; it does not replay or replace it.
