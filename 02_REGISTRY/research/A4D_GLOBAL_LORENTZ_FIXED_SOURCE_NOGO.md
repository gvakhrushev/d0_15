# A4D full-Lorentz fixed-curved-source refusal

Task: EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, Draft PR #310.
Input head for the signed Q8 integration: 720dee65f8c1c186f5862602a4723486eff4b566.
Status: **exact nonlinear NO-GO on the stated full configuration domain**.
The original task's sufficiently small identity chart remains **OPEN**.
No admissibility restriction, action term or source convention is changed.

## 1. One fixed geometry, one fixed source, actual exact roots

Fix before selecting links

\[
 f(y_1)=1+\frac{1-\cos(2\pi y_1)}{50},\qquad
 E(y)=\operatorname{diag}(1,1,f,f),\qquad
 g(y)=E(y)^T\eta E(y)=\operatorname{diag}(1,-1,-f^2,-f^2),
 \quad \eta=\operatorname{diag}(1,-1,-1,-1).
 \tag{1}
\]

Use exact samples $g_h(x)=g(hx)$ on $X_L=(\mathbb Z/L)^4$,
$h=1/L$, $L\in4\mathbb N$. The metric is smooth, nondegenerate,
nonconstant and genuinely curved. Prescribe the single fixed smooth source
$\tau(y)=0$, with uniformly bounded derivatives of every order.

**Theorem.** Explicit physical links $U_{x,r}\in SO^+(1,3)$ exist on every
such mesh and satisfy the literal full equations exactly:

\[
 E_K(g_h,U_h)=0,\qquad H(g_h,U_h)=0,\qquad
 \Xi(g_h,U_h)=h^2\tau(hx)=0.
 \tag{2}
\]

All 24 shared-link rows and all 16 unrestricted solder partials vanish.
The links have nontrivial, gauge-invariant plaquette holonomies.
For the designated #216 smooth comparator, put

\[
 \mathcal G_h=h^{-2}
       \|\Xi(g_h,U_h)-\Xi(g_h,U_h^{\rm sm})\|_{\mathrm{owner},1}.
\]

Then

\[
 h^4\mathcal G_h\longrightarrow
 C_0=\int_{\mathbb T^4}\|\rho_0[g](y)\|_{\mathrm{packed},1}\,dy
 \ \ge\ \frac{\pi^2}{2500}>0.
 \tag{3}
\]

Thus $\mathcal G_h$ diverges like $C_0h^{-4}$. Even the volume-normalized
response gap has a positive limit. The actual normalized response of
(2) is identically zero and differs from the nonzero Einstein response of
the one fixed curved metric (1).

The theorem is on the full finite proper-Lorentz, nondegenerate configuration
domain of the [nonlinear quotient owner](MEMO_A4D_STAR_DENSITY_LORENTZ_NONLINEAR_QUOTIENT.md),
Sections 1--2 and 9. Its raw row solder is $\Theta=E^T\eta$, so its Gram
$\Theta\eta\Theta^T$ is exactly (1). This is a concrete realization in that
domain, not an appeal to an untyped native carrier. A universal transfer
from **every state in this domain** to the Einstein response, preserving
instantaneous response fidelity, is therefore false.

The construction contains finite rotations by $\pi$. It lies outside the
small identity chart in [H-DOMAIN](A4D_J2_METRIC_RESPONSE_SENSITIVITY.md),
and outside the log-$O(h)$ domain of the
[finite-probe theorem](A4D_NATIVE_FINITE_PROBE_COMPLETION.md).
It is not labeled the original task's small-chart terminal and does not
retire that task.

## 2. The face-level identity

Keep the unchanged action face

\[
 \ell_{rs}(E,P)=
 \operatorname{orient}(r,s)
 \langle e_u\wedge e_v,*b(C(P))\rangle_{G_2},
 \qquad C(P)=\tfrac12(P-P^{-1}),
 \tag{4}
\]

