#!/usr/bin/env python3
"""validate_csv.py - integrity guard for the canonical D0 claim registry.

Canonical source of truth: 09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv
(+ LEAN_ASSUMPTION_LEDGER.csv). theory_status_map.csv and the graph are generated.

Checks: schema, canonical enums, on-disk artifact existence (catches phantom
modules/certs and the empty-cert PYTHON_CERTIFIED case), assumption FK, and
generated-view consistency (staleness). Exit 0 = pass, 1 = failures, 2 = IO/usage.
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_theory_status_map as s  # noqa: E402
import d0_status_model as m  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

EXPECTED_HEADER = [
    "claim_id", "book", "section", "lean_module", "lean_theorem", "lean_status",
    "uses_bridge_assumptions", "assumption_ids", "python_cert", "release_status", "notes",
]
GENERATED_CSV = s.THEORY_DIR / "theory_status_map.csv"

failures: list[str] = []
warnings: list[str] = []


def fail(check: str, claim: str, msg: str) -> None:
    failures.append(f"[{check}] {claim}: {msg}")


def warn(check: str, msg: str) -> None:
    warnings.append(f"[{check}] {msg}")


def main() -> int:
    if not s.CLAIM_MAP.exists():
        print(f"FATAL: canonical registry missing: {s.CLAIM_MAP}")
        return 2
    rows = s.read_csv(s.CLAIM_MAP)
    ledger_ids = {r["assumption_id"] for r in s.read_csv(s.ASSUMPTION_LEDGER)}

    # A. schema
    header = list(rows[0].keys()) if rows else []
    if header != EXPECTED_HEADER:
        fail("schema", "<header>", f"expected {EXPECTED_HEADER}, got {header}")
    seen_ids: dict[str, int] = {}

    for r in rows:
        cid = r.get("claim_id", "").strip()
        if not cid:
            fail("schema", "<row>", "empty claim_id")
            continue
        seen_ids[cid] = seen_ids.get(cid, 0) + 1
        lean_status = r.get("lean_status", "").strip()
        release = r.get("release_status", "").strip()
        ub = r.get("uses_bridge_assumptions", "").strip()

        # B. enums
        if release not in m.CANONICAL_RELEASE_STATUS:
            sugg = m.canonical_release(release)
            hint = f" -> collapse to {sugg}" if sugg in m.CANONICAL_RELEASE_STATUS else ""
            fail("enum", cid, f"non-canonical release_status '{release}'{hint}")
        if lean_status not in m.VALID_LEAN_STATUS:
            fail("enum", cid, f"invalid lean_status '{lean_status}'")
        if ub not in {"True", "False"}:
            fail("enum", cid, f"uses_bridge_assumptions must be True/False, got '{ub}'")

        # C. artifact existence
        mods = s.split_values(r.get("lean_module", ""))
        certs = s.split_values(r.get("python_cert", ""))
        if lean_status in {"LEAN_PROVED", "LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS"}:
            if not mods:
                fail("artifact", cid, f"{lean_status} but no lean_module listed")
            elif not s.modules_exist(r["lean_module"]):
                missing = [mm for mm in mods if not s.module_path(mm).exists()]
                fail("artifact", cid, f"{lean_status} but module(s) absent: {missing}")
        if lean_status == "PYTHON_CERTIFIED":
            if not certs:
                fail("artifact", cid, "PYTHON_CERTIFIED but python_cert is empty")
            else:
                missing = [c for c in certs if not s.cert_path(c).exists()]
                if missing:
                    fail("artifact", cid, f"PYTHON_CERTIFIED but cert(s) absent: {missing}")

        # D. assumption FK + firewall coupling
        aids = s.split_values(r.get("assumption_ids", ""))
        for aid in aids:
            if aid not in ledger_ids:
                fail("fk", cid, f"assumption_id '{aid}' not in ledger")
        if ub == "True" and not aids:
            fail("fk", cid, "uses_bridge_assumptions=True but assumption_ids empty")
        if ub == "False" and aids:
            fail("fk", cid, "uses_bridge_assumptions=False but assumption_ids present")

    for cid, n in seen_ids.items():
        if n > 1:
            fail("schema", cid, f"duplicate claim_id ({n} rows)")

    # E. generated-view consistency (staleness)
    if GENERATED_CSV.exists():
        gen = {g["claim_id"]: g for g in s.read_csv(GENERATED_CSV)}
        if len(gen) != len(rows):
            warn("stale", f"generated theory_status_map.csv has {len(gen)} rows vs canonical {len(rows)} -> run regen_graph")
        for r in rows:
            cid = r["claim_id"]
            g = gen.get(cid)
            if not g:
                continue
            disk_mod = "True" if s.modules_exist(r["lean_module"]) else "False"
            disk_cert = "True" if all(s.cert_path(c).exists() for c in s.split_values(r["python_cert"])) else "False"
            if g.get("module_exists") not in (None, disk_mod):
                warn("stale", f"{cid}: generated module_exists={g.get('module_exists')} != disk {disk_mod}")
            if g.get("certs_exist") not in (None, disk_cert):
                warn("stale", f"{cid}: generated certs_exist={g.get('certs_exist')} != disk {disk_cert}")
    else:
        warn("stale", "generated theory_status_map.csv absent -> run regen_graph")

    # report
    print(f"validate_csv: {len(rows)} canonical claim rows")
    if warnings:
        print(f"\n-- {len(warnings)} staleness warning(s) (non-fatal; resolved by Phase 4 regen) --")
        for w in warnings[:40]:
            print("  " + w)
        if len(warnings) > 40:
            print(f"  ... +{len(warnings) - 40} more")
    if failures:
        print(f"\n!! {len(failures)} FAILURE(S) (the Phase 3 worklist):")
        by_check: dict[str, list[str]] = {}
        for f in failures:
            k = f.split("]")[0].strip("[")
            by_check.setdefault(k, []).append(f)
        for k, items in sorted(by_check.items()):
            print(f"  -- {k}: {len(items)}")
            for it in items[:30]:
                print("    " + it)
            if len(items) > 30:
                print(f"    ... +{len(items) - 30} more")
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
