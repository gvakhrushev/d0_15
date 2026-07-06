# D0 CORPUS-WIDE UPLIFT SWEEP — W0 MASTER MAP

Date: 2026-07-05. Task: classify EVERY negative-status object by uplift class.
READ-ONLY sweep — no registry rows were touched; this file is the only artifact.

## Inputs (frozen at read time)

- Registry `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` — 545 claim rows:
  **84 no-gos** (76 NO-GO + 8 NO_GO_PROVED), 29 rows with `uses_bridge_assumptions=True`
  (39 bridge-shaped rows incl. CORE_BRIDGE_SPLIT×8 + BRIDGE-CALIBRATION×3), **28 passports**
  (20 PASSPORT-CLOSED + 8 EMPIRICAL-PASSPORT).
- `03_THEORY_MAP/frontier_dag.json` `nogo_flags` (11 kind-tagged entries: wall / witness_pair / unclassified).
- Atlases: `04_VERIFICATION/D0_FINAL_NO_GO_ATLAS.md` (8 entries, "proved:" + "admissible completion class:"),
  `04_VERIFICATION/VNEXT2_SCENE_NATIVE_NO_GO_ATLAS.md` (3 entries), `04_VERIFICATION/TOTAL_NO_GO_ATLAS.md`
  (54 cert-backed routes), `04_VERIFICATION/POSTCORE_NOGO_STRENGTH_AUDIT.md` (E1–E5 strength classes).

## The rubric (validated taxonomy, applied per object)

- **T1 Obstruction=Equation** — the no-go COMPUTES a specific nonzero quantity; uplift = identify what the quantity IS (owned-typed). Pilot: div G_A2 = 4·deg = capacity coupling.
- **T2 Wall=Principle** — universal structural impossibility; uplift = invert into a defining property. Pilot: selector no-go → M1-derived gauge principle.
- **T3 Choice-freedom=Torsor/moduli** — witness-pair underdetermination; the degenerate manifold IS the object; the free parameter = gauge-fixing data (measured input).
- **T4 Missing-object=Decomposition** — the "absent" object is a constituent of an owned structure read differently. Pilot: {D₂,ABCD} = layers of Q₈'s central extension.
- **T5 Boundary=Interface** — honest external import → I/O-spec entry (input: measurement/gauge-fixing; output: invariants).
- **T6 Redundancy=Corollary** — instance of a principle → `corollary-of:<principle>` tag (hierarchy only; rows NOT deleted).
- **(в) GENUINE-BOUNDARY** — legitimately stays a boundary; no forced uplift.
- **AMBIGUOUS→sweep-frontier** — needs a dedicated forge before classification is honest.

Priorities: **H** = feeds books/headline architecture; **M** = registry hygiene; **L** = cosmetic.

## Seed-cluster reconstruction note (read before the tables)

The seed clustering (A×8→T6-gauge, B×8→T3, J×10→T1, C+E+F+I×16→T4-or-boundary, D+H×12→T5,
G×5→case-by-case) totals ~59 objects; the registry holds 84 no-gos. Reconstruction used here:
**A** = gauge-sector no-gos (8); **B** = D0_FINAL_NO_GO_ATLAS members (7 of the 84 + 1 flagged
PROOF-TARGET); **J** = ROOT R1–R5 + Post-core E1–E4 + G_A2 (10); **C/E/F/I** = vNext/vNext+1/vNext+2
AF-tower family (**18 actual, not 16** — seed miscount, flagged); **D/H** = external-interface
no-gos (10 clean members found, not 12 — two seeds land in G-residue); **G-residue** = everything
else (**31 objects**, far beyond the seeded ×5). Every membership was verified against the object's
actual "proved:" content; **9 seed disagreements** are flagged inline with `⚠SEED`.

Verdict-line format per object:
`claim_id | shape | T-class | uplift candidate (≤15 words) | priority`

---

## Cluster A — gauge-sector no-gos (8) [seed: T6(gauge) — CONFIRMED 7/8, 1 flag]

The seven pure-gauge rows are all instances of one principle already implicitly owned:
**P-GAUGE**: *finite gauge structure requires the graded incidence carrier + an associative
matrix representation + the symmOffDiag projection; every ungraded/flat/bare shortcut fails.*

| claim_id | shape | T-class | uplift candidate | prio |
|---|---|---|---|---|
| D0-NO-GO-BARE-ARCHIVE-NONABELIAN-001 | absence (bare archive lacks nonabelian completion) | T6 | corollary-of:P-GAUGE (matrix-rep leg) | M |
| D0-NO-GO-EDGE-STIFFNESS-SCALAR-LEAKAGE-001 | computed (scalar diagonal leaks without projection) | T6 | corollary-of:P-GAUGE (projection leg) | M |
| D0-NO-GO-FLAT-TENSOR-NONABELIAN-001 | computed (flat tensor of two skews is symmetric) | T6 | corollary-of:P-GAUGE (grading leg) | M |
| D0-GAUGE-BIANCHI-RESIDUAL-BOUNDARY-001 | computed (flat ungraded residual exact; graded Bianchi closed) | T6 | corollary-of:P-GAUGE (graded-Bianchi leg) | M |
| D0-NO-GO-ABSTRACT-LIERING-FINITE-TRANSFORM-001 | wall (unstateable in bare LieRing) | T6 | corollary-of:P-GAUGE (associativity leg) | M |
| D0-NO-GO-NAIVE-LOCAL-GAUGE-COVARIANCE-001 | witness (Fin 3 counterexample) | T6 | corollary-of:P-GAUGE (negative control exhibit) | L |
| D0-NO-GO-UNGRADED-BIANCHI-RESIDUAL-001 | witness (Fin 2 counterexample) | T6 | corollary-of:P-GAUGE (negative control exhibit) | L |
| D0-NO-GO-STRESS-SUITE-001 | 4-leg suite (mixed) | T6 ⚠SEED | SPLIT: 4 legs tag to 3 DIFFERENT principles (see below) | M |

