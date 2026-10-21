# Actual clock elimination retains the coherent return and its full source

21 October 2026. Existing Draft #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`,
`constitutive/native-programme-v1`. Published foundation:
df53abbef4979ecf670839bfccbb9f8e445e9361. Exact stage inputs are the
reviewed [stage-clock packet](NATIVE_STAGE_CLOCK_AND_POINTED_DESCENT.md)
and its checker, frozen locally at68346fbbd4e27efd2f962fed9e582adfa35c7da8;
that packet is pending joint publication in this same PR, not presented
as an already published source. Their precise SHA pins are in the checker.

Consumer: [two-query parent](TWO_NATIVE_8D_DETERMINANT_SOURCE.md), section22,
and section21's actual tick-to-macro operator/source obligation. This
application eliminates the literal given stage archive rather than
postulating a clock multiplicity or reset. It constructs a coherent
amplitude return, not a selected new physical price or heat operator.

## 1. Full-apparatus archive, before the prepared cut

Use the exact owned Book03 apparatus: clock16 tensor arm2 tensor spin4
tensor record2, Euclidean pairing. W_s is the complete autonomous
transition of the retained identity/order program block. All apparatus
coordinates remain, including the output record and unprepared arm.
The final stage is the given reversible idle15->0. The reported
original trial stops after15 transitions from0, before this wrap.
The two blocks retain different input program bits inside the same
fixed device; they are not a same-complete-initial prospective test.

In this calculation choose

```text
k0=|0>_clock tensor I16,
P=k0 k0*,  Q=I-P,
D=Q W_s Q,
M_s=U_s,15 U_s,14 ... U_s,0.
```

This P has rank16. It is NOT the earlier rank4 arm0/record0 input
cut. With all16 phase transitions retained, M_s is a full orthogonal
apparatus operator. Its chronological product has15 nonidle operations
and one idle; the sixteen-transition closure is a different declared
finite execution from the pre-wrap trial. No elapsed-time reset follows.

The actual shift on clock labels gives

```text
P W_s P=0,
D^15=0, D^14!=0,
P W_s Q D^k Q W_s P=0 for k=0,...,13,
P W_s Q D^14 Q W_s P=k0 M_s k0*.
```

There is exactly one first-return path:0->1->...->15->0. It has14
internal QWQ factors and two boundary transitions. Book06 section06.8.F's
archive-delay index is therefore k=14 here, not the total transition
count16. This is a concrete application of the owned Feshbach path
grammar; it does not reclassify encoded stage labels as physical time.

## 2. Exact return map and determinant, with no extra clock factor

Let t be a scalar ANALYSIS marker. Nilpotency makes
(I_Q-tD)^-1=sum_(k=0)^14 t^k D^k a finite polynomial for every t.
The Schur complement of I-tW_s on the actual P is exactly

```text
S_P(I-tW_s)=I16-t^16 M_s.
```

Ordering the archive stages1,...,15 makes I_Q-tD block triangular
with identity diagonal. Its determinant is1, not a discarded residual.
Consequently

```text
det_256(I-tW_s)=det_16(I-qM_s),   q=t^16,
k0*(I-tW_s)^-1 k0=(I-qM_s)^-1 whenever the full inverse exists.
```

In particular these are nonsingular for0<t<1, since M_s is orthogonal.
There is NO extra exponent16 on the determinant on the right: the
actual clock has been eliminated with its full archive determinant.
No normalization is chosen to remove that factor.

At t=1 the archive inverse and Schur operator still exist, but the
actual M_s has eigenvalue1. Thus I-W_s is singular; neither the full
resolvent nor its logarithm can be evaluated at that endpoint. A return
operator at t=1 does not supply an invertible full statistical sum.

The geometric-series coefficients are literal coherent loop amplitudes
of the given apparatus, before Born readout. Repeated cycles reuse its
existing record; they are not fresh independent trials or a free record
reset. The variable t, and therefore q, has not been identified with
the physical Book weight, z, Golden port probability or elapsed clock.

## 3. Literal monodromy and complete loop determinant

Write G=[[a,-p],[p,a]], a=sqrt(p), p=phi^-1, and Z=diag(1,-1)
on the arm. The owned words give

```text
M_identity=WRITE,
M_order=WRITE G* Z G,
c=cos(2theta)=p-p^2=p^3.
```

In the record-X eigenbasis, WRITE is I_arm on record+ and Z_arm on
record-. Thus, with all spin4 coordinates retained,

