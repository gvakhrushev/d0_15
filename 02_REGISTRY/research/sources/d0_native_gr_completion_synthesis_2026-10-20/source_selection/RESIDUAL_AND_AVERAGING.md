# Full residual and source preserving averaging

Baseline `4867b6d4`, existing research owner #334. The parent is equation (9)
of `A4D_CAUSAL_BOOK_SOURCE_TO_EXACT_GR_SYNTHESIS_2026_10_20.md`.
The purpose is to type the proposed comparison with relative entropy,
Jones coordinates and a Golden history average before assigning a value.

## The full residual is explicit but its valuation must be specified

For the parent's declared mean-history price representation,

    G = sum_w (C_w-I_w) K_w* K_w = s_c I + delta E_mark + R,
    S = Tr(rho G)+W,         Tr rho=1,

`R` is a Hermitian operator on the input space. The scalar residual is
`Tr(rho R)+W`, and its first source includes both `Tr(rho dR)` and
`Tr((d rho)R)`. A scalar entropy or cocycle cannot literally equal the
operator R without an identification or contraction. An operator identity
`R=c I` would be stronger than equality on a single preparation.

The exact formula determines how all specified prices contribute. It does
not numerically specify an as yet unspecified physical `I_w`, information
algebra, or remaining work price. For a genuinely nonlinear information
functional, its differential must be included without assuming this
linear-in-rho representation. The owned minimal Golden execution computes
two particular complete terminal valuations; neither is automatically the
mandatory full prospective Book valuation.

## Splitting does not change the physical source

For any differentiable scalars a,b, the pointwise replacements

    s_c' = s_c+a,    delta' = delta+b,
    R' = R-a I-b E_mark

leave G, S and dS exactly unchanged. In particular

    dR' = dR-da I-db E_mark-b dE_mark.

All these terms are necessary in equation (9). This is a freedom of
description of one operator, not authorization to change a native
physical valuation. If the construction fixes a particular split,
that split remains the one to test. The result explains why a test
on R alone must specify the split and cannot replace the full source.

## Averaging has two independent obligations

Let M be a fixed linear idempotent conditional expectation on a finite
record space. Then

    M r=c  has a solution iff M c=c,
    {r : M r=c} = c + ker M.

Proof: applying M gives the necessary condition; if it holds,
`M(r-c)=0` is equivalent to the equation. Thus a nontrivial averaging
kernel leaves freedom unless the admissible physical class eliminates
it. Invariance `Mr=r` instead places r in `range M`; it does not in
general make that range one-dimensional. This statement does not assume
that an arbitrary vector in the kernel is a physically admitted price.

If both the law and residual depend on fields y, the actual first source is

    d sum_w pi_w(y) r_w(y)
      = sum_w pi_w dr_w + sum_w r_w d pi_w
      = E[dr] + Cov(r,d log pi).

The covariance notation assumes positive normalized weights. Omitting the
second term changes the source. For the exact control `r=(1,-1)` and
`pi=(1/2+y,1/2-y)`, the residual mean is zero at y=0 while its derivative
is 2. This is a counterexample to inferring a source identity from a
single scalar average, even with constant leaf prices.

Conversely, a proved full identity `M_y r_y=c_y` on an open field chart
does give equality of its derivatives when **both** terms are retained.
There is no general obstruction to that stronger identity.

## Three different uses of phi

1. Golden code units fix `-log_phi P = -ln P/ln phi` for a physically
   admitted event. The latest matched-void owner already proves exactly
   this conditional normalization; it does not prove event admission.
2. The metric uniqueness theorem uses a physically interpreted dilation
   `g -> phi^2 g` and additional locality, naturality and source hypotheses.
   It is not an assertion about arbitrary record partitions.
3. Golden rotation and Beatty sequences are arithmetic objects. Their
   identification with the actual recorded history requires a map and
   preservation of the field-dependent law and full source.

The exact `history/BEATTY_BOUNDARY.md` checks the current prospective law:
for equal unit edge costs `K=c A`, the common c cancels in both finite
horizon and Perron–Doob conditional probabilities. The full stochastic
history has positive entropy rate; it is not a stationary finite-alphabet
factor of an irrational rotation. Additional clocks, coarse factors and
random couplings are not excluded by that statement.

The Hurwitz extremality of phi is asymptotic rational approximation,
not finite-N optimal discrepancy among all irrational rotations. For
`{n alpha}, n=1,...,N`, already at N=1 the star discrepancy is
`max(alpha,1-alpha)`. The irrational `alpha=1/2+sqrt(2)/100` has lower
discrepancy than `alpha=1/phi`. The asymptotic extremal approximation
class also includes unimodular transforms of phi.

Consequently the proposed Beatty average is not yet a finite substitution
with all arguments supplied. It requires the actual history-to-clock map,
conditional weights, fixed residual valuation and source transport. The
arithmetic property alone supplies none of these four objects.

## Relative entropy and observation coordinates

A differentiable nonnegative normalized relative entropy vanishes to
first order at an interior matching pair. A signed price cocycle
`A(U)-A(U0)` may have a nonzero active first derivative at that diagonal.
These objects therefore cannot be equated there if the latter derivative
is nonzero. A nonmatching pair can have a nonzero entropy source, which
must be computed rather than inferred.

This argument does **not** apply unchanged to Bianconi's discrete action.
Its equation (41) is

    sigma Tr log Gcal + Tr[Gcal(log Gcal-log G)] - Tr Gcal,

with positive definite cell-metric matrices of possibly nonunit trace.
The volume/trace terms and the induced metric are additional parts of
that action. Its source is not the source of normalized Jones entropy.
A transport must specify the cell cochains, induced metric and its
parameters, as well as positivity and the complete differential.
See [the original discrete construction](https://arxiv.org/html/2404.08556v4).

For the Jones local coordinate map q=q(theta) with nonsingular J=Dq,
an actual covector transforms as

    dS = r_theta^T dtheta = r_q^T dq,
    r_q = J^(-T) r_theta.

An invertible map cannot turn a nonzero covector into zero. The owned
34 coordinates describe metric10+link24 on their homogeneous finite
carrier; they do not absorb independently varied material or controller
directions. Rank establishes visibility, not a value for the full price.

`check_residual_transport.py` checks these algebraic identities and hostile
controls exactly. It does not claim to evaluate an unspecified native R.
