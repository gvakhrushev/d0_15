import D0.Foundation.EndogenousActionQuantum
import D0.Geometry.ArchiveAffineExteriorLink
import D0.Geometry.A4DNilpotentAffineMatterLift
import D0.Geometry.ArchiveLaplacianRG
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Pow

/-! Complete pullbacks of the actual ActionProtocol through an independently
given prepared pair. The native scalar tests below are countermodels of this
typed interface, not a new D0 action or a native history preparation theorem. -/
namespace D0.Research.NativePreparedAction
open D0 D0.Geometry D0.Geometry.ArchiveRolePhaseProductCarrier
open D0.Foundation.VerifiabilityNecessity D0.Foundation.EndogenousActionQuantum
noncomputable section

variable {P : VerificationProtocol} {X : Type}

def PreparedConditions (u v : X → P.State) (f : X → ℝ) : Prop :=
  (∀ x, u x = v x → f x = 0) ∧
  (∀ x, u x ≠ v x → 1 ≤ f x) ∧
  (∀ x y, u x = u y → v x = v y → f x = f y)

def extensionCost (u v : X → P.State) (f : X → ℝ) (s t : P.State) : ℝ := by
  classical
  exact if s = t then 0 else
    if h : ∃ x, u x = s ∧ v x = t then f (Classical.choose h) else 1

theorem extension_on_preparation (u v : X → P.State) (f : X → ℝ)
    (hf : PreparedConditions u v f) (x : X) :
    extensionCost u v f (u x) (v x) = f x := by
  classical
  by_cases h : u x = v x
  · simp [extensionCost, h, hf.1 x h]
  · have hex : ∃ y, u y = u x ∧ v y = v x := ⟨x, rfl, rfl⟩
    simp only [extensionCost, if_neg h, dif_pos hex]
    exact hf.2.2 _ x (Classical.choose_spec hex).1 (Classical.choose_spec hex).2

def extensionProtocol (u v : X → P.State) (f : X → ℝ)
    (hf : PreparedConditions u v f) : ActionProtocol P where
  action := extensionCost u v f
  action_refl s := by simp [extensionCost]
  action_nontrivial s t h := by
    classical
    simp only [extensionCost, if_neg h]
    split_ifs with hex
    · apply hf.2.1
      intro heq
      exact h ((Classical.choose_spec hex).1.symm.trans
        (heq.trans (Classical.choose_spec hex).2))
    · exact le_refl 1

/-- Both directions, for every protocol, every preparation, every scalar. -/
theorem complete_prepared_action_fiber (u v : X → P.State) (f : X → ℝ) :
    (∃ A : ActionProtocol P, ∀ x, A.action (u x) (v x) = f x) ↔
      PreparedConditions u v f := by
  constructor
  · rintro ⟨A, hA⟩
    refine ⟨?_, ?_, ?_⟩
    · intro x hx
      rw [← hA x, hx, A.action_refl]
    · intro x hx
      rw [← hA x]
      exact A.action_nontrivial _ _ hx
    · intro x y hu hv
      rw [← hA x, ← hA y, hu, hv]
  · intro hf
    exact ⟨extensionProtocol u v f hf, extension_on_preparation u v f hf⟩

theorem preparation_collision_is_record_collision (V : VerificationContract P)
    (u v : X → P.State) (x y : X) :
    (u x = u y ∧ v x = v y) ↔
      (P.record (u x) = P.record (u y) ∧ P.record (v x) = P.record (v y)) := by
  constructor
  · rintro ⟨hu,hv⟩; exact ⟨congrArg P.record hu, congrArg P.record hv⟩
  · rintro ⟨hu,hv⟩; exact ⟨record_injective V hu, record_injective V hv⟩

theorem off_diagonal_complete_fiber (u v : X → P.State)
    (hoff : ∀ x, u x ≠ v x) (f : X → ℝ) :
    (∃ A : ActionProtocol P, ∀ x, A.action (u x) (v x) = f x) ↔
      (∀ x, 1 ≤ f x) ∧
      (∀ x y, u x = u y → v x = v y → f x = f y) := by
  rw [complete_prepared_action_fiber]
  constructor
  · intro h; exact ⟨fun x => h.2.1 x (hoff x), h.2.2⟩
  · rintro ⟨hgap,hfiber⟩
    exact ⟨fun x hx => False.elim (hoff x hx), fun x _ => hgap x, hfiber⟩

