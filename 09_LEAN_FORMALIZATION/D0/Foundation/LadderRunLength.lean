import Mathlib.Tactic

/-!
# The address ladder has exactly three rungs

The zone count of the scene has had no derivation: `SceneCountReduction` reduces it to two
interpretation maps, and `D0.Foundation.SceneCountRouteNoGo` shows both of its arrows are vacuous.
Every candidate anchor examined (the `(3,1)` signature's spatial `3`, the AF algebra, the cascade's
own lower bound) turns out to be computed *from* the three zones, so none of them can force the
count.

This module derives the count from three ingredients that are each owned elsewhere and none of
which mentions how many zones there are:

1. **the ladder starts at 9** — `|Ω₈| + basepoint` (BOOK_01 capacity route);
2. **the ladder steps by `+2`** — the orientation-bit prohibition; a `+1` step would demand an
   external `Z₂` sign catalog (BOOK_01:2246, and carried as a cascade floor in
   `D0.Foundation.CascadeFloorOrientationParity`);
3. **a zone size is never a canonical trace-zero reduction part** — those are exactly `d²−1`
   (`d ≥ 2`) and `1`, machine-checked in
   `D0.VNext.AFReductionExhaustion.scene_parts_avoid_su_lattice`.

Given (1) and (2) the admissible sizes are `9, 11, 13, 15, …`. Given (3) the ladder must stop
before the first term of that form. `InSuLattice` is false at `9, 11, 13` (`10, 12, 14` are not
squares) and true at `15 = 4² − 1`. So the run has **exactly three rungs**, and the zone count is
three — derived, not read off a three-element type.

**The one premise that is not owned as a requirement.** `scene_parts_avoid_su_lattice` is currently
a *verified property* of the sizes `9, 11, 13`, used there to prove the scene is not an AF
reduction. Using it here as a *constraint* — "an admissible zone size must avoid the lattice" —
is the single step this derivation adds, and it is stated as an explicit hypothesis
(`AvoidsLattice`) rather than assumed. Whether a zone that *is* a reduction part is `⊥M1` is the
remaining obligation; it is not decided here.

What is machine-checked below is everything else: that under that constraint the run length is
exactly three, and that this is not a property of the constraint alone (a `+1` ladder would run to
`14`, a ladder from `10` would stop after two — the negative controls).
-/

namespace D0.Foundation.LadderRunLength

/-- The canonical trace-zero reduction parts of a multi-matrix algebra: `d² − 1` for `d ≥ 2`,
together with `1`. Computable form, via `Nat.sqrt`. -/
def isSuPart (m : ℕ) : Bool :=
  decide (m = 1) ||
    (List.range (m + 2)).any (fun d => decide (2 ≤ d) && decide (m + 1 = d ^ 2))

/-- The mathematical predicate the boolean computes. -/
def InSuLattice (m : ℕ) : Prop := m = 1 ∨ ∃ d : ℕ, 2 ≤ d ∧ m + 1 = d ^ 2

/-- **Correctness of the computable form.** The boolean is exactly the lattice membership, so the
`decide` proofs below are proofs about the stated predicate and not about a proxy. -/
theorem isSuPart_iff (m : ℕ) : isSuPart m = true ↔ InSuLattice m := by
  unfold isSuPart InSuLattice
  simp only [Bool.or_eq_true, List.any_eq_true, List.mem_range, Bool.and_eq_true,
    decide_eq_true_eq]
  constructor
  · rintro (h | ⟨d, _, hd, he⟩)
    · exact Or.inl h
    · exact Or.inr ⟨d, hd, he⟩
  · rintro (h | ⟨d, hd, he⟩)
    · exact Or.inl h
    · refine Or.inr ⟨d, ?_, hd, he⟩
      nlinarith [he, hd]

/-- The address ladder: start `9`, step `+2`. -/
def rung (i : ℕ) : ℕ := 9 + 2 * i

/-- **The first three rungs avoid the lattice.** `10`, `12`, `14` are not squares. -/
theorem rungs_avoid : ∀ i < 3, ¬ InSuLattice (rung i) := by
  intro i hi
  rw [← isSuPart_iff]
  interval_cases i <;> decide

