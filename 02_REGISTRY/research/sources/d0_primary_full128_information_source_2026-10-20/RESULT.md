# Full128 common-record source on the configured primary family

20 October 2026. Research application in existing Draft PR #334.
Phase: native realization. Consumer: the missing common-history information
and paid-source map in `constitutive` / `native_sector`, after the strict
native-domain application at `1e850b0f15897ba8a826106bcff681b11eccfefa`.
The complete native physical price, Book03 information binding, preparation
Euler equations, physical clock and GR closure remain open.

## 1. Same process and exact target

Use the original complete retained-record instrument from
`A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md` sections 1--3 and
the actual port code in
`sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md`.
Use the configured primary family, inverse-leg Dirac operator, strict fixed
Golden scale and actual preparation in
`sources/d0_primary_native_domain_source_2026-10-20/RESULT.md`.
These are owned inputs, not new geometric or all40 proofs.

The data space contains every site and all16 original CAR grades. The
preparation matrix C has all128 oldRIGHT columns, norm `||C||_HS=1`, and
the actual unequal n20 Golden F/R density. Set

    p = phi^-1, p+p^2=1,
    A = ell D/16 = A*, epsilon = p^2 ell^2/64.

Here D is already the transported strict-domain operator. The fixed
scale s=p^3 is part of the supplied chart, not an extra factor in these
formulas. All field derivatives use the true positive adjoint. The
coordinate `ell=1/L` and the one-round registration are fixed during
the field variations below.

For role r=0,...,3 let `P_r=X_r S_r` and let `C_r` denote the same
role's on-site CAR map (distinct from the preparation matrix C).
Define the16 distinct original Julia top rows, with i=4r+j:

    (U_(i,0),U_(i,1)) =
       (P_r,       L(P_r)),
       (P_r*,      R(P_r)),
       (-C_r,     -L(C_r)),
       (-C_r*,    -R(C_r)),
    L(X)=sqrt(I-XX*), R(X)=sqrt(I-X*X).

Each pair obeys `sum_c U_(i,c) U_(i,c)*=I`, and
`sum_i U_(i,0)=ell D=16A`. Both identities use every role and both
defects. The original32 SELECT words repeat each pair twice.
Let `H_(l,j)=(-1)^popcount(l&j)`, l,j=0,...,31, and alpha=(l,c).
The literal64 rows and128 retained output maps are

    N_(l,c) = (1/32) sum_i [H_(l,2i)+H_(l,2i+1)] U_(i,c),
    N_(0,0)=A, sum_alpha N_alpha N_alpha*=I,
    M_alpha = delta_(alpha,0) I - 2 N_alpha* A,
    K_(0,alpha) = delta_(alpha,0) I - 2p^2 N_alpha* A,
    K_(1,alpha) =                     - 2p sqrt(p) N_alpha* A.

The reference columns and all128 physical labels are retained. The
compression below is an algebraic way to compute this original output;
it is not a changed physical pointer basis or free implemented decoder.

## 2. Field-independent33-vector compression

Define the real64-by32 matrix

    G_((l,c),(i,d)) = [H_(l,2i)+H_(l,2i+1)] delta_(c,d)/8.

Walsh orthogonality gives `G*G=I32`. Also
`sum_i G_((l,c),(i,0))/4=delta_(l,0)delta_(c,0)`.
Consequently `N_alpha=(1/4)sum_(i,c) G_(alpha,(i,c)) U_(i,c)`
and the33 operator amplitudes

    L_0 = sqrt(p) I,
    L_(i,c) = (p/4)[delta_(c,0) I - 2 U_(i,c)* A]

obey `sum_(i,c) G_(alpha,(i,c)) L_(i,c)=p M_alpha`.
Define the real128-by33 matrix B by

    B_((0,alpha),0) = sqrt(p) delta_(alpha,0),
    B_((1,alpha),0) = -p      delta_(alpha,0),
    B_((0,alpha),(i,c)) = p       G_(alpha,(i,c)),
    B_((1,alpha),(i,c)) = sqrt(p) G_(alpha,(i,c)).

