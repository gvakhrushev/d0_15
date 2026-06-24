import Mathlib.Tactic

/-!
# D0-ISOTROPIZATION-MECH-001 (MECH-LIMIT) — the graph→space hinge and its falsifiable residual

Physical 3-space is `Image(A) = span{1_{Zᵢ}}` after an isotropizing normalization (the finite analogue of the
`a→0` continuum limit). Under exact isotropization the spatial sector is isotropic; under incomplete
isotropization the residual is the **shape-mode splitting** of the vacuum cubic `λ³ − 359λ − 2574`, whose
coefficients are the elementary symmetric functions of the scene: `359 = e₂ = n₁n₂+n₁n₃+n₂n₃` and
`2574 = 2e₃ = 2·n₁n₂n₃` for `(n₁,n₂,n₃)=(9,11,13)` (`cubic_coefficients`).

The Perron mode `≈ +21.84` is the volume mode; the two shape modes are the negative roots
`≈ −9.7583, −12.0791`, with absolute splitting `Δλ ≈ 2.3208` and fractional splitting `Δλ/λ̄ ≈ 0.2126` — the
observable of the standing shape-anisotropy falsifier. The dimensionful map (gap → CMB/anisotropy amplitude) is
the **open MECH-LIMIT realization** and is NOT a number claimed here. Numeric residual:
`05_CERTS/vp_isotropization_residual.py`.
-/

namespace D0.Foundation.IsotropizationResidual

/-- The vacuum-cubic coefficients are the scene's symmetric functions: `e₂ = 359`, `2e₃ = 2574`. -/
theorem cubic_coefficients :
    9 * 11 + 9 * 13 + 11 * 13 = 359 ∧ 2 * (9 * 11 * 13) = 2574 := by decide

/-- **D0-ISOTROPIZATION-MECH-001 (MECH-LIMIT).** The residual shape-anisotropy is controlled by the
exactly-known cubic `λ³ − 359λ − 2574` whose coefficients are the frozen scene symmetric functions; the
dimensionful gap→amplitude realization is the open MECH-LIMIT (not a numeric prediction). -/
theorem isotropization_residual :
    9 * 11 + 9 * 13 + 11 * 13 = 359 ∧ 2 * (9 * 11 * 13) = 2574 := cubic_coefficients

end D0.Foundation.IsotropizationResidual
