# Native vector action: actual variation, source range and background response

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input: `a4a0ee1ce0a48fe07da0da036e122262e8cc7d44`.
Control baseline: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Status: **complete finite owner classification for the stated class**, pending
CONTROL. Positive GR, whole-core completeness and the original #310 terminal
remain OPEN. There is no new native action, coefficient selection or postulate.

This closes the missing variational link between the real matrix kinetic
action and the existing double-commutator vector equation. It also proves
the full source solvability criterion, instead of assuming that any source
has a solution. The result matters to the native-source/range arrow: a
compatible external current, a background derivative and a physical metric
stress are three distinct objects.

## 1. Exact owner binding and admitted class

On any finite real matrix carrier put

\[
 \mathfrak k=\{X:X^T=-X\},\quad
 \langle X,Y\rangle_F=\operatorname{Tr}(X^TY),\quad
 K=[D,A],\quad D,A\in\mathfrak k.
\]

These are the actual definitions in `ArchiveCommutatorOperators`,
`Matter.GaugeCurvatureOrigin`, `Matter.VectorOperatorOrigin` and
`Algebra.GaugeKineticPositivity`:

\[
 S_c(D,A)=-c\operatorname{Tr}(K^2)=c\|K\|_F^2,\qquad
 L_D A=-[D,[D,A]].                                      \tag{1}
\]

The sign and factor are retained. Positivity uses `c>0`; the free-field
stationarity classification only needs `c != 0`. The owner equation
`L_D A=J` corresponds to `c=1/2` and a supplied skew current `J`.

Admitted field directions are **all** `B in k`, independently of D. The
background derivative below also uses all skew directions when a free D
gate is discussed. Neither a native coframe-to-D map nor independent
physical D variations are asserted to have been constructed by these
owners. A restriction of these directions needs its own owner and is
explicitly outside that gate.

The existing `vector_operator_origin_applies_to_field_equation` takes a
stationarity pairing as an argument. The capsule now proves that this
pairing is the derivative of (1). `vector_laplacian_energy_nonnegative`
alone previously only proved positivity of `Tr(K^T K)`; the equality to
`<A,L_D A>` is now supplied. The self-commutator term `[A,A]/2` vanishes
identically and cannot make this a nonlinear Yang--Mills curvature.
Cross-role curvatures and independently coupled systems keep their own
owners and are not silently included in (1).

## 2. First variation and complete unsourced gate

For skew D, cyclic trace gives, for arbitrary real X,Y,

\[
 \langle X,[D,Y]\rangle_F=\langle-[D,X],Y\rangle_F.
\]

Consequently L_D is self-adjoint and

\[
 \langle A,L_DA\rangle_F=\|[D,A]\|_F^2,\quad
 \ker L_D=\{A:[D,A]=0\}.                               \tag{2}
\]

The exact identity

\[
 S_c(D,A+tB)=S_c(D,A)+2ct\langle L_DA,B\rangle_F
                    +ct^2\|[D,B]\|_F^2               \tag{3}
\]

is compiled together with its actual `HasDerivAt` statement. Native
stationarity is defined by the ordinary derivative of the existing action
on every admitted skew B, not by an Einstein-contrast gate. Taking B=A
in (3), and using the positive Frobenius norm, proves

\[
 \text{full free field stationarity}\iff [D,A]=0.       \tag{4}
\]

This includes every finite size, every skew D and its complete commutant;
it is not a finite sample census. All fibers are nonempty (A=0), and for
nonzero D the nonzero fields A=tD also belong to the fiber. They have
zero action. The proof does not discard their field degrees of freedom.

The independently derived background response at c=1/2 is

\[
 P_D(D,A)=[A,[D,A]],\qquad
 \delta_D S_c[B]=2c\langle P_D,B\rangle_F.              \tag{5}
\]

On (4), P_D=0 as a full matrix, not merely on one selected direction.
For any C1 candidate map D=D(g) and any nonzero scalar coefficient c(g),
the pullback metric derivative also vanishes on that free field gate:
both the coefficient derivative and the operator derivative multiply zero.
This statement does not construct or select such a map.

Thus (1) alone cannot enforce Einstein stationarity for a mapped metric:
the A=0 branch allows every admitted background without imposing a metric
equation. For example the earlier non-Einstein curved probe metrics retain
this zero-field root whenever a map assigns them a skew D. This is a
conditional obstruction to using this **standalone action as gravity**,
not a claim that zero matter stress excludes curved vacuum GR or that the
whole D0 core is impossible.

## 3. Supplied current: complete finite solvability, without source fitting

