# Complete retained record → actual matter channel and native code-cost source

17 October 2026. Same Draft #334, input ec5d6a00. Consumer: derive the
process behind the full retained tape, rather than use the total first-exit
operator as if it determined all future records. This composes the
[actual Julia/golden programme](A4D_RETAINED_HISTORY_CAUSAL_SOURCE.md),
[complete exit/action quotient](A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE.md),
[original code cocycle](A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md) and
[compiler/resource boundary](A4D_NATIVE_COMPILER_SOURCE_AND_RESOURCE_BOUNDARY.md).
No new reset, Gibbs preparation, action or code reference is introduced.

**Positive result.** The actual128-outcome round has an exact GKSL Euler
channel. Its recycling map, total-count tilt, port-energy observable and
original golden code-cost source are explicit. On flat geometry it has a
full16 relaxation theorem and a continuum CP semigroup on the entire
trace class. The stationary momentum weights are not Gibbs weights.
The full pointer entropy, coherent record entropy and a supplied full-code
operator price can all be computed on that same process, with their
actual preparation/reference sources and distinct physical bindings.

## 1. Full output channel, not just survival

Put A=hD_h/16=A*, alpha=p²h²/128, epsilon=2alpha, B=I-2p²A²,
N_k=Q_(blank;k), with sum_k N_k N_k*=I and N_blank=A. Keep all32 labels,
coefficient qubit, both golden ports, all16 forms and reference128.
Let a²=p, p+p²=1. On data plus fresh controller the literal port maps are

```text
K0=pI+p²W, K1=ap(W-I), W=W*=W^-1.
```

The mixed terms cancel exactly:

```text
K0 sigma K0*+K1 sigma K1*=p sigma+p² W sigma W.             (1)
```

For blank controller input, W_k0=delta_k0 I-2N_k* A. Tracing the **output
register as a marginal readout**, while retaining the complete register
in the global state, therefore gives

```text
T_h(X)=sum_k N_k* X N_k,
Phi_h(rho)=rho-alpha{Delta_h,rho}+2alpha T_h(D_h rho D_h)
          =rho+epsilon L_h(rho),
L_h(rho)=T_h(D_h rho D_h)-{Delta_h,rho}/2.                  (2)
```

T_h is CP and trace preserving. The paired actual Julia words also make
it unital and Hilbert–Schmidt selfadjoint. Indeed Walsh Parseval gives

```text
T_h(X)=(1/16)sum_r [P_r*XP_r+P_rXP_r*+L(P_r)XL(P_r)+R(P_r)XR(P_r)
                   +C_r*XC_r+C_rXC_r*+L(C_r)XL(C_r)+R(C_r)XR(C_r)],
L(P)=sqrt(I-PP*), R(P)=sqrt(I-P*P).                         (3)
```

The inverse/forward and left/right defects are both required. Complete
row unitarity alone would not prove unitality; (3) does. Equivalently
J_k=N_k*D_h and sum J_k*J_k=Delta_h give the GKSL form in (2).
Phi_h itself is exactly CP for the native epsilon, not an arbitrary
Euler step declared positive. L_h need not be unital on variable geometry.

Old records never interact with the next fresh round. The actual marginal
after n rounds is thus Phi_h^n(rho0), even when the global state is entangled
with every previous record. This computes a marginal; it does not erase,
measure or reset those records. It is not imaginary-time heat preparation.

## 2. Total exits and their full source

The single complete blank map and all other output maps satisfy

```text
Bmap(rho)=B rho B,
Jmap(rho)=Phi_h(rho)-Bmap(rho)
        =epsilon T_h(D_h rho D_h)-(epsilon²/4)Delta_h rho Delta_h,
E_exit=I-B²=epsilon Delta_h-(epsilon²/4)Delta_h².            (4)
```

Jmap is CP as the sum of the actual nonblank Kraus maps. The ordered
Delta rho Delta must not be replaced by Delta²rho. Define the tilted map
Phi_s=Bmap+exp(s)Jmap. Then

```text
Z_n(s)=Tr[Phi_s^n(rho0)],
E N_exit=sum_(j=0)^(n-1)Tr[E_exit Phi_h^j(rho0)].            (5)
```

All moments follow by differentiating Z_n at s=0. This is total repeated
exit count, not first-exit probability Tr rho0(I-B^(2n)).
For arbitrary admitted field/preparation variations the exact source is
computed by the same finite recursion

```text
rho_(j+1)=Phi_h(rho_j),
drho_(j+1)=Phi_h(drho_j)+(dPhi_h)(rho_j).                   (6)
```

