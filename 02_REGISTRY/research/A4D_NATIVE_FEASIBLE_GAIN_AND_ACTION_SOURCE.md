# Feasible history tests: maximal gain, source and the required memory operation

17 October 2026. Same Draft #334, input `21f8a25f`.
Consumer: the actual test/Info/full-price source arrow, after the explicit
[golden coherence test](A4D_RETAINED_HISTORY_COHERENCE_TEST.md) and
[raw-normalizer law](A4D_RETAINED_HISTORY_READOUT_AND_NORMALIZER.md).
No physical information law, gate, price or source is installed here.

**Result.** Every finite test in the supplied one-way record class has a
translation-covariant joint pointer POVM. This survives arbitrary active
computation, extra workspaces, word length and active complex quadratures.
For a central-reference real qubit it forces the quantitative gain deficit

```text
D(sigma || I/2)-I_test(sigma) >= min(x^2,z^2)/4,
sigma=(I+xX+zZ)/2, x^2+z^2<=1.                          (1)
```

It holds even for a larger class of complex covariant effects. In the
generous supplied active-orthogonal class the optimized real gain has
second directional coefficient max(x^2,z^2), whereas quantum relative
entropy has x^2+z^2. An exact compact one-variable optimization and its
Danskin source are given below. The optimized gain has no Frechet Hessian
at the maximally mixed state. Informational completeness therefore does
not license the complete-POVM maximal-gain theorem or its entropy source.

The witness is a record-response theorem, not a claim that this entire
qubit family is a reachable literal-v8 preparation. A tensor extension
retains the whole tape and all other specified carriers; no native joint
root, all-ten Einstein discrepancy or physical D0 no-go is inferred.

## 1. All-word covariance from the actual one-way generator interface

Use the class explicitly supplied in
[A4D_NATIVE_RETAINED_RECORD_ADMISSION.md](A4D_NATIVE_RETAINED_RECORD_ADMISSION.md),
Section1. An active finite carrier A admits its supplied orthogonal
operations; R=(Z/2Z)^r is the retained record, with translations X_t.
One-way registration is C_f:(a,r)->(a,r+f(a)). Every such generator commutes
with I_A tensor X_t. Hence every word U and reversal commutes with it. Fresh tensor
workspaces with the unchanged old R-pointer have the same property. Allowing complex active
unitaries would not change this conclusion: they still act only on A.

A test uses independently supplied active preparation eta_A, the old record
state sigma, the complete word U, and final joint pointer outcomes b,omega.
For a pure active blank its effects on R are

```text
E_(b,omega)=<0| U* (F_b tensor P_omega) U |0>_A,
P_omega=|omega><omega|, sum_b F_b=I_A.
```

Mixed independent eta_A follows by convex combination. Old/data correlations
cannot silently be replaced by this product preparation; a test using an
already correlated active input requires its actual larger input interface.
A final active pointer basis, or a common active POVM, is independent of
the old label. Old-label-dependent coherent controls would be an enlarged
operation class and are not assumed.

Using P_(omega+t)=X_t P_omega X_t and the commutation gives, exactly,

```text
E_(b,omega+t)=X_t E_(b,omega) X_t,
sum_(b,omega) E_(b,omega)=I_R.                           (2)
```

For a general faithful change of representation J with transported probe S,
charge intertwining SJ=JX alone is insufficient for this POVM conclusion.
The pointer cut must also intertwine: its projectors must be paired by S.
For example J=V, S=VXV* and identity dynamics preserve that charge, while
keeping an unrelated fixed Z-pointer can pull back to an arbitrary tilted
projective test. Such a pointer change is not a free extension of this
literal tensor/pointer class. Equation (2) asserts covariance for the
declared unchanged pointer, or an explicitly equivariant transported cut.

This is a full POVM covariance theorem, stronger than the earlier conserved
state-charge statement. It covers all lengths, not a finite search. It also
covers the G C_t G informationally complete family: a conserved charge can
be measured without changing it. Arbitrary classical coarse postprocessing
cannot improve its relative-entropy gain by the scalar log-sum inequality.

For a selected old bit, the output labels split into pairs interchanged
by that bit's flip X. Pair members have equal trace. Their normalized
Bloch vectors have (v_x,v_y,v_z) and (v_x,-v_y,-v_z). This is all that
(1) needs; effects need not be rank1 or even real.

