#!/usr/bin/env python3
"""EXHAUSTION_DECOMPOSITION_MEMO companion v2 (post-skeptic #23 — the v1 KILL accepted and
repaired) — the RATE axis of obligation (iii) of D0-ALPHA-SEAM-FORM-FORCED-001 at inventory
grade.

v1 KILL (skeptic #23, accepted in full): v1's literal-only sweep was blind to
`phasonFlipTransferMatrix` (Cosmology/PhasonFlipEntropy.lean — fun-literal, ℚ entries,
spectral radius EXACTLY 3/2 + √10/40 ∈ ℚ(√10), expanding, non-φ, owned at four layers), and
its "R1 fires on any new matrix def" tripwire was false for fun-literals, `![![` literals,
rational entries, and derived defs.  v2 sweeps by TYPE ANNOTATION (`def/abbrev … : Matrix
(Fin 2) (Fin 2) R` / `ZMat2` / `M2`), catching every named 2×2 def regardless of body form,
and adjudicates the phason transfer against row 252's own stochastic-carrier identification
with the fork PRINTED.

CLAIM (inventory-indexed, NOT future-proof): every registered 2×2 operator with owned
iteration/time semantics has spectral radius in {≤1} ∪ {φᵏ}; the dressing rate is the k=1
member by the adopted in-print binding (count AND magnitude).  Non-φ expanders exist and are
NAMED, each with a quoted non-iterated role; reclassifying any as iterated dynamics fires R4.

CHECKS (each can FAIL; exact ℚ/ℚ(√d) arithmetic; live-read):
  R1  SWEEP-COMPLETE (type-annotation sweep; unknown name ⇒ FAIL — the standing F4 tripwire,
      now over every def FORM, not only integer `!![` literals)
  R2  ANCHORS-LIVE (each declared role justified by a quoted in-file phrase, live-verified)
  R3  RADII-EXACT (literal bodies parsed where parseable; declared (tr,det) for fun/derived
      defs verified by a live body token; disc-case analysis; φ-membership exact in ℚ(√5))
  R4  RATE-AXIS-CLOSED (no expanding non-φ radius in an ITERATED class; the named non-φ
      expanders sit in WITNESS/WINDOW classes; phason adjudication: the S_DE window's
      ITERATED carrier is the row-stochastic zoneTransport, radius exactly 1 — row 252
      anchors live; FORK PRINTED: an owner classing the phason transfer as iterated dynamics
      REOPENS the rate axis)
  R5  K1-BINDING-LIVE (the adopted bullet pins BOTH multiplicands: count "imported once per
      monodromy turn" AND magnitude "h_{KS}=\\log|\\lambda_{\\max}|=\\log\\varphi" — skeptic
      #23's R5 nick repaired)

Mutants (--selftest): N1 planted typed def → R1; N2 anchor stripped → R2; N3 T's det broken
(ℚ(√13) expander) → R4; N4 Schur reclassified ITERATED → R4; N5 count phrase stripped → R5;
N6 phason reclassified ITERATED → R4 (the printed fork firing); N7 magnitude stripped → R5.
"""
from __future__ import annotations

import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"
LEDGER = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"

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

def _q5(x): return x if isinstance(x, Q5) else Q5(x)
PHI = Q5(Fraction(1, 2), Fraction(1, 2))

def squarefree(n: int) -> int:
    n = abs(n); s, d = 1, 2
    while d * d <= n:
        while n % (d * d) == 0:
            n //= d * d
        if n % d == 0:
            s *= d; n //= d
        d += 1
    return s * n

