# Independent review: exact moment writer and full source transport

21 October 2026. Bounded independent review for existing Draft #334.
Reviewer: prep_synthesis. The repository was read only. This review
accepts the explicitly scoped mathematical construction; it does not
promote its physical admission or selection premises.

## 1. Frozen inputs and verification

The reviewed packet is in
/workspace/scratch/07af0e1491e7/even_construct/:

| File | SHA256 |
|---|---|
| EXACT_MOMENT_SOURCE_CONSTRUCTION.md | 8c4c3cf03ebf637de6917776f13533d8b9f20cd0e8790025cf64a092915aef15 |
| check_exact_moment_source.py | b289a8b9462d082593858dcba40699aeba58c16e6a3807b689a732f8eaf04b19 |
| MOMENT_SOURCE_PINS.json | 640d1b708d578ef46b4ffa9f3ce122bcef96d712d333c64a1bfc32b3b0c75b7d |
| CHECK_RESULT.json | 05a7daeeba2c127a2213e819bd1bc3b2d5717d7afdd68662cac42122a0770fb8 |
| RESULT_ROOT_OPTIMIZED.json | 05a7daeeba2c127a2213e819bd1bc3b2d5717d7afdd68662cac42122a0770fb8 |

The actual paid writer and counted-CQ ledger consumed by this proof are
digital_construct/PAID_CODE_AND_MOMENT_WRITER.md, SHA256
e95f0486456c53cf0ce40023bab08ac744fd6189b397d29a8773446c168244a0.
Its separate independent review is
book_construct/REVIEW_DIGITAL.md, SHA256
57ffe6313692718255828e757344d15bcc6d7db99d1d9e7d70ec361f6794dd3d.

I inspected the entire final proof and checker, recomputed the displayed
packet hashes, and inspected the root's optimized receipt. The root
performed the optimized execution; its receipt is byte identical to the
author's final receipt. I did not run a redundant third execution.
The checker uses exact rational and Golden-field arithmetic, verifies ten
scientific inputs through historical git show at
311b1d3fd505effe7082754bc80dd17d1097f095, and does not rerun an old root,
rank or all40 suite. Its finite fixtures corroborate the explicit
analytic arguments; they are not substitutes for their all-family proofs.

**Verdict: PASS within the stated addressed-gate, fixed-constant,
counted-CQ and field-chart interface. No mathematical blocker found.**

## 2. Coframe chart, calibration and both ambient jets

The exact identity
D = eta_R (T E)^(-T), D^T eta_R T = E^(-1)
removes the unavailable sqrt(rho) amplitude without altering the
decoded field. Its derivative
delta E = -E (delta D^T eta_R T) E
is an isomorphism on all sixteen matrix directions at every invertible
E in the specified chart. Scaling the sixteen independently prepared
moments by one fixed nonzero rational B_D preserves this property.

The metric distinctions in the final proof are correct. With
g_read = E^T eta_null E,
the density-dressed metric is s^(-2) g_read, whereas the raw frame
T E/(s sqrt(rho)) has metric (s^2 rho)^(-1) g_read.
These are readout/calibration statements. The construction does not
execute a moving raw-coframe Julia operator.

For Z = exterior_square(E^(-1)), the actual primary gives
N=Z-I, N^2=0. The inverse remainder is exactly
P5(Z)-Z^(-1) = -Z^(-1) N^6.
At most two arbitrary derivative insertions leave at least four N
factors in at most three uninterrupted runs, hence an N-squared factor.
Terms with derivatives on the leading inverse also vanish. This proves
the full ambient second jet, including mixed coframe directions and the
nonlinear substitution from D to Z; inserted matrices need not commute.
The raw area factor (exterior_square T)/(s^2 rho) and the net
h^(-2)/(s^2 rho) star normalization are retained. The negative
determinant of T is not replaced by an absolute orientation.

The exact checker compares all 153 Taylor-coefficient matrices through
degree two in sixteen independent D directions at a nonzero primary H.
The analytic argument, not this particular fixture, covers the family.

## 3. All proper-link directions and the C8 substitution

The six displayed rational generators span so(eta_R).
The Cayley map has derivative
delta U = (I-K/2)^(-1) delta K (I-K/2)^(-1)
and the stated smooth local inverse. Thus these six prepared coordinates
cover every original proper-link tangent, separately at each of the four
forward-edge roles. No extra matrix-normal stationarity is silently
claimed or needed for this six-coordinate chart.

At the owned primary B=K/2, B^3=0. The exact remainder
C8(K)-U(K)=-2 B^9 (I-B)^(-1) has zero derivatives through order two:
after j<=2 insertions, 9-j B factors lie in j+1 runs, at least one of
length three. Leibniz terms involving the inverse are killed by the same
argument. This works for arbitrary six-direction perturbations, rather
than just perturbations within the two null generators.

Using the eta-adjoint of C8 for a reverse edge preserves the two-jet
of the true inverse proper link. The proof correctly refrains from
inverting C8 off the primary family. Ordered plaquette multiplication,
the odd curvature and the area contraction preserve these jets by the
product rule, including mixed coframe/link terms. The conservative
degree bound is ten coframe plus thirty-two link factors, hence forty-two.
The exact checker includes all 28 coefficient matrices in six directions
and checks the reverse-edge identity through that order.

## 4. Actual material purification and the reference refinement

