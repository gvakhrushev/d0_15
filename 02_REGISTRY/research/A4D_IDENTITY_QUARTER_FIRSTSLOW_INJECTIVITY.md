# Identity-quarter full center: exact first-slow injectivity

Task: EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, Draft PR #310.
Input head before this result: c2289d0f2a43f5c7fde8bc374bfa30ffe611eadb.
Action, Gram quotient and mixed phase placement are unchanged.
Status: exact frozen flat principal-symbol theorem; no task-level Einstein or response-universality terminal.

## 1. Question

The connection-only center analysis contains hyperbolic second-order envelope
forms, but the physical problem uses the stacked joint first variation. At
the flat identity connection and diagonal quarter character

\[
q=(i,i,i,i),
\]

let

\[
\mathcal J(z)=\binom{A(z)}{C(z)}\in\mathbb C^{34\times24},
\]

where A is the literal polarized connection Hessian and C is the correctly
placed ten-component Gram readout on a connection amplitude. The flat
calculation gives rank J(q)=20. Its four-complex-dimensional kernel is one
physical role-supported triangle line per role,

\[
\begin{aligned}
T_0&=(0,0,0,1,-1,1),\\
T_1&=(0,1,-1,0,0,1),\\
T_2&=(1,0,-1,0,1,0),\\
T_3&=(1,-1,0,1,0,0),
\end{aligned}
\]

in generator order (K1,K2,K3,J12,J13,J23).

The question is whether a real slow detuning of this whole kernel has a
characteristic direction after the 20 range variables are eliminated.

## 2. Exact range chart and reduced derivative

Use the 20 connection coordinates

    0,1,2,3,4,6,7,8,9,10,12,13,14,15,17,18,19,20,22,23

and joint output rows

    0,1,3,4,6,7,8,9,12,13,14,15,18,19,20,22,24,25,26,28.

The corresponding 20 x 20 submatrix of J(q) has exact determinant

\[
\boxed{4}.
\]

Thus it is an honest range chart. Let N be the 24 x 4 matrix whose columns
are the four role vectors above. For angular variables z_j=i exp(i t_j), let
J_j be the exact derivative at t=0. Solve in the range chart

\[
R W_j=-(J_jN)_{\rm range}
\]

and retain the 14 unselected rows:

\[
\Gamma_j=(J_jN+J(q)W_j)_{\rm red}\in\mathbb C^{14\times4}.
\]

The certificate reconstructs the literal action rather than importing a rank
table. Its four Gamma_j matrices have pinned SHA-256
c3cd199183c1c16c647f116090f56dc828f857bbc934f3031b23bd978756024d.

## 3. The theorem

For a real slow covector k=(k0,k1,k2,k3) put

\[
\Gamma(k)=\sum_{j=0}^3 k_j\Gamma_j.
\]

Then

\[
\boxed{
 k\in\mathbb R^4\setminus\{0\}
 \quad\Longrightarrow\quad
 \operatorname{rank}_{\mathbb C}\Gamma(k)=4.
}
\]

Consequently, by homogeneity and compactness of the real unit sphere, there is
c_*>0 such that

\[
\boxed{
 \sigma_{\min}(\Gamma(k))\ge c_*|k|
 \qquad(k\in\mathbb R^4).
}
\]

This is an injective first-order joint center symbol. The connection-only
hyperbolic quadratic forms therefore cannot be used as the complete leading
envelope equation of the fixed-metric joint problem.

## 4. Exact real-zero proof

Suppose Gamma(k) a=0, with a=(a0,a1,a2,a3) complex. Three reduced rows in
the first center column are

\[
\begin{aligned}
[(-1+i)k_0+(-1-i)k_1]a_0&=0,\\
[(1-i)k_0+(1+i)k_2]a_0&=0,\\
[(-1+i)k_0+(-1-i)k_3]a_0&=0.
\end{aligned}
\]

For real k, if a0 is nonzero, the first equation gives k0=k1=0, and the
other two then give k2=k3=0. Hence at nonzero k one has a0=0.

On rows 8 through 13 and the remaining three center columns, harmless nonzero
row rescalings give the exact 6 x 3 matrix

