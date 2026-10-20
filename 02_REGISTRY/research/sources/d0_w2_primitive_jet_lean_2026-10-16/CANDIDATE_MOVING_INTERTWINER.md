# Moving-vertex ordered residual — candidate (DRAFT, pre-skeptic)

**Status:** DRAFT candidate; no registry row edited. Skeptic pass was not run. Pre-flight keywords `movingWordResidual`, `wordResidual`, `PrimitiveJetComposition`, `V_w I`: the skill script's `03_THEORY_MAP` / `09_LEAN_FORMALIZATION` / `05_CERTS` paths are absent in this checkout, and `formal_support.csv` / `claims.csv` / `D0/All.lean` have no `PrimitiveJetComposition` row.

## Claim (DEF-0.2.2 form)

For a finite word in a ring, with a supplied intertwiner at each vertex, the endpoint residual equals the ordered sum of one-step residuals `V_k I_{k+1} - I_k U_k`. The same identity in the jet ring keeps both adjacent vertex derivatives. Branch labels, preparations, tests, and carrier comparison stay explicit hypotheses. The constant family is the already stated fixed-intertwiner identity; that identity is not renamed.

## Owned pre-facts (verbatim)

Fixed identity, unchanged name, `03_FORMALIZATION/D0/Research/PrimitiveJetComposition.lean:228`:

```text
theorem wordResidual_eq_orderedSum (I : R) (w : List (Step R)) :
```

SOURCE `74e62cdc716e10883accba9d34ccf0e21d58eb65`, `02_REGISTRY/research/A4D_FOUNDATION_FORCING_NOT_CATALOGUE_SEARCH.md:99-103`:

```text
    V_w I-I U_w
      =sum_(j=1)^m V_(a_m)...V_(a_(j+1))
         [V_(a_j)I-I U_(a_j)] U_(a_(j-1))...U_(a_1).            (B)
Пустые произведения — identity. [...] Для разных промежуточных носителей используется тот же typed diagram с I у каждой вершины.
```

Same memo, lines 111-113:

```text
Для движущегося I(X) определим R_a(X)=V_a(X)I(X)-I(X)U_a(X). Тогда
    dR_a=(dV_a)I+V_a dI-dI U_a-I dU_a.                       (C)
```

Not this residual. `03_FORMALIZATION/D0/Foundation/EmpiricalTheoryFactorization.lean:149-151`:

```text
theorem empiricalProcess_composition (T : EmpiricalTheory) (P Q : OperationalProcess T) :
    empiricalProcess T (composeProcess T P Q) =
      empiricalProcess T Q ∘ empiricalProcess T P := by
```

Not this residual. `03_FORMALIZATION/D0/Geometry/A4DUnlabelledCenterHolonomyNoGo.lean:80-83`:

```text
theorem chainTransport_telescopes (C : Factorization corners Fiber Center) (u : corners) :
    ∀ rest : List corners,
      C.chainTransport (u :: rest) =
        (C.toCenter (rest.getLastD u)).trans (C.toCenter u).symm
```

Section 0.3 of `A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md` at the same SOURCE sha states conditional v8 maps. They are not instantiated here.

## The construction

Index `0` is the left vertex and index `w.length` is the right vertex. Letter `k` uses `I k.succ` on the right and `I (Fin.castSucc k)` on the left. Empty products are `1`. Head-of-list is the left factor.

`constantVertices_specialize_fixed` is definitional: every vertex equal to one `I0` reproduces `wordResidual` and `orderedResidualSum`.

`movingStepResidual_deriv` is

```text
dV * I_right + V * dI_right - (dI_left * U + I_left * dU).
```

The 2×2 control, checked in ordinary matrix arithmetic before Lean: word `e01` then `e10` on `V`, `e10` then `e00` on `U`; vertices `[[1,0],[0,2]]`, `[[0,0],[1,0]]`, `[[0,1],[0,0]]`. Moving residual `[[0,1],[-2,0]]`. Fixed residual at the output vertex `[[1,0],[-2,0]]`. One-step jet with left derivative `0` and right derivative `e01` has derivative `e10*e01 = [[0,0],[0,1]]`, while the single jet `⟨1, e01⟩` has derivative `[[-1,0],[0,1]]`.

## Verification

`~/.elan/bin/lake build D0.Research.PrimitiveJetComposition` in `03_FORMALIZATION`, this worktree's `.lake`, `LAKE_HOME` unset. `Build completed successfully (1475 jobs).` No `sorry`. No `sorryAx`. Axioms of the new theorems are among `propext`, `Classical.choice`, `Quot.sound`.

Negative controls that can fail the conclusion: reversed factor order (`reversed_order_fails`); frozen single `dI` (`frozen_dI_fails`); fixed residual versus moving vertices (`fixed_residual_misses_moving_intertwiner`); fixed one-jet derivative versus two vertex derivatives (`moving_vertex_dI_not_fixed_jet`); empty residual versus comparison, labels, and postselection (`moving_residual_does_not_force_comparison`).

## Named risks and pre-registered attack surface

1. Calling `jet_movingWordResidual_eq_orderedSum` a new derivative theorem when it is the ring identity on `Jet`. The separate statement is `movingStepResidual_deriv`, and `moving_vertex_dI_not_fixed_jet` separates it from `stepResidual_deriv`.
2. Reading `ComparisonHypothesis` as a proved comparison. Its fields are uninterpreted `Prop`s. They are not `D0.Foundation.AdmissibleComparisonGrammar`, and the empty-word residual does not produce them.
3. Treating formula (D)'s derivative bound as proved for unequal vertices. `movingWordResidual_norm_le` bounds the value. `jet_wordDeriv_norm_le` remains the one-parameter jet bound.
4. Importing a scene, phason, or v8 matrix as the primitive. No such specialization is in the file. Step maps stay parameters. The only specialization is the constant family back to the fixed residual.
5. A fourth program shape (tensor/parallel, or a relation quotient on words) is not covered. The theorem is one ordered word in one ring.

## What this does not show

No physical operator is selected. No v8 primitive is admitted. No `native_sector`, `positive_gr`, or GR closure. The module stays unwired in `D0.All`. Status stays candidate until a skeptic pass.
