# TASK W5 — Literature sweep: external theorem-owners for T1 and the time↔flavor link

**Goal:** an annotated bibliography of EXTERNAL theorems that can own specific D0 steps, with exact
statements and a mapping to D0 claim IDs. D0 discipline explicitly allows citing external owners
(Dedekind, Ostrik, Hollander–Solomyak are already cited this way) — we do not re-prove known math.

**Requires:** web access. No repo edits; deliver a single report.

## Thread A — Non-backtracking / Ihara zeta (feeds T1)

D0 need: promote the non-backtracking (Hashimoto) history family to the CANONICAL scene refinement
rule, with the Ihara–Bass identity as the intertwiner between the 718-dim edge transfer and the
33-dim scene data (A, D) on K(9,11,13). Collect, with precise statements and original citations:

1. Hashimoto (1989) and Bass (1992): the Ihara–Bass determinant formula for general (irregular)
   finite graphs — exact hypotheses (md2? connectivity?), exact statement.
2. Kotani–Sunada (2000) "Zeta functions of finite graphs": spectral structure of B for irregular
   graphs; what is known about the unit-circle eigenvalues and the Perron value.
3. Uniqueness/canonicity results: any theorem singling out the NB operator among walk operators —
   e.g. Angel–Friedman–Hoory (non-backtracking spectrum of the universal cover), Bordenave–Lelarge–
   Massoulié 2015+ (NB spectral redemption / community detection: why NB succeeds where A fails),
   Terras "Zeta Functions of Graphs" (which primes/cycles the zeta counts: NB cycles ONLY —
   backtracking cycles are excluded by definition of the graph zeta). The sharpest available
   statement of "the graph-theoretic zeta is intrinsically non-backtracking" is the prize here.
4. Weighted/typed versions: Watanabe–Fukumizu (graph zeta and loopy belief propagation), any result
   where the immediate-backtrack terms are identified as a separately-typed correction (this is the
   external mirror of D0's typed p²-return channel; the depth-2 identity Σd² − Σd(d−1) = 2|E| is
   trivial, we need the CONCEPTUAL owner that treats backtracks as a distinct channel).

## Thread B — Modular A₅ / golden-ratio flavor (feeds D0-MODULAR-TIME-FLAVOR-001, MECH-LIMIT)

D0 need: the corpus proves the flavor group A₅ ≅ PSL(2,5) (icosian route) and the toral time
generator as a golden hyperbolic element of GL(2,ℤ), and flags the full time↔flavor identification
as its named open gap (BOOK_06 §06.30a). Collect:

1. Feruglio (2017) modular-invariance flavor paradigm: exact setup (modular forms of level N,
   finite modular groups Γ_N; Γ_5 ≅ A₅).
2. Golden-ratio mixing from A₅: Ding–Everett–Stuart / Feruglio et al. — which mixing angles are
   predicted with φ, and from which stabilizers; note any appearance of tan θ = 1/φ or φ⁻².
3. Level-5 modular forms and the icosahedron (Klein): the classical A₅ ↔ level-5 correspondence.
4. Any result connecting a HYPERBOLIC SL(2,ℤ) element (Anosov/toral automorphism) with a finite
   level quotient acting as flavor symmetry — even partial. If nothing exists, say so: it means the
   D0 gap is genuinely novel, which is also valuable information.

## Deliverable

`TASK_W5_REPORT.md`: for each item — full citation, the exact theorem statement (verbatim or
faithfully condensed), hypotheses, and one line "maps to D0 claim/step: <claim-id or book section>".
End with a ranked shortlist: the 3 external theorems most likely to become named owners of D0 rows,
and any mismatch risks (e.g. md2 hypothesis failing on some D0 carrier).

## Acceptance criteria

- Primary sources (papers/books), not blog posts; arXiv IDs where available.
- Statements precise enough that the architect can write an owner-edge row without re-reading the paper.
- Honest nulls: if a hoped-for theorem does not exist, record the absence explicitly.
