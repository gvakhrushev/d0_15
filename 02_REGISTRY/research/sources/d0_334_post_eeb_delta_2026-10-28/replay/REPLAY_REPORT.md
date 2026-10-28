# Replay report for the current #334 continuation

**Source head:** `726192353504a81a9ab2b751f9b6c7866271e75a` (PR #334, still Draft).
**Local runtime:** Python 3.9.6, SymPy 1.14.0, NumPy 2.0.2, SciPy 1.13.1, mpmath 1.3.0. The bundled Python 3.12.14 has NumPy 2.3.5 but lacks SymPy, SciPy and PyTorch.

## Exact-source checks

- `verify_source_delta.py` passed both archive/member mode and `--verify-source-objects`: 70 changed paths, 4,606,489 snapshot bytes, exact base/head commits and decompressed patch. The lossless ZIP and gzip containers keep upstream bytes intact, including source whitespace.
- The nine-package chat intake verifier passed **member bytes only**: 9 packages, 74 files, 650,121 bytes. It explicitly reports `archived_code_executed=false`; the original ZIP bytes and archive SHA remain **not verified**.
- The existing `c296829f` nonlinear source packet verifier passed its pinned-artifact check. In this current-head replay, its nonlinear-dust and AF-word checkers were also executed in both modes: 19 + 24 controls, with stdout byte-identical to the owner JSON.

## Owner checkers in the 34-commit delta

Fourteen of the 17 standalone source checkers ran normally and with `python -O`. All 28 runs exited 0, and every normal/optimized pair produced identical stdout. Ten checker outputs match the pinned owner result byte-for-byte. Four have reproducible floating-point output differences under the local numerical-library versions; their outputs retain `PASS` and the checker thresholds pass. The three skipped scripts import PyTorch, absent from both available Python runtimes.

| Checkers | Local result | Pinned output comparison |
|---|---|---|
| canonical rigidity; closed-history AF embedding, direct source and nonlinear dust; gauge moment; phase descent/native; query stationarity; retained memory; terminal graph | All exited 0 in normal and optimized mode | 10 exact owner-output matches |
| clock winding (261 controls) | `PASS_FULL_CLOCK_WINDING_SOURCE`; normal and optimized identical | One numeric leaf differs: spectral identity error `5.68e-14` locally vs `0` in the pinned output |
| cut boundary | PASS; normal and optimized identical; no stderr | 31 floating-point leaves differ in derivative-error controls |
| full boundary source | PASS; normal and optimized identical | 52 floating-point leaves differ at low precision |
| original retained-history source (163 controls) | `PASS_ORIGINAL_RETAINED_HISTORY_SOURCE`; normal and optimized identical | Environment differs (Python 3.9.6/NumPy 2.0.2 locally vs Python 3.13.5/NumPy 2.3.5 pinned), with 12 environment/numeric leaves differing |
| refoliation closure; QUERY/cut orbit; root boundary | Not replayed | PyTorch unavailable; source and owner receipts are preserved byte-pinned |

RuntimeWarnings from NumPy matrix operations were emitted by the clock-winding, full-boundary and original-history scripts (605, 2,085 and 24,866 stderr bytes respectively). They all exited 0 and returned PASS; the warning logs are retained under `replay/diagnostics/`, with no suppression. The final 7dc checker writes a 1,252-byte validation trace to stderr, not warnings.

## Latest full-price comparison and original moving-projector source

- The exact 7dc checker was extracted from the pinned owner memo only after its source hash matched `b5f46d9c…`, then run in normal and optimized modes. Both runs exited 0; both stdout hashes equal the published receipt SHA-256 `ddff5b91…`. Its result is the scoped positive price contrast for one actual append; it does not refute fixed-duration stationarity.
- The previously integrated moving-projector checker was rerun normal and optimized. Both produce the same local output with `PASS_FULL_BOOTSTRAP_MOVING_CUT`, `moving_cut_control_source=0.06218198611141448`, and `max_fd_error=7.00670077513621e-12`. Nine floating-point fields differ from the pinned result in this NumPy/BLAS environment; stderr contains numerical RuntimeWarnings. The check explicitly reports `native_full42_replayed=false` and `lean_or_ci_run=false`.

## CI and scientific status

At the time of intake, GitHub returned no status/check rows for PR #334 head `7261923`. The latest PR #402 head before this intake was `2f57d930`; its [D0 guards](https://github.com/gvakhrushev/d0_15/actions/runs/40679513224) and [lean-build](https://github.com/gvakhrushev/d0_15/actions/runs/40679512981) checks passed. Those runs predate this intake commit; fresh checks are required on the published intake head. This packet does not claim new PR #334 CI, full42/Lean replay for the new research, physical admission, independent scientific acceptance or GR closure.

`REPLAY_RECEIPT.json` records per-mode exit codes, stdout hashes, owner comparisons and the runtime. The mismatching local outputs and captured stderr are preserved in `diagnostics/`; matching outputs are already present in the source snapshot.
