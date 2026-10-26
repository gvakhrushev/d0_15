import D0.Geometry.A4DJuliaRecoveryComposition
import Mathlib.Analysis.Calculus.FDeriv.Linear

/-!
# Pathwise differential recovery for Julia endpoint links

This module composes the owned Eq. (27)/(28) endpoint charts with a
differentiable path of actual role-indexed proper-Lorentz endpoint maps. The
coframe and normalized source covector may vary with the endpoint path, while
each endpoint path may vary independently by role. Exact chart recovery
transfers the endpoint derivative through the same finite-carrier Julia query
and chart-selected endpoint readout.

This is a directional composition result on the declared open-chart domain.
It does not construct a 24-dimensional Lorentz chart, prove every tangent is
integrable in Lean, or establish physical admission or price/source
selection.
-/

namespace D0.Geometry

open D0

noncomputable section

/-- Select the owned Julia endpoint decoder on its valid chart: Eq. (27) for a
non-null source shift and the observed-query Eq. (28) decoder on the null
locus. The source shift and query family are explicit inputs. -/
def principalFrameJuliaEndpointChartReadout
    (u : RoleSpace)
    (X : Role → ArchiveJuliaQueryOperator)
    (α : Role → Module.Dual ℝ RoleSpace)
    (r : Role) : RoleSpace → RoleSpace :=
  fun x => if archiveJuliaSourceLorentzForm u u ≠ 0 then
      archiveJuliaSourceEq27EndpointMapReadout u (X r) x
    else
      principalFrameObservedNullQueryFrameReadout
        (fun _ => archiveJuliaSourceLorentzForm)
        (fun _ => archiveJuliaSourceLorentzForm) X α r x

/-- On either owned endpoint chart, the selected readout recovers the same
proper-Lorentz endpoint map used to construct the actual Julia query. The
two-chart coverage theorem supplies Eq. (27) away from the null locus and
derives Eq. (28)'s projected-covector and branch conditions at a nonzero null
shift. -/
theorem principalFrameJuliaEndpointChartReadout_eq
    (F L : Matrix Role Role ℝ)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace)
    (α : Role → Module.Dual ℝ RoleSpace)
    (hIso : ∀ r x y,
      archiveJuliaSourceLorentzForm ((M r) x) ((M r) y) =
        archiveJuliaSourceLorentzForm x y)
    (hDet : ∀ r, LinearMap.det (M r).toLinearMap = 1)
    (hAlpha : ∀ r,
      α r ((principalFrameColumnMatrix F L).mulVec
        (Pi.single r (1 : ℝ))) = 1)
    (hShift : ∀ r,
      (principalFrameColumnMatrix F L).mulVec
        (Pi.single r (1 : ℝ)) ≠ 0)
    (r : Role) :
    principalFrameJuliaEndpointChartReadout
      ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ)))
      (principalFrameJuliaQueryFamily F L M) α r = M r := by
  funext x
  dsimp [principalFrameJuliaEndpointChartReadout]
  by_cases hq : archiveJuliaSourceLorentzForm
      ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ)))
      ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))) ≠ 0
  · simp only [if_pos hq]
    have hCoverage := principalFrameJuliaQueryFamily_nonzero_shift_chart_coverage
      F L M α r (hIso r) (hAlpha r) (hShift r)
    rcases hCoverage with ⟨_, hReadout⟩ | ⟨hNull, _⟩
    · exact congrFun (hReadout (hDet r)) x
    · exact (hq hNull).elim
  · simp only [if_neg hq]
    have hCoverage := principalFrameJuliaQueryFamily_nonzero_shift_chart_coverage
      F L M α r (hIso r) (hAlpha r) (hShift r)
    rcases hCoverage with ⟨hNonNull, _⟩ | ⟨_, hReadout⟩
    · exact (hq hNonNull).elim
    · exact congrFun hReadout x


