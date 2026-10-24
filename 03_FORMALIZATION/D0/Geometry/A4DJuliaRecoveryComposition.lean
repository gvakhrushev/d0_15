import D0.Geometry.A4DJuliaNonNullGammaRecovery
import D0.Geometry.A4DJuliaPrincipalFrameRecovery

/-!
# Composition of the non-null and open-chart Julia recoveries

This provides a shared application interface for the finite-carrier Eq. (27)
and Eq. (28) recoveries. The generic theorem requires explicit witnesses that
the same operator family has the stated raising-query representation and that
its complete vacuum readout returns the same input vector. The principal-frame
corollary supplies both maps from the owned query constructor.

The composition uses one common source Lorentz form at both endpoints,
determinant-one transport, nonzero source norm, and the open-chart covector
and positive-branch hypotheses. It does not extend Eq. (27) to distinct
endpoint forms, cover the null locus with Eq. (27), or establish that a
physical endpoint package satisfies these hypotheses.
-/

namespace D0.Geometry

open D0

noncomputable section

/-- Joint Eq. (27)/(28) application for one actual role query. The supplied
`hQuery` and `hColumn` bind the operator and full vacuum readout to the same
shift and endpoint map. The conclusion records both the endpoint map readout
and the all-grade exterior-frame recovery for that operator. -/
theorem archiveJuliaSourceQuery_nonNull_open_chart_joint_recovery
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (X : Role → ArchiveJuliaQueryOperator)
    (u : RoleSpace)
    (α : Role → Module.Dual ℝ RoleSpace)
    (r : Role)
    (hQuery : X r = archiveJuliaRaisingQuery u M)
    (hColumn : principalFrameObservedQueryVector X r = u)
    (hIso : ∀ x y,
      archiveJuliaSourceLorentzForm (M x) (M y) =
        archiveJuliaSourceLorentzForm x y)
    (hDet : LinearMap.det M.toLinearMap = 1)
    (hq : archiveJuliaSourceLorentzForm u u ≠ 0)
    (hα : α r u = 1)
    (hCovector : archiveJuliaQueryNullMetricCovector
      archiveJuliaSourceLorentzForm
      (principalFrameObservedQueryVector X r) (X r) (α r) ≠ 0)
    (hBranch : 0 < 1 +
      archiveJuliaSourceLorentzForm
        (principalFrameObservedQueryVector X r)
        (principalFrameObservedQueryVector X r) *
      α r (M (archiveJuliaQueryNullCanonicalWitness
        archiveJuliaSourceLorentzForm
        (principalFrameObservedQueryVector X r) (X r) (α r)))) :
    (principalFrameObservedNullQueryFrameReadout
      (fun _ => archiveJuliaSourceLorentzForm)
      (fun _ => archiveJuliaSourceLorentzForm) X α r = M) ∧
    (archiveExteriorFrameLift M =
      (archiveJuliaSourceLorentzForm u u)⁻¹ •
        (archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm u).comp
          (X r - archiveJuliaSourceVolumeEquiv.toLinearMap.comp
            ((X r).comp archiveJuliaSourceVolumeEquiv.symm.toLinearMap))) := by
  have hSymm : ∀ x y,
      archiveJuliaSourceLorentzForm x y =
        archiveJuliaSourceLorentzForm y x := by
    intro x y
    change archiveJuliaSourceLorentzCovector x y =
      archiveJuliaSourceLorentzCovector y x
    simp [archiveJuliaSourceLorentzCovector, archiveRoleBasis,
      Module.Basis.coord, Finsupp.lapply_apply, smul_eq_mul, mul_comm]
    apply Finset.sum_congr rfl
    intro s hs
    ring
  have hQueryModel : X r = archiveJuliaRaisingQuery u M := hQuery
  have hQueryCAR : X r = archiveJuliaCARRaisingQuery u M := by
    calc
      X r = archiveJuliaRaisingQuery u M := hQueryModel
      _ = archiveJuliaCARRaisingQuery u M :=
        (archiveJuliaCARRaisingQuery_eq_model u M).symm
  have hEq28 := principalFrameObservedQuery_open_chart_link_recovery
    M (fun _ => archiveJuliaSourceLorentzForm)
      (fun _ => archiveJuliaSourceLorentzForm) X u α r
      hQueryModel hColumn hα hSymm hIso hCovector hBranch
  have hEq27 := archiveJuliaSourceCARRaisingQuery_nonNull_gamma_recovery_of_det_one
    u M hIso hDet hq
  have hEq27' : archiveExteriorFrameLift M =
      (archiveJuliaSourceLorentzForm u u)⁻¹ •
        (archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm u).comp
          (X r - archiveJuliaSourceVolumeEquiv.toLinearMap.comp
            ((X r).comp archiveJuliaSourceVolumeEquiv.symm.toLinearMap)) := by
    simpa only [← hQueryCAR] using hEq27
  exact ⟨hEq28, hEq27'⟩

