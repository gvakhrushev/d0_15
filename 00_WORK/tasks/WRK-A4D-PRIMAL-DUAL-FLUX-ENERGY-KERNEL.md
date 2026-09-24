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

`df7779ef86ad9430d87adc32b60f15779277ff0a`

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

Do not clone again under normal operation. Do not run `lake clean`. Preserve the warm Lean/Mathlib cache.

### Sandbox recovery exception

If the existing git worktree cannot write its own shared metadata under
`.git/worktrees/...` and therefore fails on `rebase`, `merge --ff-only`,
`git add`, or equivalent ref/index operations with `Operation not permitted`,
the coordinator may authorize exactly one temporary standalone recovery clone for
this worker.

Under that exception:

- do not mutate or delete the blocked worktree;
- create the recovery clone from the authorized remote worker branch/current main;
- transfer only the worker's untracked source artifacts, with checksums recorded
  before and after;
- do not transfer `.git` metadata;
- do not commit `.lake`;
- reuse the existing Lean/Mathlib cache by a non-versioned symlink or equivalent
  cache path where supported;
- all final commits, validation, push, and the single PR must come from the
  recovery clone;
- report that this exception was used.

This exception is operational only. It does not change theorem scope, task state,
or scientific ownership.

## Three-star dictionary — keep these objects distinct

| Name | Meaning |
|---|---|
| `J` | Two-color center-matched primal/dual placement/pairing. Topological complement sign `(-1)^(k*(4-k))`. In 4D it preserves Fock parity. It is not a metric constitutive selector. |
| `h_n` / metric `*_eta` | Observer/Lorentz metric structure. The Lorentzian double-star carries the additional signature exponent `q=3`. This is not cell placement. |
| scalar reverse-star | A one-color local inverse/reverse stencil used only in the scoped two-sided-locality no-go. It is neither `J` nor the Lorentz metric star and it does not select `Q(e)`. |

Never transfer a theorem or no-go from one row to another without an explicit typed bridge.

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

## Package B — placement negative control; do not own the star here

The located-star research has classified the reference placement:

```math
F_PD(x,S) = (x - 1_{S^c}, S^c),
F_DP(y,T) = (y + 1_T, T^c).
```

This worker must NOT create a second competing placement owner.

If the older memo/ansatz contains two placement rules or a cardinality-only alternative, use the non-reference rule only as a NEGATIVE CONTROL: show that it violates the independent primal/dual incidence intertwining, center matching, or another explicitly stated condition.

The placement class is no longer “missing” at research level. It remains a separate formalization owner in `WRK-A4D-LOCATED-PRIMAL-DUAL-STAR`.

Package B may expose only the minimal interface needed by the energy/pairing construction. It must not promote `J` to a constitutive selector.
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


## Package N — Role residual / spatial-triad representation weld

This package is mandatory and must reuse the already-owned typed scene and shell symmetry APIs.

Read additionally:

```text
D0/Geometry/TypedSceneOppositeCut.lean
D0/Geometry/TypedRoleOppositeCut.lean
D0/Representation/TypedRoleSceneAction.lean
D0/Geometry/ArchiveSpatialHistorySplit.lean
D0/Geometry/ArchiveHodgeSpatialShellOperator.lean
```

Current owners already provide:

- `BalancedRole` over `ℚ`, with `balancedRole_perm`;
- `SpatialRole := {r : Role // r ≠ A}`, with cardinality three;
- `spatialAxisEquivRole : SpatialAxis ≃ SpatialRole`;
- `SpatialRoleStabilizer := {σ : Equiv.Perm Role // FixesRoleA σ}`;
- `typedRoleResidual`, whose Role-summand value is
  [
  99(w_{AC}-w_{BC})f(r);
  ]
- shell transport whose basis action is axis permutation × unchanged harmonic × signed Fock transport.

Construct the canonical restriction/extension between spatial coefficients and balanced Role functions.

Required public names should include the requested surface:

```text
balancedRoleOfSpatial
balancedRoleOfSpatial_iso
typedRoleCut_stabA_eq_spatialTriad
```

A recommended exact API is:

