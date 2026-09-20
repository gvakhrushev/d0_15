# Worker Task C1 — formalize the canonical 326 -> 327 common carrier

Branch: research/l2-c1-common-carrier-lean

Primary source:
- C1_COMMON_CARRIER_RESULT.md
- original research memo/certificate hashes are pinned there.

Do not redo the research classification.

## Carrier

Use the actual K(9,11,13) scene edge type if available.
Do not represent absent intra-zone edges as arbitrary Matrix entries unless the subtype proof is explicit.

Define:

- unsigned incidence B_+;
- signed incidence B_- for the canonical transitive orientation fixed by degree order 9<11<13;
- block decomposition by the three zone pairs;
- row/column centering operators C_9,C_11,C_13.

## C1-T1 — rank and kernel dimensions

Prove on the actual scene:

rank B_+ = 33,
rank B_- = 32,

hence

finrank ker B_+ = 326,
finrank ker B_- = 327.

Prefer a sector decomposition proof over native_decide on a 33x359 matrix.

## C1-T2 — K0 common sector

Define blockwise double-centering.

Prove:

dim K0 = 296,

K0 <= ker B_+,

K0 <= ker B_-

and, if feasible, K0 lies in every uniform zone-pair signed orientation kernel.

## C1-T3 — exact intersection

For the canonical transitive orientation prove:

dim(ker B_+ ∩ ker B_-)=316.

Prove the A_9 and A_13 kernel lines coincide and the A_11 lines are:

v_+=(13,-9),
v_-=(13,+9).

## C1-T4 — overlap/projection

With the Euclidean edge inner product prove:

||v_+||=||v_-||,

<v_+,v_-> / ||v_+||^2 = 2/11.

Define P_- as orthogonal projection onto ker B_-.

Prove P_- v_+ = (2/11) v_-.

Derive injectivity of F=P_-|ker B_+.

## C1-T5 — explicit isometry

Define Phi/U by:

U(X)_(11,13)
 = X_(11,13)
 - (2/13) C_11 X_(11,13) 1 1^T,

and identity on the other two blocks.

Prove:

U(ker B_+) <= ker B_-,

U is linear,

U is an isometry,

U is identity on the 316-dimensional intersection,

U is identity on K0.

Do not define U only via an abstract existence theorem; export the explicit finite formula.

## C1-T6 — complement mode

Define block-constant omega=(13,-11,9).

Prove exactly:

B_- omega=0,

B_+ omega is 0/234/0 on zones 9/11/13,

||omega||^2=42471,

im U = ker B_- ∩ omega^perp.

## C1-T7 — uniqueness/canonicity

State all structures explicitly.

Prove the strongest practical finite theorem:

any H-equivariant Euclidean isometry ker B_+ -> ker B_- which is identity on the literal intersection and has positive/polar sign on the A_11 sector equals U.

Do not claim absolute canonicity without these hypotheses.

## C1-T8 — adjoint and projector

Prove:

U^* U = I,

U U^* = I - omega omega^T / 42471

on ker B_-.

Export the matter-current projector

P_mg = I - omega omega^T/42471.

## Mandatory semantic firewall

In theorem/doc comments:

- B_+ is the unsigned endpoint-sum / A1 trace operator.
- B_- is the signed current divergence.
- Do not call B_+ the Hodge divergence or Bianchi operator.
- Do not call U a diffeomorphism.
- Do not claim that U alone derives the Einstein equation.

## Metric residual test

Add a separate theorem or executable check for zone-constant positive rho showing:

sign <v_+,v_->_rho = sign(13 rho_9 - 9 rho_13).

This theorem must remain visible because it prevents silently replacing A1's rho-weighted pairing by the Euclidean pairing used to define U.

## C1-T9 — canonical rho sign bridge

Import the owned scene Perron profile from D0.VNext2.ScenePerronTraceCanonicity.

Prove:

13 * (1/(sceneRho+9)) - 9 * (1/(sceneRho+13)) > 0

using sceneRho_pos.

Conclude that the rho-weighted A_11 polar sign equals the Euclidean sign for this profile.

IMPORTANT: this theorem does not prove A1 uses that rho. Keep a separate typed hypothesis/bridge:

A1VertexWeight = fullScenePerronVector

or the exact repository-equivalent statement.

If that ownership bridge is absent, leave it OPEN rather than silently substituting the Perron profile.

## Negative controls

1. K(5,7,5): the middle-sector overlap is zero and F is not injective.
2. K(4,6): signed and unsigned kernels coincide after bipartite switching.
3. Cyclic orientation: intersection drops to K0=296 and 30 standard modes are altered.
4. rho with 13 rho_9 < 9 rho_13 flips the weighted polar sign.

## Status rule

After T1-T8:
- create/upgrade a dedicated common-carrier LEAN_PROVED claim;
- D0-HODGE-LINKS-001 must remain OPEN unless the rho-weighted metric compatibility and typed source/action coupling are also proved.

## Final report

Return:
- module path;
- theorem names T1-T8;
- explicit U definition;
- orientation convention;
- rho-metric theorem;
- negative controls;
- claim status changes;
- validate_repo.py;
- generate_lean_views.py --check;
- lake build D0.All.
