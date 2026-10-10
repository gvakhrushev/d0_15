import D0.Representation.GoldenCoherentMemory
import D0.CondensedAnchor.DetectorSupportGoldenWeight
import D0.Synthesis.SceneNormalizedQuotientDescent
import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.LinearAlgebra.Matrix.Permutation
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

#check D0.Research.GoldenHistoryPreparation.flipFirst_involutive
#print axioms D0.Research.GoldenHistoryPreparation.flipFirst_involutive
#check D0.Research.GoldenHistoryPreparation.firstLabel_flipFirst
#print axioms D0.Research.GoldenHistoryPreparation.firstLabel_flipFirst
#check D0.Research.GoldenHistoryPreparation.amplitude_flipFirst
#print axioms D0.Research.GoldenHistoryPreparation.amplitude_flipFirst
#check D0.Research.GoldenHistoryPreparation.complete_mass
#print axioms D0.Research.GoldenHistoryPreparation.complete_mass
#check D0.Research.GoldenHistoryPreparation.failure_mass
#print axioms D0.Research.GoldenHistoryPreparation.failure_mass
#check D0.Research.GoldenHistoryPreparation.copyLabel_involutive
#print axioms D0.Research.GoldenHistoryPreparation.copyLabel_involutive
#check D0.Research.GoldenHistoryPreparation.controlledFlip_involutive
#print axioms D0.Research.GoldenHistoryPreparation.controlledFlip_involutive
#check D0.Research.GoldenHistoryPreparation.full_retained_route_bijective
#print axioms D0.Research.GoldenHistoryPreparation.full_retained_route_bijective
#check D0.Research.GoldenHistoryPreparation.full_retained_route_inverse
#print axioms D0.Research.GoldenHistoryPreparation.full_retained_route_inverse
#check D0.Research.GoldenHistoryPreparation.failed_record_unchanged
#print axioms D0.Research.GoldenHistoryPreparation.failed_record_unchanged
#check D0.Research.GoldenHistoryPreparation.success_false_record
#print axioms D0.Research.GoldenHistoryPreparation.success_false_record
#check D0.Research.GoldenHistoryPreparation.success_true_record
#print axioms D0.Research.GoldenHistoryPreparation.success_true_record
#check D0.Research.GoldenHistoryPreparation.successful_coherent_twins
#print axioms D0.Research.GoldenHistoryPreparation.successful_coherent_twins
#check D0.Research.GoldenHistoryPreparation.complete_coherent_success_symmetry
#print axioms D0.Research.GoldenHistoryPreparation.complete_coherent_success_symmetry
#check D0.Research.GoldenHistoryPreparation.complete_mass_partition
#print axioms D0.Research.GoldenHistoryPreparation.complete_mass_partition
#check D0.Research.GoldenHistoryPreparation.exact_fair_success_weights
#print axioms D0.Research.GoldenHistoryPreparation.exact_fair_success_weights
#check D0.Research.GoldenHistoryPreparation.actual_owned_golden_blank
#print axioms D0.Research.GoldenHistoryPreparation.actual_owned_golden_blank
#check D0.Research.GoldenHistoryPreparation.golden_factor_normalized
#print axioms D0.Research.GoldenHistoryPreparation.golden_factor_normalized
#check D0.Research.GoldenHistoryPreparation.golden_failure_parameter
#print axioms D0.Research.GoldenHistoryPreparation.golden_failure_parameter
#check D0.Research.GoldenHistoryPreparation.full_retained_route_preserves_all_norms
#print axioms D0.Research.GoldenHistoryPreparation.full_retained_route_preserves_all_norms
#check D0.Research.GoldenHistoryPreparation.golden_root_interval
#print axioms D0.Research.GoldenHistoryPreparation.golden_root_interval
#check D0.Research.GoldenHistoryPreparation.golden_pair_success_balance
#print axioms D0.Research.GoldenHistoryPreparation.golden_pair_success_balance
#check D0.Research.GoldenHistoryPreparation.golden_pair_failure_bounds
#print axioms D0.Research.GoldenHistoryPreparation.golden_pair_failure_bounds
#check D0.Research.GoldenHistoryPreparation.golden_four_pair_good_weight
#print axioms D0.Research.GoldenHistoryPreparation.golden_four_pair_good_weight
#check D0.Research.GoldenHistoryPreparation.golden_five_bit_good_bounds
#print axioms D0.Research.GoldenHistoryPreparation.golden_five_bit_good_bounds
#check D0.Research.GoldenHistoryPreparation.native_degree_retained_preparation_rate
#print axioms D0.Research.GoldenHistoryPreparation.native_degree_retained_preparation_rate
#check D0.Research.GoldenHistoryPreparation.native_degree_all_retained_retries_bound
#print axioms D0.Research.GoldenHistoryPreparation.native_degree_all_retained_retries_bound
#check D0.Research.GoldenHistoryPreparation.frozen_native_golden_fair_history
#print axioms D0.Research.GoldenHistoryPreparation.frozen_native_golden_fair_history
#check D0.Research.GoldenHistoryPreparation.complete_rejected_record_gram
#print axioms D0.Research.GoldenHistoryPreparation.complete_rejected_record_gram
#check D0.Research.GoldenHistoryPreparation.complete_rejected_record_overlap_bound
#print axioms D0.Research.GoldenHistoryPreparation.complete_rejected_record_overlap_bound
#check D0.Research.GoldenHistoryPreparation.sqrt_success_ratio_coefficient
#print axioms D0.Research.GoldenHistoryPreparation.sqrt_success_ratio_coefficient
#check D0.Research.GoldenHistoryPreparation.exact_retained_retry_gram
#print axioms D0.Research.GoldenHistoryPreparation.exact_retained_retry_gram
#check D0.Research.GoldenHistoryPreparation.whole_retained_retry_coherence_bound
#print axioms D0.Research.GoldenHistoryPreparation.whole_retained_retry_coherence_bound
#check D0.Research.GoldenHistoryPreparation.actual_degree_twenty_twentyfour_ratio
#print axioms D0.Research.GoldenHistoryPreparation.actual_degree_twenty_twentyfour_ratio
#check D0.Research.GoldenHistoryPreparation.actual_degree_retained_retry_coherence_floor
#print axioms D0.Research.GoldenHistoryPreparation.actual_degree_retained_retry_coherence_floor
#check D0.Research.GoldenHistoryPreparation.exact_retained_retry_gram_limit
#print axioms D0.Research.GoldenHistoryPreparation.exact_retained_retry_gram_limit
#check D0.Research.GoldenHistoryPreparation.complete_disjoint_record_code_mass
#print axioms D0.Research.GoldenHistoryPreparation.complete_disjoint_record_code_mass
#check D0.Research.GoldenHistoryPreparation.whole_fair_code_mass
#print axioms D0.Research.GoldenHistoryPreparation.whole_fair_code_mass
#check D0.Research.GoldenHistoryPreparation.actual_five_bit_code_carrier
#print axioms D0.Research.GoldenHistoryPreparation.actual_five_bit_code_carrier
#check D0.Research.GoldenHistoryPreparation.actual_five_bit_code_mass
#print axioms D0.Research.GoldenHistoryPreparation.actual_five_bit_code_mass
#check D0.Research.GoldenHistoryPreparation.full_retained_valid_code_mass
#print axioms D0.Research.GoldenHistoryPreparation.full_retained_valid_code_mass
#check D0.Research.GoldenHistoryPreparation.all_disjoint_retained_records_reversible
#print axioms D0.Research.GoldenHistoryPreparation.all_disjoint_retained_records_reversible
#check D0.Research.GoldenHistoryPreparation.full_successful_code_keeps_same_record
#print axioms D0.Research.GoldenHistoryPreparation.full_successful_code_keeps_same_record
#check D0.Research.GoldenHistoryPreparation.full_code_coherent_amplitude_independence
#print axioms D0.Research.GoldenHistoryPreparation.full_code_coherent_amplitude_independence
#check D0.Research.GoldenCoherentAmplification.copy_from_owned_record
#print axioms D0.Research.GoldenCoherentAmplification.copy_from_owned_record
#check D0.Research.GoldenCoherentAmplification.golden_controlled_square_word
#print axioms D0.Research.GoldenCoherentAmplification.golden_controlled_square_word
#check D0.Research.GoldenCoherentAmplification.golden_phase_components
#print axioms D0.Research.GoldenCoherentAmplification.golden_phase_components
#check D0.Research.GoldenCoherentAmplification.golden_phase_normSq
#print axioms D0.Research.GoldenCoherentAmplification.golden_phase_normSq
#check D0.Research.GoldenCoherentAmplification.unit_phase_quadratic
#print axioms D0.Research.GoldenCoherentAmplification.unit_phase_quadratic
#check D0.Research.GoldenCoherentAmplification.coherent_bad_multiplier
#print axioms D0.Research.GoldenCoherentAmplification.coherent_bad_multiplier
#check D0.Research.GoldenCoherentAmplification.actual_golden_bad_multiplier
#print axioms D0.Research.GoldenCoherentAmplification.actual_golden_bad_multiplier
#check D0.Research.GoldenCoherentAmplification.golden_coherent_failure_law
#print axioms D0.Research.GoldenCoherentAmplification.golden_coherent_failure_law
#check D0.Research.GoldenCoherentAmplification.generic_retained_contraction
#print axioms D0.Research.GoldenCoherentAmplification.generic_retained_contraction
#check D0.Research.GoldenCoherentAmplification.all_retained_contraction
#print axioms D0.Research.GoldenCoherentAmplification.all_retained_contraction
#check D0.Research.GoldenCoherentAmplification.frozen_golden_contraction_bounds
#print axioms D0.Research.GoldenCoherentAmplification.frozen_golden_contraction_bounds
#check D0.Research.GoldenCoherentAmplification.preparedRotation_conjTranspose
#print axioms D0.Research.GoldenCoherentAmplification.preparedRotation_conjTranspose
#check D0.Research.GoldenCoherentAmplification.preparedRotation_unitary
#print axioms D0.Research.GoldenCoherentAmplification.preparedRotation_unitary
#check D0.Research.GoldenCoherentAmplification.selectivePhase_unitary
#print axioms D0.Research.GoldenCoherentAmplification.selectivePhase_unitary
#check D0.Research.GoldenCoherentAmplification.complete_word_unitary
#print axioms D0.Research.GoldenCoherentAmplification.complete_word_unitary
#check D0.Research.GoldenCoherentAmplification.complete_word_bad_component
#print axioms D0.Research.GoldenCoherentAmplification.complete_word_bad_component
#check D0.Research.GoldenCoherentAmplification.complete_word_good_component
#print axioms D0.Research.GoldenCoherentAmplification.complete_word_good_component
#check D0.Research.GoldenCoherentAmplification.full_word_golden_failure_probability
#print axioms D0.Research.GoldenCoherentAmplification.full_word_golden_failure_probability
#check D0.Research.GoldenCoherentAmplification.golden_pair_realification
#print axioms D0.Research.GoldenCoherentAmplification.golden_pair_realification
#check D0.Research.GoldenCoherentAmplification.phase_aligned_complete_state_error
#print axioms D0.Research.GoldenCoherentAmplification.phase_aligned_complete_state_error
#check D0.Research.GoldenCoherentAmplification.retained_golden_depth_rate
#print axioms D0.Research.GoldenCoherentAmplification.retained_golden_depth_rate
#check D0.Research.GoldenCoherentAmplification.native_preparation_enters_retained_contraction
#print axioms D0.Research.GoldenCoherentAmplification.native_preparation_enters_retained_contraction
#check D0.Research.GoldenCoherentAmplification.native_preparation_coherent_failure_rate
#print axioms D0.Research.GoldenCoherentAmplification.native_preparation_coherent_failure_rate
#check D0.Research.GoldenCoherentAmplification.frozen_three_native_degrees_coherent_failure_rate
#print axioms D0.Research.GoldenCoherentAmplification.frozen_three_native_degrees_coherent_failure_rate
#check D0.Research.GoldenCoherentAmplification.native_complete_state_error_after_declared_phase_alignment
#print axioms D0.Research.GoldenCoherentAmplification.native_complete_state_error_after_declared_phase_alignment
#check D0.Research.GoldenCoherentAmplification.complete_weight_partition
#print axioms D0.Research.GoldenCoherentAmplification.complete_weight_partition
#check D0.Research.GoldenCoherentAmplification.rejected_weight_nonnegative
#print axioms D0.Research.GoldenCoherentAmplification.rejected_weight_nonnegative
#check D0.Research.GoldenCoherentAmplification.diagonal_phase_unitary
#print axioms D0.Research.GoldenCoherentAmplification.diagonal_phase_unitary
#check D0.Research.GoldenCoherentAmplification.blank_phase_complete_projector
#print axioms D0.Research.GoldenCoherentAmplification.blank_phase_complete_projector
#check D0.Research.GoldenCoherentAmplification.unitary_column_has_complete_weight
#print axioms D0.Research.GoldenCoherentAmplification.unitary_column_has_complete_weight
#check D0.Research.GoldenCoherentAmplification.full_amplify_unitary
#print axioms D0.Research.GoldenCoherentAmplification.full_amplify_unitary
#check D0.Research.GoldenCoherentAmplification.full_prepared_phase_conjugation
#print axioms D0.Research.GoldenCoherentAmplification.full_prepared_phase_conjugation
#check D0.Research.GoldenCoherentAmplification.complete_phase_expectation
#print axioms D0.Research.GoldenCoherentAmplification.complete_phase_expectation
#check D0.Research.GoldenCoherentAmplification.full_amplify_column
#print axioms D0.Research.GoldenCoherentAmplification.full_amplify_column
#check D0.Research.GoldenCoherentAmplification.all_failed_coordinates_keep_original_record
#print axioms D0.Research.GoldenCoherentAmplification.all_failed_coordinates_keep_original_record
#check D0.Research.GoldenCoherentAmplification.complete_failed_weight_law
#print axioms D0.Research.GoldenCoherentAmplification.complete_failed_weight_law
#check D0.Research.GoldenCoherentAmplification.all_full_words_unitary
#print axioms D0.Research.GoldenCoherentAmplification.all_full_words_unitary
#check D0.Research.GoldenCoherentAmplification.actual_full_word_golden_failure
#print axioms D0.Research.GoldenCoherentAmplification.actual_full_word_golden_failure
#check D0.Research.GoldenCoherentAmplification.fourth_unit_phase_real
#print axioms D0.Research.GoldenCoherentAmplification.fourth_unit_phase_real
#check D0.Research.GoldenCoherentAmplification.fast_golden_phase_real
#print axioms D0.Research.GoldenCoherentAmplification.fast_golden_phase_real
#check D0.Research.GoldenCoherentAmplification.fast_golden_phase_normSq
#print axioms D0.Research.GoldenCoherentAmplification.fast_golden_phase_normSq
#check D0.Research.GoldenCoherentAmplification.fast_parameter_native_bounds
#print axioms D0.Research.GoldenCoherentAmplification.fast_parameter_native_bounds
#check D0.Research.GoldenCoherentAmplification.fast_actual_bad_multiplier
#print axioms D0.Research.GoldenCoherentAmplification.fast_actual_bad_multiplier
#check D0.Research.GoldenCoherentAmplification.fast_actual_failure_law
#print axioms D0.Research.GoldenCoherentAmplification.fast_actual_failure_law
#check D0.Research.GoldenCoherentAmplification.fast_burnin_first
#print axioms D0.Research.GoldenCoherentAmplification.fast_burnin_first
#check D0.Research.GoldenCoherentAmplification.fast_burnin_second
#print axioms D0.Research.GoldenCoherentAmplification.fast_burnin_second
#check D0.Research.GoldenCoherentAmplification.fast_small_error_contraction
#print axioms D0.Research.GoldenCoherentAmplification.fast_small_error_contraction
#check D0.Research.GoldenCoherentAmplification.fast_two_stage_burnin
#print axioms D0.Research.GoldenCoherentAmplification.fast_two_stage_burnin
#check D0.Research.GoldenCoherentAmplification.fast_all_full_failure_rate
#print axioms D0.Research.GoldenCoherentAmplification.fast_all_full_failure_rate
#check D0.Research.GoldenCoherentAmplification.actual_full_word_fast_failure
#print axioms D0.Research.GoldenCoherentAmplification.actual_full_word_fast_failure
#check D0.Research.GoldenCoherentAmplification.actual_expanded_word_cost
#print axioms D0.Research.GoldenCoherentAmplification.actual_expanded_word_cost
#check D0.Research.GoldenCoherentAmplification.fast_failure_better_than_expanded_inverse_square
#print axioms D0.Research.GoldenCoherentAmplification.fast_failure_better_than_expanded_inverse_square
#check D0.Research.GoldenCoherentAmplification.fast_failure_with_literal_word_cost
#print axioms D0.Research.GoldenCoherentAmplification.fast_failure_with_literal_word_cost
#check D0.Research.GoldenCoherentAmplification.golden_square_rate_does_not_bound_tripled_word_cost
#print axioms D0.Research.GoldenCoherentAmplification.golden_square_rate_does_not_bound_tripled_word_cost
#check D0.Research.GoldenCoherentAmplification.literal_bool_golden_gate_unitary
#print axioms D0.Research.GoldenCoherentAmplification.literal_bool_golden_gate_unitary
#check D0.Research.GoldenCoherentAmplification.kronecker_retains_all_unitarity
#print axioms D0.Research.GoldenCoherentAmplification.kronecker_retains_all_unitarity
#check D0.Research.GoldenCoherentAmplification.actual_word_seed_unitary
#print axioms D0.Research.GoldenCoherentAmplification.actual_word_seed_unitary
#check D0.Research.GoldenCoherentAmplification.actual_word_seed_amplitudes
#print axioms D0.Research.GoldenCoherentAmplification.actual_word_seed_amplitudes
#check D0.Research.GoldenCoherentAmplification.pi_matrix_retains_all_unitarity
#print axioms D0.Research.GoldenCoherentAmplification.pi_matrix_retains_all_unitarity
#check D0.Research.GoldenCoherentAmplification.complete_golden_seed_unitary
#print axioms D0.Research.GoldenCoherentAmplification.complete_golden_seed_unitary
#check D0.Research.GoldenCoherentAmplification.complete_golden_seed_blank_amplitudes
#print axioms D0.Research.GoldenCoherentAmplification.complete_golden_seed_blank_amplitudes
#check D0.Research.GoldenCoherentAmplification.full_routing_permutation_unitary
#print axioms D0.Research.GoldenCoherentAmplification.full_routing_permutation_unitary
#check D0.Research.GoldenCoherentAmplification.actual_retained_routed_seed_unitary
#print axioms D0.Research.GoldenCoherentAmplification.actual_retained_routed_seed_unitary
#check D0.Research.GoldenCoherentAmplification.actual_routed_seed_successful_amplitude
#print axioms D0.Research.GoldenCoherentAmplification.actual_routed_seed_successful_amplitude
#check D0.Research.GoldenCoherentAmplification.complete_all_good_record_mass
#print axioms D0.Research.GoldenCoherentAmplification.complete_all_good_record_mass
#check D0.Research.GoldenCoherentAmplification.complete_retained_seed_valid_mass
#print axioms D0.Research.GoldenCoherentAmplification.complete_retained_seed_valid_mass
#check D0.Research.GoldenCoherentAmplification.literal_five_stream_seed_valid_mass
#print axioms D0.Research.GoldenCoherentAmplification.literal_five_stream_seed_valid_mass
#check D0.Research.GoldenCoherentAmplification.literal_five_stream_seed_failure
#print axioms D0.Research.GoldenCoherentAmplification.literal_five_stream_seed_failure
#check D0.Research.GoldenCoherentAmplification.native_literal_seed_fast_full_word_rate
#print axioms D0.Research.GoldenCoherentAmplification.native_literal_seed_fast_full_word_rate
#check D0.Research.GoldenCoherentAmplification.full_word_is_recorded_word
#print axioms D0.Research.GoldenCoherentAmplification.full_word_is_recorded_word
#check D0.Research.GoldenCoherentAmplification.suffix_lift_multiplication
#print axioms D0.Research.GoldenCoherentAmplification.suffix_lift_multiplication
#check D0.Research.GoldenCoherentAmplification.suffix_lift_conjugation
#print axioms D0.Research.GoldenCoherentAmplification.suffix_lift_conjugation
#check D0.Research.GoldenCoherentAmplification.complete_recorded_word_suffix_natural
#print axioms D0.Research.GoldenCoherentAmplification.complete_recorded_word_suffix_natural
#check D0.Research.GoldenCoherentAmplification.golden_complex_operator_intertwines
#print axioms D0.Research.GoldenCoherentAmplification.golden_complex_operator_intertwines
#check D0.Research.GoldenCoherentAmplification.golden_complex_inclusion_weight
#print axioms D0.Research.GoldenCoherentAmplification.golden_complex_inclusion_weight
#check D0.Research.GoldenCoherentAmplification.golden_complex_rejection_weight
#print axioms D0.Research.GoldenCoherentAmplification.golden_complex_rejection_weight
#check D0.Research.GoldenCoherentAmplification.complete_golden_word_refinement
#print axioms D0.Research.GoldenCoherentAmplification.complete_golden_word_refinement
#check D0.Research.GoldenCoherentAmplification.complete_golden_failure_refinement
#print axioms D0.Research.GoldenCoherentAmplification.complete_golden_failure_refinement
#check D0.Research.GoldenCoherentAmplification.single_fine_blank_is_not_cylinder_extension
#print axioms D0.Research.GoldenCoherentAmplification.single_fine_blank_is_not_cylinder_extension
#check D0.Research.GoldenCoherentAmplification.owned_condensed_cylinder_amplitudes
#print axioms D0.Research.GoldenCoherentAmplification.owned_condensed_cylinder_amplitudes
#check D0.Research.GoldenCoherentAmplification.owned_primitive_root_is_condensed_weight
#print axioms D0.Research.GoldenCoherentAmplification.owned_primitive_root_is_condensed_weight
#check D0.Research.GoldenCoherentAmplification.actual_owned_golden_suffix_letter_weights
#print axioms D0.Research.GoldenCoherentAmplification.actual_owned_golden_suffix_letter_weights
#check D0.Research.GoldenCoherentAmplification.all_accepted_coordinates_keep_original_record
#print axioms D0.Research.GoldenCoherentAmplification.all_accepted_coordinates_keep_original_record
#check D0.Research.GoldenCoherentAmplification.complete_fast_word_all_record_coefficients
#print axioms D0.Research.GoldenCoherentAmplification.complete_fast_word_all_record_coefficients
#check D0.Research.GoldenCoherentAmplification.actual_full_seed_successful_record_factorization
#print axioms D0.Research.GoldenCoherentAmplification.actual_full_seed_successful_record_factorization
#check D0.Research.GoldenCoherentAmplification.phase_aligned_full_state_distance_identity
#print axioms D0.Research.GoldenCoherentAmplification.phase_aligned_full_state_distance_identity
#check D0.Research.GoldenCoherentAmplification.phase_aligned_full_vector_error
#print axioms D0.Research.GoldenCoherentAmplification.phase_aligned_full_vector_error
#check D0.Research.GoldenCoherentAmplification.aligned_accepted_vector_has_complete_weight
#print axioms D0.Research.GoldenCoherentAmplification.aligned_accepted_vector_has_complete_weight
#check D0.Research.GoldenCoherentAmplification.native_literal_full_vector_error
#print axioms D0.Research.GoldenCoherentAmplification.native_literal_full_vector_error
#check D0.Research.GoldenCoherentAmplification.phase_real_matrix_multiplication
#print axioms D0.Research.GoldenCoherentAmplification.phase_real_matrix_multiplication
#check D0.Research.GoldenCoherentAmplification.phase_real_matrix_powers
#print axioms D0.Research.GoldenCoherentAmplification.phase_real_matrix_powers
#check D0.Research.GoldenCoherentAmplification.fast_phase_is_owned_golden_eighth_power
#print axioms D0.Research.GoldenCoherentAmplification.fast_phase_is_owned_golden_eighth_power
#check D0.Research.GoldenCoherentAmplification.actual_scene_incoming_cardinality
#print axioms D0.Research.GoldenCoherentAmplification.actual_scene_incoming_cardinality
#check D0.Research.GoldenCoherentAmplification.actual_scene_incoming_cardinality_is_owned_degree
#print axioms D0.Research.GoldenCoherentAmplification.actual_scene_incoming_cardinality_is_owned_degree
#check D0.Research.GoldenCoherentAmplification.actual_scene_incoming_fits_five_bits
#print axioms D0.Research.GoldenCoherentAmplification.actual_scene_incoming_fits_five_bits
#check D0.Research.GoldenCoherentAmplification.actual_scene_incoming_code_injective
#print axioms D0.Research.GoldenCoherentAmplification.actual_scene_incoming_code_injective
#check D0.Research.GoldenCoherentAmplification.actual_scene_accepted_codes_cardinality
#print axioms D0.Research.GoldenCoherentAmplification.actual_scene_accepted_codes_cardinality
#check D0.Research.GoldenCoherentAmplification.actual_scene_accepted_codes_exact_degrees
#print axioms D0.Research.GoldenCoherentAmplification.actual_scene_accepted_codes_exact_degrees
#check D0.Research.GoldenCoherentAmplification.actual_scene_code_member
#print axioms D0.Research.GoldenCoherentAmplification.actual_scene_code_member
#check D0.Research.GoldenCoherentAmplification.actual_scene_all_incoming_histories_have_same_record_amplitude
#print axioms D0.Research.GoldenCoherentAmplification.actual_scene_all_incoming_histories_have_same_record_amplitude
#check D0.Research.GoldenCoherentAmplification.actual_scene_full_word_failure_rate
#print axioms D0.Research.GoldenCoherentAmplification.actual_scene_full_word_failure_rate
#check D0.Research.GoldenCoherentAmplification.actual_scene_full_word_state_error
#print axioms D0.Research.GoldenCoherentAmplification.actual_scene_full_word_state_error
#check D0.Research.GoldenCoherentAmplification.good_multiplier_retains_complex_phase
#print axioms D0.Research.GoldenCoherentAmplification.good_multiplier_retains_complex_phase
#check D0.Research.GoldenCoherentAmplification.distinct_success_laws_have_relative_phase_area
#print axioms D0.Research.GoldenCoherentAmplification.distinct_success_laws_have_relative_phase_area
#check D0.Research.GoldenCoherentAmplification.nonzero_relative_phase_blocks_one_real_ray
#print axioms D0.Research.GoldenCoherentAmplification.nonzero_relative_phase_blocks_one_real_ray
#check D0.Research.GoldenCoherentAmplification.own_fast_phase_has_nonzero_relative_area
#print axioms D0.Research.GoldenCoherentAmplification.own_fast_phase_has_nonzero_relative_area
#check D0.Research.GoldenCoherentAmplification.actual_degree_twenty_twentyfour_cannot_share_success_phase
#print axioms D0.Research.GoldenCoherentAmplification.actual_degree_twenty_twentyfour_cannot_share_success_phase
