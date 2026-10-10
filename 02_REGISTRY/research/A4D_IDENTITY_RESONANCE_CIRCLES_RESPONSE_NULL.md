# Flat physical resonance circles: exact quadratic response-null identity

Task: \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`, Draft PR #310.  
Depends on: \`A4D_IDENTITY_PHYSICAL_RESONANCE_CIRCLES.md\`.  
Certificate:
\`certificates/a4d_identity_resonance_circles_response_null_check.py\`.  
Status: exact quadratic source-image reduction; not a nonlinear task terminal.

## 1. Statement

At the identity solder, the physical joint symbol has the six already
certified resonance circles.  For spatial role \(r=1,2,3\), one of them is

\[
\lambda=(a,a,i,i)
\]

with the second \(a\) in role \(r\); the other three are their complex
conjugates.  Let \(v_r(a)\) be the exact polynomial kernel vector owned by the
circle theorem,

\[
v_r(a)=c_r+a\,\ell_r .
\]

For every nonzero \(a\) on the physical unit circle and every one of the ten
Gram directions \(q\),

\[
\boxed{
v_r(a)^\dagger\,D_Q A_{\eta}(\lambda)[q]\,v_r(a)=0.
}
\tag{1}
\]

By real Laurent coefficients the same identity holds on the three conjugate
circles with fixed \(-i\).

Thus every rank-one Hermitian quadratic correlation supported on any of the
six continuous flat physical resonance circles has **zero metric-response
defect**.

## 2. Coefficientwise proof

The literal connection symbol is assembled from one direct and one inverse
character factor.  Along \((a,a,i,i)\), its solder derivative has Laurent
support

\[
D_QA(a)=D_{-1}a^{-1}+D_0+D_{+1}a .
\tag{2}
\]

The physical involution on the unit circle sends \(a\mapsto a^{-1}\).
Therefore

\[
v_r(a)^\dagger
=
c_r^\dagger+a^{-1}\ell_r^\dagger .
\]

Substituting into (1) gives a Laurent polynomial supported only on powers
\(-2,-1,0,1,2\).

The checker does not sample a singular-value curve.  It reconstructs the
three coefficient matrices \(D_{-1},D_0,D_{+1}\) exactly from the literal
face brackets, convolves them with \(c_r,\ell_r\), and verifies every
coefficient of each of the ten resulting Laurent polynomials is exactly zero
over \(\mathbb Q(i)\).  It repeats this independently for \(r=1,2,3\).
The non-fourth-root unit point

\[
a=\frac{3+4i}{5}
\]

is retained as a held-out reconstruction/kernel control.

## 3. Relation to the old L=4 flat census

Sampling the six circles at fourth roots gives exactly twenty distinct
characters:

\[
\left|
\bigcup_{\text{six circles}}
\{\lambda:a\in\{1,i,-1,-i\}\}
\right|=20.
\tag{3}
\]

The earlier exact flat-solder L=4 census found precisely twenty singular
characters and zero response moments on every one of them.  Equation (1)
explains that finite result as samples of one continuous response-null
identity; it is not twenty unrelated cancellations.

This does **not** prove that the six circles exhaust the full physical unit
torus zero locus.  No such classification is used in (1).

## 4. Source-image consequence

For a real \(O(h)\) oscillatory field, a smooth \(O(h^2)\) source receives its
quadratic zero-character contribution from a mode paired with its conjugate.
If the associated defect measure is supported on the six physical resonance
circles, (1) gives

\[
\boxed{\mathcal T_\mu=0.}
\tag{4}
\]

This is exactly the source-image statement needed by
\`A4D_SOURCE_IMAGE_COLLAPSE.md\`: an arbitrary mixture, distribution, or
envelope of these circle polarizations cannot enlarge the quadratic smooth
source image merely by redistributing mass along the circles.

Cross-correlations between distinct characters occur at nonzero output
character unless their product is one.  A prescribed smooth source forces
those fast output rows through the joint equations; they are realizability
constraints, not additional zero-character stress channels.

## 5. What remains

The old pointwise frozen null-form criterion is false at general nonorthogonal
constant solders, so (1) is intentionally scoped to the identity/flat frozen
coframe.  On a slowly varying curved background, the remaining issue is
whether the exact shared-link equations transport these response-null circle
correlations without generating a nonzero order-\(h^2\) source moment, or
instead obstruct their realization.

In the finite-current language this is no longer an unbounded frequency
problem.  It belongs to the same finite degree-2/3/4 correlation system as
all other microstructure.

Verdict:

\[
\boxed{
\texttt{A4D-IDENTITY-PHYSICAL-RESONANCE-CIRCLES-QUADRATIC-RESPONSE-NULL}
}
\]

No torus census, nonlinear branch existence, varying-coframe transfer,
connection uniqueness, new selector, action change or task-level terminal is
claimed.

## 6. Replay

\`\`\`sh
python3 02_REGISTRY/research/certificates/a4d_identity_resonance_circles_response_null_check.py
\`\`\`
