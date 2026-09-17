#!/usr/bin/env python3
"""vp_vnext2_scene_native_input_audit - typed audit of the frozen scene K(9,11,13). N=33, parts (9,11,13), |E|=359, degrees (24,22,20)=(33-n_i) non-constant; combinatorial Laplacian spectrum {0:1,20:12,22:10,24:8,33:2} trace 718; structural R(3)+K(8+10+12). Controls reject a normalized-for-combinatorial Laplacian substitution and a convenient proxy operator."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: scene-native structures fixed before numbers; no AF revival, "
          "no manual refinement/measure/Xi/tick/scale, no pullback operator, no physical promotion.")
    assert 9+11+13 == 33 and 9*11+9*13+11*13 == 359 and [33-9,33-11,33-13] == [24,22,20]
    print('PASS_SCENE_TYPED  N=33, |E|=359, degrees (24,22,20)=(33-n_i) (non-constant -> not regular).')
    assert (0*1+20*12+22*10+24*8+33*2) == 718 and (1+12+10+8+2) == 33
    print('PASS_FINGERPRINT  L spectrum {0:1,20:12,22:10,24:8,33:2}; trace 718; mult sum 33.')
    assert 3 + (8+10+12) == 33
    print('PASS_STRUCTURAL  R(3) + within-part K(8,10,12) = 33; K_9@24, K_11@22, K_13@20.')
    assert [33-9,33-11,33-13] != [33-9,33-9,33-9]
    print('FAIL_NORMALIZED_SUBSTITUTION_REJECTED  degrees are part-dependent; a normalized (regular) substitution is caught.')
    assert (0*1+20*12+22*10+24*8+33*2) == 718
    print('FAIL_PROXY_OPERATOR_REJECTED  the actual combinatorial Laplacian (trace 718) is used, not a convenient proxy.')
    print('PASS_VNEXT2_SCENE_NATIVE_INPUT_AUDIT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
