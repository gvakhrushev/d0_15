import Mathlib.Tactic
import D0.Geometry.ArchiveCARDirac
import D0.Geometry.RoleFockPermutation

/-!
# Intrinsic commutant of the owned Fock/CAR operators

The corrected Hodge/CAR operator and the older hopping operator both couple
each role through the same real Fock matrix `γ_r = c_r + c_r†`.  The
commutant of those four matrices is computed here, together with the smaller
commutant of the full creation/annihilation family.

The result is not a Standard Model gauge algebra.  Verdict:
`INTRINSIC-COMMUTANT-NOT-SM`.
-/

namespace D0.Geometry

open D0
open RoleFockPermutation

def flipRole (r : Role) (s : ArchiveFockState) : ArchiveFockState :=
  fun t => if t = r then !s t else s t

def occupationBit (r : Role) (s : ArchiveFockState) : ℤ :=
  if s r then 1 else 0

def fockNumberInt (r : Role) (bra ket : ArchiveFockState) : ℤ :=
  fockMatMul (carCreateInt r) (carAnnihilateInt r) bra ket

def fockComm (M N : ArchiveFockState → ArchiveFockState → ℤ)
    (bra ket : ArchiveFockState) : ℤ :=
  fockMatMul M N bra ket - fockMatMul N M bra ket

def FockScalar (M : ArchiveFockState → ArchiveFockState → ℤ) : Prop :=
  ∃ c : ℤ, ∀ bra ket, M bra ket = c * fockIdentityInt bra ket

theorem fockMatMul_assoc (M N P : ArchiveFockState → ArchiveFockState → ℤ) :
    fockMatMul (fockMatMul M N) P = fockMatMul M (fockMatMul N P) := by
  classical
  funext bra ket
  simp only [fockMatMul, Finset.mul_sum, Finset.sum_mul]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl ?_
  intro mid _
  refine Finset.sum_congr rfl ?_
  intro mid2 _
  ring

theorem fockMatMul_add_left (M N P : ArchiveFockState → ArchiveFockState → ℤ) :
    fockMatMul (fun bra ket => M bra ket + N bra ket) P =
      fun bra ket => fockMatMul M P bra ket + fockMatMul N P bra ket := by
  classical
  funext bra ket
  simp only [fockMatMul, add_mul, Finset.sum_add_distrib]

theorem fockMatMul_sub_left (M N P : ArchiveFockState → ArchiveFockState → ℤ) :
    fockMatMul (fun bra ket => M bra ket - N bra ket) P =
      fun bra ket => fockMatMul M P bra ket - fockMatMul N P bra ket := by
  classical
  funext bra ket
  simp only [fockMatMul, sub_mul, Finset.sum_sub_distrib]

theorem fockMatMul_add_right (M N P : ArchiveFockState → ArchiveFockState → ℤ) :
    fockMatMul M (fun bra ket => N bra ket + P bra ket) =
      fun bra ket => fockMatMul M N bra ket + fockMatMul M P bra ket := by
  classical
  funext bra ket
  simp only [fockMatMul, mul_add, Finset.sum_add_distrib]

theorem fockMatMul_sub_right (M N P : ArchiveFockState → ArchiveFockState → ℤ) :
    fockMatMul M (fun bra ket => N bra ket - P bra ket) =
      fun bra ket => fockMatMul M N bra ket - fockMatMul M P bra ket := by
  classical
  funext bra ket
  simp only [fockMatMul, mul_sub, Finset.sum_sub_distrib]

theorem flipRole_idem (r : Role) (s : ArchiveFockState) :
    flipRole r (flipRole r s) = s := by
  funext t
  by_cases ht : t = r
  · simp [flipRole, ht]
  · simp [flipRole, ht]

theorem flipRole_eq_self_iff (r : Role) (s : ArchiveFockState) :
    flipRole r s = s ↔ False := by
  constructor
  · intro h
    have := congrFun h r
    simp [flipRole] at this
  · intro h
    exact h.elim

