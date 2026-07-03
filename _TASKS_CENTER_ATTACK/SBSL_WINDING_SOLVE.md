# SBSL two-tone winding — the solve (v1–v5), REPORT-ONLY

**Status:** REPORT-ONLY computation record. The frozen pre-registration `P-SBSL-1`
(`ANALOGY_BRIDGE_LAYER.md`, made BEFORE any simulation contact) stays frozen — this document
records the first quantitative slice of the theory side and touches the pre-registration ONLY
through its own stated falsifier language. No registry row edited by this document.
Scripts: `sbsl_rp_winding_v{1..5}.py`, outputs `sbsl_v{3,4,5}_out.txt` (this folder).

**Literature status (scout, arXiv-verified):** two-tone bubble drives in print are all
integer-harmonic; winding numbers for the driven bubble are published for SINGLE-tone only
(Parlitz–Lauterborn Farey organization). The quasiperiodic (irrational-ratio) two-tone winding
computation below appears to be new. NOT claimed: novelty beyond that scoping.

## Setup (fixed across v2–v5)

Rayleigh–Plesset, water (ρ=998, μ=1.002e-3, σ=0.0725, p₀=101325, κ=1.4), R₀=10 μm;
linearized natural frequency f₀ = 346.1 kHz; drive 1 at f₁ = 0.8 f₀ = 276.9 kHz, p₁ = 0.80 p₀;
drive 2 at f₂ = ρ f₁, p₂ = 0.35 p₀; IC (R₀, 0). Observable: stroboscopic rotation number w —
angle of strobed (R−R₀, Ṙ) about the strobed centroid, unwrapped, per drive-1 period.
LSODA, rtol 1e-8; resolution in w: ~1/N_meas.

## Established results

1. **v1 regime lesson (recorded null):** a 5 μm bubble at 26.5 kHz (f₀/25, the classic SBSL
   band) is quasistatic — w ≈ 0 everywhere, no winding structure at moderate drive. The
   tongue-bearing regime is near-resonance nonlinear (the Parlitz–Lauterborn window). The
   frozen P-SBSL-1 targets the strong-collapse flash-phase observable, which this moderate
   regime does NOT probe — nothing here can confirm or falsify P-SBSL-1 by itself.
2. **Rigid-tracking branches, exact (v3, controls in v4/v5):** in the tail ρ ≥ 1.66 the
   measured w equals 1 − frac(ρ) to ~1e-4 (single torus; skew-product rigid following of
   drive 2). Below 3/2, w = frac(ρ)/2 exactly (period-doubled torus); above 3/2, the mirror
   branch w = (1−frac(ρ))/2. Machinery validation: deterministic reproducibility across runs
   to 1e-6 (repeated grid points v3↔v4).
3. **ρ = 3/2: locked EXACTLY at the rational, tongue narrower than 2.5e-3** [CORRECTED by v5b —
   the earlier "not a tongue" reading was an error of record, fixed here]. The two doubled-torus
   branches cross at w = 1/4 at ρ = 3/2 and the NEIGHBORS track the rigid lines with slope ±1/2
   (no wide plateau); but AT 3/2 exactly the cluster test gives r₄ = 0.0000 — a genuine locked
   orbit of period 4T₁ (the drive's common period 2T₁, doubled), invisible to the coarse scan
   because the tongue is narrower than the 2.5e-3 grid. (A disordered window sits just BELOW
   3/2, ρ ∈ [1.4825, 1.4975].)
4. **GOLDEN POINT: no lock, reproducibly (v3+v4+v5).** Twin points ρ = φ and φ+3.4e-5
   reproduce to 1.3e-4 (= resolution); across [1.6155, 1.6205] at step 5e-4 the rotation
   number wanders (0.167–0.185) with NO two consecutive points equal — upper bound on any
   lock interval containing φ: **width < 5e-4**, and w matches NEITHER rigid branch (a
   nontrivially dressed quasiperiodic response).
5. **v4 correction of v3 (recorded honestly):** v3's apparent w = 1/4 plateau on
   [1.630, 1.635] (three coarse-grid points agreeing to 2e-6) is NOT a clean plateau — at
   step 5e-4 interleaved points fluctuate in [0.2489, 0.2539]. The repeated points carry the
   locked-orbit fingerprint (identical w with offset −1.5e-4 from exact 1/4 = the finite-strobe
   edge effect of a period-4 orbit); the interleaved points do not. Same pattern at the golden
   convergent 13/8 = 1.625: w = 0.124777 ≈ 1/8 (same offset scale), confined to < ±5e-4.
6. **v5 attractor-type verdict:** (see below — cluster diagnostic + long transient).

## v5 verdict (cluster diagnostic, n_trans=2000, n_meas=800)

Cluster ratio r_q := max over residue classes (strobe index mod q) of class diameter, divided
by attractor diameter. A period-q locked orbit gives r_q → 0; a torus gives r_q = O(1).

- **ρ = 13/8 = 1.625 (φ-convergent): GENUINE PERIOD-8 LOCKED ORBIT — r₈ = 0.0000** (strobe
  collapses onto 8 machine-tight points), w = 0.1246 ≈ 1/8, r₄ = 0.81 (period 8, not 4).
  Neighbor 13/8 − 5e-4 is already a torus (r₈ = 0.96) → **tongue width < 1e-3.** At ρ = 13/8
  the two-tone drive is periodic with period 8T₁; the response locks to it — a true
  drive-ratio Arnold tongue, resolved.
- **The "1/4 plateau" is DEAD:** with long transient every point in [1.630, 1.635] is a torus
  (r₄ ≈ 1.0), including v3/v4's repeating points (their agreement was finite-transient
  reproducibility + coarse-grid aliasing; with n_trans=2000 they shift to 0.24970 and the
  in-between points still differ). The region is w ≈ 1/4 PROXIMITY (resonance pulling toward
  the f₁/4 subharmonic) with NO capture. Error of record for v3's plateau reading, corrected
  here.
