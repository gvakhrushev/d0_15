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
import Mathlib.Data.ZMod.Basic
import D0.Foundation.VerifiabilityNecessity
import D0.Representation.FiniteProtocolClock
import D0.Representation.PreparationMemoryBound
import D0.Representation.OrderMemoryReadout
import Mathlib.Topology.Instances.Matrix


set_option linter.unnecessarySeqFocus false
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

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.RetainedRecordAdmission
noncomputable section
open Matrix Filter Topology
open scoped BigOperators Kronecker
open D0.Research.GoldenHistoryPreparation D0.Research.GoldenProgramCompilation

/-- Toggle the last bit of an existing complete raw pair-history. -/
def flipLast : {n : ℕ} → Word n → Word n
  | 0, w => w
  | 1, (x,w) => ((x.1,!x.2),w)
  | n+2, (x,w) => (x,flipLast w)

theorem flip_last_is_retained_involution (n : ℕ) : Function.Involutive (@flipLast n) := by
  induction n using Nat.twoStepInduction with
  | zero => intro w; rfl
  | one => rintro ⟨⟨b,c⟩,w⟩; cases c <;> rfl
  | more n ih ih2 => rintro ⟨x,w⟩; change (x,flipLast (flipLast w))=(x,w); rw [ih2]

def acceptedRaw (a p : ℝ) (n : ℕ) (w : Word n) : ℝ :=
  if firstLabel w=some false then amplitude a p w else 0

def rawCharge (a p : ℝ) (n : ℕ) : ℝ :=
  ∑ w : Word n, amplitude a p w*amplitude a p (flipLast w)
def goodCharge (a p : ℝ) (n : ℕ) : ℝ :=
  ∑ w : Word n, acceptedRaw a p n w*acceptedRaw a p n (flipLast w)

theorem accepted_raw_mass_is_owned_success_mass (a p : ℝ) (n : ℕ) :
    (∑ w,acceptedRaw a p n w^2)=successMass a p n false := by
  unfold successMass
  apply Finset.sum_congr rfl
  intro w _
  by_cases h : firstLabel w=some false <;> simp [acceptedRaw,h]

theorem raw_last_bit_charge_one (a p : ℝ) : rawCharge a p 1=2*a*p*(a^2+p^2) := by
  unfold rawCharge
  change (∑ w : Pair × Unit, _) = _
  simp [flipLast,amplitude,Fintype.sum_prod_type,Fintype.sum_bool]
  ring

theorem raw_last_bit_charge_recursion (a p : ℝ) (n : ℕ) :
    rawCharge a p (n+2)=(a^2+p^2)^2*rawCharge a p (n+1) := by
  change (∑ w : Pair × Word (n+1), _) = _
  simp only [Fintype.sum_prod_type,flipLast,amplitude,Fintype.sum_bool,
    Bool.false_eq_true,if_false,if_true]
  have scale (t : ℝ) : (∑ w : Word (n+1), t*amplitude a p w* (t*amplitude a p (flipLast w)))=
      t^2*rawCharge a p (n+1) := by
    unfold rawCharge
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro w _
    ring
  simp only [scale]
  ring

theorem every_normalized_raw_last_bit_charge (a p : ℝ) (h : a^2+p^2=1) (n : ℕ) :
    rawCharge a p (n+1)=2*a*p := by
  induction n with
  | zero => rw [raw_last_bit_charge_one,h]; ring
  | succ n ih => rw [raw_last_bit_charge_recursion,h,ih]; ring

theorem first_good_last_bit_charge_zero (a p : ℝ) : goodCharge a p 1=0 := by
  unfold goodCharge
  change (∑ w : Pair × Unit, _) = _
  simp [acceptedRaw,flipLast,amplitude,firstLabel,Fintype.sum_prod_type,Fintype.sum_bool]

theorem good_last_bit_charge_recursion (a p : ℝ) (n : ℕ) :
    goodCharge a p (n+2)=q a p*goodCharge a p (n+1)+(a*p)^2*rawCharge a p (n+1) := by
  change (∑ w : Pair × Word (n+1), _) = _
  simp only [Fintype.sum_prod_type,Fintype.sum_bool,acceptedRaw,firstLabel,flipLast,
    amplitude,Bool.false_eq_true,Bool.true_eq_false,Option.some.injEq,if_false,if_true]
  have scale (t : ℝ) :
      (∑ w : Word (n+1), (if firstLabel w=some false then t*amplitude a p w else 0)*
        (if firstLabel (flipLast w)=some false then t*amplitude a p (flipLast w) else 0))=
      t^2*goodCharge a p (n+1) := by
    unfold goodCharge acceptedRaw
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro w _
    split_ifs <;> ring
  have rawscale (t : ℝ) :
      (∑ w : Word (n+1), (t*amplitude a p w)*(t*amplitude a p (flipLast w)))=
      t^2*rawCharge a p (n+1) := by
    unfold rawCharge
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro w _
    ring
  simp only [scale,rawscale,zero_mul,mul_zero,Finset.sum_const_zero,add_zero,zero_add]
  unfold q
  ring

theorem success_mass_recursion (a p : ℝ) (n : ℕ) :
    successMass a p (n+1) false=q a p*successMass a p n false+(a*p)^2*
      (∑ w : Word n,amplitude a p w^2) := by
  unfold successMass
  change (∑ w : Pair × Word n, _) = _
  simp only [Fintype.sum_prod_type,Fintype.sum_bool,firstLabel,amplitude,
    Bool.false_eq_true,Bool.true_eq_false,Option.some.injEq,if_false,if_true,mul_pow]
  have scale (t : ℝ) :
      (∑ w : Word n,if firstLabel w=some false then t*amplitude a p w^2 else 0)=
      t*(∑ w : Word n,if firstLabel w=some false then amplitude a p w^2 else 0) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro w _
    split_ifs <;> ring
  rw [scale,scale,← Finset.mul_sum]
  simp only [Finset.sum_const_zero,add_zero]
  unfold q
  ring

theorem every_good_last_bit_charge (a p : ℝ) (h : a^2+p^2=1) (n : ℕ) :
    goodCharge a p (n+1)=2*a*p*successMass a p n false := by
  induction n with
  | zero => simp [first_good_last_bit_charge_zero,successMass,Word,firstLabel]
  | succ n ih =>
    rw [good_last_bit_charge_recursion,ih,every_normalized_raw_last_bit_charge a p h,
      success_mass_recursion,complete_mass a p h]
    ring

theorem actual_four_pair_good_charge (a p : ℝ) (h : a^2+p^2=1) :
    goodCharge a p 4=a*p*(1-(q a p)^3) := by
  rw [every_good_last_bit_charge a p h 3]
  have hs := (exact_fair_success_weights a p h 3).1
  rw [hs]
  ring
end
end D0.Research.RetainedRecordAdmission

set_option autoImplicit false
set_option linter.unusedSectionVars false
namespace D0.Research.RetainedRecordAdmission
noncomputable section
open Matrix
open scoped BigOperators Kronecker
open D0.Research.GoldenCoherentAmplification D0.Research.GoldenProgramCompilation

/-- The flip probe on a retained bit, in the actual system/record basis. -/
def archiveX : Matrix (Fin 4) (Fin 4) ℝ :=
  !![0,1,0,0;1,0,0,0;0,0,0,1;0,0,1,0]

theorem literal_retained_copy_preserves_archive_flip :
    retainedCopy*archiveX=archiveX*retainedCopy := by
  ext i j; fin_cases i <;> fin_cases j <;>
    norm_num [retainedCopy,archiveX,Matrix.mul_apply,Fin.sum_univ_succ]

theorem native_active_golden_gate_preserves_archive_flip (a p : ℝ) :
    goldenSystemGate a p*archiveX=archiveX*goldenSystemGate a p := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [goldenSystemGate,archiveX,Matrix.mul_apply,Fin.sum_univ_succ]

theorem actual_full_recording_step_preserves_archive_flip (a p : ℝ) :
    D0.Representation.GoldenCoherentMemory.fullStep a p*archiveX=
      archiveX*D0.Representation.GoldenCoherentMemory.fullStep a p := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [D0.Representation.GoldenCoherentMemory.fullStep,archiveX,
      Matrix.mul_apply,Fin.sum_univ_succ]

theorem coherent_old_record_gate_breaks_archive_flip (a p : ℝ) (hp : p≠0) :
    goldenRecordGate a p*archiveX≠archiveX*goldenRecordGate a p := by
  intro h
  have he := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 0 0) h
  simp [goldenRecordGate,archiveX,Matrix.mul_apply,Fin.sum_univ_succ] at he
  exact hp (by linarith)

section WholeWord
variable {ι : Type*} [Fintype ι] [DecidableEq ι]
def matrixWord : List (Matrix ι ι ℝ) → Matrix ι ι ℝ
  | [] => 1
  | U::w => U*matrixWord w

theorem commutation_survives_every_composed_word (w : List (Matrix ι ι ℝ))
    (X : Matrix ι ι ℝ) (hw : ∀ U∈w,U*X=X*U) :
    matrixWord w*X=X*matrixWord w := by
  induction w with
  | nil => simp [matrixWord]
  | cons U w ih =>
    have ht : ∀ V∈w,V*X=X*V := by intro V h; exact hw V (by simp [h])
    simp only [matrixWord]
    calc U*matrixWord w*X=U*(X*matrixWord w) := by rw [mul_assoc,ih ht]
         _ = X*(U*matrixWord w) := by rw [← mul_assoc,hw U (by simp),mul_assoc]

theorem complete_orthogonality_survives_every_word (w : List (Matrix ι ι ℝ))
    (hw : ∀ U∈w,U.transpose*U=1) : (matrixWord w).transpose*matrixWord w=1 := by
  induction w with
  | nil => simp [matrixWord]
  | cons U w ih =>
    have ht : ∀ V∈w,V.transpose*V=1 := by intro V h; exact hw V (by simp [h])
    rw [matrixWord,Matrix.transpose_mul]
    calc (matrixWord w).transpose*U.transpose*(U*matrixWord w)=
         (matrixWord w).transpose*(U.transpose*U)*matrixWord w := by simp [mul_assoc]
         _ = 1 := by rw [hw U (by simp)]; simpa using ih ht

theorem symmetric_probe_commutation_survives_reversal (U X : Matrix ι ι ℝ)
    (hX : X.transpose=X) (hU : U*X=X*U) : U.transpose*X=X*U.transpose := by
  have h := congrArg Matrix.transpose hU
  simpa only [Matrix.transpose_mul,hX] using h.symm

def charge (X : Matrix ι ι ℝ) (x : ι → ℝ) : ℝ := dotProduct x (X.mulVec x)

theorem every_complete_commuting_step_preserves_charge (U X : Matrix ι ι ℝ)
    (hU : U.transpose*U=1) (hC : U*X=X*U) (x : ι → ℝ) :
    charge X (U.mulVec x)=charge X x := by
  unfold charge
  have he : X.mulVec (U.mulVec x)=U.mulVec (X.mulVec x) := by
    rw [mulVec_mulVec,← hC,mulVec_mulVec]
  rw [he]
  have h := dotProduct_transpose_mulVec U x (U.mulVec (X.mulVec x))
  rw [mulVec_mulVec,hU,one_mulVec] at h
  calc _ = dotProduct (U.mulVec (X.mulVec x)) (U.mulVec x) := dotProduct_comm _ _
       _ = _ := h.symm

theorem all_length_whole_word_charge_is_unchanged (w : List (Matrix ι ι ℝ))
    (X : Matrix ι ι ℝ) (hw : ∀ U∈w,U.transpose*U=1 ∧ U*X=X*U) (x : ι → ℝ) :
    charge X ((matrixWord w).mulVec x)=charge X x := by
  exact every_complete_commuting_step_preserves_charge _ _
    (complete_orthogonality_survives_every_word _ (fun U h => (hw U h).1))
    (commutation_survives_every_composed_word _ _ (fun U h => (hw U h).2)) x
end WholeWord

section ControlledRecording
variable {A R : Type*} [Fintype A] [DecidableEq A] [AddCommGroup R]
  [Fintype R] [DecidableEq R]
/-- Translate a retained record by a supplied group label. -/
def translateRecord (t : R) : Equiv.Perm (A × R) where
  toFun x := (x.1,x.2+t)
  invFun x := (x.1,x.2-t)
  left_inv := by intro ⟨a,r⟩; simp
  right_inv := by intro ⟨a,r⟩; simp
/-- One-way reversible registration; the active label controls the archive update. -/
def controlledRecord (f : A → R) : Equiv.Perm (A × R) where
  toFun x := (x.1,x.2+f x.1)
  invFun x := (x.1,x.2-f x.1)
  left_inv := by intro ⟨a,r⟩; simp
  right_inv := by intro ⟨a,r⟩; simp

theorem all_addressed_one_way_recordings_commute_with_old_translations (f : A → R) (t : R) :
    (controlledRecord f).trans (translateRecord t)=
      (translateRecord t).trans (controlledRecord f) := by
  apply Equiv.ext
  rintro ⟨a,r⟩
  change (a,(r+f a)+t)=(a,(r+t)+f a)
  congr 1
  abel

theorem actual_controlled_record_matrix_preserves_every_archive_translation
    (f : A → R) (t : R) :
    (controlledRecord f).permMatrix ℝ*(translateRecord t).permMatrix ℝ=
      (translateRecord t).permMatrix ℝ*(controlledRecord f).permMatrix ℝ := by
  rw [← Matrix.permMatrix_mul,← Matrix.permMatrix_mul]
  congr 1
  apply Equiv.ext
  rintro ⟨a,r⟩
  change (a,(r+f a)+t)=(a,(r+t)+f a)
  congr 1
  abel


theorem every_active_operator_preserves_every_old_archive_probe
    (U : Matrix A A ℝ) (X : Matrix R R ℝ) :
    (U ⊗ₖ (1 : Matrix R R ℝ))*((1 : Matrix A A ℝ) ⊗ₖ X)=
      ((1 : Matrix A A ℝ) ⊗ₖ X)*(U ⊗ₖ (1 : Matrix R R ℝ)) := by
  rw [← Matrix.mul_kronecker_mul,← Matrix.mul_kronecker_mul]
  simp

theorem every_retained_recording_matrix_is_complete_orthogonal (f : A → R) :
    ((controlledRecord f).permMatrix ℝ).transpose*(controlledRecord f).permMatrix ℝ=1 := by
  rw [Matrix.transpose_permMatrix,← Matrix.permMatrix_mul]
  simp

theorem active_orthogonality_retains_the_full_archive (U : Matrix A A ℝ)
    (hU : U.transpose*U=1) :
    (U ⊗ₖ (1 : Matrix R R ℝ)).transpose*(U ⊗ₖ (1 : Matrix R R ℝ))=1 := by
  rw [← Matrix.kroneckerMap_transpose,← Matrix.mul_kronecker_mul,hU]
  simp




def recordShift (t : R) : Equiv.Perm R where
  toFun r := r+t
  invFun r := r-t
  left_inv := by intro r; simp
  right_inv := by intro r; simp

theorem archive_translation_is_the_full_tensor_probe (t : R) :
    (translateRecord (A:=A) t).permMatrix ℝ=
      (1 : Matrix A A ℝ) ⊗ₖ (recordShift t).permMatrix ℝ := by
  ext ⟨a,r⟩ ⟨b,s⟩
  by_cases hab : a=b
  · subst b
    simp [Equiv.Perm.permMatrix,PEquiv.toMatrix_apply,Equiv.toPEquiv_apply,
      translateRecord,recordShift,Matrix.kroneckerMap_apply,Matrix.one_apply]
  · simp [Equiv.Perm.permMatrix,PEquiv.toMatrix_apply,Equiv.toPEquiv_apply,
      translateRecord,recordShift,Matrix.kroneckerMap_apply,Matrix.one_apply,hab]

/-- The generators are specified before deriving the conserved charge. -/
inductive OneWayGenerator : Matrix (A × R) (A × R) ℝ → Prop
  | active (U : Matrix A A ℝ) (hU : U.transpose*U=1) :
      OneWayGenerator (U ⊗ₖ (1 : Matrix R R ℝ))
  | recording (f : A → R) : OneWayGenerator ((controlledRecord f).permMatrix ℝ)

theorem every_one_way_generator_preserves_its_retained_translation
    (U : Matrix (A × R) (A × R) ℝ) (hU : OneWayGenerator U) (t : R) :
    U.transpose*U=1 ∧ U*(translateRecord (A:=A) t).permMatrix ℝ=
      (translateRecord (A:=A) t).permMatrix ℝ*U := by
  cases hU with
  | active V hv =>
    refine ⟨active_orthogonality_retains_the_full_archive V hv,?_⟩
    rw [archive_translation_is_the_full_tensor_probe]
    exact every_active_operator_preserves_every_old_archive_probe V _
  | recording f => exact ⟨every_retained_recording_matrix_is_complete_orthogonal f,
      actual_controlled_record_matrix_preserves_every_archive_translation f t⟩

theorem every_length_of_the_explicit_one_way_class_keeps_the_old_charge
    (w : List (Matrix (A × R) (A × R) ℝ))
    (hw : ∀ U∈w,OneWayGenerator U) (t : R) (x : A × R → ℝ) :
    charge ((translateRecord (A:=A) t).permMatrix ℝ) ((matrixWord w).mulVec x)=
      charge ((translateRecord (A:=A) t).permMatrix ℝ) x := by
  exact all_length_whole_word_charge_is_unchanged w _
    (fun U h => every_one_way_generator_preserves_its_retained_translation U (hw U h) t) x

end ControlledRecording

section Quantitative
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
def hilbertCharge (T : E →L[ℝ] E) (x : E) : ℝ := inner ℝ x (T x)

theorem unit_state_charge_difference_controls_full_error (T : E →L[ℝ] E)
    (hT : ∀ x,‖T x‖=‖x‖) (x y : E) (hx : ‖x‖=1) (hy : ‖y‖=1) :
    |hilbertCharge T x-hilbertCharge T y|≤2*‖x-y‖ := by
  have he : hilbertCharge T x-hilbertCharge T y=
      inner ℝ (x-y) (T x)+inner ℝ y (T (x-y)) := by
    simp [hilbertCharge,inner_sub_left,inner_sub_right]
  rw [he]
  have h1 := abs_real_inner_le_norm (x-y) (T x)
  have h2 := abs_real_inner_le_norm y (T (x-y))
  rw [hT,hx,mul_one] at h1
  rw [hT,hy,one_mul] at h2
  exact (abs_add_le _ _).trans (by linarith)

theorem preserved_charge_has_a_positive_uniform_state_floor
    (T : E →L[ℝ] E) (hT : ∀ x,‖T x‖=‖x‖)
    (x y : E) (c d : ℝ) (hx : ‖x‖=1) (hy : ‖y‖=1)
    (hcx : hilbertCharge T x=c) (hdy : hilbertCharge T y=d) :
    |c-d|/2≤‖x-y‖ := by
  have h := unit_state_charge_difference_controls_full_error T hT x y hx hy
  rw [hcx,hdy] at h
  linarith
end Quantitative
end
end D0.Research.RetainedRecordAdmission

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.RetainedRecordAdmission
noncomputable section
open Matrix
open scoped BigOperators
open D0.Research.GoldenHistoryPreparation D0.Research.GoldenProgramCompilation
open D0.Research.GoldenCoherentAmplification

theorem common_raw_record_is_product_of_same_accepted_streams (a p : ℝ)
    (n m : ℕ) (w : Fin m → Word n) :
    commonRawRecord a p n m w=∏ i,acceptedRaw a p n (w i) := by
  by_cases h : ∀ i,firstLabel (w i)=some false
  · simp [commonRawRecord,acceptedRaw,h]
  · have hn := h
    push Not at hn
    obtain ⟨i,hi⟩ := hn
    rw [commonRawRecord,if_neg h]
    exact (Finset.prod_eq_zero (Finset.mem_univ i) (by simp [acceptedRaw,hi])).symm

def oldRawBitFlip (w : Fin 5 → Word 4) : Fin 5 → Word 4 :=
  Function.update w 0 (flipLast (w 0))

theorem old_raw_bit_flip_is_complete_involution : Function.Involutive oldRawBitFlip := by
  intro w
  funext i
  by_cases hi : i=0
  · subst i
    simpa [oldRawBitFlip] using flip_last_is_retained_involution 4 (w 0)
  · simp [oldRawBitFlip,Function.update_of_ne hi]

theorem same_record_factor_has_exact_old_bit_cross_sum (a p : ℝ) :
    (∑ w : Fin 5 → Word 4, commonRawRecord a p 4 5 w*
      commonRawRecord a p 4 5 (oldRawBitFlip w))=
      goodCharge a p 4*(successMass a p 4 false)^4 := by
  let F (i : Fin 5) (z : Word 4) :=
    if i=0 then acceptedRaw a p 4 z*acceptedRaw a p 4 (flipLast z)
    else acceptedRaw a p 4 z^2
  have he (w : Fin 5 → Word 4) : commonRawRecord a p 4 5 w*
      commonRawRecord a p 4 5 (oldRawBitFlip w)=∏ i,F i (w i) := by
    rw [common_raw_record_is_product_of_same_accepted_streams,
      common_raw_record_is_product_of_same_accepted_streams,← Finset.prod_mul_distrib]
    apply Finset.prod_congr rfl
    intro i _
    by_cases hi : i=0
    · subst i; simp [F,oldRawBitFlip]
    · simp [F,oldRawBitFlip,hi,Function.update_of_ne hi,pow_two]
  simp_rw [he]
  rw [← Fintype.prod_sum]
  rw [Fin.prod_univ_succ]
  simp [F,goodCharge,accepted_raw_mass_is_owned_success_mass]

theorem common_five_stream_mass_is_same_success_fifth_power (a p : ℝ) :
    commonRecordMass a p 4 5=(successMass a p 4 false)^5 := by
  unfold commonRecordMass
  rw [complete_disjoint_record_code_mass]
  simp

theorem complete_common_record_has_exact_old_bit_charge (a p : ℝ)
    (hs : 0<successMass a p 4 false) :
    (∑ w : Fin 5 → Word 4, commonRecord a p 4 5 w*
      commonRecord a p 4 5 (oldRawBitFlip w))=
      goodCharge a p 4/successMass a p 4 false := by
  have hm : 0<commonRecordMass a p 4 5 := by
    rw [common_five_stream_mass_is_same_success_fifth_power]; positivity
  have hsqrt := Real.sq_sqrt (le_of_lt hm)
  calc
    _ = (∑ w,commonRawRecord a p 4 5 w*
        commonRawRecord a p 4 5 (oldRawBitFlip w))/(Real.sqrt (commonRecordMass a p 4 5))^2 := by
      rw [Finset.sum_div]
      apply Finset.sum_congr rfl
      intro w _
      unfold commonRecord
      ring
    _ = goodCharge a p 4*(successMass a p 4 false)^4/(successMass a p 4 false)^5 := by
      rw [hsqrt,same_record_factor_has_exact_old_bit_cross_sum,
        common_five_stream_mass_is_same_success_fifth_power]
    _ = _ := by field_simp

def archiveGap (a p : ℝ) : ℝ :=
  2*a*p*(q a p)^3/(1+q a p+(q a p)^2+(q a p)^3)

theorem native_accepted_four_pair_mass_is_positive (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) : 0<successMass a p 4 false := by
  rw [(exact_fair_success_weights a p (by linarith : a^2+p^2=1) 4).1]
  have h := (golden_four_pair_good_weight a p ha hp hp0).1
  linarith

theorem native_old_archive_coherence_gap_is_strictly_positive (a p : ℝ)
    (ha0 : 0<a) (hp0 : 0<p) : 0<archiveGap a p := by
  have hq : 0<q a p := by unfold q; positivity
  unfold archiveGap
  positivity

theorem raw_and_actual_common_record_charges_differ_by_native_gap (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) :
    2*a*p-(∑ w : Fin 5 → Word 4,commonRecord a p 4 5 w*
      commonRecord a p 4 5 (oldRawBitFlip w))=archiveGap a p := by
  have hnorm : a^2+p^2=1 := by linarith
  have hs := native_accepted_four_pair_mass_is_positive a p ha hp hp0
  rw [complete_common_record_has_exact_old_bit_charge a p hs,
    actual_four_pair_good_charge a p hnorm,(exact_fair_success_weights a p hnorm 4).1]
  have hg : 0<1+q a p+(q a p)^2+(q a p)^3 := by unfold q; positivity
  have hm : 0<1-(q a p)^4 := by
    have h := (golden_four_pair_good_weight a p ha hp hp0).1; linarith
  unfold archiveGap
  field_simp
  ring

theorem actual_p0_retained_archive_charge_has_fixed_positive_defect :
    let p := D0.primitiveRoot
    let a := Real.sqrt p
    0<archiveGap a p ∧
      2*a*p-(∑ w : Fin 5 → Word 4,commonRecord a p 4 5 w*
        commonRecord a p 4 5 (oldRawBitFlip w))=archiveGap a p := by
  dsimp
  have hp := D0.Representation.GoldenOrderInterferometer.primitive_positive
  exact ⟨native_old_archive_coherence_gap_is_strictly_positive _ _
    (Real.sqrt_pos.mpr hp) hp,raw_and_actual_common_record_charges_differ_by_native_gap _ _
      (Real.sq_sqrt (le_of_lt hp)) D0.primitive_root_satisfies hp⟩
section Readings
variable {Ω B : Type*} [Fintype Ω] [DecidableEq Ω] [Fintype B] [DecidableEq B]

theorem tensor_old_record_charge_ignores_the_unit_active_ray
    (u : B → ℝ) (η : Ω → ℝ) (τ : Ω → Ω) (hu : ∑ b,u b^2=1) :
    (∑ s : Ω × B,(u s.2*η s.1)*(u s.2*η (τ s.1)))=
      ∑ w,η w*η (τ w) := by
  rw [Fintype.sum_prod_type]
  apply Finset.sum_congr rfl
  intro w _
  calc
    _ = (η w*η (τ w))*(∑ b,u b^2) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro b _
      ring
    _ = _ := by rw [hu]; ring
end Readings

theorem actual_uniform_code_has_unit_complete_mass (S : Finset (Fin 5 → Bool))
    (hs : 0<S.card) : (∑ b,uniformCode S b^2)=1 := by
  have hsr : 0<(S.card : ℝ) := by exact_mod_cast hs
  have he : (∑ b,uniformCode S b^2)=
      (S.card : ℝ)/(Real.sqrt (S.card : ℝ))^2 := by
    simp [uniformCode,ite_pow,Finset.sum_ite_mem,div_eq_mul_inv]
  rw [he,Real.sq_sqrt (le_of_lt hsr)]
  exact div_self (ne_of_gt hsr)

