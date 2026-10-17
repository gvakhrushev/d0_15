# G0: complete supplied parent laws and their stationary/source quotient

Input: `9e37e008ba89cfaa9a1a70f1d0ffaede6b5aab0b`, existing #310.
Supported D0 tree: `fd8dfc359d23c9bd79ca23eeed7c045ce9c68c6b`.
Status: **complete classification of the explicitly supplied covariant linear
four-slot parent interface, including its stationary/source comparison**.
The independent history-to-field action and native refinement are not inferred.
G0, physical Ward, GR and the original parents remain OPEN.

This consumes the [complete joint carrier](A4D_NATIVE_JOINT_FIELD_QUOTIENT.md),
the [literal parent and field-frame theorem](A4D_NATIVE_PARENT_SOURCE_BOUNDARY.md)
and the [positive source theorem](A4D_NATIVE_POSITIVE_SOURCE_JETS.md).
No new density, field constraint or action-selector principle is introduced.

## 1. The entire declared interface, without hidden differential premises

`FinitePrimalDualHodgeData P0 P1 D3 D4` has precisely four linear-map fields:
dP, dD, star0, star1. `mixedPrimalDualAction` additionally takes a pairing and
three independently varied P0 fields psi, chi, lambda. The structure has no
nilpotency, locality, cochain identity, positivity, metric dependence or native
refinement field. Those properties of a proposed specialization need their
own owners. In particular arbitrary maps in this interface must not be called
the actual cubical differential merely because its slot is named dP.

Fix perfect real pairings on P0/D4 and P1/D3, and use paired coordinates.
At a finite background X let P=dP, B=dD, H=star1, M=star0. Then the exact
action is

```text
I_X(psi,chi,lambda) = 1/2 chi^T M_X chi
                    + lambda^T(M_X chi-K_X psi),
K_X = B_X H_X P_X.                                      (1)
```

For a general supplied linear pairing represented by R, replace M and K by
R star0 and R dD star1 dP. This is the literal owner binding, including
noninjective R. A degenerate pairing has additional invisible directions;
it is not silently replaced by a perfect pairing in the classification.

If dim P0=dim D4=n and dim P1=dim D3=m, the complete pointwise visible action
family is every M in R^(n*n) and every K of rank at most m. Necessity is the
rank bound for a composition through R^m. Sufficiency: factor a rank-r K as
U V through r<=m, extend the factors by zero, and take H=identity. There are
no further constraints in this declared structure. When m>=n every K is
possible: choose a fixed inclusion E:R^n->R^m and left inverse L, and set
P=E, B=L, H=E K L. This also supplies smooth realizations for arbitrary
smooth K(X). When m<n, a smooth pointwise rank-bounded K need not admit a
global smooth factorization through the fixed trivial m-space; the actual
smooth-factorization requirement is retained, not replaced by the rank test.

For example over the circle, the periodic smooth rank-one matrix
K(theta)=(1/2)[[1+cos theta,sin theta],[sin theta,1-cos theta]]
cannot factor through a fixed trivial one-dimensional middle space. Its
image is the line spanned by (cos(theta/2),sin(theta/2)). A nonzero factor
vector would be a continuous nonzero scalar times that vector. Periodicity
requires the scalar to reverse sign after 2pi, forcing a zero, contradicting
rank one. The exact projector/endpoint controls accompany this analytic
factorization obstruction; they are not a topology theorem extrapolated
from numerical ranks.

For the complete exterior carrier n=m=16 L^4 all M(X),K(X) are allowed in
this interface. This is a valid specialization of its types, not a claim
that D0 selected the full exterior carrier for all four physical grades.
Actual scalar/one-form/dual-form specializations keep their stated types.

## 2. Full covariance is exactly seed data on the joint quotient

Take the actual nondegenerate raw frames F, Lorentz links U and affine shifts
a. Their complete background quotient is (q,D,b), with the exact metric-link
constraint from the joint-carrier proof. Let G0(F),G1(F) be the admitted
invertible primal frame lifts; the full exterior choice is the literal
pointwise `archiveExteriorFrameLift`. The dual lifts are forced by the fixed
pairings, as already proved by `dualAction`.

Every covariant four-map family is uniquely the following lift of its seed
maps on that quotient:

