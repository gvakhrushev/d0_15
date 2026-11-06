import Mathlib.Data.Complex.Basic
import Mathlib.Tactic
import D0.Geometry.A4DSolderMetricCompletion
import D0.Geometry.ArchiveTwistedHodgeDirac
import D0.Geometry.FiniteCycleFourier

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

/-!
# Fourier application of the signed archive difference square

This module composes the existing product-cycle character lemmas with the
archive's actual `Role → ZMod (N + 2)` carrier and its declared Lorentz role
signs. It diagonalizes the signed second-order difference operator appearing
on the right side of the source's Eq. (4), for every archive period.

It does not construct the first-order Lorentzian CAR operator, prove that its
square is this signed difference operator, or select a physical role metric.
-/

/-- A supplied role weight applied to the actual untwisted archive differences.
The weights remain explicit data; this is the scalar second-order expression,
not a first-order Dirac operator. -/
def roleWeightedArchiveDifferenceLaplacian (N : ℕ) (w : Role → ℝ)
    (f : ArchiveRolePhaseGroup N → ℂ) : ArchiveRolePhaseGroup N → ℂ :=
  fun x => ∑ r : Role, (w r : ℂ) *
    (-twistedBackwardDifference N r 1 (twistedForwardDifference N r 1 f) x)

/-- Fourier eigenvalue of the role-weighted archive difference Laplacian. -/
noncomputable def roleWeightedArchiveFourierSymbol (N : ℕ) (w : Role → ℝ)
    (k : Role → ZMod (archiveFibers N)) : ℝ :=
  4 * (archiveFibers N : ℝ) ^ 2 *
    ∑ r : Role, w r *
      Real.sin (Real.pi * ((k r).val : ℝ) / archiveFibers N) ^ 2

private theorem roleTranslatePlus_eq_update (N : ℕ) (r : Role)
    (x : ArchiveRolePhaseGroup N) :
    roleTranslatePlus N r x = Function.update x r (x r + 1) := by
  funext s
  by_cases hs : s = r
  · subst s
    simp [roleTranslatePlus, roleTranslate, roleStep]
  · simp [roleTranslatePlus, roleTranslate, roleStep, hs]

private theorem roleTranslateMinus_eq_update (N : ℕ) (r : Role)
    (x : ArchiveRolePhaseGroup N) :
    roleTranslateMinus N r x = Function.update x r (x r - 1) := by
  funext s
  by_cases hs : s = r
  · subst s
    simp [roleTranslateMinus, roleTranslate, roleStep]
    ring
  · simp [roleTranslateMinus, roleTranslate, roleStep, hs]