theorem all_actual_scene_targets_need_the_same_changed_archive_charge
    (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) (v : Fin 33) :
    (∑ s : (Fin 5 → Word 4) × (Fin 5 → Bool),
      (uniformCode (sceneAcceptedCodes v) s.2*commonRecord a p 4 5 s.1)*
      (uniformCode (sceneAcceptedCodes v) s.2*commonRecord a p 4 5 (oldRawBitFlip s.1)))=
      2*a*p-archiveGap a p := by
  have hd := actual_scene_accepted_codes_exact_degrees v
  have hs : 0<(sceneAcceptedCodes v).card := by rcases hd with h|h|h <;> omega
  rw [tensor_old_record_charge_ignores_the_unit_active_ray _ _ _
    (actual_uniform_code_has_unit_complete_mass _ hs)]
  have h := raw_and_actual_common_record_charges_differ_by_native_gap a p ha hp hp0
  linarith

def allEqualFour : Word 4 :=
  ((true,true),((true,true),((true,true),((true,true),()))))
def flipOnRoute (s : Word 4 × Bool) : Word 4 × Bool := (flipLast s.1,s.2)

theorem actual_first_odd_route_breaks_old_record_flip :
    (fun s : Word 4 × Bool => route 4 (flipOnRoute s))≠
      (fun s : Word 4 × Bool => flipOnRoute (route 4 s)) := by
  intro h
  have he := congrArg (fun f : (Word 4 × Bool) → (Word 4 × Bool) =>
    (f (allEqualFour,false)).2) h
  norm_num [allEqualFour,flipOnRoute,flipLast,route,copyLabel,controlledFlip,
    firstBit,firstLabel,flipFirst,Function.Involutive.toPerm] at he
end
end D0.Research.RetainedRecordAdmission

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.RetainedRecordAdmission
noncomputable section
open Matrix
open scoped BigOperators
open D0.Research.GoldenHistoryPreparation D0.Research.GoldenCoherentAmplification
open D0.Research.GoldenProgramCompilation D0.Research.GoldenFixedCalibration
abbrev Archive := Fin 5 → Word 4
abbrev Label := Fin 5 → Bool
abbrev Complete := Archive × Label

def freshRaw (a p : ℝ) (w : Archive) : ℝ := ∏ i,amplitude a p (w i)
def blankLabel (b : Label) : ℝ := if b=(fun _ => false) then 1 else 0
def freshState (a p : ℝ) (s : Complete) : ℝ := freshRaw a p s.1*blankLabel s.2
def targetState (a p : ℝ) (v : Fin 33) (s : Complete) : ℝ :=
  commonRecord a p 4 5 s.1*uniformCode (sceneAcceptedCodes v) s.2

theorem fresh_complete_raw_record_is_normalized (a p : ℝ) (hn : a^2+p^2=1) :
    (∑ w,freshRaw a p w^2)=1 := by
  unfold freshRaw
  simp_rw [← Finset.prod_pow]
  rw [← Fintype.prod_sum (fun (_ : Fin 5) (z : Word 4) => amplitude a p z^2)]
  simp [complete_mass a p hn]

theorem fresh_complete_record_has_native_old_bit_charge (a p : ℝ) (hn : a^2+p^2=1) :
    (∑ w,freshRaw a p w*freshRaw a p (oldRawBitFlip w))=2*a*p := by
  let F (i : Fin 5) (z : Word 4) :=
    if i=0 then amplitude a p z*amplitude a p (flipLast z) else amplitude a p z^2
  have he (w : Archive) : freshRaw a p w*freshRaw a p (oldRawBitFlip w)=∏ i,F i (w i) := by
    unfold freshRaw
    rw [← Finset.prod_mul_distrib]
    apply Finset.prod_congr rfl
    intro i _
    by_cases hi : i=0
    · subst i; simp [F,oldRawBitFlip]
    · simp [F,oldRawBitFlip,hi,Function.update_of_ne hi,pow_two]
  simp_rw [he]
  rw [← Fintype.prod_sum,Fin.prod_univ_succ]
  simp [F,complete_mass a p hn]
  exact every_normalized_raw_last_bit_charge a p hn 3

theorem blank_label_is_complete_unit_mass : (∑ b,blankLabel b^2)=1 := by
  simp [blankLabel,ite_pow]

section Product
variable {Ω B : Type*} [Fintype Ω] [DecidableEq Ω] [Fintype B] [DecidableEq B]
theorem complete_tensor_state_keeps_both_unit_factors (u : B → ℝ) (η : Ω → ℝ)
    (hu : ∑ b,u b^2=1) (hη : ∑ w,η w^2=1) :
    (∑ s : Ω × B,(η s.1*u s.2)^2)=1 := by
  rw [Fintype.sum_prod_type]
  simp_rw [mul_pow,← Finset.mul_sum,hu,mul_one]
  exact hη
end Product

theorem full_fresh_native_state_has_unit_mass (a p : ℝ) (hn : a^2+p^2=1) :
    (∑ s,freshState a p s^2)=1 := by
  exact complete_tensor_state_keeps_both_unit_factors blankLabel (freshRaw a p)
    blank_label_is_complete_unit_mass (fresh_complete_raw_record_is_normalized a p hn)

theorem full_actual_target_has_unit_mass (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) (v : Fin 33) :
    (∑ s,targetState a p v s^2)=1 := by
  have hd := actual_scene_accepted_codes_exact_degrees v
  have hs : 0<(sceneAcceptedCodes v).card := by rcases hd with h|h|h <;> omega
  exact complete_tensor_state_keeps_both_unit_factors _ _
    (actual_uniform_code_has_unit_complete_mass _ hs)
    (common_record_has_complete_unit_mass _ _ _ _
      (actual_common_record_mass_positive a p ha hp hp0))

def completeFlip : Equiv.Perm Complete where
  toFun s := (oldRawBitFlip s.1,s.2)
  invFun s := (oldRawBitFlip s.1,s.2)
  left_inv := by intro ⟨w,b⟩; change (oldRawBitFlip (oldRawBitFlip w),b)=(w,b); rw [old_raw_bit_flip_is_complete_involution w]
  right_inv := by intro ⟨w,b⟩; change (oldRawBitFlip (oldRawBitFlip w),b)=(w,b); rw [old_raw_bit_flip_is_complete_involution w]
def completeProbe : Matrix Complete Complete ℝ := completeFlip.permMatrix ℝ

theorem actual_complete_flip_probe_is_orthogonal : completeProbe.transpose*completeProbe=1 := by
  rw [completeProbe,Matrix.transpose_permMatrix,← Matrix.permMatrix_mul]
  simp

theorem native_probe_charge_is_the_complete_coordinate_reading (x : Complete → ℝ) :
    charge completeProbe x=∑ s,x s*x (completeFlip s) := by
  simp [charge,completeProbe,Matrix.permMatrix_mulVec,dotProduct]

theorem full_fresh_state_has_literal_old_archive_charge (a p : ℝ) (hn : a^2+p^2=1) :
    charge completeProbe (freshState a p)=2*a*p := by
  rw [native_probe_charge_is_the_complete_coordinate_reading]
  have h := tensor_old_record_charge_ignores_the_unit_active_ray blankLabel (freshRaw a p)
    oldRawBitFlip blank_label_is_complete_unit_mass
  simp only [freshState,completeFlip] at *
  simp_rw [mul_comm (freshRaw a p _) (blankLabel _)]
  exact h.trans (fresh_complete_record_has_native_old_bit_charge a p hn)

theorem all_33_actual_targets_have_the_required_changed_charge (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) (v : Fin 33) :
    charge completeProbe (targetState a p v)=2*a*p-archiveGap a p := by
  rw [native_probe_charge_is_the_complete_coordinate_reading]
  unfold targetState
  simp only [completeFlip]
  simp_rw [mul_comm (commonRecord a p 4 5 _) (uniformCode _ _)]
  exact all_actual_scene_targets_need_the_same_changed_archive_charge a p ha hp hp0 v

section HilbertBinding
variable {ι : Type*} [Fintype ι] [DecidableEq ι]
theorem hilbert_and_complete_coordinate_charge_are_identical
    (X : Matrix ι ι ℝ) (x : ι → ℝ) :
    hilbertCharge (matrixOperator X) (realHilbert x)=charge X x := by
  unfold hilbertCharge
  rw [matrix_operator_acts_on_every_complete_coordinate]
  simp [PiLp.inner_apply,realHilbert,charge,dotProduct,mul_comm]

theorem complete_unit_mass_is_unit_hilbert_norm (x : ι → ℝ)
    (hx : ∑ i,x i^2=1) : ‖realHilbert x‖=1 := by
  have h := real_hilbert_norm_sq_is_complete_weight x
  change ‖realHilbert x‖^2=∑ i,x i^2 at h
  rw [hx] at h
  have hn := norm_nonneg (realHilbert x)
  nlinarith
end HilbertBinding

theorem every_complete_commuting_preparation_has_native_positive_error_floor
    (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) (ha0 : 0<a)
    (v : Fin 33) (U : Matrix Complete Complete ℝ)
    (hU : U.transpose*U=1) (hC : U*completeProbe=completeProbe*U) :
    archiveGap a p/2≤‖realHilbert (U.mulVec (freshState a p))-
      realHilbert (targetState a p v)‖ := by
  have hn : a^2+p^2=1 := by linarith
  have hx := full_fresh_native_state_has_unit_mass a p hn
  have hy := full_actual_target_has_unit_mass a p ha hp hp0 v
  have hxU : ∑ s,(U.mulVec (freshState a p) s)^2=1 := by
    have h := whole_real_orthogonal_operator_preserves_weight U hU (freshState a p)
    change (∑ s,(U.mulVec (freshState a p) s)^2)=∑ s,freshState a p s^2 at h
    exact h.trans hx
  have hcx : hilbertCharge (matrixOperator completeProbe) (realHilbert (U.mulVec (freshState a p)))=2*a*p := by
    rw [hilbert_and_complete_coordinate_charge_are_identical,
      every_complete_commuting_step_preserves_charge U completeProbe hU hC,
      full_fresh_state_has_literal_old_archive_charge a p hn]
  have hdy : hilbertCharge (matrixOperator completeProbe) (realHilbert (targetState a p v))=
      2*a*p-archiveGap a p := by
    rw [hilbert_and_complete_coordinate_charge_are_identical]
    exact all_33_actual_targets_have_the_required_changed_charge a p ha hp hp0 v
  have h := preserved_charge_has_a_positive_uniform_state_floor
    (matrixOperator completeProbe)
    (whole_real_orthogonal_operator_is_hilbert_isometry _ actual_complete_flip_probe_is_orthogonal)
    _ _ _ _ (complete_unit_mass_is_unit_hilbert_norm _ hxU)
    (complete_unit_mass_is_unit_hilbert_norm _ hy) hcx hdy
  have hg := native_old_archive_coherence_gap_is_strictly_positive a p ha0 hp0
  have he : |2*a*p-(2*a*p-archiveGap a p)|=archiveGap a p := by
    rw [show 2*a*p-(2*a*p-archiveGap a p)=archiveGap a p by ring,abs_of_pos hg]
  rwa [he] at h
end
end D0.Research.RetainedRecordAdmission

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.RetainedRecordAdmission
noncomputable section
open Matrix Filter Topology
open D0.Research.GoldenProgramCompilation

section Extension
variable {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [NormedAddCommGroup F] [InnerProductSpace ℝ F]

theorem every_whole_isometric_extension_retains_the_old_archive_charge
    (J : E →ₗᵢ[ℝ] F) (T : E →L[ℝ] E) (S : F →L[ℝ] F)
    (hJ : ∀ x,S (J x)=J (T x)) (x : E) :
    hilbertCharge S (J x)=hilbertCharge T x := by
  unfold hilbertCharge
  rw [hJ]
  exact J.inner_map_map x (T x)

theorem every_whole_isometric_commuting_dynamics_preserves_charge
    (S U : F →L[ℝ] F) (hU : ∀ x,‖U x‖=‖x‖)
    (hC : ∀ x,S (U x)=U (S x)) (x : F) :
    hilbertCharge S (U x)=hilbertCharge S x := by
  let e : F →ₗᵢ[ℝ] F := {toLinearMap := U.toLinearMap, norm_map' := hU}
  unfold hilbertCharge
  rw [hC]
  exact e.inner_map_map x (S x)

theorem full_archive_error_floor_survives_every_complete_extension
    (J : E →ₗᵢ[ℝ] F) (T : E →L[ℝ] E) (S U : F →L[ℝ] F)
    (hJ : ∀ x,S (J x)=J (T x)) (hS : ∀ x,‖S x‖=‖x‖)
    (hU : ∀ x,‖U x‖=‖x‖) (hC : ∀ x,S (U x)=U (S x))
    (x y : E) (hx : ‖x‖=1) (hy : ‖y‖=1) (δ : ℝ)
    (hδ : 0≤δ) (hgap : hilbertCharge T x-hilbertCharge T y=δ) :
    δ/2≤‖U (J x)-J y‖ := by
  have hu : ‖U (J x)‖=1 := by rw [hU,J.norm_map,hx]
  have ht : ‖J y‖=1 := by rw [J.norm_map,hy]
  have hc : hilbertCharge S (U (J x))=hilbertCharge T x := by
    rw [every_whole_isometric_commuting_dynamics_preserves_charge S U hU hC,
      every_whole_isometric_extension_retains_the_old_archive_charge J T S hJ]
  have hd : hilbertCharge S (J y)=hilbertCharge T y :=
    every_whole_isometric_extension_retains_the_old_archive_charge J T S hJ y
  have h := preserved_charge_has_a_positive_uniform_state_floor S hS _ _ _ _ hu ht hc hd
  rwa [hgap,abs_of_nonneg hδ] at h
end Extension

section Coupling
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

theorem actual_charge_change_is_bounded_by_the_complete_commutator
    (S U : E →L[ℝ] E) (hU : ∀ x,‖U x‖=‖x‖) (x : E) (hx : ‖x‖=1) :
    |hilbertCharge S (U x)-hilbertCharge S x|≤‖S.comp U-U.comp S‖ := by
  let e : E →ₗᵢ[ℝ] E := {toLinearMap := U.toLinearMap, norm_map' := hU}
  have hp : inner ℝ (U x) (U (S x))=inner ℝ x (S x) := e.inner_map_map x (S x)
  have he : hilbertCharge S (U x)-hilbertCharge S x=
      inner ℝ (U x) ((S.comp U-U.comp S) x) := by
    simp [hilbertCharge,inner_sub_right,hp]
  rw [he]
  have hn := abs_real_inner_le_norm (U x) ((S.comp U-U.comp S) x)
  rw [hU,hx,one_mul] at hn
  have hc := ContinuousLinearMap.le_opNorm (S.comp U-U.comp S) x
  rw [hx,mul_one] at hc
  exact hn.trans hc

theorem native_target_error_requires_quantitatively_noncommuting_archive_actuation
    (S U : E →L[ℝ] E) (hS : ∀ x,‖S x‖=‖x‖) (hU : ∀ x,‖U x‖=‖x‖)
    (x y : E) (hx : ‖x‖=1) (hy : ‖y‖=1) (δ : ℝ)
    (hgap : hilbertCharge S x-hilbertCharge S y=δ) :
    |δ|≤2*‖U x-y‖+‖S.comp U-U.comp S‖ := by
  have hu : ‖U x‖=1 := (hU x).trans hx
  have h1 := unit_state_charge_difference_controls_full_error S hS (U x) y hu hy
  have h2 := actual_charge_change_is_bounded_by_the_complete_commutator S U hU x hx
  have he : hilbertCharge S x-hilbertCharge S y=
      -(hilbertCharge S (U x)-hilbertCharge S x)+(hilbertCharge S (U x)-hilbertCharge S y) := by ring
  rw [← hgap,he]
  have h := abs_add_le (-(hilbertCharge S (U x)-hilbertCharge S x))
    (hilbertCharge S (U x)-hilbertCharge S y)
  rw [abs_neg] at h
  exact h.trans (by linarith)
end Coupling

theorem positive_archive_floor_excludes_every_vanishing_error_schedule
    (e : ℕ → ℝ) (δ : ℝ) (hδ : 0<δ) (he : ∀ n,δ/2≤e n) :
    ¬ Tendsto e atTop (nhds 0) := by
  intro h
  have hf : ∀ᶠ n in atTop,e n<δ/2 := (tendsto_order.mp h).2 (δ/2) (by linarith)
  obtain ⟨n,hn⟩ := hf.exists
  exact (not_lt_of_ge (he n)) hn

theorem actual_p0_commuting_preparations_never_converge_to_any_scene_target
    (v : Fin 33) (U : ℕ → Matrix Complete Complete ℝ)
    (hU : ∀ n,(U n).transpose*U n=1 ∧ U n*completeProbe=completeProbe*U n) :
    ¬ Tendsto (fun n => ‖realHilbert ((U n).mulVec (freshState
      (Real.sqrt D0.primitiveRoot) D0.primitiveRoot))-
      realHilbert (targetState (Real.sqrt D0.primitiveRoot) D0.primitiveRoot v)‖)
      atTop (nhds 0) := by
  have hp := D0.Representation.GoldenOrderInterferometer.primitive_positive
  exact positive_archive_floor_excludes_every_vanishing_error_schedule _ _
    (native_old_archive_coherence_gap_is_strictly_positive _ _ (Real.sqrt_pos.mpr hp) hp)
    (fun n => every_complete_commuting_preparation_has_native_positive_error_floor _ _
      (Real.sq_sqrt (le_of_lt hp)) D0.primitive_root_satisfies hp (Real.sqrt_pos.mpr hp)
      v (U n) (hU n).1 (hU n).2)
end
end D0.Research.RetainedRecordAdmission

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.VerifiedArchiveActuation
noncomputable section
open Matrix Filter Topology
section Hilbert
variable {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [NormedAddCommGroup F] [InnerProductSpace ℝ F]

/-- Symmetry belongs to the outcome observable, rather than the dynamics. -/
theorem opposite_exact_outcomes_are_orthogonal
    (Z : E →L[ℝ] E) (hZ : ∀ u v, inner ℝ (Z u) v=inner ℝ u (Z v))
    (u v : E) (hu : Z u = -u) (hv : Z v = v) : inner ℝ u v=0 := by
  have h := hZ u v
  rw [hu,hv,inner_neg_left] at h
  linarith

theorem opposite_unit_outcomes_have_fixed_complete_distance
    (Z : E →L[ℝ] E) (hZ : ∀ u v, inner ℝ (Z u) v=inner ℝ u (Z v))
    (u v : E) (hu : Z u = -u) (hv : Z v = v)
    (hnu : ‖u‖=1) (hnv : ‖v‖=1) : ‖u-v‖^2=2 := by
  rw [norm_sub_sq_real,hnu,hnv,opposite_exact_outcomes_are_orthogonal Z hZ u v hu hv]
  norm_num

theorem old_probe_keeps_the_internal_outcome
    (S Z : E →L[ℝ] E) (hC : ∀ x,Z (S x)=S (Z x)) (u : E)
    (hu : Z u=u) : Z (S u)=S u := by rw [hC,hu]

/-- Exact binary truth forces an archive/output interaction, regardless of junk records. -/
theorem every_exact_complete_comparison_has_a_fixed_archive_commutator
    (S Z U : E →L[ℝ] E)
    (hS : ∀ x,‖S x‖=‖x‖) (hU : ∀ x,‖U x‖=‖x‖)
    (hZ : ∀ u v,inner ℝ (Z u) v=inner ℝ u (Z v))
    (hC : ∀ x,Z (S x)=S (Z x)) (x : E) (hx : ‖x‖=1)
    (h0 : Z (U x)=U x) (h1 : Z (U (S x)) = -(U (S x))) :
    ‖(U.comp S-S.comp U) x‖^2=2 := by
  change ‖U (S x)-S (U x)‖^2=2
  exact opposite_unit_outcomes_have_fixed_complete_distance Z hZ _ _ h1
    (old_probe_keeps_the_internal_outcome S Z hC _ h0)
    (by rw [hU,hS,hx]) (by rw [hS,hU,hx])

theorem every_exact_complete_comparison_requires_uniform_archive_actuation
    (S Z U : E →L[ℝ] E)
    (hS : ∀ x,‖S x‖=‖x‖) (hU : ∀ x,‖U x‖=‖x‖)
    (hZ : ∀ u v,inner ℝ (Z u) v=inner ℝ u (Z v))
    (hC : ∀ x,Z (S x)=S (Z x)) (x : E) (hx : ‖x‖=1)
    (h0 : Z (U x)=U x) (h1 : Z (U (S x)) = -(U (S x))) :
    Real.sqrt 2≤‖U.comp S-S.comp U‖ := by
  have he := every_exact_complete_comparison_has_a_fixed_archive_commutator S Z U hS hU hZ hC x hx h0 h1
  have hn := norm_nonneg ((U.comp S-S.comp U) x)
  have hs := Real.sq_sqrt (by norm_num : (0 : ℝ)≤2)
  have hp := Real.sqrt_nonneg (2 : ℝ)
  have hi : Real.sqrt 2=‖(U.comp S-S.comp U) x‖ := by nlinarith
  rw [hi]
  simpa [hx] using ContinuousLinearMap.le_opNorm (U.comp S-S.comp U) x

theorem no_commuting_complete_comparison_realizes_both_truth_values
    (S Z U : E →L[ℝ] E)
    (hS : ∀ x,‖S x‖=‖x‖) (hU : ∀ x,‖U x‖=‖x‖)
    (hZ : ∀ u v,inner ℝ (Z u) v=inner ℝ u (Z v))
    (hC : ∀ x,Z (S x)=S (Z x)) (x : E) (hx : ‖x‖=1)
    (h0 : Z (U x)=U x) (h1 : Z (U (S x)) = -(U (S x))) :
    U.comp S≠S.comp U := by
  intro h
  have he := every_exact_complete_comparison_has_a_fixed_archive_commutator S Z U hS hU hZ hC x hx h0 h1
  rw [h,sub_self] at he
  norm_num at he

/-- Quantitative output error, without adding a gate or a preferred implementation. -/
theorem approximate_opposite_unit_outcomes_control_their_inner_product
    (Z : E →L[ℝ] E) (hZ : ∀ u v,inner ℝ (Z u) v=inner ℝ u (Z v))
    (u v : E) (hnu : ‖u‖=1) (hnv : ‖v‖=1) :
    2*|inner ℝ u v|≤‖Z u+u‖+‖Z v-v‖ := by
  have he : 2*inner ℝ u v=inner ℝ (Z u+u) v-inner ℝ u (Z v-v) := by
    rw [inner_add_left,inner_sub_right,hZ]
    ring
  have ha := abs_sub (inner ℝ (Z u+u) v) (inner ℝ u (Z v-v))
  have hu := abs_real_inner_le_norm (Z u+u) v
  have hv := abs_real_inner_le_norm u (Z v-v)
  rw [hnu,one_mul] at hv
  rw [hnv,mul_one] at hu
  have hr : |2*inner ℝ u v|=2*|inner ℝ u v| := by rw [abs_mul]; norm_num
  rw [← hr,he]
  exact ha.trans (add_le_add hu hv)

theorem approximate_comparison_requires_nondiluting_archive_actuation
    (S Z U : E →L[ℝ] E)
    (hS : ∀ x,‖S x‖=‖x‖) (hU : ∀ x,‖U x‖=‖x‖)
    (hZ : ∀ u v,inner ℝ (Z u) v=inner ℝ u (Z v))
    (hC : ∀ x,Z (S x)=S (Z x)) (x : E) (hx : ‖x‖=1) :
    2-(‖Z (U (S x))+U (S x)‖+‖Z (U x)-U x‖)≤‖U.comp S-S.comp U‖^2 := by
  have hu : ‖U (S x)‖=1 := by rw [hU,hS,hx]
  have hv : ‖S (U x)‖=1 := by rw [hS,hU,hx]
  have he : Z (S (U x))-S (U x)=S (Z (U x)-U x) := by rw [hC,map_sub]
  have hb := approximate_opposite_unit_outcomes_control_their_inner_product Z hZ _ _ hu hv
  rw [he,hS] at hb
  have hi := le_abs_self (inner ℝ (U (S x)) (S (U x)))
  have hd := norm_sub_sq_real (U (S x)) (S (U x))
  rw [hu,hv] at hd
  have hn := ContinuousLinearMap.le_opNorm (U.comp S-S.comp U) x
  rw [hx,mul_one] at hn
  change ‖U (S x)-S (U x)‖≤‖U.comp S-S.comp U‖ at hn
  have hpos := norm_nonneg (U (S x)-S (U x))
  nlinarith [norm_nonneg (U.comp S-S.comp U)]

theorem commuting_comparison_has_a_fixed_total_truth_error
    (S Z U : E →L[ℝ] E)
    (hS : ∀ x,‖S x‖=‖x‖) (hU : ∀ x,‖U x‖=‖x‖)
    (hZ : ∀ u v,inner ℝ (Z u) v=inner ℝ u (Z v))
    (hC : ∀ x,Z (S x)=S (Z x)) (hcomm : U.comp S=S.comp U)
    (x : E) (hx : ‖x‖=1) :
    2≤‖Z (U (S x))+U (S x)‖+‖Z (U x)-U x‖ := by
  have h := approximate_comparison_requires_nondiluting_archive_actuation S Z U hS hU hZ hC x hx
  rw [hcomm,sub_self] at h
  norm_num at h
  linarith

theorem full_refinement_intertwines_the_archive_actuation
    (J : E →ₗᵢ[ℝ] F) (S U : E →L[ℝ] E) (S' U' : F →L[ℝ] F)
    (hS : ∀ x,S' (J x)=J (S x)) (hU : ∀ x,U' (J x)=J (U x)) (x : E) :
    (U'.comp S'-S'.comp U') (J x)=J ((U.comp S-S.comp U) x) := by
  simp [hS,hU,map_sub]

theorem exact_archive_actuation_floor_survives_every_complete_refinement
    (J : E →ₗᵢ[ℝ] F) (S U : E →L[ℝ] E) (S' U' : F →L[ℝ] F)
    (hS : ∀ x,S' (J x)=J (S x)) (hU : ∀ x,U' (J x)=J (U x))
    (x : E) (hx : ‖x‖=1) (hf : ‖(U.comp S-S.comp U) x‖^2=2) :
    Real.sqrt 2≤‖U'.comp S'-S'.comp U'‖ := by
  have hb := ContinuousLinearMap.le_opNorm (U'.comp S'-S'.comp U') (J x)
  rw [full_refinement_intertwines_the_archive_actuation J S U S' U' hS hU x] at hb
  simp only [J.norm_map,hx,mul_one] at hb
  have hsq := Real.sq_sqrt (by norm_num : (0 : ℝ)≤2)
  have hi : Real.sqrt 2=‖(U.comp S-S.comp U) x‖ := by
    nlinarith [norm_nonneg ((U.comp S-S.comp U) x),Real.sqrt_nonneg (2 : ℝ)]
  rwa [← hi] at hb
end Hilbert
end
end D0.Research.VerifiedArchiveActuation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.VerifiedArchiveActuation
noncomputable section
open Matrix
open D0.Foundation.VerifiabilityNecessity
open D0.Representation.FiniteProtocolClock
open D0.Research.GoldenCoherentAmplification D0.Research.GoldenProgramCompilation
open D0.Research.RetainedRecordAdmission

/-- Comparison outcomes are forced by the owned contract, before an update is supplied. -/
theorem owned_comparison_separates_reference_from_every_distinct_record
    {P : VerificationProtocol} (V : VerificationContract P)
    (l : P.Line) (c : P.Catalogue) (x y : P.State) (hxy : x≠y) :
    P.compare l c (P.record x) (P.record x)=false ∧
      P.compare l c (P.record y) (P.record x)=true := by
  constructor
  · simpa using V.correct l c x x
  · simpa [Ne.symm hxy] using V.correct l c y x

/-- Operationally reading an old record is different from defining its truth table. -/
theorem owned_verification_realization_requires_record_to_detector_interaction
    {P : VerificationProtocol} (V : VerificationContract P)
    (l : P.Line) (c : P.Catalogue) (x y : P.State) (hxy : x≠y)
    {D : Type*} (blank : D) (readout : D → Bool)
    (U : P.Record × D → P.Record × D)
    (hU : ∀ z,readout (U (P.record z,blank)).2=
      P.compare l c (P.record z) (P.record x)) :
    ¬ ∃ f : P.Record → P.Record,∃ g : D → D,∀ q,U q=(f q.1,g q.2) := by
  have ht := owned_comparison_separates_reference_from_every_distinct_record V l c x y hxy
  have hd : (U (P.record x,blank)).2≠(U (P.record y,blank)).2 := by
    intro he
    have hh := congrArg readout he
    rw [hU,hU,ht.1,ht.2] at hh
    cases hh
  exact D0.Representation.PreparationMemoryBound.comparison_requires_interaction U blank _ _ hd

theorem canonical_binary_truth_is_the_retained_bit (r : Bool) :
    canonicalProtocol.compare false PUnit.unit (canonicalProtocol.record r)
      (canonicalProtocol.record false)=r := by cases r <;> rfl

/-- Minimal four basis labels: retention and correct blank-input truth, without naming a gate. -/
theorem every_retaining_binary_basis_comparison_is_owned_registration
    (U : Equiv.Perm (Bool × Bool))
    (hr : ∀ q,(U q).1=q.1)
    (ht : ∀ r,(U (r,false)).2=r) : U=register := by
  apply Equiv.ext
  rintro ⟨r,b⟩
  have blank (s : Bool) : U (s,false)=(s,s) := Prod.ext (hr _) (ht s)
  cases b with
  | false => exact (blank r).trans (blank_record_receives_arm r).symm
  | true =>
    have hd : (U (r,true)).2≠r := by
      intro hs
      have he : U (r,true)=U (r,false) := by
        rw [blank]
        exact Prod.ext (hr _) hs
      have hh := congrArg Prod.snd (U.injective he)
      cases hh
    apply Prod.ext
    · exact hr _
    · cases r <;> cases h : (U (_,true)).2 <;> simp_all [register]

theorem canonical_owned_binary_verification_forces_registration_in_the_basis_class
    (U : Equiv.Perm (Bool × Bool)) (hr : ∀ q,(U q).1=q.1)
    (ht : ∀ r,(U (r,false)).2=
      canonicalProtocol.compare false PUnit.unit (canonicalProtocol.record r)
        (canonicalProtocol.record false)) : U=register := by
  apply every_retaining_binary_basis_comparison_is_owned_registration U hr
  intro r
  rw [ht,canonical_binary_truth_is_the_retained_bit]

def reverseRegister : Equiv.Perm (Bool × Bool) :=
  (Equiv.prodComm Bool Bool).trans (register.trans (Equiv.prodComm Bool Bool))

theorem reverse_registration_is_old_record_to_new_flag (a r : Bool) :
    reverseRegister (a,r)=(Bool.xor r a,r) := rfl

theorem reverse_registration_never_resets_the_retained_record (q : Bool × Bool) :
    (reverseRegister q).2=q.2 := rfl

theorem three_owned_registrations_exchange_the_role_coordinates (q : Bool × Bool) :
    reverseRegister (register (reverseRegister q))=(q.2,q.1) := by
  rcases q with ⟨a,r⟩
  cases a <;> cases r <;> rfl

/-- Actual system/record basis, fixed by the pinned four-coordinate native representation. -/
def reverseCopy : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1,0,0,0;0,0,0,1;0,0,1,0;0,1,0,0]
def exchange : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1,0,0,0;0,0,1,0;0,1,0,0;0,0,0,1]
def flagZ : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1,0,0,0;0,1,0,0;0,0,-1,0;0,0,0,-1]
def recordZ : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1,0,0,0;0,-1,0,0;0,0,1,0;0,0,0,-1]
def blank0 : Fin 4 → ℝ := ![1,0,0,0]
def blank1 : Fin 4 → ℝ := ![0,1,0,0]

