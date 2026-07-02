# TASK W1 — Exact Ihara–Bass certificate + NB/E family audit

**Goal:** produce a D0-style executable certificate `vp_scene_ihara_bass_nb.py` proving, in exact
arithmetic, the structural facts behind candidate theorem T1, and document precisely how the three
vNext2 refinement families (W / NB / E) were constructed and what distinguishes NB from E.

**Repo:** `/Users/grigorijvahrusev/Downloads/d0_15/`

## Context (self-contained)

The scene is the complete tripartite graph K(9,11,13): 33 vertices in zones of size 9/11/13, edges
between different zones only. |E| = 359, directed edges 718. The vNext2 verdict
`D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001` (see `04_VERIFICATION/VNEXT2_SCENE_NATIVE_DEPENDENCY_GRAPH.md`
and `09_LEAN_FORMALIZATION/D0/VNext2/SceneNativeRefinementClassification.lean`) declared three history
families M1-admissible but inequivalent: W (all-walks, dim 33), NB (non-backtracking, dim 718),
E (directed-edge, dim 718). The architect's T1 claim: W double-counts the typed p²-return channel
(depth-2 excess 15708−14990 = 718 = 2|E| = exactly one immediate backtrack per directed edge), and
NB/E are carrier-vs-dynamics of one object (Hashimoto operator B), glued to the 33-dim scene by the
Ihara–Bass identity. Existing cert style examples: `05_CERTS/vp_*.py` (pick any recent one as template;
they are deterministic, exit non-zero on FAIL, and include reachable negative controls).

## Steps

1. **Family audit (read-only):** read `D0/VNext2/SceneNativeRefinementClassification.lean` and every
   `04_VERIFICATION/VNEXT2_*` file. Document, with quotes: the exact constructions of W, NB, E; the
   exact meaning of "depth-2 carriers 15708 ≠ 14990" and "transfer dims 33 ≠ 718"; and what (if
   anything) distinguishes the NB family from the E family beyond carrier presentation. This is the
   most important deliverable — T1 needs to know whether NB and E are literally the same operator.
2. **Cert, exact arithmetic** (`fractions.Fraction` / integers only; no floats in PASS/FAIL logic):
   a. Build K(9,11,13); assert |V|=33, |E|=359, degrees (24,22,20), rank(A)=3 (integer row-reduction).
   b. Assert Σd² = 15708, Σd(d−1) = 14990, difference = 718 = 2|E|, and that the excess is in
      bijection with directed edges (count immediate-backtrack length-2 walks directly).
   c. Build the Hashimoto matrix B (718×718, integer): (u→v) → (v→w), w ≠ u.
   d. Verify Ihara–Bass det(I−uB) = (1−u²)^(|E|−|V|) · det(I−uA+u²(D−I)) **exactly** at ≥5 rational
      u values. Recommended route: fraction-free Bareiss or multi-prime modular determinants
      (verify mod ≥3 large primes with CRT consistency); sympy is acceptable if runtime allows.
   e. Verify the nonzero adjacency spectrum exactly: the tripartite quotient is the 3×3 matrix
      Q = [[0,11,13],[9,0,13],[9,11,0]] (zone sizes as multiplicities); assert charpoly of the
      rank-3 part equals λ³ − 359λ − 2574 = 0, i.e. the §08.12.4 "vacuum cubic" is the adjacency
      charpoly of the scene. State this as a FINDING row, not a fork resolution.
   f. **Negative controls (must be reachable):** (i) run the same identity with backtracking
      transitions included in B — must FAIL; (ii) run on K(9,11,15) — the invariants 359/718/15708
      must change; assert the cert detects it; (iii) wrong Bass exponent (|E|−|V|±1) must FAIL.
3. Write a short report `TASK_W1_REPORT.md` next to this file: family-audit answer, cert results,
   runtime, and any surprise (e.g. if NB ≠ E as operators, describe the exact difference).

## Acceptance criteria

- Cert runs deterministically, PASSes on the scene, and every negative control demonstrably FAILs.
- No floats in decision logic. No status/claim edits anywhere in the repo.
- The NB-vs-E question is answered with file/line citations, even if the answer is "they differ, here's how".
