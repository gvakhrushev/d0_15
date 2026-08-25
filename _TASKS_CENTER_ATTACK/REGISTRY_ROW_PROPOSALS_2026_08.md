# Registry row proposals — session layer registration (2026-08-01, owner-gated)

**Nothing below is minted.** These are prepared row texts for `03_THEORY_MAP/theory_status_map.csv`
(+ `CLAIM_TO_LEAN_MAP.csv` mirrors). All modules build from `D0/All.lean` (4458 jobs, 2026-08-01),
all `sorry`-free; axioms are `propext/Classical.choice/Quot.sound` throughout (plus `native_decide`
only where inherited from existing corpus imports). Status column proposals follow the corpus's own
grammar; the owner decides each mint and may run the adversarial loop per candidate.

## Tier 1 — structural spine (propose: certificate / formal_core)

1. **D0-SCENE-DARK-ARCHIVE-STRUCTURE-001** — `D0.Spectral.DarkArchiveStructure`
   (`balanced_mem_ker; ker_imp_balanced; no_invariant_vector_in_archive`). ker A = zone-balanced
   vectors = std₉⊕std₁₁⊕std₁₃ (blocks 8/10/12); the archive carries no Aut-invariant vector; the
   visible/dark division IS the invariant/invariant-free split. Consumers: SEP leg of
   D0-PHASON-WZ-TRANSFER-OWNER-001 (annihilation now proved, was cited), R^Aut dimension reading.

2. **D0-SCENE-JOINT-COMMUTANT-SIX-001** — `D0.Spectral.JointCommutant` (`joint_commutant;
   no_rational_root`). Centralising Aut AND the adjacency leaves 6 = 3+3 (visible ℚ[Q] + one scalar
   per archive block); transport cubic λ³−359λ−2574 irreducible (48-divisor sweep). Halves the R1
   commutant 12 under the scene's own dynamics — cross-reference D0-P-M1-SATURATION-001.

3. **D0-EQUIVARIANT-SEAM-NOGO-001** — `D0.Synthesis.EquivariantSeamNoGo` (`no_equivariant_seam;
   archive_invariant; visible_invariant`). Every Aut-equivariant operator is block-diagonal across
   active(3)/archive(30); Feshbach couplings B, C vanish; W_eff z-independent, seam residue zero.
   Upgrades the α-front "EXTERNAL Dixmier extraction" from scope declaration to necessity within
   the equivariant class. Consumers: D0-ALPHA-FESHBACH-DIXMIER-OWNER-001 (honesty boundary),
   ASSUMP-DIXMIER-TRACE, and the three matter no-gos of Campaign 3.

4. **D0-TRANSPORT-CLOSED-FORM-001** — `D0.Spectral.TransportClosedForm` +
   `TransportSelfAdjoint` (`transport_rank_one; secular_eq_cubic; secular_root_gives_eigenvector;
   transport_self_adjoint`). Q = 𝟙nᵀ − diag n; secular equation Σnᵢ/(nᵢ+λ)=1 IS the transport
   cubic; eigenvectors 1/(nᵢ+λ); D·Q = Qᵀ·D (self-adjoint in the zone-size measure; real spectrum;
   parameter-free O(3) generation→transport rotation, explicitly NOT CKM-like).

5. **D0-HODGE-THREE-LEVEL-SPECTRUM-001** — `D0.Synthesis.HodgeThreeLevelSpectrum`
   (`top_hodge_factorizes; mckean_singer; susy_assembly; betti_readout; doubling_law; moment_M2`).
   P₂ = (8+x⁹)(10+x¹¹)(12+x¹³); P₀−P₁+P₂ = 961 for all x; b = (1,0,960) — b₁ = 0, the only
   homology is the archive; level-1 doubling law. HONESTY SPLIT to record verbatim: the polynomial
   identities are Lean-proved; the identification of P₁ with spec(Δ₁) rests on the Hodge assembly
   over the two owned eigenbases + ∂₁∂₂ = 0, verified in exact rational arithmetic outside Lean.

