# D0 Claim Closure Contract

`bridge` is not a positive closure status.

## Conceptual Terminal Classes

A D0 question or proof-target is terminally classified when it belongs to one of four conceptual terminal classes:

1. **CORE** — internally derived within declared D0 scope without hidden external or bridge inputs. A Lean theorem or finite certificate is an ownership mechanism, but does not by itself make a claim CORE if it depends on unproved external hypotheses or undeclared bridges.
2. **NO-GO** — internally proved not derivable from the frozen core (boundary theorem).
3. **BRIDGE / PASSPORT** — the exact external mathematical or physical input is named, typed, and isolated with an explicit owner and failure scenario. A terminal BRIDGE or PASSPORT is a classified boundary, not a positive internal or core closure.
4. **EMPIRICAL TEST** — the internal observable is frozen and only comparison with experimental/observational data remains.

These conceptual terminal classes are NOT values of claims.csv.release_status. CP1 leaves the existing registry status vocabulary unchanged; status normalization is a later control-plane task.

## Global Stop Rule

Research on a lane stops when its load-bearing ambiguity is terminally classified.

The global closure target is:

> **zero unclassified load-bearing internal ambiguities, with every remaining interface explicitly CORE, NO-GO, BRIDGE/PASSPORT, or EMPIRICAL.**

Progress is measured by the reduction of independent unclassified blocking choices, not by raw theorem counts or issue counts.

## Forbidden

- `BRIDGE-CLOSED` without proved hypotheses.
- `CONDITIONAL-CLOSED` as a status upgrade.
- `external theorem applies` without proof that all external hypotheses hold for
  the D0 object.
- `sample cert passed` as proof of an infinite family.
- `negative controls passed` without a stated failure theorem or finite scope.

## Rule

A claim is closed only if it is a theorem, a complete finite cert, an external
theorem with all D0 hypotheses proved, an empirical passport within its declared
data scope, or a no-go/boundary theorem.

Any remaining bridge is a proof obligation.

## Existing Sector Guardrail: CVFT Operator Hardening (Outside Global DoD)

The following constraints represent an existing sector-specific guardrail for closed-vacuum feedback closure, outside the general Definition of Done. Relocation to a specialized domain document is deferred to a future control task.

Closed-vacuum feedback closure may use `F_N=P_NU_N^\dagger Q_NU_NP_N` only as
feedback-return and `R_N=D_N^\dagger D_N` only as positive response/readout.
Feedback pressure is `P_fb=beta^{-1}d_V log Z_N`; `P_N` is never pressure.

Allowed feedback claims require the positive identities, the correct resolvent
domain and the logarithmic determinant trace expansion. Forbidden shortcuts are:
`Q_N\ne0 -> F_N\ne0`, determinant trace without `-\log det`, complex
mass/width poles from bare positive `F_N`, root/window/H0/Omega_m/rd refits,
arbitrary-kernel SPARC/DESI repair and empirical promotion without a pinned
passport.

## Interface Stability and Verification

Previously proved theorems must be imported through stable interface modules whenever possible. Editing a low-level core module invalidates the downstream derivation and is permitted only when the primitive itself changes.

Closure is monotonic only at the interface boundary: once a theorem is frozen, downstream active modules depend on its statement, not on rewriting its proof body.

CP1 does not yet provide a machine-enforced claim impact graph; downstream invalidation requires explicit CONTROL review. Machine impact propagation belongs to future CP3.
