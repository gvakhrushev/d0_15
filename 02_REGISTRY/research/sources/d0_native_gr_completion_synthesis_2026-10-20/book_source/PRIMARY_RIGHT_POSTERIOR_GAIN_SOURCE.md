# Intrinsic RIGHT prior and actual primary posterior gain

21 October 2026. Existing Draft
[#334](https://github.com/gvakhrushev/d0_15/pull/334), input
`0db4b499c307ae3fee11d6a6f71722cf7b8b6b81`.
Phase: native realization; `native-programme-v1`.

Consumer: [the actual record-price application](PRIMARY_CAR_RECORD_PRICE_SOURCE.md),
and [the parent](TWO_NATIVE_8D_DETERMINANT_SOURCE.md), §13. The missing
application was a reference and posterior map on the original material
experiment, required before applying the owned operational-gain theorem.
The actual oldRIGHT128 supplies this map. Its interpretation as compulsory
Book Info and the full absolute price remain additional premises.

## 1. Fixed inputs and the changed mathematical object

Keep the original L4 regulator, h=1/4, all256 sites, all16 CAR grades,
oldRIGHT128, actual cost20 density, REST order, positive shifted adjoint
and original complete one-round128-outcome instrument. Keep the local
quadratic primary family and actuator from
[the preparation owner](PRIMARY_CAR_PREPARATION_SOURCE.md):

```text
p=phi^(-1), sigma=p^3, B_*(u)=u(u-1/4), b_x=t B_*(u_x), c_x=0,
m_x=sqrt(p)|1>+b_x|15>+sqrt(p^2-b_x^2)|14>,
C_(x,grade),a=f_a(x)m_x/sqrt(128), w=(1,1,2,2).
```

The columns f_a are the actual128 orthonormal real characters. Pointwise
||m_x||=1 gives the exact identity C_t* C_t=I_128/128. At w, b_w=0 and
the14/15 actuator tangent is p|w,15> f(w)^T/sqrt(128). The full exterior
operator and its complement remain present. The continuous angle labels
the circle containing the actual finite Golden returns; it is not an
extra exact-angle primitive.

The previous pointer calculation used q_gamma=||K_gamma C_t||_HS².
The earlier33-Gram spectral calculation flattened DATA×RIGHT in each
branch. Here retain each full128×128 RIGHT matrix instead:

```text
Z_gamma=K_gamma C_t, B_gamma=Z_gamma* Z_gamma,
q_gamma=Tr B_gamma, sum_gamma B_gamma=I_128/128.              (1)
```

This is a new application of the owned gain theorem to an existing
reference carrier, not another choice of an entropy on q alone.

Immutable analytical owners at the input commit:

| Input | Git blob |
| --- | --- |
| [Primary Fourier preparation, §§2–3](../../../A4D_MICROHISTORY_EINSTEIN_QUOTIENT_AND_PRICE_EULER_UNIVERSALITY_2026_10_18.md) | `44e9fb42df728b2b4a9f70615e1c55bcda984886` |
| [Original full channel and port effect](../../../A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md) | `df8611c7fa37fa71e883831b3f01f434532d99ce` |
| [Operational gain, theorem1](../../d0_operational_gain_2026-10-15/RESULT.md) | `c1b96688e2a263bf8c3ff333a9e8ee9cb91f255a` |
| [Full128 amplitudes and source regularization](../../d0_primary_full128_information_source_2026-10-20/RESULT.md) | `dc22cc51ecea386ecfb8cb8f39c83541f4299750` |
| [Pinned outward interval definitions](check_primary_car_pointer_source.py) | `70ec8c7273de251766b4796d1562a116d19eb8c6` |

The executable pins the interval definitions and all five inherited raw
inputs by SHA-256 before calculation. It imports their definitions only.

## 2. The actual prior, posterior and gain

Write the normalized pure input as
|C_t>=sum_(i,a) C_(i,a)|i>_DATA|a>_RIGHT. Taking the DATA partial trace
of each full branch gives B_gamma^T. Transposition follows this
vectorization convention and preserves spectra. On the declared
classical pointer cut the actual joint state is therefore

```text
Omega_YR=direct_sum_gamma B_gamma^T,
rho_R=I_128/128, rho_(R|gamma)=(B_gamma/q_gamma)^T.          (2)
```

No operation on RIGHT is needed to define (2). Equation(1) supplies
the prior independently of a statistical ensemble over t or geometry.
The resulting quantum/classical mutual information is

```text
I_phi(R:Y)=sum_gamma q_gamma
              D(B_gamma/q_gamma || I_128/128)/ln(phi)
         =log_phi(128)-sum_gamma q_gamma S_phi(B_gamma/q_gamma).
                                                               (3)
```

Here D uses natural logarithms; terms of probability zero have their
continuous value0. Apply the owned central-prior theorem separately
to every conditional RIGHT state: its maximum measured gain over all
POVM on M_128 equals the corresponding D/ln(phi). Averaging those
maxima gives (3). Attainment requires gamma-dependent spectral POVM
on the protected RIGHT carrier. Algebraic optimization proves their
mathematical existence; native physical admission or their compulsory
execution is not supplied here.

The exact value bounds and zero criterion are

```text
0 <= I_phi(R:Y) <= min(log_phi(128), H_phi(q)),
I_phi(R:Y)=0 iff B_gamma=q_gamma I_128/128 for every gamma. (4)
```

Indeed B_gamma<=I/128. For q_gamma>0, every eigenvalue of
128 B_gamma/q_gamma is at most1/q_gamma, so its relative entropy is
at most-ln(q_gamma). Positivity and its strict equality criterion
give the other statements. Forgetting fine labels is a channel;
I(R:full pointer)>=I(R:port). This comparison concerns values and
does not order their derivatives.

This removes the unspecified-prior premise on this particular RIGHT
cut, conditional on the supplied C_t. It does not prepare C_t from a
fixed complete native input or choose a material inference task. A
classical extension of the same pure DATA–RIGHT input factorizes:
every positive-weight conditional state with that pure marginal
equals |C_t><C_t|. Consequently a hidden F/R label using the same
K_gamma cannot supply a nontrivial alternative input ensemble without
an actual changed preparation or controlled instrument.

## 3. An exact positive witness on the actual unequal density

The full port1 effect is p epsilon Delta, epsilon=p²h²/64 and
Delta=D*D=D² for the original self-adjoint D. At t=0 put

```text
a_z=sigma sqrt(rho_z), A=sum_z a_z²,
T_x=sum_z a_z a_(z-x)>0, S=256, m_0=sqrt(p)|1>+p|14>.
```

Use the actually selected complex characters k=(0,0,0,1) and
k'=(0,0,1,1) as an analytical rewriting of the original real
cosine/sine pairs. The transverse spatial role x=2 has squared
creation and annihilation norms p and p² on m_0. Its output vectors
are orthogonal to all other role outputs. For normalized complex
characters phi_k its energy contribution is

```text
[2p A(1-cos(k_x*pi/2))+2p²(A-T_x cos(k_x*pi/2))]/(S h²).
```

All other role contributions are independent of k_x. Thus

```text
||D(phi_k' m_0)||²-||D(phi_k m_0)||²
                  =2[p A+p² T_x]/(S h²)>0.                (5)
```

A real cosine/sine pair trace is twice the complex-character energy.
The traces on the two actual two-column principal RIGHT blocks of
B_port1=p epsilon C_0* Delta C_0 differ by

```text
4p epsilon [p A+p² T_x]/(128 S h²)>0.                      (6)
```

Hence B_port1 is nonscalar; (4) gives strict positive port gain and
strict positive full-pointer gain. No eigensolver or equal-density
substitution is needed for this witness. Finite-dimensional entropy
continuity transfers strict positivity to a sufficiently small
nonzero primary t. The complex notation in this proof adds no RIGHT
gate, measurement or physical preparation.

## 4. First source, with posterior support retained

For every admitted tangent in the same instrument, retain both jets:

```text
DZ_gamma=(DK_gamma)C_t+K_gamma DC_t,
DB_gamma=DZ_gamma* Z_gamma+Z_gamma* DZ_gamma.               (7)
```

On a constant-support chart with the fixed prior in(1), differentiation
of Tr B log B-q log q gives

```text
DI_phi(R:Y)=sum_gamma Tr[DB_gamma log(B_gamma/q_gamma)]/ln(phi).
                                                               (8)
```

Positive q_gamma alone does not justify (8) across a posterior rank
change. For a support-uncontrolled tangent the owned amplitude
regularization supplies a separate safe boundary. With M=128,N=128,
Q²=sum_gamma ||DZ_gamma||_HS² and the owned entropy regularizers,

```text
I_eta=[ln N+H_eta(q)-S_eta(direct_sum B_gamma)]/ln(phi),
|I-I_eta|<=MN eta/ln(phi),
|DI-DI_eta|<=4 sqrt(M eta)(1+sqrt(N)) Q/ln(phi).             (9)
```

All kernels and zero outcomes remain in(9). These are approximation
bounds; floating arithmetic error must be bounded separately.

For the actual local angle tangent, write C_t=C_0+t C_B+O(t²), where
C_B(x,a)=B_*(u_x)f_a(x)|15>/sqrt(128), and
V=|w,15> f(w)^T/sqrt(128). Then DC_t=pV. Each original Kraus row has
fixed CAR parity; C_0 has odd parity and C_B,V have even parity.
The original geometric D_t and Julia maps are even analytic in t.
Consequently B_gamma(t) is even, and

```text
d_theta B_gamma(t)|0=t R_gamma+O(t³),
R_gamma=p[(K_gamma C_B)* (K_gamma V)
                     +(K_gamma V)* (K_gamma C_B)] at t=0. (10)
```

Exactly64 dark Walsh outcomes are structurally zero. The certificate
below proves all remaining64 posterior matrices strictly positive at
t=0. Their support persists on a nonempty small-t chart. Equations
(8)–(10) therefore yield an actual odd analytic angle source

```text
d_theta I_phi(R:Y)|0=i_1 t+O(t³),
i_1=sum_gamma Tr[R_gamma log(B_gamma(0)/q_gamma(0))]/ln(phi)>0.
                                                               (11)
```

This is a local nonvacuum source conclusion. No numerical t_* or
particular finite actuator word is asserted by the leading-jet check.
The coefficient uses the complete declared periodic-storage L4 fixture:
the posterior logarithms depend on that full experiment. It does not
inherit the earlier local Rayleigh stencil's independence of an exterior
completion, or assert the same coefficient on every refining mesh.

## 5. Verified full-fine calculation

[The new checker](check_primary_right_posterior_gain.py) constructs
all C_0,C_B and the bare |w,15> columns through the literal analytic
Julia defects, original full Dirac and original Walsh/Fourier maps.
The nonblank port pair has exact proportional matrices B_0=p B_1
and R_0=p R_1, hence identical normalized posteriors. It computes33
distinct matrices with their exact multiplicities, retaining all64
active physical outcomes and all64 exact structural zeros.

An eigensolver proposes an orthogonal basis O and positive diagonal
Lambda. Its accuracy is not assumed. Outward interval products bound
delta>=||O^T O-I||_op and the reconstruction residual. For delta<1,
the exact polar orthogonal Q obeys

```text
||Q-O||_op <= d=delta/(1+sqrt(1-delta)),
||O||_op <= sqrt(1+delta),
epsilon>=||B-Q Lambda Q^T||_op,
epsilon=||B-O Lambda O^T||_F
                  +(2 sqrt(1+delta)d+d²)||Lambda||_op.
```

The checker verifies lambda_min-epsilon>0 separately for every
representative. The integral resolvent formula for the matrix logarithm
then gives

```text
||log B-Q log(Lambda) Q^T||_op
                         <=epsilon/(lambda_min-epsilon). (12)
```

Adding the polar-basis error for log(Lambda/q) bounds the use of O
in the trace source. The rank-two form R=p(c r^T+r c^T) gives
||R||_1<=2p||c||_2||r||_2. The trace error is this nuclear-norm
bound times the operator-log error. Interval R entries and scalar
logs are included in the computed trace itself.

Center-radius matrix products use a componentwise gamma_(2k) dot
bound, including underflow, under the explicit IEEE binary64
nearest-arithmetic/no-flush-to-zero premise. The direct NumPy einsum
contraction is treated as a sum of k binary64 products with at most
k-1 additions in any order, optionally FMA. Runtime canaries check
format, rounding and subnormals. Scalar square roots are bracketed
by exact rational squaring; scalar logs use exact rational atanh
tails. No probability floor, eigenvalue floor or library-log accuracy
assumption enters the certificate.

The author enclosure of i_1 is
`[2.1910472674029542e-9,2.1910477557180062e-9]`.
Every active fine posterior has certified minimum eigenvalue greater
than `1.8599583513003547e-13`. These are unnormalized B_gamma
eigenvalues; all128 posterior eigenvalues are retained in every active
branch. The independently aggregated known port cost coefficient is
`[-2.7461810898740312e-8,-2.746181089819066e-8]`. Subtracting the gain
gives `[-2.965285865445832e-8,-2.965285816559361e-8]`.

The [frozen validation receipt](PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE_REVIEW.md)
records independent replay, hostile mutation and exact provenance.
The primary conclusion is the strict sign in(11), not a floating
estimate of posterior rank.

## 6. Parent substitution and the remaining physical binding

Parent §13 now has an actual prior/posterior map on oldRIGHT and can
apply the owned central operational-gain theorem without inventing
an ensemble over material fields. It also has the previously missing
one-round full-fine preparation source for this gain observable.
This source has the opposite sign to the pointer entropy source.

Conditionally assigning Info=I_phi(R:Y), Cost_port=1+p epsilon R
has coefficient c_1=-p epsilon a_R<0, where a_R is the Rayleigh
coefficient from the preparation owner and epsilon=p²h²/64. Hence

```text
d_theta[Cost_port-I_phi(R:Y)]|0=(c_1-i_1)t+O(t³)<0          (13)
```

for sufficiently small positive t. This is the stated known price
component. Nonuniform complete code prices, the actual absolute Book
normalizer, required work and genuine upstream preparation equations
remain in the full action. A scalar paid word mark has zero angle
source within its declared fixed-word chart; its positive value and
comparison between different word counts remain. Neither(11) nor(13)
proves a decrease of the complete paid programme.

The precise application is supporting native-programme-v1 research:
the original preparation supplies the reference on this cut and the
actual channel supplies its conditional gain/source. Book03 Info
selection, physically available RIGHT tests, the same-initial native
preparation/field/controller graph, full-price selection, later history,
refinement and original raw216 are retained. No positive GR acceptance,
task retirement or new physical selector is introduced.
