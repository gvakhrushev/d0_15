import D0.Algebra.OriginalBookLocalBoost
import D0.Geometry.OriginalBookJuliaWords
import Mathlib.Tactic

/-!
# Local representatives of original static Julia roots

The source uses 1-(1/5)cc† and 1-(1/5)c†c for all baseline roots and,
except for the moved D mode, for live roots. The fixed original source is
uniform blob ee8de4635d24c668949ac9a0186616ab7d59f2ed, lines 77–87,
and modular blob d111c5bfeae3c384a4fe725f4a6d19277ea0005a, lines 143–157,
at commit eebcb5e467742df3e9cf7fa9702042d7294aa742. Their complex images
are the previously proved actual positive CFC roots; both modular images use
conjugation before evaluation. Moved D roots and effects are separate steps.
-/
open D0
open Matrix
open D0.Algebra.OriginalBookRadicalLocal
open D0.Algebra.OriginalBookRadicalMod1009
open D0.Algebra.OriginalBookRadicalSourceConstants
open D0.Algebra.OriginalBookLocalCreators
open D0.Geometry.OriginalBookBoost
open D0.Geometry.OriginalBookStaticRoots
open D0.Geometry.OriginalBookJuliaWords

namespace D0.Algebra.OriginalBookLocalStaticRoots

/-- In the source local ring, 1/5=1762/8810. -/
noncomputable def localInv5 : LocalSource := 1762 * localInvD

lemma complexInv5 : localSourceToComplex localInv5 = (1 / 5 : ℂ) := by
  simp [localInv5, complexInvD, map_ofNat]
  norm_num

lemma modInv5 : redPlus localInv5 = (1 / 5 : ZMod 1009) := by
  simp only [localInv5, map_mul, map_ofNat, modInvD]
  decide

lemma localInv5_star : star localInv5 = localInv5 := by
  apply localSourceToComplex_injective
  rw [localSourceToComplex_star, complexInv5]
  simp

lemma modInv5_minus : redMinus localInv5 = (1 / 5 : ZMod 1009) := by
  change redPlus (star localInv5) = _
  rw [localInv5_star, modInv5]

/-- Exact baseline (and unboosted live) source root representatives. -/
noncomputable def localStaticLeft (r : Role) : LocalOperator :=
  1 - localInv5 • (localCreator r * (localCreator r)ᴴ)

noncomputable def localStaticRight (r : Role) : LocalOperator :=
  1 - localInv5 • ((localCreator r)ᴴ * localCreator r)

/-- The complex images are the actual source baseline positive roots. -/
theorem localStaticLeft_complex (r : Role) :
    (localStaticLeft r).map localSourceToComplex = baseLeft r := by
  have hc (i j : Fin 16) : localSourceToComplex (localCreator r i j) = sourceCreatorComplex r i j := by
    exact congrArg (fun M : Matrix (Fin 16) (Fin 16) ℂ => M i j) (localCreator_complex r)
  ext bra ket
  by_cases h : bra = ket <;>
    simp [localStaticLeft, baseLeft, leftProjection, Matrix.mul_apply, localSourceToComplex_star,
      complexInv5, hc, h]

theorem localStaticRight_complex (r : Role) :
    (localStaticRight r).map localSourceToComplex = baseRight r := by
  have hc (i j : Fin 16) : localSourceToComplex (localCreator r i j) = sourceCreatorComplex r i j := by
    exact congrArg (fun M : Matrix (Fin 16) (Fin 16) ℂ => M i j) (localCreator_complex r)
  ext bra ket
  by_cases h : bra = ket <;>
    simp [localStaticRight, baseRight, rightProjection, Matrix.mul_apply, localSourceToComplex_star,
      complexInv5, hc, h]

/-- For every source role except D, the live root has the same exact value. -/
theorem localStaticLeft_live (r : Role) (h : r ≠ D) :
    (localStaticLeft r).map localSourceToComplex = liveLeft r := by
  rw [localStaticLeft_complex]
  simp [liveLeft, baseLeft, h]

theorem localStaticRight_live (r : Role) (h : r ≠ D) :
    (localStaticRight r).map localSourceToComplex = liveRight r := by
  rw [localStaticRight_complex]
  simp [liveRight, baseRight, h]

/-- The first modular evaluation uses the original conjugate creator transpose. -/
theorem localStaticLeft_mod (r : Role) :
    (localStaticLeft r).map redPlus = 1 - (1 / 5 : ZMod 1009) •
      ((localCreator r).map redPlus * ((localCreator r).map redMinus).transpose) := by
  ext bra ket
  by_cases h : bra = ket <;>
    simp [localStaticLeft, Matrix.mul_apply, redMinus, starRingEnd_apply, modInv5, h]

theorem localStaticRight_mod (r : Role) :
    (localStaticRight r).map redPlus = 1 - (1 / 5 : ZMod 1009) •
      (((localCreator r).map redMinus).transpose * (localCreator r).map redPlus) := by
  ext bra ket
  by_cases h : bra = ket <;>
    simp [localStaticRight, Matrix.mul_apply, redMinus, starRingEnd_apply, modInv5, h]

/-- Conjugate evaluation of a local star equals the first evaluation. -/
lemma redMinus_star (x : LocalSource) : redMinus (star x) = redPlus x := by
  change redPlus (star (star x)) = _
  simp

/-- The conjugate evaluation uses the opposite evaluation in the dagger. -/
theorem localStaticLeft_mod_minus (r : Role) :
    (localStaticLeft r).map redMinus = 1 - (1 / 5 : ZMod 1009) •
      ((localCreator r).map redMinus * ((localCreator r).map redPlus).transpose) := by
  ext bra ket
  by_cases h : bra = ket <;>
    simp [localStaticLeft, Matrix.mul_apply, redMinus_star, modInv5_minus, h]

theorem localStaticRight_mod_minus (r : Role) :
    (localStaticRight r).map redMinus = 1 - (1 / 5 : ZMod 1009) •
      (((localCreator r).map redPlus).transpose * (localCreator r).map redMinus) := by
  ext bra ket
  by_cases h : bra = ket <;>
    simp [localStaticRight, Matrix.mul_apply, redMinus_star, modInv5_minus, h]

end D0.Algebra.OriginalBookLocalStaticRoots
