# D0 external-data program — final report ("do everything")

Git-safe: all raw data in cache/ (gitignored); committed = fetch scripts + SHA256 manifests + test scripts +
results (this dir). Reproducible; no data blobs in git. Datasets downloaded: DESI DR2 BAO, SPARC (175 gal),
GWOSC/GWTC (671 events), PDG mass_width 2025; + published NuFIT 6.0 / CODATA / FLAG values.

## Confirmed on real data
- **PMNS δ₀** (NuFIT 6.0): sin²θ₁₂ 0.13σ, sin²θ₁₃ 1.0σ, sin²θ₂₃ 0.13σ (upper octant). Discriminating
  (degree-permutation → 17σ). Parameter-free. STANDOUT #1.
- **LIGO BBH mass-defect** (GWOSC 405 events): D0 golden-ratio formula rmse 0.0069 beats spin-only 0.0086;
  the forced φ⁻¹ coefficient is DATA-OPTIMAL (best-fit 0.64 vs φ⁻¹ 0.618). Discriminating. STANDOUT #2.
- sin²θ_W (on-shell) 0.23σ; m_s/m_d=20 0.02σ; Lucas m_μ/m_e integer=206; Coldea E8 m₂/m₁=φ;
  PDG-strict seam-α falsifier Δα<ε² (D0 not excluded).

## Bridge / passport
- Cabibbo sinθ_C=1/√20 (0.83σ, GST bridge); α⁻¹ leading 359/φ²=137.126 (0.07%, full CHK).
- Σm_ν=Δα²·m_e ≈ 0.07–0.09 eV (right neutrino scale; precise value Δα-def-dependent).

## Partial / corrected / negative / open
- DESI DR2 dark energy: evolving DE CONFIRMED (Δχ²=4.73 vs ΛCDM); thawing corner NOT forced (corpus §565
  over-read — 0/6 phason maps give it; corrected).
- SPARC dark matter: phason halo FAILS (91% worse than baryon) — honest negative, corpus-labeled failure.
- CMB n_s: open (proven no-go, no prediction).

## Meta
- Data-gated cert layer = git-safe scaffolds, largely honestly labelled; 1 placeholder-metric flaw
  (desi_bao_sde_real_data); 2 scaffolds with no sharp prediction (CMB-phason-flip, IceCube-decoherence).
- Self-caught errors: sin²θ_W wrong-definition (200σ→0.2σ); "demo-scaffold" over-classification (spot-check fix).
- Caught corpus over-read: DESI thawing corner.

NET: D0 has a real cluster of data-confirmed predictions — two of them discriminating standouts (PMNS δ₀,
LIGO φ⁻¹ mass-defect) — plus honest bridges, one clear failure (dark matter), and one corrected over-read.
A calibrated physical theory with measured strengths and walls, separated by data not rhetoric.

## ⚠ POST-HOC CORRECTION (adversarial verification of the two standouts — both RETRACTED as confirmations)
Adversarial review + self-verification showed the two "discriminating standouts" are **post-hoc fits**, both via
the same trick (freeze one tuned knob, wiggle the other, report the blow-up as discrimination):
- **PMNS δ₀**: degree-permutation "discrimination" freezes the O(1) coefficient; refitting it rescues the wrong
  degree to <1σ. ~10 simple formulas hit sin²θ₁₂ <1σ (1/4+φ⁻⁶ beats it). sin²θ₁₃=1.02σ. Octant = unforced sign
  choice. → passport-level fit (matches corpus 'CHK'), NOT forced/discriminating.
- **LIGO φ⁻¹**: (4η−1) 98.5% collinear with base; frozen 3/8 dictates the slope; honest joint fit → c=0.58≠φ⁻¹,
  rmse better. → post-hoc fit, φ⁻¹ NOT data-selected.

REVISED honest bottom line: D0 has **no sharp multi-point discriminating data confirmation**. What survives are
single-number/bridge matches (sin²θ_W on-shell ~definitional, m_s/m_d bridge, Lucas-206, Coldea-φ, α-leading
0.07%, PDG seam-α falsifier), one honest NEGATIVE (SPARC dark matter fails 91%), and one corrected over-read
(DESI thawing corner). The impressive-looking PMNS/LIGO "confirmations" do not survive coefficient-freedom /
joint-fit scrutiny. This is the calibrated, honest data-confrontation state — weaker than the headlines suggested.