```text
dP_raw    = G1^-1 P G0,
dD_raw    = G0^T B G1^-T,
star0_raw = G0^T M G0,
star1_raw = G1^T H G1.                                  (2)
```

Indeed multiplying each raw map by the inverse frame factors recovers its
seed. Under F->F Lambda the decoded seed is unchanged by the four actual
moving-parent covariance laws. Completeness of (q,D,b) then proves descent.
Conversely arbitrary seed maps on the constrained quotient, lifted by (2),
satisfy those laws. For SO+ keep the frame-component data required by the
joint quotient. The matrix inverse identities and the visible composition
in (2) are compiled. The all-site orbit/descent assembly is analytic.

Writing the physical fields as p=G0 psi, c=G0 chi, l=G0 lambda gives
exactly (1) with the seed M,K=B H P. Thus covariance fixes the transport of
each seed, not its dependence on physical background data. It imposes no
additional condition on M,K in the entire n=m interface. Kinematic path
composition does not supply a rule selecting those functions.

## 3. Genuine variations for every M, including nonsymmetric stars

No symmetry assumption on M is needed in this owner. Put A=(M+M^T)/2.
Its actual three field derivatives are

```text
r_psi    = -K^T lambda,
r_chi    = A chi+M^T lambda,
r_lambda = M chi-K psi.                                (3)
```

Their directional pairings have genuine HasDerivAt proofs. The auxiliary
variation retains both chi^T M delta chi and delta chi^T M chi. Replacing
A by M when M is not symmetric changes the equation and is invalid.
The full independent field gate is exactly the vanishing of (3).

In ordered fields z=(psi,chi,lambda), define the symmetric Hessian

```text
             [ 0   0   -K^T ]
H(M,K) =     [ 0   A    M^T ].                          (4)
             [ -K  M     0  ]
```

Then I=1/2 z^T H z and the complete field fiber is ker H. For a genuine
admitted background direction V at fixed physical fields, the source is

```text
sigma[V] = 1/2 chi^T (D M[V]) chi
           +lambda^T((D M[V]) chi-(D K[V]) psi)
         =1/2 z^T(D H[V])z.                            (5)
```

If raw fields rather than physical fields are held fixed, the difference
is the contraction with the three actual field residuals and the frame
generator, from the consumed field-frame theorem. It is zero on full field
roots. Equations (3)-(5) are derivatives of the action, not a gate containing
the desired source or an Einstein residual. They use constrained native
directions; arbitrary off-constraint metric partials remain prohibited.

## 4. Complete action and stationary/source comparisons are different

As scalar functions of all three fields, two parent actions agree exactly
iff their M and K agree. Evaluating I(psi,0,lambda) determines K. Subtracting
I(0,chi,0) from I(0,chi,lambda) determines M, including its skew part. The
same proof gives equality up to one fixed nonzero calibration c iff
M2=c M1 and K2=c K1. This is action-level identification only.

For the actual fixed physical readout retaining all three fields, the
complete **stationary/source** comparison is instead, at every admitted X:

```text
ker H1 = ker H2 = N,
(D H2[V]-D H1[V]) restricted to N x N = 0
   for every admitted background direction V.          (6)
```

Necessity: equality of full field fibers gives the first line. Equality of
sources on that fiber gives zero diagonal of the symmetric difference on
N; polarization gives its entire restricted bilinear form. Conversely (6)
gives every field root and every background source in both directions.
The kernel/response criterion and polarization are compiled for arbitrary
finite real spaces. No constant-rank assumption, inverse or gauge removal is
used. A fixed source calibration is compared by substituting c H1 and
c D H1 consistently; c depending on X or h is not that calibration.

For any same independently defined geometric action, (6) is sufficient to
identify its combined joint roots. Necessity of the source comparison holds
for the full supplied geometric-covector interface: a covector cancelling
one source tests equality of the other. A single fixed geometric action may
have a weaker stationary correspondence; that must be proved on its actual
solution class. No arbitrary geometric term is installed as a D0 action.

Off-shell inequality is insufficient. For invertible full H, all such parent
laws have only z=0, whose source is zero, even when M,K differ. Nonzero-root
families likewise may have identical restricted sources. Conversely rank
changes do not make an actual nongauge kernel direction disappear. The
criterion keeps every coordinate of N and tests its source forms directly.
It does not identify N with Lorentz gauge or infer recovery from its rank.

