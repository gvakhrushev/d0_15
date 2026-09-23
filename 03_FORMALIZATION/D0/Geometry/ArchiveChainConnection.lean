import Mathlib.Algebra.Module.Equiv.Basic
import Mathlib.Tactic
import D0.Geometry.ArchiveTwistedRoleDifference
import D0.Geometry.A4DSymRoleCentralDifference

/-!
# Finite chain connection

Stored link `U x r : V ≃ₗ[K] V` is the pull `V_{x+r} → V_x`.
Cochain transport is `(T_r ψ) x = U x r (ψ (x+r))`.

This is ordinary finite node-gauge/link algebra. It is not a centered-Cartan
transformation and does not select a physical connection.
-/

namespace D0.Geometry

open D0

variable {N : ℕ} {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

abbrev LinkConnection (N : ℕ) (K V : Type*) [Field K] [AddCommGroup V] [Module K V] :=
  ArchiveRolePhaseGroup N → Role → (V ≃ₗ[K] V)

abbrev NodeGauge (N : ℕ) (K V : Type*) [Field K] [AddCommGroup V] [Module K V] :=
  ArchiveRolePhaseGroup N → (V ≃ₗ[K] V)

abbrev CoefficientSection (N : ℕ) (V : Type*) :=
  ArchiveRolePhaseGroup N → V

def gaugeLink (g : NodeGauge N K V) (U : LinkConnection N K V)
    (x : ArchiveRolePhaseGroup N) (r : Role) : V ≃ₗ[K] V :=
  ((g (roleTranslatePlus N r x)).symm.trans (U x r)).trans (g x)

def linkTransport (U : LinkConnection N K V) (r : Role)
    (ψ : CoefficientSection N V) (x : ArchiveRolePhaseGroup N) : V :=
  (U x r) (ψ (roleTranslatePlus N r x))

def gaugeSection (g : NodeGauge N K V) (ψ : CoefficientSection N V)
    (x : ArchiveRolePhaseGroup N) : V :=
  (g x) (ψ x)

def inverseLinkTransport (U : LinkConnection N K V) (r : Role)
    (ψ : CoefficientSection N V) (x : ArchiveRolePhaseGroup N) : V :=
  (U (roleTranslateMinus N r x) r).symm (ψ (roleTranslateMinus N r x))

def translateLink (b : ArchiveRolePhaseGroup N) (U : LinkConnection N K V) :
    LinkConnection N K V :=
  fun x r => U (x + b) r

def translateSection (b : ArchiveRolePhaseGroup N) (ψ : CoefficientSection N V) :
    CoefficientSection N V :=
  fun x => ψ (x - b)

theorem transport_gauge (g : NodeGauge N K V) (U : LinkConnection N K V)
    (r : Role) (ψ : CoefficientSection N V) :
    linkTransport (gaugeLink g U) r (gaugeSection g ψ) =
      gaugeSection g (linkTransport U r ψ) := by
  funext x
  simp [linkTransport, gaugeLink, gaugeSection, LinearEquiv.trans_apply,
    LinearEquiv.symm_apply_apply]

theorem transport_inverse_left (U : LinkConnection N K V) (r : Role)
    (ψ : CoefficientSection N V) :
    inverseLinkTransport U r (linkTransport U r ψ) = ψ := by
  funext x
  simp [inverseLinkTransport, linkTransport, roleTranslate_inverse_plus,
    LinearEquiv.symm_apply_apply]

theorem transport_inverse_right (U : LinkConnection N K V) (r : Role)
    (ψ : CoefficientSection N V) :
    linkTransport U r (inverseLinkTransport U r ψ) = ψ := by
  funext x
  simp [inverseLinkTransport, linkTransport, roleTranslate_inverse_minus,
    LinearEquiv.apply_symm_apply]

theorem inverseTransport_gauge (g : NodeGauge N K V) (U : LinkConnection N K V)
    (r : Role) (ψ : CoefficientSection N V) :
    inverseLinkTransport (gaugeLink g U) r (gaugeSection g ψ) =
      gaugeSection g (inverseLinkTransport U r ψ) := by
  funext x
  have hy : roleTranslatePlus N r (roleTranslateMinus N r x) = x :=
    roleTranslate_inverse_plus N r x
  simp only [inverseLinkTransport, gaugeSection, gaugeLink, hy]
  rw [LinearEquiv.symm_trans_apply]
  simp only [LinearEquiv.symm_apply_apply]
  rw [LinearEquiv.symm_trans_apply]
  simp only [LinearEquiv.symm_symm]

theorem transport_translate (b : ArchiveRolePhaseGroup N) (U : LinkConnection N K V)
    (r : Role) (ψ : CoefficientSection N V) :
    linkTransport (translateLink b U) r ψ =
      fun x => linkTransport U r (fun y => ψ (y - b)) (x + b) := by
  funext x
  simp only [linkTransport, translateLink, roleTranslatePlus_apply]
  congr 1
  simp only [sub_eq_add_neg]
  abel_nf

/-- Oriented steps. Forward and backward links stay distinct at `L = 2`. -/
inductive ChainStep
  | fwd (r : Role)
  | bwd (r : Role)
  deriving DecidableEq

def stepTransport (U : LinkConnection N K V) : ChainStep →
    CoefficientSection N V → CoefficientSection N V
  | .fwd r, ψ => linkTransport U r ψ
  | .bwd r, ψ => inverseLinkTransport U r ψ

def pathTransport (U : LinkConnection N K V) (steps : List ChainStep)
    (ψ : CoefficientSection N V) : CoefficientSection N V :=
  steps.foldr (stepTransport U) ψ

theorem pathTransport_nil (U : LinkConnection N K V) (ψ : CoefficientSection N V) :
    pathTransport U [] ψ = ψ := rfl

theorem pathTransport_append (U : LinkConnection N K V)
    (p q : List ChainStep) (ψ : CoefficientSection N V) :
    pathTransport U (p ++ q) ψ = pathTransport U p (pathTransport U q ψ) := by
  simp [pathTransport, List.foldr_append]

def reverseStep : ChainStep → ChainStep
  | .fwd r => .bwd r
  | .bwd r => .fwd r

theorem stepTransport_reverseStep (U : LinkConnection N K V) (s : ChainStep)
    (ψ : CoefficientSection N V) :
    stepTransport U (reverseStep s) (stepTransport U s ψ) = ψ := by
  cases s with
  | fwd r => simpa [reverseStep, stepTransport] using transport_inverse_left U r ψ
  | bwd r => simpa [reverseStep, stepTransport] using transport_inverse_right U r ψ

theorem pathTransport_reverse (U : LinkConnection N K V) (steps : List ChainStep)
    (ψ : CoefficientSection N V) :
    pathTransport U (steps.map reverseStep).reverse (pathTransport U steps ψ) = ψ := by
  induction steps with
  | nil => rfl
  | cons s rest ih =>
      calc
        pathTransport U ((s :: rest).map reverseStep).reverse
            (pathTransport U (s :: rest) ψ) =
          pathTransport U ((rest.map reverseStep).reverse ++ [reverseStep s])
            (stepTransport U s (pathTransport U rest ψ)) := by
            simp [pathTransport, List.map_cons, List.reverse_cons]
        _ = pathTransport U (rest.map reverseStep).reverse
            (stepTransport U (reverseStep s)
              (stepTransport U s (pathTransport U rest ψ))) := by
            simp [pathTransport, List.foldr_append]
        _ = pathTransport U (rest.map reverseStep).reverse (pathTransport U rest ψ) := by
            rw [stepTransport_reverseStep]
        _ = ψ := ih

theorem pathTransport_gauge (g : NodeGauge N K V) (U : LinkConnection N K V)
    (steps : List ChainStep) (ψ : CoefficientSection N V) :
    pathTransport (fun x r => gaugeLink g U x r) steps (gaugeSection g ψ) =
      gaugeSection g (pathTransport U steps ψ) := by
  induction steps with
  | nil => rfl
  | cons s rest ih =>
      cases s with
      | fwd r =>
          simpa [pathTransport, stepTransport, transport_gauge] using
            congrArg (linkTransport (fun x r => gaugeLink g U x r) r) ih
      | bwd r =>
          simpa [pathTransport, stepTransport, inverseTransport_gauge] using
            congrArg (inverseLinkTransport (fun x r => gaugeLink g U x r) r) ih

/-- Two forward steps in one role return to the base when each role cycle has length 2. -/
theorem period_two_double_step (hL : archiveFibers N = 2) (r : Role)
    (x : ArchiveRolePhaseGroup N) :
    roleTranslatePlus N r (roleTranslatePlus N r x) = x := by
  funext s
  by_cases hs : s = r
  · subst hs
    simp only [roleTranslatePlus_apply, roleStep, Pi.add_apply, if_true, add_assoc]
    have h2 : ((2 : ℕ) : ZMod (archiveFibers N)) = 0 := by
      rw [hL.symm]
      exact ZMod.natCast_self _
    rw [show (1 : ZMod (archiveFibers N)) + 1 =
      ((2 : ℕ) : ZMod (archiveFibers N)) by norm_num, h2, add_zero]
  · simp [roleTranslatePlus, roleTranslate, roleStep, hs]

/-- At period 2 the forward edges based at `x` and at `x+r` share endpoints, and they
remain independent stored links. -/
theorem oriented_links_not_collapsed_at_period_two
    (hL : archiveFibers N = 2) (r : Role) (x : ArchiveRolePhaseGroup N) :
    roleTranslatePlus N r (roleTranslatePlus N r x) = x ∧
      ∃ U : LinkConnection N ℂ ℂ, U x r ≠ U (roleTranslatePlus N r x) r := by
  refine ⟨period_two_double_step hL r x, ?_⟩
  have hsite : roleTranslatePlus N r x ≠ x := by
    intro h
    have hcoord := congrFun h r
    simp only [roleTranslatePlus_apply, roleStep, Pi.add_apply, if_true] at hcoord
    have hzero : (1 : ZMod (archiveFibers N)) = 0 :=
      add_left_cancel (a := x r) (by simpa [add_zero] using hcoord)
    have hdiv : archiveFibers N ∣ 1 :=
      (ZMod.natCast_eq_zero_iff (1 : ℕ) (archiveFibers N)).mp (by simpa using hzero)
    have h1 : archiveFibers N = 1 := Nat.dvd_one.mp hdiv
    exact absurd (hL.symm.trans h1) (by decide)
  let e2 : ℂ ≃ₗ[ℂ] ℂ :=
    DistribMulAction.toLinearEquiv ℂ ℂ (Units.mk0 (2 : ℂ) (by norm_num))
  let U : LinkConnection N ℂ ℂ := fun y s =>
    if y = x ∧ s = r then e2 else LinearEquiv.refl ℂ ℂ
  refine ⟨U, ?_⟩
  intro hEq
  have hleft : U x r = e2 := by simp [U]
  have hright : U (roleTranslatePlus N r x) r = LinearEquiv.refl ℂ ℂ := by
    simp only [U]
    rw [if_neg (fun h => hsite h.1)]
  have happly : e2 (1 : ℂ) = (LinearEquiv.refl ℂ ℂ) (1 : ℂ) := by
    rw [← hleft, ← hright]
    exact congrFun (congrArg DFunLike.coe hEq) 1
  simp [e2, DistribMulAction.toLinearEquiv_apply, LinearEquiv.refl_apply] at happly

noncomputable def scalarSeamLink (h : ℂ) (hne : h ≠ 0) (r : Role) :
    LinkConnection N ℂ ℂ :=
  fun x s =>
    if hs : s = r then
      DistribMulAction.toLinearEquiv ℂ ℂ (Units.mk0 (seamFactor h (x r)) (by
        by_cases hx : x r = -1
        · simp [seamFactor, hx, hne]
        · simp [seamFactor, hx]))
    else
      LinearEquiv.refl ℂ ℂ

theorem seamConnection_recovers_twistedRoleShift (h : ℂ) (hne : h ≠ 0) (r : Role)
    (ψ : ArchiveRolePhaseGroup N → ℂ) :
    linkTransport (scalarSeamLink h hne r) r ψ = twistedRoleShift N r h ψ := by
  funext x
  simp [linkTransport, scalarSeamLink, twistedRoleShift, seamFactor, roleTranslatePlus,
    DistribMulAction.toLinearEquiv_apply]

end D0.Geometry
