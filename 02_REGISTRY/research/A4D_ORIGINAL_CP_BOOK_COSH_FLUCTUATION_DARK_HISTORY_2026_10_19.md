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

## 5. Parent consumption and reproducibility

**This resolves one existing scalar-history CP sector**, not the full physical action. The consuming live parent #384/#334 must still map the *same admitted original full128 Julia/CAR/oldRIGHT/reference/controller/clock* to actual 718 directed Cost/Info **field derivatives**, preserve ordered Lorentz memory and full preparation sources, and compare the SAME full action's 16 coframe+24 Lorentz+matter variational Euler to the already-owned finite Einstein comparator. No \(\epsilon=\Delta_\alpha\) selection, passport promotion, #216 closure or GR claim.

Independent scripts (supplied in the accompanying research snapshot) check: exact polynomial, full 718-edge transition reversals and sigma, all 1287 triangle boundaries/rank, and full-rank30 native score-conditioned covariance. All four PASS.