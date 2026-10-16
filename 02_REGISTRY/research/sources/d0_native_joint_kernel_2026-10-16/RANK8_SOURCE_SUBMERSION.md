# Pure native memory preserves all151 preparation-source rows

16 October2026. Consumer: the rank-aware continuation of the same finite
L8 conditional v8 action, after the faithful local Morse–Bott result.
The new defining calculation is
[`rank8_source_submersion.py`](rank8_source_submersion.py), API `run(repo=None)`.
It loads pinned `owned_car`/`first_jet` definitions and the existing exact
mean-slice construction. It calls no historical `run()` or root search.

The reference remains128, the occupied projector P remains rank128, all16
CAR components and all4096 thermal modes remain. The signed Q-resolvent
and the fixed price are unchanged. No physical preparation admission,
rank8 transverse inverse, nonflat branch or refinement theorem is inferred.

## 1. The actual rank8 preparation and the question being answered

Use the OWNED native/ACDB convention

```text
chi=(e_mask1+e_mask15)/sqrt2,
Pi=1_Omega tensor |chi><chi|, rank Pi=8,
rho8=Pi/8,
Omega={+/-e_r}, P=1_Omega tensor I16.
```

The positive-frame memory packet uses the opposite top sign. Its conversion
to this convention is the full `basis_phase*Lambda(eta)` map; basis_phase
is identity on masks0,1,14,15. No sign conversion is applied to only one
side of an expectation. Here all operators and chi are already native.

For F=(a-b)I+b11T, a>b>0, put c=a-b, u_r=eta F_r^T and
w_r=spatial(u_r). Write C(v),iota(v) for the full owned creators and
contractions, and Gamma(W) for their exterior infinitesimal representation.
Set

```text
t=exp(i*pi/4), lambda1=128-64sqrt2,
epsilon=lambda1*(a^2+3b^2),
K_r=diag(0,[w_r]_cross).
```

The preparation-source differential uses

```text
T8(v)=(P X_v P-epsilon1 P)|_(Pi H),
epsilon1=Tr(Pi X_v)/8,
X_v=D_l J_v+J_v D_k.
```

Equivalently one includes both Hermitian support/off-support components,
as in the rank-aware owner. Its rank equals the real rank of the normalized
amplitude source moment map. Although that target has dimension1983,
the actual native map is proved below to retain all151 independent rows.

The existing full-chart upper bounds remain valid: rank at most7 for q0,
3 for an axis transfer, and5 for a two-axis transfer. Removing three
observer and three common-spatial representations does not discard any
physical amplitude direction. The new issue is the matching lower bound
on chi, not a new symbolic census of whole field matrices.

## 2. Top-dual readouts use the full carrier

Let Omega_top=e_mask15 and let

```text
B_ij=iota(e_i)iota(e_j)Omega_top, i<j,
ordered as01,02,03,12,13,23.
```

These six vectors are orthonormal. Every X_v has even CAR parity. Therefore
its even output on `sqrt2 chi=e_mask1+Omega_top` equals its output on
Omega_top. The seven readouts `(top,B_01,...,B_23)` isolate that output;
they are witnesses inside the full16-dimensional carrier, not a truncation.
The code uses the unnormalized chi only to avoid an irrelevant common
sqrt2 in the minors and divides by2 in all squared-norm statements.

For a vector bivector write `v wedge w` in order01,02,03,12,13,23. Then
`iota(v)iota(w)Omega_top` has exactly these coefficients in the B basis.

## 3. Axis transfers retain rank3

For q=2e_i, the common-spatial representation eliminates the active
angular image. All twelve inactive coframe coordinates have J=0 on the
occupied pair k=-e_i,l=e_i. The three remaining generators are K_r,r!=i.
Since Gamma(K_r)chi=0,

```text
top-dual X_r chi = -64*(t-1) (u_r wedge K_r u_i)
```

in the unnormalized readout convention. The6x3 wedge matrix has minor
rows01,02,12 equal to

```text
2*b^5*c^4 >0
```

for i=0 and for i=1. Spatial S3 and global conjugation cover all remaining
axis representatives without rotating the observer time leg into space.
Thus the occupied rank8 preparation still detects exactly rank3.

## 4. Two-axis transfers require BOTH occupied pairs

For q=e_i+s e_j,s=+/-1, choose k=-e_i,l=s e_j. In the mean slice the
active rotations are W and -W, while two inactive stabilizers remain.
The literal ordered identity is

```text
J_W=Gamma(W)D_k+D_l Gamma(W),
T_W=2(D_l Gamma(W)D_k+epsilon Gamma(W)).
```

Gamma(W)chi=0. With beta=t^s-1, the actual top-dual7x5 matrix, divided
by64(t-1), becomes the following canonical matrix after LEFT scaling
`diag(conj(beta)/beta,1^6)` and RIGHT scaling
`diag(1/(2conj(beta)),1/(2conj(beta)),1/(2conj(beta)),-1,-1)`:

```text
W -> (u_j dot W u_i, u_j wedge W u_i),
theta_r -> (0,u_r wedge K_r u_i), r inactive.
```

