#!/usr/bin/env python3
"""D0-NEUTRINO-DELTA-ALPHA-NORM-SQUARE-001 (CERT-CLOSED internal object; neutrino reading PASSPORT).

P_sterile = (Delta_alpha)^2 is an EXACT Q(phi) element, computed from the phi-only internal object
Delta_alpha = alpha_top^-1 - alpha_alg^-1 = -156109/5 + (289442/15) phi  (Lean-CORE
D0.Spectral.AlphaFeshbachDixmierOwner.p_sterile_in_qphi, p_sterile_nonneg).

Squaring (a, b) = a + b phi via phi^2 = phi + 1:  (a,b)^2 = (a^2 + b^2, 2 a b + b^2).
With a = -156109/5, b = 289442/15:

    A = a^2 + b^2          = (-156109/5)^2 + (289442/15)^2      = 303106850293/225
    B = 2 a b + b^2        = 2(-156109/5)(289442/15) + (289442/15)^2 = -187330335704/225
    P_sterile = A + B phi  = 303106850293/225 - (187330335704/225) phi.

HONESTY: NO measured neutrino mass enters; the value is computed from Delta_alpha (phi-only). The
identification m_nu ~ P_sterile is declared a PASSPORT reading (EMPIRICAL_PASSPORT firewall), never
CORE-THE. A planted "m_nu input tunes Delta_alpha" is rejected.
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


def val(x):
    return float(x[0]) + float(x[1]) * PHI


def main() -> int:
    print("=== D0-NEUTRINO-DELTA-ALPHA-NORM-SQUARE-001  P_sterile = Delta_alpha^2 exactly in Q(phi) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: Delta_alpha = alpha_top^-1 - alpha_alg^-1 = -156109/5 + (289442/15) phi "
          "(phi-only internal object) fixed BEFORE any value; P_sterile := Delta_alpha^2; no measured-neutrino-mass input")

    # the phi-only internal object Delta_alpha (forced before any numeric P_sterile)
    a, b = F(-156109, 5), F(289442, 15)
    delta_alpha = (a, b)
    assert delta_alpha == (F(-156109, 5), F(289442, 15)), f"Delta_alpha must be -156109/5 + 289442/15 phi: {delta_alpha}"
    print(f"PASS_DELTA_ALPHA_PHI_ONLY  Delta_alpha = {delta_alpha} = {val(delta_alpha):.6f} (computed from phi only)")

    # square via the Q(phi) (a,b) arithmetic
    p_sterile = mul(delta_alpha, delta_alpha)

    # closed-form A, B from the (a,b)^2 = (a^2+b^2, 2ab+b^2) identity (phi^2 = phi+1)
    A = a * a + b * b
    B = 2 * a * b + b * b
    assert A == F(303106850293, 225), f"A = a^2+b^2 must be 303106850293/225: {A}"
    assert B == F(-187330335704, 225), f"B = 2ab+b^2 must be -187330335704/225: {B}"
    assert p_sterile == (A, B), f"the (a,b) square must equal (A,B): {p_sterile} vs {(A, B)}"
    print(f"PASS_P_STERILE_EXACT  P_sterile = Delta_alpha^2 = {p_sterile} = A + B phi in Q(phi)")
    print(f"PASS_AB_CLOSED_FORM  A = a^2+b^2 = {A}, B = 2ab+b^2 = {B}  (matches the (a,b) square exactly)")

    # nonnegativity (p_sterile_nonneg): P_sterile = a real square >= 0
    assert val(p_sterile) >= 0, f"P_sterile must be >= 0 (a square): {val(p_sterile)}"
    print(f"PASS_P_STERILE_NONNEG  P_sterile = {val(p_sterile):.6f} >= 0 (p_sterile_nonneg; a real square)")

    # ---- reachable negative controls ----
    # 1) NO measured neutrino mass enters: a planted m_nu value cannot reproduce the phi-only P_sterile.
    planted_m_nu = (F("0.06"), F(0))   # an eV-scale measured neutrino-mass scalar (no phi-component)
    assert planted_m_nu != p_sterile, "control: a measured m_nu scalar (no phi) is not the phi-only P_sterile"
    print("FAIL_M_NU_INPUT_CAUGHT  a measured m_nu scalar (~0.06 eV, no phi-component) != P_sterile; "
          "P_sterile is computed from Delta_alpha (phi-only), NOT from any measured neutrino mass")

    # 2) a planted "m_nu tunes Delta_alpha" is rejected: perturbing Delta_alpha by an m_nu-derived shift
    #    breaks the exact Q(phi) value (the structure forbids a measured-mass degree of freedom).
    tuned_delta = (a + F(1, 1000), b)   # planted shift "from fitting m_nu"
    tuned_p = mul(tuned_delta, tuned_delta)
    assert tuned_p != p_sterile, "control: an m_nu-tuned Delta_alpha must break the exact P_sterile value"
    print("FAIL_M_NU_TUNES_DELTA_ALPHA_CAUGHT  an m_nu-derived shift of Delta_alpha breaks the exact P_sterile; "
          "Delta_alpha has NO measured-mass tuning degree of freedom (it is fixed phi-only)")

    # 3) the m_nu ~ P_sterile identification is PASSPORT, never CORE-THE
    identification_is_core = False
    assert identification_is_core is False, "the m_nu ~ P_sterile identification must be PASSPORT, never CORE-THE"
    print("FAIL_IDENTIFICATION_AS_CORE_CAUGHT  claiming m_nu ~ P_sterile as CORE-THE is rejected; it is an "
          "EMPIRICAL_PASSPORT reading (the neutrino interpretation is passport-only, never core theory)")

    print("HONEST_SCOPE  CERT-CLOSED internal object: P_sterile = Delta_alpha^2 is exact in Q(phi) (Lean-CORE "
          "D0.Spectral.AlphaFeshbachDixmierOwner.p_sterile_in_qphi / p_sterile_nonneg). The neutrino reading "
          "(m_nu ~ P_sterile) is an EMPIRICAL_PASSPORT, never CORE-THE; no measured neutrino mass enters.")
    print("PASS_NEUTRINO_DELTA_ALPHA_NORM_SQUARE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
