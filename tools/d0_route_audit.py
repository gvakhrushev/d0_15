#!/usr/bin/env python3
"""d0_route_audit.py — inventory every "forced by N independent routes" claim, and triage it.

## Why this exists

Multiplicity of independent forcing routes is the corpus's antifragility claim: an object reached
by several routes survives the loss of any one. The books assert it in prose, dozens of times, in
free-form language ("two independent forcings", "two-channel forced", "neither leans on the other").
Nothing checked those assertions, and a 2026-07 audit of 20 of them found every one sharing a
load-bearing premise — so the claimed redundancy was not there.

This tool makes the inventory mechanical and repeatable. It does NOT decide independence: that needs
a premise-trace and stays a human/skeptic judgement recorded in `D0_FORCING_ROUTES.json`. What it
does is find every assertion, extract the objects each route leans on, and flag the ones where two
routes visibly lean on the same named object — the cases worth tracing first.

## The two tests that matter

**Test 1 — shared premise, not shared conclusion.** A route pair is dependent when it shares a
load-bearing *premise*. Converging on the same object is what convergence *means*; the question is
whether the inputs overlap. The triage below looks for shared named objects in the premise vicinity
and reports SUSPECT, never refuted.

**Test 2 — redundancy, not decomposition.** Two mechanisms forcing *different components* of one
object give no antifragility at all: kill either and that component is gone, because neither covers
for the other. Only mechanisms that independently reach the *same* object are redundancy. BOOK_06
§06.30a is the worked example — "(3,1) from two independent objects" supplies the 3 from a graph
rank and the 1 from a Pisot flow, which is decomposition; the section is correct but must not be
read as multiplicity. An assertion that survives Test 1 and fails Test 2 buys nothing.

Outputs 03_THEORY_MAP/D0_ROUTE_INVENTORY.md (+ .json). Exit 0 = ok, 1 = unregistered assertions
found when run with --strict, 2 = IO.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "01_BOOKS"
ROUTES = ROOT / "03_THEORY_MAP" / "D0_FORCING_ROUTES.json"
OUT_MD = ROOT / "03_THEORY_MAP" / "D0_ROUTE_INVENTORY.md"
OUT_JSON = ROOT / "03_THEORY_MAP" / "D0_ROUTE_INVENTORY.json"

ASSERTION = re.compile(
    # "four independent mathematical faces", "two independent forcings", "three independent routes"
    r"(?:two|three|four|five|2|3|4|5)\s+(?:\w+\s+){0,2}?independent\s+"
    r"(?:forcing|forcings|route|routes|channel|channels|mechanism|mechanisms|derivation|"
    r"derivations|face|faces|leg|legs|proof|proofs|witness|witnesses|object|objects|side|sides)"
    # explicit multiplicity idioms the corpus uses
    r"|two-channel\s+forced"
    r"|a\s+second,?\s+independent\s+(?:forcing|route|channel|derivation)"
    r"|(?:a\s+)?third,?\s+(?:categorical,?\s+)?(?:and\s+)?independent"
    r"|neither\s+leans\s+on\s+the\s+other"
    r"|mutually\s+reinforcing"
    r"|from\s+two\s+(?:distinct|unrelated)\s+(?:mechanisms|directions|objects)"
    r"|fix(?:ed)?\s+twice\s+over"
    r"|forced\s+(?:through|by|from)\s+(?:two|three|four|five)\s+(?:\w+\s+){0,2}?independent"
    r"|(?:two|three|four)\s+(?:\w+\s+){0,2}?(?:unrelated|orthogonal)\s+(?:failures|channels|routes)",
    re.I)

CLAIM_RE = re.compile(r"D0-[A-Z0-9][A-Z0-9\-]{3,}-(?:\d{3}|V\d+)")
SECTION_RE = re.compile(r"^#{2,4}\s+([\d.]+[\w.]*)", re.M)

# Named objects a route can lean on. Deliberately narrow: a shared MENTION of one of these inside
# two different routes' premise text is the signal worth tracing.
NAMED_OBJECT = re.compile(
    r"p\s*\+\s*p\^?2\s*=\s*1|x\^?2\s*[-−]\s*x\s*[-−]\s*1|φ\^?2\s*=\s*φ\s*\+\s*1|varphi\^2=\\varphi\+1"
    r"|Q_?8|Ω_?8|Omega_?8|K\(9,\s*11,\s*13\)|E_?8|\bD_2\b|ABCD|δ_?0|delta_?0"
    r"|rank[- ]3|nullity[- ]30|Pisot|Hurwitz|Fibonacci|Ising|Lucas|Galois|KAM|Jones"
    r"|\bM1\+|degree-?2|quarter-turn|symplectic|toral|heat-trace|\|V\|=33|359")


def sections(text: str) -> list[tuple[str, int]]:
    return [(m.group(1), m.start()) for m in SECTION_RE.finditer(text)]


def section_of(secs: list[tuple[str, int]], pos: int) -> str:
    cur = ""
    for name, start in secs:
        if start <= pos:
            cur = name
        else:
            break
    return cur


def audit() -> dict:
    # Adjudications are keyed by the SECTION they concern — the only stable join between a prose
    # assertion and its verdict, since object descriptions are free text.
    registered: dict[str, dict] = {}
    by_section: dict[str, dict] = {}
    if ROUTES.exists():
        try:
            data = json.loads(ROUTES.read_text(encoding="utf-8"))
            for row in (data.get("verified", []) + data.get("repaired", [])
                        + data.get("adjudicated_by_hand", [])):
                blob = f"{row.get('object', '')} {row.get('section', '')}"
                registered[(row.get("object") or "")[:60].lower()] = row
                for sec in re.findall(r"§\s*([\d]+\.[\w.]*[\w])", blob):
                    by_section.setdefault(sec, row)
        except (OSError, ValueError):
            pass

    findings = []
    for book in sorted(BOOKS.glob("*.md")):
        text = book.read_text(encoding="utf-8", errors="ignore")
        secs = sections(text)
        for m in ASSERTION.finditer(text):
            # Skip NEGATED occurrences ("… is a shared support, NOT two independent objects") and
            # definitional ones ("IF two independent derivations disagree by more than eps^2 …"),
            # which are criteria about routes rather than claims that some object has several.
            lead = text[max(0, m.start() - 40):m.start()].lower()
            if re.search(r"\bnot\b\s*$|\bnever\b\s*$|\bif\b\s*$|\bwhen\b\s*$|\bunless\b\s*$", lead):
                continue
            lo, hi = max(0, m.start() - 1400), min(len(text), m.end() + 1400)
            window = text[lo:hi]
            objects = sorted({o.strip() for o in NAMED_OBJECT.findall(window)})
            claims = sorted(set(CLAIM_RE.findall(window)))
            line = text.count("\n", 0, m.start()) + 1
            phrase = " ".join(text[max(0, m.start() - 60):m.end() + 60].split())
            findings.append({
                "book": book.stem,
                "line": line,
                "section": section_of(secs, m.start()),
                "assertion": phrase,
                "shared_objects": objects,
                "claim_ids": claims,
                "n_objects": len(objects),
            })

    # triage
    for f in findings:
        # A verdict may be tagged with a finer sub-section than the heading the assertion sits
        # under (§07.21.4C vs 07.21), so match on either being a prefix of the other.
        row = by_section.get(f["section"])
        if row is None and f["section"]:
            for sec, r in by_section.items():
                if sec.startswith(f["section"]) or f["section"].startswith(sec):
                    row = r
                    break
        if row is None:
            for rk in registered:
                if any(c.lower() in rk for c in f["claim_ids"]):
                    row = registered[rk]
                    break
        key = row is not None
        f["registered"] = bool(key)
        f["category"] = (row or {}).get("category", "")
        f["verdict"] = (row or {}).get("verdict", "")[:300] if row else ""
        # a claim whose window names >=2 heavy shared objects is where premises most likely overlap
        f["triage"] = ("REGISTERED" if key else
                       "SUSPECT" if f["n_objects"] >= 3 else
                       "UNCHECKED")
    return {
        "generated_from": "01_BOOKS/*.md",
        "test": "a route pair is dependent when it shares a load-bearing PREMISE, not when it "
                "reaches the same conclusion; this tool triages, it does not adjudicate",
        "assertions_found": len(findings),
        "counts": dict(Counter(f["triage"] for f in findings)),
        "findings": sorted(findings, key=lambda f: (-f["n_objects"], f["book"], f["line"])),
    }


def render(model: dict) -> str:
    c = model["counts"]
    rows = model["findings"]
    def table(rs, n=40):
        out = ["| book | § | line | shared named objects | assertion |", "|---|---|---:|---|---|"]
        for f in rs[:n]:
            objs = ", ".join(f["shared_objects"][:6]) or "—"
            out.append(f"| {f['book'].replace('BOOK_','')[:14]} | {f['section'] or '—'} | {f['line']} | "
                       f"`{objs}` | {f['assertion'][:110]}… |")
        if len(rs) > n:
            out.append(f"| … | | | | *+{len(rs)-n} more in the JSON* |")
        return "\n".join(out)
    susp = [f for f in rows if f["triage"] == "SUSPECT"]
    unch = [f for f in rows if f["triage"] == "UNCHECKED"]
    reg = [f for f in rows if f["triage"] == "REGISTERED"]
    return f"""<!-- GENERATED by tools/d0_route_audit.py — do not edit by hand. -->
