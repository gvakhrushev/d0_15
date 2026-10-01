# All-frequency four-phase circle control and a general one-coordinate designated rescue

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input head: `297f81507b8f1d580db923da45e6baf4f5cd1a13`.
2026-10-01 v2 Targets D and U remain separately typed.
Action, metric source and Lorentz quotient are unchanged.

The [exact certificate](certificates/a4d_identity_fourphase_circle_check.py)
and [pinned ledger](certificates/a4d_identity_fourphase_circle_results.json)
prove continuous complex-line ranks by fraction-free determinants and
Q(i) polynomial gcds. This is not a torsion census. Together with the
owned one-coordinate inverse, it covers every frequency of the nonlinear
invariant four-phase/one-envelope sector. A second corollary constructs
the exact designated branch for every sufficiently small coframe depending
on one coordinate, with all ten metric components allowed.

## 1. Continuous ranks of the actual identity-sheet symbol

Write

\[
J_\mu(z)=\binom{A(\mu,z,\mu,\mu)^T}{C(\mu,z,\mu,\mu)},
\quad \mu\in\{1,-1,i,-i\}.
\]

The transpose is the literal connection Euler placement. C uses the
owned ten-slot Gram lift and the opposite mixed forcing/readout phases.
For fixed mu every entry has Laurent support in `{-1,0,1}`. The code
reconstructs those three coefficient matrices, clears every row by 2z,
and computes full 24-by-24 minors over Z[i][z] by Bareiss elimination.
Every division is checked exact in the Gaussian integers. There is no
determinant interpolation or modular lift.

Two charts suffice on each new line:

| Line | degrees of the two cleared minors | exact monic gcd in Q(i)[z] |
|---|---:|---|
| `mu=-1` | 28,28 | `z^20` |
| `mu=i` | 30,30 | `z^18*(z-i)^6` |

Their row sets and all Gaussian-integer polynomial coefficients are
pinned. Independent exact evaluation at `z=(3+4i)/5` checks the clearing
factor and the complete determinant values.

Consequently, for every nonzero complex z,

\[
\operatorname{rank}J_{-1}(z)=24,
\qquad
\operatorname{rank}J_i(z)=24\quad(z\ne i),
\qquad\operatorname{rank}J_i(i)=20.\tag{1}
\]

Coefficient conjugation gives the same statement for mu=-i, with its
only nonzero complex zero at z=-i. For mu=1 the owned two-sided
Laurent inverse of `A(1,z,1,1)^T` supplies full **connection-only** rank
on the physical unit circle and convolution norm at most 35/6.
That is all needed on the phase-common channel.

The gcd exponent six is a property of the two chosen minors, not a
claimed order-six principal loss. Exact range elimination at z=i
gives a reduced 14-by-4 z derivative of rank four. All four complex
center directions therefore open linearly on this particular circle.
The diagonal-quarter kernel vectors and reduced derivative are pinned.

## 2. Every frequency of the product-closed sector

Fields depend on `(n,p)=(x1,sum(x) mod 4)`. Their physical characters are

\[
\Sigma_L=\{(\mu,z,\mu,\mu):\mu^4=1,\ z^L=1\},\qquad L\in4\mathbb N.
\]

There are 4L characters. This subgroup is closed under products, hence
the field sector is closed under the literal nonlinear equation. It
allows arbitrary n dependence; no slow-frequency support is imposed.
The only frozen physical zeros are `(i,i,i,i)` and its conjugate.
The six rank-23 identity resonances from the other owner are outside
this sector, because their temporal character is 1 and their three
transverse characters are not equal.

On the quarter channels decompose u into the four role-center columns
N and the fixed twenty-column complement B:
`u=N a+B w`. On the other two channels every coordinate is normal.
The actual envelope difference has character multiplier `z/mu-1`;
it is the physical translation `e1-e0` minus identity.

The constant-coframe symbol, using phase-common connection rows and all
nonconstant-phase joint rows, has the period-independent estimate

