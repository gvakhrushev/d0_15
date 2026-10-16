# Native verification, process admissibility and phase refinement

Research input: `606d8774bcaf4684d8caac60cb73912a8827091a`.
Parent: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft #310.
Status: scoped interface/process classification, pending CONTROL intake.
**Native physical realization, positive GR and global closure remain OPEN.**

This closes a concrete ambiguity in the first native-realization gate: what
the existing verification/M1 interfaces and actual phase refinement do, and
do not, impose on independently supplied states and variations. It introduces
no action, selector or physical postulate. A process run is not silently
identified with a metric variation, and a phase index is not a spacetime site.

## 1. Actual owners and the exact verification classification

`Foundation.VerifiabilityNecessity.VerificationContract` requires a
nontrivial state type, at least two line labels, a nonempty catalogue and

\[
 \operatorname{compare}(l,c,\operatorname{record}x,
                    \operatorname{record}y)=\operatorname{decide}(x\ne y)
                                                        \tag{1}
\]

for every line, catalogue and pair of states. Injective recording, line
agreement, catalogue independence and the equivalence of the resulting
empirical quotient with the verified state type are already owned theorems.
The owner's comments explicitly leave physical apparatus realization and
causal independence of the line labels as application obligations.

For the literal `OperationallyVerifiable T`, the new Lean theorem proves

\[
 \operatorname{OperationallyVerifiable}(T)
 \quad\Longleftrightarrow\quad
 \operatorname{Nontrivial}(\operatorname{EmpiricalState}(T)).       \tag{2}
\]

Forward: transport two distinct protocol states through the required
equivalence with the empirical quotient. Reverse: take that quotient as
both state and record, use identity recording, two Boolean line/catalogue
labels and equality comparison (1). Classical decidable equality supplies
a formal representation; (2) does **not** provide a physically implementable
or effective equality oracle for an arbitrary quotient.

Thus this formal interface, without an additional owned application map,
does not select a metric, a state preparation, an action or an Euler gate.
This observation does not discard the real class-level M1 construction:
`Synthesis.ConcretePhysicalDetectorRepresentation` already constructs the
representation on `(member,value,history)`, with independent two-sided
history catalogues. Its actual proposition proves equivalence of class M1
and full history invariance, embeddings and factorization through current
data on both arguments. Its two primitive outputs are **capability profiles**,
not all admissible comparison functions. There are `2^(4*4)=65536` Boolean
functions of two current-data arguments. The old stronger
`PhysicalComparisonRepresentation.Representation` has separate faithful
capability and subcomparison-realization fields; it is not automatically
instantiated by this class-level result. Both scopes are retained.

## 2. Complete run classification for literal point tests

`EmpiricalTheoryFactorization.OperationalProcess` has independently given
maps `run`, `pullTest` and the exact observation compatibility equation.
For `operationalEmpiricalTheory P`, tests are `(line,reference state)`.
Using (1), compatibility is exactly

\[
 fx=y\quad\Longleftrightarrow\quad
 x=(\operatorname{pullTest}(l,y)).\operatorname{reference}.         \tag{3}
\]

Every inverse image of a point is therefore a singleton. With one line and
catalogue supplied by the contract, (3) proves injectivity and surjectivity
of `run`. Conversely, every bijection has the operational lift
`pullTest(l,y)=(l,f^{-1}y)`. These implications, including infinite state
types, are compiled against the actual structures:

\[
 \text{a point-test operational lift of }f\text{ exists}
 \quad\Longleftrightarrow\quad f\text{ is bijective}.              \tag{4}
\]

An observable invariant under **all** these processes must be constant:
apply the transposition of any two states. The converse is immediate. This
does not assert that a physical action must be invariant under all verified
processes; it shows why such an assertion would itself be an extra condition.

The test-space hypothesis matters. In the empirical theory with every
predicate `e:State -> Bool` as a test, every map, including a constant run,
has a pullback `e -> e composed with f`. The capsule constructs this lift
and separately proves that a constant Boolean run has no point-test lift.
There is no general bijectivity theorem for arbitrary empirical test spaces.

An explicit action control uses the **existing** `archiveDirichletEnergy`
at phase stage `n=1`, with three vertices. The two preparations are the
zero field and the unit pulse at vertex zero. Their energies are 0 and 4.
The Boolean flip is a verified operational process, yet it exchanges these
energies. On the actual radial variation of the pulse,

