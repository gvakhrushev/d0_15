# EXP-A4D-STAGGERED-PRIMAL-DUAL-HODGE-CARRIER

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Construct or terminally classify the minimal finite carrier enlargement implied by E-CARTAN2.

The current centered metric alone loses the forward link strain needed by exact first-order Ward covariance. Full \(S_2\) additionally needs non-diagonal/off-site edge-edge Hodge variation.

Repository edits: **NONE**.

## Frozen results

Do not revisit:

- Hodge-weight placement-only repair;
- unmodified forward Cartan;
- the current pointwise metric-only Hodge carrier.

Those classes are already closed by exact no-go controls.

The positive kinematic architecture to preserve is:

\[
d_f=\sum_r\nabla_r^+c_r^\dagger,
\qquad
d_f^2=0,
\]
\[
D_r=A_r\nabla_r^+,
\qquad
A_r=(I+U_r^{-1})/2,
\]
with centered metric readout
\[
\delta m=\operatorname{Sym}\mathcal C_1(d_f\xi)
=
\texttt{symmetricRoleGradient}(N,\xi).
\]

## Candidate carrier

Investigate an explicit pre-centered coframe/link field
\[
e_N
\]
on oriented primal links or equivalent local cell frames.

Its gauge law should retain forward strain:
\[
\delta_\xi e^a=d_f\xi^a.
\]

The existing centered metric is then a derived readout:
\[
m=\operatorname{Sym}\mathcal C_1(e)
\]
or the exact nonlinear analogue.

## Main questions

1. What is the minimal typed carrier for \(e_N\)?
2. How many extra degrees of freedom relative to the 10-component centered metric?
3. Which part is auxiliary Lorentz/frame redundancy?
4. Can the centered metric be recovered exactly for every finite \(N\)?
5. Is the lift from \(m\) back to \(e\) necessarily nonunique because of the Nyquist kernel?
6. Can a first-order Hodge weight on links use the forward strain and satisfy exact Ward covariance?
7. What is the smallest full \(k\)-cell anchoring rule for all 16 exterior states?
8. Does the second-order \(S_2\) route require a dual cell complex?
9. What exact non-diagonal Hodge matrix elements are required by the \(L=3\) no-go?
10. Can a primal/dual Hodge star
   \[
   \star:C^k_{primal}\to C^{4-k}_{dual}
   \]
   be defined locally with bounded stencil?

## Ward target

A positive architecture should make a theorem of the form
\[
D_eS[\delta_\xi e]
+
D_\psi S[G_\xi\psi]
=0
\]
exact or telescoping.

Then determine under what additional condition this descends to pure metric stress conservation:

- \(e\) canonical from \(m\);
- or an \(e\)-equation/constraint;
- or quotient by explicit frame gauge.

Do not silently discard the extra \(D_eS\) term.

## Formalization target

End with a theorem-ready staged package:

- carrier definitions;
- centering map;
- gauge law;
- 1D first-order positive pilot;
- Nyquist no-section theorem;
- smallest 4D primal/dual extension;
- exact future worker boundaries.

## Terminal verdict

Return exactly one:

- \`STAGGERED-HODGE-CARRIER-REACHED\`
- \`STAGGERED-FIRST-ORDER-ONLY\`
- \`PRIMAL-DUAL-HODGE-CARRIER-REQUIRED\`
- \`COFRAME-REDUNDANCY-UNRESOLVED\`
- \`STAGGERED-HODGE-WARD-STILL-NOGO\`

## Deliverable

\`MEMO_45_A4D_STAGGERED_PRIMAL_DUAL_HODGE_CARRIER.md\`
