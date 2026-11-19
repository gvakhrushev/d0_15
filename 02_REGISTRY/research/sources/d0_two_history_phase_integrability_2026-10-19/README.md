# Exact two-history phase/source interface

Input: `a95927fac939230a8e9d3e124c420fb2e3929a22`, same Draft #334.
Owner: [phase integrability and native-action gate](../../A4D_TWO_HISTORY_PHASE_HELMHOLTZ_AND_NATIVE_ACTION_GATE_2026_10_19.md).

From the repository root, with the repository's SymPy dependency installed:

```bash
python 02_REGISTRY/research/sources/d0_two_history_phase_integrability_2026-10-19/check_phase_integrability.py
```

The checker retains the complete exterior CAR16 representation, checks the
original proper-Lorentz generators and exact grade/parity preservation,
and derives both the moving-reference phase-source Jacobian and the
fixed-reference scalar Hessian. It verifies the nonzero three-direction
contact coefficient, arbitrary scalar-multiplier obstruction, exact finite
rectangle circulation, and the full h² moving-preparation example.
The latest two native detector rays are also checked explicitly: each has
contact coefficient 4/3, and every nonzero constant real combination of
their one-arm phase covectors has a strictly positive contact coefficient.
This does not alter their valid six-bilinear local inverse or their scalar,
gauge-independent Bargmann loop observable.

`RESULT.json` is a saved output; the script never rewrites expected evidence.
All calculations use exact SymPy expressions. The real archive-factor
identity is tested on a normalized real curve embedded in the 718-dimensional
space. This curve is an algebraic tensor-factor control, not a replay of the
actual Perron U_min dynamics. Its general implication follows from reality
and normalization, as proved in the owner. Existing archive and all40
certificates are not changed or replayed.

The new result tests whether a diagonal one-arm phase source can be inserted
into the existing single-action Schur argument. It does not invalidate the
bivariate scalar echo phase, a path-dependent action, or a full physical
stationary section with moving/complex preparation. The fixed-input
small-face limit can be integrable at leading order. The moving-preparation
control shows exactly why that limit cannot be used after freezing genuine
preparation derivatives.

Independent read-only analytical review checked the exact generators,
exterior16 lift, mixed-source signs, contact/circulation identities,
small-face estimates and physical scope. It does not constitute scientific
registry acceptance. Full apparatus admission, selected native price,
stationary full-history source, Einstein recovery and RAW-216 remain open.
