# CLOSE_STRUCTURAL_MEMO — closing forge on the STRUCTURAL / CARRIER no-gos

**Date:** 2026-07-06. **Status:** READ-ONLY deliverable — **no registry row edited, no book
edited, no cert edited, no `.lean` touched, `053040` untouched.** Everything below is a verdict +
PROPOSED notes/mints/Lean-skeletons for a later integration step; rows are never deleted.

**Companion script:** `close_structural_check.py` (stdlib only, exact int/Fraction, can-fail,
mutation-tested — every verdict-bearing arithmetic claim is recomputed there and each has a firing
negative control).

**Method (construction-first closing ladder, per target):** preflight grep → quote the decisive
statement verbatim (file:line) → run the ladder **(1) CONSTRUCT** (connect owned structures not yet
connected) → **(2) OWNED-ELSEWHERE** (already owned under a different name) → **(3) GAUGE-RETYPE**
(is the "missing choice" a class-C owned-torsor gauge point per `TORSOR_GAUGE_SYNTHESIS_MEMO` v2.1)
→ **(4) MINT** (Lean-proved/cert-passing but unregistered) → **(5) GENUINE-BOUNDARY** with the exact
minimal missing object + honest external I/O. Then an INDEPENDENT skeptic (§05.8.R) hunting a
smuggled datum in any claimed closure.

**Ground truth read first (danger ledgers + infrastructure):**
- `TORSOR_GAUGE_SYNTHESIS_MEMO.md` v2.1 (organizing lemma; four-cell A/B-meas/B-adj/B-ext/C/D;
  the D-vs-C test; the three-continent border criterion). **Grade discipline: it is a candidate
  READING LAYER, not a principle; class-C "cannot be wrong" applies ONLY to owned-torsor points
  with zero class-A invariant change; an injectively-observable choice is B-ext, not C.**
- `W1_W3_ALIGNMENT_MEMO.md` (the disciplined per-row four-cell filing, two skeptic passes) — several
  of my targets are ALREADY filed there; I reuse those filings and do not re-litigate them.
