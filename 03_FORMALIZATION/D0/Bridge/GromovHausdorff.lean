import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Tactic
import D0.Geometry.GHPGoldenCauchyBound
import D0.Geometry.GHPGoldenCauchySequence

/-!
# Honest boundary of the golden metric-Cauchy result

This module previously described a generic `PseudoMetricSpace` Cauchy lemma as
quantum Gromov--Hausdorff propinquity convergence.  The theorem itself is useful,
but that interpretation was too strong.

What is actually proved here is purely metric:

* if successive points of **any** pseudometric-space sequence satisfy the
  golden geometric step bound, the sequence is Cauchy;
* no C*-algebra, order-unit space, state space, Lip-norm separation,
  Leibniz property, tunnel, bridge or Latremoliere propinquity is constructed.

The first missing quantum-metric object is therefore represented below by an
explicit target signature.  It is a target, not an inhabited CORE object.
-/

namespace D0.Bridge.GromovHausdorff

open D0 D0.Geometry D0.Geometry.GHPGoldenCauchySequence

/-- Minimal nonnegative seminorm-shaped data.  This is intentionally *not*
called a compact quantum metric space: nonnegativity alone does not supply the
Rieffel/Latremoliere axioms. -/
structure NonnegativeLipCandidate (A : Type*) where
  lipNorm : A → ℝ
  lip_nonneg : ∀ a, 0 ≤ lipNorm a

/-- Geometric step envelope used by the already-owned golden Cauchy theorem. -/
noncomputable def goldenMetricStep (C : ℝ) (k : ℕ) : ℝ :=
  C * delta0 ^ k

/-- The exact theorem currently owned: a generic pseudometric sequence with the
golden step bound is Cauchy. -/
theorem golden_pseudometric_cauchy {X : Type*} [PseudoMetricSpace X]
    (x : ℕ → X) (C : ℝ)
    (hstep : ∀ k, dist (x k) (x (k + 1)) ≤ goldenMetricStep C k) :
    CauchySeq x := by
  have htower : GoldenTower x C := ⟨hstep⟩
  exact goldenTower_cauchySeq htower

/-- Package of the honest generic result. -/
theorem generic_metric_cauchy_owner :
    delta0 < 1 ∧
    (∀ (X : Type*) [PseudoMetricSpace X] (x : ℕ → X) (C : ℝ),
      GoldenTower x C → CauchySeq x) := by
  refine ⟨delta0_lt_one, ?_⟩
  intro X _ x C h
  exact goldenTower_cauchySeq h

/-- Scope witness: the theorem applies already to an ordinary real-valued
sequence.  Thus its proof consumes no quantum-metric structure. -/
theorem real_sequence_scope_witness
    (x : ℕ → ℝ) (C : ℝ)
    (hstep : ∀ k, dist (x k) (x (k + 1)) ≤ goldenMetricStep C k) :
    CauchySeq x :=
  golden_pseudometric_cauchy x C hstep

/-! ## First missing quantum-propinquity object

This structure is only a theorem-target signature.  An inhabitant would have to
supply actual stage algebra/state-space data, a Lip-norm predicate stronger than
mere nonnegativity, an actual propinquity-valued distance together with the
metric/tunnel axioms that justify that name, and a D0-specific stage estimate.
The current core provides none of these fields.
-/

/-- Typed target for a genuine Latremoliere-style stage tower.  The predicates
are fields precisely so that this declaration does not smuggle the missing
theorems in as definitions. -/
structure LatremoliereQuantumPropinquityTarget where
  Stage : ℕ → Type*
  LipNorm : (n : ℕ) → Stage n → ℝ
  lip_nonneg : ∀ n a, 0 ≤ LipNorm n a
  /-- Placeholder predicate to be replaced/proved by the actual Rieffel
  Lip-norm axioms (separation/weak-* metricization and required regularity). -/
  isRieffelLipNorm : Prop
  /-- State-space carrier associated to each genuine finite stage. -/
  StateSpace : ℕ → Type*
  /-- Candidate numerical propinquity between stages. -/
  propinquity : ℕ → ℕ → ℝ
  propinquity_nonneg : ∀ m n, 0 ≤ propinquity m n
  /-- The missing mathematical theorem that the preceding quantity is an
  actual Latremoliere propinquity, e.g. obtained from valid tunnels/bridges. -/
  isActualQuantumPropinquity : Prop
  /-- D0-specific estimate needed before the generic Cauchy lemma can be
  applied in that quantum metric. -/
  stage_step_estimate :
    ∃ C : ℝ, ∀ k, propinquity k (k + 1) ≤ goldenMetricStep C k

/-- The present generic Cauchy package and a genuine propinquity target are
logically separate pieces of data.  The theorem records only what CORE owns. -/
theorem pseudometric_cauchy_scope :
    delta0 < 1 ∧
    (∀ (X : Type*) [PseudoMetricSpace X] (x : ℕ → X) (C : ℝ),
      GoldenTower x C → CauchySeq x) :=
  generic_metric_cauchy_owner

end D0.Bridge.GromovHausdorff
