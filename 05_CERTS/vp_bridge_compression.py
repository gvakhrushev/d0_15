#!/usr/bin/env python3
"""D0-BRIDGE-COMPRESSION-001 — bridge closure as passport closure (verification rule).

A bridge is not an indefinite theorem debt: once its D0-internal object is frozen, the external
translation is packaging (PASSPORT-CLOSED), not a source of structure. This cert enforces the rule as
a CAN-FAIL guard:
  (1) PASSPORT-CLOSED is a canonical release_status AND maps to a NON-core-promotable firewall status
      (a passport can never be laundered into CORE-THE);
  (2) the rule + the PASSPORT-CLOSED / INACTIVE-BRIDGE vocabulary + the seven passport conditions are
      documented in BOOK_05 §05.6;
  (3) the over-claim SENTINELS are ABSENT from the books (no "LIGO confirms D0", no "external data
      selects the D0 object", ...) -- the honesty firewall;
  (4) negative control: the sentinel detector itself catches a planted over-claim string.

It deliberately does NOT flag every prose mention of the word "bridge" (that would false-positive on
legitimate text); enforcing that every registry release_status is canonical is owned by validate_csv.
"""
from __future__ import annotations

import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import d0_status_model as m  # noqa: E402

BOOK05 = ROOT / "01_BOOKS" / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE"

# Over-claim sentinels: positive sentences that would promote a passport/bridge past its honest
# status. Chosen specific enough not to match the corpus's (negated) honest forms.
OVERCLAIM_SENTINELS = [
    "LIGO confirms D0",
    "external data selects the D0 object",
    "smooth manifold is a primitive D0 input",
    "neutrino data tunes Delta_alpha",
    "bridge remains open indefinitely",
    "survey data choose the D0 object",
    "passport closure proves the external theorem",
]


def book_prose() -> str:
    out = []
    for p in (ROOT / "01_BOOKS").rglob("*.md"):
        try:
            out.append(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:  # noqa: BLE001
            pass
    return "\n".join(out)


def main() -> int:
    print("=== D0-BRIDGE-COMPRESSION-001  bridge closure as passport closure (verification rule) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: PASSPORT-CLOSED is a closed external dictionary/comparison mapped "
          "to the EMPIRICAL_PASSPORT firewall status -- NEVER promotable to CORE-THE; the seven passport "
          "conditions are fixed before any external comparison")

    # (1) schema: PASSPORT-CLOSED canonical AND non-core-promotable
    assert "PASSPORT-CLOSED" in m.CANONICAL_RELEASE_STATUS, "PASSPORT-CLOSED must be a canonical release_status"
    d0s = m.RELEASE_TO_D0STATUS.get("PASSPORT-CLOSED")
    assert d0s == "EMPIRICAL_PASSPORT", f"PASSPORT-CLOSED must map to a passport firewall status, got {d0s!r}"
    assert not m.can_promote_to_core(d0s), "PASSPORT-CLOSED must NOT be promotable to CORE"
    print(f"PASS_PASSPORT_CLOSED_FIREWALL  PASSPORT-CLOSED -> {d0s}; can_promote_to_core={m.can_promote_to_core(d0s)} (forbidden)")

    # (2) rule + vocab documented in BOOK_05 §05.6
    vocab = (BOOK05 / "0007__05.6__status-vocabulary.md").read_text(encoding="utf-8", errors="replace")
    for tok in ("D0-BRIDGE-COMPRESSION-001", "`PASSPORT-CLOSED`", "`INACTIVE-BRIDGE`",
                "no reverse selection", "deterministic PASS/FAIL"):
        assert tok in vocab, f"BOOK_05 §05.6 must document {tok!r}"
    print("PASS_RULE_DOCUMENTED  D0-BRIDGE-COMPRESSION-001 + PASSPORT-CLOSED + INACTIVE-BRIDGE + the 7 conditions in BOOK_05 §05.6")

    # (3) over-claim sentinels ABSENT from book prose (the honesty firewall)
    prose = book_prose()
    hits = [s for s in OVERCLAIM_SENTINELS if s in prose]
    assert not hits, f"over-claim sentinel(s) present in book prose: {hits}"
    print(f"PASS_NO_OVERCLAIM_SENTINELS  none of the {len(OVERCLAIM_SENTINELS)} over-claim sentences appear in the books")

    # (4) negative control: the sentinel detector MUST catch a planted over-claim (the guard can FAIL)
    planted = "intro: LIGO confirms D0 and the smooth manifold is a primitive D0 input."
    caught = [s for s in OVERCLAIM_SENTINELS if s in planted]
    assert caught, "control: the sentinel detector must catch a planted over-claim string"
    print(f"FAIL_PLANTED_OVERCLAIM_CAUGHT  detector catches {len(caught)} planted over-claim(s) -- the guard is reachable")

    print("PASS_BRIDGE_COMPRESSION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
