import Mathlib.Analysis.SpecialFunctions.Trigonometric.Sinc
import Mathlib.LinearAlgebra.Dimension.Constructions
import D0.Geometry.ArchiveCARFockCarrier
import D0.Geometry.ArchiveHodgeCARDiracSquare
import D0.Geometry.ArchiveRoleEquivalence
import D0.Geometry.FiniteCycleFourier

/-!
# Spatial shell of the Hodge/difference Laplacian

The four-role kernel theorem `hodgeCarDirac_kernel_finrank` stays the zero mode
of the full operator.  This file is the separate spatial compression: the
difference Laplacian summed over the three negative-signature roles `B, C, D`
of the owned signature datum.  On cochains constant along the positive role `A`,
`D_H²` reduces to that spatial operator.  Its lowest positive shell is the six
first harmonics `±e_i` for `L ≥ 3`, with real rank `6 * 16 = 96`, and those
signs collapse when `L = 2`.
-/

namespace D0.Geometry

open D0
open Complex Real Filter D0.Geometry.FiniteCycleFourier
open scoped BigOperators Topology

noncomputable section

inductive SpatialAxis where
  | b | c | d
  deriving DecidableEq, Fintype, Repr

def spatialAxisRole : SpatialAxis → Role
  | .b => B
  | .c => C
  | .d => D

theorem spatialAxisRole_injective : Function.Injective spatialAxisRole := by
  intro a b h
  cases a <;> cases b <;> first | rfl | (simp [spatialAxisRole] at h; exact absurd h (by decide))

theorem spatialAxis_negative_sign (a : SpatialAxis) :
    roleSign (roleRoleSigEquiv (spatialAxisRole a)) = -1 := by
  cases a <;> rfl

theorem positive_role_sign : roleSign (roleRoleSigEquiv A) = 1 := rfl

/-- Positive square root of the first-harmonic symbol, `2 L sin(π / L)`. -/
noncomputable def shellEnergy (L : ℕ) : ℝ :=
  2 * (L : ℝ) * Real.sin (Real.pi / L)

theorem shellEnergy_eq_sinc (L : ℕ) (hL : 0 < L) :
    shellEnergy L = 2 * Real.pi * Real.sinc (Real.pi / L) := by
  have hne : Real.pi / (L : ℝ) ≠ 0 :=
    div_ne_zero Real.pi_ne_zero (Nat.cast_ne_zero.mpr (Nat.pos_iff_ne_zero.mp hL))
  rw [shellEnergy, Real.sinc_of_ne_zero hne]
  field_simp

theorem shellEnergy_sq (L : ℕ) :
    shellEnergy L ^ 2 = 4 * (L : ℝ) ^ 2 * Real.sin (Real.pi / L) ^ 2 := by
  unfold shellEnergy
  ring

theorem shellEnergy_pos (L : ℕ) (hL : 2 ≤ L) : 0 < shellEnergy L := by
  have hLpos : (0 : ℝ) < L := by exact_mod_cast (by omega : 0 < L)
  have hsin : 0 < Real.sin (Real.pi / L) := by
    refine Real.sin_pos_of_pos_of_lt_pi (div_pos Real.pi_pos hLpos) ?_
    rw [div_lt_iff₀ hLpos]
    have h1 : (1 : ℝ) < L := by exact_mod_cast (by omega : 1 < L)
    nlinarith [Real.pi_pos]
  exact mul_pos (mul_pos two_pos hLpos) hsin

theorem shellEnergy_tendsto_two_pi :
    Tendsto (fun L : ℕ => shellEnergy (L + 2)) atTop (nhds (2 * Real.pi)) := by
  have hrewrite : ∀ L : ℕ, shellEnergy (L + 2) =
      2 * Real.pi * Real.sinc (Real.pi / ((L + 2 : ℕ) : ℝ)) := by
    intro L
    exact shellEnergy_eq_sinc (L + 2) (by omega)
  simp_rw [hrewrite]
  have hnat : Tendsto (fun L : ℕ => ((L + 2 : ℕ) : ℝ)) atTop atTop :=
    (tendsto_add_atTop_iff_nat 2).mpr tendsto_natCast_atTop_atTop
  have hinv : Tendsto (fun L : ℕ => (((L + 2 : ℕ) : ℝ))⁻¹) atTop (nhds 0) :=
    tendsto_inv_atTop_zero.comp hnat
  have hangle : Tendsto (fun L : ℕ => Real.pi / ((L + 2 : ℕ) : ℝ)) atTop (nhds 0) := by
    have hform : (fun L : ℕ => Real.pi / ((L + 2 : ℕ) : ℝ)) =
        fun L => Real.pi * (((L + 2 : ℕ) : ℝ))⁻¹ := by
      funext L
      rw [div_eq_mul_inv]
    rw [hform]
    have hπ : Tendsto (fun _ : ℕ => Real.pi) atTop (nhds Real.pi) := tendsto_const_nhds
    simpa [mul_zero] using hπ.mul hinv
  have hsinc : Tendsto (fun L : ℕ => Real.sinc (Real.pi / ((L + 2 : ℕ) : ℝ))) atTop
      (nhds (Real.sinc 0)) :=
    (Real.continuous_sinc.tendsto 0).comp hangle
  have hconst : Tendsto (fun _ : ℕ => 2 * Real.pi) atTop (nhds (2 * Real.pi)) :=
    tendsto_const_nhds
  simpa [Real.sinc_zero, mul_one] using hconst.mul hsinc

