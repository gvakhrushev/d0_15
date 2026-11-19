# Independent review: retained report cut and prepared-input source

21 October 2026. Bounded review for existing Draft #334.
Reviewer: prep_synthesis. No author file or repository file was edited.

## Frozen bytes and one independent execution

Author packet: /workspace/scratch/07af0e1491e7/closure_book/.

| Input | SHA256 |
|---|---|
| RETAINED_CUT_AND_PREPARED_SOURCE.md | beade911fc9a51aa48cb26c2d4e74cc141c97afe96c54ce59e516d170734bc12 |
| check_retained_cut_source.py | cc760def4c6c6b125150c4af5c0d8002190a097e84b31aaec1bbdecff85f52a8 |
| SOURCE_PINS.json | 9f25b764734619ac47acaae3edf4370aedda76b4d48999ed710a5562e4657d25 |
| RESULT.json | cabe61b45ef6f13d0177737c31c9eb343407f5a5057c4e6db5cab1e91e979f3d |
| closure_stationarity/CUT_INDEPENDENT_RESULT.json | cabe61b45ef6f13d0177737c31c9eb343407f5a5057c4e6db5cab1e91e979f3d |

I read the full proof, checker and pin manifest, and checked the cited
Book01 cut/observer definitions, Book03 scene/Dirac/price definitions
and the historical normalization/range identity. I executed exactly once:

    python3 -O closure_book/check_retained_cut_source.py --repo /workspace/scratch/07af0e1491e7/d0_15 --output /workspace/scratch/07af0e1491e7/closure_stationarity/CUT_INDEPENDENT_RESULT.json

The optimized run passed all 61 bounded exact checks. Its output agrees
byte for byte with the frozen author result. The run verifies eight
historical pins at f64d4c3389b507c7e7fb66ace9480ed6191c463d and executes
no old project suite.

**Verdict: PASS at the stated cut, active-domain and price interfaces.
No blocking correction is needed.**

## 1. General operator statement

For a code unitary preserving the full active projection,
W_k=W c_k implies
N_k=c_k^*Nc_k and A_k=A c_k. Positive functional calculus gives
N_k^(-1/2)=c_k^*N^(-1/2)c_k, so the normalized complement is conjugated
by c_k. Its determinant and the range projector are exactly invariant.
This remains correct for nonscalar N and a common prescribed marked
map. No normalization derivative or input-column multiplicity is lost.

The separate prepared-state expression is an expectation of the
output effect in one specified input, and can change under c_k.
Using the unmarked physical map for Born probabilities is essential
and is explicitly required in the proof. A right-frame invariance of
the all-column determinant does not give prepared-probability invariance.

The spectator-covariance lemma is also correct: work-Z commutation
removes off-diagonal blocks, work-X commutation identifies the diagonal
blocks, and blank compression determines them. The initialized cut
fails X covariance. The proof does not assert that these covariances
follow from the original observer rule or that the relabelings are
free physical operations.

## 2. Actual all-column Golden block

The displayed Golden matrix obeys XGX=G^(-1). The fixed five-gate
downstream word therefore acts as G^3 when b=0 and as G when b=1.
With p^2=1-p its actual selected input probabilities are

\[
 r_0=(3p^2-p^3)^2=41-65p,\qquad r_1=p^2=1-p.
\]

The exact brackets 8/13<p<41/66 imply p<r_0<1 and p>1/2.
Binary entropy symmetry and strict decrease above one half give
h_phi(r_0)<h_phi(r_1). This is a strict algebraic/monotonicity
argument rather than a floating-point sign guess.

The declared projection has rank eight in the complete sixteen-dimensional
carrier. The uncoded effect has r_0 and r_1 each with multiplicity four.
Both full CNOT code maps preserve this projection. Thus the exact
determinant is [(1-z r_0)(1-z r_1)]^4 for both words, while their
selected input columns differ. The checker verifies every column and
both code permutations; it never reduces the source domain to that
one prepared column or imports an unrelated factor128.

## 3. Real paid preparation and its complete CQ ledger

The five-gate Golden parity prefix has the stated success component
ap(|011>+|111>) and readiness alpha=2p^3. Its failure is retained and
has no subsequent report. On success the actual two-CNOT code and
five-gate processor execute, keeping the known-one byproduct, u, b
and all quantum work.

The three-event law is exactly
(1-alpha, alpha(1-r_k), alpha r_k). Conditional work is pure, so its
entropy is h_phi(alpha)+alpha h_phi(r_k). With fixed per-address
charges, expected gate/read costs coincide: five common gates plus
seven success gates, and one common read plus one success read.
Consequently the complete counted-CQ contrast is the strict negative
alpha[h_phi(r_0)-h_phi(r_1)] stated in the proof. No successful-only
normalization or erased early branch is used.

**Important scope of this composition:** determinant equality is proved
on the complete sixteen-dimensional logical block and its declared
rank-eight report cut. The genuine paid prefix supplies a selected
input and the full six-qubit CQ law. These facts do not, together,
prove all-column determinant equality for the entire initialized
prefix map. The proof explicitly requires an additional invariant
range/factorization and cut identification for that extension.
This boundary must survive integration.

## 4. Book, heat and stationarity consumer

The historical Books fix the retained/archive projection and observer
query, and separately a scene representation, order memory and Dirac
operator. Their literal definitions do not identify those data with
an arbitrary endpoint Gram matrix. The proof correctly treats the
full circuit-to-scene mapping as an unproved input.

The primitive-memory observation is exact: a unitary that fixes the
ready input and commutes with both addressed A and B fixes both word
outputs individually. It cannot exchange their different code values.
An endpoint Gram equivalence alone therefore does not prove a gauge
equivalence of the primitive memory algebra or an intertwining of the
actual scene heat operator.

For the current stationarity application, a genuinely constant feedback
term cannot compensate a proved negative CQ word-price contrast.
The actual full-price correction still has to be calculated, including
the implementation-optimality gap if the constructed root word is
not itself a minimizing implementation. This packet neither sets that
gap to zero nor declares the conditional initialized/retained cut to
be compulsory Book03.

The conclusion is a precise operator/prepared-input distinction and a
genuine paid CQ diagnostic. It is not an identification of the full
moment-writer Book price, an autonomous same-controller code selector,
or a proof that the original full H+J+R is constant. GR closure remains
open at the exact stated interface.
