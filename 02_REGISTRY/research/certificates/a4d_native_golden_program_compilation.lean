import Mathlib.Analysis.SpecificLimits.Basic
import D0.Representation.GoldenCoherentMemory
import D0.CondensedAnchor.DetectorSupportGoldenWeight
import D0.Synthesis.SceneNormalizedQuotientDescent
import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.LinearAlgebra.Matrix.Permutation
import Mathlib.Analysis.Normed.Operator.NormedSpace
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Normed.Module.FiniteDimension
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
set_option linter.unnecessarySeqFocus false

/-! Complete retained golden preparation, literal recursive words and cylinder extension.
This standalone research experiment does not install a physical controller,
heat carrier, source or metric stationarity rule. -/

namespace D0.Research.GoldenHistoryPreparation

noncomputable section

abbrev Pair := Bool × Bool

def Word : ℕ → Type
  | 0 => Unit
  | n+1 => Pair × Word n

instance (n : ℕ) : Fintype (Word n) := by
  induction n with
  | zero => exact inferInstanceAs (Fintype Unit)
  | succ n ih => exact inferInstanceAs (Fintype (Pair × Word n))

instance (n : ℕ) : DecidableEq (Word n) := by
  induction n with
  | zero => exact inferInstanceAs (DecidableEq Unit)
  | succ n ih => exact inferInstanceAs (DecidableEq (Pair × Word n))

def firstLabel : {n : ℕ} → Word n → Option Bool
  | 0, _ => none
  | _+1, (x,w) => if x.1 = x.2 then firstLabel w else some x.1

def flipFirst : {n : ℕ} → Word n → Word n
  | 0, w => w
  | _+1, (x,w) => if x.1 = x.2 then (x,flipFirst w) else ((x.2,x.1),w)

def amplitude (a p : ℝ) : {n : ℕ} → Word n → ℝ
  | 0, _ => 1
  | _+1, (x,w) => ((if x.1 then p else a)*(if x.2 then p else a))*amplitude a p w

theorem flipFirst_involutive (n : ℕ) : Function.Involutive (@flipFirst n) := by
  induction n with
  | zero => intro w; rfl
  | succ n ih =>
    rintro ⟨⟨b,c⟩,w⟩
    cases b <;> cases c <;> simp only [flipFirst, Bool.false_eq_true, Bool.true_eq_false, if_true, if_false] <;> try rw [ih w]

theorem firstLabel_flipFirst (n : ℕ) (w : Word n) :
    firstLabel (flipFirst w) = (firstLabel w).map Bool.not := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rcases w with ⟨⟨b,c⟩,w⟩
    cases b <;> cases c <;> simp [flipFirst,firstLabel,ih]

theorem amplitude_flipFirst (a p : ℝ) (n : ℕ) (w : Word n) :
    amplitude a p (flipFirst w) = amplitude a p w := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rcases w with ⟨⟨b,c⟩,w⟩
    cases b <;> cases c <;> simp only [flipFirst,amplitude,Bool.false_eq_true,Bool.true_eq_false,if_true,if_false,ih] <;> ring

def q (a p : ℝ) : ℝ := a^4+p^4

 theorem complete_mass (a p : ℝ) (h : a^2+p^2=1) (n : ℕ) :
    ∑ w : Word n, (amplitude a p w)^2 = 1 := by
  induction n with
  | zero => simp [Word,amplitude]
  | succ n ih =>
    change ∑ w : Pair × Word n, (@amplitude a p (n+1) w)^2 = 1
    simp only [Fintype.sum_prod_type,amplitude,mul_pow]
    have hm (k : ℝ) : (∑ w : Word n, k*(amplitude a p w)^2) = k := by
      rw [← Finset.mul_sum,ih,mul_one]
    calc _ = ∑ b : Bool, ∑ c : Bool, (if b then p else a)^2*(if c then p else a)^2 := by
           apply Finset.sum_congr rfl; intro b _
           apply Finset.sum_congr rfl; intro c _
           exact hm ((if b then p else a)^2*(if c then p else a)^2)
         _ = 1 := by
           simp only [Fintype.sum_bool,Bool.false_eq_true,if_true,if_false]
           nlinarith [congrArg (fun x : ℝ => x^2) h]

 theorem failure_mass (a p : ℝ) (n : ℕ) :
    ∑ w : Word n, (if firstLabel w = none then (amplitude a p w)^2 else 0) = (q a p)^n := by
  induction n with
  | zero => simp [Word,firstLabel,amplitude]
  | succ n ih =>
    change ∑ w : Pair × Word n, (if @firstLabel (n+1) w = none then (@amplitude a p (n+1) w)^2 else 0) = (q a p)^(n+1)
    simp only [Fintype.sum_prod_type]
    change (∑ b : Bool, ∑ c : Bool, ∑ w : Word n, (if @firstLabel (n+1) ((b,c),w) = none then (@amplitude a p (n+1) ((b,c),w))^2 else 0)) = _
    simp only [Fintype.sum_bool,firstLabel,amplitude,Bool.false_eq_true,Bool.true_eq_false,if_true,if_false,Option.some_ne_none,mul_pow]
    have hm (k : ℝ) : (∑ w : Word n, if firstLabel w = none then k*(amplitude a p w)^2 else 0) = k*(q a p)^n := by
      calc _ = k*(∑ w : Word n, if firstLabel w = none then (amplitude a p w)^2 else 0) := by
              rw [Finset.mul_sum]; congr 1; funext w; simp [mul_ite]
           _ = _ := by rw [ih]
    simp only [Finset.sum_const_zero,hm,zero_add,add_zero]
    simp only [q,pow_succ]
    ring

def firstBit (n : ℕ) (w : Word n) : Bool := (firstLabel w).getD false

def copyLabel (n : ℕ) (s : Word n × Bool) : Word n × Bool :=
  (s.1,s.2 ^^ firstBit n s.1)

def controlledFlip (n : ℕ) (s : Word n × Bool) : Word n × Bool :=
  (if s.2 then flipFirst s.1 else s.1,s.2)

theorem copyLabel_involutive (n : ℕ) : Function.Involutive (copyLabel n) := by
  rintro ⟨w,b⟩
  simp [copyLabel]

theorem controlledFlip_involutive (n : ℕ) : Function.Involutive (controlledFlip n) := by
  rintro ⟨w,b⟩
  cases b <;> simp [controlledFlip,flipFirst_involutive n w]

def route (n : ℕ) : Equiv.Perm (Word n × Bool) :=
  ((copyLabel_involutive n).toPerm (copyLabel n)).trans
    ((controlledFlip_involutive n).toPerm (controlledFlip n))

theorem full_retained_route_bijective (n : ℕ) : Function.Bijective (route n) :=
  (route n).bijective

theorem full_retained_route_inverse (n : ℕ) (s : Word n × Bool) :
    (route n).symm (route n s) = s := (route n).symm_apply_apply s

theorem failed_record_unchanged (n : ℕ) (w : Word n) (h : firstLabel w = none) :
    route n (w,false) = (w,false) := by
  simp [route,copyLabel,controlledFlip,firstBit,h,Function.Involutive.toPerm]

theorem success_false_record (n : ℕ) (w : Word n) (h : firstLabel w = some false) :
    route n (w,false) = (w,false) := by
  simp [route,copyLabel,controlledFlip,firstBit,h,Function.Involutive.toPerm]

theorem success_true_record (n : ℕ) (w : Word n) (h : firstLabel w = some true) :
    route n (w,false) = (flipFirst w,true) := by
  simp [route,copyLabel,controlledFlip,firstBit,h,Function.Involutive.toPerm]

theorem successful_coherent_twins (a p : ℝ) (n : ℕ) (w : Word n)
    (h : firstLabel w = some false) :
    route n (w,false) = (w,false) ∧
    route n (flipFirst w,false) = (w,true) ∧
    amplitude a p (flipFirst w) = amplitude a p w := by
  refine ⟨success_false_record n w h, ?_, amplitude_flipFirst a p n w⟩
  have hf : firstLabel (flipFirst w) = some true := by
    rw [firstLabel_flipFirst,h]; rfl
  rw [success_true_record n (flipFirst w) hf,flipFirst_involutive n w]

def successMass (a p : ℝ) (n : ℕ) (b : Bool) : ℝ :=
  ∑ w : Word n, if firstLabel w = some b then (amplitude a p w)^2 else 0

theorem complete_coherent_success_symmetry (a p : ℝ) (n : ℕ) :
    successMass a p n false = successMass a p n true := by
  unfold successMass
  refine Fintype.sum_equiv ((flipFirst_involutive n).toPerm (@flipFirst n)) _ _ ?_
  intro w
  change (if firstLabel w = some false then (amplitude a p w)^2 else 0) =
    (if firstLabel (flipFirst w) = some true then (amplitude a p (flipFirst w))^2 else 0)
  rw [firstLabel_flipFirst,amplitude_flipFirst]
  cases h : firstLabel w with
  | none => simp
  | some b => cases b <;> simp

