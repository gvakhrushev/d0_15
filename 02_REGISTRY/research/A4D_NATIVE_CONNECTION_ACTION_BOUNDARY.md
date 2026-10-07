# Existing connection actions: the missing metric dependence

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input: `59fef13f804d4c5706ef86fe6df01a53f214c565`.
Status: **complete obstruction for the explicitly specified coframe-blind
factorization class**, not a no-go for the D0 core. Positive native GR,
source, recovery and the original parent terminals remain OPEN.

The [native link/readout construction](A4D_NATIVE_TRANSPORTED_CONNECTION_REALIZATION.md)
supplies actual affine Lorentz links and smooth corrected metrics. It does
not select a scalar action. This follow-up tests existing scalar connection
functionals against that construction. It adds no action or physical gate.

## 1. What the actual owners say

| Owner | Actual scalar and arguments | Variations and boundary |
|---|---|---|
| `Gauge.YangMillsKillingPositivity` | `discreteYangMillsAction Killing K = -sum Killing(K_ab,K_ab)`; both `K` and the function `Killing` are supplied | The type of `Killing` alone does not require bilinearity, Lie invariance or negative definiteness. The positivity theorem explicitly assumes every diagonal value is nonpositive. No coframe, lattice connection or matter variation is defined there. |
| `Gauge.MatrixRepGaugeTransform` | `matrixRepYangMillsAction K = -sum Tr(K_ab^2)` for supplied matrix entries | The capsule binds this literally to the preceding formula with `Killing(X,Y)=Tr(XY)`, proves its quadratic polarization and derivative, and retains the Euclidean-skew hypothesis of positivity. |
| `Gauge.NonAbelianSeamObstructionGap` | `seamEnergy B X = ||[B,X]||_F^2` for a supplied `FiniteSeamMap B` | Nonnegativity and the exact degree-two scaling are genuine. Neither a physical `B(g)` nor a native link-to-`X` map is supplied by this owner. |
| `Algebra.GaugeKineticPositivity`, `Matter.VectorOperatorOrigin` | `-c Tr([D,A]^2)` on the stated skew matrix carrier | Its literal full field gate, source range and background response are already [classified](A4D_NATIVE_VECTOR_SOURCE_BOUNDARY.md). Keeping supplied `D` and `A` unchanged cannot generate a new metric variation. A coframe-dependent `D` is outside the class below. |

The declaration
`exact_bianchi_identity_replaced_by_graded_incidence_closure` in the second
owner has the actual proposition that `[D,A]` is skew if `D` and `A` are
skew. It does not assert a covariant divergence identity. Its real type is
printed alongside the positivity hypotheses in the capsule.

Two other tempting names do not give additional scalar actions:
`resolvedCorrelatedAction` is the linear map `S.comp proj`, and
`AffineSolderOriginAction` specifies an action on solder/origin data.
The existing relative-solder classification and #202 are unaffected.

The accepted [star insertion classification](MEMO_A4D_ROLE_BIVECTOR_INSERTION_UNIQUENESS.md)
is also preserved: inside its oriented density class, linear in curvature
and quadratic in solder, the insertion is unique up to scale. That is a
different scalar with explicit solder dependence. No result below excludes
it or proves its equality with one of the native functionals above.

## 2. The complete class being tested

At one mesh h use the native data `(F,R,z)`, where F is the full raw solder,
R the actual Lorentz pull-link field and z any other retained variables.
Take precisely the factorization

\[
 I_h^N(F,R,z)=\Phi_h(R,z).                                  \tag{1}
\]

The class permits arbitrary nonlinear/nonlocal functions Phi, arbitrary
mesh factors, indefinite values, coefficients and spectator variables. It
does not assume positivity, polynomiality, convexity, a unique link root,
or any continuum expansion of Phi. For this test the admitted raw probes
include a small interval of uniform positive scalings of F with `(R,z)`
held fixed. This admission is an explicit hypothesis, not inferred from
the mere existence of a readout. A scalar native functional with metric
weights, coframe-dependent operator, metric-dependent retained variable,
or an additional constraint forbidding these probes is outside (1).

The three functionals in Section 1 are in this class **if** their supplied
arguments are functions of `(R,z)` only. For example one may test the
already constructed odd based curvature

