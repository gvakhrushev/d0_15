# EXP-A4D-STAR-TRANSLATION-INVARIANT-ACTION-COMPLETION

Class: \`EXPENSIVE\`
State on registration: \`IN_PROGRESS\`
Parent: \`CTRL-A4D-FULL-AFFINE-SOLDER-GAUGE-QUOTIENT\`

Repository: \`gvakhrushev/d0_15\`
Base: \`main\`
Branch: \`exp/a4d-star-translation-invariant-action-completion\`
Primary artifact: \`02_REGISTRY/research/MEMO_A4D_STAR_TRANSLATION_INVARIANT_ACTION_COMPLETION.md\`
Execution: \`GitHub-first\`

## Why this is EXPENSIVE

The previous pressure tests have closed the obvious symmetry routes:

- the canonical star density is nontrivial under variation;
- its nonlinear proper-Lorentz quotient survives;
- the explicit observer-completed affine translation law composes and has the
  exact flat chart, but is not a symmetry on curved backgrounds;
- the entire first Cartan-Hodge on-shell gauge-law class is rank-obstructed.

The next uncertainty is therefore whether the **action itself** admits a
minimal, internally forced affine/solder completion rather than another gauge
law.

## Fixed gauge law

Do not vary the transformation law in this task.

Use the observer-completed finite affine node action already constructed in the
full-affine boundary packet:

\[
L'_{x,r}=g_x L_{x,r}g_{x+r}^{-1},
\]

\[
\tau_{x,r}=c_x-L'_{x,r}c_{x+r},
\]

\[
n'_x=g_xn_x,
\]

\[
\Theta'_{x,r}
=
\Theta_{x,r}g_x^{-1}
+
\tau_{x,r}^{T}h_{n'_x}.
\]

The task asks whether the action can be completed so that this fixed law is an
exact finite symmetry.

## Starting action

\[
S_\star
=
\sum_{x,S}
\epsilon_S
G_2\!\left(
B_{S^c}(e,x),
\star\,\mathfrak b\!\left(
\tfrac12(P_S-P_S^{-1})
\right)
\right).
\]

Its coefficient is an overall scale already separated from structural moduli.

## Owned completion data to audit first

Before inventing new tensors, read and reuse:

- \`ArchiveAffineCartanConnection\`:
  affine open curvature, open torsion, based holonomy shift and their exact
  affine gauge laws;
- \`MEMO_A4D_RELATIVE_AE_COMPARISON_PRIMITIVE.md\`:
  the rank-stratified partial comparison
  \[
  J_y^{can}:U_y\to V_y,
  \]
  the linear relation \(\mathscr R_y\), vertical defect \(M_y\), and relative
  residual
  \[
  R_r^{A/e}
  =
  \Delta^v_r-J_y^{can}\Delta^b_r;
  \]
- the labelled-reference / solder-Cartan mismatch packets and their flat,
  exact-gauge, pure-shift, curl, harmonic, Nyquist and L=3 corner controls.

Do not insert continuum Nieh-Yan, Einstein-Cartan, teleparallel, or torsion
squares merely by analogy.

## KILL-FIRST gates

### 1. TYPE

Classify oriented scalar cell terms which can actually be formed from the owned
objects at one common fibre/cell.  Track base degree and internal degree
separately.  Reject endpoint-mismatched pairings before coefficient fitting.

### 2. REPRESENTATION / Hom-space

Within the lowest-locality class (one cell / one plaquette / one relative
A/e defect), classify all proper-Lorentz and spatial Role-natural scalar
channels.  Determine the action-family dimension before imposing translation
symmetry.

### 3. AFFINE-TRANSLATION LAW

Compute the exact finite transformation of each candidate under the fixed
observer-completed affine node action.  In particular, audit the inhomogeneous
laws

\[
T'_{\rm open}
=
g_x T_{\rm open}
-
F'_{\rm open}\,c_{\rm far}
\]

and

\[
t'_{\rm based}
=
g_x t_{\rm based}
+
(I-P')c_x.
\]

Do not call either one a covariant torsion vector unless its inhomogeneous term
is cancelled by an owned relative A/e object.

### 4. CANCELLATION / MODULI

Solve exactly for coefficients \(\lambda_i\) in

\[
S_{\rm comp}
=
S_\star+\sum_i\lambda_i S_i
\]

such that

\[
S_{\rm comp}[h\cdot z]=S_{\rm comp}[z]
\]

for the fixed affine action.

Determine:

- no solution;
- unique completion up to the already existing overall action scale;
- or a residual modulus/family.

Do not call a fitted finite witness a theorem; use enough exact controls to
classify the candidate space.

### 5. FLAT REGRESSION

Any survivor must be pressure-tested against the already accepted flat
quadratic result.  Compute whether the completion:

- leaves the flat Hessian unchanged;
- modifies only the four forward-coframe nulls;
- changes the rank-24 auxiliary connection block;
- changes the generic effective rank 6 or the three Lorentz-null rank drops.

Track the new \(d_A,d_E,d_P\) separately.

### 6. INDEPENDENT-AFFINE-SHIFT CONTROL

A constant pure affine shift must remain distinguishable from an exact
translation gauge unless the completion itself proves it gauge.

Do not erase independently owned shift data by setting \(b=e\).

### 7. RELATIVE-A/E RANK STRATA

If the completion uses \(J^{can}\) or \(R^{A/e}\), handle rank changes and
vertical relation \(M_y\) explicitly.  Do not silently extend a partial map to
all of \(V_y\).

## Exact controls

At minimum:

- flat;
- exact translation-gauge chart;
- pure independent affine shift;
- the curved \(-2/3\to-4/3\) witness from the full-affine packet;
- genuinely site-dependent proper-Lorentz frame;
- coframe-only L=2 Nyquist;
- L=3 off-diagonal corner;
- one nonzero affine open-torsion/curvature witness where the inhomogeneous
  torsion term is visible;
- one rank-drop relative-A/e example.

Use exact rational/symbolic arithmetic.

## Desired terminals

Positive unique:
\[
\texttt{STAR-AFFINE-TRANSLATION-INVARIANT-ACTION-COMPLETION-UNIQUE-UP-TO-SCALE}.
\]

Positive family:
\[
\texttt{STAR-AFFINE-TRANSLATION-INVARIANT-ACTION-COMPLETION-HAS-MODULUS}.
\]

Negative:
\[
\texttt{STAR-AFFINE-TRANSLATION-INVARIANT-ACTION-COMPLETION-NOGO-IN-MINIMAL-OWNED-CLASS}.
\]

A negative result must say whether the missing ingredient is a new scalar
density, a full-affine extension of the relative A/e relation, a
junction/overlap primitive, or a broader path/cell object.

## Scope

Research only. No Lean source edits, no claims/release promotion, no
BOOK/public edits. No continuum Einstein/torsion/diffeomorphism/time/wave
interpretation.

## Lifecycle

Open Draft before substantive research. Before Ready, self-retire the EXPENSIVE
task from manifest/status and remove this executable brief, retaining durable
memo/certificates.

## Handoff

PR number, terminal verdict, action-family dimension/moduli result, exact
certificate result, and one remaining blocker/fork. Do not self-merge.
