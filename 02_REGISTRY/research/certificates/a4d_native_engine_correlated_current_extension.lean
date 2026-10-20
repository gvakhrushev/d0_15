import D0.Algebra.FibonacciAFTower
import Mathlib.Tactic

/-! Generic exact kernels for the correlated-current sector of the existing
closed-record executor. This capsule does not select the initial correlation,
identify the current observer with the executor axis, or assert physical
admission. -/
namespace D0.Research.EngineCorrelatedCurrentExtension
noncomputable section

def highGate (a p sigma : ℝ) (v : ℝ × ℝ) : ℝ × ℝ :=
  (a*v.1-sigma*p*v.2, -sigma*p*v.1-a*v.2)

def wedge (u v : ℝ × ℝ) : ℝ := u.1*v.2-u.2*v.1

def normSq (u : ℝ × ℝ) : ℝ := u.1^2+u.2^2

def heatNumerator (x : ℝ) : ℝ :=
  -(256:ℝ)/25*x^64-(256:ℝ)/25*x^128+
  (3072:ℝ)/25*x^416+(512:ℝ)/5*x^480+(6144:ℝ)/25*x^832

theorem wedge_linear (a b c d : ℝ) (u v : ℝ × ℝ) :
    wedge (a*u.1+b*u.2,c*u.1+d*u.2)
      (a*v.1+b*v.2,c*v.1+d*v.2) = (a*d-b*c)*wedge u v := by
  simp [wedge]
  ring

theorem high_gate_wedge_negates (a p sigma : ℝ) (u v : ℝ × ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hs : sigma^2=1) :
    wedge (highGate a p sigma u) (highGate a p sigma v) = -wedge u v := by
  have hresult : wedge (highGate a p sigma u) (highGate a p sigma v) =
      (a*(-a)-(-sigma*p)*(-sigma*p))*wedge u v := by
    unfold highGate
    convert wedge_linear a (-sigma*p) (-sigma*p) (-a) u v using 1
    ring_nf
  rw [hresult]
  have hdet : a*(-a)-(-sigma*p)*(-sigma*p) = -1 := by
    nlinarith [ha,hp,hs]
  rw [hdet]
  ring

theorem high_gate_preserves_norm (a p sigma : ℝ) (u : ℝ × ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hs : sigma^2=1) :
    normSq (highGate a p sigma u) = normSq u := by
  have hnorm : a^2+sigma^2*p^2=1 := by nlinarith [ha,hp,hs]
  simp [normSq,highGate]
  linear_combination u.1^2*hnorm + u.2^2*hnorm

theorem correlation_never_zero (x : ℝ) (hx : x ≠ 0) (n : ℕ) :
    ((-1:ℝ)^n)*x ≠ 0 := by
  have hpow : (-1:ℝ)^n ≠ 0 := pow_ne_zero _ (by norm_num)
  exact mul_ne_zero hpow hx

theorem golden_amplitude_current_is_timelike (s : ℝ) (hs : s ≠ 0) :
    0 < 1-(2*s^2/(1+2*s^2))^2 := by
  have hd : 0 < 1+2*s^2 := by positivity
  have heq : 1-(2*s^2/(1+2*s^2))^2 =
      (1+4*s^2)/(1+2*s^2)^2 := by
    field_simp
    ring
  rw [heq]
  positivity

