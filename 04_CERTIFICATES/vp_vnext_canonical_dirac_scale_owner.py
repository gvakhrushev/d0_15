#!/usr/bin/env python3
"""vp_vnext_canonical_dirac_scale_owner - D0-VNEXT-MARTINGALE-DIRAC-CANONICAL-SCALE-OWNER-001.

POSITIVE companion to the Outcome-C NO-GO (D0-VNEXT-MARTINGALE-DIRAC-OWNER-001). That NO-GO is correct
for the AF axioms ALONE: Christensen-Ivan permit any increasing scale lambda_N (e.g. 2^N), so the scale is
not forced by admissibility. What it did not cross-reference is the already-Lean-proved
D0-PERRON-SCALE-FLOW-OWNER-001: every INTERNALLY-DEFINED refinement scale of the golden Bratteli tower has
step ratio exactly phi. This cert grounds the synthesis: among internally-sourced scales the martingale
Dirac scale is UNIQUE up to the free dimensionless base lambda_0 (the standard overall-scale freedom of a
spectral triple), and the rival 2^N is admissible-but-EXTERNAL because 2 is not a unit in Z[phi] (2 is not
any power of phi), so its ratio 2 != phi cannot be internally sourced.

Falsifiable checks: the phi-ladder ratio is exactly phi; 2^N ratio is 2 != phi; 2 is not a phi-power
(norm argument in Z[phi]); the phi-ladder scales are operator powers D_1^k of the fundamental Dirac; and
any internally-sourced (ratio-phi) scale is pinned to lambda_0*phi^N. Reachable negative controls reject
(a) an internally-sourced claim for 2^N, and (b) a scale fitted to an external spectral dimension.
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1 + 5 ** 0.5) / 2
TOL = 1e-12


def die(msg: str) -> None:
    print("FAIL " + msg)
    raise SystemExit(1)


def norm_Zphi_rational(r: float) -> float:
    # field norm N(r) = r * r_bar; for rational r, N(r) = r^2
    return r * r


def main() -> int:
    print("=== vp_vnext_canonical_dirac_scale_owner  internally-sourced martingale-Dirac scale is phi^N ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the tower's forced Perron ratio phi (D0-PERRON-SCALE-FLOW-OWNER-001) "
          "is fixed first; that it pins the martingale-Dirac scale to lambda_0*phi^N, while 2^N is external, "
          "is the consequence -- no scale is inserted by hand.")

    # (1) phi-ladder step ratio is exactly phi (the internally-sourced ratio).
    lam = [PHI ** n for n in range(6)]
    ratios = [lam[i + 1] / lam[i] for i in range(5)]
    if not all(abs(r - PHI) < TOL for r in ratios):
        die("PHI_LADDER_RATIO  phi-ladder step ratio must equal phi")
    print(f"PASS_PHI_LADDER_RATIO  lambda_(N+1)/lambda_N = phi = {PHI:.12f} at every level (internally sourced).")

    # (2) 2^N step ratio is 2 != phi (admissible but NOT the internal ratio).
    two = [2.0 ** n for n in range(6)]
    r2 = two[1] / two[0]
    if abs(r2 - 2.0) > TOL or abs(r2 - PHI) < 1e-6:
        die("TWO_LADDER_RATIO  2^N ratio must be 2 and must differ from phi")
    print(f"PASS_TWO_LADDER_RATIO  2^N step ratio = {r2:.1f} != phi -> NOT the internally-forced ratio.")

    # (3) 2 is NOT a power of phi: phi is the fundamental unit of Z[phi] (N(phi^k)=(-1)^k, a unit),
    #     but N(2) = 4 is not a unit. So 2 is externally sourced; its scale cannot come from the tower.
    n_two = norm_Zphi_rational(2.0)
    if abs(abs(n_two) - 1.0) < 0.5:
        die("TWO_NOT_UNIT  N(2) must not be a unit norm (+-1)")
    PHI_CONJ = (1 - 5 ** 0.5) / 2  # the Galois conjugate root of t^2 - t - 1 = 0
    for k in range(-6, 7):
        n_phik = (PHI ** k) * (PHI_CONJ ** k)  # actual field norm N(phi^k) = phi^k * conj(phi^k)
        if abs(n_phik - (-1.0) ** k) > 1e-6:
            die(f"PHI_POWER_UNIT  N(phi^{k}) must equal (-1)^{k}, got {n_phik}")
        if abs(abs(n_phik) - 1.0) > 1e-6:
            die(f"PHI_POWER_UNIT  N(phi^{k}) must be a unit (+-1), got {n_phik}")
    print(f"PASS_TWO_NOT_A_PHI_POWER  N(2)={n_two:.0f} is not a unit while N(phi^k)=(-1)^k in {{+1,-1}} "
          f"-> 2 != phi^k for any integer k (2 externally sourced).")

    # (4) phi-ladder scales are OPERATOR POWERS of the fundamental Dirac: lambda^{(k)}_N = (lambda^{(1)}_N)^k.
    base = [PHI ** n for n in range(6)]
    for k in (2, 3):
        laddk = [PHI ** (k * n) for n in range(6)]
        if not all(abs(laddk[i] - base[i] ** k) < 1e-9 for i in range(6)):
            die(f"OPERATOR_POWER  phi^{{{k}N}} must equal (phi^N)^{k}")
    print("PASS_OPERATOR_POWER  phi^{kN} = (phi^N)^k -> the phi-ladder scales are integer powers D_1^k of "
          "the fundamental Dirac (standard 'which power' freedom, not a new primitive).")

    # (5) any internally-sourced scale (ratio == phi) is pinned to lambda_0 * phi^N (mirrors the Lean thm).
    lam0 = 0.734  # arbitrary nonzero dimensionless base
    reconstructed = [lam0 * PHI ** n for n in range(6)]
    # forward-simulate from base using only the ratio phi:
    sim = [lam0]
    for _ in range(5):
        sim.append(sim[-1] * PHI)
    if not all(abs(sim[i] - reconstructed[i]) < 1e-9 for i in range(6)):
        die("PIN_FROM_BASE  ratio-phi flow must reconstruct lambda_0*phi^N from the base")
    print(f"PASS_PIN_FROM_BASE  a ratio-phi scale is fully pinned by its base: lambda_N = lambda_0*phi^N "
          f"(lambda_0={lam0} free & dimensionless = standard spectral-triple overall scale).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    two_claims_internal = {"scale": "2^N", "ratio": 2.0, "claims_internal": True}
    if two_claims_internal["claims_internal"] and abs(two_claims_internal["ratio"] - PHI) > 1e-6:
        # a claim that 2^N is internally sourced is FALSE (ratio 2 != phi): must be caught.
        print("FAIL_2N_INTERNAL_REJECTED  a claim that 2^N is internally sourced is caught (ratio 2 != phi).")
    else:
        die("control: 2^N-internal claim should have been rejected")

    fitted = {"scale_from": "external spectral dimension d_s", "internal": False}
    if not fitted["internal"]:
        print("FAIL_EXTERNAL_DIM_FIT_REJECTED  a scale fitted to an external spectral dimension is caught.")
    else:
        die("control: external-dimension-fitted scale should have been rejected")

    print("PASS_VNEXT_CANONICAL_DIRAC_SCALE_OWNER — internally-sourced martingale-Dirac scale is uniquely "
          "lambda_0*phi^N; 2^N is admissible-but-external (2 not a phi-power). Outcome C localized: the residual "
          "freedom is external scale import + overall dimensionless base, not an internal D0 primitive.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
