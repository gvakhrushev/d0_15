# Full causal principal source in the retained Julia history

17 October 2026. Same Draft #334. Consumer: Front A's retained-program →
geometric-source arrow. Inputs are the [actual first-exit
owner](A4D_RETAINED_HISTORY_CAUSAL_SOURCE.md), [causal metric
bridge](A4D_NATIVE_CAUSAL_METRIC_SOURCE_BRIDGE.md) and [intrinsic coframe
reconstruction](A4D_COFRAME_TORSION_INTRINSIC_GR_RECONSTRUCTION.md), at
`5299ddf1bf0e81b28252acf9f2729b1947cc3292`.

**Constructive result.** The three existing nonblank role records have a
specific coherent combination whose continuum quadratic response equals a
calculated multiple of the Einstein-Hilbert response on **all three** causal
cone fields near the flat cone. No scalar reweighting of their three
diagonal probabilities gives that response. Among positive detectors on
these three labels, the coherent direction is unique up to scale if its
principal response must vanish on every longitudinal gauge probe.

This specifies an observable on the existing retained register. It does
not derive its physical detector, preparation or price. In particular,
the factor `1/sqrt(3)` is not an already implemented native readout gate.
The result is a full three-field principal identity, not the nonlinear
ten-metric Einstein equation or the original fixed-source/raw terminal.

## 1. Complete local jet, without losing form grades

On the period2pi torus take `e=s O`, `s>1`,
`O=exp(epsilon sum_(a=1)^3 theta_a R_0a)`, with the same true LC links,
positive metric `G=s^2 I`, natural measure and coordinate-form matter as
the existing owner. All16 occupation states and all128 first-shell
reference columns remain. The fixed positive coordinate-form Hilbert-frame
creators are `c_r/s`;
write `i_r=c_r*`, `gamma_r=c_r-i_r` and
`Gamma(M)=sum_ab M_ab c_a i_b`. Set `X_ra=partial_r theta_a`,
`B_ia=X_ia` for spatial indices. At epsilon=0 the complete covector LC
connection `M_r=-omega_r^T` has first coefficient

```text
M_0=2 sum_a X_0a E_0a
    +sum_(a<b)(B_ab-B_ba)(E_ab-E_ba),
M_i=sum_a [(B_ia-B_ai)E_0a-(B_ia+B_ai)E_a0].          (1)
```

`E_ab` are matrix units. Each occurrence of a spatial rotation in (1)
includes **both** matrix units. Define

```text
Z_r=c_r Gamma(M_r),  J_r=Z_r+Z_r*,
sum_r Z_r=0, sum_r J_r=0.                             (2)
```

The first-jet linear map `X -> (Z_0,...,Z_3)` has precisely the six
off-diagonal spatial entries as its image coordinates. Its kernel is
`X_01,X_02,X_03,B_11,B_22,B_33`. The temporal pieces contain `c_0^2`
and the diagonal pieces contain `c_i^2`, hence vanish by CAR. Every
off-diagonal pair is retained. This is an operator calculation on the
full16 carrier, not a scalar-trace cancellation or a claim of complete
geometric tomography.

At the flat germ, `delta P_r=h Z_r/s+O(h^2)`, while `delta C_r=0`
in the fixed positive coordinate-form frame. Thus the same leading
kernel holds for **all** word/coefficient Julia blocks, not just the
selected role outputs. For `R_L=sqrt(I-PP*)` its derivative satisfies
`R_L delta R_L+delta R_L R_L=-(delta P P*+P delta P*)`, and similarly
for `R_R`. The strict contraction margin `s>1` makes the Sylvester
operator invertible, so `delta P=0` implies both derivatives vanish.
SELECT and the Walsh matrix preserve this conclusion. At norm1 the
square-root argument fails. Nor may an `O(h^2)` one-round remainder be
discarded through `O(h^-2)` rounds: there is no all-orders or finite-history
invisibility theorem here.

This uses the covariant coordinate-positive representation throughout:
preparation and form outputs are transported with the frame, as in the
input owner. The endpoint frame derivative is already included in (1).
A raw native-basis derivative contains additional representation
commutators; they cannot be dropped while freezing the old detector or
preparation. No such mixed-frame equality is used here.

For clarity the complete fine-row map can be written without omitting
the coefficient1 outputs. Set `sigma=(-1)^u`, `tau=(-1)^v`, where u is
the word-adjoint bit and v distinguishes P from the negative C words.
The even-duplicate Walsh output has index `role_index(chi)+2u+4v`.
With `N=Q_(blank;output)` and `L(X)=sqrt(I-XX*)`,
`R(X)=sqrt(I-X*X)`, its two coefficient blocks are

