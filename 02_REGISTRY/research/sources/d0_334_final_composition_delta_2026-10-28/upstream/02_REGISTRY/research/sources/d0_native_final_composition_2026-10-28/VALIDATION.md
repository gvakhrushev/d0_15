# Executed validation and precise limits

28 October 2026, existing PR #334. Initial input
`172876cdf38bfce6f87fdd4a059d524b60c10eb9`; incoming source/phase application
`1d29848fa0775485f7d48ab63f4a6625f9b705ad`.

Incoming `5fe5203da2439d325dc9ef70f52c1111822fc22b` and the final publication
parent `dd7f713cc0ec50c6f66871b3427e3a979d57ade0` were incorporated without
changing these proof inputs. Their generated-cut and all-unitary thermal
applications are read and reconciled in [INCOMING_COMPATIBILITY.md](INCOMING_COMPATIBILITY.md).

## Executed mathematical checks

| Script | Observed result | Receipt |
|---|---|---|
| `check_query_stationarity.py` | Exact full-source identities on 92 complex relative directions, ranks 1–3; mixed-sign hostile control; moving stationary determinant; original 26-stage full32-column, rank8 QUERY including original z=2^-20 | `QUERY_RESULT.json` |
| `check_gauge_moment.py` | 23 exact controls of original boundary moment, contraction, total P/U balance and lapse-source integrability | `GAUGE_RESULT.json` |
| `check_retained_memory.py` | All 12 native full16-column words at N=18,26,42; true rank8 cut and oldRIGHT; exact Golden return matrices and rational all-mode thermal tail bounds | `MEMORY_RESULT.json` |
| `check_terminal_graph.py` | 24 exact controls of the original-return terminal constraints, true reflection stationary branches, zero Schur and incompatible-kernel negative control | `TERMINAL_RESULT.json` |
| `check_phase_descent.py` | 24 exact controls of new phase form, kernel, positive and negative frequency tests, RMS residual, decoder reaction and local cosine-limit jets | `PHASE_RESULT.json` |
| `phase_native_check.py` | 29 exact controls of the actual 8-stage 2G6CX, full32-column/rank8 preparation; full label effects; excess phase source and probability tangency failure; real-base false-positive control | `NATIVE_PHASE_RESULT.json` |

All six final scripts executed successfully in ordinary and `python -O`
modes with byte-identical JSON. Tests use explicit checks that are not
disabled by optimization. Independent reviewers replayed each lane's
relevant checks; the integrator additionally reran the terminal checker in
both modes after copying it to the final repository path. Exact final script
hashes and observed result hashes are in `MANIFEST.json`; execution details
and source provenance are in `RUN_LOG.json`, `SOURCE_PINS.json`, and
`REVIEW.md`. Files copied from the bounded scratch analyses retain their
reviewed bytes.

Runtime: Python 3.12.14 and SymPy 1.14.0. The environment already supplied
SymPy through a read-only dependency directory; no dependency was installed
or modified. Each checker can be run with Python and SymPy from the repo root:

```bash
python 02_REGISTRY/research/sources/d0_native_final_composition_2026-10-28/check_query_stationarity.py
python 02_REGISTRY/research/sources/d0_native_final_composition_2026-10-28/check_gauge_moment.py
python 02_REGISTRY/research/sources/d0_native_final_composition_2026-10-28/check_retained_memory.py
python 02_REGISTRY/research/sources/d0_native_final_composition_2026-10-28/check_terminal_graph.py
python 02_REGISTRY/research/sources/d0_native_final_composition_2026-10-28/check_phase_descent.py
python 02_REGISTRY/research/sources/d0_native_final_composition_2026-10-28/phase_native_check.py
```

The native checkers pin the existing `native_execution.py` SHA256
`222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c`.
This input is unchanged by the incoming `1d29848f` continuation.

The repository structural validator was executed on the final composed
files after the incoming commit: `python3 tools/validate_repo.py` returned
PASS with zero warnings
(889 claims, 31 assumptions, 58 aliases, 183 formal-support and 918
Lean-closure rows). This is structural validation, not a new Lean execution
or an acceptance of the physical conclusion.

## What these executions do not establish

The all-mode thermal trace and its derivative tails are bounded analytically,
not numerically diagonalized on the huge complete Hodge carrier. Ordinary
floating-point numbers in receipts illustrate exact formulas and rational
bounds; they do not establish the inequalities. The phase checks distinguish
the actually executed finite native preparation from its mathematical
continuous angle/phase extension. Physical admission of those extensions,
a selected normal lapse Hamiltonian and a vanishing HDA residual are not
claimed.

No original full42 solve, full original CAR128 solver, broad historical
replay, new Lean proof, remote CI pass, human peer review, scientific
acceptance or main merge is claimed. No source budget, physical gain, clock
rank or norm is silently transferred between different carriers.
`GR_closed=false`.
