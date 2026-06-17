# D0 sector law closure

**Status:** sector-law closure of CVFT core.
**Rule:** finite object first -> transfer law -> passport boundary.
**Core operators:** `F_N = P_N U_N^dagger Q_N U_N P_N`, `U_eff = P_N U_N P_N`.

## Sector B1 - Matter law

Finite object:

```text
F_N psi = r psi
|z r| approx 1
P_term psi = psi
```

D0 defines matter internally as terminally stabilized feedback eigenmodes of the compressed finite dynamics.  Mass/inertia/stability are pole/feedback invariants after the matter transfer map is declared.  External comparison requires spin/flavour dressing, single-action-section transfer and PDG passport.

Proof target: `D0-CVFT-MATTER-001`.

## Sector B2 - Baryon resonance law

Finite object:

```text
V_B = V_shell^(tensor 3), dim V_B = 27
Pi_S3 = 1/6 sum_{sigma in S3} P_sigma
dim(Pi_S3 V_B) = 10
U_eff^B = Pi_S3 (P U P) Pi_S3
```

D0 defines the baryon resonance sector internally as the pole theory of the `S3`-symmetric compressed dynamics.  External comparison requires spin/flavour labels, mass/width convention and PDG passport.

Proof target: `D0-CVFT-BARYON-001`, with `det(I - zeta U_eff^B)=0`.

## Sector B3 - Lepton/alpha coefficient law

Finite object:

```text
F_E = P_E U_E^dagger Q_E U_E P_E
```

`P_E` projects onto the finite edge/U(1) sector of `K(9,11,13)`.  D0 defines lepton and electromagnetic coefficients internally as trace/residue invariants of the edge-sector feedback resolvent.  External comparison requires QED dressing and an alpha passport.

Proof target: `D0-CVFT-LEPTON-001`.

## Sector B4 - Gravity/QG law

Finite object:

```text
mathsf P_fb = beta^(-1) partial_V log Z_N
mathsf P_cap = partial_V E_boundary
F_N^(partial) = F_N^(2) + eta_N partial_V F_N
eta_N = partial_V Tr(F_N^2) / partial_V Tr(F_N)
```

D0 defines gravity internally as finite spectral geometry plus feedback pressure-capacity balance.  External comparison requires the Einstein macro-interface passport.

Proof target: `D0-CVFT-GRAV-001`.

## Sector B5 - Cosmology law

Finite object:

```text
F_N^(partial) = F_N^(2) + eta_N partial_V F_N
eta_N = partial_V Tr(F_N^2) / partial_V Tr(F_N)
```

D0 defines cosmological acceleration internally as feedback-pressure transfer under boundary capacity deformation.  The internal transfer mechanism is closed; survey comparison remains an empirical passport.

Proof target: `D0-CVFT-COSMO-001`.

## Sector B6 - Horizon / greybody law

Finite object:

```text
F_Q^emit(R) = Q_R U_R^dagger P_R U_R Q_R
```

D0 defines horizon emission internally as Q-to-P boundary leakage of capacity-saturated finite dynamics.  External comparison requires frequency dictionary, temperature weighting and greybody passport.

Proof target: `D0-CVFT-HORIZON-001`.

## Sector B7 - Gauge/confinement law

Finite object:

```text
|Q_N U_N P_N psi|^2 >= m_gap^2 |psi|^2
```

for all non-singlet color states.  D0 defines color confinement internally as terminal-pole obstruction caused by non-singlet leakage across the retained/traced boundary.  External comparison requires a QCD EFT bridge passport.

Proof target: `D0-CVFT-GAUGE-001`.

## Boundary

This document closes open frontiers as internal sector laws of the CVFT core only where the finite operator is declared.  It does not assign empirical fits, PDG names, physical masses or GeV widths.