⚠SEED (stress suite): not purely gauge. Its four Lean legs distribute across principles:
isolated-phason generation + isolated-phason baryon-S3 → corollary-of:**P-CAPACITY** (a lone
phason lacks the coupling capacity); Euclidean signature export → corollary-of:**P-M1-FIREWALL**
(nonreversibility forbids signature flip); rank-one Higgs projector → corollary-of:**P-GAUGE**
(rank-2 is the minimal gauge-compatible mask). Uplift = registry tags per-leg, row kept intact.

## Cluster B — Final-Atlas maximality no-gos (7 of the 84 + 1 flagged extra) [seed: T3 — CONFIRMED 5/8, 2 walls re-classed T2, 1 T4-candidate]

These carry explicit "admissible completion class" lines — the completion class IS the uplift
object in every case. The two `kind: wall` entries in frontier_dag.json are NOT torsors and
invert into principles instead (⚠SEED flags).

| claim_id | shape | T-class | uplift candidate | prio |
|---|---|---|---|---|
| D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001 | wall (every admissible tower trace-class) | **T2** ⚠SEED | mint P-SUBCRIT: present-core growth is golden-subcritical (rate φ^(a−3)<1, a≤2) | H |
| D0-CMB-CANONICAL-SMOOTHING-MAXIMALITY-NOGO-001 | moduli (3 weightings, 3 tilts) | T3 | smoothing-measure (k,u) moduli; gauge-fixing datum = Planck-comparison passport | H |
| D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001 | witness_pair (two maps, same sign+anchor) | T3 | magnitude-map moduli anchored at −φ; DESI/CPL passport = gauge fixing | H |
| D0-HIGGS-CONDENSATION-PRESENT-CORE-MAXIMALITY-NOGO-001 | wall (every present-core projector is poly-in-T) | **T2** ⚠SEED | mint P-ABELIAN: present-core is T-commutative; noncommutativity lives in extension layers | H |
| D0-CKM-OVERLAP-UNDERDETERMINATION-NOGO-001 | witness_pair (3-4-5 vs 5-12-13, 16/25≠144/169) | T3 | basis-completion torsor; Cabibbo measurement = the gauge-fixing datum | H |
| D0-TORAL-SEED-MARKOV-MAXIMALITY-NOGO-001 | moduli (2-rect and 3-rect share Perron φ) | T3 | Markov-partition moduli; Adler-Weiss passport choice = gauge fixing | M |
| D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001 | witness_pair (two companions, one charpoly) | T3 | companion-operator fiber over branch index; Green-resolvent certificate = gauge fixing | M |
| D0-INDUCTIVE-SPECTRAL-TRIPLE-OWNER-001 *(PROOF-TARGET, not among the 84; in nogo_flags)* | obstruction (only downward projections exist) | T4-candidate | read tower contravariantly: downward conditional expectations ARE the object (co-tower) | M |

⚠SEED (both walls): frontier_dag.json itself tags these `kind: wall`, and the proved lines
quantify over ALL admissible completions — that is principle territory (T2), not witness-pair
territory (T3). The T3 seeds fit the other five exactly.


## Cluster J — ROOT R1–R5 + Post-core E1–E4 + G_A2 (10) [seed: T1 — CONFIRMED 6/10, 4 flags]

The quantity-computing heart of the corpus. Verified against each "proved:" content: six
genuinely compute an ownable quantity; R4 is an assignment torsor, E3 is a role torsor with
its quantity ALREADY identified, E4 is a decomposition candidate.

| claim_id | shape | T-class | uplift candidate | prio |
|---|---|---|---|---|
| D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001 (R1) | computed (commutant dim 12 = 3²+1+1+1) | T1 | commutant M3⊕C⊕C⊕C IS the flavor-frame bundle (GL(3) generation freedom) | H |
| D0-ARCHIVE-CONTRACTION-NOGO-001 (R2) | computed (archive spectrum {24,22,20}; rescale 2\|E\|=718) | T1 | the obstructing rescale 718 IS the edge-capacity coupling constant | H |
| D0-SCENE-NATIVE-MULTISCALE-TOWER-NOGO-001 (R3) | computed (Perron ≥ 718/33 > φ³) | T1 | 718/33 IS the capacity density; obstruction = capacity-vs-golden-rate gap | H |
| D0-LEPTON-BRANCH-SELECTOR-MAXIMALITY-NOGO-001 (R4) | computed type + free assignment (420-perm class) | **T3** ⚠SEED | cycle-type (4,3) forced (T1-done); assignment = torsor, branch label = gauge datum | H |
| D0-ALPHA-LOG-CESARO-MEASURABILITY-NOGO-001 (R5) | computed (limit = 1/(3 ln φ), transcendental ≠ 12288/5) | T1 | 1/(3 ln φ) IS the golden information rate — the capacity unit alpha lives against | H |
| D0-POSTCORE-REPRESENTATION-EXTENSION-NOGO-001 (E1) | computed form + 2 completions (nc = p²+q²+3 ∈ {8,12}) | T1 (+T3 residue) | nc IS the grading-signature quadratic form on the M3 block | H |
| D0-POSTCORE-HISTORY-REFINEMENT-MAXIMALITY-NOGO-001 (E2) | computed (15708 − 14990 = 718 = 2\|E\| exactly) | T1 | the family gap IS exactly the edge capacity — the backtracking-capacity term | H |
| D0-POSTCORE-PHASON-EXTENSION-MAXIMALITY-NOGO-001 (E3) | computed disjointness + 4-torsor (role×cocycle) | **T3** ⚠SEED | quantity already owned (√10 fingerprint); remaining freedom = role torsor, DE data = gauge | H |
| D0-POSTCORE-LEPTON-SELECTOR-MAXIMALITY-NOGO-001 (E4) | wall-ish (circularity; 2 orbits < 3 generations) | **AMBIGUOUS→sweep** ⚠SEED | is the missing 3rd branch a central-extension layer? (T4 forge, w/ L4) | H |
| D0-A2-EINSTEIN-DIVERGENCE-OBSTRUCTION-NOGO-001 | computed (div G_A2 = 4·deg = {96,88,80}) | T1 | **PILOT (validated)**: divergence IS capacity coupling; conserved object = G=2L | H |

