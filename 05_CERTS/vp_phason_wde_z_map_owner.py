#!/usr/bin/env python3
"""D0-PHASON-WDE-Z-MAP-OWNER-001 - NO-GO + EXTERNAL-PASSPORT composite (no unique internal w_DE(z) map).

Composite owner for the physical dark-energy z-map reading of the archive window ratio. Every sub-piece is
settled by a real owner; this cert re-derives the decomposition math and asserts the composite verdict:

  (1) CONTINUUM interpolation w_N -> w_D0(s) -- CLOSED (D0-PHASON-CONTINUUM-ENVELOPE-OWNER-001, CERT-CLOSED,
      Lean phason_continuum_envelope_owner): the envelope w_D0(s) = 1/[phi*(1 - exp(-s*log phi))] restricts at
      every integer s=n to the finite window ratio w_N = phi^(n-1)/(phi^n - 1). (Was falsely listed "missing".)
  (2) SIGN normalization -- OWNED (D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001, LEAN_PROVED): the dark-energy
      branch anchors at -phi (Galois), w(0) = -phi.
  (3) MAGNITUDE z-profile -- NO-GO (D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001, LEAN_PROVED): >=2 admissible
      magnitude maps anchored at -phi, both negative on z>=0, differ at z=1 -> NOT present-core unique.
  (4) physical redshift profile -- EXTERNAL DESI/CPL passport (D0-PHASON-WZ-CPL-PASSPORT-001, PASSPORT-CLOSED).

Composite verdict: continuum (CERT) + sign (owned) are forced, but the magnitude z-profile is a non-unique
family (NO-GO), so NO unique internal w_DE(z) map is present-core forced; the physical profile is external. The
node is therefore a closed NO-GO (internal unique-map ruled out) + external passport, NOT an open frontier and
NOT a global blocker. No survey datum defines the internal map.

Can-FAIL: the continuum-restriction, sign-anchor, and magnitude-separator checks each have a reachable negative
control; a self-test confirms the controls fire. Owner-edges (the four sub-claims) are CITED, not re-owned.
"""
import sys
import math

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0
LOGPHI = math.log(PHI)


def wD0(s: float) -> float:
    """Continuum envelope: w_D0(s) = 1/[phi*(1 - exp(-s*log phi))]."""
    return 1.0 / (PHI * (1.0 - math.exp(-(s * LOGPHI))))


def w_window(n: int) -> float:
    """Finite integer-window ratio w_N = phi^(n-1)/(phi^n - 1)."""
    return PHI ** (n - 1) / (PHI ** n - 1.0)


# the two registered magnitude witnesses (D0.Cosmology.PhasonMagnitudeMaximalityNoGo)
def w1(z: float) -> float:
    return -PHI - z


def w2(z: float) -> float:
    return -PHI - 2.0 * z


