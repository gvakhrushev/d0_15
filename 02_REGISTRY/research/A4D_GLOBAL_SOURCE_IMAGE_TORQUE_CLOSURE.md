# A4D global source image: all-role current and transport obstruction

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Input head: `551eba1a84fe15ebdcd100b90348f291bd109692`.
Canonical main: `e80a3b1ccf615fb4f70bf5900181592604928497`.
Status: exact all-field current identity, full-eight reduced readout bound
and scoped coframe-gradient pullback control;
fixed-source global response closure remains `PARTIAL / OPEN`.
Certificate: `certificates/a4d_full_current_transport_quotient_check.py`.

## 1. Target and quantifiers

Keep one smooth nondegenerate nonconstant metric `g`, one source `tau`,
both fixed independently of the mesh and before the connection, and the
original exact sampling, action and ten Gram covector slots. For `h=1/L`,
`Q_h=g(hx)`, the outstanding problem is

\[
E_K(Q_h,K_h)=0,\qquad \Xi(Q_h,K_h)=h^2\tau(hx),
\qquad h^{-2}\|\Xi(K_h)-\Xi(K_h^{sm})\|_{\mathrm{owner},1}\to0.
\tag{1}
\]

The owner norm is the unweighted sum of absolute values of every physical
site and all ten packed components. The comparator is the designated #216
sheet with its owned residual/section convention. Its continuum reconstruction
to `-G[g]/2` does not by itself prove (1). No source weakening, replacement
norm, selector or action change is introduced here.

For a fixed source, the normalized difference in (1) is exactly
`tau(hx)-h^-2 Xi(K_h^sm)`. Thus the scientific obligation is a constraint on
which fixed smooth sources lie in the realizable stationary source image;
it is not the mutual response of two roots of the same source equation.
The source-image owner already proves this equivalence. Existence or
nonexistence of exact roots must be checked separately; an empty class does
not provide the intended nonvacuous closure.

The identities below hold for arbitrary admissible Lorentz links and every
invertible solder. Quantitative small-link conclusions would additionally
need their actual compact/log chart bounds. Such bounds cannot be silently
inferred from source regularity.

## 2. Repository truth and dependencies

At entry, #310 is open Draft / `IN_PROGRESS`; its task row and brief exist.
The `530a5132` parent NO-GO promotion is withdrawn. The weak-source raw norm
obstruction remains a valid scoped input. The mandatory merged inputs were
checked against live GitHub metadata:

| PR | merged head | merge commit | reusable input |
|---|---|---|---|
| #216 | `794ec0da4657375ccf03273b37a80d12fbdeed95` | `5523d8f679c1ea02f9b73d757c81649740010d0a` | designated smooth sheet, residual and reconstruction |
| #223 | `9068cd44e7010ea7a3c89aa7cc2c4a7e11c32716` | `25de48600cbc7c06e233d7b8f886f89566bdd6a4` | normal-coordinate locality under smooth vertex hypotheses |
| #226 | `56a62f7468b2e2db4f9ca7f95bc9de4c3dfc6c42` | `4b145afe33b2fb7381615199167608b71457d01d` | actual link-log/sum sensitivity bound, including its loss |
| #227 | `2ff59e4d803268cc682a2a1bd0f241e1f7717438` | `245095f941a047dec95877ef03996742f37cb429` | connection-stationary response-visible boost control |
| #232 | `94375cc0bd1194faa2d5219008b77f700fd29ded` | `caa1e65087ddf15cda35325189ebfcbf51a56592` | curved nongauge exact joint vacuum with Xi=0 |
| #237 | `5d8196f3874dc72ae0c76ea54307679f09e0dd88` | `7d7ad1ba561dc1fb1d726a8158e8ddfe0c001794` | synthesis and claim boundaries |

The relevant current-head lemma map is:

| owner | hypotheses / regime | source-image content | boundary |
|---|---|---|---|
| `A4D_STATIONARY_RESPONSE_MEMORY.md` | all invertible local solders; exact stationary field | Xi is the full horizontal solder readout | readout quotient alone does not prove realizability |
| `A4D_FINITE_CURRENT_CORRELATION_MEMORY.md` | exact shared Lorentz matrix links | both Euler and response equations have degree at most four | bounded degree does not bound global site count or inverse |
| `A4D_COMMUTING_B_FULL_LINK_CURRENT_RIGIDITY.md` | common real B subgroup, all roles; flat C5 source | raw normalized response at most `3 M5 h` | noncommuting links outside scope |
| same owner / curved parent | fixed warp; bounded diagonal source | excludes full commuting B image on fine meshes | source infeasibility, not unrestricted NO-GO |
| `A4D_Y_JOINT_FIRST_SLOW_REDUCTION.md` | frozen z=1 Y sheet and its regular neighborhood | full-rank phase-resolved first-slow source constraint | no z-to-zero, whole-torus or raw nonlinear uniformity |
| `A4D_IDENTITY_PHYSICAL_RESONANCE_CIRCLES.md` | literal flat physical `(A^T;C)` | six exact continuous joint resonance circles | requires enlarged center; quarter-only inverse fails |
| `A4D_IDENTITY_RESONANCE_CIRCLES_RESPONSE_NULL.md` | identity solder; Hermitian quadratic circle moments | response defect zero on those circle correlations | variable-coframe transport and cubic/quartic layers open |
| `A4D_IDENTITY_QUARTER_FIRSTSLOW_INJECTIVITY.md` | wrong-placement `(A;C)` | **negative control only** | former all-direction physical injectivity withdrawn |
| `A4D_WARPED_TRANSVERSE_MEAN_REDUCTION.md`, Section 7 | full relative-log-O(h) stationary field | one integrated trace agreement and necessary source condition | trace does not bound the other tensor components or raw norm |
| `A4D_SOURCE_IMAGE_COLLAPSE.md`, Section 10 | flat mesh-dependent C4-bounded, not C5-bounded source | exact raw gap 6; volume gap `6 h4` | fails fixed-source/nonconstant-background terminal |

The old identity-quarter first-slow theorem is not an available mesoscopic
coercivity input. No new Bloch census is required to recognize this exclusion.

## 3. All-role left/right face momentum

For every ordered pair `r != s`, define

\[
P_{rs}(x)=L_r(x)L_s(x+e_r)L_r(x+e_s)^{-1}L_s(x)^{-1},
\qquad P_{sr}=P_{rs}^{-1},\quad W_{sr}=-W_{rs}.
\]

For `r<s`, `W_rs` is exactly the literal complementary-solder face weight.
The reversed orientation has the same action, so it may be used when
differentiating a link of the larger role. Put

\[
C_{rs}=\tfrac12(P_{rs}-P_{rs}^{-1}),\qquad
V_{rs}=\tfrac12(P_{rs}+P_{rs}^{-1}).
\]

They obey `[V,C]=0` and `V^2-C^2=I`. Define left and right momenta by

\[
M_{rs}[X]=\tfrac12\langle W_{rs},XP_{rs}+P_{rs}^{-1}X\rangle,
\qquad
\Pi_{rs}[X]=\tfrac12\langle W_{rs},P_{rs}X+XP_{rs}^{-1}\rangle.
\tag{2}
\]

Their exact even/odd decomposition is

\[
A_{rs}[X]=\tfrac12\langle W_{rs},V_{rs}X+XV_{rs}\rangle,
\qquad
O_{rs}[X]=\tfrac12\langle W_{rs},[X,C_{rs}]\rangle,
\]
\[
\boxed{M=A+O,\quad \Pi=A-O,\quad A_{sr}=-A_{rs},\quad O_{sr}=O_{rs}.}
\tag{3}
\]

In particular the full oriented momenta are not one antisymmetric ordinary
two-cochain. Their even part is antisymmetric; their odd part is symmetric
under face reversal. Both are present in the actual variational equation.

## 4. Exact all-field master current identity

Use left-trivialized link Euler at the link base,

\[
\mathcal E_r(x)[X]
:=E_K(x,r)[\operatorname{Ad}_{L_r(x)^{-1}}X].
\]

The outgoing face incidence contributes `M_rs(x)[X]`. For the incoming
face at `y=x-e_s`, direct factor differentiation gives

