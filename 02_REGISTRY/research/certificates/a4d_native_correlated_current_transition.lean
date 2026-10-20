import D0.Geometry.A4DObserverPositiveExterior
import D0.Representation.GoldenCoherentMemory
import D0.Representation.GoldenOrderInterferometer
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Tactic

/-! Named finite kernels. Actual CAR matrices, complete chart recurrence,
all-time orbit and all-L heat estimates have separately stated analytic and
exact-certificate scope. No native physical admission or stationarity premise
is introduced by a definition here. -/
namespace D0.Research.CorrelatedCurrentTransition
noncomputable section
open Matrix
set_option linter.unusedSectionVars false

variable {ι ν κ : Type*} [Fintype ι] [Fintype ν] [Fintype κ]
  [DecidableEq ι] [DecidableEq ν] [DecidableEq κ]
local notation "M" => Matrix ι ι ℝ

/-- Any growing spectator isometry preserves the entire apparatus Gram. -/
theorem spectator_gram_retained (X : Matrix ι ν ℝ) (V : Matrix κ ν ℝ)
    (hV : V.transpose*V=1) :
    (X*V.transpose)*(X*V.transpose).transpose=X*X.transpose := by
  simp only [Matrix.transpose_mul,Matrix.transpose_transpose]
  calc
    _=X*(V.transpose*V)*X.transpose := by simp only [Matrix.mul_assoc]
    _=X*X.transpose := by rw [hV]; simp

theorem alpha_selfadjoint (B C : M) (hB : B.transpose=B)
    (hC : C.transpose=-C) (hCB : C*B=-(B*C)) :
    (B*C).transpose=B*C := by
  rw [Matrix.transpose_mul,hB,hC,Matrix.neg_mul,hCB,neg_neg]

theorem alpha_square (B C : M) (hB : B*B=1) (hC : C*C=-1)
    (hCB : C*B=-(B*C)) : (B*C)*(B*C)=1 := by
  calc
    _=B*(C*B)*C := by noncomm_ring
    _=-(B*B)*(C*C) := by rw [hCB]; noncomm_ring
    _=1 := by rw [hB,hC]; simp

/-- Cauchy--Schwarz step after the Clifford sum supplies its two Gram identities. -/
theorem current_causal_from_Clifford_Gram
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (x y : E) (k : ℝ) (hx : 0 < inner ℝ x x)
    (hxy : inner ℝ x y=k*inner ℝ x x)
    (hyy : inner ℝ y y=k*inner ℝ x x) : k≤1 := by
  have h := real_inner_mul_inner_self_le x y
  rw [hxy,hyy] at h
  have hpos : 0<(inner ℝ x x)*(inner ℝ x x) := mul_pos hx hx
  have hr : (k*k)*((inner ℝ x x)*(inner ℝ x x))≤k*((inner ℝ x x)*(inner ℝ x x)) := by
    convert h using 1 <;> ring
  have hs : k*k≤k := (mul_le_mul_iff_left₀ hpos).mp hr
  by_contra hn
  have hk : 1<k := lt_of_not_ge hn
  have hkp : 0<k := lt_trans (by norm_num) hk
  have hh := mul_lt_mul_of_pos_left hk hkp
  simp only [mul_one] at hh
  exact not_lt_of_ge hs hh

theorem product_current_norm (x y : ℝ) (hxy : x^2+y^2=1) :
    1-(2*x*y)^2=(x^2-y^2)^2 := by
  linear_combination -(1+x^2+y^2)*hxy

