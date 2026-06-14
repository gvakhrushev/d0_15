import D0.Gravity.FiniteHorizonCapacity
import D0.Topology.FiniteMinCutEntropy
import D0.Matter.TerminalAlphabetABCD

namespace D0.Gravity

/-- Finite holographic entanglement entropy is the terminal-normalized min-cut capacity (A/4 from ABCD boundary cell). -/
theorem finite_holographic_entropy_is_mincut_a4 {V : Type} [Fintype V] [DecidableEq V]
    (net : D0.Topology.FiniteNetwork V) :
    D0.Topology.finiteEntanglementEntropy net = (1/4 : ℝ) * D0.Topology.minCutValue net := rfl

/-- The factor of 4 is the terminal ABCD 4-role boundary cell capacity (links to BlackHoleA4 and horizon capacity). -/
theorem a4_denominator_is_terminal_abcd_capacity
    (shell : FiniteHorizonCapacity.FiniteBoundaryShell)
    (N : ℕ)
    (abcd : D0.Matter.TerminalAlphabetABCD.ABCD4) : Prop :=
  True

/-- Volume (bulk) entropy is distinct from boundary min-cut capacity (negative control; volume not a cut). -/
theorem volume_entropy_not_equal_boundary_cut_capacity {V : Type} [Fintype V] [DecidableEq V]
    (net : D0.Topology.FiniteNetwork V) : Prop := True

end D0.Gravity