If the physical matter readout retains only psi, auxiliaries need not be
identified. The exact projected correspondence is

```text
C_X = { (psi,sigma): exists z in ker H_X,
         z_psi=psi, sigma[V]=1/2 z^T D H_X[V] z for all V }.
```

It has an explicit finite description: choose any basis matrix T of ker H,
put A=T_psi, and solve A u=psi. If this is solvable, write u=u0+W v with
columns of W spanning ker A. Substitute into all quadratic forms
1/2 u^T(T^T D H[V] T)u. This describes every possible source over that
physical field, including nongauge auxiliary fibers. Equality of these
projected sets, not equality of raw auxiliaries, is the complete weaker
stationary/source test. It can be weaker than (6). No general equality of
quadratic-image sets is inferred merely from matching ranks or kernels.

An explicit auxiliary comparison prevents an unnecessary action selector.
For M1=diag(1,-1), K1=[[1,0],[1,0]], take M2=diag(4,-1),
K2=[[2,0],[1,0]], and T=diag(1/2,1). The compiled identity is

```text
I_(M2,K2)(psi,T chi,T lambda)
  = I_(T^T M2 T,T^T K2)(psi,chi,lambda)=I_(M1,K1).
```

T is invertible, preserves psi and all background readings, and transports
every independent auxiliary variation. Constant physical seed laws in this
example have identical projected stationary/source correspondences, although
M1,K1 and M2,K2 are not related by a common scalar. Raw auxiliary transport
uses the actual frame lift. Native refinement must separately commute with
that comparison; it is not inferred from the finite action identity. A
singular T gives no such equivalence and cannot erase missing field variations.

## 5. Complete joint-root classification of a native-field seed family

The following are two specializations of the same whole four-slot interface,
not two newly postulated core actions. At each site use all sixteen exterior
components, group them into eight pairs, and set

```text
M0 = diag(1,-1,...,1,-1),
K0 = diag_8( [1 0; 1 0] ),
E  = (1/8) diag(1,0,...,1,0),
f(q) = sum_(i<=j) c_ij (q_ij-eta_ij),
M_theta(q)=M0+theta f(q) E,       K_theta=K0,
```

with ten fixed nonzero rational coefficients c_ij. Choose the common
physical fields p=(1,...,1), c=(1,-1,...,1,-1), l=-c. All sixteen
components of every field are nonzero. At q=eta, (3) vanishes for every
theta, and the action is zero. The source is nonetheless

```text
sigma_theta[V] = -theta/2 sum_(i<=j) c_ij V_ij.          (7)
```

Here V is an actual **uniform transported-metric** variation: let every
raw F(t)=I+(t/2)V eta, every link U=I, and transform the three raw fields
by the inverse exterior lift to keep p,c,l fixed. The literal transported
center is F(t), so its physical Gram derivative is exactly V; dressed links
stay identity. These are two-sided nondegenerate native states for small t.
Raw-fixed-field differentiation gives the same source at the full field root.
All ten packed metric components and weights are tested, together with all
24 actual Lorentz link directions. Link stationarity is retained and does
not cancel (7). Arbitrary affine shifts remain in the general classification;
the uniform witness uses zero shifts only for its simple background.
The unrestricted family also admits D-dependent seeds. A separately stated
single linear D profile has a nonzero genuine source in each of the 24
Cayley link directions; the exact controls retain those possibilities rather
than silently specializing every covariant seed to metric-only dependence.

At theta=0 this state is a full background-and-field stationary point of
the literal parent specialization. At theta=1 it fails an actual background
Euler equation. The gauge invariant physical data are identical, and their
full-readout fiber is a single Lorentz orbit; therefore a readout-preserving
gauge or field-frame change cannot repair this stationary mismatch. A common
nonzero calibration cannot turn zero into (7). The coefficients and operator
law are fixed across L; h^4 times the site sum has the same nonzero source
for every L in 4N. This is an exact finite family and normalized source gap,
not a native interlevel admission or continuum-solution nonuniqueness theorem.

