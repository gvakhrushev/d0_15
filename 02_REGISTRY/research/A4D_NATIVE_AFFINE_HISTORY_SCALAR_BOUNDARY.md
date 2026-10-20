# G0: complete scalar readings of the native affine path transport

Research input: `7c8ee6851dc343927c04f971f0b0de7a10be7b04`, existing #310.
Owner tree: `fd8dfc359d23c9bd79ca23eeed7c045ce9c68c6b`.
Status: **complete classification in the stated total-transport scalar class**.
The physical field-dependent native action, its admission and refinement law
remain OPEN. No new action, path identification or physical postulate is added.

## 1. The actual field-path owner and the exact class

`D0/Geometry/ArchiveAffineCartanConnection.lean` already owns the field-valued
path construction. An affine link is `(U,a)`, with U an invertible real linear
map and a a translation. Its multiplication is

```text
(U,a)(V,b) = (UV,a+Ub).
```

An `AffineCartanConnection N R V` assigns one such map independently to each
stored positive `(site,role)` link. `affineStepMap` uses the inverse stored
link for a backward step. `affinePath` composes the maps in the declared pull
order. Its owned append, reverse and node-gauge laws are respectively

```text
A[pq,x] = A[p,x] A[q,end(p,x)],
A[reverse(p),end(p,x)] = A[p,x]^-1,
A^h[p,x] = h(x) A[p,x] h(end(p,x))^-1.
```

This is the archive `ChainStep` carrier. It is not identified with the scene
K(9,11,13) history carrier. In particular, the affine readout forgets immediate
inverse returns, whereas the positive scene cost in the
[history classification](A4D_NATIVE_HISTORY_ACTION_BOUNDARY.md) retains them.

Consider precisely a single real scalar rule f on total affine maps, independent
of the connection, external fields, endpoints and the chosen word, satisfying

```text
f(A[pq,x]) = f(A[p,x]) + f(A[q,end(p,x)])
```

for every actual connection, site and pair of words at a fixed N. This is the
candidate **factorization through total affine transport**, not an assertion
that every native action must have this form. No continuity is assumed yet.

**Complete reduction.** The displayed native law holds if and only if

```text
f(gh)=f(g)+f(h)       for all affine maps g,h.                 (1)
```

For necessity choose two distinct roles r,s. The stored links `(x,r)` and
`(x+r,s)` are different even at period two, so they may be set to arbitrary
g and h independently, with all other links identity. The one-step and two-step
words give (1). Sufficiency is the owned append law. The whole argument,
including the two-link realization and the equivalence, is compiled in Lean
as `complete_native_scalar_class`. Thus (1) is derived from this exact path
interface, not supplied as an extra consequence of native physics.

## 2. Complete affine character classification

Let V=R^d with d>=2, in particular the actual four frame components. Every
solution of (1), with no regularity restriction, is uniquely of the form

```text
f(U,a) = b(log |det U|),       b : R -> R additive.             (2)
```

Conversely every additive b gives a solution. If f is continuous at identity,
then b(t)=c t for one real constant c, hence

```text
f(U,a) = c log |det U|.                                      (3)
```

Here is a full algebraic proof, including completeness.

1. Equation (1) gives f(1)=0, f(g^-1)=-f(g), conjugacy invariance and vanishing
   on finite-order elements. These identities are compiled for the literal
   `AffineCartanMap` operations.
2. Write T_v=(I,v). Conjugating by the dilation D=(2I,0) gives
   D T_v D^-1=T_(2v)=T_v T_v. Conjugacy and additivity force f(T_v)=0 for
   every v. As `(U,a)=T_a(U,0)`, f is completely insensitive to translation.
   These are compiled universal theorems, with no continuity or finite sample.
3. For each elementary shear E_ij(t)=I+t e_ij, i!=j, conjugation by the
   diagonal matrix having 2 in slot i and 1 elsewhere gives E_ij(2t).
   Since E_ij(t)^2=E_ij(2t), its scalar is zero by the same argument.
4. These shears generate SL(d,R). For completeness, elimination by row additions
   clears each pivot column; a zero pivot is repaired by adding a row with a
   nonzero entry. Signed row exchanges are also shear products. The residual
   diagonal has product one and is a product of embedded `diag(t,t^-1)`.
   Each such diagonal is a shear product because, in its two-dimensional block,

   ```text
   W(t)=E12(t) E21(-1/t) E12(t)=[[0,t],[-1/t,0]],
   W(t) W(1)^-1=diag(t,t^-1).        (t != 0)
   ```

   Therefore f vanishes on all determinant-one linear factors. Any U factors
   as `diag(det U,1,...,1)` times an element of SL, so f factors uniquely
   through the determinant as an additive character a of R*. The negative
   sign has order two and contributes zero. Define b(t)=a(exp t); positivity,
   exponential multiplication and log inversion give precisely (2).
