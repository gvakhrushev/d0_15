# EXACT source-level bulk breakthrough: the original full128 recycling reproduces HJR heat through all \(m\sim h^{-2}\) steps on smooth periodic geometry

**20 October 2026 — existing PR #334, not a new task.** Consumes the accepted original full128 Kraus/Julia operator identity [\`A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE\`] as integrated in main #390, the preceding exact one-port/heat and two-moment transfer in \`FULL128_HEAT_PRICE_RECYCLING_BRIDGE.md\`, and the unchanged original full-CAR16 true positive-adjoint \(\Delta=(d+d^\dagger)^2\). It proves a new **full-field, all-step C1 operator estimate** on a specifically declared **smooth periodic** discretization chart. No time-independent Fourier diagonalization, fitted Price, postselection, external zero-cost fair bit, raw216, or compulsory G0 selection.

## 1. The one physical chart: smooth observer, original CAR16 and genuine 128 Kraus records

Let \(h=1/L\) and use the **actual** \(L^4\) periodic-site Hilbert carrier \(\mathcal H_h=\ell^2((\mathbb Z/L\mathbb Z)^4)\otimes\mathrm{CAR}_{16}\) with unchanged right/reference spectator. Fix a bounded open subset of original \(C^2\) coframes, observer gauges and proper Lorentz connections \((e,n,\Omega)\) on the smooth 4-torus, with uniformly bounded first and second site derivatives and with uniformly bounded **first variation** in a declared norm involving one spatial derivative. The original physical fields are sampled as
\[
v_r(x)=h\,e_r(x),\quad U_r(x)=\exp(h\Omega_r(x)),\quad
d_h=h^{-1}\sum_r C(v_r)[\Lambda(U_r)S_r-I],\quad D_h=d_h+d_h^\dagger,\quad \Delta_h=D_h^2.
\tag{1}
\]
For moving observers, conjugate with the actual local positive isometry \(L(n_x)\) before applying the same formulas and derivatives; assume its first two field/site jets bounded. All adjoints are **actual shifted positive adjoints**. A bounded fixed normalization factor \(\nu\in(0,1)\), when used in the native Julia chart, is included inside \(e_r\).

Assume the exact original Julia positivity margin: the four actual contractions \(P_r=C(e_r)\Lambda(U_r)S_r\) and unshifted creation words \(C_r=C(e_r)\) obey
\[
I-P_rP_r^\dagger,\ I-P_r^\dagger P_r,\ I-C_r C_r^\dagger,\ I-C_r^\dagger C_r\ \succeq\ \kappa I
\tag{2}
\]
for one \(\kappa>0\) independent of h and the field chart. The accepted full128 no-active-work input is unchanged: all 64 original label/coefficient outputs and both Golden ports are retained in every round. Its exact recycling CP map has the original already-proved symmetric Walsh/Julia form
\[
T_h^*(X)=T_h(X)=\frac1{16}\sum_{r=0}^3
\bigl[
P_r^\dagger XP_r+P_rXP_r^\dagger+L(P_r)XL(P_r)+R(P_r)XR(P_r)
+C_r^\dagger XC_r+C_rXC_r^\dagger+L(C_r)XL(C_r)+R(C_r)XR(C_r)
\bigr],
\tag{3}
\]
where \(L(P)=\sqrt{I-PP^\dagger}\), \(R(P)=\sqrt{I-P^\dagger P}\). Equation (3) is **the exact effective map of the original retained 64 coefficients**, not a replacement physical measurement; all original port/clock costs stay attached to their actual 128 outcomes.

## 2. Main LOCALITY theorem: all genuine recycling Kraus approximately commute with the ORIGINAL \(\Delta_h\)

**Theorem.** Under (1)–(2), there is an h-independent constant \(C\) for the declared smooth chart and all its declared smooth field tangents such that
\[
\boxed{\quad
\max_{r,A\in\{P_r,P_r^\dagger,C_r,C_r^\dagger,L(P_r),R(P_r),L(C_r),R(C_r)\}}
\|[\Delta_h,A]\|_{C^1(\mathrm{field})}\le Ch .
\quad}\tag{4}
\]

