# Reproduce

Python 3.13.5, SymPy 1.14.0, mpmath (100 digits in script).

```sh
python check_density_price_bridge.py > rerun.json
python -O check_density_price_bridge.py > rerun_optimized.json
cmp rerun.json rerun_optimized.json
```

The normal and optimized receipts were identical during this session. No external data or network access is needed. The supplied PROOF.md is the expanded proof; SYNTHESIS_RU.md is a Russian explanation. The Git note is the shorter proof presentation of the same result, not a byte-identical copy of PROOF.md.

Git repository: gvakhrushev/d0_15, existing branch exp/a4d-joint-response-continuation-2026-10-16, checkpoint c7708742bea04684ffd6aed16774cfdf1b94b129.

Git note: 02_REGISTRY/research/A4D_DENSITY_INVOLUTION_COMPLETE_PRICE_GENERAL_SOURCE_2026_10_27.md
Git checker: 02_REGISTRY/research/certificates/a4d_density_involution_complete_price_check.py
Git receipt: 02_REGISTRY/research/certificates/a4d_density_involution_complete_price_result_2026_10_27.json

No physical GR closure, independent scientific review, native compilation, large-lattice root replay, Lean build, or CI acceptance is asserted.
