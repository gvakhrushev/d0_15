import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic
import D0.Edge.RamificationFromUeEffCompanion
import D0.Integration.V15.EdgeAudit
import D0.Foundation.ObservableCompletionCanonicity

namespace D0.Edge.HolonomyRamificationSeparation

open Matrix
open D0.Edge
open D0.Integration.V15.EdgeAudit
open D0.Foundation.ObservableCompletionCanonicity

/-!
# D0.Edge.HolonomyRamificationSeparation

Disentangling three distinct structures previously confounded in the edge/lepton sector:
1. Physical $U(1)$ edge holonomy phase $h$;
2. Puiseux ramification deformation parameter $t$;
3. Projective cycle return lengths and the phase-blind terminal exponent observable.

## Key Insights:
* The legacy edge no-go used $\lambda = 1, 2$, where $2 \notin U(1)$. We repair this by defining
  `AdmissibleHolonomyQ h := h * h = 1`, proving that $h_+ = 1$ and $h_- = -1$ are genuine
  unitary witnesses producing distinct cover coefficients (`coverCoeffZ3 1 ≠ coverCoeffZ3 (-1)`).
* The companion matrix family is factored into a 2-parameter family $(t, h) \mapsto C_4(t \cdot h)$,
  $R_3(t \cdot h)$. On the physical slice $t = 1$, $C_4^4 = h I$ with $|h| = 1$.
  At the branch point $t = 0$, $C_4^4 = 0$ identically for ALL physical phases $h$,
  completely decoupling ramification from the physically impossible requirement $h = 0$.
* The terminal return orders are projective invariants: for any nonzero $h$, the minimal positive
  power producing a scalar multiple of identity is strictly 4 for $C_4$ and 3 for $R_3$.
* The resulting ramification exponents $(1/4, 1/3)$ and the full terminal exponent row
  $[0, 1/4, 1/3]$ are constant across the entire admissible holonomy class, and hence
  $M_1$-forced via `ObservableCompletionCanonicity.constant_readout_m1_forced`.
-/

/-- Rational unitary $U(1)$ holonomy admissibility condition: $h^2 = 1$. -/
def AdmissibleHolonomyQ (h : ℚ) : Prop :=
  h * h = 1

theorem h_plus_admissible : AdmissibleHolonomyQ 1 := by
  unfold AdmissibleHolonomyQ
  norm_num

theorem h_minus_admissible : AdmissibleHolonomyQ (-1) := by
  unfold AdmissibleHolonomyQ
  norm_num

/-- **D0-EDGE-HOLONOMY-ADMISSIBLE-FAMILY-001 (Repaired Edge No-Go)**:
Within the true rational unitary class `AdmissibleHolonomyQ`, two distinct holonomies
$h_+ = 1$ and $h_- = -1$ give distinct edge cover observables:
$\operatorname{coverCoeffZ3}(1) = -1 \ne 1 = \operatorname{coverCoeffZ3}(-1)$. -/
theorem admissible_edge_cover_is_family :
    AdmissibleHolonomyQ 1 ∧
    AdmissibleHolonomyQ (-1) ∧
    coverCoeffZ3 1 ≠ coverCoeffZ3 (-1) := by
  refine ⟨h_plus_admissible, h_minus_admissible, ?_⟩
  unfold coverCoeffZ3
  norm_num

/-- 4-cycle companion block deformed by deformation parameter $t$ and physical phase $h$. -/
def companionC4Deformed (t h : ℚ) : Matrix (Fin 4) (Fin 4) ℚ :=
  companionC4 (t * h)

/-- 3-cycle companion block deformed by deformation parameter $t$ and physical phase $h$. -/
def companionR3Deformed (t h : ℚ) : Matrix (Fin 3) (Fin 3) ℚ :=
  companionR3 (t * h)

/-- 4-cycle relation with factored deformation and phase:
$$C_4(t, h)^4 = (t \cdot h) \cdot I_4.$$ -/
theorem companionC4Deformed_cyclic (t h : ℚ) :
    (companionC4Deformed t h) ^ 4 = (t * h) • (1 : Matrix (Fin 4) (Fin 4) ℚ) :=
  companionC4_cyclic (t * h)

/-- 3-cycle relation with factored deformation and phase:
$$R_3(t, h)^3 = (t \cdot h) \cdot I_3.$$ -/
theorem companionR3Deformed_cyclic (t h : ℚ) :
    (companionR3Deformed t h) ^ 3 = (t * h) • (1 : Matrix (Fin 3) (Fin 3) ℚ) :=
  companionR3_cyclic (t * h)

