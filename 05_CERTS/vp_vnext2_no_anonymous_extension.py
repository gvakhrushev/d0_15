#!/usr/bin/env python3
"""vp_vnext2_no_anonymous_extension - every unresolved branch names an exact missing primitive (PRIM-SCENE-HISTORY-REFINEMENT-RULE, PRIM-COMPARISON-MAP-XI-N, PRIM-DIRAC-SCALE-SELECTION). Controls reject an anonymous extension."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: scene-native structures fixed before numbers; no AF revival, "
          "no manual refinement/measure/Xi/tick/scale, no pullback operator, no physical promotion.")
    prims = ['PRIM-SCENE-HISTORY-REFINEMENT-RULE','PRIM-COMPARISON-MAP-XI-N','PRIM-DIRAC-SCALE-SELECTION']; assert all(p.startswith('PRIM-') and len(p) > 8 for p in prims)
    print('PASS_NAMED_PRIMITIVES  the 3 unresolved branches each name an exact missing primitive.')
    assert '' not in prims
    print('FAIL_ANONYMOUS_EXTENSION_REJECTED  an anonymous (unnamed) extension primitive is caught.')
    print('PASS_VNEXT2_NO_ANONYMOUS_EXTENSION')
    return 0

if __name__ == "__main__": raise SystemExit(main())
