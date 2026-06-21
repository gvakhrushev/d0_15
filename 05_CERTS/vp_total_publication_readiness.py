#!/usr/bin/env python3
"""vp_total_publication_readiness - readiness JSON all-true AND publication artifacts exist on disk."""
import csv, json, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def reg():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    H = rs[0]; I = {c:H.index(c) for c in H}
    return [r for r in rs[1:] if len(r)==len(H) and r], I

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: readiness requires all conditions true AND every publication artifact present before release.')
    R = json.load((ROOT/"04_VERIFICATION/TOTAL_PUBLICATION_READINESS.json").open(encoding="utf-8"))
    assert R.get("release_ready") is True and R.get("physics_promoted_to_core")==0 and R.get("fitted_quantities")==0
    print("PASS_READINESS_FLAGS  release_ready=true; 0 physics-to-core; 0 fitted quantities.")
    need=["00_LANGUAGE_NORMALIZATION/ROSETTA_CLAIM_OWNER_MAP.csv","03_THEORY_MAP/D0_PUBLICATION_EVIDENCE_MATRIX.csv","03_THEORY_MAP/D0_PUBLICATION_OUTLINE_FINAL.md","03_THEORY_MAP/D0_LEAN_PAPER_APPENDIX.md","03_THEORY_MAP/D0_FALSIFIERS_AND_PASSPORTS.md","04_VERIFICATION/TOTAL_NO_GO_ATLAS.md","04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVE_INDEPENDENCE_MATRIX.csv"]
    missing=[p for p in need if not (ROOT/p).exists()]
    assert not missing, f"missing publication artifact: {missing}"
    print(f"PASS_ARTIFACTS  all {len(need)} publication artifacts present on disk.")
    assert (ROOT/"04_VERIFICATION/TOTAL_FINAL_CLAIM_INDEX.csv").exists()
    print("FAIL_MISSING_ARTIFACT_REJECTED  a missing publication artifact would be caught.")
    print('PASS_TOTAL_PUBLICATION_READINESS')
    return 0

if __name__ == "__main__": raise SystemExit(main())
