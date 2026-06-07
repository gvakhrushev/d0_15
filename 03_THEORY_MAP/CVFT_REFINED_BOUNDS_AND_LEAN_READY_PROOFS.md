# CVFT Refined Bounds and Lean-Ready Proofs

Status: theorem-ready proof cells only. No frontier row is promoted to core,
certificate-closed status or empirical pass.

## Refined Log-Det Rank Bound

Let `F >= 0`, `F <= P`, and `a = |z| rho(F) < 1`.  With the analytic logarithm
branch connected to `z = 0`,

```math
\left|-\log\det(I-zF)\right|
\le \operatorname{rank}(F)[-\log(1-a)]
\le \operatorname{rank}(F){a\over 1-a}.
```

The eigenvalue spelling

```math
-\log\det(I-zF)=\sum_j-\log(1-z\lambda_j)
```

is real-order preserving only when `z lambda_j < 1` is real.  Complex `z` uses
absolute values and the analytic branch.

Rejected shortcut: `rank(F) z/(1-z)` without `a = |z| rho(F)`.

## UV Feedback Tail Bound

For

```math
T_M(z,F)=\sum_{m>M}{z^m\over m}\operatorname{Tr}(F^m),
```

the preferred theorem target is

```math
|T_M(z,F)| \le {\operatorname{rank}(F)\over M+1}{a^{M+1}\over 1-a}.
```

Fallback:

```math
|T_M(z,F)| \le {\operatorname{rank}(P)\over M+1}{a^{M+1}\over 1-a}.
```

The finite condition `|T_M(z(L),F_N(L))| < delta0^12` is a readout tolerance
threshold, not the analytic convergence radius.

## Boundary-Channel Rank

Since `F=(QUP)^dagger(QUP)`,

```math
\operatorname{rank}(F)=\operatorname{rank}(QUP).
```

If `im(QUP) subset B_boundary(P,Q)`, then

```math
\operatorname{rank}(F)\le \dim B_boundary(P,Q).
```

Only identify this with `|partial(P,Q)|` when independent channel-counted cut
edges have been declared. This supports boundary localization of feedback
entropy and does not replace the terminal `A/4` capacity witness.

## Compressed Pole Discipline

`U_eff=PUP` is a contraction when `P` is an orthogonal projection and `U` is
unitary.  Eigenvalues lie in the closed unit disk.  If

```math
U_eff psi = lambda psi,  lambda = exp(-Gamma + iE),
```

then `E=arg(lambda)` and `Gamma=-log |lambda|`.  Bare positive `F` has real
nonnegative spectrum; complex poles require `U_eff`, a declared effective
non-Hermitian transfer, or Feshbach-Schur.

## Lean Targets Queued

- `D0.Dynamics.BoundaryLocalFeedbackRank`
- `D0.Gravity.UVFeedbackTailCut`
- `D0.Matter.CompressedPoleDiscipline`

Lean is deferred under `09_LEAN_FORMALIZATION/docs/LEAN_DEFERRED_RUN_POLICY.md`.
