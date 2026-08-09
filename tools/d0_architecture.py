#!/usr/bin/env python3
"""d0_architecture.py — the shape of the corpus, measured on the right edges.

## Why this replaces the import-graph view

`d0_logic_chain.py` builds the derivation DAG from Lean `import` edges. That graph is real but it
answers the wrong question: **an import records proof-term reuse, not logical dependency.** The
Born-rule module `D0.Born` is imported by exactly two files, both index aggregators — yet every
statement about measurement in the corpus presupposes it. Ranking by import in-degree therefore
sorts the most foundational results to the bottom, which is what happened. The "205 genesis blocks"
that graph reports are not 205 independent foundations; they are 205 modules that happen not to
need each other's terms.

Conceptual dependency lives in the prose, where a section that establishes X cites the claims X
rests on. That is the edge set used here.

## Why multiplicity, not depth

A chain is FRAGILE: break one link and everything downstream falls. Depth is therefore the wrong
thing to maximise. A corpus built by forcing and destruction wants the opposite property — an
object reached by SEVERAL independent routes survives the loss of any one of them, and a kill that
removes one route tells you exactly which route was load-bearing. That is the antifragile shape,
and the corpus already pursues it in prose ("two independent forcings of φ", "two-channel forced",
"(3,1) from two distinct mechanisms", "neither leans on the other").

So the two measured quantities are:

  LOAD  L(c)   how many claims conceptually presuppose c — what falls if c falls
  SUPPORT m(c) how many independent routes establish c — how many must be killed to remove it

and the two derived readings are:

  FRAGILE JOINT   high L, m = 1   a single point of failure carrying real weight.
                                  **This is the value-creation queue**: proving a SECOND
                                  independent route to a fragile joint strengthens the whole
                                  building above it, and does so without needing any new
                                  empirical input.
  PILLAR          high L, m >= 2  load-bearing and already multiply supported — the parts of the
                                  structure an attacker cannot remove with one kill.

A leaf with L = 0 is decoration regardless of how well it is proved. A joint with high L and m = 1
is where the corpus is one refutation away from losing a whole sector.

Optional overlay: if `03_THEORY_MAP/D0_FORCING_ROUTES.json` exists (produced by the architecture
extraction pass, whose independence verdicts are adversarially checked), its VERIFIED-independent
route counts override the structural proxy for the claims it covers.

Outputs 03_THEORY_MAP/D0_ARCHITECTURE.md and D0_ARCHITECTURE.json. Exit 0 = ok, 2 = IO.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "01_BOOKS"
REGISTRY = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
ROUTES = ROOT / "03_THEORY_MAP" / "D0_FORCING_ROUTES.json"
OUT_MD = ROOT / "03_THEORY_MAP" / "D0_ARCHITECTURE.md"
OUT_JSON = ROOT / "03_THEORY_MAP" / "D0_ARCHITECTURE.json"

CLAIM_RE = re.compile(r"D0-[A-Z0-9][A-Z0-9\-]{3,}-(?:\d{3}|V\d+)")
SECTION_FILE_RE = re.compile(r"^\d{4}__([^_]+(?:_[^_]+)*?)__")

# Prose that marks a genuinely separate forcing route for the same object.
MULTI_ROUTE_RE = re.compile(
    r"two independent forcing|three independent|second,?\s+independent forcing|two-channel|"
    r"two distinct mechanisms|neither leans on the other|mutually reinforcing|"
    r"independent(?:ly)? forced|forced .{0,30}\btwo ways\b|a second, independent|"
    r"two separate forcing|independent route", re.I)


def load_registry() -> list[dict]:
    with REGISTRY.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def section_files() -> list[Path]:
    return sorted(p for d in BOOKS.iterdir() if d.is_dir() for p in d.glob("*.md"))


EVIDENCE_EDGES = ROOT / "03_THEORY_MAP" / "D0_PRESUPPOSITION_EDGES.json"


def evidence_edges(valid: set[str]) -> dict[str, set[str]]:
    """Evidence-backed claim→claim presupposition edges, each carrying a quoted reason.

    The section-level edges below are a coarse prior: every claim cited in a section inherits the
    same dependents, so co-cited claims end up with identical load (the 49/49/49 clusters). These
    edges are per-claim and were extracted with a stated reason, so they refine the ranking wherever
    they exist. Missing file = the coarse prior alone, which is the previous behaviour.
    """
    out: dict[str, set[str]] = defaultdict(set)
    if not EVIDENCE_EDGES.exists():
        return out
    try:
        data = json.loads(EVIDENCE_EDGES.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return out
    for e in data.get("edges", []):
        a, b = (e.get("claim") or "").strip(), (e.get("presupposes") or "").strip()
        if a in valid and b in valid and a != b:
            out[a].add(b)
    return out


def section_clusters(valid: set[str]) -> dict[str, tuple[str, int]]:
    """Claims that co-own a section, and how many share it.

    Section-derived edges give every co-owner the SAME dependents, so co-owners end up with an
    identical load that belongs to the section, not to any one of them. Reporting that number as if
    a single claim carried it puts a four-way tie at the top of the attack queue and hides that the
    load is unresolved. The cluster size is therefore carried explicitly, and a fragile joint in a
    cluster of size > 1 is flagged as section-resolution rather than claim-resolution.
    """
    reg = load_registry()
    buckets: dict[tuple[str, str], list[str]] = defaultdict(list)
    for r in reg:
        cid = (r.get("claim_id") or "").strip()
        sec = (r.get("section") or "").strip()
        book = (r.get("book") or "").strip()
        if cid in valid and sec:
            buckets[(book, sec)].append(cid)
    out: dict[str, tuple[str, int]] = {}
    for (book, sec), members in buckets.items():
        for cid in members:
            out[cid] = (f"{book} §{sec}", len(members))
    return out


def build_edges(valid: set[str]) -> tuple[dict[str, set[str]], dict[str, str], set[str]]:
    """Directed conceptual edges, at the finest resolution the prose supports.

