import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Topology.Connected.TotallyDisconnected
import Mathlib.Topology.Homeomorph.Lemmas
import Mathlib.Tactic
import D0.Dynamics.ToralAutomorphism

/-!
# Toral map versus golden SFT: topological conjugacy no-go

A two-torus is connected.  A subshift of finite type is a subtype of a product
of finite discrete alphabets and is therefore totally disconnected.  Hence a
nontrivial torus cannot be homeomorphic to a golden SFT, so a topological
conjugacy between the toral automorphism and the shift cannot exist.

The correct classical relation is symbolic coding / finite-to-one
semiconjugacy after a Markov partition (with a boundary quotient when one wants
a homeomorphic symbolic model), not a homeomorphism from the torus itself to
the raw SFT.

We also record the elementary matrix-level warning: the D0 toral matrix
`T = [[0,1],[1,-1]]` has trace -1 while the golden transition matrix
`[[0,1],[1,1]]` has trace +1.
-/

namespace D0.Dynamics.ToralSFTConjugacyNoGo

open Matrix
open D0.Dynamics

/-- The connected two-torus `(R/Z)^2`. -/
abbrev Torus2 := Fin 2 → AddCircle (1 : ℝ)

/-- Golden transition matrix used by the two-symbol SFT. -/
def goldenTransition : ZMat2 := !![0, 1; 1, 1]

/-- The toral matrix and the golden adjacency do not even have the same trace. -/
theorem toral_golden_trace_mismatch :
    Matrix.trace T ≠ Matrix.trace goldenTransition := by
  native_decide

/-- Admissibility for the golden edge shift with adjacency
`[[0,1],[1,1]]`: state 0 must be followed by state 1. -/
def goldenAdmissible (x : ℤ → Fin 2) : Prop :=
  ∀ n : ℤ, x n = 0 → x (n + 1) = 1

/-- The raw two-sided golden SFT as a closed symbolic carrier.  For the no-go
only its inherited totally-disconnected topology is needed. -/
abbrev GoldenSFT := {x : ℤ → Fin 2 // goldenAdmissible x}

instance goldenSFTTotallyDisconnected : TotallyDisconnectedSpace GoldenSFT :=
  inferInstance

/-- Two explicit points witness that the two-torus is nontrivial.  We avoid
relying on a `Nontrivial (AddCircle 1)` instance because the pinned Mathlib
version does not expose that instance through this import surface. -/
theorem torus_two_points :
    ∃ x y : Torus2, x ≠ y := by
  let x : Torus2 := fun _ => (0 : AddCircle (1 : ℝ))
  let y : Torus2 := fun i =>
    if i = (0 : Fin 2) then ((1 / 2 : ℝ) : AddCircle (1 : ℝ)) else 0
  refine ⟨x, y, ?_⟩
  intro hxy
  have h0 := congrFun hxy (0 : Fin 2)
  have hcircle :
      ((0 : ℝ) : AddCircle (1 : ℝ)) =
        ((1 / 2 : ℝ) : AddCircle (1 : ℝ)) := by
    simpa [x, y] using h0
  have hz : (0 : ℝ) ∈ Set.Ico (0 : ℝ) (0 + 1) := by
    norm_num
  have hh : (1 / 2 : ℝ) ∈ Set.Ico (0 : ℝ) (0 + 1) := by
    norm_num
  have hreal : (0 : ℝ) = 1 / 2 :=
    (AddCircle.coe_eq_coe_iff_of_mem_Ico (p := (1 : ℝ)) (a := 0) hz hh).mp hcircle
  norm_num at hreal

/-- Every continuous map from a preconnected space into a totally disconnected
space is constant.  This is the exact topological obstruction used below. -/
theorem continuous_into_goldenSFT_constant
    {α : Type*} [TopologicalSpace α] [PreconnectedSpace α]
    (f : α → GoldenSFT) (hf : Continuous f) (x y : α) :
    f x = f y := by
  exact TotallyDisconnectedSpace.eq_of_continuous f hf x y

/-- The connected two-torus is not homeomorphic to the raw golden SFT. -/
theorem torus_not_homeomorphic_goldenSFT :
    IsEmpty (Torus2 ≃ₜ GoldenSFT) := by
  constructor
  intro h
  obtain ⟨x, y, hxy⟩ := torus_two_points
  have heq : h x = h y :=
    continuous_into_goldenSFT_constant h h.continuous x y
  exact hxy (h.injective heq)

/-- **D0-TORAL-SFT-TOPOLOGICAL-CONJUGACY-NOGO-001.**
A torus-to-raw-SFT topological conjugacy is impossible already at the level of
underlying spaces; independently, the displayed toral and golden matrices have
opposite traces.  Any positive closure must therefore be stated as a symbolic
factor/semiconjugacy (or as a boundary-quotient model), not `Torus2 ≃ GoldenSFT`. -/
theorem toral_sft_topological_conjugacy_nogo :
    IsEmpty (Torus2 ≃ₜ GoldenSFT) ∧
    Matrix.trace T ≠ Matrix.trace goldenTransition := by
  exact ⟨torus_not_homeomorphic_goldenSFT, toral_golden_trace_mismatch⟩

end D0.Dynamics.ToralSFTConjugacyNoGo
