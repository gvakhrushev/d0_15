# Independent review: retained code, true lifts and apparatus elimination

21 October 2026. Reviewer: clock_synthesis, independent of the
stationarity packet author. Existing #334 only. Scientific source input
f64d4c3389b507c7e7fb66ace9480ed6191c463d.

**Verdict: PASS with the finite-table wording clarification incorporated.**
No mathematical or physical-scope blocker remains in the reviewed packet.

## Frozen files reviewed

All four author files are in closure_stationarity.

| Artifact | SHA256 |
|---|---|
| RETAINED_CODE_LIFT_AND_APPARATUS_ELIMINATION.md | 792ee430b1fce22c132a3f7a9d5ec28b97ca0c4ba4f9ef2b1ac60f1e7c5fb698 |
| check_retained_code_lift.py | 0a078a9af6187bf29cb73f5f5f03cc97ee11fc83e32db4e701e506678044f2e2 |
| STATIONARITY_SOURCE_PINS.json | aacdc9459b64af1f0cea57caa435b1cb792eccb85e55649d558b19326e2562ea |
| RESULT.json | c0881a7b060e1e1661fbadc1f344820d2b64c194f61e0ce2d8d5be298ad03db7 |

Independent optimized receipt:
closure_book/STATE_LIFT_INDEPENDENT_RESULT.json,
SHA256 45627b6919f6b2066321f05f89e6378edb3868b2373445d0e284e1eab0198746.
It is byte-for-byte identical to the author's normal receipt at the
executed proof version
5fa698adace52918ac940d9ab7fba9bbaf14c19c5d6d7e6022015f75c88c1108.
The final prose-only revision and receipt provenance are recorded below.

The single independent replay was:

    python3 -O /workspace/scratch/07af0e1491e7/closure_stationarity/check_retained_code_lift.py
      --repo /workspace/scratch/07af0e1491e7/d0_15
      --output /workspace/scratch/07af0e1491e7/closure_book/STATE_LIFT_INDEPENDENT_RESULT.json

Result: **PASS 75 exact controls**, including nine historical source
pins. The checker extracts only specified primitive/entropy definitions
and a literal structural tape from the pinned writer source; it does not
execute that old checker. No original geometry, all42, root census,
factory or compiler suite was rerun.

## Mathematical review

### Actual code distance, including every late abort

The exact trace distance is \(a_{\rm pre}\), the probability of reaching
the deterministic code block, on the declared execution interface with
identical early output. It is not merely the final report readiness
\(\gamma\). The proof correctly uses positive operators on disjoint
retained code sectors, and includes all later abort work. It requires
no equality of their conditional quantum states or final report laws.

For an enlarged instruction controller, early records may already
differ. The proof correspondingly retains only the lower bound
\(D_{\rm tr}\ge a_{\rm pre}\), obtained from the actual u/b register
test or contractivity under partial trace. It does not claim the
controller was erased or that a new test was added to the priced word.
An initially orthogonal instruction tape can make the full distance
one, consistent with the theorem.

The checker independently builds complete two-row states using the
actual CNOT and Fredkin functions, checks their selected marginal
moments and disjoint full code supports, and includes a late abort in
the structural fixture. Its rational tape is explicitly a control
fixture; it is not represented as a recomputation of the Golden
factory probabilities.

### Finite catalogues and limiting full-state topology

I requested one prose qualification, now present in §2. A finite
table has a discrete domain and admits smooth interpolations. The
proved result is that no admitted smooth full-state interpolation
is supplied by that table. With a uniform positive readiness lower
bound, the trace-distance gap prevents two approaching field-node
sequences from converging to the same full state under faithful
common isometric embeddings.

That conclusion is valid by the triangle inequality and invariance
of trace distance under the stated embeddings. It is not a no-go
for every alternative encoding or physical topology. The proof
correctly keeps the mathematical moment extension separate from
a differentiable complete-state action.

The density argument for continuous field-only constraints is also
properly scoped: it concerns the constraints claimed to follow solely
from the literal common circuit rules for every catalogue. It does
not remove an independently derived controller-dependent constraint
or prove that all addressed words are alternatives within one fixed
complete autonomous initial state.

### Exact full-price inequality and implementation slack

With \(D=C(w_0)-C(w_1)>0\), \(U=P-C\), and
\(\Delta_0=P(w_0)-\inf_{Y(w)=y_0}P(w)\), feasibility gives

\[
 E(y_1)\le E(y_0)+\Delta_0-D+U(w_1)-U(w_0).
\]

