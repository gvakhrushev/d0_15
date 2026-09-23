import Mathlib.Data.Complex.Basic
import Mathlib.Tactic
import D0.Geometry.ArchiveHodgeCARDiracKernel
import D0.Geometry.ArchiveTwistedHodgeDirac

/-!
# Zero-mode lifting for scalar seam holonomy

A unitary seam holonomy removes the phase-constant kernel of the twisted
difference Laplacian precisely when it is not `1`. The four-role Hodge/CAR
operator inherits that conclusion: one nontrivial scalar holonomy kills every
Fock component.

The trigonometric eigenvalue `16 L² sin²(θ / (2L))` for `h = exp(iθ)` is not
formalized. It needs a Bloch root of `h` and is left as a follow-up. No `π₀`
holonomy is chosen.
-/

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

variable {L : ℕ} [NeZero L]

def twistedCycleSecond (h : ℂ) (f : ZMod L → ℂ) : ZMod L → ℂ :=
  fun x => 2 * f x - twistedCycleShift h f x - twistedCycleShiftInv h f x

theorem twistedCycleShift_map_sub (h : ℂ) (f g : ZMod L → ℂ) :
    twistedCycleShift h (f - g) = twistedCycleShift h f - twistedCycleShift h g := by
  funext x
  simp [twistedCycleShift, Pi.sub_apply]
  ring

theorem twistedCycleShift_map_smul (h c : ℂ) (f : ZMod L → ℂ) :
    twistedCycleShift h (c • f) = c • twistedCycleShift h f := by
  funext x
  simp [twistedCycleShift, Pi.smul_apply, smul_eq_mul]
  ring

theorem twistedCycleShift_iterate_fixed (h : ℂ) (f : ZMod L → ℂ)
    (hf : twistedCycleShift h f = f) (k : ℕ) :
    (twistedCycleShift h)^[k] f = f := by
  induction k with
  | zero => rfl
  | succ k ih =>
      rw [Function.iterate_succ_apply', ih, hf]

theorem twistedCycleShift_fixed_eq_zero (h : ℂ) (hh : h ≠ 1) (f : ZMod L → ℂ)
    (hf : twistedCycleShift h f = f) : f = 0 := by
  have hpow := twistedCycleShift_pow_cycle h f
  have hiter := twistedCycleShift_iterate_fixed h f hf L
  have hsmul : h • f = f := by rw [← hpow, hiter]
  funext x
  have hx := congrFun hsmul x
  simp only [Pi.smul_apply, smul_eq_mul] at hx
  have hmul : (h - 1) * f x = 0 := by
    rw [sub_mul, one_mul, hx, sub_self]
  exact (mul_eq_zero.mp hmul).resolve_left (sub_ne_zero.mpr hh)

theorem twistedCycleShiftInv_one (f : ZMod L → ℂ) :
    twistedCycleShiftInv 1 f = fun x => f (x - 1) := by
  funext x
  by_cases hx : x = 0
  · simp [twistedCycleShiftInv, hx, inv_one]
  · simp [twistedCycleShiftInv, hx]

/-- Nontrivial unitary scalar holonomy: `ker(2I - U_h - U_h⁻¹) = 0`. -/
theorem twistedCycle_nontrivial_holonomy_kernel_eq_bot (h : ℂ) (hu : star h * h = 1)
    (hh : h ≠ 1) (f : ZMod L → ℂ) (hf : twistedCycleSecond h f = 0) : f = 0 := by
  have hne : h ≠ 0 := unitary_ne_zero h hu
  have hfun : twistedCycleShiftInv h f = (2 : ℂ) • f - twistedCycleShift h f := by
    funext x
    have hx := congrFun hf x
    simp only [twistedCycleSecond, Pi.zero_apply, Pi.sub_apply, Pi.smul_apply,
      smul_eq_mul] at hx ⊢
    linear_combination -hx
  have happly := congrArg (twistedCycleShift h) hfun
  rw [twistedCycleShift_rightInverse h hne f, twistedCycleShift_map_sub,
    twistedCycleShift_map_smul] at happly
  have hpoly : ∀ x, twistedCycleShift h (twistedCycleShift h f) x -
      (2 : ℂ) * twistedCycleShift h f x + f x = 0 := by
    intro x
    have hx := congrFun happly x
    simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul] at hx
    rw [hx]
    ring
  let g := twistedCycleShift h f - f
  have hUg : twistedCycleShift h g = g := by
    funext x
    have hp := hpoly x
    simp only [g, twistedCycleShift_map_sub, Pi.sub_apply]
    linear_combination hp
  have hg : g = 0 := twistedCycleShift_fixed_eq_zero h hh g hUg
  have hshift : twistedCycleShift h f = f := sub_eq_zero.mp hg
  exact twistedCycleShift_fixed_eq_zero h hh f hshift

