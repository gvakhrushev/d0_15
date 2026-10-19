# A4D geometry-first continuation: horizontal Fredholm reciprocity and one-round native hidden-port source

**Date:** 2026-10-19  
**Status:** RESEARCH / exact mathematical identity + exact native original-port component; conditional physical application.  
**Home:** draft PR #383, repository gvakhrushev/d0_15.  
**No action change, no claim promotion; GR_closed=false.**

## 1. New operational strategy

The original mixed-rectangle memo in this PR tests whether two finite stationary realizations give the same metric contrast. A stronger *local criterion* can make the response comparison automatic: a connection-center tangent is geometrically invisible along every metric direction for which the **same native connection Euler equation admits a horizontal lift**.

This is a finite, same-action Hessian reciprocity theorem; it is not a gauge argument, a new field equation or a proposal to force the Y center to vanish. The criterion applies to whatever differentiable action is *actually selected*. It is already meaningful for the original naked six-face geometric action. It cannot silently import the full Book Cost−Info without its separate owner.

## 2. Exact horizontal reciprocity (all finite dimensions)

Let A(q,K) be a C² scalar action on an open finite coordinate chart, with q in an m-dimensional physical metric/Gram chart and K in an n-dimensional connection chart. Use the literal variational covectors

E_K = D_K A, E_q = D_q A,
L = D_K E_K = L^T, B = D_q E_K.

The identity B^T = D_K E_q holds because **the same scalar action** defines both rows and q, K use consistent coordinate pairings. In symmetric Gram coordinates retain all factor-2 weights for off-diagonal components and the corresponding dual conversion. An invertible convention change does not change the ranks below.

For a fixed metric q, ANY smooth connection curve K(z), its tangent v(z)=dK/dz, ANY fixed metric direction u and ANY candidate connection lift w(z), define two directly measurable residuals:

r_center = L v = dE_K(q,K(z))/dz,
r_lift   = L w + B u.

Then, by symmetry and the chain rule, the following is an **exact identity even OFF SHELL**:

  d/dz <E_q(q,K(z)),u>
    = <v,Bu>
    = <v,r_lift> - <r_center,w>.                           (R1)

Consequently,

  |<E_q(q,K(z1))-E_q(q,K(z0)),u>|
    <= integral[z0,z1] ( ||v|| ||r_lift|| + ||w|| ||r_center|| ) dz.     (R2)

No inverse of L appears. Large/resonant lifts still contribute through ||w||, so this is **not** a covert uniform-rescue claim.

If K(z) is an EXACT connection-stationary curve, then r_center=0. If the connection equation admits a compatible first-order lift w for one fixed u at EVERY z on the curve, r_lift=0 and <E_q,u> is exactly constant along that curve. If all physical metric directions u lift, the entire physical E_q vector is constant. Different disconnected exact roots can have different responses; connectedness plus liftability matters.

This concerns the connection equation only, not the full matter, preparation and clock Euler unless those variables are included in K with the **actual full action**.

## 3. Exact rank-duality statement

At a fixed stationary background and Hessian blocks L=L^T and B, define the horizontal metric subspace

  H = { u in R^m : B u in im L }.

Because im L = (ker L)^perp, there is an exact equivalence

  u in H  <=>  <B^T v,u>=0 for every v in ker L.

Therefore

  H = [ B^T ker L ]^perp,
  dim H = m - rank(B^T|ker L).                              (R3)

For ANY matrix M=B^T in dual coordinate conventions,

  rank([L;M]) - rank(L) = rank(M|ker L).                       (R4)

**Exact consumed owner counts:** A4D_Y_SLOW_JOINT_CONTINUATION.md has n=96, m=40, rank L0=80 and rank([L0;M0])=88. Therefore dim ker L0=16 and rank(M0|ker L0)=8, while the joint-invisible kernel has dimension 8. If and only if M0 is the transpose mixed Hessian B^T for the same physical Gram directions (with convention conversion), (R3) additionally gives an exactly 32-dimensional linearized horizontal-compatible metric space among the forty phase-resolved Gram directions.

This **32** is a derived algebraic rank consequence under the specified mixed-Hessian identification, NOT a claim that 32 geometries are physically admitted, that eight other directions are forbidden by D0, or that the full native Cost−Info has the same blocks. The next computational test should explicitly construct B from the original action and compare it with M0 using the correct Gram dual weights.

### Existing positive carrier

Merged #232 gives an exact non-gauge curved Y connection-stationary family at flat solder. A4D_Y_SLOW_JOINT_CONTINUATION.md further proves exact link and solder equations for arbitrary **constant nondegenerate coframes with a spacelike difference plane**, plus an exact metric completion with varying time columns and constant spatial Gram. The explicit dependence K(q,z) provides horizontal lifts in the declared constant-coframe directions. Thus the response equality in these directions also follows from (R1) without classifying or suppressing Y. This does not infer curved macroscopic Einstein universality outside that class.

