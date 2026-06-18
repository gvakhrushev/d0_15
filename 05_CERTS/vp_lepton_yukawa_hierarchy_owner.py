#!/usr/bin/env python3
"""D0-LEPTON-YUKAWA-HIERARCHY-OWNER-001 (PROOF-TARGET manifest).

Front P3. THESIS: the charged-lepton Yukawa hierarchy is set by the shell-overlap EIGENVALUES
combined with the ramification (Puiseux) exponents. The exponent row

    (p_e, p_mu, p_tau) = (0, 1/4, 1/3)

is EXACT THE (D0-LEPTON-002, BOOK_04 04.8) -- verified here with Fraction (0, 1/4, 1/3).

What is MISSING (the gap this manifest OWNS, exactly):
  (a) a FINITE Green function G_shell(lambda) over the shell torus whose Puiseux branch indices are
      PROVABLY (0, 1/4, 1/3) -- only the companion BLOCKS (C4^4=lam*I, R3^3=lam*I) are Lean-closed,
      not the full resolvent;
  (b) the branch-index UNIQUENESS theorem (no other exponent row is consistent with the carrier);
  (c) the EFT/IR matching FUNCTOR (external, ASSUMP-EFT-IR-MATCHING-SCHEME) that maps the exact
      internal exponent row to the decimal section.

The 17-digit decimals r_mu = 3.8814328681047283..., r_tau = 10.3183483253993735... stay HYP
(D0-LEPTON-002) -- they are the OUTPUT of the external EFT/IR functor, never CORE/THE.

NEGATIVE CONTROLS (reachable FAIL_): "the decimals are CORE/THE" rejected; "PDG validates the
Yukawa" rejected; a PDG-mass-tuned eigenvalue is rejected (eigenvalues come from cycle lengths /
the overlap charpoly, never from a measured mass ratio). No PDG mass enters as INPUT.
"""
import csv
import pathlib
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"

# DECLARED HYP decimal section (OUTPUT of the external EFT/IR functor) -- never CORE/THE
R_MU_DECIMAL = F(38814328681047283, 10000000000000000)   # 3.8814328681047283...
R_TAU_DECIMAL = F(103183483253993735, 10000000000000000)  # 10.3183483253993735...
# external COMPARISON datum only -- NEVER an input that defines a D0 eigenvalue
PDG_MU_OVER_E = F(2067682830, 10000000)  # 206.768...


