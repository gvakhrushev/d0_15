# C1 Result Review — canonical common carrier between signless A1 edge data and signed Hodge currents

Date: 2026-09-20

Source research artifacts supplied to reviewer:
- memo SHA-256: a0509687334ad53ca9d2f6ea719dfad718c2ed370b0f5e44927f28ff4ef37f9f
- verifier SHA-256: 1c552c0150852c9b2eb035428f9b58bc47e88f936ed7ed60f5cdf377d62428b8

Status in this repository: RESEARCH-CERTIFIED / FORMALISM until T1-T8 below are formalized in Lean.

## Reviewer verdict

The central C1 hypothesis is positive.

For K(9,11,13), with unsigned incidence B_+ and the signed incidence B_- for the intrinsic transitive zone orientation

V_9 -> V_11,
V_9 -> V_13,
V_11 -> V_13,

there exists a canonical Euclidean H-equivariant isometric embedding

U : ker(B_+) -> ker(B_-),

where H = S_9 x S_11 x S_13.

The exact formula is

U(X)_(11,13)
  = X_(11,13)
    - (2/13) C_11 X_(11,13) 1_13 1_13^T,

with

U(X)_(9,11)=X_(9,11),
U(X)_(9,13)=X_(9,13),

and C_11 = I - (1/11) 11^T.

Only the 10-dimensional A_11 sector is altered.

## Exact finite structure

Let

K_0 =
(A_9 tensor A_11)
+ (A_9 tensor A_13)
+ (A_11 tensor A_13),

dim K_0 = 80+96+120 = 296.

Then

ker(B_+) ~= K_0 + A_9 + A_11 + A_13,
dim ker(B_+) = 326,

ker(B_-) ~= K_0 + A_9 + A_11 + A_13 + 1,
dim ker(B_-) = 327.

For the transitive orientation,

dim(ker(B_+) ∩ ker(B_-)) = 316.

The only mismatch among the standard sectors is A_11.

On its two-copy multiplicity space:

v_+ = (13,-9) in ker(B_+),
v_- = (13,+9) in ker(B_-),

with the natural edge metric diag(9,13),

<v_+,v_-> / (||v_+|| ||v_-||) = 2/11.

Thus if

F = P_- | ker(B_+),

then the singular values are

1 with multiplicity 316,
2/11 with multiplicity 10.

Hence F is injective, and its polar-normalized map

U = F (F^* F)^(-1/2)

is an isometric embedding.

## One-dimensional complement

The signed-Hodge carrier has one extra H-trivial mode

omega = (13,-11,9)

on the three edge blocks (9,11), (9,13), (11,13).

Exactly:

B_- omega = 0,

B_+ omega =
0 on V_9,
234 on V_11,
0 on V_13,

and

||omega||^2 = 9*11*13*(9+11+13) = 42471.

The image of U is

im(U)=ker(B_-) ∩ omega^perp.

The adjoint satisfies

U^* U = I,

U U^* = I - (omega omega^T)/42471

on ker(B_-).

Therefore the matter-current projector onto the gravity-visible image is canonical and coefficient-free.

## What makes U canonical

The word "canonical" is conditional on explicit structures.

The common irreducible H-sectors occur multiplicity-free, so

dim Hom_H(ker B_+, ker B_-)=6.

H-equivariant isometries leave independent signs on those six sectors.

Requiring identity on the 316-dimensional literal intersection leaves only the A_11 sign unresolved.

Polar positivity of F selects the sign because

(13-9)/(13+9)=2/11 > 0.

Thus the canonical data are:

1. the Euclidean H-invariant edge metric;
2. the transitive orientation class fixed by the intrinsic degree ordering 9<11<13;
3. polar positivity.

Without these, uniqueness is false.

## Orientation audit

The eight uniform zone-pair orientations split into four classes up to global reversal.

- middle zone 11: overlap 2/11 on A_11; 10 modes altered; intersection dimension 316;
- middle zone 9: overlap 1/12 on A_9; 8 modes altered; intersection dimension 318;
- middle zone 13: overlap 1/10 on A_13; 12 modes altered; intersection dimension 314;
- cyclic orientation: all A_9,A_11,A_13 altered; 30 modes altered; intersection dimension 296=K_0.

Injectivity survives for all four classes because 9,11,13 are pairwise distinct.

K_0 and the fact U|K_0=I are orientation-class invariant.

## Semantic correction to A1

This is load-bearing.

The A1 unsigned operator

J_+ = B_+^T,
(J_+ xi)_ij = xi_i + xi_j

is zero-order in the continuum sense. Its natural interpretation is a discrete Weyl/conformal scaling generator:

delta h_ij ~ xi_i + xi_j.

Its adjoint B_+ is therefore trace-like, not the ordinary divergence of an oriented 1-current.

The A1 compensator identity is accordingly a finite Weyl/Stueckelberg Ward identity with a diagonal compensator.

The actual signed current divergence is B_-.

Therefore:

- A1 conservation language must not be promoted to a discrete Bianchi identity solely from B_+ G=0;
- U is a canonical linear carrier bridge from A1 traceless/signless-response data into a signed conserved-current carrier;
- U is NOT, by itself, a proof that Weyl-trace conservation and matter-current conservation are the same geometric law;
- "discrete diffeomorphism" is not established by this construction.

This correction strengthens the architecture by separating two operator types that were previously conflated.

## Remaining C-track residual

The old blocker "there is no shared carrier map" is substantially reduced.

The exact residual is now:

1. RHO OWNERSHIP / METRIC COMPATIBILITY.
   A1's variational universal property uses the rho-weighted edge pairing, while the canonical U above is selected by the Euclidean edge metric. The already-owned Perron profile would give the same polar sign, but A1 has not yet been typed to that profile.

   For zone-constant rho, the A_11 overlap sign is controlled by

   sign(13 rho_9 - 9 rho_13).

   It can flip and degenerates when

   13 rho_9 = 9 rho_13.

   Therefore the Euclidean polar U and the A1-weighted polar map are not automatically the same.

2. OPERATOR/SEMANTIC COUPLING.
   A typed theorem must state how the A1 response is converted by U into the signed Hodge current carrier and how source/action pairings transform.

3. MATTER-ONLY COMPLEMENT.
   The one-dimensional omega mode has no A1 preimage. The theory must either:
   - identify it as a genuine matter-only conserved mode;
   - constrain it away;
   - or couple it through additional structure.

4. TT/GRAVITY DYNAMICS.
   C1 supplies a carrier map, not a derivation of the existing TT wave operator or continuum Einstein dynamics.

## Metric residual sharpened by an existing owned Perron profile

The repository already owns a canonical normalized positive scene Perron profile in
D0.VNext2.ScenePerronTraceCanonicity:

rho_9  = 1/(sceneRho+9),
rho_11 = 1/(sceneRho+11),
rho_13 = 1/(sceneRho+13),

with sceneRho>0.

For this profile,

13 rho_9 - 9 rho_13
 = (4 sceneRho + 88) / ((sceneRho+9)(sceneRho+13))
 > 0.

Therefore, IF this owned Perron profile is the rho used by the A1 variational action,
the rho-weighted polar sign on A_11 agrees with the Euclidean C1 polar sign and the
explicit U above survives unchanged.

A second natural but currently certificate-level choice, rho_i=deg(i), gives
(rho_9,rho_11,rho_13)=(24,22,20) and likewise
13*24-9*20=132>0.

Do not collapse this conditional into an ownership claim. The exact remaining metric task is now:

> type the rho used in A1 and prove it is the owned Perron profile (or another internally forced profile satisfying 13 rho_9 > 9 rho_13).

Once that is done, the sign/degeneracy concern is discharged for the physical scene.

## Lean-ready theorem package

Suggested module:

D0.Geometry.SignlessSignedCommonCarrier

T1. General rank theorem for K(a,b,c):
rank B_+ = a+b+c and rank B_- = a+b+c-1.

T2. Double-centered common sector:
dim K_0=(a-1)(b-1)+(a-1)(c-1)+(b-1)(c-1), and K_0 lies in both kernels for every uniform zone-pair orientation.

T3. Transitive intersection:
for p->m->q,
dim(ker B_+ ∩ ker B_-)=dim K_0+(p-1)+(q-1).

T4. Projection singular values:
P_-|ker B_+ has singular values 1 and |p-q|/(p+q) with multiplicities stated by the sector decomposition.

T5. Explicit U:
for 9->11->13, the rank-10 row-centering correction above is an isometry ker B_+ -> ker B_-.

T6. Complement:
omega=(13,-11,9), B_-omega=0, B_+omega=(0,234,0), ||omega||^2=42471.

T7. H-equivariant uniqueness:
after fixing Euclidean metric, degree-order orientation, identity on the intersection and polar positivity, U is unique.

T8. Adjoint/projector:
U^*U=I and UU^*=I-omega omega^T/42471.

## Acceptance boundary

C1 may be promoted beyond FORMALISM only after the actual finite edge carrier, B_+, B_-, U and omega are typed in Lean and T1-T8 are proved.

D0-HODGE-LINKS-001 remains a PROOF-TARGET until the rho-metric compatibility and typed matter/gravity coupling theorem are settled.
