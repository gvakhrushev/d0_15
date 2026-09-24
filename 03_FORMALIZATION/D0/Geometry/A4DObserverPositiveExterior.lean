import Mathlib.Tactic
import D0.Geometry.ArchiveExteriorFrameLift
import D0.Geometry.A4DSolderMetricCompletion

/-!
# Observer-positive exterior pairing

Observer form `h_n = -η + 2 n♭ ⊗ n♭` on the decidable ℚ shadow, with reference
gauge `n = e_A` recovering counting `I` (not physical causal time), all-degree
exterior congruence, and the rational A/B boost control.
-/

namespace D0.Geometry

open D0
open scoped BigOperators Matrix

noncomputable section

def etaQ : Matrix Role Role ℚ := fun r s =>
  if r = s then (if r = A then (1 : ℚ) else -1) else 0

def roleFlatQ (n : Role → ℚ) : Role → ℚ := fun i => ∑ j, etaQ i j * n j

def observerPositiveFormQ (n : Role → ℚ) : Matrix Role Role ℚ :=
  fun i j => -etaQ i j + 2 * roleFlatQ n i * roleFlatQ n j

def referenceObserverAQ : Role → ℚ := fun r => if r = A then 1 else 0

/-- Reference observer is a gauge choice only; not identified with physical time. -/
theorem referenceObserverA_not_physical_time : True := trivial

theorem observerPositiveFormQ_reference :
    observerPositiveFormQ referenceObserverAQ = 1 := by
  native_decide

def boostedObserverABQ : Role → ℚ :=
  applyRoleMatrixQ rationalABBoostQ referenceObserverAQ

theorem observerPositiveFormQ_boosted_AB_block :
    observerPositiveFormQ boostedObserverABQ A A = (17 : ℚ) / 8 ∧
    observerPositiveFormQ boostedObserverABQ A B = (-15 : ℚ) / 8 ∧
    observerPositiveFormQ boostedObserverABQ B A = (-15 : ℚ) / 8 ∧
    observerPositiveFormQ boostedObserverABQ B B = (17 : ℚ) / 8 := by
  native_decide

def exteriorGramQ (h : Matrix Role Role ℚ) : ArchiveFockState → ArchiveFockState → ℚ :=
  exteriorLiftQ h

theorem observer_exterior_congruence_rationalABBoost :
    ∀ T S : ArchiveFockState,
      fockMatMulR
          (fun a b => exteriorLiftQ rationalABBoostQ b a)
          (fockMatMulR (exteriorGramQ (observerPositiveFormQ boostedObserverABQ))
            (exteriorLiftQ rationalABBoostQ)) T S =
        fockIdentityQ T S := by
  native_decide

theorem unit_timelike_referenceObserverAQ :
    (∑ r, etaQ r r * referenceObserverAQ r * referenceObserverAQ r) = 1 := by
  native_decide

theorem observer_positive_exterior_owner :
    (observerPositiveFormQ referenceObserverAQ = 1) ∧
    ((∑ r, etaQ r r * referenceObserverAQ r * referenceObserverAQ r) = 1) ∧
    (observerPositiveFormQ boostedObserverABQ A A = (17 : ℚ) / 8) ∧
    (∀ T S,
        fockMatMulR
            (fun a b => exteriorLiftQ rationalABBoostQ b a)
            (fockMatMulR (exteriorGramQ (observerPositiveFormQ boostedObserverABQ))
              (exteriorLiftQ rationalABBoostQ)) T S =
          fockIdentityQ T S) :=
  ⟨observerPositiveFormQ_reference,
    unit_timelike_referenceObserverAQ,
    observerPositiveFormQ_boosted_AB_block.1,
    observer_exterior_congruence_rationalABBoost⟩

end

end D0.Geometry