6. **D0-GENERIC-SCENE-CALCULUS-001** — `D0.Synthesis.GenericSceneCalculus` (`moment0..2;
   euler_generic; rival_rules_dependent`). M₂ = D(V+6) derived generically (the +6 structural);
   χ = 1 + H generically; allwalks − nonbacktracking = 2E (the vNext2 rival carriers are linearly
   dependent). Cross-references D0-M1-HOMOLOGICAL-SCENE-READING-001,
   D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001 (no-go unchanged; dependency added).

7. **D0-ZONE-IS-GENERATION-001** — `D0.Synthesis.ZoneIsGeneration` (`decomposition;
   decomposition_unique; dark_mem_ker`). Per zone: 1 visible + (nᵢ−1) dark, split unique; ties the
   generation index, the phason index (torusShell ladder) and the archive index into one.

## Tier 2 — zone count and boundaries (propose: certificate; two with no-go type)

8. **D0-ZONE-COUNT-MULTIPLICATIVE-001** — `ZoneCountFromSpectrum` + `ZoneCountCompleteness`.
   (D,H) = (1287,960) has a unique preimage over ALL part counts (5|H forces 11, 3|H forces 13,
   remainder [9]); the ADDITIVE pair (V,H) does not force the count (witnesses [3,5,9,16],
   [2,2,4,5,9,11] — `HomologicalReadingClassBoundary`, supplying the class-boundary witness the
   owned reading's own controls lacked).

9. **D0-TRANSPORT-SPECTRUM-BLINDNESS-NOGO-001** (no-go) — `TransportSpectrumBlindness`. The
   transport cubic omits V; 55 isospectral pairs; the frozen scene is pinned only by the
   arithmetic of (E,T) = (359,1287). Blocks any future "reconstruct the scene from transport
   data" claim.

10. **D0-TRANSPORT-NOT-GOLDEN-001** (boundary) — `TransportNotGolden`. No transport eigenvalue in
    ℚ(√5); the overclaimed engine-limit reading is retracted inside the module. Consumer: α-front
    obligation (i) — the sharpest pointer that a per-crossing φ⁻¹ mechanism cannot live on the
    transport spectrum itself.

## Tier 3 — dark-EOS chain (propose: certificate / cosmology, with conditionality verbatim)

11. **D0-DARK-EOS-DISCRETE-SET-001** — `RoleOrientationEOS` + `DarkEOSDiscreteSet` +
    `LambdaCDMExcluded` + `RoleModelDiscrimination` + `RoleAssignmentNarrowing` +
    `DarkEOSMagnitudeFree`. MUST record the split: (unconditional) ΛCDM excluded by the
    degeneracies alone in the ratio reading (w = −1 needs s = 15 ∉ subset sums of {8,10,12});
    (conditional on reading |w| = φ — the sign owner row explicitly keeps |w_DE| PROOF-TARGET)
    eight values −φ + s/30, exclusion by irrationality, minimal deviation φ − 8/5, narrowed
    w = 3/5 − φ via the owned radial order. Two modelling steps named as the author's:
    one-orientation-per-mode; degeneracy-weighted mean.

## Tier 4 — supporting closures of named gaps (propose: certificate / formal_core)

12. **D0-PARTITION-ALGEBRA-001** — `PartitionAlgebra` (finite Stone–Weierstrass; closes
    `InvariantMinimal.lean:32` "cited not formalized").
13. **D0-ZONE-CONNECTIVITY-001** — `ZoneConnectivity` (30 swaps' orbits = zones; closes
    `InvariantGenerationBridge.lean:42` "cited not formalized").
14. **D0-SUBCRITICAL-TRACE-CLASS-001** — `SubcriticalTraceClass` (Summable ↔ a ≤ 2; closes the
    two named gaps of D0-P-SUBCRIT-001).
15. **D0-CASCADE-FLOOR-ORIENTATION-PARITY-001** — `CascadeFloorOrientationParity` (the +2 step as
    a cascade floor; reuses D0-LUCAS-DEFECT-SIGN-001).
16. **Symmetric-function / active-spectrum family** — `SymmetricFunctionCalculus`,
    `ActiveSplittingFromDistinctness`, `ActiveSpectrumClosedForm`, `ActiveWindowIrrational`:
    ∏(N−nᵢ) = Ne₂−e₃; gap = Σa(b−c)² (zero iff equal zones); discriminant = gap/∏deg = 1/40
    (the √10 explained); the S_DE window contains no integer (SEP leg structural). One row or
    four, owner's choice.

## Tier 5 — recorded dead ends (propose: no-go/boundary rows OR leave as in-module records)

17. `SceneCountRouteNoGo` (propositional route caps at 2; both reduction arrows vacuous),
    `DiscriminationRetyping` (uninhabitable), `DiscriminationKinds` (circular),
    `LadderRunLength` (stop-at-15 generic), `DyadExponentForced` (retraction inserted 2026-08-01).
    Value: prevents re-attack; the corpus's traps-checklist culture suggests these deserve rows.

## Tier 6 — Campaign 1/2/3 additions (2026-08-02, owner-gated like everything above)

18. **D0-SCENE-HEAT-KERNEL-001** — `D0.Synthesis.SceneHeatKernel` (projector partition of
    identity; zoneHeat closed forms; total_heat_is_P0; zetaL with values ζ(0)=32, ζ(−1)=718,
    ζ(−2)=16426, ζ(1)=239/165). First closed-form heat/zeta layer at the scene.

19. **D0-SCENE-TRACE-HEAT-CAPACITY-001** — `D0.Synthesis.SceneTraceHeatCapacity` (sceneGraph :
    FiniteArchiveGraph — FIRST concrete instance; cut_zone = n_z(33−n_z); horizon structure
    decided at both granularities: zone unions never saturate, full scene + co-vertex saturate;
    lucas_defect_of_full_scene = 30 = archive dim — first genuine TraceHeatDefect instance).

20. **D0-SCENE-SPECTRAL-ACTION-001** — `D0.Synthesis.SceneSpectralAction` (first scene
    instantiation of rows 91–92 ladder: a₀ = 718 = 2E = ζ_L(−1); a₂ = 16426 = ζ_L(−2) =
    15708 + 2·359; **discrete EH action proxy = 359 = |E|** — the same owned object the α_top
    numerator consumes; mechanism: off-diagonal −1 squares are edge indicators). Shared-object
    bridge gravity↔α; no identification beyond the shared object claimed.

21. **D0-TRANSPORT-FORK-ENDGAME-001** — `D0.Synthesis.TransportForkEndgame` + memo
    `TRANSPORT_FORK_ENDGAME_MEMO.md` (POST-SKEPTIC: 1 KILL accepted+repaired, confirm CLEAN).
    Door-5 double instability (Lean assembly, both no_equivariant_seam conjuncts); two-12
    no-merge vaccination; toral stable root φ⁻¹ + exclusivity + matrix wire; 12 = L₅+1 from the
    ξ₅ return (+1 anonymous); φ⁻¹/−φ not transport-cubic roots (scoped). Door-2 route reduced to
    named residual **PRIM-SEAM-CROSSING-TICK-IDENTIFICATION**; door 1 remains live rival.
    Row 583 obligation-(i) note update goes with this mint.

22. **D0-EQUIVARIANT-HYPERCHARGE-CARRIER-001** — `D0.Synthesis.EquivariantHyperchargeCarrier`
    (POST-SKEPTIC 2026-08-02: uniqueness overclaim killed and repaired). Vertex carrier no-go
    (≤3 < 5) + symmetric-edge no-go (≤3) + directed-edge pass (≤6). Scope: carrier classes
    audited = {vertex, symmetric edge, directed edge} ONLY — ordered triangles and directed
    2-paths also pass counting, not audited. CITE-NOT-REMINT: ≤6 = owned "6 cross-part"
    pair-orbit count (D0-RAW-SCENE-GRAPH-001); vertex leg = corollary of owned zone-indicator
    minimality (D0-P-INVARIANT-MINIMAL-001/F7). Both row conventions recorded: 5-field passes
    with slack; 6-field (ν_R=0, `hypercharge_row_six`) saturates ⇒ directed carrier must be
    injective on the 6 classes. Lemma reuse: zone-constancy delegates to
    `swap_fixed_zoneConstant`.

23. **D0-EQUIVARIANT-MATRIX-STRUCTURE-001** — `D0.Synthesis.EquivariantMatrixStructure`
    (POST-SKEPTIC 2026-08-02: Higgs carrier-mismatch binding killed and repaired). Operator-level
    normal form: determination by ≤ 12 structure constants (3+3+6); equality/freeness of the
    count owned at D0-RAW-SCENE-GRAPH-001 / D0-RAW-COMMUTANT-WEDDERBURN-001 (cited).
    archive_scalar_action: scalar diagC−offC per zone; archive_actions_commute: the 33-scene
    archive block is abelian; no_equivariant_archive_noncommutativity — scoped: the Higgs
    blocker's Q₀ is typed on M₂(ZMod 44) (J2 firewall "NOT the 33-dim scene"; GROUPE: wall is
    ownership, not existence) and is UNTOUCHED; the theorem closes only the hypothetical
    33-scene equivariant analogue. Visible-block non-commuting witness described (cross-indicator
    pair, MN≠NM), not formalized.

