# D0 v16 Theorem Dependency Graph

Status: FINAL-PUBLICATION-GUARDRAIL / DEPENDENCY-SPINE

This graph records what depends on what. It is intentionally conservative: external bridges and empirical scans do not support the finite mathematical core. They can motivate protocols and tests, but the core must remain standing if every external bridge is removed.

## Minimal finite-readout spine

```text
T0. Finite retained/archive split
    ↓
T1. Finite compression U_N and retained projector P_N
    ↓
T2. Feedback-return operator F_N = (Q_N U_N P_N)^†(Q_N U_N P_N)
    ↓
T3. Positivity / finite spectral discipline for F_N
    ↓
T4. Finite-volume derivative and log-det partition response
    ↓
T5. Active/archive trace mechanics and feedback pressure
    ↓
T6. Sector operators and guarded bridge protocols
```

## Core insulation rule

```text
The finite-readout core does not depend on:
- LIGO/GWOSC scans,
- dusty-plasma laboratory analogues,
- PDG resonance matching,
- cosmology survey fits,
- numerical visual resemblance.
```

If an external bridge fails, only the corresponding bridge/passport row changes status. The finite retained/archive algebra remains unaffected.

## Sector dependency map

| Sector | Depends on | Does not depend on | Publication boundary |
|---|---|---|---|
| Feedback-return algebra | T0--T3 | empirical data | finite positive operator and compressed dynamics only |
| Log-det pressure | T0--T5 and resolvent domain | cosmological survey success | positive first response, sign-corrected second response |
| Fractal tick / relative archive ratio | finite recurrence and phi tick convention | LIGO or dusty plasma | internal recurrence; external tests are separate |
| Edge alpha / ramification | finite edge space, companion block construction | QED RG fit | algebraic construction only |
| Baryon 40/56 | tensor symmetrizers, image-basis compression | PDG sorting | anonymous pole construction only |
| Horizon jet observable | axis/transverse projectors and finite emission operator | astrophysical jet data | observable scaffold, not empirical jet proof |
| Dusty plasma tabletop bridge | article facts + D0 dictionary | core closure | active-medium/channel-clearing analogue only |
| LIGO/GWOSC discovery track | GWOSC proxy notebooks | core theorem proof | negative controls and transfer-map target only |

## Corrected phi/log-det placement

The log-det response and relative archive-ratio acceleration are separate claims:

```text
L(V) = -d_tau log(1 - z + z exp(-kappa V))
L'(V) > 0 on the stated domain
L''(V) < 0 for 0 < z < 1
R_n = phi^n - 1 has positive relative acceleration
```

Publication text must not merge these into a single “accelerating log-det pressure” claim.

## External bridge firewall

External bridge rows may feed back into D0 only by creating:

```text
- prediction targets,
- negative controls,
- new finite operator hypotheses,
- experiment protocols.
```

They may not directly promote a physical analogy into a core theorem.
