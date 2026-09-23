import Mathlib.Data.Complex.Basic
import Mathlib.Tactic
import D0.Geometry.ArchiveHodgeCARDirac
import D0.Geometry.ArchiveTwistedRoleDifference

/-!
# Generic twisted Hodge / CAR operator

Parallel complex carrier. The real operator `hodgeCarDirac` is not modified.

For a role-indexed scalar seam holonomy `H`,

`d_H = ∑_r c_r† ∇_{r,H(r)}⁺`,
`d_H† = -∑_r c_r ∇_{r,H(r)}⁻`,
`D_H = d_H + d_H†`.

The square reuses the owned CAR anticommutators. Differences commute because the
holonomies are scalars. No value of `π₀` is selected, and no canonical
`H_π₀` is defined.
-/

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

abbrev ArchiveCochainC (N : ℕ) := ArchiveCochainBasis N → ℂ

/-- Data a later specialization must supply. It is not populated from `π₀`. -/
structure ScalarSeamHolonomy (N : ℕ) where
  holonomy : Role → ℂ
  unitary : ∀ r, star (holonomy r) * holonomy r = 1
  support : Set Role
  support_spec : ∀ r, r ∉ support → holonomy r = 1

def ScalarSeamHolonomy.untwisted {N : ℕ} (H : ScalarSeamHolonomy N) : Prop :=
  ∀ r, H.holonomy r = 1

def cochainPairingC (N : ℕ) (ψ φ : ArchiveCochainC N) : ℂ :=
  ∑ x, ∑ s, star (ψ (x, s)) * φ (x, s)

def HomogeneousCochainC (N k : ℕ) (ψ : ArchiveCochainC N) : Prop :=
  ∀ x S, fockDegree S ≠ k → ψ (x, S) = 0

def parityCochainC (N : ℕ) (ψ : ArchiveCochainC N) : ArchiveCochainC N :=
  fun p => (fockParitySign p.2 : ℂ) * ψ p

/-! ## Complex CAR actions -/

def createActionC (N : ℕ) (r : Role) (ψ : ArchiveCochainC N) : ArchiveCochainC N :=
  fun p => ∑ ket, (carCreate r p.2 ket : ℂ) * ψ (p.1, ket)

def annihilateActionC (N : ℕ) (r : Role) (ψ : ArchiveCochainC N) : ArchiveCochainC N :=
  fun p => ∑ ket, (carAnnihilate r p.2 ket : ℂ) * ψ (p.1, ket)

theorem carCreate_anticomm_complex (r s : Role) (bra ket : ArchiveFockState) :
    (∑ mid : ArchiveFockState, (carCreate r bra mid : ℂ) * (carCreate s mid ket : ℂ)) +
      (∑ mid : ArchiveFockState, (carCreate s bra mid : ℂ) * (carCreate r mid ket : ℂ)) = 0 := by
  have h := car_create_anticommutator r s bra ket
  unfold anticommutator at h
  simpa [Complex.ofReal_add, Complex.ofReal_sum, Complex.ofReal_mul] using
    congrArg (fun z : ℝ => (z : ℂ)) h

theorem carAnnihilate_anticomm_complex (r s : Role) (bra ket : ArchiveFockState) :
    (∑ mid : ArchiveFockState, (carAnnihilate r bra mid : ℂ) * (carAnnihilate s mid ket : ℂ)) +
      (∑ mid : ArchiveFockState,
        (carAnnihilate s bra mid : ℂ) * (carAnnihilate r mid ket : ℂ)) = 0 := by
  have h := car_annihilate_anticommutator r s bra ket
  unfold anticommutator at h
  simpa [Complex.ofReal_add, Complex.ofReal_sum, Complex.ofReal_mul] using
    congrArg (fun z : ℝ => (z : ℂ)) h

theorem carMixed_create_first_complex (r s : Role) (bra ket : ArchiveFockState) :
    (∑ mid : ArchiveFockState, (carCreate r bra mid : ℂ) * (carAnnihilate s mid ket : ℂ)) +
      (∑ mid : ArchiveFockState,
        (carAnnihilate s bra mid : ℂ) * (carCreate r mid ket : ℂ)) =
        (roleDelta r s : ℂ) * (fockIdentity bra ket : ℂ) := by
  have h := car_mixed_anticommutator_create_first r s bra ket
  unfold anticommutator at h
  simpa [Complex.ofReal_add, Complex.ofReal_sum, Complex.ofReal_mul] using
    congrArg (fun z : ℝ => (z : ℂ)) h

theorem fibreComposeC {N : ℕ}
    (M Nmat : ArchiveFockState → ArchiveFockState → ℂ)
    (ψ : ArchiveCochainC N) (x : ArchiveRolePhaseGroup N) (bra : ArchiveFockState) :
    (∑ mid, M bra mid * ∑ ket, Nmat mid ket * ψ (x, ket)) =
      ∑ ket, (∑ mid, M bra mid * Nmat mid ket) * ψ (x, ket) := by
  classical
  calc
    (∑ mid, M bra mid * ∑ ket, Nmat mid ket * ψ (x, ket)) =
        ∑ mid, ∑ ket, M bra mid * (Nmat mid ket * ψ (x, ket)) := by
          apply Finset.sum_congr rfl
          intro mid _
          rw [Finset.mul_sum]
    _ = ∑ ket, ∑ mid, M bra mid * Nmat mid ket * ψ (x, ket) := by
          rw [Finset.sum_comm]
          apply Finset.sum_congr rfl
          intro ket _
          apply Finset.sum_congr rfl
          intro mid _
          ring
    _ = ∑ ket, (∑ mid, M bra mid * Nmat mid ket) * ψ (x, ket) := by
          apply Finset.sum_congr rfl
          intro ket _
          rw [← Finset.sum_mul]

theorem createActionC_comp_apply (N : ℕ) (r s : Role)
    (ψ : ArchiveCochainC N) (p : ArchiveCochainBasis N) :
    createActionC N r (createActionC N s ψ) p =
      ∑ ket, (∑ mid, (carCreate r p.2 mid : ℂ) * (carCreate s mid ket : ℂ)) *
        ψ (p.1, ket) := by
  classical
  unfold createActionC
  exact fibreComposeC (fun a b => (carCreate r a b : ℂ))
    (fun a b => (carCreate s a b : ℂ)) ψ p.1 p.2

theorem annihilateActionC_comp_apply (N : ℕ) (r s : Role)
    (ψ : ArchiveCochainC N) (p : ArchiveCochainBasis N) :
    annihilateActionC N r (annihilateActionC N s ψ) p =
      ∑ ket, (∑ mid, (carAnnihilate r p.2 mid : ℂ) * (carAnnihilate s mid ket : ℂ)) *
        ψ (p.1, ket) := by
  classical
  unfold annihilateActionC
  exact fibreComposeC (fun a b => (carAnnihilate r a b : ℂ))
    (fun a b => (carAnnihilate s a b : ℂ)) ψ p.1 p.2

theorem create_annihilate_comp_apply (N : ℕ) (r s : Role)
    (ψ : ArchiveCochainC N) (p : ArchiveCochainBasis N) :
    createActionC N r (annihilateActionC N s ψ) p =
      ∑ ket, (∑ mid, (carCreate r p.2 mid : ℂ) * (carAnnihilate s mid ket : ℂ)) *
        ψ (p.1, ket) := by
  classical
  unfold createActionC annihilateActionC
  exact fibreComposeC (fun a b => (carCreate r a b : ℂ))
    (fun a b => (carAnnihilate s a b : ℂ)) ψ p.1 p.2

theorem annihilate_create_comp_apply (N : ℕ) (r s : Role)
    (ψ : ArchiveCochainC N) (p : ArchiveCochainBasis N) :
    annihilateActionC N s (createActionC N r ψ) p =
      ∑ ket, (∑ mid, (carAnnihilate s p.2 mid : ℂ) * (carCreate r mid ket : ℂ)) *
        ψ (p.1, ket) := by
  classical
  unfold createActionC annihilateActionC
  exact fibreComposeC (fun a b => (carAnnihilate s a b : ℂ))
    (fun a b => (carCreate r a b : ℂ)) ψ p.1 p.2

