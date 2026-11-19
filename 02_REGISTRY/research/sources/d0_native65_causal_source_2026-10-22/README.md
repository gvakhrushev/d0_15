# Native65 causal source continuation

Read `THEOREM.md` first. It separates the exact finite analytical identities, consumed earlier results, numerical checks, and unproved physical selections.

`check_native65_causal_source.py` compares fullfine and merged prices, causal forward and backward responses, initial-state derivatives, retained-reference corrections and the actual native two-tick predictive information. `check_archive_birth_extension.py` is the bounded K=3 diagnostic accompanying the analytic all-finite-K lower bound. `native_excerpt.py` preserves the source functions read through the GitHub connector; it is not a complete repository checkout.

The saved `RESULT.json`, `RESULT_OPTIMIZED.json` and `ARCHIVE_BIRTH_RESULT.json` are actual local execution outputs. The first two are byte-identical. Numerical thresholds and original source scope are explicit in the checker and theorem. No new Lean, interval or remote CI claim is made.

Run:

```sh
OPENBLAS_NUM_THREADS=1 python check_native65_causal_source.py
OPENBLAS_NUM_THREADS=1 python -O check_native65_causal_source.py
OPENBLAS_NUM_THREADS=1 python check_archive_birth_extension.py
```

Dependencies used: Python, NumPy, SciPy. See `PROVENANCE.json` for actual runtime versions and SHA-256 hashes. Additional local code is read-only with respect to the source repository.
