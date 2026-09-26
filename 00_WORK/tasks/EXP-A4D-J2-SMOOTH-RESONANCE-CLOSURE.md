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

Merged PR #208 established the nonlinear metric provenance of the selected star action and the pure Einstein flat ray, but also found a correctly polarized L=4 diagonal quarter-wave connection resonance. The surviving H-J2-SMOOTH problem is genuinely nonlinear and requires Lyapunov-Schmidt reduction, exact finite spectral classification and asymptotic smooth-sampling analysis. This is not a bounded worker calculation.

## Mandatory inputs

Read fully:

- `02_REGISTRY/research/MEMO_A4D_NONLINEAR_EINSTEIN_J2_BRIDGE.md`;
- `02_REGISTRY/research/certificates/a4d_nonlinear_einstein_j2_bridge_check.py`;
- `02_REGISTRY/research/MEMO_A4D_RESOLVED_AFFINE_PHYSICAL_QUOTIENT.md`;
- `02_REGISTRY/research/ATORUS_NORMAL_JET_EINSTEIN_BRIDGE.md`;
- `02_REGISTRY/research/ATORUS_TYPED_RESPONSE_RECONSTRUCTION.md`;
- `02_REGISTRY/research/ATORUS_LOVELOVK_LOCAL_UNIVERSALITY.md`.

## Objective

Resolve the H-J2-SMOOTH gate after #208.

The corrected polarized diagonal character obeys
[
det H_{AA}^{pol}(t)=\frac{(t^2+1)^{12}}{16t^{12}},
]
so the first exact resonance occurs at L=4, t=i, with
[
\operatorname{rank}H_{AA}=16,
\qquad
\operatorname{rank}[H_{AA}^T\mid H_{Aq}]=20.
]

Do not stop at this linear incompatibility. Determine whether the full nonlinear connection Euler equation has a small resonant branch and whether that branch is asymptotically invisible for smooth continuum sampling.

## Required gates

1. Use the **polarized** (z\leftrightarrow z^{-1}) Fourier form only. The earlier unpolarized arbitrary-phase formula is withdrawn.
2. Perform Lyapunov-Schmidt reduction at the L=4 diagonal quarter-wave:
   - exact kernel/cokernel;
   - regular complement;
   - first nonzero reduced potential/Euler term;
   - source projection from genuine symmetric metric directions.
3. If the linear source is resolved nonlinearly, determine the branch exponent
   [
   A_{res}\sim q_{UV}^{\alpha}
   ]
   and certify a nondegenerate reduced root.
4. Classify the remaining polarized L=4 singular characters/orbits far enough to know whether the diagonal orbit is representative or only one unresolved case.
5. For smooth T4 sampling, prove or sharply obstruct the needed Fourier-tail statement. In particular quantify how a (C^\infty) quarter-wave coefficient scales with (L=N+2) and whether the induced resonant connection contribution vanishes faster than the (\varepsilon_N^2) Einstein response after reconstruction.
6. Keep exact finite stationarity separate from asymptotic J2 equivalence. No arbitrary spectral filter/projection may be inserted.
7. If the resonance closure succeeds, state the minimal hypotheses under which #201 + E-NJET yield
   [
   E_\star[g]=-\frac12G[g]
   ]
   for the naked-star normalization.
8. Keep finite-Noether-to-Levi-Civita divergence and the independent cosmological (bg) channel separate.

## KILL-FIRST outcomes

A. **Puiseux closure:** a small nonlinear branch exists, is selected without an arbitrary filter, and smooth-sampling resonant corrections are (o(\varepsilon_N^2)).

B. **Resonance no-go:** the reduced nonlinear equations have no branch approaching flat for a genuine metric source.

C. **Partial closure:** the diagonal orbit closes but another polarized singular orbit remains unresolved/obstructed. Name it exactly.

## Deliverables

- durable research memo;
- exact symbolic/rational low-order reduction where feasible;
- reproducible certificate for kernel/rank/reduced polynomial/root;
- explicit asymptotic smooth-sampling estimate;
- exact/conditional theorem-ready statements;
- terminal A/B/C with the first remaining blocker.

No Lean/claims/BOOK/release promotion. Do not edit #202 curved-stationary or Palatini-span primary artifacts.

## GitHub execution contract

Start from fresh current `main`; run lifecycle start; open Draft PR before substantive edits; keep the derivation and certificates in that PR; self-retire before Ready; never self-merge.

## Chat handoff

Return PR, tip SHA, terminal A/B/C, the exact reduced branch statement, and only the first remaining blocker.