```text
N_(chi,u,v,0)=sum_r chi_r(P_r+sigma P_r*-tau C_r-sigma tau C_r*)/16,
N_(chi,u,v,1)=sum_r chi_r[L(P_r)+sigma R(P_r)
                              -tau L(C_r)-sigma tau R(C_r)]/16. (1a)
```

Odd-duplicate rows vanish exactly. Differentiating (1a), with the two
Sylvester equations above, gives every fine output jet. For a nonblank
output its two-port effect is `4p^2 A* N N* A`; its variation retains all
four ordered product terms and the preparation/normalizer variation of
the original owner. This is the complete row interface behind the
principal-kernel claim, not a replacement of the full instrument by
three probabilities.

## 2. Diagonal role probabilities are not the Einstein source

Use exactly the three owned characters, in order
`chi_1=(+,+,-,-)`, `chi_2=(+,-,+,-)`, `chi_3=(+,-,-,+)`, at actual labels
`16,8,24`. Put `J_chi=sum_r chi_r J_r`. The complete full16 trace is

```text
Q_diag=(1/16) sum_chi Tr(J_chi^2)
 =sum_(i<a) [2(B_ia+B_ai)^2+4(B_ia-B_ai)^2].           (3)
```

There is no linear signal at the flat germ on the faithful shell. For a
real Fourier amplitude `theta=v cos(q.x)`, the unaveraged spatial symbol
is `v^T P(q_sp) v`, where

```text
P_aa=6 sum_(i!=a) q_i^2,    P_ab=-2 q_a q_b (a!=b),
det P=32[6 sum_(i!=j) q_i^4 q_j^2+13 q_1^2 q_2^2 q_3^2]. (4)
```

The torus average contributes `1/2`. The rank is3 for at least two
nonzero spatial momentum components,2 on one spatial axis,0 if
`q_sp=0`; `q_0` is arbitrary. These are symbol ranks, not propagating
degree counts. The existing first-exit clock gives the diagonal sum's
quadratic contrast as
`(1-exp(-beta/s^2)) <Q_diag>/(256 s^2)`.

In the inherited curvature convention, the EH action instead has expansion

```text
I_EH[e_epsilon]=epsilon^2 I_EH^[2]+O(epsilon^3),
I_EH^[2]=-2s^2 <sum_(i<a)(B_ia-B_ai)^2>.                (5)
```

One independent derivation uses `delta g_0a=2s^2 theta_a` and
`G^(1)_0a=Delta_sp theta_a-partial_a div_sp theta`. Hence
`I_EH''(0)=4s^2 <theta.(Delta_sp theta-grad_sp div_sp theta)>`.
Integration by parts gives (5); the explicit spatial divergence is
`partial_i[theta_a(partial_i theta_a-partial_a theta_i)]`.
The EH variation also has its usual boundary term. Periodic or compact
variations remove these boundary integrals, not their interior sources.

For the static probe `q=(0,1,1,0)`, `v=(1,1,0)`, all ten linearized
Einstein rows vanish, whereas
`<Q_diag>=4`. Thus no nonzero scalar normalization repairs (3). In fact
no fixed signed linear combination of just these three diagonal role
probabilities yields a nonzero EH quadratic form: the three longitudinal
pair probes force all three coefficients to zero. Smooth functions of
only these probabilities have the same obstruction at quadratic order,
because their first cone derivatives vanish. This does not classify all
word/coefficient outcomes or all history functionals.

## 3. The required coherent observable already has a place in the register

Define the unit vector in the retained label space

```text
v_label=(|16>+|8>+|24>)/sqrt(3),   Pi_v=|v_label><v_label|. (6)
```

It is orthogonal to the complete blank. Project on (6) at the first
nonblank round, retain coefficient0 and **both** golden ports, and leave
every later round unrestricted. This is a positive coherent observable
on the existing unmeasured history. It is not a union of three classical
label events: the six off-diagonal label entries in Pi_v are essential.
An implemented measurement in this basis has not been supplied.

The first-exit algebra of the existing owner applies by linearity to
`M_v=(M_chi1+M_chi2+M_chi3)/sqrt(3)`. Exactly at finite h,

```text
E_v=4p^2 A* M_v M_v* A,
F_v,n=sum_(j=0)^(n-1) B^j E_v B^j,
A=hD_h/16, B=I-p^2 h^2 Delta_h/128.                    (7)
```