theorem reverse_copy_is_complete_involution : reverseCopy*reverseCopy=1 := by
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [reverseCopy,Matrix.mul_apply,Fin.sum_univ_succ]

theorem reverse_copy_reads_both_blank_inputs_without_erasure :
    reverseCopy.mulVec blank0=blank0 ∧
      reverseCopy.mulVec blank1=![0,0,0,1] := by
  constructor <;> ext i <;> fin_cases i <;>
    norm_num [reverseCopy,blank0,blank1,Matrix.mulVec,dotProduct,Fin.sum_univ_succ]

theorem opposite_directions_synthesize_complete_exchange :
    reverseCopy*retainedCopy*reverseCopy=exchange := by
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [reverseCopy,retainedCopy,exchange,Matrix.mul_apply,Fin.sum_univ_succ]

theorem exchange_keeps_both_coordinates : exchange*exchange=1 ∧ exchange.transpose=exchange := by
  constructor <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [exchange,Matrix.transpose_apply,Matrix.mul_apply,Fin.sum_univ_succ]

theorem comparison_and_recording_move_the_owned_golden_gate_to_old_memory (a p : ℝ) :
    exchange*goldenSystemGate a p*exchange=goldenRecordGate a p := by
  ext i j;fin_cases i <;> fin_cases j <;>
    simp [exchange,goldenSystemGate,goldenRecordGate,Matrix.mul_apply,Fin.sum_univ_succ]

theorem golden_memory_actuation_needs_only_the_same_gate_and_both_recording_directions
    (a p : ℝ) :
    (reverseCopy*retainedCopy*reverseCopy)*goldenSystemGate a p*
      (reverseCopy*retainedCopy*reverseCopy)=goldenRecordGate a p := by
  rw [opposite_directions_synthesize_complete_exchange,
    comparison_and_recording_move_the_owned_golden_gate_to_old_memory]

theorem synthesized_owned_golden_memory_gate_breaks_the_old_archive_invariant
    (a p : ℝ) (hp : p≠0) :
    (exchange*goldenSystemGate a p*exchange)*archiveX≠
      archiveX*(exchange*goldenSystemGate a p*exchange) := by
  rw [comparison_and_recording_move_the_owned_golden_gate_to_old_memory]
  exact coherent_old_record_gate_breaks_archive_flip a p hp

end
end D0.Research.VerifiedArchiveActuation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.VerifiedArchiveActuation
noncomputable section
open Matrix
open D0.Research.RetainedRecordAdmission D0.Research.GoldenProgramCompilation

/-- The outcome specification says nothing about phases or a selected gate. -/
def RetainingRealComparison (U : Matrix (Fin 4) (Fin 4) ℝ) : Prop :=
  U.transpose*U=1 ∧ U*recordZ=recordZ*U ∧
    flagZ.mulVec (U.mulVec blank0)=U.mulVec blank0 ∧
    flagZ.mulVec (U.mulVec blank1)=-(U.mulVec blank1)

def signedComparison (c : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![c 0,0,0,0;0,0,0,c 3;0,0,c 2,0;0,c 1,0,0]

theorem every_retaining_real_comparison_has_only_four_signed_columns
    (U : Matrix (Fin 4) (Fin 4) ℝ) (h : RetainingRealComparison U) :
    ∃ c : Fin 4 → ℝ,(∀ i,c i^2=1) ∧ U=signedComparison c := by
  rcases h with ⟨ho,hr,h0,h1⟩
  have cross (i j : Fin 4) (hij : i.val%2≠j.val%2) : U i j=0 := by
    have hh := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M i j) hr
    fin_cases i <;> fin_cases j <;> norm_num at hij
    all_goals
      simp [recordZ,Matrix.mul_apply,Fin.sum_univ_succ] at hh ⊢
      linarith only [hh]
  have h01 := cross 0 1 (by decide)
  have h03 := cross 0 3 (by decide)
  have h10 := cross 1 0 (by decide)
  have h12 := cross 1 2 (by decide)
  have h21 := cross 2 1 (by decide)
  have h23 := cross 2 3 (by decide)
  have h30 := cross 3 0 (by decide)
  have h32 := cross 3 2 (by decide)
  have h20 : U 2 0=0 := by
    have hh := congrFun h0 2
    simp [flagZ,blank0,Matrix.mulVec,dotProduct,Fin.sum_univ_succ] at hh
    linarith
  have h11 : U 1 1=0 := by
    have hh := congrFun h1 1
    simp [flagZ,blank1,Matrix.mulVec,dotProduct,Fin.sum_univ_succ] at hh
    linarith
  have col (i j : Fin 4) := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M i j) ho
  have hc0 : U 0 0^2=1 := by
    have hh := col 0 0
    simpa [Matrix.mul_apply,Matrix.transpose_apply,Fin.sum_univ_succ,h10,h20,h30,pow_two] using hh
  have hc1 : U 3 1^2=1 := by
    have hh := col 1 1
    simpa [Matrix.mul_apply,Matrix.transpose_apply,Fin.sum_univ_succ,h01,h11,h21,pow_two] using hh
  have h02 : U 0 2=0 := by
    have hh := col 0 2
    simp [Matrix.mul_apply,Matrix.transpose_apply,Fin.sum_univ_succ,h10,h20,h30] at hh
    rcases hh with hz|hz
    · rw [hz] at hc0;norm_num at hc0
    · exact hz
  have h33 : U 3 3=0 := by
    have hh := col 1 3
    simp [Matrix.mul_apply,Matrix.transpose_apply,Fin.sum_univ_succ,h01,h11,h21] at hh
    rcases hh with hz|hz
    · rw [hz] at hc1;norm_num at hc1
    · exact hz
  have hc2 : U 2 2^2=1 := by
    have hh := col 2 2
    simpa [Matrix.mul_apply,Matrix.transpose_apply,Fin.sum_univ_succ,h02,h12,h32,pow_two] using hh
  have hc3 : U 1 3^2=1 := by
    have hh := col 3 3
    simpa [Matrix.mul_apply,Matrix.transpose_apply,Fin.sum_univ_succ,h03,h23,h33,pow_two] using hh
  refine ⟨![U 0 0,U 3 1,U 2 2,U 1 3],?_,?_⟩
  · intro i
    fin_cases i
    · exact hc0
    · exact hc1
    · exact hc2
    · exact hc3
  · ext i j;fin_cases i <;> fin_cases j <;>
      simp_all [signedComparison]

theorem every_four_signed_columns_realize_the_same_exact_comparison
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) : RetainingRealComparison (signedComparison c) := by
  have h0 := hc 0;have h1 := hc 1;have h2 := hc 2;have h3 := hc 3
  refine ⟨?_,?_,?_,?_⟩
  · ext i j;fin_cases i <;> fin_cases j <;>
      simp [signedComparison,Matrix.transpose_apply,Matrix.mul_apply,Fin.sum_univ_succ] <;> nlinarith
  · ext i j;fin_cases i <;> fin_cases j <;>
      simp [signedComparison,recordZ,Matrix.mul_apply,Fin.sum_univ_succ]
  · ext i;fin_cases i <;>
      simp [signedComparison,flagZ,blank0,Matrix.mulVec,dotProduct,Fin.sum_univ_succ]
  · ext i;fin_cases i <;>
      simp [signedComparison,flagZ,blank1,Matrix.mulVec,dotProduct,Fin.sum_univ_succ]

theorem complete_retaining_real_comparison_classification
    (U : Matrix (Fin 4) (Fin 4) ℝ) :
    RetainingRealComparison U ↔ ∃ c : Fin 4 → ℝ,(∀ i,c i^2=1) ∧ U=signedComparison c := by
  constructor
  · exact every_retaining_real_comparison_has_only_four_signed_columns U
  · rintro ⟨c,hc,rfl⟩
    exact every_four_signed_columns_realize_the_same_exact_comparison c hc

theorem exact_binary_truth_does_not_select_unsigned_coherent_registration :
    RetainingRealComparison (signedComparison ![1,1,1,-1]) ∧
      signedComparison ![1,1,1,-1]≠reverseCopy := by
  constructor
  · apply every_four_signed_columns_realize_the_same_exact_comparison
    intro i;fin_cases i <;> norm_num
  · intro h
    have hh := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 1 3) h
    change (-1 : ℝ)=1 at hh
    norm_num at hh

theorem signed_comparison_is_unsigned_copy_with_retained_input_phases (c : Fin 4 → ℝ) :
    signedComparison c=reverseCopy*Matrix.diagonal c := by
  ext i j;fin_cases i <;> fin_cases j <;>
    simp [signedComparison,reverseCopy,Matrix.mul_apply,Matrix.diagonal,Fin.sum_univ_succ]

theorem every_signed_comparison_has_fixed_complete_blank_commutator_mass
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) :
    ∑ i,((signedComparison c*archiveX-archiveX*signedComparison c).mulVec blank0 i)^2=2 := by
  have h0 := hc 0;have h1 := hc 1
  simp [signedComparison,archiveX,blank0,Matrix.mulVec,dotProduct,Matrix.mul_apply,Fin.sum_univ_succ]
  nlinarith

end
end D0.Research.VerifiedArchiveActuation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.VerifiedArchiveActuation
noncomputable section
open Matrix
open D0.Research.GoldenCoherentAmplification D0.Research.GoldenProgramCompilation
open D0.Research.RetainedRecordAdmission
open D0.Representation.FiniteProtocolClock

def bitCoordinates : Fin 4 ≃ Bool × Bool where
  toFun i := ![(false,false),(false,true),(true,false),(true,true)] i
  invFun q := if q.1 then (if q.2 then 3 else 2) else (if q.2 then 1 else 0)
  left_inv := by intro i;fin_cases i <;> rfl
  right_inv := by rintro ⟨a,r⟩;cases a <;> cases r <;> rfl

theorem native_reverse_copy_is_exactly_the_owned_reversible_registration
    (i j : Fin 4) :
    reverseCopy i j=if bitCoordinates i=reverseRegister (bitCoordinates j) then 1 else 0 := by
  fin_cases i <;> fin_cases j <;> rfl

theorem native_forward_copy_is_exactly_the_owned_reversible_registration
    (i j : Fin 4) :
    retainedCopy i j=if bitCoordinates i=register (bitCoordinates j) then 1 else 0 := by
  fin_cases i <;> fin_cases j <;> rfl

theorem native_flag_and_old_record_probes_act_on_different_roles :
    flagZ*archiveX=archiveX*flagZ ∧ flagZ.transpose=flagZ ∧
      archiveX.transpose*archiveX=1 := by
  refine ⟨?_,?_,?_⟩ <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [flagZ,archiveX,Matrix.transpose_apply,Matrix.mul_apply,Fin.sum_univ_succ]

theorem native_reverse_registration_breaks_the_old_archive_probe :
    reverseCopy*archiveX≠archiveX*reverseCopy := by
  intro h
  have hh := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 0 1) h
  norm_num [reverseCopy,archiveX,Matrix.mul_apply,Fin.sum_univ_succ] at hh

theorem two_directions_are_not_the_same_record_operation : reverseCopy≠retainedCopy := by
  intro h
  have hh := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 1 3) h
  change (1 : ℝ)=0 at hh
  norm_num at hh

theorem whole_record_to_flag_reading_and_exchange_do_not_change_p0 :
    reverseCopy*retainedCopy*reverseCopy*goldenSystemGate
      (Real.sqrt D0.primitiveRoot) D0.primitiveRoot*
      (reverseCopy*retainedCopy*reverseCopy)=goldenRecordGate
      (Real.sqrt D0.primitiveRoot) D0.primitiveRoot :=
  golden_memory_actuation_needs_only_the_same_gate_and_both_recording_directions _ _
end
end D0.Research.VerifiedArchiveActuation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.VerifiedArchiveActuation
noncomputable section
open Matrix Filter Topology
open D0.Foundation.VerifiabilityNecessity
open D0.Research.RetainedRecordAdmission D0.Research.GoldenProgramCompilation

section Bridge
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

def outcomeSign (b : Bool) : ℝ := if b then -1 else 1

/-- The dynamic representation of the owned truth table is an explicit application input. -/
theorem every_complete_realization_of_owned_verification_requires_archive_actuation
    {P : VerificationProtocol} (V : VerificationContract P)
    (l : P.Line) (c : P.Catalogue) (x y : P.State) (hxy : x≠y)
    (encode : P.Record → E) (S Z U : E →L[ℝ] E)
    (hS : ∀ q,‖S q‖=‖q‖) (hU : ∀ q,‖U q‖=‖q‖)
    (hZ : ∀ u v,inner ℝ (Z u) v=inner ℝ u (Z v))
    (hC : ∀ q,Z (S q)=S (Z q))
    (hx : ‖encode (P.record x)‖=1) (hpair : S (encode (P.record x))=encode (P.record y))
    (hout : ∀ z,Z (U (encode (P.record z)))=
      outcomeSign (P.compare l c (P.record z) (P.record x)) • U (encode (P.record z))) :
    Real.sqrt 2≤‖U.comp S-S.comp U‖ := by
  have ht := owned_comparison_separates_reference_from_every_distinct_record V l c x y hxy
  apply every_exact_complete_comparison_requires_uniform_archive_actuation S Z U hS hU hZ hC
    (encode (P.record x)) hx
  · have hh := hout x
    simpa [ht.1,outcomeSign] using hh
  · rw [hpair]
    have hh := hout y
    simpa [ht.2,outcomeSign] using hh

/-- Approximation does not replace native truth by a new gate definition. -/
theorem owned_verification_error_and_archive_actuation_have_a_fixed_tradeoff
    {P : VerificationProtocol} (V : VerificationContract P)
    (l : P.Line) (c : P.Catalogue) (x y : P.State) (hxy : x≠y)
    (encode : P.Record → E) (S Z U : E →L[ℝ] E)
    (hS : ∀ q,‖S q‖=‖q‖) (hU : ∀ q,‖U q‖=‖q‖)
    (hZ : ∀ u v,inner ℝ (Z u) v=inner ℝ u (Z v))
    (hC : ∀ q,Z (S q)=S (Z q))
    (hx : ‖encode (P.record x)‖=1) (hpair : S (encode (P.record x))=encode (P.record y)) :
    2-(‖Z (U (encode (P.record x)))-
      outcomeSign (P.compare l c (P.record x) (P.record x)) • U (encode (P.record x))‖+
      ‖Z (U (encode (P.record y)))-
      outcomeSign (P.compare l c (P.record y) (P.record x)) • U (encode (P.record y))‖)
      ≤‖U.comp S-S.comp U‖^2 := by
  have ht := owned_comparison_separates_reference_from_every_distinct_record V l c x y hxy
  have h := approximate_comparison_requires_nondiluting_archive_actuation S Z U hS hU hZ hC
    (encode (P.record x)) hx
  simpa [hpair,ht.1,ht.2,outcomeSign,add_comm] using h

/-- A unitary complete realization cannot perfectly retain two nonorthogonal records while
writing orthogonal deterministic outcomes. This does not assert cloning arbitrary states. -/
theorem exact_retained_comparison_forces_orthogonality_of_distinct_encoded_records
    (J : E →ₗᵢ[ℝ] E) (Z : E →L[ℝ] E)
    (hZ : ∀ u v,inner ℝ (Z u) v=inner ℝ u (Z v)) (u v : E)
    (hu : Z (J u)=-(J u)) (hv : Z (J v)=J v) : inner ℝ u v=0 := by
  rw [← J.inner_map_map]
  exact opposite_exact_outcomes_are_orthogonal Z hZ _ _ hu hv
end Bridge

/-- The owned finite native gate still has the same split; no new mixer angle occurs. -/
theorem literal_native_golden_memory_actuation_is_the_same_owned_gate :
    exchange*D0.Research.GoldenCoherentAmplification.goldenSystemGate
      (Real.sqrt D0.primitiveRoot) D0.primitiveRoot*exchange=
    D0.Research.GoldenCoherentAmplification.goldenRecordGate
      (Real.sqrt D0.primitiveRoot) D0.primitiveRoot :=
  comparison_and_recording_move_the_owned_golden_gate_to_old_memory _ _

theorem literal_p0_synthesized_memory_gate_changes_the_old_archive_probe :
    (exchange*D0.Research.GoldenCoherentAmplification.goldenSystemGate
      (Real.sqrt D0.primitiveRoot) D0.primitiveRoot*exchange)*archiveX≠
    archiveX*(exchange*D0.Research.GoldenCoherentAmplification.goldenSystemGate
      (Real.sqrt D0.primitiveRoot) D0.primitiveRoot*exchange) := by
  exact synthesized_owned_golden_memory_gate_breaks_the_old_archive_invariant _ _
    (ne_of_gt D0.Representation.GoldenOrderInterferometer.primitive_positive)

end
end D0.Research.VerifiedArchiveActuation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.VerifiedArchiveActuation
noncomputable section
open Matrix
open D0.Research.RetainedRecordAdmission

def phaseVector (e : Fin 4 → Bool) (i : Fin 4) : ℝ := if e i then -1 else 1

theorem every_boolean_phase_signature_has_unit_columns (e : Fin 4 → Bool) :
    ∀ i,phaseVector e i^2=1 := by
  intro i;cases h : e i <;> simp [phaseVector,h]

theorem four_column_phases_determine_the_complete_real_operator :
    Function.Injective signedComparison := by
  intro c d h
  have h0 := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 0 0) h
  have h1 := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 3 1) h
  have h2 := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 2 2) h
  have h3 := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 1 3) h
  change c 0=d 0 at h0
  change c 1=d 1 at h1
  change c 2=d 2 at h2
  change c 3=d 3 at h3
  funext i;fin_cases i <;> assumption

