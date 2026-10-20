# Independent prepared-feedback review

Status: PASS for the exact source snapshot below. Read-only review by
`relational_history_bridge`; no repository edits or Lean builds.

Source: `02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/prepared_price_feedback.md`
SHA256: `9100d15bb50daf22f6f6eceb9f35dcb399b475d40309716e7b6be08d5e0c0a4f`

## 1. Isometry, echo and exact cut

For a trace-preserving complete finite instrument, V*V=I. With the original
blank-apparatus inclusion i and V=Wi, the echo's top-left block on that input
is exactly A=i*W*sqrt(I-E)Wi=V*sqrt(I-E)V. It is Hermitian. Hence the genuine
complement Q=I-ii* on the active flag plus the entire other flag gives

    F_in=I-A*A=I-A^2.

Writing B=sqrt(I-E), use V*B^2V=I-G to obtain

    F_in-G=V*B(I-VV*)BV >= 0.

This includes the marker-zero output outside the prepared work subspace.
Neither an output branch nor its positive leakage effect is discarded.
The operator depends only on the actual isometry V, not the arbitrary
extension of W away from its prepared input. All untouched oldRIGHT input
states, including correlated preparations, remain allowed by tensoring
with identity. The original fresh blank-controller preparation remains a
real premise; this is not arbitrary active-work input admission.

For the full-work cut the effect is W*EW. Its spectrum and full counting
determinant are constant for a fixed marker E, exactly as claimed. A moving
input cut must move its inclusion isometry and retain that derivative.
The source correctly avoids applying the fixed-marker statement to the
paired circuit's moving relative interfering arms.

## 2. Native one-round factors

The original W_00=I-epsilon Delta/(2p^2), together with the complete sum over
64 labels, gives

    R=p^3(2I-W_00-W_00*)=p epsilon Delta.

At t=ln(phi), E takes p on cost1 and p^2 on cost2. Since p+p^2=1,
sqrt(1-p)=p and sqrt(1-p^2)=sqrt(p)=a. Therefore

    G=p(I-R)+p^2R=pI-p^3R,
    A=p(I-R)+aR=pI+(a-p)R,
    F_in=pI-2p(a-p)R-(a-p)^2R^2.

The identity p^3-2p(a-p)=(a-p)^2 gives
L=(a-p)^2(R-R^2), agreeing with the universal complement formula.
Every polynomial is an identity for an operator R, not a diagonalized
expectation. The derivative of R^2 is R dR+dR R; all displayed noncommuting
first-source expressions follow. On a scalar eigenmode, dL=(a-p)^2(1-2R)dR
is strictly positive for 0<R<1/2 and positive dR. A moving density adds its
actual Tr((d rho)L), as stated.

## 3. C1 and C2 bounds

Put D=sqrt(I-E)-I, eta=1-sqrt(1-b), C=V*DV and B0=V*D^2V.
D is fixed when t, the literal code and horizon are fixed. The isometry
normalization cancels the linear terms and gives L=B0-C^2. Since
0<=L<=B0<=eta^2 I, the claimed operator bound follows.

For unit tangent directions u,v the norm bounds are

    ||dB0|| <= 2 M1 eta^2,
    ||d2B0|| <= (2 M2+2 M1^2)eta^2,
    ||C|| <= eta,
    ||dC|| <= 2 M1 eta,
    ||d2C|| <= (2 M2+2 M1^2)eta.

Thus ||d(C^2)||<=4 M1 eta^2. Its mixed second derivative has the two terms
(d2C)C+C(d2C), bounded by (4M2+4M1^2)eta^2, and both cross-order products
(dC[u])(dC[v])+(dC[v])(dC[u]), bounded by 8M1^2 eta^2. Adding the B0 term
gives precisely

    ||dL|| <= 6 M1 eta^2,
    ||d2L|| <= (6 M2+14 M1^2)eta^2.

No commutativity of C or its derivatives is required. eta=O(b), so the
normalization statements are conditional on the actual stated growth of
isometry jets, counting dimension and preparation source. They are not a
uniform estimate for an unpriced compiler or a permission to drop the
baseline paid n.

## 4. Full logdet source bound

Both F=I-A^2 and G=V*EV satisfy 0<=F<=I and 0<=G<=bI. For fixed 0<=z<1,
write R_F=(I-zF)^(-1), R_G=(I-zG)^(-1). The exact difference is

    d[-logdet(I-zF)+logdet(I-zG)]
      =z Tr[R_F dL+(R_F-R_G)dG],
    R_F-R_G=z R_F L R_G.

Using ||R_F||,||R_G||<=1/(1-z), ||dG||<=2M1 b and
|Tr X|<=dim(H)||X|| yields exactly

    dim(H) eta^2 M1 [6z/(1-z)+2z^2 b/(1-z)^2].

The full counting dimension is retained. A field-varying z would need its
additional source, which the theorem explicitly excludes by fixing z.
The formula is not the prepared trace or the mean-cost generator.

## 5. Scientific scope

The source states all necessary remaining boundaries: physical compilation
and payment of W, W*, the marker and controls; original Info; actual
refinement/normalization; selected Einstein coefficient; and nonlinear
whole-action closure. It does not claim the mathematical marker is an
admitted free gate or that G equals the complete physical action. The
n=1 Golden probabilities do not automatically implement the long-history
marker. The positive complement and its source are kept at finite n.

No mathematical or scope blocker was found in the reviewed snapshot.
The universal derivative bounds were checked analytically; the companion
finite checker remains a separate validation, not a proof of those bounds.
