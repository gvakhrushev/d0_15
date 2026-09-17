import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecificLimits.Basic

/-!
# D0-CVFT-F7 — boundary-local holographic rank lemma (Lean lift)

Backs `04_CERTIFICATES/vp_cvft_boundary_channel_rank_REFORGED.py` (F7a) and
`04_CERTIFICATES/vp_cvft_refined_logdet_rank_bound_REFORGED.py` (F7b, scalar leg).

Typing (closure contract, `D0_CLAIM_CLOSURE_CONTRACT.md:43-52`): `F = (QUP)ᴴ (QUP)`,
`Q,P` projections, `U` unitary, so `F` is PosSemidef Hermitian. The reforged certs
verify these numerically on scene members; here F7a's rank/dim leg is a THEOREM over
any STAR-ORDERED FIELD.

Scope note (honest, per the registry `notes`): this module carries F7's **titled**
content — the boundary-local holographic RANK lemma ("supports localization only,
not an A4 proof"). The rank/dim/PSD leg (`cvft_rank_F_eq_rank_QUP`,
`cvft_rank_QUP_le_rank_P`, `cvft_rank_F_le_dim_boundary`, `cvft_scene_rank_F_le_three`,
`cvft_F_posSemidef`) and the scalar log-det inequality (`cvft_neg_log_le_geom`) are
sorry-free. The refined MATRIX log-det bound `|−log det(I−zF)| ≤ rank(F)·(−log(1−a))`
(gap G2 in `historical development memo`) remains a separate
obligation and is deliberately NOT stated here, so this module is 0-sorry.

The star-ordered-field context is required by `Matrix.rank_conjTranspose_mul_self`
and `Matrix.rank_le_card_height` (both in `Rank.lean` `section StarOrderedField`,
`variable [Fintype m] [Field R] [PartialOrder R] [StarRing R] [StarOrderedRing R]`).
`ℂ` (with `open ComplexOrder`) satisfies it, so the scene instance is covered; the
`rank_mul_le_right` localization sub-leg (`cvft_rank_QUP_le_rank_P`) holds over an
arbitrary field.
-/

namespace D0.CVFT

open Matrix

-- The star-rank lemmas `rank_conjTranspose_mul_self` / `rank_le_card_height` live in
-- `Mathlib/LinearAlgebra/Matrix/Rank.lean` `section StarOrderedField` under
-- `variable [Fintype m] [Field R] [PartialOrder R] [StarRing R] [StarOrderedRing R]`.
variable {m n : Type*} [Fintype m] [Fintype n]
variable {𝕜 : Type*} [Field 𝕜] [PartialOrder 𝕜] [StarRing 𝕜] [StarOrderedRing 𝕜]

/-- **F7a-core: rank(F) = rank(QUP).**  Direct instance of Mathlib's
`Matrix.rank_conjTranspose_mul_self` with `A := QUP`, `F := Aᴴ*A`. -/
theorem cvft_rank_F_eq_rank_QUP (QUP : Matrix m n 𝕜) :
    (QUPᴴ * QUP).rank = QUP.rank :=
  Matrix.rank_conjTranspose_mul_self QUP

/-- **F7a-localization: rank(QUP) ≤ rank(P).**  `QUP = (QU)·P`, so `rank_mul_le_right`
bounds it by `rank P`. Feedback return cannot exceed the retained support. (Plain-field
lemma — needs no star order.) -/
theorem cvft_rank_QUP_le_rank_P
    (QU : Matrix m n 𝕜) (P : Matrix n n 𝕜) :
    (QU * P).rank ≤ P.rank :=
  Matrix.rank_mul_le_right QU P

/-- **F7a-boundary: rank(F) ≤ dim of the boundary index set.**  When the feedback
return is presented on the boundary channel index type `m` (`QUP : Matrix m n`),
`rank F = rank QUP ≤ card m = dim B_boundary`.  This is the holographic bound: the
rank is capped by the number of cut/boundary channels (ROWS of `QUP`). -/
theorem cvft_rank_F_le_dim_boundary
    (QUP : Matrix m n 𝕜) :
    (QUPᴴ * QUP).rank ≤ Fintype.card m := by
  rw [Matrix.rank_conjTranspose_mul_self]
  exact Matrix.rank_le_card_height QUP

/-- **F7a scene instance: on the frozen scene rank(F) ≤ 3.**  The retained projector
has rank 3 (`D0.Claims.KernelZoneSplit`: the scene adjacency has rank 3), so every
feedback-return `F` on the scene has rank ≤ 3 — the "localization only" ceiling.
Stated abstractly in `hP : P.rank = 3` so the module carries no scene-matrix import. -/
theorem cvft_scene_rank_F_le_three
    (QU : Matrix (Fin 33) (Fin 33) ℚ) (P : Matrix (Fin 33) (Fin 33) ℚ)
    (hP : P.rank = 3) :
    (QU * P).rank ≤ 3 := by
  have := Matrix.rank_mul_le_right QU P
  rwa [hP] at this

/-- **F7a PSD typing: F is positive semidefinite Hermitian.**  Owned outright by
`Matrix.posSemidef_conjTranspose_mul_self`. -/
theorem cvft_F_posSemidef
    {R : Type*} [CommRing R] [PartialOrder R] [StarRing R] [StarOrderedRing R]
    (QUP : Matrix m n R) :
    (QUPᴴ * QUP).PosSemidef :=
  Matrix.posSemidef_conjTranspose_mul_self QUP

/-- **F7b scalar chain: -log(1-a) ≤ a/(1-a) for 0 ≤ a < 1.**  Second inequality of the
log-det chain; pure real analysis, no matrix content.
`-log(1-a) = log(1/(1-a)) ≤ 1/(1-a) - 1 = a/(1-a)` via `Real.log_le_sub_one_of_pos`. -/
theorem cvft_neg_log_le_geom {a : ℝ} (h0 : 0 ≤ a) (h1 : a < 1) :
    -Real.log (1 - a) ≤ a / (1 - a) := by
  have hpos : (0:ℝ) < 1 - a := by linarith
  have hx : (0:ℝ) < 1 / (1 - a) := by positivity
  have hlog : Real.log (1 / (1 - a)) ≤ 1 / (1 - a) - 1 :=
    Real.log_le_sub_one_of_pos hx
  rw [Real.log_div one_ne_zero (ne_of_gt hpos), Real.log_one, zero_sub] at hlog
  have : (1:ℝ) / (1 - a) - 1 = a / (1 - a) := by field_simp; ring
  linarith [this ▸ hlog]

end D0.CVFT
