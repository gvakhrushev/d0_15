# A4D: original 718-edge CP cost yields an exact cosh cubic, a unique dark history current and a quadratic Book source

2026-10-19. **RESEARCH / exact finite original-scene companion to #384**. Upstream input: \`90fc38d\`; consume existing \`D0.Geometry.SignlessSignedCommonCarrier\`, \`D0.Matter.TickS3BaryonAsymmetry\`, \`D0.Spectral.DeltaAlphaExact\`, and the ORIGINAL 718-edge all-walks scalar Book-flow Hessian / 685 archive and dark653 split already developed in this PR. No new action, detector, native preparation, physical mass or GR claim. \`GR_closed=false\`.

## 1. One ORIGINAL directed scalar Cost family, one exact spectrum

With \(\ell=\ln\varphi\), \(p=\varphi^{-1}\), use **all and only** 718 native directed scene edges; set \(d_{uv}=+1\) along the already-owned cycle \(9\to11\to13\to9\), and \(d_{vu}=-1\). Consider the native primitive Cost perturbation \(C_{uv}(\epsilon)=1+\epsilon d_{uv}\), \(K_{uv}(\epsilon)=p e^{-\ell\epsilon d_{uv}}\), positive for \(|\epsilon|<1\).

Every block is zone-constant, so the 30 original vertex Ker modes remain exact zeros for all epsilon. On the original 3-zone quotient \(K_\epsilon\) is represented by

\[
p\begin{pmatrix}
0&11e^{-\ell\epsilon}&13e^{\ell\epsilon}\\
9e^{\ell\epsilon}&0&13e^{-\ell\epsilon}\\
9e^{-\ell\epsilon}&11e^{\ell\epsilon}&0
\end{pmatrix}.
\]

The full **33-site** determinant is EXACT:

\[
\boxed{\det(xI_{33}-K_\epsilon)
=x^{30}\bigl(x^3-359p^2x-2574p^3\cosh(3\ell\epsilon)\bigr).}\tag{1}
\]

Consequences: \(\operatorname{Tr}K_\epsilon^2=718p^2\) for all epsilon; the \(359p^2\) term of \(\alpha_{\rm top}^{-1}=359p^2-p^5\) does not feel the CP bias; the third coefficient (both 1287 triangle orientations) is \(2574p^3\cosh(3\ell\epsilon)\). Thus the exact topological \(\Delta_\alpha\) is *not* a selector of epsilon.

The original **scalar all-path Book macroaction** already constructed in #384 is \(\mathcal A=-\log_\varphi\rho(K_\epsilon)\). For \(\rho_0>0\) satisfying \(\rho_0^3-359\rho_0-2574=0\), implicit differentiation gives

\[
\boxed{\mathcal A'(0)=0,\quad
\mathcal A''(0)=-\frac{23166\ln\varphi}{\rho_0(3\rho_0^2-359)}
=-0.47637445155264586669\ldots.}\tag{2}
\]

The corresponding stationary additive-history variance is exactly
\(\mathcal V_{CP}=23166/[\rho_0(3\rho_0^2-359)]=0.98994751738206263285\ldots\).
It is the *same* native history Schur norm of #384 on this specific CP tangent, not a different fitted feedback operator.

### 1A. Exact graph-imbalance correction; why the native quadratic coefficient is nearly 1, but NOT fitted to 1

For a GENERAL positive complete tripartite \(K(a,b,c)\), let \(S=ab+bc+ca\), \(T=abc\) and \(\rho^3-S\rho-2T=0\) be its native positive adjacency Perron root. The same CP-cycle bias argument gives, with no symmetry of the *sizes* assumed,

\[
\boxed{\mathcal V_{CP}(a,b,c)
=\frac{18T}{\rho(3\rho^2-S)}
=\frac{9abc}{(ab+bc+ca)\rho+3abc}.}\tag{2a}
\]

The second equality uses only the original Perron cubic. Independently, with three true one-direction stationary macro-edge masses \(m_i>0\), \(\sum m_i=1/2\), the previously derived exact native harmonic formula is \(\mathcal V_{CP}=18/(\sum_i1/m_i)\). Cauchy-Schwarz / AM-HM gives **universally**

