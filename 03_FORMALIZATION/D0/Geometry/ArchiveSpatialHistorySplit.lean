import D0.Geometry.ArchiveHodgeCARDiracShell
import D0.Evolution.FeshbachSchurTimeDelayOwner

/-!
# Literal archive spatial factor and separate history carrier

A-invariance means precisely the one-step predicate in the existing Hodge
spatial-square theorem. Its cyclic orbit gives a structural factorization,
valid for every N including L=2, with the original 16-state Fock fibre.
Only the Hodge square is transported; no first-order spatial Dirac is asserted.

ARCHIVE-A-PHASE-NOT-USED-AS-HISTORY-COORDINATE: `HistoryIndex` reads the existing
Feshbach path grammar and is independent of the cyclic A coordinate. No map
from a history tick to A-phase is defined. The phi-ladder, tick-scale section,
and physical observer representation remain distinct structures.
CAUSAL-TIME-ROLE-INTERTWINER-MISSING is unchanged.
-/

namespace D0.Geometry
open D0
open scoped BigOperators
noncomputable section

abbrev SpatialRole := {r : Role // r ≠ A}

def spatialRoleB : SpatialRole := ⟨B, by decide⟩
def spatialRoleC : SpatialRole := ⟨C, by decide⟩
def spatialRoleD : SpatialRole := ⟨D, by decide⟩

theorem spatialRole_card_three : Fintype.card SpatialRole = 3 := by decide

/-- Explicit bridge to the existing shell's named b,c,d axes. -/
def spatialAxisEquivRole : SpatialAxis ≃ SpatialRole where
  toFun a := match a with
    | .b => spatialRoleB
    | .c => spatialRoleC
    | .d => spatialRoleD
  invFun r := if r.1 = B then .b else if r.1 = C then .c else .d
  left_inv a := by cases a <;> rfl
  right_inv r := by
    rcases r with ⟨⟨a,b⟩,h⟩
    fin_cases a <;> fin_cases b <;>
      simp [A, B, C, D, spatialRoleB, spatialRoleC, spatialRoleD] at h ⊢

@[simp] theorem spatialAxisEquivRole_val (a : SpatialAxis) :
    (spatialAxisEquivRole a).val = spatialAxisRole a := by cases a <;> rfl

abbrev SpatialArchivePhaseGroup (N : ℕ) := SpatialRole → ZMod (archiveFibers N)

theorem spatialArchivePhaseGroup_card (N : ℕ) :
    Fintype.card (SpatialArchivePhaseGroup N) = (archiveFibers N)^3 := by
  rw [Fintype.card_fun, ZMod.card, spatialRole_card_three]

def spatialProjection (N : ℕ) (x : ArchiveRolePhaseGroup N) : SpatialArchivePhaseGroup N :=
  fun r => x r.val

def spatialWithTime (N : ℕ) (t : ZMod (archiveFibers N))
    (y : SpatialArchivePhaseGroup N) : ArchiveRolePhaseGroup N :=
  fun r => if h : r = A then t else y ⟨r,h⟩

@[simp] theorem timeComponent_spatialWithTime (N : ℕ) (t : ZMod (archiveFibers N))
    (y : SpatialArchivePhaseGroup N) : spatialWithTime N t y A = t := by simp [spatialWithTime]
@[simp] theorem spatialWithTime_spatial (N : ℕ) (t : ZMod (archiveFibers N))
    (y : SpatialArchivePhaseGroup N) (r : SpatialRole) : spatialWithTime N t y r = y r := by
  simp [spatialWithTime, r.property]
@[simp] theorem spatialProjection_spatialWithTime (N : ℕ) (t : ZMod (archiveFibers N))
    (y : SpatialArchivePhaseGroup N) : spatialProjection N (spatialWithTime N t y) = y := by
  funext r
  exact spatialWithTime_spatial N t y r
@[simp] theorem spatialWithTime_projection (N : ℕ) (x : ArchiveRolePhaseGroup N) :
    spatialWithTime N (x A) (spatialProjection N x) = x := by
  funext r
  by_cases h : r = A
  · subst r; simp
  · simp [spatialWithTime, spatialProjection, h]

/-- Here `time` in the API name denotes only the distinguished cyclic A factor. -/
def archiveRolePhase_timeSpatialEquiv (N : ℕ) :
    ArchiveRolePhaseGroup N ≃ ZMod (archiveFibers N) × SpatialArchivePhaseGroup N where
  toFun x := (x A, spatialProjection N x)
  invFun p := spatialWithTime N p.1 p.2
  left_inv := spatialWithTime_projection N
  right_inv p := by simp

@[simp] theorem archiveRolePhase_timeSpatialEquiv_A (N : ℕ) (x : ArchiveRolePhaseGroup N) :
    (archiveRolePhase_timeSpatialEquiv N x).1 = x A := rfl
@[simp] theorem archiveRolePhase_timeSpatialEquiv_spatial (N : ℕ) (x : ArchiveRolePhaseGroup N) :
    (archiveRolePhase_timeSpatialEquiv N x).2 = spatialProjection N x := rfl

/-- Exact generic wrapper of the inline invariance hypothesis in the shell owner. -/
def AxisInvariantA (N : ℕ) {α : Type*} (f : ArchiveRolePhaseGroup N → α) : Prop :=
  ∀ x, f (roleTranslatePlus N A x) = f x

@[simp] theorem spatialProjection_translate_A (N : ℕ) (x : ArchiveRolePhaseGroup N) :
    spatialProjection N (roleTranslatePlus N A x) = spatialProjection N x := by
  funext r
  simp [spatialProjection, roleTranslatePlus, roleTranslate, roleStep, r.property]

/-- Finite cyclic propagation, with the exact natural number of steps retained. -/
theorem axisInvariant_add_nsmul {N : ℕ} {α : Type*} {f : ArchiveRolePhaseGroup N → α}
    (h : AxisInvariantA N f) (k : ℕ) (x : ArchiveRolePhaseGroup N) :
    f (x + k • roleStep N A) = f x := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [succ_nsmul, ← add_assoc]
    exact (h (x + k • roleStep N A)).trans ih

theorem axisInvariant_eq_of_same_spatialProjection {N : ℕ} {α : Type*}
    {f : ArchiveRolePhaseGroup N → α} (h : AxisInvariantA N f)
    (x y : ArchiveRolePhaseGroup N) (hxy : spatialProjection N x = spatialProjection N y) :
    f x = f y := by
  let k := (y A - x A).val
  have hy : x + k • roleStep N A = y := by
    funext r
    by_cases hr : r = A
    · subst r
      change x A + k • (1 : ZMod (archiveFibers N)) = y A
      simp [k, nsmul_eq_mul]
    · have hv := congrFun hxy (⟨r,hr⟩ : SpatialRole)
      simpa [spatialProjection, roleStep, hr] using hv
  rw [← hy]
  exact (axisInvariant_add_nsmul h k x).symm

/-- Evaluation at A-phase zero is inverse to pullback; no structure on α is required. -/
def axisInvariantFunctionEquiv (N : ℕ) (α : Type*) :
    {f : ArchiveRolePhaseGroup N → α // AxisInvariantA N f} ≃
      (SpatialArchivePhaseGroup N → α) where
  toFun f y := f.val (spatialWithTime N 0 y)
  invFun g := ⟨fun x => g (spatialProjection N x), by
    intro x
    simp only [spatialProjection_translate_A]⟩
  left_inv f := by
    apply Subtype.ext
    funext x
    apply axisInvariant_eq_of_same_spatialProjection f.property
    simp
  right_inv g := by
    funext y
    simp

abbrev SpatialArchiveCochain (N : ℕ) := SpatialArchivePhaseGroup N → ArchiveFockState → ℝ

def axisInvariantCochainSubmodule (N : ℕ) : Submodule ℝ (ArchiveCochain N) where
  carrier := {ψ | ∀ x s, ψ (roleTranslatePlus N A x, s) = ψ (x,s)}
  zero_mem' := by intro x s; rfl
  add_mem' := by intro f g hf hg x s; simp only [Pi.add_apply, hf x s, hg x s]
  smul_mem' := by intro t f hf x s; simp only [Pi.smul_apply, hf x s]

def spatialCochainPullback (N : ℕ) (ψ : SpatialArchiveCochain N) : ArchiveCochain N :=
  fun p => ψ (spatialProjection N p.1) p.2

theorem spatialCochainPullback_invariant (N : ℕ) (ψ : SpatialArchiveCochain N) :
    spatialCochainPullback N ψ ∈ axisInvariantCochainSubmodule N := by
  intro x s
  simp [spatialCochainPullback]

/-- Linear factorization, retaining the full original exterior/Fock fibre. -/
def axisInvariantCochainEquivSpatial (N : ℕ) :
    axisInvariantCochainSubmodule N ≃ₗ[ℝ] SpatialArchiveCochain N where
  toFun ψ y s := ψ.val (spatialWithTime N 0 y,s)
  invFun ψ := ⟨spatialCochainPullback N ψ, spatialCochainPullback_invariant N ψ⟩
  left_inv ψ := by
    apply Subtype.ext
    funext p
    exact axisInvariant_eq_of_same_spatialProjection
      (f := fun x => ψ.val (x,p.2)) (fun x => ψ.property x p.2)
      (spatialWithTime N 0 (spatialProjection N p.1)) p.1 (by simp)
  right_inv ψ := by
    funext y s
    simp [spatialCochainPullback]
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

def spatialRoleStep (N : ℕ) (r : SpatialRole) : SpatialArchivePhaseGroup N :=
  fun s => if s = r then 1 else 0

def spatialTranslatePlus (N : ℕ) (r : SpatialRole) (x : SpatialArchivePhaseGroup N) :=
  x + spatialRoleStep N r

def spatialTranslateMinus (N : ℕ) (r : SpatialRole) (x : SpatialArchivePhaseGroup N) :=
  x - spatialRoleStep N r

@[simp] theorem spatialProjection_translatePlus (N : ℕ) (r : SpatialRole)
    (x : ArchiveRolePhaseGroup N) :
    spatialProjection N (roleTranslatePlus N r.val x) =
      spatialTranslatePlus N r (spatialProjection N x) := by
  funext s
  simp [spatialProjection, roleTranslatePlus, roleTranslate, roleStep,
    spatialTranslatePlus, spatialRoleStep, Subtype.ext_iff]

@[simp] theorem spatialProjection_translateMinus (N : ℕ) (r : SpatialRole)
    (x : ArchiveRolePhaseGroup N) :
    spatialProjection N (roleTranslateMinus N r.val x) =
      spatialTranslateMinus N r (spatialProjection N x) := by
  funext s
  simp [spatialProjection, roleTranslateMinus, roleTranslate, roleStep,
    spatialTranslateMinus, spatialRoleStep, Subtype.ext_iff, sub_eq_add_neg]

def spatialForwardDifference (N : ℕ) (r : SpatialRole)
    (f : SpatialArchivePhaseGroup N → ℝ) (x : SpatialArchivePhaseGroup N) : ℝ :=
  forwardDifferenceScale N * (f (spatialTranslatePlus N r x) - f x)

def spatialBackwardDifference (N : ℕ) (r : SpatialRole)
    (f : SpatialArchivePhaseGroup N → ℝ) (x : SpatialArchivePhaseGroup N) : ℝ :=
  forwardDifferenceScale N * (f x - f (spatialTranslateMinus N r x))

theorem spatial_forwardDifference_intertwine (N : ℕ) (r : SpatialRole)
    (f : SpatialArchivePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) :
    forwardDifference N r.val (fun y => f (spatialProjection N y)) x =
      spatialForwardDifference N r f (spatialProjection N x) := by
  simp [forwardDifference, spatialForwardDifference]

theorem spatial_backwardDifference_intertwine (N : ℕ) (r : SpatialRole)
    (f : SpatialArchivePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) :
    backwardDifference N r.val (fun y => f (spatialProjection N y)) x =
      spatialBackwardDifference N r f (spatialProjection N x) := by
  simp [backwardDifference, spatialBackwardDifference]

/-- The literal spatial difference Laplacian on the smaller site carrier. -/
def spatialArchiveLaplacian (N : ℕ) (f : SpatialArchivePhaseGroup N → ℝ)
    (x : SpatialArchivePhaseGroup N) : ℝ :=
  ∑ r : SpatialRole, forwardDifferenceScale N ^ 2 *
    (2 * f x - f (spatialTranslatePlus N r x) - f (spatialTranslateMinus N r x))

/-- The stencil is exactly minus backward-after-forward, including L=2. -/
theorem spatialArchiveLaplacian_eq_backward_forward (N : ℕ)
    (f : SpatialArchivePhaseGroup N → ℝ) (x : SpatialArchivePhaseGroup N) :
    spatialArchiveLaplacian N f x =
      ∑ r : SpatialRole, -spatialBackwardDifference N r (spatialForwardDifference N r f) x := by
  unfold spatialArchiveLaplacian
  apply Finset.sum_congr rfl
  intro r _
  have hcancel : spatialTranslatePlus N r (spatialTranslateMinus N r x) = x := by
    simp [spatialTranslatePlus, spatialTranslateMinus]
  simp only [spatialBackwardDifference, spatialForwardDifference, hcancel]
  ring

def spatialCochainLaplacian (N : ℕ) (ψ : SpatialArchiveCochain N) : SpatialArchiveCochain N :=
  fun x s => spatialArchiveLaplacian N (fun y => ψ y s) x

theorem scalarSpatialLaplacian_pullback (N : ℕ) (f : SpatialArchivePhaseGroup N → ℝ)
    (x : ArchiveRolePhaseGroup N) :
    scalarSpatialLaplacian N (fun y => f (spatialProjection N y)) x =
      spatialArchiveLaplacian N f (spatialProjection N x) := by
  unfold scalarSpatialLaplacian spatialArchiveLaplacian
  rw [← Equiv.sum_comp spatialAxisEquivRole]
  apply Finset.sum_congr rfl
  intro a _
  rw [← spatialAxisEquivRole_val a]
  simp only [spatialProjection_translatePlus, spatialProjection_translateMinus]

/-- Exact intertwiner with the already-owned Hodge square, with Fock a spectator. -/
theorem spatialCochainPullback_hodgeSquare (N : ℕ) (ψ : SpatialArchiveCochain N) :
    hodgeCarDirac N (hodgeCarDirac N (spatialCochainPullback N ψ)) =
      spatialCochainPullback N (spatialCochainLaplacian N ψ) := by
  funext p
  rw [hodgeCarDirac_sq_spatial_of_axisInvariant N _
    (spatialCochainPullback_invariant N ψ) p]
  exact scalarSpatialLaplacian_pullback N (fun y => ψ y p.2) p.1

theorem axisInvariant_hodgeSquare_invariant (N : ℕ) (ψ : axisInvariantCochainSubmodule N) :
    hodgeCarDirac N (hodgeCarDirac N ψ.val) ∈ axisInvariantCochainSubmodule N := by
  have hψ := (axisInvariantCochainEquivSpatial N).symm_apply_apply ψ
  have heq : spatialCochainPullback N (axisInvariantCochainEquivSpatial N ψ) = ψ.val :=
    congrArg Subtype.val hψ
  rw [← heq, spatialCochainPullback_hodgeSquare]
  exact spatialCochainPullback_invariant N _

/-- Restrict the existing square to its now-proved invariant subspace. -/
def axisInvariantHodgeSquare (N : ℕ) (ψ : axisInvariantCochainSubmodule N) :
    axisInvariantCochainSubmodule N :=
  ⟨hodgeCarDirac N (hodgeCarDirac N ψ.val), axisInvariant_hodgeSquare_invariant N ψ⟩

theorem axisInvariant_hodgeSquare_equiv_spatialLaplacian (N : ℕ)
    (ψ : axisInvariantCochainSubmodule N) :
    axisInvariantCochainEquivSpatial N (axisInvariantHodgeSquare N ψ) =
      spatialCochainLaplacian N (axisInvariantCochainEquivSpatial N ψ) := by
  have heq : spatialCochainPullback N (axisInvariantCochainEquivSpatial N ψ) = ψ.val :=
    congrArg Subtype.val ((axisInvariantCochainEquivSpatial N).symm_apply_apply ψ)
  funext y s
  change hodgeCarDirac N (hodgeCarDirac N ψ.val) (spatialWithTime N 0 y,s) = _
  rw [← heq, spatialCochainPullback_hodgeSquare]
  simp [spatialCochainPullback]

/-- Natural archive-delay count, as in the existing Feshbach path grammar. -/
abbrev HistoryIndex := ℕ
abbrev HistorySpatialCarrier (N : ℕ) := HistoryIndex × SpatialArchivePhaseGroup N

/-- Reads the existing history owner, without reading or assigning any A-phase. -/
def historySpatialReading (N : ℕ)
    (t : D0.Evolution.FeshbachSchurTimeDelayOwner.ArchivePathTerm)
    (y : SpatialArchivePhaseGroup N) : HistorySpatialCarrier N :=
  (D0.Evolution.FeshbachSchurTimeDelayOwner.tickIndex t, y)

theorem historySpatialReading_history (N k : ℕ) (y : SpatialArchivePhaseGroup N) :
    (historySpatialReading N (D0.Evolution.FeshbachSchurTimeDelayOwner.neumannTerm k) y).1 = k :=
  D0.Evolution.FeshbachSchurTimeDelayOwner.tick_index_eq_k k

theorem historySpatialReading_spatial (N : ℕ)
    (t : D0.Evolution.FeshbachSchurTimeDelayOwner.ArchivePathTerm)
    (y : SpatialArchivePhaseGroup N) : (historySpatialReading N t y).2 = y := rfl

/-- Unique positive INTERNAL label. Not a unique timelike vector or physical e₀. -/
theorem roleA_is_unique_positive_internal_role (r : Role) :
    roleSign (roleRoleSigEquiv r) = 1 ↔ r = A := by
  rcases r with ⟨a,b⟩
  fin_cases a <;> fin_cases b <;> norm_num [roleRoleSigEquiv, roleSign, A, B, C, D]

end
end D0.Geometry
