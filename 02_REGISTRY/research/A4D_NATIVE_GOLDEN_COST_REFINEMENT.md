# Golden cylinder cost and the full Fibonacci matrix refinement

Research parent: existing #310. Input SOURCE
`123d9e969ec56705b4b485adb59a36c19f5a8797`.
Status: a constructive connection between the existing golden detector
measure, Fibonacci refinement and a literal trace-preserving matrix
inclusion. The common physical preparation T0 is still open.

The detector owner assigns cost 1 and 2 to its two letters and weight
`p^cost`, where `p=phi^-1`. Reading that same support at a fixed accumulated
cost gives the Fibonacci refinement already named in the corpus. Its
matrix inclusion has an explicit conditional expectation. In normalized
GNS coordinates its duplicated block is the existing golden column
`(sqrt(p),p)`. Both rectangular matrix blocks are retained in the
orthogonal complement. Thus this connection needs neither an arbitrary
matrix embedding nor an independently chosen trace state.

This supplies an actual preparation/refinement input to T0. It supplies
no heat generator, physical clock identification or map to `(q,D,b,m)`.
In particular the factorization of an isometry is not a proof of physical
permission to execute its unitary extension. These remain separate from
the constructive statements below.

## Existing inputs

`CondensedAnchor.DetectorSupportGoldenWeight` defines `cylWeight` and
`weightExp`, proves cylinder refinement and `cylWeight w=p^(weightExp w)`.
The direct letter has cost 1 and the return letter cost 2.
`Geometry.FibonacciBratteliRefinement` defines the forbid-11 language and
its incidence `M=[[1,1],[1,0]]`. `Algebra.FibonacciAFTower` defines
`pathCount(0)=(1,1)` and `pathCount(N+1)=(a+b,a)`. Its generic GNS theorem
takes a multiplicative, star-preserving, trace-preserving inclusion as
input. The inclusion and its trace equality are constructed here.

`Representation.GoldenCoherentMemory.blank_record_evolution` binds the
normalized column to the actual retained recording gate. Equality of
that prepared column does not identify a two-coordinate unitary with
the complete four-coordinate recording operation.

## The cost cut is a complete prefix partition

Encode a direct letter by `0` and a return letter by `10`. For every
finite raw word w, the encoded length is exactly `weightExp w`. Infinite
concatenation gives a bijection onto binary sequences with no adjacent
ones: parse a 0 as a direct letter and a 1 together with its compulsory
following 0 as a return letter. Parsing and concatenation are inverse.

For n>=1 take the shortest raw prefix whose cost reaches or exceeds n.
Its cost is either n or n+1. This is a finite complete prefix partition:
cost increases by 1 or 2, so each infinite history reaches the cut once;
minimal prefixes cannot contain one another. The n=0 partition contains
the empty word. No histories are accepted or rejected by this construction.

The first n encoded symbols determine the cut word, including a pending
return if the last symbol is 1. Conversely, the cut word determines those
n symbols. The pending zero is compulsory and introduces no independent
hidden flag. Let a_n count prefixes ending in state 0, and b_n those
ending in state 1, with the empty prefix in state 0. Then

```
(a_0,b_0)=(1,0),       (a_(n+1),b_(n+1))=(a_n+b_n,a_n).
```

Thus `(a_(N+1),b_(N+1))=pathCount(N)` exactly. At the next cut a leaf
of cost n splits into both existing branches; a leaf of cost n+1 is
carried unchanged. Splitting every leaf at every cost level would be a
different refinement.

The partition retains the same profinite support. A cost-n cut is determined
by the first n raw letters, and the cost-2m cut refines the first-m-letter
partition. These two cofinality bounds prove that no old finite record is
lost. They do not assert that accumulated cost is physical proper time.

## The existing measure gives the Perron weights

The cut-cylinder weights are `p^n` on its a_n states and `p^(n+1)` on
its b_n states. Consequently

