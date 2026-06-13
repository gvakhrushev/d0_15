# Техническое задание: полный перенос D0 в Lean 4

**Версия ТЗ:** 2026-05-28
**Исходный корпус:** `D0_v11_45_OPERATOR_BRIDGE_TRIPLE_CLOSURE_20260528`
**Цель:** превратить D0 из монографического корпуса с Python-certificates в формально проверяемую систему: Lean закрывает математическое ядро, Python/CI закрывает вычислительные и эмпирические паспорта, теория-граф связывает каждое утверждение с доказательством, сертификатом, мостом и данными.

---

## 0. Главный принцип

Lean-порт не должен быть “переписыванием текста в Lean”. Это формальная реконструкция теории по уровням строгости.

```
Lean core theorem      = строгое математическое доказательство без sorry/axiom в релизном ядре
Lean bridge theorem    = теорема с явно объявленными предпосылками/assumptions
Python cert            = вычислительная проверка конечных инвариантов, больших матриц, эмпирических данных
External passport      = воспроизводимый pipeline с данными, hash, схемой, логом запуска
Theory map             = claim → Lean theorem → cert → data → book section
```

Запрещено смешивать эти уровни. Если физический claim зависит от внешней схемы RG, данных DESI/PDG, lattice/QFT conventions, он не должен становиться “core theorem” в Lean. Он должен иметь Lean-ядро + Python/CI bridge/passport.

---

## 1. Непосредственные проблемы текущего Lean seed

Текущий `09_LEAN_FORMALIZATION` в v11.45 является только seed. Его нельзя считать доказательством.

Выявленные проблемы:

1. `PositiveResponseSplit` использует `Float`. Это запрещено для core.
2. Есть `axiom role_cardinality_target`, `axiom omega8_cardinality_target`, `axiom primitive_equation_target`. В релизном core такие аксиомы запрещены.
3. Нет Lake-проекта с устойчивой зависимостью на mathlib.
4. Нет единой карты `Claim ID → Lean theorem`.
5. Нет CI-команды, которая отличает `core`, `bridge`, `passport`.

Требование v12 Lean-core: заменить seed на компилируемый проект без `sorry` и без неразрешённых `axiom` в `D0/Core/*`.

---

## 2. Целевое разделение на слои

### 2.1. Lean Core

Доказуемо полностью внутри Lean:

- конечные типы и мощности: `D₂`, `ABCD`, `Ω₈`, `V₉`, `V₁₁`, `V₁₃`;
- алгебра `p + p² = 1`, уникальность положительного корня;
- `δ₀ = (p - p²)/2 = 1/(2φ³)`;
- capacity-chain `D₂ → ABCD → Ω₈ → V₉ → V₁₁,V₁₃`;
- counts для `K(9,11,13)`: vertices, edges, triangles, no 3-simplices;
- forced return windows: `q_T=44`, `φ_Euler(44)=20`, `q_EW=710`, `φ_Euler(710)=280`, `280/8=35`;
- off-diagonal destructive count `18×17=306`;
- finite matrix Clifford check for `Cl(1,3)` with explicit gamma matrices;
- finite trace/Born skeleton for finite matrices/effects;
- finite anomaly arithmetic for one SM generation as rational sums;
- boundary-of-boundary identity for finite simplicial incidence matrices.

### 2.2. Lean Bridge Theorems

Формализуются как теоремы с явными предпосылками:

- condensed/profinite support: projective system, representable functor, naturality;
- Lorentz macro bridge: finite Clifford representation → stated Lie-group bridge assumptions;
- `φ`-discrete RG: finite difference step → continuous interpolation under smoothness assumptions;
- smooth metric bridge: covariance family + heat trace/Weyl assumptions → smooth macro interpretation;
- HST/convex-response bridge: finite subgaussian source + external theorem assumption.

В bridge-файлах допустимы named assumptions, но они должны быть явно заключены в структуры `Assumptions` и не импортироваться в `D0/Core`.

### 2.3. Python/CI Certificates

Остаются в Python:

- большие численные матрицы, если Lean-доказательство избыточно дорого;
- BAO/SDE likelihood reproduction;
- PDG/RG scheme passports;
- hadron/meson numerical comparison;
- full cert runners and release ledgers.

### 2.4. Не переносить в Lean на первом этапе

- Полный collider generator;
- полные 2-loop/3-loop SM RG kernels;
- full DESI/Planck likelihood;
- lattice QCD comparisons;
- raw experimental-data pipelines.

Эти части должны ссылаться на Lean-core assumptions и проверяться CI.

---

## 3. Целевая структура Lean-проекта

```
D0Lean/
  lakefile.lean
  lean-toolchain
  D0/
    Core/
      FiniteTypes.lean
      DyadABCD.lean
      Phi.lean
      Delta.lean
      CapacityChain.lean
      PositiveResponse.lean
      MatrixResponse.lean
      BornFinite.lean
    Combinatorics/
      EulerPhi.lean
      CompleteTripartite.lean
      CliqueComplex.lean
      PhaseUnfolding.lean
      ForcedReturnWindows.lean
      HighGainCounts.lean
    Topology/
      SimplicialIncidence.lean
      BoundaryBoundary.lean
      NoThreeSimplices.lean
    Algebra/
      Clifford13.lean
      GammaMatrices.lean
      LieCarrierFinite.lean
    Gauge/
      SMCharges.lean
      AnomalySums.lean
      WardFinite.lean
    Condensed/
      ProjectiveSystem.lean
      ProfiniteSupport.lean
      AdmissibleSubfunctor.lean
      OperatorNaturality.lean
    Bridge/
      LorentzBridge.lean
      PhiDiscreteRG.lean
      SmoothMetricBridge.lean
      ConvexResponseBridge.lean
    TheoremLedger/
      ClaimMap.lean
      ReleaseStatus.lean
    All.lean
```

Правило импорта:

```
Core        imports Mathlib only
Combinatorics imports Core
Topology    imports Core + Combinatorics
Algebra     imports Core + Matrix
Gauge       imports Core + Topology + Algebra
Condensed   imports Core only where possible
Bridge      imports Core/Combinatorics/Topology/Algebra/Gauge + explicit assumptions
All         imports all modules and exposes theorem list
```

---

## 4. Этапы работ

## P0. Bootstrapping Lake/mathlib project

### Задача
Создать реально компилируемый Lean 4 проект.

### Deliverables

- `lakefile.lean` with mathlib dependency;
- `lean-toolchain` fixed to current stable mathlib-compatible version;
- `D0/All.lean` compiling;
- GitHub/IDE command:

```
lake exe cache get
lake build
```

### PASS

- `lake build` passes on clean machine.
- В `D0/Core` нет `sorry`, `axiom`, `admit`, `unsafe`.

---

## P1. Exact arithmetic and φ-core

### Цель
Закрыть математическое ядро `p+p²=1`, `φ`, `δ₀`, `Q(D)` без float.

### Теоремы

1. `primitive_quadratic_unique_pos_root`
   Для `p : ℝ`, если `0 < p`, `p < 1`, `p + p^2 = 1`, то `p = (Real.sqrt 5 - 1)/2`.

2. `phi_inv_satisfies_primitive`
   `φ = (1 + sqrt 5)/2`, `p=φ⁻¹`, then `p + p^2 = 1`.

3. `psi_conjugate_identities`
   `φ+ψ=1`, `φψ=-1`, `φ²=φ+1`, `ψ²=ψ+1`.

4. `delta_half_gap`
   `δ₀ = (φ⁻¹ - φ⁻²)/2 = 1/(2φ^3)`.

5. `Q_dimension_ladder`
   `Q(D)=2δ₀ φ^(D-1)=φ^(D-4)` for integer `D`, with careful handling of integer powers.

### Implementation notes

- Use `ℝ`, not `Float`.
- Prefer lemmas over exact radicals if simplification becomes painful.
- If mathlib lacks convenient automation, create local lemmas for `sqrt 5` positivity.

### PASS

- All theorem statements compiled.
- No `norm_num` over floats.
- No hidden axiom for existence/uniqueness.

---