1. `balancedRoleOfSpatial : (SpatialRole → ℚ) →ₗ[ℚ] BalancedRole`, with
   [
   (iota g)(A)=-sum_{r:SpatialRole}g(r),
   qquad
   (iota g)(r)=g(r)quad(r
e A).
   ]

2. `spatialOfBalancedRole : BalancedRole →ₗ[ℚ] (SpatialRole → ℚ)` by restriction.

3. `balancedRoleOfSpatial_iso : (SpatialRole → ℚ) ≃ₗ[ℚ] BalancedRole`, proving the two maps are inverse.

4. Define the natural stabilizer action on `SpatialRole → ℚ` and prove that the equivalence intertwines it with `balancedRole_perm` restricted to `SpatialRoleStabilizer`.

The intertwining theorem should be structural, not an enumeration of all six permutations.

### Spatial residual readout

Define a restricted Role-summand/spatial readout of `typedRoleResidual`:

[
R_{sp}(w)(g)(r)
=
typedRoleResidual(w)(iota g)
  (Role	ext{-summand at }r),
qquad r:SpatialRole.
]

Prove exactly:

[
oxed{
R_{sp}(w)
=
99(w_{AC}-w_{BC}),I_3.
}
]

The requested capstone `typedRoleCut_stabA_eq_spatialTriad` should express this identity together with stabilizer equivariance, or be accompanied by a clearly named scalar identity plus an equivariance theorem.

This is the precise sense in which the rank-three typed Role residual is the spatial triad representation after freezing Role A.

Do NOT identify the whole typed vertex residual carrier with a spatial cochain carrier.

### Shell representation compatibility

Use `spatialAxisEquivRole` and the already-owned
`diagonalRoleTransport_shellCochain` to state the exact common stabilizer action.

The full rank-96 shell basis transforms as:

[
SpatialAxis
	imes
ShellHarmonic
	imes
ArchiveFockState,
]

with:

- `SpatialAxis` permuted by the A-stabilizer;
- `ShellHarmonic` unchanged;
- `ArchiveFockState` moved by the signed Fock representation.

Therefore the shell is an amplification/tensor-type representation of the spatial-axis action, not literally the same 3-dimensional representation.

Because `BalancedRole` is over `ℚ` and the shell is over `ℝ`, any direct linear comparison must explicitly perform scalar extension/casting. Do not silently identify the fields.

Strongly preferred control:

- exhibit at least two distinct stabilizer-equivariant spatial-triad embeddings into the shell when `archiveFibers N ≥ 3`, for example the vacuum `cos` and vacuum `sin` axis spans, if the existing API makes this clean;
- conclude that Role symmetry alone does not select a unique physical `3 → 96` scene-to-shell embedding.

If this preferred control is expensive, the mandatory result is the spatial coefficient/BalancedRole isomorphism and exact residual scalar identity.

### Representation truth boundary

This package establishes a common representation language for the same A-stabilizer.

It does NOT establish:

- scene carrier = archive cochain carrier;
- typed Role residual = matter state;
- typed Role residual = Hodge shell;
- a canonical physical scene-to-shell embedding;
- Einstein residual/stress identification.

Any constitutive use of the spatial residual must be typed as additional data or a later derived pairing.


Additional Package N firewalls:

- the typed cut/`BalancedRole` side is over `ℚ`; the archive coframe/energy side is over `ℝ`. Any scalar extension must be explicit;
- `dim Hom_{S3}(R^3, H_shell)=48` is a nonselection result for direct shell embeddings, not a material selector;
- the only permitted coupling chain here is `99-cut → e_spatial → Q(e) → S_J(e) → matter`; do not insert the scene residual directly into the 96-shell;
- Package N does not choose `c=1`, `c=2`, or any nonlinear `Q(e)`.

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

## Shell compression naming firewall

If the worker defines the shell compression of the flat/first-jet matter kernel, name it `spatialShellFluxCompression` (mathematically `F_shell^flux = P_96 (I + H(e)) P_96`).

Do NOT call this BOOK `F_N`. The independent shell theorem `D_H^2|shell = E_1^2 I` is a control, not the definition of this compression.

## Additional forbidden promotions

- do not wait for the frame-lift EXP;
- do not choose between the nonlinear reference laws `c=1` and `c=2`;
- do not identify `U_A` with physical time evolution;
- do not identify `J` with the Lorentzian metric star.
