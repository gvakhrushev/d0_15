# WRK-GEO-CAR-DIRAC-PARITY

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
