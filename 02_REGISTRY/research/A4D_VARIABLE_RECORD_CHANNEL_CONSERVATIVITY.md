# The actual variable-field record generator has a conservative continuum channel

17 October 2026. Same Draft #334, input aa834d4f. Consumer: extend the
[actual record channel](A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md)
beyond invariant flat Fourier windows. The [full variable-field stencil](A4D_NATIVE_FINITE_HEAT_SOURCE_LIMIT.md)
supplies the true adjoint, proper-link scaling, coframe and observer chart.
This is a mathematical evolution theorem for that declared instrument;
it does not select its physical admission, action, Info or time reading.

**Result.** On the full smooth compact torus, with all 16 form components
and reference 128, the actual limiting GKSL generator defines a unique
conservative minimal quantum dynamical semigroup. Its predual is a
strongly continuous completely positive trace-preserving evolution on
the entire trace class. No finite energy window or preparation rank is
imposed on the state space. An explicit subprincipal Lyapunov corrector
proves conservativity even when the bare energy estimate is false.
It changes no jump, Delta, record, preparation or action. The actual
finite-h marginal trajectories also converge strongly in trace norm at
every fixed record time, for every converging trace-class preparation.
The proof uses the exact positive jump decomposition and conservation
to control its tails; it does not assume a trace-class generator core.

## 1. The limiting generator comes from the existing rounds

Work in the actual observer-whitened Hilbert space
`H=L2(T4;C16)`, with the original density/coframe trivialization. Assume
smooth coefficients on the compact torus, proper links with their selected
first jets, a controlled timelike observer chart, and a real invertible
coframe row matrix U=(u_ra) with

```text
s_min(U(x))>=sigma>0, |u_r(x)|<=nu_max<1.
```

The bounds are regularity/strict-Julia hypotheses of the existing matrix
programme, not new physical constraints. The full proper Lorentz
connection may be arbitrary within the smooth controlled chart; metricity,
torsion-free/LC reduction and a stationary field equation are not imposed.

Let D=d+d* be the existing first-order operator, Delta=D². Its principal
symbol P(x,xi) is Hermitian Clifford multiplication, with
`P²=lambda(x,xi)I16`, `lambda>=sigma²|xi|²`. Formal selfadjointness and
elliptic regularity on the boundaryless torus give the selfadjoint
realizations `D(D)=H1`, `D(Delta)=H2`, with common smooth cores.

The actual finite round has, exactly,

```text
Phi_h=Id+epsilon_h L_h,
L_h(rho)=sum_k N_k,h* D_h rho D_h N_k,h-{Delta_h,rho}/2.
```

At proper scaling the rows converge on smooth vectors to multiplication
matrices N_k(x). For smooth u,v the finite-difference/adjoint consistency
therefore gives trace-norm convergence of L_h(|u><v|) to

```text
L(rho)=sum_k J_k rho J_k*-{Delta,rho}/2,
J_k=N_k*D, sum_k J_k*J_k=Delta.                           (1)
```

Rank-one trace-norm consistency identifies this same generator; it is
not by itself convergence of the finite-time lattice channels.
All 128 physical output slots remain in their native history. The 64-row
jump description is a marginal-generator identity, not an erasure or
a new physical Kraus-basis readout.

## 2. A native fixed-phase identity is essential

At h=0 the paired Julia expression on multiplication matrices is

```text
T_x(A)=(1/8)sum_r[C_r* A C_r+C_r A C_r*
                          +L_r A L_r+R_r A R_r],
C_r=c(u_r), L_r=sqrt(I-C_r C_r*), R_r=sqrt(I-C_r* C_r).
```

The actual Walsh rows have a stronger spatial identity than pointwise
bistochasticity. With fixed word characters sigma_w,tau_w in{±1}, their
nonzero limiting rows are proportional to

```text
coefficient0: (1-tau_w)sum_r chi_r(C_r+sigma_w C_r*),
coefficient1: (1-tau_w)sum_r chi_r(L_r+sigma_w R_r).
```

Thus each N_k* equals either +N_k or -N_k with a sign independent of x.
Multiplication by one fixed phase gives Hermitian matrices B_a(x) such
that the **global operator map** and its local version are

```text
T_global(X)=sum_a B_a X B_a,
T_x(A)=sum_a B_a(x) A B_a(x), sum_a B_a²=I.
```

In particular `Tr16 sum_a B_a partial_i B_a=0`.
This uses the actual native rows. A variable phase N=e^(if(x))I would
have the same pointwise identity map but a nonzero derivative trace;
pointwise selfadjointness alone cannot replace the fixed-phase proof.
The phases here are an analytical representation of the same channel,
not extra allowed rotations of a physical record.

