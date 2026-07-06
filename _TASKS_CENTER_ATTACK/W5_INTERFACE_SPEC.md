# W5 — BOUNDARY = INTERFACE: THE D0 I/O SPECIFICATION (T5 consolidation)

Date: 2026-07-06. Wave W5 of the corpus-wide uplift sweep (rubric T5 of
`_TASKS_CENTER_ATTACK/UPLIFT_MAP.md`). READ-ONLY consolidation: no registry row, book,
or Lean file was modified; this file (+ `w5_interface_check.py`) is the only artifact.

Sources (frozen at read time):
- `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` — 545 rows; 29 `uses_bridge_assumptions=True`
  (28 LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS + 1 PYTHON_CERTIFIED), 8 CORE_BRIDGE_SPLIT,
  3 BRIDGE-CALIBRATION; 1 overlap (D0-CARRIER-003 is both True and CORE_BRIDGE_SPLIT)
  → **39 unique bridge-shaped rows** (matches UPLIFT_MAP header).
- `09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv` — 24 assumption entries with
  Lean names, files, justifications, failure meanings.
- `04_VERIFICATION/EXTERNAL_ASSUMPTION_REGISTRY.csv` — 26 assumption entries (type/status).
- `_TASKS_CENTER_ATTACK/UPLIFT_MAP.md` (cluster D/H, bridge-owners, passports sections);
  `_TASKS_CENTER_ATTACK/M1QM_RATE_ENERGY_MEMO.md` (Λ_act ownership chain).

Method discipline: every row claim below was verbatim-checked against the CSV; every
assumption text is quoted from `LEAN_ASSUMPTION_LEDGER.csv` (justification column) or the
named Lean file. This wave asserts NO new physics; mismatches are FLAGGED, not fixed.

---

## 0. TAXONOMY DRIFT FLAG (read first)

The task brief's "6 ASSUMP types" (HST-EXTERNAL, RG-SMOOTH-INTERP, LORENTZ-MACRO,
SMOOTH-COVARIANCE, SMOOTH-HEATTRACE, HURWITZ-GOLDEN) are exactly the six carried by the
aggregate row `D0-LEAN-BRIDGE-001` — the ORIGINAL bridge block. The corpus has since grown:

| source | distinct ASSUMP ids |
|---|---|
| CLAIM_TO_LEAN_MAP.csv `assumption_ids` column | **22** |
| LEAN_ASSUMPTION_LEDGER.csv | **24** (adds ASSUMP-JONES-INDEX, ASSUMP-MORDELL-E8 — consumed by NO CSV row) |
| EXTERNAL_ASSUMPTION_REGISTRY.csv | **26** (adds ASSUMP-PRL-RQM-GENERAL, ASSUMP-NO-EXOTIC-FERMIONS, ASSUMP-LEPTON-EFT-DECIMALS — in neither ledger nor CSV) |

The 6-type block covers only **7 of the 29** True-rows (13 id-mentions: HST×4 + RG×2 +
LORENTZ×2 + SM-COV×2 + SM-HEAT×2 + HURWITZ×1). The remaining 22 rows carry 16
further assumption ids (8 singleton bridge-owners + FROBENIUS/WILSON/KERNEL-CHARGE +
LINDEMANN×7-consumers + 3 Clay internal targets + COMPACT-LIE-KILLING). Sections 1.A–1.D
below consolidate ALL of them; the three-source desync is FLAG-1 in the mismatch roster (§1.E).

---

## 1. ASSUMP CONSOLIDATION

### 1.0 Row enumeration (all 39 bridge-shaped rows, verbatim from CLAIM_TO_LEAN_MAP.csv)

**29 rows with `uses_bridge_assumptions=True`:**

| claim_id | lean_status | assumption_ids | release_status |
|---|---|---|---|
| D0-LEAN-BRIDGE-001 | LP_W_BA | HURWITZ-GOLDEN; RG-SMOOTH-INTERP; LORENTZ-MACRO; SMOOTH-COVARIANCE; SMOOTH-HEATTRACE; HST-EXTERNAL | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-QM-BORN-001 | LP_W_BA | HST-EXTERNAL | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-QM-BORN-002 | LP_W_BA | HST-EXTERNAL | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-CARRIER-003 | LP_W_BA | LORENTZ-MACRO | CORE_BRIDGE_SPLIT |
| D0-GAUGE-MATTER-001 | LP_W_BA | HST-EXTERNAL | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-RG-001 | LP_W_BA | RG-SMOOTH-INTERP | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-SMOOTH-001 | LP_W_BA | SMOOTH-COVARIANCE; SMOOTH-HEATTRACE | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-GAUGE-YANG-MILLS-KILLING-POSITIVITY-001 | LP_W_BA | COMPACT-LIE-KILLING-NEGATIVE | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-CVFT-F1 | LP_W_BA | LINDEMANN-LNPHI | NO-GO |
| D0-CONNES-RECONSTRUCTION-OWNER-001 | LP_W_BA | CONNES-RECONSTRUCTION | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-DIXMIER-RESIDUE-OWNER-001 | LP_W_BA | DIXMIER-TRACE | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-RIEFFEL-GHP-CONTINUUM-OWNER-001 | LP_W_BA | RIEFFEL-GHP | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-TIME-MODULAR-FLOW-OWNER-001 | LP_W_BA | TOMITA-TAKESAKI | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-ADLER-WEISS-PARTITION-OWNER-001 | LP_W_BA | ADLER-WEISS | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-COMPLEX-QM-FORCING-001 | LP_W_BA | COMPLEX-QM | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-M1-INFO-RECONSTRUCTION-001 | LP_W_BA | M1-INFO-RECONSTRUCTION | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-ENTROPIC-DARK-GRAVITY-001 | LP_W_BA | VERLINDE-ENTROPIC | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-FROBENIUS-DIVISION-3D-001 | LP_W_BA | FROBENIUS-1877 | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-LATTICE-FINITENESS-BRIDGE-001 | PYTHON_CERTIFIED | WILSON-LATTICE-1974 | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-HODGE-M1-REDUCTIO-001 | LP_W_BA | HODGE-ALGEBRAIC-FORCING | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-RIEMANN-AXIS-M1-001 | LP_W_BA | PACKAGING-REFLECTION-SYMMETRY | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-PVSNP-LYAPUNOV-M1-001 | LP_W_BA | GLOBAL-LYAPUNOV-POTENTIAL | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-ALPHA-LOG-CESARO-MEASURABILITY-NOGO-001 | LP_W_BA | LINDEMANN-LNPHI | NO-GO |
| D0-POSTCORE-DIXMIER-WODZICKI-PASSPORT-001 | LP_W_BA | LINDEMANN-LNPHI | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-POSTCORE-EXTENSION-BOUNDARY-001 | LP_W_BA | LINDEMANN-LNPHI | CERT-CLOSED |
| D0-ALPHA-ANALYTIC-FORMALISM-BOUNDARY-001 | LP_W_BA | LINDEMANN-LNPHI | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-RAW-ALPHA-ANALYTIC-RESIDUE-BOUNDARY-001 | LP_W_BA | LINDEMANN-LNPHI | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-X5-ALPHA-BOUNDARY-001 | LP_W_BA | LINDEMANN-LNPHI | BRIDGE-ASSUMPTIONS-EXPLICIT |
| D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001 | LP_W_BA | KERNEL-CHARGE-LOCALIZATION | BRIDGE-ASSUMPTIONS-EXPLICIT |