Note (E1/E2 strength audit): POSTCORE_NOGO_STRENGTH_AUDIT.md classes E1/E3 CLASS-SCOPED and
E2/E4 TWO-COMPLETION-WITNESS-ONLY — none is a universal impossibility, which is exactly why
the T1 quantity-identification uplift (not a wall-inversion) is the right move here.

## Cluster C/E/F/I — vNext / vNext+1 / vNext+2 AF-tower family (18, seed said 16 ⚠SEED miscount) [seed: T4-or-boundary — SPLIT: 2×T4, 4×T3, 8×T6, 3×boundary, 1×T1]

One story told 18 times: the AF/Fibonacci tower is a correct FORMALISM object that is NOT
the scene's inductive completion. The honest uplift is (i) T4 where the tower is read as its
own constituent, (ii) T3 where families/scales form moduli, (iii) T6 for the corollary fan-out,
(iv) GENUINE-BOUNDARY for the anti-numerology capstones.

| claim_id | shape | T-class | uplift candidate | prio |
|---|---|---|---|---|
| D0-VNEXT-MARTINGALE-DIRAC-OWNER-001 | witness_pair (φ^N vs 2^N scales) | **T3** ⚠SEED | Dirac-scale cocycle torsor; scale law = gauge-fixing datum | M |
| D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY-OWNER-001 | structural mismatch (dims 2,5,13,34 skip 33; opposite directions) | T4 | AF tower = independent owned layer (formalism constituent), not a scene refinement | M |
| D0-VNEXT-ISOMETRIC-DIRAC-TOWER-NOGO-001 | decomposition (1 primitive splits into 2) | T4 | literal decomposition: PRIM-ISOMETRIC-J_N = scale-selection ⊕ comparison-map layers | M |
| D0-VNEXT-33-SCENE-ANCHOR-OWNER-001 | typed coincidence (34 vs 33) | GENUINE-BOUNDARY | none — anti-numerology stands; 34−1=33 is NOT a quotient | M |
| D0-VNEXT-AF-ONE-DIMENSIONAL-REDUCTION-CLASSIFICATION-001 | computed ((24,8,1) ≠ (9,11,13); 2 blocks ≠ 3 parts) | GENUINE-BOUNDARY | none — honest structural mismatch | L |
| D0-VNEXT-CANONICAL-XI-ANCHOR-OWNER-001 | absence (no canonical χ) | T6 | corollary-of:AF-reduction mismatch + spectral obstruction | L |
| D0-VNEXT-JOINT-DIRAC-SCALE-SELECTION-OWNER-001 | absence (no anchored matching) | T6 | corollary-of:anchor no-go | L |
| D0-VNEXT-AF-D0-SPECTRAL-COMPRESSION-OWNER-001 | computed ({1,3,8,21} ≠ {1,2,8,10,12}, 4≠5) | T1 | multiplicity fingerprints ARE typed separators (Fibonacci increments vs degree multiplicities) | M |
| D0-VNEXT-33-SCENE-ANCHOR-NOGO-001 | capstone (double obstruction) | T6 | corollary-of:44+48 (anchor-owner + spectral compression) | L |
| D0-VNEXT-JOINT-DIRAC-ANCHOR-NOGO-001 | capstone (primitives stay independent) | T6 | corollary-of:anchor no-go (independence statement) | L |
| D0-VNEXT2-SCENE-NATIVE-REFINEMENT-OWNER-001 | moduli (families W/NB/E inequivalent) | T3 | refinement-family 3-point moduli; history rule = gauge-fixing datum | M |
| D0-VNEXT2-TRIPARTITE-PATH-TOWER-OWNER-001 | family-dependence | T6 | corollary-of:refinement-family moduli | L |
| D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001 | witness_pair (15708 vs 14990) | T3 | same moduli, registered witness pair; Ihara-Bass/Bartholdi coords already certified | M |
| D0-VNEXT2-SCENE-XI-INTERTWINER-OWNER-001 | family/measure dependence | T6 | corollary-of:refinement-family moduli | L |
| D0-VNEXT2-XI-MAXIMALITY-NOGO-001 | maximality restatement | T6 | corollary-of:refinement-family moduli (Ξ leg) | L |
| D0-VNEXT2-DIRAC-COVARIANCE-MAXIMALITY-NOGO-001 | moduli (cocycles differ across families) | T3 | scale-cocycle torsor fibered over refinement moduli | M |
| D0-VNEXT2-SCENE-NATIVE-MAXIMALITY-OWNER-001 | capstone | T6 | corollary-of:refinement-family moduli (conjunction) | L |
| D0-VNEXT2-SCENE-NATIVE-CLOSURE-BOUNDARY-001 | closure boundary (downstream gates stay closed) | GENUINE-BOUNDARY | none — the gate-keeping statement is the value | M |

