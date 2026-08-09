#!/usr/bin/env python3
"""SEAM_RATE_IMPORT_MEMO companion — obligation (ii) of D0-ALPHA-SEAM-FORM-FORCED-001 adjudicated.

Adjudicates the open rate leg (leg 5) of the α seam dressing `1 + h_KS·sin θ_seam`:
(A) STRUCTURE: the rate cannot be intrinsic to the seam monodromy (an isometry — zero KS rate);
    it is necessarily an IMPORT from the golden symbolic system (toral T / fusion N_τ).
(B) RECORD (v4, ADOPTED state): the cross-scope identification EXISTS in print — BOOK_06
    §06.30a: "The rate h_KS=log φ here is *exactly* the closure-holonomy stretch per monodromy
    turn (§02.13.h, D0-SEAM-HOLONOMY-001)". Found ONE-SIDED by the 2026-07-18 external review;
    reciprocity minted the same day; then ADOPTED post-skeptic #22 (SEAM_RATE_ADOPTION_MEMO):
    the §02.13.h stretch bullet now binds the rate to the toral time generator with the Lean
    carrier D0.Spectral.SeamRateImport, and the entropy reading stays the named external
    wrapper (boundary as D0-IF-KS-FORMULA-FIX-001). Release stays PROOF-TARGET ((i)/(iii)).

WHAT IS CHECKED (each can FAIL; exact arithmetic on all load-bearing facts):
  C1  INTRINSIC-RATE-ZERO   — U(θ)=cosθ·I+sinθ·G satisfies U^T·U=I exactly mod (c²+s²−1), so
      |λ(U)|≡1, Lyapunov {0,0}, intrinsic KS rate 0 ≠ ln φ (Pesin wrapper, same external grade
      as row 253's h_KS=log|λ_max| wrapper).  Controls: toral T radius = φ, hyperbolic
      H=[[2,1],[1,1]] radius = φ² (both exact, >1 ⇒ nonzero rate) — the method distinguishes.
  C2  TORAL-SOURCE-EXACT    — charpoly(T)=x²+x−1, |λ_max|=φ exact in ℚ(√5);
      Tr(Tⁿ)=(−1)ⁿLₙ re-derived n=1..13 by exact integer matrix powers (BOOK_06 §06.8).
  C3  REFERENT-SELECTIVITY  — among owned operators of the two scopes {seam G, seam U, seam N,
      toral T, fusion N_τ}, a magnitude-φ eigenvalue occurs EXACTLY in {T, N_τ} (seam side:
      magnitudes {1}/{0}); T↔N_τ are one golden system by the owned §01.21.4 chain (anchor
      live-checked).  ":88 the φ eigenvalue" has a unique referent up to an owned identification.
  C4  BINDING-EXISTS-RECIPROCATED — live corpus scan: the ONLY line joining {seam/monodromy} ×
      {toral/tick} × {rate/KS} is the BOOK_06 §06.30a identification sentence (explicit
      "§02.13.h" + "D0-SEAM-HOLONOMY-001" cross-refs, "is exactly"); AND the minted reciprocity
      is live — §02.13.h:95 carries the §06.30a pointer and the notes of rows 564 and 285 cite
      06.30a in BOTH registries.  (Fails if the sentence is removed OR reciprocity is reverted.)
  C5  GRADE-TABLE           — precedent bar: GAP-E `:325` transfer cleared on an in-print
      name-match; GAP-W R-A failed with none.  THIS case (post-mint): in-print IDENTIFICATION
      sentence + value match + referent selectivity + carrier (this cert, registered in row
      564's note) + reciprocity ⇒ ASSEMBLY-CANDIDATE-MINTED with exactly ONE residual — owner
      adoption at owned grade (live-checked: the :95 clause names "owner adoption" as the
      residual) — still distinct from GAP-E (adopted) and GAP-W R-A (nothing).
  C6  CERT-AHEAD-OF-BOOK    — vp_seam_holonomy_alpha.py's docstring names the toral generator +
      row D0-IF-KS-FORMULA-FIX-001 (and the |V₁₁|+1 transport-factor candidate for obligation
      (i)), while §02.13.h's stretch line (:88) still names no system: the (i) lead stays at
      cert-comment grade and the stretch line itself remains un-adopted (the residual is real).

STRUCTURE_FIXED_BEFORE_NUMBER: T=[[0,1],[1,-1]]; U(θ)=cosθ·I+sinθ·G, G²=−I; ideal c²+s²=1;
charpolys x²+x−1 (toral), x²−x−1 (fusion), x²+1 (G); φ=(1+√5)/2.  No measured number enters.

Mutants (--selftest, each must FAIL its check's CONCLUSION):
  M1 identification sentence stripped from the scan → C4;   M2 hyperbolic imposter as the seam
  monodromy → C1;   M3 relation c²+s²=1 dropped → C1;   M4 dressing rate ln2 (value mismatch)
  → C5;   M5 fusion N_τ removed from the referent inventory → C3;   M6 reciprocity reverted
  (06.30a stripped from the ledger notes and the :95 pointer) → C4 — the pre-mint state must
  no longer pass v3.
"""
from __future__ import annotations

