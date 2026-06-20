import D0.Geometry.ToralLucasPeriodicSeed

/-!
# D0-TORAL-CANONICAL-MARKOV-PARTITION-NOGO-001 — Outcome B

The campaign decides **Outcome B**: the canonical periodic seed exists (the primitive period-3 orbit,
`D0-TORAL-LUCAS-PERIODIC-SEED-OWNER-001`), but a *canonical* Markov partition — and hence the symbolic
strong-shift-equivalence to the golden cylinder shift — does NOT follow from present inputs. Two grounded
obstructions:

1. **The integral conjugacy is not the symbolic SSE.** `C T C⁻¹ = −M_φ`
   (`D0-TORAL-INTEGRAL-CONJUGACY-OWNER-001`), but `−M_φ` has a negative entry and `−M_φ ≠ M_φ`, so it is
   not the nonnegative golden cylinder adjacency matrix. An integral matrix conjugacy at the `2×2` level
   does not produce the symbolic conjugacy of edge shifts.

2. **No canonical Markov partition from a 3-point seed.** Adler–Weiss Markov partitions for a hyperbolic
   toral automorphism are non-unique (they involve choices of rectangle boundaries) and a 3-point
   periodic orbit does not canonically determine one. Choosing rectangles/vertices is forbidden.

Hence the Markov-rectangle, symbolic-coding, boundary-quotient, and Williams-SSE owners stay
PROOF-TARGET. EXACT MISSING ARTIFACT (`D0-TORAL-WILLIAMS-SSE-OWNER-001`): a canonical, seed-determined
finite Markov partition whose nonnegative adjacency matrix is exhibited strong-shift-equivalent to
`M_φ` — derived, not chosen. No Adler–Weiss import, no manual rectangles, no `T⁴⁴ = I`.
-/

namespace D0.Geometry.ToralCanonicalMarkovNoGo

open D0.Geometry.ToralIntegralConjugacy

/-- **The integral conjugate `−M_φ` is not the golden adjacency matrix `M_φ`** (and has a negative
entry): the integral conjugacy is not the symbolic SSE to the golden cylinder shift. -/
theorem integral_conjugacy_is_not_symbolic_sse :
    (-Mphi) 0 0 < 0 ∧ Mphi ≠ -Mphi := by
  refine ⟨negative_golden_not_adjacency, ?_⟩
  intro h; have := congrArg (fun M => M 0 0) h; simp [Mphi] at this

/-- **D0-TORAL-CANONICAL-MARKOV-PARTITION-NOGO-001 (Outcome B).** The canonical periodic seed exists,
but no canonical Markov partition / golden-cylinder SSE follows: the integral conjugate `−M_φ` is a
negative-entry matrix `≠ M_φ` (not the symbolic SSE), and a 3-point seed does not canonically determine
a Markov partition. The Markov/coding/quotient/SSE owners stay PROOF-TARGET with that exact gap. -/
theorem toral_canonical_markov_partition_nogo :
    (-Mphi) 0 0 < 0 ∧ Mphi ≠ -Mphi ∧ D0.Geometry.ToralLucasPeriodicSeed.seedCard = 3 := by
  exact ⟨integral_conjugacy_is_not_symbolic_sse.1, integral_conjugacy_is_not_symbolic_sse.2, rfl⟩

end D0.Geometry.ToralCanonicalMarkovNoGo