⚠SEED (cluster level): actual family size is 18, not 16; and the dominant honest class inside
is T3/T6 (moduli + corollary fan), with only 2 clean T4 reads. The "T4-or-boundary" seed holds
for the vNext Fast-Track trio + capstones, not for the vNext+2 rows.


## Cluster D/H — external-interface no-gos (10 clean members; seed said 12 ⚠SEED) [seed: T5 — CONFIRMED 8/10, 2 demoted to T6]

Each is an honest external import whose uplift is a typed I/O-spec entry: INPUT (measurement /
gauge-fixing / matching scheme) → OUTPUT (owned invariants the core guarantees).

| claim_id | shape | T-class | uplift candidate | prio |
|---|---|---|---|---|
| D0-GRAV-QNM-001 | absence (no preregistered inputs) | T5 | I/O: in = preregistered model + modes table; out = δ₀ overtone-ladder check | M |
| D0-GEN-MASS-001 | boundary (index proved, masses external) | T5 | I/O: in = Yukawa/PDG scheme; out = generation index 3 + clustering invariants | M |
| D0-SRC-NOGO-001 | witness (Ca/Fe shell contact defeats A-only, N/Z-only) | T5 | I/O: in = shell-structure datum beyond (A, N/Z); out = SRC contact scalars | M |
| D0-CVFT-F1 | computed (residue ∝ 1/ln φ transcendental ≠ Q(φ)) | T5 | I/O: in = ASSUMP-LINDEMANN + Dixmier owner; out = μ1=1/3, μ2=2¹²·(3/5), form forced | H |
| D0-NOGO-LIGO-DISCOVERY-001 | negative-control freeze (V3–V12) | T5 | I/O: in = discovery-scan protocol; out = proxy-promotion block (negative control) | M |
| D0-LEPTON-RAW-GRAPH-COEFFICIENT-OWNER-001 | skeleton forced, coefficient external | T5 | I/O: in = EFT/IR matching (m_μ); out = L11+L4=206, exponents (0,¼,⅓), order 12 | H |
| D0-BARE-GRAPH-DECIMAL-NOGO-001 | absence (direct raw→decimal M1-forbidden) | **T6** ⚠SEED | corollary-of:LEPTON-RAW-GRAPH owner (direct-route instance of the general boundary) | M |
| D0-PHASON-WDE-Z-MAP-OWNER-001 | composite (all 4 sub-pieces settled) | T5 | already interface-shaped; formalize the 4-slot I/O decomposition as the registry template | M |
| D0-LEPTON-DECIMAL-MASS-RATIOS | computed (Vandermonde det=1/144 ≠ 0 ⇒ any pair realizable) | T5 | I/O: in = PRIM-EFT-IR-MATCHING-FUNCTIONAL; out = exponent-row realizability theorem | M |
| D0-COLOUR-GENERATION-TYPED-CARRIER-NOGO-001 | computed (commutant 8<9; typed collapse to diagonal) | T5 | I/O: in = external ⊗C³ (octonion/E8 terminal-passport owners); out = zones=generations | H |

Demotion note: BARE-GRAPH-DECIMAL is subsumed by the RAW-GRAPH-COEFFICIENT owner (the owner
row itself states it "lifts the DIRECT-route NO-GO to the GENERAL owner level") — tag T6 under
the owner's T5 interface rather than a second interface entry. COLOUR row confirms the standing
terminal-passport reading (colour is NOT scene-derived); the uplift formalizes it, no promotion.

## Cluster G + residue — case-by-case (31; seed ×5 vastly under-counted ⚠SEED)

The seed clustering covered ~61/84. This bucket holds the lanes (G2/H3/L4/P1-C), the v15/v16
WP rows, the alpha rows, firewall suites, and singletons. Each classified individually.

### G.1 Torsor/moduli reads (T3) — 12

| claim_id | shape | T-class | uplift candidate | prio |
|---|---|---|---|---|
| D0-EDGE-COVER-FAMILY-001 | U(1) λ-family, injective separator −λ | T3 | **cleanest torsor in corpus**: holonomy U(1)-torsor; λ = gauge-fixing datum | H |
| D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001 | computed (rank 3 ⇒ 3-dim space ⊃ span{Y, B−L}) | T3 | hypercharge 2-dim charge-moduli; ν_R-charge datum = gauge fixing (bridge EXISTS: BL-DIRECTION) | H |
| D0-GRADING-NEUTRAL-CURRENT-MAXIMALITY-NOGO-001 (G2) | witness_pair (nc 8 vs 12, both admissible) | T3 | grading-signature torsor on M3 block; measured neutral-current content = gauge fixing | H |
| D0-PHASON-PRESSURE-ENERGY-MAXIMALITY-NOGO-001 (P1-C) | class-scoped (no typed common sector) | T3 | pressure-energy role torsor; observed w(z) = gauge fixing; √10 leg → T6 P-TYPED | H |
| D0-PHASON-WZ-TRANSFER-OWNER-001 | witness_pair (w_A≈0.900 ≠ w_B≈1.111) + SEP | T3 | role-orientation torsor; SEP leg = corollary-of:P-TYPED (field disjointness) | H |
| D0-CMB-NS-SMOOTHING-UNDETERMINED-NOGO-001 | witness_pair (tilt varies in k and weighting) | T6 | corollary-of:M2 maximality sibling (superseded as evidence, kept as instance) | M |
| D0-ALPHA-RESIDUE-DELTA-NORMALIZATION-NOGO-001 | computed residue + free normalization | T3 | canonization torsor; Dixmier-pairing passport = the 2nd-canonization gauge datum | M |
| D0-BRANCH-CP-READOUT-NOGO-V15 | witness (3-block commutant; same marginals) | T3 | coherence-readout torsor over branch commutant; isotropic readout = gauge datum | M |
| D0-P1-PHYSICAL-EOS | witness (same response, distinct w=p/ρ) | T3 | sibling instance of P1-C role torsor (candidate corollary tag under it) | M |
| D0-LEPTON-BRANCH-ROW-MINIMAL-EXTENSION-001 | computed (B_row passes 240/420, one bit of 35→1) | T3 | orbit-labeling moduli C(7,4)=35; B_row = 1 gauge-fixing bit (of ~5.13) | M |
| D0-ARCHIVE-LAPLACIAN-PHASE-NATURALITY | wall-ish (naturality insufficient) | T3 | operator-phase moduli; phase structure = gauge-fixing data | M |
| D0-SCENE-HISTORY-REFINEMENT-RULE-OWNER-001 (H3) | witness_pair (W 21.84/15708 vs NB 20.83/14990) | T3 | refinement-family torsor (same moduli as vNext2 cluster; single object, two registrations) | M |
| D0-CKM-CLASS5-PARITY-EXCLUSION-001 | computed degeneracy (sel(5)=sel(1)) | T6 | corollary-of:Z5-aliasing owner (substantive exclusion lives there) | M |