## 2. Quantitative maximal-gain gap without an optimizer search

Use natural logarithms until division by log(phi). Let mu=I/2 and
sigma=(I+xX+zZ)/2, r=sqrt(x^2+z^2)<=1. For any qubit POVM write

```text
E_y=tau_y(I+v_y.sigma_Pauli), tau_y=Tr E_y/2,
tau_y>=0, |v_y|<=1, sum tau_y=1, sum tau_y v_y=0.
```

Then q_mu,y=tau_y and q_sigma,y=tau_y(1+x v_x+z v_z). Zero-trace
outcomes vanish identically. With f(t)=t log t, f(0)=0, define the
measured gain I_M=D(q_sigma||q_mu)=sum_y tau_y f(1+xv_x+zv_z).
The quantum gain is [f(1+r)+f(1-r)]/2.

The elementary function f(t)-t^2/4 is convex on [0,2], since its second
derivative is 1/t-1/2>=0 on the interior and it extends continuously
at0. Applying its Jensen inequality to the two eigenvalues1+/-r,
with overlap weights [1+/- (xv_x+zv_z)/r]/2, proves

```text
D(sigma||mu)-I_M
 >= (1/4)[r^2-sum_y tau_y(xv_x+zv_z)^2].                (3)
```

At r=0 use continuity. Completeness makes the averaged spectral weights
1/2, so the left side really is quantum minus measured gain. No theorem
assuming arbitrary feasible POVMs is being imported to identify Info.
For a covariant pair the mixed term v_x v_z cancels. Therefore

```text
sum tau_y(xv_x+zv_z)^2
 =x^2 sum tau_y v_x^2+z^2 sum tau_y v_z^2
 <=max(x^2,z^2) sum tau_y(v_x^2+v_z^2)
 <=max(x^2,z^2).
```

Substitution in (3) proves (1), uniformly over every word and extension.
For the faithful explicit response x=z=1/2 the deficit is at least1/16
nats, or 1/[16 log(phi)] in the Book units. Thus full-D saturation fails
strictly even before programme cost or finite precision is charged.
Adding a cost cannot justify calling this missing measured gain available.

This is a universal test-class counterexample. It does not assert that its
record density has already been generated by the native v8 history, or that
mu=I/2 is the physical reference of that history. The actual golden/AF
reference must retain its owned centrality/block hypotheses. In particular,
a noncentral reference cannot be renamed I/2 to apply the earlier theorem.

For a literal larger tape R=C2 tensor C^m, the same test-class bound
holds on the full-carrier response fixture sigma tensor I_m/m with
reference I_(2m)/(2m). Set F_y=Tr_rest(E_y)/m; these form a complete qubit
POVM and inherit the selected bit's covariance. They have exactly the same
outcome probabilities, while the quantum relative entropy is unchanged.
Further full16/reference128 spectator factors can be retained by the same
partial expectation. This retains, rather than deletes, those factors.
Their preparation/reachability and their independently moving physical
sources are not proved by this algebraic fixture and are not frozen in the
parent theory. No two equal-cost literal labels are declared a native qubit.

## 3. Exact real-covariant optimum and its genuine source

A positive real qubit effect can be refined into real rank1 effects. The
log-sum inequality says that refinement cannot decrease measured gain.
Refine entire flip orbits together, preserving covariance. Consequently
the supremum over real covariant POVMs is represented by orbit seeds

```text
E_(u,+)=(w/2)[I+u X+sqrt(1-u^2) Z],
E_(u,-)=X E_(u,+) X,
-1<=u<=1, w>=0, sum w=1, sum w u=0.                    (4)
```

Choosing the opposite Z sign just relabels the pair. Let v=sqrt(1-u^2),
a_+=1+xu+zv, a_-=1+xu-zv and

```text
g_(x,z)(u)=[f(a_+)+f(a_-)]/2,
I_cov(x,z)=max_(probability W on[-1,1], integral u dW=0)
                                     integral g_(x,z)(u)dW.      (5)
```

This is the upper concave envelope of g at0, not a rank census. The
probability-measure set is compact and g is continuous, so the maximum
exists. A maximizing extreme measure needs at most two support points:
three distinct supports admit a nonzero signed perturbation with both
mass and first moment zero, and hence cannot be extreme. The general
measure assertion follows by the same moment convex-hull argument.
One or two covariant seed pairs suffice for the value in (5).

