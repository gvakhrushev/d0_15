import Mathlib.Data.Real.Basic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchiveCubicalCochainCarrier
import D0.Geometry.Archive1DCochainRefinement

namespace D0.Geometry

open D0

/-!
# D0.Geometry.ArchiveGradedRefinementChainMap

Owner: `D0-ARCHIVE-GRADED-REFINEMENT-CHAIN-MAP-001`.

This module proves only the role-product dimension and the cardinality of the
finite role and cubical-cell label types. It does not define the tensor-product
maps `B_S` or prove graded differential commutation.

The unscaled four-dimensional chain argument is recorded in
`02_REGISTRY/research/A4D_NATIVE_COCHAIN_REFINEMENT.md`. A typed full 4D Lean
composition, including transport for the scale-corrected `dForward`, remains
open in the supported library.
-/

/-- The 4 directions in the product torus. -/
def roleProductDim : ℕ := 4

theorem role_product_dim_eq : roleProductDim = Fintype.card Role := by
  rw [card_role]
  rfl

/-- **D0-ARCHIVE-GRADED-REFINEMENT-CHAIN-MAP-001 (Owner, label scope)**:
Records that the product dimension and role cardinality are 4 and that the
cubical-cell label type has 16 elements. No graded chain map is asserted. -/
theorem archive_graded_refinement_chain_map_owner :
    (roleProductDim = 4) ∧
    (Fintype.card CubicalCellType = 16) ∧
    (Fintype.card Role = 4) :=
  ⟨rfl, card_archive_fock_state, card_role⟩

end D0.Geometry
