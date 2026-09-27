# A4D flat-link metric Euler identity

**Task:** `WRK-A4D-FLAT-METRIC-EULER-IDENTITY`
**Class:** `WORKER`
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
**Owners pinned:** naked-star density and quotient coordinates `(Q,K)`, merge `60e39da0` (#180); first variation (2.5), merge `4913b9ac`; Gram lift \(H(q)=\tfrac12 q\eta\), merge `deb05e05` (#208).
**Certificate:** `02_REGISTRY/research/certificates/a4d_flat_metric_euler_identity_check.py`

## 0. Terminal

\[
\boxed{\texttt{J2-FLAT-LINK-METRIC-EULER-IDENTITY-CERTIFIED}}
\]

On the \(L=2\) carrier, for every nondegenerate solder,

\[
\boxed{E_Q(Q,I)=0}
\]

in all ten symmetric Gram components, at every site. The same evaluator on one finite boost is not identically zero.

## 1. Direct formula

The density of a face \((r,s)\) based at \(x\) is the #180 term

\[
\epsilon_{rs}\,
G_2\bigl(v_u\wedge v_v,\,\star\mathfrak b(\mathcal R(P))\bigr),
\qquad
\mathcal R(P)=\tfrac12(P-P^{-1}),
\]

with \(P\) the based plaquette of the raw links and \(v\) the solder legs. The metric partial \(E_Q\) is the derivative of this density in the ten directions \(H(q)=\tfrac12 q\eta\), \(DQ[H(q)]=q\). No continuum curvature is used.

The dressed link is \(K_{x,r}=\Theta_x L_{x,r}\Theta_{x+r}^{-1}\). If every \(K\) is \(I\), then

\[
L_{x,r}=\Theta_x^{-1}\Theta_{x+r}
\]

and the four-corner product collapses:

\[
P=\Theta_x^{-1}(K_r K_s K_r^{-1} K_s^{-1})\Theta_x=I.
\]

The certificate checks this as a matrix identity in four indeterminate invertible frames. Thus \(\mathcal R(P)=0\) for every face and every solder. Every density term is the zero function of \(Q\), and every component of \(E_Q(Q,I)\) is zero. The same vanishing holds for raw identity links, which are the special case of constant solder inside \(K=I\); a displaced rational solder is included so the zero is not special to \(\eta\).

## 2. Hostile control

Replace the single edge \(L_{(0,0,0,0),0}\) by the #180 boost

\[
\begin{pmatrix}5/3&4/3&0&0\\4/3&5/3&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix}.
\]

Its \((0,1)\) plaquette curvature is nonzero. At the origin the ten metric components are

\[
(0,0,0,0,0,2/3,2/3,-2/3,0,-2/3)
\]

in the order \((00,01,02,03,11,12,13,22,23,33)\). The evaluator can return a nonzero rational.

Along the Cayley curve of the \(0\)-\(1\) boost generator the \((1,2)\) component is exactly \(-2t/(t^2-4)\). Its Taylor coefficient of \(t^0\) is \(0\) and the coefficient of \(t^1\) is \(1/2\).

## 3. Tangent cone

Let \(K(h)=I+h^m A+o(h^m)\) be differentiable in the link coordinate, with \(m\ge 1\), at a fixed admissible \(Q\). Because \(E_Q(Q,I)=0\),

\[
E_Q\bigl(Q,K(h)\bigr)=O(h^m).
\]

There is no connection-independent term. The boost curve shows that the first connection order can be exactly \(m\) and nonzero. This does not assert existence, uniqueness, smoothness, or an Einstein value of any joint germ.

## 4. Scope

No branch search, kernel census, or new action term. The identity is the direct finite Euler map on the declared \(L=2\) carrier.

## 5. Validation

```bash
python3 02_REGISTRY/research/certificates/a4d_flat_metric_euler_identity_check.py
```
