# Record second jet: integrated kinematic result, physical source closure open

2026-10-15. Continuation of #310, not a new execution or a retired parent.

The supplied five-file package has been preserved byte-for-byte in
[the input archive](sources/d0_record_second_jet_intake_2026-10-15/provenance.json).
Its documents are research proposals and its printed PASS/status labels are
claims to check. Their recommendations do not authorize new physical
postulates, independent tasks, temperatures, or action terms.

The useful new result is an explicit curved unitary-record germ whose
second jet has a surjective ten-slot metric variation. The thermal example
reproduces the already owned joint-limit theorem at c=1. Neither calculation
identifies the native action on this germ. In particular, the input's title
"source closure" is not adopted as a physical closure verdict.

## 1. What is integrated

| Input | Integrated use | Scope correction |
|---|---|---|
| `check_record_2jet.py` | Exact Pauli-product fixture, normalized projector jets, ten-slot normal map, curvature and controls | A free U(4) kinematic germ, not an admitted native family |
| `A4D_NATIVE_GEOMETRIC_READING_INTERFACE.md` | [Corrected geometric interface](A4D_NATIVE_GEOMETRIC_READING_INTERFACE.md) | Consistent metric/connection normalization, explicit packing and allowed normal variations |
| `check_heat_window.py` | Its original computation function, extracted without executing its file-writing tail | The hard-coded foreign output path is preserved only in the immutable input |
| `heat_window_results.json` | All nine supplied finite values compared with that function | Numerical reproduction supplements the existing analytic theorem |
| `A4D_NATIVE_RECORD_SECOND_JET_SOURCE_CLOSURE.md` | This corrected synthesis and connection to actual AF sources | Native Info, admission, stationary descent and GR remain open |

The five-file packet does not include its referenced `SYNTHESIS_RU.md`.
A second-jet synthesis with that name is available locally in Downloads;
the repository's `d0_flat_record_2026-10-15/SYNTHESIS_RU.md` is a different
flat-record document. They must not be equated by filename. The concrete
generator lists are fully specified in the supplied script, so the finite
fixture does not require an additional document.

## 2. Exact local geometry, without installing a physical family

Let p+p²=1, p>0, d=4. For a unitary germ U(x), define

```text
J_U psi = sqrt(p)|0>psi + p|1>U psi,
P_U = J_U J_U*,
<X,Y>_P = Re Tr(X*Y)/(2d),
q_mn = <d_m P,d_n P>_P
     = (p³/d) Re Tr(d_m U* d_n U).
```

The supplied Pauli matrices A_m and ten mutually orthogonal Hermitian B_mn
give H(x)=sum A_m x_m + (1/2)sum B_mn x_m x_n, U=exp(iH), B_mn=B_nm.
At zero, U_m=iA_m and
U_mn=iB_mn-(A_m A_n+A_n A_m)/2. With the **actual** projector jets,

```text
q(0)=p³ I4,  dq(0)=0,
Gamma(0)=0,
<b_mn,N_A>_P=p³ delta_((m,n),A),
R_q(0)=-6/p³.
```

The supplied script removes the common projector-jet factor p^(3/2) and
checks the resulting identities in the dimensionless metric. The consumer
restores that factor when stating q, b and the normal metric map. It does
not conflate a normalized jet with the unscaled P derivative.

For a smoothly extended normal variation N=sum f_A N_A, the induced first
metric variation at zero is

```text
delta q_mn=-2<b_mn,N>_P,
delta q_packed=-2p³ f.                                (1)
```

The extension must stay normal along the immersion and must be an allowed
variation in the declared carrier. A constant ambient perturbation specified
only at the origin does not imply (1): its derivative also enters delta q.
The corrected interface states these hypotheses and its coefficient norms.

Equation (1) is surjective onto the ten independent symmetric metric entries.
Thus a **previously derived metric covector** can be recovered from all these
normal probes. If a functional variation really factors through these metric
entries and the probes are admitted, stationarity under every such probe
forces that metric covector to vanish. This is the conditional consequence;
it does not identify the covector with an Einstein equation.

