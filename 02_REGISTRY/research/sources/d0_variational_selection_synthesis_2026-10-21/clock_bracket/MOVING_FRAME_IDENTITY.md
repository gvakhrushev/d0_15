# The missing coframe derivative cancels the shift-normal defect

21 October 2026. Bounded analytical addendum to existing PR #334.
Author: Book-binding review lane. This new derivation is separate from the
independent replay of the existing 66-check clock packet. It is an exact
conditional operator identity, not admission of a physical clock or shift.

## 1. Exact statement and sign

Work at a **constant flat spatial frame**, on smooth compactly supported
spinor half-densities with all16 CAR components retained. Let the Hermitian
matrices `alpha^i`, i=1,2,3, obey
`{alpha^i,alpha^j}=2 delta^ij I16`. Indices in this section use delta.
The fourth CAR mode and all its grades remain in the carrier. For a
variable Hermitian coefficient field define the formal continuation

    D_alpha = -i [alpha^j partial_j + (1/2) partial_j alpha^j],
    H_N(alpha) = {N,D_alpha}/2
               = -i [N alpha^j partial_j + (1/2)partial_j(N alpha^j)].

The derivative acts on the displayed coefficient in the last multiplication
term. This is a declared true-adjoint half-density continuation; principal
Clifford data alone do not prove that an actual curved native operator has
exactly these subprincipal terms. A further connection or matrix potential
would have its own variation.

For real smooth X and N put

    sigma_ij = partial_(i X_j)
             = (partial_i X_j+partial_j X_i)/2,
    S_X = (1/8)[alpha^i,alpha^j] partial_i X_j,
    K_X = X^i partial_i + (1/2)div X + S_X,
    delta_X alpha^j = -alpha^i sigma_ij.

At the constant flat base the full first-order operator identity is

    [K_X,H_N] - H_(X dot grad N)
       = delta_alpha H_N[delta_X alpha]
       = i [N alpha^i sigma_ij partial_j
                       +(1/2)alpha^i partial_j(N sigma_ij)].       (A)

Consequently the covariant comparison has the **minus** field derivative:

    [K_X,H_N] - delta_alpha H_N[delta_X alpha]
       = H_(X dot grad N).                                      (B)

Adding that derivative to the frozen-frame commutator would double its
strain defect. The convention and sign in (B) are part of the statement;
no canonical Poisson-bracket sign is being inferred from it.

Equation (A) includes the term without a derivative on the test spinor.
It is not merely equality of principal symbols. It holds for arbitrary
smooth X,N at this base, rather than only a dilation or a polynomial sample.
It does not assert the corresponding formula at a general variable frame
without its advective, connection and frame-lift variations.

## 2. Direct proof

Write `H_N=-i A_N` with
`A_N=N alpha^j partial_j+alpha^j N_j/2`. The Clifford relation gives

    [S_X,alpha^j]
       = (1/2)alpha^i(partial_i X_j-partial_j X_i).

The principal coefficient of `[K_X,A_N]-A_(X dot grad N)` is therefore

    -N alpha^i partial_i X_j + N[S_X,alpha^j]
       = -N alpha^i sigma_ij.

For the multiplication term, differentiating the half-density and spin
pieces, and subtracting `alpha^j partial_j(X dot grad N)/2`, gives

    -(1/2)alpha^i sigma_ij N_j
      -N[(1/2)alpha^i partial_i div X+alpha^j partial_j S_X].

The potentially third-grade Clifford part of `alpha^j partial_j S_X`
vanishes against the symmetric second derivatives. Exactly,

    alpha^j partial_j S_X
       = (1/4)alpha^i(Delta X_i-partial_i div X),
    (1/2)alpha^i partial_i div X+alpha^j partial_j S_X
       = (1/2)alpha^i partial_j sigma_ij.

Thus the multiplication coefficient is
`-alpha^i partial_j(N sigma_ij)/2`. Multiplying the complete commutator by
`-i` proves (A). Differentiating the definition of `H_N(alpha)` gives the
same two coefficients with `delta alpha^j=-alpha^i sigma_ij`.

Three simple controls expose the needed terms. For `X=x partial_x,N=1`,
the frozen residual and the field derivative both equal `i alpha^x partial_x`.
For `X=x^2 partial_x,N=1`, the residual is
`i(2x alpha^x partial_x+alpha^x)`: the last term is lost if the derivative
of the moving half-density coefficient is omitted. For a rigid rotation
`X=(-y,x,0)`, sigma=0, but the spin term is needed to cancel rotation of the
Clifford coefficients.

## 3. The tangent fits the existing paid moment chart

The original moment writer's actual coframe dictionary is

    D = eta_R (T E)^(-T),
    R = D^T eta_R T = E^(-1),
    DE[delta D] = -E(delta D^T eta_R T)E.                 (C)

Its sixteen means are `D_ar/B_D`. This is a local diffeomorphism on the
stated invertible, bounded chart, rather than a restriction to the primary
Brinkmann tangent. It already admits general small coframe changes.

Let B_X be the four-dimensional matrix which equals sigma on the chosen
spatial slice and has zero normal row/column in that slice basis. Use the
existing fixed REST/null change of basis when expressing it in the stored
coframe coordinates. The matrix identities below are independent of that
constant basis choice. Taking

    delta E = E B_X,
    delta R = -B_X R,
    delta D = -D B_X^T                                  (D)

