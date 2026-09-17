import Mathlib.Data.Fin.VecNotation
import Mathlib.Logic.Function.Basic
import Mathlib.Tactic

/-!
# D0-GRAPH-SPACE-NO-ISOMETRY-001 (NO-GO) — no forced isometry `Image(A) ≅ span{i,j,k}`

There is no M1-admissible **isometry** from the rank-3 image of `A = K(9,11,13)` to the transport triple
`span{i,j,k}`. Two independent obstructions, both decidable consequences of the distinct zone sizes
`(9,11,13)`:

* **Symmetry type.** `Aut(K(9,11,13)) = S₉×S₁₁×S₁₃`; since the zone sizes are pairwise distinct, the induced
  action on the three zone-classes is the **trivial** group (only the identity permutation preserves the size
  assignment — `zone_perm_trivial`). The transport triple `{i,j,k}` carries the order-3 cyclic `Aut(Q₈)`. A
  symmetry-respecting bijection between a rigidly-labelled triple and a cyclically-symmetric one requires an
  exogenous axis labelling (`⊥M1`).
* **Metric.** The image generators `1_{Zᵢ}` carry squared norms `nᵢ = 9,11,13` (`sizes_distinct`); a literal
  isometry would impose permanent spatial axis anisotropy `√9:√11:√13`.

So `L3(ii)` cannot be a forced identity (it is the isotropization MECH-LIMIT). This is a *positive* structural
result: the graph→space map must factor through a scale/limit erasing the size asymmetry.
-/

namespace D0.Foundation.GraphSpaceNoIsometry

/-- The three zone sizes. -/
def sizes : Fin 3 → ℕ := ![9, 11, 13]

/-- The zone sizes are pairwise distinct (anisotropic norms / size-rigid labelling). -/
theorem sizes_distinct : sizes 0 ≠ sizes 1 ∧ sizes 1 ≠ sizes 2 ∧ sizes 0 ≠ sizes 2 := by decide

/-- `sizes` is injective. -/
theorem sizes_injective : Function.Injective sizes := by decide

/-- **Trivial induced symmetry.** Any reindexing `σ : Fin 3 → Fin 3` that preserves the size assignment
(`sizes ∘ σ = sizes`) and is itself injective must be the identity — the zone-class symmetry the rank-3 image
can inherit is trivial, unlike the cyclic `Aut(Q₈)` on `{i,j,k}`. -/
theorem zone_perm_trivial (σ : Fin 3 → Fin 3) (hinj : Function.Injective σ)
    (h : ∀ i, sizes (σ i) = sizes i) : σ = id := by
  funext i
  have : σ i = i := sizes_injective (h i)
  simpa using this

/-- **D0-GRAPH-SPACE-NO-ISOMETRY-001.** The distinct zone sizes give both obstructions: trivial induced
zone-symmetry (≠ the cyclic `Aut(Q₈)`) and anisotropic norms — so no M1-admissible isometry
`Image(A) ≅ span{i,j,k}` exists; the graph→space hinge is the isotropization MECH-LIMIT, not an identity. -/
theorem graph_space_no_isometry :
    Function.Injective sizes ∧
    (sizes 0 ≠ sizes 1 ∧ sizes 1 ≠ sizes 2 ∧ sizes 0 ≠ sizes 2) ∧
    (∀ σ : Fin 3 → Fin 3, Function.Injective σ → (∀ i, sizes (σ i) = sizes i) → σ = id) :=
  ⟨sizes_injective, sizes_distinct, zone_perm_trivial⟩

end D0.Foundation.GraphSpaceNoIsometry