## 3. Full16 mixing gives an explicit principal inverse

Put nu_r=|u_r|, b_r=sqrt(1-nu_r²), n_r=u_r/nu_r. Pointwise only,
the same map has the random-unitary identity

```text
T_x=wI Id+sum_r[(nu_r²/16)(Ad_beta(n_r)+Ad_eta(n_r))
                        +(1-b_r)² Ad_Z(n_r)/16],
wI=sum_r(1+b_r)²/16>=1/4.
```

Here beta(n)=c(n)+c(n)*, eta(n)=i(c(n)-c(n)*),
Z(n)=I-2c(n)c(n)*. These are Hermitian unitaries. Do not differentiate
this pointwise Kraus recombination as if it were the global T_global:
its coefficients depend on x. Section 2 supplies the correct global rows.

The unitary Dirichlet identity and s_min(U)>=sigma give, on traceless
internal matrices X,

```text
<X,(I-T_x)X>HS >=(sigma²/32)sum_(a=1)^8 ||[gamma_a,X]||HS²
                 >=sigma² ||X||HS²/8.
```

Here gamma_a are the eight constant CAR Majoranas. For a Clifford
monomial of degree k, the commutator sum has factor4k
at even k and4(8-k) at odd k; its smallest nonidentity factor is4.
This proves the last bound on the complete 16-dimensional CAR module,
without an eigenvalue/rank census. The identity weight also gives
`spec T_x>=-1/2`, hence

```text
||T_x|_(Tr=0)||HS<=1-sigma²/8<1.                         (2)
```

This is an internal form gap. No irreducibility on reference 128 or
spatial momentum, and no Gibbs state, is inferred.

## 4. The bare energy fails, but its cubic defect is traceless

The Heisenberg form of (1) is

```text
L*(X)=D T_global(X)D-{Delta,X}/2.
```

In particular `L*(Delta)=D[T_global(Delta)-Delta]D`.
Write `Delta=-g^ij partial_i partial_j+A^j partial_j+V`. Its scalar
second-order principal term cancels in T_global(Delta)-Delta. The
remaining first-order coefficients are

```text
Q^j=T_x(A^j)-A^j-2g^ij sum_a B_a partial_i B_a.
```

Trace preservation and Section 2 give Tr16 Q^j=0. Therefore the Hermitian
degree-three principal symbol F3 of L*(Delta) obeys

```text
F3=P [i sum_j Q^j xi_j]P, Tr16 F3=0.                     (3)
```

The drift itself need not vanish. An actual constant-coframe, constant
proper-boost example already shows this: C_r=nu c_r, only Omega_2=B01,
Gamma(B01)=c0 c1*+c1 c0*. Along momentum k e0 put

```text
D(k)=nu[k eta0+beta2 Gamma(B01)], V01=i beta2 beta1.
```

The linear Delta term is nu² k V01. T0(V01)=(1+b)V01/2, b=sqrt(1-nu²),
so the cubic defect is `-(1-b)nu^4 k³ V01/2`, with both signs and
nonzero magnitude. It cannot be bounded above by a constant times
I+Delta. Thus a bare-energy proof would incorrectly remove genuine
proper-link fields.

## 5. An analytic corrector cancels that actual defect

For xi!=0 let W=P/sqrt(lambda). It is a Hermitian involution. The
principal action of L* on a first-order correction symbol b1 is

```text
M_(x,xi)(b1)=P T_x(b1)P-lambda b1
           =lambda[Ad_W T_x-I](b1).
```

It preserves traceless Hermitian matrices. By (2), its inverse exists
there, with

```text
||M^-1|| <=8/(lambda sigma²)<=8/(sigma^4 |xi|²),
b1(x,xi)=-M_(x,xi)^-1 F3(x,xi).                          (4)
```

The Neumann inverse is smooth on the unit cotangent sphere. Thus b1
is Hermitian and homogeneous of degree1. A real low-frequency cutoff
and torus Weyl quantization give a symmetric order1 operator B1.
For a sufficiently large constant a define

```text
H=2(Delta+B1)+aI>=I+Delta.                              (5)
```

Order1 relative form/operator bounds and elliptic regularity give a
selfadjoint H on H2, with H1 form domain and an equivalent energy norm.
The correction cancels the complete cubic symbol (3), so L*(H) is a
symmetric pseudodifferential operator of order at most2. Consequently

```text
|<u,L*(H)u>|<=C ||u||H1²<=C' <u,H u>, u smooth.           (6)
```

In the boost example b1(k)=-nu² k V01 does the cancellation exactly.
This illustrates (4); the general proof does not restrict the field
or matter to this example. H is solely a Lyapunov operator used in the
proof. Delta, all jumps, the code/action and the actual dynamics are
unchanged; no compensating physical energy has been added.