The observer-line reflection of a positive q has an invertible ten-slot
differential at fixed observer line, as the script checks. A physical observer
line and its motion still require their native current/field owner.
The input's Levi-Civita formula must use the same normalized inner product
as q; combining q with the unnormalized trace would multiply Gamma by 2d.

The linear-H negative control has zero projection to the chosen ten
B-generated normal directions. Its precise allowed-normal scope is stated
in the interface; it must not be advertised as eliminating all sources in
every ambient normal direction.

Varying only B_mn as Taylor coefficients while U(0) and dU(0) stay fixed
instead gives delta q(0)=0. The independent normal-field deformations in
(1) change the first jet. This distinction is required to use the supplied
rank computation as a metric-source consumer.

## 3. Thermal window: consume the existing theorem once

The supplied finite values reproduce F_L=d[log Z_L/beta]/dt on
Q(t)=diag(4 exp(2t),exp(-2t)/4,1,1), at beta=1/L. The factor16 cancels from
the normalized derivative and zero modes remain included. For example,

| L | F_L |
|---:|---:|
| 4 | 3.8144935047012773 |
| 128 | 1.8547687714851406 |
| 512 | 0.47070751232035946 |
| 1024 | 0.4697257394652752 |

The analytic [joint heat-limit proof](sources/d0_tower_heat_synthesis_2026-10-15/HEAT_JOINT_LIMIT_PROOF.md)
already establishes, for every fixed c>0,

```text
beta_L=c/L,  F_L -> 15/(32c²).
```

The new packet confirms its c=1 specialization, rather than supplying an
independent native temperature law. In particular beta->0 and beta/h²->infty
do not suffice to remove the shape response. The proposed slower temperature
path may be investigated for this same heat functional, but is not selected
by the Fibonacci trace-band width. A finite-depth trace uncertainty and a
physical heat scale are different inputs.

## 4. Join with the actual complete AF record source

The [canonical trace-record source](A4D_NATIVE_CANONICAL_TRACE_RECORD_SOURCE.md)
supplies a constructive operator source on an existing complete active AF
process. Its first operator readout A7 has old action6 and zero preparation
covector; the nonzero coarse A4 source is compensated by its archive.
Its second active record has complete operator algebra A10 and the exact
identity A_old,operator10=6+A_old,coarse4. On the inherited full-blank matter
variation its source lies in

```text
0.43415444592488 < dA_old,operator10 < 0.43415444592489.
```

Thus an actual native-record spectral covector is available to consume,
including all16 matter components,4 scalar coordinates and the full working
complement. The U(4) germ contributes a different ingredient: a surjective
kinematic geometric readout. There is no proved identification between their
preparations, record projectors, physical field jets or price functionals.
Their coexistence does not establish their composition.

There is already a concrete retained observable for the actual AF germ,
rather than an assumed identification with resonant chi. Let
`r_B=Tr(sigma4,B)` on the canonical trace-record matter curve. Its derivative
is exactly `-8ap7`, while the complete second-record old source is the
positive interval above. Hence r_B is a valid local coordinate on this
one-dimensional germ and

```text
dA_old,operator10/dr_B = A'_old,operator10/(-8ap7).
```

This is a derivative of the existing action and observable, not a new
chosen source term. It makes no sufficiency claim outside that germ.
It is not a definition of the resonant chi_1,chi_2.

The existing observer metric alone misses this germ's source. To see this
without a new current census, its matter support is the four masks
S={0,1,14,15}. At the identity frame the owner's spatial current operators
are alpha_i=(c0+c0*) (ci-ci*), i=1,2,3. Each flips bits0 and i, taking
every mask in S outside S. Thus their compressions to S vanish exactly.
Every normalized matter state on the curve has current e0 and observer
pairing I at fixed Lorentz form eta. Its observer-metric derivative is zero,
but its complete second-record spectral derivative is nonzero. Therefore
that price covector cannot descend through this observer-metric readout
alone. The retained observable r_B supplies an actual visible matter/archive
direction. This does not identify the observer metric with the free U(4)
projector metric, whose native binding is still open.

Indeed the general native right-module theorem makes every first-record
operator-entropy source from gate motion alone vanish at fixed seed, despite
changing operators. The germ's rank10 is therefore not evidence that its
native price source is nonzero or gravitational. One must first construct
the **same** family for both the readout and the price.

