# WRK-A4D-SOURCED-MISMATCH-FACTOR-PASSPORT

## Class

WORKER

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Objective

Lean-own the **algebraic factorization passport** isolated by research PR #128 / memo
`02_REGISTRY/research/MEMO_A4D_CLASSICAL_KINEMATIC_INTERFACE_PRESSURE.md` §6:

\\[
\\boxed{\\kappa(x,r)=L_{x,r}\\bigl(R_r(y)+h_r(y)\\bigr)}
\\]

under the sourced ansatz `δ = a + h`, with the memo's **source/predecessor index**
conventions and **pull order** made explicit in Lean names and comments.

This worker assembles already-landed owners; it does **not** re-prove them.

## Start inputs (import / reuse — do not duplicate)

- `A4DConditionalSourcedDiagonalTransport` (#125): `ρ = a − R`, seed `a`,
  relative defect `R`, parallel residual `h`, sourced solution `δ = a + h`
- `A4DRoleOverlapTwistedCocycle`: `transportedReferenceMismatch_diagonal_form`
- `A4DTransportedReferenceMismatch`: conditional `κ_q`
- `A4DActiveSpanExtensionIndependence` (#127): `conditionalMismatchFromSuppliedDelta`,
  `referenceFromSuppliedDiagonal` (supplied-δ assembly of κ)
- Research derivation only: memo §6.1 (and §5 pull-order remarks)

## Preferred module

`03_FORMALIZATION/D0/Geometry/A4DSourcedMismatchFactorPassport.lean`

## Index / pull-order conventions (mandatory in Lean)

- Predecessor site: `x`
- Source site: `y = x + r` (`roleTranslatePlus`), equivalently `x = predecessorSite r y`
- Pull order for predecessor data matches #125: bars are `L_{x,r}^{-1}`-pulled to the source fibre
- Path-source append/reverse laws remain the #125 owners (`S_{p++q}=S_p+P_p S_q`, etc.);
  this passport only cites them as ambient pull-order context

## Mandatory theorem package

1. Predecessor torsion identity: `τ_r = −L_{x,r} ρ_r` with
   `τ_r = b_{x,r} + L_{x,r} v_r(y) − v_r(x)`
2. Diagonal/supplied-δ expansion: `κ = τ + L δ` (reuse diagonal-form owner)
3. **Passport:** for sourced `δ = a + h`,
   `κ(x,r) = L_{x,r}(R_r(y) + h_r(y))`
4. Thin corollaries as needed (e.g. `κ = L(δ − ρ)`), without new selectors

## Firewalls (HARD)

- No new `J` selector / constructing `J`
- No finite E/F dressing, no `A=A(e)`, no stress/time/golden
- No claiming classicality / continuum / GR/QFT
- No `sorry`, no new axioms, no `lake clean`, **no self-merge**
- Do not re-duplicate #125/#126/#127 modules; import from main
- Keep scope SHORT: factorization passport only (not the full pressure memo,
  not transported-mean selector (6.2), not continuity / rank-jump)

## Exit condition

Lean owns `κ = L(R+h)` under `δ = a+h` with explicit source/predecessor indices
and pull-order comments; wired into `D0.All` / `formal_support.csv`; narrow +
`D0` build and `validate_repo.py` PASS; axioms ⊆ `{propext, Classical.choice, Quot.sound}`;
task self-retired; PR Ready; **do not merge**.
