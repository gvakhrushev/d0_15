# Full native clock: all-unitary C1/C2 source bound beyond reflections

28 October 2026. Existing research PR #334 in gvakhrushev/d0_15.
Scientific input `5fe5203da2439d325dc9ef70f52c1111822fc22b`, preserving its generated-cut and literal native-word result and the incoming `1d29848f` reader/clock application.

[Proof in Russian](sources/d0_clock_winding_source_2026-10-28/PROOF_RU.md), [executed checker](sources/d0_clock_winding_source_2026-10-28/check_clock_winding.py), [observed receipt](sources/d0_clock_winding_source_2026-10-28/result.json).

## Same-execution input and removed premise

Consume the actual cyclic-clock and generated-prefix-cut construction in `sources/d0_native_execution_domain_2026-10-24/BOOK_MAP.md` (blob `a845c2e26eb01bb35e7ed3d5eaa000f2631e8ec3`) and the full-column native grammar (blob `9a32a3fa2e594c087d24b9d5dec497c4c5e03f44`).

For ANY unitary complete endpoint W, not necessarily a reflection, the full homogeneous INTERNAL K(9,11,13) heat is

    Z01=Nd(2a0+359)+4N sum_(k>=1) a_(kN) Re Tr(W^k),
    a_l>=0, a_l<=33 exp(beta(b-1)) I_|l|(2 beta c),
    b=||B_scene||<=1, c=||C_scene||=1/22.

The complete paired-Hodge carrier and all harmonic modes remain. The coefficients are obtained by an absolutely convergent noncommuting word expansion, not by assuming B_scene and C_scene commute. The bare paired-clock has the corresponding exact Bessel formula.

The full source satisfies |DH|<=A1_N ||DW||, with an explicit factorially small bound, and the full second jet satisfies

    |H_ab|<=A1_N ||W_ab||+A2_N ||W_a|| ||W_b||.

The norm of W_ab is NOT suppressed. At original beta=2p^2, 3/4<beta<4/5, the exact rational majorant for the INTERNAL A1_N is

    (176/359)/(1-x^2) * q_N/(1-q_N)^2,
    x=2/55, q_N=x^N/N!.

At N=26,38,39 this is respectively 4.600e-65, 1.896e-100, 1.768e-103. Gate-max transport multiplies by the actual N. Arbitrary endpoints of two real same-size/same-length words satisfy |H(W')-H(W)|<=A1_N ||W'-W||, without a continuous native gate assumption.

## Actual composition with the parent source

Generated cuts give the SAME full scalar B_root=H_N(W)-logdet(I-z E_W), E_W=P0 W*(I-P0)W P0. For the actual field lift L_h and actual gain Gamma_h,

    || DB_root L_h/Gamma_h - DJ_endpoint L_h/Gamma_h ||
       <= A1_(N_h) N_h ||L_h||_(field -> gate-max)/|Gamma_h|.

This consumes the existing endpoint source and supplies its full thermal remainder without exact-reflection or isospectral completion, whenever the displayed normalized bound vanishes. A sufficient growth condition is log[N_h ||L_h||/|Gamma_h|]=o(N_h log N_h), with fixed beta and the stated homogeneous scene. No free padding or omitted baseline is used. Different lengths, variable beta/scene, changed Gram and additional selected costs retain their own sources.

## Literal native validation, not only a small substitute channel

261 checks were actually executed. Full32 exact Golden-field reconstruction reproduces the incoming 38-stage words, inventory 4G/24CX/10SourceI, rank8 input and immutable oldRIGHT. All generated nonclosing leakage jets vanish; gate and generated-cut terms are equal positive halves of the actual QUERY source (total 6.8027514874981e-6 at z=2^-20).

Appending one genuine CX produces two 39-stage NONREFLECTIVE words. All-column spectral moments and a positive-first-winding versus exact-tail bound prove 2.2878e-106 < H_C-H_D < 3.5356e-103 on the full 530400-mode homogeneous scene carrier. The feedback difference is 5.59831568986097e-6. The huge heat matrix is not diagonalized.

A separate 39-stage pair (last CX versus last SourceI) has exactly identical ALL eight admitted input-output columns and exactly equal feedback, yet a strictly positive heat difference within the same bounds. Their primitive inventories differ; no equality of other per-gate costs, code histories or physical task semantics is asserted.

Small full-scene spectral checks and 160-digit bare-clock phase C1/C2 controls independently verify the formulas. Smooth controls are not continuous native pulse admission. Standard Bessel expansion is credited to NIST DLMF 10.35.2.

## Evidence and scope

Python 3.13.5 / SymPy 1.14.0 / NumPy 2.3.5 / SciPy 1.17.0 / mpmath 1.3.0. Normal and python -O executions, including repeat executions, produce byte-identical JSON. Exact rational bounds establish the stated sign and budgets; floating checks are structural controls.

Checker: SHA256 `37adfe34424d64947ed7bbd29727696e9b1b584f878256f7b07ea47292fd5774`, Git blob `5aae8b506730b6d758939deb53a67c2e047bcda9`.
Proof: SHA256 `ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418`, Git blob `1354b8dadd924b0d96639ba402385e9b734787a9`.
Receipt: SHA256 `06c614c3b0fead54ffe94bc68e9cefca75c9ebba16602dba86fd407627c62b42`, Git blob `d941031c937b5615aa234981e9ff4c1bfb39e87f`.

No original full42 root, huge READY, full128 CAR, Lean or CI replay. The homogeneous clock is not arbitrary RawZone or moving spatial geometry. The actual source/gain/metric map and the distinction between f_star and f_mom remain. Physical action/task selection, independent equations and generic exact-root recovery are not solved by thermal smallness. No claim/assembly promotion or merge: GR_closed=false.
