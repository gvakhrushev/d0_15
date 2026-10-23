# Original stopped RIGHT128 price: continuation value and preparation source

21 October 2026. Existing Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334),
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, constitutive /
`native-programme-v1`. Input `60b55b0cd5948b9e063a9cf1168953a9af750044`.
Phase: native realization / composition. Consumer:
[paid finite-return comparison](PRIMARY_CAR_PAID_RETURN_PRICE.md), §4,
and [parent](TWO_NATIVE_8D_DETERMINANT_SOURCE.md), §§11–15.

The previous decrease application was restricted to one round. Here the
original stopped experiment, including its abort and full oldRIGHT128,
has its own calculated cap2 source. A separate analytical theorem gives
a strictly positive continuation value at every finite cap. These are
different statements: increasing the value with cap does not determine
its derivative along a preparation orbit. No new physical Info, work,
task tolerance or Book normalization is selected.

## 1. Exact statement, input and conventions

Retain the original finite L4 completion, all256 sites, CAR16, RIGHT128,
the actual cost20 density, sigma=p³, REST positive adjoint and true
shifted weights. The flat-centre Kraus matrices K_alpha and the primary
preparation C_t are exactly those in the
[one-round posterior owner](PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE.md).
Write B=K_0=I-epsilon D²/2. Geometry and instrument remain frozen between
queries. The finite cap N is fixed in every derivative.

The complete first-nonblank cut consists of

```text
L_(j,alpha)=K_alpha B^j, 0<=j<N, alpha!=0,
L_abort=B^N.                                                (1)
```

No blank prefix, terminal time or abort is discarded. On the declared
classical-leaf/quantum-RIGHT algebra, set
G_omega=C_t* L_omega* L_omega C_t. Its physical RIGHT block is G_omega^T;
transposition changes neither traces nor spectra. Completeness gives
sum G_omega=I_128/128 on this primary family. The price component is

```text
A_N=H_phi(complete leaf_N|RIGHT)
   =-sum Tr G_omega log_phi G_omega-log_phi128.               (2)
```

This is the already proved matching complete-code Cost-minus-gain
identity on THIS cut. Coherent flag entropy is a different observable.
An actual outside-code W_N and all other baseline/factory charges remain.

For N=2 there are255 literal leaves:63 active first exits,63 active
second exits, one active abort and128 exactly dark Walsh leaves.
Paired ports leave65 distinct spectral problems. The pinned one-round
calculation supplies32 first-exit problems and its old blank. The new
calculation replaces that blank by33 actual second-stage problems.

## 2. A positive continuation value on the whole finite-cap family

The [original norm budget](PRIMARY_CAR_PAID_RETURN_PRICE.md), §1, gives
epsilon||D||²<1/6 on its nonempty small-primary chart. Hence

```text
B>(11/12)I,   beta=(11/12)^2=121/144>1/2.                    (3)
```

This section applies to ANY normalized conditional input and its actual
RIGHT prior sigma, not only a uniform prior. Its one-round blocks obey
G_0>=beta sigma and sum_(alpha!=0)G_alpha<= (1-beta)sigma.
In particular every G_alpha<=G_0; on supp(sigma), G_0 is faithful.
For Omega=direct_sum G_alpha, operator monotonicity of log, with zero
blocks obtained by regularization, gives

```text
H_phi(Y|R) >= Tr sigma(log sigma-log G_0)/ln phi
           = D_phi(sigma||G_0/q_0)-log_phi q_0
           >= -log_phi q_0,   q_0=Tr G_0.                  (4)
```

Both states in the relative entropy are normalized on the same support.
No physical measurement of that operator logarithm is assumed. This is
an algebraic conditional-entropy inequality. Log monotonicity follows
from its positive resolvent integral; the last inequality is the usual
nonnegative relative entropy already used by the matching-gain owner.
Operator dominance cannot be replaced by the survival probability alone:
a perfect RIGHT record of two equiprobable outcomes can instead have
H(Y|R)=0 and q_0=1/2, with domination beta_max=0.

Let s_j=||B^j C||_F², s_0=1. The exact conditional entropy chain for
first-nonblank caps gives

```text
A_(j+1)-A_j = s_j H_phi(next outcome|R,blank^j)
            >= s_j log_phi(s_j/s_(j+1))
            >= (s_j-s_(j+1))/ln phi.                       (5)
```

Thus A_N> A_(N-1) whenever DC!=0. Indeed B is invertible and commutes
with D, so DB^j C!=0 for every finite j. The original strict spectrum
also makes s_j-s_(j+1)>0. Conversely DC=0 gives only blank and A_N=0.
In particular A_N>=(1-s_N)/ln phi. The same all-blank term lower-bounds
the increment of a full fixed-length tape, but (5)'s equality is for
the stopped cuts (1).

The primary C has DC!=0, already witnessed by its active one-round
outcomes. Thus extra rounds have a real positive entropy price under
the matching-gain contract. On the restricted ordered family of caps,
if a genuinely supplied task specifies an abort tolerance and W_N is
nondecreasing, the earliest admissible cap minimizes A_N+W_N. Neither
the tolerance, this work monotonicity nor compulsory continuation is
derived here. The actual task must supply them.

## 3. Full preparation source, with the moving conditional prior retained

The original primary chart has D_t=D_0+O(t²),
C_t=C_0+t C_B+O(t²), with C_0 odd and C_B even in CAR parity.
The actual angle generator at w=(1,1,2,2) rotates grades14/15.
Its leading even vector is p e_(w,15) rr, where
rr_a=f_a(w)/sqrt128=F_integer(w,a)/128: f_a denotes the original
orthonormal Fourier column and F_integer its integer numerator. For any leaf
L in (1), put

