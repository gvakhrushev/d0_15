# WRK-A4D-OBSERVER-QUADRATIC-REFERENCE-NOGO

## Class

WORKER

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Objective

Lean-own the exact scoped observer-positive quadratic obstruction from PR #117.

The theorem is only about the canonical background-independent local quadratic

\[
E_{\alpha,\beta}(\delta)
=
\alpha\|b+\delta\|^2
+
\beta\|\delta\|^2,
\qquad
\alpha,\beta\ge0.
\]

It is not a no-go for nonlinear or sourced overlap functionals.

## Read first

- \`02_REGISTRY/research/MEMO_A4D_LABELLED_REFERENCE_SELECTION_PRINCIPLE.md\`,
  especially §§8–10 and theorem-ready F/G;
- the observer-positive form owner from PR #103;
- RoleSpace basis/vector owners.

## Preferred module

\`03_FORMALIZATION/D0/Geometry/A4DObserverQuadraticReferenceNoGo.lean\`

## Formalization strategy

Prefer an exact scalar hostile ray first.

Fix one nonzero Role basis vector \(b\) and restrict to

\[
\delta=t\,b.
\]

At the rest observer the energy reduces to a positive scalar multiple of

\[
E_{\alpha,\beta}(t)
=
\alpha(1+t)^2+\beta t^2.
\]

This is enough to own the gauge/pure-shift incompatibility.

A generic inner-product theorem is optional, not required.

## Mandatory theorems

### 1. Exact quadratic completion

For \(\alpha+\beta>0\), prove

\[
E_{\alpha,\beta}(t)
=
(\alpha+\beta)
\left(t+\frac{\alpha}{\alpha+\beta}\right)^2
+
\frac{\alpha\beta}{\alpha+\beta}.
\]

### 2. Unique minimizer

For \(\alpha,\beta\ge0\) and \(\alpha+\beta>0\), prove the unique minimizer

\[
t_*=-\frac{\alpha}{\alpha+\beta}.
\]

Translate this to

\[
\delta_*=-\frac{\alpha}{\alpha+\beta}b,
\qquad
\kappa_*=\frac{\beta}{\alpha+\beta}b.
\]

### 3. Exact pure-gauge condition

For nonzero \(b\), requiring

\[
\delta_*=-b
\]

forces

\[
\beta=0
\]

under the stated positivity/nondegeneracy hypotheses.

### 4. Pure-shift failure

With \(\beta=0\) and \(\alpha>0\), the same minimizer on the pure affine-shift
control gives

\[
\delta_*=-b,
\qquad
\kappa_*=0,
\]

violating pure-shift visibility.

### 5. Converse endpoint

If \(\alpha=0,\beta>0\), prove

\[
\delta_*=0,\qquad \kappa_*=b,
\]

which is correct for pure shift but fails exact pure-gauge cancellation.

### 6. Positive interpolation boundary

If \(\alpha,\beta>0\), prove

\[
-b\ne\delta_*\ne0
\]

for the nonzero witness, so neither exact sector is selected.

### 7. Scoped no-go theorem

Package:

no background-independent nonnegative pair \((\alpha,\beta)\), with
\(\alpha+\beta>0\), makes this canonical local quadratic select both the exact
pure-gauge and pure-shift controls.

## Optional observer bridge

If existing APIs make it short, prove that the scalar hostile-ray reduction is
literally the rest-observer \(h_n\)-norm restriction.

Do not block the task on this optional theorem.

## Firewalls

Do not:

- claim no observer-based selector can exist;
- claim no nonlinear/q-derivative functional can work;
- invent curl/harmonic penalties;
- start finite E dressing;
- introduce a second clock;
- touch stress/Einstein/golden work.

## Exit condition

Lean owns the exact minimizer of the canonical observer-positive local quadratic
on the hostile Role-space ray and the resulting pure-gauge versus pure-shift
incompatibility, scoped explicitly to this background-independent quadratic
class.

## GitHub-first flow

Fresh main → lifecycle start → Draft PR → narrow build → incremental
\`D0.All\` → support registration → self-retire → \`Lifecycle: REVIEW\` →
Ready → do not self-merge.

No \`sorry\`, no new axioms, no \`lake clean\`.
