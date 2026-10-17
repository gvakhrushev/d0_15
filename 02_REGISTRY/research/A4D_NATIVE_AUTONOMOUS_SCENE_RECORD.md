# A fixed autonomous record word on the whole scene and its complete price

Date: 13 October 2026. Existing Draft #310. Input SOURCE
`68c593f1d12af20378642fa81cee982835cede1d`; main
`fa2b04b9c8aae5a0b8470322d6091712ce56567a`.

This continues [the closed record engine](A4D_NATIVE_CLOSED_RECORD_ENGINE.md).
That packet supplied an exact state-dependent algorithm and an indefinitely
regular seed orbit. It did not compile its amplitude-sign test into the owned
linear gates. This is a real operation-admission issue, not a numerical one.
The previous goal turn was progress: it published the engine/proof at the
input SHA and integrated its verified bytes in CONTROL `47c914e3`.

**Result.** A fixed word of nine forward golden/recording primitives realizes
the engine after its explicit two-record preparation, with the switching
record retained inside the complete state. On the actual K(9,11,13) scene
the switch is the intrinsic orientation of an existing directed edge; it
needs no new fundamental role. The full word acts on all 718 scene histories,
both values of its one additional permanent record and all sixteen matter
components. It has 22976 coordinates. Its original scene and matter readouts
give the explicit composed feedback `p^2 I+p(2 Delta-Delta^2)` in the
prepared record sector, and the complete one/two-tick price is computed
without deleting the other sector.

This is an exact realization in the **previously stated addressed
golden/CNOT palette**. Physical availability of the addressing, basis-one
preparation and common geometric binding is not inferred from matrix
ownership. No new action, selector, physical time, refinement trigger or
source is introduced. The common native preparation/tangent and G1-G4,
together with the original #310/#202/#317 terminals, remain open.

## 1. Why a retained controller is necessary in a fixed isometric execution

In the unnormalized four nonzero coordinates (scalar, first grade, spatial
top, full top), let x2,x3,x4 be the previous seed's second, third and fourth
states. Their full sixteen-coordinate norm squared is 2. Exact reduction
by a^2=p and p+p^2=1 gives

    <x2,x3>=0,       <x3,x4>=4ap^2>0.                (1)

No fixed isometry can therefore implement x2->x3 and x3->x4 on that whole
state space. This includes every fixed word of the owned orthogonal gates.
It also includes any isometric embedding into an arbitrarily large space
with a single auxiliary state returned unchanged: such an embedding still
preserves both inner products. State-dependent norm conservation alone
does not imply this stronger property.

The obstruction is quantitative. Normalize the three states by sqrt(2).
If a fixed isometry implements each of the two required outputs within
epsilon in the full norm, Cauchy-Schwarz gives

    2ap^2 <= 2 epsilon,       epsilon >= ap^2>27/100. (2)

Indeed the difference of the two inner products is bounded by the sum of
the two norm errors, since both the target vectors and isometric outputs
have norm one. The last bound uses p>3/5 and a>3/4 from the compiled prior
packet. This does not exclude nonlinear native laws or an evolving internal
controller. The following construction retains precisely such a controller.

## 2. A literal forward word, with every auxiliary coordinate retained

On each spatial pair of the CAR fibre put

    G=[[a,-p],[p,a]], X=[[0,1],[1,0]], Z=diag(1,-1).

Let N denote the e0 occupation bit. Let K be I on spatial degrees 0,1 and
Z on spatial degrees 2,3. Then the actual complete records are

    U+=K G_N,          U-=K G_N^T,      X G X=G^T.    (3)

The order K G is load-bearing. Reversing it interchanges the high-grade
signs. In the signed CAR apparatus frame, G_N is the ordinary owned system
gate and K is the owned recording CNOT in its record-eigenbasis. The
certificate verifies these claims against the actual original fullStep
and its published fixed change of coordinates; that coordinate change is
not an extra physical gate to be executed on every tick.

Use a switching bit f and a permanent record c initially equal to one.
For CNOTs C_fN, C_cN, C_cf, the chronological fixed program is

    C_fN, G_N, C_fN, C_cN, G_N, C_cN, U+, C_cf.     (4)

