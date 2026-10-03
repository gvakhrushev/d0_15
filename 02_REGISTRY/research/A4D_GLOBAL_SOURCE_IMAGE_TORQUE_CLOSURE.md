# A4D global source image: all-role current and transport obstruction

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Input head: `551eba1a84fe15ebdcd100b90348f291bd109692`.
Canonical main: `e80a3b1ccf615fb4f70bf5900181592604928497`.
Status: exact all-field current identity and local transport theorem;
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
