import D0.Representation.GoldenCoherentMemory
import Mathlib.Tactic

/-! Generic all-time domain and conjugate-growth lemmas for the research
engine. No native admission, new CORE owner, physical refinement or GR. -/
namespace D0.Research.ClosedRecordEngine
noncomputable section

def lowerStep (a p : ℝ) (v : ℝ × ℝ) : ℝ × ℝ :=
  if 0 < v.2 then (a * v.1 - p * v.2, p * v.1 + a * v.2)
  else (a * v.1 + p * v.2, -p * v.1 + a * v.2)

def bandA (a p : ℝ) : ℝ × ℝ := (-2*a*p, 2*p-1)
def bandB (a p : ℝ) : ℝ × ℝ := (5*p-4, a*(4*p-3))
def Safe (a p : ℝ) (v : ℝ × ℝ) : Prop :=
  v = (0,1) ∨ v = (-p,a) ∨ v = bandA a p ∨ v = bandB a p

theorem golden_bounds (a p : ℝ) (ha0 : 0<a) (hp0 : 0<p)
    (ha : a^2=p) (hp : p+p^2=1) :
    (3:ℝ)/5 < p ∧ p < (5:ℝ)/8 ∧ (3:ℝ)/4 < a := by
  have hlow : (3:ℝ)/5 < p := by
    by_contra h
    have hh : p ≤ (3:ℝ)/5 := le_of_not_gt h
    nlinarith [mul_nonneg hp0.le (sub_nonneg.mpr hh)]
  have hupp : p < (5:ℝ)/8 := by
    by_contra h
    have hh : (5:ℝ)/8 ≤ p := le_of_not_gt h
    nlinarith [mul_nonneg (show 0 ≤ p+(5:ℝ)/8 by linarith) (sub_nonneg.mpr hh)]
  refine ⟨hlow, hupp, ?_⟩
  by_contra h
  have hh : a ≤ (3:ℝ)/4 := le_of_not_gt h
  nlinarith [mul_nonneg ha0.le (sub_nonneg.mpr hh)]

theorem band_signs (a p : ℝ) (ha0 : 0<a) (hp0 : 0<p)
    (ha : a^2=p) (hp : p+p^2=1) :
    (1:ℝ)/5 < (bandA a p).2 ∧ (bandB a p).2 < -(3:ℝ)/8 := by
  obtain ⟨hl, hu, hla⟩ := golden_bounds a p ha0 hp0 ha hp
  simp only [bandA, bandB]
  constructor
  · linarith
  · nlinarith [mul_pos ha0 (show 0 < (5:ℝ)/2-4*p by linarith)]

theorem seed_enters_band (a p : ℝ) (ha0 : 0<a)
    (ha : a^2=p) (hp : p+p^2=1) :
    lowerStep a p (0,1) = (-p,a) ∧ lowerStep a p (-p,a) = bandA a p := by
  constructor
  · simp [lowerStep]
  · simp only [lowerStep, ha0, ↓reduceIte, bandA]
    apply Prod.ext
    · dsimp; ring
    · dsimp; nlinarith

theorem band_transitions (a p : ℝ) (ha0 : 0<a) (hp0 : 0<p)
    (ha : a^2=p) (hp : p+p^2=1) :
    lowerStep a p (bandA a p) = bandB a p ∧
    lowerStep a p (bandB a p) = bandA a p := by
  obtain ⟨hA, hB⟩ := band_signs a p ha0 hp0 ha hp
  have hAp : 0 < (bandA a p).2 := by linarith
  have hBn : ¬ 0 < (bandB a p).2 := by linarith
  constructor
  · rw [lowerStep, if_pos hAp]
    apply Prod.ext
    · dsimp [bandA, bandB]; linear_combination -2*p*ha - 4*hp
    · dsimp [bandA, bandB]; linear_combination -2*a*hp
  · rw [lowerStep, if_neg hBn]
    apply Prod.ext
    · dsimp [bandA, bandB]; linear_combination 4*a*hp
    · dsimp [bandA, bandB]; linear_combination (4*p-3)*ha - hp

theorem safe_invariant (a p : ℝ) (ha0 : 0<a) (hp0 : 0<p)
    (ha : a^2=p) (hp : p+p^2=1) (v : ℝ × ℝ) (hv : Safe a p v) :
    Safe a p (lowerStep a p v) := by
  obtain ⟨h0,h1⟩ := seed_enters_band a p ha0 ha hp
  obtain ⟨hA,hB⟩ := band_transitions a p ha0 hp0 ha hp
  rcases hv with rfl | rfl | rfl | rfl
  · exact Or.inr (Or.inl h0)
  · exact Or.inr (Or.inr (Or.inl h1))
  · exact Or.inr (Or.inr (Or.inr hA))
  · exact Or.inr (Or.inr (Or.inl hB))

