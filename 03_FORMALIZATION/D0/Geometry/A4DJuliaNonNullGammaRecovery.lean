import D0.Geometry.ArchiveJuliaRaisingOperatorReadout

/-!
# Non-null Lorentz-Clifford recovery for the finite Julia query

This formalizes the algebraic inverse in Eq. (27) of the published #334 source
at commit `fe5cf335da04cac14e50407b03f98b96be17dc52`, path
`02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`,
blob `1c8d59e5533b443d9a015dc4512cfbc160ae7e62`, §8.4. The source consumer is
§5.1 of
`02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md`,
blob `734e21ae6bc04ff3446ad15858936d417fdd2e55`.

The gamma-square identity is derived from the existing creator/contraction
CAR on the full 16-state exterior carrier. The recovery theorem then composes
that identity with the exact finite query `C(u) ρ(M)`. Its two endpoint
Clifford identities remain explicit hypotheses: conjugating the creator by
the source volume element gives negative metric contraction, and the endpoint
volume elements intertwine the frame lift. They are not inferred from a
query name or from the desired recovered frame. Thus this is the compiled
Eq. (27) algebraic adapter; proving those identities for the source's
proper-Lorentz endpoint package and joining the non-null chart to Eq. (28)
remain separate work. It makes no physical admission or GR-selection claim.
-/

namespace D0.Geometry

noncomputable section

/-- The Lorentz-Clifford operator `C(u) + i_(P u)` on the owned finite
exterior carrier. `P u` is the metric-dual covector at the source endpoint. -/
def archiveJuliaLorentzGamma (P : ArchiveRoleBilinear) (u : RoleSpace) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  archiveExteriorCreatorLM u + archiveExteriorContraction (P u)

/-- The Clifford square on the full 16-state carrier is the endpoint quadratic
form. This follows from the existing creator/contraction CAR, not an assumed
square identity. -/
theorem archiveJuliaLorentzGamma_square (P : ArchiveRoleBilinear)
    (u : RoleSpace) :
    (archiveJuliaLorentzGamma P u).comp (archiveJuliaLorentzGamma P u) =
      (P u u) • LinearMap.id := by
  apply LinearMap.ext
  intro ψ
  let C := archiveExteriorCreatorLM u
  let I := archiveExteriorContraction (P u)
  have hC : C (C ψ) = 0 := by
    change archiveExteriorCreator u (archiveExteriorCreator u ψ) = 0
    have h := archiveExteriorCreator_anticommute u u ψ
    have hzero : (2 : ℝ) • archiveExteriorCreator u
        (archiveExteriorCreator u ψ) = 0 := by
      simpa [two_smul] using h
    rcases smul_eq_zero.mp hzero with htwo | hcc
    · norm_num at htwo
    · exact hcc
  have hI : I (I ψ) = 0 := by
    change archiveExteriorContraction (P u)
        (archiveExteriorContraction (P u) ψ) = 0
    have h := archiveExteriorContraction_anticommute (P u) (P u) ψ
    have hsum : archiveExteriorContraction (P u)
        (archiveExteriorContraction (P u) ψ) +
      archiveExteriorContraction (P u)
        (archiveExteriorContraction (P u) ψ) = 0 := by
      exact (add_eq_zero_iff_eq_neg).2 h
    have hzero : (2 : ℝ) • archiveExteriorContraction (P u)
        (archiveExteriorContraction (P u) ψ) = 0 := by
      simpa [two_smul] using hsum
    rcases smul_eq_zero.mp hzero with htwo | hii
    · norm_num at htwo
    · exact hii
  have hmixed : C (I ψ) + I (C ψ) = (P u u) • ψ := by
    change archiveExteriorCreator u
        (archiveExteriorContraction (P u) ψ) +
      archiveExteriorContraction (P u) (archiveExteriorCreator u ψ) =
        (P u u) • ψ
    rw [archiveExteriorContraction_creator]
    abel
  change (C + I) ((C + I) ψ) = (P u u) • ψ
  change C (C ψ + I ψ) + I (C ψ + I ψ) = (P u u) • ψ
  rw [map_add, map_add, hC, hI]
  simpa [add_zero, zero_add] using hmixed

