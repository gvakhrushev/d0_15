# MEMO A4D — flat-jet vanishing of the quadratic residual completion (Lean owner)

**Task:** `WRK-A4D-FORMALIZE-STAR-EINSTEIN-SEED`
**Lean owner:** `D0.Geometry.A4DStarEinsteinSeed`
**Exact regression:** `02_REGISTRY/research/certificates/a4d_star_flat_jet_regression_check.py`
**Status:** Lean-owned finite algebra. No claim/BOOK/release promotion.
**Baseline:** merged #201 (`EXP-A4D: resolve affine physical quotient and Einstein detector`)

## 0. Purpose

This memo records the durable content of the Lean owner that closes the
**seed/completion split** of the A4D star programme. It exists so that the
structural fact below cannot be silently reinterpreted, weakened, or dropped in
later research cycles.

## 1. The structural fact

For the joint-residual lane write the two defects as

    X_i = I - P_i.

On the flat Lorentz background `P_i = I` both defects vanish. The two-stratum
residual is

    R_{2|1} = det(X_1) t_2 - X_2 adj(X_1) t_1.

The load-bearing content is not that `R` vanishes at the flat point — that is
immediate — but its **order** in the flat deviation:

| Quantity | Degree | Owner |
|---|---|---|
| `det(X)` | 4 | `star_residual_defect_det_eq_four_mul` |
| `adj(X)` | 3 | `star_residual_defect_adjugate_eq_three_mul` |
| `R` in `X`, fixed `t` | 4 | `star_residual_scaled_order` |
| `R` in `t` | 1 | `star_residual_translation_order` |
| `R` under `X = t = O(e)` | 5 | `star_residual_joint_flat_order` |
| `Q_H(R) = Rᵗ H R` | 2 in `R` | `star_quadratic_completion_smul` |
| `Q_H` under `X = t = O(e)` | 10 | `star_completion_joint_flat_order` |

Hence

    R = O(X^4 t),        Q_H(R) = O(X^8 t^2) = O(e^10).

## 2. The two-jet consequence

Because the owned completion is `O(e^10)` about the flat point `e = 0`, its
flat two-jet is identically zero:

    Q_H(0) = 0,     DQ_H|*_flat = 0,     D²Q_H|*_flat = 0.

The seed/completion identity is owned directly:

    `star_flat_second_jet_vanishes_of_completion_order`
      : j²_flat(S_star + Q) = j²_flat S_star

and its blocking corollary:

    `star_completion_cannot_cancel_seed_term`
      : no choice of completion coefficients can cancel a quadratic
        contamination already carried by the seed.

## 3. What this terminally forbids

It is now **impossible** to argue that fitting the completion coefficients
`(a, b, alpha_adj, ...)` can remove an `E_sp`-type term from the linear
operator, if that term is already present in `S_star`.

Reason: such a contamination is a property of the seed's own quadratic form at
flat order. The completion contributes nothing at flat two-jet order, so the
family `S_star + Q(R)` and the seed `S_star` have the **same** flat two-jet.
Fitting `(Q)` therefore moves nothing at the order where the contamination
lives. Any claim that coefficient selection cancelled it would have to
contradict an owned theorem.

This does **not** say the seed is contamination-free. Merged #201 separately
certifies `c_sp = 0`, `c_eta = 1/4 ≠ 0` for the naked star seed. The two facts
are complementary:

* #201: the seed carries the Einstein ray and no extra ray;
* this memo: the completion cannot alter that verdict either way.

Together they fix the flat linear operator of the family to the seed's.

## 4. Scope and non-claims

Deliberately **not** claimed here:

* no coefficient is selected for `Q`;
* no curved configuration is asserted stationary;
* no curved root is searched for;
* no identification of `E_eta` with the continuum Einstein tensor;
* no Newton coupling, cosmological constant, or matter source.

The module is finite linear algebra on one four-dimensional fibre. The
continuum bridge (`E-NJET`, `E-T4NAT`, `E-RAYSEL`) remains separate and is
owned elsewhere.

## 5. Regression

The Lean statements are homogeneity laws, so they could in principle be
vacuous. The exact SymPy regression checks them on explicit rational
invertible defects at the owned `L = 2` background and additionally:

* reads off the **exact** polynomial orders (residual 5, completion 10);
* verifies the flat value is zero;
* verifies all ten sub-orders of the completion vanish at `z = 0`;
* includes a negative control: the completion is **not** identically zero and
  the order is **exactly** 10, not higher.

Result: 24/24 PASS, exit 0.

```
python 02_REGISTRY/research/certificates/a4d_star_flat_jet_regression_check.py
```

## 6. Handoff

The seed/completion separation is now Lean-owned and cannot be reopened by
argument. Downstream work may assume `j²_flat(S_star + Q) = j²_flat S_star` and
must not re-derive coefficient selection for `Q` as a flat-linear-degree of
freedom.

The remaining open walls are unchanged and live elsewhere:

* `EXP-A4D-NONLINEAR-EINSTEIN-J2-BRIDGE` — the nonlinear metric-only J² bridge;
* `EXP-A4D-DISCRETE-PALATINI-TARGET-SPAN` — the top-down Palatini target span;
* `EXP-A4D-RESOLVED-CURVED-STATIONARY-CLOSURE` — the curved stationary sector.
