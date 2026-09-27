# WRK-A4D-ELIN-ESP-EXECUTABLE-OWNER

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-elin-esp-executable-owner`
Primary artifact: `02_REGISTRY/research/certificates/a4d_elin_esp_executable_owner_check.py`
Execution: `GitHub-first`

## Why delegated

Bounded exact reconstruction of the missing executable E_sp owner. The accepted E-LIN memo records a two-dimensional Lorentz constrained operator space, but the complementary coefficient/symbol owner was not preserved executably.

## Objective

Reconstruct the E-LIN degree-two response space from its own finite axioms, independently of #262.

Use only: Sym^2(Role), centered degree-two monomials, eta=diag(+---), signature-preserving signed-hypercubic equivariance, self-adjointness, metric gauge nullity under the owned symmetric centered gradient, and divergence freedom.

## Mandatory gates

1. Build the complete symmetry-allowed coefficient space; do not start from a guessed five-term ansatz.
2. Build exact rational constraint matrices for self-adjointness, gauge nullity and divergence.
3. Reproduce constrained dimension 2. Otherwise stop with the first mismatch.
4. Put the accepted Lorentz five-term E_eta ray (1,-1,1,1,-1) in the same coefficient representation and prove membership.
5. Choose a complementary ray by deterministic normalization independent of #262: primitive rational/integer vector plus lexicographic sign convention.
6. Prove the complementary E_sp is independent of E_eta and together they span the full constrained kernel.
7. Add a hostile control: dropping a required condition changes the space, or a coefficient perturbation violates one.
8. The certificate must not import/read #262 census/nullspace artifacts or normalize from any J2 orbit.

## Durable output

- primary executable certificate;
- `02_REGISTRY/research/A4D_ELIN_ESP_EXECUTABLE_OWNER.md` with exact coefficient convention and callable Fourier-symbol API.

Only after this owner is merged may #265 resume.

## Allowed terminals

- `ELIN-ESP-EXECUTABLE-OWNER-CERTIFIED`
- `ELIN-LORENTZ-CONSTRAINED-DIMENSION-MISMATCH`
- `ELIN-ESP-NOT-DETERMINED-BY-RECORDED-CONSTRAINTS`

Do not force the positive terminal.

## GitHub execution contract

Run `python tools/task_lifecycle.py start WRK-A4D-ELIN-ESP-EXECUTABLE-OWNER` as the first lifecycle change, open the Draft PR immediately, and work only there. Before Ready, run the certificate and repository guards, retire the task in the same PR, and set `Lifecycle: REVIEW`. Do not self-merge.

## Chat handoff

Report only the PR number, exact terminal/blocker, constrained dimension, and normalized E_sp owner if one exists.
