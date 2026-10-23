# Whole-lattice energy control → coherent entropy and actual code limits

17 October 2026. Same Draft #334, input `23c82df4`. Consumer: the
[full variable-field record process](A4D_VARIABLE_RECORD_CHANNEL_CONSERVATIVITY.md)
now has its actual finite-h trajectory limit. This owner proves the
uniform integrability needed to pass from that state limit to coherent
entropy and known code/count observables. It retains the actual full
spatial carrier, all 16 forms, reference 128, density, observer and
proper-link jets. It does not identify a physical Info, change the
operator/action, or choose an ensemble or clock law.

**Result.** On the same uniformly smooth compact chart, the native
finite-grid channels have uniform first- and second-moment Lyapunov
operators, comparable to I+Delta_h and (I+Delta_h)^2. Uniform initial
first energy implies convergence of output entropy, hence complete
coherent-record entropy for the actual purified preparation. Uniform
initial second moment additionally gives the continuum limits of the
actual total exit count, original port-code excess, and any supplied
fixed per-round code. These are value/expectation theorems. They do not
assert convergence of field derivatives or of pointer entropy.

## 1. Objects, assumptions and the exact global recycling identity

Use H_h on the entire L^4 torus and its exact Fourier isometry E_h
into H=L2(T4;C16), with reference I128. Coefficients are smooth on a
compact family, with uniform bounds on every derivative used below;
U=(u_ra) is real, s_min(U)>=sigma>0 and |u_r|<=nu_max<1. Proper links
are I+h Omega_r+O(h^2) with controlled smooth remainders, in the actual
observer/density trivialization. No LC condition, stationary equation,
matter freezing or admitted-tangent replacement is imposed. Constants
may depend on finitely many smooth seminorms but not h or L.

The existing channel is exactly Phi_h=Id+epsilon_h L_h,
epsilon_h=p^2 h^2/64, p+p^2=1, Delta_h=D_h^2. The true shifted adjoints
and all link/observer/density terms belong to D_h. The paired **global**
Julia formula in the [complete-channel owner](A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md),
Section 1, is stronger than a pointwise matrix identity. For each P_r
and C_r pair, replace P* X P+P X P* analytically by two Hermitian Kraus
operators

```text
B_+=(P+P*)/sqrt(32), B_-=i(P-P*)/sqrt(32),
B_L=sqrt(I-PP*)/4, B_R=sqrt(I-P*P)/4,
```

and likewise for C. All factors include the original 1/16 weight.
These are fixed linear combinations of global operators, including
shifts; they are not spatially varying rotations of a physical record.
Consequently, exactly on the full grid,

```text
T_h(X)=sum_a B_a,h X B_a,h,
B_a,h*=B_a,h, sum_a B_a,h^2=I,
T_h(X)-X=(1/2)sum_a[B_a,h,[X,B_a,h]].                    (1)
```

In particular (1) retains all derivative and finite-frequency terms.
A pointwise Kraus recombination alone would not justify it. The physical
128-output tape, its measurements and its price are unchanged.

## 2. A uniform finite-grid calculus, including aliasing

Let theta in T4 be the dimensionless Fourier variable, theta_k=2pi h k
on the half-open Brillouin cube. Put

```text
rho(theta)^2=sum_r |exp(i theta_r)-1|^2,
w_h(theta)=(1+rho(theta)^2/h^2)^(1/2).
```

Use left quantization on the finite cyclic grid. An order-m family
satisfies, for every required multiindex,

```text
|h^|beta| partial_theta^beta partial_x^alpha a_h(x,theta)|
       <=C_alpha,beta w_h(theta)^(m-|beta|).             (2)
```

This is a definition with uniform constants, not an appeal to a
continuum quantization on a truncated grid. Finite Fourier convolution
is exact:

```text
(a #_h b)(x,theta)=sum_n exp(2pi i n.x)
                         a(x,theta+2pi h n) b_hat_grid(n,theta).
```

Here n ranges over the canonical finite Fourier representatives and
frequency addition is modulo L. The identity for exp(i theta)-1 gives
w_h(theta+2pi h n)<=C<n>w_h(theta), and the reverse inequality follows
by replacing n by -n. Smooth x-Fourier coefficients have arbitrarily
many uniformly summable moments. Sampling does not lose this property:

```text
sum_n <n>^q |b_hat_grid(n,theta)|
 <=sum_m <m>^q |b_hat_cont(m,theta)|.
```

Taylor expansion of a in its periodic theta variable therefore gives
r composition terms and a remainder of order ma+mb-r, uniformly in h.
Derivatives in the first exact Taylor sum are those of the trigonometric
interpolant. Replacing them by sampled smooth derivatives produces
alias tails with factors ((n+Lz)^beta-n^beta). Smooth Fourier decay
bounds these by O(h^R) of the corresponding order for arbitrary fixed
R; choose R at least the required lost order. Since h^R<=C w_h^(-R)
on the whole cube, they belong to the same stated remainder class.
Thus sampled-derivative Taylor formulas hold modulo this controlled
remainder, not as exact identities.

