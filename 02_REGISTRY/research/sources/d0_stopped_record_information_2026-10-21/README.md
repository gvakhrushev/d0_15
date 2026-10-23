# Original stopped all128 record: entropy/gain source application

Research continuation in existing PR #334, 21 October 2026. Consumer:
[complete derivation](../../A4D_ORIGINAL_STOPPED_RECORD_INFORMATION_SOURCE_2026_10_21.md).

This applies the old finite-memory Gram-spectrum calculation to the actual
stopped all128 instrument. The new deliverable is its complete nonlinear
entropy adjoint, with initial preparation, fixed cap, every nonblank and the
unresolved outcome. The two old Info meanings have explicitly opposite
coherence corrections. No physical Info convention is installed.

`SOURCE_PINS.json` records ten original immutable source SHA/Git-blob pins at
`f1618c2de48d851fba0c7171ef783706f41e11d3`.
`check_stopped_info.py` consumes definitions from the pinned exact CAR16
builder by AST, without executing its old suite. The Python 3.9 adapter only
replaces integer popcount by the identical `bin(n).count('1')` operation.
All original labels and all CAR16 grades remain in the calculation.

Replay with Python, NumPy and SymPy:

```sh
python3 02_REGISTRY/research/sources/d0_stopped_record_information_2026-10-21/check_stopped_info.py .
```

`VALIDATION.json` records the actual clean run using Python 3.12.14,
NumPy 2.3.5 and SymPy 1.14.0. This host's bundled Python/NumPy loaded the
pure-Python SymPy/mpmath from the user's existing site after NumPy import;
no packages were installed and no existing runtime was changed. SciPy is
not needed.

The check compares:

* the actual 128 original Kraus and their moving link jets;
* the exit CP map against the recycling-minus-quartic identity and source;
* all 255 stopped cap-two leaf amplitudes against the finite channel and jet;
* full pointer entropy against the independently calculated conditional chain;
* nonlinear entropy adjoint against the direct full-amplitude derivative;
* both derivatives against genuine compact-link/unitary-preparation curves;
* the effect of freezing preparation and of changing the record reading.

The fixture is the already owned rank16 Fourier purification with 16 RIGHT
columns. It is not an evaluation on the primary full-site RIGHT128 GR family.
The test reference is uniform64×Golden(p,p²); its role is checking the code
identity, not selecting physical label/controller prices. Numerical controls
support the finite algebraic proof; they are not interval sign or continuum
certificates. The entropy source at rank birth is a finite first-jet result;
no uniform physical refinement, generic Hessian or field-minimum law follows.

The actual programme/Info-algebra selection and full work/preparation/clock
source remain the parent premise. The original late cap and coherent
padding cannot be priced as a free measured stop. No claims, Book, Lean,
queue state or physical GR acceptance is changed.

[Independent analytical review](INDEPENDENT_REVIEW.md) pins the final proof and checker.
[Integration](INTEGRATION.md) consumes three concurrently published source files: the
actual primary full128 preparation/pointer certificate and the complete
compiler/coframe result. The primary one-round input is exactly cap N=1
of this theorem; its certified source is reused without a second replay.

[Independent integration review](INTEGRATION_REVIEW.md) accepts the cap-one
primary substitution, both conditional Info signs, the retained common
normalizer and the vacuum/nonconstant-null boundary.