/-- Eq. (27) on one actual finite-carrier Julia query. The endpoint volume
identities are explicit inputs; when they hold, the nonzero Lorentz norm
recovers the full frame lift on all 16 grades. -/
theorem archiveJuliaRaisingQuery_nonNull_gamma_recovery
    (P : ArchiveRoleBilinear) (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (χₓ χᵧ : (ArchiveFockState → ℝ) ≃ₗ[ℝ] (ArchiveFockState → ℝ))
    (hConjugation : χₓ.toLinearMap.comp
        ((archiveExteriorCreatorLM u).comp χₓ.symm.toLinearMap) =
      -(archiveExteriorContraction (P u)))
    (hEndpointCovariance : χₓ.toLinearMap.comp (archiveExteriorFrameLift M) =
      (archiveExteriorFrameLift M).comp χᵧ.toLinearMap)
    (hq : P u u ≠ 0) :
    archiveExteriorFrameLift M = (P u u)⁻¹ •
      (archiveJuliaLorentzGamma P u).comp
        (archiveJuliaRaisingQuery u M -
          χₓ.toLinearMap.comp
            ((archiveJuliaRaisingQuery u M).comp χᵧ.symm.toLinearMap)) := by
  let C := archiveExteriorCreatorLM u
  let I := archiveExteriorContraction (P u)
  let U := archiveExteriorFrameLift M
  let q := P u u
  have hTransportInverse : U.comp χᵧ.symm.toLinearMap =
      χₓ.symm.toLinearMap.comp U := by
    calc
      U.comp χᵧ.symm.toLinearMap =
          χₓ.symm.toLinearMap.comp
            ((χₓ.toLinearMap.comp U).comp χᵧ.symm.toLinearMap) := by
              simp [LinearMap.comp_assoc]
      _ = χₓ.symm.toLinearMap.comp
            ((U.comp χᵧ.toLinearMap).comp χᵧ.symm.toLinearMap) := by
              rw [hEndpointCovariance]
      _ = χₓ.symm.toLinearMap.comp U := by
            simp [LinearMap.comp_assoc]
  have hConjugationLocal :
      (χₓ.toLinearMap.comp C).comp χₓ.symm.toLinearMap = -I := by
    simpa [C, I, LinearMap.comp_assoc] using hConjugation
  have hConjugatedQuery :
      χₓ.toLinearMap.comp ((C.comp U).comp χᵧ.symm.toLinearMap) =
        -(I.comp U) := by
    calc
      χₓ.toLinearMap.comp ((C.comp U).comp χᵧ.symm.toLinearMap) =
          (χₓ.toLinearMap.comp C).comp
            (U.comp χᵧ.symm.toLinearMap) := by
              simp [LinearMap.comp_assoc]
      _ = (χₓ.toLinearMap.comp C).comp
            (χₓ.symm.toLinearMap.comp U) := by
              rw [hTransportInverse]
      _ = ((χₓ.toLinearMap.comp C).comp χₓ.symm.toLinearMap).comp U := by
            simp [LinearMap.comp_assoc]
      _ = -(I.comp U) := by
            rw [hConjugationLocal]
            simp
  have hDifference :
      archiveJuliaRaisingQuery u M -
          χₓ.toLinearMap.comp
            ((archiveJuliaRaisingQuery u M).comp χᵧ.symm.toLinearMap) =
        (archiveJuliaLorentzGamma P u).comp U := by
    change (C.comp U) -
        χₓ.toLinearMap.comp ((C.comp U).comp χᵧ.symm.toLinearMap) =
      (C + I).comp U
    rw [hConjugatedQuery]
    ext ψ
    simp [LinearMap.comp_assoc]
  have hGammaDifference :
      (archiveJuliaLorentzGamma P u).comp
          (archiveJuliaRaisingQuery u M -
            χₓ.toLinearMap.comp
              ((archiveJuliaRaisingQuery u M).comp χᵧ.symm.toLinearMap)) =
        q • U := by
    rw [hDifference]
    calc
      (archiveJuliaLorentzGamma P u).comp
          ((archiveJuliaLorentzGamma P u).comp U) =
        ((archiveJuliaLorentzGamma P u).comp
          (archiveJuliaLorentzGamma P u)).comp U := by
            simp [LinearMap.comp_assoc]
      _ = ((P u u) • LinearMap.id).comp U := by
            rw [archiveJuliaLorentzGamma_square]
      _ = q • U := by
        ext ψ
        simp [q]
  calc
    U = (q⁻¹ * q) • U := by
      rw [inv_mul_cancel₀ hq]
      simp
    _ = q⁻¹ • (q • U) := by rw [smul_smul]
    _ = q⁻¹ • (archiveJuliaLorentzGamma P u).comp
          (archiveJuliaRaisingQuery u M -
            χₓ.toLinearMap.comp
              ((archiveJuliaRaisingQuery u M).comp χᵧ.symm.toLinearMap)) := by
            rw [← hGammaDifference]
    _ = _ := rfl

/-- The same Eq. (27) recovery holds for the owned Jordan--Wigner query because
its complete 16-state operator equals the exterior-model query. -/
theorem archiveJuliaCARRaisingQuery_nonNull_gamma_recovery
    (P : ArchiveRoleBilinear) (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (χₓ χᵧ : (ArchiveFockState → ℝ) ≃ₗ[ℝ] (ArchiveFockState → ℝ))
    (hConjugation : χₓ.toLinearMap.comp
        ((archiveExteriorCreatorLM u).comp χₓ.symm.toLinearMap) =
      -(archiveExteriorContraction (P u)))
    (hEndpointCovariance : χₓ.toLinearMap.comp (archiveExteriorFrameLift M) =
      (archiveExteriorFrameLift M).comp χᵧ.toLinearMap)
    (hq : P u u ≠ 0) :
    archiveExteriorFrameLift M = (P u u)⁻¹ •
      (archiveJuliaLorentzGamma P u).comp
        (archiveJuliaCARRaisingQuery u M -
          χₓ.toLinearMap.comp
            ((archiveJuliaCARRaisingQuery u M).comp χᵧ.symm.toLinearMap)) := by
  rw [archiveJuliaCARRaisingQuery_eq_model]
  exact archiveJuliaRaisingQuery_nonNull_gamma_recovery
    P u M χₓ χᵧ hConjugation hEndpointCovariance hq

end
end D0.Geometry
