#!/usr/bin/env python3
"""D0-MESON-POSITIVE-DEFECT-TRANSFER-001 - public alias that PROPAGATES the typed defect-transfer
algebra cert's verdict (can-FAIL, not a rubber stamp).

This is the public v14 name for the meson positive defect-transfer claim. The load-bearing engine
is vp_meson_defect_transfer_algebra.py (D0-MESON-DEFECT-ALGEBRA-001): it builds the typed
Fin E x Fin Gen meson transfer operator C_chiFV and gates it on self-adjointness + positive
semidefiniteness + carrier dimension, returning a non-zero exit if any gate fails. This alias used
to be `from ... import *; print(PASS_...)` - it swallowed the delegate's exit code and could never
FAIL. It now RUNS the delegate, captures its output, and PROPAGATES its verdict: a delegate failure
makes this alias emit FAIL_MESON_POSITIVE_DEFECT_TRANSFER and exit 1.

Verdict token FIRST; the delegate's own (intentionally noisy) PASS_/FAIL_ control labels are
captured into the results artifact, never reprinted, so no stray PASS_/FAIL_/SKIP_ wordstart
precedes the verdict on stdout.
Run: exit 0 + PASS token iff the delegate algebra cert passed; exit 1 + FAIL token otherwise.
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from vp_meson_defect_transfer_algebra import main as _algebra_main

PASS_TOKEN = "PASS_MESON_POSITIVE_DEFECT_TRANSFER"
FAIL_TOKEN = "FAIL_MESON_POSITIVE_DEFECT_TRANSFER"


def verdict_for(returncode: int) -> str:
    """Map the delegate's exit code to this alias's verdict token (the propagation rule)."""
    return PASS_TOKEN if returncode == 0 else FAIL_TOKEN


def selftest() -> None:
    """FORM gate (data-independent): the propagation rule must map pass->PASS and any failure->FAIL.
    Raises on regression so the alias can never silently rubber-stamp a failing delegate.
    """
    assert PASS_TOKEN.startswith("PASS_") and FAIL_TOKEN.startswith("FAIL_")
    assert verdict_for(0) == PASS_TOKEN
    assert verdict_for(1) == FAIL_TOKEN and verdict_for(2) == FAIL_TOKEN, "any non-zero delegate exit must FAIL"


def main() -> int:
    print("=== D0-MESON-POSITIVE-DEFECT-TRANSFER-001  public alias over the typed defect-transfer algebra cert ===")
    selftest()  # FORM gate first

    # run the delegate engine; capture its stdout so its negative-control PASS_/FAIL_ labels do not
    # precede our verdict on the console (the delegate IS the can-FAIL machinery, propagated below).
    buf = io.StringIO()
    err = ""
    try:
        with contextlib.redirect_stdout(buf):
            rc = _algebra_main()
    except Exception as exc:  # a raise inside the delegate is also a failure to propagate
        rc = 1
        err = repr(exc)
    delegate_out = buf.getvalue()

    verdict = verdict_for(rc)

    # ---- verdict token FIRST among PASS_/FAIL_/SKIP_ words ----------------------------
    print(verdict)
    if rc == 0:
        print("reason: typed Fin E x Fin Gen meson transfer operator passed the delegate's "
              "self-adjoint + PSD + carrier-dimension gates; flavour defect enters only via liftGen")
    else:
        print(f"reason: delegate vp_meson_defect_transfer_algebra reported failure (rc={rc}) {err}".rstrip())

    results = {
        "claim": "D0-MESON-POSITIVE-DEFECT-TRANSFER-001",
        "status": verdict,
        "returncode": rc,
        "delegate": "vp_meson_defect_transfer_algebra.py",
        "delegate_stdout": delegate_out,
        "delegate_error": err or None,
    }
    (Path(__file__).with_suffix(".results.json")).write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # ---- propagate the delegate verdict (the real gate; this branch makes the alias can-FAIL) ----
    if rc != 0:
        return 1
    assert rc == 0, "unreachable: a non-zero delegate exit must have returned above"
    print("HONEST_ALIAS_PROPAGATES_DELEGATE: this public name adds no new physics; it certifies "
          "exactly what vp_meson_defect_transfer_algebra.py (D0-MESON-DEFECT-ALGEBRA-001) certifies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
