# D0 — Open-frontier roadmap (living)

**What this is.** The single, de-duplicated, prioritized map of every place in the theory that is
**not yet closed**. It is maintained *from the repository* — every item below points to a real
registry row (`09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv`) or a §05.6 obligation, so it
cannot drift into fog. Length, not emptiness, is the honest measure of distance to closure
(BOOK_05 §05.6 register discipline).

**How it is kept fresh.** On each iteration: (1) re-derive the open set from the registry
(PROOF-TARGET / BRIDGE-CALIBRATION / CORE_BRIDGE_SPLIT / OPEN-Lean rows + notes carrying a gap
phrase) and the §05.6 register; (2) move any newly-closed item out and record it in
`INTEGRATION_LOG.md`; (3) add any new named gap a closure leaves behind. Do **not** silently drop
an item — close it (cert+Lean+registry) or demote it honestly.

**Tiers.** T1 = D0-closeable, finite/decidable (real next work). T2 = sharpenable but
owner-edged/profinite. T3 = Mathlib-blocked (wait for Mathlib). T4 = external owners (not a D0
action). T5 = owner-decision / hygiene.

_Last synced: 2026-06-15 (Iteration 13). Registry: 258 claims, strength 3370, integrity demotions 0._

---

## Tier 1 — D0-closeable, finite/decidable (the real next work)

| item | registry anchor | status | what closes it |
|---|---|---|---|
| Q₈-orientation groupoid → `Z(Q₈)` explicit map (spinor leaf → holonomy parity) | `D0-OMEGA8-001` / §01.7.1C | PROOF-TARGET (cert obligation open) | a finite cert + decidable Lean exhibiting the map; pure group theory, no external owner |
| `D0-NO-GO-STRESS-SUITE-001` rank-one Higgs scalar-projector Lean leg | `D0-NO-GO-STRESS-SUITE-001` | open Lean theorem-target (cert-only since base-v14) | write the `FiniteScalarProjector`/`GaugeCompatible` finite API + `no_go_rank_one_higgs_scalar_projector`; finite/decidable |
| `D0-EDGE-001` trace-leg vs unitary-dilation leg | `D0-EDGE-001`/`-002` | PROOF-TARGET | owner-decision already taken: split the (closeable) trace leg `Tr(F_E)` from the open dilation/Puiseux leg; close the trace leg |
| PMNS angle-formula M1-forcing (`sin²θ₁₂=⅓−2δ₀²`, …) | `D0-PMNS-DELTA0-NUFIT-001` (EMPIRICAL-PASSPORT) | passport; forcing not attempted | attempt to derive the angle formulas from M1; **may honestly resolve to HYP/named-gap** — that is a valid outcome, not a failure |
| detection-quadratic categorical-exhaustiveness as a machine theorem | `D0-DETECTION-QUADRATIC-001` (Iter-13) | CORE for the algebra; the categorical step is forcing prose | formalize "exactly two comparison kinds" as a decidable statement (if a faithful finite model exists) — would lift the forcing reading to machine-checked |

## Tier 2 — sharpenable but owner-edged / profinite

| item | registry anchor | status | what would sharpen / close it |
|---|---|---|---|
| `Δ_α` analytic owner — two residue amplitudes (`μ₂=2¹¹π₀φ⁻²`, `μ₁=⅓`) | §05.6 obligation 4 / `D0-CVFT-F1` / `D0-DELTA-ALPHA-MOMENT-001` | OPEN, **narrowed Iter-12** (form forced; residues profinite) | the `s→pole` continuation (profinite spectral measure) fixing the two residues; needs the resolvent-trace engine |
| horizon emission / greybody leakage | `D0-CVFT-F2` | PROOF-TARGET | freeze the boundary operator + an observable passport |
| Yang–Mills leakage / mass-gap language | `D0-CVFT-F6` | PROOF-TARGET | a gauge-boundary commutator obstruction theorem (continuum YM = Clay, external) |
| `S_DE` exceptional-point algebra → DESI H₀ | `D0-CVFT-F8` | PROOF-TARGET | effective two-mode transfer only; not a cosmology closure without frozen operator + data |
| Hodge matter-gravity linking; finite A2 Einstein response | `D0-HODGE-LINKS-001`, `D0-SPECTRAL-EINSTEIN-001` | PROOF-TARGET (print-stub demoted; no quick finite witness) | a genuine finite witness for the A2 Einstein-tensor/Hodge-matter coupling |
| IceCube dynamic feedback passport | `D0-CVFT-F5` | PROOF-TARGET | a frozen operator + data manifest (empirical passport gate) |

