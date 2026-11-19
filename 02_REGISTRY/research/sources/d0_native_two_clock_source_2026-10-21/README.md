# Native two-clock input/source packet

Supporting research for existing Draft #334. Full proof: `PROOF.md`.

The original flat full128 instrument, restricted to one axial CAR16 Fourier
block, has an exact Pauli spectrum and attained mixing gap O(h^6). Its stated
port-cost/coherent-record valuation has an exact unique uniform input minimum
for every n>=8 and an interior joint scalar-field/input minimum at the physical
n=128h^-4 horizon for every L>=4. The refining source converges in C2 to the
already-owned positive scalar minimum, but254 input Hessian directions soften.
The h^-6 equilibration clock has a different positive h^-2 paid field source.

This is NOT full physical D0->GR, a whole-spatial42 root, an input writer,
a physical choice of Info or a new same-execution Book binding. The diagnostic
uses16 active Schmidt columns embedded in oldRIGHT128. No implicit rank128
primary-preparation or fixed-collar source claim is made.

Run from this directory (Python3.9+):

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python check_two_clocks.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python validate_packet.py
```

Dependencies: numpy, scipy, sympy, mpmath. The author environment versions
and byte-identical normal/-O evidence are in `VALIDATION.json`.
`RESULT.json` is frozen expected output; validation never rewrites it.

`native_axial.py` independently reconstructs the original128 matrices and
both defect jets at the specified axial phases. `spectral_price.py` evaluates
the analytically derived coherent spectrum with high precision; these are
not pointer-history probabilities. `check_two_clocks.py` performs exact and
floating controls, with four explicit semantic mutations in the validator.

No fresh Lean, repository-wide CI or independent-agent review is claimed.
The consumed limiting Lambda_*, physical dephasing law and Info-cut contrast
retain the original20 October owner's priority; see `SOURCE_PINS.json`.
