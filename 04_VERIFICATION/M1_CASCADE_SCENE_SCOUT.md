# M1 cascade to variable scene — adversarial scout

**Verdict: `NO-GO-CLOSABLE`.**

## Frozen boundary

- `D0.Foundation.SceneCountReduction.exact_zone_count_of_interpretations` is an honest
  reduction: it proves `zoneCount = 3` from embeddings in both directions.
- `D0.Foundation.SceneCountRouteNoGo.reduction_is_bare_arithmetic` proves that the two
  current interpretation records are equivalent to `3 ≤ zoneCount` and
  `zoneCount ≤ 3`; their theorem antecedents can be discarded.
- `D0.Foundation.CascadeCarriedAssembly.cascade_carried_assembly` already carries six
  genuine ordered floors, four interlocks, the terminal count leg and the separate
  orientation-parity floor. This scout does not reopen or downgrade those results.
- `D0.Foundation.ZoneCountFromRank.zoneCount_le_three_of_rank_le_three` is a genuine
  variable-scene upper theorem, but no present owner derives `rank ≤ 3` for the
  variable scene. The frozen `K(9,11,13)` rank is not transferable.
- `D0.Synthesis.ConcretePhysicalDetectorRepresentation` already closes the two-sided
  class-M1 detector representation on `Observation`; singleton/class admissibility is
  not a blocker here.

## Countermodel tests

| proposed bridge | `zoneCount = 2` | `zoneCount = 4` | verdict |
|---|---:|---:|---|
| current cascade and no-extension owner propositions | preserved | preserved | no scene argument occurs in either proposition |
| current interpretation records | upper record exists | lower record exists | each record is only its target embedding |
| proposition-valued floor classes | at most two classes | at most two classes | cannot produce the lower three-class carrier |
| pair-indexed `Discrimination` assignment | impossible | impossible | infinitely many `trivialDisc n`; hypothesis is empty |
| `DatumKind` assignment | impossible | possible | `Nonempty (ZoneAssignmentK S)` is exactly the lower cardinal bound |
| variable complete-multipartite rank | compatible only when rank is actually small | four surjective zones force rank at least four | useful invariant, but present grammar supplies no variable-scene rank cap |
| ladder stop at 15 | unaffected | unaffected | stop predicate is an imported selector, not an M1 consequence |

The decisive model is stronger than either isolated control: the complete present package
(carried cascade, the three computed datum kinds, concrete class-M1 detector representation,
and the existing no-extension owner proposition) is independent of `SceneCandidate.zoneCount`.
It therefore has models at both two and four zones. No theorem in the current grammar can
determine any unique zone count without adding a relation between semantic repair classes and
variable zones.

## Killed routes

1. **Owner-fact arrow route:** killed by
   `cascade_interpretation_arrow_vacuous`,
   `noextension_interpretation_arrow_vacuous` and
   `reduction_is_bare_arithmetic`.
2. **Proposition quotient:** killed by
   `no_three_pairwise_inequivalent_props`.
3. **Designated-pair quotient:** killed by
   `zoneAssignment_is_uninhabitable`.
4. **Three-constructor kind quotient as selector:** killed because its zone assignment is
   equivalent to the desired lower bound; it is a renamed embedding, not a derivation.
5. **Frozen-rank transfer:** killed by the dependence of the frozen adjacency on the already
   selected three-zone scene.
6. **Arithmetic stop filter:** killed by the multiple independent first-failure predicates
   at 15 in `LadderRunLength`.

## Closable no-go and exact reopening contract

The closable result is a formal count-parametric countermodel: all present M1/cascade facts
survive at arbitrary positive `zoneCount`, including explicit two- and four-zone instances.

The single constructive reopening owner is:

> construct an independently derived quotient `Q` of mandatory, outcome-affecting,
> non-protocol insufficiency repairs by observational equivalence, and a faithful
> representation `Q ≃ Fin S.zoneCount`; prove the quotient/exhaustion theorem by the M1
> reductio, not by declaring three constructors or a cardinal bound.

This one representation theorem must simultaneously make the cascade-to-zone map
non-vacuous and make a fourth zone produce a mandatory external catalogue. Until it exists,
`D0-SCENE-COUNT-REDUCTION-001` and
`D0-CASCADE-INSUFFICIENCY-CHAIN-001` remain `PROOF-TARGET`.
