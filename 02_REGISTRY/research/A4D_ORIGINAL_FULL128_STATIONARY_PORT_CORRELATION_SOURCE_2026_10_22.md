# ORIGINAL CAR16/full128: stationary Golden-port pair has strictly positive memory information and a nonzero native first source

22 October 2026 · EXISTING Draft PR #334 / EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE. **New exact finite operator theorem on the ACTUAL original 128-Kraus CAR16 channel**, not a fresh Markov proxy, detector, action, fitted Info, new physics/GR claim, or reset programme. Scientific inputs are the unchanged original 128-Kraus constructor and the existing exact inverse-square stationary-preparation owner. This result resolves a narrower missing native premise: the source of consecutive coarse PORT information cannot be calculated from one-step Born statistics as if the original DATA were freshly reset. GR_closed=false.

## 1. Exact original sequential instrument and its two physical port classes

Use the same native full128 Walsh/Julia/Golden Kraus matrices \(K_j(y)\), \(j=0,\dots,127\), retaining ALL 128 labels and the oldRIGHT/reference. The original port is the literal parity \(b(j)=j\bmod2\), so the two coarse CP maps are
\[
\mathcal I_b(X)=\sum_{j:\,j\bmod2=b}K_j X K_j^\dagger,\qquad
\Phi=\mathcal I_0+\mathcal I_1 .
\]
**Only for a coarse readout calculation** do we sum over the fine labels; the actual retained fine tape is not physically erased.

Consume the exact original native preparation theorem's notation
\[
\Delta=D^2>0,\quad \mathcal T(I)=I,\quad
\operatorname{Tr}\mathcal T(X)=\operatorname{Tr}X,\quad
\Phi(\rho)=\rho+\epsilon
 [\mathcal T(D\rho D)-\{\Delta,\rho\}/2],
\]
with original \(\epsilon=4p^2\) in the L4 Fourier/A-units and \(p=\varphi^{-1}\).
The **unchanged** port-one CP map, read directly from the original marked-adjoint identity \(\Phi_t^*=\mathrm{Id}+\epsilon\{\eta D\mathcal T^*(\cdot)D-\{\Delta,\cdot\}/2\}\), \(\eta=p^2+p e^{-t}\), is
\[
\boxed{\mathcal I_1(\rho)=c\,\mathcal T(D\rho D),
\qquad c=p\epsilon=4p^3,\qquad
\mathcal I_1^*(I)=c\Delta.} \tag{1}
\]
No independent branch charge has been assigned: the actual port charge is \(1+b\), as in the original native paid-port owner.

On the exact regular native stationary preparation
\[
\rho_*=\Delta^{-1}/Z,\qquad Z=\operatorname{Tr}\Delta^{-1},
\]
one has \(D\rho_*D=I/Z\), and unitality of the **ACTUAL recycling map** gives
\[
\boxed{\mathcal I_1(\rho_*)=\frac cZ I,\quad
q:=\Pr_*(b=1)=c\frac dZ,\quad
\rho_{*|b=1}=\frac{I}{d}.} \tag{2}
\]
This is a one-event exact *conditional maximally mixed update from the stationary state*, not a claim that all later rounds are iid or that the fine full128 work is reset. A subsequent port-one event has probability \(c\mu\) given this update, where \(\mu=\operatorname{Tr}\Delta/d\). The stationary one-port probability is \(q=ch\), where \(h=d/Z\) is the harmonic spectral mean.

## 2. New universal original two-tick correlation theorem, independent of the details of recycling

Both genuine chronological rounds use the same original instrument on the PREVIOUS DATA OUTPUT, without an inserted blank/reset. Put
\[
\mu=\frac{\operatorname{Tr}\Delta}{d},\qquad
h=\frac d{\operatorname{Tr}\Delta^{-1}},\qquad q=ch.
\]
Trace preservation of \(\mathcal T\) and (2) give the **exact** joint port-one probability
\[
\Pr_*(1,1)=\operatorname{Tr}\mathcal I_1(\mathcal I_1(\rho_*))
=\frac{c^2}{Z}\operatorname{Tr}\Delta=c^2h\mu.
\]
Both time marginals equal \(q\) by stationarity. Thus the ENTIRE normalized two-port distribution, not only a selected probability, is
\[
\boxed{
\begin{array}{c|cc}
 & b_2=0 & b_2=1\\\hline
b_1=0 &(1-q)^2+\delta&q(1-q)-\delta\\
b_1=1 &q(1-q)-\delta&q^2+\delta
\end{array},
\qquad
\delta=c^2h(\mu-h). }\tag{3}
\]
Every full128 fine Kraus branch is summed once in this genuine observational marginal, and no extra Markov approximation is made. By the arithmetic/harmonic Cauchy–Schwarz inequality
\[
(\operatorname{Tr}\Delta)(\operatorname{Tr}\Delta^{-1})\ge d^2,
\]
with equality iff \(\Delta\) is scalar. Therefore
\[
\boxed{\delta>0\quad\Longleftrightarrow\quad
\Delta\text{ is nonscalar on the regular stationary carrier}.}\tag{4}
\]
This is an operational **two-native-port witness of native spectral nonuniformity**. In particular an original nonscalar inverse-square stationary state cannot be represented by iid consecutive port records, even though its marginal is stationary, its reversal law holds and a separate first-match occupation theorem gives an exact mean count.

