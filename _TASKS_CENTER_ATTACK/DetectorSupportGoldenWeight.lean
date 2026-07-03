import Mathlib.NumberTheory.Real.GoldenRatio
import Mathlib.Topology.Category.Profinite.AsLimit
import Mathlib.Topology.Category.Profinite.CofilteredLimit
import Mathlib.Tactic

/-!
# Detector-support golden weight (DRAFT; entry-contract §00.3/§00.4 anchor)

BOOK_00 §00.4 posits the primitive support `S_D0 = {A,B}^ℕ` with weights `μ(A) = φ⁻¹, μ(B) = φ⁻²`.
This module supplies the first Lean owner of the MEASURE layer and its load-bearing identity:

**The detector closure `p + p² = 1` (§00.3, owned) IS the Kolmogorov consistency of the golden
Bernoulli weight**: refining any cylinder by one more readout letter preserves its weight EXACTLY
because `φ⁻¹ + φ⁻² = 1`. A non-golden branch pair (e.g. `1/2, 1/4`) fails consistency — the
negative control. The profinite carrier itself follows the repo's existing archive pattern
(`ArchiveLightProfinite`, Clausen–Scholze stack in Mathlib); this module owns the weight algebra.
No registry row edited; lives in _TASKS_CENTER_ATTACK until minted.
-/

namespace D0.CondensedAnchor

open Real
open scoped goldenRatio

/-- **The detector closure as an identity of the golden ratio:** `φ⁻¹ + φ⁻² = 1`.
This is `p + p² = 1` at `p = φ⁻¹` — the §00.3 closure, in Mathlib's `goldenRatio`. -/
theorem inv_gold_closure : φ⁻¹ + (φ⁻¹) ^ 2 = 1 := by
  have h1 : φ⁻¹ = φ - 1 := by rw [inv_goldenRatio, ← one_sub_goldenConj]; ring
  rw [h1]
  nlinarith [goldenRatio_sq]

/-- Golden weight of a finite readout word (cylinder): product of per-letter branch weights,
`true ↦ φ⁻¹` (direct), `false ↦ φ⁻²` (return). -/
noncomputable def cylWeight : List Bool → ℝ
  | [] => 1
  | b :: w => (if b then φ⁻¹ else (φ⁻¹) ^ 2) * cylWeight w

@[simp] theorem cylWeight_nil : cylWeight [] = 1 := rfl

/-- **Kolmogorov consistency = detector closure.** Splitting any cylinder by one further readout
letter preserves its weight: `w ↦ {w·A, w·B}` is weight-exact, BECAUSE `φ⁻¹ + φ⁻² = 1`. -/
theorem cylWeight_refine (w : List Bool) :
    cylWeight (w.concat true) + cylWeight (w.concat false) = cylWeight w := by
  induction w with
  | nil => simpa [cylWeight] using inv_gold_closure
  | cons b w ih =>
      simp only [List.concat_cons, cylWeight]
      rw [← mul_add, ih]

/-- Total mass of the level-1 partition is 1 (probability normalization at the first readout). -/
theorem level_one_mass : cylWeight [true] + cylWeight [false] = 1 := by
  simpa using cylWeight_refine []

/-- **Negative control:** the non-golden branch pair `(1/2, 1/4)` fails the closure — a fair-coin
detector cannot satisfy the §00.3 closure; the golden pair is not a convention. -/
theorem non_golden_control : ¬ ((1/2 : ℝ) + (1/2 : ℝ) ^ 2 = 1) := by norm_num

/-! ## Anchor 1b — the φ-self-return clause and the gap-module seam

The §00.4 subfunctor clause "φ self-return" at the weight layer: the return branch carries the
squared direct weight (definitional here; the closure makes it consistent). And the SEAM to the
owned K-theory row (`D0.Claims.KTheoryGapModule`, the Bellissard owner-edge): **every golden
cylinder weight lies in the rank-2 gap-label module ℤ + ℤφ⁻¹** — the measure layer and the
gap-label layer share one module. (The owned row holds the module's defining relations; this
theorem proves the measure lands in it — cross-reference, not duplication.) -/

/-- §00.4 φ-self-return at the weight layer: the return branch weight is the square of the
direct branch weight. -/
theorem cylWeight_return (w : List Bool) :
    cylWeight (false :: w) = (φ⁻¹) ^ 2 * cylWeight w := by
  simp [cylWeight]

