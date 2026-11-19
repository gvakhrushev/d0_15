# Shrinking-native-leg full H+J+R scale source: corrected relation to the primary GR carrier

**20 October 2026 — conditional matrix-family analytic source theorem / existing
research Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334).**
Parent task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Phase: `constitutive -> native_sector -> gr_operational_realization`.
No new action, task, source term, claim/Book status or physical selector.
`GR_closed=false`.

**23 October 2026 normalization correction.** This note computes the conditional full HJR source on the explicit native creation-leg family `v_h=h sqrt(rho) e`. Its arithmetic and formulas below are retained. The former interpretation as the SAME fixed-physical-metric [primary Einstein family](D0_GR_PRIMARY_POSITIVE_CASE.md) omitted an inverse-coframe/mesh factor and is withdrawn.

The original Palatini edge is \(w_h=hE_{\rm phys}\): see the [all40 sampling](../gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md), (1), and its [constructor](sources/d0_arbitrary_brinkmann_all40_2026-10-19/check_all40_arbitrary_brinkmann.py), lines 33–36. By contrast the [native coframe owner](A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md), §2, uses \(v=\eta E_{\rm phys}^{-T}\), and the [full-Lorentz owner](A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md), (4), already has the factor \(h^{-1}\) in d. These are different typed variables.

For the [actual kinematic map](A4D_SAME_HISTORY_PRICE_AND_SOURCE_COMPOSITION_2026_10_20.md), §7,
\[
 E_N=\nu^{-1}S E_{J2},\qquad
 v_N=\nu S\eta E_{J2}^{-T}.
\]
The [literal coframe check](sources/d0_same_history_price_composition_2026-10-20/check_connection_coframe_review.py), lines 26–35, uses physical E_J2 with no h. At fixed physical flat E_J2 and fixed nu this gives
\[
 \Delta_N=\nu^2 h^{-2}\sum_r\omega_r I_{16},\qquad
 \rho_{\rm box}=\nu^2/h^2.
\]
Thus fixed \(\nu=3/5\) leaves the bounded \(0<\rho\le1\) chart on fine meshes. In contrast this note's scalar box reconstructs \(g_{h,\rho}=h^{-2}\rho^{-1}\eta\); fixed rho does not fix the physical metric.

The distinct [fixed-v refinement theorem](sources/d0_hjr_flat_density_zero_2026-10-20/REFINING_UNIFORM_SOURCE.md), with \(v=s e/4\) independent of h and its correct \(L^2\) spectrum, remains unchanged. The present shrinking-leg source test is not a no-go for an unidentified complete physical D0 Cost–Info programme or for the primary fixed-metric recovery.

## 1. The primary flat member and the distinct native chart

Start with the original all40 finite Brinkmann carrier at H=0,
constant original CAR scalar/top amplitudes and the original proper
Lorentz links U_r=I. The finite star plus configured Golden-J2 matter
source has **all** independent coframe, link and material Euler rows
zero, for every h. Its continuum metric is exactly Minkowski; every
positive constant metric scaling is another vacuum Einstein member.
Use the physical unwrapped/Dirichlet sector or its exact flat periodic
regulator to test local source compatibility. No independent Einstein
field equation is installed in the HJR model.

Let eta have null eta_(+,-)=1, eta_(2,2)=eta_(3,3)=-1.
With constant unit observer n=(e_++e_-)/sqrt(2), the actual positive
observer fibre
\[
h_n=-\eta+2n_\flat\otimes n_\flat
\]
makes the four native null/spatial reference legs `e_r` positively
orthonormal: `h_n(e_r,e_s)=delta_rs`. This is the **original
Lorentz/observer-positive CAR pairing**, not a Euclidean replacement
of the physical Lorentz metric. Keep ALL original CAR16 grades.

On the original periodic L^4 site carrier, with h=1/L, use
\[
v_r(x;\rho)=h\sqrt{\rho}\,e_r,\quad
U_r=I,\quad n_x=n,\quad \rho>0.
\tag{1}
\]
The scale `rho=1` is a nondegenerate shrinking native creation-leg chart,
with reconstructed metric h^-2 eta. It is not the native inverse-coframe
image of the fixed physical flat member above. Varying rho is an actual
coframe direction of THIS conditional matrix experiment. Fix the actual
old reference128 Gram
I_128/128 and take its entire eight-momentum x CAR16 isolated positive
Riesz preparation. At EACH finite L>=4 this rank128 shell exists and
commutes with Delta, so every fixed-Gram LEFT preparation equation
is satisfied; its gap need not be uniform as h->0. We do NOT assume
stationarity of the geometric/observer/clock equations in HJR.