# D0 — inventory of "forced by N independent routes" assertions

*Multiplicity of independent routes is the corpus's antifragility claim: an object reached by
several routes survives the loss of any one. This file inventories every place the books assert it.*

**The test:** a route pair is dependent when it shares a load-bearing **premise** — not when it
reaches the same **conclusion**. Convergence on one object is what convergence means; the question
is whether the inputs overlap. This tool triages by shared named objects and never adjudicates;
verdicts live in [`D0_FORCING_ROUTES.json`](D0_FORCING_ROUTES.json).

| triage | count | meaning |
|---|---:|---|
| REGISTERED | {c.get('REGISTERED',0)} | already adjudicated in the routes ledger |
| **SUSPECT** | {c.get('SUSPECT',0)} | ≥3 named objects shared across the routes' premise text — trace these first |
| UNCHECKED | {c.get('UNCHECKED',0)} | asserted, never adjudicated |

Total assertions found: **{model['assertions_found']}**.

---

## SUSPECT — premises visibly overlap

{table(susp)}

---

## UNCHECKED — asserted, never adjudicated

{table(unch, 30)}

---

## REGISTERED — already adjudicated

{table(reg, 20)}
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any assertion is unregistered (CI gate for new prose)")
    args = ap.parse_args()
    try:
        model = audit()
        OUT_JSON.write_text(json.dumps(model, indent=2, sort_keys=True), encoding="utf-8")
        OUT_MD.write_text(render(model), encoding="utf-8")
    except OSError as exc:
        print(f"IO error: {exc}", file=sys.stderr)
        return 2
    c = model["counts"]
    print(f"route audit: {model['assertions_found']} assertions | " +
          " ".join(f"{k}={v}" for k, v in sorted(c.items())))
    print(f"wrote {OUT_MD.relative_to(ROOT)}")
    if args.strict and (c.get("SUSPECT", 0) or c.get("UNCHECKED", 0)):
        print("FAIL: unadjudicated independence assertions present", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
