# D0 — Informational Mechanics and Fractal Tick Principle

## 1. Scope

CVFT supplies feedback thermodynamics through the determinant and pressure law. Informational mechanics supplies the step-by-step law of trace production: how a retained state becomes archive trace while total substrate is conserved.

## 2. Trace fractions

For \(\psi\in P_N\mathcal H_N\), define

\[
\mu_N(\psi)=\frac{\langle\psi,F_N\psi\rangle}{\|\psi\|^2}
=\frac{\|Q_NU_NP_N\psi\|^2}{\|\psi\|^2},
\]

and

\[
\lambda_N(\psi)=\frac{\|P_NU_NP_N\psi\|^2}{\|\psi\|^2}.
\]

Unitarity gives

\[
\lambda_N(\psi)+\mu_N(\psi)=1.
\]

## 3. Fractal tick fixed point

Let \(p=\varphi^{-1}\). Since

\[
p+p^2=1,
\]

the detector-clock fixed point is

\[
\lambda_*=p=\varphi^{-1},
\qquad
\mu_*=p^2=\varphi^{-2}.
\]

On a declared detector-clock subspace \(\Pi_\tau\),

\[
\Pi_\tau F_N\Pi_\tau=\varphi^{-2}\Pi_\tau,
\]

and

\[
\Pi_\tau U_{\rm eff}^\dagger U_{\rm eff}\Pi_\tau=\varphi^{-1}\Pi_\tau,
\qquad
U_{\rm eff}=P_NU_NP_N.
\]

This is a fixed-point sector law, not a global identity for arbitrary \(U_N\).

## 4. Golden tick gate

The fixed point is realized by the active/archive splitter

\[
U_\varphi=
\begin{pmatrix}
\sqrt p\,I&-pI\\
pI&\sqrt p\,I
\end{pmatrix}.
\]

It is unitary because \(p+p^2=1\). For this gate,

\[
F_N=p^2P_N,
\qquad
U_{\rm eff}^\dagger U_{\rm eff}=pP_N.
\]

## 5. Trace recursion

Let \(A_t\) be retained substrate and \(B_t\) archive trace. The fractal tick obeys

\[
A_{t+1}=pA_t,
\qquad
B_{t+1}=B_t+p^2A_t.
\]

Thus \(A_{t+1}+B_{t+1}=A_t+B_t\). If \(B_0=0\), then

\[
A_t=p^tA_0,
\qquad
B_t=(1-p^t)A_0.
\]

The retained component never vanishes in finite time. Time is the ordered index induced by stable trace production.

## 6. Informational phases

- \(\mu=0\): coherent optical phase.
- \(\mu=\varphi^{-2}\): fractal clock phase.
- \(0<\mu<1\), \(\mu\ne\varphi^{-2}\): viscous matter phase.
- \(\mu\to1\): archive saturation phase.
- accumulated \(Q\)-trace: crystallized archive phase.
