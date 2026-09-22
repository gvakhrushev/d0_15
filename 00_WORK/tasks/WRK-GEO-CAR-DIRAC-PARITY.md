# WRK-GEO-CAR-DIRAC-PARITY

## Queue state
**PLANNED / PAUSED.** Do not execute during the current gravity closure sequence. CONTROL will explicitly promote this task later.

Repository: https://github.com/gvakhrushev/d0_15

When promoted, start from a fresh then-current `origin/main`; do not assume any local backup branch is present in a stateless worker environment.

## Class
WORKER

## Objective
Reimplement the explicit CAR Dirac operator, prove its self-adjointness, formalize a typed parity operator $\Gamma_F$ and the exact anticommutation $\{\Gamma_F, D_{CAR}\} = 0$ on current main.

## Scope
1. Reimplement CAR Dirac matrix on the typed 16-state finite Fock basis $\mathcal{H}_F$.
2. Prove self-adjointness $D_{CAR}^\dagger = D_{CAR}$.
3. Formalize the fermionic parity operator $\Gamma_F = (-1)^{N_F}$ and prove $\Gamma_F^2 = I_{16}$ and $\Gamma_F^\dagger = \Gamma_F$.
4. Prove exact anticommutation $\Gamma_F D_{CAR} + D_{CAR} \Gamma_F = 0$.
5. Derive $\pm \lambda$ spectral pairing consequence on the finite carrier without importing unstated infinite-dimensional spectral theorems.
6. **Boundary:** Scope is strictly bounded to the two selected claims. Do not expand to CAR square, zero-mode dimension, heat trace, or continuum convergence.

## Source Payload
- Current `origin/main` baseline `ArchiveCARDirac.lean`
- Local committed `backup/local-41d9550c`
- Uncommitted parity payload in `ArchiveCARDirac.lean` (preserved in tag `backup/dirty-archive-car-dirac`)

## Affected Claims
- `D0-ARCHIVE-CAR-DIRAC-OWNER-001`
- `D0-ARCHIVE-CAR-PARITY-SPECTRUM-001`

## Exit Condition
Current-main ArchiveCARDirac contains the explicit supported CAR Dirac operator, its self-adjointness theorem, a typed parity operator Γ_F and the exact anticommutation Γ_F D = −D Γ_F; any ± spectral-pairing consequence is added only if it follows on the actually typed finite carrier without importing an unstated spectral theorem.

## Lean build-cache policy

This worker must preserve the local Lean/Mathlib cache.

- Iterate with the narrowest target/module build.
- After the implementation stabilizes, run one incremental \`lake build D0.All\`.
- Run the normal guards/generated-view/no-sorry/axiom checks required by scope.
- **Do not run \`lake clean\`, delete \`.lake\`, or clear the Mathlib cache for routine evidence.**
- A cold rebuild is only for an explicit CONTROL/release request, a toolchain/dependency-manifest change, or confirmed cache corruption.
- Remote GitHub \`lean-build\` is the independent integration build.

If a long cold build was already started before reading this policy and no source change depends on its result, it may be cancelled rather than treated as mandatory evidence.