The owner of a section is the claim (or claims) the registry assigns to that section number.
    Where the registry gives prose instead of a number, the owner is taken to be any claim whose id
    appears in the section's first heading block — the corpus writes the owner up front.

    RECORDED NEGATIVE (2026-07): a proximity refinement was tried and reverted. Attributing to each
    claim the other ids within a character window of *its own* mentions looked like the way to split
    a shared section load per claim. It is not: proximity is SYMMETRIC, so it emits an edge in both
    directions, every dense claim listing becomes a near-clique, the whole citation graph collapses
    into one strongly-connected component, and the transitive load degenerates to a single number
    shared by hundreds of claims (observed: 230-231 across a large block). A directed dependency
    needs an asymmetric signal — dependency LANGUAGE around the citation, or the evidence-backed
    edges in `D0_PRESUPPOSITION_EDGES.json` — not nearness. Section-level edges are asymmetric by
    construction (owner -> cited) and are therefore kept as the prior, with `resolution` disclosing
    where the load is still shared rather than attributed.
    """
    reg = load_registry()
    by_section: dict[tuple[str, str], list[str]] = defaultdict(list)
    for r in reg:
        cid = (r.get("claim_id") or "").strip()
        sec = (r.get("section") or "").strip()
        book = (r.get("book") or "").strip()
        if cid and sec:
            for b in re.split(r"[/,]", book):
                by_section[(b.strip(), sec)].append(cid)

    edges: dict[str, set[str]] = defaultdict(set)
    where: dict[str, str] = {}
    resolved: set[str] = set()
    for path in section_files():
        m = SECTION_FILE_RE.match(path.name)
        if not m:
            continue
        secnum = m.group(1)
        book = path.parent.name.split("_")[0] + "_" + path.parent.name.split("_")[1]
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        cited = {c for c in CLAIM_RE.findall(text) if c in valid}
        if not cited:
            continue

        owners = [c for c in by_section.get((book, secnum), []) if c in valid]
        if not owners:
            owners = [c for c in CLAIM_RE.findall(text[:1200]) if c in valid]
        for o in dict.fromkeys(owners):
            where.setdefault(o, f"{book} §{secnum}")
            edges[o] |= (cited - {o})
    return edges, where, resolved


def support_multiplicity(valid: set[str]) -> tuple[dict[str, int], dict[str, str]]:
    """How many independent routes establish each claim.

    Verified overlay first (adversarially checked route independence). Otherwise a structural
    proxy: distinct Lean theorems + distinct certificates backing the row, plus one if the prose
    around the claim explicitly asserts a second independent forcing. The proxy is deliberately
    conservative — it never invents a route the registry cannot show.
    """
    m: dict[str, int] = {}
    src: dict[str, str] = {}

    if ROUTES.exists():
        try:
            data = json.loads(ROUTES.read_text(encoding="utf-8"))
            for row in data.get("verified", []):
                for cid in row.get("claim_ids", []):
                    if cid in valid and row.get("independent"):
                        m[cid] = max(m.get(cid, 0), int(row.get("routes", 2)))
                        src[cid] = "verified"
            # Hand adjudications OVERRIDE the proxy, and override it downwards where the audit
            # found the asserted multiplicity absent. Without this the proxy keeps believing the
            # prose ("a second independent forcing") that the audit disproved, and inflates support
            # exactly where none exists.
            for row in data.get("adjudicated_by_hand", []):
                n = row.get("audited_support")
                if n is None:
                    continue
                for cid in row.get("target_claims", []):
                    if cid in valid:
                        m[cid] = int(n)
                        src[cid] = "audited"
        except (OSError, ValueError, TypeError):
            pass

    prose = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in BOOKS.glob("*.md"))
    multi_claims: set[str] = set()
    for mt in MULTI_ROUTE_RE.finditer(prose):
        window = prose[max(0, mt.start() - 700): mt.end() + 700]
        multi_claims |= {c for c in CLAIM_RE.findall(window) if c in valid}

    for r in load_registry():
        cid = (r.get("claim_id") or "").strip()
        if cid not in valid or cid in m:
            continue  # an audited or verified count is authoritative; never re-derive it
        thms = {t.strip() for t in re.split(r"[;,]", r.get("lean_theorem") or "") if t.strip()}
        certs = {t.strip() for t in re.split(r"[;,]", r.get("python_cert") or "") if t.strip()}
        n = (1 if thms else 0) + (1 if certs else 0)
        # several distinct theorems on one row are separate finite arguments for the same claim
        if len(thms) > 1:
            n += 1
        if cid in multi_claims:
            n += 1
        m[cid] = max(n, 1 if (thms or certs) else 0)
        src[cid] = "proxy"
    return m, src


def main() -> int:
    try:
        reg = load_registry()
        valid = {(r.get("claim_id") or "").strip() for r in reg if (r.get("claim_id") or "").strip()}
        live = {(r.get("claim_id") or "").strip() for r in reg
                if (r.get("release_status") or "").strip() != "DEPRECATED"}
        edges, where, resolved = build_edges(valid)
        clusters = section_clusters(valid)
        ev = evidence_edges(valid)
        for k, v in ev.items():
            edges[k] |= v
        mult, msrc = support_multiplicity(valid)
    except OSError as exc:
        print(f"IO error: {exc}", file=sys.stderr)
        return 2

    # LOAD: how many claims presuppose c (transitively, so a sector's weight reaches its root)
    direct: dict[str, set[str]] = defaultdict(set)
    for owner, deps in edges.items():
        for d in deps:
            direct[d].add(owner)

    load: dict[str, int] = {}
    for c in valid:
        seen: set[str] = set()
        stack = list(direct.get(c, ()))
        while stack:
            x = stack.pop()
            if x in seen or x == c:
                continue
            seen.add(x)
            stack.extend(direct.get(x, ()))
        load[c] = len(seen)

    status = {(r.get("claim_id") or "").strip(): (r.get("release_status") or "").strip() for r in reg}
    rows = []
    for c in sorted(live):
        L, m = load.get(c, 0), mult.get(c, 0)
        rows.append({
            "claim_id": c, "load": L, "support": m,
            "fragility": round(L / m, 1) if m else float(L),
            "pillar": L * m,
            "kind": ("PILLAR" if L >= 5 and m >= 2 else
                     "FRAGILE-JOINT" if L >= 5 and m <= 1 else
                     "SUPPORTED" if m >= 2 else "LEAF"),
            "support_source": msrc.get(c, ""), "status": status.get(c, ""),
            "where": where.get(c, ""),
            "cluster": clusters.get(c, ("", 1))[0],
            "cluster_size": clusters.get(c, ("", 1))[1],
            "resolution": ("claim" if c in resolved or clusters.get(c, ("", 1))[1] == 1
                           else "section"),
        })

    n_ev = sum(len(v) for v in evidence_edges(valid).values())
    kinds = Counter(r["kind"] for r in rows)
    frag = sorted((r for r in rows if r["kind"] == "FRAGILE-JOINT"), key=lambda r: -r["fragility"])
    pill = sorted((r for r in rows if r["kind"] == "PILLAR"), key=lambda r: -r["pillar"])
    verified_n = sum(1 for r in rows if r["support_source"] in ("verified", "audited"))

    def table(rs, cols, n=20):
        head = "| " + " | ".join(cols) + " |"
        sep = "|" + "|".join("---:" if c != "claim" and c != "where" else "---" for c in cols) + "|"
        out = [head, sep]
        for r in rs[:n]:
            out.append("| " + " | ".join(
                f"`{r['claim_id']}`" if c == "claim" else str(r.get(c.replace(" ", "_"), ""))
                for c in cols) + " |")
        if len(rs) > n:
            out.append(f"| *+{len(rs)-n} more in D0_ARCHITECTURE.json* |" + " |" * (len(cols) - 1))
        return "\n".join(out)

    n_unresolved = sum(1 for r in frag if r["cluster_size"] > 1)
    cols = ["claim", "load", "support", "resolution", "status"]
    md = f"""<!-- GENERATED by tools/d0_architecture.py — do not edit by hand. -->
