# Native quantum return: bounded implementation handoff

22 October 2026. Existing Draft #334; input
e92ecb3bdc53a2b958b1cc09a7b0398f978c87f3. This applies the analytic
terminal-balance and quantum-information identities to the actual unchanged
CAR16/full128 native constructor. It does not select physical Book03 Info.

**Stopping-predicate scope.** These 223 checks use the previously declared
port-return comparison \(b(z)=z\bmod2\), with two positive classes and
stationary mean length three. Every fine record is retained throughout
that port-stopped execution. The literal original full-label comparator
instead uses \(b(z)=z\); this boost fixture has 64 active fine labels, so its
stationary mean length is 65. It is a different stopping language. The
general analytic theorem can be applied to that comparator separately,
but none of the binary numerical values or budgets below is transferred
to full-label stopping.

## Frozen implementation and replay

| File | SHA-256 |
|---|---|
| check_native_quantum_return.py | 79cbfad7027d0ea46598dfc7f881ae44476defc68f664e634e846e24fabbeb00 |
| NATIVE_QUANTUM_RETURN_RESULT.json | 8b1a9984b0b6da9b0809fd1097010d513e0fdd0766582f5f15c27de94dd6b67b |

The new calculation passes **223 explicit checks**. Normal receipt authoring
and optimized read-only execution produced exactly equal parsed output.
There are no assert statements. Default execution compares the immutable
receipt with explicit tolerances and does not write. Only the explicit
--write-result option authors a receipt; --print-only diagnoses a changed
calculation without writing or comparing.

    OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_native_stopped_quantum_balance_2026-10-22/check_native_quantum_return.py

The original constructor, previously owned joint jet, and earlier one/two-round
entropy receipt are separately SHA-256 pinned. Only needed AST definitions
are loaded. No historical suite executes.

## Actual carrier and independent evaluations

The fixture is \(r=1/9,\nu=3/5\), phases \((i,i,-1,-i)\), and
\(\rho=\Delta^{-1}/\operatorname{Tr}\Delta^{-1}\). All128 slots enter the
two row-vectorized \(256\times256\) CP maps. Exactly64 slots and their jets
are structurally zero; no small-probability cutoff is used.

The \(r\) jet retains \(d\theta/dr=81/40\). The owned one-port-invisible
tangent uses \(d\nu=0.04408551592126523\,dr\). Its actual port derivatives
are below \(1.4\times10^{-17}\). Five-point values use a local straight
path with this tangent, without asserting higher-order level-set agreement.

The actual resolvents check

\[
R_a\mathcal A_a\rho=\rho,\quad
\sum_a\mathcal A_aR_a\mathcal A_a\rho=\rho,\quad
R_a=(\mathsf I-\mathcal A_{1-a})^{-1},
\]

with full source jets, all128 last-fine-label DATA blocks equal to
\(\mathcal I_z(\rho)\), and all expected fine counts equal to \(3q_z\).
Both success effects have positive spectral gaps. For caps \(K=1,8,64\),
direct native Kraus iteration retaining every abort agrees with separate
binary matrix powers and full product-rule jets:

\[
e_K=(\mathsf I-\Phi)B_K,\quad B_K=\sum_a\mathcal T_a^K\rho,\qquad
de_K=-d\Phi B_K+(\mathsf I-\Phi)dB_K.
\]

All fine-count cap terms are retained. At \(K=8\), abort mass is
0.011727206418411178 and terminal boundary trace norm is
\(8.018321001951106\times10^{-6}\).

## Quantum witness and genuine preparation residual

The four blocks retaining the first two coarse ports and terminal DATA are

\[
X_{aa}=\mathcal A_a^2\rho,\qquad
X_{ab}=\mathcal A_aR_a\mathcal A_b\mathcal A_a\rho\quad(a\ne b).
\]

The reference is \(q_aq_b\rho\). Actual block traces retain the correlated
two-port law. Every normalized DATA eigenvalue exceeds 0.0599. Full-spectrum
logarithms use no clipping or regularization. The noncommuting logarithm
derivative agrees with the stationary entropy identity and five-point values.

| Quantity | Native numerical result |
|---|---:|
| Compressed quantum relative entropy | \(2.121930145854855\times10^{-5}\) nats |
| Two-coarse-port MI component | \(2.262922261955878\times10^{-10}\) nats |
| Terminal DATA Holevo component | \(2.121907516539068\times10^{-5}\) nats |
| Full \(r\) source of this witness | \(4.020705930763725\times10^{-4}\) |
| Full one-port-invisible \(v\) source | \(4.052168714788892\times10^{-4}\) |

This witness supplies an analytic **value** lower bound. Its computed
derivative is not a bound on the unknown complete entropy source.

Freezing initial DATA while varying real gates leaves the stationary
section: the terminal source has trace norm 0.0024462117467806896 and
mean-round source is 0.0023392532638302627. Uncapped and finite-cap
preparation corrections are retained.

For the declared fine charge \(c_z=1+\operatorname{port}(z)\), define

\[
F=\sum_z(c_z+\ell^{-1}\log q_z)K_z^\dagger K_z,\qquad
B=\sum_aR_a^*F+
\ell^{-1}\left[\log\rho+\sum_aR_a^*\mathcal A_a^*\log\rho\right].
\]

The directly differentiated count-plus-terminal boundary source is
0.002435857477514029; \(\operatorname{Tr}(B\,d\delta)\) is
0.002435857477514013. Reversing the adjoint order changes the source by
\(2.8260118173978853\times10^{-5}\), while
\(\|[B,\rho]\|_1=0.002442401233461373\). Additional paid ledgers remain
external to this declared charge.

## Consumed complete-entropy bounds and scope

Hash-consumed historical evidence gives
\(\chi_1=0.00016955914079330725\),
\(M_{\rm pair}=6.512430039684602\times10^{-10}\), and
\(L_{\rm first}=3.9309466792758485\times10^{-9}\). The analytic parent's
strengthened bounds instantiate nominally as

\[
0.00016955979203631122
\ \le D_{\rm full,stop}\le\
0.0005086734914332425.
\]

These are bounds for the **complete fine tape under the declared port-return
stopping rule**, not the literal full-label stopping rule. The endpoints
evaluate analytic bounds in floating arithmetic; they are not outward-rounded
intervals. The receipt preserves inherited all-mode regularization errors
and derivatives of these expressions without claiming derivative inequalities.

The complete stopped entropy and source are not computed. The stationary
boundary does not pay for physical preparation. Information-algebra
selection, all42 field transport, other paid ledgers, and genuine upstream
equations remain obligations. GR_closed=false.
