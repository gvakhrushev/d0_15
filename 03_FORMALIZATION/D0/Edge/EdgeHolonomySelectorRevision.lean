import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Edge.RamificationFromUeEffCompanion
import D0.Integration.V15.EdgeAudit

/-!
# D0-EDGE-HOLONOMY-SELECTOR-REVISION-001

## Structural Analysis of PRIM-EDGE-HOLONOMY-SELECTOR: Frozen Return vs. Twisted Deformation

This module formalizes the exact bifurcation regarding `PRIM-EDGE-HOLONOMY-SELECTOR`:
1. In `D0.Edge.RamificationFromUeEffCompanion`, the companion blocks satisfy:
   $$C_4(\lambda)^4 = \lambda \cdot I_4, \quad R_3(\lambda)^3 = \lambda \cdot I_3.$$
2. **Terminal Return Preservation**:
   The frozen terminal operator owns exact integer returns:
   - 4-cycle on the terminal capacity sector: $C_4^4 = I_4$;
   - 3-cycle on the scene rank sector: $R_3^3 = I_3$;
   - Total order $\operatorname{lcm}(4, 3) = 12$.
3. Under the constraint that the edge cover preserves these unramified terminal returns:
   $$\lambda \cdot I_4 = I_4 \iff \lambda = 1.$$
   Hence the choice $\lambda = 1$ is **uniquely forced**, eliminating `PRIM-EDGE-HOLONOMY-SELECTOR`
   as an independent frozen primitive.
4. If $\lambda \ne 1$ ($\lambda \in U(1)$) is permitted, it represents a **twisted deformation family**
   (non-trivial holonomy / boundary twist), rather than an incomplete frozen core construction.
-/

namespace D0.Edge.EdgeHolonomySelectorRevision

open Matrix
open D0.Edge
open D0.Integration.V15.EdgeAudit

/-- The inherited terminal return condition for the 4-cycle capacity block:
$$C_4(\lambda)^4 = I_4.$$ -/
def PreservesCapacityReturn (lam : ℚ) : Prop :=
  (companionC4 lam) ^ 4 = (1 : Matrix (Fin 4) (Fin 4) ℚ)

/-- The inherited terminal return condition for the 3-cycle rank block:
$$R_3(\lambda)^3 = I_3.$$ -/
def PreservesRankReturn (lam : ℚ) : Prop :=
  (companionR3 lam) ^ 3 = (1 : Matrix (Fin 3) (Fin 3) ℚ)

/-- **D0-EDGE-HOLONOMY-SELECTOR-REVISION-001 (Theorem 1)**:
Preserving the capacity return uniquely forces $\lambda = 1$. -/
theorem capacity_return_forces_unit_holonomy (lam : ℚ) :
    PreservesCapacityReturn lam ↔ lam = 1 := by
  unfold PreservesCapacityReturn
  rw [companionC4_cyclic]
  constructor
  · intro h
    have h00 := congr_fun (congr_fun h 0) 0
    simp [Matrix.smul_apply] at h00
    exact h00
  · rintro rfl
    simp

/-- **D0-EDGE-HOLONOMY-SELECTOR-REVISION-001 (Theorem 2)**:
Preserving the scene-rank return uniquely forces $\lambda = 1$. -/
theorem rank_return_forces_unit_holonomy (lam : ℚ) :
    PreservesRankReturn lam ↔ lam = 1 := by
  unfold PreservesRankReturn
  rw [companionR3_cyclic]
  constructor
  · intro h
    have h00 := congr_fun (congr_fun h 0) 0
    simp [Matrix.smul_apply] at h00
    exact h00
  · rintro rfl
    simp

/-- **D0-EDGE-HOLONOMY-SELECTOR-REVISION-001 (Bifurcation Master Theorem)**:
Either the edge cover preserves the frozen terminal cycles (which forces $\lambda = 1$ uniquely,
removing the primitive selector), or $\lambda$ belongs to a post-core twisted deformation family. -/
theorem edge_holonomy_bifurcation :
    (∀ lam : ℚ, (PreservesCapacityReturn lam ∧ PreservesRankReturn lam) ↔ lam = 1) ∧
    PreservesCapacityReturn 1 ∧
    ¬ PreservesCapacityReturn 2 := by
  refine ⟨fun lam => ?_, ?_, ?_⟩
  · constructor
    · intro ⟨h4, _⟩
      exact (capacity_return_forces_unit_holonomy lam).mp h4
    · rintro rfl
      exact ⟨(capacity_return_forces_unit_holonomy 1).mpr rfl,
             (rank_return_forces_unit_holonomy 1).mpr rfl⟩
  · exact (capacity_return_forces_unit_holonomy 1).mpr rfl
  · intro h2
    have h_eq := (capacity_return_forces_unit_holonomy 2).mp h2
    norm_num at h_eq

end D0.Edge.EdgeHolonomySelectorRevision