\[
0<\mathcal V_{CP}\le1
\]

with equality iff the three stationary macro-edge masses are equal. In the original symmetric complete tripartite family this happens exactly when \(a=b=c\): equal macro masses force equal zone stationary masses, and the positive Perron eigenvector equation then forces equal cardinalities.

For the D0 arithmetic progression \(a=n-d,b=n,c=n+d\), the positive Perron root and native CP coefficient have **no linear imbalance correction**:

\[
\frac{\rho}{n}=2-\frac49(d/n)^2-\frac{20}{243}(d/n)^4+O((d/n)^6),
\]

\[
\boxed{\mathcal V_{CP}=1-\frac8{27}(d/n)^2-\frac{56}{243}(d/n)^4+O((d/n)^6).}\tag{2b}
\]

In D0 \(n=11,d=2\), this explains the *internally generated* response \(0.989947517382\ldots\). The near-one coefficient arises from mild zone-size imbalance, NOT an externally chosen unit sterile probability. It remains a native scalar-history fluctuation coefficient, not the exact Book04 neutrino mass-pole normalization.

## 2. One FULL directed original path sees the sign that scalar pressure erases

The original Perron–Doob chain \(P_\epsilon\), **true stationary bulk** \(\pi_\epsilon\) (distinct from the actual one-sided initial \(\mu_0\)), and complete stationary edge law \(\mu_\epsilon=\pi_\epsilon P_\epsilon\) obey EXACTLY:

\[
\boxed{\pi_{-\epsilon}=\pi_\epsilon,\qquad
P_{-\epsilon}(u,v)=\frac{\pi_\epsilon(v)}{\pi_\epsilon(u)}P_\epsilon(v,u).}\tag{3}
\]

Vertex frequencies and the entire scalar pressure are even in epsilon, but the ratio of the two opposite original triangle paths has logarithm \(-6\ell\epsilon\). Therefore an *oriented* complete original Book history observes the sign linearly; a stationary vertex-only readout does not observe it at any order.

The Markov time-reversal relative entropy per transition is not postulated. Differentiating (1) and using the stationary edge ratio gives:

\[
\boxed{
\sigma(\epsilon)=\sum_{uv}\mu_\epsilon(u,v)
\ln\frac{\mu_\epsilon(u,v)}{\mu_\epsilon(v,u)}
=2\epsilon\partial_\epsilon\ln\rho(K_\epsilon)
=\frac{15444\,\ell\epsilon\sinh(3\ell\epsilon)}
{\rho_\epsilon(3\rho_\epsilon^2-359)}\ge0.}\tag{4}
\]

Hence \(\sigma(\epsilon)=2\ell^2\mathcal V_{CP}\epsilon^2+O(\epsilon^4)\) and full directed-history Fisher information rate at zero is \(\ell^2\mathcal V_{CP}\). The *conditional test substitution* \(\epsilon=\Delta_\alpha=-0.000415216862356\ldots\) produces \(\sigma=7.9043235222\times10^{-8}\) per transition; it is NOT selected physics or a neutrino mass.

### 2.1. Crucial native boundary: ORIGINAL one-sided initial Perron law does see CP sign

The even stationary \(\pi_\epsilon\) of (3) is **NOT** the native one-sided preparation \(\mu_{0,\epsilon}(u)=r_\epsilon(u)/\sum_vr_\epsilon(v)\). A complete ORIGINAL Perron path starts from the latter; it converges to \(\pi_\epsilon\) only with bulk mixing. Under the same CP Cost family, its actual initial three **zone-total** masses at epsilon=0 are

\[
\mu_{0,0}=(0.29185356535552,\ 0.33498406985153,\ 0.37316236479295).
\]

The exact first-order source follows from the SAME Poisson potential \(\xi\) in (6):

\[
\boxed{\partial_\epsilon\mu_{0,\epsilon}(Z_i)|_0
=-\ln\varphi\cdot\mu_{0,0}(Z_i)
\bigl(\xi_i-\mathbb E_{\mu_{0,0}}\xi\bigr).}\tag{3a}
\]

