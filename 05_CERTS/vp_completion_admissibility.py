#!/usr/bin/env python3
"""vp_completion_admissibility - D0-COMPLETION-ADMISSIBILITY-001. The strengthened 5-item two-completion
standard: a witness is VALID iff (1) class, (2) two completions, (3) separating observable, (4) preserves
owners, (5) exhaustion or universal-property. Items 4 and 5 are NECESSARY. Controls reject a witness missing
item 4 or item 5.
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def valid(w):
    return w["cls"] and w["two"] and w["obs"] and w["owners"] and w["item5"]


def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: validity requires all five items; item 4 (owner preservation) and "
          "item 5 (exhaustion/universal-property) are necessary before any witness counts as a no-go.")
    full = {"cls": True, "two": True, "obs": True, "owners": True, "item5": True}
    assert valid(full)
    print("PASS_FIVE_ITEMS  a witness with all 5 items is valid.")
    assert not valid({**full, "owners": False})
    print("FAIL_ITEM4_MISSING_REJECTED  a witness violating owner-preservation (item 4) is invalid.")
    assert not valid({**full, "item5": False})
    print("FAIL_ITEM5_MISSING_REJECTED  a witness with no exhaustion/universal-property (item 5) is invalid.")
    print("PASS_COMPLETION_ADMISSIBILITY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
