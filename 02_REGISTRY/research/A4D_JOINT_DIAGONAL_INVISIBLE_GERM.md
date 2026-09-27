# A4D diagonal invisible joint germ

**Task:** `WRK-A4D-JOINT-DIAGONAL-INVISIBLE-GERM`
**Class:** `WORKER`
**Research lane:** `EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS`
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
**Dependency:** `WRK-A4D-JOINT-RESONANCE-LINEAR-KERNEL`, merged as PR #252. The orbit-4 basis is read from `a4d_joint_resonance_kernel_census.json` and recomputed from the polarized symbol.
**Certificate:** `02_REGISTRY/research/certificates/a4d_joint_diagonal_invisible_germ_check.py`

## 0. Status

```text
BLOCKED
J2-DIAGONAL-INVISIBLE-ORTHOGONAL-DEGREE-3-EULER-OUTSIDE-LINK-IMAGE
```

The origin-isolated terminal is not accepted. The complex quarter-wave and its conjugate each have a nonzero corrected degree-4 metric Euler on \(u=(0,0,1,1)\). On the real cosine and sine dressings the resonant weight, the same weight as the ray, has connection Euler zero through degree 6 after the even corrections. At degree 7 that resonant Euler is the same nonzero vector for both rays,
\[
(0,0,0,-128,-128,0,\ 0,-128,-128,0,0,0,\ 0,128,0,128,0,0,\ 0,0,128,0,128,0).
\]
The degree-6 even correction does not change it. The orthogonal odd weight is already nonzero at degree 3, before that degree-7 term. For the cosine the degree-3 orthogonal connection Euler is \((0,32,32,0,0,0,\ 0,0,0,32,32,0,\ 0,-32,0,-32,0,0,\ 0,0,-32,0,-32,0)\), and the sine vector is its negative. The four Fourier weights on the four phases span every phase-dependent link correction. Their degree-3 responses on this probe have ranks \(0,0,16,0\) for the zero mode, character \((-1)\), the resonant weight, and the orthogonal weight. The joint rank is 16, and the forcing lies outside that image on both rays. No degree-3 link correction cancels it, and a higher-order correction does not enter degree 3. Neither isolation nor a finite curved germ is claimed.

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

On the resonant weight the connection Euler stays zero through degree 6, with or without the degree-6 correction, and at degree 7 both rays carry the vector displayed in §0. On the orthogonal weight the cosine Euler is nonzero at degrees 3, 5 and 7; the sine Euler is the negative of the cosine Euler at each of those degrees. The degree-3 orthogonal components are
\[
(0,32,32,0,0,0,\ 0,0,0,32,32,0,\ 0,-32,0,-32,0,0,\ 0,0,-32,0,-32,0).
\]
The degree-5 resonant vanishing does not see this weight. The degree-3 orthogonal Euler is the first failure, and it lies outside the image of every degree-3 link correction.

No torsion constraint, new action channel, \(\varphi\)-selector, or global Einstein equation is used. The four-space is census data on one L4 orbit. It is not a local Lorentz quotient, and the #264 coframe descent is not a gauge deletion of the regular variables.

## 8. Validation

```bash
python3 02_REGISTRY/research/certificates/a4d_joint_diagonal_invisible_germ_check.py
python3 tools/validate_repo.py
python3 tools/validate_work.py
```