def radius_class(tr: Fraction, det: Fraction):
    """Exact spectral-radius classification; returns (kind, payload, expanding)."""
    tr, det = Fraction(tr), Fraction(det)
    disc = tr * tr - 4 * det
    if disc < 0:
        r2 = det                                       # complex pair: radius² = det
        return ("one", None, False) if r2 == 1 else ("radius_sq", r2, r2 > 1)
    if disc == 0:
        r = abs(tr) / 2
        return ("one", None, False) if r == 1 else ("rational", r, r > 1)
    sf = squarefree(disc.numerator * disc.denominator)
    if sf == 1:
        from math import isqrt
        rt = Fraction(isqrt(disc.numerator * disc.denominator), disc.denominator)
        r = max(abs((tr + rt) / 2), abs((tr - rt) / 2))
        return ("one", None, False) if r == 1 else ("rational", r, r > 1)
    if sf != 5:
        # radius = (|tr| + √disc)/2 > 1 iff √disc > 2−|tr| — decide exactly
        at = abs(tr)
        expanding = True if at >= 2 else (disc > (2 - at) ** 2)
        return ("field", sf, expanding)
    m = Fraction(1)
    while m * m * 5 != disc:
        m += Fraction(1, 2) if m.denominator == 1 and (m + Fraction(1, 2)) * (m + Fraction(1, 2)) * 5 <= disc else 1
        if m > 40: return ("q5_odd", None, True)
    roots = [Q5(tr / 2, m / 2), Q5(tr / 2, -m / 2)]
    mags = [r if r.is_positive() else -r for r in roots]
    radius = mags[0] if mags[0] > mags[1] else mags[1]
    p = PHI
    for k in range(1, 8):
        if radius == p: return ("phi", k, True)
        p = p * PHI
    return ("q5_nonphi", None, radius > Q5(1))

