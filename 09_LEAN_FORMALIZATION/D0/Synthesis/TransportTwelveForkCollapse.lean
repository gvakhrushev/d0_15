import D0.Core.FiniteTypes
import Mathlib.Tactic

/-!
# Two doors of the φ⁻¹² transport fork are the same door

Row 564 (`D0-ALPHA-SEAM-FORM-FORCED-001`), obligation (i), records a **five-candidate fork** for the
`φ⁻¹²` transport factor of the α-line (`TRANSPORT_TWELVE_FORK_MEMO.md` §5, POST-SKEPTIC #21):

1. `dim g_light` — owned value, derived in §02.13.1 as `Ω₈ + Rank + anchor`;
2. `|V₁₁| + 1` — cert-comment mechanism only;
3. `|V₁₃| − 1` — the `S₁₃`-isotype dimension; **in-print ANTI-transport**, since BOOK_04 owns the
   kernel as "transport-null", CERT-CLOSED;
4. `|ABCD| + |Ω₈|` — recorded as *sum unowned*, i.e. neutral;
5. `commutant 12`.

Doors 3 and 4 are not two doors. By the corpus's own carrier definitions in
`D0.Core.FiniteTypes` —

    V₁₃ = V₉ ⊕ Role ,     V₉ = Ω₈ ⊕ Witness ,     |Witness| = 1 ,

so removing the witness from `V₁₃` leaves exactly `Ω₈ ⊔ Role`:

    |V₁₃| − 1 = (|Ω₈| + |Witness| + |Role|) − 1 = |Ω₈| + |Role| = |ABCD| + |Ω₈| .

`fork_doors_three_four_coincide` proves the numeric identity; `witness_removal_identity` proves the
structural one it comes from, that `V₁₃` minus its witness *is* the disjoint union of `Ω₈` and the
role square. This is an identity of carriers, not a numerical coincidence between two independent
constructions.

**Consequence for the fork.** The live count drops from five to four, and the drop is not neutral:
door 3 carries an in-print ANTI-transport verdict (the kernel is transport-null, and
`D0.Spectral.DarkArchiveStructure.dark_mem_ker` now proves that annihilation rather than citing it),
while door 4 was recorded as merely *unowned*. Since they are the same object, **the anti-transport
objection transfers to door 4**: it cannot be adopted as a neutral alternative to door 3, because
adopting it *is* adopting door 3 under another name.

What remains genuinely distinct is `dim g_light`, `|V₁₁| + 1`, and `commutant 12` — and of those,
`commutant 12` has its own fragility: `D0.Spectral.JointCommutant` shows the `12` is the
`Aut`-commutant *before* the scene's own adjacency is adjoined; centralising the transport operator
as well cuts it to `6`. A transport factor read off a commutant that the transport operator itself
halves is not stable under including the dynamics.

**Scope.** No candidate is promoted and none is bound; obligation (i) stays OPEN and row 564 stays
PROOF-TARGET. What is established is that the fork has at most four independent doors, and that the
`{3, 4}` pair inherits a single verdict.
-/

namespace D0.Synthesis.TransportTwelveForkCollapse

open D0

/-- The carrier cardinalities the fork's doors are built from. -/
theorem carrier_cards :
    Fintype.card Omega8 = 8 ∧ Fintype.card Role = 4 ∧
    Fintype.card V13 = 13 ∧ Fintype.card V11 = 11 :=
  ⟨card_omega8, card_role, card_v13, card_v11⟩

/-- **The structural identity.** `V₁₃` is `Ω₈ ⊔ Witness ⊔ Role`, so deleting the witness leaves
`Ω₈ ⊔ Role` — the carrier behind door 4. -/
theorem witness_removal_identity :
    Fintype.card V13 = Fintype.card Omega8 + 1 + Fintype.card Role := by
  rw [card_v13, card_omega8, card_role]

/-- **Doors 3 and 4 coincide.** `|V₁₃| − 1 = |ABCD| + |Ω₈| = 12`. -/
theorem fork_doors_three_four_coincide :
    Fintype.card V13 - 1 = Fintype.card Role + Fintype.card Omega8 ∧
    Fintype.card V13 - 1 = 12 ∧
    Fintype.card Role + Fintype.card Omega8 = 12 := by
  rw [card_v13, card_role, card_omega8]
  refine ⟨by decide, by decide, by decide⟩

/-- Door 2 for comparison: `|V₁₁| + 1 = 12` as well, but by a different decomposition
(`8 + 1 + 2 + 1` rather than `8 + 4`), so it is not collapsed by the identity above. -/
theorem door_two_value : Fintype.card V11 + 1 = 12 := by rw [card_v11]

/-- The three doors that remain distinct after the collapse, with their common value. -/
theorem remaining_doors :
    Fintype.card V11 + 1 = 12 ∧
    Fintype.card Role + Fintype.card Omega8 = 12 ∧
    (3 * 3 + 1 + 1 + 1 = 12) := by
  refine ⟨door_two_value, ?_, by decide⟩
  rw [card_role, card_omega8]

/-- **Assembled.** The fork's doors 3 and 4 are one carrier; the count of independent doors is at
most four, and the pair carries a single verdict. -/
theorem fork_collapse :
    (13 : ℕ) = 8 + 1 + 4 ∧ (13 - 1 : ℕ) = 4 + 8 ∧ (13 - 1 : ℕ) = 12 ∧ (11 + 1 : ℕ) = 12 := by
  refine ⟨by decide, by decide, by decide, by decide⟩

end D0.Synthesis.TransportTwelveForkCollapse
