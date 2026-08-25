import D0.Synthesis.SceneSpectralAction
import D0.Synthesis.SectorGaloisClosure
import D0.Synthesis.TransportCubicGaloisS3
import D0.Synthesis.YukawaCommutantSpectrum

/-!
# Five-sector field ledger: three independent irrational characters and one rational hub

T13 identifies the same edge count `359` in five sectors. T26–T30 identify the exact
field content behind that sharing. This module gives the resulting architecture as a
single finite linear object rather than a prose list.

The five sectors have the character-incidence rows

```
geometry         (0,0,1)
gravity          (0,0,0)
electromagnetism (1,0,0)
mass / Yukawa    (0,0,1)
dark energy      (0,1,0)
```

on the independent axes `(√5, √10, √386579)`. Thus:

* the character rank is exactly three;
* gravity is the unique rational-only row;
* geometry and mass are the unique distinct sectors sharing an irrational character;
* the only linear redundancies are the rational gravity coordinate and the
  geometry-minus-mass transport relation.

The capstone connects this incidence theorem to the already internal degree-eight
`(ℤ/2)³` character field, full transport `S₃`, `√5,√10 ∉ K`, the rational EH proxy,
and equivariant Yukawa rigidity.
-/

namespace D0.Synthesis.FiveSectorFieldLedger

open D0.Synthesis.SceneSpectralAction
open D0.Synthesis.SectorFieldIndependence
open D0.Synthesis.SectorGaloisClosure
open D0.Synthesis.TransportCubicGaloisS3
open D0.Synthesis.YukawaCommutantSpectrum

noncomputable section

-- Restore the scalar structures of the nested degree-eight character field.
local instance algAB : Algebra AlphaCharacterAlgebra AlphaDECharacterAlgebra :=
  QuadraticAlgebra.instAlgebra
local instance algQB : Algebra ℚ AlphaDECharacterAlgebra :=
  QuadraticAlgebra.instAlgebra
local instance charB : CharZero AlphaDECharacterAlgebra :=
  algebraRat.charZero AlphaDECharacterAlgebra
local instance algBC : Algebra AlphaDECharacterAlgebra SectorCharacterAlgebra :=
  QuadraticAlgebra.instAlgebra
local instance algQC : Algebra ℚ SectorCharacterAlgebra :=
  QuadraticAlgebra.instAlgebra
local instance charC : CharZero SectorCharacterAlgebra :=
  algebraRat.charZero SectorCharacterAlgebra
local instance fdC : FiniteDimensional ℚ SectorCharacterAlgebra :=
  FiniteDimensional.of_finrank_pos (by rw [sector_character_finrank]; norm_num)
local instance autFin : Fintype (SectorCharacterAlgebra ≃ₐ[ℚ] SectorCharacterAlgebra) :=
  @AlgEquiv.fintype ℚ SectorCharacterAlgebra inferInstance sectorCharacterField algQC fdC

/-- The five consumers of the scene invariant in T13. -/
inductive PhysicsSector
  | geometry
  | gravity
  | electromagnetism
  | mass
  | darkEnergy
  deriving DecidableEq, Fintype, Repr

/-- The three independent non-rational field characters. -/
abbrev CharacterAxis := Fin 3

/-- Character row of each physics sector, ordered `(α, DE, transport)`. -/
def sectorCharacter : PhysicsSector → CharacterAxis → ℚ
  | .geometry => fun a => if a = 2 then 1 else 0
  | .gravity => fun _ => 0
  | .electromagnetism => fun a => if a = 0 then 1 else 0
  | .mass => fun a => if a = 2 then 1 else 0
  | .darkEnergy => fun a => if a = 1 then 1 else 0

theorem geometry_character :
    sectorCharacter .geometry = fun a => if a = 2 then 1 else 0 := rfl

theorem gravity_character : sectorCharacter .gravity = 0 := by
  funext a
  rfl

