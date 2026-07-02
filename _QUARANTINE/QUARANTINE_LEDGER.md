# Quarantine Ledger

Contents of `_QUARANTINE/` are **excluded from the corpus**: they must not be
imported, cited, or promoted. Kept temporarily for forensic reference and for
harvesting their *legitimate* reach (Phase 8E of the refactor plan), after which
`v17_overshoots/` is deleted (git history retains it).

## v17_overshoots/ — the v17 book draft (10 books)

The v17 "reach" draft is condensed but contaminated by three load-bearing
overshoots that violate D0's own admissibility contract (`BOOK_00 §00.4` "no
claim may move upward by rhetoric"; `BOOK_05 §05.5` demotion is part of claim
discipline). All three were flagged by the transfer documents
(`add/files/D0_PHILOSOPHY_AND_METHOD.md §8`) and confirmed by a dedicated audit.

1. **Status-as-dogma.** `BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md` ~lines
   299, 305–344 (§00.16 "Immutable Core Synthesis", §00.19 "The Final Closure",
   §00.20 "Grand Singularity Lock"): theorems stamped "Immutable / Modification
   forbidden / Promotion irreversible", and `BOOK_05` §05.9b/c "Demotion is
   forbidden". A clause that forbids its own revision is a dogma, not a theorem —
   and §05.9c sits inside the verification book that *defines* demotion.

2. **Coefficient-as-group.** `BOOK_08_COSMOLOGY_...md` ~lines 151–170 (and
   `BOOK_03` §03.8c): the Golod–Shafarevich "Δ_GS = 1/160" promoted to a
   `D0.Core` theorem driving Λ. But `1/160 = 360/160 − 359/160` is the arithmetic
   remainder of a hand-built quadratic's coefficients (`160 = 2·|Ω₈|·γ`), not a
   generator/relation count of any constructed pro-p tower. No group is exhibited.
   Phantom cert `vp_golod_shafarevich_gap_160.py` (absent on disk).

3. **Fabricated citation.** "OpenAI 2026" (class-field-tower disproval /
   unit-distance counterexample) cited ~5× across BOOK_00/01/05/08 as the
   external authority for carrier uniqueness, with phantom cert
   `vp_openai_tower_kerr_359.py` (absent on disk). No such work exists.

## Legitimate reach to harvest before deletion (Phase 8E)

These v17 intuitions are sound and should be re-entered as proper `PROOF-TARGET`
rows (not Core): the R-operator partial-trace family, `R_n = φⁿ − 1`, `Ω₈ ≅ Q₈`,
the Schur (1/3)I₃ isotropy, the Ostrik/Gleason/Darboux φ-rigidity, and the
IR-Lorentz Schur curvature bound `|c₄| ≤ (5744/33)·δ₀¹²` (`5744 = 16·359`).

## Iter-21 constructive reforges (transformations, **not** discards)

These two are recorded here for provenance: the artifact was not deleted as an
overshoot — its *legitimate kernel* was reforged into a derived object, and the
over-claiming wrapper was retired. (Same move as the v17 `I_f = Tr(log T)` →
`h_KS` reforge: keep the information functional, drop the dressed-up framing.)

1. **`q_res` α-fit → closure holonomy.** The fitted multiplicative residue
   `q_res = 1.0000043305576405` raised to `5/8 + δ₀/384` (`BOOK_02 §02.13`, the
   old `α_D0⁻¹ = α_top⁻¹·q_res^(…)` line) was a tuned number with no derivation.
   Its legitimate kernel — that the α-correction is a *small multiplicative seam
   factor* — is reforged into the **derived closure holonomy** `1 + h_KS·sin θ_seam`
   with `h_KS = ln φ`, `θ_seam = 12/5 = 2π₀(2−φ)` exact, depth `φ⁻¹⁷` (§02.13.h,
   `D0-SEAM-HOLONOMY-001` / `D0-ALPHA-HOLONOMY-002`, certs `vp_seam_holonomy_alpha.py`
   + `vp_pi0_discrete_angle.py` + `vp_q8_sin_channel.py`). The bare `q_res` decimal
   is **deleted** from the spine; the structure is THE, the 9-digit data match CHK,
   the last ~10⁻⁸ HYP. No bare fit survives.

