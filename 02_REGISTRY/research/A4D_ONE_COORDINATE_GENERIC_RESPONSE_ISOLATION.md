# Generic one-coordinate metrics: exact stationary-response isolation

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Status: a genericity corollary of the literal shared-link first-slow owner
and the nonregular isolation theorem. It enlarges their curved metric class;
it does not settle unrestricted four-dimensional microstructure.

## Statement

Work in the fixed smooth Gram coframe section near `I`. There is a
`C^1`-small neighborhood of the constant metric among smooth periodic
one-coordinate metrics `S(y1)` in which the following class is **open and
dense**: at some point `y0`, the shared-link first-slow compatibility
map is **injective on all four complex quarter amplitudes**. For every
fixed metric in this class, the [nonregular isolation
theorem](A4D_WARPED_QUARTER_NONREGULAR_ISOLATION.md) holds verbatim:
for some `c_S,h_S>0`, every arbitrary four-phase lattice field in the
one-coordinate invariant sector satisfying all connection equations and
all thirty nonconstant-phase metric equations, with relative log
`||u_h||_infinity<=c_S sqrt(h)`, equals the exact designated connection.
No envelope expansion or frequency cutoff is assumed.

Consequently these exact fields have the same ten-component metric
response as the smooth comparator up to `O(h^infinity)` in the full
unweighted owner sum after `h^-2` normalization. The phase-common
metric response is not imposed in the hypothesis. The designated root
exists for every sufficiently small fixed one-coordinate coframe by the
owned connection-only inverse; this is an actual curved solution class,
not a vacuous implication.

This is a generic theorem *within one-coordinate metrics*, not a claim
about all smooth metrics on a four-dimensional domain. The generic set
is open and dense in the stated `C^1` neighborhood, but a profile on its
exceptional complement is not thereby an extra branch.

The class contains explicit genuinely curved profiles: choose the
local Gram section of `Q(y1)=eta+epsilon*sin(2*pi*y1)*dot Q` with `dot Q`
from (3) and sufficiently small nonzero `epsilon`. At `y1=0` its
coframe derivative is `2*pi*epsilon*v_*`, so the minor in (4) scales
by `(2*pi*epsilon)^4` and stays nonzero. The linearized
`R_(0101)` contains the nonzero second derivative of `Q_00` away from
the sine zeros; curvature therefore does not vanish identically.

## One exact witness gives a whole generic class

At a frozen constant coframe `S`, use the four complex quarter amplitudes
`alpha_r=a_r-i b_r` and the 14-complex-row first-slow equation obtained
from the literal faces at `0,-e_r,-e_s`:

\[
D_S\partial_1\alpha+B_{S,v}\alpha=0,
\qquad v=\partial_1S.
\tag{1}
\]

The owner [shared-link certificate](certificates/a4d_warped_quarter_regular_response_check.py)
builds this equation with neighboring coframes and the first smooth
comparison connection, not with independently frozen cells. Its selected
four rows of `D_I` have nonzero determinant; they remain invertible for
`S` near `I`. Put

\[
L_S=(D_S)_{\mathcal I}^{-1}\Pi_{\mathcal I},\qquad
K_{S,v}=(I-D_SL_S)B_{S,v}.
\tag{2}
\]

Equation (1) is equivalent to
`alpha'=-L_SB_{S,v}alpha` together with `K_{S,v}alpha=0`.
At fixed `S`, `B_{S,v}` is **linear in v**. Every first-order change of a
face area or transported triangle bivector is linear in `S'`; the first
smooth comparator connection is obtained by an invertible frozen
connection matrix acting on that same linear forcing. The stencil has
no first-slow forcing when `v=0`. Thus `K_{S,v}` is linear in the 16 real
entries of `v`, with coefficients analytic in `S`. No regularity of a
candidate amplitude has been used in this construction.

The diagonal warp tangent
`v_warp=diag(0,0,1,1)` has `rank_C K_(I,v_warp)=2` and needs the
separate quadratic metric gate in the owned theorem. A new [exact
physical-gradient certificate](certificates/a4d_onecoordinate_generic_firstslow_check.py)
instead uses the symmetric Gram tangent

\[
\dot Q=\begin{pmatrix}
3&11/2&8&21/2\\
11/2&9&25/2&16\\
8&25/2&17&43/2\\
21/2&16&43/2&27
\end{pmatrix},\qquad
v_*=\tfrac12\eta\dot Q.
\tag{3}
\]

