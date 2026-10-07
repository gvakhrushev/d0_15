# Native homogeneous matter sources and complete positive quadratic jets

Input: `20928b17563fc1d840bbc204ced7c3fd28610175`, existing #310.
Supported D0 tree: `fd8dfc359d23c9bd79ca23eeed7c045ce9c68c6b`.
Status: **complete source theorem for the declared locally nonnegative
homogeneous field-action class, and complete positive quadratic jet
classification**. G0, physical matter/Ward, positive GR and global closure
remain OPEN. No action, positivity postulate or field constraint is installed.

The [joint field quotient](A4D_NATIVE_JOINT_FIELD_QUOTIENT.md) supplies actual
states and admissible tangents. The [mixed-parent source theorem](A4D_NATIVE_PARENT_SOURCE_BOUNDARY.md)
already proves zero source for its positive scalar form and retains genuine
indefinite-source roots. This result consumes both. It treats arbitrary
nonlinear background dependence, positive semidefinite forms and rank changes;
it is not another fixed-weight or fixed-frame test.

## 1. The complete class and independent field gate

Let X be any admitted background, including raw coframes, actual links and
affine shifts. Let z comprise all independently varied matter/auxiliary fields.
Along each admitted two-sided background curve X(t), set I(t,z)=I(X(t),z).
Assume precisely:

1. The field variation z+s z is admitted. Full field stationarity annihilates
   the actual derivative in every admitted independent field direction.
2. I(0,a z)=a^p I(0,z) near a=1 for some p>0.
3. At the same fixed z, I(t,z)>=0 for sufficiently small positive and negative t.
4. The genuine fixed-field derivative sigma=partial_t I(t,z)|_0 exists.

Neither stationarity of a normalized field nor a zero totalized derivative at
a nondifferentiable point is used. The gate contains field derivatives only;
it does not include zero source or an Einstein residual.

**Theorem.** Every full field root in this class has I(0,z)=0 and sigma=0
for every admitted background curve.

Proof: radial differentiation gives d_z I[z]=p I. The independent field gate
sets this derivative to zero, hence I=0. At fixed z, t=0 is now a local
minimum of the actual scalar I(t,z). A genuine two-sided derivative there is
zero. No inverse, root continuation, locality, fixed rank, finite polynomial
degree in X or field-frame factorization is needed.

The compiled theorem allows every positive integral degree; the analytic
argument also covers real p>0 with homogeneity for positive a. All metric,
connection and other background covectors are covered when their native
curves meet these hypotheses. Positivity need only hold along each such
curve, not on arbitrary ambient extensions of the constrained quotient.

A primitive ActionProtocol cost being nonnegative does not prove hypothesis
3 for an effective field action after recording, subtraction or a limit.
The direct primitive variational boundary remains consumed, not bypassed.
A Lorentzian indefinite action, complex action, nonhomogeneous potential or
an independently owned constraint excluding radial variations lies outside
this theorem. No such escape is silently introduced.

## 2. Literal quadratic owner, including nonzero kernel matter

For a symmetric real matrix M(X), write

```text
I(X,z)=1/2 z^T M(X) z.
```

This is the literal `squaredFluxEnergy alpha H z` when
M=`kernelPoly alpha H=1+H+alpha H^2`. The capsule compiles that binding,
the exact field-variation polynomial, its HasDerivAt statement and

```text
full field gate  <=>  M(X)z=0.
```

For any locally positive semidefinite M(X), every such root has zero source.
Nonzero kernel matter is retained; zero source does not mean z=0 or that
the operator's derivative vanishes.

The actual owner's complete-square identity is

```text
2 squaredFluxEnergy alpha H z
  = ||z+H z/2||^2 + (alpha-1/4)||H z||^2,   H^T=H.
```

Thus alpha>=1/4 supplies the required nonnegativity on any native curve
where symmetry and that inequality persist. This statement and its
source consequence are compiled, including background-dependent alpha and H.
For alpha>1/4, full roots are zero fields by the existing strict positivity
theorem. At alpha=1/4 the full kernel is H z=-2z and may be nonzero.
The statement is about the existing supplied-operator action family; it does
not select H(X), alpha, a Lorentz-covariant binding or a physical refinement.

The mixed parent action is generally indefinite even when its scalar block
M is positive. It is not identified with this nonnegative action. Its
indefinite source/radical and no-continuation controls remain valid.

