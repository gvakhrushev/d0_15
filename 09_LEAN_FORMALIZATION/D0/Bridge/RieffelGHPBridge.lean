namespace D0.Bridge

namespace BridgeAssumption

/-- External owner of the finite→smooth **continuum limit** for the gravity/geometry layer
(BOOK_07 §07.51.3). The D0 scene is a sequence of finite metric graphs at increasing refinement;
the question is whether that sequence converges to a smooth compact Riemannian space. The apt
classical framework is:

* **Rieffel — compact quantum metric spaces** (M. Rieffel, *Metrics on state spaces*, Doc. Math. 4
  (1999) 559; *Gromov–Hausdorff distance for quantum metric spaces*, Mem. AMS 168 (2004)): a
  spectral/order-unit datum with a Lipschitz seminorm is a compact quantum metric space, and such
  spaces carry a **quantum Gromov–Hausdorff distance**.
* **Gromov–Hausdorff(–Prokhorov) convergence**: a Cauchy sequence of compact metric (measure)
  spaces in the (q)GH(P) metric has a limit compact metric space.

D0 proves internally (cert `vp_connes_distance_geodesic.py`, claim
`D0-CONNES-DISTANCE-GEODESIC-001`): on each finite scene the Connes spectral distance equals the
graph geodesic and the cone speed is `c = 1 = edge/tick` (structural), so each finite scene is an
*internal* compact quantum metric space — no external metric input. The continuum limit (that the
refinement sequence is GHP-Cauchy and its limit is a smooth Riemannian manifold) is the assumed
external owner; this refines the abstract Connes-reconstruction *confirmation*
(`D0-CONNES-RECONSTRUCTION-OWNER-001`) with the specific convergence framework. Connes
reconstruction identifies the *limit object* (a spectral triple is a spin manifold); Rieffel/GHP
own the *convergence to it*. D0 does NOT prove GHP-Cauchyness of the refinement sequence — that is
the explicit named residual. -/
structure RieffelGHPContinuum where
  /-- D0-side anchor: each finite scene is an internal compact quantum metric space (Connes
      distance = geodesic, `c=1=edge/tick`; cert-proved). -/
  d0FiniteInternalQuantumMetric : Prop
  /-- External: the refinement sequence is GHP-Cauchy and converges (Rieffel qGH + GHP) to a
      smooth compact Riemannian space. -/
  ghpCauchyConvergesToSmooth : Prop
  d0Witness : d0FiniteInternalQuantumMetric
  cited : ghpCauchyConvergesToSmooth

end BridgeAssumption

abbrev RieffelGHPContinuum := BridgeAssumption.RieffelGHPContinuum

/-- Conditional bridge: given the D0 finite internal quantum metric (Connes distance = geodesic on
each finite scene) and Rieffel quantum-Gromov–Hausdorff + GHP convergence (assumed), the finite
scene sequence converges to a smooth compact Riemannian space. Proved ONLY relative to the declared
external assumption (`ASSUMP-RIEFFEL-GHP`); the GHP-Cauchy proof for the D0 refinement sequence is
the named residual, not supplied here. -/
theorem rieffel_ghp_continuum_conditional (h : RieffelGHPContinuum) :
    h.d0FiniteInternalQuantumMetric ∧ h.ghpCauchyConvergesToSmooth :=
  ⟨h.d0Witness, h.cited⟩

end D0.Bridge
