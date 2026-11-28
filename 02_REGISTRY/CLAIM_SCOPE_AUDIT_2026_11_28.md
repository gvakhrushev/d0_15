# Statement and certificate scope audit

This audit compares the listed declaration statements, executable checks and
registry prose. It does not alter registered claim IDs, release or Lean
statuses, module owners, theorem names or historical evidence. A positive
finite check is evidence only for its actual inputs and conclusion.

| Claim or artifact | Verified scope and remaining boundary |
|---|---|
| `D0-TRIALITY-SEDENION-S3-DISJOINTNESS-GUARD-001` | [Lean](../03_FORMALIZATION/D0/Algebra/Sedenions.lean) constructs two actions of the same six-element permutation group. The natural action has a bijective self-intertwiner, while no injective intertwiner leads from it to the trivial action. Equal group order alone therefore does not identify actions. The proof does not construct or compare the actual Brown and Spin(8) triality actions. |
| `D0-FIBONACCI-AF-TOWER-OWNER-001` | [Lean](../03_FORMALIZATION/D0/Algebra/FibonacciAFTower.lean) proves five declared dimension values, two scalar identities and a matrix-square identity. Its separate pairing equality assumes a supplied multiplication-, star- and trace-preserving map. These declarations do not construct an AF inductive limit, unique trace state, Hilbert-space GNS tower or Dixmier normalization. |
| `D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001` | The [Lean module](../03_FORMALIZATION/D0/VNext2/AdlerWeissInternalMarkov.lean) proves a matrix conjugacy and determinant. The [certificate](../04_CERTIFICATES/vp_adler_weiss_internal_markov.py) checks golden interval endpoints, evaluates two expressions numerically and checks the matrix identity. It does not construct a natural-extension-to-torus map or transport a partition. Its computational checks are unchanged; its descriptions and output now state their scope. |
| `D0-ALBERT-SM-GAUGE-PROJECTION-001` | The [Lean owner](../03_FORMALIZATION/D0/Gauge/AlbertSMProjection.lean) establishes the numerical dimension inequality, factor count, charge-coordinate alignment and anomaly sums. It does not construct an embedding or representation. `D0-ALBERT-SM-SUBGROUP-REPRESENTATION-OWNER-001` remains the separate `UNPROVED / PROOF-TARGET`. |
| `D0-MINCUT-001` | On the original four-vertex network, the original source `0` and sink `3` have max-flow and min-cut `0`. The separate specified cut `A={0,1}` has capacity `4`, and its `/4` value is defined to be `1`. The [certificate](../04_CERTIFICATES/vp_finite_mincut_holographic_entropy.py) no longer equates these two cuts or labels the defined value as computed quantum entropy. Historical [manifest](../05_EXPERIMENTS/FiniteHolography/finite_mincut_entropy_manifest.json) and summary are retained as historical evidence, not as verification of the former `0 = 4` output. |
| `D0-CONNES-DISTANCE-GEODESIC-001` | The [certificate](../04_CERTIFICATES/vp_connes_distance_geodesic.py) checks graph distances and sampled edge-Lipschitz functions on finite examples. It does not construct the Dirac commutator norm or establish a physical signal-speed bound. |
| `D0-COSMOLOGY-CONNECTIVITY-THRESHOLD-OWNER-001` and `D0-REHEATING-PERCOLATION-OWNER-001` | Their [Lean owner](../03_FORMALIZATION/D0/Cosmology/ReheatingPercolationOwner.lean) returns Boolean fields of the declared transition. The connectivity certificate separately checks two selected finite graphs. Neither establishes a physical transition time or absence of an initial singularity. |
| `D0-CVFT-001A` and `D0-CVFT-NOGO-001` | The [registered aggregator](../04_CERTIFICATES/vp_closed_vacuum_feedback_full_wave.py) checks exit codes and output tokens; several tokens lack the named independent control. The listed Lean modules include elementary consequences of supplied Boolean fields. See the [consumer audit](CERTIFICATE_CONSUMER_AUDIT_2026_11_28.md) for the separate checks and limitations. |
| `D0-PASSPORT-DESI-BAO-001` | The old standalone DESI runner could generate synthetic rows and emit a physical `FAIL`. Its entrypoint now returns `SKIP` without creating files or changing the manifest. Even a hash-verified input does not establish that the required covariance, baseline and comparison pipeline is implemented. Historical result files are retained and are not an observational verdict. |

The registered statuses remain as in `claims.csv`; the notes now identify
the actual owner statements and their limits. The historical
`vp_external_research_status_guard.py` requires obsolete `FORMALISM` statuses
and fails against the current registry. It is retained byte-for-byte because
the historical [checkpoint](research/CONTROL_A4D_NATIVE_VARIATIONAL_CHECKPOINT.json)
records its input hash and failed result. Its result is not an assessment of
the current conditional Albert theorem.

Three registry rows had unquoted commas in their final notes fields. The rows
were re-quoted without changing their first ten fields or the complete note
text at that step. The triality note was subsequently updated to describe the
new theorem above. `tools/validate_repo.py` now rejects extra or missing parsed fields;
the regression check covers both malformed forms and a correctly quoted comma.

The remaining missing weighted-leakage owner is tracked in the
[Lean reference audit](LEAN_REFERENCE_AUDIT.md). Its original general
operator claim and the exclusive Hodge interpretation must not be inferred
from a scalar inequality or from one finite counterexample alone. The new
[structural witness](research/sources/d0_weighted_leakage_2026_11_27/RESULT_STRUCTURAL_RU.md)
proves a general conditional two-shift criterion and a concrete four-role CAR
leakage at level 0; it does not prove every-level leakage or Hodge uniqueness.
