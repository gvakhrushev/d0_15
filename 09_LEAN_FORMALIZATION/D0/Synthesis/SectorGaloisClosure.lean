import Mathlib.FieldTheory.Fixed
import Mathlib.FieldTheory.Galois.Basic
import Mathlib.Data.Fintype.EquivFin
import D0.Synthesis.SectorFieldIndependence

/-!
# Full Galois closure of the three sector characters

`D0-SECTOR-FIELD-INDEPENDENCE-001` constructed the degree-eight field

`K₈ = ℚ(√5, √10, √386579)`

and three commuting sign involutions `σ_α`, `σ_DE`, `σ_transport` with the diagonal
eigenvector table

`diag(-1,+1,+1)`, `diag(+1,-1,+1)`, `diag(+1,+1,-1)`.

This module closes the remaining internal Galois question.

1. The `2³ = 8` products of the three signs define eight distinct `ℚ`-automorphisms
   (`signAut_injective`), distinguished by their action on the three explicit axis generators.
2. For every finite extension, `|Aut(K/F)| ≤ [K:F]`; here the right side is `8`, so the
   injection and the general upper bound force `|Aut(K₈/ℚ)| = 8`.
3. Mathlib's `IsGalois.of_card_aut_eq_finrank` then proves `K₈/ℚ` Galois.
4. `signAut_bijective` proves every automorphism is uniquely one of the eight sign choices.

Thus the Galois group is exactly the explicit three-bit sign group `(ℤ/2)³`, not merely a
commuting subgroup. All field/algebra/module instances are supplied explicitly to avoid the
nested `QuadraticAlgebra` native-vs-local instance diamond.
-/

namespace D0.Synthesis.SectorGaloisClosure

open D0.Synthesis.SectorFieldIndependence

noncomputable section

-- Restore the exact scalar structures used by the nested quadratic tower.
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

/-- The eight sign automorphisms, indexed by a three-bit vector. -/
def signAut (p : Bool × Bool × Bool) :
    SectorCharacterAlgebra ≃ₐ[ℚ] SectorCharacterAlgebra :=
  (if p.1 then sigmaAlpha else 1) *
  (if p.2.1 then sigmaDE else 1) *
  (if p.2.2 then sigmaTransport else 1)

theorem signAut_alphaAxis (p : Bool × Bool × Bool) :
    signAut p alphaAxis = if p.1 then -alphaAxis else alphaAxis := by
  rcases p with ⟨a, b, c⟩
  cases a <;> cases b <;> cases c <;> rfl

theorem signAut_deAxis (p : Bool × Bool × Bool) :
    signAut p deAxis = if p.2.1 then -deAxis else deAxis := by
  rcases p with ⟨a, b, c⟩
  cases a <;> cases b <;> cases c <;> rfl

theorem signAut_transportAxis (p : Bool × Bool × Bool) :
    signAut p transportAxis = if p.2.2 then -transportAxis else transportAxis := by
  rcases p with ⟨a, b, c⟩
  cases a <;> cases b <;> cases c <;> rfl

private theorem negAlpha : -alphaAxis ≠ alphaAxis := by
  intro h
  have hh := congrArg (fun z : SectorCharacterAlgebra => z.re.re.im) h
  norm_num [alphaAxis, sqrtGen, QuadraticAlgebra.algebraMap_eq,
    QuadraticAlgebra.re_one, QuadraticAlgebra.im_one] at hh

private theorem negDe : -deAxis ≠ deAxis := by
  intro h
  have hh := congrArg (fun z : SectorCharacterAlgebra => z.re.im.re) h
  norm_num [deAxis, sqrtGen, QuadraticAlgebra.algebraMap_eq,
    QuadraticAlgebra.re_one, QuadraticAlgebra.im_one] at hh

private theorem negTransport : -transportAxis ≠ transportAxis := by
  intro h
  have hh := congrArg (fun z : SectorCharacterAlgebra => z.im.re.re) h
  norm_num [transportAxis, sqrtGen, QuadraticAlgebra.algebraMap_eq,
    QuadraticAlgebra.re_one, QuadraticAlgebra.im_one] at hh