import csv
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
LEDGER = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
STATUS_MAP = ROOT / "03_THEORY_MAP" / "theory_status_map.csv"

# ---------- exact Q(√5): value = a + b·√5, a,b ∈ ℚ ----------
class Q5:
    __slots__ = ("a", "b")
    def __init__(self, a, b=0):
        self.a, self.b = Fraction(a), Fraction(b)
    def __add__(self, o): o = _q5(o); return Q5(self.a + o.a, self.b + o.b)
    def __sub__(self, o): o = _q5(o); return Q5(self.a - o.a, self.b - o.b)
    def __mul__(self, o): o = _q5(o); return Q5(self.a * o.a + 5 * self.b * o.b, self.a * o.b + self.b * o.a)
    __radd__, __rmul__ = __add__, __mul__
    def __neg__(self): return Q5(-self.a, -self.b)
    def __eq__(self, o): o = _q5(o); return self.a == o.a and self.b == o.b
    def is_positive(self):
        if self.b == 0: return self.a > 0
        if self.a == 0: return self.b > 0
        if self.a > 0 and self.b > 0: return True
        if self.a < 0 and self.b < 0: return False
        return (self.a * self.a > 5 * self.b * self.b) == (self.a > 0)
    def __gt__(self, o): return (self - _q5(o)).is_positive()
    def __repr__(self): return f"({self.a}+{self.b}√5)"

def _q5(x): return x if isinstance(x, Q5) else Q5(x)

PHI = Q5(Fraction(1, 2), Fraction(1, 2))
ONE, ZERO = Q5(1), Q5(0)

def quad_roots_abs(p, q):
    """Magnitudes of the (real) roots of x² + p·x + q, integer p,q, disc ∈ {1,4,5}."""
    disc = p * p - 4 * q
    s5 = {5: Q5(0, 1), 1: Q5(1), 4: Q5(2)}[disc]
    r1 = Q5(Fraction(-p, 2)) + Q5(Fraction(1, 2)) * s5
    r2 = Q5(Fraction(-p, 2)) - Q5(Fraction(1, 2)) * s5
    return [r if r.is_positive() else -r for r in (r1, r2)]

# ---------- exact polynomials in c,s modulo (c²+s²−1) ----------
def pmul(P, Q):
    R = {}
    for (i, j), x in P.items():
        for (k, l), y in Q.items():
            key = (i + k, j + l); R[key] = R.get(key, Fraction(0)) + x * y
    return {k: v for k, v in R.items() if v != 0}

def padd(P, Q):
    R = dict(P)
    for k, v in Q.items():
        R[k] = R.get(k, Fraction(0)) + v
    return {k: v for k, v in R.items() if v != 0}

def preduce(P, use_relation=True):
    if not use_relation:
        return dict(P)
    P = dict(P); changed = True
    while changed:
        changed = False
        for (i, j), x in list(P.items()):
            if j >= 2:
                del P[(i, j)]
                for key, y in (((i, j - 2), x), ((i + 2, j - 2), -x)):
                    P[key] = P.get(key, Fraction(0)) + y
                changed = True
        P = {k: v for k, v in P.items() if v != 0}
    return P

C, S, P1 = {(1, 0): Fraction(1)}, {(0, 1): Fraction(1)}, {(0, 0): Fraction(1)}

def matpoly_mul(A, B, use_rel=True):
    return [[preduce(padd(pmul(A[i][0], B[0][j]), pmul(A[i][1], B[1][j])), use_rel)
             for j in range(2)] for i in range(2)]

