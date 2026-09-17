import Mathlib.Tactic

/-!
# D0-SCENE-LAPLACIAN-SPECTRUM-FORCED-001 — the whole Laplacian spectrum is the multipartite closed form

For the complete `k`-partite graph `K(n₁,…,n_k)` with `N = Σ nᵢ`, the graph Laplacian `L = D − A` has the
closed-form spectrum
* `0` with multiplicity `1` (the all-ones kernel mode),
* `N − nᵢ` with multiplicity `nᵢ − 1` for each zone `i` (within-zone sum-zero modes),
* `N` with multiplicity `k − 1` (zone-constant sum-zero modes).

The multiplicities total `1 + Σ(nᵢ − 1) + (k − 1) = N`. For the scene `K(9,11,13)` this is
`0¹, 24⁸, 22¹⁰, 20¹², 33²` — the entire spectrum forced by the three `+2`-spaced zones, with no fit.

This file records the arithmetic backbone: the eigenvalues as `N − nᵢ`, the multiplicity bookkeeping
totalling `N`, the edge count `|E| = (N² − Σnᵢ²)/2 = 359`, the nullity `Σ(nᵢ−1) = 30 = N − k`, and the
trace `Σ deg = 2|E| = 718`. The full explicit-eigenvector proof (that these are the *only* eigenvalues) is
carried in the failable cert `vp_scene_laplacian_spectrum_forced.py`; here we fix the closed-form data and
its internal consistency.

Honest scope: `30 = N − k` has no Fibonacci form, and `359` is prime (the `α_top` coefficient); no `φ`
structure is asserted for either. The `+2`-graded even-Fibonacci story is the *separate*
`D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001` (dimension only).
-/

namespace D0.VNext2.SceneLaplacianSpectrumForced

/-- Zone sizes of the scene, a `+2` arithmetic progression. -/
def n₁ : ℕ := 9
def n₂ : ℕ := 11
def n₃ : ℕ := 13

/-- Vertex count. -/
def Nv : ℕ := n₁ + n₂ + n₃

/-- Number of parts. -/
def kParts : ℕ := 3

theorem N_eq : Nv = 33 := by decide

/-- Zones are the `+2` progression. -/
theorem zones_plus_two : n₂ - n₁ = 2 ∧ n₃ - n₂ = 2 := by decide

/-- The three nonzero-non-top eigenvalues are `N − nᵢ = 24, 22, 20`. -/
theorem zone_eigenvalues : (Nv - n₁, Nv - n₂, Nv - n₃) = (24, 22, 20) := by decide

/-- Multiplicity bookkeeping: `1 + Σ(nᵢ − 1) + (k − 1) = N`. -/
theorem multiplicities_total :
    1 + ((n₁ - 1) + (n₂ - 1) + (n₃ - 1)) + (kParts - 1) = Nv := by decide

/-- The per-eigenvalue multiplicities are `{0↦1, 24↦8, 22↦10, 20↦12, 33↦2}`. -/
theorem eigenvalue_multiplicities :
    (1, n₁ - 1, n₂ - 1, n₃ - 1, kParts - 1) = (1, 8, 10, 12, 2) := by decide

/-- Edge count `|E| = (N² − Σnᵢ²)/2 = 359`. -/
theorem edge_count : (Nv ^ 2 - (n₁ ^ 2 + n₂ ^ 2 + n₃ ^ 2)) / 2 = 359 := by decide

/-- Nullity of the adjacency `= Σ(nᵢ − 1) = 30 = N − k` (the dark archive). -/
theorem nullity_eq : (n₁ - 1) + (n₂ - 1) + (n₃ - 1) = 30 ∧ (30 : ℕ) = Nv - kParts := by
  constructor <;> decide

/-- Trace of the Laplacian equals `2|E|`: `Σ (N − nᵢ)·nᵢ = 2·359 = 718`. -/
theorem trace_eq_two_edges :
    (Nv - n₁) * n₁ + (Nv - n₂) * n₂ + (Nv - n₃) * n₃ = 2 * 359 := by decide

/-- Honest rejection: `30` is not a Fibonacci number (no `φ` closed form for the nullity). -/
theorem nullity_not_fibonacci : ∀ m ≤ 12, Nat.fib m ≠ 30 := by decide

/-- Honest rejection: `359` is prime (it is the `α_top` coefficient, not a Fibonacci number). -/
theorem edges_prime : Nat.Prime 359 := by norm_num

end D0.VNext2.SceneLaplacianSpectrumForced
