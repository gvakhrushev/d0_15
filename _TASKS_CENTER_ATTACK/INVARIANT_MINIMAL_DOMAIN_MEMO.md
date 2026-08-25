# INVARIANT_MINIMAL_DOMAIN — v3, post-skeptic #24 and #25. **Grade: EDITORIAL.**

**Status:** DRAFT. **No registry row edited. Row 574 stays PROOF-TARGET.** No status word promoted.
**No theory defect was found.** The surviving deliverable is a documentation correction in a Lean
docstring plus a false label on one check in a prior cert. Graded EDITORIAL on skeptic #25's
recommendation, accepted without argument.

Target: `D0-P-INVARIANT-MINIMAL-001` (theory_status_map.csv:574).
Cert: `_TASKS_CENTER_ATTACK/invariant_minimal_domain_check.py` — 29/29 PASS, exit 0.

---

## Withdrawn across two adversarial passes (errors of record, no defence)

**v1 → skeptic #24 (WOUNDED-FIXABLE).** v1 claimed to *close* RR-1's universal by scanning "the
claim's own domain". Withdrawn: v1 equivocated between pointwise-fixed and Aut-stable invariance;
its trap-(n) accusation against `raise_selector_minimal_check.py` was wrong; its headline counts
were printed but never asserted (deleting the transitivity clause gave 64 partitions and still
exited 14/14 PASS); "three independent legs" was false; its negative control never re-ran the
conclusion.

**v2 → skeptic #25 (WOUNDED; significance KILLED).** v2's **X.3** claimed that under the
Aut-stable reading the extremality of `R^Aut` "survives ONLY as a unique-minimum-**dimension**
statement". **X.3 is false and is withdrawn.** All 8 separating Aut-stable partitions refine the
orbit partition (no block can span two zones, the zone degrees being distinct), so every
separating Aut-closed algebra *contains* `R^Aut`. Hence `R^Aut` is the unique **inclusion**-minimum
and the lattice **meet** — verbatim what row 574 asserts — under **both** readings. Independently
confirmed here: 8 separating partitions, 0 failing to refine.

Three live cert defects from that pass, all now repaired and each re-verified by mutation:
`is_pointwise` had an inert clause (deleting half of it left 26/26); dropping the zone-swap
generators went undetected, so the control scene ran against the wrong group; and `min_unique`
compared against the zone count as a **proxy** for `dim R^Aut`, which is why v2 mis-reported
K(9,9,13) as a firing negative control. Re-run against the real object, **the conclusion holds on
that scene too** — it is not a counterexample, and v2's claim that it was is retracted.

---

## What stands

**S1 (correct, minor).** On the frozen scene the two invariance notions give different domains:
**5** pointwise-invariant partitions versus **15** Aut-stable ones.

**S2 (correct).** The universal *"no invariant proper refinement exists"* is **TRUE** under the
pointwise reading (0 separating proper refinements) and **FALSE** under the Aut-stable reading,
with exactly **7** witnesses, block counts 11, 13, 15, 21, 23, 25, 33. Named witness:
`P₁₁ = {{0},…,{8}} ∪ {9…19} ∪ {20…32}` — Aut-stable, `deg` constant on every block, 11 blocks,
strictly refines the zone partition.

**S3 (the two bridges row 574 lists as "cited-not-formalized", discharged).**
*"gens generate Aut"*: adjacency(u,v) ⟺ zone(u)≠zone(v) over all 33² pairs, and the zone degrees
computed from adjacency are (24, 22, 20), pairwise distinct — so `Aut` is exactly the zone-wise
symmetric product. Brute-forced on `K(1,2,3)`: |Aut| = 12 = |S₁×S₂×S₃|.
*subalgebra↔partition*: for any field `K`, a unital `K`-subalgebra `A ⊆ K^V` is finite-dimensional,
commutative and reduced, hence Artinian and a product of field extensions of `K`; `1 ∈ A` makes
each `ev_v` surjective, so `ker ev_v` is maximal with residue field `K`; by CRT any **proper subset
of `Max(A)`** has nonzero intersection, while `⋂_v ker ev_v = 0`, forcing `{ker ev_v} = Max(A)`;
the primitive idempotents pull back to indicators of the fibres of `v ↦ ker ev_v`. *(Correction
carried from skeptic #25: v2 wrote this as "any proper subset of coordinate kernels has nonzero
intersection", which is false — `A = K·1 ⊆ K²` has `ker ev_1 = ker ev_2 = 0`. The statement is
about proper subsets of `Max(A)`; coordinate kernels may coincide, and their coinciding is
precisely what produces the blocks.)* Field-independent, and `n = 33` is not special.