Every conditional CAR vector in the four equal branches has norm one
because a^2+p^2=p+p^2=1. The sign kind, selector branch and factory
purifiers remain quantum. In the branch assigned to A=0 or15, the
clock-A interference is 2 a p sigma; its branch weight is one quarter.
Including the original site row weight 1/S gives precisely

mu_(x,A) = a p t_(x,A)/(2S) = 2a psi_(x,A)/S,
psi_(x,A)=p t_(x,A)/4.

The clock population remains p. Orthogonality of the actual site register
and normalization of each complete conditional work vector give
C_mom^* C_mom=I128/128. This remains true when the unselected site/row
banks are included in the complete work vector. No division by an
off-site Fourier overlap, RIGHT operation or supplied moving material
amplitude is required.

Two genuinely independent complete material copies therefore yield the
old calibrated product
psi_(x,A) psi_(y,A) = S^2/(4p) <O_(x,A) tensor O_(y,A)>.
The exact substitution in q is
s^2/(rho h^2) sum eta_aa D_ar D_at Delta_r psi Delta_t psi.
Both factors of the original inverse-PF normalization, the fixed scale
and h are accounted for. In particular the resulting coefficient
s^2 S^2/(4p rho h^2) is in Q(p); it introduces no forbidden radical.
All material and mixed field derivatives are present.

The literal L4 reference is the historically pinned Fourier128 reference,
with coefficients 0 or +/-1/128. The final proof's refinement is an
actual further preparation: append four paid fair site bits at each
step and relabel x -> 2x+delta. After n-2 steps each original row has
2^(4(n-2)) descendants, each multiplied by 2^(-2(n-2)).
Consequently every fine row has squared norm 1/2^(4n), while the sum
of its descendants' RIGHT Gram contributions equals the original one.
The same-site moment and two-copy argument therefore survives exactly.

This inherited fine reference generally differs from recomputing the
first64 Fourier-pair list at the fine mesh. The proof explicitly preserves
that distinction: the present report only consumes the same-site swaps
and independent products; no equality of off-site coherences, raw128
operators, HJR preparation price or complete archives is claimed.
Existence of the original positive mesh densities and fixed normalizations
at each refinement remains a hypothesis, not an output of this isometry.

The new CAR marginal also differs from the original pure matter section.
That is legitimate for this observable consumer, but cannot establish
stationarity of the original independent preparation functional.

## 5. Complete positive report, price and source interpretation

The monomial degree bounds justify the stated finite fresh-copy plan:
forty-two independent geometry arrays per f-probe, and two geometry
arrays plus two actual material copies per q-probe. Every candidate
array and every unused row is prepared and charged. Known fixed
permutations and the owned positive coefficient/majority tables suffice;
no controlled unknown gate or cloning operation is being substituted.
The choice of a larger majority depends on the new fixed coefficient
bound. Its identity first jet and zero second derivative at zero give
the asserted full report two-jet when composed with the P5/C8 fields.

The unchanged literal nu*528*D_j local-copy disintegration is essential.
Separate complete quantum work and final reports give a sum of the
original weighted local entropies, not the entropy of one spatially
averaged Bernoulli. Common padded factory laws give one actual positive
readiness gamma_m; the companion proves the common complete prefix price.
The finite table is prepared before any selected code chooses a row.
Thus the exact finite-node formula
S_m(j)=B_m-gamma_m sum_i c_i h_phi(r_sharp,i(j))
includes the preparation prefix, controller, unused rows and all failures.
An additional state-dependent physical charge is outside this counted
interface and is not disposed of by the inventory argument.

Exact Q(p) nodes give exact values of the declared polynomial report.
Only its primary second jet equals that of the original geometric
report. The central source error is consequently the stated Taylor error
gamma_m M3 delta^2/6; it does not rely on an incorrect off-primary
action equality. The combined moment-to-field map is invertible, so the
full covector transfers, including the original collars and shared-address
identifications. The explicit small nonvacuum primary belongs to this
open material/coframe/link chart and is consumed from its original owner.

Readiness is positive, whereas the raw-J2 calibration is signed:
gamma_1=-alpha beta d0 h'_phi(r0)<0.
The new price is compared to the SAME old counted-CQ price by the positive
readiness ratio. At a primary stationary point the full Hessian therefore
transforms by positive scaling and chart congruence. No raw-J2 Hessian
equality or removal of existing negative field directions is inferred.
The first and second secants are limits of genuine finite word price
comparisons, not derivatives or stationary points of a finite staircase.

## 6. Accepted parent substitution and retained boundary

The construction removes supplied moving Julia amplitudes and supplied
material-copy states from this report implementation. Their relevant
moments, including a nonvacuum primary and all independent source
stencils, are generated by paid finite words. This is a substantive
positive replacement of those input premises on the specified interface.

The deterministic AB/BA alternatives use common quantum blanks, but
their ordered instructions may differ in the complete initial controller.
The separate uniform-code instrument establishes reachability from one
fixed complete programme at its honest averaged price; it does not
select an Einstein code or identify conditional prices with the full
unconditional action. The final proof states both points.

Native physical admission of addressed operations, the compulsory
Book03/Info cut and full physical valuation, autonomous controller
selection, and an original physical stationary/constraint law remain.
The old independent HJR preparation source is not set to zero by
changing the domain to generated words. The prior arithmetic no-go is
respected because the forbidden sqrt(rho) output amplitude is never
prepared. The accepted conclusion is exact finite moment realization
and complete counted-CQ source transport under the displayed hypotheses,
with GR_closed=false.
