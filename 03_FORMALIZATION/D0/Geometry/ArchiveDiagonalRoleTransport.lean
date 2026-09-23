import Mathlib.Tactic
import D0.Geometry.ArchiveHodgeCARDiracSquare
import D0.Geometry.ArchiveRolePermutationAction
import D0.Geometry.RoleFockPermutation

/-!
# Diagonal Role transport on archive cochains

`diagonalRoleTransport σ` permutes site coordinates and applies the owned
signed Fock transport at the same time. The pure Fock action, which leaves
the site fixed, is not a symmetry of `D_H`.
-/

namespace D0.Geometry

open D0
open RoleFockPermutation
open scoped BigOperators

noncomputable section

variable {N : ℕ}

def diagonalRoleTransport (σ : Equiv.Perm Role) (ψ : ArchiveCochain N) :
    ArchiveCochain N :=
  fun p => ∑ ket : ArchiveFockState,
    (signedTransport σ p.2 ket : ℝ) * ψ (permuteRoleSite σ.symm p.1, ket)

def fockOnlyRoleTransport (σ : Equiv.Perm Role) (ψ : ArchiveCochain N) :
    ArchiveCochain N :=
  fun p => ∑ ket : ArchiveFockState,
    (signedTransport σ p.2 ket : ℝ) * ψ (p.1, ket)

theorem diagonalRoleTransport_add (σ : Equiv.Perm Role) (ψ φ : ArchiveCochain N) :
    diagonalRoleTransport σ (ψ + φ) =
      diagonalRoleTransport σ ψ + diagonalRoleTransport σ φ := by
  funext p
  simp only [diagonalRoleTransport, Pi.add_apply, mul_add, Finset.sum_add_distrib]

