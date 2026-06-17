# D0 baryon spin-flavour 40/56 transfer

## 1. Scope

This layer extends the certified baryon `S3` scaffold with an internal spin/flavour transfer carrier.  It uses no PDG data, no physical masses, no GeV conversion and no external datasets.

The correction is structural:

```text
rank-40 = fully symmetric flavour x fully symmetric spin sector
rank-56 = full diagonal S3-symmetric spin-flavour carrier
```

## 2. Certified 27D S3 scaffold

The existing scaffold is:

```text
V_B = V_shell^(tensor 3), dim V_B = 27
Pi_S3 = 1/6 sum_{sigma in S3} P_sigma
dim(Pi_S3 V_B) = 10
```

It is certified by `05_CERTS/vp_cvft_baryon_s3_scaffold.py`.

## 3. Spin dyad carrier

The spin carrier is the three-fold dyad carrier:

```text
D_2^(tensor 3), dim = 8
```

Its fully symmetric subspace has rank:

```text
dim Sym^3(C^2) = binom(2+3-1,3) = 4.
```

## 4. Flavour shell carrier

The flavour shell carrier is:

```text
V_shell^(tensor 3), dim = 27
```

Its fully symmetric subspace has rank:

```text
dim Sym^3(C^3) = binom(3+3-1,3) = 10.
```

## 5. Rank-40 separable symmetric sector

Define:

```text
Pi_B^40 = Pi_S3^flavour tensor Pi_S3^spin.
```

Then:

```text
rank(Pi_B^40) = 10 * 4 = 40.
```

This is the fully symmetric separable spin-flavour transfer sector, also called the rank-40 decuplet-candidate transfer sector.  It is not the full baryon resonance carrier.

The compressed pole operator is:

```text
U_eff^(B,40) = Pi_B^40 P U P Pi_B^40.
```

It is a contraction:

```text
|U_eff^(B,40)| <= 1.
```

The contraction is strict only on subspaces with nonzero feedback leakage.

## 6. Rank-56 diagonal symmetric spin-flavour carrier

The full diagonal exchange-symmetric spin-flavour projector is:

```text
Pi_B^56 = 1/6 sum_{sigma in S3} P_sigma^flavour tensor P_sigma^spin.
```

It acts on:

```text
(V_shell tensor D_2)^(tensor 3) ~= (C^6)^(tensor 3).
```

The rank is:

```text
rank(Pi_B^56) = dim Sym^3(C^6) = binom(6+3-1,3) = 56.
```

Inclusion:

```text
im(Pi_B^40) subset im(Pi_B^56)
Pi_B^56 Pi_B^40 = Pi_B^40
Pi_B^40 Pi_B^56 = Pi_B^40
```

The rank-56 carrier is the full internal exchange-symmetric spin-flavour carrier.  The rank-40 sector is the fully symmetric flavour x fully symmetric spin subcarrier.  The missing 16 dimensions form the mixed spin-flavour sector, which remains internal and anonymous until a later transfer/passport layer.

## 7. Internal pole laws

The internal pole laws are:

```text
det(I - zeta U_eff^(B,40)) = 0
det(I - zeta U_eff^(B,56)) = 0
```

with:

```text
U_eff^(B,k) = Pi_B^k P U P Pi_B^k, k in {40,56}.
```

## 8. Negative controls

Forbidden shortcuts:

```text
rank-40 as full baryon carrier
PDG sorting before spin-flavour transfer
complex poles from bare F
random non-Hermitian resonance operator
```

## 9. Book 04 patch

Book 04 must state that D0 has two internal baryon spin-flavour carriers before any PDG passport: rank-40 separable symmetric sector and rank-56 diagonal exchange-symmetric carrier.

## 10. Cert targets

Certificate:

```text
05_CERTS/vp_cvft_baryon_spin_flavour_40_56.py
```

Required PASS targets:

```text
PASS_FLAVOUR_S3_SYMMETRIC_RANK_10
PASS_SPIN_S3_SYMMETRIC_RANK_4
PASS_BARYON_SPIN_FLAVOUR_RANK_40
PASS_BARYON_DIAGONAL_SPIN_FLAVOUR_RANK_56
PASS_RANK40_SUBSECTOR_OF_RANK56
PASS_BARYON_SPIN_FLAVOUR_NO_PDG_ASSIGNMENT
```