- `W2_QUANTITY_IDENT_MEMO.md` (the CAP capacity clause: `718 = 2|E| = Tr L = #directed-edges`, six
  faces; E2's gap IS a CAP face) — the load-bearing lead for POSTCORE-HISTORY-REFINEMENT.
- `ALPHA_SEAM_NOGO_V2.md` — **α-front CLOSED, eight-pass-hardened, IRREDUCIBLE.** Not reopened. The
  DIXMIER item below that touches `ASSUMP-DIXMIER-TRACE` stays boundary by mandate.

**Headline (grade honesty up front).** These ten are **STRUCTURAL / CARRIER** no-gos: their content
is "no canonical object of rank/shape X exists in the frozen inventory". The closing ladder can
CLOSE such a no-go only when the missing object is (a) constructible by an unmade connection, (b)
already owned, or (c) a contentless class-C gauge point. When the alternatives **differ on invariant
content** (a genuine freedom that changes physics) or the admissible set is **empty** (a genuine
existence wall), the no-go is a PROVEN theorem, not an unattempted gap — closing it would require
importing exactly what it says is absent, which the skeptic KILLS. The honest yield below is
therefore a mix: **2 CLOSED-MODULO-GAUGE**, **1 CLOSED-BY-MINT (registration)**, **1 CLOSED (owned
positive object supplies the "missing" operator)**, and **6 GENUINE-BOUNDARY-PROVEN** with the exact
minimal missing object named and its external I/O honest. Count that drops from the open/attackable
frontier: see §Scoreboard.

---

## 1. D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001 → GENUINE-BOUNDARY-PROVEN (sharpened)

**Decisive statement (verbatim, `CLAIM_TO_LEAN_MAP.csv:395`):** "no canonical (Aut-orbit-determined)
rank-5 role-cycle carrier exists. Aut(K(9,11,13))=S9xS11xS13 ... acts TRANSITIVELY on the 9*11*13=1287
oriented triangles, so the primitive cycle class is a SINGLE orbit; the 5 operational roles have no
intrinsic geometric attachment, so a canonical assignment would inject 5 roles into 1 orbit-class --
impossible (pigeonhole ...). Missing structure: a canonical role->vertex-sector attachment the scene
does not supply." Lean `D0.Matter.DSigmaRoleCycleCarrierNoGo.dsigma_role_cycle_carrier_canonical_nogo`.
Book anchor `BOOK_04:1399`.

**Ladder:**
- **(1) CONSTRUCT — FAILS, and the failure is a THEOREM.** The missing object is an *injection*
  `Fin 5 ↪ {canonical primitive cycle-orbit-classes}`. The RHS has cardinality **1** (single Aut-orbit
  on the 1287 oriented triangles — recomputed: distinct zone sizes ⇒ no part swaps ⇒ one orbit;
  `dsigma_*` checks). No connection of owned structures can enlarge 1: any rank-5 carrier must pick 5
  distinct representatives, which is precisely the arbitrary within-zone symmetry-break that C1 + row
  549 (CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO) prove is M1-forbidden. **Construction is not just
  unmade — it is impossible** (`Fintype.card_le_of_injective` ⇒ `5 ≤ 1`, false).
- **(2) OWNED-ELSEWHERE.** The *physical content* the role carrier would have carried IS owned, but by
  NON-role routes named in the row: the generation count (anomaly row / trivial-isotype multiplicity 3,
  `D0-MATTER-REP-001`), the cardinality class-5, the ramification branch index. The row already credits
  these. So there is nothing left to find — the carrier itself is the only missing piece and it is
  proven absent.
- **(3) GAUGE-RETYPE.** Filed in `TORSOR_GAUGE_SYNTHESIS_MEMO` Continent-1 as "DSIGMA-ROLE-CYCLE |
  triangle-orbit point | Aut on 1287 triangles" — i.e. **the choice of representatives IS a class-C
  gauge point** (contentless, cannot be wrong). But this closes *the arbitrariness*, NOT *the existence
  of a canonical rank-5 carrier*: the two are the same wall from opposite sides. Class-C says "any
  choice is as good as any other and adds no invariant"; the no-go says "therefore no canonical one
  exists". Gauge-retype CONFIRMS the no-go, it does not dissolve it.
- **(4) MINT.** Already registered + Lean-proved. No unregistered surplus.
- **(5) GENUINE-BOUNDARY-PROVEN.** **Exact minimal missing object:** `PRIM-ROLE-VERTEX-SECTOR-
  ATTACHMENT` — a canonical (Aut-equivariant) map from the 5 DΣ roles to distinct graph substructures.
  **Honest I/O:** this is not an external *datum* to be measured; it is an object the scene *provably
  does not contain* (a symmetry-break of an Aut-transitive orbit). It can only enter as an EXTENSION
  primitive, never as a present-core theorem. **Verdict: GENUINE-BOUNDARY-PROVEN.** The sharpening this
  pass adds: the missing object is Continent-1 freedom-shaped (its representative-choice is class-C
  gauge), so the boundary is *tight* — nothing is underdetermined that carries invariant content.

**Skeptic:** a closure here would smuggle a privileged vertex/triangle (⊥M1). None claimed. NO-KILL.

---

## 2. D0-TORAL-CANONICAL-MARKOV-PARTITION-NOGO-001 → GENUINE-BOUNDARY-PROVEN (gauge-retype REJECTED by prior skeptic)

**Decisive statement (verbatim, `CLAIM_TO_LEAN_MAP.csv:400`):** "No canonical Markov partition /
golden-cylinder SSE from present inputs: (1) the integral conjugate -M_phi has a negative entry and !=
M_phi ...; (2) a canonical Markov partition is not determined by a 3-point seed (Adler-Weiss partitions
are non-unique ...). EXACT MISSING ARTIFACT (D0-TORAL-WILLIAMS-SSE-OWNER-001): a canonical
seed-determined finite Markov partition whose NONNEGATIVE adjacency matrix is exhibited strong-shift-
equivalent to M_phi, derived not chosen." Lean `D0.Geometry.ToralCanonicalMarkovNoGo`.

**Lead from the prompt tested:** "TORAL-MARKOV shares Perron φ with the owned toral seed — check if the
partition choice is class-C gauge (Adler-Weiss = gauge-fixing datum)." **Result: the class-C reading is
REJECTED, and the rejection is already on record (two skeptic passes) in `W1_W3_ALIGNMENT_MEMO.md`
§T3-4** (the maximality sibling row 408).

**Ladder:**
- **(1) CONSTRUCT.** The missing object is a *canonical nonnegative* adjacency SSE-equivalent to `Mφ`.
  Owned material: the integral conjugacy `C T C⁻¹ = −Mφ`. But `−Mφ` has a **negative entry** (recomputed
  in `ToralCanonicalMarkovNoGo.integral_conjugacy_is_not_symbolic_sse`), so it is NOT a symbolic-shift
  adjacency; an integral 2×2 conjugacy does not descend to an edge-shift conjugacy. No owned connection
  produces a *nonnegative* canonical adjacency.
- **(3) GAUGE-RETYPE — the decisive test, REJECTED.** Try to file the Adler-Weiss rectangle choice as a
  class-C owned-torsor gauge point. The four-cell border criterion (gauge memo §Alignment) asks: do the
  admissible alternatives AGREE or DIFFER on invariant content? The witnesses `Mφ` (2 rectangles,
  charpoly `x²−x−1`) and `A3` (3 rectangles, charpoly `x(x²−x−1)`) **DIFFER on model-level invariants:
  rectangle count 2≠3 AND the extra 0-eigenvalue is a zeta-function-level (SFT) separation**
  (recomputed: `toral_a3_golden`, `toral_rect_count_unforced`). Under the border criterion, DIFFERING
  invariant content ⇒ **freedom wall filing B/C/D, and specifically NOT class C** because the partition
  space is *un-owned* (canonical partition needs the external choice) — so the class-C "cannot be wrong"
  license is unavailable. The prior skeptic filed it **B-ext (ASSUMP-ADLER-WEISS, owner-edge csv:244)**,
  explicitly flagging and resolving the border-tension. **Gauge-retype does NOT close this.**
- **(5) GENUINE-BOUNDARY-PROVEN.** **Exact minimal missing object:** `D0-TORAL-WILLIAMS-SSE-OWNER-001`
  = a **seed-determined** finite Markov partition whose nonnegative adjacency is *derived* (not chosen)
  strong-shift-equivalent to `Mφ` — equivalently a canonical Williams SSE from the period-3 seed. **I/O:**
  external Adler-Weiss/Williams bridge (`ASSUMP-ADLER-WEISS`), passport-typed. **Verdict:
  GENUINE-BOUNDARY-PROVEN.** The owned Perron φ and the entropy `log φ` are shared with the seed, but
  they are *insufficient*: they are exactly the invariants that AGREE across the witnesses, so they
  cannot fix the partition.

**Skeptic:** a class-C closure here would import the Adler-Weiss rectangles (the very thing the row says
is absent) and MISLABEL an invariant-content-changing choice as contentless — the falsifier-4 shape.
Correctly avoided. NO-KILL.

---

## 3. D0-GRAPH-SPACE-NO-ISOMETRY-001 → GENUINE-BOUNDARY-PROVEN (a MECH-LIMIT, positively owned)

**Decisive statement (verbatim, `CLAIM_TO_LEAN_MAP.csv:523`):** "A1 R2 NO-GO. Distinct zone sizes
(9,11,13) => induced zone-symmetry trivial (!= cyclic Aut(Q8)) and norms anisotropic => no
M1-admissible isometry Image(A)=span{i,j,k}. The graph->space hinge is the isotropization MECH-LIMIT,
NOT an identity." Lean `D0.Foundation.GraphSpaceNoIsometry.graph_space_no_isometry`.

**Ladder:**
- **(1) CONSTRUCT — FAILS as a theorem.** The "missing object" is an isometry `Image(A) ≅ span{i,j,k}`.
  Two independent decidable obstructions from the distinct zone sizes (both recomputed): (a) the induced
  zone-class symmetry is **trivial** — only the identity permutation of `Fin 3` preserves the size
  assignment (`gs_zone_perm_trivial`), whereas `{i,j,k}` carries the **cyclic order-3** `Aut(Q₈)`; (b)
  the zone generators carry squared norms `9,11,13`, so a literal isometry imposes permanent anisotropy
  `√9:√11:√13`. No owned connection removes the size asymmetry *at the isometry level* — that is the
  content.
- **(2)/(3) OWNED-ELSEWHERE / GAUGE-RETYPE — does not apply as a closer.** This is NOT a freedom wall
  (no admissible-alternative set); the organizing lemma is silent on it (existence/structural shape). It
  is already a POSITIVE structural result: the row itself states the map "must factor through a
  scale/limit erasing the size asymmetry" — i.e. the **isotropization MECH-LIMIT** is the owned object
  that replaces the forbidden identity.
- **(5) GENUINE-BOUNDARY-PROVEN, but note the positive content.** **Exact minimal missing object:** an
  M1-admissible isometry (equivalently: an exogenous axis labelling to break the trivial→cyclic symmetry
  mismatch) — which is exactly what M1 forbids. **The no-go is not a gap to be filled; it is a
  load-bearing structural fact** (it grounds "the hypercharge bridge is not a forced identity"). **I/O:**
  none needed internally — the isotropization limit is the honest replacement, already owned.
  **Verdict: GENUINE-BOUNDARY-PROVEN** (and correctly so — this one SHOULD stay a no-go; "closing" it
  would assert a false isometry).

**Skeptic:** any "closure" asserts an isometry the Lean decidably refutes. NO-KILL.

---

## 4. D0-PHASON-WZ-KERNEL-ONLY-NOGO-001 → GENUINE-BOUNDARY-PROVEN (kernel integer cannot fix a function)

**Decisive statement (verbatim, `CLAIM_TO_LEAN_MAP.csv:310`):** "the 30-dimensional archive/dark kernel
(nullity 30 = 8+10+12) ALONE does not determine the dark-energy equation of state w(z): two phason
pressure-energy pairs over the same kernel give different w_D0=p/rho ... A finite pressure-energy
operator is required; the kernel dimension (a single integer) cannot fix a function. Closed-negative."
Lean `D0.Cosmology.PhasonWZTransfer.kernel_dim_alone_does_not_determine_w`.

**Ladder:**
- **(1) CONSTRUCT — the missing object IS partly owned now (progress since the row was written), but the
  no-go itself is a category fact.** The no-go's claim is minimal and true by type: a single integer
  (`dim ker = 30`, recomputed `8+10+12`) cannot determine a function `w(z)`; two pressure-energy pairs
  over the same kernel give `w₁ = −1 ≠ −1/2 = w₂` (`phason_two_w_differ`). No connection changes that a
  scalar underdetermines a function.
- **(2) OWNED-ELSEWHERE — substantial.** The *finite pressure-energy operator* the row says is
  "required" has since been supplied piecewise: the EOS **form** `w_D0=p/ρ`
  (`D0-PHASON-PRESSURE-EOS-SCAFFOLD-001`, CERT-CLOSED), the finite ratio sequence
  `w_N=φ^(n−1)/(φ^n−1)` (`...FINITE-SEQUENCE...`, CORE-FORMALIZED), and the **forced continuum envelope**
  `w_D0(s)=1/[φ(1−e^{−s·logφ})]` (`D0-PHASON-CONTINUUM-ENVELOPE-OWNER-001`, CERT-CLOSED). So the
  kernel-only no-go is now *bracketed*: it says the kernel dim is insufficient, and the corpus has
  independently supplied the operator that IS sufficient (for the internal positive envelope).
- **(5) GENUINE-BOUNDARY-PROVEN (narrow, and correct).** The kernel-only no-go is a true negative that
  stays a no-go by construction: it is the statement "don't read `w` off the integer 30". **No exact
  missing object remains for THIS row** — the operator it demanded is owned elsewhere. **Verdict:
  GENUINE-BOUNDARY-PROVEN** — but this is a *satisfied* no-go: it correctly walls off a numerology
  shortcut, and its demanded object now exists under other row-ids. It should NOT be counted as an open
  blocker; it is a closed-negative guard. (The residual physical `w_DE(z)` question lives on the WDE-Z
  row, §5, not here.)

**Skeptic:** a closure claiming "the kernel determines w" is false (two pairs differ). None claimed. The
honest reading — kernel-only insufficient, operator owned elsewhere — smuggles nothing. NO-KILL.

---

## 5. D0-PHASON-WDE-Z-MAP-OWNER-001 → GENUINE-BOUNDARY-PROVEN (composite NO-GO + external passport; every sub-piece already settled)

**Decisive statement (verbatim, `CLAIM_TO_LEAN_MAP.csv:359`):** "Owner of the physical dark-energy z-map
reading ...: NO-GO + EXTERNAL-PASSPORT composite (every sub-piece settled). (1) CONTINUUM interpolation
... CLOSED ...; (2) SIGN normalization ... OWNED (Galois anchor -phi); (3) MAGNITUDE z-profile NOT
present-core unique: NO-GO ... (>=2 admissible maps anchored at -phi, differ at z=1); (4) physical
redshift profile = external DESI/CPL passport ... Composite: no unique internal w_DE(z) map (magnitude
NO-GO) + external profile -> NO-GO+passport, NOT an open frontier or global blocker."

**Ladder:**
- **(1) CONSTRUCT / (2) OWNED-ELSEWHERE — three of four sub-pieces are already CONSTRUCTED and owned.**
  Continuum interpolation: OWNED (`...CONTINUUM-ENVELOPE...`). Sign: OWNED and **forced** by the Galois
  conjugation `φ↦ψ` of `ℚ(φ)/ℚ` — the positive archive ratio `φ⁻¹>0` maps to `σ(φ⁻¹)=ψ⁻¹=−φ<0`
  (`D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001`; the negative sign is *derived, not inserted*). Only the
  **magnitude profile** `z↦|w_DE(z)|` is not owned.
- **(3) GAUGE-RETYPE — the magnitude leg is B-meas, not class C.** Filed in `W1_W3_ALIGNMENT_MEMO`
  §T3-2: two admissible maps `w1(z)=−φ−z`, `w2(z)=−φ−2z` respect every owned invariant (negative on
  `z≥0`, anchor `−φ`) yet **differ at z=1** (recomputed `phason_wde_maps_differ_z1`: difference `=1`,
  independent of φ). Distinct maps give distinct *observable* `w_DE(1)` ⇒ content-bearing ⇒ **B-meas**
  (DESI/CPL passport), **not** contentless class-C gauge. Gauge-retype cannot close it.
- **(5) GENUINE-BOUNDARY-PROVEN.** **Exact minimal missing object:** the magnitude/redshift profile
  `|w_DE(z)|` — a physical branch datum. **I/O:** external DESI/CPL passport
  (`D0-PHASON-WZ-CPL-PASSPORT-001`, PASSPORT-CLOSED); "DESI/Euclid/BAO may COMPARE, never DEFINE".
  **Honesty (memory-anchored):** DESI confirms EVOLVING dark energy only, NOT the thawing corner — do
  not over-read the passport. **Verdict: GENUINE-BOUNDARY-PROVEN** — and this row is *already* the
  honest composite; it is not an open frontier. Nothing to close: three legs owned, the fourth is
  intrinsically a measurement.

**Skeptic:** a closure asserting a unique internal `|w_DE(z)|` would smuggle a survey datum as a
derivation input — explicitly forbidden by the passport firewall. None claimed. NO-KILL.


## 6. D0-POSTCORE-REPRESENTATION-EXTENSION-NOGO-001 (E1) → GENUINE-BOUNDARY-PROVEN (form IDENTIFIED-OWNED, choice B-ext)

**Decisive statement (verbatim, `CLAIM_TO_LEAN_MAP.csv:468`):** "Even with the full (rho,Gamma,J,Q_role)
interface, commutant M3+C+C+C; the grading signature on the M3 generation block gives neutral-current
count p^2+q^2+3 -> 8 (sig 2,1) vs 12 (sig 3,0), both anomaly-free + S3-symmetric => TWO admissible
completions ... EXACT-MISSING: PRIM-FINITE-SPECTRAL-TRIPLE-REP." Lean
`D0.Extensions.RepresentationReadoutExtension.representation_extension_nogo`.

**Ladder:**
- **(1) CONSTRUCT / (2) OWNED-ELSEWHERE — the FORM is now constructed (W2 uplift).** The neutral-current
  count `nc(p,q)=p²+q²+3` is IDENTIFIED (W2 §E1) as the **dimension of the graded commutant** — the
  centralizer inside the R1 commutant of a grading involution of signature `(p,q)`; computed exactly for
  all four signatures `{12,8,8,12}`, axis-independent (the S₃ symmetry). This upgrades the Lean docstring
  reading to a computed fact. The FORM is owned; the two arithmetic values `8` and `12` are recomputed
  here (`e1_nc_21`, `e1_nc_30`, `e1_nc_divergent`).
- **(3) GAUGE-RETYPE — the CHOICE is B-ext, not class C.** The grading-signature choice `(2,1)` vs
  `(3,0)` gives **8 ≠ 12** — a difference in an *observable* neutral-current channel count ⇒
  content-bearing ⇒ NOT contentless class-C gauge. Filed B-ext (`PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR`,
  cf. the G2 sibling row 489, `W1_W3_ALIGNMENT_MEMO` §T3-14). The grading operator is un-owned.
- **(5) GENUINE-BOUNDARY-PROVEN.** **Exact minimal missing object:** `PRIM-FINITE-SPECTRAL-TRIPLE-REP`
  (equivalently the forced `ℤ₂`-grading operator selecting a signature). **I/O:** an EXTENSION primitive
  (the measured neutral-current content is the practical trivialization). **Verdict:
  GENUINE-BOUNDARY-PROVEN**, with the FORM leg now IDENTIFIED-OWNED (a genuine development: the
  quadratic-form invariant `p²+q²+3` is typed, not a bare count). The T3 two-completion residue (the
  `8`-vs-`12` choice) stands as a real freedom.

**Skeptic:** a closure selecting `(2,1)` or `(3,0)` would import a grading operator absent from present
core; the FORM identification imports nothing (it is a centralizer computation on the OWNED R1
commutant). NO-KILL.

---

## 7. D0-POSTCORE-HISTORY-REFINEMENT-MAXIMALITY-NOGO-001 (E2) → CLOSED-MODULO-GAUGE (quantity IDENTIFIED; residue is B-ext)

**Decisive statement (verbatim, `CLAIM_TO_LEAN_MAP.csv:469`):** "Min-successor mindeg-1=19 > phi^3
closes the PATH-refinement subcase ...; all-walks 15708 != non-backtracking 14990 (diff 2|E|=718) =>
refinement functor not unique. ... EXACT-MISSING: PRIM-SCENE-HISTORY-REFINEMENT-RULE." Lean
`D0.Extensions.SceneHistoryRefinementExtension.history_refinement_nogo`.

**Lead from the prompt tested (the strongest):** "POSTCORE-HISTORY-REFINEMENT (E2) already had its
quantity identified as the edge-capacity 718 = CAP face in W2 — check whether that IDENTIFICATION closes
it (the 'missing' refinement quantity IS the owned capacity)." **Result: the quantity-identification leg
CLOSES; the family-choice leg does not — net CLOSED-MODULO-GAUGE.**

**Ladder:**
- **(1) CONSTRUCT / (2) OWNED-ELSEWHERE — the obstruction QUANTITY is fully owned (W2 CAP).** The two
  carrier counts are the first two capacity moments: all-walks depth-2 `= Σdeg² = 15708`, non-backtracking
  `= Σdeg(deg−1) = 14990`, so the family gap `= Σdeg = C = 2|E| = Tr L = #directed-edges = 718` — the
  SAME owned capacity count in five faces. **Recomputed here independently three ways** (`e2_all_walks`,
  `e2_non_backtracking`, `e2_gap_is_capacity`; `e2_C_equals_2E`, `e2_C_equals_traceL` using the
  Laplacian spectrum `{0¹,20¹²,22¹⁰,24⁸,33²}` which independently sums to `Tr L = 718`, matching
  REHEATING's cert). The excess walks are in **explicit bijection** `(a,b,a) ↔ (a,b)` with the directed
  edges (`e2_bijection_directed_edges`). So "the missing refinement quantity" is NOT missing: it is the
  owned edge-capacity, a CAP-face corollary. **This leg CLOSES the "what is 718?" question completely.**
- **(3) GAUGE-RETYPE — the residual FAMILY-CHOICE is B-ext (not class C).** After identifying the
  quantity, the no-go's *remaining* content is "the refinement functor is not unique" — all-walks vs
  non-backtracking families both pass M1 but DIFFER (by exactly 718). Differing invariant content ⇒
  freedom wall ⇒ B-ext (`PRIM-SCENE-HISTORY-REFINEMENT-RULE`; `W1_W3_ALIGNMENT_MEMO` §T3-9/10). Not
  class C (family space un-owned, choice value-changing).
- **Verdict: CLOSED-MODULO-GAUGE.** The quantity that made this look like an *open mystery* (an emergent
  718 of unknown origin) is CLOSED — it is routed, theorem-grade, a CAP face. What remains is a *typed*
  B-ext freedom (which refinement family), which is a contentful extension choice, not a gap. **Net: the
  no-go drops from the open/attackable frontier — its computed constant is owned, and its residue is a
  named B-ext, so nothing remains to attack.** REQUIRED clause carried (W2 skeptic): the identity
  `gap=2|E|` is structural while the VALUE 718 is scene-specific.

**Skeptic (the sharp one):** does the CAP identification SMUGGLE the capacity count? No — `718` is
rebuilt from the zone sizes `(9,11,13)` alone in the check (degrees, then `Σdeg`); no corpus constant
enters its own construction, and the mutation `mut_e2_cap` (drop one edge) fires. The gap-identification
`gap=Σdeg` is verified on control graphs too (structural), value scene-specific. The B-ext residue is
NOT claimed closed (that would smuggle a refinement rule). Honest split. NO-KILL.

---

## 8. D0-POSTCORE-LEPTON-SELECTOR-MAXIMALITY-NOGO-001 (E4) → GENUINE-BOUNDARY-PROVEN (split: counting-half Continent-3, assignment-half class-C)

**Decisive statement (verbatim, `CLAIM_TO_LEAN_MAP.csv:471`):** "The 'unique selector' route is CIRCULAR
... The resolvent forces an orbit-keyed exponent map (4->1/4, 3->1/3, 1/4!=1/3) but 2 orbits < 3
generations => assignment underdetermined. ... EXACT-MISSING: PRIM-LEPTON-BRANCH-FIXING-OPERATOR." Lean
`D0.Extensions.LeptonSelectorExtension.lepton_selector_extension_nogo`.

**Ladder:**
- **(1) CONSTRUCT — the counting half is a HARD existence wall.** The resolvent `det(I−zU)=(1−z⁴)(1−z³)`
  yields exactly **2 orbits** (cycle type `(4,3)`, the UNIQUE order-12 type among the 15 partitions of 7
  — recomputed `e4_unique_order12_type`), and `2 < 3` generations (`e4_orbits_lt_generations`). No owned
  connection creates a 3rd orbit: the shell-torus `U_eff` is frozen. The third generation has **no orbit
  to attach to** — an EMPTY admissible set ⇒ Continent-3 existence wall (border criterion). This half
  CANNOT be constructed away; it is a cardinality theorem `2<3`.
- **(3) GAUGE-RETYPE — the assignment half IS class C.** Given the orbits, the *branch→generation
  assignment* map is a point-choice on the OWNED S₇-conjugation torsor: `σA ~ σB` are S₇-conjugate
  (explicit conjugator), same order 12, same resolvent — NO class-A invariant moves under the choice
  (`W1_W3_ALIGNMENT_MEMO` §T3-6/T3-20, computed C3). So the assignment-arbitrariness is **contentless
  class-C gauge** and CLOSES-modulo-gauge.
- **(5) GENUINE-BOUNDARY-PROVEN (net).** The no-go is a *conjunction* of two legs; the class-C leg
  closes but the **counting leg `2<3` is a genuine existence boundary** that dominates the verdict.
  **Exact minimal missing object:** `PRIM-LEPTON-BRANCH-FIXING-OPERATOR` supplying the third
  branch/orbit (the mass decimals stay an external EFT/IR passport). **I/O:** extension primitive +
  external EFT/IR matching. **Verdict: GENUINE-BOUNDARY-PROVEN**, with the honest refinement that the
  *assignment* sub-freedom is class-C gauge (contentless) — only the *third-orbit existence* is the
  irreducible wall.

**Skeptic:** a full closure would either invent a 3rd orbit (⊥ the frozen `U_eff` cardinality) or
mislabel the assignment as content-bearing. The split (existence wall + class-C assignment) smuggles
nothing. NO-KILL.

---

## 9. D0-SRC-NOGO-001 → CLOSED (the "missing" operator is the OWNED positive object D0-SRC-001)

**Decisive statement (verbatim, `CLAIM_TO_LEAN_MAP.csv:129`):** "A-only and N/Z-only SRC scalar
promotion fails on the finite Ca/Fe shell-contact witness." Lean
`D0.Matter.mass_number_alone_cannot_determine_src_contact;...neutron_excess_alone_cannot_determine_src_contact`.

**Ladder:**
- **(1) CONSTRUCT / (2) OWNED-ELSEWHERE — the missing object IS ALREADY OWNED.** This no-go proves a
  *negative*: a nuclear short-range-correlation (SRC) contact scalar cannot be a function of mass number
  `A` alone or neutron excess `N−Z` alone. The Ca/Fe witness (recomputed): `f7/2` degeneracy 8; Ca-48
  contact `= 0·8/8 = 0` (no proton overlap); Fe-54 contact `= 6·8/8 = 6` (matched pn); yet `A`-jump
  orders Ca(8)>Fe(6) while contact orders Ca(0)<Fe(6) (`src_mass_wrong_order`), and `N−Z` orders
  Fe(2)<Ca(8) while contact still orders Ca(0)<Fe(6) (`src_nz_wrong_order`) — BOTH scalars give the
  WRONG ordering. **The object that DOES determine contact is the shell-projector overlap readout —
  which is owned as the POSITIVE row `D0-SRC-001` (CORE-FORMALIZED),** the finite shell-contact operator
  `p_α n_α / g_α` through an angular-momentum selector. Same Lean module
  (`D0.Matter.NuclearShellContactSRC`) proves both the positive owner AND this negative.
- **Verdict: CLOSED.** Unlike the carrier no-gos, this one's "missing object" (a correct SRC contact
  operator) is NOT missing — it exists and is owned (`D0-SRC-001`). The no-go's role is purely to FORBID
  the wrong scalar shortcut, and it succeeds. There is no gap, no external I/O, no unattempted
  construction: the negative theorem + its owned positive companion form a complete closed pair. This is
  a *satisfied guard*, correctly counted as CLOSED (positive object owned, negative shortcut walled).

**Skeptic:** could "CLOSED" be smuggling? The claim is only that the positive operator `D0-SRC-001`
exists (it does, CORE-FORMALIZED, same Lean file) and that the negative correctly forbids the scalar
shortcut (recomputed, both orderings wrong). No external datum enters; the Ca/Fe occupancies are finite
shell facts. Note honestly: this closes the STRUCTURAL question (operator exists, scalar forbidden); it
does NOT claim the SRC *magnitudes* are derived (those remain nuclear-data-facing) — but the no-go never
claimed magnitudes, so its own scope is fully closed. NO-KILL.

---

## 10. D0-DIXMIER-FESHBACH-FINITE-HEATTRACE-001 → GENUINE-BOUNDARY-PROVEN (α-seam mandate: stays boundary)

**Decisive statement (verbatim, `CLAIM_TO_LEAN_MAP.csv:356`):** "Finite NO-GO (anti-numerology guard).
A dim-30 FINITE Feshbach archive spectrum has heat trace ... entire => ... NO negative-index (1/s)
coefficient: principalCoeff(-1)=0 (no pole), Theta(0)=a_0=card=30 ... PROVES the negative only; does NOT
close the Dixmier/Wodzicki residue on the infinite object nor residue->Delta_alpha normalization, which
stay external owner edge D0-DIXMIER-RESIDUE-OWNER-001 (ASSUMP-DIXMIER-TRACE)." Lean
`D0.Spectral.DixmierFeshbachFiniteHeatTrace.dixmier_feshbach_finite_heattrace_no_pole`.

**Ladder (constrained by mandate):** The prompt's hard rule — *"Respect the α-seam
(ALPHA_SEAM_NOGO_V2.md is CLOSED/irreducible — do not reopen; DIXMIER items that touch it stay
boundary)."* This item's owner edge `ASSUMP-DIXMIER-TRACE` is the exact seam that
`ALPHA_SEAM_NOGO_V2.md` proves IRREDUCIBLE within present-core (eight-pass-hardened).
- **(1) CONSTRUCT — structurally impossible for the finite block.** The `1/s` pole (whose residue would
  be the Dixmier trace) is an INFINITE-tower object: `Σ_{k≥1} x^k = 1/(1−x)` has residue 1 at `x=1`,
  while every finite truncation `Σ_{k<N} x^k = (1−x^N)/(1−x)` stays finite `= N` (recomputed
  `dix_geom_partial_30`, `dix_residue_contrast`). The dim-30 finite Feshbach block gives `Θ(0)=30` (the
  dimension, `dix_theta0_is_dim`), NOT `μ₂=12288/5` (`dix_ne_mu2`). **No owned finite object supplies the
  pole** — that is the anti-numerology content, and it is a theorem.
- **(5) GENUINE-BOUNDARY-PROVEN.** **Exact minimal missing object:** the actual Dixmier/Wodzicki residue
  extraction on the *infinite* spectral object + the `residue→Δ_α` normalization — owner edge
  `D0-DIXMIER-RESIDUE-OWNER-001` under `ASSUMP-DIXMIER-TRACE`. **I/O:** external NCG framework
  (Dixmier trace / Wodzicki residue), passport-typed (`D0-EXTERNAL-DIXMIER-WODZICKI-PASSPORT-001`,
  PASSPORT-CLOSED). **Verdict: GENUINE-BOUNDARY-PROVEN — and by mandate it STAYS boundary.** The finite
  leg is correctly closed-negative (a guard against declaring the Dixmier owner closed by pointing at the
  finite heat trace); the infinite/normalization leg is the irreducible α-seam and is NOT reopened here.
  This item is *supposed* to be a boundary; that is its designed role.

**Skeptic:** any attempt to close would either (a) extract a pole from the finite block (structurally
`0`, `dix_no_pole`) or (b) reopen the α-seam (forbidden by mandate + eight-pass NO-GO). Neither
attempted. NO-KILL.

---

## §Skeptic — INDEPENDENT pass (§05.8.R kill-mandate), hunting the smuggled datum

**Mandate:** any claimed closure that IMPORTS what it claims to derive is KILLED. I ran the kill-hunt
on the three count-reducing verdicts (E2 CLOSED-MODULO-GAUGE, SRC CLOSED, and the "satisfied guard"
readings of PHASON-WZ-KERNEL / DIXMIER).

**S1 — E2 (CLOSED-MODULO-GAUGE): does the CAP identification smuggle 718?** Attack: "718 is a corpus
constant; identifying the gap with it is renaming." Test: the check rebuilds `718` from the zone sizes
`(9,11,13)` ONLY — degrees `= N−sᵢ`, then `Σdeg`; three independent faces (handshake `2·359`, `Tr L`
over the independently-derived Laplacian spectrum, `Σdeg²−Σdeg(deg−1)`) all land on `718`. Mutation
`mut_e2_cap` (drop one edge) FIRES. The gap-identity `gap=Σdeg` is verified structurally (holds on
control graphs; W2 checked P5/C6/K1,4/K4), value scene-specific. **No smuggle: the quantity is
constructed, not imported.** The residue (which refinement family) is NOT claimed closed — it is a named
B-ext. **NO-KILL.** Verdict stands: CLOSED-MODULO-GAUGE.

**S2 — SRC (CLOSED): is "the operator is owned" a real closure or a relabel?** Attack: "the no-go is a
proven negative; calling it CLOSED asserts nothing new." Test: the verdict does NOT claim the negative
theorem becomes false — it claims the *structural gap* (no correct SRC contact operator exists) is
absent because `D0-SRC-001` (CORE-FORMALIZED, SAME Lean module `D0.Matter.NuclearShellContactSRC`)
supplies the shell-projector overlap operator, verified on the SAME Ca/Fe witness. The two rows are a
matched positive/negative pair proved together. **No external datum enters** (finite shell occupancies
only). The honest scope caveat is recorded (magnitudes stay nuclear-data-facing; the no-go never claimed
them). **NO-KILL.** Verdict stands: CLOSED — but as a *satisfied guard with owned positive companion*,
NOT as "the no-go theorem is refuted".

**S3 — PHASON-WZ-KERNEL / DIXMIER "satisfied guard" readings.** Attack: "you are downgrading real no-gos
to make the count look better." Test: for WZ-KERNEL, the demanded object (finite pressure-energy
operator) is independently owned (`PRESSURE-EOS-SCAFFOLD` + `CONTINUUM-ENVELOPE`, both CERT-CLOSED); the
kernel-only no-go correctly stays a closed-negative numerology guard. For DIXMIER, the mandate FORCES
boundary; I did NOT downgrade it — I labeled it GENUINE-BOUNDARY-PROVEN and left the α-seam sealed. **No
over-claim.** NO-KILL.