Every scale is invertible for both signs. Rows `(scalar,01,02,12)` and
columns `(W0,W1,theta_r,theta_s)` have minor

```text
+2*b^6*c^4 for (i,j)=(0,1),
-2*b^6*c^4 for (i,j)=(1,2).
```

The first-pair kernel is exactly W=lambda K_i and both theta=0.
It is genuinely invisible on chi at this pair, not merely invisible in
the selected readout: W u_i=0 and Gamma(W)chi=0 imply T_W chi=0.
Dropping the second pair therefore gives rank4 and is a hostile failure.

The other occupied pair is k'=-s e_j,l'=e_i. Its literal action is

```text
T_axis chi=-2 D_l' [Gamma(lambda K_i),D_k']chi,
||T_axis chi||^2
  =4*epsilon*lambda1*|lambda|^2*||w_i cross w_j||^2.
```

Here chi is normalized. Both factors D_l' and the commutator Dirac vector
are invertible unless lambda=0: the latter has real vector K_i u_j and
square lambda1 times its squared norm. Explicitly

```text
||w_0 cross w_1||^2=2*b^2*c^2,
||w_1 cross w_2||^2=c^2*((a+b)^2+2*b^2),
```

strictly positive for every a>b>0. Thus the second pair removes the last
axis and the full transfer has rank5. This is one sign-independent proof,
not a fifth minor inferred from a sampled ratio a/b.

## 5. q0 retains rank7

Every homogeneous coframe jet gives the scalar shell entries
`lambda1 delta(G_E)_rr chi`. Centering the four independent diagonal
Gram variations gives the projector `I4-11T/4`, of rank3.

For each homogeneous link J_r(k)chi=0 and J_r(k) is Hermitian. Hence
`<chi,{D,J_r}chi>=0` at every occupied momentum: link images are
orthogonal to the scalar coframe image, not just orthogonal after a sum.
At k=e_i their top-dual bivector readout is

```text
-64*(conj(t)-1) u_r wedge K_r u_i.
```

For coefficients xi_r, set M=sum_r xi_r w_r w_r^T. The spatial Hodge
readouts equal `(M-tr(M)I)w_i` up to that nonzero common phase.
The three spatial vectors w1,w2,w3 span because their determinant is
`-c^2(a+2b)`. Vanishing readouts force M-tr(M)I=0, hence M=0.
The four readouts

```text
M12-M13, M12-M23, M11-M12, M12
```

have determinant b^4 c^4 in xi0..xi3. Thus the four link images remain
independent, giving total q0 rank3+4=7.

## 6. The real rank is151 and the amplitude boundary is regular

The shell difference support contains q0, four axis conjugate pairs and
twelve two-axis conjugate pairs. Consequently

```text
rank_real T8=7+4*2*3+12*2*5=151.
```

The full faithful T map has these same ranks and its kernel is contained
in the rank8 kernel. Centering agrees: coframe entries are scalar and the
link expectation on chi vanishes at every momentum. Hence their FIELD
kernels coincide at this particular pure-memory preparation. Generic
rank-deficient amplitudes need not have this property.

The normalized shell-amplitude sphere has dimension2*128^2-1=32767.
The151 source rows are therefore a submersion at C8. Its exact stationary
level set has dimension32616 through rank8. In particular all28800
genuine rank-birth directions are tangent to this smooth level set;
second amplitude corrections can restore their quadratic source terms.
An arbitrary uncorrected straight birth path need not stay stationary.
The explicit lift/correction and the full flat-family parametrization are
owned by [`RANK8_AMPLITUDE_FIBRE.md`](RANK8_AMPLITUDE_FIBRE.md).
Adding the already constructed24579-dimensional flat field family gives
57195 stationary amplitude/field parameters. A transverse inverse at C8
is NOT proved here, so local completeness or Morse–Bott at rank8 is not
inferred from this dimension.

For a prospective nonflat field velocity outside Omega-Omega, E1=0 and
the second matter equation remains E2 C8=0. A birth tangent C1 cannot
cancel it. For a C3 stationary curve the next equation is
`E3 C8+3E2 C1=0`. Since E2 is Hermitian, E2 Pi=0 also gives Pi E2=0.
On reference ker C8 the occupied-output part of C1 is therefore
annihilated, so the equation forces E2 D=0 for its genuine complementary
birth block D. If D has full rank120 on the complementary shell, these
two equations imply E2=0. Indeed such a birth has full-rank C(t) for
small nonzero t and the exact equation E(t)C(t)=0 then gives E(t)=0.
Thus generic full-complement rank birth restores the faithful shell
condition; it does not automatically open a geometric branch.
This is a return to the full eigen-equation, not an application of the
previous faithful local Morse--Bott theorem near I128/128. Such
preparations lie near rho8 instead; their source-dependent field Hessian
changes, and its normal inverse has not been established here.

The shortest remaining geometric test is the actual C8-dependent normal
field operator with ALL preparation equations, followed by E2 C8=0 for
any additional normal kernel. The faithful normal inverse cannot simply
be transported to this boundary. No fitted source or extra action is used.
