# A4D Y slow joint continuation

**Task:** \`WRK-A4D-Y-SLOW-JOINT-CONTINUATION\`  
**Lifecycle:** BLOCKED  
**Research lane:** \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`

## 0. Partial terminal

\[
\boxed{\texttt{J2-Y-SLOW-PRIMARY-SCALING-RANGE-RESPONSE-REDUCES-TO-N0}}
\]

On the pinned #232 Y microstructure and the #241/#259 valued slow background, the next primary-scaling range correction exists and cancels the complete remaining order-\(h^3\) metric response at \(z=h\).

The full period-4 homogeneous connection freedom is not zero.  At the first order where that freedom matters it splits exactly into:

\[
16_{\mathbb R}
=
8_{\mathbb R}\text{ source-visible}
\;+\;
8_{\mathbb R}\text{ joint-invisible}.
\]

The \(8_{\mathbb R}\) joint-invisible space is exactly the cosine/sine realification of the owned diagonal quarter-wave

\[
N_0=\operatorname{span}_{\mathbb C}
\{\lambda_1,\lambda_3,\lambda_4,\lambda_6\}
\]

used by #260.

Therefore the explicit Y slow-background problem has been reduced to the already-owned diagonal invisible germ.  The remaining blocker is the nonlinear slow-background continuation of that \(N_0\) sector, whose constant-solder real rays are presently blocked in #260 on their degree-5 connection Euler.

No global response-decoupling terminal is claimed.

## 1. Inputs

This packet consumes only merged owners:

- #232: exact curved nongauge Y-family at flat metric;
- #241: raw valued-slow-background pointwise response;
- #259: exact order-\(h\) connection-stationary lift at fixed microstructure amplitude \(z\);
- #270: moving metric-null Hessian complex;
- #273: direct Schur identification \(K_{\rm Schur}=-\tfrac12K_{G^{(1)}}\).

The primary scaling is

\[
z_h=h.
\]

The distinction between the formal slow parameter \(h\) and the microstructure amplitude \(z\) is essential.  A term that is order \(h^2z\) at fixed \(z\) is order \(h^3\) on the primary scaling.

## 2. First unresolved connection forcing after #259

Re-expanding the literal all-edge connection Euler after the #259 correction gives exactly ten nonzero order-\(h^2\) coefficients at fixed \(z\).

With \(D=3z^2+4\), the phase-1, role-0 entries are

\[
\begin{aligned}
E_{K,K_1}^{(2)}&=\frac{z^2(z-2)}{D^2},\\
E_{K,K_2}^{(2)}&=-\frac{z^2(z-2)}{D^2},\\
E_{K,J_{12}}^{(2)}&=-\frac{2x_0z}{D},\\
E_{K,J_{13}}^{(2)}&=\frac{2x_0z}{D},\\
E_{K,J_{23}}^{(2)}&=\frac{4x_0z}{D},
\end{aligned}
\]

and phase 3 carries the exact negatives.  All other phase/role/generator entries vanish at this order.

At \(z=h\), the boost pair begins only at total order \(h^4\).  The leading unresolved forcing is the total order-\(h^3\) slope term.

## 3. Flat period-4 correction operator

Let \(L_0\) be the real period-4 connection Hessian at the identity connection and standard solder on the 96-dimensional carrier

\[
4\text{ phases}\times4\text{ roles}\times6\text{ Lorentz generators}.
\]

The certificate builds \(2L_0\) as an integer matrix directly from the star pairing and the literal link Euler variation.  It proves

\[
\boxed{\operatorname{rank}L_0=80},
\qquad
\boxed{\dim\ker L_0=16}.
\]

Thus the higher-order connection correction is not unique.  This is the real conjugate-paired diagonal quarter-wave resonance, not a numerical near-kernel.

## 4. Metric readout of the homogeneous freedom

Let \(M_0\) be the pointwise 40-component metric readout on the same real carrier:

\[
4\text{ phases}\times10\text{ Gram directions}.
\]

The exact stacked rank is

\[
\boxed{
\operatorname{rank}
\begin{pmatrix}
L_0\\M_0
\end{pmatrix}
=88.
}
\]

Therefore

\[
\dim(\ker L_0\cap\ker M_0)=8_{\mathbb R},
\]

while \(M_0\) has rank \(8\) on the 16-real-dimensional connection kernel.

Operationally:

- eight homogeneous connection directions are source-visible and cannot be freely added while preserving a fixed smooth metric source at the same normalized order;
- eight are joint-invisible at the linear level.

