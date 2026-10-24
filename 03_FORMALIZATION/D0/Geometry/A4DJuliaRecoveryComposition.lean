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
open ExteriorAlgebra

noncomputable section

/-- Read the endpoint role map from the action of a finite-carrier query on
degree-one creator states above the vacuum. This decoder is defined for any
query operator; the recovery theorem below identifies its value on the full
exterior-frame lift. -/
def archiveExteriorFrameLiftRoleReadout
    (U : ArchiveJuliaQueryOperator) : RoleSpace → RoleSpace :=
  fun v => archiveJuliaVacuumVectorReadout
    (U (archiveExteriorCreator v (Pi.single fockVacuumState (1 : ℝ))))

/-- The full exterior-frame action determines its endpoint role map through
the same degree-one vacuum readout used by Eq. (26). -/
theorem archiveExteriorFrameLiftRoleReadout_frameLift
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveExteriorFrameLiftRoleReadout (archiveExteriorFrameLift M) = M := by
  funext v
  change ιInv (archiveFockExteriorEquiv
    (archiveExteriorFrameLift M
      (archiveExteriorCreator v (Pi.single fockVacuumState (1 : ℝ))))) = M v
  rw [archiveExteriorFrameLift_creator_covariant,
    archiveExteriorFrameLift_vacuum]
  rw [archiveExteriorCreator_on_vacuum_eq_ι]
  exact ExteriorAlgebra.ι_leftInverse (M v)

/-- Eq. (27) alone recovers the endpoint role map on its non-null chart. The
determinant-one hypothesis is used only by the owned Eq. (27) frame-lift
recovery; this degree-one readout adds no Eq. (28) covector or branch premise. -/
theorem archiveJuliaSourceCARRaisingQuery_nonNull_endpoint_map_recovery_of_det_one
    (u : RoleSpace) (M : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (hIso : ∀ x y, archiveJuliaSourceLorentzForm (M x) (M y) =
      archiveJuliaSourceLorentzForm x y)
    (hDet : LinearMap.det M.toLinearMap = 1)
    (hq : archiveJuliaSourceLorentzForm u u ≠ 0) :
    archiveExteriorFrameLiftRoleReadout
      ((archiveJuliaSourceLorentzForm u u)⁻¹ •
        (archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm u).comp
          (archiveJuliaCARRaisingQuery u M -
            archiveJuliaSourceVolumeEquiv.toLinearMap.comp
              ((archiveJuliaCARRaisingQuery u M).comp
                archiveJuliaSourceVolumeEquiv.symm.toLinearMap))) = M := by
  rw [← archiveJuliaSourceCARRaisingQuery_nonNull_gamma_recovery_of_det_one
    u M hIso hDet hq]
  exact archiveExteriorFrameLiftRoleReadout_frameLift M

/-- Symmetry of the source's fixed diagonal Lorentz form. -/
theorem archiveJuliaSourceLorentzForm_symmetric :
    ∀ x y, archiveJuliaSourceLorentzForm x y =
      archiveJuliaSourceLorentzForm y x := by
  intro x y
  change archiveJuliaSourceLorentzCovector x y =
    archiveJuliaSourceLorentzCovector y x
  simp [archiveJuliaSourceLorentzCovector, archiveRoleBasis,
    Module.Basis.coord, Finsupp.lapply_apply, smul_eq_mul, mul_comm]
  apply Finset.sum_congr rfl
  intro s hs
  ring

/-- Nondegeneracy of the source's fixed diagonal Lorentz form, proved from its
four nonzero diagonal coordinate signs. -/
theorem archiveJuliaSourceLorentzForm_nondegenerate :
    ∀ x, (∀ y, archiveJuliaSourceLorentzForm x y = 0) → x = 0 := by
  intro x hx
  ext r
  have hcoord : archiveJuliaSourceLorentzForm x (archiveRoleBasis r) =
      archiveJuliaSourceLorentzSign r * x r := by
    have hxexp : x = ∑ s : Role, x s • archiveRoleBasis s := by
      simpa [archiveRoleBasis, Pi.basisFun_repr] using
        (archiveRoleBasis.sum_repr x).symm
    calc
      archiveJuliaSourceLorentzForm x (archiveRoleBasis r) =
          archiveJuliaSourceLorentzForm
            (∑ s : Role, x s • archiveRoleBasis s) (archiveRoleBasis r) := by
              congr 1
              exact congrArg archiveJuliaSourceLorentzForm hxexp
      _ = ∑ s : Role,
          archiveJuliaSourceLorentzForm (x s • archiveRoleBasis s)
            (archiveRoleBasis r) := by
              rw [map_sum]
              rfl
      _ = ∑ s : Role, x s *
          archiveJuliaSourceLorentzForm (archiveRoleBasis s)
            (archiveRoleBasis r) := by
              apply Finset.sum_congr rfl
              intro s hs
              rw [map_smul]
              simp [LinearMap.smul_apply]
      _ = archiveJuliaSourceLorentzSign r * x r := by
              rw [Finset.sum_eq_single r]
              · rw [archiveJuliaSourceLorentzForm_basis_basis]
                simp
                ring
              · intro s hs hsr
                rw [archiveJuliaSourceLorentzForm_basis_basis]
                simp [hsr]
              · intro hr
                exact (hr (Finset.mem_univ r)).elim
  have hzero := hx (archiveRoleBasis r)
  rw [hcoord] at hzero
  have hsign : archiveJuliaSourceLorentzSign r ≠ 0 := by
    by_cases hr : r = A <;> simp [archiveJuliaSourceLorentzSign, hr]
  exact (mul_eq_zero.mp hzero).resolve_left hsign

/-- Every nonzero principal-frame shift lies in one of the two owned inverse
charts. Eq. (27) decodes the endpoint map when its source norm is nonzero. On
the null locus, nondegeneracy and the nonzero shift derive Eq. (28)'s projected
covector and positive-branch requirements internally. -/
theorem principalFrameJuliaQueryFamily_nonzero_shift_chart_coverage
    (F L : Matrix Role Role ℝ)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace)
    (α : Role → Module.Dual ℝ RoleSpace)
    (r : Role)
    (hIso : ∀ x y,
      archiveJuliaSourceLorentzForm ((M r) x) ((M r) y) =
        archiveJuliaSourceLorentzForm x y)
    (hα : α r ((principalFrameColumnMatrix F L).mulVec
      (Pi.single r (1 : ℝ))) = 1)
    (hu : (principalFrameColumnMatrix F L).mulVec
      (Pi.single r (1 : ℝ)) ≠ 0) :
    (archiveJuliaSourceLorentzForm
        ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ)))
        ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))) ≠ 0 ∧
      (LinearMap.det (M r).toLinearMap = 1 →
      archiveExteriorFrameLiftRoleReadout
        ((archiveJuliaSourceLorentzForm
          ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ)))
          ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))))⁻¹ •
          (archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm
            ((principalFrameColumnMatrix F L).mulVec
              (Pi.single r (1 : ℝ)))).comp
            (archiveJuliaCARRaisingQuery
                ((principalFrameColumnMatrix F L).mulVec
                  (Pi.single r (1 : ℝ))) (M r) -
              archiveJuliaSourceVolumeEquiv.toLinearMap.comp
                ((archiveJuliaCARRaisingQuery
                    ((principalFrameColumnMatrix F L).mulVec
                      (Pi.single r (1 : ℝ))) (M r)).comp
                  archiveJuliaSourceVolumeEquiv.symm.toLinearMap))) = M r)) ∨
    (archiveJuliaSourceLorentzForm
        ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ)))
        ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))) = 0 ∧
      principalFrameObservedNullQueryFrameReadout
        (fun _ => archiveJuliaSourceLorentzForm)
        (fun _ => archiveJuliaSourceLorentzForm)
        (principalFrameJuliaQueryFamily F L M) α r = M r) := by
  let u := (principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))
  by_cases hq : archiveJuliaSourceLorentzForm u u ≠ 0
  · left
    refine ⟨hq, ?_⟩
    intro hDet
    simpa [u] using
      archiveJuliaSourceCARRaisingQuery_nonNull_endpoint_map_recovery_of_det_one
        u (M r) hIso hDet hq
  · right
    have hq0 : archiveJuliaSourceLorentzForm u u = 0 := not_ne_iff.mp hq
    refine ⟨by simpa [u] using hq0, ?_⟩
    simpa [u] using principalFrameJuliaQueryFamily_null_link_recovery
      F L M (fun _ => archiveJuliaSourceLorentzForm)
      (fun _ => archiveJuliaSourceLorentzForm) α r
      archiveJuliaSourceLorentzForm_symmetric
      archiveJuliaSourceLorentzForm_nondegenerate hIso hα hu hq0