theorem electromagnetism_character :
    sectorCharacter .electromagnetism = fun a => if a = 0 then 1 else 0 := rfl

theorem mass_character :
    sectorCharacter .mass = sectorCharacter .geometry := rfl

theorem darkEnergy_character :
    sectorCharacter .darkEnergy = fun a => if a = 1 then 1 else 0 := rfl

/-- The field-character readout of a formal linear combination of the five sectors.
Coordinates are `(EM, DE, geometry + mass)`; gravity carries no irrational character. -/
def characterReadout : (PhysicsSector → ℚ) →ₗ[ℚ] (CharacterAxis → ℚ) where
  toFun w a :=
    if a = 0 then w .electromagnetism
    else if a = 1 then w .darkEnergy
    else w .geometry + w .mass
  map_add' x y := by
    funext a
    fin_cases a <;> simp [add_left_comm, add_comm]
  map_smul' q x := by
    funext a
    fin_cases a <;> simp [mul_add]

@[simp] theorem characterReadout_zero (w : PhysicsSector → ℚ) :
    characterReadout w 0 = w .electromagnetism := by
  simp [characterReadout]

@[simp] theorem characterReadout_one (w : PhysicsSector → ℚ) :
    characterReadout w 1 = w .darkEnergy := by
  simp [characterReadout]

@[simp] theorem characterReadout_two (w : PhysicsSector → ℚ) :
    characterReadout w 2 = w .geometry + w .mass := by
  simp [characterReadout]

/-- Exact kernel: gravity is free, EM and DE vanish, and geometry cancels mass. -/
theorem characterReadout_eq_zero_iff (w : PhysicsSector → ℚ) :
    characterReadout w = 0 ↔
      w .electromagnetism = 0 ∧
      w .darkEnergy = 0 ∧
      w .geometry + w .mass = 0 := by
  constructor
  · intro h
    have h0 := congrFun h (0 : CharacterAxis)
    have h1 := congrFun h (1 : CharacterAxis)
    have h2 := congrFun h (2 : CharacterAxis)
    simpa using ⟨h0, h1, h2⟩
  · rintro ⟨h0, h1, h2⟩
    funext a
    fin_cases a <;> simp [h0, h1, h2]

/-- Every three-character vector is realized: use EM, DE, and geometry representatives. -/
theorem characterReadout_surjective : Function.Surjective characterReadout := by
  intro y
  let w : PhysicsSector → ℚ
    | .geometry => y 2
    | .gravity => 0
    | .electromagnetism => y 0
    | .mass => 0
    | .darkEnergy => y 1
  refine ⟨w, ?_⟩
  funext a
  fin_cases a <;> simp [characterReadout, w]

theorem characterReadout_range_eq_top :
    LinearMap.range characterReadout = ⊤ :=
  LinearMap.range_eq_top.mpr characterReadout_surjective

/-- The five-sector irrational incidence has rank exactly three. -/
theorem five_sector_character_rank :
    Module.finrank ℚ (LinearMap.range characterReadout) = 3 := by
  rw [characterReadout_range_eq_top]
  simp

theorem physicsSector_card : Fintype.card PhysicsSector = 5 := by decide

/-- The two-dimensional redundancy space is exactly: the rational gravity direction
and the geometry-minus-mass transport relation. -/
theorem five_sector_character_kernel_rank :
    Module.finrank ℚ (LinearMap.ker characterReadout) = 2 := by
  have h := characterReadout.finrank_range_add_finrank_ker
  rw [five_sector_character_rank] at h
  have hdom : Module.finrank ℚ (PhysicsSector → ℚ) = 5 := by
    rw [Module.finrank_pi, physicsSector_card]
  omega

/-- Geometry and mass are the unique distinct sectors with the same character row. -/
theorem sectorCharacter_eq_iff (s t : PhysicsSector) :
    sectorCharacter s = sectorCharacter t ↔
      s = t ∨
      (s = .geometry ∧ t = .mass) ∨
      (s = .mass ∧ t = .geometry) := by
  fin_cases s <;> fin_cases t <;> decide

