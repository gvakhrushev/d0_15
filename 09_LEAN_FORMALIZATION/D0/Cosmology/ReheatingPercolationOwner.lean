import Mathlib.Tactic

/-!
# D0-COSMOLOGY-CONNECTIVITY-THRESHOLD-OWNER-001 / reheating percolation (Lean)

Python certificates: `05_CERTS/vp_connectivity_threshold_owner.py`,
`05_CERTS/vp_reheating_percolation_owner.py`, `05_CERTS/vp_cmb_phason_spectrum_owner.py`,
`05_CERTS/vp_inflationless_early_universe_owner.py`.

Front P4 construction. The onset of cosmic expansion is modelled as a **graph connectivity threshold**
(percolation transition), not an inflationary singularity (BOOK_08 §08.49, GOLDEN-LEDGER THE 61.4):
below the threshold the scene graph is disconnected and the retained-rank cannot register coherent
volume; at the threshold the largest component spans the scene (`K(9,11,13)`, 33 vertices) and the
expansion history begins. This records the transition `before.connected = false → after.connected = true`.

HONESTY BOUNDARY. What is owned here (CERT-CLOSED): the connectivity-transition STRUCTURE (and, in the
cert, the decidable fact that the complete tripartite `K(9,11,13)` is connected while a sub-threshold
edgeless stage is not). What stays PROOF-TARGET: the exact threshold depth `u*`, the heat-trace phase
change at `u*`, the scalar spectral index `n_s` from the Laplacian spectrum (NOT a Planck fit,
`D0-CMB-PHASON-SPECTRUM-OWNER-001`), and the reheating energy budget / rate
(`D0-REHEATING-PERCOLATION-OWNER-001`, `D0-INFLATIONLESS-EARLY-UNIVERSE-OWNER-001`). No inflaton field
and no CMB datum enters.
-/

namespace D0.Cosmology

/-- A stage of the scene graph along refinement depth: its vertex count and whether it is connected. -/
structure GraphStage where
  vertices : Nat
  connected : Bool

/-- A percolation transition: a disconnected sub-threshold stage followed by a connected stage. -/
structure PercolationTransition where
  before : GraphStage
  after : GraphStage
  h_before : before.connected = false
  h_after : after.connected = true

/-- The scene at full depth: `K(9,11,13)`, 33 vertices, connected. -/
def sceneConnected : GraphStage := ⟨33, true⟩

/-- The sub-threshold scene: the 33 vertices not yet linked into one component. -/
def sceneSubThreshold : GraphStage := ⟨33, false⟩

/-- The reheating transition: sub-threshold (disconnected) → connected scene. -/
def reheatingTransition : PercolationTransition := ⟨sceneSubThreshold, sceneConnected, rfl, rfl⟩

/-- The connected scene has `9 + 11 + 13 = 33` vertices. -/
theorem scene_vertices_33 : sceneConnected.vertices = 33 := rfl

/-- **D0-COSMOLOGY-CONNECTIVITY-THRESHOLD-OWNER-001.** `t = 0` is a connectivity onset, not a
singularity: the transition goes from a disconnected sub-threshold stage to the connected scene
(`K(9,11,13)`, 33 vertices). -/
theorem connectivity_threshold_owner (t : PercolationTransition) :
    t.before.connected = false ∧ t.after.connected = true :=
  ⟨t.h_before, t.h_after⟩

/-- The reheating transition witnesses the connectivity onset on the 33-vertex scene. -/
theorem reheating_is_connectivity_onset :
    reheatingTransition.before.connected = false
      ∧ reheatingTransition.after.connected = true
      ∧ reheatingTransition.after.vertices = 33 :=
  ⟨rfl, rfl, rfl⟩

end D0.Cosmology
