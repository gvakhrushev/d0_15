import D0.Extensions.X5.PrimitiveContract
import D0.Extensions.ArchiveCoordinateExtension
import D0.Cosmology.ArchiveContractionCriterion
import D0.Core.Phi
import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic

/-!
# D0-X5-P1 — PhasonPressureEnergy contract + model + deletion (Lane P1)

The pressure-energy common-sector primitive POSTULATED (HYP, D0-X5). Concrete model: `H_phi` = the `S_DE`
two-mode sector, with `i_energy, i_pressure` the two window eigendirections (window product `359/160`).
Deletion of the Galois-sign / role-assignment law admits both role assignments (`w_A ≠ w_B`) — the law is
necessary. The operator-type firewall (`L_archive ≠ QUQ ≠ W_eff ≠ S_DE`) is maintained; no trace/det
coincidence is an intertwiner. Internal only — no physical EOS.
-/

namespace D0.Extensions.X5.Phason

open D0 D0.Extensions.X5

/-- The PhasonPressureEnergy contract (HYP, D0-X5). -/
def peContract : PrimitiveContract :=
  ⟨"PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT", "D0-X5",
   ["energy-domain-nonzero", "pressure-typed", "response-positive", "galois-sign", "phi-semigroup-typed"], 2⟩

theorem pe_wellFormed : peContract.wellFormed := ⟨rfl, by decide, by decide⟩

/-- Concrete model: the `S_DE` 2-mode sector window product `359/160` (the two pressure/energy eigendirections). -/
theorem pe_model_window :
    (3 / 2 - Real.sqrt 10 / 40) * (3 / 2 + Real.sqrt 10 / 40) = 359 / 160 :=
  D0.Extensions.ArchiveCoordinateExtension.window_product

def peModel : ModelWitness := ⟨2, 5, true⟩
theorem pe_model_complete : peModel.complete peContract := ⟨rfl, by decide, rfl⟩

/-- Deletion test: drop the Galois-sign role-assignment ⇒ `w_A` and `w_B` both admissible (≥2 role models). -/
def pe_deletion : DeletionTest := ⟨"galois-sign", 2⟩
theorem pe_deletion_necessary : pe_deletion.lawNecessary := by decide
/-- The two role models differ: `w_A ≠ w_B`. -/
theorem pe_deletion_models_differ :
    (361 / 359 - 12 * Real.sqrt 10 / 359 : ℝ) ≠ 361 / 359 + 12 * Real.sqrt 10 / 359 :=
  D0.Cosmology.ArchiveContractionCriterion.w_underdetermined

/-- **D0-X5-P1 terminal.** Contract well-formed, sector model complete, deletion-minimal. -/
theorem phason_pe_x5_terminal :
    peContract.wellFormed ∧ peModel.complete peContract ∧ pe_deletion.lawNecessary ∧
      (361 / 359 - 12 * Real.sqrt 10 / 359 : ℝ) ≠ 361 / 359 + 12 * Real.sqrt 10 / 359 :=
  ⟨pe_wellFormed, pe_model_complete, pe_deletion_necessary, pe_deletion_models_differ⟩

end D0.Extensions.X5.Phason