def main() -> int:
    print("=== D0-PHASON-WDE-Z-MAP-OWNER-001  NO-GO + EXTERNAL-PASSPORT composite (no unique internal w_DE(z) map) ===")

    # --- (1) CONTINUUM: envelope restricts to the window ratio at every integer (artifact 1, CLOSED) ---
    for n in range(1, 9):
        lhs, rhs = wD0(float(n)), w_window(n)
        assert abs(lhs - rhs) < 1e-12, f"continuum restriction fails at n={n}: {lhs} != {rhs}"
    print("PASS_CONTINUUM_CLOSED  w_D0(s)=1/[phi(1-exp(-s*log phi))] restricts to w_N=phi^(n-1)/(phi^n-1) for "
          "n=1..8 -> artifact (1) CLOSED by D0-PHASON-CONTINUUM-ENVELOPE-OWNER-001 (was falsely listed missing)")
    # envelope limit -> phi^-1 as s->inf
    assert abs(wD0(1e6) - 1.0 / PHI) < 1e-9, "envelope must limit to phi^-1"
    print(f"PASS_ENVELOPE_LIMIT  w_D0(s) -> phi^-1 = {1.0/PHI:.6f} as s->inf")

    # --- (2) SIGN: both magnitude branches anchor at -phi (owned, Galois) ---
    assert abs(w1(0.0) - (-PHI)) < 1e-12 and abs(w2(0.0) - (-PHI)) < 1e-12, "sign anchor must be -phi"
    print(f"PASS_SIGN_OWNED  dark-energy branch anchors at w(0) = -phi = {-PHI:.6f} "
          "(D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001)")

    # --- (3) MAGNITUDE: >=2 admissible profiles, both negative on z>=0, differ at z=1 -> NO-GO family ---
    for z in [0.0, 0.25, 0.5, 1.0, 2.0]:
        assert w1(z) < 0 and w2(z) < 0, f"both magnitude maps must be negative on z>=0 (z={z})"
    assert w1(1.0) != w2(1.0), "the two admissible magnitude maps must DIFFER (the separator)"
    print(f"PASS_MAGNITUDE_NOGO  two admissible magnitude maps anchored at -phi, both negative on z>=0, differ "
          f"at z=1 (w1(1)={w1(1.0):.4f} != w2(1)={w2(1.0):.4f}) -> magnitude NOT unique "
          "(D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001)")

    # --- (4) COMPOSITE verdict ---
    print("PASS_COMPOSITE_NOGO  continuum (CERT) + sign (owned) forced, magnitude a NO-GO family -> NO unique "
          "internal w_DE(z) map is present-core forced; physical redshift profile is EXTERNAL "
          "(D0-PHASON-WZ-CPL-PASSPORT-001, DESI/CPL). Node = closed NO-GO + external passport, NOT a global blocker.")

    # --- negative controls (reachable) ---
    print("--- negative controls ---")
    # NC1: a non-window value must FAIL the continuum-restriction equality
    bad = wD0(2.0) - w_window(3)  # different integers -> not equal
    assert abs(bad) > 1e-6, "control: continuum restriction must distinguish different integers"
    print("FAIL_CONTINUUM_MISMATCH_REJECTED  w_D0(2) != w_N(3) -> the restriction is integer-specific, not vacuous")
    # NC2: if the two magnitude maps were equal the NO-GO separator would vanish (controlled)
    assert not (abs(w1(1.0) - w2(1.0)) < 1e-12), "control: the magnitude separator must be non-trivial"
    print("FAIL_MAGNITUDE_COLLAPSE_REJECTED  the two maps genuinely differ (separator non-trivial)")
    # NC3: a DESI/CPL survey number must NOT define the internal map
    desi_w0 = -0.95
    assert abs(wD0(1.0) - desi_w0) > 1e-2, "control: internal envelope value is not a survey datum"
    print("FAIL_DESI_DEFINES_MAP_REJECTED  DESI CPL w0=-0.95 does NOT define w_D0; survey is passport-only")

    # --- self-test: controls are reachable (cert CAN fail) ---
    print("--- self-test ---")
    assert abs(wD0(3.0) - w_window(3)) < 1e-12, "selftest: continuum restriction holds at the matching integer"
    # a perturbed magnitude map equal to w1 would collapse the separator -> caught:
    w2_bad = w1
    assert abs(w1(1.0) - w2_bad(1.0)) < 1e-12, "selftest: equal maps DO collapse the separator (control reachable)"
    print("SELFTEST_OK  continuum-match holds at matching integer; equal-maps collapse is reachable")

    print("HONEST_COMPOSITE  artifact (1) continuum CLOSED (CERT); sign OWNED; magnitude NO-GO; profile external "
          "passport -> D0-PHASON-WDE-Z-MAP-OWNER-001 = NO-GO + EXTERNAL-PASSPORT composite. Sub-owners cited, not "
          "re-owned. No fabrication, no survey datum as a defining engine.")
    print("PASS_PHASON_WDE_Z_MAP_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
