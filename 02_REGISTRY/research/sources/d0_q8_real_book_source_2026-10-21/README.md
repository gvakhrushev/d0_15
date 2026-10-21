# Q8 real Book source: algebraic completion of complex feedback probes

21 October 2026. Existing Draft PR #334; `GR_closed=false`.

The [main proof](../../A4D_Q8_REAL_BOOK_SOURCE_INTERFACE_2026_10_21.md) constructs the doubled-real / Q8-quadrature representation of the **original complex normalized feedback component**, not a newly admitted D0 gate or the complete Book03 H+J+R action.

Exactly d² real Golden/quadrature input settings reconstruct a Hermitian d-by-d effect, with its first jets; on the original CAR16 parity algebra the count is 128 settings **per effect**, provided access to both 8-dimensional sectors. Full 128-port two-round Fourier numeric checks retain original weights, jets, 128 oldRIGHT trace multiplicity and exact 1/2 correction for doubled real determinants. An exact 2-by-2 witness proves real-only probes miss a nonzero first source (8/35). Book06 maximum-entropy duality and the noninjectivity of terminal Q8 class aggregation are stated with their exact boundaries.

- [Proof](../../A4D_Q8_REAL_BOOK_SOURCE_INTERFACE_2026_10_21.md)
- [Standalone checker](check_rebit_book_interface.py)
- [Saved normal receipt](REBIT_RESULT.json)

Reproduce from the repository root with Python, NumPy, SciPy:

```sh
python3 02_REGISTRY/research/sources/d0_q8_real_book_source_2026-10-21/check_rebit_book_interface.py --output /tmp/d0_q8_rebit.json
python3 -O 02_REGISTRY/research/sources/d0_q8_real_book_source_2026-10-21/check_rebit_book_interface.py --output /tmp/d0_q8_rebit_opt.json
cmp /tmp/d0_q8_rebit.json /tmp/d0_q8_rebit_opt.json
```

Normal and optimized author runs on the standalone reconstruction passed 50 scoped controls with byte-identical JSON. Original owner all42/geometry/Book03/Lean suites were not replayed, and no independent reviewer or CI result is claimed. Proof and program were composed against the original full128 native formulas; physical doubling and quarter-turn admission remain open.
