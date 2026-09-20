import D0.Geometry.ArchiveSpectralCounting
import D0.Geometry.SpectralActionAdmissibility

namespace D0.Geometry.ArchiveWeylDimensionVacuityNoGo

open D0

/-- **Negative Control Witness**: For ANY arbitrary tower function `tower : Nat → ArchiveState`,
the structure `HasWeylDimension tower 4` can be inhabited vacuously by providing propositions
as data (e.g., `True`). -/
def vacuousWitness (tower : Nat → ArchiveState) : HasWeylDimension tower 4 :=
  { countingAsymptotic := True
  , heatTraceScaling := True
  , noSpectralPollution := True
  , dimensionValue := rfl }

/-- **D0-ARCHIVE-WEYL-DIMENSION-VACUITY-NOGO-001 (Part 1)**:
For every tower, `HasWeylDimension tower 4` is non-empty without requiring any spectral hypothesis. -/
theorem hasWeylDimension_vacuous (tower : Nat → ArchiveState) :
    Nonempty (HasWeylDimension tower 4) :=
  ⟨vacuousWitness tower⟩

/-- **D0-ARCHIVE-WEYL-DIMENSION-VACUITY-NOGO-001 (Part 2)**:
The predicate `ArchiveHeatTrace4D tower` is unconditionally true for ANY tower:
it carries zero mathematical constraint on the spectrum of the Laplacian. -/
theorem archiveHeatTrace4D_vacuous (tower : Nat → ArchiveState) :
    ArchiveHeatTrace4D tower :=
  ⟨vacuousWitness tower⟩

/-- Even for contradictory propositions (`False`), the structure fields can be instantiated
because `False : Prop`, proving that the fields are propositions-as-data rather than proof terms. -/
def vacuousFalseWitness (tower : Nat → ArchiveState) : HasWeylDimension tower 4 :=
  { countingAsymptotic := False
  , heatTraceScaling := False
  , noSpectralPollution := False
  , dimensionValue := rfl }

theorem hasWeylDimension_vacuous_false (tower : Nat → ArchiveState) :
    Nonempty (HasWeylDimension tower 4) :=
  ⟨vacuousFalseWitness tower⟩

/-- **D0-ARCHIVE-WEYL-DIMENSION-VACUITY-NOGO-001 (Owner)**:
Summary theorem establishing that the current formalization of 4D Weyl dimension
and heat-trace scaling in `ArchiveSpectralCounting` is vacuous and must be replaced
by a genuine operator-level spectral counting framework. -/
theorem archive_weyl_dimension_vacuity_nogo_owner :
    (∀ tower : Nat → ArchiveState, Nonempty (HasWeylDimension tower 4)) ∧
    (∀ tower : Nat → ArchiveState, ArchiveHeatTrace4D tower) ∧
    (∀ tower : Nat → ArchiveState, (vacuousWitness tower).dimensionValue = rfl) :=
  ⟨hasWeylDimension_vacuous, archiveHeatTrace4D_vacuous, fun _ => rfl⟩

end D0.Geometry.ArchiveWeylDimensionVacuityNoGo