# D0 — architecture: load, support, and where the building is thin

*Measured on CONCEPTUAL edges (a section that establishes X cites what X rests on), not on Lean
imports. An import records proof-term reuse; it is not logical dependency, and ranking by it sorts
the most foundational results to the bottom. See the module docstring for the worked case.*

**Load** `L` = how many claims transitively presuppose this one — what falls if it falls.
**Support** `m` = how many independent routes establish it — how many kills are needed to remove it.
{verified_n} claims carry an audited or adversarially-verified route count, which OVERRIDES the
structural proxy — including downwards, where the audit found an asserted second route absent. The
rest use the conservative proxy.

| shape | count | reading |
|---|---:|---|
| **FRAGILE JOINT** (L≥5, m≤1) | {kinds['FRAGILE-JOINT']} | carries weight on ONE route — **the value-creation queue** |
| **PILLAR** (L≥5, m≥2) | {kinds['PILLAR']} | load-bearing and multiply supported — survives a kill |
| SUPPORTED (L<5, m≥2) | {kinds['SUPPORTED']} | redundantly established but little rests on it |
| LEAF (L<5, m≤1) | {kinds['LEAF']} | decoration, however well proved |

---

## 1. FRAGILE JOINTS — where a second route creates the most value

These carry real weight on a single support. One successful refutation removes a whole sector.
Proving a **second independent forcing route** to any of them strengthens everything above it, needs
no new empirical input, and is the highest-value theorem available at any moment. Work here first.

