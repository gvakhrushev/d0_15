#!/usr/bin/env python3
"""vp_total_extension_primitive_minimality - N-parametric (2026-08-09 rework).

The catalog TOTAL_EXTENSION_PRIMITIVES.csv is, since motion A(d) of the CEMENT
campaign (APPLIED_MOTIONS_LOG.md, O2 policy), the SOLE canonical primitive
catalog: it contains every registry-consumed PRIM-* name, including registered
BUNDLES.  The minimality/independence claim therefore has two layers:
  (1) CATALOG layer: every row fully typed, signatures pairwise distinct;
  (2) INDEPENDENCE layer: the derive-relation on the catalog is EXACTLY the
      registered edge ledger (TOTAL_EXTENSION_PRIMITIVE_DERIVE_EDGES.csv, each
      edge owned by an existing registry claim), and the catalog minus the
      registered exclusions is a pairwise-INDEPENDENT core.
A non-independent pair outside the ledger, an ill-typed row, or a ledger edge
without a registry owner FAILS this cert.  Nothing is silently weakened: the
exceptions are themselves registered, owned results (conjunction / NOGO-split /
GRADAXIS component), not tolerances.

Lean split (hybrid owner, as in D0-EDGE-COVER-FAMILY-001): the Lean theorem
total_extension_primitive_independence owns the ORIGINAL 11-row pairwise
independence (Nodup by decide, empty derive-relation); the full-catalog
adjudication (N rows, 9-edge derive-relation, 17-row core) is cert-borne.
"""
import csv, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]

REQ = ["primitive_id", "mathematical_type", "minimal_input", "why_core_cannot_derive",
       "admissible_completion_class", "necessary_conditions", "sufficient_conditions",
       "counterexample_witness", "negative_controls"]
CELLS = {"independent", "subsumes", "component-of"}
# scope of the Lean theorem: these rows, in this order (order is load-bearing for primSig)
LEAN_11 = ["PRIM-SCENE-HISTORY-REFINEMENT-RULE", "PRIM-COMPARISON-MAP-XI-N", "PRIM-DIRAC-SCALE-SELECTION",
           "PRIM-PHYSICAL-MAGNITUDE-MAP", "PRIM-PHYSICAL-REDSHIFT-OBSERVABLE", "PRIM-FORCED-SMOOTHING-WINDOW",
           "PRIM-LEPTON-BRANCH-FIXING-OPERATOR", "PRIM-PERRON-PHI3-CARRIER", "PRIM-NONCOMMUTING-TRIPLE",
           "PRIM-FINITE-SPECTRAL-TRIPLE-REP", "PRIM-BARYON-PHYSICAL-LABEL-TRANSFER"]


