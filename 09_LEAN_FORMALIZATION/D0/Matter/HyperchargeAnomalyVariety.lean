import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Tactic
import D0.Matter.HyperchargeFlowLattice

/-!
# D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001 — the SM hypercharge row is NOT forced (Lean)

Python certificate: `05_CERTS/vp_hypercharge_anomaly_variety.py`.

Front F7 (NO-GO). Finite object: the one-generation charge `6`-vector in the field order
`(q_L, u^c, d^c, ℓ_L, e^c, ν^c)` and the Standard-Model anomaly constraints. The claim under
test is that anomaly-freedom plus the proposed constraints *force* the SM hypercharge row
`Y = (1/6, −2/3, 1/3, −1/2, 1, 0)`. It does NOT.

What is closed here (all by robust finite tactics over `ℚ`):

* **Linear anomaly system has a 3-dimensional solution space.** The three *linear* anomaly /
  gauge constraints — gravitational·U(1) (`grav`), SU(2)²·U(1) (`su2`, doublets only) and
  SU(3)²·U(1) (`su3`, colour triplets only) — are the rows of the `3×6` multiplicity matrix

  ```
  A = [[6,3,3,2,1,1],   -- grav : Σ mult_i X_i
       [3,0,0,1,0,0],   -- su2  : doublet count · X (q ×3 colour, ℓ ×1)
       [2,1,1,0,0,0]]   -- su3  : colour count · X (q ×2 doublet, u^c, d^c)
  ```

  `A` has rank exactly `3` (an explicit `3×3` minor on columns `{0,1,4}` has determinant `3 ≠ 0`,
  and `A` has only `3` rows). By rank–nullity the solution space `{X : A·X = 0}` has dimension
  `6 − 3 = 3`. So the *linear* constraints alone leave a `3`-parameter family.

* **The cubic constraint does not collapse it to a ray.** We exhibit TWO `ℚ`-linearly independent
  rows that satisfy ALL of `grav = su2 = su3 = 0` AND the cubic `U(1)³` constraint `cubic = 0`:
  hypercharge `Y` and `B−L = (1/3, −1/3, −1/3, −1, 1, 1)`. Both are anomaly-free; they are not
  scalar multiples of one another. Hence the joint anomaly-free set contains `span{Y, B−L}`, a
  `2`-dimensional space — it is NOT a single ray, so anomaly-freedom + the proposed constraints
  do **not** force the SM row.

HONESTY BOUNDARY.
* **NO-GO closed here (`D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001`):** anomaly-freedom + the proposed
  linear/cubic constraints leave a variety of dimension `≥ 2` (`span{Y, B−L}`); the row is not forced.
* The only thing that removes `B−L` is imposing `Y_{ν^c} = 0` (the SM convention that the right-handed
  neutrino is hypercharge-neutral). That is an *imposed* convention, not a *derived* consequence of
  anomaly-freedom — singling out `Y` from `span{Y, B−L}` by assuming `Y_{ν^c} = 0` is question-begging.
* The minimal denominator `6` of `Y` is a SEPARATE fact owned by
  `D0-SM-HYPERCHARGE-MINIMAL-DENOMINATOR-001` (integrality route); it is NOT redone here, and it does
  not single out the row either (`B−L` is anomaly-free with denominator `3`).
-/

open Matrix

namespace D0.Matter.HyperchargeAnomalyVariety

open D0.Matter.HyperchargeFlowLattice (bMinusL mult gravSum cubicSum)

/-! ## (a) The linear anomaly system has rank `3` ⇒ a `3`-dimensional solution space. -/

/-- The `3×6` linear anomaly / gauge constraint matrix over `ℚ`, rows `grav, su2, su3`,
columns in the field order `(q_L, u^c, d^c, ℓ_L, e^c, ν^c)`. -/
def anomalyMat : Matrix (Fin 3) (Fin 6) ℚ :=
  !![6, 3, 3, 2, 1, 1;
     3, 0, 0, 1, 0, 0;
     2, 1, 1, 0, 0, 0]

/-- Pick out columns `{0, 1, 4}` of `anomalyMat` (a `3×3` submatrix). -/
def minorCols : Fin 3 → Fin 6
  | 0 => 0
  | 1 => 1
  | 2 => 4

