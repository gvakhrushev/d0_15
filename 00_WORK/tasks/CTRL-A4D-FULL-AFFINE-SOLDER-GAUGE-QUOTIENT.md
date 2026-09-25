# CTRL-A4D-FULL-AFFINE-SOLDER-GAUGE-QUOTIENT

Class: `CONTROL`
State on registration: `IN_PROGRESS`
Parent: `ROOT`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `control/a4d-full-affine-solder-gauge-quotient`
Primary artifact: `02_REGISTRY/research/MEMO_A4D_FULL_AFFINE_SOLDER_GAUGE_QUOTIENT.md`
Execution: `GitHub-first`

## Purpose

Pressure the first blocker left by PR #175: determine whether the current raw
solder/coframe carrier admits a genuine finite affine node-gauge action that can
support a nonlinear gauge/constraint quotient for the accepted canonical
star-density.

The task must not assume that a raw solder leg is already an affine point.

## KILL-FIRST gates

1. TYPE: write the exact carrier and transformation types for node gauge
   `h_x=(g_x,c_x)`, raw coframe `e`, raw solder matrix `E`, and solder
   legs `v_r`.
2. REPRESENTATION: classify affine actions on the same raw carrier that extend
   the owned pure-linear right frame action.
3. FLAT LIMIT: require exact compatibility with
   `translationGauge` and `forwardGaugeCoframe`.
4. COMPOSITION: require a genuine group/groupoid action under node-gauge
   composition.
5. DENSITY: test the complete finite star-density under the surviving action.
6. QUOTIENT: only if the action survives, define the nonlinear Euler quotient
   and classify global `d_P`.
7. If the same-carrier action is impossible, identify the minimal typed carrier
   enlargement and stop there.

## Mandatory hostile controls

- constant nonzero node translation;
- nonconstant translation gauge on L=2 and L=3;
- pure local Lorentz frame;
- mixed Lorentz+translation composition;
- pure independent affine link shift must not be silently erased;
- raw Nyquist/curl/harmonic data remain distinguishable;
- no endpoint/reference section may be inserted without ownership.

## Scope

Research/control only. No Lean edits, no claims/release promotion, no BOOK/public
claim, no Einstein/time/continuum interpretation.

## Output

Primary memo and exact research certificate(s) under
`02_REGISTRY/research/certificates/` if useful. Update one research-ledger row
only after the verdict is stable.

## Exit condition

Either an exact finite same-carrier affine solder action is constructed and
used to define the nonlinear quotient, or a scoped theorem shows why the
current carrier cannot support it while preserving the owned translation chart,
with the minimal enlargement stated exactly.
