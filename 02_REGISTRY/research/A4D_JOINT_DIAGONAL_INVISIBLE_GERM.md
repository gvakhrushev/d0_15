# A4D diagonal invisible joint germ

**Task:** `WRK-A4D-JOINT-DIAGONAL-INVISIBLE-GERM`
**Class:** `WORKER`
**Research lane:** `EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS`
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
**Dependency:** `WRK-A4D-JOINT-RESONANCE-LINEAR-KERNEL`, merged as PR #252. The orbit-4 basis is read from `a4d_joint_resonance_kernel_census.json` and recomputed from the polarized symbol.
**Certificate:** `02_REGISTRY/research/certificates/a4d_joint_diagonal_invisible_germ_check.py`

## 0. Status

```text
REVIEW
J2-DIAGONAL-INVISIBLE-JOINT-VACUUM-GERM-FOUND
```

The origin is **not isolated**. Section 9 gives exact finite analytic curved joint-vacuum branches on every pure real COS/SIN axis of the owned four-dimensional N0. The full independent-edge Euler and all unrestricted solder partials vanish identically. This existence result closes the task's isolation-versus-branch question; it does not classify mixed directions.

The following records the separate, still valid obstruction on the selected mixed ray. The complex quarter-wave and its conjugate each have a nonzero corrected degree-4 metric Euler on \(u=(0,0,1,1)\). On the real cosine and sine dressings the resonant weight has connection Euler zero through degree 7 after the degree-2 even correction. The orthogonal weight does not. For the cosine its degree-3 part is \((0,32,32,0,0,0,\ 0,0,0,32,32,0,\ 0,-32,0,-32,0,0,\ 0,0,-32,0,-32,0)\), and the sine vector is the negative. The covector \(e_0+e_1+e_2\) pairs with these vectors to \(64\) and \(-64\). Every degree-3 link correction, expanded in the four Fourier weights, leaves that pairing unchanged. The forcing is therefore outside the image. A higher-order link correction does not enter degree 3. In the Gram chart \(H(q)=q\eta/2\) the derivative along the ten constant components has rank 10, with unique direction \(q=-\eta\). On the line \(t(-\eta)\) the Euler is \((1-t/2)^2\) times the forcing, hence zero only at the zero frame \(t=2\). Every constant root has \(\det(I+\eta q/2)=0\). A solder jet of degrees \(0\) through \(3\) has linear image rank 15 and does contain the forcing. The quadratic solder equations are the full response of this fixed flux, because the area element is quadratic in \(q\). Their ideal contains \(\det(I+\eta q/2)\), so every solder solution is degenerate. The pure axes \(u=e_i\) have zero degree-2 even forcing and zero connection Euler through degree 6 in all four Fourier weights, so they are not cut by this degree-3 obstruction. That selected-ray obstruction does not apply to the exact pure-axis germs proved in section 9.

PR #264 closes the affine bypass. Its terminal `J2-AFFINE-COFRAME-L4-KINEMATIC-DESCENT-NOT-GAUGE-NULL` shows that the flat forward-coframe image is not joint-Hessian-null on any singular L4 orbit. Those directions are not a gauge quotient of this carrier and cannot be used to delete the regular variables.

## 1. Invisible basis

At the diagonal quarter wave \(z=(i,i,i,i)\), \(H_{AA}\) has rank 16 and an 8-dimensional kernel. The metric map \(H_{QA}\) cuts that kernel down to the census orbit-4 space \(N_0\), dimension 4. In the integer kernel basis \((\lambda_0,\ldots,\lambda_7)\) one has

\[
N_0=\operatorname{span}\{\lambda_1,\lambda_3,\lambda_4,\lambda_6\}.
\]

Each vector occupies one Role. With generators \((K_1,K_2,K_3,J_{12},J_{13},J_{23})\),

| Coordinate | Census vector | Role | Weights |
|---|---|---|---|
| \(u_0\) | \(\lambda_1\) | 0 | \((0,0,0,1,-1,1)\) |
| \(u_1\) | \(\lambda_3\) | 1 | \((0,1,-1,0,0,1)\) |
| \(u_2\) | \(\lambda_4\) | 2 | \((1,0,-1,0,1,0)\) |
| \(u_3\) | \(\lambda_6\) | 3 | \((1,-1,0,1,0,0)\) |

The #216 range elimination applies at \(q=0\): a 16-dimensional complement of \(\ker H_{AA}\) is injected by \(H_{AA}\). The visible lines \(\lambda_0\) and \(w=\lambda_2+\lambda_5-\lambda_7\), and the #227 tangent, all have nonzero metric response, so they are not in \(N_0\).

