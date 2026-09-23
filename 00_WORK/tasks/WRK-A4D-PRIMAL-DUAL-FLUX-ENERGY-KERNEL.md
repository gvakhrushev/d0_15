# WRK-A4D-PRIMAL-DUAL-FLUX-ENERGY-KERNEL

## Class

WORKER / LARGE LEAN FORMALIZATION

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

IN_PROGRESS

## Canonical baseline

Repository:

`https://github.com/gvakhrushev/d0_15`

Authorized registration baseline:

`b5803d02447dba4ab09e9e56e726706af60d3771`

At launch:

```bash
git fetch origin
git rev-parse origin/main
```

If remote fetch is unavailable in the worker environment but the local `origin/main`
already equals or descends from the authorized baseline, proceed from that local
reference and report the fetch restriction. Do not modify an unrelated working tree.

Create one worktree on branch:

`work/a4d-primal-dual-flux-energy-kernel`

Do not clone again. Do not run `lake clean`. Preserve the warm Lean/Mathlib cache.

## Research source

Primary research input:

`MEMO_A4D_GRADED_CONSTITUTIVE_ENERGY_KERNEL_SELECTOR`

Research terminal:

`CONSTITUTIVE-KERNEL-FAMILY-CLASSIFIED-SELECTOR-MISSING`

This task formalizes the constructive flat-energy half only. It must not claim a
selected physical Hodge law.

## Main objective

Lean-own the chain

[
\text{algebraic complementary pairing}
\to
\text{full staggered }H(e)
\to
\text{finite flux energy}
\to
\text{Riesz kernel }I+H(e).
]

The construction must retain the full uncentered coframe
[
e_r{}^a(x).
]
Do not replace it by the centered readout, solder matrix, or Gram metric.

## Read first

Read fully:

```text
D0/Geometry/ArchiveCubicalCochainCarrier.lean
D0/Geometry/ArchiveCubicalDifferential.lean
D0/Geometry/ArchiveCubicalCartan.lean
D0/Geometry/ArchiveCARFockCarrier.lean
D0/Geometry/ArchiveCARRelations.lean
D0/Geometry/ArchiveCARDegreePreserving.lean
D0/Geometry/ArchiveHodgeCARDirac.lean
D0/Geometry/ArchiveHodgeCARDiracSquare.lean
D0/Geometry/A4DCoframeParentConstraint.lean
D0/Geometry/A4DSolderMetricCompletion.lean
D0/Geometry/FinitePrimalDualHodgeParent.lean
D0/Geometry/A4DPathWordParentWard.lean
```

Use current literal APIs. Do not create duplicate Role, Fock, cochain, pairing,
translation, or CAR carriers.

## Package A — algebraic complementary primal/dual pairing

Add:

`D0/Geometry/A4DPrimalDualCellPairing.lean`

Use homogeneous primal cochains from the existing archive/Fock carrier.

For degree (k), construct an algebraic complementary dual using the occupation
complement (S^c) and the ordered Role orientation sign.

Target pairing:
[
\beta_k(\phi,z)
=
\sum_{x,|S|=k}
\epsilon(S)\phi(x,S)z(x,S^c).
]

Required theorem family should include equivalents of:

```text
degree_complement
epsilon_complement_sign
algebraicComplementPairing
algebraicComplementPairing_perfect
evaluation_equiv_complement
```

This is algebraic duality only. It is not a located physical dual cell.

## Package B — geometric placement interface and nonuniqueness

Define a supplied-data structure such as:

```lean
structure GeometryDualPlacement ...
```

for any future located dual-cell rule. Do not install a canonical default instance.

For (L\ge3), construct at least two distinct local placement rules with identical
carrier cardinalities/algebraic duality.

Capstone:

`same_cardinality_does_not_provide_placement`

## Package C — Riesz uniqueness relative to supplied pairing and energy

For a supplied symmetric bilinear energy (Q_k), prove existence and uniqueness of:
[
S_k
]
such that
[
\beta_k(\phi,S_k\psi)=Q_k(\phi,\psi).
]

Target:

`energy_riesz_unique`

This theorem is relative to supplied (Q_k) and pairing. It is not physical-Hodge
uniqueness.

## Package D — full flat staggered first jet

Add:

`D0/Geometry/A4DDiscreteEnergyKernel.lean`

Define the research operator:
[
H(e)=
\sum_r B_r(e_r{}^r)I_{\mathcal F}
-
\sum_{s,r}
\left(
M_{e_s{}^r}U_sA_rE_{sr}
+
E_{rs}A_r^*U_s^{-1}M_{e_s{}^r}
\right).
]

Reuse existing shifts, backward averages, CAR operators, and counting pairing.

Required:

```text
flatStaggeredH_selfAdjoint
flatStaggeredH_preserves_degree
flatStaggeredH_preserves_parity
```

## Package E — exact finite Cartan expansion

Re-derive structurally:
[
G_\xi=
\sum_rM_{\xi^r}D_rI_{\mathcal F}
+
\sum_{s,r}
M_{\Delta_s\xi^r}U_sA_rE_{sr}.
]

Target:

`cartanGenerator_exact_expansion`

Use CAR and exact shifted-product identities. Do not use finite enumeration as the
main proof.

## Package F — exact Ward tangent

Prove:
[
H(d_f\xi)=-(G_\xi^*+G_\xi).
]

Target:

`H_forwardGauge_eq_negative_sym_Cartan`

Do not insert odd-period assumptions unless the literal proof requires them.

## Package G — distance-two corner support

