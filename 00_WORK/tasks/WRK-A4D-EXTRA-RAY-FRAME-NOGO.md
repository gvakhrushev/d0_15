# WRK-A4D-EXTRA-RAY-FRAME-NOGO

## Class
WORKER

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## State
REVIEW

Do not start while another ordinary WORKER is active.

## Objective

Machine-check the finite-dimensional algebraic core of the E-RAYSEL continuum selector.

No manifold, continuum or Lovelock theorem is required.

## Preferred branch

`work/a4d-extra-ray-frame-nogo`

## Euclidean control

Work in (mathbb R^4) with
[
u=(1,1,1,1)^T,
\qquad
P=I-\frac14uu^T.
]

Define the rational Hadamard orthogonal matrix
[
H=
\frac12
\begin{pmatrix}
1&1&1&1\\
1&-1&1&-1\\
1&1&-1&-1\\
1&-1&-1&1
\end{pmatrix}.
]

Prove exactly:

- (H^TH=I);
- (H(u/2)=e_0);
- (HPH^T\ne P).

This is the finite algebraic witness that the (E_\perp) background projector is not determined by the Euclidean metric alone.

If cheap, also formalize one vector/polarization witness showing the projected principal degree-two data differ under the two projectors.

## Lorentz control

Avoid transcendental hyperbolic functions.

Use the exact rational boost in the (0)-(1) plane
[
B=
\begin{pmatrix}
5/3&4/3&0&0\\
4/3&5/3&0&0\\
0&0&1&0\\
0&0&0&1
\end{pmatrix}
]
with
[
\eta=\operatorname{diag}(1,-1,-1,-1).
]

Prove:

- (B^T\eta B=\eta);
- for (T=e_0), (T'=BT=(5/3,4/3,0,0));
- (\eta(T',T')=1);
- the spatial projectors
  [
  S_T=I-TT^\flat,
  \qquad
  S_{T'}=I-T'T'^\flat
  ]
  are unequal.

If cheap, use (k=dt) to prove its spatial projection is zero for (T) and nonzero for (T').

## Firewalls

Do not claim:

- local Diff naturality;
- a continuum manifold;
- the full E_perp/E_sp response theorem;
- Einstein uniqueness;
- Lorentz covariance of the finite D0 theory.

This worker owns only the exact finite-dimensional frame-dependence witnesses used by the research argument.

## Integration

Register as formal support for the E-RAYSEL research packet unless a literal claim row already matches.

Run target build, `lake build D0.All`, guards/generated views and no-sorry scan.

Move task to REVIEW and stop.