theorem complete_mass_partition (a p : ℝ) (n : ℕ) :
    successMass a p n false + successMass a p n true + (q a p)^n =
      ∑ w : Word n, (amplitude a p w)^2 := by
  rw [← failure_mass]
  unfold successMass
  rw [← Finset.sum_add_distrib,← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl; intro w _
  cases h : firstLabel w with
  | none => simp
  | some b => cases b <;> simp

theorem exact_fair_success_weights (a p : ℝ) (h : a^2+p^2=1) (n : ℕ) :
    successMass a p n false = (1-(q a p)^n)/2 ∧
    successMass a p n true = (1-(q a p)^n)/2 := by
  have hm := complete_mass_partition a p n
  rw [complete_mass a p h n] at hm
  have he := complete_coherent_success_symmetry a p n
  constructor <;> linarith

theorem actual_owned_golden_blank (a p : ℝ) :
    (D0.Representation.GoldenOrderInterferometer.gate a p).mulVec ![1,0] = ![a,p] := by
  ext i; fin_cases i <;>
    simp [D0.Representation.GoldenOrderInterferometer.gate,Matrix.mulVec,dotProduct,Fin.sum_univ_two]

theorem golden_factor_normalized (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    a^2+p^2=1 := by rw [ha,hp]

theorem golden_failure_parameter (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    q a p = 3-4*p := by
  unfold q
  have hs := congrArg (fun x : ℝ => x^2) hp
  have hc := D0.Representation.GoldenOrderInterferometer.golden_cube p hp
  nlinarith [congrArg (fun x : ℝ => x^2) ha]

theorem full_retained_route_preserves_all_norms (n : ℕ) (f : Word n × Bool → ℝ) :
    ∑ s, (f (route n s))^2 = ∑ s, (f s)^2 :=
  Equiv.sum_comp (route n) (fun s => (f s)^2)

theorem golden_root_interval (p : ℝ) (hp : p+p^2=1) (hp0 : 0<p) :
    (617/1000 : ℝ) < p ∧ p < 1 := by
  constructor
  · by_contra h
    have hx : p ≤ 617/1000 := le_of_not_gt h
    have hm := mul_nonneg (le_of_lt hp0) (sub_nonneg.mpr hx)
    nlinarith
  · nlinarith [sq_pos_of_pos hp0]

theorem golden_pair_success_balance (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    q a p + 2*p^3 = 1 := by
  rw [golden_failure_parameter a p ha hp]
  have hc := D0.Representation.GoldenOrderInterferometer.golden_cube p hp
  nlinarith

theorem golden_pair_failure_bounds (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) :
    0 ≤ q a p ∧ q a p ≤ 8/15 ∧ q a p < 1 := by
  have hn : 0 ≤ q a p := by unfold q; positivity
  have hl := (golden_root_interval p hp hp0).1
  have hq := golden_failure_parameter a p ha hp
  have hs := golden_pair_success_balance a p ha hp
  have hc : 0<p^3 := pow_pos hp0 3
  refine ⟨hn,?_,?_⟩ <;> linarith

 theorem golden_four_pair_good_weight (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) :
    (919/1000 : ℝ) ≤ 1-(q a p)^4 ∧ 1-(q a p)^4 ≤ 1 := by
  have hq := golden_pair_failure_bounds a p ha hp hp0
  have hpow := pow_le_pow_left₀ hq.1 hq.2.1 4
  constructor
  · norm_num at hpow ⊢
    linarith
  · have hn : 0 ≤ (q a p)^4 := by positivity
    linarith

def jointGoodWeight (a p : ℝ) : ℝ := (1-(q a p)^4)^5

def historySuccess (a p d : ℝ) : ℝ := (d/32)*jointGoodWeight a p

def historyFailure (a p d : ℝ) : ℝ := 1-historySuccess a p d

theorem golden_five_bit_good_bounds (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) :
    (919/1000 : ℝ)^5 ≤ jointGoodWeight a p ∧ jointGoodWeight a p ≤ 1 := by
  have h := golden_four_pair_good_weight a p ha hp hp0
  have hn : 0 ≤ 1-(q a p)^4 := by linarith [h.1]
  exact ⟨pow_le_pow_left₀ (by norm_num) h.1 5,pow_le_one₀ hn h.2⟩

theorem native_degree_retained_preparation_rate (a p d : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) (hd0 : 20≤d) (hd1 : d≤24) :
    0 ≤ historyFailure a p d ∧ historyFailure a p d < p ∧ historyFailure a p d < 1 := by
  have hg := golden_five_bit_good_bounds a p ha hp hp0
  have hgn : 0 ≤ jointGoodWeight a p := le_trans (by positivity) hg.1
  have hslo : (383/1000 : ℝ) < historySuccess a p d := by
    unfold historySuccess
    have hm := mul_le_mul_of_nonneg_right (show (5/8 : ℝ) ≤ d/32 by linarith) hgn
    have hglo := mul_le_mul_of_nonneg_left hg.1 (show (0 : ℝ) ≤ 5/8 by norm_num)
    have hstrict : (383/1000 : ℝ) < (5/8)*(919/1000)^5 := by norm_num
    linarith
  have hsupp : historySuccess a p d ≤ 3/4 := by
    unfold historySuccess
    have hm := mul_le_mul_of_nonneg_left hg.2 (show (0 : ℝ) ≤ d/32 by linarith)
    nlinarith
  have hl := (golden_root_interval p hp hp0).1
  unfold historyFailure
  refine ⟨?_,?_,?_⟩ <;> linarith

theorem native_degree_all_retained_retries_bound (a p d : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) (hd0 : 20≤d) (hd1 : d≤24) (k : ℕ) :
    (historyFailure a p d)^k ≤ p^k := by
  have h := native_degree_retained_preparation_rate a p d ha hp hp0 hd0 hd1
  exact pow_le_pow_left₀ h.1 (le_of_lt h.2.1) k

theorem frozen_native_golden_fair_history (n : ℕ) :
    let p := D0.primitiveRoot
    let a := Real.sqrt p
    successMass a p n false = (1-(3-4*p)^n)/2 ∧
    successMass a p n true = (1-(3-4*p)^n)/2 := by
  dsimp
  have hp0 := D0.Representation.GoldenOrderInterferometer.primitive_positive
  have hp := D0.primitive_root_satisfies
  have ha := Real.sq_sqrt (le_of_lt hp0)
  have h := exact_fair_success_weights (Real.sqrt D0.primitiveRoot) D0.primitiveRoot
    (golden_factor_normalized _ _ ha hp) n
  rw [golden_failure_parameter _ _ ha hp] at h
  exact h

def rejectedVector {Ω : Type*} [DecidableEq Ω] (ψ : Ω → ℝ) (A : Finset Ω) (x : Ω) : ℝ :=
  if x ∈ A then 0 else ψ x

theorem complete_rejected_record_gram {Ω : Type*} [Fintype Ω] [DecidableEq Ω]
    (ψ : Ω → ℝ) (A B : Finset Ω) :
    ∑ x, rejectedVector ψ A x * rejectedVector ψ B x =
      ∑ x, (rejectedVector ψ (A ∪ B) x)^2 := by
  apply Finset.sum_congr rfl; intro x _
  by_cases ha : x∈A <;> by_cases hb : x∈B <;>
    simp [rejectedVector,ha,hb,pow_two]

theorem complete_rejected_record_overlap_bound {Ω : Type*} [Fintype Ω] [DecidableEq Ω]
    (ψ : Ω → ℝ) (A B : Finset Ω) :
    0 ≤ ∑ x, rejectedVector ψ A x * rejectedVector ψ B x ∧
    (∑ x, rejectedVector ψ A x * rejectedVector ψ B x) ≤
      ∑ x, (rejectedVector ψ B x)^2 := by
  rw [complete_rejected_record_gram]
  constructor
  · exact Finset.sum_nonneg (fun x _ => sq_nonneg _)
  · apply Finset.sum_le_sum; intro x _
    by_cases ha : x∈A <;> by_cases hb : x∈B <;>
      simp [rejectedVector,ha,hb,sq_nonneg]

def delaySum (c : ℝ) (k : ℕ) : ℝ := ∑ i ∈ Finset.range k, c^i

def retainedRetryGram (small large c : ℝ) (k : ℕ) : ℝ :=
  Real.sqrt small * Real.sqrt large * delaySum c k

theorem sqrt_success_ratio_coefficient (small large : ℝ) (hs : 0≤small) (hl : 0<large) :
    Real.sqrt small * Real.sqrt large = Real.sqrt (small/large)*large := by
  rw [Real.sqrt_div hs]
  have hn : Real.sqrt large ≠ 0 := Real.sqrt_ne_zero'.mpr hl
  have hsq := Real.sq_sqrt (le_of_lt hl)
  calc _ = Real.sqrt small/Real.sqrt large * (Real.sqrt large)^2 := by field_simp
       _ = _ := by rw [hsq]

theorem exact_retained_retry_gram (small large : ℝ) (hs : 0≤small) (hl : 0<large) (k : ℕ) :
    retainedRetryGram small large (1-large) k =
      Real.sqrt (small/large)*(1-(1-large)^k) := by
  unfold retainedRetryGram delaySum
  rw [sqrt_success_ratio_coefficient small large hs hl,mul_assoc]
  have h := geom_sum_mul_neg (1-large) k
  have hi : 1-(1-large) = large := by ring
  rw [hi] at h
  rw [mul_comm large,h]

theorem whole_retained_retry_coherence_bound (small large c : ℝ)
    (hs : 0≤small) (hl : 0<large) (hl1 : large≤1) (hc : 0≤c) (hcl : c≤1-large) (k : ℕ) :
    retainedRetryGram small large c k ≤ Real.sqrt (small/large) := by
  have hm : delaySum c k ≤ delaySum (1-large) k := by
    apply Finset.sum_le_sum; intro i _
    exact pow_le_pow_left₀ hc hcl i
  have hmul : 0≤Real.sqrt small*Real.sqrt large := by positivity
  have h := mul_le_mul_of_nonneg_left hm hmul
  change retainedRetryGram small large c k ≤ retainedRetryGram small large (1-large) k at h
  rw [exact_retained_retry_gram small large hs hl k] at h
  have hp : 0≤(1-large)^k := pow_nonneg (by linarith) k
  have hr := Real.sqrt_nonneg (small/large)
  nlinarith

theorem actual_degree_twenty_twentyfour_ratio (α : ℝ) (h : 0<α) :
    ((20/32)*α)/((24/32)*α) = (5/6 : ℝ) := by
  have hn : α ≠ 0 := ne_of_gt h
  field_simp
  ring

theorem actual_degree_retained_retry_coherence_floor (α c : ℝ)
    (hα : 0<α) (hα1 : α≤1) (hc : 0≤c) (hcl : c≤1-(24/32)*α) (k : ℕ) :
    retainedRetryGram ((20/32)*α) ((24/32)*α) c k ≤ Real.sqrt (5/6) ∧
    Real.sqrt (5/6 : ℝ) < 1 := by
  have hs : (0 : ℝ) ≤ (20/32)*α := by positivity
  have hl : (0 : ℝ) < (24/32)*α := by positivity
  have hl1 : (24/32 : ℝ)*α ≤ 1 := by nlinarith
  have hb := whole_retained_retry_coherence_bound _ _ c hs hl hl1 hc hcl k
  rw [actual_degree_twenty_twentyfour_ratio α hα] at hb
  refine ⟨hb,?_⟩
  have hsq := Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 5/6)
  have hn := Real.sqrt_nonneg (5/6:ℝ)
  nlinarith

theorem exact_retained_retry_gram_limit (small large : ℝ)
    (hs : 0≤small) (hl : 0<large) (hl1 : large≤1) :
    Filter.Tendsto (fun k => retainedRetryGram small large (1-large) k)
      Filter.atTop (nhds (Real.sqrt (small/large))) := by
  have hn : 0≤1-large := by linarith
  have hlt : 1-large < 1 := by linarith
  have hpow := tendsto_pow_atTop_nhds_zero_of_lt_one hn hlt
  have h : Filter.Tendsto (fun k : ℕ => Real.sqrt (small/large)*(1-(1-large)^k))
      Filter.atTop (nhds (Real.sqrt (small/large))) := by
    have h1 : Filter.Tendsto (fun _ : ℕ => (1:ℝ)) Filter.atTop (nhds 1) := tendsto_const_nhds
    simpa using (h1.sub hpow).const_mul (Real.sqrt (small/large))
  convert h using 1
  ext k
  exact exact_retained_retry_gram small large hs hl k

def completeCodeMass (a p : ℝ) (n m : ℕ) (b : Fin m → Bool) : ℝ :=
  ∑ w : Fin m → Word n, ∏ i : Fin m,
    if firstLabel (w i) = some (b i) then (amplitude a p (w i))^2 else 0

theorem complete_disjoint_record_code_mass (a p : ℝ) (n m : ℕ) (b : Fin m → Bool) :
    completeCodeMass a p n m b = ∏ i : Fin m, successMass a p n (b i) := by
  unfold completeCodeMass successMass
  exact (Fintype.prod_sum (fun i : Fin m => fun w : Word n =>
    if firstLabel w = some (b i) then (amplitude a p w)^2 else 0)).symm

theorem whole_fair_code_mass (a p : ℝ) (h : a^2+p^2=1) (n m : ℕ) (b : Fin m → Bool) :
    completeCodeMass a p n m b = ((1-(q a p)^n)/2)^m := by
  have hf (bit : Bool) : successMass a p n bit = (1-(q a p)^n)/2 := by
    cases bit
    · exact (exact_fair_success_weights a p h n).1
    · exact (exact_fair_success_weights a p h n).2
  rw [complete_disjoint_record_code_mass]
  simp [hf,div_pow]

theorem actual_five_bit_code_carrier : Fintype.card (Fin 5 → Bool) = 32 := by
  norm_num [Fintype.card_fun]

theorem actual_five_bit_code_mass (a p : ℝ) (h : a^2+p^2=1) (b : Fin 5 → Bool) :
    completeCodeMass a p 4 5 b = jointGoodWeight a p/32 := by
  rw [whole_fair_code_mass a p h]
  unfold jointGoodWeight
  ring

theorem full_retained_valid_code_mass (a p : ℝ) (h : a^2+p^2=1)
    (S : Finset (Fin 5 → Bool)) :
    (∑ b ∈ S, completeCodeMass a p 4 5 b) = historySuccess a p (S.card : ℝ) := by
  simp_rw [actual_five_bit_code_mass a p h]
  simp [historySuccess]
  ring

def tensorRoute (n m : ℕ) : Equiv.Perm (Fin m → Word n × Bool) :=
  Equiv.piCongrRight (fun _ => route n)

theorem all_disjoint_retained_records_reversible (n m : ℕ) :
    Function.Bijective (tensorRoute n m) := (tensorRoute n m).bijective

def rawForCode (n m : ℕ) (b : Fin m → Bool) (w : Fin m → Word n) : Fin m → Word n :=
  fun i => if b i then flipFirst (w i) else w i

theorem full_successful_code_keeps_same_record (n m : ℕ) (b : Fin m → Bool) (w : Fin m → Word n)
    (hw : ∀ i, firstLabel (w i) = some false) :
    tensorRoute n m (fun i => (rawForCode n m b w i,false)) = fun i => (w i,b i) := by
  funext i
  change route n (rawForCode n m b w i,false) = (w i,b i)
  unfold rawForCode
  cases h : b i
  · simp only [Bool.false_eq_true,if_false]
    exact success_false_record n (w i) (hw i)
  · simp only [if_true]
    exact (successful_coherent_twins 1 1 n (w i) (hw i)).2.1

theorem full_code_coherent_amplitude_independence (a p : ℝ) (n m : ℕ)
    (b : Fin m → Bool) (w : Fin m → Word n) :
    (∏ i : Fin m, amplitude a p (rawForCode n m b w i)) = ∏ i : Fin m, amplitude a p (w i) := by
  apply Finset.prod_congr rfl; intro i _
  unfold rawForCode
  cases h : b i <;>
    simp only [Bool.false_eq_true,if_true,if_false,amplitude_flipFirst]

end

end D0.Research.GoldenHistoryPreparation

namespace D0.Research.GoldenCoherentAmplification
noncomputable section
open Matrix Complex D0.Representation.GoldenOrderInterferometer

def goldenRecordGate (a p : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![a,-p,0,0; p,a,0,0; 0,0,a,-p; 0,0,p,a]

def goldenSystemGate (a p : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![a,0,-p,0; 0,a,0,-p; p,0,a,0; 0,p,0,a]

def retainedCopy : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1,0,0,0; 0,1,0,0; 0,0,0,1; 0,0,1,0]

theorem copy_from_owned_record (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    D0.Representation.GoldenCoherentMemory.fullStep a p *
      (goldenSystemGate a p).transpose = retainedCopy := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [D0.Representation.GoldenCoherentMemory.fullStep,
      goldenSystemGate,retainedCopy,Matrix.mul_apply,Fin.sum_univ_succ] <;> nlinarith

def controlledGoldenSquare (a p : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1,0,0,0; 0,1,0,0;
     0,0,a^2-p^2,-2*a*p; 0,0,2*a*p,a^2-p^2]

theorem golden_controlled_square_word (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    goldenRecordGate a p * retainedCopy *
      (goldenRecordGate a p).transpose * retainedCopy =
      controlledGoldenSquare a p := by
  have hi : (goldenRecordGate a p).transpose=goldenRecordGate a (-p) := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [goldenRecordGate,Matrix.transpose_apply]
  rw [hi]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [goldenRecordGate,retainedCopy,controlledGoldenSquare,
      Matrix.mul_apply,Fin.sum_univ_succ] <;> nlinarith

def goldenPhase (a p : ℝ) : ℂ :=
  ((a : ℂ)+Complex.I*(p : ℂ))^2

theorem golden_phase_components (a p : ℝ) (ha : a^2=p) :
    (goldenPhase a p).re=p-p^2 ∧
    (goldenPhase a p).im=2*a*p := by
  unfold goldenPhase
  constructor <;> simp [pow_two,Complex.mul_re,Complex.mul_im] <;> nlinarith

theorem golden_phase_normSq (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    Complex.normSq (goldenPhase a p)=1 := by
  have h := golden_phase_components a p ha
  rw [Complex.normSq_apply,h.1,h.2]
  have hha := congrArg (fun x : ℝ => x*p^2) ha
  have hhp := congrArg (fun x : ℝ => x^2) hp
  nlinarith

theorem unit_phase_quadratic (w : ℂ) (hw : Complex.normSq w=1) :
    w^2-(2*w.re : ℝ)*w+1=0 := by
  apply Complex.ext
  · simp [pow_two,Complex.mul_re,Complex.normSq_apply] at hw ⊢
    nlinarith
  · simp [pow_two,Complex.mul_im]
    ring

def badMultiplier (w : ℂ) (e : ℝ) : ℂ :=
  1+(w-1)*(w*(1-(e : ℂ))+(e : ℂ))

theorem coherent_bad_multiplier (w : ℂ) (e : ℝ)
    (hw : Complex.normSq w=1) :
    badMultiplier w e = w*((2*w.re-1+2*(1-w.re)*e : ℝ) : ℂ) := by
  have h := unit_phase_quadratic w hw
  push_cast at h
  unfold badMultiplier
  push_cast
  linear_combination (1-(e : ℂ))*h

def contractionParameter (p : ℝ) : ℝ := 3-4*p

theorem actual_golden_bad_multiplier (a p e : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    badMultiplier (goldenPhase a p) e =
      goldenPhase a p *
        ((-contractionParameter p+(1+contractionParameter p)*e : ℝ) : ℂ) := by
  rw [coherent_bad_multiplier _ _ (golden_phase_normSq a p ha hp),
    (golden_phase_components a p ha).1]
  congr 2
  unfold contractionParameter
  linear_combination -2*(1-e)*hp

theorem golden_coherent_failure_law (a p e : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    Complex.normSq (badMultiplier (goldenPhase a p) e)=
      (-contractionParameter p+(1+contractionParameter p)*e)^2 := by
  rw [actual_golden_bad_multiplier a p e ha hp,Complex.normSq_mul,
    golden_phase_normSq a p ha hp]
  simp [Complex.normSq_apply,pow_two]

def improveFailure (q e : ℝ) : ℝ := e*(-q+(1+q)*e)^2

theorem generic_retained_contraction (q e : ℝ)
    (hq : 11/21 ≤ q) (hq1 : q<1)
    (he : 0≤e) (he1 : e≤11/16) :
    0 ≤ improveFailure q e ∧ improveFailure q e ≤ q^2*e := by
  have hq0 : 0≤q := by linarith
  have hlo : -q ≤ -q+(1+q)*e := by nlinarith
  have hhi : -q+(1+q)*e ≤ q := by nlinarith
  have hs : (-q+(1+q)*e)^2 ≤ q^2 := by
    nlinarith [mul_nonneg (by linarith : 0≤q-(-q+(1+q)*e))
      (by linarith : 0≤q+(-q+(1+q)*e))]
  unfold improveFailure
  exact ⟨mul_nonneg he (sq_nonneg _),by nlinarith [mul_nonneg he (sub_nonneg.mpr hs)]⟩

def retainedFailure (q e : ℝ) : ℕ → ℝ
  | 0 => e
  | k+1 => improveFailure q (retainedFailure q e k)

theorem all_retained_contraction (q e : ℝ)
    (hq : 11/21 ≤ q) (hq1 : q<1)
    (he : 0≤e) (he1 : e≤11/16) (k : ℕ) :
    0≤retainedFailure q e k ∧
    retainedFailure q e k≤e ∧
    retainedFailure q e k≤(q^2)^k*e := by
  have hq0 : 0≤q := by linarith
  have hq2 : q^2≤1 := by nlinarith
  induction k with
  | zero => simp [retainedFailure,he]
  | succ k ih =>
    have hc := generic_retained_contraction q (retainedFailure q e k)
      hq hq1 ih.1 (ih.2.1.trans he1)
    change 0 ≤ improveFailure q (retainedFailure q e k) ∧ _
    refine ⟨hc.1,?_,?_⟩
    · exact (hc.2.trans (by nlinarith [mul_nonneg ih.1 (sub_nonneg.mpr hq2)])).trans ih.2.1
    · change improveFailure q (retainedFailure q e k)≤_
      rw [pow_succ]
      nlinarith [mul_nonneg (sq_nonneg q) (sub_nonneg.mpr ih.2.2)]

theorem frozen_golden_contraction_bounds (p : ℝ)
    (hp : p+p^2=1) (hp0 : 0<p) :
    11/21<contractionParameter p ∧
    contractionParameter p<p ∧ p<1 := by
  have hp1 : p<1 := by nlinarith [sq_pos_of_pos hp0]
  have hl : 3/5<p := by
    by_contra hn
    have h : p≤3/5 := le_of_not_gt hn
    nlinarith [mul_nonneg (le_of_lt hp0) (sub_nonneg.mpr h)]
  have hh : p<13/21 := by
    by_contra hn
    have h : 13/21≤p := le_of_not_gt hn
    nlinarith [mul_nonneg (by norm_num : (0:ℝ)≤13/21) (sub_nonneg.mpr h)]
  unfold contractionParameter
  exact ⟨by linarith,by linarith,hp1⟩

def preparedRotation (g b : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![(g : ℂ),-(b : ℂ);(b : ℂ),(g : ℂ)]

def selectivePhase (w : ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![w,0;0,1]

def completeAmplifiedWord (g b : ℝ) (w : ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  preparedRotation g b * selectivePhase w *
    (preparedRotation g b).conjTranspose * selectivePhase w * preparedRotation g b

theorem preparedRotation_conjTranspose (g b : ℝ) :
    (preparedRotation g b).conjTranspose=preparedRotation g (-b) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [preparedRotation,Matrix.conjTranspose_apply]

theorem preparedRotation_unitary (g b : ℝ) (hn : g^2+b^2=1) :
    (preparedRotation g b).conjTranspose * preparedRotation g b=1 ∧
    preparedRotation g b*(preparedRotation g b).conjTranspose=1 := by
  constructor <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [preparedRotation,Matrix.conjTranspose_apply,Matrix.mul_apply,Fin.sum_univ_two]
    <;> norm_cast <;> nlinarith

theorem selectivePhase_unitary (w : ℂ) (hw : Complex.normSq w=1) :
    (selectivePhase w).conjTranspose*selectivePhase w=1 ∧
    selectivePhase w*(selectivePhase w).conjTranspose=1 := by
  have hc : star w*w=1 := by
    simpa using (Complex.normSq_eq_conj_mul_self (z:=w)).symm.trans
      (congrArg (fun x : ℝ => (x : ℂ)) hw)
  change (starRingEnd ℂ) w*w=1 at hc
  constructor <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [selectivePhase,Matrix.conjTranspose_apply,Matrix.mul_apply,
      Fin.sum_univ_two,hc,mul_comm w]

theorem complete_word_unitary (g b : ℝ) (w : ℂ)
    (hn : g^2+b^2=1) (hw : Complex.normSq w=1) :
    (completeAmplifiedWord g b w).conjTranspose*completeAmplifiedWord g b w=1 := by
  have hu := preparedRotation_unitary g b hn
  have hp := selectivePhase_unitary w hw
  unfold completeAmplifiedWord
  simp only [Matrix.conjTranspose_mul,Matrix.conjTranspose_conjTranspose]
  simp only [Matrix.mul_assoc]
  simp only [← Matrix.mul_assoc,hu.1,hu.2,hp.1,Matrix.one_mul]

theorem complete_word_bad_component (g b : ℝ) (w : ℂ)
    (hn : g^2+b^2=1) :
    ((completeAmplifiedWord g b w).mulVec ![1,0]) 1=
      (b : ℂ)*badMultiplier w (b^2) := by
  have hc := congrArg (fun x : ℝ => (x : ℂ)) hn
  push_cast at hc
  unfold completeAmplifiedWord
  rw [preparedRotation_conjTranspose]
  simp only [← Matrix.mulVec_mulVec]
  simp [preparedRotation,selectivePhase,badMultiplier,
    Matrix.mulVec,
    dotProduct,Fin.sum_univ_two]
  push_cast
  linear_combination (b : ℂ)*(w^2-w+1)*hc

theorem complete_word_good_component (g b : ℝ) (w : ℂ)
    (hn : g^2+b^2=1) :
    ((completeAmplifiedWord g b w).mulVec ![1,0]) 0=
      (g : ℂ)*(w^2-(w-1)^2*(b^2 : ℝ)) := by
  have hc := congrArg (fun x : ℝ => (x : ℂ)) hn
  push_cast at hc
  unfold completeAmplifiedWord
  rw [preparedRotation_conjTranspose]
  simp only [← Matrix.mulVec_mulVec]
  simp [preparedRotation,selectivePhase,Matrix.mulVec,dotProduct,Fin.sum_univ_two]
  push_cast
  linear_combination (g : ℂ)*w^2*hc

theorem full_word_golden_failure_probability (a p g b : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hn : g^2+b^2=1) :
    Complex.normSq (((completeAmplifiedWord g b (goldenPhase a p)).mulVec ![1,0]) 1)=
      improveFailure (contractionParameter p) (b^2) := by
  rw [complete_word_bad_component g b _ hn,Complex.normSq_mul,
    golden_coherent_failure_law a p (b^2) ha hp]
  simp [improveFailure,pow_two]

theorem golden_pair_realification (a p : ℝ) (ha : a^2=p) :
    !![(goldenPhase a p).re,-(goldenPhase a p).im;
       (goldenPhase a p).im,(goldenPhase a p).re] =
      gate a p*gate a p := by
  rw [(golden_phase_components a p ha).1,(golden_phase_components a p ha).2]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [gate,Matrix.mul_apply,Fin.sum_univ_two] <;> nlinarith

theorem phase_aligned_complete_state_error (u v : ℂ)
    (hn : Complex.normSq u+Complex.normSq v=1) (hu : u≠0) :
    Complex.normSq (u-u/((‖u‖ : ℝ) : ℂ))+Complex.normSq v ≤
      2*Complex.normSq v := by
  have hnorm : 0<‖u‖ := norm_pos_iff.mpr hu
  have husq : Complex.normSq u=‖u‖^2 := Complex.normSq_eq_norm_sq u
  have hule : ‖u‖≤1 := by nlinarith [Complex.normSq_nonneg v]
  have he : u-u/((‖u‖ : ℝ) : ℂ)=
      u*((1-1/‖u‖ : ℝ) : ℂ) := by push_cast; ring
  rw [he,Complex.normSq_mul,Complex.normSq_ofReal,husq]
  have halg : ‖u‖^2*((1-1/‖u‖)*(1-1/‖u‖))=(1-‖u‖)^2 := by
    field_simp
    ring
  rw [halg]
  nlinarith [Complex.normSq_nonneg v]

theorem retained_golden_depth_rate (p e : ℝ)
    (hp : p+p^2=1) (hp0 : 0<p)
    (he : 0≤e) (he1 : e≤11/16) (k : ℕ) :
    retainedFailure (contractionParameter p) e k ≤ p^(2*k)*e := by
  have hb := frozen_golden_contraction_bounds p hp hp0
  have hc := all_retained_contraction (contractionParameter p) e
    (le_of_lt hb.1) (hb.2.1.trans hb.2.2) he he1 k
  have hq0 : 0≤contractionParameter p := by linarith [hb.1]
  have hpow := pow_le_pow_left₀ hq0 (le_of_lt hb.2.1) (2*k)
  have heq : (contractionParameter p^2)^k=contractionParameter p^(2*k) :=
    (pow_mul _ 2 k).symm
  rw [heq] at hc
  exact hc.2.2.trans (mul_le_mul_of_nonneg_right hpow he)

end
end D0.Research.GoldenCoherentAmplification
namespace D0.Research.GoldenCoherentAmplification
noncomputable section
open D0.Research.GoldenHistoryPreparation

theorem native_preparation_enters_retained_contraction (a p d : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hd0 : 20≤d) (hd1 : d≤24) :
    0 ≤ historyFailure a p d ∧ historyFailure a p d ≤ 11/16 := by
  have h := native_degree_retained_preparation_rate a p d ha hp hp0 hd0 hd1
  have hb := frozen_golden_contraction_bounds p hp hp0
  unfold contractionParameter at hb
  exact ⟨h.1,by linarith⟩

theorem native_preparation_coherent_failure_rate (a p d : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hd0 : 20≤d) (hd1 : d≤24) (k : ℕ) :
    retainedFailure (contractionParameter p) (historyFailure a p d) k ≤ p^(2*k) := by
  have h := native_preparation_enters_retained_contraction a p d ha hp hp0 hd0 hd1
  have hs := native_degree_retained_preparation_rate a p d ha hp hp0 hd0 hd1
  have hc := retained_golden_depth_rate p _ hp hp0 h.1 h.2 k
  have hm := mul_le_mul_of_nonneg_left (le_of_lt hs.2.2)
    (pow_nonneg (le_of_lt hp0) (2*k))
  simpa using hc.trans hm

theorem frozen_three_native_degrees_coherent_failure_rate (d : ℝ)
    (hd : d=20 ∨ d=22 ∨ d=24) (k : ℕ) :
    let p := D0.primitiveRoot
    let a := Real.sqrt p
    retainedFailure (contractionParameter p) (historyFailure a p d) k ≤ p^(2*k) := by
  dsimp
  have hp0 := D0.Representation.GoldenOrderInterferometer.primitive_positive
  apply native_preparation_coherent_failure_rate _ _ d (Real.sq_sqrt (le_of_lt hp0))
    D0.primitive_root_satisfies hp0
  · rcases hd with h|h|h <;> rw [h] <;> norm_num
  · rcases hd with h|h|h <;> rw [h] <;> norm_num

theorem native_complete_state_error_after_declared_phase_alignment (a p d : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hd0 : 20≤d) (hd1 : d≤24) (k : ℕ) (u v : ℂ)
    (hn : Complex.normSq u+Complex.normSq v=1) (hu : u≠0)
    (hv : Complex.normSq v≤retainedFailure (contractionParameter p)
      (historyFailure a p d) k) :
    Complex.normSq (u-u/((‖u‖ : ℝ) : ℂ))+Complex.normSq v ≤ 2*p^(2*k) := by
  have hs := phase_aligned_complete_state_error u v hn hu
  have hc := native_preparation_coherent_failure_rate a p d ha hp hp0 hd0 hd1 k
  exact hs.trans (by linarith [hv.trans hc])

end
end D0.Research.GoldenCoherentAmplification
namespace D0.Research.GoldenCoherentAmplification
noncomputable section
open Matrix Complex
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def vectorWeight (x : ι → ℂ) : ℝ := ∑ i, Complex.normSq (x i)
def rejectedWeight (χ : ι → Bool) (x : ι → ℂ) : ℝ :=
  ∑ i, if χ i then 0 else Complex.normSq (x i)
def acceptedWeight (χ : ι → Bool) (x : ι → ℂ) : ℝ :=
  ∑ i, if χ i then Complex.normSq (x i) else 0

theorem complete_weight_partition (χ : ι → Bool) (x : ι → ℂ) :
    acceptedWeight χ x+rejectedWeight χ x=vectorWeight x := by
  rw [acceptedWeight,rejectedWeight,← Finset.sum_add_distrib]
  unfold vectorWeight
  apply Finset.sum_congr rfl
  intro i _
  cases χ i <;> simp

theorem rejected_weight_nonnegative (χ : ι → Bool) (x : ι → ℂ) :
    0 ≤ rejectedWeight χ x := by
  apply Finset.sum_nonneg
  intro i _
  cases χ i <;> simp [Complex.normSq_nonneg]

def diagonalPhase (χ : ι → Bool) (w : ℂ) : Matrix ι ι ℂ :=
  Matrix.diagonal (fun i => if χ i then w else 1)

theorem diagonal_phase_unitary (χ : ι → Bool) (w : ℂ)
    (hw : Complex.normSq w=1) :
    (diagonalPhase χ w).conjTranspose*diagonalPhase χ w=1 ∧
    diagonalPhase χ w*(diagonalPhase χ w).conjTranspose=1 := by
  have hc : star w*w=1 := by
    simpa using (Complex.normSq_eq_conj_mul_self (z:=w)).symm.trans
      (congrArg (fun x : ℝ => (x : ℂ)) hw)
  change (starRingEnd ℂ) w*w=1 at hc
  constructor <;> unfold diagonalPhase <;>
    rw [Matrix.diagonal_conjTranspose,Matrix.diagonal_mul_diagonal,
      ← Matrix.diagonal_one]
  · congr 1
    funext i
    cases h : χ i <;> simp [h,hc]
  · congr 1
    funext i
    cases h : χ i <;> simp [h,hc,mul_comm w]

def blankVector (z : ι) : ι → ℂ := Pi.single z 1

def blankPhase (z : ι) (w : ℂ) : Matrix ι ι ℂ :=
  diagonalPhase (fun i => decide (i=z)) w

theorem blank_phase_complete_projector (z : ι) (w : ℂ) :
    blankPhase z w=1+(w-1) • Matrix.vecMulVec (blankVector z) (star (blankVector z)) := by
  ext i j
  by_cases hij : i=j
  · subst j
    by_cases hi : i=z <;>
      simp [blankPhase,diagonalPhase,blankVector,Matrix.diagonal_apply,
        Matrix.one_apply,Matrix.vecMulVec,Pi.single_apply,hi]
  · by_cases hi : i=z <;> by_cases hj : j=z <;>
      simp_all [blankPhase,diagonalPhase,blankVector,Matrix.diagonal_apply,
        Matrix.one_apply,Matrix.vecMulVec,Pi.single_apply]

theorem unitary_column_has_complete_weight (U : Matrix ι ι ℂ) (z : ι)
    (hu : U.conjTranspose*U=1) :
    vectorWeight (fun i => U i z)=1 := by
  have hc : ((vectorWeight (fun i => U i z) : ℝ) : ℂ)=
      (U.conjTranspose*U) z z := by
    unfold vectorWeight
    push_cast
    simp [Matrix.mul_apply,Matrix.conjTranspose_apply,
      Complex.normSq_eq_conj_mul_self,Complex.star_def]
  rw [hu] at hc
  simp only [Matrix.one_apply_eq] at hc
  exact_mod_cast hc

def fullAmplify (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool) (w : ℂ) : Matrix ι ι ℂ :=
  U*blankPhase z w*U.conjTranspose*diagonalPhase χ w*U

theorem full_amplify_unitary (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool) (w : ℂ)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) (hw : Complex.normSq w=1) :
    (fullAmplify U z χ w).conjTranspose*fullAmplify U z χ w=1 ∧
    fullAmplify U z χ w*(fullAmplify U z χ w).conjTranspose=1 := by
  have h0 := diagonal_phase_unitary (fun i => decide (i=z)) w hw
  have h1 := diagonal_phase_unitary χ w hw
  constructor <;> unfold fullAmplify blankPhase <;>
    simp only [Matrix.conjTranspose_mul,Matrix.conjTranspose_conjTranspose] <;>
    simp only [Matrix.mul_assoc] <;>
    simp only [← Matrix.mul_assoc,hU.1,hU.2,h0.1,h0.2,h1.1,h1.2,
      Matrix.one_mul,Matrix.mul_one]

theorem full_prepared_phase_conjugation (U : Matrix ι ι ℂ) (z : ι) (w : ℂ)
    (hu : U*U.conjTranspose=1) :
    U*blankPhase z w*U.conjTranspose=
      1+(w-1) • Matrix.vecMulVec (fun i => U i z) (star (fun i => U i z)) := by
  rw [blank_phase_complete_projector,Matrix.mul_add,Matrix.add_mul,
    Matrix.mul_smul,Matrix.smul_mul,Matrix.mul_one,hu]
  congr 1
  rw [Matrix.mul_vecMulVec,Matrix.vecMulVec_mul]
  have hs : star (blankVector z)=blankVector z := by
    funext i
    simp [blankVector,Pi.single_apply]
  rw [← hs,Matrix.vecMul_conjTranspose]
  simp [blankVector,Matrix.mulVec_single_one,Matrix.col_apply]
  rfl

theorem complete_phase_expectation (χ : ι → Bool) (x : ι → ℂ) (w : ℂ)
    (hn : vectorWeight x=1) :
    (star x) ⬝ᵥ ((diagonalPhase χ w).mulVec x)=
      w*(1-(rejectedWeight χ x : ℂ))+(rejectedWeight χ x : ℂ) := by
  have hp := complete_weight_partition χ x
  rw [hn] at hp
  have h : (star x) ⬝ᵥ ((diagonalPhase χ w).mulVec x)=
      w*(acceptedWeight χ x : ℂ)+(rejectedWeight χ x : ℂ) := by
    unfold diagonalPhase acceptedWeight rejectedWeight
    simp only [Matrix.mulVec_diagonal,dotProduct,Pi.star_apply]
    push_cast
    rw [Finset.mul_sum,← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro i _
    cases h : χ i <;> simp [h,Complex.normSq_eq_conj_mul_self,Complex.star_def] <;> ring
  rw [h]
  have he : acceptedWeight χ x=1-rejectedWeight χ x := by linarith
  rw [he]
  push_cast
  rfl

theorem full_amplify_column (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool) (w : ℂ)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) (i : ι) :
    fullAmplify U z χ w i z=
      U i z*((if χ i then w else 1)+(w-1)*
        (w*(1-(rejectedWeight χ (fun j => U j z) : ℂ))+
          (rejectedWeight χ (fun j => U j z) : ℂ))) := by
  have hn := unitary_column_has_complete_weight U z hU.1
  have hE := complete_phase_expectation χ (fun j => U j z) w hn
  have hconj := full_prepared_phase_conjugation U z w hU.2
  change ((U*blankPhase z w*U.conjTranspose)*diagonalPhase χ w*U) i z=_
  rw [hconj]
  have hvec : ((1+(w-1) • Matrix.vecMulVec (fun j => U j z) (star (fun j => U j z)))*
      diagonalPhase χ w*U).mulVec (blankVector z)=
      ((diagonalPhase χ w).mulVec (fun j => U j z))+
        (w-1) • ((Matrix.vecMulVec (fun j => U j z) (star (fun j => U j z))).mulVec
          ((diagonalPhase χ w).mulVec (fun j => U j z))) := by
    unfold blankVector
    rw [← Matrix.mulVec_mulVec,← Matrix.mulVec_mulVec,Matrix.mulVec_single_one]
    change (1+(w-1) • Matrix.vecMulVec (fun j => U j z) (star (fun j => U j z))).mulVec
      ((diagonalPhase χ w).mulVec (fun j => U j z))=_
    rw [Matrix.add_mulVec,Matrix.one_mulVec,Matrix.smul_mulVec]
  have hi := congrFun hvec i
  simp only [blankVector,Matrix.mulVec_single_one,Matrix.vecMulVec_mulVec,
    Pi.add_apply,Pi.smul_apply,smul_eq_mul,hE] at hi
  simp only [Matrix.col_apply] at hi
  rw [hi]
  cases hχ : χ i <;>
    simp [diagonalPhase,Matrix.mulVec_diagonal,smul_eq_mul,hχ] <;> ring

theorem all_failed_coordinates_keep_original_record (U : Matrix ι ι ℂ)
    (z : ι) (χ : ι → Bool) (w : ℂ)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) (i : ι) (hi : χ i=false) :
    fullAmplify U z χ w i z=U i z*badMultiplier w (rejectedWeight χ (fun j => U j z)) := by
  rw [full_amplify_column U z χ w hU i,hi]
  simp [badMultiplier]

theorem complete_failed_weight_law (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool) (w : ℂ)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) :
    rejectedWeight χ (fun i => fullAmplify U z χ w i z)=
      rejectedWeight χ (fun i => U i z)*
        Complex.normSq (badMultiplier w (rejectedWeight χ (fun i => U i z))) := by
  unfold rejectedWeight at *
  rw [Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro i _
  cases hi : χ i
  · simp only [Bool.false_eq_true,if_false]
    change Complex.normSq (fullAmplify U z χ w i z)=_
    rw [all_failed_coordinates_keep_original_record U z χ w hU i hi]
    rw [Complex.normSq_mul]
    rfl
  · simp [hi]

def fullWord (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool) (w : ℂ) : ℕ → Matrix ι ι ℂ
  | 0 => U
  | k+1 => fullAmplify (fullWord U z χ w k) z χ w

theorem all_full_words_unitary (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool) (w : ℂ)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) (hw : Complex.normSq w=1) (k : ℕ) :
    (fullWord U z χ w k).conjTranspose*fullWord U z χ w k=1 ∧
      fullWord U z χ w k*(fullWord U z χ w k).conjTranspose=1 := by
  induction k with
  | zero => exact hU
  | succ k ih => exact full_amplify_unitary _ _ _ _ ih hw

theorem actual_full_word_golden_failure (a p : ℝ) (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) (k : ℕ) :
    rejectedWeight χ (fun i => fullWord U z χ (goldenPhase a p) k i z)=
      retainedFailure (contractionParameter p) (rejectedWeight χ (fun i => U i z)) k := by
  induction k with
  | zero => rfl
  | succ k ih =>
    change rejectedWeight χ (fun i => fullAmplify (fullWord U z χ (goldenPhase a p) k)
      z χ (goldenPhase a p) i z)=_
    rw [complete_failed_weight_law _ z χ _
      (all_full_words_unitary U z χ _ hU (golden_phase_normSq a p ha hp) k),
      golden_coherent_failure_law a p _ ha hp,ih]
    rfl

end
end D0.Research.GoldenCoherentAmplification
namespace D0.Research.GoldenCoherentAmplification
noncomputable section
open Complex Matrix
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def fastGoldenPhase (a p : ℝ) : ℂ := goldenPhase a p^4
def fastParameter (p : ℝ) : ℝ := 1345-2176*p

theorem fourth_unit_phase_real (w : ℂ) (hw : Complex.normSq w=1) :
    (w^4).re=8*w.re^4-8*w.re^2+1 := by
  have hn : w.re^2+w.im^2=1 := by simpa [Complex.normSq_apply,pow_two] using hw
  rw [show w^4=(w*w)*(w*w) by ring]
  simp [Complex.mul_re,Complex.mul_im]
  linear_combination (w.im^2-7*w.re^2+1)*hn

theorem fast_golden_phase_real (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    (fastGoldenPhase a p).re=673-1088*p := by
  unfold fastGoldenPhase
  rw [fourth_unit_phase_real _ (golden_phase_normSq a p ha hp),
    (golden_phase_components a p ha).1]
  have he : p-p^2=2*p-1 := by nlinarith
  rw [he]
  linear_combination (128*p^2-384*p+672)*hp

theorem fast_golden_phase_normSq (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    Complex.normSq (fastGoldenPhase a p)=1 := by
  simp [fastGoldenPhase,map_pow,golden_phase_normSq a p ha hp]

theorem fast_parameter_native_bounds (p : ℝ) (hp : p+p^2=1) (hp0 : 0<p) :
    0<fastParameter p ∧ fastParameter p<1/6 := by
  have hl : (8069/13056 : ℝ)<p := by
    by_contra hn
    have h : p≤8069/13056 := le_of_not_gt hn
    nlinarith [mul_nonneg (le_of_lt hp0) (sub_nonneg.mpr h)]
  have hh : p<(1345/2176 : ℝ) := by
    by_contra hn
    have h : 1345/2176≤p := le_of_not_gt hn
    nlinarith [mul_nonneg (by norm_num : (0:ℝ)≤1345/2176) (sub_nonneg.mpr h)]
  unfold fastParameter
  constructor <;> linarith

theorem fast_actual_bad_multiplier (a p e : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    badMultiplier (fastGoldenPhase a p) e=fastGoldenPhase a p*
      ((fastParameter p+(1-fastParameter p)*e : ℝ) : ℂ) := by
  rw [coherent_bad_multiplier _ _ (fast_golden_phase_normSq a p ha hp),
    fast_golden_phase_real a p ha hp]
  congr 2
  unfold fastParameter
  ring

def fastImprove (r e : ℝ) : ℝ := e*(r+(1-r)*e)^2
def fastFailure (r e : ℝ) : ℕ → ℝ
  | 0 => e
  | k+1 => fastImprove r (fastFailure r e k)

theorem fast_actual_failure_law (a p e : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    e*Complex.normSq (badMultiplier (fastGoldenPhase a p) e)=fastImprove (fastParameter p) e := by
  rw [fast_actual_bad_multiplier a p e ha hp,Complex.normSq_mul,
    fast_golden_phase_normSq a p ha hp]
  simp [fastImprove,Complex.normSq_apply,pow_two]

theorem fast_burnin_first (r e : ℝ) (hr0 : 0≤r) (hr1 : r≤1/6)
    (he0 : 0≤e) (he1 : e≤11/16) :
    0 ≤ fastImprove r e ∧ fastImprove r e ≤ 2/5 := by
  have hf0 : 0≤r+(1-r)*e := by nlinarith
  have hmon := mul_nonneg (sub_nonneg.mpr hr1) (show 0≤1-e by linarith)
  have hf1 : r+(1-r)*e ≤ 71/96 := by nlinarith
  have hsq : (r+(1-r)*e)^2≤(71/96)^2 := by nlinarith
  unfold fastImprove
  constructor
  · exact mul_nonneg he0 (sq_nonneg _)
  · have hm0 := mul_nonneg he0 (sub_nonneg.mpr hsq)
    have hm1 := mul_nonneg (sq_nonneg (71/96:ℝ)) (sub_nonneg.mpr he1)
    nlinarith

theorem fast_burnin_second (r e : ℝ) (hr0 : 0≤r) (hr1 : r≤1/6)
    (he0 : 0≤e) (he1 : e≤2/5) :
    0 ≤ fastImprove r e ∧ fastImprove r e ≤ 1/10 := by
  have hf0 : 0≤r+(1-r)*e := by nlinarith
  have hmon := mul_nonneg (sub_nonneg.mpr hr1) (show 0≤1-e by linarith)
  have hf1 : r+(1-r)*e ≤ 1/2 := by nlinarith
  have hsq : (r+(1-r)*e)^2≤(1/2)^2 := by nlinarith
  unfold fastImprove
  constructor
  · exact mul_nonneg he0 (sq_nonneg _)
  · have hm0 := mul_nonneg he0 (sub_nonneg.mpr hsq)
    have hm1 := mul_nonneg (sq_nonneg (1/2:ℝ)) (sub_nonneg.mpr he1)
    nlinarith

theorem fast_small_error_contraction (r e : ℝ) (hr0 : 0≤r) (hr1 : r≤1/6)
    (he0 : 0≤e) (he1 : e≤1/10) :
    0 ≤ fastImprove r e ∧ fastImprove r e ≤ e/16 := by
  have hf0 : 0≤r+(1-r)*e := by nlinarith
  have hmon := mul_nonneg (sub_nonneg.mpr hr1) (show 0≤1-e by linarith)
  have hf1 : r+(1-r)*e ≤ 1/4 := by nlinarith
  have hsq : (r+(1-r)*e)^2≤(1/4)^2 := by nlinarith
  unfold fastImprove
  exact ⟨mul_nonneg he0 (sq_nonneg _),by
    nlinarith [mul_nonneg he0 (sub_nonneg.mpr hsq)]⟩

theorem fast_two_stage_burnin (r e : ℝ) (hr0 : 0≤r) (hr1 : r≤1/6)
    (he0 : 0≤e) (he1 : e≤11/16) :
    0 ≤ fastFailure r e 2 ∧ fastFailure r e 2 ≤ 1/10 := by
  have h0 := fast_burnin_first r e hr0 hr1 he0 he1
  exact fast_burnin_second r _ hr0 hr1 h0.1 h0.2

theorem fast_all_full_failure_rate (r e : ℝ) (hr0 : 0≤r) (hr1 : r≤1/6)
    (he0 : 0≤e) (he1 : e≤11/16) (k : ℕ) :
    0 ≤ fastFailure r e (k+2) ∧
    fastFailure r e (k+2)≤1/10 ∧
    fastFailure r e (k+2)≤(1/16)^k/10 := by
  induction k with
  | zero =>
    have h := fast_two_stage_burnin r e hr0 hr1 he0 he1
    exact ⟨h.1,h.2,by simpa using h.2⟩
  | succ k ih =>
    have h := fast_small_error_contraction r (fastFailure r e (k+2)) hr0 hr1 ih.1 ih.2.1
    have heq : k+1+2=(k+2)+1 := by omega
    rw [heq]
    change 0 ≤ fastImprove r (fastFailure r e (k+2)) ∧
      fastImprove r (fastFailure r e (k+2))≤1/10 ∧
      fastImprove r (fastFailure r e (k+2))≤(1/16)^(k+1)/10
    refine ⟨h.1,by linarith,?_⟩
    rw [pow_succ]
    nlinarith

theorem actual_full_word_fast_failure (a p : ℝ) (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) (k : ℕ) :
    rejectedWeight χ (fun i => fullWord U z χ (fastGoldenPhase a p) k i z)=
      fastFailure (fastParameter p) (rejectedWeight χ (fun i => U i z)) k := by
  induction k with
  | zero => rfl
  | succ k ih =>
    change rejectedWeight χ (fun i => fullAmplify (fullWord U z χ (fastGoldenPhase a p) k)
      z χ (fastGoldenPhase a p) i z)=_
    rw [complete_failed_weight_law _ z χ _
      (all_full_words_unitary U z χ _ hU (fast_golden_phase_normSq a p ha hp) k),
      fast_actual_failure_law a p _ ha hp,ih]
    rfl

def expandedCost (seed phase : ℕ) : ℕ → ℕ
  | 0 => seed
  | k+1 => 3*expandedCost seed phase k+2*phase

theorem actual_expanded_word_cost (seed phase k : ℕ) :
    expandedCost seed phase k+phase=3^k*(seed+phase) := by
  induction k with
  | zero => simp [expandedCost]
  | succ k ih =>
    simp only [expandedCost,pow_succ]
    nlinarith

theorem fast_failure_better_than_expanded_inverse_square (r e : ℝ)
    (hr0 : 0≤r) (hr1 : r≤1/6) (he0 : 0≤e) (he1 : e≤11/16) (k : ℕ) :
    fastFailure r e (k+2)*(3^k : ℝ)^2 ≤ 1/10 := by
  have hf := fast_all_full_failure_rate r e hr0 hr1 he0 he1 k
  have heq : (3^k : ℝ)^2=9^k := by
    rw [← pow_mul, Nat.mul_comm k 2,pow_mul]
    norm_num
  rw [heq]
  have hh := pow_le_pow_left₀ (by norm_num : (0:ℝ)≤9/16)
    (by norm_num : (9/16:ℝ)≤1) k
  have hprod : ((1/16:ℝ)^k/10)*9^k=(9/16:ℝ)^k/10 := by
    calc _ = ((1/16:ℝ)^k*9^k)/10 := by ring
         _ = _ := by rw [← mul_pow]; norm_num
  have hm := mul_le_mul_of_nonneg_right hf.2.2 (pow_nonneg (by norm_num : (0:ℝ)≤9) k)
  rw [hprod] at hm
  simp only [one_pow] at hh
  linarith


theorem fast_failure_with_literal_word_cost (r e : ℝ) (seed phase k : ℕ)
    (hr0 : 0≤r) (hr1 : r≤1/6) (he0 : 0≤e) (he1 : e≤11/16) :
    fastFailure r e (k+2)*((expandedCost seed phase (k+2)+phase : ℕ) : ℝ)^2 ≤
      (81/10)*((seed+phase : ℕ) : ℝ)^2 := by
  have hh := fast_failure_better_than_expanded_inverse_square r e hr0 hr1 he0 he1 k
  rw [actual_expanded_word_cost]
  push_cast
  rw [pow_add]
  norm_num
  have hm := mul_le_mul_of_nonneg_right hh (sq_nonneg ((seed+phase : ℕ) : ℝ))
  push_cast at hm
  nlinarith

theorem golden_square_rate_does_not_bound_tripled_word_cost (p : ℝ)
    (hp : p+p^2=1) (hp0 : 0<p) :
    1<9*(contractionParameter p)^2 := by
  have h := frozen_golden_contraction_bounds p hp hp0
  nlinarith

end
end D0.Research.GoldenCoherentAmplification
namespace D0.Research.GoldenCoherentAmplification
noncomputable section
open Matrix Complex D0.Research.GoldenHistoryPreparation
open scoped Kronecker

def boolGoldenGate (a p : ℝ) : Matrix Bool Bool ℂ :=
  fun b c => if b then (if c then (a : ℂ) else (p : ℂ))
    else (if c then -(p : ℂ) else (a : ℂ))

theorem literal_bool_golden_gate_unitary (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    (boolGoldenGate a p).conjTranspose*boolGoldenGate a p=1 ∧
    boolGoldenGate a p*(boolGoldenGate a p).conjTranspose=1 := by
  have hc := congrArg (fun x : ℝ => (x : ℂ)) (show a^2+p^2=1 by rw [ha,hp])
  push_cast at hc
  constructor <;> ext i j <;> cases i <;> cases j <;>
    simp [boolGoldenGate,Matrix.conjTranspose_apply,Matrix.mul_apply,Fintype.sum_bool]
    <;> norm_cast <;> nlinarith

theorem kronecker_retains_all_unitarity {X Y : Type*} [Fintype X] [DecidableEq X]
    [Fintype Y] [DecidableEq Y] (U : Matrix X X ℂ) (V : Matrix Y Y ℂ)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (hV : V.conjTranspose*V=1 ∧ V*V.conjTranspose=1) :
    (U ⊗ₖ V).conjTranspose*(U ⊗ₖ V)=1 ∧
    (U ⊗ₖ V)*(U ⊗ₖ V).conjTranspose=1 := by
  constructor <;> rw [Matrix.conjTranspose_kronecker,← Matrix.mul_kronecker_mul]
  · rw [hU.1,hV.1,Matrix.one_kronecker_one]
  · rw [hU.2,hV.2,Matrix.one_kronecker_one]

def wordBlank : (n : ℕ) → Word n
  | 0 => ()
  | n+1 => ((false,false),wordBlank n)

def wordGoldenSeed (a p : ℝ) : (n : ℕ) → Matrix (Word n) (Word n) ℂ
  | 0 => 1
  | n+1 => (boolGoldenGate a p ⊗ₖ boolGoldenGate a p) ⊗ₖ wordGoldenSeed a p n

theorem actual_word_seed_unitary (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (n : ℕ) :
    (wordGoldenSeed a p n).conjTranspose*wordGoldenSeed a p n=1 ∧
    wordGoldenSeed a p n*(wordGoldenSeed a p n).conjTranspose=1 := by
  induction n with
  | zero => simp [wordGoldenSeed]
  | succ n ih =>
    have hg := literal_bool_golden_gate_unitary a p ha hp
    exact kronecker_retains_all_unitarity _ _
      (kronecker_retains_all_unitarity _ _ hg hg) ih

theorem actual_word_seed_amplitudes (a p : ℝ) (n : ℕ) (w : Word n) :
    wordGoldenSeed a p n w (wordBlank n)=(amplitude a p w : ℝ) := by
  induction n with
  | zero =>
    cases w
    change (1 : Matrix PUnit PUnit ℂ) () ()=1
    simp [Matrix.one_apply]
  | succ n ih =>
    rcases w with ⟨⟨b,c⟩,w⟩
    change ((boolGoldenGate a p b false)*(boolGoldenGate a p c false))*
      wordGoldenSeed a p n w (wordBlank n)=_
    rw [ih]
    cases b <;> cases c <;> simp [boolGoldenGate,amplitude]

def piMatrix {X : Type*} (m : ℕ) (U : Matrix X X ℂ) :
    Matrix (Fin m → X) (Fin m → X) ℂ := fun x y => ∏ i, U (x i) (y i)

theorem pi_matrix_retains_all_unitarity {X : Type*} [Fintype X] [DecidableEq X]
    (m : ℕ) (U : Matrix X X ℂ)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) :
    (piMatrix m U).conjTranspose*piMatrix m U=1 ∧
    piMatrix m U*(piMatrix m U).conjTranspose=1 := by
  constructor
  · ext x y
    simp only [Matrix.mul_apply,Matrix.conjTranspose_apply,piMatrix]
    simp only [star_prod,← Finset.prod_mul_distrib]
    rw [← Fintype.prod_sum (fun (i : Fin m) (z : X) => star (U z (x i))*U z (y i))]
    have he (i : Fin m) : (∑ z : X, star (U z (x i))*U z (y i))=
        if x i=y i then 1 else 0 := by
      have h := congrFun (congrFun hU.1 (x i)) (y i)
      simpa [Matrix.mul_apply,Matrix.conjTranspose_apply,Matrix.one_apply] using h
    simp_rw [he]
    by_cases hxy : x=y
    · subst y; simp
    · have hx : ∃ i, x i≠y i := by contrapose! hxy; exact funext hxy
      rcases hx with ⟨i,hi⟩
      have hz : (∏ j : Fin m, if x j=y j then (1 : ℂ) else 0)=0 := by
        apply Finset.prod_eq_zero (Finset.mem_univ i)
        simp [hi]
      simp [Matrix.one_apply,hxy,hz]
  · ext x y
    simp only [Matrix.mul_apply,Matrix.conjTranspose_apply,piMatrix]
    simp only [star_prod,← Finset.prod_mul_distrib]
    rw [← Fintype.prod_sum (fun (i : Fin m) (z : X) => U (x i) z*star (U (y i) z))]
    have he (i : Fin m) : (∑ z : X, U (x i) z*star (U (y i) z))=
        if x i=y i then 1 else 0 := by
      have h := congrFun (congrFun hU.2 (x i)) (y i)
      simpa [Matrix.mul_apply,Matrix.conjTranspose_apply,Matrix.one_apply] using h
    simp_rw [he]
    by_cases hxy : x=y
    · subst y; simp
    · have hx : ∃ i, x i≠y i := by contrapose! hxy; exact funext hxy
      rcases hx with ⟨i,hi⟩
      have hz : (∏ j : Fin m, if x j=y j then (1 : ℂ) else 0)=0 := by
        apply Finset.prod_eq_zero (Finset.mem_univ i)
        simp [hi]
      simp [Matrix.one_apply,hxy,hz]

abbrev CompleteSeedCarrier (n m : ℕ) := Fin m → Word n × Bool
def completeBlank (n m : ℕ) : CompleteSeedCarrier n m := fun _ => (wordBlank n,false)

def disjointGoldenSeed (a p : ℝ) (n m : ℕ) :
    Matrix (CompleteSeedCarrier n m) (CompleteSeedCarrier n m) ℂ :=
  piMatrix m (wordGoldenSeed a p n ⊗ₖ (1 : Matrix Bool Bool ℂ))

theorem complete_golden_seed_unitary (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (n m : ℕ) :
    (disjointGoldenSeed a p n m).conjTranspose*disjointGoldenSeed a p n m=1 ∧
    disjointGoldenSeed a p n m*(disjointGoldenSeed a p n m).conjTranspose=1 := by
  apply pi_matrix_retains_all_unitarity
  exact kronecker_retains_all_unitarity _ _ (actual_word_seed_unitary a p ha hp n) (by simp)

theorem complete_golden_seed_blank_amplitudes (a p : ℝ) (n m : ℕ)
    (w : Fin m → Word n) :
    disjointGoldenSeed a p n m (fun i => (w i,false)) (completeBlank n m)=
      ((∏ i : Fin m, amplitude a p (w i) : ℝ) : ℂ) := by
  unfold disjointGoldenSeed piMatrix completeBlank
  simp [Matrix.kroneckerMap_apply,actual_word_seed_amplitudes]

theorem full_routing_permutation_unitary {X : Type*} [Fintype X] [DecidableEq X]
    (σ : Equiv.Perm X) :
    (σ.permMatrix ℂ).conjTranspose*σ.permMatrix ℂ=1 ∧
    σ.permMatrix ℂ*(σ.permMatrix ℂ).conjTranspose=1 := by
  simp [Matrix.conjTranspose_permMatrix,← Matrix.permMatrix_mul]

def routedGoldenSeed (a p : ℝ) (n m : ℕ) :
    Matrix (CompleteSeedCarrier n m) (CompleteSeedCarrier n m) ℂ :=
  Equiv.Perm.permMatrix ℂ (tensorRoute n m).symm*disjointGoldenSeed a p n m

theorem actual_retained_routed_seed_unitary (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (n m : ℕ) :
    (routedGoldenSeed a p n m).conjTranspose*routedGoldenSeed a p n m=1 ∧
    routedGoldenSeed a p n m*(routedGoldenSeed a p n m).conjTranspose=1 := by
  have hpM := full_routing_permutation_unitary (tensorRoute n m).symm
  have hg := complete_golden_seed_unitary a p ha hp n m
  unfold routedGoldenSeed
  constructor <;> rw [Matrix.conjTranspose_mul] <;> simp only [Matrix.mul_assoc]
  · simp only [← Matrix.mul_assoc,hpM.1,Matrix.one_mul,hg.1]
  · rw [← Matrix.mul_assoc (disjointGoldenSeed a p n m)]
    rw [hg.2,Matrix.one_mul,hpM.2]

theorem actual_routed_seed_successful_amplitude (a p : ℝ) (n m : ℕ)
    (b : Fin m → Bool) (w : Fin m → Word n)
    (hw : ∀ i, firstLabel (w i)=some false) :
    routedGoldenSeed a p n m (fun i => (w i,b i)) (completeBlank n m)=
      ((∏ i : Fin m, amplitude a p (w i) : ℝ) : ℂ) := by
  have hr := full_successful_code_keeps_same_record n m b w hw
  have hinv : (tensorRoute n m).symm (fun i => (w i,b i))=
      fun i => (rawForCode n m b w i,false) := by
    rw [← hr,Equiv.symm_apply_apply]
  have hs : (routedGoldenSeed a p n m).mulVec (blankVector (completeBlank n m))=
      (disjointGoldenSeed a p n m).mulVec (blankVector (completeBlank n m)) ∘
        (tensorRoute n m).symm := by
    simp [routedGoldenSeed,← Matrix.mulVec_mulVec,Matrix.permMatrix_mulVec]
  have h := congrFun hs (fun i => (w i,b i))
  simp only [blankVector,Matrix.mulVec_single_one,Matrix.col_apply,
    Function.comp_apply,hinv] at h
  rw [h,complete_golden_seed_blank_amplitudes,full_code_coherent_amplitude_independence]

end
end D0.Research.GoldenCoherentAmplification
namespace D0.Research.GoldenCoherentAmplification
noncomputable section
open Matrix Complex D0.Research.GoldenHistoryPreparation

def splitCompleteCarrier (n m : ℕ) : CompleteSeedCarrier n m ≃
    (Fin m → Word n) × (Fin m → Bool) where
  toFun s := (fun i => (s i).1,fun i => (s i).2)
  invFun s := fun i => (s.1 i,s.2 i)
  left_inv s := by funext i; exact Prod.eta (s i)
  right_inv s := by rcases s with ⟨w,b⟩; rfl

def codeValidity (n m : ℕ) (S : Finset (Fin m → Bool)) (s : CompleteSeedCarrier n m) : Bool :=
  decide ((∀ i, firstLabel ((s i).1)=some false) ∧ (fun i => (s i).2)∈S)

theorem complete_all_good_record_mass (a p : ℝ) (n m : ℕ) :
    (∑ w : Fin m → Word n, if (∀ i, firstLabel (w i)=some false)
      then (∏ i : Fin m, amplitude a p (w i))^2 else 0)=
        completeCodeMass a p n m (fun _ => false) := by
  unfold completeCodeMass
  apply Finset.sum_congr rfl
  intro w _
  by_cases h : ∀ i, firstLabel (w i)=some false
  · simp [h,← Finset.prod_pow]
  · push_neg at h
    rcases h with ⟨i,hi⟩
    have hn : ¬∀ j, firstLabel (w j)=some false := by intro h; exact hi (h i)
    rw [if_neg hn]
    symm
    apply Finset.prod_eq_zero (Finset.mem_univ i)
    simp [hi]

theorem complete_retained_seed_valid_mass (a p : ℝ) (n m : ℕ)
    (S : Finset (Fin m → Bool)) :
    acceptedWeight (codeValidity n m S)
      (fun s => routedGoldenSeed a p n m s (completeBlank n m))=
        (S.card : ℝ)*completeCodeMass a p n m (fun _ => false) := by
  unfold acceptedWeight
  rw [← Equiv.sum_comp (splitCompleteCarrier n m).symm
    (fun s => if codeValidity n m S s then
      Complex.normSq (routedGoldenSeed a p n m s (completeBlank n m)) else 0)]
  simp only [Fintype.sum_prod_type]
  have he (w : Fin m → Word n) :
      (∑ b : Fin m → Bool, if codeValidity n m S ((splitCompleteCarrier n m).symm (w,b))
        then Complex.normSq (routedGoldenSeed a p n m ((splitCompleteCarrier n m).symm (w,b))
          (completeBlank n m)) else 0)=
      (S.card : ℝ)*(if (∀ i, firstLabel (w i)=some false)
        then (∏ i : Fin m, amplitude a p (w i))^2 else 0) := by
    change (∑ b : Fin m → Bool, if codeValidity n m S (fun i => (w i,b i))
      then Complex.normSq (routedGoldenSeed a p n m (fun i => (w i,b i))
        (completeBlank n m)) else 0)=_
    by_cases hw : ∀ i, firstLabel (w i)=some false
    · have hc (b : Fin m → Bool) : codeValidity n m S (fun i => (w i,b i))=
          decide (b∈S) := by simp [codeValidity,hw]
      simp_rw [hc,actual_routed_seed_successful_amplitude a p n m _ w hw,
        Complex.normSq_ofReal]
      simp [hw,pow_two]
    · simp [codeValidity,hw]
  simp_rw [he]
  rw [← Finset.mul_sum,complete_all_good_record_mass]

theorem literal_five_stream_seed_valid_mass (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (S : Finset (Fin 5 → Bool)) :
    acceptedWeight (codeValidity 4 5 S)
      (fun s => routedGoldenSeed a p 4 5 s (completeBlank 4 5))=
        historySuccess a p (S.card : ℝ) := by
  rw [complete_retained_seed_valid_mass,
    whole_fair_code_mass a p (show a^2+p^2=1 by rw [ha,hp])]
  unfold historySuccess jointGoodWeight
  ring

theorem literal_five_stream_seed_failure (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (S : Finset (Fin 5 → Bool)) :
    rejectedWeight (codeValidity 4 5 S)
      (fun s => routedGoldenSeed a p 4 5 s (completeBlank 4 5))=
        historyFailure a p (S.card : ℝ) := by
  have hu := actual_retained_routed_seed_unitary a p ha hp 4 5
  have hn := unitary_column_has_complete_weight (routedGoldenSeed a p 4 5)
    (completeBlank 4 5) hu.1
  have hh := complete_weight_partition (codeValidity 4 5 S)
    (fun s => routedGoldenSeed a p 4 5 s (completeBlank 4 5))
  rw [hn,literal_five_stream_seed_valid_mass a p ha hp S] at hh
  unfold historyFailure
  linarith

theorem native_literal_seed_fast_full_word_rate (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (S : Finset (Fin 5 → Bool)) (hs : S.card=20 ∨ S.card=22 ∨ S.card=24) (k : ℕ) :
    rejectedWeight (codeValidity 4 5 S) (fun s =>
      fullWord (routedGoldenSeed a p 4 5) (completeBlank 4 5) (codeValidity 4 5 S)
        (fastGoldenPhase a p) (k+2) s (completeBlank 4 5))≤(1/16)^k/10 := by
  rw [actual_full_word_fast_failure a p _ _ _ ha hp
    (actual_retained_routed_seed_unitary a p ha hp 4 5),
    literal_five_stream_seed_failure a p ha hp S]
  have hd0 : 20≤(S.card : ℝ) := by rcases hs with h|h|h <;> rw [h] <;> norm_num
  have hd1 : (S.card : ℝ)≤24 := by rcases hs with h|h|h <;> rw [h] <;> norm_num
  have he := native_preparation_enters_retained_contraction a p _ ha hp hp0 hd0 hd1
  have hr := fast_parameter_native_bounds p hp hp0
  exact (fast_all_full_failure_rate _ _ (le_of_lt hr.1) (le_of_lt hr.2) he.1 he.2 k).2.2

end
end D0.Research.GoldenCoherentAmplification
namespace D0.Research.GoldenCoherentAmplification
noncomputable section
open Matrix Complex
open scoped Kronecker
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def recordedAmplify (U B Q : Matrix ι ι ℂ) : Matrix ι ι ℂ := U*B*U.conjTranspose*Q*U

def recordedWord (U B Q : Matrix ι ι ℂ) : ℕ → Matrix ι ι ℂ
  | 0 => U
  | k+1 => recordedAmplify (recordedWord U B Q k) B Q

theorem full_word_is_recorded_word (U : Matrix ι ι ℂ) (z : ι)
    (χ : ι → Bool) (w : ℂ) (k : ℕ) :
    fullWord U z χ w k=recordedWord U (blankPhase z w) (diagonalPhase χ w) k := by
  induction k with
  | zero => rfl
  | succ k ih => simp only [fullWord,recordedWord,fullAmplify,recordedAmplify,ih]

def suffixLift {X : Type*} [Fintype X] [DecidableEq X] (A : Matrix ι ι ℂ) :
    Matrix (ι × X) (ι × X) ℂ := A ⊗ₖ (1 : Matrix X X ℂ)

theorem suffix_lift_multiplication {X : Type*} [Fintype X] [DecidableEq X]
    (A B : Matrix ι ι ℂ) :
    suffixLift (X:=X) (A*B)=suffixLift (X:=X) A*suffixLift (X:=X) B := by
  simp [suffixLift,← Matrix.mul_kronecker_mul]

theorem suffix_lift_conjugation {X : Type*} [Fintype X] [DecidableEq X]
    (A : Matrix ι ι ℂ) :
    suffixLift (X:=X) A.conjTranspose=(suffixLift (X:=X) A).conjTranspose := by
  simp [suffixLift,Matrix.conjTranspose_kronecker]

theorem complete_recorded_word_suffix_natural {X : Type*} [Fintype X] [DecidableEq X]
    (U B Q : Matrix ι ι ℂ) (k : ℕ) :
    recordedWord (suffixLift (X:=X) U) (suffixLift (X:=X) B)
      (suffixLift (X:=X) Q) k=suffixLift (X:=X) (recordedWord U B Q k) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    simp only [recordedWord,recordedAmplify,ih,suffix_lift_multiplication,
      suffix_lift_conjugation]

def goldenComplexInclusion (a p : ℝ) (x : ι → ℂ) : ι × Bool → ℂ :=
  fun s => x s.1*(if s.2 then (p : ℂ) else (a : ℂ))

theorem golden_complex_operator_intertwines (A : Matrix ι ι ℂ)
    (a p : ℝ) (x : ι → ℂ) :
    (suffixLift (X:=Bool) A).mulVec (goldenComplexInclusion a p x)=
      goldenComplexInclusion a p (A.mulVec x) := by
  ext s
  rcases s with ⟨i,b⟩
  cases b <;> simp [suffixLift,goldenComplexInclusion,Matrix.mulVec,dotProduct,
    Matrix.kroneckerMap_apply,Fintype.sum_prod_type,Finset.sum_mul,mul_assoc]

theorem golden_complex_inclusion_weight (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (x : ι → ℂ) :
    vectorWeight (goldenComplexInclusion a p x)=vectorWeight x := by
  unfold vectorWeight
  simp only [Fintype.sum_prod_type,goldenComplexInclusion,Fintype.sum_bool,
    Bool.false_eq_true,if_false,if_true,Complex.normSq_mul,Complex.normSq_ofReal]
  apply Finset.sum_congr rfl
  intro i _
  have hn : a*a+p*p=1 := by nlinarith
  linear_combination Complex.normSq (x i)*hn

theorem golden_complex_rejection_weight (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (χ : ι → Bool) (x : ι → ℂ) :
    rejectedWeight (fun s : ι × Bool => χ s.1) (goldenComplexInclusion a p x)=
      rejectedWeight χ x := by
  unfold rejectedWeight
  simp only [Fintype.sum_prod_type,goldenComplexInclusion,Fintype.sum_bool,
    Bool.false_eq_true,if_false,if_true,Complex.normSq_mul,Complex.normSq_ofReal]
  apply Finset.sum_congr rfl
  intro i _
  cases hχ : χ i <;> simp [hχ]
  have hn : a*a+p*p=1 := by nlinarith
  linear_combination Complex.normSq (x i)*hn

theorem complete_golden_word_refinement (U : Matrix ι ι ℂ)
    (z : ι) (χ : ι → Bool) (w : ℂ) (k : ℕ) (a p : ℝ) (x : ι → ℂ) :
    (recordedWord (suffixLift (X:=Bool) U) (suffixLift (X:=Bool) (blankPhase z w))
      (suffixLift (X:=Bool) (diagonalPhase χ w)) k).mulVec (goldenComplexInclusion a p x)=
      goldenComplexInclusion a p ((fullWord U z χ w k).mulVec x) := by
  rw [complete_recorded_word_suffix_natural,golden_complex_operator_intertwines,
    full_word_is_recorded_word]

theorem complete_golden_failure_refinement (U : Matrix ι ι ℂ)
    (z : ι) (χ : ι → Bool) (w : ℂ) (k : ℕ) (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (x : ι → ℂ) :
    rejectedWeight (fun s : ι × Bool => χ s.1)
      ((recordedWord (suffixLift (X:=Bool) U) (suffixLift (X:=Bool) (blankPhase z w))
        (suffixLift (X:=Bool) (diagonalPhase χ w)) k).mulVec
        (goldenComplexInclusion a p x))=
      rejectedWeight χ ((fullWord U z χ w k).mulVec x) := by
  rw [complete_golden_word_refinement,golden_complex_rejection_weight a p ha hp]

theorem single_fine_blank_is_not_cylinder_extension (w : ℂ) (hw : w≠1) :
    blankPhase ((),false) w ≠ suffixLift (X:=Bool) (blankPhase (ι:=PUnit) () w) := by
  intro h
  have hh := congrFun (congrFun h ((),true)) ((),true)
  simp [blankPhase,diagonalPhase,suffixLift,Matrix.kroneckerMap_apply] at hh
  exact hw hh.symm

open scoped goldenRatio in
theorem owned_condensed_cylinder_amplitudes (a : ℝ)
    (ha : a^2=(φ : ℝ)⁻¹) :
    a^2=D0.CondensedAnchor.cylWeight [true] ∧
      ((φ : ℝ)⁻¹)^2=D0.CondensedAnchor.cylWeight [false] := by
  simp [D0.CondensedAnchor.cylWeight,ha]


open scoped goldenRatio in
theorem owned_primitive_root_is_condensed_weight : D0.primitiveRoot=(φ : ℝ)⁻¹ := by
  rw [← D0.phi_inv_eq_primitiveRoot]
  rfl

open scoped goldenRatio in
theorem actual_owned_golden_suffix_letter_weights (a : ℝ)
    (ha : a^2=D0.primitiveRoot) (b : Bool) :
    Complex.normSq (if b then (D0.primitiveRoot : ℂ) else (a : ℂ))=
      D0.CondensedAnchor.cylWeight [!b] := by
  rw [owned_primitive_root_is_condensed_weight] at ha ⊢
  cases b <;> simp only [Bool.not_false,Bool.not_true,Bool.false_eq_true,if_false,if_true,
    D0.CondensedAnchor.cylWeight,mul_one,Complex.normSq_ofReal] <;> nlinarith

end
end D0.Research.GoldenCoherentAmplification
namespace D0.Research.GoldenCoherentAmplification
noncomputable section
open Matrix Complex D0.Research.GoldenHistoryPreparation
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def goodMultiplier (w : ℂ) (e : ℝ) : ℂ := w^2-(w-1)^2*(e : ℂ)

theorem all_accepted_coordinates_keep_original_record (U : Matrix ι ι ℂ)
    (z : ι) (χ : ι → Bool) (w : ℂ)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) (i : ι) (hi : χ i=true) :
    fullAmplify U z χ w i z=U i z*goodMultiplier w (rejectedWeight χ (fun j => U j z)) := by
  rw [full_amplify_column U z χ w hU i,hi]
  simp only [if_true]
  unfold goodMultiplier
  ring

def fastAcceptedCoefficient (a p e : ℝ) : ℕ → ℂ
  | 0 => 1
  | k+1 => fastAcceptedCoefficient a p e k*goodMultiplier (fastGoldenPhase a p)
      (fastFailure (fastParameter p) e k)

def fastRejectedCoefficient (a p e : ℝ) : ℕ → ℂ
  | 0 => 1
  | k+1 => fastRejectedCoefficient a p e k*badMultiplier (fastGoldenPhase a p)
      (fastFailure (fastParameter p) e k)

theorem complete_fast_word_all_record_coefficients (a p : ℝ) (U : Matrix ι ι ℂ)
    (z : ι) (χ : ι → Bool) (ha : a^2=p) (hp : p+p^2=1)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) (k : ℕ) (i : ι) :
    fullWord U z χ (fastGoldenPhase a p) k i z=U i z*
      (if χ i then fastAcceptedCoefficient a p (rejectedWeight χ (fun j => U j z)) k
        else fastRejectedCoefficient a p (rejectedWeight χ (fun j => U j z)) k) := by
  induction k with
  | zero => simp [fullWord,fastAcceptedCoefficient,fastRejectedCoefficient]
  | succ k ih =>
    have huk := all_full_words_unitary U z χ _ hU (fast_golden_phase_normSq a p ha hp) k
    cases hi : χ i
    · change fullAmplify (fullWord U z χ (fastGoldenPhase a p) k) z χ _ i z=_
      rw [all_failed_coordinates_keep_original_record _ _ _ _ huk i hi,
        actual_full_word_fast_failure a p U z χ ha hp hU k,ih]
      simp [hi,fastRejectedCoefficient,mul_assoc]
    · change fullAmplify (fullWord U z χ (fastGoldenPhase a p) k) z χ _ i z=_
      rw [all_accepted_coordinates_keep_original_record _ _ _ _ huk i hi,
        actual_full_word_fast_failure a p U z χ ha hp hU k,ih]
      simp [hi,fastAcceptedCoefficient,mul_assoc]

theorem actual_full_seed_successful_record_factorization (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (n m : ℕ)
    (S : Finset (Fin m → Bool)) (b : Fin m → Bool) (hb : b∈S)
    (w : Fin m → Word n) (hw : ∀ i, firstLabel (w i)=some false) (k : ℕ) :
    fullWord (routedGoldenSeed a p n m) (completeBlank n m) (codeValidity n m S)
      (fastGoldenPhase a p) k (fun i => (w i,b i)) (completeBlank n m)=
      ((∏ i : Fin m, amplitude a p (w i) : ℝ) : ℂ)*
        fastAcceptedCoefficient a p (rejectedWeight (codeValidity n m S)
          (fun s => routedGoldenSeed a p n m s (completeBlank n m))) k := by
  rw [complete_fast_word_all_record_coefficients a p _ _ _ ha hp
    (actual_retained_routed_seed_unitary a p ha hp n m),
    actual_routed_seed_successful_amplitude a p n m b w hw]
  simp [codeValidity,hw,hb]

def alignedAcceptedVector (χ : ι → Bool) (x : ι → ℂ) : ι → ℂ :=
  fun i => if χ i then x i/((Real.sqrt (acceptedWeight χ x) : ℝ) : ℂ) else 0

theorem phase_aligned_full_state_distance_identity (χ : ι → Bool) (x : ι → ℂ)
    (hs : 0<acceptedWeight χ x) :
    vectorWeight (x-alignedAcceptedVector χ x)=
      (1-Real.sqrt (acceptedWeight χ x))^2+rejectedWeight χ x := by
  let t := Real.sqrt (acceptedWeight χ x)
  have ht : 0<t := Real.sqrt_pos.2 hs
  have ht2 : t^2=acceptedWeight χ x := Real.sq_sqrt (le_of_lt hs)
  have he (i : ι) : Complex.normSq (x i-alignedAcceptedVector χ x i)=
      (if χ i then Complex.normSq (x i)*(1-1/t)^2 else 0)+
      (if χ i then 0 else Complex.normSq (x i)) := by
    cases hi : χ i
    · simp [alignedAcceptedVector,hi]
    · have h : x i-x i/(t : ℂ)=x i*((1-1/t : ℝ) : ℂ) := by push_cast; ring
      simp only [alignedAcceptedVector,hi,if_true,if_false,add_zero]
      change Complex.normSq (x i-x i/(t : ℂ))=_
      rw [h,Complex.normSq_mul,Complex.normSq_ofReal]
      ring
  unfold vectorWeight
  simp only [Pi.sub_apply]
  simp_rw [he]
  rw [Finset.sum_add_distrib]
  have hsum : (∑ i, if χ i then Complex.normSq (x i)*(1-1/t)^2 else 0)=
      acceptedWeight χ x*(1-1/t)^2 := by
    unfold acceptedWeight
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro i _
    cases χ i <;> simp
  have halg : t^2*(1-1/t)^2=(1-t)^2 := by
    field_simp
    ring
  have hg := congrArg (fun u : ℝ => u*(1-1/t)^2) ht2
  have hsqt : acceptedWeight χ x*(1-1/t)^2=(1-t)^2 := hg.symm.trans halg
  rw [hsum,hsqt]
  rfl

theorem phase_aligned_full_vector_error (χ : ι → Bool) (x : ι → ℂ)
    (hn : vectorWeight x=1) (hs : 0<acceptedWeight χ x) :
    vectorWeight (x-alignedAcceptedVector χ x)≤2*rejectedWeight χ x := by
  have hh := complete_weight_partition χ x
  rw [hn] at hh
  have he := rejected_weight_nonnegative χ x
  have ht0 := Real.sqrt_nonneg (acceptedWeight χ x)
  have ht2 := Real.sq_sqrt (le_of_lt hs)
  have ht1 : Real.sqrt (acceptedWeight χ x)≤1 := by nlinarith
  rw [phase_aligned_full_state_distance_identity χ x hs]
  nlinarith

theorem aligned_accepted_vector_has_complete_weight (χ : ι → Bool) (x : ι → ℂ)
    (hs : 0<acceptedWeight χ x) :
    vectorWeight (alignedAcceptedVector χ x)=1 := by
  have ht : Real.sqrt (acceptedWeight χ x)≠0 := ne_of_gt (Real.sqrt_pos.2 hs)
  have ht2 := Real.sq_sqrt (le_of_lt hs)
  unfold vectorWeight alignedAcceptedVector
  have he (i : ι) : Complex.normSq
      (if χ i then x i/((Real.sqrt (acceptedWeight χ x) : ℝ) : ℂ) else 0)=
      (if χ i then Complex.normSq (x i) else 0)/acceptedWeight χ x := by
    cases hi : χ i <;> simp [hi,Complex.normSq_div,Complex.normSq_ofReal,
      ← pow_two,ht2]
  simp_rw [he]
  rw [← Finset.sum_div]
  change acceptedWeight χ x/acceptedWeight χ x=1
  exact div_self (ne_of_gt hs)

theorem native_literal_full_vector_error (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (S : Finset (Fin 5 → Bool)) (hs : S.card=20 ∨ S.card=22 ∨ S.card=24) (k : ℕ) :
    let x := fun s => fullWord (routedGoldenSeed a p 4 5) (completeBlank 4 5)
      (codeValidity 4 5 S) (fastGoldenPhase a p) (k+2) s (completeBlank 4 5)
    0<acceptedWeight (codeValidity 4 5 S) x ∧
      vectorWeight (alignedAcceptedVector (codeValidity 4 5 S) x)=1 ∧
      vectorWeight (x-alignedAcceptedVector (codeValidity 4 5 S) x)≤(1/16)^k/5 := by
  dsimp only
  let x := fun s => fullWord (routedGoldenSeed a p 4 5) (completeBlank 4 5)
    (codeValidity 4 5 S) (fastGoldenPhase a p) (k+2) s (completeBlank 4 5)
  have hu := all_full_words_unitary (routedGoldenSeed a p 4 5) (completeBlank 4 5)
    (codeValidity 4 5 S) (fastGoldenPhase a p)
    (actual_retained_routed_seed_unitary a p ha hp 4 5)
    (fast_golden_phase_normSq a p ha hp) (k+2)
  have hn : vectorWeight x=1 := unitary_column_has_complete_weight _ _ hu.1
  have hf := native_literal_seed_fast_full_word_rate a p ha hp hp0 S hs k
  have hpow : (1/16 : ℝ)^k≤1 := by
    simpa using pow_le_pow_left₀ (by norm_num : (0:ℝ)≤1/16)
      (by norm_num : (1/16:ℝ)≤1) k
  have hh := complete_weight_partition (codeValidity 4 5 S) x
  rw [hn] at hh
  have hs0 : 0<acceptedWeight (codeValidity 4 5 S) x := by
    change rejectedWeight (codeValidity 4 5 S) x≤(1/16)^k/10 at hf
    linarith
  refine ⟨hs0,aligned_accepted_vector_has_complete_weight _ _ hs0,?_⟩
  have h := phase_aligned_full_vector_error _ _ hn hs0
  change rejectedWeight (codeValidity 4 5 S) x≤(1/16)^k/10 at hf
  linarith

end
end D0.Research.GoldenCoherentAmplification
namespace D0.Research.GoldenCoherentAmplification
noncomputable section
open Matrix Complex D0.Representation.GoldenOrderInterferometer

def phaseRealMatrix (w : ℂ) : Matrix (Fin 2) (Fin 2) ℝ := !![w.re,-w.im;w.im,w.re]

theorem phase_real_matrix_multiplication (w z : ℂ) :
    phaseRealMatrix (w*z)=phaseRealMatrix w*phaseRealMatrix z := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [phaseRealMatrix,Complex.mul_re,Complex.mul_im,Matrix.mul_apply,Fin.sum_univ_two]
    <;> ring

theorem phase_real_matrix_powers (w : ℂ) (k : ℕ) :
    phaseRealMatrix (w^k)=(phaseRealMatrix w)^k := by
  induction k with
  | zero => ext i j; fin_cases i <;> fin_cases j <;> simp [phaseRealMatrix]
  | succ k ih => rw [pow_succ,phase_real_matrix_multiplication,ih,pow_succ]

theorem fast_phase_is_owned_golden_eighth_power (a p : ℝ) (ha : a^2=p) :
    phaseRealMatrix (fastGoldenPhase a p)=(gate a p)^8 := by
  unfold fastGoldenPhase
  rw [phase_real_matrix_powers]
  have h : phaseRealMatrix (goldenPhase a p)=(gate a p)^2 := by
    simpa [phaseRealMatrix,pow_two] using golden_pair_realification a p ha
  rw [h,← pow_mul]

end
end D0.Research.GoldenCoherentAmplification
namespace D0.Research.GoldenCoherentAmplification
noncomputable section
open Matrix Complex D0.Research.GoldenHistoryPreparation
open D0.Claims D0.Synthesis.SceneNormalizedQuotientDescent

def sceneIncomingMask (v : Fin 33) : Finset (Fin 33) :=
  Finset.univ.filter (fun u => Adj31 u v=1)
abbrev SceneIncoming (v : Fin 33) := {u : Fin 33 // u∈sceneIncomingMask v}

theorem actual_scene_incoming_cardinality (v : Fin 33) :
    Fintype.card (SceneIncoming v)=20 ∨ Fintype.card (SceneIncoming v)=22 ∨
      Fintype.card (SceneIncoming v)=24 := by
  revert v
  decide

theorem actual_scene_incoming_cardinality_is_owned_degree (v : Fin 33) :
    ((Fintype.card (SceneIncoming v) : ℕ) : ℚ)=fullDegreeValue v := by
  have hc : Fintype.card (SceneIncoming v)=(sceneIncomingMask v).card := by
    simp [SceneIncoming]
  rw [hc]
  unfold sceneIncomingMask
  rw [Finset.card_eq_sum_ones,Finset.sum_filter]
  push_cast
  unfold fullDegreeValue
  apply Finset.sum_congr rfl
  intro u _
  by_cases hz : zone31 u=zone31 v
  · simp [Adj31,hz]
  · have hz' : zone31 v≠zone31 u := Ne.symm hz
    simp [Adj31,hz,hz']

theorem actual_scene_incoming_fits_five_bits (v : Fin 33) :
    Fintype.card (SceneIncoming v)≤32 := by
  rcases actual_scene_incoming_cardinality v with h|h|h <;> rw [h] <;> omega

def fiveBitIndex : (Fin 5 → Bool) ≃ Fin 32 :=
  Fintype.equivOfCardEq (by simpa using actual_five_bit_code_carrier)

def sceneIncomingCode (v : Fin 33) (u : SceneIncoming v) : Fin 5 → Bool :=
  fiveBitIndex.symm ⟨(Fintype.equivFin (SceneIncoming v) u).val,
    lt_of_lt_of_le (Fintype.equivFin (SceneIncoming v) u).isLt
      (actual_scene_incoming_fits_five_bits v)⟩

theorem actual_scene_incoming_code_injective (v : Fin 33) :
    Function.Injective (sceneIncomingCode v) := by
  intro u t h
  apply (Fintype.equivFin (SceneIncoming v)).injective
  apply Fin.ext
  have hh := congrArg (fun b => (fiveBitIndex b).val) h
  simpa [sceneIncomingCode] using hh

def sceneAcceptedCodes (v : Fin 33) : Finset (Fin 5 → Bool) :=
  Finset.univ.image (sceneIncomingCode v)

theorem actual_scene_accepted_codes_cardinality (v : Fin 33) :
    (sceneAcceptedCodes v).card=Fintype.card (SceneIncoming v) := by
  simp [sceneAcceptedCodes,Finset.card_image_of_injective,
    actual_scene_incoming_code_injective]

theorem actual_scene_accepted_codes_exact_degrees (v : Fin 33) :
    (sceneAcceptedCodes v).card=20 ∨ (sceneAcceptedCodes v).card=22 ∨
      (sceneAcceptedCodes v).card=24 := by
  rw [actual_scene_accepted_codes_cardinality]
  exact actual_scene_incoming_cardinality v

theorem actual_scene_code_member (v : Fin 33) (u : SceneIncoming v) :
    sceneIncomingCode v u∈sceneAcceptedCodes v := by
  exact Finset.mem_image.mpr ⟨u,Finset.mem_univ _,rfl⟩

theorem actual_scene_all_incoming_histories_have_same_record_amplitude (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (v : Fin 33) (u : SceneIncoming v)
    (w : Fin 5 → Word 4) (hw : ∀ i, firstLabel (w i)=some false) (k : ℕ) :
    fullWord (routedGoldenSeed a p 4 5) (completeBlank 4 5) (codeValidity 4 5 (sceneAcceptedCodes v))
      (fastGoldenPhase a p) k (fun i => (w i,sceneIncomingCode v u i)) (completeBlank 4 5)=
      ((∏ i : Fin 5, amplitude a p (w i) : ℝ) : ℂ)*
        fastAcceptedCoefficient a p (historyFailure a p (fullDegreeValue v : ℝ)) k := by
  rw [actual_full_seed_successful_record_factorization a p ha hp 4 5 _ _
    (actual_scene_code_member v u) w hw k,literal_five_stream_seed_failure a p ha hp]
  congr 2
  rw [actual_scene_accepted_codes_cardinality]
  congr 1
  have h := actual_scene_incoming_cardinality_is_owned_degree v
  exact_mod_cast h

theorem actual_scene_full_word_failure_rate (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) (v : Fin 33) (k : ℕ) :
    rejectedWeight (codeValidity 4 5 (sceneAcceptedCodes v)) (fun s =>
      fullWord (routedGoldenSeed a p 4 5) (completeBlank 4 5)
        (codeValidity 4 5 (sceneAcceptedCodes v)) (fastGoldenPhase a p) (k+2) s (completeBlank 4 5))
      ≤(1/16)^k/10 := by
  exact native_literal_seed_fast_full_word_rate a p ha hp hp0 _
    (actual_scene_accepted_codes_exact_degrees v) k

theorem actual_scene_full_word_state_error (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) (v : Fin 33) (k : ℕ) :
    let x := fun s => fullWord (routedGoldenSeed a p 4 5) (completeBlank 4 5)
      (codeValidity 4 5 (sceneAcceptedCodes v)) (fastGoldenPhase a p) (k+2) s (completeBlank 4 5)
    0<acceptedWeight (codeValidity 4 5 (sceneAcceptedCodes v)) x ∧
      vectorWeight (alignedAcceptedVector (codeValidity 4 5 (sceneAcceptedCodes v)) x)=1 ∧
      vectorWeight (x-alignedAcceptedVector (codeValidity 4 5 (sceneAcceptedCodes v)) x)≤(1/16)^k/5 := by
  exact native_literal_full_vector_error a p ha hp hp0 _
    (actual_scene_accepted_codes_exact_degrees v) k

end
end D0.Research.GoldenCoherentAmplification
namespace D0.Research.GoldenCoherentAmplification
noncomputable section
open Matrix Complex

theorem good_multiplier_retains_complex_phase (w : ℂ) (e : ℝ)
    (hw : Complex.normSq w=1) :
    goodMultiplier w e=w*(w+((2-2*w.re : ℝ) : ℂ)*(e : ℂ)) := by
  have h := unit_phase_quadratic w hw
  unfold goodMultiplier
  push_cast at h ⊢
  linear_combination -(e : ℂ)*h

theorem distinct_success_laws_have_relative_phase_area (w : ℂ) (e f : ℝ)
    (hw : Complex.normSq w=1) :
    (goodMultiplier w e*star (goodMultiplier w f)).im=
      (2-2*w.re)*(f-e)*w.im := by
  rw [good_multiplier_retains_complex_phase w e hw,
    good_multiplier_retains_complex_phase w f hw]
  have hn : w.re^2+w.im^2=1 := by simpa [Complex.normSq_apply,pow_two] using hw
  simp [Complex.mul_re,Complex.mul_im,Complex.star_def]
  linear_combination (2-2*w.re)*(f-e)*w.im*hn

theorem nonzero_relative_phase_blocks_one_real_ray (w : ℂ) (e f : ℝ)
    (hw : Complex.normSq w=1) (hr : w.re≠1) (hi : w.im≠0) (he : e≠f) :
    (goodMultiplier w e*star (goodMultiplier w f)).im≠0 := by
  rw [distinct_success_laws_have_relative_phase_area w e f hw]
  exact mul_ne_zero (mul_ne_zero (by intro h; apply hr; linarith)
    (sub_ne_zero.mpr (Ne.symm he))) hi


theorem own_fast_phase_has_nonzero_relative_area (a p e f : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) (he : e≠f) :
    (goodMultiplier (fastGoldenPhase a p) e*
      star (goodMultiplier (fastGoldenPhase a p) f)).im≠0 := by
  have hw := fast_golden_phase_normSq a p ha hp
  have hb := fast_parameter_native_bounds p hp hp0
  have hRe : (fastGoldenPhase a p).re=(fastParameter p+1)/2 := by
    rw [fast_golden_phase_real a p ha hp]
    unfold fastParameter
    ring
  have hr : (fastGoldenPhase a p).re≠1 := by rw [hRe]; linarith
  have hn : (fastGoldenPhase a p).re^2+(fastGoldenPhase a p).im^2=1 := by
    simpa [Complex.normSq_apply,pow_two] using hw
  have hi : (fastGoldenPhase a p).im≠0 := by
    intro h
    rw [h,hRe] at hn
    nlinarith
  exact nonzero_relative_phase_blocks_one_real_ray _ _ _ hw hr hi he

theorem actual_degree_twenty_twentyfour_cannot_share_success_phase (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) :
    (goodMultiplier (fastGoldenPhase a p) (D0.Research.GoldenHistoryPreparation.historyFailure a p 20)*
      star (goodMultiplier (fastGoldenPhase a p)
        (D0.Research.GoldenHistoryPreparation.historyFailure a p 24))).im≠0 := by
  apply own_fast_phase_has_nonzero_relative_area a p _ _ ha hp hp0
  have h := D0.Research.GoldenHistoryPreparation.golden_five_bit_good_bounds a p ha hp hp0
  unfold D0.Research.GoldenHistoryPreparation.historyFailure
    D0.Research.GoldenHistoryPreparation.historySuccess
  intro he
  nlinarith

end
end D0.Research.GoldenCoherentAmplification

namespace D0.Research.GoldenFixedCalibration
noncomputable section
open Matrix Complex Filter Topology D0.Research.GoldenCoherentAmplification
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def unspunColumn (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool) (w : ℂ) (k : ℕ) : ι → ℂ :=
  fun i => (star w)^(2*k)*fullWord U z χ w k i z

theorem complete_unit_phase_norm (w : ℂ) (hw : Complex.normSq w=1) : ‖w‖=1 := by
  have h := Complex.normSq_eq_norm_sq w
  rw [hw] at h
  nlinarith [norm_nonneg w]

theorem complete_unit_phase_star_product (w : ℂ) (hw : Complex.normSq w=1) :
    star w*w=1 := by
  simpa using (Complex.normSq_eq_conj_mul_self (z:=w)).symm.trans
    (congrArg (fun x : ℝ => (x : ℂ)) hw)

theorem unitary_complete_column_coordinate_norm (U : Matrix ι ι ℂ) (z i : ι)
    (hU : U.conjTranspose*U=1) : ‖U i z‖≤1 := by
  have hn := unitary_column_has_complete_weight U z hU
  have hs : Complex.normSq (U i z)≤vectorWeight (fun j => U j z) :=
    Finset.single_le_sum (fun j _ => Complex.normSq_nonneg (U j z)) (Finset.mem_univ i)
  rw [hn,Complex.normSq_eq_norm_sq] at hs
  nlinarith [norm_nonneg (U i z)]

theorem actual_unspun_coordinate_norm (U : Matrix ι ι ℂ) (z i : ι)
    (χ : ι → Bool) (w : ℂ) (k : ℕ)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) (hw : Complex.normSq w=1) :
    ‖unspunColumn U z χ w k i‖≤1 := by
  have hu := all_full_words_unitary U z χ w hU hw k
  have h := unitary_complete_column_coordinate_norm _ z i hu.1
  simpa [unspunColumn,norm_mul,norm_pow,complete_unit_phase_norm w hw] using h

theorem actual_unspun_weight_preserved (U : Matrix ι ι ℂ) (z : ι)
    (χ : ι → Bool) (w : ℂ) (k : ℕ) (hw : Complex.normSq w=1) :
    vectorWeight (unspunColumn U z χ w k)=
      vectorWeight (fun i => fullWord U z χ w k i z) := by
  unfold vectorWeight unspunColumn
  apply Finset.sum_congr rfl
  intro i _
  simp [Complex.normSq_mul,map_pow,Complex.normSq_conj,Complex.star_def,hw]

theorem all_unspun_full_columns_normalized (U : Matrix ι ι ℂ) (z : ι)
    (χ : ι → Bool) (w : ℂ) (k : ℕ)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) (hw : Complex.normSq w=1) :
    vectorWeight (unspunColumn U z χ w k)=1 := by
  rw [actual_unspun_weight_preserved U z χ w k hw]
  exact unitary_column_has_complete_weight _ z (all_full_words_unitary U z χ w hU hw k).1

theorem full_unspun_accepted_increment (U : Matrix ι ι ℂ) (z i : ι)
    (χ : ι → Bool) (w : ℂ) (k : ℕ) (hi : χ i=true)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) (hw : Complex.normSq w=1) :
    unspunColumn U z χ w (k+1) i-unspunColumn U z χ w k i=
      -((star w)^2*(w-1)^2*(rejectedWeight χ (fun j => fullWord U z χ w k j z) : ℂ)*
        unspunColumn U z χ w k i) := by
  have hu := all_full_words_unitary U z χ w hU hw k
  have hs : (star w)^2*w^2=1 := by
    rw [← mul_pow,complete_unit_phase_star_product w hw,one_pow]
  unfold unspunColumn
  change (star w)^(2*(k+1))*fullAmplify (fullWord U z χ w k) z χ w i z-
    (star w)^(2*k)*fullWord U z χ w k i z=_
  rw [all_accepted_coordinates_keep_original_record _ _ _ _ hu i hi]
  unfold goodMultiplier
  rw [show 2*(k+1)=2*k+2 by omega,pow_add]
  linear_combination (star w)^(2*k)*fullWord U z χ w k i z*(hs)

theorem own_fast_phase_increment_factor_norm (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    ‖(star (fastGoldenPhase a p))^2*(fastGoldenPhase a p-1)^2‖=1-fastParameter p := by
  have hw := fast_golden_phase_normSq a p ha hp
  have hn := complete_unit_phase_norm _ hw
  rw [norm_mul,norm_pow,norm_star,hn,one_pow,one_mul,norm_pow,
    ← Complex.normSq_eq_norm_sq]
  have h0 : Complex.normSq (fastGoldenPhase a p-1)=2-2*(fastGoldenPhase a p).re := by
    simp [Complex.normSq_apply,pow_two] at hw ⊢
    nlinarith
  rw [h0,fast_golden_phase_real a p ha hp]
  unfold fastParameter
  ring

theorem literal_unspun_good_coordinate_increment_bound (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (U : Matrix ι ι ℂ) (z i : ι) (χ : ι → Bool) (hi : χ i=true)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he : rejectedWeight χ (fun j => U j z)≤11/16) (k : ℕ) :
    dist (unspunColumn U z χ (fastGoldenPhase a p) (k+2) i)
      (unspunColumn U z χ (fastGoldenPhase a p) (k+1+2) i)≤(1/16)^k/10 := by
  have hw := fast_golden_phase_normSq a p ha hp
  have hr := fast_parameter_native_bounds p hp hp0
  have hf := fast_all_full_failure_rate _ _ (le_of_lt hr.1) (le_of_lt hr.2)
    (rejected_weight_nonnegative χ (fun j => U j z)) he k
  have heq : k+1+2=k+2+1 := by omega
  rw [heq,dist_comm,dist_eq_norm,full_unspun_accepted_increment U z i χ _ (k+2) hi hU hw]
  rw [norm_neg,norm_mul,norm_mul,own_fast_phase_increment_factor_norm a p ha hp]
  have he0 := rejected_weight_nonnegative χ (fun j => fullWord U z χ (fastGoldenPhase a p) (k+2) j z)
  rw [Complex.norm_real,Real.norm_eq_abs,abs_of_nonneg he0]
  have hc := actual_unspun_coordinate_norm U z i χ _ (k+2) hU hw
  have h10 : 0≤1-fastParameter p := by linarith
  have h11 : 1-fastParameter p≤1 := by linarith
  have hg : rejectedWeight χ (fun j => fullWord U z χ (fastGoldenPhase a p) (k+2) j z)=
      fastFailure (fastParameter p) (rejectedWeight χ (fun j => U j z)) (k+2) :=
    actual_full_word_fast_failure a p U z χ ha hp hU (k+2)
  have hmul : (1-fastParameter p)*rejectedWeight χ
      (fun j => fullWord U z χ (fastGoldenPhase a p) (k+2) j z)*
      ‖unspunColumn U z χ (fastGoldenPhase a p) (k+2) i‖≤
      rejectedWeight χ (fun j => fullWord U z χ (fastGoldenPhase a p) (k+2) j z) := by
    have hm0 := mul_le_mul_of_nonneg_right h11 he0
    have hm1 := mul_le_mul_of_nonneg_left hc (mul_nonneg h10 he0)
    nlinarith
  exact hmul.trans (hg ▸ hf.2.2)

theorem literal_good_coordinate_has_fixed_calibration (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (U : Matrix ι ι ℂ) (z i : ι) (χ : ι → Bool) (hi : χ i=true)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he : rejectedWeight χ (fun j => U j z)≤11/16) :
    ∃ L : ℂ, Tendsto (fun k => unspunColumn U z χ (fastGoldenPhase a p) (k+2) i) atTop (𝓝 L) ∧
      ∀ k, dist (unspunColumn U z χ (fastGoldenPhase a p) (k+2) i) L≤(8/75)*(1/16)^k := by
  have hh (k : ℕ) := literal_unspun_good_coordinate_increment_bound a p ha hp hp0 U z i χ hi hU he k
  have hc := cauchySeq_of_le_geometric (1/16) (1/10) (by norm_num : (1/16:ℝ)<1)
    (by intro k; simpa [div_eq_mul_inv,mul_comm] using hh k)
  obtain ⟨L,hL⟩ := cauchySeq_tendsto_of_complete hc
  refine ⟨L,hL,?_⟩
  intro k
  have h := dist_le_of_le_geometric_of_tendsto (1/16) (1/10)
    (by norm_num : (1/16:ℝ)<1)
    (by intro j; simpa [div_eq_mul_inv,mul_comm] using hh j) hL k
  convert h using 1 <;> ring

end
end D0.Research.GoldenFixedCalibration

namespace D0.Research.GoldenFixedCalibration
noncomputable section
open Matrix Complex D0.Research.GoldenCoherentAmplification
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def maskedVector (χ : ι → Bool) (x : ι → ℂ) : ι → ℂ := fun i => if χ i then x i else 0

def pureProjection (x : ι → ℂ) : Matrix ι ι ℂ := Matrix.vecMulVec x (star x)

def normalizedAcceptedProjection (χ : ι → Bool) (x : ι → ℂ) : Matrix ι ι ℂ :=
  ((acceptedWeight χ x : ℝ) : ℂ)⁻¹ • pureProjection (maskedVector χ x)

def frobeniusWeight (A : Matrix ι ι ℂ) : ℝ := ∑ i, ∑ j, Complex.normSq (A i j)

theorem complete_accepted_mass_scalar (χ : ι → Bool) (x : ι → ℂ) (c : ℂ) :
    acceptedWeight χ (fun i => c*x i)=Complex.normSq c*acceptedWeight χ x := by
  unfold acceptedWeight
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  cases χ i <;> simp [Complex.normSq_mul]

theorem pure_projection_scalar (c : ℂ) (x : ι → ℂ) :
    pureProjection (fun i => c*x i)=((Complex.normSq c : ℝ) : ℂ) • pureProjection x := by
  ext i j
  simp only [pureProjection,Matrix.vecMulVec,Matrix.of_apply,Pi.star_apply,
    star_mul,Matrix.smul_apply,smul_eq_mul]
  rw [Complex.normSq_eq_conj_mul_self]
  simp only [Complex.star_def]
  ring

theorem normalized_accepted_projection_phase_cancels (χ : ι → Bool) (x : ι → ℂ)
    (c : ℂ) (hc : c≠0) :
    normalizedAcceptedProjection χ (fun i => c*x i)=normalizedAcceptedProjection χ x := by
  have hn : Complex.normSq c≠0 := mt Complex.normSq_eq_zero.mp hc
  have hcn : ((Complex.normSq c : ℝ) : ℂ)≠0 := by exact_mod_cast hn
  have hm : maskedVector χ (fun i => c*x i)=fun i => c*maskedVector χ x i := by
    funext i
    cases hi : χ i <;> simp [maskedVector,hi]
  unfold normalizedAcceptedProjection
  rw [complete_accepted_mass_scalar,hm,pure_projection_scalar,← smul_assoc]
  congr 1
  push_cast
  simp [_root_.mul_inv_rev,mul_assoc,hcn]

theorem full_phase_aligned_target_projection (χ : ι → Bool) (x : ι → ℂ)
    (hs : 0<acceptedWeight χ x) :
    pureProjection (alignedAcceptedVector χ x)=normalizedAcceptedProjection χ x := by
  have ht2 := Real.sq_sqrt (le_of_lt hs)
  have he : alignedAcceptedVector χ x=fun i =>
      ((Real.sqrt (acceptedWeight χ x) : ℝ) : ℂ)⁻¹*maskedVector χ x i := by
    funext i
    cases hi : χ i <;> simp [alignedAcceptedVector,maskedVector,hi,div_eq_mul_inv,mul_comm]
  rw [he,pure_projection_scalar]
  unfold normalizedAcceptedProjection
  congr 1
  simp only [Complex.normSq_inv,Complex.normSq_ofReal,← pow_two,ht2]
  push_cast
  rfl

theorem normalized_accepted_projection_depends_only_on_accepted (χ : ι → Bool)
    (x y : ι → ℂ) (h : ∀ i, χ i=true → x i=y i) :
    normalizedAcceptedProjection χ x=normalizedAcceptedProjection χ y := by
  have hm : maskedVector χ x=maskedVector χ y := by
    funext i
    cases hi : χ i
    · simp [maskedVector,hi]
    · simp [maskedVector,hi,h i hi]
  have hs : acceptedWeight χ x=acceptedWeight χ y := by
    unfold acceptedWeight
    apply Finset.sum_congr rfl
    intro i _
    cases hi : χ i
    · simp [hi]
    · simp [hi,h i hi]
  simp only [normalizedAcceptedProjection,hs,hm]

theorem full_fast_word_target_projection_is_fixed (a p : ℝ) (U : Matrix ι ι ℂ)
    (z : ι) (χ : ι → Bool) (ha : a^2=p) (hp : p+p^2=1)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) (k : ℕ)
    (hc : fastAcceptedCoefficient a p (rejectedWeight χ (fun j => U j z)) k≠0) :
    normalizedAcceptedProjection χ (fun i => fullWord U z χ (fastGoldenPhase a p) k i z)=
      normalizedAcceptedProjection χ (fun i => U i z) := by
  calc
    _ = normalizedAcceptedProjection χ
        (fun i => fastAcceptedCoefficient a p (rejectedWeight χ (fun j => U j z)) k*U i z) := by
      apply normalized_accepted_projection_depends_only_on_accepted
      intro i hi
      rw [complete_fast_word_all_record_coefficients a p U z χ ha hp hU k i,hi]
      simp [mul_comm]
    _ = _ := normalized_accepted_projection_phase_cancels χ (fun i => U i z) _ hc

theorem frobenius_weight_pure_projection (x : ι → ℂ) :
    frobeniusWeight (pureProjection x)=(vectorWeight x)^2 := by
  unfold frobeniusWeight pureProjection vectorWeight
  simp only [Matrix.vecMulVec,Matrix.of_apply,Pi.star_apply,Complex.normSq_mul,Complex.star_def,
    Complex.normSq_conj]
  rw [pow_two,Finset.sum_mul_sum]

theorem full_projection_cross_sum (x y : ι → ℂ) :
    (∑ i, ∑ j, (pureProjection x i j)*star (pureProjection y i j))=
      ((Complex.normSq (star x ⬝ᵥ y) : ℝ) : ℂ) := by
  rw [Complex.normSq_eq_conj_mul_self]
  simp only [pureProjection,Matrix.vecMulVec,Matrix.of_apply,Pi.star_apply,star_mul,star_star,
    dotProduct,map_sum]
  rw [Finset.sum_mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  simp [Complex.star_def]
  ring

theorem frobenius_distance_pure_projections (x y : ι → ℂ) :
    frobeniusWeight (pureProjection x-pureProjection y)=
      (vectorWeight x)^2+(vectorWeight y)^2-2*Complex.normSq (star x ⬝ᵥ y) := by
  unfold frobeniusWeight
  simp only [Matrix.sub_apply,Complex.normSq_sub]
  simp only [Finset.sum_sub_distrib,Finset.sum_add_distrib,← Finset.mul_sum]
  have hx := frobenius_weight_pure_projection x
  have hy := frobenius_weight_pure_projection y
  unfold frobeniusWeight at hx hy
  rw [hx,hy]
  have he := congrArg Complex.re (full_projection_cross_sum x y)
  simp only [Complex.re_sum,Complex.ofReal_re,Complex.star_def] at he
  rw [he]

theorem accepted_target_inner_product_squared (χ : ι → Bool) (x : ι → ℂ)
    (hs : 0<acceptedWeight χ x) :
    Complex.normSq (star x ⬝ᵥ alignedAcceptedVector χ x)=acceptedWeight χ x := by
  have ht0 : Real.sqrt (acceptedWeight χ x)≠0 := ne_of_gt (Real.sqrt_pos.2 hs)
  have h : star x ⬝ᵥ alignedAcceptedVector χ x=
      ((acceptedWeight χ x : ℝ) : ℂ)/((Real.sqrt (acceptedWeight χ x) : ℝ) : ℂ) := by
    unfold dotProduct alignedAcceptedVector acceptedWeight
    push_cast
    rw [Finset.sum_div]
    apply Finset.sum_congr rfl
    intro i _
    cases hi : χ i <;> simp [hi,Complex.normSq_eq_conj_mul_self,Complex.star_def,mul_div_assoc]
  rw [h,Complex.normSq_div,Complex.normSq_ofReal,Complex.normSq_ofReal]
  have ht2 := Real.sq_sqrt (le_of_lt hs)
  simp only [← pow_two,ht2]
  field_simp

theorem whole_unconditional_prepared_projection_error (χ : ι → Bool) (x : ι → ℂ)
    (hn : vectorWeight x=1) (hs : 0<acceptedWeight χ x) :
    frobeniusWeight (pureProjection x-normalizedAcceptedProjection χ x)=
      2*rejectedWeight χ x := by
  rw [← full_phase_aligned_target_projection χ x hs,
    frobenius_distance_pure_projections,hn,aligned_accepted_vector_has_complete_weight χ x hs,
    accepted_target_inner_product_squared χ x hs]
  have h := complete_weight_partition χ x
  rw [hn] at h
  nlinarith

end
end D0.Research.GoldenFixedCalibration

namespace D0.Research.GoldenFixedCalibration
noncomputable section
open Matrix Complex Filter Topology D0.Research.GoldenCoherentAmplification
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

theorem all_unspun_failed_coordinates_have_full_mass_bound (U : Matrix ι ι ℂ)
    (z i : ι) (χ : ι → Bool) (w : ℂ) (k : ℕ)
    (hw : Complex.normSq w=1) (hi : χ i=false) :
    Complex.normSq (unspunColumn U z χ w k i)≤
      rejectedWeight χ (fun j => fullWord U z χ w k j z) := by
  have hs : (if χ i then 0 else Complex.normSq (fullWord U z χ w k i z))≤
      rejectedWeight χ (fun j => fullWord U z χ w k j z) := by
    apply Finset.single_le_sum _ (Finset.mem_univ i)
    intro j _
    cases χ j <;> simp [Complex.normSq_nonneg]
  simpa [hi,unspunColumn,Complex.normSq_mul,map_pow,Complex.star_def,Complex.normSq_conj,hw] using hs

theorem all_literal_unspun_failed_coordinate_rates (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (U : Matrix ι ι ℂ) (z i : ι) (χ : ι → Bool) (hi : χ i=false)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he : rejectedWeight χ (fun j => U j z)≤11/16) (k : ℕ) :
    Complex.normSq (unspunColumn U z χ (fastGoldenPhase a p) (k+2) i)≤(1/16)^k/10 ∧
      ‖unspunColumn U z χ (fastGoldenPhase a p) (k+2) i‖≤(1/4)^k := by
  have hr := fast_parameter_native_bounds p hp hp0
  have hf := fast_all_full_failure_rate _ _ (le_of_lt hr.1) (le_of_lt hr.2)
    (rejected_weight_nonnegative χ (fun j => U j z)) he k
  have h0 := all_unspun_failed_coordinates_have_full_mass_bound U z i χ _ (k+2)
    (fast_golden_phase_normSq a p ha hp) hi
  rw [actual_full_word_fast_failure a p U z χ ha hp hU] at h0
  have h := h0.trans hf.2.2
  refine ⟨h,?_⟩
  have hn := norm_nonneg (unspunColumn U z χ (fastGoldenPhase a p) (k+2) i)
  have hb := pow_nonneg (by norm_num : (0:ℝ)≤1/4) k
  have heq : ((1/4 : ℝ)^k)^2=(1/16)^k := by
    rw [← pow_mul,Nat.mul_comm k 2,pow_mul]
    norm_num
  rw [Complex.normSq_eq_norm_sq] at h
  nlinarith [pow_nonneg (by norm_num : (0:ℝ)≤1/16) k]

theorem literal_unspun_failed_coordinate_tends_zero (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (U : Matrix ι ι ℂ) (z i : ι) (χ : ι → Bool) (hi : χ i=false)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he : rejectedWeight χ (fun j => U j z)≤11/16) :
    Tendsto (fun k => unspunColumn U z χ (fastGoldenPhase a p) (k+2) i) atTop (𝓝 0) := by
  apply tendsto_iff_norm_sub_tendsto_zero.mpr
  simp only [sub_zero]
  apply squeeze_zero (fun _ => norm_nonneg _) (fun k =>
    (all_literal_unspun_failed_coordinate_rates a p ha hp hp0 U z i χ hi hU he k).2)
  exact tendsto_pow_atTop_nhds_zero_of_lt_one (by norm_num : (0:ℝ)≤1/4)
    (by norm_num : (1/4:ℝ)<1)

theorem complete_literal_unspun_column_has_fixed_normalized_limit (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he : rejectedWeight χ (fun j => U j z)≤11/16) :
    ∃ L : ι → ℂ,
      Tendsto (fun k => unspunColumn U z χ (fastGoldenPhase a p) (k+2)) atTop (𝓝 L) ∧
      vectorWeight L=1 ∧ (∀ i, χ i=false → L i=0) := by
  have hall (i : ι) : ∃ Li : ℂ,
      Tendsto (fun k => unspunColumn U z χ (fastGoldenPhase a p) (k+2) i) atTop (𝓝 Li) ∧
        (χ i=false → Li=0) := by
    cases hi : χ i
    · exact ⟨0,literal_unspun_failed_coordinate_tends_zero a p ha hp hp0 U z i χ hi hU he,
        by intro _; rfl⟩
    · obtain ⟨Li,hLi,_⟩ := literal_good_coordinate_has_fixed_calibration a p ha hp hp0 U z i χ hi hU he
      exact ⟨Li,hLi,by simp [hi]⟩
  choose L hL hz using hall
  refine ⟨L,tendsto_pi_nhds.mpr hL,?_,hz⟩
  have hm : Tendsto (fun k => vectorWeight (unspunColumn U z χ (fastGoldenPhase a p) (k+2)))
      atTop (𝓝 (vectorWeight L)) := by
    unfold vectorWeight
    apply tendsto_finset_sum
    intro i _
    exact Complex.continuous_normSq.continuousAt.tendsto.comp (hL i)
  have hn : Tendsto (fun k => vectorWeight (unspunColumn U z χ (fastGoldenPhase a p) (k+2)))
      atTop (𝓝 1) := by
    have heq (k : ℕ) := all_unspun_full_columns_normalized U z χ (fastGoldenPhase a p) (k+2)
      hU (fast_golden_phase_normSq a p ha hp)
    simp_rw [heq]
    exact tendsto_const_nhds
  exact tendsto_nhds_unique hm hn

end
end D0.Research.GoldenFixedCalibration

namespace D0.Research.GoldenFixedCalibration
noncomputable section
open Matrix Complex D0.Research.GoldenCoherentAmplification

def realPointerBlank : Matrix (Fin 2) (Fin 2) ℝ := !![1,0;0,0]

theorem scalar_complex_projection_cannot_detect_unit_phase (w : ℂ) (hw : Complex.normSq w=1) :
    pureProjection (fun _ : PUnit => w)=pureProjection (fun _ : PUnit => (1 : ℂ)) := by
  ext i j
  simp only [pureProjection,Matrix.vecMulVec,Matrix.of_apply,Pi.star_apply,star_one,mul_one]
  rw [mul_comm,complete_unit_phase_star_product w hw]

theorem real_pointer_projection_detects_phase (w : ℂ) (hi : w.im≠0) :
    phaseRealMatrix w*realPointerBlank*(phaseRealMatrix w).transpose≠realPointerBlank := by
  intro h
  have hh := congrFun (congrFun h (1 : Fin 2)) (1 : Fin 2)
  simp [phaseRealMatrix,realPointerBlank,Matrix.mul_apply,Fin.sum_univ_two] at hh
  apply hi
  nlinarith

theorem own_fast_phase_visible_to_real_pointer (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) :
    phaseRealMatrix (fastGoldenPhase a p)*realPointerBlank*
      (phaseRealMatrix (fastGoldenPhase a p)).transpose≠realPointerBlank := by
  apply real_pointer_projection_detects_phase
  have h := own_fast_phase_has_nonzero_relative_area a p 0 1 ha hp hp0 (by norm_num)
  rw [distinct_success_laws_have_relative_phase_area _ _ _ (fast_golden_phase_normSq a p ha hp)] at h
  intro hz
  rw [hz,mul_zero] at h
  exact h rfl

end
end D0.Research.GoldenFixedCalibration

namespace D0.Research.GoldenFixedCalibration
noncomputable section
open Matrix Complex Filter Topology D0.Research.GoldenCoherentAmplification
open D0.Research.GoldenHistoryPreparation

theorem actual_scene_seed_is_in_fixed_limit_basin (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) (v : Fin 33) :
    rejectedWeight (codeValidity 4 5 (sceneAcceptedCodes v))
      (fun i => routedGoldenSeed a p 4 5 i (completeBlank 4 5))≤11/16 := by
  rw [literal_five_stream_seed_failure a p ha hp]
  have hs := actual_scene_accepted_codes_exact_degrees v
  have h0 : 20≤((sceneAcceptedCodes v).card : ℝ) := by
    rcases hs with h|h|h <;> rw [h] <;> norm_num
  have h1 : ((sceneAcceptedCodes v).card : ℝ)≤24 := by
    rcases hs with h|h|h <;> rw [h] <;> norm_num
  exact (native_preparation_enters_retained_contraction a p _ ha hp hp0 h0 h1).2

theorem actual_whole_scene_unspun_column_has_fixed_normalized_limit (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) (v : Fin 33) :
    ∃ L : CompleteSeedCarrier 4 5 → ℂ,
      Tendsto (fun k => unspunColumn (routedGoldenSeed a p 4 5) (completeBlank 4 5)
        (codeValidity 4 5 (sceneAcceptedCodes v)) (fastGoldenPhase a p) (k+2)) atTop (𝓝 L) ∧
      vectorWeight L=1 ∧ (∀ i, codeValidity 4 5 (sceneAcceptedCodes v) i=false → L i=0) := by
  exact complete_literal_unspun_column_has_fixed_normalized_limit a p ha hp hp0 _ _ _
    (actual_retained_routed_seed_unitary a p ha hp 4 5)
    (actual_scene_seed_is_in_fixed_limit_basin a p ha hp hp0 v)

theorem actual_scene_complete_success_coefficient_nonzero (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) (v : Fin 33) (k : ℕ) :
    fastAcceptedCoefficient a p (rejectedWeight (codeValidity 4 5 (sceneAcceptedCodes v))
      (fun i => routedGoldenSeed a p 4 5 i (completeBlank 4 5))) (k+2)≠0 := by
  have hs := (native_literal_full_vector_error a p ha hp hp0 _
    (actual_scene_accepted_codes_exact_degrees v) k).1
  intro hc
  have hz : acceptedWeight (codeValidity 4 5 (sceneAcceptedCodes v)) (fun i =>
      fullWord (routedGoldenSeed a p 4 5) (completeBlank 4 5)
        (codeValidity 4 5 (sceneAcceptedCodes v)) (fastGoldenPhase a p) (k+2) i (completeBlank 4 5))=0 := by
    unfold acceptedWeight
    apply Finset.sum_eq_zero
    intro i _
    cases hi : codeValidity 4 5 (sceneAcceptedCodes v) i
    · simp [hi]
    · change Complex.normSq (fullWord (routedGoldenSeed a p 4 5) (completeBlank 4 5)
        (codeValidity 4 5 (sceneAcceptedCodes v)) (fastGoldenPhase a p) (k+2) i (completeBlank 4 5))=0
      rw [complete_fast_word_all_record_coefficients a p _ _ _ ha hp
        (actual_retained_routed_seed_unitary a p ha hp 4 5),hi,hc]
      simp
  rw [hz] at hs
  exact (lt_irrefl 0) hs

theorem actual_scene_complex_projection_only_preparation_error (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) (v : Fin 33) (k : ℕ) :
    frobeniusWeight (pureProjection (fun i =>
      fullWord (routedGoldenSeed a p 4 5) (completeBlank 4 5)
        (codeValidity 4 5 (sceneAcceptedCodes v)) (fastGoldenPhase a p) (k+2) i (completeBlank 4 5))-
      normalizedAcceptedProjection (codeValidity 4 5 (sceneAcceptedCodes v))
        (fun i => routedGoldenSeed a p 4 5 i (completeBlank 4 5)))≤(1/16)^k/5 := by
  have hu := actual_retained_routed_seed_unitary a p ha hp 4 5
  have huk := all_full_words_unitary _ (completeBlank 4 5) (codeValidity 4 5 (sceneAcceptedCodes v))
    (fastGoldenPhase a p) hu (fast_golden_phase_normSq a p ha hp) (k+2)
  have hn := unitary_column_has_complete_weight _ (completeBlank 4 5) huk.1
  have hs := (native_literal_full_vector_error a p ha hp hp0 _
    (actual_scene_accepted_codes_exact_degrees v) k).1
  have hc := actual_scene_complete_success_coefficient_nonzero a p ha hp hp0 v k
  rw [← full_fast_word_target_projection_is_fixed a p _ (completeBlank 4 5)
    (codeValidity 4 5 (sceneAcceptedCodes v)) ha hp hu (k+2) hc,
    whole_unconditional_prepared_projection_error _ _ hn hs]
  have h := actual_scene_full_word_failure_rate a p ha hp hp0 v k
  linarith

section Refinement
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

theorem actual_golden_inclusion_preserves_fixed_limit {x : ℕ → ι → ℂ} {L : ι → ℂ}
    (a p : ℝ) (hL : Tendsto x atTop (𝓝 L)) :
    Tendsto (fun k => goldenComplexInclusion a p (x k)) atTop
      (𝓝 (goldenComplexInclusion a p L)) := by
  apply tendsto_pi_nhds.mpr
  intro s
  have h := (tendsto_pi_nhds.mp hL) s.1
  exact h.mul_const (if s.2 then (p : ℂ) else (a : ℂ))

theorem actual_golden_fixed_limit_normalization (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (L : ι → ℂ) (hL : vectorWeight L=1) :
    vectorWeight (goldenComplexInclusion a p L)=1 := by
  rw [golden_complex_inclusion_weight a p ha hp,hL]

end Refinement
end
end D0.Research.GoldenFixedCalibration

namespace D0.Research.GoldenFixedCalibration
noncomputable section
open Matrix Complex D0.Research.GoldenCoherentAmplification
open D0.Representation.GoldenOrderInterferometer

theorem conjugate_phase_is_real_inverse_orientation (w : ℂ) :
    phaseRealMatrix (star w)=(phaseRealMatrix w).transpose := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [phaseRealMatrix,Complex.star_def]

theorem actual_global_unspin_is_owned_golden_word (a p : ℝ) (ha : a^2=p) (k : ℕ) :
    phaseRealMatrix ((star (fastGoldenPhase a p))^(2*k))=
      ((gate a p)^(16*k)).transpose := by
  rw [phase_real_matrix_powers,conjugate_phase_is_real_inverse_orientation,
    fast_phase_is_owned_golden_eighth_power a p ha,← Matrix.transpose_pow,← pow_mul]
  congr 1
  congr 1
  omega

end
end D0.Research.GoldenFixedCalibration

namespace D0.Research.GoldenFixedCalibration
noncomputable section
open Matrix Complex D0.Research.GoldenCoherentAmplification
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def RealEntry (A : Matrix ι ι ℂ) : Prop := ∀ i j, (A i j).im=0

theorem all_native_real_matrix_casts_have_real_entries (A : Matrix ι ι ℝ) :
    RealEntry (A.map (fun x : ℝ => (x : ℂ))) := by
  intro i j
  simp

theorem all_real_entry_products_remain_real (A B : Matrix ι ι ℂ)
    (hA : RealEntry A) (hB : RealEntry B) : RealEntry (A*B) := by
  intro i j
  simp only [Matrix.mul_apply,Complex.im_sum,Complex.mul_im]
  apply Finset.sum_eq_zero
  intro k _
  rw [hA i k,hB k j]
  ring

theorem all_real_entry_adjoints_remain_real (A : Matrix ι ι ℂ)
    (hA : RealEntry A) : RealEntry A.conjTranspose := by
  intro i j
  simp [Matrix.conjTranspose_apply,Complex.star_def,hA j i]

theorem all_real_entry_words_preserve_real_columns (A : Matrix ι ι ℂ)
    (hA : RealEntry A) (x : ι → ℂ) (hx : ∀ i, (x i).im=0) :
    ∀ i, (A.mulVec x i).im=0 := by
  intro i
  simp only [Matrix.mulVec,dotProduct,Complex.im_sum,Complex.mul_im]
  apply Finset.sum_eq_zero
  intro j _
  rw [hA i j,hx j]
  ring

theorem direct_nonreal_phase_oracle_outside_real_entry_class (χ : ι → Bool)
    (w : ℂ) (hw : w.im≠0) (i : ι) (hi : χ i=true) :
    ¬RealEntry (diagonalPhase χ w) := by
  intro h
  have hh := h i i
  simp [diagonalPhase,hi] at hh
  exact hw hh

theorem actual_golden_fast_phase_oracle_outside_real_entry_class (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (χ : ι → Bool) (i : ι) (hi : χ i=true) :
    ¬RealEntry (diagonalPhase χ (fastGoldenPhase a p)) := by
  apply direct_nonreal_phase_oracle_outside_real_entry_class χ _ _ i hi
  have h := own_fast_phase_has_nonzero_relative_area a p 0 1 ha hp hp0 (by norm_num)
  rw [distinct_success_laws_have_relative_phase_area _ _ _ (fast_golden_phase_normSq a p ha hp)] at h
  intro hz
  rw [hz,mul_zero] at h
  exact h rfl

end
end D0.Research.GoldenFixedCalibration

namespace D0.Research.GoldenFixedCalibration
noncomputable section
open Matrix Complex Filter Topology D0.Research.GoldenCoherentAmplification
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def normalizedSuccessScalar (a p : ℝ) (U : Matrix ι ι ℂ) (z : ι)
    (χ : ι → Bool) (k : ℕ) : ℂ :=
  (Real.sqrt (acceptedWeight χ (fun i => U i z)) : ℂ)*
    (star (fastGoldenPhase a p))^(2*k)*
    fastAcceptedCoefficient a p (rejectedWeight χ (fun i => U i z)) k

theorem actual_initial_accepted_mass_positive (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (hU : U.conjTranspose*U=1)
    (he : rejectedWeight χ (fun i => U i z)≤11/16) :
    0<acceptedWeight χ (fun i => U i z) := by
  have h := complete_weight_partition χ (fun i => U i z)
  rw [unitary_column_has_complete_weight U z hU] at h
  linarith

theorem actual_normalized_success_factorization (a p : ℝ) (U : Matrix ι ι ℂ)
    (z : ι) (χ : ι → Bool) (ha : a^2=p) (hp : p+p^2=1)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (hs : 0<acceptedWeight χ (fun i => U i z)) (k : ℕ) (i : ι) (hi : χ i=true) :
    unspunColumn U z χ (fastGoldenPhase a p) k i=
      normalizedSuccessScalar a p U z χ k*alignedAcceptedVector χ (fun i => U i z) i := by
  have ht : (Real.sqrt (acceptedWeight χ (fun i => U i z)) : ℂ)≠0 := by
    exact_mod_cast ne_of_gt (Real.sqrt_pos.mpr hs)
  unfold unspunColumn normalizedSuccessScalar alignedAcceptedVector
  rw [complete_fast_word_all_record_coefficients a p U z χ ha hp hU k i,hi]
  simp only [if_true]
  field_simp
  <;> ring

theorem normalized_success_scalar_full_balance (a p : ℝ) (U : Matrix ι ι ℂ)
    (z : ι) (χ : ι → Bool) (ha : a^2=p) (hp : p+p^2=1)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (hs : 0<acceptedWeight χ (fun i => U i z)) (k : ℕ) :
    Complex.normSq (normalizedSuccessScalar a p U z χ k)+
      rejectedWeight χ (fun i => fullWord U z χ (fastGoldenPhase a p) k i z)=1 := by
  have hc : acceptedWeight χ (unspunColumn U z χ (fastGoldenPhase a p) k)=
      Complex.normSq (normalizedSuccessScalar a p U z χ k) := by
    have h1 : acceptedWeight χ (unspunColumn U z χ (fastGoldenPhase a p) k)=
        acceptedWeight χ (fun i => normalizedSuccessScalar a p U z χ k*
          alignedAcceptedVector χ (fun j => U j z) i) := by
      unfold acceptedWeight
      apply Finset.sum_congr rfl
      intro i _
      cases hi : χ i
      · simp [hi]
      · rw [actual_normalized_success_factorization a p U z χ ha hp hU hs k i hi]
    rw [h1,complete_accepted_mass_scalar]
    have h2 : acceptedWeight χ (alignedAcceptedVector χ (fun j => U j z))=1 := by
      calc _ = vectorWeight (alignedAcceptedVector χ (fun j => U j z)) := by
             unfold acceptedWeight vectorWeight
             apply Finset.sum_congr rfl
             intro i _
             cases hi : χ i <;> simp [alignedAcceptedVector,hi]
           _ = 1 := aligned_accepted_vector_has_complete_weight χ (fun j => U j z) hs
    rw [h2,mul_one]
  have hr : rejectedWeight χ (unspunColumn U z χ (fastGoldenPhase a p) k)=
      rejectedWeight χ (fun i => fullWord U z χ (fastGoldenPhase a p) k i z) := by
    unfold rejectedWeight unspunColumn
    apply Finset.sum_congr rfl
    intro i _
    cases χ i <;> simp [Complex.normSq_mul,map_pow,Complex.star_def,
      Complex.normSq_conj,fast_golden_phase_normSq a p ha hp]
  have h := complete_weight_partition χ (unspunColumn U z χ (fastGoldenPhase a p) k)
  rw [hc,hr,all_unspun_full_columns_normalized U z χ (fastGoldenPhase a p) k
    hU (fast_golden_phase_normSq a p ha hp)] at h
  exact h

theorem normalized_success_scalar_increment (a p : ℝ) (U : Matrix ι ι ℂ)
    (z : ι) (χ : ι → Bool) (ha : a^2=p) (hp : p+p^2=1) (k : ℕ) :
    normalizedSuccessScalar a p U z χ (k+1)-normalizedSuccessScalar a p U z χ k=
      -((star (fastGoldenPhase a p))^2*(fastGoldenPhase a p-1)^2*
        (fastFailure (fastParameter p) (rejectedWeight χ (fun i => U i z)) k : ℂ)*
        normalizedSuccessScalar a p U z χ k) := by
  have hw := fast_golden_phase_normSq a p ha hp
  have h : (star (fastGoldenPhase a p))^2*(fastGoldenPhase a p)^2=1 := by
    rw [← mul_pow,complete_unit_phase_star_product _ hw,one_pow]
  unfold normalizedSuccessScalar
  rw [fastAcceptedCoefficient]
  unfold goodMultiplier
  rw [show 2*(k+1)=2*k+2 by omega,pow_add]
  linear_combination (Real.sqrt (acceptedWeight χ (fun i => U i z)) : ℂ)*
    (star (fastGoldenPhase a p))^(2*k)*
    fastAcceptedCoefficient a p (rejectedWeight χ (fun i => U i z)) k*h

theorem normalized_success_scalar_norm_le_one (a p : ℝ) (U : Matrix ι ι ℂ)
    (z : ι) (χ : ι → Bool) (ha : a^2=p) (hp : p+p^2=1)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (hs : 0<acceptedWeight χ (fun i => U i z)) (k : ℕ) :
    ‖normalizedSuccessScalar a p U z χ k‖≤1 := by
  have h := normalized_success_scalar_full_balance a p U z χ ha hp hU hs k
  have h0 := rejected_weight_nonnegative χ
    (fun i => fullWord U z χ (fastGoldenPhase a p) k i z)
  rw [Complex.normSq_eq_norm_sq] at h
  nlinarith [norm_nonneg (normalizedSuccessScalar a p U z χ k)]

theorem normalized_success_scalar_increment_bound (a p : ℝ) (U : Matrix ι ι ℂ)
    (z : ι) (χ : ι → Bool) (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he : rejectedWeight χ (fun i => U i z)≤11/16) (k : ℕ) :
    dist (normalizedSuccessScalar a p U z χ (k+2))
      (normalizedSuccessScalar a p U z χ (k+1+2))≤(1/16)^k/10 := by
  have hr := fast_parameter_native_bounds p hp hp0
  have hs := actual_initial_accepted_mass_positive U z χ hU.1 he
  have hf := fast_all_full_failure_rate _ _ (le_of_lt hr.1) (le_of_lt hr.2)
    (rejected_weight_nonnegative χ (fun i => U i z)) he k
  have heq : k+1+2=k+2+1 := by omega
  rw [heq,dist_comm,dist_eq_norm,normalized_success_scalar_increment a p U z χ ha hp]
  rw [norm_neg,norm_mul,norm_mul,own_fast_phase_increment_factor_norm a p ha hp]
  have hn := normalized_success_scalar_norm_le_one a p U z χ ha hp hU hs (k+2)
  have he0 := hf.1
  rw [Complex.norm_real,Real.norm_eq_abs,abs_of_nonneg he0]
  have hm0 := mul_le_mul_of_nonneg_right (show 1-fastParameter p≤1 by linarith) he0
  have hm1 := mul_le_mul_of_nonneg_left hn (mul_nonneg (by linarith : 0≤1-fastParameter p) he0)
  exact (by nlinarith : (1-fastParameter p)*
    fastFailure (fastParameter p) (rejectedWeight χ (fun i => U i z)) (k+2)*
      ‖normalizedSuccessScalar a p U z χ (k+2)‖≤
        fastFailure (fastParameter p) (rejectedWeight χ (fun i => U i z)) (k+2)).trans hf.2.2

theorem complete_literal_rejected_mass_tends_zero (a p : ℝ) (U : Matrix ι ι ℂ)
    (z : ι) (χ : ι → Bool) (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he : rejectedWeight χ (fun i => U i z)≤11/16) :
    Tendsto (fun k => rejectedWeight χ
      (fun i => fullWord U z χ (fastGoldenPhase a p) (k+2) i z)) atTop (𝓝 0) := by
  have hr := fast_parameter_native_bounds p hp hp0
  have hh (k : ℕ) : rejectedWeight χ
      (fun i => fullWord U z χ (fastGoldenPhase a p) (k+2) i z)≤(1/16)^k/10 := by
    rw [actual_full_word_fast_failure a p U z χ ha hp hU]
    exact (fast_all_full_failure_rate _ _ (le_of_lt hr.1) (le_of_lt hr.2)
      (rejected_weight_nonnegative χ (fun i => U i z)) he k).2.2
  have h := tendsto_pow_atTop_nhds_zero_of_lt_one (by norm_num : (0:ℝ)≤1/16)
    (by norm_num : (1/16:ℝ)<1)
  have ht : Tendsto (fun k : ℕ => (1/16:ℝ)^k/10) atTop (𝓝 0) := by
    simpa using h.div_const (10:ℝ)
  exact squeeze_zero (fun _ => rejected_weight_nonnegative χ _) hh ht

theorem complete_normalized_success_has_fixed_unit_calibration (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he : rejectedWeight χ (fun i => U i z)≤11/16) :
    ∃ γ : ℂ, Complex.normSq γ=1 ∧
      Tendsto (fun k => normalizedSuccessScalar a p U z χ (k+2)) atTop (𝓝 γ) ∧
      ∀ k, dist (normalizedSuccessScalar a p U z χ (k+2)) γ≤(8/75)*(1/16)^k := by
  have hh (k : ℕ) := normalized_success_scalar_increment_bound a p U z χ ha hp hp0 hU he k
  have hc := cauchySeq_of_le_geometric (1/16) (1/10) (by norm_num : (1/16:ℝ)<1)
    (by intro k; simpa [div_eq_mul_inv,mul_comm] using hh k)
  obtain ⟨γ,hγ⟩ := cauchySeq_tendsto_of_complete hc
  have hs := actual_initial_accepted_mass_positive U z χ hU.1 he
  have hn : Tendsto (fun k => Complex.normSq (normalizedSuccessScalar a p U z χ (k+2)))
      atTop (𝓝 1) := by
    have h := (tendsto_const_nhds : Tendsto (fun _ : ℕ => (1:ℝ)) atTop (𝓝 1)).sub
      (complete_literal_rejected_mass_tends_zero a p U z χ ha hp hp0 hU he)
    simp only [sub_zero] at h
    convert h using 1
    funext k
    have heq := normalized_success_scalar_full_balance a p U z χ ha hp hU hs (k+2)
    linarith
  have hsq := Complex.continuous_normSq.continuousAt.tendsto.comp hγ
  refine ⟨γ,tendsto_nhds_unique hsq hn,hγ,?_⟩
  intro k
  have h := dist_le_of_le_geometric_of_tendsto (1/16) (1/10)
    (by norm_num : (1/16:ℝ)<1)
    (by intro j; simpa [div_eq_mul_inv,mul_comm] using hh j) hγ k
  convert h using 1 <;> ring

end
end D0.Research.GoldenFixedCalibration

namespace D0.Research.GoldenFixedCalibration
noncomputable section
open Matrix Complex Filter Topology D0.Research.GoldenCoherentAmplification
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

theorem actual_unspun_rejected_weight_preserved (U : Matrix ι ι ℂ) (z : ι)
    (χ : ι → Bool) (w : ℂ) (k : ℕ) (hw : Complex.normSq w=1) :
    rejectedWeight χ (unspunColumn U z χ w k)=
      rejectedWeight χ (fun i => fullWord U z χ w k i z) := by
  unfold rejectedWeight unspunColumn
  apply Finset.sum_congr rfl
  intro i _
  cases χ i <;> simp [Complex.normSq_mul,map_pow,Complex.star_def,Complex.normSq_conj,hw]

theorem aligned_accepted_vector_has_accepted_weight (χ : ι → Bool) (x : ι → ℂ)
    (hs : 0<acceptedWeight χ x) :
    acceptedWeight χ (alignedAcceptedVector χ x)=1 := by
  calc _ = vectorWeight (alignedAcceptedVector χ x) := by
         unfold acceptedWeight vectorWeight
         apply Finset.sum_congr rfl
         intro i _
         cases hi : χ i <;> simp [alignedAcceptedVector,hi]
       _ = 1 := aligned_accepted_vector_has_complete_weight χ x hs

theorem all_size_complete_fixed_target_distance_identity (a p : ℝ) (U : Matrix ι ι ℂ)
    (z : ι) (χ : ι → Bool) (ha : a^2=p) (hp : p+p^2=1)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (hs : 0<acceptedWeight χ (fun i => U i z)) (k : ℕ) (γ : ℂ) :
    vectorWeight (fun i => unspunColumn U z χ (fastGoldenPhase a p) k i-
      γ*alignedAcceptedVector χ (fun j => U j z) i)=
        Complex.normSq (normalizedSuccessScalar a p U z χ k-γ)+
          rejectedWeight χ (fun i => fullWord U z χ (fastGoldenPhase a p) k i z) := by
  have h : vectorWeight (fun i => unspunColumn U z χ (fastGoldenPhase a p) k i-
      γ*alignedAcceptedVector χ (fun j => U j z) i)=
        Complex.normSq (normalizedSuccessScalar a p U z χ k-γ)*
          acceptedWeight χ (alignedAcceptedVector χ (fun j => U j z))+
            rejectedWeight χ (unspunColumn U z χ (fastGoldenPhase a p) k) := by
    unfold vectorWeight acceptedWeight rejectedWeight
    rw [Finset.mul_sum,← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro i _
    cases hi : χ i
    · simp [alignedAcceptedVector,hi]
    · simp only [hi,if_true,add_zero]
      rw [actual_normalized_success_factorization a p U z χ ha hp hU hs k i hi]
      rw [← Complex.normSq_mul]
      congr 1
      ring
  rw [h,aligned_accepted_vector_has_accepted_weight χ _ hs,mul_one,
    actual_unspun_rejected_weight_preserved U z χ _ k (fast_golden_phase_normSq a p ha hp)]

theorem vector_weight_scalar_factor (c : ℂ) (x : ι → ℂ) :
    vectorWeight (fun i => c*x i)=Complex.normSq c*vectorWeight x := by
  unfold vectorWeight
  simp only [Complex.normSq_mul,Finset.mul_sum]

theorem all_size_fixed_target_has_complete_unit_weight (χ : ι → Bool) (x : ι → ℂ)
    (hs : 0<acceptedWeight χ x) (γ : ℂ) (hγ : Complex.normSq γ=1) :
    vectorWeight (fun i => γ*alignedAcceptedVector χ x i)=1 := by
  rw [vector_weight_scalar_factor,hγ,one_mul,aligned_accepted_vector_has_complete_weight χ x hs]

theorem all_size_complete_fixed_calibration_rate (a p : ℝ) (U : Matrix ι ι ℂ)
    (z : ι) (χ : ι → Bool) (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he : rejectedWeight χ (fun i => U i z)≤11/16) :
    ∃ γ : ℂ, Complex.normSq γ=1 ∧
      vectorWeight (fun i => γ*alignedAcceptedVector χ (fun j => U j z) i)=1 ∧
      ∀ k, vectorWeight (fun i => unspunColumn U z χ (fastGoldenPhase a p) (k+2) i-
        γ*alignedAcceptedVector χ (fun j => U j z) i)≤(1/8)*(1/16)^k := by
  obtain ⟨γ,hγ,hlim,hbound⟩ :=
    complete_normalized_success_has_fixed_unit_calibration a p U z χ ha hp hp0 hU he
  have hs := actual_initial_accepted_mass_positive U z χ hU.1 he
  refine ⟨γ,hγ,all_size_fixed_target_has_complete_unit_weight χ _ hs γ hγ,?_⟩
  intro k
  rw [all_size_complete_fixed_target_distance_identity a p U z χ ha hp hU hs (k+2),
    actual_full_word_fast_failure a p U z χ ha hp hU]
  have hr := fast_parameter_native_bounds p hp hp0
  have hf := fast_all_full_failure_rate _ _ (le_of_lt hr.1) (le_of_lt hr.2)
    (rejected_weight_nonnegative χ (fun i => U i z)) he k
  have h0 : 0≤(1/16:ℝ)^k := pow_nonneg (by norm_num) k
  have h1 : (1/16:ℝ)^k≤1 := pow_le_one₀ (by norm_num) (by norm_num)
  have hn := norm_nonneg (normalizedSuccessScalar a p U z χ (k+2)-γ)
  rw [Complex.normSq_eq_norm_sq]
  have hnorm := hbound k
  rw [dist_eq_norm] at hnorm
  nlinarith [mul_nonneg h0 (sub_nonneg.mpr h1)]

end
end D0.Research.GoldenFixedCalibration

namespace D0.Research.GoldenFixedCalibration
noncomputable section
open Matrix Complex D0.Research.GoldenCoherentAmplification
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def fullRealVector (x : ι → ℂ) : ι × Fin 2 → ℝ :=
  fun s => if s.2=0 then (x s.1).re else (x s.1).im

def fullRealMatrix (A : Matrix ι ι ℂ) : Matrix (ι × Fin 2) (ι × Fin 2) ℝ :=
  fun s t => phaseRealMatrix (A s.1 t.1) s.2 t.2

def realVectorWeight (x : ι → ℝ) : ℝ := ∑ i, (x i)^2

theorem full_real_encoding_retains_complete_weight (x : ι → ℂ) :
    realVectorWeight (fullRealVector x)=vectorWeight x := by
  unfold realVectorWeight vectorWeight
  rw [Fintype.sum_prod_type]
  apply Finset.sum_congr rfl
  intro i _
  simp [fullRealVector,Fin.sum_univ_two,Complex.normSq_apply]
  ring

theorem full_real_encoding_is_injective : Function.Injective (@fullRealVector ι) := by
  intro x y h
  funext i
  apply Complex.ext
  · have hh := congrFun h (i,0)
    simpa [fullRealVector] using hh
  · have hh := congrFun h (i,1)
    simpa [fullRealVector] using hh

theorem full_real_encoding_subtracts (x y : ι → ℂ) :
    fullRealVector (fun i => x i-y i)=fun s => fullRealVector x s-fullRealVector y s := by
  funext s
  rcases s with ⟨i,b⟩
  fin_cases b <;> simp [fullRealVector]

theorem full_real_matrix_preserves_identity : fullRealMatrix (1 : Matrix ι ι ℂ)=1 := by
  ext s t
  rcases s with ⟨i,b⟩
  rcases t with ⟨j,c⟩
  by_cases hij : i=j
  · subst j
    fin_cases b <;> fin_cases c <;> simp [fullRealMatrix,phaseRealMatrix,Matrix.one_apply]
  · fin_cases b <;> fin_cases c <;>
      simp [fullRealMatrix,phaseRealMatrix,Matrix.one_apply,hij,Prod.mk.injEq]

theorem full_real_matrix_preserves_product (A B : Matrix ι ι ℂ) :
    fullRealMatrix (A*B)=fullRealMatrix A*fullRealMatrix B := by
  ext s t
  rcases s with ⟨i,b⟩
  rcases t with ⟨j,c⟩
  fin_cases b <;> fin_cases c <;>
    simp [fullRealMatrix,phaseRealMatrix,Matrix.mul_apply,Fintype.sum_prod_type,Fin.sum_univ_two,
      Complex.mul_re,Complex.mul_im,Complex.re_sum,Complex.im_sum,Finset.sum_sub_distrib,
      Finset.sum_add_distrib,Finset.sum_neg_distrib]
  all_goals ring

theorem full_real_matrix_preserves_adjoint (A : Matrix ι ι ℂ) :
    fullRealMatrix A.conjTranspose=(fullRealMatrix A).transpose := by
  ext s t
  rcases s with ⟨i,b⟩
  rcases t with ⟨j,c⟩
  fin_cases b <;> fin_cases c <;>
    simp [fullRealMatrix,phaseRealMatrix,Matrix.conjTranspose_apply,Complex.star_def]

theorem full_real_matrix_intertwines_every_state (A : Matrix ι ι ℂ) (x : ι → ℂ) :
    fullRealVector (A.mulVec x)=(fullRealMatrix A).mulVec (fullRealVector x) := by
  funext s
  rcases s with ⟨i,b⟩
  fin_cases b <;>
    simp [fullRealVector,fullRealMatrix,phaseRealMatrix,Matrix.mulVec,dotProduct,
      Fintype.sum_prod_type,Fin.sum_univ_two,Complex.mul_re,Complex.mul_im,
      Complex.re_sum,Complex.im_sum,Finset.sum_sub_distrib,Finset.sum_add_distrib,
      Finset.sum_neg_distrib]
  all_goals ring

theorem every_full_real_unitary_word_is_orthogonal (U : Matrix ι ι ℂ)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1) :
    (fullRealMatrix U).transpose*fullRealMatrix U=1 ∧
      fullRealMatrix U*(fullRealMatrix U).transpose=1 := by
  constructor
  · rw [← full_real_matrix_preserves_adjoint,← full_real_matrix_preserves_product,
      hU.1,full_real_matrix_preserves_identity]
  · rw [← full_real_matrix_preserves_adjoint,← full_real_matrix_preserves_product,
      hU.2,full_real_matrix_preserves_identity]

theorem literal_full_real_recursive_word (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (w : ℂ) (k : ℕ) :
    fullRealMatrix (fullWord U z χ w (k+1))=
      fullRealMatrix (fullWord U z χ w k)*fullRealMatrix (blankPhase z w)*
        (fullRealMatrix (fullWord U z χ w k)).transpose*
          fullRealMatrix (diagonalPhase χ w)*fullRealMatrix (fullWord U z χ w k) := by
  change fullRealMatrix (fullAmplify (fullWord U z χ w k) z χ w)=_
  unfold fullAmplify
  simp only [full_real_matrix_preserves_product,full_real_matrix_preserves_adjoint]

theorem full_real_state_preserves_complete_fixed_limit_rate (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he : rejectedWeight χ (fun i => U i z)≤11/16) :
    ∃ γ : ℂ, Complex.normSq γ=1 ∧
      realVectorWeight (fullRealVector (fun i => γ*alignedAcceptedVector χ (fun j => U j z) i))=1 ∧
      ∀ k, realVectorWeight (fun s =>
        fullRealVector (unspunColumn U z χ (fastGoldenPhase a p) (k+2)) s-
          fullRealVector (fun i => γ*alignedAcceptedVector χ (fun j => U j z) i) s)≤(1/8)*(1/16)^k := by
  obtain ⟨γ,hγ,hunit,hbound⟩ := all_size_complete_fixed_calibration_rate a p U z χ ha hp hp0 hU he
  refine ⟨γ,hγ,?_,?_⟩
  · rw [full_real_encoding_retains_complete_weight,hunit]
  · intro k
    rw [← full_real_encoding_subtracts,full_real_encoding_retains_complete_weight]
    exact hbound k

end
end D0.Research.GoldenFixedCalibration

namespace D0.Research.GoldenFixedCalibration
noncomputable section
open Matrix Complex D0.Research.GoldenCoherentAmplification
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def realQuadraticReading (P : Matrix ι ι ℝ) (x : ι → ℝ) : ℝ := x ⬝ᵥ P.mulVec x

theorem real_complete_weight_is_self_dot (x : ι → ℝ) : realVectorWeight x=x ⬝ᵥ x := by
  simp [realVectorWeight,dotProduct,pow_two]

theorem real_complete_weight_nonnegative (x : ι → ℝ) : 0≤realVectorWeight x := by
  exact Finset.sum_nonneg (fun _ _ => sq_nonneg _)

theorem real_complete_weight_difference (x y : ι → ℝ) :
    realVectorWeight (x-y)=realVectorWeight x+realVectorWeight y-2*(x ⬝ᵥ y) := by
  simp only [realVectorWeight,Pi.sub_apply,dotProduct,Finset.sum_add_distrib,
    Finset.sum_sub_distrib,Finset.mul_sum]
  rw [← Finset.sum_add_distrib,← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem real_complete_weight_sum_bound (x y : ι → ℝ) :
    realVectorWeight (x+y)≤2*realVectorWeight x+2*realVectorWeight y := by
  unfold realVectorWeight
  rw [Finset.mul_sum,Finset.mul_sum,← Finset.sum_add_distrib]
  apply Finset.sum_le_sum
  intro i _
  change (x i+y i)^2≤2*(x i)^2+2*(y i)^2
  nlinarith [sq_nonneg (x i-y i)]

theorem real_projector_image_weight (P : Matrix ι ι ℝ)
    (hs : P.transpose=P) (hp : P*P=P) (x : ι → ℝ) :
    realVectorWeight (P.mulVec x)=realQuadraticReading P x := by
  have h := dotProduct_transpose_mulVec P x (P.mulVec x)
  rw [hs,mulVec_mulVec,hp] at h
  rw [real_complete_weight_is_self_dot]
  exact h.symm

theorem real_projector_contracts_every_complete_state (P : Matrix ι ι ℝ)
    (hs : P.transpose=P) (hp : P*P=P) (x : ι → ℝ) :
    realVectorWeight (P.mulVec x)≤realVectorWeight x := by
  have h := real_complete_weight_nonnegative (x-P.mulVec x)
  rw [real_complete_weight_difference,real_projector_image_weight P hs hp] at h
  unfold realQuadraticReading at h
  rw [real_projector_image_weight P hs hp]
  change x ⬝ᵥ P.mulVec x≤realVectorWeight x
  linarith

theorem real_symmetric_quadratic_difference_identity (P : Matrix ι ι ℝ)
    (hs : P.transpose=P) (x y : ι → ℝ) :
    realQuadraticReading P x-realQuadraticReading P y=
      (x-y) ⬝ᵥ P.mulVec (x+y) := by
  have h := dotProduct_transpose_mulVec P x y
  rw [hs] at h
  unfold realQuadraticReading
  rw [mulVec_add,sub_dotProduct,dotProduct_add,dotProduct_add,h]
  ring

theorem all_real_projector_readout_squared_error (P : Matrix ι ι ℝ)
    (hs : P.transpose=P) (hp : P*P=P) (x y : ι → ℝ)
    (hx : realVectorWeight x=1) (hy : realVectorWeight y=1) :
    (realQuadraticReading P x-realQuadraticReading P y)^2≤4*realVectorWeight (x-y) := by
  rw [real_symmetric_quadratic_difference_identity P hs]
  have hc := Finset.sum_mul_sq_le_sq_mul_sq Finset.univ (x-y) (P.mulVec (x+y))
  change ((x-y) ⬝ᵥ P.mulVec (x+y))^2≤
    realVectorWeight (x-y)*realVectorWeight (P.mulVec (x+y)) at hc
  have h1 := real_projector_contracts_every_complete_state P hs hp (x+y)
  have h2 := real_complete_weight_sum_bound x y
  rw [hx,hy] at h2
  have hn := real_complete_weight_nonnegative (x-y)
  have hm := mul_le_mul_of_nonneg_left (h1.trans (by linarith : realVectorWeight (x+y)≤4)) hn
  exact hc.trans (by simpa [mul_comm] using hm)

theorem full_real_fixed_limit_all_projector_readings (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he : rejectedWeight χ (fun i => U i z)≤11/16) :
    ∃ γ : ℂ, Complex.normSq γ=1 ∧
      ∀ (P : Matrix (ι × Fin 2) (ι × Fin 2) ℝ), P.transpose=P → P*P=P → ∀ k,
        (realQuadraticReading P (fullRealVector (unspunColumn U z χ (fastGoldenPhase a p) (k+2)))-
          realQuadraticReading P (fullRealVector (fun i => γ*alignedAcceptedVector χ
            (fun j => U j z) i)))^2≤(1/2)*(1/16)^k := by
  obtain ⟨γ,hγ,hunit,hbound⟩ := full_real_state_preserves_complete_fixed_limit_rate a p U z χ ha hp hp0 hU he
  refine ⟨γ,hγ,?_⟩
  intro P hPs hPp k
  have hx : realVectorWeight (fullRealVector
      (unspunColumn U z χ (fastGoldenPhase a p) (k+2)))=1 := by
    rw [full_real_encoding_retains_complete_weight,
      all_unspun_full_columns_normalized U z χ _ (k+2) hU (fast_golden_phase_normSq a p ha hp)]
  have hh := all_real_projector_readout_squared_error P hPs hPp _ _ hx hunit
  have hb := hbound k
  change realVectorWeight (fullRealVector
      (unspunColumn U z χ (fastGoldenPhase a p) (k+2))-
        fullRealVector (fun i => γ*alignedAcceptedVector χ (fun j => U j z) i))≤_ at hb
  nlinarith

end
end D0.Research.GoldenFixedCalibration

namespace D0.Research.GoldenFixedCalibration
noncomputable section
open Matrix Complex Filter Topology D0.Research.GoldenCoherentAmplification
open D0.Research.GoldenHistoryPreparation
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

theorem fixed_success_calibration_is_unique (a p : ℝ) (U : Matrix ι ι ℂ) (z : ι)
    (χ : ι → Bool) (γ δ : ℂ)
    (hγ : Tendsto (fun k => normalizedSuccessScalar a p U z χ (k+2)) atTop (𝓝 γ))
    (hδ : Tendsto (fun k => normalizedSuccessScalar a p U z χ (k+2)) atTop (𝓝 δ)) : γ=δ :=
  tendsto_nhds_unique hγ hδ

theorem actual_seed_forces_one_fixed_success_calibration (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he : rejectedWeight χ (fun i => U i z)≤11/16) :
    ∃! γ : ℂ, Tendsto (fun k => normalizedSuccessScalar a p U z χ (k+2)) atTop (𝓝 γ) := by
  obtain ⟨γ,_,hγ,_⟩ := complete_normalized_success_has_fixed_unit_calibration a p U z χ ha hp hp0 hU he
  exact ⟨γ,hγ,fun δ hδ => fixed_success_calibration_is_unique a p U z χ δ γ hδ hγ⟩

def historyCylinderInclusion (a p : ℝ) (n : ℕ) (x : ι → ℂ) : ι × Word n → ℂ :=
  fun s => x s.1*(amplitude a p s.2 : ℂ)

theorem every_golden_history_depth_preserves_complete_weight (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (n : ℕ) (x : ι → ℂ) :
    vectorWeight (historyCylinderInclusion a p n x)=vectorWeight x := by
  have hn : a^2+p^2=1 := by linarith
  have hmass := complete_mass a p hn n
  unfold vectorWeight historyCylinderInclusion
  simp only [Fintype.sum_prod_type,Complex.normSq_mul,Complex.normSq_ofReal,← pow_two]
  apply Finset.sum_congr rfl
  intro i _
  rw [← Finset.mul_sum,hmass,mul_one]

theorem all_golden_history_inclusions_subtract (a p : ℝ) (n : ℕ) (x y : ι → ℂ) :
    historyCylinderInclusion a p n (x-y)=historyCylinderInclusion a p n x-
      historyCylinderInclusion a p n y := by
  funext s
  simp [historyCylinderInclusion,sub_mul]

theorem every_golden_history_depth_intertwines_complete_operator (A : Matrix ι ι ℂ)
    (a p : ℝ) (n : ℕ) (x : ι → ℂ) :
    (suffixLift (X:=Word n) A).mulVec (historyCylinderInclusion a p n x)=
      historyCylinderInclusion a p n (A.mulVec x) := by
  ext s
  rcases s with ⟨i,w⟩
  simp [suffixLift,historyCylinderInclusion,Matrix.mulVec,dotProduct,
    Matrix.kroneckerMap_apply,Fintype.sum_prod_type,Matrix.one_apply,Finset.sum_mul,mul_assoc]

theorem literal_complete_word_intertwines_every_golden_history_depth
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool) (w : ℂ) (k n : ℕ) (a p : ℝ) (x : ι → ℂ) :
    (recordedWord (suffixLift (X:=Word n) U) (suffixLift (X:=Word n) (blankPhase z w))
      (suffixLift (X:=Word n) (diagonalPhase χ w)) k).mulVec
        (historyCylinderInclusion a p n x)=
          historyCylinderInclusion a p n ((fullWord U z χ w k).mulVec x) := by
  rw [complete_recorded_word_suffix_natural,every_golden_history_depth_intertwines_complete_operator,
    full_word_is_recorded_word]

theorem complete_fixed_calibration_rate_uniform_at_every_history_depth (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he : rejectedWeight χ (fun i => U i z)≤11/16) :
    ∃ γ : ℂ, Complex.normSq γ=1 ∧
      ∀ n, vectorWeight (historyCylinderInclusion a p n
        (fun i => γ*alignedAcceptedVector χ (fun j => U j z) i))=1 ∧
        ∀ k, vectorWeight (historyCylinderInclusion a p n
          (unspunColumn U z χ (fastGoldenPhase a p) (k+2))-
            historyCylinderInclusion a p n
              (fun i => γ*alignedAcceptedVector χ (fun j => U j z) i))≤(1/8)*(1/16)^k := by
  obtain ⟨γ,hγ,hunit,hbound⟩ := all_size_complete_fixed_calibration_rate a p U z χ ha hp hp0 hU he
  refine ⟨γ,hγ,?_⟩
  intro n
  constructor
  · rw [every_golden_history_depth_preserves_complete_weight a p ha hp,hunit]
  · intro k
    rw [← all_golden_history_inclusions_subtract,every_golden_history_depth_preserves_complete_weight a p ha hp]
    exact hbound k

theorem actual_all_scene_fixed_calibrations_and_all_real_readouts (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) :
    ∃ γ : Fin 33 → ℂ, ∀ v, Complex.normSq (γ v)=1 ∧
      ∀ (P : Matrix (CompleteSeedCarrier 4 5 × Fin 2) (CompleteSeedCarrier 4 5 × Fin 2) ℝ),
        P.transpose=P → P*P=P → ∀ k,
          (realQuadraticReading P (fullRealVector (unspunColumn
            (routedGoldenSeed a p 4 5) (completeBlank 4 5)
              (codeValidity 4 5 (sceneAcceptedCodes v)) (fastGoldenPhase a p) (k+2)))-
            realQuadraticReading P (fullRealVector (fun i => γ v*alignedAcceptedVector
              (codeValidity 4 5 (sceneAcceptedCodes v))
                (fun j => routedGoldenSeed a p 4 5 j (completeBlank 4 5)) i)))^2≤(1/2)*(1/16)^k := by
  have h (v : Fin 33) := full_real_fixed_limit_all_projector_readings a p
    (routedGoldenSeed a p 4 5) (completeBlank 4 5) (codeValidity 4 5 (sceneAcceptedCodes v))
      ha hp hp0 (actual_retained_routed_seed_unitary a p ha hp 4 5)
        (actual_scene_seed_is_in_fixed_limit_basin a p ha hp hp0 v)
  choose γ hγ hread using h
  exact ⟨γ,fun v => ⟨hγ v,hread v⟩⟩

def actualSceneUnspunColumn (v : Fin 33) (k : ℕ) : CompleteSeedCarrier 4 5 → ℂ :=
  unspunColumn (routedGoldenSeed (Real.sqrt D0.primitiveRoot) D0.primitiveRoot 4 5)
    (completeBlank 4 5) (codeValidity 4 5 (sceneAcceptedCodes v))
      (fastGoldenPhase (Real.sqrt D0.primitiveRoot) D0.primitiveRoot) (k+2)

def actualSceneAlignedSeed (v : Fin 33) : CompleteSeedCarrier 4 5 → ℂ :=
  alignedAcceptedVector (codeValidity 4 5 (sceneAcceptedCodes v))
    (fun i => routedGoldenSeed (Real.sqrt D0.primitiveRoot) D0.primitiveRoot 4 5 i (completeBlank 4 5))

theorem literal_p0_all_scene_readouts_have_one_fixed_target_family :
    ∃ γ : Fin 33 → ℂ, ∀ v, Complex.normSq (γ v)=1 ∧
      ∀ (P : Matrix (CompleteSeedCarrier 4 5 × Fin 2) (CompleteSeedCarrier 4 5 × Fin 2) ℝ),
        P.transpose=P → P*P=P → ∀ k,
          (realQuadraticReading P (fullRealVector (actualSceneUnspunColumn v k))-
            realQuadraticReading P (fullRealVector (fun i => γ v*actualSceneAlignedSeed v i)))^2≤
              (1/2)*(1/16)^k := by
  exact actual_all_scene_fixed_calibrations_and_all_real_readouts (Real.sqrt D0.primitiveRoot)
    D0.primitiveRoot (Real.sq_sqrt (le_of_lt D0.Representation.GoldenOrderInterferometer.primitive_positive))
      D0.primitive_root_satisfies D0.Representation.GoldenOrderInterferometer.primitive_positive

end
end D0.Research.GoldenFixedCalibration

namespace D0.Research.GoldenFixedCalibration
noncomputable section
open Matrix Complex D0.Research.GoldenCoherentAmplification
open D0.Representation.GoldenOrderInterferometer
open scoped Kronecker
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

theorem full_real_scalar_phase_is_global_pointer_rotation (c : ℂ) (x : ι → ℂ) :
    fullRealVector (fun i => c*x i)=
      ((1 : Matrix ι ι ℝ) ⊗ₖ phaseRealMatrix c).mulVec (fullRealVector x) := by
  funext s
  rcases s with ⟨i,b⟩
  fin_cases b <;> simp [fullRealVector,phaseRealMatrix,Matrix.mulVec,dotProduct,
    Matrix.kroneckerMap_apply,Fintype.sum_prod_type,Fin.sum_univ_two,
    Complex.mul_re,Complex.mul_im,Matrix.one_apply,Finset.sum_add_distrib,Finset.sum_neg_distrib]
  all_goals ring

theorem actual_complete_unspin_is_one_owned_pointer_word (a p : ℝ) (ha : a^2=p)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool) (k : ℕ) :
    fullRealVector (unspunColumn U z χ (fastGoldenPhase a p) k)=
      ((1 : Matrix ι ι ℝ) ⊗ₖ ((gate a p)^(16*k)).transpose).mulVec
        (fullRealVector (fun i => fullWord U z χ (fastGoldenPhase a p) k i z)) := by
  unfold unspunColumn
  rw [full_real_scalar_phase_is_global_pointer_rotation,
    actual_global_unspin_is_owned_golden_word a p ha]

end
end D0.Research.GoldenFixedCalibration


namespace D0.Research.GoldenProgramCompilation
noncomputable section
open Matrix Filter Topology

def G (a p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  D0.Representation.GoldenOrderInterferometer.gate a p

theorem golden_square_formula (a p : ℝ) :
    G a p ^ 2 = !![a^2-p^2,-2*a*p;2*a*p,a^2-p^2] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [G, D0.Representation.GoldenOrderInterferometer.gate,
      pow_two, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

theorem native_root_interval (p : ℝ) (hp : p+p^2=1) (hp0 : 0<p) :
    1/2<p ∧ p<1 := by
  constructor
  · by_contra h
    have hh : p≤1/2 := le_of_not_gt h
    nlinarith [sq_nonneg (p-1/2)]
  · by_contra h
    have hh : 1≤p := le_of_not_gt h
    nlinarith [sq_nonneg (p-1)]

theorem owned_golden_square_changes_basis (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) :
    (G a p ^ 2) 0 0 ≠ 0 ∧ (G a p ^ 2) 1 0 ≠ 0 ∧
    (G a p ^ 2) 0 1 ≠ 0 ∧ (G a p ^ 2) 1 1 ≠ 0 := by
  have hi := native_root_interval p hp hp0
  have ha0 : a≠0 := by intro h; simp [h] at ha; linarith
  rw [golden_square_formula]
  change a^2-p^2≠0 ∧ 2*a*p≠0 ∧ -2*a*p≠0 ∧ a^2-p^2≠0
  have hd : a^2-p^2≠0 := by intro h; nlinarith
  have hm : 2*a*p≠0 := mul_ne_zero (mul_ne_zero (by norm_num) ha0) (ne_of_gt hp0)
  exact ⟨hd,hm,by simpa using neg_ne_zero.mpr hm,hd⟩

theorem literal_p0_square_changes_basis :
    let p := D0.primitiveRoot
    let a := Real.sqrt p
    (G a p ^ 2) 0 0 ≠ 0 ∧ (G a p ^ 2) 1 0 ≠ 0 ∧
    (G a p ^ 2) 0 1 ≠ 0 ∧ (G a p ^ 2) 1 1 ≠ 0 := by
  dsimp
  exact owned_golden_square_changes_basis _ _
    (Real.sq_sqrt (le_of_lt D0.Representation.GoldenOrderInterferometer.primitive_positive))
    D0.primitive_root_satisfies D0.Representation.GoldenOrderInterferometer.primitive_positive

def copy : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1,0,0,0;0,1,0,0;0,0,0,1;0,0,1,0]
def recordGate (a p : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![a,-p,0,0;p,a,0,0;0,0,a,-p;0,0,p,a]

theorem retained_copy_is_involutive : copy * copy = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [copy, Matrix.mul_apply, Fin.sum_univ_succ]

theorem forward_copy_echo_formula (a p : ℝ) :
    copy * recordGate a p * copy =
      !![a,-p,0,0;p,a,0,0;0,0,a,p;0,0,-p,a] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [copy, recordGate, Matrix.mul_apply, Fin.sum_univ_succ]

theorem forward_copy_echo_retains_one_and_inverts_pointer (a p u v : ℝ) :
    (copy * recordGate a p * copy).mulVec ![0,0,u,v] =
      ![0,0,((G a p).transpose.mulVec ![u,v]) 0,
        ((G a p).transpose.mulVec ![u,v]) 1] := by
  rw [forward_copy_echo_formula]
  ext i
  fin_cases i <;>
    simp [G, D0.Representation.GoldenOrderInterferometer.gate,
      Matrix.mulVec, dotProduct, Fin.sum_univ_succ]

section Stability
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

def evalWord : List (E →L[ℝ] E) → (E →L[ℝ] E)
  | [] => ContinuousLinearMap.id ℝ E
  | U::w => U.comp (evalWord w)

theorem eval_empty (x : E) : evalWord [] x=x := rfl
theorem eval_cons (U : E →L[ℝ] E) (w : List (E →L[ℝ] E)) (x : E) :
    evalWord (U::w) x=U (evalWord w x) := rfl

theorem complete_word_isometry (w : List (E →L[ℝ] E))
    (hw : ∀ U∈w, ∀ x, ‖U x‖=‖x‖) (x : E) : ‖evalWord w x‖=‖x‖ := by
  induction w with
  | nil => rfl
  | cons U w ih =>
    rw [eval_cons,hw U (by simp),ih (by intro V h; exact hw V (by simp [h]))]

theorem one_compiled_step_error (U V : E →L[ℝ] E) (δ : ℝ)
    (hU : ∀ x, ‖U x‖=‖x‖) (hUV : ‖U-V‖≤δ) (x y : E) :
    ‖U x-V y‖≤‖x-y‖+δ*‖y‖ := by
  have he : U x-V y=U (x-y)+(U-V) y := by simp
  rw [he]
  calc
    ‖U (x-y)+(U-V) y‖≤‖U (x-y)‖+‖(U-V) y‖ := norm_add_le _ _
    _ ≤ ‖x-y‖+δ*‖y‖ := by
      rw [hU]
      exact add_le_add_right ((ContinuousLinearMap.le_opNorm _ y).trans
        (mul_le_mul_of_nonneg_right hUV (norm_nonneg y))) _

theorem whole_compiled_word_error (w v : List (E →L[ℝ] E)) (δ : ℝ)
    (hw : ∀ U∈w, ∀ x, ‖U x‖=‖x‖)
    (hv : ∀ V∈v, ∀ x, ‖V x‖=‖x‖)
    (hpaired : List.Forall₂ (fun U V => ‖U-V‖≤δ) w v) (x : E) :
    ‖evalWord w x-evalWord v x‖≤(w.length : ℝ)*δ*‖x‖ := by
  induction hpaired with
  | nil => simp [evalWord]
  | @cons U V w v huv htail ih =>
    have hwt : ∀ A∈w, ∀ y, ‖A y‖=‖y‖ := by intro A h; exact hw A (by simp [h])
    have hvt : ∀ A∈v, ∀ y, ‖A y‖=‖y‖ := by intro A h; exact hv A (by simp [h])
    have hi := ih hwt hvt
    have hs := one_compiled_step_error U V δ (hw U (by simp)) huv
      (evalWord w x) (evalWord v x)
    rw [complete_word_isometry v hvt x] at hs
    simp only [eval_cons,List.length_cons,Nat.cast_add,Nat.cast_one]
    linarith

theorem compiled_word_preserves_every_record_norm (v : List (E →L[ℝ] E))
    (hv : ∀ V∈v, ∀ x, ‖V x‖=‖x‖) (x : E) :
    ‖evalWord v x‖=‖x‖ := complete_word_isometry v hv x

theorem calibrated_complete_state_error (x t : E) (C A : E →L[ℝ] E)
    (ε δ : ℝ) (hC : ∀ y, ‖C y‖=‖y‖) (hx : ‖x‖=1)
    (hprep : ‖x-t‖≤ε) (hcompile : ‖A-C‖≤δ) :
    ‖A x-C t‖≤ε+δ := by
  have hi : A x-C t=C (x-t)+(A-C) x := by simp
  rw [hi]
  calc
    ‖C (x-t)+(A-C) x‖≤‖C (x-t)‖+‖(A-C) x‖ := norm_add_le _ _
    _ ≤ ε+δ := by
      rw [hC]
      have hb := (ContinuousLinearMap.le_opNorm (A-C) x).trans
        (mul_le_mul_of_nonneg_right hcompile (norm_nonneg x))
      rw [hx,mul_one] at hb
      exact add_le_add hprep hb
end Stability

section Budget
def resolution (p : ℝ) (m : ℕ) : ℝ := (1+p)^(5*m)
def precision (m : ℕ) : ℝ := (1/16 : ℝ)^m

theorem native_fifth_resolution_scale (p : ℝ) (hp : p+p^2=1) :
    (1+p)^5=8+5*p := by
  linear_combination (p^3+4*p^2+7*p+7)*hp

theorem native_fifth_scale_separates_cost_and_accuracy (p : ℝ)
    (hp : p+p^2=1) (hp0 : 0<p) : 9<(1+p)^5 ∧ (1+p)^5<16 := by
  rw [native_fifth_resolution_scale p hp]
  have hi := native_root_interval p hp hp0
  constructor <;> linarith

theorem precision_has_native_resolution_bound (p : ℝ)
    (hp : p+p^2=1) (hp0 : 0<p) (m : ℕ) :
    precision m≤(resolution p m)⁻¹ := by
  have h := native_fifth_scale_separates_cost_and_accuracy p hp hp0
  have hp1 : 0<1+p := by linarith
  unfold precision resolution
  rw [pow_mul]
  rw [← inv_pow]
  apply pow_le_pow_left₀ (by norm_num)
  simpa only [one_div] using
    (inv_le_inv₀ (by norm_num) (pow_pos hp1 5)).2 (le_of_lt h.2)

theorem expanded_compiler_cost_div_resolution_tends_zero (p A : ℝ) (c : ℕ)
    (hp : p+p^2=1) (hp0 : 0<p) :
    Tendsto (fun m : ℕ => A*(m : ℝ)^c*9^m/resolution p m) atTop (𝓝 0) := by
  have hs := native_fifth_scale_separates_cost_and_accuracy p hp hp0
  have hbase : 0<(1+p)^5 := by linarith
  have hq0 : 0≤9/(1+p)^5 := le_of_lt (div_pos (by norm_num) hbase)
  have hq1 : 9/(1+p)^5<1 := (div_lt_one hbase).2 hs.1
  have h := tendsto_pow_const_mul_const_pow_of_lt_one c hq0 hq1
  have hA : Tendsto (fun m : ℕ => A*((m : ℝ)^c*(9/(1+p)^5)^m))
      atTop (𝓝 (A*0)) := tendsto_const_nhds.mul h
  convert hA using 1
  · ext m
    simp only [resolution,pow_mul,div_pow]
    ring
  · simp

theorem every_fixed_compiler_polynomial_eventually_fits (p A : ℝ) (c : ℕ)
    (hp : p+p^2=1) (hp0 : 0<p) :
    ∀ᶠ m : ℕ in atTop, A*(m : ℝ)^c*9^m≤resolution p m := by
  have h := expanded_compiler_cost_div_resolution_tends_zero p A c hp hp0
  have he := h.eventually (gt_mem_nhds (show (0 : ℝ)<1 by norm_num))
  filter_upwards [he] with m hm
  have hpos : 0<resolution p m := pow_pos (by linarith) _
  exact le_of_lt ((div_lt_one hpos).1 hm)

theorem actual_owned_phi_is_one_plus_primitive : D0.phi=1+D0.primitiveRoot := by
  unfold D0.phi D0.primitiveRoot
  ring

theorem actual_resolution_is_owned_phi_level (m : ℕ) :
    resolution D0.primitiveRoot m=D0.phi^(5*m) := by
  simp [resolution,actual_owned_phi_is_one_plus_primitive]

theorem actual_owned_code_scale_and_accuracy (m : ℕ) :
    precision m≤(D0.phi^(5*m))⁻¹ := by
  rw [← actual_resolution_is_owned_phi_level]
  exact precision_has_native_resolution_bound D0.primitiveRoot D0.primitive_root_satisfies
    D0.Representation.GoldenOrderInterferometer.primitive_positive m

theorem actual_expanded_compiler_cost_eventually_fits_owned_phi (A : ℝ) (c : ℕ) :
    ∀ᶠ m : ℕ in atTop, A*(m : ℝ)^c*9^m≤D0.phi^(5*m) := by
  simpa only [actual_resolution_is_owned_phi_level] using
    every_fixed_compiler_polynomial_eventually_fits D0.primitiveRoot A c D0.primitive_root_satisfies
      D0.Representation.GoldenOrderInterferometer.primitive_positive
end Budget
end
end D0.Research.GoldenProgramCompilation


namespace D0.Research.GoldenProgramCompilation
noncomputable section
open Matrix Complex Filter Topology
open scoped Kronecker
open D0.Research.GoldenCoherentAmplification D0.Research.GoldenFixedCalibration
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def successPhase (b : ℂ) : ℂ := b/(‖b‖ : ℂ)
def successCorrection (b : ℂ) : ℂ := star (successPhase b)

theorem success_phase_unit (b : ℂ) (hb : b≠0) :
    Complex.normSq (successPhase b)=1 := by
  have hn : ‖b‖≠0 := norm_ne_zero_iff.mpr hb
  unfold successPhase
  rw [Complex.normSq_div,Complex.normSq_ofReal,← pow_two,Complex.normSq_eq_norm_sq]
  exact div_self (pow_ne_zero 2 hn)

theorem success_correction_unit (b : ℂ) (hb : b≠0) :
    Complex.normSq (successCorrection b)=1 := by
  simpa [successCorrection,Complex.star_def,Complex.normSq_conj] using success_phase_unit b hb

theorem success_phase_times_own_norm (b : ℂ) (hb : b≠0) :
    (‖b‖ : ℂ)*successPhase b=b := by
  have hn : (‖b‖ : ℂ)≠0 := by exact_mod_cast norm_ne_zero_iff.mpr hb
  unfold successPhase
  field_simp

theorem success_correction_times_phase (b : ℂ) (hb : b≠0) :
    successCorrection b*successPhase b=1 :=
  complete_unit_phase_star_product _ (success_phase_unit b hb)

theorem success_correction_makes_own_success_positive (b : ℂ) (hb : b≠0) :
    successCorrection b*b=(‖b‖ : ℂ) := by
  calc
    successCorrection b*b=successCorrection b*((‖b‖ : ℂ)*successPhase b) :=
      congrArg (fun z : ℂ => successCorrection b*z) (success_phase_times_own_norm b hb).symm
    _ =
      (‖b‖ : ℂ)*(successCorrection b*successPhase b) := by ring
    _ = (‖b‖ : ℂ) := by rw [success_correction_times_phase b hb,mul_one]

theorem success_correction_is_unique (b c : ℂ) (hb : b≠0)
    (hc : c*b=(‖b‖ : ℂ)) : c=successCorrection b := by
  apply mul_right_cancel₀ hb
  rw [hc,success_correction_makes_own_success_positive b hb]

theorem success_distance_from_unit_phase (b : ℂ) (hb : b≠0) :
    Complex.normSq (b-successPhase b)=(‖b‖-1)^2 := by
  have he : b-successPhase b=((‖b‖ : ℂ)-1)*successPhase b := by
    rw [sub_mul,one_mul,success_phase_times_own_norm b hb]
  rw [he,Complex.normSq_mul,success_phase_unit b hb,mul_one]
  rw [← Complex.ofReal_one,← Complex.ofReal_sub,Complex.normSq_ofReal]
  ring

theorem complete_calibrated_distance_identity (b : ℂ) (hb : b≠0)
    (x t : ι → ℂ) :
    vectorWeight (fun i => successCorrection b*x i-t i)=
      vectorWeight (fun i => x i-successPhase b*t i) := by
  have he : (fun i => successCorrection b*x i-t i)=
      (fun i => successCorrection b*(x i-successPhase b*t i)) := by
    funext i
    rw [mul_sub,← mul_assoc,success_correction_times_phase b hb,one_mul]
  rw [he,vector_weight_scalar_factor,success_correction_unit b hb,one_mul]

theorem balanced_success_ne_zero (b : ℂ) (e : ℝ)
    (hbalance : Complex.normSq b+e=1) (he : e<1) : b≠0 := by
  intro h
  simp [h] at hbalance
  linarith

theorem balanced_success_radial_error (b : ℂ) (e : ℝ)
    (hbalance : Complex.normSq b+e=1) (he0 : 0≤e) :
    (‖b‖-1)^2≤e := by
  rw [Complex.normSq_eq_norm_sq] at hbalance
  have hn0 := norm_nonneg b
  have hn1 : ‖b‖≤1 := by nlinarith
  nlinarith [mul_nonneg hn0 (sub_nonneg.mpr hn1)]

def calibratedColumn (a p : ℝ) (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (k : ℕ) : ι → ℂ :=
  fun i => successCorrection (normalizedSuccessScalar a p U z χ k)*
    unspunColumn U z χ (fastGoldenPhase a p) k i

theorem actual_full_calibrated_column_fixed_target_error (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (hs : 0<acceptedWeight χ (fun i => U i z)) (k : ℕ)
    (he : rejectedWeight χ (fun i => fullWord U z χ (fastGoldenPhase a p) k i z)<1) :
    vectorWeight (calibratedColumn a p U z χ k-alignedAcceptedVector χ (fun i => U i z))≤
      2*rejectedWeight χ (fun i => fullWord U z χ (fastGoldenPhase a p) k i z) := by
  let b := normalizedSuccessScalar a p U z χ k
  have hbalance := normalized_success_scalar_full_balance a p U z χ ha hp hU hs k
  have hb : b≠0 := balanced_success_ne_zero b _ hbalance he
  change vectorWeight (fun i => successCorrection b*
    unspunColumn U z χ (fastGoldenPhase a p) k i-alignedAcceptedVector χ (fun i => U i z) i)≤_
  rw [complete_calibrated_distance_identity b hb,
    all_size_complete_fixed_target_distance_identity a p U z χ ha hp hU hs k,
    success_distance_from_unit_phase b hb]
  have h := balanced_success_radial_error b _ hbalance (rejected_weight_nonnegative χ _)
  linarith

theorem actual_full_calibrated_column_has_complete_unit_weight (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (hs : 0<acceptedWeight χ (fun i => U i z)) (k : ℕ)
    (he : rejectedWeight χ (fun i => fullWord U z χ (fastGoldenPhase a p) k i z)<1) :
    vectorWeight (calibratedColumn a p U z χ k)=1 := by
  have hb := balanced_success_ne_zero _ _
    (normalized_success_scalar_full_balance a p U z χ ha hp hU hs k) he
  unfold calibratedColumn
  rw [vector_weight_scalar_factor,success_correction_unit _ hb,one_mul,
    all_unspun_full_columns_normalized U z χ _ k hU (fast_golden_phase_normSq a p ha hp)]

theorem native_full_calibrated_column_rate (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he0 : rejectedWeight χ (fun i => U i z)≤11/16) (k : ℕ) :
    vectorWeight (calibratedColumn a p U z χ (k+2))=1 ∧
    vectorWeight (calibratedColumn a p U z χ (k+2)-alignedAcceptedVector χ (fun i => U i z))≤
      (1/16)^k/5 := by
  have hs := actual_initial_accepted_mass_positive U z χ hU.1 he0
  have hr := fast_parameter_native_bounds p hp hp0
  have hf := (fast_all_full_failure_rate _ _ (le_of_lt hr.1) (le_of_lt hr.2)
    (rejected_weight_nonnegative χ (fun i => U i z)) he0 k).2.2
  rw [← actual_full_word_fast_failure a p U z χ ha hp hU] at hf
  have hpow : (1/16 : ℝ)^k≤1 := pow_le_one₀ (by norm_num) (by norm_num)
  have he : rejectedWeight χ (fun i => fullWord U z χ (fastGoldenPhase a p) (k+2) i z)<1 := by
    linarith
  refine ⟨actual_full_calibrated_column_has_complete_unit_weight a p U z χ ha hp hU hs (k+2) he,?_⟩
  have hh := actual_full_calibrated_column_fixed_target_error a p U z χ ha hp hU hs (k+2) he
  linarith

theorem calibration_is_one_complete_pointer_operation (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool) (k : ℕ) :
    fullRealVector (calibratedColumn a p U z χ k)=
      ((1 : Matrix ι ι ℝ) ⊗ₖ phaseRealMatrix
        (successCorrection (normalizedSuccessScalar a p U z χ k))).mulVec
          (fullRealVector (unspunColumn U z χ (fastGoldenPhase a p) k)) := by
  exact full_real_scalar_phase_is_global_pointer_rotation _ _

theorem all_33_literal_scene_calibrated_columns_have_fixed_real_targets (k : ℕ) :
    ∀ v : Fin 33,
      vectorWeight (calibratedColumn (Real.sqrt D0.primitiveRoot) D0.primitiveRoot
        (routedGoldenSeed (Real.sqrt D0.primitiveRoot) D0.primitiveRoot 4 5)
        (completeBlank 4 5) (codeValidity 4 5 (sceneAcceptedCodes v)) (k+2))=1 ∧
      vectorWeight (calibratedColumn (Real.sqrt D0.primitiveRoot) D0.primitiveRoot
        (routedGoldenSeed (Real.sqrt D0.primitiveRoot) D0.primitiveRoot 4 5)
        (completeBlank 4 5) (codeValidity 4 5 (sceneAcceptedCodes v)) (k+2)-
        actualSceneAlignedSeed v)≤(1/16)^k/5 := by
  intro v
  have hp0 := D0.Representation.GoldenOrderInterferometer.primitive_positive
  have ha := Real.sq_sqrt (le_of_lt hp0)
  have hp := D0.primitive_root_satisfies
  exact native_full_calibrated_column_rate _ _ _ _ _ ha hp hp0
    (actual_retained_routed_seed_unitary _ _ ha hp 4 5)
    (actual_scene_seed_is_in_fixed_limit_basin _ _ ha hp hp0 v) k

end
end D0.Research.GoldenProgramCompilation

set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false

namespace D0.Research.GoldenProgramCompilation
noncomputable section
open Matrix Complex Filter Topology
open scoped Kronecker
open D0.Research.GoldenCoherentAmplification D0.Research.GoldenFixedCalibration
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def realHilbert (x : ι → ℝ) : EuclideanSpace ℝ ι := WithLp.toLp 2 x
def matrixOperator (A : Matrix ι ι ℝ) : EuclideanSpace ℝ ι →L[ℝ] EuclideanSpace ℝ ι :=
  (A.toLpLin 2 2).toContinuousLinearMap

theorem real_hilbert_norm_sq_is_complete_weight (x : ι → ℝ) :
    ‖realHilbert x‖^2=realVectorWeight x := by
  exact EuclideanSpace.real_norm_sq_eq _

theorem real_hilbert_subtracts (x y : ι → ℝ) :
    realHilbert (x-y)=realHilbert x-realHilbert y := rfl

theorem matrix_operator_acts_on_every_complete_coordinate (A : Matrix ι ι ℝ) (x : ι → ℝ) :
    matrixOperator A (realHilbert x)=realHilbert (A.mulVec x) := rfl

theorem whole_real_orthogonal_operator_preserves_weight (A : Matrix ι ι ℝ)
    (hA : A.transpose*A=1) (x : ι → ℝ) :
    realVectorWeight (A.mulVec x)=realVectorWeight x := by
  have h := dotProduct_transpose_mulVec A x (A.mulVec x)
  rw [mulVec_mulVec,hA,one_mulVec] at h
  rw [real_complete_weight_is_self_dot,real_complete_weight_is_self_dot]
  exact h.symm

theorem whole_real_orthogonal_operator_is_hilbert_isometry (A : Matrix ι ι ℝ)
    (hA : A.transpose*A=1) (x : EuclideanSpace ℝ ι) :
    ‖matrixOperator A x‖=‖x‖ := by
  have h := whole_real_orthogonal_operator_preserves_weight A hA (WithLp.ofLp x)
  have he : realHilbert (WithLp.ofLp x)=x := rfl
  rw [← real_hilbert_norm_sq_is_complete_weight,
    ← real_hilbert_norm_sq_is_complete_weight,
    ← matrix_operator_acts_on_every_complete_coordinate,he] at h
  exact (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp h

theorem faithful_full_complex_norm_is_hilbert_norm_sq (x : ι → ℂ) :
    ‖realHilbert (fullRealVector x)‖^2=vectorWeight x := by
  rw [real_hilbert_norm_sq_is_complete_weight,full_real_encoding_retains_complete_weight]

def calibratedFullMatrix (a p : ℝ) (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (k : ℕ) : Matrix ι ι ℂ :=
  (successCorrection (normalizedSuccessScalar a p U z χ k)*
    (star (fastGoldenPhase a p))^(2*k)) • fullWord U z χ (fastGoldenPhase a p) k

theorem complete_calibrated_matrix_column_is_actual_calibrated_state (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool) (k : ℕ) :
    (fun i => calibratedFullMatrix a p U z χ k i z)=calibratedColumn a p U z χ k := by
  funext i
  simp only [calibratedFullMatrix,calibratedColumn,unspunColumn,Matrix.smul_apply,
    smul_eq_mul,mul_assoc]

theorem complete_calibrated_matrix_is_unitary (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (hb : normalizedSuccessScalar a p U z χ k≠0) :
    (calibratedFullMatrix a p U z χ k).conjTranspose*calibratedFullMatrix a p U z χ k=1 ∧
      calibratedFullMatrix a p U z χ k*(calibratedFullMatrix a p U z χ k).conjTranspose=1 := by
  let c := successCorrection (normalizedSuccessScalar a p U z χ k)*
    (star (fastGoldenPhase a p))^(2*k)
  have hc : Complex.normSq c=1 := by
    simp [c,Complex.normSq_mul,success_correction_unit _ hb,map_pow,
      Complex.star_def,Complex.normSq_conj,fast_golden_phase_normSq a p ha hp]
  have h := all_full_words_unitary U z χ (fastGoldenPhase a p) hU
    (fast_golden_phase_normSq a p ha hp) k
  let V := fullWord U z χ (fastGoldenPhase a p) k
  change (c • V).conjTranspose*(c • V)=1 ∧ (c • V)*(c • V).conjTranspose=1
  have hc1 := complete_unit_phase_star_product c hc
  have hc2 : c*star c=1 := by simpa [mul_comm] using hc1
  simp only [Matrix.conjTranspose_smul,smul_mul_smul_comm,h.1,h.2,V]
  change (star c*c) • (1 : Matrix ι ι ℂ)=1 ∧
    (c*star c) • (1 : Matrix ι ι ℂ)=1
  exact ⟨(congrArg (fun z : ℂ => z • (1 : Matrix ι ι ℂ)) hc1).trans (one_smul ℂ _),
    (congrArg (fun z : ℂ => z • (1 : Matrix ι ι ℂ)) hc2).trans (one_smul ℂ _)⟩

theorem complete_calibrated_real_matrix_is_orthogonal (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (hb : normalizedSuccessScalar a p U z χ k≠0) :
    (fullRealMatrix (calibratedFullMatrix a p U z χ k)).transpose*
      fullRealMatrix (calibratedFullMatrix a p U z χ k)=1 := by
  exact (every_full_real_unitary_word_is_orthogonal _
    (complete_calibrated_matrix_is_unitary a p U z χ ha hp hU hb)).1

theorem actual_calibrated_matrix_blank_hilbert_action (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool) (k : ℕ) :
    matrixOperator (fullRealMatrix (calibratedFullMatrix a p U z χ k))
      (realHilbert (fullRealVector (blankVector z)))=
        realHilbert (fullRealVector (calibratedColumn a p U z χ k)) := by
  rw [matrix_operator_acts_on_every_complete_coordinate,← full_real_matrix_intertwines_every_state]
  congr 2
  rw [show (calibratedFullMatrix a p U z χ k).mulVec (blankVector z)=
      (fun i => calibratedFullMatrix a p U z χ k i z) by
    ext i; simp [blankVector,Matrix.mulVec,dotProduct,Pi.single_apply,
      Function.update_apply,apply_ite,eq_comm]]
  exact complete_calibrated_matrix_column_is_actual_calibrated_state a p U z χ k

theorem actual_blank_is_complete_unit_hilbert_state (z : ι) :
    ‖realHilbert (fullRealVector (blankVector z))‖=1 := by
  have h : vectorWeight (blankVector z)=1 := by
    have hb : blankVector z=(fun i => (1 : Matrix ι ι ℂ) i z) := by
      funext i
      by_cases hi : z=i
      · subst i; simp [blankVector]
      · simp [blankVector,Pi.single,Function.update,hi,Matrix.one_apply,Ne.symm hi]
    rw [hb]
    exact unitary_column_has_complete_weight (1 : Matrix ι ι ℂ) z (by simp)
  have hn := faithful_full_complex_norm_is_hilbert_norm_sq (blankVector z)
  rw [h] at hn
  have h0 := norm_nonneg (realHilbert (fullRealVector (blankVector z)))
  nlinarith

theorem actual_target_seed_is_complete_unit_hilbert_state (χ : ι → Bool) (x : ι → ℂ)
    (hs : 0<acceptedWeight χ x) :
    ‖realHilbert (fullRealVector (alignedAcceptedVector χ x))‖=1 := by
  have hn := faithful_full_complex_norm_is_hilbert_norm_sq (alignedAcceptedVector χ x)
  rw [aligned_accepted_vector_has_complete_weight χ x hs] at hn
  have h0 := norm_nonneg (realHilbert (fullRealVector (alignedAcceptedVector χ x)))
  nlinarith

section CombinedError
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

theorem complete_compilation_and_preparation_error (A U : E →L[ℝ] E) (z t : E)
    (ε δ : ℝ) (hz : ‖z‖=1) (hprep : ‖U z-t‖≤ε) (hcompile : ‖A-U‖≤δ) :
    ‖A z-t‖≤ε+δ := by
  have he : A z-t=(A-U) z+(U z-t) := by simp
  rw [he]
  have hc := (ContinuousLinearMap.le_opNorm (A-U) z).trans
    (mul_le_mul_of_nonneg_right hcompile (norm_nonneg z))
  rw [hz,mul_one] at hc
  exact (norm_add_le _ _).trans (by linarith)

theorem entire_literal_word_and_preparation_error (w v : List (E →L[ℝ] E))
    (z t : E) (ε δ : ℝ)
    (hw : ∀ U∈w, ∀ x, ‖U x‖=‖x‖)
    (hv : ∀ U∈v, ∀ x, ‖U x‖=‖x‖)
    (hpaired : List.Forall₂ (fun U V => ‖U-V‖≤δ) w v)
    (hz : ‖z‖=1) (hprep : ‖evalWord w z-t‖≤ε) :
    ‖evalWord v z-t‖≤ε+(w.length : ℝ)*δ := by
  have hc := whole_compiled_word_error w v δ hw hv hpaired z
  rw [hz,mul_one,norm_sub_rev] at hc
  have he : evalWord v z-t=(evalWord v z-evalWord w z)+(evalWord w z-t) := by abel
  rw [he]
  exact (norm_add_le _ _).trans (by linarith)

theorem finite_compilation_budget_can_be_shared (ε : ℝ) (N : ℕ)
    (hN : 0<N) : (N : ℝ)*(ε/(2*N))=ε/2 := by
  have hNr : (N : ℝ)≠0 := by exact_mod_cast Nat.ne_of_gt hN
  field_simp

theorem two_error_halves_give_fixed_complete_rate (x t : E) (ε : ℝ)
    (h : ‖x-t‖≤ε/2+ε/2) : ‖x-t‖≤ε := by linarith
end CombinedError

theorem actual_native_preparation_norm_fits_half_precision (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he0 : rejectedWeight χ (fun i => U i z)≤11/16) (m : ℕ) :
    ‖realHilbert (fullRealVector (calibratedColumn a p U z χ (2*m+2)))-
      realHilbert (fullRealVector (alignedAcceptedVector χ (fun i => U i z)))‖≤precision m/2 := by
  have h := (native_full_calibrated_column_rate a p U z χ ha hp hp0 hU he0 (2*m)).2
  have he := faithful_full_complex_norm_is_hilbert_norm_sq
    (calibratedColumn a p U z χ (2*m+2)-alignedAcceptedVector χ (fun i => U i z))
  have henc := full_real_encoding_subtracts (calibratedColumn a p U z χ (2*m+2))
    (alignedAcceptedVector χ (fun i => U i z))
  change fullRealVector (calibratedColumn a p U z χ (2*m+2)-
    alignedAcceptedVector χ (fun i => U i z))=_ at henc
  rw [henc] at he
  change ‖realHilbert (fullRealVector (calibratedColumn a p U z χ (2*m+2)))-
    realHilbert (fullRealVector (alignedAcceptedVector χ (fun i => U i z)))‖^2=
      vectorWeight (calibratedColumn a p U z χ (2*m+2)-
        alignedAcceptedVector χ (fun i => U i z)) at he
  have hpow : (1/16 : ℝ)^(2*m)=precision m^2 := by
    change (1/16 : ℝ)^(2*m)=((1/16 : ℝ)^m)^2
    rw [← pow_mul,Nat.mul_comm]
  rw [hpow,← he] at h
  have hp0' : 0≤precision m := pow_nonneg (by norm_num) _
  have hn := norm_nonneg (realHilbert (fullRealVector (calibratedColumn a p U z χ (2*m+2)))-
    realHilbert (fullRealVector (alignedAcceptedVector χ (fun i => U i z))))
  nlinarith

theorem actual_compiled_native_state_has_fixed_complete_rate (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he0 : rejectedWeight χ (fun i => U i z)≤11/16) (m : ℕ)
    (A : Matrix (ι × Fin 2) (ι × Fin 2) ℝ)
    (hcompile : ‖matrixOperator A-matrixOperator
      (fullRealMatrix (calibratedFullMatrix a p U z χ (2*m+2)))‖≤precision m/2) :
    ‖matrixOperator A (realHilbert (fullRealVector (blankVector z)))-
      realHilbert (fullRealVector (alignedAcceptedVector χ (fun i => U i z)))‖≤precision m := by
  have hp := actual_native_preparation_norm_fits_half_precision a p U z χ ha hp hp0 hU he0 m
  rw [← actual_calibrated_matrix_blank_hilbert_action] at hp
  have hh := complete_compilation_and_preparation_error (matrixOperator A)
    (matrixOperator (fullRealMatrix (calibratedFullMatrix a p U z χ (2*m+2))))
    _ _ (precision m/2) (precision m/2) (actual_blank_is_complete_unit_hilbert_state z) hp hcompile
  linarith

theorem every_real_projector_reading_follows_complete_compilation_rate
    (P : Matrix ι ι ℝ) (hs : P.transpose=P) (hp : P*P=P)
    (x t : ι → ℝ) (hx : realVectorWeight x=1) (ht : realVectorWeight t=1)
    (ε : ℝ) (he : 0≤ε) (herror : ‖realHilbert x-realHilbert t‖≤ε) :
    (realQuadraticReading P x-realQuadraticReading P t)^2≤4*ε^2 := by
  have h := all_real_projector_readout_squared_error P hs hp x t hx ht
  rw [← real_hilbert_norm_sq_is_complete_weight,real_hilbert_subtracts] at h
  have hn := norm_nonneg (realHilbert x-realHilbert t)
  nlinarith

theorem entire_refinement_preserves_compiled_error (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (n : ℕ) (x t : ι → ℂ) (ε : ℝ)
    (he : vectorWeight (x-t)≤ε) :
    vectorWeight (historyCylinderInclusion a p n x-historyCylinderInclusion a p n t)≤ε := by
  rw [← all_golden_history_inclusions_subtract,every_golden_history_depth_preserves_complete_weight a p ha hp]
  exact he

end
end D0.Research.GoldenProgramCompilation

set_option linter.unusedSectionVars false

namespace D0.Research.GoldenProgramCompilation
noncomputable section
open Filter Topology
open D0.Research.GoldenCoherentAmplification D0.Research.GoldenFixedCalibration

section EmbeddedWord
variable {E F : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]

theorem one_ancilla_retaining_compiled_step_error (J : E →L[ℝ] F)
    (U : E →L[ℝ] E) (V : F →L[ℝ] F) (δ : ℝ)
    (hV : ∀ y, ‖V y‖=‖y‖) (hcompile : ‖V.comp J-J.comp U‖≤δ)
    (x : E) (y : F) :
    ‖V y-J (U x)‖≤‖y-J x‖+δ*‖x‖ := by
  have he : V y-J (U x)=V (y-J x)+(V.comp J-J.comp U) x := by simp
  rw [he]
  calc
    ‖V (y-J x)+(V.comp J-J.comp U) x‖≤‖V (y-J x)‖+‖(V.comp J-J.comp U) x‖ := norm_add_le _ _
    _ ≤ ‖y-J x‖+δ*‖x‖ := by
      rw [hV]
      exact add_le_add_right ((ContinuousLinearMap.le_opNorm _ x).trans
        (mul_le_mul_of_nonneg_right hcompile (norm_nonneg x))) _

theorem whole_compiled_word_keeps_all_ancilla_leakage (J : E →L[ℝ] F)
    (w : List (E →L[ℝ] E)) (v : List (F →L[ℝ] F)) (δ : ℝ)
    (hw : ∀ U∈w, ∀ x, ‖U x‖=‖x‖)
    (hv : ∀ V∈v, ∀ y, ‖V y‖=‖y‖)
    (hpaired : List.Forall₂ (fun U V => ‖V.comp J-J.comp U‖≤δ) w v) (x : E) :
    ‖evalWord v (J x)-J (evalWord w x)‖≤(w.length : ℝ)*δ*‖x‖ := by
  induction hpaired with
  | nil => simp [evalWord]
  | @cons U V w v huv htail ih =>
    have hwt : ∀ A∈w, ∀ y, ‖A y‖=‖y‖ := by intro A h; exact hw A (by simp [h])
    have hvt : ∀ A∈v, ∀ y, ‖A y‖=‖y‖ := by intro A h; exact hv A (by simp [h])
    have hi := ih hwt hvt
    have hs := one_ancilla_retaining_compiled_step_error J U V δ
      (hv V (by simp)) huv (evalWord w x) (evalWord v (J x))
    rw [complete_word_isometry w hwt x] at hs
    simp only [eval_cons,List.length_cons,Nat.cast_add,Nat.cast_one]
    linarith

theorem whole_ancilla_retaining_program_has_complete_unit_norm (J : E →L[ℝ] F)
    (hJ : ∀ x, ‖J x‖=‖x‖) (v : List (F →L[ℝ] F))
    (hv : ∀ V∈v, ∀ y, ‖V y‖=‖y‖) (x : E) (hx : ‖x‖=1) :
    ‖evalWord v (J x)‖=1 := by
  rw [complete_word_isometry v hv,hJ,hx]

theorem ancilla_retaining_compiler_and_preparation_error (J : E →L[ℝ] F)
    (hJ : ∀ x, ‖J x‖=‖x‖) (U : E →L[ℝ] E) (A : F →L[ℝ] F)
    (z t : E) (ε δ : ℝ) (hz : ‖z‖=1) (hprep : ‖U z-t‖≤ε)
    (hcompile : ‖A.comp J-J.comp U‖≤δ) :
    ‖A (J z)-J t‖≤ε+δ := by
  have he : A (J z)-J t=(A.comp J-J.comp U) z+J (U z-t) := by simp
  rw [he]
  have hc := (ContinuousLinearMap.le_opNorm (A.comp J-J.comp U) z).trans
    (mul_le_mul_of_nonneg_right hcompile (norm_nonneg z))
  rw [hz,mul_one] at hc
  exact (norm_add_le _ _).trans (by rw [hJ]; linarith)

theorem literal_ancilla_retaining_word_and_preparation_error (J : E →L[ℝ] F)
    (hJ : ∀ x, ‖J x‖=‖x‖) (w : List (E →L[ℝ] E)) (v : List (F →L[ℝ] F))
    (z t : E) (ε δ : ℝ)
    (hw : ∀ U∈w, ∀ x, ‖U x‖=‖x‖)
    (hv : ∀ V∈v, ∀ y, ‖V y‖=‖y‖)
    (hpaired : List.Forall₂ (fun U V => ‖V.comp J-J.comp U‖≤δ) w v)
    (hz : ‖z‖=1) (hprep : ‖evalWord w z-t‖≤ε) :
    ‖evalWord v (J z)-J t‖≤ε+(w.length : ℝ)*δ := by
  have hc := whole_compiled_word_keeps_all_ancilla_leakage J w v δ hw hv hpaired z
  rw [hz,mul_one] at hc
  have he : evalWord v (J z)-J t=(evalWord v (J z)-J (evalWord w z))+J (evalWord w z-t) := by simp
  rw [he]
  exact (norm_add_le _ _).trans (by rw [hJ]; linarith)

theorem every_compilation_choice_with_vanishing_error_has_same_fixed_limit
    (x y : ℕ → F) (t : F) (ε : ℕ → ℝ)
    (hx : ∀ m, ‖x m-t‖≤ε m) (hy : ∀ m, ‖y m-t‖≤ε m)
    (hε : Tendsto ε atTop (𝓝 0)) :
    Tendsto x atTop (𝓝 t) ∧ Tendsto y atTop (𝓝 t) := by
  constructor
  · rw [tendsto_iff_norm_sub_tendsto_zero]
    exact squeeze_zero (fun m => norm_nonneg _) hx hε
  · rw [tendsto_iff_norm_sub_tendsto_zero]
    exact squeeze_zero (fun m => norm_nonneg _) hy hε
end EmbeddedWord

section NativeLift
variable {ι : Type*} [Fintype ι] [DecidableEq ι]
  {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]

theorem actual_ancilla_retaining_compiled_native_state_rate (a p : ℝ)
    (U : Matrix ι ι ℂ) (z : ι) (χ : ι → Bool)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (hU : U.conjTranspose*U=1 ∧ U*U.conjTranspose=1)
    (he0 : rejectedWeight χ (fun i => U i z)≤11/16) (m : ℕ)
    (J : EuclideanSpace ℝ (ι × Fin 2) →L[ℝ] F) (hJ : ∀ x, ‖J x‖=‖x‖)
    (A : F →L[ℝ] F)
    (hcompile : ‖A.comp J-J.comp (matrixOperator
      (fullRealMatrix (calibratedFullMatrix a p U z χ (2*m+2))))‖≤precision m/2) :
    ‖A (J (realHilbert (fullRealVector (blankVector z))))-
      J (realHilbert (fullRealVector (alignedAcceptedVector χ (fun i => U i z))))‖≤precision m := by
  have hh := actual_native_preparation_norm_fits_half_precision a p U z χ ha hp hp0 hU he0 m
  rw [← actual_calibrated_matrix_blank_hilbert_action] at hh
  have h := ancilla_retaining_compiler_and_preparation_error J hJ
    (matrixOperator (fullRealMatrix (calibratedFullMatrix a p U z χ (2*m+2)))) A
    _ _ (precision m/2) (precision m/2) (actual_blank_is_complete_unit_hilbert_state z) hh hcompile
  linarith

theorem native_compiled_precision_tends_zero : Tendsto precision atTop (𝓝 0) :=
  tendsto_pow_atTop_nhds_zero_of_lt_one (by norm_num : (0 : ℝ)≤1/16)
    (by norm_num : (1/16 : ℝ)<1)
end NativeLift
end
end D0.Research.GoldenProgramCompilation

set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false

namespace D0.Research.GoldenProgramCompilation
noncomputable section
open Matrix Complex Filter Topology
open scoped BigOperators Kronecker
open D0.Research.GoldenHistoryPreparation D0.Research.GoldenCoherentAmplification
open D0.Research.GoldenFixedCalibration

def commonRawRecord (a p : ℝ) (n m : ℕ) (w : Fin m → Word n) : ℝ :=
  if ∀ i, firstLabel (w i)=some false then ∏ i, amplitude a p (w i) else 0
def commonRecordMass (a p : ℝ) (n m : ℕ) : ℝ :=
  completeCodeMass a p n m (fun _ => false)
def commonRecord (a p : ℝ) (n m : ℕ) (w : Fin m → Word n) : ℝ :=
  commonRawRecord a p n m w/Real.sqrt (commonRecordMass a p n m)
def uniformCode (S : Finset (Fin m → Bool)) (b : Fin m → Bool) : ℝ :=
  if b∈S then (Real.sqrt (S.card : ℝ))⁻¹ else 0

theorem whole_common_raw_record_mass (a p : ℝ) (n m : ℕ) :
    (∑ w, commonRawRecord a p n m w^2)=commonRecordMass a p n m := by
  have he (w : Fin m → Word n) : commonRawRecord a p n m w^2=
      if ∀ i, firstLabel (w i)=some false then (∏ i,amplitude a p (w i))^2 else 0 := by
    by_cases hw : ∀ i, firstLabel (w i)=some false <;> simp [commonRawRecord,hw]
  simp_rw [he]
  exact complete_all_good_record_mass a p n m

theorem common_record_has_complete_unit_mass (a p : ℝ) (n m : ℕ)
    (hm : 0<commonRecordMass a p n m) :
    (∑ w, commonRecord a p n m w^2)=1 := by
  have ht := Real.sq_sqrt (le_of_lt hm)
  unfold commonRecord
  simp_rw [div_pow]
  rw [← Finset.sum_div,whole_common_raw_record_mass,ht]
  exact div_self (ne_of_gt hm)

theorem actual_common_record_mass_is_native_value (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    commonRecordMass a p 4 5=jointGoodWeight a p/32 := by
  unfold commonRecordMass
  rw [whole_fair_code_mass a p (show a^2+p^2=1 by linarith)]
  unfold jointGoodWeight
  ring

theorem actual_common_record_mass_positive (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) :
    0<commonRecordMass a p 4 5 := by
  rw [actual_common_record_mass_is_native_value a p ha hp]
  have h := golden_five_bit_good_bounds a p ha hp hp0
  exact div_pos (by linarith) (by norm_num)

theorem complete_retained_target_has_one_common_record_factor (a p : ℝ)
    (n m : ℕ) (S : Finset (Fin m → Bool)) (hs : 0<S.card)
    (hm : 0<commonRecordMass a p n m)
    (w : Fin m → Word n) (b : Fin m → Bool) :
    alignedAcceptedVector (codeValidity n m S)
      (fun s => routedGoldenSeed a p n m s (completeBlank n m)) (fun i => (w i,b i))=
        ((uniformCode S b*commonRecord a p n m w : ℝ) : ℂ) := by
  by_cases hw : ∀ i,firstLabel (w i)=some false
  · by_cases hb : b∈S
    · have hs0 : 0<(S.card : ℝ) := by exact_mod_cast hs
      have hsqrt : Real.sqrt (S.card : ℝ)≠0 := ne_of_gt (Real.sqrt_pos.mpr hs0)
      have hmsqrt : Real.sqrt (commonRecordMass a p n m)≠0 := ne_of_gt (Real.sqrt_pos.mpr hm)
      unfold alignedAcceptedVector
      rw [complete_retained_seed_valid_mass]
      change (if codeValidity n m S (fun i => (w i,b i)) then
        routedGoldenSeed a p n m (fun i => (w i,b i)) (completeBlank n m)/
          ((Real.sqrt ((S.card : ℝ)*commonRecordMass a p n m) : ℝ) : ℂ) else 0)=_
      simp [codeValidity,hw,hb]
      rw [actual_routed_seed_successful_amplitude a p n m b w hw]
      simp [uniformCode,hb,commonRecord,commonRawRecord,hw,
        Complex.ofReal_mul,Complex.ofReal_inv,Complex.ofReal_div]
      ring
    · simp [alignedAcceptedVector,codeValidity,hb,uniformCode]
  · simp [alignedAcceptedVector,codeValidity,hw,uniformCode,commonRecord,commonRawRecord]

theorem every_actual_scene_target_has_same_retained_record (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) (v : Fin 33)
    (w : Fin 5 → Word 4) (b : Fin 5 → Bool) :
    alignedAcceptedVector (codeValidity 4 5 (sceneAcceptedCodes v))
      (fun s => routedGoldenSeed a p 4 5 s (completeBlank 4 5)) (fun i => (w i,b i))=
        ((uniformCode (sceneAcceptedCodes v) b*commonRecord a p 4 5 w : ℝ) : ℂ) := by
  have hd := actual_scene_accepted_codes_exact_degrees v
  have hs : 0<(sceneAcceptedCodes v).card := by rcases hd with h|h|h <;> omega
  exact complete_retained_target_has_one_common_record_factor a p 4 5 _ hs
    (actual_common_record_mass_positive a p ha hp hp0) w b

theorem actual_p0_common_retained_record_has_unit_mass :
    (∑ w, commonRecord (Real.sqrt D0.primitiveRoot) D0.primitiveRoot 4 5 w^2)=1 := by
  have hp0 := D0.Representation.GoldenOrderInterferometer.primitive_positive
  exact common_record_has_complete_unit_mass _ _ _ _
    (actual_common_record_mass_positive _ _ (Real.sq_sqrt (le_of_lt hp0))
      D0.primitive_root_satisfies hp0)

section Frame
variable {H V Ω : Type*} [Fintype H] [DecidableEq H] [Fintype V] [DecidableEq V]
  [Fintype Ω] [DecidableEq Ω]

def retainedFrame (J : Matrix H V ℝ) (η : Ω → ℝ) : Matrix (H × Ω) V ℝ :=
  fun s v => J s.1 v*η s.2

theorem complete_common_record_preserves_every_mixed_gram (J K : Matrix H V ℝ)
    (η : Ω → ℝ) (hη : ∑ w,η w^2=1) :
    (retainedFrame J η).transpose*retainedFrame K η=J.transpose*K := by
  ext u v
  simp only [Matrix.mul_apply,Matrix.transpose_apply,retainedFrame,Fintype.sum_prod_type]
  have he (h : H) : (∑ w : Ω,(J h u*η w)*(K h v*η w))=
      (J h u*K h v)*(∑ w : Ω,η w^2) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro w _
    ring
  simp_rw [he,hη,mul_one]

theorem complete_common_record_preserves_history_frame_isometry (J : Matrix H V ℝ)
    (η : Ω → ℝ) (hJ : J.transpose*J=1) (hη : ∑ w,η w^2=1) :
    (retainedFrame J η).transpose*retainedFrame J η=1 := by
  rw [complete_common_record_preserves_every_mixed_gram J J η hη,hJ]

theorem complete_reverse_acts_without_forgetting_common_record (R : Matrix H H ℝ)
    (J : Matrix H V ℝ) (η : Ω → ℝ) :
    (R ⊗ₖ (1 : Matrix Ω Ω ℝ))*retainedFrame J η=retainedFrame (R*J) η := by
  ext s v
  rcases s with ⟨h,w⟩
  simp [Matrix.mul_apply,retainedFrame,Matrix.kroneckerMap_apply,Fintype.sum_prod_type,
    Matrix.one_apply,Finset.sum_mul,mul_assoc]

theorem complete_common_record_preserves_every_history_return (R : Matrix H H ℝ)
    (J : Matrix H V ℝ) (η : Ω → ℝ) (hη : ∑ w,η w^2=1) :
    (retainedFrame J η).transpose*(R ⊗ₖ (1 : Matrix Ω Ω ℝ))*retainedFrame J η=
      J.transpose*R*J := by
  rw [Matrix.mul_assoc,complete_reverse_acts_without_forgetting_common_record,
    complete_common_record_preserves_every_mixed_gram J (R*J) η hη,Matrix.mul_assoc]

theorem native_common_record_preserves_owned_history_return (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p)
    (R : Matrix H H ℝ) (J : Matrix H V ℝ) :
    (retainedFrame J (commonRecord a p 4 5)).transpose*
      (R ⊗ₖ (1 : Matrix (Fin 5 → Word 4) (Fin 5 → Word 4) ℝ))*
        retainedFrame J (commonRecord a p 4 5)=J.transpose*R*J := by
  exact complete_common_record_preserves_every_history_return R J _
    (common_record_has_complete_unit_mass a p 4 5 (actual_common_record_mass_positive a p ha hp hp0))

end Frame
end
end D0.Research.GoldenProgramCompilation


namespace D0.Research.GoldenProgramCompilation
noncomputable section
open Filter Topology D0.Research.GoldenCoherentAmplification

theorem exact_full_preparation_cost_at_resolution_schedule (seed phase m : ℕ) :
    expandedCost seed phase (2*m+2)+phase=9*(seed+phase)*9^m := by
  rw [actual_expanded_word_cost]
  rw [show 2*m+2=2*(m+1) by omega,pow_mul,Nat.pow_succ]
  norm_num
  ring

theorem literal_expanded_code_schedule_eventually_fits_owned_resolution
    (seed phase c : ℕ) (A : ℝ) :
    ∀ᶠ m : ℕ in atTop,
      (expandedCost seed phase (2*m+2)+phase : ℕ)*A*(m : ℝ)^c≤D0.phi^(5*m) := by
  have h := actual_expanded_compiler_cost_eventually_fits_owned_phi
    (9*(seed+phase)*A) c
  filter_upwards [h] with m hm
  rw [exact_full_preparation_cost_at_resolution_schedule]
  push_cast
  nlinarith only [hm]

end
end D0.Research.GoldenProgramCompilation

#check D0.Research.GoldenProgramCompilation.golden_square_formula
#print axioms D0.Research.GoldenProgramCompilation.golden_square_formula
#check D0.Research.GoldenProgramCompilation.native_root_interval
#print axioms D0.Research.GoldenProgramCompilation.native_root_interval
#check D0.Research.GoldenProgramCompilation.owned_golden_square_changes_basis
#print axioms D0.Research.GoldenProgramCompilation.owned_golden_square_changes_basis
#check D0.Research.GoldenProgramCompilation.literal_p0_square_changes_basis
#print axioms D0.Research.GoldenProgramCompilation.literal_p0_square_changes_basis
#check D0.Research.GoldenProgramCompilation.retained_copy_is_involutive
#print axioms D0.Research.GoldenProgramCompilation.retained_copy_is_involutive
#check D0.Research.GoldenProgramCompilation.forward_copy_echo_formula
#print axioms D0.Research.GoldenProgramCompilation.forward_copy_echo_formula
#check D0.Research.GoldenProgramCompilation.forward_copy_echo_retains_one_and_inverts_pointer
#print axioms D0.Research.GoldenProgramCompilation.forward_copy_echo_retains_one_and_inverts_pointer
#check D0.Research.GoldenProgramCompilation.eval_empty
#print axioms D0.Research.GoldenProgramCompilation.eval_empty
#check D0.Research.GoldenProgramCompilation.eval_cons
#print axioms D0.Research.GoldenProgramCompilation.eval_cons
#check D0.Research.GoldenProgramCompilation.complete_word_isometry
#print axioms D0.Research.GoldenProgramCompilation.complete_word_isometry
#check D0.Research.GoldenProgramCompilation.one_compiled_step_error
#print axioms D0.Research.GoldenProgramCompilation.one_compiled_step_error
#check D0.Research.GoldenProgramCompilation.whole_compiled_word_error
#print axioms D0.Research.GoldenProgramCompilation.whole_compiled_word_error
#check D0.Research.GoldenProgramCompilation.compiled_word_preserves_every_record_norm
#print axioms D0.Research.GoldenProgramCompilation.compiled_word_preserves_every_record_norm
#check D0.Research.GoldenProgramCompilation.calibrated_complete_state_error
#print axioms D0.Research.GoldenProgramCompilation.calibrated_complete_state_error
#check D0.Research.GoldenProgramCompilation.native_fifth_resolution_scale
#print axioms D0.Research.GoldenProgramCompilation.native_fifth_resolution_scale
#check D0.Research.GoldenProgramCompilation.native_fifth_scale_separates_cost_and_accuracy
#print axioms D0.Research.GoldenProgramCompilation.native_fifth_scale_separates_cost_and_accuracy
#check D0.Research.GoldenProgramCompilation.precision_has_native_resolution_bound
#print axioms D0.Research.GoldenProgramCompilation.precision_has_native_resolution_bound
#check D0.Research.GoldenProgramCompilation.expanded_compiler_cost_div_resolution_tends_zero
#print axioms D0.Research.GoldenProgramCompilation.expanded_compiler_cost_div_resolution_tends_zero
#check D0.Research.GoldenProgramCompilation.every_fixed_compiler_polynomial_eventually_fits
#print axioms D0.Research.GoldenProgramCompilation.every_fixed_compiler_polynomial_eventually_fits
#check D0.Research.GoldenProgramCompilation.actual_owned_phi_is_one_plus_primitive
#print axioms D0.Research.GoldenProgramCompilation.actual_owned_phi_is_one_plus_primitive
#check D0.Research.GoldenProgramCompilation.actual_resolution_is_owned_phi_level
#print axioms D0.Research.GoldenProgramCompilation.actual_resolution_is_owned_phi_level
#check D0.Research.GoldenProgramCompilation.actual_owned_code_scale_and_accuracy
#print axioms D0.Research.GoldenProgramCompilation.actual_owned_code_scale_and_accuracy
#check D0.Research.GoldenProgramCompilation.actual_expanded_compiler_cost_eventually_fits_owned_phi
#print axioms D0.Research.GoldenProgramCompilation.actual_expanded_compiler_cost_eventually_fits_owned_phi
#check D0.Research.GoldenProgramCompilation.success_phase_unit
#print axioms D0.Research.GoldenProgramCompilation.success_phase_unit
#check D0.Research.GoldenProgramCompilation.success_correction_unit
#print axioms D0.Research.GoldenProgramCompilation.success_correction_unit
#check D0.Research.GoldenProgramCompilation.success_phase_times_own_norm
#print axioms D0.Research.GoldenProgramCompilation.success_phase_times_own_norm
#check D0.Research.GoldenProgramCompilation.success_correction_times_phase
#print axioms D0.Research.GoldenProgramCompilation.success_correction_times_phase
#check D0.Research.GoldenProgramCompilation.success_correction_makes_own_success_positive
#print axioms D0.Research.GoldenProgramCompilation.success_correction_makes_own_success_positive
#check D0.Research.GoldenProgramCompilation.success_correction_is_unique
#print axioms D0.Research.GoldenProgramCompilation.success_correction_is_unique
#check D0.Research.GoldenProgramCompilation.success_distance_from_unit_phase
#print axioms D0.Research.GoldenProgramCompilation.success_distance_from_unit_phase
#check D0.Research.GoldenProgramCompilation.complete_calibrated_distance_identity
#print axioms D0.Research.GoldenProgramCompilation.complete_calibrated_distance_identity
#check D0.Research.GoldenProgramCompilation.balanced_success_ne_zero
#print axioms D0.Research.GoldenProgramCompilation.balanced_success_ne_zero
#check D0.Research.GoldenProgramCompilation.balanced_success_radial_error
#print axioms D0.Research.GoldenProgramCompilation.balanced_success_radial_error
#check D0.Research.GoldenProgramCompilation.actual_full_calibrated_column_fixed_target_error
#print axioms D0.Research.GoldenProgramCompilation.actual_full_calibrated_column_fixed_target_error
#check D0.Research.GoldenProgramCompilation.actual_full_calibrated_column_has_complete_unit_weight
#print axioms D0.Research.GoldenProgramCompilation.actual_full_calibrated_column_has_complete_unit_weight
#check D0.Research.GoldenProgramCompilation.native_full_calibrated_column_rate
#print axioms D0.Research.GoldenProgramCompilation.native_full_calibrated_column_rate
#check D0.Research.GoldenProgramCompilation.calibration_is_one_complete_pointer_operation
#print axioms D0.Research.GoldenProgramCompilation.calibration_is_one_complete_pointer_operation
#check D0.Research.GoldenProgramCompilation.all_33_literal_scene_calibrated_columns_have_fixed_real_targets
#print axioms D0.Research.GoldenProgramCompilation.all_33_literal_scene_calibrated_columns_have_fixed_real_targets
#check D0.Research.GoldenProgramCompilation.real_hilbert_norm_sq_is_complete_weight
#print axioms D0.Research.GoldenProgramCompilation.real_hilbert_norm_sq_is_complete_weight
#check D0.Research.GoldenProgramCompilation.real_hilbert_subtracts
#print axioms D0.Research.GoldenProgramCompilation.real_hilbert_subtracts
#check D0.Research.GoldenProgramCompilation.matrix_operator_acts_on_every_complete_coordinate
#print axioms D0.Research.GoldenProgramCompilation.matrix_operator_acts_on_every_complete_coordinate
#check D0.Research.GoldenProgramCompilation.whole_real_orthogonal_operator_preserves_weight
#print axioms D0.Research.GoldenProgramCompilation.whole_real_orthogonal_operator_preserves_weight
#check D0.Research.GoldenProgramCompilation.whole_real_orthogonal_operator_is_hilbert_isometry
#print axioms D0.Research.GoldenProgramCompilation.whole_real_orthogonal_operator_is_hilbert_isometry
#check D0.Research.GoldenProgramCompilation.faithful_full_complex_norm_is_hilbert_norm_sq
#print axioms D0.Research.GoldenProgramCompilation.faithful_full_complex_norm_is_hilbert_norm_sq
#check D0.Research.GoldenProgramCompilation.complete_calibrated_matrix_column_is_actual_calibrated_state
#print axioms D0.Research.GoldenProgramCompilation.complete_calibrated_matrix_column_is_actual_calibrated_state
#check D0.Research.GoldenProgramCompilation.complete_calibrated_matrix_is_unitary
#print axioms D0.Research.GoldenProgramCompilation.complete_calibrated_matrix_is_unitary
#check D0.Research.GoldenProgramCompilation.complete_calibrated_real_matrix_is_orthogonal
#print axioms D0.Research.GoldenProgramCompilation.complete_calibrated_real_matrix_is_orthogonal
#check D0.Research.GoldenProgramCompilation.actual_calibrated_matrix_blank_hilbert_action
#print axioms D0.Research.GoldenProgramCompilation.actual_calibrated_matrix_blank_hilbert_action
#check D0.Research.GoldenProgramCompilation.actual_blank_is_complete_unit_hilbert_state
#print axioms D0.Research.GoldenProgramCompilation.actual_blank_is_complete_unit_hilbert_state
#check D0.Research.GoldenProgramCompilation.actual_target_seed_is_complete_unit_hilbert_state
#print axioms D0.Research.GoldenProgramCompilation.actual_target_seed_is_complete_unit_hilbert_state
#check D0.Research.GoldenProgramCompilation.complete_compilation_and_preparation_error
#print axioms D0.Research.GoldenProgramCompilation.complete_compilation_and_preparation_error
#check D0.Research.GoldenProgramCompilation.entire_literal_word_and_preparation_error
#print axioms D0.Research.GoldenProgramCompilation.entire_literal_word_and_preparation_error
#check D0.Research.GoldenProgramCompilation.finite_compilation_budget_can_be_shared
#print axioms D0.Research.GoldenProgramCompilation.finite_compilation_budget_can_be_shared
#check D0.Research.GoldenProgramCompilation.two_error_halves_give_fixed_complete_rate
#print axioms D0.Research.GoldenProgramCompilation.two_error_halves_give_fixed_complete_rate
#check D0.Research.GoldenProgramCompilation.actual_native_preparation_norm_fits_half_precision
#print axioms D0.Research.GoldenProgramCompilation.actual_native_preparation_norm_fits_half_precision
#check D0.Research.GoldenProgramCompilation.actual_compiled_native_state_has_fixed_complete_rate
#print axioms D0.Research.GoldenProgramCompilation.actual_compiled_native_state_has_fixed_complete_rate
#check D0.Research.GoldenProgramCompilation.every_real_projector_reading_follows_complete_compilation_rate
#print axioms D0.Research.GoldenProgramCompilation.every_real_projector_reading_follows_complete_compilation_rate
#check D0.Research.GoldenProgramCompilation.entire_refinement_preserves_compiled_error
#print axioms D0.Research.GoldenProgramCompilation.entire_refinement_preserves_compiled_error
#check D0.Research.GoldenProgramCompilation.one_ancilla_retaining_compiled_step_error
#print axioms D0.Research.GoldenProgramCompilation.one_ancilla_retaining_compiled_step_error
#check D0.Research.GoldenProgramCompilation.whole_compiled_word_keeps_all_ancilla_leakage
#print axioms D0.Research.GoldenProgramCompilation.whole_compiled_word_keeps_all_ancilla_leakage
#check D0.Research.GoldenProgramCompilation.whole_ancilla_retaining_program_has_complete_unit_norm
#print axioms D0.Research.GoldenProgramCompilation.whole_ancilla_retaining_program_has_complete_unit_norm
#check D0.Research.GoldenProgramCompilation.ancilla_retaining_compiler_and_preparation_error
#print axioms D0.Research.GoldenProgramCompilation.ancilla_retaining_compiler_and_preparation_error
#check D0.Research.GoldenProgramCompilation.literal_ancilla_retaining_word_and_preparation_error
#print axioms D0.Research.GoldenProgramCompilation.literal_ancilla_retaining_word_and_preparation_error
#check D0.Research.GoldenProgramCompilation.every_compilation_choice_with_vanishing_error_has_same_fixed_limit
#print axioms D0.Research.GoldenProgramCompilation.every_compilation_choice_with_vanishing_error_has_same_fixed_limit
#check D0.Research.GoldenProgramCompilation.actual_ancilla_retaining_compiled_native_state_rate
#print axioms D0.Research.GoldenProgramCompilation.actual_ancilla_retaining_compiled_native_state_rate
#check D0.Research.GoldenProgramCompilation.native_compiled_precision_tends_zero
#print axioms D0.Research.GoldenProgramCompilation.native_compiled_precision_tends_zero
#check D0.Research.GoldenProgramCompilation.whole_common_raw_record_mass
#print axioms D0.Research.GoldenProgramCompilation.whole_common_raw_record_mass
#check D0.Research.GoldenProgramCompilation.common_record_has_complete_unit_mass
#print axioms D0.Research.GoldenProgramCompilation.common_record_has_complete_unit_mass
#check D0.Research.GoldenProgramCompilation.actual_common_record_mass_is_native_value
#print axioms D0.Research.GoldenProgramCompilation.actual_common_record_mass_is_native_value
#check D0.Research.GoldenProgramCompilation.actual_common_record_mass_positive
#print axioms D0.Research.GoldenProgramCompilation.actual_common_record_mass_positive
#check D0.Research.GoldenProgramCompilation.complete_retained_target_has_one_common_record_factor
#print axioms D0.Research.GoldenProgramCompilation.complete_retained_target_has_one_common_record_factor
#check D0.Research.GoldenProgramCompilation.every_actual_scene_target_has_same_retained_record
#print axioms D0.Research.GoldenProgramCompilation.every_actual_scene_target_has_same_retained_record
#check D0.Research.GoldenProgramCompilation.actual_p0_common_retained_record_has_unit_mass
#print axioms D0.Research.GoldenProgramCompilation.actual_p0_common_retained_record_has_unit_mass
#check D0.Research.GoldenProgramCompilation.complete_common_record_preserves_every_mixed_gram
#print axioms D0.Research.GoldenProgramCompilation.complete_common_record_preserves_every_mixed_gram
#check D0.Research.GoldenProgramCompilation.complete_common_record_preserves_history_frame_isometry
#print axioms D0.Research.GoldenProgramCompilation.complete_common_record_preserves_history_frame_isometry
#check D0.Research.GoldenProgramCompilation.complete_reverse_acts_without_forgetting_common_record
#print axioms D0.Research.GoldenProgramCompilation.complete_reverse_acts_without_forgetting_common_record
#check D0.Research.GoldenProgramCompilation.complete_common_record_preserves_every_history_return
#print axioms D0.Research.GoldenProgramCompilation.complete_common_record_preserves_every_history_return
#check D0.Research.GoldenProgramCompilation.native_common_record_preserves_owned_history_return
#print axioms D0.Research.GoldenProgramCompilation.native_common_record_preserves_owned_history_return
#check D0.Research.GoldenProgramCompilation.exact_full_preparation_cost_at_resolution_schedule
#print axioms D0.Research.GoldenProgramCompilation.exact_full_preparation_cost_at_resolution_schedule
#check D0.Research.GoldenProgramCompilation.literal_expanded_code_schedule_eventually_fits_owned_resolution
#print axioms D0.Research.GoldenProgramCompilation.literal_expanded_code_schedule_eventually_fits_owned_resolution