\[
 a_n p^n+b_n p^{n+1}=1.                                      \tag{1}
\]

The recurrence proves (1) by induction, using only `p+p^2=1`.
It is not normalization imposed after discarding histories. Equivalently,
the encoded process starts in state 0 and has transitions

\[
 K=\begin{pmatrix}p&p^2\\1&0\end{pmatrix}.
                                                               \tag{2}
\]

With `v=(phi,1)`, each allowed transition obeys
`K_ij=M_ij v_j/(phi v_i)`. Multiplication along a path telescopes to
the weights in (1). This is the rooted Perron/Doob process; its initial
law is not silently replaced by a stationary Markov law.

The classical probability matrix of the cut has only the two eigenvalues
`p^n,p^(n+1)`, with multiplicities a_n,b_n. Its logarithmic spectral width
is `log(phi)`, independent of n; the variance of the surprisal is at most
`log(phi)^2/4`. This is a different finite readout from m independent
golden letters. The previous independent-factor state-separation theorem
remains valid in its class, but is not applied to these cost cuts.
No equality with a Hodge Gibbs state is concluded.

## The full matrix inclusion and its trace

At AF level N put `(a,b)=pathCount(N)` and use the actual matrix spaces

\[
 \mathcal A_N=M_a(\mathbb C)\oplus M_b(\mathbb C),\qquad
 \iota_N(A,B)=(\operatorname{diag}(A,B),A)
       \in M_{a+b}(\mathbb C)\oplus M_a(\mathbb C).             \tag{3}
\]

Block multiplication proves that (3) is an injective unital star-algebra
map. Define the trace by the cut weights already obtained:

\[
 \tau_N(A,B)=p^{N+1}\operatorname{Tr}A
                    +p^{N+2}\operatorname{Tr}B.               \tag{4}
\]

Equation (1) gives `tau_N(1)=1`. Positive weights make it faithful.
With `t=p^(N+1)`, the fine block weights are `pt,p^2t`, and

\[
 \tau_{N+1}(\iota_N(A,B))
 =pt(\operatorname{Tr}A+\operatorname{Tr}B)
          +p^2t\operatorname{Tr}A
 =\tau_N(A,B).                                               \tag{5}
\]

This proves the three hypotheses of the existing generic GNS isometry
for the concrete inclusion. The Hilbert space is the full matrix space
with inner product `tau_N(Y*X)`, of complex dimension `a^2+b^2`.
It is not the a+b dimensional cylinder/defining representation.
The positive tracial state (4) is not a nontracial tensor marginal and
is not a faithful density on the full matrix algebra of its GNS Hilbert
space. Those distinctions matter for any proposed modular or heat reading.

## All retained and complementary directions

Write a fine element as

\[
 (Z,W),\qquad Z=\begin{pmatrix}X&U\\V&Y\end{pmatrix}.
\]

The actual adjoint of the inclusion, for these GNS forms, is

\[
 C_N(Z,W)=(pX+p^2W,Y),\qquad C_N\iota_N=I.                   \tag{6}
\]

Indeed pairing against every `(A,B)` in (3) gives
`pt Tr(A*X+B*Y)+p^2t Tr(A*W)`, which is exactly the coarse pairing
with (6). This also proves uniqueness of the adjoint. The map is positive,
unital and bimodular for the embedded algebra: diagonal compression and
positive averaging prove positivity, and block multiplication proves
the other properties. Therefore `P_N=iota_N C_N` is the orthogonal
projection onto the actual old algebra.

The complete Pythagorean identity is

\[
 \|(Z,W)\|_{N+1}^2-\|C_N(Z,W)\|_N^2
 =t\{p^3\|X-W\|_F^2+p\|U\|_F^2+p\|V\|_F^2\}.             \tag{7}
\]