## P2. Capacity chain: D₂, ABCD, Ω₈, V₉, V₁₁, V₁₃

### Цель
Формально доказать информационную ёмкость терминального алфавита.

### Definitions

- `Dyad := Fin 2`
- `Role := Dyad × Dyad`
- `Orient := Bool`
- `Omega8 := Role × Orient`
- `Witness := PUnit` or singleton type
- `V9 := Sum Omega8 Witness`
- `V11 := Sum V9 Dyad`
- `V13 := Sum V9 Role`

### Теоремы

- `card_role = 4`
- `card_omega8 = 8`
- `card_v9 = 9`
- `card_v11 = 11`
- `card_v13 = 13`
- `scene_card_total = 33`

### Negative controls

- `no_three_role_terminal_capacity`: a 3-role alphabet cannot represent `Dyad × Dyad` bijectively.
- `no_five_role_minimality`: a 5-role alphabet is not minimal for two-port terminal readout.

### PASS

- Cardinalities proved by `Fintype.card`.
- Role definitions are not arbitrary enums; ABCD must be represented as product `Dyad × Dyad`.

---

## P3. K(9,11,13) finite combinatorics and clique complex

### Цель
Формально закрыть counts и topological guardrail.

### Definitions

- `Part := P9 | P11 | P13`
- vertices as dependent sum over parts with finite indices.
- edge relation: distinct parts.
- triangle relation: one vertex from each part.
- no 4-clique theorem.

### Теоремы

- `num_vertices = 33`
- `num_edges = 9*11 + 9*13 + 11*13 = 359`
- `num_triangles = 9*11*13 = 1287`
- `no_four_clique`
- `clique_complex_max_dim_eq_two` or weaker `no_3_simplices`

### Important guardrail

Do not formalize “no 3-simplex ⇒ all SM anomalies vanish” as a core theorem. Formalize:

- no internal 3-simplex carrier;
- separate finite anomaly trace sums over the declared one-generation matter ledger.

### PASS

- Combinatorial counts exact.
- No claim that `H₃=0` alone proves SM anomaly cancellation.

---

## P4. Phase unfolding and forced return windows

### Цель
Закрыть, что `44` и `710` forced by capacity, not post-hoc approximants.

### Definitions

- Euler totient, using mathlib if available.
- `qT := Nat.lcm 4 11 = 44`
- `mT := 4 + 3 = 7`
- `d13 := Nat.totient 44 = 20`
- `B := 5`
- `L := 2*33 + 5 = 71`
- `qEW := 2*B*L = 710`
- `mEW := B*d13 + 13 = 113`
- `DEW := Nat.totient 710 / 8 = 35`

### Теоремы

- `lcm_abcd_v11 = 44`
- `totient_44 = 20`
- `d13_from_return_window = 20`
- `qEW_forced = 710`
- `totient_710 = 280`
- `ew_depth_from_omega8 = 35`

### Negative controls

- `355` as half-window fails full oriented return requirement.
- `568` fails witness/basepoint pointed alphabet requirement.

These can be theorem statements depending on formal predicates:

```
FullOrientedReturn q := ...
PointedAlphabetReturn q := ...
```

### PASS

- No use of decimal `2π` to derive `44` or `710`.
- Near-return to `2π` can be a separate lemma/check, not the defining proof.

---

## P5. Hurwitz / φ phase rigidity

### Цель
Формализовать диофантовый смысл `φ` как non-resonant phase generator.

### Minimum Lean target

Full Hurwitz theorem may be too large for initial port. Minimum accepted core:

- define continued fraction prefix for `φ` or `φ⁻²`;
- prove Fibonacci convergents for `[1;1,1,...]` up to general recurrence if feasible;
- prove finite certificate lemmas for first N convergents used by D0;
- state full Hurwitz/golden worst-approximable theorem as bridge assumption if mathlib lacks it.

### Theorem layers

Core:

- `phi_cf_all_ones_prefix_N` for computable finite prefixes;
- `convergents_fibonacci_relation`.

Bridge:

- `GoldenBadlyApproximableAssumption` with precise statement and citation outside Lean.

### PASS

