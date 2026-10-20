# Complete memory minimization in the cyclic-history realization

Existing research #310. Input SOURCE
`d64296ce4dcb937abc440ece03e49e50442db4e8`; main
`fa2b04b9c8aae5a0b8470322d6091712ce56567a`. 12 October 2026.

This consumes the entire word preparation in
[the cyclic-history proof](A4D_NATIVE_CYCLIC_HISTORY_PRICE_PREPARATION.md).
Its earlier nonzero memory direction was off minimum. Here the full
two-term bootstrap is minimized over **every** closed word with the stated
one-step frequencies, including arbitrary order correlations. Finite
minima exist, their feedback values tend uniformly to zero, and a stronger
prefix-constrained minimum construction retains the complete previous
record. No enumeration of candidate histories is needed for the proof.

The class remains the explicitly declared cycle heat, visit-fiber readout
and two-step feedback realization. Its physical admission, golden clock,
4D archive refinement and map to constrained `(q,D,b,m)` are unproved.
The theorem does not minimize the unevaluated full D0 matter/action stack
or identify word minima with continuous native Euler roots. Section 6 also
tests this realization against the actual golden recorded operator, with
a uniform quantitative obstruction to the stated joint representation.

## 1. Same-input coarse geometry and complete variational domain

Fix any symmetric positive integer array A on **all** 359 actual scene
edges, zero elsewhere. Let L0=sum_(i,j) A_ij, D=diag(A1), and choose an
Euler word w having N1(w)=A. Its existence is proved in the consumed
all-walks construction. Root it at 0 and let its first neighbor be b.
D here is the visit-count pairing, not the transport D in the physical
constraint D q_t D^T=q_s; no map between those types is supplied.
All words below use the actual `SceneStep`, `composePath` and
`SceneHistoryFamily`, with the complete retained record.

For each K>=1, let W_K(A) be ALL closed valid rooted words of length KL0
having N1=KA. This is a finite nonempty set: repetition of w is a witness.
No prescribed N2 or Markov assumption is included in this domain.

On the complete record carrier use exactly the preceding P, U and
Delta_L=2I-U-U^T. The normalized visit pairing D/L0 and the compression
of the canonical heat are determined by the same word:

    T1=D^-1 A,
    C Delta_L J=2I-T1-T1^dagger=2(I-T1).                   (1)

For every word in W_K, the raw pairing is KD, but its normalized pairing
is D/L0. Thus (1) and the entire normalized coarse Dirichlet geometry are
fixed throughout the memory fiber and across K. Raw total record volume
grows; it is not identified with a physical volume or metric.

At fixed beta>0 and 0<z<1 the actual two-term bootstrap is

    B_L(w)=H_L+S2(w),
    H_L=beta^-1 log Tr_(R^L) exp(-beta Delta_L),
    S2(w)=-log det(I_33-z(I-T2^dagger T2)).                (2)

Every one of the L heat modes is retained. On W_K the whole H_(KL0) is
identical, so minimizing (2) is exactly minimizing S2. The contraction
proof from the preceding construction gives 0<=S2<infinity.

Any fixed additive edge valuation is constant on W_K, since its value
is K sum w_ij A_ij. It cannot select a different memory minimizer there.
Such a term may have a separate response when A changes; this theorem
does not remove that response from the unevaluated action stack.

## 2. An admitted return operation with exact counts

For odd q=2m-1>=1, replace every one-step arrow u->v in a closed word by

    u,v,u,v,...,u,v              (q steps, same endpoints).

Denote the resulting full word E_q(w). Every inserted arrow is legal by
the actual symmetry of SceneStep; composition completeness admits the
entire word. No inverse cancellation erases the recorded returns. Direct
counting gives, for ANY closed word, including non-reversible ones,

    D(E_q(w))=q D(w),
    N1(E_q(w))=m N1(w)+(m-1)N1(w)^T,
    N2(E_q(w))=(q-1)D(w)+N2(w).                           (3)

Proof: an original oriented edge contributes m forward and m-1 backward
arrows. At each old junction there is exactly one two-step pair with the
old initial and final labels. Every other two-step pair returns to its
own label. Incoming and outgoing visit counts coincide on a closed word,
giving the first and third identities. The cyclic closing junction is
included. Reversibility is essential to the next specialization:

    N1(E_q(w))=q A,
    T2(E_q(w))=(1-1/q)I+(1/q)T2(w).                       (4)

## 3. Uniform minimum bound over the whole frequency fiber

For any contraction T in the weighted D pairing, and 0<=alpha<=1, put
T_alpha=(1-alpha)I+alpha T. It is a contraction. Its positive feedback
obeys

    F_alpha=I-T_alpha^dagger T_alpha
      =alpha(2I-T-T^dagger)-alpha^2(I-T)^dagger(I-T),
    0<=F_alpha<=I,               ||F_alpha||<=4alpha.

