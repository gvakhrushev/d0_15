# Native history, response descent and source-preserving archive elimination

Research owner: existing PR #310, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Input research head: `ad2e43f4eae418d6fe7386d37c7ee4c76400ed42`.
Input main: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Date: 2026-10-08. Status: exact generic theorem package with an actual native
golden-operator specialization; research admission, not a new CORE claim.

## 1. Consumed premise and existing owners

**Open input:** `native_sector` / `constitutive` (G0). A state used in subsequent
native dynamics must retain the correlations which affect later experiments.
The next consumer, G0b, needs actual compatible processes and observations;
G1 needs elimination which preserves the full action variation and sources.

**Owned inputs:** Book 01 §01.4 and §01.6 give finite registration and golden
preparation; Book 03 §03.1.3 retains ordered path memory, §03.26 supplies
joint reversible golden apparatus, and §03.2 owns the feedback determinant
action. `GoldenCoherentMemory.fullStep` is an actual four-dimensional operator,
with an orthogonality theorem and a complete joint-correlation balance.
The generic lemmas below take explicitly typed states, operations, readouts
and blocks as inputs. They do not promote their input family to a uniquely
forced physical universe. In particular, the two recorded preparations are
normalized carrier states; the first is constructed by the owned gate from
the blank basis vector. Admission of both preparations to a particular closed
native protocol remains an obligation of that protocol.

**Discharged premise:** the exact meaning, universal property and finite-depth
construction of history-preserving descent; complete linear archive return;
all-root, all-source Schur elimination and its determinant variation.
The actual native operator gives a strict witness that even BOTH separate
current marginals are insufficient. The single next consumer is the joint
native refinement construction specified in
`D0_NATIVE_CORE_EXECUTION_PLAN_2026-10-08.md`.

The proof capsule is `certificates/a4d_native_history_response_descent.lean`.
The checker, compiler receipt, transcript and exact ledger have the same stem.
All named propositions are printed, with their transitive logical axioms.

## 2. What a complete operational state retains

Let S be the admitted joint state space, L the admitted internal operation
labels, T_l:S→S their actual maps, and r:S→O the admitted readout. Several
readouts can be represented by their joint value. For a finite word w in L,
let T_w be the corresponding ordered composition (empty word is identity).
The labels specify internal protocols; no external duration is assigned.

Define

    x ≈ y  iff  r(T_w x)=r(T_w y) for every finite admitted word w.

This is an equivalence relation. It preserves the present readout and is
stable under every T_l, because a future after l is the word l::w. Therefore
both r and all T_l descend to Q=S/≈, and every finite experiment on Q gives
exactly the original result. If another exact factor q:S→C has

    q(T_l x)=T'_l(q x),       r(x)=r'(q x),

then q(x)=q(y) implies x≈y, by induction on the word. Thus Q is the coarsest
exact process quotient for these operations and observations. Keeping the
present output alone is legitimate only when it meets this full condition.
This is an operational equivalence, not an assertion of physical gauge.
Omitted probes cannot be recovered by renaming the resulting quotient.

The Lean statements prove this for arbitrary state, operation and output
types. Universal quantification over words is part of the proposition, not
an extrapolation from a finite test collection.

## 3. A canonical observation tower, constructed from the process

Define the depth-d response recursively:

    R_0(x)=r(x),
    R_(d+1)(x)=(r(x), (R_d(T_l x))_(l∈L)).

Its state space is the **realized image** C_d=range(R_d), not the whole set
of formally possible response tables. Truncation π_d:C_(d+1)→C_d deletes
the last observation layer. The identity π_d R_(d+1)=R_d is an induction,
and π_d is surjective: the same realizing x gives a lift.

Every operation has the canonical depth-shifting map

    A_(l,d):C_(d+1)→C_d,       A_(l,d)R_(d+1)(x)=R_d(T_l x).

Truncation and processing commute:

    π_d A_(l,d+1)=A_(l,d) π_(d+1).

Both sides select the same child table and delete its last layer. These
are actual maps and equalities, including on the realized subtypes.
All-depth equality R_d(x)=R_d(y) for every d is equivalent to x≈y. If L and
O are finite, each C_d is finite, by the recursive product/function-space
construction. Its coarse upper bound is

    |C_d| ≤ |O|^(1+|L|+...+|L|^d).

This bound is not a claim that every table occurs or that this many memory
bits have accumulated. In particular, real probability-valued observations
do not satisfy the finite-O hypothesis merely because a detector has two
outcomes. The native witness below uses a real expectation and does not
silently discretize it.

An autonomous endomorphism on one fixed C_d is stronger than this canonical
depth-shifting construction. If R_d T_l=N_l R_d for some actual N_l, then
equality at that depth already implies equality of every future response.
This necessary condition is Lean-formalized. It identifies exactly what a
finite sufficient-memory argument must prove.

