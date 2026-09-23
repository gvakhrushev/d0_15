import Mathlib.Tactic
import D0.Geometry.ArchiveCubicalDifferential
import D0.Geometry.ArchiveHodgeCARDirac

namespace D0.Geometry

open D0
open scoped BigOperators

/-!
# Algebraic complementary primal/dual pairing on the archive cochains

This owner pairs complementary occupation labels at the same archive site.  It
does not locate geometric dual cells.  Placement data are kept in a separate,
explicit structure below.
-/

/-- Occupation-label complement on the existing archive Fock carrier. -/
def occupationComplement (S : ArchiveFockState) : ArchiveFockState := fun r => !(S r)

@[simp] theorem occupationComplement_apply (S : ArchiveFockState) (r : Role) :
    occupationComplement S r = !(S r) := rfl

@[simp] theorem occupationComplement_involutive (S : ArchiveFockState) :
    occupationComplement (occupationComplement S) = S := by
  funext r
  simp [occupationComplement]

/-- The four-mode degree relation for complementary occupation labels. -/
theorem degree_complement : ∀ S : ArchiveFockState,
    fockDegree (occupationComplement S) = 4 - fockDegree S := by
  native_decide

/-- Number of inversions in the ordered concatenation `S, Sᶜ`. -/
def complementOrientationInversions (S : ArchiveFockState) : ℕ :=
  (Finset.univ.filter fun p : Role × Role =>
    S p.1 = true ∧ S p.2 = false ∧ roleOrderIndex p.2 < roleOrderIndex p.1).card

/-- Orientation coefficient of the algebraic complementary label. -/
def complementOrientationInt (S : ArchiveFockState) : ℤ :=
  if complementOrientationInversions S % 2 = 0 then 1 else -1

def complementOrientation (S : ArchiveFockState) : ℝ :=
  (complementOrientationInt S : ℝ)

theorem complementOrientation_sq (S : ArchiveFockState) :
    complementOrientation S * complementOrientation S = 1 := by
  unfold complementOrientation
  have h : complementOrientationInt S = 1 ∨ complementOrientationInt S = -1 := by
    unfold complementOrientationInt
    split <;> simp_all
  rcases h with h | h <;> simp [h]

/-- Complement orientation reversal, with the Koszul sign of degrees `k` and `4-k`. -/
theorem epsilon_complement_sign_int : ∀ S : ArchiveFockState,
    complementOrientationInt S * complementOrientationInt (occupationComplement S) =
      if (fockDegree S * (4 - fockDegree S)) % 2 = 0 then 1 else -1 := by
  native_decide

theorem epsilon_complement_sign (S : ArchiveFockState) :
    complementOrientation S * complementOrientation (occupationComplement S) =
      if (fockDegree S * (4 - fockDegree S)) % 2 = 0 then 1 else -1 := by
  have h := congrArg (fun z : ℤ => (z : ℝ)) (epsilon_complement_sign_int S)
  simpa [complementOrientation] using h

/-- The literal homogeneous subspace of archive cochains. -/
def archiveDegreeSubmodule (N k : ℕ) : Submodule ℝ (ArchiveCochain N) where
  carrier := {ψ | HomogeneousCochain N k ψ}
  zero_mem' := homogeneousCochain_zero N k
  add_mem' := by
    intro ψ φ hψ hφ
    exact homogeneousCochain_add N k ψ φ hψ hφ
  smul_mem' := by
    intro c ψ hψ x S hS
    simp [HomogeneousCochain, hψ x S hS]

/-- Apply the signed occupation-complement map to a dual-degree cochain. -/
def algebraicComplementToPrimal (N k : ℕ) (hk : k ≤ 4)
    (z : archiveDegreeSubmodule N (4 - k)) : archiveDegreeSubmodule N k := by
  refine ⟨fun p => if fockDegree p.2 = k then
    complementOrientation p.2 * z.1 (p.1, occupationComplement p.2) else 0, ?_⟩
  intro x S hS
  simp only [Pi.zero_apply]
  split
  · rename_i h
    exact (hS h).elim
  · rfl