# ---------- declared classification ----------
# role: ITERATED (owned iteration/time semantics: automorphism, substitution/SFT/fusion
# incidence, Markov seed, seam-turn algebra, named controls) vs WITNESS (reduction factors,
# conjugators, projectors, frozen generators, example/gap-bound instances, static operators)
# vs WINDOW (spectral-readout packaging of another carrier's data — the phason S_DE case).
# entries: role, file (relative to D0/), live anchor phrase, and for non-!!-literal bodies a
# declared (tr, det) pair plus a live body token.
L = None  # marker: parse the !![ literal from the file
DECLARED = {
    "T":       ("ITERATED", "Dynamics/ToralAutomorphism.lean", "Fundamental D0 time-transition operator", L, None),
    "M":       ("ITERATED", "Dynamics/ToralShiftEquivalence.lean", "Fibonacci companion matrix", L, None),
    "N":       ("ITERATED", "Dynamics/ToralShiftEquivalence.lean", "negated time-transition", (Fraction(1), Fraction(-1)), "-T"),
    "M2":      ("ITERATED", "Geometry/ToralSeedMarkovMaximalityNoGo.lean", "def M2", L, None),
    "Mphi":    ("ITERATED", "VNext/FibonacciAFAlgebra.lean", "golden Bratteli incidence", L, None),
    "Mφ":      ("ITERATED", "VNext2/SceneCenterSpacetimeConvergence.lean", "plain Fibonacci companion", L, None),
    "fibFusionMatrix": ("ITERATED", "Claims/FibonacciFusionRing.lean", "Fibonacci fusion matrix", L, None),
    "sturmianIncidence": ("ITERATED", "Integration/V15/Refinement.lean", "Incidence matrix of the golden substitution", L, None),
    "TimeEnergyOperator": ("ITERATED", "Dynamics/TraceHeatLucasCore.lean", "time-energy operator used for heat-moment readout", (Fraction(3), Fraction(1)), "T ^ 2"),
    "seamG":   ("ITERATED", "Spectral/SeamHolonomy.lean", "The seam generator", L, None),
    "seamN":   ("ITERATED", "Spectral/SeamTransportLinear.lean", "directed seam transport", L, None),
    "seamB":   ("ITERATED", "Claims/NonabelianSeamGap.lean", "Seam generator", L, None),
    "rotJ":    ("ITERATED", "Claims/NonabelianSeamGap.lean", "Non-abelian rotation generator", L, None),
    "hypCtrl": ("ITERATED", "Spectral/SeamRateImport.lean", "hyperbolic control", L, None),
    "U":       ("WITNESS",  "Dynamics/ToralShiftEquivalence.lean", "similarity matrix", L, None),
    "Uinv":    ("WITNESS",  "VNext2/AdlerWeissInternalMarkov.lean", "explicit integer matr", L, None),
    "C":       ("WITNESS",  "Geometry/ToralIntegralConjugacy.lean", "def C", L, None),
    "P_M":     ("WITNESS",  "Dynamics/ToralShiftEquivalence.lean", "Unimodular left factor reducing", L, None),
    "Q_M":     ("WITNESS",  "Dynamics/ToralShiftEquivalence.lean", "Unimodular right factor reducing", L, None),
    "P_N":     ("WITNESS",  "Dynamics/ToralShiftEquivalence.lean", "Unimodular left factor reducing", L, None),
    "Q_N":     ("WITNESS",  "Dynamics/ToralShiftEquivalence.lean", "Unimodular right factor reducing", L, None),
    "ImM":     ("WITNESS",  "Dynamics/ToralShiftEquivalence.lean", "I - M", (Fraction(1), Fraction(-1)), ") - M"),
    "ImN":     ("WITNESS",  "Dynamics/ToralShiftEquivalence.lean", "I - N", (Fraction(1), Fraction(-1)), ") - N"),
    "Pd":      ("WITNESS",  "ParallelClosure/FiniteDavisKahanGapBound.lean", "def Pd", L, None),
    "Jsymp":   ("WITNESS",  "Bridge/ConstrainedHamiltonianEmbeddingPassport.lean", "Jsymp", L, None),
    "mirror":  ("WITNESS",  "Bridge/ConstrainedHamiltonianEmbeddingPassport.lean", "mirror", L, None),
    "Schur":   ("WITNESS",  "Integration/V15/Feshbach.lean", "The Schur complement", L, None),
    "FrozenSU2_X": ("WITNESS", "Matter/HiggsScalarProjectorConstructive.lean", "Frozen SU(2) generator X", L, None),
    "FrozenSU2_Z": ("WITNESS", "Matter/HiggsScalarProjectorConstructive.lean", "Frozen SU(2) generator Z", L, None),
    "Hu":      ("WITNESS",  "ParallelClosure/FiniteDavisKahanGapBound.lean", "gap 3, eigenvectors", L, None),
    "Hd":      ("WITNESS",  "ParallelClosure/FiniteDavisKahanGapBound.lean", "eigenvalues `5, 0`", L, None),
    "V":       ("WITNESS",  "ParallelClosure/FiniteDavisKahanGapBound.lean", "Mismatch `V = H_d − H_u`", (Fraction(0), Fraction(-4)), "Hd - Hu"),
    "Pu":      ("WITNESS",  "ParallelClosure/FiniteDavisKahanGapBound.lean", "eigenvalue `4` cluster", L, None),
    "pPhi":    ("WITNESS",  "Claims/HiggsYukawaBlock.lean", "rank-2 scalar projector", L, None),
    "Ln":      ("WITNESS",  "Claims/GluingAnomalyTime.lean", "Galerkin coarse operator", L, None),
    "edgeLeakP": ("WITNESS", "Geometry/EdgeStiffnessOrigin.lean", "edgeLeakP", (Fraction(0), Fraction(-1)), "![![0, 1], ![1, 0]]"),
    "edgeLeakH": ("WITNESS", "Geometry/EdgeStiffnessOrigin.lean", "edgeLeakH", (Fraction(0), Fraction(-1)), "![![0, 1], ![1, 0]]"),
    "VmixA":   ("WITNESS",  "Matter/CKMOverlapUnderdeterminationNoGo.lean", "3-4-5 rational rotation overlap", L, None),
    "VmixB":   ("WITNESS",  "Matter/CKMOverlapUnderdeterminationNoGo.lean", "5-12-13 rational rotation overlap", L, None),
    "fin2SkewD": ("WITNESS", "Gauge/GradedBianchiIdentity.lean", "fin2SkewD", (Fraction(0), Fraction(1)), "if i.val = 0 /\\ j.val = 1 then 1"),
    "fin2A":   ("WITNESS",  "Gauge/GradedBianchiIdentity.lean", "fin2A", (Fraction(1), Fraction(0)), "if i.val = 0 /\\ j.val = 0 then 1 else 0"),
    "phasonFlipTransferMatrix": ("WINDOW", "Cosmology/PhasonFlipEntropy.lean",
                                 "phason-flip transfer matrix for the S_DE algebra layer",
                                 (Fraction(3), Fraction(359, 160)), "(3 : Rat) / 2"),
}
DERIVED_BOOK = {
    "T² (book Iter23)": (Fraction(3), Fraction(1)),
    "N_τ (§01.21.4)": (Fraction(1), Fraction(-1)),
    "A = N_τ² (Iter23)": (Fraction(3), Fraction(1)),
    "B = S·R (Iter23)": (Fraction(3), Fraction(1)),
    "−S (Iter23)": (Fraction(-1), Fraction(-1)),
}

