# Literal scene: global minimum, exact 359-variable elimination, and full-source descent

22 October 2026. Existing scientific Draft #334 in `gvakhrushev/d0_15`.
Read snapshot: `5a9764b20c2b7b481ec90d06a711ce3739f4e773`.

**Research, not physical GR promotion.** This result uses the literal normalized
33-vertex / 718-history scene price in the already declared positive-conductance
extension. It does not identify that extension with the binary scene passport,
or the one-reversal return with the two-tick Golden J2 detector.
`GR_closed=false`.

Packet: [proof and replay index](sources/d0_literal_scene_closure_2026-10-22/README.md).

## 1. The mathematical result is a whole internal-sector solution

The existing [shared-scene owner](A4D_NATIVE_SHARED_SCENE_PRICE_SOURCE.md) defines

\[
T=D^{-1/2}AD^{-1/2},\quad L=I-T,\quad
\mathcal B(w)=\beta^{-1}\log\operatorname{Tr}e^{-\beta(I-T)}
-\log\det[(1-z)I+zT^2].                                      \tag{1}
\]

A has all 359 positive cross-zone weights on K(9,11,13); D contains their
moving degrees. Its true complete 718-history feedback has the SAME determinant
as I-T^2, with complementary identity modes retained. The fixed calibration is
\(\beta=3-\sqrt5=2\varphi^{-2}\), \(z=2^{-20}\).

**Theorem.** The entire set of global minima of (1) in this positive-weight
class is

\[
\boxed{w_{uv}=c r_u r_v,\qquad c>0,\quad r_u>0,
\quad\sum_{u\in V_a}r_u=1\ \text{for each of the three zones}.} \tag{2}
\]

All 359 independent weight Euler equations vanish. The minimum family has 31
parameters: thirty normalized vertex-profile parameters and a common scale.
They are NOT declared physical gauge coordinates.

Put \(q_a(u)=\sqrt{r_u}\) within zone a and zero elsewhere. Then

\[
T_*={1\over2}\sum_{a\ne b}q_aq_b^T,\qquad
\operatorname{spec}T_*=(1,-1/2,-1/2,0^{\times30}).              \tag{3}
\]

The full value, including all dark modes, is

\[
\mathcal B_*=\beta^{-1}\log(1+30e^{-\beta}+2e^{-3\beta/2})
-30\log(1-z)-2\log(1-3z/4).                                  \tag{4}
\]

This changes no coefficient of the existing action and fits no Einstein source.
It solves the free conductance problem instead of specifying a desired
conductance as a function of an already constructed action.

### Proof: a global bound, not a numerical root certificate

On symmetric trace-zero matrices with operator norm at most one, the heat
Hessian in a traceless direction X is

\[
\beta\int_0^1\operatorname{Tr}(\rho^s X_c\rho^{1-s}X_c)\,ds,
\quad\rho={e^{\beta T}\over\operatorname{Tr}e^{\beta T}},
\quad X_c=X-\operatorname{Tr}(\rho X)I.
\]

Every coefficient of this quadratic form in an eigenbasis of rho is at least
\(\lambda_{\min}(\rho)\ge e^{-2\beta}/33\). Since Tr X=0,
\(\|X_c\|_F^2\ge\|X\|_F^2\). For
\(f(t)=-\log(1-z+zt^2)\), \(f''(t)\ge-2z/(1-z)\); its divided differences
satisfy the same lower bound, including coinciding eigenvalues. Hence

\[
D^2\mathcal B(T)[X,X]\ge\mu\|X\|_F^2,
\qquad\mu={\beta e^{-2\beta}\over33}-{2z\over1-z}
>\underbrace{{1\over352}-{2\over2^{20}-1}}_{\mu_0=95261/33554400>0}. \tag{5}
\]

The rational bound uses 3/4<beta<1 and e^(-2)>1/8. No commutation of T and X
is assumed. This larger convex matrix space is a proof device, not an
additional class of physically admitted operations.

For arbitrary positive w, let \(D_a=\sum_{u\in V_a}d_u\), and now let q_a
be \(\sqrt{d_u/D_a}\) on its zone. With Q having columns q_a, define
\(B_3=Q^TTQ\). Its off-diagonal entries are
\(W_{ab}/\sqrt{D_aD_b}\), where W_ab is the total conductance between zones.
It has eigenvalues \(1,-1/2+s,-1/2-s\), \(0\le s<1/2\).

Write \(P_a=q_aq_a^T\) and \(Q_a=I_{V_a}-P_a\). Averaging the eight
orthogonal conjugations by \(U_\epsilon=\sum_a(P_a+\epsilon_aQ_a)\),
\(\epsilon_a=\pm1\), gives exactly \(\bar T=QB_3Q^T\), because the
within-zone blocks of T vanish. Strong convexity and orthogonal invariance give

\[
\mathcal B(T)-\mathcal B(\bar T)\ge{\mu_0\over2}\|T-\bar T\|_F^2.
\]

