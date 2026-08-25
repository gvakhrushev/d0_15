#!/usr/bin/env python3
"""d0_value_model.py — how much each claim is WORTH, computed, not asserted.

The registry already answers "how well is this proved?" (`lean_status`, `release_status`) and the
scoreboard answers "how much strength is banked". Neither answers the question a reader and a
campaign planner actually need: **what would be lost if this claim vanished?** Without that axis
the corpus sorts by bookkeeping, its front door leads to whichever module has the loudest name,
and effort goes wherever it is cheapest rather than wherever it matters.

VALUE (0-100) is the sum of four measured components — every one of them derived from the
corpus itself, none hand-assigned:

  V1 STRUCTURAL WEIGHT (0-28)   how many claims transitively rest on this one
                                (`carries`, from tools/d0_logic_chain.py). If it falls, they fall.
  V2 SEMANTIC LOAD (0-20)       do its Lean statements QUANTIFY (bind a variable / forall / exists)
                                or are they closed numerals? A statement over a class can be
                                falsified by a second object; `(0:Z) < 6185264` cannot.
  V3 FALSIFIABILITY REACH (0-20) does it expose a surface an outsider can attack — an external
                                measurement (passport/empirical), a proved impossibility, or a
                                uniqueness/rigidity assertion that a second object would kill.
  V4 FOUNDATION POSITION (0-12)  near the genesis block AND carrying dependents: the layer whose
                                failure is not local.
  V5 EXTERNAL SIGNIFICANCE (0-20) does it answer a question the outside field already has? This is
                                the ONLY declared component; every weight names an external
                                question and a citation in D0_EXTERNAL_SIGNIFICANCE.csv, so it is
                                disputable per row. Without it the model is blind to exactly the
                                results that matter most to a reader outside the corpus - they
                                carry nothing internally and would sort as ballast.

STRENGTH (0-100) is the orthogonal axis: Lean-proved > python-certified > open, with an explicit
bridge discount (a claim holding modulo a named external theorem is not core-strength).

The two axes give the quadrants the refactor is FOR:

  ATTACK QUEUE   high value, low strength  -> the next campaign, ranked. This is the point.
  FRONT DOOR     high value, high strength -> what the README and the reading order must lead with
  BALLAST        low value, high strength  -> proved, cited by nothing: bottom of the registry
  DRIFT          low value, low strength   -> candidates for retirement, not for work

Outputs:
  09_LEAN_FORMALIZATION/docs/D0_VALUE_LEDGER.csv   machine-readable, one row per claim
  03_THEORY_MAP/D0_VALUE_RANKED.md                 the human view, quadrant-ordered

Re-run after any registry or Lean edit. Exit 0 = ok, 2 = IO/usage.
"""
from __future__ import annotations

import csv
import json
import math
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
LEAN_ROOT = ROOT / "09_LEAN_FORMALIZATION"
CHAIN = ROOT / "03_THEORY_MAP" / "D0_LOGIC_CHAIN.json"
OUT_CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "D0_VALUE_LEDGER.csv"
OUT_MD = ROOT / "03_THEORY_MAP" / "D0_VALUE_RANKED.md"