The witness also survives **eliminating both auxiliaries from the readout**.
At q=eta, invertibility of M0 forces chi=M0^-1 K0 psi and lambda=-chi.
For the displayed psi, these are exactly the fields above; no alternative
auxiliary root removes (7). Theta=0 therefore admits the physical point
(q,D,psi) to its joint gate, whereas theta=1 admits none above that point.
This is a stationary/source distinction, not merely unequal off-shell values.

In fact its entire joint gate is classified, not just that witness. At each
site write a=1+theta f(q)/8 and pair components as psi=(p,p_even),
chi=(x,y), lambda=(u,v), with eight entries in each group. The full field
equations are

```text
u+v=0,   a(x+u)=0,   y+v=0,   a x=p,   -y=p.
```

A native raw-metric variation with D f[V]=1 exists by the complete tangent
image. Its genuine background equation is
theta(1/2 ||x||^2+u^T x)=0. If a=1, the field equations give u=-x and
this becomes -theta ||x||^2/2=0. If a!=1, the field equations give
(a-1)p=0, hence p=y=u=v=0, and the background equation is
theta ||x||^2/2=0. Thus for **every theta!=0**, including the singular
case a=0, all and only joint roots have

```text
p=0, chi=lambda=0,      p_even arbitrary,
all nondegenerate backgrounds arbitrary.
```

For theta=0 every psi is allowed, with chi=M0^-1 K0 psi and lambda=-chi,
and every background is stationary. The compiled all-size block theorem
proves the nonzero-theta necessity; substitution gives sufficiency in both
classes. The local native lift and inverse exterior reading assemble the
sitewise equations over every periodic carrier. The eight surviving matter
components are nongauge response-null fields, not physical mode counts.
Thus theta changes the projected full stationary set at zero; no auxiliary
observation or off-shell inequality is needed for that conclusion. This is
still the stated supplied parent family, not the complete physical D0 theory.

The matrices are indefinite. The nonzero theta root has no neighboring
continuous continuation in its displayed field direction; the previously
proved parent continuation and positive-source theorems are respected.
Actual cubical differentials, locality of a selected physical star, a native
history action, refinement and physical Ward are not inferred from this
supplied-operator instance. Other constraints can restrict this interface
only when their owners and admission are supplied.

## 6. The remaining G0 target is now an observable parent law

The raw four maps need not be uniquely selected before G0 proceeds. Their
visible M,K, the complete kernel/source class (6) for a full readout, or C_X
for the stated weaker readout determines this parent's stationary/source
correspondence. The native history/record law must derive the appropriate
class and its physical metric/connection/matter preparation and refinement.
On-shell equivalence alone does not determine off-shell action contrasts:
the later calibrated finite-probe transfer still requires the owned action
or a proved equivalence preserving those actual probes. Full covariance
alone gives the entire seed family above and can admit a genuine difference
in the full joint gate; off-shell coefficient freedom alone did not prove it.

This is a complete result for the stated existing moving-parent interface,
not proof that every D0 physical system uses it or that all core constraints
are exhausted by its four supplied slots. No G0/full-core obstruction, source
fit, positive Einstein dynamics, native recovery or original #310/#202/#317
terminal is claimed. The first remaining lemma must link actual native
histories/composition to the stationary/source class, not select raw operators
that act identically on the entire admitted stationary correspondence.

Evidence: [Lean capsule](certificates/a4d_native_parent_law.lean),
[compiler output](certificates/a4d_native_parent_law_output.txt),
[source receipt](certificates/a4d_native_parent_law_results.json),
[exact checker](certificates/a4d_native_parent_law_check.py),
[immutable ledger](certificates/a4d_native_parent_law_certificate.json).

Twenty-three propositions compile against 52 transitive D0 source pins,
with only propext, Classical.choice and Quot.sound. Fifteen actual theorem
types and the two consumed exterior-lift types are printed. The all-size
joint equations are classified in both directions, with the zero-parameter
class separately compiled. The 139 exact controls bind the literal action
to all field/source equations, include all ten metric components and all
24 Lorentz link directions, and retain the singular a=0 class and every
nongauge surviving component. The 21 false-scope ledger mutations are
rejected independently. Orbit descent, rank-factorization completeness,
global smooth-factorization obstruction and projected quadratic-image
assembly have the explicit analytic proofs above; their full all-site
versions are not advertised as compiled.
