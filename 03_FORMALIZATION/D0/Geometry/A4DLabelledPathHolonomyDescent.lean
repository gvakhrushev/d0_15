import Mathlib.Algebra.Module.Equiv.Basic
import Mathlib.Tactic
import D0.Geometry.ArchiveAffineCartanConnection

/-!
# Labelled `List ChainStep` holonomy descent skeleton

Generic invertible **positive** edge family on the archive's literal labelled
carrier `List ChainStep`. Backward steps are the shifted inverse of the positive
letter — no independent backward link.

Pull/composition order matches `affinePath` / `covariantLin`: later steps act
first.

Review note: this file is the generic word/descent skeleton only; the physical letter remains external.

This module does **not** construct a physical matter link, does not specialize
to an unknown `ell_N^+`, and does not widen
`pathEval_factors_pairGroupoid_iff_trivial_holonomy` (Prop-edge `ChainPath E`).

The new owner is the slot-faithful endpoint-independence ↔ trivial labelled
holonomy theorem on `List ChainStep`, plus the exact `L = 2` parallel-slot
period forced by endpoint descent.
-/

namespace D0.Geometry

open D0

variable {N : ℕ} {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

/-- Generic positive labelled letter family `ell⁺(x, r)`. -/
abbrev LabelledPositiveFamily (N : ℕ) (K V : Type*)
    [Field K] [AddCommGroup V] [Module K V] :=
  ArchiveRolePhaseGroup N → Role → V ≃ₗ[K] V

/-- One oriented step. Backward is the shifted inverse of the stored positive letter. -/
def labelledStep (ellPlus : LabelledPositiveFamily N K V) :
    ChainStep → ArchiveRolePhaseGroup N → V ≃ₗ[K] V
  | .fwd r, x => ellPlus x r
  | .bwd r, x => (ellPlus (roleTranslateMinus N r x) r).symm

/-- Left-to-right labelled path value. Later steps act first (`covariantLin` order). -/
def labelledPathEval (ellPlus : LabelledPositiveFamily N K V) :
    List ChainStep → ArchiveRolePhaseGroup N → V ≃ₗ[K] V
  | [], _ => LinearEquiv.refl K V
  | s :: rest, x =>
      (labelledPathEval ellPlus rest (stepTarget N s x)).trans (labelledStep ellPlus s x)

@[simp] theorem labelledPathEval_nil (ellPlus : LabelledPositiveFamily N K V)
    (x : ArchiveRolePhaseGroup N) :
    labelledPathEval ellPlus [] x = LinearEquiv.refl K V := rfl

@[simp] theorem labelledPathEval_cons (ellPlus : LabelledPositiveFamily N K V)
    (s : ChainStep) (rest : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    labelledPathEval ellPlus (s :: rest) x =
      (labelledPathEval ellPlus rest (stepTarget N s x)).trans
        (labelledStep ellPlus s x) := rfl

/-- Empty word evaluates to the identity. -/
theorem labelledPathEval_empty (ellPlus : LabelledPositiveFamily N K V)
    (x : ArchiveRolePhaseGroup N) :
    labelledPathEval ellPlus [] x = LinearEquiv.refl K V :=
  labelledPathEval_nil ellPlus x

/-- Append law in repository pull order. -/
theorem labelledPathEval_append (ellPlus : LabelledPositiveFamily N K V)
    (p q : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    labelledPathEval ellPlus (p ++ q) x =
      (labelledPathEval ellPlus q (pathEnd N p x)).trans
        (labelledPathEval ellPlus p x) := by
  induction p generalizing x with
  | nil =>
      simp [labelledPathEval, pathEnd]
  | cons s rest ih =>
      simp only [List.cons_append, labelledPathEval_cons, pathEnd_cons, ih]
      exact (LinearEquiv.trans_assoc _ _ _).symm

theorem labelledStep_reverse (ellPlus : LabelledPositiveFamily N K V)
    (s : ChainStep) (x : ArchiveRolePhaseGroup N) :
    labelledStep ellPlus (reverseStep s) (stepTarget N s x) =
      (labelledStep ellPlus s x).symm := by
  cases s with
  | fwd r =>
      simp [labelledStep, reverseStep, stepTarget, roleTranslate_inverse_minus]
  | bwd r =>
      simp [labelledStep, reverseStep, stepTarget, LinearEquiv.symm_symm]

/-- Reverse path (map `reverseStep`, then reverse the list) evaluates to the inverse. -/
theorem labelledPathEval_reverse (ellPlus : LabelledPositiveFamily N K V)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    labelledPathEval ellPlus ((steps.map reverseStep).reverse) (pathEnd N steps x) =
      (labelledPathEval ellPlus steps x).symm := by
  induction steps generalizing x with
  | nil =>
      simp [labelledPathEval, pathEnd]
  | cons s rest ih =>
      calc
        labelledPathEval ellPlus (((s :: rest).map reverseStep).reverse)
            (pathEnd N (s :: rest) x) =
            labelledPathEval ellPlus
              ((rest.map reverseStep).reverse ++ [reverseStep s])
              (pathEnd N rest (stepTarget N s x)) := by
              simp [pathEnd_cons, List.map_cons, List.reverse_cons]
        _ = (labelledPathEval ellPlus [reverseStep s]
              (pathEnd N (rest.map reverseStep).reverse
                (pathEnd N rest (stepTarget N s x)))).trans
            (labelledPathEval ellPlus (rest.map reverseStep).reverse
              (pathEnd N rest (stepTarget N s x))) := by
              rw [labelledPathEval_append]
        _ = (labelledStep ellPlus (reverseStep s)
              (pathEnd N (rest.map reverseStep).reverse
                (pathEnd N rest (stepTarget N s x)))).trans
            (labelledPathEval ellPlus rest (stepTarget N s x)).symm := by
              simp [labelledPathEval, ih]
        _ = (labelledStep ellPlus (reverseStep s) (stepTarget N s x)).trans
            (labelledPathEval ellPlus rest (stepTarget N s x)).symm := by
              rw [pathEnd_reverse]
        _ = (labelledStep ellPlus s x).symm.trans
            (labelledPathEval ellPlus rest (stepTarget N s x)).symm := by
              rw [labelledStep_reverse]
        _ = ((labelledPathEval ellPlus rest (stepTarget N s x)).trans
              (labelledStep ellPlus s x)).symm := by
              rw [LinearEquiv.trans_symm]
        _ = (labelledPathEval ellPlus (s :: rest) x).symm := by
              simp [labelledPathEval]

/-- Inverse transport: reverse word from the path endpoint recovers the inverse. -/
theorem labelledPathEval_inverse (ellPlus : LabelledPositiveFamily N K V)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    labelledPathEval ellPlus ((steps.map reverseStep).reverse) (pathEnd N steps x) =
      (labelledPathEval ellPlus steps x).symm :=
  labelledPathEval_reverse ellPlus steps x

/-- Slot-faithful labelled endpoint descent ↔ trivial labelled loop holonomy.

Typed over `List ChainStep` with `pathEnd`. Distinct from
`pathEval_factors_pairGroupoid_iff_trivial_holonomy` on Prop-edge `ChainPath E`. -/
theorem labelledPathEval_factors_endpoints_iff_trivial_holonomy
    (ellPlus : LabelledPositiveFamily N K V) :
    (∀ (x y : ArchiveRolePhaseGroup N) (p q : List ChainStep),
        pathEnd N p x = y → pathEnd N q x = y →
          labelledPathEval ellPlus p x = labelledPathEval ellPlus q x) ↔
      (∀ (x : ArchiveRolePhaseGroup N) (p : List ChainStep),
        pathEnd N p x = x →
          labelledPathEval ellPlus p x = LinearEquiv.refl K V) := by
  constructor
  · intro h x p hp
    simpa [labelledPathEval, pathEnd] using
      h x x p ([] : List ChainStep) hp (by simp [pathEnd])
  · intro h x y p q hp hq
    have hloop :
        labelledPathEval ellPlus (p ++ (q.map reverseStep).reverse) x =
          LinearEquiv.refl K V := by
      apply h x
      calc
        pathEnd N (p ++ (q.map reverseStep).reverse) x =
            pathEnd N ((q.map reverseStep).reverse) (pathEnd N p x) :=
          pathEnd_append _ _ _
        _ = pathEnd N ((q.map reverseStep).reverse) y := by rw [hp]
        _ = pathEnd N ((q.map reverseStep).reverse) (pathEnd N q x) := by rw [← hq]
        _ = x := pathEnd_reverse q x
    have hform :
        labelledPathEval ellPlus (p ++ (q.map reverseStep).reverse) x =
          (labelledPathEval ellPlus q x).symm.trans (labelledPathEval ellPlus p x) := by
      calc
        labelledPathEval ellPlus (p ++ (q.map reverseStep).reverse) x =
            (labelledPathEval ellPlus ((q.map reverseStep).reverse)
              (pathEnd N p x)).trans (labelledPathEval ellPlus p x) :=
          labelledPathEval_append _ _ _ _
        _ = (labelledPathEval ellPlus ((q.map reverseStep).reverse) y).trans
              (labelledPathEval ellPlus p x) := by rw [hp]
        _ = (labelledPathEval ellPlus ((q.map reverseStep).reverse)
              (pathEnd N q x)).trans (labelledPathEval ellPlus p x) := by rw [← hq]
        _ = (labelledPathEval ellPlus q x).symm.trans
              (labelledPathEval ellPlus p x) := by rw [labelledPathEval_reverse]
    have hEq :
        (labelledPathEval ellPlus q x).symm.trans (labelledPathEval ellPlus p x) =
          LinearEquiv.refl K V := by
      rw [← hform]; exact hloop
    have htrans :=
      congrArg (fun f => (labelledPathEval ellPlus q x).trans f) hEq
    simpa [LinearEquiv.trans_symm_cancel_left, LinearEquiv.trans_refl] using htrans

/-! ## Exact L = 2 parallel-slot period -/

/-- At `N = 0` (`L = 2`), `.fwd r` and `.bwd r` from the same site share an endpoint. -/
theorem labelled_L2_fwd_bwd_same_endpoint (r : Role)
    (x : ArchiveRolePhaseGroup 0) :
    stepTarget 0 (.fwd r) x = stepTarget 0 (.bwd r) x := by
  simp [stepTarget, roleTranslatePlus_eq_minus_at_zero]

/-- The parallel labels remain distinct `ChainStep` constructors. -/
theorem labelled_L2_fwd_ne_bwd (r : Role) :
    ChainStep.fwd r ≠ ChainStep.bwd r := by
  intro h
  cases h

/-- Endpoint descent at `L = 2` forces the exact length-two positive-link period.

In repository pull/`LinearEquiv.trans` order (later acts first), this is
`(ellPlus (x + roleStep 0 r) r).trans (ellPlus x r) = refl`, matching the
affine-mul form `ellPlus x r * ellPlus (x + roleStep 0 r) r = 1`. -/
theorem labelled_L2_period_of_endpoint_descent
    (ellPlus : LabelledPositiveFamily 0 K V)
    (hdesc :
      ∀ (x y : ArchiveRolePhaseGroup 0) (p q : List ChainStep),
        pathEnd 0 p x = y → pathEnd 0 q x = y →
          labelledPathEval ellPlus p x = labelledPathEval ellPlus q x)
    (x : ArchiveRolePhaseGroup 0) (r : Role) :
    (ellPlus (x + roleStep 0 r) r).trans (ellPlus x r) = LinearEquiv.refl K V := by
  have hend :
      pathEnd 0 [ChainStep.fwd r] x = pathEnd 0 [ChainStep.bwd r] x := by
    simp [pathEnd, labelled_L2_fwd_bwd_same_endpoint]
  have heval :=
    hdesc x (pathEnd 0 [ChainStep.fwd r] x) [ChainStep.fwd r] [ChainStep.bwd r]
      rfl (by simpa using hend.symm)
  have hfwd :
      labelledPathEval ellPlus [ChainStep.fwd r] x = ellPlus x r := by
    simp [labelledPathEval, labelledStep]
  have hbwd :
      labelledPathEval ellPlus [ChainStep.bwd r] x =
        (ellPlus (roleTranslateMinus 0 r x) r).symm := by
    simp [labelledPathEval, labelledStep]
  have hEq : ellPlus x r = (ellPlus (roleTranslateMinus 0 r x) r).symm := by
    simpa [hfwd, hbwd] using heval
  have hsite : roleTranslateMinus 0 r x = x + roleStep 0 r := by
    simpa [stepTarget, roleTranslatePlus_apply, roleTranslateMinus_apply] using
      (labelled_L2_fwd_bwd_same_endpoint r x).symm
  have hEq' : ellPlus x r = (ellPlus (x + roleStep 0 r) r).symm := by
    simpa [hsite] using hEq
  calc
    (ellPlus (x + roleStep 0 r) r).trans (ellPlus x r) =
        (ellPlus (x + roleStep 0 r) r).trans
          (ellPlus (x + roleStep 0 r) r).symm := by rw [hEq']
    _ = LinearEquiv.refl K V := LinearEquiv.self_trans_symm _

/-- Companion packaging `f.trans g = refl` (mutual inverse of the pull-order period). -/
theorem labelled_L2_period_of_endpoint_descent'
    (ellPlus : LabelledPositiveFamily 0 K V)
    (hdesc :
      ∀ (x y : ArchiveRolePhaseGroup 0) (p q : List ChainStep),
        pathEnd 0 p x = y → pathEnd 0 q x = y →
          labelledPathEval ellPlus p x = labelledPathEval ellPlus q x)
    (x : ArchiveRolePhaseGroup 0) (r : Role) :
    (ellPlus x r).trans (ellPlus (x + roleStep 0 r) r) = LinearEquiv.refl K V := by
  have h := labelled_L2_period_of_endpoint_descent (K := K) (V := V) ellPlus hdesc x r
  -- h : g.trans f = refl with g = ellPlus (x+r) r, f = ellPlus x r
  set g := ellPlus (x + roleStep 0 r) r
  set f := ellPlus x r
  have hf_symm : f = g.symm := by
    have hcongr := congrArg (fun e => g.symm.trans e) h
    -- g.symm.trans (g.trans f) = g.symm.trans refl
    have hlhs :
        g.symm.trans (g.trans f) = f := by
      rw [← LinearEquiv.trans_assoc, LinearEquiv.symm_trans_self, LinearEquiv.refl_trans]
    have hrhs : g.symm.trans (LinearEquiv.refl K V) = g.symm := by
      simp
    exact hlhs.symm.trans (hcongr.trans hrhs)
  calc
    f.trans g = g.symm.trans g := by rw [hf_symm]
    _ = LinearEquiv.refl K V := LinearEquiv.symm_trans_self _

end D0.Geometry
