# D0 v15 — Continuum from Fractal Tick

## 1. Statement

D0 does not introduce continuum time as a primitive. Continuum time is the exponential envelope of a self-similar retained/archive trace ladder.

Let

\[
q=\varphi^{-1},
\qquad
\kappa=\log\varphi.
\]

The stable detector-clock tick is

\[
A_{n+1}=qA_n,
\qquad
B_{n+1}=B_n+(1-q)A_n.
\]

Since \(1-q=\varphi^{-2}\), each tick converts a constant fractal fraction of retained substrate into archive trace.

## 2. Constant logarithmic gradient

\[
\Delta\log A=\log A_{n+1}-\log A_n=-\log\varphi.
\]

The gradient is constant in logarithmic coordinates, not in absolute substrate amount.

## 3. Continuous semigroup envelope

The discrete tick is the integer sampling of

\[
\frac{dA}{ds}=-\kappa A,
\qquad
\frac{dB}{ds}=\kappa A.
\]

The solution is

\[
A(s)=A_0e^{-\kappa s},
\qquad
B(s)=B_0+A_0(1-e^{-\kappa s}).
\]

In matrix form, the flow generator is

\[
G_\varphi=
\begin{pmatrix}
-\log\varphi&0\\
\log\varphi&0
\end{pmatrix}.
\]

The continuum is therefore the semigroup envelope of infinite self-similar trace production.

## 4. Operator form

On a detector-clock subspace \(\Pi_\tau\),

\[
U_{\rm eff}(s)^\dagger U_{\rm eff}(s)=e^{-s\log\varphi}\Pi_\tau,
\]

and

\[
F(s)=(1-e^{-s\log\varphi})\Pi_\tau.
\]

At one tick, \(F(1)=\varphi^{-2}\Pi_\tau\).
