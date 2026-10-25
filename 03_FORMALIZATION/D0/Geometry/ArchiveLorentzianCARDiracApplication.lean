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
all-period Fourier action of the first-order operator on every
sixteen-component Fock fibre and the eigenvalue of its square. It remains a
conditional operator theorem for the explicit role-sign assignment, not a
physical source-selection result.
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
The claim is about the composed square; the first-order operator generally
updates the internal Fock profile instead of acting by a scalar. -/
theorem archiveLorentzianCARDirac_square_fourier_mode (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (v : ArchiveFockState → ℂ) :
    archiveLorentzianCARDirac N
        (archiveLorentzianCARDirac N (archiveFourierFockMode N k v)) =
      fun p => Complex.ofReal (archiveLorentzianFourierSymbol N k) *
        archiveFourierFockMode N k v p := by
  rw [archiveLorentzianCARDirac_square N
    (archiveFourierFockMode N k v)]
  exact archiveLorentzianDifferenceOperator_fourier_mode N k v

/-! ## Exact first-order action on one Fourier fibre

The second-order symbol alone does not describe the first-order operator on a
Fourier mode: creation and annihilation change the internal Fock coefficient.
The definitions below retain that sixteen-component profile and prove that
the first-order operator preserves the corresponding Fourier subspace.
-/

/-- The forward shift multiplier of a product character in one archive role. -/
noncomputable def archiveFourierForwardMultiplier (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (r : Role) : ℂ :=
  (archiveFibers N : ℂ) * (FiniteCycleFourier.cycleChar (k r) 1 - 1)

/-- The backward shift multiplier of a product character in one archive role. -/
noncomputable def archiveFourierBackwardMultiplier (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (r : Role) : ℂ :=
  (archiveFibers N : ℂ) * (1 - FiniteCycleFourier.cycleChar (k r) (-1))

/-- Creation on the sixteen-component Fock coefficient at fixed momentum,
represented by the shared finite matrix action. -/
def archiveFourierCreateProfileLinear (r : Role) :
    (ArchiveFockState → ℂ) →ₗ[ℂ] (ArchiveFockState → ℂ) :=
  carMatrixEnd (fun bra ket => (carCreate r bra ket : ℂ))

/-- Annihilation on the sixteen-component Fock coefficient, represented by the
same shared finite matrix action. -/
def archiveFourierAnnihilateProfileLinear (r : Role) :
    (ArchiveFockState → ℂ) →ₗ[ℂ] (ArchiveFockState → ℂ) :=
  carMatrixEnd (fun bra ket => (carAnnihilate r bra ket : ℂ))

/-- Function-valued compatibility view of the creation matrix action. -/
def archiveFourierCreateProfile (r : Role) (v : ArchiveFockState → ℂ) :
    ArchiveFockState → ℂ :=
  archiveFourierCreateProfileLinear r v

/-- Function-valued compatibility view of the annihilation matrix action. -/
def archiveFourierAnnihilateProfile (r : Role) (v : ArchiveFockState → ℂ) :
    ArchiveFockState → ℂ :=
  archiveFourierAnnihilateProfileLinear r v

/-- Exact finite-dimensional CAR action induced on one archive Fourier fibre.
The source weights act only on the backward annihilation term. -/
def roleWeightedArchiveFourierFockAction (N : ℕ) (w : Role → ℝ)
    (k : Role → ZMod (archiveFibers N)) (v : ArchiveFockState → ℂ) :
    ArchiveFockState → ℂ :=
  fun S => ∑ r : Role, (
    archiveFourierForwardMultiplier N k r * archiveFourierCreateProfile r v S -
      (w r : ℂ) * archiveFourierBackwardMultiplier N k r *
        archiveFourierAnnihilateProfile r v S)

/-- The same Fourier-fibre CAR action as an endomorphism of the finite
sixteen-component complex profile space. This is the typed operator API used
for composition and matrix-level applications. -/
noncomputable def roleWeightedArchiveFourierFockActionLinear (N : ℕ)
    (w : Role → ℝ) (k : Role → ZMod (archiveFibers N)) :
    (ArchiveFockState → ℂ) →ₗ[ℂ] (ArchiveFockState → ℂ) :=
  ∑ r : Role,
    (archiveFourierForwardMultiplier N k r • archiveFourierCreateProfileLinear r -
      ((w r : ℂ) * archiveFourierBackwardMultiplier N k r) •
        archiveFourierAnnihilateProfileLinear r)

/-- Applying the typed Fourier-fibre operator recovers the established
function-valued compatibility view exactly. -/
theorem roleWeightedArchiveFourierFockActionLinear_apply (N : ℕ)
    (w : Role → ℝ) (k : Role → ZMod (archiveFibers N))
    (v : ArchiveFockState → ℂ) :
    roleWeightedArchiveFourierFockActionLinear N w k v =
      roleWeightedArchiveFourierFockAction N w k v := by
  funext S
  simp [roleWeightedArchiveFourierFockActionLinear,
    roleWeightedArchiveFourierFockAction,
    archiveFourierCreateProfile, archiveFourierAnnihilateProfile,
    archiveFourierCreateProfileLinear, archiveFourierAnnihilateProfileLinear,
    carMatrixEnd]

private theorem archiveFourierCharacter_zero (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) :
    FiniteCycleFourier.piCycleChar k (0 : ArchiveRolePhaseGroup N) = 1 := by
  unfold FiniteCycleFourier.piCycleChar
  simp [FiniteCycleFourier.cycleChar_zero_right]

private theorem archiveFourierCharacter_roleStep (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (r : Role) :
    FiniteCycleFourier.piCycleChar k (roleStep N r) =
      FiniteCycleFourier.cycleChar (k r) 1 := by
  classical
  unfold FiniteCycleFourier.piCycleChar roleStep
  rw [Finset.prod_eq_single r]
  · simp
  · intro s _ hsr
    simp [hsr, FiniteCycleFourier.cycleChar_zero_right]
  · simp

private theorem archiveFourierCharacter_negRoleStep (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (r : Role) :
    FiniteCycleFourier.piCycleChar k (-(roleStep N r)) =
      FiniteCycleFourier.cycleChar (k r) (-1) := by
  classical
  unfold FiniteCycleFourier.piCycleChar roleStep
  rw [Finset.prod_eq_single r]
  · simp
  · intro s _ hsr
    simp [hsr, FiniteCycleFourier.cycleChar_zero_right]
  · simp

private theorem archiveFourierCharacter_forwardShift (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (r : Role)
    (x : ArchiveRolePhaseGroup N) :
    FiniteCycleFourier.piCycleChar k (roleTranslatePlus N r x) =
      FiniteCycleFourier.cycleChar (k r) 1 * FiniteCycleFourier.piCycleChar k x := by
  rw [roleTranslatePlus_apply, FiniteCycleFourier.piCycleChar_add_right,
    archiveFourierCharacter_roleStep]
  ring

private theorem archiveFourierCharacter_backwardShift (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (r : Role)
    (x : ArchiveRolePhaseGroup N) :
    FiniteCycleFourier.piCycleChar k (roleTranslateMinus N r x) =
      FiniteCycleFourier.cycleChar (k r) (-1) * FiniteCycleFourier.piCycleChar k x := by
  rw [roleTranslateMinus_apply, show x - roleStep N r =
      x + -(roleStep N r) by rw [sub_eq_add_neg],
    FiniteCycleFourier.piCycleChar_add_right,
    archiveFourierCharacter_negRoleStep]
  ring

private theorem twistedRoleShiftInv_one_archive (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShiftInv N r 1 f = fun x => f (roleTranslateMinus N r x) := by
  funext x
  simp [twistedRoleShiftInv]

private theorem archiveFourierCharacter_forwardDifference (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (r : Role) :
    twistedForwardDifference N r 1 (FiniteCycleFourier.piCycleChar k) =
      fun x => archiveFourierForwardMultiplier N k r *
        FiniteCycleFourier.piCycleChar k x := by
  funext x
  rw [twistedForward_one, archiveFourierCharacter_forwardShift]
  unfold archiveFourierForwardMultiplier
  ring

private theorem archiveFourierCharacter_backwardDifference (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (r : Role) :
    twistedBackwardDifference N r 1 (FiniteCycleFourier.piCycleChar k) =
      fun x => archiveFourierBackwardMultiplier N k r *
        FiniteCycleFourier.piCycleChar k x := by
  funext x
  change (archiveFibers N : ℂ) *
      (FiniteCycleFourier.piCycleChar k x -
        twistedRoleShiftInv N r 1 (FiniteCycleFourier.piCycleChar k) x) = _
  rw [twistedRoleShiftInv_one_archive]
  change (archiveFibers N : ℂ) *
      (FiniteCycleFourier.piCycleChar k x -
        FiniteCycleFourier.piCycleChar k (roleTranslateMinus N r x)) = _
  rw [archiveFourierCharacter_backwardShift]
  unfold archiveFourierBackwardMultiplier
  ring

/-- The archive forward creation term acts within a single Fourier fibre and
updates only its Fock profile. -/
theorem twistedCreateDirection_fourier_mode (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (r : Role)
    (v : ArchiveFockState → ℂ) :
    twistedCreateDirection N (fun _ => 1) r (archiveFourierFockMode N k v) =
      archiveFourierFockMode N k
        (fun S => archiveFourierForwardMultiplier N k r *
          archiveFourierCreateProfile r v S) := by
  classical
  funext p
  change (∑ ket, (carCreate r p.2 ket : ℂ) *
      twistedForwardDifference N r 1
        (fun x => v ket * FiniteCycleFourier.piCycleChar k x) p.1) = _
  have hdiff (ket : ArchiveFockState) :
      twistedForwardDifference N r 1
          (fun x => v ket * FiniteCycleFourier.piCycleChar k x) p.1 =
        v ket * archiveFourierForwardMultiplier N k r *
          FiniteCycleFourier.piCycleChar k p.1 := by
    calc
      twistedForwardDifference N r 1
          (fun x => v ket * FiniteCycleFourier.piCycleChar k x) p.1 =
        v ket * twistedForwardDifference N r 1
          (FiniteCycleFourier.piCycleChar k) p.1 := by
            rw [twistedForwardDifference_const_mul]
      _ = v ket * (archiveFourierForwardMultiplier N k r *
          FiniteCycleFourier.piCycleChar k p.1) := by
            rw [archiveFourierCharacter_forwardDifference]
      _ = v ket * archiveFourierForwardMultiplier N k r *
          FiniteCycleFourier.piCycleChar k p.1 := by ring
  simp_rw [hdiff]
  unfold archiveFourierFockMode archiveFourierCreateProfile
    archiveFourierCreateProfileLinear carMatrixEnd
  calc
    (∑ ket, (carCreate r p.2 ket : ℂ) *
        (v ket * archiveFourierForwardMultiplier N k r *
          FiniteCycleFourier.piCycleChar k p.1)) =
        ∑ ket, ((carCreate r p.2 ket : ℂ) * v ket) *
          (archiveFourierForwardMultiplier N k r *
            FiniteCycleFourier.piCycleChar k p.1) := by
              apply Finset.sum_congr rfl
              intro ket _
              ring
    _ = (∑ ket, (carCreate r p.2 ket : ℂ) * v ket) *
          (archiveFourierForwardMultiplier N k r *
            FiniteCycleFourier.piCycleChar k p.1) := by rw [← Finset.sum_mul]
    _ = (archiveFourierForwardMultiplier N k r *
          (∑ ket, (carCreate r p.2 ket : ℂ) * v ket)) *
          FiniteCycleFourier.piCycleChar k p.1 := by ring

/-- The archive backward annihilation term acts within a single Fourier fibre
and updates only its Fock profile. -/
theorem twistedAnnihilateDirection_fourier_mode (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (r : Role)
    (v : ArchiveFockState → ℂ) :
    twistedAnnihilateDirection N (fun _ => 1) r (archiveFourierFockMode N k v) =
      archiveFourierFockMode N k
        (fun S => archiveFourierBackwardMultiplier N k r *
          archiveFourierAnnihilateProfile r v S) := by
  classical
  funext p
  change (∑ ket, (carAnnihilate r p.2 ket : ℂ) *
      twistedBackwardDifference N r 1
        (fun x => v ket * FiniteCycleFourier.piCycleChar k x) p.1) = _
  have hdiff (ket : ArchiveFockState) :
      twistedBackwardDifference N r 1
          (fun x => v ket * FiniteCycleFourier.piCycleChar k x) p.1 =
        v ket * archiveFourierBackwardMultiplier N k r *
          FiniteCycleFourier.piCycleChar k p.1 := by
    calc
      twistedBackwardDifference N r 1
          (fun x => v ket * FiniteCycleFourier.piCycleChar k x) p.1 =
        v ket * twistedBackwardDifference N r 1
          (FiniteCycleFourier.piCycleChar k) p.1 := by
            rw [twistedBackwardDifference_const_mul]
      _ = v ket * (archiveFourierBackwardMultiplier N k r *
          FiniteCycleFourier.piCycleChar k p.1) := by
            rw [archiveFourierCharacter_backwardDifference]
      _ = v ket * archiveFourierBackwardMultiplier N k r *
          FiniteCycleFourier.piCycleChar k p.1 := by ring
  simp_rw [hdiff]
  unfold archiveFourierFockMode archiveFourierAnnihilateProfile
    archiveFourierAnnihilateProfileLinear carMatrixEnd
  calc
    (∑ ket, (carAnnihilate r p.2 ket : ℂ) *
        (v ket * archiveFourierBackwardMultiplier N k r *
          FiniteCycleFourier.piCycleChar k p.1)) =
        ∑ ket, ((carAnnihilate r p.2 ket : ℂ) * v ket) *
          (archiveFourierBackwardMultiplier N k r *
            FiniteCycleFourier.piCycleChar k p.1) := by
              apply Finset.sum_congr rfl
              intro ket _
              ring
    _ = (∑ ket, (carAnnihilate r p.2 ket : ℂ) * v ket) *
          (archiveFourierBackwardMultiplier N k r *
            FiniteCycleFourier.piCycleChar k p.1) := by rw [← Finset.sum_mul]
    _ = (archiveFourierBackwardMultiplier N k r *
          (∑ ket, (carAnnihilate r p.2 ket : ℂ) * v ket)) *
          FiniteCycleFourier.piCycleChar k p.1 := by ring

/-- The full role-weighted first-order operator leaves each product Fourier
subspace invariant. Its action is the displayed finite CAR map on the Fock
profile, not scalar multiplication on an arbitrary profile. -/
theorem roleWeightedArchiveCARDirac_fourier_mode (N : ℕ)
    (w : Role → ℝ) (k : Role → ZMod (archiveFibers N))
    (v : ArchiveFockState → ℂ) :
    roleWeightedArchiveCARDirac N w (archiveFourierFockMode N k v) =
      archiveFourierFockMode N k (roleWeightedArchiveFourierFockAction N w k v) := by
  classical
  funext p
  unfold roleWeightedArchiveCARDirac dTwisted roleWeightedArchiveCodifferential
    roleWeightedArchiveFourierFockAction
  simp only [Pi.add_apply, Finset.sum_apply]
  simp_rw [twistedCreateDirection_fourier_mode,
    twistedAnnihilateDirection_fourier_mode]
  simp only [Pi.smul_apply, smul_eq_mul, archiveFourierFockMode]
  calc
    (∑ r : Role, archiveFourierForwardMultiplier N k r *
        archiveFourierCreateProfile r v p.2 *
          FiniteCycleFourier.piCycleChar k p.1) +
      ∑ r : Role, -(w r : ℂ) *
        (archiveFourierBackwardMultiplier N k r *
          archiveFourierAnnihilateProfile r v p.2 *
            FiniteCycleFourier.piCycleChar k p.1) =
      ∑ r : Role, (
        (archiveFourierForwardMultiplier N k r *
            archiveFourierCreateProfile r v p.2 *
            FiniteCycleFourier.piCycleChar k p.1) +
          (-(w r : ℂ) * (archiveFourierBackwardMultiplier N k r *
            archiveFourierAnnihilateProfile r v p.2 *
            FiniteCycleFourier.piCycleChar k p.1))) := by
              rw [← Finset.sum_add_distrib]
    _ = ∑ r : Role,
          ((archiveFourierForwardMultiplier N k r *
              archiveFourierCreateProfile r v p.2 -
            (w r : ℂ) * archiveFourierBackwardMultiplier N k r *
              archiveFourierAnnihilateProfile r v p.2) *
            FiniteCycleFourier.piCycleChar k p.1) := by
              apply Finset.sum_congr rfl
              intro r _
              ring
    _ = (∑ r : Role, (
          archiveFourierForwardMultiplier N k r *
              archiveFourierCreateProfile r v p.2 -
            (w r : ℂ) * archiveFourierBackwardMultiplier N k r *
              archiveFourierAnnihilateProfile r v p.2)) *
            FiniteCycleFourier.piCycleChar k p.1 := by rw [← Finset.sum_mul]

/-- The explicit repository Lorentz-sign assignment specializes the generic
first-order fibre action. This is an operator specialization, not a proof that
the assignment is physically selected. -/
theorem archiveLorentzianCARDirac_fourier_mode (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (v : ArchiveFockState → ℂ) :
    archiveLorentzianCARDirac N (archiveFourierFockMode N k v) =
      archiveFourierFockMode N k
        (roleWeightedArchiveFourierFockAction N roleLorentzSign k v) := by
  exact roleWeightedArchiveCARDirac_fourier_mode N roleLorentzSign k v

/-- The generic weighted second-order operator acts on the actual site × Fock
carrier with its role-weighted scalar Fourier symbol. -/
theorem roleWeightedArchiveDifferenceOperator_fourier_mode (N : ℕ)
    (w : Role → ℝ) (k : Role → ZMod (archiveFibers N))
    (v : ArchiveFockState → ℂ) :
    roleWeightedArchiveDifferenceOperator N w (archiveFourierFockMode N k v) =
      fun p => Complex.ofReal (roleWeightedArchiveFourierSymbol N w k) *
        archiveFourierFockMode N k v p := by
  funext p
  change roleWeightedArchiveDifferenceLaplacian N w
      (fun x => v p.2 * FiniteCycleFourier.piCycleChar k x) p.1 = _
  rw [roleWeightedArchiveDifferenceLaplacian_const_mul]
  change v p.2 * roleWeightedArchiveDifferenceLaplacian N w
      (FiniteCycleFourier.piCycleChar k) p.1 = _
  rw [roleWeightedArchiveDifferenceLaplacian_fourier]
  simp only [archiveFourierFockMode]
  ring

/-- The induced finite CAR map has the same signed second-order Fourier symbol
as the full archive operator. This is an operator identity on the Fock fibre;
the role weights remain explicit inputs. -/
theorem roleWeightedArchiveFourierFockAction_square (N : ℕ)
    (w : Role → ℝ) (k : Role → ZMod (archiveFibers N))
    (v : ArchiveFockState → ℂ) :
    roleWeightedArchiveFourierFockAction N w k
        (roleWeightedArchiveFourierFockAction N w k v) =
      fun S => Complex.ofReal (roleWeightedArchiveFourierSymbol N w k) * v S := by
  apply archiveFourierFockMode_injective N k
  calc
    archiveFourierFockMode N k
        (roleWeightedArchiveFourierFockAction N w k
          (roleWeightedArchiveFourierFockAction N w k v)) =
        roleWeightedArchiveCARDirac N w
          (roleWeightedArchiveCARDirac N w (archiveFourierFockMode N k v)) := by
            rw [← roleWeightedArchiveCARDirac_fourier_mode,
              ← roleWeightedArchiveCARDirac_fourier_mode]
    _ = roleWeightedArchiveDifferenceOperator N w
          (archiveFourierFockMode N k v) :=
            roleWeightedArchiveCARDirac_square N w (archiveFourierFockMode N k v)
    _ = fun p => Complex.ofReal (roleWeightedArchiveFourierSymbol N w k) *
          archiveFourierFockMode N k v p :=
            roleWeightedArchiveDifferenceOperator_fourier_mode N w k v
    _ = archiveFourierFockMode N k
          (fun S => Complex.ofReal (roleWeightedArchiveFourierSymbol N w k) * v S) := by
            funext p
            simp [archiveFourierFockMode]
            ring

/-- As a genuine finite-dimensional linear operator, the Fourier-fibre CAR
map composes with itself to the scalar Eq. (5) symbol. -/
theorem roleWeightedArchiveFourierFockActionLinear_square (N : ℕ)
    (w : Role → ℝ) (k : Role → ZMod (archiveFibers N)) :
    (roleWeightedArchiveFourierFockActionLinear N w k).comp
        (roleWeightedArchiveFourierFockActionLinear N w k) =
      (Complex.ofReal (roleWeightedArchiveFourierSymbol N w k)) • LinearMap.id := by
  apply LinearMap.ext
  intro v
  funext S
  change roleWeightedArchiveFourierFockActionLinear N w k
      (roleWeightedArchiveFourierFockActionLinear N w k v) S = _
  rw [roleWeightedArchiveFourierFockActionLinear_apply,
    roleWeightedArchiveFourierFockActionLinear_apply,
    roleWeightedArchiveFourierFockAction_square]
  simp [LinearMap.id_apply, Pi.smul_apply, smul_eq_mul]

/-- With the repository role signs, the induced Fock-fibre map squares to the
Eq. (5) symbol on every profile and every archive Fourier momentum. -/
theorem archiveLorentzianCARFourierFockAction_square (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (v : ArchiveFockState → ℂ) :
    roleWeightedArchiveFourierFockAction N roleLorentzSign k
        (roleWeightedArchiveFourierFockAction N roleLorentzSign k v) =
      fun S => Complex.ofReal (archiveLorentzianFourierSymbol N k) * v S := by
  rw [roleWeightedArchiveFourierFockAction_square,
    roleWeightedArchiveFourierSymbol_lorentzian]

end

end D0.Geometry