## 6. Minimal evolution and all conservation hypotheses

Use the standard minimal-QDS construction with G=-Delta/2 and jumps J_k.
The theorem applied here is Corollary 4.5 of
[Chebotarev–Fagnola, Sufficient Conditions for Conservativity of Minimal
Quantum Dynamical Semigroups](https://arxiv.org/pdf/funct-an/9711006).
Its conservation criterion is prior work; the native gap and corrector
above verify its assumptions for this generator.

The verification is explicit. G generates a selfadjoint contraction
semigroup. D(G)=D(H)=H2; Fourier smoothing approximates both graph norms
simultaneously, so C-infinity is a joint core. Every J_k preserves smooth
vectors. The dissipative operator is exactly Delta because
`-2Re<u,Gu>=sum_k||J_k u||²=<u,Delta u><=<u,H u>`.
Finally on that same core,

```text
2Re<Hu,Gu>+sum_k<J_k u,H J_k u>
       =<u,L*(H)u><=C'<u,H u>.
```

Thus all four hypotheses of that corollary hold. The minimal QDS is
conservative on B(H). It is the unique normal contractive CP solution
of the corresponding weak integral equation: minimality gives order
domination by another solution, while equality on I forces the positive
difference map to vanish. Its predual preserves trace and positivity
on the whole trace class. Weak continuity plus trace conservation and
finite-rank approximation give strong trace-norm continuity, without
assuming an energy cutoff for the input density.

Tensor every jump with I128 and H with I128. The same finite direct-sum
domain/core proof retains every reference component and correlation.
This proves the stated evolution on the entire full16 spatial carrier
with reference 128; the internal gap is not improperly applied to the
reference commutant.

## 7. The actual finite-h trajectories converge

Use the Fourier isometries E_h:H_h -> H and projections P_h=E_h E_h*,
P_h -> I, from the finite heat/source owner, Section 5. Its embedded
heat convergence gives the no-jump limit. Indeed the native contraction
A=hD_h/16 has norm at most 1, so

```text
epsilon_h ||Delta_h||<=4p²<2,
B_h=I-epsilon_h Delta_h/2>=1-2p²>0.
```

For n=floor(t/epsilon_h), functional calculus bounds the scalar
difference between (1-epsilon_h x/2)^n and exp(-n epsilon_h x/2)
uniformly on the actual spectral interval. Together with the embedded
heat limit and contractivity this gives

```text
C_h(t)=E_h B_h^floor(t/epsilon_h) E_h* -> C(t)=exp(-t Delta/2)
```

strongly, uniformly on bounded time intervals. At t=0 use P_h -> I;
uniformity near zero follows first on a smooth dense set and then by
contractivity. No full-channel lattice Lyapunov estimate is required.

### The exact positive split includes the special blank jump

Let k=0 denote the blank label/coefficient, so N_0,h=hD_h/16 and
J_0,h=hDelta_h/16. Define mathematical jump representatives

```text
tilde J_k,h=J_k,h for k!=0, tilde J_0,h=sqrt(p) J_0,h.
```

The actual ordinary/nonblank decomposition, including blank-label/port1,
is exactly

```text
Phi_h(rho)=B_h rho B_h+epsilon_h sum_k tilde J_k,h rho tilde J_k,h*,
epsilon_h sum_k tilde J_k,h* tilde J_k,h=I-B_h².          (7)
```

For verification, the recycling term loses
epsilon_h(1-p)h²Delta_h rho Delta_h/256
=epsilon_h²Delta_h rho Delta_h/4, since 1-p=p².
This is exactly the excess term in B_h rho B_h. Thus (7) is a sum of
actual nonblank port maps, with their common port factors combined
analytically. It neither adds a detector nor rotates the physical tape.
For the path proof keep the actual 127 nonblank record slots rather
than introduce a readout in this reduced mathematical basis. With
a=sqrt(p), their rescaled literal Kraus operators are

```text
ell_(k,port0),h=-p J_k,h, ell_(k,port1),h=-a J_k,h (k!=0),
ell_(0,port1),h=-sqrt(p) hDelta_h/16.
```

Their recycling sum is the same as in (7), and
epsilon_h sum_alpha ell_alpha,h* ell_alpha,h=I-B_h².
The special last jump and its adjoint vanish on smooth vectors.
All other jumps and adjoints converge on that core with their actual
port factors. Their continuum recycling sum is exactly (1), since
p²+p=1. Every original physical output slot is retained in this proof.

### First-jump contractions remove the adjacent-jump singularity

Fix T>0, n_h=floor(T/epsilon_h), and use one common 127-dimensional
mathematical mark space. For s in [j epsilon_h,(j+1)epsilon_h),
0<=j<n_h, define the embedded Hilbert-space map

```text
(F_h^T u)(s,alpha)=E_h ell_alpha,h B_h^j E_h* u;
F_h^T u=0 on the remainder of [0,T].
```

Equation (7) telescopes exactly:

```text
||F_h^T u||L2²=||P_h u||²-||C_h(n_h epsilon_h)u||².      (8)
```

Hence ||F_h^T||<=1. The limit F^T u=(ell_alpha C(s)u)_alpha satisfies
the identical integrated energy identity

```text
||F^T u||L2²=||u||²-||C(T)u||²,
```

by sum ell_alpha*ell_alpha=Delta and the spectral theorem. Pair F_h^T u with
time-dependent smooth spatial test vectors. Move ell_alpha,h to that
test vector; smooth-core adjoint consistency and strong convergence of
C_h give weak L2 convergence. Such tests are dense, and (8) bounds all
the maps. Their norms converge by the no-jump limit. Weak convergence
and convergence of norms in this fixed Hilbert space therefore prove
F_h^T u -> F^T u strongly, for every u in H. No pointwise control of
an unbounded jump at s=0 or high-energy input moment is assumed.

For a fixed number m of jumps, iterate F_h^T on the last H factor of
the product waiting-time space [0,T]^m. The maps remain contractions.
Bounded strong convergence passes through each tensor extension and
finite composition, first on simple tensors and then by density.
On a waiting cell with indices j_1,...,j_m, multiply by

```text
1_(sum_i j_i<=n_h-m) C_h((n_h-m-sum_i j_i)epsilon_h).     (9)
```

Each jump consumes one time step. The cell integral epsilon_h^m
therefore gives exactly the m-jump term in the noncommutative expansion
of Phi_h^n_h, including its final no-jump interval. The bounded
multiplication operators (9) converge strongly to
1_(sum_i s_i<T) C(T-sum_i s_i). The simplex boundary has measure zero,
and strong no-jump convergence and domination apply everywhere else.
This proves strong convergence of each terminated m-jump Stinespring
map. In particular, arbitrarily adjacent jumps cause no hidden graph
estimate: they are included in the strong L2 contraction argument.

Partial trace now gives trace-norm convergence of every fixed m-jump
CP output, for every trace-class input. This follows first for rank-one
inputs from strong Stinespring convergence and then by contraction and
finite-rank approximation. The continuum terms are precisely the
minimal-QDS Dyson construction verified in Section 6.

### Conservativity controls the entire jump tail

For positive rho_h whose embedded operators converge in trace norm to
rho, let Omega_h^(<=M) and Omega^(<=M) be the sums through M jumps.
Both remainders are positive. The actual lattice channel is TP, so

```text
||Phi_h^n_h(rho_h)-Omega_h^(<=M)(rho_h)||1
       =Tr rho_h-Tr Omega_h^(<=M)(rho_h).
```

Fixed-M convergence identifies the limit of this tail trace. Section 6
conservativity gives Tr Omega^(<=M)(rho) -> Tr rho. Consequently

```text
limsup_h ||E_h Phi_h^n_h(rho_h) E_h*-exp(T L)(rho)||1
       <=2[Tr rho-Tr Omega^(<=M)(rho)] ->0.               (10)
```

Every trace-class input is a linear combination of four positive ones;
contractivity also handles arbitrary converging preparations. Tensor
all maps with I128 to retain every reference correlation. This proves
the stated full variable-field marginal trajectory limit without
asserting that smooth rank-one operators form a generator core in
trace norm. Equation (10) is qualitative; no h^-2 source rate follows.

## 8. The consumed arrow and its remaining source boundary

The actual variable-field limiting record generator now has a well-defined
conservative evolution. The proof does not demand constant geometry,
fixed preparation rank, an invariant finite Fourier window or vanishing
recycling drift. This removes a genuine analytic prerequisite for using
the full record process on spatially varying geometries.

The actual finite-h marginal trajectories converge by Section 7.
Still separate: uniform entropy and its field-source limits, full tape
state limits, rank-birth control, complete
native code/Info/admission, equality with intrinsic Einstein sources and
a compatible nonempty joint refinement. Core-generator consistency is
not substituted for those limits. Neither the earlier 2048 compression
nor its spectral gap is extended to a growing UV carrier. The original
fixed-g/tau, all 10 packed raw h^-2/#216 terminal remains open.

The [bounded input controls](sources/d0_variable_record_channel_2026-10-17/README.md)
check the actual full 16-component phase, derivative, boost, correction
and positive split identities. Conservativity and trajectory convergence
are the analytic proofs above, not a
conclusion drawn from a finite matrix fixture.
