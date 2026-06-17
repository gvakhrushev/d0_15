# D0_DUSTY_PLASMA_EXPERIMENTAL_PROTOCOL

**Status:** `EXTERNAL-EXPERIMENT-PROTOCOL / NOT-RUN`
**Bridge:** `D0_DUSTY_PLASMA_TABLETOP_BRIDGE`.

## 1. Purpose

Define falsifiable tabletop tests for D0 active/archive trace mechanics using electron-beam dusty-plasma systems. The protocol is designed to avoid overclaim: it tests whether D0-inspired invariants appear after detector-frame normalization, not whether dusty plasma proves quantum gravity.

## 2. Test A: pulsed mass-loss fraction

### Observable

For an ordered levitating dusty structure under a sequence of identical electron-beam pulses, measure irreversible dust loss per stabilization cycle:

```text
L_k = Delta M_lost(k) / M_initial(k)
```

### D0 candidate

```text
L_k -> phi^-2 ≈ 0.381966
```

### Controls

- randomized pulse intervals,
- beam-off RF-only trap evolution,
- non-D0 fractions with the same fitting freedom,
- pressure and dust-density sweep.

### Admission rule

The D0 target is admitted only if the fraction is stable under repeated cycles and beats negative controls without retuning.

## 3. Test B: acoustic/log-frequency spacing

### Observable

Measure low-frequency vibration/acoustic spectra of an isolated dusty plasma structure after subtracting RF trap modes, gas damping, and apparatus resonances.

### D0 candidate

```text
Delta log f = log(phi)
```

### Controls

- empty RF trap spectrum,
- dust species swap,
- pressure sweep,
- randomized synthetic spectra with matched peak count.

### Admission rule

The log-phi spacing must appear as a frozen target against a full spacing sweep, not after selecting peaks manually.

## 4. Test C: phase transition surface

### Observable

Map the regime label

```text
(P_m, I_b, n_d) -> {undisturbed, transition, disturbed}
```

across pressure, beam current, and dust density.

### D0 target

A reproducible transition surface separating passive trace absorption, channel clearing, and saturated ejection.

### Controls

- dust-free gas,
- multiple dust materials,
- beam-current reversal/deflection controls,
- independent image-processing classifier for dust-free channels.

## 5. Reporting discipline

Allowed statuses:

```text
NOT-RUN
NEGATIVE-CONTROL
WEAK-CANDIDATE
EMPIRICAL-PASSPORT-CANDIDATE
```

Forbidden statuses:

```text
CORE-CLOSED
TABLETOP-QG-PROVED
ISOMORPHISM-CLOSED
```
## 6. Pre-registration requirement

Before any laboratory run is counted as a D0 passport candidate, the pulse sequence, dust material, pressure sweep, image-processing rule, spectral-subtraction rule, and negative-control suite must be frozen. No phi target may be selected after viewing the experimental spectra or mass-loss curves.
