# Shrinking-native-leg flat H+J+R source: all stationary preparations and a conditional family obstruction

20 October 2026. Original-scientific-owner research continuation in existing Draft #334, \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`, with **unchanged** inputs:

1. Original full CAR16 + global-normalizer + 128-feedback + fixedRIGHT Riesz \`H+J+R\` from \`A4D_EXACT_CURVED_WHOLE_HJR_FIXED_COLLAR_ROOT_2026_10_20.md\`, and already proved exact rational Fourier flat-source owners \`sources/d0_hjr_flat_density_zero_2026-10-20/REFINING_UNIFORM_SOURCE.md\` and \`check_common_einstein_coframe_scale.py\`;
2. Main positive nonvacuum same-metric Einstein family \`D0_GR_PRIMARY_POSITIVE_CASE.md\`, \`A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md\` and the unchanged 16+24+2 configured Golden-J2 theorem;
3. complete fixedRIGHT preparation tangent theorem \`A4D_EXACT_CURVED_NATIVE_DIRAC_FIXED_RIGHT_PREPARATION_AND_SOURCE_2026_10_20.md\` §3.

**Scope after the 23 October normalization correction below:** prove the flat-source obstruction for **EVERY genuinely preparation-stationary fullRIGHT128 state** on the explicit shrinking-native-leg chart, not merely one 128-mode Riesz shell. The continuity argument excludes a punctured stationary family only when an actual same-action map is proved to land in this chart at its flat endpoint. Its former unconditional application to the fixed-physical-metric primary Einstein family is withdrawn. The no-go targets the **specified conditional bare H+J+R**, not the as-yet-unidentified compulsory complete Book03 Cost−Info/oldRIGHT/controller/work/clock price. It is not a new GR action, a selector or a global D0⇒GR no-go.

## 1. Explicit shrinking-native-leg carrier and the FULL thermal + feedback object

Fix integer \(L\ge256\), \(h=L^{-1}\), every one of the original \(L^4\) sites and all 16 CAR grades. Use the original observer's positive scalar product and the following **shrinking native creation-leg** chart
\[
v_r(\rho)=h\sqrt\rho\,e_r,\qquad U_r=I,\qquad \rho>0.
\]
At \(\rho=1\) this is a nondegenerate flat native chart at each fixed h, but its reconstructed physical metric is \(h^{-2}\eta\), not the fixed flat limit of the primary family. A separately identified flat Palatini action has \(DS_\star=0\) because its plaquettes are identity; this does not identify the two coframe variables. The coframe chart is nondegenerate and uses the genuine shifted positive-adjoint exterior Dirac and all fields, not a bare spectral surrogate.

Exact CAR cancellation on the entire original site×CAR Hilbert space gives
\[
\Delta_\rho=\rho\,\Delta_1,\quad
\operatorname{spec}\Delta_1=\{\mu(q)=\sum_{r=0}^{3}[2-2\cos(2\pi q_r/L)]\}_{q\in(\mathbb Z/L)^4}^{\times16}.
\tag{1}
\]
The original, entirely unchanged conditional \(H+J+R\) is
\[
S_L(\rho,M)=
\frac{\log(C_L\,16\sum_q b_q(\rho)^m)}\beta
-2048\sum_q\log(1-z+zb_q(\rho)^m)
+\operatorname{Tr}(M^\dagger\Delta_\rho M),
\tag{2}
\]
where
\[
p=\varphi^{-1},\quad\alpha=\frac{p^2}{128L^2},\quad
m=256L^2,\quad\beta=m\alpha=2p^2,\quad
z=2^{-20},\quad b_q(\rho)=1-\alpha\rho\mu(q).
\]
All \(16L^4\) thermal modes and all \(128\times16\) feedback modes occur with the proper multiplicities. The workspace factor \(C_L\) is field-independent in precisely this already-certified conditional owner; a moving **actual** complete workspace/cost must be added to the *physical* Book03 comparison, not silently suppressed or assumed field independent in another owner.

## 2. PREPARATION-INDEPENDENT flat no-go (new uniform theorem)

Take **any** genuinely admitted normalized fixedRIGHT rank128 preparation \(M\) on this same full Hilbert space, \(M^\dagger M=\Sigma_R\succeq0,\operatorname{Tr}\Sigma_R=1\), with its full original LEFT-unitary preparation Euler satisfied,
\[
[\Delta_\rho,MM^\dagger]=0
\]
(the fixed-Gram criterion, not merely a restricted orbital stationarity). The original \(H,J\) in (2) are independent of \(M\); along the *actual* coframe tangent \(\partial_\rho\), the envelope/stationary-preparation theorem therefore yields
\[
\partial_\rho R_L(\rho,M)
=\operatorname{Tr}(M^\dagger\Delta_1M)\ge0.
\tag{3}
\]
The same expression is valid when \(M(\rho)\) is any differentiable family of fixedRIGHT stationary preparations: the extra \(D_MM\) term drops because the preparation Euler already vanishes. Neither the particular Riesz first-positive shell, a zero-mode-filled preparation, the choice of 128 eigenvectors nor a possible negative preparation second variation can make (3) negative. If a different native **preparation/work** functional couples to \(M\), it is outside the conditional action (2) and must enter its **full** preparation Euler and source rather than being postulated absent.

Direct differentiation of the *entire* (2), with \(f_q=b_q^m\), gives:
\[
\partial_\rho(H_L+J_L)\big|_{\rho=1}
=-\frac{\sum_q\mu(q)f_q/b_q}{\sum_q f_q}
+2048z\beta\sum_q\frac{\mu(q)f_q/b_q}{1-z+zf_q}.
\tag{4}
\]
The earlier exact rational proof on this SAME bounded-spectrum native chart (source \`check_common_einstein_coframe_scale.py\`) supplies, for **every** integer \(L\ge256\):
\[
\begin{aligned}
0\le\mu(q)\le16,\quad \sum_q\mu(q)=8L^4,\quad b_q>79/80,\\
0<f_q\le1,\quad f_q>e^{-13}>1/500000,\quad
3/4<\beta<4/5 .
\end{aligned}
\tag{5}
\]
The first thermal term in (4) is bounded below by \(-1280/79\). The second feedback term, since \(b_q\le1\), \(1-z+zf_q\le1\), and \(2048z=1/512\), is bounded below by \((3/128000000)L^4\). Thus the **bare H+J tensor component is strictly positive BEFORE ANY choice of preparation**:
\[
L^{-4}\partial_\rho(H_L+J_L)
\ge \frac3{128000000}-\frac{1280}{79L^4}
\ge c_*:=\frac3{128000000}-\frac{1280}{79\cdot256^4}
>\frac1{100000000}>0.
\tag{6}
\]
Combining with (3):
\[
\boxed{
L^{-4}\partial_\rho S_L(\rho,M)\big|_{\rho=1}
\ge c_*>10^{-8}
\quad\text{FOR EVERY full fixedRIGHT preparation-stationary }M,\ L\ge256.
}\tag{7}
\]
This also excludes every genuine stationary preparation with additional occupancy of the flat Dirac zero modes. A stationary field equation in all 16 independent coframe rows would imply its contraction with this uniform coframe tangent is zero, contradicting (7). Therefore **this shrinking-native-leg flat chart is NOT a stationary solution of bare conditional full \(H+J+R\), independently of the occupied rank128 spectral shell.**

No new finite-matrix census or expensive original HJR replay is needed: the only new step beyond the previously exact Fourier/rational owner is the *stationary-preparation envelope*, taking advantage of positivity of the unchanged original Rayleigh \(R\). The existing fixed-Riesz calculation is one strict special case. A checker independently verifies the rational strict bound and the logical uniform-preparation inequality.



### 2.1. An even stronger **four-independent-leg** theorem: not merely one dilatation

Do not restrict the original 16 coframe Euler coordinates to the uniform radial direction. On the same flat original fullCAR16 carrier, vary the four genuine orthogonal positive-observer leg scales **independently**,
\[
v_r=h\sqrt{\rho_r}\,e_r,\quad r=0,1,2,3,\qquad U=I.
\]
The exact original CAR adjoint and anticommutators give
\[
\Delta_{\boldsymbol\rho}=\sum_{r=0}^{3}\rho_r\Delta_r,\quad
\Delta_r(q)=\omega_r(q)I_{16},\qquad \Delta_r\succeq0.
\]
At \(\rho_0=\cdots=\rho_3=1\), the COMPLETE original H and J trace is invariant under permutations of the four \(q_r\). Its four individual first derivatives are therefore equal to **one quarter** of the positive radial derivative in (6), even though the underlying internal Lorentz metric has a different signature:
\[
\left.\partial_{\rho_r}(H+J)\right|_{\boldsymbol\rho=1}
=\tfrac14\partial_\rho(H+J)\big|_{\rho=1}.
\]
Every preparation-stationary Rayleigh response remains nonnegative in each independent leg:
\(\partial_{\rho_r}R=\operatorname{Tr}(M^\dagger\Delta_rM)\ge0\).
Thus for **every** genuine preparation-stationary normalized \(M\),
\[
\boxed{
L^{-4}\partial_{\rho_r}S_L\big|_{\boldsymbol\rho=1}
\ge c_*/4>2.5\times10^{-9},
\qquad r=0,1,2,3,\ L\ge256.
}\tag{7a}
\]
The separately specified flat-link Palatini star has exactly **zero** coframe source; identifying its variables and tangents with this native chart still requires the actual carrier map. This proves a **four-row tensorial obstruction on a genuine independent coframe chart**, not a one-direction numerical mismatch. It is conditional on the same positive-observer orthogonal leg chart as (1); it is NOT a claim that the complete physically covariant stress tensor equals a Lorentz cosmological-constant term. In particular no identification of positive-observer isotropy with Minkowski \(\eta\)-isotropy is made.



### 2.2. No stationary flat point inside the **shrinking-native-leg four-dimensional box**

The same rational calculation in fact does **not require** \(\rho_r=1\), nor does it require the four flat legs to have equal lengths. At all original flat links \(U=I\), fix any four *independent* positive-observer scales
\[
0<\rho_0,\rho_1,\rho_2,\rho_3\le1,\qquad
v_r=h\sqrt{\rho_r}\,e_r.
\]
The exact whole-CAR16 spectrum is still
\[
\mu_{\boldsymbol\rho}(q)=\sum_{s=0}^{3}\rho_s\omega_s(q),
\quad0\le\mu_{\boldsymbol\rho}(q)\le16,
\quad b_q=1-\alpha\mu_{\boldsymbol\rho}(q).
\]
As \(0<\rho_s\le1\), the same **pointwise** rational inequalities \(b_q>79/80,\ f_q=b_q^{256L^2}>1/500000\) hold uniformly on this entire four-dimensional box. When differentiating in \(\rho_r\), the score \(\mu\) in (4) is replaced by \(\omega_r(q)\), satisfying
\[
0\le\omega_r(q)\le4,\qquad\sum_q\omega_r(q)=2L^4.
\]
Therefore the exact thermal/feedback derivative in **each** coframe direction obeys, without invoking permutation symmetry,
\[
\partial_{\rho_r}H
\ge-\frac{4}{79/80}=-\frac{320}{79},\qquad
\partial_{\rho_r}J
\ge 2048z\cdot\frac34\cdot
  \frac{2L^4}{500000}
=\frac{3L^4}{512000000}.
\]
With \(\partial_{\rho_r}R=\operatorname{Tr}(M^\dagger\Delta_rM)\ge0\) under true preparation stationarity:
\[
\boxed{
L^{-4}\partial_{\rho_r}S^{\rm bare\,HJR}_L(\boldsymbol\rho,M)
\ge \underbrace{\frac3{512000000}
-\frac{320}{79L^4}}_{\ge c_*/4> 2.5\cdot10^{-9}},
\quad r=0,1,2,3,\quad
L\ge256,\quad0<\rho_s\le1.
}\tag{7b}
\]
Thus the bare conditional full \(H+J+R\) has **no genuine stationary flat-link field configuration anywhere inside this whole nondegenerate box**, for ANY genuinely fixedRIGHT-stationary normalized preparation, rather than merely failing at one point of this shrinking chart. A separately specified constant-matter flat-link star/Golden-J2 geometry has zero coframe source; this fact alone does not identify its coframe with the native creation coefficients.

**23 October 2026 normalization correction (the bounds above are unchanged).**
The original Palatini edge/solder variable is \(w_{h,r}=hE_{\rm phys,r}\), whereas the native creation coefficient is an inverse physical coframe. The original [all40 sampling](../../../gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md), equation (1), and its [literal constructor](../d0_arbitrary_brinkmann_all40_2026-10-19/check_all40_arbitrary_brinkmann.py), function `e`, retain the factor h. The [native coframe owner](../../A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md), §2, uses \(v_r=\eta(E_{\rm phys}^{-T})_r\); the [full-Lorentz owner](../../A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md), (4), already has \(d_h=h^{-1}\sum_r C(v_r)(\Lambda(U_r)S_r-I)\).

In the kinematic [J2-to-native map](../../A4D_SAME_HISTORY_PRICE_AND_SOURCE_COMPOSITION_2026_10_20.md), §7, the physical coframe obeys
\[
 E_N=\nu^{-1}S E_{J2},\qquad
 v_N=\nu S\eta E_{J2}^{-T},\qquad
 S=\operatorname{diag}(1,1,-1,-1).
\]
Its [coframe check](../d0_same_history_price_composition_2026-10-20/check_connection_coframe_review.py), lines 26–35, has no h in this physical coframe. Thus a fixed physical flat E_J2 and fixed \(\nu=3/5\) give native legs of length nu, not h nu. In the box coordinates this is
\[
 \rho_r=\nu^2/h^2,\qquad
 \Delta_N=\nu^2h^{-2}\sum_r\omega_r I_{16}.
\]
It leaves \(0<\rho_r\le1\) on fine meshes, so (7b) does not apply to it. By contrast the scalar box itself reconstructs
\[
 g_{h,\rho}=h^{-2}\rho^{-1}\eta,
\]
or its diagonal four-scale version, at fixed rho. The earlier substitution \(\rho_r=\nu^2\) omitted h and is withdrawn. No bound, same-primary no-go, or fugacity schedule for a fixed physical metric follows by that substitution. The distinct fixed-v theorem in [REFINING_UNIFORM_SOURCE.md](REFINING_UNIFORM_SOURCE.md), with its \(L^2\) spectrum, is unchanged.

This correction preserves the full trace, original clock/calibrations, stationary-preparation envelope and all arithmetic on the box. It repairs their application map; it supplies neither a new physical restriction nor a fitted price term.



### 2.3. NEW operator-level extension to PERIODIC OR OPEN rectangular shifts: no reliance on Fourier diagonalization or a torus

To separate the bounded-spectrum statement from a periodic Fourier assumption, here is a second exact result **directly on a full finite product box**, with each of its four original coordinate shifts chosen independently as either a length-L periodic unitary or the standard length-L one-sided open/Dirichlet truncated shift. We keep every interior/boundary site and all original CAR16 grades; a fixed Dirichlet coframe collar makes the admissibility of a **global** coframe variation an additional physical boundary condition (see below).

Let \(\mathcal H_{\rm site}=(\mathbb C^L)^{\otimes4}\), \(N=L^4\). On the same positive observer CAR16 space, write
\[
\delta_r=S_r-I,\quad d=\sum_r\sqrt{\rho_r}\,C_r\delta_r,\quad
D=d+d^\dagger,\quad
\Delta=D^2.
\]
The genuinely shifted adjoint of an open unilateral shift satisfies \(S_r^\dagger\ne S_r^{-1}\); this proof retains it EXACTLY. For different coordinate directions all \(\delta_r,\delta_s^\dagger\) commute; the genuine CAR relations give the **exact positive operator decomposition**
\[
\boxed{
\Delta_{\boldsymbol\rho}=\sum_r\rho_r\Delta_r,\quad
\Delta_r=C_r I_r\,\delta_r\delta_r^\dagger+
I_r C_r\,\delta_r^\dagger\delta_r
\succeq0,\qquad
\|\Delta_r\|\le4,\quad \|\Delta\|\le16.
}\tag{B1}
\]
The two CAR occupancy projectors have exact trace 8 each. Since every original shift has zero diagonal when \(L\ge2\),
\[
\operatorname{Tr}_{\rm site}(\delta_r^\dagger\delta_r)
=N+\operatorname{rank}(S_r)
=\begin{cases}
2N,&S_r\text{ periodic},\\
(2-L^{-1})N,&S_r\text{ unilateral open},
\end{cases}
\]
and so the entire original site×CAR trace is
\[
\boxed{
\operatorname{Tr}\Delta_r
=16\,\operatorname{Tr}_{\rm site}(\delta_r^\dagger\delta_r)
\ge16(2-L^{-1})N.
}\tag{B2}
\]
No normality of the open shift, independent diagonalization by a discrete Fourier transform, or boundaryless exterior calculus is assumed.

Use the **unchanged same algebraic conditional original HJR trace action** (2) on this actual full finite Hilbert space, with \(B=I-\alpha\Delta,\ F=1-z+zB^m\), global \(Z=\operatorname{Tr}B^m\), feedback \(-128\operatorname{Tr}\log F\), and any genuine fixedRIGHT normalized preparation. If \(0<\rho_r\le1\), every eigenvalue \(\mu\) of \(\Delta\) obeys \(0\le\mu\le16\); hence \(B>79/80\) and \(B^{m-1}>1/500000\) by the exact same mα/Golden rational inequality.

The operators \(\Delta_r\) commute with \(\Delta\) in this separable product construction; equivalently the following trace estimates can be obtained from positive spectral functional calculus. For every independent coframe variation, at fixed internal state,
\[
\begin{aligned}
\partial_{\rho_r}H
&=-\frac{\operatorname{Tr}(\Delta_rB^{m-1})}
 {\operatorname{Tr}B^m}
\ge-\frac{4}{79/80}=-\frac{320}{79},\\
\partial_{\rho_r}J
&=128\beta z\,\operatorname{Tr}
\left(\frac{\Delta_rB^{m-1}}{1-z+zB^m}\right)\\
&\ge \frac{128\cdot(3/4)z}{500000}
\operatorname{Tr}\Delta_r
\ge \frac3{512000000}\left(1-\frac1{2L}\right)N.
\end{aligned}
\tag{B3}
\]
The original Rayleigh derivative is \(\operatorname{Tr}M^\dagger\Delta_rM\ge0\), with either bare stationary-preparation envelope or the actual **full**-internals envelope when testing an additive physically complete price. Thus on EVERY one of these exact original periodic/open finite shift boxes, for any positive coframe scales \(0<\rho_s\le1\) and any genuinely bare-R preparation-stationary fixedRIGHT128 state,
\[
\boxed{
L^{-4}\partial_{\rho_r}S^{\rm bare\,HJR}
\ge
\underbrace{\frac3{512000000}\left(1-\frac1{2L}\right)
-\frac{320}{79L^4}}_{c_{r,L}}
\ge c_{\rm open}:=
\frac{406303}{4\cdot20709376000000}
>4.9\times10^{-9},\quad L\ge256.
}\tag{B4}
\]
The **source is strictly nonzero in all FOUR original coframe legs even without any periodic Fourier normality**, and the all-role radial sum exceeds \(4c_{\rm open}>1.96\times10^{-8}\) per site. The original Palatini star remains identically zero at \(U=I\) on any such site/face carrier.

This kills the simple boundary-change escape **for the unchanged full-trace HJR functional**: periodic vs standard open/Dirichlet shift choice alone does not restore a stationary flat point in this shrinking-native-leg box, and rank128 occupancy cannot do so either. It remains important NOT to overclaim the full original Brinkmann collar physical boundary problem: when boundary coframe values are externally fixed, a variation of **all** boundary and interior coframes together need not be an admissible Euler tangent. To turn (B4) into an exact interior-only no-go on that specific fixed collar one must redo the \(\partial_\rho\) test for an *admissible interior-supported* variation, including moving boundary/work/traction terms. That further tangent-specific bridge is NOT provided by (B4). Conversely, the conditional full-HJR result itself cannot invoke a torus-only Fourier restriction to excuse the bulk pressure on a physically admitted open global coframe chart.

This operator extension is novel relative to the prior periodic-rank Fourier certificate: it uses the literal shifted TRUE positive adjoint, a fullCAR16 occupancy trace and a positive-operator spectral bound to cover the physically relevant open-shift type **without re-solving the continuum Einstein equation**.

## 3. Conditional family theorem: no continuous stationary lift landing in this box

The already accepted same-metric positive configured Golden-J2 theorem supplies a genuine **one-parameter subfamily of its infinite-dimensional exact NONVACUUM solutions**. For any sufficiently small fixed smooth \(\Psi_0\not\equiv\text{constant}\) and harmonic wave \(W_0(u,x,y)\not\equiv0\), let, for real small \(t\),
\[
\Psi_t=t\Psi_0,\qquad
H_t(u,x,y)=-\lambda t^2\|\Psi'_0(u)\|^2(x^2+y^2)+tW_0(u,x,y).
\tag{8}
\]
For every sufficiently small \(t\ne0\) the original configured J2 action has exact nonvacuum Einstein/positive Weyl 16+24+2 interior stationary representatives **on each admissible mesh** under its actual midpoint time labels and true scalar/top increment records. Their geometric coframes and null holonomies depend smoothly on \(t\) and converge to the flat Einstein fields as \(t\to0\).

**Conditional no-lift theorem, fixed \(L\ge256\).** Suppose an actual admitted same-action transport maps the displayed punctured Einstein family (or any punctured family) to bare-HJR stationary fields for every sufficiently small nonzero t. Require explicitly that its continuous flat image is
\[
 v_{L,r}(0)=h\sqrt{\rho_{*,r}}e_r,\quad
 0<\rho_{*,r}\le1,\quad U_r(0)=I,
\]
that the global coframe scale variations used in (7b) are admitted, and that its genuine fixedRIGHT stationary preparations M_L(t) converge to a normalized stationary M_L(0). Require the full HJR source to be continuous under this actual field/state map, with no missing field-dependent work or moving-clock source. Then this transport does not exist. The fixed-physical-metric map above does NOT satisfy the asserted box landing on fine meshes; its application requires a separate source analysis.

Proof: the complete coframe Euler vanishes for every \(t\ne0\). Its contraction with the admissible uniform scalar coframe direction must therefore vanish. Continuity gives vanishing at \(t=0\), contradicting (7b). This excludes an entire punctured stationary family only under the explicit landing and tangent hypotheses. It is not an unconditional no-go for the primary fixed-physical-metric Einstein waves.

Even stronger, for each fixed \(L\ge256\) and any fixed genuinely stationary \(M_L(0)\), the source map has a positive neighborhood in the combined field+state chart, so there is a (possibly L-dependent) \(\delta_L>0\) excluding **all** bare-HJR stationary roots that remain in that neighborhood. The bound (7) is L-uniform **at the flat point**, but no common \(\delta>0\) independent of L is asserted without actual second-source/modulus-of-continuity estimates. A root sequence with a discontinuously changing physical preparation, or one using a genuinely different/extra Book price, is not ruled out by this theorem.

## 4. Necessary complete-price source threshold ON THIS BOX

Let a proposed physically admitted complete same-carrier action be
\[
S^{\rm physical}_{L}=S^{\rm bare\,HJR}_{L}+E_L,
\]
where \(E_L\) denotes **only actually derived and paid** additional native preparation/clock/work/reference/history/controller/normalizer terms, or instead supply a precise typed non-additive operator-source equality. For the flat endpoint \(v_{L,r}=h e_r\) of THIS BOX to be an actual stationary solution with any fixedRIGHT stationary preparation of the bare part, it is NECESSARY (not sufficient) that the full extra coframe source obey
\[
\boxed{L^{-4}D_\rho E_L\big|_{\rho=1}\le-c_*<-10^{-8}\qquad(L\ge256).}\tag{9}
\]
**Stronger FULL-stationary-envelope theorem (no bare-R preparation premise).** Suppose \(M,z\) satisfy the true **complete** internal Euler equations \(D_{M,z}S^{\rm physical}=0\) with the physical fixedRIGHT Gram held fixed, even when \(E\) changes those internal equations. Along any smooth locally stationary section, the full chain rule eliminates **the combined** internal derivative:
\[
\frac d{d\rho}S^{\rm physical}(\rho,M(\rho),z(\rho))
=\partial_\rho(H+J)+\underbrace{\operatorname{Tr}(M^\dagger\Delta_1 M)}_{\ge0}
+\left.\partial_\rho E\right|_{M,z\ {\rm fixed}}.
\]
Thus (9) still holds at a physical stationary flat solution IN THIS BOX **without requiring \(M\) to be stationary for the bare \(R\) alone**. The true necessary compensating price is the **explicit coframe derivative of the complete paid remainder at fixed internal state**, evaluated on that true full-stationary state. The all-4-leg analogue requires \(\partial_{\rho_r}E/L^4\le-c_*/4\) for each original independent scale, because each \(\Delta_r\succeq0\). If E instead changes the operator \(D\), thermal normalization, physical Hilbert chart or carries a non-additive source, this additive comparison must be rederived for the actual model; no such source equivalence is assumed.

In particular any proposed E whose **entire** normalised first source is \(o(1)\) as \(L\to\infty\) CANNOT restore the flat endpoint of this shrinking-native-leg chart. The already owned compact equal-weight stopped Golden *flag-only* first source is zero on the identity-link tree, and it cannot compensate (7) by itself on a genuinely proven shared carrier. A previously discovered p/clock transformation, observational positivity, a match of all40 configured J2 equations, or a finite-curvature readout does not cancel the actual nonzero scalar source. One full paid physical programme must provide a bulk counterpressure of the required size, or a non-additive source-selection mechanism that truly changes the conditional action.

This gives **an explicit quantitative decision fork** for the current \`constitutive/native_sector\` route, conditional on an actual same-action map landing in this box:
- The compulsory complete Book source **derives** the required finite bulk coframe counterpressure and the correct oriented coframe×connection source on the same execution, with every actual internal Euler solved; THEN consume the already proven exact nonlinear Golden-J2 recovery.
- Otherwise the bare conditional \(H+J+R\) branch cannot carry a continuous punctured stationary family whose actual flat image lies in this box and whose fixedRIGHT preparation has the stated stationary limit. Do not repeat geometry or detector catalogues to evade the first-source test.

This is not a claim that the full D0 theory is impossible: the actual Book03 action is algebra-valued and complete G0/oldRIGHT preparation, work and clock contributions have not been uniquely bound to the conditional HJR owner. A different *admitted* native source and a proved equivalence of equation loci, rather than full action equality, may constitute another physical GR route. Such a route must still respect this original flat-source witness under its actual explicit carrier/variation map; the fixed-physical-metric primary map has not been shown to land in this box.

**Scientific verdict after correction:** the ALL-preparations source bound (not one Riesz shell) remains valid on the shrinking-native-leg box, as does the continuous-lift obstruction conditional on landing there. It is not a uniform source threshold at the fixed-physical-metric primary Einstein point. Full physical GR, complete Book action, two-sided refinement and raw216 remain OPEN. \`GR_closed=false\`.

**Bounded rational replay:** \`sources/d0_hjr_flat_density_zero_2026-10-20/check_all_preparations_primary_gr_flat_obstruction.py\`.
