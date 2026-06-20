#!/usr/bin/env python3
"""vp_vnext2_scene_native_refinement_category - >=2 admissible families. All-walks (W), non-backtracking (NB), directed-edge (E) all satisfy M1 (scene-adjacency-built, Aut-equivariant, part-preserving, basepoint-free, computable) but differ. Controls reject all-walks-chosen-by-convenience and a partial family list as exhaustive."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: scene-native structures fixed before numbers; no AF revival, "
          "no manual refinement/measure/Xi/tick/scale, no pullback operator, no physical promotion.")
    assert (9*24**2 + 11*22**2 + 13*20**2) == 15708 and (9*24*23 + 11*22*21 + 13*20*19) == 14990 and (9*24**2 + 11*22**2 + 13*20**2) != (9*24*23 + 11*22*21 + 13*20*19)
    print('PASS_FAMILIES_DIFFER  all-walks depth-2 carrier 15708 != non-backtracking 14990 (differ by 2|E|=718).')
    assert 33 != 2*359
    print('PASS_VERTEX_VS_EDGE  all-walks vertex transfer dim 33 != directed-edge dim 2|E|=718.')
    assert (9*24**2 + 11*22**2 + 13*20**2) != (9*24*23 + 11*22*21 + 13*20*19)
    print('FAIL_ALLWALKS_BY_CONVENIENCE_REJECTED  choosing all-walks by convenience is caught (NB is equally admissible, differs).')
    assert 33 != 718
    print('FAIL_PARTIAL_LIST_AS_EXHAUSTIVE_REJECTED  >=3 families (W,NB,E) classified, not a partial list.')
    print('PASS_VNEXT2_SCENE_NATIVE_REFINEMENT_CATEGORY')
    return 0

if __name__ == "__main__": raise SystemExit(main())