private theorem alphaNeg : alphaAxis ≠ -alphaAxis := fun h => negAlpha h.symm
private theorem deNeg : deAxis ≠ -deAxis := fun h => negDe h.symm
private theorem transportNeg : transportAxis ≠ -transportAxis := fun h => negTransport h.symm

/-- The eight sign choices give eight distinct automorphisms. -/
theorem signAut_injective : Function.Injective signAut := by
  rintro ⟨a, b, c⟩ ⟨a', b', c'⟩ h
  have ha := congrArg (fun e => e alphaAxis) h
  have hb := congrArg (fun e => e deAxis) h
  have hc := congrArg (fun e => e transportAxis) h
  change signAut (a, b, c) alphaAxis = signAut (a', b', c') alphaAxis at ha
  change signAut (a, b, c) deAxis = signAut (a', b', c') deAxis at hb
  change signAut (a, b, c) transportAxis = signAut (a', b', c') transportAxis at hc
  rw [signAut_alphaAxis, signAut_alphaAxis] at ha
  rw [signAut_deAxis, signAut_deAxis] at hb
  rw [signAut_transportAxis, signAut_transportAxis] at hc
  cases a <;> cases a' <;> cases b <;> cases b' <;> cases c <;> cases c' <;>
    simp_all [negAlpha, negDe, negTransport, alphaNeg, deNeg, transportNeg]

/-- The automorphism group has exactly eight elements. -/
theorem sector_galois_card :
    Fintype.card (SectorCharacterAlgebra ≃ₐ[ℚ] SectorCharacterAlgebra) = 8 := by
  have hle₀ :=
    @AlgEquiv.card_le ℚ SectorCharacterAlgebra inferInstance sectorCharacterField algQC fdC
  have hle : Fintype.card (SectorCharacterAlgebra ≃ₐ[ℚ] SectorCharacterAlgebra) ≤ 8 :=
    hle₀.trans_eq sector_character_finrank
  have hge₀ := Fintype.card_le_of_injective signAut signAut_injective
  have hge : 8 ≤ Fintype.card (SectorCharacterAlgebra ≃ₐ[ℚ] SectorCharacterAlgebra) := by
    norm_num at hge₀ ⊢
    exact hge₀
  exact Nat.le_antisymm hle hge

/-- The degree-eight sector field is Galois over `ℚ`. -/
theorem sector_isGalois : IsGalois ℚ SectorCharacterAlgebra := by
  apply @IsGalois.of_card_aut_eq_finrank ℚ inferInstance SectorCharacterAlgebra
    sectorCharacterField algQC fdC
  rw [Nat.card_eq_fintype_card]
  have hfin : Module.finrank ℚ SectorCharacterAlgebra = 8 := sector_character_finrank
  exact sector_galois_card.trans hfin.symm

/-- Every `ℚ`-automorphism of the sector field is uniquely one of the eight sign choices. -/
theorem signAut_bijective : Function.Bijective signAut := by
  apply (Fintype.bijective_iff_injective_and_card signAut).2
  refine ⟨signAut_injective, ?_⟩
  norm_num [sector_galois_card]

/-- A concrete equivalence between three-bit sign vectors and the full Galois group. -/
noncomputable def signBitsEquivGalois :
    (Bool × Bool × Bool) ≃ (SectorCharacterAlgebra ≃ₐ[ℚ] SectorCharacterAlgebra) :=
  Equiv.ofBijective signAut signAut_bijective

/-- Capstone: degree 8, Galois, eight automorphisms, and every automorphism is a unique
three-bit sign choice. -/
theorem sector_galois_closure :
    Module.finrank ℚ SectorCharacterAlgebra = 8
      ∧ IsGalois ℚ SectorCharacterAlgebra
      ∧ Fintype.card (SectorCharacterAlgebra ≃ₐ[ℚ] SectorCharacterAlgebra) = 8
      ∧ Function.Bijective signAut :=
  ⟨sector_character_finrank, sector_isGalois, sector_galois_card, signAut_bijective⟩

end

end D0.Synthesis.SectorGaloisClosure
