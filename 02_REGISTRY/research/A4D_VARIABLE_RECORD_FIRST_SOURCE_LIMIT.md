# Full spatial first sources of the actual record process, entropy and code

17 October 2026. Same Draft #334, input `5cfabc85`. Consumer: turn the
[whole-lattice entropy/code value limits](A4D_VARIABLE_RECORD_ENTROPY_AND_CODE_LIMIT.md)
into actual first sources. This uses the existing variable native
process, full spatial carrier, all 16 forms and reference 128. It adds
no action, Info, physical admission, ensemble, reset or clock law.

**Result.** On uniformly smooth controlled parameter charts, the actual
state derivative converges in trace norm under a uniform third initial
energy moment and the stated locally uniform initial tangent convergence.
With a bounded actual normalized preparation-purification tangent,
the complete coherent-record entropy derivative also
converges, without a fixed support or a positive spectral floor. A
fourth initial moment and a weighted initial tangent give convergence
of the original port-cost and every supplied fixed per-round-code
first source. These are smooth-field covectors of this declared native
process, not the original rough all-grid raw h^-2 terminal and not an
identification with the Einstein source.

## 1. The actual fields, preparation and clock must all be differentiated

Let s vary in a compact smooth parameter interval inside the previous
strict Julia/coframe/observer chart. Bounds include the needed spatial
and parameter derivatives. Proper links satisfy
M_h(s)=I+h Omega(s)+O(h^2), including their derivatives: M'_h=O(h).
All 24 proper connection jets, coframe directions and observer/density
jets remain; none is frozen. This is a controlled smooth variation,
not an arbitrary O(1) lattice link variation.

Work in one fixed observer-whitened Hilbert space. If a raw preparation
is x_raw(s), its actual representative is x=I_s x_raw, with squared
normalization N=Tr x*x. Then

```text
x'=I_s x_raw'+K_s x, K_s=I'_s I_s^(-1),
rho0=xx*/N,
eta0=(x'x*+xx'*)/N-(N'/N)rho0, Tr eta0=0.                (1)
```

For its actual pure system/reference vector, the derivative is
Xi0=x'/sqrt(N)-(N'/(2N))Psi0. All existing reference columns remain;
(1) includes both the moving trivialization and normalization source.
Initial state and tangent convergence below are assumptions on this
actual normalized preparation, not on an unnormalized surrogate.
They are locally uniform in the indicated weighted trace topology,
with a continuous limiting tangent. C1 convergence of sampled smooth
normalized preparation amplitudes is one sufficient realization;
pointwise tangent convergence to a discontinuous function is excluded.

At each fixed h keep the integer depth n locally fixed. Usually
h,p and epsilon_h=p^2 h^2/64 are fixed under field variation. If an
actual supplied smooth programme changes epsilon_h(s), keep epsilon_h/h^2
bounded above and below and retain the actual native CFL condition.
Require bounded kappa_h=epsilon'_h/epsilon_h converging locally uniformly
to its prescribed continuous limit kappa. The
record-time jet is then T'=kappa T when n epsilon_h ->T. No derivative
of floor(n(s)) is introduced, and no independent clock law is inferred.

There are two distinct exact jump descriptions. The generator uses
all 64 rows J_k,h=N_k,h*D_h, with sum J_k,h*J_k,h=Delta_h. Thus

```text
L'_h(X)=sum_k[J'_k,h X J_k,h*+J_k,h X J'_k,h*]
                         -{Delta'_h,X}/2.              (2)
```

The actual 127 nonblank physical outputs ell_alpha,h instead obey
sum ell_alpha,h*ell_alpha,h=Delta_h-epsilon_h Delta_h^2/4.
They are used for the physical tape and code, not substituted into
(2) without its missing finite-step correction.

## 2. Integer moment control and the weighted trace spaces

The previous periodic-symbol construction extends to every fixed
integer m>=1. Its principal defect and correction are

```text
q_m=m lambda^(m-1)q1,
F_m=m lambda^(m-1)F1,
b_m=m lambda^(m-1)b1.
```

The symmetrized correction has order 2m-1 and cancels the entire
order-(2m+1) defect; the remaining form is order 2m. The low-frequency
part is bounded because F_m=O(rho^(2m+1)). The same finite-grid calculus
and elliptic estimate therefore give analytic Lyapunov operators

```text
H_m,h comparable to (I+Delta_h)^m,
L_h* H_m,h<=C_m H_m,h                                  (3)
```

uniformly on the full Brillouin cube. Only finitely many m are needed
here. This is the same argument, with no new spectral or rank search.
The analytic operators replace no physical observable or action.