Consequently a minimum at \(y_0\) requires
\(U(w_1)-U(w_0)\ge D-\Delta_0\). The sign, reference field,
and placement of the implementation slack are correct. No optimizer
at \(y_1\), differentiability at ties, or smooth envelope is required.
Both words must be admissible in the same full initial task, and
the root infimum must be finite, as stated.

The proof explicitly avoids assuming that an expensive common
catalogue is near the physical optimum. Cancellation of its common
counted baseline does not bound \(\Delta_0\). The checker verifies
an actual positive entropy gap of its retained-row fixture and the
hostile case in which omitting \(\Delta_0\) would yield a false
contradiction. The identity \(U=P-C\) does not authorize choosing U.

### True joint lifting and stable apparatus elimination

The Hessian pullback is correctly conditional on a genuinely admitted
smooth section and a full joint stationary point. The otherwise
present term \(DP[D^2\sigma]\) is explicitly retained before joint
stationarity. The field source alone does not test independent
preparation, reference or controller equations.

At a full minimum, restricting the positive second form yields
\(K[v,v]\ge-\gamma H[v,v]\). For the joint block
\(\bigl(\begin{smallmatrix}\gamma H+K&C\\C^*&A\end{smallmatrix}\bigr)\),
the stated \(A\ge0\) and \(\ker A\subseteq\ker C\) are exactly the
range conditions needed to minimize over apparatus. The reduced
form subtracts \(CA^\dagger C^*\); its nonnegative contraction
strengthens the required correction by
\(\|A^{\dagger/2}C^*v\|^2\). A mixed coupling to an apparatus kernel,
or a negative apparatus direction, precludes a full minimum.

These are correct tests of one full price. They do not manufacture a
new stabilizing term, assume a smooth realization of the current
discrete writer, or infer physical stability from a stationary saddle.

## Bounded integration review

I separately read §§4–7 of
02_REGISTRY/research/A4D_MOMENT_WRITER_NATIVE_SELECTION_TEST_2026_10_21.md,
at SHA256
316369e5eaea1b3423db2607759cdc3597db6ba51c1b8ae6a7c7c5b3af99733e.
Verdict on those paragraphs: **PASS**.

The draft now contains the blank-compression premise for the conditional
spectator commutant lemma, the correctly typed
\(W_{k,t}=V_tC_ki=(V_ti)c_k\), and the explicit admission/optimality
qualification in its route decision. The full rank-eight Golden
feedback spectrum remains separate from a selected prepared input;
the genuine factory-prefix CQ calculation is not promoted into an
unproved full-prefix Book factorization. The positive paired-epoch
clock lift is preserved at its own cut and heat hypotheses.

The updated main also states the finite-catalogue versus limiting
topology distinction and preserves implementation slack. No equality
of the full H+J+R is inferred from equal J. No original nonvacuum
solution is discarded, and no physical GR closure is claimed.

For the final original-Book conclusion, the precise scope is failure
to derive the application map for THIS writer, not a theorem that
every native law is underdetermined. Book03 §§03.3.0–03.3.0a specify
the memory-class weighted history sum, the exponential weight and
Cost-minus-distinguishability-gain action. They do not identify this
writer's full record with that scene/history/observer structure.
The explicit NativeHistoryActionResponse owner accepts the numerical
information and memory maps as arguments; the scene Perron owner
likewise states its input \(C_{uv}(y),I_v(y)\) and its physical-selection
boundary. Those scoped interfaces justify leaving this writer's actual
gain/heat/cut source uncomputed, without treating Info as a freely
selectable physical control.

No author source, repository file or frozen scientific packet was
modified by this review.

## Final proof-only clarification

After the optimized replay, §4 equation (7a) was corrected to sum over
all changed literal report copies:

\[
 D=\gamma\sum_{\lambda\ {\rm changed}}w_\lambda
       [h_\varphi(r_{1,\lambda})-h_\varphi(r_0)]>0.
\]

I read this final paragraph and accepted it. Positive weights and
\(0<r_0<r_{1,\lambda}<1/2\) give the stated strict sign separately
for each summand; no equality between changed report probabilities
is needed. The general finite-gap and apparatus theorems were already
stated in terms of the actual complete D and are unchanged.

The final proof hash and author receipt hash are the ones in the
table above. A direct JSON comparison with my executed receipt shows
that only the proof_sha256 metadata differs; the checker, source pins
and every control output are identical. My executed receipt is retained
without rewriting its provenance. No checker was rerun for this
analytically reviewed wording/formula generalization.
