import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic
import D0.Geometry.ArchiveCARRelations
import D0.Geometry.ArchiveRolePhaseGroup
import D0.Geometry.A4DSymRoleCentralDifference

namespace D0.Geometry

open D0
open scoped BigOperators

/-!
# D0.Geometry.ArchiveCubicalDifferential

Candidate literal cubical cochain/differential implementation for
`WRK-A4D-CUBICAL-DIFFERENTIAL-CARTAN`.

This module is deliberately finite.  The topological differential is the forward operator
  d_f = sum_r (N+2) (U_r - I) c_r†.
The already-owned centered derivative is related to it by exact backward link averaging.
No Hodge/Ward, stress, continuum Diff, or Einstein statement is made here.
-/

/-- Literal basis of archive cubical cochains: site × exterior/Fock label. -/
abbrev ArchiveCochainBasis (N : ℕ) : Type :=
  ArchiveRolePhaseGroup N × ArchiveFockState

/-- Real cubical cochain amplitudes. -/
abbrev ArchiveCochain (N : ℕ) : Type :=
  ArchiveCochainBasis N → ℝ

/-- Public vacuum label for scalar cochains. -/
abbrev vacuumFockState : ArchiveFockState := fockVacuumState

/-- Public singleton one-form label. -/
abbrev singletonFockState (r : Role) : ArchiveFockState := fockSingletonState r

/-- Embed a scalar field as the degree-zero Fock component. -/
def scalarCochain (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ) : ArchiveCochain N :=
  fun p => if p.2 = vacuumFockState then f p.1 else 0

/-- Read the scalar component. -/
def scalarComponent (N : ℕ) (ψ : ArchiveCochain N) :
    ArchiveRolePhaseGroup N → ℝ :=
  fun x => ψ (x, vacuumFockState)

/-- Read the coefficient of the singleton one-form in role `r`. -/
def oneFormComponent (N : ℕ) (ψ : ArchiveCochain N) (r : Role) :
    ArchiveRolePhaseGroup N → ℝ :=
  fun x => ψ (x, singletonFockState r)

/-- Embed a role one-form field into the singleton Fock sector. -/
def oneFormCochain (N : ℕ) (α : LocalRoleVector N) : ArchiveCochain N :=
  fun p => ∑ r : Role, if p.2 = singletonFockState r then α p.1 r else 0

/-- Homogeneous degree support. -/
def HomogeneousCochain (N k : ℕ) (ψ : ArchiveCochain N) : Prop :=
  ∀ x S, fockDegree S ≠ k → ψ (x, S) = 0

/-- Archive derivative scale L = N+2. -/
noncomputable def forwardDifferenceScale (N : ℕ) : ℝ :=
  (archiveFibers N : ℝ)

/-- Forward role difference `L (U_r - I)`. -/
noncomputable def forwardDifference (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) : ArchiveRolePhaseGroup N → ℝ :=
  fun x => forwardDifferenceScale N *
    (f (roleTranslatePlus N r x) - f x)

/-- Backward role difference `L (I - U_r^{-1})`. -/
noncomputable def backwardDifference (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) : ArchiveRolePhaseGroup N → ℝ :=
  fun x => forwardDifferenceScale N *
    (f x - f (roleTranslateMinus N r x))

@[simp] theorem forwardDifference_apply (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) :
    forwardDifference N r f x =
      forwardDifferenceScale N * (f (roleTranslatePlus N r x) - f x) := rfl

@[simp] theorem backwardDifference_apply (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) :
    backwardDifference N r f x =
      forwardDifferenceScale N * (f x - f (roleTranslateMinus N r x)) := rfl

theorem forwardDifference_zero (N : ℕ) (r : Role) :
    forwardDifference N r (fun _ => 0) = 0 := by
  funext x
  simp [forwardDifference]

theorem forwardDifference_const (N : ℕ) (r : Role) (c : ℝ) :
    forwardDifference N r (fun _ => c) = 0 := by
  funext x
  simp [forwardDifference]

theorem forwardDifference_add (N : ℕ) (r : Role)
    (f g : ArchiveRolePhaseGroup N → ℝ) :
    forwardDifference N r (f + g) =
      forwardDifference N r f + forwardDifference N r g := by
  funext x
  simp [forwardDifference]
  ring

theorem forwardDifference_smul (N : ℕ) (r : Role) (c : ℝ)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    forwardDifference N r (c • f) = c • forwardDifference N r f := by
  funext x
  simp [forwardDifference]
  ring