/-- Spatial difference Laplacian: the three negative-signature directions only. -/
noncomputable def scalarSpatialLaplacian (N : ℕ)
    (f : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) : ℝ :=
  ∑ a : SpatialAxis, forwardDifferenceScale N ^ 2 *
    (2 * f x - f (roleTranslatePlus N (spatialAxisRole a) x) -
      f (roleTranslateMinus N (spatialAxisRole a) x))

theorem axis_invariant_kills_direction (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ)
    (h : ∀ x, f (roleTranslatePlus N r x) = f x) (x : ArchiveRolePhaseGroup N) :
    2 * f x - f (roleTranslatePlus N r x) - f (roleTranslateMinus N r x) = 0 := by
  have hcancel : roleTranslatePlus N r (roleTranslateMinus N r x) = x := by
    dsimp [roleTranslatePlus, roleTranslateMinus, roleTranslate]
    abel
  have hback : f (roleTranslateMinus N r x) = f x := by
    have hfx := h (roleTranslateMinus N r x)
    rw [hcancel] at hfx
    exact hfx.symm
  rw [h x, hback]
  ring

theorem scalarDifferenceLaplacian_eq_spatial_of_axisInvariant (N : ℕ)
    (f : ArchiveRolePhaseGroup N → ℝ)
    (h : ∀ x, f (roleTranslatePlus N A x) = f x) (x : ArchiveRolePhaseGroup N) :
    scalarDifferenceLaplacian N f x = scalarSpatialLaplacian N f x := by
  classical
  rw [scalarDifferenceLaplacian_apply]
  have hA := axis_invariant_kills_direction N A f h x
  have hdisj : Disjoint ({A} : Finset Role)
      (Finset.image spatialAxisRole (Finset.univ : Finset SpatialAxis)) := by
    rw [Finset.disjoint_left]
    intro r hr hrimg
    simp only [Finset.mem_singleton] at hr
    subst hr
    simp only [Finset.mem_image, Finset.mem_univ, true_and] at hrimg
    rcases hrimg with ⟨a, ha⟩
    cases a <;> simp [spatialAxisRole] at ha <;> exact absurd ha (by decide)
  have hroles : (Finset.univ : Finset Role) =
      {A} ∪ Finset.image spatialAxisRole Finset.univ := by
    decide
  rw [hroles, Finset.sum_union hdisj, Finset.sum_singleton,
    Finset.sum_image spatialAxisRole_injective.injOn, hA]
  simp [scalarSpatialLaplacian]

/-- On cochains constant along the positive role, `D_H²` is the spatial Laplacian. -/
theorem hodgeCarDirac_sq_spatial_of_axisInvariant (N : ℕ) (ψ : ArchiveCochain N)
    (h : ∀ x s, ψ (roleTranslatePlus N A x, s) = ψ (x, s)) (p : ArchiveCochainBasis N) :
    hodgeCarDirac N (hodgeCarDirac N ψ) p =
      scalarSpatialLaplacian N (fun x => ψ (x, p.2)) p.1 := by
  rw [hodgeCarDirac_sq_fibre]
  exact scalarDifferenceLaplacian_eq_spatial_of_axisInvariant N
    (fun x => ψ (x, p.2)) (fun x => h x p.2) p.1

theorem one_ne_neg_one_of_three (L : ℕ) (hL : 3 ≤ L) : (1 : ZMod L) ≠ -1 := by
  intro h
  have hsum : (1 : ZMod L) + 1 = 0 := by
    rw [← neg_eq_iff_add_eq_zero]
    exact h.symm
  have h2 : (2 : ZMod L) = 0 := by
    rw [← one_add_one_eq_two]
    exact hsum
  have hdiv : L ∣ 2 := (ZMod.natCast_eq_zero_iff 2 L).mp h2
  have hle : L ≤ 2 := Nat.le_of_dvd (by decide : 0 < 2) hdiv
  omega

/-- First-harmonic labels `± e_i` on the three spatial axes.  The Boolean is the sign. -/
def firstShellMomentum (L : ℕ) (a : SpatialAxis) (positive : Bool) :
    SpatialAxis → ZMod L :=
  fun b => if b = a then (if positive then 1 else -1) else 0

theorem firstShellMomentum_injective (L : ℕ) (hL : 3 ≤ L) :
    Function.Injective fun p : SpatialAxis × Bool => firstShellMomentum L p.1 p.2 := by
  intro p q h
  rcases p with ⟨a, sa⟩
  rcases q with ⟨b, sb⟩
  have hval := congrFun h
  have ha : firstShellMomentum L a sa a = (if sa then 1 else -1) := by
    simp [firstShellMomentum]
  have hb : firstShellMomentum L b sb a = (if a = b then (if sb then 1 else -1) else 0) := by
    simp [firstShellMomentum]
  have hne : (1 : ZMod L) ≠ 0 := by
    intro hz
    have hdiv : L ∣ 1 := (ZMod.natCast_eq_zero_iff 1 L).mp (by simpa using hz)
    have : L = 1 := Nat.dvd_one.mp hdiv
    omega
  have hneg : (-1 : ZMod L) ≠ 0 := by
    intro hz
    exact hne (by simpa using congrArg Neg.neg hz)
  have hsign : (1 : ZMod L) ≠ -1 := one_ne_neg_one_of_three L hL
  have hab : a = b := by
    by_contra hnab
    have : firstShellMomentum L a sa a = firstShellMomentum L b sb a := hval a
    rw [ha, hb, if_neg hnab] at this
    cases sa
    · exact hneg this
    · exact hne this
  subst hab
  have hsigns : (if sa then (1 : ZMod L) else -1) = (if sb then 1 else -1) := by
    simpa [firstShellMomentum] using hval a
  cases sa <;> cases sb <;> simp at hsigns
  · rfl
  · exact absurd hsigns hsign.symm
  · exact absurd hsigns hsign
  · rfl

