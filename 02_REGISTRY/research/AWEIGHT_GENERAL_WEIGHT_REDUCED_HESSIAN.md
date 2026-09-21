# A-WEIGHT-DYN — General-Weight A1 Reduced Hessian

CONTROL disposition: **ACCEPT AS RESEARCH / FOUR-FINITE-MODULI-PROVED**  
Research baseline: `78aa6686bccc142512937ab171e34d9d094b6e27`  
Source memo: `MEMO_17_AWEIGHT_GENERAL_WEIGHT_REDUCED_HESSIAN.md`

This packet is a durable research summary, not a Lean proof owner.

## Exact reduced operator

Let
[
B=B_+,qquad K_+=\ker B,
]
and let the positive H-invariant A1 edge metric be
[
W=xI_{9,11}\oplus yI_{9,13}\oplus zI_{11,13}.
]

For (h\in K_+), compensator minimisation gives
[
q_W(h)=\min_\phi 2\langle h-B^T\phi,,W(h-B^T\phi)\rangle.
]

Because (B) has rank 33 on the literal scene, (BWB^T) is positive definite. The unique minimiser is
[
\phi_W(h)=(BWB^T)^{-1}BWh.
]

Define
[
M_W=W-WB^T(BWB^T)^{-1}BW.
]
Then
[
q_W(h)=2h^TM_Wh
      =\frac12\langle h,A_Wh\rangle_{\rm Euc},
]
with exact Euclidean Riesz Hessian
[
\boxed{
A_W=
4\left[
W-WB^T(BWB^T)^{-1}BW
\right]\big|_{K_+}.
}
]

It is Euclidean self-adjoint, positive definite on (K_+), H-equivariant, and its image lies in (K_+).

## Six-sector decomposition and spectrum

Use
[
K_+
=
Z_{9,11}\oplus Z_{9,13}\oplus Z_{11,13}
\oplus A_9\oplus A_{11}\oplus A_{13},
]
with dimensions
[
80,96,120,8,10,12.
]

The exact A1 eigenvalues are
[
\boxed{
4x,quad4y,quad4z,quad
4\frac{24xy}{11x+13y},quad
4\frac{22xz}{9x+13z},quad
4\frac{20yz}{9y+11z}.
}
]

An exact 326-vector rational matrix check passed for
[
\rho=(1,1,1),quad(1,2,3),quad(2,3,5).
]

## Uniform locus

[
\boxed{
A_W=cI
\iff
x=y=z
\iff
r_9=r_{11}=r_{13}.
}
]

There is no positive nonuniform exceptional locus.

More strongly, within the positive weighted A1 family,
[
\boxed{
A_W\in\operatorname{span}\{I,Q_H,\varepsilon_{A_{11}}\}
\iff
x=y=z.
}
]

Thus general nonuniform compensator-reduced A1 contact dynamics lies outside the A-SEL intrinsic degree-1 locality class. This is not a contradiction because the weighted Schur complement depends on extra background data (W) and a global inverse.

## Projective coordinates and general finite spatial operator

Write
[
\rho=r_{11}(u,1,v),qquad \sigma=r_{11}^{-2}.
]
Then
[
x=\frac\sigma u,qquad
y=\frac\sigma{uv},qquad
z=\frac\sigma v.
]

Define
[
A_W=4\sigma D(u,v),
]
where the six shape eigenvalues are
[
\boxed{
\left(
\frac1u,
\frac1{uv},
\frac1v,
\frac{24}{u(11v+13)},
\frac{22}{9v+13u},
\frac{20}{v(9+11u)}
\right).
}
]

With
[
\mu=\frac{4\kappa_A\sigma}{\kappa_H},
]
the general spatial operator is
[
\boxed{
Q_{\rm gen}
=
\kappa_H[Q_H+\mu D(u,v)].
}
]

Its six normalized sector eigenvalues are
[
\boxed{
\begin{aligned}
L_{Z_{9,11}}&=13+\mu/u,\\
L_{Z_{9,13}}&=11+\mu/(uv),\\
L_{Z_{11,13}}&=9+\mu/v,\\
L_{A_9}&=24+24\mu/[u(11v+13)],\\
L_{A_{11}}&=22+22\mu/(9v+13u),\\
L_{A_{13}}&=20+20\mu/[v(9+11u)].
\end{aligned}
}
]

Only on
[
u=v=1
]
does (D=I), and only there may
[
\mu
]
be renamed
[
m^2.
]

## Exact finite modulus theorem

After quotienting:

- overall action scale;
- common (ho)-scale against (kappa_A);
- exact (Q\leftrightarrow\alpha) reciprocal scaling;
- canonical field-coordinate/symplectic conjugacies;
- discrete branch/time-orientation equivalences;

the active nonzero finite lane has exactly
[
\boxed{4}
]
observable continuous moduli:
[
\boxed{(\mu,\gamma,u,v)},
qquad
\gamma=\alpha\kappa_H.
]

The sector transfer traces are
[
\tau_s=3-\gamma L_s.
]

The four labelled traces
[
(\tau_{Z_{9,11}},\tau_{Z_{9,13}},\tau_{Z_{11,13}},\tau_{A_9})
]
have exact Jacobian determinant
[
\boxed{
-\frac{6864\gamma^3\mu^2}
{u^3v^2(11v+13)^2},
}
]
which is nonzero throughout
[
u,v>0,qquad \mu\gamma\ne0.
]

Therefore the four parameters are locally observable everywhere in the nondegenerate interior; this is not merely parameter bookkeeping.

## Stability / energy domain

For the oriented representative,
[
1<\gamma L_s(\mu,u,v)<5
]
for all six sectors.

Equivalently,
[
L_{\min}>0,qquad
L_{\max}<5L_{\min},qquad
\frac1{L_{\min}}<\gamma<\frac5{L_{\max}}.
]

This is an open region and does not select a point.

## Impact on previous research

A-NORM is exactly the codimension-two uniform subfamily
[
u=v=1.
]
On that locus
[
\mu=m^2.
]

Outside that locus the notation (m^2) is not a valid scalar general-weight contact shift.

The smallest positive selector target is now explicit:

1. force (u=v=1);
2. fix (mu);
3. if full finite closure is desired, fix (gamma).

No CORE upgrade of `D0-HODGE-LINKS-001` follows from this packet.

Primary verdict:
[
\boxed{\texttt{FOUR-FINITE-MODULI-PROVED}}.
]
