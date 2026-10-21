# Exact null two-field source fibre

Existing PR #334 supporting packet. Read PROOF.md for the full local
classification, intrinsic inverse, exact nonlinear characteristic example,
fixed-native-gauge restriction and complete-readout criterion.

Reproduce from this directory:

```bash
python check_source_fibre.py > replay.json
python -O check_source_fibre.py > replay.optimized.json
cmp replay.json RESULT.json
cmp replay.json replay.optimized.json
```

Python 3 and SymPy are required. Recorded author environment: Python 3.13.5,
SymPy 1.14.0. 87 exact groups pass; no network or historical input replay is
needed. Explicit exceptions keep every check active under -O.

SOURCE_PINS.json records the immutable D0 owners and limited external
background. VALIDATION.json records exact hashes and validation scope.
No independent review or physical GR closure is asserted.
