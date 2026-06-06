# D0 Claim Closure Contract

`bridge` is not a positive closure status.

## Forbidden

- `BRIDGE-CLOSED` without proved hypotheses.
- `CONDITIONAL-CLOSED` as a status upgrade.
- `external theorem applies` without proof that all external hypotheses hold for
  the D0 object.
- `sample cert passed` as proof of an infinite family.
- `negative controls passed` without a stated failure theorem or finite scope.

## Allowed Closure Statuses

- `LEAN-THEOREM-CLOSED`
- `FINITE-CERT-CLOSED`
- `INFINITE-FAMILY-PROVED`
- `EXTERNAL-THEOREM-APPLIED-HYPOTHESES-PROVED`
- `EMPIRICAL-PASSPORT-CLOSED`
- `NO-GO-CLOSED`
- `OPEN`

## Reduction Statuses

These are not closure statuses:

- `THEOREM-AVAILABLE / D0-HYPOTHESES-OPEN`
- `REDUCED-TO-HYPOTHESES`
- `PASSPORT-SAMPLE-EVIDENCE`
- `FINITE-PASSPORT-CERTIFIED / INFINITE-FAMILY-OPEN`

## Rule

A claim is closed only if it is a theorem, a complete finite cert, an external
theorem with all D0 hypotheses proved, an empirical passport within its declared
data scope, or a no-go/boundary theorem.

Any remaining bridge is a proof obligation.

## Development / release split

The full hard closure is a release gate, not the normal theorem-development loop.

Allowed development loop:

```text
edit active theorem module
→ build active module
→ build ActiveClosureIndex
→ run only touched certificates
```

Required release loop:

```text
build HardClosureTheoremIndex
→ run all hard certificates
→ check claim map coverage
→ check no forbidden sorry/axiom/Float in protected layers
→ rebuild release ledger
```

Previously proved theorems must be imported through stable interface modules whenever possible.  Editing a low-level core module invalidates the downstream DAG and is permitted only when the primitive itself changes.

Closure is monotonic only at the interface boundary: once a theorem is frozen, downstream active modules depend on its statement, not on rewriting its proof body.
