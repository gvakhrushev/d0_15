# D0 → GR: exact amplitude-Born Book03 Bellman Info, UNIQUE 3/2 root anchor, full-history mean source, and the pressure/mean mismatch

22 October 2026. **New analytical synthesis in existing scientific Draft PR #334**, consuming two independent already-published Book03/Golden lines. No new fundamental action, presumed full128⇔N1 identity, free initial preparation, clock/oldRIGHT cost, scene heat, selected Book observer, physical root promotion, or universal GR is asserted. `GR_closed=false; compulsory_Book03_Info=false; raw216_closed=false`.

Actual prior sources:
1. `A4D_NATIVE_BOOK03_BORN_ENTROPY_BELLMAN_VERTEX_INFORMATION_WELD_2026_10_22.md`: EXACT conditional **scalar** Born+expected-Shannon Bellman rule, original no-reset 128 Kraus/positive PORT stopping and full conditional jets; its binding assumes \(P_\gamma\propto\varphi^{-S_\gamma}\).
2. `A4D_BOOK03_BORN_HALF_ENTROPY_AGGREGATION_GATE_2026_10_21.md`: original **AMPLITUDE** Book03 weight \(\varphi^{-S_\gamma}\), conditional orthogonal fine recording \(P_\gamma\propto\varphi^{-2S_\gamma}\); absolute amplitude anchor \(j=3H_\varphi/2-C\) if its **mean** is to equal counted-CQ Cost−Shannon, and the exact gap mean–pressure \(H_\varphi/2\).
3. Book03 §§03.3.0–03.3.0a and §03.10: weight semantics, action as Cost−Info and quadratic amplitude readout. **The physical Book programme has NOT been proved to satisfy the simultaneous binding premises** below.

## 1. The missing change of exponent: one theorem, both earlier owner coefficients

Take ONE genuinely specified finite positive-support prefix tree of FULLY retained paid fine histories \(\Gamma\), with true (possibly correlated, no-reset) conditional BORN laws \(P_y(b|u)>0\), true already declared primitive charges \(c_y(u,b)\), all supplied oldRIGHT/clock/factory labels included, and complete fine leaf probabilities \(P_y(\gamma)=\prod_{u\to ub\in\gamma}P_y(b|u)\).

For clarity separate THREE distinct mathematical objects: positive *amplitude* \(a_\gamma=\varphi^{-S_\gamma}\); positive normalized **Born probability** \(P_\gamma\); and original mean history price \(\mathbb E_P S_\gamma\). They coincide under no generic identification.

For a finite constant \(\nu>0\), define the explicitly CONDITIONAL source binding
\[
\boxed{\quad
(\mathrm{BORN}_\nu):\
P_y(\gamma)=\frac{\varphi^{-\nu S_y(\gamma)}}{Z_{\nu,y}},
\quad Z_{\nu,y}=\sum_{\gamma\in\Gamma}\varphi^{-\nu S_y(\gamma)},\
S_\gamma=\sum_{u\to ub\in\gamma}[c_y(u,b)-I_y(u,b)].
\quad}\tag{1}
\]
The previously owned scalar interpretation is \(\nu=1\). The original orthogonal-amplitude Born reading is **\(\nu=2\)**, NOT \(\nu=1\). This \(\nu=2\) identification needs an actual isometry from original phase-bearing memory-valued paths to **orthogonally distinguishable FULL fine pointer leaves** and no unaccounted interference cross terms; a generic coherent memory sum does NOT supply (1).

Independently impose precisely the same previous **conditional local gain** premise
\[
\boxed{(\mathrm{GAIN}):\
\sum_bP_y(b|u)I_y(u,b)
=h_y(u):=-\sum_bP_y(b|u)\log_\varphi P_y(b|u).
}\tag{2}
\]
No claim is made that these two equations already follow from M1/G0 or that every realised Info must be nonnegative.

## 2. THEOREM A — UNIQUE complete amplitude-Born/expected-Shannon Book information, every finite tree and all jets

