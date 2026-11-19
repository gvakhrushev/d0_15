# Original full128 cost-marked archive: uniform normalization and the Golden-clock source law

21 October 2026. Continuation of existing research PR #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`,
`constitutive/native-programme-v1`. Scientific input:
`b60a111b43f723a841d253b1d5bd9650c46b2cf8`.

## 0. Exact new substitution and its boundaries

Two source owners now compose: the original complete-history C1 limit on its
128-dimensional first Fourier shell, and the corrected *operator-normalized*
complementary Book determinant. The first owner supplied a positive denominator
as a separate hypothesis; the second provided only a finite-horizon bound
which decays exponentially with the number of paid rounds. This packet proves
that the denominator for this specified cost-marked interface is instead
controlled by the original **excess-count effect**, and applies it on the
actual longer physical horizon `n_h=128 h^-4`.

The main application is stronger than a probability calculation. On that
same first-shell chart, the **entire normalized cost-marked coherent archive**
is equivalent in the continuum to the original complete archive with an
explicit event-time change and a field-independent port operation. For the
specific EXTRA amplitude mark `phi^(-Cost)`, the event-time factor is exactly
`p=phi^-1`, and the operation is just exchange of the two nonblank ports.
The orphan port1/blank outcome is retained at finite h and tends to zero with
its source; it is never identified with the ordinary blank.

The corresponding absolute complementary-feedback value and first source
have explicit C1 limits. All128 outcome labels, all16 CAR grades on each
of the eight modes, and the actual oldRIGHT128 trace multiplier remain.
No normalized trace replaces the original counting trace.

This is NOT a proof that Book03 chooses this extra mark, that its memory
algebra equals a scalar weighted Kraus sum, or that the normalized transform
is a freely executable hardware operation. It does not identify the full128
with the different N=1 CQ compiler. It does not establish the 42-direction
nonvacuum spatial source, physical field writing, full Info/work equations,
or raw216. `GR_closed=false`.

The finite-matrix normalization/Doob-transform background is standard; see
Carollo et al., Phys. Rev. A 98, 010103(R), arXiv:1711.10951, and Cilluffo
et al., *Microscopic Biasing of Discrete-Time Quantum Trajectories*, Quantum
Sci. Technol. The new contribution is the following explicit D0 application,
its physical-horizon bound, port/clock intertwiner and retained price boundary.

## 1. Original complete charge and removal of a representation scalar

Let `K_omega` be the chronological Kraus product of an actual n-round native
execution, with every complete history retained. Its isometry is

    V_n = sum_omega |omega> tensor K_omega,    V_n* V_n=I.

The literal port charges are `c_b=1+b`, b in {0,1}. Thus

    C_omega=n+B_omega,    B_omega=sum_j b_j >= 0.

For a FIXED analytical cost mark t>=0,

    W_n,t = sum_omega exp(-t C_omega/2)|omega> K_omega
          = exp(-tn/2) Wbar_n,t,
    Wbar_n,t = sum_omega exp(-t B_omega/2)|omega> K_omega.

Write `Nbar=Wbar*Wbar`, and let i be the same rank-d active embedding.
The corrected owner proves, with `A=i*Wbar`, `G=A*A`, r=128 and 0<z<1,

    Q=(1-z)Nbar+zG,
    Jhat=r logdet Nbar-r logdet Q.                         (1)

Consequently the scalar `exp(-tn/2)` cancels from Jhat EXACTLY; its field or
mark derivative also cancels if both determinant arguments are varied.
This is a representation identity, not subtraction of the n paid ticks.
Their actual cost and their role in programme comparison stay present.
A physical attenuation carrying its own failure flag is a different map.

## 2. The all-horizon denominator is paid-count controlled

Define the original excess-count effect

    T_n=sum_omega B_omega K_omega* K_omega.

**Theorem 1.** If `T_n <= M I`, then

    exp(-t M) I <= Nbar_n,t <= I.                         (2)

This is valid for arbitrary noncommuting original Kraus products, all zero
outcomes, all retained references, and a nonuniform complete record.
No independent-round distribution, spectral floor of individual histories,
or extra state preparation is assumed.

Proof. For any unit vector u, `q_omega=||K_omega u||^2` is a probability law.
Scalar Jensen applied to the convex function `exp(-t b)` gives

    <u,Nbar u> = E_u exp(-t B)
               >= exp(-t E_u B) >= exp(-t M).

The upper bound follows from `B>=0`. Testing all u proves the operator
inequality. We have NOT used operator convexity of the exponential.
The same proof holds for a countable complete record when its first count
moment is finite, by monotone finite truncation with the complement retained.

For the repeated original round, with `Phi*(X)=sum K_gamma* X K_gamma` and
`E1=sum_port1 K_gamma* K_gamma`, its exact effect is

    T_n=sum_(j=0)^(n-1) (Phi*)^j(E1).                    (3)

