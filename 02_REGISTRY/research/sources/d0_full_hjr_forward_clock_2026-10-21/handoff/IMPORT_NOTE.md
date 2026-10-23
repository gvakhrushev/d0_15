# Forward-clock package import

The supplied `D0_full_HJR_forward_clock_2026-10-21.zip` has SHA-256
`1fce3a47eaa54c367392e2aa5cb12e0ff4d187307ee55eb1a6f22c2ca79cb23a`.
All 14 entries in its package checksum manifest were verified. The eight
repository additions are installed at their canonical paths; the archive's
top-level proof and result are byte-identical to the canonical source copies.
The original additions patch, package manifest, Russian readme, validation,
and integration-status files are retained verbatim in this directory.

The imported repository replay wrapper is made portable across numerical
environments: its normal and optimized runs must still match byte for byte,
while floating scalars are compared with tight relative and absolute tolerances
against the unchanged authored result. On this host the archived wrapper's byte
comparison failed only on seven floating-point values at machine precision
(largest absolute difference `1.42e-13`). The original wrapper remains
available inside `additions.patch` and is hash-pinned by
`PACKAGE_SHA256SUMS.json`. The revised wrapper hash is included in the source
package's `SHA256SUMS.json`.

`INTEGRATION_STATUS.json` records the state when the archive was assembled,
including that no remote publication had yet happened. It is historical
package metadata, not a direction governing this import. The present files
continue the existing Draft #334 and keep the original boundaries: no
compulsory physical clock/cut/heat choice, independent review, full native
replay, or `GR_closed` claim is added.