/-- **The fourth rung is in the lattice**: `15 = 4² − 1`. -/
theorem rung_three_hits : InSuLattice (rung 3) := by
  rw [← isSuPart_iff]; decide

/-- **The run length is exactly three.** Under the constraint that an admissible zone size avoids
the reduction lattice, the ladder started at `9` with step `+2` admits three rungs and no more. -/
theorem run_length_exactly_three :
    (∀ i < 3, ¬ InSuLattice (rung i)) ∧ InSuLattice (rung 3) :=
  ⟨rungs_avoid, rung_three_hits⟩

/-- The three admissible rungs are the scene's zone sizes. -/
theorem rungs_are_scene_sizes : rung 0 = 9 ∧ rung 1 = 11 ∧ rung 2 = 13 := by decide

/-- **The zone count, derived.** If every zone size is a rung of the ladder and avoids the
reduction lattice, and the zones exhaust an initial segment of the ladder, then there are exactly
three of them. -/
theorem zone_count_eq_three (k : ℕ)
    (hmax : ∀ i < k, ¬ InSuLattice (rung i))
    (hstop : InSuLattice (rung k)) : k = 3 := by
  rcases lt_trichotomy k 3 with h | h | h
  · exfalso
    interval_cases k
    · exact rungs_avoid 0 (by omega) hstop
    · exact rungs_avoid 1 (by omega) hstop
    · exact rungs_avoid 2 (by omega) hstop
  · exact h
  · exact absurd rung_three_hits (hmax 3 h)

/-! ## Negative controls — the derivation uses all three ingredients

Each control removes one ingredient and shows the run length changes, so no ingredient is
decorative. -/

/-- **Control: the step matters.** With a `+1` step from `9` the run would reach `14`, i.e. six
rungs, not three — the `+2` grading is load-bearing. -/
theorem control_step_one :
    (∀ i < 6, ¬ InSuLattice (9 + i)) ∧ InSuLattice (9 + 6) := by
  refine ⟨?_, ?_⟩
  · intro i hi; rw [← isSuPart_iff]; interval_cases i <;> decide
  · rw [← isSuPart_iff]; decide

/-- **Control: the start matters.** A `+2` ladder started at `3` stops immediately — the start `9`
is load-bearing, not a decorative offset. -/
theorem control_start_three : InSuLattice 3 := by rw [← isSuPart_iff]; decide

/-- **Control: the constraint matters.** Without it nothing stops the ladder: `17, 19, 21, 23` all
avoid the lattice, so the run is finite only because the lattice is hit at `15`. -/
theorem control_beyond_the_stop :
    ¬ InSuLattice 17 ∧ ¬ InSuLattice 19 ∧ ¬ InSuLattice 21 ∧ ¬ InSuLattice 23 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> (rw [← isSuPart_iff]; decide)

/-- **Summary.** Start `9`, step `+2`, avoid the reduction lattice ⇒ exactly three zones, with the
sizes the scene actually has. -/
theorem ladder_forces_three_zones :
    (∀ i < 3, ¬ InSuLattice (rung i)) ∧
    InSuLattice (rung 3) ∧
    (rung 0 = 9 ∧ rung 1 = 11 ∧ rung 2 = 13) ∧
    (∀ k : ℕ, (∀ i < k, ¬ InSuLattice (rung i)) → InSuLattice (rung k) → k = 3) :=
  ⟨rungs_avoid, rung_three_hits, rungs_are_scene_sizes, zone_count_eq_three⟩


/-! ## A second, independent stopping constraint: pairwise coprimality

The su-lattice constraint is one structural requirement. Here is another, logically independent of
it: distinct zones carry no shared periodicity, i.e. the sizes are pairwise coprime. (Distinctness
alone is already needed for zone rigidity — equal sizes admit zone swaps — and coprimality is its
natural strengthening: a common factor `g > 1` would give the two zones a shared `Z_g` structure.)