Thus the bound uses an already physically identified cost observable.
An expectation in just one prepared state is NOT an operator bound on all
inputs. On a supplied isometric input section E one may apply (2) to
`E*T_n E`, but that is the specified restricted input/return cut, not a
silent replacement of the full ordinary Book trace by a rank128 trace.

## 3. Full first-source transport; no entropy or probability floor

Suppose the complete original isometries have a common record embedding and
converge in operator C1 on a fixed finite input space. Assume the embedding
preserves the port1 count. The multiplier

    M_t|omega>=exp(-t B_omega/2)|omega>

is then one fixed bounded operator, norm at most one, on that common carrier.
The time-cell/ordered-history embedding of the consumed source has exactly
this property. Hence `Wbar_h=M_t V_h` converges in C1. If the count budgets
are bounded by one M on the parameter chart, (2) gives a uniform lower
bound, and inversion, square root and (1) preserve C1 convergence.

A useful absolute bound avoids differentiating square roots. Let

    Pi_W=Wbar Nbar^-1 Wbar*,     R=i* Pi_W i.

The corrected normalized owner gives

    Jhat=-r logdet[(1-z)I+z R].                           (4)

For a tangent, `D Pi_W` is an off-diagonal Hermitian block relative to Pi_W:

    D Pi_W = (I-Pi_W) D Wbar Wbar^+ + adjoint,
    ||D Pi_W|| <= ||D Wbar|| / sqrt(eta),
    eta=exp(-tM).                                        (5)

For completeness, the norm of `[0,T*;T,0]` is `||T||`, not the sum of the
two block norms. If `||D V||<=K` and `||D i||<=K_i`, then

    |D Jhat| <= r d z/(1-z) [K/sqrt(eta)+2K_i].           (6)

The dimension d and actual RIGHT factor r are not discarded. To use an
original h-dependent raw source norm or divide by a small geometric gain,
those additional factors must explicitly enter the budget. This theorem
alone gives no whole-lattice/raw216 bound.

Moving t, genuinely moving charges, and moving active cuts contribute their
own derivatives. The displayed C1 statement holds with t fixed, or for such
motions only when their actual marked-operator derivatives are controlled.
It does not grant a freely adjusted clock/calibration law.

## 4. Stable noncommuting source and the exact reverse recursion

At fixed z, put `dG=dA* A+A* dA`. The source can be evaluated without the
cancellation of two O(1) traces at the native `z=2^-20`:

    H=Nbar^-1-(1-z)Q^-1 = z Nbar^-1 G Q^-1 >=0,
    dJhat=r Tr(H dNbar)-r z Tr(Q^-1 dG).                 (7)

The last ordered product is Hermitian because it equals the preceding
Hermitian difference. No Nbar/G commutation is required.

For step-dependent tilted maps `L_j*` and their actual jets, let
`N_j=L_j*(N_(j-1))`, `N_0=I`. Initialize `P_n=rH`, and propagate backward

    P_(j-1)=L_j(P_j).

Then the complete normalizer source is exactly

    r Tr(H dN_n)=sum_j Tr[P_j (dL_j*)(N_(j-1))].          (8)

Add the corner term from (7). This is the same complete-history source as
the forward product rule, using n operator recursions instead of enumerating
128^n histories. It is an explicit application of causal adjoints, not a new
variational price. The checks compare it with direct two-round histories
and independent field finite differences on the actual original CAR fixture.

There is also a useful all-size sign. With the active corner being the all
port0/blank word, its baseline-stripped A does not depend on t. Since

    partial_t Nbar = -sum B_omega exp(-tB_omega)K_omega*K_omega <=0,

(7) proves `partial_t Jhat<=0`. It is strict when A is invertible and a
positive excess event has nonzero effect. This is a source of this defined
marked functional, not an independently admitted physical Euler equation.
An extra physical mark controller must retain its own cost and Info.

## 5. Exact application on the original physical first shell

Use the input owner RESULT.md, sections1--6.1. DATA is its eight first
Fourier characters times all16 CAR grades, so d=128. Tensor with actual
oldRIGHT128. Let a lie in a fixed compact positive interval, h=1/L,

    nu_h=h a,       w_h=4 sin^2(pi h),
    epsilon_h=p^2 h^2/64,     n_h=128 h^-4,
    Delta_h=a^2 w_h I,
    s_h=epsilon_h a^2 w_h/2,
    B_h=(1-s_h)I,             E1_h=2p s_h I.             (9)

Integers n_h are fixed while differentiating a. All every-round physical
costs are still paid. The old horizon 128 h^-2 has a blank limit on these
physical fields; it is not substituted for the longer one.