\[
 C_{rs}(R)=(P_{rs}(R)-P_{rs}(R)^{-1})/2
\]

as the argument K of the existing matrix action. This is a specified
mathematical binding for the test, not a claim that its owner already
selects K, nor a replacement action installed in D0. The obstruction holds
for every other coframe-independent binding too.

Write the actual transported center and its Gram readout as

\[
 T_R(F)_r(x)=\tfrac12\{F_r(x)+F_r(x-r)R_{x-r,r}\},\qquad
 Q(F,R)=T_R(F)\eta T_R(F)^T.                              \tag{2}
\]

Linearity, directly on the actual owner, gives

\[
 T_R(cF)=cT_R(F),\qquad Q(cF,R)=c^2Q(F,R).                 \tag{3}
\]

Thus for `F_t=sqrt(1+t) F`, `|t|<1`, the **actual finite** metric is
`Q_t=(1+t)Q`, while (1) is exactly constant. In particular its half-contrast
and derivative in this allowed probe both vanish. The capsule proves (3)
and the general factorization consequences; no surjectivity of the full
finite metric/link differential is assumed.

## 3. A curved prepared experiment with a quantitative contradiction

Use the already pinned periodic metric

\[
 f(y_0)=1+\tfrac1{10}\cos(2\pi y_0),\quad
 \Theta=f\eta,\quad E=\eta\Theta^T=fI,\quad g=f^2\eta.
\]

It is nondegenerate with `9/10<=f<=11/10`, has nonzero curvature, and in
the existing owner's curvature convention

