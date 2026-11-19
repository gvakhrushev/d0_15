# An exact integral-ring boundary for a clean controlled Golden gate

25 October 2026. SAME PR334 / constitutive owner. Input publication
`49b78ad87365a2b62b99439781b2c244e7fac51f`; consumer: primary §7am.
This note closes one finite-word implementation question raised by
§7ak's positive conditional Gibbs point. It concerns the precise
literal G/CX/SourceI profile and computational clean-return interface.
It is not a universal restriction on physical D0 operations, measured
controllers, heralded instruments or scalar Golden probabilities.

## 1. The actual generators and the target interface

Consume the actual matrices and placement rules of
[native_execution.py](../d0_native_execution_domain_2026-10-24/native_execution.py),
the source-I inverse of primary §7j, and the supplied fixed-frame
known-port task of
[TASK_MAP.md](../d0_known_port_task_source_2026-10-25/TASK_MAP.md).
The matrices are

    p=(sqrt(5)-1)/2,   a=sqrt(p)>0,
    a^4+a²-1=0,
    G=[[a,-a²],[a²,a]],
    SourceI=diag(I4,L_i),
    L_i=[[0,-1,0,0],[1,0,0,0],
         [0,0,0,-1],[0,0,1,0]].                    (CB1)

CX is the addressed computational CNOT permutation. Source-spin bits
are not individually addressable by G/CX. Immutable oldRIGHT is not a
target OR control. A SourceI inverse is THREE actual SourceI letters;
the exact positive implementation of G^dagger has one G and four
SourceI letters, plus the real routing CX where required. All those
expanded primitives are included below. No negative-power or variable-
angle primitive, measurement, projection or normalization is added.

The desired coherent operator is

    CG=P_c0 tensor I_z+P_c1 tensor G_z,             (CB2)

identity on the other unknown/spectator factors, in this computational
control/target frame. It has to work on the WHOLE control/target input,
including superpositions and entanglement, not merely when c is known
to be1. A clean ancillary realization means a finite literal orthogonal
word W on this data plus finitely many computational auxiliary bits,
with the exact initialized-input identity

    W(|psi> tensor |0_aux>)
          =(CG|psi>) tensor |0_aux>                (CB3)

for EVERY data vector, including the original arbitrary spin input.
Any harmless reordering of these tensor factors is fixed in advance.
The auxiliaries return exactly and carry no residual success flag,
input-dependent garbage or approximate error. A fixed computational
basis string in place of0 gives the same argument. No arbitrary new
noncomputational reference state is supplied in(CB3).

## 2. Reduce the integral Golden ring, retaining its nilpotent part

All entries of every finite literal word lie in

    R=Z[a]=Z[x]/(x^4+x²-1).                         (CB4)

This is the integral ring, not the whole field Q(a): no denominator
or successful-branch renormalization is needed to multiply the raw
primitive matrices. The polynomial in(CB4) is the minimal polynomial
of a. For example Q(p)=Q(sqrt(5)) and the field norm of p is-1;
if p were a square in that quadratic field its norm would be a square
of a rational number, impossible. Thus sqrt(p) has degree4, proving
the stated monic degree-four presentation. This also agrees with the
owned exact Golden field used by the native matrix implementation.

There is consequently a well-defined reduction homomorphism

    R -> S=F2[x]/((x²+x+1)²),
    q=x²+x+1,   t=class(q),
    t!=0,       t²=0.                              (CB5)

Indeed x^4+x²-1 reduces modulo2 to x^4+x²+1=q².
The degree-two q is nonzero in the degree-four monic quotient, while
q² vanishes. Arithmetic has characteristic2 and

    x+x²=1+t,
    (1+t)²=1.                                     (CB6)

In particular1 and1+t are distinct UNITS. We never divide by t;
it is a nonzero nilpotent zero divisor. Reducing further to the field
F2[x]/q would kill t and lose the distinction needed by the proof.
The nilpotent quotient is essential, not an added physical degree
of freedom or a new scalar in the native programme.

## 3. Every full native word has one uniform reduced row sum

