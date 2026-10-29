# What the full root differential can and cannot generate canonically

Input: PR #334 at `172876cdf38bfce6f87fdd4a059d524b60c10eb9`.
Consumer: the full spectral Hessian / stationary boundary relation and its
proposed use by the strong hypersurface-deformation classifier. This note
retains the original price. It does not declare auxiliary cotangent variables
to be physical fields or extend the native action.

## 1. An exact terminal graph supplies an Abelian constraint system for any price

Let y be any finite smooth chart of actual retained arguments, and let B(y)
be the unchanged, fully differentiated price on that chart. On the auxiliary
cotangent bundle use {y^i,lambda_j}=delta^i_j and define

    C_i=lambda_i-partial_i B.

Direct differentiation gives, strongly and off the terminal graph,

    {C_i,C_j}=partial_i partial_j B-partial_j partial_i B=0.  (1)

The change (y,lambda)->(y,C) is canonical: its canonical one-form changes by
dB. Thus the abstract algebra (1) contains no action-selection information.
On C=0 the canonical
two-form pulls back to zero, as already required for graph(dB) to be
Lagrangian. Locally the Hamiltonian flows of all C_i translate every y
direction; quotienting this entire constraint system leaves a point, rather
than an open metric/momentum phase space.

For actual vector fields V,W on the y-chart, put J_V=V^i C_i. With the stated
Poisson convention,

    {J_V,J_W}=-J_[V,W].                                   (2)

Consequently the bracket of these auxiliary constraints is controlled by the
chosen vector fields, independently of B. If only C=0 is tested, every such
bracket vanishes for every B and every V,W. A weak zero=zero check on this
graph cannot establish the strong geometric structure functions needed by
the owned classifier. Conversely, prescribing vector fields that already
satisfy a deformation algebra installs its kinematics without deriving it
from the original price.

This is an obstruction to one proposed final inference, not to genuine
Hamiltonian dynamics obtained from independent boundary data. It does not
invalidate the existing two-boundary generating relation: that relation lives
in a product of boundary cotangent spaces, and requires its actual mixed
rank and physical boundary interpretation. It cannot be replaced by treating
the one-terminal graph as the whole phase space.

The distinction has a standard field-theory counterpart: parametrized field
theories on a prescribed background also possess deformation generators.
Their added embedding variables are not the six independent dynamical metric
coordinates of the repository's Einstein rigidity theorem. See Isham and
Kuchar, *Representations of spacetime diffeomorphisms. I. Canonical
parametrized field theories*, Annals of Physics 164 (1985), 288–315,
DOI: https://doi.org/10.1016/0003-4916(85)90018-1. No new embedding variables
are inserted in D0 here.

## 2. The precise gauge-compatible replacement for an interior inverse

The new full-boundary owner uses coordinates (x,w), full Hessian B_ab and a
regular stationary interior B_w=0. Real gauge modes cannot be silently
removed by replacing B_ww with a pseudoinverse. The required compatibility
can, however, be proved from a true symmetry before doing that calculation.

Suppose a genuine smooth internal symmetry leaves x fixed and leaves the
complete B invariant. Let v(x,w) be any of its vertical infinitesimal
generators. At B_w=0, differentiation of B_w v=0 in w and x gives

    A v=0,  v^T B_wx=0,  A=B_ww.                         (3)

Assume on a specified regular stratum that this symmetry has a smooth local
quotient, and that ker A is exactly its vertical tangent space. These are
rank and physical-symmetry assumptions; diagonal covariance of an operator
alone does not establish that the symmetry fixes the physical boundary.
Then the quotient interior Hessian is nondegenerate, and the implicit
function theorem applies on that quotient. For the resulting stationary
value S(x),

    S_x=B_x,
    S_xx=B_xx-B_xw G B_wx,                               (4)

where G is any generalized inverse satisfying A G A=A. Indeed A is a real
symmetric Hessian, so (3) puts every column of B_wx in range(A). If B_wx=A Y,
then B_xw G B_wx=Y^T A G A Y=Y^T A Y, independent of G and of the gauge
representative. The quotient equation gives the same expression. This is
why a gauge inverse is permitted only after proving (3) and the quotient
rank, and why projection of an incompatible source is not legitimate.