## 2. Exact full-CAR spectrum and UNCHANGED conditional original price

In the [original full-Lorentz positive-adjoint
owner](A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md) and
[unchanged whole-HJR action](A4D_EXACT_CURVED_WHOLE_HJR_FIXED_COLLAR_ROOT_2026_10_20.md),
keep
\[
d_h=h^{-1}\sum_r C(v_r)(S_r-I),\quad
\widehat D_h=d_h+d_h^\sharp,\quad \Delta_h=\widehat D_h^2,
\]
\[
B_h=I-\alpha_h\Delta_h,\quad
Z_h=\operatorname{Tr}_H B_h^{m_h},\quad
F_h=1-z+zB_h^{m_h},
\quad S_h=\frac{\log(C_h Z_h)}{\beta}
 -128\operatorname{Tr}_H\log F_h
 +\operatorname{Tr}(M_h^*\Delta_h M_h).
\tag{2}
\]
All native constants are UNCHANGED:
\[
p=\varphi^{-1},\quad
\alpha_h=\frac{p^2h^2}{128},\quad
m_h=256L^2,\quad
\beta=m_h\alpha_h=2p^2,\quad z=2^{-20}.
\tag{3}
\]
The declared workspace `C_h` is field-independent in THIS
conditional experiment; it can depend on L but contributes no
coframe derivative. All thermal/feedback bands and all 16 CAR grades
are counted, no trace normalization is smuggled into the price.
Actual full native preparation/work/clock/Info terms outside (2)
are NOT set to zero physically: they are explicitly unowned.

At Bloch momentum theta_r=2pi k_r/L, exact CAR anti-commutation
and the TRUE shifted positive adjoint give
\[
\boxed{\Delta_h(\rho,k)=\rho\,\mu_L(k)I_{16},
\qquad
\mu_L(k)=\sum_{r=0}^3(2-2\cos(2\pi k_r/L)).}
\tag{4}
\]
This holds on the explicit native creation-leg family (1), with its
genuine CAR differential. It does not identify (1) with the physical
Palatini coframe or its inverse-frame image. In particular
\[
0\le\mu_L\le16,\quad \sum_k\mu_L(k)=8L^4,\quad
\mu_{1,L}=2-2\cos(2\pi/L)>0.
\tag{5}
\]
For the entire 128-dimensional lowest nonzero shell
the original fixed-right Riesz Rayleigh term is exactly
\(\operatorname{Tr}(M_h^*\Delta_h M_h)=\rho\mu_{1,L}\).
No complementary eigenvalue is deleted.

Set `b_k=1-alpha_h rho mu_L(k)`, `w_k=b_k^m`,
`Q_L=sum_k w_k`. With the full trace `Z=16Q_L` and
all full CAR16 feedback contributions retained, the ORIGINAL action is
\[
\boxed{
S_L(\rho)=\frac{\log(16C_hQ_L)}\beta
 -2048\sum_k\log(1-z+z w_k)+\rho\mu_{1,L}.}
\tag{6}
\]
Consequently its exact ORIGINAL first geometric source at fixed L is
\[
\boxed{
\partial_\rho S_L=
-\frac{\sum_k\mu_L(k)b_k^{m-1}}{Q_L}
+2048z\beta\sum_k
 \frac{\mu_L(k)b_k^{m-1}}{1-z+zb_k^m}
+\mu_{1,L}.}
\tag{7}
\]
This is the real entire H, feedback J, moving-preparation R
first variation. The global `-Z_i/Z` and feedback multiplicity
`128*16=2048` are essential; `z` and clock depth are not fitted.
The underlying native full128/Golden preparation is a conditional
mathematical realization, NOT proof that Book03 selects (2).

## 3. Analytic all-h conclusion on compact shrinking-leg scale intervals