\[
-M_{rs}(y)[\operatorname{Ad}_{P_{rs}(y)L_s(y)}X]
=-\Pi_{rs}(y)[\operatorname{Ad}_{L_s(y)}X].
\]

This proves, for all four roles and all six Lie directions,

\[
\boxed{
\mathcal E_r(x)[X]
=\sum_{s\ne r}\{M_{rs}(x)[X]
-\Pi_{rs}(x-e_s)[\operatorname{Ad}_{L_s(x-e_s)}X]\}.
}
\tag{4}
\]

Substituting (3) gives the central decomposition

\[
\boxed{\mathcal E=d_L^*A+\mathcal T_C,}
\tag{5}
\]
\[
(d_L^*A)_r(x)[X]=\sum_{s\ne r}
\{A_{rs}(x)[X]-A_{rs}(y)[\operatorname{Ad}_{L_s(y)}X]\},
\]
\[
(\mathcal T_C)_r(x)[X]=\sum_{s\ne r}
\{O_{rs}(x)[X]+O_{rs}(y)[\operatorname{Ad}_{L_s(y)}X]\}.
\]

If an ordinary difference is desired in a chosen frame, then

\[
\mathcal E_r=D^-A_r+\mathcal T_{Ad,r}^A+\mathcal T_{C,r},\qquad
\mathcal T_{Ad,r}^A[X]=\sum_{s\ne r}A_{rs}(y)[X-\operatorname{Ad}_{L_s(y)}X].
\tag{6}
\]

The separate ordinary difference in (6) is frame dependent; (4)--(5) are
covariant under the actual vertex Lorentz transformations. For a variable
test section use its value `b(x)` as X and transport that value into the
incoming face. No additional current conservation law is assumed.

Equations (4)--(6) are the all-role continuation of the existing temporal
right-B identity. In the common B subgroup, testing on B makes O vanish
and adjoint transport fixes B, recovering the owned commuting divergence.
The checker uses independent direct derivatives of all four actual face
factors, rather than checking (5) against a second implementation of (5).

## 5. Source, Ward constraints and the twenty latent curvature directions

Let `H=M_S C` be the complete sixteen-component solder current. The owned
metric memory is `Xi=sym(Q^-1 S^T H)/2`. Define

\[
\Gamma=\operatorname{skew}(Q^{-1}S^TH).
\]

Exactly, before stationarity,

\[
\boxed{H=2\eta S\Xi+\eta S\Gamma.}
\tag{7}
\]

The local vertical row satisfies

\[
H_x:XS_x=-2\sum_{r<s}O_{rs}(x)[X].
\tag{8}
\]

This follows by differentiating simultaneous solder/plaquette conjugation.
The literal local Ward identity equates (8) to incident link Euler rows;
hence `E_K=0` implies `Gamma=0`. With the prescribed source,

\[
\boxed{M_{S_x}C_x=2h^2\eta S_x\tau^{mat}(hx).}
\tag{9}
\]

Here `tau^mat` unpacks off-diagonal source slots with a factor one half.
Since `rank M_S=16`, the local source fiber has the exact affine form

\[
C_x=h^2 B_{S_x}\tau^{mat}(hx)+Z_x,\qquad Z_x\in\ker M_{S_x},
\quad \dim\ker M_S=20,
\tag{10}
\]

for any chosen right inverse defining B. Equation (10) is not a realizability
theorem: shared plaquette identities, the four link Euler equations and the
actual even factors remain to be imposed. In particular source regularity
controls the first term, and supplies no automatic bound on Z.

## 6. New local theorem: null curvature is not a transport quotient

At `S=I` let `Z0=ker M_I`, and let `ad_X` act on the internal Lie coordinate
of every one of the six role faces. Exact rational row reduction gives

\[
\dim Z_0=20,\quad
\dim\bigl(Z_0+\sum_{j=1}^6ad_{G_j}Z_0\bigr)=35,
\]
\[
\dim\bigl(Z_1+\sum_{j=1}^6ad_{G_j}Z_1\bigr)=36.
\tag{11}
\]

The first transported solder image has rank fifteen. Its vertical image
has rank six. Restricting the transported image to the Ward annihilator
leaves a metric image of rank **nine**, exactly the trace-free symmetric
covectors at eta. Thus all nine trace-free source directions occur in this
local linear transport relaxation. The trace of every such first transfer
is zero, because `M_S C=0` also annihilates the infinitesimal Lorentz variation
of the degree-two solder action.

For the larger twenty-six-dimensional kernel of the metric readout alone,
one adjoint-span step already generates the complete 36-dimensional carrier.
Neither local kernel is invariant under arbitrary physical adjoint transport
with the solder held fixed.

This gives a universal local linear statement. Suppose a linear quotient
`p:V->Y` erases `ker M_S`, has an induced internal adjoint action, and is
response sufficient (`D_S=d p`). Its kernel is adjoint invariant and contains
`ker M_S`. By the two-step generation in (11), it contains all of V, so p=0.
That contradicts `rank D_S=10`. Therefore **no** such local linear quotient
exists, for any Y. Keeping latent current data or using additional full-field
stationary constraints is necessary. This statement is about arbitrary
adjoint transport at fixed solder, not about the genuine simultaneous gauge
quotient of `(S,C)`.

### Explicit Ward-compatible finite control

Set only `C02=J13` and `C03=J12`, with every other face curvature zero.
Its complete solder current is zero. The first K1 transport gives

\[
[K_1,C_{02}]=K_3,\qquad[K_1,C_{03}]=K_2,
\qquad\operatorname{pack}\Xi=(0,0,0,0,0,0,0,0,1,0).
\tag{12}
\]

All six vertical rows remain zero. More strongly, for the exact Lorentz
Cayley boost `g(a)=(I-a K1/2)^-1(I+a K1/2)`, `|a|<2`,

\[
\operatorname{Ad}_{g(a)}C
=\frac{4+a^2}{4-a^2}C+\frac{4a}{4-a^2}ad_{K_1}C,
\]
\[
\boxed{\operatorname{pack}\Xi(\operatorname{Ad}_{g(a)}C)
=\frac{4a}{4-a^2}\,e_{23},\qquad E_{vert}=0.}
\tag{13}
\]

The checker clears `(4-a^2)^2` and verifies every polynomial coefficient,
so (13) is an all-parameter identity, not a small-parameter extrapolation.
Transporting S together with C is a genuine gauge transformation and keeps
the current zero. Equation (13) holds S fixed, and checks physical transport
relative to that solder; it is not a failure of gauge covariance.

**Scope:** these are local curvature carriers and local Ward constraints.
No shared-link stationarity, mesoscopic pseudokernel, fixed-source all-mesh
witness or task NO-GO is asserted. The full link equations may exclude
every realization of a proposed local transfer. Their exclusion is exactly
the remaining proof obligation.

### Every nondegenerate coframe

The ranks and noninvariance in (11)--(13) are not peculiar to eta. For an
invertible S define the local role change

\[
(T_SC)_{ab}=\sum_{r<s}
\bigl((S^{-1})_{ra}(S^{-1})_{sb}-(S^{-1})_{sa}(S^{-1})_{rb}\bigr)C_{rs}.
\]

Exterior multilinearity of the literal action gives

\[
H_S(C)=\det(S)H_I(T_SC)S^{-T},\qquad
\Xi_S(C)=\det(S)S^{-1}\Xi_I(T_SC)S^{-T}.
\tag{14}
\]

The role change is invertible and commutes with every internal adjoint.
The vertical current likewise is `det(S)` times the identity vertical
current of `T_S C`. Therefore the kernel-span dimensions, the first
fifteen-dimensional solder transfer and the Ward-compatible nine-dimensional
metric transfer hold for every invertible S. The metric trace transforms to
`Q:Xi_S=det(S) eta:Xi_I`; the nine-dimensional image remains trace-free.
The checker independently verifies every matrix coefficient of (14) on
diagonal and genuinely nonorthogonal rational coframes. The all-S proof
is the exterior-square identity, not those two samples.

This is a **local carrier isomorphism**. It does not mix or replace the four
independent lattice shifts and cannot identify the physical Fourier symbols
at arbitrary constant coframes. In particular it supplies no spectral gap.

## 7. Consequence for the global proof