theorem firstShellLabel_card (L : ℕ) (hL : 3 ≤ L) :
    Function.Injective (fun p : SpatialAxis × Bool => firstShellMomentum L p.1 p.2) ∧
      Fintype.card (SpatialAxis × Bool) = 6 := by
  refine ⟨firstShellMomentum_injective L hL, ?_⟩
  have hA : Fintype.card SpatialAxis = 3 := by decide
  simp [Fintype.card_prod, hA, Fintype.card_bool]

theorem firstShellMomentum_collapse (a : SpatialAxis) :
    firstShellMomentum 2 a true = firstShellMomentum 2 a false := by
  funext b
  fin_cases a <;> fin_cases b <;> decide

/-! ## Real first harmonics -/

noncomputable def shellCos (N : ℕ) (a : SpatialAxis) (x : ArchiveRolePhaseGroup N) : ℝ :=
  Real.cos (2 * Real.pi * ((x (spatialAxisRole a)).val : ℝ) / archiveFibers N)

noncomputable def shellSin (N : ℕ) (a : SpatialAxis) (x : ArchiveRolePhaseGroup N) : ℝ :=
  Real.sin (2 * Real.pi * ((x (spatialAxisRole a)).val : ℝ) / archiveFibers N)

theorem shellCos_eq_cycle (N : ℕ) (a : SpatialAxis) (x : ArchiveRolePhaseGroup N) :
    shellCos N a x =
      cycleCos (1 : ZMod (archiveFibers N)) (x (spatialAxisRole a)) := by
  rw [shellCos, cycleCos_eq]
  congr 1
  simp

theorem shellSin_eq_cycle (N : ℕ) (a : SpatialAxis) (x : ArchiveRolePhaseGroup N) :
    shellSin N a x =
      cycleSin (1 : ZMod (archiveFibers N)) (x (spatialAxisRole a)) := by
  rw [shellSin, cycleSin_eq]
  congr 1
  simp

theorem shellCos_translate_ne (N : ℕ) (a : SpatialAxis) {r : Role}
    (hr : r ≠ spatialAxisRole a) (x : ArchiveRolePhaseGroup N) :
    shellCos N a (roleTranslatePlus N r x) = shellCos N a x := by
  simp only [shellCos, roleTranslatePlus_apply, Pi.add_apply, roleStep]
  have hif : (if spatialAxisRole a = r then (1 : ZMod (archiveFibers N)) else 0) = 0 := by
    simp [hr.symm]
  simp [hif]

theorem shellCos_translateMinus_ne (N : ℕ) (a : SpatialAxis) {r : Role}
    (hr : r ≠ spatialAxisRole a) (x : ArchiveRolePhaseGroup N) :
    shellCos N a (roleTranslateMinus N r x) = shellCos N a x := by
  simp only [shellCos, roleTranslateMinus_apply, Pi.sub_apply, roleStep]
  have hif : (if spatialAxisRole a = r then (1 : ZMod (archiveFibers N)) else 0) = 0 := by
    simp [hr.symm]
  simp [hif]

theorem shellSin_translate_ne (N : ℕ) (a : SpatialAxis) {r : Role}
    (hr : r ≠ spatialAxisRole a) (x : ArchiveRolePhaseGroup N) :
    shellSin N a (roleTranslatePlus N r x) = shellSin N a x := by
  simp only [shellSin, roleTranslatePlus_apply, Pi.add_apply, roleStep]
  have hif : (if spatialAxisRole a = r then (1 : ZMod (archiveFibers N)) else 0) = 0 := by
    simp [hr.symm]
  simp [hif]

theorem shellSin_translateMinus_ne (N : ℕ) (a : SpatialAxis) {r : Role}
    (hr : r ≠ spatialAxisRole a) (x : ArchiveRolePhaseGroup N) :
    shellSin N a (roleTranslateMinus N r x) = shellSin N a x := by
  simp only [shellSin, roleTranslateMinus_apply, Pi.sub_apply, roleStep]
  have hif : (if spatialAxisRole a = r then (1 : ZMod (archiveFibers N)) else 0) = 0 := by
    simp [hr.symm]
  simp [hif]

theorem shellCos_A_invariant (N : ℕ) (a : SpatialAxis) (x : ArchiveRolePhaseGroup N) :
    shellCos N a (roleTranslatePlus N A x) = shellCos N a x := by
  have hr : A ≠ spatialAxisRole a := by
    cases a <;> decide
  exact shellCos_translate_ne N a hr x

theorem shellSin_A_invariant (N : ℕ) (a : SpatialAxis) (x : ArchiveRolePhaseGroup N) :
    shellSin N a (roleTranslatePlus N A x) = shellSin N a x := by
  have hr : A ≠ spatialAxisRole a := by
    cases a <;> decide
  exact shellSin_translate_ne N a hr x