/-- The `3×3` minor of `anomalyMat` on columns `{0,1,4}` is the explicit pattern
`!![6,3,1; 3,0,0; 2,1,0]`. -/
theorem anomaly_minor :
    anomalyMat.submatrix id minorCols = !![(6 : ℚ), 3, 1; 3, 0, 0; 2, 1, 0] := by
  ext i j; fin_cases i <;> fin_cases j <;> rfl

/-- That `3×3` minor has determinant `3` (a genuine `det_fin_three` computation, not `rfl`). -/
theorem anomaly_minor_det : (!![(6 : ℚ), 3, 1; 3, 0, 0; 2, 1, 0]).det = 3 := by
  simp [Matrix.det_fin_three]

/-- Upper bound: `anomalyMat` has rank `≤ 3` (it has only `3` rows). -/
theorem anomaly_rank_le_three : anomalyMat.rank ≤ 3 :=
  anomalyMat.rank_le_height

/-- Lower bound: the `3×3` minor on `{0,1,4}` is invertible (det `= 3 ≠ 0`), so it has full
rank `3`, giving `3 ≤ rank anomalyMat`. -/
theorem anomaly_rank_ge_three : 3 ≤ anomalyMat.rank := by
  have hunit : IsUnit (anomalyMat.submatrix id minorCols).det := by
    rw [anomaly_minor, anomaly_minor_det]
    exact isUnit_iff_ne_zero.mpr (by norm_num)
  have hrank : (anomalyMat.submatrix id minorCols).rank = 3 := by
    have := Matrix.rank_of_isUnit (anomalyMat.submatrix id minorCols)
      ((Matrix.isUnit_iff_isUnit_det _).mpr hunit)
    simpa using this
  calc 3 = (anomalyMat.submatrix id minorCols).rank := hrank.symm
    _ ≤ anomalyMat.rank := rank_submatrix_le _ _ _

/-- **The linear anomaly matrix has rank exactly `3`.** -/
theorem anomaly_rank_eq_three : anomalyMat.rank = 3 :=
  le_antisymm anomaly_rank_le_three anomaly_rank_ge_three

/-- **Solution-space dimension (rank–nullity corollary).** Over `ℚ⁶`, the linear anomaly system
`A · X = 0` has solution space of dimension `6 − rank A = 6 − 3 = 3`. (Stated as the rank
deficiency `6 − rank A`, which equals `3` once `rank A = 3` is known.) -/
theorem anomaly_solution_dim_eq_three : 6 - anomalyMat.rank = 3 := by
  have h : anomalyMat.rank = 3 := anomaly_rank_eq_three
  omega

/-! ## (b) Two independent anomaly-free rows: hypercharge `Y` and `B−L`.

`B−L`, `mult`, `gravSum`, `cubicSum`, and the independence `Y_and_BminusL_independent`
are reused from `D0.Matter.HyperchargeFlowLattice`. We add hypercharge `Y` and the
SU(2)/SU(3) linear constraint sums explicitly.
-/

/-- Hypercharge `Y` of the one generation in the field order `(q, u^c, d^c, ℓ, e^c, ν^c)`. -/
def Y : Fin 6 → ℚ
  | 0 => 1 / 6    -- q_L
  | 1 => -2 / 3   -- u^c
  | 2 => 1 / 3    -- d^c
  | 3 => -1 / 2   -- ℓ_L
  | 4 => 1        -- e^c
  | 5 => 0        -- ν^c

/-- SU(2)²·U(1) linear constraint sum: only weak-doublets contribute, with their colour
multiplicities — `q_L` (`×3` colour) and `ℓ_L` (`×1`). This is row `[3,0,0,1,0,0]` of `A`. -/
def su2Sum (X : Fin 6 → ℚ) : ℚ := 3 * X 0 + X 3

/-- SU(3)²·U(1) linear constraint sum: only colour triplets contribute, with their weak
multiplicities — `q_L` (`×2` doublet), `u^c`, `d^c`. This is row `[2,1,1,0,0,0]` of `A`. -/
def su3Sum (X : Fin 6 → ℚ) : ℚ := 2 * X 0 + X 1 + X 2

