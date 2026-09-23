import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.Tactic
import D0.Geometry.ArchiveCARFockCarrier
import D0.Geometry.ArchiveHodgeCARDiracSquare

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

/-!
# Kernel of the Hodge/difference CAR operator

`D_H²` is the fibrewise oriented difference Laplacian. Its kernel is the
cochains constant along every role. Self-adjointness for the counting pairing
identifies that kernel with `ker D_H`. The parameter space is one real
amplitude for each of the 16 Fock states.
-/

theorem backwardAnnihilateDirection_smul (N : ℕ) (r : Role) (a : ℝ)
    (ψ : ArchiveCochain N) :
    backwardAnnihilateDirection N r (a • ψ) =
      a • backwardAnnihilateDirection N r ψ := by
  unfold backwardAnnihilateDirection
  have hsite : backwardSite N r (a • ψ) = a • backwardSite N r ψ := by
    funext p
    simp only [backwardSite, backwardDifference_apply, Pi.smul_apply, smul_eq_mul]
    ring
  rw [hsite, annihilateAction_smul]

theorem hodgeCodifferential_smul (N : ℕ) (a : ℝ) (ψ : ArchiveCochain N) :
    hodgeCodifferential N (a • ψ) = a • hodgeCodifferential N ψ := by
  rw [hodgeCodifferential_eq_sum, hodgeCodifferential_eq_sum]
  simp_rw [codiffDirection_eq_neg, backwardAnnihilateDirection_smul]
  rw [Finset.smul_sum]
  refine Finset.sum_congr rfl ?_
  intro r _
  simp [smul_neg]

theorem hodgeCarDirac_add (N : ℕ) (ψ φ : ArchiveCochain N) :
    hodgeCarDirac N (ψ + φ) = hodgeCarDirac N ψ + hodgeCarDirac N φ := by
  unfold hodgeCarDirac
  rw [dForward_add, hodgeCodifferential_add]
  abel

theorem hodgeCarDirac_smul (N : ℕ) (a : ℝ) (ψ : ArchiveCochain N) :
    hodgeCarDirac N (a • ψ) = a • hodgeCarDirac N ψ := by
  unfold hodgeCarDirac
  rw [dForward_smul, hodgeCodifferential_smul]
  rw [smul_add]

theorem hodgeCarDirac_zero (N : ℕ) : hodgeCarDirac N (0 : ArchiveCochain N) = 0 := by
  simpa using hodgeCarDirac_smul N 0 (0 : ArchiveCochain N)

/-- Coefficients of the Fock fibre, extended as phase-constant cochains. -/
def hodgeKernelSection (N : ℕ) (c : ArchiveFockState → ℝ) : ArchiveCochain N :=
  fun p => c p.2

theorem hodgeKernelSection_injective (N : ℕ) :
    Function.Injective (hodgeKernelSection N) := by
  intro c₁ c₂ h
  funext s
  have := congrFun h (0, s)
  simpa [hodgeKernelSection] using this

theorem phase_coordinate_decomposition (N : ℕ) (x : ArchiveRolePhaseGroup N) :
    x = ∑ r : Role, (x r).val • roleStep N r := by
  classical
  funext s
  simp only [Finset.sum_apply, roleStep, Pi.smul_apply]
  rw [Finset.sum_eq_single s]
  · simp
  · intro r _ hrs
    simp [hrs.symm]
  · simp

theorem invariant_add_nsmul {N : ℕ} {f : ArchiveRolePhaseGroup N → ℝ}
    (h : ∀ r x, f (x + roleStep N r) = f x) (r : Role)
    (x : ArchiveRolePhaseGroup N) (k : ℕ) :
    f (x + k • roleStep N r) = f x := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [succ_nsmul, ← add_assoc, h r, ih]

theorem invariant_partial_sum {N : ℕ} {f : ArchiveRolePhaseGroup N → ℝ}
    (h : ∀ r x, f (x + roleStep N r) = f x)
    (x : ArchiveRolePhaseGroup N) (z : ArchiveRolePhaseGroup N)
    (s : Finset Role) :
    f (x + ∑ r ∈ s, (z r).val • roleStep N r) = f x := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert a s ha ih =>
    rw [Finset.sum_insert ha]
    have hcomm :
        x + ((z a).val • roleStep N a + ∑ r ∈ s, (z r).val • roleStep N r) =
          (x + ∑ r ∈ s, (z r).val • roleStep N r) + (z a).val • roleStep N a := by
      abel
    rw [hcomm, invariant_add_nsmul h a, ih]

