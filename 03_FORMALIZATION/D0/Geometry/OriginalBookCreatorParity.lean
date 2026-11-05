import D0.Geometry.OriginalBookBoost
import Mathlib.Tactic

/-!
# Source creator parity from the existing Fock convention

The parity signs are those of the existing Fock carrier, related to the
original integer occupation basis by `source_parity_eq_car`. The creators are
the published `sourceCreatorComplex`, whose entries are proved equal to the
original CAR source. This file establishes only the starting parity algebra;
the Kraus/effect upper bound and effect-span lower bound are separate claims.
-/
open D0
open D0.Geometry.OriginalBookCreatorBridge
open D0.Geometry.OriginalBookBoost
open Matrix

namespace D0.Geometry.OriginalBookCreatorParity

/-- Parity in the original integer bit basis, prior to complex embedding. -/
def sourceParityInt (bits : Fin 16) : ℤ :=
  if (([0, 1, 2, 3] : List Nat).filter bits.val.testBit).length % 2 = 0 then 1 else -1

/-- This is the existing typed Fock parity, not a new parity choice. -/
theorem sourceParityInt_eq_fock (bits : Fin 16) :
    (sourceParityInt bits : ℝ) = fockParitySign (sourceState bits) := by
  rw [source_parity_eq_car]
  simp only [sourceParityInt]
  split <;> norm_num

/-- Parity operator on the actual 16-state source basis. -/
def sourceParity : Matrix (Fin 16) (Fin 16) ℂ :=
  Matrix.diagonal fun bits => (sourceParityInt bits : ℂ)

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_0 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 0 =
      -(sourceCreator (sourceBit r) bra 0 * sourceParityInt 0) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_1 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 1 =
      -(sourceCreator (sourceBit r) bra 1 * sourceParityInt 1) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_2 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 2 =
      -(sourceCreator (sourceBit r) bra 2 * sourceParityInt 2) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_3 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 3 =
      -(sourceCreator (sourceBit r) bra 3 * sourceParityInt 3) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_4 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 4 =
      -(sourceCreator (sourceBit r) bra 4 * sourceParityInt 4) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_5 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 5 =
      -(sourceCreator (sourceBit r) bra 5 * sourceParityInt 5) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_6 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 6 =
      -(sourceCreator (sourceBit r) bra 6 * sourceParityInt 6) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_7 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 7 =
      -(sourceCreator (sourceBit r) bra 7 * sourceParityInt 7) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_8 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 8 =
      -(sourceCreator (sourceBit r) bra 8 * sourceParityInt 8) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_9 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 9 =
      -(sourceCreator (sourceBit r) bra 9 * sourceParityInt 9) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_10 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 10 =
      -(sourceCreator (sourceBit r) bra 10 * sourceParityInt 10) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_11 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 11 =
      -(sourceCreator (sourceBit r) bra 11 * sourceParityInt 11) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_12 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 12 =
      -(sourceCreator (sourceBit r) bra 12 * sourceParityInt 12) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_13 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 13 =
      -(sourceCreator (sourceBit r) bra 13 * sourceParityInt 13) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_14 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 14 =
      -(sourceCreator (sourceBit r) bra 14 * sourceParityInt 14) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_parity_ket_15 : ∀ (r : Role) (bra : Fin 16),
    sourceParityInt bra * sourceCreator (sourceBit r) bra 15 =
      -(sourceCreator (sourceBit r) bra 15 * sourceParityInt 15) := by
  decide

/-- All four source creators flip the existing Fock parity. -/
theorem creator_entry_parity_int (r : Role) (bra ket : Fin 16) :
    sourceParityInt bra * sourceCreator (sourceBit r) bra ket =
      -(sourceCreator (sourceBit r) bra ket * sourceParityInt ket) := by
  fin_cases ket
  · exact creator_parity_ket_0 r bra
  · exact creator_parity_ket_1 r bra
  · exact creator_parity_ket_2 r bra
  · exact creator_parity_ket_3 r bra
  · exact creator_parity_ket_4 r bra
  · exact creator_parity_ket_5 r bra
  · exact creator_parity_ket_6 r bra
  · exact creator_parity_ket_7 r bra
  · exact creator_parity_ket_8 r bra
  · exact creator_parity_ket_9 r bra
  · exact creator_parity_ket_10 r bra
  · exact creator_parity_ket_11 r bra
  · exact creator_parity_ket_12 r bra
  · exact creator_parity_ket_13 r bra
  · exact creator_parity_ket_14 r bra
  · exact creator_parity_ket_15 r bra

/-- Operator forms of the existing parity sign. -/
theorem sourceParity_hermitian : sourceParityᴴ = sourceParity := by
  ext bra ket
  by_cases h : bra = ket
  · subst ket
    simp [sourceParity, sourceParityInt, Matrix.conjTranspose_apply]
    split <;> norm_num
  · simp [sourceParity, Matrix.conjTranspose_apply, h, Ne.symm h]

theorem sourceParity_sq : sourceParity * sourceParity = 1 := by
  ext bra ket
  by_cases h : bra = ket
  · subst ket
    simp [sourceParity, sourceParityInt]
    split <;> norm_num
  · simp [sourceParity, h]

/-- Creator oddness uses the actual source matrices with no physical assumption. -/
theorem creator_odd (r : Role) :
    sourceParity * sourceCreatorComplex r = -(sourceCreatorComplex r * sourceParity) := by
  ext bra ket
  have h : (sourceParityInt bra : ℂ) * (sourceCreator (sourceBit r) bra ket : ℂ) =
      -((sourceCreator (sourceBit r) bra ket : ℂ) * (sourceParityInt ket : ℂ)) := by
    exact_mod_cast creator_entry_parity_int r bra ket
  simpa [sourceParity, sourceCreatorComplex, sourceCreatorMatrix,
    Matrix.diagonal_mul, Matrix.mul_diagonal] using h

end D0.Geometry.OriginalBookCreatorParity
