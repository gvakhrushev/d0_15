#!/usr/bin/env python3
"""generate_lean_aggregates.py - regenerate the Lean aggregator/ledger files from
the canonical CLAIM_TO_LEAN_MAP.csv so they are never hand-edited (the two
highest-conflict serialization points for parallel formalization).

Generates:
  D0/All.lean                          - import every D0 module (release "build all")
  D0/TheoremLedger/ClaimMap.lean       - one ClaimMapEntry per CSV claim with a lean_module
  D0/TheoremLedger/ActiveClosureIndex.lean - import + #check the active per-claim modules
                                         (everything under D0/Claims/) + the final bridge index

Deterministic + idempotent: same CSV + same on-disk modules => byte-identical output,
so N agents that only append a CSV row / add a D0/Claims/<id>.lean never merge-conflict
on these files. Use --check to verify the committed files match a fresh generation.
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_theory_status_map as s  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

LEAN = s.ROOT / "09_LEAN_FORMALIZATION"
D0DIR = LEAN / "D0"
HEADER = "-- AUTO-GENERATED from CLAIM_TO_LEAN_MAP.csv by tools/generate_lean_aggregates.py.\n-- Do not edit by hand; run `python tools/generate_lean_aggregates.py`.\n"
EOL = "\n"

# Modules that must not enter the release build-all (known broken / intentionally out).
ALL_EXCLUDE: set[str] = set()

# CSV (lean_status, release_status) -> Lean ClaimStatus constructor.
def claim_status(lean_status: str, release: str) -> str:
    ls = lean_status.strip()
    rel = s.__dict__.get("_noop", None)  # placeholder to keep import used
    rel = release.strip()
    if ls == "LEAN_PROVED" and rel in ("NO_GO_PROVED", "NO-GO"):
        return "leanNoGoProved"
    if ls == "LEAN_PROVED":
        return "leanCoreProved"
    if ls == "LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS":
        return "leanBridgeAssumptionsExplicit"
    if ls == "PYTHON_CERTIFIED":
        return "pythonCertClosed"
    if ls == "OPEN":
        return "openObligation"
    if ls == "DEPRECATED":
        return "deprecated"
    return "notInLeanScope"


def module_name(path: Path) -> str:
    return path.relative_to(LEAN).as_posix()[:-len(".lean")].replace("/", ".")


def all_modules() -> list[str]:
    mods = []
    for p in sorted(D0DIR.rglob("*.lean")):
        m = module_name(p)
        if m == "D0.All" or m in ALL_EXCLUDE:
            continue
        mods.append(m)
    return sorted(set(mods))


def gen_all() -> str:
    lines = [HEADER, ""]
    lines += [f"import {m}" for m in all_modules()]
    return EOL.join(lines) + EOL


def gen_claimmap() -> str:
    rows = s.read_csv(s.CLAIM_MAP)
    entries = []
    for r in rows:
        mod = r.get("lean_module", "").strip()
        if not mod:                      # cert-only / passport rows are not Lean claims
            continue
        cid = r["claim_id"]
        thm = r.get("lean_theorem", "").strip()
        st = claim_status(r.get("lean_status", ""), r.get("release_status", ""))
        entries.append(
            f'    {{ claimId := "{cid}", moduleName := "{mod}",\n'
            f'      theoremName := "{thm}", status := ClaimStatus.{st} }}'
        )
    body = ",\n".join(entries)
    return (
        HEADER + "\n"
        "namespace D0\n\n"
        "inductive ClaimStatus where\n"
        "  | leanCoreProved\n"
        "  | leanBridgeAssumptionsExplicit\n"
        "  | pythonCertRequired\n"
        "  | pythonCertClosed\n"
        "  | empiricalDataRequired\n"
        "  | leanNoGoProved\n"
        "  | openObligation\n"
        "  | deprecated\n"
        "  | notInLeanScope\n"
        "  deriving DecidableEq, Repr\n\n"
        "structure ClaimMapEntry where\n"
        "  claimId : String\n"
        "  moduleName : String\n"
        "  theoremName : String\n"
        "  status : ClaimStatus\n\n"
        "def claimMap : List ClaimMapEntry :=\n  [\n"
        + body + "\n  ]\n\n"
        "theorem claimMap_nonempty : claimMap ≠ [] := by\n  decide\n\n"
        "end D0\n"
    )


def gen_active() -> str:
    claim_mods = sorted({module_name(p) for p in (D0DIR / "Claims").rglob("*.lean")}) if (D0DIR / "Claims").exists() else []
    lines = [HEADER, ""]
    for m in claim_mods:
        lines.append(f"import {m}")
    lines.append("import D0.Bridge.FinalBridgeIndex")
    lines.append("")
    lines.append("namespace D0")
    lines.append("")
    lines.append("-- Fast active gate: per-claim modules under D0/Claims/ + the final bridge index.")
    lines.append("#check D0.Bridge.D0_FINAL_FOUNDATION_INDEX")
    lines.append("")
    lines.append("end D0")
    return EOL.join(lines) + EOL


TARGETS = {
    "all": (D0DIR / "All.lean", gen_all),
    "claimmap": (D0DIR / "TheoremLedger" / "ClaimMap.lean", gen_claimmap),
    "active": (D0DIR / "TheoremLedger" / "ActiveClosureIndex.lean", gen_active),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if committed files differ from fresh generation")
    ap.add_argument("--only", choices=list(TARGETS), help="regenerate a single target")
    args = ap.parse_args()
    names = [args.only] if args.only else list(TARGETS)

    stale = []
    for name in names:
        path, gen = TARGETS[name]
        new = gen()
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if args.check:
            if old != new:
                stale.append(path.relative_to(s.ROOT).as_posix())
        else:
            # Path.write_text(newline=...) is Python 3.10+; open(newline=...) works on 3.9 too.
            with path.open("w", encoding="utf-8", newline="") as f:
                f.write(new)
            print(f"wrote {path.relative_to(s.ROOT).as_posix()}")
    if args.check:
        if stale:
            print("STALE (regenerate): " + ", ".join(stale))
            print("RESULT: FAIL")
            return 1
        print("RESULT: PASS (aggregates idempotent)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
