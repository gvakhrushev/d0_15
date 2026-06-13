#!/usr/bin/env python3
"""build_coverage_ledger.py - aggregate the BR0 audit-agent row files into the
canonical GOLDEN_COVERAGE_LEDGER (CSV + md), checked against the chunk manifest so
that EVERY chunk is guaranteed a verdict. This is the deterministic backbone of the
"nothing is missed" guarantee (the M1 failure mode).

Inputs (all under 03_THEORY_MAP/coverage_audit/):
  chunk_manifest.json   - authoritative chunk list (from chunk_sources.py)
  rows/<batch>.json     - one file per audit agent: {batch_id, rows:[{chunk_id, ...}]}
  critic/<name>.json    - completeness-critic corrections: {corrections:[{chunk_id,
                          revised_verdict?, revised_present?, critic_note}]}

Outputs:
  03_THEORY_MAP/GOLDEN_COVERAGE_LEDGER.csv  - one row per chunk (canonical worklist)
  03_THEORY_MAP/GOLDEN_COVERAGE_LEDGER.md   - human view + integrate worklist + gaps

Exit 0 if every chunk has a verdict row; exit 1 if chunks are missing a row
(so a failed/skipped batch is loud, never silently dropped).
"""
from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUD = ROOT / "03_THEORY_MAP" / "coverage_audit"
LEDGER_CSV = ROOT / "03_THEORY_MAP" / "GOLDEN_COVERAGE_LEDGER.csv"
LEDGER_MD = ROOT / "03_THEORY_MAP" / "GOLDEN_COVERAGE_LEDGER.md"

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

COLS = ["chunk_id", "layer", "book", "kind", "marker", "concept",
        "present_in_v14", "v14_locations", "verdict", "target_section",
        "strength", "note", "critic_flag", "critic_note"]

VALID_VERDICT = {"integrate", "already-present", "skip"}
VALID_PRESENT = {"yes", "partial", "no", ""}


def load_manifest() -> dict[str, dict]:
    data = json.loads((AUD / "chunk_manifest.json").read_text(encoding="utf-8"))
    return {c["chunk_id"]: c for c in data["chunks"]}


def load_rows() -> tuple[dict[str, dict], list[str]]:
    rows: dict[str, dict] = {}
    problems: list[str] = []
    for f in sorted((AUD / "rows").glob("*.json")):
        try:
            obj = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            problems.append(f"{f.name}: JSON parse error: {e}")
            continue
        for r in obj.get("rows", []):
            cid = r.get("chunk_id", "").strip()
            if not cid:
                problems.append(f"{f.name}: row with no chunk_id")
                continue
            rows[cid] = r
    return rows, problems