/-- No nontrivial `√5` or `√10` coordinate can occur inside the transport field.
This is an intrinsic intersection statement: a nonzero quadratic coordinate would
construct the forbidden square root by division. -/
theorem transport_has_no_alpha_or_de_coordinate (d : ℚ)
    (hno : ¬ ∃ s : TransportSplit, s ^ 2 = algebraMap ℚ TransportSplit d) :
    ¬ ∃ y : TransportSplit, ∃ u v : ℚ, v ≠ 0 ∧
      (y - algebraMap ℚ TransportSplit u) ^ 2 =
        algebraMap ℚ TransportSplit (d * v ^ 2) := by
  rintro ⟨y, u, v, hv, hy⟩
  apply hno
  refine ⟨(y - algebraMap ℚ TransportSplit u) /
      algebraMap ℚ TransportSplit v, ?_⟩
  have hvK : algebraMap ℚ TransportSplit v ≠ 0 :=
    fun h => hv ((algebraMap ℚ TransportSplit).injective (by simpa using h))
  rw [div_pow, hy, map_mul, map_pow]
  field_simp

theorem transport_has_no_alpha_coordinate :
    ¬ ∃ y : TransportSplit, ∃ u v : ℚ, v ≠ 0 ∧
      (y - algebraMap ℚ TransportSplit u) ^ 2 =
        algebraMap ℚ TransportSplit (5 * v ^ 2) :=
  transport_has_no_alpha_or_de_coordinate 5 sqrt5_not_mem

theorem transport_has_no_de_coordinate :
    ¬ ∃ y : TransportSplit, ∃ u v : ℚ, v ≠ 0 ∧
      (y - algebraMap ℚ TransportSplit u) ^ 2 =
        algebraMap ℚ TransportSplit (10 * v ^ 2) :=
  transport_has_no_alpha_or_de_coordinate 10 sqrt10_not_mem

/-- Capstone: five sectors compress to a rational hub plus three independent characters.
The only duplicated irrational carrier is the forced geometry/mass transport line. -/
theorem five_sector_field_ledger :
    Module.finrank ℚ (LinearMap.range characterReadout) = 3
      ∧ Module.finrank ℚ (LinearMap.ker characterReadout) = 2
      ∧ (∀ w : PhysicsSector → ℚ, characterReadout w = 0 ↔
          w .electromagnetism = 0 ∧
          w .darkEnergy = 0 ∧
          w .geometry + w .mass = 0)
      ∧ (∀ s t, sectorCharacter s = sectorCharacter t ↔
          s = t ∨
          (s = .geometry ∧ t = .mass) ∨
          (s = .mass ∧ t = .geometry))
      ∧ Module.finrank ℚ SectorCharacterAlgebra = 8
      ∧ Fintype.card (SectorCharacterAlgebra ≃ₐ[ℚ] SectorCharacterAlgebra) = 8
      ∧ Nat.card D0.Synthesis.TransportFieldNoGolden.Pcubic.Gal = 6
      ∧ (¬ ∃ s : TransportSplit, s ^ 2 = algebraMap ℚ TransportSplit 5)
      ∧ (¬ ∃ s : TransportSplit, s ^ 2 = algebraMap ℚ TransportSplit 10)
      ∧ D0.Geometry.HeatTraceA2Decomposition.discreteEHActionProxy Lr ρ1 = 359
      ∧ (∀ q : ℚ, q ^ 3 - 359 * q - 2574 ≠ 0) :=
  ⟨five_sector_character_rank, five_sector_character_kernel_rank,
    characterReadout_eq_zero_iff, sectorCharacter_eq_iff, sector_character_finrank,
    sector_galois_card, transport_gal_card_eq_six, sqrt5_not_mem, sqrt10_not_mem,
    eh_proxy_is_edge_count, no_rational_root_rat⟩

end

end D0.Synthesis.FiveSectorFieldLedger
