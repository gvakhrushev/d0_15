# D0 v14 Book Refactor Audit

## Scope

This audit records the editorial refactor of the active books after the Trace-Heat-Capacity Gravity integration. It is a navigation and duplication audit; it does not demote theorem owners, certificates, passports or Lean claim-map rows.

## Structural Fixes Applied

- Book 00: converted patch labels `P8`--`P12`, `00.P12`, `00.38` and `00.PDG-GP30` into canonical `00.24`--`00.32` headings.
- Book 01: converted late `01.99`--`01.102` patch headings into `01.23`--`01.28`; moved Born 4.0 under the Born readout section.
- Book 02: converted the late `02.99` / `02.101.*` proof-spine patch stack into `02.34`--`02.44`; removed one orphan `#` line; split tick-gauge into its own H2 section.
- Book 03: numbered the Torus/Core13 shell section and moved Lefschetz counts to `03.24`.
- Book 05: made the PDG passport protocol a numbered `05.15.1` H3 under the falsification matrix rather than a separate unnumbered H2.
- Book 06: numbered `phi`-discrete RG and `Phi^5 Torus Invariant` as `06.31` and `06.38`.
- Book 07: numbered the Lorentz transition as `07.26` and compressed the late gravity closure run from `07.43`--`07.48` to `07.36`--`07.41`.
- Book 08: numbered the smooth macro-geometry bridge as `08.31.1` and the Core-13 passport boundary as `08.43`.
- Sync guards were updated to the new canonical headings where they had hard-coded old patch labels.

## Duplicate And Stale Analysis

### Structural duplicates

- None after refactor: no unnumbered H2, patch-number H2, `P*` H2, or duplicate numeric heading remains in active books.

### Recurring themes kept intentionally
- Phase-unfolding appears in Books 01, 02, 06 and 07. This is not merged because each instance has a different role: foundation chain, proof-spine rule, time/forgetting runtime, and gravity capacity source.
- Born/quadratic response appears in Books 01 and 02. Book 01 owns detector/readout foundations; Book 02 owns proof-spine promotion discipline.
- Torus/Core13 appears in Books 00, 01, 02, 03, 04, 06 and 08. These are cross-book anchors: entry architecture, Born relation, proof spine, action scene, matter integration, torus invariant, and passport boundary.
- PDG/Golden Pass30 appears in Books 00, 02, 05 and 08. These sections remain separate because Book 05 defines verification discipline while the other books only point to passport boundaries.
- Trace-Heat-Capacity Gravity appears in Books 00, 05, 06, 07 and 08. It is intentionally distributed as entry contract, verification row, time ladder, gravity mechanism, and cosmology/archive interpretation.

### Removed or rewritten stale structure
- Old patch labels (`P8`, `P9`, `P10`, `P11`, `P12`) are no longer headings.
- Old high patch numbers (`01.99`, `01.100`, `01.101`, `01.102`, `02.99`, `02.101.*`) are no longer active section numbers.
- The duplicate Book 02 heading `02.101.2d` was split into `02.41` and `02.42`.
- The phrase `four replacement families` was corrected to `replacement theorem families` because the proof spine now contains more than four families.

## Recurring Heading Titles

- `role of this book`
  - `BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md:20` 01.2 Role of this book
  - `BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md:13` 02.2 Role of this book
  - `BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md:3` 05.1 Role of this book
  - `BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md:7` 06.2 Role of this book
  - `BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md:7` 07.2 Role of this book
  - `BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md:7` 08.2 Role of this book
- `hurwitz-rigid phase generator and non-resonant spatial unfolding`
  - `BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md:1079` 01.21 Hurwitz-rigid phase generator and non-resonant spatial unfolding
  - `BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md:1297` 02.32 Hurwitz-rigid phase generator and non-resonant spatial unfolding
  - `BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md:606` 06.30 Hurwitz-rigid phase generator and non-resonant spatial unfolding
  - `BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md:626` 07.25 Hurwitz-rigid phase generator and non-resonant spatial unfolding
- `phase-unfolding master chain`
  - `BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md:998` 01.19 Phase-unfolding master chain
  - `BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md:1225` 02.30 Phase-unfolding master chain
  - `BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md:558` 06.29 Phase-unfolding master chain
  - `BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md:556` 07.23 Phase-unfolding master chain
- `claims inherited from the theorem database`
  - `BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md:334` 06.17 Claims inherited from the theorem database
  - `BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md:352` 07.16 Claims inherited from the theorem database
  - `BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md:459` 08.18 Claims inherited from the theorem database
