# WRK-A4D-RELATIVE-AE-GRAPHIFICATION-CLOSURE

## Class

WORKER

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

IN_PROGRESS

## Objective

Lean-own the **graphification / residual / two-sided functional** closure that
research PR #128 already proved on top of Lean #126
(`A4DRelativeAEComparisonSpan`).

Existing Lean owns `canonicalResidual_mem_vertical` and
`SpanCalibration ↔ verticalDefect = ⊥`, but not the full residual-range
equality, Role-basis residual criterion, residual-rank formula, full-rank ⇒
graph corollary, or reverse/horizontal defect package.

## Read first

- `03_FORMALIZATION/D0/Geometry/A4DRelativeAEComparisonSpan.lean` (owner API);
- `02_REGISTRY/research/MEMO_A4D_CLASSICAL_KINEMATIC_INTERFACE_PRESSURE.md`
  §§3–5 and handoff table §13 (esp. lines ~143–270, ~861–878);
- research PR #128 / Lean PR #126;
- sample brief style: `git show 163e607:00_WORK/tasks/WRK-A4D-LABELLED-ENDPOINT-CLASSICAL-DESCENT.md`.

## Preferred module

`03_FORMALIZATION/D0/Geometry/A4DRelativeAEGraphificationClosure.lean`

Namespace: `D0.Geometry.A4DRelativeAEGraphificationClosure`

Import and reuse `D0.Geometry.A4DRelativeAEComparisonSpan` (do not fork or
duplicate the span API). Extending the span module with a short closure
section is acceptable only if it stays clear; prefer a dedicated module.

## Mandatory theorem package

### 1. Residual range equals vertical defect

Prove
\[
\operatorname{LinearMap.range}(\mathrm{canonicalResidual}\,B\,S)
=
\mathrm{verticalDefect}\,B\,S.
\]
Use that the kernel component is the identity on \(\ker B\).

### 2. Role-basis residual criterion and span

With \(M := \mathrm{verticalDefect}\,B\,S\) and
\(R_r := \mathrm{canonicalResidual}\,B\,S\,(\mathrm{EuclideanSpace.single}\,r\,1)\):

- \(M = 0 \iff \forall r,\; R_r = 0\);
- \(M = \bigsqcup_r \mathbb{R}\cdot R_r\) / span of the four Role residuals.

Optional hostile control: vanishing of one Role residual (or of the sum of all
residuals) is strictly weaker than \(M=0\).

### 3. Residual-rank formula

Under `FiniteDimensional ℝ V` (and the always-finite label coefficient space),
\[
\mathrm{Module.finrank}\,\mathbb{R}\,(\mathrm{verticalDefect}\,B\,S)
=
\mathrm{Module.finrank}\,\mathbb{R}\,(\mathrm{LinearMap.range}\,(\mathrm{pairSynthesis}\,B\,S))
-
\mathrm{Module.finrank}\,\mathbb{R}\,(\mathrm{LinearMap.range}\,B).
\]
Equivalently: rank-nullity for the relation projection whose kernel is
\(\{0\}\oplus M\). State hypotheses carefully; use Mathlib rank-nullity.

### 4. Full-rank \(B\) implies graph

If `LinearMap.ker B = ⊥` (equivalently \(B\) injective), then
`verticalDefect B S = ⊥` and `SpanCalibration B S`.

Optionally, when `FiniteDimensional ℝ V` and
`Module.finrank ℝ LabelCoeff \le Module.finrank ℝ V` with
`LinearMap.rank B = Module.finrank ℝ LabelCoeff`, the same conclusion.

Do **not** claim physical classicality. Full rank is not needed for formulas
that only require \(M=0\).

### 5. Both-directions functional iff equal kernels

- Forward graph \Leftrightarrow `verticalDefect B S = ⊥` \Leftrightarrow `ker B \le ker S` (already owned;
  restate/reuse).
- Reverse graph: define horizontal defect `B '' (ker S)` /
  `(ker S).map B`; the reversed relation is a function on `range S` iff that
  defect is `⊥` iff `ker S \le ker B`.
- Both directions functional iff `ker B = ker S`.

Do **not** identify one-sided graph with a reversible change of variables.

## Firewalls

Do not:

- introduce `sorry` or new axioms;
- run `lake clean`;
- start finite graded \(F\), continuum, GR, QFT, action, stress, or physical
  time claims;
- identify one-sided graphification with invertible comparison / paired gauge
  orbit;
- claim full rank is required for statements that only need \(M=0\);
- treat one Role residual vanishing as graphification;
- self-merge.

## Exit condition

Lean owns residual-range equality, Role-basis residual criterion, residual-rank
formula, full-rank \(\Rightarrow\) graph corollary, and two-sided functional \(\leftrightarrow\) equal kernels,
wired through `formal_support.csv` / `D0.All`, with the task self-retired before
Ready.

## GitHub-first flow

Fresh current main \(\to\) lifecycle start \(\to\) Draft PR \(\to\) narrow build \(\to\) incremental
`D0.All` \(\to\) support registration \(\to\) self-retire \(\to\) `Lifecycle: REVIEW` \(\to\)
Ready \(\to\) do not self-merge.

No `sorry`, no new axioms, no `lake clean`.
