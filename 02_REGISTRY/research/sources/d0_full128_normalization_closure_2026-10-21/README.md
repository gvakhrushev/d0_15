# Executed full128 normalization and true-source application

This packet reconstructs the actual operator normalizer, differentiates the true complementary Book feedback, retains all physical filter failures, and applies the result to the owned primary HJR preparation source. It also corrects three recent authored scalar-normalizer notes.

The proof is `PROOF.md`; `RESULT.json` is actual stdout from `check_normalization.py`. `MUTATION_RESULTS.json` records four independently modified scripts that the checker rejected. This is author's replay and self-check, not independent mathematical review.

Run with Python 3.10+ and NumPy, SciPy, SymPy:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python check_normalization.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -O check_normalization.py
```

The script does not rewrite expected results unless an explicit `--output PATH` is passed. Its Fourier-block diagnostic contains all128 labels and all16,384 two-round histories, not the whole256-site primary spectrum. The exact primary source formula is consumed from its pinned owner; its two relevant integer site counts are recomputed. OldRIGHT128 is retained as the actual feedback multiplicity, not falsely represented as a rank128 state on DATA16.

No new Book information rule, physical cutoff, natively admitted post-filter, full field-writer, generic GR theorem, or completed closure is claimed. The common scalar convention cannot repair the tested primary HJR source. The real remaining problem is the admitted full action/variation map, not an unfixed normalization of the known isometry.

Repository publication target: the existing #334, native-programme-v1. Main acceptance and independent review remain separate.