(LP_W_BA = LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS; ASSUMP- prefixes elided for width.)

**8 CORE_BRIDGE_SPLIT rows** (core half proved unconditionally; the split names what stays
bridge — these rows carry NO assumption_ids except CARRIER-003, listed above):

| claim_id | lean_status | what is core / what stays bridge (notes, abridged verbatim) |
|---|---|---|
| D0-CARRIER-003 | LP_W_BA | "Finite Clifford relation is core; Lorentz macro integration is bridge." |
| D0-INTERPRETATION-SPINE-001 | LEAN_PROVED | "SI readout uses one ExternalSICalibration without mutating core shape." |
| D0-GRAVITY-MACRO-EINSTEIN-INTERFACE-001 | LEAN_PROVED | "no continuum Einstein-Hilbert primitive is imported into core." |
| D0-TRACE-HEAT-CAPACITY-GRAVITY-001 | LEAN_PROVED | "macro gravity stays bridge-scoped through the finite witness." |
| D0-CVFT-F6 | LEAN_PROVED | "EXACT-MISSING: a gauge-boundary commutator obstruction theorem (external/PROOF-TARGET)." |
| D0-SPECTRAL-EINSTEIN-001 | LEAN_PROVED | owned = G=2L Laplacian-Bianchi conservation, "NOT the Einstein tensor" (G_A2 reconciliation). |
| D0-CRITICAL-COLLAPSE-001 | PYTHON_CERTIFIED | "The external result is CITED, not fetched/pinned" (Iter21 over-claim fixed). |
| D0-RANK3-CAUSAL-CONE-FORCING-001 | LEAN_PROVED | counting closure (3 real transport modes + 1 Pisot arrow ↔ Lorentzian (3,1)); signature reading stays interface. |

**3 BRIDGE-CALIBRATION rows** (the SI/measurement seam itself, typed):

| claim_id | lean_status | content (notes, abridged verbatim) |
|---|---|---|
| D0-BRIDGE-SI-CALIBRATION-BOUNDARY-001 | PYTHON_CERTIFIED | "c0/c2/G_N/H0 are bridge calibration symbols and cannot mutate core a0/a2 trace shapes." |
| D0-BRIDGE-SI-CALIBRATION-CLOSURE-001 | LEAN_PROVED | "D0 core computes dimensionless traces; H0/GN/Lambda require an explicit ExternalSICalibration object." |
| D0-HIGGS-CUBE-DIAGONAL-001 | PYTHON_CERTIFIED | "√2 forced & kept regardless; delta_loop is a NAMED-GAP … a BRIDGE needing external RG to evaluate exactly." |

### 1.A The six original bridge types — I/O contracts

Grades: **[MS]** mathematically-standard, **[PM]** physically-motivated, **[GO]** genuinely-open.

**ASSUMP-HST-EXTERNAL** — `D0/Bridge/Assumptions/ExternalHST.lean` (`ExternalHSTAssumptions`),
type PHYSICS_DICTIONARY. **[PM]**
- IMPORTED: the subgaussian → continuum-Gaussian convex-response comparison. Ledger [Iter19]:
  "D0 supplies the finite subgaussian source internally (bounded centered archive atom =>
  subgaussian MGF); the continuum-Gaussian convex-response comparison is the genuinely-external
  owner (the continuum Gaussian ensemble is not a D0 primitive)." BOOK_02 §02.22.2 confirms:
  "The continuum Gaussian ensemble is not primitive; it enters only through the external macro
  bridge after the finite archive source has been closed."
- LICENSES: the continuum readings of D0-QM-BORN-001/002 (finite Born skeleton → continuum
  Born comparison) and D0-GAUGE-MATTER-001, plus D0-LEAN-BRIDGE-001 aggregate. NOTE the
  Lean-side consumer of the structure is `convex_response_bridge_conditional`
  (`D0/Bridge/ConvexResponseBridge.lean`) — whose claim_id has NO registry row (FLAG-2).
- DISCHARGE: a formalized subgaussian-concentration / Gaussian-comparison theorem plus a D0
  construction of the continuum ensemble as a limit object — the latter is exactly the
  RIEFFEL-GHP residual, so this discharges only jointly with the continuum-limit front.
- Risk: physically-motivated (standard concentration mathematics, but the continuum ensemble
  is a physics dictionary choice).

**ASSUMP-RG-SMOOTH-INTERP** — `D0/Bridge/Assumptions/SmoothInterpolation.lean`, type
QFT_RG_BRIDGE. **[PM]**
- IMPORTED: "Continuous RG shadow requires declared smooth interpolation and scheme data."
- LICENSES: D0-RG-001 (`phi_rg_bridge_conditional`); failure meaning: "RG claim stays finite
  scale algebra only."
- DISCHARGE: none available — scheme data is genuinely external (matching-scheme choice);
  the honest posture is permanent-interface under P-M1-FIREWALL.

**ASSUMP-LORENTZ-MACRO** — `D0/Bridge/LorentzBridge.lean`, type MACRO_LIMIT. **[PM]**
- IMPORTED: "Spin/Lorentz macro integration is conditional beyond finite Clifford matrices."
- LICENSES: D0-CARRIER-003 (finite `clifford_relation` is core; the macro Lorentz reading is
  the licensed shadow) + aggregate. Downstream support: D0-RANK3-CAUSAL-CONE-FORCING-001
  closes the (3,1) COUNTING internally, which narrows but does not discharge this import.
