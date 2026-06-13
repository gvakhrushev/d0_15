## Finite cochain complex and Hodge Laplacian

The finite graded incidence complex is the common algebraic carrier for
cochain-level defect, response and heat-trace constructions. The D0 core uses
finite boundary maps and finite Hodge Laplacians, not continuum curvature
tensors, as its master topological object.

Closed-vacuum feedback adds the paired operator `(Delta_N, F_N)`: the Hodge Laplacian supplies the geometry spectrum, and the feedback determinant supplies unresolved return cycles. `F_N=P_N U_N^dagger Q_N U_N P_N` is the feedback-return operator; `R_N=D_N^dagger D_N` remains the positive response/readout operator. Owners: `D0.Cosmology.FeedbackPartitionFunction`, `feedback_determinant_return_cycles`, `feedback_variation_universal_source`.

The admissible finite identities are:

```math
F_N=(Q_NU_NP_N)^\dagger(Q_NU_NP_N)
=P_N-(P_NU_NP_N)^\dagger(P_NU_NP_N),
\qquad F_N\ge0,
\qquad F_N=0\Longleftrightarrow Q_NU_NP_N=0.
```

The complement being nonzero does not force feedback: `Q_N\ne0` alone does not imply `F_N\ne0`.

The resolvent `(I-zF_N)^{-1}` exists when `z^{-1}` is outside the finite spectrum of `F_N`. Neumann and loop expansions require the stricter radius condition `|z|\rho(F_N)<1`, and the determinant trace formula is logarithmic:

```math
-\log\det(I-zF_N)=\sum_{m\ge1}{z^m\over m}\operatorname{Tr}(F_N^m).
```

For a finite deformation parameter `V`, `d_V` means either a declared finite-difference operator on a finite matrix family or an ordinary derivative of a smooth finite-dimensional matrix family.

