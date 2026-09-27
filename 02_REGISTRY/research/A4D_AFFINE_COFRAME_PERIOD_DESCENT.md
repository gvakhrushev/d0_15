# A4D affine/coframe period descent — exact early classification

**Task:** \`EXP-A4D-AFFINE-COFRAME-PERIOD-DESCENT\`  
**Status:** REVIEW / terminal classification complete  
**Baseline:** merged CONTROL taxonomy #263  
**Certificate:** \`02_REGISTRY/research/certificates/a4d_affine_coframe_period_descent_check.py\`

## 0. Correction of the starting picture

The raw coframe map is not an L=2-only primitive.

Lean already owns, for every archive period,

\[
\operatorname{coframeDifferential}(N)
=
\operatorname{forwardGaugeCoframe}(N),
\]

with

\[
\dim\ker d_f=4,\qquad
\dim\operatorname{im}d_f=4(L^4-1).
\]

The exact affine theorem
\`affineTranslation_flat_eq_forwardGaugeCoframe\`
is also quantified over arbitrary \(N\).

Therefore a square-root choice in character space is not needed to define the raw L=4 coframe/translation tangent. The real question is whether this kinematic tangent descends to the already local-Lorentz-quotiented \((Q,K)\) carrier, and whether it is a legitimate gauge redundancy of the selected star action.

## 1. Exact Fourier rank of the raw coframe map

For a Fourier character \(z=(z_0,\dots,z_3)\) and a four-component node amplitude \(v\),

\[
(d_f v)_{ra}=L(z_r-1)v_a.
\]

Hence

\[
\operatorname{rank}d_f(z)=
\begin{cases}
0,&z=(1,1,1,1),\\
4,&\text{otherwise}.
\end{cases}
\]

At L=2 this gives

\[
15\cdot4=60,
\]

exactly explaining the registered global rank-60 owner without identifying it with the six-dimensional local-Lorentz algebra.

## 2. Readout firewall: centered parent metric is not the J2 quotient metric

The owned centered parent/readout satisfies

\[
R(d_f\xi)=\operatorname{symmetricRoleGradient}(\xi),
\]

with Fourier derivative

\[
d_r(z)=\frac L2(z_r-z_r^{-1}).
\]

For L=2 all characters have \(z_r=\pm1\), so this centered readout vanishes on the complete rank-60 forward-coframe image.  At L=4 it has rank 0 on 16 characters and rank 4 on 240.

This is a genuine finite fact, but it is **not** the metric carrier used by #262/#208.  It is retained only as a hostile type control: two different registered metric readouts must not be silently identified.

The J2 carrier instead uses the nonlinear Lorentz-quotient coordinate

\[
Q_x=\Theta_x\eta\Theta_x^T.
\]

If \(H\) stores the flat solder-vector perturbations as rows, #208 owns

\[
DQ_{\rm flat}[H]=H\eta+\eta H^T.
\]

For a forward-coframe Fourier tangent

\[
H_{ra}=L(z_r-1)\xi_a,
\]

the map \(\xi\mapsto DQ[H]\) has exact rank 4 for every nontrivial character, at both L=2 and L=4.  Thus the target statement is

\[
\boxed{
\operatorname{rank}(DQ_{\rm raw}\circ d_f)=4
\quad\text{for every nontrivial Fourier character.}
}
\]

There is no L2-to-L4 visibility jump on the actual J2 metric quotient.

### 2.1 Flat differential into the joint quotient carrier

The target connection coordinate can also be typed directly.

With raw linear links fixed, differentiate

\[
K_{x,r}=\Theta_xL_{x,r}\Theta_{x+r}^{-1}
\]

at \((\Theta,L)=(\eta,I)\).  In the #208 solder-vector convention the Fourier link tangent is

\[
k_r=(1-z_r)H.
\]

The exact metric-compatibility identity
\(KQ_{x+r}K^T=Q_x\) gives

\[
k_r\eta+\eta k_r^T=(1-z_r)q,
\qquad q=DQ[H].
\]

Using the #208 metric section \(H(q)=\frac12q\eta\), define the residual connection coordinate

\[
\boxed{
a_r
=
(1-z_r)
\left(
H-\frac12q\eta
\right).
}
\]

The bracket is an exact Lorentz tangent:

\[
\left(H-\frac12q\eta\right)\eta
+
\eta\left(H-\frac12q\eta\right)^T
=0.
\]

Therefore the flat forward-coframe tangent has a canonical typed image in the complex \(10+24\) joint carrier.  The next exact gate is no longer TYPE existence: it is to realify this map with the #262 \(z\leftrightarrow\bar z\) convention and test its image against the literal #262 joint Hessian/nullspace on all nine singular orbits.

## 3. The square map does not select the diagonal quarter-wave

The fully alternating L2 character has fibre

\[
\pi^{-1}((-1,-1,-1,-1))=\{\pm i\}^4,
\]

with 16 elements. It contains both \((i,i,i,i)\) and \((i,i,-i,-i)\).

Thus coordinatewise squaring cannot explain why #262 sees a six-dimensional connection-only block only on the diagonal orbit while the mixed orbit has none.

## 4. Stronger TYPE obstruction: the owned affine solder action needs observer data

Merged affine-solder work already constructs an exact affine group action on the enlarged raw carrier. For a pure translation its solder law is

\[
\Theta'_{x,r}
=
\Theta_{x,r}
+
\tau_{x,r}^{T}h_{n_x},
\]

where \(h_n\) is the owned observer-positive form.

This reproduces the flat \`forwardGaugeCoframe\` chart and is Lorentz-covariant. But \(n\) is not part of the quotient-coordinate pair \((Q,K)\).

The certificate gives an exact rational hostile witness. Start from

\[
\Theta=\eta,\qquad L=I,
\]

hence the same starting \(Q=\eta,\ K=I\). Take

\[
n_0=(1,0,0,0),\qquad
n_1=(5/3,4/3,0,0),
\]

related by a proper rational Lorentz boost. Then

\[
h_{n_0}=I,
\]

whereas

\[
h_{n_1}
=
\begin{pmatrix}
41/9&-40/9&0&0\\
-40/9&41/9&0&0\\
0&0&1&0\\
0&0&0&1
\end{pmatrix}.
\]

For the same local pure translation row \(\tau=e_0\), the transformed metric is respectively

\[
Q'_0=\operatorname{diag}(4,-1,-1,-1)
\]

and

\[
Q'_1=
\begin{pmatrix}
100/9&-40/9&0&0\\
-40/9&-1&0&0\\
0&0&-1&0\\
0&0&0&-1
\end{pmatrix}.
\]

Therefore the observer-completed affine transformation is not a function of the starting \((Q,K)\) coordinates alone. A descent requires either retaining observer/section data or supplying a canonical observer/section selector.

## 5. Symmetry gate is independent and stronger than a rank map

The merged owner
\`MEMO_A4D_FULL_AFFINE_SOLDER_GAUGE_QUOTIENT.md\`
already proves that the observer-completed affine translation is not an off-shell symmetry of the accepted star density on curved backgrounds.

Hence even an enlarged \((Q,K,n)\) kinematic action cannot be called a physical gauge quotient of the selected action.

The hierarchy is

\[
\text{raw all-period }d_f\quad\checkmark,
\]

\[
\text{observer-completed affine representation}\quad\checkmark,
\]

\[
\text{descent to }(Q,K)\text{ alone}
\quad\text{blocked by observer/section data},
\]

\[
\text{gauge quotient of }S_\star
\quad\text{blocked by exact off-shell symmetry failure}.
\]

## 6. Current exact blocker

The original "build an L2-to-L4 gauge intertwiner" wording was too coarse.

The exact current blocker is

\`\`\`text
J2-AFFINE-COFRAME-QK-DESCENT-REQUIRES-OBSERVER-OR-ACTION-COMPLETION
\`\`\`

This is a partial blocker, not yet one of the task's final terminals.

The next useful question is narrower: whether a section-independent differential on the L4 real \((Q,K)\) carrier can be extracted from the supplied observer family, or whether the observer witness above upgrades to a universal no-descent theorem after quotienting all allowed raw representatives.

No local-Lorentz re-quotient, Einstein claim, remnant interpretation, \(\varphi\) identification or seam-number identification follows.


## 7. Exact L4 joint-carrier image

The can-fail certificate

\`02_REGISTRY/research/certificates/a4d_affine_coframe_joint_carrier_check.py\`

now performs the literal same-carrier test against the accepted #262
conjugate-paired joint Hessian.

The construction is first checked against the already-owned L2 control:
all 15 nontrivial L2 forward-coframe Fourier images have complex rank four
and are exact flat joint-Hessian null directions.  This pins the compensating
local-Lorentz convention before any L4 conclusion is read.

At L4 the complex four-dimensional map realifies to an eight-dimensional
image on every singular orbit representative.  The exact table is

| orbit | ids | real affine image | rank of connection residual | affine image intersect joint kernel | type of surviving intersection |
|---|---|---:|---:|---:|---|
| 0 | (0,0,1,1) | 8 | 6 | 2 | metric-only |
| 1 | (0,0,1,3) | 8 | 6 | 2 | mixed |
| 2 | (0,1,1,2) | 8 | 8 | 0 | none |
| 3 | (1,0,1,2) | 8 | 8 | 0 | none |
| 4 | (1,1,1,1) | 8 | 6 | 2 | metric-only |
| 5 | (1,1,3,3) | 8 | 8 | 0 | none |
| 6 | (2,0,1,1) | 8 | 8 | 0 | none |
| 7 | (2,1,1,2) | 8 | 8 | 0 | none |
| 8 | (2,1,2,3) | 8 | 6 | 2 | mixed |

On orbits 0 and 4 the two-dimensional surviving affine intersection equals
the complete #262 metric-only plane.  On orbits 1 and 8 both projections of
the surviving two-plane have rank two, so the intersection is genuinely
mixed.  The other five orbit types have zero intersection.

Thus

\[
\boxed{
\text{no L4 singular orbit has the full forward-coframe image in }
\ker H_J^{\rm real}.
}
\]

This is the decisive firewall against calling the period-generic
forward-coframe tangent a gauge image of the selected L4 star Hessian.
The L2 rank-60 flat null result is a special period-two result; it does not
transport as gauge-nullity merely because the raw coframe differential itself
is defined at every period.

The square-map slogan is also too weak in the opposite direction.  Orbit 4 and
orbit 5 both lie in the fully alternating square fibre, yet their affine/null
intersections are respectively 2 and 0.  The actual star symbol, not the
covering, controls the difference.

## 8. Revised classification

The task has now separated four logically different statements:

1. **Raw period-generic coframe tangent:** owned for every L.
2. **Flat linear descent to Lorentz-quotient (Q,K):** explicitly constructed.
3. **L4 star-Hessian gauge-nullity:** rejected by the nine-orbit exact table.
4. **Nonlinear affine gauge symmetry:** independently rejected for the current
   observer-completed law by the merged curved off-shell witness.

The durable checkpoint is therefore

\`\`\`text
J2-AFFINE-COFRAME-L4-KINEMATIC-DESCENT-NOT-GAUGE-NULL
\`\`\`

This is intentionally not promoted to one of the brief's original final
terminals: the computation found a third outcome not anticipated by that
terminal list.  A typed kinematic descent exists, so there is no no-map theorem;
but the descended image is not a gauge-null image of the selected L4 action.

No physical quotient by this affine image is licensed.