For clarity, (2) is not full dynamical regeneration: starting from \(I/d\) the NEXT conditioned port-one state is proportional to \(\mathcal T(\Delta)\), not generally \(I/d\). No iid assumption or quantum memory deletion follows from a single uniform conditional update.

## 3. Genuine original L4 CAR16 fixture: exact rational covariance and field source

Fix precisely the already-owned original Fourier phase word \((i,i,-1,-i)\), \(\nu=3/5\), the real proper role-1 boost parameter \(r=\tanh(\theta/2)\), and the algebraic point \(r=1/9\) (\(\theta=\log(5/4)\)). The **same original 16×16** \(\Delta=A^\dagger A\) has the certified quadratic minimal polynomial with eight eigenvalues of each type; its arithmetic and harmonic spectral means and their ORIGINAL r-jets are exactly
\[
\boxed{\begin{aligned}
\mu&=\frac{141489}{10240000},&
h&=\frac{69399}{5030720},\\
\partial_r\mu&=-\frac{328779}{204800000},&
\partial_r h&=-\frac{20040939}{9885993640}.
\end{aligned}}\tag{5}
\]
The \(h\) formula follows from the independently owned two-root minimal polynomial \(\Delta^2-2\mu\Delta+vI=0\), via \(h=v/\mu\), not from an adjustable Gibbs prior.

The new strict correlation and its exact first field source are
\[
\boxed{\begin{aligned}
\delta_*&=(4p^3)^2 h(\mu-h)>0,\\
\left.\partial_r\delta\right|_*
&=(4p^3)^2\,\frac{1470321323030360979}
 {254636369534058496000000}>0.
\end{aligned}}\tag{6}
\]
At this actual native point, \(q=0.0130262718422078\dots\), \(\delta=2.7358301456152\dots\times10^{-7}\), and \(\partial_r\delta=5.1485621897563\dots\times10^{-6}\). The quoted decimals are diagnostics; the *strict signs* are exact consequences of (5),(6) in \(\mathbb Q(\sqrt5)\).

## 4. Strictly POSITIVE full two-port information-memory source — algebraic sign proof, no unstable numerical subtraction

Define the native observed two-port mutual information (in NATURAL nats)
\[
\mathcal I_2(q,\delta)=
\sum_{i,j=0}^1p_{ij}\ln\frac{p_{ij}}{p_i p_j}
=2h_{\rm nat}(q)-H_{\rm nat}(b_1,b_2).
\]
Set \(A=(1-q)^2+\delta\), \(B=q(1-q)-\delta\), \(C=q^2+\delta\), and
\[
L_A=\ln\left(1+\frac{\delta}{(1-q)^2}\right),\quad
L_B=\ln\left(1-\frac{\delta}{q(1-q)}\right),\quad
L_C=\ln\left(1+\frac{\delta}{q^2}\right).
\]
On the actual strictly positive chart \(0<q<1/2\), \(0<\delta<q(1-q)\),
\[
\boxed{\begin{aligned}
\partial_\delta\mathcal I_2
  &=L_A-2L_B+L_C=\ln(AC/B^2)>0,\\
\partial_q\mathcal I_2
  &=-2\mathcal B(q,\delta)<0,\qquad
\mathcal B=(1-q)L_A-(1-2q)L_B-qL_C.
\end{aligned}}\tag{7}
\]
The second strict sign does NOT rely on floating cancellation: \(\mathcal B(q,0)=0\) and exact differentiation gives
\[
\partial_\delta\mathcal B
=\frac{\delta(2q-1)}
 {(\delta+q^2)(\delta-q(1-q))(\delta+(1-q)^2)}>0
\quad(q<1/2,\ 0<\delta<q(1-q)).
\tag{8}
\]
Also \(AC-B^2=\delta>0\). Hence (7),(8) prove both strict signs.

