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


## 6. SAME-128-PORT SIGN RESULT: original paid port Cost cannot cancel the already-owned flat HJR source

The analytic smooth transfer above solves the serial-memory error; it does NOT supply the needed flat Einstein counterpressure. An exact independent conclusion is available from the **actual original paid-port full-history source itself**, without the optional thinning/challenge controller.

On the unchanged periodic flat \(U=I\) carrier and four independent positive creation-leg scales \(v_r=h\sqrt{\rho_r}e_r\), every momentum block of the true fullCAR16 Dirac square is
\[
\Delta_{\boldsymbol\rho}(k)
=\Big[\sum_r\rho_r\omega_r(k)\Big] I_{16},\quad
\omega_r(k)=2-2\cos(2\pi k_r/L)\ge0 .
\]
Every original N_k is block diagonal in the momentum label (although NOT scalar in CAR), so for every bounded function f,
\(T^*_{\boldsymbol\rho}(f(\Delta_{\boldsymbol\rho}))=f(\Delta_{\boldsymbol\rho})\) **exactly**. The actual full128 unconditional channel \(\Phi\) therefore satisfies \(\Phi^*(\Delta)=\Delta\). The accepted literal complete two-port code, cost1 for direct and cost2 for return, obeys at **every** integer horizon m for every normalized fixed input/reference density \(\rho_{\rm in}\):
\[
\boxed{
\mathbb E_{\rho_{\rm in}}C_{\rm port,m}
=m+mp\varepsilon\,\operatorname{Tr}(\rho_{\rm in}\Delta_{\boldsymbol\rho}),\qquad
\partial_{\rho_r}\mathbb E C_{\rm port,m}\big|_{\rho_{\rm in}\,\rm fixed}
=mp\varepsilon\,\operatorname{Tr}(\rho_{\rm in}\Delta_r)\ge0.
}\tag{15}
\]
This holds on the **same original all128 history** without the extra Golden thinning programme, without throwing out zero-momentum modes and for EVERY stationary or nonstationary \(\rho_{\rm in}\) at fixed preparation. The full reference remains a spectator, so a general correlated input has the same positive \(\Delta_r\otimes I_{\rm ref}\).

Thus the class of proposed scalar physical completions
\[
S_{\rm candidate}=S^{\rm bare\,HJR}+\kappa C_{\rm port,m}+C_{\rm fixed},
\qquad \kappa\ge0,
\tag{16}
\]
with no other field-dependent price/Info terms and the above actual fixed or truly envelope-stationary input state, **cannot** admit the original flat Einstein vacuum as a stationary solution on the all-L≥256 coframe scale box. Its true partial coframe source is bounded below by the already-certified positive flat HJR value, because (15) is nonnegative. The bare-HJR proof provides \(L^{-4}\partial_{\rho_r}S_{HJR}>4.9\times10^{-9}\) for periodic or the specified open trace geometry; this new positive-port sign theorem itself is on the periodic homogeneous complete original full128 carrier, **not** a fixed-Dirichlet interior Euler.

Even after solving the **combined** internal/preparation Euler of a genuinely additive candidate (16), the envelope derivative is the partial field derivative with internals fixed; the Rayleigh energy and the new port term each have nonnegative \(\partial_{\rho_r}\) there. Hence no positive multiple of the KNOWN PAID PORT COST restores the flat Einstein Euler on that chart. Retaining additional mandatory port ticks simply increases m, not its sign. If an alternative source has field-dependent controller/label/clock/preparation **costs or negative Info**, the theorem does NOT exclude it: that is the exact remaining Book03 source obligation, which cannot be discharged by another return-port probability alone.

**Strong synthesis:** The *original* same-history port cost already has a determined sign, and the original HJR flat bulk pressure has the SAME sign. Therefore the physical restoring source, if D0 admits one, must arise in its truly selected **nontrivial Info/reference/relative-history or genuinely additional internal price**, with a derived negative coframe first jet; it is not hidden in the previously-missing multistep Γ correction, since that correction vanishes in the flat full128 history and is O(h) in smooth periodic bulk. This does NOT identify Shannon entropy with compulsory Book03 Info or choose a fitted negative term. It is a sharp physical selection test.


## 7. NEW UV/IR EXTENSIVITY SEPARATOR ON THE ACTUAL FULL rank128 RIESZ PREPARATION