Both dN_k and dD_h enter dPhi_h, with the actual Julia-root and adjoint
jets. If epsilon moves, dPhi_h=(d epsilon)L_h+epsilon dL_h. The initial
normalized preparation derivative is retained. This is a source formula
on every real native tangent, not an injectivity assumption on ten fields.

## 3. An actual port observable fixes the Rayleigh-cost coefficient

Summing **every label/coefficient at port1**, including blank-label/port1,
gives exactly

```text
E_port1=4p³A²=p epsilon Delta_h,
Pr(port1)=p epsilon Tr(rho Delta_h).                       (7)
```

Consequently R_h=Tr rho Delta_h has a direct existing-record readout.
At fixed h,p its full source is
`dR_h=Tr[(drho)Delta_h+rho dDelta_h]`, equivalently dPr(port1)/(p epsilon).
No commuting matter, fitted source or spectral oracle is needed.

The original binary golden code is port0/direct0 of length1 and
port1/return10 of length2, reference mu_port=(p,p²). Its code-cost
observable and n-round expectation therefore are

```text
G_port=I+E_port1=I+p epsilon Delta_h,
E Cost_port=n+p epsilon sum_(j<n)Tr[Delta_h rho_j].          (8)
```

This is a derived part of the native code cost and its full source,
without choosing an entropy. It does not pay for the remaining label,
coefficient, controller or archive code. At flat geometry energy is
conserved by this actual channel, so (8) becomes
`n+p beta_h R0`, beta_h=n epsilon. The coefficient p beta_h follows from
the original gate/code/clock; it is not independently selected.

For every nonblank **label/coefficient** k, both port maps are scalar
multiples of the same data operator: K_0k=p L_k, K_1k=a L_k,
L_k=-2p N_k* A. Their conditional probabilities are (p²,p). The retained
port bit affects neither the normalized data state nor any later outcome.
Hence the factorization holds conditioned on all reduced past and future
records. Keep both special blank-label ports separate. For the original
reference (p,p²), per nonblank-label occurrence,

```text
E code cost=1+p, E log_phi(q_port/mu_port)=p³,
H_phi(q_port)=2-p.                                        (9)
```

In particular the information term is not zero. Reversing the reference
to (p²,p) would change the original code. The exact full-tape Shannon
identity is H(full)=H(reduced)+(2-p)E N_label in phi units. Under the
owned path-weight binding, the corresponding information/cost identities
follow from the same cocycle; this does not select that binding globally.

## 4. Flat full16 recycling and actual relaxation

For constant C_r=nu c_r, 0<nu<1, put b=sqrt(1-nu²). On each momentum
diagonal block, phases of P_r=C_r exp(i k_r h) cancel exactly in (3).
Thus T_h,kk is the same full16 channel for every h,k:

```text
T0(X)=wI X+wM sum_(j=1)^8 xi_j X xi_j+wZ sum_(r=0)^3 Z_r X Z_r,
wI=(1+b)²/4, wM=nu²/16, wZ=(1-b)²/16,
xi=(c+c*, i(c-c*)), Z_r=I-2c_r c_r*.                        (10)
```

All weights are nonnegative and wI+8wM+4wZ=1. This is internal CAR
recycling, not merely D-dephasing. A Clifford monomial of degree k,
with o pairs containing exactly one Majorana, has eigenvalue

```text
t_(k,o)=wI+wM(-1)^k(8-2k)+wZ(4-2o), k=o+2d, o+d<=4.        (11)
```

The identity is the only invariant internal algebra. On traceless HS
operators the sharp norm is (3+b)/4<1, attained at k=7,o=1.
For fixed grade the largest value has minimal o (0 for even k,1 for odd
k); the largest nonconstant odd grade is7, and it dominates grade2.
In fact every eigenvalue is at least b²: with n_i role pairs containing
i Majoranas, the even-grade value is
`1-[(1-b)n1+(1-b²)n2]/4`; the odd-grade value instead has n0 in place
of n2. This also bounds the absolute value by the stated positive maximum.
This proves the norm statement without a256-state eigenvalue census.

On a positive momentum block Delta_h(k)=lambda_h(k)I16 and
U_h(k)=D_h(k)/sqrt(lambda_h(k)) is a Hermitian involution. Then

```text
L_h,k=lambda_h(k)[T0 composed with Ad(U_h(k))-Id].           (12)
```

The traceless form part contracts with rate at least
`lambda_h(k)(1-b)/4`. The exact discrete bound follows from
Phi_h,k=(1-t)Id+t T0 Ad(U_h), t=epsilon lambda_h(k), 0<=t<1.
Thus its unique stationary system form density is I16/16, with actual
occupations approaching1/2. Every reference component remains: stationary
blocks have form I16/16 tensor R_k, not a discarded reference state.

