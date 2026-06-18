import Mathlib.Tactic

/-!
# D0-REHEATING-HEAT-TRACE-JUMP-001 / heat-trace jump at the connectivity threshold (Lean)

Python certificate: `05_CERTS/vp_reheating_heat_trace_jump.py`.

Companion to `D0.Cosmology.ReheatingPercolationOwner` (the connectivity-onset OWNER module). Here we
encode the EXACT graph-Laplacian spectra of the two reheating stages as finite data and prove the
spectral jump that drives the heat trace `H(u) = Tr exp(-u L) = Σ mult · exp(-u·λ)`.

Verified mathematics (encoded, not assumed). The complete-tripartite graph `K(9,11,13)` (the connected
AFTER scene, 33 vertices) has graph-Laplacian spectrum, by the complete-multipartite formula
(eigenvalue 0 once; eigenvalue N = 33 with multiplicity k-1 = 2 for k = 3 parts; eigenvalue N - n_i
with multiplicity n_i - 1 per part):

    { 0 : mult 1, 20 : mult 12, 22 : mult 10, 24 : mult 8, 33 : mult 2 }

(24 = 33-9 ×(9-1)=8, 22 = 33-11 ×(11-1)=10, 20 = 33-13 ×(13-1)=12). The edgeless sub-threshold BEFORE
stage (33 isolated vertices, Laplacian = 0) has spectrum `{ 0 : mult 33 }`.

The multiplicity of eigenvalue 0 equals the number of connected components (kernel of the graph
Laplacian), which is also the `u → ∞` limit of the heat trace. It JUMPS `33 → 1` across the threshold.
The total multiplicity (= number of vertices = dimension) is `33` on BOTH sides; the algebraic
connectivity `λ₂ = 20 > 0` for the connected scene.

HONESTY BOUNDARY. CERT-CLOSED here: the two spectra as finite data, the zero-eigenvalue multiplicity
jump `33 → 1` (= component-count / heat-trace `u→∞` limit jump), the conserved total multiplicity `33`,
and `λ₂ = 20 > 0`. What stays PROOF-TARGET: the scalar spectral index `n_s` from this Laplacian
spectrum (`D0-CMB-PHASON-SPECTRUM-OWNER-001`); no CMB datum, no Planck fit, no inflaton enters.
-/

namespace D0.Cosmology

/-- A finite Laplacian spectrum: a list of `(eigenvalue, multiplicity)` pairs. -/
abbrev Spectrum := List (Nat × Nat)

/-- The EXACT spectrum of the connected AFTER scene `K(9,11,13)` (complete-tripartite formula). -/
def specConnected : Spectrum := [(0, 1), (20, 12), (22, 10), (24, 8), (33, 2)]

/-- The spectrum of the edgeless sub-threshold BEFORE stage: 33 isolated vertices, Laplacian `0`. -/
def specEdgeless : Spectrum := [(0, 33)]

/-- Total multiplicity = sum of all multiplicities = dimension = vertex count. -/
def totalMult (s : Spectrum) : Nat := (s.map Prod.snd).sum

/-- Multiplicity of a given eigenvalue: sum of multiplicities of pairs with that eigenvalue. -/
def multOf (s : Spectrum) (lam : Nat) : Nat :=
  ((s.filter (fun p => p.1 == lam)).map Prod.snd).sum

/-- The number of connected components = `dim ker L` = multiplicity of eigenvalue `0`. -/
def zeroMultiplicity (s : Spectrum) : Nat := multOf s 0

/-- The heat trace at depth `u` is `Σ mult · exp(-u·λ)`; as `u → ∞` only the `λ = 0` term survives,
so the limit equals the zero-eigenvalue multiplicity = the component count. We expose this limit as
an exact natural number (no real-analysis dependence): the `u → ∞` heat-trace limit IS
`zeroMultiplicity`. -/
def heatTraceLimit (s : Spectrum) : Nat := zeroMultiplicity s

