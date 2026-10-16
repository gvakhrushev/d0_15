# Warped quarter envelopes: shared-link compatibility excludes every regular center

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input head: `cfb92e9ea4eb4585bd3e59aa799d0ee089eb7e4e`.
Authoritative contract: 2026-10-01 v2, separate Targets D and U.
Action, independent-source convention and Lorentz quotient are unchanged.

Status: an exact finite compatibility certificate and an analytic
all-orders response theorem for a declared regular two-scale class on
fixed small nonconstant warped metrics. This is a scoped Target-U result,
not universality over unrestricted refinement families.

The [certificate](certificates/a4d_warped_quarter_regular_response_check.py)
and [pinned ledger](certificates/a4d_warped_quarter_regular_response_results.json)
assemble actual incident faces, the varying transported coframe and the
first smooth comparison connection. They retain all eight real quarter
coordinates. Ten exact rank-three minors exclude their real quadratic
cone from the first-slow compatibility kernel.

## 1. Fixed metric and exact class

There is an epsilon0>0 with the following property. Fix a smooth positive
nonconstant periodic f with `||f-1||_infinity<epsilon0`, and put

\[
S(y)=\operatorname{diag}(1,1,f(y_1),f(y_1)),\qquad
g=S^T\eta S,\quad h=1/L,\quad L\in4\mathbb N.
\]

The radius epsilon0 is existential, from exact transversality and
compactness below. No numerical value is asserted; in particular this
note does not assert that the earlier epsilon=1/50 probe is inside this
new radius. The separate designated rescue works on its explicitly
larger stated warp interval and supplies an exact connection branch.

Consider genuine Lorentz links

\[
K_h(n,p)=K_h^{\rm sm}(n)\exp\delta_h(hn,p),\qquad
p=(x_0+x_1+x_2+x_3)\bmod4,\quad n=x_1.
\]

The envelope has every one of the 24 link-generator components on each
of the four phases. A role-1 shift changes `(n,p)` to `(n+1,p+1)`;
the other role shifts change p to p+1 at fixed n. This class is preserved
by shifts, products, inverses and the full Euler equation.

Declare **regular integer-h envelopes** by

\[
\delta_h(y,p)\sim\sum_{m\ge1}h^m\delta_m(y,p)
\tag{1}
\]

in every fixed smooth seminorm on the envelope circle. Precisely, for
each M and k the remainder after M terms is `O_{C^k}(h^(M+1))`, with
fixed smooth real coefficients. This is an assumption on the exact
family; it is not inferred from a sup bound `delta=O(h)`.

Require literal connection stationarity and metric phase erasure:

\[
E_K(Q_h,K_h)=0,\qquad \Pi_{p\ne0}E_Q(Q_h,K_h)=0.
\tag{2}
\]

The second condition retains all 30 nonconstant-phase metric equations.
It is necessary for any independently prescribed source depending only
on y1. The phase-common response is not fixed by this condition. No
source is assigned from a candidate after solving the connection rows.

**Theorem.** Every exact family satisfying (1)--(2) has

\[
\delta_m=0\quad\text{for all }m,\qquad
\boxed{h^{-2}\|E_Q(Q_h,K_h)-E_Q(Q_h,K_h^{\rm sm})\|_1
=O(h^\infty).}\tag{3}
\]

The norm is the unweighted sum on the full L^4 carrier. Consequently the
same #216 ten-slot reconstruction has limit `-G[g]/2`. This is response
agreement, not exact connection uniqueness: differences beyond all
orders are allowed. The theorem neither constructs extra joint-source
branches nor assumes their existence. The designated invariant branch
from the preceding rescue satisfies the necessary phase-erasure class.

## 2. Literal shared-link first-slow calculation

Use the owned transported role generators

\[
T_r(S)=v_ru_r^\flat-u_rv_r^\flat,\qquad
u_r=s_b-s_a,\ v_r=s_c-s_a,\quad\{a,b,c\}=\{0,1,2,3\}\setminus\{r\}.
\]

The quarter log is `(a_r,b_r,-a_r,-b_r)_p T_r(S)`; write
`alpha_r=a_r-i*b_r`. These are four complex, eight real coordinates.
At a face `(r,s)`, the factors sit at `0,e_r,e_s,0`, with the final two
inverted. For its link Euler row at the output site, the code also uses
face bases `0,-e_r,-e_s`. Thus area weights and every boundary link have
their actual differing coframe arguments. None are reset cellwise.

