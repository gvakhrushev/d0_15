# Causal clock minima and stationary source descent

21 October 2026. Native realization and final composition in existing Draft
PR #334, EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE,
constitutive/native-programme-v1. Local input snapshot
60d57f7c805eccaf827f57648c8555558cc6626b. This bounded application changes
the clock-selection premise of the paired-epoch source transport; it creates
no independent execution or physical action. The integration below preserves
remote 8223d58f9b96d12749c451a551fb54b420abe1f0 in local de6f4f9a.

The [paired-epoch result](A4D_PAIRED_EPOCH_CLOCK_COMPLETE_SOURCE_TRANSPORT_2026_10_21.md)
constructs a stationary clock cut preserving a given conditional H+J+R.
Here that cut is also a global minimum of the feedback in a specified
causal comparison class. Every minimizing cut has the same value and field
source. Uniqueness of the cut is unnecessary. For separately retained clock
epochs, the feedback selection survives a phase-dependent complete word.
The remaining heat, Info, normalization and work determine whether this is
also a minimum of the actual full price.

The consuming parent is the actual clock/cut selection in
[the two-query source construction, sections 21 and 22](sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/TWO_NATIVE_8D_DETERMINANT_SOURCE.md),
then the stationary-section escape in
[global composition section 8.7](A4D_GLOBAL_RESULT_COMPOSITION_2026_10_20.md).
The exact positive GR consumer remains
[the original nonvacuum family](D0_GR_PRIMARY_POSITIVE_CASE.md).

## 1. Clock minimization with a retained initial epoch

Let S be a unitary clock transition and let u, Su, S²u be orthonormal
epochs. Let W_d be one given complete unitary word on data plus all its
retained work. For a fixed active isometry i of dimension d put

    A = i* W_d i,       C = A* A,       0 <= C <= I.

Allow the two-dimensional clock isometries E=(u,v) obeying

    E*E=I,             u* S E=0.                         (1)

The first input epoch is fixed. The second condition prohibits an active
output back into that epoch. It is a declared causal comparison condition,
not a consequence of the verification kernel. The pair E_ep=(u,Su) is
admissible. On the complete unitary S tensor W_d,

    T=E*SE=[[0,0],[a,b]],      A_E=T tensor A.

A unitary compression is a contraction. Thus T*T has eigenvalues
lambda=|a|²+|b|² in [0,1] and zero. With the original r=128 and 0<z<1,
the TRUE complementary feedback is

    F_E=I-A_E* A_E,
    J_E=-r Tr log(I-z F_E)
       =-r d log(1-z)
        -r logdet((1-z)I_d+z lambda C).                  (2)

No selected abort replaces the full complement. Its derivative in lambda is

    partial_lambda J_E
      =-r z Tr[((1-z)I+z lambda C)^(-1) C] <= 0.          (3)

It is strictly negative when A is nonzero. The endpoint cut has lambda=1.
Consequently

    min_E J_E = J_d - r d log(1-z),
    J_d=-r logdet((1-z)I_d+z C).                         (4)

When A is nonzero EVERY minimizer has lambda=1 and gives (4), including
all its actual data derivatives. When A=0 the value identity still holds.
The minimum value is explicitly smooth in any smooth data chart with
fixed d and 0<z<1. No inverse clock Hessian, isolated clock root, or unique
minimizer is required.

This is minimization over an implementation variable at FIXED physical
fields and fixed complete word. It supplies no minimum over metrics or
matter and preserves the existing full-field minimum exclusion.

## 2. The full price and its exact limitation

Use the SAME conditional H+J+R formula as the paired-epoch owner, with

    Delta_E=I_2 tensor Delta_d,     B_E=I_2 tensor B_d,
    Cprep_E=|first> tensor Cprep_d, Z_E=2 Z_d.            (5)

If the actual remaining full price and normalizer ratio are independent
of E on (1), their addition does not change the minimizing set. Then

    min_E S_E = S_d + O,
    O=beta^(-1) log(2 Cwork_E/Cwork_d)-r d log(1-z).      (6)

Here the ratio in (6) is the actual supplied ratio, not a clock-volume
renormalization. Every derivative of O is retained:

    dO=beta^(-1) d log(2 Cwork_E/Cwork_d)
       -beta^(-2) log(2 Cwork_E/Cwork_d) d beta
       +r d/(1-z) dz.                                  (7)