```text
M_identity = (I_arm direct_sum Z_arm) tensor I4,
M_order = ((G* Z G) direct_sum G^2) tensor I4.
```

The record basis is an analytical orthogonal decomposition, not a new
physical gate or discarded record sector. The two-dimensional reflection
has eigenvalues+1,-1; the rotation G^2 has determinant1 and trace2p^3.
Exact finite determinants therefore give

```text
det(I-qM_identity)=(1-q)^12(1+q)^4,
det(I-qM_order)=(1-q)^4(1+q)^4(1-2p^3q+q^2)^4,
det_order/det_identity=[1+4p^2 q/(1-q)^2]^4.
```

Every factor is positive for0<q<1. If the scalar statistic considered
is J_loop=-logdet(I-qM), its order-minus-identity value is

```text
Delta J_loop=-4 log[1+4p^2 q/(1-q)^2] <0.
```

This is an exact scalar consequence of the coherent loop operator.
It is not the earlier positive Book-complement macro feedback statistic,
and J_loop has not been selected as full physical Cost-Info. The complete
spin and record determinants are retained rather than replacing M by
its prepared scalar p^3. M has a negative eigenvalue and rotation phases;
the Book feedback F=P U*Q U P is positive semidefinite. They are different
typed operators even when both are read by a determinant formula.

## 4. Full source and the three different feedback cuts

On this fixed finite carrier, let R=(I-qM)^-1 and retain the ordered
actual product source

```text
dM=sum_(r=0)^15 U15 ... U_(r+1) (dUr) U_(r-1) ... U0,
dq=16t^15 dt,
dR=R[(dq)M+q(dM)]R,
dJ_loop=Tr[R((dq)M+q(dM))].
```

The fixed idle has zero operator derivative only if it is actually
held fixed; its executed duration/payment is not deleted. Moving clock,
cut or pairing data retain their sources. For the full clock determinant
the same formula is exact by Schur elimination; no small-t truncation,
commuting field variation or additional factor16 is used. If the archive
map itself changes away from this literal shift interface, its determinant
and source must be rederived rather than declared constant.

The following complete-apparatus feedbacks show exactly what this
return map supplies and what it does not:

```text
F(P,W_s)=I16,             certain first escape from stage0,
F(P,W_s^16)=I16-M_s*M_s=0,  full orthogonal apparatus returns.
```

Neither equals M_s or R. The first forgets the delay and holonomy; the
second retains a full unitary return rather than a prepared apparatus.
Only AFTER retaining/eliminating the complete clock archive may the
separately supplied j:spin4->arm0,record0 be applied. Then

```text
j* M_identity j=I4,
j* M_order j=p^3I4,
F_j=I4-(j*Mj)*(j*Mj) = 0 / (1-p^6)I4.
```

This recovers the owned seed0 leakage through an actual sixteen-step
encoded return, including the additional idle transition whose actual
duration/payment must be retained. It does not change
the original fifteen-step experiment, derive physical j, or identify
the one-step Book action with that prepared return action. Eliminating
the remaining work complement in a resolvent is a further Schur map;
it cannot be replaced by simply deleting the arm/record blocks.

## 5. Exact parent substitution and remaining physical premise

The stage-clock consumer now has a concrete clock elimination, an actual
pretrace monodromy, a complete determinant with archive factor1 and its
ordered source. This resolves the algebraic tick-to-return map on the
literal supplied apparatus. Pointed condensed assembly can transport
this map when it intertwines W, P, the actual adjoints and marker/source;
it is no longer a claim based only on probability-cylinder compatibility.

The original CAR stopped controller still needs its own admitted
chronology, terminal/work wiring, physical tick and active cut. On that
actual execution, compute the returned operator and archive determinant
before identifying a Book valuation. The scalar waiting-time statistic,
monodromy amplitude, one-step feedback and prepared return feedback
cannot substitute for one another. Derive the actual weight/cost/gain
map and complete heat/Info/work sources; no t or q is fitted to GR.

The smallest decisive check is the literal sixteen-apparatus monodromy,
record-sector characteristic polynomials and exact archive path length,
with hostile omitted-idle, feedback/return and record-deletion controls.
No new graph heat generator, physical cycle reset, independent task,
assembly acceptance, joint-source equality, GR or raw216 closure is added.
Write paths: this proof, its checker/certificate/review, and parent section22.