theorem createActionC_anticommute (N : ℕ) (r s : Role) (ψ : ArchiveCochainC N) :
    createActionC N r (createActionC N s ψ) +
      createActionC N s (createActionC N r ψ) = 0 := by
  classical
  funext p
  simp only [Pi.add_apply, Pi.zero_apply]
  rw [createActionC_comp_apply, createActionC_comp_apply, ← Finset.sum_add_distrib]
  apply Finset.sum_eq_zero
  intro ket _
  rw [← add_mul, carCreate_anticomm_complex]
  simp

theorem annihilateActionC_anticommute (N : ℕ) (r s : Role) (ψ : ArchiveCochainC N) :
    annihilateActionC N r (annihilateActionC N s ψ) +
      annihilateActionC N s (annihilateActionC N r ψ) = 0 := by
  classical
  funext p
  simp only [Pi.add_apply, Pi.zero_apply]
  rw [annihilateActionC_comp_apply, annihilateActionC_comp_apply, ← Finset.sum_add_distrib]
  apply Finset.sum_eq_zero
  intro ket _
  rw [← add_mul, carAnnihilate_anticomm_complex]
  simp

theorem create_annihilate_deltaC (N : ℕ) (r s : Role) (ψ : ArchiveCochainC N) :
    createActionC N r (annihilateActionC N s ψ) +
      annihilateActionC N s (createActionC N r ψ) =
        if r = s then ψ else 0 := by
  classical
  by_cases hrs : r = s
  · subst hrs
    funext p
    simp only [Pi.add_apply, if_true]
    rw [create_annihilate_comp_apply, annihilate_create_comp_apply, ← Finset.sum_add_distrib]
    rw [Finset.sum_eq_single p.2]
    · rw [← add_mul, carMixed_create_first_complex]
      simp [roleDelta, fockIdentity]
    · intro ket _ hket
      rw [← add_mul, carMixed_create_first_complex, fockIdentity, if_neg (Ne.symm hket)]
      simp [roleDelta]
    · simp
  · funext p
    simp only [Pi.add_apply, Pi.zero_apply, if_neg hrs]
    rw [create_annihilate_comp_apply, annihilate_create_comp_apply, ← Finset.sum_add_distrib]
    apply Finset.sum_eq_zero
    intro ket _
    rw [← add_mul, carMixed_create_first_complex]
    simp [roleDelta, hrs]

/-! ## Twisted sites -/

def twistedForwardSite (N : ℕ) (H : Role → ℂ) (r : Role)
    (ψ : ArchiveCochainC N) : ArchiveCochainC N :=
  fun p => twistedForwardDifference N r (H r) (fun x => ψ (x, p.2)) p.1

def twistedBackwardSite (N : ℕ) (H : Role → ℂ) (r : Role)
    (ψ : ArchiveCochainC N) : ArchiveCochainC N :=
  fun p => twistedBackwardDifference N r (H r) (fun x => ψ (x, p.2)) p.1

theorem twistedForwardDifference_fock_sum (N : ℕ) (r : Role) (h : ℂ)
    (c : ArchiveFockState → ℂ)
    (F : ArchiveFockState → ArchiveRolePhaseGroup N → ℂ) :
    twistedForwardDifference N r h (fun x => ∑ ket, c ket * F ket x) =
      fun x => ∑ ket, c ket * twistedForwardDifference N r h (F ket) x := by
  classical
  funext x
  rw [congrFun (twistedForwardDifference_sum N r h (fun ket y => c ket * F ket y)) x]
  refine Finset.sum_congr rfl ?_
  intro ket _
  exact congrFun (twistedForwardDifference_const_mul N r h (c ket) (F ket)) x

theorem twistedBackwardDifference_fock_sum (N : ℕ) (r : Role) (h : ℂ)
    (c : ArchiveFockState → ℂ)
    (F : ArchiveFockState → ArchiveRolePhaseGroup N → ℂ) :
    twistedBackwardDifference N r h (fun x => ∑ ket, c ket * F ket x) =
      fun x => ∑ ket, c ket * twistedBackwardDifference N r h (F ket) x := by
  classical
  funext x
  rw [congrFun (twistedBackwardDifference_sum N r h (fun ket y => c ket * F ket y)) x]
  refine Finset.sum_congr rfl ?_
  intro ket _
  exact congrFun (twistedBackwardDifference_const_mul N r h (c ket) (F ket)) x

theorem twistedForwardSite_comm (N : ℕ) (H : Role → ℂ) (r s : Role)
    (ψ : ArchiveCochainC N) :
    twistedForwardSite N H r (twistedForwardSite N H s ψ) =
      twistedForwardSite N H s (twistedForwardSite N H r ψ) := by
  funext p
  exact congrFun (twistedForward_family_comm N r s H (fun x => ψ (x, p.2))) p.1

theorem twistedBackwardSite_comm (N : ℕ) (H : Role → ℂ) (r s : Role)
    (ψ : ArchiveCochainC N) :
    twistedBackwardSite N H r (twistedBackwardSite N H s ψ) =
      twistedBackwardSite N H s (twistedBackwardSite N H r ψ) := by
  funext p
  exact congrFun (twistedBackward_family_comm N r s H (fun x => ψ (x, p.2))) p.1

theorem twistedForwardSite_backwardSite_comm (N : ℕ) (H : Role → ℂ)
    (hne : ∀ t, H t ≠ 0) (r s : Role) (ψ : ArchiveCochainC N) :
    twistedForwardSite N H r (twistedBackwardSite N H s ψ) =
      twistedBackwardSite N H s (twistedForwardSite N H r ψ) := by
  funext p
  exact congrFun
    (twistedForward_backward_family_comm N r s H hne (fun x => ψ (x, p.2))) p.1

theorem twistedForwardSite_create_comm (N : ℕ) (H : Role → ℂ) (r s : Role)
    (ψ : ArchiveCochainC N) :
    twistedForwardSite N H r (createActionC N s ψ) =
      createActionC N s (twistedForwardSite N H r ψ) := by
  classical
  funext p
  change
    twistedForwardDifference N r (H r)
        (fun x => ∑ ket, (carCreate s p.2 ket : ℂ) * ψ (x, ket)) p.1 =
      ∑ ket, (carCreate s p.2 ket : ℂ) *
        twistedForwardDifference N r (H r) (fun x => ψ (x, ket)) p.1
  exact congrFun (twistedForwardDifference_fock_sum N r (H r)
    (fun ket => (carCreate s p.2 ket : ℂ)) (fun ket x => ψ (x, ket))) p.1

theorem twistedForwardSite_annihilate_comm (N : ℕ) (H : Role → ℂ) (r s : Role)
    (ψ : ArchiveCochainC N) :
    twistedForwardSite N H r (annihilateActionC N s ψ) =
      annihilateActionC N s (twistedForwardSite N H r ψ) := by
  classical
  funext p
  change
    twistedForwardDifference N r (H r)
        (fun x => ∑ ket, (carAnnihilate s p.2 ket : ℂ) * ψ (x, ket)) p.1 =
      ∑ ket, (carAnnihilate s p.2 ket : ℂ) *
        twistedForwardDifference N r (H r) (fun x => ψ (x, ket)) p.1
  exact congrFun (twistedForwardDifference_fock_sum N r (H r)
    (fun ket => (carAnnihilate s p.2 ket : ℂ)) (fun ket x => ψ (x, ket))) p.1

theorem twistedBackwardSite_create_comm (N : ℕ) (H : Role → ℂ) (r s : Role)
    (ψ : ArchiveCochainC N) :
    twistedBackwardSite N H r (createActionC N s ψ) =
      createActionC N s (twistedBackwardSite N H r ψ) := by
  classical
  funext p
  change
    twistedBackwardDifference N r (H r)
        (fun x => ∑ ket, (carCreate s p.2 ket : ℂ) * ψ (x, ket)) p.1 =
      ∑ ket, (carCreate s p.2 ket : ℂ) *
        twistedBackwardDifference N r (H r) (fun x => ψ (x, ket)) p.1
  exact congrFun (twistedBackwardDifference_fock_sum N r (H r)
    (fun ket => (carCreate s p.2 ket : ℂ)) (fun ket x => ψ (x, ket))) p.1

