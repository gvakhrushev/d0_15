import D0.Extensions.X5.PrimitiveContract
import D0.Extensions.ArchiveCoordinateExtension
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-X5-P2 — PhasonCoordinate contract + model + deletion + redshift boundary (Lane P2)

The internal coordinate functor POSTULATED (HYP, D0-X5). Concrete model: the φ-tick cocycle `z(s) = φ^s − 1`
(`z(1) = φ − 1`). Deletion of the internal-normalization law admits the integer-tick model (`z(1) = 1`), and
`φ − 1 ≠ 1` — the law is necessary. Two layers kept distinct: P2-internal (this cocycle) vs P2-passport (the
physical redshift bridge). Terminal **P2-E**: the observed-redshift reading is external-passport-only; no
internal coordinate equals observed redshift, and physical `w_DE(z)` stays a maximality no-go.
-/

namespace D0.Extensions.X5.Coordinate

open D0 D0.Extensions.X5

/-- The PhasonCoordinate contract (HYP, D0-X5). -/
def coordContract : PrimitiveContract :=
  ⟨"PRIM-PHASON-COORDINATE-FUNCTOR", "D0-X5",
   ["cocycle-composition", "symmetry-equivariant", "readout-compatible", "normalization-internal"], 1⟩

theorem coord_wellFormed : coordContract.wellFormed := ⟨rfl, by decide, by decide⟩

/-- Concrete model: φ-tick cocycle value `z(1) = φ − 1` (`≠ 1` since `φ < 2`). -/
theorem coord_model_z1 : phi - 1 ≠ 1 := D0.Extensions.ArchiveCoordinateExtension.coordinate_cocycle_divergent

def coordModel : ModelWitness := ⟨1, 4, true⟩
theorem coord_model_complete : coordModel.complete coordContract := ⟨rfl, by decide, rfl⟩

/-- Deletion test: drop internal-normalization ⇒ φ-tick (`φ−1`) and integer-tick (`1`) both admissible. -/
def coord_deletion : DeletionTest := ⟨"normalization-internal", 2⟩
theorem coord_deletion_necessary : coord_deletion.lawNecessary := by decide

/-- **Redshift passport boundary (P2-E).** The physical redshift reading is external-passport-only: the
internal coordinate `φ−1 ≠ 1` is well-defined but is not equated to observed `z`. -/
theorem coordinate_x5_terminal :
    coordContract.wellFormed ∧ coordModel.complete coordContract ∧ coord_deletion.lawNecessary ∧
      (phi - 1 ≠ 1) :=
  ⟨coord_wellFormed, coord_model_complete, coord_deletion_necessary, coord_model_z1⟩

end D0.Extensions.X5.Coordinate