This enlarged optimum is constructible in the SUPPLIED all-active-
orthogonal class, conditional on the same old-target addressability.
In the old X eigenbasis a complete two-seed POVM has amplitudes

```text
f_(b,+)=sqrt(w_b(1+u_b)),
f_(b,-)=sqrt(w_b(1-u_b)), sum_b f_(b,+/-)^2=1.
```

Choose independently supplied active rotations R(theta_+) and R(theta_-)
whose first columns are these two unit vectors. With
alpha=(theta_++theta_-)/2, beta=(theta_+-theta_-)/2, the word
R(alpha)_A CNOT_(A->R) R(beta)_A CNOT_(A->R) acts as
R(theta_+) in the old X=+1 sector and R(theta_-) in the X=-1 sector.
The complete final joint pointer gives exactly (4). This costs two active
rotations and two registrations, all outcomes retained. It does NOT prove
that these continuously chosen rotations are exact native golden words,
that their preparation/decoder is free, or that an optimal state-dependent
measurement programme has zero cost or zero source. Equation (5) is an
upper bound for every smaller actual one-way class even without this
constructibility premise.

For a faithful response r<1 all a_+/- are uniformly positive. The derivative
of g is uniformly continuous on compact response sets. Differentiation of
a specified test, with its fixed prior, gives the genuine linear covector

```text
L_W[delta x,delta z]
 =integral [ (u/2)log(a_+ a_-) delta x
             +(v/2)log(a_+/a_-) delta z ] dW.            (6)
```

The +1 terms in f' cancel because integral u dW=0 and the Z pair is balanced.
Compactness and a direct maximizing-subsequence argument prove Danskin:

```text
D^+ I_cov[(delta x,delta z)]
                =max_(W in Opt(x,z)) L_W[delta x,delta z].        (7)
```

Indeed a fixed optimizer gives the lower bound; take a convergent subsequence
of optimizers at perturbed responses for the reverse bound. This is an exact
one-sided source formula. If the optimizer's covectors disagree, the physical
source is set-valued until the native rule supplies a particular actual test.
On a branch with a unique optimizing covector it is the ordinary derivative.
Actual field dependence pulls (6) back through the genuine normalized
record-state jets, delta x=Tr(X delta sigma), delta z=Tr(Z delta sigma).
A moving reference/test or charged programme requires its additional terms.
No source is inferred by differentiating an unproved value limit.

## 4. The optimized second response is not the quantum entropy Hessian

For sigma_t=[I+t(xX+zZ)]/2 with bounded x,z, scalar Taylor at1 is uniform
in EVERY effect because |xv_x+zv_z|<=r and sum tau=1. Thus

```text
I_M(sigma_t)=t^2/2 sum tau_y(xv_x+zv_z)^2+O(t^3),
I_cov(sigma_t)<=t^2/2 max(x^2,z^2)+O(t^3).               (8)
```

The pointer Z test achieves the z^2 coefficient. In the supplied active-
orthogonal class, a sharp X test uses blank active port, H_A, one CNOT
A->R, and H_A, where H=(X+Z)/sqrt(2). It gives
K0=(I+X)/2, K1=(I-X)/2. Its joint old pointer only splits each outcome
into two equal suboutcomes, leaving KL unchanged. Hence

```text
I_cov(sigma_t)=t^2/2 max(x^2,z^2)+O(t^3),
D(sigma_t||I/2)=t^2/2 (x^2+z^2)+O(t^4).                (9)
```

For a smaller literal golden class (8) remains an upper bound; exact H
is not declared native by this calculation. The previous compiler's
integral-ring/resource restrictions remain in force. Pointer Z alone
already makes (9) sharp in the two equal-magnitude directions below.

The second directional coefficient q(x,z)=max(x^2,z^2) violates the
parallelogram identity:

```text
q(1,1)+q(1,-1)=2,
2q(1,0)+2q(0,1)=4.                                    (10)
```

Therefore no bilinear Frechet Hessian can represent this optimized gain
at mu. Its first derivative there is0; failure is at the second response.
The argument uses a uniform Taylor bound over all feasible tests. It does
not pretend that a scalar value expansion automatically supplies derivatives
of a varying optimizer. The genuine first source is (7); convexity and
secant bounds also recover the same radial second directional coefficient.