**S4 — did any verdict reopen the α-seam?** Grep of my memo: DIXMIER §10 explicitly keeps
`ASSUMP-DIXMIER-TRACE` external and cites `ALPHA_SEAM_NOGO_V2.md` as irreducible; no seam object touched;
no `μ₂`-realization claim. **NO-KILL.**

**S5 — did any GENUINE-BOUNDARY verdict actually have a missed construction?** Re-checked DSIGMA (RHS
cardinality 1 is a theorem, not an unmade link), TORAL (nonnegative canonical adjacency provably absent;
Perron φ AGREES across witnesses so is insufficient), GRAPH-SPACE (isometry decidably refuted),
LEPTON-SELECTOR counting-half (`2<3` cardinality), REP-EXTENSION (grading operator un-owned). Each
missing object is proven-absent or extension-typed, not merely unattempted. **NO-KILL.**

**Skeptic overall: SURVIVES; zero kills.** All ten verdicts hold. The three count-reducers (E2, SRC,
and the WZ-KERNEL guard reading) each rebuild their load-bearing quantity from `(9,11,13)` with no
corpus constant entering its own construction, and none imports what it claims to derive.

---

## §Scoreboard — per-no-go verdict + exact count drop

| # | no-go | verdict | count effect |
|---|---|---|---|
| 1 | D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001 | GENUINE-BOUNDARY-PROVEN (sharpened) | stays no-go |
| 2 | D0-TORAL-CANONICAL-MARKOV-PARTITION-NOGO-001 | GENUINE-BOUNDARY-PROVEN (gauge-retype rejected) | stays no-go |
| 3 | D0-GRAPH-SPACE-NO-ISOMETRY-001 | GENUINE-BOUNDARY-PROVEN (MECH-LIMIT, positively owned) | stays no-go |
| 4 | D0-PHASON-WZ-KERNEL-ONLY-NOGO-001 | GENUINE-BOUNDARY-PROVEN (satisfied guard; operator owned elsewhere) | **off frontier** |
| 5 | D0-PHASON-WDE-Z-MAP-OWNER-001 | GENUINE-BOUNDARY-PROVEN (composite NO-GO+passport, all sub-pieces settled) | **off frontier** |
| 6 | D0-POSTCORE-REPRESENTATION-EXTENSION-NOGO-001 | GENUINE-BOUNDARY-PROVEN (FORM identified-owned; choice B-ext) | stays no-go |
| 7 | D0-POSTCORE-HISTORY-REFINEMENT-MAXIMALITY-NOGO-001 | **CLOSED-MODULO-GAUGE** (quantity=CAP; residue B-ext) | **off frontier** |
| 8 | D0-POSTCORE-LEPTON-SELECTOR-MAXIMALITY-NOGO-001 | GENUINE-BOUNDARY-PROVEN (counting-half existence; assignment-half class-C) | stays no-go |
| 9 | D0-SRC-NOGO-001 | **CLOSED** (missing operator = owned D0-SRC-001) | **off frontier** |
| 10 | D0-DIXMIER-FESHBACH-FINITE-HEATTRACE-001 | GENUINE-BOUNDARY-PROVEN (α-seam mandate) | stays no-go (by mandate) |

