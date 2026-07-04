# D0 external-data scoreboard (real downloaded/published data, git-safe flow)

Honest status vocabulary: **PASSPORT** = data-consistent but post-hoc / not uniquely forced;
**SINGLE-MATCH** = one forced number or bridge that lands; **NEGATIVE** = corpus-labeled failure;
**OPEN** = honest no-go. There is **no** sharp multi-point discriminating data confirmation.

| prediction | D0 (parameter-free unless noted) | real data | agreement | status |
|---|---|---|---|---|
| PMNS sin²θ₁₂ | 1/3−2δ₀² = 0.30547 | NuFIT6.0 0.307±0.012 | 0.13σ | PASSPORT (post-hoc δ₀-family; degree-1 refit 1/3−δ₀/4 also <1σ) |
| PMNS sin²θ₁₃ | φ⁻⁵/4 = 0.02254 | NuFIT6.0 0.02195±0.00058 | 1.02σ | PASSPORT (post-hoc δ₀-family) |
| PMNS sin²θ₂₃ | 1/2+δ₀/2 = 0.55902 | NuFIT6.0 0.561±0.015 (UO) | 0.13σ | PASSPORT (upper octant is an unforced sign choice) |
| sin²θ_W (on-shell) | 0.22328 | 1−M_W²/M_Z² = 0.22321±0.00029 | 0.23σ | SINGLE-MATCH |
| m_s/m_d | 20 (=\|ℤ/44*\|) | FLAG 20.01±0.55 | 0.02σ | SINGLE-MATCH (bridge) |
| Cabibbo sinθ_C | 1/√20 = 0.22361 | \|V_us\| 0.22431±0.00085 | 0.83σ | SINGLE-MATCH (bridge, GST) |
| m_μ/m_e integer | 206 (=L₁₁+L₄) | PDG 206.768 | int matches | SINGLE-MATCH (decimals HYP) |
| α⁻¹ leading | 359/φ² = 137.1258 | CODATA 137.036 | 0.07% | STRUCTURAL (full value CHK; 9-digit uses seam params) |
| dark energy | dynamical (w≠−1), convexity | DESI DR2 Δχ²=4.73 vs ΛCDM | evolving confirmed | PASSPORT (evolving confirmed; thawing corner NOT forced — over-read, corrected) |

Discipline: the PMNS δ₀-family is **not** discriminating — the degree-permutation control breaks only at
*fixed* coefficient; refitting the coefficient at degree-1 recovers <1σ (`1/3−δ₀/4 = 0.30382`, 0.62σ), and
several simple δ₀-forms hit <1σ. sin²θ₁₃ is 1.02σ; the θ₂₃ octant is an unforced sign choice. DESI
thawing-corner claim was an over-read (0/6 natural phason→w(z) maps land in the corner), corrected in
`BOOK_08 §08.13`. sin²θ_W had a self-inflicted wrong-definition error (caught, corrected). All data git-safe:
manifests+SHA256+fetch committed, raw data gitignored. Provenance in `manifests/`.

## Additional (passport-level)
| prediction | D0 | real data | agreement | status |
|---|---|---|---|---|
| Σm_ν | Δα²·m_e = 0.070–0.088 eV | [0.058,0.072] eV window (osc+cosmo) | right scale | PASSPORT (geometric-Δα in window; seam-Δα mild tension) |
| E8 m₂/m₁ | 2cos(π/5)=φ=1.618 | Coldea 2010 1.618(10) | exact | SINGLE-MATCH (passport) |
| CMB n_s | (no prediction — no-go) | Planck 0.9649±0.0042 | n/a | OPEN (honest no-go) |

## Dark sector (real data)
| prediction | D0 | real data | result | status |
|---|---|---|---|---|
| dark matter (phason halo) | simple radial smoothing kernel | SPARC 175 galaxies | worse than baryon-only in 91% | NEGATIVE (corpus-labeled failure; kernel rejected) |

## Corpus's own real-data certs (run) + cert-layer audit
| cert | data | result |
|---|---|---|
| vp_pdg_strict_passport | PDG 317 particles (pinned) | PASS — seam-α falsifier Δα=4.15e-4 < ε²=4.53e-4 (D0 not excluded); φ-lattice median_rel 9e-4 |
| vp_sparc_phason_halo_failure_diagnostics | SPARC 175 gal (downloaded) | phason halo FAILS (91% worse than baryon) — honest negative |
| vp_h0_evolving_w | (reads no data) | honestly PROOF-TARGET (not a confrontation) |
| vp_desi_bao_sde_real_data | synthetic 3-tracer + placeholder metrics | DEMO scaffold (flagged; not a real DESI test) |

Data-gated cert layer: mostly real-capable scaffolds (raw data not shipped — git-safe by design), largely
honestly labelled; 1 placeholder-metric flaw (`vp_desi_bao_sde_real_data`). Substantive confrontations = the
downloaded-data analyses above + the particle scoreboard.

## Gravitational waves (real GWOSC data)
| prediction | D0 | real data | agreement | status |
|---|---|---|---|---|
| BBH radiated-mass fraction | ξ=η(3/8+φ⁻¹(4η−1)+spin) | GWOSC 405 clean BBH | rmse_d0 0.0069 < spin-only 0.0086 | PASSPORT (frozen φ⁻¹; joint best-fit c≈0.58–0.64 ≠ φ⁻¹, not discriminating) |

## Scaffolds (no sharp forced prediction — not tested against data)
| cert | why not tested |
|---|---|
| vp_cmb_phason_flip_entropy_passport | scaffold (synthetic/manifest modes); no sharp forced n_s/Cl prediction (CMB n_s is a no-go) |
| vp_neutrino_phason_decoherence_passport | explicit scaffold (docstring: "manifest-only, SKIP without data"); no implemented sharp flavor-ratio prediction |

## Adversarial-verification note (the two former "standouts")
PMNS δ₀ and LIGO φ⁻¹ were both **downgraded from "discriminating confirmation" to post-hoc passport fits**
(self-verified, now reflected in the rows above and in `BOOK_04 §04.5` / `BOOK_07 §07.48` / the registry):
- PMNS: the "discrimination" freezes the tuned coefficient and permutes only the degree; the coefficient-refit
  rescue and multiple simple δ₀-forms landing <1σ show it is not discriminated.
- LIGO: (4η−1) is 98.5% collinear with the base; the frozen 3/8 dictates the slope; a joint fit gives
  c≈0.58–0.64 ≠ φ⁻¹ with slightly better rmse.
Honest survivors are single-number/bridge matches (sin²θ_W on-shell, m_s/m_d, Lucas-206, Coldea-φ, α-leading,
PDG seam-α falsifier), one honest negative (SPARC dark matter), and a corrected over-read (DESI thawing corner).
