import Mathlib.Algebra.Group.Hom.Basic
import Mathlib.Algebra.Group.Pi.Basic
import Mathlib.Data.Nat.Fib.Basic
import Mathlib.Data.Nat.GCD.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.GroupTheory.OrderOfElement
import D0.Core.DyadABCD
import D0.Geometry.ArchiveRefinementTower
import D0.Geometry.ArchiveRolePhaseGroup

/-!
# Group-refinement boundary for consecutive Role-phase moduli

Owned consecutive Role-phase fibres `L = n+2`, `L' = n+3` are always coprime, so every
additive group homomorphism `(Role → ZMod L') →+ (Role → ZMod L)` is the zero map.
The zero homomorphism exists; there is no nontrivial (in particular no surjective) group
refinement along the owned consecutive step.

A surjective product-cyclic refinement still forces the necessary divisibility `L ∣ L'`.
Explicit hostile named sequences fail that necessary adjacent condition at an early step.
-/

namespace D0.Geometry

open D0

private theorem eq_zero_of_coprime_annihilators
    {B : Type*} [AddCommGroup B] {L L' : ℕ} {b : B}
    (hL : L • b = 0) (hL' : L' • b = 0) (hcop : Nat.Coprime L L') : b = 0 := by
  obtain ⟨u, v, huv⟩ := hcop.isCoprime
  have : (1 : ℤ) • b = 0 := by
    calc
      (1 : ℤ) • b
          = (u * (L : ℤ) + v * (L' : ℤ)) • b := by
            simpa using congrArg (fun z : ℤ => z • b) huv.symm
      _ = (u * (L : ℤ)) • b + (v * (L' : ℤ)) • b := add_zsmul _ _ _
      _ = u • ((L : ℤ) • b) + v • ((L' : ℤ) • b) := by simp [mul_zsmul]
      _ = u • (L • b) + v • (L' • b) := by simp [natCast_zsmul]
      _ = 0 := by simp [hL, hL']
  simpa using this

private theorem nsmul_roleZMod_eq_zero {L : ℕ} [NeZero L] (x : Role → ZMod L) :
    L • x = 0 := by
  funext r
  change L • x r = (0 : ZMod L)
  rw [nsmul_eq_mul, CharP.cast_eq_zero (ZMod L) L, zero_mul]

/-- General Role-product lemma: `gcd(L,L')=1` forces every additive hom to be zero. -/
theorem roleZModAddHom_eq_zero_of_coprime {L L' : ℕ} [NeZero L] [NeZero L']
    (hcop : Nat.Coprime L L')
    (f : (Role → ZMod L') →+ (Role → ZMod L)) : f = 0 := by
  apply AddMonoidHom.ext
  intro x
  refine eq_zero_of_coprime_annihilators (nsmul_roleZMod_eq_zero (f x)) ?_ hcop
  calc
    L' • f x = f (L' • x) := (map_nsmul f L' x).symm
    _ = f 0 := by rw [nsmul_roleZMod_eq_zero x]
    _ = 0 := by simp

/-- Owned consecutive fibre cardinalities are always coprime. -/
theorem archiveFibers_consecutive_coprime (n : ℕ) :
    Nat.Coprime (archiveFibers n) (archiveFibers (n + 1)) := by
  unfold archiveFibers
  exact (Nat.coprime_self_add_right (m := n + 2) (n := 1)).2 (Nat.coprime_one_right _)

/-- Consecutive Role-phase group homs are trivial (the zero hom). -/
theorem consecutive_rolePhase_addHom_eq_zero (n : ℕ)
    (f : ArchiveRolePhaseGroup (n + 1) →+ ArchiveRolePhaseGroup n) : f = 0 :=
  roleZModAddHom_eq_zero_of_coprime (archiveFibers_consecutive_coprime n) f

/-- Zero hom exists, so the consecutive statement is triviality rather than emptiness. -/
theorem consecutive_rolePhase_zeroHom_exists (n : ℕ) :
    ∃ f : ArchiveRolePhaseGroup (n + 1) →+ ArchiveRolePhaseGroup n, f = 0 :=
  ⟨0, rfl⟩

/-- No nontrivial consecutive Role-phase group refinement. -/
theorem no_nontrivial_consecutive_rolePhase_group_refinement (n : ℕ)
    (f : ArchiveRolePhaseGroup (n + 1) →+ ArchiveRolePhaseGroup n) :
    f = 0 :=
  consecutive_rolePhase_addHom_eq_zero n f

/-- Point mass generator: `1` at a fixed role, `0` elsewhere. -/
def roleUnit (L : ℕ) [NeZero L] (r : Role) : Role → ZMod L :=
  fun s => if s = r then (1 : ZMod L) else 0

theorem nsmul_roleUnit (L m : ℕ) [NeZero L] (r : Role) :
    m • roleUnit L r = fun s => if s = r then (m : ZMod L) else 0 := by
  funext s
  change m • roleUnit L r s = _
  simp only [roleUnit]
  split_ifs <;> simp [nsmul_eq_mul]

theorem addOrderOf_roleUnit (L : ℕ) [NeZero L] (r : Role) :
    addOrderOf (roleUnit L r) = L := by
  rw [addOrderOf_eq_iff (Nat.pos_of_neZero L)]
  constructor
  · rw [nsmul_roleUnit]
    funext s
    split_ifs <;> simp
  · intro m hm hmpos
    rw [nsmul_roleUnit]
    intro h
    have hm0 : (m : ZMod L) = 0 := by
      simpa using congrFun h r
    have hdiv : L ∣ m := (ZMod.natCast_eq_zero_iff m L).1 hm0
    exact (Nat.le_of_dvd hmpos hdiv).not_gt hm

/-- Surjective product-cyclic refinement requires modulus divisibility. -/
theorem surjective_roleZMod_addHom_implies_dvd
    {L L' : ℕ} [NeZero L] [NeZero L']
    (f : (Role → ZMod L') →+ (Role → ZMod L))
    (hf : Function.Surjective f) : L ∣ L' := by
  have hAnn : ∀ y : Role → ZMod L, L' • y = 0 := by
    intro y
    obtain ⟨x, rfl⟩ := hf y
    calc
      L' • f x = f (L' • x) := (map_nsmul f L' x).symm
      _ = f 0 := by rw [nsmul_roleZMod_eq_zero x]
      _ = 0 := by simp
  obtain ⟨r⟩ := (inferInstance : Nonempty Role)
  have hkill : L' • roleUnit L r = 0 := hAnn _
  have hord : addOrderOf (roleUnit L r) = L := addOrderOf_roleUnit L r
  have : addOrderOf (roleUnit L r) ∣ L' :=
    (addOrderOf_dvd_iff_nsmul_eq_zero).2 hkill
  simpa [hord] using this

/-- Surjective consecutive refinement is impossible. -/
theorem no_surjective_consecutive_rolePhase_group_refinement (n : ℕ)
    (f : ArchiveRolePhaseGroup (n + 1) →+ ArchiveRolePhaseGroup n)
    (hf : Function.Surjective f) : False := by
  have hdiv :
      archiveFibers n ∣ archiveFibers (n + 1) :=
    surjective_roleZMod_addHom_implies_dvd (L := archiveFibers n)
      (L' := archiveFibers (n + 1)) f hf
  have hdiv' : n + 2 ∣ (n + 2) + 1 := by
    simpa [archiveFibers, Nat.add_assoc] using hdiv
  have h1 : n + 2 ∣ 1 := (Nat.dvd_add_self_left (m := n + 2) (n := 1)).mp hdiv'
  have hnot : ¬ n + 2 ∣ 1 :=
    Nat.not_dvd_of_pos_of_lt (by decide : (0 : ℕ) < 1) (by omega : 1 < n + 2)
  exact hnot h1

/-! ## Hostile named full consecutive surjective towers -/

def hostileFib (j : ℕ) : ℕ := Nat.fib j
def hostileFibAddOne (j : ℕ) : ℕ := Nat.fib j + 1
def hostileFibAddTwo (j : ℕ) : ℕ := Nat.fib j + 2

/-- Explicit rationalized initial `floor(φ^j)` controls from the memo: 1,2,4,6,11. -/
def hostileFloorPhi : ℕ → ℕ
  | 0 => 1
  | 1 => 2
  | 2 => 4
  | 3 => 6
  | 4 => 11
  | n + 5 => hostileFloorPhi (n + 4) + hostileFloorPhi (n + 3)

/-- Lucas-style memo sequence 1,3,4,7,11,… -/
def hostileLucas : ℕ → ℕ
  | 0 => 1
  | 1 => 3
  | n + 2 => hostileLucas n + hostileLucas (n + 1)

/-- One adjacent failure per named full consecutive surjective tower
(memo pairs: 2∤3, 2∤3, 3∤4, 4∤6, 3∤4). -/
theorem hostile_named_full_consecutive_towers_fail_divisibility :
    (¬ hostileFib 3 ∣ hostileFib 4) ∧
    (¬ hostileFibAddOne 2 ∣ hostileFibAddOne 3) ∧
    (¬ hostileFibAddTwo 2 ∣ hostileFibAddTwo 3) ∧
    (¬ hostileFloorPhi 2 ∣ hostileFloorPhi 3) ∧
    (¬ hostileLucas 1 ∣ hostileLucas 2) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> decide

end D0.Geometry