theorem safe_uniform_first_grade (a p : ℝ) (ha0 : 0<a) (hp0 : 0<p)
    (ha : a^2=p) (hp : p+p^2=1) (v : ℝ × ℝ) (hv : Safe a p v) :
    (1:ℝ)/5 < |v.2| := by
  obtain ⟨_,_,hla⟩ := golden_bounds a p ha0 hp0 ha hp
  obtain ⟨hA,hB⟩ := band_signs a p ha0 hp0 ha hp
  rcases hv with rfl | rfl | rfl | rfl
  · norm_num
  · simpa only [abs_of_pos ha0] using (show (1:ℝ)/5 < a by linarith)
  · rw [abs_of_pos (show 0 < (bandA a p).2 by linarith)]; exact hA
  · rw [abs_of_neg (show (bandB a p).2 < 0 by linarith)]; linarith

theorem every_seed_tick_regular (a p : ℝ) (ha0 : 0<a) (hp0 : 0<p)
    (ha : a^2=p) (hp : p+p^2=1) (n : ℕ) :
    (1:ℝ)/5 < |((lowerStep a p)^[n] (0,1)).2| := by
  apply safe_uniform_first_grade a p ha0 hp0 ha hp
  induction n with
  | zero => exact Or.inl rfl
  | succ n ih =>
      rw [Function.iterate_succ_apply']
      exact safe_invariant a p ha0 hp0 ha hp _ ih

def chebPair (C : ℝ) : ℕ → ℝ × ℝ
  | 0 => (1,C)
  | n+1 => let v := chebPair C n; (v.2, 2*C*v.2-v.1)

theorem conjugate_growth (C : ℝ) (hC : 1 ≤ C) (n : ℕ) :
    0 ≤ (chebPair C n).1 ∧ (chebPair C n).1 ≤ (chebPair C n).2 ∧
    C^(n+1) ≤ (chebPair C n).2 := by
  induction n with
  | zero => simpa [chebPair] using (show (0:ℝ) ≤ 1 ∧ 1 ≤ C ∧ C ≤ C from ⟨by norm_num,hC,le_rfl⟩)
  | succ n ih =>
      obtain ⟨hx,hxy,hpow⟩ := ih
      have hy : 0 ≤ (chebPair C n).2 := le_trans hx hxy
      have hm : (chebPair C n).2 ≤ C*(chebPair C n).2 := by
        nlinarith [mul_nonneg (sub_nonneg.mpr hC) hy]
      have hnext : C*(chebPair C n).2 ≤ 2*C*(chebPair C n).2-(chebPair C n).1 := by
        linarith
      change 0 ≤ (chebPair C n).2 ∧
        (chebPair C n).2 ≤ 2*C*(chebPair C n).2-(chebPair C n).1 ∧
        C^(n+1+1) ≤ 2*C*(chebPair C n).2-(chebPair C n).1
      refine ⟨hy, le_trans hm hnext, ?_⟩
      calc
        C^(n+1+1) = C*C^(n+1) := by rw [pow_succ]; ring
        _ ≤ C*(chebPair C n).2 := mul_le_mul_of_nonneg_left hpow (by linarith)
        _ ≤ _ := hnext

theorem conjugate_never_returns (C : ℝ) (hC : 1<C) (n : ℕ) :
    1 < (chebPair C n).2 := by
  have h := (conjugate_growth C hC.le n).2.2
  have hp : 1 < C^(n+1) := one_lt_pow₀ hC (by omega)
  linarith

end
end D0.Research.ClosedRecordEngine

#check D0.Research.ClosedRecordEngine.every_seed_tick_regular
#check D0.Research.ClosedRecordEngine.conjugate_growth
#print axioms D0.Research.ClosedRecordEngine.golden_bounds
#print axioms D0.Research.ClosedRecordEngine.band_signs
#print axioms D0.Research.ClosedRecordEngine.seed_enters_band
#print axioms D0.Research.ClosedRecordEngine.band_transitions
#print axioms D0.Research.ClosedRecordEngine.safe_invariant
#print axioms D0.Research.ClosedRecordEngine.safe_uniform_first_grade
#print axioms D0.Research.ClosedRecordEngine.every_seed_tick_regular
#print axioms D0.Research.ClosedRecordEngine.conjugate_growth
#print axioms D0.Research.ClosedRecordEngine.conjugate_never_returns
#print axioms D0.Representation.GoldenCoherentMemory.fullStep_orthogonal