For (s\ne r), the (U_sA_rE_{sr}) term contains the source offset (s-r).

Prove an exact structural statement or an explicit (L=3) theorem showing a nonzero
matter matrix entry at graph distance two.

Target:

`gradedH_requires_corner_distance_two`

This is a finite corner-locality theorem, not the arbitrary path-word bracket-growth
no-go.

## Package H — independent finite quadratic flux energy

Define the energy from site/edge/corner sums before referring to its Riesz kernel:

[
\begin{aligned}
\mathcal E_{\rm flux}(e;\psi)
={}&\frac12\sum_{x,S}\psi(x,S)^2\\
&+\frac12\sum_{r,x,S}e_r{}^r(x)\psi(x,S)\psi(x+r,S)\\
&-\sum_{s,r,x,S}e_s{}^r(x)
\psi(x,S)[U_sA_rE_{sr}\psi](x,S).
\end{aligned}
]

Suggested definition:

`fluxEnergy`

Do not define it as (\frac12\langle\psi,(I+H)e\psi\rangle). That relation must
be proved independently.

## Package I — polarization / Riesz-kernel theorem

Prove:
[
oxed{
2\mathcal E_{\rm flux}(e;\psi)
=
\langle\psi,(I+H(e))\psi\rangle_{count}.
}
]

Target:

`fluxEnergy_polarization_eq_H`

This is the load-bearing constructive theorem.

## Package J — flat controls

Prove:
[
H(0)=0,
\qquad
W_{\rm flux}(0)=I.
]

Then connect, only as independent checks, to the existing flat codifferential and
Hodge-Dirac square.

Suggested:

```text
fluxEnergy_flat_eq_counting
fluxEnergy_flatDirac_check
```

Do not define (H) from (D_H^2).

## Package K — L=2 Nyquist truth firewall

Construct the exact period-two nonzero coframe perturbation with:
[
B(e)=0,
\quad
\Theta(te)=\eta,
\quad
g(te)=\eta,
]
while the one-form component of (H(e)) is nonzero.

Targets:

```text
centeredNyquist_nonzero_H_oneForm
no_centeredMetricFactorization_firstJet
```

Do not declare this uncentered mode gauge.

## Package L — positivity near flat

Prove an explicit safe finite bound of the form:
[
\|H(e)\|\le C\epsilon,
\qquad
\epsilon=\max|e_s{}^r(x)|
]
and hence positivity of (I+H(e)) for sufficiently small (epsilon).

The research bound (C=36) may be used if it formalizes cleanly; a coarser explicit
uniform constant is acceptable.

Target:

`fluxEnergy_small_e_positive`

This is positivity of the real counting matter energy, not Lorentzian metric
nondegeneracy.

## Package M — algebraic-dual Riesz candidate

Using the complementary pairing, construct the graded map:
[
S_k^{alg}=J_k^{-1}Q_k^\flat.
]

Target:

`fluxEnergy_Riesz_abstractDual`

Document it explicitly as an algebraic-dual constitutive candidate.

Do not call it the selected physical Hodge.

## Mandatory controls

Include exact controls for:

- L=2 centered/Nyquist blindness;
- L=3 off-site scalar response;
- L=3 distance-two graded corner;
- L=5 centered Cartan/Ward regression;
- self-adjointness;
- degree preservation;
- parity preservation.

Use structural proofs wherever possible. Finite decision procedures are acceptable
only for bounded regression witnesses.

## Truth boundaries

Do NOT select or claim:

- geometric dual-cell placement;
- physical cell volumes;
- a Lorentzian signature convention;
- a physical timelike normal;
- nonlinear constitutive uniqueness;
- determinant-density exponent;
- preferred holonomy route;
- BOOK finite feedback operator;
- Einstein dynamics.

Do not identify abstract complementary Fock labels with located geometric dual cells.

## Expected verdicts

Primary:

`FLAT-GRADED-FLUX-ENERGY-KERNEL-OWNED`

Secondary where proved:

```text
ALGEBRAIC-PRIMAL-DUAL-COMPLEMENT-PAIRING-OWNED
STAGGERED-HODGE-FIRST-JET-OWNED
CENTERED-METRIC-ONLY-HODGE-NOGO
EVEN-L-NYQUIST-CONSTITUTIVE-OBSERVABILITY
GRADED-HODGE-CORNER-SUPPORT-OWNED
```

Retain:

```text
CONSTITUTIVE-KERNEL-FAMILY-CLASSIFIED-SELECTOR-MISSING
GEOMETRIC-DUAL-CELL-PLACEMENT-PRIMITIVE-REQUIRED
```

## Validation

During work use narrow builds.

Before PR:

```bash
lake build D0.All
python3 03_FORMALIZATION/tools/check_no_sorry_in_core.py --all-modules
python3 tools/validate_repo.py
python3 tools/validate_work.py
python3 tools/generate_lean_views.py --check
git diff --check
```

Inspect capstones with `#print axioms`.

No new:

```text
sorry
sorryAx
axiom
```

## Lifecycle / PR discipline

The task is canonically registered and authorized as `IN_PROGRESS`.

When complete:

1. fetch current `origin/main` if the environment permits;
2. rebase once if needed;
3. preserve all merged registry work;
4. regenerate tracked views using repository tooling;
5. rerun validation;
6. push branch;
7. open ONE PR;
8. report PR URL, head SHA, verdicts, capstones and axiom report;
9. STOP.

Do not wait for CI. Do not run watcher scripts. Do not self-merge.
