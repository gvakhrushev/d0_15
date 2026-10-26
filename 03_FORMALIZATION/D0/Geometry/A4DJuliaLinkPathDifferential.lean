import D0.Geometry.A4DJuliaRecoveryComposition
import Mathlib.Analysis.Calculus.FDeriv.Linear
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Prod
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Topology.Order.IntermediateValue

/-!
# Pathwise differential recovery for Julia endpoint links

This module composes the owned Eq. (27)/(28) endpoint charts with a
differentiable path of actual role-indexed proper-Lorentz endpoint maps. The
coframe and normalized source covector may vary with the endpoint path, while
each endpoint path may vary independently by role. Exact chart recovery
transfers the endpoint derivative through the same finite-carrier Julia query
and chart-selected endpoint readout.

This is a directional composition result on the declared open-chart domain.
Every declared Lorentz tangent now has an exponential path through the identity,
with properness and its endpoint derivative proved in Lean. This does not
construct a full six-dimensional chart, connect every determinant-one Lorentz
link to the identity, or establish physical admission or price/source selection.
-/

namespace D0.Geometry

open D0
open scoped Matrix.Norms.Operator

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

private theorem roleLorentzMetric_det_sq :
    roleLorentzMetric.det * roleLorentzMetric.det = 1 := by
  rw [← Matrix.det_mul, roleLorentzMetric_sq, Matrix.det_one]

private theorem roleLorentz_det_sq_of_isRoleLorentz (Λ : Matrix Role Role ℝ)
    (hΛ : IsRoleLorentz Λ) : Λ.det * Λ.det = 1 := by
  have hηdet : roleLorentzMetric.det ≠ 0 := by
    intro h
    have hs := roleLorentzMetric_det_sq
    rw [h] at hs
    norm_num at hs
  have hdet := congrArg Matrix.det hΛ
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_transpose] at hdet
  have hmul : (Λ.det * Λ.det) * roleLorentzMetric.det = 1 * roleLorentzMetric.det := by
    nlinarith [hdet]
  exact mul_right_cancel₀ hηdet hmul

private theorem isRoleLorentz_exp_tangent (a : Matrix Role Role ℝ)
    (ha : IsRoleLorentzTangent a) (t : ℝ) :
    IsRoleLorentz (NormedSpace.exp (t • a)) := by
  let A : Matrix Role Role ℝ := t • a
  have hAtranspose : A.transpose = roleLorentzMetric * (-A) * roleLorentzMetric := by
    have hmul := congrArg (fun m : Matrix Role Role ℝ => m * roleLorentzMetric) ha
    have hlinear : a.transpose + roleLorentzMetric * a * roleLorentzMetric = 0 := by
      simpa only [Matrix.add_mul, Matrix.zero_mul, Matrix.mul_assoc,
        roleLorentzMetric_sq, Matrix.mul_one, Matrix.one_mul] using hmul
    have htranspose : a.transpose = -(roleLorentzMetric * a * roleLorentzMetric) :=
      eq_neg_of_add_eq_zero_left hlinear
    dsimp [A]
    rw [htranspose]
    simp [smul_neg, Matrix.mul_assoc]
  have hηdet : roleLorentzMetric.det ≠ 0 := by
    intro h
    have hs := roleLorentzMetric_det_sq
    rw [h] at hs
    norm_num at hs
  have hηdetUnit : IsUnit roleLorentzMetric.det := isUnit_iff_ne_zero.mpr hηdet
  have hηunit : IsUnit roleLorentzMetric :=
    (Matrix.isUnit_iff_isUnit_det _).2 hηdetUnit
  have hηleft := Matrix.nonsing_inv_mul roleLorentzMetric hηdetUnit
  have hηinv : roleLorentzMetric⁻¹ = roleLorentzMetric := by
    exact (Matrix.right_inv_eq_left_inv (A := roleLorentzMetric)
      (B := roleLorentzMetric) (C := roleLorentzMetric⁻¹)
      roleLorentzMetric_sq hηleft).symm
  have hExpTranspose : (NormedSpace.exp A).transpose =
      roleLorentzMetric * NormedSpace.exp (-A) * roleLorentzMetric := by
    calc
      (NormedSpace.exp A).transpose = NormedSpace.exp A.transpose := by rw [Matrix.exp_transpose]
      _ = NormedSpace.exp (roleLorentzMetric * (-A) * roleLorentzMetric) := by rw [hAtranspose]
      _ = roleLorentzMetric * NormedSpace.exp (-A) * roleLorentzMetric := by
        simpa [hηinv] using (Matrix.exp_conj roleLorentzMetric (-A) hηunit)
  have hProduct : NormedSpace.exp A * NormedSpace.exp (-A) = 1 := by
    rw [Matrix.exp_neg]
    have hEunit : IsUnit (NormedSpace.exp A) := Matrix.isUnit_exp A
    exact Matrix.mul_nonsing_inv (NormedSpace.exp A)
      ((Matrix.isUnit_iff_isUnit_det _).mp hEunit)
  change NormedSpace.exp A * roleLorentzMetric * (NormedSpace.exp A).transpose = roleLorentzMetric
  calc
    NormedSpace.exp A * roleLorentzMetric * (NormedSpace.exp A).transpose =
        NormedSpace.exp A * roleLorentzMetric *
          (roleLorentzMetric * NormedSpace.exp (-A) * roleLorentzMetric) := by rw [hExpTranspose]
    _ = NormedSpace.exp A * (roleLorentzMetric *
          (roleLorentzMetric * (NormedSpace.exp (-A) * roleLorentzMetric))) := by
      simp only [Matrix.mul_assoc]
    _ = NormedSpace.exp A * ((roleLorentzMetric * roleLorentzMetric) *
          (NormedSpace.exp (-A) * roleLorentzMetric)) := by
      congr 1
      exact (Matrix.mul_assoc _ _ _).symm
    _ = NormedSpace.exp A * NormedSpace.exp (-A) * roleLorentzMetric := by
      rw [roleLorentzMetric_sq]
      simp [Matrix.mul_assoc]
    _ = roleLorentzMetric := by rw [hProduct, Matrix.one_mul]