/-- Inverse signed complement map, using the same involution and orientation. -/
def algebraicPrimalToComplement (N k : ℕ) (hk : k ≤ 4)
    (φ : archiveDegreeSubmodule N k) : archiveDegreeSubmodule N (4 - k) := by
  refine ⟨fun p => if fockDegree p.2 = 4 - k then
    complementOrientation (occupationComplement p.2) *
      φ.1 (p.1, occupationComplement p.2) else 0, ?_⟩
  intro x S hS
  simp only [Pi.zero_apply]
  split
  · rename_i h
    exact (hS h).elim
  · rfl

/-- Signed complement is a linear equivalence between primal and complementary labels. -/
noncomputable def algebraicComplementEquiv (N k : ℕ) (hk : k ≤ 4) :
    archiveDegreeSubmodule N (4 - k) ≃ₗ[ℝ] archiveDegreeSubmodule N k where
  toFun := algebraicComplementToPrimal N k hk
  invFun := algebraicPrimalToComplement N k hk
  left_inv := by
    intro z
    apply Subtype.ext
    funext p
    by_cases h : fockDegree p.2 = 4 - k
    · have hc : fockDegree (occupationComplement p.2) = k := by
        rw [degree_complement, h]
        omega
      simp only [algebraicComplementToPrimal, algebraicPrimalToComplement,
        if_pos h, if_pos hc, occupationComplement_involutive]
      rw [← mul_assoc, complementOrientation_sq]
      ring
    · have hz := z.2 p.1 p.2 h
      simp [algebraicComplementToPrimal, algebraicPrimalToComplement, h, hz]
  right_inv := by
    intro φ
    apply Subtype.ext
    funext p
    by_cases h : fockDegree p.2 = k
    · have hc : fockDegree (occupationComplement p.2) = 4 - k := by
        rw [degree_complement, h]
      simp only [algebraicComplementToPrimal, algebraicPrimalToComplement,
        if_pos h, if_pos hc, occupationComplement_involutive]
      rw [← mul_assoc, complementOrientation_sq]
      ring
    · have hφ := φ.2 p.1 p.2 h
      simp [algebraicComplementToPrimal, algebraicPrimalToComplement, h, hφ]
  map_add' z w := by
    apply Subtype.ext
    funext p
    by_cases h : fockDegree p.2 = k <;>
      simp [algebraicComplementToPrimal, h] <;> ring
  map_smul' c z := by
    apply Subtype.ext
    funext p
    by_cases h : fockDegree p.2 = k <;>
      simp [algebraicComplementToPrimal, h] <;> ring

/-- The complementary evaluation map exposed as a reusable owner. -/
noncomputable def evaluation_equiv_complement (N k : ℕ) (hk : k ≤ 4) :
    archiveDegreeSubmodule N (4 - k) ≃ₗ[ℝ] archiveDegreeSubmodule N k :=
  algebraicComplementEquiv N k hk

/-- Signed complementary pairing on literal site/Fock cochains. -/
def algebraicComplementPairing (N k : ℕ) (hk : k ≤ 4)
    (φ : archiveDegreeSubmodule N k)
    (z : archiveDegreeSubmodule N (4 - k)) : ℝ :=
  cochainPairing N φ.1 (algebraicComplementToPrimal N k hk z).1

theorem algebraicComplementPairing_sub_right (N k : ℕ) (hk : k ≤ 4)
    (φ : archiveDegreeSubmodule N k)
    (z w : archiveDegreeSubmodule N (4 - k)) :
    algebraicComplementPairing N k hk φ (z - w) =
      algebraicComplementPairing N k hk φ z -
        algebraicComplementPairing N k hk φ w := by
  unfold algebraicComplementPairing
  have hmap : algebraicComplementToPrimal N k hk (z - w) =
      algebraicComplementToPrimal N k hk z - algebraicComplementToPrimal N k hk w :=
    (algebraicComplementEquiv N k hk).map_sub z w
  rw [hmap]
  simp [cochainPairing, Pi.sub_apply, mul_sub, Finset.sum_sub_distrib]