The source sign result in §6 is sharpened **without inventing another preparation**. On the original periodic flat *physically scaled* coframe \(v_r=h\nu e_r\), \(h=1/L\), the actual rank128 prepared RIGHT Gram \(I_{128}/128\) occupies the COMPLETE first positive Dirac shell: \(8\) momenta \(q=\pm\hat e_r\) times ALL16 CAR grades. Its eigenvalue is exactly
\[
\lambda_{1,L}=4\nu^2\sin^2(\pi/L)\le4\nu^2\pi^2 L^{-2}.
\tag{22}
\]
The original all128 full-history port-cost owner, evaluated on the same normalized rank128 density (or its unchanged oldRIGHT purification), gives for EVERY \(m=256L^2\) and \(\varepsilon=p^2/(64L^2)\):
\[
\boxed{\ \mathbb E C_{\rm port,m}
=m+4p^3\lambda_{1,L},\qquad
\partial_{\rho_r}\mathbb E C_{\rm port,m}\Big|_{\rho_r=1}
=4p^3\,\operatorname{Tr}(\rho_{\rm Riesz}\Delta_r)
=p^3\lambda_{1,L}=O(L^{-2}),\quad r=0,1,2,3. \ }\tag{23}
\]
Here \(\rho_r\) scales the four creation-leg **squares** separately; each of the eight original selected momenta contributes one direction, and exactly two of them are in each r, so the \(1/4\) is an exact original rank128 multiplicity ratio. The full \(\rho_{\rm Riesz}\) is held fixed in the partial source; if the actual Riesz section moves, the total source at *true complete* internal stationarity is this partial derivative by the envelope identity. These equalities also hold for arbitrary fixed Riesz-shell weights with \(0\le\partial_{\rho_r}\mathbb E C_{\rm port,m}\le4p^3\lambda_{1,L}\), although the exact \(1/4\) then changes.

