# Fixed complete Golden17 readout after compact coherent accumulation

This supplies the explicit final measurement map used in `coherent_execution.md`.
It reuses the original grade-one Choi preparation and six marked effects. The
fixed measurement is represented on a 4×4 grade-one/reference input, inside
the existing CAR16 apparatus. It does not assert native G0 synthesis/payment
or availability of an arbitrary oldRIGHT128 preparation.

## One common input, no programme for the accumulated power

Supply once the same grade-one maximally entangled preparation

    |Omega4> = (1/2) sum_(j=0)^3 |j,j>.

For a compact proper Lorentz matrix P, the CAR16 exterior operator restricts
to P on grade one, and the flagged Julia accumulation branch containing k
good flags gives

    |chi_(P^k)> = (P^k tensor I4)|Omega4> = vec(P^k)/2.

This vector has unit norm. Its right reduced density is exactly I4/4 for all
k and P. The more general scalar-failure theorem preserves any supplied old
reference Gram, but this particular Golden17 measurement fixture uses the
displayed Choi preparation; an arbitrary prescribed rank128 Gram cannot be
silently substituted for it. An additional old reference may be a genuine
spectator when the complete preparation factorization is supplied.

## Complete fixed POVM

Let G_a, a=1,...,6, be the original traceless Lorentz generators in a fixed
Frobenius-orthogonal basis, Tr(G_a^T G_b)=2 delta_ab. Set

    u=vec(I4)/2,       v_a=vec(G_a)/sqrt(2).

The seven vectors u,v_1,...,v_6 are orthonormal. For chi_P=vec(P)/2,

    <u,chi_P> = m(P)=Tr(P)/4,
    <v_a,chi_P> = s_a(P)=Tr(G_a^T P)/(2 sqrt(2)).

Let g=p², p+g=1, b=1/4096 and kappa=g² b/24. Define the twelve fixed effects

    E_(a,+)=kappa |u+v_a><u+v_a|,
    E_(a,-)=kappa |u-v_a><u-v_a|.

They give exactly the original complete Golden/Bell marked probabilities

    <chi_P,E_(a,±)chi_P> = kappa (m(P)±s_a(P))².

Their sum is

    E_marks = 12 kappa |u><u| + 2 kappa sum_a |v_a><v_a|.

Consequently the thirteenth-through-seventeenth completion is explicit:

    E_GGrest = g² b I16 - E_marks,
    E_GB = g p b I16,
    E_BG = p g b I16,
    E_BB = p² b I16,
    E_Bellfail = (1-b) I16.

Here g² b=24 kappa. E_GGrest has exact eigenvalues 12 kappa on span{u},
22 kappa on span{v_a}, and 24 kappa on the remaining nine-dimensional
complement. In particular E_GGrest>=12 kappa I16>0. All seventeen effects
are positive and their sum is I16. This is a globally defined fixed POVM on
the compact Choi state space; the positive square-root chart is needed only
for the signed decoding/overlap formula, not positivity or completeness.

The resulting full distribution is exactly the previously used compact
Golden17 law, including GG-rest, GB, BG, BB and the whole Bell-failure label.
Applying THIS SAME POVM to chi_(P^k) therefore gives q17(P^k). Its effects do
not depend on P, k, h or the field. No additional moving programme encoding
P^k is needed for this mathematical readout. This eliminates a potential
circularity in the accumulated-query argument.

Equality here is of the complete seventeen-label probability law. It does
not establish equality of unmeasured postmeasurement quantum states to every
historical Bell processor implementation. If later future tests interrogate
those states, the required instrument extension must also be specified.

## The resource claim with this map

The same probabilities also have a fixed realization on the **whole CAR16
Choi preparation**, without discarding its other grades. Supply
`Omega16=vec(I16)/4` and accumulate `Lambda(P)` on its left half. Let `Pi`
project onto grade-one left times grade-one reference. On
`chi=vec(Lambda(P))/4`, `||Pi chi||^2=1/4` for every compact P.

