# E-FRAME — T4 Frame Erasure and Local Diff Naturality

CONTROL disposition: **ACCEPT AS RESEARCH / ATORUS-RESPONSE-RECONSTRUCTION-MISSING**  
Source memo: `MEMO_27_ATORUS_FRAME_ERASURE_LOCAL_DIFF_NATURALITY.md`

## First exact repository failure

The fixed-(T^4) Lovelock shortcut remains valid, but current D0 still lacks the typed maps needed to even compare two finite framed responses in one continuum tensor fibre.

The missing objects are, schematically,
[
S^{F}_{N,x}:
J_x^2\operatorname{Met}_{(1,3)}(T^4)
\to
\text{finite stencil data},
]
and especially
[
R^{F,resp}_{N,x}:
\operatorname{Sym}^2(Role)
\to
S^2T_x^*T^4.
]

Without these maps the frame-erasure difference
[
R_N^{F,resp}E_N[S_N^Fg;F_N]
-
R_N^{F',resp}E_N[S_N^{F'}g;F_N']
]
is not a typed repository expression.

Therefore the earliest current bridge failure is:
[
\boxed{\texttt{ATORUS-RESPONSE-RECONSTRUCTION-MISSING}}.
]

## Correct framed finite type

The honest finite response should be written
[
E_N[m;F_N],
]
where (F_N) records the local grid/frame realization of abstract Role directions.

At minimum (F_N) determines:

- local stencil positions in (T^4);
- the tangent directions represented by Role labels;
- the coframe that reconstructs finite components as a geometric tensor;
- the lattice scale (1/(N+2));
- comparison data between different local realizations.

## Minimal local construction

For a point (x\in T^4), an admissible local realization should carry a chart
[
\psi_F:B_\rho(0)\subset\mathbb R^4\to U\subset T^4,
\qquad \psi_F(0)=x,
]
a Role-labelled frame/coframe, and the local stencil
[
k\mapsto \psi_F(\varepsilon_N k),
\qquad \varepsilon_N=(N+2)^{-1}.
]

Sampling an arbitrary smooth Lorentz metric should be
[
S_{N,x}^{F}g(k)_{ab}
=
(\psi_F^*g)_{\varepsilon_N k}(\partial_a,\partial_b).
]

Pointwise response reconstruction should be
[
R_x^{F,resp}(T)
=
\sum_{a,b}
T_{ab}\,\theta_F^a\otimes\theta_F^b
\in S^2T_x^*T^4.
]

A global interpolation theorem is not required merely to state the local jet response.

## Exact frame-erasure condition

Two shrinking grid/frame realizations (F,F') of the same geometric metric 2-jet must satisfy
[
\lim_{N\to\infty}
\|\Phi_N(j;F_N)-\Phi_N(j;F'_N)\|
=0.
]

Equivalently, the continuum response must be constant on fibres of the forgetful map from framed/grid jets to ordinary metric jets.

## Pullback implication

If admissible local realizations are closed under pullback by local diffeomorphisms and the exact identities
[
S_N^{\phi^*F}(\phi^*g)=S_N^F(g),
]
[
R^{\phi^*F}(T)=\phi^*R^F(T)
]
hold, then frame erasure implies the literal fixed-(T^4) local-Diff naturality condition required by Navarro.

Thus the target is mathematically precise; the current problem is missing typed comparison ownership, not conceptual ambiguity.

## Divergence is a second independent bridge

The exact finite centered divergence
[
D^aE_{ab}=0
]
does not by itself imply
[
\nabla_g^aE_{ab}=0.
]

A separate theorem must intertwine a metric-dependent finite divergence with the Levi-Civita covariant divergence, or provide an equivalent normal-coordinate (C^1)-consistency theorem.

This gap is downstream of response reconstruction.

## Strong negative control

A framed continuum law
[
\widetilde E[g;F]
=
G[g]+\alpha R[g]q_F
]
may be fully covariant as a theory of ((g,F)) while failing metric-only descent. A local Lorentz boost changes (q_F) at fixed geometric metric jet.

The exact frame-erasure criterion therefore rejects background-grid theories as intended.

## Strategic consequence

The next positive implementation step is not another proposition-only bridge structure. It is an actual typed package for:

1. local (T^4) grid/frame realizations;
2. arbitrary Lorentz metric sampling;
3. pointwise response reconstruction;
4. exact pullback identities.

Only after those maps exist should D0 attempt the convergence/frame-erasure theorem itself.