Put G=I-sum_r partial_r^2 on the spatial carrier, tensor I_(16*128),
and G_h=E_h*G E_h. The whole-grid elliptic estimates compare G_h^m
and (I+Delta_h)^m as forms, with uniform constants. Define

```text
||X||1,r=||G^(r/2) X G^(r/2)||1,
S1,r={X: ||X||1,r<infinity}, r=0,1,... .                 (4)
```

Use the analogous grid norms before embedding. For a positive state,
||rho||1,r=Tr G^r rho. CP and (3) imply a uniform propagator bound in
(4): conjugate Phi_h by G_h^(r/2) and its inverse. The conjugated map
is CP, and its trace norm is bounded by the positive-input energy
bound. Hence its whole trace-class norm has the same bound.

The same bound passes to the continuum process by positivity and lower
semicontinuity. Weighted finite-rank density is explicit: Fourier
compressions commute with G and approximate G^(r/2)XG^(r/2) in trace
norm. The interpolation estimate

```text
||X||1,r<=||X||1^(1-r/m) ||X||1,m^(r/m), 0<r<m,         (5)
```

follows by the three-lines inequality applied first in finite Fourier
dimension, then by compression. Ordinary trajectory convergence and
higher moments therefore give weighted convergence on smooth finite
rank inputs. Uniform propagator bounds and density extend this to
every converging input in S1,r. On the dense S1,r+2 class the exact
one-step identity gives time modulus C(|t-u|+epsilon_h)||X||1,r+2;
contraction/density extend compact-time strong convergence. No claim
about a trace-class generator core is needed.

## 3. The actual state source has a strong weighted Duhamel limit

The true differentiated jumps, including the special physical
hDelta_h/16 output, are uniform first-order operators on the grid.
Delta'_h is order 2. Both assertions use full parameter derivatives
of the shifted Julia roots and adjoints. The CFL inequality
h G_h^(1/2)<=C keeps hDelta_h uniformly first order even at Nyquist.
Factorization of left/right products in (2) gives

```text
L'_h: S1,r+2 -> S1,r uniformly.                         (6)
```

For example the second-order left product factors as
G_h^(r/2)Delta'_h G_h^(-(r+2)/2) times a trace-class
operator times G_h^(-1); both outside factors are bounded. The jump
sandwiches require no more derivatives. Differentiated stencil/root
consistency on smooth finite-rank inputs proves strong convergence
in (6); weighted finite-rank density extends it to the entire domain.
This uses actual field jets, not value consistency alone.

Set eta_h,j=partial_s rho_h,j. At fixed n the exact recursion and sum are

```text
eta_h,j+1=Phi_h eta_h,j+epsilon_h K_h rho_h,j,
K_h=L'_h+kappa_h L_h,
eta_h,n=Phi_h^n eta_h,0
       +epsilon_h sum_(j<n)Phi_h^(n-1-j)K_h rho_h,j.     (7)
```

Suppose initial states converge locally uniformly in trace norm with
uniform moment r+3, and their normalized tangents converge locally
uniformly in S1,r to a continuous eta0(s). Equations (3)–(5)
give rho_h(t)->rho(t) in S1,r+2, uniformly on bounded time intervals.
Together with (6) this makes the sources converge in S1,r. Bounded
propagators, compact-time convergence and the actual Riemann sum (7)
give

```text
eta(T)=P_T eta0+integral_0^T P_(T-t)[L'+kappa L]rho(t)dt,
eta_h,n -> eta(T) in S1,r.                              (8)
```

On compact parameter intervals these bounds are uniform. Pass to the
limit in the finite-h fundamental theorem of calculus; the same
weighted density/consistency estimates make the right-hand side (8)
continuous in s. Thus the limiting state is genuinely C1 along the
stated smooth field/preparation curve, with derivative (8). A value
limit has not merely been differentiated formally.

For fixed native epsilon, kappa=0. For an actual given clock jet the
extra term in (8) equals kappa T L rho(T) on the present regularity
class, exactly the endpoint time derivative T' L rho(T).

## 4. The actual tape derivative is bounded by an orthogonal innovation

This step needs no convergence or even common embedding of tape
purification derivatives. At each finite h the literal one-round
isometry is

```text
W_h u=(K_blank,0 u, (K_alpha u)_(127 nonblank)),
K_blank,0=I-epsilon_h Delta_h/2,
K_alpha=sqrt(epsilon_h) ell_alpha,h,
W_h*W_h=I.
```

