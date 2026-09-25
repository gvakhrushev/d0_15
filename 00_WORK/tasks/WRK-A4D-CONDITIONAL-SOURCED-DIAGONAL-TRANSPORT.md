# WRK-A4D-CONDITIONAL-SOURCED-DIAGONAL-TRANSPORT

## Class

WORKER

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Objective

Lean-own the theorem-ready **conditional sourced diagonal transport package**
from PR #120.

This worker assumes a supplied relative comparison endomorphism / action
\(\mathfrak J\).  It does not construct or select \(\mathfrak J\).

## Read first

- \`02_REGISTRY/research/MEMO_A4D_DIAGONAL_JUNCTION_OVERLAP_LAW.md\`,
  theorem-ready A–F;
- \`03_FORMALIZATION/D0/Geometry/A4DRoleOverlapTwistedCocycle.lean\`;
- \`03_FORMALIZATION/D0/Geometry/A4DTransportedReferenceMismatch.lean\`;
- affine Cartan path transport owners.

## Preferred module

\`03_FORMALIZATION/D0/Geometry/A4DConditionalSourcedDiagonalTransport.lean\`

Keep path-order conventions literal to the existing \`covariantLin\` owner.

## Mandatory definitions

For \(x=y-r\), define source-fibre data

\[
\bar b_r(y)=L_{x,r}^{-1}b_{x,r},
\]

\[
\bar v_r(y)=L_{x,r}^{-1}v_r(e,x),
\]

\[
\Delta^b_r(y)=b_{y,r}-\bar b_r(y),
\]

\[
\Delta^v_r(y)=v_r(e,y)-\bar v_r(y).
\]

For supplied \(\mathfrak J_y\), define

\[
R^{A/e}_r=\Delta^v_r-\mathfrak J_y\Delta^b_r,
\]

and

\[
a_r=-\bar b_r-\mathfrak J_y\Delta^b_r.
\]

## Mandatory theorem package

### 1. Relative increments are source typed

Own the exact source-site typing and pure-linear covariance under explicit
hypotheses for \(\mathfrak J\).

### 2. Conditional relative defect covariance

If

\[
\mathfrak J'_y=g_y\mathfrak J_yg_y^{-1},
\]

prove

\[
(R^{A/e}_r)'=g_yR^{A/e}_r.
\]

### 3. Gauge calibration

If

\[
\mathfrak J_y\Delta^b_r=\Delta^v_r,
\]

prove

\[
R^{A/e}_r=0.
\]

### 4. Finite seed

Prove \(a_r\) is source typed/covariant and package its exact expansion.

### 5. Predecessor decomposition

For

\[
\rho_r=A^{-1}_{x,r}(v_r(e,x))-v_r(e,y),
\]

prove exactly

\[
\rho_r=a_r-R^{A/e}_r.
\]

### 6. Path source

For a labelled path \(p:y\to y'\), define

\[
S_p=P_pa(y')-a(y).
\]

### 7. Append law

Prove

\[
S_{p++q}=S_p+P_pS_q
\]

with the repository's exact append convention.

### 8. Reverse law

Prove

\[
S_{\bar p}=-P_p^{-1}S_p.
\]

### 9. Sourced solution characterization

Prove

\[
P_p\delta(y')-\delta(y)=S_p
\]

iff

\[
h:=\delta-a
\]

is parallel along the same path.

If straightforward, lift this to “for all labelled paths”.

### 10. Loop kernel

For a basepoint loop \(\gamma\), derive

\[
P_\gamma h(o)=h(o).
\]

Do not introduce a new basepoint selector.

## Optional exact controls

If the APIs make them short, specialize:

- \(b=0\Rightarrow a=0\);
- constant pure shift with \(\Delta^b=0\Rightarrow a=-b\);
- calibrated exact gauge \(\Rightarrow a=\rho\).

These are conditional controls only.

## Firewalls

Do not:

- construct \(\mathfrak J\);
- claim \(\mathfrak J\) exists globally;
- select the parallel/holonomy kernel;
- use observer positivity to define the source;
- start finite E dressing;
- identify \(A=A(e)\);
- touch second jet/stress/time/golden work.

## Exit condition

Lean owns the conditional relative defect, finite diagonal seed,
predecessor decomposition, sourced append/reverse transport, and the exact
“solution = seed + parallel section” characterization, all conditional on a
supplied comparison primitive \(\mathfrak J\).

## GitHub-first flow

Fresh main → lifecycle start → Draft PR → narrow build → incremental
\`D0.All\` → support registration → self-retire → \`Lifecycle: REVIEW\` →
Ready → do not self-merge.

No \`sorry\`, no new axioms, no \`lake clean\`.
