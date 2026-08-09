# CASCADE-FLOOR-DEFECT-CLOSURE — a NEW floor: defect ⇒ circulation needs closure (POST-SKEPTIC v2)

**Status:** POST-SKEPTIC v2 (2026-08-09). Skeptic #1: WOUNDED-FIXABLE, no kill; R1-R4 applied,
errors of record in the Repairs section. Pre-flight: no `ConjClasses` usage in D0/
(checked; the only in-tree conjugacy content is the toral GL(2,ℤ) conjugacy at
`ToralShiftEquivalence` and the Q₈ role-group class partition at `FactorBlockLaw` — both
different carriers, both pre-registered as non-bindings below); no DEFECT-CLOSURE row; the
prose step `defect ⇒ circulation needs closure` (§01.6.1c one-liner, verbatim) has NO floor in
the scaffold. Target: the umbrella `D0-CASCADE-INSUFFICIENCY-CHAIN-001` — now #2 of the
computed attack queue (value 55.7 after the second link) — whose missing floors the scaffold
names: "defect⇒closure⇒shell … remain unformalized".

## Claim X (DEF-0.2.2 form)

X (Lean `D0.Foundation.CascadeFloorDefectClosure`, clean axioms, standalone + D0.All GREEN):
the cascade step `defect ⇒ circulation needs closure` is carried as a genuine `CascadeStep`
(`stepDefectClosure`) plus the THIRD interlock link:

1. the defect is the commutator `[a,b] = a·b·a⁻¹·b⁻¹` — the exact element measuring the
   order floor's failure; on the abelian carrier it is identically 1
   (`abelian_defect_trivial`: nothing to measure — invariance below is vacuous,
   `abelian_invariance_is_vacuous`);
2. on the order-repair carrier (`S₃`, the scaffold's registered repair) defects exist
   (`defect_exists`) BUT the element-level defect fails the invariance obligation under the
   basepoint move = conjugation (`element_defect_not_invariant`, explicit witness, kernel
   `decide`);
3. the CLOSED reading — the conjugacy CLASS of the defect — is invariant, fully generically
   (`class_defect_invariant`); conjugacy classes of π₁ are exactly free-homotopy classes of
   CLOSED loops (standard correspondence, docstring-grade convention);
4. the floor is genuine (`defect_closure_floor_genuine` via the scaffold's own
   `step_discriminates`), and the third link holds
   (`chain_linked_order_to_defect_closure`): the order repair creates the object on which
   the next obligation is asked, fails its open form, and forces the closed one.

Grade claimed: a NEW FLOOR + LINK in the registered shape; the umbrella stays
OPEN/PROOF-TARGET (closure⇒shell and three-insufficiencies⇒three-zones still missing).

## Owned pre-facts (verbatim, file:line)

- §01.6.1c one-liner (0008__01.6:161): "… the torus is abelian, so order is not encoded
  `\Rightarrow` defect `\Rightarrow` circulation needs closure `\Rightarrow` shell …".
- Umbrella note: "floors defect=>closure=>shell and 'three insufficiencies = three zones'
  remain unformalized" (updated 2026-08-09; still true before this mint).
- `CascadeChain.lean:51-57`: the `CascadeStep` record (ObligationBelow/Above, insufficient,
  control) — the registered floor shape, instantiated here.
- `CascadeChain.lean` (chain-linked section): "The repair does not anticipate the next
  obligation; it creates the object on which the next obligation is asked, and fails it."
- `CascadeFloorOrderMemory.lean:63`: `control_orderEncoded : OrderEncoded (Equiv.Perm (Fin 3))`
  — the repair carrier this floor opens on (cited, not re-proved).
- §01.6.1c gloss list (0008__01.6:167): "**generations** = defect classes" — pre-registered
  NON-binding (ATT-C).

## The forcing / construction

New definition: `commDefect a b := a*b*a⁻¹*b⁻¹` (the standard commutator, named for the
floor). All proofs are kernel-level: `decide` on S₃ (order 6) for existence and the
invariance failure; generic conjugacy-class invariance via
`ConjClasses.mk_eq_mk_iff_isConj` + `isConj_iff` (witness `g⁻¹`, `group`); the abelian
degenerate by `simp`. Axioms propext/Classical.choice/Quot.sound on all exported theorems;
no `native_decide`. Lean: standalone 3030 jobs GREEN; D0.All GREEN. No python cert (kernel
arithmetic only; sibling-floor precedent).

## Named risks & PRE-REGISTERED attack surface (strongest first)

- **ATT-A (strongest: the obligations are about DIFFERENT objects).** SKEPTIC ADJUDICATED:
  SURVIVES via the stepComparison precedent (Below/Above are acceptor readings on ONE type)
  and via the descent framing — the Above obligation IS the statement that the datum
  descends to the QUOTIENT CARRIER ConjClasses (Equiv.Perm (Fin 3)), making the floor a
  genuine below-carrier (S3) / above-carrier (quotient) split. ERROR OF RECORD (R2,
  accepted): the draft defense quoted the CascadeChain docstring 'verbatim' with an inserted
  word ('/readings') — the actual text is 'recorded at both carriers — as the proposition it
  actually becomes there'. Repaired: true quote + descent framing in the module; restricted
  corollary class_defect_of_commutator_invariant added so the exact requirement is
  instantiated at the defect classes.
- **ATT-B (triviality: "conjugation moves elements" is classical).** Defense: same grade as
  the minted sibling floors (dyad-acceptor constancy; ℤ×ℤ abelianness); the content is the
  FLOOR (the prose step carried in the registered shape with a genuine
  insufficient/control pair) + the LINK, not the group theory. `step_discriminates` gives
  non-collapse for free from the record.
- **ATT-C (binding traps, two).** (i) "generations = defect classes" (prose gloss) — NOT
  bound; the floor makes no generation claim. (ii) The Q₈ role-group conjugacy-class
  partition (`FactorBlockLaw`, GAP-E) — different carrier; `ConjClasses` here is generic
  Mathlib machinery. Both stated in-module.
- **ATT-D (basepoint reading).** "Conjugation = the basepoint move" and "conjugacy classes
  of π₁ = closed loops" are standard-correspondence citations at docstring grade (the corpus
  convention used by TransportFieldNoGolden for eigenvalue↔root). The Lean content is the
  invariance split; the topological reading is the named convention. A kill must show the
  corpus already owns a DIFFERENT circulation-invariance reading that contradicts this one.
