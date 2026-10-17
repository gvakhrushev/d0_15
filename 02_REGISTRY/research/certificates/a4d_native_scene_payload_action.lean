import Mathlib.Tactic
import D0.Claims.Signature31Split
import D0.SelfReading.TypedIncidenceCarriers
import D0.VNext2.SceneNativeRefinementClassification
import D0.VNext2.ScenePathHistoryCanonicity
import D0.Foundation.EndogenousActionQuantum
import D0.Geometry.ArchiveAffineExteriorLink
import D0.Geometry.A4DNilpotentAffineMatterLift
import D0.Geometry.ArchiveLaplacianRG
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Pow

/-!
# Joint scene-history / native-payload action fiber

This capsule composes the literal D0 scene-walk carrier with the full raw
coframe, Lorentz-affine link and all-grade archive-cochain payload. It proves
the exact observable edge-cost family permitted by the existing verification
`ActionProtocol` and path additivity, and exhibits two refinement-compatible
members with distinct full-matter response. This is a theorem about that
typed interface. It does not prove that this product protocol is the admitted
physical D0 preparation or derive its action from the native history owner.
-/

namespace D0.Research.NativeScenePayloadAction

open D0.Claims
open D0.VNext2.ScenePathHistoryCanonicity
open D0.SelfReading.TypedIncidenceCarriers
open D0.VNext2.SceneNativeRefinementClassification
open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.EndogenousActionQuantum
open D0.Geometry
open D0.Geometry.ArchiveRolePhaseProductCarrier
noncomputable section