The completely literal original *total nonblank output* probability is
\(e_{L}=\varepsilon\lambda_{1,L}-(\varepsilon^2/4)\lambda_{1,L}^2=O(L^{-4})\).
Expected total nonblank events over ALL \(m\) actual rounds are therefore
\(m e_L=O(L^{-2})\), **not** order one. The unchanged full-record source owner
\`A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE\` §§6,12 has the exact
conditional pointer entropy chain and the uniform strict-Julia fixed-shell mark jets. On this same low-energy shell it yields
\[
H_{\rm pointer}=O(L^{-2}\log L),\qquad
\partial_{\rho_r}H_{\rm pointer}=O(L^{-2}\log L)
\tag{24}
\]
in a uniformly bounded C1 coframe/observer chart with the specified fixed complete output labels. No "missing" exit labels or reduced-record postselection is used; the conditional 63-way mark entropy is bounded by each rare event's actual probability and controlled row jets. Equation (24) is a property of THIS pointer Shannon Info **candidate**, not an identification with the complete original Book03 operator Info. Coherent rank-birth entropy can have different C2 behavior, so do not infer a second-source bound from (24).

By contrast, the previously exact SAME normalized physical coframe full-HJR first-source certificate proves
\[
\boxed{L^{-4}\partial_{\rho_r}(H+J+R)\ge c_r>4.9\times10^{-9}
\quad\text{for EVERY}\ L\ge256,}
\tag{25}
\]
while the original star/Golden-J2 flat vacuum source is zero. At fixed full RIGHT128 preparation, the port expected Cost first source is \(O(L^{-2})\) in **TOTAL** and \(O(L^{-6})\) after dividing by \(L^4\), and this pointer entropy candidate is \(O(L^{-2}\log L)\) total, \(O(L^{-6}\log L)\) in bulk units. Neither can cancel the extensive nonzero bare-HJR pressure; the signs of the actual port Cost and HJR source are moreover both nonnegative.

**Physical discriminatory conclusion:** on the SAME 16L⁴ site/fullCAR carrier with the SAME original normalized Riesz128 input and full128 tape, the *currently derived* one-preparation original port Cost and its classical pointer Shannon candidate are **subextensive**, while the bare HJR thermal/feedback source is extensive. No multiplication by the number of outcomes 128^m is legitimate: actual normalized full-history probabilities already sum to one. Therefore a full native Book03 completion that is genuinely Einstein-stationary must supply another **bulk-extensive, field-sensitive** Info/reference/work/clock/ensemble preparation source, or change the conditional physical action through a genuinely derived nonadditive binding. Simply lengthening the already-paid rank128 tape, adding a finite fixed number of such tapes, or ignoring Γ cannot work.

This still does NOT refute D0: a compulsory per-site complete archive, a different admitted physical state/clock distribution, an explicitly proved extensive reference/Info accounting or a non-additive native operator law could alter the scaling. But this is a precise "one normalized oldRIGHT128 programme cannot pay for the bulk pressure" separator on the SAME flat physical-carrier root, not a philosophical missing-action remark.


## 8. EVEN STRONGER: the ENTIRE coherent retained original full128 tape is operationally blind to the flat low-shell scale in the continuum

The UV/IR mismatch is **not merely** a Shannon-vs-Cost normalization concern. On the same original flat periodic coframe \(v_r=h\nu\sqrt\rho\,e_r\), \(\rho\in[\rho_-,1]\) and unchanged original full rank128 Riesz-shell preparation \(|\Psi_{\rm in}\rangle\) with its **entire** oldRIGHT correlations, every one of the eight first-shell momenta has the same exact CAR16 energy
\[
\lambda_{\rho,L}=\rho\,4\nu^2\sin^2(\pi/L)\le 4\nu^2\pi^2/L^2 .
\]
The ORIGINAL **no-nonblank-output Kraus row** of each genuine full128 round is exactly \(K_{(b=0,k=0)}=B=I-\alpha\Delta\) (the original \`A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE\` §2; do not confuse this output event with the OPTIONAL Golden-thinned port mark). Since \(B\) is the same scalar \(b_{\rho,L}=1-\alpha\lambda_{\rho,L}\) on the entire original shell, the exact \(m=256L^2\) step all-blank probability is
\[
\boxed{
P_{\rho,L}(\text{every one of m labels blank})
=(1-\alpha\lambda_{\rho,L})^{2m},
\quad
P_{\rho,L}(\text{any actual nonblank})
\le2m\alpha\lambda_{\rho,L}
=4p^2\lambda_{\rho,L}
\le {16p^2\nu^2\pi^2\over L^2}.
}\tag{26}
\]
Every original port, k-label, oldRIGHT state and chronological failure is retained; no stochastic independence of actual outputs has been assumed. Equation (26) follows from a SINGLE exact complete-word Kraus amplitude \(B^m|\Psi_{\rm in}\rangle\), not from multiplying guessed probabilities after ignoring back-action.

Let \(|\mathcal V_{\rho,L}\rangle\) be the genuinely purified coherent result of composing the **original m complete full128 Stinespring rounds** on this input, with every historical register present. Let \(|{\bf blank}\rangle\otimes|\Psi_{\rm in}\rangle\) be the common identical all-blank record with unmodified initial data+oldRIGHT. Because every nonblank word is orthogonal in the record and the blank-branch amplitude is exactly \(b_{\rho,L}^{m}|\Psi_{\rm in}\rangle\),
\[
\begin{aligned}
\bigl\||\mathcal V_{\rho,L}\rangle-
 |{\bf blank}\rangle|\Psi_{\rm in}\rangle\bigr\|^2
&=(1-b_{\rho,L}^m)^2+(1-b_{\rho,L}^{2m})\\
&=2(1-b_{\rho,L}^m)
\le2m\alpha\lambda_{\rho,L}\\
&\le {8p^2\nu^2\pi^2\over L^2}.
\end{aligned}\tag{27}
\]
Thus \(\||\mathcal V_{\rho,L}\rangle-|{\bf blank}\rangle|\Psi_{\rm in}\rangle\|\le\sqrt8\,p\nu\pi/L\). For any TWO constant scales \(\rho,\rho'\) in this fixed chart, their entire normalized final **coherent record+data+oldRIGHT** density matrices have trace distance \(O(1/L)\) (and the purely classical pointer-record distributions have total variation \(O(1/L^2)\) by (26)). In particular **every** norm-bounded subsequently admitted POVM effect on THIS SAME complete quantum tape, including any interference across all recorded outcomes, has an \(O(1/L)\) difference in event probability; measuring only the orthogonal pointer tape is even less informative, \(O(1/L^2)\). No subsequent bounded test on these retained registers alone restores finite local scale sensitivity at fixed one-programme input. A physical observer which independently reads/modifies the coframe, or a new prepared high-energy/local reference, is a DIFFERENT operation and must be explicitly admitted and paid.

This is the sharpest **same-preparation quantitative obstruction** to reading the formal HJR bulk pressure as the Cost–Info response of one completed prepared Golden programme: the HJR feedback/coframe source is extensive \(+\Omega(L^4)\) even at the genuine physical flat scale, while every bounded measurement of the one original rank128 quantum execution loses all scale information as \(L\to\infty\). It does NOT follow that an action-gradient necessarily vanishes from total-variation convergence alone (a rapidly changing price can have a nonvanishing derivative), so the rigorous source mismatch remains separately certified in (23)–(25). Their combination, **both a derivative bound and a full-operational-norm bound**, makes the missing Book03 binding explicit.

**Physical consequence:** any positive Einstein closure that keeps the original entire counting-trace HJR feedback MUST derive a genuinely **bulk-extensive** native state ensemble/operation, a nontrivial charged Info/relative-reference source, or a different justified operator/action semantics. Merely applying an infinite number of abstract bounded future readouts to the *same fixed completed tape* does not change (27), whereas running many independent physically paid preparations can change the distinguishability budget. This is not a general impossibility theorem for D0 or an arbitrary gravity observer; it is a rigorous **one fullRIGHT128 prepared programme versus entire HJR UV spectral trace** separation on the original identical flat carrier.


## 9. Genuine 4D **resource lower bound**: Ω(L⁴) ORIGINAL full128 rounds required to distinguish low-shell coframe scales

Section 8 considered the owned finite clock \(m=256L²\), but the proof yields a stronger **all-clock resource theorem**. On the SAME homogeneous proper-flat carrier, fix two positive constant isotropic coframe scales \(\rho\ne\rho'\) in a bounded compact interval, the exact common original normalized fullRIGHT128 first-shell input \(|\Psi_{\rm in}\rangle\), the unchanged oldRIGHT/reference and the same original 128-output Kraus round.

On every one of the eight lowest positive momentum shells, the entire actual full16/RIGHT input has the exact \(\Delta_\rho=\rho\lambda_{1,L}I\), and the complete original **single** blank-record Kraus operator is
\(B_\rho=I-\alpha\Delta_\rho=(1-\alpha\rho\lambda_{1,L})I\).
The original nonblank effect is
\[
E_{\rm exit}(\rho)=I-B_\rho^2=
(2\alpha\rho\lambda_{1,L}-\alpha^2\rho^2\lambda_{1,L}^2)I
=O(L^{-4})I.
\tag{28}
\]

**THEOREM (arbitrary chronological depth R).** Append \(R\) of the **same full original 128-outcome rounds**, always retaining ALL data, labels, ports, other work and oldRIGHT. Let \(|V_{\rho,R}\rangle\) be the resulting FULL purified record from the fixed common input. For every integer \(R\ge1\),
\[
\boxed{
\||V_{\rho,R}\rangle-|{\bf blank}_R\rangle|\Psi_{\rm in}\rangle\|^2
=2[1-(1-\alpha\rho\lambda_{1,L})^R]
\le2R\alpha\rho\lambda_{1,L}
\le{p^2\nu^2\pi^2\over 16}\,{R\over L^4}\,
}\tag{29}
\]
using \(\lambda_{1,L}\le4\nu²\pi²/L²\) and \(\alpha=p²/(128L²)\). (The last displayed coefficient is \(2\cdot(1/128)\cdot4=1/16\).) The common all-blank branch is the exact ORIGINAL event, not a normalized success-postselected state; **all nonblank branches remain present and orthogonal** in the tape.

By triangle inequality, the two entire coherent outputs \(|V_{\rho,R}\rangle\) and \(|V_{\rho',R}\rangle\) differ in Hilbert norm by at most
\[
\frac{p\nu\pi}{4}\,(\sqrt\rho+\sqrt{\rho'})\,\frac{\sqrt R}{L^2}.
\tag{30}
\]
Consequently their trace distance and all downstream bounded measurement statistics, including globally coherent joint POVMs that read the complete oldRIGHT and full chronological tape, are \(O(\sqrt R/L²)\). If \(R_L=o(L^4)\), the trace distance tends to zero. Therefore
\[
\boxed{\quad
\text{constant limiting distinguishability by THIS full128 low-shell process}
\Longrightarrow R_L=\Omega(L^4).\quad}\tag{31}
\]
This is an information-theoretic **necessary** execution-volume bound, not an appeal to independent Bernoulli attempts; the complete quantum Stinespring isometry and its true all-blank word supply the proof. The classical pointer tape has a still sharper bound \(O(R/L^4)\) for \(R\ll L^4\). The bound survives multiple fresh SAME-shell preparations with a total of \(R\) actual rounds and no inserted high-energy/field-sensitive state reset: their common all-blank amplitude factorizes to the same scalar, and (29) uses only total clock exposure. An admitted extra active controller that moves states into high-energy shells or directly observes the coframe is a **different** field-sensitive operation and must be priced separately.

**Nontrivial synthesis with the original HJR trace:** the full thermal/feedback HJR flat coframe derivative contains an extensive contribution \(+\Omega(L^4)\), while the original normalized low-shell right128 tape at its owned \(m=256L²=o(L^4)\) clock has vanishing complete future-test distinguishability and a vanishing known port Cost first jet \(O(L^{-2})\). The same \(L^4\) that counts original four-dimensional UV modes is an unavoidable MINIMUM number of raw physical channel rounds for this specified low-shell observable to yield an \(O(1)\) distinction. This matching exponent does NOT prove the D0 dimension, physical GR, statistical sufficiency at \(R\simeq L^4\), or the actual Book03 Cost–Info functional; it supplies a quantified missing **operational ensemble/resources** gate instead of an invented cosmological counterterm.

**Single continuing physical test:** determine from Book03/G0 whether the actual compulsory physical history includes the necessary \(L^4\)-scale ensemble, a new paid high-energy probe or an operator-valued site trace/relative-comparison price; and calculate its full native Info/work source and coframe-link Euler. The oldRIGHT128 low-shell programme ALONE cannot produce a finite operational bulk Einstein source from one \(O(L^2)\) execution.