Average the two matrices obtained by exchanging the two non-Perron eigenvalues
of bar T. Their mean replaces those eigenvalues by -1/2. Applying (5) again,

\[
\boxed{\mathcal B(T)-\mathcal B_*\ge
{\mu_0\over2}\|T-\bar T\|_F^2+\mu_0s^2.}                  \tag{6}
\]

The endpoint value is attained by the genuine positive graph (2). If the price
equals B_*, (6) forces T=bar T and s=0. A symmetric zero-diagonal positive
3x3 matrix with spectrum (1,-1/2,-1/2) has all off-diagonal entries 1/2.
Thus the three total zone degrees coincide and w has exactly the form (2).
Conversely (2) attains (4). This proves the minimum and its complete equality
classification over all 359 variables.

## 2. Exact joint elimination, including the mixed field source

Stationarity at (2) is stronger than the particular minimum theorem. For
EVERY conductance tangent at a balanced scene,

\[
\operatorname{Tr}DT=\operatorname{Tr}(P_1DT)
=\operatorname{Tr}(P_-DT)=\operatorname{Tr}(P_0DT)=0.          \tag{7}
\]

The first equality uses the zero diagonal. The Perron eigenvalue is always 1,
so its derivative is zero. Also P_0=I-sum_a q_aq_a^T and every within-zone
block of DT is zero; hence Tr(P_0DT)=0. The remaining projector identity follows.

Let Y denote all remaining fields and independent inputs. Suppose the ACTUAL
operators have matrix-valued functional calculus in the scene T, for example

\[
\Delta(T,Y)=\sum_kT^k\otimes D_k(Y),\qquad
F(T,Y)=\sum_kT^k\otimes F_k(Y),                              \tag{8}
\]

or analytic versions, with the stipulated Hermiticity/positivity. Coefficient
matrices need not commute with one another. This is stronger than commuting
with T at one point: arbitrary fixed vertex ports are not covered.

Cyclicity of the full trace makes every weight source a linear combination of
Tr(P_l DT). Therefore, for every Y,

\[
\boxed{D_w\mathcal B(Y,w_*)=0\quad\text{in all 359 directions}.} \tag{9}
\]

The remaining joint equations are EXACTLY those of the three-sector functional

\[
\boxed{\mathcal B_{\rm red}(Y)=\beta^{-1}\log
\sum_{l\in\{1,-1/2,0\}}m_l\operatorname{Tr}e^{-\beta\Delta_l(Y)}
-\sum_lm_l\log\det[I-zF_l(Y)],\quad(m_1,m_-,m_0)=(1,2,30).} \tag{10}
\]

There is ONE global heat logarithm, and all thirty zero-adjacency modes remain.
The complete remaining source is

\[
D\mathcal B_{\rm red}=-{\sum_lm_l\operatorname{Tr}(e^{-\beta\Delta_l}D\Delta_l)\over Z}
+z\sum_lm_l\operatorname{Tr}[(I-zF_l)^{-1}DF_l].             \tag{11}
\]

Differentiating (9) gives \(\mathcal B_{Yw}=0\). Thus this stationary section
requires no inverse of its singular internal Hessian and introduces no missing
Schur term. This solves the conductance equations by their OWN complete source,
not by freezing an independently selectable preparation.

**Sharp boundary.** At a balanced point \((T_*^2)_{uu}=r_u/2\). A fixed vertex
readout varies along the minimum family. Anchored record, controller, reference
or other non-spectral costs need their actual equations. In particular (9) does
not cancel the nonzero preparation source of the separate native full128
port-CQ experiment. A pure scene spectral action by itself has no nontrivial
reduced field source and is not an Einstein selector.

## 3. The original binary scene and the weighted extension stay distinct

Section 8 of the inherited shared-scene owner already proves constant scalar
price on the dimension-33, rank-at-most-3, quadratic-moment-718 SIMPLE BINARY
passport. Conductance derivatives leave that domain. The new minimizer (2) is
not substituted for that binary graph. Neither the existence nor optimality of
(2) proves its compulsory M1 admission. This distinction is essential when
joining the new internal elimination to the physical field execution.

## 4. Genuine scene heat can also be controlled without operator equality

For any fixed finite graph with positive conductances and positive degrees, set
\(a_v=\max_e|D_v\log w_e|\),
\(b_{vu}=\max_e|D_vD_u\log w_e|\). Differentiating the moving degrees gives

\[
\|D_vL\|_{op}\le2a_v,\qquad
\|D_vD_uL\|_{op}\le5a_va_u+2b_{vu}.                        \tag{12}
\]

One proof writes T=GAG, G=D^(-1/2). The normalized first adjacency derivative
has norm at most a_v by absolute-entry domination by T. The relative degree
jet is a convex average of edge log jets. The second normalized adjacency
jet is bounded by a_va_u+b_vu, while G^(-1)D_vD_uG is bounded by
3a_va_u/4+b_vu/2. Expanding D^2(GAG) gives (12).

