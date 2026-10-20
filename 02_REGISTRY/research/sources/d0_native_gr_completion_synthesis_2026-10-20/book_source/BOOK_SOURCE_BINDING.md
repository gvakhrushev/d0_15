# Direct Book source on the complete native history: amplitude binding and a preparation-safe first-jet composition

20 October 2026. Existing PR #334 and
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`. Research theorem on the
original complete instrument. No replacement action, selected Info law,
new physical parameter or GR closure is asserted. `GR_closed=false`.

## 1. The exact owner interface, rather than an entropy substitution

The following are the actual definitions used here.

* Book01, “What mass/energy is allowed to mean before calibration”, defines
  `F_0(X)=|D_min(X)|`. This is a state code length. It does not identify the
  Book03 vertex gain with its difference along the native 128-outcome tape.
* Book03 §§03.3.0–03.3.0a defines
  `Z_D(k)=sum_gamma phi^(-S_gamma)[q_gamma]` in the memory algebra and
  `S_gamma=sum Cost - sum Info`. Its explanation of Info is a gain in
  distinguishability/lowering of uncertainty at a branch. It supplies no
  native128 prior/posterior, complete coherent-record information operator,
  or formula for its field/preparation first jet.
* Book03 §§03.8 and 03.10(c)–(e) puts the memory-valued sum BEFORE the
  quadratic response and its normalization. Section 03.10(f) also expressly
  distinguishes its geometry sum from the feedback partition. A positive
  scalar path weight, a vector amplitude and a squared amplitude cannot be
  interchanged at this interface.
* The existing retained-history normalizer and information-scale owners
  prove the scalar likelihood binding and its normalizer debt CONDITIONAL
  on `q=w/sum w`. The prospective finite-future owner supplies the exact
  scalar future law CONDITIONAL on its complete costs and task. Neither
  theorem identifies this scalar binding with the memory-algebra amplitude.
* The original paid-port owner supplies all 128 Kraus operators and their
  exact cost-marked map. No new instrument is needed below.

All these input files are pinned in `INPUTS.json`. The precise positive
result here is a translation from a full amplitude/record binding to its
first source, plus a sufficient **operator** source test that also controls
preparation. It is not a second Gibbs or Bellman proof.

## 2. Full coherent first jet, including moving preparation and all cross terms

Fix a finite, genuinely supplied complete history set at a fixed clock.
Work on the actual common Hilbert fibre after its admitted isometric
trivialization. Put `ell=log(phi)`. For every history let `S_gamma(y)` be
the supplied real net price and let `v_gamma(y)` be its actual represented
memory vector, including its retained record and oldRIGHT purification.
The latter may be `(M_gamma(y) tensor I) psi(y)`; its derivative then
includes both the operator and the preparation. For a moving positive
readout effect `E(y)`, define

    w_gamma = exp(-ell S_gamma),
    Q = sum_gamma w_gamma v_gamma,
    G^E_(gamma,delta) = <v_gamma,E v_delta>,
    N_E = <Q,E Q> = sum_(gamma,delta) w_gamma w_delta G^E_(gamma,delta).

All oldRIGHT/reference factors stay in these expressions. Faithful
memory representation and a physically admitted readout are hypotheses;
passing to an unfaithful quaternion compression is not allowed.

**Theorem 1 (direct first jet).** On any smooth chart where `N_E>0`,

    dN_E = sum_(gamma,delta) w_gamma w_delta
        [dG^E_(gamma,delta)
         -ell G^E_(gamma,delta)(dS_gamma+dS_delta)].              (1)

In particular, with

    pi_gamma^E = Re(sum_delta w_gamma w_delta G^E_(gamma,delta))/N_E,

one has `sum pi^E=1` and

    d[-log(N_E)/(2ell)]
      = sum_gamma pi_gamma^E dS_gamma
        -(sum_(gamma,delta) w_gamma w_delta dG^E_(gamma,delta))
          /(2ell N_E).                                         (2)

The `pi` need not be positive when distinct memory amplitudes interfere.
They are not a Gibbs probability distribution. The imaginary parts in
(1)–(2) cancel by Hermiticity. For the normalized actual response
`p_E=N_E/N_I`, subtract the corresponding two log sources. This includes
the derivative of the real denominator, rather than holding it fixed.

**Proof.** Differentiate the finite sum, use
`dw_gamma=-ell w_gamma dS_gamma`, and pair the two conjugate Gram terms.
No limit, entropy identification or assumption about commutativity is
used. The derivative of the Gram matrix contains the moving effect,
memory, state, reference and observer/fibre map. Formula (1), unlike an
individual log probability, is valid through dark individual outcomes
as long as these actual amplitude maps are smooth. The total positive
readout denominator is the only logarithm needed in (2).

Thus the first jet can be computed BEFORE an H+J+R expansion. This is a
useful route only once the physical net-price and memory map in (1) are
actually supplied; the formula does not select them.

## 3. Three different same-history bindings and the exact native test

Let `K_omega` be the product of the original full128 Kraus operators at
the true fixed clock `n`, and let

    V_n psi = sum_omega |omega> (K_omega tensor I) psi,
    q_omega = ||(K_omega tensor I) psi||^2,
    sum_omega q_omega = 1.                                    (3)

The complete history labels are orthogonal. All labels, including every
failure and both special blank ports, are present. On a fixed positive
support chart define `u_omega=(K_omega tensor I)psi/sqrt(q_omega)`.
The original branch phase is included in `u_omega`, not dropped.

### 3.1. Absolute amplitude binding

Suppose the Book vector on THIS complete record is

    Q_B = sum_omega phi^(-C_omega+I_omega) |omega> u_omega,        (4)

and its normalized full coherent state equals (3), including future
interference tests, with the indicated phase convention. Equality holds
if and only if, for one common real `J(y)`,

    phi^(-C_omega+I_omega) = phi^J sqrt(q_omega),
    I_omega = C_omega + (1/2)log_phi q_omega + J.                 (5)

The positive prefactor is then `phi^J`, and `||Q_B||^2=phi^(2J)`.

**Proof.** Project equality of the two normalized vectors onto every
orthogonal history summand. Its normalized nonzero state is the same
`u_omega`, so the scalar coefficients must agree. Conversely (5)
substitutes directly into (4). Matching only current probabilities would
not prove the relative branch phases; this theorem fixes them by the
actual native branch vectors.

With `H_phi(q)=-sum q log_phi q`, (5) gives the distinct exact identities

    E_q(C-I) = (1/2)H_phi(q)-J,
    E_q d(C-I) = -dJ,
    d E_q(C-I) = (1/2)dH_phi(q)-dJ,
    d[-log ||Q_B||^2/(2ell)] = -dJ.                             (6)

The second equality uses `sum dq=0`; the third also differentiates the
actual distribution. An expectation of a differential, a differential
of an expected price and a log-normalizer source are therefore different
objects. Choosing which one is the compulsory variational price is a
physical binding, not a consequence of notation.

### 3.2. Absolute scalar probability binding

For the ALREADY OWNED contract `q_omega=w_omega/N` with
`w_omega=phi^(-C_omega+I_omega)`, the corresponding identity is instead

    I_omega=C_omega+log_phi q_omega+log_phi N.                   (7)

There is no factor `1/2`. This is the exact existing scalar information
owner, not an error in that theorem. It is a different typed binding.

### 3.3. A further marker on an already executed native amplitude

If the Book factor is instead an EXTRA multiplier of the existing
`K_omega psi`, the vector is

    Q_mark = sum_omega phi^(-C_omega+I_omega)
                       |omega>(K_omega tensor I)psi.            (8)

To preserve the SAME normalized full coherent state in (3), its positive
factor must be common on every positive branch:

    I_omega=C_omega+J.                                        (9)

Otherwise (8) is a tilted analytical object, or a different physically
implemented filter if one is actually supplied. The native `K_omega`
already contains its Golden amplitudes. Applying a second cost weight
to it is not justified merely by calling both weights “Book”.

### 3.4. Decisive ORIGINAL full128 nonblank port calculation

For EVERY original nonblank `k`, the exact literal Kraus formulas give

    K_(0,k)=p L_k,  K_(1,k)=sqrt(p) L_k,
    p=phi^-1,  p+p^2=1,
    q(b|k)=(p^2,p),  C_port=(1,2).                             (10)

The normalized data and every later conditional future are identical for
the two ports at the same `k`. These are actual original operators; this
is not a replacement two-level instrument. For the port contribution
alone, the relative gains REQUIRED by the three bindings are

| Binding | Required `I_1-I_0` for the port ledger | Required net `S_1-S_0` |
|---|---:|---:|
| Absolute amplitude with normalized branch states, (5) | `3/2` | `-1/2` |
| Absolute scalar probability, (7) | `2` | `-1` |
| Additional factor on the actual native Kraus vector, (9) | `1` | `0` |

For example, inserting the scalar probabilities `(p^2,p)` as the absolute
amplitudes of (4) gives normalized probabilities

    (p^4,p^2)/(p^4+p^2)
       = ((5-sqrt(5))/10,(5+sqrt(5))/10),                       (11)

which are NOT `(p^2,p)`. This falsifies that particular identification
before a gravitational source is considered; it is not a no-go for D0.
The port-cost ledger here does not claim that every other work/gain
contribution to a complete history is the same in the two branches.

For comparison, the existing actual cost marker gives

    q_t(0|k)=p/(p+exp(-t)),
    q_t(1|k)=exp(-t)/(p+exp(-t)).                              (12)

At `t=log(phi)` it is `(1/2,1/2)`; at `t=2log(phi)` it is `(p,p^2)`.
Thus a probability cost mark and an extra amplitude cost factor are
experimentally distinct even on this original complete port pair.
This is an analytical diagnostic of a marker, not a new physical law.

## 4. Why a common normalization does not close the missing source

In (5) the full normalized state and all its future predictions determine
the relative gains but not `J`. Multiplication by `phi^J` changes the raw
source in (6). This observation is only a statement of the map's kernel;
it does not declare arbitrary field-dependent factors physically allowed.
The actual programme's gain/cut/work rule must fix that common factor.

This matters for the original closed-memory feedback. If a history
operator `F` is multiplied by a positive common factor `a(y)`, then

    d[-log det(I-z a F)]
      = Tr[(I-z aF)^(-1) z(a dF+F da)].                       (13)

The factor is a genuine loop/normalizer source at fixed native `z`.
Normalized open history probabilities do not remove it from repeated
closed cycles. Rescaling `z` to compensate would be another physical
identification requiring its own derivation.

The original paid-cost transform already gives the correctly typed
additional amplitude `exp(-t C_port/2)` and probability marker
`exp(-t C_port)` on every actual word. Formulae (8), (12) identify exactly
which of these objects a proposed Book map would have to consume.

Neither the state complexity `F_0` nor the threshold-only formal
`ActionProtocol` determines the choice among (5), (7), (9), its common
factor, or the derivative of the remaining full information gain. An
asserted `Info=delta F_0`, or `Info=Shannon`, would be an extra constitutive
identification until proved on this record. No such identification is
made here.

## 5. Positive composition theorem: a full price effect controls preparation as well as field source

The following theorem applies IF the actual Book price is the expected
sum of its supplied per-history Cost-minus-Info, together with the
remaining actual work/preparation price `W`. It does not select that
aggregation over the other readings distinguished in (6).

On the complete instrument put `s_omega=C_omega-I_omega` and

    G(y)=sum_omega s_omega(y) K_omega(y)^* K_omega(y),
    S_bar(y,rho)=Tr rho G(y)+W(y,rho).                         (14)

`G` acts on the full original data fibre and as identity on unchanged
oldRIGHT. All history labels remain stored; (14) reads their price and
does not erase them. If a genuine gain depends explicitly on preparation
or other internal variables, that dependence remains in `G` and its
derivative. An unproved linear-in-rho information law is not inferred.

The exact joint source is

    d S_bar = Tr rho dG + Tr (d rho) G + dW.                   (15)

**Theorem 2 (preparation-safe source criterion).** At an actual null
stratum `f_i=q_i=0`, suppose the whole priced programme satisfies

    G=g_0 I,
    dG+dW I = a_h d(sum_z fhat_z) I
               + b_h d(sum_z q_z) I                          (16)

on all required physical field directions, with `a_h != 0`. Here the
notation `dW I` is valid only when `W` is a scalar functional, and
`dg_0` is included in `dG`, never discarded. Suppose also that all other
actual internal variations have zero total source in (15).
Then (15) is exactly the all40 §5.1 source identity. If (16) holds uniformly
for the same class of preparations, this conclusion holds for every
normalized preparation in that class. In particular, when `G=G(y)` and
`W=W(y)` have NO additional explicit dependence on the input rho, its
entire constrained input-preparation Euler is already zero from
`G=g_0 I`; no frozen-preparation or Riesz-gap premise is needed for that
particular input-state variation. If `G(y,rho)` or `W(y,rho)` depends on
preparation, the extra terms `Tr rho D_rho G + D_rho W` must independently
vanish; scalar `G` does not remove them.

**Proof.** `Tr d rho=0`, so the second term of (15) vanishes when `G` is
scalar. Contract (16) with `rho`, whose trace is one. Conversely, scalar
`G` is necessary for the input-density derivative to vanish for EVERY
density at fixed instrument/price: traceless Hermitian variations span
the orthogonal complement of scalar matrices. This converse concerns
all input densities; the admitted fixed-oldRIGHT preparation subset may
require less, and no larger physical variation class is assumed.

Scalar `G` alone does NOT resolve moving apparatus, clock, code, observer,
or preparation-dependent information equations: their terms in `dG+dW`
must still satisfy (16) or the stated internal zero source. This is why
centrality of a single Choi mark cannot replace (16).

### 5.1. Exact marked/complement reduction and its unavoidable residual

For any actual complete marked event `M`, write its effect as
`E_M=sum_(omega in M) K_omega^*K_omega`. Decompose the TRUE prices as

    s_omega=s_c+delta_s 1_(omega in M)+xi_omega,
    R=sum_omega xi_omega K_omega^*K_omega.

Then EXACTLY

    G=s_c I+delta_s E_M+R.                                   (17)

Here `R` is fixed by the already supplied physical price table through
the displayed formula. It is NOT a freely adjustable remainder. Choosing
`R` or Info so as to enforce (16) would not prove the theorem's physical
hypothesis. On the given programme it is a computable Hermitian matrix
with a computable jet, and (16) is a nontrivial equality of those matrices
on all stated directions.

Suppose an actually constructed coherent CAR readout has at the target

    E_M=q_0 I,
    dE_M=kappa_f df I+kappa_q dq I                            (18)

on all ambient field directions. The complete price source is

    dS_bar=delta_s(kappa_f df+kappa_q dq)
       +ds_c+q_0 d(delta_s)
       +Tr rho dR+Tr(d rho)R+dW.                             (19)

There is no hidden self-information subtraction in (19). If the actual
code has two constant net prices, no residual, and only field-independent
common work at the chosen fixed programme, its source coefficient is
precisely `delta_s kappa_f`. For a real reference-interference amplitude
`u I+v A I` with `A=0,dA=df`, the marked effect has `kappa_f=2uv`.
The resulting coefficient is `2uv(s_mark-s_rest)`, fixed by the real
full net prices, not by assigning a desired Einstein coefficient.

All actual failure/work records contribute to `R` if their net prices
are not the common complement price. Equality of primitive gate counts
alone proves neither `dR=0` nor absence of an information source. Likewise
a field-independent nonzero common work price still matters when D_min
compares different clocks/programmes; it is not made free by a zero
fixed-programme first derivative.

The new coherent CAR construction can therefore be consumed by (19)
without expanding HJR: the remaining decisive calculation is the priced
effect `G`, including Info and every failure/controller/preparation term.
The observable mark derivative by itself is insufficient.

### 5.2. An executed algebraic source with the original Golden comparison port

The comparison construction used by the companion geometric-source lane
has a particularly direct price consumer. Its input is a supplied full
unitary `U` on logical data and ALL retained work, with clean-input
compression `T=i^* U i=t I`. It does not postselect a successful work
outcome. The original Golden comparison matrix is

    R_G=[[p,sqrt(p)],[sqrt(p),-p]],   R_G^2=I.

Apply `R_G`, controlled-U, then the SAME `R_G` to the initial control0.
The final port1 operator on the full work space is
`p sqrt(p)(I-U)`. Unitarity gives its complete logical effect

    E_1=p^3(2I-T-T^*)=2p^3(1-t)I,   E_0=I-E_1.               (20)

For the real scalar compression `t=-sigma A/2`, with `A=0,dA=df` at
the actual target, the two complete marginal effects therefore satisfy

    E_1=(2p^3+sigma p^3 A)I,
    dE_1=sigma p^3 df I.                                    (21)

If this final control is ACTUALLY reported by the original retained
direct0/return10 encoder, with its specified wire map `port0 -> 0`,
`port1 -> 10`, the price effect of THAT executed reporter component is

    G_port=1 E_0+2 E_1=(1+2p^3+sigma p^3 A)I,
    d E Cost_port=sigma p^3 df.                              (22)

Thus (22) is a concrete nonzero original-cost first variation once the
stated compression and encoder are implemented; no continuous price was
fitted to a geometric target. Its input-preparation term vanishes on
this scalar component. A new binary flag does not inherit cost1/2 merely
by being called a port: actual reuse of that encoder is the necessary
typing condition. Its implementation cost and all inner queries remain
in the same full programme.

What remains is exact and separate: the priced effect of those inner
queries, their work/archive and actual Info, including any explicit
preparation dependence, must complete (16). Equation (22) is not their
price and does not establish their stationarity. The `-1/2` net-price
gap in §3.4 concerns the original CONDITIONAL nonblank pair `(p^2,p)`;
it must not be transferred to the different outer comparison baseline
`(1-2p^3,2p^3)` in (20).

## 6. Actual application to the accepted exact GR family

The accepted common-null Brinkmann family has `f_i=q_i=0`. Its existing
all40 §5.1 theorem consumes precisely (16), with the true site weights
already absorbed into the operational coframe, site-independent derived
coefficients and all actual internal Euler resolved. If the native
coherent CAR amplitude realizes `A=0,dA=df` on this family, (19) supplies
an explicit finite source-composition route on the same family; it does
not need a global equality of actions or a high-mode HJR expansion.

After (16) is actually established, the owned Cartan/Poisson proof gives
the sourced finite Brinkmann solution with ratio `b_h/a_h`. Reusing the
LITERAL already configured midpoint solution requires its already fixed
ratio `lambda_-(2^-20)` as well. A different measured ratio determines
the corresponding solution family, not those identical configured
points. Physical prospective minimality and full programme admission
are not consequences of source equality alone.

There is a concrete diagnostic on the SAME family, not a new geometric
test. At its flat member with physical `v=h e`, original `U=I`, fullCAR16
and the fixed-oldRIGHT128 Riesz preparation, the common-carrier HJR owner
proves for every `L>=256` a strictly positive local coframe source

    D S_HJR[V_x] > 10^(-8),

where the accepted geometric source is zero. Thus, IF one insists on
the decomposition `S_full=S_HJR+E`, the actual remaining source must
satisfy `DE[V_x]=-DS_HJR[V_x]`. Neither `sum q=1` nor (1) forces that
identity. With a direct Book construction, the proper alternative is to
compute (1) or (15) for the ACTUAL complete price and check its zero
source there, rather than add a fitted counterterm to HJR.

This pins the missing choice exactly. Book03 supplies the weight form,
finite memory and quadratic readout; it does not yet supply the
same-process complete gain map and aggregate that turn them into (14)
or another uniquely specified full variational price. The new native
port calculation fixes a necessary translation test for that map, and
(16)–(19) give a positive, preparation-aware endpoint to prove. No claim
that this physical identification has already been discharged is made.

## 7. Small exact check and its scope

`check_book_source_binding.py` uses exact arithmetic in Q(sqrt(5)) and
rational jets. It checks the original port Kraus ratios, all three
relative-gain translations, the wrong squared-probability law, both
true cost-marker cuts, the common-normalizer/source identity on the
original Golden pair, and the moving complete-price product rule and
preparation term on that same two-port class. It is a targeted check of
the translation and composition algebra. It does not re-enumerate the
old 128 matrices, prove primitive admission, assign physical Info, or
replay any historical suite.
