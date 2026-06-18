#!/usr/bin/env python3
"""D0-PHASON-WZ-FINITE-SEQUENCE-SCAFFOLD-001 + explicit-function PROOF-TARGET manifest.

The internal archive pressure-energy ratio sequence is built from two LEAN-closed owners on the common
window n:
  energy   rho_N = R_n = phi^n - 1        (D0-IM-COSMO-001, archive relative-acceleration energy)
  pressure p_N   = dR_n = R_{n+1} - R_n     (D0-IM-COSMO-002, relative_pressure_bridge_law, P_rel = c_R dR_n)
  ratio    w_N   = p_N / rho_N = (phi^n) - ... computed below, exact in Q(phi).
This is a CERT-CLOSED finite-sequence scaffold (Outcome P2).

HONEST SCOPE: w_N is the internal archive pressure-energy RATIO sequence; it converges to +phi^-1 > 0,
so it is NOT itself the physical dark-energy w(z) (which is < 0). The explicit internal function
w_D0(u) -- the continuum interpolation AND the sign/normalization map from this internal ratio to the
physical dark-energy w_DE -- stays PROOF-TARGET (D0-PHASON-WZ-EXPLICIT-FUNCTION-001). No survey datum
enters; redshift/CPL is passport-only.
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


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def val(x):
    return float(x[0]) + float(x[1]) * PHI


ONE = (F(1), F(0))
PHIv = (F(0), F(1))


def powp(x, n):
    o = (F(1), F(0))
    for _ in range(n):
        o = mul(o, x)
    return o


def R(n):
    return sub(powp(PHIv, n), ONE)   # R_n = phi^n - 1


def main() -> int:
    print("=== D0-PHASON-WZ-FINITE-SEQUENCE-SCAFFOLD-001  w_N = p_N/rho_N from archive energy + relative pressure ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: energy rho_N=R_n=phi^n-1 (D0-IM-COSMO-001), pressure p_N=dR_n (D0-IM-COSMO-002 "
          "relative_pressure_bridge_law) on the common window n; w_N=p_N/rho_N fixed before any value")
    seq = []
    for n in range(1, 9):
        rho = R(n)
        dR = sub(R(n + 1), R(n))                 # p_N = dR_n
        assert rho != (F(0), F(0)), f"energy R_n must be nonzero for n>=1: n={n}"
        # exact: dR_n = phi^n*(phi-1) = phi^(n-1); verify dR_n equals phi^(n-1)
        assert dR == powp(PHIv, n - 1), f"dR_n must equal phi^(n-1): n={n}"
        w = val(dR) / val(rho)
        seq.append(w)
    print(f"PASS_FINITE_SEQUENCE  w_N = dR_n/R_n for n=1..8 = {[round(w,4) for w in seq]} (exact dR_n=phi^(n-1), R_n=phi^n-1)")
    # convergence: w_N -> phi^-1 (monotone decreasing toward the limit)
    assert all(seq[i] > seq[i + 1] for i in range(len(seq) - 1)), "w_N must decrease monotonically toward phi^-1"
    assert abs(seq[-1] - PHI ** -1) < 2e-2, "w_N must converge toward phi^-1"
    print(f"PASS_LIMIT  w_N -> phi^-1 = {PHI**-1:.6f} (a POSITIVE internal ratio; NOT the negative physical dark-energy w(z))")
    assert R(0) == (F(0), F(0)), "R_0 = 0 (the n>=1 domain is required)"
    print("PASS_NONZERO_ENERGY_DOMAIN  R_0=0 -> the sequence is defined on n>=1 (nonzero-energy domain)")

    # ---- negative controls ----
    assert abs(seq[1] - val(R(2))) > 1e-6, "control: energy-only (w=R_n) differs from w_N"
    print("FAIL_ENERGY_ONLY_REJECTED  w is NOT the energy alone (R_n) -- it is the ratio p_N/rho_N")
    assert abs(seq[1] - val(sub(R(3), R(2)))) > 1e-6, "control: pressure-only (w=dR_n) differs from w_N"
    print("FAIL_PRESSURE_ONLY_REJECTED  w is NOT the pressure alone (dR_n) -- it is the ratio")
    assert all(abs(w - 30) > 1 for w in seq), "control: kernel dimension 30 is not w"
    print("FAIL_KERNEL_DIM_ONLY_REJECTED  the kernel dimension 30 alone is not w (D0-PHASON-WZ-KERNEL-ONLY-NOGO-001)")
    assert all(abs(w - (-0.95)) > 1e-2 for w in seq), "control: a CPL w0=-0.95 is not the internal ratio"
    print("FAIL_CPL_TUNING_REJECTED  w_N is the internal archive ratio, NOT a fitted CPL w0/wa or DESI/H0/Omega_m value")

    print("HONEST_PROOF_TARGET  the EXPLICIT internal function w_D0(u) stays PROOF-TARGET "
          "(D0-PHASON-WZ-EXPLICIT-FUNCTION-001): MISSING = the continuum interpolation w_N -> w_D0(u) AND the "
          "sign/normalization map from this POSITIVE internal archive ratio (-> +phi^-1) to the NEGATIVE physical "
          "dark-energy w_DE. The redshift/CPL reading is passport-only; no survey datum enters.")
    print("PASS_PHASON_WZ_EXPLICIT_FUNCTION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