For ANY \(\nu>0\), define a backward potential \(f_{\nu,y}(\mathrm{leaf})=0\) and at every other node
\[
\boxed{
f_{\nu,y}(u)=\left(1+\frac1\nu\right)h_y(u)
-\bar c_y(u)+\sum_bP_y(b|u)f_{\nu,y}(ub),\
\bar c_y(u)=\sum_bP_y(b|u)c_y(u,b).
}\tag{3}
\]
Then define the realised, branch-labelled, generally SIGNED information
\[
\boxed{
I_{\nu,y}(u,b)=c_y(u,b)+\frac1\nu\log_\varphi P_y(b|u)
+f_{\nu,y}(u)-f_{\nu,y}(ub).
}\tag{4}
\]

**Claim:** (3)–(4) are the UNIQUE real solution of (1)+(2) on the actual finite positive tree, including every individual output and future continuation. No independent Info table, fit to the desired field action, external entropy coefficient or new Golden primitive is used.

**Exact proof.** Along any leaf \(\gamma\), (4) telescopes:
\[
\boxed{
S_y(\gamma)=-\frac1\nu\log_\varphi P_y(\gamma)
-f_{\nu,y}(\emptyset),\
\varphi^{-\nu S_\gamma}
=\varphi^{\nu f_{\nu,y}(\emptyset)}P_y(\gamma).
}\tag{5}
\]
Thus \((\mathrm{BORN}_\nu)\) holds with the UNIQUE absolute normalization \(Z_{\nu,y}=\varphi^{\nu f_{\nu,y}(\emptyset)}\). The conditional mean of (4) is
\(\bar c_y-h_y/\nu+f_\nu-\sum P f_\nu(\mathrm{child})=h_y\) by (3), proving (GAIN). Conversely (1) fixes all completed root-to-leaf action differences; on a tree every edge deviation from (4) with zero total path sum is a unique node coboundary with f(leaf)=0. (2) then gives the same backward recurrence, proving uniqueness and excluding an independent root normalization degree of freedom **inside this specified two-premise class**.

Shannon chain rule on the ENTIRE actual paid tree gives
\[
\boxed{
\begin{aligned}
f_{\nu,y}(\emptyset)&=\left(1+\frac1\nu\right)H_\varphi(P_y)-C_y,\\
\log_\varphi Z_{\nu,y}&=(\nu+1)H_\varphi(P_y)-\nu C_y,\\
\mathbb E_{P_y}\sum_{u\to ub\in\gamma}I_{\nu,y}(u,b)
 &=H_\varphi(P_y),\\
\mathbb E_{P_y}S_y(\gamma)
 &=\boxed{C_y-H_\varphi(P_y)}\qquad\text{for EVERY }\nu>0,
\end{aligned}
}\tag{6}
\]
where \(C_y=\mathbb E_{P_y}\sum c_y\) includes EVERY declared true primitive charge. Every expression is one exact scalar function, not merely a root/first-source match.

On a smooth positive-support actual field/independent-input chart, ALL 42 field and genuine upstream first-source rows follow by honest differentiation:
\[
\boxed{
\begin{aligned}
Df_\nu(u)
&=\left(1+\frac1\nu\right)Dh(u)-D\bar c(u)
  +\sum_b[DP(b|u)\,f_\nu(ub)+P(b|u)\,Df_\nu(ub)],\\
DI_\nu(u,b)
&=Dc(u,b)+\frac{DP(b|u)}{\nu\ln\varphi\,P(b|u)}
  +Df_\nu(u)-Df_\nu(ub),\\
D f_\nu(\emptyset)
&=\left(1+\frac1\nu\right)D H_\varphi(P)-DC,\\
D\mathbb E S
&=DC-DH_\varphi(P).
\end{aligned}
}\tag{7}
\]
These equations include the true moving quantum preparation and all conditional Kraus jets PROVIDED the actual P and c input to this theorem are those of the same native programme. Singular zero-support strata require a separate limit; no division by a born-zero branch is permitted.

## 3. THEOREM B — the ORIGINAL \(\nu=2\) amplitude theorem fixes \(j=3H/2-C\) without an external anchor