There are eight displayed factors, nine primitive factors when U+ is
expanded into its existing golden gate and recording CNOT. Every operation
is forward. The three middle operations realize G_N^T on c=1 by the exact
retained echo, without erasing or replacing c. No amplitude sign, iteration
number, source value or past history is an input to (4).

For c=1, the action is exactly

    |f=0> tensor m -> |f=1> tensor U+ m,
    |f=1> tensor m -> |f=0> tensor U- m.              (5)

The unitary block is [[0,U-],[U+,0]]. Starting at f=0 with the previous
second seed output reproduces every later state of the old algorithm.
The two earlier U+ preparation operations are retained explicitly in the
seed construction. The initial records are declared preparation resources;
their supply is not inferred from an external unrecorded scheduler.

All 64 coordinates (c,f,Fock) are acted on. In particular c=0 is not
deleted from the operator. Its flag does not flip, and the two branches are

    f=0: K G_N^3,         f=1: K G_N.                (6)

Every branch is orthogonal, so (4) is orthogonal on the whole carrier.
The initial c=1 subspace is invariant. The complete state, including f,
preserves inner products; forgetting f is not a faithful reconstruction
of this process on arbitrary input superpositions. No pure-state
nonlinear operation is asserted on the old sixteen-coordinate space.

## 3. The switch is an existing scene-history coordinate

Use the literal scene-history owner: Gamma consists of all 718 directed
edges (u,v) of K(9,11,13). Its degrees are 24,22,20. Every edge joins
different degree classes. Define

    f(u,v)=0 if deg(u)<deg(v), and 1 otherwise.

The actual reverseEdge exchanges f=0 and f=1. Each of the 359 unordered
edges therefore supplies the two switch coordinates in (5). This is a
bijection Gamma = (unordered edges) x Bool, derived from existing endpoint
degrees. It preserves every history and is invariant under every scene
automorphism. The degree labels are internal graph data; no distinguished
vertex or external orientation is chosen.

The actual carrier for the whole program is

    H = R^Gamma tensor R^{Bool_c} tensor Lambda*(R^4),
    dim H = 718*2*16 = 22976.                        (7)

C_cf is controlled edge reversal. C_fN is controlled by the intrinsic
edge flag. This is a concrete addressing map for the stated compiler
palette, not a proof of its physical actuation admission. No scene edge
is dropped; the 64-row block is repeated over all 359 reversal pairs.

An explicit seed populates both directions of every edge: in c=1 use
the prior A-band seed on f=0 and its U+ output on f=1. The first grade is
nonzero on every populated history fibre and retains the corresponding
sign after each program step. Each such fibre has q=eta,Q=I throughout.
This binds the conditional local pairing on that invariant sector. Scene
adjacency is not silently identified with a physical A4D connection or
with a varying metric mesh; neither an interacting spacetime field law nor
all off-sector physical equations is supplied by this flat example.

## 4. The original two readouts, on the complete carrier

Retain the actual endpoint lift J and average C=D^-1 J^T. Thus P_Gamma=JC
is the counting-Hilbert orthogonal projection, and

    T=CRJ=D^-1 A,      Delta=I-T.

On matter retain the original P_m=I-N, rank eight. The combined readout is

    Pi=P_Gamma tensor I_c tensor P_m,   rank Pi=528.

It preserves both values of c. It is not I_Gamma tensor P_m, an endpoint
reset, a new blank, or a conditional trace over only the occupied c=1
sector. For the fixed whole word W define the already owned functional

    F_k=Pi (W^k)^T (I-Pi) W^k Pi,
    J_k=-log det(I_H-z F_k),             0<z<1.       (8)

All of H, including zero feedback eigenvalues, is retained. Orthogonality
gives 0<=F_k<=I; the pencil is positive for the entire stated z interval.
On the prepared endpoint space the pairing is D, not the unweighted
identity. Compression M_k=C W^k J with the matter cut included yields
`F_(k,coarse)=I-M_k^dagger_D M_k`. Sylvester's identity gives the same full
determinant with the remaining ambient eigenvalues equal to one.

### One actual tick

