# Moving preparation as a golden comparison on the D0 Role index — 2026-10-16

This result derives the v3 channel coefficients from the existing D0 golden
gate and proves the failure effect for a return-matrix family indexed by the
literal type `D0.Role`. It does not yet construct a faithful finite-matrix
representation of the owned cochain shifts, or admit the controlled
composition and count-window event as a physical D0 evolution.

## Operator identity

Let the owned gate be

\[
G=\begin{pmatrix}a&-p\\p&a\end{pmatrix},
\qquad a^2=p,\qquad p+p^2=1.
\]

For a return operator \(U\) on the field carrier, lift the two control ports
to the carrier and form

\[
\mathcal C(U)=G^T\begin{pmatrix}I&0\\0&U\end{pmatrix}G.
\]

Its two outputs from the blank first port are

\[
K_0(U)=a^2I+p^2U=pI+p^2U,
\qquad K_1(U)=ap(U-I).
\]

The Lean capsule proves this operator-valued formula, proves its scalar
specialization is exactly
`D0.Representation.GoldenOrderInterferometer.output`, and proves the failed
port effect

\[
K_1(U)^T K_1(U)=p^3(U-I)^T(U-I).
\]

This uses the actual gate matrix. It adds no splitter angle or fitted
coefficient. The controlled comparison \(\operatorname{diag}(I,U)\) is the
operator-valued lift being tested; physical admission of that controlled
operation remains a separate obligation.

## The v3 channels and native energy

The D0 carrier has the literal type `Role = Dyad × Dyad`, with four elements,
and its owned flat shifts are the `cochainForwardShift N r` operators. For any
Role-indexed family of return matrices \(U_r\), the Lean capsule proves the
failure-effect formula directly over `D0.Role`. If the matrices are shown to
represent the four `cochainForwardShift N r` returns, the result specializes
to the candidate comparison below. The capsule does not yet construct or
prove faithful that finite-matrix representation.

With the v3 instrument's normalized four-Role average,

\[
A_{0,r}=\tfrac12 K_0(U_r),\qquad A_{1,r}=\tfrac12 K_1(U_r),
\]

which is exactly the submitted
\(A_{0,r}=(pI+p^2U_r)/\sqrt4\) and
\(A_{1,r}=ap(U_r-I)/\sqrt4\). For an orthogonal return,

\[
K_0^TK_0+K_1^TK_1=pI+p^2U^TU=I,
\]

so the two outcomes retain the complete trace. Summing the failure effects
over all four retained Role labels gives

\[
E=\sum_r A_{1,r}^T A_{1,r}
 =\frac{p^3}{4}\sum_r(U_r-I)^T(U_r-I).
\]

Under that still-unproved shift-to-matrix identification, with the v3
flat-energy notation
\(\Delta_0=L^2\sum_r(U_r-I)^T(U_r-I)\),

\[
E=\frac{p^3}{4L^2}\Delta_0.
\]

For the periodic Fourier realization of those translations its eigenvalue is
\(e_k=p^3\sum_{r=0}^3\sin^2(\pi k_r/L)\). Conditional on the unproved
identification, the finite count preparation filters the spectrum of the
Role-translation energy. The gate fixes the scale of this candidate filter.

The normalized counting factor \(1/4\) is the v3 instrument's weighting of
the four Role labels. D0 owns the four-element Role set and its translations;
whether the full physical apparatus prepares/traces those labels with this
counting weight is part of the still-open admission test.

## What this closes and what remains

The v3 first-variation and interval results now have a specific gate-derived
operator candidate, conditional on the shift-to-matrix identification. The
Kraus coefficient is fixed by the owned gate and the proposed Laplacian is
the sum of the Role-return differences. The source package's verified
moving-state derivative, event normalization and \(L=8\) bounds apply to its
declared finite instrument as mathematics.

The following are not derived by this weld:

- joint physical admission of the controlled returns, retained outcome
  registers and four-Role averaging;
- a faithful finite-matrix representation/intertwiner identifying the
  abstract \(U_r\) in the capsule with each owned `cochainForwardShift N r`;
- an owner-derived rule selecting the fixed event
  \(l\leq\#1\leq u\) at each refinement level;
- a map from the admitted full preparation and its variations into the
  complete constrained \((q,D,b,m)\) tangent;
- the common full \(H+J+R\) action, physical Ward identity, and source
  comparison with \(\rho_0\) on all ten metric slots and 24 link directions;
- native on-shell stationarity, a curved joint solution, soundness/recovery,
  or GR.

The next proof is now sharply stated: construct the above comparison and
fixed count event from an existing retained-record owner, without adding a
selector; then differentiate that admitted construction along the full
constrained tangent and compare its source with \(\rho_0\). If the existing
owners do not admit that composition, this specific route is closed without
promoting the conditional count-filter theorem to physical D0.

Evidence is in
`certificates/a4d_moving_preparation_golden_interferometer.lean`, its compiler
output and the companion JSON receipt/checker. The independent v1/v2/v3
replay remains recorded in `a4d_local_record_to_matter_intake_replay_2026-10-16.json`.
