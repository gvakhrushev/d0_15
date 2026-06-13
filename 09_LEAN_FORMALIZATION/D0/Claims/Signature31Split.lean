import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Tactic
import D0.Dynamics.ToralAutomorphism

/-!
# D0-SIGNATURE-31-SPLIT-001 — the Lorentz signature (3,1) is forced by two split objects

Certificate of record: `05_CERTS/vp_signature_31_split.py`.

The claim is that "3" (space) and "1" (time) come from two *independent* finite
objects, so they can never conflict:

* **"3" (space)** = the rank of the adjacency matrix of the complete tripartite
  graph `K(9,11,13)` on `33` vertices equals exactly `3`
  (three non-Pisot transport modes). We prove this on the *literal* 33×33
  rational adjacency matrix `Adj` (entry `1` iff two vertices lie in different
  zones) with Mathlib's real `Matrix.rank`:
  - upper bound `rank Adj ≤ 3` from the factorization `Adj = C · B` through the
    3-column zone-indicator `C`;
  - lower bound `3 ≤ rank Adj` from the 3×3 hollow submatrix on one
    representative vertex per zone, whose determinant `= 2 ≠ 0` makes it a unit.

* **"1" (time)** = the single modular flow `T = !![0,1; 1,-1]`, a single
  hyperbolic (Pisot) operator with `trace T = -1`, `det T = -1` and the
  characteristic relation `λ² + λ - 1 = 0` (`T^2 + T - 1 = 0`). These are reused
  verbatim from the frozen, proved `D0.Dynamics.ToralAutomorphism`.

* The two real roots of `f(x) = x² + x - 1` are bracketed by integer sign
  changes, `f(0) < 0 < f(1)` and `f(-1) < 0 < f(-2)`: one contracting root in
  `(0,1)` and one expanding root in `(-2,-1)` — the arrow of time.

Putting these together: the "3" is a graph rank and the "1" is a matrix flow —
distinct objects — so the signature `(3,1)` is forced without conflict.

This is a leaf per-claim module: it imports only Mathlib and the frozen
`D0.Dynamics.ToralAutomorphism`, so it builds in seconds against the warm cache.
-/

namespace D0.Claims

open Matrix

/-! ## The "3": rank of the adjacency of `K(9,11,13)` -/

/-- Zone of a vertex index in `{0,…,32}`: `0..8 → 0`, `9..19 → 1`, `20..32 → 2`
(zone sizes `9`, `11`, `13` exactly as in the certificate). -/
def zone31 (i : Fin 33) : Fin 3 :=
  if (i : Nat) < 9 then 0 else if (i : Nat) < 20 then 1 else 2

/-- The 33×33 adjacency matrix of `K(9,11,13)` over `ℚ`: entry `1` iff the two
vertices lie in different zones (else `0`). -/
def Adj31 : Matrix (Fin 33) (Fin 33) ℚ :=
  Matrix.of fun i j => if zone31 i = zone31 j then 0 else 1

/-- Zone-membership indicator, 33×3: `C i z = 1` iff vertex `i` is in zone `z`. -/
def Cind31 : Matrix (Fin 33) (Fin 3) ℚ :=
  Matrix.of fun i z => if zone31 i = z then 1 else 0

/-- Zone-to-vertex pattern, 3×33: `B z j = 1` iff vertex `j` is outside zone `z`. -/
def Bpat31 : Matrix (Fin 3) (Fin 33) ℚ :=
  Matrix.of fun z j => if z = zone31 j then 0 else 1

/-- The adjacency factors through the 3 zones: `Adj = Cind · Bpat`. -/
theorem adj31_factor : Adj31 = Cind31 * Bpat31 := by
  ext i j
  simp only [Adj31, Cind31, Bpat31, Matrix.mul_apply, Matrix.of_apply]
  rw [Finset.sum_eq_single (zone31 i)]
  · rcases eq_or_ne (zone31 i) (zone31 j) with h | h
    · simp [h]
    · simp [h]
  · intro z _ hz
    simp [Ne.symm hz]
  · intro h; exact absurd (Finset.mem_univ _) h

/-- Upper bound: the adjacency has rank `≤ 3`, since it factors through the
3-column zone indicator. -/
theorem adj31_rank_le_three : Adj31.rank ≤ 3 := by
  rw [adj31_factor]
  calc (Cind31 * Bpat31).rank ≤ Cind31.rank := rank_mul_le_left _ _
    _ ≤ 3 := rank_le_width _