The [complete source recursion](A4D_NATIVE_RECORD_SOURCE_JOINT_CONTINUATION.md)
then provides the appropriate derivative, with moving preparation,
noncommuting operation jets and the normalizer. Its hypotheses must be
verified on that family. Replacing the price by
`H+J+R+Info+normalizer` without a native identity can double-count terms;
the supplied sum is retained as a proposal only. Nor can an arbitrary
coherent diagnostic state or a rank-one chronology block substitute for
the actual whole state and sixteen-component feedback determinant.

The resonant coefficient32/49 belongs to its declared naked-star action and
normalization. The supplied packet gives no common-family calculation
transferring it to native Cost-Info. The geometric interface does not make
that transfer automatic. The earlier `(1,i,i,1)` phase and the current
source owner's `(1,1,i,i)` also require an explicit permutation before
comparing such coefficients.

## 5. Reproduction and the next missing arrow

### Parallel published results retained in the same SOURCE

Before this intake was published, SOURCE advanced to `fad5600f` with three
complementary owners. They have been retained together with this packet:

- [Price-metric and phase-complete source lift](A4D_RECORD_PRICE_METRIC_SOURCE_INTEGRATION.md)
  derives the projector metric from the Hessian of an actual two-record
  logdet comparator. Its separate twelve-channel amplitude/phase family has
  a bounded joint metric/internal lift on an explicit open C2 domain. This
  is stronger than merely counting ten slots at one point, but does not
  identify that family with the supplied U(4) germ or the full AF/CAR state.
- [Normal-volume source](A4D_RECORD_NORMAL_VOLUME_SOURCE.md) derives a
  geometric volume contrast under its stated normal-measure hypotheses.
  Its ambient normal displacements must not be substituted for the allowed
  unitary normal fields in (1).
- [Finite golden-cylinder curvature reading](A4D_GOLDEN_CYLINDER_CURVATURE_READOUT.md)
  uses actual complete two-letter cylinders, a full normal Parseval family
  and a calibrated three-scale contrast to read scalar curvature exactly.
  Its moving-preparation calibration and normalizer yield a well-defined
  covector for that declared readout. It needs no continuum fourth-moment
  law and does not reinterpret the contrast as a positive probability.

The last owner supplies a concrete calibrated Einstein-Hilbert **readout**
and its metric covector. That mathematical arrow is no longer described as
missing. What remains unproved is its selection by the complete native
price/source sector and its primitive implementation on the same admitted
AF/CAR field family. The nonzero retained source in Section 4 is not
defined as the residual needed to enforce that selection. These owners are
consumed by reference without replaying their unchanged suites.

There is a direct geometric specialization, rather than only a dependency
link: apply that cylinder readout to the present rank4 projector immersion
in Herm(C8). Its ambient dimension is64 and its full normal dimension60.
Using the projected full64-element ambient orthonormal basis gives the
required Parseval family, including its redundant settings. The existing
theorem then yields `R_read(0)=R_q(0)=-6/p³` exactly on this U(4) germ.
The ten graph-normal fields in (1) serve metric variation; replacing the
full curvature-reading frame with those ten fields is not justified.
This closes the fixture-to-declared-curvature-reading link while leaving
selection of that reading by native Cost-Info open.

The focused entrypoint is
`certificates/a4d_native_record_second_jet_intake_check.py`. It pins all five
immutable inputs, consumes the supplied finite fixture, checks the corrected
normal map conventions, and reproduces the nine thermal values without
executing the original output-writing tail. It writes no result ledger.
The older tower/heat proof, existing source recursion and Lean builds are
consumed without replay.

The next missing arrow is an admitted common native preparation whose
complete price derivative factors through this geometric readout with a
controlled remainder on the full constrained (q,D,b,m) tangent. Equation (1)
then gives the local finite inverse in declared norms. Refinement-uniform
control, the complete matter/link equations, curved joint solutions and
the original fixed-source/raw-owner #310 terminal require their own proofs.
No physical source/action closure or GR verdict is changed by this intake.
