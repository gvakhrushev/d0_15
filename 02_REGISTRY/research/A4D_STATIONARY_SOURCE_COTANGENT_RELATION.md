# Full stationary source image as an exact cotangent relation

Task: EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, Draft PR #310.
Input: f4f88161325574e4c5750e0af4a8cc14a2f4b48e.
Status: full finite stationary-relation theorem and exact hostile controls;
original parent PARTIAL / OPEN.

For the complete finite stationary locus, the source map satisfies
\[
 i^*(\Xi\,dQ)=d(\mathscr A|_Z),\qquad
 i^*d(\Xi\,dQ)=0.
\]
This keeps the forward metric derivative and its horizontal-lifting
obstruction, which are not determined by stationary action values alone.

## 1. Flat endpoint is outside the current terminal

The task's 2026-10-03 scope explicitly retains one fixed nonconstant smooth
background and one independently declared fixed smooth source. An exact rooted
flat example would be a weaker terminal. A lift to a literally sampled
nonconstant metric would have to be proved separately; continuum coordinate
covariance cannot substitute for an invariance of this lattice action.

## 2. General exact statement, including stationary singularities

Fix a finite lattice and let B be the open finite-dimensional manifold of
nondegenerate metric/coframe quotient coordinates. Let M be the physical
Lorentz link manifold (or one genuine gauge slice where it exists). Write the
literal finite action as A(q,k). Its full stationary locus is

    Z = {(q,k): d_k A(q,k)=0}.

The stationary source image is the map

    i: Z -> T*B, i(q,k)=(q,d_q A(q,k)).

Let theta=p dq be the canonical one-form. On every smooth stratum of Z,

    i*theta = d(A|Z),             i*(dtheta)=0.                (1)

Proof: along any tangent (qdot,kdot) to Z, the chain rule gives
A_dot = d_qA qdot + d_kA kdot = d_qA qdot. Exterior differentiation on
that stratum gives the second identity. No inverse Hessian, connection
uniqueness, polynomial nonsingularity or source regularity enters. The exact
unconditional assertion is the pullback identity (1), not an assertion that
a singular image is an immersed manifold. Where i has locally constant rank,
the constant-rank theorem gives a local immersed image, and its tangent spaces
are isotropic because every image tangent lifts to the stratum. Its rank is
at most dim B. If that rank equals dim B, the local image is Lagrangian.
The function A is locally constant along fibers of i, so on such a local
constant-rank image it supplies a primitive of theta. Self-intersecting global
images can carry multiple primitives and require separate branches.

A smooth stratification of the finite matrix equations covers singular
stationary loci before any local quotient coordinate choice. Neither (1) nor
image isotropy proves that the source fibers vanish.

If A is constant on a stationary stratum C, equation (1) implies that the
response annihilates the metric projection tangent:

    d_qA in (d pi_B(TC))^ann.                                  (2)

If pi_B is submersive at a point on that constant-action stratum, all metric
responses at that point vanish. Without submersivity the exact conclusion is
only the pointwise annihilator statement (2). If pi_B has locally constant
rank on C, its local projected image D is a smooth submanifold of B, and (2)
places the response in its conormal bundle N*D. Calling D a metric
discriminant is a useful local description, not a theorem identifying one
global discriminant. This conormal conclusion applies only to constant-action
strata. For a stratum on which A varies, the full identity (1) must be kept.
The missing horizontal metric directions, rather than the connection moduli
themselves, are the possible source directions on a constant-action stratum.

A constant critical value on each fixed-metric stationary component does not
supply submersivity of the full stationary locus in metric variables.

## 3. Exact infinitesimal lifting/source duality

At a stationary point, write the full action Hessian in blocks

\[
 \begin{pmatrix}B&C^T\\ C&H\end{pmatrix}.
\]

The complete connection linearization is H delta k + C delta q=0. It admits a
horizontal lift of the metric variation delta q if and only if

    <v,C delta q>=0 for every v in ker H.                      (3)

