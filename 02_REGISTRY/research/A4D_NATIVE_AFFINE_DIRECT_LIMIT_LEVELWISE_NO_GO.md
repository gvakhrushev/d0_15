# A levelwise unitary affine action on the golden direct limit is trivial

**Scoped result, 15 October 2026.** The existing finite-carrier Lorentz theorem
has a direct consequence for the already-owned golden Hilbert tower. If an
affine-covariant unitary action preserves every finite level and commutes with
the isometric refinement inclusions, then its translation subgroup is the
identity on every level and therefore on the completed direct limit. A
nontrivial translation action on this tower must mix refinement levels.

This gives a sharp next test for the hidden heat block: a separate finite-level
operator or an inherited tensor extension cannot carry the required
translation-sensitive preparation. Any surviving route must derive
cross-level generator blocks from the existing history process and then derive
the complete heat/action variation from those same blocks. The result does
not prove that such a process exists in D0.

## Exact inputs

The finite theorem in
[`A4D_NATIVE_FINITE_AFFINE_UNITARY_NO_GO.md`](A4D_NATIVE_FINITE_AFFINE_UNITARY_NO_GO.md)
proves that every differentiable finite-dimensional unitary representation
of the affine Lorentz action on one fixed positive carrier is trivial on pure
translations. Its proof uses positivity of the matrix trace form and the
actual rational Lorentz boost; the exact checker passes 20 controls.

The golden response owner
[`A4D_NATIVE_HISTORY_RESPONSE_DESCENT.md`](A4D_NATIVE_HISTORY_RESPONSE_DESCENT.md)
constructs finite-dimensional Hilbert levels and isometric cylinder inclusions

\[
J e_w=a e_{wA}+p e_{wB},\qquad a^2+p^2=1,
\]

and proves operator naturality for the tensor extension \(A\otimes I\). It
does not construct the completed Hilbert direct limit or admit an affine
action on it. Forming the standard completion of the algebraic inductive limit
is mathematically available, with dense cylinder union by construction, but
that completion is not yet a repository-owned physical state space. The
physical transition/action owner is still missing.

## Direct-limit theorem

Let \(\mathcal H_0\subseteq\mathcal H_1\subseteq\cdots\) be finite-dimensional
positive Hilbert spaces with isometric inclusions, and let
\(\mathcal H_\infty=\overline{\bigcup_n\mathcal H_n}\). Suppose a strongly
continuous unitary representation of the affine Lorentz group acts on
\(\mathcal H_\infty\), and every \(\mathcal H_n\) is invariant under each
group element and its inverse. The finite-dimensional restrictions are
continuous, hence smooth, affine representations. The finite theorem gives

\[
U_n(I,b)=I_{\mathcal H_n}\quad\text{for every }n,b.
\]

Thus \(U(I,b)\) fixes the dense union. The compiled Lean lemma
`directLimit_translation_eq_id` proves that a continuous linear map fixed on
that union is the identity on the completion. Therefore

\[
U(I,b)=I_{\mathcal H_\infty}\quad\text{for every }b.
\]

The argument does not depend on the dimensions of the levels or on the number
of golden refinements. It uses their finiteness, positive pairing, exact
affine covariance at each level, and density of the cylinder union. When the
golden finite stages are completed in the standard way, density is built into
the completion; the existence of a physical affine action is an additional
open claim.

## What this cuts out and what remains

This rules out the following attempted construction: assign each finite
refinement level its own fixed-carrier unitary affine readout, make the maps
exactly natural under the owned inclusions, and expect their direct limit to
acquire a nonzero translation response. The direct limit cannot create the
response that is absent on every dense finite stage. Consequently a
level-diagonal heat completion cannot be the missing translation-sensitive
preparation in this class.

The required escape is precise. Some admitted translation generator must
have a nonzero component between refinement levels; equivalently, at least
one pure translation must send a vector in some finite \(\mathcal H_n\) outside
that level. This is compatible with an infinite history-dependent process,
but it is not supplied by the current tensor extension, by the 16-state CAR
return, or by the 718-state scene-history reversal. The existing finite
affine lift \(T_b\rho(D)\) is shift-sensitive and compositional, but its
translation matrices are nonunitary on a fixed positive pairing.

This conclusion is limited to affine-covariant unitary actions whose
restrictions preserve every finite level. It does not exclude a genuinely
level-mixing unitary on the completed carrier, a stateful channel with a
separately derived pairing, or another native process not captured by the
current interface. In particular it is not a proof that the whole D0 core
has no preparation map \(F\), and it is not a metric-source or Einstein
equation.

The next proof target is now one object: derive the cross-level affine
generator (or prove the actual admitted history process forbids one), bind
its action to the existing cylinder refinements, and compute the full
heat/feedback/matter covector on the true \((q,D,b,m)\) tangent. An arbitrary
complement block, the infinite-dimensional \(L^2(V^*)\) comparison model, or
a fitted cancellation does not meet that target.

## Verification

The Lean capsule
[`a4d_affine_direct_limit_levelwise_no_go.lean`](certificates/a4d_affine_direct_limit_levelwise_no_go.lean)
proves the generic dense-limit step with standard logical axioms. The exact
intake checks for the two consumed owners pass:

```sh
python3 02_REGISTRY/research/certificates/a4d_affine_direct_limit_levelwise_no_go_check.py
python3 02_REGISTRY/research/certificates/a4d_finite_lorentz_covariant_positive_quadratic_check.py
python3 02_REGISTRY/research/certificates/a4d_native_history_response_descent_check.py
```

The certificate checker replays the hash-pinned Lean transcript in the normal
portable path. To recompile locally and refresh the transcript and receipt,
refresh it with `--runtime-check --write`; `--runtime-check` without
`--write` compares a fresh local compile with the pinned transcript.

Their finite-level theorem and isometric-history claims remain separately
scoped. The physical action, its cross-level source, full price, native
stationarity, curved roots, soundness/recovery, GR, and the original #310,
#202 and #317 terminals remain open.