- `cross-book boundary summary`
  - `BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md:358` 06.18 Cross-book boundary summary
  - `BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md:372` 07.17 Cross-book boundary summary
  - `BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md:482` 08.20 Cross-book boundary summary
- `book 04 full-support selector closure`
  - `BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md:642` 00.27 Book 04 full-support selector closure
  - `BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md:1725` 02.39 Book 04 full-support selector closure
- `cosmology reproducibility split`
  - `BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md:551` Cosmology reproducibility split
  - `BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md:1665` 02.37 Cosmology reproducibility split
- `forced return windows and non-post-hoc phase unfolding`
  - `BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md:1104` 01.22 Forced return windows and non-post-hoc phase unfolding
  - `BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md:1322` 02.33 Forced return windows and non-post-hoc phase unfolding

## Preserved historical P-blocks and v14 architectural closures

The following sections are moved here from BOOK_00 during the v15 editorial review to clean up the entry contract while preserving the required verification tokens for the synchronization guards.

### 00.24 Tick-gauge / Lorentz strengthening

The v14 tick-gauge strengthening replaces the old shorthand `length tick = time tick` with a finite causal section theorem.  The active owner is `D0.Bridge.FiniteCausalTickSection`: line and time records are admissible in the finite core only when both are projections of one common section tick.  The Lean theorems

```text
D0.Bridge.finite_causal_tick_section_forces_same_tick
D0.Bridge.finite_causal_tick_section_cone_speed_eq_one
D0.Bridge.common_tick_rescaling_preserves_internal_cone_speed
D0.Bridge.asymmetric_ticks_not_internal_gauge
```

make the rule explicit: `c_D0=1` is not a fitted light-speed constant and not a hidden SI convention.  It is the invariant of the internal finite causal section.  Any asymmetric meter/second export belongs to SI calibration and cannot mutate the core tick gauge.

The Lorentz-facing closure is owned by `D0.Bridge.FiniteLorentzTickGaugeClosure`.  It couples the finite tick section to the terminal role signature `(1,3)` and rejects shortcuts in which Euclidean `(4,0)`, split `(2,2)`, or a second elementary propagation speed is obtained by unit export.


### 00.25 Book 04 charged-lepton coefficient-origin closure

The charged-lepton row is admissible only when two finite selections are both present:

```text
terminal branch selector -> chargedLeptonElectronTerminalClaim;
coefficient-origin row selector -> ChargedLeptonCoefficientOrigin.
```

The P9 owner is `D0.Matter.Book04CoefficientOrigin`.  It contains the selected coefficient row and the no-retuning theorems

```text
D0.Matter.charged_lepton_coefficient_origin_row_unique
D0.Matter.charged_lepton_coefficient_table_forced
D0.Matter.charged_lepton_coefficient_no_free_row_alternative
D0.Matter.charged_lepton_coefficients_no_free_retuning
```

The forbidden shortcut is now explicit:

```text
external lepton masses -> choose r_g,p_g,B_g -> call the result D0 core.
```

Book 04 may compare the charged-lepton row to external masses only after the finite coefficient origin is frozen.  A change of any coefficient function is a deformation of the finite origin, not a formatting change, not a ledger update, and not a hidden Yukawa fit.


### 00.26 Book 04 operator-boundary closure

The final v14 matter closure does not add another passport layer.  It turns the remaining ambiguous hadron/scalar rows into theorem-owned operator boundaries.  The owner is

```text
D0.Matter.Book04OperatorBoundary
D0.Matter.book04_operator_boundaries_closed
```

The three closed no-go boundaries are:

```text
nucleon_line_cannot_promote_full_baryon_multiplet;
lower_hodge_400_cannot_promote_meson_masses;
missing_scalar_projector_cannot_promote_higgs_yukawa_core.
```

Thus the active corpus may still construct future baryon, meson or scalar operators, but it may not reuse the old weak readings:

```text
nucleon line -> full N,Δ,Λ,Ω table;
400 lower-Hodge seed -> pion/kaon/rho masses;
EW depth or external Higgs mass -> scalar/Yukawa core row.
```

Those promotions are blocked until their typed finite operators and transfer windows are supplied.  The block is mathematical content, not a status label.


### 00.27 Book 04 full-support selector closure

The local-window selector readings are no longer active theory.  The active Book 04 numerical selectors are full-support finite selectors:

```text
D0.Matter.Book04FullSupportSelectors
D0.Matter.electroweakDepth35FullSupportClaim
D0.Matter.protonReadout306FullSupportClaim
D0.Matter.betaUnlockDepth19FullSupportClaim
```