This uses the finite symmetric Hessian identity im H=(ker H)^perp, after a
legitimate coordinate choice; gauge null vectors must be included or
quotiented consistently. The first source variation along a linearized
stationary vertical vector v in ker H is C^T v. Hence (3) says precisely

    metric directions admitting a linearized horizontal lift
      = annihilator of C^T ker H.

At a singular stationary point ker H is a linearized kernel. Its vectors need
not be tangent to exact stationary curves; the true tangent cone can be
smaller. Likewise a solution of H delta k+C delta q=0 need not integrate to
an exact branch. Equations (3) and the source formula are exact all-link
first-order statements. Higher obstruction ideals are necessary to decide
nonlinear continuation.

## 4. Hostile exact control: homogeneity and finite critical values are not enough

Consider the abstract generating family, NOT the D0 action,

    A(Q,u)=(Q00+Q11)u^2,

with eta=diag(1,-1,-1,-1). It has the same degree-one metric homogeneity used
by the radial action identity. At Q=eta every real u is stationary, its only
critical value is zero (also at every Q off that hyperplane, where u=0
is the only critical point), and

    Xi=u^2 (1,0,0,0,1,0,0,0,0,0),     eta:Xi=0.

Declare first tau=(1,0,0,0,1,0,0,0,0,0). Then u_h=h gives exact roots
Xi=h^2 tau inside every sufficiently small fixed chart and a nonzero
trace-free constant source on every lattice. The owner normalized gap from
zero is 2 L^4. This shows that zero action, finitely many critical values,
radial Ward identity, arbitrarily small root amplitudes and a fixed smooth
source do not together force source nullity.

There is no horizontal stationary lift through u!=0 in the metric direction
Q00+Q11: stationarity is 2(Q00+Q11)u=0. The nonzero source is exactly conormal
to that metric discriminant. The combined immutable Fraction replay is
[the combined checker](certificates/a4d_stationary_source_conormal_check.py)
with its adjacent pinned JSON. This is a proof-obligation
negative control, not a counterexample to D0.

## 5. Actual owned D0 datum: #232 is not metric-transversely constant

Use the exact owned period-four Y solution at t=1/5, Y=J12-J13+J23, Role0
links (U,I,U^-1,I), other links identity, flat standard solder. The literal
all-24 connection rows and all-10 metric rows vanish. Keeping these physical
links fixed, reconstruct the entire local metric normal Hessian
B_p=D_Q Xi_p from the two-leg face weight derivative. Since the full solder
Euler vanishes at the base, the second Gram-lift correction multiplies zero,
so the true metric Hessian is simply

    B_p[m,n] = sum_faces epsilon <W(H_m wedge H_n + H_n wedge H_m),P_face>,

where H_m are the true first Gram lifts. This includes all ten packed metric
components.

The exact result is

    rank B_p = 4,      B_p=(+,+,-,-)_p B_0,      sum_p B_p=0.

Examples (owner order 00,01,02,03,11,12,13,22,23,33):

    B_0[01,12]=-5/103,    B_0[01,13]=5/103,
    B_0[02,11]=5/103,     B_0[03,11]=-5/103.

All 24 nonzero entries, the full 10 by 10 matrix on every phase, and all
connection, metric and solder rows are recorded in the immutable combined
ledger. The checker compares the owned Euler with an independently assembled
full odd-curvature Euler and checks that every action, Gram and second-weight
pairing agrees with the literal (P-P^-1)/2. Four rational t values are replayed;
the general parameter identity below is an algebraic proof, not an
extrapolation from those samples.
For a general nonzero real Cayley t these entries are the same signed matrix
multiplied by t/(4+3t^2): odd plaquette curvature is
4t/(4+3t^2) Y, and the paired even Y^2 term vanishes. Therefore the rank-four
statement extends algebraically to every t!=0 in this rotational chart.

