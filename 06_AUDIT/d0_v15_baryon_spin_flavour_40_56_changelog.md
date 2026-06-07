# D0 v15 baryon spin-flavour 40/56 changelog

## 1. Rank-40 sector added

Added the fully symmetric separable spin-flavour transfer sector:

```text
Pi_B^40 = Pi_S3^flavour tensor Pi_S3^spin
rank(Pi_B^40) = 10 * 4 = 40
```

This is a rank-40 decuplet-candidate transfer sector, not the full baryon resonance carrier.

## 2. Rank-56 carrier added

Added the full diagonal exchange-symmetric spin-flavour carrier:

```text
Pi_B^56 = 1/6 sum_sigma P_sigma^flavour tensor P_sigma^spin
rank(Pi_B^56) = dim Sym^3(C^6) = 56
```

## 3. Inclusion certified

The certificate proves:

```text
Pi_B^56 Pi_B^40 = Pi_B^40
Pi_B^40 Pi_B^56 = Pi_B^40
```

The remaining 16 dimensions are internal mixed spin-flavour states.

## 4. Book 04 patched

Book 04 now has `04.CVFT.F3b Baryon spin-flavour transfer layer` with the rank-40 and rank-56 carriers and internal pole laws:

```text
det(I - zeta U_eff^(B,40)) = 0
det(I - zeta U_eff^(B,56)) = 0
```

## 5. Book 05 closure class added

Added:

```text
SPIN-FLAVOUR-TRANSFER-CERTIFIED
```

Meaning: finite internal spin/flavour carrier exists and is certified before external passport.

Forbidden promotions:

```text
SPIN-FLAVOUR-TRANSFER-CERTIFIED -> PDG-PASS
SPIN-FLAVOUR-TRANSFER-CERTIFIED -> BARYON-MASS-CLOSED
```

## 6. Remaining passport boundary

No PDG names, no physical masses, no widths, no GeV conversion and no external data are assigned at this layer.  Remaining obligations are spin/flavour naming convention, frozen pole normalization, mass/width transfer and PDG passport.