For every compact interval `I subset (0,infinity)` of fixed
box-coordinate rho values, the original strict Julia/B-positive chart is
valid for all sufficiently small h. The complete **per-site coframe
dilation source** has an honest, uniform continuum limit
\[
\boxed{
\frac1{L^4}\partial_\rho S_L(\rho)
\ \longrightarrow\
\mathcal P(\rho)
=2048z\beta\int_{[0,2\pi]^4}
\frac{\mu(\theta)e^{-\beta\rho\mu(\theta)}}
 {1-z+z e^{-\beta\rho\mu(\theta)}}\,
\frac{d^4\theta}{(2\pi)^4}>0,\quad
\mu=\sum_r(2-2\cos\theta_r).}
\tag{8}
\]
The convergence is uniform for \(\rho\in I\); it is O(h²) after
the smooth-periodic trapezoid and finite-B estimates. Thus the
original HJR homogeneous flat branch has NO scale-stationary point
on any compact fixed-rho interval of this shrinking-leg chart when L is sufficiently
large: changing the common scale of these native creation coefficients strictly
changes the action. No fixed-physical-metric refinement conclusion follows.

**Proof.** Since `alpha_h=O(L^-2)` and
`m_h alpha_h=beta`, the entire Bloch bands satisfy uniformly
\[
b_k^{m_h}, b_k^{m_h-1}\to e^{-\beta\rho\mu(\theta_k)}
\]
with O(L^-2) error on any such compact rho chart. The H term
in (7) is bounded independently of L by `16/min b`, hence
vanishes after division by L⁴. The R term is `<=4/L^4`.
The positive feedback J term is the Riemann sum of a uniformly
smooth periodic bounded function and tends to (8). The integrand
is positive away from theta=0; on any compact rho interval its
integral is continuous and has a strictly positive minimum.
No assumptions about a microscopic gravitational Lagrangian or
an Einstein equation are used here.

At the exact box point \(\rho=1\), (8) has the independent
convergent Bessel-series representation
\[
\begin{aligned}
\mathcal P(1)
 &=\frac{2048z\beta}{1-z}
   \sum_{n=0}^\infty
   \left(-\frac{z}{1-z}\right)^n
   {\cal I}((n+1)\beta),\\
{\cal I}(t)&=8e^{-8t} I_0(2t)^3[I_0(2t)-I_1(2t)].
\end{aligned}\tag{9}
\]
Here \(\mathcal I(t)=\int\mu e^{-t\mu}\) follows by
differentiating the factorized torus heat trace
\(\int e^{-t\mu}=e^{-8t}I_0(2t)^4\).
The alternating series is absolutely convergent since
`z/(1-z)<10^-5`; positivity follows from (8), NOT from
declaring alternating terms positive. Its high-precision diagnostic is
\[
\boxed{\mathcal P(1)=
0.00008261452974774104031023512849688104\ldots>0.}
\tag{10}
\]

## 4. Explicit all-L rational source inequality, no numerical threshold fit

More strongly, for EVERY integer L>=256, at rho=1:
\[
\boxed{\frac1{L^4}\partial_\rho S_L(1)>10^{-8}.}
\tag{11}
\]
This is an exact rational-inequality proof, not a numerical finite-L
survey. Use \(3/8<p^2<2/5\), so
\(3/4<\beta<4/5\). For every Bloch mode,
\[
0\le\alpha_h\mu_L<1/(20L^2)\le1/80,\quad
b_k>79/80.
\]
Since \(-\log(1-t)\le t/(1-t)\),
\[
(m_h-1)(-\log b_k)
<\frac{16\beta}{79/80}
<\frac{1024}{79}<13.
\]
The elementary exact series bound
\(\mathrm e<68/25\) and
\((68/25)^{13}<500000\) yield
\[
b_k^{m_h-1}>e^{-13}>1/500000.
\tag{12}
\]
The entire negative H source is bounded below by
\[
-\frac{\sum_k\mu_k b_k^{m-1}}{Q_L}>
-\frac{16}{79/80}=-1280/79.
\]
Since \(1-z+zb_k^m\le1\), positivity of every
CAR16 feedback term and (5) give
\[
2048z\beta\sum_k\frac{\mu_k b_k^{m-1}}{1-z+zb_k^m}
>\frac1{512}\,\frac34\,\frac{8L^4}{500000}
=\frac{3L^4}{128000000}.
\]
The moving rank128 Rayleigh derivative is nonnegative.
Thus at L>=256,
\[
\frac{\partial_\rho S_L(1)}{L^4}
>\frac3{128000000}-\frac{1280}{79L^4}
\ge\frac3{128000000}-\frac{1280}{79\cdot256^4}
>10^{-8},
\]
the last inequality being exact rational arithmetic. This proves
(11) without invoking a continuum limit.

## 5. Local coframe Euler obstruction on the shrinking-native-leg chart

