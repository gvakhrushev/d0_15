# Independent moving-cut numerical controls

These checks supplement the unmodified Book03 moving-cut checker from PR
[#334](https://github.com/gvakhrushev/d0_15/pull/334), pinned at commit
`eebcb5e467742df3e9cf7fa9702042d7294aa742`. The independent script imports
[`../d0_root_moving_cut_2026-10-28/check_root_moving_cut.py`](../d0_root_moving_cut_2026-10-28/check_root_moving_cut.py)
using a path relative to this directory and checks its SHA-256 before use. It
compares the original source to the full matrix-exponential Frechet derivative
on 25 finite examples, including every projector rank from zero to the full
space for dimensions 2–6. The recorded inputs, seed and tolerances are in
[`result.json`](result.json). Separate five-point controls cover the beta and z
partial derivatives, co-transport and noncommuting matrix exponentials. The
field `required_max_noncommuting_gap_exceeds` is the lower threshold for the
**maximum observed** noncommuting gap across samples; it is not a per-sample
minimum. No input/output JSON is used as a substitute for computation.

The two result files are byte-identical locally in normal and `-O` mode. They
were produced with Python 3.13.5, NumPy 2.3.5 and SciPy 1.17.0 on the platform
recorded in the result. Floating-point values can differ between platforms;
replay the controls and their stated tolerances rather than requiring
cross-platform byte identity. Run from the repository root:

```sh
uv run --python 3.13.5 --with numpy==2.3.5 --with scipy==1.17.0 02_REGISTRY/research/sources/d0_chat_integration_checks_2026-10-28/independent_frechet_controls.py
uv run --python 3.13.5 --with numpy==2.3.5 --with scipy==1.17.0 python -O 02_REGISTRY/research/sources/d0_chat_integration_checks_2026-10-28/independent_frechet_controls.py
uv run --python 3.13.5 --with numpy==2.3.5 --with scipy==1.17.0 02_REGISTRY/research/sources/d0_chat_integration_checks_2026-10-28/check_nonfinite_guard.py
```

The last command mutates temporary copies, not source files. Its
[`nonfinite_guard_receipt.json`](nonfinite_guard_receipt.json) records 34 NaN
mutations: all 12 raw numerical outputs and five computed errors, each in
both normal and `-O` mode, must fail with the expected diagnostic. The guard
checks each value before aggregation; `max(0.0, NaN)` cannot mask a failure.

These are finite numerical checks of the stated matrix identity and its
assumptions. They are not native full42 replay, a Lean proof, physical
admission, independent scientific acceptance or GR closure.