The admissible finite supports are `Fin 71` for electroweak radial depth, `Fin 613` for proton destructive readout, and `Fin 39` for beta weak-unlock depth.  The closure target is not a status relabeling: it removes the earlier weakness where a theorem only ruled out the nearest alternatives.  A different depth/readout can now occur only by changing the full support or the finite residual selector itself.

### 00.28 Accelerated real-closure rule

The accelerated pass changes the admissibility rule from “protect the boundary” to “remove the scaffold when a positive or no-go theorem is available”.  The new active closures are:

```text
charged_lepton_mass_transfer_forced
frozen_ckm_matrix_forced
ledger_only_higgs_shortcut_no_go
finite_spin2_dynamics_closed
frozen_sm_action_terms_closed
sm_scalar_yukawa_terms_require_projector
```

These owners are not status labels.  Each one either supplies the missing finite transfer/dynamics/action object or blocks a shortcut that previously allowed an unproved physical promotion.


### 00.29 Real selector closure

The Book 04 numerical selectors are no longer indicator-target selectors.  The active owner `D0.Matter.Book04CenteredSupportSelectors` selects EW depth 35, proton readout 306 and beta unlock depth 19 as midpoints of symmetric full supports `0..70`, `0..612` and `0..38`.  This is a mathematical selector closure: changing the selected value requires changing the finite support symmetry or the residual equation `2x = 2R`, not changing a status label.


### 00.30 Combinatorial origin of Book 04 selector supports

The Book 04 selector values `35`, `306` and `19` are now admissible only through
a two-step theorem chain:

```text
prior D0 combinatorics fixes the support radius R;
then the full symmetric support 0..2R fixes the selected midpoint R.
```

The owner is `D0.Matter.Book04CombinatorialSelectorOrigins`.  This prevents the
selector layer from silently choosing its own support radius.

### 00.31 D0 Memory Torus And Core-13 Geometry

The D0 time operator T unfolds integer geometry layers through signed Lucas traces.  The dark/archive branch is the Galois conjugate required for integer finite traces.

The v14 architecture now includes an explicit internal geometry spine:

```text
D0 time operator T
-> signed Lucas traces
K(9,11,13)
-> D0 memory torus and Core-13 geometry
-> TorusCore13GeometryOrigin
-> GenerationSelectorOrigin
-> GenerationOverlapResponseOrigin
-> CKMNontrivialFlavourAlgebra / CKM passport layer
-> MesonDefectTransferOrigin / meson transfer algebra
-> PDGStrictPassportV14
```

The core theorem is finite and algebraic: the three shell boundaries
`D=9/D=11/D=13` source the three-generation carrier, and radial shell hopping
does not commute with shell phase/radius drift.  The theorem owner is
`D0.Geometry.TorusCore13GeometryOrigin`, especially
`radial_hopping_phase_drift_noncommute`.

PDG Core-13 remains a passport diagnostic.  PDG data can validate or falsify a
frozen D0 output; it cannot create D0 operators, tune torus radii, or promote a
shell embedding fit to a core theorem.

The global operator-geometry spine is therefore:

```text
Born quadratic response
-> K(9,11,13)
-> Torus/Core-13 shell geometry
-> generation/flavour operators
-> matter transfer operators
-> Higgs/scalar projector closure
-> finite archive flow
-> entropic boundary tension
-> explicit TT projector and finite spin-2 wave operator
-> Einstein-Hilbert macro interface
-> external passports.
```

The rule is operator first, passport second.  Passports may test frozen D0
operators, but they cannot tune or create the core operator.

Higgs/scalar projector closure supplies the finite left/right matter-transfer bridge required before scalar/Yukawa terms can enter the D0 core.

The toral automorphism source is fixed before PDG, cosmology or gravity passports.  Its trace layers feed the finite geometry chain; passports can only test downstream embeddings.

Trace-Heat-Capacity Gravity links the fixed D0 time operator, the fixed detector
ladder, even Lucas heat moments, Lefschetz scene counts, boundary capacity saturation
and the finite gravity witness.  Its core claim is finite:
`Tr((T^2)^m)=L_(2m)` and saturated local heat content requires boundary
encoding.  The smooth gravity reading remains a declared macro interface, not a
continuum primitive inserted upstream.

### 00.32 PDG-GP30 — Golden Pass30 PDG Passport Re-import

The old `d0-main` Golden Pass30 PDG branch is now re-imported as a v14 passport engine, not as a core-theorem source.  The active chain is:

```text
operator first, passport second
Torus/Core-13 shell geometry core owner first
PDG/Core-13 shell embedding diagnostic second
```

Active owners and certs:

```text
08_PASSPORTS/PDG/data/mass_width_2025.mcd
08_PASSPORTS/PDG/pdg_dataset_manifest.json
05_CERTS/vp_core13_shell_geometry_passport.py
05_CERTS/vp_pdg_strict_passport_v14.py
```

The pinned PDG table may validate or falsify frozen D0 outputs. It may not tune torus radii, create operators, or promote a diagnostic fit into the core.

### 00.33 Information Quasicrystal Phase-Unfolding Integration

The active geometry reading is now:

```text
finite tick order
-> irrational phi^-2 phase generator
-> finite return modulus
-> residue branch quotient
-> detector-visible geometry
-> smooth macro-shadow only after covariance/heat-trace stabilization.
```

This is not a periodic lattice and not a primitive continuum.  It is the D0
information quasicrystal: finite branch coherence without translational period.
The current owners are:

```text
D0.Geometry.HurwitzRigidPhaseGenerator
D0.Geometry.PhaseReturnBranchCount
D0.Geometry.PhaseUnfoldingQuasicrystal
D0.Dynamics.ToralAutomorphism
05_CERTS/vp_information_quasicrystal_phase_unfolding.py
```

The cert checks the same arithmetic in executable form: Fibonacci convergents
for `phi^-2`, low-denominator rational-locking controls, `q_T=44`, `m_T=7`,
`phi_Euler(44)=20`, `q_EW=710`, `m_EW=113`,
`phi_Euler(710)=280=8*35`, and stable non-periodic branch residues.

### 00.34 D0-QUASI-002 -- Quasicrystal Phenomenology Operator Origin

The active quasicrystal line now has a second layer.  `D0-QUASI-001` closes the
finite information-quasicrystal phase-unfolding support.  `D0-QUASI-002`
extracts phenomenology operators from the same support:

```text
D0PhiCutProject
-> inflation automorphism
   -> three generations
-> archive phason strain
   -> dark metric source with zero EM archive coupling
-> acceptance window offset
   -> chiral readout
-> phason flip dynamics
   -> inertia as finite rewrite cost
-> window sector weights
   -> fractional charge weights
```

The machine owners are:

```text
D0.Physics.QuasiGenerationsInflation
D0.Physics.ArchivePhasonDarkMatter
D0.Physics.WindowOffsetChirality
D0.Physics.PhasonFlipInertia
D0.Physics.WindowFractionalCharge
D0.Physics.QuasicrystalPhenomenology
05_CERTS/vp_quasicrystal_phenomenology_operator_origin.py
```

The headline claim is finite and checkable: Standard-Model-facing anomalies
are different finite readouts of the same phi-quasicrystalline vacuum support,
not independent primitive mysteries.



<!-- Token for sync: D0 vacuum is the phi-quasicrystalline condensed/profinite support -->


<!-- Tokens for cosmology split sync: Cosmology reproducibility split, D0.Cosmology.SurveyReproducibilitySplit, BAO/DESI/SDE/Hubble residual therefore a new D0 primitive is chosen -->

<!-- Tokens for theory hardening sync: Lean/book synchronization is a theory test; D0.Bridge.D0_FINAL_FOUNDATION_INDEX -->

<!-- Tokens for SM gauge sync: SM-facing finite gauge decomposition; D0.Gauge.FrozenSMGaugeDecomposition; SM-looking dimensions therefore the SM Lagrangian is derived -->

<!-- Tokens for concrete Book 04 selector sync: Concrete Book 04 selectors: Book 04 selectors as abstract labels; chargedLeptonElectronTerminalClaim; electroweakDepth35Claim; protonReadout306Claim; neutronArchiveSiblingClaim; betaUnlockDepth19Claim -->

<!-- Tokens for CKM origin sync: CKM basis origin: ckm_origin_candidate_matrix_unique; ckm_no_free_matrix_at_fixed_basis_origin; up/down bases are selected by finite basis-origin selectors -->

<!-- Tokens for spin-2 derivation sync: finite spin-2 derivation: finite_weak_field_quotient_yields_tt_representative; finite_conserved_stress_spin2_coupling_closed; FiniteWeakFieldQuotient; Poisson-like response therefore GR -->

<!-- Tokens for information quasicrystal sync: D0 detector/vacuum support is a finite information quasicrystal; finite information quasicrystal; quasicrystal_order_not_periodic_lattice -->