(CMB-NS and CKM-CLASS5 sit in this table for adjacency but carry T6 verdicts; net T3 here = 11.)

### G.2 Wall→principle reads (T2) — 2 + the pilot

| claim_id | shape | T-class | uplift candidate | prio |
|---|---|---|---|---|
| D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001 | wall (0 Aut-invariant labelings; SSB relocates catalog) | T2 | **PILOT (validated)**: mint P-GAUGE-M1 — within-zone labels are gauge, M1-derived | H |
| D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001 | wall (Aut transitive on 1287 triangles; 5→1 pigeonhole) | T6 | corollary-of:P-GAUGE-M1 (role-attachment instance of the selector principle) | H |
| D0-GRAPH-SPACE-NO-ISOMETRY-001 | wall (anisotropic norms, trivial zone symmetry) | T2 | mint P-MECH-LIMIT: graph→space isotropization is a mechanism limit, never an identity | M |

### G.3 Quantity reads (T1) — 2

| claim_id | shape | T-class | uplift candidate | prio |
|---|---|---|---|---|
| D0-REHEATING-NO-INFLATON-NOGO-001 | computed (threshold = 718/33, no tunable) | T1 | SAME quantity as R3: 718/33 = capacity density as threshold energy — unify | H |
| D0-DIXMIER-FESHBACH-FINITE-HEATTRACE-001 | computed (no pole; a₀ = 30 = dim) | T1-done | quantity already identified (archive dimension); tag corollary-of:P-CAPACITY count | M |

### G.4 Corollary reads (T6) — 9

| claim_id | shape | T-class | uplift candidate | prio |
|---|---|---|---|---|
| D0-GENERATION-RAYS-001 | dead route (index owned elsewhere) | T6 | corollary-of:projective branch-defect index (GEN-INDEX owner) | L |
| D0-CVFT-NOGO-001 | firewall suite (mirror/ideal-gas/refits forbidden) | T6 | corollary-of:P-M1-FIREWALL (no-refit discipline instances) | M |
| D0-PHASON-WZ-KERNEL-ONLY-NOGO-001 | wall (an integer cannot fix a function) | T6 | corollary-of:P-TYPED (arity/type discipline instance) | M |
| D0-ISING-ANYON-EXCLUSION-001 | computed (3 simple objects > 2 eigenbranches) | T6 | corollary-of:degree-2 toral dichotomy (p+p²=1 two-branch principle) | M |
| D0-HIGGS-PHASON-ORBIT-TRIVIAL-NOGO-001 | wall (commuting orbit constant) | T6 | corollary-of:P-ABELIAN (superseded by M3 maximality sibling) | M |
| D0-TORAL-CANONICAL-MARKOV-PARTITION-NOGO-001 | absence (partition not seed-determined) | T6 | corollary-of:M4 maximality sibling + Adler-Weiss passport | M |
| D0-ALPHA-PROFINITE-TOWER-NOGO-001 | computed (rate φ^(a−3) summable ⇒ Dixmier 0) | T6 | corollary-of:P-SUBCRIT (the M1 maximality generalizes it) | M |
| D0-RAW-SELF-READING-EXTRACTIONS-001 | 4-terminal composite (G2/C4/L3/P3) | T6 | per-terminal corollary tags to the four lane owners; row kept | M |
| D0-ARCHIVE-REGULAR-REFINEMENT-NOGO-001 | computed (359/160 ≠ 1) | T6 | corollary-of:P-TYPED (window-scale/contraction fingerprint instance) | M |
| D0-STURMIAN-REFINEMENT-DISCHARGE-NOGO-001 | computed (√10 ∉ Q(√5); trace −1 vs +1) | T6 | corollary-of:P-TYPED (discriminant fingerprint) + orientation invariant | M |

(G.4 = 10 rows; plus CMB-NS + CKM-CLASS5 carrying T6 in the G.1 table and DSIGMA-ROLE in G.2
→ net T6 verdicts in the residue = 13.)

### G.5 Boundary + ambiguous — 1 + 2

| claim_id | shape | T-class | uplift candidate | prio |
|---|---|---|---|---|
| D0-ALPHA-SEAM-REALIZATION-NOGO-001 | 8-pass-hardened composite (valuation: 5 ramifies in Z[φ]; μ2=2¹²ρ tautology) | GENUINE-BOUNDARY | none — ASSUMP-DIXMIER-TRACE proven irreducible; 4 reopening hooks already named | H |
| D0-PHASE-TOWER-002 | computed-ish (recursion stabilizes at shell two) | AMBIGUOUS→sweep | is shell-2 stabilization depth an ownable capacity quantity (T1) or honest terminal (в)? | M |
| D0-LEPTON-BRANCH-FIXING-OPERATOR-OWNER-001 (L4) | wall (Gen(3)↔Branch(2) impossible by cardinality, no fixed point) | AMBIGUOUS→sweep | joint forge with E4: is the missing 3rd branch a central-extension/trivial-isotype layer (T4)? | H |


