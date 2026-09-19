import D0.Core.DyadABCD
import D0.Geometry.ArchivePhaseDistance
import D0.Geometry.ArchiveLaplacianRG

namespace D0

/-!
# Role × phase archive carrier

The legacy archive state stores only the cardinality `(archiveFibers n)^4`.  This module supplies a
typed realization of exactly that many states, with the exponent caused by the four terminal roles:

```
ArchiveRolePhasePoint n = Role → archivePhaseIndex n.
```

The refinement map is coordinatewise.  It therefore preserves the role decomposition instead of
flattening the product into a single radix-dependent `Fin (L^4)` index.
-/

/-- Four role-labelled phase coordinates at archive level `n`. -/
abbrev ArchiveRolePhasePoint (n : Nat) : Type :=
  Role → archivePhaseIndex n

/-- Cardinality in invariant form: one phase coordinate for every terminal role. -/
theorem archiveRolePhasePoint_card_pow_roles (n : Nat) :
    Fintype.card (ArchiveRolePhasePoint n) =
      archiveFibers n ^ Fintype.card Role := by
  simp [ArchiveRolePhasePoint, archivePhaseIndex]

/-- The role-product carrier realizes the legacy archive mode count. -/
theorem archiveRolePhasePoint_card_eq_archiveModes (n : Nat) :
    Fintype.card (ArchiveRolePhasePoint n) = archiveModes n := by
  rw [archiveRolePhasePoint_card_pow_roles, card_role]
  rfl

/-- Coordinatewise phase refinement on the role-product carrier. -/
def archiveRolePhaseProjection (n : Nat) :
    ArchiveRolePhasePoint (n + 1) → ArchiveRolePhasePoint n :=
  fun x r => archiveRGPhaseProjection n (x r)

/-- Coordinatewise refinement is surjective because every one-dimensional phase projection is. -/
theorem archiveRolePhaseProjection_surjective (n : Nat) :
    Function.Surjective (archiveRolePhaseProjection n) := by
  classical
  intro y
  let x : ArchiveRolePhasePoint (n + 1) :=
    fun r => (archiveRGPhaseProjection_surjective n (y r)).choose
  refine ⟨x, ?_⟩
  funext r
  exact (archiveRGPhaseProjection_surjective n (y r)).choose_spec

/--
The typed carrier supplies the causal direction missing from the old hard-coded exponent:
the archive mode count is the cardinality of a function space indexed by the four roles.
-/
theorem archive_modes_realized_by_role_phase_product (n : Nat) :
    archiveModes n = Fintype.card (ArchiveRolePhasePoint n) := by
  exact (archiveRolePhasePoint_card_eq_archiveModes n).symm

/-- Packaging owner for the product-carrier realization and its refinement map. -/
theorem archive_role_phase_product_carrier_owner :
    (∀ n, archiveModes n = Fintype.card (ArchiveRolePhasePoint n)) ∧
      (∀ n, Function.Surjective (archiveRolePhaseProjection n)) := by
  exact ⟨archive_modes_realized_by_role_phase_product,
    archiveRolePhaseProjection_surjective⟩

end D0
