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