theorem twistedCycle_one_second_constant (c : ℂ) :
    twistedCycleSecond (L := L) 1 (fun _ => c) = 0 := by
  funext x
  simp [twistedCycleSecond, twistedCycle_one_eq_untwisted, twistedCycleShiftInv_one]
  ring

theorem twistedCycle_kernel_nontrivial_iff (h : ℂ) (hu : star h * h = 1) :
    (∃ f : ZMod L → ℂ, f ≠ 0 ∧ twistedCycleSecond h f = 0) ↔ h = 1 := by
  constructor
  · intro ⟨f, hf0, hker⟩
    by_contra hh
    exact hf0 (twistedCycle_nontrivial_holonomy_kernel_eq_bot h hu hh f hker)
  · intro hh
    subst hh
    refine ⟨fun _ => 1, ?_, twistedCycle_one_second_constant (L := L) 1⟩
    intro hzero
    have := congrFun hzero 0
    simp at this

/-! ## Product Laplacian -/

theorem phasePairing_sub_left (N : ℕ) (f g φ : ArchiveRolePhaseGroup N → ℂ) :
    phasePairing N (f - g) φ = phasePairing N f φ - phasePairing N g φ := by
  unfold phasePairing
  simp [Pi.sub_apply, star_sub, sub_mul, Finset.sum_sub_distrib]

theorem phasePairing_sub_right (N : ℕ) (f g φ : ArchiveRolePhaseGroup N → ℂ) :
    phasePairing N φ (f - g) = phasePairing N φ f - phasePairing N φ g := by
  unfold phasePairing
  simp [Pi.sub_apply, mul_sub, Finset.sum_sub_distrib]

theorem phasePairing_self_norm (N : ℕ) (f : ArchiveRolePhaseGroup N → ℂ) :
    phasePairing N f f = ∑ x, (Complex.normSq (f x) : ℂ) := by
  unfold phasePairing
  refine Finset.sum_congr rfl ?_
  intro x _
  simpa using
    (Complex.normSq_eq_conj_mul_self : (Complex.normSq (f x) : ℂ) = star (f x) * f x).symm

theorem phasePairing_self_eq_zero_iff (N : ℕ) (f : ArchiveRolePhaseGroup N → ℂ) :
    phasePairing N f f = 0 ↔ f = 0 := by
  classical
  constructor
  · intro h
    have hsum : ∑ x, (Complex.normSq (f x) : ℂ) = 0 := by
      simpa [phasePairing_self_norm] using h
    have hreal : ∑ x, Complex.normSq (f x) = 0 := by
      apply Complex.ofReal_injective
      simpa [Complex.ofReal_sum] using hsum
    have hnn : ∀ x ∈ (Finset.univ : Finset (ArchiveRolePhaseGroup N)),
        0 ≤ Complex.normSq (f x) := by
      intro x _
      exact Complex.normSq_nonneg _
    rw [Finset.sum_eq_zero_iff_of_nonneg hnn] at hreal
    funext x
    exact Complex.normSq_eq_zero.mp (hreal x (Finset.mem_univ _))
  · intro h
    simp [phasePairing, h]

