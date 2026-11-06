# PR #334 continuation after the `7261923` checkpoint

This packet records the next exact source range of the same open Draft PR #334:
`726192353504a81a9ab2b751f9b6c7866271e75a` →
`8daed32d560df18837bcc69458a8fa538a9cf135`. The live PR head was checked on
28 October 2026; the range contains seven commits, six changed files, 2,816
inserted lines, and 4,170,797 snapshot bytes. It extends the earlier
[post-`eebcb5e` packet](../d0_334_post_eeb_delta_2026-10-28/README.md) without
changing that historical snapshot.

## Results integrated

- **Retained past (`§7dd`, equations 910–918).** The full nonlinear
  Einstein–dust source is carried through an arbitrary fixed, possibly
  noncommuting full128 history. The proof keeps the actual cumulative gain,
  the changing-past source row, old records, and full heat. A sealed-prefix
  corollary varies only the newest block. Its 22 exact changed-input checks
  pass in ordinary and optimized Python with byte-identical receipts.
- **Fixed-boundary scale source (`§7de`, equations 919–926).** On the original
  L4/full4096 CAR realization, the first and last complete groups stay fixed
  while the seven internal groups vary. The full feedback source has opposite
  certified endpoint signs; the whole-scene heat derivative is bounded by
  `2^-240`. Continuity gives one zero of the sum of those seven internal
  scale rows. This is not separate vanishing of all seven rows, full
  40+matter stationarity, a minimum, or physical selection. Both endpoint
  calculations were rerun with Python 3.9.6 / NumPy 2.0.2. The low receipt
  JSON matches its embedded owner JSON, but the owner's printed low-receipt
  SHA-256 differs from the digest of those exact bytes by one hex digit; see
  the replay report. The high receipt digest matches.
- **General direct-click reverse lift.** For every sufficiently smooth local
  positive-density irrotational geodesic Einstein–dust solution on the fixed
  branch, conserved mass `M = ρ E` defines a local map with Jacobian
  `J = M/(2q₀)`. It preserves proper time and gives `ρ E_X = 2q₀`, placing the
  same metric and matter fields on the original nonlinear direct-click
  branch. The proof checks all 16 coframe, 24 independent connection, and two
  material rows in ambient directions. A separate local Ricci-flat vacuum
  sector is retained. The 109 symbolic controls pass in normal and optimized
  mode; both receipts match the owner JSON exactly.
- **Cauchy application (`§7df`, equations 927–934).** Smooth constraint-
  compatible dust-orthogonal data generate a local development in the same
  derived nonlinear sector. The result retains all four initial Einstein
  constraints, the two material equations, the initial-data mass map, and a
  negative control for the discarded Hamiltonian row. Its 28 exact symbolic
  controls pass in normal and optimized mode with a byte-exact owner receipt.
  The existence theorem is external and attributed to Choquet-Bruhat and
  Friedrich, *Motion of Isolated Bodies*, Theorem 2.1 and Corollary 2.2
  ([arXiv:gr-qc/0605096](https://arxiv.org/abs/gr-qc/0605096)); the checker is
  not a proof of that theorem.

## Composition boundary

These are useful continuum source and solution results on their declared
carriers. They do not identify the direct-click price with the original
full128 price, establish physical admission of the comparisons, prove exact
finite stationary words, discharge every independent apparatus equation, or
complete a physical refinement. The new continuum results have not been
formalized in Lean and add no `formal_support`, claim, acceptance, or lifecycle
row. Existing scalar-branch and finite moving-projector Lean results remain
separate. `GR_closed=false`.

## Packet contents

- `UPSTREAM_SOURCES.zip` and `UPSTREAM.patch.gz` preserve the six changed
  owner files and exact full-index Git patch.
- `COMMITS.tsv` and `MANIFEST.json` pin the seven-commit range, changed paths,
  byte counts, Git blob IDs, SHA-256 values, and the replay artifacts.
- `direct_click/` exposes the new proof, checker, summary, and owner result for
  convenient reading.
- `replay/` stores the exact extracted checkers and their normal/optimized
  outputs, including the two fixed-boundary endpoint outputs.
- `verify_source_delta.py` checks packet bytes, source archive, patch, source
  receipts, and optional exact Git objects. It does not execute the research
  checkers or establish scientific acceptance.

Run `python3 verify_source_delta.py` for packet verification. Add
`--verify-source-objects` when both commits are available locally.