With c=1/2 the actual derivative equals the supplied work pairing
`<J,B>` for every skew B if and only if L_D A=J. The current is fixed
before solving. Its origin is not supplied by this equivalence.

On the finite-dimensional real inner-product space k, (2) gives the
complete Fredholm alternative

\[
 \exists A\in\mathfrak k:\ L_DA=J
 \iff J\perp\mathfrak z_D,\qquad
 \mathfrak z_D=\{Z\in\mathfrak k:[D,Z]=0\}.            \tag{6}
\]

Necessity follows by self-adjointness. For sufficiency, the range of a
self-adjoint linear map equals the orthogonal complement of its kernel.
The capsule constructs the **actual skew-matrix subspace** of finite
Euclidean space, its actual L_D linear map and the equality
`range = kernel.orthogonal`; it then proves (6). No invertibility or
constant-rank assumption is smuggled into (6). In zero dimension or for
D=0 the range is {0}, as required. All solutions differ precisely by z_D.

For fixed D, a positive range gap lambda_* gives the unique orthogonal
solution A_perp and

\[
 \|A_\perp\|_F\le\lambda_*^{-1}\|J\|_F.              \tag{7}
\]

This is an exact finite bound; neither (6) nor nondegeneracy of D supplies
a uniform positive lambda_* under refinement. An incompatible current
has an empty fiber, not a negative physical response terminal. Defining
J=L_DA after choosing A does not solve a fixed-source problem.

## 4. Derived joint identity and the kernel-response distinction

Jacobi, or direct multiplication, proves the off-shell identity

\[
 [D,P_D]+[A,L_DA]=0.                                   \tag{8}
\]

It is the identity for simultaneous orthogonal conjugation of D and A.
On a sourced field solution it becomes `[D,P_D]+[A,J]=0`. This is an
owned algebraic identity derived from the action; it is **not** yet a
spacetime divergence identity for a local metric stress. In particular,
conjugating A alone while keeping an arbitrary D fixed is not an action
symmetry. A physical spacetime Ward assertion still needs the appropriate
state/action/readout maps.

If D is also freely varied and no other term supplies its equation, its
gate requires P_D=0. Since P_D=L_A D, (2) applied with A in place of D
forces `[D,A]=0`, hence J=0. This rejects every **nonzero fixed current
with this standalone full joint gate**. It does not reject a compatible
current at fixed D or a separately owned coupled action.

For the diagnostic supplied-work functional `S_{1/2}-<J,A>`, on-shell
value is `-<J,A>/2` and is independent of the solution's commutant shift.
This functional is a variational primitive of the already supplied
current; it is **not installed as a new native action**. Even with one
fixed compatible J, the full background response can change:

\[
 P_D(D,A+Z)-P_D(D,A)=[Z,[D,A]],\qquad Z\in\mathfrak z_D. \tag{9}
\]

There is no contradiction with the unique value: differentiating a
reduced value requires a genuine neighboring family of compatible fibers.
Along `[D(t),Z(t)]=0`, the derivative identity is

\[
 \langle[Z,K],\dot D\rangle_F=-\langle J,\dot Z\rangle_F.
\]

For fixed J, compatibility along that family makes the right side zero.
A direction leaving the compatible-source class does not define a
reduced-action derivative. The exact certificate contains two roots of
one fixed nonzero current with a nonzero difference (9), and verifies
the differentiated identity. It never promotes a transverse derivative
into an admissible prepared contrast.

Kernel directions also cannot all be declared gauge. At A=0 every
conjugation tangent `[X,A]` is zero, while nonzero D belongs to ker L_D.
More concretely, A=0 and A=D have different invariant Frobenius norms.
The certificate additionally exhibits a sourced kernel shift changing
that norm, so quotienting the entire kernel would remove more than the
actual conjugation symmetry.

## 5. Exact range obstruction with bounded, nonsingular backgrounds

Let E_ij have entries +1 at (i,j), -1 at (j,i), and zero elsewhere.
For the full six-dimensional real skew 4 by 4 carrier,

\[
 D_{a,b}=aE_{01}+bE_{23},\quad
 \operatorname{spec}L_D=
 \{0,0,(a-b)^2,(a-b)^2,(a+b)^2,(a+b)^2\}.              \tag{10}
\]

An exact orthogonal basis is
`E01,E23,E02+E13,E03-E12,E02-E13,E03+E12`, with squared norms
`2,2,4,4,4,4`. The certificate checks the complete 6 by 6 matrix identity,
not floating eigenvalues. Regular rank is four; a=+/-b !=0 gives rank
two; a=b=0 gives rank zero. This is a different operator from the #317
A4D Laurent symbol and supplies no result about that symbol's strata.

