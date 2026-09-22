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

theorem homogeneousCochain_zero (N k : ℕ) :
    HomogeneousCochain N k (0 : ArchiveCochain N) := by
  intro x S hS
  rfl

theorem homogeneousCochain_add (N k : ℕ) (ψ φ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ)
    (hφ : HomogeneousCochain N k φ) :
    HomogeneousCochain N k (ψ + φ) := by
  intro x S hS
  simp [hψ x S hS, hφ x S hS]

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

/-- Forward difference distributes through a finite sum with site-independent coefficients. -/
theorem forwardDifference_weighted_sum {ι : Type*} [Fintype ι]
    (N : ℕ) (r : Role) (c : ι → ℝ)
    (F : ι → ArchiveRolePhaseGroup N → ℝ) :
    forwardDifference N r (fun x => ∑ i, c i * F i x) =
      fun x => ∑ i, c i * forwardDifference N r (F i) x := by
  classical
  funext x
  simp only [forwardDifference_apply]
  calc
    forwardDifferenceScale N *
        ((∑ i, c i * F i (roleTranslatePlus N r x)) -
          ∑ i, c i * F i x) =
      forwardDifferenceScale N *
        (∑ i, (c i * F i (roleTranslatePlus N r x) - c i * F i x)) := by
          rw [Finset.sum_sub_distrib]
    _ = ∑ i, forwardDifferenceScale N *
        (c i * F i (roleTranslatePlus N r x) - c i * F i x) := by
          rw [Finset.mul_sum]
    _ = ∑ i, c i *
        (forwardDifferenceScale N *
          (F i (roleTranslatePlus N r x) - F i x)) := by
          apply Finset.sum_congr rfl
          intro i hi
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

