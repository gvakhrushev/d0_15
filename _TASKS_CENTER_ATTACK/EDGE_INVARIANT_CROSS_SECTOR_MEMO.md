# EDGE-INVARIANT-CROSS-SECTOR — 359 = e2 = |E|: one owned invariant, five registered consumer chains (DRAFT, pre-skeptic)

**Status:** DRAFT candidate; no registry row edited. Pre-flight run: `CROSS-SECTOR`, `359`,
`edge count` — precedent found and imitated, not duplicated: `D0-XI5-CROSS-SECTOR-001` (COR row
type, cert `vp_xi5_cross_sector.py`); nearest in-print neighbour found and cross-referenced, not
absorbed: the BOOK_07:1789 Iter27-CAP capacity clause (five-face roster of `C_total = 718 = 2|E|`
WITHIN the capacity narrative, with its mandatory structural-vs-scene-specific clause). 40 registry
rows mention 359; none is a cross-sector consumer row.

## Claim X (DEF-0.2.2 form)

X: the integer `359`, owned once as the edge count `|E(K(9,11,13))| = e2(9,11,13)` (second
elementary symmetric function of the zone sizes), is the SAME owned object consumed by five
independently registered sector chains:

1. **gravity/spectral action** — discrete EH action proxy `= 359 = |E|`, and `a0 = 718 = 2E`
   (`D0-SCENE-SPECTRAL-ACTION-001`, Lean `eh_proxy_is_edge_count`, mechanism: off-diagonal −1
   squares are edge indicators);
2. **alpha** — `alpha_top^-1 = 359*phi^-2 − phi^-5` with the coefficient `= zeta_E(0) = |E|`
   (`D0-EDGE-ALPHA-001`, Lean `D0.Spectral.ZetaResidueAlpha.zetaEdge_neg_one`);
3. **metric/signature** — the rank-3 zone-quotient cubic `lambda^3 − 359*lambda − 2574` has
   `e2 = −359 = −|E|` as its linear coefficient (`D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001`,
   `pairwise_is_edgecount`); its positive discriminant carries the (1+,2−) signature reading;
4. **matter** — the SAME cubic's rational-root emptiness / irreducibility is what forbids Yukawa
   degeneracy (`D0-YUKAWA-COMMUTANT-SPECTRUM-001` `qq_spectrum_splits`, minted this session;
   charpoly owner `D0-SCENE-JOINT-COMMUTANT-SIX-001`);
5. **cosmology** — the VALUE-OWNED phason window scales (BOOK_08 Iter23: `lambda_c, lambda_r` are
   the nontrivial normalized-Laplacian eigenvalues) satisfy `lambda_c*lambda_r = 359/160 = |E|/160`
   with `160 = prod(deg)/(2V)` (`D0-PHASON-WZ-LOGDET-WINDOW-OWNER-001` + the S_DE window of
   `D0-PHASON-PRESSURE-ENERGY-MAXIMALITY-NOGO-001`).

Grade claimed: **COR** (cross-sector correlation of consumers of one invariant), exactly the
`D0-XI5-CROSS-SECTOR-001` row type. NOT claimed: any intertwiner, any identification beyond the
shared object, exhaustiveness of the consumer list.

## Owned pre-facts (verbatim, file:line)

- `D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001` note (CLAIM_TO_LEAN_MAP.csv): "e2 = -359 = -|E|
  (pairwise_is_edgecount: sum of pairwise zone products = 9*11+9*13+11*13 = 359) and e3 = 2574 =
  2*(9*11*13)".
- `D0-EDGE-ALPHA-001` note: "The edge-alpha trace identity zeta_E(-1)=359*phi^-2-phi^-5=alpha_top^-1
  is machine-checked in D0.Spectral.ZetaResidueAlpha.zetaEdge_neg_one".
- `09_LEAN_FORMALIZATION/D0/Synthesis/SceneSpectralAction.lean:173`:
  `theorem eh_proxy_is_edge_count : discreteEHActionProxy Lr ρ1 = 359`; :28-29: "the scene
  Laplacian's off-diagonal entries are −1 exactly on edges, so their squares are edge indicators".
- `D0-SDE-CUBIC-SPECTRAL-DISJOINTNESS-001` note: "P=160x^2-480x+359 and rank-3 scene polynomial
  Q=x^3-359x-2574 have the explicit integral Bezout certificate A*P+B*Q=39590739579959 with nonzero
  resultant … no nonzero intertwiner."
- `D0-PHASON-PRESSURE-ENERGY-MAXIMALITY-NOGO-001` note: "No trace/det coincidence is an
  intertwiner."