## Tier 3 — Mathlib-blocked (wait for Mathlib / external formal kernel)

| item | registry anchor | status | blocker |
|---|---|---|---|
| K-theory / Connes spectral-triple / phason-holonomy class | `D0-KTHEORY-001`, `D0-QUASI007/008/009`, `D0-SOLENOID-001`/`-GRAVITY-001`, `D0-MESON-K0-001` | CERT-CLOSED, **EXTERNAL-GAP** (finite content cert-closed; Lean scaffold reference-only) | K-theory / spectral-triple machinery absent from Mathlib 4.30 |
| topological/measure conjugacy (`φ⁻²` rotation ↔ toral `T` foliation) | §05.6 obligation 6 | symbolic part certified; conjugacy a theorem-target | Sturm/Morse–Hedlund ergodic machinery not in the formal kernel |

## Tier 4 — external owners (cited edges; not a D0 derivation)

| item | registry anchor | status | owner |
|---|---|---|---|
| cone-speed / smooth Lorentzian metric `g_{μν}` (light-speed unit) | §07.51.3 residual of `D0-RANK3-CAUSAL-CONE-FORCING-001` | named external edge | `ASSUMP-CONNES-RECONSTRUCTION` (metric = spectrum of the Dirac operator) |
| ℍ→𝕆 octet `|Ω₈|=8` (two different eights) | `D0-FROBENIUS-DIVISION-3D-001` (Iter-13) | **HYP**, not a forcing | needs `dim 𝕆=8` (algebra) and `|Q₈|=8` (group order) identified first |
| `γ_Choptuik ↔ 3/8` packing | `D0-PACKING-LIMIT-001` | **HYP** (limits diverge: γ→½, C_max=3/8) | a common `F(D)` giving both, or accept the `D=4` coincidence |
| `S_DE` cubic-vs-quadratic fork | `D0-VACUUM-CUBIC-WINDOW-001` | both branches exact; discriminator computed | DESI DR3 selects the branch (external data) |
| Pisot ≥3-letter conjecture | (cited, time layer) | OPEN | external number theory |

## Tier 5 — owner-decision / hygiene

| item | status | disposition |
|---|---|---|
| 19 grandfathered print-stub certs (compute-but-don't-gate) | explicit ratchet (`tools/check_cert_can_fail.py`), must only shrink | rewrite-where-finite-content-exists, else leave grandfathered (owner-decision) |
| `nullity 30 = icosahedron edges` | confirmed **coincidence**, kept flagged | do not promote to a derivation (anti-numerology) |
| `K(9,11,13)` ↔ explicit `33D→3D` cut-and-project | `D0-QUASICRYSTAL-PROJECTION-001` resolved by separation (`D0-CARRIER-NOT-ICOSAHEDRAL-001`); the *explicit projection reproducing (9,11,13)* stays a named screw | do not fit the projection to (9,11,13) |

---

## Closed since the docs were drafted (do not re-open)
- `rank-3 = causal cone` — **FORCED** (Iter-11, `D0-RANK3-CAUSAL-CONE-FORCING-001`); residual is only
  the cone-speed metric (Tier 4). The unity-split (`D0-UNITY-SPLIT-SPACETIME-001`) rank-3 dependency
  routes here, it is not a fresh open gap.
- `K(9,11,13) = icosahedral` — resolved by **separation** (Iter-11, `D0-CARRIER-NOT-ICOSAHEDRAL-001`).
- §05.6 obligation 5 (tower stops at 3) — **closed** (Iter-9, `D0-TOWER-STOP-NOEXT-001`); now with a
  second independent channel (detection-types, Iter-13).
- `Δ_α` exact value + bound — **closed** (`D0-DELTA-ALPHA-EXACT-001`); the analytic owner is the
  Tier-2 obligation-4 residue, narrowed Iter-12.