THM_RE = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|nonrec\s+)?(?:theorem|lemma)\s+([A-Za-z_][\w'.]*)", re.M)
BLOCK_COMMENT_RE = re.compile(r"/-.*?-/", re.S)
LINE_COMMENT_RE = re.compile(r"--.*")
NUMERIC_ONLY = re.compile(r"^[\s\d\+\-\*/\^%<>=≤≥≠()\[\]:,.|ℕℤℚℝ∧∨¬↔→'√]*$")
BINDER_RE = re.compile(r"[({\[]\s*[\w\s]+\s*:\s")

# V3: what makes a claim attackable from outside
EXTERNAL_STATUSES = {"EMPIRICAL-PASSPORT", "PASSPORT-CLOSED", "BRIDGE-CALIBRATION"}
IMPOSSIBILITY_STATUSES = {"NO-GO", "NO_GO_PROVED"}
RIGIDITY_TOKENS = ("UNIQUE", "FORCING", "FORCED", "RIGID", "NOGO", "NO-GO", "MINIMAL",
                   "MAXIMALITY", "EXHAUSTION", "SATURATION", "EXTREMAL", "FALSIFIER")

STRENGTH = {"LEAN_PROVED": 100, "LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS": 70,
            "PYTHON_CERTIFIED": 55, "OPEN": 5, "DEPRECATED": 0}


def statement_kinds(text: str) -> Counter:
    """Classify each theorem STATEMENT in a module: GENERAL (quantified) / APPLIED / GROUND."""
    text = BLOCK_COMMENT_RE.sub("", text)
    text = LINE_COMMENT_RE.sub("", text)
    kinds: Counter = Counter()
    for m in THM_RE.finditer(text):
        rest = text[m.end():m.end() + 4000]
        depth = cut = 0
        i = 0
        cut = len(rest)
        while i < len(rest):
            c = rest[i]
            if c in "([{":
                depth += 1
            elif c in ")]}":
                depth -= 1
            elif depth == 0 and rest.startswith(":=", i):
                cut = i
                break
            elif depth == 0 and c == "\n" and re.match(r"\n\s*(theorem|lemma|def|end|/-)", rest[i:]):
                cut = i
                break
            i += 1
        sig = rest[:cut]
        if BINDER_RE.search(sig) or "∀" in sig or "∃" in sig:
            kinds["GENERAL"] += 1
            continue
        depth = 0
        last = -1
        for i, c in enumerate(sig):
            if c in "([{":
                depth += 1
            elif c in ")]}":
                depth -= 1
            elif c == ":" and depth == 0 and not sig.startswith("::", i):
                last = i
        stmt = sig[last + 1:] if last >= 0 else sig
        kinds["GROUND" if NUMERIC_ONLY.match(stmt) else "APPLIED"] += 1
    return kinds


def citation_weight() -> Counter:
    """How often each claim_id is cited in the books and in other rows' notes.

    An OPEN claim has no Lean module, so it can never earn structural weight from the chain — yet
    an open row that ten sections are waiting on is the most valuable thing in the corpus. Citation
    count is the honest proxy for "how much already rests on this being closed".
    """
    cites: Counter = Counter()
    blob_parts = []
    for p in (ROOT / "01_BOOKS").glob("*.md"):
        blob_parts.append(p.read_text(encoding="utf-8", errors="ignore"))
    if REGISTRY.exists():
        blob_parts.append(REGISTRY.read_text(encoding="utf-8", errors="ignore"))
    blob = "\n".join(blob_parts)
    for cid in re.findall(r"D0-[A-Z0-9][A-Z0-9\-]{3,}-\d{3}", blob):
        cites[cid] += 1
    return cites


def external_significance() -> dict:
    """The ONE declared (not computed) component: does this claim answer a question the outside
    field already has? Kept in 03_THEORY_MAP/D0_EXTERNAL_SIGNIFICANCE.csv so that every weight
    carries a named external question and a citation, and can be disputed row by row rather than
    argued in prose. Absent file = component contributes zero everywhere."""
    path = ROOT / "03_THEORY_MAP" / "D0_EXTERNAL_SIGNIFICANCE.csv"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return {r["claim_id"].strip(): r for r in csv.DictReader(fh) if r.get("claim_id")}


def load_chain() -> dict:
    if not CHAIN.exists():
        subprocess.run([sys.executable, str(ROOT / "tools" / "d0_logic_chain.py")], check=False)
    return json.loads(CHAIN.read_text(encoding="utf-8"))["blocks"] if CHAIN.exists() else {}


def score(rows: list[dict], blocks: dict) -> list[dict]:
    max_carries = max((b["carries"] for b in blocks.values()), default=1) or 1
    cites = citation_weight()
    sig = external_significance()
    max_cites = max(cites.values(), default=1) or 1
    src_cache: dict[str, Counter] = {}
    out = []
    for r in rows:
        cid = (r.get("claim_id") or "").strip()
        if not cid:
            continue
        rel = (r.get("release_status") or "").strip()
        lean = (r.get("lean_status") or "").strip()
        blk = blocks.get(cid, {})
        carries = blk.get("carries", 0)
        depth = blk.get("depth", -1)

        # V1 structural weight — log-scaled so one giant hub does not flatten everything else.
        # Two channels, whichever is larger: what already rests on it (the chain), and what is
        # waiting on it (citations). Without the second channel every OPEN row scores zero.
        v1_chain = 28.0 * math.log1p(carries) / math.log1p(max_carries) if carries else 0.0
        n_cites = max(0, cites.get(cid, 0) - 1)  # discount the row's own registry line
        v1_cite = 28.0 * math.log1p(n_cites) / math.log1p(max_cites) if n_cites else 0.0
        v1 = max(v1_chain, v1_cite)

        # V2 semantic load — fraction of this claim's Lean statements that quantify
        kinds: Counter = Counter()
        for mod in blk.get("modules", []):
            if mod not in src_cache:
                p = LEAN_ROOT / (mod.replace(".", "/") + ".lean")
                src_cache[mod] = statement_kinds(p.read_text(encoding="utf-8", errors="ignore")) if p.exists() else Counter()
            kinds += src_cache[mod]
        total = sum(kinds.values())
        if total:
            v2 = 20.0 * (kinds["GENERAL"] + 0.45 * kinds["APPLIED"]) / total
        else:
            v2 = 6.0 if lean == "PYTHON_CERTIFIED" else 0.0

        # V3 falsifiability reach — an outsider must have somewhere to aim
        v3 = 0.0
        if rel in EXTERNAL_STATUSES:
            v3 += 14.0
        if rel in IMPOSSIBILITY_STATUSES:
            v3 += 11.0
        blob = f"{cid} {r.get('lean_theorem','')}".upper()
        if any(tok in blob for tok in RIGIDITY_TOKENS):
            v3 += 9.0
        if (r.get("python_cert") or "").strip():
            v3 += 4.0
        v3 = min(v3, 20.0)

        # V4 foundation position — shallow AND load-bearing
        if depth < 0 or carries == 0:
            v4 = 0.0
        else:
            v4 = 12.0 * (1.0 / (1.0 + depth)) * min(1.0, carries / 8.0)

        v5 = min(20.0, 6.7 * float(sig.get(cid, {}).get("weight", 0) or 0))
        value = round(min(100.0, v1 + v2 + v3 + v4 + v5), 1)
        strength = STRENGTH.get(lean, 5)
        if (r.get("uses_bridge_assumptions") or "").strip().lower() == "true" and strength > 70:
            strength = 70
        if rel == "PROOF-TARGET":
            # a Lean theorem covering one leg does not close the row; cap so the ranking cannot
            # show an open claim at full strength
            strength = min(strength, 45)
        out.append({
            "claim_id": cid,
            "value": value,
            "strength": strength,
            "quadrant": "",
            "carries": carries,
            "cites": n_cites,
            "rests_on": blk.get("rests_on", 0),
            "depth": depth if depth >= 0 else "",
            "genesis": blk.get("genesis", ""),
            "v1_structural": round(v1, 1),
            "v2_semantic": round(v2, 1),
            "v3_falsifiable": round(v3, 1),
            "v4_foundation": round(v4, 1),
            "v5_external": round(v5, 1),
            "value_floored": "",
            "external_question": sig.get(cid, {}).get("external_question", ""),
            "lean_status": lean,
            "release_status": rel,
            "book": (r.get("book") or "").strip(),
            "lean_module": (r.get("lean_module") or "").strip(),
        })

    live = [o for o in out if o["release_status"] != "DEPRECATED"]
    vs = sorted((o["value"] for o in live), reverse=True)
    v_cut = vs[max(0, int(len(vs) * 0.25) - 1)] if vs else 0

    # A newly identified OPEN target cannot earn structural weight: it has no Lean module (V2=0),
    # no chain position (V1,V4=0), and prose citations accrue only after it is written up. Its
    # ceiling is V5 alone, so the instrument whose job is to surface important new work would bury
    # exactly that. A declared weight-3 claim is therefore RAISED TO THE VISIBILITY THRESHOLD —
    # never above it: everything ranking higher got there by measurement, and declaration alone
    # buys visibility, not precedence. Inflation is blocked by check_value_ledger_sync, which fails
    # CI on a weight-3 claim that ranks as ballast or drift.
    for o in out:
        if sig.get(o["claim_id"], {}).get("weight", "").strip() == "3" and o["value"] < v_cut:
            o["value"] = v_cut
            o["value_floored"] = "declared-weight-3"

    for o in out:
        # "Closed" is the corpus's own word: it has an owner that discharges it. An open
        # PROOF-TARGET is not closed however strong its neighbours are.
        closed = (o["lean_status"] in ("LEAN_PROVED", "LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS",
                                       "PYTHON_CERTIFIED")
                  and o["release_status"] not in ("PROOF-TARGET", "DEPRECATED"))
        hv = o["value"] >= v_cut
        o["quadrant"] = ("FRONT-DOOR" if hv and closed else "ATTACK-QUEUE" if hv else
                         "BALLAST" if closed else "DRIFT")
    return out


def render(rows: list[dict], v_cut: float) -> str:
    q = lambda name: sorted((r for r in rows if r["quadrant"] == name),
                            key=lambda r: (-r["value"], -r["carries"]))

    def table(rs, n=25):
        out = ["| value | strength | carries | depth | claim | status |", "|---:|---:|---:|---:|---|---|"]
        for r in rs[:n]:
            out.append(f"| **{r['value']}** | {r['strength']} | {r['carries']} | {r['depth']} | "
                       f"`{r['claim_id']}` | {r['release_status']} |")
        if len(rs) > n:
            out.append(f"| … | | | | *+{len(rs)-n} more in the ledger CSV* | |")
        return "\n".join(out)

    aq, fd, bl, dr = q("ATTACK-QUEUE"), q("FRONT-DOOR"), q("BALLAST"), q("DRIFT")
    return f"""<!-- GENERATED by tools/d0_value_model.py — do not edit by hand. -->
# D0 — claims ranked by VALUE

*Value is computed, not assigned. Four components come from the corpus itself — structural weight
(how many claims transitively rest on it), semantic load (does the Lean statement quantify over a
class, or is it a closed numeral), falsifiability reach (can an outsider aim at it), foundation
position (shallow and load-bearing). One component is declared: external significance, where every
weight names the outside question it answers and cites a source
([D0_EXTERNAL_SIGNIFICANCE.csv](D0_EXTERNAL_SIGNIFICANCE.csv)) and is disputable row by row.
Strength is the orthogonal axis — how well the claim is closed. Regenerate with
`python tools/d0_value_model.py`; kept honest by `tools/check_value_ledger_sync.py`.*

High-value cut (top quartile): **{v_cut}**. Claims: {len(rows)}.

| quadrant | count | what it means |
|---|---:|---|
| **ATTACK QUEUE** | {len(aq)} | high value, not closed — **this is the work queue** |
| **FRONT DOOR** | {len(fd)} | high value, closed — what the README and reading order must lead with |
| BALLAST | {len(bl)} | closed but nothing rests on it — bottom of the registry |
| DRIFT | {len(dr)} | low value, not closed — retirement candidates, not campaign targets |

---

## 1. ATTACK QUEUE — highest value not yet closed

The next campaign, in order. Every row here is load-bearing or externally exposed **and** open:
closing it moves the corpus, closing anything below it does not.

{table(aq)}

---

## 2. FRONT DOOR — highest value already closed

This is the reading order for a new reader and the claim list for any external submission.
Nothing outside this table belongs in an abstract.

{table(fd)}

---

## 3. BALLAST — closed, but nothing rests on it

Proved and cited by no other claim. Not wrong, not worth foregrounding. Kept for completeness,
sorted to the bottom of the registry.

{table(bl, 15)}

---

## 4. DRIFT — low value and not closed

Neither load-bearing nor externally exposed nor closed. These are retirement candidates: work
spent here is bookkeeping. Review for merge into a parent claim or deprecation.

{table(dr, 15)}
"""


def main() -> int:
    try:
        with REGISTRY.open(encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))
        blocks = load_chain()
        scored = score(rows, blocks)
    except OSError as exc:
        print(f"IO error: {exc}", file=sys.stderr)
        return 2

    live = [o for o in scored if o["release_status"] != "DEPRECATED"]
    vs = sorted((o["value"] for o in live), reverse=True)
    v_cut = vs[max(0, int(len(vs) * 0.25) - 1)] if vs else 0

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(scored[0].keys()))
        w.writeheader()
        w.writerows(sorted(scored, key=lambda r: (-r["value"], -r["strength"])))
    OUT_MD.write_text(render(scored, v_cut), encoding="utf-8")

    c = Counter(r["quadrant"] for r in scored)
    print(f"value model: {len(scored)} claims | cut={v_cut} | " +
          " ".join(f"{k}={c[k]}" for k in ("FRONT-DOOR", "ATTACK-QUEUE", "BALLAST", "DRIFT")))
    print(f"wrote {OUT_CSV.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
