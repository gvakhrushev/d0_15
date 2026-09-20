# WRK-GRAV-COMPENSATOR-NOETHER

## Class
WORKER

## Objective
Reimplement the research-certified compensator construction as a generic Lean owner for the proved A1/Noether/Ward statements on current main under a strict semantic firewall.

## Scope
1. Reimplement row divergence, shift adjoints, variational compensator, and Euler/Noether identities from `A2CompensatorNoether.lean`.
2. Prove gauge invariance and the supported projected-field variational identity.
3. **Hard Firewall:** Do NOT reintroduce any statement claiming $A_1 \text{ Ward} = \text{Bianchi}$ or $B_+ = \text{signed Hodge divergence / Einstein tensor}$. $B_+$ is strictly the unsigned Weyl/Ward operator and is distinct from $B_-$, Hodge divergence, and Bianchi conservation.

## Source Payload
- Local `A2CompensatorNoether.lean` (888 lines)

## Affected Claims
- `D0-A2-COMPENSATOR-NOETHER-RESEARCH-001`
- `D0-SPECTRAL-EINSTEIN-001`
- `D0-HODGE-LINKS-001`

## Exit Condition
The research-certified compensator construction is reimplemented as a generic Lean owner for the proved A1/Noether/Ward statements, including gauge invariance, Euler/Noether identity and the supported projected-field result, while preserving the semantic firewall that B₊ is the unsigned Weyl/Ward operator and is not B₋, Hodge divergence, Bianchi conservation or an Einstein tensor.