private theorem twistedRoleShiftInv_one_archive (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShiftInv N r 1 f = fun x => f (roleTranslateMinus N r x) := by
  funext x
  simp [twistedRoleShiftInv]

/-- Every product-cycle character diagonalizes the actual weighted
second-difference expression on the archive phase group. The formula is valid
for every `N`; no Fourier mode or period is supplied as an extra premise. -/
theorem roleWeightedArchiveDifferenceLaplacian_fourier
    (N : ℕ) (w : Role → ℝ)
    (k : Role → ZMod (archiveFibers N))
    (x : ArchiveRolePhaseGroup N) :
    roleWeightedArchiveDifferenceLaplacian N w
        (FiniteCycleFourier.piCycleChar k) x =
      Complex.ofReal (roleWeightedArchiveFourierSymbol N w k) *
        FiniteCycleFourier.piCycleChar k x := by
  classical
  unfold roleWeightedArchiveDifferenceLaplacian
  calc
    (∑ r : Role, (w r : ℂ) *
        (-twistedBackwardDifference N r 1
          (twistedForwardDifference N r 1 (FiniteCycleFourier.piCycleChar k)) x)) =
      ∑ r : Role, (w r : ℂ) *
        (Complex.ofReal (4 * (archiveFibers N : ℝ) ^ 2 *
          Real.sin (Real.pi * ((k r).val : ℝ) / archiveFibers N) ^ 2) *
          FiniteCycleFourier.piCycleChar k x) := by
        refine Finset.sum_congr rfl ?_
        intro r hr
        have hplus := roleTranslatePlus_eq_update N r x
        have hminus := roleTranslateMinus_eq_update N r x
        have hcoord :=
          FiniteCycleFourier.piCycleChar_coordinate_difference
            (k := k) (i := r) (x := x)
        rw [← hplus, ← hminus] at hcoord
        have hdirection :
            -twistedBackwardDifference N r 1
                (twistedForwardDifference N r 1 (FiniteCycleFourier.piCycleChar k)) x =
              (archiveFibers N : ℂ) ^ 2 *
                (2 * FiniteCycleFourier.piCycleChar k x -
                  FiniteCycleFourier.piCycleChar k (roleTranslatePlus N r x) -
                  FiniteCycleFourier.piCycleChar k (roleTranslateMinus N r x)) := by
          rw [twistedBackwardDifference, twistedRoleShiftInv_one_archive]
          simp only [twistedForwardDifference, twistedRoleShift_one]
          rw [roleTranslate_inverse_plus]
          ring_nf
        rw [hdirection, hcoord]
    _ = Complex.ofReal (roleWeightedArchiveFourierSymbol N w k) *
          FiniteCycleFourier.piCycleChar k x := by
        calc
          (∑ r : Role, (w r : ℂ) *
              (Complex.ofReal (4 * (archiveFibers N : ℝ) ^ 2 *
                Real.sin (Real.pi * ((k r).val : ℝ) / archiveFibers N) ^ 2) *
                FiniteCycleFourier.piCycleChar k x)) =
            ∑ r : Role, Complex.ofReal (w r *
                (4 * (archiveFibers N : ℝ) ^ 2 *
                  Real.sin (Real.pi * ((k r).val : ℝ) / archiveFibers N) ^ 2)) *
                FiniteCycleFourier.piCycleChar k x := by
                  refine Finset.sum_congr rfl ?_
                  intro r hr
                  push_cast
                  ring
          _ = (∑ r : Role, Complex.ofReal (w r *
                (4 * (archiveFibers N : ℝ) ^ 2 *
                  Real.sin (Real.pi * ((k r).val : ℝ) / archiveFibers N) ^ 2))) *
                FiniteCycleFourier.piCycleChar k x := by
                  rw [← Finset.sum_mul]
          _ = Complex.ofReal (roleWeightedArchiveFourierSymbol N w k) *
                FiniteCycleFourier.piCycleChar k x := by
                  rw [← Complex.ofReal_sum]
                  refine congrArg (fun q : ℝ =>
                    (q : ℂ) * FiniteCycleFourier.piCycleChar k x) ?_
                  unfold roleWeightedArchiveFourierSymbol
                  rw [Finset.mul_sum]
                  refine Finset.sum_congr rfl ?_
                  intro r hr
                  ring

/-- The role-weighted scalar expression acts independently on each Fock
coordinate of the existing complex cochain carrier. -/
def roleWeightedArchiveDifferenceOperator (N : ℕ) (w : Role → ℝ)
    (ψ : ArchiveCochainC N) : ArchiveCochainC N :=
  fun p => roleWeightedArchiveDifferenceLaplacian N w
    (fun x => ψ (x, p.2)) p.1

/-- A product-cycle character tensored with an arbitrary Fock coefficient. -/
def archiveFourierFockMode (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) (v : ArchiveFockState → ℂ) :
    ArchiveCochainC N :=
  fun p => v p.2 * FiniteCycleFourier.piCycleChar k p.1

theorem roleWeightedArchiveDifferenceLaplacian_const_mul
    (N : ℕ) (w : Role → ℝ) (c : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    roleWeightedArchiveDifferenceLaplacian N w (fun x => c * f x) =
      fun x => c * roleWeightedArchiveDifferenceLaplacian N w f x := by
  funext x
  unfold roleWeightedArchiveDifferenceLaplacian
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl ?_
  intro r hr
  rw [twistedForwardDifference_const_mul N r 1 c f,
    twistedBackwardDifference_const_mul N r 1 c
      (twistedForwardDifference N r 1 f)]
  ring

/-- For fixed momentum, tensoring a Fock coefficient with the character is
injective: no Fock component is lost in the mode restriction. The existing
carrier theorem gives this fibre dimension as sixteen. -/
theorem archiveFourierFockMode_injective (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) :
    Function.Injective (archiveFourierFockMode N k) := by
  intro v w h
  funext s
  have hzero : FiniteCycleFourier.piCycleChar k (0 : ArchiveRolePhaseGroup N) = 1 := by
    unfold FiniteCycleFourier.piCycleChar
    simp [FiniteCycleFourier.cycleChar_zero_right]
  have hpoint := congrFun h ((0 : ArchiveRolePhaseGroup N), s)
  simpa [archiveFourierFockMode, hzero] using hpoint

/-- With the repository's declared `(1,3)` role signs, the general weighted
symbol specializes to the signed momentum expression of Eq. (5), written in
the canonical `A/B/C/D` role coordinates. -/
noncomputable def archiveLorentzianFourierSymbol (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) : ℝ :=
  4 * (archiveFibers N : ℝ) ^ 2 *
    (Real.sin (Real.pi * ((k D0.A).val : ℝ) / archiveFibers N) ^ 2 -
      Real.sin (Real.pi * ((k D0.B).val : ℝ) / archiveFibers N) ^ 2 -
      Real.sin (Real.pi * ((k D0.C).val : ℝ) / archiveFibers N) ^ 2 -
      Real.sin (Real.pi * ((k D0.D).val : ℝ) / archiveFibers N) ^ 2)

theorem roleWeightedArchiveFourierSymbol_lorentzian (N : ℕ)
    (k : Role → ZMod (archiveFibers N)) :
    roleWeightedArchiveFourierSymbol N roleLorentzSign k =
      archiveLorentzianFourierSymbol N k := by
  classical
  unfold roleWeightedArchiveFourierSymbol archiveLorentzianFourierSymbol
  apply congrArg (fun z : ℝ =>
    4 * (archiveFibers N : ℝ) ^ 2 * z)
  simp [Role, Dyad, roleLorentzSign, roleRoleSigEquiv, roleSign,
    D0.A, D0.B, D0.C, D0.D, Fintype.sum_prod_type]
  ring

/-- The signed archive scalar difference expression has exactly the source
Eq. (5) dispersion on every product character, conditional only on the
explicit role-sign assignment already used by `roleLorentzSign`. -/
theorem archiveLorentzianDifferenceLaplacian_fourier
    (N : ℕ) (k : Role → ZMod (archiveFibers N))
    (x : ArchiveRolePhaseGroup N) :
    roleWeightedArchiveDifferenceLaplacian N roleLorentzSign
        (FiniteCycleFourier.piCycleChar k) x =
      Complex.ofReal (archiveLorentzianFourierSymbol N k) *
        FiniteCycleFourier.piCycleChar k x := by
  rw [roleWeightedArchiveDifferenceLaplacian_fourier,
    roleWeightedArchiveFourierSymbol_lorentzian]

/-- The signed second-order expression has the Eq. (5) eigenvalue on the
entire sixteen-component Fock fibre over each product Fourier character. This
is a theorem about the actual finite site × Fock carrier. -/
theorem archiveLorentzianDifferenceOperator_fourier_mode
    (N : ℕ) (k : Role → ZMod (archiveFibers N))
    (v : ArchiveFockState → ℂ) :
    roleWeightedArchiveDifferenceOperator N roleLorentzSign
        (archiveFourierFockMode N k v) =
      fun p => Complex.ofReal (archiveLorentzianFourierSymbol N k) *
        archiveFourierFockMode N k v p := by
  funext p
  change roleWeightedArchiveDifferenceLaplacian N roleLorentzSign
      (fun x => v p.2 * FiniteCycleFourier.piCycleChar k x) p.1 =
    Complex.ofReal (archiveLorentzianFourierSymbol N k) *
      (v p.2 * FiniteCycleFourier.piCycleChar k p.1)
  rw [roleWeightedArchiveDifferenceLaplacian_const_mul]
  change v p.2 * roleWeightedArchiveDifferenceLaplacian N roleLorentzSign
      (FiniteCycleFourier.piCycleChar k) p.1 =
    Complex.ofReal (archiveLorentzianFourierSymbol N k) *
      (v p.2 * FiniteCycleFourier.piCycleChar k p.1)
  rw [archiveLorentzianDifferenceLaplacian_fourier]
  ring

/-- The existing generic product Fourier inversion specializes directly to
the actual archive site carrier; hence these all-size character eigenvectors
span every scalar site field. -/
theorem archiveRoleFourierInversion (N : ℕ)
    (f : ArchiveRolePhaseGroup N → ℂ) (x : ArchiveRolePhaseGroup N) :
    (archiveFibers N : ℂ) ^ Fintype.card Role * f x =
      ∑ k : Role → ZMod (archiveFibers N),
        FiniteCycleFourier.fourierCoeff f k *
          FiniteCycleFourier.piCycleChar k x := by
  simpa [ArchiveRolePhaseGroup] using
    (FiniteCycleFourier.fourier_inversion
      (ι := Role) (n := archiveFibers N) f x)

end

end D0.Geometry