- Do not fake full Hurwitz theorem with an axiom in Core.
- If assumed, isolate in `D0/Bridge/HurwitzAssumption.lean`.

---

## P6. Positive response and finite Born rule

### Цель
Формально закрыть “probability = normalized positive trace response” для конечного случая.

### Definitions

- finite Hilbert space as `n × n` complex matrices;
- `PositiveSemidefinite` using mathlib matrix positivity if available;
- effect family `E_i ≥ 0`, `∑ E_i = I`;
- state `ρ ≥ 0`, `Tr ρ = 1`;
- response `p_i = Re(Tr(ρ E_i))`.

### Теоремы

- `response_nonnegative`
- `response_sum_one`
- `response_additive_on_orthogonal_effects`
- `unitary_covariance_trace_response`

### Scope guardrail

Do not claim full Gleason theorem unless proved or imported. For first release: finite POVM trace response theorem under explicit state/effect assumptions.

### PASS

- Exact finite matrix proof compiles.
- Dimension-2 caveat documented.

---

## P7. Clifford/Lorentz finite carrier

### Цель
Закрыть finite matrix realization of `Cl(1,3)`.

### Definitions

- explicit complex `4×4` gamma matrices.
- metric `η = diag(1,-1,-1,-1)`.

### Теоремы

- `gamma_anticomm`:
  `{γ^μ,γ^ν}=2η^{μν}I`.
- `bivector_count = 6` for commutators `[γ^μ,γ^ν]` with `μ<ν`.
- negative controls:
  - Euclidean all-plus signature does not satisfy `B_N=-I` role assignment;
  - fifth gamma requires extra terminal role.

### Bridge boundary

Full Lie group `SO⁺(1,3)` and `Spin(1,3)` can be in bridge layer initially. Core closes Clifford finite carrier.

### PASS

- Explicit matrices compile and anticommutator proof passes.

---

## P8. Gauge/matter/Ward/anomaly bridge

### Цель
Lean formalizes exact rational anomaly sums and finite boundary identity.

### Definitions

- one generation of left-handed Weyl fields with rational hypercharges:
  - `Q_L`: multiplicity `3*2`, `Y=1/6`
  - `u_R^c`: multiplicity `3`, `Y=-2/3`
  - `d_R^c`: multiplicity `3`, `Y=1/3`
  - `L_L`: multiplicity `2`, `Y=-1/2`
  - `e_R^c`: multiplicity `1`, `Y=1`
  - optional `ν_R^c`: multiplicity `1`, `Y=0`

### Теоремы

- `grav_U1_anomaly_sum = 0`
- `U1_cubic_anomaly_sum = 0`
- `SU2_SU2_U1_anomaly_sum = 0`
- `SU3_SU3_U1_anomaly_sum = 0`
- `boundary_boundary_zero` for finite incidence matrices.

### Guardrail

Separate:

1. topological no-3-simplex internal carrier;
2. representation-trace anomaly cancellation.

### PASS

- All anomaly sums exact over `ℚ`.
- No floating approximations.

---

## P9. High-gain hostile uniqueness atlas in Lean

### Цель
Move simple high-gain arithmetic to Lean; keep heavy physics in Python certs.

### Core Lean arithmetic targets

- `readout306 = 18*17 = 306`
- `lambdaAct38 = 2*(2*10-1) = 38`
- `depth99 = 9*11 = 99`
- `ew35 = totient 710 / 8 = 35`
- `unlock19 = 2*10 - 1 = 19`
- `lambdaRoots`: if using rationals/sqrt, prove `λ_c,λ_r` roots of `160x²-480x+359` in bridge real layer.

### Negative controls

Formalize predicates where possible:

- off-diagonal complete directed no-loop count requires `n(n-1)`;
- dropping one channel breaks completeness;
- adding one channel requires external sink.

### PASS

- Arithmetic atlas compiles.
- Narrative uniqueness not encoded as comments only; use predicates for completeness/minimality where possible.

---

## P10. Condensed/profinite formal layer

### Цель
Formal skeleton of D0 condensed support without overclaim.

### Definitions