The same convolution estimate and the weight comparison imply

```text
Op_h(S_h^m): H_h^s -> H_h^(s-m) uniformly,                (3)
||u||H_h^s^2=sum_k w_h(theta_k)^(2s)|u_hat(k)|^2.
```

For example, an order-2 symmetric remainder has absolute form bounded
by C||u||H_h^1^2. A fixed sufficiently large Fourier moment proves (3)
by the Schur/Young convolution estimate; no rank or spectral census is
involved. Adjoints and symmetrized symbols have the same calculus.
Formal Weyl principal/subprincipal symbols can be obtained from this
left/adjoint expansion modulo the stated lower orders; there is no
need to divide by 2 on an even cyclic grid.

Uniform ellipticity also gives ||u||H_h^2<=C||(I+Delta_h)u||. For
completeness, invert the scalar principal symbol outside rho<=O(h),
using (2); the resulting order -2 parametrix leaves an order -1 error.
The low-frequency part is uniformly bounded. This gives
||u||H_h^2<=C(||(I+Delta_h)u||+||u||H_h^1). Interpolation absorbs the
last term, and I+Delta_h>=I controls the remaining L2 norm. Combined
with the existing whole-grid Gårding estimate, both first and second
energy forms are uniformly equivalent to these Sobolev norms.

## 3. The actual cubic defect is internally traceless at every frequency

The principal finite-difference symbol is

```text
P(x,theta)=sum_r[c(u_r)(exp(i theta_r)-1)
                       +c(u_r)* (exp(-i theta_r)-1)],
P*=P, P^2=lambda I,
lambda=|sum_r u_r(exp(i theta_r)-1)|^2>=sigma^2 rho^2.
```

The actual operators have formal Weyl expansions
D_h=P/h+order0 and Delta_h=lambda I/h^2+A/h+order0.
The Hermitian subprincipal A is O(rho): the product contains P times
the true lower-order connection and the Poisson term of P; both vanish
at theta=0. Proper links, moving observer and density occur in A and
the bounded remainders, rather than being set to zero.

Write b_a for the principal Hermitian symbol of B_a,h in (1).
The frozen internal recycling map sum b_a X b_a is exactly T_x from
the previous owner, independent of theta: the paired forward/inverse
phases cancel, and both Julia defects remain. Its full CAR traceless
norm is at most 1-delta, delta=sigma^2/8. This gap applies only to the
internal 16-component matrix algebra.

Equation (1) gives the leading defect directly. With the convention
a#b=ab+h{a,b}/(2i)+lower orders,

```text
T_h(Delta_h)-Delta_h=q1/h+order0,
q1=(1/2)sum_a[b_a,[A,b_a]+{lambda,b_a}/i].                (4)
```

Every summand is a matrix commutator, so Tr16 q1=0. It is Hermitian
and O(rho), with the corresponding differentiated symbol bounds.
Because D_h commutes Delta_h exactly,

```text
L_h*(Delta_h)=D_h[T_h(Delta_h)-Delta_h]D_h
             =F/h^3+order2, F=P q1 P, Tr16 F=0.         (5)
```

The trace follows from P^2=lambda I; F=O(rho^3). The previously
exhibited proper-boost cubic defect need not vanish, so no bare-energy
estimate is substituted for (5).

## 4. Periodic correctors control the whole lattice, not only low modes

For rho!=0 set W=P/sqrt(lambda) and
M(b)=P T_x(b)P-lambda b. On traceless Hermitian matrices its inverse
has norm at most 1/(delta lambda). Define b=-M^(-1)F. Equivalently,

```text
b=(I-Ad_W T_x)^(-1) Ad_W(q1).
```

The contraction gap gives b=O(rho) and
partial_theta^alpha partial_x^beta b=O(rho^(1-|alpha|)).
Let chi be zero for rho<=h and one for rho>=2h, with a smooth transition.
It is periodic because rho^2 is periodic; choose the cutoff as a smooth
function of rho^2/h^2. Symmetrize left quantization to define

```text
C_1,h=Sym Op_h[chi b/h].
```

This is uniformly order 1 in (2). Composition from Section 2 gives
L_h*C_1,h=-chi F/h^3+order2. The omitted (1-chi)F/h^3 is uniformly
order 0: F vanishes to order 3 and its support has rho<=2h. Thus
L_h*(Delta_h+C_1,h) is uniformly order 2.