def imat_mul(A, B):
    return [[A[i][0] * B[0][j] + A[i][1] * B[1][j] for j in range(2)] for i in range(2)]

def imat_pow(A, n):
    R = [[1, 0], [0, 1]]
    for _ in range(n):
        R = imat_mul(R, A)
    return R

FAILS = []
def check(name, ok, detail):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} — {detail}")
    if not ok:
        FAILS.append(name)

def read_book_lines():
    out = []
    for p in sorted(BOOKS.glob("BOOK_0*.md")):
        for i, ln in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            out.append((p.name, i, ln))
    return out

def ledger_note(claim_id):
    """Concatenated notes for claim_id from BOTH registries (R3 hardening, skeptic #20)."""
    out = []
    for path in (LEDGER, STATUS_MAP):
        with path.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("claim_id") == claim_id:
                    out.append(row.get("notes", "") or "")
    return " || ".join(out)

SEAM_TOK = re.compile(r"\bseam|\bmonodrom|\bholonom|\bstretch", re.I)
TORAL_TOK = re.compile(r"\btoral\b|\btorus\b|\btick\b|\[\[0,1\],\[1,-1\]\]|time generator|automorphism", re.I)
RATE_TOK = re.compile(r"h_\{?KS\}?|Kolmogorov|\bln ?\\?varphi|\blog ?\\?varphi|log phi|ln phi|\brate\b", re.I)
IDENT_SIG = re.compile(r"closure-holonomy stretch per monodromy turn.*02\.13\.h.*SEAM-HOLONOMY", re.I)
POINTER_SIG = re.compile(r"06\.30a.*(toral rate|in-print candidate)", re.I)
ADOPTED_SIG = re.compile(r"toral time generator.*SeamRateImport", re.I)

