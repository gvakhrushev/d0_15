# Passport — PMNS neutrino mixing angles (seam-topology rule)

**Claim ids:** `D0-PMNS-SEAM-TOPOLOGY-001` (rule THE / numbers CHK), `D0-PMNS-DELTACP-PI0-001` (HYP),
`D0-XI5-CROSS-SECTOR-001` (COR). **Cert:** `05_CERTS/vp_pmns_seam_topology.py`.

## The rule

One closure-holonomy rule projected onto the three channels of the kernel `30 = 8⊕10⊕12`: the **degree of
δ₀** in an angle correction = the seam-cycle topology, `bare/open/closed → δ₀^{0,1,2}` (δ₀ = ½φ⁻³, forced).

## σ-table vs pinned data

| Observable | D0 formula | D0 value | data (source) | σ |
|---|---|---|---|---|
| sin²θ₁₃ | φ⁻⁵/4 (bare, δ₀⁰) | 0.02254 | 0.02195 ± 0.0007 (NuFIT-6.0) | 0.85 |
| sin²θ₂₃ | 1/2 + δ₀/2 (open, δ₀¹) | 0.55902 | 0.561 ± 0.020 (NuFIT-6.0) | 0.10 |
| sin²θ₁₂ | 1/3 − 2δ₀² (closed, δ₀²) | 0.30547 | 0.3092 ± 0.0087 (JUNO-2026) | 0.43 |
| δ_CP | ≈ π₀ ≈ π (HYP) | ~π | NuFIT-6.0 NO band | (prediction) |

All three angles land **< 1σ**. Data: NuFIT-6.0 (JHEP 12(2024)216, arXiv:2410.05380, normal ordering);
JUNO-2026 (first solar-sector reactor result, Nature 2026).

## Pre-registered windows
- `sin²θ₁₂ ∈ [0.300, 0.311]` — **passed** by JUNO-2026 (0.3092 ± 0.0087).
- `δ_CP ≈ π` (CP near-conservation) — a normal-ordering prediction to confront with future δ_CP precision.
- JUNO-2026 excluded tri-bimaximal / golden-A / golden-B at 2.8–4.2σ, while the δ₀-family held at 0.43σ.

## Discriminating test (in the cert, must FAIL)
Permuting the δ₀ degrees breaks the fits: `sin²θ₁₂` forced to degree-1 → **24.4σ** off JUNO; `sin²θ₂₃`
forced to degree-2 → **2.7σ** off NuFIT. Correct degrees: all three < 1σ.

## Honest bounds
- The degree↔topology **rule** is the THE content (directional structure machine-checked in
  `D0.Matter.PMNSSeamTopology`: θ₁₃>0, θ₂₃>1/2, θ₁₂<1/3); the **numeric values** are CHK (this passport).
- `δ_CP ≈ π₀` is **HYP** (a prediction), not derived.
- `θ₁₃` carries the shared seam `ξ₅ = φ⁻⁵` (depth-5 geometry common with α — `D0-XI5-CROSS-SECTOR-001`, COR).
- The cone-angle `2π₀` and the `δ₀=(6/5)` chain micro-derivations lean on corpus THE (`§04.6.π.4`) — a
  named **MECH-LIMIT** residual, not closed here.
