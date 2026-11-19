# Lorentz-covariant translation generators cannot have finite positive Hilbert norm

**Scoped theorem, 15 October 2026.** A linear map from four-dimensional
Minkowski translation data into any positive real Hilbert space, if its norm
is invariant under the repository's exact rational Lorentz boost and two
spatial quarter-turns, is identically zero. Unlike the fixed finite-carrier
trace argument, this statement applies to infinite-dimensional Hilbert spaces
as well.

## Exact statement

Write the image of the four coordinate directions as (A,B,C,D\in E), where
(E) is a real Hilbert space, and set

\[
P(t,x,y,z)=tA+xB+yC+zD.
\]

Assume \(\|P(\Lambda v)\|=\|P(v)\|\) for the owned boost

\[
B_{tx}=\frac13\begin{pmatrix}5&4\\4&5\end{pmatrix}
\]

and the spatial quarter-turns \((t,x,y,z)\mapsto(t,-y,x,z)\) and
\((t,x,y,z)\mapsto(t,z,y,-x)\). Lean proves

\[
A=B=C=D=0.
\]

The exact boost assumption also gives its inverse: apply it at
\((t,x)=(5/3,-4/3)\), which the boost sends to \((1,0)\). Comparing the
positive and negative boosted time vectors yields, with
\(a=\|A\|^2\), \(b=\|B\|^2\), and \(c=\langle A,B\rangle\),

\[
16a+40c+16b=0,\qquad 16a-40c+16b=0.
\]

Thus \(c=0\), \(a+b=0\), and positivity forces \(A=B=0\). The quarter-turns
then give \(C=D=0\). The Lean proof uses only standard logical axioms; the
companion exact checker verifies the rational boost, its inverse, the quarter
turns, and controls showing the boost and positivity assumptions do work.

## Hilbert–Schmidt consequence

Let a strongly continuous unitary representation of the affine Lorentz group
act on a Hilbert carrier, and suppose its translation generator map
\(v\mapsto P(v)\) is real-linear, differentiable, and satisfies exact
covariance

\[
U(D)P(v)U(D)^{-1}=P(Dv).
\]

If every \(P(v)\) is Hilbert–Schmidt, the real Hilbert space of
self-adjoint Hilbert–Schmidt operators, with inner product
\(\operatorname{Re}\operatorname{Tr}(XY)\), has positive norm
\(\|P(v)\|_{HS}\). Unitary conjugation preserves that norm, so the theorem
forces every generator to vanish. Therefore a nontrivial translation action
on an infinite carrier cannot have a finite Hilbert–Schmidt generator under
these hypotheses. Nontrivial infinite-dimensional affine representations
remain possible when their generators are unbounded or are not
Hilbert–Schmidt.

This is a conditional classification, not a claim that the D0 two-tick price
is a Hilbert–Schmidt norm. It does not construct or exclude the actual
cross-level D0 action, identify the native source with a generator norm, prove
stationarity, or derive gravity. It does sharpen the next physical test: derive
the two-tick price derivative on the constrained \((q,D,b,m)\) tangent and
determine whether the resulting translation generator is Hilbert–Schmidt. If
it is, a nonzero Lorentz-covariant response is impossible; if it is not, the
divergent or non-Hilbert–Schmidt part must be derived from the native history
operator rather than inserted as a new postulate.

The finite-stage result and its scope are recorded in
[`A4D_NATIVE_AFFINE_DIRECT_LIMIT_LEVELWISE_NO_GO.md`](A4D_NATIVE_AFFINE_DIRECT_LIMIT_LEVELWISE_NO_GO.md).
That theorem requires level preservation; the present Hilbert-norm theorem
does not. Both are narrower than a no-go for the whole D0 core. Positive GR,
the physical heat block, the native source and the original #310, #202 and
#317 terminals remain open.

## Verification

The Lean capsule
[`a4d_positive_hilbert_translation_generator_no_go.lean`](certificates/a4d_positive_hilbert_translation_generator_no_go.lean)
proves the positive-Hilbert-space statement without adding hypotheses about
the native carrier. Reproduce its exact receipt with:

```sh
python3 02_REGISTRY/research/certificates/a4d_positive_hilbert_translation_generator_no_go_check.py --runtime-check --write
python3 02_REGISTRY/research/certificates/a4d_positive_hilbert_translation_generator_no_go_check.py
```