For c=1 the matter compression of either U sign is a I_8. Edge reversal
therefore gives M_1=a T tensor I_8 and

    F_(1,c=1)=I-p T^2
              =p^2 I+p(2 Delta-Delta^2),             (9)

with all eight matter copies. This is a directly constructed coupling of
the existing golden record and scene-history feedback. It is not a new
assumed field action. The former 30-dimensional balanced scene kernel is
retained, with eigenvalue one of this feedback.

For c=0 there is no reversal. Put

    b=cos(3 theta)=a(4p-3),     a=cos(theta),
    w=(13b+9a)/22=a(26p-15)/11.

The notation is shorthand for powers of G; no angle is fitted. Incoming
flags are all zero in the degree-24 zone, all one in the degree-20 zone,
and occur 13:9 in the degree-22 zone. Thus M_1 is scalar b,w,a on the
three zones, with eight matter copies in each case.

The literal T has 30 zero eigenvalues and a three-zone characteristic
polynomial `(lambda-1)(lambda^2+lambda+39/160)`. Define

    B(z)=(1-z)^2+(41/80)zp(1-z)+(1521/25600)z^2p^2,
    L_b=1-b^2,  L_w=1-w^2.

The complete one-tick determinant is

    det(I_H-z F_1) = (1-z)^240 (1-zp^2)^112
                     * B(z)^8 * (1-z L_b)^72 * (1-z L_w)^88. (10)

Its degree is 528, as required by the complete feedback rank. The exponent
112 includes the eight constant scene modes of c=1 and the 104 matter
modes in the last zone of c=0. The other 22448 ambient modes are included
as unit factors, not removed by changing the carrier.

### Two actual ticks

Put r=2p-1=cos(2 theta), r3=4r^3-3r=130p-81=cos(6 theta), and

    v=(13r3+9r)/22=(854p-531)/11,
    L=1-r^2=4p^3,  L3=1-r3^2,  Lv=1-v^2.

On c=1 the two reversed histories return to the same edge. The four low
spatial pairs give M_2=1 and the four high pairs give M_2=r, independently
of the orientation. On c=0 the low pairs have compressions r3,v,r on the
three zones, and all high pairs have compression one. Therefore

    det(I_H-z F_2)=(1-zL)^184 (1-zL3)^36 (1-zLv)^44. (11)

The feedback rank is 264, with all other 22712 ambient unit factors
retained. Deleting the unoccupied c=0 record sector would leave only
`(1-zL)^132`, which is a different price. Ordinary determinant and the
full auxiliary spectrum are essential, even when the realized state
starts in c=1. Equations (10)-(11) do not infer a ten-component stress
tensor or an on-shell condition from a scalar price.

## 5. What this closes and what must be carried into the metric problem

The previous amplitude-sign oracle now has an exact fixed-word realization
with an internal switch, its extra record, a complete scene carrier and
the real endpoint/matter readout. The Gram obstruction explains why the
switch cannot simply be erased from the complete state. The combined
kernel (9) and full prices (10)-(11) are fixed by this explicit word and
these owned readouts. The native coefficients p and the scene counts are
not fitted to an Einstein target.

Remaining premises are concrete: the operational admission of this addressed
word and its initial records, its placement on an independently admitted
common (q,D,b,m) preparation, the actual metric/link/refinement transitions
and their full tangent, and the native whole-price stationarity equations.
The construction does not classify all permitted words or prove that this
one is selected. Matrix-price differences alone do not establish physically
different Euler operators; action, Euler and physical quotient freedom
retain their separate obligations.

No external `stage += 1` is used. The prior exact-storage and hereditary
maps remain available, with their capacity/admission scope. An endogenous
refinement rule must preserve this **whole** processor and its price,
including its retained controller. A source/Ward theorem, quantitative
native contrast, curved roots, soundness/recovery and GR must use that
same actual preparation and its permitted variations.

The exact executor and paired certificate bind every 64-row gate column,
all 718 histories, all 528 retained endpoint/matter columns, the complete
one/two-tick feedback, and the old seed orbit. Generic kernel propositions
and their actual compilation receipt are separate evidence; the whole
scene/processor binding and physical admission are not promoted to a new
supported CORE owner.
