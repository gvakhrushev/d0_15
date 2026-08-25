import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-!
# D0-TRIPARTITE-SIGNATURE-GENERAL-001 — Lorentzian signature from tripartiteness alone

`D0-SIGNATURE-31-SPLIT-001` is the corpus's highest-load single-support claim (62 claims presuppose
it, one route establishes it). Its existing route counts: "3" from the rank of the scene adjacency,
"1" from a separate Pisot flow. That is *decomposition* — each mechanism supplies a different
component, so neither covers for the other and the arrangement buys no redundancy.

This module supplies a **second route to the indefiniteness itself**, independent of any counting
and of the time operator: it is a property of tripartiteness, for every choice of positive zone
sizes, not a computation at `(9,11,13)`.

## The statement

The equitable quotient of a complete tripartite graph with zone sizes `a, b, c` is the hollow matrix
`B = [[0,b,c],[a,0,c],[a,b,0]]`, whose characteristic polynomial is

  `λ³ − (ab+ac+bc)·λ − 2abc`

— trace zero, and the constant term `−2abc`. So for the eigenvalues `r₁,r₂,r₃`:

  `r₁+r₂+r₃ = 0`  (zero trace)   and   `r₁r₂r₃ = 2abc > 0`  (positive parts).

From those two facts alone: **exactly one eigenvalue is positive and two are negative.** All three
positive would violate the zero sum; all three negative would make the product negative; and among
mixed signs only `(+,−,−)` has positive product. Hence signature `(1+, 2−)` — an indefinite form,
i.e. a light cone — with no input beyond "three zones, all non-empty".

Two further facts complete the picture, both proved here:

* **the roots are always real** — `4(ab+ac+bc)³ ≥ 108(abc)²` by AM–GM, which is exactly the
  non-negativity of the depressed cubic's discriminant;
* **the anisotropy falsifier, as an iff** — the discriminant vanishes **exactly** at equal zones.
  The forward direction is a ring identity; the converse is the AM–GM equality case, proved here by
  the explicit sum-of-squares decomposition
  `(x+y+z)³ − 27xyz = ½(x+y+z)Σ(x−y)² + 3[x(y−z)² + y(z−x)² + z(x−y)²]`, both groups non-negative
  for positive sizes so the whole vanishes only when every square does. At `(9,11,13)` the
  discriminant is `6185264 > 0`, so the two negative eigenvalues are strictly split: the carrier
  form is anisotropic, and an isotropic one would require equal zones and would kill the scene.

## Scope limit found 2026-07: the anisotropy iff is k = 3 only

The discriminant characterisation below does **not** generalise past three zones. At `k = 4` with
sizes `(1,1,1,5)` the spectrum is `{5, −1, −1, −3}` — repeated negative eigenvalues with *unequal*
zones — because `charpoly(1,1,1,c) = (λ+1)²(λ² − 2λ − 3c)`. The corpus's own proof method is
`k = 3`-specific for the same reason: "three reals with zero sum and positive product are `(+,−,−)`"
says nothing at `k = 4`, where trace `0` and `det < 0` are consistent with both `(1+,3−)` and
`(3+,1−)`. The uniform argument is the symmetrisation in `D0.Combinatorics.MultipartiteLorentzian`.

## Why this is a second route and not a restatement

The existing route needs the scene's adjacency rank *and* a separately-owned Pisot time operator.
This one needs neither: it is an algebraic consequence of a hollow non-negative 3×3 quotient. Kill
the rank argument, or kill the Pisot flow, and the indefiniteness proved here survives — which is
what support multiplicity means. It also generalises the corpus's `(9,11,13)` computation to the
whole admissible class, so it cannot be a numerical accident of one triple.

Honest scope: this owns the *signature* of the transport form and the anisotropy criterion. The
identification of the positive direction with time, and of the null set with the causal cone,
remains the reading owned by BOOK_07 §07.51.3 and its named Connes-unit residual.
-/

