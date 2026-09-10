import D0.Foundation.EmpiricalTheoryFactorization

/-! A fixed Boolean current table is finite; universal protocol semantics must retain
addresses/contexts or additional structure. This does not bound a network of D0 detectors. -/
namespace D0.Foundation.EmpiricalFiniteDetectorBoundary

open D0.Foundation.CurrentDataFactorization
open D0.Synthesis.DetectorLayerEquivalence
open D0.Foundation.EmpiricalTheoryFactorization

theorem fixed_current_table_card :
    Fintype.card (CurrentComparison (Bool × Bool)) = 65536 := by
  norm_num [CurrentComparison]

/-- T51's fixed target cannot faithfully contain arbitrarily many distinct comparisons. -/
theorem no_65537_embedding_in_fixed_layer :
    ¬ Nonempty (Fin 65537 ↪ HistoryInvariantCarrier (Bool × Bool) Bool) := by
  rintro ⟨e⟩
  let f := e.trans (currentEquivHistoryInvariant (Bool × Bool) Bool).symm.toEmbedding
  have h := Fintype.card_le_of_injective f f.injective
  rw [fixed_current_table_card] at h
  norm_num at h

/-- An abstract addressable-record semantics; physical generation of the records is not inferred. -/
def recordTheory (A : Type) [DecidableEq A] : EmpiricalTheory where
  State := A
  Test := A
  Catalogue := Unit
  Outcome := Bool
  observe s _ test := decide (s = test)

theorem record_signature_injective (A : Type) [DecidableEq A] :
    Function.Injective (signature (recordTheory A)) := by
  classical
  intro s t h
  have he := congrFun (congrFun h ()) s
  have hts : t=s := by simpa [signature, recordTheory] using he.symm
  exact hts.symm

theorem every_record_admissible (A : Type) [DecidableEq A] (s : A) :
    D0.Foundation.M1ClassAdmissibility.M1ClassAdmissible
      (rawCatalogueSystem (recordTheory A)) s := by
  intro c d
  cases c
  cases d
  rfl

end D0.Foundation.EmpiricalFiniteDetectorBoundary