The tower distinguishes operational depth from physical time or spatial
mesh. It also distinguishes compatible limiting tables from actual states:
surjective finite truncations alone do not imply that every infinite table
has a realization in S. For example, take S=ℕ, T(k)=max(k−1,0), r(k)=[k=0].
At any finite depth d, some k>d has an all-zero table; the compatible
all-zero infinite table has no realization in S. Native compactness or
another proved completeness condition is needed before invoking that step.
This is a control against empty infinite fibers, not a rejection of the
native profinite construction. No condensed sheaf or native preparation
theorem is replaced by a table definition.

### 3.1. Consume the native profinite owner for the complete response

There is a positive resolution of the infinite-fiber issue on compact
native support. Assume a finite admitted operation family, continuous T_l,
and a locally constant readout r. A finite family of locally constant
functions is jointly locally constant: at each point intersect their
finitely many constant neighborhoods. Composition with continuous T_l
preserves local constancy. Induction therefore makes the **entire** R_d
locally constant, not only its present component.

On compact support its realized range is finite, even when the nominal
output type O is infinite. Thus the finite-O assumption of Section 3 has
a different sufficient replacement here; neither condition is claimed
necessary in every special process. On a profinite S, the actual owner
`CondensedAnchor.readout_factors_through_finite_level` now factors this
complete R_d through a finite quotient of S. The capsule applies that
owner directly, with continuous operations and local constancy visible
in the printed proposition.

Moreover, every compatible family c_d∈C_d is realized by one x∈S:
the nonempty fibers {x:R_d(x)=c_d} are closed, and truncation makes them
nested. Compactness gives a common point. This all-depth realization
theorem is compiled, including the actual fiber construction. The chosen
x is unique only modulo the full-future equivalence, as it should be.
The countdown countercontrol is noncompact, so it does not satisfy this
theorem's hypotheses. No imaginary limiting state is silently admitted.

This consumes the profinite part of the existing condensed framework.
It does not prove its remaining physical subfunctor or sheaf conditions.
Points of a profinite support and Hilbert amplitudes on that support are
different types. A coherent matrix operator on amplitudes is not thereby
a continuous point map of the support; the theorem is applied only where
its actual T_l and r have the stated types and properties.

### 3.2. Golden weights give a coherent inclusion and a record preparation

For any finite collection of golden parent cylinders, the existing
`cylWeight_refine` identity gives, for **every** coarse reading f,

    Σ_w [μ(wA)f(w)+μ(wB)f(w)] = Σ_w μ(w)f(w).

The local and finite-partition identities are compiled. This preserves
expectations of readings pulled back along the actual prefix projection;
it does not impose independence on future outputs of a coupled apparatus.

There is also a direct Hilbert-space construction. In the normalized
cylinder basis e_w=1_[w]/sqrt(μ(w)), pulling back the same function to
the next partition is exactly

    J e_w=a e_(wA)+p e_(wB),       a=sqrt(p), p=φ^(-1).

The coefficients squared are the **owned** cylinder branch weights.
For arbitrary real amplitude vectors x,y, J preserves their pairing,
because a²+p²=p+p²=1. Every already given linear operator A on the
coarse amplitude space has the tensor extension A⊗I, with

    (A⊗I)J=JA.

Both the all-vector pairing identity and arbitrary-linear-operator
naturality are compiled; no chosen differential or field action enters.
Thus the new tensor factor in this existing cylindrical inclusion is
the normalized vector v=(a,p). The inverse of the already owned golden
gate G=[[a,−p],[p,a]] gives

    Gᵀ v=(1,0).

This is a reversible construction of a blank factor from the refined
golden factor, and the equality is compiled against the actual gate.
It is not a reset of an occupied record: invertibility preserves whatever
joint state is already present. A physical protocol must still admit the
refinement and this inverse-gate operation. The construction does not make
their repeated execution an equation of motion or an infinite resource
law. It supplies explicit maps where the former interface supplied only
trace-preservation hypotheses.

## 4. Strict return of correlations in the actual golden apparatus

Write p=φ^(-1), a²=p, p+p²=1, p>0. In the owned system/record basis
00,01,10,11 the operator is exactly

    W = [ a  0 -p  0
          0  a  0 -p
          0  p  0  a
          p  0  a  0 ].

Set ψ₊=(a,0,0,p), ψ₋=(a,0,0,−p). Both have norm one. The present system
and archive reduced density matrices coincide separately:

    ρ_system(ψ₊)=ρ_system(ψ₋)=diag(p,p²),
    ρ_record(ψ₊)=ρ_record(ψ₋)=diag(p,p²).

Their joint correlations differ. ψ₊ is exactly W(1,0,0,0). Reusing the
SAME full W on the SAME record, with no fresh blank substitution, yields
for the system Z readout z(v)=v₀²+v₁²−v₂²−v₃²:

    z(W²ψ₊)−z(W²ψ₋)
      =8 a² p²(p²−a²)
      =−8 p⁶ ≠ 0.

Consequently these equal present marginals cannot identify operational
states of this joint apparatus. The depth-two response tables differ;
Lean proves that as a specialization of the generic tower. For the Z
readout alone even one reuse gives zero gap, so testing only the first
return misses this distinction. The probability of system output zero
differs after two reuses by −4p⁶. No new memory register is supplied
between the two reuses. This finite result establishes actual back-action
of stored correlations on later observations; it does not assume a
cosmological interpretation of that record.

