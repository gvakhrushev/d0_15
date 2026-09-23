import Mathlib.Data.Complex.Basic
import Mathlib.Tactic
import D0.Geometry.A4DSymRoleCentralDifference
import D0.Geometry.ArchiveCubicalDifferential

/-!
# Seam-local twisted role translations

A scalar holonomy `h` acts only when a cyclic coordinate crosses the seam:

`(U_h f)(x) = f(x + 1)` off the seam, and `h f(0)` on the seam.

The load-bearing identity is `U_h^L = h I`. The shift is not built from an
`L`-th root of `h`. For unitary `h`, `U_h` is unitary and

`(∇_h⁺)† = -∇_h⁻`.

No canonical `π₀` holonomy is chosen.
-/

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

variable {L : ℕ} [NeZero L]

def seamFactor (h : ℂ) (x : ZMod L) : ℂ :=
  if x = -1 then h else 1

def twistedCycleShift (h : ℂ) (f : ZMod L → ℂ) : ZMod L → ℂ :=
  fun x => seamFactor h x * f (x + 1)

def twistedCycleShiftInv (h : ℂ) (f : ZMod L → ℂ) : ZMod L → ℂ :=
  fun x => (if x = 0 then h⁻¹ else 1) * f (x - 1)

def seamProduct (h : ℂ) (x : ZMod L) (k : ℕ) : ℂ :=
  ∏ j : Fin k, seamFactor h (x + (j.val : ZMod L))

theorem seamFactor_prod_univ (h : ℂ) :
    ∏ x : ZMod L, seamFactor h x = h := by
  classical
  simpa [seamFactor] using
    (Finset.prod_ite_eq (Finset.univ : Finset (ZMod L)) (-1) h)

