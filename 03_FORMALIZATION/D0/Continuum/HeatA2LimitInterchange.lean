import Mathlib.Data.Real.Basic
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Tactic

/-!
# D0.Continuum.HeatA2LimitInterchange

Theoretical owner: `D0-HEAT-A2-LIMIT-INTERCHANGE-001`.

Analytic firewall against spectral pollution in the short-time expansion of the heat trace:
Formalization of the limit interchange lemma for the $a_2$ coefficient in the short-time
asymptotics of a sequence of heat traces $F_N(t)$.

Setup:
- Consider a family of functions $F_N, F : (0, t_0] \to \mathbb{R}$ expanding as:
  $$F_N(t) = \frac{a_{0,N}}{t^2} + \frac{a_{2,N}}{t} + R_N(t)$$
  $$F(t) = \frac{a_0}{t^2} + \frac{a_2}{t} + R(t)$$
- Key uniform remainder bound: there exists $C \ge 0$ such that for all $N$ and all $t \in (0, t_0]$,
  $$|R_N(t)| \le C \quad \text{and} \quad |R(t)| \le C.$$
- Pointwise convergence: for every fixed $t \in (0, t_0]$, $F_N(t) \to F(t)$ as $N \to \infty$.
- Volume coefficient convergence: $a_{0,N} \to a_0$ as $N \to \infty$.

Algebraic Identity:
Multiplying by $t$:
$$t F_N(t) - \frac{a_{0,N}}{t} = a_{2,N} + t R_N(t)$$
Therefore:
$$a_{2,N} - a_2 = t (F_N(t) - F(t)) - \frac{a_{0,N} - a_0}{t} - t (R_N(t) - R(t)).$$

Bounding for any fixed $t \in (0, t_0]$:
$$|a_{2,N} - a_2| \le t |F_N(t) - F(t)| + \frac{|a_{0,N} - a_0|}{t} + 2 C t.$$

Consequently, taking $\limsup_{N \to \infty}$ yields:
$$\limsup_{N \to \infty} |a_{2,N} - a_2| \le 2 C t.$$
Since this holds for arbitrarily small $t > 0$, it follows that $a_{2,N} \to a_2$.

This is a pure mathematical analysis theorem, independent of any smooth manifold prior,
providing the exact rigorous bridge from discrete $a_{2,N}$ to continuum Einstein-Hilbert action.
-/

namespace D0.Continuum.HeatA2LimitInterchange

/-- The fundamental algebraic identity relating $a_{2,N} - a_2$ to $F_N - F$, $a_{0,N} - a_0$, and $R_N - R$. -/
theorem a2_difference_identity
    (t a0N a2N RN a0 a2 R FN F : ℝ)
    (ht : t ≠ 0)
    (hFN : FN = a0N / t ^ 2 + a2N / t + RN)
    (hF : F = a0 / t ^ 2 + a2 / t + R) :
    a2N - a2 = t * (FN - F) - (a0N - a0) / t - t * (RN - R) := by
  rw [hFN, hF]
  have ht2 : t ^ 2 = t * t := sq t
  field_simp
  ring

/-- Error bound at a fixed scale $t > 0$ under uniform remainder bounds $|R_N| \le C$ and $|R| \le C$. -/
theorem a2_error_bound_at_t
    (t a0N a2N RN a0 a2 R FN F C : ℝ)
    (ht_pos : 0 < t)
    (hFN : FN = a0N / t ^ 2 + a2N / t + RN)
    (hF : F = a0 / t ^ 2 + a2 / t + R)
    (hRN : |RN| ≤ C)
    (hR : |R| ≤ C) :
    |a2N - a2| ≤ t * |FN - F| + |a0N - a0| / t + 2 * C * t := by
  have ht_ne : t ≠ 0 := ne_of_gt ht_pos
  have h_id := a2_difference_identity t a0N a2N RN a0 a2 R FN F ht_ne hFN hF
  rw [h_id]
  have h_tri1 : |t * (FN - F) - (a0N - a0) / t - t * (RN - R)| ≤
                |t * (FN - F) - (a0N - a0) / t| + |t * (RN - R)| := by
    exact abs_sub (t * (FN - F) - (a0N - a0) / t) (t * (RN - R))
  have h_tri2 : |t * (FN - F) - (a0N - a0) / t| ≤ |t * (FN - F)| + |(a0N - a0) / t| := by
    exact abs_sub (t * (FN - F)) ((a0N - a0) / t)
  have h_rem : |t * (RN - R)| ≤ 2 * C * t := by
    rw [abs_mul, abs_of_pos ht_pos]
    have h_diff_rem : |RN - R| ≤ 2 * C := by
      calc |RN - R| ≤ |RN| + |R| := abs_sub RN R
      _ ≤ C + C := add_le_add hRN hR
      _ = 2 * C := by ring
    calc t * |RN - R| ≤ t * (2 * C) := mul_le_mul_of_nonneg_left h_diff_rem (le_of_lt ht_pos)
    _ = 2 * C * t := by ring
  have h_term1 : |t * (FN - F)| = t * |FN - F| := by
    rw [abs_mul, abs_of_pos ht_pos]
  have h_term2 : |(a0N - a0) / t| = |a0N - a0| / t := by
    rw [abs_div, abs_of_pos ht_pos]
  linarith

