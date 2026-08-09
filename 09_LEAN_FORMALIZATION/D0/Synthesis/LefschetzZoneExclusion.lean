import D0.Dynamics.TraceHeatLucasCore
import Mathlib.Tactic

/-!
# The Lefschetz zone exclusion: 13 misses both owned toral address families

The corpus owns TWO direct toral address families on the same `T`: the anti-periodic Lefschetz
family `NFermion n = |det(Tⁿ + 1)|` with its scene unfolding
(`D0-TRACE-HEAT-CAPACITY-GRAVITY-001`, `lefschetz_spectrum_unfolds_scene`: `F(3) = 4, F(4) = 9,
F(5) = 11, F(6) = 20`, composite `13 = F(3) + F(4)`), and the periodic fixed-point family
`G(n) = |det(Tⁿ − 1)|` (`D0-TORAL-LUCAS-PERIODIC-SEED-OWNER-001`, `#Fix₅ = 11`). This module
proves the zone size **13 lies outside BOTH families** — so the owner's composite reading is
forced at value level, and 13 is the unique zone size with no direct address in either family
(9 = F(4); 11 = F(5) = G(5)).

* `nfermion_closed_form` — for ALL `n`: `det(Tⁿ + 1) = 1 + (−1)ⁿ·Lₙ + (−1)ⁿ`, i.e.
  `F(n) = Lₙ + 2` at even `n` and `F(n) = Lₙ` at odd `n`. The owner's per-value `native_decide`
  facts become one structural identity (generic 2×2 `det(A+1) = det A + tr A + 1` + the trace
  and determinant laws, re-derived here with a clean axiom profile — no `native_decide`).
* `thirteen_no_direct_address` — **`F(n) ≠ 13` for every `n`** (anti-periodic family). Parity
  split: odd `n` needs `Lₙ = 13`, but 13 is not a Lucas number (`thirteen_not_lucas`; the gap is
  `L₅ = 11 < 13 < 18 = L₆`); even `n` needs `Lₙ = 11 = L₅` — but 11 sits at an ODD Lucas index
  (`eleven_not_even_lucas`).
* `thirteen_no_periodic_address` — **`G(n) ≠ 13` for every `n`** (periodic family): odd `n`
  needs `Lₙ = 13` again; even `n` needs `Lₙ = 15`, also not Lucas (`fifteen_not_lucas`). With
  `periodic_five` (`G(5) = 11`) this makes 13 the unique zone size outside both owned families —
  scoped to these two; no claim about address families the corpus does not own.
* `composite_address_value_unique` — if `F(m) + F(n) = 13` then the value pair is `{4, 9}`:
  the owned composite reading is forced AT VALUE LEVEL. The index pair is NOT unique —
  `(0, 4)` also lands on 13 (`F(0) = det(2·I) = 4`); necessity is claimed for the values only.
* `lucas_recurrence_shares_degree_arithmetic` — `F(6) = F(4) + F(5)` (the Lucas recurrence
  inside the family) and `33 − 13 = 9 + 11` (the scene degree identity `d₁₃ = n₉ + n₁₁`) share
  the arithmetic `20 = 9 + 11`. A shared equation between two owned facts — **no binding is
  minted**; whether the toral recurrence *is* the degree identity is not claimed (the name says
  "shares", deliberately).

**Scope honesty.** The positive values and the composite reading stay at the owner's grade;
this module adds the necessity layer (exclusion + uniqueness) and the all-`n` closed form. The
`+2` appearing at even `n` is the orientation term `1 + det(Tⁿ)`; any identification with other
owned `+2`s (cascade floor, address `+2`) is a shared numeral across different carriers and is
NOT made here.
-/

namespace D0.Synthesis.LefschetzZoneExclusion

open D0.Dynamics

/-! ## Clean re-derivation of the trace law (no `native_decide`) -/

/-- Generic 2×2: `det(A + 1) = det A + tr A + 1`. -/
theorem det_add_one_fin_two (A : Matrix (Fin 2) (Fin 2) ℤ) :
    Matrix.det (A + 1) = Matrix.det A + Matrix.trace A + 1 := by
  rw [Matrix.det_fin_two, Matrix.det_fin_two, Matrix.trace_fin_two]
  simp only [Matrix.add_apply, Matrix.one_apply]
  norm_num
  ring

theorem detT_clean : Matrix.det T = -1 := by decide

theorem Tsq_clean : T ^ 2 = 1 - T := by decide

theorem trace_rec_clean (n : ℕ) :
    Matrix.trace (T ^ (n + 2)) = Matrix.trace (T ^ n) - Matrix.trace (T ^ (n + 1)) := by
  have h : T ^ (n + 2) = T ^ n - T ^ (n + 1) := by
    calc T ^ (n + 2) = T ^ n * T ^ 2 := by rw [pow_add]
    _ = T ^ n * (1 - T) := by rw [Tsq_clean]
    _ = T ^ n - T ^ (n + 1) := by rw [mul_sub, mul_one, pow_succ]
  rw [h, Matrix.trace_sub]

