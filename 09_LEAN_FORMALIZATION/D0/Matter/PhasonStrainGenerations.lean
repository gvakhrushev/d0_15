import D0.Geometry.TorusCore13GeometryOrigin
import D0.Matter.BaryonS3Symmetrizer
import D0.Matter.BaryonMultipletBoundary

namespace D0.Matter

/-!
D0-QUASI-002 phason-strain generation and baryon S3 owner.

This layer ties the generation/phason carrier to the already closed
memory-torus shell carrier and ties baryon promotion to the finite S3 symmetric
triple sector.  It does not infer a physical resonance table.
-/

/-- Finite phi-quasicrystal vacuum support seen by the matter phason layer. -/
structure D0PhiQuasicrystalVacuum where
  shellGeometry : D0.Geometry.TorusCore13GeometryOriginClosure

/-- The active finite support used by this package. -/
def d0PhiQuasicrystalVacuum : D0PhiQuasicrystalVacuum where
  shellGeometry := D0.Geometry.torusCore13GeometryOriginClosure

/-- Phason modes are the three torus-shell roles. -/
abbrev PhasonMode : Type := D0.Geometry.TorusShell

/-- The phason-mode carrier has exactly three finite roles. -/
theorem phason_mode_card_eq_three :
    Fintype.card PhasonMode = 3 := by
  exact D0.Geometry.torus_shell_card_eq_three

/-- Finite phason strain tensor entry between two phason modes. -/
structure PhasonStrainTensor where
  source : PhasonMode
  target : PhasonMode
  weight : Rat

/-- Generation modes are read as phason modes of the same finite carrier. -/
abbrev GenerationPhasonMode : Type := PhasonMode

/-- The generation/phason carrier has exactly three modes. -/
theorem generation_phason_mode_card_eq_three :
    Fintype.card GenerationPhasonMode = 3 := by
  exact phason_mode_card_eq_three

/-- Ordered baryon phason triple before S3 symmetrization. -/
abbrev BaryonPhasonTriple : Type :=
  Prod PhasonMode (Prod PhasonMode PhasonMode)

/-- The ordered baryon phason triple carrier has dimension `3^3 = 27`. -/
theorem baryon_phason_triple_card_eq_27 :
    Fintype.card BaryonPhasonTriple = 27 := by
  simpa [BaryonPhasonTriple, PhasonMode, BaryonTripleShellCarrier]
    using baryon_triple_shell_card_eq_27

/-- Symmetric baryon phason sector represented by sorted S3 orbit owners. -/
abbrev BaryonPhasonSymmetricSector : Type := SortedTriple

/-- The S3-symmetric triple sector has decuplet dimension 10. -/
theorem baryon_phason_symmetric_sector_dim_eq_ten :
    Fintype.card BaryonPhasonSymmetricSector = 10 := by
  exact sorted_triple_card_eq_ten

/-- Closure package for QUASI-002 phason generations and baryon S3 transfer. -/
structure PhasonStrainGenerationsBaryonClosure where
  vacuum : D0PhiQuasicrystalVacuum
  phason_mode_card : Fintype.card PhasonMode = 3
  generation_mode_card : Fintype.card GenerationPhasonMode = 3
  ordered_triple_dim : Fintype.card BaryonPhasonTriple = 27
  symmetric_sector_dim : Fintype.card BaryonPhasonSymmetricSector = 10
  s3Symmetrizer : BaryonS3SymmetrizerClosure
  nucleonLineBoundary :
    ¬ CanPromoteBaryonMultiplet nucleonLineOnlyBaryonOperator

/-- Concrete closure witness for the finite phason/baryon S3 package. -/
def phasonStrainGenerationsBaryonClosure :
    PhasonStrainGenerationsBaryonClosure where
  vacuum := d0PhiQuasicrystalVacuum
  phason_mode_card := phason_mode_card_eq_three
  generation_mode_card := generation_phason_mode_card_eq_three
  ordered_triple_dim := baryon_phason_triple_card_eq_27
  symmetric_sector_dim := baryon_phason_symmetric_sector_dim_eq_ten
  s3Symmetrizer := baryon_s3_symmetrizer_closure
  nucleonLineBoundary := nucleon_line_cannot_promote_full_baryon_multiplet

/-- The finite phason S3 symmetrizer admits a baryon decuplet transfer carrier. -/
theorem phason_s3_symmetrizer_admits_baryon_decuplet_transfer :
    Fintype.card PhasonMode = 3 ∧
      Fintype.card BaryonPhasonTriple = 27 ∧
      Fintype.card BaryonPhasonSymmetricSector = 10 ∧
      ∃ C : BaryonS3SymmetrizerClosure,
        C.carrier_witness = (0, (0, 0)) ∧
          Fintype.card BaryonTripleCarrier = 27 ∧ Fintype.card SortedTriple = 10 := by
  exact
    ⟨phason_mode_card_eq_three,
      baryon_phason_triple_card_eq_27,
      baryon_phason_symmetric_sector_dim_eq_ten,
      ⟨baryon_s3_symmetrizer_closure,
        rfl,
        baryon_triple_carrier_card,
        sorted_triple_card_eq_ten⟩⟩

/-- Any full baryon multiplet promotion must expose the phason S3 sector. -/
theorem full_baryon_multiplet_requires_phason_s3_symmetrizer
    (O : BaryonMultipletOperator) :
    CanPromoteBaryonMultiplet O →
      HasBaryonDecupletCarrier O ∧
        Fintype.card BaryonPhasonSymmetricSector = 10 := by
  intro h
  exact ⟨h.2.2.1, baryon_phason_symmetric_sector_dim_eq_ten⟩

/-- Nucleon-line data alone still cannot promote the full baryon multiplet. -/
theorem nucleon_line_cannot_promote_without_phason_s3 :
    ¬ CanPromoteBaryonMultiplet nucleonLineOnlyBaryonOperator := by
  exact nucleon_line_cannot_promote_full_baryon_multiplet

/-- Machine-checkable owner for the QUASI-002 phason/baryon package. -/
theorem phason_strain_generations_baryon_closure :
    Fintype.card PhasonMode = 3 ∧
      Fintype.card GenerationPhasonMode = 3 ∧
      Fintype.card BaryonPhasonTriple = 27 ∧
      Fintype.card BaryonPhasonSymmetricSector = 10 ∧
      ¬ CanPromoteBaryonMultiplet nucleonLineOnlyBaryonOperator := by
  exact
    ⟨phason_mode_card_eq_three,
      generation_phason_mode_card_eq_three,
      baryon_phason_triple_card_eq_27,
      baryon_phason_symmetric_sector_dim_eq_ten,
      nucleon_line_cannot_promote_without_phason_s3⟩

end D0.Matter
