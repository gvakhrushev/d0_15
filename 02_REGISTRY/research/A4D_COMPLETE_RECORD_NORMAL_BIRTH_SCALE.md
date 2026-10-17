# The full coherent record has a derived h^2 log(1/h) birth term

17 October 2026. Same Draft #334, input `090c957fddde61946da03cac7d1e658a6197f4e5`.
Consumer: the real h^2 history signal survives continuum cone blindness,
but its complete information price must be computed before identifying
that scale with an Einstein action. This owner computes a genuine full
coherent-entropy contribution, retaining all8 shell momenta, full16 forms,
reference128 and actual preparation/field correctors. It does not replace
entropy by a selected event probability or choose a physical Info law.

**Result.** A weighted second-order output-state expansion of the same
native rounds gives a positive Schur birth operator B. Its trace b produces
`+2 b h^2 log(1/h)` in complete coherent entropy. Six actual rare outputs
give a strictly positive lower bound on b for every nonconstant owned LC
cone, even with arbitrary normalized preparation and field first correctors.
A fixed finite per-round code has no cancelling logarithm. The existing
fixed-beta H+J+R price is not silently redefined to contain this entropy.

## 1. Actual normalized preparation, clock and smooth stencil expansion

Use the [variable process](A4D_VARIABLE_RECORD_CHANNEL_CONSERVATIVITY.md),
[whole-grid calculus](A4D_VARIABLE_RECORD_ENTROPY_AND_CODE_LIMIT.md) and
[integer-moment/source estimates](A4D_VARIABLE_RECORD_FIRST_SOURCE_LIMIT.md).
The native round is exactly Phi_h=Id+epsilon_h L_h, epsilon_h=c h^2,
c=p^2/64. Every actual 127 nonblank output is retained. The 64-row GKSL
identity is only a marginal identity, not a change of record basis.

Work on a bounded smooth positive-adjoint chart with strict Julia margins,
proper links and their controlled smooth remainders. For this higher-order
claim, actual fields have smooth h-jets through order2 with bounded order3
remainders. Because D_h divides a transported difference by h, its exterior
link additionally must satisfy
`(Lambda(M_h)-I)/h=R0+h R1+h^2 R2+O(h^3)` with controlled spatial
derivatives: links through order h^3 with O(h^4) remainder. Exact proper
path transport of a connection with those field jets supplies this.
An unspecified O(h^2), or even O(h^3), link remainder alone would not
suffice. In the common true observer/density trivialization let
the actual normalized amplitude have

```text
C_h=C0+h C1+h^2 C2+O_H24(h^3),  ||C_h||HS=1.             (1)
```

All 128 columns and all grades of C1,C2 vary. Use a fixed sufficiently
smooth controlled chart; the H24 condition is a sufficient analytic
regularity assumption, not a derived physical preparation law. Include
all coframe/link/observer/measure first and second correctors in the
actual stencil coefficients. Nothing freezes them by taking a trace.

Taylor expansion of the true shifted stencil and the local positive
Julia roots gives, on the sampled/embedded weighted trace classes,

```text
L_h=L0+h L1+h^2 L2+R_h,
||R_h X||_(1,r)<=C h^3 ||X||_(1,r+8),
L0:S1,r+2 -> S1,r, L1:S1,r+4 -> S1,r,
L2:S1,r+6 -> S1,r.                                     (2)
```

These safe losses include all anticommutators, not just recycling.
To justify (2), D_h has Taylor coefficients of differential orders1,2,3
and a remainder h^3 of order4. Each N_k,h has orders0,1,2 and remainder
h^3 of order3, so J_k,h=N_k,h*D_h has orders1,2,3 and remainder of
order4. The order-h^3 remainder of the full generator has at most
order5 on either side; the stated loss8 suffices. Proper shifted
P_h P_h* and P_h* P_h are multiplication operators, including their
shifted coefficients; their Julia square roots have uniformly positive
arguments and ordinary local Taylor remainders. No unproved norm-small
expansion of a global differential square root is used.

The scalar bound for the shift remainder holds for every frequency,
including |h k| near pi. The periodic Fourier calculus of the input
owner controls coefficient sampling/alias tails. Applied to the smooth
states below, their arbitrarily chosen finite-order tail bound is at
least O(h^3) in the same norm. This is a common-grid consistency statement
with Fourier projections, not an operator-norm Taylor expansion on L2
without a Sobolev loss or an omission of Nyquist modes.

## 2. Weighted output expansion by a one-step residual

On data times reference128 let X_i be the coefficients of the ACTUAL
initial pure density from (1):

