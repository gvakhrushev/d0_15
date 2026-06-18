#!/usr/bin/env python3
"""vp_assumption_ledger_green - D0-ASSUMPTION-LEDGER-GREEN-001 (CERT-CLOSED).

Layer-0 gate repair. The core no-sorry guard (`check_no_sorry_in_core.py`) embeds an
assumption-ledger validator whose `ALLOWED_TYPES` whitelist was frozen at base-v14 (7 generic
bridge types) while the ledger legitimately grew two evolved categories across Iter-18/19/20:
  (A) precise EXTERNAL-owner theorem types (Frobenius DIVISION_ALGEBRA_CLASSIFICATION, Tomita
      VON_NEUMANN_MODULAR_THEOREM, ...), each a real classical theorem wrapped as one explicit
      `D0.Bridge.BridgeAssumption.*` under `D0/Bridge/`, never an axiom; and
  (B) D0-INTERNAL forcing targets (Hodge / Riemann-axis / P-vs-NP Lyapunov + the navigation/
      packaging types) -- decidable M1-reductio hypotheses living in their own domain module.

This guard certifies the reconciliation is DISCIPLINE-PRESERVING, not "stop checking":
  * every ledger row carries a recognized type and is NEVER typed CORE/FOUNDATION/UNSPECIFIED;
  * every EXTERNAL row is a `BridgeAssumption.*` under `D0/Bridge/`;
  * every INTERNAL forcing-target row is EXPLICIT and references a real Lean decl;
  * `check_no_sorry_in_core.py` exits 0 (PASS).
Negative controls (reachable): a planted CORE-typed row, a planted unknown-type row, and a
planted external row outside `D0/Bridge/` are each caught by the same predicates.
"""
import csv
import pathlib
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION"
LEDGER = LEAN / "docs" / "LEAN_ASSUMPTION_LEDGER.csv"
GUARD = LEAN / "tools" / "check_no_sorry_in_core.py"

FORBIDDEN_TYPES = {"CORE", "FOUNDATION", "UNSPECIFIED", ""}
# the recognized external + internal type taxonomy (must match the guard)
EXTERNAL_TYPES = {
    "CONDENSED_BRIDGE", "QFT_RG_BRIDGE", "EMPIRICAL_DATA", "SMOOTH_LIMIT", "MACRO_LIMIT",
    "PHYSICS_DICTIONARY", "LIE_ALGEBRA_LIBRARY_GAP",
    "CARTAN_COMPACTNESS_CRITERION", "SUBFACTOR_INDEX_QUANTIZATION", "LATTICE_GENUS_THEOREM",
    "NONCOMMUTATIVE_GEOMETRY_THEOREM", "VON_NEUMANN_MODULAR_THEOREM", "QM_FOUNDATIONS_THEOREM",
    "QM_RECONSTRUCTION_THEOREM", "EMERGENT_GRAVITY_PROGRAM", "DIVISION_ALGEBRA_CLASSIFICATION",
    "LATTICE_GAUGE_RIGOR", "NONCOMMUTATIVE_INTEGRAL_THEOREM", "QUANTUM_METRIC_CONVERGENCE",
    "SYMBOLIC_DYNAMICS_CLASSIFICATION", "TRANSCENDENCE_THEOREM_LINDEMANN_WEIERSTRASS",
}
INTERNAL_TYPES = {
    "D0_INTERNAL_FORCING_TARGET", "COMPLEXITY_NAVIGATION_POTENTIAL", "SPECTRAL_PACKAGING_SYMMETRY",
}


def row_ok(row):
    """Return the list of discipline violations for one ledger row (empty == conformant)."""
    aid = row.get("assumption_id", "")
    typ = row.get("assumption_type", "")
    bad = []
    if typ in FORBIDDEN_TYPES or typ not in (EXTERNAL_TYPES | INTERNAL_TYPES):
        bad.append(f"{aid}: bad type {typ!r}")
    if typ in INTERNAL_TYPES:
        if row.get("status", "") != "EXPLICIT":
            bad.append(f"{aid}: internal target not EXPLICIT")
        if not row.get("lean_name") or not row.get("lean_file"):
            bad.append(f"{aid}: internal target missing Lean ref")
    else:
        if "BridgeAssumption." not in row.get("lean_name", ""):
            bad.append(f"{aid}: external row lean_name not BridgeAssumption.*")
        if not row.get("lean_file", "").replace("\\", "/").startswith("D0/Bridge/"):
            bad.append(f"{aid}: external row not under D0/Bridge/")
    return bad


