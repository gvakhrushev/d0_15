# Worker Task A1 — formalize the compensator/Noether completion

Branch: research/l2-a1-compensator-noether-lean
Target module: D0.Gravity.A2CompensatorNoether

Research source:
- 02_REGISTRY/frontier/A1_COMPENSATOR_NOETHER_RESULT.md
- 04_CERTIFICATES/vp_a2_compensator_noether.py

Do not redo the conceptual search. The mechanism is fixed for this task.
Do not promote any claim beyond the literal theorem body.

## Mathematical data

For a finite undirected graph with edge carrier E, let

B : R^E -> R^V,     (B T)_i = sum_{e incident to i} T_e,
J = B^T,            (J phi)_{ij} = phi_i + phi_j,
W_e = 1/(rho_i rho_j), rho_i>0,
M = W h.

Raw action:

S_A2(h,rho) = 2 sum_e W_e h_e^2.

Extended compensator action:

w = h - (1/2) J eta,
S_ext(h,eta,rho) = 2 sum_e W_e w_e^2.

Reduced action:

S_phys(h,rho) = min_phi S_A2(h-J phi,rho).

Physical edge response:

G_phys = 4 W (h-J phi_*),

where phi_* solves

B W B^T phi_* = B W h.

## Carrier rule

Prefer an actual edge type derived from a SimpleGraph / incidence Finset, not Matrix V V with unused entries.
If existing D0 edge/cochain infrastructure makes this impractical, define one reusable finite-edge abstraction and
write an explicit specialization theorem to K(9,11,13).

Do not hide orientation/symmetry in comments. The edge carrier must make each undirected edge occur once.

## A1-T1 — row divergence is the shift adjoint

Required theorem shape:

theorem row_divergence_is_shift_adjoint
  (T : Edge -> R) (xi : V -> R) :
  sum_e T e * (xi (src e) + xi (dst e))
    = sum_v xi v * divRow T v

Requirements:
- arbitrary finite graph;
- no rho;
- exact finite sum theorem.

Negative control:
use a signed incidence operator in a separate example and show its adjoint gives the usual oriented divergence,
not the row-sum divergence. This prevents accidental operator conflation.

## A1-T2 — extended action and off-shell Noether identity

Define eta : V -> R and w_e=h_e-(eta_i+eta_j)/2.

Prove:
1. finite shift invariance:
   S_ext(h+J xi, eta+2 xi, rho)=S_ext(h,eta,rho);
2. edge derivative:
   dS_ext/dh_e = 4 W_e w_e;
3. diagonal derivative:
   2 dS_ext/deta_i = -4 sum_j W_ij w_ij;
4. off-shell identity:
   Tdiag_i + divRow(Tedge)_i = 0.

The derivative statements should be real derivative theorems or an exact polynomial directional-derivative theorem,
not comments attached to closed formulas.

Negative control:
define the post-hoc Laplacianized response and prove/compute that its mixed Hessian integrability condition is not
the derivative of S_ext.

Acceptance:
D0-A2-COMPENSATOR-NOETHER-RESEARCH-001 stays FORMALISM until this theorem exists.

## A1-T3 — positivity no-go

Prove:

theorem nonneg_divRow_zero_implies_edge_zero
  (h_nonneg : forall e, 0 <= T e)
  (h_div : forall v, divRow T v = 0) :
  forall e, T e = 0

State the exact assumptions needed for isolated vertices / edge membership.

Corollary:
a nonzero divRow-free response cannot be entrywise nonnegative.

Do not interpret this as negative energy density; it is only a componentwise edge-response theorem.

## A1-T4 — compensator elimination without invertibility assumption

Let K = B W B^T with W strictly positive diagonal.

Prove, in this order:

1. ker(K)=ker(B^T).
   Suggested proof:
   phi^T K phi = || W^(1/2) B^T phi ||^2.

2. range(K)=range(B).
   In finite dimension this follows from the kernel equality of adjoints / orthogonal complements.

3. Since B W h is in range(B), there exists phi with
   K phi = B W h.

4. If phi1 and phi2 solve the equation, then
   B^T phi1 = B^T phi2.

5. Therefore w=h-B^T phi is unique.

6. B W w = 0 and hence
   divRow(4 W w)=0.

Bipartite components are mandatory:
phi itself may be nonunique; do not assume K invertible.

Negative control:
C6 must exhibit nonunique phi but unique w.

## A1-T5 — reduced action and envelope theorem

Define projectedW(h,rho) as the unique w from T4, avoiding a noncanonical chosen phi if possible.

Define

S_phys = 2 sum_e W_e projectedW_e^2.

Prove:
1. gauge invariance under h -> h+J xi;
2. minimality:
   S_phys <= S_A2(h-J psi,rho) for all psi;
3. weighted orthogonality:
   for all delta with B delta=0,
   sum_e rho_i rho_j (G_raw-G_phys)_e delta_e = 0;
4. directional derivative / Frechet derivative:
   d S_phys / d h_e = G_phys(e).

The derivative result is load-bearing: it upgrades G_phys from a conserved projection to a genuine variational response.

Negative control:
show that the corresponding Euclidean orthogonality generally fails for inhomogeneous rho.

## A1-T6 — K(9,11,13) specialization

Use the actual scene edge type, not copied constants, to prove:

1. |E|=359;
2. rank(unsigned incidence B)=33;
3. dim ker B=326;
4. every zone-constant edge field is in range(B^T).

For 4, construct explicitly:
phi_1=(c12+c13-c23)/2,
phi_2=(c12+c23-c13)/2,
phi_3=(c13+c23-c12)/2.

Then prove:
for every zone-constant h and arbitrary positive zone-constant rho,
projectedW=0, S_phys=0, G_phys=0.

Add a negative control on a 4-partite graph:
a generic six-parameter zone-constant field is not necessarily in range(B^T).

## Claim/status integration

When T1-T5 are proved:
- create or upgrade a LEAN_PROVED owner for the generic compensator/Noether mechanism;
- keep the K specialization separate if T6 is not yet complete;
- do not close the full Einstein gate merely from conservation.

The full gravity target still additionally requires:
- common matter-gravity carrier (D0-HODGE-LINKS-001);
- source equation G_phys = kappa T on that carrier;
- weak-field and TT reductions;
- continuum GR limit.

## Required final report

Return:
- exact module path;
- theorem names;
- which of T1..T6 are complete;
- any changed normalization/factor relative to this task;
- negative controls;
- claim status changes;
- validate_repo.py result;
- generate_lean_views.py --check result;
- lake build D0.All result;
- certificate result.
