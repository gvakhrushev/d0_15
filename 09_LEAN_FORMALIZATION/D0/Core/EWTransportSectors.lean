import Mathlib.Tactic
import D0.Core.DyadABCD

/-!
# D0-EW-TRANSPORT-SECTORS-001 — the EW transport depth is φ⁻¹², closing the α depth decomposition

The α closure holonomy (`D0-ALPHA-HOLONOMY-002`, BOOK_02 §02.13.h) uses the depth
`φ⁻¹⁷ = φ⁻⁵ · φ⁻¹²` — "the seam ξ₅ times the electroweak transport".  The ξ₅ leg was owned
(`D0-XI5-TORUS-DEFECT-001`); the φ⁻¹² leg had NO owner — the one soft joint of the flagship
chain (flagged by the 2026 session audit).  This module supplies it.

**The sector count.**  The electroweak transport crossing zone `V₁₁` registers at every vertex
of the zone and carries exactly one directed seam-crossing bit:

* no-skip (M1): skipping any vertex requires a selection rule over `V₁₁`'s elements — an
  exogenous catalog, forbidden; hence ALL of `V₁₁` registers;
* single directed crossing: the CP-seam is crossed exactly once per closure (`N² = 0`, owned by
  the directed CP-3-cycle of `D0-BARYON-ASYMMETRY-DELTA0-001`) — that crossing is itself one
  sector.

Hence `N_EW = |V₁₁| + 1`.  The capacity ladder owns the pieces: `|Ω₈| = 8` (§01.7),
`|V₉| = |Ω₈| + 1 = 9` (graph-birth basepoint ω₀, §01.8), `V₁₁ = V₉ ⊔ D₂` with
`|D₂| = 2` ⇒ `|V₁₁| = 11` (§01.20, count-certified by `vp_v1141_abcd_omega8_v9_phi_capacity.py`).
Therefore `N_EW = 12`.

**Depth identity.**  The transport depth is the φ-weight of the sector count,
`φ⁻N_EW = φ⁻¹²`; composed with the seam ξ₅ = φ⁻⁵:

    φ⁻⁵ · φ⁻¹² = φ⁻¹⁷,

which is exactly the depth entering `vp_seam_holonomy_alpha.py`.  The decomposition is an exact
identity in ℚ(φ) — nothing numeric is new here; what is new is that BOTH factors now have owners.

Honest scope: the M1 no-skip principle and the single-directed-crossing input are cited from
their owners (M1 axiom §00; `D0-BARYON-ASYMMETRY-DELTA0-001`), not re-derived here; this module
owns the COUNTING layer (capacity chain + depth composition) and thereby discharges the unowned
φ⁻¹² leg at candidate grade, pending the standard independent-skeptic pass before any registry
promotion beyond CERT-CLOSED.
-/

namespace D0

/-- Owned capacity ladder (BOOK_01 §01.7–§01.20): the zone cardinalities as natural numbers. -/
def omega8Card : ℕ := 8
def dyadCard : ℕ := 2

theorem v9_card : omega8Card + 1 = 9 := rfl

theorem v11_card : omega8Card + 1 + dyadCard = 11 := by
  unfold omega8Card dyadCard
  norm_num

/-- **The electroweak transport sector count**: all of V₁₁ (no-skip under M1) plus the single
    directed seam-crossing bit. -/
def ewSectorCount : ℕ := omega8Card + 1 + dyadCard + 1

theorem ew_sector_count_value : ewSectorCount = 12 := by
  simp only [ewSectorCount, omega8Card, dyadCard]

/-! ### Depth composition -/

/-- The two depth factors compose into the holonomy depth: exact in ℚ(φ). -/
theorem ew_depth_composition (φ : ℝ) (hφ1 : (1 : ℝ) < φ) :
    φ ^ (-5 : ℤ) * φ ^ (-12 : ℤ) = φ ^ (-17 : ℤ) := by
  have hφ0 : φ ≠ 0 := ne_of_gt (by linarith)
  rw [← zpow_add₀ hφ0]
  ring

/-- The transport depth factor equals φ⁻¹² given the forced sector count. -/
theorem ew_depth_is_twelve (φ : ℝ) :
    φ ^ (-(ewSectorCount : ℤ)) = φ ^ (-12 : ℤ) := by
  rw [ew_sector_count_value]
  push_cast
  ring_nf

end D0
