# MEMO_A4D_GOLDEN_ROLE_PHASE_CARRIER_OPERATOR_WELD

**Baseline:** `main = fa4af53bed53a693efbd1db832ae092c51eb5536`.
**Branch start:** `4ffc910` (lifecycle `IN_PROGRESS`).
**Brief:** `00_WORK/tasks/EXP-A4D-GOLDEN-ROLE-PHASE-CARRIER-OPERATOR-WELD.md`.
**Consumed:** PR #86 `MEMO_A4D_GOLDEN_ROLE_PHASE_REFINEMENT_WELD.md`, `ROADMAP_A4D_RELATIONAL_REFINEMENT_SYNTHESIS.md`, PR #99 `A4DGoldenRolePhaseRGDefect` and `A4DGoldenCarrierWeldBoundary`.
**No Lean source. No physical time. No `J` / `D_H` / `H(e)` inter-level naturality.**

## 0. Terminal verdict

**GOLDEN-ROLE-PHASE-WELD-NEW-PRIMITIVE-REQUIRED**

The first comparison layer that is not immediately empty is a Role-equivariant correspondence / Hilbert bimodule

```text
(A_k, C(B_n), X_{k,n})
```

together with an owned index rule relating Bratteli depth `k` to Role-phase period `n`. Neither datum is owned.

Scoped no-gos on the owned finite stages:

1. no bijection of finite point carriers `C_k ↔ B_n`;
2. no consecutive group-homomorphism tower `B_{L_{k+1}} → B_{L_k}` along Fibonacci, Lucas, `F_k+1`, `F_k+2`, or `floor(phi^k)` period names;
3. no injective unital `*-homomorphism A_k → C(B_n)` for `k ≥ 1`;
4. no dimension-matching GNS identification of `(A_k, τ)` with `ℓ²(B_n)` or `ℓ²(B_n × Fock)`.

The PR #99 scalar

```text
goldenScaleProbe k = phi
```

is independent of `k` and transports no Tower-C state. It is not a carrier weld.

## 1. Exact tower types

### Tower B — Role-phase / CAR

- `ArchiveRolePhasePoint n = Role → Fin(n+2)`
- `ArchiveRolePhaseGroup n = Role → ℤ/(n+2)ℤ`
- `archiveRolePhaseProjection n` is coordinatewise `archiveRGPhaseProjection n`, and `archiveRGPhaseProjection n x = ⟨x.val % archiveFibers n, …⟩`

With `L = n+2`:

| n | L | `|B_n| = L^4` | cochain `16 L^4` |
|---|---|---|---|
| 0 | 2 | 16 | 256 |
| 1 | 3 | 81 | 1296 |
| 2 | 4 | 256 | 4096 |
| 3 | 5 | 625 | 10000 |
| 4 | 6 | 1296 | 20736 |
| 5 | 7 | 2401 | 38416 |
| 6 | 8 | 4096 | 65536 |

A group homomorphism `ℤ/L' → ℤ/L` requires `L | L'`. The owned consecutive projection always goes `n+1 → n`, i.e. `L+1 → L`, and is a finite-set map, not in general a group map.

Role `S_4` acts by permuting coordinates. PR #99 owns that this commutes with the coordinatewise projection at the **set** level only.

### Tower C — golden cylinder / Bratteli / AF

- incidence `M_φ = [[1,1],[1,0]]` recovered from forbid-`11`
- `M_φ² = M_φ + I`
- path counts `p(0)=(1,1)`, `p(k+1)=(a+b, a)`
- `A_k = M_a(ℂ) ⊕ M_b(ℂ)`, `dim A_k = a² + b²`
- unique normalized trace ratio `φ`
- cylinder identity `μ(w0)+μ(w1)=μ(w)` on allowed words

| k | `(a,b)` | paths / words | `dim A_k` |
|---|---|---|---|
| 0 | (1,1) | 2 | 2 |
| 1 | (2,1) | 3 | 5 |
| 2 | (3,2) | 5 | 13 |
| 3 | (5,3) | 8 | 34 |
| 4 | (8,5) | 13 | 89 |
| 5 | (13,8) | 21 | 233 |
| 6 | (21,13) | 34 | 610 |

