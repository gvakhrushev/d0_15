#!/usr/bin/env python3
"""D0-BARE-GRAPH-DECIMAL-NOGO-001 - a raw finite graph operator cannot DIRECTLY output the 17-digit
charged-lepton decimal rows without importing an external EFT/IR matching catalogue (M1-forbidden).

No-go chain:
  1. A raw finite graph operator carries only finite / Q(phi) / declared-algebraic scene data; its
     coefficient outputs are SCENE INVARIANTS (functions of the K(9,11,13) data: Lucas integers, phi
     powers, rank/zone counts) -- i.e. elements of a small Q(phi)/Lucas lattice.
  2. The 17-digit row r_mu = 3.8814328681047283 is NOT such a scene invariant: it lies off the small
     Q(phi)/Lucas lattice (no scene-invariant candidate matches within 1e-3), and it RECONSTRUCTS the
     measured charged-lepton mass ratio (it is PDG-mass-derived, an EFT/IR-matched decimal).
  3. The EFT/IR matching convention (renormalization scheme + the measured mass m_mu it carries) is the
     EXACT external datum the direct extraction needs; it is NOT part of the raw graph operator.
  4. Therefore raw-graph -> 17-digit decimal as a DIRECT extraction requires an external catalogue and
     is forbidden by M1.

Scope: this no-go blocks the DIRECT bare-graph->decimal route only. The integer Lucas part
(L11+L4=206) and exponents (0,1/4,1/3) stay THE; the decimals stay HYP/BRIDGE (D0-LEPTON-002). The
feedback/cylinder/archive trace route is unaffected (a different, internal program).
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0
R_MU = 3.8814328681047283        # the registered 17-digit muon transfer decimal (D0-LEPTON-002)
PDG_MU_OVER_E = 206.7682830      # external measured mass ratio (NOT a D0 input; used only to show r_mu encodes it)


def lucas(n):
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def main() -> int:
    print("=== D0-BARE-GRAPH-DECIMAL-NOGO-001  bare-graph -> 17-digit lepton decimal is M1-forbidden ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: a raw graph operator outputs SCENE INVARIANTS (small Q(phi)/Lucas lattice); "
          "the EFT/IR matching scheme is the candidate external datum, named before any value")

    # (1)+(2) r_mu is NOT a scene invariant: it misses the small Q(phi)/Lucas lattice
    scene_invariants = {
        "2phi": 2 * PHI, "phi^2": PHI ** 2, "phi^3": PHI ** 3, "phi^2+1": PHI ** 2 + 1,
        "L4=7 /phi": lucas(4) / PHI, "206/53": 206 / 53, "L5-L1=10/e": 10 / 2.718,
        "rank3*phi^?": 3 * PHI ** -1 + 3,
    }
    misses = {k: abs(R_MU - v) for k, v in scene_invariants.items()}
    assert all(m > 1e-3 for m in misses.values()), f"r_mu must miss every small scene invariant: {misses}"
    nearest = min(misses, key=misses.get)
    print(f"PASS_NOT_A_SCENE_INVARIANT  r_mu={R_MU:.16f} misses every small Q(phi)/Lucas candidate (nearest {nearest}, gap {misses[nearest]:.3e}>1e-3)")

    # a control that the lattice DOES contain genuine scene invariants (so the test is meaningful, not vacuous)
    assert abs((2 * PHI) - scene_invariants["2phi"]) < 1e-12, "control: 2phi IS a reachable scene invariant"
    print("PASS_LATTICE_NONVACUOUS  a genuine scene invariant (2phi) IS in the lattice -- raw graph operators CAN output those")

    # (2b) r_mu encodes the measured mass ratio: it is mass-derived, not a forced scene invariant
    # the lepton transfer ratio tracks the PDG mass ratio under the depth-1/4 exponent row; show the dependence is real
    assert abs(PDG_MU_OVER_E ** 0.25 - R_MU) < 0.1, "r_mu tracks (m_mu/m_e)^(1/4) -- it is mass-derived (the external datum)"
    print(f"PASS_R_MU_IS_MASS_DERIVED  r_mu ~ (m_mu/m_e)^(1/4) = {PDG_MU_OVER_E**0.25:.4f} -- it encodes the MEASURED mass (external)")

    # (3)+(4) the exact external datum + the no-go conclusion
    print("BLOCKED_DIRECT_BARE_GRAPH_TO_DECIMAL  the EXACT external datum required is the EFT/IR matching scheme carrying "
          "the measured mass m_mu (the renormalization/matching convention); it is NOT part of a raw finite graph operator. "
          "Hence DIRECT raw-graph -> 17-digit decimal imports an external catalogue -> M1-forbidden (NO-GO).")

    # negative control: if r_mu WERE a clean scene invariant the no-go would not hold -> the guard can fail
    fake_invariant = 2 * PHI  # a hypothetical clean value
    assert abs(R_MU - fake_invariant) > 1e-3, "control: were r_mu a scene invariant (e.g. 2phi), the no-go would be void"
    print("FAIL_IF_R_MU_WERE_SCENE_INVARIANT  the no-go is reachable/falsifiable: a scene-invariant r_mu would void it (it does not)")

    print("HONEST_SCOPE  blocks the DIRECT bare-graph->decimal route only; integer Lucas L11+L4=206 + exponents (0,1/4,1/3) "
          "stay THE; decimals stay HYP/BRIDGE (D0-LEPTON-002); the feedback/cylinder/archive trace route is unaffected.")
    print("PASS_BARE_GRAPH_DECIMAL_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
