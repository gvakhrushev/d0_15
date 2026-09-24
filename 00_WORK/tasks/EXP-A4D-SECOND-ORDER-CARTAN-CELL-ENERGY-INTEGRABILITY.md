# EXP-A4D-SECOND-ORDER-CARTAN-CELL-ENERGY-INTEGRABILITY

## Class

EXPENSIVE / BREAKTHROUGH RESEARCH

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

IN_PROGRESS

## Baseline

Repository:

`https://github.com/gvakhrushev/d0_15`

Minimum baseline:

`c45e6c94759b2d52efdfbe28065038f1bfe60474`

Use newer `origin/main` if available.

This is a stateless mathematical research task. Do not edit Lean claims or lifecycle metadata.

## Frozen frontier

Do not reopen:

- the flat CAR/Hodge Dirac operator;
- the full accepted first jet `H(e)`;
- the moving-d parent Ward;
- the Role/spatial representation weld;
- the 48-dimensional scene-to-shell intertwiner no-go;
- the center-matched dual placement classification.

The frontier is:

```text
LOCATED-DUAL-PAIRING-FIXED-NONLINEAR-CELL-ENERGY-LAW-MISSING
```

The selector variable is the nonlinear quadratic cell law `Q(e)`, not the location of the dual cell.

## Frozen two-model family

Use the two reference actions from the geometric-dual memo:

[
E^{(1)}=E_{flux}+\frac12\sum q_S(e)\psi_S^2,
]

[
E^{(2)}=E_{flux}+\sum q_S(e)\psi_S^2.
]

Their kernels are

[
W_c(e)=I+H(e)+cM_{q(e)}+O(e^3),
]

with `c=1` and `c=2` respectively in kernel normalization.

They share:

- the same located dual;
- the same full uncentered coframe;
- the same flat normalization;
- the same entire derivative `DW|_0=H`;
- the same Nyquist response at first order;
- the same distance-two corner.

Do not use Nyquist or the corner as if they separated these two models.


## Upstream physical-frame boundary from later research

A later located-star/cell-action memo establishes a sharper physical gate:

```text
SOLDERED-CREATOR-FRAME-LIFT-PRIMITIVE-REQUIRED
```

and proves that the two reference kernels and the naive flux seed fail a fixed-counting Lorentz boost test, while a pointwise Lorentz metric star cannot reproduce the staggered off-site jet.

Therefore this task is a PARALLEL ALGEBRAIC INTEGRABILITY LANE.

Its second-order Cartan calculation must not be presented as the first physical blocker or as a replacement for the missing local frame lift.

If `EXP-A4D-SOLDERED-CREATOR-OBSERVER-FRAME-LIFT` lands first, consume its frame-action conventions where relevant but keep Cartan gauge and local Lorentz frame covariance distinct.


## Newly owned affine background action

PR #70 is frozen input.

The repository owns `D0.Geometry.ArchiveAffineCartanConnection`, including `affineTranslation_flat_eq_forwardGaugeCoframe`, affine node gauge/path transport, open curvature/torsion and their gauge laws.

For the flat identity-linear affine connection and node translation `b_x=-L ξ(x)`, the transformed link shift is EXACTLY `forwardGaugeCoframe ξ`. Therefore this task must not search again for a finite background coframe orbit.

For the scaled parameter `t ξ`, the owned flat translation sector gives the exact linear background path

```math
e(t)=t d_f ξ,
```

so on this owner `a=e''(0)=0`.

The unresolved object is the action of the same finite background gauge on the MATTER carrier, hence its second jet `K=Q''(0)`.

PR #70 also owns `no_uniform_radius_lie_closed`. Any matter lift of the full scalar Cartan closure must distinguish factorized-local path cost from a uniformly bounded compressed stencil.

## Primary question

Given

[
W(0)=I,
qquad
DW_0[h]=H(h)=-(G^*+G),
]

what does exact second-order covariance of the SAME action force on

[
D^2W_0[h,h]?
]

In particular: does the already-owned finite affine BACKGROUND gauge admit a derived matter representation whose second jet selects `c`, or is that matter representation/second jet itself a new primitive?