theorem fockNumberInt_eq_occupation (r : Role) (bra ket : ArchiveFockState) :
    fockNumberInt r bra ket = if bra = ket then occupationBit r bra else 0 := by
  classical
  revert bra ket r
  native_decide

theorem fockMatMul_diagonal_number (M : ArchiveFockState → ArchiveFockState → ℤ)
    (r : Role) (bra ket : ArchiveFockState) :
    fockMatMul M (fockNumberInt r) bra ket =
      M bra ket * occupationBit r ket ∧
    fockMatMul (fockNumberInt r) M bra ket =
      occupationBit r bra * M bra ket := by
  classical
  constructor
  · simp only [fockMatMul, fockNumberInt_eq_occupation]
    rw [Finset.sum_eq_single ket]
    · simp [occupationBit]
    · intro mid _ hmid
      rw [if_neg hmid]
      simp
    · intro h
      exact (h (Finset.mem_univ _)).elim
  · simp only [fockMatMul, fockNumberInt_eq_occupation]
    rw [Finset.sum_eq_single bra]
    · simp [occupationBit]
    · intro mid _ hmid
      rw [if_neg (Ne.symm hmid)]
      simp
    · intro h
      exact (h (Finset.mem_univ _)).elim

theorem fock_comm_number_forces_diagonal
    (M : ArchiveFockState → ArchiveFockState → ℤ)
    (hN : ∀ r bra ket, fockComm M (fockNumberInt r) bra ket = 0)
    {bra ket : ArchiveFockState} (hneq : bra ≠ ket) : M bra ket = 0 := by
  classical
  obtain ⟨r, hr⟩ : ∃ r : Role, bra r ≠ ket r := by
    by_contra h
    push Not at h
    apply hneq
    funext r
    exact h r
  have hdiff : occupationBit r ket - occupationBit r bra ≠ 0 := by
    simp only [occupationBit]
    cases hbr : bra r <;> cases hkt : ket r <;> simp [hbr, hkt] at hr ⊢
  have hcomm := hN r bra ket
  unfold fockComm at hcomm
  have hmul := fockMatMul_diagonal_number M r bra ket
  rw [hmul.1, hmul.2] at hcomm
  have hlin : (occupationBit r ket - occupationBit r bra) * M bra ket = 0 := by
    linear_combination hcomm
  exact (mul_eq_zero.mp hlin).resolve_left hdiff

theorem fockComm_of_factors
    (M A B : ArchiveFockState → ArchiveFockState → ℤ)
    (hA : ∀ bra ket, fockComm M A bra ket = 0)
    (hB : ∀ bra ket, fockComm M B bra ket = 0) :
    ∀ bra ket, fockComm M (fun x y => fockMatMul A B x y) bra ket = 0 := by
  classical
  intro bra ket
  unfold fockComm
  have hAfun : fockMatMul M A = fockMatMul A M := by
    funext x y
    have h := hA x y
    unfold fockComm at h
    linear_combination h
  have hBfun : fockMatMul M B = fockMatMul B M := by
    funext x y
    have h := hB x y
    unfold fockComm at h
    linear_combination h
  rw [← fockMatMul_assoc, hAfun, fockMatMul_assoc, hBfun, fockMatMul_assoc]
  simp

def carMajoranaInt (r : Role) (bra ket : ArchiveFockState) : ℤ :=
  carAnnihilateInt r bra ket + carCreateInt r bra ket

def carSkewInt (r : Role) (bra ket : ArchiveFockState) : ℤ :=
  carAnnihilateInt r bra ket - carCreateInt r bra ket

def fockParityInt (bra ket : ArchiveFockState) : ℤ :=
  if bra = ket then
    if fockOccupationCount bra % 2 = 0 then 1 else -1
  else 0

def dressedSkewInt (r : Role) : ArchiveFockState → ArchiveFockState → ℤ :=
  fun bra ket => fockMatMul fockParityInt (carSkewInt r) bra ket

theorem carMajoranaInt_eq_fockGamma (r : Role) (bra ket : ArchiveFockState) :
    (carMajoranaInt r bra ket : ℝ) = fockGamma r bra ket := by
  simp [carMajoranaInt, fockGamma, carAnnihilate_eq_intCast, carCreate_eq_intCast]