## 5. The full flat stationary algebra and continuum process

At finite h the complete flat channel is unital. The bistochastic
Dirichlet identity characterizes fixed operators by commutation with all
Kraus operators and their adjoints. The unshifted row blocks C,C*,L,R
span I and all xi_j because L+R=(1+b)I. Multiplication by D_h then puts
D_h and all xi_j D_h in the actual jump-Kraus span.
On the complement of ker D_h, commutation with D_h and xi_j D_h forces
commutation with all eight Majoranas, hence scalar form blocks.
The native Fourier symbol is injective: D_h(k)=D_h(l) requires k=l.
Therefore the system fixed algebra is

```text
M16 on zero momentum, plus one scalar I16 for each nonzero momentum.
```

The full system/reference fixed algebra is its tensor product with M128.

Mixed zero/nonzero momentum coherences vanish; the dark zero-momentum
state remains arbitrary. The positive lazy identity contribution in (1)
excludes other peripheral phases, so finite-h powers converge to this
fixed algebra. Momentum weights are conserved, rather than forced Gibbs
or uniform weights. Pure Rayleigh-eigenshell stationarity is a different
condition: a faithful system density may be stationary while its actual
maximally entangled system/reference purification changes under Phi tensor Id.

There is also a rigorous full trace-class flat continuum construction.
Every finite Fourier cutoff is invariant under every flat Kraus operator.
On each fixed cutoff, L_h converges to L0 and finite-dimensional Euler
powers converge for beta_h→beta. The compatible CP trace-preserving limits
agree on nested cutoffs. Trace-norm contraction then extends them by
cutoff density to a unique strongly continuous CP semigroup on the full
trace class, with all16 modes and reference128. This is not an appeal to
an unproved unbounded Trotter theorem.

For a fixed finite-energy continuum input rho0, use its normalized Fourier
compression onto the grid's resolved momentum window for rho0,h. These
compressions converge in trace norm; pointwise sampling of an arbitrary
finite-energy state in four dimensions is not assumed.
Then lambda_h(k)<=nu²|k|² and spectral dominated convergence give

```text
E N_exit -> beta Tr(rho0 Delta0),
E N_port1 -> p beta Tr(rho0 Delta0).                        (13)
```

The quadratic correction in (4) is dominated by the first energy moment
because epsilon lambda_h is uniformly bounded. No second energy moment
is required here. A moving uniform full-grid state I/d_h has no fixed
trace-class continuum limit and is outside this statement, consistently
with the earlier UV preparation separator.

### 5.1 A finite-carrier criterion for faithful stationary matter

This channel also gives a variable-geometry statement without a new
stationarity postulate. On a finite carrier let P0 project onto ker D,
and P+=I-P0. Then

```text
there exists rho>0 with L(rho)=0  iff  T(P0)=P0.
```

Indeed the actual dark-block mass obeys
`d Tr(P0 rho)/dt=Tr[rho D T*(P0)D]>=0`. Faithful stationarity forces
`D T*(P0)D=0`. Positivity, `0<=T*(P0)<=I`, and trace preservation of the
bistochastic T* then give T*(P0)=P0; here T*=T by (3). Conversely
T(P0)=P0 gives T(P+)=P+ and L(Delta_+^-1)=0. Any positive dark-block
sigma0 is stationary, so a normalized `a Delta_+^-1+sigma0`, a>0,
is faithful. Empty-block conventions cover D=0 or invertible D.
The projection condition equivalently says every actual recycling Kraus
N_k reduces P0/P+; unitality places the fixed projection in the
multiplicative domain.

This is system-density stationarity, not a derived requirement that a
physical preparation be stationary. A faithful density on the whole
16L^4 system cannot in general be purified using reference128 alone.
Nor is Delta_+^-1 generally trace class in four-dimensional continuum.
Thus this finite criterion does not manufacture an admitted full-reference
preparation or a continuum Gibbs/steady-state law.

## 6. Full tape entropy: exact chain and one controlled source

Pointer probabilities refer to the actual final orthogonal record basis.
For every prefix pi let p_a(pi) be the conditional probability of a
nonblank output and lambda_a=p_a/epsilon, Lambda=sum lambda_a.
Shannon's conditional chain rule is exactly

```text
H_pointer=log(1/epsilon) E N_exit
 +E sum_(j<n)[-(1-epsilon Lambda)log(1-epsilon Lambda)
             -epsilon sum_a lambda_a log lambda_a].       (14)
```

No prefix normalizer or conditional future state is frozen. In the
canonical ordinary/rare partition an equally exact two-scale expression
has log(1/epsilon) coefficient E N_ordinary+2E N_rare when probabilities
are written epsilon r_o and epsilon²r_r. Their rate-entropy terms remain.
Thus a rare first-exit h² reading does not fix the complete h²logh source.