\[
 I(g)=\tfrac12\int\sqrt{|g|}R[g]
     =-3\int_0^1(f')^2\,dy_0=-3\pi^2/50=:I_*\ne0.          \tag{4}
\]

This is an explicit non-Einstein vacuum probe, not asserted to be a native
solution or a solution with an independently generated nonzero source.
The full earlier curvature calculation, sign and packed convention are
retained; the new checker independently rechecks the integral and all ten
homothetic Gram slots.

Constant metric scaling `g_t=(1+t)g` leaves the Levi-Civita Christoffel
symbols unchanged: the inverse metric factor cancels the factor in each
metric derivative. Scaling E by the same constant square root leaves
the spin connection omega unchanged too. No equality for *spatially
varying* conformal scalings is claimed.

For `L in 4N`, `h=1/L`, use the actual previous preparation

\[
 R_{h,r}(x)=C(h\omega_r(hx)),\qquad
 F_{h,r}(x)=\Theta_r(hx+he_r/2)C(-h\omega_r(hx)/2),
 \quad C(Z)=(I-Z/2)^{-1}(I+Z/2).                           \tag{5}
\]

Its full affine native linear part acts by R, in the verified pull
orientation. Fix the retained affine shifts and z independently of t.
Set `F_h(t)=sqrt(1+t) F_h(0)` and keep R fixed. Equation (3) yields exactly

\[
 Q_h(t)=(1+t)Q_h(0),\qquad Q_h(0)=g+O_{C^k}(h^2).          \tag{6}
\]

These are nonempty native readout fibers, with preparation bounds from
the displayed smooth fields. They need not solve additional native
field/interlevel equations. In the existing physical naked-star action
every face weight is quadratic in E. Consequently at the **same finite
links**, both its action and every one of its 24 connection Euler rows
scale by `1+t`. The previously proved all-row `O(h^2)` residual therefore
holds throughout a fixed small t interval, with one uniform bound. This
step checks all shared-link positions; it does not identify the residual
bound with exact stationarity.

Let `I_h^star(t)=h^2 A_h(E_h(t),R_h)`. The previous smooth preparation
estimate and the exact scaling imply

\[
 I_h^\star(0)=I_*+O(h),\qquad
 I_h^\star(t)=(1+t)I_h^\star(0).                          \tag{7}
\]

With the half-contrast convention `Delta I=(I(+eps)-I(-eps))/2`,

\[
 \Delta I_h^N=0,\qquad
 \Delta I_h^\star=\epsilon I_h^\star(0).                  \tag{8}
\]

For every fixed nonzero calibration a, sufficiently small h and positive eps,

\[
 |a^{-1}\Delta I_h^N-\Delta I_h^\star|
 \ge \tfrac12|I_*|\epsilon.                              \tag{9}
\]

In fact a mesh-dependent scalar multiplier cannot change a zero contrast.
At `eps=h^(1/3)` the sharper prepared estimate is

\[
 \Delta I_h^\star=-\frac{3\pi^2}{50}h^{1/3}+O(h^{4/3}).     \tag{10}
\]

If calibrated recording and refinement errors in the compared
half-contrast have total absolute size at most `C_err h`, the lower bound
is `|I_*|h^(1/3)/2-C_err h`, hence at least `|I_*|h^(1/3)/4` for small h.
It cannot be bounded by `C_V h`. Equivalently, the normalized centered
contrast has native value zero and physical limit `I_*`, not an error
`O(h^(2/3))`.

**Theorem.** Every factorization (1) admitting the prepared probes (5)--(6)
fails the requested calibrated `O(h)` contrast transfer. This includes
every coframe-independent binding of the existing Section 1 functionals,
regardless of their coefficients or positivity. The theorem concerns
prepared contrasts, not exact native roots. Prohibiting the displayed
probes requires an independently owned constraint and a replacement
metric-variation/recovery proof; it does not follow from (1).

## 4. Native stationarity and auxiliary choices are separate

For (1), all free raw-coframe Euler rows vanish identically off shell.
Thus this action by itself cannot impose a ten-component metric equation
through its coframe derivative. At any solution of its independent `(R,z)`
gate, every admitted F remains a coframe root. Existence of such link
roots, nondegeneracy of their readout and interlevel admission must still
be checked. We do not declare the smooth Levi-Civita data (5) on shell.

At fixed R suppose an auxiliary gate depends only on `(R,z)` as well.
The complete set

\[
 \{\Phi_h(R,z): z\text{ satisfies that gate}\}
\]

is the same for every F. This exact set statement is compiled and does not
assert uniqueness or even nonemptiness. If a differentiable family of
auxiliary roots satisfies the actual auxiliary first variations of Phi,
then `d Phi(R,z(t))/dt=0` by the chain rule, so its value is constant on
each connected interval. The latter calculus argument is analytical.
An arbitrary selection between disconnected root values is neither this
theorem nor a metric response derived from the auxiliary equations. No
selection rule is silently added.

Adding a term with independent coframe dependence can change the argument.
The old standalone flux zero-field example is one already proved instance
where that dependence contributes zero on the tested branch. We do not
assert that every combination with matter or constraints has this property.

### 4.1 A nonempty native critical set for the specified curvature binding

There is a stronger gate test for the particular, completely described
binding of the existing matrix action to `C(P(R))`. Its variables are free
raw F and independent Lorentz links R; its scalar is the unchanged
`matrixRepYangMillsAction` evaluated on all six odd based curvatures per
site. Its equations are its actual derivatives in all raw directions and
all six Lorentz tangents of every link. No matter or interlevel constraint
is added. This is an analyzed realization class, not a selected core law.

Set every `R=I`. Then every `C=0`. The literal derivative
`-2 sum Tr(C dC)` vanishes for every link tangent. The coframe derivative
vanishes by (1). These are exact full roots of this stated finite gate,
with value zero. The capsule proves zero derivative along every
differentiable zero-curvature path, not merely along independent affine
curvature variations. Inversion and matrix products are smooth near the
identity, so the actual Lorentz link paths satisfy its hypothesis.

Take `F_h,r(x)=Theta_r(hx+h e_r/2)` with the same Theta as Section 3.
This is the actual R=I specialization of the earlier midpoint lift:
its Gram is `g+O(h^2)`, so these exact native roots have the curved,
non-Einstein limit (4). No source was fitted to this metric. Consequently
metric Einstein-vacuum soundness fails for this full **levelwise binding
and readout class**. Additional native constraints or a narrower admitted
solution class are outside this statement.

It also shows why native stationarity cannot be substituted for the
physical preparation premise. In the physical star Euler stencil, test
one spatial link `r=1` in the actual generator
`G_01=(E_01-E_10)eta=-B_01`. At the identity links the two adjacent `(0,1)`
face weights give exactly

\[
 E_{1,G_{01}}(x)=f(hx_0)^2-f(hx_0-h)^2.                   \tag{11a}
\]

All four link positions are retained in this calculation. Complementary
solder legs are spatial, so the corrected temporal midpoint leg does not
alter (11a). At the fixed physical point `hx_0=1/4`, which is present for
every `L in 4N`,

\[
 h^{-1}E_{1,G_{01}}\longrightarrow 2f(1/4)f'(1/4)
 =-2\pi/5\ne0.                                          \tag{11b}
\]

Thus the all-24-row physical residual cannot be `O(h^2)`. The exact L=4
row at `x_0=0` is `21/100`, and all 24 row formulas are checked. This is
a native on-shell counterexample to the implication into that physical
preparation domain, for the stated binding. It is deliberately distinct
from the smooth Levi-Civita prepared family (5), whose native stationarity
is not asserted. A source term, coframe coupling or native torsion equation
would change the tested system and needs its own existing owner.

## 5. The Euclidean positivity theorem cannot supply Lorentz dynamics

Write every real eta-skew 4x4 matrix uniquely as

\[
 K(b,r)=\begin{pmatrix}
 0&b_0&b_1&b_2\\
 b_0&0&r_0&r_1\\
 b_1&-r_0&0&r_2\\
 b_2&-r_1&-r_2&0
 \end{pmatrix}.
\]

The literal singleton matrix action is

\[
 -\operatorname{Tr}K^2=2(\|r\|^2-\|b\|^2).               \tag{11}
\]

The capsule proves the eta-skew condition, all-six-variable formula,
and that Euclidean skew is equivalent to `b=0`. Thus the positive compact
owner hypothesis discards three of six Lorentz directions per link;
on four links it discards 12 of the 24 connection directions. No such
restriction is part of the accepted all-24-row physical preparation.

The supplied trace pairing has a boost with positive diagonal value 2,
so the hypothesis `Killing(X,X)<=0` is false on this Lorentz class. Its
restriction (11) is nondegenerate of signature `(3,3)`. Its full
independent-curvature critical gate is nevertheless `K=0`, because all
six derivatives vanish only there. This does not solve the composed
nonlinear link gate, which tests derivatives through the curvature map.

For `b_0=r_0=1`, other coordinates zero, K is nonzero and nilpotent,
has zero action, but the derivative in b_0 is -4. Zero value is therefore
not stationarity. Nor can the action be changed to the Euclidean
Frobenius square without changing its symmetry. For the proper Lorentz boost

\[
 U=\begin{pmatrix}5/3&4/3&0&0\\4/3&5/3&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix}
\]

