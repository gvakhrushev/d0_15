# E-NJET — Normal-Jet Einstein Estimator Bridge

CONTROL disposition: **ACCEPT AS RESEARCH / NORMAL-JET-EINSTEIN-ESTIMATOR-REACHED**  
Source memo: `MEMO_30_ATORUS_NORMAL_JET_EINSTEIN_BRIDGE.md`

## Exact estimator theorem

Let (g) be any smooth Lorentz metric and (F) a (g)-orthonormal frame at (x).

Use the (g)-normal chart determined by (F), so
[
g_{ab}(x)=\eta_{ab},
\qquad
\partial_cg_{ab}(x)=0.
]

For the accepted centered-difference Lorentz ray
[
\begin{aligned}
(E_{\eta,N}h)_{ab}
={}&
\Box_Nh_{ab}
-D_av_b-D_bv_a
+D_aD_bt\\
&+\eta_{ab}q
-\eta_{ab}\Box_Nt,
\end{aligned}
]
with literal D0 centered differences and
[
\varepsilon_N=(N+2)^{-1},
]
the reconstructed local response satisfies
[
\boxed{
R_x^{F,resp}
(E_{\eta,N}[S_{N,x}^{g,F}g](0))
=
-2G[g](x)+O(\varepsilon_N^2)
}.
]

The coefficient is (c=-2) under the memo's explicit Ricci convention; reversing the Riemann/Ricci sign convention reverses this sign.

## Why this is the full Einstein tensor

At the normal-coordinate center:

- (g=\eta);
- all first metric derivatives vanish;
- Christoffel symbols vanish;
- every nonlinear term quadratic in first metric derivatives vanishes.

Therefore the full Einstein tensor at the center is exactly its second-metric-derivative expression.

No weak-field smallness assumption is used.

Metric second derivatives may be arbitrarily large.

## Literal stencil accuracy

For the actual D0 centered difference,
[
D_af(0)
=
\frac{f(\varepsilon e_a)-f(-\varepsilon e_a)}{2\varepsilon},
]
while the diagonal composition is
[
D_a^2f(0)
=
\frac{f(2\varepsilon e_a)-2f(0)+f(-2\varepsilon e_a)}
{4\varepsilon^2}.
]

Hence
[
D_a^2f
=
\partial_a^2f
+
\frac{\varepsilon^2}{3}\partial_a^4f
+
O(\varepsilon^4),
]
not the ordinary nearest-neighbour coefficient (\varepsilon^2/12).

The clean radius-two periodic no-alias guard is
[
N\ge3
\quad(L=N+2\ge5).
]

## Independent exact check

The coefficient identity
[
E_\eta=-2G
]
was checked on all 100 basis elements of
[
\operatorname{Sym}^2(\mathbb R^4)^*
\otimes
\operatorname{Sym}^2(\mathbb R^4)^*,
]
and independently derived analytically from the Levi-Civita/Ricci formulas.

The finite verification is corroboration; the proof is the analytic identity on arbitrary symmetric metric Hessians.

## Frame erasure

Two metric normal frames related by (O(1,3)) yield the same reconstructed geometric tensor in the limit.

The isotropic ray contracts only with (eta).

The extra spatial ray fails this test exactly as in E-RAYSEL.

## Epistemic boundary

This result is not circular with the Einstein **field equation**.

Imported external background:

- Levi-Civita connection;
- normal coordinates;
- curvature/Ricci/Einstein tensor definitions.

Not imported:

[
G+\Lambda g=\kappa T.
]

The theorem identifies the limit of an independently specified finite stencil with the geometric Einstein tensor.

However, this still does not prove that D0 CORE uniquely supplies:

- arbitrary smooth Lorentz metric inputs;
- metric-normal sampling;
- the Lorentz isotropic ray as physical finite dynamics;
- matter coupling;
- Newton normalization;
- cosmological term.

Thus it is a strong estimator/realization theorem, not closure of D0 physical gravity.

## Divergence routes

There are two distinct routes:

1. identify the limit as (G) and then use external contracted Bianchi;
2. derive covariant divergence from finite Noether using a third-difference / normal-frame intertwining theorem.

These routes must remain epistemically distinct.

The second route needs a radius-three stencil and clean guard
[
L\ge7.
]

## Cosmological term

The pure second-difference estimator annihilates constant metrics, so its own limit has no (b,g) term.

This does **not** derive physical (\Lambda=0): an independent zeroth-order sector may still exist.

Terminal result:
[
\boxed{\texttt{NORMAL-JET-EINSTEIN-ESTIMATOR-REACHED}}.
]