def comparisonOfSignature (e : Fin 4 → Bool) :
    {U : Matrix (Fin 4) (Fin 4) ℝ // RetainingRealComparison U} :=
  ⟨signedComparison (phaseVector e),
    every_four_signed_columns_realize_the_same_exact_comparison _
      (every_boolean_phase_signature_has_unit_columns e)⟩

theorem complete_phase_signature_representation_is_injective :
    Function.Injective comparisonOfSignature := by
  intro e f h
  have hm := four_column_phases_determine_the_complete_real_operator (congrArg Subtype.val h)
  funext i
  have hi := congrFun hm i
  cases he : e i <;> cases hf : f i <;> simp_all [phaseVector] <;> norm_num at *

theorem complete_phase_signature_representation_is_surjective :
    Function.Surjective comparisonOfSignature := by
  intro U
  obtain ⟨c,hc,hU⟩ := every_retaining_real_comparison_has_only_four_signed_columns U.val U.property
  refine ⟨fun i => decide (c i=-1),?_⟩
  have he : phaseVector (fun i => decide (c i=-1))=c := by
    funext i
    rcases sq_eq_one_iff.mp (hc i) with hh|hh <;> simp [phaseVector,hh] <;> norm_num
  apply Subtype.ext
  change signedComparison (phaseVector (fun i => decide (c i=-1)))=U.val
  rw [he,← hU]

def realComparisonEquivSignatures :
    {U : Matrix (Fin 4) (Fin 4) ℝ // RetainingRealComparison U} ≃ (Fin 4 → Bool) :=
  (Equiv.ofBijective comparisonOfSignature
    ⟨complete_phase_signature_representation_is_injective,
      complete_phase_signature_representation_is_surjective⟩).symm

theorem all_retaining_real_comparisons_form_exactly_sixteen_completions :
    Nat.card {U : Matrix (Fin 4) (Fin 4) ℝ // RetainingRealComparison U}=16 := by
  rw [Nat.card_congr realComparisonEquivSignatures,Nat.card_eq_fintype_card]
  decide

def phaseCoupling (c : Fin 4 → ℝ) : ℝ := c 0*c 3+c 1*c 2

theorem complete_commutator_gram_retains_the_coherent_phase_mode
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) :
    let D := signedComparison c*archiveX-archiveX*signedComparison c
    D.transpose*D=!![2,0,-phaseCoupling c,0;0,2,0,-phaseCoupling c;
      -phaseCoupling c,0,2,0;0,-phaseCoupling c,0,2] := by
  have h0 := hc 0;have h1 := hc 1;have h2 := hc 2;have h3 := hc 3
  dsimp only
  ext i j;fin_cases i <;> fin_cases j <;>
    simp [signedComparison,archiveX,phaseCoupling,Matrix.transpose_apply,
      Matrix.mul_apply,Fin.sum_univ_succ] <;> nlinarith

theorem coherent_phase_mode_has_only_the_two_commutator_strength_classes
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) :
    phaseCoupling c^2=2+2*(c 0*c 1*c 2*c 3) := by
  calc
    phaseCoupling c^2=c 0^2*c 3^2+c 1^2*c 2^2+2*(c 0*c 1*c 2*c 3) := by
      unfold phaseCoupling;ring
    _ = 2+2*(c 0*c 1*c 2*c 3) := by rw [hc 0,hc 1,hc 2,hc 3];ring

theorem minimal_complete_archive_actuation_is_attained_by_a_correct_signed_comparison :
    let U := signedComparison ![1,1,1,-1]
    (U*archiveX-archiveX*U).transpose*(U*archiveX-archiveX*U)=2 • (1 : Matrix (Fin 4) (Fin 4) ℝ) := by
  have hc : ∀ i,(![1,1,1,-1] : Fin 4 → ℝ) i^2=1 := by
    intro i;fin_cases i <;> norm_num
  have hg := complete_commutator_gram_retains_the_coherent_phase_mode ![1,1,1,-1] hc
  have hp : phaseCoupling ![1,1,1,-1]=0 := by
    change (1 : ℝ)*(-1)+1*1=0
    norm_num
  dsimp only at hg ⊢
  rw [hg,hp]
  ext i j;fin_cases i <;> fin_cases j <;> norm_num

end
end D0.Research.VerifiedArchiveActuation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.VerifiedArchiveActuation
noncomputable section
open Matrix
open scoped BigOperators Kronecker
open D0.Research.GoldenHistoryPreparation D0.Research.GoldenProgramCompilation
open D0.Research.RetainedRecordAdmission
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def realHistoryInclusion (a p : ℝ) (n : ℕ) (x : ι → ℝ) : ι × Word n → ℝ :=
  fun s => x s.1*amplitude a p s.2

def wholeHistoryOperator (A : Matrix ι ι ℝ) (n : ℕ) :
    Matrix (ι × Word n) (ι × Word n) ℝ := A ⊗ₖ (1 : Matrix (Word n) (Word n) ℝ)

theorem literal_golden_refinement_preserves_full_real_weight
    (a p : ℝ) (hn : a^2+p^2=1) (n : ℕ) (x : ι → ℝ) :
    (∑ s,realHistoryInclusion a p n x s^2)=∑ i,x i^2 := by
  have hmass := complete_mass a p hn n
  simp only [realHistoryInclusion,Fintype.sum_prod_type,mul_pow]
  simp only [← Finset.mul_sum,hmass,mul_one]

theorem literal_golden_refinement_subtracts_without_reset
    (a p : ℝ) (n : ℕ) (x y : ι → ℝ) :
    realHistoryInclusion a p n (x-y)=realHistoryInclusion a p n x-realHistoryInclusion a p n y := by
  funext s;simp [realHistoryInclusion,sub_mul]

theorem literal_golden_refinement_intertwines_every_complete_old_operator
    (A : Matrix ι ι ℝ) (a p : ℝ) (n : ℕ) (x : ι → ℝ) :
    (wholeHistoryOperator A n).mulVec (realHistoryInclusion a p n x)=
      realHistoryInclusion a p n (A.mulVec x) := by
  ext s
  rcases s with ⟨i,w⟩
  simp [wholeHistoryOperator,realHistoryInclusion,Matrix.mulVec,dotProduct,
    Matrix.kroneckerMap_apply,Fintype.sum_prod_type,Matrix.one_apply,Finset.sum_mul,mul_assoc]

theorem complete_old_operator_composition_survives_every_history_depth
    (A B : Matrix ι ι ℝ) (n : ℕ) :
    wholeHistoryOperator A n*wholeHistoryOperator B n=wholeHistoryOperator (A*B) n := by
  simpa [wholeHistoryOperator] using
    (Matrix.mul_kronecker_mul A B (1 : Matrix (Word n) (Word n) ℝ) 1).symm

theorem complete_archive_commutator_intertwines_every_literal_golden_depth
    (A B : Matrix ι ι ℝ) (a p : ℝ) (n : ℕ) (x : ι → ℝ) :
    (wholeHistoryOperator A n*wholeHistoryOperator B n-
      wholeHistoryOperator B n*wholeHistoryOperator A n).mulVec
      (realHistoryInclusion a p n x)=
    realHistoryInclusion a p n ((A*B-B*A).mulVec x) := by
  rw [complete_old_operator_composition_survives_every_history_depth,
    complete_old_operator_composition_survives_every_history_depth,Matrix.sub_mulVec,
    literal_golden_refinement_intertwines_every_complete_old_operator,
    literal_golden_refinement_intertwines_every_complete_old_operator,
    ← literal_golden_refinement_subtracts_without_reset,Matrix.sub_mulVec]

theorem every_correct_signed_comparison_keeps_its_full_actuation_at_all_golden_depths
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (a p : ℝ) (hn : a^2+p^2=1) (n : ℕ) :
    (∑ s,((wholeHistoryOperator (signedComparison c) n*wholeHistoryOperator archiveX n-
      wholeHistoryOperator archiveX n*wholeHistoryOperator (signedComparison c) n).mulVec
        (realHistoryInclusion a p n blank0) s)^2)=2 := by
  rw [complete_archive_commutator_intertwines_every_literal_golden_depth,
    literal_golden_refinement_preserves_full_real_weight a p hn]
  exact every_signed_comparison_has_fixed_complete_blank_commutator_mass c hc

theorem actual_p0_refinement_has_no_dilution_of_binary_archive_actuation
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (n : ℕ) :
    (∑ s,((wholeHistoryOperator (signedComparison c) n*wholeHistoryOperator archiveX n-
      wholeHistoryOperator archiveX n*wholeHistoryOperator (signedComparison c) n).mulVec
        (realHistoryInclusion (Real.sqrt D0.primitiveRoot) D0.primitiveRoot n blank0) s)^2)=2 := by
  apply every_correct_signed_comparison_keeps_its_full_actuation_at_all_golden_depths c hc
  have ha := Real.sq_sqrt (le_of_lt D0.Representation.GoldenOrderInterferometer.primitive_positive)
  have hp := D0.primitive_root_satisfies
  linarith
end
end D0.Research.VerifiedArchiveActuation

set_option autoImplicit false
set_option maxHeartbeats 2000000
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.UniformMemoryActuation
noncomputable section
open Matrix
open D0.Research.GoldenCoherentAmplification D0.Research.GoldenProgramCompilation
open D0.Research.VerifiedArchiveActuation D0.Research.RetainedRecordAdmission
abbrev M4 := Matrix (Fin 4) (Fin 4) ℝ
def UnitSigns (c : Fin 4 → ℝ) : Prop := ∀ i,c i^2=1
def parity (c : Fin 4 → ℝ) : ℝ := c 0*c 1*c 2*c 3
def signedRecording (d : Fin 4 → ℝ) : M4 :=
  !![d 0,0,0,0;0,d 1,0,0;0,0,0,d 3;0,0,d 2,0]
def swappedSigns (d : Fin 4 → ℝ) : Fin 4 → ℝ := ![d 0,d 2,d 1,d 3]
def RetainingRealRecording (F : M4) : Prop :=
  RetainingRealComparison (exchange*F*exchange)

theorem sign_products_have_unit_square (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (i j : Fin 4) :
    (c i*c j)^2=1 := by
  rw [mul_pow,hc i,hc j];norm_num
theorem sign_parity_has_unit_square (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) :
    parity c^2=1 := by
  simp [parity,mul_pow,hc]
theorem sign_parity_is_only_plus_or_minus_one (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) :
    parity c=1 ∨ parity c=-1 := sq_eq_one_iff.mp (sign_parity_has_unit_square c hc)
theorem swapped_unit_signs (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) : UnitSigns (swappedSigns c) := by
  intro i;fin_cases i <;> simp [swappedSigns,hc]
theorem swapped_signs_twice (c : Fin 4 → ℝ) : swappedSigns (swappedSigns c)=c := by
  funext i;fin_cases i <;> rfl
theorem exchange_conjugates_the_complete_recording_specification (d : Fin 4 → ℝ) :
    exchange*signedRecording d*exchange=signedComparison (swappedSigns d) := by
  ext i j;fin_cases i <;> fin_cases j <;>
    simp [exchange,signedRecording,signedComparison,swappedSigns,Matrix.mul_apply,Fin.sum_univ_succ]
theorem passive_exchange_conjugation_is_involutive (F : M4) :
    exchange*(exchange*F*exchange)*exchange=F := by
  have ht := exchange_keeps_both_coordinates.1
  simp only [← Matrix.mul_assoc]
  rw [ht,one_mul]
  rw [Matrix.mul_assoc,ht,mul_one]
theorem complete_minimal_real_recording_classification (F : M4) :
    RetainingRealRecording F ↔ ∃ d : Fin 4 → ℝ,UnitSigns d ∧ F=signedRecording d := by
  constructor
  · intro h
    obtain ⟨c,hc,he⟩ := complete_retaining_real_comparison_classification _ |>.mp h
    refine ⟨swappedSigns c,swapped_unit_signs c hc,?_⟩
    have hh := exchange_conjugates_the_complete_recording_specification (swappedSigns c)
    rw [swapped_signs_twice] at hh
    have h := congrArg (fun M : M4 => exchange*M*exchange) he
    dsimp only at h
    rw [passive_exchange_conjugation_is_involutive,← hh,
      passive_exchange_conjugation_is_involutive] at h
    exact h
  · rintro ⟨d,hd,rfl⟩
    unfold RetainingRealRecording
    rw [exchange_conjugates_the_complete_recording_specification]
    exact every_four_signed_columns_realize_the_same_exact_comparison _ (swapped_unit_signs d hd)

def recordingEquivComparison : {F : M4 // RetainingRealRecording F} ≃
    {U : M4 // RetainingRealComparison U} where
  toFun F := ⟨exchange*F.val*exchange,F.property⟩
  invFun U := ⟨exchange*U.val*exchange,by
    unfold RetainingRealRecording
    rw [passive_exchange_conjugation_is_involutive]
    exact U.property⟩
  left_inv F := Subtype.ext (passive_exchange_conjugation_is_involutive _)
  right_inv U := Subtype.ext (passive_exchange_conjugation_is_involutive _)
theorem all_minimal_real_retaining_recordings_form_sixteen_completions :
    Nat.card {F : M4 // RetainingRealRecording F}=16 := by
  rw [Nat.card_congr recordingEquivComparison]
  exact all_retaining_real_comparisons_form_exactly_sixteen_completions
theorem full_joint_minimal_real_family_has_two_hundred_fifty_six_pairs :
    Nat.card ({F : M4 // RetainingRealRecording F} ×
      {U : M4 // RetainingRealComparison U})=256 := by
  rw [Nat.card_prod,all_minimal_real_retaining_recordings_form_sixteen_completions,
    all_retaining_real_comparisons_form_exactly_sixteen_completions]

theorem signed_comparison_inverse_is_three_forward_operations (c : Fin 4 → ℝ)
    (hc : ∀ i,c i^2=1) : (signedComparison c)^4=1 := by
  have cube (i : Fin 4) : c i^3=c i := by rw [pow_succ,hc i];ring
  have fourth (i : Fin 4) : c i^4=1 := by
    rw [show (4:ℕ)=2*2 by decide,pow_mul,hc i];norm_num
  ext i j;fin_cases i <;> fin_cases j <;>
    simp [signedComparison,pow_succ,Matrix.mul_apply,Fin.sum_univ_succ] <;>
    ring_nf <;> try simp [hc,cube,fourth]
theorem signed_recording_inverse_is_three_forward_operations (d : Fin 4 → ℝ)
    (hd : ∀ i,d i^2=1) : (signedRecording d)^4=1 := by
  have cube (i : Fin 4) : d i^3=d i := by rw [pow_succ,hd i];ring
  have fourth (i : Fin 4) : d i^4=1 := by
    rw [show (4:ℕ)=2*2 by decide,pow_mul,hd i];norm_num
  ext i j;fin_cases i <;> fin_cases j <;>
    simp [signedRecording,pow_succ,Matrix.mul_apply,Fin.sum_univ_succ] <;>
    ring_nf <;> try simp [hd,cube,fourth]

def signedSwap (v : Fin 4 → ℝ) : M4 :=
  !![v 0,0,0,0;0,0,v 2,0;0,v 1,0,0;0,0,0,v 3]
def routeU (c d : Fin 4 → ℝ) : Fin 4 → ℝ :=
  ![d 0,c 1*c 2*d 3,c 2*c 3*d 2,c 1*c 3*d 1]
def routeF (c d : Fin 4 → ℝ) : Fin 4 → ℝ :=
  ![c 0,c 1*d 1*d 3,c 3*d 1*d 2,c 2*d 2*d 3]
theorem full_reverse_forward_reverse_route_keeps_all_coherent_phases
    (c d : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) :
    signedComparison c*signedRecording d*signedComparison c=signedSwap (routeU c d) := by
  ext i j;fin_cases i <;> fin_cases j <;>
    simp [signedComparison,signedRecording,signedSwap,routeU,Matrix.mul_apply,Fin.sum_univ_succ] <;>
    ring_nf <;> try simp [hc]
theorem full_forward_reverse_forward_route_keeps_all_coherent_phases
    (c d : Fin 4 → ℝ) (hd : ∀ i,d i^2=1) :
    signedRecording d*signedComparison c*signedRecording d=signedSwap (routeF c d) := by
  ext i j;fin_cases i <;> fin_cases j <;>
    simp [signedComparison,signedRecording,signedSwap,routeF,Matrix.mul_apply,Fin.sum_univ_succ] <;>
    ring_nf <;> try simp [hd]
theorem both_routes_are_complete_signed_swaps (c d : Fin 4 → ℝ)
    (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1) : UnitSigns (routeU c d) ∧ UnitSigns (routeF c d) := by
  constructor <;> intro i <;> fin_cases i <;> simp [routeU,routeF,mul_pow,hc,hd]
def branchGate (a p q : ℝ) : M4 :=
  !![a,-p,0,0;p,a,0,0;0,0,a,-q;0,0,q,a]
theorem any_complete_signed_swap_has_two_memory_orientations
    (v : Fin 4 → ℝ) (hv : ∀ i,v i^2=1) (a p : ℝ) :
    signedSwap v*goldenSystemGate a p*(signedSwap v).transpose=
      branchGate a (v 0*v 2*p) (v 1*v 3*p) := by
  ext i j;fin_cases i <;> fin_cases j <;>
    simp [signedSwap,goldenSystemGate,branchGate,Matrix.transpose_apply,Matrix.mul_apply,Fin.sum_univ_succ] <;>
    ring_nf <;> try simp [hv] <;> ring
theorem unit_sign_pair_product_from_parity (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) :
    c 1*c 3=parity c*(c 0*c 2) := by
  unfold parity
  calc
    c 1*c 3=(c 0^2)*(c 2^2)*(c 1*c 3) := by rw [hc 0,hc 2];ring
    _ = c 0*c 1*c 2*c 3*(c 0*c 2) := by ring
theorem reverse_route_second_orientation_is_forward_parity_times_first
    (c d : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1) :
    routeU c d 1*routeU c d 3=parity d*(routeU c d 0*routeU c d 2) := by
  change (c 1*c 2*d 3)*(c 1*c 3*d 1)=parity d*(d 0*(c 2*c 3*d 2))
  calc
    (c 1*c 2*d 3)*(c 1*c 3*d 1)=c 1^2*c 2*c 3*(d 1*d 3) := by ring
    _ = parity d*(d 0*(c 2*c 3*d 2)) := by
      rw [hc 1,unit_sign_pair_product_from_parity d hd];ring
theorem forward_route_second_orientation_is_reverse_parity_times_first
    (c d : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1) :
    routeF c d 1*routeF c d 3=parity c*(routeF c d 0*routeF c d 2) := by
  change (c 1*d 1*d 3)*(c 2*d 2*d 3)=parity c*(c 0*(c 3*d 1*d 2))
  have hh : c 1*c 2=parity c*(c 0*c 3) := by
    unfold parity
    calc
      c 1*c 2=c 0^2*c 3^2*(c 1*c 2) := by rw [hc 0,hc 3];ring
      _ = c 0*c 1*c 2*c 3*(c 0*c 3) := by ring
  calc
    (c 1*d 1*d 3)*(c 2*d 2*d 3)=d 3^2*d 1*d 2*(c 1*c 2) := by ring
    _ = parity c*(c 0*(c 3*d 1*d 2)) := by rw [hd 3,hh];ring
theorem complete_uniform_memory_transfer_for_all_reverse_phases
    (c d : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1) (hpar : parity d=1) (a p : ℝ) :
    let S := signedComparison c*signedRecording d*signedComparison c
    S*goldenSystemGate a p*S.transpose=goldenRecordGate a (d 0*d 2*c 2*c 3*p) := by
  dsimp only
  rw [full_reverse_forward_reverse_route_keeps_all_coherent_phases c d hc,
    any_complete_signed_swap_has_two_memory_orientations _
      (both_routes_are_complete_signed_swaps c d hc hd).1,
    reverse_route_second_orientation_is_forward_parity_times_first c d hc hd,hpar,one_mul]
  ext i j;fin_cases i <;> fin_cases j <;> norm_num [branchGate,goldenRecordGate,routeU,Matrix.cons_val_two,Matrix.cons_val_three] <;> (apply Or.inl;ring)
theorem alternate_uniform_memory_transfer_for_all_forward_phases
    (c d : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1) (hpar : parity c=1) (a p : ℝ) :
    let S := signedRecording d*signedComparison c*signedRecording d
    S*goldenSystemGate a p*S.transpose=goldenRecordGate a (c 0*c 3*d 1*d 2*p) := by
  dsimp only
  rw [full_forward_reverse_forward_route_keeps_all_coherent_phases c d hd,
    any_complete_signed_swap_has_two_memory_orientations _
      (both_routes_are_complete_signed_swaps c d hc hd).2,
    forward_route_second_orientation_is_reverse_parity_times_first c d hc hd,hpar,one_mul]
  ext i j;fin_cases i <;> fin_cases j <;> norm_num [branchGate,goldenRecordGate,routeF,Matrix.cons_val_two,Matrix.cons_val_three] <;> (apply Or.inl;ring)
end
end D0.Research.UniformMemoryActuation

set_option autoImplicit false
set_option maxHeartbeats 2000000
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.UniformMemoryActuation
noncomputable section
open Matrix Filter Topology
open D0.Research.GoldenCoherentAmplification D0.Research.VerifiedArchiveActuation
@[simp] theorem spin_value_0 : D0.Representation.OrderMemoryReadout.spin 0=D0.Representation.OrderMemoryReadout.left 1 0 0 0 := rfl
@[simp] theorem spin_value_1 : D0.Representation.OrderMemoryReadout.spin 1=D0.Representation.OrderMemoryReadout.left (-1) 0 0 0 := rfl
@[simp] theorem spin_value_2 : D0.Representation.OrderMemoryReadout.spin 2=D0.Representation.OrderMemoryReadout.left 0 1 0 0 := rfl
@[simp] theorem spin_value_3 : D0.Representation.OrderMemoryReadout.spin 3=D0.Representation.OrderMemoryReadout.left 0 (-1) 0 0 := rfl
@[simp] theorem spin_value_4 : D0.Representation.OrderMemoryReadout.spin 4=D0.Representation.OrderMemoryReadout.left 0 0 1 0 := rfl
@[simp] theorem spin_value_5 : D0.Representation.OrderMemoryReadout.spin 5=D0.Representation.OrderMemoryReadout.left 0 0 (-1) 0 := rfl
@[simp] theorem spin_value_6 : D0.Representation.OrderMemoryReadout.spin 6=D0.Representation.OrderMemoryReadout.left 0 0 0 1 := rfl
@[simp] theorem spin_value_7 : D0.Representation.OrderMemoryReadout.spin 7=D0.Representation.OrderMemoryReadout.left 0 0 0 (-1) := rfl
@[simp] theorem spin_constructor_value_0 (h : (0 : ℕ)<8) : D0.Representation.OrderMemoryReadout.spin ⟨0,h⟩=D0.Representation.OrderMemoryReadout.left 1 0 0 0 := rfl
@[simp] theorem spin_constructor_value_1 (h : (1 : ℕ)<8) : D0.Representation.OrderMemoryReadout.spin ⟨1,h⟩=D0.Representation.OrderMemoryReadout.left (-1) 0 0 0 := rfl
@[simp] theorem spin_constructor_value_2 (h : (2 : ℕ)<8) : D0.Representation.OrderMemoryReadout.spin ⟨2,h⟩=D0.Representation.OrderMemoryReadout.left 0 1 0 0 := rfl
@[simp] theorem spin_constructor_value_3 (h : (3 : ℕ)<8) : D0.Representation.OrderMemoryReadout.spin ⟨3,h⟩=D0.Representation.OrderMemoryReadout.left 0 (-1) 0 0 := rfl
@[simp] theorem spin_constructor_value_4 (h : (4 : ℕ)<8) : D0.Representation.OrderMemoryReadout.spin ⟨4,h⟩=D0.Representation.OrderMemoryReadout.left 0 0 1 0 := rfl
@[simp] theorem spin_constructor_value_5 (h : (5 : ℕ)<8) : D0.Representation.OrderMemoryReadout.spin ⟨5,h⟩=D0.Representation.OrderMemoryReadout.left 0 0 (-1) 0 := rfl
@[simp] theorem spin_constructor_value_6 (h : (6 : ℕ)<8) : D0.Representation.OrderMemoryReadout.spin ⟨6,h⟩=D0.Representation.OrderMemoryReadout.left 0 0 0 1 := rfl
@[simp] theorem spin_constructor_value_7 (h : (7 : ℕ)<8) : D0.Representation.OrderMemoryReadout.spin ⟨7,h⟩=D0.Representation.OrderMemoryReadout.left 0 0 0 (-1) := rfl
def axis (k : Fin 3) : M4 :=
  (D0.Representation.OrderMemoryReadout.spin (![2,4,6] k)).map (algebraMap ℚ ℝ)
def q8Frame (g : Fin 8) : M4 :=
  (D0.Representation.OrderMemoryReadout.spin g).map (algebraMap ℚ ℝ)
def NormalizesAxes (W : M4) : Prop :=
  ∀ k : Fin 3,∃ j : Fin 3,∃ t : ℝ,t^2=1 ∧ W*axis k*W.transpose=t • axis j
def AxisSet : Set M4 := Set.range axis ∪ Set.range (fun k => -axis k)

theorem axis_is_the_owned_real_left_q8_frame (k : Fin 3) :
    axis k=(D0.Representation.OrderMemoryReadout.spin (![2,4,6] k)).map (algebraMap ℚ ℝ) := rfl
theorem golden_old_memory_is_left_quaternion_rotation (a p : ℝ) :
    goldenRecordGate a p=a • (1 : M4)+p • axis 0 := by
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [goldenRecordGate,axis,spin_value_0,spin_value_1,spin_value_2,spin_value_3,spin_value_4,spin_value_5,spin_value_6,spin_value_7,
      Matrix.cons_val_two,Matrix.cons_val_three,Matrix.cons_val_four,Matrix.cons_val_succ',
      D0.Representation.OrderMemoryReadout.left,Matrix.map_apply,Matrix.smul_apply,Matrix.one_apply]
theorem every_active_golden_gate_commutes_with_all_owned_left_axes (a p : ℝ) (k : Fin 3) :
    goldenSystemGate a p*axis k=axis k*goldenSystemGate a p := by
  fin_cases k <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [goldenSystemGate,axis,spin_value_0,spin_value_1,spin_value_2,spin_value_3,spin_value_4,spin_value_5,spin_value_6,spin_value_7,
      Matrix.cons_val_two,Matrix.cons_val_three,Matrix.cons_val_four,Matrix.cons_val_succ',
      D0.Representation.OrderMemoryReadout.left,Matrix.map_apply,Matrix.mul_apply,Matrix.vecMul,dotProduct,Fin.sum_univ_succ]
theorem complete_active_golden_gate_has_orthogonal_inverse (a p : ℝ) (hn : a^2+p^2=1) :
    goldenSystemGate a p*(goldenSystemGate a p).transpose=1 := by
  ext i j;fin_cases i <;> fin_cases j <;>
    simp [goldenSystemGate,Matrix.transpose,Matrix.transpose_apply,Matrix.mul_apply,Matrix.vecMul,dotProduct,Fin.sum_univ_succ] <;> nlinarith
theorem all_normalized_active_rotations_normalize_the_owned_axes (a p : ℝ) (hn : a^2+p^2=1) :
    NormalizesAxes (goldenSystemGate a p) := by
  intro k
  refine ⟨k,1,by norm_num,?_⟩
  rw [every_active_golden_gate_commutes_with_all_owned_left_axes,Matrix.mul_assoc,
    complete_active_golden_gate_has_orthogonal_inverse a p hn,mul_one,one_smul]
theorem identity_normalizes_axes : NormalizesAxes (1 : M4) := by
  intro k;refine ⟨k,1,by norm_num,?_⟩;simp
theorem normalization_is_closed_under_complete_composition (U V : M4)
    (hu : NormalizesAxes U) (hv : NormalizesAxes V) : NormalizesAxes (U*V) := by
  intro k
  obtain ⟨j,t,ht,he⟩ := hv k
  obtain ⟨l,u,hu,hh⟩ := hu j
  refine ⟨l,t*u,by rw [mul_pow,ht,hu];norm_num,?_⟩
  calc
    (U*V)*axis k*(U*V).transpose=U*(V*axis k*V.transpose)*U.transpose := by
      rw [Matrix.transpose_mul];noncomm_ring
    _ = U*(t • axis j)*U.transpose := by rw [he]
    _ = t • (U*axis j*U.transpose) := by simp [Matrix.mul_smul,Matrix.smul_mul]
    _ = (t*u) • axis l := by rw [hh,smul_smul]

theorem unit_sign_outer_pair_from_parity (c : Fin 4 → ℝ) (hc : UnitSigns c) :
    c 2*c 3=parity c*(c 0*c 1) := by
  unfold parity
  calc
    c 2*c 3=c 0^2*c 1^2*(c 2*c 3) := by rw [hc 0,hc 1];ring
    _ = c 0*c 1*c 2*c 3*(c 0*c 1) := by ring
theorem unit_sign_inner_pair_from_parity (c : Fin 4 → ℝ) (hc : UnitSigns c) :
    c 1*c 2=parity c*(c 0*c 3) := by
  unfold parity
  calc
    c 1*c 2=c 0^2*c 3^2*(c 1*c 2) := by rw [hc 0,hc 3];ring
    _ = c 0*c 1*c 2*c 3*(c 0*c 3) := by ring
def axisColumn (k : Fin 3) : Fin 4 := ![1,2,3] k
def reverseAxisPermutation (k : Fin 3) : Fin 3 := ![2,1,0] k
def forwardAxisPermutation (k : Fin 3) : Fin 3 := ![0,2,1] k
theorem all_proper_signed_comparators_permute_the_owned_left_axes
    (c : Fin 4 → ℝ) (hc : UnitSigns c) (hpar : parity c=-1) (k : Fin 3) :
    signedComparison c*axis k*(signedComparison c).transpose=
      (c 0*c (axisColumn k)) • axis (reverseAxisPermutation k) := by
  have h01 := unit_sign_outer_pair_from_parity c hc
  have h02 := unit_sign_pair_product_from_parity c hc
  have h03 := unit_sign_inner_pair_from_parity c hc
  rw [hpar] at h01 h02 h03
  fin_cases k <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [signedComparison,axis,reverseAxisPermutation,axisColumn,spin_value_0,spin_value_1,spin_value_2,spin_value_3,spin_value_4,spin_value_5,spin_value_6,spin_value_7,
      Matrix.cons_val_two,Matrix.cons_val_three,Matrix.cons_val_four,Matrix.cons_val_succ',
      D0.Representation.OrderMemoryReadout.left,Matrix.map_apply,Matrix.transpose,Matrix.transpose_apply,
      Matrix.smul_apply,Matrix.mul_apply,Matrix.vecMul,dotProduct,Fin.sum_univ_succ] <;>
    nlinarith only [h01,h02,h03]
theorem all_proper_signed_recordings_permute_the_owned_left_axes
    (d : Fin 4 → ℝ) (hd : UnitSigns d) (hpar : parity d=-1) (k : Fin 3) :
    signedRecording d*axis k*(signedRecording d).transpose=
      (d 0*d (axisColumn k)) • axis (forwardAxisPermutation k) := by
  have h01 := unit_sign_outer_pair_from_parity d hd
  have h02 := unit_sign_pair_product_from_parity d hd
  have h03 := unit_sign_inner_pair_from_parity d hd
  rw [hpar] at h01 h02 h03
  fin_cases k <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [signedRecording,axis,forwardAxisPermutation,axisColumn,spin_value_0,spin_value_1,spin_value_2,spin_value_3,spin_value_4,spin_value_5,spin_value_6,spin_value_7,
      Matrix.cons_val_two,Matrix.cons_val_three,Matrix.cons_val_four,Matrix.cons_val_succ',
      D0.Representation.OrderMemoryReadout.left,Matrix.map_apply,Matrix.transpose,Matrix.transpose_apply,
      Matrix.smul_apply,Matrix.mul_apply,Matrix.vecMul,dotProduct,Fin.sum_univ_succ] <;>
    nlinarith only [h01,h02,h03]
theorem every_proper_minimal_comparator_normalizes_axes
    (c : Fin 4 → ℝ) (hc : UnitSigns c) (hpar : parity c=-1) :
    NormalizesAxes (signedComparison c) := by
  intro k
  exact ⟨reverseAxisPermutation k,c 0*c (axisColumn k),sign_products_have_unit_square c hc _ _,
    all_proper_signed_comparators_permute_the_owned_left_axes c hc hpar k⟩
theorem every_proper_minimal_recording_normalizes_axes
    (d : Fin 4 → ℝ) (hd : UnitSigns d) (hpar : parity d=-1) :
    NormalizesAxes (signedRecording d) := by
  intro k
  exact ⟨forwardAxisPermutation k,d 0*d (axisColumn k),sign_products_have_unit_square d hd _ _,
    all_proper_signed_recordings_permute_the_owned_left_axes d hd hpar k⟩

def q8AxisSign (g : Fin 8) (k : Fin 3) : ℝ :=
  if g.val<2 ∨ g.val/2=k.val+1 then 1 else -1
theorem every_owned_q8_frame_normalizes_the_axes_without_compiler_trust (g : Fin 8) :
    NormalizesAxes (q8Frame g) := by
  intro k
  refine ⟨k,q8AxisSign g k,?_,?_⟩
  · unfold q8AxisSign;split <;> norm_num
  · fin_cases g <;> fin_cases k <;> ext i j <;> fin_cases i <;> fin_cases j <;>
      norm_num [q8Frame,q8AxisSign,axis,spin_value_0,spin_value_1,spin_value_2,spin_value_3,spin_value_4,spin_value_5,spin_value_6,spin_value_7,
      Matrix.cons_val_two,Matrix.cons_val_three,Matrix.cons_val_four,Matrix.cons_val_succ',
        D0.Representation.OrderMemoryReadout.left,Matrix.map_apply,Matrix.transpose,Matrix.transpose_apply,
        Matrix.smul_apply,Matrix.mul_apply,Matrix.vecMul,dotProduct,Fin.sum_univ_succ]

def Palette (c d : Fin 4 → ℝ) (A : M4) : Prop :=
  A=signedComparison c ∨ A=signedRecording d ∨ (∃ g,A=q8Frame g) ∨
    ∃ a p,a^2+p^2=1 ∧ A=goldenSystemGate a p
def completeWord : List M4 → M4
  | [] => 1
  | A::w => A*completeWord w
theorem all_proper_palette_primitives_normalize_axes (c d : Fin 4 → ℝ)
    (hc : UnitSigns c) (hd : UnitSigns d) (hpc : parity c=-1) (hpd : parity d=-1)
    (A : M4) (hA : Palette c d A) : NormalizesAxes A := by
  rcases hA with rfl|rfl|⟨g,rfl⟩|⟨a,p,hn,rfl⟩
  · exact every_proper_minimal_comparator_normalizes_axes c hc hpc
  · exact every_proper_minimal_recording_normalizes_axes d hd hpd
  · exact every_owned_q8_frame_normalizes_the_axes_without_compiler_trust g
  · exact all_normalized_active_rotations_normalize_the_owned_axes a p hn
theorem every_complete_word_of_any_length_in_the_proper_palette_normalizes_axes
    (c d : Fin 4 → ℝ) (hc : UnitSigns c) (hd : UnitSigns d)
    (hpc : parity c=-1) (hpd : parity d=-1)
    (w : List M4) (hw : ∀ A∈w,Palette c d A) : NormalizesAxes (completeWord w) := by
  induction w with
  | nil => exact identity_normalizes_axes
  | cons A w ih =>
    exact normalization_is_closed_under_complete_composition A (completeWord w)
      (all_proper_palette_primitives_normalize_axes c d hc hd hpc hpd A (hw A (by simp)))
      (ih (by intro B hB;exact hw B (by simp [hB])))

theorem a_signed_axis_is_in_the_finite_frame_set (k : Fin 3) (t : ℝ) (ht : t^2=1) :
    t • axis k∈AxisSet := by
  rcases sq_eq_one_iff.mp ht with h|h
  · rw [h,one_smul];exact Or.inl ⟨k,rfl⟩
  · rw [h,neg_one_smul];exact Or.inr ⟨k,rfl⟩
theorem the_complete_signed_q8_axis_set_is_closed : IsClosed AxisSet :=
  ((Set.finite_range axis).union (Set.finite_range (fun k : Fin 3 => -axis k))).isClosed
theorem normalization_is_closed_under_full_matrix_limits
    (W : ℕ → M4) (H : M4) (hW : ∀ n,NormalizesAxes (W n))
    (hlim : Tendsto W atTop (𝓝 H)) (k : Fin 3) : H*axis k*H.transpose∈AxisSet := by
  have hseq : ∀ n,W n*axis k*(W n).transpose∈AxisSet := by
    intro n;obtain ⟨j,t,ht,he⟩ := hW n k
    rw [he];exact a_signed_axis_is_in_the_finite_frame_set j t ht
  have hcont : Continuous (fun V : M4 => V*axis k*V.transpose) :=
    (continuous_id.mul continuous_const).mul continuous_id.matrix_transpose
  exact the_complete_signed_q8_axis_set_is_closed.mem_of_tendsto
    (hcont.continuousAt.tendsto.comp hlim) (Filter.Eventually.of_forall hseq)

theorem old_memory_golden_rotation_leaves_the_finite_q8_axis_set
    (a p : ℝ) (hcos : a^2-p^2≠0) (hsin : a*p≠0) :
    goldenRecordGate a p*axis 1*(goldenRecordGate a p).transpose∉AxisSet := by
  rintro (⟨k,hk⟩|⟨k,hk⟩)
  all_goals
    have h02 := congrArg (fun M : M4 => M 0 2) hk
    have h03 := congrArg (fun M : M4 => M 0 3) hk
    fin_cases k <;>
      norm_num [axis,goldenRecordGate,spin_value_0,spin_value_1,spin_value_2,spin_value_3,spin_value_4,spin_value_5,spin_value_6,spin_value_7,
      Matrix.cons_val_two,Matrix.cons_val_three,Matrix.cons_val_four,Matrix.cons_val_succ',
        D0.Representation.OrderMemoryReadout.left,Matrix.map_apply,Matrix.transpose,Matrix.transpose_apply,
        Matrix.mul_apply,Matrix.vecMul,dotProduct,Fin.sum_univ_succ] at h02 h03
    all_goals
      first
      | apply hcos;linarith only [h02]
      | apply hsin;linarith only [h03]
theorem all_word_no_go_for_the_complete_proper_minimal_real_palette
    (c d : Fin 4 → ℝ) (hc : UnitSigns c) (hd : UnitSigns d)
    (hpc : parity c=-1) (hpd : parity d=-1) (a p : ℝ)
    (hcos : a^2-p^2≠0) (hsin : a*p≠0)
    (w : List M4) (hw : ∀ A∈w,Palette c d A) : completeWord w≠goldenRecordGate a p := by
  intro he
  have hn := every_complete_word_of_any_length_in_the_proper_palette_normalizes_axes
    c d hc hd hpc hpd w hw
  rw [he] at hn
  obtain ⟨j,t,ht,hj⟩ := hn 1
  apply old_memory_golden_rotation_leaves_the_finite_q8_axis_set a p hcos hsin
  rw [hj];exact a_signed_axis_is_in_the_finite_frame_set j t ht
theorem arbitrarily_long_proper_programmes_cannot_converge_to_the_old_memory_gate
    (c d : Fin 4 → ℝ) (hc : UnitSigns c) (hd : UnitSigns d)
    (hpc : parity c=-1) (hpd : parity d=-1) (a p : ℝ)
    (hcos : a^2-p^2≠0) (hsin : a*p≠0)
    (w : ℕ → List M4) (hw : ∀ n,∀ A∈w n,Palette c d A) :
    ¬ Tendsto (fun n => completeWord (w n)) atTop (𝓝 (goldenRecordGate a p)) := by
  intro hlim
  have hn := fun n => every_complete_word_of_any_length_in_the_proper_palette_normalizes_axes
    c d hc hd hpc hpd (w n) (hw n)
  exact old_memory_golden_rotation_leaves_the_finite_q8_axis_set a p hcos hsin
    (normalization_is_closed_under_full_matrix_limits _ _ hn hlim 1)
end
end D0.Research.UniformMemoryActuation

set_option autoImplicit false
set_option maxHeartbeats 2000000
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.UniformMemoryActuation
noncomputable section
open Matrix Filter Topology
open D0.Research.GoldenCoherentAmplification D0.Research.VerifiedArchiveActuation
open D0.Research.GoldenProgramCompilation D0.Research.GoldenHistoryPreparation

theorem signed_recording_is_complete_orthogonal (d : Fin 4 → ℝ) (hd : ∀ i,d i^2=1) :
    (signedRecording d).transpose*signedRecording d=1 := by
  ext i j;fin_cases i <;> fin_cases j <;>
    simp [signedRecording,Matrix.transpose_apply,Matrix.mul_apply,Fin.sum_univ_succ,pow_two] <;>
    nlinarith [hd 0,hd 1,hd 2,hd 3]
theorem any_fourth_order_orthogonal_gate_has_a_forward_inverse (U : M4)
    (hu : U.transpose*U=1) (h4 : U^4=1) : U.transpose=U^3 := by
  calc
    U.transpose=U.transpose*1 := by simp
    _ = U.transpose*U^4 := by rw [h4]
    _ = U^3 := by rw [pow_succ',← Matrix.mul_assoc,hu,one_mul]
theorem every_signed_comparator_inverse_has_no_new_primitive (c : Fin 4 → ℝ)
    (hc : ∀ i,c i^2=1) : (signedComparison c).transpose=(signedComparison c)^3 :=
  any_fourth_order_orthogonal_gate_has_a_forward_inverse _
    (every_four_signed_columns_realize_the_same_exact_comparison c hc).1
    (signed_comparison_inverse_is_three_forward_operations c hc)
theorem every_signed_recording_inverse_has_no_new_primitive (d : Fin 4 → ℝ)
    (hd : ∀ i,d i^2=1) : (signedRecording d).transpose=(signedRecording d)^3 :=
  any_fourth_order_orthogonal_gate_has_a_forward_inverse _
    (signed_recording_is_complete_orthogonal d hd)
    (signed_recording_inverse_is_three_forward_operations d hd)
def forwardProgramme (U F G : M4) : List M4 :=
  [U,F,U,G,U,U,U,F,F,F,U,U,U]
theorem uniform_actuation_programme_has_thirteen_forward_operations (U F G : M4) :
    (forwardProgramme U F G).length=13 := rfl
theorem every_uniform_programme_is_the_complete_conjugation (c d : Fin 4 → ℝ)
    (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1) (G : M4) :
    completeWord (forwardProgramme (signedComparison c) (signedRecording d) G)=
      (signedComparison c*signedRecording d*signedComparison c)*G*
        (signedComparison c*signedRecording d*signedComparison c).transpose := by
  rw [Matrix.transpose_mul,Matrix.transpose_mul,
    every_signed_comparator_inverse_has_no_new_primitive c hc,
    every_signed_recording_inverse_has_no_new_primitive d hd]
  simp only [forwardProgramme,completeWord,pow_succ]
  noncomm_ring
theorem the_thirteen_operation_reverse_route_transfers_the_same_angle
    (c d : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (hpd : parity d=1) (a p : ℝ) :
    completeWord (forwardProgramme (signedComparison c) (signedRecording d) (goldenSystemGate a p))=
      goldenRecordGate a (d 0*d 2*c 2*c 3*p) := by
  rw [every_uniform_programme_is_the_complete_conjugation c d hc hd]
  exact complete_uniform_memory_transfer_for_all_reverse_phases c d hc hd hpd a p
theorem the_thirteen_operation_alternate_route_transfers_the_same_angle
    (c d : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (hpc : parity c=1) (a p : ℝ) :
    completeWord (forwardProgramme (signedRecording d) (signedComparison c) (goldenSystemGate a p))=
      goldenRecordGate a (c 0*c 3*d 1*d 2*p) := by
  have htU := every_signed_comparator_inverse_has_no_new_primitive c hc
  have htF := every_signed_recording_inverse_has_no_new_primitive d hd
  have he : completeWord (forwardProgramme (signedRecording d) (signedComparison c) (goldenSystemGate a p))=
      (signedRecording d*signedComparison c*signedRecording d)*goldenSystemGate a p*
        (signedRecording d*signedComparison c*signedRecording d).transpose := by
    rw [Matrix.transpose_mul,Matrix.transpose_mul,htU,htF]
    simp only [forwardProgramme,completeWord,pow_succ]
    noncomm_ring
  rw [he]
  exact alternate_uniform_memory_transfer_for_all_forward_phases c d hc hd hpc a p
theorem whole_joint_family_has_a_constructive_or_all_word_obstructed_parity_class
    (c d : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1) :
    (parity d=1 ∨ parity c=1) ∨ (parity c=-1 ∧ parity d=-1) := by
  rcases sign_parity_is_only_plus_or_minus_one c hc with h|h
  · exact Or.inl (Or.inr h)
  · rcases sign_parity_is_only_plus_or_minus_one d hd with hh|hh
    · exact Or.inl (Or.inl hh)
    · exact Or.inr ⟨h,hh⟩
theorem constant_thirteen_operation_expansion_keeps_the_owned_golden_resource_window
    (A : ℝ) (c : ℕ) : ∀ᶠ m : ℕ in atTop,13*A*(m : ℝ)^c*9^m≤D0.phi^(5*m) :=
  actual_expanded_compiler_cost_eventually_fits_owned_phi (13*A) c

def phiReference (a p : ℝ) : Fin 4 → ℝ := ![a,p,0,0]
def newFlagWeight (x : Fin 4 → ℝ) : ℝ := x 2^2+x 3^2
theorem independent_owned_angle_reference_distinguishes_the_two_memory_orientations
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (a p σ : ℝ)
    (ha : a^2=p) (hσ : σ^2=1) :
    newFlagWeight ((signedComparison c).mulVec
      ((goldenRecordGate a (σ*p)).mulVec (phiReference a p)))=2*p^3*(1+σ) := by
  simp [newFlagWeight,phiReference,signedComparison,goldenRecordGate,Matrix.mulVec,
    dotProduct,Fin.sum_univ_succ,Matrix.cons_val_two,Matrix.cons_val_three]
  ring_nf
  simp [hc,ha,hσ]
  ring
theorem self_preparation_erases_the_orientation_distinction
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (a p σ : ℝ)
    (ha : a^2=p) (hσ : σ^2=1) :
    newFlagWeight ((signedComparison c).mulVec
      ((goldenRecordGate a (σ*p)).mulVec (phiReference a (σ*p))))=4*p^3 := by
  simp [newFlagWeight,phiReference,signedComparison,goldenRecordGate,Matrix.mulVec,
    dotProduct,Fin.sum_univ_succ,Matrix.cons_val_two,Matrix.cons_val_three]
  ring_nf
  simp [hc,ha,hσ]
  ring
theorem actual_p0_has_nonzero_left_axis_rotation_coefficients :
    (Real.sqrt D0.primitiveRoot)^2-D0.primitiveRoot^2≠0 ∧
      Real.sqrt D0.primitiveRoot*D0.primitiveRoot≠0 := by
  have hp0 := D0.Representation.GoldenOrderInterferometer.primitive_positive
  have hp := D0.primitive_root_satisfies
  have hp1 : D0.primitiveRoot<1 := by nlinarith [sq_nonneg D0.primitiveRoot]
  have ha := Real.sq_sqrt (le_of_lt hp0)
  have hh : 0<D0.primitiveRoot*(1-D0.primitiveRoot) := mul_pos hp0 (by linarith)
  constructor
  · nlinarith
  · exact ne_of_gt (mul_pos (Real.sqrt_pos.2 hp0) hp0)
theorem actual_p0_is_unreachable_by_every_complete_proper_palette_word
    (c d : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (hpc : parity c=-1) (hpd : parity d=-1)
    (w : List M4) (hw : ∀ A∈w,Palette c d A) :
    completeWord w≠goldenRecordGate (Real.sqrt D0.primitiveRoot) D0.primitiveRoot :=
  all_word_no_go_for_the_complete_proper_minimal_real_palette c d hc hd hpc hpd _ _
    actual_p0_has_nonzero_left_axis_rotation_coefficients.1
    actual_p0_has_nonzero_left_axis_rotation_coefficients.2 w hw
theorem actual_p0_cannot_be_approached_by_increasing_proper_programme_lengths
    (c d : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (hpc : parity c=-1) (hpd : parity d=-1)
    (w : ℕ → List M4) (hw : ∀ n,∀ A∈w n,Palette c d A) :
    ¬ Tendsto (fun n => completeWord (w n)) atTop
      (𝓝 (goldenRecordGate (Real.sqrt D0.primitiveRoot) D0.primitiveRoot)) :=
  arbitrarily_long_proper_programmes_cannot_converge_to_the_old_memory_gate c d hc hd hpc hpd _ _
    actual_p0_has_nonzero_left_axis_rotation_coefficients.1
    actual_p0_has_nonzero_left_axis_rotation_coefficients.2 w hw
theorem complete_golden_refinement_retains_every_full_programme_error
    (W H : M4) (a p : ℝ) (hn : a^2+p^2=1) (n : ℕ) (x : Fin 4 → ℝ) :
    (∑ s,((wholeHistoryOperator W n).mulVec (realHistoryInclusion a p n x)-
      (wholeHistoryOperator H n).mulVec (realHistoryInclusion a p n x)) s^2)=
      ∑ i,(W.mulVec x-H.mulVec x) i^2 := by
  rw [literal_golden_refinement_intertwines_every_complete_old_operator,
    literal_golden_refinement_intertwines_every_complete_old_operator,
    ← literal_golden_refinement_subtracts_without_reset,
    literal_golden_refinement_preserves_full_real_weight a p hn]
end
end D0.Research.UniformMemoryActuation

set_option autoImplicit false
set_option maxHeartbeats 2000000
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.AddressedThirdRole
noncomputable section
open Matrix
open D0.Research.GoldenCoherentAmplification D0.Research.VerifiedArchiveActuation
open D0.Research.RetainedRecordAdmission D0.Research.UniformMemoryActuation
def activeX : M4 := !![0,0,1,0;0,0,0,1;1,0,0,0;0,1,0,0]
def activeJ : M4 := goldenSystemGate 0 1
def recordJ : M4 := goldenRecordGate 0 1

theorem proper_forward_moves_active_turn_to_correlated_target
    (d : Fin 4 → ℝ) (hd : ∀ i,d i^2=1) (hp : parity d=-1) :
    signedRecording d*activeJ*(signedRecording d).transpose=(d 0*d 2) • (activeX*recordJ) := by
  have h := unit_sign_pair_product_from_parity d hd
  rw [hp] at h
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [signedRecording,activeJ,goldenSystemGate,activeX,recordJ,goldenRecordGate,
      Matrix.transpose,Matrix.mul_apply,Matrix.vecMul,dotProduct,Matrix.smul_apply,Fin.sum_univ_succ] <;>
    nlinarith only [h]
theorem proper_reverse_correlates_active_flip_with_record_phase
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hp : parity c=-1) :
    signedComparison c*activeX*(signedComparison c).transpose=(c 0*c 2) • (activeX*recordZ) := by
  have h := unit_sign_pair_product_from_parity c hc
  rw [hp] at h
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [signedComparison,activeX,recordZ,
      Matrix.transpose,Matrix.mul_apply,Matrix.vecMul,dotProduct,Matrix.smul_apply,Fin.sum_univ_succ] <;>
    nlinarith only [h]
theorem proper_forward_turns_active_flip_record_phase_into_both_flips
    (d : Fin 4 → ℝ) (hd : ∀ i,d i^2=1) (hp : parity d=-1) :
    signedRecording d*(activeX*recordZ)*(signedRecording d).transpose=
      (d 0*d 2) • (activeX*archiveX) := by
  have h := unit_sign_pair_product_from_parity d hd
  rw [hp] at h
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [signedRecording,activeX,recordZ,archiveX,
      Matrix.transpose,Matrix.mul_apply,Matrix.vecMul,dotProduct,Matrix.smul_apply,Fin.sum_univ_succ] <;>
    nlinarith only [h]
theorem proper_forward_uncorrelates_the_target_turn
    (d : Fin 4 → ℝ) (hd : ∀ i,d i^2=1) (hp : parity d=-1) :
    signedRecording d*(activeX*recordJ)*(signedRecording d).transpose=(d 0*d 3) • activeJ := by
  have h := unit_sign_inner_pair_from_parity d hd
  rw [hp] at h
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [signedRecording,activeJ,goldenSystemGate,activeX,recordJ,goldenRecordGate,
      Matrix.transpose,Matrix.mul_apply,Matrix.vecMul,dotProduct,Matrix.smul_apply,Fin.sum_univ_succ] <;>
    nlinarith only [h]
theorem proper_reverse_uncorrelates_both_roles_into_record_turn
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hp : parity c=-1) :
    signedComparison c*(activeJ*archiveX)*(signedComparison c).transpose=(c 0*c 3) • recordJ := by
  have h := unit_sign_inner_pair_from_parity c hc
  rw [hp] at h
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [signedComparison,activeJ,goldenSystemGate,recordJ,goldenRecordGate,archiveX,
      Matrix.transpose,Matrix.mul_apply,Matrix.vecMul,dotProduct,Matrix.smul_apply,Fin.sum_univ_succ] <;>
    nlinarith only [h]
end
end D0.Research.AddressedThirdRole

set_option autoImplicit false
set_option maxHeartbeats 3000000
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.AddressedThirdRole
noncomputable section
open Matrix
open D0.Research.GoldenCoherentAmplification D0.Research.VerifiedArchiveActuation
open D0.Research.RetainedRecordAdmission D0.Research.UniformMemoryActuation
abbrev Triple := Fin 2 × (Fin 2 × Fin 2)
abbrev M8 := Matrix Triple Triple ℝ
abbrev M2 := Matrix (Fin 2) (Fin 2) ℝ
def pair (a r : Fin 2) : Fin 4 := finProdFinEquiv (a,r)
def lift01 (A : M4) : M8 := fun i j => A (pair i.1 i.2.1) (pair j.1 j.2.1)*
  (if i.2.2=j.2.2 then 1 else 0)
def lift02 (A : M4) : M8 := fun i j => A (pair i.1 i.2.2) (pair j.1 j.2.2)*
  (if i.2.1=j.2.1 then 1 else 0)
def tensor (A B C : M2) : M8 := fun i j => A i.1 j.1*B i.2.1 j.2.1*C i.2.2 j.2.2
def two (A B : M2) : M4 := fun i j =>
  A ((finProdFinEquiv : Fin 2 × Fin 2 ≃ Fin 4).symm i).1 ((finProdFinEquiv : Fin 2 × Fin 2 ≃ Fin 4).symm j).1*
    B ((finProdFinEquiv : Fin 2 × Fin 2 ≃ Fin 4).symm i).2 ((finProdFinEquiv : Fin 2 × Fin 2 ≃ Fin 4).symm j).2
def X : M2 := !![0,1;1,0]
def Z : M2 := !![1,0;0,-1]
def J : M2 := !![0,-1;1,0]

theorem first_pair_lift_keeps_complete_composition (A B : M4) : lift01 (A*B)=lift01 A*lift01 B := by
  ext i j
  rcases i with ⟨a,r,s⟩;rcases j with ⟨b,q,t⟩
  fin_cases a <;> fin_cases r <;> fin_cases s <;> fin_cases b <;> fin_cases q <;> fin_cases t <;>
    norm_num [lift01,pair,finProdFinEquiv,Matrix.mul_apply,Fintype.sum_prod_type,Fin.sum_univ_succ] <;> ring!
theorem second_pair_lift_keeps_complete_composition (A B : M4) : lift02 (A*B)=lift02 A*lift02 B := by
  ext i j
  rcases i with ⟨a,r,s⟩;rcases j with ⟨b,q,t⟩
  fin_cases a <;> fin_cases r <;> fin_cases s <;> fin_cases b <;> fin_cases q <;> fin_cases t <;>
    norm_num [lift02,pair,finProdFinEquiv,Matrix.mul_apply,Fintype.sum_prod_type,Fin.sum_univ_succ] <;> ring!
theorem first_pair_lift_keeps_complete_transpose (A : M4) : lift01 A.transpose=(lift01 A).transpose := by
  ext i j
  simp [lift01,Matrix.transpose,eq_comm]
theorem second_pair_lift_keeps_complete_transpose (A : M4) : lift02 A.transpose=(lift02 A).transpose := by
  ext i j
  simp [lift02,Matrix.transpose,eq_comm]
theorem first_pair_lift_keeps_scalar (A : M4) (t : ℝ) : lift01 (t • A)=t • lift01 A := by
  ext i j;simp [lift01,Matrix.smul_apply,mul_assoc]
theorem second_pair_lift_keeps_scalar (A : M4) (t : ℝ) : lift02 (t • A)=t • lift02 A := by
  ext i j;simp [lift02,Matrix.smul_apply,mul_assoc]
theorem first_pair_lift_keeps_identity : lift01 (1 : M4)=(1 : M8) := by
  ext i j
  rcases i with ⟨a,r,s⟩;rcases j with ⟨b,q,t⟩
  fin_cases a <;> fin_cases r <;> fin_cases s <;> fin_cases b <;> fin_cases q <;> fin_cases t <;>
    norm_num [lift01,pair,finProdFinEquiv,Matrix.one_apply]
theorem second_pair_lift_keeps_identity : lift02 (1 : M4)=(1 : M8) := by
  ext i j
  rcases i with ⟨a,r,s⟩;rcases j with ⟨b,q,t⟩
  fin_cases a <;> fin_cases r <;> fin_cases s <;> fin_cases b <;> fin_cases q <;> fin_cases t <;>
    norm_num [lift02,pair,finProdFinEquiv,Matrix.one_apply]
theorem first_pair_lift_keeps_conjugation (A B : M4) :
    lift01 A*lift01 B*(lift01 A).transpose=lift01 (A*B*A.transpose) := by
  rw [← first_pair_lift_keeps_complete_transpose,← first_pair_lift_keeps_complete_composition,
    ← first_pair_lift_keeps_complete_composition]
theorem second_pair_lift_keeps_conjugation (A B : M4) :
    lift02 A*lift02 B*(lift02 A).transpose=lift02 (A*B*A.transpose) := by
  rw [← second_pair_lift_keeps_complete_transpose,← second_pair_lift_keeps_complete_composition,
    ← second_pair_lift_keeps_complete_composition]
theorem concrete_native_four_coordinates_are_the_literal_two_role_tensor :
    activeJ=two J 1 ∧ recordJ=two 1 J ∧ activeX=two X 1 ∧
      archiveX=two 1 X ∧ recordZ=two 1 Z := by
  refine ⟨?_,?_,?_,?_,?_⟩ <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [activeJ,recordJ,activeX,goldenSystemGate,goldenRecordGate,archiveX,recordZ,
      two,finProdFinEquiv,Fin.divNat,Fin.modNat,J,X,Z,Matrix.one_apply]
end
end D0.Research.AddressedThirdRole

set_option autoImplicit false
set_option maxHeartbeats 3000000
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.AddressedThirdRole
noncomputable section
open Matrix
open D0.Research.GoldenCoherentAmplification D0.Research.VerifiedArchiveActuation
open D0.Research.RetainedRecordAdmission D0.Research.UniformMemoryActuation
def withLast (A : M4) (D : M2) : M8 := fun i j =>
  A (pair i.1 i.2.1) (pair j.1 j.2.1)*D i.2.2 j.2.2
def withMiddle (A : M4) (D : M2) : M8 := fun i j =>
  A (pair i.1 i.2.2) (pair j.1 j.2.2)*D i.2.1 j.2.1
theorem lift01_is_a_complete_identity_spectator (A : M4) : lift01 A=withLast A 1 := by
  ext i j;simp [lift01,withLast,Matrix.one_apply]
theorem lift02_is_a_complete_identity_spectator (A : M4) : lift02 A=withMiddle A 1 := by
  ext i j;simp [lift02,withMiddle,Matrix.one_apply]
theorem spectator_last_complete_multiplication (A B : M4) (C D : M2) :
    withLast A C*withLast B D=withLast (A*B) (C*D) := by
  ext i j
  rcases i with ⟨a,r,s⟩;rcases j with ⟨b,q,t⟩
  fin_cases a <;> fin_cases r <;> fin_cases s <;> fin_cases b <;> fin_cases q <;> fin_cases t <;>
    norm_num [withLast,pair,finProdFinEquiv,Matrix.mul_apply,Fintype.sum_prod_type,Fin.sum_univ_succ] <;> ring!
theorem spectator_middle_complete_multiplication (A B : M4) (C D : M2) :
    withMiddle A C*withMiddle B D=withMiddle (A*B) (C*D) := by
  ext i j
  rcases i with ⟨a,r,s⟩;rcases j with ⟨b,q,t⟩
  fin_cases a <;> fin_cases r <;> fin_cases s <;> fin_cases b <;> fin_cases q <;> fin_cases t <;>
    norm_num [withMiddle,pair,finProdFinEquiv,Matrix.mul_apply,Fintype.sum_prod_type,Fin.sum_univ_succ] <;> ring!
theorem tensor_first_pair_with_full_spectator (A B C : M2) : withLast (two A B) C=tensor A B C := by
  ext i j;simp [withLast,two,tensor,pair]
theorem tensor_second_pair_with_full_spectator (A B C : M2) : withMiddle (two A C) B=tensor A B C := by
  ext i j;simp [withMiddle,two,tensor,pair,mul_assoc,mul_comm,mul_left_comm]
theorem with_last_keeps_all_scalar_factors (A : M4) (D : M2) (s : ℝ) :
    withLast (s • A) D=s • withLast A D := by ext i j;simp [withLast,Matrix.smul_apply,mul_assoc]
theorem with_middle_keeps_all_scalar_factors (A : M4) (D : M2) (s : ℝ) :
    withMiddle (s • A) D=s • withMiddle A D := by ext i j;simp [withMiddle,Matrix.smul_apply,mul_assoc]
theorem complete_first_pair_conjugation_retains_arbitrary_spectator
    (F A : M4) (D : M2) : lift01 F*withLast A D*(lift01 F).transpose=
      withLast (F*A*F.transpose) D := by
  rw [← first_pair_lift_keeps_complete_transpose,lift01_is_a_complete_identity_spectator,
    lift01_is_a_complete_identity_spectator,spectator_last_complete_multiplication,
    spectator_last_complete_multiplication,one_mul,mul_one]
theorem complete_second_pair_conjugation_retains_arbitrary_spectator
    (F A : M4) (D : M2) : lift02 F*withMiddle A D*(lift02 F).transpose=
      withMiddle (F*A*F.transpose) D := by
  rw [← second_pair_lift_keeps_complete_transpose,lift02_is_a_complete_identity_spectator,
    lift02_is_a_complete_identity_spectator,spectator_middle_complete_multiplication,
    spectator_middle_complete_multiplication,one_mul,mul_one]
theorem the_complete_four_role_products_are_literal_pauli_tensors :
    activeX*recordJ=two X J ∧ activeX*recordZ=two X Z ∧
      activeX*archiveX=two X X ∧ activeJ*archiveX=two J X := by
  refine ⟨?_,?_,?_,?_⟩ <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [activeJ,recordJ,activeX,goldenSystemGate,goldenRecordGate,archiveX,recordZ,
      two,finProdFinEquiv,Fin.divNat,Fin.modNat,J,X,Z,
      Matrix.mul_apply,Matrix.vecMul,dotProduct,Fin.sum_univ_succ]
end
end D0.Research.AddressedThirdRole

set_option autoImplicit false
set_option maxHeartbeats 3000000
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.AddressedThirdRole
noncomputable section
open Matrix
open D0.Research.GoldenCoherentAmplification D0.Research.VerifiedArchiveActuation
open D0.Research.RetainedRecordAdmission D0.Research.UniformMemoryActuation

theorem first_coherent_recording_moves_the_turn_to_the_additional_role
    (e : Fin 4 → ℝ) (he : ∀ i,e i^2=1) (hp : parity e=-1) :
    lift02 (signedRecording e)*tensor J 1 1*(lift02 (signedRecording e)).transpose=
      (e 0*e 2) • tensor X 1 J := by
  rw [← tensor_second_pair_with_full_spectator J 1 1,
    ← concrete_native_four_coordinates_are_the_literal_two_role_tensor.1,
    complete_second_pair_conjugation_retains_arbitrary_spectator,
    proper_forward_moves_active_turn_to_correlated_target e he hp,
    with_middle_keeps_all_scalar_factors,the_complete_four_role_products_are_literal_pauli_tensors.1,
    tensor_second_pair_with_full_spectator]
theorem old_record_comparison_adds_the_retained_record_phase
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hp : parity c=-1) :
    lift01 (signedComparison c)*tensor X 1 J*(lift01 (signedComparison c)).transpose=
      (c 0*c 2) • tensor X Z J := by
  rw [← tensor_first_pair_with_full_spectator X 1 J,
    ← concrete_native_four_coordinates_are_the_literal_two_role_tensor.2.2.1,
    complete_first_pair_conjugation_retains_arbitrary_spectator,
    proper_reverse_correlates_active_flip_with_record_phase c hc hp,
    with_last_keeps_all_scalar_factors,the_complete_four_role_products_are_literal_pauli_tensors.2.1,
    tensor_first_pair_with_full_spectator]
theorem original_recording_relocates_the_two_role_flip
    (d : Fin 4 → ℝ) (hd : ∀ i,d i^2=1) (hp : parity d=-1) :
    lift01 (signedRecording d)*tensor X Z J*(lift01 (signedRecording d)).transpose=
      (d 0*d 2) • tensor X X J := by
  rw [← tensor_first_pair_with_full_spectator X Z J,
    ← the_complete_four_role_products_are_literal_pauli_tensors.2.1,
    complete_first_pair_conjugation_retains_arbitrary_spectator,
    proper_forward_turns_active_flip_record_phase_into_both_flips d hd hp,
    with_last_keeps_all_scalar_factors,the_complete_four_role_products_are_literal_pauli_tensors.2.2.1,
    tensor_first_pair_with_full_spectator]
theorem additional_recording_uncorrelates_its_complete_role
    (e : Fin 4 → ℝ) (he : ∀ i,e i^2=1) (hp : parity e=-1) :
    lift02 (signedRecording e)*tensor X X J*(lift02 (signedRecording e)).transpose=
      (e 0*e 3) • tensor J X 1 := by
  rw [← tensor_second_pair_with_full_spectator X X J,
    ← the_complete_four_role_products_are_literal_pauli_tensors.1,
    complete_second_pair_conjugation_retains_arbitrary_spectator,
    proper_forward_uncorrelates_the_target_turn e he hp,
    with_middle_keeps_all_scalar_factors,concrete_native_four_coordinates_are_the_literal_two_role_tensor.1,
    tensor_second_pair_with_full_spectator]
theorem final_old_record_comparison_uncorrelates_the_active_role
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hp : parity c=-1) :
    lift01 (signedComparison c)*tensor J X 1*(lift01 (signedComparison c)).transpose=
      (c 0*c 3) • tensor 1 J 1 := by
  rw [← tensor_first_pair_with_full_spectator J X 1,
    ← the_complete_four_role_products_are_literal_pauli_tensors.2.2.2,
    complete_first_pair_conjugation_retains_arbitrary_spectator,
    proper_reverse_uncorrelates_both_roles_into_record_turn c hc hp,
    with_last_keeps_all_scalar_factors,concrete_native_four_coordinates_are_the_literal_two_role_tensor.2.1,
    tensor_first_pair_with_full_spectator]
def conjugate (A B : M8) : M8 := A*B*A.transpose
theorem full_conjugation_composes_without_a_reset (A B Q : M8) :
    conjugate (A*B) Q=conjugate A (conjugate B Q) := by
  unfold conjugate;rw [Matrix.transpose_mul];noncomm_ring
theorem full_conjugation_keeps_its_scalar_factor (A Q : M8) (t : ℝ) :
    conjugate A (t • Q)=t • conjugate A Q := by
  simp [conjugate,Matrix.mul_smul,Matrix.smul_mul]
def fiveStep (c d e : Fin 4 → ℝ) : M8 :=
  lift01 (signedComparison c)*lift02 (signedRecording e)*lift01 (signedRecording d)*
    lift01 (signedComparison c)*lift02 (signedRecording e)
def fiveOrientation (c d e : Fin 4 → ℝ) : ℝ :=
  (e 0*e 2)*(c 0*c 2)*(d 0*d 2)*(e 0*e 3)*(c 0*c 3)
theorem all_complete_proper_three_role_realizations_have_the_same_five_step_turn_transfer
    (c d e : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1) (he : ∀ i,e i^2=1)
    (hpc : parity c=-1) (hpd : parity d=-1) (hpe : parity e=-1) :
    conjugate (fiveStep c d e) (tensor J 1 1)=fiveOrientation c d e • tensor 1 J 1 := by
  unfold fiveStep
  simp only [full_conjugation_composes_without_a_reset]
  change conjugate (lift01 (signedComparison c))
    (conjugate (lift02 (signedRecording e))
      (conjugate (lift01 (signedRecording d))
        (conjugate (lift01 (signedComparison c))
          (conjugate (lift02 (signedRecording e)) (tensor J 1 1)))))=_
  have h1 := first_coherent_recording_moves_the_turn_to_the_additional_role e he hpe
  have h2 := old_record_comparison_adds_the_retained_record_phase c hc hpc
  have h3 := original_recording_relocates_the_two_role_flip d hd hpd
  have h4 := additional_recording_uncorrelates_its_complete_role e he hpe
  have h5 := final_old_record_comparison_uncorrelates_the_active_role c hc hpc
  change conjugate _ (tensor J 1 1)=_ at h1
  change conjugate _ (tensor X 1 J)=_ at h2
  change conjugate _ (tensor X Z J)=_ at h3
  change conjugate _ (tensor X X J)=_ at h4
  change conjugate _ (tensor J X 1)=_ at h5
  simp only [h1,h2,h3,h4,h5,full_conjugation_keeps_its_scalar_factor,smul_smul]
  congr 1
theorem five_step_orientation_is_only_a_sign (c d e : Fin 4 → ℝ)
    (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1) (he : ∀ i,e i^2=1) :
    fiveOrientation c d e^2=1 := by simp [fiveOrientation,mul_pow,hc,hd,he]
end
end D0.Research.AddressedThirdRole

set_option autoImplicit false
set_option maxHeartbeats 3000000
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.AddressedThirdRole
noncomputable section
open Matrix Filter Topology
open D0.Research.GoldenCoherentAmplification D0.Research.VerifiedArchiveActuation
open D0.Research.RetainedRecordAdmission D0.Research.UniformMemoryActuation

theorem first_address_preserves_full_orthogonality (A : M4) (ha : A.transpose*A=1) :
    (lift01 A).transpose*lift01 A=1 := by
  rw [← first_pair_lift_keeps_complete_transpose,← first_pair_lift_keeps_complete_composition,
    ha,first_pair_lift_keeps_identity]
theorem additional_address_preserves_full_orthogonality (A : M4) (ha : A.transpose*A=1) :
    (lift02 A).transpose*lift02 A=1 := by
  rw [← second_pair_lift_keeps_complete_transpose,← second_pair_lift_keeps_complete_composition,
    ha,second_pair_lift_keeps_identity]
theorem two_complete_orthogonal_operations_remain_orthogonal (A B : M8)
    (ha : A.transpose*A=1) (hb : B.transpose*B=1) :
    (A*B).transpose*(A*B)=1 := by
  rw [Matrix.transpose_mul]
  calc
    B.transpose*A.transpose*(A*B)=B.transpose*(A.transpose*A)*B := by noncomm_ring
    _ = 1 := by rw [ha,mul_one,hb]
theorem every_five_step_route_is_complete_orthogonal
    (c d e : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1) (he : ∀ i,e i^2=1) :
    (fiveStep c d e).transpose*fiveStep c d e=1 := by
  have hu := first_address_preserves_full_orthogonality _
    (every_four_signed_columns_realize_the_same_exact_comparison c hc).1
  have hf := first_address_preserves_full_orthogonality _ (signed_recording_is_complete_orthogonal d hd)
  have hg := additional_address_preserves_full_orthogonality _ (signed_recording_is_complete_orthogonal e he)
  unfold fiveStep
  exact two_complete_orthogonal_operations_remain_orthogonal _ _
    (two_complete_orthogonal_operations_remain_orthogonal _ _
      (two_complete_orthogonal_operations_remain_orthogonal _ _
        (two_complete_orthogonal_operations_remain_orthogonal _ _ hu hg) hf) hu) hg

def activeTurn (a p : ℝ) : M8 := a • (1 : M8)+p • tensor J 1 1
def oldTurn (a p : ℝ) : M8 := a • (1 : M8)+p • tensor 1 J 1

theorem every_complete_conjugation_retains_its_identity_component (A : M8)
    (ha : A.transpose*A=1) (a p : ℝ) :
    conjugate A (activeTurn a p)=a • (1 : M8)+p • conjugate A (tensor J 1 1) := by
  have hi : A*A.transpose=1 := mul_eq_one_comm.1 ha
  simp [activeTurn,conjugate,Matrix.mul_add,Matrix.add_mul,Matrix.mul_smul,Matrix.smul_mul,hi]
theorem complete_five_step_actuation_restores_both_other_roles_for_every_full_state
    (c d e : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1) (he : ∀ i,e i^2=1)
    (hpc : parity c=-1) (hpd : parity d=-1) (hpe : parity e=-1) (a p : ℝ) :
    conjugate (fiveStep c d e) (activeTurn a p)=oldTurn a (fiveOrientation c d e*p) := by
  rw [every_complete_conjugation_retains_its_identity_component _
    (every_five_step_route_is_complete_orthogonal c d e hc hd he),
    all_complete_proper_three_role_realizations_have_the_same_five_step_turn_transfer c d e hc hd he hpc hpd hpe]
  simp [oldTurn,smul_smul,mul_comm]

theorem first_address_preserves_three_forward_inverse (A : M4) (ha : A.transpose=A^3) :
    (lift01 A).transpose=(lift01 A)^3 := by
  rw [← first_pair_lift_keeps_complete_transpose,ha]
  simp only [pow_succ,pow_zero,mul_one,first_pair_lift_keeps_complete_composition,first_pair_lift_keeps_identity]
theorem additional_address_preserves_three_forward_inverse (A : M4) (ha : A.transpose=A^3) :
    (lift02 A).transpose=(lift02 A)^3 := by
  rw [← second_pair_lift_keeps_complete_transpose,ha]
  simp only [pow_succ,pow_zero,mul_one,second_pair_lift_keeps_complete_composition,second_pair_lift_keeps_identity]
def word8 : List M8 → M8
  | [] => 1
  | A::w => A*word8 w
def forwardCode (B A C G : M8) : List M8 :=
  [B,A,C,B,A,G,A,A,A,B,B,B,C,C,C,A,A,A,B,B,B]
theorem complete_three_role_actuation_has_twenty_one_forward_operations (B A C G : M8) :
    (forwardCode B A C G).length=21 := rfl

theorem complete_forward_code_has_no_inverse_or_reset_primitive
    (c d e : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1) (he : ∀ i,e i^2=1) (G : M8) :
    word8 (forwardCode (lift01 (signedComparison c)) (lift02 (signedRecording e))
      (lift01 (signedRecording d)) G)=conjugate (fiveStep c d e) G := by
  have hu := first_address_preserves_three_forward_inverse _ (every_signed_comparator_inverse_has_no_new_primitive c hc)
  have hf := first_address_preserves_three_forward_inverse _ (every_signed_recording_inverse_has_no_new_primitive d hd)
  have hg := additional_address_preserves_three_forward_inverse _ (every_signed_recording_inverse_has_no_new_primitive e he)
  unfold fiveStep conjugate
  rw [Matrix.transpose_mul,Matrix.transpose_mul,Matrix.transpose_mul,Matrix.transpose_mul,hu,hf,hg]
  simp only [forwardCode,word8,pow_succ,pow_zero,mul_one]
  noncomm_ring

theorem forward_code_transfers_the_angle_on_the_entire_eight_coordinate_workspace
    (c d e : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1) (he : ∀ i,e i^2=1)
    (hpc : parity c=-1) (hpd : parity d=-1) (hpe : parity e=-1) (a p : ℝ) :
    word8 (forwardCode (lift01 (signedComparison c)) (lift02 (signedRecording e))
      (lift01 (signedRecording d)) (activeTurn a p))=oldTurn a (fiveOrientation c d e*p) := by
  rw [complete_forward_code_has_no_inverse_or_reset_primitive c d e hc hd he]
  exact complete_five_step_actuation_restores_both_other_roles_for_every_full_state c d e hc hd he hpc hpd hpe a p
end
end D0.Research.AddressedThirdRole

set_option autoImplicit false
set_option maxHeartbeats 3000000
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.AddressedThirdRole
noncomputable section
open Matrix
open D0.Research.GoldenCoherentAmplification D0.Research.VerifiedArchiveActuation
open D0.Research.RetainedRecordAdmission D0.Research.UniformMemoryActuation

theorem unit_sign_adjacent_pair_from_parity (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) :
    c 2*c 3=parity c*(c 0*c 1) := by
  unfold parity
  calc
    c 2*c 3=c 0^2*c 1^2*(c 2*c 3) := by rw [hc 0,hc 1];ring
    _ = c 0*c 1*c 2*c 3*(c 0*c 1) := by ring

theorem positive_forward_correlates_active_turn
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hp : parity c=1) :
    signedRecording c*(activeJ)*(signedRecording c).transpose=(c 0*c 2) • (activeJ*archiveX) := by
  have h1 := unit_sign_pair_product_from_parity c hc
  have h2 := unit_sign_inner_pair_from_parity c hc
  have h3 := unit_sign_adjacent_pair_from_parity c hc
  rw [hp] at h1 h2 h3
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [signedRecording,signedComparison,activeJ,goldenSystemGate,activeX,recordJ,goldenRecordGate,
      archiveX,recordZ,Matrix.transpose,Matrix.mul_apply,Matrix.vecMul,dotProduct,Matrix.smul_apply,Fin.sum_univ_succ] <;>
    nlinarith only [h1,h2,h3]

theorem positive_reverse_uncorrelates_both_flips
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hp : parity c=1) :
    signedComparison c*(activeX*archiveX)*(signedComparison c).transpose=(c 0*c 3) • (archiveX) := by
  have h1 := unit_sign_pair_product_from_parity c hc
  have h2 := unit_sign_inner_pair_from_parity c hc
  have h3 := unit_sign_adjacent_pair_from_parity c hc
  rw [hp] at h1 h2 h3
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [signedRecording,signedComparison,activeJ,goldenSystemGate,activeX,recordJ,goldenRecordGate,
      archiveX,recordZ,Matrix.transpose,Matrix.mul_apply,Matrix.vecMul,dotProduct,Matrix.smul_apply,Fin.sum_univ_succ] <;>
    nlinarith only [h1,h2,h3]

theorem proper_reverse_turns_record_into_active_correlation
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hp : parity c=-1) :
    signedComparison c*(recordJ)*(signedComparison c).transpose=(c 0*c 1) • (activeJ*archiveX) := by
  have h1 := unit_sign_pair_product_from_parity c hc
  have h2 := unit_sign_inner_pair_from_parity c hc
  have h3 := unit_sign_adjacent_pair_from_parity c hc
  rw [hp] at h1 h2 h3
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [signedRecording,signedComparison,activeJ,goldenSystemGate,activeX,recordJ,goldenRecordGate,
      archiveX,recordZ,Matrix.transpose,Matrix.mul_apply,Matrix.vecMul,dotProduct,Matrix.smul_apply,Fin.sum_univ_succ] <;>
    nlinarith only [h1,h2,h3]

theorem proper_reverse_uncorrelates_both_turns
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hp : parity c=-1) :
    signedComparison c*(activeJ*recordJ)*(signedComparison c).transpose=(c 0*c 3) • (archiveX) := by
  have h1 := unit_sign_pair_product_from_parity c hc
  have h2 := unit_sign_inner_pair_from_parity c hc
  have h3 := unit_sign_adjacent_pair_from_parity c hc
  rw [hp] at h1 h2 h3
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [signedRecording,signedComparison,activeJ,goldenSystemGate,activeX,recordJ,goldenRecordGate,
      archiveX,recordZ,Matrix.transpose,Matrix.mul_apply,Matrix.vecMul,dotProduct,Matrix.smul_apply,Fin.sum_univ_succ] <;>
    nlinarith only [h1,h2,h3]

theorem positive_forward_correlates_flip_phase_into_both_turns
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hp : parity c=1) :
    signedRecording c*(activeX*recordZ)*(signedRecording c).transpose=(c 0*c 2) • (activeJ*recordJ) := by
  have h1 := unit_sign_pair_product_from_parity c hc
  have h2 := unit_sign_inner_pair_from_parity c hc
  have h3 := unit_sign_adjacent_pair_from_parity c hc
  rw [hp] at h1 h2 h3
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [signedRecording,signedComparison,activeJ,goldenSystemGate,activeX,recordJ,goldenRecordGate,
      archiveX,recordZ,Matrix.transpose,Matrix.mul_apply,Matrix.vecMul,dotProduct,Matrix.smul_apply,Fin.sum_univ_succ] <;>
    nlinarith only [h1,h2,h3]

theorem positive_forward_uncorrelates_active_turn
    (c : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hp : parity c=1) :
    signedRecording c*(activeJ*archiveX)*(signedRecording c).transpose=(c 0*c 3) • (activeJ) := by
  have h1 := unit_sign_pair_product_from_parity c hc
  have h2 := unit_sign_inner_pair_from_parity c hc
  have h3 := unit_sign_adjacent_pair_from_parity c hc
  rw [hp] at h1 h2 h3
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [signedRecording,signedComparison,activeJ,goldenSystemGate,activeX,recordJ,goldenRecordGate,
      archiveX,recordZ,Matrix.transpose,Matrix.mul_apply,Matrix.vecMul,dotProduct,Matrix.smul_apply,Fin.sum_univ_succ] <;>
    nlinarith only [h1,h2,h3]

theorem both_native_turns_are_the_complete_tensor : activeJ*recordJ=two J J := by
  ext i j;fin_cases i <;> fin_cases j <;>
    norm_num [activeJ,recordJ,goldenSystemGate,goldenRecordGate,two,finProdFinEquiv,
      Fin.divNat,Fin.modNat,J,Matrix.mul_apply,Fin.sum_univ_succ]
end
end D0.Research.AddressedThirdRole

set_option autoImplicit false
set_option maxHeartbeats 3000000
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.AddressedThirdRole
noncomputable section
open Matrix
open D0.Research.GoldenCoherentAmplification D0.Research.VerifiedArchiveActuation
open D0.Research.RetainedRecordAdmission D0.Research.UniformMemoryActuation

theorem positive_additional_recording_correlates_the_active_turn (v : Fin 4 → ℝ)
    (hv : ∀ i,v i^2=1) (hp : parity v=1) :
    conjugate (lift02 (signedRecording v)) (tensor J 1 1)=
      (v 0*v 2) • tensor J 1 X := by
  have h := positive_forward_correlates_active_turn v hv hp
  rw [the_complete_four_role_products_are_literal_pauli_tensors.2.2.2,concrete_native_four_coordinates_are_the_literal_two_role_tensor.1] at h
  unfold conjugate
  rw [← tensor_second_pair_with_full_spectator J 1 1,complete_second_pair_conjugation_retains_arbitrary_spectator,h,with_middle_keeps_all_scalar_factors,tensor_second_pair_with_full_spectator]

theorem proper_original_recording_correlates_the_active_turn (v : Fin 4 → ℝ)
    (hv : ∀ i,v i^2=1) (hp : parity v=-1) :
    conjugate (lift01 (signedRecording v)) (tensor J 1 X)=
      (v 0*v 2) • tensor X J X := by
  have h := proper_forward_moves_active_turn_to_correlated_target v hv hp
  rw [concrete_native_four_coordinates_are_the_literal_two_role_tensor.1,the_complete_four_role_products_are_literal_pauli_tensors.1] at h
  unfold conjugate
  rw [← tensor_first_pair_with_full_spectator J 1 X,complete_first_pair_conjugation_retains_arbitrary_spectator,h,with_last_keeps_all_scalar_factors,tensor_first_pair_with_full_spectator]

theorem positive_additional_comparison_uncorrelates_both_flips (v : Fin 4 → ℝ)
    (hv : ∀ i,v i^2=1) (hp : parity v=1) :
    conjugate (lift02 (signedComparison v)) (tensor X J X)=
      (v 0*v 3) • tensor 1 J X := by
  have h := positive_reverse_uncorrelates_both_flips v hv hp
  rw [the_complete_four_role_products_are_literal_pauli_tensors.2.2.1,concrete_native_four_coordinates_are_the_literal_two_role_tensor.2.2.2.1] at h
  unfold conjugate
  rw [← tensor_second_pair_with_full_spectator X J X,complete_second_pair_conjugation_retains_arbitrary_spectator,h,with_middle_keeps_all_scalar_factors,tensor_second_pair_with_full_spectator]

theorem proper_old_record_comparison_moves_its_turn_back_to_active (v : Fin 4 → ℝ)
    (hv : ∀ i,v i^2=1) (hp : parity v=-1) :
    conjugate (lift01 (signedComparison v)) (tensor 1 J X)=
      (v 0*v 1) • tensor J X X := by
  have h := proper_reverse_turns_record_into_active_correlation v hv hp
  rw [concrete_native_four_coordinates_are_the_literal_two_role_tensor.2.1,the_complete_four_role_products_are_literal_pauli_tensors.2.2.2] at h
  unfold conjugate
  rw [← tensor_first_pair_with_full_spectator 1 J X,complete_first_pair_conjugation_retains_arbitrary_spectator,h,with_last_keeps_all_scalar_factors,tensor_first_pair_with_full_spectator]

theorem positive_additional_recording_restores_its_complete_role (v : Fin 4 → ℝ)
    (hv : ∀ i,v i^2=1) (hp : parity v=1) :
    conjugate (lift02 (signedRecording v)) (tensor J X X)=
      (v 0*v 3) • tensor J X 1 := by
  have h := positive_forward_uncorrelates_active_turn v hv hp
  rw [the_complete_four_role_products_are_literal_pauli_tensors.2.2.2,concrete_native_four_coordinates_are_the_literal_two_role_tensor.1] at h
  unfold conjugate
  rw [← tensor_second_pair_with_full_spectator J X X,complete_second_pair_conjugation_retains_arbitrary_spectator,h,with_middle_keeps_all_scalar_factors,tensor_second_pair_with_full_spectator]

theorem proper_original_recording_starts_the_mixed_route (v : Fin 4 → ℝ)
    (hv : ∀ i,v i^2=1) (hp : parity v=-1) :
    conjugate (lift01 (signedRecording v)) (tensor J 1 1)=
      (v 0*v 2) • tensor X J 1 := by
  have h := proper_forward_moves_active_turn_to_correlated_target v hv hp
  rw [concrete_native_four_coordinates_are_the_literal_two_role_tensor.1,the_complete_four_role_products_are_literal_pauli_tensors.1] at h
  unfold conjugate
  rw [← tensor_first_pair_with_full_spectator J 1 1,complete_first_pair_conjugation_retains_arbitrary_spectator,h,with_last_keeps_all_scalar_factors,tensor_first_pair_with_full_spectator]

theorem proper_additional_comparison_retains_the_old_record_turn (v : Fin 4 → ℝ)
    (hv : ∀ i,v i^2=1) (hp : parity v=-1) :
    conjugate (lift02 (signedComparison v)) (tensor X J 1)=
      (v 0*v 2) • tensor X J Z := by
  have h := proper_reverse_correlates_active_flip_with_record_phase v hv hp
  rw [the_complete_four_role_products_are_literal_pauli_tensors.2.1,concrete_native_four_coordinates_are_the_literal_two_role_tensor.2.2.1] at h
  unfold conjugate
  rw [← tensor_second_pair_with_full_spectator X J 1,complete_second_pair_conjugation_retains_arbitrary_spectator,h,with_middle_keeps_all_scalar_factors,tensor_second_pair_with_full_spectator]

theorem positive_additional_recording_correlates_both_turns (v : Fin 4 → ℝ)
    (hv : ∀ i,v i^2=1) (hp : parity v=1) :
    conjugate (lift02 (signedRecording v)) (tensor X J Z)=
      (v 0*v 2) • tensor J J J := by
  have h := positive_forward_correlates_flip_phase_into_both_turns v hv hp
  rw [the_complete_four_role_products_are_literal_pauli_tensors.2.1,both_native_turns_are_the_complete_tensor] at h
  unfold conjugate
  rw [← tensor_second_pair_with_full_spectator X J Z,complete_second_pair_conjugation_retains_arbitrary_spectator,h,with_middle_keeps_all_scalar_factors,tensor_second_pair_with_full_spectator]

theorem proper_old_record_comparison_uncorrelates_both_turns (v : Fin 4 → ℝ)
    (hv : ∀ i,v i^2=1) (hp : parity v=-1) :
    conjugate (lift01 (signedComparison v)) (tensor J J J)=
      (v 0*v 3) • tensor 1 X J := by
  have h := proper_reverse_uncorrelates_both_turns v hv hp
  rw [both_native_turns_are_the_complete_tensor,concrete_native_four_coordinates_are_the_literal_two_role_tensor.2.2.2.1] at h
  unfold conjugate
  rw [← tensor_first_pair_with_full_spectator J J J,complete_first_pair_conjugation_retains_arbitrary_spectator,h,with_last_keeps_all_scalar_factors,tensor_first_pair_with_full_spectator]

theorem proper_additional_comparison_moves_its_turn_back_to_active (v : Fin 4 → ℝ)
    (hv : ∀ i,v i^2=1) (hp : parity v=-1) :
    conjugate (lift02 (signedComparison v)) (tensor 1 X J)=
      (v 0*v 1) • tensor J X X := by
  have h := proper_reverse_turns_record_into_active_correlation v hv hp
  rw [concrete_native_four_coordinates_are_the_literal_two_role_tensor.2.1,the_complete_four_role_products_are_literal_pauli_tensors.2.2.2] at h
  unfold conjugate
  rw [← tensor_second_pair_with_full_spectator 1 X J,complete_second_pair_conjugation_retains_arbitrary_spectator,h,with_middle_keeps_all_scalar_factors,tensor_second_pair_with_full_spectator]

def sixStep (c d e f : Fin 4 → ℝ) : M8 :=
  lift01 (signedComparison c)*lift02 (signedRecording e)*lift01 (signedComparison c)*
    lift02 (signedComparison f)*lift01 (signedRecording d)*lift02 (signedRecording e)
def sixOrientation (c d e f : Fin 4 → ℝ) : ℝ :=
  (e 0*e 2)*(d 0*d 2)*(f 0*f 3)*(c 0*c 1)*(e 0*e 3)*(c 0*c 3)
theorem all_complete_positive_helper_pairs_transfer_the_turn_in_six_steps
    (c d e f : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (he : ∀ i,e i^2=1) (hf : ∀ i,f i^2=1)
    (hpc : parity c=-1) (hpd : parity d=-1) (hpe : parity e=1) (hpf : parity f=1) :
    conjugate (sixStep c d e f) (tensor J 1 1)=sixOrientation c d e f • tensor 1 J 1 := by
  have h1 := positive_additional_recording_correlates_the_active_turn e he hpe
  have h2 := proper_original_recording_correlates_the_active_turn d hd hpd
  have h3 := positive_additional_comparison_uncorrelates_both_flips f hf hpf
  have h4 := proper_old_record_comparison_moves_its_turn_back_to_active c hc hpc
  have h5 := positive_additional_recording_restores_its_complete_role e he hpe
  have h6 := final_old_record_comparison_uncorrelates_the_active_role c hc hpc
  change conjugate _ (tensor J X 1)=_ at h6
  unfold sixStep
  simp only [full_conjugation_composes_without_a_reset,h1,h2,h3,h4,h5,h6,
    full_conjugation_keeps_its_scalar_factor,smul_smul]
  congr 1
  unfold sixOrientation;ring

def sevenStep (c d e f : Fin 4 → ℝ) : M8 :=
  lift01 (signedComparison c)*lift02 (signedRecording e)*lift02 (signedComparison f)*
    lift01 (signedComparison c)*lift02 (signedRecording e)*lift02 (signedComparison f)*
      lift01 (signedRecording d)
def sevenOrientation (c d e f : Fin 4 → ℝ) : ℝ :=
  (d 0*d 2)*(f 0*f 2)*(e 0*e 2)*(c 0*c 3)*(f 0*f 1)*(e 0*e 3)*(c 0*c 3)
theorem all_complete_mixed_helper_pairs_transfer_the_turn_in_seven_steps
    (c d e f : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (he : ∀ i,e i^2=1) (hf : ∀ i,f i^2=1)
    (hpc : parity c=-1) (hpd : parity d=-1) (hpe : parity e=1) (hpf : parity f=-1) :
    conjugate (sevenStep c d e f) (tensor J 1 1)=sevenOrientation c d e f • tensor 1 J 1 := by
  have h1 := proper_original_recording_starts_the_mixed_route d hd hpd
  have h2 := proper_additional_comparison_retains_the_old_record_turn f hf hpf
  have h3 := positive_additional_recording_correlates_both_turns e he hpe
  have h4 := proper_old_record_comparison_uncorrelates_both_turns c hc hpc
  have h5 := proper_additional_comparison_moves_its_turn_back_to_active f hf hpf
  have h6 := positive_additional_recording_restores_its_complete_role e he hpe
  have h7 := final_old_record_comparison_uncorrelates_the_active_role c hc hpc
  change conjugate _ (tensor J X 1)=_ at h7
  unfold sevenStep
  simp only [full_conjugation_composes_without_a_reset,h1,h2,h3,h4,h5,h6,h7,
    full_conjugation_keeps_its_scalar_factor,smul_smul]
  congr 1
  unfold sevenOrientation;ring

theorem complete_positive_helper_route_orientation_is_a_sign
    (c d e f : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (he : ∀ i,e i^2=1) (hf : ∀ i,f i^2=1) : sixOrientation c d e f^2=1 := by
  simp [sixOrientation,mul_pow,hc,hd,he,hf]
theorem complete_mixed_helper_route_orientation_is_a_sign
    (c d e f : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (he : ∀ i,e i^2=1) (hf : ∀ i,f i^2=1) : sevenOrientation c d e f^2=1 := by
  simp [sevenOrientation,mul_pow,hc,hd,he,hf]
end
end D0.Research.AddressedThirdRole

set_option autoImplicit false
set_option maxHeartbeats 3000000
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.AddressedThirdRole
noncomputable section
open Matrix Filter Topology
open D0.Research.GoldenCoherentAmplification D0.Research.VerifiedArchiveActuation
open D0.Research.RetainedRecordAdmission D0.Research.UniformMemoryActuation

def AddressedPrimitive (c d e f : Fin 4 → ℝ) (A : M8) : Prop :=
  A=lift01 (signedComparison c) ∨ A=lift01 (signedRecording d) ∨
    A=lift02 (signedRecording e) ∨ A=lift02 (signedComparison f)
theorem every_addressed_primitive_preserves_the_complete_workspace
    (c d e f : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (he : ∀ i,e i^2=1) (hf : ∀ i,f i^2=1) (A : M8)
    (ha : AddressedPrimitive c d e f A) : A.transpose*A=1 := by
  rcases ha with h|h|h|h <;> subst A
  · exact first_address_preserves_full_orthogonality _ (every_four_signed_columns_realize_the_same_exact_comparison c hc).1
  · exact first_address_preserves_full_orthogonality _ (signed_recording_is_complete_orthogonal d hd)
  · exact additional_address_preserves_full_orthogonality _ (signed_recording_is_complete_orthogonal e he)
  · exact additional_address_preserves_full_orthogonality _ (every_four_signed_columns_realize_the_same_exact_comparison f hf).1

theorem every_addressed_primitive_has_a_three_forward_inverse
    (c d e f : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (he : ∀ i,e i^2=1) (hf : ∀ i,f i^2=1) (A : M8)
    (ha : AddressedPrimitive c d e f A) : A.transpose=A^3 := by
  rcases ha with h|h|h|h <;> subst A
  · exact first_address_preserves_three_forward_inverse _ (every_signed_comparator_inverse_has_no_new_primitive c hc)
  · exact first_address_preserves_three_forward_inverse _ (every_signed_recording_inverse_has_no_new_primitive d hd)
  · exact additional_address_preserves_three_forward_inverse _ (every_signed_recording_inverse_has_no_new_primitive e he)
  · exact additional_address_preserves_three_forward_inverse _ (every_signed_comparator_inverse_has_no_new_primitive f hf)

theorem complete_workspace_word_keeps_composition (u v : List M8) : word8 (u++v)=word8 u*word8 v := by
  induction u with
  | nil => simp [word8]
  | cons A u ih => simp [word8,ih,Matrix.mul_assoc]

theorem every_complete_addressed_word_remains_orthogonal
    (c d e f : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (he : ∀ i,e i^2=1) (hf : ∀ i,f i^2=1) (w : List M8)
    (hw : ∀ A∈w,AddressedPrimitive c d e f A) : (word8 w).transpose*word8 w=1 := by
  induction w with
  | nil => simp [word8]
  | cons A w ih =>
    exact two_complete_orthogonal_operations_remain_orthogonal _ _
      (every_addressed_primitive_preserves_the_complete_workspace c d e f hc hd he hf A (hw A (by simp)))
      (ih (by intro B hb;exact hw B (by simp [hb])))

def inverseForward8 : List M8 → List M8
  | [] => []
  | A::w => inverseForward8 w++[A,A,A]
theorem every_full_word_inverse_uses_only_the_same_forward_primitives
    (c d e f : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (he : ∀ i,e i^2=1) (hf : ∀ i,f i^2=1) (w : List M8)
    (hw : ∀ A∈w,AddressedPrimitive c d e f A) :
    word8 (inverseForward8 w)=(word8 w).transpose := by
  induction w with
  | nil => simp [inverseForward8,word8]
  | cons A w ih =>
    have hi := ih (by intro B hb;exact hw B (by simp [hb]))
    have ha := every_addressed_primitive_has_a_three_forward_inverse c d e f hc hd he hf A (hw A (by simp))
    rw [inverseForward8,complete_workspace_word_keeps_composition,hi]
    simp only [word8,Matrix.transpose_mul,ha,pow_succ,pow_zero,mul_one]
    noncomm_ring

theorem inverse_forward_code_retains_its_exact_length (w : List M8) : (inverseForward8 w).length=3*w.length := by
  induction w with
  | nil => simp [inverseForward8]
  | cons A w ih => simp [inverseForward8,ih];omega

def compileConjugation (w : List M8) (G : M8) : List M8 := w++[G]++inverseForward8 w
theorem full_actuation_compiler_has_four_times_route_length_plus_one (w : List M8) (G : M8) :
    (compileConjugation w G).length=4*w.length+1 := by
  simp [compileConjugation,inverse_forward_code_retains_its_exact_length];omega

theorem full_actuation_compiler_keeps_the_complete_conjugation
    (c d e f : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (he : ∀ i,e i^2=1) (hf : ∀ i,f i^2=1) (w : List M8)
    (hw : ∀ A∈w,AddressedPrimitive c d e f A) (G : M8) :
    word8 (compileConjugation w G)=conjugate (word8 w) G := by
  rw [compileConjugation,complete_workspace_word_keeps_composition,complete_workspace_word_keeps_composition,
    every_full_word_inverse_uses_only_the_same_forward_primitives c d e f hc hd he hf w hw]
  simp [word8,conjugate]

theorem inverse_forward_code_keeps_the_complete_primitive_palette
    (c d e f : Fin 4 → ℝ) (w : List M8)
    (hw : ∀ A∈w,AddressedPrimitive c d e f A) :
    ∀ A∈inverseForward8 w,AddressedPrimitive c d e f A := by
  induction w with
  | nil => simp [inverseForward8]
  | cons B w ih =>
    intro A ha
    have hb := hw B (by simp)
    have hit := ih (by intro C hc;exact hw C (by simp [hc]))
    simp only [inverseForward8,List.mem_append,List.mem_cons,List.not_mem_nil,or_false] at ha
    rcases ha with h|h|h|h
    · exact hit A h
    all_goals simpa [h] using hb

theorem full_actuation_compiler_introduces_only_the_owned_active_turn
    (c d e f : Fin 4 → ℝ) (w : List M8)
    (hw : ∀ A∈w,AddressedPrimitive c d e f A) (G : M8) :
    ∀ A∈compileConjugation w G,AddressedPrimitive c d e f A ∨ A=G := by
  intro A ha
  have hi := inverse_forward_code_keeps_the_complete_primitive_palette c d e f w hw
  simp only [compileConjugation,List.mem_append,List.mem_cons,List.not_mem_nil,or_false] at ha
  rcases ha with (h|h)|h
  · exact Or.inl (hw A h)
  · exact Or.inr h
  · exact Or.inl (hi A h)
end
end D0.Research.AddressedThirdRole

set_option autoImplicit false
set_option maxHeartbeats 3000000
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.AddressedThirdRole
noncomputable section
open Matrix Filter Topology
open D0.Research.GoldenCoherentAmplification D0.Research.VerifiedArchiveActuation
open D0.Research.RetainedRecordAdmission D0.Research.UniformMemoryActuation
open D0.Research.GoldenProgramCompilation

theorem native_two_role_turns_keep_their_owned_identity_and_generator
    (a p : ℝ) : goldenSystemGate a p=a • (1 : M4)+p • activeJ ∧
      goldenRecordGate a p=a • (1 : M4)+p • recordJ := by
  constructor <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [goldenSystemGate,goldenRecordGate,activeJ,recordJ,Matrix.one_apply,Matrix.smul_apply]
theorem first_address_keeps_the_complete_sum (A B : M4) : lift01 (A+B)=lift01 A+lift01 B := by
  ext i j;by_cases h : i.2.2=j.2.2 <;> simp [lift01,add_mul,h]
theorem addressed_native_turns_are_the_actual_owned_full_operators (a p : ℝ) :
    lift01 (goldenSystemGate a p)=activeTurn a p ∧ lift01 (goldenRecordGate a p)=oldTurn a p := by
  have ha : lift01 activeJ=tensor J 1 1 := by
    rw [lift01_is_a_complete_identity_spectator,concrete_native_four_coordinates_are_the_literal_two_role_tensor.1,
      tensor_first_pair_with_full_spectator]
  have hb : lift01 recordJ=tensor 1 J 1 := by
    rw [lift01_is_a_complete_identity_spectator,concrete_native_four_coordinates_are_the_literal_two_role_tensor.2.1,
      tensor_first_pair_with_full_spectator]
  constructor
  · rw [(native_two_role_turns_keep_their_owned_identity_and_generator a p).1,
      first_address_keeps_the_complete_sum,first_pair_lift_keeps_scalar,
      first_pair_lift_keeps_scalar,first_pair_lift_keeps_identity,ha]
    rfl
  · rw [(native_two_role_turns_keep_their_owned_identity_and_generator a p).2,
      first_address_keeps_the_complete_sum,first_pair_lift_keeps_scalar,
      first_pair_lift_keeps_scalar,first_pair_lift_keeps_identity,hb]
    rfl

theorem addressed_three_step_positive_forward_route_transfers_the_complete_turn
    (c d : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (hpd : parity d=1) :
    conjugate (word8 [lift01 (signedComparison c),lift01 (signedRecording d),lift01 (signedComparison c)])
      (tensor J 1 1)=(d 0*d 2*c 2*c 3) • tensor 1 J 1 := by
  have h := complete_uniform_memory_transfer_for_all_reverse_phases c d hc hd hpd 0 1
  have ht := congrArg lift01 h
  simp only [← first_pair_lift_keeps_conjugation,first_pair_lift_keeps_complete_composition,
    (addressed_native_turns_are_the_actual_owned_full_operators 0 1).1,
    (addressed_native_turns_are_the_actual_owned_full_operators 0 (d 0*d 2*c 2*c 3*1)).2] at ht
  simpa [word8,conjugate,activeTurn,oldTurn,first_pair_lift_keeps_complete_composition,
    first_pair_lift_keeps_complete_transpose,Matrix.mul_assoc] using ht

theorem addressed_three_step_positive_reverse_route_transfers_the_complete_turn
    (c d : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (hpc : parity c=1) :
    conjugate (word8 [lift01 (signedRecording d),lift01 (signedComparison c),lift01 (signedRecording d)])
      (tensor J 1 1)=(c 0*c 3*d 1*d 2) • tensor 1 J 1 := by
  have h := alternate_uniform_memory_transfer_for_all_forward_phases c d hc hd hpc 0 1
  have ht := congrArg lift01 h
  simp only [← first_pair_lift_keeps_conjugation,first_pair_lift_keeps_complete_composition,
    (addressed_native_turns_are_the_actual_owned_full_operators 0 1).1,
    (addressed_native_turns_are_the_actual_owned_full_operators 0 (c 0*c 3*d 1*d 2*1)).2] at ht
  simpa [word8,conjugate,activeTurn,oldTurn,first_pair_lift_keeps_complete_composition,
    first_pair_lift_keeps_complete_transpose,Matrix.mul_assoc] using ht

theorem every_complete_two_address_phase_family_has_a_full_turn_transfer_route
    (c d e f : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (he : ∀ i,e i^2=1) (hf : ∀ i,f i^2=1) :
    ∃ w : List M8,∃ σ : ℝ,w.length≤7 ∧ (∀ A∈w,AddressedPrimitive c d e f A) ∧
      σ^2=1 ∧ conjugate (word8 w) (tensor J 1 1)=σ • tensor 1 J 1 := by
  rcases sign_parity_is_only_plus_or_minus_one d hd with hp|hp
  · refine ⟨[lift01 (signedComparison c),lift01 (signedRecording d),lift01 (signedComparison c)],
      d 0*d 2*c 2*c 3,by simp,?_,?_,addressed_three_step_positive_forward_route_transfers_the_complete_turn c d hc hd hp⟩
    · intro A ha;simp only [List.mem_cons,List.not_mem_nil,or_false] at ha
      rcases ha with h|h|h <;> simp [AddressedPrimitive,h]
    · simp [mul_pow,hc,hd]
  · rcases sign_parity_is_only_plus_or_minus_one c hc with hq|hq
    · refine ⟨[lift01 (signedRecording d),lift01 (signedComparison c),lift01 (signedRecording d)],
        c 0*c 3*d 1*d 2,by simp,?_,?_,addressed_three_step_positive_reverse_route_transfers_the_complete_turn c d hc hd hq⟩
      · intro A ha;simp only [List.mem_cons,List.not_mem_nil,or_false] at ha
        rcases ha with h|h|h <;> simp [AddressedPrimitive,h]
      · simp [mul_pow,hc,hd]
    · rcases sign_parity_is_only_plus_or_minus_one e he with hr|hr
      · rcases sign_parity_is_only_plus_or_minus_one f hf with hs|hs
        · refine ⟨[lift01 (signedComparison c),lift02 (signedRecording e),lift01 (signedComparison c),
            lift02 (signedComparison f),lift01 (signedRecording d),lift02 (signedRecording e)],
            sixOrientation c d e f,by simp,?_,
            complete_positive_helper_route_orientation_is_a_sign c d e f hc hd he hf,?_⟩
          · intro A ha;simp only [List.mem_cons,List.not_mem_nil,or_false] at ha
            rcases ha with h|h|h|h|h|h <;> simp [AddressedPrimitive,h]
          · simpa [word8,sixStep,Matrix.mul_assoc] using all_complete_positive_helper_pairs_transfer_the_turn_in_six_steps c d e f hc hd he hf hq hp hr hs
        · refine ⟨[lift01 (signedComparison c),lift02 (signedRecording e),lift02 (signedComparison f),
            lift01 (signedComparison c),lift02 (signedRecording e),lift02 (signedComparison f),lift01 (signedRecording d)],
            sevenOrientation c d e f,by simp,?_,
            complete_mixed_helper_route_orientation_is_a_sign c d e f hc hd he hf,?_⟩
          · intro A ha;simp only [List.mem_cons,List.not_mem_nil,or_false] at ha
            rcases ha with h|h|h|h|h|h|h <;> simp [AddressedPrimitive,h]
          · simpa [word8,sevenStep,Matrix.mul_assoc] using all_complete_mixed_helper_pairs_transfer_the_turn_in_seven_steps c d e f hc hd he hf hq hp hr hs
      · refine ⟨[lift01 (signedComparison c),lift02 (signedRecording e),lift01 (signedRecording d),
          lift01 (signedComparison c),lift02 (signedRecording e)],fiveOrientation c d e,by simp,?_,
          five_step_orientation_is_only_a_sign c d e hc hd he,?_⟩
        · intro A ha;simp only [List.mem_cons,List.not_mem_nil,or_false] at ha
          rcases ha with h|h|h|h|h <;> simp [AddressedPrimitive,h]
        · simpa [word8,fiveStep,Matrix.mul_assoc] using all_complete_proper_three_role_realizations_have_the_same_five_step_turn_transfer c d e hc hd he hq hp hr

theorem complete_signed_addressed_actuation_is_constructive_with_at_most_twenty_nine_steps
    (c d e f : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (he : ∀ i,e i^2=1) (hf : ∀ i,f i^2=1) (a p : ℝ) :
    ∃ code : List M8,∃ σ : ℝ,code.length≤29 ∧ σ^2=1 ∧
      (∀ A∈code,AddressedPrimitive c d e f A ∨ A=activeTurn a p) ∧
      word8 code=oldTurn a (σ*p) := by
  obtain ⟨w,σ,hl,hpal,hs,htransfer⟩ :=
    every_complete_two_address_phase_family_has_a_full_turn_transfer_route c d e f hc hd he hf
  refine ⟨compileConjugation w (activeTurn a p),σ,?_,hs,
    full_actuation_compiler_introduces_only_the_owned_active_turn c d e f w hpal (activeTurn a p),?_⟩
  · rw [full_actuation_compiler_has_four_times_route_length_plus_one];omega
  · rw [full_actuation_compiler_keeps_the_complete_conjugation c d e f hc hd he hf w hpal,
      every_complete_conjugation_retains_its_identity_component _
        (every_complete_addressed_word_remains_orthogonal c d e f hc hd he hf w hpal),htransfer]
    simp [oldTurn,smul_smul,mul_comm]

theorem actual_owned_golden_angle_requires_no_added_rotation_primitive
    (c d e f : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (he : ∀ i,e i^2=1) (hf : ∀ i,f i^2=1) :
    ∃ code : List M8,∃ σ : ℝ,code.length≤29 ∧ σ^2=1 ∧
      (∀ A∈code,AddressedPrimitive c d e f A ∨ A=lift01
        (goldenSystemGate (Real.sqrt D0.primitiveRoot) D0.primitiveRoot)) ∧
      word8 code=lift01 (goldenRecordGate (Real.sqrt D0.primitiveRoot) (σ*D0.primitiveRoot)) := by
  simpa only [(addressed_native_turns_are_the_actual_owned_full_operators (Real.sqrt D0.primitiveRoot) D0.primitiveRoot).1,
    (addressed_native_turns_are_the_actual_owned_full_operators (Real.sqrt D0.primitiveRoot) _).2] using
    complete_signed_addressed_actuation_is_constructive_with_at_most_twenty_nine_steps c d e f hc hd he hf
      (Real.sqrt D0.primitiveRoot) D0.primitiveRoot

theorem constant_twenty_nine_step_actuation_keeps_the_owned_golden_resource_window
    (A : ℝ) (c : ℕ) : ∀ᶠ m : ℕ in atTop,29*A*(m : ℝ)^c*9^m≤D0.phi^(5*m) :=
  actual_expanded_compiler_cost_eventually_fits_owned_phi (29*A) c
end
end D0.Research.AddressedThirdRole

set_option autoImplicit false
set_option maxHeartbeats 3000000
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.AddressedThirdRole
noncomputable section
open Matrix
open D0.Research.GoldenHistoryPreparation D0.Research.VerifiedArchiveActuation

def refinedWord (n : ℕ) : List M8 → Matrix (Triple × Word n) (Triple × Word n) ℝ
  | [] => 1
  | A::w => wholeHistoryOperator A n*refinedWord n w

theorem complete_programme_refinement_keeps_every_forward_primitive (n : ℕ) (w : List M8) :
    refinedWord n w=wholeHistoryOperator (word8 w) n := by
  induction w with
  | nil =>
    simp [refinedWord,word8,wholeHistoryOperator]
  | cons A w ih =>
    rw [refinedWord,ih,complete_old_operator_composition_survives_every_history_depth,word8]

theorem every_addressed_programme_intertwines_every_full_golden_depth
    (w : List M8) (a p : ℝ) (n : ℕ) (x : Triple → ℝ) :
    (refinedWord n w).mulVec (realHistoryInclusion a p n x)=
      realHistoryInclusion a p n ((word8 w).mulVec x) := by
  rw [complete_programme_refinement_keeps_every_forward_primitive,
    literal_golden_refinement_intertwines_every_complete_old_operator]

theorem complete_three_role_programme_error_has_no_refinement_dilution
    (W H : M8) (a p : ℝ) (hn : a^2+p^2=1) (n : ℕ) (x : Triple → ℝ) :
    (∑ s,((wholeHistoryOperator W n).mulVec (realHistoryInclusion a p n x)-
      (wholeHistoryOperator H n).mulVec (realHistoryInclusion a p n x)) s^2)=
      ∑ i,(W.mulVec x-H.mulVec x) i^2 := by
  rw [literal_golden_refinement_intertwines_every_complete_old_operator,
    literal_golden_refinement_intertwines_every_complete_old_operator,
    ← literal_golden_refinement_subtracts_without_reset,
    literal_golden_refinement_preserves_full_real_weight a p hn]

theorem full_constructive_actuation_commutes_with_every_retained_golden_depth
    (c d e f : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1)
    (he : ∀ i,e i^2=1) (hf : ∀ i,f i^2=1) (a p : ℝ) :
    ∃ code : List M8,∃ σ : ℝ,code.length≤29 ∧ σ^2=1 ∧
      (∀ A∈code,AddressedPrimitive c d e f A ∨ A=activeTurn a p) ∧
      ∀ n : ℕ,∀ b q : ℝ,∀ x : Triple → ℝ,
        (refinedWord n code).mulVec (realHistoryInclusion b q n x)=
          realHistoryInclusion b q n ((oldTurn a (σ*p)).mulVec x) := by
  obtain ⟨code,σ,hl,hs,hp,hv⟩ :=
    complete_signed_addressed_actuation_is_constructive_with_at_most_twenty_nine_steps c d e f hc hd he hf a p
  refine ⟨code,σ,hl,hs,hp,?_⟩
  intro n b q x
  rw [every_addressed_programme_intertwines_every_full_golden_depth,hv]
end
end D0.Research.AddressedThirdRole

set_option autoImplicit false
set_option maxHeartbeats 3000000
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
namespace D0.Research.AddressedThirdRole
noncomputable section
open Matrix
open D0.Research.GoldenCoherentAmplification D0.Research.VerifiedArchiveActuation
open D0.Research.RetainedRecordAdmission D0.Research.UniformMemoryActuation

theorem the_complete_two_address_retaining_real_family_has_sixty_five_thousand_five_hundred_thirty_six_realizations :
    Nat.card (({F : M4 // RetainingRealRecording F} × {U : M4 // RetainingRealComparison U}) ×
      ({F : M4 // RetainingRealRecording F} × {U : M4 // RetainingRealComparison U}))=65536 := by
  rw [Nat.card_prod,full_joint_minimal_real_family_has_two_hundred_fifty_six_pairs]

theorem all_functionally_classified_addressed_real_primitives_have_a_complete_workspace_programme
    (F U E V : M4) (hf : RetainingRealRecording F) (hu : RetainingRealComparison U)
    (he : RetainingRealRecording E) (hv : RetainingRealComparison V) (a p : ℝ) :
    ∃ code : List M8,∃ σ : ℝ,code.length≤29 ∧ σ^2=1 ∧
      (∀ A∈code,A=lift01 U ∨ A=lift01 F ∨ A=lift02 E ∨ A=lift02 V ∨ A=activeTurn a p) ∧
      ∀ x : Triple → ℝ,(word8 code).mulVec x=(oldTurn a (σ*p)).mulVec x := by
  obtain ⟨d,hd,rfl⟩ := (complete_minimal_real_recording_classification F).1 hf
  obtain ⟨c,hc,rfl⟩ := (complete_retaining_real_comparison_classification U).1 hu
  obtain ⟨e,heSign,rfl⟩ := (complete_minimal_real_recording_classification E).1 he
  obtain ⟨f,hfSign,rfl⟩ := (complete_retaining_real_comparison_classification V).1 hv
  obtain ⟨code,σ,hl,hs,hpal,hcode⟩ :=
    complete_signed_addressed_actuation_is_constructive_with_at_most_twenty_nine_steps c d e f hc hd heSign hfSign a p
  refine ⟨code,σ,hl,hs,?_,?_⟩
  · intro A ha
    simpa [AddressedPrimitive,or_assoc] using hpal A ha
  · intro x;rw [hcode]

theorem already_owned_common_recording_and_comparison_need_only_thirteen_or_twenty_one_steps
    (c d : Fin 4 → ℝ) (hc : ∀ i,c i^2=1) (hd : ∀ i,d i^2=1) (a p : ℝ) :
    ∃ code : List M8,∃ σ : ℝ,code.length≤21 ∧ σ^2=1 ∧
      (∀ A∈code,AddressedPrimitive c d d c A ∨ A=activeTurn a p) ∧
      word8 code=oldTurn a (σ*p) := by
  have hroute : ∃ w : List M8,∃ σ : ℝ,w.length≤5 ∧
      (∀ A∈w,AddressedPrimitive c d d c A) ∧ σ^2=1 ∧
      conjugate (word8 w) (tensor J 1 1)=σ • tensor 1 J 1 := by
    rcases sign_parity_is_only_plus_or_minus_one d hd with hp|hp
    · refine ⟨[lift01 (signedComparison c),lift01 (signedRecording d),lift01 (signedComparison c)],
        d 0*d 2*c 2*c 3,by simp,?_,?_,addressed_three_step_positive_forward_route_transfers_the_complete_turn c d hc hd hp⟩
      · intro A ha;simp only [List.mem_cons,List.not_mem_nil,or_false] at ha
        rcases ha with h|h|h <;> simp [AddressedPrimitive,h]
      · simp [mul_pow,hc,hd]
    · rcases sign_parity_is_only_plus_or_minus_one c hc with hq|hq
      · refine ⟨[lift01 (signedRecording d),lift01 (signedComparison c),lift01 (signedRecording d)],
          c 0*c 3*d 1*d 2,by simp,?_,?_,addressed_three_step_positive_reverse_route_transfers_the_complete_turn c d hc hd hq⟩
        · intro A ha;simp only [List.mem_cons,List.not_mem_nil,or_false] at ha
          rcases ha with h|h|h <;> simp [AddressedPrimitive,h]
        · simp [mul_pow,hc,hd]
      · refine ⟨[lift01 (signedComparison c),lift02 (signedRecording d),lift01 (signedRecording d),
            lift01 (signedComparison c),lift02 (signedRecording d)],fiveOrientation c d d,by simp,?_,
            five_step_orientation_is_only_a_sign c d d hc hd hd,?_⟩
        · intro A ha;simp only [List.mem_cons,List.not_mem_nil,or_false] at ha
          rcases ha with h|h|h|h|h <;> simp [AddressedPrimitive,h]
        · simpa [word8,fiveStep,Matrix.mul_assoc] using
            all_complete_proper_three_role_realizations_have_the_same_five_step_turn_transfer c d d hc hd hd hq hp hp
  obtain ⟨w,σ,hl,hpal,hs,htransfer⟩ := hroute
  refine ⟨compileConjugation w (activeTurn a p),σ,?_,hs,
    full_actuation_compiler_introduces_only_the_owned_active_turn c d d c w hpal (activeTurn a p),?_⟩
  · rw [full_actuation_compiler_has_four_times_route_length_plus_one];omega
  · rw [full_actuation_compiler_keeps_the_complete_conjugation c d d c hc hd hd hc w hpal,
      every_complete_conjugation_retains_its_identity_component _
        (every_complete_addressed_word_remains_orthogonal c d d c hc hd hd hc w hpal),htransfer]
    simp [oldTurn,smul_smul,mul_comm]
end
end D0.Research.AddressedThirdRole
#check D0.Research.AddressedThirdRole.proper_forward_moves_active_turn_to_correlated_target
#print axioms D0.Research.AddressedThirdRole.proper_forward_moves_active_turn_to_correlated_target
#check D0.Research.AddressedThirdRole.proper_reverse_correlates_active_flip_with_record_phase
#print axioms D0.Research.AddressedThirdRole.proper_reverse_correlates_active_flip_with_record_phase
#check D0.Research.AddressedThirdRole.proper_forward_turns_active_flip_record_phase_into_both_flips
#print axioms D0.Research.AddressedThirdRole.proper_forward_turns_active_flip_record_phase_into_both_flips
#check D0.Research.AddressedThirdRole.proper_forward_uncorrelates_the_target_turn
#print axioms D0.Research.AddressedThirdRole.proper_forward_uncorrelates_the_target_turn
#check D0.Research.AddressedThirdRole.proper_reverse_uncorrelates_both_roles_into_record_turn
#print axioms D0.Research.AddressedThirdRole.proper_reverse_uncorrelates_both_roles_into_record_turn
#check D0.Research.AddressedThirdRole.first_pair_lift_keeps_complete_composition
#print axioms D0.Research.AddressedThirdRole.first_pair_lift_keeps_complete_composition
#check D0.Research.AddressedThirdRole.second_pair_lift_keeps_complete_composition
#print axioms D0.Research.AddressedThirdRole.second_pair_lift_keeps_complete_composition
#check D0.Research.AddressedThirdRole.first_pair_lift_keeps_complete_transpose
#print axioms D0.Research.AddressedThirdRole.first_pair_lift_keeps_complete_transpose
#check D0.Research.AddressedThirdRole.second_pair_lift_keeps_complete_transpose
#print axioms D0.Research.AddressedThirdRole.second_pair_lift_keeps_complete_transpose
#check D0.Research.AddressedThirdRole.first_pair_lift_keeps_scalar
#print axioms D0.Research.AddressedThirdRole.first_pair_lift_keeps_scalar
#check D0.Research.AddressedThirdRole.second_pair_lift_keeps_scalar
#print axioms D0.Research.AddressedThirdRole.second_pair_lift_keeps_scalar
#check D0.Research.AddressedThirdRole.first_pair_lift_keeps_identity
#print axioms D0.Research.AddressedThirdRole.first_pair_lift_keeps_identity
#check D0.Research.AddressedThirdRole.second_pair_lift_keeps_identity
#print axioms D0.Research.AddressedThirdRole.second_pair_lift_keeps_identity
#check D0.Research.AddressedThirdRole.first_pair_lift_keeps_conjugation
#print axioms D0.Research.AddressedThirdRole.first_pair_lift_keeps_conjugation
#check D0.Research.AddressedThirdRole.second_pair_lift_keeps_conjugation
#print axioms D0.Research.AddressedThirdRole.second_pair_lift_keeps_conjugation
#check D0.Research.AddressedThirdRole.concrete_native_four_coordinates_are_the_literal_two_role_tensor
#print axioms D0.Research.AddressedThirdRole.concrete_native_four_coordinates_are_the_literal_two_role_tensor
#check D0.Research.AddressedThirdRole.lift01_is_a_complete_identity_spectator
#print axioms D0.Research.AddressedThirdRole.lift01_is_a_complete_identity_spectator
#check D0.Research.AddressedThirdRole.lift02_is_a_complete_identity_spectator
#print axioms D0.Research.AddressedThirdRole.lift02_is_a_complete_identity_spectator
#check D0.Research.AddressedThirdRole.spectator_last_complete_multiplication
#print axioms D0.Research.AddressedThirdRole.spectator_last_complete_multiplication
#check D0.Research.AddressedThirdRole.spectator_middle_complete_multiplication
#print axioms D0.Research.AddressedThirdRole.spectator_middle_complete_multiplication
#check D0.Research.AddressedThirdRole.tensor_first_pair_with_full_spectator
#print axioms D0.Research.AddressedThirdRole.tensor_first_pair_with_full_spectator
#check D0.Research.AddressedThirdRole.tensor_second_pair_with_full_spectator
#print axioms D0.Research.AddressedThirdRole.tensor_second_pair_with_full_spectator
#check D0.Research.AddressedThirdRole.with_last_keeps_all_scalar_factors
#print axioms D0.Research.AddressedThirdRole.with_last_keeps_all_scalar_factors
#check D0.Research.AddressedThirdRole.with_middle_keeps_all_scalar_factors
#print axioms D0.Research.AddressedThirdRole.with_middle_keeps_all_scalar_factors
#check D0.Research.AddressedThirdRole.complete_first_pair_conjugation_retains_arbitrary_spectator
#print axioms D0.Research.AddressedThirdRole.complete_first_pair_conjugation_retains_arbitrary_spectator
#check D0.Research.AddressedThirdRole.complete_second_pair_conjugation_retains_arbitrary_spectator
#print axioms D0.Research.AddressedThirdRole.complete_second_pair_conjugation_retains_arbitrary_spectator
#check D0.Research.AddressedThirdRole.the_complete_four_role_products_are_literal_pauli_tensors
#print axioms D0.Research.AddressedThirdRole.the_complete_four_role_products_are_literal_pauli_tensors
#check D0.Research.AddressedThirdRole.first_coherent_recording_moves_the_turn_to_the_additional_role
#print axioms D0.Research.AddressedThirdRole.first_coherent_recording_moves_the_turn_to_the_additional_role
#check D0.Research.AddressedThirdRole.old_record_comparison_adds_the_retained_record_phase
#print axioms D0.Research.AddressedThirdRole.old_record_comparison_adds_the_retained_record_phase
#check D0.Research.AddressedThirdRole.original_recording_relocates_the_two_role_flip
#print axioms D0.Research.AddressedThirdRole.original_recording_relocates_the_two_role_flip
#check D0.Research.AddressedThirdRole.additional_recording_uncorrelates_its_complete_role
#print axioms D0.Research.AddressedThirdRole.additional_recording_uncorrelates_its_complete_role
#check D0.Research.AddressedThirdRole.final_old_record_comparison_uncorrelates_the_active_role
#print axioms D0.Research.AddressedThirdRole.final_old_record_comparison_uncorrelates_the_active_role
#check D0.Research.AddressedThirdRole.full_conjugation_composes_without_a_reset
#print axioms D0.Research.AddressedThirdRole.full_conjugation_composes_without_a_reset
#check D0.Research.AddressedThirdRole.full_conjugation_keeps_its_scalar_factor
#print axioms D0.Research.AddressedThirdRole.full_conjugation_keeps_its_scalar_factor
#check D0.Research.AddressedThirdRole.all_complete_proper_three_role_realizations_have_the_same_five_step_turn_transfer
#print axioms D0.Research.AddressedThirdRole.all_complete_proper_three_role_realizations_have_the_same_five_step_turn_transfer
#check D0.Research.AddressedThirdRole.five_step_orientation_is_only_a_sign
#print axioms D0.Research.AddressedThirdRole.five_step_orientation_is_only_a_sign
#check D0.Research.AddressedThirdRole.first_address_preserves_full_orthogonality
#print axioms D0.Research.AddressedThirdRole.first_address_preserves_full_orthogonality
#check D0.Research.AddressedThirdRole.additional_address_preserves_full_orthogonality
#print axioms D0.Research.AddressedThirdRole.additional_address_preserves_full_orthogonality
#check D0.Research.AddressedThirdRole.two_complete_orthogonal_operations_remain_orthogonal
#print axioms D0.Research.AddressedThirdRole.two_complete_orthogonal_operations_remain_orthogonal
#check D0.Research.AddressedThirdRole.every_five_step_route_is_complete_orthogonal
#print axioms D0.Research.AddressedThirdRole.every_five_step_route_is_complete_orthogonal
#check D0.Research.AddressedThirdRole.every_complete_conjugation_retains_its_identity_component
#print axioms D0.Research.AddressedThirdRole.every_complete_conjugation_retains_its_identity_component
#check D0.Research.AddressedThirdRole.complete_five_step_actuation_restores_both_other_roles_for_every_full_state
#print axioms D0.Research.AddressedThirdRole.complete_five_step_actuation_restores_both_other_roles_for_every_full_state
#check D0.Research.AddressedThirdRole.first_address_preserves_three_forward_inverse
#print axioms D0.Research.AddressedThirdRole.first_address_preserves_three_forward_inverse
#check D0.Research.AddressedThirdRole.additional_address_preserves_three_forward_inverse
#print axioms D0.Research.AddressedThirdRole.additional_address_preserves_three_forward_inverse
#check D0.Research.AddressedThirdRole.complete_three_role_actuation_has_twenty_one_forward_operations
#print axioms D0.Research.AddressedThirdRole.complete_three_role_actuation_has_twenty_one_forward_operations
#check D0.Research.AddressedThirdRole.complete_forward_code_has_no_inverse_or_reset_primitive
#print axioms D0.Research.AddressedThirdRole.complete_forward_code_has_no_inverse_or_reset_primitive
#check D0.Research.AddressedThirdRole.forward_code_transfers_the_angle_on_the_entire_eight_coordinate_workspace
#print axioms D0.Research.AddressedThirdRole.forward_code_transfers_the_angle_on_the_entire_eight_coordinate_workspace
#check D0.Research.AddressedThirdRole.unit_sign_adjacent_pair_from_parity
#print axioms D0.Research.AddressedThirdRole.unit_sign_adjacent_pair_from_parity
#check D0.Research.AddressedThirdRole.positive_forward_correlates_active_turn
#print axioms D0.Research.AddressedThirdRole.positive_forward_correlates_active_turn
#check D0.Research.AddressedThirdRole.positive_reverse_uncorrelates_both_flips
#print axioms D0.Research.AddressedThirdRole.positive_reverse_uncorrelates_both_flips
#check D0.Research.AddressedThirdRole.proper_reverse_turns_record_into_active_correlation
#print axioms D0.Research.AddressedThirdRole.proper_reverse_turns_record_into_active_correlation
#check D0.Research.AddressedThirdRole.proper_reverse_uncorrelates_both_turns
#print axioms D0.Research.AddressedThirdRole.proper_reverse_uncorrelates_both_turns
#check D0.Research.AddressedThirdRole.positive_forward_correlates_flip_phase_into_both_turns
#print axioms D0.Research.AddressedThirdRole.positive_forward_correlates_flip_phase_into_both_turns
#check D0.Research.AddressedThirdRole.positive_forward_uncorrelates_active_turn
#print axioms D0.Research.AddressedThirdRole.positive_forward_uncorrelates_active_turn
#check D0.Research.AddressedThirdRole.both_native_turns_are_the_complete_tensor
#print axioms D0.Research.AddressedThirdRole.both_native_turns_are_the_complete_tensor
#check D0.Research.AddressedThirdRole.positive_additional_recording_correlates_the_active_turn
#print axioms D0.Research.AddressedThirdRole.positive_additional_recording_correlates_the_active_turn
#check D0.Research.AddressedThirdRole.proper_original_recording_correlates_the_active_turn
#print axioms D0.Research.AddressedThirdRole.proper_original_recording_correlates_the_active_turn
#check D0.Research.AddressedThirdRole.positive_additional_comparison_uncorrelates_both_flips
#print axioms D0.Research.AddressedThirdRole.positive_additional_comparison_uncorrelates_both_flips
#check D0.Research.AddressedThirdRole.proper_old_record_comparison_moves_its_turn_back_to_active
#print axioms D0.Research.AddressedThirdRole.proper_old_record_comparison_moves_its_turn_back_to_active
#check D0.Research.AddressedThirdRole.positive_additional_recording_restores_its_complete_role
#print axioms D0.Research.AddressedThirdRole.positive_additional_recording_restores_its_complete_role
#check D0.Research.AddressedThirdRole.proper_original_recording_starts_the_mixed_route
#print axioms D0.Research.AddressedThirdRole.proper_original_recording_starts_the_mixed_route
#check D0.Research.AddressedThirdRole.proper_additional_comparison_retains_the_old_record_turn
#print axioms D0.Research.AddressedThirdRole.proper_additional_comparison_retains_the_old_record_turn
#check D0.Research.AddressedThirdRole.positive_additional_recording_correlates_both_turns
#print axioms D0.Research.AddressedThirdRole.positive_additional_recording_correlates_both_turns
#check D0.Research.AddressedThirdRole.proper_old_record_comparison_uncorrelates_both_turns
#print axioms D0.Research.AddressedThirdRole.proper_old_record_comparison_uncorrelates_both_turns
#check D0.Research.AddressedThirdRole.proper_additional_comparison_moves_its_turn_back_to_active
#print axioms D0.Research.AddressedThirdRole.proper_additional_comparison_moves_its_turn_back_to_active
#check D0.Research.AddressedThirdRole.all_complete_positive_helper_pairs_transfer_the_turn_in_six_steps
#print axioms D0.Research.AddressedThirdRole.all_complete_positive_helper_pairs_transfer_the_turn_in_six_steps
#check D0.Research.AddressedThirdRole.all_complete_mixed_helper_pairs_transfer_the_turn_in_seven_steps
#print axioms D0.Research.AddressedThirdRole.all_complete_mixed_helper_pairs_transfer_the_turn_in_seven_steps
#check D0.Research.AddressedThirdRole.complete_positive_helper_route_orientation_is_a_sign
#print axioms D0.Research.AddressedThirdRole.complete_positive_helper_route_orientation_is_a_sign
#check D0.Research.AddressedThirdRole.complete_mixed_helper_route_orientation_is_a_sign
#print axioms D0.Research.AddressedThirdRole.complete_mixed_helper_route_orientation_is_a_sign
#check D0.Research.AddressedThirdRole.every_addressed_primitive_preserves_the_complete_workspace
#print axioms D0.Research.AddressedThirdRole.every_addressed_primitive_preserves_the_complete_workspace
#check D0.Research.AddressedThirdRole.every_addressed_primitive_has_a_three_forward_inverse
#print axioms D0.Research.AddressedThirdRole.every_addressed_primitive_has_a_three_forward_inverse
#check D0.Research.AddressedThirdRole.complete_workspace_word_keeps_composition
#print axioms D0.Research.AddressedThirdRole.complete_workspace_word_keeps_composition
#check D0.Research.AddressedThirdRole.every_complete_addressed_word_remains_orthogonal
#print axioms D0.Research.AddressedThirdRole.every_complete_addressed_word_remains_orthogonal
#check D0.Research.AddressedThirdRole.every_full_word_inverse_uses_only_the_same_forward_primitives
#print axioms D0.Research.AddressedThirdRole.every_full_word_inverse_uses_only_the_same_forward_primitives
#check D0.Research.AddressedThirdRole.inverse_forward_code_retains_its_exact_length
#print axioms D0.Research.AddressedThirdRole.inverse_forward_code_retains_its_exact_length
#check D0.Research.AddressedThirdRole.full_actuation_compiler_has_four_times_route_length_plus_one
#print axioms D0.Research.AddressedThirdRole.full_actuation_compiler_has_four_times_route_length_plus_one
#check D0.Research.AddressedThirdRole.full_actuation_compiler_keeps_the_complete_conjugation
#print axioms D0.Research.AddressedThirdRole.full_actuation_compiler_keeps_the_complete_conjugation
#check D0.Research.AddressedThirdRole.inverse_forward_code_keeps_the_complete_primitive_palette
#print axioms D0.Research.AddressedThirdRole.inverse_forward_code_keeps_the_complete_primitive_palette
#check D0.Research.AddressedThirdRole.full_actuation_compiler_introduces_only_the_owned_active_turn
#print axioms D0.Research.AddressedThirdRole.full_actuation_compiler_introduces_only_the_owned_active_turn
#check D0.Research.AddressedThirdRole.native_two_role_turns_keep_their_owned_identity_and_generator
#print axioms D0.Research.AddressedThirdRole.native_two_role_turns_keep_their_owned_identity_and_generator
#check D0.Research.AddressedThirdRole.first_address_keeps_the_complete_sum
#print axioms D0.Research.AddressedThirdRole.first_address_keeps_the_complete_sum
#check D0.Research.AddressedThirdRole.addressed_native_turns_are_the_actual_owned_full_operators
#print axioms D0.Research.AddressedThirdRole.addressed_native_turns_are_the_actual_owned_full_operators
#check D0.Research.AddressedThirdRole.addressed_three_step_positive_forward_route_transfers_the_complete_turn
#print axioms D0.Research.AddressedThirdRole.addressed_three_step_positive_forward_route_transfers_the_complete_turn
#check D0.Research.AddressedThirdRole.addressed_three_step_positive_reverse_route_transfers_the_complete_turn
#print axioms D0.Research.AddressedThirdRole.addressed_three_step_positive_reverse_route_transfers_the_complete_turn
#check D0.Research.AddressedThirdRole.every_complete_two_address_phase_family_has_a_full_turn_transfer_route
#print axioms D0.Research.AddressedThirdRole.every_complete_two_address_phase_family_has_a_full_turn_transfer_route
#check D0.Research.AddressedThirdRole.complete_signed_addressed_actuation_is_constructive_with_at_most_twenty_nine_steps
#print axioms D0.Research.AddressedThirdRole.complete_signed_addressed_actuation_is_constructive_with_at_most_twenty_nine_steps
#check D0.Research.AddressedThirdRole.actual_owned_golden_angle_requires_no_added_rotation_primitive
#print axioms D0.Research.AddressedThirdRole.actual_owned_golden_angle_requires_no_added_rotation_primitive
#check D0.Research.AddressedThirdRole.constant_twenty_nine_step_actuation_keeps_the_owned_golden_resource_window
#print axioms D0.Research.AddressedThirdRole.constant_twenty_nine_step_actuation_keeps_the_owned_golden_resource_window
#check D0.Research.AddressedThirdRole.complete_programme_refinement_keeps_every_forward_primitive
#print axioms D0.Research.AddressedThirdRole.complete_programme_refinement_keeps_every_forward_primitive
#check D0.Research.AddressedThirdRole.every_addressed_programme_intertwines_every_full_golden_depth
#print axioms D0.Research.AddressedThirdRole.every_addressed_programme_intertwines_every_full_golden_depth
#check D0.Research.AddressedThirdRole.complete_three_role_programme_error_has_no_refinement_dilution
#print axioms D0.Research.AddressedThirdRole.complete_three_role_programme_error_has_no_refinement_dilution
#check D0.Research.AddressedThirdRole.full_constructive_actuation_commutes_with_every_retained_golden_depth
#print axioms D0.Research.AddressedThirdRole.full_constructive_actuation_commutes_with_every_retained_golden_depth
#check D0.Research.AddressedThirdRole.the_complete_two_address_retaining_real_family_has_sixty_five_thousand_five_hundred_thirty_six_realizations
#print axioms D0.Research.AddressedThirdRole.the_complete_two_address_retaining_real_family_has_sixty_five_thousand_five_hundred_thirty_six_realizations
#check D0.Research.AddressedThirdRole.all_functionally_classified_addressed_real_primitives_have_a_complete_workspace_programme
#print axioms D0.Research.AddressedThirdRole.all_functionally_classified_addressed_real_primitives_have_a_complete_workspace_programme
#check D0.Research.AddressedThirdRole.already_owned_common_recording_and_comparison_need_only_thirteen_or_twenty_one_steps
#print axioms D0.Research.AddressedThirdRole.already_owned_common_recording_and_comparison_need_only_thirteen_or_twenty_one_steps
