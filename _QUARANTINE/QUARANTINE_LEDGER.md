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

4. **Phantom cert (third incident, same class as #2/#3).**
   `vp_minimal_holographic_carrier.py` — cited by the v17 draft's "Theorem 1.8"
   ("K(9,11,13) is the unique minimal discrete holographic tensor network via
   Darboux symplectic conjugate-pair (+2 dimension) rule") at
   `03_THEORY_MAP/GOLDEN_COVERAGE_LEDGER.csv:811`
   (row `v17-BOOK-01-CONDENSED-FOUNDATIONS-AND-GRAPH-BIRTH-0677`, §01.8). The
   file is **absent on disk and never existed at any git commit** (verified
   `git log --all` empty), and it is **not** registered as OPEN/PROOF-TARGET in
   `CLAIM_TO_LEAN_MAP.csv` (grep = 0) — so it is a phantom cert, not an honest
   open target. Same class as the Golod–Shafarevich (`vp_golod_shafarevich_gap_160.py`)
   and "OpenAI 2026" (`vp_openai_tower_kerr_359.py`) phantom certs above: a
   named cert propping up a v17 uniqueness "Theorem" with no computation behind
   it. The *legitimate kernel* (the Darboux conjugate-pair `+2` extension rule
   as an alternate forcing of the `(9,11,13)` window) is captured honestly and
   without this cert in `_TASKS_CENTER_ATTACK/GAP_E_*_MEMO.md` and the
   `D0-WINDOW-9-13-DISSOLVE-001` PROOF-TARGET; the v17 "Theorem 1.8 + cert"
   framing is the over-claim to quarantine. Excluded from the corpus; do not
   import or cite as a passing cert.

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

## CVFT F4/F7 fabricated-control certs (retired 2026-07-05, replaced by reforges)

Four `05_CERTS/vp_cvft_*.py` certs that were the sole backing for `D0-CVFT-F4`
and `D0-CVFT-F7` CERT-CLOSED are **retired as fabricated-control theater** (sweep
F2; same class as the v17 phantom certs above, except these files DO exist on
disk — the fabrication is in their *contents*, not their absence). They are
kept on disk (still named by index/board CSVs) but are **non-load-bearing and
must not be cited as passing evidence**; the registry `python_cert` for F4/F7
now points at the reforged replacements.

- **`vp_cvft_uv_feedback_tail_bound_refined.py`** (F4) — fabricated negative
  controls over hardcoded literals; wrong owned constant `delta12 = 1e-6` vs the
  owned `δ₀¹² = 7.31e-12`.
- **`vp_cvft_ueff_pole_discipline.py`** (F4) — fabricated controls AND two
  hardcoded eigen-lists encoding the FALSE identity `spec(F) = |eig(U_eff)|²`
  (`0.64=0.8²`, `0.25=0.5²`); the owned relation is `spec(F_c) = 1 − σ²(U_eff)`
  for non-normal `U_eff`. Corroboration theater with mutually-inconsistent props.
- **`vp_cvft_boundary_channel_rank.py`** (F7) — fabricated `not-an-A4-proof`
  discipline control (never computed a non-saturation witness).
- **`vp_cvft_refined_logdet_rank_bound.py`** (F7) — fabricated `|z|-only-form`
  domain-discipline control (never computed a domain-discrimination witness).

**Replacements (live, scene-constructed, can-fail, exit 0 with 5 caught
controls each):** `05_CERTS/vp_cvft_uv_feedback_tail_bound_refined_REFORGED.py`,
`vp_cvft_ueff_pole_discipline_REFORGED.py`,
`vp_cvft_boundary_channel_rank_REFORGED.py`,
`vp_cvft_refined_logdet_rank_bound_REFORGED.py` (adjudication:
`_TASKS_CENTER_ATTACK/CVFT_F4_F7_REFORGE_REPORT.md`). F4/F7 stay
`PYTHON_CERTIFIED` (the Lean rank-block lift is compile-verified on scratch, NOT
in the built tree — no LEAN_PROVED flip). Interval-honesty note: between the
original `[8C]` closure and 2026-07-05, both CERT-CLOSED labels rested
exclusively on these non-verifying certs.

Also superseded (retire / mark non-load-bearing demos, no failure path):
`vp_cvft_boundary_rank_bound.py`, `vp_cvft_logdet_rank_bound.py`,
`vp_cvft_uv_feedback_tail_bound.py`.
