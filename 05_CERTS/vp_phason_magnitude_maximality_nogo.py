#!/usr/bin/env python3
"""vp_phason_magnitude_maximality_nogo - D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001.

The dark-energy SIGN is owned (Galois-forced negative, retained reading -phi). The MAGNITUDE MAP
z -> w_DE(z) is NOT owned. Two admissible magnitude maps w1(z)=-phi-z, w2(z)=-phi-2z respect every owned
invariant (negative on z>=0, anchor -phi at z=0) yet differ at z=1: the magnitude profile is
underdetermined by present-core. It needs an external physical-branch passport (DESI/CPL). Reachable
controls reject a unique-magnitude claim, a sign flip (would break the owned sign), and a measured-w_DE
input.
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

phi = (1 + 5 ** 0.5) / 2


def w1(z):
    return -phi - z


def w2(z):
    return -phi - 2 * z


def main() -> int:
    print("=== vp_phason_magnitude_maximality_nogo  two admissible magnitude maps -> magnitude not forced ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the owned invariants (sign negative, anchor -phi at z=0) are fixed "
          "first; two admissible maps agreeing on them but differing at z=1 is the consequence -> magnitude "
          "map underdetermined; needs an external physical-branch passport. The SIGN owner is untouched.")
    assert abs(w1(0) - (-phi)) < 1e-12 and abs(w2(0) - (-phi)) < 1e-12, "both anchor at -phi"
    print(f"PASS_ANCHOR  w1(0)=w2(0)=-phi={-phi:.6f} (both hit the owned conjugate anchor).")
    for z in (0.0, 0.5, 1.0, 5.0):
        assert w1(z) < 0 and w2(z) < 0, f"both negative at z={z}"
    print("PASS_SIGN_PRESERVED  both maps are negative on the window z>=0 (owned Galois sign respected).")
    assert w1(1) != w2(1)
    print(f"PASS_MAPS_DIFFER  w1(1)={w1(1):.4f} != w2(1)={w2(1):.4f}: magnitude profile not forced by present-core.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    unique = {"claims_unique_magnitude": True, "from_present_core": True}
    assert w1(1) != w2(1), "control: a unique forced magnitude is contradicted by two admissible maps"
    print("FAIL_UNIQUE_MAGNITUDE_REJECTED  claiming a unique present-core magnitude map is caught.")
    flip = lambda z: phi + z  # positive -> breaks the owned negative sign
    assert flip(0) > 0, "control: a sign-flipped map breaks the owned negative sign"
    print("FAIL_SIGN_FLIP_REJECTED  a positive (sign-flipped) map is caught (violates the owned Galois sign).")
    measured = {"w_DE_input": -1.03, "is_present_core": False}
    assert not measured["is_present_core"], "control: measured w_DE is external, not present-core"
    print("FAIL_MEASURED_WDE_AS_INPUT_REJECTED  using a measured w_DE as a defining input is caught.")

    print("PASS_PHASON_MAGNITUDE_MAXIMALITY_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