satisfies (C) exactly. Once the spatial Clifford readout is formed from R,
its flat-base variation is precisely `delta alpha^j=-sigma_ji alpha^i`.
In particular `delta q^ij=-2 sigma_ij` there, as for the inverse metric
under a spatial coordinate change with its antisymmetric frame rotation
compensated. This identifies the requisite tangent; it does not identify a
new gate. The original density, scale and REST/null calibrations are retained.

For a finite table with `D,delta D,epsilon in Q(p)`, the two actual nodes
`D +/- epsilon delta D` lie in the same admitted moment chart for sufficiently
small epsilon. The writer prepares those moment nodes exactly from its paid
resources, with the complete common inventory, all failures, unused bank
rows, instruction choice and work retained. Their finite source differences
approximate the stated tangent. If the old boundary collar must stay fixed,
X and its relevant derivatives must vanish there. An arbitrary real smooth
table is not silently called an exactly finite `Q(p)` word, and the discrete
writer is not called differentiable.

The exact geometrical covariance calculation therefore has a passive
coordinate/frame realization, while its coframe tangent also has a real
paid **node-preparation** realization. The latter is stronger than merely
renaming a variable, but it is not a physical transformation of one already
prepared complete execution.

## 4. What still has no owned physical implementation

The moment source explicitly says that it prepares even observable moments,
not an executed raw-coframe Julia gate or the old unknown-input channel.
Its words generally differ in their real instruction ordering. The
all16/24/2 source and second-jet correspondence does not supply an actual
local normal clock, a shift of the complete initial apparatus, or their
two-forward-order comparison. No such implementation follows from (D).

There is a further concrete carrier distinction. The particular Clifford
spin lift in (A) is generally not the old grade-preserving exterior Lorentz
link tangent. For two distinct spatial modes,

    (1/4)[alpha^i,alpha^j]|vacuum>
       = -(1/2)c_i c_j|vacuum> != 0,

with the sign fixed by the displayed creator order. This produces a
two-particle component. In contrast, every `d Lambda(L)` annihilates the
scalar vacuum because `Lambda(M)` fixes that grade. Thus the six paid proper
link moments cannot simply be relabelled as an already executed `S_X`.
This is literal inequality of the generators, not absence of a suitable
lift. In fact, with `beta_i=c_i+a_i` and i different from j,

    c_i a_j-c_j a_i = (alpha_i alpha_j+beta_i beta_j)/2,
    [beta_i beta_j,alpha_k]=0.

Thus the exterior and Clifford lifts induce the same vector rotation,
while differing by a nonzero commuting internal term. The reviewed normal
clock commutator selects the alpha part; choosing the exterior lift requires
explicit treatment of that extra term and its field derivatives. A different
compensated lift or a paid gate construction may work, but neither is supplied
by (A). The checker verifies the unequal generators and their common vector
action on the actual full16 carrier. This is an interface distinction, not
an impossibility theorem for implementing spin transport.

The density source's exact half-density conjugation is likewise a transported
representation with its norm and endpoint factors. It does not erase the
price of changing the actual old-history probabilities or prove that such a
conjugation is a free native physical operation.

The smallest positive next physical test is to implement these particular
field and spin compensations together with two admitted forward normal
orders on the same complete state, retain every record, and verify their
actual source/price and smooth-sector remainder. Until then (B) removes one
algebraic defect of the frozen comparison. It does not establish the other
constraint brackets, a phase space, Ward identities, an HKT application,
the compulsory Book selection, or GR closure.

## 5. Narrow validation and source pins

`check_frame_compensation.py` checks the full matrix coefficients with
arbitrary symbolic X_i(x,y,z), N(x,y,z), including the zero-order term. It
also checks the three omission/sign controls, the spin/exterior distinction,
and the inverse-coframe matrix order at a nonscalar rational fixture with
all six symbolic spatial strains. The fixture validates the algebraic map;
its admission as a specific primary lattice configuration is not claimed.
It uses active checks under ordinary and optimized Python. With SymPy
available in the environment, run:

    python3 check_frame_compensation.py

The default source root is the sealed packet's sibling `inputs` directory,
which preserves the repository-relative paths below. An optional first
positional argument selects another frozen source root; the standalone
wrapper supplies this argument explicitly. No live repository is needed.

Source bytes consumed and verified by the checker:

| Source relative to repository root | SHA256 |
| --- | --- |
| `02_REGISTRY/research/sources/d0_native_preparation_closure_2026-10-21/inputs/native_input.py` | `1c501d5609dda3e14a3da95aad0c77ea04ef48bf94921793a403fb058a805fe9` |
| `02_REGISTRY/research/sources/d0_paid_moment_field_writer_2026-10-21/moments/EXACT_MOMENT_SOURCE_CONSTRUCTION.md` | `8c4c3cf03ebf637de6917776f13533d8b9f20cd0e8790025cf64a092915aef15` |
| `02_REGISTRY/research/sources/d0_paid_moment_field_writer_2026-10-21/code/PAID_CODE_AND_MOMENT_WRITER.md` | `e95f0486456c53cf0ce40023bab08ac744fd6189b397d29a8773446c168244a0` |
| `02_REGISTRY/research/A4D_DENSITY_DRESSED_CAR_EINSTEIN_METRIC_2026_10_18.md` | `a33e364caed023d74cc70cfdc38380581bbb4f47af96e1c23ad7d3490e9da169` |

`physical_field_transport_admission=false`; `physical_normal_clock_admission=false`;
`full_gravitational_constraint_algebra=false`; `GR_closed=false`.
