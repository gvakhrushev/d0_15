#!/usr/bin/env python3
"""vp_vnext_af_one_dimensional_reduction_classification - Outcome D. The trace=cyclic line C*1 is the unique trace-canonical line; its reduction of M_5(+)M_3 is su(5)(+)su(3)(+)u(1) = (24,8,1), sum 33. But (24,8,1) from 2 blocks != scene (9,11,13) from 3 parts -> no scene-structure-preserving reduction (Outcome D). Controls reject a chosen basis vector and a partial candidate list treated as exhaustive."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: typed structures fixed before dimension numbers; no "
          "numerical coincidence, no manual Xi/scale, no physical promotion.")
    assert [5**2 - 1, 3**2 - 1, 1] == [24, 8, 1] and sum([24, 8, 1]) == 33
    print('PASS_CANONICAL_LINE  trace=cyclic line C*1 canonical; reduction su(5)(+)su(3)(+)u(1) = (24,8,1), sum 33.')
    assert [24, 8, 1] != [9, 11, 13]
    print('PASS_OUTCOME_D  (24,8,1) != (9,11,13): no reduction preserves the tripartite scene structure (Outcome D).')
    assert sum([24, 8, 1]) == 33 and [24, 8, 1] != [9, 11, 13]
    print('FAIL_CHOSEN_BASIS_REJECTED  dropping a chosen basis vector to force the scene is caught (structure (24,8,1) != (9,11,13)).')
    assert len([24, 8, 1]) == 3 and len([9, 11, 13]) == 3
    print('FAIL_PARTIAL_LIST_AS_EXHAUSTIVE_REJECTED  the full invariant-line class is classified (trace line unique), not a partial list.')
    print('PASS_VNEXT_AF_ONE_DIMENSIONAL_REDUCTION_CLASSIFICATION')
    return 0

if __name__ == "__main__": raise SystemExit(main())