- `ProjectiveSystem` over directed preorder/index category;
- finite stages `S_N : Type`, `[Fintype S_N]`;
- bonding maps `π_{M,N}`;
- inverse limit as subtype of product satisfying compatibility;
- representable functor `T ↦ ContinuousMap T S` if mathlib topology is manageable; otherwise finite/profinite skeleton first.

### Theorems

- projection compatibility;
- finite-stage operator family naturality predicate;
- if operators commute with projections, they induce an operator on inverse limit.

### PASS

- No vague “condensed” claims in Lean core.
- If full `Condensed` machinery is too expensive, implement profinite inverse-limit skeleton and label as `ProfiniteSupport`, not full condensed theorem.

---

## P11. φ-discrete RG bridge

### Цель
Formalize finite-difference RG scaffold.

### Core

- define scale sequence `μ k = Λ * φ^(-k)` over reals;
- define finite difference `βφ g k = (g(k+1)-g(k))/log φ`;
- prove algebraic identities of scaling sequence.

### Bridge assumptions

- smooth interpolation;
- scheme-specific RG kernels;
- thresholds.

### PASS

- No claim that SM 2-loop beta functions are fully derived until proved.

---

## P12. Smooth metric bridge

### Цель
Formalize assumptions, not fake full differential geometry.

### Lean target

- structure `CovarianceSystem` with `G_N`, projections, compatibility;
- structure `HeatTraceAssumptions` with convergence/Weyl asymptotics as fields;
- theorem: under assumptions, bridge status can be promoted.

### External/CI target

- Python cert `vp_covariance_stabilization.py` computes a concrete finite `G_N` family;
- heat-trace numeric checks.

### PASS

- Smoothness theorem remains conditional unless actual assumptions are verified.

---

## 5. Claim-to-Lean mapping policy

Create `D0/TheoremLedger/ClaimMap.lean` and a generated CSV:

```
claim_id, lean_module, lean_theorem, status, cert, book_section, release_gate
```

Statuses:

- `LEAN_CORE_PROVED`
- `LEAN_BRIDGE_ASSUMPTIONS_EXPLICIT`
- `PYTHON_CERT_REQUIRED`
- `EMPIRICAL_DATA_REQUIRED`
- `NOT_IN_LEAN_SCOPE`

No claim may be release-promoted unless it has at least one of:

- `LEAN_CORE_PROVED`
- `LEAN_BRIDGE_ASSUMPTIONS_EXPLICIT + Python cert`
- `PYTHON_CERT_REQUIRED + passing cert + data hash`

---

## 6. CI requirements

Required commands:

```
lake build
python 05_CERTS/run_all_core_certs.py
python 05_CERTS/run_all_bridge_certs.py
python 05_CERTS/run_all_empirical_passports.py
python tools/build_release_ledger.py
python tools/check_no_sorry_in_core.py
python tools/check_claim_map_coverage.py
```

Release fails if:

- `sorry` appears in `D0/Core`, `D0/Combinatorics`, `D0/Topology`, `D0/Gauge`;
- `axiom` appears outside `D0/Bridge/Assumptions`;
- any active claim lacks `lean/cert/passport` mapping;
- any Python cert result missing or stale;
- any external data file lacks hash.

---

## 7. Deliverable structure for IDE agent

```
D0LeanFormalization/
  D0/...
  certs/
  data/
  tools/
  docs/
    FORMALIZATION_STATUS.md
    CLAIM_TO_LEAN_MAP.csv
    ASSUMPTIONS_REGISTER.md
    BRIDGE_THEOREM_REGISTER.md
    RELEASE_CRITERIA.md
```

Every PR/iteration must update:

1. Lean theorem files;
2. `CLAIM_TO_LEAN_MAP.csv`;
3. `FORMALIZATION_STATUS.md`;
4. cert runners if affected;
5. active books only if formal statement changed.

---

## 8. Work order

### Milestone M1 — Compiling algebraic core

- P0, P1, P2.
- Expected result: `p+p²=1`, `δ₀`, `ABCD`, `Ω₈`, `V₉,V₁₁,V₁₃` proved.

### Milestone M2 — Finite scene and phase unfolding

