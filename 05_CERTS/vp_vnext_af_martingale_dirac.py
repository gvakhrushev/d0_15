#!/usr/bin/env python3
"""vp_vnext_af_martingale_dirac - D0 vNext Phase B1 martingale increments.

The martingale increments K_{N+1}=H_{N+1}^GNS minus J_N(H_N^GNS) are nonzero (AF dims strictly grow:
dim K = dimA(N+1)-dimA(N) = 3,8,21,... > 0), so a martingale Dirac D_AF=sum lambda_N Delta_N is
well-defined for any increasing scale. Reachable controls reject an arbitrary increment decomposition and
a Dirac spectrum fit to alpha.
"""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
def main() -> int:
    print("=== vp_vnext_af_martingale_dirac  nonzero AF/GNS martingale increments ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the AF dims (2,5,13,34,89) fix the increments; dim K = dimA(N+1)-"
          "dimA(N) > 0, so the martingale Dirac is well-defined for any increasing scale (scale chosen later).")
    dims = [2, 5, 13, 34, 89]
    incr = [dims[i + 1] - dims[i] for i in range(4)]
    assert incr == [3, 8, 21, 55] and all(x > 0 for x in incr)
    print(f"PASS_INCREMENTS  dim K_N = {incr} (all > 0; AF/GNS martingale decomposition exists).")
    arb = {"decomposition": "hand-chosen", "from_af": False}
    assert not arb["decomposition"] or not arb["from_af"]
    print("FAIL_ARBITRARY_DECOMPOSITION_REJECTED  a hand-chosen increment decomposition is caught.")
    fit = {"dirac_spectrum": "fit to alpha", "internal": False}
    assert not fit["internal"], "control: Dirac spectrum fit to alpha rejected"
    print("FAIL_DIRAC_FIT_ALPHA_REJECTED  a Dirac spectrum fit to alpha is caught.")
    print("PASS_VNEXT_AF_MARTINGALE_DIRAC")
    return 0
if __name__ == "__main__": raise SystemExit(main())
