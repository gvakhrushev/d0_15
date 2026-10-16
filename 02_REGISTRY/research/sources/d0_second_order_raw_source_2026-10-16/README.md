# Exact raw-row and finite-clock source identities

Consumer: [second-order heat/source proof, Section8](../../A4D_SECOND_ORDER_HEAT_REMAINDER.md),
same Draft #334. This new bounded calculation checks the algebra used in
the analytic source-kernel theorem; it does not replace the heat estimates.

A three-site ring retains all16 Fock grades and noncommuting proper Lorentz
transports. All39 independent source directions (12coframe,18scaled
leftlink,9observer) match direct true-adjoint differentiation and the cyclic
rows. Polynomial kappa=I+Delta is only a nonzero algebraic fixture. Three
formal heat eigenvalues separately check the full finite-clock gradient,
including the global normalizer and the distinction between the trace clock
and its derivative. Hostile order/factor/clock omissions are rejected.

Replay only the new helper from repository root:

```sh
python3 02_REGISTRY/research/sources/d0_second_order_raw_source_2026-10-16/check_second_order_raw_source.py
```

Normal and optimized outputs are byte-identical;62 exact groups. Only the
actual creator/order definitions are AST extracted. Old root/heat/kernel
suites and Lean are not executed. Exact input/output hashes and runtime are
in VALIDATION.json; RESULTS.json preserves the complete new calculation.

Локальные обозначения checker: `P=full_clock=B^m`, `K=derivative_clock=B^(m−1)=P/B`; в §8.6 `A4D_SECOND_ORDER_HEAT_REMAINDER.md` буквы `K/P` переставлены (`K=full_clock`, `P=derivative_clock`), поэтому сравниваются указанные операторы и их роли, включая полный normalizer, а не имена переменных.