```text
X0=|C0><C0|,
X1=|C1><C0|+|C0><C1|,
X2=|C2><C0|+|C0><C2|+|C1><C1|.                         (3)
```

Vectorization of amplitudes is understood. Normalization implies
Tr X0=1 and Tr X1=Tr X2=0. Solve the inhomogeneous equations using the
already owned conservative continuum semigroup and its weighted bounds:

```text
dot sigma0=L0 sigma0,                         sigma0(0)=X0,
dot sigma1=L0 sigma1+L1 sigma0,                sigma1(0)=X1,
dot sigma2=L0 sigma2+L1 sigma1+L2 sigma0
                         -(c/2)L0^2 sigma0,  sigma2(0)=X2.       (4)
```

The last term is the real Euler/record-clock correction. An exponential
continuum process with the same L_h would miss it. Let
a_h(t)=sigma0(t)+h sigma1(t)+h^2 sigma2(t). The weighted Duhamel bounds
give sigma0 in S1,24, sigma1 in S1,20 and sigma2 in S1,16 uniformly
on compact times. The required time derivatives also exist in lower
weighted spaces by (2); even the safe loss12 is within this budget.

Insert the sampled a_h into one EXACT native step. Taylor sigma0 through
epsilon_h^2, h sigma1 through epsilon_h and h^2 sigma2 through epsilon_h.
The `-(c/2)h^2 L0^2 sigma0` term in a'_h cancels
`epsilon_h^2 L0^2 sigma0/2` from time Taylor. The remaining one-step
residual in S1,1 is at most C epsilon_h h^3; terms epsilon_h^3 and
h epsilon_h^2 obey that bound. The actual Phi_h powers are bounded on
S1,1 by the corrected-moment estimate. Telescoping n steps, together
with (1) and the controlled Fourier projection errors, therefore proves

```text
||sigma_h,n-[sigma0(T_h)+h sigma1(T_h)+h^2 sigma2(T_h)]||_(1,1)
                                                       <=C h^3,
T_h=n_h epsilon_h.                                      (5)
```

Use this MATCHED actual time. Ordinary rounding T_h-T=O(h^2) only changes
the regular leading time coefficient; no derivative of integer n is
invented. A different actual clock law must supply its additional jets.
The proof uses a residual and CP moment propagation, not a strong
derivative of the growing tape or of an unbounded semigroup generator.

## 3. The true birth coefficient is a Schur complement

Now specialize the LEADING fields to the owned exact-LC cone
e=s O01(theta(y)), n=e0, s>1, G=s^2 I on the period-2pi torus with
fixed normalized coordinate measure. The initial leading amplitude is
the existing full faithful shell C0=P_Sigma/sqrt(128): eight first momenta,
16 forms and the same128 reference labels. It is not a theorem about an
arbitrary unknown global spatial optimum or all possible preparation ranks.

The [complete-channel support theorem](A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md)
shows that sigma0(T) is positive on

```text
P=vec(directsum_(k in first8) M16), dim P=2048,
Q=I-P.
```