Use formal variables h and t and keep the complete coefficient rectangle
`degree_h<=1, degree_t<=2`. Inserting the transported center on the same
comparison connection means the link is

\[
e^{hB_r}\exp\{t c_rT_r(S+h\ell\,\partial_1S)+\cdots\}.
\]

Here ell is the actual slow offset. B is fixed first: the literal
identity-background h forcing is inverted by `H_f(1)`, the same first
smooth coefficient as #216. At `f=1, f'=1` the only nonzero log-generator
coordinates are `B_(2,J12)=-1` and `B_(3,J13)=-1`; all 24 first-order
connection rows cancel exactly. This calculation is at the moving
comparison sheet, not at a finite Y vacuum.

The quarter normal chart has columns
`0,1,2,3,4,6,7,8,9,10,12,13,14,15,17,18,19,20,22,23`
and the 20 rows pinned in the ledger; its determinant is exactly 4 at
f=1. The matrix is the literal joint block `(A(i)^T;C(i))` in owner
opposite-phase placement. Eliminating these normal variables gives
14 complex first-slow equations

\[
\boxed{D_f\,\partial_1\alpha+f' B_f\alpha=0.}\tag{4}
\]

The code reconstructs all entries of B1 and D1 over Q(i). It certifies

\[
\operatorname{rank}D_1=4,\quad\operatorname{rank}B_1=4,\quad
\operatorname{rank}(B_1\ D_1)=6.
\]

Thus (4) alone leaves a compatible amplitude plane; it does not kill the
center by a false eight-column injectivity claim. Select reduced rows
`1,3,9,11` on D, put

\[
L_f=(D_f)_{\{1,3,9,11\}}^{-1}\Pi_{\{1,3,9,11\}},\qquad
\mathcal K_f=B_f-D_fL_fB_f.
\]

All coefficients are analytic for f near 1. Equation (4) implies

\[
\partial_1\alpha=-f'L_fB_f\alpha,\qquad
f'\mathcal K_f\alpha=0.\tag{5}
\]

At f=1 the complex rank of K is 2, and its entire kernel is exactly

\[
\boxed{\alpha_3=-\alpha_2,\qquad
2\alpha_2=(1+i)\alpha_0-(1-i)\alpha_1.}\tag{6}
\]

This is a computed varying-coframe compatibility condition, not the
frozen common-phase kernel or the finite-amplitude Y envelope equation.

## 3. Nonlinear quadratic gate removes the remaining plane

The already owned identity-quarter nonlinear certificate gives the
real quadratic alternating metric obstruction `Q2(c)`, after the
uniquely solved even-frequency connection corrections. Its complete
real zero cone is the ten three-dimensional planes:

* `b=0, a=(u,v,w,-v+w)`;
* `a=0, b=(u,v,w,-v+w)`;
* eight spatial planes with `a0=b0=0`, independently choosing one of
  a_r or b_r on each spatial role.

This uses the full ten-component metric gate, not the phase mean alone.
It is consumed from `A4D_IDENTITY_QUARTER_NONLINEAR_RESPONSE.md`; the
old cubic reconstruction is not rerun for this new theorem.

Realify K with the convention `alpha=a-i*b`. On every one of these
ten plane maps, the new certificate finds rank three and pins a nonzero
rational 3-by-3 minor. Hence

\[
\boxed{Q_{2,1}(c)=0,\quad\mathcal K_1\alpha(c)=0
\quad\Longrightarrow\quad c=0.}\tag{7}
\]

This finite statement is stronger than either condition separately.
On the real unit sphere the continuous function
`||Q2_1(c)||^2+||K_1 alpha(c)||^2` therefore has a positive minimum.
The normal graph defining Q2_f, and the matrices defining K_f, depend
analytically on f in the fixed invertible charts. Compactness preserves
that positive minimum for `|f-1|<epsilon0`. Thus (7) holds throughout
one whole coframe neighborhood, not only at its center. This is the
only reason a small-warp hypothesis enters the theorem.

## 4. Exact equations force every regular coefficient to vanish

Suppose the first nonzero coefficient in (1) is delta_m. The zero and
alternating fast harmonics have invertible frozen connection blocks,
so their coefficients vanish at order h^m. The leading quarter joint
equations put delta_m entirely in the four transported role lines.
Denote its amplitudes by c_m(y), or alpha_m(y).

At order h^(m+1), the quarter projection gives (4). A quadratic center
interaction is in the even harmonics, so it cannot cancel this equation.
The first odd cubic interaction has order h^(3m), strictly later than
h^(m+1) for every integer m>=1. Background, transported-basis and
range-derivative terms at this order are all retained in B_f and D_f.

At order h^(2m), the alternating connection equation determines the
quadratic normal correction uniquely. The alternating metric equation
then gives `Q2_f(c_m)=0`. Even harmonics below this order cannot be
freely inserted: their homogeneous connection coefficients are
invertible. Higher quarter coefficients and first-slow corrections
contribute to this even equation only at higher orders.

Where f' is nonzero, (5) and the neighborhood version of (7) force
`c_m=0`. A nonconstant periodic f has at least one such open interval.
The first equation in (5) is a linear ODE with smooth coefficients on
the full circle. Uniqueness propagates zero from that interval across
every critical point and plateau of f. Thus `c_m=0` everywhere, a
contradiction. Apply this argument inductively to each coefficient;
every coefficient vanishes.

The expansion's remainder definition now gives `delta_h=O(h^infinity)`
in sup norm and every fixed smooth seminorm. The full carrier has L^4
sites. Multiplication by L^4 and by h^-2 still leaves a super-algebraic
bound. Finite-stencil Lipschitz continuity in the compact metric/log
chart proves the **raw owner-sum** statement (3). No conversion of a
fixed pointwise power to an unweighted sum is used.

## 5. The first h*kappa^2 boundary term does not cancel off shell

The certificate also prevents a tempting incorrect shortcut. At
`f=1,f'=1`, choose the two cosine amplitudes `a1=a2=1`, all others
zero. This lies in the frozen real quadratic cone. Keep the frozen
quadratic normal correction, its coframe derivative, and the uniquely
solved first-slow quarter normal correction. The literal phase-mean
metric coefficient of h*t^2 is exactly

\[
\boxed{(3/8,\ 1/8,\ -1/8,\ -1/2,\ 0,\ 0,\ 1/4,\ 0,\ 0,\ 1/8)}
\tag{8}
\]

in slots `(00,01,02,03,11,12,13,22,23,33)`. An uncomputed normal
correction at order h*t^2 cannot alter this phase mean: its mean
linear metric map is C(1)=0. This is a coefficient of the formal
range solution, not a claimed global analytic range graph on the
varying lattice.

The remaining first-slow center rows are nonzero for this field. It is
therefore an off-shell control, not a response counterexample. Equation
(8) shows that unconditional first-boundary cancellation is false even
on the frozen quadratic cone. The positive regular result instead uses
the exact center compatibility (5), the quadratic metric equations,
and the all-orders consequence. No flat constant 81 is transplanted.

## 6. Scope and subsequent nonregular closure

The subsequent [nonregular isolation theorem](A4D_WARPED_QUARTER_NONREGULAR_ISOLATION.md)
removes the expansion assumption for these small nonconstant warped
backgrounds and the full product-closed one-envelope sector. Exact roots
with phase-erased metric response coincide with the designated exact branch
in a c_g*sqrt(h) sup ball, hence for every O(h) family. It uses exact parity,
the [all-frequency circle estimate](A4D_IDENTITY_FOURPHASE_CIRCLE_CONTROL.md),
and two separately normalized weak limits. Candidate expansions, normalized
derivative bounds, and envelope smoothness are no longer required there.
The theorem also persists on a C1-open class of one-coordinate coframes.
The regular theorem above and its finite certificate remain valid inputs.

General four-dimensional g, other resonant carriers, and arbitrary
finite-amplitude stationary branches remain outside both results.
The fixed nonconstant metric, exact phase-erasure equations and shrinking
neighborhood are essential. The full Target D separately needs its actual
variable-background connection estimate and exact center compatibility.
A negative terminal would require an exact independently sourced joint
witness. PR #310 remains PARTIAL/OPEN, Draft/IN_PROGRESS; no BOOK/CORE,
selector or task-level Einstein claim is promoted.

## Replay

```sh
python3 02_REGISTRY/research/certificates/a4d_warped_quarter_regular_response_check.py --expect 02_REGISTRY/research/certificates/a4d_warped_quarter_regular_response_results.json
```

The finite coefficient calculation and cone transversality are exact
rational/Gaussian-rational certificates. Openness, ODE propagation and
the regular-family induction above are analytic proofs, not Lean
formalizations. No sampled spectral extrapolation is used.