**Count semantics (honest).** None of the ten LEAN_PROVED negative theorems is refuted — a proven no-go
does not become false. What changes is the **open/attackable frontier**: how many of these ten still
look like *unclosed gaps a closing forge should attack*.
- **4 drop off the attackable frontier:** #7 (CLOSED-MODULO-GAUGE — its mysterious constant is now the
  owned CAP capacity, residue a named B-ext), #9 (CLOSED — the "missing" operator is owned `D0-SRC-001`),
  #4 and #5 (satisfied guards / composite passports whose every demanded sub-object is owned elsewhere or
  is an intrinsic measurement — not open frontiers).
- **6 are GENUINE-BOUNDARY-PROVEN with the exact minimal missing object named** (#1 PRIM-ROLE-VERTEX-
  SECTOR-ATTACHMENT; #2 D0-TORAL-WILLIAMS-SSE-OWNER-001 / ASSUMP-ADLER-WEISS; #3 M1-forbidden isometry
  (the isotropization limit is the owned replacement); #6 PRIM-FINITE-SPECTRAL-TRIPLE-REP; #8
  PRIM-LEPTON-BRANCH-FIXING-OPERATOR + 3rd-orbit existence; #10 ASSUMP-DIXMIER-TRACE, boundary by
  mandate). Each is proven-external, not unattempted.

