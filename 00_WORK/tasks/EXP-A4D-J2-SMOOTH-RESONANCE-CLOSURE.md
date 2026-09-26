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
10. Prove the shrinking-bump J² estimate inside the nonlinear solder quotient: for rho_h=h^alpha with 1/2<alpha<1, establish the actual response remainder O(h^(1-alpha))+O(h^(4alpha-2))+O(h^infty), with the coarse balanced choice alpha=3/5 giving O(h^(2/5)) if the stated analytic/Wiener bounds hold.
11. Prove uniform flat isolation + nonzero local degree on each connected compact resonance stratum; by analytic/subanalytic Łojasiewicz this gives one positive Hölder exponent per stratum. Equivalently exclude any nontrivial zero-source stationary germ accumulating at flat. A disconnected finite curved vacuum bounded away from flat is harmless for J².
12. Deduce stationary-sheet independence and two-bump locality: two shrinking bumps with the same quadratic 2-jet agree exactly on the radius-two leading stencil, and their response difference is only the vanishing analytic remainders plus O(h^infty) UV rescue. Arbitrary-global-sampling independence may remain downstream.
12. No arbitrary spectral filter/projection. Keep finite exact stationarity distinct from asymptotic J² equivalence; keep frame/grid erasure, Noether-divergence and cosmological bg channels separate.

Cross-wall observation only: PR #202 exhibits the same rank-two parabolic seam. On a fixed-rank-r stratum, Psi_r(M,t): omega↦t∧(Λ^r M)omega is a complete coordinate of the cokernel class: Psi_r(M,t)=Psi_r(M,t') iff t-t'∈im M. For a null rotation, [Λ^2(I-P)] determines the degenerate plane Pi and its radical null line ell=Pi∩Pi^perp; this is the top-nonzero-compound seam datum. Treat Psi_r as a rank-stratified quotient coordinate/resolution candidate, not a globally continuous action invariant or a new I-channel. Live #202 now has an exact enlarged parabolic curved family; for this task the only load-bearing cross-wall question is whether any nontrivial physical stationary germ from that family accumulates at the flat quotient.

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
