# A1 Result Review — compensator/Noether completion of the finite a2 response

Source research: external A1 memo v2 + exact-arithmetic verification supplied to the reviewer.
Status in this repository: RESEARCH-CERTIFIED / FORMALISM until the arbitrary-graph statements are formalized in Lean.

## Reviewer verdict

A positive mechanism exists.

For a finite undirected graph with edge variables h_e and positive vertex weights rho_i, write

S_A2(h,rho) = 2 * sum_{e={i,j}} h_e^2/(rho_i rho_j),
W_e = 1/(rho_i rho_j),
M_e = W_e h_e.

Let B be the unsigned incidence operator
(BT)_i = sum_{e incident to i} T_e,
and J = B^T, so (J phi)_{ij}=phi_i+phi_j.

Introduce a diagonal/Stueckelberg compensator eta_i and

w = h - (1/2) J eta.

Then

S_ext(h,eta,rho) = 2 * sum_e W_e w_e^2

is exactly invariant under

h -> h + J xi,
eta -> eta + 2 xi.

With the matrix pairing in which diagonal response components satisfy
T_ii = 2 dS_ext/d eta_i, the Euler response is

T_e  = 4 W_e w_e,
T_ii = -4 (B W w)_i,

hence the off-shell Noether identity

T_ii + (B T_edge)_i = 0

holds identically.

This is materially stronger than post-processing the raw a2 gradient into a Laplacian:
the diagonal component is an actual derivative, the mixed Hessian is symmetric, and the
action has a finite gauge invariance.

## Eliminating the compensator

Put phi = eta/2. The compensator Euler equation is

B W (h - B^T phi) = 0,

equivalently

(B W B^T) phi = B W h = B M.

Because W is positive diagonal,

range(B W B^T) = range(B),

so a solution always exists. Phi need not be unique on bipartite components, but

w = h - B^T phi

is unique because any ambiguity lies in ker(B^T).

Define

G_phys = 4 W w.

Then

B G_phys = 0.

The reduced action is

S_phys(h,rho) = min_phi S_A2(h - B^T phi, rho)
              = 2 * sum_e W_e w_e^2,

and the research derivation/certificate supports the envelope identity

d S_phys / d h_e = G_phys(e).

Thus the row-divergence-free response is produced by a variational gauge completion,
not imposed as an admissibility predicate.

## Projection interpretation

The minimizer w is the W-orthogonal projection of h onto

ker(B W),

while M_w = W w is the rho-weighted representative whose response lies in ker(B).

Equivalently, for every delta h with B delta h = 0,

< G_raw - G_phys, delta h >_rho = 0,

where

< A,C >_rho = sum_{e={i,j}} rho_i rho_j A_e C_e.

This pairing is load-bearing. The corresponding Euclidean projection is the distinct A' route
when rho is inhomogeneous; the two coincide when rho is constant.

## Structural consequences accepted by the reviewer

### 1. Nonnegative + row-divergence-free implies zero

If T_e >= 0 on every edge and B T = 0, then every incident nonnegative summand at every
vertex vanishes. Therefore every nonzero row-divergence-free edge response is sign-indefinite.

Consequently any D0 requirement that a nonzero gravitational response itself be entrywise
nonnegative is incompatible with this conservation law. Positivity, if needed, must belong to
the action/energy or another scalar, not to every response component.

### 2. Zone-constant K(9,11,13) is pure shift gauge

For three zones and zone-constant edge values c_12,c_13,c_23,

phi_1 = (c_12+c_13-c_23)/2,
phi_2 = (c_12+c_23-c_13)/2,
phi_3 = (c_13+c_23-c_12)/2

gives h_ij = phi_i + phi_j on every scene edge. Hence w=0, S_phys=0 and G_phys=0,
independently of zone-constant rho.

For K(9,11,13), the unsigned incidence has rank 33, so

dim ker(B) = 359 - 33 = 326.

Interpret this carefully: the surviving modes are vertex-resolved/non-zone-homogeneous edge
variations. The phrase "intra-zone modes" is potentially misleading because the complete
tripartite scene has no edges inside a zone.

This result is compatible with treating the frozen symmetric background as a flat/gauge
baseline and putting physical curvature in source-derived perturbations.

### 3. Local scale is not part of C' gauge

The h-variable compensator completion preserves global scale but not arbitrary inhomogeneous
local scale when eta != 0. This agrees with the current D0 tick discrimination, which found
only homogeneous tick rescaling to be gauge in the tested observable sense.

A C'' formulation in normalized variables g_ij=h_ij/sqrt(rho_i rho_j) can preserve both a
shift and local scale symmetry, but its natural conservation law is a sqrt(rho_i rho_j)-weighted
divergence, not the repository row-sum divergence. C'' therefore remains an alternate extension,
not the primary A1 closure candidate.

## Claims NOT accepted from the source memo as established

1. "C' is the unique mechanism in the entire A/B/C class."
   The memo compares the named routes and identifies C' as the preferred action-based mechanism,
   but it does not prove an exhaustive classification theorem over all possible constraints,
   compensators or action extensions.

2. The quartically corrected route B has only numerical evidence for a positive rho solution.
   It is not promoted to a theorem.

3. Exact-rational tests are evidence for finite instances, not substitutes for the arbitrary-graph
   Lean theorems below.

## Lean integration package

Suggested module:

D0.Gravity.A2CompensatorNoether

### A1-T1 — shift/divergence adjointness

Prove for the actual finite edge type:

sum_e T_e * (xi_i + xi_j) = sum_i xi_i * DivRow(T)_i.

This pins DivRow = J^* independently of the action.

### A1-T2 — extended action response and off-shell Noether identity

Define S_ext through w=h-(eta_i+eta_j)/2.
Prove the edge and diagonal derivatives and

T_ii + DivRow(T_edge)_i = 0.

Also prove finite shift invariance.

### A1-T3 — positivity no-go

If T_e >= 0 and DivRow T=0, prove T=0 on all scene edges.

### A1-T4 — compensator elimination

Define positive diagonal W and K=B W B^T.
Prove:

- range(K)=range(B);
- existence of phi solving K phi = B W h;
- uniqueness of w=h-B^T phi;
- B(W w)=0;
- hence DivRow(G_phys)=0.

Do not require invertibility of K; the theorem must include bipartite components.

### A1-T5 — reduced action / envelope / universal property

Define S_phys by the unique projected w (or quotient/minimizer construction).
Prove:

- shift invariance;
- G_phys is its edge derivative;
- weighted orthogonality/universal property against ker(B).

### A1-T6 — tripartite specialization

On the actual K(9,11,13) scene:

- prove rank(B)=33 or import an independently proved rank theorem;
- derive dim ker(B)=326;
- prove every zone-constant edge field is in range(B^T);
- conclude G_phys=0 for all zone-constant h and rho.

## Acceptance criterion for the Einstein track

This research result does NOT by itself close D0-SPECTRAL-EINSTEIN-001 or the full Einstein gate.

A1 is considered mathematically closed only after:

1. A1-T1 through A1-T5 are Lean theorems on an actual typed edge carrier;
2. the extended diagonal/Stueckelberg carrier is accepted as the physical/gauge completion rather
   than an arbitrary new field;
3. the resulting G_phys is connected to the common gravity/matter carrier in D0-HODGE-LINKS-001;
4. weak-field/TT reductions are derived from the same completed action.

Until then this result is the preferred positive successor mechanism and a precise implementation target.
