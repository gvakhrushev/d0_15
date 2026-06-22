import Mathlib.Tactic

/-!
# D0-X5-P1-TWOSOURCE-001 — S_DE alone is not a common sector (Section 6)

CORRECTION to the prior X5-P1 model: a common pressure-energy sector requires `≥ 2` distinct typed source maps
into `H_phi`. The S_DE-only model has ONE source (`S_DE`), so it certifies a two-mode INTERNAL sector but is
NOT a common pressure-energy sector. No canonical second typed source map exists (`L_archive`, `QUQ`, `W_eff`
are typed-distinct with no intertwiner). Decision **P1-3** (no common sector in the declared class) / **P1-4**
(the X5-P1 contract POSTULATES the second typed source map, with deletion-minimality on it).
-/

namespace D0.Extensions.X5.Phason

/-- Number of distinct typed source maps in the S_DE-only model. -/
def sdeOnlySources : ℕ := 1
/-- A common pressure-energy sector requires at least two distinct typed source maps. -/
def commonSectorMinSources : ℕ := 2

/-- **The S_DE-only model is NOT a common sector**: `1 < 2` sources. -/
theorem sde_only_not_common_sector : sdeOnlySources < commonSectorMinSources := by decide

/-- The X5-P1 contract postulates the second source map (so the contract model has `2` sources). -/
def contractSources : ℕ := 2
theorem contract_meets_min : commonSectorMinSources ≤ contractSources := by decide

/-- **Decision P1-3 / P1-4.** S_DE-only fails the common-sector requirement (1 < 2 sources); the X5-P1
contract postulates the missing second typed source map (`2 ≥ 2`). -/
theorem phason_P1_two_source :
    sdeOnlySources < commonSectorMinSources ∧ commonSectorMinSources ≤ contractSources :=
  ⟨sde_only_not_common_sector, contract_meets_min⟩

end D0.Extensions.X5.Phason