It generalizes the literal jet to this derivative while retaining all
actual face bases, shifted links, coframe weights and first smooth
connection coefficients. As a negative control, the generalized code
reproduces the old warp `B,D` matrices **entry by entry**. For `v_*`,
it checks all first-order background Euler rows and obtains

\[
\operatorname{rank}_{\mathbb C}K_{I,v_*}=4,\qquad
\det(K_{I,v_*})_{\{0,2,4,6\},\{0,1,2,3\}}
=\frac{24575+18625i}{32}\ne0.
\tag{4}
\]

The exact determinant and every input coefficient are in the [pinned
result](certificates/a4d_onecoordinate_generic_firstslow_results.json).
This is a physical metric derivative: `v_*` is the true horizontal Gram
lift of the symmetric `dot Q`, not a vertical Lorentz gauge direction.

Let `p(S,v)` be the same 4-by-4 minor of `K_(S,v)`. At fixed `S`, it is a
homogeneous degree-four **complex-valued polynomial** in the real
entries of `v`. Equation (4) proves that it is not identically zero
on the ten-dimensional physical horizontal tangent at `S=I`.
The coefficients and horizontal spaces vary analytically with `S`;
therefore the transported witness remains nonzero throughout a smaller
coframe neighborhood. Hence for every such `S`,

\[
\mathcal G_S=\{v:p(S,v)\ne0\}
\tag{5}
\]

is open and dense in physical metric-derivative space. A nonzero
complex polynomial cannot vanish on a real open set; equivalently at
least one of its real or imaginary parts is a nonzero real polynomial.
Every `v` in (5) makes `K_(S,v)` injective on all four complex center
coordinates. This is stronger than excluding only the real quadratic
cone and requires **no** classification of that cone. No uniform
lower bound is asserted as `v` approaches the exceptional algebraic
set `p=0`.

## From one generic point to a global fixed-metric theorem

For a fixed smooth periodic `S(y1)`, assume
`p(S(y0),S'(y0))!=0` at one point. By continuity the linear center
kernel is zero on an interval about `y0`. The exact
all-frequency estimate and parity argument of the [nonregular
owner](A4D_WARPED_QUARTER_NONREGULAR_ISOLATION.md) apply to arbitrary
arrays. A hypothetical nonzero root with `||u_h||/sqrt(h)->0` has a
nonzero uniformly convergent center limit. Its odd normalized weak
limit satisfies the *literal shared-link* equation (1). Its
compatibility part `K_(S,S')alpha=0` alone forces `alpha=0` on that
interval; the even quadratic limit is not needed. The first four
rows of (1) give the linear ODE
`alpha'=-L_SB_{S,S'}alpha`; uniqueness propagates zero around the
whole circle, contradicting the normalized nonzero center. The same
compactness argument yields a positive `c_S` and the isolation radius
`c_S sqrt(h)` without an asymptotic expansion of the candidate.

The set of profiles with such a `y0` is open in `C^1` by continuity.
It is dense in the small smooth periodic one-coordinate class: choose
any `y0`, keep `S(y0)` fixed, and add an arbitrarily small smooth
periodic bump whose value at `y0` is zero and whose derivative changes
`S'(y0)` into the dense set `G_{S(y0)}`. The perturbation can remain in
the Gram section and in the designated-root radius. Thus genericity is
over metric profiles, not just over formal tangent symbols.

The exact designated root has the owned super-algebraic owner-sum
distance to the smooth comparator. Isolation therefore gives the
response conclusion by the finite-stencil Lipschitz estimate, with no
replacement of an unweighted sum by a pointwise bound.

## Scope and quotient interpretation

The [minimal response-memory map](A4D_STATIONARY_RESPONSE_MEMORY.md)
is the ten-component projection of actual plaquette curvature.
Here the shared-link first-slow equation alone forces every admissible
small one-coordinate center into the
designated root on a generic curved metric; the projected memory then
agrees in the owner topology. Merely defining that quotient would not
give this collapse. Conversely the exceptional algebraic derivative
set is only a failure of this particular witness; it is not a
constructed physical rescue.

For all four spatial dependencies, other Bloch supports and finite
amplitudes, the corresponding projected-current collapse or an exact
joint-source counterexample remains the task-level gate. Keep PR #310
Draft / `IN_PROGRESS`.