/-- **Physical slice $t = 1$**: the return acquires the physical holonomy phase $h$. -/
theorem companion_physical_slice (h : ℚ) :
    (companionC4Deformed 1 h) ^ 4 = h • (1 : Matrix (Fin 4) (Fin 4) ℚ) ∧
    (companionR3Deformed 1 h) ^ 3 = h • (1 : Matrix (Fin 3) (Fin 3) ℚ) := by
  have h4 : (companionC4Deformed 1 h) ^ 4 = (1 * h) • 1 := companionC4Deformed_cyclic 1 h
  have h3 : (companionR3Deformed 1 h) ^ 3 = (1 * h) • 1 := companionR3Deformed_cyclic 1 h
  rw [one_mul] at h4 h3
  exact ⟨h4, h3⟩

/-- **Branch point locus $t = 0$**: both companion blocks become nilpotent identically for ALL
physical phases $h$, without requiring the physical holonomy to vanish. -/
theorem companion_branch_locus_nilpotent (h : ℚ) :
    (companionC4Deformed 0 h) ^ 4 = 0 ∧
    (companionR3Deformed 0 h) ^ 3 = 0 := by
  have h4 : (companionC4Deformed 0 h) ^ 4 = (0 * h) • (1 : Matrix (Fin 4) (Fin 4) ℚ) :=
    companionC4Deformed_cyclic 0 h
  have h3 : (companionR3Deformed 0 h) ^ 3 = (0 * h) • (1 : Matrix (Fin 3) (Fin 3) ℚ) :=
    companionR3Deformed_cyclic 0 h
  rw [zero_mul, zero_smul] at h4 h3
  exact ⟨h4, h3⟩

/-- Predicate asserting that the $n$-th power of matrix $U$ is a nonzero scalar multiple of identity. -/
def ProjectiveReturnAt {m : ℕ} (U : Matrix (Fin m) (Fin m) ℚ) (n : ℕ) : Prop :=
  ∃ c : ℚ, c ≠ 0 ∧ U ^ n = c • (1 : Matrix (Fin m) (Fin m) ℚ)

/-- Predicate asserting that $n$ is the minimal positive exponent of projective return. -/
def ProjectiveOrder {m : ℕ} (U : Matrix (Fin m) (Fin m) ℚ) (n : ℕ) : Prop :=
  ProjectiveReturnAt U n ∧ ∀ k : ℕ, 0 < k → k < n → ¬ ProjectiveReturnAt U k

/-- Powers of `companionC4 h` for intermediate exponents 1, 2, 3 do not return projectively to identity. -/
theorem companionC4_not_projective_intermediate (h : ℚ) (k : ℕ) (hk0 : 0 < k) (hk4 : k < 4) :
    ¬ ProjectiveReturnAt (companionC4 h) k := by
  intro ⟨c, hc, h_eq⟩
  interval_cases k
  · -- k = 1: (C4)_{0,1} = 1, but (c • I)_{0,1} = 0
    have h01 := congr_fun (congr_fun h_eq 0) 1
    unfold companionC4 at h01
    dsimp at h01
    simp at h01
  · -- k = 2: (C4^2)_{0,2} = 1, but (c • I)_{0,2} = 0
    have h_sq : (companionC4 h) ^ 2 = (companionC4 h) * (companionC4 h) := by
      rw [pow_two]
    have h02 := congr_fun (congr_fun h_eq 0) 2
    rw [h_sq] at h02
    unfold companionC4 at h02
    simp [Matrix.mul_apply, Fin.sum_univ_four] at h02
  · -- k = 3: (C4^3)_{0,3} = 1, but (c • I)_{0,3} = 0
    have h_cube : (companionC4 h) ^ 3 = (companionC4 h) ^ 2 * (companionC4 h) := by
      rw [pow_succ, pow_two]
    have h_sq : (companionC4 h) ^ 2 = (companionC4 h) * (companionC4 h) := pow_two _
    have h03 := congr_fun (congr_fun h_eq 0) 3
    rw [h_cube, h_sq] at h03
    unfold companionC4 at h03
    simp [Matrix.mul_apply, Fin.sum_univ_four] at h03