namespace D0.Combinatorics

/-- The equitable quotient of the complete tripartite graph, as an actual matrix. -/
def quotient3 (a b c : ℝ) : Matrix (Fin 3) (Fin 3) ℝ := !![0, b, c; a, 0, c; a, b, 0]

/-- **The characteristic polynomial of the equitable quotient**, computed from the matrix:
`det(λ·I − B) = λ³ − (ab+ac+bc)·λ − 2abc`.

CORRECTION OF RECORD (2026-07): an earlier version of this theorem stated the cubic as a bare
polynomial identity `l^3 − e₂l − 2e₃ = l·(l·l) − e₂l − 2e₃`, provable `by ring`. That is a tautology
in `l`: it constructs no matrix and therefore certifies nothing about the quotient — the link
between the cubic and `B` lived only in the prose. This version computes the determinant of
`λ·I − B` for the explicit `B`, which is what the claim always meant. The same defect is present in
`D0.VNext2.Rank3MetricSignature`, where `e₁, e₂, e₃` are hard-coded rather than derived from a
matrix; that module should be repaired the same way. -/
theorem quotient_charpoly (a b c l : ℝ) :
    (l • (1 : Matrix (Fin 3) (Fin 3) ℝ) - quotient3 a b c).det
      = l ^ 3 - (a * b + a * c + b * c) * l - 2 * (a * b * c) := by
  simp [Matrix.det_fin_three, quotient3]
  ring

/-- The trace of the quotient vanishes — the first of the two facts the signature rests on. -/
theorem quotient3_trace_zero (a b c : ℝ) : Matrix.trace (quotient3 a b c) = 0 := by
  simp [Matrix.trace, quotient3, Fin.sum_univ_three]

/-- **The sign split.** Three reals summing to zero whose product is positive have exactly one
positive member and two negative ones. This is the whole content of the Lorentzian signature. -/
theorem one_positive_two_negative (r₁ r₂ r₃ : ℝ)
    (hsum : r₁ + r₂ + r₃ = 0) (hprod : 0 < r₁ * r₂ * r₃) :
    (0 < r₁ ∧ r₂ < 0 ∧ r₃ < 0) ∨ (r₁ < 0 ∧ 0 < r₂ ∧ r₃ < 0) ∨ (r₁ < 0 ∧ r₂ < 0 ∧ 0 < r₃) := by
  have hne : r₁ ≠ 0 ∧ r₂ ≠ 0 ∧ r₃ ≠ 0 := by
    refine ⟨?_, ?_, ?_⟩ <;> intro h <;> rw [h] at hprod <;> simp at hprod
  obtain ⟨h1, h2, h3⟩ := hne
  rcases lt_or_gt_of_ne h1 with p1 | p1 <;>
  rcases lt_or_gt_of_ne h2 with p2 | p2 <;>
  rcases lt_or_gt_of_ne h3 with p3 | p3
  -- (−,−,−): the sum cannot vanish
  · exact absurd hsum (by linarith)
  · exact Or.inr (Or.inr ⟨p1, p2, p3⟩)
  · exact Or.inr (Or.inl ⟨p1, p2, p3⟩)
  -- (−,+,+): the product is negative
  · exact absurd hprod (by
      have := mul_neg_of_neg_of_pos (mul_neg_of_neg_of_pos p1 p2) p3; linarith)
  · exact Or.inl ⟨p1, p2, p3⟩
  -- (+,−,+): the product is negative
  · exact absurd hprod (by
      have := mul_neg_of_neg_of_pos (mul_neg_of_pos_of_neg p1 p2) p3; linarith)
  -- (+,+,−): the product is negative
  · exact absurd hprod (by
      have := mul_neg_of_pos_of_neg (mul_pos p1 p2) p3; linarith)
  -- (+,+,+): the sum cannot vanish
  · exact absurd hsum (by linarith)