Index `k` is Bratteli depth. It is not Role-phase period `n`, not record depth, not a history tick, and not physical time.

### Tower A — record / profinite

Not used as a substitute. First-step fibers `6 ≠ 16` remain the owned A/B separation (`record_rolePhase_firstStep_fibers`).

## 2. Comparison classes

### 2.1 Point carrier — scoped no-go

`|B_n| ∈ {16, 81, 256, 625, 1296, 2401, 4096, …}`.
Word / path counts `∈ {2, 3, 5, 8, 13, 21, 34, 55, 89, …}`.
`dim A_k ∈ {2, 5, 13, 34, 89, 233, 610, …}`.

No coincidence on the first twelve stages. In particular `16, 81, 256, 625, 1296` are not Fibonacci numbers.

Role-equivariance is independently empty: Tower C has the SFT shift and a 2-vertex Bratteli labelling, not an `S_4`-action. The only equivariant maps would use a trivial Role action on `C_k`, which is not a weld.

This is not a ban on correspondences.

### 2.2 Function space — no canonical weld

Linear maps `Fun(C_k) → Fun(B_n)` exist because both spaces are finite-dimensional. Canonical ones do not. `Hom_{S_4}(Fun(C_k), Fun(B_n))` vanishes unless `S_4` acts trivially on the source. Pullback along a point map is unavailable by §2.1.

### 2.3 Algebra homomorphism — scoped no-go

`A_k` is noncommutative for `k ≥ 1` (`dim A_1 = 5 = 4+1`). `C(B_n)` is commutative of dimension `L^4`.

Any unital `*-homomorphism A_k → C(B_n)` kills commutators and factors through the abelianization `ℂ ⊕ ℂ` (two block traces = two Bratteli vertices). That image is not Role-phase geometry.

A unital hom `C(B_n) → A_k` is a choice of commuting projections inside `M_a ⊕ M_b`. That is a labelling of matrix units by Role-phase points — a point-carrier map in disguise, already excluded.

### 2.4 GNS identification — scoped no-go

On these finite AF stages the GNS space of the unique trace has dimension tracking `dim A_k`. Compare:

- `dim GNS_C ∈ {2, 5, 13, 34, 89, 233}`
- `|B_n| ∈ {16, 81, 256, 625, …}`
- `|B_n| × 16 ∈ {256, 1296, 4096, …}`

No match. The existing vNext firewall already says AF/GNS isometry is not a D0 Hilbert identification. This audit does not construct a new GNS owner.

### 2.5 Reindexed group tower — scoped no-go

Hostile period names and consecutive divisibility `L_k | L_{k+1}`:

| name | first terms | consecutive divisibility after the first two steps |
|---|---|---|
| `F_k` | 1, 1, 2, 3, 5, 8, 13, … | fails from `2 ∤ 3` |
| `F_k+1` | 2, 2, 3, 4, 6, 9, … | fails from `2 ∤ 3` |
| `F_k+2` | 3, 3, 4, 5, 7, … | fails from `3 ∤ 4` |
| `floor(phi^k)` | 1, 2, 4, 6, 11, … | fails from `4 ∤ 6` |
| Lucas | 1, 3, 4, 7, 11, … | fails from `3 ∤ 4` |

No owned Tower-C theorem produces a divisibility chain of Role-phase moduli. Abstract doubling subsequences such as `F_{2^m} | F_{2^{m+1}}` are not Role-phase period laws.

Owned bonding on B is always the `+1` period step. Owned bonding on C is Bratteli incidence / letter restriction with ratio `→ φ`. These are different functors.

### 2.6 One-dimensional Zeckendorf candidate — positive, not a weld

No-`11` words of length `k` are in bijection with `{0, …, F_{k+2}-1}` by the standard Fibonacci coding. Prefix-restriction `k+1 → k` and integer reduction modulo `F_{k+2}` have the same fiber-size multiset (Fibonacci 1-or-2 fibers). Explicit control `13 → 8`: both maps have fiber sizes `{1,1,1,2,2,2,2,2}`.

