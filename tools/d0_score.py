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
import os
import re
import stat as _stat
import subprocess
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


# --------------------------------------------------------------------------- #
# Repository hygiene / refactor KPI (second axis; deterministic git+file facts) #
# --------------------------------------------------------------------------- #

def _git(args: list[str]) -> list[str]:
    """git porcelain lines; [] on any failure (pattern from check_firewall.py)."""
    try:
        out = subprocess.run(["git", "-C", str(s.ROOT), *args],
                             capture_output=True, text=True, timeout=30)
        return out.stdout.splitlines() if out.returncode == 0 else []
    except Exception:  # noqa: BLE001
        return []


def _run(args: list[str]) -> str:
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=180,
                              cwd=str(s.ROOT)).stdout
    except Exception:  # noqa: BLE001
        return ""


_TAUT_RE = re.compile(r"\(\s*h\s*:\s*[^)]+\)\s*:\s*[^:=\n]+:=\s*h\b")
# trailing dev note `... # note` — but NOT a `## ` heading, NOT a LaTeX `\#`, and NOT
# inside a ``` code fence (`# x` is a legitimate comment in pseudocode blocks).
_DEV_COMMENT_RE = re.compile(r"(?<![\\#])\S[ \t]+#[ \t]+\S")


def count_dev_comments(text: str) -> tuple[int, list[str]]:
    """Real trailing dev-`# ...` notes, skipping fenced code blocks and LaTeX `\\#`."""
    n = 0
    hits: list[str] = []
    in_fence = False
    for i, ln in enumerate(text.splitlines(), 1):
        st = ln.lstrip()
        if st.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or st.startswith("#"):  # skip code + markdown headings
            continue
        if _DEV_COMMENT_RE.search(ln):
            n += 1
            if len(hits) < 6:
                hits.append(ln.strip()[:80])
    return n, hits
_PATH_LEAK_RES = [re.compile(p) for p in (
    r"vp_\w+\.py", r"\bD0\.[A-Z]\w+(?:\.\w+)+", r"05_CERTS/", r"03_THEORY_MAP/",
    r"06_AUDIT", r"_QUARANTINE/", r"(?<![\w.])add/", r"C:\\Users", r"/Users/", r"\.lake/")]