with its owned star, orientation, bivector convention and complementary
pair $(u,v)$. At a diagonal solder
$E=\operatorname{diag}(d_0,d_1,d_2,d_3)$, the weight in (4) selects only
the internal $(r,s)$ bivector component. Its coefficient is nonzero if
the diagonal entries are nonzero.

Let $P=\operatorname{diag}(p_0,p_1,p_2,p_3)\in SO^+(1,3)$ be an involution,
and require

\[
 p_r+p_s=0.
 \tag{5}
\]

Since $P=P^{-1}$, $C(P)=0$. Every unrestricted solder derivative of
(4) is therefore zero, including all off-diagonal variations.
For a genuine right plaquette variation $\delta P=PX$,
$X\in\mathfrak{so}(1,3)$,

\[
 \delta C=\tfrac12(PX+XP^{-1})=\tfrac12(PX+XP),\qquad
 (\delta C)_{rs}=\tfrac12(p_r+p_s)X_{rs}=0.
 \tag{6}
\]

Thus the entire face momentum covector $\Pi_{rs}[X]$ is zero for all six
generators, not just for one allowed link variation. Every shared-link
variation is a transported plaquette tangent; the sum of its face
contributions is consequently zero. This proves the connection part of
(2) without freezing neighboring weights or dropping any row.

The source-null statement alone would not prove this: an involution with
$p_r+p_s\ne0$ still has $C=0$, but has a nonzero face momentum. The exact
certificate retains that hostile control.

## 3. One periodic field realizes all six face assignments

Use the proper spatial rotation group

\[
 V_4=\{I,R_1,R_2,R_3\},\qquad
 R_1=\operatorname{diag}(1,1,-1,-1),\quad
 R_2=\operatorname{diag}(1,-1,1,-1),\quad
 R_3=\operatorname{diag}(1,-1,-1,1).
 \tag{7}
\]

Each $R_i$ is a genuine spatial rotation by $\pi$ with determinant one
and unchanged positive time orientation. These are commuting order-two
Lorentz matrices. Predetermine the six face values

| Face $(r,s)$ | $P_{rs}$ |
|---|---|
| $(0,1)$ | $R_3$ |
| $(0,2)$ | $R_3$ |
| $(0,3)$ | $R_2$ |
| $(1,2)$ | $R_2$ |
| $(1,3)$ | $R_3$ |
| $(2,3)$ | $R_3$ |

Each satisfies (5). Define actual links by

\[
 U_{x,r}=\prod_{s<r}P_{sr}^{\,x_s}.
 \tag{8}
\]

The empty product is $U_{x,0}=I$. Because $L$ is even and all factors
have order two, (8) is periodic in every coordinate. Commutativity gives
the actual four-factor product

\[
 U_{x,r}U_{x+e_r,s}U_{x+e_s,r}^{-1}U_{x,s}^{-1}
 =P_{rs}\qquad(r<s)
 \tag{9}
\]

at every site, including periodic seams. This supplies true shared links;
the faces are not independently prescribed curvature variables.
Equations (5)--(9) prove (2) on every mesh for **any** nondegenerate
diagonal solder field, irrespective of its spatial variation. In particular
they prove it on the fixed curved samples (1).

### 3.1 The same field has an actual signed native Q8 lift

The rotations in (7) need no external angular constant to construct.
Use the owned multiplication table
[Q8DedekindMinimality](../../03_FORMALIZATION/D0/Claims/Q8DedekindMinimality.lean)
and its signed Role equivalence/cocycle
[Omega8Q8TypedBridge](../../03_FORMALIZATION/D0/Representation/Omega8Q8TypedBridge.lean).
On the real quaternion basis, define

\[
 {\cal R}(q)=\operatorname{diag}
       (1,\operatorname{Ad}_q|_{\operatorname{Im}\mathbb H}),
 \qquad \operatorname{Ad}_q(v)=qvq^{-1}.
\]

