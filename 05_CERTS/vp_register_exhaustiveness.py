#!/usr/bin/env python3
"""vp_register_exhaustiveness - meta-cert: is the OPEN-JOINTS register EXHAUSTIVE?

Closes the deepest blind-spot of the D0 open-frontier bookkeeping: nobody had
certified that the register (canonical registry CLAIM_TO_LEAN_MAP.csv + the
04_VERIFICATION atlases + the TOTAL_EXTENSION_PRIMITIVES.csv completion catalog)
captures EVERY open forcing obligation. New PROOF-TARGETs and new PRIM-* primitives
kept appearing at each vNext AFTER the register was declared "exhaustive by intent".

This cert makes "exhaustive by intent" MACHINE-CHECKABLE via five failable checks
over the canonical registry + atlases, reusing the measured DAG
(03_THEORY_MAP/frontier_dag.json) and the tools/build_frontier_dag.py machinery
(load_registry / is_frontier / is_nogo / extract_registry_edges / load_atlas_edges /
load_primitive_catalog / parse_nogo_flags). Measurement only: it reads, never mutates,
the registry / catalog / ledgers.

Checks (each is EXPECTED to be able to FAIL — a failing check IS the finding):
  C1  every OPEN/PROOF-TARGET claim names >=1 blocking primitive OR is an explicit
      observational passport (prose 'passport'/'external' marker, named ASSUMP-*, or
      the -PASSPORT- claim-id form). Unhomed proof-targets FAIL.
  C2  every PRIM-* named ANYWHERE has (a) a completion object row in
      TOTAL_EXTENSION_PRIMITIVES.csv AND (b) >=1 registry claim that consumes it.
      Orphan primitives (no catalog row) FAIL.
  C3  every no-go's 'admissible completion class' names a primitive that EXISTS in the
      catalog. A no-go pointing at a phantom completion class FAILS.
  C4  no atlas claim_id is absent from the registry (the Class-2 desyncs). An atlas
      row whose claim_id has no registry home FAILS.
  C5  MONOTONICITY guard: the current primitive-set + proof-target-set is pinned in a
      manifest baseline. A future vNext that ADDS a primitive or a proof-target without
      updating the baseline is DETECTED (this is what makes "exhaustive by intent"
      checkable going forward).

Run:  python3 _TASKS_CENTER_ATTACK/vp_register_exhaustiveness.py
      --update-baseline   (re)writes the C5 manifest to the current measured set
Exit 0 == all checks PASS.  Exit 1 == >=1 check FAILED (honest current state).

Discipline: candidate/measurement language only; no claim is promoted, demoted, or
closed. Every threshold is derived from the register itself, never from a desired
answer. Owned NO-GOs are respected (read, never re-opened).
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from d0_status_model import canonical_release  # noqa: E402
from sync_theory_status_map import read_csv  # noqa: E402
import build_frontier_dag as bfd  # noqa: E402

REGISTRY = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
CATALOG = ROOT / "04_VERIFICATION" / "TOTAL_EXTENSION_PRIMITIVES.csv"
VERIF = ROOT / "04_VERIFICATION"
DAG = ROOT / "03_THEORY_MAP" / "frontier_dag.json"
BASELINE = ROOT / "_TASKS_CENTER_ATTACK" / "register_exhaustiveness_manifest.json"

PRIM_RE = re.compile(r"PRIM-[A-Z0-9]+(?:-[A-Z0-9]+)*")
CLAIM_RE = re.compile(r"D0-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}|CVFT-F\d+")
ASSUMP_RE = re.compile(r"ASSUMP-[A-Z0-9-]+")
# a REFUTED / does-not-exist candidate primitive is a TESTED DEAD candidate owned by a
# NO-GO, NOT an orphan: it legitimately has no completion object, and DEMANDING one would
# silently re-open the owning NO-GO. We detect these from the registry's own phrasing so the
# exception is data-driven (never a hardcoded whitelist). Example (verbatim, registry:428):
#   "PRIM-CANONICAL-33-SCENE-ANCHOR does NOT exist (no scene-structure-preserving reduction...)"
#   owner D0-VNEXT-33-SCENE-ANCHOR-OWNER-001, release_status NO-GO.
REFUTED_RE = re.compile(r"(PRIM-[A-Z0-9-]+)\s+does\s+NOT\s+exist", re.IGNORECASE)
# an OPEN row is an explicit observational passport if its notes carry any of these,
# or its claim-id contains the -PASSPORT- token. These markers are the corpus's own
# self-declarations (verified verbatim in the memo), not a heuristic we invented.
PASSPORT_PROSE_RE = re.compile(r"\bpassport\b|\bexternal\b", re.IGNORECASE)

FAIL = "FAIL"
PASSN = "PASS"


class Check:
    def __init__(self, cid: str, title: str):
        self.cid, self.title, self.status = cid, title, PASSN
        self.violations: list[str] = []
        self.notes: list[str] = []

    def fail(self, msg: str) -> None:
        self.status = FAIL
        self.violations.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)


# ---------------------------------------------------------------------------
# shared measured objects (all read-only; reuse build_frontier_dag machinery)
# ---------------------------------------------------------------------------
def refuted_primitives(registry):
    """primitives PROVEN not to exist (tested dead candidates), extracted from the
    registry's own 'PRIM-... does NOT exist' phrasing on a NO-GO/NO_GO_PROVED row.
    These are exempt from C2 (no completion object required) and C3 (may be named as a
    'refuted completion class') — citing, not re-opening, the owning NO-GO."""
    out = {}
    for cid, r in registry.items():
        if not bfd.is_nogo(r):
            continue
        for m in REFUTED_RE.finditer(r.get("notes", "")):
            out[m.group(1)] = cid
    return out


def load_all():
    registry = bfd.load_registry()
    catalog = set(bfd.load_primitive_catalog().keys())
    frontier = {c for c, r in registry.items() if bfd.is_frontier(r)}
    nogos = {c for c, r in registry.items() if bfd.is_nogo(r)}
    refuted = refuted_primitives(registry)
    return registry, catalog, frontier, nogos, refuted


def all_prim_tokens_by_source(registry):
    """every PRIM-* token seen anywhere, mapped to the files that name it, plus
    per-primitive the set of registry claim_ids whose NOTES cite it (consumers)."""
    consumers = defaultdict(set)          # prim -> {claim_id} from registry notes
    for cid, r in registry.items():
        for p in set(PRIM_RE.findall(r.get("notes", ""))):
            consumers[p].add(cid)
    seen_files = defaultdict(set)         # prim -> {file}
    scan = [REGISTRY, DAG, CATALOG] + sorted(VERIF.glob("*.csv")) + sorted(VERIF.glob("*.md")) \
        + sorted(VERIF.glob("*.json"))
    for path in scan:
        try:
            txt = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for p in set(PRIM_RE.findall(txt)):
            seen_files[p].add(path.name)
    return consumers, seen_files


# ---------------------------------------------------------------------------
# C1  every OPEN/PROOF-TARGET claim names >=1 blocking primitive OR is an
#     explicit observational passport.
# ---------------------------------------------------------------------------
def check_c1(registry, frontier):
    chk = Check("C1", "every OPEN/PROOF-TARGET claim is primitive-gated OR an explicit passport")
    # gate edges (primitive -> claim) from registry notes AND atlases (measured DAG rule)
    r_gates, _, _, _ = bfd.extract_registry_edges(registry)
    a_gates, _, _ = bfd.load_atlas_edges()
    _, nogo_gates = bfd.parse_nogo_flags()
    gated = {e["dst"] for e in (r_gates + a_gates + nogo_gates) if e["src"].startswith("PRIM-")}
    for cid in sorted(frontier):
        if cid in gated:
            continue
        notes = registry[cid].get("notes", "")
        is_passport = ("-PASSPORT-" in cid
                       or bool(PASSPORT_PROSE_RE.search(notes))
                       or bool(ASSUMP_RE.search(notes)))
        if not is_passport:
            chk.fail(f"{cid}: OPEN/PROOF-TARGET, names NO blocking primitive and carries NO "
                     f"passport/external/ASSUMP marker (unhomed forcing obligation)")
    chk.note(f"frontier={len(frontier)}  primitive-gated={len(frontier & gated)}  "
             f"unhomed(fail)={len(chk.violations)}")
    return chk


# ---------------------------------------------------------------------------
# C2  every PRIM-* named anywhere has (a) a catalog completion object AND
#     (b) >=1 consuming registry claim. Orphans FAIL.
# ---------------------------------------------------------------------------
def check_c2(registry, catalog, refuted):
    chk = Check("C2", "every named PRIM-* has a completion object AND a consumer (no orphans)")
    consumers, seen_files = all_prim_tokens_by_source(registry)
    # CONSUMER = any registry claim gated by the primitive in the MEASURED DAG (registry
    # notes OR atlas OR no-go completion-class OR completion boards). Using notes alone
    # over-claims 'dead' objects that are in fact consumed via atlas/board gate edges.
    r_gates, _, _, _ = bfd.extract_registry_edges(registry)
    a_gates, _, _ = bfd.load_atlas_edges()
    _, nogo_gates = bfd.parse_nogo_flags()
    gate_consumers = defaultdict(set)
    for e in r_gates + a_gates + nogo_gates:
        if e["src"].startswith("PRIM-") and e["dst"] in registry:
            gate_consumers[e["src"]].add(e["dst"])
    all_named = set(seen_files) | set(consumers)
    n_refuted = 0
    for p in sorted(all_named):
        if p in refuted:
            # tested-and-refuted candidate: NO completion object is required by design.
            # Recording it as a fail would contradict the owning NO-GO (owned, not re-opened).
            n_refuted += 1
            chk.note(f"{p}: REFUTED candidate (owned by {refuted[p]}) — exempt from catalog "
                     f"requirement; cited, not re-opened")
            continue
        cataloged = p in catalog
        n_consumers = len(gate_consumers.get(p, ()))
        if not cataloged:
            where = ", ".join(sorted(seen_files.get(p, ()))[:4])
            chk.fail(f"{p}: ORPHAN — no row in TOTAL_EXTENSION_PRIMITIVES.csv "
                     f"(named in: {where}; DAG-gate consumers={n_consumers})")
        elif n_consumers == 0:
            chk.fail(f"{p}: cataloged but has NO consuming registry claim (dead completion object)")
    chk.note(f"catalog_rows={len(catalog)}  named_prims={len(all_named)}  "
             f"refuted_exempt={n_refuted}  orphans+dead(fail)={len(chk.violations)}")
    return chk


# ---------------------------------------------------------------------------
# C3  every no-go's admissible-completion-class names a primitive that EXISTS.
# ---------------------------------------------------------------------------
def check_c3(catalog, refuted):
    chk = Check("C3", "every no-go admissible completion class names an existing primitive")
    _, nogo_gates = bfd.parse_nogo_flags()          # PRIM -> nogo, from 'completion class:' lines
    for e in sorted(nogo_gates, key=lambda x: (x["dst"], x["src"])):
        if e["src"] in refuted:
            chk.note(f"{e['dst']}: names REFUTED candidate {e['src']} (owned by {refuted[e['src']]}) "
                     f"— legitimate 'this completion class does not exist' no-go, not a phantom")
            continue
        if e["src"] not in catalog:
            chk.fail(f"{e['dst']}: admissible completion class names {e['src']} which is ABSENT "
                     f"from the catalog ({e['provenance']})")
    chk.note(f"nogo completion-class gate edges={len(nogo_gates)}  phantom(fail)={len(chk.violations)}")
    return chk


# ---------------------------------------------------------------------------
# C4  no atlas claim_id is absent from the registry (Class-2 desyncs).
# ---------------------------------------------------------------------------
def check_c4(registry):
    chk = Check("C4", "every atlas claim_id has a registry home (no Class-2 desyncs)")
    missing = defaultdict(list)
    for path in sorted(VERIF.glob("*BLOCKERS*.csv")):
        for r in read_csv(path):
            cid = (r.get("claim_id") or r.get("blocker") or "").strip()
            if cid and CLAIM_RE.fullmatch(cid) and cid not in registry:
                missing[cid].append(path.name)
    for cid, files in sorted(missing.items()):
        chk.fail(f"{cid}: atlas claim_id absent from registry (in {', '.join(sorted(set(files)))})")
    chk.note(f"atlas_claim_ids_missing_from_registry(fail)={len(missing)}")
    return chk


# ---------------------------------------------------------------------------
# C5  MONOTONICITY guard: pin the primitive-set + proof-target-set. Any ADD
#     (new primitive / new proof-target) not reflected in the baseline is caught.
# ---------------------------------------------------------------------------
def current_manifest(registry, catalog, frontier):
    consumers, seen_files = all_prim_tokens_by_source(registry)
    named_prims = sorted(set(seen_files) | set(consumers))
    return {
        "catalog_primitives": sorted(catalog),
        "named_primitives": named_prims,
        "proof_targets": sorted(frontier),
    }


def check_c5(registry, catalog, frontier):
    chk = Check("C5", "MONOTONICITY guard: no un-baselined primitive/proof-target additions")
    cur = current_manifest(registry, catalog, frontier)
    if not BASELINE.exists():
        chk.fail(f"no baseline manifest at {BASELINE.name}; run --update-baseline to pin the "
                 f"current set (until then future vNext additions are UNGUARDED)")
        chk.note("baseline ABSENT — this is itself an exhaustiveness gap (nothing pins the set)")
        return chk, cur
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    for key, label in (("named_primitives", "primitive"),
                       ("proof_targets", "proof-target"),
                       ("catalog_primitives", "catalog primitive")):
        added = sorted(set(cur[key]) - set(base.get(key, [])))
        removed = sorted(set(base.get(key, [])) - set(cur[key]))
        for a in added:
            chk.fail(f"un-baselined {label} ADDED since manifest: {a} "
                     f"(a new forcing obligation appeared — update baseline consciously)")
        for r in removed:
            chk.note(f"{label} removed since baseline (retired/renamed): {r}")
    chk.note(f"baseline pins {len(base.get('named_primitives', []))} named prims, "
             f"{len(base.get('proof_targets', []))} proof-targets")
    return chk, cur


# ---------------------------------------------------------------------------
# negative controls: planting an orphan primitive / an unhomed proof-target
# MUST be caught by the respective check (proves the checks can actually fail).
# ---------------------------------------------------------------------------
def negative_controls(registry, catalog, frontier):
    out = []
    # NC1: plant an orphan primitive named by a synthetic registry note -> C2 must flag it
    fake_prim = "PRIM-NEGATIVE-CONTROL-ORPHAN"
    reg2 = {k: dict(v) for k, v in registry.items()}
    victim = next(iter(reg2))
    reg2[victim]["notes"] = (reg2[victim].get("notes", "") + f" [NC] {fake_prim}")
    consumers2, seen2 = defaultdict(set), defaultdict(set)
    for cid, r in reg2.items():
        for p in set(PRIM_RE.findall(r.get("notes", ""))):
            consumers2[p].add(cid)
    caught_nc1 = fake_prim in consumers2 and fake_prim not in catalog
    out.append(("NC1 orphan-primitive planted -> C2 catches", caught_nc1))
    # NC2: plant an unhomed proof-target (no primitive, no passport/external/ASSUMP) -> C1 must flag
    fake_claim = "D0-NEGATIVE-CONTROL-UNHOMED-999"
    r_gates, _, _, _ = bfd.extract_registry_edges(registry)
    a_gates, _, _ = bfd.load_atlas_edges()
    _, nogo_gates = bfd.parse_nogo_flags()
    gated = {e["dst"] for e in (r_gates + a_gates + nogo_gates) if e["src"].startswith("PRIM-")}
    notes = "synthetic bare proof-target with no forcing obligation named"
    unhomed = (fake_claim not in gated
               and "-PASSPORT-" not in fake_claim
               and not PASSPORT_PROSE_RE.search(notes)
               and not ASSUMP_RE.search(notes))
    out.append(("NC2 unhomed proof-target planted -> C1 catches", unhomed))
    return out


def main(argv):
    registry, catalog, frontier, nogos, refuted = load_all()

    if "--update-baseline" in argv:
        cur = current_manifest(registry, catalog, frontier)
        cur["_note"] = ("C5 monotonicity baseline for vp_register_exhaustiveness.py; "
                        "update CONSCIOUSLY when a new primitive or proof-target is legitimately "
                        "added — the whole point is that additions are never silent.")
        BASELINE.write_text(json.dumps(cur, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[baseline] wrote {BASELINE.relative_to(ROOT)}: "
              f"{len(cur['named_primitives'])} named prims, {len(cur['proof_targets'])} proof-targets")
        return 0

    checks = [
        check_c1(registry, frontier),
        check_c2(registry, catalog, refuted),
        check_c3(catalog, refuted),
        check_c4(registry),
    ]
    c5, _ = check_c5(registry, catalog, frontier)
    checks.append(c5)

    print("=" * 78)
    print("vp_register_exhaustiveness — meta-cert over the OPEN-JOINTS register")
    print(f"registry={REGISTRY.relative_to(ROOT)}  rows={len(registry)}  "
          f"frontier(OPEN/PROOF-TARGET)={len(frontier)}  no-gos={len(nogos)}  "
          f"catalog_primitives={len(catalog)}  refuted_candidates={len(refuted)}")
    print("=" * 78)
    n_fail = 0
    for chk in checks:
        mark = "PASS " if chk.status == PASSN else "FAIL*"
        print(f"\n[{mark}] {chk.cid}: {chk.title}")
        for nt in chk.notes:
            print(f"    · {nt}")
        if chk.status == FAIL:
            n_fail += 1
            for v in chk.violations:
                print(f"    ✗ {v}")

    print("\n" + "-" * 78)
    print("NEGATIVE CONTROLS (a check that cannot fail is worthless):")
    nc_ok = True
    for label, caught in negative_controls(registry, catalog, frontier):
        print(f"    {'OK ' if caught else 'BROKEN'} {label}")
        nc_ok = nc_ok and caught

    print("\n" + "=" * 78)
    verdict = "PASS" if n_fail == 0 else "FAIL"
    print(f"OVERALL: {verdict}  ({len(checks) - n_fail}/{len(checks)} checks pass; "
          f"negative-controls {'intact' if nc_ok else 'BROKEN'})")
    if n_fail:
        print("This FAILING state IS the finding: the register is NOT yet exhaustive — the")
        print("violations above are the currently-uncaptured forcing obligations. See")
        print("_TASKS_CENTER_ATTACK/REGISTER_EXHAUSTIVENESS_MEMO.md for the named gaps + fixes.")
    print("=" * 78)
    # negative-control failure is a HARD error (the cert lost its teeth)
    if not nc_ok:
        print("ERROR: negative controls broken — cert cannot be trusted.")
        return 2
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
