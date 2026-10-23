# Q8 real Book source: complex feedback from paid Golden quadrature inputs

21 October 2026. Existing Draft PR #334; `GR_closed=false`.

The [main proof](../../A4D_Q8_REAL_BOOK_SOURCE_INTERFACE_2026_10_21.md) constructs the doubled-real / Q8-quadrature representation of the original complex normalized Book feedback source, and gives a literal paid `H_r, CNOT(b,r), H_r, CNOT(b,r)` input writer. This is **not** the physical realified CAR channel or the compulsory Book03 H+J+R valuation.

Exactly d² Golden/quadrature input settings reconstruct an arbitrary Hermitian d-by-d effect and its first jets. On the original CAR16 parity algebra 128 settings **per effect** suffice if native access to both 8-dimensional sectors is actually permitted. Realification preserves normalized Book value and source with an essential factor 1/2. Original full128 two-round Fourier numeric checks retain the 128-Kraus outcome law, analytic jets, non-scalar operator normalization, 128 oldRIGHT trace multiplicity. Exact 2x2 negative control proves real-only probes can miss source 8/35. The native `H` factory is complete with finite-cap readiness `b₂²`, so the two-H conditional J input word has true readiness `b₂⁴>0`, with all failure/clock charges kept.

- [Proof](../../A4D_Q8_REAL_BOOK_SOURCE_INTERFACE_2026_10_21.md)
- [Standalone checker](check_rebit_book_interface.py)
- [Saved normal receipt](REBIT_RESULT.json)

Reproduce from repository root with Python, NumPy, SciPy and SymPy:

```sh
python3 02_REGISTRY/research/sources/d0_q8_real_book_source_2026-10-21/check_rebit_book_interface.py --output /tmp/d0_q8_rebit.json
python3 -O 02_REGISTRY/research/sources/d0_q8_real_book_source_2026-10-21/check_rebit_book_interface.py --output /tmp/d0_q8_rebit_opt.json
cmp /tmp/d0_q8_rebit.json /tmp/d0_q8_rebit_opt.json
```

Normal and optimized local runs pass 55 scoped controls with byte-identical JSON. Historical all42/Book03/refinement/Lean suites were not replayed, and no external independent peer review or CI result is claimed. Algebraic controlled-J construction and its availability through the declared addressed paid Golden H factory are proved; the physical  realified original full128 channel, native cut and Info valuations remain open.