The true values are \((+0.00536188904515,-0.01310683988815,+0.00774495084300)\), summing to zero, verified against the actual right Perron eigenvector derivative on the original 33-site graph to better than \(3\times10^{-15}\). In contrast \(\partial_\epsilon\pi_\epsilon|_0=0\) **exactly**. Thus an original finite one-sided record can detect sign through its starting endpoint distribution; only the **stationary bulk one-point distribution** is sign-blind. Full directed path ratios remain odd as in (5). Do not silently replace \(\mu_0\) by \(\pi\), or claim that *all* vertex probabilities erase the seam.

## 3. Exactly one invariant CP current in the actual history dark653

Let \(\bar Z=1287^{-1}\sum_{a\in9,b\in11,c\in13}[a,b,c]\). On the ORIGINAL 359 oriented unoriented-edge cochain carrier, exact rational enumeration gives

\[
\boxed{\partial_2\bar Z=\frac1{99}\sum_{AB}e_{AB}+
\frac1{143}\sum_{BC}e_{BC}-\frac1{117}\sum_{AC}e_{AC},\quad
\partial_1\partial_2\bar Z=0,\quad
\langle d_{CP},\partial_2\bar Z\rangle=3.}\tag{5}
\]

This is a 1-*boundary* of a 2-chain, NOT an H1 nontrivial class (the original full clique complex has H1=0). Among \(S_9\times S_{11}\times S_{13}\)-invariant directed full-edge currents, the original six macro-edge coordinates subject to both source- and target-zero conditions have a 6x6 constraint matrix of exact rank5. Therefore the space of such full-history dark currents is **one dimensional**. This generator belongs to the original rank653 future-invisible subspace of the rank685 Book-history archive, not merely the rank32 future-vertex feedback of #334.

The original stationary one-direction macro-edge masses are \(m=(0.14738111205163848,0.18844067994169849,0.16417820800666303)\ldots\). The **actual native Poisson-corrected** CP score \(h\) satisfies

\[
j=\frac3{m_{AB}^{-1}+m_{BC}^{-1}+m_{CA}^{-1}},\quad
h_e=j/m_e,\quad
\boxed{\mathcal V_{CP}=\sum_{uv}\mu_{uv}h_{uv}^2
=\frac{18}{m_{AB}^{-1}+m_{BC}^{-1}+m_{CA}^{-1}},}\tag{6}
\]

exactly matching (2) after the native \(\ln\varphi\) coefficient. Its full directed-edge Fisher vector \(g_{uv}=\sqrt{\mu_{uv}}h_{uv}\) obeys \(J_{\rm past}^Tg=J_{\rm future}^Tg=0\).

## 4. Same original edge record, precise *statistical* Ker30 coupling; dynamic no-go

Let \(Q=\operatorname{proj}_{\ker A}\) on the ORIGINAL vertex carrier and let \((u,v)\) be ONE genuine retained native edge. The history-score-conditioned vertex observation \(Y_{uv}=h_{uv}Qe_u\) has \(\mathbb E_\mu Y=0\) but

\[
\boxed{\mathbb E_\mu YY^T
=c_9\Pi_{W_9}+c_{11}\Pi_{W_{11}}+c_{13}\Pi_{W_{13}},\quad
c_i=\frac{j^2}{n_i}\Bigl(\frac1{m_{ij}}+\frac1{m_{ik}}\Bigr)>0.}\tag{7}
\]

The exact rank is30, multiplicities (8,10,12), and numerical eigenvalues (0.03894598916, 0.02992413041, 0.02386678311). This reads a positive *statistical covariance* from the same actual 718 transition labels with no invented archive copies; it is NOT a physical Ker excitation or neutrino mass.

**Strong negative control:** since every primitive \(K_\epsilon\) block remains constant within zones, \(K_\epsilon Q=QK_\epsilon=0\) for ALL epsilon. Neither the CP orientation nor the exact alpha numbers alone dynamically couples the history dark653 to vertex Ker30. Real zone-internal spatial/record-field variations and a complete native selected Book→Lorentz actuation remain necessary. The scalar real-positive \(\cosh\) is not a CAR-unitary \(\cos\) neutrino oscillation.

## 4A. NEW: exact SAME original Book quadratic source = the registered full718 two-arm contrast Hessian