At the ORIGINAL proper-boost fixture (5),(6),
\[
\partial_r q=c\,\partial_r h<0,\qquad
\partial_r\delta>0.
\]
Therefore both chain-rule terms have the SAME strictly positive sign:
\[
\boxed{\left.\partial_r\mathcal I_2\right|_*
=(\partial_q\mathcal I_2)(\partial_r q)
 +(\partial_\delta\mathcal I_2)(\partial_r\delta)>0.}\tag{9}
\]
The directly computed value is \(\mathcal I_2=2.2629223121\dots\times10^{-10}\) nats and \(\partial_r\mathcal I_2=8.5805614387\dots\times10^{-9}\) nats per original \(r\)-unit. **Nonzero sign of the information source is rigorously established independently of those decimals.**

For the actual original coarse PORT code lengths \(1+b\), stationary two-round expected code cost is \(2(1+q)\). Its honest **coarse-port pointer** Cost−measured-entropy is
\[
S_{2,\mathrm{port}}=2(1+q)-\frac{H_{\rm nat}(b_1,b_2)}{\ln\varphi}
=2\left[1+q-h_\varphi(q)\right]
 +\frac{\mathcal I_2}{\ln\varphi}.
\tag{10}
\]
Thus the strict *native, non-iid* correction to the two-independent-port-price source is
\[
\boxed{
\partial_r S_{2,\mathrm{port}}
 -2\partial_r S_{1,\mathrm{port}}
 =\frac{\partial_r\mathcal I_2}{\ln\varphi}>0,
\quad\text{numerically }1.7831152503\dots\times10^{-8}.}\tag{11}
\]
It is a small but EXACT nonzero source. It cannot be dismissed as a normalized-score Ward zero, because it is mutual information of two actually retained sequential ports. It is NOT the whole FULL128 fine-pointer/CQ entropy, nor the compulsory Book03 vertex Info or its Hodge operator; the other 126 fine categories, clock, work, preparation and oldRIGHT information remain in the real tape and its full valuation.

## 4a. Rank-two NATIVE two-parameter Golden port atlas: one-port-invisible source direction

The previous result is stronger on the ORIGINAL explicit two-real-parameter Kraus input chart \((r,\nu)\), not just along a scalar boost. The original Fourier/role-1 program constructor accepts the genuine amplitude \(\nu\) of the native four CAR words as well as the proper boost \(r=\tanh(\theta/2)\). Its Walsh row \(A\) at coefficient port zero contains only the original letters \(x,-\mathrm{base},x^\dagger,-\mathrm{base}^\dagger\), each **LINEAR** in \(\nu\); none of the square-root defect rows enters this row. Therefore, for fixed original phases, \(\Delta=A^\dagger A\) scales EXACTLY like \(\nu^2\). On the same bounded positive Julia chart,
\[
\boxed{\partial_\nu h=\frac{2h}{\nu},\quad
\partial_\nu\mu=\frac{2\mu}{\nu},
\qquad q=c h,\quad q_{11}=c^2h\mu.}\tag{12}
\]
This is a property of the ORIGINAL full128 native operator family; it does not assert the two parameters are freely writable or independently stationary in the full physical Book03/42-field programme.

Using the exact rational first derivatives (5), their determinant at \(r=1/9,\nu=3/5\) is STRICTLY NONZERO:
\[
\boxed{\begin{aligned}
B_*&=h\,\partial_r\mu-\mu\,\partial_rh
=\frac{6042018339}{1030291456000000}>0,\\
\det\frac{\partial(h,\mu)}{\partial(r,\nu)}
&=-\frac2\nu B_*
=-\frac{2014006113}{103029145600000}\ne0,\\
\det\frac{\partial(q,q_{11})}{\partial(r,\nu)}
&=-\frac{2c^3h}{\nu}B_*\ne0.
\end{aligned}}\tag{13}
\]
The middle determinant sign corresponds to row ordering \((h,\mu)\), column ordering \((r,\nu)\); using \((\nu,r)\) reverses it. The proof is direct differentiation of (12), with NO fitted determinant or extraneous native detector. In a real strictly positive two-dimensional input neighborhood, the inverse-function theorem proves that **the one-port probability and the genuine two-port joint-11 probability form local independent analytical coordinates**. A single terminal Golden-port probability cannot carry the whole two-parameter sequential source.