With the Book03 **positive REAL amplitude** \(a_\gamma=\varphi^{-S_\gamma}\) and ORTHOGONALLY retained fine leaf amplitudes, Born's quadratic rule is \(\nu=2\). Equations (3)–(7) specialize to
\[
\boxed{
\begin{aligned}
f_2(u)&=\tfrac32h(u)-\bar c(u)+\sum_bP(b|u)f_2(ub),\\
I_2(u,b)&=c(u,b)+\tfrac12\log_\varphi P(b|u)+f_2(u)-f_2(ub),\\
j_2&=\log_\varphi\sqrt{Z_2}
     =f_2(\emptyset)
     =\boxed{\tfrac32H_\varphi(P)-C},\\
Z_2&=\varphi^{3H_\varphi(P)-2C}.
\end{aligned}}\tag{8}
\]
**New explicit composition:** the formerly separately exposed necessary condition \(j=3H_\varphi/2-C\) in the OLD half-entropy aggregation theorem is now **the unique derived absolute amplitude normalization of one complete BORN2+GAIN Bellman tree**, not an independently selected source-fitted `j`. It reproduces the original FULL measured-code mean Price−Info \(C-H\) **on every positive open chart with all real source jets**. It does not establish that the compulsory physical Book03 operator realizes this entire orthogonal tree or selects that mean as its own finite Euler action.

### IMPORTANT: mean action and amplitude partition pressure are DIFFERENT objects

Let \(P_{\mathrm{amp},\nu}=-\nu^{-1}\log_\varphi Z_\nu=-f_\nu(\emptyset)\). Then (6) implies the exact universal sourced difference
\[
\boxed{
\mathbb E_P S_\gamma
=P_{\mathrm{amp},\nu}+\frac1\nu H_\varphi(P),\quad
D\mathbb E_P S-DP_{\mathrm{amp},\nu}
=\frac1\nu DH_\varphi(P).
}\tag{9}
\]
For real positive Book amplitudes \(\nu=2\) this is the OWNED half-entropy law. In particular:
\[
\boxed{P_{\mathrm{amp},2}=C-\tfrac32H_\varphi(P),\quad
\mathbb E_P S=C-H_\varphi(P).}\tag{10}
\]
A proposed GR proof that replaces the physical Book Euler with the negative log *amplitude normalizer* while previously using the counted-CQ **mean** action drops the generally NONZERO \(\tfrac12 DH\) first source. This is an exact source-type obstruction, not permission to insert \(+\tfrac12H\) as an unpaid counterterm: the correct operator/action/aggregation must be physically established.

## 4. ORIGINAL exact Golden nonblank pair: both previously independent Info differences follow from one formula

For the already real native \(j>0\) paired Kraus PORT law
\[
p=\varphi^{-1},\quad P=(p^2,p),\quad
(c_0,c_1)=(1,2),\quad
H_\varphi(P)=2-p,\quad C=1+p,
\]
the same tree gives
\[
\boxed{I_\nu(1)-I_\nu(0)=
(c_1-c_0)+\nu^{-1}\log_\varphi(P_1/P_0)
=1+\frac1\nu.}\tag{11}
\]
Thus **scalar BORN1 gives 2** (the newer whole-tree Bellman owner);
**genuine quadratic amplitude BORN2 gives 3/2**
(the OLDER Book amplitude-binding owner). These are NOT rival predictions of one physically selected process: they arise from two different declared probability/weight identifications. The two independent results are now mathematically reconciled.

At BORN2 the exact nonblank pair has
\[
\begin{split}
j_2&=\tfrac32(2-p)-(1+p)
       =2-\tfrac52p=0.454915028125\ldots,\\
I_2(0)&=j_2,\qquad I_2(1)=\tfrac32+j_2
       =1.954915028125\ldots,
\end{split}\tag{12}
\]
both positive and no new fitted coefficient. For the ORIGINAL scarce N1 binary click \(P=(1-r,r)\), c=(1,2), the SAME exact tree instead yields
\[
\boxed{I_{2,1}(r)=1-r+\tfrac32h_\varphi(r)
+\tfrac12\log_\varphi r.}\tag{13}
\]
At original \(r_{\rm ref}\simeq1.8512395784882\cdot10^{-6}\),
\(I_{2,1}\simeq-12.71493522627<0\), so the original physical
**nonnegative realised per-edge Info** interpretation is STILL
incompatible with simultaneous BORN2+GAIN on that actual rare report.
An expected positive Shannon gain and a signed realised information
counterterm are mathematically different. The amplitude correction
does not wash away the genuine sign/physical-admission gate.

## 5. Actual original FULL128 nonreset implementation target

