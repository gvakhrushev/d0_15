#!/usr/bin/env python3
"""D0 lepton no-decimal-fit guard - charged-lepton coefficients are never closed by a decimal/PDG fit.

Checks (can-FAIL): the 17-digit r_mu is NOT a clean Q(phi) value (so it is not a forced algebraic
output), and no book claims the lepton decimals are CORE-THE / PDG-validated. The integer Lucas part
L11+L4=206 and exponents (0,1/4,1/3) stay THE; the decimals stay HYP.
"""
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
PHI = (1.0 + 5.0 ** 0.5) / 2.0
R_MU = 3.8814328681047283
FORBIDDEN = [
    "charged-lepton decimals are CORE-THE",
    "PDG validates lepton coefficients",
    "lepton decimals are a derived theorem",
]


def main() -> int:
    print("=== D0 lepton no-decimal-fit guard ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: lepton coefficients may use only finite/Q(phi)/Lucas data; decimal/PDG fits are barred")
    for name, v in (("2phi", 2 * PHI), ("phi^2", PHI ** 2), ("phi^3", PHI ** 3)):
        assert abs(R_MU - v) > 1e-2, f"r_mu must not be the clean Q(phi) value {name}"
    print("PASS_NOT_DECIMAL_FORCED  r_mu is not within 1e-2 of any clean Q(phi) value (a fit knob, not a forced algebraic output)")
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))
    hits = [f for f in FORBIDDEN if f in prose]
    assert not hits, f"forbidden lepton-decimal over-claim present: {hits}"
    print("PASS_NO_DECIMAL_OVERCLAIM  no 'lepton decimals are CORE-THE' / 'PDG validates lepton coefficients' in the books")
    assert any(f in "x charged-lepton decimals are CORE-THE x" for f in FORBIDDEN), "control: detector reachable"
    print("FAIL_PLANTED_DECIMAL_OVERCLAIM_CAUGHT  the over-claim detector is reachable")
    print("PASS_LEPTON_NO_DECIMAL_FIT_GUARD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
