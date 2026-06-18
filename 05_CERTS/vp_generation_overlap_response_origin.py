#!/usr/bin/env python3
"""D0-CKM-NONTRIVIAL-FLAVOUR-ALGEBRA-001 - generation overlap-response origin: public alias that
PROPAGATES the torus-sourced generation selector cert AND independently re-gates its core fact.

The load-bearing engine is vp_generation_selector_origin.py: it derives the generation overlap
response O_ij = |<phase_i|mixed_j>|^2 from finite torus shell geometry and asserts it is
unistochastic, NON-permutation, and gives a PSD flavour-defect response. This alias used to be
`run_certificate(); print(PASS_...)` - it swallowed the delegate's failure machinery and could
never FAIL. It now (1) RUNS the delegate (its asserts raise on any contradiction, captured below)
and (2) INDEPENDENTLY re-derives the overlap response from the same torus geometry and re-checks
the load-bearing invariants. PASS requires BOTH; either failing emits
FAIL_GENERATION_OVERLAP_RESPONSE_ORIGIN and exit 1.

Verdict token FIRST; the delegate's own step labels are captured into the results artifact, never
reprinted, so no stray PASS_/FAIL_/SKIP_ wordstart precedes the verdict on stdout.
Run: exit 0 + PASS token iff delegate AND independent re-gate hold; exit 1 + FAIL token otherwise.
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from vp_generation_selector_origin import (
    is_permutation_matrix,
    run_certificate,
    torus_shell_geometry,
)

PASS_TOKEN = "PASS_GENERATION_OVERLAP_RESPONSE_ORIGIN"
FAIL_TOKEN = "FAIL_GENERATION_OVERLAP_RESPONSE_ORIGIN"
TOL = 1e-9


def overlap_response_from_geometry() -> np.ndarray:
    """Re-derive O_ij = |<phase_i | mixed_j>|^2 from the finite torus shell geometry (independent
    of the delegate's own copy of the computation)."""
    radial, phase, _ = torus_shell_geometry()
    _, u_phase = np.linalg.eigh(phase)
    _, u_mixed = np.linalg.eigh(phase + radial)
    return np.abs(u_phase.conj().T @ u_mixed) ** 2


def overlap_invariants_hold(overlap: np.ndarray) -> bool:
    """The load-bearing facts: O is unistochastic (row + column sums 1) and NOT a permutation
    (i.e. genuine generation mixing). A degenerate geometry that collapsed O to a permutation,
    or broke stochasticity, returns False here."""
    row_ok = bool(np.allclose(overlap.sum(axis=1), 1.0, atol=TOL))
    col_ok = bool(np.allclose(overlap.sum(axis=0), 1.0, atol=TOL))
    nonneg = bool(np.all(overlap >= -TOL))
    nonperm = not is_permutation_matrix(overlap)
    return row_ok and col_ok and nonneg and nonperm


def selftest() -> None:
    """FORM gate (data-independent): the independent re-gate must ACCEPT the true torus overlap and
    the permutation test must not be vacuous. Raises on any regression.
    """
    assert PASS_TOKEN.startswith("PASS_") and FAIL_TOKEN.startswith("FAIL_")
    assert overlap_invariants_hold(overlap_response_from_geometry()), "true torus overlap must pass the re-gate"
    # negative control: a genuine permutation MUST be detected as one (else the non-permutation
    # invariant is vacuous and could rubber-stamp a collapsed overlap)
    assert is_permutation_matrix(np.eye(3)), "permutation detector is vacuous"
    assert not overlap_invariants_hold(np.eye(3)), "a permutation matrix must FAIL the re-gate"


def main() -> int:
    print("=== D0-CKM-NONTRIVIAL-FLAVOUR-ALGEBRA-001  generation overlap-response origin "
          "(alias over the torus generation selector cert) ===")
    selftest()  # FORM gate first

    # (1) run the delegate engine; its asserts raise on any internal contradiction (captured so its
    #     step labels do not precede our verdict on the console).
    buf = io.StringIO()
    err = ""
    try:
        with contextlib.redirect_stdout(buf):
            run_certificate()
        delegate_ok = True
    except Exception as exc:
        delegate_ok = False
        err = repr(exc)
    delegate_out = buf.getvalue()

    # (2) independent re-gate on the SAME torus geometry (negative control in this file)
    overlap = overlap_response_from_geometry()
    regate_ok = overlap_invariants_hold(overlap)

    verdict = PASS_TOKEN if (delegate_ok and regate_ok) else FAIL_TOKEN

    # ---- verdict token FIRST among PASS_/FAIL_/SKIP_ words ----------------------------
    print(verdict)
    if verdict == PASS_TOKEN:
        print("reason: torus shell geometry yields a unistochastic, non-permutation overlap response "
              "with PSD flavour defect (delegate cert + independent re-gate both hold)")
    else:
        print(f"reason: delegate_ok={delegate_ok} regate_ok={regate_ok} {err}".rstrip())

    results = {
        "claim": "D0-CKM-NONTRIVIAL-FLAVOUR-ALGEBRA-001",
        "status": verdict,
        "delegate": "vp_generation_selector_origin.py",
        "delegate_ok": delegate_ok,
        "independent_regate_ok": regate_ok,
        "overlap_row_sums": overlap.sum(axis=1).tolist(),
        "delegate_stdout": delegate_out,
        "delegate_error": err or None,
    }
    (Path(__file__).with_suffix(".results.json")).write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # ---- propagate the verdict (the real gate; makes the alias can-FAIL) --------------
    if verdict != PASS_TOKEN:
        return 1
    assert delegate_ok and regate_ok, "unreachable: a failing verdict must have returned above"
    print("HONEST_ALIAS_PROPAGATES_DELEGATE: this public name adds no new physics; physical CKM "
          "entries remain downstream passport data, not certified here")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
