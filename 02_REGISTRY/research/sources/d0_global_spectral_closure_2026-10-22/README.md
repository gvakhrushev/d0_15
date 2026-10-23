# Global spectral action: thermal Schur / Ward closure and true-scene source limit

Repository: `gvakhrushev/d0_15`
Scientific parent: existing Draft PR #334
Target branch: `exp/a4d-joint-response-continuation-2026-10-16`
Read snapshot: `a82df288e4832d53fd52fc88a78ef2dc123bcc88`
Date: 2026-10-22

Read **THEOREM.md** for the Russian proof, inherited owners, all hypotheses and scope.

## Results

- Exactly one global auxiliary variable eliminates the logarithm of the entire paired heat trace, with the complete first source and rank-one Hessian Schur correction retained.
- The previously owned local trace/Ward theorem now applies to the explicitly stated nonlocal continuum spectral model. A whole-domain outward interval certificate proves regularity and a unique self-consistent sector for every `|y|<=0.0002`, `W>=528*8^4`, fixed `Z0>=0`.
- The full regular continuum equations correspond in both directions to Einstein equations with **two constrained real CAR scalars**, in a positive-volume gauge. This is not arbitrary matter, generic finite lattice recovery, or compulsory D0 selection.
- The actual normalized scene `L_sym(K(9,11,13))` is evaluated without identifying it with the paired cut Hodge. An independently changing existing edge has a nonzero heat source.
- Dimension-independent noncommuting heat first/second-source bounds, and relative-edge bounds for normalized graph Laplacians, give a sufficient full spectral source-limit criterion. Actual signal scaling, norms, other price terms and independent apparatus equations remain required.

`GR_closed=false`. A passing calculation does not select the actual physical execution.

## Reproduction

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python run_validation.py
```

Requires Python with `numpy`, `scipy`, `sympy`, `mpmath`. The validation wrapper does **not** rewrite expected outputs. It checks SHA-256 pins before and after, executes the new checker both normally and under `-O`, replays the pinned original symbolic 40-row checker **without** `-O`, and replays the previous global-spectral package.

See `VALIDATION.md` for the exact evidence boundaries. `RESULT.json` is a mixture of outward interval predicates, exact symbolic checks and explicitly labelled numerical diagnostics; it is not a claim that all floating-point outputs are interval-enclosed.

## Files

- `THEOREM.md`: complete proof and physical boundary.
- `native_spectral.py`: unchanged Golden polynomial formulas and explicit derivative expressions.
- `check_spectral_closure.py`: independent derivative comparisons, outward chart certificate, exact geometry normalization, Schur, true scene and noncommuting controls.
- `RESULT.json`, `RESULT_OPTIMIZED.json`: byte-identical outputs from this environment.
- `inputs/check_all40_arbitrary_brinkmann.py`: byte-identical upstream blob `e502807955321465903d7ab1a248e0456ac69f60`.
- `GEOMETRY_REPLAY.txt`: actually executed original symbolic geometry output.
- `previous/`: previous local global-spectral package preserved, not relabelled as a new proof.
- `MANIFEST.json`: immutable content pins, excluding this manifest and generated validation output.

## Delivery

This package was created locally. The connector available during this pass exposes GitHub GET operations only; the runtime has no usable GitHub network connection. No remote commit, push, PR update, main merge, CI run, or new Lean build is claimed. The separate delivery receipt records a real **local delivery-repository commit** and a portable `git am` patch. That local commit is not a descendant of the remote PR history.