/-- **D0-HEAT-A2-LIMIT-INTERCHANGE-001 (CORE-FORMALIZED).**
For any sequence of heat trace expansions with uniformly bounded remainders,
if $F_N(t) \to F(t)$ pointwise and $a_{0,N} \to a_0$, then $a_{2,N} \to a_2$.
Formulated via $\varepsilon$-$\delta$ convergence: for any $\varepsilon > 0$,
there exists $N_0$ such that for all $N \ge N_0$, $|a_{2,N} - a_2| < \varepsilon$. -/
theorem heat_a2_limit_interchange
    (a0N a2N : ℕ → ℝ) (RN : ℕ → ℝ → ℝ)
    (a0 a2 : ℝ) (R : ℝ → ℝ)
    (FN : ℕ → ℝ → ℝ) (F : ℝ → ℝ)
    (C t0 : ℝ) (ht0 : 0 < t0) (hC : 0 ≤ C)
    (hFN : ∀ N, ∀ t, 0 < t → t ≤ t0 → FN N t = a0N N / t ^ 2 + a2N N / t + RN N t)
    (hF : ∀ t, 0 < t → t ≤ t0 → F t = a0 / t ^ 2 + a2 / t + R t)
    (hRN : ∀ N, ∀ t, 0 < t → t ≤ t0 → |RN N t| ≤ C)
    (hR : ∀ t, 0 < t → t ≤ t0 → |R t| ≤ C)
    (hconv_F : ∀ t, 0 < t → t ≤ t0 → ∀ ε > 0, ∃ N_F, ∀ N ≥ N_F, |FN N t - F t| < ε)
    (hconv_a0 : ∀ ε > 0, ∃ N_0, ∀ N ≥ N_0, |a0N N - a0| < ε) :
    ∀ ε > 0, ∃ N_star, ∀ N ≥ N_star, |a2N N - a2| < ε := by
  intro ε hε
  have hC_pos : 0 < 2 * C + 1 := by linarith
  have ht_cand_pos : 0 < (ε / 4) / (2 * C + 1) := by
    have : 0 < ε / 4 := by linarith
    exact div_pos this hC_pos
  let t_test := min (t0 / 2) ((ε / 4) / (2 * C + 1))
  have ht_test_pos : 0 < t_test := lt_min (by linarith) ht_cand_pos
  have ht_test_le_t0 : t_test ≤ t0 := by
    have : t_test ≤ t0 / 2 := min_le_left _ _
    linarith
  have h_bound_rem : 2 * C * t_test < ε / 3 := by
    have ht_le_cand : t_test ≤ (ε / 4) / (2 * C + 1) := min_le_right _ _
    have h_step1 : 2 * C * t_test ≤ (2 * C + 1) * t_test := by
      have : 0 ≤ t_test := le_of_lt ht_test_pos
      have : 2 * C ≤ 2 * C + 1 := by linarith
      nlinarith
    have h_step2 : (2 * C + 1) * t_test ≤ ε / 4 := by
      have h_cancel : (2 * C + 1) * ((ε / 4) / (2 * C + 1)) = ε / 4 := by
        rw [mul_div_cancel₀]
        linarith
      calc (2 * C + 1) * t_test ≤ (2 * C + 1) * ((ε / 4) / (2 * C + 1)) :=
        mul_le_mul_of_nonneg_left ht_le_cand (by linarith)
      _ = ε / 4 := h_cancel
    have : ε / 4 < ε / 3 := by linarith
    linarith
  -- Now choose N large enough for F_N(t_test) and a0_N
  have h_eps3 : 0 < (ε / 3) / t_test := div_pos (by linarith) ht_test_pos
  have h_eps3_mul : 0 < (ε / 3) * t_test := mul_pos (by linarith) ht_test_pos
  obtain ⟨N_F, hNF⟩ := hconv_F t_test ht_test_pos ht_test_le_t0 ((ε / 3) / t_test) h_eps3
  obtain ⟨N_0, hN0⟩ := hconv_a0 ((ε / 3) * t_test) h_eps3_mul
  let N_star := max N_F N_0
  use N_star
  intro N hN
  have hN_ge_F : N ≥ N_F := le_trans (le_max_left _ _) hN
  have hN_ge_0 : N ≥ N_0 := le_trans (le_max_right _ _) hN
  have h_F_close := hNF N hN_ge_F
  have h_a0_close := hN0 N hN_ge_0
  have h_pt_bound := a2_error_bound_at_t t_test (a0N N) (a2N N) (RN N t_test) a0 a2 (R t_test)
    (FN N t_test) (F t_test) C ht_test_pos
    (hFN N t_test ht_test_pos ht_test_le_t0)
    (hF t_test ht_test_pos ht_test_le_t0)
    (hRN N t_test ht_test_pos ht_test_le_t0)
    (hR t_test ht_test_pos ht_test_le_t0)
  have h_term1_lt : t_test * |FN N t_test - F t_test| < ε / 3 := by
    calc t_test * |FN N t_test - F t_test| < t_test * ((ε / 3) / t_test) :=
      mul_lt_mul_of_pos_left h_F_close ht_test_pos
    _ = ε / 3 := by
      rw [mul_div_cancel₀]
      exact ne_of_gt ht_test_pos
  have h_term2_lt : |a0N N - a0| / t_test < ε / 3 := by
    rw [div_lt_iff₀ ht_test_pos]
    linarith
  linarith

end D0.Continuum.HeatA2LimitInterchange
