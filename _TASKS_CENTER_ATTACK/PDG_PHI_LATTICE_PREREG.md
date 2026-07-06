# PDG-PHI-LATTICE-DISCRIMINATION — pre-registered 3-arm design (FROZEN BEFORE ANY ARM IS RUN)

**Status:** DRAFT pre-registration; no arm executed at freeze time; no registry row edited.
Pre-flight: PDG / CORE13 / PHI-LATTICE / MESON-DOMAIN. PHI-LATTICE discrimination is unowned.
Cross-refs (not duplicates): D0-PASSPORT-CORE13-001 (owns the φ-fit diagnostic this test extends;
"no core promotion"), D0-GEN-MASS-001 (NO_GO_PROVED on generation-mass clustering — this campaign
claims NO core derivation of masses, only lattice discrimination), D0-TORUS-CORE13-GEOMETRY-001
(owned scene-side source of shell invariants), D0-LEPTON no-go family (untouched).

## Question (falsifiable, two-sided)

Does the D0 scene structure carry signal in the pinned PDG mass table — i.e. (Q1) is base φ
distinguished among bases at EQUAL expressible-point budget, and (Q2) are the GRAPH INVARIANTS
(Fibonacci-κ layer, Ω₈=8 window, zone shells) load-bearing beyond φ itself? Owner directive
2026-07-04: the φ-graph invariants, not φ alone, are the expected key.

## Frozen data & split

- Dataset: `08_PASSPORTS/PDG/data/mass_width_2025.mcd`, pinned by
  `08_PASSPORTS/PDG/pdg_dataset_manifest.json` (sha256 verified before parse). 317 unique ids.
- Train/holdout: the EXISTING protocol split (sha256(seed:pdgid), seed + fraction from
  `pdg_strict_protocol.json`) — 262 train / 55 holdout. NEVER refit after holdout is read.
- Strata: PRIMARY endpoint on all 317 (holdout-scored); SECONDARY descriptive stratum = the 12
  fundamental ids of `core13_geometry_protocol.json` (too few for a split; report only).

## The three arms (all scored by the same metric)

Metric M = median |log10(m) − nearest lattice point| over the scored set; lower is better.

- **Arm 1 (scene-pinned φ-lattice):** points n·log10(2) + k·log10(φ) + log10(κ), κ ∈ Fibonacci
  {F1..F12} (the repo's own BASIS layer, `vp_pdg_strict_passport.py:95-101`), integer bounds
  n,k ∈ [−16,16] (repo values). Its in-window distinct-point count defines the BUDGET **B**.
- **Arm 2 (base scan at equal budget):** for each β on grid [1.05, 2.20] step 0.005: same lattice
  form with κ ∈ Fibonacci, integer bounds RESCALED so the in-window distinct-point count is
  closest to B (density equalization — the v0 flaw of unequal density is thereby removed).
  Output: rank of φ in {M_β}.
- **Arm 3 (invariant-scrambled controls at φ, same budget):** (a) κ → arithmetic {1..12};
  (b) κ → shifted Lucas {L1..L12}; (c) shell metric: rerun the Core-13 3-circle shell fit
  (machinery of `vp_core13_shell_geometry_passport.py`) with scrambled shell_defs (zone sizes
  8/12/13 permutations) vs the true 9/11/13 — RMS comparison. Each control matched to budget B.

## Pre-registered acceptance criteria (frozen; no post-hoc thresholds)

- **A1 (φ discriminating):** holdout rank of φ in Arm 2 ≤ 5% of grid ⇒ discriminating;
  rank ≥ 50% ⇒ HONESTLY NON-DISCRIMINATING (recorded as such, no repair fits). Between: ambiguous,
  recorded as ambiguous.
- **A2 (invariants load-bearing):** Arm 1 beats EVERY Arm-3 control on holdout with margin
  ≥ 95th percentile of the null spread ⇒ graph invariants carry signal. Any control ties/beats
  Arm 1 ⇒ invariants NOT shown load-bearing (recorded).
- **Null gate (both must pass):** 200 log-uniform synthetic mass draws (same window, same n=317,
  same pipeline): A1 and A2 must each FAIL on ≥95% of synthetic draws, else the pipeline is
  non-discriminating by construction and NO positive conclusion may be drawn.
- Verdict vocabulary: "discriminating-confirmed" / "non-discriminating" / "ambiguous" only.
  FORBIDDEN regardless of outcome: "masses derived", core promotion, any registry status change
  from this campaign alone (respects D0-GEN-MASS-001 and the closure contract).

## Named risks & PRE-REGISTERED attack surface

- **S1 (strongest): density-equalization convention.** Equal-count-in-window is ONE fairness
  convention; a skeptic may propose equal-MDL-bits instead. Pre-commitment: report BOTH (count-
  equalized primary, complexity-sum-equalized sensitivity check); if they disagree on A1, verdict
  is "ambiguous", not cherry-picked.
- **S2: composite hadrons.** 305 of 317 are composites; a lattice claim on composites is weaker
  physics than on the 12 fundamentals. Mitigation: strata pre-declared; no fundamental-only
  post-hoc promotion if the 317 fail.
- **S3: β-grid degeneracies.** Near β = 2^{p/q} the two-generator lattice degenerates; such β get
  denser effective lattices at fixed bounds — density equalization handles this, but rational-
  ridge artifacts in the M_β curve are expected and will be plotted, not hidden.
- **S4: κ-layer double-dip.** Fibonacci-κ is φ-structured; giving it to ALL β arms (as done)
  slightly favors... actually disadvantages φ (others get φ's κ for free) — bias direction is
  AGAINST φ, acceptable; recorded.
- **S5: the v0 crude scan (φ rank 25/141, p≈0.2, biased) is superseded by this design; it must be
  cited in the results memo as the motivating negative, not suppressed.

## Execution order (loop discipline)

1. Freeze this file (git-add only at owner's discretion; no commit by agent).
2. Build `pdg_phi_lattice_3arm.py` implementing EXACTLY the above; run null gate FIRST;
   then train; read holdout ONCE.
3. Results memo + skeptic pass (mandate: attack S1-S5 + implementation fidelity to this prereg).
4. Verdict in the frozen vocabulary; memory updated either way.
