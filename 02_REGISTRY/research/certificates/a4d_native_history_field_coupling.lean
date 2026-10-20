import Mathlib.Tactic
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import D0.Foundation.EndogenousActionQuantum
import D0.Foundation.VerifiabilityNecessity
import D0.VNext2.ScenePathHistoryCanonicity
import D0.Geometry.ArchiveAffineExteriorLink
import D0.Geometry.A4DNilpotentAffineMatterLift
import D0.Geometry.ArchiveLaplacianRG

/-! A common-history countermodel for the G0 native-action interface.

The same fixed vertex-to-field readout, actual scene edge carrier, full path
composition law, and scalar-block cochain refinement admit two different
field-dependent edge prices.  The prices below are not selected D0 actions;
the theorem proves that primitive gap + history additivity + the already
owned matter refinement do not select one.  The readout and the full
coframe/link/memory refinement remain explicit inputs.
-/

namespace D0.Research.NativeHistoryFieldCoupling

open D0
open D0.Claims
open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.EndogenousActionQuantum
open D0.VNext2.ScenePathHistoryCanonicity
open D0.Geometry
open D0.Geometry.ArchiveRolePhaseProductCarrier
open scoped BigOperators
noncomputable section

abbrev Path := {p : List Vertex33 // IsSceneWalk p}
abbrev Edge := LevelOneSceneHistory

def edgePath (e : Edge) : Path :=
  ⟨[e.val.1,e.val.2],IsSceneWalk.cons _ _ [] e.property (IsSceneWalk.single _)⟩

def singlePath (v : Vertex33) : Path := ⟨[v],IsSceneWalk.single v⟩

def comp (p q : Path) (h : Composable p.val q.val) : Path :=
  ⟨composePath p.val q.val,isSceneWalk_compose p.property q.property h⟩

def pathSum (w : Vertex33 → Vertex33 → ℝ) : List Vertex33 → ℝ
  | u::v::rest => w u v + pathSum w (v::rest)
  | _ => 0

theorem rest_composable {u v : Vertex33} {w q : List Vertex33}
    (h : Composable (u::v::w) q) : Composable (v::w) q := by
  rcases h with ⟨x,hx,hy⟩
  refine ⟨x,?_,hy⟩
  simpa [pathFinish] using hx

theorem path_sum_composition (w : Vertex33 → Vertex33 → ℝ)
    {p q : List Vertex33} (hp : IsSceneWalk p) (h : Composable p q) :
    pathSum w (composePath p q)=pathSum w p+pathSum w q := by
  induction hp with
  | single v =>
    rcases h with ⟨x,hx,hy⟩
    have hxv : v=x := by simpa [pathFinish] using hx
    subst x
    cases q with
    | nil => simp [pathStart] at hy
    | cons a rest =>
      have ha : a=v := by simpa [pathStart] using hy
      subst a
      simp [composePath,pathSum]
  | cons u v rest hs hr ih =>
    have hi := ih (rest_composable h)
    change w u v + pathSum w ((v::rest)++q.tail) =
      (w u v + pathSum w (v::rest))+pathSum w q
    rw [show pathSum w ((v::rest)++q.tail)=pathSum w (v::rest)+pathSum w q from hi]
    ring

theorem path_sum_congr {w₁ w₂ : Vertex33 → Vertex33 → ℝ}
    (h : ∀ u v, w₁ u v = w₂ u v) (p : List Vertex33) :
    pathSum w₁ p = pathSum w₂ p := by
  induction p with
  | nil => rfl
  | cons u tail ih =>
    cases tail with
    | nil => rfl
    | cons v rest => simp [pathSum,h u v,ih]

structure AdditiveAction where
  value : Path → ℝ
  identity : ∀ v, value (singlePath v)=0
  additive : ∀ p q h, value (comp p q h)=value p+value q

abbrev NativeBackground (N : ℕ) :=
  {e : LocalCoframeField N // ∀ x, IsUnit (rawSolderMatrix N e x).det} ×
    LorentzAffineExteriorConnection N

def flatNativeBackground (N : ℕ) : NativeBackground N :=
  (⟨0,fun x => by
    have he : rawSolderMatrix N 0 x = roleLorentzMetric := by
      ext r a
      simp [rawSolderMatrix]
    rw [he]
    exact roleLorentzMetric_det_isUnit⟩,
    ⟨flatAffineConnection N,flatAffineExteriorConnection_isLorentz⟩)

def concreteEdge : Edge := ⟨(0,9),by decide⟩

/-- `B` retains whatever preparation/record-memory coordinates the consuming
owner carries; it is intentionally not quotiented or frozen here. -/
abbrev NativeJointPayload (N : ℕ) (B : Type) :=
  (NativeBackground N × B) × ArchiveCochain N

def sceneProtocol : VerificationProtocol where
  State := Vertex33
  Record := Vertex33
  Line := Bool
  Catalogue := Unit
  stateDecidableEq := inferInstance
  record := id
  compare := fun _ _ u v => decide (u ≠ v)

theorem scene_protocol_verified : VerificationContract sceneProtocol where
  state_nontrivial := inferInstanceAs (Nontrivial Vertex33)
  line_nontrivial := inferInstanceAs (Nontrivial Bool)
  catalogue_nonempty := inferInstanceAs (Nonempty Unit)
  correct := by intro _ _ _ _; rfl

def fieldVertexCost {N : ℕ} {B : Type}
    (J : NativeBackground N × B → ℝ) (m : ℝ)
    (E : ArchiveCochain N → ℝ)
    (read : Vertex33 → NativeJointPayload N B)
    (u v : Vertex33) : ℝ :=
  if SceneStep u v then
    1 + (J (read v).1 - m) + E (read v).2
  else 1

theorem fieldVertexCost_ge_one {N : ℕ} {B : Type}
    (J : NativeBackground N × B → ℝ) (m : ℝ)
    (E : ArchiveCochain N → ℝ)
    (read : Vertex33 → NativeJointPayload N B)
    (hJ : ∀ g, m ≤ J g) (hE : ∀ psi, 0 ≤ E psi)
    (u v : Vertex33) (h : SceneStep u v) :
    1 ≤ fieldVertexCost J m E read u v := by
  simp [fieldVertexCost,h]
  have hj := hJ (read v).1
  have he := hE (read v).2
  linarith

def fieldAction {N : ℕ} {B : Type}
    (J : NativeBackground N × B → ℝ) (m : ℝ)
    (E : ArchiveCochain N → ℝ)
    (read : Vertex33 → NativeJointPayload N B)
    (hJ : ∀ g, m ≤ J g) (hE : ∀ psi, 0 ≤ E psi) :
    ActionProtocol sceneProtocol where
  action u v := if u=v then 0 else fieldVertexCost J m E read u v
  action_refl u := by simp
  action_nontrivial u v huv := by
    by_cases heq : u=v
    · exact False.elim (huv heq)
    · simp only [if_neg heq]
      by_cases hs : SceneStep u v
      · simpa [fieldVertexCost,hs] using
          fieldVertexCost_ge_one J m E read hJ hE u v hs
      · simp [fieldVertexCost,hs]

def fieldHistoryPrice {N : ℕ} {B : Type}
    (J : NativeBackground N × B → ℝ) (m : ℝ)
    (E : ArchiveCochain N → ℝ)
    (read : Vertex33 → NativeJointPayload N B) : AdditiveAction where
  value p := pathSum (fieldVertexCost J m E read) p.val
  identity _v := rfl
  additive p _q h := path_sum_composition _ p.property h

theorem scene_edge_distinct (e : Edge) : e.val.1 ≠ e.val.2 := by
  intro h
  have he := e.property
  simp [SceneStep,Adj31,h] at he

theorem field_action_edge {N : ℕ} {B : Type}
    (J : NativeBackground N × B → ℝ) (m : ℝ)
    (E : ArchiveCochain N → ℝ)
    (read : Vertex33 → NativeJointPayload N B)
    (hJ : ∀ g, m ≤ J g) (hE : ∀ psi, 0 ≤ E psi) (e : Edge) :
    (fieldAction J m E read hJ hE).action e.val.1 e.val.2 =
      1 + (J (read e.val.2).1 - m) + E (read e.val.2).2 := by
  change (if e.val.1=e.val.2 then 0 else
    fieldVertexCost J m E read e.val.1 e.val.2) = _
  rw [if_neg (scene_edge_distinct e)]
  simp [fieldVertexCost,e.property]

theorem field_history_edge {N : ℕ} {B : Type}
    (J : NativeBackground N × B → ℝ) (m : ℝ)
    (E : ArchiveCochain N → ℝ)
    (read : Vertex33 → NativeJointPayload N B) (e : Edge) :
    (fieldHistoryPrice J m E read).value (edgePath e) =
      1 + (J (read e.val.2).1 - m) + E (read e.val.2).2 := by
  simp [fieldHistoryPrice,pathSum,edgePath,fieldVertexCost,e.property]

theorem edge_action_matches_history {N : ℕ} {B : Type}
    (J : NativeBackground N × B → ℝ) (m : ℝ)
    (E : ArchiveCochain N → ℝ)
    (read : Vertex33 → NativeJointPayload N B)
    (hJ : ∀ g, m ≤ J g) (hE : ∀ psi, 0 ≤ E psi) (e : Edge) :
    (fieldAction J m E read hJ hE).action e.val.1 e.val.2 =
      (fieldHistoryPrice J m E read).value (edgePath e) := by
  rw [field_action_edge J m E read hJ hE e,field_history_edge]

def refineReadout {N : ℕ} {B : Type}
    (RG : NativeBackground N × B → NativeBackground (N+1) × B)
    (R : ArchiveCochain N → ArchiveCochain (N+1))
    (read : Vertex33 → NativeJointPayload N B) :
    Vertex33 → NativeJointPayload (N+1) B :=
  fun v => (RG (read v).1,R (read v).2)

theorem fieldVertexCost_refines {N : ℕ} {B : Type}
    (J₀ : NativeBackground N × B → ℝ)
    (J₁ : NativeBackground (N+1) × B → ℝ) (m : ℝ)
    (E₀ : ArchiveCochain N → ℝ)
    (E₁ : ArchiveCochain (N+1) → ℝ)
    (read : Vertex33 → NativeJointPayload N B)
    (RG : NativeBackground N × B → NativeBackground (N+1) × B)
    (R : ArchiveCochain N → ArchiveCochain (N+1))
    (hJ : ∀ g, J₁ (RG g)=J₀ g)
    (hE : ∀ psi, E₁ (R psi)=E₀ psi)
    (u v : Vertex33) :
    fieldVertexCost J₁ m E₁ (refineReadout RG R read) u v =
      fieldVertexCost J₀ m E₀ read u v := by
  by_cases hs : SceneStep u v
  · simp [fieldVertexCost,refineReadout,hs,hJ,hE]
  · simp [fieldVertexCost,hs]

theorem fieldHistoryPrice_refines {N : ℕ} {B : Type}
    (J₀ : NativeBackground N × B → ℝ)
    (J₁ : NativeBackground (N+1) × B → ℝ) (m : ℝ)
    (E₀ : ArchiveCochain N → ℝ)
    (E₁ : ArchiveCochain (N+1) → ℝ)
    (read : Vertex33 → NativeJointPayload N B)
    (RG : NativeBackground N × B → NativeBackground (N+1) × B)
    (R : ArchiveCochain N → ArchiveCochain (N+1))
    (hJ : ∀ g, J₁ (RG g)=J₀ g)
    (hE : ∀ psi, E₁ (R psi)=E₀ psi) (p : Path) :
    (fieldHistoryPrice J₁ m E₁ (refineReadout RG R read)).value p =
      (fieldHistoryPrice J₀ m E₀ read).value p := by
  unfold fieldHistoryPrice
  exact path_sum_congr
    (fun u v => fieldVertexCost_refines J₀ J₁ m E₀ E₁ read RG R hJ hE u v)
    p.val

def anchor (N : ℕ) (k : Fin 2) : ArchiveRolePhasePoint N :=
  fun r => if r = (0,0) then ⟨k.val, by have := k.isLt; unfold archiveFibers; omega⟩ else 0

def anchorSite (N : ℕ) (k : Fin 2) : ArchiveRolePhaseGroup N :=
  archiveRolePhasePointGroupEquiv N (anchor N k)

theorem anchor_injective (N : ℕ) : Function.Injective (anchor N) := by
  intro k l h
  apply Fin.ext
  have hv := congrArg (fun p => (p (0,0)).val) h
  simpa [anchor] using hv

theorem anchor_site_injective (N : ℕ) : Function.Injective (anchorSite N) := by
  intro k l h
  exact anchor_injective N ((archiveRolePhasePointGroupEquiv N).injective h)

def sigma (N : ℕ) (psi : ArchiveCochain N) (k : Fin 2) : ℝ :=
  scalarComponent N psi (anchorSite N k)

theorem sigma_zero (N : ℕ) (k : Fin 2) : sigma N 0 k = 0 := by
  simp [sigma,scalarComponent]

theorem sigma_add (N : ℕ) (psi phi : ArchiveCochain N) (k : Fin 2) :
    sigma N (psi + phi) k = sigma N psi k + sigma N phi k := by
  simp [sigma,scalarComponent]

theorem sigma_smul (N : ℕ) (a : ℝ) (psi : ArchiveCochain N) (k : Fin 2) :
    sigma N (a • psi) k = a * sigma N psi k := by
  simp [sigma,scalarComponent,smul_eq_mul]

def anchorDirection (N : ℕ) (k : Fin 2) : ArchiveCochain N :=
  scalarCochain N (fun x => if x = anchorSite N k then 1 else 0)

theorem anchor_direction_readout (N : ℕ) (k j : Fin 2) :
    sigma N (anchorDirection N k) j = if j = k then 1 else 0 := by
  classical
  simp [sigma,anchorDirection,scalarCochain,scalarComponent,
    (anchor_site_injective N).eq_iff]

theorem anchorDirection_ne_zero (N : ℕ) (k : Fin 2) :
    anchorDirection N k ≠ 0 := by
  intro h
  have hv : sigma N (anchorDirection N k) k = sigma N 0 k := by rw [h]
  rw [anchor_direction_readout,sigma_zero] at hv
  simp at hv

def oneAnchorEnergy (N : ℕ) (psi : ArchiveCochain N) : ℝ := sigma N psi 0 ^ 2
def twoAnchorEnergy (N : ℕ) (psi : ArchiveCochain N) : ℝ :=
  sigma N psi 0 ^ 2 + sigma N psi 1 ^ 2

/-- Two full-cochain prices with the same value at the zero matter state.
The first is stationary in the second anchor direction; the second has a
nonzero response there.  Both are globally nonnegative. -/
def matchedBaselineQuadraticEnergy (N : ℕ) (psi : ArchiveCochain N) : ℝ :=
  1 + sigma N psi 0 ^ 2

def matchedBaselineExponentialEnergy (N : ℕ) (psi : ArchiveCochain N) : ℝ :=
  Real.exp (sigma N psi 1)

theorem energy_nonnegative (N : ℕ) (psi : ArchiveCochain N) :
    0 ≤ oneAnchorEnergy N psi ∧ 0 ≤ twoAnchorEnergy N psi := by
  constructor
  · exact sq_nonneg _
  · exact add_nonneg (sq_nonneg _) (sq_nonneg _)

theorem matched_baseline_energies_nonnegative (N : ℕ) (psi : ArchiveCochain N) :
    0 ≤ matchedBaselineQuadraticEnergy N psi ∧
      0 ≤ matchedBaselineExponentialEnergy N psi := by
  constructor
  · exact add_nonneg (by norm_num) (sq_nonneg _)
  · exact le_of_lt (Real.exp_pos _)

def matched_baseline_action_protocols {N : ℕ} {B : Type}
    (J : NativeBackground N × B → ℝ) (m : ℝ)
    (read : Vertex33 → NativeJointPayload N B)
    (hJ : ∀ g, m ≤ J g) : ActionProtocol sceneProtocol × ActionProtocol sceneProtocol := by
  have hQ : ∀ psi : ArchiveCochain N,
      0 ≤ matchedBaselineQuadraticEnergy N psi := by
    intro psi
    exact (matched_baseline_energies_nonnegative N psi).1
  have hE : ∀ psi : ArchiveCochain N,
      0 ≤ matchedBaselineExponentialEnergy N psi := by
    intro psi
    exact (matched_baseline_energies_nonnegative N psi).2
  exact ⟨fieldAction J m (matchedBaselineQuadraticEnergy N) read hJ hQ,
    fieldAction J m (matchedBaselineExponentialEnergy N) read hJ hE⟩

def observableFirstVariation (theta sigma dsigma : ℝ) : ℝ :=
  2 * theta * sigma * dsigma

theorem genuine_observable_derivative (theta sigma dsigma : ℝ) :
    HasDerivAt (fun t : ℝ => theta * (sigma + t * dsigma) ^ 2)
      (observableFirstVariation theta sigma dsigma) 0 := by
  have h := (((hasDerivAt_const (0 : ℝ) sigma).add
    ((hasDerivAt_id (0 : ℝ)).mul_const dsigma)).pow 2).const_mul theta
  convert h using 1
  simp [observableFirstVariation]
  ring

theorem full_cochain_one_derivative (N : ℕ) (psi direction : ArchiveCochain N) :
    HasDerivAt (fun t : ℝ => oneAnchorEnergy N (psi + t • direction))
      (2 * sigma N psi 0 * sigma N direction 0) 0 := by
  convert genuine_observable_derivative 1 (sigma N psi 0) (sigma N direction 0) using 1
  · funext t
    simp [oneAnchorEnergy,sigma,scalarComponent,Pi.add_apply,Pi.smul_apply,smul_eq_mul]
  · simp [observableFirstVariation]

theorem full_cochain_two_derivative (N : ℕ) (psi direction : ArchiveCochain N) :
    HasDerivAt (fun t : ℝ => twoAnchorEnergy N (psi + t • direction))
      (2 * sigma N psi 0 * sigma N direction 0 +
       2 * sigma N psi 1 * sigma N direction 1) 0 := by
  have h0 := full_cochain_one_derivative N psi direction
  have h1 : HasDerivAt (fun t : ℝ => sigma N (psi + t • direction) 1 ^ 2)
      (2 * sigma N psi 1 * sigma N direction 1) 0 := by
    convert genuine_observable_derivative 1 (sigma N psi 1) (sigma N direction 1) using 1
    · funext t
      simp [sigma,scalarComponent,Pi.add_apply,Pi.smul_apply,smul_eq_mul]
    · simp [observableFirstVariation]
  simpa only [twoAnchorEnergy,oneAnchorEnergy] using h0.add h1

theorem one_anchor_matter_jet (N : ℕ) :
    HasDerivAt
      (fun t : ℝ => oneAnchorEnergy N
        (anchorDirection N 1 + t • anchorDirection N 1)) 0 0 := by
  have h := full_cochain_one_derivative N (anchorDirection N 1) (anchorDirection N 1)
  simpa [anchor_direction_readout] using h

theorem two_anchor_matter_jet (N : ℕ) :
    HasDerivAt
      (fun t : ℝ => twoAnchorEnergy N
        (anchorDirection N 1 + t • anchorDirection N 1)) 2 0 := by
  have h := full_cochain_two_derivative N (anchorDirection N 1) (anchorDirection N 1)
  simpa [anchor_direction_readout] using h

def pointProjection (N : ℕ) (p : ArchiveRolePhasePoint (N+1)) : ArchiveRolePhasePoint N :=
  fun r => archiveRGPhaseProjection N (p r)

theorem literal_projection_preserves_anchors (N : ℕ) (k : Fin 2) :
    pointProjection N (anchor (N+1) k) = anchor N k := by
  funext r
  apply Fin.ext
  have hk : k.val < archiveFibers N := by
    have := k.isLt
    unfold archiveFibers
    omega
  by_cases hr : r = (0,0)
  · simp [pointProjection,anchor,hr,archiveRGPhaseProjection,Nat.mod_eq_of_lt hk]
  · simp [pointProjection,anchor,hr,archiveRGPhaseProjection]

def groupProjection (N : ℕ) (x : ArchiveRolePhaseGroup (N+1)) : ArchiveRolePhaseGroup N :=
  archiveRolePhasePointGroupEquiv N
    (pointProjection N ((archiveRolePhasePointGroupEquiv (N+1)).symm x))

theorem group_projection_preserves_anchors (N : ℕ) (k : Fin 2) :
    groupProjection N (anchorSite (N+1) k) = anchorSite N k := by
  simp [groupProjection,anchorSite,literal_projection_preserves_anchors]

def ScalarRefinementCompatible (N : ℕ)
    (R : ArchiveCochain N → ArchiveCochain (N+1)) : Prop :=
  ∀ psi x, scalarComponent (N+1) (R psi) x =
    scalarComponent N psi (groupProjection N x)

theorem actual_scalar_block_preserves_sigma (N : ℕ)
    (R : ArchiveCochain N → ArchiveCochain (N+1))
    (hR : ScalarRefinementCompatible N R) (psi : ArchiveCochain N) (k : Fin 2) :
    sigma (N+1) (R psi) k = sigma N psi k := by
  unfold sigma
  rw [hR psi,group_projection_preserves_anchors]

theorem native_scalar_block_preserves_energies (N : ℕ)
    (R : ArchiveCochain N → ArchiveCochain (N+1))
    (hR : ScalarRefinementCompatible N R) (psi : ArchiveCochain N) :
    oneAnchorEnergy (N+1) (R psi) = oneAnchorEnergy N psi ∧
      twoAnchorEnergy (N+1) (R psi) = twoAnchorEnergy N psi := by
  have h0 := actual_scalar_block_preserves_sigma N R hR psi 0
  have h1 := actual_scalar_block_preserves_sigma N R hR psi 1
  simp [oneAnchorEnergy,twoAnchorEnergy,h0,h1]

theorem native_scalar_block_preserves_matched_baseline_energies (N : ℕ)
    (R : ArchiveCochain N → ArchiveCochain (N+1))
    (hR : ScalarRefinementCompatible N R) (psi : ArchiveCochain N) :
    matchedBaselineQuadraticEnergy (N+1) (R psi) =
        matchedBaselineQuadraticEnergy N psi ∧
      matchedBaselineExponentialEnergy (N+1) (R psi) =
        matchedBaselineExponentialEnergy N psi := by
  have h0 := actual_scalar_block_preserves_sigma N R hR psi 0
  have h1 := actual_scalar_block_preserves_sigma N R hR psi 1
  simp [matchedBaselineQuadraticEnergy,matchedBaselineExponentialEnergy,h0,h1]

theorem one_anchor_history_price_refines {N : ℕ} {B : Type}
    (J₀ : NativeBackground N × B → ℝ)
    (J₁ : NativeBackground (N+1) × B → ℝ) (m : ℝ)
    (read : Vertex33 → NativeJointPayload N B)
    (RG : NativeBackground N × B → NativeBackground (N+1) × B)
    (R : ArchiveCochain N → ArchiveCochain (N+1))
    (hJ : ∀ g, J₁ (RG g)=J₀ g)
    (hR : ScalarRefinementCompatible N R) (p : Path) :
    (fieldHistoryPrice J₁ m (oneAnchorEnergy (N+1)) (refineReadout RG R read)).value p =
      (fieldHistoryPrice J₀ m (oneAnchorEnergy N) read).value p := by
  apply fieldHistoryPrice_refines J₀ J₁ m (oneAnchorEnergy N)
    (oneAnchorEnergy (N+1)) read RG R hJ
  intro psi
  exact (native_scalar_block_preserves_energies N R hR psi).1

theorem two_anchor_history_price_refines {N : ℕ} {B : Type}
    (J₀ : NativeBackground N × B → ℝ)
    (J₁ : NativeBackground (N+1) × B → ℝ) (m : ℝ)
    (read : Vertex33 → NativeJointPayload N B)
    (RG : NativeBackground N × B → NativeBackground (N+1) × B)
    (R : ArchiveCochain N → ArchiveCochain (N+1))
    (hJ : ∀ g, J₁ (RG g)=J₀ g)
    (hR : ScalarRefinementCompatible N R) (p : Path) :
    (fieldHistoryPrice J₁ m (twoAnchorEnergy (N+1)) (refineReadout RG R read)).value p =
      (fieldHistoryPrice J₀ m (twoAnchorEnergy N) read).value p := by
  apply fieldHistoryPrice_refines J₀ J₁ m (twoAnchorEnergy N)
    (twoAnchorEnergy (N+1)) read RG R hJ
  intro psi
  exact (native_scalar_block_preserves_energies N R hR psi).2

def movingReadout {N : ℕ} {B : Type} (e : Edge)
    (g : NativeBackground N × B) (psi direction : ArchiveCochain N) (t : ℝ) :
    Vertex33 → NativeJointPayload N B :=
  fun v => (g,if v=e.val.2 then psi+t • direction else 0)

theorem field_history_edge_along_matter_curve {N : ℕ} {B : Type}
    (J : NativeBackground N × B → ℝ) (m : ℝ)
    (E : ArchiveCochain N → ℝ)
    (e : Edge) (g : NativeBackground N × B)
    (psi direction : ArchiveCochain N) (t : ℝ) :
    (fieldHistoryPrice J m E (movingReadout e g psi direction t)).value (edgePath e) =
      1 + (J g - m) + E (psi + t • direction) := by
  rw [field_history_edge]
  simp [movingReadout]

theorem common_history_one_response {N : ℕ} {B : Type}
    (J : NativeBackground N × B → ℝ) (m : ℝ)
    (e : Edge) (g : NativeBackground N × B) :
    HasDerivAt
      (fun t : ℝ => (fieldHistoryPrice J m (oneAnchorEnergy N)
        (movingReadout e g (anchorDirection N 1) (anchorDirection N 1) t)).value
        (edgePath e)) 0 0 := by
  have hprice :
      (fun t : ℝ => (fieldHistoryPrice J m (oneAnchorEnergy N)
        (movingReadout e g (anchorDirection N 1) (anchorDirection N 1) t)).value
        (edgePath e)) =
      (fun t : ℝ => (1+(J g-m)) +
        oneAnchorEnergy N (anchorDirection N 1 + t • anchorDirection N 1)) := by
    funext t
    exact field_history_edge_along_matter_curve J m (oneAnchorEnergy N) e g
      (anchorDirection N 1) (anchorDirection N 1) t
  rw [hprice]
  simpa only [Pi.add_apply,zero_add] using
    (hasDerivAt_const 0 (1+(J g-m))).add (one_anchor_matter_jet N)

theorem common_history_two_response {N : ℕ} {B : Type}
    (J : NativeBackground N × B → ℝ) (m : ℝ)
    (e : Edge) (g : NativeBackground N × B) :
    HasDerivAt
      (fun t : ℝ => (fieldHistoryPrice J m (twoAnchorEnergy N)
        (movingReadout e g (anchorDirection N 1) (anchorDirection N 1) t)).value
        (edgePath e)) 2 0 := by
  have hprice :
      (fun t : ℝ => (fieldHistoryPrice J m (twoAnchorEnergy N)
        (movingReadout e g (anchorDirection N 1) (anchorDirection N 1) t)).value
        (edgePath e)) =
      (fun t : ℝ => (1+(J g-m)) +
        twoAnchorEnergy N (anchorDirection N 1 + t • anchorDirection N 1)) := by
    funext t
    exact field_history_edge_along_matter_curve J m (twoAnchorEnergy N) e g
      (anchorDirection N 1) (anchorDirection N 1) t
  rw [hprice]
  simpa only [Pi.add_apply,zero_add] using
    (hasDerivAt_const 0 (1+(J g-m))).add (two_anchor_matter_jet N)

theorem same_full_history_different_matter_response {N : ℕ} {B : Type}
    (J : NativeBackground N × B → ℝ) (m : ℝ)
    (e : Edge) (g : NativeBackground N × B) :
    deriv (fun t : ℝ => (fieldHistoryPrice J m (oneAnchorEnergy N)
      (movingReadout e g (anchorDirection N 1) (anchorDirection N 1) t)).value
      (edgePath e)) 0 = 0 ∧
    deriv (fun t : ℝ => (fieldHistoryPrice J m (twoAnchorEnergy N)
      (movingReadout e g (anchorDirection N 1) (anchorDirection N 1) t)).value
      (edgePath e)) 0 = 2 := by
  exact ⟨(common_history_one_response J m e g).deriv,
    (common_history_two_response J m e g).deriv⟩

theorem concrete_nonempty_history_response (N : ℕ) :
    deriv (fun t : ℝ => (fieldHistoryPrice
      (fun _ : NativeBackground N × ArchiveCochain N => 0)
      0 (oneAnchorEnergy N)
      (movingReadout concreteEdge (flatNativeBackground N,anchorDirection N 0)
        (anchorDirection N 1) (anchorDirection N 1) t)).value
      (edgePath concreteEdge)) 0 = 0 ∧
    deriv (fun t : ℝ => (fieldHistoryPrice
      (fun _ : NativeBackground N × ArchiveCochain N => 0)
      0 (twoAnchorEnergy N)
      (movingReadout concreteEdge (flatNativeBackground N,anchorDirection N 0)
        (anchorDirection N 1) (anchorDirection N 1) t)).value
      (edgePath concreteEdge)) 0 = 2 := by
  exact same_full_history_different_matter_response (fun _ => 0) 0 concreteEdge
    (flatNativeBackground N,anchorDirection N 0)

theorem matched_baseline_history_price_refines {N : ℕ} {B : Type}
    (J₀ : NativeBackground N × B → ℝ)
    (J₁ : NativeBackground (N+1) × B → ℝ) (m : ℝ)
    (read : Vertex33 → NativeJointPayload N B)
    (RG : NativeBackground N × B → NativeBackground (N+1) × B)
    (R : ArchiveCochain N → ArchiveCochain (N+1))
    (hJ : ∀ g, J₁ (RG g)=J₀ g)
    (hR : ScalarRefinementCompatible N R) (p : Path) :
    (fieldHistoryPrice J₁ m (matchedBaselineQuadraticEnergy (N+1))
      (refineReadout RG R read)).value p =
        (fieldHistoryPrice J₀ m (matchedBaselineQuadraticEnergy N) read).value p ∧
    (fieldHistoryPrice J₁ m (matchedBaselineExponentialEnergy (N+1))
      (refineReadout RG R read)).value p =
        (fieldHistoryPrice J₀ m (matchedBaselineExponentialEnergy N) read).value p := by
  constructor
  · apply fieldHistoryPrice_refines J₀ J₁ m
      (matchedBaselineQuadraticEnergy N) (matchedBaselineQuadraticEnergy (N+1))
      read RG R hJ
    intro psi
    exact (native_scalar_block_preserves_matched_baseline_energies N R hR psi).1
  · apply fieldHistoryPrice_refines J₀ J₁ m
      (matchedBaselineExponentialEnergy N) (matchedBaselineExponentialEnergy (N+1))
      read RG R hJ
    intro psi
    exact (native_scalar_block_preserves_matched_baseline_energies N R hR psi).2

theorem matched_baseline_same_value_different_response {N : ℕ} {B : Type}
    (J : NativeBackground N × B → ℝ) (m : ℝ)
    (e : Edge) (g : NativeBackground N × B) :
    (fieldHistoryPrice J m
      (matchedBaselineQuadraticEnergy N)
      (movingReadout e g 0 (anchorDirection N 1) 0)).value (edgePath e) =
      (fieldHistoryPrice J m
        (matchedBaselineExponentialEnergy N)
        (movingReadout e g 0 (anchorDirection N 1) 0)).value (edgePath e) ∧
    deriv (fun t : ℝ => (fieldHistoryPrice
      J m
      (matchedBaselineQuadraticEnergy N)
      (movingReadout e g 0 (anchorDirection N 1) t)).value (edgePath e)) 0 = 0 ∧
    deriv (fun t : ℝ => (fieldHistoryPrice
      J m
      (matchedBaselineExponentialEnergy N)
      (movingReadout e g 0 (anchorDirection N 1) t)).value (edgePath e)) 0 = 1 := by
  let readQ := fun t : ℝ => movingReadout e g 0 (anchorDirection N 1) t
  have hQ : (fun t : ℝ => (fieldHistoryPrice
      J m
      (matchedBaselineQuadraticEnergy N) (readQ t)).value
        (edgePath e)) = fun _ => 2 + (J g - m) := by
    funext t
    rw [field_history_edge_along_matter_curve]
    simp only [matchedBaselineQuadraticEnergy, zero_add]
    rw [sigma_smul, anchor_direction_readout]
    simp [show (0 : Fin 2) ≠ 1 by decide]
    ring
  have hE : (fun t : ℝ => (fieldHistoryPrice
      J m
      (matchedBaselineExponentialEnergy N) (readQ t)).value
        (edgePath e)) = fun t => (1 + (J g - m)) + Real.exp t := by
    funext t
    rw [field_history_edge_along_matter_curve]
    simp only [matchedBaselineExponentialEnergy, zero_add]
    rw [sigma_smul, anchor_direction_readout]
    simp
  have hQderiv : HasDerivAt
      (fun t : ℝ => (fieldHistoryPrice
        J m
        (matchedBaselineQuadraticEnergy N) (readQ t)).value
          (edgePath e)) 0 0 := by
    rw [hQ]
    exact hasDerivAt_const (0 : ℝ) (2 + (J g - m))
  have hEderiv : HasDerivAt
      (fun t : ℝ => (fieldHistoryPrice
        J m
        (matchedBaselineExponentialEnergy N) (readQ t)).value
          (edgePath e)) 1 0 := by
    rw [hE]
    have h := (Real.hasDerivAt_exp 0).const_add (1 + (J g - m))
    simpa using h
  refine ⟨?_, hQderiv.deriv, hEderiv.deriv⟩
  change (fieldHistoryPrice J m (matchedBaselineQuadraticEnergy N)
      (readQ 0)).value (edgePath e) =
    (fieldHistoryPrice J m (matchedBaselineExponentialEnergy N)
      (readQ 0)).value (edgePath e)
  rw [congrFun hQ 0, congrFun hE 0]
  simp [Real.exp_zero]
  ring

theorem concrete_nonzero_memory_same_value_different_response (N : ℕ) :
    (fieldHistoryPrice (fun _ : NativeBackground N × ArchiveCochain N => 0) 0
      (matchedBaselineQuadraticEnergy N)
      (movingReadout concreteEdge (flatNativeBackground N,anchorDirection N 0) 0
        (anchorDirection N 1) 0)).value (edgePath concreteEdge) =
      (fieldHistoryPrice (fun _ : NativeBackground N × ArchiveCochain N => 0) 0
        (matchedBaselineExponentialEnergy N)
        (movingReadout concreteEdge (flatNativeBackground N,anchorDirection N 0) 0
          (anchorDirection N 1) 0)).value (edgePath concreteEdge) ∧
    deriv (fun t : ℝ => (fieldHistoryPrice
      (fun _ : NativeBackground N × ArchiveCochain N => 0) 0
      (matchedBaselineQuadraticEnergy N)
      (movingReadout concreteEdge (flatNativeBackground N,anchorDirection N 0) 0
        (anchorDirection N 1) t)).value (edgePath concreteEdge)) 0 = 0 ∧
    deriv (fun t : ℝ => (fieldHistoryPrice
      (fun _ : NativeBackground N × ArchiveCochain N => 0) 0
      (matchedBaselineExponentialEnergy N)
      (movingReadout concreteEdge (flatNativeBackground N,anchorDirection N 0) 0
        (anchorDirection N 1) t)).value (edgePath concreteEdge)) 0 = 1 := by
  exact matched_baseline_same_value_different_response
    (fun _ : NativeBackground N × ArchiveCochain N => 0) 0 concreteEdge
    (flatNativeBackground N,anchorDirection N 0)

#check scene_protocol_verified
#check fieldAction
#check fieldHistoryPrice
#check fieldHistoryPrice_refines
#check one_anchor_history_price_refines
#check two_anchor_history_price_refines
#check same_full_history_different_matter_response
#check concrete_nonempty_history_response
#check anchorDirection_ne_zero
#check matched_baseline_action_protocols
#check native_scalar_block_preserves_matched_baseline_energies
#check matched_baseline_history_price_refines
#check matched_baseline_same_value_different_response
#check concrete_nonzero_memory_same_value_different_response

#print axioms scene_protocol_verified
#print axioms path_sum_composition
#print axioms fieldAction
#print axioms fieldHistoryPrice
#print axioms fieldHistoryPrice_refines
#print axioms one_anchor_history_price_refines
#print axioms two_anchor_history_price_refines
#print axioms same_full_history_different_matter_response
#print axioms concrete_nonempty_history_response
#print axioms anchorDirection_ne_zero
#print axioms matched_baseline_action_protocols
#print axioms native_scalar_block_preserves_matched_baseline_energies
#print axioms matched_baseline_history_price_refines
#print axioms matched_baseline_same_value_different_response
#print axioms concrete_nonzero_memory_same_value_different_response

end
end D0.Research.NativeHistoryFieldCoupling
