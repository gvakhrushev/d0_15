# D0 v15 Edge Alpha Ramification Full Construction (Researcher A)

## Status (hardened per executable evidence)

- EDGE-ALPHA-TRACE-CONSTRUCTION-TARGET
  (until S_seam is explicitly represented and trace is computed in cert)

- TORUS-RAMIFICATION-CONSTRUCTION-TARGET
  (until D_E(z,lambda), branch points and Puiseux indices are explicitly computed in cert)

External QED/lepton comparisons remain PASSPORT-LAYER.

## Edge-Sector Electromagnetic Normalization

On the 1-skeleton of K(9,11,13), the coefficient-origin trace reduces to edge-sector invariant.

Target (guardrail):

Tr(F_E) ~ ϕ^{-2} * 359 - ϕ^{-5} (with seam corrections S_seam)

The seam operator S_seam must be explicitly constructed as finite matrix on the 359-edge carrier for CERT-CLOSED.

## Lepton Ramification Indices

Charged-lepton hierarchy as branch indices of finite Green function over shell torus (Puiseux).

Target (guardrail):

p_μ = 1/4, p_τ = 1/3

Requires explicit construction of spectral cover D_E(z, λ), branch points, and indices.

## Guardrails

- PASS_EDGE_ALPHA_TRACE_TARGET_DECLARED (current, pending full construction)
- PASS_NO_ALPHA_NUMEROLOGY_CLAIM
- PASS_TORUS_RAMIFICATION_TARGET_DECLARED
- PASS_NO_LEPTON_FRACTION_FIT_CLAIM

No claim of reproducing PDG inside finite theory.

## Relation to Certs and Books

See vp_edge_alpha_trace_constructive.py and vp_edge_alpha_ramification_puiseux.py for executable status.

Book 04 lists as theorem targets (not closure).

Book 05 registers as TARGET classes (not CERT-CLOSED).

## Negative Controls

- Treating targets as closed without explicit seam/spectral construction is forbidden.
- Alpha or ramification numerology/fit claims are forbidden.

(Full construction details from Researcher A integrated here with status hardened to match current cert executability.)