private theorem det_exp_tangent_one (a : Matrix Role Role ℝ)
    (ha : IsRoleLorentzTangent a) (t : ℝ) : (NormedSpace.exp (t • a)).det = 1 := by
  let f : ℝ → ℝ := fun s => (NormedSpace.exp (s • a)).det
  have hSq : ∀ s, f s * f s = 1 := by
    intro s
    simpa [f] using roleLorentz_det_sq_of_isRoleLorentz _ (isRoleLorentz_exp_tangent a ha s)
  have hCont : Continuous f := by
    have hPath : Continuous (fun s : ℝ => NormedSpace.exp (s • a)) :=
      NormedSpace.exp_continuous.comp (continuous_id.smul continuous_const)
    simpa [f] using hPath.matrix_det
  have hzero : f 0 = 1 := by simp [f]
  by_contra hne
  have hnot : f t ≠ 1 := by simpa [f] using hne
  have hminus : f t = -1 := by
    have hfactor : (f t - 1) * (f t + 1) = 0 := by nlinarith [hSq t]
    rcases mul_eq_zero.mp hfactor with hpos | hneg
    · exact (hnot (by linarith)).elim
    · linarith
  have hz : (0 : ℝ) ∈ Set.uIcc (f 0) (f t) := by
    rw [hzero, hminus]
    norm_num [Set.uIcc]
  obtain ⟨s, _, hfs⟩ := intermediate_value_uIcc hCont.continuousOn hz
  have hs := hSq s
  rw [hfs] at hs
  norm_num at hs

private theorem hasDerivAt_exp_tangent_transpose_mulVec (a : Matrix Role Role ℝ)
    (x : RoleSpace) :
    HasDerivAt (fun t : ℝ => (NormedSpace.exp (t • a)).transpose.mulVec x)
      (a.transpose.mulVec x) (0 : ℝ) := by
  have hMatrix : HasDerivAt (fun t : ℝ => NormedSpace.exp (t • a)) a 0 := by
    simpa using (hasDerivAt_exp_smul_const (𝕂 := ℝ) (𝔸 := Matrix Role Role ℝ) a (0 : ℝ))
  apply hasDerivAt_pi.mpr
  intro i
  have hSum : HasDerivAt
      (fun t : ℝ => ∑ j : Role, (NormedSpace.exp (t • a)) j i * x j)
      (∑ j : Role, a j i * x j) 0 := by
    simpa using (HasDerivAt.fun_sum (u := Finset.univ)
      (fun j hj => (hasDerivAt_pi.mp (hasDerivAt_pi.mp hMatrix j) i).mul_const (x j)))
  simpa [Matrix.mulVec, Matrix.transpose_apply] using hSum

/-- A simultaneous family of Lorentz tangent generators produces actual
determinant-one exponential paths. Along those paths, arbitrary coframe,
column, and normalized-covector paths remain allowed, subject to the same
pointwise chart hypotheses as the general joint-path theorem. The endpoint
readout derivative at the identity is the generator's transpose action. -/
theorem principalFrameJuliaEndpointChartReadout_hasDerivAt_of_jointCoframeAndLorentzTangent
    (F L : ℝ → Matrix Role Role ℝ)
    (a : Role → Matrix Role Role ℝ)
    (hTangent : ∀ r, IsRoleLorentzTangent (a r))
    (α : ℝ → Role → Module.Dual ℝ RoleSpace)
    (hAlpha : ∀ t r,
      α t r ((principalFrameColumnMatrix (F t) (L t)).mulVec
        (Pi.single r (1 : ℝ))) = 1)
    (hShift : ∀ t r,
      (principalFrameColumnMatrix (F t) (L t)).mulVec
        (Pi.single r (1 : ℝ)) ≠ 0)
    (r : Role) (x : RoleSpace) :
    HasDerivAt
      (fun t => principalFrameJuliaEndpointChartReadout
        ((principalFrameColumnMatrix (F t) (L t)).mulVec
          (Pi.single r (1 : ℝ)))
        (principalFrameJuliaQueryFamily (F t) (L t)
          (archiveJuliaProperRoleLorentzFamily
            (fun s => NormedSpace.exp (t • a s))
            (fun s => det_exp_tangent_one (a s) (hTangent s) t)))
        (α t) r x)
      ((a r).transpose.mulVec x) (0 : ℝ) := by
  apply principalFrameJuliaEndpointChartReadout_hasDerivAt_of_jointCoframeAndLorentzPath
    F L (fun t s => NormedSpace.exp (t • a s))
    (fun t s => isRoleLorentz_exp_tangent (a s) (hTangent s) t)
    (fun t s => det_exp_tangent_one (a s) (hTangent s) t)
    α hAlpha hShift 0 r x ((a r).transpose.mulVec x)
  exact hasDerivAt_exp_tangent_transpose_mulVec (a r) x

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