theorem diagonalRoleTransport_smul (σ : Equiv.Perm Role) (c : ℝ) (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (c • ψ) = c • diagonalRoleTransport σ ψ := by
  funext p
  simp only [diagonalRoleTransport, Pi.smul_apply, mul_left_comm, Finset.mul_sum, smul_eq_mul]

theorem fock_signed_create_commute (σ : Equiv.Perm Role) (r : Role)
    (bra ket : ArchiveFockState) :
    fockMatMul (signedTransport σ) (carCreateInt r) bra ket =
      fockMatMul (carCreateInt (σ r)) (signedTransport σ) bra ket := by
  classical
  have hfun : (fun b k => conjTransport σ (carCreateInt r) b k) = carCreateInt (σ r) := by
    ext b k
    exact perm_conj_creation σ r b k
  have hassoc :=
    fockMatMul_assoc (fun b k => fockMatMul (signedTransport σ) (carCreateInt r) b k)
      (signedTransport σ.symm) (signedTransport σ) bra ket
  have hinv := signedTransport_inv_left σ
  calc
    fockMatMul (signedTransport σ) (carCreateInt r) bra ket
        = fockMatMul (fun b k => fockMatMul (signedTransport σ) (carCreateInt r) b k)
            fockIdentityInt bra ket := by
          rw [fockIdentityInt_mul_right]
    _ = fockMatMul (fun b k => fockMatMul (signedTransport σ) (carCreateInt r) b k)
          (fun b k => fockMatMul (signedTransport σ.symm) (signedTransport σ) b k) bra ket := by
          congr 1
          ext b k
          exact (hinv b k).symm
    _ = fockMatMul (fun b k => conjTransport σ (carCreateInt r) b k)
          (signedTransport σ) bra ket := by
          simpa [conjTransport] using hassoc.symm
    _ = fockMatMul (carCreateInt (σ r)) (signedTransport σ) bra ket := by
          rw [hfun]

theorem fock_signed_annihilate_commute (σ : Equiv.Perm Role) (r : Role)
    (bra ket : ArchiveFockState) :
    fockMatMul (signedTransport σ) (carAnnihilateInt r) bra ket =
      fockMatMul (carAnnihilateInt (σ r)) (signedTransport σ) bra ket := by
  classical
  have hfun : (fun b k => conjTransport σ (carAnnihilateInt r) b k) =
      carAnnihilateInt (σ r) := by
    ext b k
    exact perm_conj_annihilation σ r b k
  have hassoc :=
    fockMatMul_assoc (fun b k => fockMatMul (signedTransport σ) (carAnnihilateInt r) b k)
      (signedTransport σ.symm) (signedTransport σ) bra ket
  calc
    fockMatMul (signedTransport σ) (carAnnihilateInt r) bra ket
        = fockMatMul (fun b k => fockMatMul (signedTransport σ) (carAnnihilateInt r) b k)
            fockIdentityInt bra ket := by
          rw [fockIdentityInt_mul_right]
    _ = fockMatMul (fun b k => fockMatMul (signedTransport σ) (carAnnihilateInt r) b k)
          (fun b k => fockMatMul (signedTransport σ.symm) (signedTransport σ) b k) bra ket := by
          congr 1
          ext b k
          exact (signedTransport_inv_left σ b k).symm
    _ = fockMatMul (fun b k => conjTransport σ (carAnnihilateInt r) b k)
          (signedTransport σ) bra ket := by
          simpa [conjTransport] using hassoc.symm
    _ = fockMatMul (carAnnihilateInt (σ r)) (signedTransport σ) bra ket := by
          rw [hfun]

theorem real_signed_create_commute (σ : Equiv.Perm Role) (r : Role)
    (bra ket : ArchiveFockState) :
    (∑ mid, (signedTransport σ bra mid : ℝ) * carCreate r mid ket) =
      ∑ mid, carCreate (σ r) bra mid * (signedTransport σ mid ket : ℝ) := by
  have h := congrArg (fun z : ℤ => (z : ℝ)) (fock_signed_create_commute σ r bra ket)
  simpa [fockMatMul, carCreate_eq_intCast, Int.cast_sum, Int.cast_mul] using h

theorem real_signed_annihilate_commute (σ : Equiv.Perm Role) (r : Role)
    (bra ket : ArchiveFockState) :
    (∑ mid, (signedTransport σ bra mid : ℝ) * carAnnihilate r mid ket) =
      ∑ mid, carAnnihilate (σ r) bra mid * (signedTransport σ mid ket : ℝ) := by
  have h := congrArg (fun z : ℤ => (z : ℝ)) (fock_signed_annihilate_commute σ r bra ket)
  simpa [fockMatMul, carAnnihilate_eq_intCast, Int.cast_sum, Int.cast_mul] using h

theorem diagonalRoleTransport_one (ψ : ArchiveCochain N) :
    diagonalRoleTransport (1 : Equiv.Perm Role) ψ = ψ := by
  classical
  funext p
  simp only [diagonalRoleTransport, Equiv.Perm.one_symm]
  rw [permuteRoleSite_one]
  rw [Finset.sum_eq_single p.2]
  · simp [signedTransport_one, fockIdentityInt]
  · intro ket _ hket
    rw [signedTransport_one, fockIdentityInt, if_neg hket.symm]
    simp
  · intro h
    exact (h (Finset.mem_univ _)).elim

theorem diagonalRoleTransport_mul (σ τ : Equiv.Perm Role) (ψ : ArchiveCochain N) :
    diagonalRoleTransport (σ * τ) ψ =
      diagonalRoleTransport σ (diagonalRoleTransport τ ψ) := by
  classical
  funext p
  simp only [diagonalRoleTransport]
  have hsite :
      permuteRoleSite (σ * τ).symm p.1 =
        permuteRoleSite τ.symm (permuteRoleSite σ.symm p.1) := by
    simpa using (permuteRoleSite_mul τ.symm σ.symm p.1).symm
  simp only [hsite]
  calc
    (∑ ket, (signedTransport (σ * τ) p.2 ket : ℝ) *
        ψ (permuteRoleSite τ.symm (permuteRoleSite σ.symm p.1), ket)) =
      ∑ ket, (∑ mid, (signedTransport σ p.2 mid : ℝ) *
          (signedTransport τ mid ket : ℝ)) *
        ψ (permuteRoleSite τ.symm (permuteRoleSite σ.symm p.1), ket) := by
          refine Finset.sum_congr rfl fun ket _ => ?_
          have hmul := congrArg (fun z : ℤ => (z : ℝ))
            (signedTransport_mul σ τ p.2 ket)
          simp only [fockMatMul, Int.cast_sum, Int.cast_mul] at hmul
          rw [hmul]
    _ = ∑ mid, (signedTransport σ p.2 mid : ℝ) *
          (∑ ket, (signedTransport τ mid ket : ℝ) *
            ψ (permuteRoleSite τ.symm (permuteRoleSite σ.symm p.1), ket)) := by
          simp_rw [Finset.sum_mul]
          rw [Finset.sum_comm]
          refine Finset.sum_congr rfl fun mid _ => ?_
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl fun ket _ => ?_
          ring
    _ = ∑ mid, (signedTransport σ p.2 mid : ℝ) *
          diagonalRoleTransport τ ψ (permuteRoleSite σ.symm p.1, mid) := by
          rfl

theorem diagonalRoleTransport_inv (σ : Equiv.Perm Role) (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ.symm (diagonalRoleTransport σ ψ) = ψ := by
  rw [← diagonalRoleTransport_mul, perm_symm_mul, diagonalRoleTransport_one]

theorem diagonalRoleTransport_right_inv (σ : Equiv.Perm Role) (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (diagonalRoleTransport σ.symm ψ) = ψ := by
  rw [← diagonalRoleTransport_mul, perm_mul_symm, diagonalRoleTransport_one]

noncomputable def diagonalRoleLinearEquiv (σ : Equiv.Perm Role) :
    ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N where
  toFun := diagonalRoleTransport σ
  invFun := diagonalRoleTransport σ.symm
  left_inv := diagonalRoleTransport_inv σ
  right_inv := diagonalRoleTransport_right_inv σ
  map_add' := diagonalRoleTransport_add σ
  map_smul' := diagonalRoleTransport_smul σ

theorem signedTransport_transpose (σ : Equiv.Perm Role)
    (bra ket : ArchiveFockState) :
    signedTransport σ.symm ket bra = signedTransport σ bra ket := by
  classical
  have hiff : ket = transportState σ.symm bra ↔ bra = transportState σ ket := by
    constructor
    · intro h
      rw [h]
      exact (transportState_leftInverse σ.symm bra).symm
    · intro h
      rw [h]
      exact (transportState_leftInverse σ ket).symm
  unfold signedTransport
  by_cases hket : ket = transportState σ.symm bra
  · have hbra : bra = transportState σ ket := hiff.mp hket
    rw [if_pos hket, if_pos hbra]
    have hsign := fermionSign_symm_transport σ (transportState σ.symm bra)
    rw [transport_state_inverse_apply σ bra] at hsign
    rw [hket]
    exact hsign
  · have hbra : bra ≠ transportState σ ket := fun hbra => hket (hiff.mpr hbra)
    rw [if_neg hket, if_neg hbra]

theorem diagonalRoleTransport_pairing (σ : Equiv.Perm Role)
    (ψ φ : ArchiveCochain N) :
    cochainPairing N (diagonalRoleTransport σ ψ) (diagonalRoleTransport σ φ) =
      cochainPairing N ψ φ := by
  classical
  have horth : ∀ k m : ArchiveFockState,
      (∑ s : ArchiveFockState, (signedTransport σ s k : ℝ) * (signedTransport σ s m : ℝ)) =
        if k = m then (1 : ℝ) else 0 := by
    intro k m
    have hmul := congrArg (fun z : ℤ => (z : ℝ)) (signedTransport_inv_left σ k m)
    simp only [fockMatMul, Int.cast_sum, Int.cast_mul, signedTransport_transpose] at hmul
    simpa [fockIdentityInt] using hmul
  unfold cochainPairing diagonalRoleTransport
  calc
    (∑ x, ∑ s,
        (∑ k, (signedTransport σ s k : ℝ) * ψ (permuteRoleSite σ.symm x, k)) *
        (∑ m, (signedTransport σ s m : ℝ) * φ (permuteRoleSite σ.symm x, m))) =
      ∑ x, ∑ s, ∑ k, ∑ m,
        (signedTransport σ s k : ℝ) * ψ (permuteRoleSite σ.symm x, k) *
          ((signedTransport σ s m : ℝ) * φ (permuteRoleSite σ.symm x, m)) := by
        refine Finset.sum_congr rfl fun x _ => ?_
        refine Finset.sum_congr rfl fun s _ => ?_
        rw [Finset.sum_mul]
        refine Finset.sum_congr rfl fun k _ => ?_
        rw [Finset.mul_sum]
    _ = ∑ x, ∑ k, ∑ m, ∑ s,
        (signedTransport σ s k : ℝ) * (signedTransport σ s m : ℝ) *
          ψ (permuteRoleSite σ.symm x, k) * φ (permuteRoleSite σ.symm x, m) := by
        refine Finset.sum_congr rfl fun x _ => ?_
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl fun k _ => ?_
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl fun m _ => ?_
        refine Finset.sum_congr rfl fun s _ => ?_
        ring
    _ = ∑ x, ∑ k, ∑ m,
        (∑ s, (signedTransport σ s k : ℝ) * (signedTransport σ s m : ℝ)) *
          (ψ (permuteRoleSite σ.symm x, k) * φ (permuteRoleSite σ.symm x, m)) := by
        refine Finset.sum_congr rfl fun x _ => ?_
        refine Finset.sum_congr rfl fun k _ => ?_
        refine Finset.sum_congr rfl fun m _ => ?_
        have hregroup :
            (∑ s, (signedTransport σ s k : ℝ) * (signedTransport σ s m : ℝ) *
                ψ (permuteRoleSite σ.symm x, k) * φ (permuteRoleSite σ.symm x, m)) =
              ∑ s, ((signedTransport σ s k : ℝ) * (signedTransport σ s m : ℝ)) *
                (ψ (permuteRoleSite σ.symm x, k) * φ (permuteRoleSite σ.symm x, m)) := by
          refine Finset.sum_congr rfl fun s _ => ?_
          ring
        rw [hregroup, ← Finset.sum_mul]
    _ = ∑ x, ∑ k,
        ψ (permuteRoleSite σ.symm x, k) * φ (permuteRoleSite σ.symm x, k) := by
        refine Finset.sum_congr rfl fun x _ => ?_
        refine Finset.sum_congr rfl fun k _ => ?_
        rw [Finset.sum_eq_single k]
        · rw [horth k k, if_pos rfl]
          ring
        · intro m _ hmk
          rw [horth k m, if_neg (Ne.symm hmk)]
          ring
        · intro hk
          exact (hk (Finset.mem_univ _)).elim
    _ = ∑ x, ∑ k, ψ (x, k) * φ (x, k) := by
        let e : ArchiveRolePhaseGroup N ≃ ArchiveRolePhaseGroup N :=
          { toFun := permuteRoleSite σ.symm
            invFun := permuteRoleSite σ
            left_inv := permuteRoleSite_right_inv σ
            right_inv := permuteRoleSite_inv σ }
        have hsite := e.sum_comp fun y => ∑ k, ψ (y, k) * φ (y, k)
        simpa [e] using hsite

theorem diagonalRoleTransport_isometry (σ : Equiv.Perm Role)
    (ψ φ : ArchiveCochain N) :
    cochainPairing N (diagonalRoleTransport σ ψ) (diagonalRoleTransport σ φ) =
      cochainPairing N ψ φ :=
  diagonalRoleTransport_pairing σ ψ φ

theorem diagonalRoleTransport_create (σ : Equiv.Perm Role) (r : Role)
    (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (createAction N r ψ) =
      createAction N (σ r) (diagonalRoleTransport σ ψ) := by
  classical
  funext p
  unfold diagonalRoleTransport createAction
  calc
    (∑ ket, (signedTransport σ p.2 ket : ℝ) *
        (∑ mid, carCreate r ket mid * ψ (permuteRoleSite σ.symm p.1, mid))) =
      ∑ ket, ∑ mid,
        (signedTransport σ p.2 ket : ℝ) *
          (carCreate r ket mid * ψ (permuteRoleSite σ.symm p.1, mid)) := by
        refine Finset.sum_congr rfl fun ket _ => ?_
        rw [Finset.mul_sum]
    _ = ∑ mid, ∑ ket,
        (signedTransport σ p.2 ket : ℝ) *
          (carCreate r ket mid * ψ (permuteRoleSite σ.symm p.1, mid)) := by
        rw [Finset.sum_comm]
    _ = ∑ mid,
        (∑ ket, (signedTransport σ p.2 ket : ℝ) * carCreate r ket mid) *
          ψ (permuteRoleSite σ.symm p.1, mid) := by
        refine Finset.sum_congr rfl fun mid _ => ?_
        rw [Finset.sum_mul]
        refine Finset.sum_congr rfl fun ket _ => ?_
        ring
    _ = ∑ mid,
        (∑ ket, carCreate (σ r) p.2 ket * (signedTransport σ ket mid : ℝ)) *
          ψ (permuteRoleSite σ.symm p.1, mid) := by
        refine Finset.sum_congr rfl fun mid _ => ?_
        rw [real_signed_create_commute]
    _ = ∑ mid, ∑ ket,
        carCreate (σ r) p.2 ket * (signedTransport σ ket mid : ℝ) *
          ψ (permuteRoleSite σ.symm p.1, mid) := by
        refine Finset.sum_congr rfl fun mid _ => ?_
        rw [Finset.sum_mul]
    _ = ∑ ket, ∑ mid,
        carCreate (σ r) p.2 ket *
          ((signedTransport σ ket mid : ℝ) *
            ψ (permuteRoleSite σ.symm p.1, mid)) := by
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl fun ket _ => ?_
        refine Finset.sum_congr rfl fun mid _ => ?_
        ring
    _ = ∑ ket, carCreate (σ r) p.2 ket *
        (∑ mid, (signedTransport σ ket mid : ℝ) *
          ψ (permuteRoleSite σ.symm p.1, mid)) := by
        refine Finset.sum_congr rfl fun ket _ => ?_
        rw [← Finset.mul_sum]
    _ = createAction N (σ r) (diagonalRoleTransport σ ψ) p := by
        simp only [createAction, diagonalRoleTransport]

theorem diagonalRoleTransport_annihilate (σ : Equiv.Perm Role) (r : Role)
    (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (annihilateAction N r ψ) =
      annihilateAction N (σ r) (diagonalRoleTransport σ ψ) := by
  classical
  funext p
  unfold diagonalRoleTransport annihilateAction
  calc
    (∑ ket, (signedTransport σ p.2 ket : ℝ) *
        (∑ mid, carAnnihilate r ket mid * ψ (permuteRoleSite σ.symm p.1, mid))) =
      ∑ ket, ∑ mid,
        (signedTransport σ p.2 ket : ℝ) *
          (carAnnihilate r ket mid * ψ (permuteRoleSite σ.symm p.1, mid)) := by
        refine Finset.sum_congr rfl fun ket _ => ?_
        rw [Finset.mul_sum]
    _ = ∑ mid, ∑ ket,
        (signedTransport σ p.2 ket : ℝ) *
          (carAnnihilate r ket mid * ψ (permuteRoleSite σ.symm p.1, mid)) := by
        rw [Finset.sum_comm]
    _ = ∑ mid,
        (∑ ket, (signedTransport σ p.2 ket : ℝ) * carAnnihilate r ket mid) *
          ψ (permuteRoleSite σ.symm p.1, mid) := by
        refine Finset.sum_congr rfl fun mid _ => ?_
        rw [Finset.sum_mul]
        refine Finset.sum_congr rfl fun ket _ => ?_
        ring
    _ = ∑ mid,
        (∑ ket, carAnnihilate (σ r) p.2 ket * (signedTransport σ ket mid : ℝ)) *
          ψ (permuteRoleSite σ.symm p.1, mid) := by
        refine Finset.sum_congr rfl fun mid _ => ?_
        rw [real_signed_annihilate_commute]
    _ = ∑ mid, ∑ ket,
        carAnnihilate (σ r) p.2 ket * (signedTransport σ ket mid : ℝ) *
          ψ (permuteRoleSite σ.symm p.1, mid) := by
        refine Finset.sum_congr rfl fun mid _ => ?_
        rw [Finset.sum_mul]
    _ = ∑ ket, ∑ mid,
        carAnnihilate (σ r) p.2 ket *
          ((signedTransport σ ket mid : ℝ) *
            ψ (permuteRoleSite σ.symm p.1, mid)) := by
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl fun ket _ => ?_
        refine Finset.sum_congr rfl fun mid _ => ?_
        ring
    _ = ∑ ket, carAnnihilate (σ r) p.2 ket *
        (∑ mid, (signedTransport σ ket mid : ℝ) *
          ψ (permuteRoleSite σ.symm p.1, mid)) := by
        refine Finset.sum_congr rfl fun ket _ => ?_
        rw [← Finset.mul_sum]
    _ = annihilateAction N (σ r) (diagonalRoleTransport σ ψ) p := by
        simp only [annihilateAction, diagonalRoleTransport]

theorem diagonalRoleTransport_forwardSite (σ : Equiv.Perm Role) (r : Role)
    (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (forwardSite N r ψ) =
      forwardSite N (σ r) (diagonalRoleTransport σ ψ) := by
  funext p
  simp only [diagonalRoleTransport, forwardSite, forwardDifference_apply]
  have hplus := permuteRoleSite_translatePlus σ.symm (σ r) p.1
  simp only [Equiv.symm_apply_apply] at hplus
  simp only [hplus, mul_sub, Finset.sum_sub_distrib, Finset.mul_sum, mul_left_comm]

theorem diagonalRoleTransport_backwardSite (σ : Equiv.Perm Role) (r : Role)
    (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (backwardSite N r ψ) =
      backwardSite N (σ r) (diagonalRoleTransport σ ψ) := by
  funext p
  simp only [diagonalRoleTransport, backwardSite, backwardDifference_apply]
  have hminus := permuteRoleSite_translateMinus σ.symm (σ r) p.1
  simp only [Equiv.symm_apply_apply] at hminus
  simp only [hminus, mul_sub, Finset.sum_sub_distrib, Finset.mul_sum, mul_left_comm]

theorem diagonalRoleTransport_forwardDifference (σ : Equiv.Perm Role) (r : Role)
    (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (forwardSite N r ψ) =
      forwardSite N (σ r) (diagonalRoleTransport σ ψ) :=
  diagonalRoleTransport_forwardSite σ r ψ

theorem diagonalRoleTransport_backwardDifference (σ : Equiv.Perm Role) (r : Role)
    (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (backwardSite N r ψ) =
      backwardSite N (σ r) (diagonalRoleTransport σ ψ) :=
  diagonalRoleTransport_backwardSite σ r ψ

theorem diagonalRoleTransport_forwardCreate (σ : Equiv.Perm Role) (r : Role)
    (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (forwardCreateDirection N r ψ) =
      forwardCreateDirection N (σ r) (diagonalRoleTransport σ ψ) := by
  rw [forwardCreateDirection_eq_createAction_forwardSite]
  rw [diagonalRoleTransport_create]
  rw [diagonalRoleTransport_forwardSite]
  rw [← forwardCreateDirection_eq_createAction_forwardSite]

theorem diagonalRoleTransport_dForward (σ : Equiv.Perm Role) (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (dForward N ψ) = dForward N (diagonalRoleTransport σ ψ) := by
  classical
  funext p
  unfold dForward
  simp only [diagonalRoleTransport]
  calc
    (∑ ket, (signedTransport σ p.2 ket : ℝ) *
        (∑ r, forwardCreateDirection N r ψ (permuteRoleSite σ.symm p.1, ket))) =
      ∑ ket, ∑ r, (signedTransport σ p.2 ket : ℝ) *
        forwardCreateDirection N r ψ (permuteRoleSite σ.symm p.1, ket) := by
        refine Finset.sum_congr rfl fun ket _ => ?_
        rw [Finset.mul_sum]
    _ = ∑ r, ∑ ket, (signedTransport σ p.2 ket : ℝ) *
        forwardCreateDirection N r ψ (permuteRoleSite σ.symm p.1, ket) := by
        rw [Finset.sum_comm]
    _ = ∑ r, diagonalRoleTransport σ (forwardCreateDirection N r ψ) p := by
        rfl
    _ = ∑ r, forwardCreateDirection N (σ r) (diagonalRoleTransport σ ψ) p := by
        refine Finset.sum_congr rfl fun r _ => ?_
        exact congrFun (diagonalRoleTransport_forwardCreate σ r ψ) p
    _ = ∑ r, forwardCreateDirection N r (diagonalRoleTransport σ ψ) p :=
        Equiv.sum_comp σ fun r =>
          forwardCreateDirection N r (diagonalRoleTransport σ ψ) p

theorem diagonalRoleTransport_backwardAnnihilate (σ : Equiv.Perm Role) (r : Role)
    (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (backwardAnnihilateDirection N r ψ) =
      backwardAnnihilateDirection N (σ r) (diagonalRoleTransport σ ψ) := by
  simp only [backwardAnnihilateDirection, diagonalRoleTransport_backwardSite,
    diagonalRoleTransport_annihilate]

theorem diagonalRoleTransport_neg (σ : Equiv.Perm Role) (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (-ψ) = -diagonalRoleTransport σ ψ := by
  funext p
  simp only [diagonalRoleTransport, Pi.neg_apply, mul_neg, Finset.sum_neg_distrib]

theorem diagonalRoleTransport_hodgeCodifferential (σ : Equiv.Perm Role)
    (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (hodgeCodifferential N ψ) =
      hodgeCodifferential N (diagonalRoleTransport σ ψ) := by
  classical
  funext p
  unfold hodgeCodifferential
  simp only [diagonalRoleTransport]
  calc
    (∑ ket, (signedTransport σ p.2 ket : ℝ) *
        (∑ r, -backwardAnnihilateDirection N r ψ (permuteRoleSite σ.symm p.1, ket))) =
      ∑ ket, ∑ r, (signedTransport σ p.2 ket : ℝ) *
        -backwardAnnihilateDirection N r ψ (permuteRoleSite σ.symm p.1, ket) := by
        refine Finset.sum_congr rfl fun ket _ => ?_
        rw [Finset.mul_sum]
    _ = ∑ r, ∑ ket, (signedTransport σ p.2 ket : ℝ) *
        -backwardAnnihilateDirection N r ψ (permuteRoleSite σ.symm p.1, ket) := by
        rw [Finset.sum_comm]
    _ = ∑ r, diagonalRoleTransport σ (-backwardAnnihilateDirection N r ψ) p := by
        refine Finset.sum_congr rfl fun r _ => ?_
        simp only [diagonalRoleTransport, Pi.neg_apply]
    _ = ∑ r, -backwardAnnihilateDirection N (σ r) (diagonalRoleTransport σ ψ) p := by
        refine Finset.sum_congr rfl fun r _ => ?_
        rw [diagonalRoleTransport_neg, diagonalRoleTransport_backwardAnnihilate]
        rfl
    _ = ∑ r, -backwardAnnihilateDirection N r (diagonalRoleTransport σ ψ) p :=
        Equiv.sum_comp σ fun r =>
          -backwardAnnihilateDirection N r (diagonalRoleTransport σ ψ) p

theorem diagonalRoleTransport_commutes_hodgeCarDirac (σ : Equiv.Perm Role)
    (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (hodgeCarDirac N ψ) =
      hodgeCarDirac N (diagonalRoleTransport σ ψ) := by
  simp only [hodgeCarDirac, diagonalRoleTransport_add, diagonalRoleTransport_dForward,
    diagonalRoleTransport_hodgeCodifferential]

theorem diagonalRoleTransport_commutes_hodgeSquare (σ : Equiv.Perm Role)
    (ψ : ArchiveCochain N) :
    diagonalRoleTransport σ (hodgeCarDirac N (hodgeCarDirac N ψ)) =
      hodgeCarDirac N (hodgeCarDirac N (diagonalRoleTransport σ ψ)) := by
  rw [diagonalRoleTransport_commutes_hodgeCarDirac,
    diagonalRoleTransport_commutes_hodgeCarDirac]

/-! ## Fock-only transport is not a symmetry of `D_H` -/

def bZeroIndicator : ArchiveRolePhaseGroup 1 → ℝ :=
  fun x => if x B = 0 then 1 else 0

def bVacuumCochain : ArchiveCochain 1 :=
  fun p => if p.2 = fockVacuumState then bZeroIndicator p.1 else 0

def witnessOrigin : ArchiveRolePhaseGroup 1 := fun _ => 0

private lemma transportState_vacuum (σ : Equiv.Perm Role) :
    transportState σ fockVacuumState = fockVacuumState := by
  funext r
  rfl

private lemma fermionSign_vacuum (σ : Equiv.Perm Role) :
    fermionSign σ fockVacuumState = 1 := by
  unfold fermionSign occupiedInversionCount fockVacuumState
  simp

private lemma fermionSign_singleton (σ : Equiv.Perm Role) (r : Role) :
    fermionSign σ (fockSingletonState r) = 1 := by
  unfold fermionSign
  have h0 : occupiedInversionCount σ (fockSingletonState r) = 0 := by
    unfold occupiedInversionCount
    rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
    intro p _ hp
    have h1 : p.1 = r := by
      simpa [fockSingletonState] using hp.1
    have h2 : p.2 = r := by
      simpa [fockSingletonState] using hp.2.1
    rw [h1, h2] at hp
    exact lt_irrefl _ hp.2.2.1
  simp [h0]

private lemma fockSingletonState_injective : Function.Injective fockSingletonState := by
  intro a b h
  have htrue : fockSingletonState a a = true := by simp [fockSingletonState]
  have := congrFun h a
  rw [htrue] at this
  simpa [fockSingletonState] using this

private lemma transportState_singleton (σ : Equiv.Perm Role) (r : Role) :
    transportState σ (fockSingletonState r) = fockSingletonState (σ r) := by
  funext s
  simp only [transportState, fockSingletonState]
  by_cases h : σ.symm s = r
  · have hs : s = σ r := by
      simpa using congrArg σ h
    simp [hs]
  · have hs : s ≠ σ r := by
      intro hs
      apply h
      rw [hs]
      simp
    simp [hs]
    exact h

private lemma signedTransport_on_vacuum (σ : Equiv.Perm Role) (bra : ArchiveFockState) :
    signedTransport σ bra fockVacuumState =
      if bra = fockVacuumState then 1 else 0 := by
  unfold signedTransport
  rw [transportState_vacuum, fermionSign_vacuum]

private lemma carCreate_from_vacuum (r : Role) (bra : ArchiveFockState) :
    carCreate r bra fockVacuumState =
      if bra = fockSingletonState r then (1 : ℝ) else 0 := by
  classical
  by_cases hbra : bra = fockSingletonState r
  · subst hbra
    rw [carCreate_singleton_vacuum, roleDelta, if_pos rfl, if_pos rfl]
  · unfold carCreate carAnnihilate
    rw [if_neg, if_neg hbra]
    intro hcond
    apply hbra
    funext s
    rcases hcond with ⟨hket, _, hrest⟩
    by_cases hs : s = r
    · subst hs
      simp [fockSingletonState, hket]
    · have hsval := hrest s hs
      simp [fockVacuumState] at hsval
      simp [fockSingletonState, hs, hsval]

private lemma forwardDifference_zero_fun (r : Role) (x : ArchiveRolePhaseGroup 1) :
    forwardDifference 1 r (fun _ => (0 : ℝ)) x = 0 := by
  simp [forwardDifference_apply]

private lemma forward_bZero_origin (r : Role) :
    forwardDifference 1 r bZeroIndicator witnessOrigin =
      if r = B then -3 else 0 := by
  have hscale : forwardDifferenceScale 1 = 3 := by
    simp [forwardDifferenceScale, archiveFibers]
  rw [forwardDifference_apply, hscale]
  have horigin : bZeroIndicator witnessOrigin = 1 := by
    simp [bZeroIndicator, witnessOrigin]
  rw [horigin]
  by_cases hr : r = B
  · subst hr
    have hcoord : roleTranslatePlus 1 B witnessOrigin B = 1 := by
      simp [roleTranslatePlus_apply, witnessOrigin, roleStep]
    have hval : bZeroIndicator (roleTranslatePlus 1 B witnessOrigin) = 0 := by
      simp only [bZeroIndicator]
      rw [hcoord]
      have hne : (1 : ZMod (archiveFibers 1)) ≠ 0 := by
        rw [show archiveFibers 1 = 3 by simp [archiveFibers]]
        decide
      rw [if_neg hne]
    rw [hval, if_pos rfl]
    norm_num
  · have hcoord : roleTranslatePlus 1 r witnessOrigin B = 0 := by
      simp [roleTranslatePlus_apply, witnessOrigin, roleStep, Ne.symm hr]
    have hval : bZeroIndicator (roleTranslatePlus 1 r witnessOrigin) = 1 := by
      simp [bZeroIndicator, hcoord]
    rw [hval, if_neg hr]
    norm_num

private lemma bVacuum_slice (ket : ArchiveFockState) :
    (fun y => bVacuumCochain (y, ket)) =
      if ket = fockVacuumState then bZeroIndicator else fun _ => 0 := by
  funext y
  by_cases h : ket = fockVacuumState
  · simp [bVacuumCochain, h]
  · simp [bVacuumCochain, h]

private lemma hodgeCodifferential_bVacuum : hodgeCodifferential 1 bVacuumCochain = 0 := by
  classical
  funext p
  unfold hodgeCodifferential backwardAnnihilateDirection annihilateAction
  apply Finset.sum_eq_zero
  intro r _
  rw [neg_eq_zero]
  apply Finset.sum_eq_zero
  intro ket _
  by_cases hket : ket = fockVacuumState
  · subst hket
    have hann : carAnnihilate r p.2 fockVacuumState = 0 := by
      simp [carAnnihilate, fockVacuumState]
    rw [hann, zero_mul]
  · have hfun := bVacuum_slice ket
    rw [if_neg hket] at hfun
    have hzero : backwardSite 1 r bVacuumCochain (p.1, ket) = 0 := by
      simp only [backwardSite, backwardDifference_apply, hfun, sub_self, mul_zero]
    rw [hzero, mul_zero]

private lemma dForward_bVacuum_origin (ket : ArchiveFockState) :
    dForward 1 bVacuumCochain (witnessOrigin, ket) =
      if ket = fockSingletonState B then -3 else 0 := by
  classical
  unfold dForward
  by_cases hket : ket = fockSingletonState B
  · subst hket
    rw [if_pos rfl]
    rw [Finset.sum_eq_single B]
    · unfold forwardCreateDirection
      rw [Finset.sum_eq_single fockVacuumState]
      · rw [carCreate_from_vacuum, if_pos rfl]
        have hslice := bVacuum_slice fockVacuumState
        rw [if_pos rfl] at hslice
        rw [hslice, forward_bZero_origin, if_pos rfl]
        norm_num
      · intro mid _ hmid
        have hslice := bVacuum_slice mid
        rw [if_neg hmid] at hslice
        rw [hslice, forwardDifference_zero_fun, mul_zero]
      · intro hmem
        exact (hmem (Finset.mem_univ _)).elim
    · intro r _ hr
      unfold forwardCreateDirection
      apply Finset.sum_eq_zero
      intro mid _
      by_cases hmid : mid = fockVacuumState
      · subst hmid
        have hne : fockSingletonState B ≠ fockSingletonState r := by
          intro hs
          exact hr (fockSingletonState_injective hs).symm
        rw [carCreate_from_vacuum, if_neg hne, zero_mul]
      · have hslice := bVacuum_slice mid
        rw [if_neg hmid] at hslice
        rw [hslice, forwardDifference_zero_fun, mul_zero]
    · intro hmem
      exact (hmem (Finset.mem_univ _)).elim
  · rw [if_neg hket]
    apply Finset.sum_eq_zero
    intro r _
    unfold forwardCreateDirection
    apply Finset.sum_eq_zero
    intro mid _
    by_cases hmid : mid = fockVacuumState
    · subst hmid
      by_cases hsing : ket = fockSingletonState r
      · have hr : r ≠ B := by
          intro hrB
          apply hket
          rw [hsing, hrB]
        have hslice := bVacuum_slice fockVacuumState
        rw [if_pos rfl] at hslice
        rw [hslice, forward_bZero_origin, if_neg hr, mul_zero]
      · rw [carCreate_from_vacuum, if_neg hsing, zero_mul]
    · have hslice := bVacuum_slice mid
      rw [if_neg hmid] at hslice
      rw [hslice, forwardDifference_zero_fun, mul_zero]

private lemma fockOnly_fixes_bVacuum :
    fockOnlyRoleTransport swapBC bVacuumCochain = bVacuumCochain := by
  classical
  funext p
  unfold fockOnlyRoleTransport
  rw [Finset.sum_eq_single fockVacuumState]
  · rw [signedTransport_on_vacuum]
    by_cases hbra : p.2 = fockVacuumState
    · simp [bVacuumCochain, hbra]
    · simp [bVacuumCochain, hbra]
  · intro ket _ hket
    simp [bVacuumCochain, hket]
  · intro hmem
    exact (hmem (Finset.mem_univ _)).elim

private lemma fockOnly_moves_singleton_B :
    fockOnlyRoleTransport swapBC (dForward 1 bVacuumCochain)
      (witnessOrigin, fockSingletonState C) = -3 := by
  classical
  unfold fockOnlyRoleTransport
  rw [Finset.sum_eq_single (fockSingletonState B)]
  · have htr : transportState swapBC (fockSingletonState B) = fockSingletonState C := by
      rw [transportState_singleton]
      simp [swapBC, Equiv.swap_apply_left]
    have hsign : signedTransport swapBC (fockSingletonState C) (fockSingletonState B) = 1 := by
      unfold signedTransport
      rw [htr, fermionSign_singleton, if_pos rfl]
    rw [hsign, dForward_bVacuum_origin, if_pos rfl]
    ring
  · intro ket _ hket
    rw [dForward_bVacuum_origin]
    have hne : ket ≠ fockSingletonState B := hket
    simp [hne]
  · intro hmem
    exact (hmem (Finset.mem_univ _)).elim

theorem fockDegree_vacuum : fockDegree fockVacuumState = 0 := by
  simp [fockDegree, fockVacuumState]

theorem bVacuumCochain_support_vacuum (p : ArchiveCochainBasis 1)
    (hp : bVacuumCochain p ≠ 0) : p.2 = fockVacuumState := by
  by_contra h
  apply hp
  simp [bVacuumCochain, h]

theorem hodgeCarDirac_bVacuum_at_singletonB :
    hodgeCarDirac 1 bVacuumCochain (witnessOrigin, fockSingletonState B) = -3 := by
  rw [hodgeCarDirac, hodgeCodifferential_bVacuum]
  simp only [Pi.add_apply, Pi.zero_apply, add_zero]
  rw [dForward_bVacuum_origin, if_pos rfl]

/-- Fock-only transport leaves the site fixed. It is not a symmetry of `D_H`. -/
theorem fockOnlyTransport_not_hodgeSymmetry :
    ∃ ψ : ArchiveCochain 1,
      fockOnlyRoleTransport swapBC (hodgeCarDirac 1 ψ) ≠
        hodgeCarDirac 1 (fockOnlyRoleTransport swapBC ψ) := by
  classical
  refine ⟨bVacuumCochain, ?_⟩
  intro h
  have hfix := fockOnly_fixes_bVacuum
  have hcod := hodgeCodifferential_bVacuum
  have hdirac : hodgeCarDirac 1 bVacuumCochain = dForward 1 bVacuumCochain := by
    simp [hodgeCarDirac, hcod]
  rw [hfix, hdirac] at h
  have hpt := congrFun h (witnessOrigin, fockSingletonState C)
  rw [fockOnly_moves_singleton_B, dForward_bVacuum_origin, if_neg] at hpt
  · norm_num at hpt
  · intro hs
    have := fockSingletonState_injective hs
    simp [B, C] at this

end

end D0.Geometry
