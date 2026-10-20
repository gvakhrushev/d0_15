# Cyclic recorded histories and the full price comparison

Existing research #310. Input SOURCE `5a4c5eacec603d04b2b5e6e73ce9ba2aab8d119d`;
main `fa2b04b9c8aae5a0b8470322d6091712ce56567a`. 11 October 2026.

This tests the history-gluing route at its missing preparation step. An actual
closed scene word determines its readout projection, pairing and every return
matrix. Positive rational edge frequencies are realized by complete scene
words, rather than installed as free conductances. On the explicitly stated
cycle-heat realization, their paired **whole-price** contrasts converge to the
weighted return law with an explicit error. Two ordered records with identical
one-step frequencies nevertheless have different two-step prices, and this
difference persists under repetition with all added heat modes retained.

The result is an analytic construction in the owned all-walks interface plus
an exact certificate. It does not prove physical selection of this joint
cycle/readout realization, identify a physical metric or change T0. In
particular, the cycle heat is an existing operator used in a specified common
realization; it is not asserted to be the uniquely forced physical heat law.

## The complete recorded carrier

Let L>=3 and let w=(w_0,...,w_(L-1),w_0) be a closed valid walk on the literal
`Adj31` scene, visiting all 33 vertices. Its membership in every composition
complete `SceneHistoryFamily` follows from
`ScenePathHistoryCanonicity.composition_complete_eq_all_walks`. This is history
admission in that exact interface, not the separate physical representation
predicate. The whole ordered word, including repeated visits, is retained.

On H_L=R^(Z/LZ) use the literal `archiveShiftMatrix L`,
`(Uf)(t)=f(t+1)`. The actual unscaled `archiveCanonicalLaplacian (L-2)`, after
the Fin/ZMod index equivalence, is Delta_L=2I-U-U^T. Its full carrier has L
modes, including the constant zero mode. The L>=3 condition avoids the
two-vertex edge-count convention. Set

    n_i = #{t : w_t=i},            D=diag(n_i),
    J(t,i) = [w_t=i],             C=D^-1 J^T,
    P=JC,                        N_k(i,j)=#{t : w_t=i, w_(t+k)=j}.

All n_i are positive. The counting pairing gives J^T J=D, CJ=I, and P is the
unique orthogonal projection onto the label-readout subspace im J. Thus its
normalizer and pairing are determined by the same record. This is the
Reynolds/conditional-average construction of the endpoint owner, applied to
the actual visit fibers; it is not the fixed uniform average over all 718
possible generating arrows and not a multiplication event projector.

No record is erased by U or by the definition of the action. P specifies a
readout subspace; its complement is retained in the full feedback operator.
The scalar label map alone is insufficient to prescribe an active physical
subspace without the stated readout interpretation.

## Exact full price and returns

The complete k-step operator is U^k, not the kth power of its compression.
Writing T_k=C U^k J=D^-1 N_k and T_k^dagger=D^-1 T_k^T D gives

    F_k=P (U^k)^T (I-P) U^k P
       =J (I-T_k^dagger T_k) C,
    det(I_L-z F_k)=det(I_33-z(I-T_k^dagger T_k)).             (1)

Proof: expand F_k=P-P(U^k)^T P U^k P, using orthogonality of U^k,
P^2=P and CJ=I. Then apply det(I+AB)=det(I+BA). In normalized coordinates
J D^-1/2 is an isometry, and its compression of U^k is a contraction.
Hence F_k>=0, F_k<=I and the pencil is positive for 0<z<1. The full
complement contributes identity factors to THIS determinant, not to the
heat trace. An exact rational formula avoiding square roots is

    det(I_L-z F_k)
      = det((1-z)D+z N_k^T D^-1 N_k) / det D.               (2)

Insert these actual operators into the existing bootstrap, at fixed beta>0:

    B_(L,k)(w)= beta^-1 log Tr_HL exp(-beta Delta_L)
                 -log det(I_L-z F_k(w)).                   (3)