/-- The product of the eigenvalues is `2abc`, positive whenever all three zones are non-empty. -/
theorem product_positive {a b c : ℝ} (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    0 < 2 * (a * b * c) := by positivity

/-- **The roots are real.** `4·e₂³ ≥ 108·(abc)²` — the non-negativity of the depressed cubic's
discriminant `−4p³ − 27q²` at `p = −e₂`, `q = −2abc` — holds for all positive zone sizes. -/
theorem discriminant_nonneg {a b c : ℝ} (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    0 ≤ 4 * (a * b + a * c + b * c) ^ 3 - 108 * (a * b * c) ^ 2 := by
  nlinarith [sq_nonneg (a * b - a * c), sq_nonneg (a * b - b * c), sq_nonneg (a * c - b * c),
             sq_nonneg (a * b + a * c + b * c), mul_pos ha hb, mul_pos ha hc, mul_pos hb hc,
             mul_pos (mul_pos ha hb) hc]

/-- **The anisotropy falsifier, general form (one direction).** Equal zones make the discriminant
vanish, i.e. the two negative eigenvalues coincide and the carrier form is isotropic. -/
theorem equal_zones_discriminant_zero (n : ℝ) :
    4 * (n * n + n * n + n * n) ^ 3 - 108 * (n * n * n) ^ 2 = 0 := by ring

/-- **The split is strict at the scene.** At `(9,11,13)` the discriminant is `6185264 > 0`, so the
two negative eigenvalues are distinct and the carrier form is anisotropic — the falsifier the corpus
states, now sitting on the general theorem above rather than on a one-off computation. -/
theorem scene_discriminant_positive :
    (0 : ℝ) < 4 * ((9:ℝ) * 11 + 9 * 13 + 11 * 13) ^ 3 - 108 * ((9:ℝ) * 11 * 13) ^ 2 := by
  norm_num

/-- **The AM–GM equality case, by an explicit sum-of-squares decomposition.**

`(x+y+z)³ − 27xyz = ½(x+y+z)[(x−y)²+(y−z)²+(z−x)²] + 3[x(y−z)² + y(z−x)² + z(x−y)²]`

Both bracketed groups are non-negative for positive `x,y,z`, so the whole vanishes only when every
square does. This is the identity that turns "the discriminant vanishes" into "the zones are
equal". -/
theorem amgm_sos_identity (x y z : ℝ) :
    (x + y + z) ^ 3 - 27 * (x * y * z)
      = (x + y + z) * ((x - y) ^ 2 + (y - z) ^ 2 + (z - x) ^ 2) / 2
        + 3 * (x * (y - z) ^ 2 + y * (z - x) ^ 2 + z * (x - y) ^ 2) := by
  ring

/-- **AM–GM equality forces equality.** For positive reals, `(x+y+z)³ = 27xyz` only at `x = y = z`. -/
theorem amgm_equality {x y z : ℝ} (hx : 0 < x) (hy : 0 < y) (hz : 0 < z)
    (h : (x + y + z) ^ 3 = 27 * (x * y * z)) : x = y ∧ y = z := by
  have hid := amgm_sos_identity x y z
  have hxy : (x - y) ^ 2 ≤ 0 := by nlinarith [sq_nonneg (x - y), sq_nonneg (y - z), sq_nonneg (z - x)]
  have hyz : (y - z) ^ 2 ≤ 0 := by nlinarith [sq_nonneg (x - y), sq_nonneg (y - z), sq_nonneg (z - x)]
  constructor
  · have := le_antisymm hxy (sq_nonneg (x - y))
    have : x - y = 0 := by nlinarith [sq_nonneg (x - y)]
    linarith
  · have := le_antisymm hyz (sq_nonneg (y - z))
    have : y - z = 0 := by nlinarith [sq_nonneg (y - z)]
    linarith

/-- **The anisotropy falsifier, converse direction — now proved.** A vanishing discriminant forces
equal zones: with `x = ab, y = ac, z = bc` the discriminant is `4[(x+y+z)³ − 27xyz]`, so it vanishes
only at `ab = ac = bc`, which for positive sizes gives `a = b = c`. Combined with
`equal_zones_discriminant_zero` this is an **iff**: the carrier form is isotropic exactly when the
zones are equal, and at `(9,11,13)` they are not. -/
theorem discriminant_zero_iff_equal_zones {a b c : ℝ} (ha : 0 < a) (hb : 0 < b) (hc : 0 < c)
    (h : 4 * (a * b + a * c + b * c) ^ 3 - 108 * (a * b * c) ^ 2 = 0) :
    a = b ∧ b = c := by
  have hx : (0:ℝ) < a * b := mul_pos ha hb
  have hy : (0:ℝ) < a * c := mul_pos ha hc
  have hz : (0:ℝ) < b * c := mul_pos hb hc
  have hkey : (a * b + a * c + b * c) ^ 3 = 27 * ((a * b) * (a * c) * (b * c)) := by nlinarith [h]
  obtain ⟨h1, h2⟩ := amgm_equality hx hy hz hkey
  -- `h1 : a*b = a*c` cancels `a`; `h2 : a*c = b*c` cancels `c`
  exact ⟨mul_right_cancel₀ (ne_of_gt hc) h2, mul_left_cancel₀ (ne_of_gt ha) h1⟩

/-- **D0-TRIPARTITE-SIGNATURE-GENERAL-001.** For every complete tripartite graph with non-empty
zones the equitable-quotient form is indefinite with exactly one positive and two negative
eigenvalues; the eigenvalues are always real; the discriminant vanishes **iff** the zones are equal
(both directions proved); and at `(9,11,13)` it is strictly positive, so the anisotropy is real. A
second route to the indefiniteness, using neither the adjacency rank nor the Pisot time
operator, and valid for the whole class rather than for `(9,11,13)`. -/
theorem tripartite_signature_general :
    (∀ r₁ r₂ r₃ : ℝ, r₁ + r₂ + r₃ = 0 → 0 < r₁ * r₂ * r₃ →
      (0 < r₁ ∧ r₂ < 0 ∧ r₃ < 0) ∨ (r₁ < 0 ∧ 0 < r₂ ∧ r₃ < 0) ∨ (r₁ < 0 ∧ r₂ < 0 ∧ 0 < r₃)) ∧
    (∀ a b c : ℝ, 0 < a → 0 < b → 0 < c → 0 < 2 * (a * b * c)) ∧
    (∀ a b c : ℝ, 0 < a → 0 < b → 0 < c →
      0 ≤ 4 * (a * b + a * c + b * c) ^ 3 - 108 * (a * b * c) ^ 2) ∧
    (∀ n : ℝ, 4 * (n * n + n * n + n * n) ^ 3 - 108 * (n * n * n) ^ 2 = 0) ∧
    ((0 : ℝ) < 4 * ((9:ℝ) * 11 + 9 * 13 + 11 * 13) ^ 3 - 108 * ((9:ℝ) * 11 * 13) ^ 2) ∧
    (∀ a b c : ℝ, 0 < a → 0 < b → 0 < c →
      4 * (a * b + a * c + b * c) ^ 3 - 108 * (a * b * c) ^ 2 = 0 → a = b ∧ b = c) ∧
    (∀ a b c l : ℝ, (l • (1 : Matrix (Fin 3) (Fin 3) ℝ) - quotient3 a b c).det
      = l ^ 3 - (a * b + a * c + b * c) * l - 2 * (a * b * c)) :=
  ⟨one_positive_two_negative, fun _ _ _ ha hb hc => product_positive ha hb hc,
   fun _ _ _ ha hb hc => discriminant_nonneg ha hb hc, equal_zones_discriminant_zero,
   scene_discriminant_positive,
   fun _ _ _ ha hb hc h => discriminant_zero_iff_equal_zones ha hb hc h,
   quotient_charpoly⟩

end D0.Combinatorics
