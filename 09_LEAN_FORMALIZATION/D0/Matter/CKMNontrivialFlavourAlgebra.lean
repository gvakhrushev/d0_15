import D0.Matter.GenerationOverlapResponseOrigin
import Mathlib.Tactic

namespace D0.Matter

/-- A nontrivial flavour transfer is any generation response that is not a full
column-permutation witness.  This is an algebraic condition, not a PDG CKM
numerical claim. -/
def NontrivialFlavourTransfer
    (O : Matrix GenCarrier GenCarrier Real) : Prop :=
  Not (IsPermutationWitness O)

/-- Torus-origin source for non-permutation flavour transfer. -/
def TorusNonPermutationFlavourSource
    (T : D0.Geometry.TorusParameter) : Prop :=
  HasNonCommutingGenerationSelectors
    D0.Geometry.radialAdjacency
    (D0.Geometry.phaseDrift T)

/-- Flavour defect `F_fl = I - O`. -/
def flavourDefect
    (O : Matrix GenCarrier GenCarrier Real) :
    Matrix GenCarrier GenCarrier Real :=
  fun i j => (if i = j then 1 else 0) - O i j

/-- Column response of `F_fl^T F_fl`. -/
def flavourDefectColumnResponse
    (O : Matrix GenCarrier GenCarrier Real) (j : GenCarrier) : Real :=
  Finset.univ.sum
    (fun i : GenCarrier => flavourDefect O i j * flavourDefect O i j)

/-- Positive finite response carried by `F_fl^T F_fl`. -/
def FlavourDefectPositiveResponse
    (O : Matrix GenCarrier GenCarrier Real) : Prop :=
  forall j : GenCarrier, 0 <= flavourDefectColumnResponse O j

/-- A permutation witness has no nontrivial flavour transfer at fixed convention. -/
theorem permutation_witness_has_no_nontrivial_flavour_transfer
    (O : Matrix GenCarrier GenCarrier Real)
    (hperm : IsPermutationWitness O) :
    Not (NontrivialFlavourTransfer O) := by
  intro hnontrivial
  exact hnontrivial hperm

/-- A non-permutation overlap response is a nontrivial flavour transfer. -/
theorem overlap_response_can_force_nonpermutation_transfer
    (O : Matrix GenCarrier GenCarrier Real)
    (hnonperm : Not (IsPermutationWitness O)) :
    NontrivialFlavourTransfer O := by
  exact hnonperm

/--
The torus shell noncommutativity supplies the finite source used by the
non-permutation flavour-transfer layer.
-/
theorem torus_overlap_generates_nonpermutation_flavour_transfer
    (T : D0.Geometry.TorusParameter) :
    TorusNonPermutationFlavourSource T := by
  exact torus_shell_noncommutativity_forces_nonpermutation_overlap_source T

/-- `F_fl^T F_fl` has nonnegative column responses. -/
theorem nontrivial_flavour_defect_positive_response
    (O : Matrix GenCarrier GenCarrier Real) :
    FlavourDefectPositiveResponse O := by
  intro j
  unfold flavourDefectColumnResponse
  exact Finset.sum_nonneg
    (fun i _ => mul_self_nonneg (flavourDefect O i j))

/-- Admissibility of a nontrivial finite flavour defect for meson transfer. -/
def FlavourDefectAdmissibleForMesonTransfer
    (O : Matrix GenCarrier GenCarrier Real) : Prop :=
  NontrivialFlavourTransfer O /\ FlavourDefectPositiveResponse O

/-- Non-permutation plus positivity makes the flavour defect admissible. -/
theorem nontrivial_flavour_defect_admissible_for_meson_transfer
    (O : Matrix GenCarrier GenCarrier Real)
    (hnonperm : Not (IsPermutationWitness O)) :
    FlavourDefectAdmissibleForMesonTransfer O := by
  exact
    ⟨overlap_response_can_force_nonpermutation_transfer O hnonperm,
      nontrivial_flavour_defect_positive_response O⟩

/-- Closure package for the algebraic nontrivial flavour layer. -/
structure CKMNontrivialFlavourAlgebraClosure where
  permutation_no_go :
    forall O : Matrix GenCarrier GenCarrier Real,
      IsPermutationWitness O -> Not (NontrivialFlavourTransfer O)
  nonpermutation_promotes :
    forall O : Matrix GenCarrier GenCarrier Real,
      Not (IsPermutationWitness O) -> NontrivialFlavourTransfer O
  torus_source :
    forall T : D0.Geometry.TorusParameter,
      TorusNonPermutationFlavourSource T
  positive_response :
    forall O : Matrix GenCarrier GenCarrier Real,
      FlavourDefectPositiveResponse O

/-- Concrete closure object for CKM/flavour algebra without physical CKM entries. -/
def ckm_nontrivial_flavour_algebra_closure :
    CKMNontrivialFlavourAlgebraClosure where
  permutation_no_go := permutation_witness_has_no_nontrivial_flavour_transfer
  nonpermutation_promotes := overlap_response_can_force_nonpermutation_transfer
  torus_source := torus_overlap_generates_nonpermutation_flavour_transfer
  positive_response := nontrivial_flavour_defect_positive_response

end D0.Matter