For fixed beta,z,d and a field-independent normalizer ratio, (6) preserves
all coframe, link and matter FIRST sources. Genuine independent internal
equations remain D_internal S_d+D_internal O=0. In particular clock
minimization neither solves an old preparation residual nor makes
normalizer work free.

This removes a SPECIFIC extra assumption inside this interface: G0 need
not choose the displayed endpoint basis uniquely. Any actual minimum in
the admitted causal class gives the same source. The native admission of
that class, the complete word, (5) and the complete remaining price are
still physical application premises.

## 3. Retained epochs need no word factorization for the feedback test

Let a genuine phase-dependent complete word be

    W=sum_c |sigma(c)><c| tensor M_c,                    (8)

where sigma permutes the clock labels and each M_c is unitary on the
full data/work apparatus. The M_c may all differ. Consider diagonal
two-epoch cuts containing the initial label 0, retaining its sharp
preparation, with no active input wrapping in the admitted clock interval.
Assume sigma has no fixed points, sigma²(0) differs from 0, and an active
output into 0 is excluded. The feasible class contains {0,sigma(0)}.

For E_ep={0,sigma(0)}, the true prepared compression is

    A_ep=[[0,0],[A_0,0]],       A_0=i* M_0 i.

Every other feasible pair has no retained arrow and A_E=0. Thus endpoint
feedback is strictly cheaper whenever A_0 is nonzero. No common M_c, clock
reset, or replacement of the chronological word by one elementary tick
has been used.

Write K_E for the ENTIRE actual price outside this feedback, including
heat, Rayleigh/preparation, Info, active-cut preparation, normalizer, word
execution and work, with every genuine derivative. For a dark pair D,

    S_D-S_ep = K_D-K_ep+Gamma,
    Gamma = r logdet(I_d+[z/(1-z)] A_0* A_0) > 0.        (9)

The endpoint is a full-price minimizer against all such D precisely when
K_ep-K_D<=Gamma. Strict inequality gives strict preference. This is the
same-programme finite test to apply to ACTUAL costs; it is not permission
to assign K after calculating Gamma.

The explicit sensitivity matters:

    0<Gamma<=r z Tr(A_0* A_0)/(1-z)
             <=r d z/(1-z).                            (10)

At z=2^-20, r=128, d=4 the last bound is 512/1048575<1.
This compares quantities already in the SAME action units. It does not
identify one G0 primitive charge with one HJR action unit. A genuine
additional price can reverse feedback preference; equal logical
inventories do not establish equal K.

The actual phase-dependent Book03 one-tick transition and its completed
word remain different operators, as the pinned stage-clock owner proves.
Equation (8) improves the clock FEEDBACK test. It does not supply spectator
heat (5), native admission of a macro word, or its Book03 U_N binding.

There is a direct application to that actual one-tick Book03 prototype.
Its retained initial spin4 cut has the original first operation G in
BOTH stored-program blocks, with j*G j=sqrt(p) I_4 and p=phi^(-1).
The feasible diagonal two-epoch cuts contain clock0; clock15 is excluded
because its output wraps to 0. Applying the displayed feedback functional
to that prototype, its minimum among these cuts is

    E={clock0,clock1},
    J_min=-512 log[(1-z)(1-z+z p)].                      (10a)

It is identical for the identity and order programmes. Later X,Y letters
do not enter this one-tick compression. Thus causal cut minimization of
this functional of the literal one-tick operator cannot recover their completed-word
contrast. Other heat, Info and work sources are not being set to zero.
This consumes the actual stage result and prevents using the generic
minimum theorem as a covert tick-to-word identification.

## 4. Clock stationarity alone has two different source branches

An exact control in the same conditional class prevents an overclaim.
Take the five-epoch forward shift, completed cyclically only on unused
inputs, and E_ep=(|0>,|1>), E_dark=(|0>,|2>). Both admit forward active
inputs without a wrap. Both are stationary in ALL pure-clock Stiefel
directions for the feedback, and for spectator H and R.

For a one-dimensional data cut with A=cos(theta),

    J_ep=-r log[(1-z)(1-z sin²(theta))],
    J_dark=-2r log(1-z),
    partial_theta J_ep
      =r z sin(2theta)/(1-z sin²(theta)),
    partial_theta J_dark=0.                             (11)