Then **B*B=I33 and K_gamma=sum_j B_(gamma,j)L_j**.
Indeed the first column has norm squared p+p^2=1, its cross terms
cancel, and the remaining Gram is `(p+p^2)G*G=I32`.
The first physical port gives `p delta I+p^2 M`; the second gives
`p sqrt(p)(M-delta I)`, exactly the original Kraus maps.

This also proves normalization without diagonalizing a data operator:

    sum_(i,c) L_(i,c)* L_(i,c)
      = (p^2/16)[16I-32A^2-32A^2+64A^2]
      = p^2 I,
    sum_j L_j*L_j = (p+p^2)I=I.

The identities hold for arbitrary strict native fields, not just for
the configured solutions. B is independent of every field, observer
trivialization, preparation and clock coordinate. Its only scalar is the
fixed Golden p. Therefore differentiation commutes with reconstruction.

## 3. Both information observables and their full first sources

Flatten each data-by-reference amplitude `V_j=L_j C` as one column
of V, and put `Gamma=V*V`. The reduced record density in the physical
128 basis is `B Gamma^T B*` with the usual column inner-product
convention. Its nonzero spectrum is that of Gamma. Since B is real,
its diagonal is also `diag(B Gamma B*)`. Thus

    q_gamma = ||K_gamma C||_HS^2 = [B Gamma B*]_(gamma,gamma),
    H_pointer = -sum_gamma q_gamma log q_gamma,
    S_record = -Tr Gamma log Gamma,
    Tr Gamma = sum_gamma q_gamma = 1.

Logarithms here are natural. Divide both entropy sources by `log(phi)`
when comparing to the stated Golden code-cost units. Coherent record
entropy and entropy after dephasing in the literal pointer basis are
different observables. The33 compressed diagonal entries are NOT
physical pointer probabilities.

On any differentiable admitted real tangent, including a preparation
jet when it is present,

    V_j' = L_j' C + L_j C',
    Gamma' = V'* V + V* V',
    q_gamma' = [B Gamma' B*]_(gamma,gamma),
    Tr Gamma' = sum_gamma q_gamma' = 0.

At positive spectral values the entropy source is
`-Tr Gamma'(log Gamma+I)` and the pointer source is
`-sum q_gamma'(log q_gamma+1)`. Zero values are interpreted through
the amplitude factorization, not by a numerical probability floor.
At a zero eigenvalue `u`, `Vu=0` and `u*Gamma'u=0`; the entropy
derivative extends continuously through a smooth rank birth.

For an explicit stable finite calculation use, for eta>0,

    S_eta(Gamma) = -Tr Gamma log(Gamma+eta I33),
    S_eta' = -Tr Gamma'[log(Gamma+eta I33)
                                +Gamma(Gamma+eta I33)^-1].

There is no eigenvalue deletion, renormalization or hidden cutoff.
For a dimension-d amplitude Gram,

    0 <= S-S_eta <= d eta,
    |S'-S_eta'| <= 4 sqrt(d eta) ||V'||_HS.                 (1)

Proof: `x log(1+eta/x)<=eta`. If lambda is a positive eigenvalue
with eigenvector u, then
`|lambda'|<=2 sqrt(lambda)||V'u||`. The derivative difference factor
is `log(1+eta/lambda)-eta/(lambda+eta)`, between zero and
`2 sqrt(eta/lambda)`. Cauchy--Schwarz over d vectors proves (1).
At a zero eigenvalue the limiting contribution is zero; the same
bound is uniform through rank changes. These bounds also establish
the stated continuous source extension for a C1 amplitude family.

For the128 pointer amplitudes the same proof yields value error at
most128eta and source error at most
`4 sqrt(128eta)||V'||_HS`; B is an isometry and preserves the jet
Hilbert--Schmidt norm. These are analytic regularization bounds.
They do not certify floating-point eigensolver or arithmetic errors.
The numerical receipt reports those diagnostics separately.

## 4. Actual paid-port source on the same output

The owned original direct0/return10 port code charges `1+b`.
Its complete one-round expectation and source are exactly

    Cost_port = sum_(b,alpha)(1+b)q_(b,alpha)
              = 1+p epsilon R,
    R=||D C||_HS^2,
    Cost_port' = p epsilon R' + p epsilon' R.             (2)