This is the precise place where connection stationarity alone stops and the metric/source equation starts selecting the sheet.

## 5. Exact identification with #260

The certificate inserts the four complex owned #260 vectors

\[
\begin{array}{c|c|c}
&\text{Role}&(K_1,K_2,K_3,J_{12},J_{13},J_{23})\\ \hline
\lambda_1&0&(0,0,0,1,-1,1)\\
\lambda_3&1&(0,1,-1,0,0,1)\\
\lambda_4&2&(1,0,-1,0,1,0)\\
\lambda_6&3&(1,-1,0,1,0,0)
\end{array}
\]

with cosine dressing \((1,0,-1,0)\) and sine dressing \((0,1,0,-1)\).

These eight real vectors are independent and obey

\[
L_0N_0^{\rm real}=0,
\qquad
M_0N_0^{\rm real}=0.
\]

Since the stacked nullity is exactly eight,

\[
\boxed{
\ker
\begin{pmatrix}
L_0\\M_0
\end{pmatrix}
=
N_0^{\rm real}.
}
\]

So the residual seam after the Y range correction is not a new FUGU sector and not a new letter.  It is exactly the already-owned diagonal source-invisible joint sector.

## 6. The next range correction exists

Factor \(x_0\) out.  On the primary scaling the total order-\(h^3\) forcing is solved by

\[
\boxed{
r_3=
\frac{x_0h^3}{2}
\left[
(K_2-K_3)_{\phi=0}
-
(K_2-K_3)_{\phi=2}
\right].
}
\]

The certificate checks this as an exact integer identity after clearing the common factor four:

\[
L_0r_3+f_3=0.
\]

Thus there is no Fredholm obstruction in the range channel at this order.

## 7. The complete \(h^3\) response cancels

The #259 corrected metric response has, at \(z=h\), a total order-\(h^3\) slope component on Gram entries

\[
(12,13,22,33)
\]

with phase signs \((+,+,-,-)\).

The metric response \(M_0r_3\) is exactly its negative on all four phases and all ten Gram components:

\[
\boxed{
E_Q^{(3)}\big|_{\#259}
+
M_0r_3
=0.
}
\]

Hence the canonical range continuation has no normalized order-\(h\) response:

\[
h^{-2}\Delta E_Q
=
O(h^2)
\]

through the orders controlled here.

This is stronger than the #259 statement \(O(h)\) for its first correction alone.

## 8. Why this is the useful bridge to the stationary-sheet theorem

The stationary-sheet synthesis in #240 says that response variation along a stationary sheet is the obstruction to transporting that sheet horizontally in metric space.

This calculation realizes that statement concretely:

1. the explicit slow forcing is in the range through the next primary-scaling order;
2. its range correction cancels the metric response;
3. the only remaining nonuniqueness is the true joint kernel \(N_0^{\rm real}\).

Thus the possible macroscopic response defect is localized to the nonlinear fate of the joint-invisible seam, not to the generic range variables.

The raw #241 \(-1/4\) pointwise limit was therefore not a stable anomaly.  It disappeared first under #259 stationarity and then again under the next exact range correction.

## 9. Remaining blocker

#260 has already followed the same \(N_0\) sector nonlinearly on the constant solder.  Its current exact state is:

- real cosine/sine rays are curved;
- scalar, connection Euler and metric Euler vanish through degree 4 after the zero-mode and character-\((-1)\) corrections;
- the first missing coefficient is the degree-5 connection Euler of those corrected real rays.

For the present slow-background problem one must additionally include cross terms between:

- the \(O(h)\) Y background microstructure,
- the \(O(h)\) slow Gram value,
- the range corrections above,
- and an \(O(h^2)\) homogeneous \(N_0^{\rm real}\) amplitude.

That nonlinear coupled map is not computed here.  Computing it independently in this PR would duplicate the scientific core of #260.  The next step must consume or coordinate with #260's degree-5 result rather than create a parallel germ convention.

This is the named blocker:

\[
\boxed{
\texttt{Y-SLOW-N0-NONLINEAR-CROSS-TERM-MISSING}.
}
\]

## 10. Boundary

This packet does not prove global response decoupling for arbitrary realizable correlation measures.  It proves a much narrower but constructive statement for the explicit #232 Y family and primary scaling \(z=h\).

No new action term, torsion constraint, selector, Fourier cutoff, finite diffeomorphism gauge, or continuum Einstein theorem is introduced.

## Validation

\`\`\`bash
python3 02_REGISTRY/research/certificates/a4d_y_slow_joint_continuation_check.py
\`\`\`