def load_critic() -> dict[str, dict]:
    corr: dict[str, dict] = {}
    cdir = AUD / "critic"
    if not cdir.exists():
        return corr
    for f in sorted(cdir.glob("*.json")):
        try:
            obj = json.loads(f.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        for c in obj.get("corrections", []):
            cid = c.get("chunk_id", "").strip()
            if cid:
                corr[cid] = c
    return corr


def norm_list(v) -> str:
    if isinstance(v, list):
        return "; ".join(str(x) for x in v)
    return str(v or "")


def main() -> int:
    manifest = load_manifest()
    rows, problems = load_rows()
    critic = load_critic()

    out_rows: list[dict] = []
    missing: list[str] = []
    for cid, m in manifest.items():
        r = rows.get(cid)
        if r is None:
            missing.append(cid)
            out_rows.append({
                "chunk_id": cid, "layer": m["layer"], "book": m["book"],
                "kind": m["kind"], "marker": m["marker"], "concept": "",
                "present_in_v14": "", "v14_locations": "", "verdict": "MISSING",
                "target_section": "", "strength": "", "note": "no audit row produced",
                "critic_flag": "", "critic_note": "",
            })
            continue
        verdict = str(r.get("verdict", "")).strip()
        present = str(r.get("present_in_v14", "")).strip()
        cf = critic.get(cid)
        flag = ""
        cnote = ""
        if cf:
            flag = "revised" if (cf.get("revised_verdict") or cf.get("revised_present")) else "reviewed"
            cnote = str(cf.get("critic_note", "")).strip()
            if cf.get("revised_verdict"):
                verdict = str(cf["revised_verdict"]).strip()
            if cf.get("revised_present"):
                present = str(cf["revised_present"]).strip()
        out_rows.append({
            "chunk_id": cid, "layer": m["layer"], "book": m["book"],
            "kind": m["kind"], "marker": m["marker"],
            "concept": str(r.get("concept", "")).strip(),
            "present_in_v14": present,
            "v14_locations": norm_list(r.get("v14_locations", "")),
            "verdict": verdict,
            "target_section": str(r.get("target_section", "")).strip(),
            "strength": str(r.get("strength", "")).strip(),
            "note": str(r.get("note", "")).strip(),
            "critic_flag": flag, "critic_note": cnote,
        })

    out_rows.sort(key=lambda d: d["chunk_id"])
    with LEDGER_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for d in out_rows:
            w.writerow(d)

    # --- summary / md view ---
    from collections import Counter
    by_verdict = Counter(d["verdict"] for d in out_rows)
    by_present = Counter(d["present_in_v14"] for d in out_rows if d["verdict"] != "MISSING")
    integrate = [d for d in out_rows if d["verdict"] == "integrate"]
    integrate_core = [d for d in integrate if d["strength"] == "core-forcing"]
    weaker = [d for d in out_rows if d["present_in_v14"] == "partial"]
    bad_verdict = [d for d in out_rows if d["verdict"] not in VALID_VERDICT and d["verdict"] != "MISSING"]

    md = ["# GOLDEN → v14 coverage ledger", "",
          f"Generated by `tools/build_coverage_ledger.py` from {len(manifest)} chunks.", "",
          "## Headline",
          f"- chunks total: **{len(out_rows)}**",
          f"- verdicts: {dict(by_verdict)}",
          f"- present_in_v14: {dict(by_present)}",
          f"- **integrate** rows (BR3 worklist): **{len(integrate)}** "
          f"(of which core-forcing: **{len(integrate_core)}**)",
          f"- partial/weaker restatements (M1 failure mode): **{len(weaker)}**", ""]
    if missing:
        md += [f"## ⚠ MISSING audit rows: {len(missing)}",
               "These chunks have no verdict — re-run their batch:", ""]
        md += [f"- `{c}`" for c in missing[:50]]
        if len(missing) > 50:
            md.append(f"- … +{len(missing) - 50} more")
        md.append("")
    if bad_verdict:
        md += [f"## ⚠ invalid verdicts: {len(bad_verdict)}", ""]
        md += [f"- `{d['chunk_id']}`: '{d['verdict']}'" for d in bad_verdict[:30]]
        md.append("")

    md += ["## Integrate worklist (core-forcing first)", "",
           "| chunk | book | kind | concept | target | note |",
           "|---|---|---|---|---|---|"]
    order = {"core-forcing": 0, "supporting": 1, "peripheral": 2, "": 3}
    for d in sorted(integrate, key=lambda x: (order.get(x["strength"], 3), x["chunk_id"])):
        concept = d["concept"].replace("|", "\\|")[:90]
        note = d["note"].replace("|", "\\|")[:90]
        md.append(f"| `{d['chunk_id']}` | {d['book']} | {d['kind']} | {concept} "
                  f"| {d['target_section']} | {note} |")
    md.append("")
    if weaker:
        md += ["## Partial / weaker restatements (strengthen in place)", "",
               "| chunk | concept | v14 location | note |", "|---|---|---|---|"]
        for d in sorted(weaker, key=lambda x: x["chunk_id"]):
            concept = d["concept"].replace("|", "\\|")[:80]
            note = d["note"].replace("|", "\\|")[:80]
            md.append(f"| `{d['chunk_id']}` | {concept} "
                      f"| {d['v14_locations']} | {note} |")
        md.append("")

    LEDGER_MD.write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")

    print(f"ledger: {len(out_rows)} rows -> {LEDGER_CSV.relative_to(ROOT).as_posix()}")
    print(f"verdicts={dict(by_verdict)} present={dict(by_present)}")
    print(f"integrate={len(integrate)} (core={len(integrate_core)}) weaker={len(weaker)}")
    if problems:
        print("PARSE PROBLEMS:")
        for p in problems:
            print("  " + p)
    if missing:
        print(f"RESULT: FAIL — {len(missing)} chunks missing an audit row")
        return 1
    if bad_verdict:
        print(f"RESULT: FAIL — {len(bad_verdict)} invalid verdicts")
        return 1
    print("RESULT: PASS — every chunk has a verdict")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
