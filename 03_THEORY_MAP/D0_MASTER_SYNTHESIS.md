# D0 v15 master synthesis

## 1. Core thesis

D0 v15 is a finite-observability theory over condensed/profinite quasicrystalline support.  The active chain is

```text
finite support -> retained/traced split -> F_N=P_N U_N^dagger Q_N U_N P_N
-> resolvent thermodynamics -> matter / gravity / cosmology / time sector laws
```

Every physical phrase must pass through a finite object:

```text
standard object -> finite D0 operator -> theorem/sector law -> bridge/passport boundary
```

The central derived dynamical operator is the closed-vacuum feedback-return operator

```text
F_N = P_N U_N^dagger Q_N U_N P_N.
```

It is not the primitive support.  The primitive support is the finite/profinite D0 carrier with projection and tick structure.

## 2. Finite support and retained/traced split

At finite stage `N`, D0 uses a finite Hilbert/register carrier

```text
H_N = H_N^ret direct_sum H_N^tr,
P_N + Q_N = I,
P_N Q_N = 0.
```

`P_N` retains detector-visible degrees of freedom.  `Q_N` traces unresolved/archive degrees of freedom.  The finite tick is `U_N`.

## 3. Feedback-return / unitarity-defect operator

The unresolved return map is

```text
A_N = Q_N U_N P_N.
```

The positive feedback-return operator is

```text
F_N = A_N^dagger A_N
    = (Q_N U_N P_N)^dagger (Q_N U_N P_N)
    = P_N U_N^dagger Q_N U_N P_N.
```

For unitary `U_N`,

```text
F_N = P_N - (P_N U_N P_N)^dagger (P_N U_N P_N),
0 <= F_N <= P_N.
```

The positive readout/Born response is

```text
R_N = D_N^dagger D_N.
```

## 4. Resolvent and determinant thermodynamics

The feedback resolvent is

```text
G_N(z) = (I - z F_N)^(-1),
det(I - z F_N) != 0.
```

If `|z| rho(F_N) < 1`, then

```text
(I - z F_N)^(-1) = sum_{m>=0} z^m F_N^m
```

and

```text
-log det(I - z F_N)
= sum_{m>=1} z^m/m Tr(F_N^m).
```

With `a = |z| rho(F_N) < 1`,

```text
|-log det(I - z F_N)| <= rank(F_N)[-log(1-a)]
```

and

```text
|T_M(z,F_N)| <= rank(F_N)/(M+1) * a^(M+1)/(1-a).
```

## 5. Finite deformation and pressure law

Finite deformation is a finite difference or a derivative along a frozen finite matrix family `Delta_N(V), F_N(V)`.

```text
Z_N = Tr exp(-beta Delta_N(V)) det(I - z F_N(V))^(-1).
```

The feedback pressure is

```text
P_fb_mathsf = beta^(-1) partial_V log Z_N.
```

In book notation this is written as `mathsf P_fb`.  Plain `P_N` is always the retained projector, never pressure.

## 6. Matter sector law

A D0 matter candidate is a terminally projected near-critical feedback mode:

```text
F_N psi_j = r_j psi_j,
|z r_j| approx 1,
P_term psi_j = psi_j.
```

Physical naming requires an additional transfer layer: charge/spin/flavour labels, calibration, and an empirical passport when external comparison is claimed.

## 7. Baryon and meson resonance program

Resonance poles live in compressed nonunitary pole dynamics

```text
U_eff = P_N U_N P_N
```

or in Feshbach-Schur form

```text
H_eff(E)=H_PP+H_PQ(E-H_QQ)^(-1)H_QP.
```

If

```text
U_eff psi = lambda psi,
lambda = exp(-Gamma + i E),
```

then

```text
E = arg(lambda),
Gamma = -log |lambda|.
```

The certified baryon scaffold is finite:

```text
V_B = V_shell^(tensor 3), dim V_B = 27,
Pi_S3 = 1/6 sum_{sigma in S3} P_sigma,
dim Pi_S3 V_B = 10.
```

This is an operator scaffold, not a physical baryon spectrum.

## 8. Gravity and quantum-gravity regime

The gravity sector is finite spectral geometry plus feedback pressure and boundary capacity.  It uses heat trace, boundary energy and rank localization; it does not import continuum geometry as primitive.

```text
mathsf P_fb = beta^(-1) partial_V log Z_N,
mathsf P_cap = partial_V E_boundary.
```

Regimes:

```text
P_fb > P_cap -> expansion/acceleration
P_fb = P_cap -> stationary horizon/boundary
P_fb < P_cap -> contraction/capacity saturation
```

The UV/QG cut is the finite tail condition

```text
|T_M(z(L),F_N(L))| >= delta0^12.
```

When this holds, smooth gravity language stops and finite D0 algebra is the active theory.

## 9. Time and entropy channel

The D0 time arrow is the ordering induced by normalized coarse-grained feedback channels:

```text
hat Phi_N(rho) = Phi_N(rho) / Tr Phi_N(rho).
```

Entropy monotonicity is a theorem only for a normalized, coarse-grained, entropy-monotone channel.  The internal sync gauge is

```text
c_D0 = 1 tick gauge
```

not an SI-speed prediction.

## 10. Cosmology and S_DE transfer

`S_DE` is a two-mode feedback-pressure transfer.  The boundary derivative correction is

```text
F_N^(partial) = F_N^(2) + eta_N partial_V F_N,
eta_N = partial_V Tr(F_N^2) / partial_V Tr(F_N).
```

The exceptional-point diagnostic uses

```text
M(eta) = [[lambda_c, eta],[-eta, lambda_r]],
eta_EP = sqrt(10)/40.
```

This closes the internal transfer mechanism.  Survey comparison remains an empirical passport.

## 11. Coefficient-origin program

Coefficient claims must come from the resolvent trace program, residues, finite rank, and registered bridge/passport maps.  No coefficient is promoted from numerology or from detached curve fitting.

## 12. Horizon/greybody emission program

Horizon and greybody statements are finite boundary-capacity and leakage operators first.  External emission spectra require a frozen observable map and passport.

## 13. Gauge/confinement obstruction program

Gauge/confinement language is admitted only through finite commutator, boundary leakage, selector, and no-go operators.  A physical gauge-sector statement is a bridge/passport statement unless its finite operator law is explicitly closed.

## 14. Empirical passport layer

External comparison uses empirical passports.  IceCube, SPARC, DESI, CMB, CKM and PDG-facing comparisons must state data manifest, frozen operator, response map, negative controls, and pass/fail boundary.

The IceCube sync owner is:

```text
vp_neutrino_phason_decoherence_passport.py
```

## 15. Final claim boundary

D0 v15 closes the finite feedback operator core and several sector/operator scaffolds.  It does not automatically convert an operator scaffold into an external physical spectrum.  The final classes are:

```text
core theorem
sector theorem
operator scaffold
bridge law
empirical passport
no-go theorem
```

A claim is complete when it names one of these classes, a finite operator, and a falsification boundary.
