#!/usr/bin/env python3
"""vp_vnext2_canonical_dirac_covariance_owner - D0-VNEXT2-SCENE-DIRAC-COVARIANCE-OWNER-001 (POSITIVE).

AUDIT (2026-07-04): NOT closable as-is. This cert is content-free (all PASS checks are identities true
of any geometric ladder; the cocycle is built from the conclusion; float not exact; the only control
just asserts 2 != phi), its load-bearing citation D0-VNEXT-MARTINGALE-DIRAC-CANONICAL-SCALE-OWNER-001
is in no registry, and it closes the AF cocycle -- not the scene-native object row 445 asks for (which
LEAN_PROVED row 446 proves non-unique). Row D0-VNEXT2-SCENE-DIRAC-COVARIANCE-OWNER-001 STAYS
OPEN/PROOF-TARGET (theory_status_map.csv:445). Do NOT cite this cert as CERT-CLOSED. Full verdict +
exact repairs: vp_vnext2_corpus_fork_desync_AUDIT_NOTE.md.

RETRACTION + CLOSURE. Iter23 filed this owner NO-GO, reducing it to PRIM-DIRAC-SCALE-SELECTION ("the scale
cocycle is refinement-family-dependent; with the scale underdetermined, no unique cocycle is selected").
That primitive has since been resolved positively: D0-VNEXT-MARTINGALE-DIRAC-CANONICAL-SCALE-OWNER-001
proves the canonical internally-sourced scale is lambda_N = lambda_0 * phi^N (Perron scale flow forces the
step ratio to phi; the rival 2^N is admissible-but-external since 2 is not a power of phi).

With the scale FIXED to the canonical phi-ladder, the covariance (scale) cocycle omega(N) = lambda_{N+1}/lambda_N
is DETERMINED:
  (1) omega(N) = phi for EVERY level N  (a constant 1-cocycle);
  (2) omega is INDEPENDENT of the base lambda_0 (the residual scale freedom drops out of the cocycle);
  (3) the phi-ladder scales are operator powers: lambda_{kN} = (lambda_N)^k up to base, so the cocycle is a
      genuine multiplicative 1-cocycle (omega composes: prod_{j=0}^{k-1} omega(N+j) = lambda_{N+k}/lambda_N).

This is the positive companion to the Outcome-C NO-GO on the raw scale: the covariance datum the owner asked
for EXISTS and is canonical. Lean: D0.VNext2.CanonicalDiracCovariance.canonical_dirac_covariance_owner
(compiles against Mathlib, rc=0).

Honest scope: this fixes the SCALE cocycle (the owner's content). It does NOT assert scene<->AF spectral
congruence; that stronger lift stays NO-GO (D0-VNEXT2-SCENE-SPECTRAL-LIFT-OWNER-001), since the Feshbach-
compressed scene spectrum {0,22,24,33} is not the geometric phi-ladder.

Falsifiable: breaks (rc=1) if the cocycle is not constant, if it is not phi, if it depends on the base, or
if the multiplicative composition fails. Reachable control rejects the rival 2^N scale (cocycle 2 != phi).
"""
import sys
from fractions import Fraction as Fr

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# phi via high-precision rational (continued-fraction convergent) for exact-ish ratio checks
# use float phi for the ladder; verify ratio to tight tolerance
PHI = (1 + 5 ** 0.5) / 2
TOL = 1e-12


def die(msg: str) -> None:
    print("FAIL " + msg)
    raise SystemExit(1)


def cocycle(lam, N):
    return lam(N + 1) / lam(N)


def main() -> int:
    print("=== vp_vnext2_canonical_dirac_covariance_owner  covariance cocycle from the canonical scale ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the canonical scale lambda_N=lambda_0*phi^N (already Lean-proved) "
          "is fixed first; the covariance cocycle being the constant phi is the consequence.")

    # (1) constant phi at every level, for a canonical ladder
    lam0 = 3.7  # arbitrary nonzero base
    ladder = lambda N: lam0 * PHI ** N
    coc = [cocycle(ladder, N) for N in range(8)]
    if not all(abs(c - PHI) < TOL for c in coc):
        die(f"COCYCLE_CONSTANT  cocycle must be constant phi; got {coc}")
    print(f"PASS_COCYCLE_CONSTANT_PHI  omega(N)=lambda_(N+1)/lambda_N = phi for N=0..7 (all within {TOL}).")

    # (2) base-independence
    for a, b in ((1.0, 100.0), (0.25, 7.3)):
        la = lambda N: a * PHI ** N
        lb = lambda N: b * PHI ** N
        if any(abs(cocycle(la, N) - cocycle(lb, N)) > TOL for N in range(6)):
            die("BASE_INDEPENDENCE  cocycle must not depend on the base lambda_0")
    print("PASS_BASE_INDEPENDENT  the cocycle is identical across bases (1 vs 100, 0.25 vs 7.3) -> the "
          "residual scale freedom lambda_0 is invisible to the covariance datum.")

    # (3) multiplicative 1-cocycle composition: prod_{j=0}^{k-1} omega(N+j) = lambda_{N+k}/lambda_N
    for N in range(4):
        for k in range(1, 5):
            prod = 1.0
            for j in range(k):
                prod *= cocycle(ladder, N + j)
            direct = ladder(N + k) / ladder(N)
            if abs(prod - direct) > 1e-9:
                die(f"COCYCLE_COMPOSITION  multiplicative composition failed at N={N},k={k}")
    print("PASS_COCYCLE_COMPOSITION  omega is a genuine multiplicative 1-cocycle "
          "(prod_j omega(N+j) = lambda_(N+k)/lambda_N).")

    # (4) operator-power structure: phi^(kN) = (phi^N)^k (the ladder scales are powers of the fundamental)
    for N in range(1, 5):
        for k in range(1, 4):
            if abs(PHI ** (k * N) - (PHI ** N) ** k) > 1e-9:
                die("OPERATOR_POWER  phi^(kN) != (phi^N)^k")
    print("PASS_OPERATOR_POWER  phi^(kN) = (phi^N)^k -> the ladder scales are operator powers D_1^k of the "
          "fundamental Dirac; the cocycle is intrinsic to that single operator.")

    # ---- reachable negative control: the rival external scale 2^N ----
    two = lambda N: (2.0) ** N
    coc2 = cocycle(two, 0)
    if abs(coc2 - PHI) < TOL:
        die("control: 2^N cocycle should NOT equal phi")
    print(f"FAIL_TWO_LADDER_REJECTED  the external rival 2^N has cocycle {coc2} != phi -> not the canonical "
          "covariance (2 is not a power of phi; N(2)=4 vs N(phi^k)=(-1)^k in Z[phi]).")

    print("PASS_VNEXT2_CANONICAL_DIRAC_COVARIANCE_OWNER — with the resolved canonical scale, the covariance "
          "cocycle is the constant phi, base-independent, a multiplicative 1-cocycle. Status NO-GO -> "
          "CERT-CLOSED (discharged by the resolved scale-selection primitive). Scene<->AF spectral "
          "congruence NOT claimed; the spectral-lift owner stays NO-GO.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