The same construction gives the second moment without a new search.
Let Lambda_h=I+Delta_h. Since it commutes D_h, its square has principal
lambda^2/h^4 and subprincipal 2lambda A/h^3. Formula (4) therefore
has q2=2lambda q1, F2=2lambda F and cell corrector b2=2lambda b.
Set C_2,h=Sym Op_h[chi b2/h^3], uniformly order 3. Its correction
cancels the complete order-5 symbol of L_h*(Lambda_h^2). The remainder
is order 4, including the low-frequency region.

Order-1 and order-3 symmetric forms are arbitrarily small relative to
the respective principal positive energy forms, with a sufficiently
large L2 constant. This follows from (3), interpolation and the
elliptic estimates in Section 2. Therefore choose fixed a_s so that

```text
H_1,h=2(Delta_h+C_1,h)+a_1 I >= I+Delta_h,
H_2,h=2(Lambda_h^2+C_2,h)+a_2 I >= Lambda_h^2,
H_s,h<=C_s Lambda_h^s,
L_h*H_s,h<=C_s H_s,h, s=1,2.                            (6)
```

All constants are independent of h. Theta is periodic, with lambda
vanishing only at its origin; no Nyquist direction is omitted. H_s,h
are analytic Lyapunov operators only. They replace no Delta, action,
observable, state, physical source or preparation law.

For positive normalized rho_h,j the exact Euler identity now gives

```text
Tr H_s,h rho_h,j <=(1+C_s epsilon_h)^j Tr H_s,h rho_h,0.
```

Consequently, at every bounded record time T,

```text
sup_(j epsilon_h<=T) Tr Lambda_h^s rho_h,j
                  <=C_T Tr Lambda_h^s rho_h,0.           (7)
```

The first moment gives entropy tightness; it does not itself assert
uniform integrability of energy. The second moment supplies the
Rayleigh/code integrability used below. These follow from actual
discrete estimates rather than assumptions about the outputs. Tensoring I128
keeps all reference correlations and only finite multiplicities.

## 5. Full spatial coherent entropy converges under first initial energy

Suppose the actual embedded preparations converge in trace norm and
sup_h Tr Lambda_h rho_h,0<infinity. The previous trajectory theorem
and (7) give converging output states with a common bound on

```text
G=(I-sum_r partial_r^2) tensor I_(16*128).
```

Indeed |2pi k|<=C rho(theta_k)/h on the entire cube, and the whole-grid
Gårding inequality controls this fixed Fourier energy. The limiting
state has the same energy bound by lower semicontinuity.

