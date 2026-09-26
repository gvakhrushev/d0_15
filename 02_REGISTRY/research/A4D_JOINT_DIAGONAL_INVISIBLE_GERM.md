# A4D diagonal invisible joint germ

**Task:** `WRK-A4D-JOINT-DIAGONAL-INVISIBLE-GERM`
**Class:** `WORKER`
**Research lane:** `EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS`
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
**Dependency:** `WRK-A4D-JOINT-RESONANCE-LINEAR-KERNEL` (PR #231). Its execution tip had not yet published the basis, so this certificate reconstructs the same diagonal \(N_0\) from the owned #208/#216 polarized symbol and records the basis it uses.
**Certificate:** `02_REGISTRY/research/certificates/a4d_joint_diagonal_invisible_germ_check.py`

## 0. Terminal

\[
\boxed{\texttt{J2-DIAGONAL-INVISIBLE-JOINT-VACUUM-GERM-FOUND}}
\]

The origin of the diagonal source-invisible sector is not isolated modulo gauge. One explicit curved family satisfies the joint system

\[
E_Q(\eta,K(t))=0,
\qquad
E_K(\eta,K(t))=0
\]

through connection order \(8\), with nonzero plaquette curvature at order \(1\). This is not an Einstein equation and not an all-orbit statement.

## 1. Invisible basis

At the diagonal quarter wave \(z_A=z_B=z_C=z_D=i\), the owned polarized connection symbol has rank \(16\) and an \(8\)-dimensional kernel with the integer basis \(\lambda_0,\ldots,\lambda_7\) of the diagonal certificate. The metric map \(H_{QA}\) on that kernel has a \(4\)-dimensional kernel. In that basis

\[
N_0=\operatorname{span}\{\lambda_1,\lambda_3,\lambda_4,\lambda_6\}.
\]

Explicitly, each vector lives on one Role:

| Basis | Role | Generator weights \((K_1,K_2,K_3,J_{12},J_{13},J_{23})\) |
|---|---|---|
| \(\lambda_1\) | \(0\) | \((0,0,0,1,-1,1)\) |
| \(\lambda_3\) | \(1\) | \((0,1,-1,0,0,1)\) |
| \(\lambda_4\) | \(2\) | \((1,0,-1,0,1,0)\) |
| \(\lambda_6\) | \(3\) | \((1,-1,0,1,0,0)\) |

\(\lambda_0=(1,1,1,0,0,0)\) on Role \(0\) pairs with \(q_{11}\) by \(-1-i\), so it lies in the source-visible complement, not in \(N_0\). The #216/#225 coordinates \((a,b)\) on \(\lambda_0\) and \((c,d)\) on \(w=\lambda_2+\lambda_5-\lambda_7\) are therefore disjoint from this sector. Their connection-only quartic does not decide the joint invisible germ.

## 2. The curved family

Let

\[
Y=J_{12}-J_{13}+J_{23}.
\]

The certificate checks \(Y^3+3Y=0\) and \(b(Y)\ne 0\). The cosine family on Role \(0\) is

\[
L_0(x)=\exp\bigl(t\,\sigma(\textstyle\sum_i x_i)\,Y\bigr),
\qquad
L_r=I\ (r\ne 0),
\]

with \(\sigma=(1,0,-1,0)\) on residues modulo \(4\). Every nontrivial plaquette is of the form \(\exp(aY)\) with \(a=t(\sigma(s)-\sigma(s+1))\). The odd part of the exponential therefore stays on the line of \(Y\):

\[
\mathcal R=\frac{\sinh(\sqrt 3\, a)}{\sqrt 3}\,Y.
\]

For \(t\ne 0\) one has \(a\ne 0\) on a positive-density set of faces, so the curvature is not identically zero.

The same sites \((0,0,0,0)\) and \((0,1,0,0)\) have equal \(x_0\) and unequal cosine weights. A pure gauge transformation of the identity that keeps every non-zero Role link at \(I\) would force \(L_0\) to depend only on \(x_0\). The family is not that gauge orbit.

## 3. Joint equations

**Metric.** At standard solder the complementary area of a face through Role \(0\) is spatial, while \(\star b(Y)\) is a pure boost. The diagonal bivector metric pairs them to \(0\), so every cell density vanishes and

\[
S_\star(\eta,K(t))=0.
\]

The solder derivative at \(\eta\) reduces to the sum of the three oriented complementary variations of the faces \((0,1),(0,2),(0,3)\) contracted with the fixed bivector \(b(Y)\). That covector is identically zero: all \(16\) leg components vanish. The common curvature scale of the three faces factors out, so this is not a small-\(t\) statement. Hence

\[
\boxed{E_Q(\eta,K(t))=0\qquad\text{for every }t.}
\]

**Connection.** An edge \(L_0(x)\) meets six plaquettes: the first corner of each face \((0,s)\) based at \(x\), and the inverse corner of the same faces based at \(x-e_s\). Differentiating the link logarithm in each of the six Lorentz generators and expanding in \(t\) gives the zero polynomial through degree \(8\). Therefore

\[
\boxed{E_K(\eta,K(t))=O(t^9)}
\]

as a Taylor jet at the identity, in every edge direction tested by those six generators. Together with the exact metric equation, the family is a curved joint vacuum through connection order \(8\).

The reduced joint germ on this ray is consequently

\[
E_K^{\rm red}=0+O(t^9),
\qquad
E_Q^{\rm red}=0.
\]

The first nonzero geometric invariant on the ray is the order-\(1\) curvature, not a nonzero Euler component.

## 4. Comparison

- #227 produces a source-visible connection-stationary curve whose metric partial on \(q_{11}\) tends to \(-1\) after \(h^{-2}\). That curve is cut by \(E_Q\). It is not this \(N_0\) family.
- #225 splits the frozen lines of the visible quartic \((a,b,c,d)\) under a slow phase detuning. Those coordinates are supported on \(\lambda_0\) and \(w\), the complement of \(N_0\). The splitting does not decide the invisible sector.
- The connection-only quartic on that visible four-space is not the joint reduced system computed here.

## 5. Boundary

The germ is one cosine ray in one diagonal orbit, certified through connection order \(8\). Sine weights and the other three \(N_0\) rays are the same kind of one-Role pattern; this certificate exhibits the Role-\(0\) ray rather than enumerating them. No torsion constraint, new action channel, or global Einstein claim is used.

## 6. Validation

```bash
python3 02_REGISTRY/research/certificates/a4d_joint_diagonal_invisible_germ_check.py
python3 tools/validate_repo.py
python3 tools/validate_work.py
```
