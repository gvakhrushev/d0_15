# D0 Cosmology Closure — Dependency Graph (Iteration 22)

The internal cosmology chain, with each link either a machine-owned CERT-CLOSED owner or a named
PROOF-TARGET with an exact missing artifact (`COSMOLOGY_CLOSURE_BLOCKERS.csv`). **Global closure is NOT
claimed**: the chain is machine-owned from reheating energy through the phason initial covariance, the
Fiedler freeze-out, and the dark/transfer composition; the `n_s` value (forced smoothing window) and the
physical `w_DE(z)` magnitude remain open and are named exactly.

```
frozen scene spectrum K(9,11,13) {0:1,20:12,22:10,24:8,33:2}, λ₂=20, λ_max=33   [frozen]
  └─ heat-trace time H(u), E(u)=−∂_u log H        D0-REHEATING-ENERGY-BUDGET-OWNER-001   [CERT-CLOSED, frozen]
       └─ A. phason initial covariance C_φ(u), ρ_φ∈[20,33]>0, normalized
              D0-REHEATING-PHASON-INITIAL-DATA-OWNER-001 / D0-PHASON-INITIAL-COVARIANCE-OWNER-001  [CERT-CLOSED ✓ new]
              gap: forced threshold window u_* (ρ_φ is a curve)                         [PROOF-TARGET]
       └─ B. two-mode pressure–energy window M(η), η_EP=√10/40, EOS p/ρ
              D0-PHASON-TWOMODE-PRESSURE-ENERGY-WINDOW-001                              [PROOF-TARGET: Lean owner not yet built (scratch-verified nonempty)]
              └─ continuum interpolation w_N→w_D0(u)                                    [PROOF-TARGET]
       └─ C. archive-capacity redshift a_D0(s), 1+z>0, monotone   D0-PHASON-ARCHIVE-CAPACITY-REDSHIFT-001  [CERT-CLOSED, frozen]
              └─ physical branch Σ_DE: w_DE<0 (sign via Galois σ(φ⁻¹)=−φ, owned)        [CERT-CLOSED sign]
                 gap: w_DE(z) MAGNITUDE map (D0-PHASON-WDE-Z-MAP-OWNER-001)             [PROOF-TARGET]
       └─ D. Fiedler freeze-out k_*²=λ₂=20   D0-CMB-FIEDLER-FREEZEOUT-OWNER-001          [CERT-CLOSED ✓ new]
              └─ IDS staircase + P(k)   D0-CMB-NS-LAPLACIAN-IDS-OWNER-001                [CERT-CLOSED, frozen]
                 gap: forced (k,u) smoothing rule (tilt differs at two (k,u) → n_s NOT fixed)
                      D0-CMB-IDS-SMOOTHING-OWNER-001 / D0-CMB-HEATKERNEL-SPECTRAL-TILT-OWNER-001 / D0-CMB-PHASON-SPECTRUM-OWNER-001  [PROOF-TARGET]
       └─ E. phason→curvature transfer T_R, P_R(k), n_s^D0
              D0-CMB-PHASON-TRANSFER-OWNER-001 / …-COVARIANCE-TO-POWER / …-NS-INTERNAL-EXPRESSION  [PROOF-TARGET: concrete T_R + forced (k,u)]
       └─ F. dark/transport: rank 3 / nullity 30, γ=10, visible 1/11, dark 10/11; EM-dark/metric-active; 5-stage composition
              D0-DARK-RATIO-TRANSFER-OWNER-001 / D0-ARCHIVE-PHASON-METRIC-TRANSFER-OWNER-001 / D0-COSMOLOGY-INTERNAL-TRANSFER-COMPOSITION-001  [CERT-CLOSED ✓ new]
       └─ G. passports (seven-field): CPL  D0-PHASON-WZ-CPL-PASSPORT-001                 [PASSPORT-CLOSED, frozen]
              CMB-spectral / dark-ratio passports                                       [PROOF-TARGET: external-data manifest missing]
              D0-COSMOLOGY-FROZEN-PASSPORTS-OWNER-001                                    [PROOF-TARGET]
  └─ umbrella  D0-COSMOLOGY-REHEATING-TO-CMB-CLOSURE-001                                 [PROOF-TARGET: n_s value + w_DE magnitude]
```

## This campaign closed (6 new CERT-CLOSED owners, real chain links A / D-Fiedler / F)
- `D0-REHEATING-PHASON-INITIAL-DATA-OWNER-001`, `D0-PHASON-INITIAL-COVARIANCE-OWNER-001` (Lean `D0.Cosmology.PhasonInitialCovariance`)
- `D0-CMB-FIEDLER-FREEZEOUT-OWNER-001` (Lean `D0.Cosmology.CMBFiedlerFreezeout`)
- `D0-DARK-RATIO-TRANSFER-OWNER-001`, `D0-ARCHIVE-PHASON-METRIC-TRANSFER-OWNER-001`, `D0-COSMOLOGY-INTERNAL-TRANSFER-COMPOSITION-001` (Lean `D0.Cosmology.DarkArchiveTransfer`)

## Remaining global blockers (exact, machine-listed in COSMOLOGY_CLOSURE_BLOCKERS.csv)
The two load-bearing gaps that keep the umbrella open: (1) a **canonical forced `(k,u)` smoothing rule**
(the spectrum alone does not determine `n_s` — tilt differs at two `(k,u)` points); (2) the physical
**`w_DE(z)` magnitude** map (the negative SIGN is owned via Galois; the magnitude is not). The two-mode
window (B) and the curvature transfer (E) are scratch-verified closable and named as PROOF-TARGET Lean
owners not yet built. No external survey datum may retune any internal window.