theorem phaseInvariant_iff_constant (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ) :
    (∀ r x, f (roleTranslatePlus N r x) = f x) ↔ ∀ x y, f x = f y := by
  constructor
  · intro h x y
    have hstep : ∀ r z, f (z + roleStep N r) = f z := by
      intro r z
      simpa [roleTranslatePlus, roleTranslate] using h r z
    have hx : f x = f 0 := by
      have hdec := phase_coordinate_decomposition N x
      have hsum := invariant_partial_sum hstep 0 x Finset.univ
      rw [zero_add] at hsum
      rw [hdec.symm] at hsum
      exact hsum
    have hy : f y = f 0 := by
      have hdec := phase_coordinate_decomposition N y
      have hsum := invariant_partial_sum hstep 0 y Finset.univ
      rw [zero_add] at hsum
      rw [hdec.symm] at hsum
      exact hsum
    exact hx.trans hy.symm
  · intro h r x
    exact h _ _

theorem sum_sub_sub {α : Type*} [Fintype α]
    (a b c : α → ℝ) :
    ∑ x, (a x - b x - c x) = ∑ x, a x - ∑ x, b x - ∑ x, c x := by
  simp_rw [sub_eq_add_neg, Finset.sum_add_distrib, Finset.sum_neg_distrib]

theorem directional_second_difference_energy (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    ∑ x, f x * (2 * f x - f (x + roleStep N r) - f (x - roleStep N r)) =
      ∑ x, (f (x + roleStep N r) - f x) ^ 2 := by
  classical
  let e := roleStep N r
  have hshift : ∑ x, f x * f (x - e) = ∑ x, f x * f (x + e) := by
    have h := sum_translate N (-e) (fun x => f (x + e) * f x)
    have harg : ∀ x, (x + -e) + e = x := by
      intro x
      abel
    simp only [harg, mul_comm] at h
    simpa [sub_eq_add_neg] using h
  have hnorm : ∑ x, f (x + e) ^ 2 = ∑ x, f x ^ 2 := by
    simpa using sum_translate N e (fun x => f x ^ 2)
  have hmul : ∑ x, f x * (2 * f x - f (x + e) - f (x - e)) =
      ∑ x, (2 * f x ^ 2 - f x * f (x + e) - f x * f (x - e)) := by
    refine Finset.sum_congr rfl ?_
    intro x _
    ring
  rw [hmul, sum_sub_sub]
  have hsq : ∑ x, (f (x + e) - f x) ^ 2 =
      ∑ x, f (x + e) ^ 2 - ∑ x, (2 * f (x + e) * f x) + ∑ x, f x ^ 2 := by
    have hexpand : ∑ x, (f (x + e) - f x) ^ 2 =
        ∑ x, (f (x + e) ^ 2 - 2 * f (x + e) * f x + f x ^ 2) := by
      refine Finset.sum_congr rfl ?_
      intro x _
      ring
    rw [hexpand]
    simp_rw [sub_eq_add_neg, add_assoc, Finset.sum_add_distrib, Finset.sum_neg_distrib]
  rw [hshift]
  have htwo : ∑ x, (2 * f x ^ 2) = 2 * ∑ x, f x ^ 2 := by
    rw [← Finset.mul_sum]
  rw [htwo]
  have hcross : ∑ x, (2 * f (x + e) * f x) = 2 * ∑ x, f x * f (x + e) := by
    have hrewrite : ∑ x, (2 * f (x + e) * f x) = ∑ x, 2 * (f x * f (x + e)) := by
      refine Finset.sum_congr rfl ?_
      intro x _
      ring
    rw [hrewrite, Finset.mul_sum]
  rw [hsq, hnorm, hcross]
  ring

theorem scalarDifferenceLaplacian_energy (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ) :
    ∑ x, f x * scalarDifferenceLaplacian N f x =
      ∑ r : Role, forwardDifferenceScale N ^ 2 *
        ∑ x, (f (roleTranslatePlus N r x) - f x) ^ 2 := by
  classical
  simp_rw [scalarDifferenceLaplacian_apply, Finset.mul_sum]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl ?_
  intro r _
  have hscale :
      ∑ x, f x * (forwardDifferenceScale N ^ 2 *
          (2 * f x - f (roleTranslatePlus N r x) - f (roleTranslateMinus N r x))) =
        forwardDifferenceScale N ^ 2 *
          ∑ x, f x * (2 * f x - f (roleTranslatePlus N r x) -
            f (roleTranslateMinus N r x)) := by
    have hpoint :
        ∑ x, f x * (forwardDifferenceScale N ^ 2 *
            (2 * f x - f (roleTranslatePlus N r x) - f (roleTranslateMinus N r x))) =
          ∑ x, forwardDifferenceScale N ^ 2 *
            (f x * (2 * f x - f (roleTranslatePlus N r x) -
              f (roleTranslateMinus N r x))) := by
      refine Finset.sum_congr rfl ?_
      intro x _
      ring
    rw [hpoint, ← Finset.mul_sum]
  rw [hscale]
  have hplus : ∀ x, roleTranslatePlus N r x = x + roleStep N r := fun x =>
    roleTranslatePlus_apply N r x
  have hminus : ∀ x, roleTranslateMinus N r x = x - roleStep N r := fun x =>
    roleTranslateMinus_apply N r x
  simp_rw [hplus, hminus]
  rw [directional_second_difference_energy, Finset.mul_sum]

theorem scalarDifferenceLaplacian_eq_zero_iff_constant (N : ℕ)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    scalarDifferenceLaplacian N f = 0 ↔ ∀ x y, f x = f y := by
  classical
  constructor
  · intro h
    have henergy := scalarDifferenceLaplacian_energy N f
    rw [h] at henergy
    simp only [Pi.zero_apply, mul_zero, Finset.sum_const_zero] at henergy
    have henergy' :
        ∑ r : Role, forwardDifferenceScale N ^ 2 *
          ∑ x, (f (roleTranslatePlus N r x) - f x) ^ 2 = 0 := henergy.symm
    have hL : forwardDifferenceScale N ≠ 0 := by
      have hfib : archiveFibers N ≠ 0 := by
        unfold archiveFibers
        omega
      simpa [forwardDifferenceScale] using Nat.cast_ne_zero.mpr hfib
    have hsq : ∀ r, ∑ x, (f (roleTranslatePlus N r x) - f x) ^ 2 = 0 := by
      intro r
      have hnonneg : ∀ s ∈ (Finset.univ : Finset Role),
          0 ≤ forwardDifferenceScale N ^ 2 *
            ∑ x, (f (roleTranslatePlus N s x) - f x) ^ 2 := by
        intro s _
        positivity
      rw [Finset.sum_eq_zero_iff_of_nonneg hnonneg] at henergy'
      have hterm := henergy' r (Finset.mem_univ _)
      exact (mul_eq_zero.mp hterm).resolve_left (pow_ne_zero 2 hL)
    have hinv : ∀ r x, f (roleTranslatePlus N r x) = f x := by
      intro r x
      have hzero : (f (roleTranslatePlus N r x) - f x) ^ 2 = 0 := by
        have hsum := hsq r
        have hnonneg : ∀ y ∈ Finset.univ, 0 ≤ (f (roleTranslatePlus N r y) - f y) ^ 2 := by
          intro y _
          positivity
        rw [Finset.sum_eq_zero_iff_of_nonneg hnonneg] at hsum
        exact hsum x (Finset.mem_univ _)
      exact sub_eq_zero.mp (sq_eq_zero_iff.mp hzero)
    exact (phaseInvariant_iff_constant N f).mp hinv
  · intro h
    funext x
    rw [scalarDifferenceLaplacian_apply]
    refine Finset.sum_eq_zero ?_
    intro r _
    rw [h (roleTranslatePlus N r x) x, h (roleTranslateMinus N r x) x]
    ring

theorem cochainDifferenceLaplacian_eq_zero_iff (N : ℕ) (ψ : ArchiveCochain N) :
    cochainDifferenceLaplacian N ψ = 0 ↔
      ∀ s x y, ψ (x, s) = ψ (y, s) := by
  constructor
  · intro h s
    have hslice : scalarDifferenceLaplacian N (fun x => ψ (x, s)) = 0 := by
      funext x
      have happ := congrFun h (x, s)
      simpa [cochainDifferenceLaplacian] using happ
    exact (scalarDifferenceLaplacian_eq_zero_iff_constant N _).mp hslice
  · intro h
    funext p
    have hslice :=
      (scalarDifferenceLaplacian_eq_zero_iff_constant N (fun x => ψ (x, p.2))).mpr
        (fun x y => h p.2 x y)
    simpa [cochainDifferenceLaplacian] using congrFun hslice p.1

theorem hodgeCarDirac_sq_eq_zero_iff_constant (N : ℕ) (ψ : ArchiveCochain N) :
    hodgeCarDirac N (hodgeCarDirac N ψ) = 0 ↔ ∀ s x y, ψ (x, s) = ψ (y, s) := by
  rw [hodgeCarDirac_sq]
  exact cochainDifferenceLaplacian_eq_zero_iff N ψ

theorem cochainPairing_zero_right (N : ℕ) (ψ : ArchiveCochain N) :
    cochainPairing N ψ 0 = 0 := by
  simp [cochainPairing]

theorem cochainPairing_self_eq_zero_iff (N : ℕ) (ψ : ArchiveCochain N) :
    cochainPairing N ψ ψ = 0 ↔ ψ = 0 := by
  classical
  constructor
  · intro h
    unfold cochainPairing at h
    have houter : ∀ x, ∑ s, ψ (x, s) * ψ (x, s) = 0 := by
      have hnonneg : ∀ x ∈ (Finset.univ : Finset (ArchiveRolePhaseGroup N)),
          0 ≤ ∑ s, ψ (x, s) * ψ (x, s) := by
        intro x _
        refine Finset.sum_nonneg ?_
        intro s _
        exact mul_self_nonneg (ψ (x, s))
      rw [Finset.sum_eq_zero_iff_of_nonneg hnonneg] at h
      intro x
      exact h x (Finset.mem_univ _)
    funext p
    have hinner := houter p.1
    have hnonneg : ∀ s ∈ (Finset.univ : Finset ArchiveFockState),
        0 ≤ ψ (p.1, s) * ψ (p.1, s) := by
      intro s _
      exact mul_self_nonneg _
    rw [Finset.sum_eq_zero_iff_of_nonneg hnonneg] at hinner
    have hsq := hinner p.2 (Finset.mem_univ _)
    exact (mul_self_eq_zero.mp hsq)
  · intro h
    simp [h, cochainPairing]

theorem hodgeCarDirac_eq_zero_iff_sq_zero (N : ℕ) (ψ : ArchiveCochain N) :
    hodgeCarDirac N ψ = 0 ↔ hodgeCarDirac N (hodgeCarDirac N ψ) = 0 := by
  constructor
  · intro h
    rw [h, hodgeCarDirac_zero]
  · intro h
    have hadj := hodgeCarDirac_self_adjoint N ψ (hodgeCarDirac N ψ)
    have hself : cochainPairing N (hodgeCarDirac N ψ) (hodgeCarDirac N ψ) = 0 := by
      rw [hadj, h, cochainPairing_zero_right]
    exact (cochainPairing_self_eq_zero_iff N _).mp hself

theorem hodgeCarDirac_eq_zero_iff_section (N : ℕ) (ψ : ArchiveCochain N) :
    hodgeCarDirac N ψ = 0 ↔ ψ = hodgeKernelSection N (fun s => ψ (0, s)) := by
  rw [hodgeCarDirac_eq_zero_iff_sq_zero, hodgeCarDirac_sq_eq_zero_iff_constant]
  constructor
  · intro h
    funext p
    simpa [hodgeKernelSection] using (h p.2 p.1 0)
  · intro h s x y
    have hx := congrFun h (x, s)
    have hy := congrFun h (y, s)
    simpa [hodgeKernelSection] using hx.trans hy.symm

def hodgeCarDiracₗ (N : ℕ) : ArchiveCochain N →ₗ[ℝ] ArchiveCochain N where
  toFun := hodgeCarDirac N
  map_add' := hodgeCarDirac_add N
  map_smul' := hodgeCarDirac_smul N

def hodgeKernelSectionₗ (N : ℕ) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] ArchiveCochain N where
  toFun := hodgeKernelSection N
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

