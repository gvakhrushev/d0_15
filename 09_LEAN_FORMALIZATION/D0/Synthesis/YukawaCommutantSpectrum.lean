import D0.Spectral.JointCommutant
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Tactic

/-!
# The equivariant Yukawa spectrum: automatic three-fold splitting from the transport cubic

The Yukawa tension log (`YUKAWA_COMMUTANT_TENSION_LOG.md`, 2026-08-01) records that the owned
overlap scaffold is NOT in `ℚ[Q]` — the joint commutant of `{Aut, adjacency}` on the visible
3-space (`D0.Spectral.JointCommutant`) — and names two owner-gated resolutions. This module
supplies the mathematics of resolution 2 (the "interesting branch", Campaign 3 item 4 of
`NEXT_FRONT_PLAN_2026_08.md`) **without deciding it**: what is guaranteed if the Yukawa operator
on the generation space is taken from the equivariant-and-adjacency-compatible class.

In that class an operator is `a + bQ + cQ²` with `a, b, c ∈ ℚ` (the `ℚ[Q]` identification is
DOCSTRING-GRADE in the owner — `JointCommutant.visible_centraliser_dim` is a placeholder `rfl`;
the centraliser argument is standard prose there — flagged here exactly like spectral mapping;
the theorems below quantify over `(a, b, c)` literally and are self-contained), and
its spectrum is `{a + bλᵢ + cλᵢ²}` for the three roots `λᵢ` of the transport cubic
`λ³ − 359λ − 2574` (spectral mapping — docstring grade, standard). Proved here:

* `no_rational_root_rat` — the FULLY QUANTIFIED irrationality `∀ q : ℚ, q³ − 359q − 2574 ≠ 0`.
  The owned statements (`JointCommutant.no_rational_root`, `TransportNotGolden.
  transport_no_rational_root`) are divisor-list sweeps over integer candidates; the rational-root
  theorem step (monic ⇒ a rational root is an integer; self-contained integer exclusion
  `no_integer_root` by tail bounds + finite sweep) closes the full field-level statement.
* `qq_spectrum_splits` — **automatic non-degeneracy**: for EVERY non-scalar member (`(b, c) ≠
  (0, 0)`) and any two distinct real roots `λ ≠ μ`, the values `a + bλ + cλ²` and `a + bμ + cμ²`
  differ. Mechanism: equality would force `λ + μ = −b/c ∈ ℚ`, and the division identity for the
  monic cubic then makes `b/c` a rational root of the transport cubic itself
  (`(λ+μ)³ − 359(λ+μ) + 2574 = 0` is derivable from the two root equations alone) —
  contradicting `no_rational_root_rat`. **The same irreducibility that defines the commutant
  forbids Yukawa degeneracy.**
* `transport_three_real_roots` — three distinct real roots WITH exported locations, in the
  OWNED integer brackets `(−13,−12)`, `(−10,−9)`, `(21,22)` (the ℚ sign table is
  `TransportNotGolden.transport_roots_bracketed`; discriminant-grade realness is owned by
  `D0-MIXING-HIERARCHY-INVERSION-001`, `D0-RANK3-METRIC-TRANSPORT-001`,
  `D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001` — this is the first Lean proposition with
  REAL-TYPED root existence, scoped exactly so). The exported brackets give float-free ratio
  bounds: `|λ₁|/|λ₂| ≤ 13/9`, `λ₃/|λ₁| ≤ 22/12`, `λ₃/|λ₂| ≤ 22/9 < 2.5` — squares `< 6`.
