# Full-record entropy ledger and an exact future-test witness

Research continuation for [PR #334](https://github.com/gvakhrushev/d0_15/pull/334), 20 October 2026.
**Phase:** native realization / constitutive source gate.
**Input:** accepted main `02_REGISTRY/research/A4D_COMPLETE_FLAG_SOURCE_AND_NATIVE_MINIMUM_GATE_2026_10_20.md`, §§2–4, and its pinned compact Julia/CAR16 control; source construction `02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/flag_source.md`.
**Scope:** exact mathematical identity on the specified retained, purified finite archive; not a Book03 Info selection, physical admission proof, or GR closure.

## 1. No new carrier or forgotten branches

At fixed positive weights `w_s` (sum 1) and a supplied normalized pure state with actual oldRIGHT, the coherent finite record is

```math
|\Psi_y\rangle=\sum_s \sqrt{w_s}\,|s\rangle_F\otimes|\psi_s(y)\rangle_D,
\qquad D=\mathrm{data}\otimes\mathrm{oldRIGHT},\qquad
\langle\psi_s|\psi_s\rangle=1.
```

All chronological flags, incomplete cap words, true attempt clock and oldRIGHT are retained. Here `F` and `D` are complementary parts of the **same** pure record, not the different full128 or HJR-collar programme. If an abstract purification is appended to a mixed input, its algebraic identity below does not automatically make that added factor an admitted native record.

Let `rho_F=Tr_D |Psi><Psi|`, `rho_D=Tr_F |Psi><Psi|`. Define `H_phi(w)=-sum_s w_s log_phi(w_s)`, `S=-Tr rho log rho` (natural logs), and the already specified coherent relative-code component

```math
A_F=D_\varphi(\rho_F\|\operatorname{diag}w)
  = H_\varphi(w)-\frac{S(\rho_F)}{\ln\varphi}.
```

The diagonal of `rho_F` is exactly `w` without a dephasing postulate.

## 2. Exact complete-record correlation ledger

The global record is pure. By the Schmidt/singular-value identity,
`S(rho_F)=S(rho_D)` and `S(rho_FD)=0`. Therefore its quantum mutual information satisfies

```math
I(F:D)=S(\rho_F)+S(\rho_D)-S(\rho_{FD})=2S(\rho_F),
```

which gives the **exact, all-angle, all-cap identity**

```math
\boxed{\quad A_F+\frac{I(F:D)}{2\ln\varphi}=H_\varphi(w).\quad}
\tag{L}
```

If `w_s` is independent of the compact field at fixed cap, the RHS has zero field variation **at every differentiability order**; the identity is valid even across rank births where derivatives of the individual terms may not exist. This is not the claim that physical Book03 Price includes `I/2`: (L) is an information-accounting equality for two already-defined reduced quantities. The actual native choice of Cost/Info, what is paid/retained, and which reference tests are physically accessible remain the missing application.

## 3. Exact CAR16 stopped-control reduction and singular cancellation

Use exactly the accepted hostile control: CAR16 Choi input `Omega16`, compact `V(theta)=Lambda(exp(theta J23))`, `K_G=p V`, `K_B=sqrt(p) I`, `p=phi^-1`, one required success `m=1` and cap `N=6`. There are six success words `B^(j-1)G` of weights `p^(j+1)` (`j=1,...,6`) and the actual all-failure word `B^6` of weight `epsilon=p^6=9-4sqrt(5)>0`. They add to 1 by `1-p=p^2`. The math-only unitary regrouping of successful flag coordinates gives orthonormal `|G>_F,|B>_F` with

```math
|\Psi_\theta\rangle
=\sqrt{1-\varepsilon}\,|G\rangle_F\otimes(V(\theta)\otimes I)|\Omega_{16}\rangle
+\sqrt\varepsilon\,|B\rangle_F\otimes|\Omega_{16}\rangle .
```

The exact CAR16 Choi overlap `c(theta)=Tr V(theta)/16=cos^2(theta/2)` yields

```math
\rho_F=
\begin{pmatrix}
1-\varepsilon &\sqrt{\varepsilon(1-\varepsilon)}\,c(\theta)\\
\sqrt{\varepsilon(1-\varepsilon)}\,c(\theta)&\varepsilon
\end{pmatrix},
\qquad
\det\rho_F=\varepsilon(1-\varepsilon)(1-c(\theta)^2).
```

Hence `lambda_-=epsilon(1-epsilon) theta^2/2+O(theta^4)` and

```math
S(\rho_F)=\varepsilon(1-\varepsilon)\,\theta^2\ln(1/|\theta|)+O(\theta^2).
```

The marginal code term has the *negative* leading nonanalytic contribution
`-epsilon(1-epsilon) theta^2 ln(1/|theta|)/ln(phi)`.
The existing mutual information `I(F:D)/(2 ln phi)` has the *opposite, exactly equal* contribution; by (L) they cancel identically, not merely to second order. No fitted counterterm or new dynamics is introduced by writing this identity. Physical cancellation requires proving that the actual native full price counts the two terms with the prescribed ledger relation.

**Consequent correction to a minimum claim:** the prior conditional rank-birth obstruction remains valid for a price `A_F+F(theta)` when the remainder is C2. It is **not** an obstruction for an unspecified full retained price; the complete record already supplies a mathematically canonical nonsmooth partner, whose physical coefficient/admission must be derived.

## 4. Flag-only Code/Clock is provably not a complete physical source

For every stopped success/failure history in this specified compact instrument, the probabilities `w_s`, attempts `T_s`, successes `K_s`, and original code lengths `L_s=T_s+K_s` are exactly independent of `theta`. Therefore **any** scalar price depending on the compact field only through this finite classical history distribution and these fixed labels has zero first and higher field derivatives. This is a precise null-source theorem for the **flag-only** submodel, not the complete Book03 programme.

Yet the *same* full CAR16 Choi state differs with the field. The fixed mathematical future effect `P_Omega=|Omega16><Omega16|` on data+oldRIGHT (ignoring F) has probability

```math
R(\theta)=\langle P_\Omega\rangle_\theta
=\varepsilon+(1-\varepsilon)\cos^4(\theta/2).
```

Consequently
```math
R(0)=1,\quad R''(0)=-(1-\varepsilon)\neq0,
\qquad R(\theta)\xrightarrow[\varepsilon\to0]{}\cos^4(\theta/2).
```

So shrinking the failed-archive entropy source cannot erase the order-one dependence of **possible joint future tests** on the underlying field. A flag-only source/readout would identify states that this mathematical future effect distinguishes. Its *physical* implementation is not proved by this algebraic witness. The original Golden17 positive full-POVM field-sensitivity theorem uses a distinct grade-one Choi input and must not be silently substituted for the CAR16 Choi effect used here. Native `theory_transfer` must specify which future distinctions the actual D0 implementation admits and charge the complete readout.

## 5. One decisive native-source gate

On the **same** admitted execution and actual Book03 cost/info algebra, construct the full retained price `S_full` with chronological flags, data, oldRIGHT, final readout, preparation, controller/work and the actual clock. Differentiate it before eliminating internally stationary variables. Determine, rather than stipulate, which of the following the native accounting implies:

1. Exact correlation completion of (L) in `S_full`, with its physical bookkeeping source then zero in the compact field but readout/work/other terms retained;
2. A genuinely unpaired marginal coherent-code term, with the proven rank-birth non-C2 minimum gate;
3. A different admitted Info functional, established from its original operations/records and carrying its own source.

A frozen field-independent `H_phi(w)` alone cannot generate a nonzero gravitational response. Conversely vanishing of that component cannot justify dropping the full future readout, physical work or coframe/link matter responses. Do not mix in the separate conditional HJR Hessian or identify distinct preparations without a proved same-programme map.

**What changes for the parent:** rank-birth is not an unconditional reason to discard a native programme; the correlation ledger identifies an exact potential completion already inside its retained state. The only real missing step is **Book03 physical selection and admission of that ledger and its nonzero source-bearing complements**. Original `positive_gr`, raw216, complete full-price and nonlinear-refinement terminals remain OPEN.

Reproduce the exact finite golden/quadratic controls with `check_rank_birth_full_record_ledger.py`. The entropy/Schmidt and operational-source arguments above are analytic; that checker is a bounded hostile-control replay, not the source of the general theorem.


## 6. Exact normalizer identifiability obstruction: branch law fixes only action differences

This is a separate, strictly finite consequence of the same stopped programme and directly addresses Book03 §03.3.0a. Let `y` range over any compact field chart, and suppose one proposes to recover its native history actions `S_s(y)` solely from the **normalized scalar flag law** using

```math
P_s(y)=\frac{\varphi^{-S_s(y)}}{Z(y)},\qquad
Z(y)=\sum_t\varphi^{-S_t(y)},\qquad P_s(y)=w_s=\varphi^{-L_s}>0.
```

Taking base-`phi` logarithms on every finite positive branch gives the necessary and sufficient normal form

```math
\boxed{\quad S_s(y)=L_s+C(y)\quad(\forall s),\qquad
C(y)=-\log_\varphi Z(y).\quad}
\tag{N}
```

Conversely **every** common real function `C(y)` defines an action family with exactly these normalized probabilities, since `sum_s phi^{-L_s}=1`. Thus `S_s-S_t=L_s-L_t` is fixed, while the common field variation `D_y C(y)` is *not identifiable* from the flag probabilities alone. Equivalent score formulation:

```math
D_y\log P_s=-\ln\varphi\left(D_y S_s-
\sum_tP_tD_y S_t\right)=0,
\qquad D_yS_s=D_yC\ \text{for every }s.
```

There are two different physical claims that must not be conflated:

- If Book03's exact `w(gamma)=phi^{-S(gamma)}` is asserted as the **already normalized full-history weight** of these branches, then `Z=1` is an additional equality and (N) fixes `C=0`. The branch-only price is precisely `L_s` and contributes **zero** compact-field source.
- If it is an **unnormalized** weight whose Born probabilities are divided by `Z(y)`, the normalized branch law leaves `C(y)` unrestricted. This is a *non-identifiability*, **not** permission to insert a fitted source: the missing `C` must be derived from actual Book03 Cost−Info operations, controller/preparation/work/clock or the complete physical execution. A free common shift cannot be calibrated out of branch probabilities while simultaneously claimed as a uniquely predicted gravitational source.

The extra future-test witness in §4 shows that the *complete* output is not field blind, even though this marginal law is. Hence neither (L) nor (N) determines the full dynamical source; they identify exactly the information missing in an attempted flag-only extraction. This is the parent `constitutive -> native_sector -> gr_operational_realization` substitution gate: demonstrate one common admitted full record, native price **and** physical normalization, not just a matched histogram or another stationary geometry.


## 7. Classicalizing the actual flag pointer: a stronger Holevo ledger

The pure coherent tape and the classically readable tape must not be silently equated. Define the physical *candidate* pinching of the chronological flag register (when the controller actually registers orthogonal labels):
\[
\mathcal D_F(|\Psi\rangle\langle\Psi|)
 =\omega_{FD}
 =\sum_s w_s |s\rangle\langle s|\otimes
 |\psi_s\rangle\langle\psi_s|.
\]
This map does **not** remove failed leaves, data, oldRIGHT or the attempt clock. The data marginal is unchanged: \(\rho_D=\sum_s w_s|\psi_s\rangle\langle\psi_s|\). The classical flag marginal becomes \(\operatorname{diag}w\).

For pure conditional states, the Holevo quantity of that *existing* classical-quantum history ensemble is
\[
\chi(F{:}D)=S(\rho_D)-\sum_s w_s S(|\psi_s\rangle\langle\psi_s|)
 =S(\rho_D)=S(\rho_F).
\]
Thus the previously proved coherent-flag relative code has the **exact alternative form**
\[
\boxed{\quad \mathcal A_F+\frac{\chi(F{:}D)}{\ln\varphi}=H_\varphi(w).\quad}\tag{H}
\]
Equivalently \( \mathcal A_F=H_\varphi(F|D)_{\omega}\), the *quantum conditional entropy of the already classicalized flag labels*, in base-\(\varphi\) units. This explains precisely how a record may have a large raw code \(H_\varphi(w)\) but a smaller conditional code when some branch information is already reflected in the retained data. The Holevo quantity is a bound on obtainable classical information, **not** an assertion that every admitted one-shot D0 readout reaches it.

The pure-tape quantum mutual information is \(I(F{:}D)_{|\Psi\rangle}=2\chi\); after flag pinching it is \(\chi\). Flag pinching produces entropy \(S(\omega_{FD})-S(|\Psi\rangle)=H(w)\). Its marginal entropy change is \(H(w)-S(\rho_F)\); the remaining \(S(\rho_F)\) accounts for the drop in mutual information. These equalities are exact entropy bookkeeping, not an additional physical price or a license to count \(\mathcal A_F\) and \(\chi\) independently. To identify the actual Book03 Info one must show whether the controller writes a coherent or classical flag, which tests are retained and how the Cost−Info ledger pays for its operations.

## 8. Full stopped history -> final readout: exact source transfer without an outcome floor

Retain **every** stopped history \(s\), with fixed field-independent Golden probability \(w_s\), attempted ticks \(T_s\), and success count \(K_s\in\{0,\ldots,m\}\). Append a single fixed, finite, complete physical-*candidate* POVM at the **end** of the programme. Let its Kraus amplitudes on the conditional normalized data+oldRIGHT state be
\[
a_{k,r}(y)=L_r(y)|\psi_k(y)\rangle,\quad
q_{k,r}(y)=\|a_{k,r}(y)\|^2,\quad \sum_{r=1}^{R}q_{k,r}=1.
\]
For the stopped joint *classical* record,
\[
P(s,r;y)=w_s q_{K_s,r}(y).
\]
No success-only renormalization is made. The Shannon chain rule, with actual attempt clocks already inside \(s\), gives
\[
H_\varphi(S,R;y)=H_\varphi(w)+\sum_s w_sH_\varphi(q_{K_s}(y)).
\]
All \(K_s=m\) completed words share **exactly** the same \(\psi_m\). Writing
\(\varepsilon=\sum_{s:K_s<m}w_s\),
\[
\boxed{
D_y H_\varphi(S,R)-D_yH_\varphi(q_m)
=\sum_{s:K_s<m}w_s\bigl(D_yH_\varphi(q_{K_s})-D_yH_\varphi(q_m)\bigr).
}\tag{T}
\]
This is valid for any finite cap \(N\), all failures and all final outcomes, including zero-probability outcomes.

Here is a **uniform C1 bound without any outcome-probability floor**. Suppose for all \(0\le k\le m\) and unit field tangents \(v\),
\[
\left(\sum_{r=1}^{R}\|D_v a_{k,r}\|^2\right)^{1/2}\le B.
\]
Every \(q_{k,r}=\|a_{k,r}\|^2\) has a C1 Shannon term even at amplitude zeros. Indeed
\[
|D_vH_\varphi(q_k)|
\le\frac2{\ln\varphi}
\left(\sum_rq_{k,r}(\ln q_{k,r})^2\right)^{1/2}
\left(\sum_r\|D_v a_{k,r}\|^2\right)^{1/2}
\le\frac{4\sqrt R}{e\ln\varphi}B,
\]
using \(\sup_{0\le x\le1}x(\ln x)^2=4/e^2\). Thus (T) implies
\[
\boxed{\quad
\|D_y H_\varphi(S,R)-D_yH_\varphi(q_m)\|_*
\le \frac{8\sqrt R}{e\ln\varphi}\,\varepsilon B.
\quad}\tag{U}
\]
For a *fixed* POVM, completeness gives \(\sum_r\|D_v(L_r\psi_k)\|^2=\|D_v\psi_k\|^2\). For moving POVM or preparation, their **actual** operator/amplitude jets must instead enter \(B\); this estimate does not delete those sources.

In the existing compact success-count protocol take \(m_h=\lfloor\tau/h^2\rfloor\), \(N_h=\lceil 2m_h/g\rceil\), \(g=p^2\), and \(\psi_k(y)=\exp(kh^2X(y))\psi_0(y)\), with \(X(y)\) skew-adjoint and bounded first jets. Duhamel's formula gives for \(k\le m_h\):
\[
\|D_y\psi_k\|\le\|D_y\psi_0\|+\tau\|D_yX\|.
\]
Therefore for an actually fixed admitted finite POVM, \(B=O(1)\) on the declared bounded chart, whereas the owned \(\varepsilon_h\le e^{-m_h/4}\). In particular
\[
h^{-2}\|D_yH_\varphi(S,R)-D_yH_\varphi(q_{m_h})\|_*\to0.
\]
The same holds for an \(O(h^{-4})\) raw site sum followed by \(h^{-2}\), subject to the actual local-support/overlap map and a polynomial \(B_h\); its conservative right-hand bound is \(O(h^{-6}\sqrt{R_h}B_h e^{-m_h/4})\). The final readout source \(D H_\varphi(q_{m_h})\) is **not** forced to vanish. This is a precise transfer of the full-history *classical Shannon component*, not an equality with the complete native Book03 Cost−Info source.

## 9. Exact CAR16 local Fisher saturation on the whole retained archive

There is a sharper operational test of why the final source remains relevant. Let the **original** CAR16 Choi state \(|\Omega_{16}\rangle\) and compact generator \(J_{23}\) be as in §3. For any finite stopped success-count tree with the actual weights \(w_s\), put \(t_s=K_s h^2\) and
\[
|\Psi(F)\rangle=
\sum_s\sqrt{w_s}\,|s\rangle\otimes
(\Lambda(e^{t_s FJ_{23}})\otimes I)|\Omega_{16}\rangle.
\]
Its original branch distribution \(w_s\) is independent of \(F\); hence its **classical flag-only Fisher information is identically zero**.

The exact CAR16 Choi overlap is
\[
\langle\Omega_{16}|(\Lambda(e^{tFJ_{23}})\otimes I)|\Omega_{16}\rangle
=\cos^2(tF/2).
\]
Differentiating at \(F=0\) gives the mean generator \(0\) and squared derivative norm \(t^2/2\). The entire pure flag+data+oldRIGHT record therefore has exact single-parameter quantum Fisher information
\[
\boxed{\quad \mathcal I_Q(0)=2\sum_s w_s t_s^2
=2h^4\mathbb E[K^2].\quad}\tag{Q}
\]
The classically pinched flag+conditional-pure-state record has the **same** quantum Fisher information: the weights are fixed and the pure-branch QFI values add. Thus in this exact one-axis model, the full local parameter information is not lost merely by the controller classically registering the flags, although its coherence entropy ledger changes.

For an explicit *mathematical* future effect on the supplied CAR16 data+oldRIGHT, take
\(P_\Omega=|\Omega_{16}\rangle\langle\Omega_{16}|\), ignoring flags. Its binary return law is
\[
q_{\Omega,h}(F)=\sum_sw_s\cos^4(t_sF/2)
=1-\tfrac12\mathbb E[t_s^2]F^2+O(F^4).
\]
The other event has probability \(1-q_\Omega=\frac12\mathbb E[t_s^2]F^2+O(F^4)\). Its classical Fisher information **in the punctured limit**, not the support-restricted Fisher sum at the rank-deficient point, is exactly
\[
\boxed{\quad
\lim_{F\to0,\;F\ne0}\mathcal I_{\{P_\Omega,I-P_\Omega\}}(F)
=2\mathbb E[t_s^2]=\mathcal I_Q(0).
\quad}\tag{F}
\]
Thus this positive two-effect test locally attains the full pure-record quantum Fisher value along the one compact angle, although the flag histogram itself is perfectly blind. The positive effect is a *mathematical Choi-reference benchmark*, not a newly asserted native-admitted measurement; a physical implementation and its price, including access to oldRIGHT, remain open. The equal limit is nonregular because the rejected event is zero at \(F=0\); the full detector Shannon has a rank-birth \(F^2\ln(1/|F|)\) term and is only C1 there.

With the existing cap rule, \(\tau_h=m_hh^2\), every completed history has \(t_s=\tau_h\) and every incomplete history has \(0\le t_s<\tau_h\). Hence the **uniform finite-cap sandwich**
\[
2(1-\varepsilon_h)\tau_h^2
\le\mathcal I_Q(0)=2\mathbb E[t_s^2]\le2\tau_h^2,
\]
and in the exact success-count refinement
\[
\boxed{\mathcal I_Q(0)\longrightarrow 2\tau^2}
\]
as \(h\to0\), with the missing-cap contribution at most \(2\varepsilon_h\tau_h^2\). The actual attempt time \(T_s\), code \(L_s=T_s+K_s\), real preparation and controller charges remain retained/paid; \(t_s\) is the accumulated **success** angle, not a replacement of that clock.

This is a concrete source-vs-information separation under refinement. It does **not** yield an Einstein tensor, select a metric action, or identify a local Lorentz-frame angle with physical curvature. The Choi probe fixes a relational reference, and its native permission, gauge/observer transport, full128 substitution and physical Cost−Info must be established before any gravitational use. The whole-HJR saddle and raw216 original terminal remain separate.

The bounded exact \(\mathbb Q[p]\) replay for finite caps is \`check_golden_full_history_fisher.py\`. The general (T),(U),(Q),(F) are analytic identities; the checker verifies the original stopped Golden combinatorics and second-jet coefficients without numerical differentiation.


## 10. A precise full128 no-factorization theorem from the owned 6-vs-24 ranks

The live #334 research branch has an **independent exact** original full128 two-sided Lorentz result, at source snapshot \`1f5c576809e2457b7ac2e677d7f898a10001d99b\`: see \`sources/d0_native_full128_order_readout_2026-10-19/RESULT.md\` and its exact checker. For the fixed \(L=4\), \(h=1/4\), Fourier phases \((1,1,1,i)\), \(I_{16}/16\) system preparation and untouched full-rank reference128 spectator, vary the original four proper Lorentz links in all 24 independent tangent directions. The **entire 128-outcome probability map** \(q(y)=(\operatorname{tr}\sigma_j(y))_j\) has exact derivative rank 6. The **entire unnormalized conditional quantum-output map** \(\sigma(y)=(K_j(y)(I_{16}/16)K_j(y)^*)_{j=1}^{128}\) has exact derivative rank 24, established by a nonzero 24-by-24 minor over \(\mathbb Q(\sqrt5)\).

**Differential no-factorization theorem.** There is no \(C^1\) map \(G\), defined on a neighborhood of the base probability vector in its probability affine span, with
\[
\sigma(y)=G(q(y))
\]
on a neighborhood of the base link fields. If such a map existed, the chain rule would yield
\(D\sigma=DG\circ Dq\), hence \(\operatorname{rank}D\sigma\le\operatorname{rank}Dq=6\), in direct contradiction to \(\operatorname{rank}D\sigma=24\). No model-specific numerical threshold enters the proof; it consumes the already-certified exact ranks.

More concretely the 18-dimensional \(\ker Dq\) is disjoint from \(\ker D\sigma=\{0\}\) except at zero. **Every nonzero link tangent in that 18-dimensional space is invisible to the complete classical pointer probabilities at first order, but changes at least one retained branch density matrix at first order.** In such a branch \(\operatorname{tr}D\sigma_j= Dq_j=0\), so its nonzero Hermitian derivative has a positive and a negative spectral part. A rank-one positive effect \(E=|u\rangle\langle u|\) in a nonzero eigendirection yields \(D\,\operatorname{tr}(E\sigma_j)\ne0\). This proves existence of a mathematical future two-effect test that resolves that direction. Since the full \(D\sigma\) is injective, a finite selection of at most 24 suitable branch-conditioned rank-one tests gives a locally full-rank Jacobian (linear algebra: the real span of rank-one projector effects separates Hermitian matrices).

**Interpretation and remaining physical application.** A purported faithful GR/native operational realization that factors the *whole retained output state and its admissible future tests* through the 128 classical pointer frequencies alone is impossible on this fixed chart. This does NOT imply that a scalar Book action is forbidden to depend only on \(q\), does NOT force the 24 distinguishing future effects to be physically admitted, and does NOT turn 24 frame/link parameters into 24 gauge-invariant gravitational observables. The untransported reference and gauge quotient must be handled by the original observer/coframe interface. A precise next experiment is not another Bloch census: select/compile and charge a **finite basis of these future distinguishing tests on the SAME original full128 history**, verify their admitted measurement and source derivatives, and consume their nonfactorizing channel in \`gr_operational_realization\`. Whether the compulsory full Book03 cost pays for this carrier is still open.

This result connects the compact benchmark of §§7–9 (where all flag probabilities are blind but a future datum is responsive) to the *original* full128 program (where exactly 18 link tangents are first-order pointer-blind but not output-state-blind). It does not conflate their preparations or numerical Fisher coefficients.


## 11. Stronger exact result: a SIGNED, regular three-outcome CAR16 readout saturates full-history QFI

The binary Choi-return benchmark in §9 measures the magnitude of a small rotation but is even in \(F\) and does **not** distinguish \(+F\) from \(-F\). Its punctured-limit Fisher equality is therefore not by itself a first-order source or a signed curvature test. There is an exact positive, fixed, sign-sensitive repair using the **same original CAR16 Choi state** with **no extra generator**, as a mathematical measurement benchmark.

Put \(u=|\Omega_{16}\rangle\), \(G=\Lambda_*(J_{23})\otimes I\). From the exact CAR16 overlap,
\(\langle u|Gu\rangle=0\), \(\|Gu\|^2=1/2\). Set \(v=\sqrt2\,Gu\), so \(u,v\) are orthonormal. Define the fixed three-effect projective POVM on data+oldRIGHT:
\[
E_\pm=\tfrac12|u\pm v\rangle\langle u\pm v|,
\qquad E_\perp=I-E_+-E_-\succeq0.
\]
For one branch \(|\psi(\theta)\rangle=e^{\theta G}u\), differentiate the exact overlap \(m(\theta)=\langle u|\psi(\theta)\rangle=\cos^2(\theta/2)\). Since
\(\langle v|\psi(\theta)\rangle=-\sqrt2\,m'(\theta)=\sin\theta/\sqrt2\), **all three exact probabilities** are
\[
\boxed{
q_\pm(\theta)=\tfrac12\left(\cos^2(\theta/2)\pm\frac{\sin\theta}{\sqrt2}\right)^2,
\qquad
q_\perp(\theta)=\sin^4(\theta/2).
}\tag{S}
\]
They are positive and sum exactly to one. At \(\theta=0\):
\[
(q_+,q_-,q_\perp)=(1/2,1/2,0),\quad
(q'_+,q'_-,q'_\perp)=(1/\sqrt2,-1/\sqrt2,0),\quad
q''_+=q''_-=q''_\perp=0.
\]
Thus the *regular, signed* Fisher information at the base, computed from the positive-support \(\pm\) outcomes, is
\[
\mathcal I_{\rm signed}(0)=2
\]
for \(t=1\), which equals the original pure CAR16 Choi QFI. The third probability vanishes to **fourth** order \(O(\theta^4)\), so its entropy is \(O(\theta^4\log(1/|\theta|))\), which **is C2** at zero. All \(\pm\) probabilities are strictly positive there and have regular sources. Directly,
\[
H_\varphi(q(\theta))''\big|_{\theta=0}=-\frac{2}{\ln\varphi}.
\tag{S2}
\]
This is a *specific C2 final readout* even though the *different coherent flag marginal* has a \(\theta^2\log(1/|\theta|)\) rank-birth term. It is not a proof that every part of the complete Book price is C2.

For the same stopped tree of §9, each conditional angle is \(\theta_s=t_sF\), \(t_s=K_sh^2\). **Retain all history labels** and apply this single fixed measurement at the end. The joint classical source \(\{P(s,\pm),P(s,\perp)\}\), \(P(s,r;F)=w_s q_r(t_sF)\), has
\[
\boxed{
\mathcal I_{\rm signed}^{\rm full}(0)=2\,\mathbb E[t_s^2]
=\mathcal I_Q(0),\qquad
D_F^2H_\varphi(S,R)\big|_0
=-\frac{2\mathbb E[t_s^2]}{\ln\varphi}.
}\tag{SR}
\]
The **sign** is detected at first order on each branch with \(t_s>0\), and every positive-baseline \((s,\pm)\) history contributes its genuine conditional information. The result is unaffected by dephasing the flag register in its actual pointer basis, since the joint classical law is the same. In the Book03 sign convention \(S=\mathrm{Cost}-\mathrm{Info}\), **if** this entire final Shannon entropy is proved to be an actual counted Info term and its other price components have zero second jet on this path, the corresponding \(-H_\varphi\) term supplies the positive quadratic variation \(+2\mathbb E[t_s^2]/\ln\varphi\) without an inserted stabilizer. This is a conditional implication, NOT a selected Book price or a numerical repair of the unrelated HJR saddle.

An additional **exact record-value theorem** follows by ignoring the labels only for the *statistics* of the same final readout. Its marginal derivatives are proportional to \(\mathbb E[t_s]\), so
\[
\mathcal I_{\rm signed}^{\rm marginal}(0)=2(\mathbb E[t_s])^2,
\qquad
\boxed{\;
\mathcal I_{\rm signed}^{\rm full}(0)-
\mathcal I_{\rm signed}^{\rm marginal}(0)
=2\,\operatorname{Var}(t_s).
\;}
\tag{V}
\]
Equivalently the difference between the joint and marginal Shannon second jets is \(-2\operatorname{Var}(t_s)/\ln\varphi\). The actual chronological record contributes exactly this *success-count clock-jitter information*. Because all completed paths have \(t_s=\tau_h\) and failures weigh only \(\varepsilon_h\),
\[
0\le\operatorname{Var}(t_s)\le
\mathbb E[(t_s-\tau_h)^2]\le\varepsilon_h\tau_h^2.
\]
Thus both signed first-order information and its C2 readout source survive the \(h\to0\) limit, while the **incremental** price of retaining the random success-count in this particular Fisher comparison becomes exponentially small. This does not erase the actual attempt clock \(T_s\) or its nonzero prospective code/work charge.

**Interface to the original D0 detector:** The functional shape in (S) is the unattenuated version of the already-owned fixed Golden17 *signed marks*
\(q_\pm^{\rm Golden17}(\theta)=\kappa(\cos^2(\theta/2)\pm\sin\theta/\sqrt2)^2\) on its **different grade-one Choi preparation**. The Golden17 test retains other outcomes and a small factor \(\kappa\), whereas (S) has \(1/2\), so their Fisher scales and preparations are NOT identified. They share an exact mathematical sign-sensitive response mechanism. Physical access to the full CAR16 Choi reference, the actual rank-one effects and their native Cost−Info/measurement implementation must be supplied; gauge/observer transport and the complete full128 programme are separate.

**Takeaway for \`gr_operational_realization\`:** There is no mathematical necessity to discard failures, use an unphysical infinitely sharp readout, introduce a fitted Hessian, or lose the *sign* of the compact field to obtain a smooth first and second operational source. A fixed complete positive future measurement exists and carries the exact stopped-history Fisher/entropy jets. The still-open physics is its **admission and mandatory price on the same full D0 carrier**, and its extension from this one compact direction to the physically gauge-quotiented complete Lorentz/coframe/matter response.