For an eigenvalue 0<=f<=1,
-log(1-zf)<=zf/(1-z). The complete feedback has rank at most 33, hence

    0<=S2(T_alpha)<=C_z alpha,       C_z=132z/(1-z).        (5)

This is independent of the edge weights, their smallest value, all order
correlations and every heat eigenvalue. It follows from the actual whole
operator formula, not a spectral profile chosen for a source.

Define f_K(A)=min_(v in W_K(A)) S2(v). Finiteness and nonemptiness prove
attainment by a genuine global minimum of (2) within this complete class.
For every odd q, (4)-(5) give

    0<=f_q(A)<=C_z/q.                                     (6)

Consequently the relaxed feedback infimum at fixed normalized coarse
geometry is zero for EVERY positive reversible integer frequency array.
This conclusion concerns minimum values, not an assumed on-shell gate.

### No finite zero is hidden in the proof

Every word in W_K(A) has S2>0. If S2=0, positivity would give F2=0,
so U^2 preserves the finite label-readout algebra. Thus there is a
permutation sigma of the 33 labels satisfying w_(t+2)=sigma(w_t).

For odd length, U is a power of U^2, and every label has one possible
successor. This contradicts all native outgoing edges being present.
For even length, the even and odd positions trace at most two sigma
orbits. If these orbits are disjoint, the observed graph is bipartite,
contradicting the present triangle 0--9--20--0. If they intersect they
coincide and include all 33 vertices. Each label then has at most two
successors, one from each parity; actual degrees are 20,22,24. This is
again impossible. Therefore f_K(A)>0 at each finite K, although (6)
forces the relaxed infimum to zero. A finite minimum and a zero limit
are distinct statements. Merely visiting all vertices would not prove
this: a Hamiltonian scene word has P=I and S2=0 but omits most edges.

## 4. Minimum extensions with the whole past retained

Let p be ANY closed past word starting with (0,b) and N1(p)=KA. Its
entire original list is kept as a prefix. Append E_q(w) using composePath.
Both first neighbors are b; this suffices for the cyclic two-step junction
counts to add. Thus the actual candidate r=p composed with E_q(w) has

    N1(r)=(K+q)A,
    N2(r)=N2(p)+(q-1)D+N2(w),
    T2(r)=(1-alpha)I+alpha Tbar,
    alpha=(K+1)/(K+q),
    Tbar=[K T2(p)+T2(w)]/(K+1).                           (7)

Tbar is a contraction in the same pairing. For ANY prescribed n>=1 choose
q=2n(K+1)+1, an odd integer. Then

    Knew=(2n+1)(K+1),           alpha=1/(2n+1).

The set of ALL words extending p, of length Knew L0 and with one-step
counts Knew A, is finite and nonempty by (7). Every minimum of its whole
price obeys

    0<S2_min<=C_z/(2n+1).                                 (8)

This is uniform over ALL pasts in the declared fiber, including past
minimum branches whose detailed order was never computed. Repeating this
procedure gives a nonempty set-valued sequence of minimum extensions,
with K0=1 and K_n=(2n+1)(K_(n-1)+1). The first two entries and every prior
record persist literally. Finite existence, not a fitted selector or
enumeration, proves recovery of such complete histories. All newly added
heat modes remain in the price.

This is actual admissible history composition and prefix retention.
An intertwiner of the full cyclic operators across an append seam is not
claimed. The construction is not the native golden or 4D physical
refinement, and these minimum histories are not physical GR solutions.

## 5. Minimum-value contrasts and the source consumer

Take ANY two positive reversible arrays A_plus,A_minus with the SAME
total L0. At step n their K_n and entire heat terms coincide. For either
unconstrained minima or the prefix-minimum extensions above, the actual
half contrast therefore satisfies

    |[B_min(A_plus)-B_min(A_minus)]/2|
       <=C_z/[2(2n+1)].                                  (9)

The two arrays and past orders may depend on n; the bound is uniform.
For prefix minima this means admissible pasts with the corresponding
frequency array at each comparison level. A fixed A gives the actual
coherent tower in Section 4. Varying probe arrays do not acquire a common
cross-level physical transition from this levelwise bound.
At epsilon=n^(-1/3), the absolute central response is at most
(C_z/4)n^(-2/3). This is a response of independently specified minimum
value functions. It is not the derivative of a finite word, a lifted
ten-component metric probe, or stationarity of every excluded direction.

