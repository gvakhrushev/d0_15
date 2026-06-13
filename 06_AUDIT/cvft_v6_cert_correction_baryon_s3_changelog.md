# CVFT v6 Cert Correction and Baryon S3 Changelog

## A4 Errors Corrected

The flawed 3x3 rank example was replaced. The new minimal cert uses a 4D
full-rank crossing example with `rank(F)=rank(QUP)=2` and a Householder
boundary-channel example with `edge_count_like=3`, `dim(B_partial)=1` and
`rank(F)=1`.

## Refined Bound Examples Replaced

Log-det and UV-tail bounds use `a=|z|rho(F)<1`. The false
`-log(1-z)>z/(1-z)` negative control was removed; complex `z` invalidity and
`z=1.5,rho(F)=0.5` now test the forbidden shortcut.

## Baryon S3 Scaffold Cert Added

The baryon cert uses the lexicographic `(9,11,13)^3` basis, 27x27 permutation
matrices, representation/inverse-adjoint checks, the S3 symmetrizer, the
antisymmetric projector and deterministic block-rotation `U_eff^B` admissibility.

## Book Patches

Books 04 and 05 now state the carrier/symmetrizer-only status and the v6
forbidden shortcuts. Book 04 avoids treating the 10D symmetric carrier as a
physical decuplet status before spin/flavour labels and PDG passport.

## Maps Updated

F3 remains `OPERATOR-SCAFFOLD-COMPLETE`; F4 and F7 are `CERT-CANDIDATE`; no row
is `CORE`, `CERT-CLOSED` or `PDG-PASS`.

## Remaining Proof Obligations

Lean proofs for the refined bounds and boundary rank remain deferred. Physical
baryon resonance claims still require spin/flavour transfer, frozen pole set,
mass/width transfer, calibration and external passport.

## Next Recommended Frontier

Promote only the minimal refined-bounds certs into Lean-ready skeletons, starting
with boundary-channel rank.
