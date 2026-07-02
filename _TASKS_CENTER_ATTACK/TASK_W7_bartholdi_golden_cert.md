# TASK W7 — Typed (Bartholdi) zeta certificate: exact identity + golden-point specialization

**Goal:** turn the T1 addendum's verified-in-float structure into an exact, D0-style certificate and
a sourced external-owner row. This is the weighted successor of TASK W1's cert; read
`_TASKS_CENTER_ATTACK/T1_FORCING_MEMO.md` and `T1_FORCING_MEMO_ADDENDUM.md` first.

**Repo:** `/Users/grigorijvahrusev/Downloads/d0_15/`
**Deliverables only into `_TASKS_CENTER_ATTACK/`** (cert NOT in `05_CERTS/` — keep it out of CI globs).
Python 3.9-compatible; no floats in PASS/FAIL logic.

## Context (self-contained)

On the scene K(9,11,13) (33 vertices, 359 edges, 718 directed edges) define on directed edges:
B = Hashimoto (non-backtracking transfer), R = backtrack involution (u→v)↦(v→u). The Bartholdi
identity (verified in float at 5 points, incl. t=0 → Ihara–Bass and t=1 → all-walks side):

```
det(I − u(B + tR)) = (1 − (1−t)²u²)^(|E|−|V|) · det(I − uA + (1−t)(D − (1−t)I)u²)
```

D0 hook: the closure equation p + p² = 1 (p = φ⁻¹) is literally "1 − t = t²", whose unique root in
(0,1) is t = p. At this golden point the identity reads
`det(I − u(B+pR)) = (1 − p⁴u²)^326 · det(I − uA + p²(D − p²I)u²)` — the vertex-side backtrack
correction carries exactly the typed channel weight p². The T1 addendum's revised claim is a
two-completion situation {t=0, t=p}; this task supplies the calculation legs for both.

## Steps

1. **Source the exact theorem.** Bartholdi 1999 ("Counting paths in graphs", Enseign. Math. 45) and
   Mizuno–Sato (J. Combin. Theory Ser. B / Linear Algebra Appl. treatments). Record: exact statement
   and conventions (how bumps are counted, cyclic-word conventions, any md≥2 or connectivity
   hypotheses), and whether the formula above matches their normalization verbatim. If the published
   form differs (sign/shift of t), document the dictionary precisely — the cert must implement the
   PUBLISHED form and show it equals the form above under the dictionary.
   **1b. Source the intertwining maps (feeds Addendum 2).** Bass's block-matrix proof of the identity
   works over the space ℂ^V ⊕ ℂ^E with explicit start/end (source/target) maps between the edge and
   vertex carriers. Extract those maps explicitly (as matrices on K(9,11,13) conventions), and record
   any published vertex-weighted / edge-weighted generalizations (Mizuno–Sato weighted Bartholdi;
   Watanabe–Fukumizu graph-zeta/belief-propagation form) — these are the candidates for upgrading the
   det-level identities to conditional-expectation-level intertwiners Ξ_N (see
   `T1_FORCING_MEMO_ADDENDUM_2.md` §4.1).
   **1c. Verify the t=1 collapse exactly.** Add to the cert: det(I − u(B+R)) = det(I − uA) at ≥3
   rational u (exact/modular) — the E≡W spectral identity of Addendum 2 §2 (float-verified; needs the
   exact leg).
2. **Exact two-variable verification over ℚ.** Cert `vp_scene_bartholdi_typed.py`: verify the
   identity at ≥6 rational pairs (u,t) spanning interior + both degenerations (t=0 must reproduce
   W1's Ihara–Bass numbers; t=1 must reproduce the all-walks vertex side det(I−uA)·(1−0·…) — check
   the exponent factor degenerates correctly). Determinants: multi-prime modular (≥3 primes ≥ 10⁹,
   CRT-consistency) or fraction-free Bareiss, as in W1.
3. **Exact golden-point verification over ℚ(φ).** Represent ℚ(φ) as pairs (a+bφ) with
   φ² = φ+1; implement exact 2-component arithmetic (or ℤ[x]/(x²−x−1) with rational coefficients).
   Verify: (i) 1−t = t² exactly at t = φ−1 (= φ⁻¹); (ii) the golden specialization at ≥3 rational u.
   For determinants over ℚ(φ), either do Bareiss over the quadratic field or verify under BOTH real
   embeddings φ ↦ (1±√5)/2 via modular arithmetic in ℚ(√5)-split primes (p ≡ ±1 mod 5, where x²−x−1
   factors) — document the method.
4. **Negative controls (reachable):** (i) wrong bump matrix (R with one transposition corrupted) —
   FAIL; (ii) wrong exponent |E|−|V|±1 — FAIL; (iii) non-golden t claimed as golden (t = 3/5:
   1−t ≠ t²) — the golden-structure check must FAIL while the generic identity still PASSes (this
   control separates the identity from the specialization); (iv) K(9,11,15) — invariants shift, cert
   detects.
5. **Spectral/structural report (report-only, no promotion):**
   a. Char poly of B_p = B + pR over ℚ(φ): at minimum its restriction to the rank-relevant part;
      numerically Perron(B_p) ≈ 21.4540 — pin it exactly if feasible (it satisfies an algebraic
      equation over ℚ(φ); try the tripartite-quotient reduction that worked for A: zone symmetry
      should compress B_p to a small exact block — document the compressed block and its charpoly).
   b. The golden vertex-side polynomial P(u) = det(I − uA + p²(D − p²I)u²) as an exact element of
      ℚ(φ)[u] via the zone quotient (3×3 or small block): report its coefficients and factorization.
   c. Comparison table against owned invariants — 359/160 (archive window), λ³−359λ−2574 (adjacency
      cubic), 718/33, Perron values — mark every hit/miss plainly; NO interpretation beyond the table.
6. **Report** `TASK_W7_REPORT.md`: sourcing verdict (published form + dictionary), cert results and
   runtimes, negative-control matrix, the exact golden polynomial data, comparison table, and a
   skeptic's paragraph: the strongest reason the golden point t = p is NOT the forced typing (e.g.
   if the published bump convention makes t = p unnatural, say so bluntly).

## Acceptance criteria

- Cert deterministic, PASS on scene, every negative control demonstrably FAILs; exit non-zero on FAIL.
- ℚ(φ) arithmetic exact (2-component or split-prime modular); no floats in decisions.
- The t=0 leg reproduces W1's numbers bit-for-bit where they overlap.
- Report separates: SOURCED / PROVED-HERE (computation) / REPORT-ONLY (comparisons) / OPEN.
- No language of promotion ("forced", "derived", "confirmed") outside quoted context; no edits
  outside `_TASKS_CENTER_ATTACK/`.