Then

\[
 {\cal R}(i)=R_1,\quad {\cal R}(j)=R_2,\quad
 {\cal R}(k)=R_3,\qquad
 \ker{\cal R}=\{1,-1\}.
\]

All matrix entries are integers. The words use precisely the owned
relations $i^2=j^2=k^2=-1$, $ij=k$, $ji=-k$; no value of classical
$\pi$ or of $\pi_0$ enters them. Calling an image a half-turn is its
smooth geometric description, not a transcendental input to the word.

Set $q_{03}=q_{12}=j$ and the four remaining $q_{rs}=k$. Keep the order

\[
 u_{x,r}=\prod_{s=0}^{r-1}q_{sr}^{\,x_s},
 \qquad U_{x,r}={\cal R}(u_{x,r}).
\]

Every factor has order four, so $u$ is genuinely periodic on
$L\in4\mathbb N$, including each seam. The adjoint representation is
a homomorphism and gives exactly (8). Its actual four-link quaternion
plaquettes are

\[
 u_{x,r}u_{x+e_r,s}u_{x+e_s,r}^{-1}u_{x,s}^{-1}
   =\sigma_{x,rs}q_{rs},\qquad \sigma_{x,rs}\in\{1,-1\}.
\]

Every lifted face is noncentral and squares to -1, retaining the
owned anisotropic self-return of Q8 rather than a native null ray.
These signs are computed from the noncommuting words and retained,
not silently replaced by independent face data. The literal certificate
checks all 64 signed Role-cocycle products against the actual owned table,
all 1024 lifted links and all 1536 lifted faces at $L=4$, including both
signs. Its all-mesh extension follows from the displayed words and
order-four periodicity. The projected field is still the exact full
stationary/source-null field (2), tested against every physical Lorentz
tangent, not merely against the finite subgroup.

This supplies an actual **Q8 carrier preimage** of the existing
counterexample. It does not establish the remaining native admissibility,
metric realization, gravitational-response descent or interlevel
operator conditions for arbitrary D0 states. In particular, the central
Q8 orientation record is not identified with every earlier response-visible
amplitude sign. Minimality of Q8 and closure of $\pi_0$ therefore cannot
by themselves exclude this field; an exclusion would need an actual
native admissibility theorem beyond those carrier identities.

## 4. Gauge quotient and the unavoidable chart boundary

For every face in (9),

\[
 \operatorname{tr}P_{rs}=0,\qquad
 \chi_{P_{rs}}(z)=(z-1)^2(z+1)^2,
 \tag{10}
\]

whereas the identity has trace four. Proper Lorentz node gauges conjugate
the based holonomy. The invariants (10) prove that the field cannot be
gauged to the identity field. Its accepted odd extraction $C$ vanishes;
its actual holonomy remains nontrivial. These statements are kept distinct.

The gauge action and the nondegenerate solder quotient are exactly those
already owned; no extra quotient identifies (10) with the identity.
The literal certificate also checks a nonconstant proper-Lorentz node
dressing across a periodic seam, preserving the same Gram and zero face
momenta.

No gauge can turn this family into a log-$O(h)$ field. If four physical
face links have logarithms bounded by $Rh$ in a submultiplicative norm,

\[
 \|P-I\|\le e^{4Rh}-1\longrightarrow0.
 \tag{11}
\]

But (10) implies $\rho(P-I)=2$, so $\|P-I\|\ge2$ in every node gauge.
Likewise a sufficiently small fixed identity-log chart excludes the field.
Nonidentity links have $\det(I+U)=0$, outside the identity Cayley chart.
This is an invariant scope boundary, not a missing coordinate choice.

## 5. Fixed-source continuum discrepancy