## The 8 conditional bridge-owners [all T5 by construction — owner-edges ARE interface entries]

Identified as the eight singleton-ASSUMP owner-edge rows (Iter6/7/18). Uplift for the whole
block: promote from prose "owner-edge" notes to typed I/O-spec entries with explicit
input/output columns; none is promotable to core.

| claim_id | assumption | shape | T-class | uplift candidate | prio |
|---|---|---|---|---|---|
| D0-CONNES-RECONSTRUCTION-OWNER-001 | ASSUMP-CONNES-RECONSTRUCTION | external owner (metric=Dirac spectrum) | T5 | I/O: in = Connes reconstruction; out = finite metric tower reading | M |
| D0-DIXMIER-RESIDUE-OWNER-001 | ASSUMP-DIXMIER-TRACE | external owner (residue extraction) | T5 (irreducible) | I/O entry; ALPHA-SEAM proves this import irreducible in present-core | H |
| D0-RIEFFEL-GHP-CONTINUUM-OWNER-001 | ASSUMP-RIEFFEL-GHP | external owner (finite→smooth convergence) | T5 | I/O: in = GHP framework; out = golden-Cauchy bound consumer | M |
| D0-TIME-MODULAR-FLOW-OWNER-001 | ASSUMP-TOMITA-TAKESAKI | external owner (time=modular flow) | T5 | I/O: in = Tomita-Takesaki; out = thermal-time reading of tick | M |
| D0-ADLER-WEISS-PARTITION-OWNER-001 | ASSUMP-ADLER-WEISS | external owner (Markov partitions) | T5 | I/O entry; doubles as the gauge-fixing PROVIDER for the toral T3 torsor | M |
| D0-COMPLEX-QM-FORCING-001 | ASSUMP-COMPLEX-QM | external axiom owner (complex vs real QM) | T5 | I/O entry; keep — survived mechanism filter; pairs with real-quotient passport | M |
| D0-M1-INFO-RECONSTRUCTION-001 | ASSUMP-M1-INFO-RECONSTRUCTION | external owner of M1 itself | T5 | I/O entry; NOTE: P-GAUGE-M1 (T2 pilot) hangs from this import — make edge explicit | H |
| D0-ENTROPIC-DARK-GRAVITY-001 | ASSUMP-VERLINDE-ENTROPIC | cross-bridge (Verlinde) | T5 (flagged) | I/O entry + honesty flag: SPARC dark-matter comparison FAILED — scope the output claims down | M |

Adjacent conditional rows (beyond the 8, same treatment, listed for completeness):
D0-FROBENIUS-DIVISION-3D-001 (ASSUMP-FROBENIUS-1877, T5), D0-LATTICE-FINITENESS-BRIDGE-001
(ASSUMP-WILSON-LATTICE-1974, T5), D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001
(ASSUMP-KERNEL-CHARGE-LOCALIZATION, T5 — and the designated GAUGE-FIXING datum for the
hypercharge T3 torsor), the three Clay M1-reductios (HODGE/RIEMANN-AXIS/PVSNP — T5,
conditional reductios, GENUINE-BOUNDARY posture), and the ASSUMP-LINDEMANN-LNPHI family
(CVFT-F1, R5, E5/POSTCORE-DIXMIER-WODZICKI, ALPHA-ANALYTIC-FORMALISM, RAW-ALPHA-ANALYTIC,
X5-ALPHA — one shared import, six consumers: candidate single I/O node with 6 corollary edges).

## Load-bearing passports (12 audited of 28) [T5-done unless flagged]

Passports are already interface objects; the uplift is wiring them as the NAMED gauge-fixing
providers of specific T3 torsors (right column), turning "external comparison" into typed
torsor-trivialization data.

| claim_id | status | T-class | pairs with (torsor / role) | prio |
|---|---|---|---|---|
| D0-EXTERNAL-DIXMIER-WODZICKI-PASSPORT-001 | PASSPORT-CLOSED | T5-done | R5/α-tower wall: the sanctioned external realization of μ2 | H |
| D0-FINITE-SPECTRAL-TRIPLE-REPRESENTATION-PASSPORT-001 | PASSPORT-CLOSED | T5-done | R1 flavor-frame bundle (T1): NCG representation consumer | H |
| D0-HYPERCHARGE-FLOW-ORIGIN-PASSPORT-001 | PASSPORT-CLOSED | T5-done | hypercharge T3 torsor (with BL-DIRECTION bridge as gauge fixing) | H |
| D0-PHASON-WZ-CPL-PASSPORT-001 | PASSPORT-CLOSED | T5-done | DE magnitude T3 torsor gauge-fixer; honesty: DESI confirms EVOLVING only, not the corner | H |
| D0-ADLER-WEISS-WILLIAMS-PASSPORT-001 | PASSPORT-CLOSED | T5-done | toral Markov T3 torsor gauge-fixer | M |
| D0-SMOOTH-QUANTUM-METRIC-PASSPORT-001 | PASSPORT-CLOSED | T5-done | golden refinement tower interface (algebra level) | M |
| D0-SMOOTH-MANIFOLD-FORMALISM-PASSPORT-001 | PASSPORT-CLOSED | T5-done | finite→continuum boundary (with GHP owner-edge) | M |
| D0-NEUTRINO-MASS-PASSPORT-001 | PASSPORT-CLOSED | T5-done | seam-frozen P_sterile interface | M |
| D0-PMNS-DELTA0-NUFIT-001 | EMPIRICAL-PASSPORT | GENUINE-BOUNDARY | none — post-hoc/not discriminating (coefficient freedom); do NOT uplift; stays empirical | M |
| D0-ALPHA-MEASUREMENT-LIMIT-001 | EMPIRICAL-PASSPORT | T5-done | measurement-band interface for the last ~1e-8 α layer | M |
| D0-HORIZON-HUM-EMPIRICAL-PASSPORT-001 | PASSPORT-CLOSED | T5-done | pre-registered I_f=log φ residual test (keep pre-registration discipline) | M |
| D0-PASSPORT-PDG-STRICT-001 | EMPIRICAL-PASSPORT | T5-done | comparison engine (pinning/holdout/multiple-testing) — template for all T5 I/O entries | M |


