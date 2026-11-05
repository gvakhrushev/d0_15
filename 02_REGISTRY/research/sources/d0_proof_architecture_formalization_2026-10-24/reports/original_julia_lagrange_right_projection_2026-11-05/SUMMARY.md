# Moved-D right projection and Lagrange polynomial

The generic source Lagrange polynomial is now applied to the actual previously proved integer-derived right projectors after reduction modulo 1009. Their orthogonality and idempotence, including the 1/1762 normalization, imply that the polynomial on `969 * modRegular + 410 * modBoosted` equals the explicit `modMovedRight`. This is a concrete application, not a fresh rank search.

Narrow Lean and axiom diagnostics passed on exact source blob `d462f55f1ae0c5a1a322625fda839732c80573cb` using an existing dependency cache; axioms were `propext`, `Classical.choice`, `Quot.sound`. An independent read-only review found no defects. A trailing-blank-only normalization may change the committed blob; final provenance-guarded integration remains open.

The decomposition of the actual source Gram as this weighted projector sum and the Lean/Python executable correspondence remain separate obligations. No complex rank, physical admission or GR closure follows yet. Owner #334 and `GR_closed=false` remain unchanged.