Consequences:
- Xi=0 on the flat stationary Y modulus does not mean D_QXi=0.
- The visible normal response is fast and mean zero, so it cannot itself be a
  fixed smooth source on refining meshes.
- Continuing the links to retain full stationarity can cancel this normal
  Hessian. No derivative of the frozen links alone is an exact rooted source.
- The correct object for Phi/pi0 or a stationary-sheet quotient is the exact
  cotangent relation (1), including the horizontal-lifting obstruction (3),
  not the stationary action value or the flat response fiber alone.

## 6. What remains unproved

Neither (1) nor (3) proves that the D0 exact stationary relation over a fixed
nonconstant sampled g contains one independently chosen fixed smooth source
at all refinements. Neither excludes all such roots. The existing generic
infeasibility theorem constrains critical values, while this audit identifies
why that theorem cannot discard the remaining trace-free conormal source
channels. An all-ten discriminant/conormal classification or an exact
horizontal continuation on the chosen nonconstant metric is still required.


## 7. Native finite-action completion needs the forward metric derivative

The [conformal forward bridge](A4D_CONFORMAL_FORWARD_SOURCE_BRIDGE.md)
now supplies that additional variation theorem in scalar metric directions.
It builds approximate horizontal endpoints through every retained exact
root with amplitudes `r_h^3/h^2 -> 0`, without a derivative bound on the
unknown links. The actual forward response has tested error
`O(r_h^2/h^(4/3))`; a fixed smooth exact source therefore obeys
`g:(tau-rho0[g])=0` pointwise. This determines the trace, while the
traceless conormal channels and fixed-amplitude parent chart remain open.

The [completed metric-probe source law](A4D_NATIVE_FINITE_PROBE_COMPLETION.md#15-constructive-fixed-source-closure-in-the-completed-variational-criterion)
is constructively solvable with one prior smooth Einstein source.
Its criterion uses independently prepared finite metric contrasts.
The exact original source relation uses the forward map

    (Q,K stationary) -> Xi(Q,K),

and then exact samples Xi(Q_h,K_h)=h^2 tau_h of one fixed smooth source.
A native finite-action or probe convergence theorem can provide a genuine
completion in its own norm. It does not identify that completion with this
forward derivative at a singular stationary projection without an additional
variation theorem.

The abstract control makes the logical gap exact: every stationary critical
value is identically zero for every metric, yet singular stationary roots on
ell(Q)=0 carry nonzero normal Xi. Thus even knowing all nearby stationary
action values cannot recover the source fiber on the vertical component.
Differentiating the critical-value function gives zero, while differentiating
the literal action at the retained root gives u^2 ell. These are different
derivatives because a horizontal stationary continuation through that root
does not exist.

This does not refute a completion which retains sufficiently many off-shell
metric-variation probes and proves their scale-uniform convergence. Such a
forward normal-projection theorem would be additional input. Neither this
audit nor finite-action values alone supply it. No new parent terminal is
claimed.

## 8. Portable immutable replay

Run, from any directory:

```sh
python3 /path/to/d0_15/02_REGISTRY/research/certificates/a4d_stationary_source_conormal_check.py --repo /path/to/d0_15
```

The adjacent JSON is an immutable expected ledger in default mode. The checker
first compares SHA-256 pins for the literal action owner, its generator/star
owner, the #232 provenance memo and the original source/nonconstant task brief.
It then recomputes all results independently of the ledger and compares the
entire object. The audited input is f4f88161; replay on a later head is allowed
if the pinned owners remain identical. No absolute repository path occurs in
the checker or ledger. --expect selects another immutable ledger; --output
explicitly writes a candidate replacement and is not the default replay.

PASS: all 24 Euler, 10 Gram and 16 solder rows; rank-four normal Hessian; true
Gram lifts; odd-curvature action/derivative pairing; exact phase cancellation;
complete polynomial trace-free fixed-source negative control. The proof of
(1)-(3) is analytic finite-dimensional mathematics above, not certified by the
finite Y calculation.