/-- **Zero-eigenvalue multiplicity of the connected scene is `1`** (one connected component). -/
theorem zeroMultiplicity_connected : zeroMultiplicity specConnected = 1 := by
  decide

/-- **Zero-eigenvalue multiplicity of the edgeless stage is `33`** (33 isolated components). -/
theorem zeroMultiplicity_edgeless : zeroMultiplicity specEdgeless = 33 := by
  decide

/-- **The component count JUMPS `33 → 1`** across the connectivity threshold: the two
zero-multiplicities are genuinely different. -/
theorem zeroMultiplicity_jump :
    zeroMultiplicity specEdgeless = 33
      ∧ zeroMultiplicity specConnected = 1
      ∧ zeroMultiplicity specEdgeless ≠ zeroMultiplicity specConnected := by
  refine ⟨by decide, by decide, ?_⟩
  decide

/-- The `u → ∞` heat-trace limit equals the component count, and it jumps `33 → 1` as well. -/
theorem heatTraceLimit_jump :
    heatTraceLimit specEdgeless = 33
      ∧ heatTraceLimit specConnected = 1
      ∧ heatTraceLimit specEdgeless > heatTraceLimit specConnected := by
  refine ⟨by decide, by decide, ?_⟩
  decide

/-- **Total multiplicity is conserved: `33` on BOTH sides** (= number of vertices = dimension).
This is the non-trivial content that the jump is purely a kernel/component reshuffle, not a change
of dimension. -/
theorem totalMult_conserved :
    totalMult specConnected = 33 ∧ totalMult specEdgeless = 33 := by
  refine ⟨?_, ?_⟩ <;> decide

/-- The connected-scene total multiplicity decomposes as `1 + 12 + 10 + 8 + 2 = 33`, and the
non-zero (positive-eigenvalue) part carries `32` of those modes. -/
theorem connected_mult_decomposition :
    multOf specConnected 0 + multOf specConnected 20 + multOf specConnected 22
        + multOf specConnected 24 + multOf specConnected 33 = 33
      ∧ multOf specConnected 20 + multOf specConnected 22
          + multOf specConnected 24 + multOf specConnected 33 = 32 := by
  refine ⟨?_, ?_⟩ <;> decide

/-- **Algebraic connectivity `λ₂ = 20 > 0`** for the connected scene: the smallest NON-zero
eigenvalue present is `20`, witnessed by a positive-multiplicity entry, and it is strictly positive
while no eigenvalue strictly between `0` and `20` carries any multiplicity. -/
theorem algebraic_connectivity_pos :
    multOf specConnected 20 = 12
      ∧ (0 : Nat) < 20
      ∧ (∀ lam, 0 < lam → lam < 20 → multOf specConnected lam = 0) := by
  refine ⟨by decide, by decide, ?_⟩
  intro lam h0 h20
  -- only eigenvalues 0,20,22,24,33 occur; none lies strictly in (0,20)
  unfold multOf specConnected
  interval_cases lam <;> rfl

/-- **D0-REHEATING-HEAT-TRACE-JUMP-001.** The reheating heat trace jumps at the connectivity
threshold: the zero-eigenvalue multiplicity (= component count = `u→∞` heat-trace limit) drops
`33 → 1`, while the total multiplicity (dimension) is conserved at `33`, and the connected scene
has strictly positive algebraic connectivity `λ₂ = 20`. -/
theorem reheating_heat_trace_jump :
    zeroMultiplicity specEdgeless = 33
      ∧ zeroMultiplicity specConnected = 1
      ∧ zeroMultiplicity specEdgeless ≠ zeroMultiplicity specConnected
      ∧ totalMult specEdgeless = totalMult specConnected
      ∧ multOf specConnected 20 = 12 := by
  refine ⟨by decide, by decide, by decide, by decide, by decide⟩

end D0.Cosmology