24. **D0-LEFSCHETZ-ZONE-EXCLUSION-001** — `D0.Synthesis.LefschetzZoneExclusion` (POST-SKEPTIC
    2026-08-02: WOUNDED-FIXABLE, W1–W3 repaired; clean axioms, NO native_decide). BOTH closed
    forms: `det(Tⁿ±1) = (−1)ⁿ ± (−1)ⁿLₙ + 1` for ALL n; **13 lies outside BOTH owned toral
    address families** — anti-periodic (needs L=13 or even-11) AND periodic #Fix (needs L=13 or
    L=15; `fifteen_not_lucas`) — scoped to the two owned families, no wider universal. The owned
    composite `13 = F(3)+F(4)` forced AT VALUE LEVEL ({4,9} unique among two-term sums; index
    pair NOT unique — (0,4) also lands, F(0)=det(2I)=4). `periodic_five`: G(5)=11=#Fix₅ (both
    families own 11; anti-periodic owns 9; 13 unique zone size outside both).
    `lucas_recurrence_shares_degree_arithmetic` (renamed from "is" per skeptic W2): 20=9+11
    shared equation, no binding minted. Cross-refs: D0-TRACE-HEAT-CAPACITY-GRAVITY-001 (owner of
    the values + composite reading), D0-TORAL-LUCAS-PERIODIC-SEED-OWNER-001 (periodic family).