theorem twistedBackwardSite_annihilate_comm (N : ℕ) (H : Role → ℂ) (r s : Role)
    (ψ : ArchiveCochainC N) :
    twistedBackwardSite N H r (annihilateActionC N s ψ) =
      annihilateActionC N s (twistedBackwardSite N H r ψ) := by
  classical
  funext p
  change
    twistedBackwardDifference N r (H r)
        (fun x => ∑ ket, (carAnnihilate s p.2 ket : ℂ) * ψ (x, ket)) p.1 =
      ∑ ket, (carAnnihilate s p.2 ket : ℂ) *
        twistedBackwardDifference N r (H r) (fun x => ψ (x, ket)) p.1
  exact congrFun (twistedBackwardDifference_fock_sum N r (H r)
    (fun ket => (carAnnihilate s p.2 ket : ℂ)) (fun ket x => ψ (x, ket))) p.1

def twistedCreateDirection (N : ℕ) (H : Role → ℂ) (r : Role)
    (ψ : ArchiveCochainC N) : ArchiveCochainC N :=
  createActionC N r (twistedForwardSite N H r ψ)

def twistedAnnihilateDirection (N : ℕ) (H : Role → ℂ) (r : Role)
    (ψ : ArchiveCochainC N) : ArchiveCochainC N :=
  annihilateActionC N r (twistedBackwardSite N H r ψ)

theorem twistedCreate_anticommute (N : ℕ) (H : Role → ℂ) (r s : Role)
    (ψ : ArchiveCochainC N) :
    twistedCreateDirection N H r (twistedCreateDirection N H s ψ) +
      twistedCreateDirection N H s (twistedCreateDirection N H r ψ) = 0 := by
  change
    createActionC N r (twistedForwardSite N H r
        (createActionC N s (twistedForwardSite N H s ψ))) +
      createActionC N s (twistedForwardSite N H s
        (createActionC N r (twistedForwardSite N H r ψ))) = 0
  rw [twistedForwardSite_create_comm N H r s (twistedForwardSite N H s ψ)]
  rw [twistedForwardSite_create_comm N H s r (twistedForwardSite N H r ψ)]
  rw [twistedForwardSite_comm N H s r ψ]
  exact createActionC_anticommute N r s
    (twistedForwardSite N H r (twistedForwardSite N H s ψ))

theorem twistedAnnihilate_anticommute (N : ℕ) (H : Role → ℂ) (r s : Role)
    (ψ : ArchiveCochainC N) :
    twistedAnnihilateDirection N H r (twistedAnnihilateDirection N H s ψ) +
      twistedAnnihilateDirection N H s (twistedAnnihilateDirection N H r ψ) = 0 := by
  change
    annihilateActionC N r (twistedBackwardSite N H r
        (annihilateActionC N s (twistedBackwardSite N H s ψ))) +
      annihilateActionC N s (twistedBackwardSite N H s
        (annihilateActionC N r (twistedBackwardSite N H r ψ))) = 0
  rw [twistedBackwardSite_annihilate_comm N H r s (twistedBackwardSite N H s ψ)]
  rw [twistedBackwardSite_annihilate_comm N H s r (twistedBackwardSite N H r ψ)]
  rw [twistedBackwardSite_comm N H s r ψ]
  exact annihilateActionC_anticommute N r s
    (twistedBackwardSite N H r (twistedBackwardSite N H s ψ))

theorem twistedCreateDirection_sum {ι : Type*} [Fintype ι] (N : ℕ) (H : Role → ℂ)
    (r : Role) (F : ι → ArchiveCochainC N) :
    twistedCreateDirection N H r (∑ i, F i) =
      ∑ i, twistedCreateDirection N H r (F i) := by
  classical
  funext p
  unfold twistedCreateDirection createActionC twistedForwardSite
  simp only [Finset.sum_apply]
  have hΔ : ∀ ket,
      twistedForwardDifference N r (H r) (fun x => ∑ i, F i (x, ket)) p.1 =
        ∑ i, twistedForwardDifference N r (H r) (fun x => F i (x, ket)) p.1 := by
    intro ket
    exact congrFun (twistedForwardDifference_sum N r (H r) (fun i x => F i (x, ket))) p.1
  simp_rw [hΔ]
  calc
    (∑ ket, (carCreate r p.2 ket : ℂ) *
        ∑ i, twistedForwardDifference N r (H r) (fun x => F i (x, ket)) p.1) =
        ∑ ket, ∑ i, (carCreate r p.2 ket : ℂ) *
          twistedForwardDifference N r (H r) (fun x => F i (x, ket)) p.1 := by
            refine Finset.sum_congr rfl ?_
            intro ket _
            rw [Finset.mul_sum]
    _ = ∑ i, ∑ ket, (carCreate r p.2 ket : ℂ) *
          twistedForwardDifference N r (H r) (fun x => F i (x, ket)) p.1 := by
          rw [Finset.sum_comm]

theorem twistedAnnihilateDirection_sum {ι : Type*} [Fintype ι] (N : ℕ) (H : Role → ℂ)
    (r : Role) (F : ι → ArchiveCochainC N) :
    twistedAnnihilateDirection N H r (∑ i, F i) =
      ∑ i, twistedAnnihilateDirection N H r (F i) := by
  classical
  funext p
  unfold twistedAnnihilateDirection annihilateActionC twistedBackwardSite
  simp only [Finset.sum_apply]
  have hΔ : ∀ ket,
      twistedBackwardDifference N r (H r) (fun x => ∑ i, F i (x, ket)) p.1 =
        ∑ i, twistedBackwardDifference N r (H r) (fun x => F i (x, ket)) p.1 := by
    intro ket
    exact congrFun
      (twistedBackwardDifference_sum N r (H r) (fun i x => F i (x, ket))) p.1
  simp_rw [hΔ]
  calc
    (∑ ket, (carAnnihilate r p.2 ket : ℂ) *
        ∑ i, twistedBackwardDifference N r (H r) (fun x => F i (x, ket)) p.1) =
        ∑ ket, ∑ i, (carAnnihilate r p.2 ket : ℂ) *
          twistedBackwardDifference N r (H r) (fun x => F i (x, ket)) p.1 := by
            refine Finset.sum_congr rfl ?_
            intro ket _
            rw [Finset.mul_sum]
    _ = ∑ i, ∑ ket, (carAnnihilate r p.2 ket : ℂ) *
          twistedBackwardDifference N r (H r) (fun x => F i (x, ket)) p.1 := by
          rw [Finset.sum_comm]

