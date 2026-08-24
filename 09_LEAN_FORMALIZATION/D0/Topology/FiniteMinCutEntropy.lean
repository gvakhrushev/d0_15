import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic

open scoped BigOperators

namespace D0.Topology

/-!
# D0-MINCUT-A4-ENTROPY-001 — finite min-cut existence and the terminal-normalized A/4 entropy

A finite network (Fintype vertices, nonneg capacity matrix) has, over the FINITE collection of
proper nonempty vertex subsets, a minimum cut capacity that is ATTAINED by an actual partition —
finiteness replaces the max-flow machinery.  The D0 entanglement entropy is the terminal-
normalized quantity `S = (1/4)·minCutValue`, the `/4` being the ABCD boundary-cell capacity
(link to the gravity sector's area law reading).

Everything here is finite combinatorics: no limits, no measure theory.
-/

/-- Finite network with vertices (Fintype), directed edges encoded via capacity matrix. -/
structure FiniteNetwork (V : Type) [Fintype V] where
  capacity : Matrix V V ℝ
  capacity_nonneg : ∀ i j, 0 ≤ capacity i j

/-- Capacity of a cut (sum of capacities of edges leaving A). -/
noncomputable def cutCapacity {V : Type} [Fintype V] [DecidableEq V]
    (A : Finset V) (net : FiniteNetwork V) : ℝ :=
  ∑ i ∈ A, ∑ j ∈ (Finset.univ \ A), net.capacity i j

theorem finite_cut_capacity_nonnegative {V : Type} [Fintype V] [DecidableEq V]
    (net : FiniteNetwork V) (A : Finset V) :
    0 ≤ cutCapacity A net := by
  unfold cutCapacity
  apply Finset.sum_nonneg
  intro i _
  apply Finset.sum_nonneg
  intro j _
  exact net.capacity_nonneg i j

/-- The collection of proper nonempty subsets (the admissible cuts). -/
noncomputable def properCuts {V : Type} [Fintype V] [DecidableEq V] [Nontrivial V] :
    Finset (Finset V) :=
  Finset.univ.filter fun A => A.Nonempty ∧ A ≠ Finset.univ

theorem properCuts_nonempty {V : Type} [Fintype V] [DecidableEq V] [Nontrivial V] :
    (properCuts (V := V)).Nonempty := by
  obtain ⟨x, y, hxy⟩ := ‹Nontrivial V›.exists_pair_ne
  refine Exists.intro {x} ?_
  show {x} ∈ Finset.univ.filter fun A : Finset V => A.Nonempty ∧ A ≠ Finset.univ
  rw [Finset.mem_filter]
  simp only [Finset.mem_univ, true_and]
  refine ⟨Finset.singleton_nonempty x, ?_⟩
  intro hcon
  obtain ⟨u, v, huv⟩ := ‹Nontrivial V›.exists_pair_ne
  have hu : u = x := by
    have hu1 : u ∈ ({x} : Finset V) := by
      rw [hcon]
      exact Finset.mem_univ u
    simpa using hu1
  have hv : v = x := by
    have hv2 : v ∈ ({x} : Finset V) := by
      rw [hcon]
      exact Finset.mem_univ v
    simpa using hv2
  exact absurd (hu.trans hv.symm) huv

/-- **Finite min-cut attainment.**  Over the finite family of proper nonempty cuts the minimum
    capacity is attained by an actual partition — no max-flow iteration needed. -/
theorem finite_min_cut_exists {V : Type} [Fintype V] [DecidableEq V] [Nontrivial V]
    (net : FiniteNetwork V) :
    ∃ A : Finset V, A ∈ properCuts ∧
      ∀ B : Finset V, B ∈ properCuts → cutCapacity B net ≥ cutCapacity A net := by
  classical
  have himg : ((properCuts (V := V)).image (fun A => cutCapacity A net)).Nonempty :=
    (properCuts_nonempty (V := V)).image _
  have hmin := Finset.min'_mem _ himg
  obtain ⟨A, hAin, hAcap⟩ := Finset.mem_image.mp hmin
  refine ⟨A, hAin, fun B hB => ?_⟩
  have hBcap : cutCapacity B net ∈ (properCuts (V := V)).image (fun A => cutCapacity A net) :=
    Finset.mem_image.mpr ⟨B, hB, rfl⟩
  rw [hAcap]
  exact Finset.min'_le _ _ hBcap

/-- Minimum cut capacity over all proper nonempty partitions. -/
noncomputable def minCutValue {V : Type} [Fintype V] [DecidableEq V] [Nontrivial V]
    (net : FiniteNetwork V) : ℝ :=
  ((properCuts (V := V)).image (fun A => cutCapacity A net)).min'
    ((properCuts_nonempty (V := V)).image _)

/-- D0 finite entanglement entropy: terminal-normalized min-cut capacity / 4. -/
noncomputable def finiteEntanglementEntropy {V : Type} [Fintype V] [DecidableEq V] [Nontrivial V]
    (net : FiniteNetwork V) : ℝ :=
  (1 / 4 : ℝ) * minCutValue net

theorem finite_entanglement_entropy_is_terminal_normalized_min_cut
    {V : Type} [Fintype V] [DecidableEq V] [Nontrivial V] (net : FiniteNetwork V) :
    finiteEntanglementEntropy net = (1 / 4 : ℝ) * minCutValue net := rfl

/-- Entropy is nonnegative (every capacity is). -/
theorem finite_entanglement_entropy_nonneg {V : Type} [Fintype V] [DecidableEq V] [Nontrivial V]
    (net : FiniteNetwork V) : 0 ≤ finiteEntanglementEntropy net := by
  classical
  unfold finiteEntanglementEntropy minCutValue
  obtain ⟨A₀, hA₀mem, hA₀eq⟩ := Finset.mem_image.mp
    (Finset.min'_mem ((properCuts (V := V)).image (fun A => cutCapacity A net))
      ((properCuts_nonempty (V := V)).image _))
  have hnn : 0 ≤ cutCapacity A₀ net := finite_cut_capacity_nonnegative net A₀
  rw [← hA₀eq]
  linarith

end D0.Topology