theorem canonical_prepared_action (u v : X → P.State)
    (hoff : ∀ x, u x ≠ v x) (x : X) :
    (canonicalActionProtocol P).action (u x) (v x) = 1 := by
  simp [canonicalActionProtocol, hoff x]

/-- A readout is required to be constant on prepared-record fibers. This
premise is shown explicitly; it is not a native preparation theorem. -/
theorem observable_energy_is_extendible (u v : X → P.State)
    (hoff : ∀ x, u x ≠ v x) (sigma : X → ℝ)
    (hfiber : ∀ x y, u x = u y → v x = v y → sigma x = sigma y)
    (theta : ℝ) (htheta : 0 ≤ theta) :
    ∃ A : ActionProtocol P, ∀ x,
      A.action (u x) (v x) = 1 + theta * sigma x ^ 2 := by
  apply (off_diagonal_complete_fiber u v hoff _).2
  constructor
  · intro x; nlinarith [sq_nonneg (sigma x), mul_nonneg htheta (sq_nonneg (sigma x))]
  · intro x y hu hv; rw [hfiber x y hu hv]

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

def anchorDirection (N : ℕ) (k : Fin 2) : ArchiveCochain N :=
  scalarCochain N (fun x => if x = anchorSite N k then 1 else 0)

theorem anchor_direction_readout (N : ℕ) (k j : Fin 2) :
    sigma N (anchorDirection N k) j = if j = k then 1 else 0 := by
  classical
  simp [sigma, anchorDirection, scalarCochain, scalarComponent,
    (anchor_site_injective N).eq_iff]

theorem actual_affine_node_gauge_preserves_sigma {N : ℕ}
    (g : AffineNodeGauge N ℝ RoleSpace) (psi : ArchiveCochain N) (k : Fin 2) :
    sigma N (archiveAffineCoChainGauge g psi) k = sigma N psi k := by
  exact archiveExteriorFrameLift_vacuum_coeff (g (anchorSite N k)).lin _

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
  · simp [pointProjection, anchor, hr, archiveRGPhaseProjection, Nat.mod_eq_of_lt hk]
  · simp [pointProjection, anchor, hr, archiveRGPhaseProjection]

def groupProjection (N : ℕ) (x : ArchiveRolePhaseGroup (N+1)) : ArchiveRolePhaseGroup N :=
  archiveRolePhasePointGroupEquiv N
    (pointProjection N ((archiveRolePhasePointGroupEquiv (N+1)).symm x))

theorem group_projection_preserves_anchors (N : ℕ) (k : Fin 2) :
    groupProjection N (anchorSite (N+1) k) = anchorSite N k := by
  simp [groupProjection, anchorSite, literal_projection_preserves_anchors]

/-- Only the scalar block is prescribed. In particular this definition does
not replace the other fifteen graded blocks by a vertex pullback. -/
def ScalarRefinementCompatible (N : ℕ)
    (R : ArchiveCochain N → ArchiveCochain (N+1)) : Prop :=
  ∀ psi x, scalarComponent (N+1) (R psi) x =
    scalarComponent N psi (groupProjection N x)

theorem actual_scalar_block_preserves_sigma (N : ℕ)
    (R : ArchiveCochain N → ArchiveCochain (N+1))
    (hR : ScalarRefinementCompatible N R) (psi : ArchiveCochain N) (k : Fin 2) :
    sigma (N+1) (R psi) k = sigma N psi k := by
  unfold sigma
  rw [hR psi, group_projection_preserves_anchors]

def oneAnchorEnergy (N : ℕ) (psi : ArchiveCochain N) : ℝ := sigma N psi 0 ^ 2
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
  convert genuine_observable_derivative 1 (sigma N psi 0) (sigma N direction 0) using 1
  · funext t; simp [oneAnchorEnergy, sigma, scalarComponent, Pi.add_apply,
      Pi.smul_apply, smul_eq_mul]
  · simp [observableFirstVariation]

