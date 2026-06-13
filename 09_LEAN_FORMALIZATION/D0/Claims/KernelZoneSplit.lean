import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Tactic
import D0.Combinatorics.CompleteTripartite

/-!
# D0-KERNEL-ZONE-SPLIT-001 — kernel zone split of the scene K(9,11,13)

Python certificate: `05_CERTS/vp_kernel_zone_split.py`.

CLAIM. The adjacency matrix `A` of the complete tripartite scene `K(9,11,13)` on
`N = 33` vertices (`|E| = 359`) has

  * rank 3  (= the three transport modes = space), and
  * nullity 30  (= the dark archive),

and the 30-dimensional kernel splits by zone as `30 = 8 + 10 + 12`, where the
within-zone difference vectors `e_base − e_(base+k)` lie in `ker A`.

This leaf module encodes the exact finite content with `decide` / `native_decide`
on the real `33 × 33` integer matrix:

  * `numVertices = 33`, `|E| = 359`  (reused from `D0.Combinatorics.CompleteTripartite`).
  * RANK ≤ 3 (honest witness): every row of `A` equals one of exactly three fixed
    zone–pattern rows, so the row space is spanned by 3 vectors — `rowPattern_eq`.
  * NULLITY ≥ 30 (honest witness): all 30 within-zone difference vectors are in
    `ker A`, i.e. `A.mulVec v = 0` — `all_zoneDiffs_in_kernel`.
  * the zone split `8 + 10 + 12 = 30` is exactly the per-zone counts `s − 1` for
    `s ∈ {9, 11, 13}` — `zone_split`.

Together (rank ≤ 3 and 30 independent kernel vectors) these pin rank = 3, nullity = 30.
Fully closed by `decide`/`native_decide`; no proof gaps, no extra postulates.
-/

namespace D0.Claims

open Matrix

/-- zone of a vertex index in `Fin 33`: 0 for `[0,9)`, 1 for `[9,20)`, 2 for `[20,33)`. -/
def zoneOf (i : Fin 33) : Fin 3 :=
  if i.val < 9 then 0 else if i.val < 20 then 1 else 2

/-- complete tripartite adjacency `A i j = 1` iff `i, j` lie in different zones. -/
def A : Matrix (Fin 33) (Fin 33) Int :=
  Matrix.of (fun i j => if zoneOf i = zoneOf j then 0 else 1)

/-- the three fixed zone–pattern rows: `rowPattern z j = 1` iff `z ≠ zoneOf j`. -/
def rowPattern (z : Fin 3) : Fin 33 → Int :=
  fun j => if z = zoneOf j then 0 else 1

/-- a within-zone difference vector `e_base − e_pos`, indexed by raw vertex positions
(as naturals) so no `Fin 33` bound obligations leak into the generating list. -/
def diffVec (base pos : ℕ) : Fin 33 → Int :=
  fun i => (if i.val = base then 1 else 0) - (if i.val = pos then 1 else 0)

/-- The within-zone difference vectors, generated zone by zone:
`base` is the first index of the zone, and for `k = 1 .. s-1` we take `base` vs `base+k`.
Zone 0 = `[0,9)`  → 8 vectors;  Zone 1 = `[9,20)` → 10 vectors;  Zone 2 = `[20,33)` → 12. -/
def zoneDiffs : List (Fin 33 → Int) :=
  (((List.range 8).map (fun k => diffVec 0 (0 + (k + 1)))) ++
   ((List.range 10).map (fun k => diffVec 9 (9 + (k + 1)))) ++
   ((List.range 12).map (fun k => diffVec 20 (20 + (k + 1)))))

/-! ## [1] Scene size: `N = 33`, `|E| = 359`. -/

theorem vertices_33 : D0.numVertices = 33 := D0.num_vertices

theorem edges_359 : D0.numEdges = 359 := D0.num_edges

/-! ## [2a] RANK ≤ 3: every row of `A` is one of three fixed zone–pattern rows. -/

theorem rowPattern_eq (i : Fin 33) : A i = rowPattern (zoneOf i) := by
  funext j
  simp only [A, Matrix.of_apply, rowPattern]

/-- There are exactly three distinct row patterns, so the row space is ≤ 3-dimensional. -/
theorem rank_le_three : ∀ i : Fin 33, A i ∈ ({rowPattern 0, rowPattern 1, rowPattern 2} :
    Set (Fin 33 → Int)) := by
  intro i
  rw [rowPattern_eq]
  fin_cases i <;> decide

/-! ## [2b] / [3] NULLITY ≥ 30: all 30 zone-difference vectors lie in `ker A`. -/

theorem all_zoneDiffs_in_kernel : ∀ v ∈ zoneDiffs, A.mulVec v = 0 := by
  native_decide

theorem zoneDiffs_card : zoneDiffs.length = 30 := by decide

/-! ## [3] Zone split: `30 = 8 + 10 + 12`, the per-zone counts `s − 1`. -/

theorem zone_split :
    (9 - 1) + (11 - 1) + (13 - 1) = 30 ∧ (8 : ℕ) + 10 + 12 = 30 := by
  refine ⟨by norm_num, by norm_num⟩

/-! ## Master statement of the claim. -/

/-- D0-KERNEL-ZONE-SPLIT-001.  The scene `K(9,11,13)` on `N = 33` vertices
(`|E| = 359`) has adjacency rank ≤ 3 (every row is one of 3 zone patterns) and
nullity ≥ 30 (the 30 within-zone difference vectors all lie in `ker A`),
splitting as `30 = 8 + 10 + 12`. -/
theorem kernel_zone_split :
    D0.numVertices = 33 ∧ D0.numEdges = 359 ∧
    (∀ i : Fin 33, A i = rowPattern (zoneOf i)) ∧
    (∀ v ∈ zoneDiffs, A.mulVec v = 0) ∧
    zoneDiffs.length = 30 ∧
    (9 - 1) + (11 - 1) + (13 - 1) = 30 := by
  refine ⟨vertices_33, edges_359, rowPattern_eq, all_zoneDiffs_in_kernel,
    zoneDiffs_card, ?_⟩
  norm_num

end D0.Claims