---

# SYNTHESIS

## (a) Counts per T-class (the 84 no-gos; bridge-owners and passports tallied separately)

| class | count | members (abbreviated) |
|---|---|---|
| T1 Obstruction=Equation | **10** | R1, R2, R3, R5, E1, E2, A2-pilot, AF-SPECTRAL-COMPRESSION, REHEATING, DIXMIER-FESHBACH(T1-done) |
| T2 Wall=Principle | **4** | ALPHA-PRESENT-CORE, HIGGS-CONDENSATION, SELECTOR-pilot, GRAPH-SPACE-NO-ISOMETRY |
| T3 Torsor/moduli | **22** | CMB-CANONICAL, PHASON-MAGNITUDE, CKM-OVERLAP, TORAL-SEED, LEPTON-PUISEUX, R4, E3, MARTINGALE-DIRAC, VNEXT2-REFINEMENT-OWNER, VNEXT2-REFINEMENT-NOGO, VNEXT2-DIRAC-COVARIANCE, EDGE-COVER, HYPERCHARGE-VARIETY, G2, P1-C, WZ-TRANSFER, ALPHA-RESIDUE-DELTA, BRANCH-CP, P1-EOS, BRANCH-ROW, ARCHIVE-LAPLACIAN-PHASE, H3 |
| T4 Decomposition | **2** | VNEXT-DIRAC-LAPLACIAN-COMPAT, VNEXT-ISOMETRIC-DIRAC-TOWER (+1 flagged PROOF-TARGET: INDUCTIVE-SPECTRAL-TRIPLE) |
| T5 Interface | **9** | QNM, GEN-MASS, SRC, CVFT-F1, LIGO, LEPTON-RAW-COEFF, WDE-Z-MAP, LEPTON-DECIMAL, COLOUR |
| T6 Corollary | **30** | gauge×8, BARE-GRAPH-DECIMAL, vNext corollary fan×8, CMB-NS, CKM-CLASS5, DSIGMA-ROLE, G.4×10 |
| (в) GENUINE-BOUNDARY | **4** | ALPHA-SEAM, 33-ANCHOR-OWNER, AF-ONE-DIM-REDUCTION, VNEXT2-CLOSURE-BOUNDARY |
| AMBIGUOUS→sweep | **3** | E4, L4, PHASE-TOWER-002 |
| **Total** | **84** | ✓ every registry NO-GO / NO_GO_PROVED row classified exactly once |

Bridge-owners: 8×T5 (2 High: DIXMIER irreducible, M1-INFO as P-GAUGE-M1 anchor).
Passports audited: 11×T5-done + 1 GENUINE-BOUNDARY (PMNS-DELTA0 — post-hoc, stays empirical).
Grand total objects classified: **104** (+1 flagged PROOF-TARGET).

## (b) Proposed PRINCIPLE LIST (everything hangs from seven statements)

Five were named in the rubric seeds; **two are NEW mints proposed by this sweep (P-SUBCRIT,
P-TYPED)** — both fall out of walls/fingerprints that recur across ≥4 rows each.

1. **P-GAUGE-M1** (gauge/selector; T2 pilot mint). *Aut(K)=S9×S11×S13 is within-zone
   transitive and M1 admits no legal symmetry-breaking rule ⇒ every within-zone label, role
   attachment, and assignment is gauge.* Roster: CANONICAL-WITHIN-ZONE-SELECTOR (mint),
   DSIGMA-ROLE-CYCLE, CKM-CLASS5-PARITY, R1's Weyl-freedom leg, R4/E4 assignment freedom —
   and it GROUNDS the existence of all 22 T3 torsors (each torsor = one gauge orbit).
2. **P-CAPACITY** (capacity-coupling; T1 pilot). *Degree/edge counts ARE the coupling
   quantities: what blocks conservation/contraction/criticality is always a capacity term.*
   Instances: div G_A2 = 4·deg (pilot); R2 rescale 718; R3 & REHEATING 718/33; E2 gap = 2|E|;
   heat-trace a₀ = 30; stress-suite isolated-phason legs.
3. **P-SUBCRIT** (NEW mint, from the ALPHA-PRESENT-CORE wall). *Every present-core carrier
   grows at golden rate ≤ φ; per-block rate φ^(a−3) < 1 ⇒ trace-class ⇒ ordinary Dixmier
   limit 0; the critical φ³ carrier is M1-forbidden.* Roster: ALPHA-PRESENT-CORE (mint),
   ALPHA-PROFINITE-TOWER, R5's critical-rate reading, R3 (shared with P-CAPACITY).