The prior whole-tree Bellman owner already supplies the genuine ORIGINAL 128-Kraus normalised conditional \(P(\alpha|u)\), original moving DATA/oldRIGHT and the strictly positive matched PORT effect bounds for the NO-RESET first-return future. Its \(\nu=1\) contraction proof does not use the value 2 multiplying \(h\); change its stage payoff to
\[
g_\nu(X)=\left(1+\frac1\nu\right)H_\varphi(q(X))
-\sum_{\alpha=0}^{127}q_\alpha(X)c_\alpha,\qquad
q_\alpha(X)=\operatorname{Tr}K_\alpha X K_\alpha^\dagger,
\tag{14}
\]
and define, after true first anchor a,
\[
\boxed{
f_{a,\nu}(X)=g_\nu(X)+
\sum_{\alpha:\,\alpha\bmod 2\ne a}
q_\alpha(X)f_{a,\nu}(X_\alpha),\quad
X_\alpha=K_\alpha X K_\alpha^\dagger/q_\alpha(X).
}\tag{15}
\]
If the prior original positive matching effect satisfies \(E_a\succeq\eta_a I,\eta_a>0\), the true continuation operator still contracts the sup norm by \(\le1-\eta_a\). Thus (15) has a **unique bounded amplitude-Born \(\nu=2\) predictive solution** on this original specified quantum stopping task, no iid reset or new finite HMM catalogue. Its continuation value/entire first-source are not automatically the Book03 feedback \(J=-\log\det(I-\zeta F)\), and the physical code and preparations must be fully paid. Derivative convergence requires the prior genuine Kraus C1/tail estimates, not just value contraction.

**Numerical exact-probability *input consumption*, not fresh full128 replay.** The prior *literal two-round full128 CAR16 partial PORT-ledger* owner reports \(H_\varphi(P_{\alpha\beta})\simeq0.5701407300473663\) and \(C_{\rm port,2}\simeq2.0260945042476832\). Applying the rigorous identities here (not asserting those rounded values are certified) yields
\[
j_2\simeq-1.170883409176634,\quad
Z_2\simeq0.324040787254856,\quad
C-H\simeq1.455953774200317,\quad
-\tfrac12\log_\varphi Z_2\simeq1.170883409176634,
\]
with exact difference \(H/2\simeq0.285070365023683\). This preserves the true sequential fine history law but is not a NEW 128×128 numerical source run or original SCENE Book admission.

## 6. EXACT scope and physical next gate

**Mathematically CLOSED within (BORN2)+(GAIN) on any supplied positive complete orthogonal recorded tree:**
a unique per-edge information allocation, unique future Bellman potential and *absolute amplitude scalar normalization* (8), correct full-history Cost−Info MEAN source \(DC-DH\) with all field/input jets, exact pressure-versus-mean correction (9), and a corresponding bounded no-reset CAR16 quantum predictive-value fixed point under the pre-existing positive matching-effect hypothesis.

**NOT closed physically:** whether original Book03's phase/memory-valued histories have precisely this **orthogonal positive-amplitude** Born interpretation; whether its Info gain is the conditional local entropy **rather than** pathwise surprisal or a distinct quantum conditional information; whether signed realised gains are M1-admissible; whether the predictive f is actually implemented and PAID; whether compulsory SCENE \(\Delta_N(V)\), its \(P_N\), heat and \(-\log\det\) action aggregate by this mean rather than amplitude pressure; and actual full original all42 field/input/clock equations and uniform physical GR/raw216 refinement.

**One immediately decisive physical comparison:** evaluate the ACTUAL full Book03 \(H+J+R\), complete oldRIGHT/controller/clock/Info action and its 42 + independent-input differential on ONE actually common original history; check whether its entropy source matches \(DC-DH\), \(DC-\tfrac32 DH\), or neither. The EXACT \(\tfrac12 DH\) gap is already testable using the old native moving query and 128-Kraus record, not a new rank scan or Einstein coefficient fit. Only a real SAME-EXECUTION source identity and complete physical selection can promote \(GR\).

Bounded replay: `sources/d0_book_amplitude_bellman_2026-10-22/check_amplitude_bellman.py`. Neither Lean nor large historical/physical full128 suites is asserted freshly rerun.