For each duplicated entry it is the scalar identity
`p|x|^2+p^2|w|^2-|px+p^2w|^2=p^3|x-w|^2`; sum all entries,
and add both rectangular blocks. This proves (7) for complex matrices
as well as real ones. The complement has dimension `a^2+2ab`, and

\[
 (a+b)^2+a^2=(a^2+b^2)+(a^2+2ab).                            \tag{8}
\]

In particular neither rectangular block is quotiented out of the
carrier or declared physical gauge. Its absence from the coarse
readout does not permit omitting it from a separately specified full
heat trace.

## The golden block occurs inside this inclusion

Normalize a coarse A-entry by `sqrt(t)`, its fine X-copy by `sqrt(pt)`
and its W-copy by `p sqrt(t)`. Equation (3) then sends each normalized
coarse coordinate x to

\[
 x\longmapsto(\sqrt p\,x,p x)
 =G\binom{x}{0},\qquad
 G=\begin{pmatrix}\sqrt p&-p\\p&\sqrt p\end{pmatrix}.         \tag{9}
\]

The B-block is carried identically. Both rectangular blocks remain as
new independent coordinates. The complete coordinate extension is G on
each of the a^2 duplicated pairs and identity on the B and rectangular
blocks. It is orthogonal/unitary. The retained projector on a duplicated
pair is

\[
 P=G\begin{pmatrix}1&0\\0&0\end{pmatrix}G^*
   =\begin{pmatrix}p&p\sqrt p\\p\sqrt p&p^2\end{pmatrix}.    \tag{10}
\]

Thus the coefficients in (9) are fixed by the existing measure and
inclusion, not chosen to match a desired source. The literal recorded
gate sends `(x,0,0,0)` to `(sqrt(p)x,0,0,px)`, which is the same
prepared column with its record coordinates retained.

Equations (9)--(10) are a representation of the inclusion. They do not
prove that a passive change of normalized coordinates is an executable
native time step. In particular the carried B-block prevents replacing
this refinement by a uniform fresh golden split on the whole old space.
Composition of (3) gives the actual two-step inclusion, of incidence M^2,
with the same compatible trace; no independently chosen lift is needed.

## Exact boundary for the next calculation

The previously generic trace-preserving-inclusion input now has actual
matrices, all-level cylinder provenance, full adjoint and retained
complement. This is the concrete premise supplied to the preparation
part of T0. It does not identify the Fibonacci AF tower with the 33/718
scene history or the four-role lattice, and does not bypass their existing
carrier/spectrum boundaries.

A physical common preparation must still derive its heat generator and
allowed dynamics on this same complete carrier, its readout to the
constrained `(q,D,b,m)`, and their variations. The scalar phi scale
identity is not a theorem selecting the power or shape of that generator.
Ordinary matrix trace in the bootstrap is not replaced by the normalized
AF trace (4). No temperature, source, action, selector, physical time or
stationarity condition is introduced here. T0--T3, all 44 dependency
nodes, original #310 fixed-source/raw-owner and independent #202/#317
terminals remain open.

The companion Lean capsule proves 24 propositions: the cost length and
owner count binding, the all-level mass identity, real matrix algebra and
trace identities, the actual all-size GNS isometry and conditional adjoint,
the complete entrywise residual, and the golden-column identities. All
declarations resolve; their transitive axiom union is exactly `propext`,
`Classical.choice`, `Quot.sound`. The prefix partition, cofinality and
extension of the GNS argument to complex matrices are analytic proofs
above; they are not advertised as separately compiled theorems.

The exact checker passes 6157 controls in 36 groups and rejects eight
executed mathematical mutants and sixteen false scope ledgers. It tests
complete prefix cuts through cost 12, all retained matrix directions at
four successive AF sizes, complex non-diagonal fixtures and the literal
recorded gate. The all-level assertions follow from the proofs, not an
extrapolation from those finite controls. The receipt pins the capsule,
its output, the actual transitive D0 inputs and the separately read
forbid-11 owner. No supported D0 source or core claim changes.