theorem shellCos_active (N : ℕ) (a : SpatialAxis) (x : ArchiveRolePhaseGroup N)
    (hL : 2 ≤ archiveFibers N) :
    (archiveFibers N : ℝ) ^ 2 *
        (2 * shellCos N a x -
          shellCos N a (roleTranslatePlus N (spatialAxisRole a) x) -
          shellCos N a (roleTranslateMinus N (spatialAxisRole a) x)) =
      shellEnergy (archiveFibers N) ^ 2 * shellCos N a x := by
  haveI : Fact (1 < archiveFibers N) := ⟨by omega⟩
  have hplus : (roleTranslatePlus N (spatialAxisRole a) x) (spatialAxisRole a) =
      x (spatialAxisRole a) + 1 := by
    simp [roleTranslatePlus_apply, roleStep]
  have hminus : (roleTranslateMinus N (spatialAxisRole a) x) (spatialAxisRole a) =
      x (spatialAxisRole a) - 1 := by
    simp [roleTranslateMinus_apply, roleStep]
  have hcos := cycleCos_second_difference (n := archiveFibers N)
    (1 : ZMod (archiveFibers N)) (x (spatialAxisRole a))
  simp only [ZMod.val_one, Nat.cast_one, mul_one] at hcos
  rw [shellEnergy_sq]
  simp_rw [shellCos_eq_cycle, hplus, hminus]
  exact hcos

theorem shellSin_active (N : ℕ) (a : SpatialAxis) (x : ArchiveRolePhaseGroup N)
    (hL : 2 ≤ archiveFibers N) :
    (archiveFibers N : ℝ) ^ 2 *
        (2 * shellSin N a x -
          shellSin N a (roleTranslatePlus N (spatialAxisRole a) x) -
          shellSin N a (roleTranslateMinus N (spatialAxisRole a) x)) =
      shellEnergy (archiveFibers N) ^ 2 * shellSin N a x := by
  haveI : Fact (1 < archiveFibers N) := ⟨by omega⟩
  have hplus : (roleTranslatePlus N (spatialAxisRole a) x) (spatialAxisRole a) =
      x (spatialAxisRole a) + 1 := by
    simp [roleTranslatePlus_apply, roleStep]
  have hminus : (roleTranslateMinus N (spatialAxisRole a) x) (spatialAxisRole a) =
      x (spatialAxisRole a) - 1 := by
    simp [roleTranslateMinus_apply, roleStep]
  have hsin := cycleSin_second_difference (n := archiveFibers N)
    (1 : ZMod (archiveFibers N)) (x (spatialAxisRole a))
  simp only [ZMod.val_one, Nat.cast_one, mul_one] at hsin
  rw [shellEnergy_sq]
  simp_rw [shellSin_eq_cycle, hplus, hminus]
  exact hsin

theorem shellCos_spatial_eigen (N : ℕ) (a : SpatialAxis) (x : ArchiveRolePhaseGroup N)
    (hL : 2 ≤ archiveFibers N) :
    scalarSpatialLaplacian N (shellCos N a) x =
      shellEnergy (archiveFibers N) ^ 2 * shellCos N a x := by
  classical
  unfold scalarSpatialLaplacian
  rw [Finset.sum_eq_single a]
  · exact shellCos_active N a x hL
  · intro b _ hb
    have hr : spatialAxisRole b ≠ spatialAxisRole a := fun h => hb (spatialAxisRole_injective h)
    have hinv : ∀ y, shellCos N a (roleTranslatePlus N (spatialAxisRole b) y) =
        shellCos N a y := fun y => shellCos_translate_ne N a hr y
    rw [axis_invariant_kills_direction N (spatialAxisRole b) (shellCos N a) hinv x]
    ring
  · intro ha
    exact absurd (Finset.mem_univ a) ha

theorem shellSin_spatial_eigen (N : ℕ) (a : SpatialAxis) (x : ArchiveRolePhaseGroup N)
    (hL : 2 ≤ archiveFibers N) :
    scalarSpatialLaplacian N (shellSin N a) x =
      shellEnergy (archiveFibers N) ^ 2 * shellSin N a x := by
  classical
  unfold scalarSpatialLaplacian
  rw [Finset.sum_eq_single a]
  · exact shellSin_active N a x hL
  · intro b _ hb
    have hr : spatialAxisRole b ≠ spatialAxisRole a := fun h => hb (spatialAxisRole_injective h)
    have hinv : ∀ y, shellSin N a (roleTranslatePlus N (spatialAxisRole b) y) =
        shellSin N a y := fun y => shellSin_translate_ne N a hr y
    rw [axis_invariant_kills_direction N (spatialAxisRole b) (shellSin N a) hinv x]
    ring
  · intro ha
    exact absurd (Finset.mem_univ a) ha

/-- Cosine or sine along one spatial axis. At `L = 2` the sine mode is identically zero. -/
inductive ShellHarmonic
  | cos
  | sin
  deriving DecidableEq, Fintype, Repr

def shellMode (N : ℕ) : SpatialAxis × ShellHarmonic → ArchiveRolePhaseGroup N → ℝ
  | (a, .cos) => shellCos N a
  | (a, .sin) => shellSin N a

theorem shellMode_A_invariant (N : ℕ) (p : SpatialAxis × ShellHarmonic)
    (x : ArchiveRolePhaseGroup N) :
    shellMode N p (roleTranslatePlus N A x) = shellMode N p x := by
  rcases p with ⟨a, h⟩
  cases h
  · exact shellCos_A_invariant N a x
  · exact shellSin_A_invariant N a x

theorem shellMode_spatial_eigen (N : ℕ) (p : SpatialAxis × ShellHarmonic)
    (x : ArchiveRolePhaseGroup N) (hL : 2 ≤ archiveFibers N) :
    scalarSpatialLaplacian N (shellMode N p) x =
      shellEnergy (archiveFibers N) ^ 2 * shellMode N p x := by
  rcases p with ⟨a, h⟩
  cases h
  · exact shellCos_spatial_eigen N a x hL
  · exact shellSin_spatial_eigen N a x hL