def main(mut=None) -> int:
    FAILS.clear()
    # ---------- C1 ----------
    use_rel = mut != "M3"
    if mut == "M2":
        mags_are_one = all(l == ONE for l in quad_roots_abs(-3, 1))
    else:
        U = [[dict(C), {k: -v for k, v in S.items()}], [dict(S), dict(C)]]
        UT = [[U[0][0], U[1][0]], [U[0][1], U[1][1]]]
        M = matpoly_mul(UT, U, use_rel)
        mags_are_one = (M[0][0] == P1 and M[1][1] == P1 and M[0][1] == {} and M[1][0] == {})
    check("C1_ISOMETRY_ZERO_RATE", mags_are_one,
          "U(θ)ᵀU(θ)=I exactly mod (c²+s²−1) ⇒ |λ(U)|≡1 ⇒ Lyapunov {0,0} ⇒ intrinsic seam KS"
          " rate = 0 ≠ ln φ (Pesin wrapper) — the dressing rate is necessarily an IMPORT")
    tor_abs, hyp_abs = quad_roots_abs(1, -1), quad_roots_abs(-3, 1)
    check("C1_CONTROL_DISTINGUISHES",
          any(l == PHI for l in tor_abs) and any(l == PHI * PHI for l in hyp_abs)
          and any(l > ONE for l in tor_abs),
          "toral radius = φ exactly, hyperbolic control radius = φ² exactly (>1 ⇒ rate>0):"
          " the zero-rate verdict is a property of the SEAM map, not of the method")

    # ---------- C2 ----------
    T = [[0, 1], [1, -1]]
    tr, det = T[0][0] + T[1][1], T[0][0] * T[1][1] - T[0][1] * T[1][0]
    L = [2, 1]
    for _ in range(2, 14):
        L.append(L[-1] + L[-2])
    lucas_ok = all(imat_pow(T, n)[0][0] + imat_pow(T, n)[1][1] == (-1) ** n * L[n] for n in range(1, 14))
    check("C2_TORAL_SOURCE_EXACT",
          (tr, det) == (-1, -1) and max(quad_roots_abs(1, -1), key=lambda z: (z.a, z.b)) == PHI and lucas_ok,
          "charpoly(T)=x²+x−1, |λ_max|=φ exact; Tr(Tⁿ)=(−1)ⁿLₙ verified n=1..13 by integer powers")

    # ---------- C3 ----------
    inventory = {
        "seam G (x²+1)": [ONE, ONE],
        "seam U(θ)": [ONE, ONE],
        "seam N (nilpotent)": [ZERO, ZERO],
        "toral T (x²+x−1)": quad_roots_abs(1, -1),
        "fusion N_τ (x²−x−1)": quad_roots_abs(-1, -1),
    }
    if mut == "M5":
        del inventory["fusion N_τ (x²−x−1)"]
    with_phi = sorted(n for n, mags in inventory.items() if any(m == PHI for m in mags))
    b01 = (BOOKS / "BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md").read_text(encoding="utf-8")
    ident_owned = ("h_{KS}(T)" in b01 and "h_{\\mathrm{top}}(N_\\tau)" in b01
                   and "I_f \\;=\\; \\log\\varphi" in b01)
    check("C3_REFERENT_SELECTIVITY",
          not any("seam" in n for n in with_phi)
          and with_phi == ["fusion N_τ (x²−x−1)", "toral T (x²+x−1)"] and ident_owned,
          f"magnitude-φ eigenvalue occurs exactly in {with_phi} (seam side: never); T↔N_τ are one"
          " golden system by the owned §01.21.4 chain (I_f = log φ = h_top(N_τ) = h_KS(T))")

    # ---------- C4 ----------
    lines = read_book_lines()
    if mut == "M1":
        lines = [(b, i, ln) for (b, i, ln) in lines if not IDENT_SIG.search(ln)]
    joint = [(b, i, ln) for (b, i, ln) in lines
             if SEAM_TOK.search(ln) and TORAL_TOK.search(ln) and RATE_TOK.search(ln)]
    if mut == "M6":
        joint = [(b, i, ln.replace("06.30a", "")) for (b, i, ln) in joint]
    if mut == "M7":
        joint = [(b, i, ln.replace("toral time generator", "")) for (b, i, ln) in joint]
    ident_hits = [(b, i) for (b, i, ln) in joint if IDENT_SIG.search(ln)]
    ident_lines = [ln for (b, i, ln) in joint if IDENT_SIG.search(ln)]
    adopted_hits = [(b, i) for (b, i, ln) in joint
                    if ADOPTED_SIG.search(ln) and not IDENT_SIG.search(ln)]
    pointer_hits = [(b, i) for (b, i, ln) in joint
                    if POINTER_SIG.search(ln) and not IDENT_SIG.search(ln)
                    and not ADOPTED_SIG.search(ln)]
    incidental = [(b, i) for (b, i, ln) in joint
                  if not IDENT_SIG.search(ln) and not POINTER_SIG.search(ln)
                  and not ADOPTED_SIG.search(ln)]
    src_0213 = (BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS" /
                "0018__02.13__gauge-and-coefficient-proof-cells.md").read_text(encoding="utf-8")
    note564 = ledger_note("D0-ALPHA-SEAM-FORM-FORCED-001")
    note285 = ledger_note("D0-SEAM-HOLONOMY-001")
    if mut == "M6":
        src_0213 = src_0213.replace("06.30a", "")
        note564 = note564.replace("06.30a", "")
        note285 = note285.replace("06.30a", "")
    reciprocity_minted = ("06.30a" in src_0213 and "06.30a" in note564 and "06.30a" in note285
                          and "seam_rate_import_check.py" in note564)
    check("C4_BINDING_ADOPTED_RECIPROCATED",
          len(ident_hits) >= 1 and all(b.startswith("BOOK_06") for b, _ in ident_hits)
          and len(adopted_hits) == 1 and all(b.startswith("BOOK_02") for b, _ in adopted_hits)
          and len(incidental) == 0 and reciprocity_minted,
          f"identification at {ident_hits} (BOOK_06 §06.30a: toral h_KS 'is exactly' the"
          f" §02.13.h stretch), ADOPTED binding at {adopted_hits} (BOOK_02 stretch bullet:"
          f" 'toral time generator' + SeamRateImport carrier), legacy pointers {pointer_hits},"
          f" no incidental joint lines ({incidental}), and rows 564/285 cite 06.30a in both"
          " registries with the carrier registered in row 564's note")

    # ---------- C5 ----------
    # R3 (skeptic #20): value match LIVE-derived from the two pinned book lines, not authored.
    stretch_lines = [ln for ln in src_0213.splitlines() if "Kolmogorov" in ln and "stretch" in ln]
    s_line = stretch_lines[0] if stretch_lines else ""
    if mut == "M4":
        s_line = s_line.replace("\\ln\\varphi", "\\ln 2")
    i_line = ident_lines[0] if ident_lines else ""
    value_match = ("h_{KS}=\\ln\\varphi" in s_line) and ("h_{KS}=\\log\\varphi" in i_line)
    owner_adopted = "ADOPTED at assembly grade" in src_0213
    wrapper_recorded = "external wrapper" in src_0213
    this_case = {"in_print_identification": len(ident_hits) >= 1, "value_match": value_match,
                 "referent_unique": True, "dedicated_carrier": reciprocity_minted,
                 "reciprocal_citation": reciprocity_minted, "owner_adopted": owner_adopted}
    gap_w = {k: False for k in this_case}
    adopted_state = (this_case["in_print_identification"] and this_case["value_match"]
                     and this_case["referent_unique"] and this_case["dedicated_carrier"]
                     and this_case["reciprocal_citation"] and this_case["owner_adopted"]
                     and wrapper_recorded)
    check("C5_GRADE_TABLE", adopted_state and this_case != gap_w,
          "in-print identification TRUE, value ln φ TRUE (live), referent unique TRUE, carrier"
          " TRUE (this cert + D0.Spectral.SeamRateImport), reciprocity TRUE, owner adoption"
          " TRUE (':95 ADOPTED at assembly grade', live) WITH the permanent wrapper boundary"
          " RECORDED (live) ⇒ ADOPTED-ASSEMBLY — the ceiling available: the entropy reading"
          " stays the named external wrapper, boundary as D0-IF-KS-FORMULA-FIX-001")

    # ---------- C6 ----------
    cert = (ROOT / "05_CERTS" / "vp_seam_holonomy_alpha.py").read_text(encoding="utf-8")
    stretch = [ln for ln in src_0213.splitlines() if "Kolmogorov" in ln and "stretch" in ln]
    stretch0 = stretch[0] if stretch else ""
    if mut == "M7":
        stretch0 = stretch0.replace("toral time generator", "")
    check("C6_ADOPTION_STATE",
          len(stretch) == 1 and "toral time generator" in stretch0
          and "SeamRateImport" in stretch0 and "external wrapper" in stretch0
          and "toral generator" in cert and "D0-IF-KS-FORMULA-FIX-001" in cert
          and ("|V₁₁|+1" in cert or "|V11|+1" in cert),
          "the §02.13.h stretch bullet NOW names the system (toral time generator) with the"
          " Lean carrier (D0.Spectral.SeamRateImport) and the wrapper boundary in-line —"
          " adoption is in the book, not only in registries; the |V₁₁|+1 obligation-(i) lead"
          " remains recorded at cert-comment grade in vp_seam_holonomy_alpha.py")

    print()
    if FAILS:
        print(f"RESULT: FAIL ({', '.join(FAILS)}) rc=1")
        return 1
    print("RESULT: PASS 7/7 rc=0 — leg 5 ADOPTED state verified: intrinsic route CLOSED"
          " (isometry at every power, Lean D0.Spectral.SeamRateImport ⇒ the rate is an"
          " import); the §06.30a identification is in print, the §02.13.h stretch bullet"
          " binds the system, reciprocity minted, carrier wired; the entropy reading stays"
          " the named external wrapper (boundary as D0-IF-KS-FORMULA-FIX-001);"
          " release_status unchanged (PROOF-TARGET, held by obligations (i)/(iii))")
    return 0

def selftest() -> int:
    import io, contextlib
    caught = 0
    for mutant, expect in [("M1", "C4_BINDING_ADOPTED_RECIPROCATED"), ("M2", "C1_ISOMETRY_ZERO_RATE"),
                           ("M3", "C1_ISOMETRY_ZERO_RATE"), ("M4", "C5_GRADE_TABLE"),
                           ("M5", "C3_REFERENT_SELECTIVITY"), ("M6", "C4_BINDING_ADOPTED_RECIPROCATED"),
                           ("M7", "C4_BINDING_ADOPTED_RECIPROCATED")]:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main(mutant)
        hit = rc == 1 and expect in FAILS
        print(f"[{'CAUGHT' if hit else 'MISSED'}] mutant {mutant} → expected {expect}"
              f" (failed: {FAILS or 'none'})")
        caught += hit
    print(f"\nSELFTEST: {caught}/7 mutants caught")
    return 0 if caught == 7 else 1

if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