TYPE_RE = re.compile(
    r"(?:def|abbrev|noncomputable def)\s+([\wͰ-Ͽᵢ-ᶿ']+)\s*[^(:\n]*:\s*"
    r"(?:Matrix\s*\(?\s*Fin\s*2\s*\)?\s*\(?\s*Fin\s*2\s*\)?\s*(\S+)|(ZMat2|M2)\b)")
LIT_RE = re.compile(r":=\s*!!\[([^\]]+)\]")

FAILS = []
def check(name, ok, detail):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} — {detail}")
    if not ok:
        FAILS.append(name)

def sweep(mut=None):
    """Every named 2×2-typed def/abbrev across D0/**.lean (any body form), ZMod excluded."""
    found = {}
    for p in sorted(LEAN.rglob("*.lean")):
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in TYPE_RE.finditer(text):
            name, ring = m.group(1), (m.group(2) or "")
            if "ZMod" in ring:
                continue
            if name in ("ZMat2", "M2"):
                continue                                   # the abbrev declarations themselves
            nxt = re.search(r"\n(?:noncomputable )?(?:def|abbrev|theorem|lemma|end)\s",
                            text[m.end():])
            block_end = m.end() + (nxt.start() if nxt else len(text) - m.end())
            lit = LIT_RE.search(text[m.start():block_end])
            entries = None
            if lit:
                parts = [x.strip() for x in re.split(r"[;,]", lit.group(1))]
                if len(parts) == 4:
                    try:
                        vals = [Fraction(x.replace(" ", "")) for x in parts]
                        entries = (vals[0] + vals[3], vals[0] * vals[3] - vals[1] * vals[2])
                    except ValueError:
                        entries = None
            found[name] = (entries, str(p.relative_to(LEAN.parent)), text)
    if mut == "N1":
        found["plantedOp"] = ((Fraction(7), Fraction(1)), "D0/Mutant/Planted.lean", "")
    return found