The shared-current identity now retains both the even plaquette data and
the odd curvature current. The local source equation retains twenty latent
curvature directions. Those directions can feed all nine trace-free
metric directions under Ward-compatible transport.

Consequently, projecting away local response-null curvature before proving
its stationary transport compatibility loses a possible source channel.
There is no well-defined arbitrary-adjoint operator on that local quotient.
A quotient of the **full stationary field space** remains legitimate, but
its invariance/readout estimate must follow from the actual shared-link
equations. The nine-direction result also explains why the already owned
single integrated trace condition cannot close the tensor problem alone.

For log-O(h) links, `C=O(h)` and the principal even correction is quadratic:
`(V-I)(V+I)=C^2`. On the identity plaquette branch, `V+I` has a bounded
inverse. An O(h) latent curvature and an O(h) adjoint change can therefore
produce an O(h2) source-visible local term. Smoothness of the prescribed
source alone does not rule out a slowly varying term of this type. This
power count identifies a candidate interaction, not its stationary existence.

The exact degree-four matrix-link system already owns all interaction
orders. A positive proof can work with its quadratic/cubic/quartic
correlation constraints simultaneously. A frozen first-slow estimate at z=1
or a flat quadratic circle null identity is an input on its stated chart;
neither controls the latent-to-visible transport just exhibited on a general
variable coframe.

The single first missing estimate is now:

> On the exact shared-link system with (9), control the source-visible
> transport of the twenty latent curvature directions, including their
> even-plaquette and cubic/quartic correlations, uniformly in the original
> owner norm relative to the designated sheet.

It is insufficient to bound every torque as small: stationary response-null
memory is allowed. The estimate must bound its **actual metric contribution**
or prove that the contribution cannot be realized with the fixed smooth
source. A candidate dual identity must retain all role incidences in (4),
all Ward constraints and shared Lorentz links. A local relaxed moment point
is not an exact negative witness.

## 8. Frequency and curved-background boundary

UV smooth-source suppression controls source modes only. Nonlinear internal
transport may create a smooth output; excluding that conversion requires
the preceding joint estimate. IR consistency concerns the designated
response and the actual source-image compatibility. Mesoscopic estimates
must include the corrected transported resonance center and its null
correlations, with the physical Euler placement.

Local coefficient freezing is available only after a bound uniform on the
required frozen chart. Its error must be absorbed in the same owner norm,
with explicit chart, source and coframe constants. A local carrier rank
theorem supplies no such absorption estimate and no uniform control at a
degenerate link/plaquette stratum. No null/parabolic census is started here.

The all-role identity is valid before freezing, and is the correct equation
to retain when patching variable coefficients. A compactness argument would
likewise have to pass the latent-to-visible nonlinear moments through this
identity, not just discard high-frequency connection mass by source regularity.

## 9. Raw topology consistency gate

At fixed source set `rho_h^sm=h^-2 Xi(K_h^sm)`. With O(L4) sites and bounded
slot multiplicities, a pointwise source/comparator error O(h^p) gives a raw
bound O(h^(p-4)). Thus the proposed raw O(h) rate requires a source error
O(h5), or an equivalent global cancellation estimate in the **absolute** sum.
For Xi itself the corresponding local error is O(h7).

For example, if `rho_h^sm=tau0+h2 c+o(h2)` with a nonzero smooth c and
there exist exact roots with fixed source tau0, their raw normalized gap
generically scales as h^-2 although their volume-normalized gap tends to
zero. This is a conditional consistency warning, not an assertion of that
expansion or of root existence in this repository. The #216 reconstruction
rate must not be substituted for the stronger comparator estimate in (1).
Both norms may be reported; the theorem target retains the original norm.

The retained C4-but-not-C5 oscillatory family refutes a uniform weaker-source
statement. It does not establish sharpness for a single fixed C4 source;
that different quantifier needs a separate argument.

## 10. Replay and result boundary

```sh
python 02_REGISTRY/research/certificates/a4d_full_current_transport_quotient_check.py
```

The checker verifies exact local ranks and every coefficient of (13)--(14).
On a noncommuting 24-site four-dimensional lattice with variable nonorthogonal
solders it compares all **576** independent literal link Euler components
with (5), checks 1728 transported covariance incidences, the local Ward and
solder/source split, and rejects deletion of adjoint transport or odd momentum
on every one of the 576 rows in that hostile array. The lattice is a finite
control of the analytic all-field proof, not an extrapolated stationary theorem.

Verdicts:

* `ALL-ROLE-LEFT-RIGHT-CURRENT-DECOMPOSITION-CERTIFIED`;
* `LOCAL-RESPONSE-NULL-ADJOINT-QUOTIENT-OBSTRUCTED`;
* `WARD-COMPATIBLE-NULL-TRANSPORT-HAS-NINE-TRACEFREE-SOURCE-DIRECTIONS`;
* parent fixed-source theory: `PARTIAL / OPEN`, Draft / `IN_PROGRESS`.

No positive task terminal, exact all-mesh negative terminal, new selector,
action, Lean owner, BOOK/CORE or release claim is promoted.

Local validation for this increment: the new pinned checker; the retained
stationary-response memory, full-link B current and weak-source topology
controls; canonical architecture, generated Lean views, active-work,
agent-protocol, claim-strength and formalization-debt guards; the actual
Draft PR contract; certificate artifact freshness and semantic mutation
controls; Python compilation and whitespace checks all pass. Lean sources
are unchanged, so no full Lean rebuild was needed for this research increment.
Remote current-head CI remains separately reported.

## 11. Shared-link quadratic completion: a slow interaction remains visible

Input head for this increment: `135d6a74cc6318bb9c4bcca0c52f6203b19f8a3a`.
Certificate: `certificates/a4d_joint_quadratic_beat_transfer_check.py`, with
its pinned `_results.json`. This calculation uses the already owned physical
circle kernels. It neither searches for additional fibres nor classifies
nonlinear connection families.

Section 6 concerned an arbitrary local curvature carrier. Here the inputs
are actual full-lattice **linear joint modes**, and every shared-link
connection equation is retained in their quadratic completion. The result
is a nonzero slow metric interaction after that completion. It closes the
question whether imposing quadratic connection stationarity alone erases
this transfer: it does not. The additional smooth-source constraints still
matter, and the packet below fails a fast-source gate.

### Two owned joint modes and their slow output

Work at the identity solder. Write `H(lambda)` for the physical connection
Hessian, with the literal input-minus-output incidence convention, and
`C(lambda)` for the ten-slot linear metric response. Thus `H=A^T` in the
older `flat_symbols` convention; replacing H by A is invalid. Set

\[
T_1=K_2-K_3+J_{23},\quad T_2=K_1-K_3+J_{13},\quad
T_3=K_1-K_2+J_{12}.
\]

The first owned circle vector has role components

\[
v_1(a)=((i-a)K_1,(i-a)K_1,(1-i)T_2,(1-i)T_3).
\]

The second is its simultaneous internal/role permutation `1 <-> 2`:

\[
v_2(a)=((i-a)K_2,(1-i)T_1,(i-a)K_2,-(1-i)T_3).
\]

For a unit t near 1, use the characters

\[
\lambda_1=(it,it,i,i),\quad\lambda_2=(it,i,it,i),\qquad
u(x)=\lambda_1^xv_1(it),\quad
v(x)=\overline{\lambda_2^xv_2(it)}.
\]

Both satisfy all 24 linear connection and all ten linear metric equations.
Their mixed character is

\[
z=\lambda_1\overline{\lambda_2}=(1,t,t^{-1},1).
\]

Let f(t) and q(t) be the coefficients of `epsilon*delta` in the literal
right-trivialized E_K and packed Xi for the link logs
`epsilon*u+delta*v`. Differentiate every direct and inverse face factor and
scatter its covector to the actual link base. The certificate does this
independently of the symbol assembly and proves the linear matches
coefficientwise in Laurent t, rather than by a rank census.

Add the log correction `epsilon*delta*z^x*w(t)`. Its connection equation
and metric response are

\[
H(z)w+f=0,\qquad S(t)=q(t)+C(z)w(t).
\tag{Q1}
\]

