# Actual stage-clock corners and pointed history descent

21 October 2026. Existing Draft #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`,
`constitutive/native-programme-v1`. Published input
df53abbef4979ecf670839bfccbb9f8e445e9361.

Consumer: [two-query parent](TWO_NATIVE_8D_DETERMINANT_SOURCE.md), section21,
and the actual clock/work premise in
[the Book complement](NATIVE_COHERENT_BOOK_COMPLEMENT.md), section2.
This is a bounded application to the existing Book03 apparatus, not a
new clock search or a replacement for the original primary D instrument.
It determines what the owned generic stage construction actually supplies
and the data a condensed assembly must preserve.

## 1. Exact statement and owned carrier

Consume Book03 section03.26.1 and its actual owners
`04_CERTIFICATES/order_memory_control_verify.py` and
`03_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean`.
The apparatus is arm2 tensor spin4 tensor record2, with the positive
Euclidean pairing used by that certificate. A stored program bit selects
identity/order inside one fixed512-dimensional device. The clock is
ZMod16. Its given full reversible extension has one final idle wrap;
the original reported experiment starts at0 and executes15 transitions,
before wrap. These are encoded stage labels. Their identification with
physical elapsed time or the original cap2 controller is not asserted.
The two program blocks have different retained input program bits;
this comparison is not a same-complete-initial prospective alternative.

Let j embed arbitrary spin in arm0,record0. With a=sqrt(p), p=phi^-1,
the actual chronological schedules are

```text
identity word: X X X X Y Y Y Y,
order word:    X Y X X X Y Y Y,
schedule: G, word, X X G X X, WRITE, idle.
```

Here X=diag(I,L_i), Y=diag(L_j,L_j), G=[[a,-p],[p,a]] tensor I,
and WRITE reversibly xors arm into the record. Every spin and record
column remains in the complete apparatus. X^2=Z=diag(I,-I),
Z G Z=G*, and the two eight-letter words are respectively I and Z.
Only supplied local routing/blank preparation are consumed; their M1
physical admission is the original explicit boundary.

For either stored program s, write its sixteen stage operators U_s,c.
With indices modulo16,

```text
W_s = sum_c |c+1><c| tensor U_s,c,
W_s^L = sum_c |c+L><c| tensor M_s,c,
M_s,c = U_s,c+L-1 ... U_s,c,
a_s,c = j* M_s,c j.
```

The product is chronological with the last operation on the left.
No reverse query or clock reset is inserted.

## 2. Two actual cuts, and a decisive shared-factor test

For the initial-stage-only embedding i0=|0> tensor j and L=15,

```text
i0* W_s^15 i0=0,
F_start=I4,
S_fb,start=-4 log(1-z),  0<z<1.
```

The active clock component has left the initial stage. Norm conservation
and a retained final record do not change this zero corner.

For the clock-spanning cut i_all=I16 tensor j, the exact blocks instead are

```text
A_s = sum_c |c+15><c| tensor a_s,c,
F_s = direct_sum_c (I4-a_s,c* a_s,c).
```

Thus its full feedback price is the SUM of the sixteen actual block
log-determinants. It is not automatically sixteen times the price of
the trial that starts at0. Off-seed windows in the given full reversible
extension include wrap; they are not extra claims about histories
executed in the original fifteen-transition experiment.

Two literal windows already decide the common-factor question:

| Initial stage c | a_identity,c | a_order,c |
|---|---|---|
| 0 | I4 | p^3 I4 |
| 1 | a I4 | a I4 |

At c0 the schedule is WRITE G* word G. Its compressed arm0 block is
I for the identity and (p-p^2)I=p^3I for the order word; WRITE retains
arm0,record0 and sends the other arm outside the cut. At c1 the window
omits the initial G and includes idle: it is WRITE G* word. Both words
fix the input arm0, so both compressed blocks are aI.

Consequently NO single clock operator T and data operators D_identity,
D_order can satisfy A_s=T tensor D_s for both programs. The c0 block
forces D_order=p^3 D_identity; c1 forces D_order=D_identity, with both
clock entries nonzero. The exact cross difference is
a(p^3-1)I4, which is nonzero. Allowing a different T for each program
would discard the shared-clock premise being tested.

At c0 the feedback blocks are0 and (1-p^6)I4; at c1 both are p^2I4.
The retained output record is essential to these compressions. Its
deletion changes the corner rather than merely its notation.

The complete sixteen-window calculation gives a POSITIVE result even
though the shared factor fails. Every feedback block is scalar I4:

| Feedback scalar | Identity multiplicity in clock | Order multiplicity in clock |
|---|---:|---:|
| 0 | 4 | 0 |
| p^2 | 2 | 2 |
| p | 10 | 10 |
| 1-p^6=4p^3 | 0 | 4 |

Therefore on the actual64-dimensional clock-spanning input carrier,

```text
det(I-z F_identity)=(1-zp^2)^8 (1-zp)^40,
det(I-z F_order)=det(I-z F_identity) (1-4zp^3)^16,
S_fb,order-S_fb,identity=-16 log(1-4zp^3)>0,  0<z<1.
```

All factors are positive since4p^3=1-p^6<1. This is exactly FOUR
times the seed0 feedback-price difference, not sixteen times it.
The full off-seed complement can retain an order-sensitive Book penalty
without satisfying T tensor D_program. It must be computed, not inferred
from a clock multiplicity or erased when factorization fails. This is
the given encoded full-clock cut, with its explicitly retained off-seed
cyclic extension; it does not select that cut as physical.

There is a second necessary TYPE distinction: this positive difference
evaluates the feedback functional on the macroargument W_s^15. On the
same clock-spanning cut, ONE autonomous transition instead has

