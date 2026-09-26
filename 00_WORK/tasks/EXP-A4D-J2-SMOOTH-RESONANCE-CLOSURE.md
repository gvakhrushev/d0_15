# EXP-A4D-J2-SMOOTH-RESONANCE-CLOSURE

Class: `EXPENSIVE`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `exp/a4d-j2-smooth-resonance-closure`  
Primary artifact: `02_REGISTRY/research/MEMO_A4D_J2_SMOOTH_RESONANCE_CLOSURE.md`  
Execution: `GitHub-first`

## Why delegated

Merged PR #208 established the nonlinear metric provenance of the selected star action and the pure Einstein flat ray, but also found a correctly polarized L=4 diagonal quarter-wave connection resonance. The surviving H-J2-SMOOTH problem is genuinely nonlinear and requires Lyapunov-Schmidt reduction, exact finite spectral classification and asymptotic smooth-sampling analysis.

## Mandatory inputs

Read fully:
- `02_REGISTRY/research/MEMO_A4D_NONLINEAR_EINSTEIN_J2_BRIDGE.md`;
- `02_REGISTRY/research/certificates/a4d_nonlinear_einstein_j2_bridge_check.py`;
- `02_REGISTRY/research/MEMO_A4D_RESOLVED_AFFINE_PHYSICAL_QUOTIENT.md`;
- `02_REGISTRY/research/ATORUS_NORMAL_JET_EINSTEIN_BRIDGE.md`;
- `02_REGISTRY/research/ATORUS_TYPED_RESPONSE_RECONSTRUCTION.md`;
- `02_REGISTRY/research/ATORUS_LOVELOVK_LOCAL_UNIVERSALITY.md`.

## Objective

Resolve H-J2-SMOOTH after #208. Use only the corrected polarized (z\leftrightarrow z^{-1}) Fourier pairing.

## Required gates

Certified diagonal gates 1--4 are already reached in this PR and remain regression requirements:

1. Exact kernel/cokernel and regular complement at the L=4 diagonal quarter-wave.
2. Exact first nonzero Lyapunov-Schmidt reduced potential/Euler term.
3. Genuine symmetric-metric source projection and branch exponent.
4. Nondegenerate reduced root certificate and C^\infty quarter-wave J² invisibility.

Continuation gates now replace the old "repeat eight L=4 orbits" plan:

5. Certificate the self-dual/anti-self-dual chiral block split and an explicit uniform low-frequency gap separating the resonance variety from z=1.
6. Certificate the parameterized rank-22 family z=(w,w,i,i), its w-independent physical source channel, its SIM(2) null-line stabilizer, and the exact finite-amplitude identity S_star|pure resonant kernel=0.
7. Certificate the w=1 parabolic reduced-quartic cancellation; then compute V6^red or otherwise prove that u=0 is an isolated zero of the unsourced reduced Euler map.
8. On the generic rank-22 / d_incompat=2 stratum, derive parameterized V4,z and its projective critical discriminant/resultant instead of orbit-by-orbit Newton solving.
9. Prove a finite algebraic/subanalytic resonance stratification with a uniform positive Hölder/Łojasiewicz exponent. Pointwise finite Puiseux order is not enough.
10. Combine fixed (L-independent) smooth bump realization, IR invertibility and UV super-algebraic Fourier tails to prove every resonant correction is o(epsilon_N^2).
11. Prove asymptotic locality / extension independence: two global smooth realizations of the same local metric 2-jet must give the same reconstructed center response in the limit.
12. No arbitrary spectral filter/projection. Keep finite exact stationarity distinct from asymptotic J² equivalence; keep frame/grid erasure, Noether-divergence and cosmological bg channels separate.

Cross-wall observation only: PR #202 exhibits related parabolic/null-line affine-residual blindness. Treat "parabolic null-line seam" as a hypothesis until both sides have compatible exact stabilizer theorems; do not edit #202 from this task.

## Terminal outcomes

A. `J2-SMOOTH-PUISEUX-RESONANCE-CLOSURE`: small nonlinear resonant branches exist and all smooth-sampling resonant corrections are asymptotically invisible at J2 order.

B. `J2-SMOOTH-RESONANCE-NOGO`: some genuine metric source has no branch approaching flat.

C. `J2-SMOOTH-PARTIAL-CLOSURE`: the certified diagonal orbit closes but some resonance stratum / uniformity / locality gate remains unresolved or obstructed.

## Deliverables

Durable research memo, exact symbolic/rational low-order certificate, reproducible root/nondegeneracy certificate, smooth-tail estimate, theorem-ready statements, and terminal A/B/C.

No Lean/claims/BOOK/release promotion. Do not edit #202 or Palatini-span primary artifacts.

## GitHub execution contract

Start from fresh current `main`; lifecycle start; Draft PR before substantive edits; self-retire before Ready; never self-merge.

## Chat handoff

Return PR, tip SHA, terminal A/B/C, exact reduced branch statement, and only the first remaining blocker.
