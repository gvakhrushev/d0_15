import Mathlib.Tactic

/-!
# D0-V15 Work Package C — physical edge cover (CONDITIONAL-EXTENSION)

The edge carrier has frozen dimension `359 = |E|` (owner `D0-EDGE-ALPHA-001`, `D0.Spectral.ZetaResidueAlpha`).
The candidate physical edge cover has a return-edge holonomy `λ` entering the characteristic factor
`P(z;λ) = (1 − λ(z c_b)⁴)(1 − λ(z c_b)³)`. The coefficient of `z³` (at `c_b = 1`) is `−λ`, an injective
function of `λ`: distinct `λ` give **inequivalent** terminal observables (`cover_coeff_injective`). Nothing in
the frozen data — not symmetry, not unitarity, not the feedback `F` — pins `λ` to a unique value. Therefore the
physical edge cover is a **1-parameter family**, registered as

```
D0-EDGE-COVER-FAMILY-001 : CONDITIONAL-EXTENSION
missing : PRIM-EDGE-HOLONOMY-SELECTOR
```

NOT a present-core `THE`. (Halmos: every contraction admits a unitary dilation — an existence theorem — but
that does not single out a frozen physical edge operator; existence ≠ uniqueness.)
-/

namespace D0.Integration.V15.EdgeAudit

/-- Frozen edge-carrier dimension `|E| = 359`. -/
def edgeCarrierDim : ℕ := 359
theorem edge_dim : edgeCarrierDim = 359 := rfl

/-- The `z³` coefficient of the cover characteristic factor `(1 − λz⁴)(1 − λz³)` at `c_b = 1` is `−λ`. -/
def coverCoeffZ3 (lam : ℚ) : ℚ := -lam

/-- `λ` is recoverable from the observable (the map is injective) — yet it is not fixed by frozen data. -/
theorem cover_coeff_injective {a b : ℚ} (h : coverCoeffZ3 a = coverCoeffZ3 b) : a = b := by
  simpa [coverCoeffZ3] using h

/-- **C is a CONDITIONAL-EXTENSION.** Two holonomies `λ = 1, 2` give different cover observables, so the edge
cover is a genuine 1-parameter family; a frozen selector `PRIM-EDGE-HOLONOMY-SELECTOR` is required to make it a
theorem. -/
theorem edge_cover_is_family :
    edgeCarrierDim = 359 ∧ coverCoeffZ3 1 ≠ coverCoeffZ3 2 := by
  refine ⟨rfl, ?_⟩
  simp [coverCoeffZ3]

end D0.Integration.V15.EdgeAudit
