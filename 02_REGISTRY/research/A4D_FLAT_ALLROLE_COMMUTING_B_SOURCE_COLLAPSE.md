# Flat all-role commuting-B source-image collapse

Task: \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`, Draft PR #310.  
Parent controls: \`A4D_PERIODIC_COMMUTING_B_SOURCE_RIGIDITY.md\`,
the literal physical flat symbol \((A^T;C)\), and the #216 smooth-tail lemma.  
Status: exact linear symbol theorem plus a refinement-uniform nonlinear
small-field consequence for the complete all-role real commuting
\(B=K_1+K_2+K_3\) subgroup.  No unrestricted task terminal.

## 1. Sector

At flat solder \(Q=\eta\), let every link lie in the same real
one-parameter Lorentz subgroup

\[
L_{x,r}=\exp(a_{x,r}B),\qquad
B=K_1+K_2+K_3 .
\]

All four roles and arbitrary lattice dependence are allowed.  There is no
four-phase, one-envelope, or Fourier-support ansatz.

For the linearized field, write the four role amplitudes as
\(u=(u_0,u_1,u_2,u_3)^T\).  Let

\[
J_B(z)=
\begin{pmatrix}H_B(z)\\ C_B(z)\end{pmatrix}
\]

be the restriction of the physical flat joint symbol
\((A(z)^T;C(z))\) to the four columns
\(B^{(0)},\ldots,B^{(3)}\).

Use forward differences
\[
d_r=z_r-1,\qquad s=d_1+d_2+d_3.
\]

## 2. Exact metric block

After multiplying by two, the only nonzero rows of \(C_B\) are

\[
2C_B(d)=
\begin{pmatrix}
0&-(d_2+d_3)&d_1&d_1\\
0&d_2&-(d_1+d_3)&d_2\\
0&d_3&d_3&-(d_1+d_2)\\
d_2+d_3&0&-d_0&-d_0\\
-(d_1+d_2)&d_0&d_0&0\\
-(d_1+d_3)&d_0&0&d_0\\
d_1+d_3&-d_0&0&-d_0\\
-(d_2+d_3)&0&d_0&d_0\\
d_1+d_2&-d_0&-d_0&0
\end{pmatrix},
\tag{1}
\]

up to the one identically zero metric row.

There is an exact moving line
\[
\boxed{C_B(d)d=0.}
\tag{2}
\]

If \(d_0\ne0\), one displayed \(3\times3\) minor is
\[
\det (2C_B)_{\{4,5,6\},\{1,2,3\}}=2d_0^3,
\]
equivalently the same minor of \(C_B\) is \(d_0^3/4\).
Hence \(\operatorname{rank}C_B=3\) and
\[
\ker C_B=\mathbb C d.
\tag{3}
\]

If \(d_0=0\), the spatial \(3\times3\) block is
\[
2N=d_{\rm sp}\mathbf1^T-sI_3.
\tag{4}
\]
For \(s\ne0\), \(N\) has rank two and the lower first-column rows add one
independent direction, again giving rank three.  For \(s=0\ne d_{\rm sp}\),
\(N=d_{\rm sp}\mathbf1^T/2\) has rank one and the lower first column adds one,
so the rank drops to two.

Thus the complete nonzero complex rank-drop locus of the restricted metric
block is

\[
\boxed{d_0=0,\qquad d_1+d_2+d_3=0.}
\tag{5}
\]

On the physical unit torus, (5) has no nontrivial point.  Indeed
\(d_0=0\) gives \(z_0=1\), while \(s=0\) gives
\[
z_1+z_2+z_3=3.
\]
For \(|z_j|=1\), equality in the triangle inequality forces
\(z_1=z_2=z_3=1\).  Therefore for every nontrivial physical character,

\[
\boxed{\ker C_B(z)=\mathbb C\,d(z).}
\tag{6}
\]

## 3. Connection rows kill the last metric-null line

Substitute \(u=d\) into the physical connection block.  Four literal rows are

\[
(H_Bd)_9=-\frac{d_0}{1+d_0},\qquad
(H_Bd)_{12}=-\frac{d_1}{1+d_1},
\]
\[
(H_Bd)_7=-\frac{d_2}{1+d_2},\qquad
(H_Bd)_8=-\frac{d_3}{1+d_3}.
\tag{7}
\]

Since physical characters have \(1+d_r=z_r\ne0\), equations (6)--(7) imply

\[
H_Bu=0,\quad C_Bu=0
\quad\Longrightarrow\quad
u=0
\]

at every nontrivial unit character.  At the trivial character the full
connection Hessian is already invertible with determinant \(256\), so its
four-column restriction is injective.

Hence

\[
\boxed{
\ker J_B(z)=0
\quad\text{for every }z\in\mathbb T^4.
}
\tag{8}
\]

This is an all-frequency theorem, not a root-grid census.

By continuity on the compact torus there is a constant \(c_B>0\) such that

\[
\|J_B(z)u\|_2\ge c_B\|u\|_2
\quad\text{for all }z\in\mathbb T^4.
\tag{9}
\]

The smooth periodic left inverse
\[
L_B(z)=(J_B(z)^*J_B(z))^{-1}J_B(z)^*
\]
has absolutely summable Fourier kernel.  Therefore its periodic restrictions
have refinement-independent convolution bounds on every componentwise
\(\ell^p\), \(1\le p\le\infty\).

This is the restricted analogue of the desired global joint inf-sup estimate,
but here it is unconditional because the whole physical unit torus has been
removed algebraically.

## 4. Nonlinear smooth-source consequence

Let an exact field in the same subgroup satisfy

\[
\|a_h\|_\infty\le C_0h,
\tag{10}
\]
\[
E_K(\eta,L(a_h))=0,\qquad
E_Q(\eta,L(a_h))=h^2\tau_h,
\tag{11}
\]

where \(\tau_h\) is sampled from a uniformly smooth bounded source family.
Finite-stencil analyticity gives, in every \(\ell^p\),

\[
E_K=H_Ba_h+N_K(a_h),\qquad
E_Q=C_Ba_h+N_Q(a_h),
\]
\[
\|N_K(a_h)\|_p+\|N_Q(a_h)\|_p
\le C\|a_h\|_\infty\|a_h\|_p.
\tag{12}
\]

Apply the global joint left inverse from (9).  For sufficiently small \(h\),

\[
\|a_h\|_p
\le C_B\left(h^2\|\tau_h\|_p
              +C_0h\|a_h\|_p\right),
\]
hence

\[
\boxed{\|a_h\|_p\le C h^2\|\tau_h\|_p.}
\tag{13}
\]

Choose a fixed low-phase ball on which the connection block \(H_B(z)\)
itself is invertible; this exists because the full \(H(1)\) is invertible.
Let \(P_{\rm IR}\) be a smooth Fourier cutoff supported there.  Projecting
the exact connection equation and using (10),(12),(13),

\[
\|P_{\rm IR}a_h\|_p
\le C\|N_K(a_h)\|_p
\le C h^3\|\tau_h\|_p .
\tag{14}
\]

Project the metric equation to the same IR region:

\[
h^2\|P_{\rm IR}\tau_h\|_p
\le
C\|P_{\rm IR}a_h\|_p
+
C\|N_Q(a_h)\|_p
\le C h^3\|\tau_h\|_p .
\]

Thus

\[
\boxed{
\|P_{\rm IR}\tau_h\|_p
\le Ch\|\tau_h\|_p.
}
\tag{15}
\]

For a fixed \(C^\infty\) source (or a uniformly bounded smooth/Wiener family),
the #216 sampling/alias lemma gives

\[
\|(1-P_{\rm IR})\tau_h\|_p=O(h^\infty)
\]

in the corresponding smooth Fourier topology; in particular this holds in
\(p=\infty\), and by the convolution formulation in the normalized \(p\)
topologies used for continuum testing.  Combining with (15),

\[
\boxed{\|\tau_h\|=O(h)+O(h^\infty).}
\tag{16}
\]

Therefore a source sampled from one fixed smooth nonzero continuum tensor
cannot be realized by any exact small field in the complete all-role
commuting-\(B\) subgroup:

\[
\boxed{
\tau_h\to\tau\text{ smoothly and (10)--(11)}
\quad\Longrightarrow\quad
\tau=0.
}
\tag{17}
\]

The #227 family is not a counterexample: its normalized source is a fixed
checkerboard/quarter-wave field, not a smooth sampled source.  Equation
(13) is consistent with its amplitude \(a_h=O(h^2)\).

## 5. What this closes

This removes the spatial-compensation loophole **inside the entire commuting
\(B\) class**.  Spatial links may be arbitrary functions of all four
coordinates and may occupy any lattice frequencies; no phase count or
envelope period is fixed.

In source-image language,

\[
\boxed{
\lim_{h\to0}
\mathscr T_h^{B,\;O(h),\;{\rm smooth}}
=\{0\}.
}
\tag{18}
\]

Thus any surviving non-Einstein smooth-source anomaly must leave the
one-parameter commuting subgroup: it must use genuinely noncommuting Lorentz
directions (or a different finite-amplitude chart/background mechanism).

This is a class cut, not a representative census.

## 6. Scope

The theorem is centered at the flat identity solder and assumes all candidate
links lie in one common real \(B\) subgroup with \(O(h)\) logarithms.  It does
not yet transport the global gap through a general varying coframe, and it
does not control noncommuting mixtures of different resonance centers.

The \(\ell^p\) nonlinear estimate is a standard finite-stencil consequence of
the exact global symbol gap.  Raw unnormalized owner sums must keep their
explicit lattice-volume factors when translating (16); the fixed-source
nonexistence conclusion (17) is topology-independent once uniform convergence
of the sampled source is assumed.

Verdict:

\[
\boxed{\texttt{FLAT-ALLROLE-COMMUTING-B-SMOOTH-SOURCE-IMAGE-COLLAPSES}.}
\]

No action change, selector, torus census, connection uniqueness, BOOK/CORE
promotion or unrestricted Einstein terminal is asserted.