Let 1_d be the column vector of d ones, on the ENTIRE raw carrier,
including spin, dirty work, invalid/unprepared columns and every
computational auxiliary bit. This is an ALGEBRAIC witness vector,
not an assumed physically prepared plus state or free resource.
Put a bar over the reduction in S.
Both rows of a reduced Golden gate have the same sum:

    Gbar=[[x,x²],[x²,x]],
    Gbar 1_2=(1+t)1_2.                             (CB7)

Tensoring with identities and addressing/routing the gate preserves
this statement in the full dimension. Signs have disappeared modulo2.
A CX becomes a permutation, so CXbar 1_d=1_d. The specified L_i is
a signed permutation; hence SourceI also becomes a permutation and
SourceIbar 1_d=1_d. These facts use the actual fixed computational/
quaternion frame in(CB1), not arbitrary matrices commuting with L_i.

For two matrices M,N with M1=lambda_M 1 and N1=lambda_N 1,
(MN)1=lambda_N M1=lambda_M lambda_N 1. Induction on the literal
chronological word therefore gives

    Wbar 1_d=(1+t)^(n_G)1_d
       =[1+(n_G mod2)t]1_d.                        (CB8)

Every row has the SAME reduced sum, either1 or1+t. The full number
n_G counts each actual G letter, including those in inverse/routing
macros. It is not the number of logical rotations in a compressed
description. Any finite number of allowed dirty work bits, helper
visits, SourceI cycles and CX permutations preserves(CB8).

This is a word invariant, with no approximation or resource threshold.
It also applies to an optimized exact adjoint recipe once that recipe
has been expanded into its real letters. In particular real G;InvG
and CX;CX identity padding does not defeat it. A common global minus
sign also disappears in characteristic2 and cannot remove the result.

## 4. A controlled odd Golden power violates the invariant

The two computational control sectors of(CG) have reduced row sums

    c=0: 1,
    c=1: 1+t.                                      (CB9)

Both sectors occur. Tensoring with actual identity spectators repeats
those distinct rows; it does not equate them. Equations(CB8)–(CB9)
contradict equality of CG with ANY finite literal word on that full
carrier. The target is a real orthogonal matrix; the obstruction is
exact arithmetic, not a determinant or norm failure.

The same proof excludes clean coherent control of G^(2r+1), r any
integer, in place of G. Negative powers have the same reduction as
the corresponding positive powers because Gbar²1=1. It does not
exclude controlled EVEN powers: their two reduced row sums agree.
The existing exact W_1(L) controlled G^(2L) is consistent with this
boundary. This corollary does not classify every word with a chosen
scalar probability; it only concerns these specified full matrices.

The earlier irrational-angle observation excluded u_L=p² within the
one-parameter power family u_L=sin²(2L theta). The present result is
stronger but differently typed: it rules out a finite clean compiler
for the WHOLE coherent gate(CG), even if the circuit uses other
allowed wires and macros rather than one controlled-power recipe.
It does not turn that statement into a universal probability no-go.

## 5. Exactly returned computational auxiliaries do not help

Suppose(CB3) holds, and let P be its computational coordinate input
subspace. Since W is orthogonal and CG maps P unitarily onto P,
W(P)=P and W(P_perp)=P_perp. Thus P is a REDUCING block of the full
word. In a coordinate basis adapted to the computational auxiliary
pattern,

    W=CG direct_sum W_perp.                         (CB10)

The off-block entries are exactly zero in R. Consequently a row in
the CG block has exactly its CG row sum even when summed over ALL
full-carrier columns: the other columns contribute zero. Applying
the ring reduction to(CB10), (CB8) would force all those rows to
have one common sum. But(CB9) gives1 and1+t. This is impossible.

Hence NO finite number of computational auxiliary bits returned
exactly as in(CB3) can realize clean coherent CG in this profile.
An ordinary finite native preparation from blanks followed by its
actual exact unpreparation is also covered whenever the resulting
whole word satisfies(CB3). It is the completed literal word, not an
unpriced prepared ancilla, to which(CB8) applies.

