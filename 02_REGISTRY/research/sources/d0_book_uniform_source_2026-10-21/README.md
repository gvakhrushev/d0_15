# Complete cost-marked full128 archive source

This packet continues PR #334 on the original first-shell full128 process.
Read PROOF.md for the analytic count-bound, C1 normalized complementary source,
Golden event-time/port intertwiner, real logical price transport and scope.

Reproduce from this directory with Python, NumPy, SciPy and SymPy:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python check_uniform_book_source.py > /tmp/d0-book-source.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -O check_uniform_book_source.py > /tmp/d0-book-source-opt.json
cmp /tmp/d0-book-source.json /tmp/d0-book-source-opt.json
```

RESULT.json is the unchanged author-run output (115 checks); VALIDATION.json
pins its bytes and the proof/checker, with actual run scope. Floating results
carry the explicit tolerances in the checker and may differ in last bits
between numerical libraries. SOURCE_PINS.json identifies the prior owners.
No independence, whole-lattice, physical Info, native padding controller,
new Lean/CI, or GR closure is claimed. The analytical result is not a test
of a second physical price or a physical metric-rescaling theorem.