G has counting bound N_G(E)<=C E^2 and finite partition function for
every positive inverse temperature. Its maximum entropy at mean energy
E is at most C+2log(1+E), by the Gibbs variational bound. Apply
[Winter, Tight uniform continuity bounds for quantum entropies,
Lemma 11](https://arxiv.org/html/1507.07775v2): if delta_h is half the
output trace distance and both energies are <=E, then

```text
|S(rho_h(T))-S(rho(T))|
 <=2 delta_h F_G(E/delta_h)+h2(delta_h) ->0.               (8)
```

The prior continuity theorem is used with its actual energy hypotheses;
(7), not the continuity theorem, proves them for this native process.
For pure normalized system/reference preparations, every fresh record
round is an isometry and old records are retained. Schmidt equality
identifies the complete coherent-record entropy with this final
system/reference entropy, so (8) proves its full spatial value limit.
No 2048-dimensional Choi compression is extrapolated to a growing grid.
For mixed inputs (8) is a system/reference entropy theorem; an additional
unrepresented purifier is not silently supplied.

## 6. Actual counts and any supplied per-round code converge under second energy

If sup_h Tr Lambda_h^2 rho_h,0<infinity, (7) controls the second output
moment. The original total-exit effect is exactly

```text
E_exit,h=epsilon_h Delta_h-(epsilon_h^2/4)Delta_h^2.
```

Bounded spectral cutoffs of Delta_h converge under the owned embedded
resolvent theorem. The second moment bounds the Rayleigh tail by C/R.
Together with trace-norm trajectory convergence this proves
Tr Delta_h rho_h(t) -> Tr Delta rho(t). The same bound is uniform for
t<=T, so dominated convergence applies to the step-function time
integrals. Thus, with n epsilon_h ->T,

```text
E N_exit,h -> integral_0^T Tr Delta rho(t) dt,
E Cost_port,h = n+p integral_0^T Tr Delta rho(t) dt+o(1). (9)
```

The second-order exit correction has magnitude <=C_T epsilon_h.
The port formula uses the existing golden 0/10 costs 1/2, not a fitted
coefficient or a new subtraction in the physical action. Its divergent
n baseline is displayed explicitly.

More generally let one **supplied** finite per-round code have lengths
ell_0 on blank/port0 and ell_alpha on the actual 127 nonblank outputs.
No such complete code is physically selected here. Put
c_alpha=ell_alpha-ell_0 and use the original rescaled literal jump
operators from the previous owner, Section 7. Then exactly

```text
A_c,h=sum_alpha c_alpha elljump_alpha,h* elljump_alpha,h,
E Cost_code,h=n ell_0+epsilon_h sum_(j<n) Tr A_c,h rho_h,j.
```

Its quadratic form obeys |<u,A_c,h u>|<=C<u,Delta_h u>.
No inequality |A_c,h|<=C Delta_h for operator absolute values is needed.
More directly, its bilinear form is bounded by
C||Delta_h^(1/2)u|| ||Delta_h^(1/2)v||, by Cauchy–Schwarz
on the actual jump sum.
On bounded energy blocks its
limit is A_c=sum c_alpha elljump_alpha*elljump_alpha, with the special
blank-label/port1 jump tending to zero. Bounded-energy convergence uses
the actual N_k,h and D_h, not just a scalar heat trace. The remaining
cross-block tails are bounded by C sqrt(Tr Delta_h rho_h(high)), via
Cauchy–Schwarz in the energy form, and hence vanish under the second
moment bound. Therefore

```text
E Cost_code,h=n ell_0+integral_0^T Tr A_c rho(t)dt+o(1).   (10)
```

This establishes a complete fixed per-round code component once given.
History-dependent codes, ensemble normalization, calibration, controller
and workspace prices require their actual additional laws. Equations
(8)–(10) neither choose physical Info nor identify Cost-Info with v8.

## 7. Why the energy hypothesis is substantive: a full-reference control

Mere trace convergence is insufficient even for the actual flat native
instrument and pure preparations. Keep the original faithful preparation
Psi0=P_Sigma/sqrt(128), all eight shell momenta, all 16 forms and all
128 independent reference columns. Take R_L=ceil(log L),
N_L=floor(sqrt(L)/R_L), k_j=j R_L e0, and a normalized full-form vector
v=(1/4)sum_(a=1)^16 |a>. Let psi_UV=N_L^(-1/2)sum_j |k_j,v>.
Using one existing reference
column r0, define

```text
delta_L=1/log(16 N_L),
Psi_L=sqrt(1-delta_L)Psi0+sqrt(delta_L)psi_UV tensor r0.
```

Data supports are disjoint. Every original reference column remains
independent and every original shell occupation positive; no extra
carrier or lost matter grade is used. Inputs converge in trace norm to
Psi0, but their energy grows as L/log L.

Here is a direct native bound, rather than an assumed dephasing. On a
flat momentum pair (k,l), bistochasticity of T_h and its invariant
block imply Hilbert–Schmidt contraction. The Euler coefficient
1-epsilon_h(lambda_k+lambda_l)/2 is nonnegative because the actual flat
bound epsilon_h lambda_max<=p^2 nu^2/4<1 holds. Consequently

```text
||Phi_h,kl^n||HS->HS
 <=exp[-(n epsilon_h/2)(sqrt(lambda_k)-sqrt(lambda_l))^2]. (11)
```

On the chosen positive collinear UV sequence, sqrt(lambda_h(k))
=2nu L sin(pi k/L) has derivative bounded below up to sqrt(L).
Thus distinct radial gaps are >=c R_L|j-l|, and gaps to every base
shell mode are >=c(j R_L-1). Same-momentum traceless form parts relax
by the owned full CAR gap. Summing (11) and the diagonal bound shows
that the output is within C exp(-c(log L)^2) in trace norm of

```text
(1-delta_L)rho_base,h(T) directsum
 delta_L [I_N/N_L tensor I16/16 tensor |r0><r0|].
```

The trace error times log(16 L^4*128) tends to zero, so the finite
entropy continuity bound applies. The displayed block entropy tends
to S(rho_base(T))+1 nat. This defeats entropy convergence from trace
convergence alone while preserving the full faithful reference carrier.
It does not contradict (8): its initial energy bound fails.

## 8. The remaining physical and source arrow

The full spatial process now has uniform lattice moment estimates,
coherent entropy values and actual known code/count limits. These
remove analytic assumptions from the complete-price programme. The
moment hypotheses are stated regularity classes, not newly derived
admission conditions. Strong convergence alone does not supply them.

Still separate: convergence of field/preparation/clock derivatives,
rank-birth logarithmic jets, pointer entropy, actual full-history code
and workspace/ensemble laws, native operation/test/Info selection,
Einstein-source equality and a nonempty compatible joint refinement.
The original fixed nonconstant g, independent tau, all 10 packed rows,
unweighted raw h^-2/#216 terminal remains open. In particular a value
limit is not a source limit or an Einstein field equation.

The [bounded global-operator controls](sources/d0_variable_record_entropy_2026-10-17/README.md)
check native defect roots, global Hermitian Kraus and double-commutator
identities. The uniform calculus and limit statements are analytic
proofs above, not finite-spectrum extrapolations.