At cos(theta)=3/5, sin(theta)=4/5 the first derivative in (11) is strictly
positive. The two stationary cut branches have distinct field sources.
These are candidate cuts of one complete unitary; they are not asserted
to be alternatives of a native task that already fixes its cut.

For any clock tangent dE=L E with L anti-Hermitian,
dT=E*(S L-L S)E. At the dark cut T=0, so d(T*T)=0.
At the endpoint cut the diagonal of d(T*T) vanishes; the inverse in the
trace derivative of J is block diagonal. This proves both stationarity
claims. The finite checker also tests all 25 real generators of u(5).

Thus solving pure-clock Euler equations alone does not remove branch
selection. The minimum theorem removes this ambiguity in its declared
causal class WHEN the other actual prices meet (6) or (9).

## 5. Source descent after actual internal equations

There is a useful weaker route than requiring equal prices on ALL histories
with the same metric. Let pi:X->M be a smooth submersion from one admitted
full programme chart to its external field chart. S is its actual C2
action. Let C be a smooth component of its full VERTICAL critical locus,

    dS|ker(D pi)=0.

Assume pi|C is a surjective submersion and its fibres are path connected.
Then S|C descends to a smooth scalar I on M and its full horizontal source
is unique, independently of a chosen stationary section.
These are the actual constrained charts, with only justified gauge
directions removed. A singular critical set or an unsolved constraint
range does not acquire these hypotheses through a formal inverse.

Indeed S is constant along each vertical critical path. Local sections
of pi|C define I, and connected fibres make their values agree. Equivalently
alpha=d(S|C) is closed and annihilates vertical tangents, so
L_V alpha=i_V d alpha+d(i_V alpha)=0; the horizontal covector is constant
along each fibre. The induced source is dI. Locally unique stationary
branches modulo actual gauge give another sufficient case.

For disconnected stationary branches, an actual native choice or equality
of their horizontal sources is still needed. Local reduced actions may
differ by field-independent overlap constants while defining the same
Euler source. No equality of arbitrary paid history prices is necessary.
Equation (11) shows why the branch condition cannot be omitted.

On a condensed/profinite presentation apply the equalizer condition to
the SELECTED vertical-critical object covering the metric chart, with its
actual smooth local sections. The theorem above can establish that
equalizer; profinite naturality alone establishes neither connected
critical fibres, physical selection, nor differentiability.

## 6. A weaker native scale test before Golden rigidity

Exact scaling of the full action away from its internal stationary locus
is also stronger than needed. In local field/internal coordinates (g,zeta),
put E_zeta=D_zeta S. Let a supplied physical lift

    T_rho(g,zeta)=(rho g,Phi_rho(g,zeta)), rho=phi²,

have an invertible vertical derivative. Define its ACTUAL scale defect

    D_rho=S composed with T_rho-rho S.

If dD_rho=0 on the selected internal critical component, the chain rule
gives E_zeta(T_rho)=0 there and the correct reduced source scaling,
provided the target critical branch is the selected one. Connected
critical fibres remove the target ambiguity when the image lies in
the covering critical object of section 5. If that object contains ALL
admitted vertical critical points, the image condition follows from
admission of T_rho and E_zeta(T_rho)=0. For a restricted selected branch,
its physical equivariance remains an explicit requirement.
On a connected reduced chart I[rho g]=rho I[g]+constant.

For example a physically derived identity

    D_rho=constant+sum_ab E_zeta,a H_ab E_zeta,b           (12)

is sufficient: its full first differential vanishes when E_zeta=0.
Equation (12) is a CHECK of a given action and physical lift. Introducing
it as a correction would choose a new action. Merely making D_rho constant
on a parametrized section is insufficient: its normal derivative may
move the image away from internal stationarity.

An exact scalar control makes the difference visible. With

    S(x,t)=x+(t-x²)²/2,
    Phi_rho(x,t)=t+(rho²-1)x²,

the defect is (1-rho)(t-x²)²/2, although the unreduced expression is not
homogeneous with t held fixed. Its true stationary reduction is I=x.
Adding a nonzero constant a to Phi leaves a constant defect a²/2 ON the
old section, but the new internal source equals a, so that is not an
admissible stationary transport.

