# DESI DR2 BAO test — D0 dark-energy prediction (real downloaded data)

Data: DESI DR2 BAO ALL_GCcomb (13 pts, z=0.295–2.33). SHA256 in `manifests/desi_dr2_bao.json`; raw data in
`cache/` (gitignored). Fetch: `fetch/fetch_desi_dr2_bao.sh`. Tests: `tests/test_desi_w0wa.py`.

## Data result (solid)
- ΛCDM χ² = 10.35 ; w0waCDM best χ² = 5.63 (w0=-0.15, wa=-2.8, Om=0.39) ; **Δχ² = 4.73** (2 dof, BAO-only).
- Best fit is in the **(w0>-1, wa<0) thawing corner**; non-triviality confirmed: corner χ²≈7.75 vs opposite
  corners 13 / 44 / 613. So DESI DR2 BAO genuinely prefers **evolving DE in the thawing corner** (matches the
  DESI collaboration's headline; their 3.1σ uses BAO+CMB+SNe).

## D0 verdict — PARTIAL, and a CORRECTION to the corpus's passport claim
- **CONFIRMED (forced):** D0 forces **dynamical / evolving** dark energy (`w ≠ const −1`) via the convexity
  `Δ²R_n = φⁿ(φ−1)² > 0` of the relative-archive acceleration `R_n = φⁿ − 1`. DESI rejects ΛCDM in favour of
  evolving `w` (Δχ²≈4.7 BAO-only) — so the *evolving* content is confirmed.
- **NOT forced (over-read in BOOK_08 §565):** the corpus claims convexity ⇒ *the specific thawing corner*
  `(w0>-1, wa<0)` that DESI favours. **This does not hold.** I attempted the corpus's named-HYP phason→w(z)
  map: over **6 natural (source ∈ {R, R′, R″}) × (map direction N=±ln a)** choices, **0/6 land in the thawing
  corner** — all give `wa > 0` (the *opposite* sign) or phantom `w0<-1`. The corner (thawing vs phantom) is
  **map-dependent**, and the natural maps give the wrong `wa` sign. So the convexity forces "evolving", **not**
  "thawing corner".

## Honest status
DESI confirms D0's *evolving-DE* prediction (forced, real-data Δχ²≈4.7). D0 does **not** predict the specific
thawing corner — the corpus's "convexity ⇒ thawing (w0>-1,wa<0)" (BOOK_08 §565) is an **over-reading**: the
sign of `wa` depends on the unwritten n↔z map, and natural maps give `wa>0`. **Recommended corpus correction:**
downgrade the DESI passport from "predicts the thawing corner" to "predicts dynamical DE (w≠−1); the corner
sign is map-dependent and not forced." The numerical `w(z)` remains genuinely HYP (map-underdetermined) — now
demonstrated with an explicit 6-map enumeration + a concave control, not just asserted.