**Fully finite proof (no pseudodifferential existence theorem).** Write the original shift \(S_a\) on the periodic torus and \(M_f\) for a sampled smooth coefficient multiplier. The exact source of every O(h) below is the elementary finite difference
\[
\|[S_a,M_f]\|
=\sup_x\|f(x+ha)-f(x)\|
\le h|a|\,\|\nabla f\|_\infty
\tag{5}
\]
(and the identical field-differentiated identity). Every original \(P_r,C_r\) is a finite coefficient-times-shift word plus an O(h) word from \(\Lambda(\exp(h\Omega_r))-I\); (2) keeps its Julia root domain strict.

For **frozen coefficients at each site**, the CAR creation/annihilation algebra is exact and the flat principal Dirac is
\(d_0(x,\mathbf z)=\sum_r C(e_r(x))(z_r-1)\), with \(|z_r|=1\).
Then \(d_0^2=(d_0^\dagger)^2=0\), and its **full 16-grade** positive square is
\[
(d_0+d_0^\dagger)^2(x,\mathbf z)
=\left\|\sum_re_r(x)(z_r-1)\right\|_{\rm observer}^2 I_{16}
=:\lambda(x,\mathbf z) I_{16}.
\tag{6}
\]
This is a genuine **operator CAR identity**, including all nonorthogonal coframe cross terms; no rank-one CAR/thermal-shell approximation is involved. Expand the degree-two finite products forming the **actual global** \(\Delta_h\) and move sampled coefficient multipliers past shifts using (5). Every difference from the finite-stencil **scalar** operator \(Q_h=\sum_{a\in A_0}M_{q_a(x)}S_a\otimes I_{16}\), obtained by Fourier-expanding \(\lambda(x,\mathbf z)\), is O(h), uniformly in C1 field jets:
\[
\|\Delta_h-Q_h\|_{C^1}\le C_0h.
\tag{7}
\]
In particular \(\|\Delta_h\|\le\Lambda\) uniformly on this chart. Because every \(q_a\) is scalar in CAR and every original finite P/C shift word has smooth coefficients, another use of (5) gives
\(\|[Q_h,P_r]\|_{C^1}+\|[Q_h,C_r]\|_{C^1}\le C_1h\).
Together with (7), this proves the commutator O(h) for \(P_r,C_r\) and their adjoints.

For any of the four positive Julia defect operands \(K=I-PP^\dagger,I-P^\dagger P,I-CC^\dagger,I-C^\dagger C\), (2) gives \(A=\sqrt K\succeq\sqrt\kappa I\). The exact Sylvester relation
\[
A[\Delta_h,A]+[\Delta_h,A]A=[\Delta_h,K]
\tag{8}
\]
and its first field derivative imply
\[
\|[\Delta_h,\sqrt K]\|\le(2\sqrt\kappa)^{-1}\|[\Delta_h,K]\|=O(h),
\tag{9}
\]
and the same O(h) estimate for its **complete field first jet**, because \(A^{-1}\) Sylvester bounds and the actual \(dA,dK,d\Delta\) stay uniform in the strict margin. This proves (4) for **all eight** words of (3). Original Walsh Parseval represents the 64 N_k as fixed finite linear combinations of these same 32 primitive words, so their commutators are O(h) too; no output coefficient is deleted from (3).

## 3. TWO recycling defects are O(h), O(h²) on the original full128 channel

Choose the exact **32-term Kraus representation of the same CP channel (3)**, with each displayed word multiplied by 1/4, and label them \(V_j\), \(j=1,\ldots,32\). This is **only an analysis Kraus decomposition** of exactly the original 64-label marginal CP map, not an erasure or replacement of the original 128 charged output records. Original unitality gives \(\sum_jV_j^\dagger V_j=I\).