Now consume the existing Golden rigidity theorem. If the selected reduced
GRAVITATIONAL action is metric-only, local and open-Diff-invariant, its
source is differentiable at flat sections, and the actual physical scale
lift passes this first-jet test, its covariant Euler tensor is aG.
Local Diff invariance supplies the Ward identity; no new second-order
assumption is needed. Matter is retained separately on the SAME action.
Only actual full stationary flat and nonvacuum witnesses calibrate the
ratio -lambda_minus. Internal clock minimization does not derive native
field stationarity or open-Diff coverage.

## 7. The composed physical application

The synthesis replaces two unnecessarily strong demands. Within sections
1 and 2, unique selection of a particular clock basis is replaced by
source equality of all true causal minima. Within sections 5 and 6,
descent of arbitrary histories and full off-stationary scale invariance
are replaced by descent and a first-jet symmetry on the actual selected
internal critical object.

To apply this to D0, evaluate ONE admitted full Book programme, its actual
causal comparison class and K_E in (9). Solve its other independent
preparation, Info, oldRIGHT, work and controller equations including (7).
Use its native stationary/constraint law and actually reachable physical
tangents. Then test physical metric descent, Diff contexts and the
first-jet scale defect of THAT programme. The original all40+2 solutions
and recovery, or Golden rigidity plus their calibration, are the existing
consumers. No new geometry search is called for.

## 8. Application after the concurrent native source integration

The [current causal native synthesis](A4D_CAUSAL_NATIVE_SOURCE_AND_WEIGHTED_DYNAMICS_2026_10_21.md)
already supplies a finite polynomial report with the original full ambient
two-jet, a complete forward full128 archive determinant equal to the
original J_n plus its retained clock boundary, and the actual weighted
continuum consumer. Reuse these maps. The two-epoch minimum theorem is a
supporting selection test for its specified class; it does not identify
that class with the already constructed full128 archive window or the
new report with the old full128 price.

The concurrent coherent cap2 preparation reduction and actual N=1 CQ
constitutive source also remain separate executions. Their established
stationary and field-source maps are inputs to the
[one admitted common-map gate](A4D_NEXT_COMMON_MAP_CONSTRUCTION_GATE_2026_10_21.md),
not a reason to equate their information cuts or independently free inputs.
The original nine-file clock handoff is now present on the fetched remote
8223d58f: every manifest-listed Git blob was compared successfully.

The [Book source identifiability theorem](A4D_BOOK03_SOURCE_IDENTIFIABILITY_THEOREM_2026_10_21.md)
pinpoints the remaining valuation data. On a connected positive history
support, actually derived relative branch weights and jets leave one
common absolute weight and its first jet. The closed memory feedback
sees that mode. Neither normalized observations, a stationary clock cut,
nor condensed descent specifies it. Dark support births retain their
amplitude/source obligations; this statement does not discard them.

Thus the next consuming calculation is the SINGLE common native
field-to-instrument-to-Book map and its literal branch gain plus absolute
normalizer jet, with the complete independent-input price. The clock
budget (9) and critical scale test (12) can evaluate that map; they cannot
define its missing price. On the finite positive route its all42 source
and internal equations consume the exact Einstein family. On the
universal route its genuine metric/Diff/flat-smooth reduced source and
physical scale lift consume Golden rigidity. The latter is an independent
shortcut, not an added prerequisite of the finite witness route.

The bounded checker pins eight inputs and uses exact complete unitary
matrices, non-diagonal C, all clock tangent generators, a genuinely
phase-dependent word, the work-price reversal, and scale-lift controls.
It does not compute the missing physical K_E, select Book Info, solve the
upstream preparation source, or prove that G0 admits the proposed clock
variation. Full physical D0 selection, GR_closed and raw216 remain open.

Run
[check_causal_clock_descent.py](sources/d0_native_gr_completion_synthesis_2026-10-20/source_selection/metric/check_causal_clock_descent.py)
from the repository root. Its
[exact receipt](sources/d0_native_gr_completion_synthesis_2026-10-20/source_selection/metric/CAUSAL_CLOCK_DESCENT_CERTIFICATE.json)
records the finite controls separately from the analytic conditional
theorems. The
[validation receipt](sources/d0_native_gr_completion_synthesis_2026-10-20/source_selection/metric/CAUSAL_CLOCK_DESCENT_VALIDATION.json)
records the optimized replay, three rejected mutations and affected
structural checks. Publication of the earlier clock files is distinct
from independent physical acceptance of their interpretation.