This does **not** identify:

- owned `archiveRGPhaseProjection : Fin(n+3) → Fin(n+2)` with Fibonacci restriction;
- cyclic translation `+1 mod L` with the golden shift;
- the four-fold Role product `B_n` with a product of four word spaces;
- an `S_4` action on words.

To promote it one would have to choose `n+2 = F_m` and replace the owned consecutive projection by a non-owned Fibonacci bonding. That is new primitive data, not a weld of present owners.

### 2.7 Correspondence / bimodule — the remaining layer

A Hilbert `A_k`–`C(B_n)` bimodule `X_{k,n}` is the first class not killed by commutativity, cardinality, or missing `S_4` on C: the bimodule can carry the Role action on the `C(B_n)` side only. Existence of *some* bimodule is cheap and noncanonical. A weld requires:

1. an owned rule `k ↔ n` that is not `k = n` and not an ad-hoc `L = F_k`;
2. Role-equivariance of `X` on the B side;
3. compatibility of the two refinement operations (Bratteli inclusion on `A_k`, `p_n` on `B_n`) as a correspondence square;
4. only then a residual test against PR #99.

None of (1)–(3) is owned. This is the missing primitive.

## 3. PR #99 residual after the comparison audit

```text
goldenScaleProbe k = phi          for every k
goldenRGResidual n k P = 0  iff  RenormalizedProjectiveCompatibility n P phi
```

Energy residual is a separate Dirichlet statement.

These theorems take an arbitrary finite-set comparison `P` of one-dimensional phase indices and a real probe. They do not receive a Tower-C word, AF element, or measure. After §2 there is still no `P` supplied by a carrier / function / algebra map from C. The residual remains a conditional diagnostic. Setting `c = phi` does not upgrade it to a weld.

Nearest-neighbor exact projective failure for `n > 1` stays a negative control at scale `1`, not a theorem that the golden residual never vanishes.

## 4. Index and Role-equivariance audit

| datum | status |
|---|---|
| `k` vs `n` | distinct; no owned relation |
| record depth | Tower A; not used |
| history tick / `U_A` / physical time | firewalled |
| Role set-equivariance of `p_n` | owned |
| Role action on Tower C | absent |
| translation intertwining of consecutive `p_n` | fails in general (moduli not divisible) |
| Fock 16-fiber identity lift | a construction choice, not a C-consequence |

## 5. Firewalls respected

Not inferred: `k = n`; physical time from golden depth; carrier weld from `c = phi`; Tower A = Tower B; located-`J`, `D_H`, or `H(e)` inter-level naturality; stress or Einstein dynamics.

## 6. Exact controls

- `|B_n| = (n+2)^4` and `16(n+2)^4` for `n = 0..6`
- `dim A_k` and path counts from `FibonacciAFAlgebra` / Bratteli owner for `k = 0..6`
- forbid-`11` word lists and prefix-fiber sizes for `k = 4,5`
- modular fibers of `{0,…,12} → ℤ/8ℤ`
- divisibility table for five hostile period names
- PR #99 `goldenScaleProbe_eq_phi` and first-step fibers `6 ≠ 16`
- commutativity of `C(B_n)` versus `A_k` for `k ≥ 1`

These controls can fail the conclusion if a later owner produces a Role action on C, a divisibility subsequence canonized by Tower C, or a named bimodule with an index rule. Until then the terminal stands.

## 7. Theorem-ready handoff

Lean-next, one module, no correspondence constructor:

extend `A4DGoldenCarrierWeldBoundary` with explicit cardinality and divisibility lemmas:

- `fib_dimA_not_rolePhaseCard` for small `k, n`
- `hostile_period_not_consecutive_divisor` for the five named sequences
- optional later: `af_to_continuous_functions_factors_abelianization`

Do not add a `Correspondence` structure with placeholder fields. Do not claim `J` / `D_H` / `H(e)` squares.

## 8. Exactly one next step

Formalize the cardinality / hostile-divisibility boundary next to `A4DGoldenCarrierWeldBoundary`. The correspondence primitive stays research-named until an owned index rule exists.
