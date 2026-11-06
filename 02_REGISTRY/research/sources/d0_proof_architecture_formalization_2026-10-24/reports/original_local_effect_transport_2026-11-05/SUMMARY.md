# Local chronological effect transport

For any local Kraus family and any finite chronological word, the local effect transports to the corresponding complex effect and to both modular evaluations. Each modular adjoint uses the transpose of the opposite evaluation, with no assumption that the Kraus matrices are real. The word recursion agrees with the source effect order. Independent read-only review checked those identities.

Narrow Lean and axiom diagnostics passed on blob `14765fac612363a1d5f5a25c610f50d4337531ad` using an existing scratch dependency cache; all three declarations have only `propext`, `Classical.choice`, `Quot.sound`. The committed file may differ only in trailing blank lines. Final provenance-guarded integration is still pending.

This generic theorem does not yet construct the original local Kraus family, identify its evaluated entries with the saved 128-history matrix, transfer the determinant or prove physical admission. Owner #334 and `GR_closed=false` remain unchanged.