- DISCHARGE: named missing theorem = macro Lorentz-group integration of the finite Clifford/
  graph carrier (the isotropization limit; blocked as an identity by
  D0-GRAPH-SPACE-NO-ISOMETRY-001 → P-MECH-LIMIT, so discharge can only be mechanism-level).

**ASSUMP-SMOOTH-COVARIANCE** — `D0/Bridge/SmoothMetricBridge.lean` (`CovarianceSystem`),
type SMOOTH_LIMIT. **[PM]**
- IMPORTED: "Smooth metric bridge requires covariance compatibility and nondegeneracy."
- LICENSES: D0-SMOOTH-001 (`smooth_metric_bridge_conditional`) + aggregate.
- DISCHARGE: jointly with ASSUMP-RIEFFEL-GHP (the finite→smooth convergence would produce
  the limit metric) + ASSUMP-CONNES-RECONSTRUCTION (identifies the limit as a spin manifold).
  See §2 incidence table.

**ASSUMP-SMOOTH-HEATTRACE** — `D0/Bridge/Assumptions/HeatTraceWeyl.lean`, type SMOOTH_LIMIT. **[PM]**
- IMPORTED: "Heat trace convergence/Weyl asymptotics/signature are bridge hypotheses."
- LICENSES: D0-SMOOTH-001 + aggregate; the a0/a2 trace-shape exports (which the
  BRIDGE-CALIBRATION rows prove CANNOT be mutated by calibration symbols).
- DISCHARGE: Weyl-asymptotics theorem for the D0 refinement tower — same joint front as
  SMOOTH-COVARIANCE.

**ASSUMP-HURWITZ-GOLDEN** — `D0/Bridge/Assumptions/Hurwitz.lean`, type PHYSICS_DICTIONARY. **[MS]**
- IMPORTED: "Full Hurwitz/golden worst-approximable theorem is not promoted to Core."
  (φ is the worst-approximable irrational; only finite core lemmas are in-tree.)
- LICENSES: only D0-LEAN-BRIDGE-001 carries it in the CSV; the operative class result is
  OWNED unconditionally by D0-PHI-HURWITZ-001 (LEAN_PROVED, CORE-FORMALIZED: "D0 admissible
  period-one quadratic phase class proved; full global Lagrange spectrum remains external").
- DISCHARGE: formalize the classical Hurwitz theorem (Mathlib-shaped work, no D0 content).
  Lowest-risk import in the six.

### 1.B The Lindemann family — one import, seven consumer rows

**ASSUMP-LINDEMANN-LNPHI** — `D0/Bridge/Assumptions/LindemannLnPhi.lean`, type
TRANSCENDENCE_THEOREM_LINDEMANN_WEIERSTRASS. **[MS]**
- IMPORTED (ledger verbatim): "Lindemann-Weierstrass: for an algebraic phi != 1, ln phi is
  transcendental over Q. Mathlib 4.30 formalizes only the analytic part
  (NumberTheory.Transcendental.Lindemann.AnalyticalPart…); the full theorem is not assembled.
  Carried as one explicit hypothesis (LindemannLnPhi), never a global axiom. D0 proves
  everything else from phi^2=phi+1."
- LICENSES (7 rows, CSV-checked): D0-CVFT-F1, D0-ALPHA-LOG-CESARO-MEASURABILITY-NOGO-001 (R5),
  D0-POSTCORE-DIXMIER-WODZICKI-PASSPORT-001, D0-POSTCORE-EXTENSION-BOUNDARY-001,
  D0-ALPHA-ANALYTIC-FORMALISM-BOUNDARY-001, D0-RAW-ALPHA-ANALYTIC-RESIDUE-BOUNDARY-001,
  D0-X5-ALPHA-BOUNDARY-001. ⚠ UPLIFT_MAP's adjacency note lists **six** consumers — the CSV
  has a seventh (POSTCORE-EXTENSION-BOUNDARY-001); FLAG-6, count desync only.
- What it licenses substantively: the α-front NO-GOs — "if ln phi were algebraic, a phi-graded
  zeta residue (~1/ln phi) could lie in Q(phi) and the residue route to Delta_alpha would not
  be blocked" (failure meaning, verbatim). The import RUNS THE FIREWALL, it does not produce
  numbers.
- DISCHARGE: assemble full Lindemann-Weierstrass in Mathlib (analytic part already in the pin).
  Mechanical, zero physics risk. UPLIFT_MAP §(d): "one honest classical fact, never core."

### 1.C The singleton external-theorem imports (non-owner rows)

**ASSUMP-COMPACT-LIE-KILLING-NEGATIVE** (D0-GAUGE-YANG-MILLS-KILLING-POSITIVITY-001), type
CARTAN_COMPACTNESS_CRITERION. **[MS — generality bridge only]** Ledger [Iter18]: Cartan's
criterion "is ABSENT from the pinned Mathlib … a LEGITIMATE external owner"; crucially
"D0's OPERATIVE finite positivity does NOT depend on this assumption:
matrixRepYangMillsAction >= 0 is proved INTERNALLY via
D0.Algebra.GaugeActionSignBridge.skew_square_trace_nonpositive. So this is a generality
bridge, not a load-bearing gap." DISCHARGE: formalize Cartan compactness; value cosmetic.

**ASSUMP-FROBENIUS-1877** (D0-FROBENIUS-DIVISION-3D-001), type
DIVISION_ALGEBRA_CLASSIFICATION. **[MS]** Imported: "the only finite-dim associative division
algebras over R are R(1),C(2),H(4); D0 proves only the finite quaternion content." Licenses
the 3-space-from-Im(H) corroboration (terminal-passport posture, matches the matter-sector
map: EW ℂ⊕ℍ derived-core, this leg cited-external). DISCHARGE: formalize Frobenius 1877.

**ASSUMP-WILSON-LATTICE-1974** (D0-LATTICE-FINITENESS-BRIDGE-001, the one PYTHON_CERTIFIED
True-row), type LATTICE_GAUGE_RIGOR. **[PM]** Imported: "non-perturbative gauge theory
rigorous only on a finite lattice; continuum YM mass gap = open Clay problem. D0 forces
finiteness; with M1 … forces the unique self-similar carrier." Licenses: the lattice-rigor
reading; "D0 only removes the arbitrary-spacing freedom." DISCHARGE: none (Clay-adjacent);
permanent interface.

**ASSUMP-KERNEL-CHARGE-LOCALIZATION** (D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001), type
PHYSICS_DICTIONARY. **[PM]** Imported: "nu^c uncharged = nu_R localized in ker(A) is the R2
graph->physics map (MECH-LIMIT…); a physics-dictionary identification, NOT a forced D0
identity." Licenses: trivialization of the hypercharge 2-dim charge moduli
(D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001, T3) — this is the designated GAUGE-FIXING datum
for the hypercharge torsor (UPLIFT_MAP). Failure meaning: "B-L stays gaugeable … 2-dim
anomaly-free freedom returns." DISCHARGE: a D0-internal forcing of ν_R kernel-localization
(named open; F7 story remains torsor+interface).

### 1.D The three D0-INTERNAL forcing targets (Clay reductios) — NOT external imports

These carry ASSUMP- ids but the ledger types them `D0_INTERNAL_FORCING_TARGET` /
`SPECTRAL_PACKAGING_SYMMETRY` / `COMPLEXITY_NAVIGATION_POTENTIAL` with source
"D0-internal … (not external)". They are IOUs of the theory to itself — the only
assumptions in the corpus that are **[GO] genuinely-open** by the ledger's own text:

- **ASSUMP-HODGE-ALGEBRAIC-FORCING** (D0-HODGE-M1-REDUCTIO-001): "the hypothesis that the
  canonical finite cohomology data M1-forces (strictly selects) the algebraic realization …
  assumed as a structure field, NOT derived … deriving the strict selection from
  kappa-stability + the finite cohomology functional is the open work."
- **ASSUMP-PACKAGING-REFLECTION-SYMMETRY** (D0-RIEMANN-AXIS-M1-001): "the RH-content (that
  the packaging symmetry is this reflection) is assumed not derived, a named target … NOT
  the ZFC Riemann statement."