Since `det H(1,1,1,1)=256`, w is uniquely defined and regular near t=1.
The checker solves (Q1) in `QQ(i)(t)` and verifies every one of its 24 rows
as an exact rational identity. Two particularly simple corrected slots are

\[
\boxed{S_{11}(t)=i(t-1)/t,\qquad S_{22}(t)=i(t-1).}
\tag{Q2}
\]

In the original packed-slot order, the full first derivative is

\[
S(1)=0,\qquad
S'(1)=(0,1-i,-1-i,2i,i,0,0,i,0,-2i).
\tag{Q3}
\]

Its metric trace vanishes. It is not the zero source. Omitting w changes
the response, so (Q2) already includes the actual quadratic connection
range solve. On `t=exp(i*kappa)`, these diagonal slots have nonzero terms
linear in kappa. The exact zero mean stress of one circle mode therefore
does **not** give higher-order suppression of interactions between circles.

### Full quadratic connection stationarity, and the source limitation

Adjoin the conjugates of both inputs to obtain real Lorentz link logs.
Every quadratic product character of these four modes approaches either
`(1,1,1,1)` or `(-1,-1,-1,-1)` as t approaches 1. Both physical Hessians
have determinant 256. By continuity, all these finitely many output fibres
have bounded inverses in one fixed neighbourhood. Solve each Fourier
forcing there. This constructs a real second-order correction with
**all** quadratic shared-link connection rows zero; its z coefficient is
the w of (Q1). This is an analytic finite-convolution argument using two
owned IR matrices, not a claimed gap over all characters. At higher orders
output frequencies return to the resonant carriers, and this argument
supplies no corresponding inverse or nonlinear compatibility theorem.

Connection stationarity alone is insufficient. The first input already
has a nonzero fast self-source. At t=1 its real part is the four-phase
profile with roles 2 and 3 equal to `(1,1,-1,-1)*T_r`. After the complete
second-order connection correction its phase-pi metric coefficient is

\[
b=(2,-2,-1,-1,0,1,1,0,0,0).
\tag{Q4}
\]

The new literal mixed-jet calculation agrees exactly with the independent
existing four-phase Euler assembly on (Q4). For t near 1 the positive
self-product character is `(-t^2,-t^2,-1,-1)`, and its response remains
nonzero by continuity. On fine meshes this fast character is distinct
from the slow z and from the other quadratic products, so its coefficient
cannot be removed by a correction at z. A fixed smooth source, or uniform
C5 source bounds, requires its fast Fourier coefficient to be O(h5) or
smaller after dividing Xi by h2. With leading link amplitude h, the
coefficient in (Q4) instead has order one in that rescaled source. Thus
this chosen leading packet cannot be used as a fixed-source witness.
Additional leading modes could change the fast-source algebra; no general
classification or exclusion of those combinations is claimed here.

### Raw norm and the precise remaining obligation

On `L in 4N`, choose `t=exp(2*pi*i/L)`. All input characters are exact
lattice characters, and z is a macroscopic frequency. For the **quadratic
coefficient alone**, the Fourier inequality in the original owner norm
gives, at log amplitude epsilon,

\[
h^{-2}\|\Xi^{[2]}\|_{\mathrm{owner},1}
\ \ge\ \epsilon^2h^{-2}L^4|t-1|.
\tag{Q5}
\]

At epsilon=h this benchmark grows like `2*pi*L^3`, while its
volume-normalized counterpart tends to zero. Equation (Q5) is not a
bound on the response of an exact root: at that simultaneous scaling the
cubic amplitude term h3 can have the same size as this slow quadratic
term h2*(t-1). It must be retained, together with the quartic correlations.
Moreover (Q4) already fails the required source convention. Neither this
jet nor (Q5) is a parent NO-GO, on a nonconstant background or otherwise.

The first missing estimate is now more concrete: **use the full fast metric
source constraints and shared-link stationarity to control these corrected
slow interaction moments, their cubic/quartic completions, and their
transport through the fixed varying coframe, in the raw owner norm.**
Single-mode stress nullity, Ward trace cancellation, or the quadratic
connection equation separately cannot supply it. The result remains
`PARTIAL / OPEN`, Draft / `IN_PROGRESS`.

Replay:

```sh
python 02_REGISTRY/research/certificates/a4d_joint_quadratic_beat_transfer_check.py
```

Scoped verdict: `QUADRATIC-STATIONARY-BEAT-SOURCE-NONZERO`.
The exact fast-source negative control is part of the certificate and is
required when interpreting this verdict.

Validation for this increment: the new pinned mixed-jet checker and the
retained all-role current/transport checker pass, including their independent
Euler and wrong-placement controls. Canonical repository, generated views,
work, agent-protocol, claim-strength, formalization-debt, actual Draft PR
contract, certificate artifact freshness, compilation and whitespace checks
pass locally. No Lean source or task lifecycle state changes.


## 12. A pointwise transport detector controls a reduced mixing moment

Input head: `b3bae8fe54cf8fd88d8eb46d45728ad741c0962a`.
Certificate: `certificates/a4d_spatial_transport_entropy_check.py` and its
pinned result ledger. It consumes the owned quarter nonlinear reduction
and literal physical incidence stencil, pinned by Git blob SHA. It does
not search for carriers, enumerate periods, or construct another family.

Section 11 leaves a slow interaction after quadratic connection completion
and excludes its chosen packet by a fast metric-source gate. Here a positive
interaction moment is controlled by an exact polynomial consequence of
the reduced joint gates. This yields a mesh-independent raw estimate for
the **cubic first-slow reduction**. Its identification with the full
fixed-source lattice problem remains unproved.

### Exact pointwise detector

Use real amplitudes c=(a0,a1,a2,a3,b0,b1,b2,b3),
c_s=(a1,a2,a3,b1,b2,b3), and c_t=(a0,b0).
The leading four-phase logs are `(a_r,b_r,-a_r,-b_r)*T_r`; their quarter
Fourier coefficient is `(a_r-i*b_r)/2`. Let B be the owned lower fourteen
complex row projection after eliminating the twenty normal columns,
and T insert the four center vectors. For the physical joint symbol
J=(A^T;C), set

\[
\Gamma_\mu=B(\partial_{\theta_\mu}J)T,\qquad
G_\mu=\frac12
\begin{pmatrix}
\operatorname{Im}\Gamma_\mu&-\operatorname{Re}\Gamma_\mu\\
-\operatorname{Re}\Gamma_\mu&-\operatorname{Im}\Gamma_\mu
\end{pmatrix}.
\tag{E1}
\]

The factor -i turning Fourier theta into an envelope derivative is included.
All 24 connection and ten packed metric rows, and all Laurent incidences,
are retained before B. The checker reconstructs the derivative from the
literal face Hessians; the incorrect Euler placement A is a negative control.

Let Q_3(c) be the owned 28-component real cubic projected joint forcing
after the quadratic normal solve, and Q_3^s its restriction to c_t=0.
The ledger supplies a rational 6 by 28 matrix P and quadratic R_r such that

\[
\boxed{P G_{\mu,s}=0\quad(\mu=0,1,2,3)}
\tag{E2}
\]

and

\[
\boxed{c_s^TPQ_3^s(c_s)=D_s(c_s)+\sum_{r=1}^3 a_rb_rR_r(c_s),\quad
D_s=\sum_{r<s}(a_r^2+b_r^2)(a_s^2+b_s^2).}
\tag{E3}
\]

All 144 entries in (E2) vanish; all 126 degree-four coefficients in (E3)
agree over Q. This is coefficientwise verification, without extrapolation
from a numerical positivity test. On this spatial restriction the products
a1*b1, a2*b2, a3*b3 are exactly the fast quadratic metric coefficients
at packed slots 23, 13, 12, including the normal correction. The bounds are

\[
\|P\|_{1\to1}=\frac{3209848}{5565}<577,\qquad
\max_r\sum_m |(R_r)_m|=\frac{7585775}{4452}<1704.
\tag{E4}
\]

### Uniform raw estimate for arbitrary reduced fields

On any finite periodic grid, take any field c_s(x) and any componentwise
difference operators D_mu. Define

\[
\mathcal R_3^s=\sum_\mu G_{\mu,s}D_\mu c_s+Q_3^s(c_s).
\]

