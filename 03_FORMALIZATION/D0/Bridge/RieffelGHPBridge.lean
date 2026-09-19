namespace D0.Bridge

namespace BridgeAssumption

/-!
External owner of the finite -> quantum-metric -> smooth continuum interface.

The present D0 core owns a finite graph metric (the finite Connes-distance/geodesic
identity is handled elsewhere).  It does **not** by that fact alone construct a Rieffel
compact quantum metric space: the required order-unit/C*-algebraic state-space and
Lip-norm axioms, and any quantum Gromov-Hausdorff/propinquity distance, are absent from
the local Lean development.

Accordingly this bridge keeps two external pieces explicit:

1. a genuine quantum-metric realization of the finite refinement stages, including
   whatever hypotheses are required by the chosen Rieffel/Latrémolière framework;
2. convergence of those realized stages to the intended continuum limit.

The generic golden Cauchy lemma in `D0.Bridge.GromovHausdorff` can be applied only
*after* such a concrete metric-stage realization and its step bound are supplied.
-/

/-- Explicit external bridge contract.  These propositions are intentionally assumptions,
not locally fabricated CQMS objects. -/
structure RieffelGHPContinuum where
  /-- External mathematical realization of D0 finite stages as genuine objects in the
  selected quantum-metric framework. -/
  finiteStageQuantumMetricRealization : Prop
  /-- External convergence statement in the selected quantum metric/distance, together
  with identification of the intended smooth compact limit. -/
  quantumMetricConvergesToSmooth : Prop
  finiteStageCited : finiteStageQuantumMetricRealization
  convergenceCited : quantumMetricConvergesToSmooth

end BridgeAssumption

abbrev RieffelGHPContinuum := BridgeAssumption.RieffelGHPContinuum

/-- Conditional bridge, and nothing stronger: once a genuine finite-stage quantum-metric
realization and its continuum convergence are supplied externally, both are available to
downstream bridge consumers.

This theorem does not construct a compact quantum metric space or a propinquity distance. -/
theorem rieffel_ghp_continuum_conditional (h : RieffelGHPContinuum) :
    h.finiteStageQuantumMetricRealization ∧ h.quantumMetricConvergesToSmooth :=
  ⟨h.finiteStageCited, h.convergenceCited⟩

end D0.Bridge