* `no_rational_value_at_root` — non-scalar members take IRRATIONAL values at every transport
  root: the attainable value triples are a dense countable set, so the class approximates any
  target but hits none exactly (the memo's C2(b), repaired).
* `equivariant_yukawa_rigidity` — assembled: three distinct real transport eigenvalues exist,
  and every non-scalar equivariant Yukawa splits them into three pairwise distinct generation
  values. **Three non-degenerate generations are a theorem of the equivariant class, not a
  modelling choice**; the free 3×3 matrix (9 parameters) collapses to `(a, b, c)` (3 rational
  parameters), with all differences controlled by `(b, c)` alone.

**Scope honesty.** No mass values are claimed and no member `(a, b, c)` is selected — binding
the class to the charged-lepton table is the owner-gated content of resolution 2 (the ratios
would be fixed by the choice, hence immediately falsifiable — trap-(f)-clean by construction,
as the plan requires). The tension log's fork stays open; resolution 1 (different carrier for
the scaffold) is untouched. The Puiseux/Green-function leg lives on the 7-point shell torus (a
different carrier, per the log's cross-reference) and is not addressed. Spectral mapping
(matrix ↦ eigenvalue polynomial) is used at docstring grade, not formalized.
-/

namespace D0.Synthesis.YukawaCommutantSpectrum

/-! ## Full rational-root exclusion -/

/-- No INTEGER root: tail bounds `|n| ≥ 22` plus a finite sweep of `|n| ≤ 21`. -/
theorem no_integer_root (n : ℤ) : n ^ 3 - 359 * n - 2574 ≠ 0 := by
  intro h
  rcases (by omega : n ≤ 21 ∨ 22 ≤ n) with h1 | h1
  · rcases (by omega : -21 ≤ n ∨ n ≤ -22) with h2 | h2
    · interval_cases n <;> revert h <;> decide
    · have hn : n ≤ -22 := h2
      have hb : (0 : ℤ) ≤ n ^ 2 - 484 := by nlinarith [sq_nonneg (n + 22)]
      have ha : (0 : ℤ) ≤ -n - 22 := by omega
      nlinarith [mul_nonneg ha hb]
  · have hn : 22 ≤ n := h1
    have hb : (0 : ℤ) ≤ n ^ 2 - 484 := by nlinarith [sq_nonneg (n - 22)]
    have ha : (0 : ℤ) ≤ n - 22 := by omega
    nlinarith [mul_nonneg ha hb]

/-- **No RATIONAL root, fully quantified**: the monic transport cubic has no root in `ℚ`.
Rational-root theorem: clearing denominators forces the denominator to divide the numerator
cube, coprimality kills it, and `no_integer_root` finishes. -/
theorem no_rational_root_rat (q : ℚ) : q ^ 3 - 359 * q - 2574 ≠ 0 := by
  intro hq
  have hnum : (q.num : ℚ) = q * (q.den : ℚ) := by
    have h0 := Rat.num_div_den q
    have hden : (q.den : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr q.den_nz
    field_simp at h0
    linarith [h0]
  have hint : q.num ^ 3 - 359 * q.num * (q.den : ℤ) ^ 2 - 2574 * (q.den : ℤ) ^ 3 = 0 := by
    have hcalc : ((q.num ^ 3 - 359 * q.num * (q.den : ℤ) ^ 2 - 2574 * (q.den : ℤ) ^ 3 : ℤ) : ℚ)
        = (q ^ 3 - 359 * q - 2574) * (q.den : ℚ) ^ 3 := by
      push_cast
      rw [hnum]
      ring
    rw [hq, zero_mul] at hcalc
    exact_mod_cast hcalc
  have hdvd : (q.den : ℤ) ∣ q.num ^ 3 :=
    ⟨359 * q.num * (q.den : ℤ) + 2574 * (q.den : ℤ) ^ 2, by linear_combination hint⟩
  have hdvdN : q.den ∣ q.num.natAbs ^ 3 := by
    have h1 := Int.natAbs_dvd_natAbs.mpr hdvd
    simpa [Int.natAbs_pow] using h1
  have hcop : Nat.Coprime q.den (q.num.natAbs ^ 3) := (q.reduced.symm).pow_right 3
  have hg := Nat.dvd_gcd (dvd_refl q.den) hdvdN
  rw [hcop.gcd_eq_one] at hg
  have hden1 : q.den = 1 := Nat.dvd_one.mp hg
  have hqz : q = (q.num : ℚ) := by
    conv_lhs => rw [← Rat.num_div_den q]
    rw [hden1]
    norm_num
  have hZ : q.num ^ 3 - 359 * q.num - 2574 = 0 := by
    have h2 : ((q.num : ℚ)) ^ 3 - 359 * (q.num : ℚ) - 2574 = 0 := by
      rw [← hqz]; exact hq
    exact_mod_cast h2
  exact no_integer_root q.num hZ

/-! ## Automatic three-fold splitting -/

/-- **Non-degeneracy is automatic in the equivariant class**: a non-scalar `a + bQ + cQ²` takes
different values at different transport roots. Equality would force `b/c` to be a rational root
of the transport cubic itself. -/
theorem qq_spectrum_splits (a b c : ℚ) (hbc : ¬(b = 0 ∧ c = 0))
    (lam mu : ℝ) (hl : lam ^ 3 - 359 * lam - 2574 = 0)
    (hm : mu ^ 3 - 359 * mu - 2574 = 0) (hne : lam ≠ mu) :
    (a : ℝ) + b * lam + c * lam ^ 2 ≠ (a : ℝ) + b * mu + c * mu ^ 2 := by
  intro heq
  have hfac : (lam - mu) * ((b : ℝ) + (c : ℝ) * (lam + mu)) = 0 := by
    linear_combination heq
  have hsum : (b : ℝ) + (c : ℝ) * (lam + mu) = 0 :=
    (mul_eq_zero.mp hfac).resolve_left (sub_ne_zero.mpr hne)
  by_cases hc : c = 0
  · have hcR : (c : ℝ) = 0 := by exact_mod_cast hc
    have hb : (b : ℝ) = 0 := by rw [hcR] at hsum; linarith
    exact hbc ⟨by exact_mod_cast hb, hc⟩
  · have hcR : (c : ℝ) ≠ 0 := by exact_mod_cast hc
    have hs : lam + mu = -((b : ℝ) / (c : ℝ)) := by
      field_simp
      linear_combination hsum
    have hquadfac : (lam - mu) * (lam ^ 2 + lam * mu + mu ^ 2 - 359) = 0 := by
      linear_combination hl - hm
    have hquad : lam ^ 2 + lam * mu + mu ^ 2 - 359 = 0 :=
      (mul_eq_zero.mp hquadfac).resolve_left (sub_ne_zero.mpr hne)
    have hprod : lam * mu * (lam + mu) + 2574 = 0 := by
      linear_combination lam * hquad - hl
    have hkey : (lam + mu) ^ 3 - 359 * (lam + mu) + 2574 = 0 := by
      linear_combination hl + hm + 3 * hprod
    rw [hs] at hkey
    have hR : ((b / c : ℚ) : ℝ) ^ 3 - 359 * ((b / c : ℚ) : ℝ) - 2574 = 0 := by
      push_cast
      linear_combination -hkey
    have hQ : (b / c : ℚ) ^ 3 - 359 * (b / c) - 2574 = 0 := by exact_mod_cast hR
    exact no_rational_root_rat (b / c) hQ

/-! ## Three distinct real transport eigenvalues -/

/-- The transport cubic has three distinct real roots, in the OWNED integer brackets of
`TransportNotGolden.transport_roots_bracketed` (`(−13,−12)`, `(−10,−9)`, `(21,22)` — the sign
table is owned there over ℚ; here it is combined with the IVT to export real-typed existence
WITH locations in the statement). -/
theorem transport_three_real_roots :
    ∃ l1 l2 l3 : ℝ,
      (l1 ^ 3 - 359 * l1 - 2574 = 0) ∧ (l2 ^ 3 - 359 * l2 - 2574 = 0) ∧
      (l3 ^ 3 - 359 * l3 - 2574 = 0) ∧
      (-13 ≤ l1 ∧ l1 ≤ -12) ∧ (-10 ≤ l2 ∧ l2 ≤ -9) ∧ (21 ≤ l3 ∧ l3 ≤ 22) ∧
      l1 < l2 ∧ l2 < l3 := by
  have hcont : Continuous fun x : ℝ => x ^ 3 - 359 * x - 2574 := by continuity
  obtain ⟨x1, hx1, hf1⟩ :=
    intermediate_value_Icc (by norm_num : (-13 : ℝ) ≤ -12) hcont.continuousOn
      (by norm_num :
        (0 : ℝ) ∈ Set.Icc ((-13 : ℝ) ^ 3 - 359 * (-13) - 2574)
          ((-12 : ℝ) ^ 3 - 359 * (-12) - 2574))
  obtain ⟨x2, hx2, hf2⟩ :=
    intermediate_value_Icc' (by norm_num : (-10 : ℝ) ≤ -9) hcont.continuousOn
      (by norm_num :
        (0 : ℝ) ∈ Set.Icc ((-9 : ℝ) ^ 3 - 359 * (-9) - 2574)
          ((-10 : ℝ) ^ 3 - 359 * (-10) - 2574))
  obtain ⟨x3, hx3, hf3⟩ :=
    intermediate_value_Icc (by norm_num : (21 : ℝ) ≤ 22) hcont.continuousOn
      (by norm_num :
        (0 : ℝ) ∈ Set.Icc ((21 : ℝ) ^ 3 - 359 * 21 - 2574)
          ((22 : ℝ) ^ 3 - 359 * 22 - 2574))
  refine ⟨x1, x2, x3, hf1, hf2, hf3, ⟨hx1.1, hx1.2⟩, ⟨hx2.1, hx2.2⟩, ⟨hx3.1, hx3.2⟩, ?_, ?_⟩
  · linarith [hx1.2, hx2.1]
  · linarith [hx2.2, hx3.1]

/-! ## Forced irrationality of the generation values -/

/-- **Non-scalar equivariant Yukawa values are never rational**: at any transport root, a
non-scalar `a + bQ + cQ²` takes an irrational value. (Consequently the attainable value triples
form a dense countable set — the class can approximate any target to arbitrary precision but
hits none exactly; see the memo's C2(b) as repaired.) -/
theorem no_rational_value_at_root (a b c r : ℚ) (hbc : ¬(b = 0 ∧ c = 0))
    (lam : ℝ) (hl : lam ^ 3 - 359 * lam - 2574 = 0) :
    (a : ℝ) + b * lam + c * lam ^ 2 ≠ r := by
  have hlam_irr : ∀ s : ℚ, lam ≠ (s : ℝ) := by
    intro s hs
    apply no_rational_root_rat s
    have h0 : ((s : ℝ)) ^ 3 - 359 * (s : ℝ) - 2574 = 0 := by rw [← hs]; exact hl
    exact_mod_cast h0
  intro heq
  by_cases hc : c = 0
  · have hb : b ≠ 0 := fun h => hbc ⟨h, hc⟩
    have hbR : (b : ℝ) ≠ 0 := by exact_mod_cast hb
    have hcR : (c : ℝ) = 0 := by exact_mod_cast hc
    refine hlam_irr ((r - a) / b) ?_
    push_cast
    rw [eq_div_iff hbR]
    linear_combination heq - lam ^ 2 * hcR
  · have hquad : (c : ℝ) * lam ^ 2 = -(b : ℝ) * lam + ((r : ℝ) - (a : ℝ)) := by
      linear_combination heq
    have hcube2 : ((b : ℝ) ^ 2 + (c : ℝ) * ((r : ℝ) - (a : ℝ)) - 359 * (c : ℝ) ^ 2) * lam
        = 2574 * (c : ℝ) ^ 2 + (b : ℝ) * ((r : ℝ) - (a : ℝ)) := by
      linear_combination (c : ℝ) ^ 2 * hl - ((c : ℝ) * lam - (b : ℝ)) * hquad
    by_cases hD : (b ^ 2 + c * (r - a) - 359 * c ^ 2 : ℚ) = 0
    · have hDR : ((b : ℝ) ^ 2 + (c : ℝ) * ((r : ℝ) - (a : ℝ)) - 359 * (c : ℝ) ^ 2) = 0 := by
        exact_mod_cast hD
      rw [hDR, zero_mul] at hcube2
      have hE : (2574 * c ^ 2 + b * (r - a) : ℚ) = 0 := by exact_mod_cast hcube2.symm
      apply no_rational_root_rat (b / c)
      have hcleared : b ^ 3 - 359 * b * c ^ 2 - 2574 * c ^ 3 = 0 := by
        linear_combination b * hD - c * hE
      have hcQ : c ≠ 0 := hc
      field_simp
      first
      | linear_combination hcleared
      | linear_combination -hcleared
      | linear_combination c ^ 3 * hcleared
    · have hDR : ((b : ℝ) ^ 2 + (c : ℝ) * ((r : ℝ) - (a : ℝ)) - 359 * (c : ℝ) ^ 2) ≠ 0 := by
        exact_mod_cast hD
      refine hlam_irr ((2574 * c ^ 2 + b * (r - a)) / (b ^ 2 + c * (r - a) - 359 * c ^ 2)) ?_
      push_cast
      rw [eq_div_iff hDR]
      linear_combination hcube2

/-! ## Assembled -/

/-- **Equivariant Yukawa rigidity**: three distinct real transport eigenvalues in owned
brackets; every non-scalar member splits them into pairwise distinct — and individually
irrational — generation values; the cubic has no rational root at full ℚ grade. -/
theorem equivariant_yukawa_rigidity :
    (∃ l1 l2 l3 : ℝ,
      (l1 ^ 3 - 359 * l1 - 2574 = 0) ∧ (l2 ^ 3 - 359 * l2 - 2574 = 0) ∧
      (l3 ^ 3 - 359 * l3 - 2574 = 0) ∧
      (-13 ≤ l1 ∧ l1 ≤ -12) ∧ (-10 ≤ l2 ∧ l2 ≤ -9) ∧ (21 ≤ l3 ∧ l3 ≤ 22) ∧
      l1 < l2 ∧ l2 < l3) ∧
    (∀ a b c : ℚ, ¬(b = 0 ∧ c = 0) →
      ∀ lam mu : ℝ, lam ^ 3 - 359 * lam - 2574 = 0 → mu ^ 3 - 359 * mu - 2574 = 0 →
        lam ≠ mu →
        (a : ℝ) + b * lam + c * lam ^ 2 ≠ (a : ℝ) + b * mu + c * mu ^ 2) ∧
    (∀ a b c r : ℚ, ¬(b = 0 ∧ c = 0) → ∀ lam : ℝ, lam ^ 3 - 359 * lam - 2574 = 0 →
      (a : ℝ) + b * lam + c * lam ^ 2 ≠ r) ∧
    (∀ q : ℚ, q ^ 3 - 359 * q - 2574 ≠ 0) :=
  ⟨transport_three_real_roots, qq_spectrum_splits, no_rational_value_at_root,
   no_rational_root_rat⟩

end D0.Synthesis.YukawaCommutantSpectrum