/-- The counting pairing reads a coordinate against a literal delta cochain. -/
theorem cochainPairing_basis_right (N : ℕ) (ψ : ArchiveCochain N)
    (p : ArchiveCochainBasis N) :
    cochainPairing N ψ (fun q => if q = p then 1 else 0) = ψ p := by
  classical
  unfold cochainPairing
  calc
    (∑ x, ∑ s, ψ (x, s) * (if (x, s) = p then (1 : ℝ) else 0)) =
        ∑ q : ArchiveCochainBasis N, ψ q * (if q = p then (1 : ℝ) else 0) :=
      (Fintype.sum_prod_type
        (fun q : ArchiveCochainBasis N => ψ q * (if q = p then (1 : ℝ) else 0))).symm
    _ = ψ p := by
      rw [Finset.sum_eq_single p]
      · simp
      · intro q hq hne
        simp [hne]
      · simp

/-- Delta evaluation in the first slot follows by symmetry of the counting pairing. -/
theorem cochainPairing_basis_left (N : ℕ) (ψ : ArchiveCochain N)
    (p : ArchiveCochainBasis N) :
    cochainPairing N (fun q => if q = p then 1 else 0) ψ = ψ p := by
  rw [cochainPairing_symm]
  exact cochainPairing_basis_right N ψ p

theorem algebraicComplementPairing_sum (N k : ℕ) (hk : k ≤ 4)
    (φ : archiveDegreeSubmodule N k)
    (z : archiveDegreeSubmodule N (4 - k)) :
    algebraicComplementPairing N k hk φ z =
      ∑ x, ∑ S, if fockDegree S = k then
        complementOrientation S * φ.1 (x, S) * z.1 (x, occupationComplement S)
        else 0 := by
  unfold algebraicComplementPairing cochainPairing algebraicComplementToPrimal
  apply Finset.sum_congr rfl
  intro x hx
  apply Finset.sum_congr rfl
  intro S hS
  by_cases h : fockDegree S = k <;> simp [h] <;> ring

/-- The signed pairing separates every nonzero primal cochain. -/
theorem algebraicComplementPairing_left_nondegenerate
    (N k : ℕ) (hk : k ≤ 4) (φ : archiveDegreeSubmodule N k)
    (hφ : ∀ z : archiveDegreeSubmodule N (4 - k),
      algebraicComplementPairing N k hk φ z = 0) : φ = 0 := by
  apply Subtype.ext
  funext p
  by_cases hp : fockDegree p.2 = k
  · let b : ArchiveCochain N := fun q => if q = p then 1 else 0
    have hb : b ∈ archiveDegreeSubmodule N k := by
      intro x S hS
      by_cases hq : (x, S) = p
      · have hS_eq : S = p.2 := congrArg Prod.snd hq
        have hdeg : fockDegree S = k := by rw [hS_eq]; exact hp
        exact (hS hdeg).elim
      · simp [b, hq]
    let b' : archiveDegreeSubmodule N k := ⟨b, hb⟩
    let z := (algebraicComplementEquiv N k hk).symm b'
    have hz := hφ z
    have he : algebraicComplementToPrimal N k hk z = b' :=
      (algebraicComplementEquiv N k hk).apply_symm_apply b'
    have heval : algebraicComplementPairing N k hk φ z = φ.1 p := by
      unfold algebraicComplementPairing
      rw [show (algebraicComplementToPrimal N k hk z).1 = b from congrArg Subtype.val he]
      exact cochainPairing_basis_right N φ.1 p
    rw [heval] at hz
    exact hz
  · exact φ.2 p.1 p.2 hp