- P3, P4, P5 partial.
- Expected result: `K(9,11,13)` counts, no 3-simplices, forced windows `44/710`, Euler counts.

### Milestone M3 — Finite quantum/operator core

- P6, P7, P8.
- Expected result: finite Born response, Clifford check, Ward/anomaly finite exact sums.

### Milestone M4 — High-gain arithmetic and cert lock

- P9 + Python cert integration.
- Expected result: Lean proves arithmetic locks; Python certs prove larger numerical passports.

### Milestone M5 — Bridge formalization

- P10, P11, P12.
- Expected result: bridge assumptions are explicit, no hidden continuum postulates.

### Milestone M6 — Release hardening

- full claim coverage, CI, docs, no sorry in core.

---

## 9. Definition of done

### v12-alpha

- `lake build` passes.
- M1+M2 complete.
- `D0/Core` and `D0/Combinatorics` no `sorry`, no `axiom`.

### v12-beta

- M1–M4 complete.
- finite Born, Clifford, anomaly sums compiled.
- release cert runners pass.

### v12-release

- M1–M6 complete.
- every active claim mapped.
- theorem/status database generated from source ledger.
- clean docs and release archive.

---

## 10. Non-negotiable rules

1. No `Float` in Lean proofs.
2. No hidden `axiom` in core.
3. No theorem named as proved if it is assumption-dependent.
4. No physical passport promoted by Lean arithmetic alone.
5. No “D0 term” without standard math object.
6. No status rewrite without proof/cert/assumption update.
7. Every bridge must state its external assumptions.
8. Every empirical claim must have data hash and runner.

---

## 11. First IDE task packet

Give IDE agent exactly this first packet:

```
TASK M1.1: Create Lean 4 + mathlib Lake project.
TASK M1.2: Replace Float PositiveResponseSplit by exact Real theorem.
TASK M1.3: Prove role/omega/V9/V11/V13 cardinalities.
TASK M1.4: Create ClaimMap.csv rows for D0-FOUND-001, D0-PHI-HURWITZ-001, D0-PHASE-UNFOLD-002.
TASK M1.5: Add CI check: fail on Float/axiom/sorry in D0/Core.
```

Acceptance:

```
lake build PASS
python tools/check_no_sorry_in_core.py PASS
CLAIM_TO_LEAN_MAP.csv has all M1 claims mapped
```

---

## v12.24 Active closure direction

The next phase is not a broad rewrite.  It is the closure of the active map by proving the remaining structural bridges that connect the finite archive/action layer to the primitive languages used by effective theories.

Key closure goals:

```text
1. Constrained conserved stress representative
   raw curvature gradient
   → admissible symmetric row-sum-zero representative
   → same variation pairing.

2. Non-vacuous scalar Poisson reduction
   scalar potential ansatz
   → scalar Laplacian variation
   → stationarity
   → graph Poisson equation.

3. Nonzero generated matter source neutrality
   MatterRep / generated carrier
   → archive phase localization
   → source density ρ_R
   → anomaly/charge neutrality
   → ∑ ρ_R = 0.

4. Fast Lean iteration architecture
   frozen proved interfaces
   → active theorem index
   → full hard closure only at release.
```

These are key goals, not a new theory map.  The existing map remains the closure target; this section only states the active proof bottlenecks.

## v12.24 Lean monolith refactor requirement

The current monolithic build loop is too slow for theorem development.  The required refactor is:

```text
Frozen modules:
  stable proved theorems and definitions.

Interface modules:
  small theorem-only exports used downstream.

Active modules:
  current theorem targets and local helper lemmas.

ActiveClosureIndex:
  #check only current iteration targets.

HardClosureTheoremIndex:
  full release gate, unchanged in authority but not used as the edit loop.
```

Acceptance:

```text
lake build D0.Active.<CurrentTarget>            -- normal edit loop
lake build D0.TheoremLedger.ActiveClosureIndex -- active gate
python tools/run_hard_theorem_closure.py --mode active
python tools/run_hard_theorem_closure.py --mode full --release
```

No active theorem file may import `D0.All` or the full hard closure index.
