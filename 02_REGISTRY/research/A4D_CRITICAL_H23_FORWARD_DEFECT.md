# Critical h^(2/3) conformal forward defect

Repository: `gvakhrushev/d0_15`. Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Execution: existing Draft PR #310; input `1857d4a3c1a5bf7802ed1d0ce7830b1855d8734f`.
Status: analytic cubic extraction with exact finite coefficient controls;
stationary-sequence cancellation OPEN. No parent terminal or sharp threshold.

## 1. Unchanged objects and answer

Retain the cosine warp, solder, fixed smooth source, sampling, carrier and
all connection/metric Euler rows of A4D_FIXED_SOURCE_AMPLITUDE_ESCAPE.md.
Write the actual logarithm as a=h^(2/3) A, with ||A|| infinity <= M.
Here A is a normalized mesh field, not a smooth extension.
Let S_h be the literal unnormalized action, I_h=h^2 S_h, and B=h omega_LC[g].
For every fixed smooth scalar psi, exact connection stationarity gives

    h^2 sum Xi(g,exp a):psi g - integral rho0[g]:psi g
       = - (1/2) h^4 sum_faces psi(hx) p3_x,rs(g_h; A) + O_psi,M(h^(1/3)).  (1)

The coefficient on the right is explicit, not an uncontrolled Taylor remainder.
Its limit is not asserted to exist. For joint roots with the fixed source,
its weak limit necessarily exists as a distribution and equals the fixed
smooth trace mismatch. Whether stationarity forces it to zero is still open.

## 2. Literal coefficient, including ordered incidences

For the face (x;r,s), use the unchanged naked-star weight W_x,rs and set

    X1=A_x,r, X2=A_x+er,s, X3=-A_x+es,r, X4=-A_x,s.

Every A_x,r is its physical Lorentz Lie-algebra matrix in the existing
six-generator convention. If <W,P> denotes exactly the owner's entrywise
weight contraction, then

    p3_x,rs(A) = <W_x,rs,
       sum_{n1+n2+n3+n4=3} X1^n1 X2^n2 X3^n3 X4^n4/(n1! n2! n3! n4!)>. (2)

The order in each product is fixed. The sum has 20 terms. Thus P3=sum p3
is the homogeneous cubic Taylor coefficient of S_h at identity; the third
derivative tensor is 6 P3, not P3. No continuum derivative of A appears.
Formula (2) applies on the actual full lattice, without choosing a period-four
ansatz. Smooth weights are evaluated at their actual face bases.

## 3. Direct forward proof; no differentiation of a big-O estimate

All pairings below are finite full-field sums. Put D=a-B and q_s=(1+s psi)g,
B_s=h omega_LC[q_s]. Exact conformal face scaling makes the action linear
in s at fixed log field. Write H=D_a^2 S_h(g,0), ell=D_a S_h(g,0).
The smooth preparation and its parameter derivative satisfy

    F(g,B)=O(h^2),
    ell' + H' B + H B' = O(h^2),  B'=O(h).

These are smooth known-field estimates, not derivatives of mesh equations.
Finite analytic Taylor expansion at B and at identity gives

    H D = -F(g,B) - grad P3(D) + O(h |D| + h |D|^2 + |D|^3),

where the h|D| term includes the difference between the Hessian at B and H.
Equivalently its leading nonlinear remainder is bounded by O(h r+r^3),
with r=max(h,||a|| infinity). All constants have bounded incidence multiplicity.

The direct metric derivative difference at fixed a and B is

    (ell'+H' B).D + (1/2) D^T H' D + P3'(D)
       + O(N_h (h r^2+r^4)),

with primes denoting the conformal parameter derivative, N_h=h^-4.
Replace ell'+H'B by -H B'+O(h^2). Pair stationarity with B'
to bound -B'^T H D by O(N_h(h^2 r+h r^2)); all retained smooth
preparation chain-rule terms obey the same bound or O(N_h h^3).

The exact weighted Hessian identity of the pinned forward owner gives

    D^T H' D = <H D, psi D> + O(N_h h r^2).

Pair stationarity with psi D. The linear preparation error contributes
O(N_h h^2 r). Replacing the Hessian at B by H contributes O(N_h h r^2).
For the cubic gradient, termwise face locality and Euler homogeneity give

    <grad P3(D), psi D> = 3 P3_psi(D) + O(N_h h r^3),
    P3'(D) = P3_psi(D) exactly.

The coefficient is therefore 1 - 3/2 = -1/2. The resulting normalized
error is bounded by

    C [h + r + r^2/h + r^4/h^2].                           (3)

Replacing D by a in the cubic adds O(r^2/h); this is already in (3).
The smooth preparation response converges with O(h) error by the owned
smooth full-action expansion and its smooth parameter derivative.
For r<=C_M h^(2/3), (3) is O_M(h^(1/3)). Homogeneity yields
h^2 P3_psi(a)=h^4 sum psi p3(A), proving (1).
No secant optimization and no derivative of C9 is used.

## 4. What the finite checker does and does not establish

`certificates/a4d_critical_h23_cubic_check.py` reuses the unchanged generator,
weight and ordered four-link owner. Exact Fraction arithmetic compares (2)
against independent truncated exponential multiplication and checks cubic
homogeneity and the radial elimination factor. On three arbitrary rough
four-phase fields it obtains respectively

    P3 = -1668/12167, -639/12167, -2213/12167.

Thus P3 is NOT the zero polynomial on arbitrary admissible log directions.
These fields are NOT exact stationary roots or fixed-source witnesses.
Three quarter-kernel controls, including the single Y direction, have P3=0
and zero first-order connection Euler. Neither these samples nor generic
nonzero values classify the cubic on realizable stationary sequences.
The existing full weighted incidence checker is separately replayed.

Reproduce from the repository root:

    python 02_REGISTRY/research/certificates/a4d_critical_h23_cubic_check.py
    python 02_REGISTRY/research/certificates/a4d_conformal_forward_response_check.py

## 5. Exact next pass/fail gate

Define C_h,psi(A)=h^4 sum_faces psi(hx) p3_x,rs(A).
For the joint roots, (1) fixes

    lim C_h,psi(A_h) = -2 integral psi g:(tau-rho0[g]).       (4)

PASS for exclusion of the entire bounded critical-amplitude class requires
an analytic identity/estimate, uniform for every bounded normalized actual
stationary sequence on this same carrier, proving C_h,psi -> 0 for every
fixed smooth psi. Together with the fixed source this forces Einstein trace;
the pinned algebraic critical-value obstruction then excludes these roots.
It would strengthen o(h^(2/3)) exclusion to O(h^(2/3)) exclusion, without
automatically establishing a higher exponent or a sharp threshold.

FAIL of structural zero on the stationary class requires an actual refining
connection-stationary sequence with a certified nonzero limiting C_h,psi.
FAIL of fixed-source amplitude no-go additionally requires every literal
metric row to equal the one fixed sampled source. An arbitrary direction,
finite kernel sample, formal jet or fitted source is insufficient for either.

The smallest missing estimate is cancellation (or a certified nonzero limit)
of this explicit cubic moment on actual stationary sequences. Merely checking
that A_h lies near a linear kernel does not suffice: variable coefficients,
mesh-dependent near-resonances and nonlinear range solvability must be retained.
No Young-measure closure is assumed. The bounded cubic densities have weak
subsequential limits, but their vanishing has not been proved.

The fixed-amplitude branch, traceless channels, carrier replacement, full
parent terminal and sharp-threshold claims remain outside this critical gate.