The old records remain and every new round acts on the data and a fresh
register. Define the genuine parameter connection and innovation

```text
A_h=W_h* W'_h, A_h*=-A_h,
R_h=W'_h-W_h A_h, W_h*R_h=0,
R_h*R_h=W'_h*W'_h-A_h*A_h.                              (9)
```

The global calculus, all actual output jets and the whole-band CFL
bound epsilon_h G_h<=C imply

```text
W'_h*W'_h<=C epsilon_h G_h,
||A_h u||<=C epsilon_h ||G_h u||.                        (10)
```

Indeed the blank derivative is epsilon_h times an order-2 operator,
while every nonblank derivative is sqrt(epsilon_h) times order 1.
For its squared norm the blank term epsilon_h^2 G_h^2 is bounded by
C epsilon_h G_h. In A_h the products are epsilon_h order 2 plus
epsilon_h^2 order 4, which is bounded by epsilon_h times order 2
using the same whole-band estimate. Bounded epsilon'/epsilon terms
have these orders as well. These are global graph/form bounds, not
frozen pointwise Kraus identities.

Differentiate the n-round pure state. Split each insertion of W'_h
into W_h A_h and R_h. Two innovation insertions at different times
are exactly orthogonal: cancel identical future isometries; at the
later insertion the cross factor is W_h*R_h=0, regardless of previous
record/reference entanglement. The drift terms need not be orthogonal;
use the triangle inequality. If E_m bounds Tr G_h^m rho_h,j over the
fixed time interval, the actual normalized purification derivative
Xi_h,n therefore obeys

```text
||Xi_h,n||<=||Xi_h,0||+C sqrt(T E_1)+C T sqrt(E_2).      (11)
```

No record enumeration, environment decoder or erasure is used. The
literal finite tape basis is fixed while differentiating, including
when an actual smooth clock changes the jump amplitudes. We do not
differentiate moving boundaries of a waiting-time embedding.

## 5. Energy bounds the small-eigenvalue logarithms without a spectral floor

For any state rho with Tr G rho<=E, set p=3/4. In an eigenbasis of rho,
write g_j=<e_j,G e_j>. Scalar Holder gives

```text
Tr rho^(3/4)<=E^(3/4) [sum_j g_j^(-3)]^(1/4)
             <=E^(3/4) [Tr G^(-3)]^(1/4).               (12)
```

The second inequality is scalar Jensen in the spectral measure of G,
summed over an orthonormal basis. Tr G^(-3) is finite on the 4-torus
with finite 16*128 multiplicity. Finite energy makes every g_j with a
nonzero eigenvalue well-defined. Thus (12) needs no full rank, spectral
floor or chosen inverse on the kernel.

For any actual purification Psi of rho, functional calculus and the
scalar estimate

```text
x log^2(1+z/x)<=C z^(1/4) x^(3/4), x,z>0,
```

give the uniform logarithm tail bound

```text
||[(log rho-log(rho+zI)) tensor I]Psi||<=C_E z^(1/8).    (13)
```

The kernel contributes zero because Psi has no component there. This
also follows from uniform higher log moments; (13) gives a useful
explicit regularization power.

## 6. Complete coherent-entropy first sources converge, including rank births

Let rho_h(T) be the actual final system/reference state and eta_h its
state source. Its purification derivative Xi_h is the actual one in
(11). Define the finite first source by the regularized pairing

```text
g_h=-lim_(z down to 0) Tr eta_h log(rho_h+zI).
```

It is a true derivative, not an assumed unbounded trace product. To
see this, use f_z(x)=-integral_0^x log(t+z)dt, so f_z(0)=0 and
Tr f_z(rho)->S(rho)+1 uniformly under (12). Its derivative along the
normalized purification is
-Tr eta log(rho+zI)=-2Re<Xi,[log(rho+zI) tensor I]Psi>.
Equation (13) gives uniform convergence of these derivatives. The
fundamental theorem then proves entropy is C1, with that source,
even when new eigenvalues are born.

Now use r=0 in (8): a uniform third initial moment, converging initial
state tangent and bounded normalized initial purification tangent
suffice. The lower moments in (11) are automatically controlled.
At every fixed z>0, rho_h->rho in trace norm and eta_h->eta in trace
norm imply

```text
-Tr eta_h log(rho_h+zI) -> -Tr eta log(rho+zI).
```

Functional calculus is bounded here. Equations (11)–(13) bound the
regularization error by C z^(1/8), uniformly in h and locally in s.
Consequently

```text
g_h -> g=-lim_(z down to 0) Tr eta log(rho+zI).           (14)
```