- `01_BOOKS/BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md:1420` (Iter23): "The two window scales
  `λ_c, λ_r` … are no longer representative domain-check numbers: they are owned **exactly** as the
  two nontrivial eigenvalues of the **normalized graph Laplacian** … of the scene `K(9,11,13)`".
- `01_BOOKS/BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md:1789` (Iter27-CAP, REQUIRED clause carried
  verbatim): "**the identity is structural while the VALUE 718 is scene-specific** — `gap = 2|E|`
  and `Tr L = Σ deg` hold on any finite graph (… the mutation K(9,11,15) moves all faces
  together)".
- Precedent row `D0-XI5-CROSS-SECTOR-001` note: "Cross-sector correlation (COR), not a new
  derivation; control: phi^-4/phi^-6 != the alpha seam."

## The forcing / construction (every constant computed, exact)

`05_CERTS/vp_edge_invariant_cross_sector.py` rebuilds each face from its OWN sector definition,
independently: |E| counted from the 33x33 adjacency; a0 = Tr L and EH proxy = off-diagonal square
count from the matrix; alpha_top^-1 in exact Z[phi] pairs; the secular cubic by exact 3x3
determinant expansion of `Q = 1 n^T − diag n`; the 24-divisor x 2-sign rational-root sweep; the
normalized-Laplacian zone-quotient charpoly `x(x^2 − 3x + 359/160)` in exact fractions; the
Sylvester resultant of (P,Q) by fraction-free Bareiss elimination, reproducing the minted Bezout
value `39590739579959` from an independent construction.

## Verification

`vp_edge_invariant_cross_sector.py` — 6/6 PASS faces; negative controls (each can fail the
CONCLUSION): `FAIL_LOCKSTEP_RIVAL` (K(9,11,15): every face moves to e2 = 399 together — breaks if
any face tracked a different invariant), `FAIL_WRONG_INVARIANT` (e1 = 33, e3 = 1287, a2-remainder
15708, window 160 all differ from |E| — only e2 is shared; a2 consumes it only through its 2|E|
part), `FAIL_NO_INTERTWINER` (resultant(P,Q) ≠ 0, exact match to the minted certificate).
Mutation-tested: zone-size, window-denominator, resultant-value and P-coefficient mutants all
killed. One non-informative mutation recorded honestly: transposing the random-walk quotient
denominator produces a SIMILAR matrix (same spectrum), so it cannot fail the conclusion — not a
control.

## Named risks & PRE-REGISTERED attack surface (strongest first)

- **ATT-A (strongest self-attack, trap (d): number-coincidence-as-construction).** "Five numbers
  equal 359" is numerology unless the faces consume ONE object. Defense: each face's 359 is rebuilt
  from that sector's own registered definition; the lockstep control shows the shared object is the
  symmetric function e2, structurally; the row claims COR grade only, never a mechanism. A kill
  here must name a face whose 359 is NOT the edge count under its own registered definition.
- **ATT-B (trap (n)/(1): universal over unexhausted class).** "Five consumers" must not read as
  "exactly five". The row text enumerates REGISTERED chains and states non-exhaustiveness (40 rows
  mention 359). A kill naming a sixth consumer strengthens, not kills.
- **ATT-C (carrier mismatch).** The alpha face's 359 is the EDGE zeta at 0; the gravity face is the
  Laplacian ladder; both literally count E(K(9,11,13)) — typing verified in the two Lean modules.
  The cosmology face's carrier is the normalized (not raw) Laplacian: only the PRODUCT of its
  nontrivial eigenvalues consumes |E| (times 1/160); the raw-vs-normalized distinction is stated.
- **ATT-D (duplication, §05.8.U).** BOOK_07:1789 already records a five-face roster of 718 = 2|E|
  WITHIN the capacity narrative. This row is the cross-SECTOR consumer registry of e2 = 359 (alpha
  chain, metric/Yukawa chain, phason chain are not in 1789's roster) and cross-references the
  capacity clause rather than absorbing it. A kill here must show a single existing row already
  NAMING the cross-sector consumer list.
- **ATT-E (intertwiner ceiling).** Two owned no-gos cap the reading: the Bezout no-intertwiner
  certificate and "no trace/det coincidence is an intertwiner". The row carries both as its
  ceiling. Any future upgrade claim must go THROUGH those no-gos, not around them.

## What this does NOT show

No mechanism, no derivation of any face from any other, no intertwiner between the polynomial
carriers, no continuum Einstein-Hilbert promotion (scope guard of the spectral-action domain), no
claim that the consumer list is complete, and no upgrade of the alpha dressing obligations (the
depth sub-leg of `D0-ALPHA-SEAM-FORM-FORCED-001` is untouched — this row lives entirely at the
`alpha_top` level, which is already CORE-FORMALIZED).