If auxiliary garbage is not returned, if success is selected, or if
the claimed map is only an initialized column with a different
unobserved output sector, the reducing-block argument has not been
established. One must examine that actual interface instead of
applying(CB10) by name. Conversely equality of normalized output
probabilities alone is not the exact all-vector identity(CB3).

## 6. The actual heralded construction escapes for a stated reason

The separate [HERALDED_CONTROL.md](HERALDED_CONTROL.md) constructs
the original-palette heralded interface using actual Boolean/H/X
factories and their flags, not a clean free CG primitive. At its stated
logical resource stage its successful Kraus block is

    K_success=alpha CG,    alpha=2p^4,
    alpha²=4p^8.                                    (CB11)

The complete native Boolean/resource success factors and every other
raw outcome remain as in that owner. In particular the successful
block is NOT the complete raw unitary and cannot replace R in the
unconditioned conjugacy formula of §7ak.

Since p=a² lies in R, alpha lies in R and reduces to ZERO modulo2:

    alphabar=0,    Kbar_success=0.                  (CB12)

The success block therefore has neither the clean unit amplitude
nor the reducing-block hypothesis of §5. Failure columns and other
input columns of the complete unitary can carry its required uniform
row sums. There is no contradiction with(CB8). Normalizing a selected
Kraus block divides out alpha and changes the interface; it is not a
legal equality of the full raw word with(CG).

This explanation is specific to the supplied successful amplitude.
No claim is made that all possible heralded schemes have that factor
or that this invariant classifies arbitrary success amplitudes. The
owner retains all actual failure effects, input/reference protection,
registration, clock, cap/abort and native controller price. Its true
raw C/F and joint fine record require their own source transport.

## 7. The exact parent consequence and preserved positive alternatives

For the SPECIFIED conditional0/10 ledger in §7ak, the scalar Gibbs
comparison has stationary point u_*=p². One attempted coherent
implementation would replace the completion's controlled G^(2L) by
the exact CG on fresh junk, leaving the c=0 input block untouched.
If it also returns every computational work bit exactly, that attempt
is ruled out by §5. This replaces an unbounded exact-circuit search
with a precise finite-word theorem. It does not deny the positive
matrix-comparison stationary point or invent a physical ledger.

There are positive interfaces OUTSIDE that clean target:

- The original primitive G on a fresh known bit ALREADY prepares
  probabilities(p,p²) exactly. The actual all-branches construction
  of [ALL_BRANCHES.md](ALL_BRANCHES.md) uses it and the owned typed
  0/10 writer without a free conditional G. It retains the c=0 trial,
  its records/costs and the changed raw corner, phase spectrum, true
  clock/carrier and gain. Exact code-component cancellation is not
  unproved full Book/controller stationarity.
- The heralded successful operation(CB11) is an actual alternative
  with its stated raw failures and source/price obligations. It is
  not converted to a deterministic clean word by discarding them.
- A measured or adaptive classical controller can have a different
  allowed input/action class. If c has been registered and a real
  controller conditionally enables a subsequent G, its retained
  branch/cursor/clock/decoder dynamics must actually be supplied.
  This theorem does not rule out that different instrument and does
  not grant its actuation for free.
- A new noncomputational reference, moving source frame, extra native
  primitive, non-clean output, or approximate gate is outside the
  literal statement unless its complete realization reduces back to
  the word/clean interface proved above.

The owned [Golden/CX Lie closure](../../A4D_LITERAL_GOLDEN_CNOT_ACTIVE_LIE_COMPLETENESS_AND_C2_SOURCE_2026_10_19.md)
is compatible with this result: density in SO concerns approximation
and closure, not exact membership of every target in a finitely
generated subgroup. It supplies no contradiction to a finite-ring
exact-word obstruction. No fresh rank/circuit census is needed here.

The parent is one implementation option for one conditional Gibbs
row. Clean CG is NOT declared a universal GR prerequisite. The direct
Book route, original all42 source family, changed all-branches source
map and other genuinely paid source-equivalent realizations retain
their stated scope. Full physical controller/task availability,
selected scalar Cost/Info, complete source normalization, joint
stationary refinement and GR_closed remain unpromoted. This note
adds no action, selector, claim, registry entry or physical postulate.