theorem hodgeKernelSection_mem_ker (N : ℕ) (c : ArchiveFockState → ℝ) :
    hodgeKernelSectionₗ N c ∈ LinearMap.ker (hodgeCarDiracₗ N) := by
  rw [LinearMap.mem_ker]
  exact (hodgeCarDirac_eq_zero_iff_section N _).mpr rfl

noncomputable def hodgeKernelEquiv (N : ℕ) :
    LinearMap.ker (hodgeCarDiracₗ N) ≃ₗ[ℝ] (ArchiveFockState → ℝ) where
  toFun ψ := fun s => ψ.1 (0, s)
  invFun c := ⟨hodgeKernelSectionₗ N c, hodgeKernelSection_mem_ker N c⟩
  left_inv ψ := by
    apply Subtype.ext
    have hzero : hodgeCarDirac N ψ.1 = 0 := ψ.2
    have hconst :=
      (hodgeCarDirac_sq_eq_zero_iff_constant N ψ.1).mp
        ((hodgeCarDirac_eq_zero_iff_sq_zero N ψ.1).mp hzero)
    funext p
    exact (hconst p.2 p.1 0).symm
  right_inv c := by
    funext s
    rfl
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

theorem hodgeCarDirac_kernel_finrank (N : ℕ) :
    Module.finrank ℝ (LinearMap.ker (hodgeCarDiracₗ N)) = 16 := by
  rw [LinearEquiv.finrank_eq (hodgeKernelEquiv N), Module.finrank_fintype_fun_eq_card,
    card_archive_fock_state]

end

end D0.Geometry