/-- The direct branch carries one factor φ⁻¹. -/
theorem cylWeight_direct (w : List Bool) :
    cylWeight (true :: w) = φ⁻¹ * cylWeight w := by
  simp [cylWeight]

/-- `φ⁻² = 1 − φ⁻¹` (the module's defining relation, from the closure). -/
theorem inv_gold_sq : (φ⁻¹) ^ 2 = 1 - φ⁻¹ := by
  have h := inv_gold_closure; linarith

/-- The weight exponent of a word: direct letters cost 1, return letters cost 2. -/
def weightExp : List Bool → ℕ
  | [] => 0
  | b :: w => (if b then 1 else 2) + weightExp w

/-- Every cylinder weight is a pure power: `cylWeight w = (φ⁻¹) ^ weightExp w`. -/
theorem cylWeight_eq_pow (w : List Bool) : cylWeight w = (φ⁻¹) ^ weightExp w := by
  induction w with
  | nil => simp [cylWeight, weightExp]
  | cons b w ih =>
      cases b <;> simp [cylWeight, weightExp, ih, pow_add]

/-- Powers of `φ⁻¹` lie in `ℤ + ℤφ⁻¹` (signed-Fibonacci coefficients, recursion (a,b) ↦ (b, a−b)). -/
theorem inv_gold_pow_mem (k : ℕ) : ∃ a b : ℤ, (φ⁻¹) ^ k = (a : ℝ) + (b : ℝ) * φ⁻¹ := by
  induction k with
  | zero => exact ⟨1, 0, by norm_num⟩
  | succ n ih =>
      obtain ⟨a, b, h⟩ := ih
      refine ⟨b, a - b, ?_⟩
      have : (φ⁻¹ : ℝ) ^ (n + 1) = ((a : ℝ) + (b : ℝ) * φ⁻¹) * φ⁻¹ := by
        rw [pow_succ, h]
      rw [this]
      calc ((a : ℝ) + (b : ℝ) * φ⁻¹) * φ⁻¹
          = (a : ℝ) * φ⁻¹ + (b : ℝ) * (φ⁻¹) ^ 2 := by ring
        _ = (a : ℝ) * φ⁻¹ + (b : ℝ) * (1 - φ⁻¹) := by rw [inv_gold_sq]
        _ = ((b : ℤ) : ℝ) + (((a - b : ℤ)) : ℝ) * φ⁻¹ := by push_cast; ring

/-- **The gap-module seam:** every golden cylinder weight lies in ℤ + ℤφ⁻¹ — the same rank-2
module as the K-theory gap labels of the golden hull (`D0.Claims.KTheoryGapModule` holds the
defining relations; Bellissard owner-edge holds the external theorem). The measure layer and the
gap-label layer share one module. -/
theorem cylWeight_mem_gap_module (w : List Bool) :
    ∃ a b : ℤ, cylWeight w = (a : ℝ) + (b : ℝ) * φ⁻¹ := by
  rw [cylWeight_eq_pow]
  exact inv_gold_pow_mem (weightExp w)

/-! ## Anchor 2 — the finite-factorization clause of §00.4 is a THEOREM, not a constraint

BOOK_00 §00.4 lists "finite factorization" among the defining constraints of the D0-admissible
readout subfunctor `M^D0(S_D0^φ) ⊂ Hom_Top(S, X)`. For finite-valued (locally constant) readouts
of ANY profinite support this clause holds automatically — it is owned by Mathlib
(`Profinite.exists_locallyConstant` over the canonical tower `Profinite.asLimit`). Consequence for
the entry contract: the constraint content of the admissible subfunctor lives entirely in the
REMAINING clauses (φ self-return, quadratic response, single-section, gate stationarity,
archive/active separation) — finite factorization is free. -/

open CategoryTheory in
/-- **Finite factorization is automatic**: every locally constant readout of a profinite detector
support factors through a finite quotient level of its canonical tower. -/
theorem readout_factors_through_finite_level (S : Profinite) {α : Type*}
    (f : LocallyConstant S α) :
    ∃ (j : DiscreteQuotient S) (g : LocallyConstant (S.diagram.obj j) α),
      f = g.comap (S.asLimitCone.π.app j).hom.hom :=
  Profinite.exists_locallyConstant S.asLimitCone S.asLimit f

end D0.CondensedAnchor
