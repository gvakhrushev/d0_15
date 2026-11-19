# D0: a complete Golden sign verifier with an intrinsic stopping event

20 October 2026. Existing Draft #334, task `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, interface `native-programme-v1`, consuming `constitutive` / `native_sector`. Phase: native realization. **Conditional exact execution/source theorem, not compulsory G0 admission, global prospective optimality or GR closure.** Input snapshot: `6b5fdc323b2109e7955d55dcc6f209b76835f0f4`.

## 1. The missing substitution actually addressed

The preceding [finite-future Book law](A4D_PROSPECTIVE_BOOK_FINITE_FUTURE_LAW_Q8_VERIFICATION_2026_10_20.md) supplies a continuation law once the verification task and horizon are given. The existing one-sided Q8 test detects a negative relative central sign with probability `4p^3`, but its dark outcome cannot certify the positive sign. A prescribed number of repeats therefore either leaves an unresolved outcome or introduces a false-negative tolerance.

This note removes that imposed horizon and tolerance **for the specified central-sign verification task**. It composes two already-owned Golden comparisons with opposite reference signs. Their joint inconclusive operator is exactly a scalar identity on the entire unknown source, not merely a small error or a preserved marginal. Repetition therefore needs no independent copies or reset of the unknown source. The first conclusive label is an intrinsic zero-error stopping event.

Owned inputs, reused rather than re-proved:

- `D0.Representation.GoldenOrderInterferometer`: actual gate `[[a,-p],[p,a]]`, `a^2=p`, `p+p^2=1`, exact minus output `[p^3,-2ap]`, and `p^6+4p^3=1`. Blob `7b59090312c610e1e19f426d7ed8f4a982ebf296`.
- `D0.Representation.OrderMemoryControl`: `localIQ^2=relativeSignQ` and `relativeSign * mixer * relativeSign = mixer.transpose`. The opposite reference and inverse mixer have a forward-control representation; availability of those physical controls is still an admission premise. Blob `b7e7fb4bda7ad2d6d67ce911b042c6ac7b493cc4`.
- [Q8 327-triangle inverse](A4D_Q8_SPIN_SHEET_327_TRIANGLE_INVERSE_AND_960_COHERENCE_GATES_2026_10_20.md): 143+104+80 existing ABC triangle signs reconstruct the original graph-edge central sheet modulo vertex gauge. Its 327/960 topology is consumed, not recertified as a new rank result.
- The accepted future-memory kernel and the [prospective route](MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md#prospective-minimality-and-physical-execution) retain their original quantifiers. Existence of an available future test is not a theorem that every physical state must execute it immediately.

The construction concerns a supplied relative central involution. A raw noncentral Q8 or Lorentz holonomy does not automatically meet that input type. Comparing two lifts of the same SO connection needs an actually admitted reference/routing map, or a declared central-loop sector. No such map is obtained merely from the following algebra.

## 2. Two original comparisons, with every outcome retained

Let `Z=Z*`, `Z^2=I` be the supplied relative central sign on the source, and let `Pi_+=(I+Z)/2`, `Pi_-=(I-Z)/2`. These are notation for its two existing sectors, not a newly introduced physical field. A coherent quantum control of Z is an additional operational realization; for a fixed but unknown classical sheet `s=+1` or `-1`, the same formulas are simply the two original quaternion-arm experiments.

Use the literal original splitter

\[
G=\begin{pmatrix}a&-p\\p&a\end{pmatrix},\qquad
p=\varphi^{-1},\quad a^2=p,\quad p+p^2=1.
\]

Preparing the first probe port and applying `G* diag(I,tZ) G`, with reference `t=+1` or `-1`, gives the complete dark and bright Kraus operators

\[
D_t=pI+t p^2Z,\qquad B_t=ap(tZ-I).
\tag{1}
\]

They obey `D_t*D_t+B_t*B_t=I`. In particular

\[
\begin{array}{ll}
D_+=\Pi_++p^3\Pi_-,&B_+=-2ap\Pi_-,\\
D_-=p^3\Pi_++\Pi_-,&B_-=-2ap\Pi_+.
\end{array}
\tag{2}
\]

One round runs the positive-reference test. A bright result certifies the negative sign and stops. Only after dark does it run the negative-reference test. Its bright result certifies the positive sign. Two dark results retain their full chronological labels and request a repeat. Thus the actual complete round is

\[
\boxed{
K_{-}=B_+=-2ap\Pi_-,\quad
K_{+}=B_-D_+=-2ap\Pi_+,\quad
K_{?}=D_-D_+=p^3I.
}
\tag{3}
\]

No postselected normalization was used to obtain (3). The exact completeness relation is

\[
K_-^*K_-+K_+^*K_++K_?^*K_?
=4p^3(\Pi_-+\Pi_+)+p^6I=I.
\tag{4}
\]

The two terminal signs can never be wrong: `K_- Pi_+=0` and `K_+ Pi_-=0`. Neither orientation is one of M1's independent checking lines. They are two choices inside one comparator; causal independence and provenance of separate verification lines remain separate requirements.

### Full unknown memory and reference, not only its scalar probability

For any joint state `rho_AR`, including an arbitrary retained reference of dimension128,

\[
(K_?\otimes I_R)\rho_{AR}(K_?^*\otimes I_R)=p^6\rho_{AR}.
\tag{5}
\]

Consequently a normalized inconclusive branch preserves **the entire joint state** exactly. The dark probe is back in its known first-port state; its outcome remains in the archive. Reuse of that probe is not erasure of the retained record or cloning of the source. Fresh record capacity and all actually executed controls must still be paid.
The first dark branch by itself is not scalar. A constraint requiring fixed RIGHT in every intermediate conditional branch needs its own check; restoration after a complete round does not prove that stronger prefix condition.

On an actual definite central-sheet sector, the nonzero conclusive Kraus operator is also a scalar on the source. It preserves any supplied fixed-RIGHT preparation after normalization. For a general coherent or correlated mixture of sign sectors, success performs a real projective measurement and its conditional right marginal may change. The exact additional condition for retaining a preparation Gram `I128/128` in each successful branch is

\[
M^*\Pi_\sigma M=w_\sigma I_{128}/128.
\tag{6}
\]

This condition is not imposed for free. The checker includes both an exact-instrument failure test and a correlated full128 fixture in which successful postselection changes RIGHT, while the nonselective complete instrument preserves its marginal.

### A scoped shortest-round fact

One original sign query has only one conclusive sign; its dark operator has unequal singular values `1,p^3`. It cannot give both signs conclusively and have an undisturbing inconclusive branch. Two identical reference choices still have unequal dark singular values. Two opposite choices give (3). Therefore two comparisons are the shortest round **within this fixed one-sided Golden-query/reference palette** meeting those three conditions. This is not an optimum over all admitted D0 circuits or a proof of their fully paid minimal cost.

## 3. Stopping is determined by the record, not an error tolerance

Write

\[
q=4p^3=0.9442719099991588\ldots,\qquad
r=p^6=0.0557280900008412\ldots,\qquad q+r=1.
\]

The complete stopped words are `(DD)^(k-1) B_+` and `(DD)^(k-1) D_+ B_-`; their source operators are `p^(3(k-1)) K_-` and `p^(3(k-1)) K_+`. For `w_sigma=Tr(rho Pi_sigma)` their joint law is

\[
\boxed{\Pr(T=k,\sigma)=q r^{k-1}w_\sigma,\quad k\ge1.}
\tag{7}
\]

Thus `Pr(T>N)=r^N` is independent of the unknown sign and even of a coherent source preparation. The rule halts almost surely, with zero probability of a wrong conclusive label and

\[
\boxed{\mathbb E T=\frac1q=\frac12+\frac{\sqrt5}{4}
=1.0590169943749474\ldots.}
\tag{8}
\]

The stopping rule is the earliest unambiguous record in this execution. An all-dark prefix retains both sign possibilities with nonzero weight and, for an initially unresolved sign, cannot be a completed zero-error verdict. A bright record leaves exactly one possible sign. No chosen confidence `epsilon` or prescribed horizon `N` appears in this rule.

**Finite-resource boundary:** there is no finite worst-case halting time. At any finite cap N, all completed labels and the unresolved branch must be kept. Their exact normalization is

\[
\sum_{k=1}^{N}q r^{k-1}+r^N=1.
\tag{9}
\]

A capped run never needs to guess: it reports unresolved with probability `r^N`. The almost-sure execution is a finite-description controller with almost surely finite, but not uniformly bounded, runtime and archival demand. This is not a claim that a strictly bounded finite apparatus implements an exact infinite protocol. Its actual finite resource/refinement schedule remains physical input.

The preceding divergence of an unrestricted raw sum over all K913 path lengths is not contradicted. Here the allowed execution is a specified adaptive verification tree whose exact branch completeness follows from (4), not an unweighted sum over every scene walk and every duration. The tree is normalized without adding the earlier hypothetical 5.408-per-tick scalar work penalty. Costs of admitting and running this tree remain genuine.

## 4. The clock does not erase the sign source

Equation (7) factorizes the number of rounds from the actual sign. For fixed Golden p and any moving supplied state/projector family, the score of a completed record is

\[
D\log\Pr(T=k,\sigma)=D\log w_\sigma.
\tag{10}
\]

Therefore the complete classical record retains the full sign Fisher quadratic form, and at a finite cap N retains exactly the fraction `1-r^N`:

\[
\mathcal I_{\mathrm{stopped}}=\mathcal I_{\mathrm{sign}},\qquad
\mathcal I_{N}=(1-r^N)\mathcal I_{\mathrm{sign}}.
\tag{11}
\]

On a regular positive-probability chart, its entropy identity in the actual Golden logarithm is

\[
H_\varphi(T,\sigma)=H_\varphi(T)+H_\varphi(w),\qquad
H_\varphi(T)=\frac{-\log q-(r/q)\log r}{\log\varphi}
=0.47326178542457\ldots.
\tag{12}
\]

The first term has zero field derivative; the genuine sign source remains. Nothing identifies this classical record entropy with the entire physical Book03 Info. No C2 entropy assertion across zero-probability rank births is made.

There is also a direct source-transport statement at the channel level. Let `L_Z` be the resolved sign instrument with its classical sign register, and let `U` append an unresolved flag without changing the source. After summing only the retry-count register, while it remains retained elsewhere, the capped output channel is

\[
\mathcal C_N=(1-r^N)\mathcal L_Z+r^N\mathcal U.
\tag{13}
\]

The resolved and unresolved output subspaces are orthogonal. Hence its distance from the ideal resolved channel in diamond norm is exactly `2r^N`, including entangled reference inputs. For a differentiable family on the same identified Hilbert fibres, `D C_N=(1-r^N)D L_Z+r^N D U`; errors in controlled field derivatives inherit the same factor. This is a transfer of this signed readout, not the full 16+24+matter Euler source or raw216.

## 5. Actual queries and complete price still have their own source

The real invocation clock is not identical to the round count. A negative result stops at query `2T-1`; a positive result at `2T`. Thus

\[
\mathbb E[\tau\mid -]=2/q-1=1.118033988749895\ldots,
\qquad
\mathbb E[\tau\mid +]=2/q=2.118033988749895\ldots.
\tag{14}
\]

Reference flips, reverse-mixer synthesis, scene routing, archive writes and any detector/reset work are additional executed operations. They are not free or included by calling one round one tick.

Suppose a supplied admitted, time-homogeneous complete payment model charges Hermitian observables `C_0(y)` before the first query and `C_1(y)` before the second, including its actual control/preparation/clock/record work. It must not have already integrated in the same retry cost again. The complete expected payment of this execution is then fixed by its genuine recurrence:

\[
\Gamma=C_0+D_+^*C_1D_+,\qquad
\boxed{\mathbb E C=\frac{\operatorname{Tr}(\rho\Gamma)}q.}
\tag{15}
\]

The second charge is weighted by the real first-dark branch, not by an invented prior. Repetition of an inconclusive round contributes r times the same joint-state price. Differentiating retains all actual source terms:

\[
D\mathbb E C=\frac1q\operatorname{Tr}[(D\rho)\Gamma+\rho D\Gamma],
\quad
D\Gamma=DC_0+(DD_+^*)C_1D_++D_+^*(DC_1)D_++D_+^*C_1(DD_+).
\tag{16}
\]

For constant scalar full per-query prices `c_0,c_1`, (15) reduces to

\[
\mathbb E[C\mid -]=(c_0+r c_1)/q,\qquad
\mathbb E[C\mid +]=(c_0+c_1)/q.
\tag{17}
\]

Clock-dependent prices require their actual weighted series instead of this homogeneous recurrence. If full net Cost-Info of an extra post-verdict operation is strictly positive and no other task requires it, the existing prospective no-detour result excludes that redundant continuation. The primitive Cost floor alone does not prove positivity of net Cost-Info, nor global optimality of the chosen policy. This note derives no C_0/C_1 from an ActionProtocol floor.

## 6. Unknown full 327-bit sheet: a stopping algorithm, not a known-target test

Consume the owned actual K913 triangle basis: 143 triangles `(a0,b,c)`, 104 additional `(a,b0,c)`, and 80 additional `(a,b,c0)`. Assume their relative central comparisons and address controls are physically admitted on the same retained source. No changed edge or true sign needs to be known beforehand.

Run the stopped verifier for each independent basis sign and apply the existing three-pass inverse. For a coherent version assume the 327 syndrome involutions commute and are jointly realized by the actual source; for a fixed classical sheet the requirement is simply that the sheet stays fixed during its comparisons. Each incomplete round is scalar on the entire joint source. Consequently the retry counts are independent geometric variables even if the sign outcomes are correlated, and

\[
\boxed{\mathbb E T_{\mathrm{total}}=327/q
=346.2985571606078\ldots.}
\tag{18}
\]

This is a number of paired rounds, not a paid primitive-gate count. Their total cycle distribution is `Pr(T_total=n)=binom(n-1,326) q^327 r^(n-327)` for `n>=327`. The actual query count also depends on the number of negative outcomes through (14).

At cap N on each basis comparison, the probability that any basis bit remains unresolved is exactly `1-(1-r^N)^327`. With N=7 it is

\[
1-(1-p^{42})^{327}=5.45841741640033\cdot10^{-7}.
\tag{19}
\]

This number is a resource diagnostic, not a false-answer probability or a confidence level used to define the uncapped rule. An unresolved component remains labelled unresolved. The 960 further triangle constraints are existing consistency relations, not 960 new independent unknowns; an independent second-line verification has its own actual price.

## 7. What is and is not now supplied to the parent argument

**Supplied on the declared existing comparison interface:** both central signs have an exact conclusive output; the record itself decides when verification is complete; no externally chosen error threshold is needed; every failed round preserves unknown source and reference; all stopped labels have a complete normalized law; the actual sign source and query/payment clocks are explicit. This replaces the imposed-horizon and independent-source-reset hypotheses in the previous central-sign test application. It is supporting work for `constitutive`, not an accepted discharge of the whole obligation.

**Still required from the same physical G0/Book execution:** the actual controlled relative central comparison and reference flip; physical routing to the 327 native triangle inputs; an unresolved verification obligation that genuinely arises in the source state; the actual complete price/Info, permitted archive capacity and source evolution during the query. A conditional completion algorithm does not prove that verification must start in every state. If the sign is already known and no new verification is required, nothing here forbids idle.

The sign input is not automatically the SO/exterior CAR16 readout, and the two reference orientations do not establish the two independent witness lines. General successful conditioning does not automatically satisfy fixedRIGHT128, as (6) and the checker explicitly show. The new claim is neither a unique complete physical action, nor an all-field Einstein source, nor a nonempty joint GR refinement theorem. `GR_closed=false`; raw216, global physical prospective selection and native admission remain open.

The general repeat-after-recoverable-failure framework is established quantum-instrument methodology; see Paetznick and Svore, arXiv:1311.1074, and Guerreschi, arXiv:1808.02900. The specific result here is the exact composition of the existing D0 Golden/Q8 controls into the scalar failure `p^3 I`, with both signed outputs, complete reference behavior and the parent source/clock application. No claim of inventing repeat-until-success as a general technique is made.

## 8. Reproduction and evidence

Run `python3 02_REGISTRY/research/sources/d0_complementary_golden_stopping_2026-10-20/check_complementary_golden_stopping.py`. The script is standard-library-only and read-only by default; `--output /tmp/receipt.json` writes an explicit new receipt. Exact arithmetic is over `Q[a]/(a^4+a^2-1)`; it verifies the original gate, every entry of the eight-axis quaternion control, the complete instrument, zero-error support, scalar failure, finite leaf normalization and repeated-same-reference hostile control. The 128-column preparation/source and chronological-cost checks are labelled numerical controls. The native 359-edge fixture consumes the original triangle inverse and reconstructs all 1287 signs without a new rank census.

The checker was executed locally with Python 3.13.5 and passed; `py_compile` also passed. Exact input refs/blobs, checker SHA256 and numbers are recorded in `sources/d0_complementary_golden_stopping_2026-10-20/receipt.json`. This is an author replay, not independent scientific acceptance or a Lean formalization. No BOOK, claim, assembly goal, shared workflow or lifecycle is changed.