theorem twistedCreateDirection_neg (N : ℕ) (H : Role → ℂ) (r : Role)
    (ψ : ArchiveCochainC N) :
    twistedCreateDirection N H r (-ψ) = -twistedCreateDirection N H r ψ := by
  classical
  funext p
  unfold twistedCreateDirection createActionC twistedForwardSite
  simp only [Pi.neg_apply]
  rw [← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl ?_
  intro ket _
  have hΔ : twistedForwardDifference N r (H r) (fun x => -ψ (x, ket)) p.1 =
      -twistedForwardDifference N r (H r) (fun x => ψ (x, ket)) p.1 := by
    simp only [twistedForwardDifference, twistedRoleShift, Pi.neg_apply]
    ring
  rw [hΔ]
  ring

theorem twistedAnnihilateDirection_neg (N : ℕ) (H : Role → ℂ) (r : Role)
    (ψ : ArchiveCochainC N) :
    twistedAnnihilateDirection N H r (-ψ) = -twistedAnnihilateDirection N H r ψ := by
  classical
  funext p
  unfold twistedAnnihilateDirection annihilateActionC twistedBackwardSite
  simp only [Pi.neg_apply]
  rw [← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl ?_
  intro ket _
  have hΔ : twistedBackwardDifference N r (H r) (fun x => -ψ (x, ket)) p.1 =
      -twistedBackwardDifference N r (H r) (fun x => ψ (x, ket)) p.1 := by
    simp only [twistedBackwardDifference, twistedRoleShiftInv, Pi.neg_apply]
    split_ifs <;> ring
  rw [hΔ]
  ring

/-! ## Dirac operator -/

def dTwisted (N : ℕ) (H : Role → ℂ) (ψ : ArchiveCochainC N) : ArchiveCochainC N :=
  ∑ r : Role, twistedCreateDirection N H r ψ

def dTwistedAdjoint (N : ℕ) (H : Role → ℂ) (ψ : ArchiveCochainC N) : ArchiveCochainC N :=
  ∑ r : Role, -twistedAnnihilateDirection N H r ψ

def hodgeCarDiracTwisted (N : ℕ) (H : Role → ℂ) (ψ : ArchiveCochainC N) : ArchiveCochainC N :=
  dTwisted N H ψ + dTwistedAdjoint N H ψ

def twistedScalarLaplacian (N : ℕ) (H : Role → ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) : ArchiveRolePhaseGroup N → ℂ :=
  fun x => ∑ r : Role,
    -twistedBackwardDifference N r (H r) (twistedForwardDifference N r (H r) f) x

def twistedDifferenceLaplacian (N : ℕ) (H : Role → ℂ)
    (ψ : ArchiveCochainC N) : ArchiveCochainC N :=
  fun p => twistedScalarLaplacian N H (fun x => ψ (x, p.2)) p.1

theorem pairwise_complex_sum_zero {ι : Type*} [Fintype ι]
    (A : ι → ι → ℂ) (h : ∀ i j, A i j + A j i = 0) :
    ∑ i, ∑ j, A i j = 0 := by
  classical
  have hpair : ∑ i, ∑ j, (A i j + A j i) = 0 := by
    apply Finset.sum_eq_zero
    intro i _
    apply Finset.sum_eq_zero
    intro j _
    exact h i j
  have hsplit :
      ∑ i, ∑ j, (A i j + A j i) =
        (∑ i, ∑ j, A i j) + (∑ i, ∑ j, A i j) := by
    simp_rw [Finset.sum_add_distrib]
    congr 1
    rw [Finset.sum_comm]
  have htwice : (∑ i, ∑ j, A i j) + (∑ i, ∑ j, A i j) = 0 := by
    rw [← hsplit, hpair]
  have hmul : (2 : ℂ) * ∑ i, ∑ j, A i j = 0 := by
    simpa [two_mul] using htwice
  exact (mul_eq_zero.mp hmul).resolve_left (by norm_num)

theorem dTwisted_sq (N : ℕ) (H : Role → ℂ) (ψ : ArchiveCochainC N) :
    dTwisted N H (dTwisted N H ψ) = 0 := by
  classical
  have hlin : dTwisted N H (dTwisted N H ψ) =
      ∑ r : Role, ∑ s : Role,
        twistedCreateDirection N H r (twistedCreateDirection N H s ψ) := by
    unfold dTwisted
    refine Finset.sum_congr rfl ?_
    intro r _
    exact twistedCreateDirection_sum N H r (fun s => twistedCreateDirection N H s ψ)
  rw [hlin]
  funext p
  simp only [Finset.sum_apply, Pi.zero_apply]
  exact pairwise_complex_sum_zero
    (fun r s => twistedCreateDirection N H r (twistedCreateDirection N H s ψ) p)
    (fun r s => by
      simpa [Pi.add_apply, Pi.zero_apply] using
        congrFun (twistedCreate_anticommute N H r s ψ) p)

theorem dTwistedAdjoint_sq (N : ℕ) (H : Role → ℂ) (ψ : ArchiveCochainC N) :
    dTwistedAdjoint N H (dTwistedAdjoint N H ψ) = 0 := by
  classical
  funext p
  have hbody : dTwistedAdjoint N H (dTwistedAdjoint N H ψ) p =
      ∑ r : Role, ∑ s : Role,
        twistedAnnihilateDirection N H r (twistedAnnihilateDirection N H s ψ) p := by
    unfold dTwistedAdjoint
    simp only [Finset.sum_apply, Pi.neg_apply]
    refine Finset.sum_congr rfl ?_
    intro r _
    have happ := congrFun (twistedAnnihilateDirection_sum N H r
      (fun s => -twistedAnnihilateDirection N H s ψ)) p
    simp only [Finset.sum_apply, Pi.neg_apply] at happ
    rw [happ, ← Finset.sum_neg_distrib]
    refine Finset.sum_congr rfl ?_
    intro s _
    have hneg := congrFun (twistedAnnihilateDirection_neg N H r
      (twistedAnnihilateDirection N H s ψ)) p
    simp only [Pi.neg_apply] at hneg
    rw [hneg]
    ring
  rw [hbody]
  exact pairwise_complex_sum_zero
    (fun r s => twistedAnnihilateDirection N H r (twistedAnnihilateDirection N H s ψ) p)
    (fun r s => by
      simpa [Pi.add_apply, Pi.zero_apply] using
        congrFun (twistedAnnihilate_anticommute N H r s ψ) p)

theorem twistedCreate_of_annihilate (N : ℕ) (H : Role → ℂ) (r s : Role)
    (ψ : ArchiveCochainC N) :
    twistedCreateDirection N H r (twistedAnnihilateDirection N H s ψ) =
      createActionC N r (annihilateActionC N s
        (twistedForwardSite N H r (twistedBackwardSite N H s ψ))) := by
  unfold twistedCreateDirection twistedAnnihilateDirection
  rw [twistedForwardSite_annihilate_comm]

theorem twistedAnnihilate_of_create (N : ℕ) (H : Role → ℂ)
    (hne : ∀ t, H t ≠ 0) (r s : Role) (ψ : ArchiveCochainC N) :
    twistedAnnihilateDirection N H s (twistedCreateDirection N H r ψ) =
      annihilateActionC N s (createActionC N r
        (twistedForwardSite N H r (twistedBackwardSite N H s ψ))) := by
  unfold twistedAnnihilateDirection twistedCreateDirection
  rw [twistedBackwardSite_create_comm]
  rw [twistedForwardSite_backwardSite_comm N H hne r s ψ]

theorem hodgeCarDiracTwisted_cross (N : ℕ) (H : Role → ℂ)
    (hunit : ∀ r, star (H r) * H r = 1) (ψ : ArchiveCochainC N) :
    dTwisted N H (dTwistedAdjoint N H ψ) +
      dTwistedAdjoint N H (dTwisted N H ψ) =
        twistedDifferenceLaplacian N H ψ := by
  classical
  have hne : ∀ t, H t ≠ 0 := fun t => unitary_ne_zero (H t) (hunit t)
  funext p
  have hd : dTwisted N H (dTwistedAdjoint N H ψ) p =
      ∑ r : Role, ∑ s : Role,
        -twistedCreateDirection N H r (twistedAnnihilateDirection N H s ψ) p := by
    unfold dTwisted dTwistedAdjoint
    simp only [Finset.sum_apply, Pi.neg_apply]
    refine Finset.sum_congr rfl ?_
    intro r _
    have happ := congrFun
      (twistedCreateDirection_sum N H r (fun s => -twistedAnnihilateDirection N H s ψ)) p
    simp only [Finset.sum_apply, Pi.neg_apply] at happ
    have hneg : ∀ s,
        twistedCreateDirection N H r (-twistedAnnihilateDirection N H s ψ) p =
          -twistedCreateDirection N H r (twistedAnnihilateDirection N H s ψ) p :=
      fun s => congrFun (twistedCreateDirection_neg N H r _) p
    rw [happ]
    simp only [hneg, Finset.sum_neg_distrib]
  have hδ : dTwistedAdjoint N H (dTwisted N H ψ) p =
      ∑ s : Role, ∑ r : Role,
        -twistedAnnihilateDirection N H s (twistedCreateDirection N H r ψ) p := by
    unfold dTwistedAdjoint dTwisted
    simp only [Finset.sum_apply, Pi.neg_apply]
    refine Finset.sum_congr rfl ?_
    intro s _
    have happ := congrFun
      (twistedAnnihilateDirection_sum N H s (fun r => twistedCreateDirection N H r ψ)) p
    simp only [Finset.sum_apply] at happ
    rw [happ, ← Finset.sum_neg_distrib]
  simp only [Pi.add_apply, hd, hδ]
  have horder :
      (∑ s : Role, ∑ r : Role,
          -twistedAnnihilateDirection N H s (twistedCreateDirection N H r ψ) p) =
        ∑ r : Role, ∑ s : Role,
          -twistedAnnihilateDirection N H s (twistedCreateDirection N H r ψ) p :=
    Finset.sum_comm
  rw [horder]
  have hflat :
      (∑ r : Role, ∑ s : Role,
          -twistedCreateDirection N H r (twistedAnnihilateDirection N H s ψ) p) +
        (∑ r : Role, ∑ s : Role,
          -twistedAnnihilateDirection N H s (twistedCreateDirection N H r ψ) p) =
        ∑ r : Role, ∑ s : Role,
          (-twistedCreateDirection N H r (twistedAnnihilateDirection N H s ψ) p +
            -twistedAnnihilateDirection N H s (twistedCreateDirection N H r ψ) p) := by
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl ?_
    intro r _
    rw [← Finset.sum_add_distrib]
  rw [hflat]
  have hpair : ∀ r s,
      -twistedCreateDirection N H r (twistedAnnihilateDirection N H s ψ) p +
        -twistedAnnihilateDirection N H s (twistedCreateDirection N H r ψ) p =
          -(if r = s then
              twistedForwardSite N H r (twistedBackwardSite N H s ψ)
            else 0) p := by
    intro r s
    rw [twistedCreate_of_annihilate, twistedAnnihilate_of_create N H hne]
    have happ := congrFun
      (create_annihilate_deltaC N r s
        (twistedForwardSite N H r (twistedBackwardSite N H s ψ))) p
    simp only [Pi.add_apply] at happ
    rw [← neg_add, happ]
  have hjoined :
      (∑ r : Role, ∑ s : Role,
          (-twistedCreateDirection N H r (twistedAnnihilateDirection N H s ψ) p +
            -twistedAnnihilateDirection N H s (twistedCreateDirection N H r ψ) p)) =
        ∑ r : Role, ∑ s : Role,
          -(if r = s then twistedForwardSite N H r (twistedBackwardSite N H s ψ) else 0) p := by
    refine Finset.sum_congr rfl ?_
    intro r _
    refine Finset.sum_congr rfl ?_
    intro s _
    exact hpair r s
  rw [hjoined]
  have hdiag :
        (∑ r : Role, ∑ s : Role,
            -(if r = s then
                twistedForwardSite N H r (twistedBackwardSite N H s ψ) else 0) p) =
          ∑ r : Role, -(twistedForwardSite N H r (twistedBackwardSite N H r ψ) p) := by
    refine Finset.sum_congr rfl ?_
    intro r _
    rw [Finset.sum_eq_single r]
    · simp
    · intro s _ hrs
      simp [Ne.symm hrs]
    · simp
  rw [hdiag]
  have hcomm :
      (∑ r : Role, -(twistedForwardSite N H r (twistedBackwardSite N H r ψ) p)) =
        ∑ r : Role, -(twistedBackwardSite N H r (twistedForwardSite N H r ψ) p) := by
    refine Finset.sum_congr rfl ?_
    intro r _
    exact congrArg Neg.neg
      (congrFun (twistedForwardSite_backwardSite_comm N H hne r r ψ) p)
  rw [hcomm]
  simp [twistedDifferenceLaplacian, twistedScalarLaplacian, twistedBackwardSite,
    twistedForwardSite, Finset.sum_apply]

theorem twistedForwardDifference_add (N : ℕ) (r : Role) (h : ℂ)
    (f g : ArchiveRolePhaseGroup N → ℂ) :
    twistedForwardDifference N r h (f + g) =
      twistedForwardDifference N r h f + twistedForwardDifference N r h g := by
  funext x
  simp [twistedForwardDifference, twistedRoleShift, Pi.add_apply]
  ring

theorem twistedBackwardDifference_add (N : ℕ) (r : Role) (h : ℂ)
    (f g : ArchiveRolePhaseGroup N → ℂ) :
    twistedBackwardDifference N r h (f + g) =
      twistedBackwardDifference N r h f + twistedBackwardDifference N r h g := by
  funext x
  by_cases hx : x r = 0
  · simp [twistedBackwardDifference, twistedRoleShiftInv, hx, Pi.add_apply]
    ring
  · simp [twistedBackwardDifference, twistedRoleShiftInv, hx, Pi.add_apply]
    ring

theorem twistedCreateDirection_add (N : ℕ) (H : Role → ℂ) (r : Role)
    (ψ φ : ArchiveCochainC N) :
    twistedCreateDirection N H r (ψ + φ) =
      twistedCreateDirection N H r ψ + twistedCreateDirection N H r φ := by
  classical
  funext p
  unfold twistedCreateDirection createActionC twistedForwardSite
  simp only [Pi.add_apply]
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl ?_
  intro ket _
  simp only [twistedForwardDifference, twistedRoleShift, Pi.add_apply]
  ring

theorem twistedAnnihilateDirection_add (N : ℕ) (H : Role → ℂ) (r : Role)
    (ψ φ : ArchiveCochainC N) :
    twistedAnnihilateDirection N H r (ψ + φ) =
      twistedAnnihilateDirection N H r ψ + twistedAnnihilateDirection N H r φ := by
  classical
  funext p
  unfold twistedAnnihilateDirection annihilateActionC twistedBackwardSite
  simp only [Pi.add_apply]
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl ?_
  intro ket _
  by_cases hx : p.1 r = 0
  · simp only [twistedBackwardDifference, twistedRoleShiftInv, hx, Pi.add_apply]
    ring
  · simp only [twistedBackwardDifference, twistedRoleShiftInv, hx, Pi.add_apply]
    ring

theorem dTwisted_add (N : ℕ) (H : Role → ℂ) (ψ φ : ArchiveCochainC N) :
    dTwisted N H (ψ + φ) = dTwisted N H ψ + dTwisted N H φ := by
  unfold dTwisted
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl ?_
  intro r _
  exact twistedCreateDirection_add N H r ψ φ

theorem dTwistedAdjoint_add (N : ℕ) (H : Role → ℂ) (ψ φ : ArchiveCochainC N) :
    dTwistedAdjoint N H (ψ + φ) = dTwistedAdjoint N H ψ + dTwistedAdjoint N H φ := by
  unfold dTwistedAdjoint
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl ?_
  intro r _
  rw [twistedAnnihilateDirection_add]
  funext p
  simp [Pi.neg_apply, Pi.add_apply]
  ring

theorem hodgeCarDiracTwisted_sq (N : ℕ) (H : Role → ℂ)
    (hunit : ∀ r, star (H r) * H r = 1) (ψ : ArchiveCochainC N) :
    hodgeCarDiracTwisted N H (hodgeCarDiracTwisted N H ψ) =
      twistedDifferenceLaplacian N H ψ := by
  have hcross := hodgeCarDiracTwisted_cross N H hunit ψ
  unfold hodgeCarDiracTwisted
  rw [dTwisted_add, dTwistedAdjoint_add, dTwisted_sq, dTwistedAdjoint_sq]
  simp only [zero_add, add_zero]
  exact hcross

theorem hodgeCarDiracTwisted_sq_fibre (N : ℕ) (H : Role → ℂ)
    (hunit : ∀ r, star (H r) * H r = 1) (ψ : ArchiveCochainC N)
    (p : ArchiveCochainBasis N) :
    hodgeCarDiracTwisted N H (hodgeCarDiracTwisted N H ψ) p =
      twistedScalarLaplacian N H (fun x => ψ (x, p.2)) p.1 := by
  rw [hodgeCarDiracTwisted_sq N H hunit]
  rfl

/-! ## Adjoint -/

theorem cochainPairingC_conj (N : ℕ) (ψ φ : ArchiveCochainC N) :
    star (cochainPairingC N ψ φ) = cochainPairingC N φ ψ := by
  classical
  unfold cochainPairingC
  simp_rw [star_sum, star_mul, star_star]

theorem cochainPairingC_add_left (N : ℕ) (ψ φ χ : ArchiveCochainC N) :
    cochainPairingC N (ψ + φ) χ =
      cochainPairingC N ψ χ + cochainPairingC N φ χ := by
  unfold cochainPairingC
  simp [Pi.add_apply, star_add, add_mul, Finset.sum_add_distrib]

theorem cochainPairingC_add_right (N : ℕ) (ψ φ χ : ArchiveCochainC N) :
    cochainPairingC N ψ (φ + χ) =
      cochainPairingC N ψ φ + cochainPairingC N ψ χ := by
  unfold cochainPairingC
  simp [Pi.add_apply, mul_add, Finset.sum_add_distrib]

theorem cochainPairingC_sum_left {ι : Type*} [Fintype ι] (N : ℕ)
    (F : ι → ArchiveCochainC N) (φ : ArchiveCochainC N) :
    cochainPairingC N (∑ i, F i) φ = ∑ i, cochainPairingC N (F i) φ := by
  classical
  unfold cochainPairingC
  simp_rw [Finset.sum_apply, star_sum, Finset.sum_mul]
  calc
    ∑ x, ∑ s, ∑ i, star (F i (x, s)) * φ (x, s) =
        ∑ x, ∑ i, ∑ s, star (F i (x, s)) * φ (x, s) := by
          refine Finset.sum_congr rfl ?_
          intro x _
          exact Finset.sum_comm
    _ = ∑ i, ∑ x, ∑ s, star (F i (x, s)) * φ (x, s) := Finset.sum_comm

theorem cochainPairingC_sum_right {ι : Type*} [Fintype ι] (N : ℕ)
    (ψ : ArchiveCochainC N) (F : ι → ArchiveCochainC N) :
    cochainPairingC N ψ (∑ i, F i) = ∑ i, cochainPairingC N ψ (F i) := by
  classical
  unfold cochainPairingC
  simp_rw [Finset.sum_apply, Finset.mul_sum]
  calc
    ∑ x, ∑ s, ∑ i, star (ψ (x, s)) * F i (x, s) =
        ∑ x, ∑ i, ∑ s, star (ψ (x, s)) * F i (x, s) := by
          refine Finset.sum_congr rfl ?_
          intro x _
          exact Finset.sum_comm
    _ = ∑ i, ∑ x, ∑ s, star (ψ (x, s)) * F i (x, s) := Finset.sum_comm

theorem createActionC_adjoint (N : ℕ) (r : Role) (ψ φ : ArchiveCochainC N) :
    cochainPairingC N (createActionC N r ψ) φ =
      cochainPairingC N ψ (annihilateActionC N r φ) := by
  classical
  unfold cochainPairingC createActionC annihilateActionC
  simp_rw [star_sum, Finset.sum_mul]
  have hswap :
      (∑ x, ∑ bra, ∑ ket,
          star ((carCreate r bra ket : ℂ) * ψ (x, ket)) * φ (x, bra)) =
        ∑ x, ∑ ket, ∑ bra,
          star ((carCreate r bra ket : ℂ) * ψ (x, ket)) * φ (x, bra) := by
    apply Finset.sum_congr rfl
    intro x _
    exact Finset.sum_comm
  rw [hswap]
  apply Finset.sum_congr rfl
  intro x _
  apply Finset.sum_congr rfl
  intro ket _
  calc
    (∑ bra, star ((carCreate r bra ket : ℂ) * ψ (x, ket)) * φ (x, bra)) =
        ∑ bra, star (ψ (x, ket)) *
          ((carCreate r bra ket : ℂ) * φ (x, bra)) := by
            apply Finset.sum_congr rfl
            intro bra _
            rw [star_mul]
            simp
            ring
    _ = star (ψ (x, ket)) *
          ∑ bra, (carCreate r bra ket : ℂ) * φ (x, bra) := by
          rw [← Finset.mul_sum]
    _ = star (ψ (x, ket)) *
          ∑ bra, (carAnnihilate r ket bra : ℂ) * φ (x, bra) := by
          apply congrArg (fun z => star (ψ (x, ket)) * z)
          apply Finset.sum_congr rfl
          intro bra _
          rw [carCreate]

theorem twistedForwardSite_adjoint (N : ℕ) (H : Role → ℂ) (r : Role)
    (hu : star (H r) * H r = 1) (ψ φ : ArchiveCochainC N) :
    cochainPairingC N (twistedForwardSite N H r ψ) φ =
      cochainPairingC N ψ (-twistedBackwardSite N H r φ) := by
  classical
  unfold cochainPairingC twistedForwardSite twistedBackwardSite
  simp only [Pi.neg_apply]
  calc
    ∑ x, ∑ s, star (twistedForwardDifference N r (H r) (fun y => ψ (y, s)) x) * φ (x, s) =
        ∑ s, ∑ x, star (twistedForwardDifference N r (H r) (fun y => ψ (y, s)) x) *
          φ (x, s) := by
          exact Finset.sum_comm
    _ = ∑ s, phasePairing N (fun y => ψ (y, s))
          (-twistedBackwardDifference N r (H r) (fun y => φ (y, s))) := by
          refine Finset.sum_congr rfl ?_
          intro s _
          simpa [phasePairing, Pi.neg_apply] using
            twistedForward_adjoint N r (H r) hu
              (fun y => ψ (y, s)) (fun y => φ (y, s))
    _ = ∑ s, ∑ x, star (ψ (x, s)) *
          (-twistedBackwardDifference N r (H r) (fun y => φ (y, s)) x) := by
          simp [phasePairing]
    _ = ∑ x, ∑ s, star (ψ (x, s)) *
          (-twistedBackwardDifference N r (H r) (fun y => φ (y, s)) x) := by
          exact Finset.sum_comm.symm

theorem twistedCreateDirection_adjoint (N : ℕ) (H : Role → ℂ) (r : Role)
    (hu : star (H r) * H r = 1) (ψ φ : ArchiveCochainC N) :
    cochainPairingC N (twistedCreateDirection N H r ψ) φ =
      cochainPairingC N ψ (-twistedAnnihilateDirection N H r φ) := by
  calc
    cochainPairingC N (twistedCreateDirection N H r ψ) φ =
        cochainPairingC N (createActionC N r (twistedForwardSite N H r ψ)) φ := rfl
    _ = cochainPairingC N (twistedForwardSite N H r ψ) (annihilateActionC N r φ) :=
          createActionC_adjoint N r _ _
    _ = cochainPairingC N ψ
          (-twistedBackwardSite N H r (annihilateActionC N r φ)) :=
          twistedForwardSite_adjoint N H r hu _ _
    _ = cochainPairingC N ψ
          (-annihilateActionC N r (twistedBackwardSite N H r φ)) := by
          rw [twistedBackwardSite_annihilate_comm]
    _ = cochainPairingC N ψ (-twistedAnnihilateDirection N H r φ) := rfl

theorem dTwisted_adjoint (N : ℕ) (H : Role → ℂ)
    (hunit : ∀ r, star (H r) * H r = 1) (ψ φ : ArchiveCochainC N) :
    cochainPairingC N (dTwisted N H ψ) φ =
      cochainPairingC N ψ (dTwistedAdjoint N H φ) := by
  classical
  unfold dTwisted dTwistedAdjoint
  rw [cochainPairingC_sum_left, cochainPairingC_sum_right]
  refine Finset.sum_congr rfl ?_
  intro r _
  exact twistedCreateDirection_adjoint N H r (hunit r) ψ φ

theorem dTwistedAdjoint_adjoint (N : ℕ) (H : Role → ℂ)
    (hunit : ∀ r, star (H r) * H r = 1) (ψ φ : ArchiveCochainC N) :
    cochainPairingC N (dTwistedAdjoint N H ψ) φ =
      cochainPairingC N ψ (dTwisted N H φ) := by
  have h := dTwisted_adjoint N H hunit φ ψ
  have hstar := congrArg star h
  rw [cochainPairingC_conj, cochainPairingC_conj] at hstar
  exact hstar.symm

theorem hodgeCarDiracTwisted_self_adjoint (N : ℕ) (H : Role → ℂ)
    (hunit : ∀ r, star (H r) * H r = 1) (ψ φ : ArchiveCochainC N) :
    cochainPairingC N (hodgeCarDiracTwisted N H ψ) φ =
      cochainPairingC N ψ (hodgeCarDiracTwisted N H φ) := by
  unfold hodgeCarDiracTwisted
  rw [cochainPairingC_add_left, cochainPairingC_add_right,
    dTwisted_adjoint N H hunit, dTwistedAdjoint_adjoint N H hunit]
  ring

/-! ## Parity, degree, and radius one -/

theorem carCreate_parity_flip_complex (r : Role) (bra ket : ArchiveFockState) :
    (fockParitySign bra : ℂ) * (carCreate r bra ket : ℂ) =
      -((fockParitySign ket : ℂ) * (carCreate r bra ket : ℂ)) := by
  simpa [Complex.ofReal_mul, Complex.ofReal_neg] using
    congrArg (fun z : ℝ => (z : ℂ)) (carCreate_parity_flip r bra ket)

theorem carAnnihilate_parity_flip_complex (r : Role) (bra ket : ArchiveFockState) :
    (fockParitySign bra : ℂ) * (carAnnihilate r bra ket : ℂ) =
      -((fockParitySign ket : ℂ) * (carAnnihilate r bra ket : ℂ)) := by
  simpa [Complex.ofReal_mul, Complex.ofReal_neg] using
    congrArg (fun z : ℝ => (z : ℂ)) (carAnnihilate_parity_flip r bra ket)

theorem dTwisted_parity_odd (N : ℕ) (H : Role → ℂ) (ψ : ArchiveCochainC N) :
    parityCochainC N (dTwisted N H ψ) =
      -dTwisted N H (parityCochainC N ψ) := by
  classical
  funext p
  unfold parityCochainC dTwisted twistedCreateDirection createActionC twistedForwardSite
  simp only [Finset.sum_apply, Pi.neg_apply]
  rw [Finset.mul_sum, ← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl ?_
  intro r _
  rw [Finset.mul_sum, ← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl ?_
  intro ket _
  have hflip := carCreate_parity_flip_complex r p.2 ket
  have hΔ := congrFun (twistedForwardDifference_const_mul N r (H r)
    (fockParitySign ket : ℂ) (fun x => ψ (x, ket))) p.1
  calc
    (fockParitySign p.2 : ℂ) * ((carCreate r p.2 ket : ℂ) *
        twistedForwardDifference N r (H r) (fun x => ψ (x, ket)) p.1) =
        ((fockParitySign p.2 : ℂ) * (carCreate r p.2 ket : ℂ)) *
          twistedForwardDifference N r (H r) (fun x => ψ (x, ket)) p.1 := by ring
    _ = (-((fockParitySign ket : ℂ) * (carCreate r p.2 ket : ℂ))) *
          twistedForwardDifference N r (H r) (fun x => ψ (x, ket)) p.1 := by rw [hflip]
    _ = -((carCreate r p.2 ket : ℂ) *
          ((fockParitySign ket : ℂ) *
            twistedForwardDifference N r (H r) (fun x => ψ (x, ket)) p.1)) := by ring
    _ = -((carCreate r p.2 ket : ℂ) *
          twistedForwardDifference N r (H r)
            (fun x => (fockParitySign ket : ℂ) * ψ (x, ket)) p.1) := by rw [hΔ]

theorem twistedAnnihilateDirection_parity (N : ℕ) (H : Role → ℂ) (r : Role)
    (ψ : ArchiveCochainC N) :
    parityCochainC N (twistedAnnihilateDirection N H r ψ) =
      -twistedAnnihilateDirection N H r (parityCochainC N ψ) := by
  classical
  funext p
  unfold parityCochainC twistedAnnihilateDirection annihilateActionC twistedBackwardSite
  simp only [Pi.neg_apply]
  rw [Finset.mul_sum, ← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl ?_
  intro ket _
  have hflip := carAnnihilate_parity_flip_complex r p.2 ket
  have hΔ := congrFun (twistedBackwardDifference_const_mul N r (H r)
    (fockParitySign ket : ℂ) (fun x => ψ (x, ket))) p.1
  calc
    (fockParitySign p.2 : ℂ) * ((carAnnihilate r p.2 ket : ℂ) *
        twistedBackwardDifference N r (H r) (fun x => ψ (x, ket)) p.1) =
        ((fockParitySign p.2 : ℂ) * (carAnnihilate r p.2 ket : ℂ)) *
          twistedBackwardDifference N r (H r) (fun x => ψ (x, ket)) p.1 := by ring
    _ = (-((fockParitySign ket : ℂ) * (carAnnihilate r p.2 ket : ℂ))) *
          twistedBackwardDifference N r (H r) (fun x => ψ (x, ket)) p.1 := by rw [hflip]
    _ = -((carAnnihilate r p.2 ket : ℂ) *
          ((fockParitySign ket : ℂ) *
            twistedBackwardDifference N r (H r) (fun x => ψ (x, ket)) p.1)) := by ring
    _ = -((carAnnihilate r p.2 ket : ℂ) *
          twistedBackwardDifference N r (H r)
            (fun x => (fockParitySign ket : ℂ) * ψ (x, ket)) p.1) := by
          rw [← hΔ]

theorem dTwistedAdjoint_parity_odd (N : ℕ) (H : Role → ℂ) (ψ : ArchiveCochainC N) :
    parityCochainC N (dTwistedAdjoint N H ψ) =
      -dTwistedAdjoint N H (parityCochainC N ψ) := by
  classical
  funext p
  simp only [parityCochainC, dTwistedAdjoint, Finset.sum_apply, Pi.neg_apply]
  rw [Finset.mul_sum, ← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl ?_
  intro r _
  have h := congrFun (twistedAnnihilateDirection_parity N H r ψ) p
  simp only [parityCochainC, Pi.neg_apply] at h
  rw [mul_neg, h]

theorem hodgeCarDiracTwisted_parity_odd (N : ℕ) (H : Role → ℂ) (ψ : ArchiveCochainC N) :
    parityCochainC N (hodgeCarDiracTwisted N H ψ) =
      -hodgeCarDiracTwisted N H (parityCochainC N ψ) := by
  unfold hodgeCarDiracTwisted
  rw [show parityCochainC N (dTwisted N H ψ + dTwistedAdjoint N H ψ) =
      parityCochainC N (dTwisted N H ψ) + parityCochainC N (dTwistedAdjoint N H ψ) by
    funext p
    unfold parityCochainC
    simp [Pi.add_apply]
    ring]
  rw [dTwisted_parity_odd, dTwistedAdjoint_parity_odd]
  funext p
  simp [Pi.neg_apply, Pi.add_apply]
  ring

theorem dTwisted_degree_raise (N k : ℕ) (H : Role → ℂ) (ψ : ArchiveCochainC N)
    (hψ : HomogeneousCochainC N k ψ) :
    HomogeneousCochainC N (k + 1) (dTwisted N H ψ) := by
  classical
  intro x bra hbra
  unfold dTwisted twistedCreateDirection createActionC twistedForwardSite
  simp only [Finset.sum_apply]
  apply Finset.sum_eq_zero
  intro r _
  apply Finset.sum_eq_zero
  intro ket _
  by_cases hc : carCreate r bra ket = 0
  · rw [show (carCreate r bra ket : ℂ) = 0 by
      simpa using congrArg (fun z : ℝ => (z : ℂ)) hc]
    simp
  · have hdeg := carCreate_degree_raise r bra ket hc
    have hket : fockDegree ket ≠ k := by
      intro hk
      apply hbra
      omega
    have hx := hψ x ket hket
    have hxp := hψ (roleTranslatePlus N r x) ket hket
    simp [twistedForwardDifference, twistedRoleShift, hx, hxp, hc]

theorem dTwistedAdjoint_degree_lower (N k : ℕ) (H : Role → ℂ) (ψ : ArchiveCochainC N)
    (hψ : HomogeneousCochainC N (k + 1) ψ) :
    HomogeneousCochainC N k (dTwistedAdjoint N H ψ) := by
  classical
  intro x bra hbra
  unfold dTwistedAdjoint twistedAnnihilateDirection annihilateActionC twistedBackwardSite
  simp only [Finset.sum_apply, Pi.neg_apply]
  apply Finset.sum_eq_zero
  intro r _
  rw [neg_eq_zero]
  apply Finset.sum_eq_zero
  intro ket _
  by_cases hc : carAnnihilate r bra ket = 0
  · rw [show (carAnnihilate r bra ket : ℂ) = 0 by
      simpa using congrArg (fun z : ℝ => (z : ℂ)) hc]
    simp
  · have hdeg := carAnnihilate_degree_lower r bra ket hc
    have hket : fockDegree ket ≠ k + 1 := by
      intro hk
      apply hbra
      omega
    have hx := hψ x ket hket
    have hxm := hψ (roleTranslateMinus N r x) ket hket
    simp [twistedBackwardDifference, twistedRoleShiftInv, hx, hxm]

/-- `d_H` at a site reads that site and the forward neighbour on each role.
On the seam the neighbour is multiplied by the holonomy, so the link stays radius one. -/
theorem dTwisted_radius_one (N : ℕ) (H : Role → ℂ)
    (ψ φ : ArchiveCochainC N) (x : ArchiveRolePhaseGroup N) (bra : ArchiveFockState)
    (h : ∀ r ket,
      ψ (x, ket) = φ (x, ket) ∧
        ψ (roleTranslatePlus N r x, ket) = φ (roleTranslatePlus N r x, ket)) :
    dTwisted N H ψ (x, bra) = dTwisted N H φ (x, bra) := by
  unfold dTwisted twistedCreateDirection createActionC twistedForwardSite
  simp only [Finset.sum_apply]
  refine Finset.sum_congr rfl ?_
  intro r _
  refine Finset.sum_congr rfl ?_
  intro ket _
  congr 1
  exact twistedForwardDifference_local N r (H r) _ _ x (h r ket).1 (h r ket).2

theorem dTwistedAdjoint_radius_one (N : ℕ) (H : Role → ℂ)
    (ψ φ : ArchiveCochainC N) (x : ArchiveRolePhaseGroup N) (bra : ArchiveFockState)
    (h : ∀ r ket,
      ψ (x, ket) = φ (x, ket) ∧
        ψ (roleTranslateMinus N r x, ket) = φ (roleTranslateMinus N r x, ket)) :
    dTwistedAdjoint N H ψ (x, bra) = dTwistedAdjoint N H φ (x, bra) := by
  simp only [dTwistedAdjoint, twistedAnnihilateDirection, annihilateActionC,
    twistedBackwardSite, Finset.sum_apply, Pi.neg_apply]
  refine Finset.sum_congr rfl ?_
  intro r _
  congr 1
  refine Finset.sum_congr rfl ?_
  intro ket _
  congr 1
  exact twistedBackwardDifference_local N r (H r) _ _ x (h r ket).1 (h r ket).2

theorem hodgeCarDiracTwisted_radius_one (N : ℕ) (H : Role → ℂ)
    (ψ φ : ArchiveCochainC N) (x : ArchiveRolePhaseGroup N) (bra : ArchiveFockState)
    (h : ∀ r ket,
      ψ (x, ket) = φ (x, ket) ∧
        ψ (roleTranslatePlus N r x, ket) = φ (roleTranslatePlus N r x, ket) ∧
        ψ (roleTranslateMinus N r x, ket) = φ (roleTranslateMinus N r x, ket)) :
    hodgeCarDiracTwisted N H ψ (x, bra) = hodgeCarDiracTwisted N H φ (x, bra) := by
  have hd := dTwisted_radius_one N H ψ φ x bra (fun r ket => ⟨(h r ket).1, (h r ket).2.1⟩)
  have hδ := dTwistedAdjoint_radius_one N H ψ φ x bra
    (fun r ket => ⟨(h r ket).1, (h r ket).2.2⟩)
  simp only [hodgeCarDiracTwisted, Pi.add_apply, hd, hδ]

/-! ## Trivial holonomy recovers the real operator -/

theorem twistedForward_one_ofReal (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) :
    twistedForwardDifference N r 1 (fun y => (f y : ℂ)) x =
      (forwardDifference N r f x : ℂ) := by
  simp only [twistedForward_one, forwardDifference_apply, forwardDifferenceScale]
  push_cast
  ring

theorem twistedBackward_one_ofReal (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) :
    twistedBackwardDifference N r 1 (fun y => (f y : ℂ)) x =
      (backwardDifference N r f x : ℂ) := by
  by_cases hx : x r = 0
  · simp [twistedBackwardDifference, twistedRoleShiftInv, hx, inv_one,
      backwardDifference_apply, forwardDifferenceScale]
  · simp [twistedBackwardDifference, twistedRoleShiftInv, hx,
      backwardDifference_apply, forwardDifferenceScale]

theorem dTwisted_one_ofReal (N : ℕ) (ψ : ArchiveCochain N) :
    dTwisted N (fun _ => (1 : ℂ)) (fun p => (ψ p : ℂ)) =
      fun p => (dForward N ψ p : ℂ) := by
  funext p
  have hL : dTwisted N (fun _ => (1 : ℂ)) (fun q => (ψ q : ℂ)) p =
      ∑ r : Role, ∑ ket : ArchiveFockState,
        (carCreate r p.2 ket : ℂ) *
          twistedForwardDifference N r 1 (fun y => (ψ (y, ket) : ℂ)) p.1 := by
    simp [dTwisted, twistedCreateDirection, createActionC, twistedForwardSite,
      Finset.sum_apply]
  have hR : (dForward N ψ p : ℂ) =
      ∑ r : Role, ∑ ket : ArchiveFockState,
        ((carCreate r p.2 ket : ℝ) * forwardDifference N r (fun y => ψ (y, ket)) p.1 : ℂ) := by
    simp [dForward, forwardCreateDirection, Finset.sum_apply, Complex.ofReal_sum,
      Complex.ofReal_mul]
  rw [hL, hR]
  refine Finset.sum_congr rfl ?_
  intro r _
  refine Finset.sum_congr rfl ?_
  intro ket _
  rw [twistedForward_one_ofReal]

theorem dTwistedAdjoint_one_ofReal (N : ℕ) (ψ : ArchiveCochain N) :
    dTwistedAdjoint N (fun _ => (1 : ℂ)) (fun p => (ψ p : ℂ)) =
      fun p => (hodgeCodifferential N ψ p : ℂ) := by
  funext p
  have hL : dTwistedAdjoint N (fun _ => (1 : ℂ)) (fun q => (ψ q : ℂ)) p =
      ∑ r : Role, -∑ ket : ArchiveFockState,
        (carAnnihilate r p.2 ket : ℂ) *
          twistedBackwardDifference N r 1 (fun y => (ψ (y, ket) : ℂ)) p.1 := by
    simp [dTwistedAdjoint, twistedAnnihilateDirection, annihilateActionC,
      twistedBackwardSite, Finset.sum_apply, Pi.neg_apply]
  have hR : (hodgeCodifferential N ψ p : ℂ) =
      ∑ r : Role, -∑ ket : ArchiveFockState,
        ((carAnnihilate r p.2 ket : ℝ) *
          backwardDifference N r (fun y => ψ (y, ket)) p.1 : ℂ) := by
    simp [hodgeCodifferential, backwardAnnihilateDirection, annihilateAction, backwardSite,
      Finset.sum_apply, Pi.neg_apply, Complex.ofReal_sum, Complex.ofReal_neg,
      Complex.ofReal_mul]
  rw [hL, hR]
  refine Finset.sum_congr rfl ?_
  intro r _
  congr 1
  refine Finset.sum_congr rfl ?_
  intro ket _
  rw [twistedBackward_one_ofReal]

theorem hodgeCarDiracTwisted_one_ofReal (N : ℕ) (ψ : ArchiveCochain N) :
    hodgeCarDiracTwisted N (fun _ => (1 : ℂ)) (fun p => (ψ p : ℂ)) =
      fun p => (hodgeCarDirac N ψ p : ℂ) := by
  funext p
  simp only [hodgeCarDiracTwisted, hodgeCarDirac, Pi.add_apply]
  rw [congrFun (dTwisted_one_ofReal N ψ) p, congrFun (dTwistedAdjoint_one_ofReal N ψ) p]
  push_cast
  ring

theorem trivialHolonomy_unitary (r : Role) : star (1 : ℂ) * (1 : ℂ) = 1 := by
  simp

end

end D0.Geometry
