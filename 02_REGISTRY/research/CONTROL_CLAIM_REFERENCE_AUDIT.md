# Claim-reference audit boundary — 2026-10-06

Repository: `gvakhrushev/d0_15`
CONTROL PR: #321
Audited registry: `bda840b12792178d183f209de047a9c3dfbfc026`
Status: source-name diagnostics, not a Lean elaboration or semantic proof audit.

## Distinct checks

`D0.All` compilation checks its actual imported declarations. `ClaimMap` has historically stored declaration names as strings. A successful build of that list does not resolve those strings in the Lean environment or check that an owner's proposition proves the registry's prose. PR #321 now exposes independent `leanStatus` and `releaseStatus` fields and prevents an open target from acquiring a closed summary status. It does not silently change scientific status to make a string reference pass.

A diagnostic inspection stripped comments, indexed ordinary namespace-qualified source declarations and followed `D0.*` imports. Direct owner declarations take precedence over imported names; imported suffix ambiguity is not evidence of a missing proof. This lexical inspection is deliberately not Lean's elaborator: generated declarations, notation and namespace aliases can require manual or kernel-level resolution.

## Names requiring owner reconciliation

The following twelve string references were not resolved by that source inspection. Their named modules do contain mathematical constructions, but substituting a nearby theorem would require checking the claim's exact intended scope. In particular a finite scaffold must not be relabeled a proof of its stronger physical interpretation. These are concrete metadata/ownership obligations, not a conclusion that twelve Lean proofs are false or absent.

| Claim | Proof status | Release status | Unresolved reference | Named module(s) |
|---|---|---|---|---|
| `D0-CVFT-001A` | `LEAN_PROVED` | `CORE-FORMALIZED` | `Cosmology.feedback_pressure_trace_log` | `D0.Dynamics.InternalFeedbackResolvent;D0.Cosmology.FeedbackPartitionFunction` |
| `D0-SEDENION-BRANCH-THREESET-SCAFFOLD-001` | `LEAN_PROVED` | `CORE-FORMALIZED` | `sedenion_branch_threeset_scaffold_owner` | `D0.Algebra.Sedenions` |
| `D0-TRIALITY-SEDENION-S3-DISJOINTNESS-GUARD-001` | `LEAN_PROVED` | `NO-GO` | `triality_sedenion_s3_disjointness_guard` | `D0.Algebra.Sedenions` |
| `D0-ARCHIVE-CUBICAL-COCHAIN-CARRIER-001` | `LEAN_PROVED` | `CORE-FORMALIZED` | `card_cubical_cochain_carrier` | `D0.Geometry.ArchiveCubicalCochainCarrier` |
| `D0-ARCHIVE-CUBICAL-COCHAIN-CARRIER-001` | `LEAN_PROVED` | `CORE-FORMALIZED` | `cubical_betti_sum_eq_sixteen` | `D0.Geometry.ArchiveCubicalCochainCarrier` |
| `D0-ARCHIVE-CUBICAL-COBOUNDARY-001` | `LEAN_PROVED` | `CORE-FORMALIZED` | `d_squared_eq_zero` | `D0.Geometry.ArchiveCubicalCoboundary` |
| `D0-ARCHIVE-1D-COCHAIN-REFINEMENT-001` | `LEAN_PROVED` | `CORE-FORMALIZED` | `b1_isometry` | `D0.Geometry.Archive1DCochainRefinement` |
| `D0-ARCHIVE-1D-COCHAIN-REFINEMENT-001` | `LEAN_PROVED` | `CORE-FORMALIZED` | `intertwining_d_b0_eq_b1_d` | `D0.Geometry.Archive1DCochainRefinement` |
| `D0-ARCHIVE-REFINEMENT-HODGE-WEIGHTS-001` | `LEAN_PROVED` | `CORE-FORMALIZED` | `hodge_mass_trace_sum` | `D0.Geometry.ArchiveRefinementHodgeWeights` |
| `D0-ARCHIVE-METRIC-MEASURE-HODGE-LIFT-001` | `LEAN_PROVED` | `FORMALISM` | `metric_measure_hodge_lift_owner` | `D0.Geometry.ArchiveMetricMeasureHodgeLift` |
| `D0-ARCHIVE-NAIVE-WEIGHTED-CAR-DEGREE-LEAKAGE-NOGO-001` | `LEAN_PROVED` | `NO-GO` | `archive_naive_weighted_degree_leakage_nogo_owner` | `D0.Geometry.ArchiveNaiveWeightedDegreeLeakageNoGo` |
| `D0-MATTER-LOCALIZATION-OBSERVABLE-CANONICITY-001` | `LEAN_PROVED` | `CORE-FORMALIZED` | `matter_neutrality_m1_forced` | `D0.Matter.MatterLocalizationNonuniquenessNoGo` |

## Reconciliation rule

For each entry, either identify the intended declaration by a fully qualified elaborated reference and review its actual proposition, or retain an explicitly unfulfilled ownership obligation. Correcting spelling is allowed only after that match; manufacturing a same-named trivial theorem or copying an unrelated owner is not. A proved intermediate construction and an open release target may legitimately coexist. The registry's claim IDs and scientific proof/release labels remain unchanged in PR #321.

This audit is retained in Git so that unresolved name binding is no longer an unspecified lost local task. The bounded README/status-generator cleanup is complete independently of this broader claim-to-proposition reconciliation. A future binding mechanism must cover imported declarations and registry entries naming definitions as well as theorems; a regex-only gate must not advertise kernel verification.