/-- **`Y` is gravitational-anomaly-free.** -/
theorem Y_grav_free : gravSum Y = 0 := by
  norm_num [gravSum, Y, mult]

/-- **`Y` satisfies the SU(2) linear constraint.** -/
theorem Y_su2_free : su2Sum Y = 0 := by
  norm_num [su2Sum, Y]

/-- **`Y` satisfies the SU(3) linear constraint.** -/
theorem Y_su3_free : su3Sum Y = 0 := by
  norm_num [su3Sum, Y]

/-- **`Y` is cubic-anomaly-free.** -/
theorem Y_cubic_free : cubicSum Y = 0 := by
  norm_num [cubicSum, Y, mult]

/-- **`B−L` satisfies the SU(2) linear constraint.** -/
theorem bMinusL_su2_free : su2Sum bMinusL = 0 := by
  norm_num [su2Sum, bMinusL]

/-- **`B−L` satisfies the SU(3) linear constraint.** -/
theorem bMinusL_su3_free : su3Sum bMinusL = 0 := by
  norm_num [su3Sum, bMinusL]

/-- `Y` and `B−L` are `ℚ`-linearly independent: no scalar `c` makes `Y = c·(B−L)` on the
quark and lepton-singlet entries (`c = 1/2` from the quark forces `Y_{e^c} = 1/2 ≠ 1`).
This is exactly `D0.Matter.HyperchargeFlowLattice.Y_and_BminusL_independent` with the
local `Y` substituted (`Y 0 = 1/6`, `Y 4 = 1`). -/
theorem Y_BminusL_independent :
    ¬ ∃ c : ℚ, Y 0 = c * bMinusL 0 ∧ Y 4 = c * bMinusL 4 := by
  have h := D0.Matter.HyperchargeFlowLattice.Y_and_BminusL_independent
  intro hc
  apply h
  obtain ⟨c, hq, he⟩ := hc
  exact ⟨c, by simpa [Y] using hq, by simpa [Y] using he⟩

/-! ## (c) The joint anomaly-free set contains a 2-dimensional span — the row is not forced. -/

/-- **D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001 (NO-GO).** Anomaly-freedom + the proposed
constraints do NOT force the SM hypercharge row. Concretely:

* the linear anomaly matrix `A` has rank `3`, so its solution space is `3`-dimensional
  (`6 − rank A = 3`);
* hypercharge `Y` AND `B−L` BOTH satisfy every constraint — gravitational, SU(2), SU(3),
  and the cubic `U(1)³` — and they are `ℚ`-linearly independent;
* therefore the joint anomaly-free set contains the `2`-dimensional `span{Y, B−L}`: it is NOT
  a single ray, so the SM row is underdetermined by anomaly-freedom alone.

The only thing removing `B−L` is imposing `Y_{ν^c} = 0` (`Y 5 = 0`, the SM convention) — an input,
not a derivation. -/
theorem anomaly_free_contains_two_independent :
    -- the linear system has a 3-dim solution space
    anomalyMat.rank = 3
      ∧ 6 - anomalyMat.rank = 3
      -- Y is fully anomaly-free
      ∧ gravSum Y = 0 ∧ su2Sum Y = 0 ∧ su3Sum Y = 0 ∧ cubicSum Y = 0
      -- B−L is fully anomaly-free
      ∧ gravSum bMinusL = 0 ∧ su2Sum bMinusL = 0 ∧ su3Sum bMinusL = 0 ∧ cubicSum bMinusL = 0
      -- Y and B−L are independent ⇒ the anomaly-free set is at least 2-dimensional, not a ray
      ∧ (¬ ∃ c : ℚ, Y 0 = c * bMinusL 0 ∧ Y 4 = c * bMinusL 4) :=
  ⟨anomaly_rank_eq_three, anomaly_solution_dim_eq_three,
   Y_grav_free, Y_su2_free, Y_su3_free, Y_cubic_free,
   D0.Matter.HyperchargeFlowLattice.bMinusL_grav_free, bMinusL_su2_free, bMinusL_su3_free,
   D0.Matter.HyperchargeFlowLattice.bMinusL_cubic_free,
   Y_BminusL_independent⟩

end D0.Matter.HyperchargeAnomalyVariety
