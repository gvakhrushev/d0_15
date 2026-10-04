# A4D finite action probes: a constructive Einstein observable completion

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input head: `aed0db1782184e8318cf9b150e5134be6800b177`.
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
