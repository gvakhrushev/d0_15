import Mathlib.Tactic
import D0.Geometry.ArchiveCARDirac
import D0.Geometry.ArchiveCubicalCartan
import D0.Geometry.ArchiveCubicalDifferential

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

/-!
# Hodge / difference CAR operator

This module owns the massless finite-difference operator

  d     = ∑_r c_r† ∇_r⁺
  d†    = -∑_r c_r ∇_r⁻
  D_H   = d + d†

on the cubical cochain carrier.  `D_H` is not `hoppingCarDirac` / `carDirac`.

This file owns the counting adjoint and fermionic parity of `D_H`.
The operator square is not proved here.  The scalar difference Laplacian and
the `L = 2` diagonal collision live in `ArchiveHodgeCARDiracSquare`.
No constitutive metric deformation is selected.
-/

/-- Backward difference on each fixed Fock component. -/
def backwardSite (N : ℕ) (r : Role) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => backwardDifference N r (fun x => ψ (x, p.2)) p.1

/-- Directional summand `c_r ∇_r⁻`. -/
def backwardAnnihilateDirection (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  annihilateAction N r (backwardSite N r ψ)

theorem backwardAnnihilateDirection_eq (N : ℕ) (r : Role) (ψ : ArchiveCochain N) :
    backwardAnnihilateDirection N r ψ =
      fun p =>
        ∑ ket : ArchiveFockState,
          carAnnihilate r p.2 ket *
            backwardDifference N r (fun x => ψ (x, ket)) p.1 := by
  funext p
  rfl

/-- Counting codifferential `d† = -∑_r c_r ∇_r⁻`. -/
def hodgeCodifferential (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ∑ r : Role, -backwardAnnihilateDirection N r ψ p

/-- Massless Hodge/difference CAR operator `D_H = d + d†`. -/
def hodgeCarDirac (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  dForward N ψ + hodgeCodifferential N ψ

/-- Oriented difference Laplacian `-∑_r ∇_r⁻ ∇_r⁺` on scalar fields. -/
def scalarDifferenceLaplacian (N : ℕ)
    (f : ArchiveRolePhaseGroup N → ℝ) : ArchiveRolePhaseGroup N → ℝ :=
  fun x => ∑ r : Role, -backwardDifference N r (forwardDifference N r f) x

/-- The same Laplacian acting separately on every Fock component. -/
def cochainDifferenceLaplacian (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => scalarDifferenceLaplacian N (fun x => ψ (x, p.2)) p.1

def cochainPairing (N : ℕ) (ψ φ : ArchiveCochain N) : ℝ :=
  ∑ x, ∑ s, ψ (x, s) * φ (x, s)

def parityCochain (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => fockParitySign p.2 * ψ p

/-! ## Adjoint -/

theorem createAction_adjoint (N : ℕ) (r : Role) (ψ φ : ArchiveCochain N) :
    cochainPairing N (createAction N r ψ) φ =
      cochainPairing N ψ (annihilateAction N r φ) := by
  classical
  unfold cochainPairing createAction annihilateAction
  simp_rw [Finset.sum_mul]
  have hswap :
      (∑ x, ∑ bra, ∑ ket,
          carCreate r bra ket * ψ (x, ket) * φ (x, bra)) =
        ∑ x, ∑ ket, ∑ bra,
          carCreate r bra ket * ψ (x, ket) * φ (x, bra) := by
    apply Finset.sum_congr rfl
    intro x _
    exact Finset.sum_comm
  rw [hswap]
  apply Finset.sum_congr rfl
  intro x _
  apply Finset.sum_congr rfl
  intro ket _
  calc
    (∑ bra, carCreate r bra ket * ψ (x, ket) * φ (x, bra)) =
        ∑ bra, ψ (x, ket) * (carCreate r bra ket * φ (x, bra)) := by
          apply Finset.sum_congr rfl
          intro bra _
          ring
    _ = ψ (x, ket) * ∑ bra, carCreate r bra ket * φ (x, bra) := by
          rw [← Finset.mul_sum]
    _ = ψ (x, ket) * ∑ bra, carAnnihilate r ket bra * φ (x, bra) := by
          apply congrArg (fun z => ψ (x, ket) * z)
          apply Finset.sum_congr rfl
          intro bra _
          rw [carCreate]

theorem forwardSite_adjoint (N : ℕ) (r : Role) (ψ φ : ArchiveCochain N) :
    cochainPairing N (forwardSite N r ψ) φ =
      -cochainPairing N ψ (backwardSite N r φ) := by
  classical
  unfold cochainPairing forwardSite backwardSite
  rw [Finset.sum_comm]
  calc
    (∑ s, ∑ x, forwardDifference N r (fun y => ψ (y, s)) x * φ (x, s)) =
        ∑ s, -∑ x, ψ (x, s) *
          backwardDifference N r (fun y => φ (y, s)) x := by
          apply Finset.sum_congr rfl
          intro s _
          exact forward_backward_adjoint N r
            (fun y => ψ (y, s)) (fun y => φ (y, s))
    _ = -∑ s, ∑ x, ψ (x, s) *
          backwardDifference N r (fun y => φ (y, s)) x := by
          simp_rw [← Finset.sum_neg_distrib]
    _ = -∑ x, ∑ s, ψ (x, s) *
          backwardDifference N r (fun y => φ (y, s)) x := by
          rw [Finset.sum_comm]

theorem backwardSite_createAction_comm (N : ℕ) (r s : Role) (ψ : ArchiveCochain N) :
    backwardSite N r (createAction N s ψ) =
      createAction N s (backwardSite N r ψ) := by
  classical
  funext p
  change
    backwardDifference N r
        (fun x => ∑ ket : ArchiveFockState, carCreate s p.2 ket * ψ (x, ket)) p.1 =
      ∑ ket : ArchiveFockState,
        carCreate s p.2 ket *
          backwardDifference N r (fun x => ψ (x, ket)) p.1
  have hmul : ∀ (c : ArchiveFockState → ℝ) (F : ArchiveFockState → ArchiveRolePhaseGroup N → ℝ),
      backwardDifference N r (fun x => ∑ ket, c ket * F ket x) =
        fun x => ∑ ket, c ket * backwardDifference N r (F ket) x := by
    intro c F
    funext x
    simp only [backwardDifference_apply]
    calc
      forwardDifferenceScale N *
          ((∑ ket, c ket * F ket x) - ∑ ket, c ket * F ket (roleTranslateMinus N r x)) =
          forwardDifferenceScale N *
            ∑ ket, (c ket * F ket x - c ket * F ket (roleTranslateMinus N r x)) := by
        rw [← Finset.sum_sub_distrib]
      _ = ∑ ket, forwardDifferenceScale N *
            (c ket * F ket x - c ket * F ket (roleTranslateMinus N r x)) := by
        rw [Finset.mul_sum]
      _ = ∑ ket, c ket *
            (forwardDifferenceScale N *
              (F ket x - F ket (roleTranslateMinus N r x))) := by
        apply Finset.sum_congr rfl
        intro ket _
        ring
  exact congrFun (hmul (fun ket => carCreate s p.2 ket) (fun ket x => ψ (x, ket))) p.1

theorem backwardSite_annihilateAction_comm (N : ℕ) (r s : Role) (ψ : ArchiveCochain N) :
    backwardSite N r (annihilateAction N s ψ) =
      annihilateAction N s (backwardSite N r ψ) := by
  classical
  funext p
  change
    backwardDifference N r
        (fun x => ∑ ket, carAnnihilate s p.2 ket * ψ (x, ket)) p.1 =
      ∑ ket, carAnnihilate s p.2 ket *
        backwardDifference N r (fun x => ψ (x, ket)) p.1
  have hmul : ∀ (c : ArchiveFockState → ℝ) (F : ArchiveFockState → ArchiveRolePhaseGroup N → ℝ),
      backwardDifference N r (fun x => ∑ ket, c ket * F ket x) =
        fun x => ∑ ket, c ket * backwardDifference N r (F ket) x := by
    intro c F
    funext x
    simp only [backwardDifference_apply]
    calc
      forwardDifferenceScale N *
          ((∑ ket, c ket * F ket x) - ∑ ket, c ket * F ket (roleTranslateMinus N r x)) =
          forwardDifferenceScale N *
            ∑ ket, (c ket * F ket x - c ket * F ket (roleTranslateMinus N r x)) := by
        rw [← Finset.sum_sub_distrib]
      _ = ∑ ket, forwardDifferenceScale N *
            (c ket * F ket x - c ket * F ket (roleTranslateMinus N r x)) := by
        rw [Finset.mul_sum]
      _ = ∑ ket, c ket *
            (forwardDifferenceScale N *
              (F ket x - F ket (roleTranslateMinus N r x))) := by
        apply Finset.sum_congr rfl
        intro ket _
        ring
  exact congrFun (hmul (fun ket => carAnnihilate s p.2 ket) (fun ket x => ψ (x, ket))) p.1

theorem forwardCreateDirection_adjoint (N : ℕ) (r : Role) (ψ φ : ArchiveCochain N) :
    cochainPairing N (forwardCreateDirection N r ψ) φ =
      cochainPairing N ψ (-backwardAnnihilateDirection N r φ) := by
  calc
    cochainPairing N (forwardCreateDirection N r ψ) φ =
        cochainPairing N (createAction N r (forwardSite N r ψ)) φ := by
          rw [forwardCreateDirection_eq_createAction_forwardSite]
    _ = cochainPairing N (forwardSite N r ψ) (annihilateAction N r φ) :=
          createAction_adjoint N r _ _
    _ = -cochainPairing N ψ (backwardSite N r (annihilateAction N r φ)) :=
          forwardSite_adjoint N r _ _
    _ = -cochainPairing N ψ (annihilateAction N r (backwardSite N r φ)) := by
          rw [backwardSite_annihilateAction_comm]
    _ = cochainPairing N ψ (-backwardAnnihilateDirection N r φ) := by
          unfold cochainPairing backwardAnnihilateDirection
          simp only [Pi.neg_apply]
          simp_rw [mul_neg, ← Finset.sum_neg_distrib]

theorem cochainPairing_symm (N : ℕ) (ψ φ : ArchiveCochain N) :
    cochainPairing N ψ φ = cochainPairing N φ ψ := by
  unfold cochainPairing
  apply Finset.sum_congr rfl
  intro x _
  apply Finset.sum_congr rfl
  intro s _
  ring

theorem cochainPairing_sum_left {ι : Type*} [Fintype ι] (N : ℕ)
    (F : ι → ArchiveCochain N) (φ : ArchiveCochain N) :
    cochainPairing N (∑ i, F i) φ = ∑ i, cochainPairing N (F i) φ := by
  classical
  unfold cochainPairing
  simp only [Finset.sum_apply, Finset.sum_mul]
  conv_lhs =>
    enter [2, x]
    rw [Finset.sum_comm]
  rw [Finset.sum_comm]

theorem cochainPairing_sum_right {ι : Type*} [Fintype ι] (N : ℕ)
    (ψ : ArchiveCochain N) (F : ι → ArchiveCochain N) :
    cochainPairing N ψ (∑ i, F i) = ∑ i, cochainPairing N ψ (F i) := by
  rw [cochainPairing_symm, cochainPairing_sum_left]
  apply Finset.sum_congr rfl
  intro i _
  exact cochainPairing_symm N (F i) ψ

theorem dForward_adjoint (N : ℕ) (ψ φ : ArchiveCochain N) :
    cochainPairing N (dForward N ψ) φ =
      cochainPairing N ψ (hodgeCodifferential N φ) := by
  classical
  have hcod : hodgeCodifferential N φ =
      ∑ r : Role, fun p => -backwardAnnihilateDirection N r φ p := by
    funext p
    simp [hodgeCodifferential, Finset.sum_apply]
  calc
    cochainPairing N (dForward N ψ) φ =
        cochainPairing N (∑ r : Role, forwardCreateDirection N r ψ) φ := by
          rw [dForward_eq_sum_directions]
    _ = ∑ r, cochainPairing N (forwardCreateDirection N r ψ) φ :=
          cochainPairing_sum_left N (fun r => forwardCreateDirection N r ψ) φ
    _ = ∑ r, cochainPairing N ψ (-backwardAnnihilateDirection N r φ) := by
          apply Finset.sum_congr rfl
          intro r _
          exact forwardCreateDirection_adjoint N r ψ φ
    _ = cochainPairing N ψ
          (∑ r : Role, fun p => -backwardAnnihilateDirection N r φ p) := by
          rw [← cochainPairing_sum_right]
          rfl
    _ = cochainPairing N ψ (hodgeCodifferential N φ) := by
          rw [← hcod]

theorem hodgeCodifferential_adjoint (N : ℕ) (ψ φ : ArchiveCochain N) :
    cochainPairing N (hodgeCodifferential N ψ) φ =
      cochainPairing N ψ (dForward N φ) := by
  calc
    cochainPairing N (hodgeCodifferential N ψ) φ =
        cochainPairing N φ (hodgeCodifferential N ψ) := cochainPairing_symm _ _ _
    _ = cochainPairing N (dForward N φ) ψ := (dForward_adjoint N φ ψ).symm
    _ = cochainPairing N ψ (dForward N φ) := cochainPairing_symm _ _ _

/-- `D_H` is symmetric for the finite counting pairing: `D_H† = D_H`. -/
theorem hodgeCarDirac_self_adjoint (N : ℕ) (ψ φ : ArchiveCochain N) :
    cochainPairing N (hodgeCarDirac N ψ) φ =
      cochainPairing N ψ (hodgeCarDirac N φ) := by
  unfold hodgeCarDirac cochainPairing
  simp_rw [Pi.add_apply, add_mul, mul_add, Finset.sum_add_distrib]
  have hd := dForward_adjoint N ψ φ
  have hδ := hodgeCodifferential_adjoint N ψ φ
  unfold cochainPairing at hd hδ
  linarith

/-! ## Fermionic parity -/

theorem fockOccupationCount_eq_fockDegree :
    ∀ s : ArchiveFockState, fockOccupationCount s = fockDegree s := by
  native_decide

theorem fockParitySign_succ (n : ℕ) :
    (if (n + 1) % 2 = 0 then (1 : ℝ) else -1) =
      -(if n % 2 = 0 then 1 else -1) := by
  rcases Nat.mod_two_eq_zero_or_one n with h | h
  · simp [h, Nat.add_mod]
  · have h2 : (n + 1) % 2 = 0 := by omega
    simp [h, h2]

theorem fockParitySign_of_succ_degree
    {bra ket : ArchiveFockState} (h : fockDegree bra = fockDegree ket + 1) :
    fockParitySign bra = -fockParitySign ket := by
  have hocc : fockOccupationCount bra = fockOccupationCount ket + 1 := by
    rw [fockOccupationCount_eq_fockDegree bra, fockOccupationCount_eq_fockDegree ket, h]
  unfold fockParitySign
  rw [hocc]
  exact fockParitySign_succ (fockOccupationCount ket)

theorem carCreate_parity_flip (r : Role) (bra ket : ArchiveFockState) :
    fockParitySign bra * carCreate r bra ket =
      -(fockParitySign ket * carCreate r bra ket) := by
  classical
  by_cases hc : carCreate r bra ket = 0
  · rw [hc]
    ring
  · have hdeg := carCreate_degree_raise r bra ket hc
    have hsign := fockParitySign_of_succ_degree hdeg
    rw [hsign]
    ring

theorem carAnnihilate_parity_flip (r : Role) (bra ket : ArchiveFockState) :
    fockParitySign bra * carAnnihilate r bra ket =
      -(fockParitySign ket * carAnnihilate r bra ket) := by
  classical
  by_cases hc : carAnnihilate r bra ket = 0
  · rw [hc]
    ring
  · have hdeg := carAnnihilate_degree_lower r bra ket hc
    have hsign := fockParitySign_of_succ_degree hdeg
    rw [hsign]
    ring

theorem createAction_parity_odd (N : ℕ) (r : Role) (ψ : ArchiveCochain N) :
    parityCochain N (createAction N r ψ) =
      -createAction N r (parityCochain N ψ) := by
  classical
  funext p
  unfold parityCochain createAction
  simp only [Pi.neg_apply]
  rw [Finset.mul_sum, ← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl
  intro ket _
  have h := carCreate_parity_flip r p.2 ket
  calc
    fockParitySign p.2 * (carCreate r p.2 ket * ψ (p.1, ket)) =
        (fockParitySign p.2 * carCreate r p.2 ket) * ψ (p.1, ket) := by ring
    _ = (-(fockParitySign ket * carCreate r p.2 ket)) * ψ (p.1, ket) := by rw [h]
    _ = -(carCreate r p.2 ket * (fockParitySign ket * ψ (p.1, ket))) := by ring

theorem annihilateAction_parity_odd (N : ℕ) (r : Role) (ψ : ArchiveCochain N) :
    parityCochain N (annihilateAction N r ψ) =
      -annihilateAction N r (parityCochain N ψ) := by
  classical
  funext p
  unfold parityCochain annihilateAction
  simp only [Pi.neg_apply]
  rw [Finset.mul_sum, ← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl
  intro ket _
  have h := carAnnihilate_parity_flip r p.2 ket
  calc
    fockParitySign p.2 * (carAnnihilate r p.2 ket * ψ (p.1, ket)) =
        (fockParitySign p.2 * carAnnihilate r p.2 ket) * ψ (p.1, ket) := by ring
    _ = (-(fockParitySign ket * carAnnihilate r p.2 ket)) * ψ (p.1, ket) := by rw [h]
    _ = -(carAnnihilate r p.2 ket * (fockParitySign ket * ψ (p.1, ket))) := by ring

theorem forwardSite_parity_comm (N : ℕ) (r : Role) (ψ : ArchiveCochain N) :
    parityCochain N (forwardSite N r ψ) =
      forwardSite N r (parityCochain N ψ) := by
  funext p
  unfold parityCochain forwardSite forwardDifference
  simp
  ring

theorem backwardSite_parity_comm (N : ℕ) (r : Role) (ψ : ArchiveCochain N) :
    parityCochain N (backwardSite N r ψ) =
      backwardSite N r (parityCochain N ψ) := by
  funext p
  unfold parityCochain backwardSite backwardDifference
  simp
  ring

theorem dForward_parity_odd (N : ℕ) (ψ : ArchiveCochain N) :
    parityCochain N (dForward N ψ) = -dForward N (parityCochain N ψ) := by
  classical
  funext p
  unfold parityCochain dForward
  simp only [Pi.neg_apply]
  rw [Finset.mul_sum, ← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl
  intro r _
  rw [forwardCreateDirection_eq_createAction_forwardSite,
    forwardCreateDirection_eq_createAction_forwardSite]
  have h := congrFun (createAction_parity_odd N r (forwardSite N r ψ)) p
  simp only [parityCochain, Pi.neg_apply] at h
  rw [h]
  have harg : parityCochain N (forwardSite N r ψ) =
      forwardSite N r (parityCochain N ψ) := forwardSite_parity_comm N r ψ
  rw [harg]
  unfold parityCochain
  rfl

theorem hodgeCodifferential_parity_odd (N : ℕ) (ψ : ArchiveCochain N) :
    parityCochain N (hodgeCodifferential N ψ) =
      -hodgeCodifferential N (parityCochain N ψ) := by
  classical
  funext p
  unfold parityCochain hodgeCodifferential
  simp only [Pi.neg_apply]
  rw [Finset.mul_sum, ← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl
  intro r _
  have h := congrFun
    (annihilateAction_parity_odd N r (backwardSite N r ψ)) p
  simp only [parityCochain, Pi.neg_apply, backwardAnnihilateDirection] at h
  calc
    fockParitySign p.2 * -annihilateAction N r (backwardSite N r ψ) p =
        -(fockParitySign p.2 * annihilateAction N r (backwardSite N r ψ) p) := by ring
    _ = -((-annihilateAction N r (parityCochain N (backwardSite N r ψ))) p) := by
          rw [h]
          rfl
    _ = annihilateAction N r (backwardSite N r (parityCochain N ψ)) p := by
          rw [backwardSite_parity_comm]
          simp
    _ = -(-annihilateAction N r (backwardSite N r (parityCochain N ψ)) p) := by
          simp

theorem parityCochain_add (N : ℕ) (ψ φ : ArchiveCochain N) :
    parityCochain N (ψ + φ) = parityCochain N ψ + parityCochain N φ := by
  funext p
  unfold parityCochain
  simp
  ring

/-- Fermionic parity is odd for `D_H`: `(-1)^F D_H = -D_H (-1)^F`. -/
theorem hodgeCarDirac_parity_odd (N : ℕ) (ψ : ArchiveCochain N) :
    parityCochain N (hodgeCarDirac N ψ) =
      -hodgeCarDirac N (parityCochain N ψ) := by
  unfold hodgeCarDirac
  rw [parityCochain_add, dForward_parity_odd, hodgeCodifferential_parity_odd]
  funext p
  simp [Pi.neg_apply, Pi.add_apply]
  ring

end

end D0.Geometry