\[
\boxed{\|w\|_p+\|D_1a\|_p\le C\|J_{\rm shift}u\|_p,
\qquad1\le p\le\infty.}\tag{2}
\]

This includes the unweighted owner sum. The complete four-role center is
retained; it is not reduced to two real envelope scalars.

Here is the all-order division argument. Near z=i the fixed twenty-row
range block is invertible. Its Schur remainder on N vanishes at z=i,
so exactly equals `(z-i)G(z)`. The new rank-four derivative says G has
a holomorphic left inverse near i. It recovers `(z-i)a`; the normal
coordinate recovery differs from the selected range output by another
factor divisible by z-i. Thus the target `(w,(z/i-1)a)` is a
holomorphic matrix times J, without a remaining small denominator.
Use the conjugate chart near -i. Elsewhere (1), the mu=-1 theorem and
the mu=1 connection inverse give smooth left inverses. A smooth
partition produces a global circle multiplier. Its Fourier coefficients
are absolutely summable, so periodization gives (2) in every l^p,
including the endpoint norms, with no L-dependent norm conversion.

For a sufficiently small compact family of constant coframes near I,
the same result persists uniformly. The generic-coframe owner gives
the four exact quarter role lines for every such S. The range and
first-derivative minors persist near the folds; the compact complement
gap persists by continuity. No additional frozen unit-circle zero can
appear in that neighborhood. No numeric coframe radius is asserted
for this joint statement.

## 3. Actual varying-background linear estimate, retaining intercell links

Let S(y1) be a fixed smooth coframe in that neighborhood and let
`K_h^sm` be the same smooth comparison sheet. Denote by F_h the full
connection rows and the thirty nonconstant-phase metric rows, in the
96L-variable sector above, and by H_h its derivative at the comparator.
This is a joint derivative; it is not the connection-only inverse of
general Target D.

Choose the smooth multiplier M_S from the preceding construction and
write its kernel as M_k(S). Smoothness in circle frequency, uniformly
over a compact coframe family, gives coefficientwise envelopes

\[
\sum_k\sup_S\|M_k(S)\|<\infty,\qquad
\sum_k|k|\sup_S\|M_k(S)\|<\infty.
\]

These are sums of suprema, sufficient for variable-coefficient l1.
Left quantization at S(hn) gives the exact commutator terms

\[
\sum_{k,j}M_k(S(hn))
\bigl[J_j(S(h(n+k)))-J_j(S(hn))\bigr]u(n+k+j).
\]

The mean-value bound costs `h|k| ||S'||`, controlled by the first kernel
moment. The literal derivative differs from the frozen-coefficient
one by O(h), from every actual neighboring area sample and the
O(h)-log comparison link. The target's center projection also varies
with S; its commutator with the actual envelope difference is O(h).
All these are finite-stencil or first-moment bounds in both endpoint
norms. Thus, with the actual transported center coordinates,

\[
\boxed{\|w\|_p+\|D_1a\|_p
\le C_g\bigl(\|H_hu\|_p+h\|u\|_p\bigr).}\tag{3}
\]

The constant depends on the fixed smooth coframe and comparator bounds,
and is independent of refinement. Formula (3) controls **all frequencies
of this sector on the actual varying comparator**, including boundary
links. The explicit h*center term is retained; it is not silently absorbed
to manufacture a false full inverse or response remainder.
On the chosen normal complement a=0, that term can be absorbed for
sufficiently small h, giving `||w||_p<=2 C_g ||H_h B_S w||_p`.
This is a uniform normal estimate for the rectangular joint operator;
it neither discards its unselected equations nor supplies a
connection-only projected root with the center held fixed.

## 4. General small one-coordinate metric: exact designated root

A separate Target-D corollary needs no quarter joint inverse. Let
`g(y1)=S(y1)^T eta S(y1)` with arbitrary smooth real 4-by-4 S satisfying

