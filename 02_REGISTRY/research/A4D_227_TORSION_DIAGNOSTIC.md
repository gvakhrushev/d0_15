# A4D #227 torsion diagnostic

**Task:** `WRK-A4D-227-TORSION-DIAGNOSTIC`  
**Class:** `WORKER`  
**Research lane:** `EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS`  
**Input:** merged #227, family \(L_0(x)=W_{p(x)}\), \(L_s(x)=I\) for \(s=1,2,3\), with \(W=(U,I,U^{-1},I)\) and \(U\) the Cayley transform of \(t(K_1+K_2+K_3)\).  
**Certificate:** `02_REGISTRY/research/certificates/a4d_227_torsion_diagnostic_check.py`

## 0. Terminal

\[
\boxed{\texttt{J2-227-CURVED-STATIONARY-FAMILY-TORSION-DIAGNOSTIC-CERTIFIED}}
\]

Torsion-free is not added as a field equation. No \(T_{\rm open}^2\) term is introduced. Raw open torsion is not claimed to be a legal full-affine scalar. The calculation is a branch diagnostic compatible with the existing Palatini equations.

## 1. Canonical formula

The coframe torsion used here is the owned transport at a solder frame \(v\),

\[
T_{rs}(x)
=
L_r(x)\,v_s(x+e_r)-v_s(x)
-
\bigl(L_s(x)\,v_r(x+e_s)-v_r(x)\bigr).
\]

At the constant standard solder \(v_r=e_r\) this is exactly

\[
\boxed{T_{rs}(x)=(L_r(x)-I)e_s-(L_s(x)-I)e_r.}
\]

The schematic is therefore correct for this convention. It is not the affine open torsion of `affineOpenTorsion`, which is a difference of translation shifts. The #227 links are pure Lorentz matrices, so that translation defect is the zero vector on every phase and face, for every \(t\).

## 2. Exact phase and face table

Write \(D=4-3t^2\), \(c(t)=4t/D\), \(B=K_1+K_2+K_3\), and \(e_\Sigma=e_1+e_2+e_3\). In the chart \(D\neq 0\),

| Phase | Spatial faces \((r,s)\ge 1\) | Faces \((0,s)\) |
|---|---|---|
| \(0\) | \(T=0\), curvature \(0\) | \(T_{0s}=(U-I)e_s=c\,e_0+(2t^2/D)\,e_\Sigma\), curvature \(cB\) |
| \(1\) | \(T=0\), curvature \(0\) | \(T_{0s}=0\), curvature \(cB\) |
| \(2\) | \(T=0\), curvature \(0\) | \(T_{0s}=(U^{-1}-I)e_s=-c\,e_0+(2t^2/D)\,e_\Sigma\), curvature \(-cB\) |
| \(3\) | \(T=0\), curvature \(0\) | \(T_{0s}=0\), curvature \(-cB\) |

The value depends on the phase of the base site only. Every ordered face is the negative of its swap.

## 3. Corrected vanishing statement

The time component of \(T_{01}\) at phase \(0\) is exactly \(c(t)\). Thus \(c(t)=0\) if and only if \(t=0\) whenever \(D\neq 0\). Combined with the table,

\[
\boxed{
T=0\text{ on every phase and every face}
\iff
t=0
}
\]

in the near-identity chart \(3t^2\neq 4\).

The phasewise reading is false. Phases \(1\) and \(3\) have \(T=0\) for every \(t\), while their curvature is \(\pm c(t)B\) and their metric partial remains \(\pm c(t)\,m\), with the owned direction

\[
m=(0,0,0,0,-1,1,1,-1,1,-1).
\]

Torsion-free does not cut the #227 family down to the identity one phase at a time. Requiring it on all phases does.

## 4. Leading order against curvature and \(E_Q\)

\[
c(t)=t+O(t^3).
\]

On the active phases the torsion is \(c\,e_0+O(t^2)\). The plaquette curvature is exactly \(\pm c(t)B\), and the metric partial is exactly \(\pm c(t)\,m\). All three are order \(t\) and share the amplitude \(c(t)\). They are different tensors: torsion leads along \(e_0\), curvature along \(B\), and \(E_Q\) along \(m\).

At \(t=0\) all three vanish and the links are the identity. For \(t\neq 0\) inside the chart, curvature and \(E_Q\) are nonzero on every phase, including the two phases whose coframe torsion vanishes.

## 5. Validation

```bash
python3 02_REGISTRY/research/certificates/a4d_227_torsion_diagnostic_check.py
python3 tools/validate_work.py
python3 tools/validate_repo.py
```