Equation (4) gives \(\|[\Delta_h,V_j]\|_{C^1}\le Ch\). Write the original Stinespring isometry \(V:\psi\mapsto(V_j\psi)_j\). Its energy intertwiner has the exact entries \([\Delta_h,V_j]\). Thus, using the true original \(T_h^*\),
\[
\begin{aligned}
\|T_h^*(\Delta_h)-\Delta_h\|_{C^1}&\le C'h,\\
0\preceq T_h^*(\Delta_h^2)-T_h^*(\Delta_h)^2
&=V^\dagger(\Delta_h\otimes I)(I-VV^\dagger)(\Delta_h\otimes I)V,\\
\|T_h^*(\Delta_h^2)-T_h^*(\Delta_h)^2\|&\le C''h^2 .
\end{aligned}\tag{10}
\]
The field derivative of the **positive variance operator** in the second line is O(h²), since both factors in its Stinespring residual are O_C1(h); the field derivative of its operator norm is not needed. Consequently the **actual original complete recycling defects** obey \(\delta_1+\sqrt{\delta_2}\le C'''h\) on the smooth chart, with a directly controlled C1 intertwinement.

## 4. ALL \(m=256h^{-2}\) actual Golden histories converge to the TRUE thermal/feedback source in \(C^1\)

Use the **same original** \(p=\varphi^{-1}\), \(\alpha=p^2h^2/128\), \(m=256h^{-2}\), \(B=I-\alpha\Delta_h\), and the previously derived actual full128 thinned no-accepted CP map \(\mathcal N^*\). The exact full-history 2-moment estimate (18) from the companion note gives
\[
\boxed{
\|(\mathcal N_h^*)^m(I)-B_h^m\|\le C h.
}\tag{11}
\]
The **first actual field variation** is O(h) as well: differentiate the *exact* recurrence (12) of the preceding proof. Its inhomogeneity has norm \(j\alpha^2\Lambda\,O(h)\), and its first derivative has the same bound by (4), (8), the Stinespring intertwinement field jet, bounded \(\|\partial\mathcal N^*\|\le C\alpha\), \(\|\partial B\|\le C\alpha\), and \(j\alpha\le m\alpha=2p^2\). The m-term sum is \(O(m^2\alpha^2h)=O(h)\), while derivatives of the propagators contribute only a uniform multiplicative constant \(O(m\alpha)=O(1)\). Thus
\[
\boxed{
\|(\mathcal N_h^*)^m(I)-B_h^m\|_{C^1(\mathrm{field})}\le Ch.
}\tag{12}
\]
No invented field-source counterterm or spectral projection is introduced; all derivative terms of \(D,T,\rho\) were included. For the capped native-Golden acceptance extraction choose \(M_h=\lceil(4+\gamma)\log L/|\log(5-2\sqrt5)|\rceil\); its finite controller adds O(q^{M_h}) in operator C1 on the same bounded chart, so the result survives a strictly finite executed controller:
\[
\boxed{\|(\mathcal N_{M_h}^*)^m(I)-B_h^m\|_{C^1}\le Ch+O(q^{M_h}).}\tag{13}
\]

The normalizers/feedback are **counting-trace** quantities over ALL \(16L^4\) site/Fock modes. Since \(\|\Delta_h\|\le\Lambda\) and \(m\alpha=2p^2\), \(B_h^m\succeq b_*I\) for an h-independent \(b_*>0\) at sufficiently small h. The survival \((\mathcal N^*)^m(I)\) is positive and C1-close, also bounded below by \(b_*/2\). Hence the usual finite resolvent derivative identities yield
\[
\begin{aligned}
\left\|\log\frac{\operatorname{Tr}(\mathcal N_{M_h}^*)^m(I)}
 {\operatorname{Tr}B_h^m}\right\|_{C^1}&\le Ch,\\
\left\|L^{-4}\operatorname{Tr}\big[
\log(1-z+z(\mathcal N_{M_h}^*)^m(I))
-\log(1-z+zB_h^m)\big]\right\|_{C^1}&\le Ch,
\end{aligned}\tag{14}
\]
for the literal original \(z=2^{-20}\). This is an **operator-source** theorem all the way through the original HJR thermal/feedback functions, on the declared smooth bulk chart, not simply a value-level one-step probability coincidence.

**Interpretation.** On smooth periodic geometry the mismatch from using true fully retained full128 histories instead of the formal heat factor **is O(h) in the normalized bulk first source**. In particular the previously exact positive flat bulk \(H+J\) source is **not** generally cancelled by the history recycling back-action: it is inherited at leading normalized order when the same controller and action readout are chosen. Repairing that pressure still requires the actual **full physical Price/Info/work** or a proved distinct reference-comparison source, not an optimistic appeal to repeated quantum-state disturbance.

## 5. Applicability and limits: DO NOT promote this to physical GR closure

- **Positive actual theorem:** original periodic, uniformly smooth \(C^2\) coframe/observer/link chart, \(U=\exp(h\Omega)\), strict Julia margin, real 64-label/128-port channel, correct true positive adjoints, all site/CAR modes, all repeated history, C1 field-source limit. This is NOT a flat-only Bloch symbol theorem. It applies to varying small-amplitude smooth Lorentz scenes that are **periodic and in the strict chart**, not only constant links.
- **Physical Brinkmann collar:** the accepted exact nonlinear Einstein-positive family has unwrapped null time/transverse collar data. Replacing its unilateral/open shifts by periodic shifts is NOT justified on the boundary. On the open collar, \([S,S^\dagger]\) has O(1) boundary operator norm, so the proof of (7) fails globally in operator norm. An interior-supported/normalized-trace boundary-layer control with actual traction is a separate proof obligation. Do NOT claim this theorem directly on the full open finite GR family.
- **Actual control/payment:** the accepted literal 128 Kraus family is original. The new thinning controller, its twenty challenge bits, its work/archive/clock and complete original \(Cost-Info\) weight are **not demonstrated compulsory**. A positive CP POVM source or event surprisal is not automatically the compulsory physical action. Equations (11)–(14) are exact transfer conditions for the declared POSSIBLE programme, not proof of a native selected Einstein response.
- **Even if completely admitted**, heat/full-history agreement only transports the genuine conditional HJR \(H+J\) sources; it does not turn them into the already configured Golden-J2 Palatini/Einstein action. The independent flat Einstein coframe-source obstruction (already exactly proved for all h) remains. Its compensating genuine paid complete Book03 source must still be derived.
- **No raw216 or all-geometries uniform claim:** the estimate is C1 in a smooth chart; it does not control the original weak all-scene metric-to-GR owner norms or spectra on high-Bloch microstructure. Its physical coframe/observer gauge quotient and actual preparation/clock identity remain separate.

**Most valuable conclusion:** under the physically important **regular continuum** hypothesis, there is NO new explosion of memory terms from repeating the actual 128-outcome measurement \(O(h^{-2})\) times. The full noncommutative memory correction can be proved negligible in the **normalized bulk first source** from native locality and CAR alone. The physical closure frontier has narrowed: neither extra states, multi-round \(\Gamma\) tensors nor another preselected spectral penalty is needed to connect actual serial records to the original HJR heat source in this chart. The remaining problem is the **selected full Book action**, especially its missing flat bulk source and oriented Cartan coupling, not the long history itself.

**Bounded numerical stress test, not theorem proof:** \`check_smooth_car16_recycling_bulk.py\`, actual Julia/defect 32 terms on a fully CAR16-represented reduced 1D site profile, with every remaining role present (their site shifts trivialized only for the diagnostic). Proof equations (5)–(14) are analytic on the full original four-dimensional periodic product, not extrapolated from the reduced diagnostic.