theorem full_cochain_two_derivative (N : ℕ) (psi direction : ArchiveCochain N) :
    HasDerivAt (fun t : ℝ => twoAnchorEnergy N (psi + t • direction))
      (2 * sigma N psi 0 * sigma N direction 0 +
       2 * sigma N psi 1 * sigma N direction 1) 0 := by
  have h0 := full_cochain_one_derivative N psi direction
  have h1 : HasDerivAt (fun t : ℝ => sigma N (psi + t • direction) 1 ^ 2)
      (2 * sigma N psi 1 * sigma N direction 1) 0 := by
    convert genuine_observable_derivative 1 (sigma N psi 1) (sigma N direction 1) using 1
    · funext t; simp [sigma, scalarComponent, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    · simp [observableFirstVariation]
  simpa only [twoAnchorEnergy, oneAnchorEnergy] using h0.add h1

/-- These gates use the actual derivative of the displayed polynomial for
every direction on the full sixteen-component cochain, not a target gate. -/
def OneAnchorGate (N : ℕ) (psi : ArchiveCochain N) : Prop :=
  ∀ direction, deriv (fun t : ℝ => oneAnchorEnergy N (psi + t • direction)) 0 = 0
def TwoAnchorGate (N : ℕ) (psi : ArchiveCochain N) : Prop :=
  ∀ direction, deriv (fun t : ℝ => twoAnchorEnergy N (psi + t • direction)) 0 = 0

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
  · rintro ⟨h0,h1⟩ direction
    rw [(full_cochain_two_derivative N psi direction).deriv, h0, h1]
    ring

theorem genuine_root_difference (N : ℕ) :
    OneAnchorGate N (anchorDirection N 1) ∧
      ¬ TwoAnchorGate N (anchorDirection N 1) := by
  rw [one_anchor_full_gate_iff, two_anchor_full_gate_iff]
  simp [anchor_direction_readout]

theorem same_native_gauge_cannot_remove_difference (N : ℕ)
    (g : AffineNodeGauge N ℝ RoleSpace) :
    ¬ TwoAnchorGate N (archiveAffineCoChainGauge g (anchorDirection N 1)) := by
  rw [two_anchor_full_gate_iff]
  simp [actual_affine_node_gauge_preserves_sigma, anchor_direction_readout]

theorem scalar_compatible_refinement_preserves_actions (N : ℕ)
    (R : ArchiveCochain N → ArchiveCochain (N+1))
    (hR : ScalarRefinementCompatible N R) (psi : ArchiveCochain N) :
    oneAnchorEnergy (N+1) (R psi) = oneAnchorEnergy N psi ∧
      twoAnchorEnergy (N+1) (R psi) = twoAnchorEnergy N psi := by
  simp [oneAnchorEnergy, twoAnchorEnergy, actual_scalar_block_preserves_sigma N R hR]

theorem scalar_compatible_refinement_preserves_gates (N : ℕ)
    (R : ArchiveCochain N → ArchiveCochain (N+1))
    (hR : ScalarRefinementCompatible N R) (psi : ArchiveCochain N) :
    (OneAnchorGate (N+1) (R psi) ↔ OneAnchorGate N psi) ∧
      (TwoAnchorGate (N+1) (R psi) ↔ TwoAnchorGate N psi) := by
  simp [one_anchor_full_gate_iff, two_anchor_full_gate_iff,
    actual_scalar_block_preserves_sigma N R hR]

theorem background_source_zero {Y : Type} (N : ℕ)
    (psi : ArchiveCochain N) (curve : ℝ → Y) :
    HasDerivAt (fun t : ℝ => (fun _ : Y => twoAnchorEnergy N psi) (curve t)) 0 0 :=
  hasDerivAt_const _ _

def GeometryGate {Y D : Type} (J : Y → ℝ) (curves : Y → D → ℝ → Y) (b : Y) : Prop :=
  ∀ d, deriv (fun t => J (curves b d t)) 0 = 0

def MatterGate {N : ℕ} (E : ArchiveCochain N → ℝ) (psi : ArchiveCochain N) : Prop :=
  ∀ direction, deriv (fun t : ℝ => E (psi + t • direction)) 0 = 0

def JointGate {Y D : Type} {N : ℕ} (J : Y → ℝ)
    (curves : Y → D → ℝ → Y) (E : ArchiveCochain N → ℝ)
    (b : Y) (psi : ArchiveCochain N) : Prop :=
  ∀ d direction, deriv (fun t : ℝ => J (curves b d t) + E (psi + t • direction)) 0 = 0

/-- Joint stationarity is derived from actual differentientiable actions.
The geometry derivative premise is retained and no target equation enters
the gate. Independent product variations and a nonempty background direction
carrier are explicit hypotheses. -/
theorem genuine_joint_gate_iff {Y D : Type} [Nonempty D] {N : ℕ}
    (J : Y → ℝ) (curves : Y → D → ℝ → Y) (E : ArchiveCochain N → ℝ)
    (b : Y) (psi : ArchiveCochain N)
    (_hbase : ∀ d, curves b d 0 = b)
    (hJ : ∀ d, DifferentiableAt ℝ (fun t => J (curves b d t)) 0)
    (hE : ∀ direction, DifferentiableAt ℝ (fun t : ℝ => E (psi + t • direction)) 0) :
    JointGate J curves E b psi ↔ GeometryGate J curves b ∧ MatterGate E psi := by
  have hd (d : D) (direction : ArchiveCochain N) :
      deriv (fun t : ℝ => J (curves b d t) + E (psi + t • direction)) 0 =
        deriv (fun t => J (curves b d t)) 0 +
        deriv (fun t : ℝ => E (psi + t • direction)) 0 :=
    ((hJ d).hasDerivAt.add (hE direction).hasDerivAt).deriv
  constructor
  · intro h
    have hg : GeometryGate J curves b := by
      intro d
      have he := h d 0
      rw [hd] at he
      simpa using he
    refine ⟨hg, ?_⟩
    intro direction
    obtain ⟨d⟩ := ‹Nonempty D›
    have he := h d direction
    rw [hd, hg d, zero_add] at he
    exact he
  · rintro ⟨hg,he⟩ d direction
    rw [hd, hg d, he direction]
    ring

/-- A real stationary background of one pre-existing geometry action is a
premise. J=0 witnesses interface nonemptiness, never native GR dynamics. -/
theorem common_background_joint_root_difference {Y D : Type} [Nonempty D]
    (N : ℕ) (J : Y → ℝ) (curves : Y → D → ℝ → Y) (b : Y)
    (hbase : ∀ d, curves b d 0 = b)
    (hJ : ∀ d, DifferentiableAt ℝ (fun t => J (curves b d t)) 0)
    (hg : GeometryGate J curves b) :
    JointGate J curves (oneAnchorEnergy N) b (anchorDirection N 1) ∧
      ¬ JointGate J curves (twoAnchorEnergy N) b (anchorDirection N 1) := by
  have h1 := genuine_joint_gate_iff J curves (oneAnchorEnergy N) b
    (anchorDirection N 1) hbase hJ (fun v => (full_cochain_one_derivative N _ v).differentiableAt)
  have h2 := genuine_joint_gate_iff J curves (twoAnchorEnergy N) b
    (anchorDirection N 1) hbase hJ (fun v => (full_cochain_two_derivative N _ v).differentiableAt)
  rw [h1,h2]
  exact ⟨⟨hg,(genuine_root_difference N).1⟩,
    fun h => (genuine_root_difference N).2 h.2⟩

/-- Full raw solder and full affine link (including shifts) are retained.
This is a mathematical payload type, not native preparation/admission. -/
abbrev NativeBackground (N : ℕ) :=
  {e : LocalCoframeField N // ∀ x, IsUnit (rawSolderMatrix N e x).det} ×
    LorentzAffineExteriorConnection N

def flatNativeBackground (N : ℕ) : NativeBackground N :=
  (⟨0, fun x => by
    have he : rawSolderMatrix N 0 x = roleLorentzMetric := by
      ext r a
      simp [rawSolderMatrix]
    rw [he]
    exact roleLorentzMetric_det_isUnit⟩,
    ⟨flatAffineConnection N, flatAffineExteriorConnection_isLorentz⟩)

abbrev NativePayload (N : ℕ) := NativeBackground N × ArchiveCochain N

/-- Explicit verification countermodel: the persistent bit separates a
prepared edge without changing its literal field payload. It is not the
scene history carrier and is not adopted as a physical D0 protocol. -/
def payloadProtocol (N : ℕ) : VerificationProtocol where
  State := Bool × NativePayload N
  Record := Bool × NativePayload N
  Line := Bool
  Catalogue := Unit
  stateDecidableEq := Classical.decEq _
  record := id
  compare := by
    classical
    exact fun _ _ s t => decide (s ≠ t)

theorem payload_verification_contract (N : ℕ) : VerificationContract (payloadProtocol N) where
  state_nontrivial := ⟨⟨(false,flatNativeBackground N,0),
    (true,flatNativeBackground N,0), by intro h; cases congrArg Prod.fst h⟩⟩
  line_nontrivial := inferInstanceAs (Nontrivial Bool)
  catalogue_nonempty := inferInstanceAs (Nonempty Unit)
  correct := by intro _ _ _ _; simp [payloadProtocol]

def payloadAction (N : ℕ) (E : ArchiveCochain N → ℝ) (hE : ∀ psi, 0 ≤ E psi) :
    ActionProtocol (payloadProtocol N) where
  action s t := if s = t then 0 else 1 + E t.2.2
  action_refl s := by simp
  action_nontrivial s t h := by simp only [if_neg h]; linarith [hE t.2.2]

def jointPayloadAction (N : ℕ) (J : NativeBackground N → ℝ) (m : ℝ)
    (hJ : ∀ b, m ≤ J b) (E : ArchiveCochain N → ℝ) (hE : ∀ psi, 0 ≤ E psi) :
    ActionProtocol (payloadProtocol N) where
  action s t := if s = t then 0 else 1 + (J t.2.1 - m) + E t.2.2
  action_refl s := by simp
  action_nontrivial s t h := by
    simp only [if_neg h]
    linarith [hE t.2.2, hJ t.2.1]

theorem joint_payload_prepared_edge_value (N : ℕ)
    (J : NativeBackground N → ℝ) (m : ℝ) (hJ : ∀ b, m ≤ J b)
    (E : ArchiveCochain N → ℝ) (hE : ∀ psi, 0 ≤ E psi) (z : NativePayload N) :
    (jointPayloadAction N J m hJ E hE).action (false,z) (true,z) =
      1 + (J z.1 - m) + E z.2 := by
  classical
  have h : ((false,z) : (payloadProtocol N).State) ≠ (true,z) := by
    intro h
    cases congrArg Prod.fst h
  simp only [jointPayloadAction]
  split_ifs with heq
  · exact False.elim (h heq)
  · rfl

theorem payload_prepared_edge_value (N : ℕ)
    (E : ArchiveCochain N → ℝ) (hE : ∀ psi, 0 ≤ E psi) (z : NativePayload N) :
    (payloadAction N E hE).action (false,z) (true,z) = 1 + E z.2 := by
  classical
  have h : ((false,z) : (payloadProtocol N).State) ≠ (true,z) := by
    intro h
    cases congrArg Prod.fst h
  simp only [payloadAction]
  split_ifs with heq
  · exact False.elim (h heq)
  · rfl

theorem both_native_energies_are_verified_cost_readings (N : ℕ) :
    ∃ A B : ActionProtocol (payloadProtocol N), ∀ z : NativePayload N,
      A.action (false,z) (true,z) = 1 + oneAnchorEnergy N z.2 ∧
      B.action (false,z) (true,z) = 1 + twoAnchorEnergy N z.2 := by
  refine ⟨payloadAction N _ (fun psi => (energy_nonnegative N psi).1),
    payloadAction N _ (fun psi => (energy_nonnegative N psi).2), ?_⟩
  intro z
  exact ⟨payload_prepared_edge_value _ _ _ _, payload_prepared_edge_value _ _ _ _⟩

end
end D0.Research.NativePreparedAction

#check D0.Foundation.EndogenousActionQuantum.ActionProtocol
#check D0.Foundation.VerifiabilityNecessity.VerificationContract
#check D0.Research.NativePreparedAction.complete_prepared_action_fiber
#check D0.Research.NativePreparedAction.off_diagonal_complete_fiber
#check D0.Research.NativePreparedAction.observable_energy_is_extendible
#check D0.Research.NativePreparedAction.genuine_observable_derivative
#check D0.Geometry.archiveExteriorFrameLift_vacuum_coeff
#check D0.Geometry.archiveAffineCoChainGauge
#check D0.Research.NativePreparedAction.ScalarRefinementCompatible
#check D0.Research.NativePreparedAction.one_anchor_full_gate_iff
#check D0.Research.NativePreparedAction.two_anchor_full_gate_iff
#check D0.Research.NativePreparedAction.common_background_joint_root_difference
#check D0.Research.NativePreparedAction.genuine_joint_gate_iff
#check D0.Research.NativePreparedAction.NativeBackground
#check D0.Research.NativePreparedAction.payloadProtocol
#check D0.Research.NativePreparedAction.jointPayloadAction
#check D0.Research.NativePreparedAction.actual_scalar_block_preserves_sigma
#check D0.Research.NativePreparedAction.actual_affine_node_gauge_preserves_sigma
#check D0.Research.NativePreparedAction.scalar_compatible_refinement_preserves_gates
#check D0.Research.NativePreparedAction.both_native_energies_are_verified_cost_readings
#print D0.Research.NativePreparedAction.ScalarRefinementCompatible
#print axioms D0.Research.NativePreparedAction.extension_on_preparation
#print axioms D0.Research.NativePreparedAction.complete_prepared_action_fiber
#print axioms D0.Research.NativePreparedAction.preparation_collision_is_record_collision
#print axioms D0.Research.NativePreparedAction.off_diagonal_complete_fiber
#print axioms D0.Research.NativePreparedAction.canonical_prepared_action
#print axioms D0.Research.NativePreparedAction.observable_energy_is_extendible
#print axioms D0.Research.NativePreparedAction.genuine_observable_derivative
#print axioms D0.Research.NativePreparedAction.anchor_injective
#print axioms D0.Research.NativePreparedAction.anchor_site_injective
#print axioms D0.Research.NativePreparedAction.anchor_direction_readout
#print axioms D0.Research.NativePreparedAction.actual_affine_node_gauge_preserves_sigma
#print axioms D0.Research.NativePreparedAction.literal_projection_preserves_anchors
#print axioms D0.Research.NativePreparedAction.group_projection_preserves_anchors
#print axioms D0.Research.NativePreparedAction.actual_scalar_block_preserves_sigma
#print axioms D0.Research.NativePreparedAction.energy_nonnegative
#print axioms D0.Research.NativePreparedAction.full_cochain_one_derivative
#print axioms D0.Research.NativePreparedAction.full_cochain_two_derivative
#print axioms D0.Research.NativePreparedAction.one_anchor_full_gate_iff
#print axioms D0.Research.NativePreparedAction.two_anchor_full_gate_iff
#print axioms D0.Research.NativePreparedAction.genuine_root_difference
#print axioms D0.Research.NativePreparedAction.same_native_gauge_cannot_remove_difference
#print axioms D0.Research.NativePreparedAction.scalar_compatible_refinement_preserves_actions
#print axioms D0.Research.NativePreparedAction.scalar_compatible_refinement_preserves_gates
#print axioms D0.Research.NativePreparedAction.background_source_zero
#print axioms D0.Research.NativePreparedAction.common_background_joint_root_difference
#print axioms D0.Research.NativePreparedAction.genuine_joint_gate_iff
#print axioms D0.Research.NativePreparedAction.payload_verification_contract
#print axioms D0.Research.NativePreparedAction.payload_prepared_edge_value
#print axioms D0.Research.NativePreparedAction.joint_payload_prepared_edge_value
#print axioms D0.Research.NativePreparedAction.both_native_energies_are_verified_cost_readings
