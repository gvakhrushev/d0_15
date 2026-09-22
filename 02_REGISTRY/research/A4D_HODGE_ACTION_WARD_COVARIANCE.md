# E-HWARD — Hodge Action Ward Covariance

CONTROL disposition: **ACCEPT AS RESEARCH / HODGE-WARD-DISCRETE-LEIBNIZ-NOGO**

Source memo: MEMO_41_A4D_HODGE_ACTION_WARD_COVARIANCE.

For the full-metric Hodge actions
\[
S_D=\langle\psi,D_m\psi\rangle_{W_m},
\qquad
S_2=\frac12\langle D_m\psi,D_m\psi\rangle_{W_m},
\]
the requested exact Ward identity fails under the **unmodified forward CAR Cartan transformation** together with the reconstructed centered metric variation.

The obstruction already appears for constant metric and constant vector field. Then
\[
K_N\xi=0,
\qquad
\dot W_m[K_N\xi]=0,
\]
but the forward generator is
\[
G_\xi=L\sum_r\xi^r(U_r-I),
\]
whose symmetric part contains
\[
L(U_r^{-1}+U_r-2I).
\]
This produces a genuine periodic bulk quadratic defect on every nonconstant mode. It is not a boundary/telescoping term.

Therefore no site/link/cell/corner placement of the Hodge weight can repair the Ward identity while the matter transformation remains the same forward Cartan generator.

Exact small-lattice controls on the \(L=3\) cycle give nonzero joint variations:

- \(S_2\) control: \(-81\);
- \(S_D\) 0+1 block control: \(-324\).

The failure is the shifted discrete Leibniz defect.

A transformation-level repair remains possible. The first candidate inserts the exact centering operator
\[
A_r=(I+U_r^{-1})/2
\]
into the contraction:
\[
\iota_\xi^{cen}=\sum_rM_{\xi^r}A_rc_r.
\]
For constant \(\xi\), this yields centered transport on 0-forms and removes the constant-vector non-skew defect, while preserving the plausible route to coframe reconstruction. Variable-\(\xi\) covariance, \(d\)-commutation and exact Cartan reconstruction remain open. Flux-split alternatives are also possible but are not yet owned Cartan operators.

Terminal result:
\[
\boxed{\texttt{HODGE-WARD-DISCRETE-LEIBNIZ-NOGO}}.
\]