def hygiene_report(rows: list[dict]) -> dict:
    """Score repo cleanliness 0..budget from deterministic git+file signals.
    Every signal names offending files so the section doubles as a cleanup worklist."""
    D0DIR = s.ROOT / "09_LEAN_FORMALIZATION" / "D0"
    books = sorted((s.ROOT / "01_BOOKS").glob("BOOK_0*.md"))
    book_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in books)

    counts: dict[str, int] = {}
    evidence: dict[str, list[str]] = {}

    tt = _git(["ls-files", "add/", "_QUARANTINE/v17_overshoots/"])
    counts["tracked_meta_trash"] = len(tt); evidence["tracked_meta_trash"] = tt[:6]
    ti = _git(["ls-files", "-i", "-c", "--exclude-standard"])
    counts["tracked_but_ignored"] = len(ti); evidence["tracked_but_ignored"] = ti[:6]

    taut = []
    for p in D0DIR.rglob("*.lean"):
        n = len(_TAUT_RE.findall(p.read_text(encoding="utf-8", errors="replace")))
        if n:
            taut.append(f"{p.relative_to(D0DIR).as_posix()}:{n}")
    counts["tautology_proofs"] = sum(int(x.rsplit(':', 1)[1]) for x in taut)
    evidence["tautology_proofs"] = taut[:6]

    pd = []
    for p in D0DIR.rglob("*.lean"):
        for i, ln in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            st = ln.lstrip()
            if st.startswith("--") or st.startswith("/-") or st.startswith("*"):
                continue
            if re.search(r"\b(sorry|admit)\b|(^|\s)axiom\s", ln):
                pd.append(f"{p.name}:{i}")
    counts["proof_debt"] = len(pd); evidence["proof_debt"] = pd[:6]

    pc = _run([sys.executable, "tools/check_book_cert_references.py"])
    mph = re.search(r"(\d+)\s+PHANTOM", pc)
    counts["phantom_certs"] = int(mph.group(1)) if mph else 0

    prose_pt = len(re.findall(r"PROOF-TARGET", book_text))
    reg_pt = sum(1 for r in rows if m.canonical_release(r.get("release_status", "")) == "PROOF-TARGET")
    counts["orphan_proof_targets"] = max(0, prose_pt - reg_pt)

    dc = [count_dev_comments(p.read_text(encoding="utf-8", errors="replace")) for p in books]
    counts["dev_comments"] = sum(n for n, _ in dc)
    evidence["dev_comments"] = [h for _, hs in dc for h in hs][:6]
    counts["path_leaks"] = sum(len(rx.findall(book_text)) for rx in _PATH_LEAK_RES)

    cc = _run([sys.executable, "tools/check_v14_clean_corpus.py"])
    counts["corpus_errors"] = cc.count("\n  - ")

    # a real in-project .lake is bad; a junction/symlink to the external cache is fine.
    # On Windows a junction is a reparse point, which Path.is_symlink() does NOT detect.
    def _is_reparse(p: Path) -> bool:
        try:
            return bool(os.lstat(p).st_file_attributes & _stat.FILE_ATTRIBUTE_REPARSE_POINT)
        except AttributeError:
            return p.is_symlink()
        except OSError:
            return False
    lake = D0DIR.parent / ".lake"
    counts["real_in_project_lake"] = 1 if (lake.exists() and not _is_reparse(lake)
                                           and not lake.is_symlink() and (lake / "build").exists()) else 0

    counts["files_deleted_vs_base"] = len(_git(["diff", "--diff-filter=D", "--name-only", "base-v14", "HEAD"]))

    signals = []
    pen_total = 0.0
    for name, (unit, cap, label) in m.HYGIENE_PENALTIES.items():
        c = counts.get(name, 0)
        pts = min(c * unit, cap)
        pen_total += pts
        signals.append({"signal": name, "count": c, "points": -round(pts, 1),
                        "cap": -cap, "label": label, "evidence": evidence.get(name, [])})
    bon_total = 0.0
    for name, (unit, cap, label) in m.HYGIENE_BONUSES.items():
        c = counts.get(name, 0)
        pts = min(c * unit, cap)
        bon_total += pts
        signals.append({"signal": name, "count": c, "points": round(pts, 1),
                        "cap": cap, "label": label, "evidence": []})

    score = max(0.0, min(float(m.HYGIENE_BUDGET), m.HYGIENE_BUDGET - pen_total + bon_total))
    top_actions = sorted([x for x in signals if x["points"] < 0], key=lambda x: x["points"])
    return {
        "score": round(score, 1), "budget": m.HYGIENE_BUDGET,
        "penalty_total": round(pen_total, 1), "bonus_total": round(bon_total, 1),
        "signals": signals, "top_actions": top_actions,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="exit 1 on any integrity demotion")
    ap.add_argument("--top", type=int, default=25, help="rows per ranked list")
    ap.add_argument("--strict-hygiene", action="store_true",
                    help="exit 1 if the repository-hygiene score is below budget (opt-in; default off)")
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
    hygiene = hygiene_report(rows)
    payload["hygiene"] = hygiene
    (s.THEORY_DIR / "scoreboard.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    write_markdown(totals, by_domain, by_book, promotions, leverage_gaps, integrity, hygiene, args.top)

    print(f"d0_score: strength {realized}/{track_fair_max} ({totals['pct_strength']}%), "
          f"core headroom {totals['core_headroom']}, integrity demotions {len(integrity)}")
    print(f"d0_score: repo hygiene {hygiene['score']}/{hygiene['budget']} "
          f"(penalties -{hygiene['penalty_total']}, bonuses +{hygiene['bonus_total']})")
    if args.strict and integrity:
        print("RESULT: FAIL (integrity demotions under --strict)")
        return 1
    if args.strict_hygiene and hygiene["score"] < hygiene["budget"]:
        print(f"RESULT: FAIL (hygiene {hygiene['score']} < {hygiene['budget']} under --strict-hygiene)")
        return 1
    print("RESULT: PASS")
    return 0


def write_markdown(totals, by_domain, by_book, promotions, leverage_gaps, integrity, hygiene, top):
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

    # second axis: repository hygiene / refactor (cleanup is itself a tracked KPI)
    L.append("## Repository hygiene / refactor score\n")
    L.append(f"- **Hygiene:** {hygiene['score']} / {hygiene['budget']} "
             f"(penalties **-{hygiene['penalty_total']}**, bonuses **+{hygiene['bonus_total']}**) — "
             "cleanup *gains* points here; tracked meta-trash / fake proofs / book-clutter *lose* them.")
    L.append("")
    L.append("| signal | count | points | what to clean |")
    L.append("|---|--:|--:|---|")
    for x in hygiene["signals"]:
        ev = ("  ·  e.g. " + ", ".join(x["evidence"][:3])) if x.get("evidence") else ""
        L.append(f"| `{x['signal']}` | {x['count']} | {x['points']:+g} | {x['label']}{ev} |")
    L.append("")
    if hygiene["top_actions"]:
        L.append("**Top cleanup actions (most points to regain):** "
                 + "; ".join(f"`{a['signal']}` ({a['points']:+g})" for a in hygiene["top_actions"][:5]))
        L.append("")

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