The earlier off-minimum memory derivative is thus not retained by this
complete memory-minimum limit. In the named realization, coarse heat
compression (1), freely realized reversible frequencies and elimination
by the whole two-term minimum do not supply a nonzero limiting shape
source at one fixed calibration. A physical preparation needs an owned
law relating the actual clock/readout/heat and remaining contributions,
or independently admitted restrictions on these history variations.
Such a law must be proved; the forbidden restriction cannot be defined
as the desired Einstein response. The actual golden fixed-compression
class and the full D0 action stack are outside this theorem.

## 6. The actual golden recording operator tests native admission

This class has a stronger representation boundary than the minimum-value
limit. The actual owner `Representation/GoldenCoherentMemory.lean` defines,
in system/record order 00,01,10,11,

    R=fullStep(a,p)=[a,0,-p,0; 0,a,0,-p; 0,p,0,a; p,0,a,0],
    p=primitiveRoot=(sqrt(5)-1)/2,       a=sqrt(p).

Its owned `blank_record_evolution` supplies the blank-record plane
P0=diag(1,0,1,0). This is the span of its actual input (u,0,v,0), not a
new physical sector. The native primitive identities make R orthogonal.
On that plane the compression is

    P0 R P0, restricted to im P0 = [a,-p;0,0],
    ||(P0 R P0-(P0 R P0)^T)/2||=p/2.                      (10)

In EVERY word of W_K(A), the whole cyclic compression PUP is symmetric:

    PUP=J D_word^-1 N1 D_word^-1 J^T,

and N1=N1^T. Consider ANY real or complex isometry V from the four
recorded coordinates into the whole L-coordinate carrier, retaining all
ambient directions, and define its two actual binding errors

    delta=||U V-V R||,
    eta=||P V-V P0||.

Then, for every carrier length, frequency array and ordered word,

    delta+2eta >= p/2 > 3/10.                             (11)

Proof: M=V^dagger P U P V is self-adjoint. Put X=PV and Y=VP0. Both have norm
at most one. The difference between X^dagger U X and Y^dagger U Y has norm at
most 2eta. Further,
||P0(V^dagger U V-R)P0||<=delta by isometry. Therefore
||M-P0 R P0||<=delta+2eta. The distance from P0 R P0 to ANY self-adjoint
matrix is at least the norm p/2 of its antisymmetric part, proving (11).
The strict rational bound follows from sqrt(5)>11/5. No spectrum scan,
large-word assumption, selected state or source is involved.

Thus exact preservation of this recorded clock and its actual blank-record
projection is impossible in the entire reversible conditional-label
realization. Vanishing-error preservation of both is also excluded, even
with arbitrarily large carriers and full retained complements. If eta=0,
the clock error alone is at least p/2; if delta=0, the projection error is
at least p/4. Changing embedding phases alone does not remove the bound.
This is an operator representation result, not a claim that
the finite apparatus owner already proves physical clock admission.

Exact representation is also excluded for ANY injective linear V, without
assuming it is normalized. Indeed H=V^dagger V is strictly positive.
Exact clock intertwining and unitarity imply R^dagger H R=H; exact
projection intertwining and self-adjointness imply H P0=P0 H.
Thus H^(-1/2) commutes with both R and P0, and V H^(-1/2) is an isometry
with the same exact intertwiners, contradicting (11). This uses only
finite positive diagonalization. The approximate numerical bound (11)
is stated for isometries: scaling an injective encoding to zero scales
both absolute errors to zero while losing its normalized readout.

This identifies the failed preparation implication precisely. Legality
of every path does not prove a joint operator representation of the owned
golden recorded operation and its input readout. A joint preparation that
uses those two owners must preserve their noncommuting structure or prove
a different physical readout relation. Non-reversible frequencies, coherent
readout algebras, other operations and relational physical preparations
are outside (11). None is selected here. The fixed-golden-compression
feedback theorems remain unchanged.

## Verification and preserved obligations

The companion exact replay checks both stretching laws, full operator
controls, normalized coarse geometry, strict finite feedback, actual
prefix extensions and the rational bound. Non-reversible words and a
full-vertex Hamiltonian word guard the necessary hypotheses. All-size
minimum existence, interval inequalities and the no-zero argument above
retain their analytic status. The literal golden matrix, blank input plane,
its exact antisymmetric norm and the full reversible compression are also
checked. The all-isometry bound (11) is the analytic argument above.
No new Lean theorem is claimed.

This completes this proposed cyclic-word internal-minimum mechanism. It
does not close native common preparation, source/Ward, native stationarity,
curved joint roots, soundness/recovery or the original #310/#202/#317
terminals. The existing T0--T3 and 44-node graph remain open. The next
consumer is the precise native clock/heat/readout admission implication;
another unconstrained word, spectrum or hidden heat variation cannot
repair the mechanism classified here.
