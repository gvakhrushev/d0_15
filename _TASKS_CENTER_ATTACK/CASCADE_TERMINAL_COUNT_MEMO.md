# CASCADE-TERMINAL-COUNT — the count leg of the terminal step, at proxy grade (POST-SKEPTIC v2)

**Status:** POST-SKEPTIC v2 (2026-08-09). Skeptic #1: MINT-AFTER-REPAIRS, 0 kills; NEW ROW
adjudicated (one-row-per-carried-leg precedent; different prose step than the shell floor);
R1-R4 applied, errors of record in the Repairs section. Pre-flight: the terminal step
`three insufficiencies = three zones` has THREE recorded dead routes — all three obituaries
read and differentiated (this campaign's mandatory first move): the propositional route caps
at two (`SceneCountRouteNoGo.propositional_route_caps_at_two`), the pair-indexed typing is
uninhabitable (`DiscriminationRetyping.zoneAssignment_is_uninhabitable`), the sort-indexed
route is circular (`DiscriminationKinds`: `Nonempty (ZoneAssignmentK S) ↔ 3 ≤ S.zoneCount`).
No prior count-from-closure content (`closed_superset` / orbit-cardinality route nowhere in
D0/). Target: umbrella `D0-CASCADE-INSUFFICIENCY-CHAIN-001` (value 58.0, #2 of the queue).

## Claim X (DEF-0.2.2 form)

X (Lean `D0.Foundation.CascadeTerminalCount`, clean axioms, standalone 3036 GREEN + D0.All
4475 GREEN): the COUNT leg of the terminal step is carried at the reflection-proxy grade of
`D0-CASCADE-FLOOR-SHELL-CLOSURE-001`, on the owned shell geometry, for EVERY admissible
parameter, by a route on a DIFFERENT CARRIER from all three dead ones:

1. the interior pair (defect layer + circulation core, §03.23.5's own identification) has
   exactly TWO elements (`interior_card_two`);
2. any reflection-closed superset of the interior pair MUST contain the outer radius
   (`closed_superset_contains_outer`) — the closure forces a third element;
3. the three-shell set is the LEAST reflection-closed completion
   (`three_shells_least_closed`; its own closedness owned at `shells_reflection_closed`);
4. the completion has EXACTLY THREE elements (`closure_card_three`) — ρ swaps inner↔outer
   and fixes the core, the orbit closes, no fourth element is generated;
5. the three-element carrier is the OWNED zone-attachment carrier — the carrier count is
   CITED, not new (R1): `D0-TORUS-CORE13-GEOMETRY-001` owns `torus_shell_card_eq_three`;
   zone sizes 9/11/13 ride the owned attachment (`carrier_card_three`).

Route-vs-obituaries, explicit: the count lives on SET CARDINALITY of radii in ℚ (not
propositions — obituary 1 does not apply); no `ZoneAssignment` occurs (obituary 2); the
least completion is EXHIBITED as the triple, PROVED least and closed, and its cardinality
is proved exactly 3 — no hypothesis of shape `3 <= _` occurs anywhere (obituary 3's
circularity does not apply; R3 wording). None of the three recorded dead ends (MODULES,
registered in the umbrella row's note — they have no rows of their own, R4) is re-attacked
or weakened; all three stand. TYPED SEAM NOT DISCHARGED (R2): SceneCountReduction's two
interpretation records (CascadeCountInterpretation, NoExtensionCountInterpretation) remain
unconstructed; the count lives on the radius/shell carrier, not SceneCandidate.zoneCount;
D0-SCENE-COUNT-REDUCTION-001 stays PROOF-TARGET.

## Owned pre-facts (verbatim, file:line)

- The three obituaries: `SceneCountRouteNoGo.lean:45,66` (`no_three_pairwise_inequivalent_
  props`, `propositional_route_caps_at_two`); `DiscriminationRetyping.lean:35-36`
  ("`ZoneAssignment` is **provably uninhabitable** for every finite scene");
  `DiscriminationKinds.lean:24` ("the hypothesis is *equivalent to the conclusion*").
- `D0-CASCADE-FLOOR-SHELL-CLOSURE-001` (minted this session): `shellReflection`,
  `shells_reflection_closed`, the reflection-proxy grade and its registered scope.
- `TorusShellAttachment.lean`: `torusShell_radius_strictMono` (distinctness),
  `torusShellEquivShell3`, `TorusShell.zoneSize` (9/11/13), `Fintype` derived on
  `TorusShell` (`TorusCore13GeometryOrigin.lean:63`).
- BOOK_03 §03.23.5 (FORCED): the two-interior-layer identification (defect + circulation),
  as carried by the shell floor's row.
- `D0-ZONE-COUNT-MULTIPLICATIVE-001` (minted this session): the zone-SIZES owner — cited as
  the separate owner of {9,11,13}; this module derives the COUNT only.

## The forcing / construction

All proofs are short and exact: cardinalities via `Finset.card_eq_two/three` with
distinctness from the owned strict monotonicity; the forcing step is one `ring` identity
(`ρ(inner) = outer`); minimality is a three-case membership argument; the carrier count is
kernel `decide` on the derived `Fintype`. Axioms propext/Classical.choice/Quot.sound on the
assembly and the least-closed theorem; no `native_decide`. No python cert (kernel content
only; sibling precedent).

## Named risks & PRE-REGISTERED attack surface (strongest first)

- **ATT-A (strongest: is this the terminal step at all?).** The prose says "three
  INSUFFICIENCIES = three zones"; this module counts LAYERS (two interior + one forced).
  Pre-registered defense: scope clause 3 in the module states the arithmetic carried is
  2 + 1 and does NOT re-interpret the prose enumeration — the identification of the prose's
  "three insufficiencies" with the three layers stays at prose grade, exactly like the shell
  floor's fourth link. The row must claim "the COUNT LEG at proxy grade", never "the
  terminal step closed". A kill must show the count leg itself is vacuous or circular.
- **ATT-B (proxy inheritance).** The route inherits the reflection-proxy grade of the shell
  floor (its registered scope: topological reading OPEN). The row must inherit that caveat
  verbatim. A different closure proxy could complete the pair differently (the shell floor's
  row already pre-empts the rival reflection); under the registered proxy the count is
  exactly 3.
- **ATT-C (does it secretly assume 3?).** The construction's inputs: two radii + one
  reflection. The number 3 appears only as the computed cardinality of the least completion.
  The zone sizes 9/11/13 are cited from owners, not derived, and play no role in the count.
  A kill must exhibit a hidden 3 in the inputs.
- **ATT-D (carrier mismatch with the zone carrier).** The count lives on radii in ℚ; the
  zone carrier is `TorusShell`/`Shell3`. The bridge is the OWNED attachment equivalence
  (`torusShellEquivShell3`) — cited, not constructed here. The row states: count on radii,
  attachment owned, sizes owned elsewhere.
- **ATT-E (obituary boundaries).** This route must not be readable as reviving any dead
  route. All three no-gos quantify over THEIR OWN carriers (propositions; `ZoneAssignment`;
  `ZoneAssignmentK`); nothing here inhabits or weakens them; the module docstring names all
  three and the differences. The three rows stay untouched.

## What this does NOT show

The terminal step as a whole (the insufficiencies↔layers identification stays at prose
grade); the zone sizes; the topological closure reading; the full chain assembly. What it
adds: the COUNT leg — the first machine-checked derivation of the number three from the
cascade's own closure structure, on a carrier none of the three dead routes used, with all
three obituaries standing.

## Repairs (errors of record, accepted in full)

- R1 (strongest, duplication): the draft re-proved Fintype.card TorusShell = 3 by decide —
  the theorem is OWNED at D0-TORUS-CORE13-GEOMETRY-001 (torus_shell_card_eq_three,
  TorusCore13GeometryOrigin.lean:65) and the corpus precedent is citation
  (DarkSectorCensus.dark_couplings_three). Repaired: carrier_card_three.1 now IS the owned
  theorem; the carrier count removed from every 'what is new' claim.
- R2 (named seam): SceneCountReduction's two unconstructed interpretation records now named
  in module scope, row note and umbrella update; D0-SCENE-COUNT-REDUCTION-001 stays
  PROOF-TARGET.
- R3 (wording): 'the number three is the OUTPUT' -> 'exhibited as the triple, proved least
  and closed; cardinality proved exactly 3'.
- R4: 'the three rows stay untouched' -> 'the three recorded dead ends (modules, registered
  in the umbrella row's note)'.
- Advisory adopted: DiscriminationKinds quote pin :23 -> :24; sibling boilerplate closer +
  token hygiene in the row note.
