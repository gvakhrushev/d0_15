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

1. Exact kernel/cokernel and regular complement at the L=4 diagonal quarter-wave.
2. Exact first nonzero Lyapunov-Schmidt reduced potential/Euler term.
3. Genuine symmetric-metric source projection and branch exponent (A_{res}\sim q_{UV}^{\alpha}).
4. Nondegenerate reduced root certificate.
5. Classify remaining polarized L=4 singular characters/orbits far enough to decide whether the diagonal orbit is representative.
6. Quantify (C^\infty) T4 Fourier-tail decay at quarter-wave and whether induced resonant connection corrections are (o(\varepsilon_N^2)).
7. No arbitrary spectral filter/projection.
8. Keep finite exact stationarity distinct from asymptotic J2 equivalence; keep Noether-divergence and cosmological (bg) channels separate.

## Terminal outcomes

A. `J2-SMOOTH-PUISEUX-RESONANCE-CLOSURE`: small nonlinear resonant branches exist and all smooth-sampling resonant corrections are asymptotically invisible at J2 order.

B. `J2-SMOOTH-RESONANCE-NOGO`: some genuine metric source has no branch approaching flat.

C. `J2-SMOOTH-PARTIAL-CLOSURE`: diagonal orbit closes but another polarized singular orbit remains unresolved or obstructed.

## Deliverables

Durable research memo, exact symbolic/rational low-order certificate, reproducible root/nondegeneracy certificate, smooth-tail estimate, theorem-ready statements, and terminal A/B/C.

No Lean/claims/BOOK/release promotion. Do not edit #202 or Palatini-span primary artifacts.

## GitHub execution contract

Start from fresh current `main`; lifecycle start; Draft PR before substantive edits; self-retire before Ready; never self-merge.

## Chat handoff

Return PR, tip SHA, terminal A/B/C, exact reduced branch statement, and only the first remaining blocker.