## 3. Every positive quadratic first jet, with arbitrary rank

Let M(t) be C1, symmetric and positive semidefinite on a two-sided interval.
At t=0 split the field space orthogonally into range and kernel:

```text
M0 = [ A  0 ],    A>0,
     [ 0  0 ]

B=M'(0) = [ B11 B12 ].
          [ B12^T B22 ]
```

For every kernel vector v, v^T M(t)v>=0 with value zero at t=0. Section 1
gives v^T Bv=0. Polarization gives **B22=0**. Cross blocks B12 need not vanish.

Conversely every symmetric B with B22=0 is an actual admissible first jet.
Choose

```text
X = [ (1/2) A^-1 B11   A^-1 B12 ],
    [          0              0 ]
M(t)=(I+tX)^T M0(I+tX).
```

This polynomial is positive semidefinite for all real t and has derivative B.
With support projection P and support inverse G, the same explicit formula is
X=G B-(1/2)G B P. The capsule compiles M0 X+X^T M0=B whenever
M0 G=G M0=P, P and G are symmetric and (I-P)B(I-P)=0.
The analytic range/kernel split supplies exactly those hypotheses.

Hence this is the **entire** positive first-jet class, not a sampled list.
For n field coordinates and kernel dimension k its dimension is
n(n+1)/2-k(k+1)/2. For all sixteen matter components n=16; at each rank r
the dimension is r(33-r)/2. These are constitutive-jet dimensions, not
propagating physical degrees of freedom.

For several background coordinates, every collection B_i satisfying the
same kernel compression condition has the common polynomial realization
M(t)=(I+sum_i t_i X_i)^T M0(I+sum_i t_i X_i).
Thus arbitrary metric and link first jets can be treated simultaneously.
No uniform bound on X_i follows when the positive eigenvalues of A collapse.

## 4. Complete second jets and why rank changes survive

Let C=M''(0). A necessary and sufficient condition for a C2 positive
semidefinite curve with prescribed (M0,B,C) is

```text
B22=0,    C22-2 B12^T A^-1 B12 >= 0.                 (1)
```

Necessity: the range block A(t) stays positive definite near zero.
Its Schur complement is nonnegative and expands as

```text
M22(t)-M21(t) A(t)^-1 M12(t)
  = (t^2/2)(C22-2 B12^T A^-1 B12)+o(t^2).
```

Sufficiency is constructive. Take X above, set
S=C22-2 B12^T A^-1 B12>=0 on the kernel and zero elsewhere.
The symmetric matrix T=C-2 X^T M0 X-S has zero kernel block.
Apply the first-jet inverse to T, obtaining Y with M0 Y+Y^T M0=T.
Then

```text
R(t)=I+tX+(t^2/2)Y,
M(t)=R(t)^T M0 R(t)+(t^2/2)S
```

is positive semidefinite for every t and has exactly the requested first
two derivatives. S>0 on a kernel direction allows the rank to increase
at order two. Constant rank and a continuous nonzero-root branch are not
assumed.

For several parameters the corresponding condition is positivity, for
every parameter vector u, of
C22[u,u]-2 B12(u)^T A^-1 B12(u).
The same polynomial construction with X(u), quadratic Y(u) and this
nonnegative quadratic matrix S(u) proves sufficiency. Testing only the
coordinate axes does not establish that condition. No sum-of-squares
representation of every positive matrix polynomial is asserted.

Both all-rank jet classifications are analytic explicit constructions.
The first-jet inverse is additionally compiled. Finite examples certify
the algebra and negative controls, not an extrapolation to all dimensions.

## 5. Approximate field roots require actual uniform action bounds

Let f(t)=I(X(t),z)>=0 on [-r,r], E=f(0), and |f''|<=K there.
Taylor's theorem with its upper remainder gives for every 0<s<=r:

```text
|sigma| <= E/s+K s/2.                                  (2)
```

The finite inequality from the two Taylor bounds is compiled. The actual
C2 hypothesis and constants are separate analytic premises. For E>0 and K>0, choosing s=sqrt(2E/K) when it is <=r gives
sqrt(2KE); otherwise s=r gives E/r+K r/2. When K=0 use E/r;
when E=0 the exact local-minimum theorem gives zero source. For fixed r
and uniformly bounded K, E->0 implies sigma->0. Radial homogeneity gives
p E=d_z I[z], so bounded fields and vanishing full field residuals imply
E->0 when p is fixed positive or uniformly bounded away from zero. Required quantitative rates must be
proved from the admitted native action/preparation; the state quotient
alone supplies no uniform action-derivative bound.

