# A4D finite action probes: a constructive Einstein observable completion

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input head: `aed0db1782184e8318cf9b150e5134be6800b177`.
Exact-endpoint and detector extension input:
`f317a3b842b2d10c5a3a381b6b03cb9850e77f66`; independently audited
on `f4f88161325574e4c5750e0af4a8cc14a2f4b48e`.
Status: **analytic theorem for the explicitly defined action-probe observable**.
This is a completed construction, not a conjectured constant-readout premise
and not a new Lean owner. The original fixed-source, raw-owner response task
remains `PARTIAL / OPEN`.
The local observable germ below is the leading continuum metric response;
it does not assert recovery of every subleading coefficient of the formal
mesh-power stationary germ from arbitrary rough states.

## 1. The result and the finite experiment

Fix one smooth periodic, oriented and time-oriented nondegenerate metric
$g$ on the unit four-torus, an owned smooth Lorentz solder representative,
and one smooth symmetric covariant metric probe $V$. These are specified
before selecting a connection. Choose $s_0>0$ so that the pencil
$g_s=g+sV$, $|s|\le s_0$, stays in a compact nondegenerate Gram section.
All constants refer to this one fixed experiment.

Let $h=1/L$, $L\in4\mathbb N$. Write $\mathscr A_h(g_s,A)$ for the unchanged
literal naked-star counting action, with physical links $U=\exp A$,
all six based faces and all four shared-link positions retained. Set

\[
 I_h(g_s,A)=h^2\mathscr A_h(g_s,A).
 \tag{1}
\]

For fixed finite constants $R,M$, the experimental preparation domain is

\[
 \mathcal P_h(g_s;R,M)=
 \{A:\|A\|_\infty\le Rh,\quad
          \|E_K(g_s,\exp A)\|_\infty\le Mh^2\}.
 \tag{2}
\]

The residual includes **all 24 physical connection Euler rows per site**.
There is no derivative bound, Fourier restriction, prescribed stationary
sheet, or curvature constraint on an unknown member. Every exact full
stationary log-$O(h)$ family belongs for its fixed log constant $R$, enlarged
if necessary to include the explicit preparations below. Uniformity is
proved for each fixed $R,M$, not over an unbounded union of log constants.
Domain (2) is an auxiliary preparation domain; it does not redefine the
parent's exact joint/source admissibility.

For $0<\epsilon\le s_0$, retain a triple

\[
 (A_0,A_+,A_-)\in
 \mathcal P_h(g;R,M)\times\mathcal P_h(g_{+\epsilon};R,M)
                         \times\mathcal P_h(g_{-\epsilon};R,M).
 \tag{3}
\]

Read the actual central and endpoint actions, and form

\[
 D_h^+=\frac{I_h(g_{+\epsilon},A_+)-I_h(g,A_0)}\epsilon,
 \qquad
 D_h^-=\frac{I_h(g,A_0)-I_h(g_{-\epsilon},A_-)}\epsilon,
\]
\[
 T_{h,\epsilon}=\frac{D_h^++D_h^-}{2}
 =\frac{I_h(g_{+\epsilon},A_+)-I_h(g_{-\epsilon},A_-)}{2\epsilon}.
 \tag{4}
\]

The finite record retains $A_0$, its curvature and its original sitewise
$\Xi$; cancellation of its scalar action in (4) is exact. Endpoints are
chosen independently. Continuation of a particular singular stationary
branch is not part of this experiment.

**Theorem.** Domain (2) is constructively nonempty at every probe metric
for suitable predeclared $R,M$. Uniformly over **all** triples (3),

\[
 \left|T_{h,\epsilon}
 +\frac12\int_{\mathbb T^4}\sqrt{|g|}\,
                   G^{\mu\nu}[g]V_{\mu\nu}\,dy\right|
 \le C\left(\frac h\epsilon+\epsilon^2\right).
 \tag{5}
\]

Here $G$ uses the literal owner's curvature sign and index/density
reconstruction specified in Section 2. With $\epsilon=h^{1/3}$,

\[
 \sup_{(3)}|T_{h,h^{1/3}}-DI(g)[V]|\le Ch^{2/3},
 \qquad
 I(g)=\frac12\int_{\mathbb T^4}\sqrt{|g|}R[g]\,dy.
 \tag{6}
\]

The geometric measurement completion therefore has one output, obtained
as a limit of finite action readings. Sections 6--7 construct this limit
and its native catalogue instance. A fixed finite list of probes gives a
finite response vector; all smooth probes identify the Einstein distribution.
Section 8 gives a predeclared localization schedule for its ten components.

The factor $h^2=h^4h^{-2}$ in (1) is the integral action normalization.
It is not a change to the parent's unweighted owner norm of $\Xi$.

### 1.1 The centered theorem extends to unrestricted physical central states

Let \(\mathcal L_h(g)\) be all finite physical Lorentz link fields on the
fixed sampled metric, using matrices directly when no log exists. Replace
only the first factor of (3) by \(\mathcal L_h(g)\). The central action is
finite for every member. Equation (4) cancels that action identically;
the proof of (5) bounds only the two endpoint actions. Hence (5)--(6)
hold with the same constants, uniformly over
\[
 \mathcal L_h(g)\times\mathcal P_h(g_{+\epsilon};R,M)
                  \times\mathcal P_h(g_{-\epsilon};R,M).
 \tag{6a}
\]
No equation, chart, derivative or amplitude bound on the central state is
needed. This extends the centered observable only. The separate one-sided
increments and central stationary-action stability retain their original
hypotheses. The [signed full-Lorentz curved joint vacuum](A4D_GLOBAL_LORENTZ_FIXED_SOURCE_NOGO.md)
therefore has a valid centered Einstein completion while retaining its
zero instantaneous response. Reusing the same central record in both
increments cancels its measurement error as well. If endpoint action
records have errors \(e_+,e_-\), their added centered error is at most
\((|e_+|+|e_-|)/(2\epsilon)\), independently of the central record.