\[
 E((1+t)\delta_0)=4(1+t)^2,\qquad
 E((1+\epsilon)\delta_0)-E((1-\epsilon)\delta_0)=16\epsilon.        \tag{5}
\]

These identities are compiled from the owner's directed adjacency sum.
The zero radial derivative and the pulse derivative 8 are not identified by
verification. The preparation is a countercontrol to a proposed inference,
not a claim that verification already selects a physical field variation.

## 3. Exact reversible processes on the full native phase tower

For `archivePhaseIndex n = Fin(n+2)`, write `L=n+2`. The actual
`archiveRGPhaseProjection` is

\[
 p_L:\{0,\ldots,L\}\longrightarrow\{0,\ldots,L-1\},\qquad
 p_L(i)=i\bmod L.                                                \tag{6}
\]

Suppose permutations satisfy `p_L sigma_(L+1)=sigma_L p_L` for **every**
`L>=2`. Then every permutation is the identity. Here is the all-size proof,
also compiled with the actual owner projection.

The zero fiber is `{0,L}`, and every other fiber is a singleton. Compatibility
of two bijections preserves fiber cardinalities, so `sigma_L(0)=0`. Because
each stage has a successor, every stage fixes zero. At `L=2` this fixes the
other point. Inductively, a nonzero coarse point has only one inverse image,
so every old nonzero point is fixed. The two zero-fiber points are zero and
the new point; zero is already fixed, hence the new point is fixed too.

A finite prefix is not a proof of the infinite statement. Every full
consecutive prefix beginning at `L=2` with at least one transition has two
coherent families: the identity, and the identity below the last stage with
zero and the last new point swapped at the last stage. Only the first
extends one more step. The exact enumeration retains this negative control.

This theorem classifies exact reversible **phase-point** processes. It is
not a theorem about all field processes, quotient dynamics, continuous
variations, four-Role carriers, approximate refinement or physical time.

## 4. Subsequence classification and the real sparse-level exception

The actual composite of (6) from `K` down to `L<K` is

\[
 p_{L,K}(i)=\begin{cases}i&i<L,\\0&i\ge L.\end{cases}             \tag{7}
\]

Indeed, an index below L never changes; an index `i>=L` first hits its own
projection `p_i` and becomes zero permanently. In particular (7) is not a
single modulo operation for a long jump.

Let `2<=L_0<L_1<...` be any unbounded subsequence, using these actual
composites. Define birth blocks

\[
 B_0=\{1,\ldots,L_0-1\},\qquad
 B_j=\{L_{j-1},\ldots,L_j-1\}\quad(j\ge1).
\]

The complete group of exact coherent permutation families is

\[
 \operatorname{Sym}(B_0)\times\prod_{j\ge1}\operatorname{Sym}(B_j). \tag{8}
\]

Proof: the unique nonsingleton fiber of every successive composite forces
zero fixed at every level. Every old nonzero point then has its unique old
image, so the coarse permutation persists unchanged. The new block must
permute within itself. Conversely, these independent block permutations,
fixing zero, plainly commute with (7). This proves necessity, sufficiency
and uniqueness of the block data; there is no finite-search extrapolation.

For a finite horizon `H>=1`, the last zero need not be fixed. The exact count
is `(L_0-1)! product_(1<=j<H)(L_j-L_(j-1))! (L_H-L_(H-1)+1)!`.
Prefixes extendable to an infinite sequence instead have count
`(L_0-1)! product_(1<=j<=H)(L_j-L_(j-1))!`. The checker independently enumerates
both quantities on complete small permutation spaces.

On the dense subsequence `L=4,8,12,...`, (8) is nontrivial, but each point's
integer displacement is at most 3. In the normalized phase coordinate its
displacement is at most `3/L`. More generally the upper bound is

\[
 \frac{\max\{L_0-2,\max_{1\le k\le j}(L_k-L_{k-1}-1)\}}{L_j}.  \tag{9}
\]

It tends to zero if relative increments `(L_j-L_(j-1))/L_j` tend to zero:
bound all sufficiently late increments by `epsilon L_k<=epsilon L_j`,
then divide the finitely many early increments by `L_j`.