For two words of the SAME length the entire heat terms in (3) are identical.
Their cancellation in a paired contrast is exact. Heat is not replaced by
I-T_k or by a 33-dimensional compressed heat trace. The full heat term
generally changes with L and remains part of (3).

Here "whole price" means both terms of this named bootstrap on the whole
carrier. Additional matter/action-stack contributions are not evaluated by
this result; their cancellation or stationarity is not inferred from (3).

Vertex relabeling leaves the visit partition P unchanged. A change of cyclic
origin conjugates P by a power of U, which commutes with Delta_L and U^k.
Consequently the whole price is invariant under these catalogue changes.
This proves those concrete symmetries; it is not a proof that they exhaust
the physical M1 comparison catalogue.

## Realized frequency variations and a uniform paired estimate

For every positive symmetric integer array a_ij supported on the 359 scene
edges, there is a closed scene word having exactly a_ij occurrences of each
directed transition i->j. Indeed the directed multigraph has equal incoming
and outgoing degree and is connected. Start a trail until returning to its
initial vertex; balance prevents it ending elsewhere. If unused edges
remain, connectedness supplies a visited vertex incident to an unused edge.
Splice in another closed trail. The finite number of unused edges strictly
decreases, proving the construction. This also gives a deterministic checker.
It realizes every such integer array without adding a transition forbidden
by Adj31. This is not a claim about arbitrary non-reversible frequencies.

In particular let E have entries E_0,9=E_9,0=1 and
E_0,20=E_20,0=-1, all others zero. For even m>=2 and integer |r|<m, use
a=m Adj31+r E. The word has L=718m, lies in L in 4N, and gives

    T_1(t)=D(t)^-1 A(t),  A(t)=Adj31+t E,  t=r/m,
    D(t)=diag(A(t)1),     N_1=m A(t),     D_word=m D(t).      (4)

Thus the positive conductance pencil is realized by discrete complete
histories. Its smooth parameter is a limit of frequencies, not a presumed
continuous operation on the literal discrete word space. All changes in
the degree, pairing and projector are included in (1)-(4).

For |t|<=1/2, let V(t)=D(t)^-1/2 A(t) D(t)^-1/2. Its norm is at most one,
d_min>=19, ||A||<=25, ||E||<=2, ||D'||<=1, and direct product
differentiation gives

    ||V'(t)|| <= 2/19+25/19^2 < 1.

For G(t)=-log det(I-z(I-V(t)^2)), integration of the log-det differential
on the positive pencil yields

    |G(t)-G(s)| <= 66 z/(1-z) |t-s|.                       (5)

Choose nearest r/m for each of two prescribed endpoints in [-1/2,1/2]
(m even makes the boundary endpoints exact). Every rounded endpoint is
realized by (4), on the same full carrier L=718m. Equation (3) and (5) give

    | 1/2[B(w_+)-B(w_-)] - 1/2[G(t_+)-G(t_-)] |
        <= 33 z/((1-z)m).                                 (6)

There is one calibration, a=1. No heat counterterm, branch normalization or
record deletion is used. Formula (6) transfers to this weighted return
observable. It does not identify it with the Einstein action, identify
1/m with a physical mesh, or supply ten physical metric probes.

The first variation of the limiting observable is nonzero generically.
At t=0, kappa=39/160 and kappa'=359/1161600. The exact previously owned
359-edge first-jet quotient gives

    G'(0) = [2z(1-z(1+kappa)) /
             (1-z-2z(1-z)kappa+z^2 kappa^2)] * 359/1161600. (7)

It vanishes at z=160/199; this protected exception is retained. At the
non-selected test value z=1/2 it is 359/1207230. This derivative is not
called a native metric stress or a stationarity equation.

## Ordered memory cannot be replaced by the frequency matrix

Construct the deterministic Euler tour c from a_ij=2 Adj31, rooted at 0.
The checker removes the largest available next vertex at each traversal,
using the standard stack-and-splice construction above. It has 1436 steps.
Append the following four valid rooted excursions:

    w_A = c ++ [9,0,10,0,20,0,21,0],
    w_B = c ++ [9,0,20,0,10,0,21,0].

