# Full minimal real memory-actuation family and the owned Q8 word boundary

Research parent: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, [#310](https://github.com/gvakhrushev/d0_15/pull/310).
Input head: `d8b8f0712da3ddb23f966ed7b13b4e06b4973a71`.
Base: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Date: 2026-10-09.

The [verified archive packet](A4D_NATIVE_VERIFIED_ARCHIVE_ACTUATION.md)
forces archive interaction from independently represented comparison
truth and classifies all 16 minimal real comparator completions. This
packet retains coherent phases in BOTH recording directions. It closes
the complete declared minimal four-real-coordinate family for the
specific operator transfer: a uniform old-memory golden gate, retaining
every active/workspace state. It does not claim that this carrier
exhausts D0, that all state preparations require this operator, or that
a physical representation is supplied by a matrix classification.

## 1. Independent specifications and complete joint family

Keep the actual basis (active bit a, old record r). Let C be the already
bound forward registration C(a,r)=(a,r XOR a), R the reverse registration
R(a,r)=(a XOR r,r), and T the passive interchange of role coordinates.
The previous independent comparator specification is complete
orthogonality, commutation with the retained record Z, and correct new
flag Z outcomes on the two blank-flag inputs. Its entire family is
U=R diag(c0,c1,c2,c3), ci^2=1.

The recording specification is the same independent retention/truth
contract in exchanged coordinates: T F T obeys the comparator
specification. T in this definition changes coordinates; no physical
swap is assumed available. Equivalently F is complete orthogonal,
commutes with active Z, and writes active truth into old-record Z from
the two blank-record inputs. The kernel proves its complete family is
F=C diag(d0,d1,d2,d3), di^2=1. The two carrier subtypes are bijective;
each has 16 elements and their full joint family has exactly 256 pairs.
No unsigned phase completion is selected from M1 or Boolean truth.

Write pc=product(ci), pd=product(di). Both are +/-1, whereas
det(U)=-pc, det(F)=-pd. These determinants refer to the specified real
four-dimensional carrier, not an assumed physical parity postulate or
the determinant of a faithful complex realification.

## 2. Both complete transfer routes, with all phases retained

Let G=[[a,-p],[p,a]], G_a=G tensor I. The first signed exchange
S=U F U has columns

    (d0 e0, c1 c2 d3 e2, c2 c3 d2 e1, c1 c3 d1 e3).

Its exact complete conjugation is

    S G_a S^T = diag(G(a,s0 p), G(a,s1 p)),
    s0=d0 d2 c2 c3, s1=d1 d3 c2 c3=pd*s0.

Thus pd=+1 gives I tensor G(a,s0 p), with all active/workspace states
retained, even correlated ones. If pd=-1, the two branches have opposite
orientation. Declaring the result a workspace-independent old-memory
gate would delete an actual coherent phase effect.

The alternate signed exchange V=F U F gives

    V G_a V^T = diag(G(a,t0 p), G(a,t1 p)),
    t0=c0 c3 d1 d2, t1=c1 c2 d1 d2=pc*t0.

It is uniform if pc=+1. All ci,di are unit signs, so s0,t0=+/-1.
Both routes use the same owned p0 and a=sqrt(p0); no new continuous
angle, source or coupling parameter is chosen.

Both signed primitives satisfy U^4=F^4=I and U^T=U^3,F^T=F^3.
Consequently the complete first conjugation uses only 13 FORWARD
primitives in matrix order

    [U,F,U,G_a,U,U,U,F,F,F,U,U,U].

Chronological order is the reverse of this list. The alternate route
exchanges U/F in the same fixed code. It is independent of sign values
inside the declared parity sector. With the existing unsigned forward
C, C^-1=C reduces the first route to 11 forward operations for every
one of the 16 reverse completions. This is an additional bounded
specialization, not a phase-selection rule.

Exactly 192 of the 256 pairs have pd=+1 OR pc=+1; all have a uniform
route above. Each parity test admits 128 pairs and their intersection
has 64. The remaining 64 have pc=pd=-1. The next argument classifies
every word in their declared palette rather than stopping at these two
short routes.

## 3. The proper sector: use D0's actual Q8, not a word census

In the owned order-memory basis (1,i,j,k), let L_i,L_j,L_k be the real
maps of `Representation.OrderMemoryReadout.spin(2,4,6)`. The new
kernel statements bind these ACTUAL rational-owner definitions. Their
finite identities are proved anew in the capsule; imported
compiler-trust theorem leaves are not used.

The active rotation G tensor I is right quaternion multiplication by
a+p j, so it commutes with every L axis. The desired I tensor G is
left multiplication by a+p i. Every existing Q8 left operation
normalizes the six-point frame

    A={+/-L_i,+/-L_j,+/-L_k}.

When pc=-1, conjugation by U sends

    L_i -> c0 c1 L_k, L_j -> c0 c2 L_j, L_k -> c0 c3 L_i.

When pd=-1, F sends

    L_i -> d0 d1 L_i, L_j -> d0 d2 L_k, L_k -> d0 d3 L_j.

The signed coefficients have square one. Thus both proper primitives,
every Q8 operation, and EVERY normalized active rotation normalize A.
The palette is deliberately more generous than the one fixed golden
angle. It still excludes an assumed old-memory rotation, an
orientation-reversing exchange, and arbitrary additional operations.

Normalization is closed under matrix products. Induction on a list
proves that every complete finite word of any length in this entire
palette normalizes A. This is the all-word kernel theorem. Increasing
word length or enumerating further words cannot remove its invariant.

For H=I tensor G,

    H L_j H^T=(a^2-p^2)L_j+2ap L_k.

At actual p0, a^2=p,p+p^2=1,p>0: cos(2theta)=p^3>0 and
sin(2theta)=2p^(3/2)>0. Both are nonzero. This operator is outside A.
Hence H is not any word in the proper palette. The six-point set is
closed; complete matrix conjugation is continuous. The kernel also
proves that no sequence of arbitrarily long proper-palette words
converges to actual H. A numerical word/rank census is not the proof.

## 4. A quantitative complete-operator gap

Use the Frobenius norm in this four-coordinate carrier. The three
axes are orthogonal and each has squared norm 4. The exact six
squared distances of H L_j H^T from A are

    [8,8-8c,8-8s,8,8+8c,8+8s],
    c=p^3, s=2p^(3/2), 0<c<s<1.

Every proper-palette W is orthogonal and its conjugated axis belongs
to A. Thus its Frobenius distance from the target conjugated axis is
at least sqrt(8(1-s)). The identity

    W L_j W^T-H L_j H^T
      =(W-H)L_j W^T+H L_j(W^T-H^T)

and ||L_j||op=||W||op=||H||op=1 give an upper bound
4||W-H||op (each four-coordinate factor has Frobenius norm 2).
Consequently

    ||W-H||op >= sqrt((1-2p^(3/2))/2) > 0.

The exact certificate checks the six squared distances and positivity.
This quantitative norm inequality has the explicit elementary proof
above. The printed kernel terminal is the generic all-word and
no-vanishing-error result; a formal quantitative operator-norm theorem
is not silently substituted for it. Nor is this norm declared an
independently admitted gravitational detector.

## 5. Anchored reference vs fitting the experiment to its operation

For an independent own-angle reference x_phi=(a,p,0,0), compare after
H_sigma=I tensor G(a,sigma p) with any U_c. The represented new-flag
quadratic weight is

    weight_true(U_c H_sigma x_phi)=2p^3(1+sigma), sigma^2=1.

It equals 4p^3 for + and zero for -. This proof keeps the full vectors
and the complete comparator phases. The available preparation of an
INDEPENDENT reference and an operational calibrated flag remain
apparatus inputs; the algebra does not supply those admissions.

The hostile control prepares x=(a,sigma p,0,0) by the tested
orientation itself. It gives 4p^3 for BOTH orientations. A fitted or
co-moving reference cannot establish that the anchored distinction
has disappeared. A whole-frame conjugation by record Z transports
H_+ to H_- AND x_phi to the changed reference; readouts and other
apparatus operators must likewise be transported. Changing only the
tested operation is not that equivalence.

## 6. Full retained history refinement and budget boundary

For the literal complete normalized golden inclusion J_n and old
operator extension W_n=W tensor I, the kernel proves for any x,

    weight(W_n J_n x-H_n J_n x)=weight(Wx-Hx).

All histories, failed/ancillary records and correlated input are
retained. The obstruction is not diluted by passive tensor refinement.
This does not exclude a genuinely larger addressed ancillary
PROCESSOR: operations that mix the new roles can leave this palette.
The four-coordinate gate obstruction is also not an impossibility
theorem for every scene/state preparation.

The 13-operation substitution keeps the previously proved conditional
golden polynomial resource window. Primitive word length is not an
executed native MDL/runtime cost law. A matrix list does not derive
native addressing, a decoder, a blank coherent apparatus, its internal
full-word schedule, or the admission of both role placements.

## 7. Validation and next native consumer

The standalone capsule prints 59 new actual propositions and their
transitive axiom dependencies; prior bodies are not recounted. All 37
transitive D0 source pins, toolchain and prior-packet pins match. The
axiom union is Classical.choice, Quot.sound and propext; no placeholder
or compiler-trust leaf is accepted. The exact checker passes all
2409 controls, including every one of the 256 pairs and both
complete forward-only programmes, actual Q8 normalizers, all six exact
axis distances, independent/self-prepared reference controls and
complete retained cylinders. The checker rejects 24 false-scope and
16 false-exact ledgers.

This closes a precise child question under the first native-dynamics
goal: the full declared minimal real family is classified for complete
old-memory golden operator transfer, with a constructive 192-pair
sector and a Q8 all-word/no-approximation 64-pair sector. The unsigned
forward completion is no longer silently fixed when assessing the
larger family. Positive GR, G0b/G0/global closure and the original
#310 fixed-source/raw-owner terminal are not claimed; #202/#317 stay
independent.

The first next consumer is the native admission of the COMPLETE
apparatus: identify which already-owned coherent roles and addressed
operations are actually available. In the obstructed sector either
prove that an owned additional role/operation exits this exact Q8
normalizer while retaining all states, or prove completeness of the
palette for the intended apparatus. No arbitrary extra qubit, selected
coherent phase, old-memory gate or physical postulate is installed.

After that admission, the independently owned joint Delta/P/U,
complete variations and condensed refinement must keep the 653
complementary histories and both thermal-memory source defects. Own
metric/matter source/Ward, quantitative metric contrast and native
stationarity, curved joint roots, soundness/recovery and constraints
remain required. All parent contracts and historical results remain
open where their own terminals have not been established.