The regularized limiting sources are continuous in s, and their
uniform limit g is continuous. Entropy values already converge; pass
finite-h fundamental theorems to the limit to prove the limiting
entropy is genuinely C1 with derivative g. No strong convergence of
Xi_h, fixed support, Choi compression or continuous tape embedding is
needed. For the actual pure normalized input, Schmidt equality makes
this the first source of the **complete coherent record entropy**.
The natural-log units convert to phi units by division by log(phi).

This is a first-source theorem. A rank birth proportional to s^2 can
produce -s^2 log(s^2); its first derivative is continuous, while its
second derivative diverges. No second-source theorem follows here.

## 7. Actual original port and supplied code sources converge

Take r=1 in (8). A uniform fourth initial moment and initial tangent
convergence in S1,1 give eta_h->eta in S1,1. Any supplied fixed per-round
code has the exact expectation from the previous owner,

```text
C_h=n ell_0+epsilon_h sum_(j<n) Tr A_c,h rho_h,j,
A_c,h=sum_alpha(ell_alpha-ell_0) elljump_alpha,h*elljump_alpha,h.
```

The original 127 physical outputs are used here, including the special
blank-label/port1 term. Both A_c,h and A'_c,h are uniform order-2 forms,
and their bounded-energy block limits follow from the actual jet
consistency. Weighted trace convergence controls their full pairings.
Thus at fixed native clock and fixed supplied code,

```text
d(C-n ell_0)
 =integral_0^T [Tr A'_c rho(t)+Tr A_c eta(t)]dt.          (15)
```

For an actual supplied clock jet one may either keep kappa in (8) and
add kappa Tr A_c rho to the integrand, or use the fixed-time eta in
(15) and add T' Tr A_c rho(T). These are the same formula by integration
by parts. Do not include both clock contributions twice. If the given
code lengths themselves change, include their true derivatives in
A'_c and the explicit baseline n ell'_0; it need not have a finite
refinement limit and is not silently discarded.

For the original golden port code A_c=p Delta, hence

```text
d(C_port-n)=p integral_0^T
              [Tr Delta' rho(t)+Tr Delta eta(t)]dt,     (16)
```

with the same clock endpoint term when supplied. The factor p is fixed
by the original gate/code. Total-exit first sources have the analogous
formula without p; the finite-step epsilon Delta^2 correction and its
first derivative vanish using the available fourth moment and weighted
state-source bounds. In particular epsilon_h Delta_h^2 is bounded as
an order-2 form and tends strongly to zero on every fixed energy block;
strong S1,1 convergence of eta_h then controls its pairing with the
signed tangent. Bounded tangent norms alone would not justify this
last limit. These are actual code/count sources, not fitted
stress tensors.

For any already specified coherent Cost-Info contract, (14) and (15)
now supply both first-source components on this same process. They do
not select that physical contract or supply missing history-dependent,
ensemble, calibration or workspace terms.

## 8. Boundary and next consuming source equality

The source covectors above are defined on uniformly smooth controlled
field/preparation charts, with all original components and jets. Moment
and tangent convergence are stated analytic hypotheses, not newly
forced physical admission. A preparation family may have converging
values and all spatial moments while its parameter jets oscillate;
its derivative cannot be inferred from the value theorem alone.

The actual native-history/test/Info/code law and full ensemble/workspace
price remain with the physical morphism programme. Their admitted full
first source must then be compared to the intrinsic nonlinear Einstein
covector, including all matter and retained equations. This theorem
does not replace those equalities or create a compatible joint root.

The parallel [complete preparation descent](A4D_COMPLETE_RECORD_PREPARATION_DESCENT.md)
solves a complementary consuming block: for a supplied coherent code
on the actual eight-momentum shell it gives a unique interior observable
preparation, a quantitative information Hessian and its genuine envelope/
Schur source. Use that retained preparation derivative when the declared
price and admitted preparation variations match. Do not freeze it or
transfer its finite-shell positive Hessian to the growing spatial
carrier without proof. Invisible intermomentum/reference data and the
other retained equations are not eliminated by that block.

The original fixed nonconstant g, independent tau, all 10 packed rows,
unweighted raw h^-2/#216 terminal remains open: controlled smooth
M'_h=O(h) tests do not give a raw rough-link or all-grid source norm.

The [bounded actual first-jet controls](sources/d0_variable_record_first_source_2026-10-17/README.md)
check the full 128-output isometry/innovation and 64-row generator
derivative. The weighted evolution and logarithmic source limits are
analytic proofs above, not extrapolations from the finite fixture.
