# Memory-preserving source code and the finite orbit compatibility test

[Full derivation](../../A4D_MEMORY_PRESERVING_SOURCE_CODE.md).
Repository `gvakhrushev/d0_15`, existing research PR #334; no new execution.

The three already-owned full16 link-source operators satisfy exact code
identities on the four-dimensional native memory subspace. The entire16-state
carrier splits into four syndrome and four logical coordinates. An explicit
full unitary changes the source for every balanced memory state while preserving
its logical history. No extra register, reset, or new physical noise model is
introduced. Repeated source products retain a nontrivial logical operator.

For an actual candidate M_v, the previous necessary nonlinear memory condition
is exactly four4x4 real-eigenvector conditions, not a scalar expectation test.
Four consecutive own even-tail states test this condition for the whole tail
at one fixed field velocity; five test all affine preparation-dependent first
field rows. These results do NOT solve those five native systems, the remaining
third-order compatibility, or a curved branch. They do not select a physical
encoder, change v8, or establish GR.

Inputs: `A4D_NATIVE_MEMORY_SOURCE_FIBRE.md` at
`ec45c8cc4085e7bce888d97439251be9e578d4ff`, blob
`0dbe97237dc0a2e3ae09501b9c47e100ece3b0b0`, the literal closed engine,
and the full joint native second-source owner. The relevant prior attached
nonlinear equations are reproduced in the proof; no ZIP or chat is needed.
The concurrent `0dd1853a81f5ac3f9883e09d9d2f6dd8695f030e` classifies the
nearby faithful finite critical locus as flat. That result is consumed, not
recomputed or extended to the rank8 boundary. The present consumer is N06/N07's
rank-free memory branch, using their ACTUAL M_v and full first kernel.

## Reproduce without changing committed evidence

From this directory, Python/SymPy only:

```sh
python check_memory_source_code.py > /tmp/d0-memory-code-normal.json
cmp /tmp/d0-memory-code-normal.json result.json
python -O check_memory_source_code.py > /tmp/d0-memory-code-optimized.json
cmp /tmp/d0-memory-code-optimized.json result.json
python test_mutations.py
```

`result.json` records117 exact conditions. General CAR/Gram/third-moment
identities are symbolic in A,B. The full unitary has an exact rational bounded
fixture; it is not a new root. Golden orbit identities use exact algebraic
reduction. `test_mutations.py` changes only temporary copies and verifies four
mathematical failures against the preserved validation. It never rewrites
source or result receipts. `validation.json` records actual normal/optimized
runs, versions, mutations, and hashes.

No prior scientific suite or Lean build is replayed. The attempted new native
q3300 numerical assembly did not complete and supplies no evidence here.
No independent scientific acceptance, main merge, physical primitive admission,
new native critical velocity, nonflat joint solution, or refinement-uniform
GR theorem is claimed. The own code's infinite history has no uniform finite
resolution separation; this isometry preserves, rather than evades, that fact.