and the spatial rotation `K=J_12`,

\[
 -\operatorname{Tr}(UKU^{-1})^2=-\operatorname{Tr}K^2=2,
 \quad \|K\|_F^2=2,\quad \|UKU^{-1}\|_F^2=82/9.            \tag{12}
\]

This rejects a fixed Euclidean positive replacement. A jointly transforming
observer/constitutive field is an explicit different class and remains
outside the test. Finite Lorentz trace invariance is not physical Ward
conservation or a source-generation theorem.

### 5.1 Every invariant quadratic coefficient is classified

The indefinite trace is not repaired by a different invariant quadratic
coefficient. Use boost coordinates b and rotation coordinates
`j=(r_2,-r_1,r_0)`. Invariance under all three spatial rotations forces a
real symmetric quadratic form to have blocks `alpha I`, `beta I`,
`gamma I`: an invariant 3x3 bilinear form has zero off-diagonal entries
under half-turns and equal diagonal entries under quarter-turns.
Infinitesimal invariance under the three boost generators then forces
`gamma=-alpha`. Conversely the two resulting forms are the trace and
oriented bivector pairing, both invariant under the proper Lorentz action
in the accepted insertion owner. The complete family is therefore

\[
 q_{\alpha,\beta}(b,j)=
 \alpha(\|b\|^2-\|j\|^2)+2\beta\,b\cdot j.               \tag{12a}
\]

The exact six-generator calculation on all 21 symmetric coefficients
has rank 19 and this two-dimensional kernel. After grouping `(b_i,j_i)`
the form is three copies of `[[alpha,beta],[beta,-alpha]]`. Every nonzero
pair `(alpha,beta)` has signature `(3,3)`; only the zero pair is positive
semidefinite. The last implication is compiled for arbitrary real
coefficients, and the exact symbolic certificate checks the complete
invariant space and block identity. This classifies coefficient repair,
not an added physical action family. An observer-dependent form is not
invariant under these transformations with its observer held fixed and
remains outside the class.

