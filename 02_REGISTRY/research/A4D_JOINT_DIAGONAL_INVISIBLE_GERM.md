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

The origin of the diagonal source-invisible sector is not isolated modulo gauge. One explicit curved family has nonzero plaquette curvature and satisfies

\[
E_Q(\eta,K(t))=0
\]

for every amplitude, together with \(E_K=0\) on every Role-0 edge. This is not an Einstein equation and not an all-orbit statement.

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

**Connection, excited edges.** A Role-0 edge on a residue whose cosine weight is nonzero has identity partner link. Its forward plaquette is some \(U\in\exp(\mathbb R Y)\) and its backward plaquette is \(U^{-1}\), with the same complementary area and the same face orientation. Curvature extraction is odd, \(\mathcal R(U^{-1})=-\mathcal R(U)\), so the two cell densities cancel for every \(t\) and every Lorentz tangent of that edge. On a zero-weight Role-0 residue the neighbor carries \(\exp(\pm t Y)\). The closed-form derivative of those six plaquettes is the zero function of \(t\) for each of the six Lorentz generators.

**Connection, one non-excited edge.** The certificate also expands the edge Euler of Role \(2\) at residue \(1\), in all six generators, through degree \(4\) in \(t\). Every coefficient is zero. Edges of Roles \(1\) and \(3\) are the same residue-class calculation with a different fixed direction; they are not given a separate exact block here.

The reduced joint germ on the Role-0 ray is therefore

\[
E_Q^{\rm red}=0,
\qquad
E_K^{\rm red}=0
\]

on every Role-0 edge, with the displayed Role-2 jet also zero through degree \(4\). The first nonzero geometric invariant on the ray is the order-\(1\) curvature.

## 4. Comparison

- #227 produces a source-visible connection-stationary curve whose metric partial on \(q_{11}\) tends to \(-1\) after \(h^{-2}\). That curve is cut by \(E_Q\). It is not this \(N_0\) family.
- #225 splits the frozen lines of the visible quartic \((a,b,c,d)\) under a slow phase detuning. Those coordinates are supported on \(\lambda_0\) and \(w\), the complement of \(N_0\). The splitting does not decide the invisible sector.
- The connection-only quartic on that visible four-space is not the joint reduced system computed here.

## 5. Boundary

The certified germ is the Role-0 cosine ray only. \(\lambda_3,\lambda_4,\lambda_6\) contain boost generators, so they are not the same spatial-rotation family and are not claimed to be vacua. Sine weights are not given a separate block. No torsion constraint, new action channel, or global Einstein claim is used.

## 6. Validation

```bash
python3 02_REGISTRY/research/certificates/a4d_joint_diagonal_invisible_germ_check.py
python3 tools/validate_repo.py
python3 tools/validate_work.py
```