Equation (E2) gives `P R_3^s=P Q_3^s` **at every site**. No boundary
flux, amplitude regularity or sum cancellation is needed for this algebraic
statement. With rho=max_x,j |(c_s)_j(x)|, (E3)-(E4) give

\[
\boxed{\sum_xD_s(c_s(x))
\le577\rho\|\mathcal R_3^s\|_{\mathrm{raw},1}
 +1704\rho^2\sum_r\|a_rb_r\|_{\mathrm{raw},1}.}
\tag{E5}
\]

These are unweighted site/component sums, without h4 volume normalization.
The estimate controls a correlated quartic mixing moment, rather than just
an averaged trace. An unrestricted rational field on a 4 by 4 by 4 by 4
grid with forward differences verifies the pointwise and summed identities.
That replay checks the implementation; (E2)-(E3) prove all-grid validity.

Invisible oscillations along one axis are retained. If the three products
and P Q_3^s vanish, (E3) allows at most one spatial role; its fast product
allows at most one parity. The common zero set is therefore the six spatial
amplitude axes A_s. The derivative of
`c_s -> (a1*b1,a2*b2,a3*b3,P Q_3^s(c_s))` has rank five at each unit
axis, as verified exactly. Compactness on the unit sphere, those injective
tangent derivatives, and the absence of other zeros imply a kappa>0 with

\[
\|s(c_s)\|_1+\|P Q_3^s(c_s)\|_1
\ge\kappa |c_s|^2\operatorname{dist}(c_s,A_s),\qquad |c_s|\le1.
\tag{E6}
\]

For c_s=r*omega, quadratic and cubic homogeneity bound the left side below
by r3 times its angular counterpart, while distance scales by r. This
explains the exponent and does not impose connection uniqueness.

The owned local analytic normal graph has even mean readout m=O(|c_s|4),
Dm=O(|c_s|3), and exact zero readout on A_s. Thus
`|m(c_s)|<=C*|c_s|3*dist(c_s,A_s)`. Equations (E2),(E6) yield

\[
\sum_x\|m(c_s(x))\|_1
\le C\rho\left(\|\mathcal R_3^s\|_{\mathrm{raw},1}
                    +\sum_r\|a_rb_r\|_{\mathrm{raw},1}\right).
\tag{E7}
\]

This is a bound on the frozen analytic readout, not its identification with
the full varying-coframe Xi.

### Full eight-amplitude balance retains the temporal carrier

Set B_mu=P G_mu,t. Each of the four 6 by 2 matrices has ten nonzero
entries. Their exact ledger gives

\[
\max_{\mu,j}\sum_i |(B_\mu)_{ij}|=\frac{304751}{1113}<274.
\tag{E8}
\]

The full fast coefficients q_f=(Q2,23,Q2,13,Q2,12) equal
q_f,r=a_r*b_r+alpha_r, where

\[
\begin{aligned}
\alpha_1&=a_0b_0+a_0b_2+a_2b_0-a_0b_3-a_3b_0,\\
\alpha_2&=a_0b_0-a_0b_1-a_1b_0-a_0b_3-a_3b_0,\\
\alpha_3&=a_0b_0-a_0b_1-a_1b_0+a_0b_2+a_2b_0 .
\end{aligned}
\tag{E9}
\]

These three full fast coefficients alone do not separately control the
spatial products. Section 13 uses all ten coefficients and the real source
image to obtain a uniform bound on every quadratic gate moment.
Define the homogeneous quartic polynomial

\[
T(c)=c_s^TPQ_3(c)-D_s(c_s)-\sum_r a_rb_rR_r(c_s).
\]

Its 179 nonzero monomials each contain temporal and spatial amplitudes.
Their absolute coefficient sum is 43759468/5565<7864. For component
suprema rho_s, rho_t and rho=||c||_infty,

\[
|T(c)|\le7864\rho_s\rho_t\rho^2.
\tag{E10}
\]

For the full reduced residual R_3=sum_mu G_mu D_mu c+Q_3(c),
the exact balance is

\[
D_s=c_s^TP\mathcal R_3-\sum_\mu c_s^TB_\mu D_\mu c_t
 -T(c)-\sum_r(q_{f,r}-\alpha_r)R_r(c_s).
\tag{E11}
\]

It implies the all-grid raw bound

\[
\begin{aligned}
\sum_xD_s\le{}&
577\rho_s\|\mathcal R_3\|_{\mathrm{raw},1}
+1704\rho_s^2\|q_f\|_{\mathrm{raw},1}\\
&+274\rho_s\sum_\mu\|D_\mu c_t\|_{\mathrm{raw},1}
+\|T(c)\|_{\mathrm{raw},1}
+1704\rho_s^2\sum_r\|\alpha_r(c)\|_{\mathrm{raw},1}.
\end{aligned}
\tag{E12}
\]

No bound on these temporal terms follows from response invisibility. The
latent carrier is explicitly retained in the proposed quotient.

### Full-field gap and validation

The first missing estimate is a **uniform pullback of this moment balance
and readout to the full realizable source image**, controlling temporal
terms, varying-coframe transport, shared-link quartic correlations and
the remainder outside the frozen graph in the original raw owner norm.
Arbitrary rapidly varying amplitudes do not justify spectral separation
or a truncated first-slow expansion of actual lattice equations. Pointwise
cancellation in the reduction supplies no bound on its omitted lattice terms.

The fixed smooth source, including the uniform-C5 option, and the #216
comparator remain required. Replacing R_3 by E_K or the fast coefficients
by tau in (E5)-(E7) without that pullback would be invalid. No exact negative
witness, terminal, selector, action term, Lean or public/CORE promotion is
asserted. Scoped verdict:
`SPATIAL-REDUCED-TRANSPORT-ENTROPY-CERTIFIED`.
Parent: `PARTIAL / OPEN`, Draft / `IN_PROGRESS`.

Replay:

```sh
python 02_REGISTRY/research/certificates/a4d_spatial_transport_entropy_check.py
```

Preparation validation: an independent exact BigInt-rational replay verified
the literal first-slow matrices, all 126 quartic coefficients and 144 zero
transport entries, six rank-five derivatives, the 256-site raw balance and
the temporal coefficients/bounds. Removing a detector coefficient or
omitting the fast terms fails the controls. Input head b3bae8fe passed
GitHub D0 guards run 37109272782. The local execution service is unavailable,
so fresh local Python and guard execution is not claimed. The Python replay
and new-head guards are submitted to existing CI; their execution status
must be tracked separately.
## 13. The real source image removes the false quadratic null direction

Input head: `5eda55851f67b81060c1b9b75bb36cf45b031b8e`.
Certificate: `certificates/a4d_full_quartic_source_quotient_check.py` and its
pinned ledger. This increment uses all eight owned center amplitudes and
all ten fast metric coefficients. It identifies the actual quartic mean
readout before choosing a coercive moment; no new carrier or stationary
family is classified.

### All ten fast coefficients control the real quadratic image

Retain the owned eight-vector t(c) from the nonlinear quarter owner:

\[
\begin{aligned}
t_0&=a_0(a_1-a_2+a_3)-b_0(b_1-b_2+b_3),&
t_1&=a_0b_0,\\
t_2&=a_1b_1,&t_3&=a_2b_2,&t_4&=a_3b_3,\\
t_5&=a_0b_1+a_1b_0,&t_6&=a_0b_2+a_2b_0,&
t_7&=a_0b_3+a_3b_0 .
\end{aligned}
\]

The full fast quadratic metric gate is q=Q_2(c)=M_2 t(c).
M_2 has rank seven and kernel spanned by
xi=(3,1,1,1,1,1,-1,1). Its apparent null direction is not a realizable
nonzero **real** quadratic image. The exact identity

\[
(a_0b_1-a_1b_0)^2=t_5^2-4t_1t_2
\tag{R1}
\]

makes the right side nonnegative, whereas it equals \(-3s^2\) at t=s*xi.
This yields a quantitative statement, rather than just zero-set isolation.

The ledger gives an 8 by 10 rational L such that
`L M_2=I-xi e_1^T`, where e_1 selects t1 in zero-based indexing.
Set w=Lq and s=t1. Then t=s*xi+w, w1=0, and (R1) implies

