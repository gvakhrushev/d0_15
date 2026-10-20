import D0.Representation.GoldenCoherentMemory
import D0.Geometry.A4DObserverPositiveExterior
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.Deriv.Add

/-! A finite state-dependent input to the existing observer form.
The explicit density-to-Role coordinate readout below is mathematical data;
its native physical admission and a complete heat preparation are not proved.
No new action, temperature, source equation, or physical gate is defined. -/
namespace D0.Research.RecordedObserverPreparation
noncomputable section
open D0 D0.Geometry Matrix
open D0.Representation.GoldenCoherentMemory
open scoped BigOperators

def roleCoords (a b c d : ℝ) : RoleVector :=
  fun r => if r = A then a else if r = B then b else if r = C then c else d

def currentSquare (j : RoleVector) : ℝ := ∑ r, roleLorentzSign r * j r ^ 2

theorem currentSquare_coords (a b c d : ℝ) :
    currentSquare (roleCoords a b c d) = a^2-b^2-c^2-d^2 := by
  simp [currentSquare, roleCoords, roleLorentzSign, roleRoleSigEquiv,
    roleSign, Role, Dyad, Fintype.sum_prod_type, A, B, C, D]
  ring

/-- Coordinates of [[x,z+i*w],[z-i*w,y]] in the stated Pauli readout. -/
def densityCurrent (x y z w : ℝ) : RoleVector :=
  roleCoords (x+y) (2*z) (-2*w) (x-y)

theorem density_current_square (x y z w : ℝ) :
    currentSquare (densityCurrent x y z w) = 4*(x*y-z^2-w^2) := by
  rw [densityCurrent, currentSquare_coords]
  ring

/-- True tensor partial trace of a real full amplitude matrix [[a,b],[c,d]]. -/
def retainedCurrent (a b c d : ℝ) : RoleVector :=
  densityCurrent (a^2+b^2) (c^2+d^2) (a*c+b*d) 0

theorem retained_current_square (a b c d : ℝ) :
    currentSquare (retainedCurrent a b c d) = 4*(a*d-b*c)^2 := by
  rw [retainedCurrent, density_current_square]
  ring

def observerFromCurrent (j : RoleVector) : RoleVector :=
  fun r => j r / Real.sqrt (currentSquare j)

theorem observerFromCurrent_unit (j : RoleVector) (hk : 0 < currentSquare j) :
    lorentzUnitObserver (observerFromCurrent j) := by
  unfold lorentzUnitObserver observerFromCurrent
  calc
    _ = (∑ r, roleLorentzSign r * j r ^ 2) / (Real.sqrt (currentSquare j))^2 := by
      simp only [div_pow, mul_div_assoc, Finset.sum_div]
    _ = currentSquare j / currentSquare j := by
      rw [Real.sq_sqrt hk.le]
      rfl
    _ = 1 := div_self (ne_of_gt hk)

def metricFromCurrent (j : RoleVector) : Matrix Role Role ℝ :=
  fun r s => -roleLorentzMetric r s +
    2*(roleLorentzSign r*j r)*(roleLorentzSign s*j s)/currentSquare j

theorem metricFromCurrent_eq_observer (j : RoleVector) (hk : 0 < currentSquare j) :
    metricFromCurrent j = observerMetric (observerFromCurrent j) := by
  ext r s
  unfold metricFromCurrent observerMetric observerCovector observerFromCurrent
  have hs := Real.sq_sqrt hk.le
  have hn : Real.sqrt (currentSquare j) ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hk)
  have hk0 : currentSquare j ≠ 0 := ne_of_gt hk
  field_simp
  rw [hs]
  ring

theorem retained_metric_positive (a b c d : ℝ) (hd : a*d-b*c ≠ 0) :
    (metricFromCurrent (retainedCurrent a b c d)).PosDef := by
  have hk : 0 < currentSquare (retainedCurrent a b c d) := by
    rw [retained_current_square]
    positivity
  rw [metricFromCurrent_eq_observer _ hk]
  exact observerMetric_posDef _ (observerFromCurrent_unit _ hk)