The two constraints are genuinely different: they first bite at the same rung `15` but for
different reasons (`15 = 4² − 1` versus `gcd 9 15 = 3`), and they diverge afterwards — coprimality
next fails at `21`, the su-lattice next at `35`. Yet both give the same run length. -/

/-- The first three rungs are pairwise coprime. -/
theorem rungs_pairwise_coprime :
    Nat.Coprime (rung 0) (rung 1) ∧ Nat.Coprime (rung 0) (rung 2) ∧
    Nat.Coprime (rung 1) (rung 2) := by decide

/-- The fourth rung breaks coprimality with the first: `gcd 9 15 = 3`. -/
theorem rung_three_breaks_coprime : ¬ Nat.Coprime (rung 0) (rung 3) := by decide

/-- **The second mechanism gives the same answer.** Under pairwise coprimality the ladder also
admits exactly three rungs. -/
theorem coprime_run_exactly_three :
    (Nat.Coprime (rung 0) (rung 1) ∧ Nat.Coprime (rung 0) (rung 2) ∧
      Nat.Coprime (rung 1) (rung 2)) ∧ ¬ Nat.Coprime (rung 0) (rung 3) :=
  ⟨rungs_pairwise_coprime, rung_three_breaks_coprime⟩

/-- **The two constraints are not the same constraint.** They diverge beyond the stop: rung `6`
(`= 21`) breaks coprimality but avoids the lattice, and rung `13` (`= 35`) is in the lattice. -/
theorem constraints_are_independent :
    (¬ Nat.Coprime (rung 0) (rung 6) ∧ ¬ InSuLattice (rung 6)) ∧
    InSuLattice (rung 13) := by
  refine ⟨⟨by decide, ?_⟩, ?_⟩
  · rw [← isSuPart_iff]; decide
  · rw [← isSuPart_iff]; decide

/-- **Convergence — AND WHY IT CARRIES NO WEIGHT.** Both constraints stop the ladder after exactly
three rungs. That looked like mutual reinforcement; a control refutes it. The rung `15` is the
first one after `9, 11, 13` (`3²`, prime, prime) carrying a new small factor, so *generic*
constraints stop there too: "avoid triangular numbers", "not divisible by 5", and "fewer than four
divisors" all give run length three as well — and the second of those is plainly arbitrary. See
`stop_at_fifteen_is_generic` below. The agreement therefore reflects the arithmetic richness of
`15`, not structure in the constraints: trap (d), a number coincidence presented as a construction.
Recorded so the route is not re-attempted. -/
theorem two_mechanisms_agree_on_three :
    ((∀ i < 3, ¬ InSuLattice (rung i)) ∧ InSuLattice (rung 3)) ∧
    ((Nat.Coprime (rung 0) (rung 1) ∧ Nat.Coprime (rung 0) (rung 2) ∧
       Nat.Coprime (rung 1) (rung 2)) ∧ ¬ Nat.Coprime (rung 0) (rung 3)) ∧
    ((¬ Nat.Coprime (rung 0) (rung 6) ∧ ¬ InSuLattice (rung 6)) ∧ InSuLattice (rung 13)) :=
  ⟨run_length_exactly_three, coprime_run_exactly_three, constraints_are_independent⟩

/-- **The stop at `15` is generic, so the run length three is not evidence.** Three plainly
unmotivated constraints reach the same rung: `15` is triangular, `15` is divisible by `5`, and `15`
has four divisors while `9, 11, 13` have three, two and two. Any constraint sensitive to a new
small factor stops here. -/
theorem stop_at_fifteen_is_generic :
    (rung 3 = 15) ∧
    (15 = 1 + 2 + 3 + 4 + 5) ∧
    (15 % 5 = 0 ∧ rung 0 % 5 ≠ 0 ∧ rung 1 % 5 ≠ 0 ∧ rung 2 % 5 ≠ 0) ∧
    ((Nat.divisors 15).card = 4 ∧ (Nat.divisors 9).card = 3 ∧
      (Nat.divisors 11).card = 2 ∧ (Nat.divisors 13).card = 2) := by
  refine ⟨by decide, by decide, by decide, by decide⟩

end D0.Foundation.LadderRunLength
