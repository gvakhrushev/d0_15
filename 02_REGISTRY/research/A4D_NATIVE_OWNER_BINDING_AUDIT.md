# Twelve declaration diagnostics: kernel binding and proposition reconciliation

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Source head: `af221e2fed92821c52afc88a5500774de8cd9a93`.
Registry/control baseline: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Status: **compiled diagnostic and semantic assessment**; no registry or
Lean-owner edits. Closure of the stronger scientific obligations is not
inferred from a successful compilation.

This extends the earlier lexical
[CONTROL audit](CONTROL_CLAIM_REFERENCE_AUDIT.md). The
[diagnostic source](certificates/a4d_native_owner_diagnostics.lean),
[captured Lean output](certificates/a4d_native_owner_diagnostics_output.txt)
and [source-hash ledger](certificates/a4d_native_owner_diagnostics_results.json)
are retained. Lean 4.30.0 elaborated the imports and queried the actual
environment; each bound candidate's actual proposition and transitive
axioms were printed. The diagnostic does not manufacture aliases or
same-named trivial theorems.

The first 12 lookups use the named modules' intended fully qualified
names. One resolves after importing an additional real module, eleven
do not resolve under those exact names in this environment. Missing exact
names are not a theorem that no equivalent proof can exist anywhere.
Candidate replacements are assessed below against the registry prose.

| Diagnostic reference | Kernel result and actual candidate | Reconciliation verdict |
|---|---|---|
| `Cosmology.feedback_pressure_trace_log` | `D0.Cosmology.feedback_pressure_trace_log` exists in `FiniteFeedbackEquationOfState`, outside the row's two named modules. Its proposition combines two assumed true Boolean flags. | Import/binding repair is possible. This proposition does not prove an operator log-determinant pressure derivative; that stronger portion remains an owner obligation. |
| `sedenion_branch_threeset_scaffold_owner` | Exact name missing; `D0.Algebra.Sedenions.branch_label_s3_scaffold` proves three labels, transitive explicit permutations and distinct products. | Candidate matches the deliberately limited three-set scaffold. CONTROL may bind this finite scope; no Cayley--Dickson or physical generations promotion. |
| `triality_sedenion_s3_disjointness_guard` | Exact name missing. `bare_threeset_insufficient_for_sedenion_realization` proves two distinct equivariant products on the same three-set. | Reject as a substitute for a typed Spin(8)-triality/sedenion intertwiner guard. Keep that specific ownership obligation OPEN. |
| `card_cubical_cochain_carrier` | Exact name missing; `archive_cubical_cochain_carrier_owner` contains `card CubicalCellType = 16`. | The 16-label finite clause is owned. Full site-amplitude carrier is separately defined as `ArchiveCochainBasis`/`ArchiveCochain` in `ArchiveCubicalDifferential`; neither cardinality alone proves a Hilbert/topological identification. |
| `cubical_betti_sum_eq_sixteen` | Exact name missing; `total_betti_sum` adds five **defined numbers** to 16. | Valid arithmetic binding for that sum only. Actual cohomology/Betti calculation is not obtained by renaming the numbers. |
| `d_squared_eq_zero` | Exact name missing; old `archive_cubical_coboundary_owner` proves `CoboundaryNilpotent true`. The separate actual `D0.Geometry.dForward_sq_zero` proves $d_f(d_f\psi)=0$ for the explicitly defined forward cubical differential. | Use the real forward-operator owner for the nilpotency clause, with its carrier and scale. The old Boolean capstone is insufficient. Grading/locality are separate real theorems in that module. No assertion that a curved covariant differential is nilpotent. |
| `b1_isometry` | Exact name missing; `archive_1d_cochain_refinement_owner` proves the defined traces 3 and 2 differ. | Reject replacement by trace arithmetic. No $B_1$ matrix or $B_1^TB_1=I$ theorem is constructed by that owner; leave the exact operator obligation OPEN. |
| `intertwining_d_b0_eq_b1_d` | Exact name missing; same trace owner; the related `archive_graded_refinement_chain_map_owner` proves only dimension/cardinality equalities. | Reject replacement. The actual cross-level $d_{L+1}B_0=B_1d_L$ equation remains an owner obligation for these claimed maps. |
| `hodge_mass_trace_sum` | Exact name missing; `total_hodge_gram_trace_sum_eq` proves the explicitly defined binomial arithmetic sum 256. | That arithmetic is owned; a $B_S^TB_S$ construction or unique refinement-induced metric is not implied. |
| `metric_measure_hodge_lift_owner` | Exact name missing; `archive_metric_measure_hodge_lift_owner` proves degree 0/1 endpoint formulas and cardinalities. | Candidate matches the current row's **already honest limited notes**. No uniqueness or all-grade reduction theorem is added. |
| `archive_naive_weighted_degree_leakage_nogo_owner` | Exact name missing; `archive_naive_weighted_car_degree_leakage_nogo_owner` proves $\sqrt1\ne\sqrt4$ and `card Role = 4`. | Reject as an operator nilpotency/degree-leakage proof. No nonzero commutator or $d_w^2$ witness occurs in that proposition. The comment even refers to applying a difference operator to a constant, whose first difference is zero. |
| `matter_neutrality_m1_forced` | Exact name missing; `matter_localization_observable_canonicity_owner` proves `M1Forced` total readout zero over explicitly neutral source completions on `Fin 2`. | Its finite total-readout clause is owned. The completion relation assumes total neutrality; the proposition neither derives anomaly cancellation nor constructs local metric stress. |