/-- Apply a directional forward difference without changing the Fock label. -/
noncomputable def forwardSite (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => forwardDifference N r (fun x => ψ (x, p.2)) p.1

/-- Apply the Fock creation matrix at each site. -/
noncomputable def createAction (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ∑ ket : ArchiveFockState, carCreate r p.2 ket * ψ (p.1, ket)

/-- One directional summand ∇_r^+ c_r†. -/
noncomputable def forwardCreateDirection (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p =>
    ∑ ket : ArchiveFockState,
      carCreate r p.2 ket *
        forwardDifference N r (fun x => ψ (x, ket)) p.1

theorem forwardCreateDirection_eq_createAction_forwardSite (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) :
    forwardCreateDirection N r ψ = createAction N r (forwardSite N r ψ) := by
  rfl

theorem forwardSite_comm (N : ℕ) (r s : Role) (ψ : ArchiveCochain N) :
    forwardSite N r (forwardSite N s ψ) =
      forwardSite N s (forwardSite N r ψ) := by
  funext p
  change
    forwardDifference N r
        (forwardDifference N s (fun x => ψ (x, p.2))) p.1 =
      forwardDifference N s
        (forwardDifference N r (fun x => ψ (x, p.2))) p.1
  exact congrFun (forwardDifference_comm N r s (fun x => ψ (x, p.2))) p.1

theorem forwardSite_createAction_comm (N : ℕ) (r s : Role)
    (ψ : ArchiveCochain N) :
    forwardSite N r (createAction N s ψ) =
      createAction N s (forwardSite N r ψ) := by
  classical
  funext p
  change
    forwardDifference N r
        (fun x => ∑ ket : ArchiveFockState,
          carCreate s p.2 ket * ψ (x, ket)) p.1 =
      ∑ ket : ArchiveFockState,
        carCreate s p.2 ket *
          forwardDifference N r (fun x => ψ (x, ket)) p.1
  exact congrFun
    (forwardDifference_weighted_sum N r
      (fun ket : ArchiveFockState => carCreate s p.2 ket)
      (fun ket x => ψ (x, ket))) p.1

theorem createAction_comp_apply (N : ℕ) (r s : Role)
    (ψ : ArchiveCochain N) (p : ArchiveCochainBasis N) :
    createAction N r (createAction N s ψ) p =
      ∑ ket : ArchiveFockState,
        (∑ mid : ArchiveFockState,
          carCreate r p.2 mid * carCreate s mid ket) * ψ (p.1, ket) := by
  classical
  unfold createAction
  calc
    (∑ mid : ArchiveFockState,
      carCreate r p.2 mid *
        (∑ ket : ArchiveFockState,
          carCreate s mid ket * ψ (p.1, ket))) =
      ∑ mid : ArchiveFockState, ∑ ket : ArchiveFockState,
        carCreate r p.2 mid *
          (carCreate s mid ket * ψ (p.1, ket)) := by
            apply Finset.sum_congr rfl
            intro mid hmid
            rw [Finset.mul_sum]
    _ = ∑ ket : ArchiveFockState, ∑ mid : ArchiveFockState,
        carCreate r p.2 mid *
          (carCreate s mid ket * ψ (p.1, ket)) := by
            rw [Finset.sum_comm]
    _ = ∑ ket : ArchiveFockState,
        (∑ mid : ArchiveFockState,
          carCreate r p.2 mid * carCreate s mid ket) * ψ (p.1, ket) := by
            apply Finset.sum_congr rfl
            intro ket hket
            rw [Finset.sum_mul]
            apply Finset.sum_congr rfl
            intro mid hmid
            ring

/-- Creation actions anticommute as literal cochain operators. -/
theorem createAction_anticommute (N : ℕ) (r s : Role)
    (ψ : ArchiveCochain N) :
    createAction N r (createAction N s ψ) +
      createAction N s (createAction N r ψ) = 0 := by
  classical
  funext p
  simp only [Pi.add_apply, Pi.zero_apply]
  rw [createAction_comp_apply, createAction_comp_apply]
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_eq_zero
  intro ket hket
  rw [← add_mul]
  have hcar := car_create_anticommutator r s p.2 ket
  unfold anticommutator at hcar
  rw [hcar]
  simp

/-- Directional forward-create pieces anticommute. -/
theorem forwardCreateDirection_anticommute (N : ℕ) (r s : Role)
    (ψ : ArchiveCochain N) :
    forwardCreateDirection N r (forwardCreateDirection N s ψ) +
      forwardCreateDirection N s (forwardCreateDirection N r ψ) = 0 := by
  change
    createAction N r
        (forwardSite N r (createAction N s (forwardSite N s ψ))) +
      createAction N s
        (forwardSite N s (createAction N r (forwardSite N r ψ))) = 0
  rw [forwardSite_createAction_comm N r s (forwardSite N s ψ)]
  rw [forwardSite_createAction_comm N s r (forwardSite N r ψ)]
  rw [forwardSite_comm N s r ψ]
  exact createAction_anticommute N r s
    (forwardSite N r (forwardSite N s ψ))

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

theorem dForward_eq_sum_directions (N : ℕ) (ψ : ArchiveCochain N) :
    dForward N ψ = ∑ r : Role, forwardCreateDirection N r ψ := by
  funext p
  simp [dForward]

theorem dForward_sum {ι : Type*} [Fintype ι] (N : ℕ)
    (F : ι → ArchiveCochain N) :
    dForward N (∑ i, F i) = ∑ i, dForward N (F i) := by
  classical
  have hfin : ∀ s : Finset ι,
      dForward N (∑ i in s, F i) = ∑ i in s, dForward N (F i) := by
    intro s
    induction s using Finset.induction_on with
    | empty =>
        simp [dForward_zero]
    | @insert a s ha ih =>
        rw [Finset.sum_insert ha, dForward_add, Finset.sum_insert ha, ih]
  exact hfin Finset.univ

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
  classical
  funext x
  unfold oneFormComponent dForward forwardCreateDirection
  have hinner : ∀ s : Role,
      (∑ ket : ArchiveFockState,
        carCreate s (singletonFockState r) ket *
          forwardDifference N s (fun y => scalarCochain N f (y, ket)) x) =
        roleDelta s r * forwardDifference N s f x := by
    intro s
    rw [Finset.sum_eq_single vacuumFockState]
    · simp [scalarCochain, carCreate_singleton_vacuum]
    · intro ket _ hket
      have hz : (fun y : ArchiveRolePhaseGroup N =>
          scalarCochain N f (y, ket)) = 0 := by
        funext y
        simp [scalarCochain, hket]
      rw [hz, forwardDifference_zero]
      simp
    · simp
  simp_rw [hinner]
  rw [Finset.sum_eq_single r]
  · simp [roleDelta]
  · intro s _ hsr
    simp [roleDelta, hsr]
  · simp

/-- Canonical nilpotency.  Algebraically this is the pairwise cancellation of
commuting forward differences against the creation-creation CAR. -/
theorem dForward_sq_zero (N : ℕ) (ψ : ArchiveCochain N) :
    dForward N (dForward N ψ) = 0 := by
  classical
  rw [dForward_eq_sum_directions N ψ, dForward_sum]
  simp_rw [dForward_eq_sum_directions]
  funext p
  simp only [Finset.sum_apply, Pi.zero_apply]
  let X : Role → Role → ℝ :=
    fun r s => forwardCreateDirection N r
      (forwardCreateDirection N s ψ) p
  change (∑ s : Role, ∑ r : Role, X r s) = 0
  have hanti : ∀ r s : Role, X r s + X s r = 0 := by
    intro r s
    have h := congrFun (forwardCreateDirection_anticommute N r s ψ) p
    simpa [X] using h
  have hpair : (∑ s : Role, ∑ r : Role, (X r s + X s r)) = 0 := by
    apply Finset.sum_eq_zero
    intro s hs
    apply Finset.sum_eq_zero
    intro r hr
    exact hanti r s
  have hswap :
      (∑ s : Role, ∑ r : Role, X s r) =
        ∑ s : Role, ∑ r : Role, X r s := by
    rw [Finset.sum_comm]
  simp only [Finset.sum_add_distrib] at hpair
  rw [hswap] at hpair
  linarith

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

/-- Centered difference distributes through finite site-independent weights. -/
theorem centeredDifference_weighted_sum {ι : Type*} [Fintype ι]
    (N : ℕ) (r : Role) (c : ι → ℝ)
    (F : ι → ArchiveRolePhaseGroup N → ℝ) :
    centeredDifference N r (fun x => ∑ i, c i * F i x) =
      fun x => ∑ i, c i * centeredDifference N r (F i) x := by
  classical
  funext x
  simp only [centeredDifference_apply]
  calc
    centeredDifferenceScale N *
        ((∑ i, c i * F i (roleTranslatePlus N r x)) -
          ∑ i, c i * F i (roleTranslateMinus N r x)) =
      centeredDifferenceScale N *
        (∑ i, (c i * F i (roleTranslatePlus N r x) -
          c i * F i (roleTranslateMinus N r x))) := by
            rw [Finset.sum_sub_distrib]
    _ = ∑ i, centeredDifferenceScale N *
        (c i * F i (roleTranslatePlus N r x) -
          c i * F i (roleTranslateMinus N r x)) := by
            rw [Finset.mul_sum]
    _ = ∑ i, c i *
        (centeredDifferenceScale N *
          (F i (roleTranslatePlus N r x) -
            F i (roleTranslateMinus N r x))) := by
            apply Finset.sum_congr rfl
            intro i hi
            ring

noncomputable def centeredSite (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => centeredDifference N r (fun x => ψ (x, p.2)) p.1

noncomputable def centeredCreateDirection (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p =>
    ∑ ket : ArchiveFockState,
      carCreate r p.2 ket *
        centeredDifference N r (fun x => ψ (x, ket)) p.1

theorem centeredCreateDirection_eq_createAction_centeredSite (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) :
    centeredCreateDirection N r ψ =
      createAction N r (centeredSite N r ψ) := by
  rfl

theorem centeredSite_comm (N : ℕ) (r s : Role) (ψ : ArchiveCochain N) :
    centeredSite N r (centeredSite N s ψ) =
      centeredSite N s (centeredSite N r ψ) := by
  funext p
  change
    centeredDifference N r
        (centeredDifference N s (fun x => ψ (x, p.2))) p.1 =
      centeredDifference N s
        (centeredDifference N r (fun x => ψ (x, p.2))) p.1
  exact congrFun (centeredDifference_comm N r s (fun x => ψ (x, p.2))) p.1

theorem centeredSite_createAction_comm (N : ℕ) (r s : Role)
    (ψ : ArchiveCochain N) :
    centeredSite N r (createAction N s ψ) =
      createAction N s (centeredSite N r ψ) := by
  classical
  funext p
  change
    centeredDifference N r
        (fun x => ∑ ket : ArchiveFockState,
          carCreate s p.2 ket * ψ (x, ket)) p.1 =
      ∑ ket : ArchiveFockState,
        carCreate s p.2 ket *
          centeredDifference N r (fun x => ψ (x, ket)) p.1
  exact congrFun
    (centeredDifference_weighted_sum N r
      (fun ket : ArchiveFockState => carCreate s p.2 ket)
      (fun ket x => ψ (x, ket))) p.1

theorem centeredCreateDirection_anticommute (N : ℕ) (r s : Role)
    (ψ : ArchiveCochain N) :
    centeredCreateDirection N r (centeredCreateDirection N s ψ) +
      centeredCreateDirection N s (centeredCreateDirection N r ψ) = 0 := by
  change
    createAction N r
        (centeredSite N r (createAction N s (centeredSite N s ψ))) +
      createAction N s
        (centeredSite N s (createAction N r (centeredSite N r ψ))) = 0
  rw [centeredSite_createAction_comm N r s (centeredSite N s ψ)]
  rw [centeredSite_createAction_comm N s r (centeredSite N r ψ)]
  rw [centeredSite_comm N s r ψ]
  exact createAction_anticommute N r s
    (centeredSite N r (centeredSite N s ψ))

noncomputable def dCentered (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ∑ r : Role, centeredCreateDirection N r ψ p

@[simp] theorem dCentered_zero (N : ℕ) :
    dCentered N (0 : ArchiveCochain N) = 0 := by
  funext p
  simp [dCentered, centeredCreateDirection, centeredDifference_apply]

theorem dCentered_add (N : ℕ) (ψ φ : ArchiveCochain N) :
    dCentered N (ψ + φ) = dCentered N ψ + dCentered N φ := by
  funext p
  simp [dCentered, centeredCreateDirection, centeredDifference_apply]
  ring

theorem dCentered_eq_sum_directions (N : ℕ) (ψ : ArchiveCochain N) :
    dCentered N ψ = ∑ r : Role, centeredCreateDirection N r ψ := by
  funext p
  simp [dCentered]

theorem dCentered_sum {ι : Type*} [Fintype ι] (N : ℕ)
    (F : ι → ArchiveCochain N) :
    dCentered N (∑ i, F i) = ∑ i, dCentered N (F i) := by
  classical
  have hfin : ∀ s : Finset ι,
      dCentered N (∑ i in s, F i) = ∑ i in s, dCentered N (F i) := by
    intro s
    induction s using Finset.induction_on with
    | empty =>
        simp [dCentered_zero]
    | @insert a s ha ih =>
        rw [Finset.sum_insert ha, dCentered_add, Finset.sum_insert ha, ih]
  exact hfin Finset.univ

theorem dCentered_sq_zero (N : ℕ) (ψ : ArchiveCochain N) :
    dCentered N (dCentered N ψ) = 0 := by
  classical
  rw [dCentered_eq_sum_directions N ψ, dCentered_sum]
  simp_rw [dCentered_eq_sum_directions]
  funext p
  simp only [Finset.sum_apply, Pi.zero_apply]
  let X : Role → Role → ℝ :=
    fun r s => centeredCreateDirection N r
      (centeredCreateDirection N s ψ) p
  change (∑ s : Role, ∑ r : Role, X r s) = 0
  have hanti : ∀ r s : Role, X r s + X s r = 0 := by
    intro r s
    have h := congrFun (centeredCreateDirection_anticommute N r s ψ) p
    simpa [X] using h
  have hpair : (∑ s : Role, ∑ r : Role, (X r s + X s r)) = 0 := by
    apply Finset.sum_eq_zero
    intro s hs
    apply Finset.sum_eq_zero
    intro r hr
    exact hanti r s
  have hswap :
      (∑ s : Role, ∑ r : Role, X s r) =
        ∑ s : Role, ∑ r : Role, X r s := by
    rw [Finset.sum_comm]
  simp only [Finset.sum_add_distrib] at hpair
  rw [hswap] at hpair
  linarith

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