def shellCochain (N : ℕ) (p : (SpatialAxis × ShellHarmonic) × ArchiveFockState) :
    ArchiveCochain N :=
  fun q => if q.2 = p.2 then shellMode N p.1 q.1 else 0

theorem shellCochain_eigen (N : ℕ) (p : (SpatialAxis × ShellHarmonic) × ArchiveFockState)
    (hL : 2 ≤ archiveFibers N) :
    hodgeCarDirac N (hodgeCarDirac N (shellCochain N p)) =
      shellEnergy (archiveFibers N) ^ 2 • shellCochain N p := by
  funext q
  rw [hodgeCarDirac_sq_fibre]
  by_cases hq : q.2 = p.2
  · have hslice : (fun x => shellCochain N p (x, q.2)) = shellMode N p.1 := by
      funext x
      simp [shellCochain, hq]
    have hinv : ∀ x, shellMode N p.1 (roleTranslatePlus N A x) = shellMode N p.1 x :=
      shellMode_A_invariant N p.1
    rw [hslice, scalarDifferenceLaplacian_eq_spatial_of_axisInvariant N _ hinv,
      shellMode_spatial_eigen N p.1 q.1 hL]
    simp [shellCochain, hq, Pi.smul_apply, smul_eq_mul]
  · have hslice : (fun x => shellCochain N p (x, q.2)) = 0 := by
      funext x
      simp [shellCochain, hq]
    rw [hslice]
    simp [scalarDifferenceLaplacian_apply, shellCochain, hq, smul_eq_mul]

/-- `L = 2` kills the sine harmonic: `sin(π j) = 0` for `j ∈ ℤ/2ℤ`. -/
theorem shellSin_eq_zero_l2 (a : SpatialAxis) (x : ArchiveRolePhaseGroup 0) :
    shellSin 0 a x = 0 := by
  have hv : (x (spatialAxisRole a)).val = 0 ∨ (x (spatialAxisRole a)).val = 1 := by
    have hlt := ZMod.val_lt (x (spatialAxisRole a))
    have hfib : archiveFibers 0 = 2 := rfl
    omega
  rcases hv with h0 | h1
  · rw [shellSin, h0]
    simp [archiveFibers, Real.sin_zero]
  · rw [shellSin, h1, archiveFibers]
    have : 2 * Real.pi * ((1 : ℕ) : ℝ) / ((0 + 2 : ℕ) : ℝ) = Real.pi := by
      norm_num
    rw [this, Real.sin_pi]

def axisProbe (N : ℕ) (a : SpatialAxis) (j : ZMod (archiveFibers N)) :
    ArchiveRolePhaseGroup N :=
  fun r => if r = spatialAxisRole a then j else 0

theorem shellCos_probe_self (N : ℕ) (a : SpatialAxis) (j : ZMod (archiveFibers N)) :
    shellCos N a (axisProbe N a j) =
      Real.cos (2 * Real.pi * (j.val : ℝ) / archiveFibers N) := by
  simp [shellCos, axisProbe]

theorem shellSin_probe_self (N : ℕ) (a : SpatialAxis) (j : ZMod (archiveFibers N)) :
    shellSin N a (axisProbe N a j) =
      Real.sin (2 * Real.pi * (j.val : ℝ) / archiveFibers N) := by
  simp [shellSin, axisProbe]

theorem shellCos_probe_other (N : ℕ) {a b : SpatialAxis} (h : a ≠ b)
    (j : ZMod (archiveFibers N)) :
    shellCos N b (axisProbe N a j) = 1 := by
  have hr : spatialAxisRole b ≠ spatialAxisRole a :=
    fun hrole => h (spatialAxisRole_injective hrole.symm)
  simp [shellCos, axisProbe, hr, ZMod.val_zero, Real.cos_zero]

theorem shellSin_probe_other (N : ℕ) {a b : SpatialAxis} (h : a ≠ b)
    (j : ZMod (archiveFibers N)) :
    shellSin N b (axisProbe N a j) = 0 := by
  have hr : spatialAxisRole b ≠ spatialAxisRole a :=
    fun hrole => h (spatialAxisRole_injective hrole.symm)
  simp [shellSin, axisProbe, hr, ZMod.val_zero, Real.sin_zero]