theorem seamProduct_univ (h : ℂ) (x : ZMod L) :
    seamProduct h x L = h := by
  classical
  unfold seamProduct
  let j0 : Fin L := ⟨( -1 - x).val, ZMod.val_lt _⟩
  have hhit : x + (j0.val : ZMod L) = -1 := by
    simp [j0, ZMod.natCast_val, sub_eq_add_neg]
  have hprod := Finset.prod_eq_single (f := fun j : Fin L => seamFactor h (x + (j.val : ZMod L)))
    j0 (by
      intro j _ hj
      have hj' : x + (j.val : ZMod L) ≠ -1 := by
        intro hbad
        apply hj
        apply Fin.ext
        have hvals : (j.val : ZMod L) = (j0.val : ZMod L) := by
          apply add_left_cancel (a := x)
          rw [hbad, hhit]
        have hjlt := j.isLt
        have hj0lt := j0.isLt
        have hjv : ((j.val : ZMod L).val) = j.val := ZMod.val_natCast_of_lt hjlt
        have hj0v : ((j0.val : ZMod L).val) = j0.val := ZMod.val_natCast_of_lt hj0lt
        rw [← hjv, ← hj0v, hvals]
      simp [seamFactor, hj'])
    (by
      intro hnot
      exact (hnot (Finset.mem_univ j0)).elim)
  rw [hprod]
  simp [seamFactor, hhit]

theorem twistedCycleShift_iterate (h : ℂ) (k : ℕ) (f : ZMod L → ℂ) (x : ZMod L) :
    (twistedCycleShift h)^[k] f x = seamProduct h x k * f (x + k) := by
  classical
  induction k generalizing x with
  | zero =>
      simp [seamProduct]
  | succ k ih =>
      rw [Function.iterate_succ_apply']
      rw [twistedCycleShift, ih]
      unfold seamProduct
      rw [Fin.prod_univ_succ]
      simp only [Fin.val_zero, add_zero, Fin.val_succ]
      have hshift : ∀ j : Fin k,
          (x + 1 + (j.val : ZMod L)) = x + ((j.succ).val : ZMod L) := by
        intro j
        simp [Fin.val_succ, Nat.cast_add, add_assoc, add_comm, add_left_comm]
      simp_rw [hshift]
      simp [Nat.cast_add, add_assoc, add_left_comm, add_comm, mul_assoc, mul_left_comm]

theorem twistedCycleShift_pow_cycle (h : ℂ) (f : ZMod L → ℂ) :
    (twistedCycleShift h)^[L] f = h • f := by
  funext x
  rw [twistedCycleShift_iterate, seamProduct_univ]
  have : (L : ZMod L) = 0 := ZMod.natCast_self L
  simp [this, Pi.smul_apply, smul_eq_mul]

theorem twistedCycleShift_leftInverse (h : ℂ) (hh : h ≠ 0) (f : ZMod L → ℂ) :
    twistedCycleShiftInv h (twistedCycleShift h f) = f := by
  funext x
  by_cases hx : x = 0
  · subst hx
    simp [twistedCycleShiftInv, twistedCycleShift, seamFactor, sub_eq_add_neg]
    field_simp [hh]
  · have hx' : x - 1 ≠ -1 := by
      intro hbad
      apply hx
      have : x = 0 := by
        calc
          x = (x - 1) + 1 := by ring
          _ = (-1 : ZMod L) + 1 := by rw [hbad]
          _ = 0 := by ring
      exact this
    simp [twistedCycleShiftInv, twistedCycleShift, seamFactor, hx, hx']

theorem twistedCycleShift_rightInverse (h : ℂ) (hh : h ≠ 0) (f : ZMod L → ℂ) :
    twistedCycleShift h (twistedCycleShiftInv h f) = f := by
  funext x
  by_cases hx : x = -1
  · subst hx
    simp [twistedCycleShift, twistedCycleShiftInv, seamFactor]
    field_simp [hh]
  · have hx0 : x + 1 ≠ 0 := by
      intro hbad
      apply hx
      calc
        x = (x + 1) - 1 := by ring
        _ = (0 : ZMod L) - 1 := by rw [hbad]
        _ = -1 := by ring
    simp [twistedCycleShift, twistedCycleShiftInv, seamFactor, hx, hx0]

theorem twistedCycleShift_bijective (h : ℂ) (hh : h ≠ 0) :
    Function.Bijective (twistedCycleShift (L := L) h) :=
  ⟨Function.LeftInverse.injective (twistedCycleShift_leftInverse h hh),
   Function.RightInverse.surjective (twistedCycleShift_rightInverse h hh)⟩

def cyclePairing (f g : ZMod L → ℂ) : ℂ :=
  ∑ x, star f x * g x

theorem star_eq_inv_of_unitary (h : ℂ) (hu : star h * h = 1) :
    star h = h⁻¹ := by
  have hne : h ≠ 0 := by
    intro hz
    rw [hz, star_zero, zero_mul] at hu
    exact zero_ne_one hu
  have : h⁻¹ = star h := by
    calc
      h⁻¹ = h⁻¹ * (star h * h) := by rw [hu, mul_one]
      _ = (h⁻¹ * h) * star h := by ring
      _ = star h := by simp [hne]
  exact this.symm

theorem twistedCycleShift_unitary (h : ℂ) (hu : star h * h = 1)
    (f g : ZMod L → ℂ) :
    cyclePairing (twistedCycleShift h f) g =
      cyclePairing f (twistedCycleShiftInv h g) := by
  classical
  have hstar : star h = h⁻¹ := star_eq_inv_of_unitary h hu
  unfold cyclePairing twistedCycleShift twistedCycleShiftInv seamFactor
  have hreindex :
      (∑ x : ZMod L, star ((if x = -1 then h else 1) * f (x + 1)) * g x) =
        ∑ y : ZMod L,
          star ((if y - 1 = -1 then h else 1) * f y) * g (y - 1) := by
    let e : ZMod L ≃ ZMod L :=
      { toFun := fun x => x + 1
        invFun := fun x => x - 1
        left_inv := by intro x; ring
        right_inv := by intro x; ring }
    refine Fintype.sum_equiv e _ _ ?_
    intro x
    simp [e, sub_eq_add_neg]
  simp only [Pi.star_apply]
  rw [hreindex]
  refine Finset.sum_congr rfl ?_
  intro y _
  by_cases hy : y = 0
  · subst hy
    simp [hstar]
    ring
  · have hy' : y - 1 ≠ -1 := by
      intro hbad
      apply hy
      calc
        y = (y - 1) + 1 := by ring
        _ = (-1 : ZMod L) + 1 := by rw [hbad]
        _ = 0 := by ring
    simp [hy, hy']

/-! ## Role directions on the product phase group -/

def twistedRoleShift (N : ℕ) (r : Role) (h : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) : ArchiveRolePhaseGroup N → ℂ :=
  fun x => seamFactor h (x r) * f (roleTranslatePlus N r x)

def twistedRoleShiftInv (N : ℕ) (r : Role) (h : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) : ArchiveRolePhaseGroup N → ℂ :=
  fun x => (if x r = 0 then h⁻¹ else 1) * f (roleTranslateMinus N r x)

def freezeRole (N : ℕ) (r : Role) (x : ArchiveRolePhaseGroup N)
    (t : ZMod (archiveFibers N)) : ArchiveRolePhaseGroup N :=
  fun s => if s = r then t else x s

theorem freezeRole_coord (N : ℕ) (r : Role) (x : ArchiveRolePhaseGroup N)
    (t : ZMod (archiveFibers N)) :
    freezeRole N r x t r = t := by
  simp [freezeRole]

theorem freezeRole_translate (N : ℕ) (r : Role) (x : ArchiveRolePhaseGroup N)
    (t : ZMod (archiveFibers N)) :
    roleTranslatePlus N r (freezeRole N r x t) = freezeRole N r x (t + 1) := by
  funext s
  by_cases hs : s = r
  · subst hs
    simp [freezeRole, roleTranslatePlus, roleTranslate, roleStep]
  · simp [freezeRole, roleTranslatePlus, roleTranslate, roleStep, hs]

theorem twistedRoleShift_on_slice (N : ℕ) (r : Role) (h : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) (x : ArchiveRolePhaseGroup N)
    (t : ZMod (archiveFibers N)) :
    twistedRoleShift N r h f (freezeRole N r x t) =
      twistedCycleShift h (fun u => f (freezeRole N r x u)) t := by
  simp [twistedRoleShift, twistedCycleShift, freezeRole_coord, freezeRole_translate]

theorem twistedRoleShift_iterate_slice (N : ℕ) (r : Role) (h : ℂ) (k : ℕ)
    (f : ArchiveRolePhaseGroup N → ℂ) (x : ArchiveRolePhaseGroup N)
    (t : ZMod (archiveFibers N)) :
    (twistedRoleShift N r h)^[k] f (freezeRole N r x t) =
      (twistedCycleShift h)^[k] (fun u => f (freezeRole N r x u)) t := by
  induction k generalizing t with
  | zero => rfl
  | succ k ih =>
      rw [Function.iterate_succ_apply', Function.iterate_succ_apply']
      have hstep := twistedRoleShift_on_slice N r h
        ((twistedRoleShift N r h)^[k] f) x t
      rw [hstep]
      congr 1
      funext u
      exact ih u

theorem twistedRoleShift_pow_cycle (N : ℕ) (r : Role) (h : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    (twistedRoleShift N r h)^[archiveFibers N] f = h • f := by
  funext x
  have hslice := twistedRoleShift_iterate_slice N r h (archiveFibers N) f x (x r)
  have hx : freezeRole N r x (x r) = x := by
    funext s
    by_cases hs : s = r
    · subst hs
      simp [freezeRole]
    · simp [freezeRole, hs]
  rw [hx] at hslice
  rw [hslice, twistedCycleShift_pow_cycle]
  simp only [Pi.smul_apply, smul_eq_mul, hx]

theorem roleTranslate_inverse_plus (N : ℕ) (r : Role) (x : ArchiveRolePhaseGroup N) :
    roleTranslatePlus N r (roleTranslateMinus N r x) = x := by
  simp [roleTranslatePlus, roleTranslateMinus, roleTranslate, sub_eq_add_neg]

theorem roleTranslate_inverse_minus (N : ℕ) (r : Role) (x : ArchiveRolePhaseGroup N) :
    roleTranslateMinus N r (roleTranslatePlus N r x) = x := by
  simp [roleTranslatePlus, roleTranslateMinus, roleTranslate, sub_eq_add_neg]

theorem twistedRoleShift_leftInverse (N : ℕ) (r : Role) (h : ℂ) (hh : h ≠ 0)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShiftInv N r h (twistedRoleShift N r h f) = f := by
  funext x
  by_cases hx : x r = 0
  · have hseam : (roleTranslateMinus N r x) r = -1 := by
      simp [roleTranslateMinus, roleTranslate, roleStep, hx, sub_eq_add_neg]
    simp [twistedRoleShiftInv, twistedRoleShift, seamFactor, hx, hseam,
      roleTranslate_inverse_plus]
    field_simp [hh]
  · have hseam : (roleTranslateMinus N r x) r ≠ -1 := by
      intro hbad
      apply hx
      have hcoord := congrArg (fun y : ArchiveRolePhaseGroup N => y r)
        (roleTranslate_inverse_plus N r x)
      simp [roleTranslatePlus, roleTranslate, roleStep, hbad, sub_eq_add_neg] at hcoord
      exact hcoord.symm
    simp [twistedRoleShiftInv, twistedRoleShift, seamFactor, hx, hseam,
      roleTranslate_inverse_plus]

theorem twistedRoleShift_rightInverse (N : ℕ) (r : Role) (h : ℂ) (hh : h ≠ 0)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShift N r h (twistedRoleShiftInv N r h f) = f := by
  funext x
  by_cases hx : x r = -1
  · have hzero : (roleTranslatePlus N r x) r = 0 := by
      simp [roleTranslatePlus, roleTranslate, roleStep, hx]
    simp [twistedRoleShift, twistedRoleShiftInv, seamFactor, hx, hzero,
      roleTranslate_inverse_minus]
    field_simp [hh]
  · have hzero : (roleTranslatePlus N r x) r ≠ 0 := by
      intro hbad
      apply hx
      have hcoord := congrArg (fun y : ArchiveRolePhaseGroup N => y r)
        (roleTranslate_inverse_minus N r x)
      simp [roleTranslateMinus, roleTranslate, roleStep, hbad, sub_eq_add_neg] at hcoord
      exact hcoord.symm
    simp [twistedRoleShift, twistedRoleShiftInv, seamFactor, hx, hzero,
      roleTranslate_inverse_minus]

theorem twistedRoleShift_bijective (N : ℕ) (r : Role) (h : ℂ) (hh : h ≠ 0) :
    Function.Bijective (twistedRoleShift N r h) :=
  ⟨Function.LeftInverse.injective (twistedRoleShift_leftInverse N r h hh),
   Function.RightInverse.surjective (twistedRoleShift_rightInverse N r h hh)⟩

def phasePairing (N : ℕ) (f g : ArchiveRolePhaseGroup N → ℂ) : ℂ :=
  ∑ x, star f x * g x

theorem twistedRoleShift_unitary (N : ℕ) (r : Role) (h : ℂ) (hu : star h * h = 1)
    (f g : ArchiveRolePhaseGroup N → ℂ) :
    phasePairing N (twistedRoleShift N r h f) g =
      phasePairing N f (twistedRoleShiftInv N r h g) := by
  classical
  have hstar : star h = h⁻¹ := star_eq_inv_of_unitary h hu
  unfold phasePairing
  simp only [Pi.star_apply, twistedRoleShift, twistedRoleShiftInv, seamFactor]
  have hreindex :
      (∑ x, star ((if x r = -1 then h else 1) * f (roleTranslatePlus N r x)) * g x) =
        ∑ y, star ((if (y - roleStep N r) r = -1 then h else 1) *
          f (roleTranslatePlus N r (y - roleStep N r))) *
          g (y - roleStep N r) := by
    exact (Equiv.sum_comp (roleTranslateEquiv N (roleStep N r)).symm
      (fun x => star ((if x r = -1 then h else 1) * f (roleTranslatePlus N r x)) * g x)).symm
  rw [hreindex]
  refine Finset.sum_congr rfl ?_
  intro y _
  have hback : roleTranslatePlus N r (y - roleStep N r) = y := by
    simp [roleTranslatePlus, roleTranslate, sub_eq_add_neg]
  rw [hback]
  by_cases hy : y r = 0
  · have hseam : (y - roleStep N r) r = -1 := by
      simp [roleStep, hy, sub_eq_add_neg]
    simp [hseam, hy, hstar, roleTranslateMinus, roleTranslate, roleStep, sub_eq_add_neg]
    ring
  · have hseam : (y - roleStep N r) r ≠ -1 := by
      intro hbad
      simp [roleStep, sub_eq_add_neg] at hbad
      exact hy hbad
    simp [hseam, hy, roleTranslateMinus, roleTranslate, roleStep, sub_eq_add_neg]

def twistedForwardDifference (N : ℕ) (r : Role) (h : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) : ArchiveRolePhaseGroup N → ℂ :=
  fun x => (archiveFibers N : ℂ) * (twistedRoleShift N r h f x - f x)

def twistedBackwardDifference (N : ℕ) (r : Role) (h : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) : ArchiveRolePhaseGroup N → ℂ :=
  fun x => (archiveFibers N : ℂ) * (f x - twistedRoleShiftInv N r h f x)

theorem twistedForward_adjoint (N : ℕ) (r : Role) (h : ℂ) (hu : star h * h = 1)
    (f g : ArchiveRolePhaseGroup N → ℂ) :
    phasePairing N (twistedForwardDifference N r h f) g =
      phasePairing N f (-twistedBackwardDifference N r h g) := by
  classical
  have hU := twistedRoleShift_unitary N r h hu f g
  unfold phasePairing at hU
  simp only [Pi.star_apply] at hU
  unfold twistedForwardDifference twistedBackwardDifference phasePairing
  simp only [Pi.star_apply, Pi.neg_apply]
  have hreal : star (archiveFibers N : ℂ) = (archiveFibers N : ℂ) := by simp
  calc
    ∑ x, star ((archiveFibers N : ℂ) *
        (twistedRoleShift N r h f x - f x)) * g x =
        ∑ x, (archiveFibers N : ℂ) *
          (star (twistedRoleShift N r h f x) - star (f x)) * g x := by
            refine Finset.sum_congr rfl ?_
            intro x _
            rw [star_mul, hreal, star_sub]
            ring
    _ = (archiveFibers N : ℂ) *
        ∑ x, (star (twistedRoleShift N r h f x) * g x - star (f x) * g x) := by
          have hreassoc :
              ∑ x, (archiveFibers N : ℂ) *
                  (star (twistedRoleShift N r h f x) - star (f x)) * g x =
                ∑ x, (archiveFibers N : ℂ) *
                  (star (twistedRoleShift N r h f x) * g x - star (f x) * g x) := by
            refine Finset.sum_congr rfl ?_
            intro x _
            ring
          rw [hreassoc, ← Finset.mul_sum]
    _ = (archiveFibers N : ℂ) *
        ((∑ x, star (twistedRoleShift N r h f x) * g x) -
          ∑ x, star (f x) * g x) := by
          rw [Finset.sum_sub_distrib]
    _ = (archiveFibers N : ℂ) *
        ((∑ x, star (f x) * twistedRoleShiftInv N r h g x) -
          ∑ x, star (f x) * g x) := by
          rw [hU]
    _ = ∑ x, star (f x) *
        (-((archiveFibers N : ℂ) *
          (g x - twistedRoleShiftInv N r h g x))) := by
          rw [← Finset.sum_sub_distrib, Finset.mul_sum]
          refine Finset.sum_congr rfl ?_
          intro x _
          ring

theorem twistedRoleShift_comm (N : ℕ) {r s : Role} (hr : r ≠ s) (h k : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShift N r h (twistedRoleShift N s k f) =
      twistedRoleShift N s k (twistedRoleShift N r h f) := by
  funext x
  have htrans :
      roleTranslatePlus N r (roleTranslatePlus N s x) =
        roleTranslatePlus N s (roleTranslatePlus N r x) := by
    simp [roleTranslatePlus, roleTranslate]
    abel
  have hrcoord : (roleTranslatePlus N s x) r = x r := by
    simp [roleTranslatePlus, roleTranslate, roleStep, hr]
  have hscoord : (roleTranslatePlus N r x) s = x s := by
    simp [roleTranslatePlus, roleTranslate, roleStep, Ne.symm hr]
  simp only [twistedRoleShift, htrans, hrcoord, hscoord]
  ring

theorem twistedRoleShift_one (N : ℕ) (r : Role) (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShift N r 1 f = fun x => f (roleTranslatePlus N r x) := by
  funext x
  simp [twistedRoleShift, seamFactor]

theorem twistedForward_one (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℂ) (x : ArchiveRolePhaseGroup N) :
    twistedForwardDifference N r 1 f x =
      (archiveFibers N : ℂ) * (f (roleTranslatePlus N r x) - f x) := by
  simp [twistedForwardDifference, twistedRoleShift_one]

theorem twistedCycle_one_eq_untwisted (f : ZMod L → ℂ) :
    twistedCycleShift 1 f = fun x => f (x + 1) := by
  funext x
  simp [twistedCycleShift, seamFactor]

theorem unitary_ne_zero (h : ℂ) (hu : star h * h = 1) : h ≠ 0 := by
  intro hz
  rw [hz, star_zero, zero_mul] at hu
  exact zero_ne_one hu

theorem twistedRoleShift_map_sub (N : ℕ) (r : Role) (h : ℂ)
    (f g : ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShift N r h (f - g) =
      twistedRoleShift N r h f - twistedRoleShift N r h g := by
  funext x
  simp [twistedRoleShift, Pi.sub_apply]
  ring

theorem twistedRoleShift_const_mul (N : ℕ) (r : Role) (h c : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShift N r h (fun x => c * f x) =
      fun x => c * twistedRoleShift N r h f x := by
  funext x
  simp [twistedRoleShift]
  ring

theorem twistedRoleShiftInv_map_sub (N : ℕ) (r : Role) (h : ℂ)
    (f g : ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShiftInv N r h (f - g) =
      twistedRoleShiftInv N r h f - twistedRoleShiftInv N r h g := by
  funext x
  by_cases hx : x r = 0
  · simp [twistedRoleShiftInv, hx, Pi.sub_apply]
    ring
  · simp [twistedRoleShiftInv, hx, Pi.sub_apply]

theorem twistedRoleShiftInv_const_mul (N : ℕ) (r : Role) (h c : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShiftInv N r h (fun x => c * f x) =
      fun x => c * twistedRoleShiftInv N r h f x := by
  funext x
  by_cases hx : x r = 0
  · simp [twistedRoleShiftInv, hx]
    ring
  · simp [twistedRoleShiftInv, hx]

theorem twistedRoleShift_sum {ι : Type*} [Fintype ι] (N : ℕ) (r : Role) (h : ℂ)
    (F : ι → ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShift N r h (fun x => ∑ i, F i x) =
      fun x => ∑ i, twistedRoleShift N r h (F i) x := by
  funext x
  classical
  simp [twistedRoleShift, Finset.mul_sum]

theorem twistedRoleShiftInv_sum {ι : Type*} [Fintype ι] (N : ℕ) (r : Role) (h : ℂ)
    (F : ι → ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShiftInv N r h (fun x => ∑ i, F i x) =
      fun x => ∑ i, twistedRoleShiftInv N r h (F i) x := by
  funext x
  classical
  simp [twistedRoleShiftInv, Finset.mul_sum]

theorem twistedForwardDifference_sum {ι : Type*} [Fintype ι] (N : ℕ) (r : Role) (h : ℂ)
    (F : ι → ArchiveRolePhaseGroup N → ℂ) :
    twistedForwardDifference N r h (fun x => ∑ i, F i x) =
      fun x => ∑ i, twistedForwardDifference N r h (F i) x := by
  funext x
  classical
  simp only [twistedForwardDifference]
  rw [congrFun (twistedRoleShift_sum N r h F) x]
  rw [← Finset.sum_sub_distrib, Finset.mul_sum]

theorem twistedForwardDifference_const_mul (N : ℕ) (r : Role) (h c : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedForwardDifference N r h (fun x => c * f x) =
      fun x => c * twistedForwardDifference N r h f x := by
  funext x
  simp only [twistedForwardDifference]
  rw [twistedRoleShift_const_mul]
  ring

theorem twistedBackwardDifference_sum {ι : Type*} [Fintype ι] (N : ℕ) (r : Role) (h : ℂ)
    (F : ι → ArchiveRolePhaseGroup N → ℂ) :
    twistedBackwardDifference N r h (fun x => ∑ i, F i x) =
      fun x => ∑ i, twistedBackwardDifference N r h (F i) x := by
  funext x
  classical
  simp only [twistedBackwardDifference]
  rw [congrFun (twistedRoleShiftInv_sum N r h F) x]
  rw [← Finset.sum_sub_distrib, Finset.mul_sum]

theorem twistedBackwardDifference_const_mul (N : ℕ) (r : Role) (h c : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedBackwardDifference N r h (fun x => c * f x) =
      fun x => c * twistedBackwardDifference N r h f x := by
  funext x
  simp only [twistedBackwardDifference]
  rw [twistedRoleShiftInv_const_mul]
  ring

theorem twistedRoleShift_family_comm (N : ℕ) (r s : Role) (H : Role → ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShift N r (H r) (twistedRoleShift N s (H s) f) =
      twistedRoleShift N s (H s) (twistedRoleShift N r (H r) f) := by
  by_cases hrs : r = s
  · subst hrs
    rfl
  · exact twistedRoleShift_comm N hrs (H r) (H s) f

theorem twistedRoleShift_inv_comm (N : ℕ) {r s : Role} (hrs : r ≠ s) (h k : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShift N r h (twistedRoleShiftInv N s k f) =
      twistedRoleShiftInv N s k (twistedRoleShift N r h f) := by
  funext x
  have htrans :
      roleTranslatePlus N r (roleTranslateMinus N s x) =
        roleTranslateMinus N s (roleTranslatePlus N r x) := by
    simp [roleTranslatePlus, roleTranslateMinus, roleTranslate]
    abel
  have hrcoord : (roleTranslateMinus N s x) r = x r := by
    simp [roleTranslateMinus, roleTranslate, roleStep, hrs]
  have hscoord : (roleTranslatePlus N r x) s = x s := by
    simp [roleTranslatePlus, roleTranslate, roleStep, Ne.symm hrs]
  simp only [twistedRoleShift, twistedRoleShiftInv, htrans, hrcoord, hscoord]
  ring

theorem twistedRoleShiftInv_comm (N : ℕ) {r s : Role} (hrs : r ≠ s) (h k : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedRoleShiftInv N r h (twistedRoleShiftInv N s k f) =
      twistedRoleShiftInv N s k (twistedRoleShiftInv N r h f) := by
  funext x
  have htrans :
      roleTranslateMinus N r (roleTranslateMinus N s x) =
        roleTranslateMinus N s (roleTranslateMinus N r x) := by
    simp [roleTranslateMinus, roleTranslate]
    abel
  have hrcoord : (roleTranslateMinus N s x) r = x r := by
    simp [roleTranslateMinus, roleTranslate, roleStep, hrs]
  have hscoord : (roleTranslateMinus N r x) s = x s := by
    simp [roleTranslateMinus, roleTranslate, roleStep, Ne.symm hrs]
  simp only [twistedRoleShiftInv, htrans, hrcoord, hscoord]
  ring

theorem twistedRoleShift_of_backward (N : ℕ) (r : Role) (h : ℂ) (hh : h ≠ 0)
    (f : ArchiveRolePhaseGroup N → ℂ) (x : ArchiveRolePhaseGroup N) :
    twistedRoleShift N r h (twistedBackwardDifference N r h f) x =
      (archiveFibers N : ℂ) * (twistedRoleShift N r h f x - f x) := by
  have hinv := congrFun (twistedRoleShift_rightInverse N r h hh f) x
  simp only [twistedRoleShift] at hinv
  simp only [twistedBackwardDifference, twistedRoleShift]
  calc
    seamFactor h (x r) * ((archiveFibers N : ℂ) *
        (f (roleTranslatePlus N r x) -
          twistedRoleShiftInv N r h f (roleTranslatePlus N r x))) =
        (archiveFibers N : ℂ) *
          (seamFactor h (x r) * f (roleTranslatePlus N r x) -
            seamFactor h (x r) *
              twistedRoleShiftInv N r h f (roleTranslatePlus N r x)) := by ring
    _ = (archiveFibers N : ℂ) *
          (seamFactor h (x r) * f (roleTranslatePlus N r x) - f x) := by
            rw [hinv]

theorem twistedRoleShiftInv_of_forward (N : ℕ) (r : Role) (h : ℂ) (hh : h ≠ 0)
    (f : ArchiveRolePhaseGroup N → ℂ) (x : ArchiveRolePhaseGroup N) :
    twistedRoleShiftInv N r h (twistedForwardDifference N r h f) x =
      (archiveFibers N : ℂ) * (f x - twistedRoleShiftInv N r h f x) := by
  have hinv := congrFun (twistedRoleShift_leftInverse N r h hh f) x
  simp only [twistedRoleShiftInv] at hinv
  simp only [twistedForwardDifference, twistedRoleShiftInv]
  calc
    (if x r = 0 then h⁻¹ else 1) * ((archiveFibers N : ℂ) *
        (twistedRoleShift N r h f (roleTranslateMinus N r x) -
          f (roleTranslateMinus N r x))) =
        (archiveFibers N : ℂ) *
          ((if x r = 0 then h⁻¹ else 1) *
              twistedRoleShift N r h f (roleTranslateMinus N r x) -
            (if x r = 0 then h⁻¹ else 1) * f (roleTranslateMinus N r x)) := by
              split_ifs <;> ring
    _ = (archiveFibers N : ℂ) *
          (f x - (if x r = 0 then h⁻¹ else 1) * f (roleTranslateMinus N r x)) := by
            rw [hinv]

theorem twistedBackward_forward_expand (N : ℕ) (r : Role) (h : ℂ) (hh : h ≠ 0)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedBackwardDifference N r h (twistedForwardDifference N r h f) =
      fun x => (archiveFibers N : ℂ) ^ 2 *
        (twistedRoleShift N r h f x + twistedRoleShiftInv N r h f x - 2 * f x) := by
  funext x
  simp only [twistedBackwardDifference]
  rw [twistedRoleShiftInv_of_forward N r h hh f x]
  simp only [twistedForwardDifference, twistedRoleShift]
  ring

theorem twistedForward_backward_expand (N : ℕ) (r : Role) (h : ℂ) (hh : h ≠ 0)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedForwardDifference N r h (twistedBackwardDifference N r h f) =
      fun x => (archiveFibers N : ℂ) ^ 2 *
        (twistedRoleShift N r h f x + twistedRoleShiftInv N r h f x - 2 * f x) := by
  funext x
  simp only [twistedForwardDifference]
  rw [twistedRoleShift_of_backward N r h hh f x]
  simp only [twistedBackwardDifference, twistedRoleShiftInv]
  ring

theorem twistedForward_backward_same (N : ℕ) (r : Role) (h : ℂ) (hh : h ≠ 0)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedForwardDifference N r h (twistedBackwardDifference N r h f) =
      twistedBackwardDifference N r h (twistedForwardDifference N r h f) := by
  rw [twistedForward_backward_expand N r h hh f, twistedBackward_forward_expand N r h hh f]

theorem twistedForward_family_comm (N : ℕ) (r s : Role) (H : Role → ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedForwardDifference N r (H r) (twistedForwardDifference N s (H s) f) =
      twistedForwardDifference N s (H s) (twistedForwardDifference N r (H r) f) := by
  funext x
  have hcomm := congrFun (twistedRoleShift_family_comm N r s H f)
  simp only [twistedForwardDifference] at hcomm ⊢
  have hlin_r :
      twistedRoleShift N r (H r) (twistedForwardDifference N s (H s) f) x =
        (archiveFibers N : ℂ) * (twistedRoleShift N r (H r) (twistedRoleShift N s (H s) f) x -
          twistedRoleShift N r (H r) f x) := by
    simp only [twistedForwardDifference, twistedRoleShift, Pi.sub_apply]
    ring
  have hlin_s :
      twistedRoleShift N s (H s) (twistedForwardDifference N r (H r) f) x =
        (archiveFibers N : ℂ) * (twistedRoleShift N s (H s) (twistedRoleShift N r (H r) f) x -
          twistedRoleShift N s (H s) f x) := by
    simp only [twistedForwardDifference, twistedRoleShift, Pi.sub_apply]
    ring
  rw [hlin_r, hlin_s, hcomm]
  ring

theorem twistedBackward_family_comm (N : ℕ) (r s : Role) (H : Role → ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedBackwardDifference N r (H r) (twistedBackwardDifference N s (H s) f) =
      twistedBackwardDifference N s (H s) (twistedBackwardDifference N r (H r) f) := by
  funext x
  by_cases hrs : r = s
  · subst hrs
    rfl
  · have hcomm := congrFun (twistedRoleShiftInv_comm N hrs (H r) (H s) f)
    simp only [twistedBackwardDifference] at hcomm ⊢
    have hlin_r :
        twistedRoleShiftInv N r (H r) (twistedBackwardDifference N s (H s) f) x =
          (archiveFibers N : ℂ) *
            (twistedRoleShiftInv N r (H r) f x -
              twistedRoleShiftInv N r (H r) (twistedRoleShiftInv N s (H s) f) x) := by
      simp only [twistedBackwardDifference, twistedRoleShiftInv, Pi.sub_apply]
      ring
    have hlin_s :
        twistedRoleShiftInv N s (H s) (twistedBackwardDifference N r (H r) f) x =
          (archiveFibers N : ℂ) *
            (twistedRoleShiftInv N s (H s) f x -
              twistedRoleShiftInv N s (H s) (twistedRoleShiftInv N r (H r) f) x) := by
      simp only [twistedBackwardDifference, twistedRoleShiftInv, Pi.sub_apply]
      ring
    rw [hlin_r, hlin_s, hcomm]
    ring

theorem twistedForward_backward_ne (N : ℕ) {r s : Role} (hrs : r ≠ s) (h k : ℂ)
    (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedForwardDifference N r h (twistedBackwardDifference N s k f) =
      twistedBackwardDifference N s k (twistedForwardDifference N r h f) := by
  funext x
  have hcomm := congrFun (twistedRoleShift_inv_comm N hrs h k f) x
  simp only [twistedForwardDifference, twistedBackwardDifference] at hcomm ⊢
  have hlin_r :
      twistedRoleShift N r h (twistedBackwardDifference N s k f) x =
        (archiveFibers N : ℂ) * (twistedRoleShift N r h f x -
          twistedRoleShift N r h (twistedRoleShiftInv N s k f) x) := by
    simp only [twistedBackwardDifference, twistedRoleShift, Pi.sub_apply]
    ring
  have hlin_s :
      twistedRoleShiftInv N s k (twistedForwardDifference N r h f) x =
        (archiveFibers N : ℂ) * (twistedRoleShiftInv N s k (twistedRoleShift N r h f) x -
          twistedRoleShiftInv N s k f x) := by
    simp only [twistedForwardDifference, twistedRoleShiftInv, Pi.sub_apply]
    ring
  rw [hlin_r, hlin_s, hcomm]
  ring

theorem twistedForward_backward_family_comm (N : ℕ) (r s : Role) (H : Role → ℂ)
    (hne : ∀ t, H t ≠ 0) (f : ArchiveRolePhaseGroup N → ℂ) :
    twistedForwardDifference N r (H r) (twistedBackwardDifference N s (H s) f) =
      twistedBackwardDifference N s (H s) (twistedForwardDifference N r (H r) f) := by
  by_cases hrs : r = s
  · subst hrs
    exact twistedForward_backward_same N r (H r) (hne r) f
  · exact twistedForward_backward_ne N hrs (H r) (H s) f

theorem twistedForwardDifference_local (N : ℕ) (r : Role) (h : ℂ)
    (f g : ArchiveRolePhaseGroup N → ℂ) (x : ArchiveRolePhaseGroup N)
    (hx : f x = g x)
    (hplus : f (roleTranslatePlus N r x) = g (roleTranslatePlus N r x)) :
    twistedForwardDifference N r h f x = twistedForwardDifference N r h g x := by
  simp [twistedForwardDifference, twistedRoleShift, hx, hplus]

theorem twistedBackwardDifference_local (N : ℕ) (r : Role) (h : ℂ)
    (f g : ArchiveRolePhaseGroup N → ℂ) (x : ArchiveRolePhaseGroup N)
    (hx : f x = g x)
    (hminus : f (roleTranslateMinus N r x) = g (roleTranslateMinus N r x)) :
    twistedBackwardDifference N r h f x = twistedBackwardDifference N r h g x := by
  simp [twistedBackwardDifference, twistedRoleShiftInv, hx, hminus]

end

end D0.Geometry
