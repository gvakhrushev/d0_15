# Retained entropy and paid input Euler: reproduction

Existing research owner #334. Main entry:
`../../A4D_COMPLETE_RETAINED_ENTROPY_INPUT_EULER_2026_10_21.md`.

Run the narrow checker with one BLAS thread:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python check_retained_input.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -O check_retained_input.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python validate_packet.py
```

Requires numpy, scipy and sympy. Byte comparisons target the environment in
VALIDATION.json; another BLAS stack may change final digits even if the
declared tolerance checks pass. The unchanged full128 input is found in the
existing native-preparation packet or in the delivery ZIP's `inputs/` folder;
its Git blob is checked before any calculation. The validation script compares
frozen outputs rather than rewriting them. `--record` is only for explicitly
creating a new validation record after a deliberate review of changed inputs.

PROOF.md is the analytical finite and asymptotic theorem. RESULT.json contains
63 bounded checks and numerical diagnostics. Those diagnostics are not interval
certificates or a whole spatial rank128/all42 validation. SOURCE_PINS.json records
provenance. VALIDATION.json distinguishes exact algebra, numerical replay and
physical hypotheses. No independent-agent review, full Book valuation, physical
input admission or GR closure is claimed. Earlier scientific receipts are reused
unchanged and are not represented as freshly executed.
