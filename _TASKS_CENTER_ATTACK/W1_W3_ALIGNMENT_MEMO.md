# W1+W3 ALIGNMENT MEMO — A-cluster filing under P-GAUGE-STRUCTURAL + full T3/B-cluster filing under the FOUR-CELL import classification

**Date:** 2026-07-06. **Waves:** W1 (A-cluster, 8 rows) + W3 (all 22 T3 rows + B-cluster 8).
**Status:** READ-ONLY deliverable. No registry row edited, no book edited, no cert edited,
no `.lean` touched, **row/claim 053040 untouched**. All notes-texts below are PROPOSALS for
a later integration step; rows are never deleted.

**Ground truth used:**
1. `_TASKS_CENTER_ATTACK/TORSOR_GAUGE_SYNTHESIS_MEMO.md` (DRAFT v2.1, post-2-skeptics) — the
   ORGANIZING LEMMA in its final form: four-cell classification **A / B-meas / B-adj / B-ext /
   C (owned-torsor gauge-fixing) / D (un-owned ansatz)**, the computable D-vs-C test
   (does the choice generate a new family-canonical invariant?), the three-continent wall map
   with border criterion (empty admissible set ⇒ existence wall; alternatives AGREEING on
   invariant content ⇒ insufficiency wall; DIFFERING ⇒ freedom wall → files B/C/D).
   **Grade discipline observed throughout:** the lemma is a *candidate reading layer*, NOT a
   principle. Every tag below says "instance-of the organizing lemma (reading layer)" — never
   "corollary of the gauge principle".
2. `_TASKS_CENTER_ATTACK/UPLIFT_MAP.md` — cluster A (8), cluster B (7+1), the 22 T3 rows.
3. Registry `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` (549 lines; line = row number)
   + `03_THEORY_MAP/theory_status_map.csv` (generated twin; sync spot-checked, line numbers
   and notes identical for sampled rows 406/526/549).

**Two principles kept DISTINCT (do-not-conflate discipline, stated once here):**
- **P-GAUGE-STRUCTURAL** (UPLIFT_MAP cluster-A "P-GAUGE"): *finite gauge structure requires
  the graded incidence carrier + an associative matrix representation + the symmOffDiag
  projection; every ungraded/flat/bare shortcut fails.* A candidate structural principle,
  un-minted. Its instances are formalism-shape no-gos — NOT freedom walls.
- **The within-zone ORGANIZING LEMMA** (TORSOR_GAUGE_SYNTHESIS_MEMO v2.1): within-zone labels
  are gauge-fixing data; internal physics lives in the invariant ring; imports type
  A / B-meas / B-adj / B-ext / C / D. A candidate READING LAYER over C1 + row 549 + M2.
  Its domain is freedom-shaped walls only; it is SILENT on existence/insufficiency walls
  (Continent 3) and on structural-formalism no-gos (the A-cluster).

**Headline W1 finding (⚠DISAGREE with the wave seeding itself):** the A-cluster no-gos are
NOT filable as corollaries/instances of the within-zone organizing lemma. None of the eight
is freedom-shaped: each proves a structural/formalism impossibility (a wall or a computed
counterexample), i.e. the organizing lemma's own scope clause ("freedom-shaped matter walls
only") excludes them. They file as corollaries of **P-GAUGE-STRUCTURAL** (plus, for the
stress-suite legs, P-CAPACITY and P-M1-FIREWALL), exactly as UPLIFT_MAP seeded. Filing them
under the organizing lemma would be the precise conflation the two-principles note forbids.

---

## Contents
- §1 W1 — A-cluster (8 rows): P-GAUGE-STRUCTURAL leg per row
- §2 W3 — the 22 T3 rows: four-cell filing per row
- §3 W3 — B-cluster remainder (3 rows not already in §2)
- §4 Counts per cell
- §5 Disagreement roster
- §6 Blocked-on-reading (M2/G_res 3-way)
- §7 Ranked highest-value notes-texts
- §8 Skeptic pass (independent agent) — verdict

(Sections filled incrementally below.)

---

## §1 W1 — A-cluster (8 rows) → P-GAUGE-STRUCTURAL legs

Registry citations are `CLAIM_TO_LEAN_MAP.csv:<line>` (line = row number; header is line 1).
Every row here is LEAN_PROVED with release_status NO-GO (row 120: NO_GO_PROVED). Scope check
performed per row: none of the eight contains a witness-pair / moduli / underdetermination
statement — all are structural impossibilities or computed counterexamples, so the
ORGANIZING LEMMA is silent on all eight (its domain is freedom-shaped walls). Filing parent:
**P-GAUGE-STRUCTURAL** (candidate principle, un-minted — the corollary tags below are
proposals contingent on its future mint; until minted they are grouping tags only).

### A1. D0-NO-GO-BARE-ARCHIVE-NONABELIAN-001 (csv:79)
- **Decisive sentence (verbatim, csv:79):** "Nonabelian completion remains outside bare
  archive operator."
- **Filed:** corollary-of:P-GAUGE-STRUCTURAL, **matrix-rep leg** (the bare archive lacks the
  associative matrix representation required for nonabelian structure). Matches UPLIFT_MAP:52.
- **Not the organizing lemma:** no admissible-alternative set is exhibited; this is an
  absence statement (Continent-3 shape), not a freedom.
- **Notes-text:** `UPLIFT[2026-07-06]: corollary-of:P-GAUGE-STRUCTURAL (matrix-rep leg;
  candidate principle, un-minted); NOT an instance of the within-zone organizing lemma
  (absence-shaped, not freedom-shaped); row unchanged.`

### A2. D0-NO-GO-EDGE-STIFFNESS-SCALAR-LEAKAGE-001 (csv:80)
- **Decisive sentence (verbatim, csv:80):** "Bare HP+PH can leak scalar diagonal without
  symmOffDiag projection."
- **Filed:** corollary-of:P-GAUGE-STRUCTURAL, **projection (symmOffDiag) leg**. Matches
  UPLIFT_MAP:53.
- **Notes-text:** `UPLIFT[2026-07-06]: corollary-of:P-GAUGE-STRUCTURAL (symmOffDiag
  projection leg; candidate principle, un-minted); computed-leakage exhibit, not a freedom
  wall — organizing lemma silent; row unchanged.`

### A3. D0-NO-GO-FLAT-TENSOR-NONABELIAN-001 (csv:81)
- **Decisive sentence (verbatim, csv:81):** "Naive flat tensor of two skew sectors is
  symmetric and leaves the skew/vector sector."
- **Filed:** corollary-of:P-GAUGE-STRUCTURAL, **grading leg** (flat = ungraded tensor fails;
  the graded incidence carrier is what keeps the skew sector). Matches UPLIFT_MAP:54.
- **Notes-text:** `UPLIFT[2026-07-06]: corollary-of:P-GAUGE-STRUCTURAL (grading leg;
  candidate principle, un-minted); structural impossibility, organizing lemma silent;
  row unchanged.`

### A4. D0-GAUGE-BIANCHI-RESIDUAL-BOUNDARY-001 (csv:83)
- **Decisive sentence (verbatim, csv:83):** "Residual expansion is exact by definition; flat
  ungraded residual is NO-GO while graded incidence Bianchi is closed."
- **Filed:** corollary-of:P-GAUGE-STRUCTURAL, **graded-Bianchi leg** (positive half: graded
  Bianchi closes; negative half: flat ungraded fails). Matches UPLIFT_MAP:55.
- **Notes-text:** `UPLIFT[2026-07-06]: corollary-of:P-GAUGE-STRUCTURAL (graded-Bianchi leg;
  candidate principle, un-minted); paired positive/negative exhibit, organizing lemma silent;
  row unchanged.`

### A5. D0-NO-GO-ABSTRACT-LIERING-FINITE-TRANSFORM-001 (csv:89)
- **Decisive sentence (verbatim, csv:89):** "Finite transform cannot be stated in bare
  abstract LieRing form without an associative matrix representation."
- **Filed:** corollary-of:P-GAUGE-STRUCTURAL, **associativity leg** — the strongest leg
  witness: the statement is UNSTATEABLE without the associative rep (a wall, not a
  counterexample). Matches UPLIFT_MAP:56.
- **Notes-text:** `UPLIFT[2026-07-06]: corollary-of:P-GAUGE-STRUCTURAL (associativity leg;
  candidate principle, un-minted); unstateability wall, organizing lemma silent;
  row unchanged.`

### A6. D0-NO-GO-NAIVE-LOCAL-GAUGE-COVARIANCE-001 (csv:94)
- **Decisive sentence (verbatim, csv:94):** "Old naive flat matrix local transform has a
  concrete Fin 3 counterexample."
- **Filed:** corollary-of:P-GAUGE-STRUCTURAL, **negative-control exhibit** (Fin 3). Matches
  UPLIFT_MAP:57.
- **Notes-text:** `UPLIFT[2026-07-06]: corollary-of:P-GAUGE-STRUCTURAL (negative-control
  exhibit, Fin 3; candidate principle, un-minted); computed counterexample, organizing lemma
  silent; row unchanged.`