theorem twistedRole_energy (N : ℕ) (r : Role) (h : ℂ) (hu : star h * h = 1)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    phasePairing N (twistedRoleShift N r h f - f) (twistedRoleShift N r h f - f) =
      phasePairing N f (fun x =>
        2 * f x - twistedRoleShift N r h f x - twistedRoleShiftInv N r h f x) := by
  have hleft := twistedRoleShift_leftInverse N r h (unitary_ne_zero h hu) f
  have hunit := twistedRoleShift_unitary N r h hu f (twistedRoleShift N r h f)
  have hunit' := twistedRoleShift_unitary N r h hu f f
  have hnorm : phasePairing N (twistedRoleShift N r h f) (twistedRoleShift N r h f) =
      phasePairing N f f := by
    simpa [hleft] using hunit
  calc
    phasePairing N (twistedRoleShift N r h f - f) (twistedRoleShift N r h f - f) =
        (phasePairing N (twistedRoleShift N r h f) (twistedRoleShift N r h f) -
            phasePairing N f (twistedRoleShift N r h f)) -
          (phasePairing N (twistedRoleShift N r h f) f - phasePairing N f f) := by
            rw [phasePairing_sub_right, phasePairing_sub_left, phasePairing_sub_left]
    _ = phasePairing N f f - phasePairing N f (twistedRoleShiftInv N r h f) -
          phasePairing N f (twistedRoleShift N r h f) + phasePairing N f f := by
          rw [hnorm, hunit']
          abel
    _ = phasePairing N f (fun x =>
          2 * f x - twistedRoleShift N r h f x - twistedRoleShiftInv N r h f x) := by
          unfold phasePairing
          simp only [Pi.star_apply]
          have hjoin :
              (∑ x, star (f x) * f x) - (∑ x, star (f x) * twistedRoleShiftInv N r h f x) -
                (∑ x, star (f x) * twistedRoleShift N r h f x) +
                (∑ x, star (f x) * f x) =
                ∑ x, (star (f x) * f x - star (f x) * twistedRoleShiftInv N r h f x -
                  star (f x) * twistedRoleShift N r h f x + star (f x) * f x) := by
            simp [Finset.sum_add_distrib, Finset.sum_sub_distrib]
          rw [hjoin]
          refine Finset.sum_congr rfl ?_
          intro x _
          ring

theorem twistedScalarLaplacian_expand (N : ℕ) (H : Role → ℂ) (hne : ∀ t, H t ≠ 0)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedScalarLaplacian N H f = fun x => ∑ r : Role, (archiveFibers N : ℂ) ^ 2 *
      (2 * f x - twistedRoleShift N r (H r) f x -
        twistedRoleShiftInv N r (H r) f x) := by
  funext x
  unfold twistedScalarLaplacian
  refine Finset.sum_congr rfl ?_
  intro r _
  rw [congrFun (twistedBackward_forward_expand N r (H r) (hne r) f) x]
  ring

theorem twistedRoleShift_iterate_fixed (N : ℕ) (r : Role) (h : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) (hf : twistedRoleShift N r h f = f) (k : ℕ) :
    (twistedRoleShift N r h)^[k] f = f := by
  induction k with
  | zero => rfl
  | succ k ih =>
      rw [Function.iterate_succ_apply', ih, hf]

theorem twistedRole_fixed_eq_zero (N : ℕ) (r : Role) (h : ℂ) (hh : h ≠ 1)
    (f : ArchiveRolePhaseGroup N → ℂ) (hf : twistedRoleShift N r h f = f) : f = 0 := by
  have hpow := twistedRoleShift_pow_cycle N r h f
  have hiter := twistedRoleShift_iterate_fixed N r h f hf (archiveFibers N)
  have hsmul : h • f = f := by rw [← hpow, hiter]
  funext x
  have hx := congrFun hsmul x
  simp only [Pi.smul_apply, smul_eq_mul] at hx
  have hmul : (h - 1) * f x = 0 := by
    rw [sub_mul, one_mul, hx, sub_self]
  exact (mul_eq_zero.mp hmul).resolve_left (sub_ne_zero.mpr hh)

theorem twistedScalar_nontrivial_kernel_eq_bot (N : ℕ) (H : Role → ℂ)
    (hunit : ∀ r, star (H r) * H r = 1) (r0 : Role) (hr0 : H r0 ≠ 1)
    (f : ArchiveRolePhaseGroup N → ℂ) (hf : twistedScalarLaplacian N H f = 0) : f = 0 := by
  classical
  have hne : ∀ t, H t ≠ 0 := fun t => unitary_ne_zero (H t) (hunit t)
  have hexpand := twistedScalarLaplacian_expand N H hne f
  rw [hexpand] at hf
  have hzero_second : ∀ x, ∑ r : Role, (archiveFibers N : ℂ) ^ 2 *
      (2 * f x - twistedRoleShift N r (H r) f x -
        twistedRoleShiftInv N r (H r) f x) = 0 := by
    intro x
    simpa using congrFun hf x
  have hpair : ∑ r : Role, (archiveFibers N : ℂ) ^ 2 *
      phasePairing N (twistedRoleShift N r (H r) f - f)
        (twistedRoleShift N r (H r) f - f) = 0 := by
    simp_rw [fun r => twistedRole_energy N r (H r) (hunit r) f, phasePairing,
      Finset.mul_sum]
    simp only [Pi.star_apply]
    have hswap :
        (∑ r : Role, ∑ x, (archiveFibers N : ℂ) ^ 2 *
            (star (f x) * (2 * f x - twistedRoleShift N r (H r) f x -
              twistedRoleShiftInv N r (H r) f x))) =
          ∑ x, ∑ r : Role, (archiveFibers N : ℂ) ^ 2 *
            (star (f x) * (2 * f x - twistedRoleShift N r (H r) f x -
              twistedRoleShiftInv N r (H r) f x)) := by
      rw [Finset.sum_comm]
    rw [hswap]
    apply Finset.sum_eq_zero
    intro x _
    have hsum := hzero_second x
    have hfactor : ∑ r : Role, (archiveFibers N : ℂ) ^ 2 *
        (star (f x) * (2 * f x - twistedRoleShift N r (H r) f x -
          twistedRoleShiftInv N r (H r) f x)) =
        star (f x) * ∑ r : Role, (archiveFibers N : ℂ) ^ 2 *
          (2 * f x - twistedRoleShift N r (H r) f x -
            twistedRoleShiftInv N r (H r) f x) := by
      rw [Finset.mul_sum]
      refine Finset.sum_congr rfl ?_
      intro r _
      ring
    rw [hfactor, hsum]
    simp
  have hnorm : ∀ r, phasePairing N (twistedRoleShift N r (H r) f - f)
      (twistedRoleShift N r (H r) f - f) =
      ∑ x, (Complex.normSq ((twistedRoleShift N r (H r) f - f) x) : ℂ) :=
    fun r => phasePairing_self_norm N _
  simp_rw [hnorm] at hpair
  have hreal : ∑ r : Role, (archiveFibers N : ℝ) ^ 2 *
      ∑ x, Complex.normSq ((twistedRoleShift N r (H r) f - f) x) = 0 := by
    apply Complex.ofReal_injective
    simpa [Complex.ofReal_sum, Complex.ofReal_mul, Complex.ofReal_pow] using hpair
  have hnn : ∀ r ∈ (Finset.univ : Finset Role), 0 ≤ (archiveFibers N : ℝ) ^ 2 *
      ∑ x, Complex.normSq ((twistedRoleShift N r (H r) f - f) x) := by
    intro r _
    apply mul_nonneg (sq_nonneg _)
    exact Finset.sum_nonneg (fun x _ => Complex.normSq_nonneg _)
  rw [Finset.sum_eq_zero_iff_of_nonneg hnn] at hreal
  have hscale : (archiveFibers N : ℝ) ≠ 0 := by
    rw [archiveFibers]
    exact Nat.cast_ne_zero.mpr (Nat.succ_ne_zero (N + 1))
  have hshift : ∀ r, twistedRoleShift N r (H r) f = f := by
    intro r
    have hterm := hreal r (Finset.mem_univ _)
    have hsq : ∑ x, Complex.normSq ((twistedRoleShift N r (H r) f - f) x) = 0 := by
      exact (mul_eq_zero.mp hterm).resolve_left (pow_ne_zero 2 hscale)
    have hnnx : ∀ x ∈ (Finset.univ : Finset (ArchiveRolePhaseGroup N)),
        0 ≤ Complex.normSq ((twistedRoleShift N r (H r) f - f) x) := by
      intro x _
      exact Complex.normSq_nonneg _
    rw [Finset.sum_eq_zero_iff_of_nonneg hnnx] at hsq
    funext x
    exact sub_eq_zero.mp (Complex.normSq_eq_zero.mp (hsq x (Finset.mem_univ _)))
  exact twistedRole_fixed_eq_zero N r0 (H r0) hr0 f (hshift r0)

theorem cochainPairingC_self_norm (N : ℕ) (ψ : ArchiveCochainC N) :
    cochainPairingC N ψ ψ = ∑ p : ArchiveCochainBasis N, (Complex.normSq (ψ p) : ℂ) := by
  classical
  unfold cochainPairingC
  simp_rw [← Finset.sum_product']
  refine Finset.sum_congr rfl ?_
  intro p _
  simpa using
    (Complex.normSq_eq_conj_mul_self :
      (Complex.normSq (ψ p) : ℂ) = star (ψ p) * ψ p).symm

theorem cochainPairingC_self_eq_zero_iff (N : ℕ) (ψ : ArchiveCochainC N) :
    cochainPairingC N ψ ψ = 0 ↔ ψ = 0 := by
  classical
  constructor
  · intro h
    have hsum : ∑ p : ArchiveCochainBasis N, (Complex.normSq (ψ p) : ℂ) = 0 := by
      simpa [cochainPairingC_self_norm] using h
    have hreal : ∑ p, Complex.normSq (ψ p) = 0 := by
      apply Complex.ofReal_injective
      simpa [Complex.ofReal_sum] using hsum
    have hnn : ∀ p ∈ (Finset.univ : Finset (ArchiveCochainBasis N)),
        0 ≤ Complex.normSq (ψ p) := by
      intro p _
      exact Complex.normSq_nonneg _
    rw [Finset.sum_eq_zero_iff_of_nonneg hnn] at hreal
    funext p
    exact Complex.normSq_eq_zero.mp (hreal p (Finset.mem_univ _))
  · intro h
    simp [cochainPairingC, h]

theorem hodgeCarDiracTwisted_zero (N : ℕ) (H : Role → ℂ) :
    hodgeCarDiracTwisted N H 0 = 0 := by
  have hd := dTwisted_add N H (0 : ArchiveCochainC N) 0
  have hδ := dTwistedAdjoint_add N H (0 : ArchiveCochainC N) 0
  have hd0 : dTwisted N H 0 = 0 := by
    have h' : dTwisted N H 0 + (0 : ArchiveCochainC N) =
        dTwisted N H 0 + dTwisted N H 0 := by simpa using hd
    exact (add_left_cancel (a := dTwisted N H 0) h').symm
  have hδ0 : dTwistedAdjoint N H 0 = 0 := by
    have h' : dTwistedAdjoint N H 0 + (0 : ArchiveCochainC N) =
        dTwistedAdjoint N H 0 + dTwistedAdjoint N H 0 := by simpa using hδ
    exact (add_left_cancel (a := dTwistedAdjoint N H 0) h').symm
  simp [hodgeCarDiracTwisted, hd0, hδ0]

theorem hodgeCarDiracTwisted_eq_zero_iff_sq_zero (N : ℕ) (H : Role → ℂ)
    (hunit : ∀ r, star (H r) * H r = 1) (ψ : ArchiveCochainC N) :
    hodgeCarDiracTwisted N H ψ = 0 ↔
      hodgeCarDiracTwisted N H (hodgeCarDiracTwisted N H ψ) = 0 := by
  constructor
  · intro h
    rw [h, hodgeCarDiracTwisted_zero]
  · intro h
    have hadj := hodgeCarDiracTwisted_self_adjoint N H hunit ψ
      (hodgeCarDiracTwisted N H ψ)
    have hself : cochainPairingC N (hodgeCarDiracTwisted N H ψ)
        (hodgeCarDiracTwisted N H ψ) = 0 := by
      rw [hadj, h, cochainPairingC]
      simp
    exact (cochainPairingC_self_eq_zero_iff N _).mp hself

theorem hodgeCarDiracTwisted_nontrivial_kernel_eq_bot (N : ℕ) (H : Role → ℂ)
    (hunit : ∀ r, star (H r) * H r = 1) (r0 : Role) (hr0 : H r0 ≠ 1)
    (ψ : ArchiveCochainC N) (hψ : hodgeCarDiracTwisted N H ψ = 0) : ψ = 0 := by
  have hsq : hodgeCarDiracTwisted N H (hodgeCarDiracTwisted N H ψ) = 0 :=
    (hodgeCarDiracTwisted_eq_zero_iff_sq_zero N H hunit ψ).mp hψ
  rw [hodgeCarDiracTwisted_sq N H hunit] at hsq
  funext p
  have hslice : twistedScalarLaplacian N H (fun x => ψ (x, p.2)) = 0 := by
    funext x
    simpa [twistedDifferenceLaplacian] using congrFun hsq (x, p.2)
  exact congrFun (twistedScalar_nontrivial_kernel_eq_bot N H hunit r0 hr0 _ hslice) p.1

/-- Trivial holonomy recovers the owned real kernel dimension. -/
theorem twistedHolonomy_one_recovers_kernel_finrank (N : ℕ) :
    Module.finrank ℝ (LinearMap.ker (hodgeCarDiracₗ N)) = 16 :=
  hodgeCarDirac_kernel_finrank N

end

end D0.Geometry