Under the separate conditional maximal-gain interpretation with central
cost -Tr sigma log mu=log2, the net action is log2-I_cov, not S_vN(sigma).
The latter would have the Euclidean second coefficient in (9). Divide all
these gain/net-action expressions by log(phi) for the Book units. Nothing
here selects that interpretation as D0's physical Cost-minus-Info or adds
it to the previously specified v8 H+J+R price.
This maximization is over complete experiments. It is not the pathwise
likelihood Info of one fixed outcome cut. The existing SAME-history
identity E S=(H-log N)/log(phi) retains its own binding; neither formula
is substituted for the other without an actual native history/test map.

## 5. What operation is needed, and what existing phase objects actually own

The obstruction follows from commutation with the old translations. Thus
a universal complete-D gain theorem on this response interface needs a
physically admitted operation or a measurement beyond this class. An active
phase alone does not supply it. Even if S=diag(1,i) is independently given,
all active gates and one-way C_f still commute with every old X_t.

Such an S does give a positive TOMOGRAPHIC result: the complete word
(G tensor I)(S tensor I) C_t(G tensor I) has

```text
K0=pI-i p^2 X_t, K1=ap(I+iX_t),
E_(1,i)=p^3(P_i+P_j+i|i><j|-i|j><i|),
q_(1,i)=p^3[d_i+d_j+2 Im sigma_ij].                     (11)
```

Together with the real test it reconstructs a general Hermitian record.
The word uses3+Hamming(t) supplied operations. It still obeys (2) and the
gain deficit. Complete tomography is not operational equality in the
relative-entropy data-processing theorem.

The currently owned `OrderMemoryReadout.complexTurn` is a commuting
right-i real matrix defining a complex reading, not this physical active
phase-placement instruction. `OrderMemoryControl.localIQ` is controlled
LEFT-i. Relative to the right-i reading, its spin action is diag(i,-i),
not iI on the full spin carrier. A separately prepared +i spin eigenline,
or a proved shared realification/reference encoding, would be an extra
resource/weld. No grade or reference direction is removed to supply it.
Role-phase translations are not automatically multiplication-by-i gates.

Likewise `VerifiabilityNecessity.VerificationProtocol` has states, records,
lines, catalogues and a comparator, but no operation/admissibility/decoder
field. Its injective-retention and truth-invariance theorem does not pick
between append-only operations and old-target addressability. The physical
comparison-representation interface takes admissible operations as inputs.
This is a type inspection of the actual owners, not two asserted complete
physical D0 models. A full native decoder/operation theorem is still needed.

For example a gate acting on OLD memory that fails to commute with X_t
can leave the bound's class; the actual old golden rotation has this
property. Its physical placement and cost must be derived. Conversely the
physical Info law could be a genuinely restricted gain instead of full D;
then (5)-(10), rather than a quantum-entropy Hessian, describe this record
interface. No option is silently chosen here.

## 6. A positive normalization construction from the actual scene tower

The [native-history owner](A4D_NATIVE_HISTORY_ACTION_BOUNDARY.md), Sections4–5,
already proves endpoint-central Perron weights for the fixed K(9,11,13)
scene adjacency A. If Ar=rho_scene r, r>0, its transition law is

```text
p(u,v)=A_uv r(v)/(rho_scene r(u)), sum_v p(u,v)=1.        (12)
```

This is a genuine local projectivity example, not a chosen normalizer1.
For an actual allowed scene path v0,...,vn, amplitudes are not being added;
the classical product weight telescopes as

```text
w_path=product_j A_(v_j,v_(j+1))
                     r(v_n)/(rho_scene^n r(v_0)).
```

On the unweighted fixed scene its negative log is n log rho_scene plus
the endpoint log-r boundary. At fixed length/endpoints this has no internal
coframe/link source. If these quantities move in an independently supplied
weighted-scene family, their FULL derivative is

```text
d log w_path=sum_edges d log A_uv - n d log rho_scene
                              +d log r(v_n)-d log r(v_0).         (13)
```

Here the eigenvector/source is not an arbitrary input. On a smooth
positive-weighted fixed connected scene, the simple Perron eigenpair and
normalization 1^T r=1 give the unique finite bordered solve

```text
[ rho I-A    r ][dr  ] = [dA r],
[   1^T      0 ][drho]   [  0 ],
drho=(l^T dA r)/(l^T r), l^T A=rho l^T.
```

