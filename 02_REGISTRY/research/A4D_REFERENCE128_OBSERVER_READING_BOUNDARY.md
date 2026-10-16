# Reference128 observer reading: exact correlation and regular centering boundaries

16 October 2026. Same Draft #334, scientific input `a4f4d4e8`.
Consumer: the full-reference observer-law gap in
[causal metric/source bridge](A4D_NATIVE_CAUSAL_METRIC_SOURCE_BRIDGE.md).
No action, reference orientation, preparation law, or native selector is added.

**Result.** An explicit correlation uses the full128 reference through the
faithful-to-balanced rank path. Its native gate/price-cut pointer is exact,
but the required reference tensor is not selected by the existing programme.
The proposed observer-alignment inverse has rank0 on that whole path.
Norm centering instead has rank3 and a unique coercive centre there, but
leaves the causal cone fibre intact. Thus neither calculation closes the
native causal/source row.

## 1. Owned operators and what reference128 currently supplies

Use the actual ACDB-order creators from
`certificates/a4d_native_curved_soldered_heat.py`, not an unannounced Jordan–Wigner
order. All16 occupation states and grades `1,4,6,4,1` remain. Set

```text
beta_i=C_i+C_i*,        {beta_i,beta_j}=2delta_ij I16,
H_j=Gamma(B_0j)=C_0 C_j*+C_j C_0*,    H_j*=H_j.           (1)
```

The actual full Fock golden gate and price cut give a concrete pointer:

```text
Z_n=2P_n-I,
U_n* Z_n U_n=p^3 Z_n-2ap beta_n,
beta_n=(p^3 Z_n-U_n* Z_n U_n)/(2ap), a^2=p, p+p^2=1.      (2)
```

The new checker extracts only `record_basis` and the literal `U/P/T`
matrix assignments from the owned Fock source; it does not execute its
controls. Equation(2) holds on all16 components, including both native
two-dimensional record branches. It is a gate/cut readout identity, not
an admitted transfer of that tuple to a separate reference register.

The [v8 owner, §4](sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md)
retains reference128 and identity action on it. The existing
[reference/memory owner](A4D_NATIVE_REFERENCE_MEMORY_PREPARATION.md)
and [correlated-current owner, §3](A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md)
retain their specific apparatus/observer inputs. None of these statements
selects `K_ref=I8 tensor beta_0^T`, initializes eight copies of the tuple
there, or derives a joint reference measurement. The latter current uses
`beta_u gamma_v` and already requires retained u; it is not the readout below.

## 2. An exact conditional correlation on the same128 reference

For a purification map `C:R->H`, `N=Tr C*C`, and a **given** Hermitian
right-reference tensor K, define

```text
q_i=Re Tr(C* beta_i C K)/N.                              (3)
```

In ket-vector notation the joint observable is `beta_i tensor K^T`.
This convention matters under complex reference changes. The positive
pairing and all reference/workspace factors remain; no marginal replaces
the full matter state or its price.

Let `chi=(mask0+mask1+mask14+mask15)/2`, `P=chi chi*`. Then
`beta_0 chi=chi`. For `0<=theta<=pi/2`, put

```text
a=cos(theta)/4,
b=sqrt(cos(theta)^2/16+sin(theta)^2),
C_theta=a I16+(b-a)P,
C_theta C_theta*=cos(theta)^2 I16/16+sin(theta)^2 P.       (4)
```

This is a smooth amplitude curve even at the rank-loss endpoint (extend
the signed cos, rather than inserting an absolute value). Since
`[C_theta,beta_0]=0`, K=`beta_0^T` gives exactly q=e0. For all eight shell
momenta use

```text
C_total=I8/sqrt(8) tensor C_theta,
K_ref=I8 tensor beta_0^T.                                (5)
```

The physical shell dimension and reference dimension are both128.
The ranks are128 in the interior and8 at the balanced endpoint. No
seventeenth slot per momentum,136-dimensional reference, discarded
column, or removal of rank-birth variations is used. The explicit new
128-by-128 fixture checks the normalized correlation in(5).

## 3. Full derivative, covariance and the failed observer inverse

In the fixed whitened Hilbert convention,

```text
delta q_i=2 Re Tr delta C*(beta_i C K-q_i C)/N
          +Re Tr C*(delta beta_i) C K/N
          +Re Tr C*beta_i C(delta K)/N.                  (6)
```

With moving pairings, their actual whitening jets belong to delta C,
delta beta and delta K; they cannot be frozen. Under
`C->U C V*`, `beta_i->U beta_i U*`, `K->V K V*`, the reading transforms
with its vector frame. Keeping K fixed while changing the physical
reference frame is another experiment. Overall sign of the eventual
unit covector does not select a future.

For K^2=I, the joint Clifford Gram is `delta_ij-q_i q_j`.
At(4), q=e0, its rank is3, with explicit full-amplitude transverse lifts
`delta C=(1/2)sum_(i>0)delta q_i beta_i C K`. This establishes a regular
**matter** constraint. It does not establish an observer inverse.

Indeed hold the RAW C_theta fixed and vary the observer by a boost01:

```text
n(r)=(cosh r,sinh r,0,0), L(n)=exp(-r B01),
w=Lambda(L(n))C_theta,
Tr w*w=cosh(r)^2,
Re Tr w*beta_i w K=delta_i0 cosh(r),
q(r,theta)=(sech r,0,0,0).                              (7)
```

These are full16 identities on the entire rank path. Spatial rotations
give the same result for every boost direction. Normalized q is e0 for
every n: the observer-alignment Jacobian has rank0. Asking additionally
q0=1 selects a quadratic maximum with zero differential at r=0; it is
not a regular C1 inverse and would be a new singular selection condition.

An intrinsic covector `q_form(G,C_form,K)` can nevertheless define the
NEW joint constraint `a=q_form/||q_form||_(G^-1)` and `g=-G+2aa^T`
where q_form is nonzero. This would fix the cone at fixed output data.
It is distinct from selecting n as a function of fixed raw preparation,
and remains conditional on actual K, its readout and the constraint law.
Its source requires(6) and the full normalized-reflection chain rule;
one cannot substitute the old independent-observer amplitude equation.

## 4. Norm centering is regular and coercive on this path

Consider the separate proposal to centre the complete density by

```text
N_C(n)=Tr C* Lambda(h_n) C,
<H_j>_(Lambda(L(n))C)=0.                                (8)
```

At rest, on every state(4),

```text
<H_j>=0,
Re <H_i H_j>=delta_ij/2,
D_(boost_l)<H_j>=-delta_jl.                             (9)
```

Thus the centre has a genuine rank3 observer Jacobian, unlike(7).
Along any observer boost of rapidity r, exactly `N_C(n)=cosh(r)^2`.
It is coercive, with a unique centre line; its log has radial second
derivative `2 sech(r)^2>0` and positive transverse Hessian. No uniform
global lower Hessian bound as r->infinity is asserted.

More generally a hyperbolic geodesic in an adapted Lorentz frame gives
`N(t)=A exp(2t)+B+C exp(-2t)` with nonnegative weights. Log norm is
geodesically convex; strictness/coercivity need their own nonvanishing
spectral-weight conditions. On(4) the weights are exactly1/4,1/2,1/4.
Under a simultaneous Lorentz change of raw C and n, the norm is unchanged,
so a unique centre transports covariantly. Rank-deficient states outside
this domain can have stabilizers and nonunique centres.

## 5. A regular centre still leaves the causal cone undetermined

Keep G=I and the SAME coordinate-form preparation, choose `e=O01(phi)`,
`n=e0`, and `C_native=Lambda(e^T eta)^-1 C_form`. Then
`g=e^T eta e` varies through genuine nongauge Lorentz-cone directions.
For faithful `C_form=I16/4`, native reduced density is still I16/16.
Consequently (8) has the same unique centre n=e0 for every phi. All
three causal directions survive at fixed `(G,C_form)`.

The balanced path does not rescue the rule locally. With
`t=sin(theta)^2`, the centering Jacobian on this co-transformed cone
family is exactly

```text
-diag(1,1-t sin(phi)^2,1-t sin(phi)^2).                  (10)
```

It remains invertible near phi=0, while g changes. Thus regularity of
the observer inverse in RAW coordinates does not imply reconstruction
of g from the factorized positive data.

A reference-unitary-invariant reading of the full purification depends
on reduced density. At faithful density, positive SO(4) fixes that data
and has no nonzero fixed covector. This is the precise stabilizer domain;
an existing g/eta/observer or a retained reference tensor is extra input,
so this is not a universal D0 obstruction.

The alternative signed Choi matrix `C1 K_eta C1*` reconstructs eta on
the faithful first-grade Choi block. At the balanced endpoint C1 has
rank1, so this matrix has rank<=1 and cannot remain a Lorentz metric.
The fixed signed reference tensor also requires its own native provenance.

## 6. What is and is not selected by the existing price

H+J+R is homogeneous in the preparation amplitude. A minimum of N_C(n)
is not a minimum of that price, and its scalar normalizer cannot be
reinterpreted as an extra norm penalty. Even preparation criticality on
a scalar occupied shell does not force(8): an H1-eigenvector can be a
valid shell amplitude while having nonzero <H1>. Conversely centering
does not solve the full field equations. No general implication from
the native joint EL to(8) is proved here.

The useful pointer is(2): physical beta_n is already an exact readout
of existing gate/cut data. The remaining concrete arrow is an admitted
same-history initialization/transport of the required reference tensor,
its full joint observable, and the corresponding source law. Neither
an arbitrary reference column, assumed tomography, norm minimization,
nor an added action term supplies that arrow.

## 7. Bounded evidence

[New helper and immutable output](sources/d0_reference128_observer_2026-10-16/)
pin the creator/gate definitions and reference contracts. Only the new
exact small calculation is run normally and with Python optimization;
all mathematical gates use explicit exceptions, not removable asserts.
No old entrypoint, old root/heat/Hessian suite, receipt generator or
Lean build is executed. No native observer law, physical admission,
joint-root classification, refinement or GR terminal is promoted.