- **ASSUMP-GLOBAL-LYAPUNOV-POTENTIAL** (D0-PVSNP-LYAPUNOV-M1-001): "a global heat-trace
  Lyapunov navigation potential V … Assumed as a structure field, NOT derived … the
  uniform-across-tower spectral gap is assumed. Regularized P_D0 vs NP_D0 at fixed UV; NOT
  the ZFC P=?NP question."

I/O contract for all three: INPUT = the named internal hypothesis; OUTPUT = a conditional
reductio via `D0.Foundation.m1_alternative_needs_catalogue`. DISCHARGE = derive the
hypothesis internally (each is a named open target). Interface posture per UPLIFT_MAP:
GENUINE-BOUNDARY (conditional reductios), consistent with the CLAY_CORE_AUDIT ("Clay-core
all honest").

### 1.E MISMATCH / DESYNC FLAGS (verify-adversarially pass; flagged, NOT fixed)

- **FLAG-1 (taxonomy drift, 3 sources).** 22 ASSUMP ids in the CSV vs 24 in the ledger vs 26
  in EXTERNAL_ASSUMPTION_REGISTRY.csv. Registry-only ids ASSUMP-PRL-RQM-GENERAL,
  ASSUMP-NO-EXOTIC-FERMIONS, ASSUMP-LEPTON-EFT-DECIMALS have NO ledger entry and NO consuming
  CSV row — either stale or awaiting wiring (LEPTON-EFT-DECIMALS is exactly the §3.6/§5
  lepton-decimal import, so a row SHOULD eventually carry it).
- **FLAG-2 (phantom claim_id in ledger).** Ledger row ASSUMP-HST-EXTERNAL cites
  `claim_id = D0-CONVEX-RESPONSE-BRIDGE`; no such row exists in CLAIM_TO_LEAN_MAP.csv, though
  the Lean theorem `convex_response_bridge_conditional` exists and consumes
  `ExternalHSTAssumptions`. An assumption-consuming Lean theorem with no registry row.
- **FLAG-3 (HST tag semantics on Born/gauge rows — soft mismatch).** D0-QM-BORN-001/002
  claim ASSUMP-HST-EXTERNAL, but their Lean theorems (`finite_born_sum_one`,
  `finite_born_nonnegative` in `D0/Born.lean`) take a `TwoOutcomeBorn` structure — they do
  NOT consume `ExternalHSTAssumptions`. The tag reads as "promotion to continuum licensed
  via HST bridge", not "hypothesis of the theorem". Defensible but type-ambiguous.
- **FLAG-4 (likely mislabel).** D0-GAUGE-MATTER-001 = `boundary_boundary_zero` on a declared
  `IncidencePair` (`D0/Topology/BoundaryBoundary.lean`) is tagged ASSUMP-HST-EXTERNAL. ∂∂=0
  conditional on an incidence declaration has NO subgaussian/Gaussian-comparison content
  (the Iter19 redefinition of HST). Strongest single-row mismatch found; candidate correct
  posture: no ASSUMP id (structure-hypothesis only) or a new dictionary id. NOT fixed here.
- **FLAG-5 (ledger "used_by_theorem" is adjacency, not consumption).** ASSUMP-JONES-INDEX and
  ASSUMP-MORDELL-E8 cite `jones_index_phi` / `icosian_e8_gram_finite`, but both Lean theorems
  are UNCONDITIONAL (verbatim statements checked: `(3+√5)/2 = φ² ∧ φ² = φ+1`; Gram symmetric/
  even/det=1/rank 8=2·4) and their CSV rows are `uses_bridge_assumptions=False`,
  CORE-FORMALIZED. Same pattern for ASSUMP-HURWITZ-GOLDEN ↔ D0-PHI-HURWITZ-001. The CSV is
  honest; the ledger column overstates. Consolidation reading: these three are
  "named-external-owner-adjacent", not row-consumed.
- **FLAG-6 (count desync).** UPLIFT_MAP says LINDEMANN has 6 consumers; CSV has 7
  (adds D0-POSTCORE-EXTENSION-BOUNDARY-001, release_status CERT-CLOSED).
- **No hard type-mismatch found** between any True-row's assumption_ids and the ledger's
  typed content EXCEPT FLAG-4; FLAG-3 is semantic looseness, not wrong physics.

---

## 2. THE 8 CONDITIONAL OWNER ROWS × ASSUMP INCIDENCE

The eight singleton-ASSUMP owner-edge rows (UPLIFT_MAP: "all T5 by construction — owner-edges
ARE interface entries"). Each CONSUMES exactly its own assumption; the table tests each owner
against the six original bridge types and the other imports for discharge/support edges.

Legend: **C** = consumes (hypothesis of its conditional theorem); **d** = would partially
discharge if the owner's external theorem were formalized in-tree; **s** = supports/feeds;
**g** = acts as gauge-fixing provider for a T3 torsor; blank = independent.

| owner row (consumed ASSUMP) | HST-EXT | RG-SM | LOR-MAC | SM-COV | SM-HEAT | HURWITZ | other edges |
|---|---|---|---|---|---|---|---|
| D0-CONNES-RECONSTRUCTION-OWNER-001 (CONNES-RECONSTRUCTION) **C** | | | | **d** (identifies limit metric as spin-manifold g; Iter17: "CONTINUUM-LIMIT CONFIRMATION that the geodesic metric -> Riemannian g") | s (Weyl reading) | | s← RIEFFEL-GHP (needs the limit to exist first) |
| D0-DIXMIER-RESIDUE-OWNER-001 (DIXMIER-TRACE) **C** | | | | | s (residue↔heat-trace formalism) | | co-consumed with LINDEMANN by the α rows (CVFT-F1 I/O: "in = ASSUMP-LINDEMANN + Dixmier owner"); ALPHA-SEAM proves this import IRREDUCIBLE in present-core |
| D0-RIEFFEL-GHP-CONTINUUM-OWNER-001 (RIEFFEL-GHP) **C** | **d** (would construct the continuum ensemble HST compares against) | | | **d** (finite→smooth convergence IS what SMOOTH-001 assumes) | **d** (trace convergence leg) | | named open residual: "the GHP-Cauchy proof for the D0 refinement sequence" — the ONLY partially-internal discharge lever in the eight |
| D0-TIME-MODULAR-FLOW-OWNER-001 (TOMITA-TAKESAKI) **C** | | | s (time layer of the macro reading) | | | | independent of the other seven; "D0 proves only the Pisot/symbolic structure" |
| D0-ADLER-WEISS-PARTITION-OWNER-001 (ADLER-WEISS) **C** | | | | | | | **g**: "doubles as the gauge-fixing PROVIDER for the toral T3 torsor" (UPLIFT_MAP); internal side already built (D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001, CERT-CLOSED) |
| D0-COMPLEX-QM-FORCING-001 (COMPLEX-QM) **C** | s (complex structure of the Born skeleton) | | | | | | REDUNDANCY CANDIDATE: M1-INFO-RECONSTRUCTION's conclusion (complex Hilbert QM) subsumes this row's conclusion — if M1-INFO is kept, COMPLEX-QM is a T6 corollary-of candidate (experimental- vs reconstruction-route); named gap stands ("the experiments assume the standard QM postulates") |
| D0-M1-INFO-RECONSTRUCTION-001 (M1-INFO-RECONSTRUCTION) **C** | s (licenses the finite-Born → QM-structure promotion) | | | | | | ANCHOR EDGE: "P-GAUGE-M1 (T2 pilot) hangs from this import — make edge explicit" (UPLIFT_MAP, prio H); grounds the M1⇒QM bridge frame (emergent-approx-QM, GAP-1 = continuous reversibility) |
| D0-ENTROPIC-DARK-GRAVITY-001 (VERLINDE-ENTROPIC) **C** | | | | s (downstream of the macro-gravity interface) | s | | **honesty flag carried**: "SPARC dark-matter comparison FAILED — scope the output claims down" (UPLIFT_MAP); riskiest import in the corpus (program-level, not theorem-level) |

Readings off the table:
1. **No owner discharges any of the six original types outright.** The smooth-limit pair
   (SM-COV + SM-HEAT) is the only column with a real discharge path, and it needs BOTH
   RIEFFEL-GHP (existence of the limit) AND CONNES-RECONSTRUCTION (identification of the
   limit) formalized — a joint, not single, discharge.
2. **The only internal work item among the eight** is the RIEFFEL-GHP golden-Cauchy residual;
   everything else discharges solely by formalizing a cited classical theorem.
3. **One redundancy edge inside the eight** (COMPLEX-QM ⊂ M1-INFO conclusions) — a T6
   candidate for a later wave, NOT actioned here.
4. **One negative-scope edge**: VERLINDE-ENTROPIC is the only owner whose downstream
   comparison has a recorded empirical FAILURE (SPARC); its I/O entry must carry the
   scoped-down output claim.

---

## 3. GAUGE-FIXING INPUTS (the measured/adjudicated data the theory consumes)

Classification per datum (post-skeptic care): **[TORSOR-POINT]** = point choice on an OWNED
torsor/moduli (the degenerate manifold is a theorem; data only selects the point);
**[UNOWNED-ANSATZ]** = the functional form itself is imported, not owned;
**[UNSPLIT]** = split pending the gauge memo repair — do not over-claim either way.

| # | datum (external) | consuming torsor/moduli (registry row) | split verdict |
|---|---|---|---|
| G1 | **Planck comparison** (CMB smoothing) | smoothing-measure (k,u) moduli — D0-CMB-CANONICAL-SMOOTHING-MAXIMALITY-NOGO-001 (T3: "3 weightings, 3 tilts"; "gauge-fixing datum = Planck-comparison passport") | **[TORSOR-POINT]** — moduli proved (maximality NO-GO), Planck selects the point. n_s itself stays OPEN (§4). |
| G2 | **DESI/CPL w(z)** | (a) role×cocycle 4-torsor — D0-POSTCORE-PHASON-EXTENSION-MAXIMALITY-NOGO-001 (E3: "quantity already owned (√10 fingerprint); remaining freedom = role torsor, DE data = gauge"); (b) pressure-energy role torsor — D0-PHASON-PRESSURE-ENERGY-MAXIMALITY-NOGO-001 (P1-C: "observed w(z) = gauge fixing"); passport D0-PHASON-WZ-CPL-PASSPORT-001 (PASSPORT-CLOSED) | **[TORSOR-POINT]** for role/orientation; **honesty line carried verbatim**: "DESI confirms EVOLVING only, not the corner" (convexity forces evolving DE; 0/6 thawing-corner maps). |
| G3 | **DE magnitude / z-map** | magnitude-map moduli anchored at −φ — D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001; 4-slot I/O row D0-PHASON-WDE-Z-MAP-OWNER-001 ("already interface-shaped") | **[UNSPLIT]** — the sign+anchor (−φ) is owned (witness_pair shares them) but UPLIFT_MAP §(d) lists "DE magnitude map (external by M2)" as boundary; whether the residual freedom is a point on an owned moduli or an imported map form is exactly the gauge-memo question. Mark UNSPLIT pending repair. |
| G4 | **Cabibbo angle / CKM** | basis-completion torsor — D0-CKM-OVERLAP-UNDERDETERMINATION-NOGO-001 (T3: "3-4-5 vs 5-12-13, 16/25≠144/169"; "Cabibbo measurement = the gauge-fixing datum") | **[TORSOR-POINT]** — the witness pair proves the torsor; measurement selects. |
| G5 | **Adler-Weiss partition choice** | Markov-partition moduli — D0-TORAL-SEED-MARKOV-MAXIMALITY-NOGO-001 ("2-rect and 3-rect share Perron φ"); provider row D0-ADLER-WEISS-PARTITION-OWNER-001; passport D0-ADLER-WEISS-WILLIAMS-PASSPORT-001 (PASSPORT-CLOSED) | **[TORSOR-POINT]** — mathematical adjudication (not a measurement): partition choice on owned moduli; entropy log φ owned on both sides. |
| G6 | **SI calibration incl. Λ_act = 38 m_e c²** | the single ExternalSICalibration slot — D0-BRIDGE-SI-CALIBRATION-CLOSURE-001 ("H0/GN/Lambda require an explicit ExternalSICalibration object"), D0-INTERPRETATION-SPINE-001 ("single external calibration"). The 38 itself is OWNED: M1QM_RATE_ENERGY_MEMO cites BOOK_03/0021__03.19:12 "C_e = 1/(2(2γ−1)) = 1/38", γ=10 integer-pinned; BOOK_03/0007__03.6:18 "Λ_act = h/τ₀ = 38 m_e c²". | **[TORSOR-POINT]** — m_e (one measured mass) fills the ONE owned calibration slot; the coefficient 38 and the slot-uniqueness are theorems. Cleanest input in the list. |
| G7 | **PDG anchors (comparison engine)** | D0-PASSPORT-PDG-STRICT-001 (EMPIRICAL-PASSPORT: "comparison engine (pinning/holdout/multiple-testing) — template for all T5 I/O entries") | input DISCIPLINE, not a gauge datum: pins comparisons, never back-reads (P-M1-FIREWALL). PDG-φ-lattice campaign verdict stands: shell membership confirmed, base non-discriminating. |
| G8 | **m_μ (EFT/IR matching)** | lepton coefficient interface — D0-LEPTON-RAW-GRAPH-COEFFICIENT-OWNER-001 (T5: "in = EFT/IR matching (m_μ); out = L11+L4=206, exponents (0,¼,⅓), order 12") | **[UNOWNED-ANSATZ]** — the EFT/IR matching FUNCTIONAL (PRIM-EFT-IR-MATCHING-FUNCTIONAL) is imported; skeleton/exponents owned, 17-digit decimals never (permanent boundary, §5). Registry-only id ASSUMP-LEPTON-EFT-DECIMALS is the un-wired name for this import (FLAG-1). |
| G9 | **IceCube HESE data** | decoherence-form test — rows D0-ICECUBE-001 (EMPIRICAL-PASSPORT) + D0-PASSPORT-ICECUBE-HESE-001 (OPEN/PROOF-TARGET) | NOT gauge-fixing — pre-registered TEST input (form frozen PRE-data): F1 monomial envelope (8:10:12) is reading-conditional [UNSPLIT at envelope level]; the flagship D1 bounded-plateau prediction is reading-ROBUST (output, §4). Falsifiers pre-stated. |
| G10 | **ν_R charge datum** | hypercharge 2-dim charge moduli — D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001 (T3), gauge-fixed by D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001 (ASSUMP-KERNEL-CHARGE-LOCALIZATION) | **[TORSOR-POINT]** with an honest caveat: the point is selected by a physics-dictionary identification (§1.C), not a measurement — the bridge row carries the ASSUMP explicitly. |
| G11 | **λ (edge-cover holonomy)** | U(1) λ-family — D0-EDGE-COVER-FAMILY-001 ("cleanest torsor in corpus: holonomy U(1)-torsor; λ = gauge-fixing datum") | **[TORSOR-POINT]** — the reference electromagnetic gauge datum. |
| G12 | **Branch label / assignment data** | R4 420-perm assignment torsor — D0-LEPTON-BRANCH-SELECTOR-MAXIMALITY-NOGO-001 ("cycle-type (4,3) forced…; assignment = torsor, branch label = gauge datum"); one-bit refinement D0-LEPTON-BRANCH-ROW-MINIMAL-EXTENSION-001 ("B_row = 1 gauge-fixing bit (of ~5.13)") | **[TORSOR-POINT]** — grounded in P-GAUGE-M1 (selector M1-FORBIDDEN is theorem-backed; within-zone labels are gauge). |

Input-side summary: 8 × [TORSOR-POINT], 1 × [UNOWNED-ANSATZ] (m_μ EFT/IR), 2 × [UNSPLIT]
(DE magnitude map; IceCube envelope reading), 1 × discipline-engine (PDG-STRICT). The
point-choice-vs-ansatz distinction is preserved exactly as it survived the skeptic: only
G8 is claimed as ansatz-import; G3/G9 stay UNSPLIT rather than over-claimed.

---

## 4. OUTPUT SIDE — what the theory returns

The invariants/predictions the interface guarantees for the §3 inputs. Status verbatim from
the registry; no promotion implied by listing.

| output | value/form | registry row(s) | status |
|---|---|---|---|
| O1 α composite (single number) | μ₁ = 1/3 (rank-trace), μ₂ = 2¹²·(3/5) ledger; algebraic closure of the seam-frozen composite | D0-ALPHA-MU1-RANKTRACE-001, D0-ALPHA-MU2-FULL-LEDGER-001, D0-ALPHA-ALG-CLOSED-001 | CERT-CLOSED ×3 |
| O2 α measurement band | last ~1e-8 layer = measurement-band interface | D0-ALPHA-MEASUREMENT-LIMIT-001 | EMPIRICAL-PASSPORT |
| O3 α analytic wall (negative output) | Cesàro limit = 1/(3 ln φ), transcendental ∉ Q(φ) — the golden information rate; residue route BLOCKED conditional on LINDEMANN | D0-ALPHA-LOG-CESARO-MEASURABILITY-NOGO-001 (R5), D0-ALPHA-SEAM-REALIZATION-NOGO-001 | NO-GO (8-pass) |
| O4 rank-3 charpoly coefficients | depressed cubic λ³ − 359λ − 2574 (discriminant 6185264 > 0, 3 real modes + 1 Pisot arrow) | D0-RANK3-CAUSAL-CONE-FORCING-001, D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001 | LEAN_PROVED / CORE-FORMALIZED |
| O5 Higgs geometric ratio | m_H/m_Z = √2 forced (cube in-plane diagonal); measured 2.9% deficit = δ_loop NAMED-GAP needing external RG | D0-HIGGS-CUBE-DIAGONAL-001 | BRIDGE-CALIBRATION |
| O6 lepton coefficient skeleton | L11+L4 = 206, exponents (0, ¼, ⅓), order 12 — given m_μ (G8) | D0-LEPTON-RAW-GRAPH-COEFFICIENT-OWNER-001 | NO-GO (owner; skeleton forced, coefficient external) |
| O7 lepton exponent-row realizability | Vandermonde det = 1/144 ≠ 0 ⇒ any pair realizable (honest anti-claim: decimals carry no fingerprint) | D0-LEPTON-DECIMAL-MASS-RATIOS | NO-GO |
| O8 generation index | 3 generations + clustering invariants — given Yukawa/PDG scheme | D0-GEN-MASS-001 (UPLIFT_MAP T5: "index proved, masses external") | per row |
| O9 IceCube flagship | bounded-plateau decoherence prediction (reading-ROBUST) vs Lindblad unbounded; envelope 8:10:12 reading-conditional | D0-ICECUBE-001, D0-PASSPORT-ICECUBE-HESE-001 | EMPIRICAL-PASSPORT / OPEN (PROOF-TARGET) |
| O10 M2 phase fingerprint | {80/81, −1/9, 8/9} Fraction-exact (zone-9 labeling = Q₈-typed torsor of detector-layer pointed shell) | D0-M2-PHASE-LABELING-V9-SHELL-001, D0-M2-NO-CANONICAL-CYCLIC-LABELING-V9-001 | OPEN (PROOF-TARGET, minting pending) |
| O11 DE qualitative | evolving dark energy FORCED (convexity); √10 fingerprint owned; w(z) role fixed by G2 | D0-PHASON-THAWING-001 (CORE-FORMALIZED), D0-PHASON-WZ-CPL-PASSPORT-001 | closed at EVOLVING-only scope |
| O12 n_s | **OPEN** — smoothing moduli proved underdetermined; tilt varies in (k,u); no owned n_s number | D0-CMB-NS-SMOOTHING-UNDETERMINED-NOGO-001, D0-CMB-NS-LAPLACIAN-IDS-OWNER-001, D0-CMB-PHASON-SPECTRUM-OWNER-001 (OPEN) | honest OPEN |
| O13 QNM overtone check | δ₀ overtone-ladder check — given preregistered model + modes table | D0-GRAV-QNM-001 (UPLIFT_MAP T5) | per row |
| O14 PMNS δ₀ | δ₀ forced internally; the NuFIT comparison is post-hoc/NOT discriminating (coefficient freedom) — listed as output honesty, not evidence | D0-PMNS-DELTA0-NUFIT-001 | EMPIRICAL-PASSPORT (demoted, stays) |
| O15 departure rate | Γ₀ = φ⁻¹/τ₀ ≈ 2.90×10²¹ s⁻¹, hΓ₀ = φ⁻¹·Λ_act ≈ 12.0 MeV — owned given G6; E-dependence external | M1QM_RATE_ENERGY_MEMO (memo-level; THE 6.1.2) — no dedicated registry row yet | memo-owned |
| O16 dimensionless trace shapes | a0/a2 trace shapes invariant under calibration (the guarantee that G6 cannot mutate outputs) | D0-BRIDGE-SI-CALIBRATION-BOUNDARY-001 | BRIDGE-CALIBRATION |

Scoreboard honesty carried over (memory-verified, no change here): EW/single-number matches
hold; PMNS+LIGO post-hoc; DESI evolving-only; SPARC dark-matter FAILS (scopes O-side of
VERLINDE owner); n_s open.

---

## 5. THE HONEST BOUNDARY ROSTER (stays external — and WHY that is legitimate)

One-line interface entries; each cites the no-go/audit that ESTABLISHES the boundary (these
are not holes — each has a theorem or hardened audit saying the external status is forced).

- **ALPHA-SEAM** — D0-ALPHA-SEAM-REALIZATION-NOGO-001: μ₂ = 2¹²ρ tautology + "5 ramifies in
  Z[φ]" valuation; ASSUMP-DIXMIER-TRACE **proven irreducible in present-core**; 8-pass-hardened
  (ALPHA_SEAM_NOGO_V2.md); reopening only via its 4 named hooks. Legitimacy: theorem-grade NO-GO.
- **34≠33 pair** — D0-VNEXT-33-SCENE-ANCHOR-OWNER-001 + D0-VNEXT-AF-ONE-DIMENSIONAL-REDUCTION-
  CLASSIFICATION-001: "34−1=33 is NOT a quotient"; (24,8,1) ≠ (9,11,13). Legitimacy:
  anti-numerology stands by computed mismatch — the boundary IS the result.
- **vNext2 gate** — D0-VNEXT2-SCENE-NATIVE-CLOSURE-BOUNDARY-001: "downstream gates stay
  closed; the gate-keeping IS the content" (UPLIFT_MAP GENUINE-BOUNDARY). Legitimacy:
  closure-boundary row, deliberate.
- **PMNS-δ₀** — D0-PMNS-DELTA0-NUFIT-001: post-hoc, non-discriminating (degree-1 refit
  1/3−δ₀/4 also <1σ; Lean directions true-by-construction); demoted CORE-FORMALIZED →
  EMPIRICAL-PASSPORT. Legitimacy: adversarial audit already adjudicated; do NOT uplift.
- **LINDEMANN** — ASSUMP-LINDEMANN-LNPHI (7 CSV consumers, §1.B): "one honest classical
  fact, never core" (UPLIFT_MAP §(d)); carried as ONE explicit hypothesis, never a global
  axiom. Legitimacy: classical transcendence theorem; Mathlib-assembly is the only path in.
- **Colour ⊗C³** — D0-COLOUR-GENERATION-TYPED-CARRIER-NOGO-001: commutant 8 < 9, typed
  collapse to diagonal; colour is NOT scene-derived — octonion/E8 route is terminal-passport
  (Furey/Mordell owners). Legitimacy: computed commutant obstruction + standing audit.
- **Lepton decimals** — D0-LEPTON-DECIMAL-MASS-RATIOS (Vandermonde ⇒ any pair realizable) +
  D0-BARE-GRAPH-DECIMAL-NOGO-001 (direct raw→decimal M1-forbidden, T6 under the RAW-GRAPH
  owner): 17-digit decimals live in EFT/IR forever. Legitimacy: realizability theorem shows
  decimals cannot carry a D0 fingerprint; P-M1-FIREWALL forbids back-reads.
- **DE magnitude** — D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001 + D0-PHASON-WDE-Z-MAP-OWNER-001:
  magnitude map external by M2; sign+anchor (−φ) owned, magnitude form not. Legitimacy:
  maximality NO-GO establishes the moduli; split verdict G3 = UNSPLIT pending gauge memo.
- (Adjacent, same posture:) the three **Clay reductios** (§1.D) — conditional-reductio
  boundary under their internal forcing targets; **Verlinde/SPARC** — output claims scoped
  down after empirical failure; **RG scheme data** (§1.A RG-SMOOTH-INTERP) — matching-scheme
  choice is permanently external under P-M1-FIREWALL.

---

## 6. SUMMARY COUNTS + DISCHARGE QUEUE

### Counts

**Inputs (N = 12 named in §3), split:**
- measured-physical: 7 — Planck (G1), DESI/CPL (G2), Cabibbo (G4), m_e/SI (G6), m_μ (G8),
  IceCube HESE (G9, test-input), ν_R charge datum (G10; dictionary-selected).
- adjudication/convention (mathematical choice on owned moduli): 4 — Adler-Weiss partition
  (G5), PDG comparison engine (G7, discipline), λ holonomy reference (G11), branch
  labels/assignment bits (G12).
- input-side split verdicts: 8 TORSOR-POINT / 1 UNOWNED-ANSATZ / 2 UNSPLIT / 1 discipline.

**Mathematical imports (the ASSUMP layer): 22 ids in the CSV** (24 ledger / 26 registry —
FLAG-1), consumed by 29 True-rows; risk split: **9 [MS]** mathematically-standard
(HURWITZ-GOLDEN, LINDEMANN-LNPHI, FROBENIUS-1877, COMPACT-LIE-KILLING, ADLER-WEISS,
TOMITA-TAKESAKI, DIXMIER-TRACE, CONNES-RECONSTRUCTION, RIEFFEL-GHP), **10 [PM]**
physically-motivated (HST-EXTERNAL, RG-SMOOTH-INTERP, LORENTZ-MACRO, SMOOTH-COVARIANCE,
SMOOTH-HEATTRACE, WILSON-LATTICE, KERNEL-CHARGE-LOCALIZATION, COMPLEX-QM,
M1-INFO-RECONSTRUCTION, VERLINDE-ENTROPIC — the last carrying the SPARC failure flag),
**3 [GO]** genuinely-open (the D0-internal Clay targets, §1.D; plus the RIEFFEL-GHP
golden-Cauchy residual as the one partially-internal [MS→GO] leg).

**Outputs: M = 16 interface outputs (§4)** — of which 2 are honest OPENs (O12 n_s, O10
pending minting), 2 are negative-guarantees (O3 wall, O16 invariance), 1 memo-level (O15).

**Bridge-shaped rows: 39 unique** (29 True + 8 CBS + 3 BC − 1 overlap). Untouched: all
053040 rows (none of the 39 is one).

### Discharge queue (ordered by value = what it unlocks per unit of named work)

1. **RIEFFEL-GHP golden-Cauchy residual** — the ONLY partially-internal lever among the 8
   owners; named open: "the GHP-Cauchy proof for the D0 refinement sequence". Unlocks (with
   #2) the smooth-limit pair SM-COV+SM-HEAT and the HST continuum ensemble — three of the six
   original types hang on this front.
2. **ASSUMP-CONNES-RECONSTRUCTION formalization** — joint partner of #1: identification of
   the GHP limit as Riemannian g (Iter17 "continuum-limit confirmation" reading). External-
   theorem work, but the highest-leverage joint discharge in the incidence table (§2).
3. **The three D0-internal Clay targets (§1.D)** — HODGE-ALGEBRAIC-FORCING,
   PACKAGING-REFLECTION-SYMMETRY, GLOBAL-LYAPUNOV-POTENTIAL: the only [GO] assumptions;
   each discharge converts a conditional reductio into an unconditional theorem. High value,
   unknown difficulty (they are named-open research targets, not formalization chores).
4. **ASSUMP-LINDEMANN-LNPHI assembly in Mathlib** — mechanical (analytic part already in the
   pin); hardens 7 consumer rows incl. the α-front NO-GOs from hypothesis to theorem. High
   certainty, moderate value (the firewall already behaves as if true).
5. **ASSUMP-KERNEL-CHARGE-LOCALIZATION internal forcing** — would convert the hypercharge
   torsor's gauge fixing from dictionary-identification to owned selection, closing the F7
   story at torsor+owned-point level. Single-row, physics-visible value.
   (Non-queue: ASSUMP-DIXMIER-TRACE is EXCLUDED — proven irreducible in present-core by
   ALPHA-SEAM; queueing it would contradict the corpus's own no-go. COMPACT-LIE-KILLING and
   FROBENIUS/HURWITZ/MORDELL/JONES are cosmetic-grade formalization chores; RG-SMOOTH /
   LORENTZ-MACRO / WILSON are permanent-interface under P-M1-FIREWALL / P-MECH-LIMIT.)

---

*End of W5 interface spec. Checkable count/consistency claims are certified by
`w5_interface_check.py` (same directory). No registry row, book, or Lean file was modified.*