4. **P-ABELIAN** (central-extension-layers; T4 pilot's parent). *Present-core is
   T-commutative — every frozen projector is polynomial in T; all noncommutative structure
   lives in central-extension layers ({D₂,ABCD} = Q₈ layers, pilot).* Roster:
   HIGGS-CONDENSATION (mint), HIGGS-PHASON-ORBIT, the E4+L4 third-generation forge target.
5. **P-R1-COMMUTANT** (R1-commutant). *Commutant dim 12 = M3⊕C⊕C⊕C is the flavor-frame
   bundle; every generation/grading/branch structure is a frame choice on the M3 block.*
   Roster: R1 (mint), E1, G2, BRANCH-CP-READOUT, the R4/L4 assignment legs.
6. **P-TYPED** (NEW mint: typed-carrier / field-fingerprint separation). *Owned carriers
   carry typed invariants — number field (Q(√5) vs Q(√10)), integer-vs-window spectra,
   multiplicity fingerprints, arity — and no canonical intertwiner crosses a type boundary.*
   Roster: STURMIAN-DISCHARGE, ARCHIVE-REGULAR-REFINEMENT, WZ-KERNEL-ONLY, WZ-TRANSFER
   SEP-leg, E3/P1-C incommensurability, AF-SPECTRAL-COMPRESSION, 33-ANCHOR posture,
   COLOUR typed collapse.
7. **P-M1-FIREWALL** (M1-nonreversibility). *External data may trivialize a torsor
   (gauge-fix); it may never mutate a core shape — no refits, mirrors, signature exports,
   or decimal back-reads.* Roster: CVFT-NOGO suite, stress-suite Euclidean leg,
   BARE-GRAPH-DECIMAL, the entire passport discipline (T5 column).

## (c) Sweep-frontier (AMBIGUOUS — need a dedicated forge each)

1. **E4 + L4 third-generation forge** (highest value): 2 branch orbits < 3 generations, no
   in-carrier fixed point. T4 hypothesis to force or kill: the missing third branch is the
   trivial-isotype / central-extension layer (P-ABELIAN ∩ P-R1-COMMUTANT). NOTE the standing
   third-generation NO-GO — the forge must be adversarial, not promotional.
2. **PHASE-TOWER-002**: is shell-2 stabilization depth an ownable capacity quantity (T1
   under P-CAPACITY) or an honest terminal (в)?
3. **STRESS-SUITE split**: mechanically split 4 legs into per-principle corollary tags
   (P-CAPACITY ×2, P-M1-FIREWALL, P-GAUGE) without touching the row.
4. **E1 signature form**: is nc = p²+q²+3 an owned quadratic-form invariant on the M3 block
   (full T1) or merely a count (stays T3 residue)?
5. **INDUCTIVE-SPECTRAL-TRIPLE co-tower** (PROOF-TARGET, flagged): T4 read of the downward
   conditional-expectation system as the object itself.

## (d) Genuine-boundary roster (honestly stays; no uplift forced)

- **D0-ALPHA-SEAM-REALIZATION-NOGO-001** — eight-pass-hardened; ASSUMP-DIXMIER-TRACE proven
  irreducible in present-core; reopening only via its 4 named hooks.
- **D0-VNEXT-33-SCENE-ANCHOR-OWNER-001** + **D0-VNEXT-AF-ONE-DIMENSIONAL-REDUCTION-
  CLASSIFICATION-001** — the 34≠33 anti-numerology stands.
- **D0-VNEXT2-SCENE-NATIVE-CLOSURE-BOUNDARY-001** — downstream gates stay closed; the
  gate-keeping IS the content.
- **D0-PMNS-DELTA0-NUFIT-001** — post-hoc, non-discriminating; stays EMPIRICAL-PASSPORT.
- **ASSUMP-LINDEMANN-LNPHI** import (6 consumers) — one honest classical fact, never core.
- Colour **⊗C³** import (octonion/E8 terminal-passport owners), lepton **17-digit decimals**
  (EFT/IR), **DE magnitude map** (external by M2), the three **Clay reductios** — all
  interface-shaped forever under P-M1-FIREWALL.

## Top-10 highest-value uplift candidates beyond the 5 pilots

1. **R5 → 1/(3 ln φ)** is the golden information rate — the alpha wall becomes a computed capacity unit (T1, H).
2. **E2 → family gap = 2|E| exactly** — the refinement underdetermination IS the backtracking-capacity term (T1, H).
3. **R3 + REHEATING → 718/33** capacity density: one quantity, two independent theorems — unify under P-CAPACITY (T1, H).
4. **R1 → commutant M3⊕C³ = flavor-frame bundle**; mint P-R1-COMMUTANT and hang the E1/G2/BRANCH-CP roster from it (T1→principle, H).
5. **EDGE-COVER → U(1) holonomy torsor** — cleanest torsor in the corpus; λ = THE electromagnetic gauge-fixing datum (T3, H).
6. **HYPERCHARGE variety → span{Y, B−L} charge moduli** with the EXISTING ν_R bridge as gauge fixing — closes the F7 story honestly as torsor+interface (T3+T5, H).
7. **ALPHA-PRESENT-CORE → mint P-SUBCRIT** and re-tag PROFINITE-TOWER/R5-rate as corollaries (T2, H).
8. **HIGGS-CONDENSATION → mint P-ABELIAN**, wiring the Q₈ central-extension T4 pilot to the named Higgs F6 missing object (T2→T4, H).
9. **R2 → rescale 718 = capacity coupling** of the archive contraction — the "unwitnessable" contraction becomes a typed capacity statement (T1, H).
10. **P-TYPED mint** — one new principle absorbing 8-9 scattered fingerprint rows (√10, 359/160, arity, multiplicities) into a single corollary roster (T2+T6, H/M).

*End of W0 master map. No registry rows were modified; all uplift candidates are proposals
pending the adversarial forcing loop (per-candidate forge → skeptic pass → registry motion).*

