# Curved Y joint symbol: an explicit zero-free folded neighborhood

Status: exact local research theorem. Task:
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
No global torus or physical-response terminal follows from this statement.

Let `Q(theta)` be the literal curved `z=1` full joint Bloch symbol of size
`136 x 96`, with `lambda_j=exp(i theta_j)`. For any of the four diagonal
folded characters `lambda_j=zeta`, `zeta^4=1`, choose a local real lift of
the angles and put

\[
\delta=\sum_{j=0}^3|\theta_j-\theta_j^*|,
\qquad r=10^{-8}.
\]

The exact conclusion is

\[
\boxed{0<\delta\le r\quad\Longrightarrow\quad
  \sigma_{\min}Q(\theta)>\frac{\delta}{20150}>0.}
\]

Thus each folded zero has an explicit zero-free punctured neighborhood.
The small constant is a conservative rational norm bound, not an estimate
of the true spectral scale.

## Proof from the owned chart

The folded-isolation owner selects 95 output rows and four residual rows,
then deletes the phase-0 `J12` Y coordinate. Write this selected 99-row
submatrix of the symbol as

\[
\begin{pmatrix}S(\theta)&q(\theta)\\
                B(\theta)&b(\theta)
\end{pmatrix},
\quad S\in\mathbb C^{95\times95},\quad
 B\in\mathbb C^{4\times95},
\]

where the second block consists of the owner's four reduced-residual rows.
Set `x(theta)=-S(theta)^{-1}q(theta)` and
`F(theta)=B(theta)x(theta)+b(theta)`. The owner gives
`||S(0)^{-1}||_2<40`, `F(0)=0`, and the inverse norm of the
four-by-four angular derivative `J_0=D F(0)` is `<5`. Its normalized
physical Y vector has six entries `+/-1`; the deleted entry is `1`, so
`||x(0)||_2=sqrt(5)<3`. The four residual rows at the center have exact
squared Frobenius norm `340/49<9`.

The exact Laurent support has every coordinate exponent in `{-1,0,1}`.
The owned entrywise derivative envelope bounds each `||partial_j Q||_2`
by `22/7<4` on the unit torus. Since `|d_j d_k|<=|d_k|` for every Laurent
monomial, the same envelope bounds each mixed second derivative by `4`.
For `delta<=r`, Neumann's lemma and the graph derivative identities give

\[
\begin{aligned}
 \|S(\theta)^{-1}\|&<50, & \|x(\theta)-x(0)\|&<800\delta,
   &\|x(\theta)\|&<4,\\
 \|\partial_k x(0)\|&<640,
   &\|\partial_k x(\theta)-\partial_k x(0)\|&<288800\delta.
\end{aligned}
\]

Indeed, `||S(theta)^{-1}-S(0)^{-1}||<8000 delta`; the derivative
difference of `q_k+S_k x` is at most `3216 delta`. Applying the product
rule to `F=Bx+b`, using `||(B,b)(0)||<3` and
`||(B,b)(theta)||<4`, yields

\[
\|\partial_k F(\theta)-\partial_k F(0)\|_2
 <1160972\delta<1200000\delta.
\]

Since `||J_0^{-1}||<5` and four coordinates obey
`||a||_2>=||a||_1/2`, integration along the angle segment gives

\[
\|F(\theta)\|_2
 >\bigl(1/10-1200000\delta\bigr)\delta
 >\delta/20.
\]

For any column `u=(u_T,a)`, put `e=u_T-x(theta)a`. If
`Y=||Q(theta)u||_2`, the selected 95 rows imply `||e||<50Y`.
The four residual rows then give
`|a|<20(1+4*50)Y/delta=4020Y/delta`. Because
`||(x(theta),1)||<5`, it follows that
`||u||<(50+20100/delta)Y <=20150Y/delta`, proving the bound.

Finally, the literal Laurent stencil satisfies
`sum(d)+phase(row)-phase(column) == 0 mod 4` entry by entry. Multiplication
of all characters by a fourth root therefore conjugates the entire symbol
by unitary diagonal phase matrices. It transports the chart, Y vector and
angular derivative bounds to all four folded copies.

Replay:

```bash
python3 02_REGISTRY/research/certificates/a4d_y_curved_joint_folded_quantitative_isolation_check.py
```

The certificate consumes the pinned exact inverse bounds from the
folded-isolation and torus-Lipschitz owners, checks the literal stencil,
covariance, kernel vector and rational inequalities, and compares its
result with its pinned JSON. No zero-set or gap on the compact complement
of these four neighborhoods is asserted. The nonlinear reduced Y-center
equation and refinement-uniform response remainder also remain open.