- **GOLDEN: torus, r₄ = r₈ = 1.0000** — no lock, converged, machine-clean.
- **Control ρ = 1.66: torus, w = 0.3398** = rigid line 1 − frac(ρ) — machinery sanity holds.

## v5b verdict (`sbsl_v5b_out.txt`)

| ρ | w | cluster | verdict |
|---|---|---|---|
| 3/2 exact | 0.2502 | r₄ = 0.0000 | LOCKED, period 4T₁ (doubled common period) |
| 8/5 exact | 0.19997 ≈ 1/5 | r₅ = 0.0000 | LOCKED, period 5T₁; both ±5e-4 neighbors tori |
| 13/8 exact | 0.1246 ≈ 1/8 | r₈ = 0.0000 | LOCKED, period 8T₁; −5e-4 neighbor torus |
| φ | 0.1727 | all r = 1.0000 | TORUS — no lock, bound < 5e-4 |
| 5/3 exact | 0.3335 = 1−frac | all r = 1.0000 | NO lock — rigid tail, response enslaved to drive 2 |

## The computed structure (final, this regime)

1. There is a bounded **interaction window** in ρ (≈[1.44, 1.65] here): outside it (e.g. 5/3)
   the single response torus rigidly follows drive 2 (w = 1−frac(ρ) exactly) — no free phase,
   no locking at all, even at the lowest-denominator rational in the scan.
2. Inside the window, **every sampled rational locks exactly at the rational** — 3/2 (period
   4T₁), 8/5 (period 5T₁), 13/8 (period 8T₁) — with machine-exact strobe clustering
   (r_q = 0.0000), and **every tongue is narrower than 1e-3–2.5e-3** in ρ despite the strong
   second tone (p₂ = 0.35 p₀): the response torus is strongly normally hyperbolic.
3. **The golden point does not lock** (torus; lock-width bound < 5e-4 = the resolution of the
   dense scan), and its w matches neither rigid branch — a nontrivially dressed quasiperiodic
   response. The two rationals that DO lock nearest φ in the window are its own convergents
   8/5 and 13/8 — as continued-fraction structure demands (the convergents are the
   moderate-q rationals nearest φ).
4. No wide subharmonic plateau exists at this amplitude (the v3 "1/4 tongue" was aliasing +
   transient; killed by the cluster test — error of record, corrected in v5 section).

## v6: tongue widths vs second-tone amplitude (`sbsl_v6_out.txt`)

Right-edge half-widths by log-bisection of the cluster test (factor-~2 brackets; reduced
n_trans=1200/n_meas=320 — accuracy caveat recorded):

| p₂/p₀ | 3/2 | 8/5 | 13/8 | golden |
|---|---|---|---|---|
| 0.15 | [1.3e-4, 2.1e-4] | [2.4e-5, 3.7e-5] | [2.4e-5, 3.7e-5] | unlocked (r ≥ 0.995) |
| 0.35 | [1.3e-4, 2.1e-4] | [3.7e-5, 5.6e-5] | [3.7e-5, 5.6e-5] | unlocked (r ≥ 0.996) |
| 0.60 | [1.5e-5, 2.4e-5] | NOT locked (attractor changed) | NOT locked (attractor changed) | attractor changed (w ~ 0.02–0.06, r ~ 0.75–0.87) |

Findings, stated conservatively:

1. **First tongue-width measurements for this system:** at p₂ ∈ {0.15, 0.35} p₀ the 3/2 tongue
   is ~1.3–2.1e-4 wide, the convergents 8/5 and 13/8 are ~2–6e-5 — q-ordered (wider at lower
   denominator), and the convergent tongues WIDEN slightly with p₂ (2.4–3.7e-5 → 3.7–5.6e-5).