In a specified Euclidean physical chart, if the least absolute nonzero
eigenvalue of A is at least mu>0, its Moore–Penrose inverse satisfies

    ||B_xw A^+ B_wx|| <= ||B_xw||^2/mu.                  (5)

Uniform refinement needs a uniform bound in the true scaled norm; no such
bound is created by this identity. If ker A contains additional physical
flat directions, or a gauge transformation moves x, the claimed quotient
and (4)'s use must be reconsidered on the actual constrained chart.

## 3. Application to the original reflection source

The [exact QUERY stationary-reduction theorem](QUERY_STATIONARY_REDUCTION.md)
now decides this question on the current matched-reflection construction.
Write T for the QUERY reflection, P for the genuine active cut, and
A=(PTP)|ran(P). The full free relative QUERY orbit equation is equivalent to

    spec(A) subset {-1,0,+1}.

On any connected smooth stationary section, with rank r and z fixed, the
multiplicity m of zero cannot change. The unchanged return therefore becomes

    J_reduced=-m log(1-z).

For the specified history that remains INTERNAL at EVERY stage for EVERY x
on the section, with fixed scene, beta, paid clock N and full work dimension,
the actual matched-reflection heat is also constant,
because the monodromy's reflection signature is fixed. Every Hodge grade and
absolute trace anchor is retained. An INTERNAL base alone does not suffice
if neighboring stages mix the scene. Hence the reduced full master B is locally
constant, and its WHOLE boundary Hessian is zero. This conclusion follows
from the value identity and does not require an invertible interior Hessian.
If a regular interior inverse exists, the full Schur expression is zero; if
only the genuine regular gauge quotient of §2 exists, its gauge-independent
Schur expression is likewise zero. A pseudoinverse cannot create the missing
boundary rank.

An exact rank-one control makes this concrete. Let the original reflection
have relative angle 2(w-x-y), and put

    J=-log(1-z sin^2(2(w-x-y))).

This is the original return for P=diag(1,0) and the real reflection with
entries cos(2(w-x-y)), sin(2(w-x-y)); it is not an imported action. The angle
chart is an ambient matrix chart, not a claim of native continuous gates.
At the true stationary branch w=x+y, J=0 and J_ww=8z. At the other branch
w=x+y+pi/4, J=-log(1-z) and J_ww=-8z/(1-z). BOTH regular stationary branches
have identically zero reduced boundary Hessian, even though their interior
curvature is nonzero and the second branch is a maximum. Adding an actual
redundant gauge coordinate gives the same result through (3)-(4). The checker
also exhibits a kernel-incompatible source for which two generalized
inverses give results differing by 1; this is the necessary hostile control.

The parent source-transfer implication is explicit. On a genuinely open
field chart, suppose the proposed identity were

    dB_reduced=a(x) F_ref(x)+R(x), |a(x)|>=a_min>0.

Here a is the actual source multiplier, not a replacement action a S_ref.
In this sector dB_reduced=0, so necessarily

    R(x)=-a(x) F_ref(x),
    ||R(x)||=|a(x)| ||F_ref(x)||>=a_min ||F_ref(x)||.     (6)

It cannot supply an exact nonzero source transfer wherever F_ref is nonzero,
or a relative residual smaller than the target source there. Agreement at an
already stationary Einstein witness gives only zero=zero and does not select
the off-shell equations. Likewise, the nondegenerate endpoint-bracket
consumer cannot be used when its actual reduced mixed block is zero.

This is a scoped exclusion of free-QUERY stationary elimination as the final
composition of the current candidate. A physically derived restriction on
QUERY, a genuinely varying scene, noninternal history, or other actual price
terms can change its premises. Those are different remaining applications,
not ruled out by (6), and their sources must be retained. No restriction is
chosen here to impose the desired Einstein equation.

All displayed canonical/gauge facts are finite mathematical statements.
They do not identify the actual native variation graph with a continuous
chart or prove the physical strong deformation algebra. `GR_closed=false`.