Reuse the globally identified canonical comparator of
[the finite-probe synthesis](A4D_NATIVE_FINITE_PROBE_COMPLETION.md#5-global-action-limit-and-its-ten-component-variation).
In the ten packed Gram slots
$(00,01,02,03,11,12,13,22,23,33)$ its leading raw covector is, with
$p=f'$ and $q=f''$,

\[
 \rho_0[g]=
 (-fq-p^2/2,0,0,0,p^2/2,0,0,q/(2f),0,q/(2f)).
 \tag{12}
\]

Sign, density, both raised indices and off-diagonal weights are those of
[the fixed-source owner](A4D_FIXED_SOURCE_ALGEBRAIC_COMPATIBILITY.md).
The owned reconstruction is $-G[g]/2$. The comparator obeys

\[
 h^{-2}\Xi(g_h,U_h^{\rm sm})(x)=\rho_0[g](hx)+O(h)
 \tag{13}
\]

uniformly on this one smooth metric. With (2),

\[
 \mathcal G_h=\sum_x\|\rho_0[g](hx)+O(h)\|_{\mathrm{packed},1}.
 \tag{14}
\]

Riemann sums and the Lipschitz property of a fixed norm give (3).
The $11$ slot alone has integral

\[
 \int_{\mathbb T^4}\frac{p^2}{2}\,dy
 =\frac12\left(\frac{2\pi}{50}\right)^2
              \int_0^1\sin^2(2\pi y_1)\,dy_1
 =\frac{\pi^2}{2500}.
 \tag{15}
\]

The exact roots exist, the smooth source is fixed in advance, the
background is curved, and separation survives continuum volume
normalization. None of the fixed-source/curved/continuum defects of the
older shrinking flat-source witness occurs here. The distinction from the
original task is precisely the link-chart domain.

There is no contradiction with the arithmetic theorem: it excludes this
metric's exact **Einstein** source, whereas (2) uses the independently
specified vacuum source zero.

## 6. Relation to finite probes and theory closure

The positive small-log action-probe completion remains valid. An exact
open probe family or a compatible recording tower strengthens that
measurement construction; it does not turn the different source
$\Xi=0$ in (2) into (12).

For this witness the central normalized action is exactly zero on every
mesh, while the canonical smooth limit is $I(g)=\pi^2/1250>0$.
Small-log action stability therefore cannot apply. If a centered protocol
keeps this central state but chooses small-log endpoints independently,
the central action cancels algebraically. Its finite Einstein output would
be a coarser measurement, with no fidelity to this state's instantaneous
source. Separate one-sided readings have leading opposite terms
$\pm I(g)/\epsilon$ and cannot both approach the same continuum response.

A universal full-domain source/response transfer preserving raw response
is therefore ruled out by a realizable exact state. Restricting a physical
theory to a small identity-holonomy sector requires an independently
justified native admissibility statement. Such a statement is not inserted
here and is not supplied merely by a choice of chart.

Verdict for the explicit full domain:
**FULL-LORENTZ-FIXED-CURVED-SOURCE-RESPONSE-NOGO**.
Disposition of the original small-chart task: **PARTIAL / OPEN**, Draft.
No public claim, Lean owner or task lifecycle terminal is promoted.

## 7. Reproducible exact certificate

[The full replay](certificates/a4d_global_lorentz_fixed_source_v4_check.py)
uses exact rational arithmetic and the existing literal matrix/star owner.
[Its pinned output](certificates/a4d_global_lorentz_fixed_source_v4_results.json)
records one $L=4$ curved sample:
1536 actual based plaquettes, 6144 shared-link Euler rows,
4096 unrestricted solder rows and 2560 Gram rows, all exactly zero.
The same replay now retains the owned signed Q8 lift of that field.
It checks every face's six momenta and every transported edge contribution,
the true Gram lift, a wrong-involution hostile control and an actual
nonconstant Lorentz dressing. Involutions and (8)--(9) prove the all-mesh
extension; no finite-grid extrapolation is used.