On the actual flat first shell Delta_h=lambda_h I, every prefix has the
same exit probability e_h=epsilon lambda_h-epsilon²lambda_h²/4 and the
blank map is scalar. Complete exit indicators are therefore exactly iid
Bernoulli. With J_a=K_a/sqrt(e_h) the normalized63-mark jump instrument,

```text
H_pointer=n h_bin(e_h)+E_(K~Bin(n,e_h)) H_J(K),
0<=H_J(K)<=K log63.                                       (15)
```

All128 physical outcomes remain;64 duplicate outcomes are exactly dark,
leaving63 active nonblank slots. The full count tends to Poisson mean
beta lambda, distinct from first-exit probability1-exp(-beta lambda).

For isotropic nu in a compact strict interval and a fixed smooth
first-shell input, the normalized jump Stinespring map and its first nu
jet are uniformly bounded. A K-mark word has derivative norm O(K+1),
so its classical Fisher information is O((K+1)²). For at most63^K marks,
`E[log² q]<= (K log63)²+2K log63+2`; Cauchy–Schwarz bounds its entropy
source by O((K+1)²), without assuming probabilities bounded away from zero.
Binomial moments and e_h'/e_h are uniformly bounded on this interval.
Thus the remainder in (15) is bounded in C1, and at fixed epsilon,n,

```text
H_pointer=beta_h lambda_h log(1/epsilon)+O_C1(1),
partial_nu H_pointer
 =beta_h (partial_nu lambda_h)log(1/epsilon)+O(1).           (16)
```

This is an actual full-history source, not an inference from a coarse
entropy inequality. Binding expected Cost−Info to this Shannon quantity
still requires the original path-weight/code interpretation on the entire
tape. It is not the supplied finite-source v8 action by renaming entropy.
No general variable-field/UV trajectory entropy theorem is claimed.

## 7. Coherent record entropy and full-code source can be kept exact

The coherently retained record state generally has off-diagonal entries
Tr(K_omega rho K_omega'*); its von Neumann entropy differs from pointer
Shannon entropy. For pure initial system/reference state Psi0, let V have
columns v_omega=K_omega Psi0. The record matrix is (V*V)^T, while the final
system/reference density is VV*. Their nonzero spectra coincide. Hence

```text
S_vN(record)=S_vN(rho_system,reference,n).                  (17)
```

The right side is computed on the original system/reference carrier,
without enumerating an exponentially large tape. On the first shell its
entropy is bounded by log(128*128), independent of n, unlike (16).
The moving preparation and all reference correlations belong in (17).

For a **given** actual normalized full-code prior mu_a=phi^(-c_a)>0,
let G_nat=log(phi) sum_a c_a K_a*K_a. Its additive expected cost and
operator relative entropy have the exact diagram. In (18)–(19), rho_j
means the **full system/reference density**, Phi means Phi tensor Id128,
and G means G tensor I128; system entropy cannot replace this final entropy.

```text
A_nat=D(record || diag(mu)^tensor n)
     =sum_(j<n)Tr(G_nat rho_j)+Tr(rho_n log rho_n),
A_phi=A_nat/log(phi).                                    (18)
```

If the code is only Kraft-subnormalized, put s=sum mu. Explicitly
`D(record || diag(mu/s)^tensor n)=A_nat+n log s`, including the source of
that term. Neither the label prior
nor physical choice of Info is selected by (18).
For a pure preparation family, fixed n and a final state with fixed smooth
positive support, the complete source is obtained from a small-state
costate recursion

```text
Y_n=log rho_n+I, Y_j=G_nat+Phi_h*(Y_(j+1)),
dA_nat=Tr(Y_0 d rho_0)
       +sum_(j<n)Tr[(dG_nat)rho_j+Y_(j+1)(dPhi_h)(rho_j)].  (19)
```

This includes actual coframe/link/observer and normalized preparation jets.
Moving calibration is differentiated inside Phi,G; changing integer depth
requires its declared schedule. Rank births require their true entropy
limit and cannot use a frozen-support logarithm. Thus the mathematical
full-code/source interface is explicit without replacing coherent
information by classical probabilities or introducing a Gibbs state.

The bounded adjacent checks verify new full16 round/count/code identities
and flat recycling/relaxation controls. Continuum extension, entropy C1
control and the source costate are analytic arguments above. Native
primitive/resource admission, complete code/Info selection, equality to
intrinsic Einstein sources and compatible joint refinement remain open;
the original fixed-g/tau/all10 raw h^-2/#216 terminal is unchanged.
