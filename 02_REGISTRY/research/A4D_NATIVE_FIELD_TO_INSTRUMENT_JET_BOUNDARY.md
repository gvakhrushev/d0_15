# Complete first-jet boundary of the field-to-instrument variation

**Exact research result, extended 15 October 2026.** This packet classifies
the complete first-jet family of unitary-return maps on the actual constrained
joint field tangent, then tests whether the moving-preparation source fixes
one response from the reference instrument alone. It adds no D0 primitive,
selects no action, and does not claim that the instrument is physically
admitted.

The input is the published v3 moving-preparation source at
[`f1270f63`](https://github.com/gvakhrushev/d0_15/tree/f1270f63cffa5fcfc27b469ff2517d8398d5362a/02_REGISTRY/research/sources/d0_local_record_to_matter_2026-10-14/continuation_v3).
Its exact checker passes 169 controls. That source derives the full first
pullback for a fixed registered count event and allows differentiable return
variations that make formerly commuting returns noncommute. It does not give
a map from a coframe/link variation to those return tangents.

## Complete first-jet family on the actual joint field tangent

Use the full kinematic quotient from
[`A4D_NATIVE_JOINT_FIELD_QUOTIENT.md`](A4D_NATIVE_JOINT_FIELD_QUOTIENT.md),
whose local coordinates are `(q,D,b,m)` and whose exact admissible tangent
image is (5) there. At the constant reference `q_source=q_target=eta`,
`D=I`, choose at every site the tangent

\[
 K=\operatorname{diag}(1,1,0,0),\qquad
 \delta q_{source}=\delta q_{target}=K,\quad
 \delta D=\delta b=\delta m=0.
\]

It satisfies the differentiated edge constraint. It is symmetric,
nonzero, nongauge, tracefree relative to `eta`, and volume-preserving to first
order. It has an actual nondegenerate raw-solder lift for `|t|<1`:

\[
 q(t)=\operatorname{diag}(1+t,-1+t,-1,-1),\qquad
 F(t)=\operatorname{diag}(\sqrt{1+t},\sqrt{1-t},1,1),\qquad
 q(t)=F(t)\eta F(t)^T.
\]

For `v=L^4` sites, fix the unit probe coordinate
\(\xi(q)=(2v)^{-1}\sum_x\operatorname{tr}(K(q_x-\eta))\); then
\(d\xi[K]=1\). This is a test coordinate on the owned field quotient, not a
physical action or selected readout. The registered periodic carrier has
`L` divisible by four; the exact checker uses its smallest size, `L=4`
(`v=256`), rather than a smaller auxiliary torus.

Now fix the two reference returns \(U_{r0}\in U(4)\). For any differentiable
field-to-return map \(U_r:X\to U(4)\), its derivative \(A_r:T_xX\to
M_4(\mathbb C)\) must satisfy
\[
 A_r(v)U_{r0}^*+U_{r0}A_r(v)^*=0.
\]
Equivalently there is a unique real-linear Hermitian-valued map
\(H_r:T_xX\to\operatorname{Herm}(4)\) with
\(A_r(v)=iH_r(v)U_{r0}\). Conversely every such pair \((H_1,H_2)\) is
realized by the smooth unitary germs
\[
 U_r(x)=\exp(iH_r(\chi(x)))U_{r0},
\]
where `chi` is a local chart centered at the reference with derivative the
identity. Thus the entire first-jet family allowed by the current interface
is
\[
 \operatorname{Hom}_{\mathbb R}(T_xX,\operatorname{Herm}(4)\oplus
 \operatorname{Herm}(4)),
\]
of real dimension \(32\cdot66L^4=2112L^4\). Unitarity imposes exactly the
skew-Hermitian tangent condition above and no further restriction. This is
completeness for the declared instrument interface; it is not a claim that
every such map is admitted by D0. On the smallest registered carrier this is
540,672 real first-jet parameters across the two returns.

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

Along the actual quotient path above, so that `xi(q(t))=t`, the complete
first-jet family contains these field-to-return maps for λ=1 and λ=2:

\[
U_r^{(\lambda)}(x)=e^{i\lambda \xi(q(x))H_r}U_{r0}.
\]

Each is unitary, has the same value \(U_{r0}\) at the reference, and its
tangent along the genuine quotient direction K is iλH_rU_{r0}. The registered
event, apparatus, reference density, and probe calibration are identical.
Both tangents are in the v3 instrument class; the v3 source explicitly
allows noncommuting nearby returns.

Let ρ_A(t) be the normalized state conditioned on that same event,
computed from the actual two-outcome channel recursion, and put

\[
\Delta(t)=\sum_{r=1}^2(U_r^{(\lambda)}(q(t))-I)^*
                         (U_r^{(\lambda)}(q(t))-I),
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

The exact receipt also retains the event-normalizer jet along this same field
direction. For the fixed event \(A=\{1,2\}\),

\[
D_\xi P_A(0)=\lambda(189p-117),\qquad
D_\xi\log P_A(0)
=\lambda\left(\frac{6}{71}-\frac{54p}{71}\right)\ne0.
\]

This makes the event-normalization direction response-visible across the
complete free-scale family, in addition to the prepared-cost response below.
If the raw event weights are also identified with the \(\varphi^{-S}\) path
weights, this is the \(D_\xi\log\mathcal N\) term in the partition-corrected
information theorem. That identification and physical D0 admission remain
unproved; this is an exact instrument-interface calculation.

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
normalization derivative, both tangents, and the event-normalizer jet (33 exact
controls). Its receipt is
[`a4d_native_field_instrument_jet_results.json`](certificates/a4d_native_field_instrument_jet_results.json).

## What this resolves

This classifies the complete **instrument-interface first-jet family** and
shows that its free parameters are response-visible: on the actual joint
field tangent K, the prepared scalar cost derivative ranges over all real values
\(\lambda(1644p+17733)/5041\). The reference returns, event, preparation,
and probe calibration do not select λ. The exact missing datum is an
independently owned map from the constrained coframe/link/matter tangent to
the pair of unitary-return Lie-algebra tangents, together with its
refinement-compatibility law. Fixing an overall unit after the fact cannot
recover this map.

The witness is not two claimed D0 physical solutions. Neither completion has
been shown admitted by the D0 core, and the current interface does not yet
provide that admission predicate. The calculation uses a four-dimensional
instrument block and one genuine nongauge tangent in the shared `(q,D,b,m)`
carrier; it does not construct a ten-component stress tensor, a complete
`H+J+R` stationary point, a native refinement, or an Einstein solution. It
therefore closes the mathematical first-jet classification of this interface,
while leaving physical admission and G0 open, along with the positive ОТО
path and the original #310 response-decoupling terminal.

## Typed field-to-readout factorization audit (19 October 2026)

The first-jet space above is a space of candidate maps, not the kernel of one
map. For the declared pointwise output
\(Y=\operatorname{Herm}(4)\oplus\operatorname{Herm}(4)\),
\(\dim_{\mathbb R}Y=32\). With \(\dim T_xX=66L^4\), the family
\(\operatorname{Hom}_{\mathbb R}(T_xX,Y)\) has dimension
\(32\cdot66L^4=2112L^4\); at \(L=4\), this is 540,672 possible jet
parameters. For any one selected \(\Gamma:T_xX\to Y\), rank-nullity instead
gives
\[
\dim\ker\Gamma=66L^4-\operatorname{rank}\Gamma\ge66L^4-32.
\]
At \(L=4\), the lower bound is 16,864. The exact rank and invisible
subspace are not fixed because this owner does not select an admitted
\(\Gamma\). If a different model uses site-indexed outputs, its actual target
dimension must be substituted before applying rank-nullity.

The factorization claim also has a precise dual criterion. Given a physical
first variation \(\alpha=dS_x\in T_x^*X\), a readout covector
\(\tau\in Y^*\) satisfying \(\alpha=\Gamma^*\tau\) exists exactly when
\(\alpha\) vanishes on \(\ker\Gamma\). When it exists, its restriction to
\(\operatorname{im}\Gamma\) is fixed; an extension to all of \(Y\) is unique
exactly when \(\Gamma\) is surjective. Injectivity is neither the existence
criterion nor the uniqueness criterion for \(\tau\). Even if the
state-level readout \(D\pi_h\) is injective on \(T_{\sigma(x)}M\), an
extension of \(\tau\) to all of \(T_y^*Y\) is unique only when that
readout is also surjective. For the declared composite field-to-two-return
type, injectivity is impossible at \(L=4\) because the domain has dimension
16,896 and the target dimension is 32.

If \(\sigma:X\to M\) is the field-to-state map and
\(\pi_h:M\to Y\) is the readout, the physical map is the composite
\(\Gamma=D\pi_h|_{\sigma(x)}\circ D\sigma|_x\). Writing \(D\pi_h[V]\) for
\(V\in T_xX\) skips the state map unless \(X=M\). Likewise,
\(D\sigma[V]=i[H(V),\sigma]\) covers only a unitary-orbit tangent and
preserves every spectral moment of \(\sigma\). There is also a carrier
mismatch in the proposed example: its density is \(3\times3\), while each
owned return generator acts on \(\mathbb C^4\); no channel or representation
connecting those carriers is specified.

This last restriction excludes the proposed three-parameter density example
as a realization of that unitary-return formula. At
\((\eta,\xi,\zeta)=(0,3/5,0)\),
\[
D_\xi\sigma=p^2\begin{pmatrix}0&1\\1&0\end{pmatrix}\oplus0,
\qquad
\operatorname{tr}(\sigma D_\xi\sigma)=\frac65p^4\ne0,
\]
whereas \(\operatorname{tr}(\sigma\,i[H,\sigma])=0\) by cyclicity of trace.
The diagonal-readout example remains a valid abstract illustration that a
functional derivative can fail to factor through a coarse readout; it does not
supply the missing D0 field-to-return map. The conditional full-action
chronology relation is already owned by
[A4D_NATIVE_CHRONOLOGICAL_STATIONARY_DESCENT.md](A4D_NATIVE_CHRONOLOGICAL_STATIONARY_DESCENT.md),
§4; the source from the other retained action terms remains required there.

This correction narrows the next GR obligation: derive the same-history native
map \(\Gamma\), prove that the full action covector annihilates its kernel,
and establish refinement compatibility before interpreting its ten metric
components as a physical source. The jet-family dimension, a tomographic
condition, and the toy entropy do not establish those premises.

Reproduce with

```sh
python3 02_REGISTRY/research/certificates/a4d_native_field_instrument_jet_check.py
```

Use `--write` only to refresh the adjacent receipt after an intentional change.

The checker pins the v3 source and receipt. The adjacent JSON is immutable by
default; `--write` is only for an explicitly reviewed certificate refresh.
It checks the differentiated joint constraint directly in the source/target
convention and uses the smallest registered `L=4` carrier.
The exact replay also revalidates the complete joint-field quotient owner
(41 controls, 51 transitive source pins). Its sole prior owner-hash mismatch
was an appended pair of shift-blindness theorems; the quotient capsule was
recompiled on the current source tree and its compiler output matched the
stored output byte-for-byte. The quotient, instrument first-jet
classification, and physical admission remain distinct scopes.