abbrev NativeBackground (N : ℕ) :=
  {e : LocalCoframeField N // ∀ x, IsUnit (rawSolderMatrix N e x).det} ×
    LorentzAffineExteriorConnection N

abbrev NativePayload (N : ℕ) := NativeBackground N × ArchiveCochain N

def flatNativeBackground (N : ℕ) : NativeBackground N :=
  (⟨0, fun x => by
    have he : rawSolderMatrix N 0 x = roleLorentzMetric := by
      ext r a
      simp [rawSolderMatrix]
    rw [he]
    exact roleLorentzMetric_det_isUnit⟩,
    ⟨flatAffineConnection N, flatAffineExteriorConnection_isLorentz⟩)

/-- The product protocol retains the literal scene vertex and every native
coframe, link and matter coordinate in its state and record. -/
def scenePayloadProtocol (N : ℕ) : VerificationProtocol where
  State := Vertex33 × NativePayload N
  Record := Vertex33 × NativePayload N
  Line := Bool
  Catalogue := Unit
  stateDecidableEq := Classical.decEq _
  record := id
  compare := by
    classical
    exact fun _ _ s t => decide (s ≠ t)

theorem scene_payload_verification_contract (N : ℕ) :
    VerificationContract (scenePayloadProtocol N) where
  state_nontrivial := ⟨⟨(0, (flatNativeBackground N, 0)),
    (1, (flatNativeBackground N, 0)), by
      intro h
      have hv := congrArg Prod.fst h
      norm_num at hv⟩⟩
  line_nontrivial := inferInstanceAs (Nontrivial Bool)
  catalogue_nonempty := inferInstanceAs (Nonempty Unit)
  correct := by intro _ _ _ _; simp [scenePayloadProtocol]

abbrev ScenePath := {p : List Vertex33 // IsSceneWalk p}
abbrev SceneEdge := LevelOneSceneHistory

def edgePath (e : SceneEdge) : ScenePath :=
  ⟨[e.val.1, e.val.2],
    IsSceneWalk.cons _ _ [] e.property (IsSceneWalk.single _)⟩

def singlePath (v : Vertex33) : ScenePath := ⟨[v], IsSceneWalk.single v⟩

theorem scene_edge_distinct (e : SceneEdge) : e.val.1 ≠ e.val.2 := by
  intro h
  have he := e.property
  simp [SceneStep, Adj31, h] at he

structure AdditiveHistoryAction where
  value : ScenePath → ℝ
  identity : ∀ v, value (singlePath v) = 0
  additive : ∀ p q h, value ⟨composePath p.val q.val,
    isSceneWalk_compose p.property q.property h⟩ = value p + value q

def pathSum (w : Vertex33 → Vertex33 → ℝ) : List Vertex33 → ℝ
  | u :: v :: rest => w u v + pathSum w (v :: rest)
  | _ => 0

def edgeReading (w : SceneEdge → ℝ) (u v : Vertex33) : ℝ :=
  if h : SceneStep u v then w ⟨(u, v), h⟩ else 0

theorem rest_composable {u v : Vertex33} {w q : List Vertex33}
    (h : Composable (u :: v :: w) q) : Composable (v :: w) q := by
  rcases h with ⟨x, hx, hy⟩
  refine ⟨x, ?_, hy⟩
  simpa [pathFinish] using hx

theorem path_sum_composition (w : Vertex33 → Vertex33 → ℝ)
    {p q : List Vertex33} (hp : IsSceneWalk p) (h : Composable p q) :
    pathSum w (composePath p q) = pathSum w p + pathSum w q := by
  induction hp with
  | single v =>
    rcases h with ⟨x, hx, hy⟩
    have hxv : v = x := by simpa [pathFinish] using hx
    subst x
    cases q with
    | nil => simp [pathStart] at hy
    | cons a rest =>
      have ha : a = v := by simpa [pathStart] using hy
      subst a
      simp [composePath, pathSum]
  | cons u v rest hs hr ih =>
    have hi := ih (rest_composable h)
    change w u v + pathSum w ((v :: rest) ++ q.tail) =
      (w u v + pathSum w (v :: rest)) + pathSum w q
    rw [show pathSum w ((v :: rest) ++ q.tail) =
      pathSum w (v :: rest) + pathSum w q from hi]
    ring

def historyFromEdges (w : SceneEdge → ℝ) : AdditiveHistoryAction where
  value p := pathSum (edgeReading w) p.val
  identity _ := rfl
  additive p _q h := path_sum_composition _ p.property h

def historyEdge (S : AdditiveHistoryAction) (e : SceneEdge) : ℝ :=
  S.value (edgePath e)

theorem edge_of_history_extension (w : SceneEdge → ℝ) :
    ∀ e, historyEdge (historyFromEdges w) e = w e := by
  intro e
  simp [historyEdge, historyFromEdges, edgePath, pathSum, edgeReading, e.property]

theorem history_value_forced (S : AdditiveHistoryAction) (p : ScenePath) :
    S.value p = pathSum (edgeReading (historyEdge S)) p.val := by
  rcases p with ⟨p, hp⟩
  induction hp with
  | single v => exact S.identity v
  | cons u v rest hs hr ih =>
    have hc : Composable [u, v] (v :: rest) := ⟨v, rfl, rfl⟩
    have ha := S.additive (edgePath ⟨(u, v), hs⟩) ⟨v :: rest, hr⟩ hc
    change S.value ⟨u :: v :: rest, _⟩ = _ at ha
    rw [ha, ih]
    simp [pathSum, edgeReading, hs, historyEdge]

theorem additive_history_ext (S T : AdditiveHistoryAction)
    (h : ∀ p, S.value p = T.value p) : S = T := by
  cases S with
  | mk sv si sa =>
    cases T with
    | mk tv ti ta =>
      simp only at h
      have hv : sv = tv := funext h
      cases hv
      rfl

theorem history_extension_unique (S : AdditiveHistoryAction) :
    historyFromEdges (historyEdge S) = S := by
  apply additive_history_ext
  intro p
  exact (history_value_forced S p).symm

/-- Any profile with the native unit gap can be realized on scene steps by an
actual `ActionProtocol` over the joint scene/full-payload record. -/
def profileCost {N : ℕ} (c : SceneEdge → NativePayload N → ℝ)
    (s t : Vertex33 × NativePayload N) : ℝ := by
  classical
  exact if s = t then 0 else
    if hsame : s.2 = t.2 then
      if hstep : SceneStep s.1 t.1 then c ⟨(s.1, t.1), hstep⟩ t.2 else 1
    else 1

def profileAction (N : ℕ) (c : SceneEdge → NativePayload N → ℝ)
    (hc : ∀ e z, 1 ≤ c e z) : ActionProtocol (scenePayloadProtocol N) := by
  classical
  exact {
    action := profileCost c
    action_refl := by intro s; simp [profileCost]
    action_nontrivial := by
      intro s t hne
      unfold profileCost
      split_ifs with heq hsame hstep
      · exact False.elim (hne heq)
      · exact hc ⟨(s.1, t.1), hstep⟩ t.2
      · exact le_rfl
      · exact le_rfl
  }

def observedEdgeCost {N : ℕ} (A : ActionProtocol (scenePayloadProtocol N))
    (z : NativePayload N) (e : SceneEdge) : ℝ :=
  A.action (e.val.1, z) (e.val.2, z)

theorem profile_action_exact_edge (N : ℕ)
    (c : SceneEdge → NativePayload N → ℝ) (hc : ∀ e z, 1 ≤ c e z)
    (z : NativePayload N) (e : SceneEdge) :
    observedEdgeCost (profileAction N c hc) z e = c e z := by
  classical
  rcases e with ⟨⟨u, v⟩, hs⟩
  have hne : (u, z) ≠ (v, z) := by
    intro h
    have huv := congrArg Prod.fst h
    exact scene_edge_distinct ⟨(u, v), hs⟩ huv
  change profileCost c (u, z) (v, z) = c ⟨(u, v), hs⟩ z
  simp [profileCost, hne, hs]

theorem every_protocol_edge_profile_has_unit_gap {N : ℕ}
    (A : ActionProtocol (scenePayloadProtocol N)) (z : NativePayload N)
    (e : SceneEdge) : 1 ≤ observedEdgeCost A z e := by
  apply A.action_nontrivial
  intro h
  exact scene_edge_distinct e (congrArg Prod.fst h)

def observedHistory {N : ℕ} (A : ActionProtocol (scenePayloadProtocol N))
    (z : NativePayload N) : AdditiveHistoryAction :=
  historyFromEdges (observedEdgeCost A z)

theorem every_additive_history_is_forced_by_observed_edges {N : ℕ}
    (A : ActionProtocol (scenePayloadProtocol N)) (z : NativePayload N)
    (S : AdditiveHistoryAction)
    (hS : ∀ e, historyEdge S e = observedEdgeCost A z e) :
    S = observedHistory A z := by
  have he : historyEdge S = observedEdgeCost A z := funext hS
  rw [← history_extension_unique S, he]
  rfl

theorem complete_product_edge_cost_fiber (N : ℕ)
    (c : SceneEdge → NativePayload N → ℝ) :
    (∃ A : ActionProtocol (scenePayloadProtocol N),
      ∀ e z, observedEdgeCost A z e = c e z) ↔ ∀ e z, 1 ≤ c e z := by
  constructor
  · rintro ⟨A, hA⟩ e z
    rw [← hA e z]
    exact every_protocol_edge_profile_has_unit_gap A z e
  · intro hc
    refine ⟨profileAction N c hc, ?_⟩
    intro e z
    exact profile_action_exact_edge N c hc z e

theorem subunit_profile_rejected (N : ℕ)
    (c : SceneEdge → NativePayload N → ℝ) (e : SceneEdge) (z : NativePayload N)
    (hbelow : c e z < 1) :
    ¬ ∃ A : ActionProtocol (scenePayloadProtocol N),
      ∀ e z, observedEdgeCost A z e = c e z := by
  rintro ⟨A, hA⟩
  have hgap := every_protocol_edge_profile_has_unit_gap A z e
  rw [hA e z] at hgap
  linarith

def anchor (N : ℕ) (k : Fin 2) : ArchiveRolePhasePoint N :=
  fun r => if r = (0, 0) then
    ⟨k.val, by have hk := k.isLt; unfold archiveFibers; omega⟩ else 0

def anchorSite (N : ℕ) (k : Fin 2) : ArchiveRolePhaseGroup N :=
  archiveRolePhasePointGroupEquiv N (anchor N k)

theorem anchor_injective (N : ℕ) : Function.Injective (anchor N) := by
  intro k l h
  apply Fin.ext
  have hv := congrArg (fun p => (p (0, 0)).val) h
  simpa [anchor] using hv

theorem anchor_site_injective (N : ℕ) : Function.Injective (anchorSite N) := by
  intro k l h
  exact anchor_injective N ((archiveRolePhasePointGroupEquiv N).injective h)

def sigma (N : ℕ) (psi : ArchiveCochain N) (k : Fin 2) : ℝ :=
  scalarComponent N psi (anchorSite N k)

def anchorDirection (N : ℕ) (k : Fin 2) : ArchiveCochain N :=
  scalarCochain N (fun x => if x = anchorSite N k then 1 else 0)

theorem anchor_direction_readout (N : ℕ) (k j : Fin 2) :
    sigma N (anchorDirection N k) j = if j = k then 1 else 0 := by
  classical
  simp [sigma, anchorDirection, scalarCochain, scalarComponent,
    (anchor_site_injective N).eq_iff]

def oneAnchorEnergy (N : ℕ) (psi : ArchiveCochain N) : ℝ :=
  sigma N psi 0 ^ 2

def twoAnchorEnergy (N : ℕ) (psi : ArchiveCochain N) : ℝ :=
  sigma N psi 0 ^ 2 + sigma N psi 1 ^ 2

theorem energy_nonnegative (N : ℕ) (psi : ArchiveCochain N) :
    0 ≤ oneAnchorEnergy N psi ∧ 0 ≤ twoAnchorEnergy N psi := by
  constructor
  · exact sq_nonneg _
  · exact add_nonneg (sq_nonneg _) (sq_nonneg _)

theorem full_cochain_one_derivative (N : ℕ) (psi direction : ArchiveCochain N) :
    HasDerivAt (fun t : ℝ => oneAnchorEnergy N (psi + t • direction))
      (2 * sigma N psi 0 * sigma N direction 0) 0 := by
  have h := (((hasDerivAt_const (0 : ℝ) (sigma N psi 0)).add
    ((hasDerivAt_id (0 : ℝ)).mul_const (sigma N direction 0))).pow 2).const_mul 1
  convert h using 1
  · funext t
    simp [oneAnchorEnergy, sigma, scalarComponent, Pi.add_apply,
      Pi.smul_apply, smul_eq_mul]
  · simp

theorem full_cochain_two_derivative (N : ℕ) (psi direction : ArchiveCochain N) :
    HasDerivAt (fun t : ℝ => twoAnchorEnergy N (psi + t • direction))
      (2 * sigma N psi 0 * sigma N direction 0 +
       2 * sigma N psi 1 * sigma N direction 1) 0 := by
  have h0 := full_cochain_one_derivative N psi direction
  have h1 : HasDerivAt (fun t : ℝ => sigma N (psi + t • direction) 1 ^ 2)
      (2 * sigma N psi 1 * sigma N direction 1) 0 := by
    have h := (((hasDerivAt_const (0 : ℝ) (sigma N psi 1)).add
      ((hasDerivAt_id (0 : ℝ)).mul_const (sigma N direction 1))).pow 2).const_mul 1
    convert h using 1
    · funext t
      simp [sigma, scalarComponent, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    · simp
  simpa only [twoAnchorEnergy, oneAnchorEnergy] using h0.add h1

def OneAnchorGate (N : ℕ) (psi : ArchiveCochain N) : Prop :=
  ∀ direction,
    deriv (fun t : ℝ => oneAnchorEnergy N (psi + t • direction)) 0 = 0

def TwoAnchorGate (N : ℕ) (psi : ArchiveCochain N) : Prop :=
  ∀ direction,
    deriv (fun t : ℝ => twoAnchorEnergy N (psi + t • direction)) 0 = 0

theorem one_anchor_full_gate_iff (N : ℕ) (psi : ArchiveCochain N) :
    OneAnchorGate N psi ↔ sigma N psi 0 = 0 := by
  constructor
  · intro h
    have he := h (anchorDirection N 0)
    rw [(full_cochain_one_derivative N psi _).deriv] at he
    simp [anchor_direction_readout] at he
    linarith
  · intro h direction
    rw [(full_cochain_one_derivative N psi direction).deriv, h]
    ring

theorem two_anchor_full_gate_iff (N : ℕ) (psi : ArchiveCochain N) :
    TwoAnchorGate N psi ↔ sigma N psi 0 = 0 ∧ sigma N psi 1 = 0 := by
  constructor
  · intro h
    have h0 := h (anchorDirection N 0)
    have h1 := h (anchorDirection N 1)
    rw [(full_cochain_two_derivative N psi _).deriv] at h0 h1
    simp [anchor_direction_readout] at h0 h1
    constructor <;> linarith
  · rintro ⟨h0, h1⟩ direction
    rw [(full_cochain_two_derivative N psi direction).deriv, h0, h1]
    ring

theorem genuine_root_difference (N : ℕ) :
    OneAnchorGate N (anchorDirection N 1) ∧
      ¬ TwoAnchorGate N (anchorDirection N 1) := by
  rw [one_anchor_full_gate_iff, two_anchor_full_gate_iff]
  simp [anchor_direction_readout]

def profileOne (N : ℕ) : SceneEdge → NativePayload N → ℝ :=
  fun _ z => 1 + oneAnchorEnergy N z.2

def profileTwo (N : ℕ) : SceneEdge → NativePayload N → ℝ :=
  fun _ z => 1 + twoAnchorEnergy N z.2

def oneAction (N : ℕ) : ActionProtocol (scenePayloadProtocol N) :=
  profileAction N (profileOne N) (fun _ z => by
    have h := (energy_nonnegative N z.2).1
    change 1 ≤ 1 + oneAnchorEnergy N z.2
    linarith)

def twoAction (N : ℕ) : ActionProtocol (scenePayloadProtocol N) :=
  profileAction N (profileTwo N) (fun _ z => by
    have h := (energy_nonnegative N z.2).2
    change 1 ≤ 1 + twoAnchorEnergy N z.2
    linarith)

theorem one_action_edge_value (N : ℕ) (e : SceneEdge) (z : NativePayload N) :
    observedEdgeCost (oneAction N) z e = 1 + oneAnchorEnergy N z.2 := by
  exact profile_action_exact_edge N (profileOne N)
    (fun _ z => by
      change 1 ≤ 1 + oneAnchorEnergy N z.2
      linarith [(energy_nonnegative N z.2).1]) z e

theorem two_action_edge_value (N : ℕ) (e : SceneEdge) (z : NativePayload N) :
    observedEdgeCost (twoAction N) z e = 1 + twoAnchorEnergy N z.2 := by
  exact profile_action_exact_edge N (profileTwo N)
    (fun _ z => by
      change 1 ≤ 1 + twoAnchorEnergy N z.2
      linarith [(energy_nonnegative N z.2).2]) z e

def pointProjection (N : ℕ)
    (p : ArchiveRolePhasePoint (N + 1)) : ArchiveRolePhasePoint N :=
  fun r => archiveRGPhaseProjection N (p r)

theorem literal_projection_preserves_anchors (N : ℕ) (k : Fin 2) :
    pointProjection N (anchor (N + 1) k) = anchor N k := by
  funext r
  apply Fin.ext
  have hk : k.val < archiveFibers N := by
    have := k.isLt
    unfold archiveFibers
    omega
  by_cases hr : r = (0, 0)
  · simp [pointProjection, anchor, hr, archiveRGPhaseProjection, Nat.mod_eq_of_lt hk]
  · simp [pointProjection, anchor, hr, archiveRGPhaseProjection]

def groupProjection (N : ℕ) (x : ArchiveRolePhaseGroup (N + 1)) :
    ArchiveRolePhaseGroup N :=
  archiveRolePhasePointGroupEquiv N
    (pointProjection N ((archiveRolePhasePointGroupEquiv (N + 1)).symm x))

theorem group_projection_preserves_anchors (N : ℕ) (k : Fin 2) :
    groupProjection N (anchorSite (N + 1) k) = anchorSite N k := by
  simp [groupProjection, anchorSite, literal_projection_preserves_anchors]

def ScalarRefinementCompatible (N : ℕ)
    (R : ArchiveCochain N → ArchiveCochain (N + 1)) : Prop :=
  ∀ psi x, scalarComponent (N + 1) (R psi) x =
    scalarComponent N psi (groupProjection N x)

/-- Literal all-grade pullback along the owned archive projection. It transports
every Fock label and every cochain value; only scalar-readout compatibility is
used by the two action consumers below. This is not asserted to be the
physically admitted metric/link refinement. -/
def fullArchiveCochainLift (N : ℕ) (psi : ArchiveCochain N) :
    ArchiveCochain (N + 1) :=
  fun p => psi (groupProjection N p.1, p.2)

theorem full_archive_lift_is_scalar_compatible (N : ℕ) :
    ScalarRefinementCompatible N (fullArchiveCochainLift N) := by
  intro psi x
  rfl

theorem scalar_refinement_preserves_energies (N : ℕ)
    (R : ArchiveCochain N → ArchiveCochain (N + 1))
    (hR : ScalarRefinementCompatible N R) (psi : ArchiveCochain N) :
    oneAnchorEnergy (N + 1) (R psi) = oneAnchorEnergy N psi ∧
      twoAnchorEnergy (N + 1) (R psi) = twoAnchorEnergy N psi := by
  have hs (k : Fin 2) : sigma (N + 1) (R psi) k = sigma N psi k := by
    unfold sigma
    rw [hR psi, group_projection_preserves_anchors]
  simp [oneAnchorEnergy, twoAnchorEnergy, hs]

def payloadRefinement {N : ℕ} (B : NativeBackground N → NativeBackground (N + 1))
    (R : ArchiveCochain N → ArchiveCochain (N + 1)) :
    NativePayload N → NativePayload (N + 1) := fun z => (B z.1, R z.2)

theorem one_action_edge_refines (N : ℕ) (B : NativeBackground N → NativeBackground (N + 1))
    (R : ArchiveCochain N → ArchiveCochain (N + 1))
    (hR : ScalarRefinementCompatible N R) (e : SceneEdge) (z : NativePayload N) :
    observedEdgeCost (oneAction N) z e =
      observedEdgeCost (oneAction (N + 1)) (payloadRefinement B R z) e := by
  rw [one_action_edge_value, one_action_edge_value]
  have hE := scalar_refinement_preserves_energies N R hR z.2
  change 1 + oneAnchorEnergy N z.2 =
    1 + oneAnchorEnergy (N + 1) (R z.2)
  exact congrArg (fun x : ℝ => 1 + x) hE.1.symm

theorem two_action_edge_refines (N : ℕ) (B : NativeBackground N → NativeBackground (N + 1))
    (R : ArchiveCochain N → ArchiveCochain (N + 1))
    (hR : ScalarRefinementCompatible N R) (e : SceneEdge) (z : NativePayload N) :
    observedEdgeCost (twoAction N) z e =
      observedEdgeCost (twoAction (N + 1)) (payloadRefinement B R z) e := by
  rw [two_action_edge_value, two_action_edge_value]
  have hE := scalar_refinement_preserves_energies N R hR z.2
  change 1 + twoAnchorEnergy N z.2 =
    1 + twoAnchorEnergy (N + 1) (R z.2)
  exact congrArg (fun x : ℝ => 1 + x) hE.2.symm

theorem one_action_archive_projection_refines (N : ℕ)
    (B : NativeBackground N → NativeBackground (N + 1))
    (e : SceneEdge) (z : NativePayload N) :
    observedEdgeCost (oneAction N) z e =
      observedEdgeCost (oneAction (N + 1))
        (payloadRefinement B (fullArchiveCochainLift N) z) e := by
  exact one_action_edge_refines N B (fullArchiveCochainLift N)
    (full_archive_lift_is_scalar_compatible N) e z

theorem two_action_archive_projection_refines (N : ℕ)
    (B : NativeBackground N → NativeBackground (N + 1))
    (e : SceneEdge) (z : NativePayload N) :
    observedEdgeCost (twoAction N) z e =
      observedEdgeCost (twoAction (N + 1))
        (payloadRefinement B (fullArchiveCochainLift N) z) e := by
  exact two_action_edge_refines N B (fullArchiveCochainLift N)
    (full_archive_lift_is_scalar_compatible N) e z

def oneEdgeReadout (N : ℕ) (e : SceneEdge) (b : NativeBackground N)
    (psi : ArchiveCochain N) : ℝ :=
  observedEdgeCost (oneAction N) (b, psi) e

def twoEdgeReadout (N : ℕ) (e : SceneEdge) (b : NativeBackground N)
    (psi : ArchiveCochain N) : ℝ :=
  observedEdgeCost (twoAction N) (b, psi) e

theorem one_edge_matter_derivative (N : ℕ) (e : SceneEdge)
    (b : NativeBackground N) (psi direction : ArchiveCochain N) :
    HasDerivAt (fun t : ℝ => oneEdgeReadout N e b (psi + t • direction))
      (2 * sigma N psi 0 * sigma N direction 0) 0 := by
  convert (full_cochain_one_derivative N psi direction).const_add 1 using 1
  funext t
  simp [oneEdgeReadout, one_action_edge_value, oneAnchorEnergy]

theorem two_edge_matter_derivative (N : ℕ) (e : SceneEdge)
    (b : NativeBackground N) (psi direction : ArchiveCochain N) :
    HasDerivAt (fun t : ℝ => twoEdgeReadout N e b (psi + t • direction))
      (2 * sigma N psi 0 * sigma N direction 0 +
       2 * sigma N psi 1 * sigma N direction 1) 0 := by
  convert (full_cochain_two_derivative N psi direction).const_add 1 using 1
  funext t
  simp [twoEdgeReadout, two_action_edge_value, twoAnchorEnergy]

theorem same_state_different_matter_jet (N : ℕ) (e : SceneEdge)
    (b : NativeBackground N) :
    deriv (fun t : ℝ => oneEdgeReadout N e b
      (anchorDirection N 1 + t • anchorDirection N 1)) 0 = 0 ∧
    deriv (fun t : ℝ => twoEdgeReadout N e b
      (anchorDirection N 1 + t • anchorDirection N 1)) 0 = 2 := by
  have h1 := (one_edge_matter_derivative N e b (anchorDirection N 1)
    (anchorDirection N 1)).deriv
  have h2 := (two_edge_matter_derivative N e b (anchorDirection N 1)
    (anchorDirection N 1)).deriv
  rw [h1, h2]
  simp [anchor_direction_readout]

def sceneEdge09 : SceneEdge :=
  ⟨(0, 9), D0.VNext2.ScenePathHistoryCanonicity.edge_0_9⟩

theorem same_state_different_edge_price (N : ℕ) (e : SceneEdge)
    (b : NativeBackground N) :
    observedEdgeCost (oneAction N) (b, anchorDirection N 1) e = 1 ∧
      observedEdgeCost (twoAction N) (b, anchorDirection N 1) e = 2 := by
  rw [one_action_edge_value, two_action_edge_value]
  norm_num [oneAnchorEnergy, twoAnchorEnergy, anchor_direction_readout]

theorem concrete_scene_edge_is_present : sceneEdge09.val = (0, 9) := rfl

theorem sceneEdge09_kernel : SceneStep 0 9 := by
  unfold SceneStep Adj31 zone31
  decide

theorem sceneEdge90_kernel : SceneStep 9 0 := by
  unfold SceneStep Adj31 zone31
  decide

def sceneReturnPath09 : ScenePath :=
  ⟨[0, 9, 0], IsSceneWalk.cons 0 9 [0] sceneEdge09_kernel
    (IsSceneWalk.cons 9 0 [] sceneEdge90_kernel (IsSceneWalk.single 0))⟩

/-- With the complete payload frozen, a real closed scene return has positive
additive history cost, while the product verification state has returned to
the identical endpoint. Thus this state carrier cannot encode retained return
history in its endpoint action. -/
theorem fixed_payload_closed_return_has_history_cost (N : ℕ)
    (A : ActionProtocol (scenePayloadProtocol N)) (z : NativePayload N) :
    2 ≤ (observedHistory A z).value sceneReturnPath09 ∧
      A.action (0, z) (0, z) = 0 := by
  have hsum : (observedHistory A z).value sceneReturnPath09 =
      observedEdgeCost A z ⟨(0, 9), sceneEdge09_kernel⟩ +
      observedEdgeCost A z ⟨(9, 0), sceneEdge90_kernel⟩ := by
    rw [history_value_forced]
    simp [observedHistory, historyEdge, historyFromEdges, pathSum, edgeReading,
      edgePath, sceneReturnPath09, sceneEdge09_kernel, sceneEdge90_kernel]
  constructor
  · rw [hsum]
    have h01 := every_protocol_edge_profile_has_unit_gap A z
      ⟨(0, 9), sceneEdge09_kernel⟩
    have h90 := every_protocol_edge_profile_has_unit_gap A z
      ⟨(9, 0), sceneEdge90_kernel⟩
    linarith
  · exact A.action_refl _

theorem background_variation_is_blind_one (N : ℕ) (e : SceneEdge)
    (bcurve : ℝ → NativeBackground N) (psi : ArchiveCochain N) :
    HasDerivAt (fun t : ℝ => oneEdgeReadout N e (bcurve t) psi) 0 0 := by
  have hfun : (fun t : ℝ => oneEdgeReadout N e (bcurve t) psi) =
      fun _ => 1 + oneAnchorEnergy N psi := by
    funext t
    simp [oneEdgeReadout, one_action_edge_value, oneAnchorEnergy]
  rw [hfun]
  exact hasDerivAt_const (0 : ℝ) (1 + oneAnchorEnergy N psi)

theorem background_variation_is_blind_two (N : ℕ) (e : SceneEdge)
    (bcurve : ℝ → NativeBackground N) (psi : ArchiveCochain N) :
    HasDerivAt (fun t : ℝ => twoEdgeReadout N e (bcurve t) psi) 0 0 := by
  have hfun : (fun t : ℝ => twoEdgeReadout N e (bcurve t) psi) =
      fun _ => 1 + twoAnchorEnergy N psi := by
    funext t
    simp [twoEdgeReadout, two_action_edge_value, twoAnchorEnergy]
  rw [hfun]
  exact hasDerivAt_const (0 : ℝ) (1 + twoAnchorEnergy N psi)

end
end D0.Research.NativeScenePayloadAction

#check D0.Research.NativeScenePayloadAction.complete_product_edge_cost_fiber
#check D0.Research.NativeScenePayloadAction.subunit_profile_rejected
#check D0.Research.NativeScenePayloadAction.every_additive_history_is_forced_by_observed_edges
#check D0.Research.NativeScenePayloadAction.genuine_root_difference
#check D0.Research.NativeScenePayloadAction.same_state_different_matter_jet
#check D0.Research.NativeScenePayloadAction.same_state_different_edge_price
#check D0.Research.NativeScenePayloadAction.concrete_scene_edge_is_present
#check D0.Research.NativeScenePayloadAction.fixed_payload_closed_return_has_history_cost
#check D0.Research.NativeScenePayloadAction.scalar_refinement_preserves_energies
#check D0.Research.NativeScenePayloadAction.full_archive_lift_is_scalar_compatible
#check D0.Research.NativeScenePayloadAction.one_action_edge_refines
#check D0.Research.NativeScenePayloadAction.two_action_edge_refines
#check D0.Research.NativeScenePayloadAction.one_action_archive_projection_refines
#check D0.Research.NativeScenePayloadAction.two_action_archive_projection_refines
#check D0.Research.NativeScenePayloadAction.background_variation_is_blind_one
#check D0.Research.NativeScenePayloadAction.background_variation_is_blind_two

#print axioms D0.Research.NativeScenePayloadAction.complete_product_edge_cost_fiber
#print axioms D0.Research.NativeScenePayloadAction.subunit_profile_rejected
#print axioms D0.Research.NativeScenePayloadAction.every_additive_history_is_forced_by_observed_edges
#print axioms D0.Research.NativeScenePayloadAction.genuine_root_difference
#print axioms D0.Research.NativeScenePayloadAction.same_state_different_matter_jet
#print axioms D0.Research.NativeScenePayloadAction.same_state_different_edge_price
#print axioms D0.Research.NativeScenePayloadAction.fixed_payload_closed_return_has_history_cost
#print axioms D0.Research.NativeScenePayloadAction.scalar_refinement_preserves_energies
#print axioms D0.Research.NativeScenePayloadAction.full_archive_lift_is_scalar_compatible
#print axioms D0.Research.NativeScenePayloadAction.one_action_edge_refines
#print axioms D0.Research.NativeScenePayloadAction.two_action_edge_refines
#print axioms D0.Research.NativeScenePayloadAction.one_action_archive_projection_refines
#print axioms D0.Research.NativeScenePayloadAction.two_action_archive_projection_refines
#print axioms D0.Research.NativeScenePayloadAction.background_variation_is_blind_one
#print axioms D0.Research.NativeScenePayloadAction.background_variation_is_blind_two