Differentiating Ar=rho r proves the first row; normalization proves the
second. The left eigenvector fixes drho; simplicity then fixes dr uniquely.
Substituting this solution in (13) retains the genuine normalization and
endpoint source instead of freezing the Perron state. The fixed graph
does not supply the actual field-to-weighted-scene map.
After, and ONLY after, this law is bound to the Book action and its actual
cost, I_edge=C_edge+log_phi p solves the local gain equation automatically.
This does not derive the physical Info law merely by naming a Perron trace.
The primitive ActionProtocol's cost1 for any nonidentity endpoint is not
itself a complete per-edge prefix code on20/22/24 outgoing alternatives.
Its action quantum must not be identified with that information code.

## 7. The action binding is an amplitude/instrument map, not an effect algebra map

A source-typed native binding needs amplitudes K_omega and a physically
admitted complete outcome cut. Its effects satisfy

```text
E_omega=K_omega* K_omega,
E_(omega alpha)=K_omega* E_alpha K_omega,
sum_alpha E_(omega alpha)=E_omega.                     (14)
```

Conditional operations use their actual prefix-dependent E_alpha; writing
E_omega E_alpha would in general be wrong and need not even be positive.
For all faithful normalized preparations in an open density set, scalar
projectivity Tr rho[sum E_child-E_parent]=0 is equivalent to the operator
identity in (14): traceless Hermitian perturbations of a faithful density
show that the operator defect is cI; evaluating the original equality at
one normalized faithful base density gives c=0. No trace-changing density
tangent is needed. Once (14) holds on the
actual moving family, N=1 and all normalization jets follow automatically,
with the normalized preparation and true operator derivatives retained.
This closes the normalization step AFTER the physical cut is established.

If paths are combined coherently before readout, the actual outcome
amplitude is K_beta=sum_(gamma in beta) a_gamma U_gamma, and its effect
includes all ordered cross terms. Pointer paths are not those coherent
classes by default. The Book algebra-valued Z_D and its chosen scalar
expectation must be mapped through this amplitude/cut interface.

There is a concrete obstruction to a different shortcut: the actual
[native-cycle calculation](sources/d0_native_cycle_morphism_2026-10-17/RESULT_RU.md)
has a literal effective closed-entry cycle -(23/480)^3<0 although F>=0.
It cannot be mapped individually to a positive Born event with that weight.
The signed cyclic trace-log valuation and the positive open probability
cut must retain their distinct typing. Its1/n comes from a cyclic quotient
with stabilizers; physical future-test equivalence of that quotient remains
separate. This does not forbid a coherent valuation or the full determinant.

## 8. Consumed result and remaining full theory target

The real readout premise is now stronger and narrower: tomography can be
constructed conditionally, but the one-way class has a provable restricted
gain/source law and cannot realize the full-D theorem on all record states.
Adding an imaginary quadrature within that same commutant does not change
this. The candidate complete-gain route must derive the needed actual
memory operation/cut or carry its restricted optimized source, with true
programme/preparation/reference cost. This is the missing operational
premise consumed by the parent synthesis, not another finite-gate census.

The scene-Perron tower supplies a positive normalization theorem on its
own carrier. Its amplitude-to-instrument and Book action/Info binding are
not established by an endpoint-central trace. The original full physical
source must still equal the intrinsic nonlinear Einstein covector with
independently derived matter, nonzero coupling and a nonempty compatible
joint refinement. All 16 grades, reference128 and every original metric
row remain in that target. The fixed-g/independent-tau/all-ten unweighted
raw h^-2/#216 terminal is OPEN. No action term, fitted stress, native phase,
controller placement, source law or CORE promotion is introduced here.


## 9. Bounded verification and intake

The [source packet](sources/d0_feasible_gain_source_2026-10-17/README.md)
pins the unchanged algebra/representation/history owners. Its sole new
helper checks 49 exact identities and negative controls in ordinary and
optimized Python with identical output. It checks covariance, actual gate
ordering, strong-Jensen curvature/variance, supplied sharp tests, phase and
old-memory distinctions. The all-word inequality, compact optimum, actual
source and no-Hessian proof above are analytical, not conclusions from a
sampled measurement census. Static cross-review corrected the extension
pointer-equivariance and normalized-density-tangent wording. No old
scientific entrypoint or Lean build was run, and no independent CONTROL
acceptance, remote CI or physical closure is claimed.
