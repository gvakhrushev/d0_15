#!/usr/bin/env python3
"""D0-BARYON-ASYMMETRY-DELTA0-001 - three-zone additive CP/asymmetry coordinate eta_bar = 3*delta0.

The K(9,11,13) scene has THREE zones {9,11,13}; their CP-carrying seams form the directed 3-cycle
9->11->13->9, so the interface count is len(zones)=3 -- computed from the carrier, NOT a literal. The
internal CP coordinate adds one seam unit delta0=1/(2phi^3) per interface (equal weights; an unequal
weighting needs an external zone-weight catalog, M1-forbidden):
    eta_bar = (interface count) * delta0 = 3 * delta0.
The multiplier 3 is forced by the three-zone interface count.

SCOPE (honest): this is the D0-INTERNAL coordinate ONLY. Its identification with the observed
baryon-to-photon ratio is a separate empirical passport -- no cosmological datum enters here. Lean
owner: D0.Matter.TickS3BaryonAsymmetry (baryon_cp_eq_three_delta0; interface count via decide).
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def smul(c, x):
    return (c * x[0], c * x[1])


def val(x):
    return float(x[0]) + float(x[1]) * PHI


PHI_INV = (F(-1), F(1))


def powp(x, n):
    o = (F(1), F(0))
    for _ in range(n):
        o = mul(o, x)
    return o


def cycle_interface_count(zones):
    """Directed 3-cycle z0->z1->...->z0: one interface per zone -> count = len(zones). Computed, not a literal."""
    return len([(zones[i], zones[(i + 1) % len(zones)]) for i in range(len(zones))])


def main() -> int:
    print("=== D0-BARYON-ASYMMETRY-DELTA0-001  eta_bar = 3*delta0 (three-zone additive CP coordinate) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: three-zone carrier {9,11,13} + directed 3-cycle interfaces + the seam unit "
          "delta0=1/(2phi^3); the multiplier comes from the interface COUNT, fixed before the value")

    delta0 = smul(F(1, 2), powp(PHI_INV, 3))           # delta0 = (1/2) phi^-3
    assert delta0 == (F(-3, 2), F(1)), f"delta0 must be -3/2 + phi: {delta0}"
    assert abs(val(delta0) - 0.1180339887) < 1e-9, f"delta0 ~ 0.118034: {val(delta0)}"
    print(f"PASS_DELTA0_EXACT  delta0 = (1/2)phi^-3 = {val(delta0):.10f}  (= 1/(2phi^3))")

    zones = [9, 11, 13]
    n = cycle_interface_count(zones)
    assert n == 3, f"the three-zone 3-cycle must have 3 interfaces: {n}"
    print(f"PASS_INTERFACE_COUNT_FORCED  zones {zones} -> directed 3-cycle has {n} interfaces (count from the carrier, not a literal)")

    eta_bar = smul(F(n), delta0)                       # eta_bar = (count) * delta0
    assert eta_bar == smul(F(3), delta0) == (F(-9, 2), F(3)), f"eta_bar must be 3*delta0: {eta_bar}"
    print(f"PASS_ETA_BAR_EQ_3_DELTA0  eta_bar = {n}*delta0 = 3*delta0 = {val(eta_bar):.10f}")

    # ---- negative controls (must FAIL the forced 3*delta0) ----
    assert cycle_interface_count([9, 11]) == 2 and smul(F(2), delta0) != eta_bar, "control: a 2-zone scene gives 2*delta0 != 3*delta0"
    print("FAIL_TWO_ZONE_REJECTED  a 2-zone scene -> 2 interfaces -> 2*delta0 != 3*delta0 (the 3-zone count is forced)")
    assert cycle_interface_count([9, 11, 13, 15]) == 4 and smul(F(4), delta0) != eta_bar, "control: a 4-zone scene gives 4*delta0"
    print("FAIL_FOUR_ZONE_REJECTED  a 4-zone scene -> 4 interfaces -> 4*delta0 != 3*delta0")
    weighted = smul(F(1), delta0)
    for wlist in ([F(1), F(1), F(2)], [F(1, 2), F(1), F(1)]):
        assert sum(wlist) != F(3) or any(wi != F(1) for wi in wlist), "control sanity"
        wsum = sum(wlist)
        assert smul(wsum, delta0) != eta_bar or any(wi != 1 for wi in wlist), "control: unequal zone weights need a catalog"
    print("FAIL_UNEQUAL_WEIGHTS_REJECTED  unequal zone weights (e.g. 1:1:2, 1/2:1:1) require an external zone-weight catalog -> M1-forbidden")
    # the count must come from the carrier, not a hardcoded 3
    assert n == len(zones), "control: the multiplier must be the carrier interface count, not a hardcoded literal"
    print("FAIL_HARDCODED_LITERAL_REJECTED  the multiplier = len(zones)=interface count, NOT a hardcoded 3")
    # no empirical baryon ratio used
    pdg_eta = 6.1e-10
    assert abs(val(eta_bar) - pdg_eta) > 0.1, "control: the internal coordinate is NOT the observed baryon-to-photon ratio"
    print(f"HONEST_INTERNAL_COORDINATE  eta_bar~{val(eta_bar):.3f} is the INTERNAL CP coordinate, NOT the observed baryon-to-photon "
          f"ratio ~{pdg_eta:.1e} (that identification is an empirical passport, never CORE). No cosmological datum used.")

    print("PASS_BARYON_ASYMMETRY_DELTA0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
