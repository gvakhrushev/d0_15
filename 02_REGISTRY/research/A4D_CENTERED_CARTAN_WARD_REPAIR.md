# E-CARTAN2 — Centered Cartan Ward Repair

CONTROL disposition: **ACCEPT AS RESEARCH / FLUX-CARTAN-EXTRA-PRIMITIVE-REQUIRED**

Source memo: MEMO_43_A4D_CENTERED_CARTAN_WARD_REPAIR.

The centered-contraction candidate
\[
\iota_\xi^{cen}=\sum_rM_{\xi^r}A_rc_r,
\qquad
A_r=(I+U_r^{-1})/2,
\]
is the correct kinematic repair of the constant-vector defect.

It preserves exactly:

- constant-vector reduction to centered transport;
- flat skew-adjointness for constant transport;
- \([d_f,\mathcal L_\xi^{cen}]=0\);
- degree preservation;
- constant coframe identity;
- exact reconstruction to \`symmetricRoleGradient\`.

But the current pointwise full-metric Hodge carrier still fails the variable-\(\xi\) Ward identity through the centered shifted-product remainder.

A scalar flux-split generator can cancel the zero-form Hodge-volume defect exactly, but its natural edge contraction sends a constant coframe to
\[
B\xi,
\qquad
B=(2I+U+U^{-1})/4=A^*A,
\]
rather than \(\xi\). The operator \(B\) has an even-\(L\) Nyquist kernel.

More strongly, exact \(L=3\) one-role elimination proves that on the present \(0\oplus1\) pointwise Hodge block there is no hidden degree-preserving generator satisfying simultaneously:

- Cartan scalar behavior;
- \(d_f\)-commutation;
- exact centered coframe reconstruction;
- Ward covariance for nonconstant \(\xi\).

This no-go holds for both the first-order \(S_D\) and positive second-order \(S_2\) actions.

There is a sharp first-order positive result. If the one-form Hodge weight varies with the **forward link strain**
\[
d_f\xi
\]
rather than the centered vertex strain \(D\xi\), centered contraction gives exact 1D first-order Ward covariance. Since
\[
D=A\,d_f
\]
and \(A\) is noninvertible on even-\(L\) Nyquist modes, that forward strain cannot be recovered canonically from the current centered metric.

Hence the smallest honest finite repair is a pre-centered staggered coframe/link-metric carrier. For the full \(S_2\) route, diagonal staggered weights remain insufficient; the first algebraic escape requires non-diagonal/off-site edge-edge Hodge variation, naturally suggesting a primal/dual doubled Hodge operator.

Terminal result:
\[
\boxed{\texttt{FLUX-CARTAN-EXTRA-PRIMITIVE-REQUIRED}}.
\]
