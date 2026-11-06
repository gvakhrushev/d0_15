# Book02 review corrections: integration checks

Tested implementation snapshot `b8930d4d07bb8d5221c379ab94db3e74f1c0d415`,
whose source changes are retained in this review's commit history. This is a
local test snapshot, not a claim of GitHub publication or C0 acceptance.

- The reconciliation, candidate-range, original Book02 version, versioned
  owner and new review suites passed **119 tests** on Python 3.13.5.
- The six new controls also passed under system Python 3.9.6 and through the
  existing compact cold-start test aggregator; Lean-view fixtures passed 29.
- At the exact historical #402 snapshot `a358e91e764655b16082bf7e6161a79df96a24a6`,
  the older helper and revised helper emitted byte-identical Book02 JSON,
  SHA-256 `74a7f857a4e42c645f947bad96e1f43e458bd02476fdfad0869d456b4d904d3c`.
- On the actual corrected snapshot the view includes 30 units, the precise
  equivalence and the named bridge dependency, retaining the historical
  statement. Its historical compiled inventory is still unresolved without a
  qualifying explicit current inventory. All semantic acceptance remains
  pending and no C0 denominator is inferred.
- `real_snapshot_hostile.py`, run against a disposable local shared clone,
  verified that modifying/deleting the review, modifying its Lean control, or
  deleting the primary pointer causes the source step to fail closed; see
  `real_snapshot_hostile.log`. This script creates unreferenced Git objects
  and test commits in its disposable clone, without moving references. Its
  CLI explicitly requires that clone, target snapshot, and current helper.
- `verify_bytes.py` rechecked the exact historical/active full-file pins and
  the 30 candidate range complement. The full Lean declaration/axiom log and
  separate empty-word dependency proof were collected against an existing
  cache whose TheoryTransfer source blob exactly matches the pinned owner.
  No fresh `D0.All` or new compiled declaration inventory is claimed.

The reporting helper authenticates the exact report/control bytes and their
presence in snapshot history, not review independence or execution of Lean.
Earlier history and the historical candidate JSON/sha are not rewritten.