/-- Joint Eq. (27)/(28) application for one actual role query. The supplied
`hQuery` and `hColumn` bind the operator and full vacuum readout to the same
shift and endpoint map. The conclusion records the Eq. (28) endpoint decoder,
the Eq. (27) degree-one endpoint decoder, and the underlying all-grade
exterior-frame recovery. -/
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
    (archiveExteriorFrameLiftRoleReadout
      ((archiveJuliaSourceLorentzForm u u)⁻¹ •
        (archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm u).comp
          (X r - archiveJuliaSourceVolumeEquiv.toLinearMap.comp
            ((X r).comp archiveJuliaSourceVolumeEquiv.symm.toLinearMap))) = M) ∧
    (archiveExteriorFrameLift M =
      (archiveJuliaSourceLorentzForm u u)⁻¹ •
        (archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm u).comp
          (X r - archiveJuliaSourceVolumeEquiv.toLinearMap.comp
            ((X r).comp archiveJuliaSourceVolumeEquiv.symm.toLinearMap))) := by
  have hSymm : ∀ x y,
      archiveJuliaSourceLorentzForm x y =
        archiveJuliaSourceLorentzForm y x :=
    archiveJuliaSourceLorentzForm_symmetric
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
  have hEq27Readout : archiveExteriorFrameLiftRoleReadout
      ((archiveJuliaSourceLorentzForm u u)⁻¹ •
        (archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm u).comp
          (X r - archiveJuliaSourceVolumeEquiv.toLinearMap.comp
            ((X r).comp archiveJuliaSourceVolumeEquiv.symm.toLinearMap))) = M := by
    rw [← hEq27']
    exact archiveExteriorFrameLiftRoleReadout_frameLift M
  exact ⟨hEq28, hEq27Readout, hEq27'⟩

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
    (archiveExteriorFrameLiftRoleReadout
      ((archiveJuliaSourceLorentzForm
        ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ)))
        ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))))⁻¹ •
        (archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm
          ((principalFrameColumnMatrix F L).mulVec
            (Pi.single r (1 : ℝ)))).comp
          (principalFrameJuliaQueryFamily F L M r -
            archiveJuliaSourceVolumeEquiv.toLinearMap.comp
              ((principalFrameJuliaQueryFamily F L M r).comp
                archiveJuliaSourceVolumeEquiv.symm.toLinearMap))) = M r) ∧
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