\[
3s^2\le2s(w_5-2w_2)+w_5^2,\qquad
|s|\le\frac43(|w_5|+|w_2|).
\tag{R2}
\]

For the second inequality, solve the scalar quadratic inequality, use
`sqrt(B^2+3*w5^2)<=B+2*|w5|` for B=|w5-2*w2|,
then the triangle inequality. Since ||xi||1=10, the exact weighted column
norms of L give

\[
\boxed{\|t(c)\|_1\le\frac{110}{3}\|Q_2(c)\|_1}
\tag{R3}
\]

for **every real c**, without a small-amplitude assumption. Summing (R3)
over any finite grid preserves its constant and uses no volume factor.

Consequently all three spatial parity products, a0*b0 and all temporal
cross-phase sums are controlled by the ten-component source gate.
Section 12's three selected coefficients alone do not give this conclusion.
The alpha terms in (E9) equal
`(t1+t6-t7, t1-t5-t7, t1-t5+t6)` and are now bounded by the full gate.
A nonzero temporal single-parity amplitude can still be invisible; its
spatial derivative is not bounded by (R3).

There is also a stronger statement about individual phase products. For
j=1,2,3 set u=a0*bj and v=aj*b0. Then

\[
(u-v)^2=t_{j+4}^2-4t_1t_{j+1},\qquad
|u|+|v|=\max(|u+v|,|u-v|)
 \le |t_{j+4}|+|t_1|+|t_{j+1}|.
\]

Using (R2) and the exact column bounds of L gives

\[
\boxed{
\mathcal C(c):=
 \sum_{i=j\ {\rm or}\ i=0\ {\rm or}\ j=0}|a_i b_j|
 \le\frac{140}{3}\|Q_2(c)\|_1 .}
\tag{R4}
\]

The sum has ten terms. This proves that the full real source image
controls every temporal cross-phase product individually, even though
the linear map on the formal eight-vector has a kernel.

### The true quartic readout includes the cubic normal correction

Let W(c) be the owned analytic normal graph and let
`m(c)=mean_p Xi(eta,exp(V(c)+W(c)))`. Its degree-four term R4 is now
computed as a polynomial in **all eight amplitudes**.

Start with the pinned quadratic correction W2. Assemble every literal
Euler degree-three coefficient and apply the owned row transform B.
Its first twenty complex rows determine the cubic normal correction W3.
The lower fourteen rows reproduce all 120 owned cubic coefficient vectors.
Insert W3 before computing the degree-four metric mean. A still-unsolved
W4 cannot affect that mean because the zero-frequency linear metric
block C(1) vanishes. Thus the computed R4 is the Taylor coefficient of
the actual normal-graph readout, rather than the response of V+W2.

For \(c=e_{a_1}+e_{b_2}\), in the established packed-slot order,

\[
Q_2(c)=0,\qquad
\boxed{R_4(c)=(1/16,0,0,-1/8,0,0,0,0,0,1/16).}
\tag{R5}
\]

Its quarter-translation partner \(c=e_{a_2}-e_{b_1}\) has the same mean readout.
Omitting W3 instead produces
`(0,3/32,3/32,0,0,0,-3/32,0,-3/32,0)`.
The two vectors differ, so a W2-only quartic calculation cannot be used
as this observable's coefficient. These source-zero quadratic controls
still have a nonzero cubic joint gate; they are not exact joint fields
and do not produce a prescribed-source witness.

For \(c=e_{a_2}-e_{a_3}\) and \(c=e_{b_2}-e_{b_3}\), R4 is exactly zero even though the spatial
mixing moment D_s of Section 12 equals one. More generally, the complete
quartic mean readout vanishes on both pure-parity spaces b=0 and a=0.
This is an identity at degree four, not an all-order assertion that
these mixed fields are stationary or response-null. A bound forcing
every D_s to vanish would therefore control more than this observable
requires.

### Observable phase correlations and a uniform raw readout bound

Every nonzero monomial of R4 contains an a and a b amplitude. The ledger
factors it coefficientwise as

\[
R_{4,j}(c)=\sum_{r,s=0}^3 a_r b_s\,F_{j,rs}(c),
\tag{R6}
\]

with quadratic F_j,rs. The assignment is deterministic: prefer a
controlled pair from (R4), then the lexicographically first available
pair. It is verified on the complete polynomial, including all ten
metric slots. For the resulting witness,

\[
\max_{r\ne s,\ r,s>0}\sum_{j,m}|(F_{j,rs})_m|=\frac{99}{8},
\quad
\max_{r=s\ {\rm or}\ r=0\ {\rm or}\ s=0}
 \sum_{j,m}|(F_{j,rs})_m|=\frac{459}{4}.
\]

Define the six remaining products
`Z_s=(a1*b2,a1*b3,a2*b1,a2*b3,a3*b1,a3*b2)`.
For any field of amplitudes on any finite grid, with
rho=max_x,j |c_j(x)|, equations (R4),(R6) give

\[
\boxed{
\|R_4(c)\|_{\mathrm{raw},1}
 \le\rho^2\left(\frac{99}{8}\|Z_s(c)\|_{\mathrm{raw},1}
                       +5355\|Q_2(c)\|_{\mathrm{raw},1}\right).
}
\tag{R7}
\]

Here 5355=(459/4)*(140/3). Every norm is the unweighted site/component
sum. All eight amplitudes and the temporal carrier remain permitted;
there is no amplitude derivative or grid-size loss in this frozen
polynomial estimate. The exact 256-site control uses arbitrary rational
site values and verifies both source bounds and (R7).

Equation (R6) does not define a sufficient memory of six numbers alone.
The observable contains the **joint fourth-order correlations**
`a_r*b_s*F_j,rs(c)`. Averaging the products and the quadratic factors
separately would lose them.

### Why first/second moments and averaged cubic gates are insufficient

An exact probability-law control makes that loss visible. Let \(c=e_{a_1}+e_{b_2}\),
v=R4(c), and take

\[
\nu_1=\tfrac12(\delta_c+\delta_{-c}),\qquad
\nu_2=\tfrac18(\delta_{2c}+\delta_{-2c})+\tfrac34\delta_0.
\tag{R8}
\]

Both have zero first moments and the identical full covariance
`integral z*z^T dnu=c*c^T`. Both have zero averaged quadratic fast source
and zero averaged cubic joint gate. Nevertheless homogeneity and (R5)
give

\[
\int R_4\,d\nu_1=v,\qquad \int R_4\,d\nu_2=4v .
\tag{R9}
\]

The same calculation works after multiplying all atoms by any small
positive amplitude. Thus a description retaining only first/second
moments and averaged gates through degree three cannot reconstruct this
quartic metric mean. The checker verifies the rational weights, every
covariance entry, every averaged gate and both readouts exactly.

These are algebraic amplitude laws. No stationary lattice field with
either law is constructed, and no full shared-link correlation or source
realizability is inferred. In particular, (R9) is a memory-obligation
control, not a fixed-source counterexample or parent NO-GO.

### What remains and validation

The source-image kernel and the temporal **quadratic products** in the
frozen reduction are now controlled by (R3)-(R4). The observable obligation
is narrower: control the six cross-phase correlations in (R6), together
with their shared-link transport, and pull that control through the exact
varying-coframe source equations and the #216 comparator in the raw owner
norm. Averages of the gates do not supply this step, as (R8)-(R9) prove.

The freezing, frequency extraction and normal-graph remainder are still
uncontrolled on the full admissible class. Even the analytic remainder
`m(c)=R4(c)+O(|c|6)` is not enough in the task norm: at rho=O(h), its
naive bound \(h^{-2}L^4\rho^6\) is only O(1). The next obligation remains one
estimate on the **exact full-link quartic source/current memory**, rather
than an extrapolation of Taylor coefficients or another carrier census.
Neither Q2 nor R4 may simply be substituted for the prescribed tau or
full Xi in (R7).

Scoped verdict:
`REAL-FAST-SOURCE-COERCIVITY-AND-QUARTIC-READOUT-QUOTIENT-CERTIFIED`.
Parent: `PARTIAL / OPEN`, Draft / `IN_PROGRESS`.
No action, selector, source convention, Lean owner or public/CORE claim is
changed.

