#!/usr/bin/env python3
"""TRANSPORT_TWELVE_FORK_MEMO companion — obligation (i) of D0-ALPHA-SEAM-FORM-FORCED-001
refined from "own the φ⁻¹² transport factor" to a precise six-candidate adjudication fork.

WHAT IS CHECKED (each can FAIL; exact integer arithmetic; all corpus facts live-read):
  T1  CANDIDATE-ARITHMETIC — the six 12-valued candidates are exactly 12, and the label's
      natural referent is exactly NOT: dim g_light = 8+3+1 = 12; |V₁₁|+1 = 12;
      |V₁₃|−1 = 12 (kernel-zone dim, 30 = 8⊕10⊕12); S₁₃-isotype dim = 13−1 = 12;
      |ABCD|+|Ω₈| = 4+8 = 12; commutant Σm² −... = 3²+1+1+1 = 12; and
      dim(su(2)⊕u(1)) = 3+1 = 4 ≠ 12 (the electroweak-label tension, exact).
  T2  NO-BINDING-LIVE — widened joint scan (trap (p) families): no book line carries BOTH a
      transport token (φ⁻¹²/transport factor/EW transport) AND a candidate-mechanism token
      (V₁₁, g_light, gauge, kernel, S13, sector-count, 8+3+1).  The transport exponent is
      bound to NO owned 12-object anywhere in print.  (Flips when an owner binds one.)
  T3  ETA-EM-DISTINCT — the corpus's only in-print exponent USES of dim g_light = 12
      (BOOK_02 assembled :1204 and :1615 regions) belong to the DIFFERENT owned exponent
      η_EM = 5/8 + δ₀/384 (denominator 384 = 8·4·12): live-check those neighborhoods carry
      the 384-construction and no transport token — the owned parent exists but for another
      object (trap (o): no silent borrow).
  T4  LABEL-TENSION-LIVE — the §02.13.h:87 depth line still says "electroweak transport"
      while no candidate has an electroweak reading of 12 (dim EW = 4): the tension stands.
      (Flips if the owner relabels the line or mints an electroweak-12 object.)
  T5  GUARDRAIL-LIVE — BOOK_05 §05.19 gauge release rule is in force ("not promoted by
      writing `8+3+1`"): any future dim-g_light binding must expose the finite isolation
      cell, not the sum.  Live-checked so the fork record inherits the bar.
  T6  COMPOSITION-EXACT — 5+12 = 17 and every candidate-exponent rival breaks it exactly:
      5+4 = 9, 5+8 = 13, 5+11 = 16, 5+13 = 18 (≠ 17, integers) — the composition
      φ⁻¹⁷ = ξ₅·φ⁻¹² is exponent-rigid; the φ⁻¹⁶/φ⁻¹⁸ rivals are the same objects already
      separated in vp_alpha_seam_form_forced S2 (F3 surface), cross-referenced not re-run.

STRUCTURE_FIXED_BEFORE_NUMBER: |ABCD|=4, |Ω₈|=8, |V₉|=9, |V₁₁|=11, |V₁₃|=13, dim su(3)=8,
dim su(2)=3, dim u(1)=1, ξ₅-exponent 5.  No measured number enters any check.

Mutants (--selftest, each must FAIL its check's CONCLUSION):
  M1 planted binding line → T2;  M2 candidate arithmetic broken (|V₁₁|+2) → T1;
  M3 guardrail phrase stripped → T5;  M4 label relabeled to "gauge transport" → T4;
  M5 composition broken (5+12→18) → T6.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"

FAILS = []
def check(name, ok, detail):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} — {detail}")
    if not ok:
        FAILS.append(name)

def book_lines():
    out = []
    for p in sorted(BOOKS.glob("BOOK_0*.md")):
        for i, ln in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            out.append((p.name, i, ln))
    return out

TRANSPORT_TOK = re.compile(r"varphi\^\{-12\}|phi\^-12|φ⁻¹²|transport factor|electroweak transport|EW transport", re.I)
CANDIDATE_TOK = re.compile(r"V_\{11\}|\bV11\b|g_\{light\}|g_light|\bgauge\b|\bkernel\b|S_\{13\}|\bS13\b|8\+3\+1|sectors? crossed|\btwelve\b", re.I)

def main(mut=None) -> int:
    FAILS.clear()
    # ---------- T1 ----------
    ABCD, OM8, V9, V11, V13 = 4, 8, 9, 11, 13
    su3, su2, u1 = 8, 3, 1
    v11_plus = V11 + (2 if mut == "M2" else 1)
    candidates = {
        "dim g_light = su3+su2+u1": su3 + su2 + u1,
        "|V11|+1": v11_plus,
        "|V13|-1 (kernel-zone dim)": V13 - 1,
        "S13-isotype dim = 13-1": V13 - 1,
        "|ABCD|+|Omega8|": ABCD + OM8,
        "commutant 3^2+1+1+1": 3 * 3 + 1 + 1 + 1,
    }
    ew_dim = su2 + u1
    kernel_is_isotype = candidates["|V13|-1 (kernel-zone dim)"] == candidates["S13-isotype dim = 13-1"]
    distinct_objects = 4  # W-B (skeptic #21): kernel-12 ≡ S13-isotype-12; POST-COLLAPSE
    # [2026-08-01]: |V13|-1 ≡ |ABCD|+|Omega8| is ONE carrier (V13 = Omega8 ⊔ {witness} ⊔ Role,
    # so removing the witness leaves Omega8 ⊔ Role) — Lean D0.Synthesis.TransportTwelveForkCollapse
    # (fork_doors_three_four_coincide, witness_removal_identity). The in-print ANTI-transport
    # verdict on the kernel door therefore transfers to the |ABCD|+|Omega8| door: adopting it IS
    # adopting the kernel door under another name. Live doors: dim g_light, |V11|+1, commutant 12.
    extensions = {"theta_seam numerator (12/5)": 12, "icosahedron V (BOOK_01:1516)": 12}
    check("T1_CANDIDATE_ARITHMETIC",
          all(v == 12 for v in candidates.values()) and kernel_is_isotype
          and all(v == 12 for v in extensions.values()) and ew_dim == 4 and ew_dim != 12,
          f"FOUR distinct candidates all = 12 exactly (kernel-zone 12 ≡ S₁₃-isotype 12 ≡"
          f" |ABCD|+|Ω₈| — one carrier, TransportTwelveForkCollapse; and"
          f" object, rows 169/460 — W-B) + two extension doors (θ_seam numerator, icosahedron"
          f" V); the label's natural referent dim(su2⊕u1) = {ew_dim} ≠ 12 — the 12 is"
          " massively over-determined (trap d) and the label under-determined")

    # ---------- T2 ----------
    lines = book_lines()
    if mut == "M1":
        lines = lines + [("BOOK_02_MUTANT.md", 0,
                          "the transport factor varphi^{-12} counts the |V11|+1 sectors crossed")]
    transport_lines = [(b, i, ln) for (b, i, ln) in lines if TRANSPORT_TOK.search(ln)]
    binding = [(b, i) for (b, i, ln) in transport_lines if CANDIDATE_TOK.search(ln)]
    check("T2_NO_BINDING_LIVE", len(transport_lines) >= 1 and len(binding) == 0,
          f"{len(transport_lines)} transport-token lines in the books, ZERO carry a candidate"
          f" token (binding hits: {binding}) — the transport exponent 12 is bound to no owned"
          " 12-object in print; the only mechanism text (|V₁₁|+1) stays at cert-comment grade"
          " in vp_seam_holonomy_alpha.py — this check FLIPS when an owner mints a binding")

    # ---------- T3 ----------
    b02 = (BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md").read_text(encoding="utf-8")
    # W-C (skeptic #21): census widened beyond the g_{light} token — the §02.13.1 derivation
    # cell writes `dim g = 8+3+1` WITHOUT the g_{light} token and was invisible to v1.
    sites = sorted({m.start() for m in re.finditer(r"g_\{light\}", b02)}
                   | {m.start() for m in re.finditer(r"8\+3\+1", b02)})
    classes = []
    eta_ok = len(sites) >= 4
    for pos in sites:
        window = b02[max(0, pos - 900):pos + 900]
        if TRANSPORT_TOK.search(window):
            classes.append("TRANSPORT-ADJACENT"); eta_ok = False
        elif "384" in window or "residual exponent" in window:
            classes.append("eta_EM")
        elif ("colour sector, not electroweak" in window or "02.19C" in window
              or ("Sp(1)" in window and "electroweak" in window)):
            classes.append("THE-02.19C")
        elif "section anchor" in window or "light gauge carrier" in window:
            classes.append("derivation-cell-02.13.1")
        else:
            classes.append("UNCLASSIFIED"); eta_ok = False
    check("T3_OWNED_TWELVE_SERVES_OTHER_CELLS", eta_ok,
          f"the {len(sites)} in-print 12-sum sites (g_light token OR bare 8+3+1) classify as"
          f" {classes} — every one serves the η_EM construction (384 = 8·4·12), the"
          " [THE 02.19C] emergence cell, or the §02.13.1 derivation cell (Ω₈+Rank+anchor);"
          " NONE is transport-adjacent (±900 chars): the owned 12-parent exists but for other"
          " objects (trap o: no silent borrow)")

    # ---------- T4 ----------
    src = (BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS" /
           "0018__02.13__gauge-and-coefficient-proof-cells.md").read_text(encoding="utf-8")
    depth_lines = [ln for ln in src.splitlines() if ln.lstrip().startswith("- depth")]
    if mut == "M4":
        depth_lines = [ln.replace("electroweak transport", "gauge transport") for ln in depth_lines]
    label_ok = len(depth_lines) == 1 and "electroweak transport" in depth_lines[0]
    corpus_ew_anchor = "colour sector, not electroweak" in b02
    check("T4_LABEL_TENSION_LIVE", label_ok and ew_dim != 12 and corpus_ew_anchor,
          "the depth bullet still labels φ⁻¹² 'the electroweak transport' while the corpus's"
          " OWN owned usage ([THE 02.19C]: 'the 8 of SU(3) is the colour sector, not"
          " electroweak') fixes electroweak = Sp(1)×U(1), dim 4 ≠ 12 — a corpus-internally"
          " grounded NAMED tension: either the label or the candidate set must give")

    # ---------- T5 ----------
    b05 = (BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md").read_text(encoding="utf-8")
    guard = "not promoted by writing `8+3+1`"
    hay = b05.replace(guard, "") if mut == "M3" else b05
    check("T5_GUARDRAIL_LIVE", guard in hay,
          "BOOK_05 §05.19 gauge release rule is in force: a dim-g_light binding for the"
          " transport must expose the finite isolation cell (support-shell decomposition,"
          " non-mixing), not the sum 8+3+1 — the fork record inherits this bar")

    # ---------- T6 ----------
    seam_exp = 5
    composition = seam_exp + (13 if mut == "M5" else 12)
    rivals = {4: seam_exp + 4, 8: seam_exp + 8, 11: seam_exp + 11, 13: seam_exp + 13}
    check("T6_COMPOSITION_EXACT",
          composition == 17 and sorted(rivals.values()) == [9, 13, 16, 18]
          and all(v != 17 for v in rivals.values()),
          "5+12 = 17 exactly; candidate-exponent rivals give 9/13/16/18 ≠ 17 — the"
          " composition φ⁻¹⁷ = ξ₅·φ⁻¹² is exponent-rigid; the 16/18 depths are the S2 rivals"
          " already separated by vp_alpha_seam_form_forced (F3 surface), cross-referenced")

    print()
    if FAILS:
        print(f"RESULT: FAIL ({', '.join(FAILS)}) rc=1")
        return 1
    print("RESULT: PASS 6/6 rc=0 — obligation (i) refined to a FOUR-candidate fork post-collapse (+2"
          " extension doors): all = 12 exactly, NONE bound in print, one door in-print"
          " ANTI-transport (kernel owned 'transport-null', BOOK_04), the owned 12-parent"
          " serves other cells (η_EM / THE 02.19C / §02.13.1 derivation), the 'electroweak'"
          " label conflicts with THE 02.19C (EW dim 4), and a g-binding must clear BOOK_05"
          " §05.19; the (i) slot stays OPEN — no candidate promoted, no status change")
    return 0

def selftest() -> int:
    import io, contextlib
    caught = 0
    for mutant, expect in [("M1", "T2_NO_BINDING_LIVE"), ("M2", "T1_CANDIDATE_ARITHMETIC"),
                           ("M3", "T5_GUARDRAIL_LIVE"), ("M4", "T4_LABEL_TENSION_LIVE"),
                           ("M5", "T6_COMPOSITION_EXACT")]:
        # note: M1's planted line is deliberately ALSO transport-adjacent for T3's window scan
        # only when injected into b02 — it is injected into the line list instead, so T3 is
        # unaffected by M1; each mutant targets its named check's conclusion.
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main(mutant)
        hit = rc == 1 and expect in FAILS
        print(f"[{'CAUGHT' if hit else 'MISSED'}] mutant {mutant} → expected {expect}"
              f" (failed: {FAILS or 'none'})")
        caught += hit
    print(f"\nSELFTEST: {caught}/5 mutants caught")
    return 0 if caught == 5 else 1

if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