theorem actual_blank_record_current (a p u v : ℝ) :
    (fullStep a p).mulVec ![u,0,v,0] = ![a*u-p*v,0,0,p*u+a*v] :=
  blank_record_evolution a p u v

theorem golden_record_current (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    retainedCurrent a 0 0 p = roleCoords 1 0 0 (p-p^2) := by
  ext r
  simp [retainedCurrent, densityCurrent, roleCoords, ha, hp]

theorem golden_record_faithful (a p : ℝ) (ha : a^2=p) (hp0 : 0<p) :
    0 < currentSquare (retainedCurrent a 0 0 p) := by
  rw [retained_current_square]
  have ha0 : a ≠ 0 := by intro h; simp [h] at ha; linarith
  have hap : a*p ≠ 0 := mul_ne_zero ha0 (ne_of_gt hp0)
  simpa using mul_pos (by norm_num : (0:ℝ)<4) (sq_pos_of_ne_zero hap)

theorem pure_record_singular (a b c d : ℝ) (hd : a*d-b*c=0) :
    currentSquare (retainedCurrent a b c d) = 0 := by
  rw [retained_current_square, hd]
  norm_num

/-- A normalized rational input curve of the same gate, with all output modes retained. -/
def inputU (t : ℝ) : ℝ := (1-t^2)/(1+t^2)
def inputV (t : ℝ) : ℝ := 2*t/(1+t^2)
def outputA (a p t : ℝ) : ℝ := a*inputU t-p*inputV t
def outputB (a p t : ℝ) : ℝ := p*inputU t+a*inputV t

theorem input_curve_normalized (t : ℝ) : (inputU t)^2+(inputV t)^2=1 := by
  have hd : 1+t^2 ≠ 0 := by positivity
  unfold inputU inputV
  field_simp
  ring

theorem inputU_derivative : HasDerivAt inputU 0 0 := by
  have h := ((hasDerivAt_const (0:ℝ) 1).sub ((hasDerivAt_id (0:ℝ)).pow 2)).div
    ((hasDerivAt_const (0:ℝ) 1).add ((hasDerivAt_id (0:ℝ)).pow 2)) (by norm_num)
  simpa [inputU] using h

theorem inputV_derivative : HasDerivAt inputV 2 0 := by
  have h := ((hasDerivAt_id (0:ℝ)).const_mul 2).div
    ((hasDerivAt_const (0:ℝ) 1).add ((hasDerivAt_id (0:ℝ)).pow 2)) (by norm_num)
  simpa [inputV] using h

theorem outputA_derivative (a p : ℝ) : HasDerivAt (outputA a p) (-2*p) 0 := by
  convert (inputU_derivative.const_mul a).sub (inputV_derivative.const_mul p) using 1
  ring

theorem outputB_derivative (a p : ℝ) : HasDerivAt (outputB a p) (2*a) 0 := by
  convert (inputU_derivative.const_mul p).add (inputV_derivative.const_mul a) using 1
  ring

theorem actual_recorded_shape_derivative (a p : ℝ) :
    HasDerivAt (fun t => (outputA a p t)^2-(outputB a p t)^2) (-8*a*p) 0 := by
  have h := ((outputA_derivative a p).pow 2).sub ((outputB_derivative a p).pow 2)
  convert h using 1
  simp [outputA, outputB, inputU, inputV]
  ring

/-- Formula for every normalized diagonal retained density, away from its rank-one boundary. -/
def diagonalMetricCoefficient (x : ℝ) : ℝ := -1+1/(2*x*(1-x))
def mixedMetricCoefficient (x : ℝ) : ℝ := -(2*x-1)/(2*x*(1-x))

theorem diagonal_density_metric (x : ℝ) (hx : x ≠ 0) (hx1 : 1-x ≠ 0) :
    metricFromCurrent (densityCurrent x (1-x) 0 0) A A = diagonalMetricCoefficient x := by
  unfold metricFromCurrent
  rw [density_current_square]
  norm_num [diagonalMetricCoefficient, densityCurrent, roleCoords, roleLorentzMetric,
    roleLorentzSign, roleRoleSigEquiv, roleSign, A, B, C, D]
  field_simp
  ring

theorem mixed_density_metric (x : ℝ) (hx : x ≠ 0) (hx1 : 1-x ≠ 0) :
    metricFromCurrent (densityCurrent x (1-x) 0 0) A D = mixedMetricCoefficient x := by
  unfold metricFromCurrent
  rw [density_current_square]
  norm_num [mixedMetricCoefficient, densityCurrent, roleCoords, roleLorentzMetric,
    roleLorentzSign, roleRoleSigEquiv, roleSign, A, B, C, D]
  field_simp
  ring

theorem diagonalMetricCoefficient_derivative (x : ℝ) (hx : x ≠ 0) (hx1 : 1-x ≠ 0) :
    HasDerivAt diagonalMetricCoefficient (2*(2*x-1)/(2*x*(1-x))^2) x := by
  have hden := ((hasDerivAt_id x).const_mul 2).mul
    ((hasDerivAt_const x 1).sub (hasDerivAt_id x))
  have h := (hasDerivAt_const x 1).div hden (by exact mul_ne_zero (mul_ne_zero (by norm_num) hx) hx1)
  convert (hasDerivAt_const x (-1)).add h using 1
  simp
  ring

theorem mixedMetricCoefficient_derivative (x : ℝ) (hx : x ≠ 0) (hx1 : 1-x ≠ 0) :
    HasDerivAt mixedMetricCoefficient
      (-(4*x*(1-x)+2*(2*x-1)^2)/(2*x*(1-x))^2) x := by
  have hden := ((hasDerivAt_id x).const_mul 2).mul
    ((hasDerivAt_const x 1).sub (hasDerivAt_id x))
  have hnum := (((hasDerivAt_id x).const_mul 2).sub_const 1).neg
  convert hnum.div hden (mul_ne_zero (mul_ne_zero (by norm_num) hx) hx1) using 1
  simp
  ring

theorem actual_diagonal_pairing_derivative (a p : ℝ)
    (ha : a ≠ 0) (ha1 : 1-a^2 ≠ 0) :
    HasDerivAt (fun t => diagonalMetricCoefficient ((outputA a p t)^2))
      (2*(2*a^2-1)/(2*a^2*(1-a^2))^2 * (-4*a*p)) 0 := by
  have hx : HasDerivAt (fun t => (outputA a p t)^2) (-4*a*p) 0 := by
    convert (outputA_derivative a p).pow 2 using 1
    simp [outputA, inputU, inputV]
    ring
  have h := diagonalMetricCoefficient_derivative (a^2) (pow_ne_zero _ ha) ha1
  have he : a^2 = (outputA a p 0)^2 := by simp [outputA, inputU, inputV]
  rw [he] at h
  simpa [outputA, inputU, inputV, Function.comp_def] using h.comp 0 hx

theorem actual_mixed_pairing_derivative (a p : ℝ)
    (ha : a ≠ 0) (ha1 : 1-a^2 ≠ 0) :
    HasDerivAt (fun t => mixedMetricCoefficient ((outputA a p t)^2))
      (-(4*a^2*(1-a^2)+2*(2*a^2-1)^2)/(2*a^2*(1-a^2))^2 * (-4*a*p)) 0 := by
  have hx : HasDerivAt (fun t => (outputA a p t)^2) (-4*a*p) 0 := by
    convert (outputA_derivative a p).pow 2 using 1
    simp [outputA, inputU, inputV]
    ring
  have h := mixedMetricCoefficient_derivative (a^2) (pow_ne_zero _ ha) ha1
  have he : a^2 = (outputA a p 0)^2 := by simp [outputA, inputU, inputV]
  rw [he] at h
  simpa [outputA, inputU, inputV, Function.comp_def] using h.comp 0 hx

end
end D0.Research.RecordedObserverPreparation

#check D0.Representation.GoldenCoherentMemory.blank_record_evolution
#check D0.Geometry.observerMetric_posDef
#check D0.Geometry.observerExteriorBladeGram_pos

#check D0.Research.RecordedObserverPreparation.currentSquare_coords
#check D0.Research.RecordedObserverPreparation.density_current_square
#check D0.Research.RecordedObserverPreparation.retained_current_square
#check D0.Research.RecordedObserverPreparation.observerFromCurrent_unit
#check D0.Research.RecordedObserverPreparation.metricFromCurrent_eq_observer
#check D0.Research.RecordedObserverPreparation.retained_metric_positive
#check D0.Research.RecordedObserverPreparation.actual_blank_record_current
#check D0.Research.RecordedObserverPreparation.golden_record_current
#check D0.Research.RecordedObserverPreparation.golden_record_faithful
#check D0.Research.RecordedObserverPreparation.pure_record_singular
#check D0.Research.RecordedObserverPreparation.input_curve_normalized
#check D0.Research.RecordedObserverPreparation.inputU_derivative
#check D0.Research.RecordedObserverPreparation.inputV_derivative
#check D0.Research.RecordedObserverPreparation.outputA_derivative
#check D0.Research.RecordedObserverPreparation.outputB_derivative
#check D0.Research.RecordedObserverPreparation.actual_recorded_shape_derivative
#check D0.Research.RecordedObserverPreparation.diagonal_density_metric
#check D0.Research.RecordedObserverPreparation.mixed_density_metric
#check D0.Research.RecordedObserverPreparation.diagonalMetricCoefficient_derivative
#check D0.Research.RecordedObserverPreparation.mixedMetricCoefficient_derivative
#check D0.Research.RecordedObserverPreparation.actual_diagonal_pairing_derivative
#check D0.Research.RecordedObserverPreparation.actual_mixed_pairing_derivative

#print axioms D0.Research.RecordedObserverPreparation.currentSquare_coords
#print axioms D0.Research.RecordedObserverPreparation.density_current_square
#print axioms D0.Research.RecordedObserverPreparation.retained_current_square
#print axioms D0.Research.RecordedObserverPreparation.observerFromCurrent_unit
#print axioms D0.Research.RecordedObserverPreparation.metricFromCurrent_eq_observer
#print axioms D0.Research.RecordedObserverPreparation.retained_metric_positive
#print axioms D0.Research.RecordedObserverPreparation.actual_blank_record_current
#print axioms D0.Research.RecordedObserverPreparation.golden_record_current
#print axioms D0.Research.RecordedObserverPreparation.golden_record_faithful
#print axioms D0.Research.RecordedObserverPreparation.pure_record_singular
#print axioms D0.Research.RecordedObserverPreparation.input_curve_normalized
#print axioms D0.Research.RecordedObserverPreparation.inputU_derivative
#print axioms D0.Research.RecordedObserverPreparation.inputV_derivative
#print axioms D0.Research.RecordedObserverPreparation.outputA_derivative
#print axioms D0.Research.RecordedObserverPreparation.outputB_derivative
#print axioms D0.Research.RecordedObserverPreparation.actual_recorded_shape_derivative
#print axioms D0.Research.RecordedObserverPreparation.diagonal_density_metric
#print axioms D0.Research.RecordedObserverPreparation.mixed_density_metric
#print axioms D0.Research.RecordedObserverPreparation.diagonalMetricCoefficient_derivative
#print axioms D0.Research.RecordedObserverPreparation.mixedMetricCoefficient_derivative
#print axioms D0.Research.RecordedObserverPreparation.actual_diagonal_pairing_derivative
#print axioms D0.Research.RecordedObserverPreparation.actual_mixed_pairing_derivative
#print axioms D0.Representation.GoldenCoherentMemory.blank_record_evolution
#print axioms D0.Geometry.observerMetric_posDef
#print axioms D0.Geometry.observerExteriorBladeGram_pos