## 5. Complete archive return without a hidden reset

For any real linear blocks let one joint transition be

    x_(n+1)=A x_n+B y_n,       y_(n+1)=C x_n+D y_n.

Here n indexes this transition chain; it is not an independent clock.
Induction gives the exact identities

    y_n=D^n y_0+Σ_(j<n) D^(n−1−j) C x_j,
    x_(n+1)=A x_n+B D^n y_0+Σ_(j<n) B D^(n−1−j) C x_j.

The Lean capsule represents the finite sum by its defining recursion and
proves both identities for every trajectory satisfying the joint equations.
No asymptotic approximation or convergence of an infinite resolvent is
used. Removing the initial archive term changes the allowed initial data.
Removing a return coefficient changes a later response whenever it acts
nontrivially. An update on x alone valid for **all** joint states exists
if and only if B=0. Restricted invariant state classes need their own
factorization proof and are not excluded by this all-state assertion.

This block projection is not a quantum partial trace. Section 4 separately
tests the actual reduced marginals, including their correlations, so the
two meanings of retained state are never interchanged.

## 6. Elimination preserves all coupled equations and independent sources

For a given linear system

    A x+B y=f,       C x+D y=g,

assume V is an actual two-sided inverse of D. Then the ENTIRE system is
equivalent to

    y=V(g−C x),       (A−BVC)x=f−BVg.

The proof is substitution in both directions. It does not assume positive
definiteness, symmetry, a nonsingular retained Schur complement or an
on-shell choice of f,g. The right-hand sources are declared inputs, never
fitted from a chosen output. Thus all roots correspond with the same
sources, and retained kernels/cokernels remain present. Left invertibility
already guarantees uniqueness of a correct archive reconstruction.

Nested elimination is coherent on its actual invertibility domain. For a
three-block K, first invert K₃₃ and then the resulting middle Schur block.
These assumptions make the full middle-plus-last block invertible by the
block inverse formula. For every retained x and every pair of archive
sources, both elimination orders solve that same archive subsystem; by
uniqueness they reconstruct identical archive vectors. Substitution into
the retained row makes the effective operator and source identical. The
determinants multiply by det(K₃₃) times the middle Schur determinant.
The general uniqueness and two-block equivalence are Lean-formalized;
this three-block assembly proof is analytic, with noncommuting exact
matrix and source/variation controls in the certificate.

## 7. Preserve the existing feedback action and its archive variation

Use the actual feedback pencil K=I−zF, where the owned finite feedback is
F=P U† Q U P on its retained carrier. The block determinant identity is

    det K=det D · det(A−BD^(-1)C).

On the domain of positive determinants, the existing action becomes

    −log det K=−log det D−log det(A−BD^(-1)C).

If both factors vary differentiably along an admitted variation, its source
contains both terms:

    δS=−δ(det D)/det D−δ(det Schur)/det Schur.

The capsule proves the determinant factorization for arbitrary finite real
matrix blocks and the genuine `HasDerivAt` identity for the two determinant
factors. `Real.log` also permits the log-absolute-value extension for
nonzero real factors; no physical branch is inferred from that extension.
The source identity is conditional on the actual variation of K. It does
not supply a metric variation, a matter action or a Ward identity.

In particular, the one-return feedback F and the full history operator U
are different objects. For the explicit W of Section 4, the first-two-
coordinate block projection gives F=p² I₂, whereas

    det(I−zW)=(1−z²)(1−2az+z²),
    det(I−zF)=(1−zp²)².

These exact polynomials differ. Substituting the first determinant into
the action would add a new action. Instead, the result says how to retain
the archive determinant and its variation when eliminating variables of
the action which is actually owned. Singular archive pivots require a
range/kernel treatment and are not covered by writing an inverse symbol.

## 8. Acceptance boundary and next proof

The executable controls include noncommuting nested elimination, every
source basis direction, all matrix-entry directional derivatives, lost
initial memory, lost delayed return, wrong signs, one-step-only comparison,
discarded correlations, singular pivots, omitted archive source and
U/feedback-action substitution. The ledger pins the proof, full compiler
transcript, toolchain and transitive D0 inputs. Scope mutations must fail.

The additional exact controls check golden mass and **every parent-reading
coefficient** through six finite levels, symbolic pairing for arbitrary
vectors, arbitrary-operator naturality and the reversible blank preparation.
The universal topological statements are compiler-checked, not inferred
from these finite fixtures.

The finite observation tower is now constructed rather than a Boolean
compatibility interface. Its profinite factorization and compact history
realization, golden expectation descent and cylindrical Hilbert inclusion
are now proved. The remaining G0b arrow is **one joint native process**:
bind the admitted coupled history/record operators and preparations to these
inclusions, and prove the required action/variation compatibility. The point
process and the amplitude process cannot be identified by a type change.
A valid next result must give that joint binding or a precise proof of its
missing owner; it must not substitute another arbitrary field model.
Subsequent action/source/contrast, curved existence, soundness and recovery
obligations retain their existing order. This package changes no claim,
supported D0 owner, book, task lifecycle or terminal of #310/#202/#317.
