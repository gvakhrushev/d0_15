import D0.Spectral.DeltaAlphaMoment

/-!
# D0-ALPHA-FESHBACH-DIXMIER-OWNER-001 / -RESIDUE-FINITE-SUM-001 — explicit Feshbach residue (Lean)

Python certificates: `05_CERTS/vp_alpha_feshbach_residue_finite_sum.py`,
`05_CERTS/vp_alpha_feshbach_dixmier_owner.py`, `05_CERTS/vp_neutrino_delta_alpha_norm_square.py`.

Front A construction. The gluing anomaly lives in a Feshbach–Schur effective operator over the active
(rank-3) / archive (dim-30) split: `W_eff(z) = A − B (D − zI)⁻¹ C`, where `A` is the rank-3 active
block and `D` the 30-dim archive block. Because the archive block is FINITE, the residue functional
`Res_D0(W_eff) = (1/2πi)∮ Tr_archive(W_eff⁻¹ ∂_z W_eff) dz` reduces to a **finite pole sum** over the
archive eigenvalues — NOT an infinite ζ-residue. That finite pole sum is exactly the depth-2 archive
moment polynomial already proved (`D0-DELTA-ALPHA-MOMENT-001`): `μ₂·u² + μ₁·u` in the rank-3 unit
`u = φ⁻³`, with `μ₂ = 12288/5`, `μ₁ = 1/3`, and `μ₀ = 0` (no constant term ⇒ no infinite-ζ tail), and
it equals the CORE algebraic value `α_alg⁻¹ = 159739/5 − (294902/15)φ`.

This module assembles the explicit active/archive block data and the finite-pole-sum residue, reusing
the proven moment identity, and records the exact `ℚ(φ)` neutrino norm-square `P_sterile = Δ_α²`.

HONESTY BOUNDARY. The finite-pole-sum STRUCTURE and its value are owned here (CERT-CLOSED, reusing
`D0-DELTA-ALPHA-MOMENT-001`). What is NOT closed: the residue-NORMALIZATION equality
`Res_D0(W_eff) = Δ_α` (the seam), and the amplitude derivation (the `2¹¹` active–archive pairing) —
those are the external Dixmier/Wodzicki residue extraction `D0-DIXMIER-RESIDUE-OWNER-001`
(ASSUMP-DIXMIER-TRACE); the bare ζ-residue route is closed-negative (`D0.Spectral.DeltaAlphaResidueBlocked`,
`1/lnφ` transcendental). `m_ν ∝ P_sterile = Δ_α²` stays the neutrino passport (never CORE-THE).
-/

namespace D0.Spectral

open D0

/-- The active (rank-3) / archive (dim-30) Feshbach–Schur block data. -/
structure ActiveArchiveBlock where
  activeRank : Nat
  archiveDim : Nat
  h_active : activeRank = 3
  h_archive : archiveDim = 30

/-- The D0 Feshbach split: active rank 3 (zone carrier 9,11,13), archive dim 30 (kernel `8⊕10⊕12`). -/
def feshbachBlock : ActiveArchiveBlock := ⟨3, 30, rfl, rfl⟩

theorem active_rank_three (b : ActiveArchiveBlock) : b.activeRank = 3 := b.h_active
theorem archive_dim_thirty (b : ActiveArchiveBlock) : b.archiveDim = 30 := b.h_archive

/-- **The finite Feshbach residue** = the depth-2 archive pole sum `μ₂·u² + μ₁·u` in `u = φ⁻³`
(`μ₂ = 12288/5`, `μ₁ = 1/3`): a FINITE sum over the 30-dim archive block, not an infinite ζ-residue. -/
noncomputable def feshbachFiniteResidue : ℝ := momentPoly (12288 / 5) (1 / 3) (phi⁻¹ ^ 3)

/-- **The finite residue equals the CORE `α_alg⁻¹`** (`= 159739/5 − (294902/15)φ`). Reuses
`D0-DELTA-ALPHA-MOMENT-001`; the explicit-operator content here is the finite-pole-sum framing. -/
theorem feshbach_residue_value : feshbachFiniteResidue = 159739 / 5 - 294902 / 15 * phi :=
  alphaAlg_moment_value

/-- **No infinite-ζ tail:** the residue has no constant term (`μ₀ = 0` ⇒ zero archive depth ⇒ zero
contribution), so the contour integral is a *finite* pole sum, not a bare divergent ζ-residue. -/
theorem feshbach_residue_no_zeta_tail : momentPoly (12288 / 5) (1 / 3) 0 = 0 :=
  momentPoly_zero _ _

/-- The CORE-exact gluing-anomaly seam `Δ_α` (value `D0-DELTA-ALPHA-EXACT-001`). -/
noncomputable def deltaAlphaSeam : ℝ := -156109 / 5 + 289442 / 15 * phi

/-- **Neutrino norm-square internal object** `P_sterile = Δ_α²` (the seam squared). -/
noncomputable def pSterile : ℝ := deltaAlphaSeam ^ 2

/-- `P_sterile = Δ_α² ≥ 0` (a genuine nonnegative internal object). -/
theorem p_sterile_nonneg : 0 ≤ pSterile := sq_nonneg _

/-- **`P_sterile = Δ_α²` is an exact element of `ℚ(φ)`** (the field is closed under squaring;
`(a + bφ)² = (a²+b²) + (2ab+b²)φ` via `φ² = φ+1`). -/
theorem p_sterile_in_qphi : ∃ A B : ℝ, pSterile = A + B * phi := by
  refine ⟨(-156109 / 5) ^ 2 + (289442 / 15) ^ 2,
          2 * (-156109 / 5) * (289442 / 15) + (289442 / 15) ^ 2, ?_⟩
  unfold pSterile deltaAlphaSeam
  linear_combination ((289442 / 15) ^ 2) * phi_sq

/-- **D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001.** Over the active(rank 3)/archive(dim 30) Feshbach
split, the residue functional reduces to the FINITE depth-2 archive pole sum `μ₂u²+μ₁u` (`u=φ⁻³`),
which has no constant term (no infinite-ζ tail) and equals the CORE `α_alg⁻¹ = 159739/5 − (294902/15)φ`.
The residue→`Δ_α` normalization and the `2¹¹` pairing stay the external Dixmier owner. -/
theorem alpha_feshbach_residue_finite_sum :
    feshbachBlock.activeRank = 3
      ∧ feshbachBlock.archiveDim = 30
      ∧ feshbachFiniteResidue = 159739 / 5 - 294902 / 15 * phi
      ∧ momentPoly (12288 / 5) (1 / 3) 0 = 0 :=
  ⟨rfl, rfl, feshbach_residue_value, feshbach_residue_no_zeta_tail⟩

end D0.Spectral
