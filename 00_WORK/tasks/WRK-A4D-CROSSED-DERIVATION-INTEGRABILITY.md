# WRK-A4D-CROSSED-DERIVATION-INTEGRABILITY

## Class

WORKER

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

SATISFIED on current `main` after merged PR #101 and PR #102.

Read completely:

- `02_REGISTRY/research/MEMO_A4D_CROSSED_CONSTITUTIVE_REPRESENTATION.md`;
- `03_FORMALIZATION/D0/Geometry/A4DScalarBackgroundWordMixing.lean`;
- `03_FORMALIZATION/D0/Geometry/A4DStaggeredFirstJetPathExpansion.lean`;
- `03_FORMALIZATION/D0/Geometry/ArchivePathWordAlgebra.lean`;
- the finite Role-phase shift/crossed-product owners used by those modules.

## Objective

Lean-own the exact obstruction to extending the owned scalar first-jet vertical law from the
pure-gauge sector to an arbitrary raw coframe while keeping the **compressed endpoint/group
relations** of the finite Role-phase torus.

This is a scoped descent/integrability theorem, not a universal no-go for all crossed actions.

## Primary law

On the degree-zero scalar quotient, formalize the multi-Role candidate derivative of a Role
shift in the form inherited from PR #101:

```text
delta_e(U_t)
  = -(1/L) * sum_r M_{e_t^r} D_r U_t
```

with the repository's literal normalization for `D_r`.

Do not silently change conventions; derive the exact Lean statement from the landed owners.

## Mandatory results

1. **Cycle relation.**
   From preservation of
   ```text
   U_t^L = I
   ```
   derive the exact zero-period condition on the coefficient field in the `t` direction.
   Prove it for the generic nondegenerate range supported by the literal operator identities.
   Treat `L=2` separately; do not overstate it.

2. **Commuting-shift relation.**
   From preservation of
   ```text
   U_s U_t = U_t U_s
   ```
   derive the discrete plaquette/closedness condition
   ```text
   (U_s - I)e_t^r = (U_t - I)e_s^r
   ```
   in the exact convention actually proved.

3. **Witnesses.**
   Give exact finite witnesses at small periods, preferably `L=3` and `L=5`:
   - one harmonic/nonzero-period field violating descent;
   - one curl field violating descent.

4. **Pure-gauge compatibility.**
   Show the owned exact field
   ```text
   e = d_f xi
   ```
   satisfies the cycle and plaquette constraints.

5. **Descent boundary.**
   Package a capstone saying:
   the owned scalar first-jet law cannot descend to the compressed finite endpoint crossed
   algebra on a raw coframe that violates these defining-relation constraints.

## Optional strengthening

If the required finite-torus cohomology lemmas are already nearby or short to prove, show that
zero periods plus the plaquette condition imply exactness in the relevant finite Role-phase
cochain class. Otherwise stop at the two necessary conditions and leave the converse to research.

## Truth firewall

Do **not** claim:

- no derivation of the finite crossed algebra exists;
- no full-background matter theory exists;
- every closed finite coframe is exact unless actually proved;
- the result covers `L=2` without a separate proof;
- a fiber-only affine representation is impossible;
- stress, Einstein, golden/phi, or physical time closure.

The target is only the landed scalar first-jet law plus the fixed compressed group relations.

## Suggested modules

Prefer one new narrow owner such as:

`D0/Geometry/A4DCrossedDerivationIntegrability.lean`

and reuse PR #102 owners instead of duplicating their calculations.

## Validation

Run narrow builds first, then exactly one final D0 task build and the normal repository guards.
No `sorry`, no new axiom.

## GitHub-first flow

1. fresh branch from current `main`;
2. `python tools/task_lifecycle.py start WRK-A4D-CROSSED-DERIVATION-INTEGRABILITY`;
3. open Draft PR immediately before source edits;
4. implement and validate;
5. before Ready self-retire the task;
6. set `Lifecycle: REVIEW`;
7. Ready for review;
8. do not self-merge.

## Exit condition

The defining finite-torus relations are Lean-proved to impose the exact cycle-period and
plaquette integrability constraints on the PR #101/#102 scalar vertical first jet, with explicit
small-period hostile witnesses and pure-gauge compatibility.