For the actual heat H=beta^(-1)log Tr exp(-beta L),

\[
|D_vH|\le2a_v,\qquad
|D_vD_uH|\le(5+4\beta)a_va_u+2b_{vu}.                      \tag{13}
\]

Use DH=-Tr(rho DL), the centred Kubo-Mori covariance in D^2H, and the
logarithmic-mean <= arithmetic-mean inequality. No eigenvalue gap, minimum
edge weight or commuting-jet hypothesis is required. The bound is independent
of graph size. After a genuine internal stationary section, the log jets must
be those of the COMPOSED edge map, including the section's derivatives.

For the inherited two-band j(x,y)=-log[(1-zA)(1-zB)], put
j_x=j_x(0,0)=1.916886717977707...e-8 and lambda_-=j_y/j_x.
For fixed genuine PF weights m_s/rho_s=M_h, let
J_h=sum_s m_s j(tau_h f_s/rho_s,tau_h q_s/rho_s),
c_h=h^4/(M_h tau_h j_x), F_s=(f_s,q_s), K0=max||F_s||,
rho_min=min rho_s. On a fixed convex operand chart containing zero and all
operands, C=sup||D^2j|| gives the exact finite inequalities

\[
|c_hDJ_h[v]-DI_{\rm aff}[v]|
\le{C\tau_hK_0\over j_x\rho_{\min}}h^4\sum_s\|DF_s[v]\|,
\]
\[
|c_hD^2J_h[v,u]-D^2I_{\rm aff}[v,u]|
\le{C\tau_h\over j_x\rho_{\min}}h^4\sum_s
(\|DF_s[v]\|\|DF_s[u]\|+K_0\|D^2F_s[v,u]\|),                \tag{14}
\]

where I_aff=h^4 sum_s(f_s+lambda_- q_s). These are off-null and retain the
actual small source denominator. Combining them with (13) needs an ACTUAL
same-execution J_h; the one-reversal feedback (1) is not renamed two-tick J2.
For bounded indicated smooth-field/log-edge jets and positive lower bounds on
M_h,rho_min, a sufficient window is tau_h->0 and h^4/(M_h tau_h j_x)->0.
The example tau_h=h^2 is sufficient mathematics, NOT a derived native clock.
Consistency alone does not prove exact finite roots or uniform inverse/recovery.

Negative controls are included: direct-sum repetition suppresses heat relative
to an extensive feedback, but a tensor-SUM Hamiltonian does not; growing writer
jets defeat dimension-only suppression. At the single original scene, the
heat kappa source is about 8161.57 times the feedback source. No small finite
residual is inferred from an asymptotic slogan.

## 5. Consumption by the existing all42 theorem and the remaining physical step

If the ACTUAL three blocks in (11) give, on the common f_B=q=0 sheet,

\[
D\mathcal B_{\rm red}=g_hD\sum_s(f_{B,s}+\lambda_hq_s),\quad g_h\ne0,
\]

the owned unrestricted Cartan/Brinkmann theorem supplies all42 field zeros
with Delta_h^perp H(u+h)=-4lambda_h|D_u^+Psi|^2, while (9) supplies all359 scene
zeros at the SAME point. No separate scene solve remains in this class.
This does not claim that the original full operator already satisfies (8).
The actual block map, non-spectral apparatus equations, same-initial writer
and physical refinement remain the missing substitution, not another geometry
root census. The old paired-incidence result remains a separate sufficient
spectral model; its unchanged 88-check replay is retained in the packet.

## 6. Evidence and nonclaims

The two new scripts passed 897 and 182 checks. Normal and python -O outputs
are byte-identical. The 88-check previous paired source replay also matches its
saved receipt. Matrices are reconstructed independently from the published
33/718 formulas, not imported from a full native program. All 359 original
edge sources, all 359x359 Hessian entries, forty balanced profiles and forty
non-equitable perturbations were evaluated. The maximum scene Euler over the
forty profiles is 1.50e-18; the numerical 328-positive Hessian gap is 2.23136e-5.
The global-minimum proof is (5)-(6), not the floating Hessian-rank diagnostic.

No interval certification of that Hessian rank, fresh all42 constructor replay,
independent-agent review, Lean build, repository-wide CI or physical GR closure
is asserted. The source-functional test with a 3-dimensional report uses a
99-dimensional diagnostic carrier, not original full128.

Source pins at the read snapshot:
- shared-scene owner: `c20afcb63f955bfcfb25c561fd853cf30a21af40`;
- [earlier conditional conductance transmitter](A4D_BOOK03_DERIVED_SCENE_J2_SOURCE_TRANSMISSION_2026_10_21.md):
  `d6057607e3f328d5e0158f7fa9b22a3d2c60442f`;
- [original two-band/constitutive owner](A4D_UNPADDED_GOLDEN_N1_CONSTITUTIVE_LEGENDRE_COMPLETE_2026_10_22.md):
  `4f081ff7925b6fa2c3625ae78966929444aeff10`.
