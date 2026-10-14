# Boundary of the field-to-instrument variation

**Exact research result, 14 October 2026.** This packet tests one G0 arrow:
whether the moving-preparation source fixes the physical tangent of the
unitary returns from its reference instrument alone. It does not add a D0
primitive, select an action, or claim that the instrument is physically
admitted.

The input is the published v3 moving-preparation source at
[`f1270f63`](https://github.com/gvakhrushev/d0_15/tree/f1270f63cffa5fcfc27b469ff2517d8398d5362a/02_REGISTRY/research/sources/d0_local_record_to_matter_2026-10-14/continuation_v3).
Its exact checker passes 169 controls. That source derives the full first
pullback for a fixed registered count event and allows differentiable return
variations that make formerly commuting returns noncommute. It does not give
a map from a coframe/link variation to those return tangents.

## Two completions with the same reference data

Let p = (√5−1)/2 and γ = p³. Use the same four-dimensional reference
carrier, initial state I/4, two returns, and fixed event 1 ≤ k ≤ 2 after
T = 3 rounds as in the v3 exact checker:

\[
U_1=\operatorname{diag}(1,-1,i,-i),\qquad
U_2=\operatorname{diag}(1,i,-i,-1).
\]

They commute at the reference. Use the two real-symmetric matrices

\[
H_1=\begin{pmatrix}1&1&0&0\\1&0&1&0\\0&1&2&1\\0&0&1&-1\end{pmatrix},
\qquad
H_2=\begin{pmatrix}0&0&1&0\\0&2&0&1\\1&0&-1&0\\0&1&0&1\end{pmatrix}.
\]

For one fixed scalar probe coordinate ξ(t)=t, define two candidate
field-to-return maps, with λ=1 and λ=2:

\[
U_r^{(\lambda)}(t)=e^{i\lambda tH_r}U_r.
\]

Each is unitary for real t, has the same value U_r at t=0, and has tangent
dU_r/dt at t=0 equal to iλH_rU_r. The registered
event, apparatus, reference density, and probe calibration are identical.
Both tangents are in the v3 instrument class; the v3 source explicitly
allows noncommuting nearby returns.

Let ρ_A(t) be the normalized state conditioned on that same event,
computed from the actual two-outcome channel recursion, and put

\[
\Delta(t)=\sum_{r=1}^2(U_r^{(\lambda)}(t)-I)^*
                         (U_r^{(\lambda)}(t)-I),
\qquad
S_\lambda(t)=\operatorname{Tr}(\Delta(t)\rho_A(t)).
\]

The event probability is positive and the two completions have the same
reference value:

\[
\Pr(A)=144p-\frac{177}{2}>0,
\qquad
S_1(0)=S_2(0)=\frac{380-12p}{71}.
\]

Differentiating the full normalized event-conditioned cost, including the
change in its prepared state and in event normalization, gives the exact
values

\[
S_1'(0)=\frac{1644p+17733}{5041}>0,
\qquad
S_2'(0)=\frac{3288p+35466}{5041}=2S_1'(0).
\]

Thus the same reference instrument and the same fixed calibration give
different first responses. The difference is not a frozen-state artifact:
the certificate separately rejects replacing the moving (\rho_A(t)) by
its reference value. All matrix arithmetic is exact in Q(p,i), reduced
using p²+p=1; the event window is held fixed.
The adjacent checker reconstructs the source channel, event recursion, full
normalization derivative, and both tangents. Its receipt is
[`a4d_native_field_instrument_jet_results.json`](certificates/a4d_native_field_instrument_jet_results.json).

## What this resolves

This is a concrete non-identifiability witness for the declared
**instrument interface**: the reference unitary returns and the v3 preparation
rule do not determine the derivative of the prepared cost with respect to a
field probe. The missing datum is an independently owned map from the
coframe/link variations to δU_r, including its scale and its
admissible tangent constraints. Fixing an overall unit after the fact cannot
identify which of these two maps the core supplies.

The witness is not two claimed D0 physical solutions. Neither completion has
been shown admitted by the D0 core, and the current interface does not yet
provide that admission predicate. The calculation uses a single scalar probe
and a four-dimensional instrument block; it does not construct the shared
\((q,D,b,m)\) carrier, a ten-component stress tensor, a complete
\(H+J+R\) stationary point, a native refinement, or an Einstein solution.
It therefore closes this one interface question without closing G0, the
positive ОТО path, or the original #310 response-decoupling terminal.

Reproduce with

```sh
python3 02_REGISTRY/research/certificates/a4d_native_field_instrument_jet_check.py
```

The checker pins the v3 source and receipt. The adjacent JSON is immutable by
default; `--write` is only for an explicitly reviewed certificate refresh.