theorem dressedSkew_commutes_majorana :
    ∀ r s : Role, ∀ bra ket : ArchiveFockState,
      fockComm (dressedSkewInt r) (carMajoranaInt s) bra ket = 0 := by
  classical
  native_decide

theorem carAnnihilateInt_flip_ne_zero :
    ∀ r : Role, ∀ s : ArchiveFockState, s r = true →
      carAnnihilateInt r (flipRole r s) s ≠ 0 := by
  classical
  native_decide

def eraseRole (r : Role) (s : ArchiveFockState) : ArchiveFockState :=
  if s r then flipRole r s else s

theorem eraseRole_chain_vacuum (s : ArchiveFockState) :
    eraseRole D0.D (eraseRole D0.C (eraseRole D0.B (eraseRole D0.A s))) =
      fockVacuumState := by
  classical
  revert s
  native_decide

/-- The full creation/annihilation family has scalar commutant. -/
theorem fullCAR_commutant_scalar
    (M : ArchiveFockState → ArchiveFockState → ℤ)
    (hc : ∀ r bra ket, fockComm M (carAnnihilateInt r) bra ket = 0)
    (hd : ∀ r bra ket, fockComm M (carCreateInt r) bra ket = 0) :
    FockScalar M := by
  classical
  have hN : ∀ r bra ket, fockComm M (fockNumberInt r) bra ket = 0 := by
    intro r bra ket
    simpa [fockNumberInt] using fockComm_of_factors M (carCreateInt r) (carAnnihilateInt r)
      (hd r) (hc r) bra ket
  have hdiag : ∀ {bra ket}, bra ≠ ket → M bra ket = 0 :=
    fun hneq => fock_comm_number_forces_diagonal M hN hneq
  have hflip : ∀ r s, s r = true → M (flipRole r s) (flipRole r s) = M s s := by
    intro r s hs
    have hcom := hc r (flipRole r s) s
    unfold fockComm at hcom
    have hMc : fockMatMul M (carAnnihilateInt r) (flipRole r s) s =
        M (flipRole r s) (flipRole r s) * carAnnihilateInt r (flipRole r s) s := by
      simp only [fockMatMul]
      rw [Finset.sum_eq_single (flipRole r s)]
      · intro mid _ hmid
        simp [hdiag (Ne.symm hmid)]
      · intro h
        exact (h (Finset.mem_univ _)).elim
    have hcM : fockMatMul (carAnnihilateInt r) M (flipRole r s) s =
        carAnnihilateInt r (flipRole r s) s * M s s := by
      simp only [fockMatMul]
      rw [Finset.sum_eq_single s]
      · intro mid _ hmid
        simp [hdiag hmid]
      · intro h
        exact (h (Finset.mem_univ _)).elim
    rw [hMc, hcM] at hcom
    have : (M (flipRole r s) (flipRole r s) - M s s) *
        carAnnihilateInt r (flipRole r s) s = 0 := by
      linear_combination hcom
    exact eq_of_sub_eq_zero
      ((mul_eq_zero.mp this).resolve_right (carAnnihilateInt_flip_ne_zero r s hs))
  have herase : ∀ r s, M (eraseRole r s) (eraseRole r s) = M s s := by
    intro r s
    by_cases hs : s r = true
    · simp [eraseRole, hs, hflip r s hs]
    · simp [eraseRole, hs]
  refine ⟨M fockVacuumState fockVacuumState, ?_⟩
  intro bra ket
  by_cases hbk : bra = ket
  · subst hbk
    have hA := herase D0.A bra
    have hB := herase D0.B (eraseRole D0.A bra)
    have hC := herase D0.C (eraseRole D0.B (eraseRole D0.A bra))
    have hD := herase D0.D (eraseRole D0.C (eraseRole D0.B (eraseRole D0.A bra)))
    rw [eraseRole_chain_vacuum] at hD
    simp [fockIdentityInt, hA, hB, hC, hD]
  · simp [fockIdentityInt, hbk, hdiag hbk]

end D0.Geometry
