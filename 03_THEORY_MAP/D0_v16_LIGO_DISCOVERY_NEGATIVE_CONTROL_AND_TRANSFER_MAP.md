# D0_v16_LIGO_DISCOVERY_NEGATIVE_CONTROL_AND_TRANSFER_MAP

Status: `DISCOVERY-NEGATIVE-CONTROL / TRANSFER-MAP-TARGET`

## Scope

This document freezes the status of the GWOSC/LIGO discovery scans V3--V12 discussed during the D0 v15/v16 exploration.  It is a negative-control and transfer-map note, not an empirical passport and not a core theorem.

## Frozen discovery results

1. **Raw absolute φ frequency ladder rejected.**  The initial STFT/ratio scans found visually interesting GW170814 structures, but the ratio sweep placed φ poorly among generic ratios.  Therefore raw fixed frequency spacing is not a D0 invariant in this detector proxy.

2. **Detector-frame φ-beat did not survive nulls.**  The V6 detector-frame common-envelope subtraction test gave φ rank about 150 and an on-source φ score comparable to off-source background.

3. **GW170814 μ-plus φ^(5/4) was interesting but not significant.**  V7 found a local alignment near q=φ^(5/4), but V8 many-window off-source null gave empirical p≈0.53, so the single-event candidate is rejected as significant evidence.

4. **Ramified population ratios rejected in the proxy.**  MERS V9 paired tests over the six-event population gave negative mean deltas for μ-plus and τ-plus relative to base φ and high one-sided/permutation p-values.  These ramified ratios are not supported in the current proxy metric.

5. **Fixed α population law rejected.**  MERS V10/V11 population α-sweeps showed no stable fixed α invariant; base φ was not distinguished against a wider α-grid, and leave-one-event-out transfer was negative.  Hardened maps indicated score saturation / metric instability rather than a stable population law.

## Interpretation

The LIGO/GWOSC work is valuable because it falsified several attractive shortcuts.  It supports the conservative D0 lesson also seen in the dusty-plasma bridge: a detector medium can deform the observed channel.  Fixed φ or fixed α claims are invalid before a transfer-corrected, non-saturating residual observable is frozen.

## Admissible next target

The only admissible continuation is an event-normalized, non-saturating transfer observable:

- subtract or condition on the detector/source response;
- freeze off-source and cross-event nulls before looking at the target event;
- use residual ridge geometry, not raw frequency ratios;
- prevent q/α retuning after event inspection;
- report negative controls as first-class results.

## Forbidden promotions

The following are explicitly forbidden from V3--V12 results:

- `LIGO-PHI-PASS`;
- `GW170814-D0-CONFIRMED`;
- `RAMIFIED-PHI-GW-CLOSED`;
- `FIXED-ALPHA-POPULATION-LAW-CLOSED`;
- any Book 07/08 core promotion based on the proxy scans.
## Data-bundle note

V10 is represented by an uploaded data bundle in `08_PASSPORTS/GWOSC_LIGO/MERS_V10/`. V11/V12 are represented here as conversation-level plots and status conclusions only; they are not promoted to a full empirical passport bundle.
