# D0_v16_DUSTY_PLASMA_TABLETOP_BRIDGE

**Status:** `LAB-BRIDGE / TABLETOP-PASSPORT-SEED`
**Claim class:** external physical analogue; not core proof; not isomorphism closure.
**Primary source:** Vasiliev & Vasilieva, *Aerosol and dusty plasmas control by the electron beam irradiation*, Journal of Applied Physics 139, 173301 (2026), DOI: 10.1063/5.0310772.

## 1. Mission

This bridge imports the electron-beam dusty-plasma laboratory system as a macroscopic analogue of D0 active/archive trace mechanics. The electron beam is treated as a directed readout/witness puncture; dust grains are treated as finite archive-capacity sinks; dust-free channels and fly-out regimes are treated as channel-clearing/ejection analogues.

The bridge does **not** prove D0 quantum gravity, black-hole jet identity, golden mass loss, or acoustic log-phi spacing. It supplies a falsifiable tabletop protocol for testing whether D0-style active/archive dynamics can organize real finite media.

## 2. Article facts admitted into the bridge

The following are admitted only as external laboratory facts:

1. Electron-beam plasma in gases containing dust was studied experimentally and by simulation in forevacuum pressure ranges.
2. Dust loading changes electron-beam propagation, power deposition, plasma shape, and plasma density.
3. The article distinguishes three aerosol plasma regimes: undisturbed, transition, and disturbed/fly-out modes.
4. In transition mode, zones free of grains appear near the electron-beam propagation axis.
5. In disturbed mode, grains are pushed out of the irradiated zone and move predominantly along the beam propagation direction.
6. Ordered dusty plasma structures can be attracted or repelled by the beam-plasma cloud depending on beam distance/core-periphery conditions.

These facts are sufficient to define a D0 bridge dictionary. They are not sufficient to close any D0 core theorem.

## 3. Structural dictionary

| Dusty plasma laboratory system | D0 bridge interpretation |
|---|---|
| Electron beam injection axis | directed readout / witness puncture |
| Pure electron-beam plasma cloud | active phase / unarchived plasma volume |
| Dust grains | archive-capacity sinks / trace carriers |
| Beam power absorbed by dust | active-to-archive transfer analogue |
| Reduced gas power deposition under dust loading | active depletion / trace extraction analogue |
| Plasma cloud contraction under dust loading | active-volume contraction analogue |
| Dust-free channel near beam axis | channel-clearing analogue |
| Disturbed fly-out mode | saturated ejection / jet-like discharge analogue |
| Ordered structure attraction/repulsion | seam sign-switch: periphery capture, core clearing |
| Ambipolar electric field vs ion drag | finite backreaction force-balance analogue |

## 4. Mapping discipline

The mapping is structural, not literal identity:

| Article equation/phenomenon | Bridge class | Forbidden promotion |
|---|---|---|
| `r^2(z)` beam contour relation | continuum shape shadow | not a phi-law |
| electron density balance equation | rate-equation shadow | not a literal log-det identity |
| electrostatic force and ion drag | force-balance shadow | not the positive operator `F_N` itself |
| dust fly-out along the beam axis | jet-like channel clearing | not a proved black-hole jet identity |
| radial potential profiles | pressure-gradient analogue | not an SI gravitational potential |

A successful bridge cert may verify the dictionary and the status discipline only. It may not promote external laboratory behavior to core closure.

## 5. D0 interpretation

The central lesson is that a detector medium is active. The observed channel is not a passive coordinate track; it is dynamically formed by the readout source and the trace medium. In D0 terms, retained activity and archive capacity co-define the observed geometry.

This bridge explains why fixed-alpha/fixed-ratio tests in detector-frame LIGO proxies can fail: an active measurement medium can deform the observable channel. The correct next layer is transfer-corrected geometry, not raw frequency-ratio claims.

## 6. External tabletop predictions

The following are D0 prediction targets, not article-proven facts:

### Prediction A: golden mass-loss candidate

Under pulsed electron-beam forcing of an ordered dusty structure, irreversible dust loss per stabilization cycle may approach a repeatable detector-normalized fraction. The D0 candidate fraction is

```text
phi^-2 ≈ 0.38196601125
```

Status: `EXTERNAL_EXPERIMENT_REQUIRED`.

### Prediction B: acoustic horizon hum candidate

After subtracting trap modes, gas damping, and RF forcing, low-frequency overtone envelopes of an isolated levitating dusty structure may show logarithmic spacing

```text
Delta log f = log(phi)
```

Status: `EXTERNAL_EXPERIMENT_REQUIRED`.

### Prediction C: transition surface

The boundary between passive absorption, channel clearing, and saturated ejection should form a reproducible surface in pressure-current-dust-density space:

```text
(P_m, I_b, n_d) -> {undisturbed, transition, disturbed}
```

Status: `EXTERNAL_EXPERIMENT_REQUIRED`.

## 7. Certificate discipline

Executable cert: `05_CERTS/vp_dusty_plasma_d0_mapping.py`.

Required pass tokens:

```text
PASS_STATUS_BRIDGE_NOT_CORE_CLOSED
PASS_ARTICLE_FACTS_DECLARED
PASS_MAPPING_ANALOGY_NOT_IDENTITY
PASS_D0_OPERATOR_DICTIONARY
PASS_PHI_CONSTANTS_ARE_PREDICTION_TARGETS_ONLY
PASS_DUSTY_PLASMA_TABLETOP_BRIDGE_CERT
```

Forbidden tokens/statuses:

```text
CORE-CLOSED
ISOMORPHISM-CLOSED
TABLETOP-QG-PROVED
DUSTY-PLASMA-ISOMORPHISM-CERT-CLOSED
```

## 8. Placement

- Book 06: active detector medium and trace formation.
- Book 07: horizon/channel-clearing laboratory bridge.
- Book 08: no promotion from laboratory analogue to cosmological proof without a typed bridge protocol and external negative controls.

## 9. Status recommendation

```text
D0_v16_DUSTY_PLASMA_TABLETOP_BRIDGE = ACTIVE-LAB-BRIDGE
D0_v16_DUSTY_PLASMA_TABLETOP_ISOMORPHISM = NOT-CLOSED
D0_v16_TABLETOP_QG_PROOF = FORBIDDEN-CLAIM
```
## 10. Proofread note

This bridge is intentionally written as a conservative laboratory analogue. Numerical constants such as `phi^-2` and `log(phi)` are admitted only as pre-registered experimental targets. The article-backed facts remain separated from D0 interpretation throughout the document.
