import Mathlib.Analysis.SpecificLimits.Fibonacci
import D0.NumberTheory.HurwitzPhi

namespace D0

noncomputable def alphaD0 : Real :=
  D0PhaseGenerator

theorem alphaD0_eq_phi_inv_sq :
    alphaD0 = phi^(-2 : Int) := by
  exact D0PhaseGenerator_eq_phi_inv_sq

theorem p_eq_phi_sub_one :
    p = phi - 1 := by
  rw [show p = primitiveRoot by exact phi_inv_eq_primitiveRoot]
  unfold primitiveRoot phi
  ring

theorem alphaD0_eq_two_sub_phi :
    alphaD0 = 2 - phi := by
  unfold alphaD0 D0PhaseGenerator
  have hclosure := p_unit_closure
  rw [show p^2 = 1 - p by nlinarith [hclosure]]
  rw [p_eq_phi_sub_one]
  ring

def D0PhaseGeneratorAdmissible (alpha : Real) : Prop :=
  exists x : Real, D0ResponseRoot x /\ alpha = x^2

theorem unique_D0_phase_generator :
    ExistsUnique D0PhaseGeneratorAdmissible := by
  refine ⟨alphaD0, ?_, ?_⟩
  · exact ⟨p, ⟨p_positive, p_unit_closure⟩, rfl⟩
  · intro beta hbeta
    rcases hbeta with ⟨x, hx, rfl⟩
    simpa [alphaD0] using D0_response_forces_phase_generator x hx

theorem unique_D0_phase_generator_is_phi_inv_sq :
    D0PhaseGeneratorAdmissible alphaD0 := by
  exact ⟨p, ⟨p_positive, p_unit_closure⟩, rfl⟩

def alphaD0CFPartialQuotient (n : Nat) : Nat :=
  if n = 0 then 0 else if n = 1 then 2 else 1

theorem alphaD0_cf_head :
    alphaD0CFPartialQuotient 0 = 0 := by
  rfl

theorem alphaD0_cf_second :
    alphaD0CFPartialQuotient 1 = 2 := by
  rfl

theorem alphaD0_cf_tail_ones (n : Nat) (hn : 2 <= n) :
    alphaD0CFPartialQuotient n = 1 := by
  unfold alphaD0CFPartialQuotient
  have hn0 : n ≠ 0 := by omega
  have hn1 : n ≠ 1 := by omega
  simp [hn0, hn1]

def alphaD0ConvergentNumerator : Nat -> Nat
  | 0 => 0
  | 1 => 1
  | n + 2 => alphaD0ConvergentNumerator n + alphaD0ConvergentNumerator (n + 1)

def alphaD0ConvergentDenominator : Nat -> Nat
  | 0 => 1
  | 1 => 2
  | n + 2 => alphaD0ConvergentDenominator n + alphaD0ConvergentDenominator (n + 1)

theorem alphaD0_convergents_numerators_fibonacci (n : Nat) :
    alphaD0ConvergentNumerator n = Nat.fib n := by
  induction n using Nat.twoStepInduction with
  | zero => norm_num [alphaD0ConvergentNumerator]
  | one => norm_num [alphaD0ConvergentNumerator]
  | more n h0 h1 =>
      simp [alphaD0ConvergentNumerator, h0, h1, Nat.fib_add_two]

theorem alphaD0_convergents_denominators_fibonacci (n : Nat) :
    alphaD0ConvergentDenominator n = Nat.fib (n + 2) := by
  induction n using Nat.twoStepInduction with
  | zero => norm_num [alphaD0ConvergentDenominator]
  | one => norm_num [alphaD0ConvergentDenominator]
  | more n h0 h1 =>
      simp [alphaD0ConvergentDenominator, h0, h1, Nat.fib_add_two,
        Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]

noncomputable def periodOneTail (a : Nat) : Real :=
  (Real.sqrt ((a : Real)^2 + 4) - a) / 2

noncomputable def periodOnePhase (a : Nat) : Real :=
  (periodOneTail a)^2

noncomputable def periodOneBadApproxConstant (a : Nat) : Real :=
  1 / Real.sqrt ((a : Real)^2 + 4)

theorem periodOneTail_positive (a : Nat) :
    0 < periodOneTail a := by
  unfold periodOneTail
  have hsq : (a : Real)^2 < (a : Real)^2 + 4 := by norm_num
  have hlt : (a : Real) < Real.sqrt ((a : Real)^2 + 4) := by
    have ha : 0 <= (a : Real) := by exact_mod_cast Nat.zero_le a
    exact (Real.lt_sqrt ha).mpr hsq
  linarith

theorem periodOneTail_fixed_point (a : Nat) :
    periodOneTail a ^ 2 + (a : Real) * periodOneTail a = 1 := by
  unfold periodOneTail
  have hs : (Real.sqrt (4 + (a : Real)^2))^2 = 4 + (a : Real)^2 := by
    exact Real.sq_sqrt (by positivity)
  ring_nf
  rw [hs]
  ring

theorem periodOneTail_one_eq_p :
    periodOneTail 1 = p := by
  rw [show p = primitiveRoot by exact phi_inv_eq_primitiveRoot]
  unfold periodOneTail primitiveRoot
  norm_num

theorem periodOnePhase_one_eq_alphaD0 :
    periodOnePhase 1 = alphaD0 := by
  unfold periodOnePhase alphaD0 D0PhaseGenerator
  rw [periodOneTail_one_eq_p]

theorem periodOneBadApproxConstant_one :
    periodOneBadApproxConstant 1 = 1 / Real.sqrt 5 := by
  unfold periodOneBadApproxConstant
  norm_num

theorem periodOneBadApproxConstant_max_at_one
    (a : Nat) (ha : 1 <= a) :
    periodOneBadApproxConstant a <= periodOneBadApproxConstant 1 := by
  unfold periodOneBadApproxConstant
  norm_num
  have hrad : (5 : Real) <= (a : Real)^2 + 4 := by
    have haR : (1 : Real) <= a := by exact_mod_cast ha
    nlinarith [sq_nonneg ((a : Real) - 1)]
  have hsqrt : Real.sqrt 5 <= Real.sqrt ((a : Real)^2 + 4) :=
    Real.sqrt_le_sqrt hrad
  have hpos : 0 < Real.sqrt 5 := Real.sqrt_pos.2 (by norm_num)
  simpa [one_div] using one_div_le_one_div_of_le hpos hsqrt

theorem alphaD0_is_extremal_among_period_one_contfrac :
    forall a : Nat, 1 <= a ->
      periodOneBadApproxConstant a <= periodOneBadApproxConstant 1 := by
  intro a ha
  exact periodOneBadApproxConstant_max_at_one a ha

def HurwitzMinimaxD0ClassProved : Prop :=
  D0PhaseGeneratorAdmissible alphaD0 /\
    periodOnePhase 1 = alphaD0 /\
    (forall a : Nat, 1 <= a ->
      periodOneBadApproxConstant a <= periodOneBadApproxConstant 1)

theorem HURWITZ_MINIMAX_D0_CLASS_PROVED :
    HurwitzMinimaxD0ClassProved := by
  exact
    ⟨unique_D0_phase_generator_is_phi_inv_sq,
      periodOnePhase_one_eq_alphaD0,
      alphaD0_is_extremal_among_period_one_contfrac⟩

end D0
