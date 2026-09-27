# A4D diagonal microstructure connection-stationary slow lift

**Task:** `WRK-A4D-DIAGONAL-MICROSTRUCTURE-CONNECTION-STATIONARY-SLOW-LIFT`
**Class:** `WORKER`
**Research lane:** `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
**Owners pinned:** #232 merge `caa1e65087ddf15cda35325189ebfcbf51a56592`; #241 merge `9f9a4da468f89eea4becd931f15c3814b009babd`. Normalization is the single final factor from #226. No discrete Levi-Civita comparison is computed.
**Certificate:** `02_REGISTRY/research/certificates/a4d_diagonal_microstructure_connection_stationary_slow_lift_check.py`

## 0. Terminal

\[
\boxed{\texttt{J2-DIAGONAL-MICROSTRUCTURE-CONNECTION-STATIONARY-RESPONSE-CANCELS}}
\]

The #232 microstructure admits an exact order-\(h\) connection-stationary lift on the #241 valued slow background. After that lift the pointwise metric partial has no order-\(h\) term. Its order-\(h^2\) jet is divisible by \(z\), so

\[
h^{-2}\Delta E_Q \to 0
\]

at both \(z_h=h\) and \(z_h=h^2\). This is connection stationarity only. It is not a same-source joint solution.

## 1. Reproduced inputs

The connection is the period-4 family of #232, \(Y=J_{12}-J_{13}+J_{23}\), role-0 links \((U,I,U^{-1},I)\). At standard solder every one of the \(4\times4\times6\) connection components vanishes. The Gram lift is \(H(q)=\tfrac12 q\eta\). On

\[
Q=\eta+h\alpha+h^2 x_0\beta,
\qquad
\alpha=E_{12}+E_{21},\quad
\beta=E_{01}+E_{10},
\]

the uncorrected order-\(h\) metric partial is the #241 vector. Its \((0,1)\) entry is \(-\sigma(p)\,hz/(4+3z^2)\), with \(\sigma=(+1,+1,-1,-1)\).

## 2. Order-\(h\) connection forcing

With links held at \(K(z)\) and solder \(\eta+h\alpha\), the connection Euler is zero at order \(h^0\). The order-\(h\) forcing is supported on two phases and two boosts:

\[
\begin{aligned}
E_K(\text{phase }1,\text{role }0,b_{01}) &= h\,\frac{2z}{3z^2+4},\\
E_K(\text{phase }1,\text{role }0,b_{02}) &= -h\,\frac{2z}{3z^2+4},\\
E_K(\text{phase }3,\text{role }0,b_{01}) &= -h\,\frac{2z}{3z^2+4},\\
E_K(\text{phase }3,\text{role }0,b_{02}) &= h\,\frac{2z}{3z^2+4}.
\end{aligned}
\]

All other phase/role/generator components are zero through order \(h\). The carrier for this bidegree is the \(96\)-dimensional space of phase-uniform link corrections, four phases times four roles times six Lorentz generators. Right multiplication is the tangent convention.

## 3. The lift

The forcing is solved by a correction only on the curved role-0 edges, phases \(0\) and \(2\):

\[
\begin{aligned}
\delta A_0 &= h\Bigl(-\frac{z(z+2)}{3z^2+4}J_{12}-\frac{2z^2}{3z^2+4}J_{23}\Bigr),\\
\delta A_2 &= h\Bigl(\frac{z(z+2)}{3z^2+4}J_{12}-\frac{2z^2}{3z^2+4}J_{13}\Bigr).
\end{aligned}
\]

The \(96\times4\) Jacobian of these modes carries the forcing, and the residual on all \(96\) equations is the zero vector in \(\mathbb Q(z)\). The lift is not obtained by discarding a phase average: every one of the \(96\) components is solved.

## 4. Corrected metric partial

Substitute the lift through the quadratic piece of the exponential, and keep the slow solder through \(h^2\). Every order-\(h\) metric component vanishes at every phase. The order-\(h^2\) jet is

\[
\begin{aligned}
\Delta E_Q[E_{01}] &= -\sigma(p)\,h^2\frac{z^2(z-2)}{2(3z^2+4)^2},\\
\Delta E_Q[E_{02}] &= \sigma(p)\,h^2\frac{z^2(z-2)}{2(3z^2+4)^2},
\end{aligned}
\]

together with slope entries \(\pm\sigma(p)\,h^2 x_0 z/(3z^2+4)\) on \((12,13,22,33)\). Both families are divisible by \(z\). Therefore

\[
h^{-2}\Delta E_Q\Big|_{z=h}\to 0,
\qquad
h^{-2}\Delta E_Q\Big|_{z=h^2}\to 0.
\]

The four-phase sum of each of these expressions is zero as well. The pointwise cancellation is stronger than that average: the order-\(h\) term is zero at each phase, not merely after summation.

At \(z=0\) the lift is zero and every connection component of the identity-link Euler vanishes through \(h^2\). The order-\(h^2\) connection remainder of the lifted family is therefore not a \(z\)-independent source of a normalized finite term at the two scalings.

## 5. Scope

\(E_K=0\) through the order that carried the #241 normalized obstruction. This is not an exact same-source joint solution, and it does not identify a continuum Einstein tensor. No new density, Holst term, torsion constraint, or selector is introduced.

## 6. Validation

Review baseline: `880c8284454b072219f470982963d8dc041957c9`.

```bash
python3 02_REGISTRY/research/certificates/a4d_diagonal_microstructure_connection_stationary_slow_lift_check.py
```