\[
\sup_y\|S(y)-I\|_{\rm op}\le1/10000.\tag{4}
\]

All ten metric components are allowed. Work in the phase-common
24L-variable translation-invariant sector, with no restriction on its
n frequencies. Set `A_sm=log K_h^sm` and `||A_sm||_infinity<=M_A h`.
Every actual sampled face weight is compared directly with the eta
weight, rather than resetting coefficients at a cell boundary.

The solder-area weight is bilinear in two columns. Its matrix nuclear
norm difference is at most `2*epsilon+epsilon^2`: expand the difference
as two simple wedges, and use the star/Lorentz sign matrices, which
preserve their Euclidean singular values. Each Euler Jacobian row or
column has at most six incident faces, four link positions and six
generator inputs, hence 144 contributions. The same log differential
count as the preceding warped rescue is bounded by 8192 in the
shrinking chart. Consequently

\[
\|DF_h(A_{\rm sm})-H_\eta\|_p
\le144(2\epsilon+\epsilon^2)+8192M_Ah.\tag{5}
\]

This holds for arbitrary variation of S between its sampled sites within
(4); a derivative of S is not needed for this gap bound. With the owned
`||H_eta^-1||_p<=35/6`, the certificate checks exactly that the first
term of its Neumann error is <1/4 and the second is <1/4 whenever
`M_Ah<=1/200000`. For sufficiently fine meshes,

\[
\boxed{\|DF_h(A_{\rm sm})^{-1}\|_p<12.}\tag{6}
\]

The #216 residual is super-algebraic. The uniform quadratic remainder
bound and contraction give a real exact root

\[
K_h^*=e^{A_{\rm sm}+u_h},\quad E_K(Q_h,K_h^*)=0,\qquad
\|u_h\|_p\le24\|E_K(Q_h,K_h^{\rm sm})\|_p.
\tag{7}
\]

Translation symmetry supplies every full-carrier link Euler equation,
including variations outside this invariant solution class. The L^3
lifting multiplicity cancels on the two sides. Hence

\[
h^{-2}\|E_Q(Q_h,K_h^*)-E_Q(Q_h,K_h^{\rm sm})\|_1=O(h^\infty),
\tag{8}
\]

and the owner reconstruction gives `-G[g]/2+O(h)`. The metric is fixed
as h tends to zero; epsilon is a fixed chart radius, not an h-dependent
forcing term. This extends exact designated existence from the diagonal
warp to every small smooth one-coordinate coframe. The earlier warp
theorem covers a substantially larger explicitly parameterized range.

## 5. Scope

The continuous circle theorem removes a genuine all-frequency gap in
the four-phase/one-envelope sector. The actual-background estimate (3)
is linear and retains its h*center error. It does not, by itself, prove
raw o(h^2) response for nonregular exact center fields. The separate
regular warped-quarter theorem uses the nonlinear quadratic gate and
exact center equations to prove its stronger scoped response statement.

The new general designated result (7)--(8) still concerns metrics
depending on one coordinate. It cannot be tiled into a general g whose
other coordinate dependence breaks the invariant sector. Full
four-dimensional Target D still requires an actual connection inverse
with exact center compatibility. Full Target U still requires a nonlinear
refinement-uniform remainder for nonregular extra branches. The finite
Y H_TORUS symbol remains a separate broader-microstructure problem.

No selector, source redefinition, uniqueness among all connections,
BOOK/CORE promotion or task-level Einstein terminal follows.
PR #310 remains `PARTIAL/OPEN`, Draft / `IN_PROGRESS`.

## Replay

```sh
python3 02_REGISTRY/research/certificates/a4d_identity_fourphase_circle_check.py --expect 02_REGISTRY/research/certificates/a4d_identity_fourphase_circle_results.json
```

The determinant, gcd and derivative gates are exact finite certificates.
The circle multiplier, intercell estimate and exact nonlinear rescue are
the analytic proofs above; no Lean formalization is claimed.
