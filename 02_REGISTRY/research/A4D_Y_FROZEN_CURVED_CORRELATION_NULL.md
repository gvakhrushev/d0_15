# Frozen curved coframes: the identity-sheet Y line has zero quadratic response

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
This is a direct analytic consequence of the
[exact moving-plane joint-vacuum theorem](A4D_Y_SLOW_JOINT_CONTINUATION.md)
and the primary memo's conditional shift-correlation law. It treats the
Y **line** in the identity-sheet diagonal-quarter kernel at arbitrary
constant coframes in its spacelike-plane chart. It does not classify the
other quarter-center directions or solve nonlinear gluing on a varying
metric.

## An exact family gives an exact quadratic zero

Let `S` be any constant nondegenerate coframe for which
`span{s2-s1,s3-s1}` is spacelike, and let `Q=S^T eta S`. The owned theorem
constructs a Lorentz bivector `B(S)` for this plane and temporal links

\[
K_0(p;t)=(U_S(t),I,U_S(t)^{-1},I)_p,
\qquad K_j=I\quad(j=1,2,3),
\]

with **all** unrestricted link Euler and all 16 coframe Euler rows zero
for every sufficiently small real `t`. Here `U_S` is the Cayley rotation
of `B(S)`. Since `B(S)^3=-k(S)B(S)` with `k(S)>0`, Cayley is locally the
same one-parameter subgroup as

\[
U_S(t)=\exp\!\left(
 \frac{2}{\sqrt{k(S)}}
 \arctan\frac{\sqrt{k(S)}t}{2}\;B(S)\right).
\]

The parameter in parentheses is analytic with derivative one at zero.
Reparametrize by it. In the right-exponential link chart the family is
then the **straight line** `a=s v_Y(S)`, where `v_Y(S)` has entries
`(+B(S),0,-B(S),0)` on the four temporal phases and zero on spatial
links. The Gram metric Euler is zero at every point of this line:

\[
E_Q(Q,\exp(sv_Y(S)))\equiv0.
\]

Twice differentiating at `s=0` gives the literal all-phase identity

\[
\boxed{D_a^2E_Q(Q,I)[v_Y(S),v_Y(S)]=0.} \tag{1}
\]

No acceleration term or range correction is omitted: the logarithmic
path is exactly straight. First differentiation also puts `v_Y(S)` in
the joint connection/metric kernel. This uses the owner's full Euler
identities at fixed `S`, not merely a variation restricted to the Y
ansatz.

The cosine pattern `(1,0,-1,0)` is the real part of the diagonal-quarter
character `(i,i,i,i)`. Phase translation gives the sine pattern
`(0,1,0,-1)`. At constant `Q`, the zero-character quadratic readout is
invariant under this quarter-turn of cosine/sine coefficients, so on
their real two-plane it has the form `c(a^2+b^2)` for each metric
component. Equation (1) makes `c=0`. Equivalently, for the complex
one-dimensional line `W_Y(Q)` spanned by the quarter polarization of
`B(S)`, the Hermitian frozen quadratic response operator obeys

\[
\boxed{D_QH_Q(i,i,i,i)[q]\big|_{W_Y(Q)}=0}
\]

as a sesquilinear form for every constant metric test `q`. This zero
holds for every `Q` in the stated coframe chart, not only for `eta`.
The [flat all-center corollary](A4D_IDENTITY_QUARTER_CORRELATION_NULL.md)
annihilates the whole four-complex-dimensional quarter kernel at `eta`;
the present curved-frozen theorem claims only its transported Y line.

## What it says about a smooth curved background

Let `g(x)` be fixed and smooth, with a coframe `S(x)` ranging over a
compact subset of the spacelike-plane chart. In the primary memo's
conditional small-link-log correlation law, the principal quadratic
defect uses the frozen symbol `D_QH_{g(x)}(z)` at each macroscopic point.
If a positive shift-correlation measure `mu_x(dz)` is supported only at
the diagonal-quarter conjugate pair and its range is contained in
`W_Y(g(x))` and its conjugate, equation (1) gives pointwise

\[
\operatorname{tr}\!left(D_QH_{g(x)}(z)[q(x)]\,d\mu_x(z)\right)=0.
\]

Therefore the **quadratic** homogenized defect integral vanishes for
such a measure on a genuinely varying smooth background. Under all the
primary law's additional hypotheses—`O(h)` link logs, weak-zero
rescaled deviations, sitewise bounded independently prescribed metric
source, and strong Euler residuals—the normalized response difference
converges to zero distributionally in this microlocal Y-line class.

This is not a realizability claim for that measure. It excludes neither
mixed/transverse center correlations, other Bloch support, finite-amplitude
Y microstructure, nor a contribution from spatial gradients beyond the
conditional law's controlled remainder. It does not give the unweighted
owner-sum `o(h^2)` estimate or the task's fixed-curved terminal. The exact
nonconstant-coframe lift in the owner is a separate existence control;
it is not a general joint-critical continuation over arbitrary `g(x)`.

Owner replay:

```sh
python3 02_REGISTRY/research/certificates/a4d_y_slow_exact_plane_check.py
```