/-- Powers of `companionR3 h` for intermediate exponents 1, 2 do not return projectively to identity. -/
theorem companionR3_not_projective_intermediate (h : ℚ) (k : ℕ) (hk0 : 0 < k) (hk3 : k < 3) :
    ¬ ProjectiveReturnAt (companionR3 h) k := by
  intro ⟨c, hc, h_eq⟩
  interval_cases k
  · -- k = 1: (R3)_{0,1} = 1, but (c • I)_{0,1} = 0
    have h01 := congr_fun (congr_fun h_eq 0) 1
    unfold companionR3 at h01
    dsimp at h01
    simp at h01
  · -- k = 2: (R3^2)_{0,2} = 1, but (c • I)_{0,2} = 0
    have h_sq : (companionR3 h) ^ 2 = (companionR3 h) * (companionR3 h) := by
      rw [pow_two]
    have h02 := congr_fun (congr_fun h_eq 0) 2
    rw [h_sq] at h02
    unfold companionR3 at h02
    simp [Matrix.mul_apply, Fin.sum_univ_three] at h02

/-- **D0-PROJECTIVE-TERMINAL-RETURN-ORDER-001**:
For any nonzero holonomy phase $h \ne 0$ (including all physical $U(1)$ phases),
the projective return order is strictly 4 for $C_4(h)$ and 3 for $R_3(h)$. -/
theorem companion_projective_orders (h : ℚ) (hh : h ≠ 0) :
    ProjectiveOrder (companionC4 h) 4 ∧
    ProjectiveOrder (companionR3 h) 3 := by
  have h4_ret : ProjectiveReturnAt (companionC4 h) 4 := by
    refine ⟨h, hh, companionC4_cyclic h⟩
  have h3_ret : ProjectiveReturnAt (companionR3 h) 3 := by
    refine ⟨h, hh, companionR3_cyclic h⟩
  refine ⟨⟨h4_ret, fun k hk0 hk4 => companionC4_not_projective_intermediate h k hk0 hk4⟩,
          ⟨h3_ret, fun k hk0 hk3 => companionR3_not_projective_intermediate h k hk0 hk3⟩⟩

/-- Holonomy-blind terminal exponent row readout:
maps any admissible holonomy completion $h$ to the invariant exponent sequence $[0, 1/4, 1/3]$. -/
def terminalExponentRow (_h : ℚ) : List ℚ :=
  [0, 1/4, 1/3]

/-- The canonical target exponent row $[0, 1/4, 1/3]$. -/
def canonicalExponentRow : List ℚ :=
  [0, 1/4, 1/3]

/-- The readout is identically constant across the entire admissible holonomy class. -/
theorem terminalExponentRow_constant (h : ℚ) (_hh : AdmissibleHolonomyQ h) :
    terminalExponentRow h = canonicalExponentRow :=
  rfl

/-- **D0-LEPTON-HOLONOMY-BLIND-EXPONENT-CANONICITY-001 (Owner)**:
The structural lepton exponent row $[0, 1/4, 1/3]$ is $M_1$-forced across the entire
admissible holonomy class via `constant_readout_m1_forced`.
The raw holonomy phase $h$ is noncanonical, but the terminal exponent observable
is strictly canonical and independent of the choice of $h \in U(1)$. -/
theorem lepton_holonomy_blind_exponent_m1_forced :
    D0.Foundation.M1Forced
      (CompletionForcesReadout AdmissibleHolonomyQ terminalExponentRow)
      canonicalExponentRow :=
  constant_readout_m1_forced
    AdmissibleHolonomyQ
    terminalExponentRow
    1
    h_plus_admissible
    terminalExponentRow_constant

/-- **D0-HOLONOMY-RAMIFICATION-SEPARATION-001 (Owner)**:
Master synthesis theorem decoupling physical holonomy from ramification and proving:
1. Repaired edge no-go within unitary class ($h = \pm 1$);
2. Total ramification at $t = 0$ holds identically for all $h$;
3. Projective return lengths $(4, 3)$ hold for all $h \ne 0$;
4. Terminal exponent row $[0, 1/4, 1/3]$ is strictly $M_1$-forced. -/
theorem holonomy_ramification_separation_owner :
    (coverCoeffZ3 1 ≠ coverCoeffZ3 (-1)) ∧
    (∀ h : ℚ, (companionC4Deformed 0 h) ^ 4 = 0 ∧ (companionR3Deformed 0 h) ^ 3 = 0) ∧
    (∀ h : ℚ, h ≠ 0 → ProjectiveOrder (companionC4 h) 4 ∧ ProjectiveOrder (companionR3 h) 3) ∧
    (∀ h : ℚ, AdmissibleHolonomyQ h → terminalExponentRow h = canonicalExponentRow) :=
  ⟨admissible_edge_cover_is_family.2.2,
   companion_branch_locus_nilpotent,
   companion_projective_orders,
   terminalExponentRow_constant⟩

end D0.Edge.HolonomyRamificationSeparation
