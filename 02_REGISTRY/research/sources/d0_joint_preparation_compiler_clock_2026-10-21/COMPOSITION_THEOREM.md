# Conditional composition: balanced preparation and a positive affine compiler envelope

21 October 2026. Independent mathematical composition note for existing
Draft #334. This is a theorem about a stated SAME-ACTION interface. It
does not identify the cap1 CQ action, full128 cap2 coherent action, and
monitored return-cut action with one another.

Consumed preparation theorem:
`BALANCED_NATIVE_PREPARATION.md`, SHA256
`7b9d3afe684f34695a4dfd6d89a8db457ba9cf47002733c65e9a2dc5c5751d68`.

## 1. Exact interface and statement

Let y vary over the genuine open, finite-dimensional field/material
chart of that theorem. Every originally fixed collar remains fixed;
the selected material angles are free coordinates. Let

    A0(y)=A(y,0),       F(y)=min_(a in K) A(y,a).

Use the same compact local preparation domain K, with zero in its
interior, and the unique continuous interior minimizer a_*(y) supplied
by the balanced theorem. In particular F is C1,

    Crit(F)=Crit(A0),
    a_*(y_*)=0, F(y_*)=A0(y_*),
    D^2 F(y_*)=D^2 A0(y_*)

at every full critical point y_*. The Hessian statement means that the
complete gradient of F is differentiable there; it does not assume F
is C2 throughout a neighborhood.

Suppose an ACTUALLY admitted finite set of executions of this SAME
action has exactly the form

    S_j(y,a)=B_j+g_j A(y,a),     j=1,...,N,
    B_j real constants,        0<g_j<infinity constants,

with the same variables, information cut, field-independent constants,
and the same preparation domain K. Set

    V(s)=min_j(B_j+g_j s),
    G(y)=min_j min_(a in K) S_j(y,a).

Then G=V(F) exactly. Its classical critical set and its Clarke critical
set both equal Crit(A0). At each such root G is differentiable, even if
several unequal slopes tie. Weak and strict local minima and maxima,
and stationary points with values of both signs relative to the root
in every neighborhood, agree for G, F and A0.

At an isolated active branch j, or when all active slopes are equal,
the Hessian at a true root is g_j D^2 A0. At an unequal-slope tie the
general second-order conclusion is the piecewise quadratic expression
in section 5; a single Hessian need not exist.

## 2. Positive affine elimination and the critical set

Positive, constant g_j and the common domain give

    min_a S_j=B_j+g_j F,
    min_j min_a S_j=V(F).

Write g_min=min_j g_j>0 and g_max=max_j g_j. For s2>s1,

    g_min(s2-s1)<=V(s2)-V(s1)<=g_max(s2-s1).              (1)

For the lower bound, each affine value at s2 is at least its value at
s1 plus g_min(s2-s1), and each value at s1 is at least V(s1). For the
upper bound, use any branch minimizing at s1. Thus V is strictly
increasing and Lipschitz, with a locally Lipschitz inverse on its image.

Since F is C1 and the branch set is finite, G is locally Lipschitz.
Let I(y) be the indices attaining its minimum. The finite minimum rule
(equivalently, negate the finite maximum rule for C1 functions) gives

    partial_C G(y)
       =conv{g_j DF(y):j in I(y)}
       ={lambda DF(y):lambda in
                       [min_(I(y))g_j,max_(I(y))g_j]}.   (2)

Every multiplier is strictly positive. Therefore

    0 in partial_C G(y) iff DF(y)=0 iff DA0(y)=0.        (3)

At a point with DF=0, differentiability of F gives
F(y+h)-F(y)=o(||h||). The Lipschitz estimate (1) then gives
G(y+h)-G(y)=o(||h||), so G is classically differentiable with DG=0.
Conversely, at DF!=0 equation (2) excludes a zero classical gradient.
This proves both asserted critical-set equalities, including all ties.
An unequal-slope tie at DF!=0 can be a kink, but cannot be a spurious
Clarke critical point.

## 3. The stronger balanced inequality and local surjectivity

Equality of critical sets and Hessians alone would not prove that
degenerate local extremum types agree: x^4 and -x^4 already show why.
Here the full preparation theorem supplies an additional exact order
relation.

Work in the selected angle coordinates, retaining all other fields.
Define the actual mean map

    T(y)=(other coordinates, theta+p^2 a_*(y)).

At the minimizing anchor preparation, the balanced coordinates are
mu=T(y), delta=a_*(y). The exact relative minimum at delta=0 and the
admissibility of a=0 in the original anchor problem imply

    A0(T(y)) <= F(y) <= A0(y).                           (4)

Both sides use this SAME A0. No independent field functional is being
substituted. At a critical point y_*, T(y_*)=y_* and the quantitative
minimizer estimate of the balanced theorem gives

    T(y_*+h)=y_*+h+O(||h||/ln(1/||h||)).                 (5)

In particular T is continuous and T-id=o(distance to y_*).

For completeness, (5) supplies local surjectivity without an implicit
function theorem or a derivative of a_*. Translate y_* to zero and
choose a sufficiently small closed ball so that

    ||T(y)-y||<=epsilon ||y||,     0<epsilon<1/2.

For any smaller radius r and any ||x||<(1-epsilon)r, the continuous map

    y -> x-[T(y)-y]

sends the closed radius-r ball into itself. Brouwer's fixed-point
theorem gives y in that ball with T(y)=x. Thus T maps every sufficiently
small neighborhood of zero onto a neighborhood of zero. Also

    ||T(y)||>=(1-epsilon)||y||,

