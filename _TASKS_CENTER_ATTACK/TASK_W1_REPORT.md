# TASK W1 — Report: exact Ihara–Bass certificate + NB/E family audit

Deliverable cert: `vp_scene_ihara_bass_nb.py` (this folder; **not** placed in `05_CERTS/`, **not**
registered — kept out of the CI cert glob by design). Runtime ≈ 16.5 s on the local interpreter
(python 3.9.6 + numpy). All PASS/FAIL logic is integer/modular; no floats in any decision.

## 1. Family audit (read-only) — W / NB / E, and whether NB = E

Source of record: `09_LEAN_FORMALIZATION/D0/VNext2/SceneNativeRefinementClassification.lean`,
`04_VERIFICATION/VNEXT2_REFINEMENT_FAMILY_CLASSIFICATION.csv`,
`04_VERIFICATION/VNEXT2_SCENE_NATIVE_NO_GO_ATLAS.md`. Owning rows:
`D0-VNEXT2-SCENE-NATIVE-REFINEMENT-OWNER-001` / `-NOGO-001` (Outcome D), status **NO-GO**, Lean
`scene_native_refinement_underdetermined`, missing primitive `PRIM-SCENE-HISTORY-REFINEMENT-RULE`.

The three admissible history families, verbatim (`SceneNativeRefinementClassification.lean:11–17`):

- **W (all finite walks)** — "vertex-level transfer = adjacency `A` (carrier `H_scene`, dim 33)".
- **NB (non-backtracking walks)** — "transfer = Hashimoto operator on directed edges (dim `2|E| = 718`)".
- **E (directed-edge / de Bruijn history)** — "directed-edge carrier (dim `2|E| = 718`)".

Inequivalence, verbatim (`:15–17`): "at depth 2 the all-walks carrier is `Σ nᵢ·degᵢ² = 15708`, the
non-backtracking carrier is `Σ nᵢ·degᵢ(degᵢ−1) = 14990` — differing by exactly the `2|E| = 718`
backtracks. The vertex-transfer dim `33` differs from the directed-edge dim `718`." The no-go
(`VNEXT2_SCENE_NATIVE_NO_GO_ATLAS.md:6`): "≥2 admissible families (all-walks, non-backtracking,
directed-edge) give inequivalent carriers".

**NB-vs-E answer (the deliverable question): NB and E are NOT the same operator, but they are not two
different carriers either — they are one carrier with two dynamics.** Both act on the *same* 718-dim
directed-edge space (`2|E|`). They differ precisely by the backtracking transitions:

- **E / de Bruijn** is the full directed-edge adjacency: `(u→v) ↦ (v→w)` for **every** out-edge of `v`,
  including the immediate reversal `w = u`.
- **NB / Hashimoto `B`** is the *same* map with the reversal deleted: `(u→v) ↦ (v→w)`, `w ≠ u`.

So `E_operator = B + (backtracking transitions)`, and the 718 backtracking entries are exactly the
`2|E|` depth-2 excess that already separates W from NB. In the corpus's own words the three are
"inequivalent" families; the sharper statement — that NB and E share a carrier and differ only by the
backtrack channel — is the structural content the cert isolates below. The classification file does not
assert NB ≡ E; it lists them as distinct rows, which is consistent with "same carrier, different
operator".

The Ihara–Bass identity discriminates the two dynamics on that shared carrier: the identity holds for
the **non-backtracking** `B` and **fails** for the backtracking (E / de Bruijn) operator (cert check [3]
vs negative control (i)). External owner for "why the graph object is intrinsically non-backtracking":
Terras, *Zeta Functions of Graphs* (the graph zeta is a product over backtrackless primitive cycles) and
Bass 1992 (the Ihara–Bass identity, whose core needs no regularity hypothesis) — see `TASK_W5_REPORT.md`.

## 2. Certificate results (exact)

| check | statement | result |
|---|---|---|
| [1] | `|V|=33, |E|=359, 2|E|=718`, zone degrees `(24,22,20)`, `rank_ℚ(A)=3` (fraction-free) | PASS |
| [2] | `Σd²=15708`, `Σd(d−1)=14990`, excess `=718=2|E|`; backtrack length-2 walks `=718=` #directed edges (bijection) | PASS |
| [3] | Ihara–Bass `det(I−uB) = (1−u²)^{326}·det(I−uA+u²(D−I))` at `u ∈ {1/3, 1/7, −2/5, 2/9, 3/11}`, each mod 3 large primes (`10⁹+7, 998244353, 10⁹+9`) | PASS |
| [4] | FINDING: the rank-3 adjacency spectrum = spectrum of the zone quotient `Q=[[0,11,13],[9,0,13],[9,11,0]]`, whose charpoly is `λ³ − 359λ − 2574` (the §08.12.4 "vacuum cubic") | PASS |

`|E|−|V| = 359 − 33 = 326` is the Bass exponent used in [3].

**Negative controls (all reachable, all fire):**

| control | expectation | result |
|---|---|---|
| (i) | Hashimoto with backtracking transitions included (the E/de Bruijn operator) → Ihara–Bass **breaks** | PASS (control fires) |
| (ii) | `K(9,11,15)`: invariants change to `(399, 798, 18420) ≠ (359, 718, 15708)` → cert **detects** | PASS (control fires) |
| (iii) | wrong Bass exponent `326±1` → identity **breaks** | PASS (control fires) |

The cert exits non-zero if any check or any control fails to fire. Method note (matches the brief's
recommended route): the `718×718` determinant `det(I−uB)` is evaluated by clearing `u`'s denominator and
taking the determinant of the integer matrix modulo three ~`10⁹` primes (numpy `int64` Gaussian
elimination, `p² < 2⁶³`); the `33×33` right side is done the same way; agreement is checked in each
`𝔽_p`. Five rational `u` × three primes = fifteen independent modular witnesses of the identity.

## 3. Scope (honest)

- What the cert establishes: the exact *structural* facts behind candidate theorem T1 on `K(9,11,13)` —
  the depth-2 backtrack count is `2|E|` and is in bijection with directed edges; the Ihara–Bass identity
  relates the `718`-dim non-backtracking edge transfer to the `33`-dim scene data `(A, D)` and singles
  out the non-backtracking dynamics against the backtracking one; and the rank-3 adjacency spectrum
  equals the zone-quotient "vacuum cubic" (stated as a FINDING, not a fork resolution).
- What it does **not** establish: it does not promote NB to *the* scene-native refinement rule. The
  vNext2 verdict `D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001` (Outcome D) stands as recorded — W, NB, E
  remain inequivalent admissible families, and the completion class `PRIM-SCENE-HISTORY-REFINEMENT-RULE`
  remains the named missing primitive. T1's claim that NB is *canonical* needs that primitive (or the
  external owner sweep of `TASK_W5_REPORT.md`), not this cert. A surprise worth recording: the
  discriminator between NB and E is not a new axiom but the Ihara–Bass identity itself — the same object
  that glues NB to the scene is the one that rejects E.