### A7. D0-NO-GO-UNGRADED-BIANCHI-RESIDUAL-001 (csv:96)
- **Decisive sentence (verbatim, csv:96):** "Flat ungraded commutator graph has a concrete
  Fin 2 residual counterexample."
- **Filed:** corollary-of:P-GAUGE-STRUCTURAL, **negative-control exhibit** (Fin 2). Matches
  UPLIFT_MAP:58.
- **Notes-text:** `UPLIFT[2026-07-06]: corollary-of:P-GAUGE-STRUCTURAL (negative-control
  exhibit, Fin 2; candidate principle, un-minted); computed counterexample, organizing lemma
  silent; row unchanged.`

### A8. D0-NO-GO-STRESS-SUITE-001 (csv:120) — PER-LEG SPLIT (⚠SEED confirmed)
- **Decisive sentence (verbatim, csv:120):** "[Iter15] Lean suite now proves FOUR Lean-backed
  no-gos: isolated one-phason generation; isolated-phason baryon-S3 sector; Euclidean
  signature export; and the rank-one Higgs scalar-projector obstruction
  (no_go_rank_one_higgs_scalar_projector)."
- **Filed (four legs, three principles — UPLIFT_MAP:61-67 split VERIFIED against the four
  named Lean theorems in csv:120):**
  1. `no_go_isolated_phason_generation_carrier` → corollary-of:**P-CAPACITY** (a lone phason
     lacks coupling capacity);
  2. `no_go_isolated_phason_baryon_s3_sector` → corollary-of:**P-CAPACITY**;
  3. `no_go_euclidean_signature_export` → corollary-of:**P-M1-FIREWALL** (nonreversibility
     forbids the signature flip);
  4. `no_go_rank_one_higgs_scalar_projector` → corollary-of:**P-GAUGE-STRUCTURAL** ("a rank-1
     doublet-projector mask cannot commute with the weak swap, by decide; rank-2 is
     gauge-compatible, negative control" — csv:120 verbatim).
- **Notes-text:** `UPLIFT[2026-07-06]: PER-LEG corollary tags (row kept intact): legs 1-2
  corollary-of:P-CAPACITY, leg 3 corollary-of:P-M1-FIREWALL, leg 4
  corollary-of:P-GAUGE-STRUCTURAL (all candidate principles, un-minted); no leg is
  freedom-shaped — organizing lemma silent on all four; row unchanged.`

**§1 verdict:** 8/8 filed under P-GAUGE-STRUCTURAL (+P-CAPACITY×2, +P-M1-FIREWALL×1 via the
stress-suite split); 0/8 under the organizing lemma. The wave-1 seeding ("file as corollaries
of the organizing lemma") is a conflation and is REJECTED with reasons per row — this is the
memo's first roster-level disagreement (§5, D-1).

---

## §2 W3 — the 22 T3 rows under the four-cell classification

Procedure per row (the gauge memo's computable filing procedure, §X-L3/X-L4): declare the
acting group → run the border criterion (empty / agreeing / differing admissible set) →
if freedom, run determinacy + the D-vs-C test (does the choice generate a new
family-canonical invariant?) → assign exactly one of B-meas / B-adj / B-ext / C / D, or
relocate to Continent 3 if the content is existence/insufficiency-shaped.

**Sub-typing convention used (from the gauge memo §X-L3):** B-ext requires corpus typing as
a NEW primitive / extension / bridge assumption (`EXACT-MISSING: PRIM-*`, `ASSUMP-*`, or the
row's own "NEW primitive (extension)" wording); B-meas is an experimental number/passport
comparison with NO missing-primitive typing; C requires an OWNED torsor AND zero class-A
invariant change (the "cannot be wrong" license applies to C only).

### T3-1. D0-CMB-CANONICAL-SMOOTHING-MAXIMALITY-NOGO-001 (csv:404) — cell **B-meas**
- **Decisive sentence (verbatim, csv:404):** "THREE legitimate positive weightings give THREE
  distinct tilts (A=mult (12,10,8,2), B=low-lambda (12,5,2,1), C=high-lambda (2,4,8,12));
  also varies with k."
- **Moduli object:** the admissible-smoothing family — pairs (k, u) of evaluation scale +
  positive weighting over modes {20,22,24,33}.
- **Acting group:** the admissible-weighting class (positive weightings × evaluation points).
  FLAG: declared-by-family, not a scene-computed Aut group — reading-conditional in the weak
  sense (the admissibility class is the row's own construction).
- **Border criterion:** ≥3 alternatives DIFFERING on invariant content (three distinct n_s
  tilts) ⇒ **freedom wall** ⇒ files B/C/D.
- **D-vs-C:** each smoothing point yields a DIFFERENT tilt (no family-canonical common value,
  no owned torsor) ⇒ not C, not D ⇒ class B. Sub-type: csv:404 closes with "n_s requires an
  EXTERNAL Planck-comparison passport" and NO missing-PRIM is typed (csv:363 confirms:
  "remaining artifact is purely EXTERNAL (Planck-comparison passport), not an internal
  theorem") ⇒ **B-meas**.
- **Invariant content (survives):** the Laplacian mode set {20,22,24,33} with multiplicities;
  the closed-negative internal-forcing verdict itself.
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=(k,u) admissible-smoothing family over modes {20,22,24,33}; gauge-fixing=B-meas:
  external Planck-comparison passport; invariant content=mode set+multiplicities, internal
  forcing closed-negative; row unchanged.`

### T3-2. D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001 (csv:405) — cell **B-meas**
- **Decisive sentence (verbatim, csv:405):** "two admissible maps w1(z)=-phi-z,
  w2(z)=-phi-2z respect every owned invariant (negative on z>=0, anchor -phi at z=0) yet
  differ at z=1."
- **Moduli object:** magnitude maps z ↦ w_DE(z) anchored at −φ, sign-negative.
- **Acting group:** the admissible-map class (anchor + sign preserved). FLAG:
  declared-by-family, not scene-computed.
- **Border criterion:** ≥2 alternatives DIFFERING at z=1 ⇒ freedom wall.
- **D-vs-C:** values differ per point ⇒ not C/not D ⇒ B. Sub-type: csv:405 "needs an external
  physical-branch passport (DESI/CPL)"; no missing-PRIM typed on THIS row (the coordinate
  functor PRIM lives on E3/P2-E, distinct rows) ⇒ **B-meas** (DESI/CPL passport datum).
- **Invariant content (survives):** the SIGN (Galois-forced, owner
  D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001, anchor −φ) + the continuum envelope w_D0(s)
  (csv:452, CERT-CLOSED). HONESTY (memory-anchored): DESI confirms EVOLVING dark energy only,
  not the thawing corner — the passport datum must not be over-read.
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=magnitude maps z->w_DE(z) anchored -phi; gauge-fixing=B-meas: DESI/CPL passport
  (evolving-DE only, no corner claim); invariant content=Galois sign owner + w_D0(s)
  envelope; row unchanged.`

### T3-3. D0-CKM-OVERLAP-UNDERDETERMINATION-NOGO-001 (csv:406) — cell **B-ext** (REUSED)
- **Decisive sentence (verbatim, csv:406):** "Two admissible rational-orthogonal overlap
  completions (3-4-5 and 5-12-13 rotations) give different Cabibbo overlap invariants
  |V_mix_12|^2 = 16/25 vs 144/169".
- **Filing REUSED from the gauge memo** (§X-L3 C4, Continent 2 table, EoR-2): alternatives
  DIFFER on invariant content (16/25 ≠ 144/169, Lean-proved) ⇒ freedom wall; the row itself
  types the resolution "a canonical selector (symmetry-breaking/modulus-fixing) is a NEW
  primitive (extension), not a present-core theorem" ⇒ **B-ext**.
- **Moduli object:** basis-completion torsor (rational-orthogonal completions of the frozen
  mismatch data). **Acting group:** common-basis rotations (declared in gauge memo §X-L3).
- **Invariant content (survives):** the mismatch matrix GIVEN fixed bases
  (D0.Matter.CKMBasisMismatch); CKM topology (csv:526 scope note).
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=basis-completion torsor (3-4-5 vs 5-12-13 witnesses); gauge-fixing=B-ext: canonical
  selector row-typed NEW primitive (extension) — Cabibbo measurement is the practical
  trivialization, not core; invariant content=mismatch-given-bases + topology; filing reused
  from TORSOR_GAUGE_SYNTHESIS_MEMO v2.1 (C4); row unchanged.`

### T3-4. D0-TORAL-SEED-MARKOV-MAXIMALITY-NOGO-001 (csv:408) — cell **B-ext** (BORDERLINE, flagged)
- **Decisive sentence (verbatim, csv:408):** "A 2-rectangle and a 3-rectangle admissible
  adjacency realize the same golden dynamics => partition/adjacency/rectangle-count NOT
  forced by the seed; a canonical partition needs an external Adler-Weiss/Williams choice
  (D0-ADLER-WEISS-PARTITION-OWNER-001, passport)."
- **Moduli object:** admissible nonnegative-integer Markov adjacencies carrying golden Perron
  data (Mphi 2-rect, M2, A3 3-rect witnesses).
- **Acting group:** the admissible-adjacency class. FLAG: declared-by-family.
- **Border criterion — BORDERLINE, resolved to freedom:** the OWNED dynamical invariants
  (spectrum {phi,psi}, entropy log phi, trace, det from the integral conjugacy) AGREE across
  the witnesses — an agreeing-set reading would file this on Continent 3 (insufficiency,
  LEPTON-PUISEUX-parallel). BUT the alternatives DIFFER on symbolic-model invariant content:
  rectangle count 2 vs 3, and charpoly x²−x−1 (Mphi) vs x(x²−x−1) (A3) — the extra 0
  eigenvalue is a zeta-function-level separation of the resulting SFTs. Differing invariant
  content of the completed object ⇒ freedom wall.
- **D-vs-C:** the partition space is NOT owned (csv:408: canonical partition needs the
  external choice) ⇒ C unavailable; the choice injects model-level invariants (rectangle
  count, charpoly) ⇒ content-bearing. Resolution is typed via the owner-edge
  ASSUMP-ADLER-WEISS (csv:244, bridge assumption) ⇒ **B-ext**.
- **Invariant content (survives):** spectrum {phi,psi}, entropy log phi, trace, det — all
  forced by C T C⁻¹ = −M_phi.
- **⚠ Border-tension flag (§5, D-6):** which invariants count (owned-dynamics vs
  symbolic-model) flips this row Continent-3 ↔ B-ext. Filed B-ext because the border
  criterion tests the alternatives' OWN invariant content (as in VNEXT2: 15708 vs 14990
  counted as differing), and because the corpus already types the resolution as a bridge
  assumption — but the tension is recorded, not suppressed.
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=admissible golden Markov adjacencies (2-rect vs 3-rect witnesses); gauge-fixing=
  B-ext: ASSUMP-ADLER-WEISS partition choice (owner-edge csv:244); invariant content=
  {phi,psi} spectrum, entropy log phi, trace, det; border-tension flagged (owned invariants
  agree, model invariants differ); row unchanged.`

### T3-5. D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001 (csv:352) — **Continent 3 (insufficiency), NO B/C/D cell** (REUSED; ⚠DISAGREE with UPLIFT_MAP T3 seed)
- **Decisive sentence (verbatim, csv:352):** "ramification index 1/n does NOT uniquely
  determine the operator -- two distinct 4x4 companion-type matrices both have charpoly
  x^4-lam (index 1/4)".
- **Filing REUSED from the gauge memo** (Continent 3 table + EoR-8 re-check): "two companion
  matrices AGREE on the invariant (charpoly x⁴−λ) — the border criterion keeps this row on
  Continent 3, against the freedom-shaped first impression." Alternatives AGREEING on all
  invariant content ⇒ **insufficiency wall**; the organizing lemma is SILENT here.
- **⚠DISAGREE (§5, D-2):** UPLIFT_MAP:83 seeded T3 ("companion-operator fiber over branch
  index; Green-resolvent certificate = gauge fixing"). The row's content forces Continent 3:
  no choice among the companions carries content (they agree on the invariant), so there is
  no gauge-fixing datum to file — what is missing is a SEPARATING certificate (an
  insufficiency), not a trivialization.
- **Invariant content (survives):** charpoly x⁴−λ; the exponent row (0,1/4,1/3) as exact
  row (not branch-index theorem).
- **Notes-text:** `UPLIFT[2026-07-06]: Continent-3 INSUFFICIENCY wall per the border
  criterion (companions agree on charpoly x^4-lam) — organizing lemma silent, NO B/C/D cell;
  T3-torsor seed in UPLIFT_MAP rejected; filing reused from TORSOR_GAUGE_SYNTHESIS_MEMO v2.1
  Continent-3 table; row unchanged.`

### T3-6. D0-LEPTON-BRANCH-SELECTOR-MAXIMALITY-NOGO-001 (R4, csv:463) — cell **C** (REUSED)
- **Decisive sentence (verbatim, csv:463):** "But the block->generation ASSIGNMENT is free:
  sigmaA=(0123)(456) and sigmaB=(012)(3456) both have order exactly 12 (Lean: ^[12]=id,
  ^[4]!=id, ^[6]!=id) yet sigmaA != sigmaB; and c4=4,r3=3 are rfl INPUTS."
- **Filing REUSED from the gauge memo** (Continent 1 table: "R4/E4 lepton branch |
  block→generation assignment | S₇-conjugation (computed C3)"). Script fact C3: σA ~ σB are
  S₇-CONJUGATE (explicit h), same order-12, same resolvent — NO class-A value moves under
  the assignment choice ⇒ the D-vs-C test returns "no new invariant" ⇒ **class C**
  (owned-torsor gauge-fixing; torsor owned via the frozen shell-torus U_eff).
- **Moduli object:** the S₇-conjugation orbit of order-12 (4,3)-type permutations (420
  members). **Acting group:** S₇-conjugation — owned (computed from the frozen 7-point
  shell-torus carrier).
- **Invariant content (survives):** det(I−zU)=(1−z⁴)(1−z³); order 12; (4,3) as the UNIQUE
  order-12 cycle type among the 15 partitions of 7.
- **Scope guard carried (csv:463 SCOPE-REPAIR, verbatim):** "does NOT prove a
  branch-sensitive selector cannot exist if the group excludes it" — and indeed L4 (csv:491)
  later showed the orbit-keyed exponent selector IS branch-sensitive (orbit sizes 4≠3
  intrinsically distinct). The class-C filing covers the block→generation ASSIGNMENT leg
  only; the third-generation counting half is Continent 3 (L4, filed in the gauge memo).
- **Missing-primitive clause surfaced (csv:463, verbatim):** "EXACT-MISSING:
  PRIM-LEPTON-BRANCH-FIXING-OPERATOR." Disambiguation (same clause as T3-20): the PRIM types
  the INTERNAL non-derivability of the assignment datum (the 549-analog: no M1-legal internal
  rule selects the point), NOT the cell of the datum itself — precedent: the gauge memo's
  §Consequence files ASSUMP-WITHINZONE-LABELING-EXTERNAL as class C under exactly this
  distinction (imports a point of the owned torsor, not new structure). A missing-PRIM clause
  therefore does NOT auto-file B-ext when the D-vs-C test returns "no new invariant" on an
  owned torsor.
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=branch->generation assignment orbit (420 order-12 perms); gauge-fixing=C:
  S7-conjugation point-choice on the owned shell-torus torsor (no class-A value moves,
  script C3); EXACT-MISSING PRIM-LEPTON-BRANCH-FIXING-OPERATOR carried = internal
  non-derivability of the C-datum, not a cell change (precedent
  ASSUMP-WITHINZONE-LABELING-EXTERNAL -> class C); invariant content=resolvent det, order
  12, unique (4,3) type; counting half (2<3) stays Continent 3 with L4; filing reused from
  TORSOR_GAUGE_SYNTHESIS_MEMO v2.1 Continent-1; row unchanged.`

### T3-7. D0-POSTCORE-PHASON-EXTENSION-MAXIMALITY-NOGO-001 (E3, csv:470) — cell **B-ext**
- **Decisive sentence (verbatim, csv:470):** "even adopting S_DE, role(2) x cocycle(2) = 4
  admissible w_E(z): w_A != w_B (R2) AND phi-tick z(1)=phi-1 != integer-tick z(1)=1 (NEW)."
- **Moduli object:** the 4-point role × cocycle torsor (pressure/energy orientation ×
  tick-cocycle choice). **Acting group:** role-swap × cocycle-swap (Z2×Z2 on the witness
  set). FLAG: declared-by-construction on an ADOPTED (not owned) common sector.
- **Border criterion:** 4 alternatives DIFFERING on invariant content (w_A≠w_B; z(1) values
  differ) ⇒ freedom wall.
- **D-vs-C:** the underlying sector is explicitly un-owned (the row's first half proves NO
  typed common sector) ⇒ C unavailable; values differ per point ⇒ not family-canonical ⇒
  not D ⇒ B. Sub-type: "EXACT-MISSING: PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT +
  PRIM-PHASON-COORDINATE-FUNCTOR (physical map = external passport)" ⇒ **B-ext** (two typed
  missing primitives).
- **Invariant content (survives):** integer L_archive spectrum {24,22,20}; the
  incommensurability product 359/160; the sign owner.
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=role(2)x cocycle(2) 4-torsor over the adopted S_DE sector; gauge-fixing=B-ext:
  PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT + PRIM-PHASON-COORDINATE-FUNCTOR (typed
  missing primitives); invariant content={24,22,20}, 359/160, Galois sign; row unchanged.`

### T3-8. D0-VNEXT-MARTINGALE-DIRAC-OWNER-001 (csv:422) — cell **B-ext** (⚠ phrasing disagree with UPLIFT_MAP)
- **Decisive sentence (verbatim, csv:422):** "lambda_N=phi^N and lambda_N=2^N are each
  strictly increasing to infinity (compact-resolvent AF triples, a la Christensen-Ivan) yet
  differ at N=1 (phi!=2). Scale selection is a SECOND independent primitive
  (PRIM-DIRAC-SCALE-SELECTION)."
- **Moduli object:** Dirac scale laws N ↦ λ_N on the AF tower. **Acting group:** the
  admissible strictly-increasing scale-law class. FLAG: declared-by-family; the AF tower
  itself is an independent formalism layer, not the scene.
- **Border criterion:** alternatives DIFFER (φ ≠ 2 at N=1) ⇒ freedom wall.
- **D-vs-C:** scale-law space un-owned ⇒ not C; per-choice values differ ⇒ not D ⇒ B.
  Sub-type: the row ITSELF types the resolution as a primitive
  (PRIM-DIRAC-SCALE-SELECTION) ⇒ **B-ext**.
- **⚠ (§5, D-4 family):** UPLIFT_MAP:123 calls the scale law a "gauge-fixing datum" — under
  the four-cell test it is NOT class-C gauge (un-owned space, value-changing choice); it is a
  B-ext trivialization. The word "gauge" must not survive into the notes-text.
- **Invariant content (survives):** nonzero martingale increments (AF dims strictly grow);
  compact-resolvent property across the class.
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=Dirac scale-law family on the AF tower; gauge-fixing=B-ext:
  PRIM-DIRAC-SCALE-SELECTION (typed missing primitive — NOT class-C gauge, space un-owned);
  invariant content=nonzero increments, compact resolvent; row unchanged.`

### T3-9. D0-VNEXT2-SCENE-NATIVE-REFINEMENT-OWNER-001 (csv:437) — cell **B-ext**
- **Decisive sentence (verbatim, csv:437):** ">=2 admissible families (all-walks,
  non-backtracking, directed-edge) satisfy M1 but are inequivalent: depth-2 carriers
  15708 != 14990 (differ by 2|E|=718); transfer dims 33 != 718."
- **Moduli object:** the refinement-family 3-point moduli {all-walks, non-backtracking,
  directed-edge}. **Acting group:** the M1-admissible refinement-rule class. FLAG:
  declared-by-family.
- **Border criterion:** alternatives DIFFER on invariant content (15708 vs 14990; 33 vs 718)
  ⇒ freedom wall. (This is the gauge memo's paradigm DIFFERING case — same arithmetic
  signature 2|E|=718 as E2.)
- **D-vs-C:** rule space un-owned; values differ per family ⇒ B. Sub-type: "Missing
  PRIM-SCENE-HISTORY-REFINEMENT-RULE" ⇒ **B-ext**.
- **Invariant content (survives):** no-φ³ holds in BOTH families (csv:490: min-successor
  19); the frozen scene spectrum; 2|E|=718 as the family gap (E2's owned quantity).
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=refinement-family 3-point moduli (W/NB/E); gauge-fixing=B-ext:
  PRIM-SCENE-HISTORY-REFINEMENT-RULE (typed missing primitive); invariant content=family
  gap 2|E|=718 + no-phi^3 [WITNESS-ONLY + ANSATZ-CLASS-CONDITIONAL: verified in the two
  inspected towers (min-successor 19), NOT a whole-class theorem — do not promote
  downstream; named watch-item, see blocked-on-reading §6.4]; SAME OBJECT as csv:439 +
  csv:490 (H3) — single moduli, three registrations; row unchanged.`

### T3-10. D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001 (csv:439) — cell **B-ext** (same object as T3-9)
- **Decisive sentence (verbatim, csv:439):** "the 34-route is closed and the scene-native
  route is underdetermined (>=2 inequivalent families). First disagreement: depth-2 carrier
  count (15708 vs 14990)."
- **Filing:** identical object to T3-9 (same Lean theorem
  `scene_native_refinement_underdetermined`, same missing primitive) ⇒ **B-ext**, duplicate
  registration. Consolidation candidate: one moduli object, three registry rows (437, 439,
  490) — the notes-text cross-links rather than proposing deletion (rows never deleted).
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  same moduli object as csv:437 (refinement-family; same Lean theorem); gauge-fixing=B-ext:
  PRIM-SCENE-HISTORY-REFINEMENT-RULE; invariant content=as csv:437; duplicate registration
  cross-linked, row unchanged.`

### T3-11. D0-VNEXT2-DIRAC-COVARIANCE-MAXIMALITY-NOGO-001 (csv:446) — cell **B-ext**
- **Decisive sentence (verbatim, csv:446):** "Maximality: candidate scale cocycles
  (gap/diameter/heat-crossover/...) differ across families -> no unique cocycle. Missing
  PRIM-DIRAC-SCALE-SELECTION."
- **Moduli object:** scale-cocycle torsor FIBERED over the refinement moduli (T3-9).
  **Acting group:** cocycle-candidate class per family. FLAG: declared-by-family; doubly
  conditional (fiber over an already-B-ext base).
- **Border criterion:** cocycles DIFFER across families ⇒ freedom wall.
- **D-vs-C:** un-owned, value-differing ⇒ B; typed missing primitive
  PRIM-DIRAC-SCALE-SELECTION (shared with T3-8) ⇒ **B-ext**.
- **VNEXT2 desync note carried (memory):** row 445's Dirac-covariance sibling STAYS OPEN
  (content-free cert) — this filing covers row 446 only.
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=scale-cocycle torsor fibered over refinement moduli (csv:437); gauge-fixing=B-ext:
  PRIM-DIRAC-SCALE-SELECTION (shared with csv:422); invariant content=per-family cocycle
  candidates enumerable, none canonical; row unchanged.`

### T3-12. D0-EDGE-COVER-FAMILY-001 (csv:509) — cell **B-ext** (⚠ phrasing disagree with UPLIFT_MAP "cleanest torsor")
- **Decisive sentence (verbatim, csv:509):** "the return-edge holonomy is constrained only
  to |lambda|=1, its phase is NOT forced by symmetry/unitarity/feedback. Distinct admissible
  holonomies give inequivalent terminal covers -- separating observable z^3-coeff=-lambda is
  INJECTIVE".
- **Moduli object:** the U(1) holonomy family {λ : |λ|=1} of physical edge covers.
  **Acting group:** U(1) on the return-edge phase. FLAG: the |λ|=1 admissibility is
  cert-borne (hybrid owner), the U(1) STRUCTURE is owned-as-family but no torsor POINT is
  owned.
- **Border criterion:** distinct λ give INEQUIVALENT covers with an INJECTIVE separating
  observable (z³-coeff = −λ) ⇒ alternatives DIFFER on invariant content ⇒ freedom wall.
- **D-vs-C — the sharp case:** the injective separator means EVERY point-choice changes an
  observable-level invariant ⇒ the choice is content-bearing ⇒ NOT class C (this is exactly
  falsifier 4's shape: a "gauge" choice that changes a class-A-visible value is not gauge).
  Not D (no family-canonical common value is injected — each λ gives a different one).
  ⇒ B. Sub-type: "EXACT-MISSING: PRIM-EDGE-HOLONOMY-SELECTOR (undefined corpus-wide;
  selecting a unique lambda needs NEW frozen input)" ⇒ **B-ext**.
- **⚠ (§5, D-3):** UPLIFT_MAP:179 files this as "cleanest torsor in corpus: holonomy
  U(1)-torsor; λ = gauge-fixing datum". Under the four-cell test the phrase "gauge-fixing
  datum" is WRONG-CELL: λ-choice is injectively observable ⇒ content-bearing ⇒ B-ext, not C.
  The torsor READING (U(1)-family) survives; the gauge LICENSE does not.
- **Invariant content (survives):** |λ|=1 admissibility; the family structure itself; the
  injectivity of the separator (Lean cover_coeff_injective).
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=U(1) holonomy family |lambda|=1; gauge-fixing=B-ext: PRIM-EDGE-HOLONOMY-SELECTOR
  (typed missing primitive; lambda-choice is injectively observable, hence NOT class-C
  gauge); invariant content=family structure + separator injectivity; row unchanged.`

### T3-13. D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001 (csv:361) — cell **B-ext**
- **Decisive sentence (verbatim, csv:361):** "anomaly-freedom + the proposed {grav,su2,su3
  linear, cubic} constraints leave a >=2-dim variety span{Y, B-L}, so the SM hypercharge row
  is NOT forced."
- **Moduli object:** the 2-dim charge-direction moduli inside the 3-dim anomaly-free
  solution space (span{Y, B−L} exhibited). **Acting group:** GL-mixing on the solution
  space. FLAG: group declared on the derived variety, not a scene Aut group.
- **Border criterion:** Y and B−L are Q-independent solutions ⇒ alternatives DIFFER on
  invariant content (different charge rows are physically distinct) ⇒ freedom wall.
- **D-vs-C:** the charge-direction space is derived-owned as a VARIETY but no point is
  owned; per-point content differs ⇒ B. Sub-type: the designated trivialization is the
  EXISTING bridge D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001 under
  ASSUMP-KERNEL-CHARGE-LOCALIZATION (UPLIFT_MAP:256-258) — a bridge assumption ⇒ **B-ext**.
  csv:361 also names the question-begging alternative ("Removing B-L requires imposing
  Y_nuRc=0 (SM convention, question-begging)") — that would be an illegal C-masquerade, the
  row's own policing.
- **Invariant content (survives):** rank 3 of the anomaly matrix (exact-Q); the
  denominator-6 owner (separate row); ΣY = ΣY³ = 0 sums (class A per gauge memo C5).
- **Distinct from the C-cell HYPERCHARGE-FLOW attachment leg:** the gauge memo's Continent-1
  entry "HYPERCHARGE-FLOW (attachment leg) | slot row | slot permutations (computed C5)" is
  a DIFFERENT row (D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001); do not transfer its class-C verdict
  here.
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=charge-direction moduli span{Y,B-L} in the rank-3 anomaly kernel; gauge-fixing=
  B-ext: BL-DIRECTION bridge (ASSUMP-KERNEL-CHARGE-LOCALIZATION); invariant content=rank 3,
  sum invariants, denominator-6 owner; slot-attachment C-leg belongs to the FLOW owner row,
  not here; row unchanged.`

### T3-14. D0-GRADING-NEUTRAL-CURRENT-MAXIMALITY-NOGO-001 (G2, csv:489) — cell **B-ext**
- **Decisive sentence (verbatim, csv:489):** "a Z2-grading signature (p,q), p+q=3, gives
  neutral-current count nc=p^2+q^2+3: (2,1)->8 != (3,0)->12, both anomaly-free +
  S3-symmetric. The grading operator is NOT forced".
- **Moduli object:** grading-signature choices (p,q) on the derived M3 block.
  **Acting group:** signature swaps on the two-completion witness set. FLAG: witness-only
  (csv:489: "no whole-class exhaustion") — the moduli is exhibited, not exhausted.
- **Border criterion:** nc = 8 ≠ 12 ⇒ alternatives DIFFER ⇒ freedom wall.
- **D-vs-C:** grading operator un-owned; nc differs per choice ⇒ B. Sub-type:
  "EXACT-MISSING: PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR" ⇒ **B-ext** (measured
  neutral-current content is the practical trivialization, but the corpus types the
  resolution as a primitive).
- **Invariant content (survives):** the M3 block itself (R1 commutant); anomaly-freedom;
  S3 symmetry; the quadratic form nc = p²+q²+3 as FORM (E1's owned candidate).
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=Z2-grading signatures (p,q) on the M3 block (witness pair (2,1)/(3,0));
  gauge-fixing=B-ext: PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR (typed missing primitive);
  invariant content=M3 block, anomaly-freedom, S3 symmetry, form nc=p^2+q^2+3; row
  unchanged.`

### T3-15. D0-PHASON-PRESSURE-ENERGY-MAXIMALITY-NOGO-001 (P1-C, csv:492) — **Continent 3 (existence), NO B/C/D cell** (⚠DISAGREE with UPLIFT_MAP T3 seed)
- **Decisive sentence (verbatim, csv:492):** "No typed common sector across
  {L_archive,QUQ,W_eff,log-det pressure,S_DE}: integer L_archive spectrum {24,22,20}
  incommensurate with the irrational S_DE window (product 359/160); distinct carriers, no
  canonical intertwiner in the admissible map class (universal-property obstruction)."
- **Border criterion:** the blocking slot is "a typed common sector / canonical
  intertwiner"; the admissible set of such intertwiners is EMPTY ("no canonical intertwiner
  in the admissible map class") ⇒ **existence wall, Continent 3**. The organizing lemma is
  silent; no gauge-fixing datum exists to file.
- **⚠DISAGREE (§5, D-5):** UPLIFT_MAP:182 seeded "pressure-energy role torsor; observed
  w(z) = gauge fixing". The ROLE freedom is real but lives on the SIBLING rows (E3 csv:470,
  WZ-TRANSFER csv:312 role-leg, P1-EOS csv:508) — P1-C's own content is the empty
  intertwiner set (typed incommensurability 359/160), which is existence-shaped. Filing
  P1-C as a torsor would relabel an existence wall as a freedom — the exact over-read the
  border criterion exists to catch.
- **Resolution typing noted (not a cell):** "EXACT-MISSING:
  PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT" — the completion class is extension-typed,
  consistent with Continent 3 rows carrying admissible-completion classes (cf. gauge memo
  Continent-3 HIGGS entry).
- **Invariant content (survives):** {24,22,20}; 359/160; the operator-type firewall.
- **Notes-text:** `UPLIFT[2026-07-06]: Continent-3 EXISTENCE wall per the border criterion
  (empty admissible set of canonical/eigenvalue-matching intertwiners, typed
  incommensurability 359/160) — organizing lemma silent, NO B/C/D cell; role-freedom
  siblings (csv:470/312/508) carry the B-ext filings; UPLIFT_MAP T3 seed rejected; row
  unchanged.`

### T3-16. D0-PHASON-WZ-TRANSFER-OWNER-001 (csv:312) — **SPLIT: role leg B-ext + SEP leg Continent 3**
- **Decisive sentence (verbatim, csv:312):** "Two obstructions, the first now
  machine-checked: SEP (spectral disjointness, Lean sde_window_root_not_archive_eigenvalue):
  the integer L_archive spectrum {24,22,20} shares NO eigenvalue with the S_DE active window
  (roots of x^2-3x+359/160), so no eigenvalue-matching / canonical intertwiner maps one
  carrier onto the other; ROLE (D0-PHASON-PRESSURE-ENERGY-MAXIMALITY-NOGO-001): distinct
  admissible pressure/energy role-orientations give distinct EOS (witnesses w_A~0.900,
  w_B~1.111)".
- **Filing (two legs, mirroring UPLIFT_MAP:183's own split):**
  - **SEP leg** → empty admissible set of eigenvalue-matching intertwiners ⇒ **Continent 3
    existence** (P-TYPED-shaped: number-field/spectrum type separation); the lemma silent.
  - **ROLE leg** → admissible role-orientations DIFFER (w_A ≠ w_B) ⇒ freedom wall; un-owned
    orientation space; typed missing primitive
    PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT ⇒ **B-ext**.
- **Invariant content (survives):** {24,22,20} vs S_DE window disjointness (exact over Q);
  physical w_DE(z) stays external CPL/DESI passport, never core.
- **Notes-text:** `UPLIFT[2026-07-06]: SPLIT filing — SEP leg = Continent-3 existence wall
  (empty intertwiner set, exact spectral disjointness), organizing lemma silent; ROLE leg =
  instance-of the organizing lemma (reading layer), moduli=pressure/energy role
  orientations, gauge-fixing=B-ext: PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT; invariant
  content=exact disjointness over Q + passport boundary; row unchanged.`

### T3-17. D0-ALPHA-RESIDUE-DELTA-NORMALIZATION-NOGO-001 (csv:354) — cell **B-ext**
- **Decisive sentence (verbatim, csv:354):** "the finite Feshbach-Schur residue determines
  alpha_alg^-1=(159739/5,-294902/15) exactly, but does NOT by itself fix the Delta_alpha
  NORMALIZATION -- canonization|->Delta is injective, so the single finite residue value is
  compatible with more than one Delta_alpha".
- **Moduli object:** the 2nd-canonization choice (which 2^11 Dixmier pairing).
  **Acting group:** the canonization-choice class. FLAG: declared-by-family.
- **Border criterion:** canonization ↦ Δ_α is INJECTIVE ⇒ distinct choices give distinct
  Δ_α ⇒ alternatives DIFFER on invariant content ⇒ freedom wall.
- **D-vs-C:** injective separator ⇒ every choice is content-bearing ⇒ NOT class C (same
  falsifier-4 shape as EDGE-COVER). Not D (no family-canonical injected value). ⇒ B.
  Sub-type: the resolving datum is the external Dixmier/Wodzicki extraction, owner
  D0-DIXMIER-RESIDUE-OWNER-001 under **ASSUMP-DIXMIER-TRACE — proven IRREDUCIBLE in
  present-core** (ALPHA-SEAM, memory + UPLIFT_MAP:246) ⇒ **B-ext** (bridge-assumption-typed;
  the hardest-typed B-ext in the roster).
- **⚠ (§5, D-4 family):** UPLIFT_MAP:185 "Dixmier-pairing passport = the 2nd-canonization
  gauge datum" — wrong-cell phrasing again; injectivity forbids the gauge license.
- **Invariant content (survives):** the exact finite residue pair (159739/5, −294902/15);
  the blocks-re-declaring-Dixmier-closed policing.
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=2nd-canonization (Dixmier-pairing) choice, injective into Delta_alpha;
  gauge-fixing=B-ext: ASSUMP-DIXMIER-TRACE owner-edge (proven irreducible, ALPHA-SEAM) —
  injectivity forbids a class-C reading; invariant content=exact residue pair; row
  unchanged.`

### T3-18. D0-BRANCH-CP-READOUT-NOGO-V15 (csv:506) — cell **B-ext** (REUSED)
- **Decisive sentence (verbatim, csv:506):** "branch commutant>C*I (3 blocks); same
  marginals, different coherence. Missing PRIM-BRANCH-ISOTROPIC-READOUT."
- **Filing REUSED from the gauge memo v2.1** (EoR-8, the skeptic-#2-forced re-file): "≥ 2
  admissible readouts differing on invariant content (coherence), with the resolution typed
  as a missing primitive ⇒ freedom wall, class **B-ext** (Continent 2, parallel to
  CKM-OVERLAP) — moved out of Continent 3."
- **Moduli object:** coherence-readout choices over the 3-block branch commutant.
  **Acting group:** the block-commutant unitary freedom (>ℂ·I). Group is derived from the
  frozen carrier — owned-as-family.
- **Invariant content (survives):** the marginals (identical across readouts); the 3-block
  commutant structure.
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=coherence readouts over the 3-block branch commutant; gauge-fixing=B-ext:
  PRIM-BRANCH-ISOTROPIC-READOUT (typed missing primitive); invariant content=marginals +
  commutant structure; filing reused from TORSOR_GAUGE_SYNTHESIS_MEMO v2.1 EoR-8 re-file;
  row unchanged.`

### T3-19. D0-P1-PHYSICAL-EOS (csv:508) — cell **B-ext** (sibling instance)
- **Decisive sentence (verbatim, csv:508):** "same total response, distinct w=p/rho.
  Missing PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT."
- **Moduli object:** pressure/energy role split at fixed total response — the SAME role
  freedom as E3/WZ-TRANSFER-role (one missing primitive, three consumer rows).
  **Acting group:** role-orientation swap. FLAG: declared-by-construction.
- **Border criterion:** distinct w = p/ρ at same total response ⇒ alternatives DIFFER ⇒
  freedom wall.
- **D-vs-C:** un-owned split; values differ ⇒ B; typed missing primitive ⇒ **B-ext**.
  UPLIFT_MAP:187's "sibling instance of P1-C role torsor (candidate corollary tag under
  it)" is accepted for the SIBLING structure but re-pointed: the parent for the corollary
  tag should be the ROLE-freedom object (shared PRIM), NOT P1-C itself (which this memo
  files Continent-3, T3-15).
- **Invariant content (survives):** the total response; firewall "No 1+z=phi^n, no
  rho=e^u-1".
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=pressure/energy role split at fixed total response; gauge-fixing=B-ext:
  PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT (shared with csv:470/312); invariant
  content=total response; sibling corollary parent = the shared role-freedom object, not
  P1-C (Continent 3); row unchanged.`

### T3-20. D0-LEPTON-BRANCH-ROW-MINIMAL-EXTENSION-001 (csv:516) — cell **C** (consistent with R4)
- **Decisive sentence (verbatim, csv:516):** "B_row ('point 0 in size-4 orbit') is
  NECESSARY (separates sigmaA/sigmaB) but NOT sufficient alone -- over the full admissible
  class (420 order-12 cycle-type-(4,3) perms of Fin 7) B_row passes 240, not 1
  (sigmaA,sigmaC both pass)."
- **Moduli object:** the orbit-labeling refinement C(7,4)=35 → 1 of the R4 assignment
  torsor; B_row = one bit (35→20). **Acting group:** S₇-conjugation (as R4 — owned).
- **Border criterion + D-vs-C:** all 420 admissible perms share cycle type (4,3), order 12,
  resolvent invariants — surviving alternatives (σA, σC) are S₇-conjugate, AGREEING on all
  class-A content ⇒ each additional labeling bit is a point-refinement on the OWNED
  shell-torus torsor with no class-A change ⇒ **class C** (gauge-fixing bits; ~5.13 bits
  total per UPLIFT_MAP:188). Consistent with the R4 Continent-1 reuse (T3-6); NOT a
  contradiction with the row's "the SUFFICIENT row-fixing operator
  (=PRIM-LEPTON-BRANCH-FIXING-OPERATOR)" clause — that clause types the INTERNAL
  non-derivability of the bits (the 549-analog), not the class of the datum itself; and
  L4 (csv:491) proves the generation-ROW impossible in-carrier by cardinality (2<3), which
  is the Continent-3 half, filed with L4, not here.
- **Invariant content (survives):** cycle type (4,3) source-forced; resolvent invariants;
  B_row necessity (separates σA/σB) as a computed fact.
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  moduli=orbit-labeling refinement C(7,4)=35 of the R4 assignment torsor (B_row = 1 bit,
  35->20); gauge-fixing=C: S7-conjugation point-refinement on the owned shell-torus torsor
  (surviving alternatives conjugate, no class-A change); invariant content=(4,3) type,
  resolvent invariants, B_row necessity; generation-row half stays Continent 3 with L4;
  row unchanged.`

### T3-21. D0-ARCHIVE-LAPLACIAN-PHASE-NATURALITY (csv:39) — **BLOCKED-ON-READING** (M2/G_res 3-way)
- **Decisive sentence (verbatim, csv:39):** "Naturality alone does not uniquely fix the
  operator without further phase structure."
- **Moduli object (candidate):** operator-phase structure on the archive Laplacian.
  **Acting group:** UNDECLARED by the row — and this is the blocker: the natural candidate
  group is the detector-layer phase/labeling group whose residual G_res is exactly the
  un-adjudicated 3-way reading (M2_PHASE_LABELING_MEMO A3, OPEN; gauge memo X-L1 rungs
  below S₈ are reading-conditional).
- **Border criterion:** CANNOT BE RUN from the row's content — no witness pair, no
  invariant computation, no admissible-set structure is exhibited in the registry note
  (sparse early-format row, no cert, no EXACT-MISSING). Whether the phase alternatives
  AGREE (⇒ insufficiency, Continent 3) or DIFFER (⇒ freedom; then C if the phase torsor is
  the owned detector-layer object, B-adj if it reduces to the ω₀-bit/G_res adjudication)
  depends on which phase structure is meant — i.e. on the M2 3-way.
- **Filed:** **blocked-on-reading** (§6). Do NOT force a cell; the gauge memo's own C2
  precedent ("class flips with the open reading") applies.
- **Notes-text (conditional):** `UPLIFT[2026-07-06]: filing BLOCKED on the M2/G_res 3-way
  adjudication (phase-structure moduli, acting group undeclared; cell flips
  C/B-adj/Continent-3 with the reading); revisit after M2 A3 closes; row unchanged.`

### T3-22. D0-SCENE-HISTORY-REFINEMENT-RULE-OWNER-001 (H3, csv:490) — cell **B-ext** (same object as T3-9/10)
- **Decisive sentence (verbatim, csv:490):** "All-walks (Perron 21.84, depth-2 15708) and
  non-backtracking (Perron 20.83, 14990) are independently-generated, admissible,
  inequivalent refinement towers (refined operators NOT L_n:=J L_scene C)."
- **Filing:** the SAME refinement-family moduli as T3-9/T3-10 (UPLIFT_MAP:190 itself notes
  "single object, two registrations" — with csv:437/439 it is actually THREE
  registrations). Alternatives DIFFER (Perron, carrier counts) ⇒ freedom; missing
  PRIM-SCENE-HISTORY-REFINEMENT-RULE ⇒ **B-ext**.
- **Invariant content (survives):** "No-phi^3 holds in both (min-successor 19)"; no forced
  CMB window (policing).
- **Notes-text:** `UPLIFT[2026-07-06]: instance-of the organizing lemma (reading layer);
  same refinement-family moduli as csv:437/439 (third registration); gauge-fixing=B-ext:
  PRIM-SCENE-HISTORY-REFINEMENT-RULE; invariant content=no-phi^3 both towers
  (min-successor 19) [WITNESS-ONLY + ANSATZ-CLASS-CONDITIONAL — two inspected towers, not
  the whole admissible class; named watch-item §6.4, do not promote downstream]; row
  unchanged.`

---

## §3 W3 — B-cluster remainder (3 rows not already filed in §2)

The B-cluster (UPLIFT_MAP, 7+1) = {ALPHA-PRESENT-CORE, CMB-CANONICAL (=T3-1),
PHASON-MAGNITUDE (=T3-2), HIGGS-CONDENSATION, CKM-OVERLAP (=T3-3), TORAL-SEED (=T3-4),
LEPTON-PUISEUX (=T3-5), INDUCTIVE-SPECTRAL-TRIPLE}. Five are filed in §2; the three
remaining:

### B-1. D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001 (csv:403) — **Continent 3 (existence), NO B/C/D cell**
- **Decisive sentence (verbatim, csv:403):** "for ANY a<=2, rate(a)<1 => Summable =>
  trace-class => log-Cesaro/Dixmier coefficient 0 != mu_2=12288/5; and rate(3)=1 exactly
  (critical 1/j line) <=> carrier Perron eigenvalue phi^3, which 5-fold symmetry + M1
  forbid (single golden rate phi). No admissible present-core tower realizes mu_2."
- **Border criterion:** quantified over ALL admissible present-core towers; the admissible
  set of μ₂-realizing towers is EMPTY ⇒ **existence wall, Continent 3**. The organizing
  lemma is silent. Consistent with UPLIFT_MAP:77's T2 re-class (⚠SEED there): wall ⇒
  principle territory (P-SUBCRIT mint), a SEPARATE uplift track from this memo's four-cell
  filing — no B/C/D cell is assigned, and P-SUBCRIT must not be conflated with either
  P-GAUGE-STRUCTURAL or the organizing lemma.
- **Invariant content (survives):** rate(a)=φ^(a−3); the a∈{0,1} present-core supply; the
  interface fork (external Dixmier passport OR new φ³ carrier extension).
- **Notes-text:** `UPLIFT[2026-07-06]: Continent-3 EXISTENCE wall (empty admissible set of
  mu_2-realizing present-core towers) — organizing lemma silent, NO B/C/D cell; uplift
  track = P-SUBCRIT mint (T2, separate); completion fork stays typed (Dixmier passport
  B-ext-shaped OR phi^3-carrier extension); row unchanged.`

### B-2. D0-HIGGS-CONDENSATION-PRESENT-CORE-MAXIMALITY-NOGO-001 (csv:407) — **Continent 3 (existence), NO B/C/D cell** (REUSED)
- **Decisive sentence (verbatim, csv:407):** "every present-core frozen projector is a
  polynomial a*1+b*T in the return operator T (theorem tPoly_commutes) and commutes with T
  => constant orbit => no double-well => no condensation."
- **Filing REUSED from the gauge memo** (Continent-3 table: "no non-commuting present-core
  projector exists — empty admissible set (PRIM-NONCOMMUTING-TRIPLE)"). Empty admissible
  set ⇒ existence wall; lemma silent. UPLIFT_MAP:80's T2 re-class (P-ABELIAN mint) is the
  separate uplift track.
- **Invariant content (survives):** tPoly_commutes; the non-commuting witness Qnc exists
  but is NOT present-core (the wall is sharp, not vacuous); completion class
  PRIM-NONCOMMUTING-TRIPLE.
- **Notes-text:** `UPLIFT[2026-07-06]: Continent-3 EXISTENCE wall (empty admissible set of
  non-commuting present-core projectors; completion class PRIM-NONCOMMUTING-TRIPLE) —
  organizing lemma silent, NO B/C/D cell; filing reused from TORSOR_GAUGE_SYNTHESIS_MEMO
  v2.1 Continent-3; uplift track = P-ABELIAN mint (separate); row unchanged.`

### B-3. D0-INDUCTIVE-SPECTRAL-TRIPLE-OWNER-001 (csv:414, PROOF-TARGET, in nogo_flags) — **Continent 3 (existence), NO B/C/D cell**
- **Decisive sentence (verbatim, csv:414):** "a Dirac-compatible ISOMETRIC inductive
  spectral triple (J_N^dag J_N=I AND J_N^dag D_(N+1) J_N = D_N) is NOT present-core: the
  corpus realizes the tower as an INVERSE limit of downward projections".
- **Border criterion:** the blocking slot is the isometric J_N; the present-core admissible
  set is EMPTY (only downward projections exist) ⇒ existence wall, Continent 3. UPLIFT_MAP:84's
  T4-candidate ("read tower contravariantly: downward conditional expectations ARE the
  object (co-tower)") is a DISSOLUTION candidate for the wall, not a four-cell filing —
  compatible: if the T4 forge succeeds, the row leaves Continent 3 by re-reading, not by a
  gauge-fixing datum.
- **Invariant content (survives):** the algebra-level Bratteli tower (incidence M_phi,
  Fibonacci dims, csv:412 positive owner); the firewall to
  ASSUMP-CONNES-RECONSTRUCTION/propinquity passports.
- **Notes-text:** `UPLIFT[2026-07-06]: Continent-3 EXISTENCE wall (empty present-core set
  of isometric Dirac-compatible J_N; tower realized as inverse limit) — organizing lemma
  silent, NO B/C/D cell; T4 co-tower forge is the dissolution candidate (UPLIFT_MAP:84);
  row unchanged (PROOF-TARGET, not among the 84).`

---

## §4 Counts per cell

**W1 A-cluster (8 rows; four-cell N/A — organizing lemma silent on all 8):**

| filing | count | rows |
|---|---|---|
| corollary-of:P-GAUGE-STRUCTURAL (whole row) | 7 | csv:79, 80, 81, 83, 89, 94, 96 |
| per-leg split (P-CAPACITY ×2 + P-M1-FIREWALL ×1 + P-GAUGE-STRUCTURAL ×1) | 1 | csv:120 (STRESS-SUITE) |
| instance-of organizing lemma | **0** | — (wave seeding rejected, §5 D-1) |

**W3 four-cell filing (22 T3 rows + 3 B-cluster remainder = 25 filings; WZ-TRANSFER split
counts once in B-ext by its role leg):**

| cell | count | rows |
|---|---|---|
| **C** (owned-torsor gauge-fixing) | **2** | R4 (csv:463), BRANCH-ROW (csv:516) |
| **B-meas** | **2** | CMB-CANONICAL (csv:404), PHASON-MAGNITUDE (csv:405) |
| **B-adj** | **0** | — (no registry no-go row in scope is adjudication-resolved; the B-adj items of the gauge memo are non-row objects: G_res reading, moment convention, ω₀-bit, staticity clause) |
| **B-ext** | **15** | CKM-OVERLAP (406), TORAL-SEED (408, borderline-flagged), E3 (470), MARTINGALE-DIRAC (422), VNEXT2-REF-OWNER (437), VNEXT2-REF-NOGO (439), VNEXT2-DIRAC-COV (446), EDGE-COVER (509), HYPERCHARGE-VARIETY (361), G2 (489), WZ-TRANSFER role-leg (312), ALPHA-RESIDUE-DELTA (354), BRANCH-CP (506), P1-EOS (508), H3 (490) — 15 registrations over **11 distinct moduli objects**: refinement-family = ONE object, THREE registrations (437/439/490); role-freedom = ONE object, THREE consumers (470, 312-role-leg, 508) — E3's role(2)×cocycle(2) 4-torsor is counted as the shared role object PLUS a tick-cocycle bit riding the same filing, NOT a distinct moduli object (convention stated here once; the Dirac-scale cocycle freedom at 422/446 remains a separate object under PRIM-DIRAC-SCALE-SELECTION) |
| **D** (un-owned ansatz) | **0** | — the sole D-witness in the corpus stays the ρ=cos(π/9) cyclic-order import (row 544 consumer, per gauge memo D1); NO W3 row files D (verified row-by-row: no row injects a family-canonical invariant from un-owned structure — they either change values per point (B) or change nothing (C)) |
| **Continent 3** (lemma silent, no cell) | **5 (+1 leg)** | LEPTON-PUISEUX (352), P1-C (492), ALPHA-PRESENT-CORE (403), HIGGS-CONDENSATION (407), INDUCTIVE-SPECTRAL-TRIPLE (414); + WZ-TRANSFER SEP-leg (312) |
| **blocked-on-reading** | **1** | ARCHIVE-LAPLACIAN-PHASE-NATURALITY (csv:39) |

Arithmetic check (22 T3 rows): C = {463, 516} (2) + B-meas = {404, 405} (2) + B-ext =
{406, 408, 470, 422, 437, 439, 446, 509, 361, 489, 312-role-leg, 354, 506, 508, 490} (15)
+ Continent-3 = {352, 492} (2) + blocked = {39} (1) → 2+2+15+2+1 = 22 ✓. Row 312 is counted
exactly once (in B-ext, by its role leg); its SEP leg is a leg-level Continent-3 annotation,
not a second row count. B-cluster remainder 3 rows (403, 407, 414) → all Continent 3.
Total: 25 W3 filings + 8 A-cluster filings = 33 objects, each filed exactly once.

---

## §5 Disagreement roster (⚠DISAGREE — content forced a different filing than seeded)

- **D-1 (roster-level, W1):** the wave seeding "file the A-cluster no-gos as corollaries of
  the within-zone gauge ORGANIZING LEMMA" is REJECTED for all 8 rows: none is
  freedom-shaped; all file under P-GAUGE-STRUCTURAL (+P-CAPACITY/P-M1-FIREWALL for
  stress-suite legs). Filing them under the organizing lemma would conflate the two
  principles the task itself orders kept distinct. (§1)
- **D-2 (LEPTON-PUISEUX, csv:352):** UPLIFT_MAP T3 seed rejected; Continent-3 insufficiency
  per the border criterion (companions AGREE on charpoly) — reuses the gauge memo's own
  EoR-8 re-check. (T3-5)
- **D-3 (EDGE-COVER, csv:509):** "λ = gauge-fixing datum" is wrong-cell: the separator is
  INJECTIVE, so the choice is content-bearing ⇒ B-ext, not C. The "cleanest torsor" reading
  survives only as family-structure, not as a gauge license. (T3-12)
- **D-4 (systematic, 4 rows):** UPLIFT_MAP's T3 vocabulary uses "gauge-fixing datum" for
  external trivialization data on UN-OWNED moduli (MARTINGALE-DIRAC csv:422,
  ALPHA-RESIDUE-DELTA csv:354, E3 csv:470 "DE data = gauge", VNEXT2-DIRAC-COV csv:446 by
  inheritance). Under the four-cell test all are B-ext: class C is reserved for owned
  torsors with zero class-A change. The word "gauge" is struck from all four notes-texts.
- **D-5 (P1-C, csv:492):** UPLIFT_MAP T3 role-torsor seed rejected; the row's own content
  is an EMPTY admissible intertwiner set ⇒ Continent-3 existence wall; the role freedom
  lives on siblings 470/312/508. (T3-15)
- **D-6 (TORAL-SEED, csv:408, borderline — filed B-ext, flagged):** owned dynamical
  invariants AGREE across witnesses (Continent-3 reading available) while symbolic-model
  invariants differ (freedom reading); filed B-ext on the alternatives'-own-content reading
  + the corpus's ASSUMP-ADLER-WEISS typing, with the tension recorded for the owner. (T3-4)
- **D-7 (P1-EOS, csv:508, re-pointing):** UPLIFT_MAP's "corollary tag under P1-C" is
  re-pointed to the shared role-freedom object (the missing
  PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT), since P1-C itself files Continent 3. (T3-19)

---

## §6 Blocked-on-reading (M2/G_res 3-way adjudication needed before final filing)

1. **D0-ARCHIVE-LAPLACIAN-PHASE-NATURALITY (csv:39)** — the only W3 row whose CELL flips
   with the open reading: acting group undeclared; the candidate group is the
   detector-layer phase structure whose residual G_res is the un-adjudicated 3-way (M2
   memo A3 OPEN; gauge memo X-L1 reading-conditional rungs). Cell flips
   C / B-adj / Continent-3. Do not file until M2 A3 closes.
2. *(leg-level, not a row)* Any future refinement of the **BRANCH-ROW (csv:516)** filing
   below the S₈ rung — the class-C verdict holds at S₇-conjugation, but if a finer
   G_res-conditional labeling layer is invoked (gauge memo C2 precedent: "class flips with
   the open reading"), the additional bits inherit the 3-way condition.
3. *(watch-item)* **A4-fingerprint consumers**: no W3 row consumes the ω₀-bit directly, but
   any integration step that cites the tick fingerprint signs must carry the gauge memo's
   "A conditional on B-adj(ω₀-bit)" marking (EoR-7).
4. *(watch-item — the roster's one live D-shadow)* **no-φ³ across refinement families
   (csv:437/439/490)**: the "no-φ³ holds in both (min-successor 19)" fact is WITNESS-ONLY
   (two inspected towers) and ANSATZ-CLASS-CONDITIONAL — it is constant across the inspected
   family points yet conditional on the refinement-rule class the scene does not own, i.e.
   it has the SHAPE of a family-canonical invariant (the class-D signature) if ever promoted
   to a whole-class statement. As long as it stays a per-witness computed fact inside B-ext
   filings it is safe; any downstream consumer promoting it to "no-φ³ for ALL admissible
   refinements" must re-run the D-test first (per-filing discipline of gauge memo risk R1':
   cite the owner row declaring the structure un-owned). Named here so no integration step
   promotes it silently.

---

## §7 Ranked highest-value notes-texts (top 10)

1. **CKM-OVERLAP (csv:406, B-ext)** — the corpus's own extension-typed row, Lean-proved
   witness pair; anchors the whole B-ext sub-type. (T3-3)
2. **R4 (csv:463, C)** — the flagship class-C filing outside the selector row itself:
   assignment freedom = owned-torsor gauge bit, computed (script C3), with the
   Continent-3 counting half cleanly severed. (T3-6)
3. **EDGE-COVER (csv:509, B-ext)** — the sharpest wrong-cell catch (injective separator
   kills the "gauge datum" reading); protects falsifier 4 from a false positive. (T3-12)
4. **Refinement-family consolidation (csv:437/439/490, B-ext)** — ONE moduli object, THREE
   registrations, one missing primitive; the cross-links turn three scattered no-gos into
   one typed freedom with computed invariant content (no-φ³ both towers, gap 2|E|=718). (T3-9/10/22)
5. **ALPHA-RESIDUE-DELTA (csv:354, B-ext)** — ties the canonization freedom to the proven-
   irreducible ASSUMP-DIXMIER-TRACE owner-edge; hardest-typed import in the roster. (T3-17)
6. **Role-freedom consolidation (csv:470/312/508, B-ext)** — one missing primitive
   (PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT), three consumers, with P1-C correctly
   severed to Continent 3. (T3-7/16/19, D-5/D-7)
7. **STRESS-SUITE per-leg split (csv:120)** — four Lean legs to three principles without
   touching the row; the cleanest registry-hygiene gain in W1. (A8)
8. **HYPERCHARGE-VARIETY (csv:361, B-ext)** — the only B-ext whose trivialization bridge
   ALREADY EXISTS (BL-DIRECTION, ASSUMP-KERNEL-CHARGE-LOCALIZATION); wiring it closes the
   F7 story as moduli+bridge with the question-begging alternative policed by the row
   itself. (T3-13)
9. **BRANCH-ROW (csv:516, C)** — turns a corrected over-claim into a clean bit-accounting
   of the class-C datum (B_row = 1 of ~5.13 gauge-fixing bits), with the
   missing-PRIM-vs-cell disambiguation now explicit (precedent
   ASSUMP-WITHINZONE-LABELING-EXTERNAL); protects the C-cell from B-ext creep. (T3-20)
10. **TORAL-SEED (csv:408, B-ext, border-tension recorded)** — the roster's live test case
    for the border criterion itself (owned invariants agree / model invariants differ);
    the recorded tension is the input the owner needs to sharpen the criterion's
    "invariant content" clause — a criterion-hardening gain beyond the single row. (T3-4, D-6)

---

## §8 Skeptic pass — verdict and repairs log

**Skeptic:** ONE independent general-purpose agent, focused mandate: (Part 1) verify six
row-filings against primary sources (spanning A-cluster, both class-C rows csv:463 + 516,
one B-meas, one B-ext, one Continent-3 relocation); (Part 2) hunt ONE misfiled row — the
ρ=cos(π/9) class-D-vs-C sin specifically (an un-owned-ansatz import filed as contentless
gauge), prime suspects csv:516, csv:408, csv:463 run through the D-test verbatim ("new =
new relative to class A; family = the ansatz class, compared across classes").

**VERDICT: ACCEPT-WITH-REPAIRS — none cell-changing. Part-2 D-hunt: NO-KILL** (no W3 row
files C or B-ext while injecting a family-canonical invariant from un-owned structure; the
sole corpus D-witness remains the row-544 cyclic-order consumer, exactly as §4 claims). The
class-D count of 0 STANDS, with one D-shadow named as a watch-item (repair 5 → §6.4).

**Repairs demanded and APPLIED (5, logged):**
1. §4 B-ext table count corrected 14 → **15** (header/list mismatch; the 15-member list was
   already correct).
2. §4 distinct-moduli count corrected 12 → **11**, with the counting convention stated
   explicitly: E3's role(2)×cocycle(2) 4-torsor is counted as the shared role object plus a
   tick-cocycle bit riding the same filing, not a distinct object; the "×3 consumers"
   parenthetical is reconciled (470, 312-role-leg, 508).
3. T3-6 (csv:463): the row's own "EXACT-MISSING: PRIM-LEPTON-BRANCH-FIXING-OPERATOR" is now
   surfaced in the body AND the notes-text, carrying the T3-20 disambiguation clause (the
   PRIM types INTERNAL non-derivability of the bits, not the datum's cell; precedent:
   ASSUMP-WITHINZONE-LABELING-EXTERNAL → class C in the gauge memo §Consequence).
4. T3-15 (csv:492) notes-text precision: "empty admissible intertwiner set" → "empty
   admissible set of canonical/eigenvalue-matching intertwiners" (the row does not claim no
   maps exist — it claims no CANONICAL one does).
5. T3-9/T3-22 notes-texts: "no-φ³ (min-successor 19)" is now marked WITNESS-ONLY +
   ANSATZ-CLASS-CONDITIONAL and registered as named watch-item §6.4 (the roster's one live
   D-shadow) so no downstream consumer promotes it to a whole-class invariant without
   re-running the D-test.

**Post-repair state:** all six Part-1 verifications CONFIRM after repairs; no cell changed
anywhere in §§1-3; counts in §4 are final as printed. The memo is ready as W1/W3
integration input. `053040` untouched throughout; no registry/book/cert/lean file modified —
this memo remains the only artifact.