25. **D0-YUKAWA-COMMUTANT-SPECTRUM-001** — `D0.Synthesis.YukawaCommutantSpectrum` + memo
    `YUKAWA_COMMUTANT_SPECTRUM_MEMO.md` (POST-SKEPTIC 2026-08-03: 2× WOUNDED-FIXABLE, 0 kills,
    7 repairs applied). Resolution-2 mathematics of the Yukawa tension log: full-ℚ no-root
    statement (RRT step — owned forms are divisor sweeps); **automatic non-degeneracy**
    (`qq_spectrum_splits`); **forced irrationality** (`no_rational_value_at_root`, formalized
    FROM the skeptic's kill attempt: non-scalar members never take rational values at roots ⇒
    attainable triples dense-countable, rational targets unattainable exactly); three real
    roots with locations EXPORTED in the statement, in the OWNED brackets `(−13,−12)`,
    `(−10,−9)`, `(21,22)` (ℚ sign table: `TransportNotGolden.transport_roots_bracketed`;
    discriminant realness owned at rows MIXING-HIERARCHY-INVERSION / RANK3-METRIC / RANK3-CUBIC
    — cited, not re-minted). Honest negative: parameter-free ratio profile ≤ 22/9 < 2.5
    (squares < 6, float-free) vs lepton targets — kill carried by first ratio, factor ≥ 9 in
    every convention; Vandermonde invertibility ⇒ arbitrary-precision fit ⇒ zero predictive
    surplus without an owned (a,b,c)-selector. Rival owned route (D0-LEPTON-002 L₁₁+L₄=206 THE;
    Puiseux exponents) needs no selector — cross-referenced. Fork stays owner-gated.