Because E1_h is scalar, the port1 count law is binomial on EVERY initial
DATA/oldRIGHT preparation, even though individual jumps change the data.
Successive summation of the actual instruments proves this statement; no
reset or independent-copy assumption is used. Therefore, with
`kappa_t=1-exp(-t)`,

    T_n=2pn s_h I,
    Nbar_n,t=(1-2p kappa_t s_h)^n I,
    X_h=Ahat*Ahat=[(1-s_h)^2/(1-2p kappa_t s_h)]^n I.    (10)

The scalar character of this NORMALIZER is derived on this special shell.
It is not borrowed into a curved, inhomogeneous or general boosted field.

The uniform source limit follows by differentiating the elementary logarithm
in (10). Define

    tau(a)=8 pi^2 p^2 a^2,
    eta_t=1-p(1-exp(-t))=p^2+p exp(-t).

Then, on compact positive a charts,

    Nbar_h -> exp[-p kappa_t tau(a)] I,
    X_h -> exp[-eta_t tau(a)] I,                         (11)

and both limits are C1, with O(h^2) error for these scalar functions.
Indeed `2n_h s_h=2p^2 a^2 w_h/h^2 ->8pi^2p^2a^2=tau`, and
`n_h s_h^2=O(h^4)` with its a derivative. The usual sine expansion gives
the remaining O(h^2) error. This is an elementary uniform compact-chart
estimate, not a numerical extrapolation.

At all t>=0, the exact shell lower bound can be strengthened to

    Nbar_h >= (1-2p s_h)^n I,

whose limit is `exp(-p tau)I>0`. Thus even an indefinitely strong EXTRA
port1 mark does not destroy the normalized shell denominator. The general
Jensen bound (2), which is needed off this scalar shell, remains valid.

The actual unnormalized complementary action and source are

    J_t(a)=-16384 log[1-z+z exp(-eta_t tau(a))],
    dJ_t=16384 z exp(-eta_t tau)/(1-z+z exp(-eta_t tau))
                       [eta_t d tau+tau d eta_t].       (12)

At FIXED t, `d eta_t=0`, so `partial_a J_t>0`. In fact

    partial_a J_t >=16384 z p^2 tau'(a) exp(-tau(a))>0.  (13)

This excludes disappearance of this fixed-mark source on any compact
positive a chart. If the mark really moves, `d eta_t=-p exp(-t)dt` must
be kept; fixing `eta_t tau` would be an actual coupled variation, not a
vanishing independent a-source or a native selection law.

Numerically at a=.7,t=.7,z=2^-20 the limiting excess count is about
9.1331983948, and `partial_a J_t=1.72332434054e-5`. At L=128 the
analytical finite formulas describe 34,359,738,368 real rounds; the checker
does NOT simulate that many rounds. It evaluates (10), retaining the huge
baseline in the reported round count. No execution-time or cheap-resource
claim is made.

## 6. The full coherent archive intertwiner, not just its blank probability

The owned common limit has a scalar no-jump generator `-Delta_0/2` with
`Delta_0=4pi^2a^2 I` and total event time `T=2p^2`. For each nonblank
SELECT index alpha, its original limiting jumps are

    L_(0,alpha)=-p N_alpha* D_0,
    L_(1,alpha)=-sqrt(p) N_alpha* D_0.                   (14)

The special `(port1,SELECT0)` jump tends to zero with its first field jet.
All pairs in (14) share one port vector

    v=(p,sqrt(p)),   ||v||=1.

An extra amplitude cost marker multiplies port1 by exp(-t/2). The marked
port vector is `sqrt(eta_t) v_t`, where

    v_t=(p,sqrt(p)exp(-t/2))/sqrt(eta_t).

The global normalization in (11) changes the no-jump amplitude to
`exp(-eta_t Delta_0 T/2)`. Consequently every ordered k-event amplitude
is the product of the actual ordered data jumps, the new port vectors,
and this same scalar no-jump factor. No commutativity of the ordered data
jump operators is used.

Choose an orthogonal port matrix O_t with `O_t v_t=v`. Apply it to each
paired event mark, fix the orphan mark, and compress time by
`s_j=eta_t t_j`. The unitary map on the k-event L2 sector multiplies the
amplitude by `eta_t^(-k/2)`, exactly cancelling the k jump factors
`sqrt(eta_t)`. The resulting amplitude is precisely the original unmarked
archive at total time `eta_t T`, with the SAME field a and initial state:

    U_t Vhat_t(T,a)=V_0(eta_t T,a).                     (15)

The same field-independent U_t intertwines the first a derivatives. The
identity includes every ordered mark, all conditional work/data states,
coherences, and oldRIGHT on the declared full128 output interface. It does
not include a newly invented archive of all gate-factory/primitive stages.