A hostile smooth positive family shows why this matters. For h>0 put

```text
w_h(t)=h^2 (2+2(t/h^2)/(1+(t/h^2)^2)),
I_h(t,z)=1/2 w_h(t) z^2.
```

Globally h^2<=w_h(t)<=3h^2. At t=0,z=1 the actual field residual is
2h^2, the action is h^2, but the source is **1 for every h**.
Even uniform operator-value convergence to zero does not control the source.
The action jets vary on the scale h^2; a required second-derivative bound
fails.
The background parameter can be an actual metric curve
Q(t)=diag(1+t,-1,-1,-1), |t|<=1/2: use identity links and the uniform raw
frame F(t)=diag(sqrt(1+t),1,1,1). Its literal transported center is F(t),
and the raw/dressed data satisfy the joint constraints. The scalar exterior
matter component is unchanged by this frame lift. These state preparation
bounds are uniform; the rapidly varying supplied action weight causes the
failure. Its positivity and full matrix rank do not supply a uniform jet
bound or a selected physical matter law. These are approximate roots, not counterexamples to the exact-root
theorem. At the actual half-contrast scale epsilon=h^(1/3),

```text
Delta I_h=epsilon/(1+epsilon^2/h^4),
Delta I_h/epsilon -> 0,       sigma_h=1.
```

With h=n^-3 this normalized contrast is exactly 1/(1+n^10).
Thus point derivatives cannot be exchanged with this joint refinement/probe
limit merely because operator values and field residuals converge to zero.
The quantitative contrast requirement needs its own preparation bounds.

## 6. Essential negative controls and the next native obligation

One-point positivity is insufficient: I(t,z)=t z^2 has a full field root
at t=0,z=1 and source 1. A one-sided background domain also permits that
source. Restricting z^2=1 removes the radial variation: (1+t)z^2/2 has
constrained stationary matter and source 1/2.

Nonhomogeneous nonnegative actions can have nonzero source at full roots.
For |t|<1 use I(t,z)=(1+t)z^2((z^2-2)^2+1).
At t=0,z=1 the field derivative is zero, the energy is 2 and the
source is 2. This is an interface control, not a selected D0 action.

At M0=diag(1,0), the family M(t)=[[1,t],[t,t^2]] has a nonzero kernel
root and zero source, but B maps that kernel vector to a nonzero range
vector. Dropping cross blocks, declaring kernels gauge, or freezing the
operator is therefore invalid. Rank-changing positive examples likewise
prevent inferring root recovery from the zero-source theorem.

The prior standalone zero-field/non-Einstein branch is already proved in
[A4D_NATIVE_CENTERED_METRIC_LIFT.md](A4D_NATIVE_CENTERED_METRIC_LIFT.md#6-a-genuine-native-zero-field-root-family-with-a-non-einstein-limit);
it is consumed, not counted as a new result. Zero matter source does not
exclude curved vacuum Einstein solutions and does not derive their equations.

G0 must still derive an independently owned coupled action, its genuine
admitted variations and native refinement. Any proposed nonzero source
from a locally nonnegative homogeneous full-free-field action now contradicts
this complete theorem. An escape must be an actual owned feature of that
action or its admitted sector, not a fitted stress or an imposed new gate.
Physical Ward, native contrast, joint curved solutions, soundness/recovery
and all original #310/#202/#317 terminals remain open.

Evidence: [Lean capsule](certificates/a4d_native_positive_source.lean),
[compiler output](certificates/a4d_native_positive_source_output.txt),
[source receipt](certificates/a4d_native_positive_source_results.json),
[exact checker](certificates/a4d_native_positive_source_check.py) and
[immutable ledger](certificates/a4d_native_positive_source_certificate.json).

Validation: 18 resolved Lean propositions, 40 transitive D0 source pins and
114 exact controls. The output prints the actual source hypotheses, field
kernel equivalence, owner binding and inverse conditions. The finite joint
controls use all sixteen nonzero matter components, the literal exterior
lift, Cayley Lorentz links and the actual transported center. Their ten
metric curves have exactly unit physical packed-component derivatives;
all 24 link variations are retained. Those operator bindings are test
instances of the supplied action family, not a selected native law.