theorem L4_heat_numerator_negative (x : ℝ) (hx0 : 0 < x) (hx1 : x < 1)
    (hx5 : x^5=(1:ℝ)/2) : heatNumerator x < 0 := by
  have hxhalf : (1:ℝ)/2 < x := by
    by_contra hn
    have hle : x ≤ (1:ℝ)/2 := le_of_not_gt hn
    have hpowle : ∀ n : ℕ, x^n ≤ ((1:ℝ)/2)^n := by
      intro n
      induction n with
      | zero => norm_num
      | succ n ih =>
          rw [pow_succ]
          exact mul_le_mul ih hle hx0.le (pow_nonneg (by norm_num : (0:ℝ)≤(1/2)) _)
    have h := hpowle 5
    norm_num at h
    linarith
  have hx2 : x^2 < 1 := by
    have hleft : 0 < 1-x := sub_pos.mpr hx1
    have hright : 0 < 1+x := by linarith
    have hprod := mul_pos hleft hright
    nlinarith
  have hpowers_lower : ∀ n : ℕ, ((1:ℝ)/2)^n ≤ x^n := by
    intro n
    induction n with
    | zero => norm_num
    | succ n ih =>
        rw [pow_succ]
        exact mul_le_mul ih hxhalf.le (by norm_num) (pow_nonneg hx0.le _)
  have h64 : x^64=((1:ℝ)/2)^12*x^4 := by
    calc
      x^64=x^(5*12+4) := by norm_num
      _=(x^5)^12*x^4 := by rw [pow_add,pow_mul]
      _=((1:ℝ)/2)^12*x^4 := by rw [hx5]
  have h128 : x^128=((1:ℝ)/2)^25*x^3 := by
    calc
      x^128=x^(5*25+3) := by norm_num
      _=(x^5)^25*x^3 := by rw [pow_add,pow_mul]
      _=((1:ℝ)/2)^25*x^3 := by rw [hx5]
  have h416 : x^416=((1:ℝ)/2)^83*x := by
    calc
      x^416=x^(5*83+1) := by norm_num
      _=(x^5)^83*x^1 := by rw [pow_add,pow_mul]
      _=((1:ℝ)/2)^83*x := by rw [hx5]; simp
  have h480 : x^480=((1:ℝ)/2)^96 := by
    calc
      x^480=x^(5*96) := by norm_num
      _=(x^5)^96 := by rw [pow_mul]
      _=((1:ℝ)/2)^96 := by rw [hx5]
  have h832 : x^832=((1:ℝ)/2)^166*x^2 := by
    calc
      x^832=x^(5*166+2) := by norm_num
      _=(x^5)^166*x^2 := by rw [pow_add,pow_mul]
      _=((1:ℝ)/2)^166*x^2 := by rw [hx5]
  have hx4_lower : (1:ℝ)/16 ≤ x^4 := by
    have h := hpowers_lower 4
    norm_num at h
    exact h
  have hneg :
      -(256:ℝ)/25*((1:ℝ)/2)^12*x^4 ≤ -(1:ℝ)/6400 := by
    have h := mul_le_mul_of_nonpos_left hx4_lower
      (by norm_num : -(256:ℝ)/25*((1:ℝ)/2)^12≤0)
    nlinarith [h]
  let q1 : ℝ := (3072/25)*((1:ℝ)/2)^83
  let q2 : ℝ := (512/5)*((1:ℝ)/2)^96
  let q3 : ℝ := (6144/25)*((1:ℝ)/2)^166
  have hpos1 : q1*x < (1:ℝ)/3000000 := by
    have hq : 0<q1*(1-x) := mul_pos (by positivity) (sub_pos.mpr hx1)
    have hq' : q1 < (1:ℝ)/3000000 := by norm_num [q1]
    nlinarith [hq,hq']
  have hpos2 : q2 < (1:ℝ)/3000000 := by norm_num [q2]
  have hpos3 : q3*x^2 < (1:ℝ)/3000000 := by
    have hq : 0<q3*(1-x^2) := mul_pos (by positivity) (sub_pos.mpr hx2)
    have hq' : q3 < (1:ℝ)/3000000 := by norm_num [q3]
    nlinarith [hq,hq']
  have hpositive_sum : q1*x+q2+q3*x^2 < (1:ℝ)/1000000 := by
    norm_num at hpos1 hpos2 hpos3 ⊢
    linarith
  have hnegative2 :
      -(256:ℝ)/25*((1:ℝ)/2)^25*x^3 ≤ 0 := by
    have hpos : 0≤(256:ℝ)/25*((1:ℝ)/2)^25*x^3 := by positivity
    linarith
  have hrewrite : heatNumerator x =
      -(256:ℝ)/25*((1:ℝ)/2)^12*x^4
      -(256:ℝ)/25*((1:ℝ)/2)^25*x^3
      +q1*x+q2+q3*x^2 := by
    unfold heatNumerator q1 q2 q3
    rw [h64,h128,h416,h480,h832]
    ring
  rw [hrewrite]
  nlinarith [hneg,hnegative2,hpositive_sum]

theorem L4_heat_slope_positive (x Z : ℝ) (hx0 : 0<x) (hx1 : x<1)
    (hx5 : x^5=(1:ℝ)/2) (hZ : 0<Z) : 0 < (-4*heatNumerator x)/Z := by
  have hp := L4_heat_numerator_negative x hx0 hx1 hx5
  have hnum : 0 < -4*heatNumerator x := by nlinarith [hp]
  exact div_pos hnum hZ

end

/-- A common invertible linear frame cannot send two independent directions
    to the executor time axis at once. -/
theorem no_two_axis_collapse
    {V : Type*} [AddCommGroup V] [Module ℝ V]
    (F : V ≃ₗ[ℝ] V) (v w u : V) (r a b : ℝ)
    (hr : r ≠ 0) (hv : v ≠ 0)
    (hw : ∀ c : ℝ, w ≠ c • v)
    (hfirst : F v = a • u)
    (hcurrent : F (v + r • w) = b • u) : False := by
  have ha : a ≠ 0 := by
    intro ha
    apply hv
    apply F.injective
    calc
      F v = a • u := hfirst
      _ = F 0 := by simp [ha]
  let c : ℝ := (b - a) / r
  have hc : r * c = b - a := by
    dsimp [c]
    field_simp [hr]
  have hstep : r • F w = (b - a) • u := by
    have h : a • u + r • F w = b • u := by
      have h' := hcurrent
      rw [map_add, map_smul] at h'
      rw [hfirst] at h'
      exact h'
    have hsub : r • F w = (b • u) - a • u := by
      rw [eq_sub_iff_add_eq]
      simpa [add_assoc, add_comm, add_left_comm] using h
    calc
      r • F w = (b • u) - a • u := hsub
      _ = (b - a) • u := by rw [sub_smul]
  have hFw : F w = c • u := by
    calc
      F w = (1:ℝ) • F w := by simp
      _ = (r⁻¹ * r) • F w := by congr 1; field_simp [hr]
      _ = r⁻¹ • (r • F w) := by rw [smul_smul]
      _ = r⁻¹ • ((b - a) • u) := by rw [hstep]
      _ = (r⁻¹ * (b - a)) • u := by rw [smul_smul]
      _ = c • u := by dsimp [c]; field_simp [hr]
  have hratio : a * (c / a) = c := by field_simp [ha]
  have hdep : F w = (c / a) • F v := by
    calc
      F w = c • u := hFw
      _ = (c / a * a) • u := by congr 1; field_simp [ha]
      _ = (c / a) • (a • u) := by rw [smul_smul]
      _ = (c / a) • F v := by rw [hfirst]
  have hz : F (w - (c / a) • v) = 0 := by
    calc
      F (w - (c / a) • v) = F w - (c / a) • F v := by rw [map_sub, map_smul]
      _ = 0 := by rw [hdep]; simp
  have hrel : w - (c / a) • v = 0 := by
    apply F.injective
    simpa using hz
  have hline : w = (c / a) • v := sub_eq_zero.mp hrel
  exact (hw (c / a)) hline

def coordinateAxis0 : Fin 4 → ℝ := Pi.single 0 1
def coordinateAxis1 : Fin 4 → ℝ := Pi.single 1 1

theorem gl_frame_active_sector_impossible
    (F : (Fin 4 → ℝ) ≃ₗ[ℝ] (Fin 4 → ℝ)) (mu r a b : ℝ)
    (hmu : mu ≠ 0) (hr : r ≠ 0)
    (hfirst : F (mu • coordinateAxis0) = a • coordinateAxis0)
    (hcurrent : F (coordinateAxis0 + r • coordinateAxis1) = b • coordinateAxis0) : False := by
  have hv : mu • coordinateAxis0 ≠ 0 := by
    intro hz
    have h0 := congrFun hz 0
    simp [coordinateAxis0] at h0
    exact hmu h0
  have hw : ∀ c : ℝ, coordinateAxis1 ≠ c • (mu • coordinateAxis0) := by
    intro c heq
    have h1 := congrFun heq 1
    simp [coordinateAxis0, coordinateAxis1] at h1
  have hcurrent_scaled :
      F ((mu • coordinateAxis0) + (mu*r) • coordinateAxis1) = (mu*b) • coordinateAxis0 := by
    have harg : (mu • coordinateAxis0) + (mu*r) • coordinateAxis1 =
        mu • (coordinateAxis0 + r • coordinateAxis1) := by
      calc
        (mu • coordinateAxis0) + (mu*r) • coordinateAxis1 =
            mu • coordinateAxis0 + mu • (r • coordinateAxis1) := by rw [smul_smul]
        _ = mu • (coordinateAxis0 + r • coordinateAxis1) := by rw [smul_add]
    calc
      F ((mu • coordinateAxis0) + (mu*r) • coordinateAxis1) =
          F (mu • (coordinateAxis0 + r • coordinateAxis1)) := by rw [harg]
      _ = mu • F (coordinateAxis0 + r • coordinateAxis1) :=
          map_smul F mu (coordinateAxis0 + r • coordinateAxis1)
      _ = mu • (b • coordinateAxis0) := by rw [hcurrent]
      _ = (mu*b) • coordinateAxis0 := by rw [smul_smul]
  exact no_two_axis_collapse F (mu • coordinateAxis0) coordinateAxis1 coordinateAxis0
    (mu*r) a (mu*b) (mul_ne_zero hmu hr) hv hw hfirst hcurrent_scaled

theorem golden_first_grade_coefficient_nonzero (p : ℝ) (hp : p+p^2=1) :
    2*p-1 ≠ 0 := by
  intro h
  nlinarith

theorem active_current_tilt_nonzero (s : ℝ) (hs : s ≠ 0) :
    -2*s^2/(1+2*s^2) ≠ 0 := by
  apply div_ne_zero
  · exact mul_ne_zero (by norm_num) (pow_ne_zero 2 hs)
  · positivity

theorem active_sector_common_GL_rest_alignment_impossible
    (F : (Fin 4 → ℝ) ≃ₗ[ℝ] (Fin 4 → ℝ)) (p s a b : ℝ)
    (hp : p+p^2=1) (hs : s ≠ 0)
    (hfirst : F ((2*p-1) • coordinateAxis0) = a • coordinateAxis0)
    (hcurrent : F (coordinateAxis0 + (-2*s^2/(1+2*s^2)) • coordinateAxis1) =
      b • coordinateAxis0) : False := by
  exact gl_frame_active_sector_impossible F (2*p-1) (-2*s^2/(1+2*s^2)) a b
    (golden_first_grade_coefficient_nonzero p hp)
    (active_current_tilt_nonzero s hs) hfirst hcurrent

def afCapacity (k : ℕ) : ℕ :=
  _root_.D0.Algebra.FibonacciAFTower.dimA (1 + 3*k)

theorem dimA_two_step_recurrence (n : ℕ) :
    _root_.D0.Algebra.FibonacciAFTower.dimA (n+2) +
      _root_.D0.Algebra.FibonacciAFTower.dimA n =
      3 * _root_.D0.Algebra.FibonacciAFTower.dimA (n+1) := by
  simp only [_root_.D0.Algebra.FibonacciAFTower.dimA,
    _root_.D0.Algebra.FibonacciAFTower.pathCount]
  ring

theorem dimA_six_step_recurrence (n : ℕ) :
    _root_.D0.Algebra.FibonacciAFTower.dimA (n+6) +
      _root_.D0.Algebra.FibonacciAFTower.dimA n =
      18 * _root_.D0.Algebra.FibonacciAFTower.dimA (n+3) := by
  have h0 := dimA_two_step_recurrence n
  have h1 := dimA_two_step_recurrence (n+1)
  have h2 := dimA_two_step_recurrence (n+2)
  have h3 := dimA_two_step_recurrence (n+3)
  have h4 := dimA_two_step_recurrence (n+4)
  nlinarith

theorem afCapacity_recurrence (k : ℕ) :
    afCapacity (k+2) + afCapacity k = 18 * afCapacity (k+1) := by
  have h := dimA_six_step_recurrence (1 + 3*k)
  have h0 : 1 + 3*(k+2) = (1 + 3*k) + 6 := by omega
  have h1 : 1 + 3*(k+1) = (1 + 3*k) + 3 := by omega
  change _root_.D0.Algebra.FibonacciAFTower.dimA (1 + 3*(k+2)) +
      _root_.D0.Algebra.FibonacciAFTower.dimA (1 + 3*k) =
    18 * _root_.D0.Algebra.FibonacciAFTower.dimA (1 + 3*(k+1))
  rw [h0, h1]
  exact h

theorem afCapacity_initial : afCapacity 0 = 5 ∧ afCapacity 1 = 89 := by
  constructor <;> norm_num [afCapacity,
    _root_.D0.Algebra.FibonacciAFTower.dimA,
    _root_.D0.Algebra.FibonacciAFTower.pathCount]

end D0.Research.EngineCorrelatedCurrentExtension

#check D0.Research.EngineCorrelatedCurrentExtension.wedge_linear
#check D0.Research.EngineCorrelatedCurrentExtension.high_gate_wedge_negates
#check D0.Research.EngineCorrelatedCurrentExtension.high_gate_preserves_norm
#check D0.Research.EngineCorrelatedCurrentExtension.correlation_never_zero
#check D0.Research.EngineCorrelatedCurrentExtension.golden_amplitude_current_is_timelike
#check D0.Research.EngineCorrelatedCurrentExtension.L4_heat_numerator_negative
#check D0.Research.EngineCorrelatedCurrentExtension.L4_heat_slope_positive
#print axioms D0.Research.EngineCorrelatedCurrentExtension.wedge_linear
#print axioms D0.Research.EngineCorrelatedCurrentExtension.high_gate_wedge_negates
#print axioms D0.Research.EngineCorrelatedCurrentExtension.high_gate_preserves_norm
#print axioms D0.Research.EngineCorrelatedCurrentExtension.correlation_never_zero
#print axioms D0.Research.EngineCorrelatedCurrentExtension.golden_amplitude_current_is_timelike
#print axioms D0.Research.EngineCorrelatedCurrentExtension.L4_heat_numerator_negative
#print axioms D0.Research.EngineCorrelatedCurrentExtension.L4_heat_slope_positive

#check D0.Research.EngineCorrelatedCurrentExtension.no_two_axis_collapse
#check D0.Research.EngineCorrelatedCurrentExtension.gl_frame_active_sector_impossible
#check D0.Research.EngineCorrelatedCurrentExtension.golden_first_grade_coefficient_nonzero
#check D0.Research.EngineCorrelatedCurrentExtension.active_current_tilt_nonzero
#check D0.Research.EngineCorrelatedCurrentExtension.active_sector_common_GL_rest_alignment_impossible
#print axioms D0.Research.EngineCorrelatedCurrentExtension.no_two_axis_collapse
#print axioms D0.Research.EngineCorrelatedCurrentExtension.gl_frame_active_sector_impossible
#print axioms D0.Research.EngineCorrelatedCurrentExtension.golden_first_grade_coefficient_nonzero
#print axioms D0.Research.EngineCorrelatedCurrentExtension.active_current_tilt_nonzero
#print axioms D0.Research.EngineCorrelatedCurrentExtension.active_sector_common_GL_rest_alignment_impossible
#check D0.Research.EngineCorrelatedCurrentExtension.dimA_two_step_recurrence
#check D0.Research.EngineCorrelatedCurrentExtension.dimA_six_step_recurrence
#check D0.Research.EngineCorrelatedCurrentExtension.afCapacity_recurrence
#check D0.Research.EngineCorrelatedCurrentExtension.afCapacity_initial
#print axioms D0.Research.EngineCorrelatedCurrentExtension.afCapacity_recurrence
#print axioms D0.Research.EngineCorrelatedCurrentExtension.afCapacity_initial
