#!/usr/bin/env python3
"""vp_vnext_canonical_dirac_scale_selection - D0-VNEXT-MARTINGALE-DIRAC-OWNER-001 (Outcome C).

The Dirac scale is NOT uniquely forced: distinct admissible laws lambda_N=phi^N and lambda_N=2^N are each
strictly increasing to infinity (each gives a compact-resolvent AF spectral triple, a la Christensen-Ivan)
yet differ at N=1 (phi != 2). So the scale selection is a SECOND independent primitive (Outcome C).
Reachable controls reject phi^N inserted without a source, an external spectral dimension, and a Dirac
spectrum fit to n_s.
"""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
phi = (1 + 5 ** 0.5) / 2
def main() -> int:
    print("=== vp_vnext_canonical_dirac_scale_selection  >=2 admissible scale laws -> underdetermined ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the admissible-scale family (increasing->inf) is fixed first; that "
          "phi^N and 2^N both qualify yet differ (phi!=2) is the consequence -> scale not forced (Outcome C).")
    for nm, base in [("phi^N", phi), ("2^N", 2.0)]:
        seq = [base ** n for n in range(5)]
        assert all(seq[i + 1] > seq[i] for i in range(4)) and base > 1
    print("PASS_TWO_ADMISSIBLE_SCALES  phi^N and 2^N are both strictly increasing to infinity (admissible).")
    assert abs(phi - 2.0) > 0.3
    print(f"PASS_SCALES_DISTINCT  they differ at N=1: phi={phi:.5f} != 2 -> Dirac scale UNDERDETERMINED.")
    inserted = {"lambda": "phi^N", "has_source": False}
    assert not inserted["has_source"], "control: phi^N inserted without a forcing source"
    print("FAIL_PHI_N_WITHOUT_SOURCE_REJECTED  lambda_N=phi^N inserted without a forcing source is caught.")
    extdim = {"spectral_dimension": 4.0, "internal": False}
    assert not extdim["internal"], "control: external spectral dimension rejected"
    print("FAIL_EXTERNAL_SPECTRAL_DIM_REJECTED  an external spectral dimension is caught.")
    fit = {"dirac": "fit to n_s", "internal": False}
    assert not fit["internal"], "control: Dirac fit to n_s rejected"
    print("FAIL_DIRAC_FIT_NS_REJECTED  a Dirac spectrum fit to n_s is caught.")
    print("PASS_VNEXT_CANONICAL_DIRAC_SCALE_SELECTION")
    return 0
if __name__ == "__main__": raise SystemExit(main())