The disjoint projectors on successive first-exit times remain orthogonal;
no measurement/reset is inserted between rounds. This changes neither the
operator nor the price. In the controlled smooth matrix-element limit,

```text
h^-2 F_v,n -> (1/256) integral_0^beta
 exp(-t Delta/2) D D_v D_v* D exp(-t Delta/2) dt,
D_v=(D_chi1+D_chi2+D_chi3)/sqrt(3).                    (8)
```

Use the owned full faithful shell, `rho=P_shell/128`, `lambda=1/s^2`.
Its kinetic baseline is still lambda: the four kinetic weights of D_v
are `(3,-1,-1,-1)/sqrt(3)`, whose squared sum is4. Opposite momenta and
the full real CAR trace remove kinetic/potential cross terms.

The decisive exact identities, including all three fields, are

```text
J_chi1+J_chi2+J_chi3=4J_0,
J_0=gamma_0 Gamma(sum_(a<b)(B_ab-B_ba)(E_ab-E_ba)),
Tr16(J_0^2)=8 sum_(a<b)(B_ab-B_ba)^2,
(1/16)Tr16(J_v^2)=(8/3)sum_(a<b)(B_ab-B_ba)^2.         (9)
```

Consequently the continuum readout's quadratic contrast is

```text
L_v^[2]=(1-exp(-beta/s^2)) <|curl theta|^2>/(96s^2)
       =-(1-exp(-beta/s^2)) I_EH^[2]/(192s^4),
E_theta^[1]=-(1-exp(-beta/s^2))/(48s^2)
           (Delta_sp theta-grad_sp div_sp theta).     (10)
```

The coefficient is fixed by the actual clock and normalized projector,
not fitted to a transverse example. Formula (10) compares the entire
three-field source and its longitudinal kernel. It is a statement about
the continuum functional and its principal Hessian. The existing smooth
first-exit limit supplies its readout; no uniform raw second-source
remainder or nonflat stationary preparation is inferred.

## 4. Uniqueness within the three-label positive class

Let W be a fixed positive semidefinite operator on the three labels in
(6), with the same first-exit/port/coefficient placement. On the three
longitudinal pair probes, `J_0=0` and `J_i=-J_a`; the label-amplitude
vectors are proportional to `(chi_i-chi_a)_chi`. They span exactly the
two-dimensional plane orthogonal to `(1,1,1)`. If its principal quadratic
contrast vanishes on every such gauge probe, positivity forces W to annihilate
that plane, not merely to have a cancelling trace. Thus

```text
W=t Pi_v, t>=0.                                      (11)
```

Conversely (9) proves this detector has precisely the required curl
quadratic form. Any diagonal positive W satisfying the condition is0;
the signed diagonal obstruction in §2 is stronger within that class.
This classifies three-label detectors under a stated geometric condition.
It does not derive that condition from operational admission, classify
all128 outcomes, or promote Pi_v to a physically chosen D0 pointer.

## 5. How this is used, and what remains in the parent proof

The previous one-cone history/EH equality is not extrapolated to diagonal
probabilities. Its full principal consumer is now explicit: preserve the
off-diagonal correlations of labels16/8/24, then (10) gives the correct
three-field geometric covector. The six absent local jet coordinates in
§1 do not obstruct this particular target, since (5) depends only on the
antisymmetric spatial derivative. Full first-jet tomography would be an
unnecessary requirement for this response quotient.

The supplied scalar-weight/contorsion argument remains false for the
reasons already proved by the coframe/source owner. The present calculation
uses actual retained word amplitudes instead. It supplies a specific
coherent detector/source interface for the physical action owner, rather
than another unrestricted rank search or an added desired torsion term.

Remaining: a native realization and physical Cost−Info binding of that
coherent history reading, its actual prepared matter/observer/clock jets,
the nonlinear completion and the other metric variations, and a compatible
nonflat joint refinement family. The existing common-real-E0 winding-cone
obstruction is retained: the faithful shell used for this readout is not
thereby made stationary. No physical source term is silently added.
Front B still uses the original independent fixed g/tau, all10 packed
metric rows, unweighted raw sum, h^-2 normalization and #216 comparator.

The [bounded exact helper](sources/d0_retained_causal_principal_2026-10-17/check_principal.py)
checks the new full16 component identities and principal symbols from
pinned definitions only. Previous root, spectral and Lean entrypoints
are not executed. See its adjacent results/validation for the exact run
and review boundary.