```text
G_L=(L C_0)* (L C_0),
c_L=(L C_B)* (L e_(w,15)),
R_L=p(c_L rr^T+rr c_L^T).                                  (6)
```

Parity removes its constant jet. Once all active G_L are proved faithful,
analyticity gives d_angle G_L=t R_L+O(t³), and

```text
d_angle A_N=t a_N+O(t³),
a_N=-sum_L Tr(R_L log G_L)/ln phi.                         (7)
```

The +I entropy terms cancel over the COMPLETE tree because sum R_L=0.
They do not vanish separately in its reached second round. Original
Kraus parities and the exact Walsh structural zeros persist under B.

In particular let G_0=C_0*B²C_0 and
G_(0,alpha)=C_0*B K_alpha* K_alpha B C_0, including alpha=0
as the abort. Then sum G_(0,alpha)=G_0 and sum R_(0,alpha)=R_0.
The decisive cap2 increment is

```text
a_2-a_1=[Tr(R_0 log G_0)
          -sum_alpha Tr(R_(0,alpha) log G_(0,alpha))]/ln phi. (8)
```

The conditional RIGHT prior after blank is G_0^T/q_0. It is generally
moving and noncentral, not I/128. Equivalently,
A_2=A_1+q_0 H(next outcome|R,blank); differentiating this expression
retains BOTH the reach-probability derivative and that prior derivative.
Equation(8) includes them without normalizing/re-preparing the DATA state.

## 4. Actual calculation and finite-return consumer

The [new checker](check_primary_stopped_right_source.py) consumes the
pinned one-round interval report, removes its blank contribution, and
applies the entire original Julia/Walsh instrument to the actual
unnormalized amplitudes BC_0, BC_B, B e_(w,15). It retains full DATA
leakage; compression to the original prepared Fourier image would not
implement B. It separately certifies every new active128-dimensional
posterior, using the existing verified polar/log residual method with
no spectral cutoff and the same explicit binary64 arithmetic premise.

The saved [certificate](PRIMARY_STOPPED_RIGHT_CONDITIONAL_SOURCE_CERTIFICATE.json)
records a_2, a_2-a_1, the full pointer/posterior decomposition, actual
survival probabilities and all33 fresh support enclosures. Their strict
negative upper bounds give a_2<0 and a_2<a_1. This is a fixed-cap2,
fixed-L4 first-source result, not an inference from the value inequality
and not an all-cap, infinite-horizon or refinement theorem.

```text
a_2 in [-1.267648514875822e-6,-1.2676485137820654e-6],
a_2-a_1 in [-6.31721686553909e-7,-6.317216859530373e-7],
min new unnormalized posterior eigenvalue >1.8591133859830315e-13.
```

The new abort mass is in[0.9948965218101516,0.9948965218119936],
and its leading angle-source coefficient is strictly POSITIVE:
[8.844476767314231e-8,8.844476767331171e-8]. Thus on a nonempty small-t
chart the entropy-lowering positive-angle tangent increases the actual
abort probability. No new spectral work is needed for this scalar
source; it is the trace of the already retained abort jet.

For the same original cap2 execution at the supplied controller input,
constant outside-code work and no additional unaccounted factory terms
therefore give SOME actual finite signed Golden return lowering A_2+W.
The argument uses the open interval of strict decrease and the already
owned dense finite return angles; it introduces no continuous primitive
and asserts no uniform word bound. Every actual code/gain, controller,
address, work and task-admissibility term must still be included.

In particular a real task with abort tolerance delta must also check
s_2(angle_k)<=delta. An entropy improvement alone is insufficient.
If that constraint is active at the baseline, the local positive-angle
decreases just exhibited violate it. This does not exclude distant
returns or other directions; it identifies the actual competing source
that the task must test. It is not a fitted work penalty.
No tolerance or new stationary constraint is chosen to fit this family.

There is an already owned, narrower task boundary. The
[original stopped-clock owner](../../d0_native_minimality_closure_2026-10-20/prospective/STOPPED_CLOCK_SOURCE.md),
§§2,5, fixes the complete initial state and this instrument; its attained
port-cost theorem compares policies that only continue those rounds.
CAR preactuation is outside that policy class. Moreover the nonzero
abort source proves V_stop,2 U_angle changes the designated abort law
on this very primary input for sufficiently small positive angles in
that chart. It cannot be a channel-preserving substitute
for V_stop,2 with that retained abort label. A wider task admitting
controlled preparations may differ; no abort tolerance for that wider
class is supplied by the original theorem. This application neither
refutes its attained bound nor proves a prohibition on every CAR control.

## 5. Precise parent substitution and retained obligations

Parent §15's explicit one-round source restriction is now removed for
the original first-nonblank cap2 cut. The positive continuation theorem
also supplies an actual native lower-bound application for arbitrary
finite caps, rather than assuming a positive price per query. It is
the matched conditional-entropy component, not a letter-work charge.

Full native Book selection, outside-code incremental work, absolute
normalization, original preparation/controller admission and the
same-complete-initial-state field/programme graph remain open. The
current physical price need not choose this Info convention; the
source calculation does not select it. No GR/raw216, CORE, task
lifecycle or assembly acceptance is promoted. Write paths are this
proof/checker/certificate/review packet and append-only parent links.
The [review receipt](PRIMARY_STOPPED_RIGHT_CONDITIONAL_SOURCE_REVIEW.md)
records input provenance and the changed calculation's verification.
