# A4D joint cone: divisor strata of the Veronese kernel

**Companion to** `WRK-A4D-METRIC-NULL-HESSIAN-COMPLEX` (merged #270) and the
0/1-solder census of PR #279.
**Certificate:** `certificates/a4d_joint_cone_divisor_strata_check.py`

## Terminal

```
NO-DIVISOR-JUMP-NERONESE-LINE-IS-UNIVERSAL
```

## 1. What is being refined

#270 certifies, for the owned conjugate-paired symbol
\(C(z)=H_{AQ}(z)\) and the backward character difference \(d_r=z_r^{-1}-1\),

\[
\ker C(z)=\operatorname{span}\{d\,d^{T}\},\qquad \operatorname{rank}C(z)=9
\]
for every \(d\neq0\). The open question was the stratification of
\(N(z)=\ker C(z)\) across the divisor \(\bigcup_r\{z_r=1\}=\bigcup_r\{d_r=0\}\).

## 2. The divisor does not enlarge the kernel

On **all 174** characters of the \(L=4\) grid with at least one \(d_r=0\) and
\(d\neq0\), the kernel is still one-dimensional and still exactly
\(\operatorname{span}\{d\,d^{T}\}\). In particular \(q_0=d\,d^{T}\) stays in the
kernel at every divisor point: the extra directions the divisor was suspected
to carry do not exist as kernel directions.

The only jump in dimension on the grid is the trivial character
\(z=(1,1,1,1)\), where \(d=0\), \(C=0\) and the kernel is the whole
ten-dimensional metric space.

## 3. What the divisor does change

The divisor does not enlarge the kernel, but it decides whether the
\(q_{11}\) slot of the #240 shear witness survives inside that one-dimensional
line:

* \(q_{11}\) is present in the kernel span at **all 81** off-divisor characters;
* it is absent at **63 of the 174** divisor characters.

So the absence set is **confined to the divisor but is not all of it**. The 63 are
exactly the divisor points with role 1 on \(z_1=1\); the remaining 111 divisor
points keep \(q_{11}\). Being on the divisor is necessary but not sufficient for
losing \(q_{11}\).

## 4. Method note

The owned symbol carries **both** the \(z_j\) and the \(d_j\) symbols. An earlier
probe of mine substituted only the \(z_j\), which left \(d_j\) free and produced
a spurious off-divisor exception; that reading is withdrawn. The certificate
substitutes both families and reproduces the #270 identity at every point.

## 5. What this does and does not say

It says the divisor is a statement about *which slots survive*, not about
*how large the kernel is*. It does **not** give a criterion for which of the
81 surviving characters is selected by the physics, and it does not address
\(q_0\) trivialisation.

Boundary: the 256 characters of the \(L=4\) grid only. No other character class
is covered, and this is not a response NOGO.

## 6. Relation to the three pressures

The metric-null owner, the shear census and the two defect carriers are three
readings of the same distribution, and the table of nine points could not see
the cone. This certificate confirms the cone framing on the kernel side: the
Veronese line is universal, the divisor adds nothing to it, and the residual
selection question lives entirely in which slots survive along that line.