Replay:

```sh
python 02_REGISTRY/research/certificates/a4d_full_quartic_source_quotient_check.py
```

The complete symbolic rational jet agrees coefficientwise with the owned
cubic ledger and with independent Fraction/Q(i) literal Euler evaluations,
including a dense rational input. Source inverse identities, discriminants,
both uniform raw bounds, the two-law control and the omitted-W3 negative
control pass. The preceding head 5eda5585 has successful D0 guards run
37114124025, including its Python entropy certificate. New-head validation
is tracked separately.


Local validation of this increment: the new pinned quartic/source checker,
the retained spatial transport detector, all-role current/transport and
stationary response-memory controls pass. Canonical architecture, generated
views, active-work, agent-protocol, claim-strength, formalization-debt,
actual Draft PR contract, artifact freshness/semantic mutations, new Python
compilation and whitespace checks pass. No Lean source changes require a
full Lean rebuild. New-head CI is reported separately.

## 14. The full-eight reduced quartic readout has a pointwise source bound

Input head: `ac022ee01d0037ee0e8d8a89b8be1c8143bb38b2`.
Certificate: `certificates/a4d_quartic_joint_transport_syzygy_check.py`,
with an explicit rational ledger of all eighty identities. The input is
the complete ten-slot quartic readout of Section 13, including W3, and
all four physical first-slow transport matrices of Section 12. No new
carrier, period, circle, amplitude family or source convention is introduced.

The unresolved six spatial products in (R7) can be eliminated from the
**frozen reduced readout estimate**. For the full real eight-amplitude
field on any finite grid set

\[
\mathcal R_3=\sum_{\mu=0}^3G_\mu D_\mu c+Q_3(c),\qquad
\rho=\max_{x,i}|c_i(x)|.
\]

There are exact rational constants, independent of the grid and of the
amplitude field, such that

\[
\boxed{
\|R_4(c)\|_{raw,1}
 \le\frac{39450673}{97020}\rho\|\mathcal R_3\|_{raw,1}
       +\frac{3526141}{99}\rho^2\|Q_2(c)\|_{raw,1}.
}
\tag{S1}
\]

The constants may be rounded to 407 and 35618. All ten metric components
and both temporal amplitudes are retained. This is a bound on the observable,
not on the unnecessary positive mixing moment D_s. In particular it imposes
no smallness on temporal amplitude derivatives or on invisible amplitudes.

### A saturated identity, rather than a signed flux balance

Concatenate the four real 28 by 8 matrices G_mu. Its exact rank is twelve.
Choose a rational basis N of its common left kernel, with sixteen rows:

\[
\boxed{NG_\mu=0\quad\text{for every }\mu=0,1,2,3.}
\tag{S2}
\]

All 512 entries vanish. Consequently `N R3=N Q3` at each site for arbitrary
componentwise differences D_mu. This cancellation precedes multiplication
by an amplitude-dependent coefficient; no derivative of that coefficient
or summation by parts is used.

Let P be the ten pairs `(r,s)` with `r=s` or `r=0` or `s=0`, and let

\[
t_0=a_0(a_1-a_2+a_3)-b_0(b_1-b_2+b_3).
\]

For **every** coordinate i=0,...,7 and metric slot j=0,...,9 the checker
constructs rational homogeneous polynomials A and B of degree three and
H of degree two satisfying

\[
\boxed{
c_iR_{4,j}
 =A_{ij}t_0
  +\sum_{(r,s)\in P}B_{ij,rs}a_rb_s
  +\sum_{\alpha=1}^{16}H_{ij,\alpha}(NQ_3)_\alpha.
}
\tag{S3}
\]

These are eighty complete coefficientwise degree-five identities. They
are identities on all real amplitudes, not a classification inferred from
sampled points. After quotienting the ten controlled monomial products,
172 degree-five monomials remain. The 696 columns `t0*cubic` and
`(NQ3)*quadratic` have rank 144; adjoining all eighty `c_i R4,j` adds no
rank. The checker lifts the solutions back to the complete polynomial
ring and verifies (S3), including every removed source-product term.
The degree-five multipliers do not add a new action or correlation order.

At a site with c nonzero, choose i with `|c_i|=rho_x=max_k|c_k|`.
Divide (S3) by c_i only **at that site**. The degree-two and degree-three
coefficient bounds give factors rho_x and rho_x^2 respectively. The real
source bounds (R3)-(R4) give

\[
|t_0|\le(110/3)\|Q_2\|_1,\qquad
\sum_{(r,s)\in P}|a_rb_s|\le(140/3)\|Q_2\|_1.
\]

Combining H with N before taking the joint-row column norm gives the
constant 39450673/97020. Weighting the cubic source multipliers by the
preceding two bounds gives 3526141/99. If c=0, R4=0. Thus (S1) first
holds pointwise with rho_x, then after summing absolute values with rho.
The dominant-coordinate choice requires no regularity, no coherent choice
between sites and no differentiation. All norms remain unweighted.

This explains why a direct unsaturated tensor-multiplier search is
unnecessarily restrictive: a bounded pointwise rational cover of amplitude
space suffices. It also avoids the positive-production obstruction, whose
two witness amplitudes have zero quartic readout.

### Correlation memory and the full-field boundary

The laws in (R8)-(R9) remain valid. Their **averaged** cubic gates are zero,
but the gate `NQ3` at their visible atoms is nonzero. Estimate (S1) uses
the absolute sum of the actual pointwise residuals. Replacing it by the
absolute value of their signed averages would be false. First/second
moments still do not reconstruct the observable.

The previous reduced estimate (R7) leaves six spatial cross-phase products.
Equation (S1) now controls their actual quartic **metric contribution** in
the full-eight identity first-slow reduction. It does not bound the full
varying-coframe response by silently identifying Q2 with tau or R3 with EK.
The first remaining theorem is the uniform pullback of this observable
bound through the exact shared-link equations and the designated comparator,
including the normal-graph remainder and every coframe/adjoint shift.
At rho=O(h), a per-site O(rho6) remainder still has normalized raw size O(1).
It cannot be dropped. The exact matrix-link memory of degree at most four
already includes that effect without truncating logarithmic coordinates.

Validation: the checker reconstructs all eighty rational identities and
their coefficient norms, verifies every full-eight transport cancellation,
checks the visible atom, rejects a mutated coefficient and deletion of the
source contribution, and checks the pointwise and absolute-sum bound on
an unrestricted 81-site full-eight field with temporal and spatial forward
differences. The coefficient identities prove arbitrary-grid validity;
the finite replay checks the implementation.

Scoped verdict:
`FULL8-FROZEN-QUARTIC-READOUT-CONTROLLED-BY-REAL-JOINT-GATES`.
The original fixed-source/nonconstant-background task remains
`PARTIAL / OPEN`, Draft / `IN_PROGRESS`.

Replay:

```sh
python 02_REGISTRY/research/certificates/a4d_quartic_joint_transport_syzygy_check.py
```

## 15. Uniform C5 sources close the fixed fast part of the full response

This statement concerns the actual response, not a frozen jet. Let
`rho_sm,h(y)` be the smooth ten-slot normalized response of the prescribed
#216 comparator, and suppose its C5 seminorms are uniformly bounded. This
is supplied, under that owner's smooth-realization hypotheses, by its
asymptotic construction in every fixed smooth seminorm. Let the source
interpolants `tau_h` be uniformly C5; one fixed smooth `tau` is included.
For every exact source root, independently of its connection regularity,

\[
R_h(x):=h^{-2}(\Xi(Q_h,K_h)-\Xi(Q_h,K_h^{sm}))(x)
       = f_h(hx),\qquad f_h=\tau_h-\rho_{sm,h}.
\tag{F1}
\]

Choose any fixed smooth periodic Fourier multiplier `chi(theta)` that is
zero in a neighborhood of the zero lattice character. With the original
unweighted owner sum and
`M5=max_r sup_h,y sum_j |partial_r^5 f_h,j(y)|`,

\[
\boxed{\|\chi(T)R_h\|_{owner,1}\le C_\chi M_5h.}
\tag{F2}
\]