There is an explicit exact tangent that makes the one-port limitation falsifiable. At the fixture define
\[
\boxed{
v=\partial_r-\frac{\nu\,\partial_rh}{2h}\partial_\nu
=\partial_r+0.0440855159212652\dots\,\partial_\nu.
}\tag{14}
\]
The coefficient is not chosen by Einstein fitting: it is the unique tangent to a constant TRUE one-port Born probability level set \(q=c h\). It obeys
\[
\boxed{\begin{aligned}
D_vq&=0,\\
D_vq_{11}=D_v\delta
 &=c^2B_*>0,\\
D_v\mathcal I_2
 &=\ln(AC/B^2)\,c^2 B_*>0.
\end{aligned}}\tag{15}
\]
The last \(A,B,C\) are the **positive two-port probabilities** from §4, not Kraus matrices. Numerically the same original full128 test gives \(D_vq_{11}=5.2289691787\dots\times10^{-6}\), and \(D_v\mathcal I_2=8.6479477617\dots\times10^{-9}\) nats per native tangent unit. Their strict signs follow from exact rational \(B_*\) and \(AC-B^2=\delta>0\).

**Strong scoped consequence.** Even on the same REAL original CAR16/full128 family, all one-step port probabilities and their first source can be invariant along an admitted mathematical Kraus direction while TWO complete chronological positive outcomes and their memory-entropy source change strictly. This rules out replacing a sequential physical Book Info/clock source by a function only of the terminal ONE-PORT marginal whenever this native two-parameter tangent belongs to the physically admissible image. It remains to prove the actual 42-field and initial-writer pullback of this direction, and to establish what Book03's compulsory active algebra sees. This is an operational rank-two/sufficiency obstruction, **not** GR selection or a second Einstein source.

Independent native matrix checks at \(r=1/9,\nu=3/5\) reproduce the original \(2\times2\) observable Jacobian determinant \(-2.2704657992\dots\times10^{-7}\); a true small displacement along (14) gives numerical \(D_vq\simeq0\) and \(D_vq_{11}\simeq5.2289695\times10^{-6}\). The exact rational/calculus proof is independent of those finite differences.

## 4b. Exact TWO-PORT operational inversion of the ORIGINAL CAR16 spectral pair and its thermal Gibbs discrepancy

A further synthesis combines the just-proved native rank-two readout with the independently owned exact native inverse-square/Gibbs obstruction. On the algebraic original CAR16 fixture, the **actual** \(\Delta\) has exactly TWO distinct eigenvalues \(\lambda_\pm\), each of multiplicity eight (this is the already-proved exact 16×16 quadratic minimal polynomial, NOT a newly assumed spectral truncation).

The one-port and two-port **genuine positive original sequential probabilities** \(q=\Pr_*(b_1=1)>0\) and \(u=\Pr_*(b_1=b_2=1)>q^2\) exactly determine the arithmetic and harmonic means:
\[
\boxed{
 h=\frac q c,\qquad \mu=\frac{u}{cq},
 \qquad c=4p^3.
}\tag{16}
\]
The original quadratic spectrum then follows WITHOUT any independent matrix-eigenvalue fitting or new detector:
\[
\boxed{
\lambda_\pm
=\mu\pm\sqrt{\mu(\mu-h)}
=\frac{u\pm\sqrt{u(u-q^2)}}{c q}.
}\tag{17}
\]
All four two-round probabilities have already been shown to arise from the ORIGINAL full128 CAR16 Kraus matrices with oldRIGHT retained. Formula (17) is therefore an **operational spectral decoder** on this actual two-eigenspace native fixture, rather than a general claim that two moments determine an arbitrary 16-eigenvalue spectrum.

In particular the previously proved actual native inverse-square preparation versus the SAME-\(\Delta\) Golden Gibbs state at the unchanged \(\beta_0=2p^2\) has the trace-norm discrepancy
\[
\boxed{
\|\rho_*-\sigma_{\beta_0,\Delta}\|_1
=\sqrt{1-\frac{q^2}{u}}
-\tanh\left[
  \frac{\beta_0\sqrt{u(u-q^2)}}{cq}
 \right].
}\tag{18}
\]
The derivation is direct finite spectral calculus: the two native energies have equal multiplicity eight, so the inverse-square sector imbalance equals \(\sqrt{1-q^2/u}\), whereas the Gibbs sector imbalance equals \(\tanh(\beta_0(\lambda_+-\lambda_-)/2)\). Both are computed from the SAME two positive port probabilities and the existing fixed Golden parameters \(c,\beta_0\). There is no new temperature, spectrum, clock or observer.