The polarized scalar built from `curvature_mixed` vanishes identically on these four coordinates, and the symmetrized block \(H_{AA}+H_{AA}^T\) vanishes on them. That quadratic polarized form does not see the sector. The joint system below is the next order of the odd plaquette holonomy \((P-P^{-1})/2\), whose linear term is the census factor \((1-i)\).

## 2. Odd-holonomy truncation with regular coordinates set to zero

This section does not solve the regular connection equations. Through degree 2 the flat-metric star density on \(N_0\), with the regular coordinates held at zero, is

\[
V_2=2(1-i)\,u_0(-u_1+u_2-u_3).
\]

The connection Euler is its gradient,

\begin{align*}
E_{K,0}^{\rm red}&=2(1-i)(-u_1+u_2-u_3),\\
E_{K,1}^{\rm red}&=-2(1-i)\,u_0,\\
E_{K,2}^{\rm red}&=2(1-i)\,u_0,\\
E_{K,3}^{\rm red}&=-2(1-i)\,u_0.
\end{align*}

The metric Euler \(E_Q^{\rm red}\) is quadratic. Fifteen of the sixteen leg components are nonzero. Two of them are enough to finish the elimination:

\begin{align*}
E_{Q,01}^{\rm red}&=(1-i)u_1(u_3-u_2),\\
E_{Q,02}^{\rm red}&=(-1+i)(u_1 u_2+u_2 u_3).
\end{align*}

`E_K^{\rm red}=0` forces \(u_0=0\) and \(u_2=u_1+u_3\). Substitution into \(E_{Q,01}^{\rm red}\) gives \(-(1-i)u_1^2=0\), hence \(u_1=0\). Then \(E_{Q,02}^{\rm red}=(-1+i)u_3^2=0\), hence \(u_3=0\) and \(u_2=0\).

The only solution is the origin. The Jacobian of \(E_K^{\rm red}\) has rank 2, and every component of \(E_Q^{\rm red}\) is quadratic, so the joint differential at the origin is degenerate. Isolation is by the quadratic metric equations, not by an invertible Jacobian. A formal curve \(u(t)=t^k a+\cdots\) with \(a\neq 0\) would make every quadratic vanish at order \(2k\), which forces \(a=0\).

## 3. Comparison

- #227 is the source-visible tangent \(K_1+K_2+K_3\). It is not in \(N_0\), and \(E_Q\) cuts it. It is not a germ of this sector.
- #225 moves the visible coordinates on \(\lambda_0\) and \(w\). Those lines are the complement of \(N_0\). The slow-background splitting does not decide this sector.
- The connection-only quartic on \((a,b,c,d)\) is supported on that visible complement. It is not this joint system.

## 4. Boundary of the single-plaquette truncation

Section 2 is retained as a calculation, not as an isolation theorem. Its quadratic system is not the torus Euler: the same scalar, summed over the L=4 grid, cancels through degree 3.

## 5. Pure-mode degree-4 response

Let the link at site \(x\) in direction \(r\) be \(\exp(\zeta(x)\, u_r M_r)\), with \(\zeta(x)=i^{x_0+x_1+x_2+x_3}\) and \(M_r\) the census generator of coordinate \(u_r\). Sum the odd-holonomy scalar over all sites and all six face orientations. The sum is

\[
\begin{aligned}
V_4=-128 i\, u_0\big(
&u_0^2(3-3i)(u_1-u_2+u_3)
+u_0(-2+3i)(u_1^2+u_2^2+u_3^2)\\
&+(-1+i)(u_1^3-u_2^3+u_3^3)
\big).
\end{aligned}
\]

Degrees 0, 1, 2, and 3 are zero. The connection Euler \(\nabla V_4=0\) is the cone \(u_0=0\), \(u_1^3=u_2^3-u_3^3\). Pairing the same quartic against the visible kernel vectors gives zero on \(\lambda_0\), \(\lambda_5\), and \(\lambda_7\). The \(\lambda_2\) pairing cuts the cone to

\[
u_0=u_1=0,\qquad u_2^3=u_3^3.
\]

On that line the constant-solder metric Euler starts at degree 4. At \((u_2,u_3)=(1,1)\) its Gram component \((0,2)\) equals 32. The same component is nonzero at the other two cube roots of unity. Section 6 substitutes the character-\((-1)\) correction into this Euler.

## 6. Character \((-1)\) correction on the critical line

The quadratic product of the quarter-wave character is \((-1,-1,-1,-1)\). The variational Hessian of the odd-holonomy sum at that character is symmetric of rank 24, so the quadratic correction \(r\) is unique. On \(u=(0,0,1,1)\) it is the half-integer vector whose nonzero entries are

\[
\begin{aligned}
&(1/2+i/2,-i/2,-i/2,i/2,i/2,0),\\
&(1/2+i/2,-i/2,-i/2,i/2,i/2,0),\\
&(0,0,i/2,0,-i/2,i/2),\\
&(0,i/2,0,-i/2,0,-i/2).
\end{aligned}
\]

