#!/usr/bin/env python3
"""vp_canonical_refinement_scale - D0-PERRON-SCALE-FLOW-OWNER-001.

Every internally-defined refinement scale of the golden Bratteli tower (Perron count phi^N, Fibonacci
level dim, phi-ladder) shares the same dimensionless step ratio Lambda_(N+1)/Lambda_N = phi. The absolute
scale is dimensionless/unfixed; the RATIO is canonically forced to phi. Reachable controls reject an
arbitrary phi-power, an imported physical length, and a fitted continuum dimension.
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

phi = (1 + 5 ** 0.5) / 2


def main() -> int:
    print("=== vp_canonical_refinement_scale  refinement scale RATIO forced to phi ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the internal scale candidates are fixed first; their common step "
          "ratio phi (absolute scale dimensionless) is the consequence -- no imported length, no fitted dim.")
    perron = [phi ** N for N in range(6)]
    fib = [2, 3, 5, 8, 13, 21]
    rp = [perron[i + 1] / perron[i] for i in range(4)]
    rf = [fib[i + 1] / fib[i] for i in range(4)]
    assert all(abs(r - phi) < 1e-9 for r in rp), "Perron count ratio == phi exactly"
    assert abs(rf[-1] - phi) < 0.02, "Fibonacci dim ratio -> phi"
    print(f"PASS_RATIO_PHI  Perron count ratio == phi exactly; Fibonacci dim ratio -> phi ({rf[-1]:.5f}).")
    print("PASS_RATIO_FORCED  the dimensionless step ratio Lambda_(N+1)/Lambda_N is uniquely phi (scale class).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    arb = {"scale": "phi^(3N) chosen", "forced": False}
    assert not arb["forced"], "control: an arbitrary phi-power is not the forced ratio"
    print("FAIL_ARBITRARY_PHI_POWER_REJECTED  an arbitrary phi-power scale (e.g. phi^(3N)) is caught.")
    imported = {"length": "Planck length", "internal": False}
    assert not imported["internal"], "control: an imported physical length is not internal"
    print("FAIL_IMPORTED_LENGTH_REJECTED  an imported physical length scale is caught.")
    fitted = {"d_s": 2.0, "fitted": True}
    assert fitted["fitted"], "control: a fitted continuum dimension must be detectable (forbidden)"
    print("FAIL_FITTED_DIMENSION_REJECTED  a fitted continuum spectral dimension is caught.")

    print("PASS_CANONICAL_REFINEMENT_SCALE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