2. **The golden point stays unlocked at every amplitude tested** (r ≥ 0.995 at 0.15 and 0.35;
   at 0.60 the whole organization changes — see 3).
3. **No monotone route to tongue overlap:** at p₂ = 0.60 p₀ the doubled-torus organization
   DISSOLVES before tongues can widen toward each other — the convergent locks vanish, the 3/2
   tongue narrows an order of magnitude, and the attractor family changes (near-zero winding,
   intermediate clustering; not classified further here). The classic circle-map scenario
   (tongues widen until the golden torus is the last survivor) is therefore NOT reproduced by
   amplitude-cranking in THIS regime — the system exits the torus regime first. The
   golden-last-locked ORDERING remains untested; what IS established is the fixed-amplitude
   contrast (convergents lock, φ does not).

## Honest summary against the frozen expectation

- The golden-side clause of P-SBSL-1's intuition (φ last-unlocked) is CONSISTENT here:
  rationals lock exactly at their points inside the interaction window, φ does not
  (bound 5e-4). But the tongue widths at this moderate drive are all < 2.5e-3, so a
  width-ORDERING test ("golden is the last to lock as drive grows") is not yet resolved —
  it needs the tongue-width-vs-amplitude scan, and ultimately the strong-drive/collapse
  (Keller–Miksis) regime where the pre-registration's flash-phase observable actually lives.
- Sharpened experimental guidance for P-SBSL-1: tongues at rational drive ratios are REAL but
  extremely narrow at moderate drive (measured: 1e-5–2e-4, v6); an experiment scanning ρ at
  coarse steps would see the rigid-tracking branches and MISS every tongue. "Drive harder" does
  NOT rescue this: at p₂ = 0.60 p₀ the torus organization dissolves before tongues widen (v6.3).
  The pre-registration's ratio grid must resolve ~1e-5 near the target rationals, or the
  observable must move to the collapse regime as pre-registered.
- None of the moderate-regime results confirms or falsifies P-SBSL-1 (its observable is the
  collapse flash phase); they are the theory-side machinery + the first quantitative
  tongue/no-tongue map for a quasiperiodically two-tone-driven bubble.

## COLLAPSE-REGIME PILOT (Keller–Miksis, `sbsl_km_collapse_v1.py`, `sbsl_km_v1_out.txt`)

The pre-registered observable itself, first computation: KM with radiation damping, R₀=4.5 μm,
f₁=26.5 kHz, p₁=1.25 p₀ (SBSL-grade, R_min down to 0.07–0.26 R₀), second tone p₂=0.25 p₀ at
ρf₁. Flash-phase proxy: θ_k = ω₂ t_k mod 2π at main-collapse events; discreteness measured by
normalized circular entropy over 36 bins (1 = uniform) on ~150–200 collapses.

| drive | ent | occupied bins |
|---|---|---|
| single-tone control (vs tone 1) | 0.306 | 3 — locked, validates the pipeline |
| ρ = 3/2 (q=2) | 0.401 | 6 |
| ρ = 8/5 (q=5) | 0.712 | 14 |
| ρ = 13/8 (q=8) | 0.729 | 18 |
| ρ = 1.55 (=31/20) | 0.842 | 26 |
| ρ = √2 | 0.884 | 30 |
| **ρ = φ** | **0.888** | **31** |

**The flash phase discretizes at rationals with entropy MONOTONE in the denominator and fills
densely at φ and √2.** Long-run resolution (v2, `sbsl_km_v2_out.txt`, n≈500–620 collapses with
a matched-n Monte-Carlo uniform reference band): 3/2 → ent 0.4465 (deep below the uniform band
[0.988, 0.995] — discrete); φ → ent 0.9200, which is high but OUTSIDE the uniform band
[0.985, 0.994] — the φ distribution is dense with NO discretization yet measurably non-uniform
(the correct signature of a quasiperiodic/SNA response: dense filling with modulated density).
The pilot's "at the uniform ceiling" phrasing at n≈150 is hereby corrected: the discriminator
is DENSITY vs DISCRETENESS (0.92 vs 0.45 at matched n), not exact equidistribution.
Honest caveats carried: (i) at rational ρ the drive is qT₁-periodic, so finite phase sets are
partly kinematic — the physics content is that the response IS phase-locked there (it could
have been chaotic) while at φ it never discretizes; (ii) resolved by v2 as above; (iii) pilot
grid only — no width/robustness scan yet; also at φ only ~499 qualifying main collapses arise
in 650 periods (collapse census varies with ρ — recorded, not interpreted); (iv) P-SBSL-1
remains FROZEN: this is theory-side; the pre-registration's test order (theory → experiment)
proceeds as stated.