Substituting \(t^2 r\) with the character-\((-1)\) dressing leaves the metric Euler zero at orders \(t^2\) and \(t^3\). At order \(t^4\) the Gram components are

\[
(-64,\ 128,\ -192+192i,\ -192+192i,\ -64,\ 192-192i,\ 192-192i,\ 0,\ 0,\ 0).
\]

The same corrected degree-4 metric Euler is nonzero at \(u_2=-1/2\pm i\sqrt{3}/2\), \(u_3=1\). These three values are computed with the same-character correction held at zero.

## 7. Conjugate orbit and the real dressings

At \(z=(-i,-i,-i,-i)\) the character-\((-1)\) Hessian is the same real rank-24 matrix. On \(u=(0,0,1,1)\) the forcing, the correction, and the degree-4 metric Euler are the complex conjugates of the \(z=i\) values. The conjugate row is

\[
(-64,\ 128,\ -192-192i,\ -192-192i,\ -64,\ 192+192i,\ 192+192i,\ 0,\ 0,\ 0).
\]

The real carrier of this ray uses \(\operatorname{Re}(i^{x_0+x_1+x_2+x_3})\) and \(\operatorname{Im}(i^{x_0+x_1+x_2+x_3})\). Each dressing sources both the zero mode and the character-\((-1)\) mode at order \(t^2\), on coordinates 13, 15, 20, and 22. Both Hessians have rank 24. The cosine corrections are \(\tfrac14 K_1\) on Roles 0 and 1 in each channel. The sine zero-mode correction is the same vector, and its character-\((-1)\) correction is the negative. After substitution, both dressings have a nonzero degree-1 plaquette holonomy, while the scalar, the 24-component connection Euler, and the constant-solder metric Euler vanish through degree 4.

The degree-5 resonant connection Euler vanishes exactly for both corrected real dressings, and the degree-5 metric Euler also vanishes.

The degree-5 metric coefficient includes exponential order 5, so that vanishing is the full \(t^5\) term. At degree 6 the even forcing is supported on Roles 0 and 1. The certificate solves the even Hessian equation \(Hc+F=0\). Substituting those corrections into the metric series gives zero on all ten Gram components. For the cosine, the character-\((-1)\) forcing is
\[
(0,-20/3,-20/3,-4,-4,0,\ 0,4/3,4/3,-4/3,-4/3,0,\ 0,\ldots,0)
\]
and the zero-mode forcing is its negative. Both cosine corrections equal
\[
\begin{aligned}
&(0,-1/96,-1/96,1/96,1/96,0),\\
&(0,-1/96,-1/96,1/96,1/96,0),\\
&(1/192,0,0,0,0,1/64),\\
&(1/192,0,0,0,0,-1/64).
\end{aligned}
\]
The sine character-\((-1)\) forcing equals the sine zero-mode forcing, and both equal the negative of the cosine character-\((-1)\) forcing. The sine character-\((-1)\) correction is the negative of the vector above; the sine zero-mode correction equals that vector. After these corrections the degree-6 metric Euler is zero on all ten Gram components.

On the resonant weight the connection Euler stays zero through degree 7. On the orthogonal weight the cosine Euler is nonzero at degrees 3, 5 and 7; the sine Euler is the negative. The degree-3 piece is the vector in §0. Its pairing with \(e_0+e_1+e_2\) is \(64\) for the cosine and \(-64\) for the sine, and no degree-3 link correction changes that pairing. This is the first failure of the \(u=(0,0,1,1)\) connection jet. The quadratic solder equations of this fixed flux contain \(\det(I+\eta q/2)\), so every solder solution is degenerate. The constant root is the zero frame \(q=-2\eta\). The pure axes \(u=e_i\) have zero connection Euler through degree 6 in the four Fourier weights.

No torsion constraint, new action channel, \(\varphi\)-selector, or global Einstein equation is used. The four-space is census data on one L4 orbit. It is not a local Lorentz quotient, and the #264 coframe descent is not a gauge deletion of the regular variables.

## 8. Validation

```bash
python3 02_REGISTRY/research/certificates/a4d_joint_diagonal_invisible_germ_check.py
python3 02_REGISTRY/research/certificates/a4d_joint_diagonal_invisible_degree3_solder_check.py
python3 tools/validate_repo.py
python3 tools/validate_work.py
```


## 9. Exact finite branches on all four pure axes

The remaining pure-axis gate is resolved by a finite formula. Write the four
matrices from section 1 as `Y_r`, where `Y_r` occupies role `r`, and put