All 12 diagnostics now have an explicit assessment and owner disposition.
This is **diagnostic reconciliation**, not a claim that all 12 stronger
registry statements have been proved, amended, or accepted. Proposed
metadata changes and scientific scope corrections require CONTROL intake.
The current registry is preserved in this research execution.

## Actual curved differential and conditional hypotheses

The compiled `dConn_sq_eq_curvature` says the square of the covariant
differential is the transported curvature operator. Its flat specialization
requires every open-path curvature to vanish. Thus the real forward
nilpotency theorem cannot be substituted for a curved cochain complex.

The native gravity capstones were also checked. The parent stress descent's
type explicitly takes readout compatibility, parent Ward, auxiliary EOM and
coframe EOM as hypotheses. `gravity_variational_carrier_audit_owner` takes
`IsGraphLaplacian L` and proves conservation/symmetry of a response defined
as $2L$. `d0_archive_satisfies_structural_admissibility` takes the dimension
condition and structural predicates; the coefficient slot is not an actual
heat coefficient. `physicalPrimitive_card_eq_two` takes an actual
`Representation` with faithful physical laws; the raw toy instance does not
construct a physical realization. `locatedStar_does_not_select_reference_weight`
retains the supplied reference weights and their second-order separation.

Transitive axiom output is retained, rather than reporting a misleading
"no axioms" result. Most inspected owners use `propext`, `Classical.choice`
and/or `Quot.sound`. Structural signature and primitive-count dependencies
also include the printed `native_decide` evaluation axioms. These are distinct
from supplying a physical Ward identity, action map or continuum limit as a
theorem argument. No `sorryAx` was found in this diagnostic output.

## Verification scope

The diagnostic was built narrowly against the pinned current source tree
with a warm cache, rebuilding changed imports. Cache reuse is acceleration;
the compiler result and source hashes are the evidence. The temporary
diagnostic module under `03_FORMALIZATION/D0` is removed after capture;
the identical source remains here as a reproducible read-only capsule.

After the consumed imports are built, replay it from `03_FORMALIZATION`:

```sh
lake env lean ../02_REGISTRY/research/certificates/a4d_native_owner_diagnostics.lean
```

This import/type audit does not validate every registry row, derive every
physical premise, or replace the final `D0.All`/current-head CI gates. Those
results are recorded separately when actually run. In particular a build
of `ClaimMap` strings alone would not perform these lookups.