2. **`D0-CVFT-F1` residue route → closed-negative.** The Dixmier/ζ-residue route to
   the α precision correction (`vp_cvft_clifford_fock_capacity.py`,
   `vp_zeta_residue_alpha.py`, `vp_feshbach_residue_amplitudes.py`,
   `vp_delta_alpha_pi0_moment.py`) is **closed-negative**: any residue carrying
   `ln φ` is transcendental (`∝ 1/ln φ`) and cannot land in `α_alg ∈ ℚ(φ)`
   (algebraic). The certs keep their *proven* content (the `2¹¹ = 2^{V₁₁}` capacity,
   `μ₁ = 1/rank`, `ζ_E(0)=359`, `ζ_E(−1)=α_top⁻¹`) and now print a
   `BLOCKED_RESIDUE_ROUTE_TO_DELTA_ALPHA` verdict pointing to the working holonomy
   route. `D0-CVFT-F1` stays `PROOF-TARGET` with the route honestly marked BLOCKED —
   a named closed-negative, not a hidden dead end.

## External-data review corrections (corrected reaches, **not** discards)

Recorded for provenance after confronting the corpus with real downloaded data
(`08_PASSPORTS/{DESI,SPARC,PDG,CKM,GWOSC}`). Each kept its *legitimate* content;
only an over-read wrapper was retired, via `BOOK_05 §05.5` demotion discipline.

1. **PMNS seam-topology `δ₀`-family: "discriminating THE rule" → EMPIRICAL-PASSPORT.**
   The three angles land `<1σ` (JUNO-2026 + NuFIT-6.0) — a genuine, non-trivial
   match, kept. But the "rule is THE / discriminating" wrapper was an over-read: the
   Lean directional theorem (`D0.Matter.PMNSSeamTopology`) is *true by construction*
   of the chosen signs (`+δ₀/2`, `−2δ₀²`, `φ⁻⁵/4>0`), the degree-permutation control
   breaks only at *fixed* coefficient, and refitting the coefficient at degree-1
   recovers `<1σ` (`sin²θ₁₂ = 1/3 − δ₀/4 = 0.30382`, `0.62σ`). Under joint
   (degree, coefficient) freedom the family is not discriminated. `D0-PMNS-SEAM-TOPOLOGY-001`
   demoted `CORE-FORMALIZED → EMPIRICAL-PASSPORT`; only `δ₀ = 1/(2φ³)` stays forced
   (cert `vp_pmns_seam_topology.py`, now failable on the "forced/discriminating" claim;
   book `§04.5`). The related `D0-MIXING-HIERARCHY-INVERSION-001` rank/nullity skeleton
   stays derived; its "delta0-corrections are derived" clause is corrected to passport.

2. **DESI dark energy: "convexity ⇒ the thawing corner" → convexity ⇒ *evolving* only.**
   The convexity `Δ²R_n = φⁿ(φ−1)² > 0` forces *dynamical/evolving* dark energy, and
   real DESI DR2 BAO confirms it (rejects ΛCDM, Δχ²≈4.7 BAO-only) — kept. But the
   claim that convexity lands in DESI's *thawing* corner (`w₀>−1, wₐ<0`) is an
   over-read: an explicit enumeration of the natural phason→`w(z)` maps
   (source ∈ {R,R′,R″} × direction `N=±ln a`) gives **0/6** in the thawing corner
   (all `wₐ>0` or phantom `w₀<−1`). Corner sign is map-dependent, stays HYP; book
   `§08.13` corrected. SPARC galaxy rotation stays a recorded **negative** result
   (D0's archive-halo does not fit the SPARC rotation curves), not buried.