end
/-- Directional link-derivative transfer along simultaneous coframe and link
paths. `Λ t r` is a proper, determinant-one Lorentz link for every time and
role; the coframe, column data, and normalized covector may vary with time,
while the four role-indexed links may follow independent differentiable
paths. The pointwise chart conditions remain explicit for every time. Exact
endpoint recovery at each time makes the output derivative equal to the link
derivative; no differentiability assumption on the coframe or covector paths
is required. -/
theorem principalFrameJuliaEndpointChartReadout_hasDerivAt_of_jointCoframeAndLorentzPath
    (F L : ℝ → Matrix Role Role ℝ)
    (Λ : ℝ → Role → Matrix Role Role ℝ)
    (hLorentz : ∀ t r, IsRoleLorentz (Λ t r))
    (hDet : ∀ t r, Matrix.det (Λ t r) = 1)
    (α : ℝ → Role → Module.Dual ℝ RoleSpace)
    (hAlpha : ∀ t r,
      α t r ((principalFrameColumnMatrix (F t) (L t)).mulVec
        (Pi.single r (1 : ℝ))) = 1)
    (hShift : ∀ t r,
      (principalFrameColumnMatrix (F t) (L t)).mulVec
        (Pi.single r (1 : ℝ)) ≠ 0)
    (t₀ : ℝ) (r : Role) (x v : RoleSpace)
    (hEndpoint : HasDerivAt
      (fun t => (Λ t r).transpose.mulVec x) v t₀) :
    HasDerivAt
      (fun t => principalFrameJuliaEndpointChartReadout
        ((principalFrameColumnMatrix (F t) (L t)).mulVec
          (Pi.single r (1 : ℝ)))
        (principalFrameJuliaQueryFamily (F t) (L t)
          (archiveJuliaProperRoleLorentzFamily
            (fun s => Λ t s) (fun s => hDet t s))) (α t) r x)
      v t₀ := by
  have hPath :
      (fun t => principalFrameJuliaEndpointChartReadout
        ((principalFrameColumnMatrix (F t) (L t)).mulVec
          (Pi.single r (1 : ℝ)))
        (principalFrameJuliaQueryFamily (F t) (L t)
          (archiveJuliaProperRoleLorentzFamily
            (fun s => Λ t s) (fun s => hDet t s))) (α t) r x) =
      (fun t => (Λ t r).transpose.mulVec x) := by
    funext t
    let M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace :=
      archiveJuliaProperRoleLorentzFamily
        (fun s => Λ t s) (fun s => hDet t s)
    have hIso : ∀ s y z,
        archiveJuliaSourceLorentzForm ((M s) y) ((M s) z) =
          archiveJuliaSourceLorentzForm y z := by
      intro s y z
      simpa [M, archiveJuliaProperRoleLorentzFamily] using
        archiveJuliaProperRoleLorentzEquiv_form_isometry
          (Λ t s) (hLorentz t s) (hDet t s) y z
    have hDetM : ∀ s, LinearMap.det (M s).toLinearMap = 1 := by
      intro s
      exact archiveJuliaProperRoleLorentzEquiv_det_one
        (Λ t s) (hDet t s)
    have hRecovered := principalFrameJuliaEndpointChartReadout_eq
      (F t) (L t) M (α t) hIso hDetM (hAlpha t) (hShift t) r
    calc
      principalFrameJuliaEndpointChartReadout
          ((principalFrameColumnMatrix (F t) (L t)).mulVec
            (Pi.single r (1 : ℝ)))
          (principalFrameJuliaQueryFamily (F t) (L t) M) (α t) r x =
            (M r) x := congrFun hRecovered x
      _ = (Λ t r).transpose.mulVec x := by
        simp [M, archiveJuliaProperRoleLorentzFamily,
          archiveJuliaProperRoleLorentzEquiv_apply]
  rw [hPath]
  exact hEndpoint

/-- Compatibility specialization of the joint path theorem when the coframe,
column data, and normalized covector are fixed. The four role-indexed proper
Lorentz links may still vary independently. -/
theorem principalFrameJuliaEndpointChartReadout_hasDerivAt_of_properRoleLorentzPath
    (F L : Matrix Role Role ℝ)
    (Λ : ℝ → Role → Matrix Role Role ℝ)
    (hLorentz : ∀ t r, IsRoleLorentz (Λ t r))
    (hDet : ∀ t r, Matrix.det (Λ t r) = 1)
    (α : Role → Module.Dual ℝ RoleSpace)
    (hAlpha : ∀ r,
      α r ((principalFrameColumnMatrix F L).mulVec
        (Pi.single r (1 : ℝ))) = 1)
    (hShift : ∀ r,
      (principalFrameColumnMatrix F L).mulVec
        (Pi.single r (1 : ℝ)) ≠ 0)
    (t₀ : ℝ) (r : Role) (x v : RoleSpace)
    (hEndpoint : HasDerivAt
      (fun t => (Λ t r).transpose.mulVec x) v t₀) :
    HasDerivAt
      (fun t => principalFrameJuliaEndpointChartReadout
        ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ)))
        (principalFrameJuliaQueryFamily F L
          (archiveJuliaProperRoleLorentzFamily
            (fun s => Λ t s) (fun s => hDet t s))) α r x)
      v t₀ := by
  have hJoint :=
    principalFrameJuliaEndpointChartReadout_hasDerivAt_of_jointCoframeAndLorentzPath
      (fun _ => F) (fun _ => L) Λ hLorentz hDet (fun _ => α)
      (by intro _ s; exact hAlpha s)
      (by intro _ s; exact hShift s)
      t₀ r x v hEndpoint
  simpa using hJoint

end D0.Geometry
