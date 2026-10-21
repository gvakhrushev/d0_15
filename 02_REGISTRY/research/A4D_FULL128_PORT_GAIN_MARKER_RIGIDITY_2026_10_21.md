# Full128 port-ratio rigidity across the native cost-marker family

**Date:** 2026-10-21
**Owner:** existing Draft #334, EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE
**Status:** exact necessary compatibility law for the already-owned nonblank port pair. No new Info law, instrument, or physical selection. GR_closed=false.

## 1. Why one-point matching is too weak

The original full128 nonblank port pair has exact Kraus operators

\[
K_{0,k}=pL_k,\qquad K_{1,k}=\sqrt p\,L_k,\qquad p=\varphi^{-1},
\]
with actual port charges \(C_0=1,C_1=2\). The normalized data and every later conditional future at the same \(k\) are identical. The two probabilities are \(q_0=p^2,q_1=p\). These are the original Kraus operators, not a replacement two-outcome detector.

The owned cost marker changes the actual port probabilities to

\[
q_t(0|k)=\frac{p}{p+e^{-t}},\qquad
q_t(1|k)=\frac{e^{-t}}{p+e^{-t}}.
\tag{1}
\]

This is an actual family of marked weights on the same two ports. At \(t=\ln\varphi\) the pair is \((1/2,1/2)\); at \(t=2\ln\varphi\) it is \((p,p^2)\). The marker is a supplied analytic cost transformation; no claim is made that every t is a compulsory physical operation.

## 2. Exact relative-gain law for the three distinct bindings

Write \(\Delta I(t)=I_1(t)-I_0(t)\). Because the actual charge gap is fixed at \(C_1-C_0=1\), the Book weight ratio is

\[
\frac{w_1}{w_0}=\varphi^{-1+\Delta I(t)}.
\tag{2}
\]

### Absolute coherent-amplitude binding

To reproduce the normalized full branch vector, the ratio must be the square-root probability ratio:
\[
\frac{w_1}{w_0}=\sqrt{\frac{q_t(1)}{q_t(0)}}.
\]
Using (1)-(2), the necessary and sufficient relative gain is

\[
\boxed{\Delta I_{\rm amp}(t)
=\frac32-\frac{t}{2\ln\varphi}.}
\tag{3}
\]

Thus
\[
\boxed{D_t\Delta I_{\rm amp}=-\frac1{2\ln\varphi}.}
\tag{4}
\]

This derivative is nonzero even though the actual charge gap is fixed. A field-independent/common amplitude normalizer cannot change either (3) or (4), because it cancels in the branch ratio.

### Absolute scalar-probability binding

If the Book weights themselves must reproduce q rather than its square-root amplitude, then
\[
\frac{w_1}{w_0}=\frac{q_t(1)}{q_t(0)},
\]
and the exact required gain is instead

\[
\boxed{\Delta I_{\rm prob}(t)=2-\frac{t}{\ln\varphi},\qquad
D_t\Delta I_{\rm prob}=-\frac1{\ln\varphi}.}
\tag{5}
\]

### Additional marker on the already executed Kraus branch

If the actual \(K_{j,k}\) already supplies the native Golden amplitude and the Book factor is only an extra multiplier on that branch, preservation of the same normalized coherent state requires equal extra multipliers:
\[
\boxed{\Delta I_{\rm extra}(t)=1,\qquad D_t\Delta I_{\rm extra}=0.}
\tag{6}
\]

Equations (3), (5), and (6) are incompatible as functions of t. This is not a contradiction in the repository: they are three different typed maps. The result is that they cannot be silently interchanged in a single physical valuation.

## 3. A concrete contradiction at two marker settings

At \(t=\ln\varphi\), the same actual port pair is uniform. The three required gains are
\[
\Delta I_{\rm amp}=1,\qquad
\Delta I_{\rm prob}=1,\qquad
\Delta I_{\rm extra}=1.
\]
So a single point cannot distinguish the bindings.

At \(t=2\ln\varphi\), the probabilities are \((p,p^2)\), and the required gains are
\[
\Delta I_{\rm amp}=\tfrac12,\qquad
\Delta I_{\rm prob}=0,\qquad
\Delta I_{\rm extra}=1.
\]
The three bindings now disagree. Therefore a calibration at the uniform point does not extend to the marked family. In particular, the amplitude and scalar bindings have different marker derivatives, and neither derivative can be supplied by a common normalizer.

This two-setting test is exact in the Golden field; it does not rely on floating-point tolerances.

## 4. Closed-loop normalizer carries its own source

For the existing feedback determinant, multiplying a history operator F by a positive common factor \(a(t)\) gives

\[
D_t[-\log\det(I-z\,aF)]
=\operatorname{Tr}\left[(I-zaF)^{-1}z\bigl(a\,D_tF+F\,D_ta\bigr)\right].
\tag{7}
\]

Thus even when a common factor leaves a normalized open-record state unchanged, it generally contributes to the closed-loop Book source. Rescaling z to cancel the \(D_ta\) term changes the physical feedback calibration and is not an algebraic normalization.

For the original nonblank port pair, any proposed full binding must therefore pass both:
- the exact relative-gain law (3), (5), or (6), as appropriate to the claimed map;
- the full closed-loop source (7), including the actual common-factor derivative and the fixed native z.

Matching only the two normalized port probabilities does not pass either test by itself.

## 5. What this closes and what remains open

This result closes the finite algebraic classification of the relative-gain response for the original nonblank full128 port pair across the supplied cost-marker family. It strengthens a one-point port-ratio obstruction into an exact first-source test and shows why a calibration at one t is insufficient.

It does NOT identify which of the three maps Book03 physically uses. Book03's memory-algebra sum, quadratic response, feedback partition and absolute normalizer remain the source of that choice. It does not establish the same map on the distinct N=1 CQ compiler, nor physical admission of the t-family, nor a metric pullback with nonzero Dt. The next physical step is to derive the actual Book03 branch gain and common factor from its definitions and evaluate (7) on the same complete native execution.

No detector, action, coupling, cost or Info law is added. GR_closed=false.
