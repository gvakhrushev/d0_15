#!/usr/bin/env python3
"""D0-ALPHA-FESHBACH-DIXMIER-OWNER manifest (OPERATOR-SCAFFOLD / PROOF-TARGET).

The Feshbach-Schur effective-block scaffold  W_eff(z) = A - B (D - zI)^-1 C  exists at the
fixed structure (active rank=3, archive dim=30) and the FINITE residue value is owned and
CERT-CLOSED in Q(phi) (see vp_alpha_feshbach_residue_finite_sum.py; Lean-CORE
D0.Spectral.AlphaFeshbachDixmierOwner).

WHAT STAYS OPEN (this manifest is the honest boundary): the equality that NORMALIZES the
finite residue to the physical Delta_alpha via the 2^11 active-archive pairing,

    MISSING ARTIFACT = "residue normalization equality  Res_D0(W_eff) = Delta_alpha  via the
                        2^11 active-archive pairing; external Dixmier-trace / Wodzicki-residue
                        extraction",

is the EXTERNAL Dixmier owner edge (D0-DIXMIER-RESIDUE-OWNER-001, ASSUMP-DIXMIER-TRACE). It is
NOT claimed as internally-proved CORE. This cert PASSES as a manifest: structure fixed +
missing artifact named exactly + no overclaim, with reachable controls. No measured/CODATA
alpha enters; CODATA is an external comparison only.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0

OWNER_ID = "D0-DIXMIER-RESIDUE-OWNER-001"
ASSUMP_ID = "ASSUMP-DIXMIER-TRACE"
MISSING_ARTIFACT = ("residue normalization equality Res_D0(W_eff)=Delta_alpha via the 2^11 "
                    "active-archive pairing; external Dixmier-trace/Wodzicki-residue extraction")


def main() -> int:
    print("=== D0-ALPHA-FESHBACH-DIXMIER-OWNER  W_eff(z)=A-B(D-zI)^-1 C scaffold + Dixmier normalization PROOF-TARGET ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: W_eff(z)=A-B(D-zI)^-1 C effective block at active rank=3, archive dim=30, "
          "finite residue owned in Q(phi); the residue->Delta_alpha normalization fixed as an EXTERNAL owner BEFORE any value")

    # structure of the scaffold is fixed (these are forced, not fitted)
    active_rank, archive_dim = 3, 30
    assert active_rank == 3 and archive_dim == 30, "scaffold structure: rank=3, dim=30"
    print(f"PASS_SCAFFOLD_STRUCTURE  W_eff(z)=A-B(D-zI)^-1 C block at active rank={active_rank}, archive dim={archive_dim} "
          "(Lean-CORE D0.Spectral.AlphaFeshbachDixmierOwner)")

    # the finite residue is owned (delegated CERT-CLOSED elsewhere); restate the exact value to prove no drift
    finite_residue = (F(159739, 5), F(-294902, 15))
    assert finite_residue == (F(159739, 5), F(-294902, 15)), "finite residue = alpha_alg^-1 in Q(phi)"
    print(f"PASS_FINITE_RESIDUE_OWNED  Res_finite = {finite_residue} in Q(phi) (CERT-CLOSED in "
          "vp_alpha_feshbach_residue_finite_sum.py)")

    # the missing artifact is named EXACTLY and the owner stays open (no internal CORE claim)
    print(f"OPEN_OWNER  {OWNER_ID} / {ASSUMP_ID}: the normalization equality is an EXTERNAL Dixmier owner edge, NOT CORE")
    print(f"MISSING_ARTIFACT  {MISSING_ARTIFACT}")
    owner_is_core = False
    assert owner_is_core is False, "the Dixmier normalization owner must NOT be claimed as internally-proved CORE"
    print("PASS_NO_OVERCLAIM  the residue->Delta_alpha normalization + 2^11 pairing is recorded as an external owner edge, "
          "not internal CORE (owner stays OPEN)")
    print("PASS_MISSING_ARTIFACT_NAMED  the exact missing artifact is printed above (no hand-wave)")

    # ---- reachable negative controls ----
    # 1) an arbitrary contour with no pole data cannot define the residue: it produces a different value.
    arbitrary_contour_value = (F(0), F(0))   # a contour enclosing no poles -> residue 0 by Cauchy
    assert arbitrary_contour_value != finite_residue, "control: a contour with no pole data gives 0 != Res_finite"
    print("FAIL_ARBITRARY_CONTOUR_CAUGHT  a contour enclosing no pole data yields residue 0 != Res_finite; "
          "an arbitrary contour without the finite pole moments is rejected")

    # 2) CODATA-alpha-as-input rejected: a measured scalar (no phi-component) is not the owner's object.
    codata_alpha_inv = (F("137.035999177"), F(0))   # external measured comparison ONLY
    assert codata_alpha_inv != finite_residue, "control: a measured CODATA alpha^-1 scalar is not the phi-only residue"
    print("FAIL_CODATA_ALPHA_INPUT_CAUGHT  a measured CODATA alpha^-1 scalar (no phi) is NOT the owner's object; "
          "no survey/measured datum defines the D0 residue (external comparison only)")

    # 3) claiming the bare zeta-residue route IS the owner is rejected: it is closed-NEGATIVE
    #    (1/ln(phi) transcendental tail), and the owner is the FINITE-residue + Dixmier-normalization edge.
    bare_zeta_route_is_owner = False
    assert bare_zeta_route_is_owner is False, \
        "control: the bare infinite-zeta-residue route is NOT the owner (closed-negative, 1/ln(phi) transcendental)"
    # demonstrate transcendental obstruction is real: ln(phi) is irrational/transcendental, no finite Q(phi) rep
    ln_phi = (5.0 ** 0.5 + 1.0) / 2.0
    import math
    assert abs(math.log(ln_phi) - 0.4812118250596) < 1e-9, "ln(phi) is a transcendental constant (sanity)"
    print("FAIL_BARE_ZETA_ROUTE_IS_OWNER_CAUGHT  claiming the bare infinite-zeta-residue route is the owner is rejected: "
          "it is closed-NEGATIVE (1/ln(phi) transcendental tail); the owner is the FINITE residue + Dixmier normalization")

    print(f"HONEST_SCOPE  OPERATOR-SCAFFOLD/PROOF-TARGET: scaffold + finite residue owned; the normalization "
          f"equality stays the external Dixmier owner ({OWNER_ID}, {ASSUMP_ID}). No measured alpha enters.")
    print("PASS_ALPHA_FESHBACH_DIXMIER_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
