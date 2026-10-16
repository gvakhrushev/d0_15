# Moving preparation as a golden comparison on the D0 Role index — 2026-10-16

This result derives the v3 channel coefficients from the existing D0 golden
gate, constructs the exact finite-matrix representation of the owned cochain
shifts on the full site × Fock basis, and specializes the failure effect to
those native shifts. It does not admit the controlled composition or the
count-window event as a physical D0 evolution.

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

## Exact native shift matrices

The D0 carrier has the literal type `Role = Dyad × Dyad`, with four elements,
and its owned flat shifts are `cochainForwardShift N r`. The capsule represents
each shift by the permutation matrix on the complete basis
`ArchiveCochainBasis N = ArchiveRolePhaseGroup N × ArchiveFockState`. The
permutation is \((x,S)\mapsto(x+\mathrm{roleStep}(r),S)\), so the Fock label is
retained. Lean proves that matrix multiplication agrees with
`cochainForwardShift N r` on every cochain and that each shift matrix is
orthogonal. The return family is therefore an exact matrix representation on
the full finite carrier, with no carrier truncation or fitted operator.

The general Role-indexed failure-effect theorem now applies to these four
actual shift matrices. With the v3 instrument's normalized four-Role average,

\[
A_{0,r}=\tfrac12 K_0(U_{N,r}),\qquad
A_{1,r}=\tfrac12 K_1(U_{N,r}),
\]

which is the submitted
\(A_{0,r}=(pI+p^2U_{N,r})/\sqrt4\) and
\(A_{1,r}=ap(U_{N,r}-I)/\sqrt4\). For an orthogonal return, the two outcomes
retain the complete trace because

\[
K_0^TK_0+K_1^TK_1=pI+p^2U^TU=I.
\]

Summing the failure effects over all four retained Role labels gives the
exact finite-carrier result

\[
E_N=\sum_r A_{1,r}^T A_{1,r}
=\frac{p^3}{4}\sum_r(U_{N,r}-I)^T(U_{N,r}-I).
\]

Identifying this full carrier formula with the submitted \(L\)-torus Fourier
normalization \(\Delta_0=L^2\sum_r(U_r-I)^T(U_r-I)\), and deriving its Fourier
spectrum and count-window response, remain separate steps. The earlier
site-only eigenvalue formula is not promoted by this matrix representation.

The normalized counting factor \(1/4\) is the v3 instrument's weighting of
the four Role labels. D0 owns the four-element Role set and its translations;
whether the full physical apparatus prepares and traces those labels with
this counting weight is still open.

## What this closes and what remains

The v3 first-variation and interval results now have a specific gate-derived
operator candidate, with its native shift matrices no longer conditional. The
Kraus coefficient is fixed by the owned gate and the finite-carrier effect is
the sum of the four Role-return differences. The source package's verified
moving-state derivative, event normalization and \(L=8\) bounds apply to its
declared finite instrument as mathematics; physical admission of that
instrument remains open.

The following are not derived by this weld:

- joint physical admission of the controlled returns, retained outcome
  registers and four-Role averaging;
- an owner-derived rule selecting the fixed event
  \(l\leq\#1\leq u\) at each refinement level;
- the coordinate/intertwiner from this full site × Fock matrix effect to the
  submitted site-only \(L\)-torus Fourier normalization;
- a map from the admitted full preparation and its variations into the
  complete constrained \((q,D,b,m)\) tangent;
- the common full \(H+J+R\) action, physical Ward identity, and source
  comparison with \(\rho_0\) on all ten metric slots and 24 link directions;
- native on-shell stationarity, a curved joint solution, soundness/recovery,
  or GR.

The next proof is to construct the comparison and fixed count event from an
existing retained-record owner, without adding a selector; then differentiate
that admitted construction along the full constrained tangent and compare its
source with \(\rho_0\). If the existing owners do not admit that composition,
this route is closed without promoting the finite-carrier operator theorem to
physical D0.

Evidence is in
`certificates/a4d_moving_preparation_golden_interferometer.lean`, its compiler
output and companion JSON receipt/checker. The independent v1/v2/v3 replay
remains recorded in
`a4d_local_record_to_matter_intake_replay_2026-10-16.json`.