/-- Concrete principal-frame instance of the joint recovery. Eq. (26)'s
vacuum readout supplies `hColumn`, and the owned constructor supplies the
complete CAR raising query; all endpoint and open-chart conditions remain
explicit. -/
theorem principalFrameJuliaQueryFamily_nonNull_open_chart_joint_recovery
    (F L : Matrix Role Role ℝ)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace)
    (α : Role → Module.Dual ℝ RoleSpace)
    (r : Role)
    (hIso : ∀ x y,
      archiveJuliaSourceLorentzForm ((M r) x) ((M r) y) =
        archiveJuliaSourceLorentzForm x y)
    (hDet : LinearMap.det (M r).toLinearMap = 1)
    (hInputNorm : archiveJuliaSourceLorentzForm
      ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ)))
      ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))) ≠ 0)
    (hα : α r ((principalFrameColumnMatrix F L).mulVec
      (Pi.single r (1 : ℝ))) = 1)
    (hCovector : archiveJuliaQueryNullMetricCovector
      archiveJuliaSourceLorentzForm
      (principalFrameObservedQueryVector
        (principalFrameJuliaQueryFamily F L M) r)
      (principalFrameJuliaQueryFamily F L M r) (α r) ≠ 0)
    (hBranch : 0 < 1 +
      archiveJuliaSourceLorentzForm
        (principalFrameObservedQueryVector
          (principalFrameJuliaQueryFamily F L M) r)
        (principalFrameObservedQueryVector
          (principalFrameJuliaQueryFamily F L M) r) *
      α r ((M r) (archiveJuliaQueryNullCanonicalWitness
        archiveJuliaSourceLorentzForm
        (principalFrameObservedQueryVector
          (principalFrameJuliaQueryFamily F L M) r)
        (principalFrameJuliaQueryFamily F L M r) (α r)))) :
    (principalFrameObservedNullQueryFrameReadout
      (fun _ => archiveJuliaSourceLorentzForm)
      (fun _ => archiveJuliaSourceLorentzForm)
      (principalFrameJuliaQueryFamily F L M) α r = M r) ∧
    (archiveExteriorFrameLift (M r) =
      (archiveJuliaSourceLorentzForm
        ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ)))
        ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))))⁻¹ •
        (archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm
          ((principalFrameColumnMatrix F L).mulVec
            (Pi.single r (1 : ℝ)))).comp
          (principalFrameJuliaQueryFamily F L M r -
            archiveJuliaSourceVolumeEquiv.toLinearMap.comp
              ((principalFrameJuliaQueryFamily F L M r).comp
                archiveJuliaSourceVolumeEquiv.symm.toLinearMap))) := by
  have hQuery : principalFrameJuliaQueryFamily F L M r =
      archiveJuliaRaisingQuery
        ((principalFrameColumnMatrix F L).mulVec
          (Pi.single r (1 : ℝ))) (M r) :=
    principalFrameJuliaQueryFamily_eq_model F L M r
  have hColumn : principalFrameObservedQueryVector
      (principalFrameJuliaQueryFamily F L M) r =
        (principalFrameColumnMatrix F L).mulVec
          (Pi.single r (1 : ℝ)) := by
    exact principalFrameObservedQueryVector_eq F L M
      (principalFrameJuliaQueryFamily F L M)
      (principalFrameJuliaQueryFamily_eq_model F L M) r
  have hJoint := archiveJuliaSourceQuery_nonNull_open_chart_joint_recovery
    (M r) (principalFrameJuliaQueryFamily F L M)
      ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ)))
      α r hQuery hColumn hIso hDet hInputNorm hα hCovector hBranch
  exact hJoint

end
end D0.Geometry
