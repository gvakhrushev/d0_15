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
J2-DIAGONAL-INVISIBLE-LYAPUNOV-SCHMIDT-CORRECTION-MISSING
```

The origin-isolated terminal is not accepted. The calculation below proves that \(H_{AA}\) is injective on a complement of the diagonal kernel and then sets the regular coordinates to zero. That is not the Lyapunov–Schmidt elimination required by the brief.

The missing object is the solved correction \(r(u)=O(u^2)\) of the regular connection equations, substituted into \(E_Q\). A nonzero \(r_2(u)\) can enter the metric equation at the same quadratic order through the mixed block. Until that substitution is carried out on the conjugate-paired real carrier, neither isolation nor a curved germ is claimed.

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

## 4. Boundary

Section 2 is the odd-holonomy quadratic system with the regular coordinates set to zero. It is retained as a calculation, not as an isolation theorem. The first missing coefficient is the quadratic regular correction \(r_2(u)\) and its image under the mixed metric block.

No torsion constraint, new action channel, \(\varphi\)-selector, or global Einstein equation is used. The four-space is census data on one L4 orbit. It is not a local Lorentz quotient, and the #264 coframe descent is not a gauge deletion of the regular variables.

## 5. Validation

```bash
python3 02_REGISTRY/research/certificates/a4d_joint_diagonal_invisible_germ_check.py
python3 tools/validate_repo.py
python3 tools/validate_work.py
```
