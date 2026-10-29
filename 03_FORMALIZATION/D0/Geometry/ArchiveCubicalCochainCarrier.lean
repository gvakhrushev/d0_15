import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fintype.Card
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchiveCARFockCarrier

namespace D0.Geometry

open D0

/-!
# D0.Geometry.ArchiveCubicalCochainCarrier

Owner: `D0-ARCHIVE-CUBICAL-COCHAIN-CARRIER-001`.

Finite label layer for the four-role cubical carrier. This module proves the
cardinality of the role-subset labels, a sum of prescribed scalar counts, and a
label-type equivalence with `ArchiveFockState`. It does not construct the
grid-indexed cochain complex, its phase-space `ℓ²` factor, or a cochain/Fock
isomorphism for that full carrier.
-/

/-- Cubical cell label: subset of active role directions S ⊆ Role. -/
abbrev CubicalCellType : Type := Role → Bool

/-- Form degree of a cell type: number of active directions |S|. -/
def cellDegree (S : CubicalCellType) : ℕ :=
  (Finset.filter (fun r : Role => S r = true) Finset.univ).card

/-- Prescribed scalar counts `(1, 4, 6, 4, 1)` for the five degrees. This
module does not construct homology or identify these constants as its Betti
numbers. -/
def betti0 : ℕ := 1
def betti1 : ℕ := 4
def betti2 : ℕ := 6
def betti3 : ℕ := 4
def betti4 : ℕ := 1

/-- The five prescribed scalar counts sum to 16. -/
theorem total_betti_sum : betti0 + betti1 + betti2 + betti3 + betti4 = 16 := rfl

/-- Equivalence of the bare cubical-cell and CAR-Fock label types. It is not
an equivalence of grid-indexed cochain complexes or Hilbert spaces. -/
def cubicalCellToFockEquiv : CubicalCellType ≃ ArchiveFockState :=
  Equiv.refl _

/-- **D0-ARCHIVE-CUBICAL-COCHAIN-CARRIER-001 (Owner, finite label scope)**:
Collects the role-subset label count, scalar-count identity, and role
count. The full grid-indexed cochain-carrier identification remains open. -/
theorem archive_cubical_cochain_carrier_owner :
    (Fintype.card CubicalCellType = 16) ∧
    (betti0 + betti1 + betti2 + betti3 + betti4 = 16) ∧
    (Fintype.card Role = 4) :=
  ⟨card_archive_fock_state, total_betti_sum, card_role⟩

end D0.Geometry