theorem shellMode_linearIndependent (N : ℕ) (hL : 3 ≤ archiveFibers N) :
    LinearIndependent ℝ (fun p : SpatialAxis × ShellHarmonic => shellMode N p) := by
  classical
  rw [Fintype.linearIndependent_iff]
  intro c hc p
  let L := archiveFibers N
  haveI : Fact (1 < L) := ⟨by omega⟩
  have hline (a : SpatialAxis) (j : ZMod L) :
      c (a, .cos) * Real.cos (2 * Real.pi * (j.val : ℝ) / L) +
        c (a, .sin) * Real.sin (2 * Real.pi * (j.val : ℝ) / L) +
        ∑ b ∈ Finset.univ.erase a, c (b, .cos) = 0 := by
    have h0 := congrFun hc (axisProbe N a j)
    simp only [Pi.zero_apply, Finset.sum_apply, Pi.smul_apply, smul_eq_mul] at h0
    rw [show (Finset.univ : Finset (SpatialAxis × ShellHarmonic)) =
        (Finset.univ : Finset SpatialAxis) ×ˢ (Finset.univ : Finset ShellHarmonic) from
        Finset.univ_product_univ.symm] at h0
    rw [Finset.sum_product] at h0
    have hpair : (Finset.univ : Finset ShellHarmonic) =
        {ShellHarmonic.cos, ShellHarmonic.sin} := by decide
    simp_rw [hpair, Finset.sum_pair (by decide : ShellHarmonic.cos ≠ .sin)] at h0
    have hsplit := (Finset.add_sum_erase (Finset.univ : Finset SpatialAxis)
      (fun b => c (b, .cos) * shellMode N (b, .cos) (axisProbe N a j) +
        c (b, .sin) * shellMode N (b, .sin) (axisProbe N a j)) (Finset.mem_univ a)).symm
    rw [hsplit] at h0
    have hother : ∑ b ∈ Finset.univ.erase a,
        (c (b, .cos) * shellMode N (b, .cos) (axisProbe N a j) +
          c (b, .sin) * shellMode N (b, .sin) (axisProbe N a j)) =
        ∑ b ∈ Finset.univ.erase a, c (b, .cos) := by
      refine Finset.sum_congr rfl fun b hb => ?_
      have hbne : b ≠ a := (Finset.mem_erase.mp hb).1
      rw [shellMode, shellMode, shellCos_probe_other N hbne.symm, shellSin_probe_other N hbne.symm]
      ring
    rw [hother] at h0
    simp only [shellMode, shellCos_probe_self, shellSin_probe_self] at h0
    linarith
  have hsin_ne : Real.sin (2 * Real.pi / L) ≠ 0 := by
    have hpos : 0 < Real.sin (2 * Real.pi / L) := by
      have hLpos : (0 : ℝ) < L := by exact_mod_cast (by omega : 0 < L)
      refine Real.sin_pos_of_pos_of_lt_pi ?_ ?_
      · exact div_pos (mul_pos two_pos Real.pi_pos) hLpos
      · rw [div_lt_iff₀ hLpos]
        have hbound : (2 : ℝ) < L := by exact_mod_cast (by omega : 2 < L)
        nlinarith [Real.pi_pos]
    exact hpos.ne'
  have hcos_ne : Real.cos (2 * Real.pi / L) ≠ 1 := by
    intro hcos
    have hlt1 : -(2 * Real.pi) < 2 * Real.pi / L := by
      have : 0 < 2 * Real.pi / L := by positivity
      linarith [Real.pi_pos]
    have hlt2 : 2 * Real.pi / L < 2 * Real.pi := by
      have hLpos : (0 : ℝ) < L := by exact_mod_cast (by omega : 0 < L)
      rw [div_lt_iff₀ hLpos]
      have : (1 : ℝ) < L := by exact_mod_cast (by omega : 1 < L)
      nlinarith [Real.pi_pos]
    have hzero : 2 * Real.pi / L = 0 :=
      (Real.cos_eq_one_iff_of_lt_of_lt hlt1 hlt2).mp hcos
    have hLpos : (0 : ℝ) < L := by exact_mod_cast (by omega : 0 < L)
    have : (0 : ℝ) < 2 * Real.pi / L := div_pos (mul_pos two_pos Real.pi_pos) hLpos
    linarith
  have hbeta (a : SpatialAxis) : c (a, .sin) = 0 := by
    have h0 := hline a 0
    have h1 := hline a 1
    have hn := hline a (-1)
    have hval0 : ((0 : ZMod L).val : ℝ) = 0 := by simp [ZMod.val_zero]
    have hval1 : ((1 : ZMod L).val : ℝ) = 1 := by simp [ZMod.val_one]
    haveI : NeZero (1 : ZMod L) := ⟨by
      intro hz
      have hdiv : L ∣ 1 := (ZMod.natCast_eq_zero_iff 1 L).mp (by simpa using hz)
      have : L = 1 := Nat.dvd_one.mp hdiv
      omega⟩
    have hvaln : ((-1 : ZMod L).val : ℝ) = (L : ℝ) - 1 := by
      have hnat := ZMod.val_neg_of_ne_zero (1 : ZMod L)
      have h1v : (1 : ZMod L).val = 1 := ZMod.val_one L
      rw [hnat, h1v, Nat.cast_sub (by omega : 1 ≤ L), Nat.cast_one]
    have hcosNeg : Real.cos (2 * Real.pi * ((-1 : ZMod L).val : ℝ) / L) =
        Real.cos (2 * Real.pi / L) := by
      rw [hvaln]
      have hL0 : (L : ℝ) ≠ 0 := by exact_mod_cast (by omega : L ≠ 0)
      have harg : 2 * Real.pi * ((L : ℝ) - 1) / L = 2 * Real.pi - 2 * Real.pi / L := by
        field_simp [hL0]
      rw [harg, Real.cos_two_pi_sub]
    have hsinNeg : Real.sin (2 * Real.pi * ((-1 : ZMod L).val : ℝ) / L) =
        -Real.sin (2 * Real.pi / L) := by
      rw [hvaln]
      have hL0 : (L : ℝ) ≠ 0 := by exact_mod_cast (by omega : L ≠ 0)
      have harg : 2 * Real.pi * ((L : ℝ) - 1) / L = 2 * Real.pi - 2 * Real.pi / L := by
        field_simp [hL0]
      rw [harg]
      have : Real.sin (2 * Real.pi - 2 * Real.pi / L) = -Real.sin (2 * Real.pi / L) := by
        rw [Real.sin_sub, Real.sin_two_pi, Real.cos_two_pi]
        ring
      exact this
    rw [hval0] at h0
    rw [hval1] at h1
    have hzeroang : 2 * Real.pi * (0 : ℝ) / L = 0 := by ring
    have honeang : 2 * Real.pi * (1 : ℝ) / L = 2 * Real.pi / L := by ring
    rw [hzeroang] at h0
    rw [honeang] at h1
    simp only [Real.cos_zero, Real.sin_zero, mul_zero, add_zero, mul_one] at h0
    simp only [hcosNeg, hsinNeg] at hn
    have hsum : (2 : ℝ) * (c (a, .sin) * Real.sin (2 * Real.pi / L)) = 0 := by
      linarith
    have hprod : c (a, .sin) * Real.sin (2 * Real.pi / L) = 0 :=
      mul_left_cancel₀ two_ne_zero (by simpa using hsum)
    exact (mul_eq_zero.mp hprod).resolve_right hsin_ne
  have halpha (a : SpatialAxis) : c (a, .cos) = 0 := by
    have h0 := hline a 0
    have h1 := hline a 1
    simp only [ZMod.val_zero, ZMod.val_one, Nat.cast_zero, Nat.cast_one] at h0 h1
    have hCeq : ∑ b ∈ Finset.univ.erase a, c (b, .cos) = -c (a, .cos) := by
      simpa [Real.cos_zero, Real.sin_zero] using h0
    have h1' : c (a, .cos) * Real.cos (2 * Real.pi / L) +
        ∑ b ∈ Finset.univ.erase a, c (b, .cos) = 0 := by
      simpa [hbeta a, Real.sin_zero] using h1
    rw [hCeq] at h1'
    have : c (a, .cos) * (Real.cos (2 * Real.pi / L) - 1) = 0 := by
      linarith
    exact (mul_eq_zero.mp this).resolve_right (sub_ne_zero.mpr hcos_ne)
  rcases p with ⟨a, s⟩
  cases s
  · exact halpha a
  · exact hbeta a