The shared junction 0 is already the last entry of c. Both are valid closed
words of length 1444, visiting every scene vertex. Their D and N_1 agree
exactly. Their N_2 differ. At z=1/2 the exact determinant ratio Q_B/Q_A,
where Q denotes the full k=2 determinant (2), is

    2264614049780991122023011170469392279903682384941660442507474001136938861603830599165869
    /2257973250713359853410106616817091973348189178756999414057550441878571609489560253883093.

It is strictly greater than one. Therefore B_(1444,2)(w_A)-B_(1444,2)(w_B)
is its positive logarithm, approximately 0.00293672776184126, for every
beta>0. The unequal rational determinants, not the decimal approximation,
certify the gap. The complete word recipes and their arrays are retained
in the exact ledger.

This disproves descent of this composed full price through (D,N_1), even
though the heat operator is fixed and no independent hidden heat is varied.
It excludes a source reconstruction from only that one-step observable.
It does not exclude a joint readout retaining the relevant memory m, and
does not identify this observation with the fixed-source/raw-owner terminal.

## A full memory variation at fixed one-step reading

The witness is not only a comparison of two isolated records. Both words
have first two entries (0,32) and last two entries (21,0). Concatenate n
of these closed words using the actual `composePath`, with a copies of w_B
and n-a copies of w_A, in any order. Call the result W_(n,a). Every block
has the same two-step junction data, so direct counting, including the
cyclic closing junction, gives

    length(W_(n,a))=1444n,
    D_(n,a)=nD,       N_(1,n,a)=nN_1,
    N_(2,n,a)=(n-a)N_(2,A)+aN_(2,B).                      (8)

Thus the entire one-step readout is fixed at each n. All positive native
edges and every vertex remain. For EVERY fixed additive scalar valuation
on the actual path category the cost is also independent of a: the complete
additive-action theorem in `A4D_NATIVE_HISTORY_ACTION_BOUNDARY.md` gives
S(W)=sum_(i,j) w_ij N_1(i,j). This includes the canonical unit-step cost,
any positive ActionProtocol completion with additive extension, and the
stated Perron negative-log extension cost. No choice of those edge weights
can detect this variation. This conclusion concerns these exact additive
interfaces, not arbitrary noncommutative action readings.

Set N(theta)=N_(2,A)+theta B, where B=N_(2,B)-N_(2,A), 0<=theta<=1.
For fixed z=1/2 write

    M(theta)=(D+N(theta)^T D^-1 N(theta))/2,
    R(theta)=det M(theta)/det M(0),
    g(theta)=-log[det M(theta)/det D].

Equation (8) realizes g(a/n) exactly as the feedback part of the WHOLE
bootstrap of W_(n,a). Heat is still the complete same-length heat term.
There is no assumed continuous deformation of a finite word.

For the literal witness, B=XY has rank two, with

    X=[e_20-e_9, e_9-e_10],
    Y=[(e_10-e_21)^T; (e_20-e_21)^T].

Put V=[N(0)^T D^-1 X, Y^T] and

    K(theta)=[0, theta I_2; theta I_2, theta^2 X^T D^-1 X].

The exact determinant lemma gives the four-by-four identity

    R(theta)=det(I_4+(1/2)K(theta)V^T M(0)^-1 V)
            =1+c_1 theta+c_2 theta^2+c_3 theta^3+c_4 theta^4. (9)

The certificate computes all four rational coefficients from the full
33-by-33 matrices; their complete fractions are in its ledger. Each is
strictly positive. Exact rational comparisons give

    c_1/R(1)>1/1000,
    R'(1)<1/100,    R''(1)<1/100,    R'''(1)<1/100.

These checks, together with (9), prove for EVERY theta in [0,1]

    -1/100 < g'(theta) < -1/1000,    |g'''(theta)|<1/50.     (10)