26. **D0-SEAM-CROSSING-WEIGHT-001** — `D0.Synthesis.SeamCrossingWeightForced` + C4 addendum of
    `TRANSPORT_FORK_ENDGAME_MEMO.md` (POST-SKEPTIC 2026-08-03: **1 KILL accepted** — "derived
    from owned form" was a false grade, the depth total is PROOF-TARGET not THE; all repairs
    applied, confirm survivors fixed). Surviving conditional content (duplication sweep clean):
    per-crossing value determined by the REGISTERED form under (α) 12th-sector uniformity +
    (β) count/product reading + (γ) the registered total (the obligation's own open sub-leg);
    equivariance equalizes the eleven `V₁₁` weights (`equivariant_weights_equal`);
    `seam_crossing_composed` — one composed Lean pipeline; `nonuniform_freedom` — without (α) a
    one-parameter family (control can fail). Residual of
    PRIM-SEAM-CROSSING-TICK-IDENTIFICATION = (α)∧(β)∧(γ) under the norm; value no longer part
    of the primitive MODULO (γ). Row-305 stale-THE flagged (mechanical section).

27. **D0-TRANSPORT-FIELD-NO-GOLDEN-001** — `D0.Synthesis.TransportFieldNoGolden`
    (POST-SKEPTIC 2026-08-03: WOUNDED-FIXABLE, 0 kills, W1–W5 repaired). Field-grade upgrade of
    the twice-killed universal, in a form exhausted by construction: GENERAL export
    `no_quadratic_element_in_transport_field` — NO element of quadratic minimal-polynomial
    degree lies in `ℚ⟮λ⟯` for any real transport root λ ([ℚ⟮λ⟯:ℚ] = 3, 2 ∤ 3); `φ`, `φ⁻¹`
    instances. "Rational function" scoped to RATIONAL coefficients; single-eigenvalue fields
    ONLY (splitting field NOT claimed); eigenvalue↔root = the docstring-grade spectral-mapping
    convention (charpoly owned at JointCommutant). TransportNotGolden's ℚ(√5)-exclusion
    instances become corollaries (its bracket sign table is separate, NOT subsumed). Mint
    ordering: consumes `no_rational_root_rat` from item 25 — do not mint if 25 dies.

## Recorded dead-end (Campaign 3, no-go #3 as planned — do not re-attack as stated)

The planned "PRIM-EDGE-HOLONOMY-SELECTOR is not realizable equivariantly"
(NEXT_FRONT_PLAN_2026_08.md:108-109) is FALSE as stated: the selector must pick ONE λ ∈ U(1)
(row D0-EDGE-COVER-FAMILY-001: "selecting a unique lambda needs NEW frozen input"), and a
CONSTANT choice is trivially Aut-equivariant — equivariance obstructs only within-class
variation (which the selector does not need). The row's own no-go (phase not forced) already
owns the real obstruction: canonicity, not equivariance. Caught pre-memo by the kill-shape
check (universal over unexhausted class); no Lean written. A future equivariance statement
would need a different target: e.g. "no equivariant selector VARIES within an edge class"
(true but already implied by `equivariant_cross_constant`, and it does not bite the family).

## Deliberately NOT proposed

- `TransportTwelveForkCollapse` and the door-5 kill — these belong to the α-front campaign's own
  adversarial loop (Campaign 2), not to bulk registration.
- `SceneSpectralResolution` overlaps `D0-VNEXT2-SCENE-FINGERPRINT-OWNER-001` (vertex table already
  owned); propose only as cross-reference notes on the fingerprint row, not a new row.

## Mechanical registry repair, also owner-gated

Row 305 `D0-ALPHA-HOLONOMY-002` (flagged by C4 skeptic 2026-08-03): stale sentence "the
STRUCTURE (12/5 angle, sin-channel, phi^-17 depth) is THE via D0-PI0-DISCRETE-ANGLE-001 +
D0-Q8-SIN-CHANNEL-001" — rows 306/307 own the angle and channel only, NOT the depth; the
2026-07-18 four-level reframe (row 583 + BOOK_02 02.13.h:95) grades the depth composition as an
open sub-leg. Recommend tripwire or repair; this is the only corpus text an "owned total"
misreading could lean on.


Row `D0-ALPHA-SEAM-FORM-FORCED-001` (line 583): every internal positional row reference in its
note is uniformly **+19 stale** ("row 285" → line 304 `D0-SEAM-HOLONOMY-001`, "row 243" → 262,
"row 253" → 272, "row 460" → 479, "row 169" → 188). Recommend replacing positional references by
claim IDs. Its note also still records a FIVE-candidate fork; the certificate and memo are updated
(2026-08-01) — the row text update goes with the Campaign-2 mint.

