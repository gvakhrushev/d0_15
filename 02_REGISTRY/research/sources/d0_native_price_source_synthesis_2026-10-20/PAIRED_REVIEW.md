# Independent review of inverse-paired Golden feedback and its reference budget

Read-only source-bookkeeping review for existing #334. Reviewed `paired_feedback.md`, particularly §8, against Book03 §03.3.2 and `A4D_NATIVE_COMPOSED_FEEDBACK_DYNAMICS.md` §§1–5. This review does not replay the new curved whole-HJR branch and does not publish a duplicate exclusion result.

**Verdict:** the inverse-paired cancellation, coefficient and stated smooth small-face budget are correct under their stated matrix/admission/accounting premises. No missing σ-independent term was found inside this WHOLE-WORD feedback scalar. A separate per-inner-Julia feedback charge is not compulsory in the Book/owners examined. It would materially change the budget if selected, and its actual source can be computed exactly.

## 1. Independent block and source calculation

Write R=[[σS,D],[-D,−σS]], S^T=−S, D=sqrt(I+σ²S²), and W=diag(V,V^T), V^TV=I. The Golden outer comparison has leakage ap(W−R), hence

    F=p³(2I+RW−W^TR).

Direct multiplication, without assuming [S,V]=0 or [D,V]=0, gives

    F−2p³I = p³ [[σ(SV−V^TS),  DV^T−V^TD],
                   [VD−DV,      σ(VS−SV^T)]].           (1)

Thus at σ=0, D=I and F=2p³I EXACTLY for every V. Both archive arms remain. This is not cancellation of two scalar prices and uses no negative probability or discarded outcome.

For any real skew S,

    Tr(F−2p³I)=4p³σ Tr(SV).                             (2)

Let a_z=1−2zp³. At V=I and dV=K,

    dS_feedback=(4zp³σ/a_z)Tr(SK).

The supplied full-CAR dual moment is Tr(S_B|_(σ=1) K(X))=4p²Tr_4(BX). Therefore

    dS_feedback=(16σzp^5/a_z)Tr_4(BX)
               =−(32σzp^5/a_z)df.                      (3)

The doubled coefficient in structural §8 is correct. For the normalized retained input I64/64, dividing (2) by64 gives dr_pair=−(σp^5/2)df, also correct. The fixed binary code relative-source coefficient in §7 is consistent with the original prior(p,p²).

For the complete variation, δS=Tr[(I−zF)^−1(Fδz+zδF)], with δF obtained by differentiating EVERY factor in (1), including D and the reference. Its derivative is uniquely fixed by

    D δD+δD D=σ²(S δS+δS S)

when σ is fixed; if σ moves, its two additional σδσ S² terms are retained. Structural §4 writes the same identity with σ absorbed into S_B. No coframe/reference derivative is missing.

Let V=I+O_C²(h²), S=O_C²(1), and σ fixed on each field chart. Then D−I=O_C²(σ²), so (1) is O_C²(σh²). Equation (2) fixes its first trace; the relative-Julia linearization error contributes O_C²(σh⁴), and the logarithm remainder contributes O_C²(σ²h⁴). Thus the claimed uniform error O_C²(σh⁴+σ²h⁴) is valid. Transpose pairing must be the ACTUAL inverse of the same implemented V. Independently approximating an inverse does not inherit exact cancellation automatically.

Moving operational Euclideanizing frame T contributes to both B and P. Trace(Btilde F(Ptilde))=Trace(BF(P)) is exact, including its mixed observer derivatives. This verifies the leading observer cancellation. It does not turn an arbitrary finite operational remainder into an exactly Lorentz-invariant functional.

## 2. Is a separate −logdet compulsory for each inner Julia gate?

