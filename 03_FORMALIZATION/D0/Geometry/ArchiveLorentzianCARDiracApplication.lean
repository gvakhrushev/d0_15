import Mathlib.Data.Complex.Basic
import Mathlib.Tactic
import D0.Geometry.ArchiveLorentzianFourierApplication

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

/-!
# Lorentz-signed CAR operator on the archive carrier

The source Eq. (5) has the ordinary forward creation term and a role-signed
backward annihilation term. The existing Hodge--Dirac instead uses the same
sign for every role. This module keeps the source's signs explicit and proves
their square on the existing complex site × Fock carrier. It does not select
the role signs as a physical metric.

Together with the companion Fourier application, this gives the exact
all-period Fourier eigenvalue of the squared first-order operator on every
sixteen-component Fock fibre. It remains a conditional operator theorem for
the explicit role-sign assignment, not a physical source-selection result.
-/

/-- Role-weighted annihilation part of the source's first-order CAR operator.
The supplied weights act only on annihilation, exactly as in the source. -/
def roleWeightedArchiveCodifferential (N : ℕ) (w : Role → ℝ)
    (ψ : ArchiveCochainC N) : ArchiveCochainC N :=
  ∑ r : Role, (-(w r : ℂ)) •
    twistedAnnihilateDirection N (fun _ => 1) r ψ

/-- First-order archive CAR operator with explicit role weights. -/
def roleWeightedArchiveCARDirac (N : ℕ) (w : Role → ℝ)
    (ψ : ArchiveCochainC N) : ArchiveCochainC N :=
  dTwisted N (fun _ => 1) ψ + roleWeightedArchiveCodifferential N w ψ

/-- The existing role-sign assignment instantiated in the first-order CAR
operator. It remains an explicit mathematical input, not physical selection. -/
def archiveLorentzianCARDirac (N : ℕ) (ψ : ArchiveCochainC N) :
    ArchiveCochainC N :=
  roleWeightedArchiveCARDirac N roleLorentzSign ψ

theorem twistedAnnihilateDirection_smul (N : ℕ) (H : Role → ℂ) (r : Role)
    (c : ℂ) (ψ : ArchiveCochainC N) :
    twistedAnnihilateDirection N H r (c • ψ) =
      c • twistedAnnihilateDirection N H r ψ := by
  classical
  funext p
  unfold twistedAnnihilateDirection annihilateActionC twistedBackwardSite
  simp only [Pi.smul_apply, smul_eq_mul]
  calc
    (∑ ket, (carAnnihilate r p.2 ket : ℂ) *
        twistedBackwardDifference N r (H r)
          (fun x => c * ψ (x, ket)) p.1) =
        ∑ ket, c * ((carAnnihilate r p.2 ket : ℂ) *
          twistedBackwardDifference N r (H r) (fun x => ψ (x, ket)) p.1) := by
            refine Finset.sum_congr rfl ?_
            intro ket _
            rw [congrFun (twistedBackwardDifference_const_mul N r (H r) c
              (fun x => ψ (x, ket))) p.1]
            ring
    _ = c * ∑ ket, (carAnnihilate r p.2 ket : ℂ) *
          twistedBackwardDifference N r (H r) (fun x => ψ (x, ket)) p.1 := by
            rw [Finset.mul_sum]

theorem roleWeightedArchiveCodifferential_add (N : ℕ) (w : Role → ℝ)
    (ψ φ : ArchiveCochainC N) :
    roleWeightedArchiveCodifferential N w (ψ + φ) =
      roleWeightedArchiveCodifferential N w ψ +
        roleWeightedArchiveCodifferential N w φ := by
  classical
  unfold roleWeightedArchiveCodifferential
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl ?_
  intro r _
  rw [twistedAnnihilateDirection_add]
  simp only [smul_add]

theorem roleWeightedArchiveCodifferential_smul (N : ℕ) (w : Role → ℝ)
    (c : ℂ) (ψ : ArchiveCochainC N) :
    roleWeightedArchiveCodifferential N w (c • ψ) =
      c • roleWeightedArchiveCodifferential N w ψ := by
  classical
  unfold roleWeightedArchiveCodifferential
  funext p
  simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
  calc
    (∑ r, -(w r : ℂ) *
        twistedAnnihilateDirection N (fun _ => 1) r (c • ψ) p) =
      ∑ r, c * (-(w r : ℂ) *
        twistedAnnihilateDirection N (fun _ => 1) r ψ p) := by
          refine Finset.sum_congr rfl ?_
          intro r _
          rw [twistedAnnihilateDirection_smul]
          simp only [Pi.smul_apply, smul_eq_mul]
          ring_nf
    _ = c * ∑ r, -(w r : ℂ) *
          twistedAnnihilateDirection N (fun _ => 1) r ψ p := by
          rw [Finset.mul_sum]