def load():
    P = list(csv.DictReader((ROOT / "04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVES.csv").open(encoding="utf-8", newline="")))
    M = list(csv.reader((ROOT / "04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVE_INDEPENDENCE_MATRIX.csv").open(encoding="utf-8", newline="")))
    raw = list(csv.reader((ROOT / "04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVE_DERIVE_EDGES.csv").open(encoding="utf-8", newline="")))
    edges, excluded, section = [], {}, "edges"
    for r in raw[1:]:
        if not r or not any(c.strip() for c in r):
            continue
        if r[0].startswith("# core_excluded"):
            section = "excluded"; continue
        if section == "edges":
            edges.append({"src": r[0], "dst": r[1], "relation": r[2], "owners": r[3], "just": r[4]})
        else:
            excluded[r[0]] = r[1]
    pairs = list(csv.DictReader((ROOT / "04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVE_PAIR_JUSTIFICATIONS.csv").open(encoding="utf-8", newline="")))
    regs = list(csv.reader((ROOT / "09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    claim_ids = {r[0] for r in regs[1:] if r}
    return P, M, edges, excluded, pairs, claim_ids


def check(P, M, edges, excluded, pairs, claim_ids):
    """All structural checks; raises AssertionError on any violation."""
    ids = [p["primitive_id"] for p in P]
    N = len(ids)
    assert ids[:11] == LEAN_11, "first 11 catalog rows must match the Lean primSig list IN ORDER"
    bad = [p["primitive_id"] for p in P if any(not (p.get(k) or "").strip() for k in REQ)]
    assert not bad, f"primitive missing required field: {bad}"
    assert len(set(ids)) == N, "duplicate primitive_id"
    sigs = [(p["primitive_id"], p["mathematical_type"], p["minimal_input"]) for p in P]
    assert len(set(sigs)) == N, "signature collision (Nodup fails)"
    # matrix alignment
    assert M[0][1:] == ids, "matrix columns != catalog order"
    body = M[1:]
    assert len(body) == N and all(len(r) == N + 1 for r in body), f"matrix not {N}x{N}"
    assert [r[0] for r in body] == ids, "matrix rows != catalog order"
    idx = {p: i for i, p in enumerate(ids)}
    for i in range(N):
        assert body[i][i + 1] == "self", f"diagonal not self at {ids[i]}"
        for j in range(N):
            if i != j:
                assert body[i][j + 1] in CELLS, f"illegal cell {body[i][j+1]} at ({ids[i]},{ids[j]})"
    # matrix <-> ledger exact match
    mat_sub = {(ids[i], ids[j]) for i in range(N) for j in range(N) if i != j and body[i][j + 1] == "subsumes"}
    mat_cmp = {(ids[i], ids[j]) for i in range(N) for j in range(N) if i != j and body[i][j + 1] == "component-of"}
    led = {(e["src"], e["dst"]) for e in edges}
    assert all(e["relation"] == "subsumes" for e in edges), "ledger relation must be 'subsumes'"
    assert led == mat_sub, f"ledger != matrix subsumes cells: {led ^ mat_sub}"
    assert {(b, a) for a, b in led} == mat_cmp, "component-of cells not the exact converses"
    assert all(a in idx and b in idx for a, b in led), "ledger references unknown primitive"
    # every edge owner exists in the canonical registry
    for e in edges:
        owners = [o.strip() for o in e["owners"].replace("+", ",").split(",") if o.strip().startswith("D0-")]
        assert owners, f"edge {e['src']}->{e['dst']} cites no D0 owner claim"
        missing = [o for o in owners if o not in claim_ids]
        assert not missing, f"edge {e['src']}->{e['dst']} cites unregistered owner(s): {missing}"
    # derive-relation transitively closed (a subsuming bundle subsumes its components' components)
    for a, b in led:
        for c, d in led:
            if b == c:
                assert (a, d) in led, f"missing transitive edge {a}->{d}"
    # core: catalog minus registered exclusions is pairwise independent
    assert set(excluded) <= set(ids), "excluded row not in catalog"
    core = [p for p in ids if p not in excluded]
    for a, b in led:
        assert not (a in core and b in core), f"derive-edge inside the core: {a}->{b}"
    touched = {x for e in led for x in e}
    for p, reason in excluded.items():
        assert p in touched, f"excluded row {p} incident to no registered edge (exclusion unjustified)"
        owners = [t.strip("().,;") for t in reason.split() if t.startswith("D0-")]
        assert owners and all(o in claim_ids for o in owners), \
            f"exclusion of {p} cites no existing registry owner: {owners}"
    # pair-justifications file: every unordered pair, exactly once, verdict consistent with the matrix
    assert len(pairs) == N * (N - 1) // 2, f"pair file has {len(pairs)} rows, expected {N*(N-1)//2}"
    seen = set()
    for row in pairs:
        a, b = row["a"], row["b"]
        assert a in idx and b in idx and a != b, f"bad pair ({a},{b})"
        key = frozenset({a, b})
        assert key not in seen, f"duplicate pair ({a},{b})"
        seen.add(key)
        if (a, b) in led or (b, a) in led:
            s, d = (a, b) if (a, b) in led else (b, a)
            assert row["verdict"] == f"derive-edge {s}->{d}", f"pair ({a},{b}) verdict inconsistent with ledger"
        else:
            assert row["verdict"] == "independent", f"pair ({a},{b}) verdict inconsistent with matrix"
        assert len((row["justification"] or "").strip()) >= 40, f"pair ({a},{b}) justification missing/placeholder"
    return ids, core, led


def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: each primitive must be fully typed, and every non-independent pair must be a registered, owned result, before any count.")
    P, M, edges, excluded, pairs, claim_ids = load()
    ids, core, led = check(P, M, edges, excluded, pairs, claim_ids)
    N = len(ids)
    print(f"PASS_PRIMITIVES  {N} catalog rows, each with type/input/why/class/necessary/sufficient/counterexample/controls; signatures Nodup.")
    n_ind = N * (N - 1) - 2 * len(led)
    print(f"PASS_INDEPENDENCE  {N}x{N} matrix; {n_ind} off-diagonal cells independent; {len(led)} derive-edges, ALL registered in the ledger with existing registry owners (no unregistered merge/derivation).")
    print(f"PASS_CORE  {len(core)}-row pairwise-independent core = catalog minus registered bundles/components: {sorted(excluded)}.")
    print(f"PASS_PAIRS  all {len(pairs)} unordered pairs individually justified, verdicts consistent with matrix+ledger.")
    print(f"PASS_LEAN_SCOPE  Lean theorem owns the original 11-row independence; rows 1..11 verified IN ORDER against the primSig list; full-catalog layer cert-borne.")

    # NEGATIVE CONTROLS - planted mutations must FAIL the check (a check that
    # cannot fail is worthless; each mutation attacks the CONCLUSION).
    import copy
    def must_fail(mutate, label):
        p2, m2, e2, x2, q2 = copy.deepcopy(P), copy.deepcopy(M), copy.deepcopy(edges), dict(excluded), copy.deepcopy(pairs)
        mutate(p2, m2, e2, x2, q2)
        try:
            check(p2, m2, e2, x2, q2, claim_ids)
        except AssertionError:
            print(f"PASS_NC  {label} -> caught"); return
        raise SystemExit(f"NEGATIVE CONTROL FAILED: {label} was NOT caught")
    must_fail(lambda p, m, e, x, q: p[0].update(counterexample_witness=""), "blanked required field")
    def flip(p, m, e, x, q):
        i, j = [r[0] for r in m[1:]].index(e[0]["src"]) , m[0][1:].index(e[0]["dst"])
        m[1 + i][1 + j] = "independent"
    must_fail(flip, "derive-edge hidden as 'independent' (silent weakening)")
    must_fail(lambda p, m, e, x, q: e.pop(0), "ledger edge dropped while matrix keeps it")
    def core_edge(p, m, e, x, q):
        x.pop("PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR")
    must_fail(core_edge, "subsumed component smuggled into the core")
    must_fail(lambda p, m, e, x, q: q.pop(), "pair-justification row dropped (unverified conjunct 4)")
    def relabel_pair(p, m, e, x, q):
        tgt = next(r for r in q if r["verdict"].startswith("derive-edge"))
        tgt["verdict"] = "independent"
    must_fail(relabel_pair, "derive-edge pair relabeled independent in the pairs file")
    def reorder(p, m, e, x, q):
        p[3], p[4] = p[4], p[3]
    must_fail(reorder, "Lean-owned first-11 order broken (rows 4/5 swapped)")

    print("PASS_TOTAL_EXTENSION_PRIMITIVE_MINIMALITY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
