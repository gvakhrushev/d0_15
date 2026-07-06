#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
close_gap_e_meta_check.py — GAP-E 9th (FINAL) pass: the META route. POST-SKEPTIC STATE.

AUTHOR CLAIM (v1, KILLED by independent skeptic §05.8.R, 2026-07-06 — accepted in full):
  "GAP-E's completeness quantifier is an ordinary DEF-0.2.2 instantiation; the grammar
  bans any underived outcome-affecting addition, so AdmExt = {D2, ABCD} is forced."

THE KILL (encoded below, machine-checked):
  K1  The identification "underived presence of a step = a 'choice rule' (B00:455)" is
      AUTHORED, not verbatim: B00:455 lists 'a choice rule' as a form of required-but-
      underivable STRUCTURE a construction must CARRY; it nowhere identifies the mere
      underived PRESENCE of an alternative with one.
  K2  PARITY INVERTED: each precedent (B01:1539 bit-stop; B03:928-933 D_anchor;
      row 257 4th-zone) closes via ITS OWN owned banning sentence naming the theta
      (orientation catalog / significance catalog / copy-index + Lean p^3-exhaustion).
      X3 / size-6 have NO such sentence (GREP sweep). The profiles are NOT identical
      once the 5th bit (owned_banning_sentence) is COMPUTED rather than hardcoded, and
      denying the author's grammar clause reopens NOTHING (collateral = 0, not 3).
  K3  Step (ii) as used was absence-from-current-text, not underivability-in-principle
      (the author's own hook H-a concedes a new owned sentence could derive a rival).
  K4  The Lean route is circular for this purpose: m1_alternative_needs_catalogue takes
      the uniqueness (M1Forced) as HYPOTHESIS — it cannot supply the completeness.
  K5  Omitted adverse continuations: B00:171/376/396/494 — the firewall's force is
      NON-PROMOTION (HYP, never THE), not negation of admissibility.

WHAT SURVIVES (the honest content, still checked):
  QV     all verbatim quotes incl. the FULL adverse set (A1-A6).
  GREP   no owned sentence produces OR bans a rival step (whitelist-guarded, can-fail:
         a new hit of either kind requires re-adjudication of the ledger).
  TAXON  the precedent taxonomy: every owned stop-claim carries an owned banning
         sentence or an owned algebraic exhaustion; GAP-E's rivals carry neither.
  PIN    MUT-A: GRANTING the closed-world clause (or a banning sentence, or an
         exhaustion) would close GAP-E — the residue is exactly ONE owned-text unit.
  HONEST MUT-B: granting a rival a producing sentence makes completeness FALSE
         (the check can fail on the conclusion, trap f).

rc=2  OPEN / HONEST-FAIL (the expected, final state)   rc=1 broken support   rc=0 unreachable here
NO registry row edited; NO .lean touched; 053040 untouched. STOP-RULE ACTIVE (memo §8).
"""
import re, sys, os, copy

REPO = os.environ.get("D0_REPO", os.path.expanduser("~/Downloads/d0_15"))
B00 = os.path.join(REPO, "01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md")
B01 = os.path.join(REPO, "01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md")
B03 = os.path.join(REPO, "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md")
TSM = os.path.join(REPO, "03_THEORY_MAP/theory_status_map.csv")
M1P = os.path.join(REPO, "09_LEAN_FORMALIZATION/D0/Foundation/M1Predicate.lean")

FAILURES, NOTES = [], []
def load(path):
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()
FILES = {p: load(p) for p in (B00, B01, B03, TSM, M1P)}

# ---------------------------------------------------------------- QV layer
QUOTES = [
    (B00, 162, 2, ['strikes not at candidates but at **any** alternative at once',
                   'requires a catalog'], "Q1-any-alternative", "SUPPORT"),
    (B00, 386, 4, ['not derivable from previously introduced DEF/LEM/THE'], "Q2-schema-ii", "SUPPORT"),
    (B00, 388, 4, ['theta affects distinguishable outcomes', 'exogenous'], "Q2-schema-iii", "SUPPORT"),
    (B00, 390, 4, ['violates M1'], "Q2-schema-iv", "SUPPORT"),
    (B00, 394, 2, ['Every forced claim in the corpus', 'the K(9,11,13) scene',
                   'instantiates this schema with a different'], "Q3-schema-universal", "SUPPORT"),
    (B00, 398, 2, ['required-but-not-distinguishing addition is, by LEM 0.4.1a',
                   'hidden external catalog and falls to M1'], "Q4-lem041a-Bhorn", "SUPPORT"),
    (B00, 455, 2, ['required-but-underivable structure', 'a choice rule'], "Q5-exo-def", "SUPPORT"),
    (B00, 461, 2, ['let an independent executor reproduce the result from the published corpus'],
                   "Q6-mandatory-test", "SUPPORT"),
    (B00, 463, 2, ['ban on a mandatory external catalogue'], "Q7-M1-ban", "SUPPORT"),
    (B00, 477, 2, ['changes** the class of distinguishable outcomes',
                   '*must* be derived/justified inside the corpus'], "Q8-blade-A", "SUPPORT"),
    (B00, 484, 2, ['M1 is what terminates the recursion'], "Q10-recursion-stop", "SUPPORT"),
    (B00, 486, 2, ['forbid every add-on that needs external specification',
                   'take the only-possible'], "Q11-closed-world-addons", "SUPPORT"),
    # owned banning sentences of the PRECEDENTS (each names its own theta):
    (B01, 1530, 2, ['That is the catalog M1 forbids'], "BAN-fewer-roles", "BANNING"),
    (B01, 1539, 2, ['no further bit can be added without an exogenous orientation catalog'],
                   "BAN-bit (P-BIT)", "BANNING"),
    (B03, 928, 8, ['empty address slots', 'exogenous significance catalog'], "BAN-danchor (P-ROLE)", "BANNING"),
    (B03, 933, 8, ['unique survivor'], "BAN-danchor-unique", "BANNING"),
    (TSM, 257, 1, ['no admissible structure registers a 4th zone', 'DEF-0.2.2'], "BAN-zone4 (P-ZONE4)", "BANNING"),
    (TSM, 257, 1, ['assembled not re-derived'], "BAN-zone4-honesty", "BANNING"),
    # inventory + tower text
    (B01, 1548, 2, ['the only primitive unresolved capacities'], "Q15-only-capacities", "SUPPORT"),
    (B01, 1556, 2, ['cannot be replaced by', 'without losing one terminal role'], "Q16-v12-exclusion", "SUPPORT"),
    (B01, 325, 3, ['External Catalog of differences'], "Q18-the0140", "SUPPORT"),
    # formal keystone — K4: CONDITIONAL, uniqueness is a hypothesis, cannot supply completeness
    (M1P, 61, 6, ['m1_alternative_needs_catalogue'], "Q19-lean-keystone(K4-conditional)", "SUPPORT"),
    (M1P, 47, 4, ['always stated *against an `M1Forced` hypothesis'], "Q19-lean-honesty-guard", "SUPPORT"),
    (TSM, 277, 1, ['a proof may not depend on an unprovable postulate'], "Q19-row277", "SUPPORT"),
    # ---- FULL ADVERSE SET (A1-A3 pre-registered; A4-A6 skeptic-added, K5) ----
    (B00, 378, 2, ['at most a HYP, never a THE'], "A1-hyp-escape", "ADVERSE"),
    (B00, 466, 2, ['same class of distinguishable outcomes'], "A2-same-class-face", "ADVERSE"),
    (B00, 488, 2, ['one and the same distinguishable object'], "A3-m1plus-scope", "ADVERSE"),
    (B00, 376, 2, ['Proof by "obviousness" is forbidden'], "A4-protocol-law", "ADVERSE"),
    (B00, 396, 2, ['the content lives entirely in the axiom M1 and in the finite objects'],
                   "A5-standard-language", "ADVERSE"),
    (B00, 171, 2, ['If a forcing exists, it is a THE-candidate'], "A6-nonpromotion-force", "ADVERSE"),
]
def check_quote(path, anchor, tol, subs, lines=None):
    lines = lines if lines is not None else FILES[path]
    lo, hi = max(0, anchor - 1 - tol), min(len(lines), anchor - 1 + tol + 1)
    window = "\n".join(lines[lo:hi])
    return [s for s in subs if s not in window]

QV_OK = {}
for path, anchor, tol, subs, tag, role in QUOTES:
    missing = check_quote(path, anchor, tol, subs)
    QV_OK[tag] = not missing
    if missing:
        FAILURES.append("QV[%s/%s] %s:%d missing %r" % (role, tag, os.path.basename(path), anchor, missing))
    else:
        NOTES.append("QV ok  %-34s %s:%d" % (tag, os.path.basename(path), anchor))

# ------------------------------------------------------- GREP can-fail sweep
# TWO purposes: (a) no owned sentence PRODUCES a rival step; (b) no owned sentence
# BANS one either (that missing ban IS the residue). A new hit of either kind
# => rc=1, ledger must be re-adjudicated.
GREP_PATTERNS = [r"V_\{12\}", r"V_\{15\}", r"\bV12\b", r"\bV15\b", r"Aut-orbit", r"orbit partition"]
WHITELIST = {(os.path.basename(B01), 1556), (os.path.basename(B01), 1560)}
rival_hits = 0
for path in (B01, B03):
    base = os.path.basename(path)
    for i, line in enumerate(FILES[path], 1):
        for pat in GREP_PATTERNS:
            if re.search(pat, line) and (base, i) not in WHITELIST \
               and not re.search(r"V=12|E=30|V12,E30", line):
                rival_hits += 1
                FAILURES.append("GREP unadjudicated hit %s:%d pat=%s :: %s" % (base, i, pat, line.strip()[:100]))
NOTES.append("GREP: no owned sentence produces OR bans a rival step (whitelist B01:1556, B01:1560)")

# ------------------------------------------------- profiles (K2 repair)
# owned_banning_sentence is COMPUTED from QV/GREP, never hardcoded.
Z_OWNED = (9, 11, 13)
CANDIDATES = {
    "D2":    dict(presence_derived=True,  z=Z_OWNED, ban_tag=None,
                  src="B01:1539 sign-bit + B01:1548 inventory"),
    "ABCD":  dict(presence_derived=True,  z=Z_OWNED, ban_tag=None,
                  src="B03:910-933 D_anchor=4 + B01:1548"),
    # EoR 2026-07-06 (10th pass, GAPE-1011 integration): X3 IS covered by the owned
    # orientation-parity ban (odd step) — B01:1903 / B03 §03.23.6(3) / row 522
    # (SceneStepParity). Corrects the pass-5..9 "NONE" record. NOTE: this ban_tag is
    # NOT in the QUOTES QV set, so banned_by_owned_text() still returns False here and
    # the honest verdict is UNCHANGED (rc=2) — the tag records the owned-parity ban as a
    # provenance annotation; wiring it into QV would be a verdict change (owner-gated,
    # NOT done). See CLOSE_GAP_E_OWNER_MEMO.md §8.2.
    "X3":    dict(presence_derived=False, z=(9, 11, 12), ban_tag="B01:1903/B03:03.23.6(3)",
                  src="OWNED PARITY BAN (B01:1903/B03 03.23.6(3)/row 522 SceneStepParity); EoR 10th pass"),
    "SIZE6": dict(presence_derived=False, z=(9, 11, 15), ban_tag=None,
                  src="NONE (DYAD-POWER: silence)"),
    "ZONE4": dict(presence_derived=False, z=(9, 11, 13, 8), ban_tag="BAN-zone4 (P-ZONE4)",
                  src="row 257 owned no-go (cross-ref)"),
}
PRECEDENTS = {
    "P-BIT   (B01:1539)":   dict(ban_tag="BAN-bit (P-BIT)",
                                 mechanism="owned banning sentence naming theta (orientation catalog)"),
    "P-ROLE  (B03:928-933)": dict(ban_tag="BAN-danchor (P-ROLE)",
                                 mechanism="owned banning sentence naming theta (significance catalog)"),
    "P-ZONE4 (row 257)":    dict(ban_tag="BAN-zone4 (P-ZONE4)",
                                 mechanism="owned Lean exhaustion (p^3 reduces) + copy-index catalog"),
}
def banned_by_owned_text(entry):
    tag = entry.get("ban_tag")
    if tag is None:
        return False                        # computed: GREP found no banning sentence
    return bool(QV_OK.get(tag, False))      # computed: the banning sentence verified on disk

for name in ("X3", "SIZE6"):
    if banned_by_owned_text(CANDIDATES[name]):
        FAILURES.append("PROF %s unexpectedly has an owned banning sentence — re-adjudicate" % name)
    else:
        NOTES.append("PROF %-5s: outcome-affecting (z=%s != %s), presence underived, "
                     "NO owned banning sentence" % (name, CANDIDATES[name]["z"], Z_OWNED))
if not banned_by_owned_text(CANDIDATES["ZONE4"]):
    FAILURES.append("PROF ZONE4: row 257 banning text not verified")
else:
    NOTES.append("PROF ZONE4: banned by OWNED text (row 257) — exactly the grade GAP-E's rivals lack")

# ------------------------------------------------- TAXONOMY (K2, the inverted parity)
for pname, p in PRECEDENTS.items():
    if not banned_by_owned_text(p):
        FAILURES.append("TAXON %s: its banning sentence failed QV" % pname)
    else:
        NOTES.append("TAXON %-22s closes via %s" % (pname, p["mechanism"]))
# Decisive computed fact: the precedents' closures do NOT rest on the author's
# grammar clause — each has its own owned text. Collateral of denying it = 0.
collateral = sum(1 for p in PRECEDENTS.values() if not banned_by_owned_text(p))
if collateral != 0:
    FAILURES.append("TAXON collateral != 0 (got %d) — some precedent would rest on the clause" % collateral)
else:
    NOTES.append("TAXON collateral of denying the author's grammar clause = 0 "
                 "(v1 hardcoded 3 — the parity pin was INVERTED by the skeptic; K2)")

# ------------------------------------------------- the load-bearing bit, post-kill
# Description-level closed-world IS owned (B00:484-486) — but its force is
# NON-PROMOTION (A1/A6: unforced => at most HYP), never NEGATION of admissibility.
# The ban-direction for a specific addition requires an owned banning sentence or an
# owned exhaustion (the precedent taxonomy) — which GAP-E's rivals lack.
GRAMMAR_CLAUSE_OWNED = False   # SKEPTIC-ADJUDICATED (K1, K5). The mutation pivot.

def gap_e_state(clause_owned, cands):
    closed = clause_owned or all(banned_by_owned_text(cands[n]) for n in ("X3", "SIZE6"))
    model = sorted(n for n, c in cands.items() if c["presence_derived"]) if closed else None
    return closed, model

closed, model = gap_e_state(GRAMMAR_CLAUSE_OWNED, CANDIDATES)
if closed:
    FAILURES.append("STATE claims CLOSED without owned text — the smuggle would be back")
else:
    NOTES.append("STATE GAP-E completeness: OPEN (rivals unbanned by owned text; clause unowned)")

# ------------------------------------------------- MUTATIONS
# MUT-A (the pin): GRANT the clause -> closes with model {D2, ABCD}.
cA, mA = gap_e_state(True, CANDIDATES)
if not (cA and mA == ["ABCD", "D2"]):
    FAILURES.append("MUT-A granting the clause fails to close (model=%r)" % mA)
else:
    NOTES.append("MUT-A ok: granting the closed-world/ban clause closes GAP-E, model={D2,ABCD} (the pin)")
# MUT-A': granting owned BANNING sentences instead (the precedent-type route) closes identically.
c2 = copy.deepcopy(CANDIDATES)
c2["X3"]["ban_tag"] = c2["SIZE6"]["ban_tag"] = "BAN-bit (P-BIT)"  # stand-in for new owner-authored text
cA2, mA2 = gap_e_state(False, c2)
if not (cA2 and mA2 == ["ABCD", "D2"]):
    FAILURES.append("MUT-A' owned banning sentences fail to close (model=%r)" % mA2)
else:
    NOTES.append("MUT-A' ok: owner-authored banning sentences (precedent-type) would close identically")
# MUT-B (trap f): grant X3 a PRODUCING sentence -> completeness FALSE.
c3 = copy.deepcopy(CANDIDATES); c3["X3"]["presence_derived"] = True
cB, mB = gap_e_state(True, c3)
if mB == ["ABCD", "D2"]:
    FAILURES.append("MUT-B conclusion cannot fail (trap f)")
else:
    NOTES.append("MUT-B ok: a producing sentence for X3 -> model=%r -> completeness FALSE" % mB)
# MUT-C: tampered quote fires QV.
tampered = list(FILES[B00]); tampered[485] = tampered[485].replace("forbid every add-on", "permit every add-on")
if not check_quote(B00, 486, 2, ['forbid every add-on that needs external specification',
                                 'take the only-possible'], lines=tampered):
    FAILURES.append("MUT-C QV failed to fire on tampered quote")
else:
    NOTES.append("MUT-C ok: QV fires on tampered Q11")

# ------------------------------------------------- verdict
print("=" * 78)
print("close_gap_e_meta_check.py — GAP-E META route, 9th/FINAL pass — POST-SKEPTIC")
print("=" * 78)
for n in NOTES: print("  " + n)
if FAILURES:
    print("-" * 78)
    for f in FAILURES: print("  FAIL " + f)
    print("VERDICT: rc=1 BROKEN SUPPORT")
    sys.exit(1)
print("-" * 78)
print("VERDICT: rc=2 OPEN / HONEST-FAIL (9th independent confirmation — FINAL).")
print("  Residue = ONE owned-text unit, mechanism now ADJUDICATED (memo §8):")
print("  either an owner-authored banning sentence naming the catalog a rival step")
print("  must carry (precedent type B01:1539 / B03:928-933), or an owned algebraic")
print("  exhaustion of the capacity inventory (precedent type row 257 CASE 1).")
print("  STOP-RULE ACTIVE: GAP-E is not to be re-forged without new owned book text.")
sys.exit(2)