theorem golden_current_norm (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    1-(2*a*p)^2=p^6 := by
  have hc := D0.Representation.GoldenOrderInterferometer.golden_cube p hp
  have hc3 : p^3=2*p-1 := by linarith [hc,hp]
  calc
    _=1-4*p^3 := by linear_combination -4*p^2*ha
    _=(p^3)^2 := by rw [hc3]; nlinarith [hp]
    _=p^6 := by ring

theorem golden_chart_coefficients_positive (p : ℝ) (hp : p+p^2=1) (hp0 : 0<p) :
    0<164-264*p ∧ 0<1366-2208*p := by
  have h1 : p<(41:ℝ)/66 := by
    by_contra hn
    have h := mul_nonneg (sub_nonneg.mpr (le_of_not_gt hn))
      (show 0≤p+41/66 by linarith)
    nlinarith [hp]
  have h2 : p<(683:ℝ)/1104 := by
    by_contra hn
    have h := mul_nonneg (sub_nonneg.mpr (le_of_not_gt hn))
      (show 0≤p+683/1104 by linarith)
    nlinarith [hp]
  constructor <;> linarith

/-- The complete positive five-even-point chart cannot satisfy its actual recurrence. -/
theorem positive_chart_recurrence_impossible (p h0 h2 h4 h6 h8 : ℝ)
    (hp : p+p^2=1) (hp0 : 0<p)
    (h0n : 0≤h0) (h2n : 0≤h2) (h4n : 0≤h4) (h6n : 0≤h6) (h8n : 0≤h8)
    (hstrict : 0<h0 ∨ 0<h2)
    (hrec : h8+(164-264*p)*h6+(1366-2208*p)*h4+(164-264*p)*h2+h0=0) : False := by
  obtain ⟨hc1,hc2⟩ := golden_chart_coefficients_positive p hp hp0
  have h6p := mul_nonneg (le_of_lt hc1) h6n
  have h4p := mul_nonneg (le_of_lt hc2) h4n
  rcases hstrict with h0p|h2p
  · have h2p := mul_nonneg (le_of_lt hc1) h2n
    linarith
  · have h2p := mul_pos hc1 h2p
    linarith

def inputU (t : ℝ) := (1-t^2)/(1+t^2)
def inputV (t : ℝ) := 2*t/(1+t^2)
def outputX (a p t : ℝ) := a*inputU t-p*inputV t
def outputY (a p t : ℝ) := p*inputU t+a*inputV t
def currentR (a p t : ℝ) := 2*outputX a p t*outputY a p t

theorem inputU_derivative : HasDerivAt inputU 0 0 := by
  have h := ((hasDerivAt_const (0:ℝ) 1).sub ((hasDerivAt_id (0:ℝ)).pow 2)).div
    ((hasDerivAt_const (0:ℝ) 1).add ((hasDerivAt_id (0:ℝ)).pow 2)) (by norm_num)
  simpa [inputU] using h

theorem inputV_derivative : HasDerivAt inputV 2 0 := by
  have h := ((hasDerivAt_id (0:ℝ)).const_mul 2).div
    ((hasDerivAt_const (0:ℝ) 1).add ((hasDerivAt_id (0:ℝ)).pow 2)) (by norm_num)
  simpa [inputV] using h

theorem full_current_curve_derivative (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    HasDerivAt (currentR a p) (4*p^3) 0 := by
  have hx : HasDerivAt (outputX a p) (-2*p) 0 := by
    convert (inputU_derivative.const_mul a).sub (inputV_derivative.const_mul p) using 1; ring
  have hy : HasDerivAt (outputY a p) (2*a) 0 := by
    convert (inputU_derivative.const_mul p).add (inputV_derivative.const_mul a) using 1; ring
  have h := (hx.mul hy).const_mul 2
  convert h using 1
  · funext t; dsimp [currentR]; ring
  · simp [outputX,outputY,inputU,inputV]
    have hc := D0.Representation.GoldenOrderInterferometer.golden_cube p hp
    nlinarith [ha,hc]

theorem currentR_at_golden (a p : ℝ) : currentR a p 0=2*a*p := by
  simp [currentR,outputX,outputY,inputU,inputV]

theorem uniform_heat_rational_margin :
    (16896:ℝ)/2^30 < 1/2700-1/3000 := by norm_num

/-- Source normalization after the analytic Fourier argument supplies its bounds. -/
theorem uniform_heat_source_normalization (Kprime N Z : ℝ)
    (hK : 0<Kprime) (hN : N< -1/3000) (hZ : 0<Z) (hZ81 : Z<81) :
    Kprime/486000 < -(Kprime/2)*(N/Z) := by
  have hn := mul_lt_mul_of_pos_left hN hK
  have hz := mul_lt_mul_of_pos_left hZ81 hK
  have hre : -(Kprime/2)*(N/Z)=(-Kprime*N/2)/Z := by ring
  rw [hre]
  apply (lt_div_iff₀ hZ).mpr
  nlinarith

end
end D0.Research.CorrelatedCurrentTransition

#check D0.Geometry.archiveExteriorFrameLift_creator_covariant
#check D0.Geometry.archiveExteriorFrameLift_contraction_covariant
#check D0.Geometry.archiveExterior_contraction_creator_car
#check D0.Geometry.observerMetric_posDef
#check D0.Research.CorrelatedCurrentTransition.spectator_gram_retained
#check D0.Research.CorrelatedCurrentTransition.alpha_selfadjoint
#check D0.Research.CorrelatedCurrentTransition.alpha_square
#check D0.Research.CorrelatedCurrentTransition.current_causal_from_Clifford_Gram
#check D0.Research.CorrelatedCurrentTransition.golden_current_norm
#check D0.Research.CorrelatedCurrentTransition.positive_chart_recurrence_impossible
#check D0.Research.CorrelatedCurrentTransition.full_current_curve_derivative
#check D0.Research.CorrelatedCurrentTransition.uniform_heat_source_normalization

set_option pp.proofs false
#print D0.Research.CorrelatedCurrentTransition.product_current_norm
#print D0.Research.CorrelatedCurrentTransition.golden_chart_coefficients_positive
#print D0.Research.CorrelatedCurrentTransition.inputU_derivative
#print D0.Research.CorrelatedCurrentTransition.inputV_derivative
#print D0.Research.CorrelatedCurrentTransition.currentR_at_golden
#print D0.Research.CorrelatedCurrentTransition.uniform_heat_rational_margin
#print D0.Research.CorrelatedCurrentTransition.inputU
#print D0.Research.CorrelatedCurrentTransition.inputV
#print D0.Research.CorrelatedCurrentTransition.outputX
#print D0.Research.CorrelatedCurrentTransition.outputY
#print D0.Research.CorrelatedCurrentTransition.currentR

#print axioms D0.Research.CorrelatedCurrentTransition.spectator_gram_retained
#print axioms D0.Research.CorrelatedCurrentTransition.alpha_selfadjoint
#print axioms D0.Research.CorrelatedCurrentTransition.alpha_square
#print axioms D0.Research.CorrelatedCurrentTransition.current_causal_from_Clifford_Gram
#print axioms D0.Research.CorrelatedCurrentTransition.product_current_norm
#print axioms D0.Research.CorrelatedCurrentTransition.golden_current_norm
#print axioms D0.Research.CorrelatedCurrentTransition.golden_chart_coefficients_positive
#print axioms D0.Research.CorrelatedCurrentTransition.positive_chart_recurrence_impossible
#print axioms D0.Research.CorrelatedCurrentTransition.inputU_derivative
#print axioms D0.Research.CorrelatedCurrentTransition.inputV_derivative
#print axioms D0.Research.CorrelatedCurrentTransition.full_current_curve_derivative
#print axioms D0.Research.CorrelatedCurrentTransition.currentR_at_golden
#print axioms D0.Research.CorrelatedCurrentTransition.uniform_heat_rational_margin
#print axioms D0.Research.CorrelatedCurrentTransition.uniform_heat_source_normalization
#print axioms D0.Geometry.archiveExteriorFrameLift_creator_covariant
#print axioms D0.Geometry.archiveExteriorFrameLift_contraction_covariant
#print axioms D0.Geometry.archiveExterior_contraction_creator_car
#print axioms D0.Geometry.observerMetric_posDef