/-- Independent role translations commute, hence so do forward differences. -/
theorem forwardDifference_comm (N : ℕ) (r s : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    forwardDifference N r (forwardDifference N s f) =
      forwardDifference N s (forwardDifference N r f) := by
  funext x
  have h :
      roleTranslatePlus N s (roleTranslatePlus N r x) =
        roleTranslatePlus N r (roleTranslatePlus N s x) := by
    dsimp [roleTranslatePlus, roleTranslate]
    abel
  simp only [forwardDifference_apply]
  rw [h]
  ring

/-- Pointwise radius-one statement for one directional forward difference. -/
theorem forwardDifference_local (N : ℕ) (r : Role)
    (f g : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N)
    (hx : f x = g x)
    (hplus : f (roleTranslatePlus N r x) = g (roleTranslatePlus N r x)) :
    forwardDifference N r f x = forwardDifference N r g x := by
  simp [forwardDifference, hx, hplus]

/-- Flat counting-pairing adjoint relation between forward and backward differences. -/
theorem forward_backward_adjoint (N : ℕ) (r : Role)
    (f g : ArchiveRolePhaseGroup N → ℝ) :
    (∑ x, forwardDifference N r f x * g x) =
      -∑ x, f x * backwardDifference N r g x := by
  classical
  let e : ArchiveRolePhaseGroup N := roleStep N r
  have hplus :
      (∑ x, f (x + e) * g x) = ∑ x, f x * g (x - e) := by
    simpa [e, roleTranslateEquiv] using
      (sum_translate N e (fun y => f y * g (y - e)))
  simp only [forwardDifference_apply, backwardDifference_apply,
    roleTranslatePlus_apply, roleTranslateMinus_apply, e]
  calc
    (∑ x, forwardDifferenceScale N * (f (x + roleStep N r) - f x) * g x) =
        forwardDifferenceScale N * (∑ x, f (x + e) * g x) -
          forwardDifferenceScale N * (∑ x, f x * g x) := by
      simp [e, Finset.mul_sum, mul_sub]
      ring
    _ = forwardDifferenceScale N * (∑ x, f x * g (x - e)) -
          forwardDifferenceScale N * (∑ x, f x * g x) := by
      rw [hplus]
    _ = -∑ x, f x *
          (forwardDifferenceScale N * (g x - g (x - roleStep N r))) := by
      simp [e, Finset.mul_sum, mul_sub]
      ring

/-! ## Exact forward-to-centered bridge -/

/-- Link-to-vertex backward averaging A_r = (I + U_r^{-1})/2. -/
def backwardAverage (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) : ArchiveRolePhaseGroup N → ℝ :=
  fun x => (f x + f (roleTranslateMinus N r x)) / 2

@[simp] theorem backwardAverage_apply (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) :
    backwardAverage N r f x =
      (f x + f (roleTranslateMinus N r x)) / 2 := rfl

/-- Exact finite identity D_r = A_r ∘ ∇_r^+. -/
theorem centeredDifference_eq_average_forward (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    centeredDifference N r f =
      backwardAverage N r (forwardDifference N r f) := by
  funext x
  have hcancel :
      roleTranslatePlus N r (roleTranslateMinus N r x) = x := by
    dsimp [roleTranslatePlus, roleTranslateMinus, roleTranslate]
    abel
  simp only [centeredDifference_apply, backwardAverage_apply,
    forwardDifference_apply]
  rw [hcancel]
  unfold centeredDifferenceScale forwardDifferenceScale
  ring

/-! ## Literal forward cubical differential -/

/-- One directional summand ∇_r^+ c_r†. -/
noncomputable def forwardCreateDirection (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p =>
    ∑ ket : ArchiveFockState,
      carCreate r p.2 ket *
        forwardDifference N r (fun x => ψ (x, ket)) p.1

/-- Canonical forward cubical differential
`d_f = sum_r ∇_r^+ c_r†`. -/
noncomputable def dForward (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ∑ r : Role, forwardCreateDirection N r ψ p

@[simp] theorem dForward_zero (N : ℕ) :
    dForward N (0 : ArchiveCochain N) = 0 := by
  funext p
  simp [dForward, forwardCreateDirection, forwardDifference]

theorem dForward_add (N : ℕ) (ψ φ : ArchiveCochain N) :
    dForward N (ψ + φ) = dForward N ψ + dForward N φ := by
  funext p
  simp [dForward, forwardCreateDirection, forwardDifference]
  ring

theorem dForward_smul (N : ℕ) (c : ℝ) (ψ : ArchiveCochain N) :
    dForward N (c • ψ) = c • dForward N ψ := by
  funext p
  simp [dForward, forwardCreateDirection, forwardDifference]
  ring

/-- The full differential at x only samples x and the four forward neighbours. -/
theorem dForward_radius_one (N : ℕ) (ψ φ : ArchiveCochain N)
    (x : ArchiveRolePhaseGroup N) (bra : ArchiveFockState)
    (h :
      ∀ r ket,
        ψ (x, ket) = φ (x, ket) ∧
        ψ (roleTranslatePlus N r x, ket) =
          φ (roleTranslatePlus N r x, ket)) :
    dForward N ψ (x, bra) = dForward N φ (x, bra) := by
  unfold dForward forwardCreateDirection
  apply Finset.sum_congr rfl
  intro r hr
  apply Finset.sum_congr rfl
  intro ket hk
  congr 1
  apply forwardDifference_local
  · exact (h r ket).1
  · exact (h r ket).2

/-- Degree raising follows from creation support and does not rely on nilpotency. -/
theorem dForward_degree_raise (N k : ℕ) (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N (k + 1) (dForward N ψ) := by
  classical
  intro x bra hbra
  unfold dForward forwardCreateDirection
  apply Finset.sum_eq_zero
  intro r hr
  apply Finset.sum_eq_zero
  intro ket hk
  by_cases hc : carCreate r bra ket = 0
  · simp [hc]
  · have hdeg := carCreate_degree_raise r bra ket hc
    have hket : fockDegree ket ≠ k := by
      intro hkdeg
      apply hbra
      omega
    have hx := hψ x ket hket
    have hxp := hψ (roleTranslatePlus N r x) ket hket
    simp [forwardDifference, hc, hx, hxp]

/-- Coefficient of d_f on an embedded scalar is the directional forward derivative. -/
theorem dForward_scalar_oneForm_component (N : ℕ)
    (f : ArchiveRolePhaseGroup N → ℝ) (r : Role) :
    oneFormComponent N (dForward N (scalarCochain N f)) r =
      forwardDifference N r f := by
  -- The only surviving fiber coefficient is
  -- <{r}| c_s† |vac> = δ_sr.  The finite CAR coefficient theorem above
  -- makes this a small sum-collapse proof for the local worker to elaborate.
  sorry

/-- Canonical nilpotency.  Algebraically this is the pairwise cancellation of
commuting forward differences against the creation-creation CAR. -/
theorem dForward_sq_zero (N : ℕ) (ψ : ArchiveCochain N) :
    dForward N (dForward N ψ) = 0 := by
  -- Proof plan for the local verifier:
  -- 1. expand the two finite Role sums and the intermediate Fock sum;
  -- 2. use forwardDifference_comm;
  -- 3. swap (r,s);
  -- 4. close each paired coefficient with car_create_anticommutator.
  sorry

/-! ## One-form centering -/

/-- Center each singleton one-form coefficient along its own role direction. -/
def centerOneForm (N : ℕ) (ψ : ArchiveCochain N) : LocalRoleVector N :=
  fun x r =>
    backwardAverage N r (oneFormComponent N ψ r) x

/-- The centered gradient of a scalar field, on the existing centered Role calculus. -/
noncomputable def centeredScalarGradient (N : ℕ)
    (f : ArchiveRolePhaseGroup N → ℝ) : LocalRoleVector N :=
  fun x r => centeredDifference N r f x

/-- Exact one-form bridge C1(d_f f) = D f. -/
theorem centerOneForm_dForward_scalar (N : ℕ)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    centerOneForm N (dForward N (scalarCochain N f)) =
      centeredScalarGradient N f := by
  funext x r
  unfold centerOneForm centeredScalarGradient
  rw [dForward_scalar_oneForm_component]
  exact congrFun (centeredDifference_eq_average_forward N r f).symm x

/-! ## Centered diagnostic differential

This is diagnostic only.  It is not the topological owner: at N=0 (L=2) every centered
difference vanishes.
-/

noncomputable def centeredCreateDirection (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p =>
    ∑ ket : ArchiveFockState,
      carCreate r p.2 ket *
        centeredDifference N r (fun x => ψ (x, ket)) p.1

noncomputable def dCentered (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ∑ r : Role, centeredCreateDirection N r ψ p

theorem dCentered_sq_zero (N : ℕ) (ψ : ArchiveCochain N) :
    dCentered N (dCentered N ψ) = 0 := by
  -- Same CAR cancellation as dForward, now using centeredDifference_comm.
  sorry

theorem dCentered_zero_at_minimal (ψ : ArchiveCochain 0) :
    dCentered 0 ψ = 0 := by
  funext p
  unfold dCentered centeredCreateDirection
  apply Finset.sum_eq_zero
  intro r hr
  apply Finset.sum_eq_zero
  intro ket hk
  have hz := congrArg
    (fun D =>
      D (fun x : ArchiveRolePhaseGroup 0 => ψ (x, ket)) p.1)
    (centeredDifference_zero r)
  simp at hz
  simp [hz]

end D0.Geometry
