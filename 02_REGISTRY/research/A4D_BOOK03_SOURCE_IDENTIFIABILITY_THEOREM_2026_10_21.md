# Book03 source identifiability: relative branch data plus one absolute jet

**Date:** 2026-10-21  
**Owner:** existing Draft #334. Consumes the native full128 branch-binding and cost-marker results. No new Info law or physical admission. GR_closed=false.

## 1. Exact finite identifiability theorem

Let \(\Omega\) be a finite connected support of actual native histories. Write the positive Book branch weight as
\[
w_\omega(y)=\varphi^{-C_\omega(y)+I_\omega(y)}.
\]
Assume the proposed native map supplies the relative weight ratios
\[
R_{\omega\eta}(y)=w_\omega(y)/w_\eta(y)>0
\]
for every edge of a connected graph on \(\Omega\). Then the relative data determine all \(w_\omega\) up to exactly one common positive factor \(a(y)\):
\[
w_\omega(y)=a(y)\widehat w_\omega(y).
\]
This is the only ambiguity: along a spanning tree all ratios determine \(\widehat w\), and every other edge is a cycle-consistency check. If a cycle product is not one, no branch-weight assignment exists.

Equivalently, the gains satisfy
\[
I_\omega-I_\eta
=C_\omega-C_\eta+\log_\varphi R_{\omega\eta}.
\tag{1}
\]
Thus the relative gains and their first jets are uniquely determined by the ratios and actual charge ledger. The common scalar remains:
\[
I_\omega=C_\omega+\log_\varphi\widehat w_\omega+J(y),
\qquad
a(y)=\varphi^{J(y)}.
\tag{2}
\]

**Minimal-data corollary.** On a connected positive support, the full first source is uniquely determined iff the relative ratio jets, the actual charge jets, and one absolute anchor \(J(y_0),DJ(y_0)\) (or equivalent absolute norm and its first jet) are fixed. A value-only anchor determines the price at \(y_0\) but does not determine its source.

This is a finite graph theorem, not a choice among amplitude, probability, or extra-marker bindings. Those are different possible sources of the ratio data \(R\); the theorem says what remains after any one is actually derived.

## 2. The closed loop observes the common mode

Let \(F(y)\) be the actual closed-history operator assembled from the native branch weights, and let the common factor enter as \(F_a=a(y)F_0(y)\). At fixed native \(z\in(0,1)\),
\[
J_{\rm loop}(y)=-\log\det(I-z a(y)F_0(y)).
\]
Its full derivative is
\[
\boxed{
DJ_{\rm loop}
=\operatorname{Tr}\left[
(I-zaF_0)^{-1}z\left(a\,DF_0+F_0\,Da\right)
\right].
}
\tag{3}
\]
The second term is the common-mode source. It is generally nonzero even when every normalized open-history ratio is unchanged. Therefore relative branch data cannot determine the complete Book source without the absolute anchor jet or a separate native rule that determines it.

The same statement holds for the original full128 port pair: the cost-marker ratio fixes the relative gain law, but a field-dependent common factor still contributes to the true closed-loop determinant. Rescaling \(z\) to cancel it is a change of the physical feedback calibration, not a gauge choice unless Book03 independently proves that equivalence.

## 3. Original port witness: the ratio jet is fixed, the absolute source is not

For the actual nonblank ports,
\[
K_{0,k}=pL_k,\qquad K_{1,k}=\sqrt p\,L_k,\qquad
(C_0,C_1)=(1,2),
\]
and the supplied marker family is
\[
q_t(0|k)=\frac{p}{p+e^{-t}},\qquad
q_t(1|k)=\frac{e^{-t}}{p+e^{-t}}.
\]
The three typed candidate ratios already consumed in the parent are incompatible as functions of \(t\):
\[
\Delta I_{\rm amp}=\frac32-\frac{t}{2\ln\varphi},\quad
\Delta I_{\rm prob}=2-\frac{t}{\ln\varphi},\quad
\Delta I_{\rm extra}=1.
\]
Their derivatives are distinct. This is an exact test of relative gain, not yet the physical selection of the Book map.

Even after the correct ratio law is derived, the common \(J(t)\) in (2) is not determined by that law. Its contribution to (3) must be calculated from the original memory-algebra sum, quadratic response and feedback partition. It may not be set to zero because it cancels in normalized readout probabilities.

## 4. Necessary/sufficient finite gate for source recovery

For a proposed physical Book03 binding on one admitted complete execution, the finite source is identified exactly when all four conditions hold:

1. **Cycle consistency:** every cycle product of the proposed native relative ratios is one.
2. **Actual relative jet:** the ratios and their first derivatives agree with the full original branch operators and actual cost ledger.
3. **Absolute anchor jet:** the native memory-algebra/quadratic response determines the common factor \(a\) and \(Da\), or equivalently \(J,DJ\), on the same retained carrier.
4. **Loop source:** substituting those values into (3), with the actual fixed \(z\), reproduces the original closed-feedback source including the complementary cut.

Necessity follows from equality of the actual weights and differentiation of the actual determinant. Sufficiency follows by reconstructing all weights from a spanning tree, using the anchor to fix their common factor, then applying the exact determinant derivative. No separate entropy surrogate is needed.

After this gate, the reconstructed source must still be compared against the 16+24+2 native field source on the same execution and admitted variation image. Passing source recovery is not itself the Einstein equation, the physical selection of the execution, a refinement theorem, or GR closure.

## 5. What the next calculation must extract from Book03

The unresolved object is now minimal and explicit: from the original sections 03.3.0–03.3.0a, 03.8, 03.10(c)-(f), and the actual closed-memory loop, calculate (i) the native branch-ratio cocycle \(R_{\omega\eta}\), including its phase/amplitude typing, and (ii) one absolute normalizer and its first jet on the same complete history support. Then test cycle consistency and equation (3) without altering \(z\), deleting work/clock/reference, or replacing the full128 tape with the N=1 CQ compiler.

If the native memory algebra does not define such an absolute scalar jet, the correct result is non-identifiability of the source from the supplied Book data—not permission to choose a convenient one. GR_closed=false.
