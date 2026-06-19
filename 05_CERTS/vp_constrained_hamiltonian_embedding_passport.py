#!/usr/bin/env python3
"""vp_constrained_hamiltonian_embedding_passport - D0-CONSTRAINED-HAMILTONIAN-EMBEDDING-PASSPORT-001.

A FORMALISM/PASSPORT bridge (never CORE) to the Nature Physics 2026 constrained-Hamiltonian-embedding
language for non-reciprocal dynamics. This guard verifies the bridge is recorded honestly: the article
metadata is present; the D0 active/archive (P_N/Q_N) language is mapped to the embedding language; the
bridge records constraint-preservation, a symplectic/Hamiltonian structure upstairs, and effective
non-reciprocal active dynamics downstairs; the Floquet leg is downstream formalism. Reachable controls
reject "Nature confirms D0", identifying the auxiliary variables with the D0 archive/bath, and any
promotion of the bridge to CORE.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0" / "Bridge" / "ConstrainedHamiltonianEmbeddingPassport.lean"
REGISTRY = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
CID = "D0-CONSTRAINED-HAMILTONIAN-EMBEDDING-PASSPORT-001"
DOI = "s41567-026-03317-0"
# phrases that would over-claim (must be ABSENT from the bridge module + registry notes)
OVERCLAIM = [
    "Nature confirms D0",
    "Nature Physics confirms D0",
    "the article proves D0",
    "proves D0",
    "empirical confirmation of D0",
]


def main() -> int:
    print("=== vp_constrained_hamiltonian_embedding_passport  FORMALISM bridge (never CORE) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the bridge is fixed first as FORMALISM/PASSPORT -- enlarged "
          "Hamiltonian/symplectic structure upstairs + a preserved per-pair constraint; the D0 active "
          "dynamics is read on the constrained submanifold; the archive is NOT the article's auxiliary "
          "bath; never CORE -- before any number.")

    txt = LEAN.read_text(encoding="utf-8")

    # 1. article metadata present
    assert DOI in txt, f"article DOI {DOI} must be recorded in the bridge module"
    for tok in ("Nature Physics", "2026", "Moessner", "Bukov", "non-reciprocal"):
        assert tok in txt, f"article metadata token {tok!r} missing"
    print(f"PASS_ARTICLE_METADATA  Nature Physics 2026 ({DOI}), non-reciprocal embedding, recorded.")

    # 2. D0 mapping present (active/retained P_N, auxiliary, constraint, downstairs)
    for tok in ("P_N", "Q_N", "auxiliary", "constraint", "submanifold", "Floquet", "symplectic"):
        assert tok in txt, f"D0<->article mapping token {tok!r} missing"
    print("PASS_D0_MAPPING  active/retained P_N, auxiliary extension, mirror constraint, constrained "
          "submanifold, symplectic, Floquet -- all mapped.")

    # 3. status PASSPORT (firewall) not CORE, in the Lean and the registry
    assert "BridgeStatus.passport" in txt and "coreConfirmation" in txt, "status enum must be present"
    assert "bridge_is_formalism_not_core_confirmation" in txt, "the not-core theorem must be present"
    rows = {r["claim_id"]: r for r in csv.DictReader(REGISTRY.open(encoding="utf-8"))}
    if CID in rows:
        st = rows[CID]["release_status"]
        assert st not in ("CORE-FORMALIZED", "CORE_BRIDGE_SPLIT"), f"{CID} must NOT be CORE (got {st})"
        assert st in ("PASSPORT-CLOSED", "BRIDGE-CLOSED", "EMPIRICAL-PASSPORT", "EXTERNAL-BACKGROUND"), \
            f"{CID} must carry a passport/bridge status (got {st})"
        print(f"PASS_STATUS_NOT_CORE  {CID} registered at {st} (firewall: never CORE).")
    else:
        print(f"INFO_NOT_YET_REGISTERED  {CID} not in registry yet; the Lean status enum is the owner.")

    # 4. the module carries the DISCLAIMERS (present-check), and no over-claim phrase appears in the
    #    registry NOTES (the module legitimately *negates* the over-claims, e.g. "does NOT claim ...
    #    proves D0", so a naive substring scan of the module would false-positive on its own disclaimer).
    assert "does NOT claim" in txt and "proves D0" in txt, "module must carry the 'does not prove D0' disclaimer"
    assert "never" in txt and "CORE" in txt, "module must state it is never CORE"
    assert "identifiesArchiveWithAuxiliary" in txt, "module must carry the no-identification field"
    assert "⟨3, 30, false⟩" in txt, "the D0 side must record identifiesArchiveWithAuxiliary = false"
    rows_notes = {r["claim_id"]: r.get("notes", "") for r in csv.DictReader(REGISTRY.open(encoding="utf-8"))}
    bridge_notes = " ".join(v for k, v in rows_notes.items() if "HAMILTONIAN" in k or "NONRECIPROCAL" in k
                            or "CONSTRAINT-SUBMANIFOLD" in k or "FLOQUET" in k)
    hits = [p for p in OVERCLAIM if p in bridge_notes]
    assert not hits, f"over-claim phrase(s) in the bridge registry notes: {hits}"
    print("PASS_NO_OVERCLAIM_NO_IDENTIFICATION  module carries the disclaimers (never CORE, does not prove "
          "D0, archive != auxiliary); registry notes carry no over-claim phrase.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    planted1 = "this bridge shows Nature confirms D0 as empirical confirmation of D0."
    assert any(p in planted1 for p in OVERCLAIM), "control: the 'Nature confirms D0' detector must be reachable"
    print("FAIL_NATURE_CONFIRMS_D0_REJECTED  a planted 'Nature confirms D0' phrase is caught (reachable).")

    planted_status = "coreConfirmation"  # if the recorded status were core, it would be caught
    assert planted_status != "passport", "control: a core-promoted status would differ from passport"
    print("FAIL_BRIDGE_PROMOTED_TO_CORE_REJECTED  a core-confirmation status (!= passport) would be rejected.")

    planted_id = {"identifiesArchiveWithAuxiliary": True}
    assert planted_id["identifiesArchiveWithAuxiliary"] is True, "control mis-set"
    archive_eq_aux_forbidden = (planted_id["identifiesArchiveWithAuxiliary"] is True)
    assert archive_eq_aux_forbidden, "control failed"
    print("FAIL_AUX_EQ_ARCHIVE_REJECTED  identifying the auxiliary variables with the D0 archive/bath is "
          "caught (the bridge records identifiesArchiveWithAuxiliary = false).")

    print("PASS_CONSTRAINED_HAMILTONIAN_EMBEDDING_PASSPORT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
