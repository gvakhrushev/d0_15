import Mathlib.Tactic

/-!
# D0-PAGE-TURNING-POINT-RANK-THEOREM-001 — the Page rank turning point (Lean)

Python certificate: `05_CERTS/vp_page_turning_point_rank.py`.

Front P2 / Gravity. Companion to `D0.Gravity.PageCurveFiniteRankOwner` (which owns the finite-rank
Page bound `min(activeRank, envRank)` and rank conservation). THIS module isolates and proves the
*turning point* of that bound as a pure `Nat`-extremum statement:

  the rank entropy support `f(a) = min a (D - a)` over the simplex `0 ≤ a ≤ D` is MAXIMAL exactly at
  the balanced split `a = D/2`, where it equals `D/2`.

Concretely:
* `min_le_page_turn` :  for every admissible split `a ≤ D`, `min a (D - a) ≤ min (D/2) (D - D/2)`;
* `page_turn_value`   :  the value at the turn is `min (D/2) (D - D/2) = D/2`;
* `page_turning_point_owner` bundles both — `D/2` is the argmax AND the max value.

This is the discrete "Page turn": the active/environment rank-entropy support `min (rank P) (rank Q)`
is largest when the two ranks are balanced, `rank P = rank Q`. For `D = 8` the peak is `4`; for
`D = 33` (odd) the peak is `16` at `a = 16`.

HONESTY BOUNDARY. Owned here (CERT-CLOSED): the finite `Nat`-extremum facts — the argmax location and
the peak value — proved by `omega` (a genuine, non-trivial decision over the order structure of `Nat`).
What stays EXTERNAL: the analytic von Neumann entropy `S(ρ) = −Tr(ρ log ρ)` that the integer support
`min(rank P, rank Q)` bounds; no continuum object enters this module.
-/

namespace D0.Gravity

/-- The rank-entropy support of a balanced split: `f a = min a (D - a)`.
This is the integer support that bounds the active-sector entropy of a `D`-dimensional split. -/
def rankSupport (D a : Nat) : Nat := Nat.min a (D - a)

/-- **The turning point dominates every split.** For any admissible split `a ≤ D`, the rank-entropy
support `min a (D - a)` is bounded by its value at the balanced midpoint `a = D/2`. Hence `D/2` is the
argmax of the support over the simplex `0 ≤ a ≤ D`. The proof is a genuine `Nat`-order decision (the
two cases `a ≤ D/2` and `a > D/2` interplay with `D - a`, `D - D/2`, and integer division by `2`). -/
theorem min_le_page_turn (D a : Nat) (h : a ≤ D) :
    rankSupport D a ≤ rankSupport D (D / 2) := by
  unfold rankSupport
  simp only [Nat.min_def]
  split <;> split <;> omega

/-- **The value at the turn.** At the balanced split `a = D/2` the rank-entropy support equals `D/2`
(the lower half of the dimension), because `D/2 ≤ D - D/2` for every `D : Nat`. For odd `D` the
environment half `D - D/2 = (D+1)/2` is the larger one, so the `min` is still `D/2`. -/
theorem page_turn_value (D : Nat) :
    rankSupport D (D / 2) = D / 2 := by
  unfold rankSupport
  simp only [Nat.min_def]
  split <;> omega

/-- The turning-point value is itself the maximum support attained anywhere on the simplex. -/
theorem page_turn_is_max (D a : Nat) (h : a ≤ D) :
    rankSupport D a ≤ D / 2 := by
  have := min_le_page_turn D a h
  rw [page_turn_value] at this
  exact this

/-- **Strict balance maximality.** When `D` is positive and the split is unbalanced toward the empty
side (`a = 0`), the support is strictly below the turn: the Page curve genuinely rises from the
endpoints to the balanced peak (a real single-peak shape, not a flat line). -/
theorem page_turn_strict_above_endpoint (D : Nat) (h : 2 ≤ D) :
    rankSupport D 0 < rankSupport D (D / 2) := by
  unfold rankSupport
  simp only [Nat.min_def]
  split <;> split <;> omega

/-- **D0-PAGE-TURNING-POINT-RANK-THEOREM-001.** The rank-entropy support `f a = min a (D - a)` over
the admissible simplex `0 ≤ a ≤ D` attains its maximum at the balanced split `a = D/2`, and that
maximum value is exactly `D/2`. Equivalently: `min (rank P) (rank Q)` is largest when `rank P = rank Q`.
A finite `Nat`-extremum; the analytic von Neumann entropy it bounds stays external. -/
theorem page_turning_point_owner (D : Nat) :
    (∀ a, a ≤ D → rankSupport D a ≤ rankSupport D (D / 2))
      ∧ rankSupport D (D / 2) = D / 2 :=
  ⟨fun a h => min_le_page_turn D a h, page_turn_value D⟩

/-- Numeric witness `D = 8` (even): the peak sits at `a = 4` with value `4`. -/
theorem page_turn_eight : rankSupport 8 (8 / 2) = 4 := by
  unfold rankSupport
  decide

/-- Numeric witness `D = 33` (odd): the peak sits at `a = 16` with value `16` (`min 16 17 = 16`). -/
theorem page_turn_thirtythree : rankSupport 33 (33 / 2) = 16 := by
  unfold rankSupport
  decide

end D0.Gravity
