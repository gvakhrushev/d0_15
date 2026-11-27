# Lean reference and statement audit

Snapshot: the sources and registry at `e96eb6a732f86203b4a921239334de82f99197a1`, checked on 26 November 2026. Seven claim rows have since had their missing references replaced with declarations that occur in their owning modules, with notes scoped to their actual statements. Their statuses remain unchanged. The triality and weighted-leakage NO-GO rows still need statement-level reconciliation.

| Claim | Finding on checked source |
|---|---|
| `D0-ARCHIVE-1D-COCHAIN-REFINEMENT-001` | `b1_isometry` and `intertwining_d_b0_eq_b1_d` are absent from the owning module. `mass_trace_ne_edge_trace` and `archive_1d_cochain_refinement_owner` prove properties of two declared numeric trace constants. |
| `D0-ARCHIVE-REFINEMENT-HODGE-WEIGHTS-001` | `hodge_mass_trace_sum` is absent. `total_hodge_gram_trace_sum_eq` proves the numerical sum for a defined constant, while the owner packages selected numeric values and a cardinality. |
| `D0-SEDENION-BRANCH-THREESET-SCAFFOLD-001` | The recorded `sedenion_branch_threeset_scaffold_owner` was not found in the declared module. It has been replaced by `branch_label_s3_scaffold`, with the scope of its finite label theorem stated in the registry. |
| `D0-TRIALITY-SEDENION-S3-DISJOINTNESS-GUARD-001` | The recorded `triality_sedenion_s3_disjointness_guard` was not found in the declared module. `bare_threeset_insufficient_for_sedenion_realization` proves a specific finite ambiguity. Its relationship to a triality intertwiner requires separate verification. |
| `D0-ARCHIVE-CUBICAL-COCHAIN-CARRIER-001` | `card_cubical_cochain_carrier` and `cubical_betti_sum_eq_sixteen` were not found in the declared module. The registry now names `total_betti_sum` and `archive_cubical_cochain_carrier_owner`, with the limits of their statements recorded. |
| `D0-ARCHIVE-CUBICAL-COBOUNDARY-001` | `d_squared_eq_zero` was not found in the declared module and was removed from the references. The retained owner proves a count, a cardinality and a proposition applied to `true`; its statement does not construct the differential in the module prose. |
| `D0-ARCHIVE-METRIC-MEASURE-HODGE-LIFT-001` | `metric_measure_hodge_lift_owner` was not found in the declared module. The registry now names `archive_metric_measure_hodge_lift_owner`, consistent with the previously recorded scope. |
| `D0-ARCHIVE-NAIVE-WEIGHTED-CAR-DEGREE-LEAKAGE-NOGO-001` | `archive_naive_weighted_degree_leakage_nogo_owner` was not found. The module contains `archive_naive_weighted_car_degree_leakage_nogo_owner`; its statement must be checked before inferring the full prose claim. |
| `D0-MATTER-LOCALIZATION-OBSERVABLE-CANONICITY-001` | `matter_neutrality_m1_forced` was not found and was removed from the references. The retained owner proves a constant total readout on a class whose definition already assumes a zero source sum. |

The eight names identified after the first two row repairs were also checked
with Lean 4.30.0 after importing their declared modules and using their source
namespaces. Lean reported each checked qualified identifier as unknown. The
source files matched the locally compiled module inputs. Subsequent repairs
cover six of those names across five rows. The remaining two names concern the
triality and weighted-leakage NO-GO rows, where the available finite statements
do not establish the original full descriptions. Claim statuses are
unchanged. [Archive certificate review](ARCHIVE_CERTIFICATE_REVIEW.md)

A [finite weighted-differential witness](research/sources/d0_weighted_leakage_2026_11_27/RESULT_RU.md)
now proves a concrete non-nilpotent example and an unweighted control.
It does not prove the full weighted-leakage description or resolve the
missing registry reference.

A [finite S3 action comparison](research/sources/d0_s3_action_comparison_2026_11_27/RESULT_RU.md)
shows that two actions of the same six-element group can have no injective
intertwiner. It does not construct Spin(8) triality or the sedenion action,
and the original triality reference remains unresolved.

`python tools/audit_lean_claim_references.py` scans registry names against
source declarations with comments and strings excluded. CI checks that the
documented unresolved set does not grow or silently change. The optional
`--strict` mode exits with a failure while any unresolved reference remains.
Both modes report the unresolved names. A textual match is a screening result,
not a check of namespace, theorem type, or proof.