- **ATT-E (placement).** ERROR OF RECORD (R1, accepted; the repair STRENGTHENS the claim):
  the draft said the floor sits 'between order (5→6) and scale (6→7) in the PROSE' — FALSE
  (two owned texts: the 01.6.1c one-liner and the registered caveat at
  D0-CASCADE-INTERLOCK-SCALE-001). In the prose, the defect step is order-memory's IMMEDIATE
  successor (scale comes earlier) — the third link matches PROSE adjacency exactly. Still a
  floor + link package, not a renumbering.

## What this does NOT show

The closure⇒shell floor (the 2-cell/attachment layer); the three-zones terminal step; any
generation binding; any Q₈-role binding; any renumbering of the scaffold; the full cascade
theorem (umbrella stays PROOF-TARGET). What it adds: the first NEW floor since the scaffold
was minted, in the scaffold's own shape, with the third interlock link — the chain now runs
comparison → … → (4→5 → 5→6 link) → (5→6 → 6→7 link, scale) and (5→6 → defect-closure link),
with closure⇒shell as the next named missing floor.

## Repairs (errors of record, accepted in full)

- R1: prose-placement sentence was false; repaired — the defect step is order-memory's
  immediate prose successor, so the third link matches prose adjacency exactly (strengthens).
- R2: 'verbatim' quote had an inserted word ('/readings'); true quote restored; descent
  framing (below S3 / above ConjClasses S3) + restricted corollary added.
- R3: BOOK_03 reconciliation added — 03.23.4 'non-commutative holonomy' anchors the
  defect-datum reading; 03.23.5's outer-shell/global closure is the still-open
  closure=>shell half. Two named, non-competing closures.
- R4: no '(def)' marker in the theorem list; commDefect/stepDefectClosure named in the row
  note as load-bearing definitions.
- Advisories adopted: control-genericity honesty sentence; 'kernel decide' wording;
  simp-lint fix; classifier guardrails (row-635 safe formula).