At the homogeneous flat native state, the original fullHJR functional
and rank128 Riesz preparation are invariant under translations of
the L⁴-site regulator. Let \(V_x\) be the original **local** coframe
tangent which changes all four legs at only site x by
\(\delta v_r=h e_r/2\), holding ALL Lorentz links,
observer, other sites and the moving preparation Euler at their
actual baseline. Then \(\sum_x V_x\) is the derivative
\(\partial_\rho v|_{\rho=1}\). The true reduced first source obeys
\[
DS_{HJR}[V_x]=\frac1{L^4}\partial_\rho S_L(1)
 >10^{-8}\quad\text{for every site x and L>=256.}
\tag{13}
\]
The fixed-Gram preparation Euler and the Riesz-envelope identity
justify using the reduced action; it has no deleted complement.
Although the rank128 spectral gap shrinks with h in this
different flat chart, it remains nonzero at each finite L:
the argument claims a FIRST derivative at the baseline, not a
uniform preparation neighborhood.

On a separately specified flat Palatini configuration, every based
plaquette is identity, every original six-face
\(f_i(e,U)=0\), and every independent **coframe** first source
\(DS_\star[V_x]=0\). Constant \(\Psi\) makes the original
configured Golden-J2 scalar/top null-matter source zero as
well. The original exact finite all40 theorem includes such flat
Palatini configurations as geometric/material roots. Therefore (13)
precludes equality with a zero Palatini covector IF an actual
same-action carrier map lands in this shrinking-leg chart and
transports this tangent. The former claim that the fixed physical
primary map supplies that identification is withdrawn.

The claim is specifically about the CONDITIONAL (2)
and that genuine original scale tangent, not about an
unproved statement that every `D0` physical state must admit
it. It does not prove that any arbitrary curved solution is
excluded from the total yet-to-be-selected native theory.

## 6. Reverse physical conclusion, not another geometry campaign

If the actual complete paid physical D0 law on this SAME
admitted oldCAR/oldRIGHT/controller/preparation/clock
programme is genuinely \(\mathcal S_{\rm physical}=S_{HJR}+E\),
and if an actual source/tangent map places a required flat endpoint
in THIS shrinking-native-leg chart, then necessarily
\[
\boxed{
\lim_{L\to\infty}\frac1{L^4}\partial_\rho E(1)
=-\mathcal P(1)\ne0,
\quad
DE[V_x]= -DS_{HJR}[V_x]
\ \text{at every finite flat root in this box}.}
\tag{14}
\]
A merely vanishing/o(1) extra source on these specified local
directions CANNOT restore this box endpoint's stationary Euler.
This threshold is not established at the fixed physical primary metric.
Equation (14) is a **necessary compatibility test of an
independently DERIVED native price**, not an instruction
to insert \(-S_{HJR}\) or a fitted cosmological counterterm.

One mathematically explicit *conditional comparison escape*
is an actually executed and fully charged two-arm
same-coframe contrast
\[
S_{\rm rel}(e,U)=S_{HJR}(e,U)-S_{HJR}(e,I).
\tag{15}
\]
Its pure-flat coframe Euler vanishes by identity at U=I,
and its link Euler equals the original HJR link Euler.
This algebraic identity is NOT selection of the physical
complete Cost−Info: both arms, their references, result
records, controller and paid work must be present in the
original compulsory programme. It only shows why an
ACTUAL relative verification might screen the extensive
flat pressure without changing the original spectral
operator. The separate oriented CAR/Jones two-history
source still needs genuine physical admission and source
identification; (15) alone does NOT produce signed
Palatini curvature or its full 40 equations.

**Corrected scientific boundary:** the full HJR spectral price
has the displayed nonzero source on its shrinking-native-leg
family. A proposed source equivalence whose ACTUAL carrier map
lands there must satisfy (14), with all paid contributions retained.
The fixed physical primary Einstein map instead requires its own
full source analysis with the h^-2 spectrum; this note does not
exclude that application. The existing `constitutive/native_sector`
owner must establish the actual operator/tangent/price map and
the signed curvature/matter and refinement transport. A geometric tensor
identity, another
rank census or a small terminal-flags error cannot
discharge that premise. `GR_closed=false`.

## 7. Reproduce

`python3 02_REGISTRY/research/sources/d0_hjr_flat_density_zero_2026-10-20/check_common_einstein_coframe_scale.py`

The script proves every rational inequality in (11) from
exact integer fractions, computes the independent
Bessel expression in (9) and replays the original complete
16L⁴ spectral trace at L=8,16,24,32,40 as **diagnostics**.
No independent source owner, existing #334 task or
accepted GR goal is changed.
