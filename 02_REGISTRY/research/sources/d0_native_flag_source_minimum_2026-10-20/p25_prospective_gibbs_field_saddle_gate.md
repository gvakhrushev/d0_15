# P25 physical closure gate: history minimum vs Einstein field saddle

20 October 2026. Research continuation in existing #334 / native-programme-v1.
Primary inputs: original finite **unimodular** P25 shared-role witness
\`02_REGISTRY/research/A4D_P25_NATIVE_COST_FLOOR_PSD_MIXED_PALATINI_VACUUM_NO_GO_2026_10_20.md\` §§1–4 on current branch, and accepted architecture
\`02_REGISTRY/research/MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md\`, prospective selection and current GR route.
Mathematical result only: no new price, G0 actuator, physical source, stationarity solution, TASK or GR closure.

## 1. A complete smooth minimum cannot reproduce the original P25 off-shell 2-jet

The exact P25 original 16-site, 64 **shared** proper-link, 96-face finite geometry (not an invented test action) restricts to a genuine unimodular coframe variable \(a>0\) and a single proper shared link \(t\), with
\[
S_\star(a,t)=(1-a)\sin t.
\]
At the genuine common flat root \(a=1,t=0\), writing \(x=a-1\),
\[
\nabla S_\star(0)=0,\qquad
D^2S_\star(0)=
\begin{pmatrix}0&-1\\-1&0\end{pmatrix}
=:H_\star,\qquad
\operatorname{spec}H_\star=\{-1,+1\}.
\tag{1}
\]

**A stronger universal minimum obstruction, independent of a Cost-floor model.**
Let \(\mathcal S(x,t,z)\) be any real \(C^2\) *complete* native price on an open chart of **actually independently admitted** variations \((x,t,z)\), including all hidden programme/preparation/clock/work variables \(z\). If \((0,0,z_0)\) is a local minimum, its full Hessian is PSD; in particular its principal \((x,t)\)-compression is PSD. If a \(C^2\) internal minimizer \(z=z(x,t)\) exists locally and the effective source satisfies
\[
D_{x,t}\mathcal S_{\rm eff}(x,t)
=c\,D_{x,t}S_\star(x,t)+o(\sqrt{x^2+t^2})
\quad(c\ne0),
\tag{2}
\]
then \(D^2\mathcal S_{\rm eff}(0)=cH_\star\), which is indefinite and impossible at an effective local minimum. No nondegenerate internal Hessian is needed: a local minimum of the full price plus an actually minimizing internal section implies a local minimum of the resulting effective price. Where the usual \(H_{zz}>0\) inverse is present, the reduced Schur \(H_{\rm eff}=H_{xx}-H_{xz}H_{zz}^{-1}H_{zx}\succeq0\) yields the same contradiction.

**This does not disprove D0→GR.** Prospective minimization **over possible histories at a fixed external field** and stationarity of the resulting field action are different variations. Einstein/Palatini stationary action is allowed to have physical/gauge-quotiented saddle directions. The exact obstruction prohibits the stronger claim that the *same two unrestricted geometric directions* minimize the complete action at this root **and** reproduce its full P25 2-jet. It does not prohibit matching on-shell zero sets only, matching via a noninvertible constraint quotient, a genuine stationary (not minimizing) hidden \(z\)-Schur, or a different curved branch.

This sharpens the accepted negative-HJR minimum gate: a field Hessian saddle **cannot** be repaired merely by insisting that the D0 prospective history law is a minimum. Those are different minimizations and must be typed separately in the parent.

## 2. Exact finite Gibbs/MDL curvature identity for the *existing* Book history weights

Consider any finite complete positive set of original history weights
\[
Z(y)=\sum_{\gamma}c_\gamma e^{-\beta s_\gamma(y)},\qquad
F(y)=-\beta^{-1}\ln Z(y),\qquad
\pi_\gamma(y)=c_\gamma e^{-\beta s_\gamma(y)}/Z(y),
\quad\beta=\ln\varphi>0,
\]
with **field-independent** \(c_\gamma>0\). Field-dependent positive attempt factors, where truly present, must be absorbed in the score \(\tilde s_\gamma=s_\gamma-\beta^{-1}\ln c_\gamma(y)\) before applying the formula. Complete failed histories remain in the sum. By direct differentiation,
\[
\boxed{\
DF=\mathbb E_\pi Ds,\qquad
D^2F=\mathbb E_\pi D^2s
-\beta\,\operatorname{Cov}_\pi(Ds,Ds).
\ }\tag{3}
\]
This is the existing finite Gibbs/relative-entropy identity applied to the P25 source, NOT a newly postulated Cost or an identification of the required full Book03 price with \(F\).

The probability law \(\pi(y)\) is at each fixed \(y\) the **unique strict minimizer** over all normalized probability vectors \(q\) of
\[
\mathcal V_y(q)
=\sum_\gamma q_\gamma\,\big(s_\gamma(y)-\beta^{-1}\ln c_\gamma\big)
+\beta^{-1}\sum_\gamma q_\gamma\ln q_\gamma,
\]
since \(\mathcal V_y(q)-F(y)=\beta^{-1}D_{\rm KL}(q\|\pi(y))\ge0\).
The strict minimum is in \(q\); equation (3) permits an **indefinite** Hessian in external \(y\) because of the *negative score-covariance* term. The conditional-current all327 owner and prospective Bellman owner already supply related general variational context; (3) is consumed here only for an exact **P25 mixed-source necessary condition**. Neither unique \(q\)-selection nor finite Gibbs weights alone establish an actual D0 physical programme.

## 3. A necessary physical coframe-score variance for the P25 Einstein mixed source

At the P25 flat root, let \(y=(x,t)\) and denote
\[
A=\mathbb E_\pi D^2s,\quad
C=\operatorname{Cov}_\pi(Ds,Ds),\quad
H=A-\beta C.
\]
Suppose the entire proposed native scalar free-energy source matches \(c S_\star\) through the Hessian at the same root with \(c\ne0\), and **assume** each complete effective history score \(s_\gamma\) has PSD Hessian there (hence \(A\succeq0\)). Then
\[
H_{xx}=0,\ H_{xt}=-c
\quad\Longrightarrow\quad
\boxed{A_{xx}=\beta C_{xx}>0.}\tag{4}
\]
Proof: equality with zero permits \(A_{xx}=C_{xx}=0\) initially. But \(A\succeq0\) then forces \(A_{xt}=0\), and \(C\succeq0\) forces \(C_{xt}=0\), contradicting \(H_{xt}=-c\ne0\). Therefore BOTH the mean positive \(x\)-curvature and the **nonzero variation across actual histories of the coframe-score first derivative** are necessary. Quantitatively,
\[
\boxed{(A_{xt}+c)^2\le A_{xx}\,\beta\,C_{tt}.}\tag{5}
\]
This follows from \(C_{xt}=(A_{xt}+c)/\beta\) and Cauchy–Schwarz for the covariance matrix.

**Decisive interpretation.** If the original Golden attempt law and the **complete paid history scores** are coframe-blind to first order on the unimodular P25 witness, then \(C_{xx}=0\) and the required \((0,-c)\) mixed response is impossible for any locally convex complete history-score family—regardless of positive readout distinguishability. A nonzero first derivative of some branch probability or conditional future state is NOT alone enough: \(\partial_xs_\gamma\) must have a **nonzero interhistory variance in the actual selected Cost−Info accounting**. This extends the old saturated-Cost/coframe-blind-Info cone test into an explicit score-fluctuation gate for interior Costs. If actual scores are nonconvex, or an algebra-valued complex amplitude does not admit this scalar positive Gibbs representation, hypotheses fail and that different native mechanism must be treated directly, not labeled excluded.

## 4. Constructive algebraic countercontrol: history minimum CAN coexist with the exact P25 saddle

To prove this separation is real rather than semantic, take the **same Golden two-branch weights** \(p=\varphi^{-1}\), \(g=p^2\), \(p+g=1\), and \(\beta=\ln\varphi\).
Use \(x=a-1\), \(t\) and
\[
\alpha=(\beta p g)^{-1/2},\qquad
s_G(x,t)=3+p\alpha(x+t)+\tfrac12(x^2+t^2),\quad
s_B(x,t)=2-g\alpha(x+t)+\tfrac12(x^2+t^2).
\]
Their raw base weights are \(g p\) and \(p^2\), i.e. have normalized probabilities \(\pi_G=g,\pi_B=p\) (the common +1 in both scores is a pure baseline expense), and every score has **positive definite** field Hessian \(I_2\); locally both composite scores exceed one (this is **not** a proof that a decomposition into original primitive edge Costs and vertex Info has been admitted). The mean score gradient vanishes:
\[
g(p\alpha,p\alpha)+p(-g\alpha,-g\alpha)=0.
\]
The score covariance is *exactly*
\[
\beta C
=\beta pg\alpha^2\begin{pmatrix}1&1\\1&1\end{pmatrix}
=\begin{pmatrix}1&1\\1&1\end{pmatrix}.
\]
Consequently the **same finite Gibbs free energy** has at its stationary root
\[
\boxed{
D^2F(0)=I_2-
\begin{pmatrix}1&1\\1&1\end{pmatrix}
=\begin{pmatrix}0&-1\\-1&0\end{pmatrix}
=H_\star.
}\tag{6}
\]
Meanwhile \(\mathcal V_y(q)\) is strictly convex in the history-distribution variable, with the **unique** minimizer \(q=\pi(y)\) for every fixed \(y\). Thus positive microscopic field curvature and unique prospective statistical minimum **do not force** a positive macroscopic field Hessian.

**Crucial scientific scope.** The explicit coefficients \(\alpha\) and individual slopes in this two-score witness are engineered to demonstrate **logical compatibility** with P25; they are NOT derived from G0, 718 edges, full128, allowed history operations, observer/source or the original Book03 compulsory price. No Einstein action is claimed obtained from a native execution. The existence of a formal two-branch realization changes the theorem-search strategy (stop demanding field minima); it cannot fill \`constitutive\`, \`native_sector\` or \`positive_gr\`.

## 4a. Negative-index capacity bound: how many genuine history-score directions are needed?

A new useful consequence of (3) is the **exact finite negative-inertia bound** when \(A\succeq0\):
\[
\boxed{\quad n_-(D^2F)\le\operatorname{rank} C
\le\dim\operatorname{span}\{Ds_\gamma-\mathbb E_\pi Ds\}
\le\#\{\text{distinct history-score first jets}\}-1.\quad}\tag{7}
\]
Proof: if a negative-definite subspace had dimension \(>\operatorname{rank} C\), it would meet \(\ker C\) nontrivially, where \(v^THv=v^TAv\ge0\), contradiction. The rank bounds follow from the centered finite vector Gram representation of covariance.

For a scalar Book candidate in which every actual one of the original 8440 closed histories has a first score jet determined **solely** by its n=2 or n=3 clock class, the covariance has rank at most **one**, irrespective of 8440 path count, different coframe dependence or the original stage multiplicities. Such a reduction can never supply **more than one negative physical field direction** if its averaged conditional Hessian is PSD. Thus multiplying the number of histories without increasing their independent paid field-sensitive score jets does **not** solve higher-dimensional Einstein Hessian matching. The present P25 two-dimensional test has exactly one negative direction and therefore does not itself violate this rank-one bound; testing the larger original full metric/link Hessian's *already-owned* gauge-quotiented negative index is a named future application, not an assertion that it has been calculated here.

This is an exact **source-capacity** statement; it does not equate the number of outcome labels or the 24 rank of retained conditional quantum states with the number of genuinely distinct **physical paid score jets**. In particular, a full128 detector can be informationally complete on a tangent space while its proposed scalar Cost−Info pays only one effective field-sensitive score direction.


## 4b. DECISIVE ORIGINAL-24 CARTAN TEST: at least TWELVE independent paid score-fluctuation directions

The original, independently derived finite Lorentz-star Cartan owner
\`02_REGISTRY/gr_assembly/sources/d0_book_triangle_odds_2026-10-19/original_palatinistar_hessian_owner.md\`,
§2, on accepted main \`0f41beb04a1d19df62dc5097fa89a0a599467506\`, contains a stronger **exact original-action** input. At the original flat coframe and for the 24 homogeneous proper-link coefficients \(\omega_{r,ij}\), the original six-based-face quadratic action has symmetric Hessian \(M\) satisfying
\[
\boxed{\operatorname{rank}M=24,\quad\det M=256,\quad
\operatorname{spec}M=\{2^{[4]},(-2)^{[4]},1^{[8]},(-1)^{[8]}\}.}\tag{8}
\]
In particular \(n_-(M)=n_+(M)=12\). Its fixed-\(h\) field-source Jacobian is \(h^3M\), so multiplying by any nonzero physical normalization and positive power of \(h\) does not change this \((12,12)\) inertia.

**Native scalar-source capacity theorem.**
Suppose on THIS SAME 24-component original homogeneous-Lorentz chart a proposed scalar complete Book history law really has a positive scalar Gibbs representation (3), with its genuine source/normalizer and no omitted \(U\)-dependent coefficients, and let \(A=\mathbb E_\pi D_\omega^2s_\gamma\succeq0\) at the flat point. If it reproduces the original entire 24-link source Hessian to second order,
\[
D_\omega^2 F(0)=c M \quad\text{for some }c\ne0
\]
(with the actual nonzero lattice factors absorbed in \(c\)), then
\[
\boxed{\operatorname{rank}\operatorname{Cov}_\pi(D_\omega s_\gamma)
\ge12,\qquad
\#\{\text{distinct complete paid first-score jets}\}\ge13.}\tag{9}
\]
Proof: \(cM\) has 12 negative eigenvalues for EITHER sign of \(c\); the inertia lemma (7) bounds this number by the covariance rank. The covariance of \(r\) distinct centered history-gradient vectors has rank at most \(r-1\).

**An exact new class NO-GO, without a new spectrum run:** If the original 8440 complete history scores depend on the fields through only their two length/clock classes \(n=2,3\) at first order—regardless of arbitrary \(C^2\) nonlinear field dependence at higher order—and if the average single-history second source \(A\succeq0\), then \(\operatorname{rank} C\le1\). Such a selected scalar law CANNOT reproduce the original 24-component Cartan Hessian (8) for any nonzero normalization: \(1<12\). The same conclusion holds whenever the actual first-score-jet span has rank \(\le11\).

This is stronger than merely noting that one pointer is field-blind or matching one nonzero commutator: matching 24 independent *first-source rows* near the root requires the full Jacobian, which carries twelve negative directions. The 8440 history COUNT, all327 scalar current theorem, full128 *quantum-state* tangent rank24 and 128 pointer labels are not substitutes for twelve linearly independent **paid score fluctuations**. If the complete physical Info/clock/work has enough actual independent first jets, or the native action is algebra-valued/noncommutative, or the average microscopic Hessian \(A\) is indefinite, the theorem does not exclude it. No new imposed selector, coefficient or Einstein tensor is inferred.

**Immediate execution gate:** on the SAME original 24-link chart, compute the actual 8440 (or actually different native complete) paid score-jet *Gram/covariance matrix*, INCLUDING preparations, clock, normalization, controller and oldRIGHT charges. First check whether its **exact rank is at least 12**; this is an inexpensive KILL-FIRST discriminator. Only if it passes should one compare all source coefficients and physical Ward/GR refinement. Where the true complete price is operator-valued, derive an operator-source counterpart rather than treating classical covariance as mandatory. This result reuses the already-owned exact original Cartan spectrum; it is NOT a replay or physical admission of the proposed scalar source.


## 5. The one original physical calculation that decides the remaining hypothesis

Reuse original P25 e(a),U(t) on the **actual admitted programme** and actually paid complete original G0/Book03 history, *not* a new tester. Before freezing preparation/internal modes, compute
\[
\partial_x s_\gamma(0),\quad
\partial_t s_\gamma(0),\quad
D^2s_\gamma(0),\quad
\pi_\gamma(0)
\]
for **all paid full-history outcomes** (including failures, oldRIGHT, real clocks/work, and an observed-only vs coherent-record normalization as appropriate). If that execution really has a positive scalar Gibbs reduction with the stated regularity, evaluate the one exact tensor
\[
A-\beta C
\]
and compare the \((xx,xt)\) entries with the independently pinned P25 target \((0,-c)\) under an **already derived** normalization \(c\). Do not choose \(c\) by matching the output.

- If history coframe-score dispersion is zero and all conditional history Hessians PSD, the whole proposed scalar route fails this necessary mixed-source test.
- If it is nonzero, the exact equality (4) and quantitative constraint (5) are a test, **not** a sufficient Einstein proof; next compare all original 16+24 rows, observer, CAR matter, source Ward and nonlinear uniform refinement.
- If the native price is genuinely algebra-valued/noncommutative with no proved positive scalar reduction, derive its own operator first/second source. Do not import Gibbs covariance as a physical identity.
- If selecting actual histories does not mean minimizing over (x,t), retain the stationary Einstein saddle rather than trying to add a positive stabilizer or forbidden field constraint.

This is the smallest parent proof cut: **complete actual history-source covariance (or actual operator analog) on the true P25 tangent**, while preserving the physical distinction between distribution selection and field variation. No new Bloch census, decoder, independent continuum action or strengthened claim status. \`GR_closed=false\`, raw216 open.