## Mandatory two-jet algebra

Let

[
Q(t)=I+tG+\frac{t^2}{2}K+O(t^3)
]

be the matter-field transformation and

[
e(t)=th+\frac{t^2}{2}a+O(t^3)
]

the corresponding background orbit.

For quadratic energy covariance

[
W(e(t))=Q(t)^{-T}W(0)Q(t)^{-1},
]

derive exactly:

[
oxed{
H(a)+D^2W_0[h,h]
=
2(G^T)^2+2G^TG+2G^2-(K^T+K).
}
]

Check all signs and conventions.

For the exponential specialization `Q(t)=exp(tG)`, `K=G^2`, hence:

[
H(a)+D^2W_0[h,h]
=
(G^T)^2+2G^TG+G^2.
]

Do not suppress `K`: the project already knows from `movingDifferential_infinitesimal` that quadratic transformation remainders matter.

## Frozen scalar witness discovered by coordinator

Work on one embedded Role direction with `L≥3`.

Let:

[
U f(x)=f(x+1),
qquad
D=\frac L2(U-U^{-1}),
qquad
\Delta=L(U-I),
]

[
\xi=\delta_0,
qquad
h=\Delta\xi,
qquad
G=M_\xi D.
]

Then:

[
H_0(h)=\frac12(M_hU+U^{-1}M_h)=-(G+G^T).
]

For this witness:

[
h(0)=-L,
qquad
h(-1)=L,
]

and zero elsewhere.

Also:

[
G^2=(G^T)^2=0.
]

The diagonal of `2G^TG` equals:

[
\frac{L^2}{2}
]

at sites `+1` and `-1`, and zero at site `0`.

On the scalar sector, for arbitrary second background acceleration `a`:

[
\operatorname{diag}H_0(a)=0.
]

For the memo family:

[
D^2W_c|_0[h,h]=2cM_{h^2}.
]

Therefore second-order covariance forces the matter-transformation second jet to satisfy:

[
K_{+1,+1}=\frac{L^2}{4},
]

[
K_{0,0}=-cL^2,
]

[
K_{-1,-1}=L^2\left(\frac14-c\right).
]

In particular the naive exponential completion `K=G^2=0` fails for EVERY `c`; so does a linear path with `K=0`.

Verify this result independently and generalize it.

This is a research starting result, not yet Lean-owned.

## Phase A — exact second-order covariance calculus

Develop the full finite-dimensional two-jet calculus for:

- quadratic kernels;
- bilinear pairings;
- primal/dual maps;
- moving differentials;
- moving Hodge/constitutive maps.

Separate clearly:

- background acceleration `a=e''(0)`;
- matter action second jet `K=Q''(0)`;
- energy Hessian `D²W`;
- connection/differential variations.

## Phase B — scalar Cartan witness classification

For `L=3,5` and generic `L≥3`:

1. prove the formulas above;
2. compute the full matrix, not only its diagonal;
3. determine all second jets `K` compatible with a supplied `c`;
4. determine which parts of `K` are forced and which are invisible.

Ask whether locality, degree preservation, pairing compatibility and constant preservation constrain `K`.

## Phase C — derive the matter lift of the owned affine gauge

Do not search for another finite coframe transformation.

Start from the owned affine node gauge/background action and determine whether it induces an independently motivated representation on archive matter cochains/Fock states.

The matter lift must:

- have first derivative equal to the accepted Cartan matter generator `G_ξ`;
- compose according to the same node-gauge law;
- respect the relevant pairing and degree structures;
- distinguish factorized locality from uniformly bounded matrix support;
- not be defined by demanding invariance of a preferred energy.

Audit the exterior/frame lift of the affine linear part, site/fiber action induced by the translation part, path-word/factorized-local representations, and the rational local gates already owned by PR #70 where applicable.

The primary unknown is `K=Q''(0)`, not the existence of the background orbit.
## Phase D — composition constraints on the second jet

If a finite local family exists, derive its group/composition law to second order.

For parameters `ξ,ζ`, determine the cocycle constraints on:

[
K(ξ),
qquad
B(ξ,ζ)
]

coming from composition.

Determine whether the required scalar-witness diagonal entries can arise from a genuine local second jet.

## Phase E — selector test for c

Only after `K` is independently fixed, test:

[
c=1,qquad c=2.
]

Outcomes:

- one value survives;
- neither survives;
- both survive;
- a different `c` is selected;
- no constant-`c` diagonal completion can work.

Do not choose `K` separately for each energy model unless the purpose is to prove nonselection.

## Phase F — second-order Ward with moving d

Integrate the energy Hessian calculation with the already-owned moving differential.

The second-order identity must retain terms induced by the motion of:

[
d_P,quad d_D,quad S,quad Q.
]

Do not freeze differential variations.

Use the existing first-order six-term Ward as the linear boundary.

## Phase G — distinguish Cartan gauge from Lorentz frame covariance

Do NOT conflate:

- discrete Cartan/coframe gauge generated by `ξ`;
- internal Lorentz frame rotations of the solder;
- Role permutations.

Continuous Lorentz transformations do not act on archive sites by `x↦Λx`.

The finite Cartan integrability question must be solved before using a Lorentz boost as a selector.

## Phase H — reverse-star and volume only after second-order Cartan

If the Cartan second jet leaves a modulus, then test additional all-order constitutive identities:

1. reverse-star/double-star;
2. energy weight = specified geometric volume/minor law;
3. density exponent.

Keep the conditional tensorial deformation theorem as a hostile control:

[
E_c\mapsto(1+\lambda z_c)E_c,
quad
z_c(0)=Dz_c(0)=0.
]

Lorentz tensoriality by itself does not eliminate such a scalar multiplier.

## Required direct answers

1. What is the exact second-order covariance identity?
2. What data beyond `G` are required?
3. Does `e''(0)` affect the scalar diagonal witness?
4. What second jet `K` is forced by the delta witness?
5. Why does `Q=exp(tG)` fail?
6. Does the owned affine background action admit a matter representation with tangent `G`?
7. Does the matter-representation composition law fix `K`?
8. Does the fixed `K` select `c=1`, `c=2`, another value, or none?
9. If no finite action exists, what exact no-go blocks it?
10. Which part of the remaining energy freedom is truly constitutive rather than symmetry-jet freedom?
11. Does reverse-star reduce the remaining modulus after Cartan integrability?
12. Is an energy-volume identity still an independent primitive?

## Required exact controls

- `L=3` delta witness;
- `L=5` delta witness;
- generic support proof for `L≥3`;
- arbitrary second background acceleration `a`;
- `K=0`;
- `K=G²`;
- `c=1`;
- `c=2`;
- at least one non-delta `ξ`;
- moving-d product-rule regression.

## Primary terminal menu

Return ONE:

```text
SECOND-ORDER-CARTAN-INTEGRABILITY-SELECTS-CELL-ENERGY
SECOND-ORDER-CARTAN-INTEGRABILITY-REJECTS-CURRENT-TWO-MODEL-FAMILY
FINITE-CARTAN-SECOND-JET-PRIMITIVE-REQUIRED
BOUNDED-LOCAL-FINITE-CARTAN-ACTION-NOGO
SECOND-ORDER-CELL-ENERGY-MODULUS-CLASSIFIED
```

## Secondary terminals

```text
SECOND-ORDER-COVARIANCE-IDENTITY
SCALAR-DELTA-WITNESS-STATUS
EXPONENTIAL-CARTAN-STATUS
MATTER-TRANSFORMATION-SECOND-JET-STATUS
BACKGROUND-ACCELERATION-STATUS
CELL-HESSIAN-STATUS
MOVING-D-SECOND-ORDER-STATUS
REVERSE-STAR-POSTSELECTOR-STATUS
ENERGY-VOLUME-POSTSELECTOR-STATUS
```

## Deliverable

Produce:

`MEMO_A4D_SECOND_ORDER_CARTAN_CELL_ENERGY_INTEGRABILITY.md`

End with one terminal verdict and theorem-ready Lean handoff.

Do not end with “more research needed”.
