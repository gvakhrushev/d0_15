#!/usr/bin/env python3
"""vp_high_priority_no_false_empirical_claim - no false empirical claim in the books (negation-aware)."""
import pathlib, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
FORBIDDEN = ["echo detected", "echo is detected", "ligo confirms d0", "desi confirms d0", "alpha is derived",
             "n_s is predicted", "higgs vev is derived", "smooth manifold is proved", "all high-priority fronts closed"]
NEG = ("no ", "not ", "never ", "without ", "does not ", "is not ", "are not ", "do not ", "would ", "if ")
def hits(prose):
    o, low = [], prose.lower()
    for p in FORBIDDEN:
        for m in re.finditer(re.escape(p), low):
            if not any(n in low[max(0, m.start()-40):m.start()] for n in NEG): o.append(p); break
    return o
def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the echo is a falsifier passport, no physics derived; no affirmative "
          "empirical-confirmation phrase may appear. Scan is NEGATION-AWARE.")
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))
    h = hits(prose); assert not h, f"false empirical claim(s): {h}"
    print("PASS_NO_FALSE_EMPIRICAL  no affirmative empirical-confirmation overclaim in the books.")
    assert hits("LIGO confirms D0 and the echo is detected")
    print("FAIL_FALSE_EMPIRICAL_CAUGHT  a planted empirical-confirmation overclaim is caught.")
    assert not hits("the echo is not detected; LIGO does not confirm D0")
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")
    print("PASS_HIGH_PRIORITY_NO_FALSE_EMPIRICAL_CLAIM")
    return 0

if __name__ == "__main__": raise SystemExit(main())
