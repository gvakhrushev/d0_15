# Local moved operand and source right Gram

The actual local D operand maps to `(469 * 3/200) fortyMoved` and `(540 * 3/200) fortyMoved` under the two evaluations. Conjugation before the plus evaluation exchanges those branches. Their product gives exactly the previously established modular source right Gram, including the order `fortyMovedᵀ * fortyMoved` and scale `9/40000`. The direct generator, boost and creator-times-boost correspondence is also proved. Independent read-only review checked these source identities and phases.

Narrow Lean and axiom checks passed on exact blob `f069bb87353e3ec6f7b680fb0cfc8f4756cc2b32` using the existing dependency cache; footprint `propext`, `Classical.choice`, `Quot.sound`. Lean emitted one linter warning on tactic style. Committed source may differ only by trailing blank-line normalization. Final provenance-guarded integration is not yet complete.

Applying the Lagrange theorem to this result, the left Gram, the whole Walsh/effect chain and the correspondence to execution of the Python source remain separate obligations. This does not prove the complex rank or physical admission. Owner #334 and `GR_closed=false` are unchanged.
