# Retained golden program compilation and the actual scene-history target

Research parent: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, [#310](https://github.com/gvakhrushev/d0_15/pull/310).
Input head: `66d51fbad02e683561c938b71ba728eb9b25bf03`.
Base: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Date: 2026-10-09.

The [fixed complete preparation](A4D_NATIVE_GOLDEN_FIXED_CALIBRATION.md)
retains a derived phase for each vertex. A real pointer can distinguish
these phases. This packet derives a finite correction from the same
literal word, proves its full-state error, factors its fixed target into
the actual incoming-history ray and one common complete record, and
proves how approximate compiled operations transfer that result.

The compilation class is explicit: arbitrarily addressed copies of the
owned real golden matrix G and the recording CNOT, with specified basis
preparations and all additional records retained. Algebraic ownership of
these matrices does not establish physical addressability or preparation
admission. The packet supplies a compiler route within that class and a
cost/accuracy schedule. The native decoder, hardware admission and joint
heat/tangent/refinement/action law remain the next G0b obligation.

## 1. The native palette meets the external theorem's hypotheses

Put p=p0=primitiveRoot=phi^{-1}, a=sqrt(p), and

    G=[[a,-p],[p,a]],  a^2=p, p+p^2=1.

The kernel proves p>1/2 and p<1, the exact square

    G^2=[[a^2-p^2,-2*a*p],[2*a*p,a^2-p^2]],

and that all four entries are nonzero. Consequently G^2 changes the
computational basis. The literal p0 corollary is printed. The recording
matrix is the earlier owned CNOT, extracted algebraically from the actual
GoldenCoherentMemory fullStep in the pinned preparation packet.

[Shi's Theorems 1.2 and 3.1, together with Definition 2.1](https://arxiv.org/abs/quant-ph/0205115v2)
therefore give approximation of real orthogonal operations by addressed
G/CNOT circuits, with prepared ancillary records and a uniform error for
every logical input. The paper's efficiency statement is the external
analytic compiler input, rather than a new Lean declaration. Its real
norm approximation is used; no arbitrary complex phase quotient is
applied to a real pointer. This density theorem is not kernel-formalized
in this packet.

The inverse requirement is explicit. A supplied retained basis-one control
gives X on the target through CNOT. The exact forward echo X G X=G^T is
proved on every target vector while preserving that control. Thus an
inverse-closed compiler palette can be realized using forward G/CNOT on
the declared prepared subspace. This does not derive the physical supply
of that basis-one record or access to both ordered CNOT placements.
Every ancillary basis preparation and its G preparation circuit must be
included in the whole program and its budget.

## 2. A finite correction gives a fixed incoming-history target

Use the earlier complete seed U, validity chi, blank z, full word U_k and
unspun complete column xi_k. Its own normalized success coefficient is

    b_k=sqrt(s0)*conjugate(w)^(2*k)*alpha_k,
    |b_k|^2+e_k=1,  w=G^8 in the faithful real representation.

After two stages e_k<1, so b_k is nonzero. Define the finite quantities

    c_k=b_k/|b_k|,  C_k=conjugate(c_k).

No infinite limit, measured source, independent angle or fitted phase is
an input. Kernel proofs establish |C_k|=1, C_k*b_k=|b_k| and uniqueness of
this correction. Apply C_k to the entire state, including failed records.
With t equal to the normalized accepted **initial** seed, the exact full
distance is

    ||C_k*xi_k-t||^2=(|b_k|-1)^2+e_k <= 2*e_k.

For the literal golden recursion,

    ||C_(k+2)*xi_(k+2)-t||^2 <= 16^(-k)/5.

The corrected output remains a complete unit vector. The correction is
one real pointer rotation on every retained coordinate, not a reset or
postselection. Its full matrix is orthogonal. All 33 actual vertices and
the whole 2^45 seed are bound in the generic kernel statements. The
equation describes the exact target operation; Section 3 includes its
compilation error and additional records.

For five four-pair streams, let j(w) be the product raw amplitude on the
records whose first unequal pair has been coherently routed to false.
Let M be their total squared mass. The kernel proves

    M=((1-q^4)/2)^5=jointGoodWeight/32>0,
    eta(w)=j(w)/sqrt(M),  sum_w eta(w)^2=1.

At every actual vertex v,

    t_v(w,b)=uniform_(S_v)(b)*eta(w),

with uniform_(S_v)=1/sqrt(d_v) on its accepted incoming codes and zero
elsewhere, d_v in {20,22,24}. This identity covers every raw coordinate,
not only the successful fiber. The same eta is used for all vertices.

For any history frame J and whole history operation R, attach that record
without tracing it out: J_eta(h,w;v)=J(h;v)*eta(w). The kernel proves

    J_eta^T J_eta=J^T J,
    (R tensor I)J_eta=(RJ)_eta,
    J_eta^T(R tensor I)J_eta=J^T R J.

These equations apply to the [owned 718-history reversal and scene
readouts](A4D_NATIVE_COMPOSED_FEEDBACK_DYNAMICS.md#69-owned-scene-history-realization-and-its-full-return-action).
In orthonormal vertex coordinates, its compression is
D^(-1/2) A D^(-1/2); in the owned degree-weighted coordinates it is
D^(-1) A=fullTransport. Their coordinate change must be retained. The
additional common record preserves either correctly paired return law.
This does not prescribe a heat operator on the complementary histories.

## 3. Compilation bounds include all ancillary leakage

For complete orthogonal words of length N, uniformly replacing each step
with error at most delta gives complete-state error at most N*delta.
The kernel proves the bound for every input and every carrier size.

The external compiler may use more records. Let J map the whole logical
state to the physical state tensored with the **prepared complete**
ancillary vector. Its norm must be one. For exact logical step U and
whole physical orthogonal step V, the required condition is

    ||V J-J U||_op <= delta.

It is stronger than agreement on the blank input. The step estimate is

    ||V y-J U x|| <= ||y-J x||+delta*||x||.

For all N steps this yields

    ||V_word Jx-J U_word x|| <= N*delta*||x||.

It applies to the actual leaking physical state after each preceding
step. No ancillary reset, trace, fresh-copy replacement or postselection
is made. Separate private prepared records can be attached to form one
common J; their preparation programs, addresses and storage remain part
of the full declared program. The complete compiled output has norm one.

At k=2m after the two-stage start, let epsilon_m=16^(-m). The exact
preparation norm error is <=epsilon_m/2. Allocate total compiler error
<=epsilon_m/2, for example delta=epsilon_m/(2N) on each of N nonempty
steps, including the finite pointer correction. The compiled complete
state then differs from the fixed retained target Jt by <=epsilon_m.
The actual native blank/seed/word/real-encoding bindings are kernel
proved, including the ancillary version. Every real orthogonal-projector
reading has squared error <=4*epsilon_m^2. All circuit choices meeting
these bounds have the same limit. This establishes a common limiting
readout, not exact finite-level catalogue independence by M1.

Whole golden pair-history cylinder extensions preserve the squared error
at every depth. The prefix program acts on the whole old cylinder; the
earlier fine-singleton phase remains an invalid replacement.

## 4. A literal cost schedule fits the owned golden scale

The earlier complete recursive word has exact expanded syntax cost

    Cost_(k+1)=3*Cost_k+2*PhaseCost,
    Cost_k+PhaseCost=3^k*(SeedCost+PhaseCost).

At k=2m+2 its expanded cost plus PhaseCost is exactly
9*(SeedCost+PhaseCost)*9^m. Fixed-dimension real-gate compilation at
delta=epsilon_m/(2N) has log(1/delta)=O(m); the external polylog compiler
bound therefore multiplies this literal cost by a fixed polynomial in m.
Finite ancillary preparation and address encoding must be included in
that polynomial. This is a sufficient upper bound for this explicitly
addressed compiler class, not an installed native decoder.

The kernel binds the scale to the actual owner:

    phi=1+p0,  phi^5=8+5*p0,  9<phi^5<16.

For every fixed A and polynomial degree c,

    A*m^c*9^m/phi^(5m) -> 0,
    A*m^c*9^m <= phi^(5m) eventually,
    epsilon_m <= phi^(-5m).

Thus the declared program has a cost/accuracy schedule at levels 5m.
To conclude actual BOOK_03 admission, its literal finite code must be
bound to the own decoder and its permitted preparation, addressing,
records, inverse use and readout resources. Code length and executed path
length are different quantities; BOOK_03's finite alphabet statement alone
does not supply a runtime bound. The schedule here bounds the expanded
word itself. No program index or record depth is identified with physical
time, metric mesh or expansion, and no autonomous full-word clock is
claimed.

## 5. Proof boundary and next critical input

The standalone capsule prints 80 new actual propositions and all their
transitive axiom dependencies. Prior preparation and fixed-limit bodies
are pinned inputs and are not counted again. Only the standard kernel
axioms are allowed. The exact checker independently verifies the native
palette, finite correction, raw-record factors, full-word and ancillary
error controls, actual scene return coordinates and golden cost constants.
The external density/compiler theorem is marked separately from kernel
results and physical admission.

All 267 exact controls pass. The actual checker rejects all 27 false-scope
and 13 false-exact ledgers, including unproved M1/decoder/clock/GR
promotions, erased ancillary leakage, a blank-only compiler test, wrong
scene coordinates, omitted common-record return and false golden-scale
or input-hash ledgers. The nine repository/protocol, coverage, no-sorry,
debt and generated-view guards pass. The supported D0 owner tree is
unchanged; current-head CI and CONTROL acceptance retain their own gates.

The next G0b input is the physical admission of this same complete
prefix-natural program and readout under the actual native decoder and
budget, followed by the independently owned joint heat/tangent/refinement
law. In particular, the 19/13 complementary heat parameters from the
complete declared extension class are not selected by circuit density or
by a common-record identity. Derive their admissible variations and
source relevance from that same native state, then use the already owned
genuine bootstrap/source calculus.

Own metric/matter source and physical Ward, quantitative metric contrast,
native stationarity, curved joint roots, soundness/recovery and physical
constraints remain required. G0b/G0, positive GR, global closure and the
original #310 fixed-source/raw-owner terminal remain open. #202/#317
retain their independent criteria. No action, angle, temperature rule,
selector, coupling/source prescription or physical postulate is added.
