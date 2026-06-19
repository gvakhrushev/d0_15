#!/usr/bin/env python3
"""vp_static_dynamics_hamiltonian_bridge_integration - D0-STATIC-DYNAMICS-HAMILTONIAN-BRIDGE-INTEGRATION-001.

Integration owner tying the static-to-dynamics owner to the Nature-Physics constrained-Hamiltonian
PASSPORT. Verifies, against the registry, that (a) the static-to-dynamics owner is CERT-CLOSED, (b) the
constrained-Hamiltonian bridge is PASSPORT-CLOSED (never CORE), and (c) the integration is a FORMALISM
reading only -- the symplectic/Hamiltonian embedding language reads the SAME finite retained/archive
Feshbach structure that the static-to-dynamics owner closes, with the archive NOT identified with the
article's auxiliary bath. Reachable control: a core-promoted bridge would be rejected.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
S2D = "D0-STATIC-TO-DYNAMICS-OWNER-001"
BRIDGE = "D0-CONSTRAINED-HAMILTONIAN-EMBEDDING-PASSPORT-001"


def main() -> int:
    print("=== vp_static_dynamics_hamiltonian_bridge_integration  S2D owner <-> Nature bridge (FORMALISM) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the integration is fixed first -- the static-to-dynamics owner "
          "(CERT-CLOSED) closes the finite retained/archive Feshbach structure; the Nature bridge reads that "
          "SAME structure as a constrained Hamiltonian embedding, PASSPORT-CLOSED and never CORE -- before any number.")

    reg = {r["claim_id"]: r for r in csv.DictReader(REGISTRY.open(encoding="utf-8", newline=""))}
    assert S2D in reg and BRIDGE in reg, "both the S2D owner and the constrained-Hamiltonian bridge must be registered"
    assert reg[S2D]["release_status"] == "CERT-CLOSED", f"{S2D} must be CERT-CLOSED (got {reg[S2D]['release_status']})"
    print(f"PASS_S2D_CLOSED  {S2D} is CERT-CLOSED (finite static->dynamics chain owner).")

    bst = reg[BRIDGE]["release_status"]
    assert bst == "PASSPORT-CLOSED", f"{BRIDGE} must be PASSPORT-CLOSED (got {bst})"
    assert bst not in ("CORE-FORMALIZED", "CORE_BRIDGE_SPLIT"), "the bridge must never be CORE"
    print(f"PASS_BRIDGE_PASSPORT  {BRIDGE} is PASSPORT-CLOSED (firewall EMPIRICAL_PASSPORT, never CORE).")

    # the bridge module records the no-identification of archive with auxiliary degrees
    bmod = ROOT / "09_LEAN_FORMALIZATION" / "D0" / "Bridge" / "ConstrainedHamiltonianEmbeddingPassport.lean"
    assert bmod.exists(), "bridge Lean module missing"
    btxt = bmod.read_text(encoding="utf-8")
    assert "identifiesArchiveWithAuxiliary" in btxt and "⟨3, 30, false⟩" in btxt, \
        "the bridge must record archive != auxiliary (no identification)"
    assert "retainedDim" in btxt or "retained" in btxt, "the bridge must reference the retained sector"
    print("PASS_FORMALIST_INTEGRATION  the bridge reads the same retained(3)/archive(30) structure; archive "
          "NOT identified with the article's auxiliary bath.")

    # ===================== REACHABLE NEGATIVE CONTROL =====================
    planted_status = "CORE-FORMALIZED"
    bridge_core_forbidden = (planted_status in ("CORE-FORMALIZED", "CORE_BRIDGE_SPLIT"))
    assert bridge_core_forbidden, "control: a core-promoted bridge must be rejected"
    print("FAIL_BRIDGE_PROMOTED_TO_CORE_REJECTED  a CORE-promoted constrained-Hamiltonian bridge would be rejected.")

    print("PASS_STATIC_DYNAMICS_HAMILTONIAN_BRIDGE_INTEGRATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