However, `L_j=4*2^j` also lies in `4N`. Reverse every birth block. This is
exactly coherent, and at `i=L_j/2` its normalized displacement is
`1/2-1/L_j`. Thus neither the full consecutive theorem nor the dense
subsequence bound excludes macroscopic processes on all refining sequences
allowed merely by `L in 4N`.

## 5. Adjacent error O(h) need not control composed error

Let `sigma_L(i)=(i+floor(L/2)) mod L` and measure defects by the owned
normalized cyclic phase distance. These are bijections at every level.
Their adjacent compatibility defect has exact maximum `1/L`.

For even `L=2k`, on `0<=i<=k` the projected fine half-turn and the coarse
half-turn agree (both are zero at `i=k`). For `k+1<=i<=2k` their
cyclic difference is one, including the terminal wrapped point. For odd
`L=2k+1`, the difference is one on `0<=i<=k` and zero thereafter. The case
`L=2` has the terminal difference one as well. These explicit cases prove
the bound for every L, and the checker verifies both parities independently.

For every even L, the actual long composite at fine input zero gives

\[
 p_{L,2L}(\sigma_{2L}(0))=p_{L,2L}(L)=0,\qquad
 \sigma_L(p_{L,2L}(0))=L/2.                                     \tag{10}
\]

The normalized cyclic defect is exactly `1/2`. Hence a uniform per-step
`O(h)` estimate does not imply the total `O(h)` refinement error needed by
the native contrast-transfer plan. This example addresses a specific proof
gap; it does not preclude summable estimates, a different owned process,
an observable annihilating the defect or a different physical readout.

## 6. Carrier exceptions and the remaining physical obligation

The phase tower cannot be substituted for the four-Role product. Swapping
two Role coordinates gives a nonidentity permutation commuting with every
componentwise phase projection. In particular, the genuine local-conductance
isomorphism in `ArchiveLocalLaplacianVariation` is on `ArchiveRolePhasePoint`,
not on the one-dimensional phase carrier of `ArchiveVariation`; the native
inventory now records that distinction explicitly. Nor is that product the native flattened
`ArchivePoints = Fin((n+2)^4)` tower: already at `L=2 -> 3`, flattened modulo
has fiber sizes 6 once and 5 fifteen times. The Role product has sizes
16, 8, 4, 2, 1 with multiplicities 1, 4, 6, 4, 1. The checker reproduces both.

The closure dependency is therefore precise. If a proposed native
state/variation/refinement map invokes operational verifiability, it must
specify the test interface, actual physical application and admitted process
class. If it uses the exact full one-dimensional phase tower, its reversible
point action is rigid. If it uses subsequences, another carrier or approximate
commutation, those cases need their own estimates. None of these interfaces
by itself supplies the missing metric--connection--matter action, local
metric source, on-shell stationarity, soundness or recovery.

## 7. Reproduction and proof boundary

The companion Lean capsule prints fourteen new proof declarations and two
existing M1 owner propositions, including five actual types. It checks their
transitive axioms and 32 D0 source hashes; thirteen declarations use only
`propext`, `Classical.choice`, `Quot.sound`, and three are axiom-free. The generic classifications (2)--(4),
full phase rigidity and literal native energy identities are compiled.
The all-subsequence group, finite-horizon counts, bounds (9) and parity proof
of (10) are analytical proofs here, with independent exact finite controls.
They are not described as Lean-formalized continuum theorems.
The immutable checker passes 76 grouped controls. Two deliberately falsified
ledgers, changing the full-phase classification and the composed defect,
are rejected. Repository, lifecycle, formalization-debt, claim coverage,
no-sorry, generated-view and artifact-freshness guards pass. The unchanged
supported Lean source tree retains its previously successful exact-tree
`D0.All` build; the research capsule is compiled separately in this update.

```sh
cd 03_FORMALIZATION
lake env lean ../02_REGISTRY/research/certificates/a4d_native_verification_refinement.lean
cd ..
python3 02_REGISTRY/research/certificates/a4d_native_verification_refinement_check.py
```

Default certificate replay compares an immutable ledger. Deliberately changing
the full-phase terminal or replacing the composed error `1/2` by `0` must
fail. No supported owner or CORE claim is changed. Original #310 fixed-source
raw-owner, #202 curved-stationarity and #317 stratification terminals remain
independent and open under their own contracts.
