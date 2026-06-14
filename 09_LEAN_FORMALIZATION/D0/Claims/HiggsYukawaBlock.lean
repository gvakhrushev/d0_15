import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

/-!
# D0-HIGGS-YUKAWA-001 — finite Yukawa block is Hermitian + scalar-projector compatible

Python certificate: `05_CERTS/vp_higgs_yukawa_section_transfer.py` (exact rational).

On the minimal carrier `R ⊕ (L ⊗ φ)` (dims 1,1,2), the Yukawa map `Y : R → φ` is
`Y = (1, 1/2)ᵀ`, and the full block operator `[[0, Yᵀ],[Y, 0]]` is Hermitian; the rank-2
scalar projector `P_φ = I₂` is compatible (`P_φ · Y = Y`). All exact over `ℚ`.
-/

namespace D0.Claims

open Matrix

/-- Full Yukawa block `[[0, Yᵀ],[Y, 0]]` on `R ⊕ (L ⊗ φ)` (R first, then the 2D φ leg). -/
def yukawaBlock : Matrix (Fin 3) (Fin 3) ℚ := !![0, 1, 1/2; 1, 0, 0; 1/2, 0, 0]

/-- The rank-2 scalar projector on the φ leg. -/
def pPhi : Matrix (Fin 2) (Fin 2) ℚ := !![1, 0; 0, 1]

/-- The Yukawa leg `Y : R → φ`. -/
def yLeg : Matrix (Fin 2) (Fin 1) ℚ := !![1; 1/2]

/-- The block operator is Hermitian (symmetric over `ℝ`/`ℚ`). -/
theorem yukawa_block_hermitian : yukawaBlock = yukawaBlockᵀ := by native_decide

/-- Scalar-projector compatibility: `P_φ · Y = Y`. -/
theorem yukawa_projector_compatible : pPhi * yLeg = yLeg := by native_decide

/-- A rank-1 projector that kills the second φ component breaks compatibility (control). -/
theorem yukawa_rank1_projector_breaks : (!![1, 0; 0, 0] : Matrix (Fin 2) (Fin 2) ℚ) * yLeg ≠ yLeg := by
  native_decide

/-- **D0-HIGGS-YUKAWA-001.** The finite Yukawa block is Hermitian and compatible with the
rank-2 scalar projector, and a rank-1 projector is rejected. -/
theorem higgs_yukawa_block :
    yukawaBlock = yukawaBlockᵀ ∧ pPhi * yLeg = yLeg ∧
    (!![1, 0; 0, 0] : Matrix (Fin 2) (Fin 2) ℚ) * yLeg ≠ yLeg :=
  ⟨yukawa_block_hermitian, yukawa_projector_compatible, yukawa_rank1_projector_breaks⟩

end D0.Claims
