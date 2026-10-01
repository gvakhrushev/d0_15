# Identity-sheet rank-23 resonances are parabolic of order two

Task: EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, Draft PR #310.
Dependency: A4D_IDENTITY_QUARTER_FIRSTSLOW_INJECTIVITY.md.
No action change. No task-level response or Einstein terminal.

## 1. Representative point

Besides the two diagonal quarter points, the literal flat identity joint
symbol has the exact rank-23 point

\[
q=(1,1,i,i).
\]

The full stacked matrix J=(A;C) has rank 23 and one complex kernel line.
With generator coordinates grouped by role, a primitive kernel vector has
nonzero entries

\[
v_0=v_6=1,
\quad
v_{12}=-1, v_{14}=1, v_{16}=-1,
\quad
v_{18}=-1, v_{19}=1, v_{21}=-1.
\]

Deleting coordinate 0 gives a 23-dimensional range complement. The selected
23 output rows

    0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,26

have exact range determinant

\[
-16i(-1-i)\ne0.
\]

Thus the resonance has a literal analytic one-center Lyapunov-Schmidt chart.

## 2. First slow derivative

Eliminate the 23 range variables and differentiate in the four real angular
directions. The reduced first derivative is a real-linear map

\[
L:\mathbb R^4\longrightarrow\mathbb C^{11}.
\]

Exact arithmetic gives

\[
\operatorname{rank}_{\mathbb R}L=3,
\qquad
\ker L=\mathbb R(0,0,-1,1).
\]

So this point differs from the diagonal rank-20 quarter point: it has one
real characteristic detuning at first order.

A convenient reduced output component is original joint row 30. Its four
first derivatives are

\[
\left(-\frac{1+i}{2},-\frac{1+i}{2},0,0\right).
\]

Hence the real output covector

\[
\ell(w)=\operatorname{Im}w_{30}-\operatorname{Re}w_{30}
\]

annihilates the entire first-order image.

## 3. Exact second-order opening

Follow the physical characteristic path

\[
z_2=i e^{is},
\qquad
z_3=i e^{-is},
\qquad z_0=z_1=1.
\]

Equivalently write x=e^{is}, so z2=i x and z3=i/x. Keep the omitted center
coordinate normalized to one and solve the 23 range equations analytically.

The first reduced derivative vanishes exactly. For the x-parameter the
second derivative in output row 30 is

\[
F_{30,xx}(1)=-4+4i.
\]

Because x'(0)=i and the first derivative vanishes, the physical angular
second derivative is its negative. Therefore

\[
\boxed{
\ell(F_{ss}(0))=-8\ne0.
}
\]

This is the missing transverse second-order coefficient: the unique
first-order characteristic direction does not continue as a flat real
characteristic.

Standard finite-dimensional analytic reduction now gives local real
coordinates (y,s), where y is three-dimensional and transverse to the
characteristic line, and constants c,r>0 such that

\[
\boxed{
\|F(y,s)\|\ge c\bigl(|y|+|s|^2\bigr)
\qquad (|y|+|s|<r).
}
\]

The proof is the usual image/cokernel split. The first-order image controls
y. Projecting to ell kills that image and leaves a nonzero s^2 coefficient;
mixed and cubic terms are absorbed after shrinking r.

Thus, after restoring the uniformly invertible 23 range variables, the
literal joint symbol has at worst a quadratic small denominator near this
resonance.

## 4. The six copies

Spatial S3 symmetry gives the three choices for the pair of i-valued spatial
characters, and coefficient conjugation gives their -i copies. The
certificate also checks all six literal matrices directly:

\[
(1,i,i,1),\ (1,i,1,i),\ (1,1,i,i)
\]

and their complex conjugates. Every one has exact joint rank 23.

Therefore every currently observed non-diagonal identity-sheet physical
resonance has the same local parabolic order-two structure.

## 5. Consequence for the proposed range loss

This result is the first rigorous source for the previously speculative
bound p<=2.

It proves only the local statement:

* diagonal rank-20 quarter points: first-order joint opening, from the
  full-center theorem;
* six rank-23 points: three first-order transverse directions plus one
  second-order characteristic direction.

Hence, if the physical unit-torus singular set of the identity joint symbol
is exactly these eight points, a compact-complement gap plus these local
normal forms yields a global principal inverse loss no worse than h^-2.

That final implication is conditional because the continuous physical torus
has not yet been classified. Finite torsion scans are not a substitute for
that classification.

The remaining designated linear blocker is therefore sharpened to:

\[
\boxed{
\text{classify the real-unit-torus zero set of the identity joint symbol.}
}
\]

The finite-amplitude Y H_TORUS problem remains separate and is needed only
for the broader microstructure class.

## 6. Scope fence

This memo does not prove:

* that the eight observed points exhaust the continuous physical torus;
* a global owner-sum inverse;
* an exact nonlinear stationary correction on a varying metric;
* the varying-coframe metric-response commutator;
* response universality.

It does prove that no worse-than-quadratic local loss is hidden at the six
rank-23 identity resonances.

## 7. Replay

    python3 02_REGISTRY/research/certificates/a4d_identity_rank23_parabolic_resonance_check.py

Scoped terminal:

    A4D-IDENTITY-RANK23-RESONANCE-PARABOLIC-ORDER2