This eliminates the previous gap between "archive variational norm" and an actually normalized complete-edge RECORD on THIS same scalar programme, without selecting a new field or action. On the already-owned **current 718-edge register** \(S_\epsilon:H_{33}\to H_{718}\) of #334 set

\[
\chi_\epsilon:=S_\epsilon\sqrt{\pi_\epsilon},\qquad
\chi_\epsilon(u,v)=\sqrt{\mu_\epsilon(u,v)},\quad \|\chi_\epsilon\|=1.
\]

This is the canonical square-root amplitude encoding of the TRUE original complete positive stationary bulk **edge law**. It is a mathematical faithful encoding, not a claim that the compulsory full128 quantum detector coherently prepares it. Define the genuine all-outcome two-line statistical overlap (Bhattacharyya affinity)

\[
\mathcal Z(\epsilon_+,\epsilon_-)
=\sum_{(u,v)\in E}\sqrt{\mu_{\epsilon_+}(u,v)\mu_{\epsilon_-}(u,v)}
=\langle\chi_{\epsilon_-},\chi_{\epsilon_+}\rangle.
\]

Because the ORIGINAL CP bias has \(\partial_\epsilon\pi_\epsilon|_0=0\), its complete Markov score on every actual edge is \(\partial_\epsilon\log\mu_\epsilon|_0=-\ell h_{uv}\), with \(h\) the already-owned **dark653** Poisson innovation of (6). Thus

\[
\boxed{\partial_\epsilon\chi_\epsilon|_0
=-\frac{\ell}{2}(\sqrt{\mu_0}\,h),\qquad
J_0^\top\partial_\epsilon\chi|_0=J_1^\top\partial_\epsilon\chi|_0=0.}\tag{8}
\]

The derivative lies in the ACTUAL original edge archive's future-invisible dark653. The same Book Hessian in (2) is EXACTLY the **two-line statistical distinguishability second source**:

\[
\boxed{
\partial_{\epsilon_+}\partial_{\epsilon_-}
\log\mathcal Z|_{(0,0)}
=\|\partial_\epsilon\chi|_0\|^2
=\frac{\ell^2}{4}\mathcal V_{CP},
\qquad
\mathcal A_{\rm Book}''(0)
=-\frac{4}{\ell}\,\partial_{\epsilon_+}\partial_{\epsilon_-}
\log\mathcal Z|_0.}\tag{9}
\]