theorem trace_T_pow_clean : ∀ n, Matrix.trace (T ^ n) = signedLucasTrace n :=
  Nat.twoStepInduction (by decide) (by decide) (fun n ih1 ih2 => by
    rw [trace_rec_clean n, ih1, ih2]
    have hp2 : ((-1 : ℤ)) ^ (n + 2) = (-1) ^ n := by rw [pow_add]; ring
    have hp1 : ((-1 : ℤ)) ^ (n + 1) = -((-1) ^ n) := by rw [pow_add]; ring
    simp only [signedLucasTrace, hp2, hp1]
    rw [show lucas (n + 2) = lucas (n + 1) + lucas n from rfl]
    ring)

/-- **The closed form, all `n`**: `det(Tⁿ + 1) = 1 + (−1)ⁿLₙ + (−1)ⁿ`. -/
theorem nfermion_closed_form (n : ℕ) :
    NFermionInt n = 1 + signedLucasTrace n + (-1) ^ n := by
  unfold NFermionInt
  rw [det_add_one_fin_two, Matrix.det_pow, detT_clean, trace_T_pow_clean]
  ring

/-! ## Lucas growth -/

theorem lucas_nonneg : ∀ n, 0 ≤ lucas n :=
  Nat.twoStepInduction (by decide) (by decide) (fun n ih1 ih2 => by
    rw [show lucas (n + 2) = lucas (n + 1) + lucas n from rfl]
    omega)

theorem lucas_step (n : ℕ) : lucas (n + 1) ≤ lucas (n + 2) := by
  rw [show lucas (n + 2) = lucas (n + 1) + lucas n from rfl]
  have := lucas_nonneg n
  omega

theorem lucas_lower_six : ∀ n, 6 ≤ n → 18 ≤ lucas n := by
  intro n hn
  induction n, hn using Nat.le_induction with
  | base => decide
  | succ n hn ih =>
      obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
      exact le_trans ih (lucas_step m)

theorem lucas_lower_seven : ∀ n, 7 ≤ n → 29 ≤ lucas n := by
  intro n hn
  induction n, hn using Nat.le_induction with
  | base => decide
  | succ n hn ih =>
      obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
      exact le_trans ih (lucas_step m)

/-- 13 is not a Lucas number: `L₅ = 11 < 13 < 18 = L₆`. -/
theorem thirteen_not_lucas (n : ℕ) : lucas n ≠ 13 := by
  by_cases h : n ≤ 5
  · interval_cases n <;> decide
  · have := lucas_lower_six n (by omega)
    omega

/-- 11 is a Lucas number only at the odd index 5: no even index carries it. -/
theorem eleven_not_even_lucas (n : ℕ) (he : n % 2 = 0) : lucas n ≠ 11 := by
  by_cases h : n ≤ 5
  · interval_cases n <;> first | (exact absurd he (by decide)) | decide
  · have := lucas_lower_six n (by omega)
    omega

/-! ## The exclusion -/

/-- **13 has no direct anti-periodic address**: `NFermion n ≠ 13` for every `n`. Together with
`thirteen_no_periodic_address`, the owned composite reading is forced at value level (the value
pair `{4, 9}` — the INDEX pair `(3, 4)` is not unique, see `composite_address_value_unique`). -/
theorem thirteen_no_direct_address (n : ℕ) : NFermion n ≠ 13 := by
  unfold NFermion
  intro h
  have habs := Int.natAbs_eq_iff.mp h
  rw [nfermion_closed_form] at habs
  rcases Nat.even_or_odd n with he | ho
  · have hs : signedLucasTrace n = lucas n := by
      unfold signedLucasTrace
      rw [he.neg_one_pow, one_mul]
    rw [he.neg_one_pow, hs] at habs
    have hnn := lucas_nonneg n
    have h11 := eleven_not_even_lucas n (Nat.even_iff.mp he)
    omega
  · have hs : signedLucasTrace n = -lucas n := by
      unfold signedLucasTrace
      rw [ho.neg_one_pow, neg_one_mul]
    rw [ho.neg_one_pow, hs] at habs
    have h13 := thirteen_not_lucas n
    have hnn := lucas_nonneg n
    omega

/-! ## The periodic family -/

/-- Generic 2×2: `det(A − 1) = det A − tr A + 1`. -/
theorem det_sub_one_fin_two (A : Matrix (Fin 2) (Fin 2) ℤ) :
    Matrix.det (A - 1) = Matrix.det A - Matrix.trace A + 1 := by
  rw [Matrix.det_fin_two, Matrix.det_fin_two, Matrix.trace_fin_two]
  simp only [Matrix.sub_apply, Matrix.one_apply]
  norm_num
  ring

/-- The periodic (fixed-point) counterpart: `det(Tⁿ − 1) = (−1)ⁿ − (−1)ⁿLₙ + 1`. -/
theorem periodic_closed_form (n : ℕ) :
    Matrix.det (T ^ n - 1) = (-1) ^ n - signedLucasTrace n + 1 := by
  rw [det_sub_one_fin_two, Matrix.det_pow, detT_clean, trace_T_pow_clean]