\[
 \kappa_0=3,\qquad\kappa_1=\kappa_2=\kappa_3=-1,
 \quad
 U_r(z)=I+\frac{4z}{4+\kappa_r z^2}Y_r
          +\frac{2z^2}{4+\kappa_r z^2}Y_r^2.
\]

These are exactly the Cayley transforms of `z Y_r`. Each generator is simple:
if `a<b<c` are the roles other than `r`, then

\[
 Y_r=-[(e_b-e_a)(e_c-e_a)^T-(e_c-e_a)(e_b-e_a)^T]\eta,
 \qquad Y_r^3=-\kappa_rY_r.
\]

On the L=4 torus, let `p(x)=x0+x1+x2+x3 mod 4`. Set the solder to the identity
at every site, hence `Q=eta`, and define

\[
 K_r(x;z)=(U_r(z),I,U_r(z)^{-1},I)_{p(x)},
 \qquad K_s(x;z)=I\quad(s\ne r).
\]

For real `|z|<1` these are real analytic Lorentz links with all Cayley
charts open. The coframe determinant is exactly one. At `z=0` all links
are identity; their derivative is `cos(pi*p/2) Y_r` on role `r`, exactly
the corresponding real axis of the census `N0`. Replacing `p` by `p-1`
gives `sin(pi*p/2) Y_r`. If the real dressing is normalized as a sum of
complex conjugates rather than its half, reparameterize `z` by `2z`.

### Complete joint equations, not a restricted gradient

The standalone certificate
`certificates/a4d_joint_diagonal_invisible_exact_axes_check.py` reads and
checks the owned census basis. For each of the four axes it constructs the
full oriented plaquette

\[
 P_{ab}(x)=K_a(x)K_b(x+e_a)K_a(x+e_b)^{-1}K_b(x)^{-1},
 \qquad F_{ab}=\tfrac12(P_{ab}-P_{ab}^{-1}).
\]

It differentiates each individual edge in all incident plaquettes, including
incoming base sites, against all six independent Lorentz generators. It also
differentiates the local action against all sixteen independent coframe
entries, holding the connection fixed. All `4*24=96` connection components
and `4*16=64` solder components vanish as rational functions in `z`, for
**each** axis. These four phases represent all 256 torus sites; testing phases
does not restrict variations to a four-phase ansatz. It evaluates the gradient
of the full action at that ansatz. The ten metric partials therefore vanish
as well. The sine solutions are lattice translations of these same exact
identities. No finite Taylor cutoff is involved.

The cancellation has the simple-plane mechanism also used on the explicit
Y branch in #275. The three complementary signed areas combine into the
simple plane above. Its star pairing with its own infinitesimal coframe
variation is zero. The incident-edge sums cancel or reduce to a commutator
with this plane, whose dual commutes with it. Here the rational checker
verifies all components directly for all four roles, without importing #275
as a dependency or changing the constant metric.

At phase zero, on each face incident to the active role, the odd curvature is

\[
 F_{ab}=\pm\frac{4z}{4+\kappa_r z^2}Y_r.
\]

It is nonzero for every sufficiently small nonzero real `z`. Thus these are
curved finite joint vacua arbitrarily close to the flat point, and cannot be
removed by an internal Lorentz gauge transformation. They solve the regular
connection equations automatically; a choice of complementary coordinates
for range elimination cannot turn a full stationary branch into an isolated
zero. Every Taylor coefficient of the full joint Euler on these branches is
zero, so there is no first nonzero joint order to find on a pure axis.

The #227 source-visible control `K1+K2+K3` on role zero fails the unrestricted
solder gate under the same Cayley/four-phase construction. The nontrivial
metric test therefore does distinguish the invisible branches. No conclusion
is borrowed from #225's slow-background splitting or the invalid affine gauge
bypass. The mixed `u=(0,0,1,1)` obstruction and its degenerate-solder result
remain separate exact facts; their survival does not restore isolation.

### Terminal and scope

`J2-DIAGONAL-INVISIBLE-JOINT-VACUUM-GERM-FOUND` is certified by four explicit
real COS branches and their SIN translates. This resolves the task's required
negative alternative by exact finite existence, which is stronger than an
order-limited formal germ. It is not an eight-parameter joint solution sheet,
not a classification of mixed coordinates, and not the arbitrary slow-metric
limit of #240. No new action, torsion restriction, selector or Einstein claim
is used. No new Lean theorem is claimed.

Reproduce the new terminal:

```bash
python3 02_REGISTRY/research/certificates/a4d_joint_diagonal_invisible_exact_axes_check.py
```

The historical large germ checker in section 8 retains the selected mixed-ray
calculations and its old blocked diagnostic; that diagnostic does not describe
the pure-axis existence terminal established here. Task retirement is confined
to this isolation-versus-existence objective. Acceptance/merge remains CONTROL.