Choose a=1, b=1+delta, 0<delta<=1, and declare one fixed source
`J=T=E02+E13` before solving. Then

\[
 A_\delta=\delta^{-2}T,\quad L_{D_\delta}A_\delta=T,
 \quad\|L_{D_\delta}^{-1}\|_{\mathrm{range}}=\delta^{-2},
\]
\[
 \det D_\delta=(1+\delta)^2\ge1,\quad
 \|D_\delta\|_F^2=4+4\delta+2\delta^2\le10,
\]
\[
 \|A_\delta\|_F=2\delta^{-2},\quad
 S_{1/2}(D_\delta,A_\delta)=2\delta^{-2},\quad
 P_D=2\delta^{-3}(E_{23}-E_{01}),\quad\|P_D\|_F=4\delta^{-3}. \tag{11}
\]

Every positive-delta member has the same rank and a nonempty exact source
fiber. All solutions have at least the orthogonal-solution norm in (11).
Indeed the singular values of D_delta itself are 1,1,1+delta,1+delta:
even its inverse stays uniformly bounded. The degeneracy belongs to the
commutator range, not to D. An approximate field A_delta+delta^-1 T has
equation residual delta T but field error 2/delta; vanishing residual
therefore does not give a vanishing state error in this family.
The simultaneous identity still holds, with both commutators in (8)
zero. Hence rank constancy, source compatibility, bounded/nonsingular D
and this Ward identity do not imply a uniform inverse or response bound.
At delta=0 the fixed source becomes a nonzero kernel vector, so the
limiting source fiber is empty; no soundness claim is made for this limit.

This is a finite owner counterexample to inferring the missing range
estimate from insufficient hypotheses. It is not a fixed smooth A4D
metric/source counterexample to #310, nor a new physical refining family.

## 6. Hostile controls and protected exceptions

The independent exact certificate checks every skew coordinate, the
Frobenius off-diagonal factor two, field/background signs, source range,
all matrix Ward entries, complete eigenbasis and actual orthogonal action.
It retains the following exceptions rather than extending (4) beyond its
proof:

* A sphere constraint can have a nonzero-curvature critical eigenvector;
  its radial variation is excluded. No such native constraint is added.
* The Lorentz Lie algebra so(1,2) has a different, indefinite trace form.
  The displayed matrices N=K01+E12 and H=K02 satisfy `[N,H] !=0` but
  `Tr([N,H]^2)=0` and `[N,[N,H]]=0`. They are not real skew matrices.
  Thus the positive-norm argument cannot be exported to that algebra.
* Fixing D leaves compatible sourced roots alive; freely varying D adds
  a different equation. Extra action terms require their own owners.
* c=0 is a degenerate zero action and is outside the nonzero-coefficient
  classification.

For a separately supplied `FiniteSeamMap B`, `seamEnergy` is likewise a
positive commutator norm, but the vector operator L_D above uses skew D.
We do not replace a general seam B by skew D or infer its spectrum from
(10). Nor does `matrixRepYangMillsAction` with independently supplied
curvature slots construct a physical curvature/metric/source map.

## 7. Verification and exact remaining dependency

The [Lean capsule](certificates/a4d_native_vector_source.lean) prints 20
actual theorem axiom dependencies and eight load-bearing propositions.
It proves the generic variation/gate/range/identity results, including
finite source sufficiency. The [capture](certificates/a4d_native_vector_source_output.txt)
and [source hashes](certificates/a4d_native_vector_source_results.json)
retain its compiler result and transitive inputs. Only `propext`,
`Classical.choice` and `Quot.sound` occur, with no `sorryAx`.

The [exact checker](certificates/a4d_native_vector_source_check.py) and
[immutable ledger](certificates/a4d_native_vector_source_certificate.json)
cover 51 grouped symbolic four-dimensional source/gap/exception controls.
Replay from the repository root; the default run never rewrites its ledger:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_vector_source_check.py
```

The source stress still needs a native local matter action on the same
physical carrier and its metric pullback. A supplied skew current J is
not that stress. For example the separate `ArchiveStressCoupling` source
is a **symmetric** matrix, its defined anomaly factor times the canonical
Laplacian; its proved anomaly-free zero result does not provide a nonzero
local metric source here. Neither object can be interchanged by its name.

The native physical state/variation/action map remains the first open
arrow. The results here exhaust the independently free real-skew
commutator class, preserve its genuine kernel and specify exactly which
source/range assumptions a future map must meet. They do not prove that
this class contains every remaining core-owned mechanism. The ten metric
slots, 24 physical connection rows, native refinement, curved recovery
and soundness remain separate obligations until such a map exists.