theorem fifteen_not_lucas (n : ℕ) : lucas n ≠ 15 := by
  by_cases h : n ≤ 5
  · interval_cases n <;> decide
  · have := lucas_lower_six n (by omega)
    omega

/-- **13 has no direct periodic address either**: `|det(Tⁿ − 1)| ≠ 13` for every `n` — odd `n`
would need `Lₙ = 13`, even `n` would need `Lₙ = 15`, and neither is a Lucas number. -/
theorem thirteen_no_periodic_address (n : ℕ) : (Matrix.det (T ^ n - 1)).natAbs ≠ 13 := by
  intro h
  have habs := Int.natAbs_eq_iff.mp h
  rw [periodic_closed_form] at habs
  rcases Nat.even_or_odd n with he | ho
  · have hs : signedLucasTrace n = lucas n := by
      unfold signedLucasTrace
      rw [he.neg_one_pow, one_mul]
    rw [he.neg_one_pow, hs] at habs
    have hnn := lucas_nonneg n
    have h15 := fifteen_not_lucas n
    omega
  · have hs : signedLucasTrace n = -lucas n := by
      unfold signedLucasTrace
      rw [ho.neg_one_pow, neg_one_mul]
    rw [ho.neg_one_pow, hs] at habs
    have h13 := thirteen_not_lucas n
    have hnn := lucas_nonneg n
    omega

/-- The periodic family owns 11 at the fifth return: `|det(T⁵ − 1)| = 11 = #Fix₅`. -/
theorem periodic_five : (Matrix.det (T ^ 5 - 1)).natAbs = 11 := by
  rw [periodic_closed_form]
  decide

/-! ## Values and uniqueness -/

theorem nfermion_small :
    NFermion 0 = 4 ∧ NFermion 1 = 1 ∧ NFermion 2 = 5 ∧ NFermion 3 = 4 ∧
    NFermion 4 = 9 ∧ NFermion 5 = 11 ∧ NFermion 6 = 20 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · unfold NFermion
      rw [nfermion_closed_form]
      decide

/-- The family leaves `[1, 13]` for good after index 5. -/
theorem nfermion_large (k : ℕ) (hk : 6 ≤ k) : 20 ≤ NFermion k := by
  unfold NFermion
  have hcf := nfermion_closed_form k
  rcases Nat.even_or_odd k with he | ho
  · have hs : signedLucasTrace k = lucas k := by
      unfold signedLucasTrace
      rw [he.neg_one_pow, one_mul]
    rw [hs, he.neg_one_pow] at hcf
    have h18 := lucas_lower_six k hk
    omega
  · have hs : signedLucasTrace k = -lucas k := by
      unfold signedLucasTrace
      rw [ho.neg_one_pow, neg_one_mul]
    rw [hs, ho.neg_one_pow] at hcf
    have h29 := lucas_lower_seven k (by
      rcases Nat.odd_iff.mp ho with h1
      omega)
    omega

/-- **Value uniqueness of the composite address**: any two-term family sum landing on 13 uses
the value pair `{4, 9}` — exactly the owned reading. -/
theorem composite_address_value_unique (m n : ℕ) (h : NFermion m + NFermion n = 13) :
    (NFermion m = 4 ∧ NFermion n = 9) ∨ (NFermion m = 9 ∧ NFermion n = 4) := by
  have hm : m ≤ 5 := by
    by_contra hc
    have := nfermion_large m (by omega)
    omega
  have hn : n ≤ 5 := by
    by_contra hc
    have := nfermion_large n (by omega)
    omega
  obtain ⟨v0, v1, v2, v3, v4, v5, v6⟩ := nfermion_small
  interval_cases m <;> interval_cases n <;> omega

/-- The Lucas recurrence inside the family and the scene degree identity share the arithmetic
`20 = 9 + 11`. Two owned facts, one equation — no binding minted. -/
theorem lucas_recurrence_shares_degree_arithmetic :
    (NFermion 6 = NFermion 4 + NFermion 5) ∧ (9 + 11 + 13 = 33) ∧ (33 - 13 = 9 + 11) := by
  obtain ⟨v0, v1, v2, v3, v4, v5, v6⟩ := nfermion_small
  refine ⟨by omega, by omega, by omega⟩

/-- **Assembled**: both closed forms; the double exclusion (13 outside BOTH owned families);
value-level necessity of the composite reading; the shared recurrence/degree equation. -/
theorem lefschetz_zone_exclusion :
    (∀ n, NFermionInt n = 1 + signedLucasTrace n + (-1) ^ n) ∧
    (∀ n, NFermion n ≠ 13) ∧
    (∀ n, (Matrix.det (T ^ n - 1)).natAbs ≠ 13) ∧
    (∀ m n, NFermion m + NFermion n = 13 →
      (NFermion m = 4 ∧ NFermion n = 9) ∨ (NFermion m = 9 ∧ NFermion n = 4)) ∧
    (NFermion 6 = NFermion 4 + NFermion 5) :=
  ⟨nfermion_closed_form, thirteen_no_direct_address, thirteen_no_periodic_address,
   composite_address_value_unique, lucas_recurrence_shares_degree_arithmetic.1⟩

end D0.Synthesis.LefschetzZoneExclusion
