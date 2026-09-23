import Mathlib.Tactic
import D0.Geometry.ArchiveDiagonalRoleTransport
import D0.Geometry.ArchiveHodgeCARDiracKernel

/-!
# Fermion number and parity for the Hodge/CAR operator

`numberCochain` multiplies each Fock component by its occupation.
Creation raises that count and annihilation lowers it, so the number
operator commutes with `D_H²` and does not commute with `D_H`.
Parity remains the odd grading of `D_H`, not an ordinary commuting symmetry.
-/

namespace D0.Geometry

open D0
open RoleFockPermutation
open scoped BigOperators

noncomputable section

variable {N : ℕ}

def numberCochain (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => (fockDegree p.2 : ℝ) * ψ p

theorem numberCochain_add (ψ φ : ArchiveCochain N) :
    numberCochain N (ψ + φ) = numberCochain N ψ + numberCochain N φ := by
  funext p
  simp only [numberCochain, Pi.add_apply]
  ring

theorem numberCochain_smul (c : ℝ) (ψ : ArchiveCochain N) :
    numberCochain N (c • ψ) = c • numberCochain N ψ := by
  funext p
  simp only [numberCochain, Pi.smul_apply, smul_eq_mul]
  ring

theorem numberCochain_zero : numberCochain N (0 : ArchiveCochain N) = 0 := by
  funext p
  simp [numberCochain]

lemma forwardDifference_const_mul (r : Role) (c : ℝ)
    (f : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) :
    forwardDifference N r (fun y => c * f y) x = c * forwardDifference N r f x := by
  simp only [forwardDifference_apply]
  ring

lemma backwardDifference_const_mul (r : Role) (c : ℝ)
    (f : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) :
    backwardDifference N r (fun y => c * f y) x = c * backwardDifference N r f x := by
  simp only [backwardDifference_apply]
  ring

lemma degree_create_split (r : Role) (bra ket : ArchiveFockState) :
    (fockDegree bra : ℝ) * carCreate r bra ket =
      (fockDegree ket : ℝ) * carCreate r bra ket + carCreate r bra ket := by
  classical
  by_cases hc : carCreate r bra ket = 0
  · rw [hc]
    ring
  · rw [carCreate_degree_raise r bra ket hc, Nat.cast_add, Nat.cast_one]
    ring

lemma degree_annihilate_split (r : Role) (bra ket : ArchiveFockState) :
    (fockDegree bra : ℝ) * carAnnihilate r bra ket =
      (fockDegree ket : ℝ) * carAnnihilate r bra ket - carAnnihilate r bra ket := by
  classical
  by_cases hc : carAnnihilate r bra ket = 0
  · rw [hc]
    ring
  · have hdeg := carAnnihilate_degree_lower r bra ket hc
    have hbra : (fockDegree bra : ℝ) = (fockDegree ket : ℝ) - 1 := by
      have hnat : fockDegree ket = fockDegree bra + 1 := hdeg
      rw [hnat, Nat.cast_add, Nat.cast_one]
      ring
    rw [hbra]
    ring

theorem number_comm_dForward (ψ : ArchiveCochain N) :
    numberCochain N (dForward N ψ) =
      dForward N (numberCochain N ψ) + dForward N ψ := by
  classical
  funext p
  simp only [numberCochain, dForward, Pi.add_apply, forwardCreateDirection]
  calc
    (fockDegree p.2 : ℝ) * ∑ r, ∑ ket,
        carCreate r p.2 ket * forwardDifference N r (fun y => ψ (y, ket)) p.1 =
      ∑ r, ∑ ket, (fockDegree p.2 : ℝ) *
        (carCreate r p.2 ket * forwardDifference N r (fun y => ψ (y, ket)) p.1) := by
        rw [Finset.mul_sum]
        refine Finset.sum_congr rfl fun r _ => ?_
        rw [Finset.mul_sum]
    _ = ∑ r, ∑ ket,
        (carCreate r p.2 ket *
            forwardDifference N r (fun y => (fockDegree ket : ℝ) * ψ (y, ket)) p.1 +
          carCreate r p.2 ket *
            forwardDifference N r (fun y => ψ (y, ket)) p.1) := by
        refine Finset.sum_congr rfl fun r _ => ?_
        refine Finset.sum_congr rfl fun ket _ => ?_
        have hdiff := forwardDifference_const_mul (N := N) r (fockDegree ket)
          (fun y => ψ (y, ket)) p.1
        have hsplit := degree_create_split r p.2 ket
        calc
          (fockDegree p.2 : ℝ) *
              (carCreate r p.2 ket * forwardDifference N r (fun y => ψ (y, ket)) p.1) =
            ((fockDegree p.2 : ℝ) * carCreate r p.2 ket) *
              forwardDifference N r (fun y => ψ (y, ket)) p.1 := by ring
          _ = (((fockDegree ket : ℝ) * carCreate r p.2 ket) + carCreate r p.2 ket) *
              forwardDifference N r (fun y => ψ (y, ket)) p.1 := by rw [hsplit]
          _ = carCreate r p.2 ket *
                ((fockDegree ket : ℝ) * forwardDifference N r (fun y => ψ (y, ket)) p.1) +
              carCreate r p.2 ket *
                forwardDifference N r (fun y => ψ (y, ket)) p.1 := by ring
          _ = carCreate r p.2 ket *
                forwardDifference N r (fun y => (fockDegree ket : ℝ) * ψ (y, ket)) p.1 +
              carCreate r p.2 ket *
                forwardDifference N r (fun y => ψ (y, ket)) p.1 := by rw [← hdiff]
    _ = (∑ r, ∑ ket, carCreate r p.2 ket *
          forwardDifference N r (fun y => numberCochain N ψ (y, ket)) p.1) +
        (∑ r, ∑ ket, carCreate r p.2 ket *
          forwardDifference N r (fun y => ψ (y, ket)) p.1) := by
        rw [← Finset.sum_add_distrib]
        refine Finset.sum_congr rfl fun r _ => ?_
        rw [← Finset.sum_add_distrib]
        refine Finset.sum_congr rfl fun ket _ => ?_
        simp only [numberCochain]

theorem number_comm_hodgeCodifferential (ψ : ArchiveCochain N) :
    numberCochain N (hodgeCodifferential N ψ) =
      hodgeCodifferential N (numberCochain N ψ) - hodgeCodifferential N ψ := by
  classical
  funext p
  simp only [numberCochain, hodgeCodifferential, Pi.sub_apply,
    backwardAnnihilateDirection, annihilateAction, backwardSite]
  calc
    (fockDegree p.2 : ℝ) * ∑ r, -∑ ket,
        carAnnihilate r p.2 ket *
          backwardDifference N r (fun y => ψ (y, ket)) p.1 =
      ∑ r, -∑ ket, (fockDegree p.2 : ℝ) *
        (carAnnihilate r p.2 ket *
          backwardDifference N r (fun y => ψ (y, ket)) p.1) := by
        rw [Finset.mul_sum]
        refine Finset.sum_congr rfl fun r _ => ?_
        rw [mul_neg, Finset.mul_sum]
    _ = ∑ r, ((-∑ ket, carAnnihilate r p.2 ket *
          backwardDifference N r (fun y => (fockDegree ket : ℝ) * ψ (y, ket)) p.1) -
        (-∑ ket, carAnnihilate r p.2 ket *
          backwardDifference N r (fun y => ψ (y, ket)) p.1)) := by
        refine Finset.sum_congr rfl fun r _ => ?_
        rw [← Finset.sum_neg_distrib]
        have hR :
            (-∑ ket, carAnnihilate r p.2 ket *
                backwardDifference N r (fun y => (fockDegree ket : ℝ) * ψ (y, ket)) p.1) -
              (-∑ ket, carAnnihilate r p.2 ket *
                backwardDifference N r (fun y => ψ (y, ket)) p.1) =
              ∑ ket, (carAnnihilate r p.2 ket *
                  backwardDifference N r (fun y => ψ (y, ket)) p.1 -
                carAnnihilate r p.2 ket *
                  backwardDifference N r (fun y => (fockDegree ket : ℝ) * ψ (y, ket)) p.1) := by
          rw [sub_eq_add_neg, neg_neg, add_comm, ← Finset.sum_neg_distrib,
            ← Finset.sum_add_distrib]
          refine Finset.sum_congr rfl fun ket _ => ?_
          ring
        rw [hR]
        refine Finset.sum_congr rfl fun ket _ => ?_
        have hdiff := backwardDifference_const_mul (N := N) r (fockDegree ket)
          (fun y => ψ (y, ket)) p.1
        have hsplit := degree_annihilate_split r p.2 ket
        calc
          -((fockDegree p.2 : ℝ) *
              (carAnnihilate r p.2 ket *
                backwardDifference N r (fun y => ψ (y, ket)) p.1)) =
            -((((fockDegree ket : ℝ) * carAnnihilate r p.2 ket) -
                carAnnihilate r p.2 ket) *
              backwardDifference N r (fun y => ψ (y, ket)) p.1) := by
              rw [← hsplit]
              ring
          _ = carAnnihilate r p.2 ket *
                backwardDifference N r (fun y => ψ (y, ket)) p.1 -
              carAnnihilate r p.2 ket *
                ((fockDegree ket : ℝ) *
                  backwardDifference N r (fun y => ψ (y, ket)) p.1) := by ring
          _ = carAnnihilate r p.2 ket *
                backwardDifference N r (fun y => ψ (y, ket)) p.1 -
              carAnnihilate r p.2 ket *
                backwardDifference N r (fun y => (fockDegree ket : ℝ) * ψ (y, ket)) p.1 := by
              rw [← hdiff]
    _ = (∑ r, -∑ ket, carAnnihilate r p.2 ket *
          backwardDifference N r (fun y => numberCochain N ψ (y, ket)) p.1) -
        (∑ r, -∑ ket, carAnnihilate r p.2 ket *
          backwardDifference N r (fun y => ψ (y, ket)) p.1) := by
        rw [← Finset.sum_sub_distrib]
        refine Finset.sum_congr rfl fun r _ => ?_
        simp only [numberCochain]

theorem number_comm_hodgeCarDirac (ψ : ArchiveCochain N) :
    numberCochain N (hodgeCarDirac N ψ) - hodgeCarDirac N (numberCochain N ψ) =
      dForward N ψ - hodgeCodifferential N ψ := by
  have hd := number_comm_dForward ψ
  have hδ := number_comm_hodgeCodifferential ψ
  rw [hodgeCarDirac, hodgeCarDirac, numberCochain_add, hd, hδ]
  abel

theorem fockDegree_singleton (r : Role) : fockDegree (fockSingletonState r) = 1 := by
  classical
  unfold fockDegree
  rw [Finset.card_eq_one]
  refine ⟨r, ?_⟩
  ext s
  simp only [Finset.mem_filter, Finset.mem_univ, Finset.mem_singleton, true_and,
    fockSingletonState]
  constructor
  · intro hs
    by_cases hsr : s = r
    · exact hsr
    · simp [hsr] at hs
  · intro hs
    simp [hs]

/-- Occupation is not a symmetry of the first-order Hodge/CAR operator. -/
theorem number_not_commute_hodgeCarDirac :
    ∃ ψ : ArchiveCochain 1,
      numberCochain 1 (hodgeCarDirac 1 ψ) ≠ hodgeCarDirac 1 (numberCochain 1 ψ) := by
  classical
  refine ⟨bVacuumCochain, ?_⟩
  intro h
  have hnumber : numberCochain 1 bVacuumCochain = 0 := by
    funext p
    by_cases hp : bVacuumCochain p = 0
    · simp [numberCochain, hp]
    · have hvac := bVacuumCochain_support_vacuum p hp
      simp [numberCochain, hvac, fockDegree_vacuum]
  rw [hnumber, hodgeCarDirac_zero] at h
  have hpt := congrFun h (witnessOrigin, fockSingletonState B)
  simp only [numberCochain, Pi.zero_apply, hodgeCarDirac_bVacuum_at_singletonB,
    fockDegree_singleton, Nat.cast_one, one_mul] at hpt
  norm_num at hpt

lemma scalarDifferenceLaplacian_const_mul (c : ℝ)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    scalarDifferenceLaplacian N (fun x => c * f x) =
      fun x => c * scalarDifferenceLaplacian N f x := by
  funext x
  simp only [scalarDifferenceLaplacian]
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun r _ => ?_
  have hforward : forwardDifference N r (fun y => c * f y) =
      fun y => c * forwardDifference N r f y := by
    funext y
    exact forwardDifference_const_mul r c f y
  rw [hforward]
  have hback := backwardDifference_const_mul r c
    (forwardDifference N r f) x
  rw [hback]
  ring

theorem number_commutes_hodgeSquare (ψ : ArchiveCochain N) :
    numberCochain N (hodgeCarDirac N (hodgeCarDirac N ψ)) =
      hodgeCarDirac N (hodgeCarDirac N (numberCochain N ψ)) := by
  rw [hodgeCarDirac_sq, hodgeCarDirac_sq]
  funext p
  simp only [numberCochain, cochainDifferenceLaplacian]
  have hmul := congrFun
    (scalarDifferenceLaplacian_const_mul (N := N) (fockDegree p.2)
      (fun x => ψ (x, p.2))) p.1
  exact hmul.symm

/-- Parity anticommutes with `D_H`. It is a grading, not a commuting symmetry. -/
theorem parity_anticommutes_hodgeCarDirac (ψ : ArchiveCochain N) :
    parityCochain N (hodgeCarDirac N ψ) =
      -hodgeCarDirac N (parityCochain N ψ) :=
  hodgeCarDirac_parity_odd N ψ

theorem parity_commutes_hodgeSquare (ψ : ArchiveCochain N) :
    parityCochain N (hodgeCarDirac N (hodgeCarDirac N ψ)) =
      hodgeCarDirac N (hodgeCarDirac N (parityCochain N ψ)) := by
  rw [parity_anticommutes_hodgeCarDirac, parity_anticommutes_hodgeCarDirac]
  have hneg : hodgeCarDirac N (-hodgeCarDirac N (parityCochain N ψ)) =
      -hodgeCarDirac N (hodgeCarDirac N (parityCochain N ψ)) := by
    simpa [neg_one_smul] using
      hodgeCarDirac_smul N (-1) (hodgeCarDirac N (parityCochain N ψ))
  rw [hneg, neg_neg]

theorem diagonalRoleTransport_commutes_number (σ : Equiv.Perm Role)
    (ψ : ArchiveCochain N) :
    numberCochain N (diagonalRoleTransport σ ψ) =
      diagonalRoleTransport σ (numberCochain N ψ) := by
  classical
  funext p
  unfold numberCochain diagonalRoleTransport
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun ket _ => ?_
  by_cases htr : p.2 = transportState σ ket
  · have hdeg : fockDegree p.2 = fockDegree ket := by
      rw [htr, fockDegree_transport]
    rw [hdeg]
    ring
  · have hε : signedTransport σ p.2 ket = 0 := by
      unfold signedTransport
      rw [if_neg htr]
    simp [hε]

theorem diagonalRoleTransport_preserves_degree (σ : Equiv.Perm Role) (k : ℕ)
    (ψ : ArchiveCochain N)
    (hψ : ∀ p, ψ p ≠ 0 → fockDegree p.2 = k)
    (p : ArchiveCochainBasis N)
    (hp : diagonalRoleTransport σ ψ p ≠ 0) :
    fockDegree p.2 = k := by
  classical
  unfold diagonalRoleTransport at hp
  obtain ⟨ket, _, hterm⟩ := Finset.exists_ne_zero_of_sum_ne_zero hp
  have hψket : ψ (permuteRoleSite σ.symm p.1, ket) ≠ 0 := by
    intro h0
    apply hterm
    simp [h0]
  have hdegψ := hψ (permuteRoleSite σ.symm p.1, ket) hψket
  have hε : signedTransport σ p.2 ket ≠ 0 := by
    intro h0
    apply hterm
    simp [h0]
  have htr : p.2 = transportState σ ket := by
    by_contra hne
    apply hε
    simp [signedTransport, hne]
  rw [htr, fockDegree_transport]
  exact hdegψ

lemma fockParitySign_eq_degree (s t : ArchiveFockState)
    (h : fockDegree s = fockDegree t) :
    fockParitySign s = fockParitySign t := by
  unfold fockParitySign
  rw [fockOccupationCount_eq_fockDegree s, fockOccupationCount_eq_fockDegree t, h]

theorem diagonalRoleTransport_commutes_parity (σ : Equiv.Perm Role)
    (ψ : ArchiveCochain N) :
    parityCochain N (diagonalRoleTransport σ ψ) =
      diagonalRoleTransport σ (parityCochain N ψ) := by
  classical
  funext p
  unfold parityCochain diagonalRoleTransport
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun ket _ => ?_
  by_cases htr : p.2 = transportState σ ket
  · have hsign : fockParitySign p.2 = fockParitySign ket :=
      fockParitySign_eq_degree p.2 ket (by rw [htr, fockDegree_transport])
    rw [hsign]
    ring
  · have hε : signedTransport σ p.2 ket = 0 := by
      unfold signedTransport
      rw [if_neg htr]
    simp [hε]

end

end D0.Geometry