Embed `vec(I4 +/- sqrt(2) G_a)` in that block and set

    E_full_(a,+/-) = kappa |vec(I4 +/- sqrt(2) G_a)><...|,
    E_full_GGrest = 96 kappa Pi - sum E_full_(a,+/-),
    E_full_GB = E_full_BG = g p b I256,
    E_full_BB = p^2 b I256,
    E_full_Bellfail = [1-b(1-g^2)] I256 - 96 kappa Pi.

The mark sum on Pi has eigenvalues `48 kappa`, `8 kappa`, and zero on
the same 1,6,9 subspaces; GG-rest therefore has eigenvalues
`48,88,96` times kappa and is zero on the remaining 240 dimensions.
The Bell-failure eigenvalues are `1-b(1+3g^2)` on Pi and
`1-b(1-g^2)` on its complement, both positive. All effects sum to I256.
Their Born law on the complete compact CAR16 Choi state is exactly the
same q17(P). The factor **96**, rather than 24, accounts for the actual
one-quarter grade-one probability. The specified right Gram is I16/16;
this construction does not assert preparation of an arbitrary reference128.

The fixed effects determine record probabilities. A declared instrument
extension, for example their fixed square-root Kraus operators, can retain
the postmeasurement state as well. Equivalence to a different historical
processor on *all future tests* requires a separate instrument map, not just
equality of these seventeen probabilities.

The original exact compact Julia letter uses scalar bad operator sqrt(p) I
and good operator p V(P). Fresh-flag strings therefore generate the actual
conditional states chi_(P^k), with field-independent Binomial(n,g) weights.
The fixed POVM above proves the final law is

    Q_theta(s,r)=g^k p^(n-k) q17_r(P(theta)^k).

The stated exact mixture overlap and flat Fisher now follow on a fully typed
input/process/readout chain. At P(theta)=exp(theta J23), the final fixed POVM
has I_q(0)=4 kappa; retaining all flag strings gives

    I_n(0)=4 kappa E[K²]=4 kappa[n²g²+ng(1-g)].

The h^-2 statement counts exact compact Julia uses. If an admitted physical
implementation approximates each letter with error epsilon_h in the required
joint-reference channel norm, accumulation needs n_h epsilon_h within its
fixed discrimination budget; typically epsilon_h=O(h²). The preparation or
compilation cost of this accuracy belongs in total work. The final fixed
readout needs only h-independent accuracy after accumulation, because the
separated amplified hypotheses have a fixed positive gap. No physical gate,
reset, common-input preparation or readout is declared free.

For a physical source normalized by h^-r, a sufficient per-letter first-jet
error budget for n_h=O(h^-2) compositions is `epsilon_h=o(h^(r+2))`
in the stated small-step regime: exact per-letter derivatives are O(h²),
both value and first-jet approximation errors are at most epsilon_h, and
the cumulative exact and approximate first jets stay uniformly bounded.
The telescoping first-jet error is then O(n_h epsilon_h). In particular
`o(h^4)` is sufficient when r=2. For generic words with merely O(1)
per-letter derivatives, an O(n_h² epsilon_h) derivative term may instead
require `epsilon_h=o(h^(r+4))`; the weaker budget is not asserted there.
This implementation error is separate from the exact finite-cap failure,
which is exponentially small.

## Independent exact validation

`check_fixed_readout.py` verifies the seven-vector Gram, the positive
three-projector GG-rest decomposition, all seventeen effects summing to I,
and the exact Born probabilities on four powers of a noncommuting rational
compact rotation. It verifies the reference Gram I4/4, the flat Fisher from
actual fixed-effect/state derivatives, and the full sixteen flag branches
for horizon n=4. All calculations use exact symbolic/rational arithmetic;
no new detector data or fitted coefficients are introduced.
