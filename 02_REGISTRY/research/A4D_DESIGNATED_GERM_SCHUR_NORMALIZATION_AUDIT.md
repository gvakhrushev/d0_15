# Designated Y germ: Schur normalization and finite-tower scope audit

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE` / Draft PR #310.
Status: exact cross-check of two owned finite/linear inputs; neither task-level
terminal is reached. This audits the two supplied September 29 tower and
designated-germ syntheses without adopting their unproved finite-elevator
or all-order Einstein identities.

## 1. Direct bridge on the *same* normal Hessian

The #310 normal-jet JSON records, in ten symmetric Gram-coordinate slots,
the Hessian `J_{ab,cd}` of the normalized surviving curvature
`-Y tensor Y`. The response after phase erasure is

```text
r = (3/2, 0, 0, 0, -1/2, -1, -1, -1/2, -1, -1/2).
```

The merged #273 checker independently builds the standard flat linearized
Einstein symbol `K_G(k)` from its index formula, including raised output
indices and factor two in off-diagonal Euler coordinates, and proves the
100-entry polynomial identity `K_Schur(k)=-K_G(k)/2`. Contracting **both
owned polynomial maps** against the same pinned `J` gives

```text
K_G[J]     = (3, 0, 0, 0, -1, -2, -2, -1, -2, -1),
K_Schur[J] = (-3/2, 0, 0, 0, 1/2, 1, 1, 1/2, 1, 1/2),
r          = K_G[J]/2 = -K_Schur[J].
```

The supplied `E_Q=G=-2*K_Schur` assertion is therefore off by a factor of
two **when `G` means the standard linearized Einstein tensor on this pinned
normal Hessian**. The naked-star metric Euler response convention also needs
to be distinguished from an arbitrarily renormalized tensor named `G`.
This calculation validates one input and the flat linear Schur symbol; it
does not identify the nonlinear finite-`L` joint metric operator on an open
class of metrics. Reproduce and test the hostile unit-normalization claim:

```bash
python3 02_REGISTRY/research/certificates/a4d_designated_germ_schur_normalization_check.py
```

The checker consumes the #310 pinned normal Hessian and response and executes
the #273 direct symbol checker. Its JSON pins the complete ten-vectors and
the exact mismatch. It does not silently import `E_eta=-2G` as an input.

## 2. The proposed finite tower does not inherit the quadratic obstruction

The positive numbers `351402359/2108160` and
`21506403637/154949760` are second-order **local zero-momentum
connection-cokernel coefficients** for the specified `z=1` normal germ.
The periodic mean equation uses a fixed background and an integer-power,
uniformly bounded regular branch through `h^4`, with global product framing.
The replay checks those inputs and periodic shift sums; it does not assemble
and prove the exact full finite-`N` identity

```text
O_N(a_N) = c * mean_N(kappa_N^2)
```

for every nonlinear stationary section and every finite period. Analytic
quadratic coefficients alone do not imply such an exact identity: even the
scalar analytic function `c*t^2*(1-t)` has positive quadratic coefficient
and another zero at `t=1`. Higher center/range terms are precisely what the
regular expansion and its unproved uniform extension must control.

The proposed factors `4/9, 1/2, 3/5, 2/3, 35/48, 11/14` and an operator
intertwiner `O_{N+1}(P_N a)=q_N O_N(a)` are not pinned D0 Euler
certificates. Zero padding a scalar field gives the elementary mean-square
factor `q_N=|E_N|/|E_{N+1}|`, but it does not show that the finite plaquette
action, stationarity and its nonlinear cokernel commute with padding;
faces crossing the block boundary have to be checked. M1's conceptual
requirements do not by themselves assert this particular operator identity.
Even granting the stated naturality, it would not establish the missing
exact finite-level quadratic identity. Replacing the `h`-limit by a tower
also changes the objective of the existing task rather than proving its
normalized response convergence.

Consequently `A4D-Y-TOWER-M1-NOGO` and a joint-Euler uniqueness selector
are not consequences of these owners. The exact phase-common `h^4`
normal-jet defect does not classify all source conventions, centers, and
non-Y corrections, and it is subleading in the task's `h^-2` response norm.

## 3. Smooth-branch owner boundary and next proof obligation

Merged #216 gives a conditional local Einstein theorem. Its primary memo
explicitly leaves `H-NORMAL-RESCUE` open: uniform existence and response
control for the **full coupled** connection Euler correspondence on a
fixed smooth curved realization. Merged #275 builds an exact slow Y lift
on the valued affine solder, with a separate genuinely varying metric that
is macroscopically flat. Neither owns an all-order finite-`L` smooth
stationary branch on the nonflat product germ, and the independent
E-NJET theorem is an estimator for its chosen centered stencil rather
than an identity for the physical finite joint Euler map.

An exact finite-level equation
`E_Q(Q,K_sm)=G_disc(Q)` first needs a defined `G_disc` in the same
source/normalization convention, an exact curved-background solution of
`E_K(Q,K_sm)=0` or a proved uniform rescue, and an all-row comparison.
An asymptotic statement instead requires the corresponding source/topology
and a remainder with its actual order. The owned #216 target is conditional
`E_star,h[g]=-(1/2)G[g]+O(h)+O(h^infinity)` in its convention; it does not
provide an `O(h^5)` raw remainder for the full finite Euler map. The first
missing mathematical step therefore remains the coupled normal rescue or
an exact counterexample, with the already proved Y and Schur scopes kept
separate.