### 5.2 Nonlinear positive repair still has a full invisible sector

This argument does not require a quadratic action. On one fixed finite
lattice take a scalar `Phi(R)` continuous at the identity link field,
invariant under simultaneous constant proper-Lorentz conjugation. An
additional retained z is permitted only if it is held invariant under this
action and Phi has the same invariance at that z. No positivity is needed
yet. Define

\[
 N=B_{01}+J_{12},\qquad N^3=0,\quad N\ne0,
 \qquad U(a)=I+aN+\tfrac12a^2N^2.
\]

Exact identities give `U(a)U(b)=U(a+b)`, `U(a)^{-1}=U(-a)` and
`U(a)^T eta U(a)=eta`; these matrices lie in the identity component via
the displayed real a path. For every q>0 put

\[
 B(q)_{\{0,2\}}=
 \begin{pmatrix}(q+q^{-1})/2&(q-q^{-1})/2\\
 (q-q^{-1})/2&(q+q^{-1})/2\end{pmatrix}
\]

and use the identity on the other two coordinates. It is proper Lorentz
and `B(q) N B(q)^{-1}=N/q`. Consequently for **arbitrary real edge data**
`a_r(x)`, not a searched collection of modes,

\[
 R_{x,r}=U(a_r(x)),\qquad
 B(q)R_{x,r}B(q)^{-1}=U(a_r(x)/q)\longrightarrow I.          \tag{12b}
\]

Finiteness of each lattice gives simultaneous convergence of every link.
Invariance and continuity at the identity now imply the exact value law

\[
 \boxed{\Phi(R)=\Phi(I)\quad\text{on this entire sector}.}   \tag{12c}
\]

The generic continuity implication is compiled; the actual Lorentz
contraction is an exact rational-symbolic identity in q. Equation (12c)
allows nonlocal functions and joint-holonomy aggregation. It does not
identify these configurations with the flat gauge orbit. Indeed a face
has

\[
 P_{x,rs}=U(c_{x,rs}),\quad C(P_{x,rs})=c_{x,rs}N,
 \quad c_{x,rs}=a_r(x)+a_s(x+r)-a_r(x+s)-a_s(x).             \tag{12d}
\]

A nonzero c gives nonidentity holonomy, which no gauge conjugation makes
the identity. The checker retains exact curved faces on a periodic
lattice. Smooth `a_{h,r}=h A_r(hx)` also give log-O(h) links and
`h^{-2}C(P)->(partial_r A_s-partial_s A_r)N`; the phenomenon is not
restricted to grid-scale oscillations.

If one additionally assumes differentiability and the global lower bound
`Phi(R)>=Phi(I)`, every state (12b) is a minimum and hence a full link
critical point along every Lorentz tangent. In the coframe-blind class,
all free coframe equations vanish as well. Thus such a positive repair
retains an entire nongauge curved stationary sector and arbitrary metric
readouts; strict flatness detection and unrestricted Einstein soundness
do not follow. The positivity premise is essential: the existing trace
square is indefinite, and its null value need not be stationary, as the
compiled -4 derivative in Section 5 shows.

This result is for the explicitly projected connection-only action.
It does not contradict properness of the joint nondegenerate solder/link
quotient: the same boosts also transform its solder, which is absent from
Phi and need not stay bounded. Coupled coframe/observer/matter dependence,
constraints and noncontinuous actions lie outside this theorem. No full
classification of the nonlinear critical set of the indefinite matrix
action is asserted.

### 5.3 The actual indefinite action: full gate on the whole null sector

For the literal matrix action bound to odd plaquettes, its full gate can
be classified on every field (12b), without mistaking the identically
zero restricted action for a stationary solution. Let `D a=c` be the
real periodic edge-to-face curl in (12d), with the counting transpose
`D^*`. The source is absent; all six Lorentz tangents of every link are
tested, including directions transverse to N.

Vary one link by a left tangent G. Its contribution to a containing
plaquette has the form
`delta P=+/- U(p) G U(c-p)` for a real prefix p. Since N commutes with
every U, the literal trace derivative of that face is exactly