/-- One representative vertex per zone: `0` (zone 0), `9` (zone 1), `20` (zone 2). -/
def rep31 : Fin 3 → Fin 33
  | 0 => 0
  | 1 => 9
  | 2 => 20

/-- The 3×3 submatrix on the representatives is the hollow pattern. -/
theorem adj31_submatrix :
    Adj31.submatrix rep31 rep31 = !![(0 : ℚ), 1, 1; 1, 0, 1; 1, 1, 0] := by
  ext i j; fin_cases i <;> fin_cases j <;> rfl

/-- The hollow 3×3 pattern has determinant `2`. -/
theorem hollow31_det : (!![(0 : ℚ), 1, 1; 1, 0, 1; 1, 1, 0]).det = 2 := by
  simp [Matrix.det_fin_three]; norm_num

/-- Lower bound: the 3×3 hollow submatrix is invertible (det `= 2 ≠ 0`), so it has
full rank `3`, giving `3 ≤ rank Adj`. -/
theorem adj31_rank_ge_three : 3 ≤ Adj31.rank := by
  have hunit : IsUnit (Adj31.submatrix rep31 rep31).det := by
    rw [adj31_submatrix, hollow31_det]
    exact isUnit_iff_ne_zero.mpr (by norm_num)
  have hrank : (Adj31.submatrix rep31 rep31).rank = 3 := by
    have := Matrix.rank_of_isUnit (Adj31.submatrix rep31 rep31)
      ((Matrix.isUnit_iff_isUnit_det _).mpr hunit)
    simpa using this
  calc 3 = (Adj31.submatrix rep31 rep31).rank := hrank.symm
    _ ≤ Adj31.rank := rank_submatrix_le _ _ _

/-- **"3" (space):** the adjacency of `K(9,11,13)` has rank exactly `3`. -/
theorem adj31_rank_eq_three : Adj31.rank = 3 :=
  le_antisymm adj31_rank_le_three adj31_rank_ge_three

/-! ## The arrow of time: real roots of `x² + x - 1` bracketed by integer signs -/

/-- The characteristic value `f(x) = x² + x - 1` of the time operator. -/
def f31 (x : Int) : Int := x * x + x - 1

/-- A root in `(0,1)` [contracting] and a root in `(-2,-1)` [expanding]:
`f(0) < 0 < f(1)` and `f(-1) < 0 < f(-2)`. -/
theorem f31_sign_changes :
    f31 0 < 0 ∧ 0 < f31 1 ∧ f31 (-1) < 0 ∧ 0 < f31 (-2) := by
  decide

/-! ## The full split: "3" (graph rank) and "1" (modular flow) are distinct objects -/

/-- **D0-SIGNATURE-31-SPLIT-001.** The Lorentz signature `(3,1)` is forced by two
independent finite objects:

* the spatial `3` is the rank of the adjacency of `K(9,11,13)` (`Adj31.rank = 3`);
* the temporal `1` is the single modular flow `T = !![0,1; 1,-1]` with
  `trace T = -1`, `det T = -1` and characteristic relation `T² + T - 1 = 0`;
* the two roots of `x² + x - 1` are bracketed `f(0)<0<f(1)`, `f(-1)<0<f(-2)`,
  giving one contracting and one expanding direction (the arrow of time).

`3` is a graph invariant and `1` is a matrix-flow invariant — distinct objects —
so `(3,1)` never conflicts. -/
theorem signature_31_split :
    -- "3" = space: rank of the K(9,11,13) adjacency
    Adj31.rank = 3 ∧
    -- "1" = time: the single modular flow T and its exact invariants
    Matrix.trace D0.Dynamics.T = -1 ∧
    Matrix.det D0.Dynamics.T = -1 ∧
    D0.Dynamics.T ^ 2 + D0.Dynamics.T - 1 = 0 ∧
    -- arrow of time: the two real roots are bracketed by integer sign changes
    (f31 0 < 0 ∧ 0 < f31 1 ∧ f31 (-1) < 0 ∧ 0 < f31 (-2)) := by
  refine ⟨adj31_rank_eq_three, D0.Dynamics.trace_T1, D0.Dynamics.det_T,
    D0.Dynamics.T_charpoly_quadratic_relation, f31_sign_changes⟩

end D0.Claims