Indeed R>=1, its first three derivatives are nonnegative and bounded by
their values at one, while R'>=c_1 and R<=R(1). Differentiating -log R
gives the third-derivative bound
1/100+3/10000+2/1000000<1/50. This is a full interval proof from a rational
polynomial, not a sample of candidate points. In particular, replacing one
w_A block by w_B at fixed n lowers the full bootstrap by at least
1/(1000n). There is no stationary interior of THIS prepared block-mixture
curve. Its endpoint and other native directions are not classified here.

There is also a controlled variational readout. Let n>=8,
epsilon=n^(-1/3), and choose a_+/n and a_-/n nearest to 1/2+epsilon and
1/2-epsilon. With Delta B_n=[B(W_(n,a_+))-B(W_(n,a_-))]/2,

    |epsilon^-1 Delta B_n-g'(1/2)| <= (1/120)n^(-2/3).      (11)

The rounded price endpoints each have error at most 1/(200n) by (10).
The central difference error is at most epsilon^2/300. Summing the two
contributions after dividing the half contrast by epsilon gives (11).
The exact g'(1/2) lies between -3/1000 and -2/1000. Calibration is one;
there is no heat subtraction beyond cancellation of equal full terms.
Here 1/n is a block-frequency resolution, not an identified physical mesh.

Consequently this bootstrap cannot descend through the whole one-step
frequency reading, or equal a calibrated additive edge action plus any
function of that reading, on this family. Its omitted order variable has
an explicit nonzero first response and genuine finite decreasing moves.
Calling that variable gauge would remove a price-observable direction.
A physical quotient must instead retain sufficient m, prove its own
equations remove the response, or use an independently justified different
price/readout binding. Equations (10)-(11) do not supply that physical
binding, the (q,D,b,m) constrained tangent, or its stationary solutions.

## Repetition preserves the paired gap while retaining new modes

Repeat a closed word r>=1 times. It is still an admitted all-walks word,
now of length rL; its old record is a literal prefix. Counts satisfy
D_new=rD and N_(k,new)=rN_k for every fixed k. Thus every determinant in
(2) and every paired contrast between two such repeated words is unchanged.

There is also an explicit comparison isometry B_r f(t)=f(t mod L)/sqrt(r).
It satisfies U_new B_r=B_r U, Delta_new B_r=B_r Delta and
P_new=B_r P B_r^T. These follow entrywise from periodicity. The last identity
is for the whole conditional-average projection; replacing it by r separate
copies of P changes the experiment and raises the determinant to the rth
power. The new heat trace still includes all rL modes. Its difference
between the two equally long repeated histories remains zero.

This is word repetition and its explicit cyclic covering comparison. It
is not identified with the golden Hilbert inclusion, the consecutive
archive refinement, or the physical metric refinement without a further
intertwiner. No uniform physical-mesh conclusion is inferred from it.

## What premise changed

Within the all-walks/cyclic-record realization, the degree weights, conditional
projection and return operators now come from one full retained history.
The earlier assumption of freely supplied positive conductance variations
has been replaced by an explicit integer realization and the controlled
finite paired contrast (6). Ordered memory supplies a genuine full-price
effect invisible to the entire one-step frequency matrix, with an exact
retained refinement control. The actual concatenation law furthermore
realizes a strictly decreasing memory curve at fixed one-step reading,
with the uniform finite-probe estimate (11). Every additive edge valuation
is exactly blind to this curve; it cannot be silently identified with this
composed bootstrap.

Physical admission of this particular cycle/readout/heat combination and
its map to (q,D,b,m) are still required. In particular the theorem does not
authorize holding these operators fixed or independently varying them when
the physical metric changes. The next consumer must identify that common
physical preparation and retain at least the memory needed by its actual
price. No new heat profile or neighbouring word census is justified by this
result. Source/Ward, native stationarity, curved roots, soundness/recovery
and all original #310/#202/#317 contracts remain open.

The companion `a4d_native_cyclic_history_price_check.py` reproduces the
integer words, full finite-matrix controls, exact determinants and symbolic
jet, with executed substitutions that would lose order, pairing or full
heat. Its default mode only compares an immutable certificate. These new
analytic theorems are not labeled Lean-formalized.