5. Under continuity at identity, b is continuous at zero. Its additive law
   first gives b(q)=q b(1) on rationals. Rational approximation and continuity
   yield b(t)=t b(1) for every real t. Conversely (3) is continuous.

This determinant classification is an analytic/algebraic proof. It is not
advertised as a compiled Gaussian-elimination or Cauchy-equation theorem.
The exact checker verifies the parameterized generator identities used in
the proof. Discontinuous additive b are retained in (2), not silently omitted.

**Actual path consequence.** Equal linear links give equal scalar values on
every word for arbitrary independently varied translations. This is compiled
as `all_raw_shift_variations_invisible`. It includes all components of the
coframe when they enter as the affine shifts, regardless of their scale.
The actual flat translation/coframe weld in the owner does not repair this
loss. On GL links (3) still detects determinant changes; it is not the zero
functional on the full GL carrier.

## 3. The Lorentz restriction does not need a GL extension

Restricting (2) to Lorentz links immediately gives zero, since |det U|=1.
One might instead define the scalar only on the physical proper,
orthochronous affine Lorentz group, with no GL extension. The complete answer
is still **zero**, even without continuity. The following proof removes that
possible hidden extension premise.

An additive character is invariant under conjugacy. Whenever g is conjugate
to g^-1, its value is zero. In SO+(1,3), every pure boost along a spatial
direction is conjugate to its inverse by a spatial pi rotation about a
perpendicular axis. Every spatial rotation is likewise conjugate to its
inverse: choose its fixed axis and reflect the rotating plane while reversing
that axis, an orientation-preserving three-dimensional rotation. For the
identity and pi-angle cases, finite order gives the same conclusion.

Every Lorentz matrix L in SO+(1,3) is a boost times a spatial rotation.
Indeed let its future unit time column be `(gamma,v)`, so gamma>=1 and
gamma^2-|v|^2=1. The explicit boost

```text
B_v = [[gamma, v^T], [v, I + vv^T/(gamma+1)]]
```

has that time column, is proper and orthochronous, and preserves eta.
`B_v^-1 L` fixes the time axis; its spatial restriction is in SO(3).
For the rotation assertion above, a real odd-dimensional orthogonal matrix
of determinant one has an eigenvalue +1 (real eigenvalues are +/-1 and
nonreal eigenvalues occur in conjugate pairs). Its orthogonal plane carries
an ordinary two-dimensional rotation. This supplies the stated axis without
an assumed classification theorem. Thus every linear Lorentz factor has
zero scalar.

For the translations, spatial pi rotations send each spatial coordinate
translation to its inverse, so all spatial translations have zero scalar.
Use the rational boost with time-space block
`[[5/4,3/4],[3/4,5/4]]`. Conjugation takes T_(t e0) to
T_((5t/4)e0+(3t/4)e1). Killing the spatial summand gives
`a(5t/4)=a(t)` for the additive time function a. Multiplying by four gives
5a(t)=4a(t), so a(t)=0. Every affine Lorentz map is a translation times
a linear Lorentz map, and hence has zero scalar. All O(1,3) components are
also covered: squaring moves a component into SO+(1,3), and twice the scalar
then vanishes. The result is complete on either specified Lorentz group.

The native two-free-link argument of Section 1 also applies on this subgroup:
choose both free links inside it. No non-Lorentz physical variation is needed
for this second proof. Generator conjugation and rational-boost controls are
exact; the global boost/rotation decomposition remains an analytic proof.

## 4. Variations, gauge, refinement, and the gravity consumer

The exact scalar node-gauge law, compiled from the literal affine owner, is

```text
f(A^h[p,x]) = f(A[p,x]) + f(h(x)) - f(h(end(p,x))).            (4)
```

Consequently closed words have gauge-invariant values. For general GL gauge
an open word need not be invariant. On Lorentz affine fields all three terms
are zero. Equation (4) is not the geometric Ward identity for an independently
constructed matter action; no matter source has been supplied by this scalar.

