import Mathlib.Tactic

/-!
# Hist_D0 — the finite/profinite history source category (Section 1.1)

Objects are finite D0 record states `(S_N, R_N, D_min, Δ, P_N, Q_N, U_N, terminal readout)`, modelled by the
history depth `N` plus the six structural invariants that every admissible morphism must preserve (canonical
code, binary distinguishability, history order, terminal readout, retained/archive split, finite response).
A morphism is an admissible refinement/coarsening: it lowers (or fixes) depth, preserves all invariants, and
introduces **no** chosen root / path orientation / generation label / spectral window / external coordinate.
-/

namespace D0.Extensions.HistoryCategory

/-- A finite D0 record state: depth `N`, all six structural invariants present, and a no-chosen-data flag. -/
structure HistObject where
  level : ℕ
  invariants : Bool       -- the six preserved invariants all present
  noChosenData : Bool     -- no root/orientation/label/window/coordinate

/-- The six invariants every morphism must preserve. -/
def invariantCount : ℕ := 6
theorem six_invariants : invariantCount = 6 := by decide

/-- An admissible refinement morphism `X ⟶ Y` (Y coarser): depth non-increasing, invariants on both, no chosen data. -/
def Mor (X Y : HistObject) : Prop :=
  Y.level ≤ X.level ∧ X.invariants = true ∧ Y.invariants = true ∧
    X.noChosenData = true ∧ Y.noChosenData = true

/-- Identity morphism on an admissible object. -/
theorem mor_id (X : HistObject) (hi : X.invariants = true) (hc : X.noChosenData = true) : Mor X X :=
  ⟨le_refl _, hi, hi, hc, hc⟩

/-- Composition (refinement order is transitive). -/
theorem mor_comp {X Y Z : HistObject} (h₁ : Mor X Y) (h₂ : Mor Y Z) : Mor X Z :=
  ⟨le_trans h₂.1 h₁.1, h₁.2.1, h₂.2.2.1, h₁.2.2.2.1, h₂.2.2.2.2⟩

/-- A morphism that introduces chosen data is not admissible. -/
theorem chosen_data_rejected {X Y : HistObject} (h : X.noChosenData = false) : ¬ Mor X Y := by
  rintro ⟨_, _, _, hc, _⟩; rw [h] at hc; exact Bool.noConfusion hc

end D0.Extensions.HistoryCategory