---

## The surviving deliverable (EDITORIAL)

**E1 — `09_LEAN_FORMALIZATION/D0/Foundation/InvariantMinimal.lean:34-35`, verbatim:**

> "an Aut-closed algebra a fortiori satisfies the hypothesis, so the conclusion applies to
> every Aut-closed separating algebra"

The hypothesis is `hinv : ∀ g ∈ gens, ∀ x, c (g x) = c x` (`:148`) — **pointwise**. Aut-closure of
an *algebra* does not imply it. **Named second object:** `P₁₁` above. Its algebra is unital,
Aut-closed and `deg`-separating with dim 11 ≠ 3; its classifier violates `hinv` at
`(swap 0 1, x = 0)`, and the theorem's conclusion `c i = c j ↔ j ∈ orbit i` fails at `(i,j) = (0,1)`.
The same inference recurs at `:26-28` and `:142-144`.
**Scope:** the Lean *theorem* is untouched and correct — it carries `hinv` explicitly. Only the
docstring's informal extension to "every Aut-closed separating algebra" is wrong.

**E2 — `_TASKS_CENTER_ATTACK/raise_selector_minimal_check.py:253-255`.** The check is labelled
`"T3: unique Aut-closed algebra separating the owned observables = orbit partition"` and asserts
the count is 1. Under the pointwise reading that is right; under the Aut-**closed** reading its own
label invokes, the count is **8**. This corrects v2's over-retraction: the defect is not confined
to the `:241` comment, it reaches a check label. No numerical conclusion of that cert changes.

---

## Verification

`invariant_minimal_domain_check.py` — **29/29 PASS, exit 0.** Can-fail evidence is the mutation
battery, not a scene swap (there is no falsifying scene in this family; the statement is general):

| mutation | result |
|---|---|
| delete transitivity clause | FAIL C2 (64), C4 (19) — exit 1 |
| delete symmetry clause | FAIL C2 (171), C4 (49) — exit 1 |
| `separates` → `True` | FAIL C3, D2, D3, P1 — exit 1 |
| LEG B grid → `range(2)` | FAIL B1b (coverage n=5 stops at 4) — exit 1 |
| real scene → K(9,12,13) | FAIL C3 — exit 1 |
| **drop zone-swap generators** | **FAIL C0b, N2 — exit 1** (passed silently in v2) |

---

## Named risks

**(A)** E1/E2 are prose corrections. Neither touches a Lean statement, a registry status, a
theorem, or a number. Anyone grading this as bookkeeping rather than progress is right to.
**(B)** The asserted constants 15/8/5 are hardcoded expectations. They are justified by an
independent hand derivation (each zone whole-or-discrete ⇒ 2³ = 8 separating: 9+1+1 = 11,
1+11+1 = 13, 1+1+13 = 15, 9+11+1 = 21, 9+1+13 = 23, 1+11+13 = 25, 9+11+13 = 33; pointwise = Bell(3) = 5)
and were reproduced independently by skeptic #25 on five scenes. Still a fixture; press here.
**(C)** `leg_C`'s generator set is Aut by LEG A's *theorem*; `C0b` now catches a dropped swap but
does not prove the recipe correct in general.
**(D)** RR-2 (class-function universality, row-549 scope, EVIDENCE-grade) is **untouched**.
**(E)** LEG B proves subalgebra↔partition; the *equivariant* version (Aut-closed subalgebra ↔
Aut-stable partition) is used by S1/S2 but is not separately certified — skeptic #25's named gap,
recorded, not closed.

## What this does NOT show

Not a mint. No Lean module written. Does not close RR-1 — RR-1's universal is true in its own
pointwise reading and already Lean-owned. Does not impugn the prior cert's or the Lean lift's
numerical conclusions. Row 574's positive claims are **correct under both readings**. No physics.