theorem shellCochain_linearIndependent (N : ℕ) (hL : 3 ≤ archiveFibers N) :
    LinearIndependent ℝ (fun p : (SpatialAxis × ShellHarmonic) × ArchiveFockState =>
      shellCochain N p) := by
  classical
  rw [Fintype.linearIndependent_iff]
  intro g hg p
  let s := p.2
  have hslice : ∑ q : SpatialAxis × ShellHarmonic, g (q, s) • shellMode N q = 0 := by
    funext x
    have h0 := congrFun hg (x, s)
    simp only [Pi.zero_apply, Finset.sum_apply, Pi.smul_apply, smul_eq_mul, shellCochain] at h0
    rw [show (Finset.univ : Finset ((SpatialAxis × ShellHarmonic) × ArchiveFockState)) =
        (Finset.univ : Finset (SpatialAxis × ShellHarmonic)) ×ˢ
          (Finset.univ : Finset ArchiveFockState) from Finset.univ_product_univ.symm] at h0
    rw [Finset.sum_product] at h0
    have hpull : ∑ q : SpatialAxis × ShellHarmonic, ∑ t : ArchiveFockState,
        g (q, t) * (if t = s then shellMode N q x else 0) =
        ∑ q : SpatialAxis × ShellHarmonic, g (q, s) * shellMode N q x := by
      refine Finset.sum_congr rfl fun q _ => ?_
      rw [Finset.sum_eq_single s]
      · simp
      · intro t _ ht
        simp [ht]
      · intro hs
        exact absurd (Finset.mem_univ s) hs
    have hform : ∑ q, g (q, s) * shellMode N q x = 0 := by
      simpa [hpull] using h0
    simpa [Pi.smul_apply, smul_eq_mul] using hform
  have hind := (Fintype.linearIndependent_iff.mp (shellMode_linearIndependent N hL))
    (fun q => g (q, s)) hslice
  exact hind p.1

theorem spatial_shell_rank (N : ℕ) (hL : 3 ≤ archiveFibers N) :
    Module.finrank ℝ (Submodule.span ℝ
      (Set.range fun p : (SpatialAxis × ShellHarmonic) × ArchiveFockState =>
        shellCochain N p)) = 96 := by
  have hind := shellCochain_linearIndependent N hL
  have hcard : Fintype.card ((SpatialAxis × ShellHarmonic) × ArchiveFockState) = 96 := by
    have hA : Fintype.card SpatialAxis = 3 := by decide
    have hH : Fintype.card ShellHarmonic = 2 := by decide
    rw [Fintype.card_prod, Fintype.card_prod, hA, hH, card_archive_fock_state]
  simpa [hcard] using finrank_span_eq_card hind

/-! ## `L = 2`: the two signs agree and the sine mode vanishes -/

def shellCosCochain (a : SpatialAxis) (s : ArchiveFockState) : ArchiveCochain 0 :=
  fun q => if q.2 = s then shellCos 0 a q.1 else 0