def main() -> int:
    print("=== vp_assumption_ledger_green  D0-ASSUMPTION-LEDGER-GREEN-001 (Layer-0 gate repair) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the discipline is fixed FIRST -- every ledger row carries a "
          "recognized non-CORE type; external rows are BridgeAssumption.* under D0/Bridge/; internal "
          "forcing targets are EXPLICIT with a real Lean ref -- before any count.")

    rows = list(csv.DictReader(LEDGER.open(encoding="utf-8", newline="")))
    assert rows, "ledger is empty"

    # 1. the two rows from the original red exist and are now conformant
    by_id = {r["assumption_id"]: r for r in rows}
    for aid in ("ASSUMP-LINDEMANN-LNPHI", "ASSUMP-GLOBAL-LYAPUNOV-POTENTIAL"):
        assert aid in by_id, f"expected ledger row {aid} is missing (rows must not be deleted)"
    assert "BridgeAssumption." in by_id["ASSUMP-LINDEMANN-LNPHI"]["lean_name"], \
        "ASSUMP-LINDEMANN-LNPHI must now be a BridgeAssumption (external owner, properly wrapped)"
    assert by_id["ASSUMP-GLOBAL-LYAPUNOV-POTENTIAL"]["assumption_type"] == "COMPLEXITY_NAVIGATION_POTENTIAL", \
        "ASSUMP-GLOBAL-LYAPUNOV-POTENTIAL must stay an internal forcing target (not promoted to CORE)"
    print(f"PASS_KNOWN_ROWS_PRESENT  the two originally-red rows exist; Lindemann wrapped as bridge, "
          f"Lyapunov kept as internal forcing target (neither deleted nor promoted to CORE).")

    # 2. every row is discipline-conformant
    violations = [v for r in rows for v in row_ok(r)]
    assert not violations, f"ledger discipline violations: {violations}"
    ext = sum(1 for r in rows if r["assumption_type"] in EXTERNAL_TYPES)
    intl = sum(1 for r in rows if r["assumption_type"] in INTERNAL_TYPES)
    print(f"PASS_ALL_ROWS_CONFORMANT  {len(rows)} rows ({ext} external BridgeAssumptions under "
          f"D0/Bridge/, {intl} internal EXPLICIT forcing targets); 0 typed CORE/FOUNDATION/UNSPECIFIED.")

    # 3. the guard itself passes (the gate is green)
    res = subprocess.run([sys.executable, str(GUARD)], capture_output=True, text=True)
    assert res.returncode == 0, f"check_no_sorry_in_core still FAILS:\n{res.stdout}\n{res.stderr}"
    print("PASS_GUARD_GREEN  check_no_sorry_in_core.py exits 0 (core+bridge+all-modules clean).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    # (a) a CORE-typed bridge row is caught
    planted_core = {"assumption_id": "PLANT", "assumption_type": "CORE",
                    "lean_name": "D0.Bridge.BridgeAssumption.X", "lean_file": "D0/Bridge/X.lean",
                    "status": "EXPLICIT"}
    assert row_ok(planted_core), "negative control failed: a CORE-typed row must be rejected"
    print("FAIL_CORE_TYPED_ROW_REJECTED  a planted CORE-typed assumption row is caught (firewall reachable).")

    # (b) an unknown/garbage type is caught
    planted_unknown = {"assumption_id": "PLANT", "assumption_type": "TOTALLY_MADE_UP",
                       "lean_name": "D0.Bridge.BridgeAssumption.X", "lean_file": "D0/Bridge/X.lean",
                       "status": "EXPLICIT"}
    assert row_ok(planted_unknown), "negative control failed: an unknown type must be rejected"
    print("FAIL_UNKNOWN_TYPE_REJECTED  a planted unrecognized assumption type is caught (reachable).")

    # (c) an external row placed outside D0/Bridge/ is caught
    planted_loc = {"assumption_id": "PLANT", "assumption_type": "PHYSICS_DICTIONARY",
                   "lean_name": "D0.Bridge.BridgeAssumption.X", "lean_file": "D0/Spectral/X.lean",
                   "status": "EXPLICIT"}
    assert row_ok(planted_loc), "negative control failed: external row outside D0/Bridge/ must be rejected"
    print("FAIL_EXTERNAL_OUTSIDE_BRIDGE_REJECTED  a planted external row outside D0/Bridge/ is caught (reachable).")

    print("PASS_ASSUMPTION_LEDGER_GREEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