\[
 -2\operatorname{Tr}(C\delta C)
 =-\operatorname{Tr}\{(C+P^{-1}CP^{-1})\delta P\}
 =\mp2c\operatorname{Tr}(NG).                             \tag{12e}
\]

Here `C=cN`, `P+P^{-1}=2I+c^2N^2`, and `N^3=0` remove every higher term.
The identity is checked symbolically for arbitrary p,c and all six
generators, with both edge orientations. Summing every incident face,
the exact link Euler row is

\[
 E_{x,r,G}=-2\operatorname{Tr}(NG)(D^*D a)_{x,r}.            \tag{12f}
\]

The trace covector is not zero, for example `Tr(N B_01)=2`. Thus **all**
full link equations vanish iff `D^*D a=0`. Pairing this real scalar
equation with a gives the finite exact identity

\[
 \langle a,D^*D a\rangle=\sum_{x,r<s}c_{x,rs}^2.
\]

It follows, at every finite size, that

\[
 \boxed{\text{full matrix-action gate on (12b)}
       \ \Longleftrightarrow\ D a=0
       \ \Longleftrightarrow\ P_{x,rs}=I\text{ on all faces}.} \tag{12g}
\]

This is a complete criticality classification on the stated common-N
sector, not on all Lorentz links. Flat global holonomies are not removed
by the local equation and are not declared gauge. The certificate builds
the entire L=2 curl matrix, checks its rank 45 and its normal-equation
kernel, and verifies nonzero full Euler rows on the single-edge curved
zero-value control. The general result uses (12e)--(12g), not rank
extrapolation from L=2.

Thus the indefinite existing action and a proposed positive invariant
repair have different gates: positivity in Section 5.2 would make the
whole curved sector stationary, whereas this actual full gate removes
its curvature. Restricting variations to the null sector would hide all
these transverse equations and give a false criticality result. This
control preserves the user's requirement to test complete equations.

## 6. Flat order provides an independent action control

For constant Lorentz generators A_r use literal `R_r=C(t A_r)`.
The four-factor plaquette gives

\[
 P_{rs}=I+t^2[A_r,A_s]+O(t^3),\quad
 C(P_{rs})=t^2[A_r,A_s]+O(t^3).                            \tag{13}
\]

The matrix curvature-square action is `O(t^4)`, with zero flat two-jet on
this homogeneous connection family. The existing naked-star action has
its nonzero quadratic connection term, whose full zero-phase Hessian
has determinant 256. Equality of the two actions on the identified
constant links, up to a fixed nonzero scale and additive constant, is
impossible even before their metric dependence is compared. This is
not a ban on arbitrary nonlinear field maps or added coframe couplings.
Equation (9), unlike this local order control, already covers arbitrary
Phi and mesh normalizations in the stated coframe-blind class.

## 7. Verification and remaining obligation

The companion capsule compiles twenty propositions: actual action instances, all-size
polarization/derivative, transported homothety, exact factorization
consequences, zero-curvature path stationarity and Lorentz six-component
facts, quadratic positivity and the generic continuous-contraction law.
Its 43 transitive D0 source pins and printed actual types
distinguish hypotheses from conclusions. The
analytic preparation and infinite-mesh estimates are not advertised as
compiled continuum theorems.

The immutable checker has 84 exact controls, including rational matrices, all ten
Gram slots, all 24 connection coefficient directions, full finite
four-factor action scaling, the conformal integral, the record-error
exponent and negative controls for Euclidean positivity, zero-value
stationarity and omitted coframe dependence. The exact zero-curvature
native gate and all 24 identity-link physical Euler rows keep their
distinct meanings. False scope ledgers must
be rejected rather than regenerated into a passing result. Eight independent
false scope ledgers are retained as rejection controls.

This closes the stated connection-only action mechanism, complementing
the earlier volume-only and standalone-flux classes. It does not exhaust
all native mechanisms. The first positive obligation remains an owned
scalar law with the required simultaneous metric/connection/matter
dependence, its actual allowed probes and quantitative contrast transfer.
The conditional star insertion, independently supplied matrix curvature,
and action-number encodings do not prove that law. Native curved
solutions, independent source, physical Ward, soundness/recovery,
refinement and the original #310/#202/#317 terminals remain open.