/-- The signed pairing is perfect on both finite homogeneous sectors. -/
theorem algebraicComplementPairing_perfect (N k : ℕ) (hk : k ≤ 4) :
    (∀ φ : archiveDegreeSubmodule N k,
      (∀ z : archiveDegreeSubmodule N (4 - k),
        algebraicComplementPairing N k hk φ z = 0) → φ = 0) ∧
    (∀ z : archiveDegreeSubmodule N (4 - k),
      (∀ φ : archiveDegreeSubmodule N k,
        algebraicComplementPairing N k hk φ z = 0) → z = 0) := by
  constructor
  · exact algebraicComplementPairing_left_nondegenerate N k hk
  · intro z hz
    have hJ : algebraicComplementToPrimal N k hk z = 0 := by
      apply Subtype.ext
      funext p
      by_cases hp : fockDegree p.2 = k
      · let b : ArchiveCochain N := fun q => if q = p then 1 else 0
        have hb : b ∈ archiveDegreeSubmodule N k := by
          intro x S hS
          by_cases hq : (x, S) = p
          · have hS_eq : S = p.2 := congrArg Prod.snd hq
            have hdeg : fockDegree S = k := by rw [hS_eq]; exact hp
            exact (hS hdeg).elim
          · simp [b, hq]
        have htest := hz ⟨b, hb⟩
        have hvalue : (algebraicComplementToPrimal N k hk z).1 p = 0 := by
          rw [← cochainPairing_basis_left N (algebraicComplementToPrimal N k hk z).1 p]
          simpa [algebraicComplementPairing, b] using htest
        exact hvalue
      · exact (algebraicComplementToPrimal N k hk z).2 p.1 p.2 hp
    apply (algebraicComplementEquiv N k hk).injective
    change algebraicComplementToPrimal N k hk z =
      algebraicComplementToPrimal N k hk 0
    rw [hJ]
    exact (map_zero (algebraicComplementEquiv N k hk).toLinearMap).symm

/-! ## Supplied geometric placement data (no canonical instance) -/

/-- Data required to turn algebraic complementary labels into located dual cells. -/
structure GeometryDualPlacement (N k : ℕ) where
  targetSite : ArchiveRolePhaseGroup N → ArchiveFockState → ArchiveRolePhaseGroup N
  orientationCoefficient : ArchiveRolePhaseGroup N → ArchiveFockState → ℝ
  dualIncidence : ArchiveRolePhaseGroup N → ArchiveFockState → ℝ
  localVolume : Option (ArchiveRolePhaseGroup N → ArchiveFockState → ℝ) := none

/-- First local placement: keep the archive site. -/
def identityDualPlacement (N k : ℕ) : GeometryDualPlacement N k where
  targetSite x _ := x
  orientationCoefficient _ S := complementOrientation S
  dualIncidence _ _ := 1
  localVolume := none

/-- Second local placement: translate the target by one role edge. -/
def shiftedDualPlacement (N k : ℕ) : GeometryDualPlacement N k where
  targetSite x _ := roleTranslatePlus N D0.A x
  orientationCoefficient _ S := complementOrientation S
  dualIncidence _ _ := 1
  localVolume := none

/-- A role edge is nonzero whenever the archive cycle has at least three sites. -/
theorem roleStep_A_ne_zero_of_three_le (N : ℕ) (hN : 3 ≤ archiveFibers N) :
    roleStep N D0.A ≠ 0 := by
  intro h
  have hA := congrFun h D0.A
  have hval : (1 : ZMod (archiveFibers N)) = 0 := by
    simpa [roleStep] using hA
  have hone : (1 : ZMod (archiveFibers N)) ≠ 0 := by
    intro hcast
    have hdiv : archiveFibers N ∣ 1 :=
      (ZMod.natCast_eq_zero_iff 1 (archiveFibers N)).mp (by simpa using hcast)
    have : archiveFibers N ≤ 1 := Nat.le_of_dvd (by norm_num) hdiv
    omega
  exact hone hval

/-- The two rules have the same primal and complementary carrier cardinalities. -/
theorem placement_carrier_cardinalities_equal (N k : ℕ) :
    Fintype.card (ArchiveRolePhaseGroup N × ArchiveFockState) =
      Fintype.card (ArchiveRolePhaseGroup N × ArchiveFockState) := rfl

/-- Equal carrier cardinality does not identify a located dual-cell placement. -/
theorem same_cardinality_does_not_provide_placement (N k : ℕ)
    (hN : 3 ≤ archiveFibers N) :
    identityDualPlacement N k ≠ shiftedDualPlacement N k := by
  intro h
  have hsite := congrArg
    (fun P : GeometryDualPlacement N k => P.targetSite 0 fockVacuumState) h
  have hstep : roleStep N D0.A = 0 := by
    simpa [identityDualPlacement, shiftedDualPlacement, roleTranslatePlus,
      roleTranslate] using hsite.symm
  exact roleStep_A_ne_zero_of_three_le N hN hstep

end D0.Geometry