The meaningful Golden specialization is

    t_*=2 log(phi),     exp(-t_*/2)=p,
    eta_(t_*)=p,       v_(t_*)=(sqrt(p),p).

Here O_t can be chosen to be the literal port swap X. Thus

    U_Golden Vhat_cost(T,a)=V_0(p T,a).                 (16)

The mark is specifically an EXTRA factor `phi^(-C_omega)` on the actual
Kraus amplitude, as in the corrected marked-owner convention. Equation
(16) does not assert that this is the physical Book weight on normalized
memory classes; doing so would repeat the previously corrected double
counting/binding error.

There is also an exact finite-mesh local check. For alpha!=0 the original
Kraus pair obeys `K_1=K_0/sqrt(p)`. Multiply port1 by p and swap:

    X diag(1,p) (K_0,K_1)^T = sqrt(p)(K_0,K_1)^T.       (17)

The ordinary blank is fixed. The orphan is also fixed and multiplied by p,
not identified with the blank; its scaled jump norm is O(h^2), so its
complete bounded-time amplitude and first source vanish with the owned
common-history estimates. Finite discrete equality to a shorter-horizon
archive is NOT asserted. Equations (15)--(16) are C1 continuum identities.

For general t the same limiting DATA channel has its generator multiplied
by eta_t. Complete records still have a different labelled port law until
the explicit O_t is applied. It would be incorrect to infer equality of
complete archives merely from equality of DATA channels.

## 7. Same-initial realization candidate and the non-free clock/price boundary

The right side of (16) is not a freely supplied programme state: it is the
limit of the ORIGINAL native isometry run for `m_h=floor(p n_h)` rounds,
with the same input and coframe, followed by the fixed event-label map.
The source owner's trajectory construction applies on that convergent
shorter horizon. Together with Theorems 1--2 it yields a concrete C1
same-input candidate for the NORMALIZED marked map on this shell.
It uses no new field-dependent state writer on this already supplied shell.
It does not construct the physical field writer for arbitrary fields.

The true primitive clock/price is not invariant under the label swap.
Let b' be the swapped port for SELECT!=0, and b'=b for SELECT0. The actual
old reporting charge is 1+b, not 1+b'. On a logical interface allowing
nonnegative retained conditional unit-tick padding, the exact table is

    padding=1+b'-b in {0,1,2},
    new actual charge=(1+b)+padding=2+b'.              (18)

For every complete m-round record the resulting counted charge is
`2m+sum b'`. Relative to a target ledger `n+sum b'`, the common difference
is `2m-n`, approximately `p^3 n`, and is PAID. At fixed integer n,m it has
zero field derivative, but it is not ignorable when choosing a programme
or varying the physical clock. Every actual controller/factory cost must
be included in addition. This packet verifies the table, not a new native
implementation of its arbitrary retained conditional controller.

Likewise, the complete forward-archive/cut map must be supplied before
turning the time-cell unitary into a physical clock identification. A
reversible mathematical label/time map is not an unpaid device. Pointer
Shannon entropy can have a count-dependent divergent timestamp term; C1
coherent-archive convergence alone does NOT establish its source limit.
No general Book Info or full Cost-Info equality follows from (15)--(18).

The completed replacement of the old conditional denominator/source premise
is therefore exact and useful, but scoped: it is the specified normalized
complementary feedback of the full128 first-shell archive. The common
nonvacuum full42/physical Book execution remains a different missing map.

## 8. Verification, rejected shortcuts and unchanged inputs

The executable checks use explicit `require`, so optimized Python does not
skip tests. They verify the rational noncommuting O(z) identity, reverse
normalizer costate, original128 field jet and count budgets at horizons
1,2,3,8,32, direct all16384 two-round histories, five-point independent
field differences, exact Golden port/cost algebra, complete ordered
noncommuting jump words, and finite first-shell formulas at L=4,...,128.
The C1/all-horizon assertions are analytic proofs, not extrapolations.

One development check incorrectly demanded a noncommuting normalizer already
at n=1. It failed, as it should: N_1 is a spectral function of the blank
operator. The final suite keeps n=1 as a COMMUTING control and verifies
actual noncommutation for n=2,3,8,32. The failure was a test-premise error,
not a removed scientific condition or a tolerance relaxation.

Negative controls retain the failure of replacing an operator count bound
by one scalar mean, of freezing the normalizer jet, of treating a physical
attenuation as polar normalization, and of inferring microscopic cost/Info
or physical metric scaling from the archive-time identity.

The exact new input substitution is the count-controlled positive normalizer
plus its explicit coherent archive/Book-source application. Existing native
operators and geometric roots are unchanged. No independent agent review,
new Lean compilation, whole-lattice test or GitHub CI pass is asserted.
Scientific pins and current-run receipts are in SOURCE_PINS.json and
VALIDATION.json. `GR_closed=false`.