In particular the unscaled fast response gap is `O(h3)=o(h2)`.
All ten packed slots, including their existing off-diagonal dual convention,
are retained. No Fourier restriction on the connection is imposed.

Here is the proof with no lattice-size-dependent inverse. Put
`d_r(theta)=exp(i theta_r)-1` and define

\[
b_r(\theta)=\frac{\chi(\theta)\overline{d_r(\theta)}^5}
                 {\sum_s|d_s(\theta)|^{10}}.
\]

Extend `b_r` by zero near the zero character. These are smooth on the
four-torus, their Fourier coefficients are absolutely summable, and
`chi=sum_r b_r d_r^5` exactly. The finite-torus convolution kernel is the
periodization of those coefficients, so

\[
\|b_r(T)\|_{\ell^1\to\ell^1}
 \le\sum_{k\in\mathbb Z^4}|\widehat b_r(k)|,
\tag{F3}
\]

uniformly in L. Five successive applications of the fundamental theorem
of calculus give

\[
D_r^5 f_h(hx)=\int_{[0,h]^5}
 \partial_r^5f_h(hx+(t_1+\cdots+t_5)e_r)\,dt_1\cdots dt_5.
\]

Thus `||D_r^5 f_h(h dot)||owner,1 <= L4 h5 M5 = h M5`.
Apply (F3) and the exact factorization to obtain (F2), with
`C_chi=sum_r sum_k |hat b_r(k)|`.

This proves only the part selected by a **fixed** multiplier chi.
The remaining `(I-chi(T))R_h` includes mesoscopic and macroscopic output,
and products of fast links can contribute to it. There is no uniform
claim for an h-dependent shrinking cutoff. The decomposition is an analysis
tool; it changes neither the action nor the admissible class.

For example the abstract response field `f_h=h4 e_23` is uniformly smooth,
has zero eta-trace and zero fixed fast part, but its raw sum is one on
every grid. It is not an A4D witness because no exact shared-link root is
constructed. It proves that C5 regularity, fast suppression and a signed
trace constraint alone cannot bound the remaining absolute sum.

## 16. The fixed-source endpoint is a finite comparator-jet gate

The #216 smooth-seminorm construction supplies an expansion through each
fixed order. Write its first five normalized response coefficients as

\[
\rho_{sm,h}(y)=\rho_0(y)+h\rho_1(y)+h^2\rho_2(y)
                 +h^3\rho_3(y)+h^4\rho_4(y)+O(h^5),
\qquad \rho_0=-G[g]/2.
\tag{J1}
\]

Assume one fixed smooth source tau and a nonempty subsequence of exact
roots on this fixed background and with this comparator. By the exact
source equation (F1), the desired raw normalized convergence holds on
that subsequence **if and only if**

\[
\boxed{\tau=\rho_0,\qquad \rho_1=\rho_2=\rho_3=\rho_4=0.}
\tag{J2}
\]

To prove necessity, let k be the first nonzero coefficient of
`tau-rho_sm,h` among orders zero through four. Uniformity of (J1) and
Riemann sums imply

\[
\lim_{h\to0}h^{4-k}\|R_h\|_{owner,1}
 =\int_{\mathbb T^4}\|d_k(y)\|_{owner,1}\,dy>0,
\tag{J3}
\]

where `d_0=tau-rho_0` and `d_k=-rho_k` for k>0. Therefore the raw gap
diverges if k<4, and has a strictly positive finite limit if k=4.
Conversely (J2) makes the per-site normalized difference O(h5), so its
raw sum is O(h). This proves sufficiency. The proof retains absolute
values and works on any refining rooted subsequence, including L in 4N.

The gate is a consequence of the already declared topology and exact
sampling. It is not a replacement source convention, a source-feasibility
theorem or a NO-GO. In particular `tau=-G/2` alone proves only the order-zero
condition. To close the original task positively, the full shared-link
source-image theorem must force all of (J2) on every nonempty admissible
fixed-source class. To close negatively, exhibit an exact admissible rooted
subsequence for which one of these coefficients is nonzero. No such
nonconstant-background witness is asserted here.

## 17. Hostile pullback control: coframe-gradient channels cannot all be discarded

The positive estimate (S1) cancels envelope transport in the frozen reduction.
The following exact control tests its proposed direct coframe extension on
the already owned two-shear coframe path. It does not construct a new lattice
family or a prescribed-source witness.

At one point put `S=I`, `B=E10+E21`, and use the local affine jet
`S_eps(x)=I+eps*x_mu*B` for each physical direction mu. This is a local
smooth jet; it is not asserted to be a globally periodic metric. First
solve the complete zero-character background connection equation

\[
H(1)k=-f_{solder},\qquad \det H(1)=256.
\tag{P1}
\]

For each owned quarter center insert
`exp(eps*k_r) exp(delta*i^(sum x)*T_r(S_eps(x)))`, together with its
conjugate for real amplitudes. Assemble the eps*delta coefficient from
all outgoing and incoming literal plaquettes. This retains the derivative
of the face weight, the derivative of the center generator at the actual
link base, and the background connection transport. Apply the owned
twenty-column normal elimination and its lower fourteen complex rows;
let `U_mu` be the resulting 28 by 8 real subprincipal map.

The checker verifies that the order-eps background Euler coefficient
vanishes, that every frozen quarter center is in the full joint kernel,
and that its four independently reconstructed G_mu matrices agree with
the pinned owner. Thus U_mu is the combined first-gradient term, rather
than one isolated derivative of a frame-dependent detector.

With the sixteen-row N of (S2), the exact ranks are

\[
(\operatorname{rank}(NU_0),\operatorname{rank}(NU_1),
 \operatorname{rank}(NU_2),\operatorname{rank}(NU_3))=(4,0,4,4).
\tag{P2}
\]

For `mu=3`, the existing identity (S3) with coordinate i=1 and metric
slot j=00 has, at `c=e_a1+e_b2`, the exact contraction

\[
Q_2(c)=0,\qquad
\boxed{\sum_\alpha H_{1,00,\alpha}(c)(NU_3c)_\alpha
       =-409/1980.}
\tag{P3}
\]

The extra coframe term in these **particular** saved multipliers therefore
cannot be replaced by a controlled quadratic source product: (P3) is
nonzero on the real source-zero cone. Other covariant multipliers or a
full-field estimate are not excluded by this control.

A stronger quotient control clarifies why simply projecting out every
such gradient term would lose the observable. The real span of the columns
of all four G_mu and all four U_mu has rank twenty. Its common left
annihilator `N_ext` has eight rows. At both real atoms
`c=e_a1+e_b2` and `c=e_a1+e_b3`,

\[
Q_2(c)=0,\qquad N_{ext}Q_3(c)=0,\qquad R_4(c)\ne0.
\tag{P4}
\]

Consequently no bound of the form (S1) using only this extended projected
gate and Q2 can hold for all real c. Multiplying those vanishing gates by
additional polynomial coefficients or saturating by a nonzero amplitude
coordinate cannot recover the nonzero readout. This excludes one linear
detector that removes **all four** gradient-direction maps simultaneously;
it does not exclude a detector depending on the actual coframe jet or a
nonlinear full shared-link estimate.

These atoms have nonzero `NQ3`, and are not exact joint roots. For mu=3,
the real source-zero kernel of NU3 also contains `e_a1+e_b3` and
`-e_a3+e_b1`, with
`R4=(1/16,0,-1/8,0,0,0,0,1/16,0,0)` and nonzero NQ3. These facts prevent
any promotion of the control to a fixed-source NO-GO. The exact physical
equations retain the cubic gates and the coframe channels together.

The remaining proof must control their actual observable contribution
on the realizable shared-link/source set, rather than erase it before
imposing those equations. The original task remains `PARTIAL / OPEN`.

Replay and explicit local jets:

```sh
python 02_REGISTRY/research/certificates/a4d_two_shear_subprincipal_pullback_check.py
```

Local validation of Sections 14–17: both new pinned checkers pass, including
the independent literal coframe-gradient replay (46.6 seconds). Repository
architecture, generated views, active work, agent protocol, claim-strength,
formalization debt, certificate freshness, actual Draft PR contract, Python
compilation and whitespace checks pass. Input ac022ee completed D0 guards
run 37140352047 successfully. New-head CI is reported separately.