so T(y)!=0 whenever y!=0 in that neighborhood.

## 4. Exact preservation of local extremum types

All comparisons below are at a critical point y_*, where
F(y_*)=A0(y_*).

If A0 has a local minimum, continuity of T and the left inequality in
(4) give F(y)>=A0(T(y))>=A0(y_*). If F has a local minimum, the right
inequality gives A0(y)>=F(y)>=F(y_*). This proves equivalence of weak
minima. Strict minima also agree: for the forward implication use
T(y)!=y_* when y!=y_*; the reverse implication uses the same upper
bound directly.

If A0 has a local maximum, F(y)<=A0(y)<=A0(y_*). Conversely, suppose F
has a local maximum in a neighborhood. Choose a small closed ball in
that neighborhood. Every x sufficiently close to y_* has a preimage y
in the ball under T, so A0(x)<=F(y)<=F(y_*) by (4). This proves that A0
has a local maximum. For strict maxima, x!=y_* forces its preimage
y!=y_*, and the same argument is strict. The forward implication is
already strict from the upper bound.

A sign-changing stationary saddle is a critical point which is neither
a weak local minimum nor a weak local maximum: every neighborhood
contains both a larger and a smaller value. Its preservation follows
from these two equivalences. Finally (1) shows directly that the sign
of G(y)-G(y_*) is exactly the sign of F(y)-F(y_*), so all these local
types agree also for G. This conclusion includes degenerate extrema;
it uses (4) and local surjectivity, not merely the common Hessian.

## 5. Hessians and unequal-slope ties

Fix a true root y_* and write

    s_*=F(y_*)=A0(y_*),    H=D^2 A0(y_*),
    q(h)=one_half H[h,h],
    I_*={j:B_j+g_j s_*=V(s_*)},
    g_+=min_(I_*)g_j,      g_-=max_(I_*)g_j.

The finite inactive set has a strictly positive value gap at s_*.
After shrinking the scalar neighborhood, no inactive branch minimizes.
Consequently the following is an EXACT local scalar identity:

    V(s)-V(s_*) = g_+(s-s_*)  if s>=s_*,
                 g_-(s-s_*)  if s<=s_*.

Since the complete gradient of F is differentiable at y_*,

    F(y_*+h)=s_*+q(h)+o(||h||^2).

The preceding scalar identity and its Lipschitz bound give the uniform
second-order expansion

    G(y_*+h)-G(y_*)
       =min_(j in I_*) g_j q(h)+o(||h||^2)
       ={g_+ q(h) if q(h)>=0;
         g_- q(h) if q(h)<=0}+o(||h||^2).                (6)

In particular the coefficient of t^2 along h=tv is g_+ q(v) when
q(v)>0, g_- q(v) when q(v)<0, and zero when q(v)=0. The corresponding
symmetric second-difference limit

    lim_(t->0) [G(y_*+tv)+G(y_*-tv)-2G(y_*)]/t^2

is twice that coefficient. When q(v)!=0, the scalar F(y_*+tv)-s_*
has a fixed sign for all sufficiently small nonzero t, so the same
quantity is also the classical second derivative of the restriction
t->G(y_*+tv) at zero. For null directions q(v)=0, only the second-order
directional Peano expansion and symmetric limit are asserted: the
restriction can encounter unequal-gain switches arbitrarily close to
zero, so a derivative of its first derivative is not automatic.

If one branch j is active alone, G=B_j+g_j F on a neighborhood, hence
D^2 G(y_*)=g_j H as a derivative of its gradient. The same holds if all
active slopes are equal: their intercepts are then equal as well, so
they define one identical affine function; inactive branches have the
finite positive gap just used.

If g_+<g_- and H is indefinite, the leading function in (6) cannot be
one quadratic form. Indeed any proposed quadratic form would equal
g_+ q on the nonempty open set q>0, forcing polynomial equality
everywhere; on the nonempty open set q<0 it would have to equal g_- q,
a contradiction. There is therefore no Hessian even in the weaker
second-order Peano sense in this case.

An unequal-slope tie does not ALWAYS preclude a quadratic expansion.
For semidefinite H, (6) is one quadratic form with the appropriate
extreme slope; for H=0 it is zero. These facts alone do not assert C2
regularity in a neighborhood, or differentiability at other nearby
tie points. Formula (6), rather than a branchwise Hessian asserted
through a switch, is the generally valid statement.

## 6. Physical and mathematical limits of this composition

This theorem is conditional on the displayed same-action identity for
S_j. The native balanced theorem currently concerns the specified
full128 cap2 coherent conditional entropy and its explicitly allowed
same-density smooth ledgers. A compiler result on a different cap1 CQ
instrument or a monitored return-cut source cannot be inserted merely
because its scalar coefficients resemble B_j and g_j.

The identity must use the same complete variables, preparation domain,
initial state and information cut, and must include actual upstream
prices. Field-dependent B_j or g_j introduce extra Euler terms.
Zero or negative gains invalidate the positive-multiplier argument.
Different preparation domains need not commute with this elimination.
A boundary-selected anchor minimum is outside the stated interior
envelope hypothesis. A separately supplied upstream term must pass
the balanced relative-source test or be retained as an additional
force. Infinite branch families require their own attainment, gap and
uniform regularity analysis.

The precise conditional synthesis is therefore: once the actual
same-action positive affine interface is established, balanced
preparation and finite compiler choice preserve the full stationary
set and its local extremum types, with the stated switch qualification
for Hessians. It does not establish that the remaining coincidence
functional is the configured Golden-J2 source or that D0 selects GR.
