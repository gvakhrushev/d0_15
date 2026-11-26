# Lean reference and statement audit

Snapshot: the sources and registry at `e96eb6a732f86203b4a921239334de82f99197a1`, checked on 26 November 2026. The three missing names in the two archive rows below have since been replaced by declarations that occur in their owning modules. Their statuses remain unchanged, and their registry notes describe the actual owner statements.

| Claim | Finding on checked source |
|---|---|
| `D0-ARCHIVE-1D-COCHAIN-REFINEMENT-001` | `b1_isometry` and `intertwining_d_b0_eq_b1_d` are absent from the owning module. `mass_trace_ne_edge_trace` and `archive_1d_cochain_refinement_owner` prove properties of two declared numeric trace constants. |
| `D0-ARCHIVE-REFINEMENT-HODGE-WEIGHTS-001` | `hodge_mass_trace_sum` is absent. `total_hodge_gram_trace_sum_eq` proves the numerical sum for a defined constant, while the owner packages selected numeric values and a cardinality. |
| `D0-SEDENION-BRANCH-THREESET-SCAFFOLD-001` | The recorded `sedenion_branch_threeset_scaffold_owner` was not found in the declared module. The module does contain `branch_label_s3_scaffold`; its statement needs a deliberate comparison before changing the metadata. |
| `D0-TRIALITY-SEDENION-S3-DISJOINTNESS-GUARD-001` | The recorded `triality_sedenion_s3_disjointness_guard` was not found in the declared module. `bare_threeset_insufficient_for_sedenion_realization` proves a specific finite ambiguity. Its relationship to a triality intertwiner requires separate verification. |
| `D0-ARCHIVE-CUBICAL-COCHAIN-CARRIER-001` | `card_cubical_cochain_carrier` and `cubical_betti_sum_eq_sixteen` were not found in the declared module. The module has `total_betti_sum` and `archive_cubical_cochain_carrier_owner`; compare their statements and imports before replacing metadata. |
| `D0-ARCHIVE-CUBICAL-COBOUNDARY-001` | `d_squared_eq_zero` was not found in the declared module. The named owner proves a count, a cardinality and a proposition applied to `true`; its statement does not construct the differential in the module prose. |
| `D0-ARCHIVE-METRIC-MEASURE-HODGE-LIFT-001` | `metric_measure_hodge_lift_owner` was not found in the declared module. `archive_metric_measure_hodge_lift_owner` exists and its exact statement should be compared with the registry before repair. |
| `D0-ARCHIVE-NAIVE-WEIGHTED-CAR-DEGREE-LEAKAGE-NOGO-001` | `archive_naive_weighted_degree_leakage_nogo_owner` was not found. The module contains `archive_naive_weighted_car_degree_leakage_nogo_owner`; its statement must be checked before inferring the full prose claim. |
| `D0-MATTER-LOCALIZATION-OBSERVABLE-CANONICITY-001` | `matter_neutrality_m1_forced` was not found in the declared module. The other recorded owner exists; its exact assumptions and conclusion require separate comparison. |

The scan looks for declaration names in source text. Imported declarations, generated names and namespaces require Lean elaboration for a conclusive global audit. This list does not change claim statuses or decide unexamined mathematical statements. [Archive certificate review](ARCHIVE_CERTIFICATE_REVIEW.md)