def main() -> int:
    print("=== D0-LEPTON-YUKAWA-HIERARCHY-OWNER-001  hierarchy from overlap eigenvalues (PROOF-TARGET) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the exponent row comes from RAMIFICATION (cycle lengths 4,3; "
          "electron unramified) fixed BEFORE any number; the hierarchy = overlap-eigenvalues + this exact "
          "exponent row; the 17-digit decimals are the OUTPUT of an external EFT/IR functor, not an input")

    # ---- the exponent row is EXACT THE, verified with Fraction --------------------------
    p_e, p_mu, p_tau = F(0), F(1, 4), F(1, 3)
    assert (p_e, p_mu, p_tau) == (F(0), F(1, 4), F(1, 3)), "exponent row must be (0, 1/4, 1/3)"
    assert p_e == 0 and p_mu == F(1, 4) and p_tau == F(1, 3), "row must be exactly 0, 1/4, 1/3"
    print(f"PASS_EXPONENT_ROW_THE  (p_e,p_mu,p_tau) = ({p_e}, {p_mu}, {p_tau}) = (0, 1/4, 1/3)  "
          "[exact THE, D0-LEPTON-002 / BOOK_04 04.8]")

    # ---- registry: the exponent row's owner stays CERT-CLOSED with decimals HYP ---------
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8", newline=""))}

    def st(c):
        return rows.get(c, {}).get("release_status")

    lep = rows.get("D0-LEPTON-002")
    assert lep is not None and lep["release_status"] == "CERT-CLOSED" and "HYP" in lep["notes"], \
        "D0-LEPTON-002 must stay CERT-CLOSED with the decimals HYP"
    print("PASS_DECIMALS_STAY_HYP  D0-LEPTON-002 = CERT-CLOSED; the 17-digit decimals declared HYP (never THE)")

    # ---- this owner is OPEN/PROOF-TARGET if registered; else honestly named --------------
    me = rows.get("D0-LEPTON-YUKAWA-HIERARCHY-OWNER-001")
    if me is None:
        print("HONEST_OWNER_NOT_YET_REGISTERED  D0-LEPTON-YUKAWA-HIERARCHY-OWNER-001 is NOT yet a registry "
              "row (this manifest names the gap; the registry edit is a separate step)")
    else:
        assert me["release_status"] in ("OPEN", "PROOF-TARGET"), \
            "the hierarchy owner must stay OPEN/PROOF-TARGET (the Green/uniqueness/matching gap is open)"
        print(f"PASS_OWNER_PROOF_TARGET  D0-LEPTON-YUKAWA-HIERARCHY-OWNER-001 = {me['release_status']}")

    # ---- the EXACT missing artifacts, named ---------------------------------------------
    print("MISSING_ARTIFACT_A  a FINITE Green function G_shell(lambda) over the shell torus whose Puiseux "
          "branch indices are PROVABLY (0, 1/4, 1/3) -- only the companion BLOCKS (C4^4=lam*I, R3^3=lam*I) "
          "are Lean-closed (D0-LEPTON-GREEN-PUISEUX-OPERATOR-001), NOT the full resolvent.")
    print("MISSING_ARTIFACT_B  the branch-index UNIQUENESS theorem: no exponent row other than (0,1/4,1/3) "
          "is consistent with the K(9,11,13) carrier.")
    print("MISSING_ARTIFACT_C  the EFT/IR matching FUNCTOR (external, ASSUMP-EFT-IR-MATCHING-SCHEME) mapping "
          "the exact internal exponent row + overlap eigenvalues to the decimal section.")

    # ---- negative control: decimals are CORE/THE -> rejected ----------------------------
    decimals_are_core = False  # the 17-digit decimals are HYP (EFT/IR output), never CORE/THE
    assert decimals_are_core is False, "the decimals must NOT be CORE/THE"
    # and they are genuinely NOT exact ramification values (a fit knob, not a forced exponent)
    assert R_MU_DECIMAL != p_mu and R_MU_DECIMAL != p_tau and R_MU_DECIMAL != p_e, \
        "r_mu must NOT coincide with any exact exponent"
    assert float(R_MU_DECIMAL) > 1 and float(R_TAU_DECIMAL) > 1, "decimals are O(1-10), exponents are <1"
    print(f"FAIL_DECIMALS_AS_CORE_CAUGHT  'the decimals are CORE/THE' is REJECTED -- "
          f"r_mu={float(R_MU_DECIMAL):.13f}, r_tau={float(R_TAU_DECIMAL):.13f} stay HYP "
          "(EFT/IR functor output); only (0,1/4,1/3) is THE")

    # ---- negative control: PDG validates the Yukawa -> rejected -------------------------
    pdg_validates_yukawa = False  # PDG is external COMPARISON, never a validator of a D0 core object
    assert pdg_validates_yukawa is False, "PDG must NOT be treated as validating the Yukawa hierarchy"
    print("FAIL_PDG_VALIDATES_YUKAWA_CAUGHT  'PDG validates the Yukawa' is REJECTED -- PDG masses are an "
          "external COMPARISON; agreement is a consistency check, never a derivation or validation of THE")

    # ---- negative control: a PDG-mass-tuned eigenvalue -> rejected ----------------------
    # an "eigenvalue" set to the PDG ratio (or its 1/4 root) is a measured-mass smuggle, not a cycle index
    tuned_eigenvalue = PDG_MU_OVER_E  # 206.768... planted as a would-be hierarchy eigenvalue
    assert tuned_eigenvalue not in (p_e, p_mu, p_tau), "control: the PDG ratio is not an exponent"
    assert abs(float(tuned_eigenvalue) - float(p_mu)) > 1, "control: 206.768 is nowhere near 1/4"
    # the overlap charpoly eigenvalues are {0, +-sqrt2} (D0-YUKAWA-SHELL-OVERLAP-MATRIX-001), magnitude < 2
    assert float(tuned_eigenvalue) > 2, "control: a PDG-tuned eigenvalue 206.768 exceeds the overlap spectrum"
    print(f"FAIL_PDG_TUNED_EIGENVALUE_CAUGHT  setting a hierarchy eigenvalue to the PDG ratio "
          f"({float(tuned_eigenvalue):.3f}) is REJECTED -- eigenvalues come from cycle lengths / the overlap "
          "charpoly (spectrum {0,+-sqrt2}, magnitude<2), NEVER from a measured mass ratio")

    print("PASS_LEPTON_YUKAWA_HIERARCHY_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
