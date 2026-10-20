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