Consider any finite sum of the classified scalars of words on the full
Lorentz/coframe/matter carrier. It is identically zero, including arbitrary
smooth coefficients multiplying those zero scalars. Hence all 24 link rows
per site (four directions, six Lorentz generators), all 16 raw coframe rows,
and all matter variations vanish. The statement is identity on the whole
carrier, not vanishing of a restriction along selected tangents. All ten
independent symmetric metric probes also have zero contrast whenever lifted.
Packed off-diagonal weights cannot turn the zero covector into a source.
The exact controls use the literal (+---) signs of `roleLorentzMetric`
in `A4DSolderMetricCompletion.lean`, whose source is separately pinned.

For determinant-changing GL links the smooth scalar has first variation
`c tr(U^-1 delta U)` and zero shift derivative. Under arbitrary subdivisions
whose fine affine product is exactly the coarse link, the scalar is exactly
additive under refinement. If the product has relative determinant error
delta, its scalar error is `c log|1+delta|`; |delta|<=1/2 implies an error
at most `2|c| |delta|`. Errors in determinant-one shear or translation sectors
remain invisible even when the matrix error or physical curvature is large.
This quantifies this readout's refinement behavior, not the existence of a
native refinement map preserving all physical fields.

The already proved [centered-metric probe consumer](A4D_NATIVE_CENTERED_METRIC_LIFT.md#6-a-genuine-native-zero-field-root-family-with-a-non-einstein-limit)
provides a compact smooth nondegenerate periodic conformal pencil with

```text
I(g)=-3 pi^2/50,
Delta I_h = epsilon I(g)+O(h),      epsilon=h^(1/3).
```

It includes the actual centered raw-coframe correction, normalization one-half,
and all 24 connection residual rows. If that probe family is admitted for the
present scalar interface, its native contrast is exactly zero, for every
Lorentz connection and every nonzero fixed calibration. The proposed O(h)
transfer fails by its nonzero order-h^(1/3) leading coefficient. No new metric
or fitted source is invented for this consumer. The zero scalar's independent
Euler equations vanish, so stationarity cannot cure this contrast failure.
This does not prove that the full D0 coupled admission/refinement conditions
admit that family: those conditions remain a separate G0 obligation.

## 5. Essential exceptions and the resulting next obligation

The checker preserves the following genuine ways to leave the classified
interface; none is silently excluded from D0:

* A functional of an entire connection can assign context-dependent weights
  to edges and sum them along paths. It is additive on each fixed connection
  but does not factor through a single f of total transport. The two-free-link
  proof cannot change the connection while holding such an f fixed.
* A nonlinear function of a closed holonomy can detect curvature and be gauge
  invariant without being additive under path concatenation. For example a
  trace of `(P-I)^2` fails the additive law on exact Lorentz boosts. This is
  a countercontrol, not an added action proposal.
* Joint coframe/observer/matter dependence can retain tensors which transform
  along with holonomy. Conjugacy of the holonomy alone does not preserve those
  retained tensors. Such joint actions are outside (1).
* Retained length or individual step data distinguish a backtrack from an
  empty path. Positive primitive costs cannot factor through the affine group:
  f(g^-1)=-f(g) precludes costs at least one in both directions. This exact
  obstruction is compiled. It does not invalidate the actual scene cost.
* Endpoint-dependent potentials contribute genuine boundary terms. They cancel
  only with proved boundary conditions or balanced sums. Field-dependent
  endpoint weights cannot simply be declared variationally irrelevant.

Thus the owned affine composition law determines the vector/matrix transport,
but its entire additive scalar total-transport class cannot supply the requested
Einstein metric contrast. The remaining field-action map must retain additional
owned information or use a nonadditive joint field functional. Its actual
definition, admissible family, variations, source and refinement must be derived
from existing owners; merely choosing such a functional would add a postulate.

The [Lean capsule](certificates/a4d_native_affine_history_scalar.lean),
[output](certificates/a4d_native_affine_history_scalar_output.txt),
[receipt](certificates/a4d_native_affine_history_scalar_results.json),
[checker](certificates/a4d_native_affine_history_scalar_check.py) and
[ledger](certificates/a4d_native_affine_history_scalar_certificate.json)
separate compiled interface statements, complete analytic classifications,
and finite controls. G0, source/Ward, curved solutions, soundness/recovery,
positive GR, global closure and the original #310/#202/#317 terminals remain
open and unchanged. This is not a whole-core NO-GO.

Validation: 21 compiled declarations with 36 transitive native source pins,
49 exact controls and 17 rejected false-scope ledger mutations. Only the
standard logical axioms occur. The supported D0 source tree is unchanged.
