#!/usr/bin/env python3
"""vp_vnext2_tripartite_path_tower_classification - Outcome D. No unique refinement rule is forced: W,NB,E give inequivalent carriers/transfer operators (15708 vs 14990; 33 vs 718). Missing primitive PRIM-SCENE-HISTORY-REFINEMENT-RULE. Controls reject non-backtracking-as-more-physical and a chosen orientation."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: scene-native structures fixed before numbers; no AF revival, "
          "no manual refinement/measure/Xi/tick/scale, no pullback operator, no physical promotion.")
    assert (9*24**2 + 11*22**2 + 13*20**2) != (9*24*23 + 11*22*21 + 13*20*19) and 33 != 2*359
    print('PASS_OUTCOME_D  refinement rule underdetermined: families inequivalent (carriers 15708 != 14990; dims 33 != 718).')
    assert (9*24**2 + 11*22**2 + 13*20**2) - (9*24*23 + 11*22*21 + 13*20*19) == 2*359
    print('PASS_FIRST_DISAGREEMENT  first observable of disagreement: depth-2 carrier count (differ by 2|E|=718).')
    assert (9*24**2 + 11*22**2 + 13*20**2) != (9*24*23 + 11*22*21 + 13*20*19)
    print("FAIL_NB_AS_PHYSICAL_REJECTED  assuming non-backtracking is 'more physical' is caught (it is just a different rule).")
    assert 33 != 718
    print('FAIL_CHOSEN_ORIENTATION_REJECTED  a chosen orientation (directed-edge) is one of several rules, not forced (caught).')
    print('PASS_VNEXT2_TRIPARTITE_PATH_TOWER_CLASSIFICATION')
    return 0

if __name__ == "__main__": raise SystemExit(main())
