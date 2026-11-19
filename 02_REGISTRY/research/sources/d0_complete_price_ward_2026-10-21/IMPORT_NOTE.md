# Complete-price archive import

The supplied `d0_complete_price_density_rigidity_2026-10-21.zip` has SHA-256
`ff231dcc8fff85392d68cef8d2add6a870f5d1156e81014b1a682a6b30e86330`.
Its eight entries listed by `SHA256SUMS.json` were verified against the
archive. The proof, checker, and author receipt were already in PR #334 and
match the archive byte for byte. The remaining archive payload is now stored
beside them, including the original result and both identical run logs.

`PUBLICATION.json` records the earlier publication of the proof and checker
at `bd2005bb5f2ec6dfe4d1738941ff7ab36cde072e`; it does not claim independent
scientific acceptance. This import adds the archived outputs and provenance
to that existing research package. It does not change the source theorem's
scope: fixed-measure continuum price only, with `GR_closed=false`.