Equation (2) includes every retained label, both ports and all
reference columns. It is only the derived port component of physical
cost. It does not set preparation, label, controller, archive or work
costs to zero. The derivative of the actual record probabilities is
an independent check of this cost identity and its source.

For a flat common coframe scale `e(a)=a e_0` at fixed inverse-leg
chart, observer, density, preparation and ell,

    D(a)=a^-1 D(1), R(a)=a^-2 R(1),
    dCost_port/da|_1 = -2p epsilon R(1).

The actual reference contains nonconstant transverse characters,
so R(1)>0. This tangent scales the whole finite periodic flat
coframe. It is a common-field source diagnostic, not a variation
with a fixed exterior coframe collar. The nonvacuum link test below
instead has genuinely supported interior variation and fixed collar.

A diagonal comparison whose contrast information is identically
zero has zero common-scale derivative. The common retained-record
entropy above need not vanish, and is what this application computes.
For either candidate information I, a necessary cancellation equation is

    (Cost_extra-Info_extra)' = -(Cost_port-I)'.

This is an interface requirement for an actual paid construction,
not permission to add a fitted counterterm. Positive cost values do
not imply positive field derivatives. A failure for either candidate
does not exclude all possible complete D0 prices.

## 5. Computation and acceptance boundary

The numerical application uses exactly the supplied L4 primary fixture:
256 sites, CAR16, oldRIGHT128, original exterior order `(0,2,3,1)`,
actual n20 nonuniform F/R density, fixed s=p^3 and the actual
`m(Psi/s^2)` preparation. The two nonvacuum representatives have
harmonic amplitudes1/8 and1/4. The free u-link at `(1,1,2,2)` is
varied independently while the stored collar is held fixed.
Periodic storage of the polynomial fixture does not assert a global
periodic polynomial solution.

The checker must verify both shifted Julia defects and their Sylvester
jets, the reconstructed full output normalization and its first jet,
the direct original port-cost identity, and the entropy jets against
independent finite differences of the regularized values. It reports
eta, amplitude jet norms, analytic regularization bounds and floating
spectral diagnostics. The checked numerical instances and outcomes are
recorded with the frozen receipt and review.

At eta=1e-12 the uniform flat source of port cost is
`-0.00316136874364584`; the pointer and coherent entropy sources in
nats are respectively `-0.0360811536994540` and
`-0.0324560263641649`. Thus the two candidate price sources in
Golden units are `+0.0718184048622605` and `+0.0642850751589845`.
For the supported nonvacuum u-link tangent they are respectively
`(+4.99534781867e-7,+4.44158137473e-7)` at amplitude1/8 and
`(+5.17898344542e-7,+4.60625574975e-7)` at amplitude1/4.
On both curved rows, (1) contributes less than3.66e-8 /1.86e-8
in those respective Golden units. The maximum observed curved
entropy finite-difference discrepancy is1.04e-11 nats.
These are scoped floating diagnostics with explicit regularization
bounds, not a rigorous interval sign certificate.

The independent literal original Walsh sums reconstruct all128
probabilities and their jets on the flat and both curved fixtures.
Maximum probability discrepancy is below5e-15 and jet discrepancy
below1.5e-18. The four flat role-scale sources sum to the uniform
source. The latter verifies `R'=-2R`; the curved R and R' agree
with the published predecessor receipt to less than1e-12.
No new all40 or Rayleigh-source derivation was substituted for that
published input. The smallest recorded Gram eigenvalue, including
finite-difference points, is approximately -2.56e-17; every explicit
log argument exceeds9.99974e-13 without clipping.

The exact33-vector reconstruction removes the missing computation
map from the actual complete one-round native record to both specified
information-source candidates on this primary preparation. Numerical
source comparisons have the precision and tangent scope of the receipt.
This does not identify Book03 Info, complete physical payment or the
executed physical duration, solve internal preparation/controller Euler
rows, establish a refining full-price root, or close any GR assembly
obligation. `GR_closed=false`.