At the exact original point \(r=1/9,\nu=3/5\), the two genuine probabilities reproduce
\[
\lambda_-\approx0.0132629182178348,\quad
\lambda_+\approx0.0143716520946652,\quad
\|\rho_*-\sigma_{\beta_0,\Delta}\|_1
\approx0.03969776485485>0.0388.
\]
The strict \(0.0388\) bound is the separately established rational thermal obstruction of the prior owner; here the **new content** is its reconstruction from the positive two-port measurement coordinates (16)–(18).

This is strategically useful: a field writer/observer can test the *native spectral-preparation versus hypothetical Gibbs heat* compatibility using only TWO ordinary port-event frequencies, without asking for a new Dirac tomography. At the same time the strict rank-two Jacobian (13) proves these two outcomes resolve distinct native spectral invariants locally. Whether the selected Book03 \(\Delta_N(V)\) equals the particular original \(\Delta\), or the original native programme selects this stationary preparation and this future test, is STILL unproved; (18) is a decisive operational **NO-GO TEST FOR THAT SPECIFIC HEAT IDENTIFICATION**, not a derivation or exclusion of physical GR.

## 5. Architectural consequence: spectral Gibbs obstruction is now visible in a real cheap native future record

The previously owned original CAR16 calculation proves \(\rho_*=\Delta^{-1}/Z\ne e^{-\beta_0\Delta}/\operatorname{Tr}e^{-\beta_0\Delta}\) at its actual Golden \(\beta_0=2p^2\); its strict trace-norm separation exceeds 0.0388. The current **same-input** theorem supplies a second, operational witness of the same underlying non-scalar native \(\Delta\): the two real consecutive Golden port bits have \(\delta>0\) iff that \(\Delta\) is nonscalar, and the field derivative of their mutual information is strictly positive at the original algebraic boost.

These observations do not imply a general numerical functional equality between covariance and the thermal trace-norm gap, nor that Book03's physically selected heat equals this \(\Delta\). The source is a concrete positive candidate whose **exact original field dependence** cannot be generated from independent single-port marginals.

This sharpens the remaining same-execution H+J+R test: a proposed physical native Info assignment must specify whether the accessible algebra contains consecutive correlated port histories, and compute its full memory correlation first source **before** comparing to the Einstein–CAR 42-source. A thermal/clock operator that encodes only \(\rho_*\)'s one-step port probabilities omits (11). A modular/predictive-state generator can represent the correlations, but needs a genuine Book03 selection, actual independent preparation/source equations and native refinements. This is a STRICT source-obstruction to an iid substitution on the ORIGINAL full128 carrier, not a no-go for every D0 completion.

## 6. Independent native replay and proof boundary

The checker `sources/d0_native_stationary_port_correlation_2026-10-22/check_native_port_correlation.py` imports the UNCHANGED six original `creators/native/adj/herm/root/tr` AST definitions from the pinned source `d0_book_uniform_source_2026-10-21/check_uniform_book_source.py` (owned blob `ee8de4635d24c668949ac9a0186616ab7d59f2ed`). It constructs ALL128 genuine 16×16 Kraus matrices and their analytic proper-boost derivatives; derives the stationary density and its FULL moving jet; sums ALL 128 branches into the two coarse actual parity effects and the genuine ordered two-round CP channel; checks the four probabilities, four derivatives, exact rational means and source, clean stationarity and positive memory information.

The narrow mathematical checker was independently tested with a transcription of those exact original constructor definitions in the local runtime, and returned PASS on every displayed numerical comparison. The pinned remote owner blob is to be used when replayed in a cloned repository; the local transcription is not by itself a byte-for-byte remote source replay. The strict signs (4),(6),(9) are analytic and rational, not numerical assertions. No 42-field geometry, nonstationary full tape, original full128 complete Info law, Book03 HJR selection or uniform refinement has been re-certified here.

**Scientific disposition:** `native_original_full128_two_port_corr=true`, `native_original_full128_two_port_memory_first_source_nonzero=true` on the specified original regular chart; `whole_native_Info_selected=false`, `Book03_active_cut_selected=false`, `GR_closed=false`.