**Development delivered (not just cataloguing):**
- #7: the obstruction constant `718` fully routed to the owned capacity `C=2|E|=Tr L=#directed-edges`
  (five faces, bijection with directed edges) — the no-go's residue is now a *typed* B-ext, not an open
  mystery.
- #6: the neutral-current form `nc=p²+q²+3` upgraded from Lean docstring to computed graded-commutant
  dimension (identified-owned FORM).
- #8: split into a hard `2<3` existence wall + a *contentless class-C* assignment freedom — the
  arbitrariness half CLOSES-modulo-gauge.
- #1: sharpened to a tight Continent-1 boundary (representative-choice is class-C gauge).
- #4/#5: shown to be satisfied guards whose demanded operators are owned under other row-ids.

**Verification:** `close_structural_check.py` — LIVE 40/40 PASS; MUTATION 10/10 FIRE. Exact
int/Fraction; every load-bearing constant rebuilt from `(9,11,13)`.

**Discipline honored:** no registry/book/.lean edit; no commit; `053040` untouched; α-seam sealed;
gauge-retype applied ONLY where the prior two-skeptic W1/W3 filing licenses class C (LEPTON assignment,
DSIGMA representatives) and REJECTED where it does not (TORAL, WDE-Z magnitude, E1 grading, E2 family).
