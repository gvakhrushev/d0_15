import D0.Foundation.IndependentDetectionSideSymmetryBoundary

/-!
# Composition forces relative data beyond marginal repair ranks

The three repair ranks classify individual history supports modulo side relabeling.
They do not carry a compositional semantics for comparisons sharing an internal source.
This is a boundary on that quotient, not a refutation of its three-class count.

The positive repair is diagonal rather than independent relabeling: relative coordinates
classify joint frames exactly. For two-sided frames, n relative coordinates require at least
2^n distinguishable records. No assertion of physical M1 completeness, Q8 uniqueness,
spacetime dimension, or dynamical gauge field follows from these theorems.
-/

namespace D0.Foundation.RelationalRepairClosure

open D0.Foundation.DetectionCapabilityBoundary
open D0.Foundation.ConcreteIndependentDetectionRepairSemantics
open D0.Foundation.IndependentDetectionSideSymmetryBoundary
open D0.Foundation.IndependentDetectionRepairGrammar

/-- Compare two outputs obtained from the same pair of internally retained observations. -/
def agree (p q : Comparison) : Comparison := fun x y => decide (p x y = q x y)

theorem agree_self_arity (p : Comparison) :
    comparisonRepairArity (agree p p) = 0 := by
  have hs : historySupport (agree p p) = ∅ := by
    ext s
    cases s <;> simp [historySupport, UsesHistorySide, agree]
  apply Fin.ext
  simp [comparisonRepairArity, hs]

theorem agree_opposite_arity :
    comparisonRepairArity (agree oneArityComparison rightArityComparison) = 2 := by
  change comparisonRepairArity twoArityComparison = 2
  exact twoArity_value

/-- No binary operation on the three marginal ranks can evaluate even equality of outputs.
The same pair of marginal ranks (1,1) yields either rank 0 or rank 2. -/
theorem no_composition_on_marginal_ranks :
    ¬ ∃ compose : RepairArity detectionBudget → RepairArity detectionBudget →
        RepairArity detectionBudget,
      ∀ p q, comparisonRepairArity (agree p q) =
        compose (comparisonRepairArity p) (comparisonRepairArity q) := by
  rintro ⟨compose, h⟩
  have hsame := h oneArityComparison oneArityComparison
  have hopposite := h oneArityComparison rightArityComparison
  rw [agree_self_arity, oneArity_value] at hsame
  rw [agree_opposite_arity, oneArity_value, rightArity_value] at hopposite
  have impossible : (0 : RepairArity detectionBudget) = 2 :=
    hsame.trans hopposite.symm
  exact (by decide : (0 : RepairArity detectionBudget) ≠ 2) impossible

section RelativeFrames
variable {G I : Type*} [Group G]

/-- One internal reference and an arbitrary family of frames expressed in the same coordinates. -/
abbrev FramePacket (G I : Type*) := G × (I → G)

def relative (p : FramePacket G I) : I → G := fun i => p.1⁻¹ * p.2 i

def reframe (g : G) (p : FramePacket G I) : FramePacket G I :=
  (g * p.1, fun i => g * p.2 i)

theorem relative_reframe (g : G) (p : FramePacket G I) :
    relative (reframe g p) = relative p := by
  funext i
  simp [relative, reframe, mul_assoc]

/-- Complete classification under simultaneous changes of the whole apparatus frame. -/
theorem relative_eq_iff_common_reframe (p q : FramePacket G I) :
    relative p = relative q ↔ ∃ g : G, reframe g p = q := by
  constructor
  · intro h
    refine ⟨q.1 * p.1⁻¹, ?_⟩
    apply Prod.ext
    · simp [reframe, mul_assoc]
    · funext i
      have hi := congrFun h i
      change p.1⁻¹ * p.2 i = q.1⁻¹ * q.2 i at hi
      change (q.1 * p.1⁻¹) * p.2 i = q.2 i
      rw [mul_assoc, hi]
      simp [mul_assoc]
  · rintro ⟨g, rfl⟩
    exact (relative_reframe g p).symm

/-- Any jointly frame-invariant observable factors through relative coordinates.
The unit here fixes a mathematical representative; it supplies no external physical reference. -/
theorem invariant_readout_factors {O : Type*} (read : FramePacket G I → O)
    (hinv : ∀ g p, read (reframe g p) = read p) (p : FramePacket G I) :
    read p = read (1, relative p) := by
  have hp : reframe p.1⁻¹ p = (1, relative p) := by
    apply Prod.ext
    · simp [reframe]
    · rfl
  rw [← hp, hinv]

/-- Relative frames alone have trivial closed transport. Nontrivial holonomy needs actual
transport data beyond a list of local frame names. -/
theorem frame_only_triangle_flat (a b c : G) :
    (a⁻¹ * b) * (b⁻¹ * c) * (c⁻¹ * a) = 1 := by
  simp [mul_assoc]

/-- With actual edge transports, independent local frame changes leave the closed product
covariant by conjugation at the base point. -/
theorem transported_triangle_conjugates (a b c u v w : G) :
    (a⁻¹ * u * b) * (b⁻¹ * v * c) * (c⁻¹ * w * a) =
      a⁻¹ * (u * v * w) * a := by
  simp [mul_assoc]

end RelativeFrames

/-- The internal reference is retained while each reading is compared with it. -/
def relativeRecorder {I : Type*} (p : Bool × (I → Bool)) : Bool × (I → Bool) :=
  (p.1, fun i => Bool.xor p.1 (p.2 i))

theorem relativeRecorder_involutive {I : Type*} :
    Function.Involutive (@relativeRecorder I) := by
  intro p
  apply Prod.ext
  · rfl
  · funext i
    change Bool.xor p.1 (Bool.xor p.1 (p.2 i)) = p.2 i
    cases p.1 <;> cases p.2 i <;> rfl

/-- A record sufficient to recover every internal relative bit has exponential capacity.
This counts joint patterns, not additional repair ranks or additional spatial zones. -/
theorem relative_record_capacity (n : ℕ) {Record : Type*} [Fintype Record]
    (encode : (Fin n → Bool) → Record) (read : Record → Fin n → Bool)
    (faithful : ∀ pattern i, read (encode pattern) i = pattern i) :
    2 ^ n ≤ Fintype.card Record := by
  have hinj : Function.Injective encode := by
    intro a b hab
    funext i
    calc
      a i = read (encode a) i := (faithful a i).symm
      _ = read (encode b) i := by rw [hab]
      _ = b i := faithful b i
  simpa using Fintype.card_le_of_injective encode hinj

end D0.Foundation.RelationalRepairClosure