theorem shellCos_linearIndependent_l2 :
    LinearIndependent ℝ (fun a : SpatialAxis => shellCos 0 a) := by
  classical
  rw [Fintype.linearIndependent_iff]
  intro c hc a
  have hline (b : SpatialAxis) (j : ZMod 2) :
      c b * Real.cos (Real.pi * (j.val : ℝ)) + ∑ d ∈ Finset.univ.erase b, c d = 0 := by
    have h0 := congrFun hc (axisProbe 0 b j)
    simp only [Pi.zero_apply, Finset.sum_apply, Pi.smul_apply, smul_eq_mul] at h0
    have hsplit := (Finset.add_sum_erase (Finset.univ : Finset SpatialAxis)
      (fun d => c d * shellCos 0 d (axisProbe 0 b j)) (Finset.mem_univ b)).symm
    rw [hsplit] at h0
    have hother : ∑ d ∈ Finset.univ.erase b, c d * shellCos 0 d (axisProbe 0 b j) =
        ∑ d ∈ Finset.univ.erase b, c d := by
      refine Finset.sum_congr rfl fun d hd => ?_
      have hdne : d ≠ b := (Finset.mem_erase.mp hd).1
      rw [shellCos_probe_other 0 hdne.symm]
      ring
    rw [hother, shellCos_probe_self] at h0
    have hden : (archiveFibers 0 : ℝ) = 2 := by simp [archiveFibers]
    rw [hden] at h0
    have hangle : ∀ t : ℝ, 2 * Real.pi * t / 2 = Real.pi * t := by
      intro t
      ring
    rw [hangle] at h0
    exact h0
  have h0 := hline a 0
  have h1 := hline a 1
  have hval0 : ((0 : ZMod 2).val : ℝ) = 0 := by simp
  have hval1 : ((1 : ZMod 2).val : ℝ) = 1 := by
    haveI : Fact (1 < 2) := ⟨by decide⟩
    simp [ZMod.val_one]
  simp only [hval0, hval1, mul_zero, Real.cos_zero, Real.cos_pi, mul_one, mul_neg_one] at h0 h1
  linarith

theorem shellCosCochain_linearIndependent_l2 :
    LinearIndependent ℝ (fun p : SpatialAxis × ArchiveFockState => shellCosCochain p.1 p.2) := by
  classical
  rw [Fintype.linearIndependent_iff]
  intro g hg p
  have hslice : ∑ a : SpatialAxis, g (a, p.2) • shellCos 0 a = 0 := by
    funext x
    have h0 := congrFun hg (x, p.2)
    simp only [Pi.zero_apply, Finset.sum_apply, Pi.smul_apply, smul_eq_mul, shellCosCochain] at h0
    rw [show (Finset.univ : Finset (SpatialAxis × ArchiveFockState)) =
        (Finset.univ : Finset SpatialAxis) ×ˢ (Finset.univ : Finset ArchiveFockState) from
        Finset.univ_product_univ.symm] at h0
    rw [Finset.sum_product] at h0
    have hpull : ∑ a, ∑ t, g (a, t) * (if t = p.2 then shellCos 0 a x else 0) =
        ∑ a, g (a, p.2) * shellCos 0 a x := by
      refine Finset.sum_congr rfl fun a _ => ?_
      rw [Finset.sum_eq_single p.2]
      · simp
      · intro t _ ht
        simp [ht]
      · intro hs
        exact absurd (Finset.mem_univ p.2) hs
    simpa [Pi.smul_apply, smul_eq_mul] using (by simpa [hpull] using h0)
  have hind := (Fintype.linearIndependent_iff.mp shellCos_linearIndependent_l2)
    (fun a => g (a, p.2)) hslice
  exact hind p.1

theorem spatial_shell_rank_l2 :
    Module.finrank ℝ (Submodule.span ℝ
      (Set.range fun p : SpatialAxis × ArchiveFockState => shellCosCochain p.1 p.2)) = 48 := by
  have hcard : Fintype.card (SpatialAxis × ArchiveFockState) = 48 := by
    have hA : Fintype.card SpatialAxis = 3 := by decide
    rw [Fintype.card_prod, hA, card_archive_fock_state]
  simpa [hcard] using finrank_span_eq_card shellCosCochain_linearIndependent_l2

/-- Sine squares on the three spatial momenta add to the first harmonic exactly on `± e_i`. -/
noncomputable def momentumSymbol (L : ℕ) (k : SpatialAxis → ZMod L) : ℝ :=
  ∑ a : SpatialAxis, Real.sin (Real.pi * ((k a).val : ℝ) / L) ^ 2

theorem momentumSymbol_first (L : ℕ) (hL : 2 ≤ L) (a : SpatialAxis) (positive : Bool) :
    momentumSymbol L (firstShellMomentum L a positive) = Real.sin (Real.pi / L) ^ 2 := by
  classical
  haveI : Fact (1 < L) := ⟨by omega⟩
  have hsum : momentumSymbol L (firstShellMomentum L a positive) =
      Real.sin (Real.pi * ((if positive then (1 : ZMod L) else -1).val : ℝ) / L) ^ 2 := by
    unfold momentumSymbol
    rw [Finset.sum_eq_single a]
    · simp [firstShellMomentum]
    · intro b _ hb
      simp [firstShellMomentum, if_neg hb, ZMod.val_zero, Real.sin_zero]
    · intro ha
      exact absurd (Finset.mem_univ a) ha
  have hsin : Real.sin (Real.pi *
      ((if positive then (1 : ZMod L) else -1).val : ℝ) / L) ^ 2 =
      Real.sin (Real.pi / L) ^ 2 := by
    cases positive
    · haveI : NeZero (1 : ZMod L) := ⟨by
        intro hz
        have hdiv : L ∣ 1 := (ZMod.natCast_eq_zero_iff 1 L).mp (by simpa using hz)
        have : L = 1 := Nat.dvd_one.mp hdiv
        omega⟩
      have hval : (-1 : ZMod L).val = L - 1 := by
        simpa [ZMod.val_one] using ZMod.val_neg_of_ne_zero (1 : ZMod L)
      rw [if_neg (by decide : (false : Bool) ≠ true), hval]
      simpa using sin_sq_of_neg_one (n := L) (by omega) (by omega)
    · rw [if_pos (rfl : (true : Bool) = true)]
      simpa [ZMod.val_one] using sin_sq_of_one (by omega : 0 < L)
  rw [hsum, hsin]

end
end D0.Geometry