\[
M(k)=\begin{pmatrix}
 k_2-k_3&k_1-k_3&k_1-k_2\\
 -(1+i)k_0-2k_1+k_2-ik_3&-k_0+k_1&-ik_0+ik_1\\
 (1+i)k_0+2k_1-k_2+ik_3&-ik_0-k_1+(1+i)k_3&-k_0-ik_1+(1+i)k_2\\
 i(k_3-k_0)&i(k_0-k_3)&-i(k_1+k_2)-2k_3\\
 -k_2+k_3&k_0-k_1+2k_2+2ik_3&k_0-k_1+2ik_2+2k_3\\
 i(k_0-k_2)&-i(k_1+k_3)-2k_2&i(k_0-k_2)
\end{pmatrix}.
\]

If rank M<3, all twenty complex 3 x 3 minors vanish. Taking real and imaginary
parts gives forty rational cubic equations. Exact Groebner reduction yields,
among other consequences,

\[
(k_2-k_3)(k_2^2+k_2k_3+k_3^2)=0,
\]

\[
k_3(k_0^2+k_1^2+2k_1k_3)=0,
\qquad
k_3(k_0k_1-k_1k_2-k_1k_3+k_3^2)=0,
\]

and two cubic consequences which reduce to k0^3=0 and k1^3=0 when
k2=k3=0.

For real variables the first displayed equation forces k2=k3=t, because

\[
k_2^2+k_2k_3+k_3^2
=(k_2+k_3/2)^2+3k_3^2/4.
\]

If t=0, the cubic consequences force k0=k1=0. If t is nonzero, set
a=k0/t and b=k1/t. The next two equations become

\[
A=a^2+b^2+2b=0,
\qquad
B=ab-2b+1=0.
\]

Eliminating a gives

\[
\operatorname{Res}_a(A,B)
=b^4+2b^3+4b^2-4b+1.
\]

But exactly

\[
\boxed{
 b^4+2b^3+4b^2-4b+1
 =(b^2+b-\tfrac12)^2
 +4(b-\tfrac38)^2
 +\tfrac3{16}>0
}
\]

for every real b. Thus the common real zero of all minors is only k=0,
which proves the theorem.

## 5. Local spectral consequence

The full range block is invertible at the fold and the reduced matrix is

\[
F(t)=\Gamma(t)+O(|t|^2).
\]

Therefore, after shrinking a real angular neighborhood if needed, the literal
34 x 24 joint symbol has full column rank at every punctured point and its
center singular value is bounded below by c|t|. The diagonal-quarter zero is
thus isolated on the real physical torus even though the connection block
alone has a larger resonance.

The same statement persists on a sufficiently small compact family of frozen
constant coframes near the identity: the generic-coframe owner keeps the fold
kernel dimension four, all coefficients vary analytically with the coframe,
and the positive minimum on the real unit covector sphere is stable under a
small parameter perturbation.

## 6. What this changes in the closure architecture

The theorem separates two issues which were being conflated.

First, near the identity-quarter fold the full fixed-metric joint center has an
injective first-slow principal symbol. There is no free real characteristic
direction of the complete four-role center at this order.

Second, on a genuinely varying metric, mixed metric/coframe forcing enters the
reduced first-order equation. It can source the center and is not removed by
the present theorem. The theorem supplies the coercive principal part needed
for that variable-coefficient reduction.

In particular this result does not justify the invalid inference
O(h^2) raw response => o(h^2) after h^-2. The varying-coframe response
commutator and exact nonlinear stationary continuation still have to be
controlled.

It also does not prove the finite-amplitude Y H_TORUS premise. That is a
different symbol and remains a full-class/microstructure problem. For the
designated identity-approaching sheet, however, the correct resonant principal
object is now substantially sharper than a pair of free hyperbolic connection
envelopes.

## 7. Replay

    python3 02_REGISTRY/research/certificates/a4d_identity_quarter_firstslow_injectivity_check.py

The script uses exact rational/Gaussian-rational arithmetic for the finite
symbol and exact rational Groebner/resultant arithmetic for the real-zero
proof. No floating-point rank or sampled slow direction is used.

Scoped certificate terminal:

    A4D-IDENTITY-QUARTER-FULL-CENTER-FIRSTSLOW-INJECTIVE

PR #310 remains PARTIAL/OPEN; no task-level response or Einstein terminal is
promoted here.
