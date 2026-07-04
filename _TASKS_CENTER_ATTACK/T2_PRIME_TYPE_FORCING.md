# T2′ TYPE-KEYED MATCHING — the forcing in DEF-0.2.2 form (DRAFT, submitted to skeptic)

**Author:** chief researcher. Status: DRAFT forcing argument; no registry row edited. This document
discharges obligation 1 of `T2_PRIME_SCENE_HALF_MEMO.md`. The two blades used are the corpus's own
two Q₈-forcing blades (§01.7.1A), run in reverse.

## Claim X

The identification between the scene generation triple {innerD9, coreD11, outerD13} (definitionally
= `GenerationPhasonMode`, radially ordered, zone-labeled) and the Q₈ Fourier triple {E₀, E₄, E₃} is
unique: `9 ↔ E₀`, `11 ↔ E₄`, `13 ↔ E₃`.

## Owned pre-facts (cited, not re-derived)

- **P1.** `V₉ = Ω₈ ⊔ {ω₀}` — zone 9 is the unique zone hosting the terminal role cycle
  (BOOK_01 §01.8/§01.20, THE).
- **P2.** Three zones ↔ three structural necessities {defect/base, memory, shell}; the zone
  assignments: 9 = defect/base (by P1), 11 = memory (the torus; torus = memory of two loops, §00.8
  worked forcing; "memory zone (the torus, address 11)" BOOK_04 §04.8), 13 = terminal shell
  (BOOK_00 §00.8 line "Why stop at 13?").
- **P3.** Block signatures, verified in exact arithmetic (`w8_holomorph_check.py`, 14 PASS):
  - E₀ — the unique block fixed by both holomorph actions (trivial isotype; unramified);
  - E₄ — the unique block on which `L₋₁ = −1`, i.e. on which the **order-memory register**
    `[Q₈,Q₈] = Z(Q₈) = {±1}` (§01.7.1B) acts nontrivially; on E₀⊕E₃ the group acts through its
    abelianization (`L₋₁ = +1`) and order information is structurally invisible;
  - E₃ — the triple of characters with kernels `⟨i⟩,⟨j⟩,⟨k⟩ = ⟨B⟩,⟨C⟩,⟨D⟩` under the **forced role
    dictionary** `A↦1, B↦i, C↦j, D↦k` (§01.7.1A, THEOREM) — the terminal-role-indexed triple.

## The forcing (DEF-0.2.2 instantiation)

Assume ¬X: some matching m′ differs from the type-keyed m. Since a bijection of 3-sets is fixed by
two values, m′ must displace the memory leg or the base leg (or both).

**(i) Displacing the memory leg (11 ↛ E₄).** Then the memory zone maps to E₀ or E₃ — blocks on which
the group acts abelianly (P3: `L₋₁ = +1`), where **loop order is structurally not encoded**. The
memory necessity of zone 11 (P2) is exactly the obligation to encode order ("a torus is abelian ⇒
loop order is not encoded ⇒ defect", §00.8; "order memory forbids commutativity", §01.7.1A blade 2).
Under m′ that obligation must be carried by an additional structure θ — an external order register
attached to an abelian block. θ affects distinguishable outcomes (order-resolved vs order-blind
readouts differ), is not derivable from prior DEF/THE (the block's own algebra cannot supply it),
and is not part of the distinguishability protocol: θ is exogenous (DEF 0.3.1), ⊥M1.

**(ii) Displacing the base leg (9 ↛ E₀).** Then the role-hosting zone (P1) maps to a nontrivial
block (E₄ or E₃), on which the role group acts with distinctions; registering zone 9's *base*
function there requires distinguishing role-copies inside a block that conjugation moves — a
conjugate catalog, which is §01.7.1A blade 1 ("normality is forbiddance of a conjugate catalog"),
⊥M1. Meanwhile E₀ — the unique block blind to all role distinctions — would be attached to a zone
whose necessity (memory or shell) demands registering distinctions, reproducing (i)'s θ on the other
side.

**(iii) Third leg by elimination.** With 9 ↔ E₀ and 11 ↔ E₄ forced, `13 ↔ E₃` follows for any
bijection; no rule and no catalog is consumed. (Independently welded by P3: the E₃ triple is
role-indexed `{B,C,D}` and zone 13 is the terminal-role shell — but the forcing does not need this
extra weld; it is a consistency check, not a load-bearing step.)

Hence ¬X is impossible and X is forced. ∎ (draft, pending skeptic)

## What this argument does and does not use

- It does NOT use mass values, Lucas rows, or radial order-matching; THE 04.8.L.1's localization
  premise is corroborating (P2 citation), not load-bearing — the load is carried by the
  order-memory/abelian-block obstruction (i), which is computational (P3) plus the §00.8/§01.7.1A
  forcings.
- It reuses the two blades that forced Q₈ itself; no new principle enters.
- Scope: the argument forces the matching GIVEN the owned typings P1–P3. It does not (and need not)
  force the typings — they are cited owners.

## Effect if the skeptic passes it

P_iso fully paid (Q₈-internal half: holomorph module; scene half: definitional shells; matching:
this forcing) ⇒ the postulated content of `D0-X5-LEPTON-CONTRACT-001` is ∅ ⇒ re-scope per
`TASK_W6_REPORT.md` §(e) inventory becomes actionable under the closure protocol (scout → owner →
negative controls → gate), including the prose owners that currently say "genuinely external".
