# Source Lagrange polynomial over GF(1009)

The source three-point polynomial at 0, 969 and 410 has values 1, 808 and 278 and simplifies to `1 + 444 T + 98 T²`. For any two orthogonal idempotents P and Q, its value on `969 P + 410 Q` is `1 - P - Q + 808 P + 278 Q`. Repeated eigenvalue multiplicities do not invalidate this identity. Independent source review checked the order and coefficients.

Narrow Lean and axiom checks passed on blob `b267fc33c8663dfdbd017c18ba9cb41a8113f831`, using an existing dependency cache; the axiom footprint was `propext`, `Classical.choice`, `Quot.sound`. If the committed blob differs, only trailing blank lines were normalized. Final provenance-guarded integration remains open.

This generic result takes actual orthogonal projectors as inputs. It does not yet prove the relevant source Gram matrices have that decomposition, nor that Python execution and Lean source operators correspond, nor the 128-history complex rank. It does not add a physical premise or alter owner #334; `GR_closed=false`.