**No such compulsory per-factor rule occurs in the Book03 feedback definition or the composed-feedback owner examined.** Book03 prices F_N=P_N U_N^dagger Q_N U_N P_N for the declared whole operation and cut. The composed owner explicitly applies this SAME scalar to composed Golden words. Its exact examples prove nonadditivity: for one retained dimension,

    S_z(G)=−log(1−zp²),
    S_z(G²)=−log(1−4zp³),

and S_z(G²) is generally NOT 2S_z(G). Therefore an extra sum of internal-cut determinants cannot be inferred simply by factoring the whole word. That sum would be an additional accounting choice for genuinely priced physical cuts/operations, not a consequence of determinant multiplicativity: the feedback pencils are not multiplied by word composition.

This does not make primitive execution free. Book03 separately makes actual history Cost additive; the original fixed F/R word charges and real preparation/compiler/inverse/clock work remain. Their source depends on the actual admitted implementation. The present evidence supports allowing the whole-word feedback construction as a mathematical candidate; it does not prove that this scalar alone is the selected complete price. Absence of a derived compulsory inner determinant is neither a ban on the apparatus nor a proof that no further physical charge exists.

There is a useful exact hostile calculation if such an inner determinant IS independently charged. For J_(pΛ(P)), its natural-cut feedback is

    F_inner=I−p²Λ(P)^TΛ(P).

Set P(t)=exp(tX), Y=dΛ(X), and d_z=z_inner p²/(1−z_inner p), with 0<z_inner<1. At t=0 the first source is zero, since TrY=0, but the exact second derivative is

    S_inner''(0)=−4 d_z(1−d_z) Tr[H(Y)²],
    H(Y)=(Y+Y^T)/2.                                   (4)

It is nonzero for boosts, and is identically zero on an exactly compact/unitary transport family. For P_h=exp(h²X), an inner boost price therefore has a σ-independent O(h⁴) field source. Natural-cut prices of J and J^T have identical singular spectra, so separately charging both inverse arms doubles this term rather than cancelling it. Under σ=h³ its ratio to σh² is O(h^−1). This is a concrete conditional failure mode, not an already imposed Book rule.

## 3. Reference payment: correct scope, and a stronger coherent option

The natural-cut pointer formula q_upper,j=σ²r_j and q_lower,j=1/d−σ²r_j is correct for the specified independent reference input. Its Shannon derivative is O(σ²(1+|logσ|)); C² may fail at probability births. The original warning about measuring inside the coherent data word is necessary and correct. An independent calibration execution avoids disturbing the data, but its charge is not automatically the work charged for the reference used inside the main word.

The separate note `quantum_reference.md` proves a stronger option with the full coherent reference output, no dephasing and all quantum blocks retained. For a FIXED faithful block-diagonal code/reference operator μ in the natural port cut,

    D(ρσ||μ)=constant−(σ²/d)Tr[S0S0^T(logμ_U−logμ_L)].  (5)

It is exactly quadratic and C² even at zero pointer entries; σ=h³ then gives O(h) relative reference source. This is a conditional relative-price theorem, not selection of physical Info.

Block diagonality is a real premise: the same note gives an explicit faithful off-block μ with a nonzero O(σ) coframe source. More generally the complete coherent reference state changes at orderσ. Thus an O(σ²) pointer budget cannot be asserted for an arbitrary full quantum payment functional.

## 4. The remaining implementation error relevant to this budget

Choosing σ=p^(3k) is valid native integer arithmetic and fixes σ during field variation. It does not by itself construct a literal finite word realizing the moving quarter turn. A compiler approximation must preserve the structural identities (actual inverse pairing and quarter-turn reference) or control the induced complete source defect to o(σh²). Fixed gate counts have zero coframe derivative only when genuinely fixed on the chart; their own clock/preparation equations are not thereby solved.

This is the concrete acceptance boundary. Within it, §8 removes the previously unavoidable one-sided h⁴ noise and permits the stated σ=h³ comparison without a counterterm. Nothing in the examined Book forces an additional per-inner-Julia determinant that would automatically invalidate that result.