```text
A_s,one=sum_c |c+1><c| tensor (j*U_s,c j).
```

Each G stage has compression aI4; each X compresses to I4, each Y to
L_j, and WRITE/idle to I4. Hence BOTH programs have fourteen zero
feedback blocks and two p^2I4 blocks, exactly

```text
det(I-z F_s,one)=(1-zp^2)^8,
S_fb,s,one=-8 log(1-zp^2).
```

The one-transition feedback price has no program contrast on this cut.
It is not the macro price divided by15. Book03 section03.3.2 uses a
declared U_N and its forced tick; the stage owner defines W_s as one
autonomous transition and completion after15. Neither identification
U_N=W_s nor U_N=W_s^15 is physically supplied by this compiler.
The positive macro result therefore does not establish a compulsory
per-tick Book source. An actual tick-to-macro action/source transport,
including heat, cut, work and clock terms, is a separate parent premise.
This control does not prove that the complete Book stack is order blind.
Even on a fixed carrier its operator source must retain
d(W^15)=sum_(r=0)^14 W^(14-r)(dW)W^r; it is not15 times dW.

This counterexample excludes deriving the Book-complement section2
shared factor from the generic stage theorem, equal primitive counts,
or a clock-spanning cut alone. It does NOT prove failure for the as-yet
unsupplied complete CAR Q^k/B^k stopped controller. The latter has
4+14k nonquery stages even before its actual query/control/comparison
work; at k1 it already exceeds this sixteen-slot sample. Reusing this
clock with unnoticed wrap would be a different construction.

## 3. What a condensed assembly would have to transport

The owned
[price-naturality classification](../../../A4D_NATIVE_CONDENSED_PRICE_NATURALITY.md)
already distinguishes entrywise kernels from operators with positive
pairings and classifies compatible linear extensions as J A C+B with
free new-complement blocks. Its result is consumed here, not repeated
as a new classification. The
[history obstruction](../../../A4D_CONDENSED_HISTORY_SOURCE_OBSTRUCTION.md)
requires quantitative source control beyond qualitative projectivity.
The
[full128 relative-transfer owner](../../../A4D_NATIVE_FULL128_RELATIVE_TRANSFER_AND_CONDENSED_DESCENT.md),
section5, further distinguishes coherent cross amplitudes from probability
cylinders and retains the actual continuous-time mark/clock map.

The necessary extra object at the present step is a compatible family
of POINTED executions with cuts. At each finite level, let H_n,K_n have their actual positive
pairings, i_n:H_n->K_n be isometries, P_n=i_n i_n*, and U_n be complete
unitaries. For isometric active/archive lifts j_n and workspace lifts ell_n,
require

```text
ell_n i_n = i_(n+1) j_n,
U_(n+1) ell_n = ell_n U_n,
P_(n+1) ell_n = ell_n P_n.
```

Then for A_n=i_n* U_n i_n and F_n=I-A_n* A_n,

```text
A_(n+1) j_n = j_n A_n,
F_(n+1) j_n = j_n F_n.
```

Indeed cut compatibility gives i_(n+1)*ell_n=j_n i_n*.
The range of ell_n reduces U_(n+1): the restricted unitary is U_n,
so the adjoint also intertwines. Apply the same calculation to U_n*
and then to A_n* A_n. Hence the range of j_n reduces F_(n+1).
The full counting-trace determinant still has its new-complement term:

```text
-logdet(I-z F_(n+1))
 = -logdet(I-z F_n) -logdet(I-z F_new).
```

Compatibility preserves a SUPPLIED T/cut; it does not choose it or delete
F_new. The determinant splitting above is finite-level; an infinite
determinant would require its own trace-class/source hypotheses.
For a separate clock-INDEPENDENT product example, tensor a fixed encoded
clock shift with the owned archive lifts. This is not the phase-dependent
W_s of section2. A start-only cut gives T=0; a full encoded-clock cut gives
R=T*T=I. Both are compatible mathematical systems. Condensed compatibility
alone therefore cannot select between them or normalize away clock modes.
This example does not admit either choice as the physical D0 cut.

## 4. Full source and the next actual application

On the fixed finite clock-spanning cut put F_c=I-a_c* a_c and
M_c=I-zF_c. Its actual source is

```text
dS_fb = sum_c Tr[M_c^-1(F_c dz+z dF_c)],
dF_c = -(da_c)*a_c-a_c*(da_c),
da_c = (dj)* M_window,c j + j*(dM_window,c)j + j*M_window,c(dj).
```

The window product is differentiated in its actual order. A moving
clock cut/lift has its additional terms in i*Wi; actual retained clock
and work sources are not frozen. There is no oldRIGHT multiplicity in
this Q8 prototype. The original CAR result's factor128 cannot be copied
into this different carrier, nor can this prototype replace its D.

The parent now consumes the actual phasewise corner rather than inferring
a returned clock from a full-clock trace. Its next positive application
must supply the complete original stopped-controller chronology, terminal
status/work comparison and admitted active cut, then compute i*Wi.
Use the section20 factorized determinant ONLY if this corner supplies
its shared T hypothesis; otherwise use the unfactorized full feedback
and source. It must also identify the actual physical U_N/tick argument;
replacing one autonomous step by its completed macro word is not a free
action/source identity. Book06's archive-delay index, the retained waiting-time
statistic and positive pairings on an archive tower do not by themselves
provide that missing unitary/cut identification.

The bounded checker consumes the literal schedules/formal primitives and
checks the new corners/controls with exact arithmetic. It does not run
the old512-dimensional suite or compile Lean again. Physical clock,
compulsory P_N, absolute Book gain/work, joint-source matching, GR and
raw216 remain open. Write paths: this proof, its checker/certificate/review,
and parent section21. No new task, assembly acceptance or public claim.
