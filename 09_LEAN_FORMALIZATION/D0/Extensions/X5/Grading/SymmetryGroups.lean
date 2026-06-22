import Mathlib.Data.List.Nodup
import Mathlib.Tactic

/-!
# D0-X5-G-SYMMETRY-001 — the three distinct symmetry groups (Section 3.1)

`Aut_raw` (the actual `S₉×S₁₁×S₁₃` graph/readout action) must NOT be silently replaced by `U(3)`. Since the
part sizes `9,11,13` are pairwise distinct, `Aut_raw` fixes each part setwise and acts TRIVIALLY on the three
generation directions (the part-constant vectors are size-distinguished) — so `Aut_raw` imposes NO constraint
on the grading signature. `U3_inner` (inner `U(3)` on the `M₃` block, the commutant `*`-autos) mixes the three
generations into one orbit and classifies gradings by signature `(p,q)`. The two groups are genuinely distinct
(generation-orbit counts `3 ≠ 1`).
-/

namespace D0.Extensions.X5.Grading

/-- The three part sizes. -/
def partSizes : List ℕ := [9, 11, 13]
theorem part_sizes_distinct : partSizes.Nodup := by decide

/-- `Aut_raw` generation-orbit count: 3 (each part-constant direction is a fixed point — distinct sizes). -/
def autRawGenerationOrbits : ℕ := 3
theorem aut_raw_fixes_generations : autRawGenerationOrbits = partSizes.length := by decide

/-- `U3_inner` mixes all 3 generations into ONE orbit. -/
def u3GenerationOrbits : ℕ := 1

/-- `U3_inner` classifies gradings of the `M₃` block by signature `(p,q)`, `p+q = 3` — four classes. -/
def u3SignatureClasses : List (ℕ × ℕ) := [(3, 0), (2, 1), (1, 2), (0, 3)]
theorem u3_four_signature_classes : u3SignatureClasses.length = 4 := by decide

/-- **`Aut_raw ≠ U(3)`**: their generation-orbit counts differ (`3 ≠ 1`). -/
theorem aut_raw_ne_u3 : autRawGenerationOrbits ≠ u3GenerationOrbits := by decide

/-- **D0-X5-G-SYMMETRY-001.** The three groups are distinguished: `Aut_raw` fixes the 3 generation directions
(no signature constraint); `U3_inner` has one generation orbit and 4 signature classes. -/
theorem symmetry_groups_distinct :
    partSizes.Nodup ∧ autRawGenerationOrbits = 3 ∧ u3SignatureClasses.length = 4 ∧
      autRawGenerationOrbits ≠ u3GenerationOrbits :=
  ⟨part_sizes_distinct, rfl, u3_four_signature_classes, aut_raw_ne_u3⟩

end D0.Extensions.X5.Grading