theorem roleWeightedArchiveCodifferential_square (N : ℕ) (w : Role → ℝ)
    (ψ : ArchiveCochainC N) :
    roleWeightedArchiveCodifferential N w
        (roleWeightedArchiveCodifferential N w ψ) = 0 := by
  classical
  funext p
  unfold roleWeightedArchiveCodifferential
  simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
  have harg :
      (fun q => ∑ s : Role, -(w s : ℂ) *
        twistedAnnihilateDirection N (fun _ => 1) s ψ q) =
      ∑ s : Role, (-(w s : ℂ)) • twistedAnnihilateDirection N (fun _ => 1) s ψ := by
    funext q
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
  calc
    (∑ r, -(w r : ℂ) *
        twistedAnnihilateDirection N (fun _ => 1) r
          (fun q => ∑ s, -(w s : ℂ) *
            twistedAnnihilateDirection N (fun _ => 1) s ψ q) p) =
      ∑ r, ∑ s, (w r : ℂ) * (w s : ℂ) *
        twistedAnnihilateDirection N (fun _ => 1) r
          (twistedAnnihilateDirection N (fun _ => 1) s ψ) p := by
          refine Finset.sum_congr rfl ?_
          intro r _
          rw [harg]
          have hsum := congrFun
            (twistedAnnihilateDirection_sum N (fun _ => 1) r
              (fun s => (-(w s : ℂ)) •
                twistedAnnihilateDirection N (fun _ => 1) s ψ)) p
          rw [hsum]
          simp only [Finset.sum_apply]
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl ?_
          intro s _
          rw [twistedAnnihilateDirection_smul]
          simp only [Pi.smul_apply, smul_eq_mul]
          ring_nf
    _ = 0 := by
          exact pairwise_complex_sum_zero
            (fun r s => (w r : ℂ) * (w s : ℂ) *
              twistedAnnihilateDirection N (fun _ => 1) r
                (twistedAnnihilateDirection N (fun _ => 1) s ψ) p)
            (by
              intro r s
              change (w r : ℂ) * (w s : ℂ) *
                    twistedAnnihilateDirection N (fun _ => 1) r
                      (twistedAnnihilateDirection N (fun _ => 1) s ψ) p +
                  (w s : ℂ) * (w r : ℂ) *
                    twistedAnnihilateDirection N (fun _ => 1) s
                      (twistedAnnihilateDirection N (fun _ => 1) r ψ) p = 0
              have hanti := congrFun
                (twistedAnnihilate_anticommute N (fun _ => 1) r s ψ) p
              have hanti' :
                  twistedAnnihilateDirection N (fun _ => 1) r
                      (twistedAnnihilateDirection N (fun _ => 1) s ψ) p +
                    twistedAnnihilateDirection N (fun _ => 1) s
                      (twistedAnnihilateDirection N (fun _ => 1) r ψ) p = 0 := by
                simpa only [Pi.add_apply, Pi.zero_apply] using hanti
              calc
                (w r : ℂ) * (w s : ℂ) *
                    twistedAnnihilateDirection N (fun _ => 1) r
                      (twistedAnnihilateDirection N (fun _ => 1) s ψ) p +
                  (w s : ℂ) * (w r : ℂ) *
                    twistedAnnihilateDirection N (fun _ => 1) s
                      (twistedAnnihilateDirection N (fun _ => 1) r ψ) p =
                    (w r : ℂ) * (w s : ℂ) *
                      (twistedAnnihilateDirection N (fun _ => 1) r
                          (twistedAnnihilateDirection N (fun _ => 1) s ψ) p +
                        twistedAnnihilateDirection N (fun _ => 1) s
                          (twistedAnnihilateDirection N (fun _ => 1) r ψ) p) := by ring
                _ = 0 := by rw [hanti']; simp)

theorem roleWeightedArchiveCodifferential_cross (N : ℕ) (w : Role → ℝ)
    (ψ : ArchiveCochainC N) :
    dTwisted N (fun _ => 1) (roleWeightedArchiveCodifferential N w ψ) +
      roleWeightedArchiveCodifferential N w (dTwisted N (fun _ => 1) ψ) =
        roleWeightedArchiveDifferenceOperator N w ψ := by
  classical
  have hne : ∀ t : Role, (fun _ : Role => (1 : ℂ)) t ≠ 0 := fun _ => one_ne_zero
  funext p
  have hleft :
      dTwisted N (fun _ => 1) (roleWeightedArchiveCodifferential N w ψ) p =
        ∑ r : Role, ∑ s : Role, (-(w s : ℂ)) *
          twistedCreateDirection N (fun _ => 1) r
            (twistedAnnihilateDirection N (fun _ => 1) s ψ) p := by
    unfold dTwisted roleWeightedArchiveCodifferential
    simp only [Finset.sum_apply]
    simp_rw [twistedCreateDirection_sum, twistedCreateDirection_smul]
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]

  have hright :
      roleWeightedArchiveCodifferential N w (dTwisted N (fun _ => 1) ψ) p =
        ∑ r : Role, ∑ s : Role, (-(w s : ℂ)) *
          twistedAnnihilateDirection N (fun _ => 1) s
            (twistedCreateDirection N (fun _ => 1) r ψ) p := by
    unfold roleWeightedArchiveCodifferential dTwisted
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
    change (∑ s : Role, -(w s : ℂ) *
        twistedAnnihilateDirection N (fun _ => 1) s
          (∑ r : Role, twistedCreateDirection N (fun _ => 1) r ψ) p) = _
    calc
      (∑ s, -(w s : ℂ) *
          twistedAnnihilateDirection N (fun _ => 1) s
            (∑ r, twistedCreateDirection N (fun _ => 1) r ψ) p) =
        ∑ s, -(w s : ℂ) *
          (∑ r, twistedAnnihilateDirection N (fun _ => 1) s
            (twistedCreateDirection N (fun _ => 1) r ψ)) p := by
              refine Finset.sum_congr rfl ?_
              intro s _
              rw [congrFun (twistedAnnihilateDirection_sum N (fun _ => 1) s
                (fun r => twistedCreateDirection N (fun _ => 1) r ψ)) p]
      _ = ∑ s, ∑ r, (-(w s : ℂ)) *
            twistedAnnihilateDirection N (fun _ => 1) s
              (twistedCreateDirection N (fun _ => 1) r ψ) p := by
              refine Finset.sum_congr rfl ?_
              intro s _
              simp only [Finset.sum_apply]
              rw [Finset.mul_sum]
      _ = ∑ r, ∑ s, (-(w s : ℂ)) *
            twistedAnnihilateDirection N (fun _ => 1) s
              (twistedCreateDirection N (fun _ => 1) r ψ) p := by
              rw [Finset.sum_comm]

  change dTwisted N (fun _ => 1) (roleWeightedArchiveCodifferential N w ψ) p +
      roleWeightedArchiveCodifferential N w (dTwisted N (fun _ => 1) ψ) p = _
  rw [hleft, hright]
  have hflat :
      (∑ r : Role, ∑ s : Role,
          (-(w s : ℂ)) *
            twistedCreateDirection N (fun _ => 1) r
              (twistedAnnihilateDirection N (fun _ => 1) s ψ) p) +
        (∑ r : Role, ∑ s : Role,
          (-(w s : ℂ)) *
            twistedAnnihilateDirection N (fun _ => 1) s
              (twistedCreateDirection N (fun _ => 1) r ψ) p) =
        ∑ r : Role, ∑ s : Role,
          ((-(w s : ℂ)) *
              twistedCreateDirection N (fun _ => 1) r
                (twistedAnnihilateDirection N (fun _ => 1) s ψ) p +
            (-(w s : ℂ)) *
              twistedAnnihilateDirection N (fun _ => 1) s
                (twistedCreateDirection N (fun _ => 1) r ψ) p) := by
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl ?_
    intro r _
    rw [← Finset.sum_add_distrib]
  rw [hflat]
  have hpair : ∀ r s : Role,
      (-(w s : ℂ)) *
          twistedCreateDirection N (fun _ => 1) r
            (twistedAnnihilateDirection N (fun _ => 1) s ψ) p +
        (-(w s : ℂ)) *
          twistedAnnihilateDirection N (fun _ => 1) s
            (twistedCreateDirection N (fun _ => 1) r ψ) p =
        (-(w s : ℂ)) *
          (if r = s then
            twistedForwardSite N (fun _ => 1) r
              (twistedBackwardSite N (fun _ => 1) s ψ)
          else 0) p := by
    intro r s
    rw [twistedCreate_of_annihilate,
      twistedAnnihilate_of_create N (fun _ => 1) hne]
    let f := twistedForwardSite N (fun _ => 1) r
      (twistedBackwardSite N (fun _ => 1) s ψ)
    have happ := congrFun
      (create_annihilate_deltaC N r s f) p
    simp only [Pi.add_apply] at happ
    calc
      (-(w s : ℂ)) *
          createActionC N r (annihilateActionC N s f) p +
        (-(w s : ℂ)) *
          annihilateActionC N s (createActionC N r f) p =
        (-(w s : ℂ)) *
          (createActionC N r (annihilateActionC N s f) p +
            annihilateActionC N s (createActionC N r f) p) := by ring
      _ = (-(w s : ℂ)) *
          ((if r = s then f else 0) p) := by rw [happ]
      _ = (-(w s : ℂ)) *
          (if r = s then f else 0) p := by by_cases hrs : r = s <;> simp [hrs]
  have hjoined :
      (∑ r : Role, ∑ s : Role,
          ((-(w s : ℂ)) *
              twistedCreateDirection N (fun _ => 1) r
                (twistedAnnihilateDirection N (fun _ => 1) s ψ) p +
            (-(w s : ℂ)) *
              twistedAnnihilateDirection N (fun _ => 1) s
                (twistedCreateDirection N (fun _ => 1) r ψ) p)) =
        ∑ r : Role, ∑ s : Role,
          (-(w s : ℂ)) *
            (if r = s then
              twistedForwardSite N (fun _ => 1) r
                (twistedBackwardSite N (fun _ => 1) s ψ)
            else 0) p := by
    refine Finset.sum_congr rfl ?_
    intro r _
    refine Finset.sum_congr rfl ?_
    intro s _
    exact hpair r s
  rw [hjoined]
  have hdiag :
      (∑ r : Role, ∑ s : Role,
          (-(w s : ℂ)) *
            (if r = s then
              twistedForwardSite N (fun _ => 1) r
                (twistedBackwardSite N (fun _ => 1) s ψ)
            else 0) p) =
        ∑ r : Role, (-(w r : ℂ)) *
          twistedForwardSite N (fun _ => 1) r
            (twistedBackwardSite N (fun _ => 1) r ψ) p := by
    refine Finset.sum_congr rfl ?_
    intro r _
    rw [Finset.sum_eq_single r]
    · simp
    · intro s _ hrs
      simp [Ne.symm hrs]
    · simp
  rw [hdiag]
  have hcomm : ∀ r : Role,
      twistedForwardSite N (fun _ => 1) r
          (twistedBackwardSite N (fun _ => 1) r ψ) =
        twistedBackwardSite N (fun _ => 1) r
          (twistedForwardSite N (fun _ => 1) r ψ) := by
    intro r
    exact twistedForwardSite_backwardSite_comm N (fun _ => 1) hne r r ψ
  simp_rw [hcomm]
  change (∑ r : Role, (-(w r : ℂ)) *
      twistedBackwardSite N (fun _ => 1) r
        (twistedForwardSite N (fun _ => 1) r ψ) p) =
    roleWeightedArchiveDifferenceOperator N w ψ p
  unfold roleWeightedArchiveDifferenceOperator roleWeightedArchiveDifferenceLaplacian
  simp only [twistedBackwardSite, twistedForwardSite]
  refine Finset.sum_congr rfl ?_
  intro r _
  ring

theorem roleWeightedArchiveCARDirac_square (N : ℕ) (w : Role → ℝ)
    (ψ : ArchiveCochainC N) :
    roleWeightedArchiveCARDirac N w
        (roleWeightedArchiveCARDirac N w ψ) =
      roleWeightedArchiveDifferenceOperator N w ψ := by
  unfold roleWeightedArchiveCARDirac
  rw [dTwisted_add, roleWeightedArchiveCodifferential_add,
    dTwisted_sq, roleWeightedArchiveCodifferential_square]
  simpa only [Pi.zero_apply, zero_add, add_zero] using
    roleWeightedArchiveCodifferential_cross N w ψ

/-- With the source's declared role signs, the actual first-order CAR square
is the all-size signed scalar difference operator from the companion module. -/
theorem archiveLorentzianCARDirac_square (N : ℕ) (ψ : ArchiveCochainC N) :
    archiveLorentzianCARDirac N (archiveLorentzianCARDirac N ψ) =
      roleWeightedArchiveDifferenceOperator N roleLorentzSign ψ := by
  exact roleWeightedArchiveCARDirac_square N roleLorentzSign ψ

/-- On every product-cycle character and arbitrary Fock profile, the actual
role-signed first-order CAR operator squares to the Eq. (5) Fourier symbol.
The claim is about the composed square; it does not assert that the first-order
operator preserves a single character profile. -/
theorem archiveLorentzianCARDirac_square_fourier_mode (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (v : ArchiveFockState → ℂ) :
    archiveLorentzianCARDirac N
        (archiveLorentzianCARDirac N (archiveFourierFockMode N k v)) =
      fun p => Complex.ofReal (archiveLorentzianFourierSymbol N k) *
        archiveFourierFockMode N k v p := by
  rw [archiveLorentzianCARDirac_square N
    (archiveFourierFockMode N k v)]
  exact archiveLorentzianDifferenceOperator_fourier_mode N k v

end

end D0.Geometry