There is NO fitted proportionality constant: \(4\) comes from the square-root record amplitude, \(\ell=\ln\varphi\) from the original Book Cost base. This identity is **not** asserted for arbitrary original Cost tangents with moving \(\pi'\ne0\); CP antisymmetric first-source and (3) are necessary.

Moreover, EXACT time reversal (3) gives \(\chi_{-\epsilon}(u,v)=\chi_\epsilon(v,u)\), and the full direct/reverse record overlap obeys

\[
\boxed{1-\mathcal Z(\epsilon,-\epsilon)
=\frac{\ell^2\mathcal V_{CP}}2\epsilon^2+O(\epsilon^4).}\tag{10}
\]

At the **conditional** comparison \(\epsilon=\Delta_\alpha\), direct ALL718 sum gives \(\mathcal Z=0.9999999802391912621409198\ldots\), loss \(1.9760808737859080\times10^{-8}\); the tangent norm-square is \(0.05730925481085409018\ldots\). The original Book Hessian reconstructed from (9) is \(-0.47637445155264586669\ldots\), identical to (2) without a source fit. The two-arm overlap here is a **REAL classical Hellinger/Bhattacharyya comparison**, not a nonzero imaginary CAR/Weyl relative phase. The latter and all full128 native physical Cost−Info remain open.

## 4B. DECISIVE ONE-SCALAR CONSUMER: CP ↔ physical field same-Book Hessian is one directed Cost circulation

The full original 718-edge scalar Book-flow Hessian, already proved in this PR, now yields a sharper selection rule for an **ARBITRARY** original geometric field tangent \(V\), not just a zone-homogeneous perturbation. Let \(d_{uv}(V)=D_V s_{uv}\) be its **actual** original primitive directed edge Cost−Info derivative, with no fit, and let \(\bar d_{AB}\) denote the mean of \(d_{uv}\) over the **99 real directed AB edges**, likewise the five other ordered zone pairs. Define

\[
\boxed{\Gamma(V)=(\bar d_{AB}-\bar d_{BA})+
(\bar d_{BC}-\bar d_{CB})+(\bar d_{CA}-\bar d_{AC}).}\tag{11}
\]

This is the orbit-averaged directed cycle circulation of the *given* 718-dimensional field source. It is invariant under original vertex endpoint Cost allocation: for arbitrary actual Info jets \(D I_u\) (not assumed constant within zones) and ANY Book theta, \(s_{uv}=C_{uv}-\theta I_u-(1-\theta)I_v\) gives **exactly** \(\Gamma(Ds)=\Gamma(DC)\), because the three zone-mean Info gradients telescope. It also annihilates any vertex coboundary and all reversal-even edge-Cost tangents.

The same ORIGINAL Markov-Poisson harmonic CP score \(h_{uv}\) from §3 satisfies \(\mu_{uv}h_{uv}=j/(n_i n_j)\) on the forward i→j macro-orbit, with reversed sign on j→i, where

\[
j=\frac3{m_{AB}^{-1}+m_{BC}^{-1}+m_{CA}^{-1}}
=0.16499125289701043881\ldots
\]

is fixed by the ORIGINAL full Book stationary edge-flow masses. Consequently the **exact mixed Schur Hessian of the SAME scalar Book macroaction** has a universal 718→1 reduction:

\[
\boxed{H_{\epsilon V}
=\mathbb E_\mu[D_{\epsilon V}^2s]
-(\ln\varphi)\sum_{uv}\mu_{uv}h_{uv}d_{uv}(V)
=\mathbb E_\mu[D_{\epsilon V}^2s]-(\ln\varphi)j\,\Gamma(V).}\tag{12}
\]

There is no loss of vertex-resolution information in this statement about THIS particular CP mixed Hessian: all 718 arbitrary field costs enter but only **one gauge-invariant circulation** survives the contraction against the unique \(G\)-invariant CP harmonic.

For jointly AFFINE primitive edge Costs with independently varied epsilon and V (so \(D_{\epsilon V}^2s=0\)), the coefficient is fixed with no free normalization:

\[
\boxed{H_{\epsilon V}=-0.07939574192544097778\ldots\,\Gamma(V).}\tag{13}
\]

Negative controls passed on all actual718 edges: symmetric original AB Cost tangent has \(\Gamma=0,H=0\); arbitrary genuine 33-vertex Info derivative at theta=2/5 has \(\Gamma=0,H=0\); any vertex-gradient has zero; arbitrary **non-zone-symmetric** deterministic 718-edge field source agrees with (12) to ~\(10^{-67}\) using 65-digit arithmetic. Positive CP self-source has \(\Gamma(d_{CP})=6\) and \(H_{\epsilon\epsilon}=-6\ell j=-0.47637445155264586669\ldots\), exactly the original independent cubic/Hellinger result. If the physical full128 J23-induced *original* edge price derivative is reversal-even, the scalar CP coupling is provably ZERO at this order; a nonzero \(\Gamma(J_{23})\) produces a completely determined native scalar Book cross term.

**This is a necessary-and-sufficient scalar-CP source discriminator modulo actual mixed primitive Cost second jets**, NOT the full Lorentz/Einstein selection. No original full128/CAR/clock-to-edge derivative has yet been physically established, and the real original full128 J23 detector's nonzero first covector must not be replaced with this positive-scalar macroaction.

## 5. Parent consumption and reproducibility

**This resolves one existing scalar-history CP sector**, not the full physical action. The consuming live parent #384/#334 must still map the *same admitted original full128 Julia/CAR/oldRIGHT/reference/controller/clock* to actual 718 directed Cost/Info **field derivatives**, preserve ordered Lorentz memory and full preparation sources, and compare the SAME full action's 16 coframe+24 Lorentz+matter variational Euler to the already-owned finite Einstein comparator. No \(\epsilon=\Delta_\alpha\) selection, passport promotion, #216 closure or GR claim.

Independent scripts (supplied in the accompanying research snapshot) check: exact polynomial, full 718-edge transition reversals and sigma, all 1287 triangle boundaries/rank, and full-rank30 native score-conditioned covariance. All four PASS.