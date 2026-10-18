# Exact field-pullback boundary for the golden-mode price

**Result.** The three-coin determinant-mode price has an exact, nonzero
derivative along a genuine nongauge tangent of the existing joint field
quotient, once a smooth field-to-unitary map is supplied. Two smooth
unitary-germ completions have the same reference gate, cut, and detector but
different source derivatives. This isolates the missing G0 datum: the D0
core must independently admit and determine the field-to-return map and its
refinement law.

This is a scoped exact boundary result for the current smooth unitary-germ
interface. It is **not** a pair of physical D0 solutions, does not select a
new gate or action, and does not close G0 or derive ОТО.

## Pinned inputs

- [Golden determinant-mode source, §6.58](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md),
  Git blob `4026aad415c581266d1ecb76b9dc88d5a4052306`, SHA-256
  `cff530e4108d8d312e5e9a811c7794ac4ed01988ac3bbf32560367cc2762545a`.
  It derives r=p³/4, the unique filled-P mode, and the action
  S_mode log φ = −2 log w₀ + 2J_r(F) for rank d=1.
- [Joint field quotient](A4D_NATIVE_JOINT_FIELD_QUOTIENT.md),
  Git blob `3ed86bd268808fbde867752a454c0c678b2a8a27`, SHA-256
  `991b42eac645bb7e5e4df55f9be439f8e873b9403b4ff2a6dc1061a49dfe3e2e`.
- [Complete field-to-instrument first-jet boundary](A4D_NATIVE_FIELD_TO_INSTRUMENT_JET_BOUNDARY.md),
  Git blob `e5c168024015db4e216141e2139d2cc1f5d3e419`, SHA-256
  `9e2603039b937d7985da97bc9e4c72a9f433f2363477560806c1bdaee627ae05`.
  It supplies the genuine field tangent and proves completeness only for
  the declared kinematic unitary interface, not physical admission.

## Same base gate, different field source

Let p=(√5−1)/2, φ=p⁻¹, r=p³/4, and w₀=1−p⁶=4p³, as derived in §6.58.
Use the actual nongauge tangent

    K = diag(1,1,0,0),  δq_s=δq_t=K,  δD=δb=δm=0

of the joint quotient, and its owned test coordinate x=ξ(q), with Dξ[K]=1.
This is a trace-free, volume-preserving-to-first-order metric direction;
the coordinate is not a selected physical readout.
On the registered periodic carrier, η=diag(1,−1,−1,−1),
ξ(q)=(2v)⁻¹ Σ_y tr(K(q_y−η)); the actual quotient path
q_s(t)=q_t(t)=diag(1+t,−1+t,−1,−1), D=I, b,m fixed, gives ξ=t.

On one old return/complement pair set

    P = diag(1,0),  Q = I−P
    G = [[√p, −p], [p, √p]]
    R(λx) = [[cos(λx), −sin(λx)], [sin(λx), cos(λx)]].

The two completions are U₀(x)=G and U₁(x)=G R(x). More generally,
U_λ(x)=G R(λx). Each is unitary and all have the same reference value
U_λ(0)=G. The detector still uses the same three golden coins and the same
P,Q; only the unbound smooth field-to-unitary germ varies.

For F_λ=P U_λ* Q U_λ P restricted to ran(P), write F_λ=f_λP. Direct
multiplication gives

    f_λ(x) = (p cos(λx) + √p sin(λx))²
    f_λ(0) = p²
    Df_λ(0)[K] = 2λp√p.

With the §6.58 source J_r(f)=−log(1−rf), the rank-one mode price is

    S_mode(x) log φ = −2 log w₀ + 2J_r(f_λ(x)).

Therefore

    DS_mode(0)[K]
      = 2r Df_λ(0)[K] / (log φ · (1−rp²))
      = λp^(9/2) / (log φ · (1−p⁵/4)).

The fixed completion λ=0 has zero derivative; λ=1 has a strictly positive
derivative. Both share every basepoint quantity fixed above. The result is
response-visible without changing the golden detector or fitting a source
coefficient. Since 1<√5<3, we have 0<p<1<φ and 1−p⁵/4>3/4, so the
displayed derivative is positive for λ=1.

The unique-mode condition remains strict throughout: for any unitary
U_λ(x), 0≤F_λ≤I, so K_good=w₀(I−rF_λ)≥(1−2p⁶)I. Exactly,

    1−2p⁶ = 8√5−17 > 0
    (8√5−17)²−1/2 = (1217−544√5)/2 > 0,
    1217²−5·544² = 1409 > 0.

Thus the source-changing germ does not cross the detector's
K_good²>I/2 uniqueness margin.

## G0 consequence and limit

The determinant theorem supplies the derivative with respect to F; the
joint quotient supplies admissible field tangents; and the unitary interface
permits smooth germs. The present owners do not identify which germ is
admitted by the physical D0 evolution. Hence the displayed derivatives do
not establish physical source nonuniqueness. They show that the base gate
and the §6.58 detector formula alone cannot determine the pullback. Closing
this arrow still requires a native rule (q,D,b,m,record) → U (or F), its
admitted tangent domain, and compatibility under native refinement,
followed by the same program's stationarity law.

The exact checker is
[`check_golden_mode_field_pullback.py`](sources/d0_golden_mode_field_pullback_2026-10-18/check_golden_mode_field_pullback.py).
It verifies the two shared-base completions, the exact first derivative, and
the unique-mode margin in ordinary and optimized Python.
