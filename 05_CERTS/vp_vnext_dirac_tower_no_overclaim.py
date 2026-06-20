#!/usr/bin/env python3
"""vp_vnext_dirac_tower_no_overclaim - block vNext grand-overclaim (negation-aware).

Rejects affirmative: D0 now has a smooth manifold; D0 derives alpha from Dixmier trace; D0 predicts n_s;
D0 derives Higgs VEV; D0 has a canonical continuum metric; all vNext fronts closed. Honest negated
disclaimers pass.
"""
import pathlib, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
FORBIDDEN = ["d0 now has a smooth manifold", "derives alpha from dixmier", "d0 derives alpha",
             "d0 predicts n_s", "d0 predicts ns", "derives higgs vev", "d0 derives the higgs vev",
             "canonical continuum metric", "all vnext fronts closed", "all vnext fronts are closed"]
NEG = ("no ", "not ", "never ", "without ", "n't ", "does not ", "is not ", "are not ", "do not ")
def hits(prose):
    out, low = [], prose.lower()
    for p in FORBIDDEN:
        for m in re.finditer(re.escape(p), low):
            if not any(n in low[max(0, m.start() - 40):m.start()] for n in NEG):
                out.append(p); break
    return out
def main() -> int:
    print("=== vp_vnext_dirac_tower_no_overclaim  no vNext grand-overclaim (negation-aware) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: vNext closed the GNS isometry only; no smooth-manifold/alpha/n_s/"
          "Higgs-VEV/continuum-metric/all-closed overclaim may appear. Scan is NEGATION-AWARE.")
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))
    h = hits(prose)
    assert not h, f"affirmative vNext overclaim(s): {h}"
    print("PASS_NO_OVERCLAIM  no affirmative vNext overclaim in the books.")
    assert hits("D0 now has a smooth manifold and derives alpha from Dixmier trace; all vNext fronts closed.")
    print("FAIL_OVERCLAIM_CAUGHT  a planted vNext overclaim is caught.")
    assert not hits("D0 does not derive alpha; D0 does not predict n_s; there is no canonical continuum metric.")
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")
    print("PASS_VNEXT_DIRAC_TOWER_NO_OVERCLAIM")
    return 0
if __name__ == "__main__": raise SystemExit(main())