## 4. A hard owner-native information scale: the original nonblank Golden port

A complementary issue survives the geometric theorem: a complete native information-price candidate is not necessarily constant along geometry-invisible fine-record fibers.

Use the exact original full128 one-round instrument, not the separate k-Golden filled-return detector. Its original conditional probabilities for each nonblank label are (p²,p), with primitive Golden code reference (p,p²), p=phi^-1. The conditional full-code relative-information cost is EXACTLY p³ per nonblank label, from the existing #334/#381 owner.

The original nonblank-label effect is

  E_label = eps Delta_h ( I - h² Delta_h/256 ),
  eps=p² h²/64.

On a first-shell scalar base Delta_h=lambda_h I and a normalized trace-one preparation, its actual field tangent, even when dDelta_h is NOT a scalar matrix, yields

  dP_label = eps (1 - h² lambda_h/128) dlambda_tr,
  dlambda_tr=Tr(dDelta_h)/16.

Hence for the literal conditional port KL component

  K_port = p³ P_label,

  (1/h²) dK_port =
         (p^5/64)(1 - h² lambda_h/128) dlambda_tr.         (R5)

This is a source component of a **candidate original full-code relative-information observable**; selection of that observable as the real whole-history Book physical action remains open. It is a link/source tangent in the pinned example, NOT a measured metric-response difference or an identified Einstein stress tensor.

### Exact finite J23 original-channel pin

At the actual published original L=4, h=1/4, first shell and homogeneous J23 proper-Lorentz link direction (all from the owned full128 first-source receipt),

  lambda=288/25,
  dlambda_tr=-144/25,

the exact nonblank-label source is

  dP_label = (-42957+14319 sqrt(5))/5120000
           = -0.002136473169957131...

Therefore its native code port term has the **exact algebraic value**

  dK_port = (157509-71595 sqrt(5))/5120000
          = -0.0005043529002143444...

and the comparable h^-2 normalized component is

  h^-2 dK_port = (157509-71595 sqrt(5))/320000
               = -0.00806964640342951...                  (R6)

These equalities have been independently checked in Q(sqrt5) arithmetic, matching the owner's published original source.

On any hypothetical refining first-shell family with bounded lambda_h and dlambda_tr -> nonzero d lambda (THIS EXISTENCE IS NOT CLAIMED for the pinned J23 tangent across h),

  lim[h->0] h^-2 dK_port = (p^5/64) d lambda.              (R7)

For the fixed numerical reference dlambda=-144/25, that coefficient is (99-45 sqrt(5))/200 = -0.00811529493745268..., not zero. Thus a proof that discards this one-round fine-port *individual term* as o(h²) merely from smooth/low-shell scaling is invalid. It MAY cancel against other actual terms in the complete selected native price; a nonzero summand is not a no-go for the total. A multi-round native clock n_h eps -> beta instead gives the already-owned unnormalized p³ beta d lambda first source, a distinct scaling regime.

## 5. Precise joint strategy, not a new selector

There are two rigorously separable research actions:

1. **Geometric reciprocity:** Build the SAME-A mixed Hessian blocks of the original six-face star on the owned Y carrier; verify the 40 Gram dual conventions and the rank-eight Fredholm obstruction. On #334's actual fourth-order crossed-Weyl jet, directly compute (R1) as a diagnostic with r_center=partial_z E_K, r_lift=Lw+Bu, keeping the w norm. Prove the integral in (R2) is o(h²) only on a physically admitted near-flat class and only with C¹ bounds.
2. **Physical same-action admission:** Read the native observation/history algebra, true Cost−Info aggregator, full original 40+matter+prep+clock source. Do not identify binary odds, mean Shannon, modal blank word and coherent full-code KL as the same action. If full-code KL is selected, carry (R5) alongside all other fine/coherent/clock/work sources and prove their **aggregate** source compatible with Einstein; otherwise prove the physically selected coarse programme excludes this term rather than omitting it by convenience.

The accepted #377 endpoint geometric probe still requires a native endpoint admission and a refinement-uniform transfer. Finite Y response-nullity alone and exact rank-eight reciprocity cannot provide existence of generic curved physical roots, the actual matter Ward, G/Lambda normalization, or positive D0=>GR.

## 6. Reproduction

Run:

  python3 02_REGISTRY/research/sources/d0_mixed_rectangle_2026-10-19/check_reciprocity_and_native_port_scale.py

The standalone script checks the off-shell reciprocity identity, a true liftable and a nonliftable toy direction, disconnected stationary-root control, exact native port algebra and exact original J23 Q(sqrt5) numbers **without importing or replaying the original full128 matrix certificate**. The corresponding exact upstream parent is check_original_full128_J23_port_decomposition.py on #381; the matrix rank parent is a4d_y_slow_joint_continuation_check.py in main.

**SCOPE:** exact algebraic reduction and owner-based new normalization corollary. No D0 full joint-root, native action promotion, or GR closure.
