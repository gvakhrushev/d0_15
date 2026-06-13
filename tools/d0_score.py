#!/usr/bin/env python3
"""d0_score.py - track-fair strength scoreboard for the D0 claim tree.

Each claim is a node that climbs a maturity ladder; points accumulate per level
(increasing increments) up to CORE. Lateral tracks (no-go / bridge / passport /
external) are capped by the proved Lean firewall. The scoreboard shows total
strength, % of the track-fair maximum, core-potential headroom, and - the point -
*where points can still be gained cheapest*.

Source of truth: 09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv + on-disk
artifacts. Anti-gaming: a status can never score above what the filesystem
supports; a bridge can never score core points; deprecated is excluded.

Outputs 03_THEORY_MAP/SCOREBOARD.md + scoreboard.json. --strict exits 1 on any
integrity demotion (for CI). Exit 0 = ok, 2 = IO/usage.
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_theory_status_map as s  # noqa: E402
import d0_status_model as m  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Effort keyed by the TARGET level a claim is climbing into.
EFFORT = {2: "write cert scaffold", 3: "close finite cert", 4: "write Lean proof", 5: "release-bless to core"}


def track_of(release: str, uses_bridge: bool) -> str:
    if release == "DEPRECATED":
        return "DEPRECATED"
    if release in ("NO_GO_PROVED", "NO-GO"):
        return "NO_GO"
    if release in ("BRIDGE-ASSUMPTIONS-EXPLICIT", "BRIDGE-CALIBRATION", "CORE_BRIDGE_SPLIT") or uses_bridge:
        return "BRIDGE"
    if release == "EMPIRICAL-PASSPORT":
        return "PASSPORT"
    if release == "EXTERNAL-BACKGROUND":
        return "EXTERNAL"
    return "CORE"


def level_and_flag(release: str, lean_status: str, mods_ok: bool, certs_ok: bool, has_cert: bool):
    """Return (verified_level 0..5, integrity_flag_or_None). Declared level is
    capped by on-disk reality (the core anti-gaming invariant)."""
    if lean_status in ("LEAN_PROVED", "LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS"):
        if not mods_ok:
            return 1, "module_missing"
        if release == "CORE-FORMALIZED" and lean_status == "LEAN_PROVED":
            return 5, None
        return 4, None
    if lean_status == "PYTHON_CERTIFIED":
        if not (has_cert and certs_ok):
            return 2, "cert_missing"
        return 3, None
    if lean_status in ("", "DEPRECATED"):
        return 0, None
    return 1, None  # OPEN / proof-target


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="exit 1 on any integrity demotion")
    ap.add_argument("--top", type=int, default=25, help="rows per ranked list")
    args = ap.parse_args()

    rows = s.read_csv(s.CLAIM_MAP)

    # leverage adjacency: module/assumption -> set(claim_ids)
    mod_map: dict[str, set[str]] = {}
    asm_map: dict[str, set[str]] = {}
    for r in rows:
        for mm in s.split_values(r["lean_module"]):
            mod_map.setdefault(mm, set()).add(r["claim_id"])
        for aa in s.split_values(r["assumption_ids"]):
            asm_map.setdefault(aa, set()).add(r["claim_id"])

    scored: list[dict] = []
    seen: dict[str, int] = {}
    for r in rows:
        cid = r["claim_id"]
        seen[cid] = seen.get(cid, 0) + 1
        release = m.canonical_release(r["release_status"])
        lean_status = r["lean_status"].strip()
        uses_bridge = r.get("uses_bridge_assumptions", "").strip() == "True"
        mods = s.split_values(r["lean_module"])
        certs = s.split_values(r["python_cert"])
        mods_ok = bool(mods) and all(s.module_path(x).exists() for x in mods)
        certs_ok = all(s.cert_path(c).exists() for c in certs)
        has_cert = bool(certs)

        track = track_of(release, uses_bridge)
        level, flag = level_and_flag(release, lean_status, mods_ok, certs_ok, has_cert)
        ceiling = m.TRACK_CEILING[track]
        if track == "DEPRECATED":
            score = 0
        else:
            score = min(m.SPINE_CUMULATIVE[level], ceiling)

        neighbors: set[str] = set()
        for mm in mods:
            neighbors |= mod_map.get(mm, set())
        for aa in s.split_values(r["assumption_ids"]):
            neighbors |= asm_map.get(aa, set())
        leverage = len(neighbors - {cid})

        scored.append({
            "claim_id": cid, "track": track, "level": level,
            "level_name": m.SPINE_LEVEL_NAMES[level], "score": score, "ceiling": ceiling,
            "release_status": release, "lean_status": lean_status,
            "domain": s.claim_domain(r), "book": r["book"], "leverage": leverage,
            "integrity_flag": flag,
        })

    duplicates = [c for c, n in seen.items() if n > 1]
    active = [x for x in scored if x["track"] != "DEPRECATED"]
    realized = sum(x["score"] for x in active)
    track_fair_max = sum(x["ceiling"] for x in active)
    core = [x for x in active if x["track"] == "CORE"]
    core_potential = 20 * len(core)
    core_realized = sum(x["score"] for x in core)
    integrity = [x for x in scored if x["integrity_flag"]]

    # cheapest promotions: CORE claims with headroom, ranked by points gained then cheap effort
    promotions = []
    for x in core:
        if x["level"] >= 5:
            continue
        nxt = x["level"] + 1
        gain = m.SPINE_CUMULATIVE[nxt] - m.SPINE_CUMULATIVE[x["level"]]
        promotions.append({**{k: x[k] for k in ("claim_id", "domain", "book", "level_name", "leverage")},
                           "next": m.SPINE_LEVEL_NAMES[nxt], "points_gained": gain,
                           "effort": EFFORT[x["level"] + 1]})
    promotions.sort(key=lambda p: (-p["points_gained"], -p["leverage"]))

    leverage_gaps = sorted([x for x in core if x["level"] < 5],
                           key=lambda x: (-x["leverage"], -(20 - x["score"])))

    totals = {
        "realized": realized, "track_fair_max": track_fair_max,
        "pct_strength": round(100 * realized / track_fair_max, 1) if track_fair_max else 0.0,
        "core_realized": core_realized, "core_potential": core_potential,
        "core_headroom": core_potential - core_realized,
        "n_claims": len(scored), "n_active": len(active), "duplicates": duplicates,
        "integrity_demotions": len(integrity),
    }

    # per-domain / per-book aggregates
    def agg(key):
        out: dict[str, dict] = {}
        for x in active:
            g = out.setdefault(x[key], {"n": 0, "realized": 0, "max": 0, "core_headroom": 0})
            g["n"] += 1
            g["realized"] += x["score"]
            g["max"] += x["ceiling"]
            if x["track"] == "CORE":
                g["core_headroom"] += 20 - x["score"]
        return out

    by_domain = agg("domain")
    by_book = agg("book")

    payload = {
        "generated_from": "09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv",
        "ladder": {"spine_cumulative": m.SPINE_CUMULATIVE, "track_ceiling": m.TRACK_CEILING},
        "totals": totals, "by_domain": by_domain, "by_book": by_book,
        "cheapest_promotions": promotions, "leverage_gaps": [
            {k: x[k] for k in ("claim_id", "domain", "leverage", "level_name", "score")} for x in leverage_gaps],
        "integrity": [{k: x[k] for k in ("claim_id", "level_name", "score", "integrity_flag")} for x in integrity],
        "per_claim": scored,
    }
    (s.THEORY_DIR / "scoreboard.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    write_markdown(totals, by_domain, by_book, promotions, leverage_gaps, integrity, args.top)

    print(f"d0_score: strength {realized}/{track_fair_max} ({totals['pct_strength']}%), "
          f"core headroom {totals['core_headroom']}, integrity demotions {len(integrity)}")
    if args.strict and integrity:
        print("RESULT: FAIL (integrity demotions under --strict)")
        return 1
    print("RESULT: PASS")
    return 0


def write_markdown(totals, by_domain, by_book, promotions, leverage_gaps, integrity, top):
    L = []
    L.append("# D0 Theory Strength Scoreboard\n")
    L.append("_Generated from `CLAIM_TO_LEAN_MAP.csv` + on-disk artifacts by `tools/d0_score.py`. "
             "Track-fair: core spine L0->L5 = 1/2/4/7/12/20; ceilings no-go 12, bridge 11, passport 7, external 2._\n")
    L.append("## Headline\n")
    L.append(f"- **Realized strength:** {totals['realized']} / {totals['track_fair_max']} "
             f"(**{totals['pct_strength']}%** of track-fair max)")
    L.append(f"- **Core spine:** {totals['core_realized']} / {totals['core_potential']} "
             f"(headroom **{totals['core_headroom']}** points to take every core claim to L5)")
    L.append(f"- Claims: {totals['n_active']} active ({totals['n_claims']} total); "
             f"integrity demotions: {totals['integrity_demotions']}; duplicates: {len(totals['duplicates'])}\n")

    L.append("## Where to gain points next (cheapest promotions)\n")
    L.append("| claim | domain | at | -> | +pts | effort |")
    L.append("|---|---|---|---|--:|---|")
    for p in promotions[:top]:
        L.append(f"| `{p['claim_id']}` | {p['domain']} | {p['level_name']} | {p['next']} | "
                 f"{p['points_gained']} | {p['effort']} |")
    L.append("")

    L.append("## Highest-leverage open core gaps\n")
    L.append("| claim | domain | leverage | at | score |")
    L.append("|---|---|--:|---|--:|")
    for x in leverage_gaps[:top]:
        L.append(f"| `{x['claim_id']}` | {x['domain']} | {x['leverage']} | {x['level_name']} | {x['score']} |")
    L.append("")

    L.append("## By domain\n")
    L.append("| domain | n | realized | max | core headroom |")
    L.append("|---|--:|--:|--:|--:|")
    for d, g in sorted(by_domain.items(), key=lambda kv: -kv[1]["core_headroom"]):
        L.append(f"| {d} | {g['n']} | {g['realized']} | {g['max']} | {g['core_headroom']} |")
    L.append("")

    L.append("## By book\n")
    L.append("| book | n | realized | max | core headroom |")
    L.append("|---|--:|--:|--:|--:|")
    for b, g in sorted(by_book.items(), key=lambda kv: -kv[1]["realized"]):
        L.append(f"| {b} | {g['n']} | {g['realized']} | {g['max']} | {g['core_headroom']} |")
    L.append("")

    if integrity:
        L.append("## Integrity demotions (declared status above on-disk reality)\n")
        L.append("| claim | scored at | reason |")
        L.append("|---|---|---|")
        for x in integrity:
            L.append(f"| `{x['claim_id']}` | {x['level_name']} | {x['integrity_flag']} |")
        L.append("")

    (s.THEORY_DIR / "SCOREBOARD.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
