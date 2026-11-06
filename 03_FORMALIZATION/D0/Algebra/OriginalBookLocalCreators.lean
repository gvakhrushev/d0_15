import D0.Algebra.OriginalBookRadicalMod1009
import D0.Geometry.OriginalBookBoost
import Mathlib.Tactic

/-!
# Local model for the actual four source creators

Pinned source uniform blob ee8de4635d24c668949ac9a0186616ab7d59f2ed,
lines 51–61, and modular blob d111c5bfeae3c384a4fe725f4a6d19277ea0005a,
lines 76–86, both at eebcb5e467742df3e9cf7fa9702042d7294aa742.
The matrix entries reuse the already proved source/CAR bit correspondence.
The generic dagger lemmas carry actual local conjugation to complex conjugation
and to the separate modular conjugate evaluation. This file does not yet
construct the Julia roots, Walsh rows, reduced K/effects, or a rank certificate.
-/
open D0
open Matrix
open D0.Geometry.OriginalBookCreatorBridge
open D0.Geometry.OriginalBookBoost
open D0.Algebra.OriginalBookRadicalLocal
open D0.Algebra.OriginalBookRadicalMod1009

namespace D0.Algebra.OriginalBookLocalCreators

abbrev LocalOperator := Matrix (Fin 16) (Fin 16) LocalSource

/-- The literal source creator entries, now in the faithful local ring. -/
def localCreator (role : Role) : LocalOperator :=
  fun bra ket => (sourceCreator (sourceBit role) bra ket : LocalSource)

/-- The complex image is the existing actual source/CAR creator matrix. -/
theorem localCreator_complex (role : Role) :
    (localCreator role).map localSourceToComplex = sourceCreatorComplex role := by
  ext bra ket
  simp [localCreator, sourceCreatorComplex, sourceCreatorMatrix]

/-- Both modular evaluations use the same literal integer source creator. -/
theorem localCreator_mod (role : Role) :
    (localCreator role).map redPlus =
      fun bra ket => (sourceCreator (sourceBit role) bra ket : ZMod 1009) := by
  ext bra ket
  simp [localCreator]

/-- The conjugate evaluation agrees on the real integer creator entries. -/
theorem localCreator_mod_conjugate (role : Role) :
    (localCreator role).map redMinus =
      fun bra ket => (sourceCreator (sourceBit role) bra ket : ZMod 1009) := by
  ext bra ket
  simp [localCreator, redMinus]
/-- Local dagger maps to the actual complex conjugate-transpose. -/
theorem localDagger_complex (M : LocalOperator) :
    Mᴴ.map localSourceToComplex = (M.map localSourceToComplex)ᴴ := by
  ext bra ket
  simp [Matrix.conjTranspose_apply, localSourceToComplex_star]

/-- Modular dagger is evaluated through the conjugate map before transposition. -/
theorem localDagger_mod (M : LocalOperator) :
    Mᴴ.map redPlus = (M.map redMinus).transpose := by
  ext bra ket
  simp [Matrix.conjTranspose_apply, redMinus, starRingEnd_apply]

end D0.Algebra.OriginalBookLocalCreators
