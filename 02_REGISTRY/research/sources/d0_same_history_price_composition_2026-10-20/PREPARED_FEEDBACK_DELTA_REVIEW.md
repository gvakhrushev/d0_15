# Independent delta review: original repeated-history isometry jets

Status: PASS, with the uniform-chart interpretation specified below.
Read-only analytical review of new section 4a by relational_history_bridge.
No repository edits, Lean builds, broad replay or numerical surrogate.

Source: `02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/prepared_price_feedback.md`
Reviewed source SHA256: `d7fb655bfb46aba05e05d67fabbe04a021073db9c177c375314591b5fc7ac54f`

The earlier sections were reviewed separately. This delta concerns only
the actual original one-round bounds, their composition, the counting
dimension and the normalized first-source limit.

## 1. One-round bounds independent of the number of sites

The stated assumptions are material: a fixed bounded C2 field chart with
uniformly bounded primitive jets, a strict contraction margin uniform over
h and sites, and bounded observer trivializations/inverses and their jets.
All norms and unit tangent directions use an h-uniform chart norm. The
ordinary field derivatives are taken at fixed discretization h and fixed
integer n; refinement h->0 is an external sequence. The assertion does not
by itself bound an unscaled derivative with respect to h or a moving
integer horizon.

For B=sqrt(M)>=sqrt(delta) I, the inverse Sylvester map has norm at most
1/(2sqrt(delta)), as seen from

    X = integral_0^infinity exp(-sB) Y exp(-sB) ds.

Therefore

    ||dB[u]|| <= ||dM[u]||/(2sqrt(delta)),
    ||d2B[u,v]||
      <= (||d2M[u,v]||+2||dB[u]||||dB[v]||)/(2sqrt(delta)).

These operator-norm bounds are independent of matrix dimension. They
apply to both Julia defects with the actual adjoints and observer jets.
A fixed finite word of uniformly bounded blocks, shifts and Walsh controls
then has uniformly bounded first and second jets. The scaled input hD/16
is a fixed finite combination of the original word blocks, so an artificial
unscaled D~h^-1 bound is not inserted. This argument applies to the stated
ORIGINAL fixed-size round, not automatically to a growing coframe-oracle
compiler or a new marker apparatus.

If kappa1,kappa2 bound each of the 128 Kraus-row jets, stacking them gives

    ||dV1||^2 <= sum_j ||dK_j||^2 <= 128 kappa1^2,
    ||d2V1||^2 <= sum_j ||d2K_j||^2 <= 128 kappa2^2.

Thus finite B1,B2 independent of the site count exist under the stated
chart assumptions. Completeness gives ||V1||=1 exactly.

## 2. Complete retained-history composition

Let S_j be the actual fresh-round isometry tensored with the identity on
all already retained records and oldRIGHT. Then ||S_j||=1, and the tensor
identities do not enlarge the derivative operator norm. The chronological
isometry is V_n=S_n ... S_1.

Its first derivative is the sum of n products containing one differentiated
round. Each product has norm at most B1, so ||dV_n||<=nB1.

Its mixed second derivative has n terms with a second derivative of one
round, and n(n-1) terms with two distinct differentiated rounds. The latter
count includes the u/v assignment in both chronological orders. Thus

    M1 <= n B1,
    M2 <= n B2+n(n-1)B1^2.

There is no factor 128^n. The complete output tape can have that many
labels while the intervening maps remain isometries. No histories are
quotiented, traced away as a physical operation or removed from the Q
complement by this estimate.

## 3. Counting dimension and the source scale

The determinant here acts on the prepared INPUT H. Its rank includes every
site, CAR16 grade and the fixed oldRIGHT multiplicity. Fresh history
registers belong to the output space of V_n and its actual complement;
they are not extra independent inputs at the prepared cut. Their effects
remain in L. This is distinct from the all-work cut, whose determinant was
proved isospectral and constant.

For a fixed-volume four-dimensional lattice with bounded grid geometry,
number of sites is O(h^-4), hence dim(H)=O(h^-4) with the stated fixed
reference multiplicity. If beta_minus <= n epsilon_h <= beta_plus with
beta_minus>0 and epsilon_h=(p^2/64)h^2, then h^-4=O(n^2).

At t=ln(phi), b=p^n and eta=1-sqrt(1-b)=b/(1+sqrt(1-b))<=b. For a FIXED
0<=z<1, the bracket in equation (7) is bounded independently of h,n.
Combining that equation with M1<=nB1 gives

    p^-n |d[-logdet(I-zF_in)+logdet(I-zG)]|
      <= O(dim(H) n p^n)
      = O(n^3 p^n) -> 0.

The z=0 case is trivial. If z were allowed to approach 1, its resolvent
constants would need separate uniform control; the source correctly
fixes z. A growing oldRIGHT multiplicity would likewise require inclusion
in dim(H), and is not covered by the fixed-reference statement.

For a moving normalized preparation, the PREPARED expectation correction
has the separate bound

    p^-n |d Tr(rho L)|
      <= (||d rho||_1+6nB1) p^n,

provided the actual trace-norm preparation jet is bounded. The counting
logdet and this prepared trace are distinct observables; no conversion
between them is used in the dimension estimate.

## 4. Admission and conclusion

The result bounds the original retained-history isometry and the two
mathematically specified test effects. It does not establish native
compilation or payment of the echo inverse, marker or its controls. The
mandatory n ticks remain paid. It does not select physical Info or prove
that a complete field action equals either test effect.

The error estimate is ABSOLUTE after the stated p^-n normalization. It does
not establish a nonzero Palatini source or a relative-error estimate
against a source that could itself vanish more rapidly. The source retains
those limitations explicitly.

No algebraic, dimension or physical-admission blocker was found. The
reviewed final snapshot explicitly states at the start of section 4a that
field jets are taken at fixed h,n in an h-uniform chart norm, while
refinement varies h externally. It also states the absolute-error scope.
These clarifications resolve the possible interpretation ambiguities;
no theorem repair is needed.
