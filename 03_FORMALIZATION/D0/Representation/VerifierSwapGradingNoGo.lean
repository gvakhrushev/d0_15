import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Notation
import D0.Spectrum.BranchDefectProjectiveGeneration
import D0.Representation.CompatibleInvolutionClassification

/-!
# Verifier line-swap is not the typed generation grading

The structural seed-orbit certificate uses the verifier exchange
S(x,y)=(y,x) on the defect plane F_2^2.  On the three nonzero projective
generation rays this swaps ePlus/eMinus and fixes eGap.

Its rational permutation representation on the ordered ray basis
(ePlus,eMinus,eGap) is an involution with eigensign pattern (+,-,+):
the symmetric ePlus+eMinus direction and eGap are fixed, while the
antisymmetric ePlus-eMinus direction changes sign.

That tempting (2,1) signature is nevertheless NOT enough for the typed
generation grading.  The graph-derived degree operator has distinct entries
diag(24,22,20).  The natural verifier-swap matrix exchanges the first two
degree lines and therefore does not commute with that operator.

So the verifier swap cannot silently close the grading residual.  Turning
its eigenbasis into the intrinsic degree-fibre basis would require an
additional cross-carrier/basis identification — exactly the provenance
datum isolated elsewhere.
-/

namespace D0.Representation.VerifierSwapGradingNoGo

open Matrix
open D0
open D0.Representation.CompatibleInvolutionClassification
open D0.Representation.TypedRepresentationFunctor

abbrev M3 := Matrix (Fin 3) (Fin 3) ℚ
abbrev V3 := Fin 3 → ℚ

/-- Verifier exchange on the two-line defect plane. -/
def verifierSwapRay (v : D0.Vec2F2) : D0.Vec2F2 := (v.2, v.1)

/-- The existing projective-generation order. -/
def rayBasis : Fin 3 → D0.Vec2F2
  | 0 => D0.ePlus
  | 1 => D0.eMinus
  | 2 => D0.eGap

/-- Index action induced by verifier exchange. -/
def swapIndex : Fin 3 → Fin 3
  | 0 => 1
  | 1 => 0
  | 2 => 2

theorem verifier_swap_on_owned_rays :
    ∀ i : Fin 3, verifierSwapRay (rayBasis i) = rayBasis (swapIndex i) := by
  intro i
  fin_cases i <;> native_decide

/-- Natural permutation representation on the ordered generation-ray basis. -/
def verifierSwapMatrix : M3 :=
  !![0, 1, 0;
     1, 0, 0;
     0, 0, 1]

theorem verifierSwapMatrix_involution :
    verifierSwapMatrix * verifierSwapMatrix = (1 : M3) := by
  native_decide

theorem verifierSwapMatrix_nonscalar :
    verifierSwapMatrix ≠ (1 : M3) ∧ verifierSwapMatrix ≠ -(1 : M3) := by
  native_decide

def symmetricRay : V3 := ![1, 1, 0]
def antisymmetricRay : V3 := ![1, -1, 0]
def gapRay : V3 := ![0, 0, 1]

/-- The verifier swap has the tempting sign pattern (+,-,+). -/
theorem verifier_swap_eigensign_pattern :
    verifierSwapMatrix *ᵥ symmetricRay = symmetricRay ∧
    verifierSwapMatrix *ᵥ antisymmetricRay = -antisymmetricRay ∧
    verifierSwapMatrix *ᵥ gapRay = gapRay := by
  native_decide

/-- But it does not preserve the three distinct graph-derived degree fibres. -/
theorem verifierSwapMatrix_not_degree_compatible :
    verifierSwapMatrix * degreeOp ≠ degreeOp * verifierSwapMatrix := by
  native_decide

/-- Hence the natural verifier-swap action is not a typed compatible involution,
despite having the desired abstract 2+1 eigensign split. -/
theorem verifierSwapMatrix_not_compatible :
    ¬ CompatibleInvolution verifierSwapMatrix := by
  intro h
  exact verifierSwapMatrix_not_degree_compatible h.1

/-- Sharp route exclusion: verifier exchange alone cannot supply the missing
typed generation grading. -/
theorem verifier_swap_grading_route_closed :
    (verifierSwapMatrix * verifierSwapMatrix = (1 : M3)) ∧
    (verifierSwapMatrix ≠ (1 : M3) ∧ verifierSwapMatrix ≠ -(1 : M3)) ∧
    (verifierSwapMatrix * degreeOp ≠ degreeOp * verifierSwapMatrix) :=
  ⟨verifierSwapMatrix_involution,
    verifierSwapMatrix_nonscalar,
    verifierSwapMatrix_not_degree_compatible⟩

end D0.Representation.VerifierSwapGradingNoGo