The [phi/pi0 integration](A4D_PHI_PI0_CONTINUUM_CLOSURE.md#2-an-actual-golden-cauchy-sequence-of-readings)
gives an explicit, predeclared mesh schedule on which these actual readings
satisfy the step premise of the owned GoldenTower Cauchy theorem. It adds
no connection-holonomy selector and does not prove the original raw norm.

## 2. Literal action, Gram lift and curvature convention

Use $\eta=\operatorname{diag}(1,-1,-1,-1)$ and $g=E^T\eta E$,
$\det E=\sqrt{|\det g|}>0$. Write $e^a=E^a_\mu dy^\mu$.
An exact smooth lift of the metric pencil is

\[
 E_s=E\sqrt{I+s g^{-1}V}.
 \tag{7}
\]

The analytic square root exists for small $s$; $g^{-1}V$ is
$g$-self-adjoint, so (7) has Gram exactly $g+sV$. A different owned
smooth section differs by a proper Lorentz gauge. All finite transitions
are retained. A frame-dressed matrix is not assumed to be $\eta$-Lorentz.

The actual based plaquette and its odd part are

\[
 P_{x,rs}=U_{x,r}U_{x+e_r,s}U_{x+e_s,r}^{-1}U_{x,s}^{-1},
 \qquad C_{x,rs}=(P_{x,rs}-P_{x,rs}^{-1})/2.
\]

The literal face summand is
$\operatorname{orient}(r,s)
 \langle e_u\wedge e_v,*b(C_{rs})\rangle_{G_2}$,
with the complementary ordered pair $(u,v)$,
$b(X)^{ab}=X^a{}_c\eta^{cb}$ for $a<b$, and the existing owner's `STAR`,
$G_2$ and orientation. Code indices `[a,b]` label this contravariant
internal bivector; they do not lower its indices.
For $F=d\omega+\omega\wedge\omega$ define

\[
 R[g]=-E_a^\mu E_b^\nu(F_{\mu\nu}\eta)^{ab},
 \qquad G=\operatorname{Ric}-\tfrac12Rg.
 \tag{8}
\]

Both antisymmetric pairs in (8) are fully summed. This scalar sign is
opposite to $R^\rho{}_{\sigma\mu\nu}
=+E_a^\rho F_{\mu\nu}{}^a{}_b E^b_\sigma$ in the fixed-source arithmetic
memo. The entire owned curvature convention is
$R^\rho{}_{\sigma\mu\nu}
=-E_a^\rho F_{\mu\nu}{}^a{}_b E^b_\sigma$,
$\operatorname{Ric}=-\operatorname{Ric}_{\rm standard}$ and
$G=-G_{\rm standard}$; only the scalar is not flipped in isolation.
Thus the raw covariant Gram dual is
$-\sqrt{|g|}\operatorname{pack}(G^{\mu\nu})/2
=+\sqrt{|g|}\operatorname{pack}(G_{\rm standard}^{\mu\nu})/2$.
Off-diagonal packed slots carry the existing factor two. The owned
index/density reconstruction yields $-G/2$.

The retained warp $E=\operatorname{diag}(1,1,f,f)$ pins the convention:
$\omega_2=-f'J_{12}$, $\omega_3=-f'J_{13}$, and

\[
 R=-4f''/f-2(f')^2/f^2,
 \qquad \tfrac12\sqrt{|g|}R=-2ff''-(f')^2.
 \tag{9}
\]

## 3. Full smooth Palatini germ and explicit endpoint preparations

The [all-solder recurrence](A4D_CANONICAL_CONSTITUTIVE_GERM_SYNTHESIS.md)
uses the actual zero-phase block, with

\[
 (E^T\otimes I_6)^T H_E(0)(E^T\otimes I_6)
       =\det(E)H_I(0),\qquad \det H_I(0)=256.
 \tag{10}
\]

On the fixed compact solder family its inverse is uniformly bounded.
Expansion of the full incoming/outgoing Euler stencil at $A=h\omega$
shows that its order-$h$ coefficient is the Palatini connection equation
of the continuum face density:

\[
 D_\omega(e^a\wedge e^b)=0
 \quad\Longleftrightarrow\quad
 e^a\wedge T^b-e^b\wedge T^a=0,
 \qquad T^a=de^a+\omega^a{}_b\wedge e^b.
 \tag{11}
\]

To identify all rows, expand the actual log-coordinate Euler formula
at $A=h\omega$ as $F_h=hq_E(e,\omega)+O(h^2)$. For every arbitrary smooth
24-component connection test $\delta\omega$, the exact finite chain rule is
$D_\omega(h^2\mathscr A_h)[\delta\omega]
=h^3\sum_x F_h:\delta\omega(hx)$, tending to
$\int q_E:\delta\omega$. Differentiating the smooth four-factor face
expansion gives the Palatini first variation of the same leading density.
The fundamental lemma identifies $q_E$ componentwise with its Euler field.
The alternating tensor and star are invertible on bivectors, so (11)
contains all 24 rows. Shifted coframe values on incoming faces are retained;
the derivative terms of $e$ are not frozen away.

For completeness (11) forces zero torsion. Let $i_b$ denote contraction by
the dual frame and $\theta=\sum_b i_bT^b$. Summing $i_b$ in (11) gives
$T^a-e^a\wedge\theta-2T^a=0$, hence
$T^a=-e^a\wedge\theta$. Contracting again gives $\theta=-3\theta$,
so $\theta=0$ and $T=0$. The unique $\eta$-skew torsion-free connection
is the Levi-Civita spin connection. Therefore the first recurrence
coefficient is $A_1=\omega_{\rm LC}[g_s]$ on the entire smooth coframe,
not only at a normal-$J^2$ center.

Use the explicit finite preparations

\[
 B_h(s,hx)=h\omega_{\rm LC}[g_s](hx),\qquad
 U^{\rm prep}_{x,r}(s)=\exp B_{h,r}(s,hx).
 \tag{12}
\]

Substitution into the **same full finite Euler formula** cancels its
order-$h$ coefficient. Finite-stencil Taylor bounds, uniform in $s$, give

\[
 \|B_h(s)\|_\infty\le R_Bh,\qquad
 \|E_K(g_s,\exp B_h(s))\|_\infty\le M_Bh^2.
 \tag{13}
\]

Choose $R\ge R_B$, $M\ge M_B$ before an arbitrary candidate. Equations
(12)--(13) prove nonemptiness of every endpoint domain, and projection
of (3) onto any allowed central state is surjective. No exact-root theorem
or metric-source solvability theorem is used for preparations.

These preparations can also be generated from finite sampled metric/solder
data. Replace the first derivatives entering $\omega_{\rm LC}$ by periodic
centered differences on the same mesh. On each fixed smooth pencil the
derivative error is $O(h^2)$, hence the log changes by $O(h^3)$.
The full local Euler stencil is uniformly Lipschitz in sup norm, so its
residual remains $O(h^2)$. This supplies a finite-data implementation of
the experiment without an oracle for exact derivatives or an exact root.

Higher accuracy is constructive too. The unique recurrence gives
$B_h^{[N]}=\sum_{j=1}^Nh^jA_j$, whose actual exponentials have full-row
residual $O(h^{N+1})$ in sup norm, or $O(h^{N-3})$ in counting sum.
Thus $N\ge q+3$ supplies full counting residual $O(h^q)$.
The uniform parameter-smooth Borel construction packages every fixed order
at once, but no infinite sum is required for (5).

## 4. Rough full-field action stability

Let $F_h=\nabla_A\mathscr A_h$ be the log-coordinate gradient. The
block derivative of the exponential map relates it to the physical
right-trivialized $E_K$. In the shrinking log ball this coordinate map
and its inverse have uniformly bounded norms, independently of lattice size.

For two arbitrary rough log fields $A,B$, both of size at most $Rh$, put
$D=A-B$, $f(t)=\mathscr A_h(g_s,B+tD)$ and
$e_A=\|E_K(g_s,\exp A)\|_\infty$, similarly $e_B$.
Exact integration by parts gives

\[
 f(1)-f(0)=\tfrac12[f'(0)+f'(1)]
             -\tfrac12\int_0^1t(1-t)f'''(t)\,dt.
 \tag{14}
\]

Endpoint pairings and local analyticity imply

\[
 |f'(0)|+|f'(1)|\le C(e_A+e_B)\|D\|_{\mathrm{owner},1},
 \qquad
 |f'''(t)|\le C\|D\|_\infty^2\|D\|_{\mathrm{owner},1}.
 \tag{15}
\]

For the second bound, each face uses four links. Bound two directional
factors by the supremum and sum the third over links, using their fixed
face-incidence multiplicity. All solder weights and local analytic
derivatives are uniformly bounded. No spatial derivative of $A$ is used.
Since $\|D\|_\infty\le2Rh$ and
$\|D\|_{\mathrm{owner},1}\le24h^{-4}(2Rh)$, (14) gives

\[
 |I_h(g_s,A)-I_h(g_s,B)|
 \le C\left(h+\frac{e_A+e_B}{h}\right).
 \tag{16}
\]

In particular all of (2) has action diameter $O(h)$, and comparison with
(12) is uniform on the full preparation domain, including exact rough UV.
This controls scalar critical values without a full UV inverse.

There is an independent Taylor proof of the cancellation. Set $N_h=h^{-4}$.
For the actual symmetric full Hessian $H_h$ at identity, locality gives

\[
 \mathscr A_h(A)=\ell_h\cdot A+\tfrac12A^TH_hA+O(N_hh^3),
 \qquad F_h(A)=\ell_h+H_hA+O(h^2).
\]

Cross-pair the two $O(h^2)$ Euler equations with $B$ and $A$.
Symmetry cancels $A^TH_hB$, yielding
$\ell_h\cdot(A-B)=O(N_hh^3)$. Own pairings give
$\mathscr A_h(A)=\ell_h\cdot A/2+O(N_hh^3)$, and similarly for $B$.
Multiplication by $h^2$ gives $O(h)$. This is the true scalar-action
Hessian, not an untyped transpose of a complex Fourier block.

## 5. Global action limit and its ten-component variation

For the smooth preparation (12), actual four-factor multiplication gives

\[
 P_{rs}(y)=I+h^2(\partial_r\omega_s-\partial_s\omega_r
                                  +[\omega_r,\omega_s])+O(h^3),
 \qquad C_{rs}=h^2F_{rs}+O(h^3).
 \tag{17}
\]

The same leading coefficient holds with higher recurrence terms: the
order-$h^2$ log coefficient cancels from the leading closed face.
The literal alternating contraction is

\[
 \sum_{r<s}\operatorname{orient}(r,s)
 \langle e_u\wedge e_v,*b(F_{rs})\rangle_{G_2}
 =-\frac{\det E}{2}E_a^\mu E_b^\nu(F_{\mu\nu}\eta)^{ab}
 =\tfrac12\sqrt{|g|}R[g].
 \tag{18}
\]

At $E=I$ each of the six matched complementary face/internal-generator
pairs contributes $+1$. The determinant identity
$\epsilon^{\mu\nu\rho\sigma}E^a_\rho E^b_\sigma
=\det(E)\epsilon^{cdab}E_c^\mu E_d^\nu$
transports these coefficients and proves (18) for every invertible $E$.
This also agrees with
the pinned warp (9). Thus periodic Riemann summation gives

\[
 I_h(g_s,B_h)=h^4\sum_x\tfrac12\sqrt{|g_s|}R[g_s](hx)+O(h)
            =I(g_s)+O(h).
 \tag{19}
\]

All errors are uniform on the smooth pencil and in any fixed number of
parameter derivatives. Combining (16) and (19) proves

\[
 \sup_{A\in\mathcal P_h(g_s;R,M)}|I_h(g_s,A)-I(g_s)|\le C_Ah.
 \tag{20}
\]

Proper Lorentz node gauges conjugate each based plaquette at its base;
the transformed area and star pairing preserve the scalar action.
The limiting connection and curvature have their usual gauge transition
laws. Hence $I$ depends on $g$, not on its internal solder representative.
The fields and variations are periodic, so all boundary divergences cancel.

The full symmetric Gram variation of (19), with (8), is

\[
 DI(g)[V]=-\tfrac12\int\sqrt{|g|}G^{\mu\nu}[g]V_{\mu\nu}\,dy.
 \tag{21}
\]

Both indices of $G$ are raised by $g^{-1}$. This includes off-diagonal
variations with their correct packed dual weights. It is a global smooth
variational identity, not an extension of a normal-jet calculation by
an assumed naturality assertion.

For the parameter-smooth Borel comparator, finite chain rule gives
$D_gI_h[V]=h^2\sum_x\Xi_h(x):V(hx)$ plus a connection Euler term.
That term is $O(h^{M-1})$ for every $M$: logs and their metric derivatives
are $O(h)$, Euler residual is $O(h^M)$, and site count is $h^{-4}$.
Direct smooth face variation and (21), tested against arbitrary $V$, then
identify all ten leading components:

\[
 h^{-2}\Xi_h^{\rm sm}
 =-\tfrac12\sqrt{|g|}\operatorname{pack}(G^{\mu\nu})+O(h).
 \tag{22}
\]

The [existing $C^7$ theorem](A4D_CANONICAL_CONSTITUTIVE_GERM_SYNTHESIS.md)
calibrates regular exact instantaneous response to this same germ.
The rough-field result (20) requires no such regularity of the unknowns.

## 6. Quantitative finite readout and residual precision

Apply (20) to the independently chosen endpoints. Their action errors,
after division by $2\epsilon$, are at most $Ch/\epsilon$.
Taylor's integral formula on the fixed smooth metric pencil gives

\[
 \left|\frac{I(g_{+\epsilon})-I(g_{-\epsilon})}{2\epsilon}
                          -DI(g)[V]\right|
 \le\frac{\epsilon^2}{6}\sup_{|s|\le\epsilon}|\partial_s^3I(g_s)|.
\]

This proves (5). Individually $D_h^\pm$ have error
$O(h/\epsilon+\epsilon)$; averaging cancels the first-order continuum
truncation exactly. For general small-log endpoints, (16) retains the
more precise bound

\[
 |T_{h,\epsilon}-DI(g)[V]|
 \le C\left(\frac h\epsilon+
                 \frac{e_++e_-}{h\epsilon}+\epsilon^2\right).
 \tag{23}
\]

Thus $e_\pm=O(h^2)$ suffices for the $O(h^{2/3})$ rate. More generally
convergence holds whenever $\epsilon\to0$, $h/\epsilon\to0$ and
$(e_++e_-)/(h\epsilon)\to0$. Taking $\epsilon\to0$ at a fixed mesh is
not justified by (23). Differentiability of an arbitrary selected root
or of its critical-value branch is never inferred from action convergence.

## 7. Geometric completion and a proved native catalogue instance

Take $L_n=4\cdot2^n$, $h_n=1/L_n$ and $\epsilon_n=h_n^{1/3}$, omitting
the finitely many stages outside the preceding bounds. For geometric
nodes $X_n=(\mathbb Z/L_n\mathbb Z)^4$, the inclusion $j_n(x)=2x$ gives
$h_{n+1}j_n(x)=h_nx$. At a fixed pencil parameter $s$,

\[
 Q_{n+1}(s,j_n(x))=Q_n(s,x),\qquad Q_n(s,x)=g_s(h_nx).
\]

Keep the pencil as a family; its stage-dependent evaluations at
$\pm\epsilon_n$ are not one unchanged perturbed metric. These geometric
sampling maps are not identified with the archive coordinate-modulus or
flat-record maps. No inter-stage connection restriction is postulated.

A completion is any sequence of actual triples (3). Estimate (6) proves
for arbitrary, even adversarial independent choices

\[
 |T_m-T_n|\le C(h_m^{2/3}+h_n^{2/3}),
 \qquad \lim_nT_n=DI(g)[V].
 \tag{24}
\]

One concrete inverse system consists of measurement intervals
$E_n=[T_n-Ch_n^{2/3},T_n+Ch_n^{2/3}]$ and
$J_n=\bigcap_{j=n_0}^nE_j$. All $J_n$ contain $DI(g)[V]$; their bonding
maps are actual inclusions and $\operatorname{diam}J_n\le2Ch_n^{2/3}$.
Their intersection is exactly the singleton output. Rational outward
rounding with errors tending to zero yields the same limit from finite
precision records.

For the owned [CatalogueSystem](../../03_FORMALIZATION/D0/Foundation/M1ClassAdmissibility.lean)
interface, take `Candidate` to be the carrier of allowed central-state
sequences and `Catalogue` the carrier of endpoint-pair sequences.
Both are nonempty by (12); an arbitrary allowed exact central sequence
lifts without modification. Take `Output` to be the reals and define
`eval` as the limit of the **actual measurements** $T_n$, whose existence
is proved in (24). It is not defined by substituting an Einstein tensor.
Equation (24) proves its catalogue independence.

Identity representation retains distinct microscopic candidates.
The predicate `Forced(t)` means that **every** allowed completion's readings
converge to $t$, matching `CompletionForcesReadout` for the limit readout.
Nonemptiness and uniqueness of the measured limit give
`Forced(DI(g)[V])` and `Forced(t) -> t=DI(g)[V]`, discharging the actual
[M1Forced](../../03_FORMALIZATION/D0/Foundation/M1Predicate.lean) obligations.
The `hconst` premise of
[ObservableCompletionCanonicity](../../03_FORMALIZATION/D0/Foundation/ObservableCompletionCanonicity.lean)
is supplied by (24), not imported as a physical axiom.

This is a mathematical instantiation of existing interfaces. No claim is
made that the numerical gravitational operator or the present estimates
have been formalized in those generic Lean modules. Nor is every untyped
native D0 state asserted to have an independently owned metric realization.

## 8. Localizing the completed response

Fix a point $y_0$ and a coordinate ball of radius $\rho_*$. Predetermine
a nonnegative $\psi\in C_c^\infty(B_1)$ with integral one, and the ten
symmetric coordinate matrices $H_\alpha$: one unit diagonal entry, or two
symmetric unit entries for an off-diagonal slot. The latter pairs with the
packed covector's factor-two convention. Set

\[
 \rho_m=\rho_*2^{-m},\quad
 V_{\alpha,m}(y)=\psi((y-y_0)/\rho_m)H_\alpha,\quad w_m=\rho_m^4 .
\]

Extend these probes by zero outside the coordinate ball. The physical
metric perturbations have bounded amplitude; divide the scalar readings
by $w_m$ after measurement. If $r_\alpha(g,y)$ is the packed density in
(22), then

\[
 p_{\alpha,m}=\frac{DI(g)[V_{\alpha,m}]}{w_m}
   =\int_{B_1}\psi(z)r_\alpha(g,y_0+\rho_mz)\,dz,\qquad
 |p_{\alpha,m}-r_\alpha(g,y_0)|\le B_g\rho_m.
\]

For each fixed $m$, obtain finite $C_m\ge1,h_{0,m},\epsilon_{0,m}>0$
for all ten probes, including both one-sided and centered error bounds.
Endpoint constants $R_m,M_m$ include the explicit preparations and the
predeclared central bounds $R_0,M_0$; the same arbitrary UV center can be
retained for every component. These bounds depend on $g$ and the fixed
probes, not on the unknown states. Set

\[
 x_m=\min\{1,2^{-m}w_m/(4C_m)\},\qquad
 H_m=\min\{h_{0,m}/2,\rho_m/16,(\epsilon_{0,m}/2)^3,x_m^3\}.
\]

On the geometric dyadic meshes of Section 7, choose recursively
$n_m=\min\{n>n_{m-1}:h_n\le H_m\}$ and
$\epsilon_m=h_{n_m}^{1/3}$. The choices exist and are fixed before selecting
endpoint states. Compute $M_{\alpha,m}=T_{h_{n_m},\epsilon_m}/w_m$.
Because $h^{2/3}\le h^{1/3}$ for these meshes, (5) implies

\[
 |M_{\alpha,m}-r_\alpha(g,y_0)|
       \le 2^{-m}/2+B_g\rho_m.
 \tag{25}
\]

The one-sided localized records converge as well by
$C_m(h^{2/3}+h^{1/3})/w_m\le2^{-m}/2$. Thus all ten finite readings
converge to the pointwise canonical density and owned reconstruction gives
$-G[g](y_0)/2$. Constants are obtained separately for each shrinking bump;
no uniform $h^{2/3}$ rate under localization is asserted. This constructs
a local observable germ without claiming raw $\ell^1$ convergence of
instantaneous $\Xi$.

## 9. Retained UV fibers and the original exact-source boundary

The #232 curved nongauge vacuum and #227 response-visible stationary
family remain admissible central states at their log-$O(h)$ scales.
At $g=\eta$, (21) is zero for every periodic smooth probe; both have
zero **completed action-probe output**. The original sitewise #227
$\Xi$ remains nonzero in the retained finite record. These are therefore
the same action-probe measurement fiber and different raw-response
fibers. No curvature is declared gauge and no visible instantaneous
response is set to zero by definition.

The [full-Lorentz curved witness](A4D_GLOBAL_LORENTZ_FIXED_SOURCE_NOGO.md)
supplies an exact boundary control outside the endpoint domain (2): its
prescribed source is zero on every mesh, while its metric has nonzero Einstein response and
positive canonical action limit. The gauge-invariant involutive holonomy
prevents a log-O(h) representative. It is nevertheless included in the
unrestricted central slot (6a), with its actual zero Xi retained. An
unrestricted physical-state transfer preserving instantaneous response is
therefore false, while the centered completed factor is proved on that
full central domain. The endpoint preparation bounds are unchanged.

This theorem proves a complete path

\[
 \text{literal finite action and full Euler rows}
 \ \longrightarrow\ \text{constructible preparations and }O(h)
                    \text{ action stability}
 \ \longrightarrow\ \text{finite probes}
 \ \longrightarrow\ \text{unique Einstein observable germ}.
\]

It does **not** prove the original assertion
$h^{-2}\|\Xi(K)-\Xi(K^{\rm sm})\|_{\mathrm{owner},1}\to0$
for exact joint roots with one independently predeclared fixed source.
Approximate endpoint nonemptiness is not exact joint/source nonemptiness;
the fixed cosine-source incompatibility remains valid. The measured
factor is coarser than raw instantaneous response. Consequently neither
parent terminal, task retirement, nor public/formal claim promotion follows.

## 10. Input owners and validation boundary

* [Canonical constitutive germ](A4D_CANONICAL_CONSTITUTIVE_GERM_SYNTHESIS.md),
  §§1--3: physical chart, zero-phase recurrence, regular stationary theorem.
* [#216 smooth realization](MEMO_A4D_J2_SMOOTH_RESONANCE_CLOSURE.md),
  §§3,7: all-solder coefficientwise inverse and smooth asymptotic comparator.
* [Literal action and finite memory](A4D_FINITE_CURRENT_CORRELATION_MEMORY.md),
  §3: unchanged action, bounded shared-link stencil.
* [Warped designated rescue](A4D_WARPED_DESIGNATED_NORMAL_RESCUE.md),
  §6: owned action-density normalization and sign control.
* [Fixed-source arithmetic compatibility](A4D_FIXED_SOURCE_ALGEBRAIC_COMPATIBILITY.md),
  §§1,3: packed metric convention, visible UV control, exact-source boundary.
* Foundation interfaces linked in §7: generic admissibility and canonicity,
  instantiated only after the quantitative physical readout proof.

The analytic estimates above are the proof. Existing exact finite input
certificates and repository guards check their owned inputs and integration;
they are not advertised as a finite certification of all smooth fields.

## 11. Exact preparations on an open curved metric family

The preparation theorem in Section 3 applies to general smooth metrics
with a controlled full-row residual. On an open family around the original
curved cosine warp, the endpoints can instead be exactly stationary.
This is a stronger existence statement on a smaller geometric domain.

Let
\[
 E_0=\operatorname{diag}(1,1,f,f),\quad
 f=1+(1-\cos(2\pi y_1))/50,\quad Q_0=E_0^T\eta E_0.
\]
Fix finitely many arbitrary smooth symmetric probes $V_j(y_1)$, with
all ten Gram components allowed. There are $r,h_0>0$, independent of the
mesh, such that every pencil
\[
 Q(s)=Q_0+\sum_j s_jV_j,\qquad |s|<r,
 \tag{26}
\]
has a real exact full-connection-stationary solution $K_h^*(s)$ for every
allowed $h<h_0$. Its logs lie in the invariant 24L-dimensional sector
(dependence on $x_1$, all four link directions and six generators), are
uniformly $O(h)$, and are analytic in the finite parameters $s$.
Every fixed parameter derivative is $O(h)$ on smaller parameter balls.
There is no frequency restriction within the invariant sector.

Here is the uniform implicit argument, including the forcing estimate
needed to stay in the shrinking log chart. Use
\[
 E(s)=E_0\sqrt{I+Q_0^{-1}(Q(s)-Q_0)}.
\]
The self-adjointness relative to $Q_0$ proves its exact Gram identity.
The convergent square-root series gives a common complex parameter
neighborhood and uniform smooth spatial seminorms there.

Write $F_h(s,A)$ for the full Euler rows restricted to invariant fields.
The [owned curved rescue](A4D_WARPED_DESIGNATED_NORMAL_RESCUE.md),
Sections 4--5, gives $F_h(0,A_0)=0$, $\|A_0\|_\infty=O(h)$ and
\[
 H_0=D_AF_h(0,A_0),\qquad \|H_0^{-1}\|_{p\to p}\le36,
 \quad1\le p\le\infty,                                      \tag{27}
\]
after increasing the mesh threshold. Indeed its inverse at the smooth
comparator is at most 18 and the exact rescue changes that derivative
super-algebraically. Uniform finite-face analytic estimates give
\[
 \|D_AF_h(s,A_0)-H_0\|_{p\to p}\le C|s|,
 \qquad \|F_h(s,A_0)\|_\infty\le Ch|s|.                    \tag{28}
\]
For the second estimate split the parameter increment as
\[
 [F_h(s,0)-F_h(0,0)]
 +[F_h(s,A_0)-F_h(s,0)-F_h(0,A_0)+F_h(0,0)].
\]
At identity links, opposite incident-face contributions cancel for
constant area weights. Their remaining differences, and their parameter
increments, are $O(h)$ by the fixed spatial $C^1$ bounds. The first
bracket is therefore $O(h|s|)$. The second is $O(|s|\|A_0\|_\infty)$
by a mixed analytic derivative bound. An $O(|s|)$ forcing without this
extra factor $h$ would not establish the theorem.

For $A=A_0+u$, let $N_h(s,u)$ be the quadratic remainder. Its Lipschitz
bound on a ball is $C(\|u\|_\infty+\|v\|_\infty)\|u-v\|_\infty$,
independent of mesh population. The equation is equivalent to
\[
 u=-H_0^{-1}\{F_h(s,A_0)
       +[D_AF_h(s,A_0)-H_0]u+N_h(s,u)\}.                 \tag{29}
\]
Choose $r$ so $36Cr<1/4$, then $h_0$ so the nonlinear Lipschitz factor
is below $1/4$ on a ball $\|u\|_\infty\le C_1hr$. Increasing $C_1$
makes the ball invariant. This proves uniform contraction. Translation
invariance of both the solution and background makes the complete Euler
covector invariant: solving these rows solves every full-carrier row,
including derivatives against noninvariant variations. No projected
Euler equation has replaced full stationarity.

The same contraction on a smaller complex polydisc is holomorphic;
uniform convergence and Cauchy estimates give the asserted parameter
derivatives. Real inputs give real fixed points. The coefficientwise
recurrence and the same inverse, applied to any finite truncation, yield
\[
 \partial_s^\alpha(A_h^*(s)-A_h^{[N]}(s))=O(h^{N+1})
 \tag{30}
\]
on still smaller parameter balls, for every fixed $\alpha,N$.
Thus the exact family realizes the entire canonical asymptotic germ.
In particular its exact envelope identity is
\[
 \partial_{s_j} I_h(Q(s),K_h^*(s))
 =h^2\sum_x\Xi_h(Q(s),K_h^*(s))_x:V_j(hx_1).          \tag{31}
\]
The connection derivative term vanishes exactly. The leading limit is
the same Einstein pairing (21), with the same packed Gram convention.

Consequently all endpoint sets for the exact-root version of (4) are
nonempty throughout (26). Estimate (5) remains uniform over every exact
endpoint root in the declared log bound, including noninvariant rough
roots; only the existence witness uses the invariant construction.
No competing root is required to lie on $K_h^*(s)$ or continue through
the pencil. These exact probes test all ten components against functions
of $y_1$; they do not give exact endpoint existence for arbitrary
four-dimensional localized probes. Section 8 continues to use the
general residual-controlled preparations for that purpose.

This theorem solves the connection equation at the endpoints. Its
finite metric source is an output. It does not solve the incompatible
joint equation with the exactly sampled continuum Einstein source.

### 11.1 A fixed-width exact experiment with a nonzero output

The original curved warp admits a particularly concrete experiment which
does not require the probe width to tend to zero. Set
\[
 \psi=(1-\cos(2\pi y_1))/50=f-1,\quad f_t=f+t\psi,
 \qquad t\in[-1/2,1/2].
\]
Every $f_t$ lies in $[1,53/50]$. Section 5 of the owned curved rescue
extends its construction to any compact interval $0<a\le f\le b<\sqrt{5/2}$.
Here $b=53/50$ and the frozen scalar denominator has the uniform gap
$20-8b^2=6882/625>0$. Its finite kernel and first-moment bounds, followed
by the same parametrix and contraction, are uniform in $t$.
Thus both endpoint metrics have exact full stationary preparations for
every sufficiently fine allowed mesh.

The continuum action is exactly quadratic on this coframe path:
\[
 I(t)=\int_0^1(f_t')^2\,dy_1
     =\frac{\pi^2}{1250}(1+t)^2.
\]
Consequently, for arbitrary exact endpoint roots in a fixed log-$O(h)$
bound, including arbitrary four-dimensional UV patterns,
\[
 \boxed{
 T_h=I_h(f_{1/2},K_+)-I_h(f_{-1/2},K_-)
       =\frac{\pi^2}{625}+O(h).
 }                                                        \tag{32}
\]
The denominator $2\epsilon$ equals one. The two endpoint errors in
(20) give the stated bound uniformly; the continuum secant error is
exactly zero. Its nonzero limit is $I'(0)$, the Einstein pairing with
the tangent Gram variation of this declared path.

This path is affine in $f$ and nonlinear in the Gram metric. Quadratic
action along it does not imply a zero secant error for an arbitrary
affine Gram pencil. Equation (32) is a nonempty exact experiment with
fixed endpoints, rather than an assertion about the instantaneous
response of every central root. Its algebraic finite readings may
converge to $\pi^2/625$; the fixed-source arithmetic obstruction forbids
an exact source equality at a mesh, not this measured limit.

## 12. A finite exact quotient of all stationary action values

The exact experiment has a finite algebraic record before any completion.
For this statement, restrict Section 11 to trigonometric-polynomial probes
with algebraic coefficients and algebraic endpoint parameters. The fixed
endpoints of (32) satisfy this hypothesis. Sampled coframes in the
declared square-root section are real algebraic.

Fix a rational $M$ before choosing roots and use the polynomial chart
bound $\|U_\ell-I\|_F^2\le M^2h^2$ on every physical link. Together with
$U_\ell^T\eta U_\ell=\eta$ and all physical Euler equations, it defines
a bounded semialgebraic set $Z_h^\pm$. For small $h$ the matrix bound
implies the required log bound, and every family with a fixed log-$O(h)$
bound is included after increasing $M$. Fix $M$ large enough to contain
the exact existence witnesses. An inequality involving unevaluated
matrix logarithms would not provide this semialgebraic description.

On the Lorentz variety $U^{-1}=\eta U^T\eta$, so the literal action and
physical Euler rows are polynomials with algebraic coefficients. Define
\[
 \Sigma_h^\pm=\{h^2\mathscr A_h(Q^\pm,U):U\in Z_h^\pm\},\qquad
 S_h=\{(a-b)/(2\epsilon):a\in\Sigma_h^+,b\in\Sigma_h^-\}.
 \tag{33}
\]
Each set in (33) is **finite and nonempty**, and every element is real
algebraic. Indeed the [stationary-value arithmetic theorem](
A4D_FIXED_SOURCE_ALGEBRAIC_COMPATIBILITY.md) already proves algebraicity
of every full stationary action value, even at transcendental link
entries. Polynomial projection makes its image semialgebraic over the
real-algebraic field. A semialgebraic subset of the line is a finite
union of intervals and points; an image consisting only of algebraic
numbers has no interval. Alternatively, stationarity makes the action
constant along each of the finitely many piecewise smooth connected
components. Section 11 supplies nonemptiness.

Real quantifier elimination and algebraic root isolation compute an
ordered finite description of (33) from the input polynomials. The
projection/algorithm used here is the standard real-field theorem, for
example [Parrilo, MIT 6.972, Lecture 18, Theorems 2 and 4](
https://ocw.mit.edu/courses/6-972-algebraic-techniques-and-semidefinite-optimization-spring-2006/resources/lecture_18/).
This is a terminating construction theorem, not a reported enumeration
of the large D0 critical locus or a practical complexity bound.

For a requested $\kappa_k=\varphi^{-k}$ choose a dyadic $d_k$ with
$\kappa_k/8<d_k\le\kappa_k/4$. Using the proved error bound with a
certified constant, fix a sufficiently fine mesh so every $s\in S_{h_k}$
satisfies $|s-b|\le d_k/4$, where $b$ denotes the analytically proved
limit, not a value supplied to the algorithm. The choice uses the error
majorant and the existence threshold; it never compares with digits of
$b$. For (32) the error majorant is $Ch$; for affine probes it is
$Ch^{2/3}$. Constants and thresholds belong to the declared protocol.
No efficient numerical implementation of their bounds is claimed here.

Quantize by the fixed rule
\[
 z_k(s)=d_k\lfloor s/d_k\rfloor,\qquad
 B_k=z_k(S_{h_k}).
 \tag{34}
\]
Algebraic comparisons decide ties exactly. The image $B_k$ has at most
two adjacent rational values, since $\operatorname{diam}S_{h_k}\le d_k/2$.
Moreover
\[
 |z_k-b|\le5d_k/4\le5\kappa_k/16.                       \tag{35}
\]
A singleton is a trivial binary quotient; otherwise one binary letter
codes the ordered pair. No root, branch, or minimum-action solution is
selected. The quotient is for this scalar experiment only.

Define finite histories $X_k=\prod_{j=1}^k B_j$ with projections deleting
the last record. They are nonempty, their projections are surjective
and compose exactly. Every independent sequence of admitted endpoint
roots produces a history. The newest scalar obeys
$|z_{k+1}-z_k|\le5(\kappa_{k+1}+\kappa_k)/16$, rather than an exact
pullback identity. All histories have completed readout $b$ by (35).
This constructs the constant completion used in Section 7 directly
from finite algebraic value quotients.

The algorithm computes the possible value codes and rounds a given
algebraic value code. It is not an algorithm for extracting an exact
code from an arbitrary unknown transcendental link array. The physical
state-to-measurement interface is a separate obligation in Section 14.

## 13. Positive detector operators on the golden prefix tower

There is also an explicit operator realization of these finite records,
with exactly compatible operators, not merely compatible scalar limits.
This realization is a detector for the signed action contrast; it does
not replace that action by a positive square.

For a rational record $z$, set
\[
 D(z)=\operatorname{diag}(1,z+1,z-1,0),\quad
 R(z)=D(z)^\dagger D(z),\quad \operatorname{Tr}R(z)=2z^2+3>0.
 \tag{36}
\]
With coordinate effects $E_0,E_+,E_-,E_\emptyset$ and Born weights
$P_i=\operatorname{Tr}(E_iR)/\operatorname{Tr}R$, the exact decoder is
\[
 \frac{P_+-P_-}{4P_0}=z.                              \tag{37}
\]
The rational single-block frame instantiates the finite positive-response
arithmetic in [BornFiniteEffects](../../03_FORMALIZATION/D0/Core/BornFiniteEffects.lean).
The four channel names in (36) are detector coordinates; their cardinality
does not identify them with the physical four Role maps.

Let $p=\varphi^{-1}$, $p+p^2=1$, and use the actual BOOK_01 support
$S_n=\{A,B\}^n$ with cylinder probabilities $p,p^2$. On
$H_n=L^2(S_n,\mu_\varphi)$ the prefix pullback and its adjoint are
\[
 J_nf(wA)=J_nf(wB)=f(w),\qquad
 P_ng(w)=p\,g(wA)+p^2g(wB),\qquad P_nJ_n=I.
 \tag{38}
\]
Thus the native golden closure is exactly the isometry condition.
Its weight identities are owned by
[DetectorSupportGoldenWeight](../../03_FORMALIZATION/D0/CondensedAnchor/DetectorSupportGoldenWeight.lean).
In orthonormal coordinates put $u=(\sqrt p,p)$ and
$v=(p,-\sqrt p)$. They are orthonormal, $J_n=I\otimes u$,
$V_n=I\otimes v$, and $H_{n+1}=J_nH_n\oplus V_nH_n$.

At step $k=n-1\ge1$, let $E_n(z_k)$ be (36) on the first four address
modes of $H_n$ and zero on the remaining modes. Set $D_2=0$ and use the
fixed archive attenuation $\alpha_k=p^k$:
\[
 D_{n+1}(x)=J_nD_n(\operatorname{prefix}x)J_n^\dagger
       +\alpha_k V_nE_n(z_k)V_n^\dagger,\qquad R_n=D_n^2.
 \tag{39}
\]
Every finite detector matrix is self-adjoint. Orthogonality proves
\[
 P_nD_{n+1}=D_nP_n,\qquad
 R_{n+1}=J_nR_nJ_n^\dagger+
       \alpha_k^2V_nE_n(z_k)^2V_n^\dagger,\qquad
 P_nR_{n+1}P_n^\dagger=R_n.                           \tag{40}
\]
All historical channel projectors lift with $J_n$, preserving their
raw positive traces exactly. New normalization changes all old channel
probabilities by one common factor, which cancels in (37).
The factor $\alpha_k^2$ also cancels. There is one dimensionless unit
reference, not a new physical calibration at each stage.

Square roots in the orthonormal presentation are optional. In the
weighted value basis define $W_nf(wA)=p f(w)$ and
$W_nf(wB)=-f(w)$. Then $J_n^\dagger W_n=0$ and
$W_n^\dagger W_n=pI$. Replace the second term of (39) by
$\alpha_kp^{-1}W_nE_n(z_k)W_n^\dagger$. Its entries belong to
$\mathbb Q(\varphi)$; all finite weights have algebraic codes. The full
weighted matrix is not literally the rational-only Lean frame above;
its conditional distribution within a record block is that rational
frame. Equations (38)--(40) supply the additional linear algebra.

For a fixed experiment, (35) bounds all recorded $|z_k|\le Z$ uniformly.
Embed the finite Hilbert spaces using $J_n$ and let $\widehat D_{k+2}$
act by zero on later detail spaces. Distinct updates are orthogonal
blocks. Hence a self-adjoint compact operator $D_\infty(x)$ exists and
\[
 \|D_\infty-\widehat D_{k+2}\|
       \le(1+Z)p^{k+1},\qquad
 \operatorname{Tr}(D_\infty^2)
       \le(2Z^2+3)\frac{p^2}{1-p^2}<\infty.            \tag{41}
\]
The trace of the omitted response is at most
$(2Z^2+3)p^{2(k+1)}/(1-p^2)$. This is a genuine norm-convergent
operator construction and a positive trace-class response. Attenuation
is a fixed detector representation choice; it changes neither the
decoded record nor the gravitational action. Without attenuation
compatibility still holds and the bounded operators converge strongly,
but the infinitely many unit reference channels give infinite trace.

Different finite histories generally give different $D_\infty$.
Only their completed newest-record readout is forced to be the same
$b$; no microscopic or operator uniqueness is inferred from (35).
The decoder divides by the selected block's positive reference weight,
so no uniform probability-precision bound independent of depth follows
from norm convergence. Each finite encoded channel and its precision
remain part of the declared experiment.

### 13.1 Exact binary support-to-record realization and separation

The support-to-record arrow is explicit; it need not remain a missing
coding premise. For each finite nonempty ordered set $B_i$ of (34), put
$f_i(A)=\min B_i$ and $f_i(B)=\max B_i$. When $B_i$ is a singleton,
both letters have its one value. For the actual golden support
$S_{k+2}=\{A,B\}^{k+2}$ define
\[
 \widehat\rho_k(w)
   =(f_1(w_3),\ldots,f_k(w_{k+2}))\in X_k.             \tag{41a}
\]
The two initial letters match $D_2=0$. Each coordinate map is
surjective, so $\widehat\rho_k$ is surjective, and
\[
 \widehat\rho_k\circ\operatorname{prefix}
  =\operatorname{prefix}\circ\widehat\rho_{k+1}.        \tag{41b}
\]
Every infinite native binary word therefore gives an actual admitted
finite-record history. Equation (35), rather than an assumed constant
output, makes every such history's newest-record limit equal to $b$.
Pulling the detector family back along (41a) preserves (40) for
state words with the same prefix. Matrix addresses in $H_n$ and the
state word selecting a history are independent variables; they are
not identified by this pullback.

The positive detector also preserves the signed record injectively.
For its one-record block,
\[
 \|R(z)-R(w)\|_{\rm op}
 =|z-w|(|z+w|+2)\ge2|z-w|.                            \tag{41c}
\]
This follows directly from the two nonzero diagonal differences
$(z-w)(z+w+2)$ and $(z-w)(z+w-2)$.
Two different histories differing in record $j$ have
$\|R_\infty(x)-R_\infty(y)\|_{\rm op}
 \ge2p^{2j}|z_j-w_j|$ on that retained detail block.
The factor decays with depth. Thus the map is injective on retained
finite histories and has no depth-independent inverse bound.
The unique completed Einstein readout does not identify their
distinct finite records or detector operators.

The [arrow checker](certificates/a4d_native_record_arrow_check.py)
replays the shifted surjection, both prefix identities, generic
decoder and response difference, six exact golden tail identities
and 192 pulled-back finite operator identities.
Its JSON ledger is immutable by default.

## 14. What the native construction closes, and its remaining map

Sections 11--13 now provide exact endpoint nonemptiness on an open curved
family, finite algebraic readout quotients, terminal rational records,
positive operators, and exact prefix compression. The fixed-width
example (32) gives a nonzero Einstein output, with no branch selector
and with all rough exact endpoint roots retained. The quantitative
limit, rather than an assumed uniqueness axiom, supplies M1 canonicity.

The linear family (40) is an explicit proof of compatibility. The owner
[OperatorNaturality](../../03_FORMALIZATION/D0/Condensed/OperatorNaturality.lean)
has a set-endomorphism type; it is not advertised as a preexisting Lean
formalization of these weighted Hilbert operators.

This is a finite **record** tower on the native weighted support, with
the actual compatible surjection (41a). Section 16 below now supplies
the additional concrete realization on existing flattened archive stages.
The weighted support and archive records have not been identified with
the independently fixed physical Role-field state space and sector gate.
That physical transfer
must provide maps
\[
 \rho_k:X_k^{\rm native}\longrightarrow X_k,\qquad
 \rho_k\circ p^{\rm native}_{k+1,k}
       =\operatorname{prefix}\circ\rho_{k+1},          \tag{42}
\]
or a separately proved controlled version, together with the
action/readout and calibration identities. Full $E_K=0$ at our
endpoints is not by itself an identification with another native gate.
The retained/detail split of (39) is likewise an explicit readout
split, not an already proved physical archive identification.
BOOK_00 Section 00.4 and the comment preceding the finite-factorization
owner specifically retain these obligations. Coding alone cannot
discharge them.

The exact centered variation in
[ArchiveVariation](../../03_FORMALIZATION/D0/Geometry/ArchiveVariation.lean)
shows that finite secants are native variational objects. It concerns
the seam Hilbert--Schmidt action, however; (36) does not prove that this
positive seam action equals the signed A4D action. Such an identity
requires an action-preserving map, not a change of terminology.

The record version of (42) is supplied by Section 16. Its physical-field
interpretation and an identification with instantaneous raw $\Xi$
have not been supplied by the positive detector theorem. The
original fixed-source/raw-owner terminal remains open, and the exact
cosine-source infeasibility result is unchanged.

## 15. Constructive fixed-source closure in the completed variational criterion

This section explicitly revises the closure criterion. It proves a
nonvacuous fixed-source theorem for completed metric probes, rather than
claiming either original exact-source/raw-owner terminal.

Fix one smooth $g$ with the owned smooth oriented Lorentz solder and
one smooth packed Gram dual density $\sigma$, both before any links.
The density has exactly the ten-slot convention of (22).
The scalar functional corresponding to the original prescribed source is
\[
 J_h(g_s,A)=h^2\mathscr A_h(g_s,A)
       -h^4\sum_x \sigma(hx):g_s(hx).                  \tag{43}
\]
This records the already declared external source: its local metric
Euler equation is exactly
$h^2\Xi_x-h^4\sigma(hx)=0$, or $\Xi_x=h^2\sigma(hx)$.
No new gravitational density or connection-selection principle is
introduced.

For each fixed smooth metric probe $V$, use the independent endpoint
preparations of (2), predeclare $\epsilon=h^{1/3}$, and read the
centered contrast of (43):
\[
 W_h(V)
  =T_{h,h^{1/3}}(V)-h^4\sum_x\sigma(hx):V(hx).          \tag{44}
\]
The completed source law means
\[
 \lim_{h\to0}W_h(V)=0
       \quad\hbox{for every smooth symmetric probe }V. \tag{45}
\]
Equation (45) is a completed variational equation. It does not demand
that any endpoint solve the finite metric equation of (43).
Connection preparations retain all 24 finite Euler rows with the
explicit residual bound (2). In Section 11's one-coordinate curved
class, exact full connection-stationary endpoints can be used.

**Theorem.** The completed source law has constructive finite
preparations on every sufficiently fine mesh, and it holds uniformly
over every allowed endpoint choice if and only if
\[
 \boxed{\sigma=\rho_0[g]
   =-\tfrac12\sqrt{|g|}\operatorname{pack}(G^{\mu\nu}[g]).} \tag{46}
\]
The metric, source and probe are fixed across the mesh sequence.
The source in (46) is specified from $g$ before preparing links.
No mesh-dependent source output is substituted for it.

**Proof.** The explicit rule $B_h=h\omega_{\rm LC}[g_s]$
inhabits every preparation set by (13). For every arbitrary
rough endpoint pair within the predeclared bounds, (5) and the smooth
Riemann-sum estimate give
\[
 W_h(V)=\int_{\mathbb T^4}(\rho_0[g]-\sigma):V\,dy
                         +O_V(h^{2/3}).               \tag{47}
\]
The estimate is uniform in the unknown endpoint choices. If (46)
holds, it proves (45) with an explicit vanishing majorant. Conversely,
(45) and (47) imply that the smooth density $\rho_0[g]-\sigma$
annihilates every smooth component and bump probe. The fundamental
lemma, with the existing off-diagonal packing, forces (46).
Thus both existence and the source characterization are proved.

Each fixed finite collection of probes has its own predeclared
finite bounds $R,M$ and constants. No bounded constants over the
unbounded set of all smooth probes are assumed. The same explicit
LC preparation rule supplies all experiments. A single sequential
realization can use a countable dense list of smooth probes: at stage
$n$ retain its first $n$ probes and choose a mesh below all their
finitely many thresholds, with every error at most $\delta_0^n/4$.
These stages exist independently of endpoint choices. Each fixed
probe then has the owned golden Cauchy completion. Continuity of
the limiting smooth-density pairing extends the countable tests to
all smooth probes.

Finite source-record errors can be included in the same precision
majorant. Source readings need not be algebraic: rational outward
recording at predeclared accuracy suffices, as in the general
GoldenTower construction. The exact finite algebraic quotients of
Sections 11--13 concern the separate gravitational endpoint actions.

This theorem closes the **completed metric-probe source law** with
one fixed smooth source on a genuinely inhabited class. It retains
arbitrary central physical states and rough endpoint preparations;
its general endpoint assumption is the declared residual bound,
not exact joint criticality. The original condition
$\Xi=h^2\sigma$ at every mesh and its unweighted raw owner comparison
remain distinct and OPEN. The physical Role/action-gate realization
of Section 14 is likewise not supplied by (46).

## 16. Concrete archive record and positive-operator realization

The [native archive bridge](A4D_NATIVE_ARCHIVE_RECORD_BRIDGE.md) now
constructs the record version of (42) on the existing
`ArchivePoints n=Fin((n+2)^4)` tower, using its actual successive modulo
maps. It does not flatten the distinct coordinatewise Role projection.
For selected levels `n_0=2`, `n_(k+1)=(n_k+2)^2+2`, let `pi_k` be the
actual composite native projection and `c_k=(n_(k+1)+1)^4`.
Every old native point y has two explicit children `y` and `y+c_k`.
Their first projection is y and all remaining intermediate maps fix y.

The bit `chi_k(x)=A` for `x<c_k`, B otherwise gives
`beta_(k+1)(x)=(beta_k(pi_k x),chi_k(x))`. These compatible quotients
are surjective, with a compatible section built from the two children.
Compose beta with (41a), on the stated two-initial-letter shifted indices,
to obtain actual native archive maps onto the admitted record histories.
The newest-record limit is the already proved scalar b on every address.

There is also a full-support projective golden measure. Let `N_(k,y,b)`
count the actual native children of y with bit b; both counts are positive.
The transition probability `p_b/N_(k,y,b)` gives each bit its mass
`p_A=p`, `p_B=p^2`, for every old y. Starting from uniform positive base
mass constructs compatible full-support measures mu_k with
`(beta_k)_*mu_k=mu_phi`. This is a specified construction; it is not an
identity with a previously fixed native physical measure.

The pullback `T_k f=f composed with beta_k` is an isometry from golden
prefix Hilbert space to actual measured native archive Hilbert space.
Native pullback/conditional expectation `J^A,P^A` and golden `J^B,P^B`
satisfy
\[
 J_k^A T_k=T_{k+1}J_k^B,\qquad
 P_k^A T_{k+1}=T_kP_k^B,\qquad
 T_k^\dagger P_k^A=P_k^B T_{k+1}^\dagger.
 \tag{48}
\]
The first identity is pointwise compatibility. The second follows because
the new bit has the same conditional golden mass at every old point;
the third is the adjoint of the first. Thus the transported operators
`Dtilde_k=T_k D_k T_k^dagger`, `Rtilde_k=T_k R_k T_k^dagger` obey
\[
 P_k^A\widetilde D_{k+1}=\widetilde D_kP_k^A,\qquad
 P_k^A\widetilde R_{k+1}(P_k^A)^\dagger=\widetilde R_k.
 \tag{49}
\]
Positivity, trace-class tails, signed-record decoding and record separation
are preserved. Operators vanish on the orthogonal complement of the
isometry image; that complement is not identified with a physical sector.
The [immutable native checker](certificates/a4d_native_archive_binary_bridge_check.py)
replays all first selected archive points, the golden transition kernels,
conditional expectations, sections and actual modulo projections.

This closes the archive record/operator construction. The independently
specified physical Role-field gate, action and calibration still need one
typed realization. The [actual seam-action audit](A4D_NATIVE_SEAM_ACTION_GATE_BOUNDARY.md)
already excludes the direct fixed-fine action-preserving stationary map:
its coarse action is strictly convex, whereas literal Palatini paths
through the flat stationary base have both signs. Varying fine fields or
independent doubled sectors is outside that restricted obstruction.

## 17. The actual forward response in conformal directions

The [conformal forward-source bridge](A4D_CONFORMAL_FORWARD_SOURCE_BRIDGE.md)
now identifies a part of the retained root's original Xi, rather than
only its independently re-prepared action readings. Let every full
connection Euler row of A_h vanish, with `||A_h||_infinity<=r_h`, `r_h>=h`
and `r_h^3/h^2 -> 0`. There is no unknown-field derivative or phase bound.
For every fixed smooth scalar psi,
\[
 \left|h^2\sum_x\Xi_x:(\psi g)(hx)
       -\int\rho_0[g]:(\psi g)\right|
 \le C_\psi\frac{r_h^2}{h^{4/3}}\longrightarrow0.
 \tag{50}
\]
In particular the error is O(h^(2/3)) for r_h=Rh.

The proof constructs a continuation through the retained central root:
`A_h(s)=A_h-h omega_LC[g]+h omega_LC[(1+s psi)g]`.
Conformal face weights multiply by the same scalar at each face base.
The full weighted Hessian therefore differs from local scalar times the
old Hessian by an operator of sup norm O(h). This supplies approximate
stationary endpoints, with residual O(r_h^2+h r_h+h^2), without an inverse.
The full action secant identity gives action error O(r_h^3/h^2).
Because those face weights are exactly linear in s, the dangerous pure
rough-field terms have zero third parameter derivative. A uniform third
derivative bound and `epsilon=(r_h^3/h^2)^(1/3)` prove (50).
At the central root the connection chain-rule term vanishes exactly, so
this secant estimates its actual forward Gram derivative.

If that root sequence also satisfies the original exact equation with
one independently fixed smooth source, `Xi_x=h^2 tau(hx)`, then
\[
 \boxed{g:(\tau-\rho_0[g])=0\quad\hbox{pointwise}.}       \tag{51}
\]
Thus an exact vacuum in this amplitude class requires scalar-flat g.
The theorem leaves traceless source components and fixed nonshrinking
small amplitudes open. The exact Weyl-spin hostile control in the linked
owner shows why the ordinary right/left/symmetric correction is insufficient
for fixed-amplitude #232 fields: one full Euler row retains the first term
`epsilon*t/4`. This does not exclude a UV-dependent correction.
Neither (50) nor the native archive construction proves the original raw
owner terminal, and the parent remains Draft / IN_PROGRESS.
