# Local original Julia pairs

The local coefficient algebra now contains the phase, baseline and live operands and all four source Julia row pairs for each actual mode. Their complex embeddings equal both components of the existing source `rowPair`. Independent read-only review checked phases, mode D boost, pair order, adjoints and signs.

Narrow Lean and axiom checks passed on blob `823c18d0e341d9497e8067f3988cc0a115dc74d1` using existing scratch dependency cache; `localRowPair_complex` uses `propext`, `Classical.choice`, `Quot.sound`. Lean reported two unused simp-argument linter warnings. Final provenance-guarded integration remains pending.

This complex bridge does not alone prove execution of Python, the full modular row/word chain, complex rank or physical admission. Owner #334 and `GR_closed=false` remain unchanged.
