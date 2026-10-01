# Identity quarter: nonlinear response suppression on a constant curved-frozen coframe

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Status: analytic local theorem from two exact finite inputs, with an independent
generic rational control. The coframe is **constant** on the four-phase cell;
the theorem does not glue cells of a varying metric.

## Statement

Fix the owner Gram-section action and a constant nondegenerate coframe `S`
in a sufficiently small open neighborhood `U` of `I`. Use the real
four-phase link-log chart, and let

\[
F_S(l)=\bigl(E_K(S,e^l),\Pi_{\ne0}E_Q(S,e^l)\bigr),\qquad
M_S(l)=\frac14\sum_{p=0}^3 E_Q(S,e^l)(p).
\]

The ten metric components use the same Gram section as the [flat nonlinear
owner](A4D_IDENTITY_QUARTER_NONLINEAR_RESPONSE.md). Here `Pi_ne0` deletes
only the phase mean, so a nonzero common response is allowed in `F_S=0`.
There are a smaller neighborhood `U_0`, radius `epsilon>0`, and `C<infinity`,
uniform for `S` in every compact subset of `U_0`, such that all `F_S(l)=0`
with `||l||<epsilon` are the eight single-role, single-parity axes below.
Each is an exact *full* joint vacuum. Moreover

\[
\boxed{\|M_S(l)\|\le C\|l\|\,\|F_S(l)\|}\tag{1}
\]

for all such `S,l`. The full joint zero set is therefore the same eight
axes. A compatible local error bound is
`dist(l,V_S)<=C||F_S(l)||^(1/3)`, where `V_S` is their union.

This extends the flat nonlinear theorem to a constant coframe near `I`.
It is stronger than the separate [curved-frozen quadratic
identity](A4D_IDENTITY_QUARTER_GENERIC_COFRAME_RESPONSE.md), but does not
assert a varying-coframe stationary branch or a refinement-uniform owner
sum bound for such a branch.

## Exact axes at every constant coframe

Write `S=(s0,s1,s2,s3)`. For each role `r`, let `a<b<c` be the complementary
roles, `u_r=s_b-s_a`, `v_r=s_c-s_a`, and

\[
T_r(S)=v_r u_r^\flat-u_r v_r^\flat,
\qquad T_r(S)^3=\kappa_r(S)T_r(S).
\]

For parity `s=0,1`, put `U_r(t)=(I-tT_r/2)^(-1)(I+tT_r/2)` on link `(s,r)`,
`U_r(t)^(-1)` on `(s+2,r)`, and identity on every other link. All 96
connection and 64 unrestricted coframe Euler rows vanish identically in
`S,t` whenever the coframe and Cayley denominators are nonzero. In
particular, all 40 Gram metric rows vanish.