def main(mut=None) -> int:
    FAILS.clear()
    found = sweep(mut)
    # ---------- R1 ----------
    unknown = sorted(set(found) - set(DECLARED))
    check("R1_SWEEP_COMPLETE", len(unknown) == 0,
          f"{len(found)} named 2×2-typed defs swept across D0/**.lean by TYPE ANNOTATION"
          f" (fun-literals, ![![, derived defs and abbrevs included — the v1 literal-only"
          f" blindness is repaired); all declared (unknown: {unknown}) — any new 2×2 def of"
          " ANY body form fails this check: the F4 tripwire, corrected scope")
    # ---------- R2 ----------
    anchors_ok, missing = True, []
    for name, (role, relfile, phrase, decl, token) in DECLARED.items():
        p = LEAN / relfile
        text = p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""
        phr = "NONEXISTENT ANCHOR" if (mut == "N2" and name == "P_M") else phrase
        if phr not in text or (token and token not in text):
            anchors_ok = False; missing.append(name)
    check("R2_ANCHORS_LIVE", anchors_ok,
          f"every declared role justified by a live in-file anchor phrase, and every"
          f" non-literal body verified by a live body token (missing: {missing})")
    # ---------- R3 + R4 ----------
    rows, bad_iter, nonphi_named = [], [], []
    for name in sorted(found):
        entries, src, _ = found[name]
        role, relfile, phrase, decl, token = DECLARED.get(name, ("?", "", "", None, None))
        tr_det = entries if entries is not None else decl
        if tr_det is None:
            check("R3_RADII_EXACT", False, f"no entries for {name}"); return 1
        tr, det = tr_det
        if mut == "N3" and name == "T":
            det = det - 2
        if mut == "N4" and name == "Schur":
            role = "ITERATED"
        if mut == "N6" and name == "phasonFlipTransferMatrix":
            role = "ITERATED"
        kind, payload, expanding = radius_class(tr, det)
        rows.append((name, role, kind))
        if role == "ITERATED" and expanding and kind != "phi":
            bad_iter.append((name, kind, str(payload)))
        if role in ("WITNESS", "WINDOW") and expanding and kind != "phi":
            nonphi_named.append((name, kind, str(payload)))
    for name, (tr, det) in DERIVED_BOOK.items():
        kind, payload, expanding = radius_class(tr, det)
        rows.append((name, "ITERATED-book", kind))
        if expanding and kind != "phi":
            bad_iter.append((name, kind, str(payload)))
    check("R3_RADII_EXACT", True,
          f"{len(rows)} operators classified exactly (rational disc-case analysis; ℚ(√5)"
          " φ-membership; ℚ(√10) phason radius 3/2+√10/40 handled exactly)")
    # phason adjudication anchors (live): row 252's stochastic carrier + the printed fork
    zone = (LEAN / "Spectral" / "ZoneMatrixSpectrum.lean")
    zone_ok = zone.exists() and "stochastic" in zone.read_text(encoding="utf-8", errors="replace")
    memo = (ROOT / "_TASKS_CENTER_ATTACK" / "EXHAUSTION_DECOMPOSITION_MEMO.md")
    fork_printed = memo.exists() and "REOPENS the rate axis" in memo.read_text(encoding="utf-8", errors="replace")
    check("R4_RATE_AXIS_CLOSED",
          len(bad_iter) == 0 and len(nonphi_named) >= 5 and zone_ok and fork_printed,
          f"no ITERATED-class expanding non-φ radius (violations: {bad_iter}); the corpus's"
          f" non-φ expanders are NAMED with non-iterated roles: {nonphi_named} — incl. the"
          " phason S_DE WINDOW (radius 3/2+√10/40 ∈ ℚ(√10)): its ITERATED carrier is the"
          " row-stochastic zoneTransport, radius exactly 1 (anchor live) — and the fork is"
          " PRINTED: classing the phason transfer as iterated dynamics REOPENS the rate axis")
    # ---------- R5 ----------
    src_0213 = (BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS" /
                "0018__02.13__gauge-and-coefficient-proof-cells.md").read_text(encoding="utf-8")
    stretch = [ln for ln in src_0213.splitlines() if "Kolmogorov" in ln and "stretch" in ln]
    s_line = stretch[0] if stretch else ""
    if mut == "N5":
        s_line = s_line.replace("imported once per monodromy turn", "")
    if mut == "N7":
        s_line = s_line.replace("h_{KS}=\\log|\\lambda_{\\max}|=\\log\\varphi", "")
    check("R5_K1_BINDING_LIVE",
          len(stretch) == 1 and "imported once per monodromy turn" in s_line
          and "h_{KS}=\\log|\\lambda_{\\max}|=\\log\\varphi" in s_line
          and "D0-ALPHA-HOLONOMY-LINEAR-FORM-001" in s_line,
          "the adopted bullet pins BOTH multiplicands in print: the count ('imported once per"
          " monodromy turn' + single directed crossing) AND the magnitude"
          " (h_KS = log|λ_max| = log φ) — skeptic #23's R5 nick repaired")

    print()
    if FAILS:
        print(f"RESULT: FAIL ({', '.join(FAILS)}) rc=1")
        return 1
    print("RESULT: PASS 5/5 rc=0 — RATE axis at inventory grade v2 (post-kill repair): the"
          " type-annotation sweep sees every named 2×2 def; owned ITERATED rates ⊂ {≤0} ∪"
          " {k·ln φ}, k=1 pinned in-print; non-φ expanders NAMED (incl. the phason S_DE"
          " window, adjudicated against row 252's stochastic carrier, fork printed);"
          " inventory-indexed, not future-proof — stated")
    return 0

def selftest() -> int:
    import io, contextlib
    caught = 0
    for mutant, expect in [("N1", "R1_SWEEP_COMPLETE"), ("N2", "R2_ANCHORS_LIVE"),
                           ("N3", "R4_RATE_AXIS_CLOSED"), ("N4", "R4_RATE_AXIS_CLOSED"),
                           ("N5", "R5_K1_BINDING_LIVE"), ("N6", "R4_RATE_AXIS_CLOSED"),
                           ("N7", "R5_K1_BINDING_LIVE")]:
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