`resolution = section` means the claim co-owns its section with others, so the load shown is the
**section's**, shared and not yet attributed — a tie at the top of this table is one unresolved
sector, not several independent targets. {n_unresolved} of {len(frag)} fragile joints are at section
resolution; resolving them needs evidence-backed per-claim edges, not more section citations.

{table(frag, cols)}

---

## 2. PILLARS — what the building actually stands on

High load and at least two independent routes. An attacker must kill every route to remove one of
these; the corpus's antifragility is exactly this column being non-empty.

{table(pill, ["claim", "load", "support", "pillar", "status"])}

---

## 3. Shape

Conceptual edges: {sum(len(v) for v in edges.values())} across {len(edges)} owning claims,
of which {n_ev} are evidence-backed per-claim edges (each carrying a quoted reason); the rest are
the coarse section-level prior, at which co-cited claims share a load value.
Claims carrying load ≥ 1: {sum(1 for r in rows if r['load'] >= 1)} of {len(rows)}.
Mean support multiplicity: {round(sum(r['support'] for r in rows)/max(1,len(rows)), 2)}.

A corpus of pillars over a narrow base is a pyramid; a corpus of fragile joints is a bush of
single-thread stems. The ratio {kinds['PILLAR']}:{kinds['FRAGILE-JOINT']} is the number to move.
"""
    OUT_MD.write_text(md, encoding="utf-8")
    OUT_JSON.write_text(json.dumps({"rows": rows, "summary": dict(kinds)}, indent=2, sort_keys=True),
                        encoding="utf-8")
    print(f"architecture: {len(rows)} claims | " + " ".join(f"{k}={v}" for k, v in kinds.most_common()))
    print(f"conceptual edges: {sum(len(v) for v in edges.values())} "
          f"({n_ev} evidence-backed) | verified route counts: {verified_n}")
    print(f"wrote {OUT_MD.relative_to(ROOT)} and {OUT_JSON.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