Here is the algebraic extension argument; it is not an inference from one
numerical sample. The [exact moving-plane owner](A4D_Y_SLOW_JOINT_CONTINUATION.md#9-full-euler-proof-and-exact-certificate)
proves every literal row for role 0 on the nonempty open set where the
complementary plane is spacelike. Simultaneously permuting external roles
in the oriented face action changes its overall sign only by the
permutation parity. Every Euler zero therefore remains zero, giving the
same theorem for any role whose complementary plane is spacelike. For a
fixed role and `t`, each Euler row after clearing the nonzero Cayley and
coframe denominators is a polynomial in the 16 independent real entries
of `S`. A polynomial vanishing on the nonempty spacelike open set is
identically zero. Thus the row identity continues to all nondegenerate
real coframes at which its original rational expression is defined,
including coframes near `I` where a spatial role has a timelike plane.
Near `t=0`, the Cayley path is a straight log axis `exp(vT_r(S))` after an
analytic reparameterization.

An independent [exact rational control](certificates/a4d_identity_quarter_generic_axes_check.py)
uses one nonorthogonal coframe with all 16 entries fixed to rational
values and `t=1/5`. It reconstructs literal face derivatives and obtains
zero for all `96+64` rows on all eight axes; the pinned
[result](certificates/a4d_identity_quarter_generic_axes_results.json)
records the eight tests. This guards role and phase placement; the open-set
polynomial argument proves the universal identity.

## Stable nonlinear center classification

The [symbolic 16-variable quarter certificate](A4D_IDENTITY_QUARTER_GENERIC_COFRAME_RESPONSE.md)
proves that the full joint quarter kernel at constant `S` is exactly
`span_C{e_r tensor T_r(S):r=0,1,2,3}` near `I`. The remaining Fourier
blocks retain their flat ranks by openness. Consequently `DF_S(0)` has
rank 88 and an eight-real-dimensional kernel, smoothly parameterized by

\[
V_S(c)_{p,r}=(a_r,b_r,-a_r,-b_r)_p T_r(S),
\quad c=(a_0,\ldots,a_3,b_0,\ldots,b_3).
\]

Use the same 88 normal columns and range rows as the flat owner. Their
determinant is nonzero at `I` and hence throughout a smaller `U_0`.
The parameter-dependent analytic implicit function theorem gives a
normal graph `w=W_S(c)=O(|c|^2)`, uniformly on compact subsets of `U_0`.
Translation by two phases sends `c` to `-c` and preserves every constant
coframe. The range splitting commutes with that translation. The
remaining even-frequency and quarter equations therefore have the
uniform analytic parity expansions

\[
R_{e,S}(c)=Q_{2,S}(c)+O(|c|^4),\qquad
R_{o,S}(c)=Q_{3,S}(c)+O(|c|^5).\tag{2}
\]

Their coefficients depend analytically on `S`. At `S=I`, the [flat exact
certificate](certificates/a4d_identity_quarter_nonlinear_response_check.py)
proves that `(Q_2,Q_3)` has on the real unit sphere only the sixteen
signed axis zeros, and that its derivative on each seven-dimensional
sphere tangent has rank seven. Both facts survive on a common smaller
`U_0`: away from disjoint axis neighborhoods the compact sphere has a
uniform positive lower bound; near each signed axis, seven selected
output rows retain an injective tangent derivative. The exact axis
identities above pin a zero at the center of each neighborhood for every
`S` and every sufficiently small radius. The inverse function theorem
then excludes any displaced zero and gives a uniform transverse lower
bound. This is the same blow-up proof as the flat theorem, now with `S`
as a compact parameter; it does not require recalculating 36 quadratic
and 120 cubic coefficients symbolically in `S`.

With `A` the eight coordinate axes in `c` space, the resulting estimate is

\[
\|R_{e,S}(c)\|+\|R_{o,S}(c)\|
\ge c_* |c|^2\operatorname{dist}(c,A).\tag{3}
\]

The normal-range residual has a uniformly bounded local inverse, giving
the classification and cubic distance bound in the full 96-dimensional
chart. No full Bloch inverse is asserted.

## Uniform mean-response gain

Let `m_S(c)=M_S(V_S(c)+W_S(c))`. The phase mean is even in `c`.
Its value and derivative at zero vanish: the curvature vanishes at
identity links, and the zero-frequency discrete curl gives
`C_S(1)=0` for every constant coframe. Its complete quadratic term
also vanishes. The direct center term is zero by the universal
free-algebra quarter identity from the symbolic coframe certificate;
the degree-two normal correction is invisible to the phase mean because
`C_S(1)=0`. Hence uniformly

\[
m_S(c)=O(|c|^4),\qquad Dm_S(c)=O(|c|^3).
\]

The exact axes have `m_S=0` at every amplitude. Integrating the last
derivative to the nearest axis and applying (3) gives
`||m_S(c)||<=C|c|^3 dist(c,A)<=C|c| ||R_S(c)||`.
Moving off the range graph changes `M_S` by at most
`C||l||` times the normal residual, since `DM_S(0)=0`.
This proves (1) with constants uniform on the stated compact family.

For a strictly repeated four-phase field on `L^4`, `4|L`, the same
cell-counting argument as the flat owner gives an `L`-independent
componentwise `l^p` estimate for its *phase-common* response, including
`p=1`, provided the coframe is globally constant. A fixed smooth curved
metric has neighboring coframes that differ. Applying this result cell
by cell while ignoring boundary links would be invalid.

## Remaining task-level gate

The needed theorem is a nonlinear varying-coframe estimate for the
actual owner sum norm, including links that cross the four-phase cells,
an independently prescribed metric source, and comparison to the smooth
branch on the same sampled `g`. Other Bloch supports and finite-amplitude
microstructures also remain. Formula (1) does not by itself yield the
normalized `o(h^2)` response difference for those sequences. PR #310
remains Draft / `IN_PROGRESS`.

Replay the exact control:

```sh
python3 02_REGISTRY/research/certificates/a4d_identity_quarter_generic_axes_check.py
```
