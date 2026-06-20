#!/usr/bin/env python3
"""vp_vnext_quantum_metric_no_overclaim - block quantum-metric overclaim (negation-aware).

Scans the books for forbidden affirmative overclaims: D0 has a smooth manifold; D0 has a canonical
continuum metric; Connes reconstruction from finite stages alone. Honest negated disclaimers pass.
"""
import pathlib, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
FORBIDDEN = ["d0 now has a smooth manifold", "d0 has a smooth manifold", "canonical continuum metric",
             "primitive smooth manifold", "connes reconstruction from finite stages",
             "smooth manifold in core"]
NEG = ("no ", "not ", "never ", "without ", "n't ", "does not ", "is not ", "are not ", "no primitive ")
def hits(prose):
    out, low = [], prose.lower()
    for p in FORBIDDEN:
        for m in re.finditer(re.escape(p), low):
            if not any(n in low[max(0, m.start() - 40):m.start()] for n in NEG):
                out.append(p); break
    return out
def main() -> int:
    print("=== vp_vnext_quantum_metric_no_overclaim  no smooth-manifold / continuum-metric overclaim ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the AF tower is FORMALISM; no affirmative smooth-manifold/continuum-"
          "metric overclaim may appear in the books. Scan is NEGATION-AWARE.")
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))
    h = hits(prose)
    assert not h, f"affirmative quantum-metric overclaim(s): {h}"
    print("PASS_NO_OVERCLAIM  no affirmative smooth-manifold / continuum-metric overclaim in the books.")
    assert hits("D0 now has a smooth manifold and a canonical continuum metric.")
    print("FAIL_OVERCLAIM_CAUGHT  a planted 'smooth manifold / continuum metric' overclaim is caught.")
    assert not hits("D0 does not have a smooth manifold; there is no canonical continuum metric.")
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")
    print("PASS_VNEXT_QUANTUM_METRIC_NO_OVERCLAIM")
    return 0
if __name__ == "__main__": raise SystemExit(main())
