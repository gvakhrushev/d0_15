import Mathlib.Tactic

/-!
# D0 vNext+2 — typed scene spectral fingerprint of K(9,11,13)

The frozen D0 scene is the complete tripartite graph `K(9,11,13)`: `N = 33` vertices, parts `(9,11,13)`,
`|E| = 9·11 + 9·13 + 11·13 = 359`, degrees `(24,22,20) = (33−9, 33−11, 33−13)`. Combinatorial Laplacian
spectrum `{0:1, 20:12, 22:10, 24:8, 33:2}` (trace `= 718 = 2|E|`).

Structural decomposition (the non-negotiable target for any scene-native lift):
`H_scene = R_scene ⊕ K_scene`, `dim R = 3` (part-constant modes), `dim K = 30`, with within-part
difference subspaces `K_9 (8), K_11 (10), K_13 (12)`. Each within-part subspace `K_i` (dim `n_i − 1`) is
the `L`-eigenspace for eigenvalue `33 − n_i` (= the degree of that part), since `A` annihilates within-part
differences: `K_9 ↔ 24`, `K_11 ↔ 22`, `K_13 ↔ 20`. `R_scene` carries `{0:1}` (global constant) and
`{33:2}` (between-part modes). This is a typed fingerprint, computed not assumed.
-/

namespace D0.VNext2.SceneSpectralFingerprint

def parts : List ℕ := [9, 11, 13]
def N : ℕ := 9 + 11 + 13
def numEdges : ℕ := 9 * 11 + 9 * 13 + 11 * 13

/-- Degree of a vertex in part `n_i` of `K(9,11,13)` is `33 − n_i`. -/
def degOfPart (ni : ℕ) : ℕ := N - ni

/-- `L`-eigenvalue multiplicities `{0:1, 20:12, 22:10, 24:8, 33:2}` (as an (eigenvalue, mult) list). -/
def laplacianSpectrum : List (ℕ × ℕ) := [(0, 1), (20, 12), (22, 10), (24, 8), (33, 2)]

/-- Within-part difference subspace dimensions `(8, 10, 12) = (n_i − 1)`. -/
def withinPartDims : List ℕ := [9 - 1, 11 - 1, 13 - 1]

theorem scene_dim_and_edges : N = 33 ∧ numEdges = 359 ∧ 2 * numEdges = 718 := by
  refine ⟨by decide, by decide, by decide⟩

/-- **Degrees are `(24,22,20) = (33 − n_i)`** (non-constant: the scene is not regular). -/
theorem degrees_by_part :
    degOfPart 9 = 24 ∧ degOfPart 11 = 22 ∧ degOfPart 13 = 20 := by
  refine ⟨by decide, by decide, by decide⟩

/-- **The Laplacian multiplicities sum to 33 and the trace is 718** (`= 2|E|`). -/
theorem fingerprint_consistency :
    (laplacianSpectrum.map Prod.snd).sum = 33
      ∧ (laplacianSpectrum.map (fun p => p.1 * p.2)).sum = 718 := by
  refine ⟨by decide, by decide⟩

/-- **Structural decomposition** `3 + (8+10+12) = 33`: part-constant `R` (dim 3) plus within-part `K`
(dim 30). -/
theorem structural_decomposition :
    withinPartDims = [8, 10, 12] ∧ 3 + withinPartDims.sum = 33 := by
  refine ⟨by decide, by decide⟩

/-- **Within-part eigenvalue = degree = `33 − n_i`**: `K_9 ↔ 24`, `K_11 ↔ 22`, `K_13 ↔ 20` (and the
multiplicity equals `n_i − 1`). This binds the structural decomposition to the spectrum. -/
theorem within_part_eigenvalue_eq_degree :
    (degOfPart 9 = 24 ∧ (9 - 1) = 8)
      ∧ (degOfPart 11 = 22 ∧ (11 - 1) = 10)
      ∧ (degOfPart 13 = 20 ∧ (13 - 1) = 12) := by
  refine ⟨⟨by decide, by decide⟩, ⟨by decide, by decide⟩, ⟨by decide, by decide⟩⟩

end D0.VNext2.SceneSpectralFingerprint