For T in a compact positive interval its smallest eigenvalue on P has
a positive lower bound. In coordinate forms the leading process and P
are theta-independent by the
[labelwise factorization](A4D_SPATIAL_PREPARATION_VARIATIONAL_LIMIT.md#8-decisive-geometric-consumer-preparation-cannot-restore-an-invisible-cone).
At each matched T_h define

```text
U=Q sigma1 P,
V=Q sigma2 Q,
B=V-U(sigma0|P)^(-1)U*,   b=Tr B.                       (6)
```

The leading jump/no-jump operators reduce P and Q. The initial (3) has
Q X1 Q=0, and Q L1(sigma0)Q=0: each first-order recycling cross term has
one leading side in P, and the anticommutators also have a base side
there. Equation (4) therefore gives Q sigma1 Q=0. Positivity alone on
the one-sided mesh sequence would not prove this. The exact Schur
complement on Q, divided by h^2, converges in S1,1 to B with O(h) error
by (5); hence B>=0. Using V alone would count a coherent rotation of the
old support as new entropy. The subtraction in (6) is essential.

The full b depends only on FIRST operator/output/preparation jets. In
the projected equation (4),
`Q L2(sigma0)Q=sum_k Q J_k,1 sigma0 J_k,1* Q`:
the J_k,2 cross terms and Delta2 anticommutators have a leading side
in P. Also Q L0^2(sigma0)Q=0 and Q X2 Q=Q|C1><C1|Q.
The remaining Q L1(sigma1)Q and U use only first jets. Thus direct
second field/preparation jets and the Euler correction affect regular
terms, but cannot change b. They are retained in (4),(5) because the
full output expansion and regular second price still require them.

Equivalently, if A0 is a limiting path purification with right Schmidt
support R and a suitable first normal jet A1 exists, then
B=(Q A1(I-R))(Q A1(I-R))*. This is an explanation, not a required full
strong tape-jet theorem. The Bernoulli-to-waiting-time embedding has
collision/boundary layers of order h; a global h-derivative is not assumed.

There is also a definition using only the TRUE finite tape. Let P_h^high
be the spectral projection of sigma_h onto its 2048 eigenvalues separated
from0. Then

```text
b=lim h^-2 ||[(I-P_h^high) tensor I_record]Psi_h||^2.      (7)
```

This is independent of an environment embedding or Kraus recombination.
All reference and preparation directions remain in the formula.

## 4. Entropy extraction and its precise source topology

The separated high-eigenvalue cluster permits its usual contour projection
and near-identity unitary block rotation. These are analytical tools, not
new physical operations. Equation (5) holds with fixed energy weights;
the corresponding projection/rotation is bounded on H1 and differs from
identity there by O(h). This follows by the resolvent Neumann formula
around sigma0 on that contour, since the weighted perturbation is O(h).

The actual small block after rotation is h^2 B_h with
B_h=B+O_S1,1(h) and B_h>=0. Its trace and first energy are uniformly
bounded. The same energy/entropy estimate as in the input owners bounds
the entropy of this unnormalized positive block uniformly, including
b=0. Thus its entropy is

```text
2 h^2 log(1/h) Tr B_h+h^2 S(B_h)
                       =2 b h^2 log(1/h)+O(h^2).
```

The finite-dimensional high block is regular. Consequently the entropy
of the complete coherent record, by Schmidt equality, is

```text
S(sigma_h)=S(sigma0(T_h))
 -h Tr[P sigma1 P(log sigma0+I)]
 +2 b(T_h)h^2 log(1/h)+O(h^2).                           (8)
```

No spectral floor is imposed on the newborn states. Only the already
proved finite positive leading support is inverted.

For uniformly controlled smooth parameter families the value expansion
is locally uniform. Therefore the normalized second-order correction
has distributional parameter source 2 db: integrate against a compact
smooth parameter test and integrate by parts. This is a proved weak
source statement. We do NOT infer pointwise C1 convergence of an O(h^2)
remainder or claim the original rough raw h^-2 source norm. A stronger
pointwise source theorem would require its own logarithmic-jet control.

## 5. Six actual rare outputs give a preparation-independent lower bound

Use the THREE existing nonconstant role-Walsh characters, coefficient0,
and BOTH original golden ports. Each has N_kappa,0 identically0 for every
continuum coframe because P_r=C_r at h=0. Its first row is

```text
N_kappa,h=h D_chi/16+O(h^2),
ell_(kappa,0),h= -p h D_chi D0/16+O(h^2),
ell_(kappa,1),h= -sqrt(p) h D_chi D0/16+O(h^2).           (9)
```

The physical Kraus maps are sqrt(epsilon_h) times these. Their squared
port weights sum to p^2+p=1. D_chi contains a constant-coefficient kinetic
part and the actual potential J_chi/s. The nonzero spatial Fourier
components of the latter change data momentum while reference momentum
is retained, so their output lies in Q. Their record label has zero
leading amplitude, not just a small selected probability.

Let R_h be the sum of the six actual rare CP maps, and F_h=Phi_h-R_h,
also CP. The exact event 'at least one of these marks anywhere' has map

```text
E_h=sum_(j<n) Phi_h^(n-1-j) R_h F_h^j.                  (10)
```

It is an actual sector of the complete retained history. The corresponding
count map replaces F_h^j by Phi_h^j. Their CP difference counts additional
marks on histories with at least two. A rare map is epsilon_h h^2 times
a uniformly order2 jump squared; explicitly its weighted effect obeys
`R_h*(G^r)<=C epsilon_h h^2 G^(r+2)` as a positive form in the fixed
trivialization (and the corresponding grid energy). Two insertions and the fourth-moment bound
give total trace error O(n^2 epsilon_h^2 h^4)=O(h^4). Thus the scaled
event, not just its expected count, converges to the leading past/rare/future
integral from (9). Smooth weighted consistency proves this by the same
finite-time Duhamel/Riemann argument; no repeated old root calculation is used.

All leading ordinary jumps preserve data momentum and the reference label,
so P and Q reduce them. Their conservative future evolution preserves Q
mass; this removes future factors only AFTER summing actual histories,
not by erasing a record. The reduced leading data state is the stationary
P_Sigma/128. Fourier orthogonality and (9) consequently give

```text
lim h^-2 Tr Q E_h(|C_h><C_h|)
 =T/(4096 s^4) sum_(three chi)
                <Tr16 |J_chi-<J_chi>|^2>.              (11)
```

The moving high projection differs from P by O(h); event mass is O(h^2),
so replacing Q by I-P_h^high changes (11) only by O(h). Positivity of
the complementary history sector and (7) show b is at least (11).

This bound is immune to ANY normalized C1: its leading amplitude in
these labels is zero, so the prep correction contributes one further h.
The same is true of all h-order coframe/link/observer/measure correctors:
N_kappa,0 is identically zero throughout the continuum chart. They may
change OTHER normal terms or the regular source, but cannot cancel this
positive complete-history contribution. C2 cannot enter it either.

## 6. Full16 value and the original winding family

For the actual cone connection of the causal/source owner set

```text
A=c0 c1 i2 + (c0 c1 i2)*,
Bword=c0 c2 i1 + (c0 c2 i1)*,
Cword=c1 c2 i0 + (c1 c2 i0)*,
J0=theta'(Bword-cos(2theta)A),
J1=theta'(cos(2theta)A-Cword),
J2=theta'(Cword-Bword), J3=0.                            (12)
```

Here c_r are the original full16 creators and i_r their true adjoints;
Bword is not the positive birth operator B of (6). Full CAR gives
Tr A^2=Tr Bword^2=Tr Cword^2=4 and zero pairwise trace products.
The three Walsh potentials are -2J2,-2J1,2J0 in literal label order.
For periodic O01(theta), including winding lifts, <theta'cos(2theta)>=0.
Therefore (11) gives the full lower bound

```text
b >= T/(128 s^4)
        [2 Var(theta')+<theta'^2 cos^2(2theta)>].          (13)
```

It is strictly positive for every nonconstant such coframe. Indeed zero
would force theta' constant and theta'cos(2theta)=0 identically, hence
theta'=0. On the original winding theta=y, the single ++-- potential
is constant, but the other two are not: their squared variances are
0,8,8. Thus

```text
b >= T/(256 s^4)>0,  theta=y.                            (14)
```

This closes the winding exception left by a single selected character.
The bounded helper checks the actual CAR, proper-connection words and
literal duplicated-Walsh normalization, not a spectrum or rank census.
The full b may exceed this lower bound because other actual outputs
also contribute. Equation (13) is not its exact EH coefficient.

## 7. Consequence for the same code/coherent price and the route

Any fixed finite per-round code effect has a regular stencil expansion
A_c,h=A0+h A1+h^2 A2+O(h^3) with the same weighted losses. Combining it
with (5), its actual expectation has a power expansion

```text
Cost_h=n g0+q0(T_h)+h q1(T_h)+h^2 q2(T_h)+O(h^3).
```

The q2 term includes the left-Riemann correction
c[Tr A0 sigma0(0)-Tr A0 sigma0(T_h)]/2 as well as (4) and all real
operator/preparation jets. There is no logarithm. The divergent actual
blank baseline n g0 is displayed, not silently subtracted from a
physical action. Fixed signed relative code weights also satisfy this
power-expansion statement; their positivity is not needed here.

Consequently the declared coherent candidate Cost_h-eta S(sigma_h),
eta!=0 fixed, contains

```text
-2 eta b h^2 log(1/h).                                  (15)
```

A fixed finite code cannot cancel it. This is the FULL coherent entropy,
not the Shannon entropy or surprisal of one event. For canonical sampling
C_h=C0 with zero h-order field correctors, constant theta has b=0 because
every finite-h output stays in P. Any nonconstant cone has b>0 by (13).
Thus b is not merely a field-independent baseline. Locally uniform
expansion and the weak parameter-source argument after (8) rule out a
uniformly finite log-free h^-2 source on this whole declared family
without a separately proved cancellation. We do not assert a pointwise
source divergence at every parameter or every choice of correctors.

The preceding unscaled continuum result remains valid: its entropy/source
is cone-blind. At the next scale the same coherent candidate is not an
ordinary analytic h^2 coefficient; its real Schmidt births matter. A
physical logarithmic code, normalizer, different Info contract or scale
could alter the conclusion, but must follow from the same native law.
No such term is added here and no Einstein residual is renamed as stress.

The [complete-history binding/source theorem](A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md)
types the distinct pointer-likelihood alternative, where code cancels
and the dominant logarithmic clock source is derived. These two theorems
specify what the physical history/test/cut morphism must choose between.
They do not select it, prove a different-rank leading preparation,
primitive admission, a joint curved root or the original all-ten raw
h^-2/#216 refinement terminal. All those obligations remain OPEN.
